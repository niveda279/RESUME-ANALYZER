import React, { useState, useEffect } from 'react';
import UploadResume from './UploadResume';
import ResumeCard from '../components/ResumeCard';
import PredictionCard from '../components/PredictionCard';
import GreenFlags from '../components/GreenFlags';
import RedFlags from '../components/RedFlags';
import AccuracyCard from '../components/AccuracyCard';
import HistoryTable from '../components/HistoryTable';
import Footer from '../components/Footer';
import { resumeService } from '../services/api';

export default function Dashboard({ user }) {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [allMetrics, setAllMetrics] = useState(null);

  const fetchHistory = async () => {
    try {
      const data = await resumeService.getHistory();
      setHistory(data.resumes || []);
      if (!currentAnalysis && data.resumes && data.resumes.length > 0) {
        const latest = data.resumes[0];
        setCurrentAnalysis({
          filename: latest.filename,
          parsed_entities: latest.parsed_entities,
          prediction: {
            predicted_role: latest.prediction,
            confidence: latest.confidence
          },
          green_flags: latest.green_flags,
          red_flags: latest.red_flags
        });
      }
    } catch (err) {
      console.error('Failed to load resume history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  const fetchMLMetrics = async () => {
    try {
      const data = await resumeService.getMLComparison();
      setAllMetrics(data);
    } catch (err) {
      console.error('Failed to load ML metrics:', err);
    }
  };

  useEffect(() => {
    fetchHistory();
    fetchMLMetrics();
  }, []);

  const handleAnalysisComplete = (data) => {
    setCurrentAnalysis(data);
    // Update allMetrics if the API returned them
    if (data.all_metrics) {
      setAllMetrics(data.all_metrics);
    }
    fetchHistory();
    // Smooth scroll down to analysis section
    const elem = document.getElementById('analysis-report-section');
    if (elem) {
      elem.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSelectHistoryItem = (item) => {
    setCurrentAnalysis({
      filename: item.filename,
      parsed_entities: item.parsed_entities,
      prediction: {
        predicted_role: item.prediction,
        confidence: item.confidence
      },
      green_flags: item.green_flags,
      red_flags: item.red_flags
    });
    const elem = document.getElementById('analysis-report-section');
    if (elem) {
      elem.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Determine the best model name for display
  const bestModelName = allMetrics?.best_model || 'Logistic Regression';

  return (
    <div>
      <div className="container">
        {/* FRAME 01 — HERO & UPLOAD */}
        <div className="hero">
          <div>
            <div className="hero-eyebrow">
              <span className="dot"></span> AI-Powered Resume Intelligence
            </div>
            <h1>
              Analyze Your Resume <br /> with <span className="accent">AI</span>
            </h1>
            <p className="lead">
              Upload your resume and receive an ATS score, strengths, weaknesses, keyword analysis, and recruiter-ready insights — in seconds.
            </p>
          </div>

          <div>
            <UploadResume onAnalysisComplete={handleAnalysisComplete} />
          </div>
        </div>

        {/* FRAME 02 — ANALYSIS REPORT */}
        {currentAnalysis && (
          <div id="analysis-report-section" style={{ paddingTop: '32px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '28px', flexWrap: 'wrap', gap: '8px' }}>
              <div>
                <h2 style={{ fontSize: '24px', color: 'var(--dark)' }}>Analysis Report</h2>
                <p style={{ fontSize: '13.5px', color: 'var(--muted)', marginTop: '4px' }}>
                  {currentAnalysis.filename} · Best Model: {bestModelName}
                </p>
              </div>
            </div>

            {/* Score Ring + Summary */}
            <ResumeCard
              parsedData={currentAnalysis.parsed_entities}
              filename={currentAnalysis.filename}
              score={currentAnalysis.prediction?.confidence || 88}
            />

            {/* Career Path Prediction — now with multi-model support */}
            <PredictionCard
              prediction={currentAnalysis.prediction}
              allPredictions={currentAnalysis.all_predictions || null}
            />

            {/* Flags Grid */}
            <div className="flags-grid">
              <GreenFlags flags={currentAnalysis.green_flags} />
              <RedFlags flags={currentAnalysis.red_flags} />
            </div>

            {/* Skills & Keywords & Section Analysis + Model Comparison */}
            <AccuracyCard
              metrics={currentAnalysis.model_performance}
              allMetrics={allMetrics}
              parsedEntities={currentAnalysis.parsed_entities}
            />
          </div>
        )}

        {/* Prediction History Table */}
        <div style={{ marginTop: '40px' }}>
          <HistoryTable history={history} onSelectAnalysis={handleSelectHistoryItem} />
        </div>
      </div>

      {/* FRAME 05 — FOOTER */}
      <Footer />
    </div>
  );
}
