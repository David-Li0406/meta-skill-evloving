"""Output formatting for Layton CLI.

JSON is the default output format (agent-first design).
Use --human flag for human-readable output.
"""

import json
import sys
from dataclasses import dataclass, field
from typing import Any


@dataclass
class OutputFormatter:
    """Formats CLI output as JSON (default) or human-readable.

    Both formats apply the same compact logic:
    - All checks pass → show summary only
    - Any check fails or --verbose → show full details
    """

    human: bool = False
    verbose: bool = False
    _debug_info: dict[str, Any] = field(default_factory=dict)

    def add_debug(self, key: str, value: Any) -> None:
        """Add debug information (included if verbose=True)."""
        self._debug_info[key] = value

    def _should_expand_checks(self, checks: list[dict[str, Any]]) -> bool:
        """Determine if checks should show full details."""
        has_failures = any(c.get("status") == "fail" for c in checks)
        has_warnings = any(c.get("status") == "warn" for c in checks)
        return has_failures or has_warnings or self.verbose

    def _compact_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Apply compact logic to data before rendering.

        If checks exist and all pass (no failures/warnings), replace with summary.
        """
        if "checks" not in data:
            return data

        checks = data["checks"]
        if self._should_expand_checks(checks):
            return data  # Keep full details

        # Compact: replace checks array with summary
        total = len(checks)
        passed = sum(1 for c in checks if c.get("status") == "pass")

        compacted = dict(data)
        compacted["checks"] = {
            "summary": f"{passed}/{total} passed",
            "all_passed": True,
        }
        return compacted

    def success(
        self,
        data: dict[str, Any],
        next_steps: list[str] | None = None,
    ) -> None:
        """Output a success response."""
        # Apply compact logic to data
        output_data = self._compact_data(data)

        if self.human:
            self._render_human_success(output_data, next_steps)
        else:
            self._render_json_success(output_data, next_steps)

    def _render_json_success(
        self,
        data: dict[str, Any],
        next_steps: list[str] | None,
    ) -> None:
        """Render success as JSON."""
        response = {
            "success": True,
            "data": data,
            "next_steps": next_steps or [],
        }
        if self.verbose and self._debug_info:
            response["debug"] = self._debug_info
        print(json.dumps(response, indent=2))

    def _render_human_success(
        self,
        data: dict[str, Any],
        next_steps: list[str] | None,
    ) -> None:
        """Render success as human-readable text."""
        for key, value in data.items():
            self._print_data_item(key, value)

        if next_steps:
            print()
            print("Next steps:")
            for step in next_steps:
                print(f"  - {step}")

    def _print_data_item(self, key: str, value: Any) -> None:
        """Print a single data item in human-readable format."""
        # Special handling for compact checks summary
        if key == "checks" and isinstance(value, dict) and "summary" in value:
            print(f"✓ {value['summary']}")
            print()
            return

        # Special handling for expanded checks list
        if key == "checks" and isinstance(value, list):
            print("checks:")
            for check in value:
                status = check.get("status", "unknown")
                name = check.get("name", "unknown")
                message = check.get("message", "")
                icon = "✓" if status == "pass" else ("⚠" if status == "warn" else "✗")
                print(f"  {icon} {name}: {message}")
            print()
            return

        # Generic handling
        if isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        elif isinstance(value, list):
            if not value:
                return  # Skip empty lists
            print(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        print(f"  {k}: {v}")
                    print()
                else:
                    print(f"  - {item}")
        else:
            print(f"{key}: {value}")

    def error(
        self,
        code: str,
        message: str,
        next_steps: list[str] | None = None,
    ) -> None:
        """Output an error response."""
        if self.human:
            self._render_human_error(code, message, next_steps)
        else:
            self._render_json_error(code, message, next_steps)

    def _render_json_error(
        self,
        code: str,
        message: str,
        next_steps: list[str] | None,
    ) -> None:
        """Render error as JSON."""
        response = {
            "success": False,
            "error": {
                "code": code,
                "message": message,
            },
            "next_steps": next_steps or [],
        }
        if self.verbose and self._debug_info:
            response["debug"] = self._debug_info
        print(json.dumps(response, indent=2))

    def _render_human_error(
        self,
        code: str,
        message: str,
        next_steps: list[str] | None,
    ) -> None:
        """Render error as human-readable text."""
        print(f"Error [{code}]: {message}", file=sys.stderr)

        if next_steps:
            print()
            print("To fix:")
            for step in next_steps:
                print(f"  - {step}")
