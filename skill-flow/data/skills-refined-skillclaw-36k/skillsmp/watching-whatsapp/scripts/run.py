#!/usr/bin/env python3
"""Run the WhatsApp watcher skill."""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from watchers.whatsapp_watcher import main

if __name__ == "__main__":
    asyncio.run(main())
