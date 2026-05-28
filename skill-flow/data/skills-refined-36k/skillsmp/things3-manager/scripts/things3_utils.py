#!/usr/bin/env python3
"""
Things3 Utilities - Helper functions for Things3 operations.
"""

import subprocess
import time
import sys


def ensure_things_running(wait_seconds=1):
    """
    Ensure Things3 is running and synced.
    Opens Things if not running, waits briefly for sync.
    """
    # Check if Things is running
    result = subprocess.run(
        ["pgrep", "-x", "Things3"],
        capture_output=True,
        text=True
    )
    
    was_running = result.returncode == 0
    
    if not was_running:
        # Open Things
        subprocess.run(["open", "-a", "Things3"], check=True)
        # Wait for it to launch and sync
        time.sleep(wait_seconds + 1)
    else:
        # Already running, just give it a moment to ensure db is fresh
        # Activate it briefly to trigger any pending sync
        subprocess.run(["open", "-a", "Things3"], check=True)
        time.sleep(wait_seconds)
    
    return was_running


def get_auth_token():
    """Get the Things URL scheme auth token."""
    try:
        import things
        return things.token()
    except ImportError:
        print("Error: things.py not installed. Run: pip install things.py", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error getting auth token: {e}", file=sys.stderr)
        return None


def check_things_url_enabled():
    """Check if Things URL scheme is enabled by trying to get the token."""
    token = get_auth_token()
    if not token:
        print("Warning: Things URL scheme may not be enabled.", file=sys.stderr)
        print("Enable it in: Things → Settings → General → Enable Things URLs", file=sys.stderr)
        return False
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Things3 Utilities")
    parser.add_argument("command", choices=["sync", "check-token", "ensure-running"],
                       help="Utility command to run")
    parser.add_argument("--wait", type=int, default=1, help="Seconds to wait for sync")
    
    args = parser.parse_args()
    
    if args.command == "sync" or args.command == "ensure-running":
        was_running = ensure_things_running(args.wait)
        status = "was already running" if was_running else "was launched"
        print(f"✓ Things3 {status} and synced")
    
    elif args.command == "check-token":
        if check_things_url_enabled():
            print(f"✓ Things URL scheme is enabled")
            print(f"  Token: {get_auth_token()}")
        else:
            sys.exit(1)
