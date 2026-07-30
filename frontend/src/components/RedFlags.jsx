import React from 'react';

export default function RedFlags({ flags }) {
  if (!flags || flags.length === 0) return null;

  return (
    <div className="card flag-card">
      <h3 className="card-title">
        <span className="flag-dot red"></span> Red Flags
      </h3>

      <div>
        {flags.map((flag, index) => {
          // Remove leading ✖ if present
          const cleanText = flag.replace(/^✖\s*/, '');
          return (
            <div key={index} className="flag-item red">
              <span className="mark">!</span>
              <span>{cleanText}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
