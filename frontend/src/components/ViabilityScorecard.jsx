import React from 'react';
import { Compass, Sparkles } from 'lucide-react';

export default function ViabilityScorecard({ viability, coreOpportunity, executiveSummary, domain }) {
  if (!viability) return null;

  const clamp = (val) => {
    const num = Number(val);
    if (isNaN(num)) return 0;
    return Math.min(Math.max(Math.round(num), 0), 100);
  };

  const score = clamp(viability.overall);
  const scoreColor = score >= 80 ? '#34d399' : score >= 65 ? '#22d3ee' : '#fbbf24';

  const marketDemand = clamp(viability.market_demand);
  const differentiation = clamp(viability.differentiation_potential);
  const techFeasibility = clamp(viability.tech_feasibility);
  const competitorSaturation = clamp(viability.competitor_saturation);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px', marginBottom: '36px' }}>
      {/* Viability Gauge & Submetrics */}
      <div className="glass-panel" style={{ padding: '28px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)' }}>
              Opportunity Viability Score
            </span>
            <span style={{
              fontSize: '0.75rem',
              fontWeight: '600',
              padding: '3px 8px',
              borderRadius: '6px',
              background: 'rgba(99, 102, 241, 0.15)',
              color: '#818cf8',
              border: '1px solid rgba(99, 102, 241, 0.3)'
            }}>
              {domain || "Emerging Market"}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '24px', marginBottom: '20px' }}>
            {/* Circular Gauge Display */}
            <div style={{
              position: 'relative',
              width: '100px',
              height: '100px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: `conic-gradient(${scoreColor} ${score * 3.6}deg, rgba(255, 255, 255, 0.08) 0deg)`,
              boxShadow: `0 0 25px ${scoreColor}40`,
              transition: 'all 0.5s ease'
            }}>
              <div style={{
                width: '82px',
                height: '82px',
                borderRadius: '50%',
                background: 'var(--bg-dark)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <span style={{ fontSize: '1.75rem', fontWeight: '800', fontFamily: 'var(--font-heading)', color: scoreColor, lineHeight: '1' }}>
                  {score}
                </span>
                <span style={{ fontSize: '0.62rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>out of 100</span>
              </div>
            </div>

            <div>
              <div style={{ fontSize: '1.15rem', fontWeight: '700', color: '#ffffff', marginBottom: '4px' }}>
                {viability.verdict || "Evaluated Opportunity"}
              </div>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                {viability.rationale || "Calculated across market demand velocity, competitive saturation, technical feasibility, and differentiation potential."}
              </p>
            </div>
          </div>
        </div>

        {/* 4 Dimension Bars */}
        <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.06)', paddingTop: '16px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Market Demand</span>
                <span style={{ fontWeight: '600', color: '#22d3ee' }}>{marketDemand}%</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${marketDemand}%`, height: '100%', background: '#22d3ee', borderRadius: '3px', transition: 'width 0.4s ease' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Differentiation</span>
                <span style={{ fontWeight: '600', color: '#818cf8' }}>{differentiation}%</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${differentiation}%`, height: '100%', background: '#818cf8', borderRadius: '3px', transition: 'width 0.4s ease' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Tech Feasibility</span>
                <span style={{ fontWeight: '600', color: '#34d399' }}>{techFeasibility}%</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${techFeasibility}%`, height: '100%', background: '#34d399', borderRadius: '3px', transition: 'width 0.4s ease' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Market Saturation</span>
                <span style={{ fontWeight: '600', color: '#fbbf24' }}>{competitorSaturation}%</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${competitorSaturation}%`, height: '100%', background: '#fbbf24', borderRadius: '3px', transition: 'width 0.4s ease' }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Core Opportunity Synthesis Box */}
      <div className="glass-panel" style={{
        padding: '28px',
        background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.09) 0%, rgba(16, 22, 36, 0.8) 100%)',
        border: '1px solid rgba(99, 102, 241, 0.35)',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
            <Compass size={18} color="var(--accent-amber)" />
            <span style={{
              fontSize: '0.8rem',
              fontWeight: '700',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              color: 'var(--accent-amber)'
            }}>
              Identified Opportunity Wedge
            </span>
          </div>

          <h3 style={{
            fontSize: '1.28rem',
            fontWeight: '700',
            color: '#ffffff',
            lineHeight: '1.45',
            marginBottom: '16px'
          }}>
            {coreOpportunity}
          </h3>

          <p style={{
            fontSize: '0.88rem',
            color: 'var(--text-secondary)',
            lineHeight: '1.6',
            marginBottom: '16px'
          }}>
            {executiveSummary}
          </p>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '10px 14px',
          background: 'rgba(0, 0, 0, 0.35)',
          borderRadius: 'var(--radius-sm)',
          border: '1px solid rgba(255, 255, 255, 0.06)'
        }}>
          <Sparkles size={16} color="var(--accent-cyan)" />
          <span style={{ fontSize: '0.78rem', color: '#cbd5e1' }}>
            <strong>Strategic Thesis:</strong> Build where incumbents cannot afford or are unwilling to architect down.
          </span>
        </div>
      </div>
    </div>
  );
}
