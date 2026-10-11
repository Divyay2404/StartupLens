# StartupLens — Comprehensive Production & Deployment Issues Audit

**Deployment URL:** [https://startuplens-zeta.vercel.app/](https://startuplens-zeta.vercel.app/)  
**Audit Date:** October 2026  
**Repository:** `Divyay2404/StartupLens`  

---

## Executive Summary

StartupLens is currently deployed and serving both frontend (Vite/React) and backend (FastAPI) via Vercel services. While the basic health check and core pipeline are functional, this audit identified **14 distinct issues** across deployment architecture, residual branding, user interface & interaction bugs, data export inconsistencies, and security.

Each issue is documented below with its severity, affected files, root cause, and concrete recommended solution.

---

## 1. Critical & Infrastructure Issues

### 🔴 Issue 1.1: High Risk of Vercel Serverless Function Execution Timeout (504 Gateway Timeout)
- **Severity:** High
- **Files:** [`backend/app/services/query_planner.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/services/query_planner.py), [`backend/app/services/serpapi_client.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/services/serpapi_client.py)
- **Root Cause:**
  When a user submits an analysis request, `QueryPlanner.plan()` generates **up to 9 distinct SerpApi queries** across 5 engines (3 Google Search, 2 Google News, 2 Google Scholar, 1 Google Trends, 1 Google Patents). In `serpapi_client.py`, each request has a timeout of `12.0s`. While queries run via `asyncio.gather()`, real-world latency across 9 external SerpApi engine calls frequently ranges between 6 to 14 seconds.
  Vercel Hobby tier serverless functions enforce a default **10–15 second maximum execution duration**. Any slow response from Google Trends or Patents causes Vercel to terminate the function with a `504 FUNCTION_INVOCATION_TIMEOUT` error.
- **Recommended Fix:**
  1. Optimize `QueryPlanner` to streamline queries (e.g., reduce Google Search to 1–2 focused queries, 1 News query).
  2. In `vercel.json`, configure maximum function duration if on a Pro plan:
     ```json
     "functions": {
       "backend/app/main.py": { "maxDuration": 30 }
     }
     ```
  3. Reduce individual HTTP timeouts in `serpapi_client.py` to `8.0s` so slow engines fail fast rather than stalling the entire pipeline.

---

### 🔴 Issue 1.2: Rapid Exhaustion of SerpApi Quota Leading to Silent Degradation
- **Severity:** High
- **Files:** [`backend/app/services/query_planner.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/services/query_planner.py), [`backend/app/services/serpapi_client.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/services/serpapi_client.py)
- **Root Cause:**
  Because every single idea validation consumes up to 9 SerpApi searches, only **11 user submissions** will exhaust a standard free SerpApi tier (100 searches/month).
  Once the quota is exhausted (HTTP 429 / 401), `serpapi_client.py` silently falls back to synthetic mock data (`generate_synthetic_serp_data(idea)`). The live app ceases to show real web results without explicitly informing the user that the monthly API quota has been reached.
- **Recommended Fix:**
  1. Implement client-side or in-memory caching (e.g., using normalized idea keywords or LRU cache) to avoid re-querying identical concepts.
  2. When SerpApi quota is exhausted, return a clear banner in `OpportunityReport.meta` indicating: *"Live SerpApi monthly quota exhausted; displaying simulated high-fidelity benchmark intelligence."*

---

### 🟡 Issue 1.3: Unused LLM Keys & Misleading AI Architecture
- **Severity:** Medium
- **Files:** [`backend/app/config.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/config.py), [`backend/app/main.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/main.py), [`backend/app/services/ai_engine.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/services/ai_engine.py)
- **Root Cause:**
  The backend defines `GEMINI_API_KEY` and `OPENAI_API_KEY` in `config.py` and reports them in `/api/health`. However, examining `AIEngine`, `CompetitorEngine`, and `OpportunityEngine` reveals that neither Gemini nor OpenAI is actually implemented in the synthesis code. Opportunity synthesis and matrix ratings are generated via rule-based heuristic templates (`opportunity_engine.py`).
  This creates confusion for users and reviewers who enter OpenAI or Gemini keys expecting LLM reasoning that is never invoked.
- **Recommended Fix:**
  Either integrate actual LLM summarization inside `AIEngine` (e.g. using Google `google-genai` SDK or OpenAI client for the executive summary) or remove the unused Gemini/OpenAI configuration fields from `/api/health` and `.env.example` to accurately represent the system as a SerpApi-driven heuristic analysis engine.

---

## 2. Residual Hackathon & Track 5 Branding (Incomplete Cleanup)

### 🟡 Issue 2.1: Residual "SerpApi Hackathon" & "Track 5" Text in Multiple Files
- **Severity:** Medium
- **Files & Locations:**
  1. **HTML Title Tag:** [`frontend/index.html`](file:///e:/Projects/StartupLens/StartupLens/frontend/index.html) (Line 7):
     ```html
     <title>StartupLens 🚀 | AI Opportunity Intelligence Engine (SerpApi Hackathon)</title>
     ```
     *Fix:* Change to: `<title>StartupLens 🚀 | AI Opportunity Intelligence Engine</title>`
  2. **Footer Text:** [`frontend/src/App.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/App.jsx) (Line 233):
     ```jsx
     <strong>StartupLens</strong> — SerpApi Hackathon 2026 (Track 5: Idea Validation & Opportunity Discovery)
     ```
     *Fix:* Change to: `<strong>StartupLens</strong> — AI-Powered Idea Validation & Opportunity Discovery`
  3. **Frontend Sample Idea Tag:** [`frontend/src/App.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/App.jsx) (Line 22):
     ```javascript
     highlight: "Featured in Track 5 Brief"
     ```
     *Fix:* Change to: `highlight: "High Impact & Feasibility"`
  4. **Backend Sample Ideas Route:** [`backend/app/main.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/main.py) (Line 78):
     ```python
     "highlight": "Featured in Track 5 Brief"
     ```
     *Fix:* Change to: `"highlight": "High Impact & Feasibility"`
  5. **Orphaned Pitch Modal:** [`frontend/src/components/PitchModal.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/components/PitchModal.jsx) (Line 60):
     Contains `StartupLens — SerpApi Hackathon 2026` modal content.

---

## 3. UI / UX and Interaction Issues

### 🟡 Issue 3.1: Flawed Idea Selection Highlight & Card State
- **Severity:** Medium / High User Impact
- **Files:** [`frontend/src/components/IdeaForm.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/components/IdeaForm.jsx), [`frontend/src/App.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/App.jsx)
- **Root Cause:**
  1. **Barely Visible Highlight:** The active style uses `rgba(99, 102, 241, 0.08)` (only 8% opacity background) and `rgba(99, 102, 241, 0.35)` border, which on dark monitors is almost indistinguishable from unselected cards (`rgba(255, 255, 255, 0.03)`).
  2. **JavaScript Inline Style Overrides:** The card uses `onMouseEnter` and `onMouseLeave` inline handlers to set `style.borderColor`. On mouse leave, it overwrites the border dynamically, resulting in flickering or loss of active styles.
  3. **State Desynchronization:** If a user clicks an idea card and subsequently edits or erases the text inside the textarea, `selectedIdeaId` remains locked to the previously clicked card.
- **Recommended Fix:**
  - Create dedicated CSS classes `.idea-card` and `.idea-card.selected` in `index.css`:
    ```css
    .idea-card.selected {
      background: rgba(99, 102, 241, 0.18) !important;
      border: 1.5px solid var(--accent-primary-light) !important;
      box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
    }
    ```
  - Add a visible active badge or checkmark icon on the active card.
  - In `IdeaForm`, when the user manually modifies the `textarea` (`onChange`), clear `selectedIdeaId` if the input diverges from the sample description.

---

### 🟡 Issue 3.2: Orphaned Dead Code & Modals (`PitchModal`, `SettingsModal`)
- **Severity:** Medium
- **Files:** [`frontend/src/App.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/App.jsx), [`frontend/src/components/Navbar.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/components/Navbar.jsx)
- **Root Cause:**
  In previous cleanups, the "API Keys" and "Judge Pitch" buttons were removed from `Navbar.jsx`. However, `SettingsModal` and `PitchModal` are still imported and rendered in `App.jsx`, maintaining unused React state hooks (`isSettingsOpen`, `isPitchOpen`).
  - `PitchModal` is completely unreachable.
  - `SettingsModal` is unreachable, meaning **users have no UI method to enter their own SerpApi key** if the deployed server lacks an environment variable or runs out of credits.
- **Recommended Fix:**
  - Either remove `PitchModal` completely to clean up dead bundle code, or move the Settings (API Key) button to an unobtrusive gear icon in `Navbar` so power users can supply their own SerpApi key when needed.

---

### 🟡 Issue 3.3: Inaccurate Hardcoded Data in Markdown Export
- **Severity:** Medium
- **Files:** [`frontend/src/components/GapsAndRoadmap.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/components/GapsAndRoadmap.jsx) (Lines 45–48)
- **Root Cause:**
  When generating the downloadable Markdown report (`handleExportMarkdown`), the Competitor Capability Matrix table is constructed with hardcoded text:
  ```javascript
  ${reportData.competitor_matrix?.map((r) => `| ${r.feature_name} | ${r.importance} | Lacking / Flawed | Native (✓) | ${r.opportunity_reason} |`).join('\n')}
  ```
  It hardcodes `Lacking / Flawed` for incumbents and `Native (✓)` for the user's idea, regardless of what the real rating actually was in `reportData.competitor_matrix`.
- **Recommended Fix:**
  Format the actual `r.competitor_ratings` values (e.g., showing each competitor's real rating) and `r.user_idea_rating` dynamically in the exported table.

---

### 🟡 Issue 3.4: Misleading Local Development Error Message Shown in Production
- **Severity:** Low / Medium
- **Files:** [`frontend/src/App.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/App.jsx) (Line 116)
- **Root Cause:**
  If an API call fails or times out, the user is presented with:
  > *"Unable to connect to the backend. If running locally, ensure the backend is running and VITE_API_URL is set correctly."*
  On the deployed Vercel site, this confuses end users because they are not running it locally.
- **Recommended Fix:**
  Update the error message to distinguish between network/timeout issues and local development:
  > *"Unable to complete analysis. The intelligence server may be experiencing high demand or external search rate limits. Please try again in a few moments."*

---

### 🟡 Issue 3.5: Mobile Responsiveness & Table Overflow
- **Severity:** Low / Medium
- **Files:** [`frontend/src/components/OpportunityMatrix.jsx`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/components/OpportunityMatrix.jsx), [`frontend/src/index.css`](file:///e:/Projects/StartupLens/StartupLens/frontend/src/index.css)
- **Root Cause:**
  The `OpportunityMatrix` table contains 5+ columns (Feature, Incumbent 1, Incumbent 2, Incumbent 3, Target Wedge). On screens narrower than 768px, horizontal scrolling is required. Because the first column ("Feature") is not sticky, users lose track of feature names while scrolling horizontally.
- **Recommended Fix:**
  Add `position: sticky; left: 0; background: var(--bg-card); z-index: 2;` to the first column on mobile viewports, or provide a card-based accordion view for screens < 640px.

---

## 4. Security & Configuration Issues

### 🔴 Issue 4.1: Plaintext API Key History in Git
- **Severity:** High (Security)
- **Files:** Git commit history (specifically commits modifying [`backend/.env.example`](file:///e:/Projects/StartupLens/StartupLens/backend/.env.example))
- **Root Cause:**
  In earlier commits, an active SerpApi key (`b4a8a62388...`) was committed into `backend/.env.example` before being replaced by a placeholder in commit `19e67c5`. Anyone with read access to the GitHub repository can view past commits.
- **Recommended Fix:**
  1. **Immediately regenerate/revoke the SerpApi key** at [serpapi.com/manage-api-key](https://serpapi.com/manage-api-key).
  2. Add the newly generated key strictly in **Vercel Project Settings → Environment Variables**.

---

### 🟡 Issue 4.2: Open CORS Policy (`allow_origins=["*"]`)
- **Severity:** Low / Medium
- **Files:** [`backend/app/main.py`](file:///e:/Projects/StartupLens/StartupLens/backend/app/main.py) (Lines 19–25)
- **Root Cause:**
  CORS is configured to allow all origins (`allow_origins=["*"]`). Because the backend consumes paid SerpApi requests, third-party sites could invoke your deployed `/api/analyze` endpoint and consume your quota.
- **Recommended Fix:**
  Restrict allowed origins to the production domain and local development:
  ```python
  allow_origins=[
      "https://startuplens-zeta.vercel.app",
      "https://startuplens-frontend.vercel.app",
      "http://localhost:5173",
      "http://127.0.0.1:5173"
  ]
  ```

---

## 5. Summary Priority Action List

| Priority | Issue | Action Required |
|:---:|:---|:---|
| 1 | **Revoke & Regenerate SerpApi Key** | Rotate key at SerpApi dashboard; set only in Vercel Environment Variables. |
| 2 | **Reduce SerpApi Query Count / Latency** | Streamline queries in `QueryPlanner` to prevent Vercel 10s-15s serverless timeouts. |
| 3 | **Fix Idea Selection Highlight** | Introduce distinct `.selected` styling and active indicator; unhighlight on user typing. |
| 4 | **Clean Residual Track 5 / Hackathon Text** | Update `index.html` title, footer text in `App.jsx`, and sample idea tags in `App.jsx` & `main.py`. |
| 5 | **Fix Markdown Export in GapsAndRoadmap** | Ensure export reflects real matrix ratings instead of hardcoded strings. |
| 6 | **Remove or Reconnect Orphaned Modals** | Either remove `PitchModal` or add a subtle settings button for user API keys. |
| 7 | **Production-Ready Error Message** | Replace the "running locally" error message with a user-friendly error description. |
| 8 | **Lock Down CORS** | Whitelist only Vercel domains and local dev. |
