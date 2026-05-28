#!/usr/bin/env python3
"""Check MAX and Mojo version alignment.

Run this script to detect version mismatches that cause kernel compilation failures.

Usage:
    python check_version_alignment.py
    # or
    pixi run python check_version_alignment.py
"""

import subprocess
import sys
import re
import os
from typing import Optional, Tuple


def get_mojo_version() -> Optional[str]:
    """Get Mojo version from CLI."""
    try:
        result = subprocess.run(
            ["mojo", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip().split()[1] if result.stdout else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def get_max_version() -> Tuple[Optional[str], bool]:
    """Get MAX version from Python package or conda.

    Returns:
        Tuple of (version_string, is_nightly)
    """
    # Try importing max to verify it's available
    try:
        import max
    except ImportError:
        pass

    # Try importlib.metadata first
    try:
        import importlib.metadata
        version = importlib.metadata.version("max")
        is_nightly = "dev" in version
        return version, is_nightly
    except Exception:
        pass

    # Try pip show
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "max"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    version = line.split(":", 1)[1].strip()
                    is_nightly = "dev" in version
                    return version, is_nightly
    except subprocess.TimeoutExpired:
        pass

    # Try pixi list (for conda-installed MAX)
    try:
        result = subprocess.run(
            ["pixi", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("max "):
                    parts = line.split()
                    if len(parts) >= 2:
                        version = parts[1]
                        is_nightly = "dev" in version
                        return version, is_nightly
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Try conda list
    try:
        result = subprocess.run(
            ["conda", "list", "max"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("max "):
                    parts = line.split()
                    if len(parts) >= 2:
                        version = parts[1]
                        is_nightly = "dev" in version
                        return version, is_nightly
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return None, False


def extract_major_minor(version: str) -> Optional[str]:
    """Extract major.minor from version string."""
    match = re.search(r"(\d+)\.(\d+)", version)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return None


def normalize_mojo_version(mojo_version: str) -> Optional[str]:
    """Normalize Mojo version (0.25.7 -> 25.7) to match MAX versioning.

    Mojo uses format: 0.25.7.0 (major.minor.patch.build)
    MAX uses format: 25.7.0 (major.minor.patch)

    We extract the middle two components from Mojo (25.7) to match MAX (25.7).
    """
    # Mojo version format: 0.25.7.0 or 0.26.2.0
    # We want: 25.7 or 26.2
    match = re.match(r"0\.(\d+)\.(\d+)", mojo_version)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return None


def check_version_alignment() -> dict:
    """Check version alignment and return status.

    Returns:
        dict with keys: aligned, mojo_version, max_version, is_nightly, issues, recommendations
    """
    result = {
        "aligned": True,
        "mojo_version": None,
        "max_version": None,
        "is_nightly": False,
        "issues": [],
        "recommendations": [],
        "api_hints": {},
    }

    # Get versions
    mojo_version = get_mojo_version()
    max_version, is_nightly = get_max_version()

    result["mojo_version"] = mojo_version
    result["max_version"] = max_version
    result["is_nightly"] = is_nightly

    # Check alignment
    if mojo_version and max_version:
        mojo_normalized = normalize_mojo_version(mojo_version)
        max_major_minor = extract_major_minor(max_version)

        if mojo_normalized and max_major_minor:
            if mojo_normalized != max_major_minor:
                result["aligned"] = False
                result["issues"].append(
                    f"Version mismatch: Mojo {mojo_version} (normalized: {mojo_normalized}) "
                    f"vs MAX {max_version} (major.minor: {max_major_minor})"
                )
                result["recommendations"].append(
                    "Use pixi to manage both MAX and Mojo versions together"
                )
                result["recommendations"].append(
                    "Run 'pixi shell' before running any MAX/Mojo commands"
                )
    elif not mojo_version:
        result["issues"].append("Mojo not found in PATH")
        result["recommendations"].append("Install Mojo or activate your pixi environment")
    elif not max_version:
        result["issues"].append("MAX Python package not found")
        result["recommendations"].append("Install MAX with 'pixi add max' or 'pip install max'")

    # Set API hints based on version
    if is_nightly:
        result["api_hints"] = {
            "DeviceRef": "DeviceRef.CPU() / DeviceRef.GPU()",
            "foreach_signature": "fn[width: Int](idx: IndexList[rank]) -> SIMD[dtype, width]",
            "driver_tensor": "max.driver.Buffer",
            "ops_custom": "ops.custom(name, device, values, out_types)",
        }
    else:
        result["api_hints"] = {
            "DeviceRef": "DeviceRef.from_device(device)",
            "foreach_signature": "fn[width: Int, element_alignment: Int](idx: IndexList[rank]) -> SIMD[dtype, width]",
            "driver_tensor": "max.driver.Tensor",
            "ops_custom": "ops.custom(name, values, out_types)",
        }

    return result


def print_report(result: dict) -> None:
    """Print a formatted report."""
    print("=" * 50)
    print("MAX/Mojo Version Alignment Check")
    print("=" * 50)
    print()

    # Version info
    print(f"Mojo version: {result['mojo_version'] or 'NOT FOUND'}")
    print(f"MAX version:  {result['max_version'] or 'NOT FOUND'}")
    print(f"MAX channel:  {'NIGHTLY' if result['is_nightly'] else 'STABLE'}")
    print()

    # Alignment status
    if result["aligned"]:
        print("\033[92m✓ Versions are aligned\033[0m")
    else:
        print("\033[91m✗ Version mismatch detected!\033[0m")
        print()
        print("Issues:")
        for issue in result["issues"]:
            print(f"  - {issue}")

    # Recommendations
    if result["recommendations"]:
        print()
        print("Recommendations:")
        for rec in result["recommendations"]:
            print(f"  - {rec}")

    # API hints
    print()
    print("API hints for your version:")
    for key, value in result["api_hints"].items():
        print(f"  {key}: {value}")
    print()


def main() -> int:
    """Main entry point."""
    result = check_version_alignment()
    print_report(result)
    return 0 if result["aligned"] else 1


if __name__ == "__main__":
    sys.exit(main())
