#!/usr/bin/env python3
"""Query AI Gateway logs with conversation-focused interface."""

import argparse
from datetime import UTC, datetime, timedelta
import json
import os
import sys
import tempfile
from typing import Any

import httpx


def truncate_content(content: Any, max_length: int = 200) -> Any:
    """Truncate text content to max_length chars."""
    if isinstance(content, str):
        if len(content) > max_length:
            return content[:max_length] + f"... ({len(content)} chars total)"
        return content
    if isinstance(content, list):
        return [truncate_content(item, max_length) for item in content]  # pyright: ignore[reportUnknownVariableType]
    if isinstance(content, dict):
        return {k: truncate_content(v, max_length) for k, v in content.items()}  # pyright: ignore[reportUnknownVariableType]
    return content


def prune_request_body(
    data: dict[str, Any],
    last_messages: int | None,
    no_tools: bool,
    no_system: bool,
    truncate: int | None,
) -> dict[str, Any]:
    """Prune request body to make it more readable."""
    result = data.copy()

    if last_messages is not None and "messages" in result:
        messages = result["messages"]
        if len(messages) > last_messages:
            pruned_count = len(messages) - last_messages
            result["messages"] = messages[-last_messages:]
            result["_pruned_messages"] = f"{pruned_count} older messages removed"

    if no_tools and "tools" in result:
        tool_count = len(result["tools"])
        result["tools"] = f"[{tool_count} tools omitted]"

    if no_system and "system" in result:
        system = result["system"]
        if isinstance(system, str):
            result["system"] = f"[system prompt: {len(system)} chars omitted]"
        elif isinstance(system, list):
            result["system"] = f"[system prompt: {len(system)} blocks omitted]"  # pyright: ignore[reportUnknownArgumentType]

    if truncate is not None:
        result = truncate_content(result, truncate)

    return result


class AIGatewayClient:
    def __init__(self, account_id: str, api_token: str, gateway: str = "llms"):
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai-gateway/gateways/{gateway}"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def list_logs(
        self,
        minutes: int = 60,
        limit: int = 50,
        page: int = 1,
        filters: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """List logs with optional filters."""
        now = datetime.now(UTC)
        start_date = now - timedelta(minutes=minutes)

        all_filters = filters or []
        all_filters.extend(
            [
                {
                    "key": "created_at",
                    "operator": "gt",
                    "value": [start_date.isoformat()],
                },
                {"key": "created_at", "operator": "lt", "value": [now.isoformat()]},
            ]
        )

        params: dict[str, Any] = {
            "per_page": min(limit, 50),
            "page": page,
            "order_by": "created_at",
            "order_by_direction": "desc",
            "filters": json.dumps(all_filters),
        }

        resp = httpx.get(
            f"{self.base_url}/logs",
            headers=self.headers,
            params=params,
            timeout=60.0,
        )
        return resp.json()

    def get_request_body(self, log_id: str) -> dict[str, Any] | str | None:
        """Get request body for a specific log."""
        resp = httpx.get(
            f"{self.base_url}/logs/{log_id}/request",
            headers=self.headers,
            timeout=60.0,
        )
        if resp.status_code != 200:
            return None
        try:
            return resp.json()
        except Exception:
            return resp.text


def list_conversations(client: AIGatewayClient, minutes: int, limit: int) -> int:
    """List conversations grouped by conversation-id metadata."""
    conversations: dict[str, dict[str, Any]] = {}
    page = 1
    fetched = 0

    while fetched < limit * 10:
        data = client.list_logs(minutes=minutes, limit=50, page=page)
        if not data.get("success"):
            print(f"API Error: {json.dumps(data.get('errors', []))}", file=sys.stderr)
            return 1

        logs = data.get("result", [])
        if not logs:
            break

        for log in logs:
            metadata: dict[str, Any] = log.get("metadata") or {}
            conv_id: str = metadata.get("conversation-id", "unknown")

            if conv_id not in conversations:
                conversations[conv_id] = {
                    "conversation_id": conv_id,
                    "latest_log_id": log.get("id"),
                    "latest_at": log.get("created_at"),
                    "provider": log.get("provider"),
                    "model": log.get("model"),
                    "request_count": 0,
                    "total_tokens_in": 0,
                    "total_tokens_out": 0,
                    "total_cost": 0.0,
                }

            conversations[conv_id]["request_count"] += 1
            conversations[conv_id]["total_tokens_in"] += log.get("tokens_in") or 0
            conversations[conv_id]["total_tokens_out"] += log.get("tokens_out") or 0
            conversations[conv_id]["total_cost"] += log.get("cost") or 0.0

        fetched += len(logs)
        page += 1

        if len(conversations) >= limit:
            break

    sorted_convs = sorted(
        conversations.values(),
        key=lambda x: x["latest_at"] or "",
        reverse=True,
    )[:limit]

    print(
        json.dumps(
            {"conversations": sorted_convs, "count": len(sorted_convs)}, indent=2
        )
    )
    return 0


