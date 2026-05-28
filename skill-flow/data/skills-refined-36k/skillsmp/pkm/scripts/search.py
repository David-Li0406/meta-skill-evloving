#!/usr/bin/env python3
"""
PKM Search Engine
Searches the index with fuzzy matching, Korean/English translation, and scoring.
"""

import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def fuzzy_score(query: str, text: str, threshold: float = 0.6) -> float:
    """
    Calculate fuzzy match score between query and text.
    Returns 0-1 score, 0 if below threshold.
    """
    query = query.lower()
    text = text.lower()

    # Exact match
    if query in text:
        return 1.0

    # Check if query is in any word
    words = text.split()
    for word in words:
        if query in word:
            return 0.9

        # Calculate similarity ratio
        max_len = max(len(query), len(word))
        if max_len == 0:
            continue

        distance = levenshtein_distance(query, word)
        similarity = 1 - (distance / max_len)

        if similarity >= threshold:
            return similarity

    return 0.0


def expand_query(query: str, term_index: dict) -> List[str]:
    """Expand query with Korean/English translations."""
    queries = [query.lower()]
    query_lower = query.lower()

    # Check if query matches a term mapping
    for en, ko in term_index.items():
        if query_lower == en.lower():
            queries.append(ko.lower())
        elif query_lower == ko.lower():
            queries.append(en.lower())
        # Partial match
        elif en.lower() in query_lower:
            queries.append(query_lower.replace(en.lower(), ko.lower()))
        elif ko.lower() in query_lower:
            queries.append(query_lower.replace(ko.lower(), en.lower()))

    return list(set(queries))


def calculate_score(entry: dict, query: str, expanded_queries: List[str]) -> float:
    """
    Calculate relevance score for an entry.

    Scoring weights:
    - Exact repo name match: +100
    - Alias match: +80
    - Exact tag match: +60
    - Partial tag match: +40
    - Summary contains query: +30
    - Fuzzy match score: +25 * score
    """
    score = 0.0
    query_lower = query.lower()

    # Check all expanded queries
    for q in expanded_queries:
        q_lower = q.lower()

        # Repo name (id field)
        repo_name = entry.get('id', '').lower().replace('__', '/')
        if q_lower in repo_name:
            if q_lower == repo_name.split('/')[-1]:  # Exact repo name
                score += 100
            else:
                score += 70

        # Aliases
        for alias in entry.get('aliases', []):
            if q_lower == alias.lower():
                score += 80
            elif q_lower in alias.lower():
                score += 50

        # Tags (both original and normalized)
        for tag in entry.get('tags', []) + entry.get('tags_normalized', []):
            tag_lower = tag.lower()
            if q_lower == tag_lower:
                score += 60
            elif q_lower in tag_lower or tag_lower in q_lower:
                score += 40

        # Summary
        summary = entry.get('summary', '').lower()
        if q_lower in summary:
            score += 30

        # Language
        if q_lower == entry.get('language', '').lower():
            score += 50

    # Fuzzy matching on searchable text
    fuzzy = fuzzy_score(query_lower, entry.get('searchable_text', ''))
    if fuzzy > 0:
        score += 25 * fuzzy

    return score


def search(
    query: str,
    index: dict,
    language: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 10
) -> List[Dict]:
    """
    Search the index with the given query and filters.

    Args:
        query: Search query string
        index: The loaded search index
        language: Optional language filter (e.g., "Python")
        tags: Optional tag filters
        limit: Maximum number of results to return

    Returns:
        List of matching entries with scores
    """
    entries = index.get('entries', [])
    term_index = index.get('term_index', {})

    # Expand query with translations
    expanded_queries = expand_query(query, term_index)

    results = []

    for entry in entries:
        # Apply language filter
        if language:
            entry_lang = entry.get('language', '').lower()
            if language.lower() not in entry_lang and entry_lang not in language.lower():
                continue

        # Apply tag filter
        if tags:
            entry_tags = set(t.lower() for t in entry.get('tags', []) + entry.get('tags_normalized', []))
            if not any(t.lower() in entry_tags or any(t.lower() in et for et in entry_tags) for t in tags):
                continue

        # Calculate score
        score = calculate_score(entry, query, expanded_queries)

        if score > 0:
            results.append({
                **entry,
                'score': round(score, 2)
            })

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)

    return results[:limit]


def format_results(results: List[Dict], query: str) -> str:
    """Format search results for display."""
    if not results:
        return f'No results found for "{query}"'

    output = [f'## PKM Search Results: "{query}"\n']
    output.append(f'{len(results)} repositories found:\n')

    for i, entry in enumerate(results, 1):
        output.append(f'### {i}. {entry["id"].replace("__", "/")}')
        output.append(f'**Language**: {entry.get("language", "N/A")} | **Score**: {entry["score"]}/100')

        tags = entry.get('tags', [])
        if tags:
            output.append(f'**Tags**: {", ".join(tags[:5])}')

        if entry.get('url'):
            output.append(f'**URL**: {entry["url"]}')

        if entry.get('summary'):
            # Truncate long summaries
            summary = entry['summary']
            if len(summary) > 200:
                summary = summary[:200] + '...'
            output.append(f'\n> {summary}')

        output.append('')

    return '\n'.join(output)


def load_index(base_path: Path = None) -> dict:
    """Load the search index, building if necessary."""
    if base_path is None:
        base_path = Path(__file__).parent.parent

    index_path = base_path / 'data' / 'index.json'

    # Try to build index if it doesn't exist
    if not index_path.exists():
        print("Index not found. Building...")
        from build_index import build_index
        return build_index(base_path)

    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='Search PKM index')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--language', '-l', help='Filter by language (e.g., Python)')
    parser.add_argument('--tags', '-t', help='Filter by tags (comma-separated)')
    parser.add_argument('--limit', '-n', type=int, default=10, help='Maximum results (default: 10)')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Load index
    index = load_index()

    # Parse tags
    tags = None
    if args.tags:
        tags = [t.strip() for t in args.tags.split(',')]

    # Search
    results = search(
        query=args.query,
        index=index,
        language=args.language,
        tags=tags,
        limit=args.limit
    )

    # Output
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_results(results, args.query))


if __name__ == '__main__':
    main()
