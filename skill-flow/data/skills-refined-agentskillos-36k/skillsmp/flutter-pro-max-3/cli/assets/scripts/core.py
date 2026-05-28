#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter Pro Max Core - BM25 search engine for Flutter knowledge base
Zero dependencies - self-contained BM25 implementation
"""

import csv
import re
from pathlib import Path
from math import log
from collections import defaultdict
from typing import Any

# ============ CONFIGURATION ============
def _get_data_dir() -> Path:
    """Auto-detect data directory based on script location"""
    script_dir = Path(__file__).parent
    possible_paths = [
        # Full install: .claude/skills/flutter-pro-max/scripts/ -> data/ (sibling)
        script_dir.parent / "data",
        # Reference install: .shared/flutter-pro-max/scripts/ -> ../data
        script_dir.parent.parent / "data",
        # When running from root/scripts/
        script_dir.parent / ".shared" / "data",
        # When running from .agent/workflows/scripts/ (nested 3 levels deep)
        script_dir.parent.parent.parent / ".shared" / "data",
        # When running from .claude/skills/flutter-pro-max/scripts/ (reference mode)
        script_dir.parent.parent.parent.parent / ".shared" / "data",
        # Fallback: cwd
        Path.cwd() / ".shared" / "data",
    ]
    for p in possible_paths:
        if p.exists():
            return p.resolve()
    return possible_paths[0]  # Default to first option

DATA_DIR = _get_data_dir()
MAX_RESULTS = 5

# Domain configuration: file, search columns, output columns
CSV_CONFIG: dict[str, dict[str, str | list[str]]] = {
    "widget": {
        "file": "widget.csv",
        "search_cols": ["Widget Name", "Category", "Description", "Key Properties", "Usage Context & Pro-Tips"],
        "output_cols": ["Widget Name", "Category", "Description", "Key Properties", "Usage Context & Pro-Tips"]
    },
    "package": {
        "file": "package.csv",
        "search_cols": ["pkg_name", "category", "description", "best_practice_snippet", "pro_tip", "alternatives"],
        "output_cols": ["pkg_name", "category", "description", "best_practice_snippet", "pro_tip", "alternatives"]
    },
    "pattern": {
        "file": "patterns.csv",
        "search_cols": ["pattern_name", "category", "problem_tags", "description", "key_widgets", "code_snippet", "anti_pattern"],
        "output_cols": ["pattern_name", "category", "problem_tags", "description", "key_widgets", "code_snippet", "anti_pattern"]
    },
    "architect": {
        "file": "architect.csv",
        "search_cols": ["path_pattern", "layer", "responsibility_description", "allowed_dependencies", "tech_stack_note"],
        "output_cols": ["path_pattern", "layer", "responsibility_description", "allowed_dependencies", "tech_stack_note"]
    },
    "chart": {
        "file": "charts.csv",
        "search_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "Accessibility Notes"],
        "output_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "Color Guidance", "Accessibility Notes", "Library Recommendation"]
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Product Type", "Keywords", "Notes"],
        "output_cols": ["Product Type", "Keywords", "Primary (Hex)", "Secondary (Hex)", "CTA (Hex)", "Notes"]
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"],
        "output_cols": ["Font Pairing Name", "Category", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "Notes"]
    },
    "style": {
        "file": "styles.csv",
        "search_cols": ["Style Category", "Type", "Keywords", "Best For"],
        "output_cols": ["Style Category", "Type", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Do Not Use For"]
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't"]
    },
    "icon": {
        "file": "icons.csv",
        "search_cols": ["Category", "Icon Name", "Keywords", "Best For"],
        "output_cols": ["Category", "Icon Name", "Keywords", "Library", "Import Code", "Usage", "Best For"]
    },
    "landing": {
        "file": "landing.csv",
        "search_cols": ["Pattern Name", "Keywords", "Section Order", "Conversion Optimization"],
        "output_cols": ["Pattern Name", "Keywords", "Section Order", "Primary CTA Placement", "Color Strategy", "Conversion Optimization"]
    },
    "naming": {
        "file": "name_convention.csv",
        "search_cols": ["Layer", "File Template", "Class Template", "Example File", "Example Class", "Notes"],
        "output_cols": ["Layer", "File Template", "Class Template", "Example File", "Example Class", "Notes"]
    },
    "product": {
        "file": "products.csv",
        "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation"],
        "output_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles", "Color Palette Focus"]
    },
    "prompt": {
        "file": "prompts.csv",
        "search_cols": ["Style Category", "AI Prompt Keywords (Copy-Paste Ready)", "CSS/Technical Keywords"],
        "output_cols": ["Style Category", "AI Prompt Keywords (Copy-Paste Ready)", "CSS/Technical Keywords", "Implementation Checklist"]
    },
    "performance": {
        "file": "flutter-performance.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Issue", "Keywords", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "ui-reasoning": {
        "file": "ui-reasoning.csv",
        "search_cols": ["App_Category", "Recommended_Pattern", "Style_Priority", "Color_Mood", "Key_Effects", "Decision_Rules"],
        "output_cols": ["App_Category", "Recommended_Pattern", "Style_Priority", "Color_Mood", "Typography_Mood", "Key_Effects", "Decision_Rules", "Anti_Patterns", "Severity"]
    },
    "accessibility": {
        "file": "mobile-accessibility.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Platform", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Issue", "Keywords", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    }
}

# Stack exclusion mapping for filtering conflicting packages
STACK_EXCLUSIONS = {
    "riverpod": ["bloc", "flutter_bloc", "provider", "hydrated_bloc"],
    "bloc": ["riverpod", "flutter_riverpod", "provider"],
    "provider": ["riverpod", "flutter_riverpod", "bloc", "flutter_bloc"],
}

AVAILABLE_DOMAINS = list(CSV_CONFIG.keys())
AVAILABLE_STACKS = list(STACK_EXCLUSIONS.keys())


# ============ BM25 IMPLEMENTATION ============
class BM25:
    """BM25 ranking algorithm for text search - zero dependencies"""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.corpus: list[list[str]] = []
        self.doc_lengths: list[int] = []
        self.avgdl: float = 0
        self.idf: dict[str, float] = {}
        self.doc_freqs: defaultdict[str, int] = defaultdict(int)
        self.n: int = 0

    def tokenize(self, text: str) -> list[str]:
        """Lowercase, split, remove punctuation, filter short words"""
        text = re.sub(r'[^\w\s]', ' ', str(text).lower())
        return [w for w in text.split() if len(w) > 1]

    def fit(self, documents: list[str]) -> None:
        """Build BM25 index from documents"""
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.n = len(self.corpus)
        if self.n == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.n

        for doc in self.corpus:
            seen: set[str] = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)

        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.n - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query: str) -> list[tuple[int, float]]:
        """Score all documents against query"""
        query_tokens = self.tokenize(query)
        scores: list[tuple[int, float]] = []

        for idx, doc in enumerate(self.corpus):
            score: float = 0.0
            doc_len = self.doc_lengths[idx]
            term_freqs: defaultdict[str, int] = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1

            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    score += idf * numerator / denominator

            scores.append((idx, score))

        return sorted(scores, key=lambda x: x[1], reverse=True)


# ============ HELPER FUNCTIONS ============
def _load_csv(filepath: Path) -> list[dict[str, str]]:
    """Load CSV and return list of dicts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _search_csv(filepath: Path, search_cols: list[str], output_cols: list[str], query: str, max_results: int, boost_col: str | None = None, boost_query: str | None = None) -> list[dict[str, Any]]:
    """Core search function using BM25 with optional boosting"""
    if not filepath.exists():
        return []

    data = _load_csv(filepath)

    # Build documents from search columns
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in data]

    # BM25 search
    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)

    # Apply boosting if specified (widget name match, etc.)
    if boost_col and boost_query:
        boost_query_lower = boost_query.lower()
        boosted: list[tuple[int, float]] = []
        for idx, score in ranked:
            boosted_score = score
            if score > 0:
                boost_value = str(data[idx].get(boost_col, "")).lower()
                if boost_value in boost_query_lower or boost_query_lower in boost_value:
                    boosted_score = score * 2.0  # Double score for exact/partial match
            boosted.append((idx, boosted_score))
        ranked = sorted(boosted, key=lambda x: x[1], reverse=True)

    # Get top results with score > 0
    results: list[dict[str, Any]] = []
    for idx, score in ranked[:max_results]:
        if score > 0:
            row = data[idx]
            result: dict[str, Any] = {col: row.get(col, "") for col in output_cols if col in row}
            result["_score"] = round(score, 4)
            results.append(result)

    return results


