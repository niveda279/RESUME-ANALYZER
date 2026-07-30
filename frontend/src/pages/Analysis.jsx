import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { resumeService } from '../services/api';
import ResumeCard from '../components/ResumeCard';
import PredictionCard from '../components/PredictionCard';
import GreenFlags from '../components/GreenFlags';
import RedFlags from '../components/RedFlags';
import AccuracyCard from '../components/AccuracyCard';

export default function Analysis() {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const data = await resumeService.getAnalysis(id);
        setAnalysis(data);
      } catch (err) {
        setError('Failed to load analysis record.');
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchAnalysis();
  }, [id]);

  if (loading) return <div className="container"><p>Loading analysis...</p></div>;
  if (error) return <div className="container"><div className="alert-error">{error}</div></div>;
  if (!analysis) return null;

  return (
    <div className="container">
      <div style={{ marginBottom: '20px' }}>
        <Link to="/dashboard" className="btn-secondary" style={{ padding: '6px 14px', fontSize: '0.875rem' }}>
          &larr; Back to Dashboard
        </Link>
      </div>

      <ResumeCard parsedData={analysis.parsed_entities} filename={analysis.filename} />
      <PredictionCard prediction={analysis.prediction} />
      <GreenFlags flags={analysis.green_flags} />
      <RedFlags flags={analysis.red_flags} />
      <AccuracyCard metrics={analysis.model_performance} />
    </div>
  );
}
