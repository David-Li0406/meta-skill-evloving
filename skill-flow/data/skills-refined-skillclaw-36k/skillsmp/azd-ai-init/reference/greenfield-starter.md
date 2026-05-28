# Greenfield Starter Template

This is a complete, copy-paste ready starter template for users with no existing code.

## Quick Start Commands

```bash
# Create project structure
mkdir -p my-agent/src/MyAgent my-agent/infra

# Navigate to project
cd my-agent

# After creating all files below, deploy with:
azd auth login
azd init

# Region is set to northcentralus by default (required for hosted agents)
azd up
```

## Complete File Contents

### azure.yaml

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json

requiredVersions:
    extensions:
        azure.ai.agents: '>=0.1.0-preview'

name: my-agent

services:
    MyAgent:
        project: src/MyAgent
        host: azure.ai.agent
        language: docker
        docker:
            remoteBuild: true
        config:
            container:
                resources:
                    cpu: "1"
                    memory: 2Gi
                scale:
                    maxReplicas: 3
                    minReplicas: 1
            deployments:
                - model:
                    format: OpenAI
                    name: gpt-4o-mini
                    version: "2024-07-18"
                  name: gpt-4o-mini
                  sku:
                    capacity: 10
                    name: GlobalStandard

infra:
    provider: bicep
    path: ./infra
```

### src/MyAgent/agent.yaml

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/microsoft/AgentSchema/refs/heads/main/schemas/v1.0/ContainerAgent.yaml

kind: hosted
name: MyAgent
description: "A helpful assistant that can answer questions and perform tasks."

metadata:
    authors:
        - developer
    example:
        - content: "Hello, what can you help me with?"
          role: user
    tags:
        - starter
        - assistant

protocols:
    - protocol: responses
      version: v1

environment_variables:
  - name: FOUNDRY_PROJECT_ENDPOINT
    value: ${AZURE_AI_PROJECT_ENDPOINT}
  - name: FOUNDRY_MODEL_DEPLOYMENT_NAME
    value: gpt-4o-mini
  - name: APPLICATIONINSIGHTS_CONNECTION_STRING
    value: ${APPLICATIONINSIGHTS_CONNECTION_STRING}
```

### src/MyAgent/main.py

```python
import asyncio
import os
import logging
from typing import Annotated

from azure.identity.aio import DefaultAzureCredential
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv

load_dotenv(override=True)

logger = logging.getLogger(__name__)

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor(enable_live_metrics=True, logger_name="__main__")

ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
MODEL_DEPLOYMENT_NAME = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME", "")


# ===========================================
# Define your tools here
# ===========================================

def greet(
    name: Annotated[str, "The name of the person to greet"]
) -> str:
    """Greet someone by name.

    Args:
        name: The person's name
    """
    return f"Hello, {name}! Nice to meet you."


def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate(
    expression: Annotated[str, "A mathematical expression to evaluate, e.g. '2 + 2'"]
) -> str:
    """Safely evaluate a mathematical expression.

    Args:
        expression: Math expression like '2 + 2' or '10 * 5'
    """
    allowed_chars = set("0123456789+-*/(). ")
    if not all(c in allowed_chars for c in expression):
        return "Error: Invalid characters in expression"
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Collect all tools
tools = [greet, get_current_time, calculate]


# ===========================================
# Agent Server
# ===========================================

async def run_server():
    """Run the agent as an HTTP server."""
    credential = DefaultAzureCredential()
    
    try:
        client = AzureAIAgentClient(
            project_endpoint=ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        )
        
        agent = client.create_agent(
            name="MyAgent",
            model=MODEL_DEPLOYMENT_NAME,
            instructions="""You are a helpful assistant. You can:
- Greet people by name
- Tell the current time
- Perform basic math calculations

Be friendly and helpful. Use the available tools when appropriate.""",
            tools=tools,
        )
        
        logger.info("Starting MyAgent HTTP Server...")
        print("Starting MyAgent HTTP Server on port 8088...")
        
        await from_agent_framework(agent).run_async()
    finally:
        await credential.close()


def main():
    """Main entry point."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
```

### src/MyAgent/requirements.txt

```
# Core agent packages
agent-framework-azure-ai
agent-framework-core
azure-ai-agentserver-agentframework

# Web server (required by agent server)
uvicorn
fastapi

# Azure identity
azure-identity

# Environment
python-dotenv

# Monitoring
azure-monitor-opentelemetry
```

### src/MyAgent/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./ user_agent/

WORKDIR /app/user_agent

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8088

ENV PORT=8088
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
```

### infra/main.parameters.json

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environmentName": { "value": "${AZURE_ENV_NAME}" },
    "location": { "value": "${AZURE_LOCATION}" },
    "aiDeploymentsLocation": { "value": "${AZURE_AI_DEPLOYMENTS_LOCATION}" },
    "principalId": { "value": "${AZURE_PRINCIPAL_ID}" },
    "principalType": { "value": "${AZURE_PRINCIPAL_TYPE}" },
    "aiProjectDeploymentsJson": { "value": "${AI_PROJECT_DEPLOYMENTS}" },
    "aiProjectConnectionsJson": { "value": "${AI_PROJECT_CONNECTIONS}" },
    "aiProjectDependentResourcesJson": { "value": "${AI_PROJECT_DEPENDENT_RESOURCES}" },
    "enableHostedAgents": { "value": "${ENABLE_HOSTED_AGENTS=true}" }
  }
}
```

### infra/main.bicep

For the Bicep file, either:

1. **Use the official starter template** (recommended):
   ```bash
   azd init -t Azure-Samples/azd-ai-starter-basic
   ```
   Then copy the `infra/` folder to your project.

2. **Or copy from the bicep-templates.md reference file** in this skill.

## Project Structure Summary

```
my-agent/
├── azure.yaml                 # Project configuration
├── infra/
│   ├── main.bicep            # Infrastructure definition
│   ├── main.parameters.json  # Parameter mappings
│   └── core/
│       └── ai/
│           └── ai-project.bicep
└── src/
    └── MyAgent/
        ├── agent.yaml        # Agent metadata
        ├── Dockerfile        # Container build
        ├── main.py           # Agent code
        └── requirements.txt  # Python dependencies
```

## Customization Points

After scaffolding, users typically customize:

1. **Agent name**: Change `MyAgent` throughout all files
2. **Tools**: Add/modify functions in `main.py`
3. **Instructions**: Update the agent's system prompt
4. **Model**: Change from `gpt-4o-mini` to `gpt-4o` for more capability
5. **Scaling**: Adjust `minReplicas`/`maxReplicas` for production

## Adding More Tools

To add a new tool, define a function with type annotations:

```python
def my_new_tool(
    param1: Annotated[str, "Description of param1"],
    param2: Annotated[int, "Description of param2"] = 10
) -> str:
    """What this tool does (shown to the model).
    
    Args:
        param1: More details about param1
        param2: More details about param2
    """
    # Implementation
    return f"Result: {param1}, {param2}"

# Add to tools list
tools = [greet, get_current_time, calculate, my_new_tool]
```

## Next Steps After Deployment

1. **Test in Playground**: Visit the Azure AI Foundry portal link from `azd up` output
2. **View Logs**: `azd monitor --logs`
3. **Update Agent**: Make changes, then run `azd deploy`
4. **Clean Up**: `azd down` to delete all resources
