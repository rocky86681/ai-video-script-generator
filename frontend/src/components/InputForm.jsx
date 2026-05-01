import { useState } from 'react';
import { Clapperboard, Send } from 'lucide-react';

const VIDEO_STYLES = [
  { value: 'YouTube', label: '🎥 YouTube' },
  { value: 'Cinematic', label: '🎬 Cinematic' },
  { value: 'Instagram Reel', label: '📱 Instagram Reel' },
];

const DURATIONS = [
  { value: '30 seconds', label: '⚡ 30 Seconds' },
  { value: '1 minute', label: '⏱️ 1 Minute' },
  { value: '5 minutes', label: '🕐 5 Minutes' },
];

export default function InputForm({ onSubmit, isLoading }) {
  const [topic, setTopic] = useState('');
  const [style, setStyle] = useState('YouTube');
  const [duration, setDuration] = useState('1 minute');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!topic.trim()) return;
    onSubmit({ topic: topic.trim(), style, duration });
  };

  return (
    <section className="glass-card animate-in" id="input-section">
      <h2 className="section-title">
        <Clapperboard />
        Create Your Script
        <span className="title-line" />
      </h2>

      <form className="input-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="topic-input">
            Video Topic
          </label>
          <input
            id="topic-input"
            type="text"
            className="form-input"
            placeholder="e.g., How to Build a PC on a Budget"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            maxLength={200}
            required
            disabled={isLoading}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label" htmlFor="style-select">
              Video Style
            </label>
            <select
              id="style-select"
              className="form-select"
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              disabled={isLoading}
            >
              {VIDEO_STYLES.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="duration-select">
              Duration
            </label>
            <select
              id="duration-select"
              className="form-select"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              disabled={isLoading}
            >
              {DURATIONS.map((d) => (
                <option key={d.value} value={d.value}>
                  {d.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading || !topic.trim()}
          id="generate-btn"
        >
          <Send size={18} />
          {isLoading ? 'Generating...' : 'Generate Script'}
        </button>
      </form>
    </section>
  );
}
