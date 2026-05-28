#!/usr/bin/env python3
"""Verify digital-fte-orchestrator skill."""
import sys
from pathlib import Path

def verify():
    errors = []
    ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    for folder in ["Needs_Action", "Pending_Approval", "Approved", "Done", "Logs"]:
        if not (ROOT / "Vault" / folder).exists():
            errors.append(f"Missing Vault/{folder}")
    
    if not (ROOT / "Vault" / "Company_Handbook.md").exists():
        errors.append("Missing Vault/Company_Handbook.md")
    if not (ROOT / "src" / "orchestrator.py").exists():
        errors.append("Missing src/orchestrator.py")
    
    if errors:
        print("[FAIL] digital-fte-orchestrator invalid:")
        for e in errors: print(f"  - {e}")
        return 1
    print("[OK] digital-fte-orchestrator valid")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
