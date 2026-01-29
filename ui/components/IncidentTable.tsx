/**
 * IncidentTable component
 * Displays incidents in a table format with view actions
 */

import Link from "next/link";
import { Incident } from "@/lib/types";

interface IncidentTableProps {
  incidents: Incident[];
}

export function IncidentTable({ incidents }: IncidentTableProps) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "NEW":
        return "bg-blue-100 text-blue-800";
      case "ANALYZED":
        return "bg-purple-100 text-purple-800";
      case "APPROVED":
        return "bg-green-100 text-green-800";
      case "REJECTED":
        return "bg-red-100 text-red-800";
      case "PENDING_REVIEW":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  if (incidents.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 text-lg">No incidents found</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-300 bg-gray-50">
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">ID</th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
              ERP Reference
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
              Incident Type
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Status</th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Created At</th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Action</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map((incident) => (
            <tr
              key={incident.id}
              className="border-b border-gray-200 hover:bg-gray-50 transition-colors"
            >
              <td className="px-6 py-4 text-sm text-gray-900 font-medium">#{incident.id}</td>
              <td className="px-6 py-4 text-sm text-gray-700">{incident.erp_reference}</td>
              <td className="px-6 py-4 text-sm text-gray-700">
                {incident.incident_type.replace(/_/g, " ")}
              </td>
              <td className="px-6 py-4 text-sm">
                <span
                  className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
                    incident.status
                  )}`}
                >
                  {incident.status}
                </span>
              </td>
              <td className="px-6 py-4 text-sm text-gray-700">{formatDate(incident.created_at)}</td>
              <td className="px-6 py-4 text-sm">
                <Link
                  href={`/incidents/${incident.id}`}
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  View
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
