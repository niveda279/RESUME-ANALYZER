import React, { useState } from 'react';
import { resumeService } from '../services/api';

export default function UploadResume({ onAnalysisComplete }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    validateAndSetFile(selected);
  };

  const validateAndSetFile = (selected) => {
    setError('');
    if (!selected) return;

    const allowed = ['pdf', 'docx', 'doc'];
    const ext = selected.name.split('.').pop().toLowerCase();

    if (!allowed.includes(ext)) {
      setError('Invalid file format. Please upload a PDF or DOCX file.');
      setFile(null);
      return;
    }

    if (selected.size > 10 * 1024 * 1024) {
      setError('File size exceeds maximum allowable limit of 10MB.');
      setFile(null);
      return;
    }

    setFile(selected);
  };

  const handleUpload = async (e) => {
    if (e) e.preventDefault();
    if (!file) return;

    setError('');
    setUploading(true);
    setProgress(0);

    try {
      const data = await resumeService.uploadResume(file, (percent) => {
        setProgress(percent);
      });
      if (onAnalysisComplete) {
        onAnalysisComplete(data);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Upload and processing failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-card">
      <div className="uc-head">
        <h3>Upload your resume</h3>
        <span>PDF or DOCX · Max 10MB</span>
      </div>

      {error && <div className="alert-error">{error}</div>}

      <div className="dropzone" onClick={() => document.getElementById('file-input').click()}>
        <input
          id="file-input"
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <div className="icon-box">PDF</div>
        <h4>Drag &amp; drop your file here</h4>
        <p>or click below to browse from your device</p>
        <button type="button" className="btn btn-primary btn-sm" style={{ marginTop: '18px' }}>
          Browse File
        </button>
        <div className="filetype">
          {file ? (
            <strong style={{ color: 'var(--primary-dark)' }}>
              Selected: {file.name} ({(file.size / 1024).toFixed(1)} KB)
            </strong>
          ) : (
            'Accepted format: .pdf, .docx'
          )}
        </div>
      </div>

      {uploading && (
        <div className="upload-progress">
          <div className="up-row">
            <span className="fname">{file?.name || 'Resume.pdf'}</span>
            <span className="fpct">{progress}%</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
          </div>
          <div className="up-sub">Uploading &amp; extracting text…</div>
        </div>
      )}

      <div style={{ marginTop: '18px' }}>
        <button
          type="button"
          onClick={handleUpload}
          className="btn btn-primary btn-block"
          disabled={!file || uploading}
        >
          {uploading ? 'Processing...' : 'Analyze Resume Now'}
        </button>
      </div>
    </div>
  );
}
