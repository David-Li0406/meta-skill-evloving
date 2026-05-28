#!/usr/bin/env python3
"""Verify posting-instagram skill is properly configured."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path (5 levels up from verify.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
load_dotenv(PROJECT_ROOT / "config" / ".env")


def verify():
    errors = []

    # Check environment variables
    required_env_vars = ["META_ACCESS_TOKEN", "INSTAGRAM_ACCOUNT_ID"]

    for var in required_env_vars:
        if not os.getenv(var):
            errors.append(f"Missing environment variable: {var}")

    # Check MCP server file exists
    mcp_server = PROJECT_ROOT / "src" / "mcp_servers" / "meta_social_connector.py"
    if not mcp_server.exists():
        errors.append("MCP server not found: src/mcp_servers/meta_social_connector.py")

    # Check dependencies
    try:
        import requests
        import fastmcp
    except ImportError as e:
        errors.append(f"Missing dependency: {e.name}")

    # Check vault structure
    vault_path = PROJECT_ROOT / "Vault"
    required_dirs = ["Pending_Approval", "Approved", "Logs"]
    for dir_name in required_dirs:
        if not (vault_path / dir_name).exists():
            errors.append(f"Missing directory: Vault/{dir_name}")

    if errors:
        print("[FAIL] posting-instagram invalid:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("[OK] posting-instagram valid")
    return 0


if __name__ == "__main__":
    sys.exit(verify())
