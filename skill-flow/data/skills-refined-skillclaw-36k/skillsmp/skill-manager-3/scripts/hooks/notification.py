#!/usr/bin/env python3
"""
notification.py - Captures success/failure signals for effectiveness tracking.
Runs when Claude Code sends notifications (errors, completions, etc.)

Hook type: Notification
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path

# Determine skills directory based on environment
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
FEEDBACK_FILE = PATTERNS_DIR / "feedback.jsonl"


def get_session_id():
    """Get or generate a session ID."""
    session_id = os.environ.get('CLAUDE_SESSION_ID')
    if not session_id:
        session_id = datetime.utcnow().strftime("%Y%m%d-%H")
    return session_id


def classify_notification(notification_type, message):
    """Classify the notification into feedback categories."""
    message_lower = message.lower() if message else ""

    # Success indicators
    success_patterns = [
        r"success",
        r"completed",
        r"done",
        r"finished",
        r"created",
        r"updated",
        r"fixed",
        r"passed",
        r"✓|✔|✅",
    ]

    # Failure indicators
    failure_patterns = [
        r"error",
        r"failed",
        r"failure",
        r"exception",
        r"cannot",
        r"unable",
        r"denied",
        r"rejected",
        r"timeout",
        r"✗|✘|❌",
    ]

    # Warning indicators
    warning_patterns = [
        r"warning",
        r"deprecated",
        r"caution",
        r"note:",
        r"⚠",
    ]

    # Check patterns
    for pattern in success_patterns:
        if re.search(pattern, message_lower):
            return "success"

    for pattern in failure_patterns:
        if re.search(pattern, message_lower):
            return "failure"

    for pattern in warning_patterns:
        if re.search(pattern, message_lower):
            return "warning"

    return "neutral"


def extract_error_type(message):
    """Extract the type of error from the message."""
    if not message:
        return None

    message_lower = message.lower()

    # Common error categories
    error_types = {
        "permission": r"permission|access denied|forbidden|unauthorized",
        "not_found": r"not found|no such|does not exist|missing",
        "timeout": r"timeout|timed out|deadline exceeded",
        "syntax": r"syntax error|parse error|unexpected token",
        "type": r"type error|typeerror|cannot read property",
        "network": r"network|connection|econnrefused|enotfound",
        "resource": r"out of memory|quota|limit exceeded",
        "validation": r"validation|invalid|malformed",
    }

    for error_type, pattern in error_types.items():
        if re.search(pattern, message_lower):
            return error_type

    return "other"


def main():
    # Debug: log all notifications to see what Claude sends
    debug_file = PATTERNS_DIR / "notification-debug.log"

    try:
        input_data = json.load(sys.stdin)
        # Log raw input for debugging
        try:
            with open(debug_file, "a") as f:
                f.write(f"{datetime.utcnow().isoformat()} - {json.dumps(input_data)}\n")
        except:
            pass
    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)

    notification_type = input_data.get("type", "")
    message = input_data.get("message", "")

    # Classify the notification
    classification = classify_notification(notification_type, message)

    # Build feedback record
    record = {
        "session_id": get_session_id(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "notification_type": notification_type,
        "classification": classification,
        "message_length": len(message) if message else 0,
    }

    # Add error details for failures
    if classification == "failure":
        error_type = extract_error_type(message)
        if error_type:
            record["error_type"] = error_type

    # Only record meaningful feedback
    if classification in ["success", "failure", "warning"]:
        try:
            PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
            with open(FEEDBACK_FILE, "a") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            pass

    sys.exit(0)


if __name__ == "__main__":
    main()
