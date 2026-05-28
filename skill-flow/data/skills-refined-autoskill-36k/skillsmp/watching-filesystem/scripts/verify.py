#!/usr/bin/env python3
"""Verify watching-filesystem skill."""
import sys
from pathlib import Path

def verify():
    errors = []
    ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    if not (ROOT / "Vault" / "Needs_Action").exists():
        errors.append("Missing Vault/Needs_Action")
    if not (ROOT / "DropFolder").exists():
        errors.append("Missing DropFolder")
    if not (ROOT / "src" / "watchers" / "filesystem_watcher.py").exists():
        errors.append("Missing src/watchers/filesystem_watcher.py")
    
    try:
        import watchdog
    except ImportError:
        errors.append("Missing: watchdog")
    
    if errors:
        print("[FAIL] watching-filesystem invalid:")
        for e in errors: print(f"  - {e}")
        return 1
    print("[OK] watching-filesystem valid")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
