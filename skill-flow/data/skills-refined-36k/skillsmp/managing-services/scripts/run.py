#!/usr/bin/env python3
"""Run the service manager skill."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from service_manager import main

if __name__ == "__main__":
    main()
