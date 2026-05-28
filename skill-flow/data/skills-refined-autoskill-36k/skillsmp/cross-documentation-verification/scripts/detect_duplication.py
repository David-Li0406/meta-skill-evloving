#!/usr/bin/env python3
"""
Detect duplicate content across documentation files.

Usage:
    python detect_duplication.py --dir Docs/
    python detect_duplication.py --doc1 file1.md --doc2 file2.md
"""

import argparse
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


def normalize_text(text: str) -> str:
    """Normalize text for comparison (remove extra whitespace, lowercase)."""
    # Remove markdown syntax
    text = re.sub(r'[#*`_\[\]()]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_sections(content: str, file_path: Path) -> List[Dict]:
    """Extract sections from markdown content."""
    sections = []

    # Split by headers
    header_pattern = r'^(#{1,6})\s+(.+)$'
    current_section = {
        "level": 0,
        "title": "Frontmatter",
        "content": "",
        "file": str(file_path),
        "start_line": 1
    }

    lines = content.split('\n')
    line_num = 1

    for line in lines:
        header_match = re.match(header_pattern, line)
        if header_match:
            # Save previous section if has content
            if current_section["content"].strip():
                sections.append(current_section.copy())

            # Start new section
            level = len(header_match.group(1))
            title = header_match.group(2).strip()
            current_section = {
                "level": level,
                "title": title,
                "content": "",
                "file": str(file_path),
                "start_line": line_num
            }
        else:
            current_section["content"] += line + "\n"

        line_num += 1

    # Add final section
    if current_section["content"].strip():
        sections.append(current_section)

    return sections


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity ratio between two text blocks."""
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)

    if not norm1 or not norm2:
        return 0.0

    return difflib.SequenceMatcher(None, norm1, norm2).ratio()


def hash_content(text: str) -> str:
    """Generate hash of normalized content."""
    normalized = normalize_text(text)
    return hashlib.md5(normalized.encode()).hexdigest()


def find_duplicates_in_documents(documents: List[Path], threshold: float = 0.8) -> List[Dict]:
    """Find duplicate content across multiple documents."""
    all_sections = []

    # Extract all sections from all documents
    for doc_path in documents:
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            sections = extract_sections(content, doc_path)
            all_sections.extend(sections)
        except Exception as e:
            print(f"Error reading {doc_path}: {e}", file=sys.stderr)

    print(f"Extracted {len(all_sections)} sections from {len(documents)} documents", file=sys.stderr)

    # Find duplicates
    duplicates = []
    checked_pairs = set()

    for i, section1 in enumerate(all_sections):
        for j, section2 in enumerate(all_sections):
            if i >= j:
                continue

            # Skip if same file
            if section1["file"] == section2["file"]:
                continue

            # Skip if already checked this pair
            pair_key = f"{i}-{j}"
            if pair_key in checked_pairs:
                continue
            checked_pairs.add(pair_key)

            # Calculate similarity
            similarity = calculate_similarity(section1["content"], section2["content"])

            if similarity >= threshold:
                duplicates.append({
                    "similarity": round(similarity, 3),
                    "section1": {
                        "file": section1["file"],
                        "title": section1["title"],
                        "start_line": section1["start_line"],
                        "content_preview": section1["content"][:200]
                    },
                    "section2": {
                        "file": section2["file"],
                        "title": section2["title"],
                        "start_line": section2["start_line"],
                        "content_preview": section2["content"][:200]
                    },
                    "hash1": hash_content(section1["content"]),
                    "hash2": hash_content(section2["content"])
                })

    # Sort by similarity (highest first)
    duplicates.sort(key=lambda x: x["similarity"], reverse=True)

    return duplicates


def compare_two_files(file1: Path, file2: Path, threshold: float = 0.8) -> List[Dict]:
    """Compare two specific files for duplicate content."""
    return find_duplicates_in_documents([file1, file2], threshold)


def find_exact_duplicates(documents: List[Path]) -> List[Dict]:
    """Find sections with identical content across documents."""
    content_map = {}  # hash -> list of sections

    for doc_path in documents:
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            sections = extract_sections(content, doc_path)

            for section in sections:
                content_hash = hash_content(section["content"])
                if content_hash not in content_map:
                    content_map[content_hash] = []
                content_map[content_hash].append(section)
        except Exception as e:
            print(f"Error reading {doc_path}: {e}", file=sys.stderr)

    # Find duplicates (hash appears in multiple files)
    exact_duplicates = []
    for content_hash, sections in content_map.items():
        if len(sections) > 1:
            # Check if from different files
            files = set(s["file"] for s in sections)
            if len(files) > 1:
                exact_duplicates.append({
                    "hash": content_hash,
                    "count": len(sections),
                    "locations": [
                        {
                            "file": s["file"],
                            "title": s["title"],
                            "start_line": s["start_line"],
                            "content_preview": s["content"][:200]
                        }
                        for s in sections
                    ]
                })

    return exact_duplicates


def main():
    parser = argparse.ArgumentParser(
        description="Detect duplicate content across documentation files"
    )

    parser.add_argument("--dir", type=str,
                       help="Directory to scan for duplicates")
    parser.add_argument("--doc1", type=str,
                       help="First document for pairwise comparison")
    parser.add_argument("--doc2", type=str,
                       help="Second document for pairwise comparison")
    parser.add_argument("--threshold", type=float, default=0.8,
                       help="Similarity threshold (0.0-1.0, default 0.8)")
    parser.add_argument("--exact-only", action="store_true",
                       help="Only find exact duplicates (100%% match)")
    parser.add_argument("--output", type=str,
                       help="Output file path (JSON)")

    args = parser.parse_args()

    if not args.dir and not (args.doc1 and args.doc2):
        print("Error: Must specify either --dir or both --doc1 and --doc2", file=sys.stderr)
        sys.exit(1)

    # Find duplicates
    if args.doc1 and args.doc2:
        # Pairwise comparison
        doc1_path = Path(args.doc1)
        doc2_path = Path(args.doc2)
        if not doc1_path.exists() or not doc2_path.exists():
            print("Error: One or both documents not found", file=sys.stderr)
            sys.exit(1)

        if args.exact_only:
            duplicates = find_exact_duplicates([doc1_path, doc2_path])
        else:
            duplicates = compare_two_files(doc1_path, doc2_path, args.threshold)
    else:
        # Directory scan
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            print(f"Error: Directory not found: {dir_path}", file=sys.stderr)
            sys.exit(1)

        # Find all markdown files
        documents = [f for f in dir_path.rglob("*.md") if not any(skip in str(f) for skip in ['node_modules', '.git', 'archive'])]
        print(f"Scanning {len(documents)} documents...", file=sys.stderr)

        if args.exact_only:
            duplicates = find_exact_duplicates(documents)
        else:
            duplicates = find_duplicates_in_documents(documents, args.threshold)

    # Generate output
    output = {
        "duplicates": duplicates,
        "total_duplicates": len(duplicates),
        "threshold": args.threshold if not args.exact_only else 1.0,
        "exact_only": args.exact_only
    }

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2)
            print(f"Output written to {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(json.dumps(output, indent=2))

    # Print summary
    print(f"\nTotal duplicates found: {len(duplicates)}", file=sys.stderr)
    if duplicates:
        print("\nTop 5 duplicates:", file=sys.stderr)
        for i, dup in enumerate(duplicates[:5], 1):
            if args.exact_only:
                print(f"{i}. Found in {dup['count']} locations", file=sys.stderr)
            else:
                print(f"{i}. {dup['similarity']*100:.1f}% similarity", file=sys.stderr)
                print(f"   {dup['section1']['file']} <-> {dup['section2']['file']}", file=sys.stderr)


if __name__ == "__main__":
    main()
