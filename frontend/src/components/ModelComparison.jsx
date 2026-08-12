import React from 'react';

/**
 * ModelComparison — Renders a comparison table and feature importance charts
 * for Logistic Regression, Random Forest, and XGBoost.
 */
export default function ModelComparison({ allMetrics }) {
  if (!allMetrics) return null;

  const lr  = allMetrics.logistic_regression || {};
  const rf  = allMetrics.random_forest || {};
  const xgb = allMetrics.xgboost || {};
  const bestKey  = allMetrics.best_model_key || 'logistic_regression';
  const bestName = allMetrics.best_model || 'Logistic Regression';

  const models = [
    { key: 'logistic_regression', label: 'Logistic Regression', data: lr, color: '#6366f1' },
    { key: 'random_forest',       label: 'Random Forest',        data: rf, color: '#10b981' },
    { key: 'xgboost',             label: 'XGBoost',              data: xgb, color: '#f59e0b' },
  ];

  const metricKeys = ['accuracy', 'precision', 'recall', 'f1_score'];
  const metricLabels = { accuracy: 'Accuracy', precision: 'Precision', recall: 'Recall', f1_score: 'F1 Score' };

  return (
    <div>
      {/* Model Comparison Table */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', flexWrap: 'wrap', gap: '8px' }}>
          <h3 className="card-title" style={{ marginBottom: 0 }}>ML Model Performance Comparison</h3>
          <span className="hero-eyebrow" style={{ margin: 0, padding: '4px 12px', fontSize: '11.5px' }}>
            <span className="dot"></span> Best Model: <strong>{bestName}</strong>
          </span>
        </div>

        {/* Comparison Cards Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: '16px',
          marginBottom: '24px'
        }}>
          {models.map((m) => (
            <div key={m.key} style={{
              background: m.key === bestKey
                ? 'linear-gradient(135deg, rgba(99,102,241,0.08), rgba(16,185,129,0.08))'
                : 'var(--light)',
              border: m.key === bestKey ? '2px solid var(--primary)' : '1px solid var(--border)',
              borderRadius: '12px',
              padding: '18px',
              position: 'relative',
              transition: 'transform 0.2s ease, box-shadow 0.2s ease',
            }}>
              {m.key === bestKey && (
                <div style={{
                  position: 'absolute', top: '-10px', right: '12px',
                  background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
                  color: '#fff', fontSize: '10px', fontWeight: '700',
                  padding: '3px 10px', borderRadius: '20px',
                  letterSpacing: '.04em', textTransform: 'uppercase'
                }}>
                  ★ Best
                </div>
              )}
              <div style={{
                fontSize: '14px', fontWeight: '700', color: m.color,
                marginBottom: '14px', fontFamily: 'Poppins, sans-serif'
              }}>
                {m.label}
              </div>

              {metricKeys.map((mk) => (
                <div key={mk} style={{ marginBottom: '10px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                    <span style={{ color: 'var(--muted)', fontWeight: '500' }}>{metricLabels[mk]}</span>
                    <span style={{ fontWeight: '700', color: 'var(--dark)' }}>{m.data[mk] || 0}%</span>
                  </div>
                  <div className="bar-track" style={{ height: '6px' }}>
                    <div className="bar-fill" style={{
                      width: `${m.data[mk] || 0}%`,
                      background: m.color,
                      height: '6px',
                      borderRadius: '3px'
                    }}></div>
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>

        {/* Detailed Comparison Table */}
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--border)' }}>
                <th style={{ textAlign: 'left', padding: '10px 12px', color: 'var(--muted)', fontWeight: '600', fontSize: '11.5px', textTransform: 'uppercase', letterSpacing: '.04em' }}>Model</th>
                {metricKeys.map(mk => (
                  <th key={mk} style={{ textAlign: 'center', padding: '10px 12px', color: 'var(--muted)', fontWeight: '600', fontSize: '11.5px', textTransform: 'uppercase', letterSpacing: '.04em' }}>{metricLabels[mk]}</th>
                ))}
                <th style={{ textAlign: 'center', padding: '10px 12px', color: 'var(--muted)', fontWeight: '600', fontSize: '11.5px', textTransform: 'uppercase', letterSpacing: '.04em' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {models.map((m) => (
                <tr key={m.key} style={{
                  borderBottom: '1px solid var(--border)',
                  background: m.key === bestKey ? 'rgba(99,102,241,0.04)' : 'transparent'
                }}>
                  <td style={{ padding: '12px', fontWeight: '600', color: m.color }}>
                    {m.key === bestKey && '★ '}{m.label}
                  </td>
                  {metricKeys.map(mk => (
                    <td key={mk} style={{ textAlign: 'center', padding: '12px', fontWeight: '600', color: 'var(--dark)' }}>
                      {m.data[mk] || 0}%
                    </td>
                  ))}
                  <td style={{ textAlign: 'center', padding: '12px' }}>
                    <span className={`pill ${m.key === bestKey ? 'high' : 'mid'}`}>
                      {m.key === bestKey ? 'Best' : 'Trained'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {allMetrics.train_size && (
          <div style={{ marginTop: '14px', fontSize: '12px', color: 'var(--muted)', textAlign: 'right' }}>
            Train: {allMetrics.train_size} samples · Test: {allMetrics.test_size} samples · Seed: 42
          </div>
        )}
      </div>

      {/* Feature Importance Section */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px', marginBottom: '20px' }}>
        {models.filter(m => m.data.feature_importance && m.data.feature_importance.length > 0).map((m) => (
          <div key={m.key} className="card">
            <h3 className="card-title" style={{ fontSize: '14px', marginBottom: '14px' }}>
              {m.label} — Top Features
            </h3>
            <div className="skills-card" style={{ marginBottom: 0 }}>
              {m.data.feature_importance.slice(0, 8).map((fi, idx) => {
                const maxImp = m.data.feature_importance[0]?.importance || 1;
                const pct = maxImp > 0 ? (fi.importance / maxImp) * 100 : 0;
                return (
                  <div key={idx} className="skill-row">
                    <div className="sr-top">
                      <span className="sname" style={{ fontSize: '12px' }}>{fi.feature}</span>
                      <span className="sval" style={{ fontSize: '12px' }}>{fi.importance}</span>
                    </div>
                    <div className="bar-track" style={{ height: '5px' }}>
                      <div className="bar-fill" style={{
                        width: `${pct}%`,
                        background: m.color,
                        height: '5px',
                        borderRadius: '2.5px'
                      }}></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
