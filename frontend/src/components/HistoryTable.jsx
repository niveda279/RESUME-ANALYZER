import React from 'react';

export default function HistoryTable({ history, onSelectAnalysis }) {
  if (!history || history.length === 0) {
    return (
      <div className="card">
        <h2 className="card-title">Prediction History</h2>
        <p style={{ marginTop: '12px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          No previous resume analysis recorded yet. Upload a resume above to begin.
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h2 className="card-title">Prediction History</h2>
          <p className="card-subtitle">Previous resumes analyzed by Logistic Regression engine</p>
        </div>
      </div>

      <div className="table-container">
        <table className="custom-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Filename</th>
              <th>Predicted Role</th>
              <th>Confidence</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr key={item.id}>
                <td>#{item.id}</td>
                <td style={{ fontWeight: '500' }}>{item.filename}</td>
                <td>
                  <span className="tag tag-blue">{item.prediction}</span>
                </td>
                <td>{item.confidence ? `${item.confidence}%` : 'N/A'}</td>
                <td style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                  {new Date(item.created_at).toLocaleDateString()}
                </td>
                <td>
                  <button
                    onClick={() => onSelectAnalysis && onSelectAnalysis(item)}
                    className="btn-secondary"
                    style={{ padding: '4px 10px', fontSize: '0.8rem' }}
                  >
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
