#!/usr/bin/env python3
"""
Graduate story from STATE.md to SPEC.md.

This script moves a story from "In Progress" in STATE.md to the graduated SPEC.md,
performing validation and maintaining proper formatting.

Usage:
    graduate-story.py --story-number 3
    graduate-story.py --story-number 3 --dry-run
"""

import sys
import argparse
import re
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.file_operations import SafeFileOperations
from lib.spec_parser import SpecParser


def validate_story_ready(state_content: str, story_num: int) -> tuple:
    """
    Validate story is ready for graduation.

    Returns:
        Tuple of (is_ready: bool, errors: list)
    """
    errors = []

    # Check story is marked as "In Progress"
    story_table_pattern = re.compile(
        rf'^\| {story_num} \|.*?\| 🔄 In Progress \|',
        re.MULTILINE
    )
    if not story_table_pattern.search(state_content):
        errors.append(f"Story {story_num} is not marked as 'In Progress' in STATE.md")

    # Check for In-Progress Story Detail section
    if f'### Story {story_num}:' not in state_content and \
       f'## In-Progress Story Detail' not in state_content:
        errors.append(f"Story {story_num} details not found in STATE.md")

    return (len(errors) == 0, errors)


def extract_story_from_state(state_content: str, story_num: int) -> dict:
    """
    Extract story details from STATE.md In-Progress Story Detail.

    Returns:
        Dict with story details
    """
    story = {
        'number': story_num,
        'title': '',
        'priority': 'P1',
        'description': '',
        'scenarios': [],
        'decisions': [],
        'research': []
    }

    # Find In-Progress Story Detail section
    section_pattern = re.compile(
        r'## In-Progress Story Detail\s*\n\s*###\s*Story\s*(\d+):\s*(.+?)\s*\(Priority:\s*(P\d+)\)',
        re.MULTILINE | re.DOTALL
    )
    match = section_pattern.search(state_content)

    if match and int(match.group(1)) == story_num:
        story['title'] = match.group(2).strip()
        story['priority'] = match.group(3)

        # Extract section content
        start = match.end()
        next_section = re.search(r'\n##\s+', state_content[start:])
        end = start + next_section.start() if next_section else len(state_content)
        section_content = state_content[start:end]

        # Extract scenarios
        scenarios_pattern = re.compile(
            r'\*\*Draft Acceptance Scenarios\*\*:(.*?)(?=\*\*|$)',
            re.DOTALL
        )
        scenarios_match = scenarios_pattern.search(section_content)
        if scenarios_match:
            scenarios_text = scenarios_match.group(1).strip()
            # Parse numbered scenarios
            scenario_items = re.findall(
                r'(\d+)\.\s*\*\*Given\*\*\s+(.+?)\s+\*\*When\*\*\s+(.+?)\s+\*\*Then\*\*\s+(.+?)(?=\n\s*-|\n\d+\.|$)',
                scenarios_text,
                re.DOTALL
            )
            for num, given, when, then in scenario_items:
                story['scenarios'].append({
                    'given': given.strip(),
                    'when': when.strip(),
                    'then': then.strip()
                })

    return story


def format_story_for_spec(story: dict) -> str:
    """
    Format story for SPEC.md.

    Args:
        story: Story dict

    Returns:
        Formatted story markdown
    """
    lines = []

    # Header
    lines.append(f"### User Story {story['number']} - {story['title']} (Priority: {story['priority']})")
    lines.append("")
    lines.append(f"**Revision**: v1.0")
    lines.append("")

    # Description
    if story.get('description'):
        lines.append(story['description'])
        lines.append("")

    # Acceptance Scenarios
    if story['scenarios']:
        lines.append("**Acceptance Scenarios**:")
        lines.append("")
        for i, scenario in enumerate(story['scenarios'], 1):
            lines.append(f"{i}. **Given** {scenario['given']}, **When** {scenario['when']}, **Then** {scenario['then']}")
        lines.append("")

    # Supporting Decisions (if any)
    if story.get('decisions'):
        lines.append("<details>")
        lines.append("<summary>Supporting Decisions</summary>")
        lines.append("")
        for decision_id in story['decisions']:
            lines.append(f"- **{decision_id}**: [Summary TBD]")
        lines.append("")
        lines.append("*Full context: `discovery/archive/DECISIONS.md`*")
        lines.append("</details>")
        lines.append("")

    lines.append("---")
    lines.append("")

    return '\n'.join(lines)


