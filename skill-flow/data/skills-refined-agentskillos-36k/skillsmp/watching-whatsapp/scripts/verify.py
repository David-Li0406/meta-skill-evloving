#!/usr/bin/env python3
"""Verify watching-whatsapp skill."""
import sys
from pathlib import Path

def verify():
    errors = []
    ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    if not (ROOT / "Vault" / "Needs_Action").exists():
        errors.append("Missing Vault/Needs_Action")
    if not (ROOT / "src" / "watchers" / "whatsapp_watcher.py").exists():
        errors.append("Missing src/watchers/whatsapp_watcher.py")
    
    try:
        import playwright
    except ImportError:
        errors.append("Missing: playwright")
    
    if errors:
        print("[FAIL] watching-whatsapp invalid:")
        for e in errors: print(f"  - {e}")
        return 1
    print("[OK] watching-whatsapp valid")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
