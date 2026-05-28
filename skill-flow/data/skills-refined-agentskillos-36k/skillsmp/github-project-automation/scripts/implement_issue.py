#!/usr/bin/env python3
"""
Orchestrate full issue implementation workflow
Usage: python3 implement_issue.py ISSUE_NUMBER
       python3 implement_issue.py --auto-select [--priority critical] [--epic payment]
"""

import json
import subprocess
import sys
import argparse
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def run_command(cmd: str | list, check: bool = True) -> dict:
    """Run command and return result"""
    if isinstance(cmd, str):
        cmd = cmd.split()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode
        }

def fetch_issue(issue_number: int) -> dict:
    """Fetch issue details"""
    print(f"📥 Fetching issue #{issue_number}...")

    result = run_command([
        "python3",
        str(SCRIPT_DIR / "fetch_issue.py"),
        str(issue_number)
    ])

    if not result["success"]:
        print(f"❌ Failed to fetch issue: {result['stderr']}")
        sys.exit(1)

    issue = json.loads(result["stdout"])
    print(f"✅ Fetched: {issue['title']}")
    print(f"   Epic: {issue['epic']}, Priority: {issue['priority']}, Status: {issue['status']}")
    print()

    return issue

def select_issue(priority: str = None, epic: str = None) -> int:
    """Auto-select next issue"""
    print("🔍 Auto-selecting next issue...")

    cmd = ["python3", str(SCRIPT_DIR / "select_issue.py")]
    if priority:
        cmd.extend(["--priority", priority])
    if epic:
        cmd.extend(["--epic", epic])

    result = run_command(cmd)

    if not result["success"]:
        print(f"❌ No suitable issue found")
        sys.exit(1)

    issue_number = int(result["stdout"].strip())
    return issue_number

def slugify(text: str) -> str:
    """Convert text to URL slug"""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text[:50]  # Limit length

def create_feature_branch(issue: dict) -> str:
    """Create feature branch for issue"""
    # Detect commit type from issue title/labels
    issue_type = issue.get("type", "feature")
    if issue_type == "bug":
        prefix = "fix"
    elif issue_type == "docs":
        prefix = "docs"
    elif issue_type == "tech-debt":
        prefix = "refactor"
    else:
        prefix = "feat"

    branch_name = f"{prefix}/issue-{issue['number']}-{slugify(issue['title'])}"

    print(f"🌿 Creating feature branch: {branch_name}")

    # Check if branch already exists
    result = run_command(f"git rev-parse --verify {branch_name}", check=False)
    if result["success"]:
        print(f"⚠️  Branch already exists. Checking out...")
        run_command(f"git checkout {branch_name}")
    else:
        run_command(f"git checkout -b {branch_name}")

    print(f"✅ On branch: {branch_name}")
    print()

    return branch_name

def generate_plan_prompt(issue: dict) -> str:
    """Generate context analysis prompt for the issue"""

    # Epic-specific context templates
    EPIC_CONTEXTS = {
        "booking-payment": "payment/booking actions, Stripe integration, database models (payment, booking, payout)",
        "authentication": "Better Auth config, auth utilities, session management, protected routes",
        "onboarding": "onboarding flows, profile creation, document upload, verification workflow",
        "instructor-features": "instructor dashboard, availability, pricing, vehicle management",
        "learner-features": "learner dashboard, booking flow, instructor search",
        "admin": "admin verification queue, user management, platform analytics",
        "messaging": "message threads, notifications, email triggers",
        "reviews": "review writing, rating display, moderation",
        "search": "geospatial search, PostGIS, filtering, sorting",
        "infrastructure": "testing, CI/CD, monitoring, deployment",
        "ui-ux": "components, themes, responsive design, accessibility"
    }

    epic = issue.get("epic", "")
    context_hint = EPIC_CONTEXTS.get(epic, "relevant code and patterns")

    criteria_text = "\n".join(
        f"  - {'[x]' if c['checked'] else '[ ]'} {c['text']}"
        for c in issue.get("acceptance_criteria", [])
    )

    prompt = f"""
# Issue Implementation Context Analysis

**Issue #{issue['number']}:** {issue['title']}

**Epic:** {epic or 'Not specified'}
**Priority:** {issue.get('priority', 'Not specified')}
**Status:** {issue.get('status', 'Not specified')}

## Acceptance Criteria
{criteria_text or '  (No acceptance criteria found)'}

## Required Analysis

Analyze the codebase to understand how to implement this issue:

1. **Find relevant files:** Locate existing code related to {context_hint}
2. **Identify patterns:** Find similar implementations to follow
3. **Check dependencies:** Determine what libraries/services are needed
4. **Review tests:** Check existing test patterns and coverage

Focus areas based on epic '{epic}':
- Existing implementations in this area
- Database models and schemas
- Server actions and API routes
- UI components (if applicable)
- Test files and patterns

## Expected Output

Provide:
- **Files to modify** (with brief reason for each)
- **Files to create** (if any)
- **Existing patterns to follow** (with file references)
- **Dependencies required** (libraries, services)
- **Similar implementations** (for reference)

This analysis will be used to generate the implementation plan.
"""

    return prompt

