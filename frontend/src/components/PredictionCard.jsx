import React from 'react';

export default function PredictionCard({ prediction }) {
  if (!prediction) return null;

  const { predicted_role, confidence, breakdown } = prediction;

  return (
    <div className="card" style={{ marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
        <h3 className="card-title" style={{ marginBottom: 0 }}>Career Path Prediction</h3>
        <span className="hero-eyebrow" style={{ margin: 0, padding: '4px 10px', fontSize: '11.5px' }}>
          <span className="dot"></span> Logistic Regression Classifier
        </span>
      </div>

      <div style={{
        background: 'var(--light)',
        border: '1px solid var(--border)',
        borderRadius: '10px',
        padding: '20px',
        textAlign: 'center',
        marginBottom: '20px'
      }}>
        <div style={{ fontSize: '12px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '.04em', fontWeight: '600' }}>
          Predicted Role Match
        </div>
        <div style={{ fontSize: '28px', fontWeight: '700', fontFamily: 'Poppins, sans-serif', color: 'var(--dark)', margin: '6px 0' }}>
          {predicted_role}
        </div>
        {confidence && (
          <div style={{ fontSize: '13px', color: 'var(--primary-dark)', fontWeight: '600' }}>
            Classifier Confidence: {confidence}%
          </div>
        )}
      </div>

      {breakdown && breakdown.length > 0 && (
        <div className="skills-card" style={{ marginBottom: 0 }}>
          <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--dark)', marginBottom: '12px' }}>
            Role Probability Distribution
          </div>
          {breakdown.map((item, idx) => (
            <div key={idx} className="skill-row">
              <div className="sr-top">
                <span className="sname">{item.role}</span>
                <span className="sval">{item.probability}%</span>
              </div>
              <div className="bar-track">
                <div className="bar-fill" style={{ width: `${item.probability}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
