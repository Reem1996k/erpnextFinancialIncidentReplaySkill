'use client';

import { useState, useEffect, use } from 'react';
import Link from 'next/link';
import { Incident } from '@/app/types';

interface IncidentDetailProps {
  params: Promise<{
    id: string;
  }>;
}

export default function IncidentDetail({ params }: IncidentDetailProps) {
  const { id } = use(params);
  const [incident, setIncident] = useState<Incident | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [replayLoading, setReplayLoading] = useState(false);
  const [replayError, setReplayError] = useState<string | null>(null);

  useEffect(() => {
    fetchIncident();
  }, [id]);

  const fetchIncident = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(
        `http://localhost:8000/incidents/${id}`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch incident');
      }
      const data = await response.json();
      setIncident(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleRunReplay = async () => {
    try {
      setReplayLoading(true);
      setReplayError(null);
      const response = await fetch(
        `http://localhost:8000/incidents/${id}/replay`,
        {
          method: 'POST',
        }
      );
      if (!response.ok) {
        throw new Error('Failed to run replay');
      }
      const data = await response.json();
      setIncident(data);
    } catch (err) {
      setReplayError(
        err instanceof Error ? err.message : 'An error occurred'
      );
    } finally {
      setReplayLoading(false);
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'OPEN':
        return 'badge badge-open';
      case 'ANALYZED':
        return 'badge badge-analyzed';
      case 'ERROR':
        return 'badge badge-error';
      default:
        return 'badge';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'OPEN':
        return (
          <svg className="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        );
      case 'ANALYZED':
        return (
          <svg className="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        );
      case 'ERROR':
        return (
          <svg className="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        );
      default:
        return null;
    }
  };

  const getSectionIcon = (type: string) => {
    const iconProps = { className: 'section-icon' };
    switch (type) {
      case 'summary':
        return (
          <svg {...iconProps} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 12h18M3 6h18M3 18h18"></path>
          </svg>
        );
      case 'details':
        return (
          <svg {...iconProps} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"></path>
          </svg>
        );
      case 'decision':
        return (
          <svg {...iconProps} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
          </svg>
        );
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading incident...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <Link href="/">
          <button className="btn-secondary mb-2">Back to Incidents</button>
        </Link>
        <div className="message message-error">Error: {error}</div>
      </div>
    );
  }

  if (!incident) {
    return (
      <div>
        <Link href="/">
          <button className="btn-secondary mb-2">Back to Incidents</button>
        </Link>
        <div className="message message-info">Incident not found</div>
      </div>
    );
  }

  return (
    <div>
      <Link href="/">
        <button className="btn-secondary mb-2">Back to Incidents</button>
      </Link>

      <h1>{incident.erp_reference}</h1>

      {/* Incident Information Card */}
      <div className="incident-info-card">
        <h2>Incident Information</h2>

        <div className="info-grid">
          <div className="info-item">
            <label className="info-label">ID</label>
            <div className="info-value">#{incident.id}</div>
          </div>

          <div className="info-item">
            <label className="info-label">ERP Reference</label>
            <div className="info-value info-highlight">{incident.erp_reference}</div>
          </div>

          <div className="info-item">
            <label className="info-label">Incident Type</label>
            <div className="info-value">{incident.incident_type}</div>
          </div>

          <div className="info-item">
            <label className="info-label">Status</label>
            <div className="info-value">
              <span className={`${getStatusBadgeClass(incident.status)} badge-with-icon`}>
                {getStatusIcon(incident.status)}
                <span>{incident.status}</span>
              </span>
            </div>
          </div>

          <div className="info-item info-full-width">
            <label className="info-label">Created At</label>
            <div className="info-value">
              {new Date(incident.created_at).toLocaleString()}
            </div>
          </div>

          <div className="info-item info-full-width">
            <label className="info-label">Description</label>
            <div className="info-value info-description">{incident.description}</div>
          </div>
        </div>
      </div>

      {/* Replay Analysis Section */}
      {incident.status === 'ANALYZED' && incident.replay_summary ? (
        <div className="replay-results">
          <h2>Replay Analysis Results</h2>

          {/* Summary Section */}
          <section className="replay-section replay-summary">
            <h3>{getSectionIcon('summary')} Summary</h3>
            <p className="summary-text">{incident.replay_summary}</p>
          </section>

          {/* Details Section */}
          <section className="replay-section replay-details">
            <h3>{getSectionIcon('details')} Details</h3>
            <div className="details-content">
              <p>{incident.replay_details}</p>
            </div>
          </section>

          {/* Decision Section */}
          <section className="replay-section replay-conclusion">
            <h3>{getSectionIcon('decision')} Decision</h3>
            <div className="conclusion-content">
              <p>{incident.replay_conclusion}</p>
            </div>
          </section>

          {/* Metadata */}
          {incident.replayed_at && (
            <section className="replay-metadata">
              <p>
                <span className="metadata-label">Analysis Date:</span>
                <span className="metadata-value">
                  {new Date(incident.replayed_at).toLocaleString()}
                </span>
              </p>
            </section>
          )}
        </div>
      ) : (
        <div className="card">
          <div className="message message-info">
            <strong>Replay Analysis Not Yet Performed</strong>
            <p className="mt-1">
              This incident has not been analyzed yet. Click the button below to
              run the replay analysis and generate the financial impact
              assessment.
            </p>
          </div>

          {replayError && (
            <div className="message message-error mt-2">
              Error: {replayError}
            </div>
          )}

          <button
            onClick={handleRunReplay}
            className="btn-primary mt-2"
            disabled={replayLoading}
          >
            {replayLoading ? 'Running Analysis...' : 'Run Replay Analysis'}
          </button>
        </div>
      )}
    </div>
  );
}
