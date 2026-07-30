import React from 'react';

export default function AccuracyCard({ metrics }) {
  const modelData = metrics || {
    algorithm: "Logistic Regression",
    accuracy: 92.84,
    precision: 91.00,
    recall: 90.00,
    f1_score: 90.50
  };

  const foundKeywords = ["React.js", "REST APIs", "Node.js", "Agile", "MongoDB", "Git", "Python", "SQL"];
  const missingKeywords = ["Docker", "CI/CD", "System Design", "Kubernetes", "Unit Testing"];

  const sections = [
    "Contact Information",
    "Education",
    "Projects",
    "Experience",
    "Skills",
    "Certifications"
  ];

  return (
    <div>
      {/* Skills Analysis Card */}
      <div className="card skills-card">
        <h3 className="card-title">Skills Analysis</h3>
        <div className="skill-row">
          <div className="sr-top"><span className="sname">Technical Skills</span><span className="sval">92%</span></div>
          <div className="bar-track"><div className="bar-fill" style={{ width: '92%' }}></div></div>
        </div>
        <div className="skill-row">
          <div className="sr-top"><span className="sname">Soft Skills</span><span className="sval">74%</span></div>
          <div className="bar-track"><div className="bar-fill" style={{ width: '74%' }}></div></div>
        </div>
        <div className="skill-row">
          <div className="sr-top"><span className="sname">Domain Skills</span><span className="sval">81%</span></div>
          <div className="bar-track"><div className="bar-fill" style={{ width: '81%' }}></div></div>
        </div>
        <div className="skill-row">
          <div className="sr-top"><span className="sname">Communication</span><span className="sval">68%</span></div>
          <div className="bar-track"><div className="bar-fill" style={{ width: '68%' }}></div></div>
        </div>
      </div>

      {/* Keywords Grid */}
      <div className="keywords-grid">
        <div className="card">
          <h3 className="card-title">Found Keywords</h3>
          <div className="kw-list">
            {foundKeywords.map((kw, i) => (
              <span key={i} className="kw-chip found">{kw}</span>
            ))}
          </div>
        </div>
        <div className="card">
          <h3 className="card-title">Missing Keywords</h3>
          <div className="kw-list">
            {missingKeywords.map((kw, i) => (
              <span key={i} className="kw-chip missing">{kw}</span>
            ))}
          </div>
        </div>
      </div>

      {/* Resume Sections Checklist */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3 className="card-title">Resume Sections</h3>
        <div className="sections-grid">
          {sections.map((sec, i) => (
            <div key={i} className="section-item">
              <span className="check">✓</span>
              <span className="sname">{sec}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Model Performance Accuracy Metrics */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <h3 className="card-title" style={{ marginBottom: 0 }}>Model Performance Metrics</h3>
          <span style={{ fontSize: '12.5px', color: 'var(--muted)' }}>Algorithm: <strong>{modelData.algorithm || 'Logistic Regression'}</strong></span>
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
    </div>
  );
}
