#!/usr/bin/env python3
"""Quick scan for common errors in agentic workflow logs

Usage: python3 quick_scan.py <log-directory>
Example: python3 quick_scan.py .github/aw/logs/run-21005890162
"""

import os
import subprocess
import sys
from pathlib import Path

def count_pattern_in_file(file_path, pattern):
    """Count occurrences of a pattern in a file"""
    if not file_path.exists():
        return 0
    try:
        result = subprocess.run(
            f'grep -c "{pattern}" "{file_path}"',
            shell=True,
            capture_output=True,
            text=True
        )
        # grep returns exit code 1 if no matches found
        if result.returncode == 0:
            return int(result.stdout.strip())
        return 0
    except:
        return 0

def get_matching_lines(file_path, pattern, limit=5):
    """Get matching lines from a file"""
    if not file_path.exists():
        return []
    try:
        result = subprocess.run(
            f'grep -E "{pattern}" "{file_path}" | head -{limit}',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            return result.stdout.strip().split('\n')
        return []
    except:
        return []

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 quick_scan.py <log-directory>")
        print("Example: python3 quick_scan.py .github/aw/logs/run-21005890162")
        sys.exit(1)

    log_dir = Path(sys.argv[1])
    agent_log = log_dir / "agent-stdio.log"
    gateway_log = log_dir / "mcp-logs" / "gateway.md"
    firewall_log = log_dir / "sandbox" / "firewall" / "logs" / "access.log"

    print("=== Quick Scan for Common Errors ===")
    print(f"Log directory: {log_dir}")
    print()

    # Check if agent log exists
    if not agent_log.exists():
        print(f"⚠️  Agent log not found at: {agent_log}")
        sys.exit(1)

    # MCP server failures
    print("🔍 Scanning for MCP server failures...")
    mcp_failures = count_pattern_in_file(agent_log, "mcp:.*failed")
    if mcp_failures > 0:
        print(f"   ❌ Found {mcp_failures} MCP server failure(s)")
        for line in get_matching_lines(agent_log, "mcp:.*failed", 5):
            print(f"      {line}")
    else:
        print("   ✅ No MCP server failures")
    print()

    # DNS resolution errors
    print("🔍 Scanning for DNS resolution errors...")
    dns_errors = count_pattern_in_file(agent_log, "dns error.*Name does not resolve")
    if dns_errors > 0:
        print(f"   ❌ Found {dns_errors} DNS resolution error(s)")
        print("   This usually indicates host.docker.internal is not resolvable")
    else:
        print("   ✅ No DNS resolution errors")
    print()

    # OAuth/keyring warnings
    print("🔍 Scanning for OAuth/keyring warnings...")
    oauth_warns = count_pattern_in_file(agent_log, "WARN codex_rmcp_client::oauth")
    if oauth_warns > 0:
        print(f"   ⚠️  Found {oauth_warns} OAuth warning(s)")
        print("   This may indicate missing org.freedesktop.secrets service")
    else:
        print("   ✅ No OAuth warnings")
    print()

    # Tool availability errors
    print("🔍 Scanning for tool availability errors...")
    tool_errors_result = subprocess.run(
        f'grep -ic "tool.*not available\\|tool.*failed" "{agent_log}"',
        shell=True,
        capture_output=True,
        text=True
    )
    tool_errors = int(tool_errors_result.stdout.strip()) if tool_errors_result.returncode == 0 else 0
    if tool_errors > 0:
        print(f"   ❌ Found {tool_errors} tool error(s)")
        for line in get_matching_lines(agent_log, "tool.*not available|tool.*failed", 3):
            print(f"      {line}")
    else:
        print("   ✅ No tool availability errors")
    print()

    # Check MCP Gateway logs if they exist
    if gateway_log.exists():
        print("🔍 Scanning MCP Gateway logs...")
        session_errors = count_pattern_in_file(gateway_log, "Session not found")
        if session_errors > 0:
            print(f"   ⚠️  Found {session_errors} session error(s)")
            for line in get_matching_lines(gateway_log, "Session not found", 3):
                print(f"      {line}")
        else:
            print("   ✅ No session errors")
        print()

    # Check firewall logs if they exist
    if firewall_log.exists():
        print("🔍 Scanning firewall logs...")
        blocked = count_pattern_in_file(firewall_log, "TCP_DENIED")
        if blocked > 0:
            print(f"   ⚠️  Found {blocked} blocked request(s)")
            for line in get_matching_lines(firewall_log, "TCP_DENIED", 3):
                print(f"      {line}")
        else:
            print("   ✅ No blocked requests")
        print()

    print("=== Scan Complete ===")

if __name__ == '__main__':
    main()
