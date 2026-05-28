#!/usr/bin/env python3
"""Run the Gmail watcher skill."""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Import and run the watcher
from watchers.gmail_watcher import main

if __name__ == "__main__":
    main()
