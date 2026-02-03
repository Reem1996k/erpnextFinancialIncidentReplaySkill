'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getIncidents, Incident } from '@/app/lib/api';

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getIncidents();
      setIncidents(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load incidents');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
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
    if (!score) return 'bg-slate-200';
    if (score >= 0.8) return 'bg-green-500';
    if (score >= 0.6) return 'bg-amber-500';
    return 'bg-red-500';
  };

  return (
    <div className="page-wrapper">
      <div className="page-container">
        {/* Page Header */}
        <div className="page-header">
          <h1 className="page-title">Incidents</h1>
        </div>

        {/* Action Bar */}
        <div className="action-bar">
          <div className="incident-count">
            Showing <span className="font-bold">{incidents.length}</span> incidents
          </div>
          <button
            onClick={fetchIncidents}
            disabled={loading}
            className="action-button"
          >
            Refresh
          </button>
        </div>

        {/* Error State */}
        {error && (
          <div className="error-box">
            <p className="error-title">Error loading incidents</p>
            <p className="error-message">{error}</p>
            <button
              onClick={fetchIncidents}
              className="error-retry"
            >
              Try again
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="loading-state">
            <p className="loading-text">Loading incidents...</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && incidents.length === 0 && !error && (
          <div className="empty-state">
            <p className="empty-text">No incidents found</p>
            <p className="empty-subtext">Create your first incident to get started</p>
          </div>
        )}

        {/* Incidents Table */}
        {!loading && incidents.length > 0 && (
          <div className="table-card">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="table-head">
                  <tr>
                    <th className="table-header">ERP Reference</th>
                    <th className="table-header">Type</th>
                    <th className="table-header">Status</th>
                    <th className="table-header">Confidence</th>
                    <th className="table-header">Created</th>
                    <th className="table-header text-center">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {incidents.map((incident) => (
                    <tr key={incident.id} className="table-row">
                      <td className="table-cell font-mono font-bold">{incident.erp_reference}</td>
                      <td className="table-cell">{incident.incident_type}</td>
                      <td className="table-cell">
                        <span className={`status-badge ${getStatusColor(incident.status)}`}>
                          {incident.status}
                        </span>
                      </td>
                      <td className="table-cell">
                        <div className="confidence-display">
                          <div className="confidence-bar-bg">
                            <div
                              className={`confidence-bar ${getConfidenceColor(incident.confidence_score)}`}
                              style={{ width: `${((incident.confidence_score || 0) * 100)}%` }}
                            />
                          </div>
                          <span className="confidence-text">
                            {incident.confidence_score ? `${(incident.confidence_score * 100).toFixed(0)}%` : '—'}
                          </span>
                        </div>
                      </td>
                      <td className="table-cell text-sm">
                        {new Date(incident.created_at).toLocaleDateString()}
                      </td>
                      <td className="table-cell text-center">
                        <Link
                          href={`/incidents/${incident.id}`}
                          className="action-link"
                        >
                          View →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        .page-wrapper {
          background-color: #f1f5f9;
          min-height: 100vh;
          padding: 40px 20px;
        }

        .page-container {
          max-width: 900px;
          margin: 40px auto;
        }

        .page-header {
          margin-bottom: 32px;
        }

        .page-title {
          font-size: 32px;
          font-weight: 700;
          color: #111827;
          margin: 0;
        }

        .action-bar {
          margin-bottom: 24px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .incident-count {
          font-size: 14px;
          color: #64748b;
        }

        .action-button {
          padding: 10px 20px;
          background-color: #2563eb;
          color: white;
          border: none;
          border-radius: 8px;
          font-weight: 500;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .action-button:hover:not(:disabled) {
          background-color: #1d4ed8;
        }

        .action-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .error-box {
          margin-bottom: 24px;
          padding: 20px;
          background-color: #fee2e2;
          border: 1px solid #fca5a5;
          border-radius: 8px;
        }

        .error-title {
          font-weight: 600;
          color: #991b1b;
          margin: 0 0 8px 0;
        }

        .error-message {
          font-size: 14px;
          color: #7f1d1d;
          margin: 0 0 12px 0;
        }

        .error-retry {
          font-size: 14px;
          color: #991b1b;
          background: none;
          border: none;
          cursor: pointer;
          font-weight: 500;
          transition: color 0.2s;
        }

        .error-retry:hover {
          color: #7f1d1d;
        }

        .loading-state {
          text-align: center;
          padding: 60px 20px;
        }

        .loading-text {
          color: #64748b;
          font-weight: 500;
        }

        .empty-state {
          text-align: center;
          padding: 60px 20px;
          background: white;
          border-radius: 12px;
          border: 2px dashed #cbd5e1;
        }

        .empty-text {
          font-size: 18px;
          font-weight: 600;
          color: #64748b;
          margin: 0 0 8px 0;
        }

        .empty-subtext {
          font-size: 14px;
          color: #94a3b8;
          margin: 0;
        }

        .table-card {
          background: white;
          border-radius: 12px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
          overflow: hidden;
        }

        .table-head {
          background-color: #f8fafc;
          border-bottom: 1px solid #e2e8f0;
        }

        .table-header {
          padding: 16px;
          text-align: left;
          font-size: 12px;
          font-weight: 600;
          color: #334155;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .table-row {
          border-bottom: 1px solid #e2e8f0;
          transition: background-color 0.2s;
        }

        .table-row:hover {
          background-color: #f8fafc;
        }

        .table-cell {
          padding: 16px;
          color: #334155;
          font-size: 14px;
        }

        .status-badge {
          display: inline-block;
          padding: 6px 12px;
          border-radius: 6px;
          font-size: 12px;
          font-weight: 600;
          border: 1px solid;
        }

        .confidence-display {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .confidence-bar-bg {
          flex: 1;
          height: 8px;
          background-color: #e2e8f0;
          border-radius: 4px;
          overflow: hidden;
          min-width: 64px;
        }

        .confidence-bar {
          height: 100%;
          border-radius: 4px;
          transition: width 0.3s;
        }

        .confidence-text {
          font-size: 12px;
          font-weight: 600;
          color: #64748b;
          min-width: 40px;
          text-align: right;
        }

        .action-link {
          color: #2563eb;
          text-decoration: none;
          font-weight: 500;
          transition: all 0.2s;
        }

        .action-link:hover {
          color: #1d4ed8;
          text-decoration: underline;
        }
      `}</style>
    </div>
  );
}
