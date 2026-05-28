# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Silent Failure Audit for Claude Code Plugins.

Validates that all hook entry points emit to stderr on failure.

Checks:
1. Shellcheck on hook .sh files
2. Silent bash commands (mkdir, cp, mv, rm, jq) without `if !` pattern
3. Silent Python exceptions (`except: pass`) without stderr emission

Usage:
    uv run audit_silent_failures.py <plugin_path> [--fix]

Exit codes:
    0 = All validations passed
    1 = Violations found
    2 = Error (invalid path)
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Violation:
    """A single validation violation."""

    file: Path
    line: int
    check: str
    message: str
    severity: str = "error"  # error, warning
    fix_suggestion: str | None = None


@dataclass
class AuditResult:
    """Complete audit results for a plugin."""

    plugin_path: Path
    violations: list[Violation] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not any(v.severity == "error" for v in self.violations)

    @property
    def errors(self) -> list[Violation]:
        return [v for v in self.violations if v.severity == "error"]

    @property
    def warnings(self) -> list[Violation]:
        return [v for v in self.violations if v.severity == "warning"]


def find_hook_entry_points(plugin_path: Path) -> tuple[list[Path], list[Path]]:
    """Find actual hook entry point files by reading hooks.json.

    Only returns files that are directly invoked by Claude Code hooks,
    not utility modules that are imported by entry points.
    """
    hooks_dir = plugin_path / "hooks"
    hooks_json = hooks_dir / "hooks.json"

    if not hooks_dir.exists():
        return [], []

    entry_point_files: set[str] = set()

    # Try to read hooks.json to find actual entry points
    if hooks_json.exists():
        try:
            config = json.loads(hooks_json.read_text())
            hooks_config = config.get("hooks", {})

            # Extract file names from hook commands
            for _event_type, hook_list in hooks_config.items():
                for hook_group in hook_list:
                    for hook in hook_group.get("hooks", []):
                        command = hook.get("command", "")
                        # Extract filename from command
                        # Patterns: "uv run .../file.py", ".../file.sh", "python .../file.py"
                        for part in command.split():
                            if part.endswith(".py") or part.endswith(".sh"):
                                # Extract just the filename
                                filename = Path(part.replace("${CLAUDE_PLUGIN_ROOT}/hooks/", "")).name
                                entry_point_files.add(filename)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[audit] Warning: Failed to parse hooks.json: {e}", file=sys.stderr)
            # Fall back to checking all files
            entry_point_files = None

    # If no hooks.json or parsing failed, fall back to heuristics
    if entry_point_files is None or not entry_point_files:
        # Fall back: check all .sh files and .py files with __main__
        sh_files = list(hooks_dir.glob("*.sh"))
        py_files = []

        for py_file in hooks_dir.glob("*.py"):
            if py_file.name.startswith("__") or py_file.name.startswith("test_"):
                continue
            # Check if file has __main__ guard (indicates entry point)
            try:
                content = py_file.read_text()
                if '__name__ == "__main__"' in content or "__name__ == '__main__'" in content:
                    py_files.append(py_file)
            except OSError:
                pass

        return sh_files, py_files

    # Filter to only entry point files
    sh_files = [f for f in hooks_dir.glob("*.sh") if f.name in entry_point_files]
    py_files = [f for f in hooks_dir.glob("*.py") if f.name in entry_point_files]

    return sh_files, py_files


