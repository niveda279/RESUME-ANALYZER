import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-top">
        <div>
          <div className="logo">
            Career<span>Cast</span>
          </div>
          <p>
            AI-powered resume analysis built to help candidates present recruiter-ready applications.
          </p>
        </div>
        <div className="footer-links">
          <div className="footer-col">
            <h4>Product</h4>
            <Link to="/dashboard">Analyze Resume</Link>
            <Link to="/dashboard">Dashboard</Link>
          </div>
          <div className="footer-col">
            <h4>Account</h4>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <span>© 2026 CareerCast. All rights reserved.</span>
        <span>Made for academic & portfolio use</span>
      </div>
    </footer>
  );
}
