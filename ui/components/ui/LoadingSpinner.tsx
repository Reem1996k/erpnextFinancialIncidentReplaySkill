/**
 * LoadingSpinner component
 * Shows a loading indicator while data is being fetched
 */

export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );
}

/**
 * ErrorMessage component
 * Displays error information to the user
 */
interface ErrorMessageProps {
  error: Error | string;
  onRetry?: () => void;
}

export function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  const message = error instanceof Error ? error.message : error;

  return (
    <div className="rounded-lg bg-red-50 border border-red-200 p-6">
      <h3 className="text-lg font-semibold text-red-900 mb-2">Error</h3>
      <p className="text-red-700 mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
}
