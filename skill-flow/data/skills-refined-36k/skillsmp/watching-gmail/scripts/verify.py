#!/usr/bin/env python3
"""Verify watching-gmail skill."""
import sys
from pathlib import Path

def verify():
    errors = []
    ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    if not (ROOT / "config" / "credentials.json").exists():
        errors.append("Missing config/credentials.json")
    if not (ROOT / "Vault" / "Needs_Action").exists():
        errors.append("Missing Vault/Needs_Action")
    if not (ROOT / "src" / "watchers" / "gmail_watcher.py").exists():
        errors.append("Missing src/watchers/gmail_watcher.py")
    
    try:
        import google.oauth2.credentials
    except ImportError:
        errors.append("Missing: google-auth-oauthlib")
    
    if errors:
        print("[FAIL] watching-gmail invalid:")
        for e in errors: print(f"  - {e}")
        return 1
    print("[OK] watching-gmail valid")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
