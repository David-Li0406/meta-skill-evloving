#!/usr/bin/env python3
"""
Viz Runner - Artifact management for the viz skill.

Usage:
    python viz_runner.py [--id NAME] < script_content
    python viz_runner.py [--id NAME] --file /path/to/script.py
    echo "script content" | python viz_runner.py --id my_plot

The runner:
1. Creates /tmp/viz/ if it doesn't exist
2. Ensures ID uniqueness (appends _2, _3, etc. if needed)
3. Injects plt.savefig() before any plt.show() call
4. Writes the modified script to /tmp/viz/<id>.py
5. Executes the script
6. Prints the final ID and paths to stdout
"""

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

# Import marimo handler (all marimo-specific code lives there)
from marimo_handler import MarimoHandler

VIZ_DIR = Path("/tmp/viz")


# ============================================================================
# Core Data Structures
# ============================================================================


@dataclass
class VizMetadata:
    """Metadata for a visualization artifact."""

    viz_id: str
    description: str | None
    png_path: Path
    script_path: Path
    pid: int
    source_notebook: Path | None = None
    target_vars: list[str] | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = {
            "id": self.viz_id,
            "desc": self.description,
            "png": str(self.png_path),
            "script": str(self.script_path),
            "created": datetime.now().isoformat(timespec="seconds"),
            "pid": self.pid,
        }
        if self.source_notebook:
            data["source_notebook"] = str(self.source_notebook)
        if self.target_vars:
            data["target_vars"] = self.target_vars
        return data

    def write(self, viz_dir: Path = VIZ_DIR) -> Path:
        """Write metadata to JSON file."""
        json_path = viz_dir / f"{self.viz_id}.json"
        json_path.write_text(json.dumps(self.to_dict(), indent=2))
        return json_path


# ============================================================================
# Source Handler Architecture
# ============================================================================


class SourceHandler(Protocol):
    """Interface for handlers that know how to build scripts from different source types."""

    def build_script(
        self,
        action_code: str,
        source_path: Path | None = None,
        target_var: str | None = None,
        **kwargs,
    ) -> tuple[str, Path | None]:
        """
        Build an executable Python script that prepares data and runs action_code.

        The action_code could be plotting code, show/inspection code, or any other
        code that operates on the target variable.

        Args:
            action_code: Code to execute (plotting, showing, etc.)
            source_path: Optional path to source file (notebook, SQL file, etc.)
            target_var: Optional variable name to extract from source
            **kwargs: Handler-specific options

        Returns:
            (script_content, working_directory)
            - script_content: Complete Python script ready to execute
            - working_directory: Directory to run script from (or None for cwd)
        """
        ...

    def validate_args(self, args: argparse.Namespace) -> tuple[bool, str]:
        """
        Validate that required arguments are present.

        Returns:
            (valid, error_message)
        """
        ...


class DefaultHandler:
    """Default handler - action_code is the complete script."""

    def build_script(
        self,
        action_code: str,
        source_path: Path | None = None,
        target_var: str | None = None,
        **kwargs,
    ) -> tuple[str, Path | None]:
        """For default handler, action_code IS the complete script."""
        return action_code, None

    def validate_args(self, args: argparse.Namespace) -> tuple[bool, str]:
        """Default handler has no special requirements."""
        return True, ""


# Handler registry
HANDLERS: dict[str, type[SourceHandler]] = {
    "default": DefaultHandler,
    "marimo": MarimoHandler,
}


def get_handler(args: argparse.Namespace) -> SourceHandler:
    """Select handler based on CLI args."""
    if getattr(args, "marimo", False):
        return MarimoHandler()
    # Future: elif args.sql: return SQLHandler()
    return DefaultHandler()


# ============================================================================
# Core Execution Functions
# ============================================================================


