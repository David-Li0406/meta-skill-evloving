#!/usr/bin/env python3
"""Run the email sender MCP server."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mcp_servers.email_sender import mcp

if __name__ == "__main__":
    mcp.run()
