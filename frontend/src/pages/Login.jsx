import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/api';
import Footer from '../components/Footer';

export default function Login({ setUser }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await authService.login(email, password);
      localStorage.setItem('careercast_token', data.token);
      localStorage.setItem('careercast_user', JSON.stringify(data.user));
      setUser(data.user);

      if (data.user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="auth-body">
        <div className="auth-box">
          <div className="abadge">Welcome back</div>
          <h2>Log in to CareerCast</h2>
          <p className="a-sub">Access your resume reports and analysis history.</p>

          {error && <div className="alert-error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label>Email Address</label>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="field">
              <label>Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
              {loading ? 'Authenticating...' : 'Login'}
            </button>
          </form>

          <div className="auth-foot">
            Don't have an account? <Link to="/register">Register</Link>
          </div>

          <div style={{ marginTop: '24px', paddingTop: '16px', borderTop: '1px solid var(--border)', fontSize: '12px', color: 'var(--muted)', textAlign: 'center' }}>
            <p><strong>Demo Credentials:</strong></p>
            <p>User: user@careercast.com / User@123456</p>
            <p>Admin: admin@careercast.com / Admin@123456</p>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
