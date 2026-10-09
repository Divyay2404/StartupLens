import React, { useState } from 'react';
import { Check, X, Minus, Sparkles, ChevronDown, ChevronUp, Layers } from 'lucide-react';

export default function OpportunityMatrix({ matrix, competitors, userIdeaTitle }) {
  const [filter, setFilter] = useState('ALL');
  const [expandedRow, setExpandedRow] = useState(null);

  if (!matrix || matrix.length === 0) return null;

  const competitorNames = competitors?.slice(0, 3).map((c) => c.name) || [];

  const filteredRows = matrix.filter((row) => {
    if (filter === 'ALL') return true;
    if (filter === 'CRITICAL') return row.importance === 'Critical';
    return row.category?.toLowerCase().includes(filter.toLowerCase());
  });

  const renderBadge = (val) => {
    const v = (val || '').toLowerCase();
    if (v === 'yes') {
      return (
        <span className="status-pill status-yes" title="Present / Native Capability">
          <Check size={16} strokeWidth={3} />
        </span>
      );
    }
    if (v === 'partial') {
      return (
        <span className="status-pill status-partial" title="Partial / Limited Capability">
          <Minus size={16} strokeWidth={3} />
        </span>
      );
    }
    return (
      <span className="status-pill status-no" title="Missing / Not Supported">
        <X size={16} strokeWidth={3} />
      </span>
    );
  };

  return (
    <div className="glass-panel" style={{ padding: '32px', marginBottom: '36px' }}>
      {/* Header and Killer Feature Banner */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '24px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
            <span style={{
              fontSize: '0.72rem',
              fontWeight: '700',
              fontFamily: 'var(--font-mono)',
              textTransform: 'uppercase',
              padding: '3px 8px',
              borderRadius: '4px',
              background: 'rgba(244, 63, 94, 0.15)',
              color: '#fb7185',
              border: '1px solid rgba(244, 63, 94, 0.3)'
            }}>
              Killer Feature
            </span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Opportunity Gap Engine
            </span>
          </div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: '800', color: '#ffffff' }}>
            Competitor Capability Matrix
          </h2>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Instead of merely summarizing competitors, StartupLens converts missing incumbent capabilities into your defensible market gap.
          </p>
        </div>

        {/* Legend */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '14px',
          padding: '8px 16px',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(0, 0, 0, 0.35)',
          border: '1px solid var(--border-subtle)',
          fontSize: '0.78rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span className="status-pill status-yes" style={{ width: '20px', height: '20px' }}><Check size={12} /></span>
            <span style={{ color: '#34d399' }}>Full Capability</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span className="status-pill status-partial" style={{ width: '20px', height: '20px' }}><Minus size={12} /></span>
            <span style={{ color: '#fbbf24' }}>Partial / Flawed</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span className="status-pill status-no" style={{ width: '20px', height: '20px' }}><X size={12} /></span>
            <span style={{ color: '#fb7185' }}>Missing (Opportunity)</span>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '18px', flexWrap: 'wrap' }}>
        {[
          { id: 'ALL', label: 'All Capabilities' },
          { id: 'CRITICAL', label: 'Critical Constraints Only' },
          { id: 'Architecture', label: 'Architecture & Tech' },
          { id: 'Afford', label: 'Cost & Distribution' },
        ].map((btn) => (
          <button
            key={btn.id}
            onClick={() => setFilter(btn.id)}
            style={{
              padding: '6px 14px',
              borderRadius: 'var(--radius-full)',
              fontSize: '0.78rem',
              fontWeight: '600',
              cursor: 'pointer',
              border: filter === btn.id ? '1px solid var(--accent-primary)' : '1px solid var(--border-subtle)',
              background: filter === btn.id ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255, 255, 255, 0.03)',
              color: filter === btn.id ? '#ffffff' : 'var(--text-secondary)',
              transition: 'all 0.2s ease'
            }}
          >
            {btn.label}
          </button>
        ))}
      </div>

      {/* Interactive Matrix Table */}
      <div className="matrix-container">
        <table className="matrix-table">
          <thead>
            <tr>
              <th style={{ width: '28%' }}>Feature / Capability</th>
              {competitorNames.map((name, idx) => (
                <th key={idx} style={{ textAlign: 'center', width: '16%' }}>
                  <div style={{ color: '#e2e8f0', fontWeight: '700', fontSize: '0.8rem' }}>
                    {name.length > 20 ? name.slice(0, 18) + '...' : name}
                  </div>
                  <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', textTransform: 'none', fontWeight: '400' }}>
                    Incumbent {idx + 1}
                  </div>
                </th>
              ))}
              <th className="matrix-th-user" style={{ textAlign: 'center', width: '22%' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                  <Sparkles size={14} color="#818cf8" />
                  <span style={{ color: '#ffffff', fontWeight: '800' }}>
                    {userIdeaTitle ? (userIdeaTitle.length > 20 ? userIdeaTitle.slice(0, 18) + '...' : userIdeaTitle) : 'Your Startup Idea'}
                  </span>
                </div>
                <div style={{ fontSize: '0.68rem', color: '#c7d2fe', textTransform: 'none', fontWeight: '500' }}>
                  Targeted Wedge
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredRows.map((row, idx) => {
              const isExpanded = expandedRow === idx;
              return (
                <React.Fragment key={idx}>
                  <tr
                    onClick={() => setExpandedRow(isExpanded ? null : idx)}
                    style={{ cursor: 'pointer' }}
                  >
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div>
                          <div style={{ fontWeight: '700', color: '#ffffff', fontSize: '0.94rem' }}>
                            {row.feature_name}
                          </div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '3px' }}>
                            <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                              {row.category}
                            </span>
                            {row.importance === 'Critical' && (
                              <span style={{
                                fontSize: '0.65rem',
                                padding: '1px 5px',
                                borderRadius: '4px',
                                background: 'rgba(244, 63, 94, 0.15)',
                                color: '#fb7185',
                                fontWeight: '700'
                              }}>
                                Critical Gap
                              </span>
                            )}
                          </div>
                        </div>
                        <div style={{ color: 'var(--text-muted)' }}>
                          {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                        </div>
                      </div>
                    </td>

                    {/* Competitor Ratings */}
                    {competitorNames.map((name, cIdx) => (
                      <td key={cIdx} style={{ textAlign: 'center' }}>
                        {renderBadge(row.competitor_ratings[name])}
                      </td>
                    ))}

                    {/* User Idea Rating */}
                    <td className="matrix-col-user" style={{ textAlign: 'center' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                        {renderBadge(row.user_idea_rating)}
                        <span style={{ fontSize: '0.78rem', color: '#34d399', fontWeight: '700' }}>Native</span>
                      </div>
                    </td>
                  </tr>

                  {/* Expanded Opportunity Rationale Details */}
                  {isExpanded && (
                    <tr>
                      <td colSpan={competitorNames.length + 2} style={{ background: 'rgba(15, 23, 42, 0.7)', padding: '16px 24px' }}>
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                          <div style={{
                            padding: '6px',
                            borderRadius: '8px',
                            background: 'rgba(99, 102, 241, 0.15)',
                            marginTop: '2px'
                          }}>
                            <Layers size={16} color="var(--accent-primary-light)" />
                          </div>
                          <div>
                            <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                              Why this is your defensible opportunity gap:
                            </div>
                            <p style={{ fontSize: '0.88rem', color: '#e2e8f0', marginTop: '4px', lineHeight: '1.5' }}>
                              {row.opportunity_reason}
                            </p>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>

      <div style={{
        marginTop: '16px',
        padding: '12px 18px',
        background: 'rgba(255, 255, 255, 0.02)',
        borderRadius: 'var(--radius-sm)',
        border: '1px solid rgba(255, 255, 255, 0.05)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '0.8rem',
        color: 'var(--text-secondary)'
      }}>
        <span>💡 Click on any feature row to inspect the competitive whitespace breakdown.</span>
        <span style={{ color: 'var(--accent-cyan)' }}>Evidence Source: Live SerpApi Extraction</span>
      </div>
    </div>
  );
}
