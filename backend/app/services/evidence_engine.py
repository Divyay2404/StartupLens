from typing import List, Dict, Any
from app.models.schemas import SearchEvidenceItem

class EvidenceEngine:
    """
    Normalizes, deduplicates, and ranks raw search results across all SerpApi sources.
    Maintains a traceable index for AI reasoning citations.
    """

    @staticmethod
    def process_and_rank(raw_data: Dict[str, Any], query_terms: List[str]) -> Dict[str, Any]:
        normalized_items: List[SearchEvidenceItem] = []
        seen_links = set()

        # 1. Normalize Google Search items
        for item in raw_data.get("google", []):
            link = item.get("link", "").strip()
            if link and link in seen_links:
                continue
            if link:
                seen_links.add(link)
            normalized_items.append(SearchEvidenceItem(
                title=item.get("title", "Untitled Product"),
                link=link or "https://google.com",
                snippet=item.get("snippet", ""),
                source=item.get("source", "Web"),
                engine="google",
                extra={"type": "product_competitor"}
            ))

        # 2. Normalize Google News items
        for item in raw_data.get("google_news", []):
            link = item.get("link", "").strip()
            if link and link in seen_links:
                continue
            if link:
                seen_links.add(link)
            normalized_items.append(SearchEvidenceItem(
                title=item.get("title", "News Headline"),
                link=link or "https://news.google.com",
                snippet=item.get("snippet", ""),
                source=item.get("source", "Google News"),
                engine="google_news",
                extra={"date": item.get("date", "Recent")}
            ))

        # 3. Normalize Google Scholar items
        for item in raw_data.get("google_scholar", []):
            link = item.get("link", "").strip()
            if link and link in seen_links:
                continue
            if link:
                seen_links.add(link)
            normalized_items.append(SearchEvidenceItem(
                title=item.get("title", "Research Publication"),
                link=link or "https://scholar.google.com",
                snippet=item.get("snippet", ""),
                source=item.get("authors", "Scholar"),
                engine="google_scholar",
                extra={
                    "citations": item.get("citations", 0),
                    "year": item.get("year", "Recent")
                }
            ))

        # 4. Normalize Google Patents items
        for item in raw_data.get("google_patents", []):
            link = item.get("link", "").strip()
            if link and link in seen_links:
                continue
            if link:
                seen_links.add(link)
            normalized_items.append(SearchEvidenceItem(
                title=item.get("title", "Patent Publication"),
                link=link or "https://patents.google.com",
                snippet=item.get("snippet", ""),
                source=item.get("assignee", "Patent Office"),
                engine="google_patents",
                extra={
                    "patent_id": item.get("patent_id", ""),
                    "filing_date": item.get("filing_date", "")
                }
            ))

        # 5. Rank items based on keyword density & engine priority
        ranked_items = sorted(
            normalized_items,
            key=lambda x: EvidenceEngine._compute_relevance(x, query_terms),
            reverse=True
        )

        return {
            "evidence_items": ranked_items,
            "total_evidence_collected": len(ranked_items),
            "engine_counts": {
                "google": len(raw_data.get("google", [])),
                "google_news": len(raw_data.get("google_news", [])),
                "google_scholar": len(raw_data.get("google_scholar", [])),
                "google_patents": len(raw_data.get("google_patents", []))
            }
        }

    @staticmethod
    def _compute_relevance(item: SearchEvidenceItem, query_terms: List[str]) -> float:
        score = 1.0
        text = f"{item.title} {item.snippet}".lower()
        for term in query_terms:
            t = term.lower()
            if t in item.title.lower():
                score += 3.0
            if t in text:
                score += 1.5

        # Boost academic papers with high citations
        if item.engine == "google_scholar":
            citations = item.extra.get("citations", 0)
            score += min(citations * 0.05, 3.0)

        # Boost fresh news
        if item.engine == "google_news":
            score += 1.0

        return score
