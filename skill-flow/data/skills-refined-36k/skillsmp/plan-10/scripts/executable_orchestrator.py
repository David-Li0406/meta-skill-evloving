#!/usr/bin/env python3
"""
Plan Orchestrator - Manages multi-phase project execution with memory optimization.

This script provides utilities for:
- Creating and initializing plan structures
- Tracking phase progress in CURRENT_PLAN.md
- Managing phase transitions with memory isolation
- Resuming interrupted plans
"""

import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# Configuration constants
DEFAULT_PHASES = ["research", "planning", "revision", "building", "validation", "cleanup"]
MAX_PLAN_SIZE_MB = 5
PLAN_FILE_NAME = "CURRENT_PLAN.md"
PLANS_DIR_NAME = ".plans"
KB_DIR_NAME = "knowledge-base"

# Pre-compile regex patterns for performance
JSON_METADATA_PATTERN = re.compile(r'```json\n(.*?)\n```', re.DOTALL)
PHASE_TITLE_PATTERN_TEMPLATE = r'(### \d+\. {}) .*?\n'
OUTPUTS_PATTERN_TEMPLATE = r'(### \d+\. {}.*?\*\*Outputs:\*\*\n)- None yet'


class PlanOrchestrator:
    """Manages plan lifecycle and phase transitions."""

    def __init__(self, working_dir: str = ".", enable_timing: bool = False):
        self.working_dir = Path(working_dir).resolve()
        self.plan_file = self.working_dir / PLAN_FILE_NAME
        self.plans_dir = self.working_dir / PLANS_DIR_NAME
        self.knowledge_base_dir = self.plans_dir / KB_DIR_NAME
        self.enable_timing = enable_timing
        self._timing_data = []

    def _time_operation(self, operation_name: str):
        """Context manager for timing operations."""
        class Timer:
            def __init__(self, name, timing_data, enabled):
                self.name = name
                self.timing_data = timing_data
                self.enabled = enabled
                self.start = None

            def __enter__(self):
                if self.enabled:
                    self.start = time.perf_counter()
                return self

            def __exit__(self, *args):
                if self.enabled and self.start:
                    duration = time.perf_counter() - self.start
                    self.timing_data.append((self.name, duration))

        return Timer(operation_name, self._timing_data, self.enable_timing)

    def initialize_plan(self, goal: str, phases: Optional[List[str]] = None) -> None:
        """Initialize a new plan structure."""
        with self._time_operation("initialize_plan"):
            phase_list = phases or DEFAULT_PHASES

            # Validate goal is not empty
            if not goal or not goal.strip():
                raise ValueError("Goal cannot be empty")

            # Create directories
            self.plans_dir.mkdir(exist_ok=True)
            self.knowledge_base_dir.mkdir(exist_ok=True)

            # Create phase directories
            for phase in phase_list:
                (self.plans_dir / phase).mkdir(exist_ok=True)

            # Initialize CURRENT_PLAN.md
            plan_content = self._generate_plan_template(goal, phase_list)
            self.plan_file.write_text(plan_content)

            # Add to .gitignore if in git repo
            self._update_gitignore()

            print(f"✅ Plan initialized at {self.working_dir}")
            print(f"   Goal: {goal}")
            print(f"   Phases: {', '.join(phase_list)}")

            self._print_timing()

    def _generate_plan_template(self, goal: str, phases: List[str]) -> str:
        """Generate the CURRENT_PLAN.md template."""
        timestamp = datetime.now().isoformat()

        template = f"""<!--
META: PLAN_IN_PROGRESS
If you are a new Claude instance reading this file, use the `plan` skill to resume this plan.
Command: Use the Skill tool with skill="plan" to continue from the current phase.
-->

# Current Plan

**Goal:** {goal}

**Status:** In Progress
**Current Phase:** {phases[0]}
**Created:** {timestamp}
**Last Updated:** {timestamp}

---

## Plan Metadata

```json
{{
  "goal": "{goal}",
  "phases": {json.dumps(phases)},
  "current_phase": "{phases[0]}",
  "current_phase_index": 0,
  "completed_phases": [],
  "started": "{timestamp}",
  "last_updated": "{timestamp}"
}}
```

---

## Phase Progress

"""

        for i, phase in enumerate(phases):
            status = "⏳ Current" if i == 0 else "⏸️ Pending"
            template += f"### {i+1}. {phase.title()} {status}\n\n"
            template += f"**Plan File:** `.plans/{phase}/plan.md`\n\n"
            template += "**Status:** Not started\n\n"
            template += "**Outputs:**\n- None yet\n\n"
            template += "---\n\n"

        template += """
## Phase Transition Protocol

When transitioning between phases:

1. **Complete Current Phase**
   - Finalize all outputs in `.plans/<phase>/`
   - Update phase status and outputs in this file
   - Mark phase as completed in metadata

2. **Prepare Next Phase**
   - Read next phase plan from `.plans/<next_phase>/plan.md`
   - Review only essential outputs from previous phases
   - Do NOT load full context from previous phases

3. **Update Plan File**
   - Update current_phase in metadata
   - Add completed phase to completed_phases
   - Update last_updated timestamp
   - Update phase progress section

---

## Notes

- Each phase should maintain its own isolated context in `.plans/<phase>/`
- Phase outputs should be clearly defined and minimal
- Use knowledge-base for research artifacts that multiple phases may reference
- Avoid loading unnecessary context between phases
"""

        return template

    def _update_gitignore(self) -> None:
        """Add plan files to .gitignore if in a git repository."""
        git_dir = self.working_dir / ".git"
        if not git_dir.exists():
            return

        gitignore = self.working_dir / ".gitignore"
        entries = ["CURRENT_PLAN.md", ".plans/"]

        existing_content = ""
        if gitignore.exists():
            existing_content = gitignore.read_text()

        needs_update = False
        for entry in entries:
            if entry not in existing_content:
                needs_update = True
                break

        if needs_update:
            with gitignore.open("a") as f:
                if existing_content and not existing_content.endswith("\n"):
                    f.write("\n")
                f.write("\n# Plan skill files\n")
                for entry in entries:
                    if entry not in existing_content:
                        f.write(f"{entry}\n")

            print("✅ Updated .gitignore with plan files")

    def get_current_state(self) -> Dict:
        """Extract current plan state from CURRENT_PLAN.md."""
        with self._time_operation("get_current_state"):
            if not self.plan_file.exists():
                raise FileNotFoundError("No CURRENT_PLAN.md found")

            # Check file size
            file_size_mb = self.plan_file.stat().st_size / (1024 * 1024)
            if file_size_mb > MAX_PLAN_SIZE_MB:
                print(f"⚠️  Warning: CURRENT_PLAN.md is {file_size_mb:.2f}MB (limit: {MAX_PLAN_SIZE_MB}MB)")
                print("   Consider splitting phases or reducing detail in outputs")

            content = self.plan_file.read_text()

            # Extract JSON metadata using pre-compiled pattern
            json_match = JSON_METADATA_PATTERN.search(content)
            if not json_match:
                raise ValueError("Could not find metadata in CURRENT_PLAN.md")

            try:
                metadata = json.loads(json_match.group(1))
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON metadata in CURRENT_PLAN.md: {e}")

            self._print_timing()
            return metadata

    def update_phase(self, phase: str, status: str, outputs: Optional[List[str]] = None) -> None:
        """Update the status of a specific phase."""
        with self._time_operation("update_phase"):
            if not self.plan_file.exists():
                raise FileNotFoundError("No CURRENT_PLAN.md found")

            with self._time_operation("read_plan_file"):
                content = self.plan_file.read_text()

            # Get current metadata without re-reading file
            with self._time_operation("extract_metadata"):
                json_match = JSON_METADATA_PATTERN.search(content)
                if not json_match:
                    raise ValueError("Could not find metadata in CURRENT_PLAN.md")
                metadata = json.loads(json_match.group(1))

            # Update metadata
            with self._time_operation("update_metadata"):
                if status == "completed":
                    if phase not in metadata["completed_phases"]:
                        metadata["completed_phases"].append(phase)

                    # Move to next phase
                    current_idx = metadata["current_phase_index"]
                    if current_idx + 1 < len(metadata["phases"]):
                        metadata["current_phase_index"] = current_idx + 1
                        metadata["current_phase"] = metadata["phases"][current_idx + 1]

                metadata["last_updated"] = datetime.now().isoformat()

            # Update JSON in content using pre-compiled pattern
            with self._time_operation("update_json"):
                json_str = json.dumps(metadata, indent=2)
                content = JSON_METADATA_PATTERN.sub(
                    f'```json\n{json_str}\n```',
                    content
                )

            # Update phase section using dynamic pattern
            with self._time_operation("update_phase_status"):
                phase_pattern = PHASE_TITLE_PATTERN_TEMPLATE.format(re.escape(phase.title()))
                if status == "completed":
                    content = re.sub(phase_pattern, rf'\1 ✅ Completed\n', content)
                elif status == "in_progress":
                    content = re.sub(phase_pattern, rf'\1 ⏳ Current\n', content)

            # Update outputs if provided
            if outputs:
                with self._time_operation("update_outputs"):
                    outputs_text = "\n".join(f"- {output}" for output in outputs)
                    outputs_pattern = OUTPUTS_PATTERN_TEMPLATE.format(re.escape(phase.title()))
                    content = re.sub(
                        outputs_pattern,
                        rf'\1{outputs_text}',
                        content,
                        flags=re.DOTALL
                    )

            with self._time_operation("write_plan_file"):
                self.plan_file.write_text(content)

            print(f"✅ Updated phase: {phase} -> {status}")
            self._print_timing()

    def cleanup(self) -> None:
        """Remove all plan files after completion."""
        import shutil

        with self._time_operation("cleanup"):
            if self.plans_dir.exists():
                shutil.rmtree(self.plans_dir)
                print(f"✅ Removed {self.plans_dir}")

            if self.plan_file.exists():
                self.plan_file.unlink()
                print(f"✅ Removed {self.plan_file}")

            print("✅ Plan cleanup completed")
            self._print_timing()

    def diagnose(self) -> None:
        """Run diagnostic analysis on current plan."""
        if not self.plan_file.exists():
            print("❌ No CURRENT_PLAN.md found")
            return

        print("🔍 Plan Diagnostics\n")

        # File size analysis
        file_size = self.plan_file.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        print(f"📊 File Size: {file_size:,} bytes ({file_size_mb:.2f} MB)")
        if file_size_mb > MAX_PLAN_SIZE_MB:
            print(f"   ⚠️  Exceeds recommended limit of {MAX_PLAN_SIZE_MB}MB")
        else:
            print(f"   ✅ Within recommended limit of {MAX_PLAN_SIZE_MB}MB")

        # Content analysis
        content = self.plan_file.read_text()
        line_count = content.count('\n')
        print(f"\n📝 Lines: {line_count:,}")

        # Metadata extraction
        try:
            metadata = self.get_current_state()
            print(f"\n📋 Plan Status:")
            print(f"   Goal: {metadata.get('goal', 'Unknown')[:60]}...")
            print(f"   Current Phase: {metadata.get('current_phase', 'Unknown')}")
            print(f"   Completed: {len(metadata.get('completed_phases', []))}/{len(metadata.get('phases', []))}")
            print(f"   Last Updated: {metadata.get('last_updated', 'Unknown')}")
        except Exception as e:
            print(f"\n❌ Error reading metadata: {e}")

        # Phase directory analysis
        print(f"\n📁 Phase Directories:")
        if self.plans_dir.exists():
            total_size = 0
            for phase_dir in sorted(self.plans_dir.iterdir()):
                if phase_dir.is_dir():
                    phase_size = sum(f.stat().st_size for f in phase_dir.rglob('*') if f.is_file())
                    total_size += phase_size
                    file_count = sum(1 for _ in phase_dir.rglob('*') if _.is_file())
                    print(f"   {phase_dir.name}: {file_count} files, {phase_size:,} bytes")

            print(f"\n💾 Total Phase Data: {total_size:,} bytes ({total_size / (1024 * 1024):.2f} MB)")

        # Recommendations
        print(f"\n💡 Recommendations:")
        if file_size_mb > MAX_PLAN_SIZE_MB:
            print("   • Reduce CURRENT_PLAN.md size by removing verbose outputs")
        if line_count > 500:
            print("   • Consider more concise phase summaries")
        print("   • Keep phase_summary.md files under 500 words")
        print("   • Store large artifacts in knowledge-base/ instead of inline")

    def _print_timing(self) -> None:
        """Print timing data if enabled."""
        if self.enable_timing and self._timing_data:
            print("\n⏱️  Timing:")
            for operation, duration in self._timing_data:
                print(f"   {operation}: {duration*1000:.2f}ms")
            self._timing_data.clear()


