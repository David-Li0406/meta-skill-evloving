#!/usr/bin/env python3
"""Start MCP Gateway with GitHub MCP Server
Version: Compatible with gh-aw-mcpg v0.0.59+
"""

import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd, capture_output=True, check=True):
    """Run a shell command and return the result"""
    if capture_output:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    else:
        subprocess.run(cmd, shell=True, check=check)
        return None

def main():
    # Configuration
    gateway_version = os.environ.get('GATEWAY_VERSION', 'v0.0.59')
    gateway_port = os.environ.get('GATEWAY_PORT', '80')
    gateway_domain = os.environ.get('GATEWAY_DOMAIN', 'localhost')
    gateway_api_key = os.environ.get('GATEWAY_API_KEY', secrets.token_hex(16))
    container_name = os.environ.get('CONTAINER_NAME', 'mcpg-gateway')

    print(f"Starting MCP Gateway {gateway_version}...")

    # Get GitHub token
    github_token = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')
    if not github_token:
        print("Getting GitHub token from gh CLI...")
        try:
            github_token = run_command('gh auth token')
        except subprocess.CalledProcessError:
            print("Error: Could not get GitHub token from gh CLI")
            sys.exit(1)

    # Create MCP Gateway configuration
    print("Creating gateway configuration...")
    config = {
        "mcpServers": {
            "github": {
                "type": "stdio",
                "container": "ghcr.io/github/github-mcp-server:latest",
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": github_token
                }
            }
        },
        "gateway": {
            "port": 8000,
            "domain": gateway_domain,
            "apiKey": gateway_api_key
        }
    }

    config_path = Path('/tmp/mcpg-config.json')
    config_path.write_text(json.dumps(config, indent=2))

    # Clean up existing container
    existing_container = run_command(
        f"docker ps -a --filter name={container_name} --format '{{{{.ID}}}}'",
        check=False
    )
    if existing_container:
        print("Removing existing container...")
        run_command(f"docker stop {container_name}", check=False, capture_output=True)
        run_command(f"docker rm {container_name}", check=False, capture_output=True)

    # Start the gateway
    print("Launching container...")
    docker_cmd = f"""cat {config_path} | docker run -i \
    --name {container_name} \
    -p {gateway_port}:8000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e "GITHUB_PERSONAL_ACCESS_TOKEN={github_token}" \
    -e "MCP_GATEWAY_PORT=8000" \
    -e "MCP_GATEWAY_DOMAIN={gateway_domain}" \
    -e "MCP_GATEWAY_API_KEY={gateway_api_key}" \
    ghcr.io/githubnext/gh-aw-mcpg:{gateway_version} > /tmp/mcpg-gateway.log 2>&1 &"""

    run_command(docker_cmd, capture_output=False, check=False)

    # Wait for gateway to be ready
    print("Waiting for gateway to start...")
    for i in range(1, 31):
        try:
            run_command(f"curl -s http://127.0.0.1:{gateway_port}/health", check=False)
            if subprocess.run(
                f"curl -s http://127.0.0.1:{gateway_port}/health",
                shell=True,
                capture_output=True
            ).returncode == 0:
                print("✓ Gateway is running!")
                break
        except:
            pass

        time.sleep(1)
        if i == 30:
            print("✗ Gateway failed to start. Check logs:")
            print(f"  docker logs {container_name}")
            sys.exit(1)

    # Display information
    print()
    print("=========================================")
    print("MCP Gateway Information")
    print("=========================================")
    print(f"Version:     {gateway_version}")
    print(f"URL:         http://127.0.0.1:{gateway_port}")
    print(f"Health:      http://127.0.0.1:{gateway_port}/health")
    print(f"GitHub MCP:  http://127.0.0.1:{gateway_port}/mcp/github")
    print(f"API Key:     {gateway_api_key}")
    print(f"Container:   {container_name}")
    print("Logs:        /tmp/mcpg-gateway.log")
    print()
    print("To stop:")
    print(f"  docker stop {container_name} && docker rm {container_name}")
    print()
    print("To check status:")
    print(f"  curl http://127.0.0.1:{gateway_port}/health | jq .")
    print("=========================================")

    # Save API key for later use
    api_key_file = Path('/tmp/mcpg-api-key.txt')
    api_key_file.write_text(gateway_api_key)

if __name__ == '__main__':
    main()
