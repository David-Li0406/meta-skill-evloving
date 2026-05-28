#!/usr/bin/env python3
"""Verify managing-services skill."""
import sys
from pathlib import Path

def verify():
    errors = []
    ROOT = Path(__file__).parent.parent.parent.parent.parent
    
    if not (ROOT / "src" / "service_manager.py").exists():
        errors.append("Missing src/service_manager.py")
    if not (ROOT / "Vault" / "Logs").exists():
        errors.append("Missing Vault/Logs")
    
    # Check all managed services exist
    services = [
        "src/watchers/gmail_watcher.py",
        "src/watchers/whatsapp_watcher.py",
        "src/watchers/filesystem_watcher.py",
        "src/orchestrator.py"
    ]
    for svc in services:
        if not (ROOT / svc).exists():
            errors.append(f"Missing {svc}")
    
    if errors:
        print("[FAIL] managing-services invalid:")
        for e in errors: print(f"  - {e}")
        return 1
    print("[OK] managing-services valid")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
