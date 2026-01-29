/**
 * Status Badge Component
 * Colors incidents by status
 */

export type Status = 'OPEN' | 'UNDER_REVIEW' | 'RESOLVED' | 'ERROR';

const statusConfig: Record<Status, { bg: string; text: string; label: string }> = {
  OPEN: { bg: 'bg-slate-100', text: 'text-slate-800', label: 'Open' },
  UNDER_REVIEW: { bg: 'bg-amber-100', text: 'text-amber-800', label: 'Under Review' },
  RESOLVED: { bg: 'bg-green-100', text: 'text-green-800', label: 'Resolved' },
  ERROR: { bg: 'bg-red-100', text: 'text-red-800', label: 'Error' },
};

interface StatusBadgeProps {
  status: string;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status as Status] || statusConfig.OPEN;

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${config.bg} ${config.text}`}>
      {config.label}
    </span>
  );
}
