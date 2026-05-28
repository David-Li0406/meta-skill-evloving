#!/usr/bin/env python3
"""
Framework for systematic quality verification of sampled documents.
This script manages the verification workflow and results tracking.

This is a template-driven framework that guides interactive verification
with Claude Code. It tracks progress and saves results incrementally.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def load_sample(sample_file: Path) -> List[Dict]:
    """Load the sample of documents to verify."""
    with open(sample_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_results(results_file: Path) -> List[Dict]:
    """Load existing verification results if available."""
    if results_file.exists():
        with open(results_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_results(results: List[Dict], results_file: Path):
    """Save verification results."""
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def get_document_paths(doc: Dict, path_config: Optional[Dict] = None) -> Dict[str, Path]:
    """
    Get all relevant file paths for a document.

    This is a template function that should be customized based on
    your specific directory structure.

    Args:
        doc: Document entry from inventory
        path_config: Optional configuration for path mapping

    Returns:
        Dictionary with source_pdf, output_dir, md_files, summary_file keys
    """
    doc_stem = doc['doc_stem']
    doc_dir = Path(doc['doc_dir'])

    # Default: assume doc_dir contains all output files
    md_files = sorted([f for f in doc_dir.glob("*.md")
                      if not f.name.endswith('.summary.md')])
    summary_file = doc_dir / f"{doc_stem}.summary.md"

    # Try to find source PDF (this may need customization)
    # Look in parent directory or configured input directory
    source_pdf = None
    if path_config and 'input_dir' in path_config:
        input_dir = Path(path_config['input_dir'])
        pdf_candidates = list(input_dir.glob(f"{doc_stem}.pdf"))
        source_pdf = pdf_candidates[0] if pdf_candidates else None

    return {
        'source_pdf': source_pdf,
        'output_dir': doc_dir,
        'md_files': md_files,
        'summary_file': summary_file if summary_file.exists() else None,
    }


def create_verification_template() -> Dict:
    """Create a template for verification results."""
    return {
        'metadata_accuracy': {
            'score': 0,  # 0-10
            'issues': []
        },
        'transcription_quality': {
            'completeness_score': 0,  # 0-10
            'accuracy_score': 0,  # 0-10
            'layout_preservation_score': 0,  # 0-10
            'overall_score': 0,  # 0-10
            'issues': []
        },
        'domain_terminology': {
            'rating': '',  # Excellent/Good/Fair/Poor
            'issues': []
        },
        'summary_quality': {
            'score': 0,  # 0-10
            'issues': []
        },
        'multi_page_coherence': {
            'score': 0,  # 0-10 (only for multi-page docs)
            'issues': []
        },
        'overall_assessment': '',  # Excellent/Good/Fair/Poor
        'notable_issues': [],
        'recommendations': [],
        'verified_date': None
    }


def print_verification_checklist(doc: Dict, paths: Dict):
    """Print verification checklist for a document."""
    print("\n" + "=" * 80)
    print(f"VERIFICATION CHECKLIST: {doc['doc_stem'][:60]}")
    print("=" * 80)
    print(f"Profile: {doc.get('profile', 'N/A')}")
    print(f"Pages: {doc.get('page_count', 'N/A')}")
    print(f"Confidence: {doc.get('min_confidence', 'N/A')}")
    print(f"Category: {doc.get('category', 'unknown')}")
    print(f"Era: {doc.get('era', 'unknown')}")
    print(f"Tags: {', '.join(doc.get('tags', []))}")
    print(f"Sample Reason: {doc.get('sample_reason', 'N/A')}")
    print()
    print(f"Source PDF: {paths.get('source_pdf', 'Not found')}")
    print(f"Output Dir: {paths['output_dir']}")
    print(f"Page Files: {len(paths['md_files'])} files")
    print(f"Summary File: {'Yes' if paths.get('summary_file') else 'No'}")
    print()
    print("VERIFICATION STEPS:")
    print("1. [ ] Read source document (PDF or image)")
    print("2. [ ] Read all extraction output files")
    print("3. [ ] Verify metadata accuracy (date, title, category, etc.)")
    print("4. [ ] Verify transcription completeness & accuracy")
    print("5. [ ] Verify domain-specific terminology")

    if paths.get('summary_file'):
        print("6. [ ] Read summary file")
        print("7. [ ] Verify summary quality")

    if doc.get('page_count', 0) > 2:
        print("8. [ ] MULTI-PAGE: Verify cross-page consistency")

    if 'LOW_CONF' in doc.get('tags', []):
        print("9. [ ] LOW CONFIDENCE: Investigate root cause")

    if 'COMPLEX' in doc.get('tags', []):
        print("10. [ ] COMPLEX: Verify handling of complexity")

    print()


def print_verification_guide():
    """Print general verification guidelines."""
    print("\n" + "=" * 80)
    print("VERIFICATION GUIDELINES")
    print("=" * 80)
    print("""
1. METADATA ACCURACY (Score 0-10):
   - Date: Exact match with source?
   - Title/Name: Correctly extracted?
   - Category: Appropriate classification?
   - Facility/Doctor: Names correct (including accents)?
   - Other fields: All present and accurate?

2. TRANSCRIPTION QUALITY (Score 0-10 for each):
   - Completeness: All visible text captured? (0-10)
   - Accuracy: Text matches source exactly? (0-10)
   - Layout: Structure and spacing preserved? (0-10)
   - Overall: Average of above scores

