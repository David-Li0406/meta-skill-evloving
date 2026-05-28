#!/usr/bin/env python3
"""
UserPromptSubmit Hook: Tattoo Injection + Smart Reminders

Injects a persistent "tattoo" reminder on every prompt - tools and rules
that Claude should always have visible, like Lester's tattoos in Memento.

Also detects credential-related queries and injects the right command.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from common import read_hook_input, print_hook_output


# Keywords that indicate user is looking for credentials
CREDENTIAL_KEYWORDS = {
    'credential', 'credentials', 'password', 'passwords', 'login', 'logins',
    'secret', 'secrets', 'token', 'tokens', 'api key', 'api keys',
    'ssh', 'ftp', 'admin password', 'wp-admin', 'staging',
    'what is the password', 'what are the credentials', 'how do i login',
    'username', 'auth'
}


def main():
    """Inject tattoo on every prompt, with smart credential detection."""
    hook_input = read_hook_input()

    # Get user's prompt text
    user_prompt = ""
    if hook_input:
        user_prompt = hook_input.get("userPromptContent", "").lower()

    # Base TATTOO: Always-visible reminders
    tattoo = "TOOLS (--help): p --list | op | dev-browser | wp-test | memorize | recall | t --list (all tools) → direct, NEVER interactive, servers need nohup & | /recall if lost | REMEMBER TO MEMORIZE 💾 (for the TEAM, not you!)"

    # SMART INJECTION: Detect credential queries and add reminder
    if user_prompt and any(kw in user_prompt for kw in CREDENTIAL_KEYWORDS):
        tattoo += "\n\n🔑 CREDENTIALS: Use `memory creds` (all) or `memory creds <project>` (filtered). NOT search!"

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": tattoo
        },
        "suppressOutput": True
    }
    print_hook_output(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
