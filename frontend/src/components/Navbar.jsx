import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../services/api';

export default function Navbar({ user, setUser }) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    authService.logout();
    setUser(null);
    navigate('/login');
  };

  const isActive = (path) => (location.pathname === path ? 'active' : '');

  return (
    <div className="navbar">
      <Link to="/" className="logo" style={{ textDecoration: 'none' }}>
        Career<span>Cast</span>
      </Link>

      <div className="nav-links">
        <Link to="/dashboard" className={isActive('/dashboard')}>
          {user?.role === 'admin' ? 'Analyzer View' : 'Analyze Resume'}
        </Link>
        {user?.role === 'admin' && (
          <Link to="/admin" className={isActive('/admin')}>
            Admin Overview
          </Link>
        )}
        {user && (
          <Link to="/profile" className={isActive('/profile')}>
            Profile
          </Link>
        )}
      </div>

      <div className="nav-actions">
        {user ? (
          <>
            <span style={{ fontSize: '13.5px', color: 'var(--muted)', fontWeight: '500', marginRight: '6px' }}>
              {user.name} ({user.role})
            </span>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-text">
              Login
            </Link>
            <Link to="/register" className="btn btn-primary">
              Register
            </Link>
          </>
        )}
      </div>
    </div>
  );
}
