"""Health check logic for layton doctor.

Validates system setup and dependencies.
"""

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from laytonlib.formatters import OutputFormatter


@dataclass
class CheckResult:
    """Result of a single health check."""

    name: str
    status: Literal["pass", "warn", "fail"]
    message: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
        }


def find_git_root() -> Path | None:
    """Find the git repository root, or None if not in a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_layton_dir() -> Path:
    """Get the .layton directory path (in git root or cwd)."""
    git_root = find_git_root()
    base = git_root if git_root else Path.cwd()
    return base / ".layton"


def get_config_path() -> Path:
    """Get the config.json path."""
    return get_layton_dir() / "config.json"


def check_beads_available() -> CheckResult:
    """Check if bd CLI is available and working."""
    # Check if bd is in PATH
    bd_path = shutil.which("bd")
    if not bd_path:
        return CheckResult(
            name="beads_available",
            status="fail",
            message="bd CLI not found in PATH. Install Beads: https://github.com/steveyegge/beads",
        )

    # Check if bd info --json works
    try:
        result = subprocess.run(
            ["bd", "info", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return CheckResult(
                name="beads_available",
                status="pass",
                message=f"bd CLI available at {bd_path}",
            )
        else:
            return CheckResult(
                name="beads_available",
                status="fail",
                message=(
                    f"bd CLI found but 'bd info --json' failed: {result.stderr.strip()}"
                ),
            )
    except subprocess.TimeoutExpired:
        return CheckResult(
            name="beads_available",
            status="fail",
            message="bd CLI found but 'bd info --json' timed out",
        )
    except Exception as e:
        return CheckResult(
            name="beads_available",
            status="fail",
            message=f"bd CLI found but failed to execute: {e}",
        )


def check_beads_initialized() -> CheckResult:
    """Check if .beads/ directory exists."""
    git_root = find_git_root()
    base = git_root if git_root else Path.cwd()
    beads_dir = base / ".beads"

    if beads_dir.exists():
        return CheckResult(
            name="beads_initialized",
            status="pass",
            message=f"Beads initialized at {beads_dir}",
        )
    else:
        return CheckResult(
            name="beads_initialized",
            status="warn",
            message="Beads not initialized. Run 'bd init' to create .beads/",
        )


def check_config_exists() -> CheckResult:
    """Check if .layton/config.json exists."""
    config_path = get_config_path()

    if config_path.exists():
        return CheckResult(
            name="config_exists",
            status="pass",
            message=f"Config found at {config_path}",
        )
    else:
        return CheckResult(
            name="config_exists",
            status="fail",
            message=f"Config missing at {config_path}",
        )


def check_config_valid() -> CheckResult:
    """Check if config.json is valid JSON."""
    config_path = get_config_path()

    if not config_path.exists():
        return CheckResult(
            name="config_valid",
            status="fail",
            message="Cannot validate config - file does not exist",
        )

    try:
        with open(config_path) as f:
            json.load(f)
        return CheckResult(
            name="config_valid",
            status="pass",
            message="Config is valid JSON",
        )
    except json.JSONDecodeError as e:
        return CheckResult(
            name="config_valid",
            status="fail",
            message=f"Config has invalid JSON: {e}",
        )
    except Exception as e:
        return CheckResult(
            name="config_valid",
            status="fail",
            message=f"Cannot read config: {e}",
        )


def get_default_config() -> dict:
    """Get default configuration values."""
    # Try to detect system timezone
    try:
        from datetime import datetime

        tz = datetime.now().astimezone().tzinfo
        timezone = str(tz) if tz else "UTC"
    except Exception:
        timezone = "UTC"

    return {
        "timezone": timezone,
        "work": {
            "schedule": {
                "start": "09:00",
                "end": "17:00",
            }
        },
    }


def fix_config() -> bool:
    """Create config with defaults. Returns True if created."""
    config_path = get_config_path()
    layton_dir = get_layton_dir()

    try:
        # Create .layton/ directory if needed
        layton_dir.mkdir(parents=True, exist_ok=True)

        # Write default config
        config = get_default_config()
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False


def run_doctor(formatter: OutputFormatter, fix: bool = False) -> int:
    """Run all health checks.

    Args:
        formatter: Output formatter
        fix: If True, attempt to fix fixable issues

    Returns:
        Exit code (0=success, 1=fixable, 2=critical)
    """
    checks: list[CheckResult] = []
    next_steps: list[str] = []

    # Check beads availability (critical)
    beads_check = check_beads_available()
    checks.append(beads_check)

    if beads_check.status == "fail":
        # Critical failure - bd not available
        formatter.error(
            "BEADS_UNAVAILABLE",
            beads_check.message,
            next_steps=["Install Beads CLI: https://github.com/steveyegge/beads"],
        )
        return 2

    # Check beads initialized (warning)
    beads_init_check = check_beads_initialized()
    checks.append(beads_init_check)
    if beads_init_check.status == "warn":
        next_steps.append("Run 'bd init' to initialize Beads")

    # Check config exists (fixable)
    config_exists_check = check_config_exists()
    checks.append(config_exists_check)

    # Check config valid (if exists)
    config_valid_check = check_config_valid()
    if config_exists_check.status == "pass":
        checks.append(config_valid_check)

    # Determine if we need to fix
    config_missing = config_exists_check.status == "fail"
    config_invalid = (
        config_valid_check.status == "fail" and config_exists_check.status == "pass"
    )

    if fix and config_missing:
        # Attempt to fix config
        if fix_config():
            # Re-run config checks
            config_exists_check = check_config_exists()
            config_valid_check = check_config_valid()
            # Update checks list
            excluded = ("config_exists", "config_valid")
            checks = [c for c in checks if c.name not in excluded]
            checks.append(config_exists_check)
            checks.append(config_valid_check)
            config_missing = False

    # Build next_steps
    if config_missing:
        next_steps.append("Follow workflows/setup.md for guided onboarding")
        next_steps.append("Or run 'layton doctor --fix' for quick setup with defaults")

    if config_invalid:
        next_steps.append("Fix the JSON syntax error in .layton/config.json")

    # Determine overall status
    has_fail = any(c.status == "fail" for c in checks)
    has_warn = any(c.status == "warn" for c in checks)

    # Output results
    data = {
        "checks": [c.to_dict() for c in checks],
        "summary": {
            "total": len(checks),
            "pass": sum(1 for c in checks if c.status == "pass"),
            "warn": sum(1 for c in checks if c.status == "warn"),
            "fail": sum(1 for c in checks if c.status == "fail"),
        },
    }

    if has_fail:
        # Check if only config is failing (fixable)
        non_config_fails = [
            c
            for c in checks
            if c.status == "fail" and c.name not in ("config_exists", "config_valid")
        ]
        if non_config_fails:
            formatter.error(
                "CRITICAL_FAILURE",
                "Critical checks failed",
                next_steps=next_steps,
            )
            return 2
        else:
            # Only config failing - fixable
            formatter.success(data, next_steps=next_steps)
            return 1
    elif has_warn:
        formatter.success(data, next_steps=next_steps)
        return 0  # Warnings don't affect exit code
    else:
        # All pass
        if formatter.human:
            data["message"] = "All systems go!"
        formatter.success(data, next_steps=next_steps)
        return 0
