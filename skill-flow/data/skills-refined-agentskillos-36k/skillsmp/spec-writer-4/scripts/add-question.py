#!/usr/bin/env python3
"""
Add question to OPEN_QUESTIONS.md with auto-ID and category.

Usage:
    add-question.py --question "How should we handle X?" --category blocking --story 3
    add-question.py --question "What export formats?" --category clarifying

    # Pipe-separated for automation
    echo "How should we handle X?|blocking|Needed for Story 3|3" | add-question.py --from-stdin
"""

import sys
import argparse
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.id_manager import IDManager
from lib.file_operations import SafeFileOperations


# Category emoji mapping
CATEGORY_EMOJI = {
    'blocking': '🔴',
    'clarifying': '🟡',
    'research': '🔵',
    'watching': '🟠'
}

CATEGORY_HEADERS = {
    'blocking': '## 🔴 Blocking',
    'clarifying': '## 🟡 Clarifying',
    'research': '## 🔵 Research Pending',
    'watching': '## 🟠 Watching (May Affect Graduated)'
}


def add_question(discovery_dir: Path, question: str, category: str,
                context: str = None, story: str = None, blocking: str = None):
    """
    Add question to OPEN_QUESTIONS.md.

    Args:
        discovery_dir: Path to discovery/ directory
        question: Question text
        category: Category (blocking, clarifying, research, watching)
        context: Optional context explaining why needed
        story: Optional story number/reference
        blocking: Optional text describing what is blocked
    """
    # Get next question ID
    id_manager = IDManager(discovery_dir)
    question_id = id_manager.get_next_id('question')

    # Load OPEN_QUESTIONS.md
    questions_file = discovery_dir / 'OPEN_QUESTIONS.md'
    if not questions_file.exists():
        raise FileNotFoundError(f"File not found: {questions_file}")

    content = SafeFileOperations.read_file(questions_file)
    lines = content.split('\n')

    # Build question entry
    entry_lines = [f"- **{question_id}**: {question}"]
    if context:
        entry_lines.append(f"  - *Context*: {context}")
    if story:
        entry_lines.append(f"  - *Story*: Story {story}")
    if blocking:
        entry_lines.append(f"  - *Blocking*: {blocking}")

    # Find insertion point in correct category
    category_header = CATEGORY_HEADERS[category]
    insert_index = None

    for i, line in enumerate(lines):
        if line.strip() == category_header:
            # Find first empty line or next section after header
            for j in range(i + 1, len(lines)):
                # Skip subsection headers and example content in blocking
                if lines[j].strip().startswith('###'):
                    continue
                if lines[j].strip().startswith('[') or lines[j].strip().startswith('*'):
                    continue
                # Insert before next category or at next empty section
                if lines[j].strip().startswith('##') and lines[j].strip() != category_header:
                    insert_index = j
                    break
                if not lines[j].strip():
                    insert_index = j
                    break
            if insert_index is None:
                insert_index = len(lines)
            break

    if insert_index is None:
        raise ValueError(f"Category section not found: {category_header}")

    # Insert question entry
    for line in reversed(entry_lines):
        lines.insert(insert_index, line)

    # Add blank line after for spacing
    lines.insert(insert_index + len(entry_lines), '')

    # Write updated content
    updated_content = '\n'.join(lines)
    SafeFileOperations.write_file(questions_file, updated_content)

    print(f"✓ Added {question_id} to {category} category")
    print(f"  Question: {question}")
    if story:
        print(f"  Story: Story {story}")


def main():
    parser = argparse.ArgumentParser(
        description='Add question to OPEN_QUESTIONS.md'
    )
    parser.add_argument(
        '--question',
        help='Question text'
    )
    parser.add_argument(
        '--category',
        choices=['blocking', 'clarifying', 'research', 'watching'],
        help='Question category'
    )
    parser.add_argument(
        '--context',
        help='Context explaining why question is needed'
    )
    parser.add_argument(
        '--story',
        help='Story number this question relates to'
    )
    parser.add_argument(
        '--blocking',
        help='What this question is blocking'
    )
    parser.add_argument(
        '--from-stdin',
        action='store_true',
        help='Read pipe-separated input from stdin (question|category|context|story)'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Parse input
        if args.from_stdin:
            # Read from stdin: question|category|context|story
            line = sys.stdin.read().strip()
            parts = line.split('|')
            if len(parts) < 2:
                print("ERROR: Pipe-separated input requires at least: question|category", file=sys.stderr)
                return 1
            question = parts[0]
            category = parts[1]
            context = parts[2] if len(parts) > 2 else None
            story = parts[3] if len(parts) > 3 else None
            blocking = parts[4] if len(parts) > 4 else None
        else:
            # Read from args
            if not args.question or not args.category:
                print("ERROR: --question and --category are required", file=sys.stderr)
                return 1
            question = args.question
            category = args.category
            context = args.context
            story = args.story
            blocking = args.blocking

        # Validate category
        if category not in CATEGORY_EMOJI:
            print(f"ERROR: Invalid category: {category}", file=sys.stderr)
            print(f"Valid categories: {', '.join(CATEGORY_EMOJI.keys())}", file=sys.stderr)
            return 1

        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Add question
        add_question(discovery_dir, question, category, context, story, blocking)

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
