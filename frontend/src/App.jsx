import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import IdeaForm from './components/IdeaForm';
import ResearchStepper from './components/ResearchStepper';
import ViabilityScorecard from './components/ViabilityScorecard';
import OpportunityMatrix from './components/OpportunityMatrix';
import EvidenceTabs from './components/EvidenceTabs';
import GapsAndRoadmap from './components/GapsAndRoadmap';
import SettingsModal from './components/SettingsModal';
import PitchModal from './components/PitchModal';
import { AlertCircle } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const FALLBACK_SAMPLES = [
  {
    id: "rural_attendance",
    title: "AI Attendance System for Rural Schools",
    tag: "EdTech & Computer Vision",
    description: "An automated facial recognition attendance system optimized for low-connectivity rural schools with intermittent electricity and no high-speed internet.",
    target_region: "Emerging Markets / Rural",
    highlight: "Featured in Track 5 Brief"
  },
  {
    id: "soil_health",
    title: "Smartphone Soil Health Scanner for Smallholders",
    tag: "AgriTech & Remote Sensing",
    description: "Instant optical soil nutrient analysis using smartphone camera color calibration cards to diagnose NPK deficiencies without expensive laboratory spectrometers.",
    target_region: "Global South / Agriculture",
    highlight: "High Social Impact"
  },
  {
    id: "bakery_surplus",
    title: "Hyperlocal Bakery Surplus Real-Time Clearinghouse",
    tag: "FoodTech & Circular Economy",
    description: "B2B micro-marketplace that alerts neighborhood cafes and shelters to fresh unsold bakery goods 1 hour before closing with dynamic pricing.",
    target_region: "Urban Centers",
    highlight: "Micro-SaaS Niche"
  },
  {
    id: "senior_triage",
    title: "AI Voice Agent for Rural Senior Telehealth Triage",
    tag: "HealthTech & Voice AI",
    description: "Phone-call based voice assistant capable of triaging symptoms in local vernacular dialects for elderly patients who lack smartphones or internet literacy.",
    target_region: "Rural Healthcare",
    highlight: "Accessibility Wedge"
  }
];

