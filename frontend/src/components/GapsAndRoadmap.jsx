import React, { useState } from 'react';
import { Target, Milestone, Download, Copy, Check } from 'lucide-react';

export default function GapsAndRoadmap({ gaps = [], roadmap = [], reportData }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!reportData) return;
    const text = `
# StartupLens Opportunity Assessment: ${reportData.idea}
Viability Score: ${reportData.viability?.overall}/100 (${reportData.viability?.verdict})

Core Opportunity:
${reportData.core_opportunity}

Unaddressed Market Gaps:
${gaps.map((g, i) => `${i + 1}. ${g.title}: ${g.description}`).join('\n')}

Roadmap:
${roadmap.map((r) => `${r.phase}: ${r.title}`).join('\n')}
    `.trim();

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handleExportMarkdown = () => {
    if (!reportData) return;
    const md = `
# StartupLens: Evidence-Backed Opportunity Assessment
**Startup Concept:** ${reportData.idea}
**Viability Score:** ${reportData.viability?.overall}/100 — ${reportData.viability?.verdict}
**Generated via:** SerpApi Multi-Engine Intelligence (Search, News, Scholar, Trends, Patents)

---

## 1. Executive Summary
${reportData.executive_summary}

## 2. Differentiated Opportunity Wedge
${reportData.core_opportunity}

## 3. Killer Feature: Competitor Capability Matrix
| Feature | Importance | Incumbents | User Idea | Opportunity Rationale |
|---|---|---|---|---|
${reportData.competitor_matrix?.map((r) => `| ${r.feature_name} | ${r.importance} | Lacking / Flawed | Native (✓) | ${r.opportunity_reason} |`).join('\n')}

## 4. Unaddressed Opportunity Gaps
${gaps.map((g) => `### ${g.title} (${g.gap_type})\n- **Description:** ${g.description}\n- **Differentiation:** ${g.recommended_differentiation}\n- **Traceable Evidence:** ${g.evidence_sources?.join(', ')}\n`).join('\n')}

## 5. 3-Stage Execution Roadmap
${roadmap.map((r) => `### ${r.phase}: ${r.title}\n**Focus:** ${r.focus}\n${r.deliverables?.map((d) => `- ${d}`).join('\n')}\n`).join('\n')}

---
*Notice: Patent results are exploratory discovery signals, not legal freedom-to-operate advice.*
    `.trim();

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `StartupLens_Assessment_${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '36px', marginBottom: '40px' }}>
      {/* Opportunity Gaps Deep Dive */}
      <div className="glass-panel" style={{ padding: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', marginBottom: '24px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <Target size={18} color="var(--accent-rose)" />
              <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--accent-rose)' }}>
                Evidence-Derived Whitespace
              </span>
            </div>
            <h3 style={{ fontSize: '1.5rem', fontWeight: '800', color: '#ffffff' }}>
              Identified Opportunity Gaps
            </h3>
            <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)' }}>
              These gaps stem directly from missing competitor capabilities and academic findings.
            </p>
          </div>

          {/* Action buttons */}
          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={handleCopy} className="btn-secondary">
              {copied ? <Check size={14} color="#34d399" /> : <Copy size={14} />}
              <span>{copied ? 'Copied Assessment!' : 'Copy Summary'}</span>
            </button>
            <button onClick={handleExportMarkdown} className="btn-secondary" style={{ borderColor: 'var(--accent-primary)' }}>
              <Download size={14} color="var(--accent-primary-light)" />
              <span>Export Markdown</span>
            </button>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '18px' }}>
          {gaps.map((gap, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(15, 22, 36, 0.75)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '22px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{
                    fontSize: '0.72rem',
                    fontWeight: '700',
                    fontFamily: 'var(--font-mono)',
                    padding: '3px 8px',
                    borderRadius: '6px',
                    background: 'rgba(244, 63, 94, 0.15)',
                    color: '#fb7185',
                    border: '1px solid rgba(244, 63, 94, 0.3)'
                  }}>
                    {gap.gap_type}
                  </span>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Gap #{idx + 1}</span>
                </div>

                <h4 style={{ fontSize: '1.08rem', fontWeight: '700', color: '#ffffff', marginBottom: '8px' }}>
                  {gap.title}
                </h4>

                <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', lineHeight: '1.5', marginBottom: '16px' }}>
                  {gap.description}
                </p>
              </div>

              <div>
                <div style={{
                  padding: '12px 14px',
                  borderRadius: 'var(--radius-sm)',
                  background: 'rgba(99, 102, 241, 0.08)',
                  border: '1px solid rgba(99, 102, 241, 0.2)',
                  marginBottom: '12px'
                }}>
                  <div style={{ fontSize: '0.72rem', fontWeight: '700', color: '#a5b4fc', textTransform: 'uppercase', marginBottom: '4px' }}>
                    Differentiation Tactic:
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#e0e7ff', lineHeight: '1.4' }}>
                    {gap.recommended_differentiation}
                  </div>
                </div>

                {gap.evidence_sources && gap.evidence_sources.length > 0 && (
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    <strong>Traceable Sources:</strong> {gap.evidence_sources.join(' • ')}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 3-Stage Execution Roadmap */}
      <div className="glass-panel" style={{ padding: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <Milestone size={18} color="var(--accent-cyan)" />
          <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--accent-cyan)' }}>
            Strategic Execution Framework
          </span>
        </div>
        <h3 style={{ fontSize: '1.5rem', fontWeight: '800', color: '#ffffff', marginBottom: '6px' }}>
          3-Stage Differentiation Roadmap
        </h3>
        <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', marginBottom: '24px' }}>
          Phased execution plan turning evidence signals into defensible market position.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
          {roadmap.map((stage, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(15, 22, 36, 0.75)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '22px',
                position: 'relative'
              }}
            >
              <div style={{
                position: 'absolute',
                top: '16px',
                right: '16px',
                width: '28px',
                height: '28px',
                borderRadius: '50%',
                background: 'rgba(255, 255, 255, 0.05)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.8rem',
                color: 'var(--accent-cyan)',
                fontWeight: '700'
              }}>
                0{idx + 1}
              </div>

              <div style={{ fontSize: '0.75rem', fontWeight: '700', color: '#818cf8', marginBottom: '6px' }}>
                {stage.phase}
              </div>

              <h4 style={{ fontSize: '1.1rem', fontWeight: '700', color: '#ffffff', marginBottom: '8px' }}>
                {stage.title}
              </h4>

              <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '16px', fontStyle: 'italic' }}>
                Focus: {stage.focus}
              </div>

              <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.06)', paddingTop: '12px' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: '700', color: '#e2e8f0', marginBottom: '8px' }}>
                  Key Deliverables:
                </div>
                <ul style={{ listStyleType: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {stage.deliverables?.map((del, dIdx) => (
                    <li key={dIdx} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.8rem', color: '#cbd5e1', lineHeight: '1.4' }}>
                      <span style={{ color: 'var(--accent-emerald)', marginTop: '2px' }}>✓</span>
                      <span>{del}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
