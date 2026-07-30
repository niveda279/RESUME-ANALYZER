import React from 'react';

export default function ResumeCard({ parsedData, filename, score = 88 }) {
  if (!parsedData) return null;

  const { name, email, phone, skills, education, experience, certifications, projects } = parsedData;

  // Calculate SVG ring stroke-dashoffset (circumference = 2 * PI * 72 = 452.389)
  const circumference = 452.4;
  const currentScore = Math.min(100, Math.max(0, score));
  const dashOffset = circumference - (circumference * currentScore) / 100;

  return (
    <div className="grid-top">
      {/* Score Ring Card */}
      <div className="card score-card">
        <h3 className="card-title" style={{ alignSelf: 'flex-start' }}>Overall ATS Score</h3>
        <div className="ring-wrap">
          <svg width="168" height="168" viewBox="0 0 168 168">
            <circle cx="84" cy="84" r="72" fill="none" stroke="#EEF1F5" strokeWidth="14" />
            <circle
              cx="84"
              cy="84"
              r="72"
              fill="none"
              stroke="#6366F1"
              strokeWidth="14"
              strokeLinecap="round"
              strokeDasharray="452.4"
              strokeDashoffset={dashOffset}
              style={{ transition: 'stroke-dashoffset 0.6s ease' }}
            />
          </svg>
          <div className="ring-score">
            <b>{currentScore}</b>
            <span>out of 100</span>
          </div>
        </div>
        <div className="score-badge">
          {currentScore >= 80 ? 'Excellent — Recruiter Ready' : currentScore >= 60 ? 'Good Match — Needs Minor Edits' : 'Needs Optimization'}
        </div>
      </div>

      {/* Summary Card */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <h3 className="card-title" style={{ marginBottom: 0 }}>Resume Summary</h3>
          <span style={{ fontSize: '12.5px', color: 'var(--muted)' }}>File: {filename || 'Uploaded Document'}</span>
        </div>

        <div className="summary-list">
          <div className="summary-item">
            <div className="label">Candidate Name</div>
            <div className="value">{name || 'Candidate Name'}</div>
          </div>
          <div className="summary-item">
            <div className="label">Email / Phone</div>
            <div className="value" style={{ fontSize: '13.5px' }}>{email || 'Not Provided'} | {phone || ''}</div>
          </div>
          <div className="summary-item">
            <div className="label">Experience</div>
            <div className="value">{experience || 'Professional experience detected'}</div>
          </div>
          <div className="summary-item">
            <div className="label">Education</div>
            <div className="value">{education || 'Academic background detected'}</div>
          </div>
        </div>

        <div style={{ marginTop: '20px' }}>
          <div className="label" style={{ fontSize: '11.5px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '.04em', marginBottom: '8px' }}>
            Extracted Skills
          </div>
          <div className="skill-chip-row">
            {skills && skills.length > 0 ? (
              skills.map((skill, idx) => (
                <span key={idx} className="chip">{skill}</span>
              ))
            ) : (
              <span className="chip">General Skills</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
