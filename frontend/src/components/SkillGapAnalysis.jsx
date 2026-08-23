import React, { useState, useEffect } from 'react';

export default function SkillGapAnalysis({ roleName, data, loading, error, onClose }) {
  const [completedTasks, setCompletedTasks] = useState({});

  // Reset completed tasks when target role changes
  useEffect(() => {
    setCompletedTasks({});
  }, [roleName]);

  if (loading) {
    return (
      <div className="card" id="skill-gap-analysis-card" style={{ padding: '40px 20px', textAlign: 'center' }}>
        <div className="spinner" style={{
          width: '40px',
          height: '40px',
          border: '4px solid rgba(99, 102, 241, 0.1)',
          borderTop: '4px solid var(--primary)',
          borderRadius: '50%',
          margin: '0 auto 16px',
          animation: 'spin 1s linear infinite'
        }}></div>
        <p style={{ color: 'var(--muted)', fontSize: '14.5px' }}>Performing skill gap analysis for <b>{roleName}</b>...</p>
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card" id="skill-gap-analysis-card" style={{ border: '1px solid var(--red-border)', background: 'var(--red-bg)', color: 'var(--red-text)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h4>Skill Gap Analysis Error</h4>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: 'var(--red-text)', cursor: 'pointer', fontSize: '18px', fontWeight: 'bold' }}>&times;</button>
        </div>
        <p style={{ marginTop: '8px', fontSize: '13.5px' }}>{error}</p>
      </div>
    );
  }

  if (!data) return null;

  const { gap_analysis } = data;
  const { match_percentage, matched_skills = [], missing_skills = [], priority_gaps = [] } = gap_analysis || {};

  const handleToggleTask = (skill) => {
    setCompletedTasks(prev => ({
      ...prev,
      [skill]: !prev[skill]
    }));
  };

  // UI helpers for matches progress circle
  const size = 120;
  const strokeWidth = 10;
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (match_percentage / 100) * circumference;

  // Determine color based on alignment score
  let gaugeColor = 'var(--red-text)';
  let gaugeBg = 'var(--red-bg)';
  let message = 'Significant Skill Gap';
  let desc = 'You are missing critical credentials. Focus on the core dependencies checklist below.';

  if (match_percentage >= 70) {
    gaugeColor = 'var(--green-text)';
    gaugeBg = 'var(--green-bg)';
    message = 'Strong Skill Alignment!';
    desc = 'You have a high competency overlap for this role. Fill in the minor gaps below to stand out.';
  } else if (match_percentage >= 40) {
    gaugeColor = '#d97706'; // dark amber
    gaugeBg = 'rgba(254, 243, 199, 0.85)';
    message = 'Moderate Skill Alignment';
    desc = 'You share several common requirements, but require solid training in missing core techniques.';
  }

  return (
    <div className="card" id="skill-gap-analysis-card" style={{
      animation: 'slideDown 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
      border: '1.5px solid var(--primary)',
      boxShadow: '0 20px 25px -5px rgba(99,102,241,0.1), 0 10px 10px -5px rgba(99,102,241,0.04)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
        <div>
          <span className="hero-eyebrow" style={{ margin: '0 0 8px 0', padding: '4px 10px', fontSize: '11px', background: 'rgba(99,102,241,0.15)', color: 'var(--primary-dark)' }}>
            ROLE-BASED COMPETENCY COMPARE
          </span>
          <h2 style={{ fontSize: '20px', color: 'var(--dark)', marginTop: '4px' }}>
            Skill Gap Analysis: <span className="accent" style={{ background: 'linear-gradient(135deg, #6366F1 0%, #4F46E5 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>{roleName}</span>
          </h2>
        </div>
        <button 
          onClick={onClose} 
          style={{
            cursor: 'pointer',
            background: 'var(--primary-tint)',
            border: 'none',
            color: 'var(--primary-dark)',
            width: '28px',
            height: '28px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '16px',
            fontWeight: 'bold',
            transition: 'all 0.2s ease',
            padding: 0
          }}
          onMouseEnter={(e) => { e.target.style.background = 'var(--primary)'; e.target.style.color = '#fff'; }}
          onMouseLeave={(e) => { e.target.style.background = 'var(--primary-tint)'; e.target.style.color = 'var(--primary-dark)'; }}
          title="Close analysis"
        >
          &times;
        </button>
      </div>

      {/* Grid: Visual Score + Description */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '140px 1fr',
        gap: '24px',
        background: gaugeBg,
        borderRadius: '12px',
        padding: '20px',
        alignItems: 'center',
        marginBottom: '26px',
        border: `1px solid ${match_percentage >= 70 ? 'var(--green-border)' : match_percentage >= 40 ? 'rgba(252, 211, 77, 0.9)' : 'var(--red-border)'}`
      }}>
        {/* SVG Circular Chart */}
        <div style={{ position: 'relative', width: size, height: size, margin: '0 auto' }}>
          <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
            <circle
              stroke="rgba(0,0,0,0.04)"
              fill="transparent"
              strokeWidth={strokeWidth}
              r={radius}
              cx={size / 2}
              cy={size / 2}
            />
            <circle
              stroke={gaugeColor}
              fill="transparent"
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              r={radius}
              cx={size / 2}
              cy={size / 2}
              style={{ transition: 'stroke-dashoffset 0.8s ease-in-out' }}
            />
          </svg>
          <div style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            transform: 'none'
          }}>
            <span style={{ fontSize: '22px', fontWeight: '800', color: 'var(--dark)' }}>
              {match_percentage}%
            </span>
            <span style={{ fontSize: '10px', color: 'var(--muted)', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '.02em' }}>
              Match
            </span>
          </div>
        </div>

        {/* Diagnostic description */}
        <div>
          <h4 style={{ color: 'var(--dark)', fontWeight: '700', fontSize: '16px', marginBottom: '6px' }}>{message}</h4>
          <p style={{ color: 'var(--dark-soft)', fontSize: '13.5px', lineHeight: 1.5 }}>
            {desc}
          </p>
        </div>
      </div>

      {/* Double columns: Available vs Missing */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '20px',
        marginBottom: '26px'
      }}>
        {/* Available Skills list */}
        <div style={{
          background: 'var(--light)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          padding: '16px 20px'
        }}>
          <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13.5px', color: 'var(--green-text)', textTransform: 'uppercase', letterSpacing: '.03em', marginBottom: '12px', fontWeight: '700' }}>
            <span style={{ display: 'inline-flex', width: '18px', height: '18px', borderRadius: '50%', background: 'var(--green-bg)', alignItems: 'center', justifyContent: 'center', fontSize: '10px' }}>✓</span>
            Available Skills ({matched_skills.length})
          </h4>
          {matched_skills.length === 0 ? (
            <p style={{ color: 'var(--muted)', fontSize: '12.5px', fontStyle: 'italic' }}>No matching skills found in resume.</p>
          ) : (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {matched_skills.map((item, idx) => (
                <span key={idx} style={{
                  background: 'var(--green-bg)',
                  border: '1px solid var(--green-border)',
                  color: 'var(--green-text)',
                  fontSize: '11.5px',
                  fontWeight: '600',
                  padding: '4px 10px',
                  borderRadius: '6px'
                }}>
                  {item.skill} <span style={{ fontSize: '9px', opacity: 0.75 }}>({item.priority})</span>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Missing Skills list */}
        <div style={{
          background: 'var(--light)',
          border: '1px solid var(--border)',
          borderRadius: '12px',
          padding: '16px 20px'
        }}>
          <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13.5px', color: '#b45309', textTransform: 'uppercase', letterSpacing: '.03em', marginBottom: '12px', fontWeight: '700' }}>
            <span style={{ display: 'inline-flex', width: '18px', height: '18px', borderRadius: '50%', background: 'rgba(254, 243, 199, 1)', alignItems: 'center', justifyContent: 'center', fontSize: '10px' }}>!</span>
            Missing Required Skills ({missing_skills.length})
          </h4>
          {missing_skills.length === 0 ? (
            <p style={{ color: 'var(--green-text)', fontSize: '12.5px', fontStyle: 'italic', fontWeight: '500' }}>Excellent! You have met all competency prerequisites.</p>
          ) : (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {missing_skills.map((item, idx) => {
                const isCritical = item.priority === 'Critical' || item.priority === 'High';
                return (
                  <span key={idx} style={{
                    background: isCritical ? 'var(--red-bg)' : 'var(--primary-tint)',
                    border: isCritical ? '1px solid var(--red-border)' : '1px solid rgba(99,102,241,0.2)',
                    color: isCritical ? 'var(--red-text)' : 'var(--primary-dark)',
                    fontSize: '11.5px',
                    fontWeight: '600',
                    padding: '4px 10px',
                    borderRadius: '6px'
                  }}>
                    {item.skill} <span style={{ fontSize: '9px', opacity: 0.8 }}>({item.priority})</span>
                  </span>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Actionable recommendations checklist */}
      <div>
        <h3 style={{ fontSize: '15px', color: 'var(--dark)', fontWeight: '700', marginBottom: '14px', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>
          Actionable Recommendations — Bridge Your Skill Gap
        </h3>

        {priority_gaps.length === 0 ? (
          <div style={{
            background: 'var(--green-bg)',
            border: '1px solid var(--green-border)',
            borderRadius: '10px',
            padding: '12px 16px',
            color: 'var(--green-text)',
            fontSize: '13px'
          }}>
            <b>All set!</b> You have no critical skill gaps to bridge. You are fully ready for this role.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {priority_gaps.map((gap, idx) => {
              const isChecked = !!completedTasks[gap.skill];
              return (
                <div key={idx} style={{
                  display: 'flex',
                  gap: '14px',
                  alignItems: 'flex-start',
                  background: isChecked ? 'rgba(255,255,255,0.4)' : '#fff',
                  border: isChecked ? '1px dashed var(--border)' : '1px solid var(--border)',
                  borderRadius: '10px',
                  padding: '14px 16px',
                  transition: 'all 0.2s ease',
                  opacity: isChecked ? 0.75 : 1
                }}>
                  {/* Custom checkbox */}
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() => handleToggleTask(gap.skill)}
                    id={`skill-task-${gap.skill}`}
                    style={{
                      width: '20px',
                      height: '20px',
                      borderRadius: '5px',
                      cursor: 'pointer',
                      marginTop: '3px',
                      accentColor: 'var(--primary)'
                    }}
                  />
                  
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                      <label 
                        htmlFor={`skill-task-${gap.skill}`}
                        style={{
                          fontWeight: '700',
                          fontSize: '13.5px',
                          color: isChecked ? 'var(--muted)' : 'var(--dark)',
                          textDecoration: isChecked ? 'line-through' : 'none',
                          cursor: 'pointer'
                        }}
                      >
                        Learn {gap.skill}
                      </label>
                      <span style={{
                        background: gap.priority === 'Critical' ? 'var(--red-bg)' : 'rgba(254, 243, 199, 1)',
                        color: gap.priority === 'Critical' ? 'var(--red-text)' : '#d97706',
                        fontSize: '9.5px',
                        fontWeight: '800',
                        padding: '2px 8px',
                        borderRadius: '12px',
                        textTransform: 'uppercase',
                        letterSpacing: '.02em'
                      }}>
                        {gap.priority} Gap
                      </span>
                      {isChecked && (
                        <span style={{ color: 'var(--green-text)', fontSize: '11px', fontWeight: '700', display: 'inline-flex', alignItems: 'center', gap: '3px' }}>
                          ✓ Handled
                        </span>
                      )}
                    </div>
                    <p style={{
                      marginTop: '6px',
                      fontSize: '12.5px',
                      color: isChecked ? 'var(--muted)' : 'var(--dark-soft)',
                      lineHeight: 1.4,
                      textDecoration: isChecked ? 'line-through' : 'none'
                    }}>
                      {gap.suggestion}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <style>{`
        @keyframes slideDown {
          0% { opacity: 0; transform: translateY(-16px); }
          100% { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}
