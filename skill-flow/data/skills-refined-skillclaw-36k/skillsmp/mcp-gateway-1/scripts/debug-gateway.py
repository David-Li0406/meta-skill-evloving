#!/usr/bin/env python3
"""Debug and Troubleshoot MCP Gateway"""

import os
import subprocess
import sys

def run_command(cmd, check=True, capture_output=True):
    """Run a shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True, check=check)
    if capture_output:
        return result.stdout.strip()
    return None

def main():
    container_name = os.environ.get('CONTAINER_NAME', 'mcpg-gateway')

    print("========================================")
    print("MCP Gateway Debug Information")
    print("========================================")
    print()

    # Check if container exists
    container_exists = run_command(
        f"docker ps -a --filter name={container_name} --format '{{{{.ID}}}}'",
        check=False
    )
    if not container_exists:
        print(f"✗ Container '{container_name}' not found")
        print()
        print("Start the gateway first:")
        print("  ./start-gateway.py")
        sys.exit(1)

    # Container status
    print("=== Container Status ===")
    status = run_command(
        f'docker ps -a --filter name={container_name} --format "ID: {{{{.ID}}}}\\nImage: {{{{.Image}}}}\\nStatus: {{{{.Status}}}}\\nPorts: {{{{.Ports}}}}"'
    )
    print(status)
    print()

    # Health check
    print("=== Health Check ===")
    health_result = subprocess.run(
        "curl -s http://127.0.0.1:80/health",
        shell=True,
        capture_output=True
    )
    if health_result.returncode == 0:
        health_json = subprocess.run(
            "curl -s http://127.0.0.1:80/health | jq .",
            shell=True,
            capture_output=True,
            text=True
        )
        print(health_json.stdout)
        print("✓ Gateway is healthy")
    else:
        print("✗ Gateway health check failed")
    print()

    # Gateway logs
    print("=== Gateway Logs (last 50 lines) ===")
    logs = run_command(f"docker logs {container_name} 2>&1 | tail -50", check=False)
    print(logs)
    print()

    # Check MCP server containers
    print("=== MCP Server Containers ===")
    mcp_containers = run_command(
        'docker ps --format "{{.Names}}: {{.Image}} ({{.Status}})" | grep -E "github-mcp|mcp-server"',
        check=False
    )
    if mcp_containers:
        print(mcp_containers)
    else:
        print("No MCP server containers found")
    print()

    # Internal log files
    print("=== Internal Log Files ===")
    log_files = run_command(
        f"docker exec {container_name} ls -lh /tmp/gh-aw/mcp-logs/ 2>/dev/null",
        check=False
    )
    if log_files:
        print(log_files)
    else:
        print("Cannot access log directory")
    print()

    # Check for common issues
    print("=== Common Issues Check ===")

    # Check 1: Environment variables
    token_check = subprocess.run(
        f"docker exec {container_name} printenv GITHUB_PERSONAL_ACCESS_TOKEN",
        shell=True,
        capture_output=True
    ).returncode
    print(f"GITHUB_PERSONAL_ACCESS_TOKEN set: {'✓ Yes' if token_check == 0 else '✗ No (this may cause authentication issues)'}")

    # Check 2: Docker socket
    socket_check = subprocess.run(
        f"docker exec {container_name} test -S /var/run/docker.sock",
        shell=True,
        capture_output=True
    ).returncode
    print(f"Docker socket accessible: {'✓ Yes' if socket_check == 0 else '✗ No (cannot spawn MCP server containers)'}")

    # Check 3: Port binding
    port_check = subprocess.run(
        "netstat -tln 2>/dev/null | grep -q ':80 ' || ss -tln 2>/dev/null | grep -q ':80 '",
        shell=True
    ).returncode
    print(f"Port 80 bound: {'✓ Yes' if port_check == 0 else '⚠ Port 80 not listening'}")

    print()
    print("========================================")
    print("For detailed logs:")
    print(f"  docker logs {container_name}")
    print(f"  docker logs {container_name} -f  # follow mode")
    print()
    print("To restart gateway:")
    print(f"  docker restart {container_name}")
    print("========================================")

if __name__ == '__main__':
    main()
