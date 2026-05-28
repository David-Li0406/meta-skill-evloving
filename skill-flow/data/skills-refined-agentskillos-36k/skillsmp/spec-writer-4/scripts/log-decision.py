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

    # JSON input (RECOMMENDED for LLMs - avoids encoding issues)
    cat > /tmp/decision.json <<'EOF'
    {
      "title": "Use JWT authentication",
      "context": "Need secure auth for API",
      "decision": "Implement JWT with RS256",
      "stories": [1, 3],
      "questions": ["Q12", "Q15"]
    }
    EOF
    cat /tmp/decision.json | log-decision.py --from-json

    # Or with file reference
    log-decision.py --json-file /tmp/decision.json

    # Pipe-separated input (legacy - use JSON instead)
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
from lib.json_validator import JSONValidator
from lib.error_messages import ErrorMessages
from lib.validators import validate_story_exists, validate_question_exists


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
        help='Read pipe-separated input from stdin (legacy - use --from-json instead)'
    )
    parser.add_argument(
        '--from-json',
        action='store_true',
        help='Read JSON from stdin (RECOMMENDED for LLMs)'
    )
    parser.add_argument(
        '--json-file',
        help='Read JSON from file path'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Parse input with priority: JSON file > JSON stdin > pipe stdin > args
        if args.json_file:
            # Read JSON from file
            data, error = JSONValidator.load_json_from_file(args.json_file)
            if error:
                print(ErrorMessages.stdin_json_parse_error(error, args.json_file), file=sys.stderr)
                return 1

            # Validate against schema
            normalized, errors = JSONValidator.validate_and_normalize(data, 'decision')
            if errors:
                print(ErrorMessages.json_schema_validation_error(errors, 'schemas/decision-input.json'), file=sys.stderr)
                return 1

            # Extract fields
            title = normalized.get('title')
            context = normalized.get('context')
            question = normalized.get('question')
            options = normalized.get('options_considered')  # Note: schema uses "options_considered"
            decision = normalized.get('decision')
            rationale = normalized.get('rationale')
            implications = normalized.get('implications')
            stories = normalized.get('stories')
            questions = normalized.get('questions')

        elif args.from_json:
            # Read JSON from stdin
            data, error = JSONValidator.load_json_from_stdin()
            if error:
                content = sys.stdin.read() if not error.startswith("Empty") else ""
                print(ErrorMessages.stdin_json_parse_error(error, content), file=sys.stderr)
                return 1

            # Validate against schema
            normalized, errors = JSONValidator.validate_and_normalize(data, 'decision')
            if errors:
                print(ErrorMessages.json_schema_validation_error(errors, 'schemas/decision-input.json'), file=sys.stderr)
                return 1

            # Extract fields
            title = normalized.get('title')
            context = normalized.get('context')
            question = normalized.get('question')
            options = normalized.get('options_considered')  # Note: schema uses "options_considered"
            decision = normalized.get('decision')
            rationale = normalized.get('rationale')
            implications = normalized.get('implications')
            stories = normalized.get('stories')
            questions = normalized.get('questions')

        elif args.from_stdin:
            # Read from stdin: title|context|options|decision|rationale|implications|stories|questions
            line = sys.stdin.read().strip()
            parts = line.split('|')
            if len(parts) < 2:
                expected = ['title', 'context', '[options]', '[decision]', '[rationale]', '[implications]', '[stories]', '[questions]']
                example = "Use JWT|Need auth|JWT,OAuth2|Use JWT|Simpler|Must handle refresh|Story 1,Story 3|Q12,Q15"
                print(ErrorMessages.pipe_input_format_error(expected, len(parts), example), file=sys.stderr)
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
                print(ErrorMessages.missing_required_field('title', 'log-decision.py'), file=sys.stderr)
                return 1

            if not args.context:
                print(ErrorMessages.missing_required_field('context', 'log-decision.py'), file=sys.stderr)
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

        # Validate cross-references (warnings only - don't block)
        id_manager = IDManager(discovery_dir)

        # Validate story references
        if stories:
            # Extract story numbers from "Story 1, Story 3" format
            import re
            story_nums = re.findall(r'Story\s+(\d+)', stories, re.IGNORECASE)
            for story_num_str in story_nums:
                story_num = int(story_num_str)
                exists, suggestions = validate_story_exists(story_num, discovery_dir)
                if not exists:
                    print(f"⚠️  WARNING: Story {story_num} not found in STATE.md", file=sys.stderr)
                    if suggestions:
                        print(f"    Did you mean one of: {', '.join(map(str, suggestions))}?", file=sys.stderr)

        # Validate question references
        if questions:
            # Split question IDs (already normalized earlier in the flow)
            question_ids = [q.strip() for q in questions.split(',')]
            for question_id in question_ids:
                if question_id:  # Skip empty strings
                    exists, suggestions = validate_question_exists(question_id, discovery_dir, id_manager)
                    if not exists:
                        print(f"⚠️  WARNING: Question {question_id} not found in OPEN_QUESTIONS.md", file=sys.stderr)
                        if suggestions:
                            print(f"    Did you mean one of: {', '.join(suggestions)}?", file=sys.stderr)

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
