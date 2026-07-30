import React from 'react';

export default function GreenFlags({ flags }) {
  if (!flags || flags.length === 0) return null;

  return (
    <div className="card flag-card">
      <h3 className="card-title">
        <span className="flag-dot green"></span> Green Flags
      </h3>

      <div>
        {flags.map((flag, index) => {
          // Remove leading checkmark if present
          const cleanText = flag.replace(/^✔\s*/, '');
          return (
            <div key={index} className="flag-item green">
              <span className="mark">✓</span>
              <span>{cleanText}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
