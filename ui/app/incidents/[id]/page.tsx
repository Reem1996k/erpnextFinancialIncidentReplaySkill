'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { getIncident, runAnalysis, Incident } from '@/lib/api';

export default function IncidentDetailPage() {
  const params = useParams();
  const incidentId = params.id as string;
  const [incident, setIncident] = useState<Incident | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchIncident();
  }, [incidentId]);

  const fetchIncident = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getIncident(parseInt(incidentId));
      setIncident(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load incident');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    try {
      setAnalyzing(true);
      setError(null);
      await runAnalysis(parseInt(incidentId));
      await fetchIncident();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to run analysis');
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <div className="page-wrapper">
        <div className="page-container">
          <div className="loading-state">
            <p className="loading-text">Loading incident details...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !incident) {
    return (
      <div className="page-wrapper">
        <div className="page-container">
          <Link href="/incidents" className="back-link">
            ← Back to Incidents
          </Link>
          <div className="error-box">
            <p className="error-title">Error</p>
            <p className="error-message">{error || 'Incident not found'}</p>
            <button
              onClick={fetchIncident}
              className="error-retry"
            >
              Try again
            </button>
          </div>
        </div>
      </div>
    );
  }

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'RESOLVED':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'UNDER_REVIEW':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      case 'ERROR':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-slate-100 text-slate-800 border-slate-300';
    }
  };

  const getConfidenceColor = (score?: number) => {
    if (!score) return 'text-slate-500';
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-amber-600';
    return 'text-red-600';
  };

  return (
    <div className="page-wrapper">
      <div className="page-container">
        {/* SECTION 1: INCIDENT SUMMARY (TOP) */}
        <div className="summary-section">
          <div className="summary-card">
            {/* LEFT COLUMN */}
            <div className="summary-left">
              <div className="summary-item">
                <p className="summary-label">Incident ID</p>
                <p className="summary-id">{incident.id}</p>
              </div>
              <div className="summary-item">
                <p className="summary-label">ERP Reference</p>
                <p className="summary-value">{incident.erp_reference}</p>
              </div>
              <div className="summary-item">
                <p className="summary-label">Incident Type</p>
                <p className="summary-value">{incident.incident_type}</p>
              </div>
            </div>

            {/* RIGHT COLUMN */}
            <div className="summary-right">
              <div className="summary-item">
                <p className="summary-label">Status</p>
                <span className={`status-badge ${getStatusBadgeColor(incident.status)}`}>
                  {incident.status}
                </span>
              </div>
              <div className="summary-item">
                <p className="summary-label">Confidence Score</p>
                {incident.confidence_score ? (
                  <p className="confidence-value">{(incident.confidence_score * 100).toFixed(0)}%</p>
                ) : (
                  <p className="confidence-value">—</p>
                )}
              </div>
              <div className="summary-item">
                <p className="summary-label">Analysis Source</p>
                <p className="summary-value">{incident.analysis_source || 'N/A'}</p>
              </div>
            </div>

            {/* ACTION BUTTON */}
            <div className="summary-actions">
              <button
                onClick={handleAnalyze}
                disabled={analyzing}
                className="analyze-button"
              >
                {analyzing ? 'Analyzing...' : 'Run Analysis'}
              </button>
            </div>
          </div>
        </div>

        {/* SECTION 2: ANALYSIS DETAILS (BOTTOM) */}
        <div className="analysis-section">
          {/* LEFT CARD: ANALYSIS SUMMARY */}
          <div className="analysis-card">
            <div className="card-content">
              {incident.replay_summary && (
                <div className="content-block">
                  <h3 className="card-title">Analysis Summary</h3>
                  <p className="card-text">{incident.replay_summary}</p>
                </div>
              )}

              {incident.replay_conclusion && (
                <div className="content-block conclusion-block">
                  <h3 className="card-title">Conclusion</h3>
                  <p className="card-text conclusion-text">{incident.replay_conclusion}</p>
                </div>
              )}
            </div>
          </div>

          {/* RIGHT CARD: DETAILED ANALYSIS */}
          <div className="analysis-card">
            <div className="card-content">
              {incident.replay_details && (
                <div className="content-block">
                  <h3 className="card-title">Detailed Analysis</h3>
                  <p className="card-text details-text">{incident.replay_details}</p>
                </div>
              )}

              {incident.description && (
                <div className="content-block">
                  <h3 className="card-title">Original Description</h3>
                  <p className="card-text">{incident.description}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .page-wrapper {
          background-color: #f1f5f9;
          min-height: 100vh;
          padding: 40px 20px;
        }

        .page-container {
          max-width: 1000px;
          margin: 40px auto;
        }

        /* ========== SECTION 1: SUMMARY ========== */
        .summary-section {
          margin-bottom: 32px;
        }

        .summary-card {
          background: white;
          border-radius: 12px;
          padding: 20px 24px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
          display: flex;
          gap: 40px;
        }

        .summary-left {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .summary-right {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .summary-item {
          display: flex;
          flex-direction: column;
        }

        .summary-label {
          font-size: 12px;
          font-weight: 600;
          color: #64748b;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          margin: 0 0 4px 0;
        }

        .summary-id {
          font-size: 24px;
          font-weight: 700;
          color: #111827;
          font-family: 'Monaco', 'Menlo', monospace;
          margin: 0;
        }

        .summary-value {
          font-size: 16px;
          font-weight: 600;
          color: #334155;
          margin: 0;
        }

        .status-badge {
          display: inline-block;
          padding: 8px 16px;
          border-radius: 8px;
          font-size: 13px;
          font-weight: 600;
          border: 1px solid;
          width: fit-content;
        }

        .confidence-value {
          font-size: 20px;
          font-weight: 700;
          color: #2563eb;
          margin: 0;
        }

        .summary-actions {
          display: flex;
          justify-content: flex-end;
          padding-top: 12px;
          border-top: 1px solid #e2e8f0;
          margin-top: 12px;
        }

        .analyze-button {
          padding: 10px 20px;
          background-color: #4f46e5;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .analyze-button:hover:not(:disabled) {
          background-color: #4338ca;
        }

        .analyze-button:disabled {
          background-color: #9ca3af;
          cursor: not-allowed;
          opacity: 0.6;
        }

        /* ========== SECTION 2: ANALYSIS DETAILS ========== */
        .analysis-section {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 24px;
          margin-bottom: 32px;
        }

        .analysis-card {
          background: white;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
          display: flex;
          flex-direction: column;
        }

        .card-content {
          display: flex;
          flex-direction: column;
          gap: 24px;
        }

        .content-block {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .card-title {
          font-size: 13px;
          font-weight: 700;
          color: #334155;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          margin: 0;
        }

        .card-text {
          font-size: 14px;
          color: #334155;
          line-height: 1.6;
          margin: 0;
          white-space: pre-wrap;
        }

        .conclusion-block {
          padding-top: 12px;
          border-top: 2px solid #e2e8f0;
        }

        .conclusion-text {
          font-weight: 500;
          color: #111827;
        }

        .details-text {
          font-family: 'Monaco', 'Menlo', monospace;
          font-size: 13px;
        }

        /* ========== ACTION SECTION ========== */


        /* Responsive */
        @media (max-width: 768px) {
          .summary-card {
            flex-direction: column;
            gap: 24px;
          }

          .analysis-section {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
}
