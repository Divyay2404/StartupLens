import React, { useEffect, useState } from 'react';
import { Brain, Globe, Database, Building2, Lightbulb, CheckCircle2, Loader2 } from 'lucide-react';

const STEPS = [
  { id: 1, label: 'AI Query Planner', desc: 'Synthesizing targeted queries across 5 engines', icon: Brain },
  { id: 2, label: 'SerpApi Multi-Engine', desc: 'Querying Search, News, Scholar, Trends, Patents', icon: Globe },
  { id: 3, label: 'Evidence Engine', desc: 'Normalizing, deduplicating & ranking sources', icon: Database },
  { id: 4, label: 'Competitor Engine', desc: 'Extracting product capabilities & feature matrix', icon: Building2 },
  { id: 5, label: 'Opportunity Gap Engine', desc: 'Isolating whitespace & differentiation vector', icon: Lightbulb },
];

export default function ResearchStepper({ activeStep = 1 }) {
  const [currentStep, setCurrentStep] = useState(activeStep);

  useEffect(() => {
    // Simulate natural step progression during analysis
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < 5 ? prev + 1 : prev));
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass-panel" style={{ padding: '28px', marginBottom: '32px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: '#ffffff' }}>
            Live Intelligence Pipeline Active
          </h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            Processing multi-source signals via SerpApi and evidence reasoning
          </p>
        </div>
        <div className="scanner-bar" style={{ width: '180px' }} />
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '16px',
        position: 'relative'
      }}>
        {STEPS.map((step) => {
          const Icon = step.icon;
          const isDone = currentStep > step.id;
          const isCurrent = currentStep === step.id;

          return (
            <div
              key={step.id}
              style={{
                background: isCurrent
                  ? 'rgba(99, 102, 241, 0.12)'
                  : isDone
                  ? 'rgba(16, 185, 129, 0.06)'
                  : 'rgba(255, 255, 255, 0.02)',
                border: isCurrent
                  ? '1px solid var(--accent-primary)'
                  : isDone
                  ? '1px solid rgba(16, 185, 129, 0.3)'
                  : '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                transition: 'all 0.3s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '8px',
                  background: isCurrent ? 'var(--accent-primary)' : isDone ? 'var(--accent-emerald)' : 'rgba(255, 255, 255, 0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Icon size={16} color="#ffffff" />
                </div>
                {isDone ? (
                  <CheckCircle2 size={16} color="#34d399" />
                ) : isCurrent ? (
                  <Loader2 size={16} color="#818cf8" className="pulse-circle" style={{ animation: 'spin 1.5s linear infinite' }} />
                ) : (
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Step {step.id}</span>
                )}
              </div>
              <div style={{ fontSize: '0.9rem', fontWeight: '700', color: isCurrent ? '#ffffff' : isDone ? '#e2e8f0' : 'var(--text-secondary)' }}>
                {step.label}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                {step.desc}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
