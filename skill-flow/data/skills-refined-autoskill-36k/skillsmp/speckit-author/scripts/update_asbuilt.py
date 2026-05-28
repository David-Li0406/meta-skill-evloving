#!/usr/bin/env python3
"""Update BMAD planning with as-built implementation details.

This script runs after a feature PR is merged to contrib branch. It:
1. Reads as-built specifications from specs/<slug>/
2. Compares with original BMAD planning from planning/<slug>/
3. Conducts interactive Q&A about deviations and metrics
4. Updates planning documents with "As-Built" sections
5. Commits changes to contrib branch

Usage:
    python .claude/skills/speckit-author/scripts/update_asbuilt.py \\
        <planning_dir> <specs_dir> [--todo-file <path>]

Example:
    # From main repo on contrib branch after PR merge
    python .claude/skills/speckit-author/scripts/update_asbuilt.py \\
        planning/my-feature specs/my-feature \\
        --todo-file TODO_feature_20251024_my-feature.md

Constants:
- TIMESTAMP_FORMAT: YYYY-MM-DD (for as-built dates)
  Rationale: Human-readable date format matching original planning docs
"""

import argparse
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Constants
TIMESTAMP_FORMAT = "%Y-%m-%d"  # Human-readable date for documentation


def error_exit(message: str, code: int = 1) -> None:
    """Print error message and exit."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def run_command(cmd: list[str], capture=True, check=True) -> str | None:
    """Run command and return output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check)
            return None
    except subprocess.CalledProcessError as e:
        if check:
            error_exit(f"Command failed: {' '.join(cmd)}\n{e.stderr}")
        return None


def ask_question(prompt: str, default: str | None = None) -> str:
    """Ask user a question."""
    if default:
        print(f"\n{prompt}")
        print(f"[default: {default}]")
    else:
        print(f"\n{prompt}")

    response = input("> ").strip()
    return response if response else (default or "")


def ask_multiline(prompt: str) -> str:
    """Ask for multiline input."""
    print(f"\n{prompt}")
    print("(Enter a blank line to finish)")

    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    return "\n".join(lines)


def analyze_deviations(planning_dir: Path, specs_dir: Path) -> list[dict[str, str]]:
    """Compare planning vs specs and identify deviations."""

    deviations = []

    # Read planning documents
    arch_path = planning_dir / "architecture.md"

    # Read specs
    spec_path = specs_dir / "spec.md"

    if not spec_path.exists():
        error_exit(f"Spec file not found: {spec_path}")

    spec_text = spec_path.read_text().lower()

    # Check for technology deviations (architecture.md)
    if arch_path.exists():
        arch_text = arch_path.read_text().lower()

        # Check common technology changes
        tech_checks = [
            ("redis", "cache"),
            ("websocket", "real-time"),
            ("grpc", "rpc"),
            ("graphql", "api"),
            ("rabbitmq", "message queue"),
            ("celery", "task queue"),
        ]

        for tech, category in tech_checks:
            in_arch = tech in arch_text
            in_spec = tech in spec_text

            if in_arch and not in_spec:
                deviations.append(
                    {
                        "category": "Technology",
                        "planned": f"{tech.upper()} for {category}",
                        "actual": f"Alternative approach (not using {tech.upper()})",
                        "file": "architecture.md",
                    }
                )

    # Note: More sophisticated analysis could be added here
    # For now, rely on user to identify deviations during Q&A

    return deviations


