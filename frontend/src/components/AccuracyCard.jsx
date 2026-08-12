import React from 'react';
import ModelComparison from './ModelComparison';

export default function AccuracyCard({ metrics, allMetrics, parsedEntities }) {
  const modelData = metrics || {
    algorithm: "Logistic Regression",
    accuracy: 0,
    precision: 0,
    recall: 0,
    f1_score: 0
  };

  // Use actual extracted skills from parsed resume, falling back to empty
  const extractedSkills = parsedEntities?.skills || [];

  // Key tech keywords to check for from the extracted resume skills
  const foundKeywords = extractedSkills.slice(0, 10);
  const hasFoundKeywords = foundKeywords.length > 0;

  // Resume section checklist — derived from parsedEntities where available
  const sectionChecks = [
    { label: "Contact Information", present: !!(parsedEntities?.email && parsedEntities?.email !== "Not Provided") },
    { label: "Education", present: !!(parsedEntities?.education && parsedEntities?.education.length > 10) },
    { label: "Projects", present: !!(parsedEntities?.projects && parsedEntities?.projects !== "Project implementations mentioned in document") },
    { label: "Experience", present: !!(parsedEntities?.experience && parsedEntities?.experience.length > 10) },
    { label: "Skills", present: extractedSkills.length > 0 },
    { label: "Certifications", present: !!(parsedEntities?.certifications && parsedEntities?.certifications !== "None detected") },
  ];

  return (
    <div>
      {/* Skills Analysis Card — derived from actual extracted skills */}
      <div className="card skills-card">
        <h3 className="card-title">Skills Analysis</h3>
        {hasFoundKeywords ? (
          extractedSkills.slice(0, 5).map((skill, idx) => {
            // Generate a pseudo-score based on skill position (top skills ranked higher)
            const scoreBase = 95 - idx * 6;
            return (
              <div key={idx} className="skill-row">
                <div className="sr-top">
                  <span className="sname">{skill}</span>
                  <span className="sval">{scoreBase}%</span>
                </div>
                <div className="bar-track">
                  <div className="bar-fill" style={{ width: `${scoreBase}%` }}></div>
                </div>
              </div>
            );
          })
        ) : (
          <>
            <div className="skill-row">
              <div className="sr-top"><span className="sname">Technical Skills</span><span className="sval">—</span></div>
              <div className="bar-track"><div className="bar-fill" style={{ width: '0%' }}></div></div>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--muted)', marginTop: '8px' }}>
              Upload a resume to see skill analysis.
            </p>
          </>
        )}
      </div>

      {/* Keywords Grid — actual extracted skills from resume */}
      <div className="keywords-grid">
        <div className="card">
          <h3 className="card-title">Detected Skills</h3>
          <div className="kw-list">
            {hasFoundKeywords ? (
              foundKeywords.map((kw, i) => (
                <span key={i} className="kw-chip found">{kw}</span>
              ))
            ) : (
              <span style={{ fontSize: '12px', color: 'var(--muted)' }}>
                No skills detected yet. Upload a resume.
              </span>
            )}
          </div>
        </div>
        <div className="card">
          <h3 className="card-title">Resume Info</h3>
          <div style={{ fontSize: '13px', lineHeight: '1.8' }}>
            {parsedEntities ? (
              <>
                <div><strong>Name:</strong> {parsedEntities.name || '—'}</div>
                <div><strong>Email:</strong> {parsedEntities.email || '—'}</div>
                <div><strong>Phone:</strong> {parsedEntities.phone || '—'}</div>
                <div><strong>Skills Found:</strong> {extractedSkills.length}</div>
              </>
            ) : (
              <span style={{ fontSize: '12px', color: 'var(--muted)' }}>Upload a resume to see details.</span>
            )}
          </div>
        </div>
      </div>

      {/* Resume Sections Checklist */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3 className="card-title">Resume Sections</h3>
        <div className="sections-grid">
          {sectionChecks.map((sec, i) => (
            <div key={i} className="section-item">
              <span className="check" style={{ color: sec.present ? 'var(--success)' : 'var(--danger)' }}>
                {sec.present ? '✓' : '✗'}
              </span>
              <span className="sname" style={{ color: sec.present ? 'var(--dark)' : 'var(--muted)' }}>
                {sec.label}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Model Performance Accuracy Metrics (LR — backward-compat) */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <h3 className="card-title" style={{ marginBottom: 0 }}>Model Performance Metrics</h3>
          <span style={{ fontSize: '12.5px', color: 'var(--muted)' }}>
            Algorithm: <strong>{modelData.algorithm || 'Logistic Regression'}</strong>
          </span>
        </div>

        <div className="skill-row">
          <div className="sr-top"><span className="sname">Accuracy</span><span className="sval">{modelData.accuracy}%</span></div>
          <div className="bar-track"><div className="bar-fill" style={{ width: `${modelData.accuracy}%` }}></div></div>
        </div>
        <div className="skill-row">
          <div className="sr-top"><span className="sname">Precision</span><span className="sval">{modelData.precision}%</span></div>
          <div className="bar-track"><div className="bar-fill" style={{ width: `${modelData.precision}%` }}></div></div>
        </div>
        <div className="skill-row">
          <div className="sr-top"><span className="sname">Recall</span><span className="sval">{modelData.recall}%</span></div>
          <div className="bar-track"><div className="bar-fill" style={{ width: `${modelData.recall}%` }}></div></div>
        </div>
        <div className="skill-row">
          <div className="sr-top"><span className="sname">F1 Score</span><span className="sval">{modelData.f1_score}%</span></div>
          <div className="bar-track"><div className="bar-fill" style={{ width: `${modelData.f1_score}%` }}></div></div>
        </div>
      </div>

      {/* Multi-Model Comparison */}
      <ModelComparison allMetrics={allMetrics} />
    </div>
  );
}
