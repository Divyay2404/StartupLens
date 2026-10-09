import React, { useState } from 'react';
import { Search, TrendingUp, BookOpen, Newspaper, FileCode2, ExternalLink, ShieldAlert, ArrowUpRight } from 'lucide-react';

export default function EvidenceTabs({
  competitors = [],
  trends = [],
  scholar = [],
  news = [],
  patents = []
}) {
  const [activeTab, setActiveTab] = useState('COMPETITORS');

  const trendData = trends[0] || null;

  return (
    <div className="glass-panel" style={{ padding: '32px', marginBottom: '36px' }}>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--accent-cyan)' }}>
            Traceable Knowledge Sources
          </span>
          <span className="badge badge-engine">SerpApi Multi-Engine</span>
        </div>
        <h2 style={{ fontSize: '1.6rem', fontWeight: '800', color: '#ffffff' }}>
          Multi-Source Evidence Intelligence
        </h2>
        <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)' }}>
          Every strategic conclusion is grounded in live data extracted across Google Search, Trends, Scholar, News, and Patents.
        </p>
      </div>

      {/* Tabs Navigation */}
      <div style={{
        display: 'flex',
        gap: '8px',
        borderBottom: '1px solid var(--border-subtle)',
        paddingBottom: '12px',
        marginBottom: '24px',
        overflowX: 'auto'
      }}>
        {[
          { id: 'COMPETITORS', label: 'Competitors', icon: Search, count: competitors.length, engine: 'Google Search' },
          { id: 'TRENDS', label: 'Market Demand', icon: TrendingUp, count: trendData?.timeline?.length || 0, engine: 'Google Trends' },
          { id: 'SCHOLAR', label: 'Academic Feasibility', icon: BookOpen, count: scholar.length, engine: 'Google Scholar' },
          { id: 'NEWS', label: 'Industry Momentum', icon: Newspaper, count: news.length, engine: 'Google News' },
          { id: 'PATENTS', label: 'Patent Signals', icon: FileCode2, count: patents.length, engine: 'Google Patents' },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 18px',
                borderRadius: 'var(--radius-md)',
                background: isActive ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                border: isActive ? '1px solid var(--accent-primary)' : '1px solid transparent',
                color: isActive ? '#ffffff' : 'var(--text-secondary)',
                fontWeight: isActive ? '700' : '500',
                fontSize: '0.86rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                whiteSpace: 'nowrap'
              }}
            >
              <Icon size={16} color={isActive ? '#818cf8' : 'currentColor'} />
              <span>{tab.label}</span>
              <span style={{
                fontSize: '0.72rem',
                padding: '2px 6px',
                borderRadius: '10px',
                background: isActive ? 'var(--accent-primary)' : 'rgba(255, 255, 255, 0.08)',
                color: '#ffffff'
              }}>
                {tab.count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Tab 1: Competitors (Google Search) */}
      {activeTab === 'COMPETITORS' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
          {competitors.map((comp, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(15, 22, 36, 0.8)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '20px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <h4 style={{ fontSize: '1.1rem', fontWeight: '700', color: '#ffffff' }}>
                    {comp.name}
                  </h4>
                  {comp.url && (
                    <a
                      href={comp.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: 'var(--accent-cyan)', display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '0.78rem', textDecoration: 'none' }}
                    >
                      Visit <ExternalLink size={12} />
                    </a>
                  )}
                </div>
                <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', marginBottom: '14px', lineHeight: '1.5' }}>
                  {comp.summary}
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.8rem', marginBottom: '16px' }}>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <span style={{ color: 'var(--text-muted)', minWidth: '95px' }}>Target Audience:</span>
                    <span style={{ color: '#e2e8f0', fontWeight: '500' }}>{comp.target_audience}</span>
                  </div>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <span style={{ color: 'var(--text-muted)', minWidth: '95px' }}>Pricing Model:</span>
                    <span style={{ color: '#fbbf24', fontWeight: '600' }}>{comp.pricing_model}</span>
                  </div>
                </div>
              </div>

              <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '12px' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: '700', color: '#fb7185', textTransform: 'uppercase', marginBottom: '4px' }}>
                  Vulnerable Flaw / Gap:
                </div>
                <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>
                  {comp.weaknesses?.[0] || 'Lacks localized edge capabilities and affordable entry point.'}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab 2: Market Trends (Google Trends) */}
      {activeTab === 'TRENDS' && (
        <div>
          {trendData ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              {/* Trends Metric Summary */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                gap: '16px',
                background: 'rgba(0, 0, 0, 0.3)',
                padding: '20px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-subtle)'
              }}>
                <div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Trend Keyword Target</div>
                  <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#ffffff', marginTop: '4px' }}>
                    "{trendData.keyword}"
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Trajectory Signal</div>
                  <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#34d399', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <TrendingUp size={20} />
                    {trendData.direction}
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Search Momentum</div>
                  <div style={{ fontSize: '1.25rem', fontWeight: '700', color: 'var(--accent-cyan)', marginTop: '4px' }}>
                    {trendData.growth_rate}
                  </div>
                </div>
              </div>

              {/* Visual SVG Timeline Chart */}
              <div style={{
                background: 'rgba(15, 22, 36, 0.8)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '24px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                  <h4 style={{ fontSize: '0.95rem', fontWeight: '700', color: '#ffffff' }}>
                    Search Interest Velocity Over Time (SerpApi Timeseries)
                  </h4>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Index: 0 - 100 Relative Volume</span>
                </div>

                <div style={{ height: '140px', display: 'flex', alignItems: 'flex-end', gap: '24px', padding: '10px 0' }}>
                  {trendData.timeline.map((point, idx) => (
                    <div key={idx} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%', justifyContent: 'flex-end' }}>
                      <div style={{ fontSize: '0.72rem', fontWeight: '700', color: '#22d3ee', marginBottom: '4px' }}>
                        {point.value}
                      </div>
                      <div style={{
                        width: '100%',
                        maxWidth: '48px',
                        height: `${Math.max(point.value, 15)}%`,
                        background: 'linear-gradient(180deg, #22d3ee 0%, #6366f1 100%)',
                        borderRadius: '6px 6px 0 0',
                        transition: 'height 0.4s ease'
                      }} />
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '6px' }}>
                        {point.date}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Related Rising Queries & Breakout Topics */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                <div style={{ background: 'rgba(15, 22, 36, 0.6)', padding: '18px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: '700', color: '#818cf8', textTransform: 'uppercase', marginBottom: '10px' }}>
                    Rising Related Searches
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {trendData.related_queries.map((q, idx) => (
                      <span key={idx} style={{
                        fontSize: '0.78rem',
                        padding: '4px 10px',
                        borderRadius: '6px',
                        background: 'rgba(99, 102, 241, 0.12)',
                        color: '#c7d2fe',
                        border: '1px solid rgba(99, 102, 241, 0.25)'
                      }}>
                        {q}
                      </span>
                    ))}
                  </div>
                </div>

                <div style={{ background: 'rgba(15, 22, 36, 0.6)', padding: '18px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: '700', color: '#22d3ee', textTransform: 'uppercase', marginBottom: '10px' }}>
                    Adjacent Breakout Topics
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {trendData.related_topics.map((t, idx) => (
                      <span key={idx} style={{
                        fontSize: '0.78rem',
                        padding: '4px 10px',
                        borderRadius: '6px',
                        background: 'rgba(6, 182, 212, 0.12)',
                        color: '#a5f3fc',
                        border: '1px solid rgba(6, 182, 212, 0.25)'
                      }}>
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>No trends signal available.</p>
          )}
        </div>
      )}

      {/* Tab 3: Google Scholar Research */}
      {activeTab === 'SCHOLAR' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{
            padding: '12px 18px',
            background: 'rgba(16, 185, 129, 0.08)',
            border: '1px solid rgba(16, 185, 129, 0.25)',
            borderRadius: 'var(--radius-md)',
            fontSize: '0.84rem',
            color: '#a7f3d0'
          }}>
            📚 <strong>Academic Grounding:</strong> These peer-reviewed publications validate that your proposed technical approach (e.g. edge compression, offline algorithms) is proven feasible by researchers.
          </div>

          {scholar.map((paper, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(15, 22, 36, 0.8)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '20px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '12px', marginBottom: '8px' }}>
                <a
                  href={paper.link || 'https://scholar.google.com'}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    fontSize: '1.05rem',
                    fontWeight: '700',
                    color: '#ffffff',
                    textDecoration: 'none',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.color = 'var(--accent-primary-light)'}
                  onMouseLeave={(e) => e.currentTarget.style.color = '#ffffff'}
                >
                  {paper.title} <ArrowUpRight size={15} color="var(--accent-cyan)" />
                </a>

                {paper.citations > 0 && (
                  <span style={{
                    fontSize: '0.72rem',
                    fontWeight: '700',
                    padding: '3px 8px',
                    borderRadius: '6px',
                    background: 'rgba(16, 185, 129, 0.15)',
                    color: '#34d399',
                    border: '1px solid rgba(16, 185, 129, 0.3)',
                    whiteSpace: 'nowrap'
                  }}>
                    {paper.citations} citations
                  </span>
                )}
              </div>

              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>
                <strong>Authors:</strong> {paper.authors} • <strong>Year:</strong> {paper.year}
              </div>

              <p style={{ fontSize: '0.86rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                "{paper.key_takeaway}"
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Tab 4: Google News */}
      {activeTab === 'NEWS' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '18px' }}>
          {news.map((item, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(15, 22, 36, 0.8)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '20px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--accent-cyan)', marginBottom: '8px' }}>
                  <span>{item.source}</span>
                  <span style={{ color: 'var(--text-muted)' }}>{item.date}</span>
                </div>
                <h4 style={{ fontSize: '0.98rem', fontWeight: '700', color: '#ffffff', marginBottom: '10px', lineHeight: '1.4' }}>
                  {item.title}
                </h4>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                  {item.snippet}
                </p>
              </div>

              {item.link && (
                <div style={{ marginTop: '16px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '10px' }}>
                  <a
                    href={item.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ fontSize: '0.78rem', color: '#818cf8', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    Read coverage <ExternalLink size={12} />
                  </a>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Tab 5: Google Patents */}
      {activeTab === 'PATENTS' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Legal Disclaimer Box */}
          <div style={{
            padding: '14px 18px',
            background: 'rgba(245, 158, 11, 0.1)',
            border: '1px solid rgba(245, 158, 11, 0.3)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '12px'
          }}>
            <ShieldAlert size={20} color="#fbbf24" style={{ marginTop: '2px', flexShrink: 0 }} />
            <div>
              <div style={{ fontSize: '0.84rem', fontWeight: '700', color: '#fbbf24' }}>
                Patent Intelligence Caution & Disclaimer
              </div>
              <p style={{ fontSize: '0.8rem', color: '#fde68a', marginTop: '2px', lineHeight: '1.4' }}>
                Patent results are high-level discovery signals indicating active technological R&D clusters.
                They do <strong>not</strong> constitute formal legal clearance, freedom-to-operate counsel, or patentability verification.
              </p>
            </div>
          </div>

          {patents.map((pat, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(15, 22, 36, 0.8)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '20px'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '12px', marginBottom: '8px' }}>
                <a
                  href={pat.link || 'https://patents.google.com'}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    fontSize: '1.05rem',
                    fontWeight: '700',
                    color: '#ffffff',
                    textDecoration: 'none',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.color = 'var(--accent-primary-light)'}
                  onMouseLeave={(e) => e.currentTarget.style.color = '#ffffff'}
                >
                  {pat.title} <ArrowUpRight size={14} color="var(--accent-cyan)" />
                </a>

                <span style={{
                  fontSize: '0.72rem',
                  fontFamily: 'var(--font-mono)',
                  padding: '3px 8px',
                  borderRadius: '6px',
                  background: 'rgba(99, 102, 241, 0.15)',
                  color: '#a5b4fc',
                  border: '1px solid rgba(99, 102, 241, 0.3)',
                  whiteSpace: 'nowrap'
                }}>
                  {pat.patent_id}
                </span>
              </div>

              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '10px' }}>
                <strong>Assignee:</strong> {pat.assignee} {pat.filing_date && `• Filed: ${pat.filing_date}`}
              </div>

              <p style={{ fontSize: '0.84rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                {pat.summary}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
