#!/usr/bin/env python3
"""
Compare Keyword Sets

Usage:
    python3 compare_keywords.py <resume_keywords_file> <job_keywords_file>

    Input files should be JSON lists of strings or newline-separated text files.

Dependencies:
    None
"""

import sys
import argparse
import json


def load_keywords(file_path):
    """Load keywords from JSON or text file."""
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            # Try parsing as JSON
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    return set(str(k).lower().strip() for k in data)
            except json.JSONDecodeError:
                pass

            # Fallback to newline strings
            return set(
                line.lower().strip() for line in content.splitlines() if line.strip()
            )
    except Exception as e:
        print(f"Error reading keywords file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def compare(resume_kw, job_kw):
    """
    Compare two sets of keywords.

    Returns:
        dict: Statistics including match count, missing keywords, and score.
    """
    matches = resume_kw.intersection(job_kw)
    missing = job_kw.difference(resume_kw)

    total_job_keywords = len(job_kw)
    match_count = len(matches)

    score = 0.0
    if total_job_keywords > 0:
        score = match_count / total_job_keywords

    return {
        "score": score,
        "match_count": match_count,
        "total_required": total_job_keywords,
        "matches": list(matches),
        "missing": list(missing),
    }


def main():
    parser = argparse.ArgumentParser(description="Compare keyword sets")
    parser.add_argument("resume_keywords", help="File with resume keywords")
    parser.add_argument("job_keywords", help="File with job keywords")

    args = parser.parse_args()

    resume_set = load_keywords(args.resume_keywords)
    job_set = load_keywords(args.job_keywords)

    result = compare(resume_set, job_set)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
