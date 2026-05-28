#!/usr/bin/env python3
"""
Log research to RESEARCH.md using template.

Usage:
    log-research.py --topic "CI/CD Integration Patterns" \\
                    --purpose "Understand industry standards" \\
                    --findings "Most use polling" \\
                    --stories "Story 2, Story 3"

    # Pipe-separated input
    echo "Topic|Purpose|Findings|Story 1|Q5" | log-research.py --from-stdin
"""

import sys
import argparse
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.id_manager import IDManager
from lib.file_operations import SafeFileOperations
from lib.templates import TemplateManager


def log_research(discovery_dir: Path, topic: str, purpose: str = None,
                approach: str = None, findings: str = None, patterns: str = None,
                examples: str = None, implications: str = None,
                stories: str = None, questions: str = None):
    """
    Log research to RESEARCH.md.

    Args:
        discovery_dir: Path to discovery/ directory
        topic: Research topic
        purpose: Why research was conducted
        approach: How research was conducted
        findings: Key findings
        patterns: Industry patterns identified
        examples: Relevant examples
        implications: Implications for stories
        stories: Stories informed
        questions: Related questions
    """
    # Get next research ID
    id_manager = IDManager(discovery_dir)
    research_id = id_manager.get_next_id('research')
    id_num = research_id[1:]  # Remove 'R' prefix

    # Load and render template
    template_mgr = TemplateManager()

    rendered = template_mgr.render_template(
        'research-entry.md',
        ID=id_num,
        TOPIC=topic,
        PURPOSE=purpose or '[Purpose not provided]',
        APPROACH=approach or '[Approach not provided]',
        FINDINGS=findings or '[Findings not provided]',
        PATTERNS=patterns or '[Patterns not provided]',
        EXAMPLES=examples or '[Examples not provided]',
        IMPLICATIONS=implications or '[Implications not provided]',
        STORIES=stories or '[Stories not specified]',
        QUESTIONS=questions or '[Questions not specified]'
    )

    # Append to RESEARCH.md
    research_file = discovery_dir / 'archive' / 'RESEARCH.md'
    if not research_file.exists():
        raise FileNotFoundError(f"File not found: {research_file}")

    content = SafeFileOperations.read_file(research_file)

    # Append research entry
    updated_content = content.rstrip() + '\n\n' + rendered

    # Write updated content
    SafeFileOperations.write_file(research_file, updated_content)

    print(f"✓ Logged {research_id}: {topic}")
    if stories:
        print(f"  Stories: {stories}")
    if questions:
        print(f"  Questions: {questions}")


def main():
    parser = argparse.ArgumentParser(
        description='Log research to RESEARCH.md'
    )
    parser.add_argument(
        '--topic',
        help='Research topic'
    )
    parser.add_argument(
        '--purpose',
        help='Why research was conducted'
    )
    parser.add_argument(
        '--approach',
        help='How research was conducted'
    )
    parser.add_argument(
        '--findings',
        help='Key findings'
    )
    parser.add_argument(
        '--patterns',
        help='Industry patterns identified'
    )
    parser.add_argument(
        '--examples',
        help='Relevant examples from products'
    )
    parser.add_argument(
        '--implications',
        help='Implications for stories'
    )
    parser.add_argument(
        '--stories',
        help='Stories informed (comma-separated)'
    )
    parser.add_argument(
        '--questions',
        help='Related questions (comma-separated)'
    )
    parser.add_argument(
        '--from-stdin',
        action='store_true',
        help='Read pipe-separated input from stdin'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Parse input
        if args.from_stdin:
            # Read from stdin: topic|purpose|findings|stories|questions
            line = sys.stdin.read().strip()
            parts = line.split('|')
            if len(parts) < 2:
                print("ERROR: Pipe-separated input requires at least: topic|purpose", file=sys.stderr)
                return 1

            topic = parts[0]
            purpose = parts[1]
            findings = parts[2] if len(parts) > 2 else None
            stories = parts[3] if len(parts) > 3 else None
            questions = parts[4] if len(parts) > 4 else None
            approach = None
            patterns = None
            examples = None
            implications = None
        else:
            # Read from args
            if not args.topic:
                print("ERROR: --topic is required", file=sys.stderr)
                return 1

            topic = args.topic
            purpose = args.purpose
            approach = args.approach
            findings = args.findings
            patterns = args.patterns
            examples = args.examples
            implications = args.implications
            stories = args.stories
            questions = args.questions

        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Log research
        log_research(
            discovery_dir, topic, purpose, approach, findings,
            patterns, examples, implications, stories, questions
        )

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
