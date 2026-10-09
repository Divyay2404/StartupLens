import React from 'react';
import { Search, Sparkles, Globe, ArrowRight, Lightbulb } from 'lucide-react';

export default function IdeaForm({
  idea,
  setIdea,
  targetRegion,
  setTargetRegion,
  includePatents,
  setIncludePatents,
  sampleIdeas,
  onSelectSample,
  onSubmit,
  isLoading
}) {
  return (
    <div className="glass-panel" style={{ padding: '36px', marginBottom: '36px', position: 'relative', overflow: 'hidden' }}>
      {/* Decorative background glow */}
      <div style={{
        position: 'absolute',
        top: '-120px',
        right: '-100px',
        width: '320px',
        height: '320px',
        background: 'radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%)',
        pointerEvents: 'none'
      }} />

      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '4px 12px',
          borderRadius: '20px',
          background: 'rgba(99, 102, 241, 0.1)',
          border: '1px solid rgba(99, 102, 241, 0.25)',
          color: '#a5b4fc',
          fontSize: '0.8rem',
          fontWeight: '600',
          marginBottom: '12px'
        }}>
          <Sparkles size={14} color="#818cf8" />
          Evidence-Backed Opportunity Assessment Engine
        </div>
        <h1 style={{ fontSize: '2.4rem', fontWeight: '800', lineHeight: '1.2', marginBottom: '12px' }}>
          What is missing, and what <span className="text-gradient">new opportunity</span> can you build?
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem', maxWidth: '780px' }}>
          Enter any startup or product concept. StartupLens orchestrates <strong>SerpApi</strong> across
          Google Search, Google News, Google Scholar, Google Trends, and Google Patents to map competitor gaps and uncover your differentiation vector.
        </p>
      </div>

      {/* Main Input Form */}
      <form onSubmit={onSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div>
          <label style={{
            display: 'block',
            fontSize: '0.88rem',
            fontWeight: '600',
            color: 'var(--text-main)',
            marginBottom: '8px'
          }}>
            Describe Your Startup Idea / Project Concept:
          </label>
          <div style={{ position: 'relative' }}>
            <textarea
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="e.g. AI attendance system for rural schools with low connectivity and intermittent power..."
              rows={3}
              style={{
                width: '100%',
                background: 'var(--bg-input)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--text-main)',
                padding: '16px 20px',
                fontSize: '1.02rem',
                fontFamily: 'var(--font-body)',
                lineHeight: '1.5',
                resize: 'vertical',
                outline: 'none',
                transition: 'border-color var(--transition-normal), box-shadow var(--transition-normal)'
              }}
              onFocus={(e) => e.target.style.borderColor = 'var(--accent-primary)'}
              onBlur={(e) => e.target.style.borderColor = 'var(--border-subtle)'}
            />
          </div>
        </div>

        {/* Options Row & CTA */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '16px',
          borderTop: '1px solid rgba(255, 255, 255, 0.05)',
          paddingTop: '18px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px', flexWrap: 'wrap' }}>
            {/* Region Selector */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Globe size={16} color="var(--text-secondary)" />
              <label style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Region:</label>
              <select
                value={targetRegion}
                onChange={(e) => setTargetRegion(e.target.value)}
                style={{
                  background: 'var(--bg-elevated)',
                  color: 'var(--text-main)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '6px 12px',
                  fontSize: '0.85rem',
                  outline: 'none',
                  cursor: 'pointer'
                }}
              >
                <option value="Global">Global Market</option>
                <option value="Emerging Markets / Rural">Emerging Markets / Rural</option>
                <option value="North America">North America</option>
                <option value="India">India / South Asia</option>
                <option value="Europe">Europe</option>
              </select>
            </div>

            {/* Include Patents Checkbox */}
            <label style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '0.85rem',
              color: 'var(--text-secondary)',
              cursor: 'pointer'
            }}>
              <input
                type="checkbox"
                checked={includePatents}
                onChange={(e) => setIncludePatents(e.target.checked)}
                style={{ accentColor: 'var(--accent-primary)', width: '16px', height: '16px', cursor: 'pointer' }}
              />
              <span>Include Google Patents Landscape</span>
            </label>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading || !idea.trim()}
            className="btn-primary"
            style={{ minWidth: '240px' }}
          >
            {isLoading ? (
              <>
                <div className="pulse-circle" style={{ background: '#ffffff', boxShadow: '0 0 8px #ffffff' }}></div>
                <span>Executing SerpApi Engines...</span>
              </>
            ) : (
              <>
                <Search size={18} />
                <span>Validate & Discover Gaps</span>
                <ArrowRight size={16} />
              </>
            )}
          </button>
        </div>
      </form>

      {/* Quick-Start Demo Ideas */}
      <div style={{ marginTop: '28px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
          <Lightbulb size={16} color="var(--accent-amber)" />
          <span style={{ fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            Instant 1-Click Hackathon Scenarios:
          </span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '12px' }}>
          {sampleIdeas.map((sample) => (
            <div
              key={sample.id}
              onClick={() => onSelectSample(sample)}
              style={{
                background: sample.id === 'rural_attendance' ? 'rgba(99, 102, 241, 0.08)' : 'rgba(255, 255, 255, 0.03)',
                border: sample.id === 'rural_attendance' ? '1px solid rgba(99, 102, 241, 0.35)' : '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '12px 16px',
                cursor: 'pointer',
                transition: 'all var(--transition-fast)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.borderColor = 'var(--accent-primary)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.borderColor = sample.id === 'rural_attendance' ? 'rgba(99, 102, 241, 0.35)' : 'var(--border-subtle)';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span style={{ fontSize: '0.72rem', color: 'var(--accent-cyan)', fontWeight: '600' }}>
                  {sample.tag}
                </span>
                {sample.highlight && (
                  <span style={{
                    fontSize: '0.65rem',
                    background: 'rgba(245, 158, 11, 0.15)',
                    color: '#fbbf24',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    fontWeight: '600'
                  }}>
                    {sample.highlight}
                  </span>
                )}
              </div>
              <div style={{ fontSize: '0.92rem', fontWeight: '600', color: '#ffffff', marginBottom: '4px' }}>
                {sample.title}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                {sample.description.slice(0, 85)}...
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
