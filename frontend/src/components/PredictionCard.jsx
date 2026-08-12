import React, { useState } from 'react';

export default function PredictionCard({ prediction, allPredictions }) {
  const [activeModel, setActiveModel] = useState('best');

  if (!prediction && !allPredictions) return null;

  // Model tabs configuration
  const hasMultiModel = allPredictions &&
    allPredictions.logistic_regression &&
    allPredictions.random_forest &&
    allPredictions.xgboost;

  const bestModelName = allPredictions?.best_model || 'Logistic Regression';
  const bestModelKey  = allPredictions?.best_model_key || 'logistic_regression';

  const tabs = hasMultiModel ? [
    { key: 'best',                  label: `★ Best (${bestModelName})`, color: '#6366f1' },
    { key: 'logistic_regression',   label: 'Logistic Regression',       color: '#6366f1' },
    { key: 'random_forest',        label: 'Random Forest',              color: '#10b981' },
    { key: 'xgboost',              label: 'XGBoost',                    color: '#f59e0b' },
  ] : [];

  // Determine which prediction to display
  let displayPred;
  if (hasMultiModel) {
    if (activeModel === 'best') {
      displayPred = allPredictions[bestModelKey] || prediction;
    } else {
      displayPred = allPredictions[activeModel] || prediction;
    }
  } else {
    displayPred = prediction;
  }

  const { predicted_role, confidence, breakdown } = displayPred || {};

  // Determine label for the classifier badge
  const modelLabelMap = {
    'best':                  bestModelName,
    'logistic_regression':   'Logistic Regression',
    'random_forest':         'Random Forest',
    'xgboost':               'XGBoost'
  };
  const classifierLabel = hasMultiModel
    ? modelLabelMap[activeModel] || bestModelName
    : 'Logistic Regression';

  return (
    <div className="card" style={{ marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', flexWrap: 'wrap', gap: '8px' }}>
        <h3 className="card-title" style={{ marginBottom: 0 }}>Career Path Prediction</h3>
        <span className="hero-eyebrow" style={{ margin: 0, padding: '4px 10px', fontSize: '11.5px' }}>
          <span className="dot"></span> {classifierLabel} Classifier
        </span>
      </div>

      {/* Model selector tabs */}
      {hasMultiModel && (
        <div style={{
          display: 'flex', gap: '6px', marginBottom: '18px',
          flexWrap: 'wrap', padding: '4px',
          background: 'var(--light)', borderRadius: '10px',
          border: '1px solid var(--border)'
        }}>
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveModel(tab.key)}
              style={{
                padding: '7px 14px',
                borderRadius: '8px',
                border: activeModel === tab.key ? '1px solid var(--primary)' : '1px solid transparent',
                background: activeModel === tab.key
                  ? 'linear-gradient(135deg, rgba(99,102,241,0.1), rgba(99,102,241,0.05))'
                  : 'transparent',
                color: activeModel === tab.key ? 'var(--primary-dark)' : 'var(--muted)',
                fontWeight: activeModel === tab.key ? '700' : '500',
                fontSize: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                fontFamily: 'Inter, sans-serif'
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
      )}

      {/* Prediction Display */}
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
          {predicted_role || 'N/A'}
        </div>
        {confidence != null && (
          <div style={{ fontSize: '13px', color: 'var(--primary-dark)', fontWeight: '600' }}>
            Classifier Confidence: {confidence}%
          </div>
        )}
      </div>

      {/* Multi-model summary (when showing best) */}
      {hasMultiModel && activeModel === 'best' && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
          gap: '10px',
          marginBottom: '18px'
        }}>
          {[
            { key: 'logistic_regression', label: 'Logistic Regression', color: '#6366f1' },
            { key: 'random_forest',       label: 'Random Forest',       color: '#10b981' },
            { key: 'xgboost',             label: 'XGBoost',             color: '#f59e0b' },
          ].map((m) => {
            const p = allPredictions[m.key] || {};
            const isBest = m.key === bestModelKey;
            return (
              <div key={m.key} style={{
                background: isBest ? 'rgba(99,102,241,0.05)' : 'var(--light)',
                border: isBest ? '2px solid var(--primary)' : '1px solid var(--border)',
                borderRadius: '10px',
                padding: '12px',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'transform 0.15s ease'
              }}
                onClick={() => setActiveModel(m.key)}
              >
                <div style={{ fontSize: '10.5px', color: m.color, fontWeight: '700', textTransform: 'uppercase', letterSpacing: '.04em', marginBottom: '4px' }}>
                  {isBest && '★ '}{m.label}
                </div>
                <div style={{ fontSize: '14px', fontWeight: '700', color: 'var(--dark)', marginBottom: '2px' }}>
                  {p.predicted_role || 'N/A'}
                </div>
                <div style={{ fontSize: '11.5px', color: 'var(--muted)' }}>
                  {p.confidence || 0}% confidence
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Role Probability Breakdown */}
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