def get_conversation_messages(
    client: AIGatewayClient,
    conversation_id: str,
    minutes: int,
    last_messages: int,
    include_tools: bool,
    include_system: bool,
    truncate: int | None,
) -> int:
    """Get messages from a conversation's latest log entry."""
    filters = [
        {"key": "metadata.key", "operator": "eq", "value": ["conversation-id"]},
        {"key": "metadata.value", "operator": "eq", "value": [conversation_id]},
    ]

    data = client.list_logs(minutes=minutes, limit=1, filters=filters)
    if not data.get("success"):
        print(f"API Error: {json.dumps(data.get('errors', []))}", file=sys.stderr)
        return 1

    logs = data.get("result", [])
    if not logs:
        print(f"No logs found for conversation {conversation_id}", file=sys.stderr)
        return 1

    log = logs[0]
    request_body = client.get_request_body(log["id"])
    if request_body is None:
        print(f"Failed to get request body for log {log['id']}", file=sys.stderr)
        return 1

    if isinstance(request_body, str):
        print(request_body)
        return 0

    pruned = prune_request_body(
        request_body,
        last_messages if last_messages != 0 else None,
        not include_tools,
        not include_system,
        truncate,
    )

    output = {
        "log_id": log["id"],
        "created_at": log["created_at"],
        "model": log["model"],
        "tokens_in": log.get("tokens_in"),
        "tokens_out": log.get("tokens_out"),
        "request": pruned,
    }
    print(json.dumps(output, indent=2))
    return 0


def dump_raw_logs(
    client: AIGatewayClient, minutes: int, limit: int, include_bodies: bool
) -> int:
    """Dump raw logs to a temp file."""
    all_logs: list[dict[str, Any]] = []
    page = 1

    while len(all_logs) < limit:
        data = client.list_logs(
            minutes=minutes, limit=min(50, limit - len(all_logs)), page=page
        )
        if not data.get("success"):
            print(f"API Error: {json.dumps(data.get('errors', []))}", file=sys.stderr)
            return 1

        logs = data.get("result", [])
        if not logs:
            break

        for log in logs:
            entry: dict[str, Any] = dict(log)
            if include_bodies:
                request_body = client.get_request_body(log["id"])
                if request_body:
                    entry["request_body"] = request_body
            all_logs.append(entry)

        page += 1

    with tempfile.NamedTemporaryFile(
        mode="w",
        prefix="aig_logs_",
        suffix=".json",
        delete=False,
    ) as f:
        json.dump(all_logs, f, indent=2)
        print(f.name)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query AI Gateway logs with conversation-focused interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  --conversations       List conversations (grouped by conversation-id)
  --conversation ID     Get messages from a specific conversation
  --raw                 Dump raw logs to /tmp file (returns filename)

Examples:
  # List recent conversations
  uv run scripts/cf_ai_gateway_logs.py --conversations

  # Get last 10 messages from a conversation
  uv run scripts/cf_ai_gateway_logs.py --conversation T-xxx --last-messages 10

  # Dump 100 raw logs to file
  uv run scripts/cf_ai_gateway_logs.py --raw --limit 100

  # Include request bodies in raw dump
  uv run scripts/cf_ai_gateway_logs.py --raw --limit 10 --include-bodies
""",
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--conversations",
        action="store_true",
        help="List conversations grouped by conversation-id metadata",
    )
    mode_group.add_argument(
        "--conversation",
        metavar="ID",
        help="Get messages from a specific conversation's latest log",
    )
    mode_group.add_argument(
        "--raw",
        action="store_true",
        help="Dump raw logs to /tmp file (prints filename)",
    )

    parser.add_argument(
        "--gateway",
        default="llms",
        help="AI Gateway ID (default: llms)",
    )
    parser.add_argument(
        "--minutes",
        type=int,
        default=60,
        help="Time range in minutes (default: 60)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Max results (default: 20)",
    )

    parser.add_argument(
        "--last-messages",
        type=int,
        metavar="N",
        default=4,
        help="Only show the last N messages (default: 4, use 0 for all)",
    )
    parser.add_argument(
        "--include-tools",
        action="store_true",
        help="Include the full tools array (omitted by default)",
    )
    parser.add_argument(
        "--include-system",
        action="store_true",
        help="Include the full system prompt (omitted by default)",
    )
    parser.add_argument(
        "--truncate",
        type=int,
        metavar="CHARS",
        help="Truncate text content to N characters",
    )
    parser.add_argument(
        "--include-bodies",
        action="store_true",
        help="Include request bodies in raw dump (slow)",
    )

    args = parser.parse_args()

    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN")

    if not account_id:
        print("Error: CLOUDFLARE_ACCOUNT_ID required", file=sys.stderr)
        return 1
    if not api_token:
        print("Error: CLOUDFLARE_API_TOKEN required", file=sys.stderr)
        return 1

    client = AIGatewayClient(account_id, api_token, args.gateway)

    if args.conversations:
        return list_conversations(client, args.minutes, args.limit)

    if args.conversation:
        return get_conversation_messages(
            client,
            args.conversation,
            args.minutes,
            args.last_messages,
            args.include_tools,
            args.include_system,
            args.truncate,
        )

    if args.raw:
        return dump_raw_logs(client, args.minutes, args.limit, args.include_bodies)

    return 0


if __name__ == "__main__":
    sys.exit(main())
