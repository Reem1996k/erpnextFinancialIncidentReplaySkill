/**
 * IncidentDetailsCard component
 * Displays incident information in a structured format
 */

import { Incident } from "@/app/lib/types";

interface IncidentDetailsCardProps {
  incident: Incident;
}

export function IncidentDetailsCard({ incident }: IncidentDetailsCardProps) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Incident Information</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* ERP Reference */}
        <div>
          <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
            ERP Reference
          </label>
          <p className="text-lg text-gray-900 mt-2">{incident.erp_reference}</p>
        </div>

        {/* Incident Type */}
        <div>
          <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
            Incident Type
          </label>
          <p className="text-lg text-gray-900 mt-2">{incident.incident_type.replace(/_/g, " ")}</p>
        </div>

        {/* Status */}
        <div>
          <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
            Status
          </label>
          <p className="text-lg text-gray-900 mt-2">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
              {incident.status}
            </span>
          </p>
        </div>

        {/* Created At */}
        <div>
          <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
            Created At
          </label>
          <p className="text-lg text-gray-900 mt-2">{formatDate(incident.created_at)}</p>
        </div>
      </div>

      {/* Description - Full Width */}
      <div className="mt-8 pt-8 border-t border-gray-200">
        <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
          Description
        </label>
        <p className="text-base text-gray-700 mt-3 leading-relaxed whitespace-pre-wrap">
          {incident.description}
        </p>
      </div>
    </div>
  );
}
