#!/usr/bin/env python3
"""Verify posting-linkedin skill."""
import sys
from pathlib import Path

def verify():
    errors = []
    ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    if not (ROOT / "Vault" / "LinkedIn_Queue").exists():
        errors.append("Missing Vault/LinkedIn_Queue")
    if not (ROOT / "Vault" / "Pending_Approval").exists():
        errors.append("Missing Vault/Pending_Approval")
    if not (ROOT / "src" / "linkedin" / "linkedin_poster.py").exists():
        errors.append("Missing src/linkedin/linkedin_poster.py")
    
    try:
        import playwright
    except ImportError:
        errors.append("Missing: playwright")
    
    if errors:
        print("[FAIL] posting-linkedin invalid:")
        for e in errors: print(f"  - {e}")
        return 1
    print("[OK] posting-linkedin valid")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
