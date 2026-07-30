import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import Profile from './pages/Profile';
import Analysis from './pages/Analysis';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem('careercast_user');
    const storedToken = localStorage.getItem('careercast_token');
    if (storedUser && storedToken) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        localStorage.removeItem('careercast_user');
        localStorage.removeItem('careercast_token');
      }
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontFamily: 'Inter, sans-serif' }}>
        <p style={{ color: '#4b5563' }}>Initializing CareerCast Resume Analyzer...</p>
      </div>
    );
  }

  return (
    <Router>
      <div style={{ minHeight: '100vh', backgroundColor: 'var(--bg-main)' }}>
        <Navbar user={user} setUser={setUser} />
        <Routes>
          <Route
            path="/login"
            element={!user ? <Login setUser={setUser} /> : <Navigate to={user.role === 'admin' ? '/admin' : '/dashboard'} replace />}
          />
          <Route
            path="/register"
            element={!user ? <Register setUser={setUser} /> : <Navigate to="/dashboard" replace />}
          />

          <Route
            path="/dashboard"
            element={user ? <Dashboard user={user} /> : <Navigate to="/login" replace />}
          />
          <Route
            path="/analysis/:id"
            element={user ? <Analysis /> : <Navigate to="/login" replace />}
          />
          <Route
            path="/profile"
            element={user ? <Profile user={user} /> : <Navigate to="/login" replace />}
          />

          {/* Admin Protected Route */}
          <Route
            path="/admin"
            element={user && user.role === 'admin' ? <AdminDashboard /> : <Navigate to={user ? '/dashboard' : '/login'} replace />}
          />

          {/* Fallback */}
          <Route
            path="*"
            element={<Navigate to={user ? (user.role === 'admin' ? '/admin' : '/dashboard') : '/login'} replace />}
          />
        </Routes>
      </div>
    </Router>
  );
}
