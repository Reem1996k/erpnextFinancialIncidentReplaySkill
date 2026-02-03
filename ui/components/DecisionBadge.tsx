/**
 * DecisionBadge component
 * Displays the replay decision with appropriate styling
 */

import { ReplayDecision } from "@/app/lib/types";

interface DecisionBadgeProps {
  decision: ReplayDecision;
}

export function DecisionBadge({ decision }: DecisionBadgeProps) {
  let bgColor = "bg-gray-100";
  let textColor = "text-gray-800";
  let borderColor = "border-gray-300";

  switch (decision) {
    case "APPROVED_WITH_RISK":
      bgColor = "bg-green-100";
      textColor = "text-green-800";
      borderColor = "border-green-300";
      break;
    case "REJECTED":
      bgColor = "bg-red-100";
      textColor = "text-red-800";
      borderColor = "border-red-300";
      break;
    case "PENDING_REVIEW":
      bgColor = "bg-yellow-100";
      textColor = "text-yellow-800";
      borderColor = "border-yellow-300";
      break;
  }

  return (
    <span
      className={`inline-flex items-center px-4 py-2 rounded-full font-semibold border ${bgColor} ${textColor} ${borderColor}`}
    >
      {decision.replace(/_/g, " ")}
    </span>
  );
}