def main():
    parser = argparse.ArgumentParser(
        description="Implement GitHub issue with full automation"
    )

    # Issue selection
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "issue_number",
        nargs="?",
        type=int,
        help="Specific issue number to implement"
    )
    group.add_argument(
        "--auto-select",
        action="store_true",
        help="Auto-select next issue by priority"
    )

    # Auto-select filters
    parser.add_argument(
        "--priority",
        choices=["critical", "high", "medium", "low"],
        help="Priority filter for auto-select"
    )
    parser.add_argument(
        "--epic",
        help="Epic filter for auto-select (e.g., 'booking-payment')"
    )

    # Workflow options
    parser.add_argument(
        "--skip-branch",
        action="store_true",
        help="Skip branch creation (use current branch)"
    )
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Generate plan and stop (don't implement)"
    )

    args = parser.parse_args()

    print("🤖 GitHub Issue Implementation Automation")
    print("=" * 60)
    print()

    # Step 1: Select issue
    if args.auto_select:
        issue_number = select_issue(args.priority, args.epic)
    else:
        issue_number = args.issue_number

    # Step 2: Fetch issue details
    issue = fetch_issue(issue_number)

    # Step 3: Create feature branch (unless skipped)
    if not args.skip_branch:
        branch_name = create_feature_branch(issue)
    else:
        print("⏭️  Skipping branch creation (using current branch)")
        print()

    # Step 4: Generate context analysis prompt
    print("📋 Generating context analysis prompt...")
    context_prompt = generate_plan_prompt(issue)

    # Save prompt to file for Claude Code to use
    prompt_file = Path(f"docs/plans/issue-{issue_number}-context-prompt.md")
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(context_prompt)

    print(f"✅ Context prompt saved to: {prompt_file}")
    print()

    # Step 5: Instructions for Claude Code
    print("=" * 60)
    print("📝 NEXT STEPS (for Claude Code)")
    print("=" * 60)
    print()
    print(f"1. Read the context prompt: {prompt_file}")
    print()
    print("2. Use the Task tool with Explore agent:")
    print(f"   - Paste the prompt from {prompt_file}")
    print("   - Agent will analyze codebase and return context")
    print()
    print("3. Generate implementation plan:")
    print("   - Use superpowers:writing-plans skill")
    print(f"   - Save to: docs/plans/issue-{issue_number}-implementation-plan.md")
    print()
    print("4. Wait for USER APPROVAL of plan")
    print()
    print("5. After approval, implement:")
    print("   - Use superpowers:test-driven-development skill")
    print("   - Follow TDD workflow (tests first)")
    print("   - Run quality gates (tests, types, lint)")
    print()
    print("6. Create commit and PR:")
    print("   - Follow CLAUDE.md git workflow")
    print(f"   - Commit message: 'feat: {issue['title']}'")
    print(f"   - Include 'Closes #{issue_number}' in message")
    print("   - Create PR with test plan")
    print()
    print("=" * 60)

    if args.plan_only:
        print("✅ Plan-only mode: Stopping here")
        print(f"   Review prompt at: {prompt_file}")
        sys.exit(0)

    # Return issue data for programmatic use
    return issue

if __name__ == "__main__":
    main()
