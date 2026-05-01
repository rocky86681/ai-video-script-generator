import { useState } from 'react';
import Header from './components/Header';
import InputForm from './components/InputForm';
import LoadingState from './components/LoadingState';
import ErrorState from './components/ErrorState';
import ScriptOutput from './components/ScriptOutput';
import Footer from './components/Footer';
import './App.css';

const API_BASE = 'http://127.0.0.1:8000';

function App() {
  const [scriptData, setScriptData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastRequest, setLastRequest] = useState(null);

  const handleGenerate = async (formData) => {
    setIsLoading(true);
    setError(null);
    setScriptData(null);
    setLastRequest(formData);

    try {
      const response = await fetch(`${API_BASE}/generate-script`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errBody = await response.json().catch(() => ({}));
        throw new Error(
          errBody.detail || `Server responded with status ${response.status}`
        );
      }

      const data = await response.json();
      setScriptData(data);
    } catch (err) {
      console.error('Generation failed:', err);
      setError(err.message || 'An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = () => {
    if (lastRequest) {
      handleGenerate(lastRequest);
    }
  };

  return (
    <div className="app-container">
      <Header />

      <main>
        <InputForm onSubmit={handleGenerate} isLoading={isLoading} />

        {isLoading && <LoadingState />}

        {error && !isLoading && (
          <ErrorState
            message={error}
            onRetry={handleRegenerate}
          />
        )}

        {scriptData && !isLoading && !error && (
          <ScriptOutput
            data={scriptData}
            onRegenerate={handleRegenerate}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