def detect_domain(query: str) -> str:
    """Auto-detect the most relevant domain from query keywords"""
    query_lower = query.lower()

    domain_keywords = {
        "widget": ["widget", "listview", "column", "row", "container", "text", "button", "scaffold", "appbar", "sliver"],
        "package": ["package", "pub", "dependency", "library", "dio", "http", "riverpod", "bloc", "hive", "isar"],
        "pattern": ["pattern", "architecture", "repository", "usecase", "state", "async", "error handling", "offline"],
        "architect": ["layer", "folder", "structure", "clean", "feature", "domain", "data", "presentation"],
        "chart": ["chart", "graph", "visualization", "bar", "pie", "line", "scatter", "heatmap"],
        "color": ["color", "palette", "hex", "theme", "dark mode", "light mode"],
        "typography": ["font", "typography", "heading", "text style", "google fonts"],
        "style": ["style", "design", "ui", "glassmorphism", "neumorphism", "minimal", "modern"],
        "ux": ["ux", "usability", "accessibility", "touch", "scroll", "animation", "gesture"],
        "icon": ["icon", "lucide", "material icons", "cupertino"],
        "landing": ["landing", "page", "hero", "cta", "section"],
        "naming": ["naming", "convention", "file name", "class name", "snake_case", "PascalCase"],
        "product": ["saas", "ecommerce", "fintech", "healthcare", "education", "food", "travel"],
        "prompt": ["prompt", "ai", "css", "tailwind", "implementation"],
    }

    scores: dict[str, int] = {domain: sum(1 for kw in keywords if kw in query_lower) for domain, keywords in domain_keywords.items()}
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "widget"


