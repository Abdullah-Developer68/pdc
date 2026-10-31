import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pkg from 'pg';
const { Pool } = pkg;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function getSecret(secretName, envVar, fallback) {
  const candidatePaths = [
    `/run/secrets/${secretName}`,
    path.resolve(process.cwd(), 'secrets', `${secretName}.txt`),
    path.resolve(__dirname, '..', 'secrets', `${secretName}.txt`),
    path.resolve(__dirname, 'secrets', `${secretName}.txt`),
  ];

  for (const sPath of candidatePaths) {
    try {
      if (fs.existsSync(sPath)) {
        const val = fs.readFileSync(sPath, 'utf8').trim();
        if (val) {
          return val;
        }
      }
    } catch (_) {
    }
  }

  return process.env[envVar] || fallback;
}

const dbUser = getSecret('db_user', 'DB_USER', 'pdc_user');
const dbPassword = getSecret('db_password', 'DB_PASSWORD', 'pdc_secure_password_2026');
const dbName = getSecret('db_name', 'DB_NAME', 'pdc_assignment_db');
const dbHost = process.env.DB_HOST || 'localhost';
const dbPort = parseInt(process.env.DB_PORT || '5432', 10);

export const pool = new Pool({
  host: dbHost,
  port: dbPort,
  user: dbUser,
  password: dbPassword,
  database: dbName,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('error', (err) => {
  console.error('[Database Pool Error]:', err.message);
});

export async function initDatabase(retries = 15, delay = 2000) {
  for (let i = 1; i <= retries; i++) {
    try {
      const client = await pool.connect();

      await client.query(`
        CREATE TABLE IF NOT EXISTS tasks (
          id SERIAL PRIMARY KEY,
          title VARCHAR(255) NOT NULL,
          description TEXT,
          status VARCHAR(50) DEFAULT 'pending',
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
      `);

      const countRes = await client.query('SELECT COUNT(*) FROM tasks');
      if (parseInt(countRes.rows[0].count, 10) === 0) {
        await client.query(`
          INSERT INTO tasks (title, description, status) VALUES
          ('Configure AWS EC2', 'Launch an Amazon EC2 instance with Ubuntu and configure security groups', 'completed'),
          ('Implement Multistage Dockerfile', 'Build React in Stage 1 and serve using minimal Node runtime in Stage 2', 'completed'),
          ('Setup Docker Secrets & Volumes', 'Secure DB credentials with Docker secrets and persist data with named volume', 'in-progress');
        `);
      }

      client.release();
      return true;
    } catch (err) {
      if (i === retries) {
        throw err;
      }
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
}
