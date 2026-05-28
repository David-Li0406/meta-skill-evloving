#!/usr/bin/env python3
"""Run the orchestrator skill."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from orchestrator import main

if __name__ == "__main__":
    main()
