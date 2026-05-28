#!/usr/bin/env python3
"""
Generate comprehensive document inventory for quality investigation.
Extracts metadata from all processed documents for stratified sampling.

This script is generic and configurable for any extraction pipeline.
"""

import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Callable
import yaml


def extract_yaml_frontmatter(md_file: Path) -> Optional[Dict]:
    """Extract YAML frontmatter from markdown file."""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            return yaml.safe_load(yaml_content)
        return None
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
        return None


def extract_json_metadata(json_file: Path) -> Optional[Dict]:
    """Extract metadata from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {json_file}: {e}")
        return None


def get_document_inventory(
    profile_name: str,
    output_dir: Path,
    metadata_format: str = 'yaml',
    summary_pattern: str = '*.summary.md'
) -> List[Dict]:
    """
    Generate inventory for a single profile/category.

    Args:
        profile_name: Name of the profile or category
        output_dir: Directory containing extraction outputs
        metadata_format: Format of metadata ('yaml', 'json', 'frontmatter')
        summary_pattern: Glob pattern for summary files

    Returns:
        List of document inventory entries
    """
    inventory = []

    if not output_dir.exists():
        print(f"Warning: {output_dir} does not exist")
        return inventory

    # Iterate through all document directories
    for doc_dir in sorted(output_dir.iterdir()):
        if not doc_dir.is_dir() or doc_dir.name.startswith('.'):
            continue

        # Find all page markdown files (exclude summary)
        if metadata_format == 'yaml' or metadata_format == 'frontmatter':
            page_files = sorted([f for f in doc_dir.glob("*.md")
                                if not f.name.endswith('.summary.md')])
            summary_file = doc_dir / f"{doc_dir.name}.summary.md"
        elif metadata_format == 'json':
            page_files = sorted([f for f in doc_dir.glob("*.json")
                                if not f.name.endswith('.summary.json')])
            summary_file = doc_dir / f"{doc_dir.name}.summary.json"
        else:
            print(f"Unsupported metadata format: {metadata_format}")
            continue

        if not page_files:
            continue

        # Extract metadata from first page
        if metadata_format == 'json':
            first_page_meta = extract_json_metadata(page_files[0])
        else:
            first_page_meta = extract_yaml_frontmatter(page_files[0])

        # Collect confidence scores from all pages
        confidence_scores = []
        for page_file in page_files:
            if metadata_format == 'json':
                meta = extract_json_metadata(page_file)
            else:
                meta = extract_yaml_frontmatter(page_file)

            if meta and 'confidence' in meta:
                confidence_scores.append(meta['confidence'])

        # Build document inventory entry
        doc_entry = {
            'profile': profile_name,
            'doc_stem': doc_dir.name,
            'doc_dir': str(doc_dir),
            'page_count': len(page_files),
            'has_summary': summary_file.exists(),
            'confidence_scores': confidence_scores,
            'min_confidence': min(confidence_scores) if confidence_scores else None,
            'max_confidence': max(confidence_scores) if confidence_scores else None,
            'avg_confidence': sum(confidence_scores) / len(confidence_scores) if confidence_scores else None,
        }

        # Add metadata from first page if available
        if first_page_meta:
            # Copy all metadata fields (generic approach)
            for key, value in first_page_meta.items():
                if key not in doc_entry and key != 'page':  # Skip page number
                    doc_entry[key] = value

        # Determine document era (if date available)
        if doc_entry.get('date'):
            try:
                year = int(str(doc_entry['date'])[:4])
                if year < 2000:
                    doc_entry['era'] = '1990s'
                elif year < 2010:
                    doc_entry['era'] = '2000s'
                elif year < 2020:
                    doc_entry['era'] = '2010s'
                else:
                    doc_entry['era'] = '2020s'
            except:
                doc_entry['era'] = 'unknown'

        inventory.append(doc_entry)

    return inventory


def apply_priority_tags(
    inventory: List[Dict],
    tag_definitions: Dict[str, Callable[[Dict], bool]]
) -> List[Dict]:
    """
    Apply priority tags to inventory based on document characteristics.

    Args:
        inventory: List of document entries
        tag_definitions: Dictionary mapping tag names to lambda functions

    Returns:
        Updated inventory with tags applied
    """
    for doc in inventory:
        tags = []

        for tag_name, tag_func in tag_definitions.items():
            try:
                if tag_func(doc):
                    tags.append(tag_name)
            except Exception as e:
                # Silently skip if tag function fails
                pass

        doc['tags'] = tags

    return inventory


def print_inventory_statistics(inventory: List[Dict]):
    """Print summary statistics about the inventory."""
    print(f"\n{'='*60}")
    print(f"INVENTORY STATISTICS")
    print(f"{'='*60}")
    print(f"Total documents: {len(inventory)}")

    # Profile distribution
    profiles = {}
    for doc in inventory:
        profile = doc.get('profile', 'unknown')
        profiles[profile] = profiles.get(profile, 0) + 1

    if len(profiles) > 1:
        print(f"\nProfile Distribution:")
        for profile, count in sorted(profiles.items()):
            print(f"  {profile}: {count} documents")

    # Era distribution
    eras = {}
    for doc in inventory:
        era = doc.get('era', 'unknown')
        eras[era] = eras.get(era, 0) + 1
    print(f"\nEra Distribution:")
    for era, count in sorted(eras.items()):
        print(f"  {era}: {count} documents")

    # Category distribution
    categories = {}
    for doc in inventory:
        cat = doc.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    print(f"\nCategory Distribution:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} documents")

    # Tag distribution
    tag_counts = {}
    for doc in inventory:
        for tag in doc.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    print(f"\nTag Distribution:")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        print(f"  {tag}: {count} documents")

    # Confidence distribution
    low_conf = [d for d in inventory if d.get('min_confidence') and d['min_confidence'] < 0.7]
    med_conf = [d for d in inventory if d.get('min_confidence') and 0.7 <= d['min_confidence'] < 0.9]
    high_conf = [d for d in inventory if d.get('min_confidence') and d['min_confidence'] >= 0.9]
    print(f"\nConfidence Distribution:")
    print(f"  High (≥0.9): {len(high_conf)} documents")
    print(f"  Medium (0.7-0.9): {len(med_conf)} documents")
    print(f"  Low (<0.7): {len(low_conf)} documents")

    # Complexity distribution
    simple = [d for d in inventory if d['page_count'] <= 2]
    multi = [d for d in inventory if 3 <= d['page_count'] < 10]
    complex_docs = [d for d in inventory if d['page_count'] >= 10]
    print(f"\nComplexity Distribution:")
    print(f"  Simple (1-2 pages): {len(simple)} documents")
    print(f"  Multi-page (3-9 pages): {len(multi)} documents")
    print(f"  Complex (10+ pages): {len(complex_docs)} documents")


def main():
    parser = argparse.ArgumentParser(
        description='Generate document inventory for quality investigation'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        required=True,
        help='Directory containing extraction outputs'
    )
    parser.add_argument(
        '--profile-name',
        type=str,
        required=True,
        help='Profile or category name for this document set'
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        help='Directory containing source documents (for reference)'
    )
    parser.add_argument(
        '--metadata-format',
        type=str,
        default='yaml',
        choices=['yaml', 'json', 'frontmatter'],
        help='Format of metadata in output files'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('inventory.json'),
        help='Output filename for inventory'
    )
    parser.add_argument(
        '--multiple-profiles',
        action='store_true',
        help='Process multiple profiles from a parent directory'
    )

    args = parser.parse_args()

    # Default priority tag definitions
    TAG_DEFINITIONS = {
        'LOW_CONF': lambda doc: doc.get('min_confidence') is not None and doc['min_confidence'] < 0.7,
        'OLD_DOC': lambda doc: doc.get('era') in ['1990s', '2000s'],
        'COMPLEX': lambda doc: doc['page_count'] >= 10,
        'MULTI_PAGE': lambda doc: 3 <= doc['page_count'] < 10,
    }

    # Add category tags dynamically
    def make_category_tag(doc):
        cat = doc.get('category')
        if cat:
            return f"CAT_{cat.upper()}"
        return None

    all_inventory = []

    if args.multiple_profiles:
        # Process each subdirectory as a separate profile
        for profile_dir in sorted(args.output_dir.iterdir()):
            if not profile_dir.is_dir() or profile_dir.name.startswith('.'):
                continue

            print(f"\nProcessing {profile_dir.name} profile...")
            inventory = get_document_inventory(
                profile_dir.name,
                profile_dir,
                args.metadata_format
            )
            all_inventory.extend(inventory)
            print(f"  Found {len(inventory)} documents")
    else:
        # Process single profile
        print(f"\nProcessing {args.profile_name} profile...")
        inventory = get_document_inventory(
            args.profile_name,
            args.output_dir,
            args.metadata_format
        )
        all_inventory.extend(inventory)
        print(f"  Found {len(inventory)} documents")

    # Apply priority tags
    all_inventory = apply_priority_tags(all_inventory, TAG_DEFINITIONS)

    # Add category tags
    for doc in all_inventory:
        if doc.get('category'):
            doc['tags'].append(f"CAT_{doc['category'].upper()}")

    # Save inventory to JSON
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(all_inventory, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Inventory saved to {args.output}")

    # Print statistics
    print_inventory_statistics(all_inventory)


if __name__ == '__main__':
    main()