export default function App() {
  const [idea, setIdea] = useState('AI attendance system for rural schools');
  const [targetRegion, setTargetRegion] = useState('Emerging Markets / Rural');
  const [includePatents, setIncludePatents] = useState(true);
  const [sampleIdeas, setSampleIdeas] = useState(FALLBACK_SAMPLES);
  
  const [isLoading, setIsLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const [isLiveSerpApi, setIsLiveSerpApi] = useState(false);
  const [serpApiKey, setSerpApiKey] = useState(() => localStorage.getItem('STARTUPLENS_SERPAPI_KEY') || '');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isPitchOpen, setIsPitchOpen] = useState(false);

  // Initial health check and load sample ideas
  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((res) => res.json())
      .then((data) => {
        setIsLiveSerpApi(data.serpapi_configured || Boolean(serpApiKey));
      })
      .catch(() => {
        // Backend running on proxy or offline
      });

    fetch(`${API_BASE}/api/examples`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setSampleIdeas(data);
        }
      })
      .catch(() => {});
  }, [serpApiKey]);

  // Execute Idea Analysis
  const executeAnalysis = useCallback(async (ideaText, region, patents) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          idea: ideaText,
          target_region: region,
          include_patents: patents,
          serpapi_api_key: serpApiKey || null
        })
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const data = await response.json();
      setReport(data);
      if (data.meta?.is_live_serpapi) {
        setIsLiveSerpApi(true);
      }
    } catch (err) {
      console.error("Analysis request failed:", err);
      setError("Unable to connect to backend server. Ensure backend is running at http://127.0.0.1:8000");
    } finally {
      setIsLoading(false);
    }
  }, [serpApiKey]);

  // Run initial analysis automatically on mount so page loads with rich data!
  useEffect(() => {
    let ignore = false;
    Promise.resolve().then(() => {
      if (!ignore) {
        executeAnalysis(
          'AI attendance system for rural schools',
          'Emerging Markets / Rural',
          true
        );
      }
    });

    return () => {
      ignore = true;
    };
  }, [executeAnalysis]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!idea.trim()) return;
    executeAnalysis(idea, targetRegion, includePatents);
  };

  const handleSelectSample = (sample) => {
    setIdea(sample.description || sample.title);
    setTargetRegion(sample.target_region || 'Global');
    executeAnalysis(sample.description || sample.title, sample.target_region || 'Global', includePatents);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Navigation */}
      <Navbar
        isLiveSerpApi={isLiveSerpApi}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onOpenPitch={() => setIsPitchOpen(true)}
      />

      {/* Main Container */}
      <main style={{ maxWidth: '1280px', width: '100%', margin: '0 auto', padding: '36px 20px', flex: 1 }}>
        {/* Error notification */}
        {error && (
          <div style={{
            padding: '16px 20px',
            background: 'rgba(244, 63, 94, 0.15)',
            border: '1px solid rgba(244, 63, 94, 0.4)',
            borderRadius: 'var(--radius-md)',
            marginBottom: '24px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            color: '#fecdd3',
            fontSize: '0.9rem'
          }}>
            <AlertCircle size={20} color="#fb7185" />
            <div>
              <strong>Connection Warning:</strong> {error}
            </div>
          </div>
        )}

        {/* Idea Input Studio */}
        <IdeaForm
          idea={idea}
          setIdea={setIdea}
          targetRegion={targetRegion}
          setTargetRegion={setTargetRegion}
          includePatents={includePatents}
          setIncludePatents={setIncludePatents}
          sampleIdeas={sampleIdeas}
          onSelectSample={handleSelectSample}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />

        {/* Live Stepper Tracker during loading */}
        {isLoading && <ResearchStepper activeStep={2} />}

        {/* Assessment Results Section */}
        {report && !isLoading && (
          <div>
            {/* 1. Viability Scorecard & Executive Opportunity */}
            <ViabilityScorecard
              viability={report.viability}
              coreOpportunity={report.core_opportunity}
              executiveSummary={report.executive_summary}
              domain={report.research_plan?.core_domain}
            />

            {/* 2. Killer Feature: Opportunity Gap Matrix */}
            <OpportunityMatrix
              matrix={report.competitor_matrix}
              competitors={report.competitors}
              userIdeaTitle={report.idea}
            />

            {/* 3. Multi-Engine Traceable Evidence Tabs */}
            <EvidenceTabs
              competitors={report.competitors}
              trends={report.trend_signals}
              scholar={report.scholar_insights}
              news={report.news_developments}
              patents={report.patents}
              meta={report.meta}
            />

            {/* 4. Identified Gaps & Strategic Roadmap */}
            <GapsAndRoadmap
              gaps={report.gaps}
              roadmap={report.strategic_roadmap}
              reportData={report}
            />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid var(--border-subtle)',
        padding: '28px 24px',
        textAlign: 'center',
        fontSize: '0.82rem',
        color: 'var(--text-muted)',
        background: 'rgba(7, 9, 14, 0.95)'
      }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <strong>StartupLens</strong> — SerpApi Hackathon 2026 (Track 5: Idea Validation & Opportunity Discovery)
          </div>
          <div style={{ display: 'flex', gap: '16px' }}>
            <span>Google Search</span>
            <span>Google News</span>
            <span>Google Scholar</span>
            <span>Google Trends</span>
            <span>Google Patents</span>
          </div>
        </div>
      </footer>

      {/* Modals */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        serpApiKey={serpApiKey}
        setSerpApiKey={setSerpApiKey}
      />

      <PitchModal
        isOpen={isPitchOpen}
        onClose={() => setIsPitchOpen(false)}
      />
    </div>
  );
}