def gather_as_built_info(planning_dir: Path, specs_dir: Path, todo_file: Path | None) -> dict[str, any]:
    """Interactive Q&A to gather as-built information."""

    print("\n" + "=" * 70)
    print("As-Built Documentation Update")
    print("=" * 70)

    print(f"\nReading as-built specifications from: {specs_dir}/")
    print(f"Updating BMAD planning in: {planning_dir}/")

    info = {"date": datetime.now(UTC).strftime(TIMESTAMP_FORMAT), "specs_reference": f"specs/{specs_dir.name}/spec.md"}

    # Analyze automatic deviations
    deviations = analyze_deviations(planning_dir, specs_dir)

    if deviations:
        print(f"\n✓ Found {len(deviations)} potential deviations")

    # Ask about additional deviations
    print("\n" + "=" * 70)
    print("Deviations from Original Planning")
    print("=" * 70)

    info["deviations"] = []

    # Show auto-detected deviations first
    for dev in deviations:
        print(f"\nDetected deviation in {dev['file']}:")
        print(f"  Planned: {dev['planned']}")
        print(f"  As-Built: {dev['actual']}")

        reason = ask_question("Why was this changed?")

        info["deviations"].append({**dev, "reason": reason})

    # Ask about other deviations
    while True:
        has_more = input("\nAny other deviations from the plan? (y/N) > ").strip().lower()

        if has_more not in ["y", "yes"]:
            break

        category = ask_question("Category? (Functional/Technology/Design/Other)")
        planned = ask_question("What was planned?")
        actual = ask_question("What was actually implemented?")
        reason = ask_question("Why was this changed?")

        info["deviations"].append({"category": category, "planned": planned, "actual": actual, "reason": reason, "file": "requirements.md or architecture.md"})

    # Epic completion metrics
    print("\n" + "=" * 70)
    print("Epic Completion Metrics")
    print("=" * 70)

    epics_path = planning_dir / "epics.md"
    if epics_path.exists():
        epics_text = epics_path.read_text()
        epic_ids = re.findall(r"(E-\d+)", epics_text)

        info["epics"] = []

        for epic_id in set(epic_ids):  # unique epic IDs
            print(f"\n{epic_id}:")

            estimated_days = ask_question("  Estimated effort (days)?", default="Unknown")
            actual_days = ask_question("  Actual effort (days)?")
            notes = ask_question("  Notes/lessons learned?", default="")

            info["epics"].append({"id": epic_id, "estimated": estimated_days, "actual": actual_days, "notes": notes})

    # Quality metrics
    print("\n" + "=" * 70)
    print("Quality Metrics")
    print("=" * 70)

    info["metrics"] = {
        "test_coverage": ask_question("Final test coverage (%):", default="80"),
        "response_time": ask_question("Response time p95 (if applicable):", default="N/A"),
        "throughput": ask_question("Throughput (req/s, if applicable):", default="N/A"),
        "quality_gates": ask_question("All quality gates passing? (Y/n)", default="Y"),
    }

    # Lessons learned
    print("\n" + "=" * 70)
    print("Lessons Learned")
    print("=" * 70)

    info["lessons_learned"] = ask_multiline("Key lessons learned from this implementation?\n(What went well? What would you do differently?)")

    return info


def update_requirements_md(req_path: Path, info: dict[str, any]) -> None:
    """Append As-Built Notes section to requirements.md."""

    if not req_path.exists():
        print(f"⚠ Requirements file not found: {req_path}")
        return

    content = req_path.read_text()

    # Check if as-built section already exists
    if "## As-Built Notes" in content:
        print(f"⚠ As-Built Notes already exist in {req_path}")
        overwrite = input("  Overwrite? (y/N) > ").strip().lower()
        if overwrite not in ["y", "yes"]:
            return

        # Remove existing section
        content = re.sub(r"## As-Built Notes.*?(?=\n##|\Z)", "", content, flags=re.DOTALL)

    # Build as-built section
    as_built = "\n\n## As-Built Notes\n\n"
    as_built += f"**Implementation Date:** {info['date']}\n\n"
    as_built += f"**Final Implementation:** {info['specs_reference']}\n\n"

    if info["deviations"]:
        as_built += "### Deviations from Original Requirements\n\n"

        for dev in info["deviations"]:
            as_built += f"**{dev.get('category', 'Deviation')}:**\n"
            as_built += f"- **Planned:** {dev['planned']}\n"
            as_built += f"- **As-Built:** {dev['actual']}\n"
            as_built += f"- **Reason:** {dev['reason']}\n\n"

    if info.get("lessons_learned"):
        as_built += "### Lessons Learned\n\n"
        as_built += info["lessons_learned"] + "\n\n"

    # Append to file
    content += as_built
    req_path.write_text(content)

    print(f"✓ Updated {req_path}")


def update_architecture_md(arch_path: Path, info: dict[str, any]) -> None:
    """Append As-Built Architecture section to architecture.md."""

    if not arch_path.exists():
        print(f"⚠ Architecture file not found: {arch_path}")
        return

    content = arch_path.read_text()

    # Check if as-built section already exists
    if "## As-Built Architecture" in content:
        print(f"⚠ As-Built Architecture already exists in {arch_path}")
        overwrite = input("  Overwrite? (y/N) > ").strip().lower()
        if overwrite not in ["y", "yes"]:
            return

        # Remove existing section
        content = re.sub(r"## As-Built Architecture.*?(?=\n##|\Z)", "", content, flags=re.DOTALL)

    # Build as-built section
    as_built = "\n\n## As-Built Architecture\n\n"
    as_built += f"**Implemented:** {info['date']}\n\n"
    as_built += f"**Detailed Spec:** {info['specs_reference']}\n\n"

    # Technology deviations
    tech_deviations = [d for d in info["deviations"] if d.get("category") == "Technology"]
    if tech_deviations:
        as_built += "### Technology Stack (Final)\n\n"
        as_built += "Matches planned architecture with these changes:\n\n"

        for dev in tech_deviations:
            as_built += f"- ~~{dev['planned']}~~ → {dev['actual']}\n"
            as_built += f"  - Reason: {dev['reason']}\n"

        as_built += "\n"

    # Performance metrics
    if info["metrics"]:
        as_built += "### Performance Metrics (Actual)\n\n"

        if info["metrics"]["response_time"] != "N/A":
            as_built += f"- Response time p95: {info['metrics']['response_time']}\n"

        if info["metrics"]["throughput"] != "N/A":
            as_built += f"- Throughput: {info['metrics']['throughput']}\n"

        as_built += f"- Test coverage: {info['metrics']['test_coverage']}%\n"
        as_built += f"- Quality gates: {info['metrics']['quality_gates']}\n\n"

    # Append to file
    content += as_built
    arch_path.write_text(content)

    print(f"✓ Updated {arch_path}")


