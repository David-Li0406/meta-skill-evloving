#!/usr/bin/env python3
"""Setup Copilot CLI to use MCP Gateway"""

import json
import os
from pathlib import Path

def main():
    gateway_port = os.environ.get('GATEWAY_PORT', '80')

    # Get API key from file or use default
    api_key_file = Path('/tmp/mcpg-api-key.txt')
    if api_key_file.exists():
        api_key = api_key_file.read_text().strip()
    else:
        api_key = os.environ.get('API_KEY', 'test-api-key')

    print("Creating Copilot MCP configuration...")

    # Create MCP config for Copilot CLI
    config = {
        "mcpServers": {
            "github-gateway": {
                "type": "http",
                "url": f"http://host.docker.internal:{gateway_port}/mcp/github",
                "headers": {
                    "Authorization": api_key
                },
                "tools": ["*"]
            }
        }
    }

    config_path = Path('/tmp/mcp-gateway-config.json')
    config_path.write_text(json.dumps(config, indent=2))

    print(f"✓ Created {config_path}")
    print()
    print("To use with Copilot CLI (outside AWF):")
    print("  npx @github/copilot \\")
    print("    --disable-builtin-mcps \\")
    print("    --additional-mcp-config @/tmp/mcp-gateway-config.json \\")
    print("    --allow-all-tools \\")
    print("    --prompt 'List 3 issues from githubnext/gh-aw'")
    print()
    print("To use with AWF:")
    print("  sudo -E awf \\")
    print("    --enable-host-access \\")
    print("    --mount /tmp:/tmp:rw \\")
    print("    --allow-domains 'host.docker.internal,api.github.com,*.githubusercontent.com' \\")
    print("    -- npx -y @github/copilot \\")
    print("      --disable-builtin-mcps \\")
    print("      --additional-mcp-config @/tmp/mcp-gateway-config.json \\")
    print("      --allow-all-tools \\")
    print("      --prompt 'Your prompt here'")

if __name__ == '__main__':
    main()
