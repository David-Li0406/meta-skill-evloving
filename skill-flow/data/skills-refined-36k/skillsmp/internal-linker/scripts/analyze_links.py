#!/usr/bin/env python3
"""
Internal Link Analyzer
Analysiert Artikel und schlägt interne Verlinkungen vor.
"""

import json
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from collections import Counter

@dataclass
class Article:
    id: str
    title: str
    slug: str
    content: str
    keywords: List[str]

@dataclass
class LinkSuggestion:
    target_id: str
    target_url: str
    target_title: str
    anchor_text: str
    context: str
    relevance_score: float
    reason: str

class InternalLinkAnalyzer:
    """Analysiert Artikel und findet Link-Möglichkeiten."""

    def __init__(self, articles: List[Article]):
        self.articles = articles
        self.article_index = {a.id: a for a in articles}

    def analyze_article(self, article: Article, max_links: int = 5) -> List[LinkSuggestion]:
        """
        Analysiert einen Artikel und schlägt interne Links vor.

        Args:
            article: Der zu analysierende Artikel
            max_links: Maximale Anzahl vorgeschlagener Links

        Returns:
            Liste von LinkSuggestions
        """
        suggestions = []

        for other in self.articles:
            if other.id == article.id:
                continue

            score = self._calculate_relevance(article, other)

            if score >= 0.4:  # Minimum relevance threshold
                anchor_options = self._generate_anchors(other)
                contexts = self._find_link_contexts(article.content, other.keywords)

                if contexts:
                    suggestions.append(LinkSuggestion(
                        target_id=other.id,
                        target_url=f"/{other.slug}",
                        target_title=other.title,
                        anchor_text=anchor_options[0] if anchor_options else other.title,
                        context=contexts[0],
                        relevance_score=score,
                        reason=self._generate_reason(article, other, score)
                    ))

        # Sort by relevance and return top N
        suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
        return suggestions[:max_links]

    def _calculate_relevance(self, article_a: Article, article_b: Article) -> float:
        """Berechnet Relevanz-Score zwischen zwei Artikeln."""

        # Keyword Overlap (40% weight)
        keywords_a = set(k.lower() for k in article_a.keywords)
        keywords_b = set(k.lower() for k in article_b.keywords)

        if not keywords_a or not keywords_b:
            keyword_score = 0
        else:
            overlap = len(keywords_a & keywords_b)
            keyword_score = overlap / len(keywords_a | keywords_b)

        # Title Similarity (30% weight)
        title_words_a = set(article_a.title.lower().split())
        title_words_b = set(article_b.title.lower().split())

        # Remove common words
        stopwords = {'der', 'die', 'das', 'und', 'oder', 'für', 'mit', 'zu', 'in', 'ein', 'eine'}
        title_words_a -= stopwords
        title_words_b -= stopwords

        if not title_words_a or not title_words_b:
            title_score = 0
        else:
            title_overlap = len(title_words_a & title_words_b)
            title_score = title_overlap / len(title_words_a | title_words_b)

        # Content Keyword Presence (30% weight)
        content_lower = article_a.content.lower()
        keyword_presence = sum(1 for k in article_b.keywords if k.lower() in content_lower)
        content_score = min(keyword_presence / max(len(article_b.keywords), 1), 1.0)

        # Weighted combination
        return (keyword_score * 0.4) + (title_score * 0.3) + (content_score * 0.3)

    def _generate_anchors(self, target: Article) -> List[str]:
        """Generiert Anchor-Text-Optionen für Ziel-Artikel."""
        anchors = []

        # Option 1: Kürzerer Titel
        if len(target.title) > 40:
            # Versuche kürzere Version
            short_title = target.title.split(':')[0].strip()
            if len(short_title) < len(target.title):
                anchors.append(short_title)

        anchors.append(target.title)

        # Option 2: Keywords
        for keyword in target.keywords[:3]:
            if len(keyword) > 3:
                anchors.append(keyword)

        return anchors

    def _find_link_contexts(self, content: str, keywords: List[str]) -> List[str]:
        """Findet passende Stellen im Content für Links."""
        contexts = []

        sentences = re.split(r'[.!?]', content)

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue

            # Check if sentence contains any target keyword
            sentence_lower = sentence.lower()
            for keyword in keywords:
                if keyword.lower() in sentence_lower:
                    # Extract context (sentence with some surrounding)
                    context = f"...{sentence}..."
                    if len(context) > 200:
                        context = context[:200] + "..."
                    contexts.append(context)
                    break

        return contexts[:3]  # Max 3 contexts

    def _generate_reason(self, article_a: Article, article_b: Article, score: float) -> str:
        """Generiert Begründung für Link-Vorschlag."""

        keywords_a = set(k.lower() for k in article_a.keywords)
        keywords_b = set(k.lower() for k in article_b.keywords)
        common = keywords_a & keywords_b

        if common:
            return f"Gemeinsame Keywords: {', '.join(list(common)[:3])}"

        return f"Thematische Ähnlichkeit (Score: {score:.2f})"

    def find_orphan_pages(self, internal_links: Dict[str, List[str]]) -> List[Article]:
        """Findet Seiten ohne eingehende Links."""

        linked_to = set()
        for links in internal_links.values():
            linked_to.update(links)

        orphans = [a for a in self.articles if a.id not in linked_to]
        return orphans

    def get_link_distribution(self, internal_links: Dict[str, List[str]]) -> Dict:
        """Analysiert Link-Verteilung."""

        # Incoming links per page
        incoming = Counter()
        for source, targets in internal_links.items():
            for target in targets:
                incoming[target] += 1

        # Outgoing links per page
        outgoing = {page_id: len(links) for page_id, links in internal_links.items()}

        return {
            "incoming": dict(incoming),
            "outgoing": outgoing,
            "orphan_count": len([a for a in self.articles if incoming[a.id] == 0]),
            "avg_incoming": sum(incoming.values()) / max(len(self.articles), 1),
            "avg_outgoing": sum(outgoing.values()) / max(len(outgoing), 1)
        }


def main():
    """Beispiel-Verwendung."""

    # Beispiel-Artikel
    articles = [
        Article(
            id="1",
            title="Content Marketing Strategie: Der ultimative Guide",
            slug="content-marketing-strategie",
            content="Content Marketing ist eine der effektivsten Methoden...",
            keywords=["content marketing", "strategie", "marketing"]
        ),
        Article(
            id="2",
            title="SEO Grundlagen für Anfänger",
            slug="seo-grundlagen",
            content="SEO steht für Search Engine Optimization...",
            keywords=["seo", "grundlagen", "suchmaschinen"]
        ),
        Article(
            id="3",
            title="Content Marketing und SEO verbinden",
            slug="content-marketing-seo",
            content="Content Marketing und SEO gehören zusammen...",
            keywords=["content marketing", "seo", "strategie"]
        )
    ]

    analyzer = InternalLinkAnalyzer(articles)

    # Analysiere Artikel 1
    suggestions = analyzer.analyze_article(articles[0])

    print("Link-Vorschläge für:", articles[0].title)
    print("-" * 50)

    for s in suggestions:
        print(f"\nZiel: {s.target_title}")
        print(f"URL: {s.target_url}")
        print(f"Anchor: {s.anchor_text}")
        print(f"Score: {s.relevance_score:.2f}")
        print(f"Grund: {s.reason}")
        print(f"Kontext: {s.context}")


if __name__ == "__main__":
    main()
