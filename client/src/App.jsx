import React, { useState, useEffect } from 'react';
import {
  Server,
  Database,
  ShieldCheck,
  HardDrive,
  RefreshCw,
  Plus,
  Trash2,
  CheckCircle2,
  Clock,
  Layers,
  Cloud
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
    <div className="container">
      {/* Header */}
      <header className="header">
        <div className="title-row">
          <div className="title-group">
            <div className="logo-icon">
              <Layers size={28} />
            </div>
            <div>
              <h1>Cloud Task Manager</h1>
              <p className="subtitle">
                CSC336 DevOps Assignment 2 &bull; Multi-Container AWS EC2 Architecture
              </p>
            </div>
          </div>

          <button
            onClick={refreshAll}
            className="btn btn-secondary"
            title="Refresh status and tasks"
            disabled={refreshing}
          >
            <RefreshCw size={16} className={refreshing ? 'animate-spin' : ''} />
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>

        {/* System & Container Metadata */}
        <div className="meta-grid">
          <div className="meta-card">
            <span className="meta-label">
              <Database size={14} /> Database Server
            </span>
            <div className="meta-value">
              <span
                className={`status-indicator ${
                  isDbConnected ? 'status-online' : 'status-offline'
                }`}
              />
              {isDbConnected ? 'PostgreSQL Active' : 'Disconnected'}
            </div>
          </div>

          <div className="meta-card">
            <span className="meta-label">
              <Server size={14} /> Web Container Host
            </span>
            <div className="meta-value font-mono">
              <code>{health?.container?.hostname || 'pdc_web_app'}</code>
            </div>
          </div>

          <div className="meta-card">
            <span className="meta-label">
              <ShieldCheck size={14} /> Docker Secrets
            </span>
            <div className="meta-value" style={{ color: 'var(--accent-green)' }}>
              Enabled (/run/secrets)
            </div>
          </div>

          <div className="meta-card">
            <span className="meta-label">
              <HardDrive size={14} /> Named Volume
            </span>
            <div className="meta-value" style={{ color: 'var(--accent-blue)' }}>
              pdc_db_data (Persistent)
            </div>
          </div>
        </div>

        {/* Feature Pills */}
        <div className="features-pills">
          <span className="pill">
            <Layers size={13} /> Multi-Stage Dockerfile (Build + Alpine Runtime)
          </span>
          <span className="pill pill-green">
            <ShieldCheck size={13} /> Docker Compose Secrets
          </span>
          <span className="pill pill-purple">
            <Cloud size={13} /> Amazon EC2 Ready (IaaS)
          </span>
        </div>
      </header>

      {/* Task Creation Form */}
      <div className="card">
        <h2 style={{ fontSize: '1.15rem', marginBottom: '1rem', fontWeight: 600 }}>
          Create New Task / Record
        </h2>
        <form onSubmit={handleCreateTask} className="form-group">
          <div className="input-row">
            <input
              type="text"
              placeholder="Task Title (e.g. Deploy to EC2)"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !title.trim()}
            >
              <Plus size={18} />
              {loading ? 'Adding...' : 'Add Task'}
            </button>
          </div>
        </form>
      </div>

      {/* Task List */}
      <div className="card">
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '1rem',
          }}
        >
          <h2 style={{ fontSize: '1.15rem', fontWeight: 600 }}>
            Stored Records in PostgreSQL ({tasks.length})
          </h2>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Persists across container restarts via named volume
          </span>
        </div>

        {tasks.length === 0 ? (
          <div className="empty-state">
            <Clock size={40} style={{ opacity: 0.3, marginBottom: '0.5rem' }} />
            <p>No tasks found in the database. Add one above to test persistence!</p>
          </div>
        ) : (
          <div className="task-list">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`task-item ${task.status === 'completed' ? 'completed' : ''}`}
              >
                <div className="task-main">
                  <input
                    type="checkbox"
                    className="task-checkbox"
                    checked={task.status === 'completed'}
                    onChange={() => handleToggleTask(task)}
                  />
                  <div className="task-content">
                    <span className="task-title">{task.title}</span>
                    {task.description && (
                      <span className="task-desc">{task.description}</span>
                    )}
                    <span className="task-date">
                      ID: #{task.id} &bull; Created:{' '}
                      {new Date(task.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="btn btn-danger"
                  title="Delete Task"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>
          CSC336 - Parallel and Distributed Computing (DevOps) &bull; Assignment 2
        </p>
        <p style={{ marginTop: '0.25rem', fontSize: '0.8rem' }}>
          Containerized with Multi-Stage Docker &bull; Docker Compose Secrets &bull; PostgreSQL Named Volume
        </p>
      </footer>
    </div>
  );
}
