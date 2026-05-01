import { Sparkles } from 'lucide-react';

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-badge">
        <Sparkles />
        Powered by Generative AI
      </div>
      <h1 className="app-title">AI Video Script Generator</h1>
      <p className="app-subtitle">
        Transform any idea into a production-ready video script — complete with
        scene breakdowns, camera directions, and voiceover narration.
      </p>
    </header>
  );
}
