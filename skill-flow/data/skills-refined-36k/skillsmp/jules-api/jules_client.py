#!/usr/bin/env python3
"""Jules API Client Helper
A simple Python client for interacting with Google's Jules API.
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Any

import requests


class JulesClient:
    """Client for Google Jules API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        """Initialize the Jules client.

        Args:
            api_key: Jules API key. If not provided, will check JULES_API_KEY
                     environment variable, then fall back to gcloud auth.
            base_url: The base URL for the Jules API. If not provided, will
                      check JULES_BASE_URL environment variable, then fall back
                      to the default production URL.

        """
        self.api_key = api_key or os.environ.get("JULES_API_KEY")
        self.base_url = base_url or os.environ.get("JULES_BASE_URL", "https://jules.googleapis.com/v1alpha")
        self.access_token = None
        self.using_oauth = False  # Track if we're using OAuth vs API key

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Goog-Api-Key"] = self.api_key
        else:
            if not self.access_token:
                try:
                    result = subprocess.run(
                        ["gcloud", "auth", "print-access-token"],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    self.access_token = result.stdout.strip()
                except subprocess.CalledProcessError as e:
                    msg = (
                        "Failed to get access token. Make sure you either:\n"
                        "1. Set JULES_API_KEY environment variable, or\n"
                        "2. Authenticate with gcloud: gcloud auth login"
                    )
                    raise Exception(msg) from e
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def create_session(  # noqa: PLR0913
        self,
        prompt: str,
        owner: str,
        repo: str,
        branch: str = "main",
        title: str | None = None,
        require_plan_approval: bool = False,
        automation_mode: str = "AUTO_CREATE_PR",
    ) -> dict[str, Any]:
        """Create a new Jules session.

        Args:
            prompt: The task description
            owner: GitHub repository owner
            repo: GitHub repository name
            branch: Starting branch name (default: main)
            title: Optional session title
            require_plan_approval: Whether to require manual plan approval
            automation_mode: Automation mode (AUTO_CREATE_PR or MANUAL)

        Returns:
            Session object with id, state, etc.

        """
        url = f"{self.base_url}/sessions"
        data = {
            "prompt": prompt,
            "sourceContext": {
                "source": f"sources/github/{owner}/{repo}",
                "githubRepoContext": {"startingBranch": branch},
            },
            "automationMode": automation_mode,
        }

        if title:
            data["title"] = title

        if require_plan_approval:
            data["requirePlanApproval"] = require_plan_approval

        response = requests.post(url, headers=self._get_headers(), json=data)
        response.raise_for_status()
        return response.json()

    def get_session(self, session_id: str) -> dict[str, Any]:
        """Get details of a specific session.

        Args:
            session_id: The session ID (with or without "sessions/" prefix)

        Returns:
            Session object

        """
        # Handle both "sessions/123" and "123" formats
        if session_id.startswith("sessions/"):
            session_id = session_id.split("/")[-1]

        url = f"{self.base_url}/sessions/{session_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def list_sessions(self) -> dict[str, Any]:
        """List all sessions.

        Returns:
            List of session objects

        """
        url = f"{self.base_url}/sessions"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def send_message(self, session_id: str, message: str) -> dict[str, Any]:
        """Send a message to an active session.

        Args:
            session_id: The session ID (with or without "sessions/" prefix)
            message: Message content

        Returns:
            Updated session object

        """
        # Handle both "sessions/123" and "123" formats
        if session_id.startswith("sessions/"):
            session_id = session_id.split("/")[-1]

        url = f"{self.base_url}/sessions/{session_id}:sendMessage"
        data = {"prompt": message}
        response = requests.post(url, headers=self._get_headers(), json=data)
        response.raise_for_status()
        return response.json()

    def approve_plan(self, session_id: str) -> dict[str, Any]:
        """Approve a plan for a session.

        Args:
            session_id: The session ID (with or without "sessions/" prefix)

        Returns:
            Updated session object

        """
        # Handle both "sessions/123" and "123" formats
        if session_id.startswith("sessions/"):
            session_id = session_id.split("/")[-1]

        url = f"{self.base_url}/sessions/{session_id}:approvePlan"
        response = requests.post(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_activities(self, session_id: str) -> dict[str, Any]:
        """Get activities for a session.

        Args:
            session_id: The session ID (with or without "sessions/" prefix)

        Returns:
            Dictionary with 'activities' list containing activity objects

        """
        # Handle both "sessions/123" and "123" formats
        if session_id.startswith("sessions/"):
            session_id = session_id.split("/")[-1]

        url = f"{self.base_url}/sessions/{session_id}/activities"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def check_session_needs_attention(self, session_id: str) -> tuple[bool, str]:
        """Check if a session needs user attention.

        Args:
            session_id: The session ID (with or without "sessions/" prefix)

        Returns:
            Tuple of (needs_attention: bool, reason: str)

        """
        session = self.get_session(session_id)
        state = session.get('state', 'UNKNOWN')

        if state == 'AWAITING_USER_FEEDBACK':
            return True, "Session is waiting for user feedback"
        elif state == 'AWAITING_PLAN_APPROVAL':
            return True, "Session plan needs approval"
        elif state == 'FAILED':
            return True, "Session failed"
        elif state == 'COMPLETED':
            return False, "Session completed successfully"
        elif state in ['IN_PROGRESS', 'PLANNING', 'QUEUED']:
            return False, f"Session is active ({state})"
        else:
            return False, f"Session state: {state}"


def main(argv: list[str] | None = None) -> None:
    """CLI interface for Jules API."""
    parser = argparse.ArgumentParser(description="Jules API Client Helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new Jules session")
    create_parser.add_argument("prompt", help="The task description")
    create_parser.add_argument("owner", help="GitHub repository owner")
    create_parser.add_argument("repo", help="GitHub repository name")
    create_parser.add_argument("--branch", default="main", help="Starting branch name")
    create_parser.add_argument("--title", help="Optional session title")
    create_parser.add_argument(
        "--require-plan-approval", action="store_true", help="Require manual plan approval"
    )
    create_parser.add_argument(
        "--automation-mode",
        default="AUTO_CREATE_PR",
        help="Automation mode (AUTO_CREATE_PR or MANUAL)",
    )

    # Get command
    get_parser = subparsers.add_parser("get", help="Get details of a specific session")
    get_parser.add_argument("session_id", help="The session ID")

    # List command
    subparsers.add_parser("list", help="List all sessions")

    # Message command
    message_parser = subparsers.add_parser("message", help="Send a message to an active session")
    message_parser.add_argument("session_id", help="The session ID")
    message_parser.add_argument("message", nargs="+", help="Message content")

    # Approve command
    approve_parser = subparsers.add_parser("approve-plan", help="Approve a plan for a session")
    approve_parser.add_argument("session_id", help="The session ID")

    # Activities command
    activities_parser = subparsers.add_parser("activities", help="Get activities for a session")
    activities_parser.add_argument("session_id", help="The session ID")

    # Check command
    check_parser = subparsers.add_parser("check", help="Check if session needs attention")
    check_parser.add_argument("session_id", help="The session ID")

    # Add --json flag to parser
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args(argv)
    client = JulesClient()

    try:
        if args.command == "create":
            result = client.create_session(
                prompt=args.prompt,
                owner=args.owner,
                repo=args.repo,
                branch=args.branch,
                title=args.title,
                require_plan_approval=args.require_plan_approval,
                automation_mode=args.automation_mode,
            )
            session_id = result['name'].split('/')[-1]
            print(f"✅ Session created: {session_id}")
            print(f"URL: https://jules.google.com/sessions/{session_id}")

        elif args.command == "get":
            result = client.get_session(args.session_id)

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                session_id = result['name'].split('/')[-1]
                print(f"Session: {session_id}")
                print(f"State: {result.get('state', 'UNKNOWN')}")
                print(f"Created: {result.get('createTime', 'N/A')}")
                if result.get('title'):
                    print(f"Title: {result['title']}")
                print(f"\nURL: https://jules.google.com/sessions/{session_id}")

        elif args.command == "list":
            result = client.list_sessions()
            sessions = result.get('sessions', [])
            print(f"Found {len(sessions)} sessions:\n")
            for session in sessions[:10]:  # Show first 10
                session_id = session['name'].split('/')[-1]
                state = session.get('state', 'UNKNOWN')
                title = session.get('title', 'No title')[:50]
                print(f"  {session_id} | {state:20} | {title}")

        elif args.command == "message":
            message = " ".join(args.message)
            result = client.send_message(args.session_id, message)
            print(f"✅ Message sent to session {args.session_id}")

        elif args.command == "approve-plan":
            result = client.approve_plan(args.session_id)
            print(f"✅ Plan approved for session {args.session_id}")

        elif args.command == "activities":
            result = client.get_activities(args.session_id)
            activities = result.get('activities', [])

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Total activities: {len(activities)}\n")

                # Show last 10 activities
                for activity in activities[-10:]:
                    originator = activity.get('originator', 'unknown')
                    create_time = activity.get('createTime', 'N/A')

                    if originator == 'agent':
                        msg = activity.get('agentMessaged', {}).get('agentMessage', '')
                        print(f"[JULES at {create_time}]")
                        print(msg[:200] + ('...' if len(msg) > 200 else ''))
                        print()
                    elif originator == 'user':
                        msg = activity.get('userMessaged', {}).get('userMessage', '')
                        print(f"[USER at {create_time}]")
                        print(msg[:200] + ('...' if len(msg) > 200 else ''))
                        print()

        elif args.command == "check":
            needs_attention, reason = client.check_session_needs_attention(args.session_id)

            if args.json:
                print(json.dumps({
                    "needs_attention": needs_attention,
                    "reason": reason,
                    "session_id": args.session_id
                }))
            else:
                icon = "⚠️" if needs_attention else "✅"
                print(f"{icon} {reason}")

                if needs_attention:
                    print(f"\nTo investigate, run:")
                    print(f"  {sys.argv[0]} activities {args.session_id}")

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
