import fs from 'fs';
import pkg from 'pg';
const { Pool } = pkg;

function getSecret(secretName, envVar, fallback) {
  const secretPath = `/run/secrets/${secretName}`;
  try {
    if (fs.existsSync(secretPath)) {
      return fs.readFileSync(secretPath, 'utf8').trim();
    }
  } catch (err) {
    console.warn(`Could not read secret file at ${secretPath}: ${err.message}`);
  }
  return process.env[envVar] || fallback;
}

const dbUser = getSecret('db_user', 'DB_USER', 'postgres');
const dbPassword = getSecret('db_password', 'DB_PASSWORD', 'postgres_password');
const dbName = getSecret('db_name', 'DB_NAME', 'pdc_assignment');
const dbHost = process.env.DB_HOST || 'localhost';
const dbPort = parseInt(process.env.DB_PORT || '5432', 10);

console.log(`[Database] Configuring connection to host: ${dbHost}, port: ${dbPort}, database: ${dbName}, user: ${dbUser}`);

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

export async function initDatabase(retries = 10, delay = 3000) {
  for (let i = 1; i <= retries; i++) {
    try {
      console.log(`[Database] Attempting connection (${i}/${retries})...`);
      const client = await pool.connect();
      console.log('[Database] Successfully connected to PostgreSQL.');

      await client.query(`
        CREATE TABLE IF NOT EXISTS tasks (
          id SERIAL PRIMARY KEY,
          title VARCHAR(255) NOT NULL,
          description TEXT,
          status VARCHAR(50) DEFAULT 'pending',
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
      `);

      // Seed initial data if empty
      const countRes = await client.query('SELECT COUNT(*) FROM tasks');
      if (parseInt(countRes.rows[0].count, 10) === 0) {
        await client.query(`
          INSERT INTO tasks (title, description, status) VALUES
          ('Configure AWS EC2', 'Launch an Amazon EC2 instance with Ubuntu and configure security groups', 'completed'),
          ('Implement Multistage Dockerfile', 'Build React in Stage 1 and serve using minimal Node runtime in Stage 2', 'completed'),
          ('Setup Docker Secrets & Volumes', 'Secure DB credentials with Docker secrets and persist data with named volume', 'in-progress');
        `);
        console.log('[Database] Seeded initial sample tasks.');
      }

      client.release();
      return true;
    } catch (err) {
      console.warn(`[Database] Connection attempt ${i} failed: ${err.message}`);
      if (i === retries) {
        console.error('[Database] Max retries reached. Database initialization failed.');
        throw err;
      }
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
}
