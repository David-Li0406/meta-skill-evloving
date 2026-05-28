#!/usr/bin/env python3
"""
Amazon KDP Keyword Analyzer
Analyze and optimize backend keywords for maximum discoverability.

Usage:
    python keyword_analyzer.py --analyze "your keywords here"
"""

import argparse
import re
from collections import Counter

# Words Amazon ignores (don't waste character space on these)
STOP_WORDS = {
    'a', 'an', 'and', 'the', 'of', 'to', 'for', 'in', 'on', 'with',
    'book', 'ebook', 'kindle', 'paperback', 'hardcover', 'amazon',
    'best', 'new', 'free', 'buy', 'read', 'edition'
}

# Characters to avoid
FORBIDDEN_CHARS = {'"', "'", ',', '.', '!', '?', ';', ':', '-', '&'}

def analyze_keywords(keywords: str) -> dict:
    """Analyze keyword string for optimization opportunities."""
    
    results = {
        "total_chars": len(keywords),
        "max_chars": 350,
        "remaining_chars": 350 - len(keywords),
        "word_count": 0,
        "issues": [],
        "warnings": [],
        "suggestions": []
    }
    
    # Split into words
    words = keywords.lower().split()
    results["word_count"] = len(words)
    
    # Check for stop words
    found_stop_words = [w for w in words if w in STOP_WORDS]
    if found_stop_words:
        results["warnings"].append(
            f"Stop words found (Amazon ignores these): {', '.join(set(found_stop_words))}"
        )
    
    # Check for forbidden characters
    found_forbidden = [c for c in keywords if c in FORBIDDEN_CHARS]
    if found_forbidden:
        results["issues"].append(
            f"Forbidden characters found: {', '.join(set(found_forbidden))}"
        )
    
    # Check for repeated words
    word_counts = Counter(words)
    repeated = {w: c for w, c in word_counts.items() if c > 1 and w not in STOP_WORDS}
    if repeated:
        results["warnings"].append(
            f"Repeated words (wasting space): {repeated}"
        )
    
    # Check character usage
    if results["remaining_chars"] > 50:
        results["suggestions"].append(
            f"You have {results['remaining_chars']} unused characters. Add more keywords!"
        )
    elif results["remaining_chars"] < 0:
        results["issues"].append(
            f"Over limit by {abs(results['remaining_chars'])} characters. Trim keywords."
        )
    
    # Check for common mistakes
    if 'book' in words or 'ebook' in words:
        results["warnings"].append(
            "Remove 'book' and 'ebook' - Amazon adds these automatically."
        )
    
    return results

def suggest_keywords(topic: str, audience: str) -> list:
    """Generate keyword suggestions based on topic and audience."""
    
    suggestions = []
    
    # Topic variations
    suggestions.append(f"{topic} guide")
    suggestions.append(f"{topic} handbook")
    suggestions.append(f"{topic} for beginners")
    suggestions.append(f"{topic} masterclass")
    suggestions.append(f"how to {topic}")
    suggestions.append(f"learn {topic}")
    
    # Audience variations
    suggestions.append(f"{topic} for {audience}")
    suggestions.append(f"{audience} {topic}")
    suggestions.append(f"{topic} tips {audience}")
    
    return suggestions

def format_for_kdp(keywords: list) -> str:
    """Format keyword list for KDP backend entry."""
    
    # Clean and deduplicate
    cleaned = []
    seen = set()
    
    for kw in keywords:
        # Lowercase and remove forbidden chars
        clean = kw.lower()
        for char in FORBIDDEN_CHARS:
            clean = clean.replace(char, ' ')
        clean = ' '.join(clean.split())  # Normalize whitespace
        
        if clean and clean not in seen:
            cleaned.append(clean)
            seen.update(clean.split())
    
    # Join with spaces
    result = ' '.join(cleaned)
    
    # Truncate to 350 chars
    if len(result) > 350:
        result = result[:350].rsplit(' ', 1)[0]
    
    return result

def main():
    parser = argparse.ArgumentParser(description='KDP Keyword Analyzer')
    parser.add_argument('--analyze', help='Analyze keyword string')
    parser.add_argument('--suggest', nargs=2, metavar=('TOPIC', 'AUDIENCE'),
                       help='Generate keyword suggestions')
    parser.add_argument('--format', nargs='+', help='Format keywords for KDP')
    
    args = parser.parse_args()
    
    if args.analyze:
        results = analyze_keywords(args.analyze)
        
        print("\n📊 KEYWORD ANALYSIS REPORT")
        print("=" * 50)
        print(f"Characters: {results['total_chars']}/{results['max_chars']}")
        print(f"Remaining: {results['remaining_chars']}")
        print(f"Word Count: {results['word_count']}")
        
        if results["issues"]:
            print("\n❌ ISSUES (Fix These):")
            for issue in results["issues"]:
                print(f"  • {issue}")
        
        if results["warnings"]:
            print("\n⚠️ WARNINGS:")
            for warning in results["warnings"]:
                print(f"  • {warning}")
        
        if results["suggestions"]:
            print("\n💡 SUGGESTIONS:")
            for suggestion in results["suggestions"]:
                print(f"  • {suggestion}")
        
        if not results["issues"] and not results["warnings"]:
            print("\n✅ Keywords look good!")
    
    elif args.suggest:
        topic, audience = args.suggest
        suggestions = suggest_keywords(topic, audience)
        
        print(f"\n💡 KEYWORD SUGGESTIONS for '{topic}' + '{audience}':")
        print("=" * 50)
        for s in suggestions:
            print(f"  • {s}")
    
    elif args.format:
        formatted = format_for_kdp(args.format)
        
        print("\n📋 FORMATTED FOR KDP:")
        print("=" * 50)
        print(formatted)
        print(f"\n({len(formatted)}/350 characters)")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