def graduate_story(discovery_dir: Path, story_num: int, dry_run: bool = False):
    """
    Graduate story from STATE.md to SPEC.md.

    Args:
        discovery_dir: Path to discovery/ directory
        story_num: Story number to graduate
        dry_run: If True, show changes without applying
    """
    # Load files
    state_file = discovery_dir / 'STATE.md'
    spec_file = discovery_dir / 'SPEC.md'

    if not state_file.exists():
        raise FileNotFoundError(f"STATE.md not found")
    if not spec_file.exists():
        raise FileNotFoundError(f"SPEC.md not found")

    state_content = SafeFileOperations.read_file(state_file)
    spec_content = SafeFileOperations.read_file(spec_file)

    # Validate story is ready
    is_ready, errors = validate_story_ready(state_content, story_num)
    if not is_ready:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise ValueError("Story not ready for graduation")

    # Extract story from STATE.md
    story = extract_story_from_state(state_content, story_num)

    if not story['title']:
        raise ValueError(f"Could not extract story {story_num} from STATE.md")

    # Format story for SPEC.md
    story_markdown = format_story_for_spec(story)

    if dry_run:
        print("DRY RUN - Would add the following to SPEC.md:")
        print("")
        print(story_markdown)
        print("")
        print(f"Would update Story {story_num} status to '✅ In SPEC' in STATE.md")
        return

    # Insert into SPEC.md in User Scenarios & Testing section
    # Find insertion point (after section header or after last story)
    scenarios_section_pattern = re.compile(
        r'(## User Scenarios & Testing.*?)((?=\n## )|$)',
        re.DOTALL
    )
    match = scenarios_section_pattern.search(spec_content)

    if match:
        section_start = match.start(1)
        section_end = match.end(1)

        # Insert story before next section
        before = spec_content[:section_end]
        after = spec_content[section_end:]

        # Find where to insert based on priority
        # For now, just append to end of section
        if not after.strip().startswith('---'):
            before += '\n'

        updated_spec = before + story_markdown + after
    else:
        raise ValueError("Could not find '## User Scenarios & Testing' section in SPEC.md")

    # Update Last Updated date in SPEC.md
    date_today = datetime.now().strftime('%Y-%m-%d')
    updated_spec = re.sub(
        r'\*\*Last Updated\*\*:\s*\d{4}-\d{2}-\d{2}',
        f'**Last Updated**: {date_today}',
        updated_spec
    )

    # Write updated SPEC.md
    SafeFileOperations.write_file(spec_file, updated_spec)

    # Update STATE.md story status
    state_lines = state_content.split('\n')
    for i, line in enumerate(state_lines):
        if line.strip().startswith(f'| {story_num} |'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if len(cells) >= 4:
                cells[3] = '✅ In SPEC'
                cells[4] = '100%'  # Set confidence to 100%
                state_lines[i] = '| ' + ' | '.join(cells) + ' |'
            break

    updated_state = '\n'.join(state_lines)
    SafeFileOperations.write_file(state_file, updated_state)

    print(f"✓ Graduated Story {story_num}: {story['title']}")
    print(f"  Priority: {story['priority']}")
    print(f"  Scenarios: {len(story['scenarios'])}")
    print(f"  Updated SPEC.md and STATE.md")


def main():
    parser = argparse.ArgumentParser(
        description='Graduate story from STATE.md to SPEC.md'
    )
    parser.add_argument(
        '--story-number',
        type=int,
        required=True,
        help='Story number to graduate'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show changes without applying them'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Graduate story
        graduate_story(discovery_dir, args.story_number, args.dry_run)

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
