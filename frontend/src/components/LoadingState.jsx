import { useEffect, useState } from 'react';
import { Check, Loader } from 'lucide-react';

const LOADING_STEPS = [
  'Analyzing your topic...',
  'Crafting the perfect hook...',
  'Writing scene breakdowns...',
  'Generating voiceover narration...',
  'Finalizing script & suggestions...',
];

export default function LoadingState() {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => {
        if (prev < LOADING_STEPS.length - 1) return prev + 1;
        return prev;
      });
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="glass-card" id="loading-section">
      <div className="loading-overlay">
        <div className="loading-spinner" />
        <p className="loading-text">
          ✨ AI is crafting your video script...
        </p>
        <div className="loading-steps">
          {LOADING_STEPS.map((step, i) => (
            <div
              key={i}
              className={`loading-step ${
                i < activeStep ? 'complete' : i === activeStep ? 'active' : ''
              }`}
            >
              {i < activeStep ? (
                <Check size={16} />
              ) : i === activeStep ? (
                <Loader size={16} className="loading-step-spinner" />
              ) : (
                <span style={{ width: 16, display: 'inline-block' }} />
              )}
              {step}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
