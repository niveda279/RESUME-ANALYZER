import React, { useState } from 'react';

export default function PredictionCard({ prediction, allPredictions, onRoleClick }) {
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
      <div 
        onClick={() => predicted_role && onRoleClick && onRoleClick(predicted_role)}
        className="prediction-card-main-box"
        style={{
          background: 'var(--light)',
          border: '1px solid var(--border)',
          borderRadius: '10px',
          padding: '20px',
          textAlign: 'center',
          marginBottom: '20px',
          cursor: 'pointer',
          transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
        }}
        title={`Click to analyze skill gap for ${predicted_role}`}
      >
        <div style={{ fontSize: '12px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '.04em', fontWeight: '600' }}>
          Predicted Role Match (Click to analyze skills)
        </div>
        <div className="predicted-role-title-hover" style={{ fontSize: '28px', fontWeight: '700', fontFamily: 'Poppins, sans-serif', color: 'var(--primary-dark)', margin: '6px 0', textDecoration: 'underline' }}>
          {predicted_role || 'N/A'}
        </div>
        {confidence != null && (
          <div style={{ fontSize: '13px', color: 'var(--dark-soft)', fontWeight: '600' }}>
            Classifier Confidence: {confidence}% · <span style={{ color: 'var(--primary)', textDecoration: 'underline' }}>View Skill Gap Analysis ➔</span>
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
              <div key={m.key} 
                className="multi-model-card-hover"
                style={{
                  background: isBest ? 'rgba(99,102,241,0.05)' : 'var(--light)',
                  border: isBest ? '2px solid var(--primary)' : '1px solid var(--border)',
                  borderRadius: '10px',
                  padding: '12px',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onClick={() => {
                  setActiveModel(m.key);
                  if (p.predicted_role && onRoleClick) {
                    onRoleClick(p.predicted_role);
                  }
                }}
                title={`Select ${m.label} prediction and view skill gap`}
              >
                <div style={{ fontSize: '10.5px', color: m.color, fontWeight: '700', textTransform: 'uppercase', letterSpacing: '.04em', marginBottom: '4px' }}>
                  {isBest && '★ '}{m.label}
                </div>
                <div style={{ fontSize: '14px', fontWeight: '700', color: 'var(--primary-dark)', marginBottom: '2px', textDecoration: 'underline' }}>
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
            Role Probability Distribution (Click any role to see its Skill Gap Analysis)
          </div>
          {breakdown.map((item, idx) => (
            <div key={idx} 
              className="skill-row predicted-role-row-clickable"
              onClick={() => onRoleClick && onRoleClick(item.role)}
              style={{
                cursor: 'pointer',
                padding: '8px 12px',
                borderRadius: '8px',
                transition: 'all 0.2s ease',
                margin: '4px -12px'
              }}
              title={`Click to analyze skill gap for ${item.role}`}
            >
              <div className="sr-top" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="sname" style={{ color: 'var(--primary-dark)', fontWeight: '600', textDecoration: 'underline' }}>{item.role}</span>
                <span className="sval" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  {item.probability}% <span className="view-gap-badge" style={{ fontSize: '10px', background: 'var(--primary-tint)', color: 'var(--primary-dark)', padding: '2px 8px', borderRadius: '20px', fontWeight: '700', border: '1px solid rgba(99,102,241,0.2)' }}>Analyze Gap ➔</span>
                </span>
              </div>
              <div className="bar-track" style={{ marginTop: '8px' }}>
                <div className="bar-fill" style={{ width: `${item.probability}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