# ============ MAIN SEARCH FUNCTIONS ============
def search(query: str, domain: str | None = None, max_results: int = MAX_RESULTS) -> dict[str, Any]:
    """
    Main search function with auto-domain detection
    
    Args:
        query: Search query string
        domain: Optional domain (widget, package, pattern, etc.)
        max_results: Number of results to return
    
    Returns:
        Dict with domain, query, file, count, and results
    """
    if domain is None:
        domain = detect_domain(query)

    if domain not in CSV_CONFIG:
        return {"error": f"Unknown domain: {domain}. Available: {', '.join(AVAILABLE_DOMAINS)}"}

    config = CSV_CONFIG[domain]
    filepath = DATA_DIR / str(config["file"])

    if not filepath.exists():
        return {"error": f"File not found: {filepath}", "domain": domain}

    # Apply widget boosting for widget domain
    boost_col = "Widget Name" if domain == "widget" else None
    boost_query = query if domain == "widget" else None

    search_cols = config["search_cols"]
    output_cols = config["output_cols"]
    if isinstance(search_cols, list) and isinstance(output_cols, list):
        results = _search_csv(
            filepath, 
            search_cols, 
            output_cols, 
            query, 
            max_results,
            boost_col=boost_col,
            boost_query=boost_query
        )
    else:
        results = []

    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results
    }


def search_with_stack(query: str, stack: str, domain: str | None = None, max_results: int = MAX_RESULTS) -> dict[str, Any]:
    """
    Search with stack-specific filtering (excludes conflicting packages)
    
    Args:
        query: Search query string
        stack: Stack preference (riverpod, bloc, provider)
        domain: Optional domain filter
        max_results: Number of results to return
    
    Returns:
        Dict with filtered results
    """
    if stack not in STACK_EXCLUSIONS:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(AVAILABLE_STACKS)}"}

    result = search(query, domain, max_results * 2)  # Get more to filter

    if "error" in result:
        return result

    # Filter out conflicting packages
    excluded = STACK_EXCLUSIONS[stack]
    filtered_results: list[dict[str, Any]] = []
    
    for item in result["results"]:
        # Check package name field
        pkg_name = str(item.get("pkg_name", "")).lower()
        if pkg_name not in excluded:
            filtered_results.append(item)
        
        if len(filtered_results) >= max_results:
            break

    result["results"] = filtered_results
    result["count"] = len(filtered_results)
    result["stack"] = stack
    result["excluded"] = excluded

    return result
