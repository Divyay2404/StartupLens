import React from 'react';
import { X, Award } from 'lucide-react';

export default function PitchModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div className="glass-panel" style={{
        maxWidth: '680px',
        maxHeight: '90vh',
        overflowY: 'auto',
        width: '100%',
        padding: '36px',
        background: '#0d121f',
        position: 'relative'
      }}>
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'none',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer'
          }}
        >
          <X size={22} />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '12px',
            background: 'var(--gradient-brand)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Award size={22} color="#ffffff" />
          </div>
          <div>
            <h3 style={{ fontSize: '1.4rem', fontWeight: '800', color: '#ffffff' }}>
              StartupLens — SerpApi Hackathon 2026
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--accent-cyan)' }}>
              Track 5: Evidence-Backed Opportunity Assessment
            </p>
          </div>
        </div>

        {/* Recommended Judge Pitch Quote Box */}
        <div style={{
          padding: '20px',
          background: 'rgba(99, 102, 241, 0.1)',
          border: '1px solid rgba(99, 102, 241, 0.3)',
          borderRadius: 'var(--radius-md)',
          marginBottom: '24px'
        }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '700', color: '#a5b4fc', textTransform: 'uppercase', marginBottom: '6px' }}>
            Official Pitch Statement
          </div>
          <p style={{ fontSize: '0.96rem', color: '#ffffff', lineHeight: '1.6', fontStyle: 'italic', marginBottom: '14px' }}>
            “StartupLens is an evidence intelligence platform that transforms a startup idea into a structured opportunity
            assessment. It triangulates the idea across existing products, academic research, current news and market-interest
            signals using SerpApi, then uses AI to identify competitor gaps and recommend how the idea could be differentiated.”
          </p>
          <div style={{
            padding: '10px 14px',
            background: 'rgba(0, 0, 0, 0.3)',
            borderRadius: 'var(--radius-sm)',
            borderLeft: '3px solid var(--accent-amber)',
            fontSize: '0.86rem',
            color: '#fef08a'
          }}>
            <strong>Closing line:</strong> “We don't just ask whether an idea already exists. We investigate what exists,
            what's changing, what people are researching and where the gaps are—then turn those signals into a potential opportunity.”
          </div>
        </div>

        {/* SerpApi Knowledge Sources Matrix */}
        <div style={{ marginBottom: '24px' }}>
          <h4 style={{ fontSize: '1.05rem', fontWeight: '700', color: '#ffffff', marginBottom: '12px' }}>
            5 SerpApi Engines Deployed
          </h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '0.82rem' }}>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '10px 14px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ color: '#818cf8', fontWeight: '700' }}>Google Search (MUST)</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.76rem' }}>Existing products & competitors</div>
            </div>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '10px 14px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ color: '#22d3ee', fontWeight: '700' }}>Google News (MUST)</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.76rem' }}>Latest launches & pain points</div>
            </div>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '10px 14px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ color: '#34d399', fontWeight: '700' }}>Google Scholar (MUST)</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.76rem' }}>Academic papers & feasibility</div>
            </div>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '10px 14px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ color: '#fbbf24', fontWeight: '700' }}>Google Trends (MUST)</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.76rem' }}>Search velocity & breakout topics</div>
            </div>
            <div style={{ gridColumn: 'span 2', background: 'rgba(255, 255, 255, 0.03)', padding: '10px 14px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ color: '#f43f5e', fontWeight: '700' }}>Google Patents (Optional / Integrated)</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.76rem' }}>Prior art signals & technological R&D claims</div>
            </div>
          </div>
        </div>

        {/* Killer Feature Note */}
        <div style={{
          padding: '16px',
          background: 'rgba(244, 63, 94, 0.08)',
          border: '1px solid rgba(244, 63, 94, 0.25)',
          borderRadius: 'var(--radius-md)',
          fontSize: '0.84rem',
          color: '#fecdd3'
        }}>
          <strong>The Killer Feature:</strong> Extracting competitor features into an actionable matrix (✓, ✗, ■) instead
          of merely summarizing competitors. The system converts missing incumbent capabilities into a defensible opportunity gap!
        </div>

        <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'flex-end' }}>
          <button onClick={onClose} className="btn-primary" style={{ padding: '10px 24px' }}>
            Got It!
          </button>
        </div>
      </div>
    </div>
  );
}
