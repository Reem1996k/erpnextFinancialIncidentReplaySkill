'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Incident } from '@/app/types';

export default function IncidentsList() {
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
      const response = await fetch('http://localhost:8000/incidents');
      if (!response.ok) {
        throw new Error('Failed to fetch incidents');
      }
      const data = await response.json();
      setIncidents(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
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

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading incidents...</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Financial Incidents</h1>
      {error && <div className="message message-error">Error: {error}</div>}
      {incidents.length === 0 ? (
        <div className="message message-info">
          No incidents found.{' '}
          <Link href="/">Create one now</Link>
        </div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>ERP Reference</th>
              <th>Incident Type</th>
              <th>Status</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {incidents.map((incident) => (
              <tr key={incident.id}>
                <td>#{incident.id}</td>
                <td>{incident.erp_reference}</td>
                <td>{incident.incident_type}</td>
                <td>
                  <span className={getStatusBadgeClass(incident.status)}>
                    {incident.status}
                  </span>
                </td>
                <td>{new Date(incident.created_at).toLocaleString()}</td>
                <td>
                  <Link href={`/incidents/${incident.id}`}>
                    <button className="btn-primary btn-small">View</button>
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
