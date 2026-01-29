/**
 * Confidence Bar Component
 * Shows analysis confidence as progress bar
 */

interface ConfidenceBarProps {
  score: number; // 0-1 or 0-100
  size?: 'sm' | 'md' | 'lg';
}

export function ConfidenceBar({ score, size = 'md' }: ConfidenceBarProps) {
  // Normalize to 0-100
  const percentage = score > 1 ? score : score * 100;

  // Determine color based on confidence
  let barColor = 'bg-red-500';
  if (percentage >= 80) barColor = 'bg-green-500';
  else if (percentage >= 60) barColor = 'bg-amber-500';

  const sizeClass = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  }[size];

  const textSize = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
  }[size];

  return (
    <div className="w-full">
      <div className={`w-full bg-slate-200 rounded-full overflow-hidden ${sizeClass}`}>
        <div
          className={`${barColor} h-full rounded-full transition-all duration-300`}
          style={{ width: `${Math.min(100, percentage)}%` }}
        />
      </div>
      <p className={`${textSize} text-slate-600 mt-1`}>{percentage.toFixed(0)}% Confidence</p>
    </div>
  );
}
