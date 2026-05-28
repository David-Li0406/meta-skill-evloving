#!/usr/bin/env python3
"""
Log a decision to DECISIONS.md using template.

Usage:
    # Command-line args
    log-decision.py --title "Use JWT for auth" \\
                    --context "Need auth mechanism" \\
                    --decision "Use JWT tokens" \\
                    --rationale "Simpler implementation" \\
                    --stories "Story 1, Story 3" \\
                    --questions "Q12, Q15"

    # Pipe-separated input (for automation)
    echo "Use JWT|Need auth|Option 1: JWT...|Use JWT|Simpler|FR-001 generated|Story 1,Story 3|Q12,Q15" | \\
      log-decision.py --from-stdin
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


def log_decision(discovery_dir: Path, title: str, context: str, question: str = None,
                options: str = None, decision: str = None, rationale: str = None,
                implications: str = None, stories: str = None, questions: str = None):
    """
    Log decision to DECISIONS.md.

    Args:
        discovery_dir: Path to discovery/ directory
        title: Decision title
        context: Context explaining why decision was needed
        question: Question being answered (optional)
        options: Options considered (optional)
        decision: Chosen decision
        rationale: Rationale for decision
        implications: Implications (optional)
        stories: Stories affected (optional)
        questions: Related questions (optional)
    """
    # Get next decision ID
    id_manager = IDManager(discovery_dir)
    decision_id = id_manager.get_next_id('decision')
    id_num = decision_id[1:]  # Remove 'D' prefix

    # Load and render template
    template_mgr = TemplateManager()

    rendered = template_mgr.render_template(
        'decision-entry.md',
        ID=id_num,
        TITLE=title,
        CONTEXT=context or '[Context not provided]',
        QUESTION=question or '[Question not provided]',
        OPTIONS=options or '[Options not provided]',
        DECISION=decision or '[Decision not provided]',
        RATIONALE=rationale or '[Rationale not provided]',
        IMPLICATIONS=implications or '[Implications not provided]',
        STORIES=stories or '[Stories not specified]',
        QUESTIONS=questions or '[Questions not specified]'
    )

    # Append to DECISIONS.md
    decisions_file = discovery_dir / 'archive' / 'DECISIONS.md'
    if not decisions_file.exists():
        raise FileNotFoundError(f"File not found: {decisions_file}")

    content = SafeFileOperations.read_file(decisions_file)

    # Append decision entry
    updated_content = content.rstrip() + '\n\n' + rendered

    # Write updated content
    SafeFileOperations.write_file(decisions_file, updated_content)

    print(f"✓ Logged {decision_id}: {title}")
    if stories:
        print(f"  Stories: {stories}")
    if questions:
        print(f"  Questions: {questions}")


def main():
    parser = argparse.ArgumentParser(
        description='Log decision to DECISIONS.md'
    )
    parser.add_argument(
        '--title',
        help='Decision title'
    )
    parser.add_argument(
        '--context',
        help='Context explaining why decision was needed'
    )
    parser.add_argument(
        '--question',
        help='Question being answered'
    )
    parser.add_argument(
        '--options',
        help='Options considered (use newlines or semicolons to separate)'
    )
    parser.add_argument(
        '--decision',
        help='Chosen decision'
    )
    parser.add_argument(
        '--rationale',
        help='Rationale for decision'
    )
    parser.add_argument(
        '--implications',
        help='Implications of decision'
    )
    parser.add_argument(
        '--stories',
        help='Stories affected (comma-separated)'
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
            # Read from stdin: title|context|options|decision|rationale|implications|stories|questions
            line = sys.stdin.read().strip()
            parts = line.split('|')
            if len(parts) < 2:
                print("ERROR: Pipe-separated input requires at least: title|context", file=sys.stderr)
                return 1

            title = parts[0]
            context = parts[1]
            options = parts[2] if len(parts) > 2 else None
            decision = parts[3] if len(parts) > 3 else None
            rationale = parts[4] if len(parts) > 4 else None
            implications = parts[5] if len(parts) > 5 else None
            stories = parts[6] if len(parts) > 6 else None
            questions = parts[7] if len(parts) > 7 else None
            question = None  # Not in pipe format
        else:
            # Read from args
            if not args.title:
                print("ERROR: --title is required", file=sys.stderr)
                return 1

            title = args.title
            context = args.context
            question = args.question
            options = args.options
            decision = args.decision
            rationale = args.rationale
            implications = args.implications
            stories = args.stories
            questions = args.questions

        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Log decision
        log_decision(
            discovery_dir, title, context, question, options,
            decision, rationale, implications, stories, questions
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
