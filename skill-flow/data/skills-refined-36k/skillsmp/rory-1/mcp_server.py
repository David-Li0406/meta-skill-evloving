import os
import sys
import logging
from typing import Any, Dict, Optional, Tuple

import httpx
from fastmcp import FastMCP

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from remote_cmo import RemoteCMO

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

ROBYNN_CLI_BASE_URL = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")

mcp = FastMCP("Robynn AI - Rory")


def _get_headers(api_key: Optional[str]) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _api_get(path: str, api_key: Optional[str]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if not api_key:
        return None, "Not connected. Set ROBYNN_API_KEY."

    url = f"{ROBYNN_CLI_BASE_URL}{path}"
    try:
        with httpx.Client(headers=_get_headers(api_key)) as client:
            response = client.get(url, timeout=30.0)
            response.raise_for_status()
            data = response.json().get("data")
            return data, None
    except Exception as exc:
        return None, f"Failed to fetch {path}: {exc}"


def _run_cmo_query(message: str) -> str:
    cmo = RemoteCMO()
    for event in cmo.stream_query(message):
        event_type = event.get("type")
        if event_type == "complete":
            data = event.get("data", {})
            return data.get("response", "Task completed.")
        if event_type == "error":
            return f"Error: {event.get('message')}"
    return "No response received."


@mcp.tool(annotations={"openWorldHint": True})
def rory_query(message: str) -> str:
    """Send any marketing request to Rory."""
    return _run_cmo_query(message)


@mcp.tool(annotations={"openWorldHint": True})
def rory_research_company(company: str) -> str:
    """Research a company."""
    return _run_cmo_query(f"research {company}")


@mcp.tool(annotations={"openWorldHint": True})
def rory_research_competitors(company: str) -> str:
    """Analyze competitors for a company."""
    return _run_cmo_query(f"competitors {company}")


@mcp.tool(annotations={"openWorldHint": True})
def rory_write_content(content_type: str, topic: str) -> str:
    """Create marketing content (linkedin, tweet, blog, email)."""
    return _run_cmo_query(f"write {content_type} {topic}")


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
def rory_status() -> str:
    """Check API connection and Brand Hub status."""
    api_key = os.environ.get("ROBYNN_API_KEY")
    if not api_key:
        return (
            "Status: Not Connected (Anonymous Mode)\n"
            "Run: rory config <your_api_key>\n"
            "Get a key at https://robynn.ai/settings/api-keys"
        )

    context, error = _api_get("/context", api_key)
    if error:
        return f"Status: Connected, but unable to fetch context. {error}"
    if not context:
        return "Status: Connected, but no brand context found."

    organization = context.get("organizationId", "Loaded")
    company = context.get("companyName", "Not Set")
    website = context.get("companyWebsite", "Not Set")
    voice = "Configured" if context.get("voiceAndTone") else "Not configured"
    return (
        "Status: Connected\n"
        f"Organization: {organization}\n"
        f"Company: {company}\n"
        f"Website: {website}\n"
        f"Brand Voice: {voice}"
    )


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
def rory_usage() -> str:
    """Check remaining task quota."""
    api_key = os.environ.get("ROBYNN_API_KEY")
    if not api_key:
        return (
            "Tier: Anonymous\n"
            "Limit: 5 tasks / day (Per IP)\n"
            "Sign up at https://robynn.ai for higher limits."
        )

    usage, error = _api_get("/usage", api_key)
    if error:
        return f"Usage: Unable to fetch usage details. {error}"
    if not usage:
        return "Usage: No usage data available."

    tier = usage.get("tier", "Unknown")
    remaining = usage.get("remaining", 0)
    total = usage.get("total", 0)
    reset_date = usage.get("resetDate")
    reset_line = f"\nResets on: {reset_date}" if reset_date else ""
    return (
        f"Tier: {tier}\n"
        f"Remaining: {remaining} of {total} tasks"
        f"{reset_line}"
    )


if __name__ == "__main__":
    mcp.run()
