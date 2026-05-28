#!/usr/bin/env python3
"""Verify sending-emails skill."""
import sys
from pathlib import Path

def verify():
    errors = []
    ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    if not (ROOT / "config" / "credentials.json").exists():
        errors.append("Missing config/credentials.json")
    if not (ROOT / "src" / "mcp_servers" / "email_sender.py").exists():
        errors.append("Missing src/mcp_servers/email_sender.py")
    
    try:
        import fastmcp
    except ImportError:
        errors.append("Missing: fastmcp")
    
    if errors:
        print("[FAIL] sending-emails invalid:")
        for e in errors: print(f"  - {e}")
        return 1
    print("[OK] sending-emails valid")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
