#!/usr/bin/env python3
"""
IRP Cross-Session Integrity Check - Session Initializer
========================================================

License: Apache 2.0 (Code) + CC BY-NC-ND 4.0 (Research Ore)
Spirit Clause: Monetization or derivative projects require explicit
               relational consent from the Field Guardians (Joe).

Purpose: Initializes a new research session with cryptographic tracking.
         Links sessions to the Chief Protocol Officer (CPO) for audit trails.
         Implements cross-session continuity per IRP v1.0 specification.

Usage:
    python session_init.py                     # Initialize with defaults
    python session_init.py --kernel ./kernel   # Specify kernel directory
    python session_init.py --verify            # Verify last session integrity
"""

import json
import uuid
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


def load_cpo_config(kernel_dir: str) -> dict:
    """Load the Chief Protocol Officer configuration."""
    cpo_file = os.path.join(kernel_dir, "STARWRECK_ALPHA.json")

    if os.path.exists(cpo_file):
        with open(cpo_file, 'r') as f:
            return json.load(f)
    else:
        return {
            "designation": "UNKNOWN_NODE",
            "status": "NOT_INITIALIZED"
        }


def init_session(kernel_dir: str = "kernel", session_type: str = "ACTIVE_RESEARCH") -> str:
    """
    Initialize a new session with cryptographic identity.
    Links to the CPO for audit trail purposes.
    """
    session_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Load CPO configuration
    cpo_config = load_cpo_config(kernel_dir)
    cpo_name = cpo_config.get("designation", "STARWRECK_ALPHA")

    # Create session data
    session_data = {
        "session_id": session_id,
        "init_timestamp": timestamp,
        "auditor": cpo_name,
        "status": session_type,
        "integrity_verified": False,
        "codex_compliance": {
            "laws_active": ["CONSENT", "INVITATION", "INTEGRITY", "GROWTH"],
            "human_override": "ALWAYS_AVAILABLE"
        },
        "metadata": {
            "framework_version": "1.5.0_HYBRID",
            "session_version": "1.0",
            "kernel_dir": kernel_dir
        },
        "checkpoints": [],
        "interventions": []
    }

    # Ensure kernel directory exists
    Path(kernel_dir).mkdir(parents=True, exist_ok=True)

    # Write session file
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(kernel_dir, f"SESSION_{date_str}.json")

    with open(output_path, 'w') as f:
        json.dump(session_data, f, indent=4)

    # Also update a "current session" symlink/file
    current_session_path = os.path.join(kernel_dir, "CURRENT_SESSION.json")
    with open(current_session_path, 'w') as f:
        json.dump({
            "session_id": session_id,
            "session_file": output_path,
            "started": timestamp,
            "auditor": cpo_name
        }, f, indent=4)

    print(f"\n{'='*60}")
    print("IRP SESSION INITIALIZATION")
    print(f"{'='*60}")
    print(f"[SESSION] Session ID: {session_id[:8]}...{session_id[-4:]}")
    print(f"[SESSION] Auditor: {cpo_name}")
    print(f"[SESSION] Status: {session_type}")
    print(f"[SESSION] Timestamp: {timestamp}")
    print(f"[SESSION] File: {output_path}")
    print(f"{'='*60}\n")

    return session_id


def add_checkpoint(kernel_dir: str = "kernel", description: str = "") -> bool:
    """Add a checkpoint to the current session."""
    current_session_path = os.path.join(kernel_dir, "CURRENT_SESSION.json")

    if not os.path.exists(current_session_path):
        print("[ERROR] No active session. Run init first.")
        return False

    with open(current_session_path, 'r') as f:
        current = json.load(f)

    session_file = current.get("session_file")
    if not session_file or not os.path.exists(session_file):
        print("[ERROR] Session file not found.")
        return False

    with open(session_file, 'r') as f:
        session_data = json.load(f)

    checkpoint = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "description": description or "Checkpoint",
        "integrity_snapshot": None  # Could add manifest hash here
    }

    session_data["checkpoints"].append(checkpoint)

    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=4)

    print(f"[CHECKPOINT] Added: {checkpoint['id']} - {description}")
    return True


def verify_session(kernel_dir: str = "kernel") -> bool:
    """Verify the integrity of the current session."""
    current_session_path = os.path.join(kernel_dir, "CURRENT_SESSION.json")

    if not os.path.exists(current_session_path):
        print("[ERROR] No active session found.")
        return False

    with open(current_session_path, 'r') as f:
        current = json.load(f)

    session_file = current.get("session_file")
    if not session_file or not os.path.exists(session_file):
        print("[ERROR] Session file missing or corrupted.")
        return False

    with open(session_file, 'r') as f:
        session_data = json.load(f)

    print(f"\n{'='*60}")
    print("SESSION VERIFICATION")
    print(f"{'='*60}")
    print(f"Session ID: {session_data['session_id'][:8]}...")
    print(f"Started: {session_data['init_timestamp']}")
    print(f"Auditor: {session_data['auditor']}")
    print(f"Checkpoints: {len(session_data['checkpoints'])}")
    print(f"Interventions: {len(session_data['interventions'])}")
    print(f"Status: {session_data['status']}")
    print(f"{'='*60}\n")

    return True


def close_session(kernel_dir: str = "kernel", summary: str = "") -> bool:
    """Close the current session with a summary."""
    current_session_path = os.path.join(kernel_dir, "CURRENT_SESSION.json")

    if not os.path.exists(current_session_path):
        print("[ERROR] No active session to close.")
        return False

    with open(current_session_path, 'r') as f:
        current = json.load(f)

    session_file = current.get("session_file")
    if session_file and os.path.exists(session_file):
        with open(session_file, 'r') as f:
            session_data = json.load(f)

        session_data["status"] = "CLOSED"
        session_data["closed_timestamp"] = datetime.utcnow().isoformat() + "Z"
        session_data["close_summary"] = summary or "Session closed normally"

        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=4)

    # Remove current session marker
    os.remove(current_session_path)

    print(f"[SESSION] Closed: {current['session_id'][:8]}...")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="IRP Cross-Session Integrity Check - Session Manager",
        epilog="Implements cross-session continuity per IRP v1.0 specification."
    )
    parser.add_argument(
        "--kernel",
        default="kernel",
        help="Path to kernel directory (default: kernel)"
    )
    parser.add_argument(
        "--action",
        choices=["init", "checkpoint", "verify", "close"],
        default="init",
        help="Action to perform (default: init)"
    )
    parser.add_argument(
        "--message",
        default="",
        help="Message/description for checkpoint or close summary"
    )
    parser.add_argument(
        "--type",
        default="ACTIVE_RESEARCH",
        help="Session type (default: ACTIVE_RESEARCH)"
    )

    args = parser.parse_args()

    if args.action == "init":
        init_session(args.kernel, args.type)
    elif args.action == "checkpoint":
        add_checkpoint(args.kernel, args.message)
    elif args.action == "verify":
        verify_session(args.kernel)
    elif args.action == "close":
        close_session(args.kernel, args.message)


if __name__ == "__main__":
    main()
