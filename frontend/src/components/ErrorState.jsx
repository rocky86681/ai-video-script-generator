import { AlertCircle, RotateCcw } from 'lucide-react';

export default function ErrorState({ message, onRetry }) {
  return (
    <section className="glass-card" id="error-section">
      <div className="error-container">
        <AlertCircle className="error-icon" />
        <h3 className="error-title">Generation Failed</h3>
        <p className="error-message">{message}</p>
        {onRetry && (
          <button className="btn btn-primary" onClick={onRetry} id="retry-btn">
            <RotateCcw size={16} />
            Try Again
          </button>
        )}
      </div>
    </section>
  );
}
