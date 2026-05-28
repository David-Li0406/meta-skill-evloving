#!/usr/bin/env python3
"""
Direct Markdown to HTML Converter - Main Entry Point.

This module provides the main entry point for converting Markdown documents
directly to HTML presentations without JSON serialization.

New pipeline:
    Markdown → Parser → ParsedDocument → SlidePlanner → SlideSpec[] → DirectGenerator → HTML

Old pipeline (still supported):
    Markdown → Parser → ParsedDocument → JSON → Generator → HTML
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from parser import DocumentParser, ParsedDocument
from slide_planner import SlidePlanner
from direct_generator import DirectGenerator
from generator_v3 import PresentationGenerator


def convert_markdown_to_presentation(
    markdown_path: str,
    output_path: str = 'presentation.html',
    use_direct_pipeline: bool = True
) -> str:
    """
    Complete Markdown to HTML conversion.

    Args:
        markdown_path: Path to the Markdown file
        output_path: Path for the output HTML file
        use_direct_pipeline: If True, use new direct pipeline; if False, use old JSON pipeline

    Returns:
        Absolute path to the generated HTML file
    """
    # Validate input file exists
    md_file = Path(markdown_path)
    if not md_file.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    # 1. Parse the markdown file
    parser = DocumentParser()
    doc: ParsedDocument = parser.parse(str(md_file))

    if use_direct_pipeline:
        # 2. Plan slides
        planner = SlidePlanner()
        slide_plan = planner.plan_slides(doc)

        # 3. Generate HTML
        generator = DirectGenerator()
        output_file = generator.generate(slide_plan, output_path)
    else:
        # Use old JSON-based pipeline for backward compatibility
        generator = PresentationGenerator()
        parsed_doc_dict = _parsed_document_to_dict(doc)
        output_file = generator.generate(parsed_doc_dict, output_path)

    return output_file


def _parsed_document_to_dict(doc: ParsedDocument) -> dict:
    """Convert ParsedDocument to dict for backward compatibility."""
    return {
        'title': doc.title,
        'doc_type': doc.doc_type.value,
        'sections': [
            {
                'title': s.title,
                'content': s.content,
                'level': s.level,
                'subsections': [
                    {
                        'title': sub.title,
                        'content': sub.content,
                        'level': sub.level
                    }
                    for sub in s.subsections
                ]
            }
            for s in doc.sections
        ],
        'data_points': [
            {
                'label': dp.label,
                'value': dp.value,
                'unit': dp.unit,
                'category': dp.category
            }
            for dp in doc.data_points
        ],
        'conclusions': [
            {
                'text': c.text,
                'category': c.category,
                'priority': c.priority
            }
            for c in doc.conclusions
        ],
        'raw_content': doc.raw_content
    }


def main():
    """Command-line interface."""
    arg_parser = argparse.ArgumentParser(
        description='Convert Markdown to HTML presentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (new direct pipeline)
  python direct_converter.py input.md output.html

  # Use old JSON pipeline (backward compatibility)
  python direct_converter.py input.md output.html --use-old-pipeline

  # Specify output directory
  python direct_converter.py input.md -o ./presentations/report.html

  # Verbose mode
  python direct_converter.py input.md output.html -v
        """
    )

    arg_parser.add_argument(
        'input',
        help='Input Markdown file path'
    )

    arg_parser.add_argument(
        'output',
        nargs='?',
        default='presentation.html',
        help='Output HTML file path (default: presentation.html)'
    )

    arg_parser.add_argument(
        '-o', '--output',
        dest='output_path',
        help='Output HTML file path (alternative way to specify output)'
    )

    arg_parser.add_argument(
        '--use-old-pipeline',
        action='store_true',
        help='Use old JSON-based pipeline instead of new direct pipeline'
    )

    arg_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = arg_parser.parse_args()

    # Use output_path if provided, otherwise use output positional arg
    output_file = args.output_path or args.output

    try:
        if args.verbose:
            print(f"Converting {args.input} to {output_file}...")
            print(f"Using {'direct' if not args.use_old_pipeline else 'old JSON'} pipeline")

        result = convert_markdown_to_presentation(
            args.input,
            output_file,
            use_direct_pipeline=not args.use_old_pipeline
        )

        if args.verbose:
            print(f"✓ Successfully generated presentation: {result}")
        else:
            print(result)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error converting file: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
