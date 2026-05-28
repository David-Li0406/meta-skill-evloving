#!/usr/bin/env python3
"""
Browser CLI - sends commands to browser daemon via Unix socket.
"""

import argparse
import json
import os
import socket
import struct
import sys
from pathlib import Path


def send_command(command: str, args: dict) -> dict:
    """Send command to daemon and return response."""
    runtime_dir = Path(os.getenv("XDG_RUNTIME_DIR", "/tmp")) / "claude-browser"
    socket_path = runtime_dir / "browser.sock"

    if not socket_path.exists():
        return {"error": "Daemon not running (socket not found)"}

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(str(socket_path))

        # Send length-prefixed JSON message
        request = {"command": command, "args": args}
        payload = json.dumps(request).encode('utf-8')
        sock.sendall(struct.pack('>I', len(payload)) + payload)

        # Receive length-prefixed JSON response
        length_data = sock.recv(4)
        if not length_data:
            return {"error": "No response from daemon"}

        message_length = struct.unpack('>I', length_data)[0]
        response_data = b''
        while len(response_data) < message_length:
            chunk = sock.recv(message_length - len(response_data))
            if not chunk:
                break
            response_data += chunk

        return json.loads(response_data.decode('utf-8'))

    except Exception as e:
        return {"error": str(e)}
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="Browser CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Daemon commands
    subparsers.add_parser("status", help="Get daemon status with all browsing contexts")
    subparsers.add_parser("quit", help="Stop daemon")

    # Browsing context lifecycle commands
    create_ctx_parser = subparsers.add_parser("create-browsing-context",
                                              help="Create new browsing context (tab)")
    create_ctx_parser.add_argument("name", help="Name for the browsing context")
    create_ctx_parser.add_argument("--url", help="Optional URL to navigate to")

    close_ctx_parser = subparsers.add_parser("close-browsing-context",
                                            help="Close browsing context")
    close_ctx_parser.add_argument("browsing_context", help="Browsing context name")

    history_parser = subparsers.add_parser("browsing-context-history",
                                          help="Get action history for browsing context")
    history_parser.add_argument("browsing_context", help="Browsing context name")
    history_parser.add_argument("--limit", type=int, default=10, help="Max history entries")

    # Action commands (require browsing context and intention)
    navigate_parser = subparsers.add_parser("navigate", help="Navigate to URL")
    navigate_parser.add_argument("--browsing-context", required=True, help="Browsing context name")
    navigate_parser.add_argument("--intention", required=True, help="Why performing this action")
    navigate_parser.add_argument("url", help="URL to navigate to")

    extract_parser = subparsers.add_parser("extract", help="Extract text/HTML from element")
    extract_parser.add_argument("--browsing-context", required=True, help="Browsing context name")
    extract_parser.add_argument("--intention", required=True, help="Why performing this action")
    extract_parser.add_argument("--selector", help="CSS selector (optional, extracts whole page if not provided)")

    eval_parser = subparsers.add_parser("eval", help="Execute JavaScript")
    eval_parser.add_argument("--browsing-context", required=True, help="Browsing context name")
    eval_parser.add_argument("--intention", required=True, help="Why performing this action")
    eval_parser.add_argument("javascript", help="JavaScript code to execute")

    snapshot_parser = subparsers.add_parser("snapshot", help="Get page structure")
    snapshot_parser.add_argument("--browsing-context", required=True, help="Browsing context name")
    snapshot_parser.add_argument("--intention", required=True, help="Why performing this action")
    snapshot_parser.add_argument("--mode", choices=["tree", "dom"], default="tree",
                                help="Snapshot mode (tree=accessibility, dom=simplified DOM)")
    snapshot_parser.add_argument("--token-limit", type=int, default=None,
                                help="Max tokens (default: 70000)")
    snapshot_parser.add_argument("--focus-selector", type=str, default=None,
                                help="CSS selector to scope tree to element subtree")
    snapshot_parser.add_argument("--diff", action="store_true",
                                help="Return only new elements since last snapshot")

    click_parser = subparsers.add_parser("click", help="Click element")
    click_parser.add_argument("--browsing-context", required=True, help="Browsing context name")
    click_parser.add_argument("--intention", required=True, help="Why performing this action")
    click_parser.add_argument("selector", help="CSS selector")

    type_parser = subparsers.add_parser("type", help="Type text into element")
    type_parser.add_argument("--browsing-context", required=True, help="Browsing context name")
    type_parser.add_argument("--intention", required=True, help="Why performing this action")
    type_parser.add_argument("selector", help="CSS selector")
    type_parser.add_argument("text", help="Text to type")

    wait_parser = subparsers.add_parser("wait", help="Wait for element or text")
    wait_parser.add_argument("--browsing-context", required=True, help="Browsing context name")
    wait_parser.add_argument("--intention", required=True, help="Why performing this action")
    wait_parser.add_argument("selector", help="CSS selector or text to wait for")
    wait_parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds")

    scroll_parser = subparsers.add_parser("scroll", help="Scroll the page")
    scroll_parser.add_argument("--browsing-context", required=True, help="Browsing context name")
    scroll_parser.add_argument("--intention", required=True, help="Why performing this action")
    scroll_parser.add_argument("--direction", choices=["up", "down"], default="down", help="Scroll direction")
    scroll_parser.add_argument("--amount", choices=["page", "half", "full"], default="page", help="Scroll amount")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Build command args
    cmd_args = {}

    # Browsing context lifecycle
    if args.command == "create-browsing-context":
        cmd_args["name"] = args.name
        if args.url:
            cmd_args["url"] = args.url
        response = send_command("create_browsing_context", cmd_args)

    elif args.command == "close-browsing-context":
        cmd_args["browsing_context"] = args.browsing_context
        response = send_command("close_browsing_context", cmd_args)

    elif args.command == "browsing-context-history":
        cmd_args["browsing_context"] = args.browsing_context
        cmd_args["limit"] = args.limit
        response = send_command("get_browsing_context_history", cmd_args)

    # Action commands
    elif args.command == "navigate":
        cmd_args["browsing_context"] = getattr(args, "browsing_context")
        cmd_args["intention"] = args.intention
        cmd_args["url"] = args.url
        response = send_command("navigate", cmd_args)

    elif args.command == "extract":
        cmd_args["browsing_context"] = getattr(args, "browsing_context")
        cmd_args["intention"] = args.intention
        cmd_args["selector"] = getattr(args, "selector", None)
        response = send_command("extract", cmd_args)

    elif args.command == "eval":
        cmd_args["browsing_context"] = getattr(args, "browsing_context")
        cmd_args["intention"] = args.intention
        cmd_args["javascript"] = args.javascript
        response = send_command("eval", cmd_args)

    elif args.command == "snapshot":
        cmd_args["browsing_context"] = getattr(args, "browsing_context")
        cmd_args["intention"] = args.intention
        cmd_args["mode"] = args.mode
        cmd_args["token_limit"] = getattr(args, "token_limit", None)
        cmd_args["focus_selector"] = getattr(args, "focus_selector", None)
        cmd_args["diff"] = getattr(args, "diff", False)
        response = send_command("snapshot", cmd_args)

    elif args.command == "click":
        cmd_args["browsing_context"] = getattr(args, "browsing_context")
        cmd_args["intention"] = args.intention
        cmd_args["selector"] = args.selector
        response = send_command("click", cmd_args)

    elif args.command == "type":
        cmd_args["browsing_context"] = getattr(args, "browsing_context")
        cmd_args["intention"] = args.intention
        cmd_args["selector"] = args.selector
        cmd_args["text"] = args.text
        response = send_command("type", cmd_args)

    elif args.command == "wait":
        cmd_args["browsing_context"] = getattr(args, "browsing_context")
        cmd_args["intention"] = args.intention
        cmd_args["selector"] = args.selector
        cmd_args["timeout"] = args.timeout
        response = send_command("wait", cmd_args)

    elif args.command == "scroll":
        cmd_args["browsing_context"] = getattr(args, "browsing_context")
        cmd_args["intention"] = args.intention
        cmd_args["direction"] = args.direction
        cmd_args["amount"] = args.amount
        response = send_command("scroll", cmd_args)

    # Daemon commands
    elif args.command in ["status", "quit"]:
        response = send_command(args.command, {})

    else:
        print(json.dumps({"error": f"Unknown command: {args.command}"}), file=sys.stderr)
        sys.exit(1)

    # Output JSON
    print(json.dumps(response, indent=2))

    # Exit code
    sys.exit(0 if response.get("success") or response.get("status") else 1)


if __name__ == "__main__":
    main()