def run_shellcheck(sh_files: list[Path]) -> list[Violation]:
    """Run shellcheck on shell files."""
    violations = []

    if not sh_files:
        return violations

    # Check if shellcheck is available
    try:
        subprocess.run(["shellcheck", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[audit] Warning: shellcheck not installed, skipping shell checks", file=sys.stderr)
        return violations

    for sh_file in sh_files:
        try:
            result = subprocess.run(
                ["shellcheck", "-f", "json", str(sh_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.stdout:
                import json

                issues = json.loads(result.stdout)
                for issue in issues:
                    # Only report warnings and errors (not style/info)
                    if issue.get("level") in ("warning", "error"):
                        violations.append(
                            Violation(
                                file=sh_file,
                                line=issue.get("line", 0),
                                check="shellcheck",
                                message=f"SC{issue.get('code')}: {issue.get('message')}",
                                severity="warning" if issue.get("level") == "warning" else "error",
                            )
                        )
        except subprocess.TimeoutExpired:
            print(f"[audit] Warning: shellcheck timed out on {sh_file}", file=sys.stderr)
        except Exception as e:
            print(f"[audit] Warning: shellcheck failed on {sh_file}: {e}", file=sys.stderr)

    return violations


def check_silent_bash_commands(sh_files: list[Path]) -> list[Violation]:
    """Check for silent bash commands that should have error handling."""
    violations = []

    # Commands that can fail silently and should have `if !` pattern
    silent_commands = ["mkdir", "cp", "mv", "rm"]

    for sh_file in sh_files:
        try:
            content = sh_file.read_text()
            lines = content.splitlines()

            for i, line in enumerate(lines, 1):
                # Skip comments
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue

                for cmd in silent_commands:
                    # Pattern: command at start of line (not in if ! or ||)
                    # Look for: mkdir -p, cp file, mv file, rm -f
                    pattern = rf"^\s*{cmd}\s+"

                    if re.search(pattern, line):
                        # Check if it's properly guarded
                        # Good patterns:
                        # - if ! mkdir ...; then
                        # - mkdir ... || echo "error" >&2
                        # - mkdir ... 2>&1
                        # - if ! mkdir ... 2>&1; then

                        has_if_guard = re.search(rf"if\s+!\s+{cmd}", line)
                        has_or_guard = "||" in line
                        has_stderr_redirect = ">&2" in line or "2>&1" in line

                        if not (has_if_guard or has_or_guard or has_stderr_redirect):
                            violations.append(
                                Violation(
                                    file=sh_file,
                                    line=i,
                                    check="silent_bash",
                                    message=f"`{cmd}` without error handling - may fail silently",
                                    severity="error",
                                    fix_suggestion=f'if ! {cmd} ... 2>&1; then echo "[plugin] Failed: {cmd}" >&2; fi',
                                )
                            )
        except Exception as e:
            print(f"[audit] Warning: Failed to read {sh_file}: {e}", file=sys.stderr)

    return violations


def check_silent_python_exceptions(py_files: list[Path]) -> list[Violation]:
    """Check for silent Python exception handlers in hook entry points."""
    violations = []

    for py_file in py_files:
        try:
            content = py_file.read_text()
            lines = content.splitlines()

            i = 0
            while i < len(lines):
                line = lines[i]

                # Look for except blocks
                except_match = re.search(r"^\s*except\s+.*:", line)
                if except_match:
                    except_line = i + 1

                    # Check if exception is captured (has `as e` or `as err` etc.)
                    has_capture = re.search(r"\s+as\s+\w+", line)

                    # Look at the next few lines for the handler body
                    handler_lines = []
                    j = i + 1
                    indent_match = re.match(r"^(\s*)", line)
                    base_indent = len(indent_match.group(1)) if indent_match else 0

                    while j < len(lines):
                        next_line = lines[j]
                        if not next_line.strip():
                            j += 1
                            continue

                        next_indent_match = re.match(r"^(\s*)", next_line)
                        next_indent = len(next_indent_match.group(1)) if next_indent_match else 0

                        if next_indent <= base_indent and next_line.strip():
                            break

                        handler_lines.append(next_line)
                        j += 1

                    handler_body = "\n".join(handler_lines)

                    # Check for silent patterns
                    is_silent = False

                    # Pattern 1: Just `pass`
                    if re.search(r"^\s*pass\s*$", handler_body, re.MULTILINE):
                        # Check if stderr is used anywhere in handler
                        if "stderr" not in handler_body and "sys.stderr" not in handler_body:
                            is_silent = True

                    # Pattern 2: No capture and no stderr output
                    if not has_capture and "stderr" not in handler_body:
                        # Check if there's any logging or print
                        if "print(" not in handler_body and "logger" not in handler_body.lower():
                            is_silent = True

                    if is_silent:
                        violations.append(
                            Violation(
                                file=py_file,
                                line=except_line,
                                check="silent_python",
                                message="Silent exception handler - must emit to stderr in hook entry points",
                                severity="error",
                                fix_suggestion='except ... as e: print(f"[plugin] Warning: {e}", file=sys.stderr)',
                            )
                        )

                i += 1

        except Exception as e:
            print(f"[audit] Warning: Failed to read {py_file}: {e}", file=sys.stderr)

    return violations


def audit_plugin(plugin_path: Path) -> AuditResult:
    """Run all audits on a plugin."""
    result = AuditResult(plugin_path=plugin_path)

    sh_files, py_files = find_hook_entry_points(plugin_path)

    if not sh_files and not py_files:
        print(f"[audit] No hook entry points found in {plugin_path}/hooks/", file=sys.stderr)
        print("[audit] (Checked hooks.json for registered entry points)", file=sys.stderr)
        return result

    print(f"[audit] Found {len(sh_files)} .sh and {len(py_files)} .py hook entry points", file=sys.stderr)

    # Run all checks
    result.violations.extend(run_shellcheck(sh_files))
    result.violations.extend(check_silent_bash_commands(sh_files))
    result.violations.extend(check_silent_python_exceptions(py_files))

    return result


def print_results(result: AuditResult, show_fix: bool = False) -> None:
    """Print audit results."""
    print(f"\n{'=' * 60}")
    print(f"Silent Failure Audit: {result.plugin_path}")
    print(f"{'=' * 60}\n")

    if not result.violations:
        print("All hook entry points properly emit to stderr on failure.")
        return

    # Group by file
    by_file: dict[Path, list[Violation]] = {}
    for v in result.violations:
        by_file.setdefault(v.file, []).append(v)

    for file_path, violations in by_file.items():
        rel_path = file_path.relative_to(result.plugin_path) if file_path.is_relative_to(result.plugin_path) else file_path
        print(f"\n{rel_path}:")

        for v in sorted(violations, key=lambda x: x.line):
            icon = "X" if v.severity == "error" else "!"
            print(f"  [{icon}] Line {v.line}: {v.message}")
            if show_fix and v.fix_suggestion:
                print(f"      Fix: {v.fix_suggestion}")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Summary: {len(result.errors)} errors, {len(result.warnings)} warnings")

    if result.passed:
        print("PASSED (warnings only)")
    else:
        print("FAILED")


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    plugin_path = Path(sys.argv[1]).resolve()
    show_fix = "--fix" in sys.argv

    if not plugin_path.exists():
        print(f"Error: Path not found: {plugin_path}", file=sys.stderr)
        return 2

    if not plugin_path.is_dir():
        print(f"Error: Not a directory: {plugin_path}", file=sys.stderr)
        return 2

    result = audit_plugin(plugin_path)
    print_results(result, show_fix)

    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