def update_epics_md(epics_path: Path, info: dict[str, any]) -> None:
    """Append Epic Completion Status to epics.md."""

    if not epics_path.exists():
        print(f"⚠ Epics file not found: {epics_path}")
        return

    content = epics_path.read_text()

    # Check if completion section already exists
    if "## Epic Completion Status" in content:
        print(f"⚠ Epic Completion Status already exists in {epics_path}")
        overwrite = input("  Overwrite? (y/N) > ").strip().lower()
        if overwrite not in ["y", "yes"]:
            return

        # Remove existing section
        content = re.sub(r"## Epic Completion Status.*?(?=\n##|\Z)", "", content, flags=re.DOTALL)

    # Build completion section
    completion = "\n\n## Epic Completion Status\n\n"

    if info.get("epics"):
        for epic in info["epics"]:
            completion += f"### {epic['id']} (COMPLETED)\n"
            completion += f"- **Status:** ✓ Completed {info['date']}\n"
            completion += f"- **Estimated effort:** {epic['estimated']}\n"
            completion += f"- **Actual effort:** {epic['actual']}\n"

            if epic["notes"]:
                completion += f"- **Notes:** {epic['notes']}\n"

            completion += "\n"

    # Lessons learned for future epics
    if info.get("lessons_learned"):
        completion += "## Lessons Learned for Future Epics\n\n"
        completion += info["lessons_learned"] + "\n\n"

    # Append to file
    content += completion
    epics_path.write_text(content)

    print(f"✓ Updated {epics_path}")


def commit_changes(planning_dir: Path, specs_dir: Path) -> None:
    """Commit as-built updates."""

    # Git add planning directory
    run_command(["git", "add", str(planning_dir)])

    # Create commit message
    commit_msg = f"""docs(planning): add as-built details for {planning_dir.name}

Updated BMAD planning with implementation details:
- requirements.md: As-Built Notes (deviations, lessons learned)
- architecture.md: As-Built Architecture (tech stack, metrics)
- epics.md: Epic Completion Status (effort, outcomes)

Refs: {specs_dir}/spec.md
"""

    run_command(["git", "commit", "-m", commit_msg])

    print("\n✓ Committed as-built updates")


def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(description="Update BMAD planning with as-built implementation details")
    parser.add_argument("planning_dir", type=Path, help="Planning directory (e.g., planning/my-feature)")
    parser.add_argument("specs_dir", type=Path, help="Specs directory (e.g., specs/my-feature)")
    parser.add_argument("--todo-file", type=Path, help="Optional TODO file for reference")
    parser.add_argument("--no-commit", action="store_true", help="Skip git commit (for testing)")

    args = parser.parse_args()

    # Validate directories
    if not args.planning_dir.exists():
        error_exit(f"Planning directory not found: {args.planning_dir}")

    if not args.specs_dir.exists():
        error_exit(f"Specs directory not found: {args.specs_dir}")

    # Gather as-built information
    info = gather_as_built_info(args.planning_dir, args.specs_dir, args.todo_file)

    # Update planning documents
    print("\n" + "=" * 70)
    print("Updating Planning Documents")
    print("=" * 70)

    update_requirements_md(args.planning_dir / "requirements.md", info)
    update_architecture_md(args.planning_dir / "architecture.md", info)
    update_epics_md(args.planning_dir / "epics.md", info)

    # Commit changes
    if not args.no_commit:
        commit_changes(args.planning_dir, args.specs_dir)
    else:
        print("\n⚠ Skipping commit (--no-commit flag)")

    # Summary
    print("\n" + "=" * 70)
    print("As-Built Documentation Complete!")
    print("=" * 70)

    print("\nUpdated files:")
    print(f"  - {args.planning_dir}/requirements.md")
    print(f"  - {args.planning_dir}/architecture.md")
    print(f"  - {args.planning_dir}/epics.md")

    print(f"\nDeviations documented: {len(info['deviations'])}")
    if info.get("epics"):
        print(f"Epics completed: {len(info['epics'])}")

    print("\nThese updates will improve future planning accuracy!")
    print("")


if __name__ == "__main__":
    main()