def run_plot(
    handler: SourceHandler,
    plot_code: str,
    viz_id: str,
    description: str | None = None,
    source_path: Path | None = None,
    target_var: str | None = None,
    **handler_kwargs,
) -> tuple[bool, str, Path | None]:
    """
    Core plotting function - uses handler to build script, then executes.

    Args:
        handler: The SourceHandler to use for building the script
        plot_code: The plotting code (or complete script for DefaultHandler)
        viz_id: ID for the visualization
        description: Optional description
        source_path: Optional source file (for MarimoHandler, etc.)
        target_var: Optional target variable (for MarimoHandler, etc.)
        **handler_kwargs: Additional handler-specific options

    Returns:
        (success, message, png_path)
    """
    ensure_viz_dir()

    # Build the script using the handler
    try:
        script_content, cwd = handler.build_script(
            plot_code,
            source_path=source_path,
            target_var=target_var,
            **handler_kwargs,
        )
    except ValueError as e:
        return False, str(e), None

    # Determine paths
    script_path = VIZ_DIR / f"{viz_id}.py"
    png_path = VIZ_DIR / f"{viz_id}.png"

    # Inject savefig
    script_content = inject_savefig(script_content, str(png_path))
    script_path.write_text(script_content)

    # Execute with fallback chain - retry on module errors
    fallback_chain = get_python_fallback_chain(cwd)
    max_wait = 30.0 if source_path else 3.0
    result = None

    for python_cmd in fallback_chain:
        process = subprocess.Popen(
            [*python_cmd, str(script_path)],
            cwd=cwd,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

        result = poll_for_file(
            process, png_path, python_cmd, max_wait=max_wait, poll_interval=0.2
        )

        if result.success:
            VizMetadata(
                viz_id=viz_id,
                description=description,
                png_path=png_path,
                script_path=script_path,
                pid=result.process.pid,
                source_notebook=source_path if isinstance(handler, MarimoHandler) else None,
                target_vars=[target_var] if target_var else None,
            ).write()
            return True, "Plot generated successfully", png_path

        # If not a module error, don't try next environment
        if "MISSING MODULE" not in result.message:
            break

    return False, result.message if result else "No Python environments available", None


def generate_show_code(target_var: str, num_rows: int = 5) -> str:
    """
    Generate code to display dataframe info to stdout.

    Args:
        target_var: Name of the variable to inspect
        num_rows: Number of rows to display

    Returns:
        Python code string that prints dataframe info
    """
    return f'''
_var = {target_var}
print(f"Shape: {{_var.shape}}")
print(f"Columns: {{list(_var.columns)}}")
print(f"\\nDtypes:")
print(_var.dtypes.to_string())
print(f"\\nFirst {num_rows} rows:")
if hasattr(_var, 'to_string'):
    print(_var.head({num_rows}).to_string())
else:
    print(_var.head({num_rows}))
'''


def run_show(
    handler: SourceHandler,
    target_var: str,
    source_path: Path | None = None,
    num_rows: int = 5,
    **handler_kwargs,
) -> tuple[bool, str]:
    """
    Execute a script to show/inspect data and capture output.

    Unlike run_plot() which backgrounds and polls for a PNG, this runs
    synchronously and captures stdout.

    Args:
        handler: The SourceHandler to use for building the script
        target_var: Variable to inspect
        source_path: Optional source file (for MarimoHandler, etc.)
        num_rows: Number of rows to display
        **handler_kwargs: Additional handler-specific options

    Returns:
        (success, output_or_error)
    """
    ensure_viz_dir()

    # Generate the show code
    show_code = generate_show_code(target_var, num_rows)

    # Build the script using the handler
    try:
        script_content, cwd = handler.build_script(
            show_code,
            source_path=source_path,
            target_var=target_var,
            **handler_kwargs,
        )
    except ValueError as e:
        return False, str(e)

    # Write to temp location
    script_path = VIZ_DIR / "_show_temp.py"
    script_path.write_text(script_content)

    # Execute with fallback chain - retry on module errors
    fallback_chain = get_python_fallback_chain(cwd)
    last_error = "No Python environments available"

    for python_cmd in fallback_chain:
        try:
            result = subprocess.run(
                [*python_cmd, str(script_path)],
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                script_path.unlink(missing_ok=True)
                return True, result.stdout

            # Check for module errors - try next env if so
            module_error = format_module_error(result.stderr, python_cmd)
            if module_error:
                last_error = module_error
                continue  # Try next environment

            # Non-module error, stop here
            script_path.unlink(missing_ok=True)
            return False, f"Script failed:\n{result.stderr}"

        except subprocess.TimeoutExpired:
            script_path.unlink(missing_ok=True)
            return False, "Timeout executing script"
        except Exception as e:
            script_path.unlink(missing_ok=True)
            return False, f"Error: {e}"

    # All environments failed with module errors
    script_path.unlink(missing_ok=True)
    return False, last_error


# ============================================================================
# Python Environment Detection
# ============================================================================


def validate_python_env(python_cmd: list[str], required_module: str = "matplotlib") -> bool:
    """
    Test if a Python environment can import a required module.

    Returns True if import succeeds, False otherwise.
    """
    try:
        result = subprocess.run(
            [*python_cmd, "-c", f"import {required_module}"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def get_python_fallback_chain(cwd: Path | None = None) -> list[list[str]]:
    """
    Return ordered list of Python commands to try.

    Priority:
    1. Project environment (cwd with uv markers)
    2. System Python on PATH
    3. Viz skill's own environment (guaranteed fallback)

    Returns list of commands to try in order. Each is tried until one succeeds.
    On module errors, the next environment in the chain is attempted.
    """
    chain = []

    # Project's environment
    if cwd is not None:
        uv_markers = [cwd / "pyproject.toml", cwd / "uv.lock"]
        if any(marker.exists() for marker in uv_markers):
            project_cmd = ["uv", "run", "--directory", str(cwd), "python"]
            if validate_python_env(project_cmd):
                chain.append(project_cmd)

    # System Python on PATH
    system_cmd = ["python"]
    if validate_python_env(system_cmd):
        chain.append(system_cmd)

    # Viz skill's own environment (guaranteed deps)
    viz_skill_dir = Path(__file__).parent
    chain.append(["uv", "run", "--directory", str(viz_skill_dir), "python"])

    return chain


def get_python_command(cwd: Path | None = None) -> list[str]:
    """
    Get the first Python command from the fallback chain.

    For backwards compatibility. Use get_python_fallback_chain() for retry logic.
    """
    chain = get_python_fallback_chain(cwd)
    return chain[0] if chain else ["python"]


# ============================================================================
# File and Directory Utilities
# ============================================================================


def ensure_viz_dir():
    """Create /tmp/viz/ if it doesn't exist."""
    VIZ_DIR.mkdir(parents=True, exist_ok=True)


def get_unique_id(suggested_id: str | None) -> str:
    """
    Generate a unique ID for the visualization.

    If suggested_id is provided, check if it exists and append _2, _3, etc.
    If no suggested_id, generate a timestamp-based ID.
    """
    if suggested_id is None:
        # Generate timestamp-based ID
        base_id = datetime.now().strftime("viz_%Y%m%d_%H%M%S")
    else:
        base_id = suggested_id

    # Check if the base ID is available
    if not (VIZ_DIR / f"{base_id}.py").exists():
        return base_id

    # Find the next available suffix
    counter = 2
    while (VIZ_DIR / f"{base_id}_{counter}.py").exists():
        counter += 1

    return f"{base_id}_{counter}"


def inject_savefig(script: str, png_path: str) -> str:
    """
    Inject plt.savefig() before plt.show() calls.

    Handles various patterns:
    - plt.show()
    - pyplot.show()
    - fig.show() (less common but possible)
    """
    savefig_line = f"plt.savefig('{png_path}', dpi=150, bbox_inches='tight')"

    # Pattern to match plt.show() or pyplot.show() with optional whitespace
    # We insert savefig on the line before show()
    pattern = r'^(\s*)(plt\.show\(\)|pyplot\.show\(\))'

    def replacement(match):
        indent = match.group(1)
        show_call = match.group(2)
        return f"{indent}{savefig_line}\n{indent}{show_call}"

    modified = re.sub(pattern, replacement, script, flags=re.MULTILINE)

    # If no plt.show() was found, append savefig at the end
    if modified == script:
        # Check if matplotlib is imported
        if 'matplotlib' in script or 'plt' in script:
            modified = script.rstrip() + f"\n\n# Auto-injected by viz_runner\n{savefig_line}\n"

    return modified


# ============================================================================
# Process Polling
# ============================================================================


@dataclass
class PollResult:
    """Result from polling a subprocess for file creation."""

    success: bool
    message: str
    process: subprocess.Popen


def poll_for_file(
    process: subprocess.Popen,
    target_file: Path,
    python_cmd: list[str],
    max_wait: float = 3.0,
    poll_interval: float = 0.1,
) -> PollResult:
    """
    Poll a subprocess, waiting for a target file to be created.

    Returns early if:
    - Target file appears (success)
    - Process exits with error (failure)
    - Timeout reached (failure, but process may still be running)
    """
    waited = 0.0
    while waited < max_wait:
        if target_file.exists():
            return PollResult(success=True, message="File created", process=process)

        time.sleep(poll_interval)
        waited += poll_interval

        if process.poll() is not None:
            stderr = process.stderr.read().decode() if process.stderr else ""
            module_error = format_module_error(stderr, python_cmd)
            error_msg = module_error or f"Script failed: {stderr}"
            return PollResult(success=False, message=error_msg, process=process)

    return PollResult(
        success=False,
        message="Timeout waiting for file (process may still be running)",
        process=process,
    )


def format_module_error(stderr: str, python_cmd: list[str]) -> str | None:
    """
    Detect ModuleNotFoundError and return a clear, actionable error message.
    Returns None if not a module error.
    """
    match = re.search(r"ModuleNotFoundError: No module named ['\"]?([^'\"]+)['\"]?", stderr)
    if match:
        module = match.group(1)
        cmd_str = " ".join(python_cmd)
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  MISSING MODULE: {module:<59} ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  The viz skill's Python environment is missing required packages.            ║
║                                                                              ║
║  To fix this, either:                                                        ║
║                                                                              ║
║  1. Restart Claude Code with the correct Python environment activated:       ║
║     $ source /path/to/your/venv/bin/activate && claude                       ║
║                                                                              ║
║  2. Or configure viz_runner.py to use a different Python command:            ║
║     Set VIZ_PYTHON_CMD environment variable, e.g.:                           ║
║     $ export VIZ_PYTHON_CMD="uv run python"                                  ║
║                                                                              ║
║  Python command: {cmd_str:<57} ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    return None


def run_script_background(script_path: Path, png_path: Path) -> tuple[bool, int, str]:
    """
    Execute the script in background and wait for PNG to be created.
    Returns (success, pid, message).

    The script runs as a detached process so plt.show() doesn't block.
    Since savefig() is injected BEFORE plt.show(), the PNG gets created
    immediately while the interactive window stays open.
    """
    try:
        python_cmd = get_python_command()

        # Start script as detached background process
        # Use caller's cwd (not VIZ_DIR) so uv can find pyproject.toml
        process = subprocess.Popen(
            [*python_cmd, str(script_path)],
            start_new_session=True,  # Detach from terminal
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

        # Poll for PNG (savefig happens before plt.show)
        result = poll_for_file(process, png_path, python_cmd)

        if result.success:
            return True, result.process.pid, "Plot window opened"

        # On failure, return 0 for pid if process failed, otherwise actual pid
        pid = 0 if result.process.poll() is not None else result.process.pid
        return False, pid, result.message

    except Exception as e:
        return False, 0, f"Error: {e}"


# ============================================================================
# CLI Handlers
# ============================================================================


def handle_clean() -> int:
    """Handle --clean command. Returns exit code."""
    ensure_viz_dir()
    count = 0
    for f in VIZ_DIR.iterdir():
        if f.is_file():
            f.unlink()
            count += 1
    print(f"Cleaned {count} files from {VIZ_DIR}")
    return 0


def handle_list() -> int:
    """Handle --list command. Returns exit code."""
    ensure_viz_dir()
    json_files = sorted(VIZ_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not json_files:
        print("No visualizations found")
        return 0

    # Collect metadata
    rows = []
    for jf in json_files:
        meta = json.loads(jf.read_text())
        rows.append({
            "id": meta.get("id", jf.stem),
            "desc": meta.get("desc") or "-",
            "created": meta.get("created", "")[:16].replace("T", " "),
        })

    # Calculate column widths
    id_width = max(len("ID"), max(len(r["id"]) for r in rows))
    desc_width = max(len("Description"), max(len(r["desc"]) for r in rows))

    # Print table
    header = f"{'ID':<{id_width}}  {'Description':<{desc_width}}  Created"
    print(header)
    print(f"{'-' * id_width}  {'-' * desc_width}  {'-' * 16}")
    for r in rows:
        print(f"{r['id']:<{id_width}}  {r['desc']:<{desc_width}}  {r['created']}")
    return 0


def handle_marimo_show(args: argparse.Namespace) -> int:
    """Handle --marimo --show command. Returns exit code."""
    notebook_path = Path(args.notebook_path)

    handler = MarimoHandler()
    success, output = run_show(
        handler=handler,
        target_var=args.target_var,
        source_path=notebook_path,
        num_rows=args.rows,
    )

    if success:
        print(output)
    else:
        print(f"error: {output}", file=sys.stderr)

    return 0 if success else 1


def handle_marimo_plot(args: argparse.Namespace, plot_code: str) -> int:
    """Handle --marimo plot command. Returns exit code."""
    notebook_path = Path(args.notebook_path)
    final_id = get_unique_id(args.suggested_id)

    handler = MarimoHandler()
    success, message, png_path = run_plot(
        handler=handler,
        plot_code=plot_code,
        viz_id=final_id,
        description=args.description,
        source_path=notebook_path,
        target_var=args.target_var,
        target_line=args.target_line,
    )

    # Print human-readable output
    print(f"Plot: {final_id}")
    if args.description:
        print(f'  "{args.description}"')
    if png_path:
        print(f"  png: {png_path}")
    print(f"  source: {notebook_path}")

    if not success:
        print(f"  error: {message}")

    return 0 if success else 1


def handle_standalone_script(args: argparse.Namespace, script_content: str) -> int:
    """Handle standalone script execution. Returns exit code."""
    final_id = get_unique_id(args.suggested_id)
    png_path = VIZ_DIR / f"{final_id}.png"

    handler = DefaultHandler()
    success, message, _ = run_plot(
        handler=handler,
        plot_code=script_content,
        viz_id=final_id,
        description=args.description,
    )

    # Print human-readable output
    print(f"Plot: {final_id}")
    if args.description:
        print(f'  "{args.description}"')
    print(f"  png: {png_path}")

    if not success:
        print(f"  error: {message}")

    # Check if PNG was actually created
    if success and not png_path.exists():
        print("  warning: Script executed but PNG was not created")

    return 0 if success else 1


# ============================================================================
# Main Entry Point
# ============================================================================


def main():
    parser = argparse.ArgumentParser(description="Viz Runner - artifact management for viz skill")
    parser.add_argument("--id", dest="suggested_id", help="Suggested ID for the visualization")
    parser.add_argument("--desc", dest="description", help="Description of the visualization")
    parser.add_argument("--file", dest="script_file", help="Path to script file (alternative to stdin)")
    parser.add_argument("--clean", action="store_true", help="Remove all files from /tmp/viz/")
    parser.add_argument("--list", action="store_true", help="List all visualizations")

    # Marimo notebook support
    parser.add_argument("--marimo", action="store_true", help="Enable marimo notebook mode")
    parser.add_argument("--notebook", dest="notebook_path", help="Path to marimo notebook (.nb.py)")
    parser.add_argument("--target-var", dest="target_var", help="Variable to extract from notebook")
    parser.add_argument("--target-line", dest="target_line", type=int, help="Line number for intermediate state capture")
    parser.add_argument("--show", action="store_true", help="Show mode: print dataframe info to console instead of plotting")
    parser.add_argument("--rows", dest="rows", type=int, default=5, help="Number of rows to display in show mode (default: 5)")

    args = parser.parse_args()

    # Handle clean action
    if args.clean:
        sys.exit(handle_clean())

    # Handle list action
    if args.list:
        sys.exit(handle_list())

    # Handle marimo notebook mode
    if args.marimo:
        if not args.notebook_path:
            print("error: --marimo requires --notebook path", file=sys.stderr)
            sys.exit(1)
        if not args.target_var:
            print("error: --marimo requires --target-var", file=sys.stderr)
            sys.exit(1)

        notebook_path = Path(args.notebook_path)
        if not notebook_path.exists():
            print(f"error: Notebook not found: {notebook_path}", file=sys.stderr)
            sys.exit(1)

        # Handle --show mode (print dataframe to console)
        if args.show:
            sys.exit(handle_marimo_show(args))

        # Read plot code from stdin
        if sys.stdin.isatty():
            print("error: Pipe plot code to stdin for marimo mode", file=sys.stderr)
            sys.exit(1)
        plot_code = sys.stdin.read()

        if not plot_code.strip():
            print("error: Empty plot code provided", file=sys.stderr)
            sys.exit(1)

        sys.exit(handle_marimo_plot(args, plot_code))

    # Handle standalone script mode
    if args.script_file:
        try:
            with open(args.script_file, 'r') as f:
                script_content = f.read()
        except Exception as e:
            print(f"error: Could not read script file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("error: No script provided. Pipe script content or use --file", file=sys.stderr)
            sys.exit(1)
        script_content = sys.stdin.read()

    if not script_content.strip():
        print("error: Empty script provided", file=sys.stderr)
        sys.exit(1)

    sys.exit(handle_standalone_script(args, script_content))


if __name__ == "__main__":
    main()
