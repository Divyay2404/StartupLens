import React from 'react';
import { Telescope, Key, FileText, Zap } from 'lucide-react';

export default function Navbar({ isLiveSerpApi, onOpenSettings, onOpenPitch }) {
  return (
    <header style={{
      borderBottom: '1px solid var(--border-subtle)',
      background: 'rgba(7, 9, 14, 0.85)',
      backdropFilter: 'blur(16px)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '16px 24px'
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        {/* Brand Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '12px',
            background: 'var(--gradient-brand)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(99, 102, 241, 0.5)'
          }}>
            <Telescope size={24} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{
                fontFamily: 'var(--font-heading)',
                fontSize: '1.45rem',
                fontWeight: '800',
                letterSpacing: '-0.02em',
                color: '#ffffff'
              }}>
                Startup<span className="text-gradient-cyan">Lens</span>
              </span>
              <span style={{
                fontSize: '0.68rem',
                fontFamily: 'var(--font-mono)',
                padding: '2px 7px',
                background: 'rgba(99, 102, 241, 0.2)',
                color: '#a5b4fc',
                borderRadius: '6px',
                border: '1px solid rgba(99, 102, 241, 0.4)'
              }}>
                Track 5
              </span>
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              SerpApi Multi-Engine Opportunity Intelligence
            </p>
          </div>
        </div>

        {/* Status Pill & Action Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {isLiveSerpApi ? (
            <div className="badge badge-live" title="Connected to SerpApi Live Search Engine">
              <span className="pulse-circle"></span>
              Live SerpApi Connected
            </div>
          ) : (
            <div className="badge badge-demo" title="Operating with built-in realistic intelligence datasets. Add SerpApi key in Settings.">
              <Zap size={13} />
              Demo / High-Fidelity Mode
            </div>
          )}

          <button
            onClick={onOpenSettings}
            className="btn-secondary"
            title="Configure SerpApi and LLM API Keys"
          >
            <Key size={15} />
            <span>API Keys</span>
          </button>

          <button
            onClick={onOpenPitch}
            className="btn-secondary"
            title="View Hackathon Track 5 pitch & architecture"
          >
            <FileText size={15} />
            <span>Judge Pitch</span>
          </button>
        </div>
      </div>
    </header>
  );
}
