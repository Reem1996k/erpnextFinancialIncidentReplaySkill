/**
 * Incident Card Component
 * Used in dashboard list
 */

import { FileText, AlertTriangle, RotateCcw } from 'lucide-react';
import { Incident } from '@/app/lib/api';
import { StatusBadge } from './StatusBadge';
import { ConfidenceBar } from './ConfidenceBar';
import Link from 'next/link';

interface IncidentCardProps {
  incident: Incident;
}

export function IncidentCard({ incident }: IncidentCardProps) {
  return (
    <Link href={`/incidents/${incident.id}`}>
      <div className="bg-white border border-slate-200 rounded-lg p-6 hover:shadow-lg hover:border-slate-300 transition-all cursor-pointer">
        <div className="grid grid-cols-12 gap-4 items-start">
          {/* ERP Reference & Type */}
          <div className="col-span-3">
            <div className="flex items-center gap-2 mb-2">
              <FileText className="w-5 h-5 text-slate-500" />
              <span className="font-mono text-sm font-bold text-slate-900">{incident.erp_reference}</span>
            </div>
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-slate-400" />
              <span className="text-sm text-slate-600">{incident.incident_type}</span>
            </div>
          </div>

          {/* Status */}
          <div className="col-span-2">
            <StatusBadge status={incident.status} />
          </div>

          {/* Analysis Source */}
          <div className="col-span-2">
            <p className="text-xs text-slate-500 uppercase font-semibold">Source</p>
            <p className="text-sm font-medium text-slate-900">
              {incident.analysis_source === 'AI_WITH_ERP_SNAPSHOT' ? 'AI' : incident.analysis_source || '—'}
            </p>
          </div>

          {/* Confidence */}
          <div className="col-span-3">
            {incident.confidence_score !== undefined && incident.confidence_score !== null ? (
              <ConfidenceBar score={incident.confidence_score} size="sm" />
            ) : (
              <p className="text-sm text-slate-500">—</p>
            )}
          </div>

          {/* Created Date */}
          <div className="col-span-2 text-right">
            <p className="text-xs text-slate-500">
              {new Date(incident.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>
    </Link>
  );
}
