import React, { useState, useEffect } from 'react';
import {
  Server,
  Database,
  ShieldCheck,
  HardDrive,
  RefreshCw,
  Plus,
  Trash2,
  Clock,
  Layers
} from 'lucide-react';

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [health, setHealth] = useState(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const fetchHealth = async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setHealth(data);
      }
    } catch (err) {
      console.error('Failed to fetch health info:', err);
    }
  };

  const fetchTasks = async () => {
    try {
      const res = await fetch('/api/tasks');
      if (res.ok) {
        const data = await res.json();
        setTasks(data);
      }
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    }
  };

  const refreshAll = async () => {
    setRefreshing(true);
    await Promise.all([fetchHealth(), fetchTasks()]);
    setRefreshing(false);
  };

  useEffect(() => {
    refreshAll();
  }, []);

  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    try {
      const res = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description }),
      });
      if (res.ok) {
        setTitle('');
        setDescription('');
        await fetchTasks();
      }
    } catch (err) {
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTask = async (task) => {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed';
    try {
      const res = await fetch(`/api/tasks/${task.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });
      if (res.ok) {
        setTasks((prev) =>
          prev.map((t) => (t.id === task.id ? { ...t, status: newStatus } : t))
        );
      }
    } catch (err) {
      console.error('Error toggling task:', err);
    }
  };

  const handleDeleteTask = async (id) => {
    try {
      const res = await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setTasks((prev) => prev.filter((t) => t.id !== id));
      }
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const isDbConnected = health?.database?.status === 'connected';

  return (
    <div className="apple-app">
      <header className="apple-header">
        <div className="apple-top-bar">
          <div>
            <div className="student-tag">
              Assignment 2 &bull; DevOps
            </div>
            <h1 className="apple-title">Cloud Deployment Platform</h1>
            <p className="apple-subtitle">
              Parallel and Distributed Computing &bull; Multi-Container Architecture on AWS EC2
            </p>
            <div className="student-details">
              <span>Developer: <strong className="student-name">ABDULLAH</strong></span>
              <span>Registration ID: <strong className="student-reg">FA23-BSE-137</strong></span>
            </div>
          </div>

          <button
            onClick={refreshAll}
            className="apple-btn-secondary"
            disabled={refreshing}
          >
            <RefreshCw size={14} className={refreshing ? 'animate-spin' : ''} />
            {refreshing ? 'Syncing...' : 'Refresh'}
          </button>
        </div>

        <div className="telemetry-grid">
          <div className="telemetry-card">
            <span className="telemetry-label">Database Server</span>
            <div className="telemetry-value">
              <span className={`status-dot ${isDbConnected ? 'active' : ''}`} />
              {isDbConnected ? 'PostgreSQL Active' : 'Disconnected'}
            </div>
          </div>

          <div className="telemetry-card">
            <span className="telemetry-label">Container Node</span>
            <div className="telemetry-value font-mono">
              <code>{health?.container?.hostname || 'pdc_web_app'}</code>
            </div>
          </div>

          <div className="telemetry-card">
            <span className="telemetry-label">Secrets Manager</span>
            <div className="telemetry-value font-mono">
              /run/secrets (Mounted)
            </div>
          </div>

          <div className="telemetry-card">
            <span className="telemetry-label">Persistence Volume</span>
            <div className="telemetry-value font-mono">
              pdc_db_data (Attached)
            </div>
          </div>
        </div>
      </header>

      <section className="apple-card">
        <h2 className="card-heading">Add Record</h2>
        <form onSubmit={handleCreateTask} className="apple-form">
          <div className="form-inputs">
            <input
              type="text"
              placeholder="Record title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="apple-input"
              required
            />
            <input
              type="text"
              placeholder="Description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="apple-input"
            />
            <button
              type="submit"
              className="apple-btn-primary"
              disabled={loading || !title.trim()}
            >
              <Plus size={15} />
              {loading ? 'Adding...' : 'Add'}
            </button>
          </div>
        </form>
      </section>

      <section className="apple-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h2 className="card-heading" style={{ margin: 0 }}>
            Stored Records ({tasks.length})
          </h2>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
            PostgreSQL Named Volume
          </span>
        </div>

        {tasks.length === 0 ? (
          <div className="empty-state">
            <p>No records stored in the database. Create one above to verify volume persistence.</p>
          </div>
        ) : (
          <div className="task-list">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`task-row ${task.status === 'completed' ? 'completed' : ''}`}
              >
                <div className="task-left">
                  <input
                    type="checkbox"
                    className="apple-checkbox"
                    checked={task.status === 'completed'}
                    onChange={() => handleToggleTask(task)}
                  />
                  <div className="task-info">
                    <span className="task-title">{task.title}</span>
                    {task.description && (
                      <span className="task-desc">{task.description}</span>
                    )}
                    <span className="task-meta">
                      ID #{task.id} &bull; {new Date(task.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="apple-btn-delete"
                  title="Delete record"
                >
                  <Trash2 size={15} />
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      <footer className="apple-footer">
        <p><strong>CSC336 - Parallel and Distributed Computing</strong> &bull; Assignment 2</p>
        <p>Student: <strong>ABDULLAH</strong> &bull; Registration: <strong>FA23-BSE-137</strong></p>
        <p>Multi-Stage Dockerfile &bull; Docker Compose Secrets &bull; PostgreSQL 16 Named Volume</p>
      </footer>
    </div>
  );
}
