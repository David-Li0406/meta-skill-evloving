#!/usr/bin/env python3
"""Stop MCP Gateway"""

import os
import subprocess

def run_command(cmd, check=False):
    """Run a shell command"""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)

def main():
    container_name = os.environ.get('CONTAINER_NAME', 'mcpg-gateway')

    print("Stopping MCP Gateway...")

    # Check if container exists
    result = run_command(f"docker ps -a --filter name={container_name} --format '{{{{.ID}}}}'")
    if result.stdout.strip():
        run_command(f"docker stop {container_name}")
        run_command(f"docker rm {container_name}")
        print("✓ Gateway stopped and removed")
    else:
        print(f"⚠ Container '{container_name}' not found")

    # Clean up any orphaned MCP server containers
    print("Cleaning up MCP server containers...")
    result = run_command("docker ps -a --format '{{.Names}}' | grep -E 'github-mcp|mcp-server'")
    mcp_containers = result.stdout.strip()

    if mcp_containers:
        for container in mcp_containers.split('\n'):
            if container:
                run_command(f"docker rm -f {container}")
                print(f"  Removed: {container}")
    else:
        print("  No MCP server containers found")

    print("✓ Cleanup complete")

if __name__ == '__main__':
    main()