def main():
    """CLI interface for the orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(description="Plan Orchestrator")
    parser.add_argument("--dir", default=".", help="Working directory")
    parser.add_argument("--timing", action="store_true", help="Enable performance timing")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Initialize command
    init_parser = subparsers.add_parser("init", help="Initialize a new plan")
    init_parser.add_argument("goal", help="Plan goal")
    init_parser.add_argument("--phases", nargs="+", help="Custom phases")

    # Status command
    subparsers.add_parser("status", help="Show current plan status")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update phase status")
    update_parser.add_argument("phase", help="Phase name")
    update_parser.add_argument("status", choices=["in_progress", "completed"])
    update_parser.add_argument("--outputs", nargs="+", help="Phase outputs")

    # Cleanup command
    subparsers.add_parser("cleanup", help="Clean up plan files")

    # Diagnose command
    subparsers.add_parser("diagnose", help="Run diagnostic analysis on current plan")

    args = parser.parse_args()
    orchestrator = PlanOrchestrator(args.dir, enable_timing=args.timing)

    try:
        if args.command == "init":
            orchestrator.initialize_plan(args.goal, args.phases)
        elif args.command == "status":
            state = orchestrator.get_current_state()
            print(json.dumps(state, indent=2))
        elif args.command == "update":
            orchestrator.update_phase(args.phase, args.status, args.outputs)
        elif args.command == "cleanup":
            orchestrator.cleanup()
        elif args.command == "diagnose":
            orchestrator.diagnose()
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
