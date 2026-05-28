#!/usr/bin/env python3
"""Verify generating-ceo-briefing skill."""
import sys
from pathlib import Path

def verify():
    errors = []
    ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    if not (ROOT / "Vault" / "Logs").exists():
        errors.append("Missing Vault/Logs")
    if not (ROOT / "src" / "reports" / "ceo_briefing.py").exists():
        errors.append("Missing src/reports/ceo_briefing.py")
    
    if errors:
        print("[FAIL] generating-ceo-briefing invalid:")
        for e in errors: print(f"  - {e}")
        return 1
    print("[OK] generating-ceo-briefing valid")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