3. DOMAIN TERMINOLOGY (Excellent/Good/Fair/Poor):
   - Medical: Anatomical terms, diagnoses, measurements with units
   - Legal: Contract clauses, citations, legal entities
   - Financial: Accounting terms, currencies, numerical precision
   - Technical: Code, APIs, formulas, version numbers
   - Check: Accents/special characters preserved?

4. SUMMARY QUALITY (Score 0-10):
   - Completeness: All key findings included?
   - Accuracy: No hallucinations or errors?
   - Appropriate detail level?
   - De-identification if applicable?

5. MULTI-PAGE COHERENCE (Score 0-10):
   - Metadata consistent across all pages?
   - Page numbering correct?
   - No duplicate content?
   - Cross-page references preserved?

6. LOW CONFIDENCE INVESTIGATION:
   - What triggered low confidence?
   - Is it justified (images, handwriting, complexity)?
   - Is extraction quality still acceptable?

SCORING RUBRIC:
- 10: Perfect, no issues
- 9: Excellent, negligible issues
- 8: Very good, minor issues
- 7: Good, some noticeable issues
- 6: Fair, several issues
- 5: Mediocre, significant issues
- 0-4: Poor to failing
""")


def add_verification_result(
    results: List[Dict],
    doc: Dict,
    verification: Dict,
    results_file: Path
):
    """Add a verification result and save incrementally."""
    result_entry = {
        'doc_stem': doc['doc_stem'],
        'profile': doc.get('profile'),
        'page_count': doc.get('page_count'),
        'min_confidence': doc.get('min_confidence'),
        'category': doc.get('category'),
        'tags': doc.get('tags', []),
        'sample_reason': doc.get('sample_reason'),
        'verification': verification
    }

    results.append(result_entry)
    save_results(results, results_file)
    print(f"\n✓ Verification saved for {doc['doc_stem']}")


def print_progress(sample: List[Dict], results: List[Dict]):
    """Print verification progress."""
    verified_stems = {r['doc_stem'] for r in results}
    remaining = [d for d in sample if d['doc_stem'] not in verified_stems]

    print("\n" + "=" * 80)
    print("VERIFICATION PROGRESS")
    print("=" * 80)
    print(f"Total documents: {len(sample)}")
    print(f"Verified: {len(verified_stems)} ({len(verified_stems)/len(sample)*100:.1f}%)")
    print(f"Remaining: {len(remaining)} ({len(remaining)/len(sample)*100:.1f}%)")

    if len(verified_stems) > 0:
        # Calculate average scores
        scores = []
        for result in results:
            ver = result.get('verification', {})
            trans = ver.get('transcription_quality', {})
            overall = trans.get('overall_score', 0)
            if overall > 0:
                scores.append(overall)

        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"\nAverage Quality Score: {avg_score:.2f}/10")


def main():
    parser = argparse.ArgumentParser(
        description='Systematic quality verification framework'
    )
    parser.add_argument(
        '--sample',
        type=Path,
        default=Path('sample.json'),
        help='Sample file to verify'
    )
    parser.add_argument(
        '--results',
        type=Path,
        default=Path('verification_results.json'),
        help='Results file for saving verification data'
    )
    parser.add_argument(
        '--path-config',
        type=Path,
        help='Configuration file for path mapping (JSON)'
    )
    parser.add_argument(
        '--show-next',
        action='store_true',
        help='Show next document to verify'
    )
    parser.add_argument(
        '--show-progress',
        action='store_true',
        help='Show verification progress'
    )
    parser.add_argument(
        '--guide',
        action='store_true',
        help='Show verification guidelines'
    )

    args = parser.parse_args()

    # Load sample
    sample = load_sample(args.sample)
    print(f"Loaded {len(sample)} documents to verify")

    # Load existing results
    results = load_results(args.results)
    verified_stems = {r['doc_stem'] for r in results}
    print(f"Already verified: {len(verified_stems)} documents")

    # Load path configuration if provided
    path_config = None
    if args.path_config and args.path_config.exists():
        with open(args.path_config, 'r') as f:
            path_config = json.load(f)

    # Show verification guide
    if args.guide:
        print_verification_guide()
        return

    # Show progress
    if args.show_progress:
        print_progress(sample, results)
        return

    # Find next document to verify
    remaining = [d for d in sample if d['doc_stem'] not in verified_stems]

    if not remaining:
        print("\n✓ All documents verified!")
        print_progress(sample, results)
        return

    # Show next document
    if args.show_next or True:  # Always show next by default
        next_doc = remaining[0]
        paths = get_document_paths(next_doc, path_config)
        print_verification_checklist(next_doc, paths)

        print("\n" + "=" * 80)
        print("TO VERIFY THIS DOCUMENT:")
        print("=" * 80)
        print("\n1. Use Read tool to view source document:")
        if paths.get('source_pdf'):
            print(f"   {paths['source_pdf']}")
        else:
            print("   (Source PDF not found - update path_config)")

        print("\n2. Read each output file:")
        for md_file in paths['md_files'][:3]:  # Show first 3
            print(f"   {md_file}")
        if len(paths['md_files']) > 3:
            print(f"   ... and {len(paths['md_files']) - 3} more")

        if paths.get('summary_file'):
            print(f"\n3. Read summary file:")
            print(f"   {paths['summary_file']}")

        print("\n4. Document findings and save to results JSON")
        print(f"   Use: create_verification_template() for structure")

        print("\n" + "=" * 80)
        print(f"Progress: {len(verified_stems)}/{len(sample)} documents verified")
        print("=" * 80)


if __name__ == '__main__':
    main()
