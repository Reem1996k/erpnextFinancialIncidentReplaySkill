/**
 * AnalysisSummary component
 * Displays replay analysis results
 */

import { ReplayResponse } from "@/app/lib/types";
import { DecisionBadge } from "./DecisionBadge";

interface AnalysisSummaryProps {
  analysis: ReplayResponse;
}

export function AnalysisSummary({ analysis }: AnalysisSummaryProps) {
  return (
    <div className="space-y-6">
      {/* Executive Summary */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded">
        <h3 className="text-lg font-semibold text-blue-900 mb-2">Executive Summary</h3>
        <p className="text-blue-800 text-base">{analysis.replay_summary}</p>
      </div>

      {/* Findings */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Findings</h3>
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <p className="text-gray-700 whitespace-pre-wrap font-mono text-sm leading-relaxed">
            {analysis.replay_details}
          </p>
        </div>
      </div>

      {/* Decision */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Decision</h3>
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <DecisionBadge decision={analysis.replay_decision} />
        </div>
      </div>

      {/* Conclusion */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Conclusion</h3>
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <p className="text-gray-700 leading-relaxed">{analysis.replay_conclusion}</p>
        </div>
      </div>

      {/* Analysis Metadata */}
      {(analysis.analysis_source || analysis.confidence_score !== undefined) && (
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 text-sm">
          <div className="flex gap-6">
            {analysis.analysis_source && (
              <div>
                <span className="text-gray-600">Analysis Source:</span>
                <span className="ml-2 font-semibold text-gray-900">{analysis.analysis_source}</span>
              </div>
            )}
            {analysis.confidence_score !== undefined && (
              <div>
                <span className="text-gray-600">Confidence:</span>
                <span className="ml-2 font-semibold text-gray-900">
                  {(analysis.confidence_score * 100).toFixed(0)}%
                </span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
