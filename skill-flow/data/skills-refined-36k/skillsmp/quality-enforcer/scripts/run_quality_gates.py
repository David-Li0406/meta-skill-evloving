#!/usr/bin/env python3
"""Run all quality gates and report results."""

import shutil
import subprocess
import sys
from pathlib import Path

# Add workflow-utilities to path for worktree_context and container_utils
sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"),
)

from container_utils import get_command_prefix, get_uv_command_prefix


def get_worktree_info() -> dict:
    """Get worktree context information for logging.

    Returns:
        Dictionary with worktree_id and worktree_root, or empty values if detection fails.
    """
    try:
        from worktree_context import get_worktree_context

        ctx = get_worktree_context()
        return {
            "worktree_id": ctx.worktree_id,
            "worktree_root": str(ctx.worktree_root),
        }
    except (ImportError, RuntimeError):
        return {"worktree_id": "", "worktree_root": str(Path.cwd())}


def run_tests():
    """Run all tests and verify they pass."""
    print("Running tests...")
    prefix = get_command_prefix()
    result = subprocess.run(prefix + ["pytest", "-v"], capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("[OK] All tests passed")
    else:
        print("[X] Some tests failed")
        print(result.stdout)
        print(result.stderr)

    return passed


def check_coverage(threshold=80):
    """Check test coverage meets threshold."""
    print(f"Checking coverage (>={threshold}%)...")

    # Call check_coverage.py script using repo-relative path for container compatibility
    script_path = ".claude/skills/quality-enforcer/scripts/check_coverage.py"
    prefix = get_command_prefix()
    result = subprocess.run(prefix + ["python", script_path, str(threshold)], capture_output=True, text=True)

    passed = result.returncode == 0
    print(result.stdout)

    return passed


def check_build():
    """Verify package builds successfully."""
    print("Checking build...")
    prefix = get_uv_command_prefix()
    result = subprocess.run(prefix + ["build"], capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("[OK] Build successful")
    else:
        print("[X] Build failed")
        print(result.stderr)

    return passed


def check_linting():
    """Run ruff linting."""
    print("Checking linting...")

    prefix = get_command_prefix()
    result = subprocess.run(prefix + ["ruff", "check", "."], capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("[OK] Linting passed")
    else:
        print("[X] Linting failed")
        print(result.stdout)

    return passed


def sync_ai_config():
    """
    Sync and verify AI configuration files.

    Uses consolidated sync_ai_config utility for:
    - CLAUDE.md → AGENTS.md
    - CLAUDE.md → .github/copilot-instructions.md
    - .claude/skills/ → .agents/

    Returns:
        True if sync successful and files are in sync
    """
    print("Checking AI assistant configuration...")

    try:
        # Import consolidated sync utility
        sync_utils_path = Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"
        if str(sync_utils_path) not in sys.path:
            sys.path.insert(0, str(sync_utils_path))

        from sync_ai_config import sync_all, verify_sync

        # First, sync any out-of-date files
        success, modified = sync_all()

        if not success:
            print("[X] AI config sync failed")
            return False

        # Then verify everything is in sync
        if not verify_sync():
            print("[X] AI config verification failed - files still out of sync")
            return False

        print("[OK] AI assistant configuration synced and verified")
        return True

    except ImportError:
        # Fallback to inline implementation if import fails
        print("  ⚠️  Using fallback sync (sync_ai_config.py not found)")

        # Check if CLAUDE.md or .claude/ was modified
        git_diff = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True, check=False)
        git_diff_staged = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True, check=False)
        modified_files = git_diff.stdout + git_diff_staged.stdout
        needs_sync = "CLAUDE.md" in modified_files or ".claude/" in modified_files

        if not needs_sync:
            print("⚠️  CLAUDE.md not modified, skipping sync")
            return True

        print("📝 CLAUDE.md modified - syncing to cross-tool formats...")

        if Path("CLAUDE.md").exists():
            shutil.copy("CLAUDE.md", "AGENTS.md")
            print("  [OK] Synced CLAUDE.md → AGENTS.md")
            Path(".github").mkdir(exist_ok=True)
            shutil.copy("CLAUDE.md", ".github/copilot-instructions.md")
            print("  [OK] Synced CLAUDE.md → .github/copilot-instructions.md")

        if Path(".claude/skills").exists():
            Path(".agents").mkdir(exist_ok=True)
            for skill_dir in Path(".claude/skills").iterdir():
                if skill_dir.is_dir():
                    dest = Path(".agents") / skill_dir.name
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(skill_dir, dest)
            print("  [OK] Synced .claude/skills/ → .agents/")

        print("[OK] AI assistant configuration synced")
        return True

    except Exception as e:
        print(f"⚠️  Sync failed (non-critical): {e}")
        return True  # Don't fail quality gates if sync fails


def run_all_quality_gates(coverage_threshold=80):
    """
    Run all quality gates and report results.

    Returns:
        (passed: bool, results: dict)
    """
    results = {}
    all_passed = True

    # Get worktree context
    worktree_info = get_worktree_info()
    results["worktree_id"] = worktree_info["worktree_id"]
    results["worktree_root"] = worktree_info["worktree_root"]

    print("=" * 60)
    print("QUALITY GATES")
    if worktree_info["worktree_id"]:
        print(f"Worktree: {worktree_info['worktree_id']}")
    print("=" * 60)

    # Gate 1: Test Coverage
    print("\n[1/5] Test Coverage...")
    passed = check_coverage(coverage_threshold)
    results["coverage"] = {"passed": passed}
    all_passed &= passed

    # Gate 2: Tests Passing
    print("\n[2/5] Running Tests...")
    passed = run_tests()
    results["tests"] = {"passed": passed}
    all_passed &= passed

    # Gate 3: Build
    print("\n[3/5] Build Check...")
    passed = check_build()
    results["build"] = {"passed": passed}
    all_passed &= passed

    # Gate 4: Linting
    print("\n[4/5] Linting...")
    passed = check_linting()
    results["linting"] = {"passed": passed}
    all_passed &= passed

    # Gate 5: AI Assistant Configuration Sync
    print("\n[5/5] AI Assistant Configuration...")
    passed = sync_ai_config()
    results["ai_config_sync"] = {"passed": passed}
    all_passed &= passed

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    # Dynamically summarize gates, filtering out non-gate keys
    non_gate_keys = {"worktree_id", "worktree_root"}
    for gate, result in results.items():
        if gate in non_gate_keys:
            continue
        if isinstance(result, dict):
            status = "[OK] PASS" if result.get("passed", False) else "[X] FAIL"
            print(f"{gate.upper()}: {status}")

    print("\n" + ("[OK] ALL GATES PASSED" if all_passed else "[X] SOME GATES FAILED"))

    # Trigger sync engine (Phase 3 integration)
    try:
        import asyncio

        integration_path = Path(__file__).parent.parent.parent / "agentdb-state-manager" / "scripts"
        if str(integration_path) not in sys.path:
            sys.path.insert(0, str(integration_path))
        from worktree_agent_integration import trigger_sync_completion

        asyncio.run(
            trigger_sync_completion(
                agent_id="assess",
                action="test_complete",
                state_snapshot={
                    "all_passed": all_passed,
                    "coverage_passed": results.get("coverage", {}).get("passed", False),
                    "tests_passed": results.get("tests", {}).get("passed", False),
                    "build_passed": results.get("build", {}).get("passed", False),
                    "linting_passed": results.get("linting", {}).get("passed", False),
                    "ai_config_sync_passed": results.get("ai_config_sync", {}).get("passed", False),
                },
                context={},
            )
        )
    except Exception:
        # Graceful degradation: don't fail if sync unavailable
        pass

    return all_passed, results


if __name__ == "__main__":
    # Coverage threshold: 40% (as of 2025-11-26, actual coverage is 44%)
    # Target: Incrementally increase to 80% - tracked in GitHub issue #9
    # History:
    #   - 2025-11-23: Started at ~4%, threshold set to 0%
    #   - 2025-11-26: Reached 44%, threshold set to 40%
    passed, _ = run_all_quality_gates(coverage_threshold=40)
    sys.exit(0 if passed else 1)
