#!/usr/bin/env python3
"""
Finnish Translation Validator for Topic Names

Validates Finnish topic translations using Voikko or UralicNLP.
Outputs topics that need review.

Usage:
    python validate_finnish.py                    # Check all unchecked topics
    python validate_finnish.py --all              # Check all topics with Finnish
    python validate_finnish.py --csv input.csv   # Validate CSV file
    python validate_finnish.py --word "sana"     # Test single word

Requirements (install one):
    pip install libvoikko   # Faster, needs libvoikko system library
    pip install uralicnlp   # Pure Python, downloads models automatically

On macOS: brew install libvoikko
On Ubuntu: apt install libvoikko-dev voikko-fi
"""

import argparse
import csv
import json
import sys
from typing import Optional

# Try to import validation libraries
voikko = None
uralicApi = None

try:
    import libvoikko
    voikko = libvoikko.Voikko("fi")
except ImportError:
    pass
except Exception as e:
    print(f"Warning: libvoikko available but failed to initialize: {e}", file=sys.stderr)

if voikko is None:
    try:
        from uralicnlp import uralicApi as _uralicApi
        uralicApi = _uralicApi
    except ImportError:
        pass


def check_word(word: str) -> dict:
    """
    Check if a Finnish word is valid.
    Returns dict with 'valid', 'suggestions', 'analysis'.
    """
    word = word.strip()
    result = {
        "word": word,
        "valid": None,
        "suggestions": [],
        "analysis": [],
        "tool": None
    }

    if voikko:
        result["tool"] = "voikko"
        result["valid"] = voikko.spell(word)
        if not result["valid"]:
            result["suggestions"] = voikko.suggest(word)[:5]
        analysis = voikko.analyze(word)
        if analysis:
            result["analysis"] = [a.get("BASEFORM", word) for a in analysis[:3]]
    elif uralicApi:
        result["tool"] = "uralicnlp"
        analyses = uralicApi.analyze(word, "fin")
        result["valid"] = len(analyses) > 0
        if analyses:
            result["analysis"] = [a[0] for a in analyses[:3]]
        if not result["valid"]:
            # UralicNLP doesn't have built-in suggestions
            result["suggestions"] = []
    else:
        result["tool"] = "none"
        result["valid"] = None  # Cannot determine

    return result


def validate_topic_name(name_fi: str) -> dict:
    """
    Validate a Finnish topic name (may be multi-word).
    """
    if not name_fi:
        return {"valid": False, "error": "Empty name", "words": []}

    # Split into words and check each
    words = name_fi.split()
    word_results = []
    all_valid = True

    for word in words:
        # Skip very short words and common particles
        if len(word) <= 2 or word.lower() in {"ja", "tai", "eli", "vai", "kun", "jos", "sen", "sen"}:
            word_results.append({"word": word, "valid": True, "skipped": True})
            continue

        result = check_word(word)
        word_results.append(result)

        if result["valid"] is False:
            all_valid = False
        elif result["valid"] is None:
            # Cannot determine - don't mark as invalid
            pass

    return {
        "name_fi": name_fi,
        "valid": all_valid,
        "words": word_results
    }


def validate_csv(filepath: str) -> list:
    """
    Validate Finnish translations in a CSV file.
    Expected columns: slug, name_en, name_fi
    """
    results = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name_fi = row.get('name_fi', '')
            if not name_fi:
                continue

            validation = validate_topic_name(name_fi)
            validation["slug"] = row.get('slug', '')
            validation["name_en"] = row.get('name_en', '')
            results.append(validation)

    return results


def print_validation_report(results: list):
    """Print a human-readable validation report."""
    valid_count = sum(1 for r in results if r.get("valid"))
    invalid_count = sum(1 for r in results if not r.get("valid"))

    print(f"\n=== Finnish Translation Validation Report ===")
    print(f"Valid: {valid_count}")
    print(f"Needs Review: {invalid_count}")
    print(f"Total: {len(results)}")

    if invalid_count > 0:
        print(f"\n--- Topics Needing Review ---\n")
        for r in results:
            if not r.get("valid"):
                print(f"  {r.get('name_en', '?')} -> {r.get('name_fi', '?')}")
                for word in r.get("words", []):
                    if word.get("valid") is False:
                        suggestions = word.get("suggestions", [])
                        if suggestions:
                            print(f"    '{word['word']}' - Suggestions: {', '.join(suggestions[:3])}")
                        else:
                            print(f"    '{word['word']}' - Not recognized")
                print()


def main():
    parser = argparse.ArgumentParser(description="Validate Finnish topic translations")
    parser.add_argument("--csv", help="CSV file to validate")
    parser.add_argument("--word", help="Single word to test")
    parser.add_argument("--all", action="store_true", help="Check all topics (not just unchecked)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Check if any validation tool is available
    if voikko is None and uralicApi is None:
        print("ERROR: No Finnish validation library available.", file=sys.stderr)
        print("Install one of:", file=sys.stderr)
        print("  pip install libvoikko  (+ system library)", file=sys.stderr)
        print("  pip install uralicnlp", file=sys.stderr)
        sys.exit(1)

    tool_name = "voikko" if voikko else "uralicnlp"
    print(f"Using validation tool: {tool_name}", file=sys.stderr)

    if args.word:
        # Test single word
        result = check_word(args.word)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            status = "VALID" if result["valid"] else "INVALID" if result["valid"] is False else "UNKNOWN"
            print(f"Word: {args.word}")
            print(f"Status: {status}")
            if result["analysis"]:
                print(f"Base forms: {', '.join(result['analysis'])}")
            if result["suggestions"]:
                print(f"Suggestions: {', '.join(result['suggestions'])}")

    elif args.csv:
        # Validate CSV file
        results = validate_csv(args.csv)
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print_validation_report(results)

    else:
        # Interactive mode - print usage
        print("Finnish Topic Name Validator")
        print()
        print("Usage examples:")
        print("  python validate_finnish.py --word 'armo'")
        print("  python validate_finnish.py --word 'valtaistuin'")
        print("  python validate_finnish.py --csv topics.csv")
        print()
        print("To validate topics from database:")
        print("1. Export topics to CSV using SQL query")
        print("2. Run: python validate_finnish.py --csv exported_topics.csv")


if __name__ == "__main__":
    main()
