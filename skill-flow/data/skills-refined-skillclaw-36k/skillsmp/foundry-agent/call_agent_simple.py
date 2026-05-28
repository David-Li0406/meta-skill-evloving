#!/usr/bin/env python3
"""Call a Foundry agent. That's it."""
import sys
import os
from pathlib import Path

# Auto-use venv if it exists
script_dir = Path(__file__).parent
venv_python = script_dir / ".venv" / "bin" / "python"
if venv_python.exists() and sys.executable != str(venv_python):
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

# Load .env file if it exists
env_file = script_dir / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"\''))

PROJECT_ENDPOINT = os.environ.get("PROJECT_ENDPOINT")
AGENT_NAME = os.environ.get("AGENT_NAME", "ratemytask")

if not PROJECT_ENDPOINT:
    print("Set PROJECT_ENDPOINT environment variable", file=sys.stderr)
    sys.exit(1)

try:
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    
    client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
    agent = client.agents.get(agent_name=AGENT_NAME)
    openai_client = client.get_openai_client()
    
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello"
    
    response = openai_client.responses.create(
        input=message,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    
    print(response.output_text)
    
except ImportError:
    print("Run: pip install azure-ai-projects azure-identity", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
