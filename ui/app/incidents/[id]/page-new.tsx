'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { getIncident, runAnalysis, Incident, AnalysisResponse } from '@/app/lib/api';

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
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center py-12">
          <div className="inline-block">
            <div className="animate-spin text-4xl mb-4">⏳</div>
            <p className="text-slate-600 font-medium">Loading incident details...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !incident) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Link href="/incidents" className="text-blue-600 hover:text-blue-700 font-medium mb-6 inline-block">
          ← Back to Incidents
        </Link>
        <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 font-bold text-lg mb-2">⚠️ Error</p>
          <p className="text-red-700">{error || 'Incident not found'}</p>
          <button
            onClick={fetchIncident}
            className="mt-4 text-red-700 font-medium hover:text-red-900 underline"
          >
            Try again
          </button>
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
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Back Link */}
      <Link href="/incidents" className="text-blue-600 hover:text-blue-700 font-medium mb-6 inline-block">
        ← Back to Incidents
      </Link>

      {/* Page Header */}
      <div className="mb-8">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 mb-2 font-mono">{incident.erp_reference}</h1>
            <p className="text-slate-600">{incident.incident_type}</p>
          </div>
          <div className="text-right">
            <span className={`inline-block px-4 py-2 rounded-full text-sm font-bold border ${getStatusBadgeColor(incident.status)}`}>
              {incident.status}
            </span>
          </div>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 font-medium">⚠️ {error}</p>
        </div>
      )}

      {/* Description Section */}
      <div className="mb-8 p-6 bg-white border border-slate-200 rounded-lg">
        <h2 className="text-lg font-bold text-slate-900 mb-4">Description</h2>
        <p className="text-slate-700 leading-relaxed">{incident.description}</p>
      </div>

      {/* Grid Layout for Analysis Sections */}
      <div className="grid md:grid-cols-2 gap-8 mb-8">
        {/* Confidence & Summary Card */}
        <div className="p-6 bg-white border border-slate-200 rounded-lg">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Analysis Summary</h2>
          
          {incident.confidence_score ? (
            <>
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-slate-600">Confidence Score</span>
                  <span className={`text-2xl font-bold ${getConfidenceColor(incident.confidence_score)}`}>
                    {(incident.confidence_score * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${
                      incident.confidence_score >= 0.8
                        ? 'bg-green-500'
                        : incident.confidence_score >= 0.6
                        ? 'bg-amber-500'
                        : 'bg-red-500'
                    }`}
                    style={{ width: `${incident.confidence_score * 100}%` }}
                  />
                </div>
              </div>

              {incident.replay_summary && (
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-sm font-medium text-blue-900">{incident.replay_summary}</p>
                </div>
              )}
            </>
          ) : (
            <div className="p-6 bg-slate-50 border-2 border-dashed border-slate-300 rounded-lg text-center">
              <p className="text-slate-600 font-medium mb-4">No analysis yet</p>
              <button
                onClick={handleAnalyze}
                disabled={analyzing}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg font-bold hover:bg-blue-700 disabled:opacity-50 transition"
              >
                {analyzing ? '⏳ Analyzing...' : '🔍 Run Analysis'}
              </button>
            </div>
          )}
        </div>

        {/* Run Analysis Button */}
        {incident.confidence_score && (
          <div className="p-6 bg-white border border-slate-200 rounded-lg flex flex-col justify-center">
            <h2 className="text-lg font-bold text-slate-900 mb-6">Actions</h2>
            <button
              onClick={handleAnalyze}
              disabled={analyzing}
              className="w-full px-6 py-4 bg-blue-600 text-white rounded-lg font-bold hover:bg-blue-700 disabled:opacity-50 transition text-lg"
            >
              {analyzing ? '⏳ Re-analyzing...' : '🔄 Re-run Analysis'}
            </button>
            <p className="text-xs text-slate-500 mt-4">
              Last analyzed: {incident.replayed_at ? new Date(incident.replayed_at).toLocaleString() : '—'}
            </p>
          </div>
        )}
      </div>

      {/* Analysis Sections */}
      {incident.confidence_score && (
        <div className="space-y-8 mb-8">
          {/* Root Cause Section */}
          {incident.replay_details && (
            <div className="p-6 bg-white border border-slate-200 rounded-lg">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl">🔍</span>
                <h2 className="text-lg font-bold text-slate-900">Root Cause Analysis</h2>
              </div>
              <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
                <p className="text-indigo-900 leading-relaxed whitespace-pre-wrap">{incident.replay_details}</p>
              </div>
            </div>
          )}

          {/* Recommendation Section */}
          {incident.replay_conclusion && (
            <div className="p-6 bg-white border border-slate-200 rounded-lg">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl">✅</span>
                <h2 className="text-lg font-bold text-slate-900">Recommended Action</h2>
              </div>
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-900 font-medium leading-relaxed whitespace-pre-wrap">{incident.replay_conclusion}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Metadata Section */}
      <div className="p-6 bg-slate-50 border border-slate-200 rounded-lg">
        <h2 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-4">Metadata</h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <p className="text-xs text-slate-600 uppercase font-semibold">Created</p>
            <p className="text-slate-900 font-medium">{new Date(incident.created_at).toLocaleString()}</p>
          </div>
          <div>
            <p className="text-xs text-slate-600 uppercase font-semibold">Analysis Source</p>
            <p className="text-slate-900 font-medium">{incident.analysis_source || '—'}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
