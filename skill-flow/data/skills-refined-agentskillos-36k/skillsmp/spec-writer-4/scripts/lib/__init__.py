"""
Shared library modules for spec-writer helper scripts.
"""

from pathlib import Path
import sys

def find_discovery_dir(discovery_path: str = None) -> Path:
    """
    Smart discovery/ directory resolution.

    Priority:
    1. Explicit --discovery-path
    2. Current directory if in discovery/
    3. Auto-locate in parent directories

    Args:
        discovery_path: Optional explicit path to discovery/ directory

    Returns:
        Path to discovery/ directory

    Raises:
        FileNotFoundError: If discovery/ directory not found
    """
    # Priority 1: Explicit --discovery-path
    if discovery_path:
        path = Path(discovery_path).resolve()
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Directory not found: {path}")
        return path

    # Priority 2: Current directory if in discovery/
    if Path.cwd().name == "discovery":
        return Path.cwd()

    # Priority 3: Auto-locate in parent directories
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        discovery = parent / "discovery"
        if discovery.exists() and discovery.is_dir():
            return discovery

    raise FileNotFoundError(
        "discovery/ directory not found. "
        "Run from within discovery/, provide --discovery-path, "
        "or ensure discovery/ exists in a parent directory."
    )

__all__ = ['find_discovery_dir']
