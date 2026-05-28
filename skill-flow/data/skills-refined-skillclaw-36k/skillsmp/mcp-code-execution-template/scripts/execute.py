#!/usr/bin/env python3
"""
MCP Code Execution Runner

This script executes TypeScript code that interacts with MCP servers,
keeping all data processing outside the model context for 98%+ token efficiency.

Usage:
    python execute.py <task_file.ts>
    python execute.py workspace/task.ts

The script will:
1. Compile and run the TypeScript file using ts-node or tsx
2. Capture all console.log output (summaries)
3. Return only the summary to stdout (for model context)
4. Keep all intermediate data in the execution environment
"""

import subprocess
import sys
import os
import json
import tempfile
from pathlib import Path
from typing import Optional, Tuple

# Script directory and project paths
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR / "workspace"
SERVERS_DIR = SKILL_DIR / "servers"


def find_typescript_runner() -> Optional[str]:
    """Find available TypeScript runner (tsx, ts-node, or npx ts-node)."""
    runners = ["tsx", "ts-node", "npx ts-node"]

    for runner in runners:
        try:
            # Check if runner is available
            cmd = runner.split()[0]
            result = subprocess.run(
                ["which", cmd] if os.name != "nt" else ["where", cmd],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return runner
        except Exception:
            continue

    return None


def execute_typescript(file_path: Path) -> Tuple[int, str, str]:
    """
    Execute a TypeScript file and return (exit_code, stdout, stderr).

    Uses tsx/ts-node for direct execution without compilation step.
    """
    runner = find_typescript_runner()

    if not runner:
        return (1, "", "ERROR: No TypeScript runner found. Install tsx or ts-node:\n  npm install -g tsx\n  # or\n  npm install -g ts-node typescript")

    # Set up environment with paths to servers
    env = os.environ.copy()
    env["NODE_PATH"] = str(SERVERS_DIR)
    env["MCP_SERVERS_DIR"] = str(SERVERS_DIR)
    env["MCP_WORKSPACE_DIR"] = str(WORKSPACE_DIR)

    # Execute the TypeScript file
    try:
        result = subprocess.run(
            runner.split() + [str(file_path)],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(SKILL_DIR),
            env=env
        )
        return (result.returncode, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (124, "", "ERROR: Execution timed out after 5 minutes")
    except Exception as e:
        return (1, "", f"ERROR: Execution failed: {str(e)}")


def execute_task(task_file: str) -> dict:
    """
    Execute a task file and return structured results.

    Args:
        task_file: Path to the TypeScript task file

    Returns:
        dict with keys: success, summary, errors, exit_code
    """
    file_path = Path(task_file)

    # Handle relative paths
    if not file_path.is_absolute():
        # Check workspace first
        workspace_path = WORKSPACE_DIR / task_file
        if workspace_path.exists():
            file_path = workspace_path
        else:
            file_path = SKILL_DIR / task_file

    if not file_path.exists():
        return {
            "success": False,
            "summary": "",
            "errors": f"Task file not found: {task_file}",
            "exit_code": 1
        }

    if not file_path.suffix in [".ts", ".tsx", ".js", ".mjs"]:
        return {
            "success": False,
            "summary": "",
            "errors": f"Invalid file type: {file_path.suffix}. Expected .ts, .tsx, .js, or .mjs",
            "exit_code": 1
        }

    exit_code, stdout, stderr = execute_typescript(file_path)

    # Parse results
    success = exit_code == 0

    # Extract summary from stdout (last non-empty lines are the summary)
    summary_lines = [line for line in stdout.strip().split('\n') if line.strip()]
    summary = '\n'.join(summary_lines[-10:]) if summary_lines else "No output"

    return {
        "success": success,
        "summary": summary,
        "errors": stderr if stderr else None,
        "exit_code": exit_code
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python execute.py <task_file.ts>")
        print("")
        print("Examples:")
        print("  python execute.py workspace/fetch-data.ts")
        print("  python execute.py task.ts")
        print("")
        print("The script executes TypeScript code that calls MCP tools,")
        print("keeping all data processing outside the model context.")
        sys.exit(1)

    task_file = sys.argv[1]
    result = execute_task(task_file)

    # Output format for model consumption
    if result["success"]:
        print(f"SUCCESS: {result['summary']}")
    else:
        print(f"FAILED (exit code {result['exit_code']})")
        if result["errors"]:
            print(f"Errors: {result['errors'][:500]}")  # Limit error output
        if result["summary"]:
            print(f"Output: {result['summary']}")

    sys.exit(result["exit_code"])


if __name__ == "__main__":
    main()
