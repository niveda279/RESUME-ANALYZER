import React from 'react';

export default function Profile({ user }) {
  if (!user) return null;

  return (
    <div className="container" style={{ maxWidth: '640px' }}>
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">User Account Profile</h2>
            <p className="card-subtitle">Personal information and access credentials</p>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Full Name</label>
          <input className="form-input" value={user.name} disabled readOnly />
        </div>

        <div className="form-group">
          <label className="form-label">Email Address</label>
          <input className="form-input" value={user.email} disabled readOnly />
        </div>

        <div className="form-group">
          <label className="form-label">Role Authorization</label>
          <div>
            <span className="tag tag-blue" style={{ fontSize: '0.9rem', padding: '6px 14px' }}>
              {user.role}
            </span>
          </div>
        </div>

        <div style={{ marginTop: '24px', paddingTop: '16px', borderTop: '1px solid var(--border-color)', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Account protection powered by JWT token authentication and bcrypt password hashing.
        </div>
      </div>
    </div>
  );
}
