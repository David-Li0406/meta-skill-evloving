#!/usr/bin/env python3
"""
Log an iteration summary to ITERATIONS.md using template.

Usage:
    # Command-line args
    log-iteration.py --date-range "2026-01-19" \
                     --phase "Problem Exploration" \
                     --goals "Understand problem; Identify personas" \
                     --activities "Discovery research; User interviews" \
                     --outcomes "Problem statement drafted; 3 personas identified" \
                     --questions-added "Q1-Q5" \
                     --decisions-made "D1, D2" \
                     --research-conducted "R1" \
                     --next-steps "Transition to Story Crystallization"

    # Pipe-separated input (for automation)
    echo "2026-01-20|Story Crystallization|Define stories|Story backlog|5 stories|Q9-Q15|D1,D2|R1|Graduate stories" | \
      log-iteration.py --from-stdin
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


def log_iteration(discovery_dir: Path, date_range: str, phase: str, goals: str,
                 activities: str = None, outcomes: str = None,
                 questions_added: str = None, decisions_made: str = None,
                 research_conducted: str = None, next_steps: str = None):
    """
    Log iteration summary to ITERATIONS.md.

    Args:
        discovery_dir: Path to discovery/ directory
        date_range: Date or date range for iteration
        phase: Discovery phase name
        goals: Iteration goals
        activities: Activities performed (optional)
        outcomes: Key outcomes (optional)
        questions_added: Questions added (optional)
        decisions_made: Decisions made (optional)
        research_conducted: Research conducted (optional)
        next_steps: Next steps (optional)
    """
    # Get next iteration ID
    id_manager = IDManager(discovery_dir)
    iteration_id = id_manager.get_next_id('iteration')
    id_num = iteration_id[4:]  # Remove 'ITR-' prefix

    # Load and render template
    template_mgr = TemplateManager()

    rendered = template_mgr.render_template(
        'iteration-entry.md',
        ID=id_num,
        DATE_RANGE=date_range,
        PHASE=phase,
        GOALS=goals,
        ACTIVITIES=activities or '[Activities not provided]',
        OUTCOMES=outcomes or '[Outcomes not provided]',
        QUESTIONS_ADDED=questions_added or '[Questions not specified]',
        DECISIONS_MADE=decisions_made or '[Decisions not specified]',
        RESEARCH_CONDUCTED=research_conducted or '[Research not specified]',
        NEXT_STEPS=next_steps or '[Next steps not provided]'
    )

    # Append to ITERATIONS.md
    iterations_file = discovery_dir / 'archive' / 'ITERATIONS.md'
    if not iterations_file.exists():
        raise FileNotFoundError(f"File not found: {iterations_file}")

    content = SafeFileOperations.read_file(iterations_file)

    # Append iteration entry
    updated_content = content.rstrip() + '\n\n' + rendered

    # Write updated content
    SafeFileOperations.write_file(iterations_file, updated_content)

    print(f"✓ Logged {iteration_id}: {date_range} — {phase}")
    if outcomes:
        print(f"  Outcomes: {outcomes}")
    if next_steps:
        print(f"  Next: {next_steps}")


def main():
    parser = argparse.ArgumentParser(
        description='Log iteration summary to ITERATIONS.md'
    )
    parser.add_argument(
        '--date-range',
        help='Date or date range for iteration (e.g., "2026-01-19" or "Jan 19-20")'
    )
    parser.add_argument(
        '--phase',
        help='Discovery phase name'
    )
    parser.add_argument(
        '--goals',
        help='Iteration goals (use semicolons to separate multiple goals)'
    )
    parser.add_argument(
        '--activities',
        help='Activities performed (optional)'
    )
    parser.add_argument(
        '--outcomes',
        help='Key outcomes (optional)'
    )
    parser.add_argument(
        '--questions-added',
        help='Questions added (e.g., "Q1-Q5" or "Q9, Q12") (optional)'
    )
    parser.add_argument(
        '--decisions-made',
        help='Decisions made (e.g., "D1, D2") (optional)'
    )
    parser.add_argument(
        '--research-conducted',
        help='Research conducted (e.g., "R1, R3") (optional)'
    )
    parser.add_argument(
        '--next-steps',
        help='Next steps (optional)'
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
            # Read from stdin: date_range|phase|goals|outcomes|questions_added|decisions_made|research_conducted|next_steps
            line = sys.stdin.read().strip()
            parts = line.split('|')
            if len(parts) < 3:
                print("ERROR: Pipe-separated input requires at least: date_range|phase|goals", file=sys.stderr)
                return 1

            date_range = parts[0]
            phase = parts[1]
            goals = parts[2]
            activities = parts[3] if len(parts) > 3 else None
            outcomes = parts[4] if len(parts) > 4 else None
            questions_added = parts[5] if len(parts) > 5 else None
            decisions_made = parts[6] if len(parts) > 6 else None
            research_conducted = parts[7] if len(parts) > 7 else None
            next_steps = parts[8] if len(parts) > 8 else None
        else:
            # Read from args
            if not args.date_range:
                print("ERROR: --date-range is required", file=sys.stderr)
                return 1
            if not args.phase:
                print("ERROR: --phase is required", file=sys.stderr)
                return 1
            if not args.goals:
                print("ERROR: --goals is required", file=sys.stderr)
                return 1

            date_range = args.date_range
            phase = args.phase
            goals = args.goals
            activities = args.activities
            outcomes = args.outcomes
            questions_added = args.questions_added
            decisions_made = args.decisions_made
            research_conducted = args.research_conducted
            next_steps = args.next_steps

        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Log iteration
        log_iteration(
            discovery_dir, date_range, phase, goals, activities,
            outcomes, questions_added, decisions_made,
            research_conducted, next_steps
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
