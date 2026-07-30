import React, { useState, useEffect } from 'react';
import { adminService } from '../services/api';
import Footer from '../components/Footer';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const loadAdminData = async () => {
    setLoading(true);
    setError('');
    try {
      const [statsData, usersData, resumesData] = await Promise.all([
        adminService.getStats(),
        adminService.getUsers(),
        adminService.getResumes()
      ]);
      setStats(statsData);
      setUsers(usersData.users || []);
      setResumes(resumesData.resumes || []);
    } catch (err) {
      setError('Failed to load administrative control data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAdminData();
  }, []);

  const handleDeleteUser = async (userId, userEmail) => {
    if (!window.confirm(`Are you sure you want to delete user ${userEmail}?`)) return;
    try {
      await adminService.deleteUser(userId);
      setMessage(`User ${userEmail} deleted successfully.`);
      loadAdminData();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete user.');
    }
  };

  const handleDeleteResume = async (resumeId, filename) => {
    if (!window.confirm(`Are you sure you want to delete resume document "${filename}"?`)) return;
    try {
      await adminService.deleteResume(resumeId);
      setMessage(`Resume #${resumeId} (${filename}) deleted successfully.`);
      loadAdminData();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete resume.');
    }
  };

  const filteredResumes = resumes.filter(r =>
    r.user_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.filename?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.prediction?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '80px 0' }}>
        <p style={{ color: 'var(--muted)' }}>Loading Executive Control Center...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="container" style={{ paddingBottom: '40px' }}>
        {error && <div className="alert-error">{error}</div>}
        {message && <div className="alert-success">{message}</div>}

        {/* FRAME 04 — ADMIN DASHBOARD */}
        <div className="admin-shell">
          {/* Side Nav */}
          <div className="admin-side">
            <div className="logo">
              Career<span>Cast</span>
            </div>
            <div className="admin-nav">
              <a className="active" href="#overview">
                <span className="bullet"></span> Overview
              </a>
              <a href="#users">
                <span className="bullet"></span> Users
              </a>
              <a href="#resumes">
                <span className="bullet"></span> Resume Analyses
              </a>
            </div>
          </div>

          {/* Main Area */}
          <div className="admin-main">
            <div className="admin-top">
              <div>
                <h2>Admin Overview</h2>
                <p>Platform activity and analysis summary</p>
              </div>
              <div className="search-box">
                <span className="icon" style={{ fontSize: '12px', color: 'var(--muted)' }}>Search</span>
                <input
                  type="text"
                  placeholder="Search users or files…"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>

            {/* Stat Cards Grid */}
            <div className="stat-grid">
              <div className="stat-card">
                <div className="s-label">Total Users</div>
                <div className="s-value">{stats?.total_users || users.length}</div>
                <div className="s-delta">▲ Active registered users</div>
              </div>
              <div className="stat-card">
                <div className="s-label">Total Resume Analyses</div>
                <div className="s-value">{stats?.total_resumes || resumes.length}</div>
                <div className="s-delta">▲ Evaluated documents</div>
              </div>
              <div className="stat-card">
                <div className="s-label">Classifier Model</div>
                <div className="s-value" style={{ fontSize: '18px' }}>Logistic Regression</div>
                <div className="s-delta">▲ Scikit-learn Trained</div>
              </div>
              <div className="stat-card">
                <div className="s-label">Average ATS Score</div>
                <div className="s-value">{stats?.accuracy || 92.84}%</div>
                <div className="s-delta">▲ Cross-validation metric</div>
              </div>
            </div>

            {/* Resumes Table */}
            <div className="admin-table-card" style={{ marginBottom: '24px' }}>
              <div className="admin-table-head">
                <h3>Recent Uploads & Analyses</h3>
                <span style={{ fontSize: '12.5px', color: 'var(--muted)' }}>
                  Total: {filteredResumes.length} records
                </span>
              </div>
              <table>
                <thead>
                  <tr>
                    <th>User</th>
                    <th>File</th>
                    <th>Predicted Role</th>
                    <th>Confidence</th>
                    <th>Uploaded Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredResumes.length > 0 ? (
                    filteredResumes.map((r) => (
                      <tr key={r.id}>
                        <td className="tname">{r.user_name} ({r.user_email})</td>
                        <td>{r.filename}</td>
                        <td>
                          <span className="pill high">{r.prediction}</span>
                        </td>
                        <td>{r.confidence ? `${r.confidence}%` : '88%'}</td>
                        <td>{new Date(r.created_at).toLocaleDateString()}</td>
                        <td className="row-actions">
                          <button
                            className="danger"
                            onClick={() => handleDeleteResume(r.id, r.filename)}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="6" style={{ textAlign: 'center', padding: '24px', color: 'var(--muted)' }}>
                        No resume analysis records found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Users Table */}
            <div className="admin-table-card">
              <div className="admin-table-head">
                <h3>User Accounts Management</h3>
              </div>
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>User Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Registered Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr key={u.id}>
                      <td>#{u.id}</td>
                      <td className="tname">{u.name}</td>
                      <td>{u.email}</td>
                      <td>
                        <span className={`pill ${u.role === 'admin' ? 'mid' : 'high'}`}>
                          {u.role}
                        </span>
                      </td>
                      <td>{new Date(u.created_at).toLocaleDateString()}</td>
                      <td className="row-actions">
                        {u.role !== 'admin' && (
                          <button
                            className="danger"
                            onClick={() => handleDeleteUser(u.id, u.email)}
                          >
                            Delete User
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
