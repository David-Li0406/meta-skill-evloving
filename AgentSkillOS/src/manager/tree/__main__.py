"""
Allow running as: python -m manager.tree

Redirects to the unified CLI with appropriate subcommands.
Usage:
    python -m manager.tree build
    python -m manager.tree search "query"
    python -m manager.tree list
"""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cli import main

if __name__ == "__main__":
    main()
