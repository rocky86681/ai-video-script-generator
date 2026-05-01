import { useState } from 'react';
import {
  RotateCcw,
  FileText,
  Film,
  Camera,
  Mic,
  Image,
  Type,
  Clock,
  Hash,
  Zap,
  Eye,
  Video,
  Copy,
  CheckCircle2,
} from 'lucide-react';

const TABS = [
  { key: 'script', label: 'Script', icon: FileText },
  { key: 'scenes', label: 'Scenes', icon: Film },
  { key: 'voiceover', label: 'Voiceover', icon: Mic },
  { key: 'shots', label: 'Shot List', icon: Camera },
  { key: 'thumbnails', label: 'Thumbnails', icon: Image },
  { key: 'titles', label: 'Titles', icon: Type },
];

export default function ScriptOutput({ data, onRegenerate }) {
  const [activeTab, setActiveTab] = useState('script');

  return (
    <div className="output-container" id="output-section">
      {/* Header with title + meta */}
      <section className="glass-card">
        <div className="output-header">
          <div style={{ flex: 1 }}>
            <h2 className="script-title-display">{data.title}</h2>
          </div>
          <button
            className="btn btn-secondary"
            onClick={onRegenerate}
            id="regenerate-btn"
            title="Regenerate script"
          >
            <RotateCcw size={16} />
            Regenerate
          </button>
        </div>

        <div className="output-meta" style={{ marginTop: 16 }}>
          <span className="meta-badge accent">
            <Video size={13} />
            {data.target_duration}
          </span>
          <span className="meta-badge">
            <Hash size={13} />
            {data.estimated_word_count} words
          </span>
          <span className="meta-badge">
            <Film size={13} />
            {data.scenes?.length || 0} scenes
          </span>
          <span className="meta-badge">
            <Camera size={13} />
            {data.shot_list?.length || 0} shots
          </span>
        </div>
      </section>

      {/* Hook */}
      <section className="glass-card">
        <div className="content-block hook">
          <div className="content-block-label">
            <Zap size={15} />
            Hook — First 5 Seconds
          </div>
          <div className="content-block-text">{data.hook}</div>
        </div>
      </section>

      {/* Tabs */}
      <div className="tabs-container" id="output-tabs">
        {TABS.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            className={`tab-btn ${activeTab === key ? 'active' : ''}`}
            onClick={() => setActiveTab(key)}
            id={`tab-${key}`}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <section className="glass-card animate-in" key={activeTab}>
        {activeTab === 'script' && <ScriptTab data={data} />}
        {activeTab === 'scenes' && <ScenesTab scenes={data.scenes} />}
        {activeTab === 'voiceover' && <VoiceoverTab voiceover={data.voiceover} />}
        {activeTab === 'shots' && <ShotListTab shots={data.shot_list} />}
        {activeTab === 'thumbnails' && (
          <ThumbnailsTab thumbnails={data.thumbnail_suggestions} />
        )}
        {activeTab === 'titles' && (
          <TitlesTab titles={data.title_alternatives} mainTitle={data.title} />
        )}
      </section>
    </div>
  );
}

/* ─── Tab: Full Script ─── */
function ScriptTab({ data }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(data.script);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div>
      <div className="section-title-wrapper">
        <h3 className="section-title">
          <FileText />
          Full Script
          <span className="title-line" />
        </h3>
        <button className="btn-copy" onClick={handleCopy}>
          {copied ? <CheckCircle2 size={14} color="#34d399" /> : <Copy size={14} />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>
      <div className="content-block">
        <div className="content-block-text">{data.script}</div>
      </div>
    </div>
  );
}

/* ─── Tab: Scenes ─── */
function ScenesTab({ scenes }) {
  if (!scenes || scenes.length === 0) {
    return <EmptyState message="No scene breakdowns available." />;
  }

  return (
    <div>
      <h3 className="section-title">
        <Film />
        Scene-by-Scene Breakdown
        <span className="title-line" />
      </h3>
      <div className="scenes-grid">
        {scenes.map((scene, i) => (
          <div
            className={`scene-card animate-in stagger-${Math.min(i + 1, 5)}`}
            key={scene.scene || i}
          >
            <div className="scene-number">{scene.scene || i + 1}</div>
            <div className="scene-content">
              <p className="scene-description">{scene.description}</p>
              <div className="scene-details">
                {scene.camera && (
                  <span className="scene-tag camera">
                    <Camera size={12} />
                    {scene.camera}
                  </span>
                )}
                {scene.duration && (
                  <span className="scene-tag duration">
                    <Clock size={12} />
                    {scene.duration}
                  </span>
                )}
                {scene.visual_notes && (
                  <span className="scene-tag visual">
                    <Eye size={12} />
                    {scene.visual_notes}
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── Tab: Voiceover ─── */
function VoiceoverTab({ voiceover }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(voiceover);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div>
      <div className="section-title-wrapper">
        <h3 className="section-title">
          <Mic />
          Voiceover Narration
          <span className="title-line" />
        </h3>
        <button className="btn-copy" onClick={handleCopy}>
          {copied ? <CheckCircle2 size={14} color="#34d399" /> : <Copy size={14} />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>
      <div className="content-block">
        <div className="content-block-label">
          <Mic size={15} />
          Full Narration Script
        </div>
        <div className="content-block-text">{voiceover}</div>
      </div>
    </div>
  );
}

/* ─── Tab: Shot List ─── */
function ShotListTab({ shots }) {
  if (!shots || shots.length === 0) {
    return <EmptyState message="No shot list available." />;
  }

  return (
    <div>
      <h3 className="section-title">
        <Camera />
        Shot List for Video Editing
        <span className="title-line" />
      </h3>
      <div style={{ overflowX: 'auto' }}>
        <table className="shot-list-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Shot Type</th>
              <th>Description</th>
              <th>Equipment Notes</th>
            </tr>
          </thead>
          <tbody>
            {shots.map((shot, i) => (
              <tr key={shot.shot_number || i}>
                <td style={{ fontWeight: 600, color: 'var(--text-accent)' }}>
                  {shot.shot_number || i + 1}
                </td>
                <td>
                  <span className="shot-type-badge">{shot.shot_type}</span>
                </td>
                <td>{shot.description}</td>
                <td style={{ color: 'var(--text-muted)', fontSize: '0.83rem' }}>
                  {shot.equipment_notes || '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ─── Tab: Thumbnails ─── */
function ThumbnailsTab({ thumbnails }) {
  if (!thumbnails || thumbnails.length === 0) {
    return <EmptyState message="No thumbnail suggestions available." />;
  }

  return (
    <div>
      <h3 className="section-title">
        <Image />
        Thumbnail Suggestions
        <span className="title-line" />
      </h3>
      <div className="thumbnails-grid">
        {thumbnails.map((thumb, i) => (
          <div className={`thumbnail-card animate-in stagger-${i + 1}`} key={i}>
            <h4>Concept {i + 1}</h4>
            <div className="thumbnail-detail">
              <span className="thumbnail-detail-label">Idea:</span>
              <span className="thumbnail-detail-value">{thumb.concept}</span>
            </div>
            <div className="thumbnail-detail">
              <span className="thumbnail-detail-label">Text:</span>
              <span className="thumbnail-detail-value">{thumb.text_overlay}</span>
            </div>
            <div className="thumbnail-detail">
              <span className="thumbnail-detail-label">Colors:</span>
              <span className="thumbnail-detail-value">{thumb.color_scheme}</span>
            </div>
            <div className="thumbnail-detail">
              <span className="thumbnail-detail-label">Style:</span>
              <span className="thumbnail-detail-value">{thumb.style_notes}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── Tab: Alternative Titles ─── */
function TitlesTab({ titles, mainTitle }) {
  return (
    <div>
      <h3 className="section-title">
        <Type />
        Title Suggestions
        <span className="title-line" />
      </h3>
      <div className="alt-titles-list">
        <div className="alt-title-item" style={{
          borderLeft: '3px solid var(--accent-primary)',
          background: 'linear-gradient(135deg, rgba(124, 58, 237, 0.06), rgba(10, 10, 18, 0.5))'
        }}>
          <span className="alt-title-num">★</span>
          <span className="alt-title-text">{mainTitle}</span>
          <span className="meta-badge accent" style={{ marginLeft: 'auto' }}>
            Primary
          </span>
        </div>
        {titles && titles.map((title, i) => (
          <div className={`alt-title-item animate-in stagger-${i + 1}`} key={i}>
            <span className="alt-title-num">{i + 1}</span>
            <span className="alt-title-text">{title}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── Empty State ─── */
function EmptyState({ message }) {
  return (
    <div style={{
      textAlign: 'center',
      padding: '40px 20px',
      color: 'var(--text-muted)',
      fontSize: '0.9rem'
    }}>
      {message}
    </div>
  );
}
