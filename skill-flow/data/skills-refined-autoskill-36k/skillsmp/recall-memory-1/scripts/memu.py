#!/usr/bin/env python3
"""
memU CLI wrapper for Claude Code integration.

Provides memorize and retrieve operations with JSON output for the memU cloud API.
Uses only Python built-in libraries (no external dependencies).
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from typing import Dict, Any


API_BASE = "https://api.memu.so/api/v3/memory"


def get_api_key() -> str:
    """Get API key from environment, exit with clear error if missing."""
    api_key = os.getenv('MEMU_API_KEY')
    if not api_key:
        error_response = {
            "status": "error",
            "error": "MEMU_API_KEY environment variable not set. Get your API key from https://memu.so and set it with: export MEMU_API_KEY=your_key"
        }
        print(json.dumps(error_response), file=sys.stderr)
        sys.exit(1)
    return api_key


def get_git_user_info() -> tuple:
    """
    Get git user identity (email, name).

    Returns:
        Tuple of (email, name) or (None, None) if not configured
    """
    email_result = subprocess.run(
        ['git', 'config', 'user.email'],
        capture_output=True,
        text=True
    )

    name_result = subprocess.run(
        ['git', 'config', 'user.name'],
        capture_output=True,
        text=True
    )

    email = email_result.stdout.strip() if email_result.returncode == 0 else None
    name = name_result.stdout.strip() if name_result.returncode == 0 else None

    return (email, name)


def get_agent_info() -> tuple:
    """
    Get agent identity based on project.

    Returns:
        Tuple of (agent_id, agent_name)
        - agent_id: git remote name (e.g., "owner/repo") or directory name
        - agent_name: directory name + " Agent" (e.g., "Claude Plugins Agent")
    """
    # Try git remote for ID
    result = subprocess.run(
        ['git', 'remote', 'get-url', 'origin'],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )

    if result.returncode == 0 and result.stdout.strip():
        # Extract remote name from URL
        remote_url = result.stdout.strip()

        # Parse git URLs:
        # - git@github.com:owner/repo.git
        # - https://github.com/owner/repo.git
        # - https://github.com/owner/repo
        if ':' in remote_url and '@' in remote_url:
            # SSH format: git@github.com:owner/repo.git
            agent_id = remote_url.split(':')[1]
        elif remote_url.startswith('http'):
            # HTTPS format: https://github.com/owner/repo.git
            parts = remote_url.split('/')
            if len(parts) >= 2:
                agent_id = '/'.join(parts[-2:])
            else:
                agent_id = parts[-1]
        else:
            # Unknown format, use as-is
            agent_id = remote_url

        # Remove .git suffix if present
        if agent_id.endswith('.git'):
            agent_id = agent_id[:-4]
    else:
        # Fallback to current directory name
        agent_id = os.path.basename(os.getcwd())

    # Generate agent name from directory
    dir_name = os.path.basename(os.getcwd())
    # Convert kebab-case or snake_case to Title Case
    agent_name = ' '.join(word.capitalize() for word in dir_name.replace('-', ' ').replace('_', ' ').split())
    agent_name = f"{agent_name} Agent"

    return (agent_id, agent_name)


def http_request(url: str, method: str = "GET", headers: Dict[str, str] = None,
                 data: Dict[str, Any] = None, timeout: int = 30) -> Dict[str, Any]:
    """
    Make HTTP request using urllib (built-in library).

    Args:
        url: Full URL to request
        method: HTTP method (GET, POST)
        headers: HTTP headers dict
        data: JSON data to send (for POST)
        timeout: Request timeout in seconds

    Returns:
        Response data as dict

    Raises:
        urllib.error.HTTPError, urllib.error.URLError
    """
    headers = headers or {}

    req_data = None
    if data:
        req_data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'

    request = urllib.request.Request(
        url,
        data=req_data,
        headers=headers,
        method=method
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_data = response.read().decode('utf-8')
            return json.loads(response_data)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_data = json.loads(error_body)
            raise Exception(f"HTTP {e.code}: {error_data.get('error', error_body)}")
        except json.JSONDecodeError:
            raise Exception(f"HTTP {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {str(e.reason)}")


def parse_claude_transcript(transcript_data: str) -> list:
    """
    Parse Claude Code JSONL transcript format into simple message array.

    Args:
        transcript_data: JSONL string (one JSON object per line)

    Returns:
        List of {role, content} dicts suitable for memU API
    """
    messages = []

    for line in transcript_data.strip().split('\n'):
        if not line.strip():
            continue

        try:
            entry = json.loads(line)

            # Only process user and assistant messages
            if entry.get('type') not in ('user', 'assistant'):
                continue

            message = entry.get('message', {})
            role = message.get('role')
            content = message.get('content')

            if not role or not content:
                continue

            # Handle user messages (simple string content)
            if role == 'user':
                # Skip if content has tool_result blocks (internal tool outputs)
                if isinstance(content, list):
                    # User sent a message with tool results - skip this
                    continue
                if isinstance(content, str) and content.strip():
                    messages.append({"role": "user", "content": content})

            # Handle assistant messages (array of content blocks)
            elif role == 'assistant':
                if isinstance(content, list):
                    # Extract text from content blocks
                    # Skip: thinking blocks, tool_use blocks
                    # Include: text blocks only
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict):
                            block_type = block.get('type')
                            if block_type == 'text':
                                text_parts.append(block.get('text', ''))
                            # Skip tool_use, thinking, and other structured blocks

                    if text_parts:
                        messages.append({
                            "role": "assistant",
                            "content": '\n'.join(text_parts)
                        })
                elif isinstance(content, str):
                    messages.append({"role": "assistant", "content": content})

        except json.JSONDecodeError:
            continue

    return messages


def memorize(conversation_data: str) -> Dict[str, Any]:
    """
    Memorize conversation data via memU API.

    Args:
        conversation_data: JSON string of conversation messages or Claude JSONL transcript

    Returns:
        Dict with status and result data
    """
    api_key = get_api_key()
    user_email, user_name = get_git_user_info()
    agent_id, agent_name = get_agent_info()

    # Validate we have user identity
    if not user_email:
        return {
            "status": "error",
            "error": "Git user.email not configured. Set with: git config user.email 'your@email.com'"
        }

    try:
        # Try to parse as simple JSON array first
        try:
            messages = json.loads(conversation_data)
            if not isinstance(messages, list):
                raise ValueError("Not a list")
        except (json.JSONDecodeError, ValueError):
            # If that fails, try parsing as Claude JSONL transcript
            messages = parse_claude_transcript(conversation_data)

        # Prepare headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "conversation": messages,
            "user_id": user_email,
            "user_name": user_name or user_email,  # Use email as fallback
            "agent_id": agent_id,
            "agent_name": agent_name
        }

        # Start memorization task
        task_data = http_request(
            f"{API_BASE}/memorize",
            method="POST",
            headers=headers,
            data=payload,
            timeout=30
        )

        task_id = task_data.get("task_id")

        if not task_id:
            return {
                "status": "error",
                "error": "No task_id returned from memU API"
            }

        # Fire-and-forget: return immediately without polling
        return {
            "status": "ok",
            "message": "Memorization task started",
            "task_id": task_id
        }

    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error": f"Invalid JSON input: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"API request failed: {str(e)}"
        }


def retrieve(query: str, method: str = "rag") -> Dict[str, Any]:
    """
    Retrieve memories via memU API.

    Args:
        query: Query string
        method: "rag" (fast, default) or "llm" (deep semantic)

    Returns:
        Dict with status and retrieved data
    """
    api_key = get_api_key()
    user_email, user_name = get_git_user_info()
    agent_id, agent_name = get_agent_info()

    # Validate we have user identity
    if not user_email:
        return {
            "status": "error",
            "error": "Git user.email not configured. Set with: git config user.email 'your@email.com'"
        }

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": query,
            "user_id": user_email,
            "agent_id": agent_id,
            "method": method
        }

        result_data = http_request(
            f"{API_BASE}/retrieve",
            method="POST",
            headers=headers,
            data=payload,
            timeout=30
        )

        return {
            "status": "ok",
            "data": result_data
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"API request failed: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description='memU CLI for Claude Code',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', required=True, help='Command to execute')

    # memorize command
    mem_parser = subparsers.add_parser('memorize', help='Memorize conversation from stdin')

    # retrieve command
    ret_parser = subparsers.add_parser('retrieve', help='Retrieve memories')
    ret_parser.add_argument('--query', required=True, help='Query string')
    ret_parser.add_argument(
        '--method',
        default='rag',
        choices=['rag', 'llm'],
        help='Retrieval method: rag (fast, default) or llm (deep semantic)'
    )

    args = parser.parse_args()

    try:
        if args.command == 'memorize':
            # Read conversation from stdin
            conversation_data = sys.stdin.read()
            if not conversation_data.strip():
                result = {
                    "status": "error",
                    "error": "No conversation data provided on stdin"
                }
            else:
                result = memorize(conversation_data)

        elif args.command == 'retrieve':
            result = retrieve(args.query, args.method)

        else:
            result = {
                "status": "error",
                "error": f"Unknown command: {args.command}"
            }

        # Output JSON result
        print(json.dumps(result, indent=2))

        # Exit with error code if status is error
        if result.get("status") == "error":
            sys.exit(1)

    except Exception as e:
        error_result = {
            "status": "error",
            "error": f"Fatal error: {str(e)}"
        }
        print(json.dumps(error_result), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
