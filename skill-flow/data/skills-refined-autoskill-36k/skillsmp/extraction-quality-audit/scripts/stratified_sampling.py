#!/usr/bin/env python3
"""
Apply stratified sampling to select representative documents for quality investigation.
Configurable priority areas and sampling criteria.
"""

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Optional


def load_inventory(inventory_file: Path) -> List[Dict]:
    """Load the document inventory."""
    with open(inventory_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_sampling_config(config_file: Optional[Path]) -> Dict:
    """Load sampling configuration or return defaults."""
    if config_file and config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Default configuration
    return {
        'priority_tags': {
            'LOW_CONF': {'coverage': 1.0, 'priority': 1000},
            'COMPLEX': {'coverage': 1.0, 'priority': 100},
            'OLD_DOC': {'coverage': 0.7, 'priority': 10},
            'MULTI_PAGE': {'coverage': 0.4, 'priority': 1},
        },
        'category_balance': {
            'imaging': 3,
            'ultrasound': 3,
            'endoscopy': 3,
            'other': 2,
        },
        'random_seed': 42
    }


def stratified_sample(
    inventory: List[Dict],
    target_size: int,
    config: Dict
) -> List[Dict]:
    """
    Apply stratified sampling based on priority criteria.

    Args:
        inventory: List of document entries
        target_size: Target sample size
        config: Sampling configuration

    Returns:
        List of sampled documents with sample_reason field
    """
    sample = []
    used_stems = set()
    priority_tags = config.get('priority_tags', {})
    category_balance = config.get('category_balance', {})

    def add_to_sample(docs: List[Dict], count: int, label: str):
        """Add documents to sample, avoiding duplicates."""
        available = [d for d in docs if d['doc_stem'] not in used_stems]
        if not available:
            return []

        # Calculate actual count based on coverage
        actual_count = min(count, len(available))

        selected = random.sample(available, actual_count)
        for doc in selected:
            doc['sample_reason'] = label
            used_stems.add(doc['doc_stem'])
        sample.extend(selected)
        print(f"  {label}: selected {len(selected)} documents")
        return selected

    print("\nStratified Sampling Process:")
    print("=" * 60)

    # Phase 1: Priority tags with specified coverage
    for tag, tag_config in sorted(
        priority_tags.items(),
        key=lambda x: -x[1].get('priority', 0)
    ):
        coverage = tag_config.get('coverage', 1.0)
        docs_with_tag = [d for d in inventory if tag in d.get('tags', [])]

        if docs_with_tag:
            count = int(len(docs_with_tag) * coverage)
            if coverage == 1.0:
                add_to_sample(docs_with_tag, count, f"{tag} (all)")
            else:
                add_to_sample(docs_with_tag, count, f"{tag} ({coverage*100:.0f}%)")

    # Track remaining target
    remaining = target_size - len(sample)
    print(f"\n  Currently selected: {len(sample)} documents")
    print(f"  Remaining target: {remaining} documents")

    # Phase 2: Ensure category diversity
    if category_balance and remaining > 0:
        for category, count in category_balance.items():
            cat_docs = [d for d in inventory if d.get('category') == category]
            if cat_docs:
                add_to_sample(cat_docs, count, f"CATEGORY_{category.upper()}")

        remaining = target_size - len(sample)
        print(f"\n  After category balancing: {len(sample)} documents")
        print(f"  Remaining target: {remaining} documents")

    # Phase 3: Ensure era diversity
    if remaining > 0:
        # Try to include some recent documents for comparison
        recent_docs = [d for d in inventory if d.get('era') == '2020s']
        if recent_docs:
            add_to_sample(recent_docs, min(3, remaining), "ERA_2020s (recent)")

        remaining = target_size - len(sample)

    # Phase 4: High confidence baseline
    if remaining > 0:
        high_conf = [
            d for d in inventory
            if d.get('min_confidence') is not None and d['min_confidence'] >= 0.9
        ]
        if high_conf:
            add_to_sample(high_conf, min(3, remaining), "HIGH_CONF (baseline)")

        remaining = target_size - len(sample)

    # Phase 5: Random fill to reach target size
    if remaining > 0:
        add_to_sample(inventory, remaining, "RANDOM_FILL")

    print(f"\n  Final sample size: {len(sample)} documents")

    return sample


def print_sample_summary(sample: List[Dict], inventory: List[Dict]):
    """Print summary statistics about the sample."""
    print("\n" + "=" * 60)
    print("SAMPLE SUMMARY")
    print("=" * 60)

    # Profile distribution
    profiles = {}
    for doc in sample:
        profile = doc.get('profile', 'unknown')
        profiles[profile] = profiles.get(profile, 0) + 1

    if len(profiles) > 1:
        print(f"\nProfile Distribution:")
        for profile, count in sorted(profiles.items()):
            pct = count / len(sample) * 100
            print(f"  {profile}: {count} documents ({pct:.1f}%)")

    # Tag distribution in sample
    tag_counts = {}
    for doc in sample:
        for tag in doc.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print(f"\nPriority Tags in Sample:")
    priority_tags = ['LOW_CONF', 'COMPLEX', 'OLD_DOC', 'MULTI_PAGE']
    for tag in priority_tags:
        count = tag_counts.get(tag, 0)
        total = len([d for d in inventory if tag in d.get('tags', [])])
        if total > 0:
            coverage = count / total * 100
            print(f"  {tag}: {count} documents ({coverage:.0f}% of {total})")

    # Category distribution
    cat_counts = {}
    for doc in sample:
        cat = doc.get('category', 'unknown')
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    print(f"\nCategory Distribution:")
    for cat, count in sorted(cat_counts.items()):
        print(f"  {cat}: {count} documents")

    # Era distribution
    era_counts = {}
    for doc in sample:
        era = doc.get('era', 'unknown')
        era_counts[era] = era_counts.get(era, 0) + 1
    print(f"\nEra Distribution:")
    for era, count in sorted(era_counts.items()):
        print(f"  {era}: {count} documents")

    # Confidence distribution
    low = len([d for d in sample if d.get('min_confidence', 1) < 0.7])
    med = len([d for d in sample if d.get('min_confidence', 1) >= 0.7 and d.get('min_confidence', 1) < 0.9])
    high = len([d for d in sample if d.get('min_confidence', 1) >= 0.9])
    print(f"\nConfidence Distribution:")
    print(f"  High (≥0.9): {high} documents")
    print(f"  Medium (0.7-0.9): {med} documents")
    print(f"  Low (<0.7): {low} documents")

    # Complexity distribution
    simple = len([d for d in sample if d['page_count'] <= 2])
    multi = len([d for d in sample if 3 <= d['page_count'] < 10])
    complex_docs = len([d for d in sample if d['page_count'] >= 10])
    print(f"\nComplexity Distribution:")
    print(f"  Simple (1-2 pages): {simple} documents")
    print(f"  Multi-page (3-9 pages): {multi} documents")
    print(f"  Complex (10+ pages): {complex_docs} documents")


def print_sample_list(sample: List[Dict]):
    """Print detailed list of selected documents."""
    print("\n" + "=" * 60)
    print("SELECTED DOCUMENTS")
    print("=" * 60)

    for i, doc in enumerate(sample, 1):
        tags_str = ', '.join(doc.get('tags', []))
        conf = doc.get('min_confidence', 0)
        print(f"\n{i}. {doc['doc_stem'][:60]}")
        print(f"   Profile: {doc['profile']} | Pages: {doc['page_count']} | Conf: {conf:.2f}")
        print(f"   Category: {doc.get('category', 'unknown')} | Era: {doc.get('era', 'unknown')}")
        print(f"   Tags: {tags_str}")
        print(f"   Reason: {doc.get('sample_reason', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate stratified sample for quality investigation'
    )
    parser.add_argument(
        '--inventory',
        type=Path,
        default=Path('inventory.json'),
        help='Input inventory file'
    )
    parser.add_argument(
        '--target-size',
        type=int,
        default=30,
        help='Target sample size'
    )
    parser.add_argument(
        '--config',
        type=Path,
        help='Sampling configuration file (JSON)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('sample.json'),
        help='Output filename for sample'
    )
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='Print detailed list of selected documents'
    )

    args = parser.parse_args()

    # Load inventory
    inventory = load_inventory(args.inventory)
    print(f"Loaded inventory: {len(inventory)} documents")

    # Load sampling configuration
    config = load_sampling_config(args.config)

    # Set random seed
    seed = args.seed if args.seed else config.get('random_seed', 42)
    random.seed(seed)
    print(f"Using random seed: {seed}")

    # Generate stratified sample
    sample = stratified_sample(inventory, args.target_size, config)

    # Sort by priority tags and profile
    def sort_key(doc):
        priority = 0
        if 'LOW_CONF' in doc.get('tags', []):
            priority += 1000
        if 'COMPLEX' in doc.get('tags', []):
            priority += 100
        if 'OLD_DOC' in doc.get('tags', []):
            priority += 10
        if 'MULTI_PAGE' in doc.get('tags', []):
            priority += 1
        return (-priority, doc['profile'], doc['doc_stem'])

    sample.sort(key=sort_key)

    # Save sample to JSON
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(sample, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Sample saved to {args.output}")

    # Print summary statistics
    print_sample_summary(sample, inventory)

    # Print detailed list if requested
    if args.list:
        print_sample_list(sample)


if __name__ == '__main__':
    main()
