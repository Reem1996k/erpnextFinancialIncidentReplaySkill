/**
 * Analysis Section Component
 * Displays replay analysis results in organized sections
 */

import { Info, Calculator, CheckCircle, AlertCircle } from 'lucide-react';

interface AnalysisSectionProps {
  summary?: string;
  details?: string;
  conclusion?: string;
}

export function AnalysisSection({ summary, details, conclusion }: AnalysisSectionProps) {
  if (!summary && !details && !conclusion) {
    return (
      <div className="bg-slate-50 border border-slate-200 rounded-lg p-6 text-center text-slate-600">
        <AlertCircle className="w-8 h-8 mx-auto mb-3 text-slate-400" />
        <p>No analysis available. Run replay to generate insights.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Summary */}
      {summary && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-6">
          <div className="flex gap-3">
            <Info className="w-6 h-6 text-indigo-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-indigo-900 mb-2">Root Cause</h3>
              <p className="text-indigo-800">{summary}</p>
            </div>
          </div>
        </div>
      )}

      {/* Details */}
      {details && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex gap-3">
            <Calculator className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-blue-900 mb-2">Numerical Breakdown</h3>
              <p className="text-blue-800 font-mono text-sm whitespace-pre-wrap">{details}</p>
            </div>
          </div>
        </div>
      )}

      {/* Conclusion */}
      {conclusion && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <div className="flex gap-3">
            <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-green-900 mb-2">Recommended Resolution</h3>
              <p className="text-green-800">{conclusion}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
