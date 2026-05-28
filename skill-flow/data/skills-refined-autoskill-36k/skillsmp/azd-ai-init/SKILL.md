---
name: azd-ai-init
description: Structure agent code for Azure's `azd ai` command. Use when users mention "azd ai", "azd init agent", "Foundry agent", "scaffold agent", "convert to azd", "update for azd", "upgrade to azd ai", "fix azd ai", "migrate to Foundry", or want to deploy, convert, update, fix, or upgrade an AI agent for Azure.
model: claude-opus-4-5
---

# Azure AI Agent Scaffolding Skill

This skill helps developers prepare their AI agent code for deployment to Azure AI Foundry using the `azd ai` extension of the Azure Developer CLI.

## When to Use This Skill

Use this skill when a user wants to:
- **Scaffold a new agent from scratch** (greenfield project with no existing code)
- Convert existing agent code to the `azd ai` expected format
- Scaffold a new Azure AI Foundry agent project from scratch
- Structure their agent for deployment with `azd up`
- Understand what files and configuration `azd ai` requires
- Migrate from other agent frameworks to Azure AI Foundry hosted agents

## Core Workflow

### Step 1: Analyze the User's Current Project

First, understand what the user has:

1. **Detect existing code**: Look for agent implementations (Python, TypeScript, etc.)
2. **Identify the agent framework**: LangGraph, Semantic Kernel, AutoGen, custom, etc.
3. **Find entry points**: main.py, index.ts, or other entry files
4. **Check for existing configuration**: azure.yaml, agent.yaml, Dockerfile, requirements.txt, package.json

### Step 2: Generate Required Files

The `azd ai` extension expects a specific project structure:

```
project-root/
├── azure.yaml              # Project configuration (REQUIRED)
├── infra/                  # Bicep infrastructure files (REQUIRED)
│   ├── main.bicep
│   ├── main.parameters.json
│   └── core/               # Reusable Bicep modules
│       └── ai/
│           └── ai-project.bicep
└── src/
    └── <AgentName>/        # Agent source folder (REQUIRED)
        ├── agent.yaml      # Agent definition (REQUIRED)
        ├── Dockerfile      # Container build file (REQUIRED)
        ├── main.py         # Agent entry point
        └── requirements.txt
```

### Step 3: Create Configuration Files

#### azure.yaml (Project Root)

This is the main project configuration file that defines services and infrastructure:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json

requiredVersions:
    extensions:
        azure.ai.agents: '>=0.1.0-preview'

name: <project-name>

services:
    <AgentName>:
        project: src/<AgentName>
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

#### agent.yaml (Inside src/<AgentName>/)

Defines the agent's metadata, protocols, and environment variables:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/microsoft/AgentSchema/refs/heads/main/schemas/v1.0/ContainerAgent.yaml

kind: hosted
name: <AgentName>
description: "<Brief description of what the agent does>"

metadata:
    authors:
        - <author-name>
    example:
        - content: "<Example user prompt - always quote strings with special characters>"
          role: user
    tags:
        - <tag1>
        - <tag2>

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

**Note:** Set `FOUNDRY_MODEL_DEPLOYMENT_NAME` to match the deployment name in your `azure.yaml` (e.g., `gpt-4o-mini`).

**⚠️ Environment Variable Naming:** The hosted agent platform injects variables with `FOUNDRY_` prefix. Your Python code must read `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL_DEPLOYMENT_NAME` (not `AZURE_*` prefixes). The `agent.yaml` maps Azure outputs to the expected names.

**IMPORTANT YAML Formatting Rules:**
- Always wrap `content:` and `description:` values in double quotes
- Escape internal quotes with backslash: `"He said \"hello\""`
- Strings with colons, commas, or special characters MUST be quoted

#### Dockerfile

Standard Python container for hosted agents:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./ user_agent/

WORKDIR /app/user_agent

RUN if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    else \
        echo "No requirements.txt found"; \
    fi

EXPOSE 8088

ENV PORT=8088

CMD ["python", "main.py"]
```

For TypeScript/Node.js agents:

```dockerfile
FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 8088

ENV PORT=8088

CMD ["node", "dist/main.js"]
```

### Step 4: Adapt the Agent Code

The agent code must use the Azure AI Agent Framework pattern to run as a hosted agent:

### Client Selection Guide

| Scenario | Client Type | Notes |
|----------|-------------|-------|
| Local development with AI Services endpoint | `AzureOpenAIChatClient` | Uses ChatAgent pattern |
| **Hosted agent deployment (azd up)** | `AzureAIAgentClient` | **Required** - Uses create_agent + from_agent_framework |
| Foundry Project endpoint | `AzureAIAgentClient` | Requires FOUNDRY_* env vars |

#### Python Example (using agent_framework)

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

# Define your tools as functions with type annotations
# IMPORTANT: Use simple strings in Annotated[], NOT Pydantic Field objects
def my_tool(
    param1: Annotated[str, "Description of param1"],
    param2: Annotated[int, "Description of param2"]
) -> str:
    """Tool description that the model will see."""
    # Tool implementation
    return "result"

tools = [my_tool]

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
            name="<AgentName>",
            model=MODEL_DEPLOYMENT_NAME,
            instructions="<Your agent system instructions>",
            tools=tools,
        )
        
        logger.info("Starting Agent HTTP Server...")
        await from_agent_framework(agent).run_async()
    finally:
        await credential.close()

def main():
    asyncio.run(run_server())

if __name__ == "__main__":
    main()
```

#### Required Python Dependencies (requirements.txt)

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

## Infrastructure (Bicep Files)

**CRITICAL:** The `azd ai` extension requires infrastructure that provisions `Microsoft.CognitiveServices/accounts/projects` resources. The Bicep modules are complex (~300+ lines) and must be obtained from the official template.

### Getting the Infrastructure (Required)

**Always use the official starter template for infrastructure:**

```bash
# Option 1: Initialize a new project with infra included
azd init -t Azure-Samples/azd-ai-starter-basic

# Option 2: Copy infra to an existing project
git clone --depth 1 https://github.com/Azure-Samples/azd-ai-starter-basic.git temp-starter
cp -r temp-starter/infra ./infra
rm -rf temp-starter
```

The official `infra/` folder contains:

```
infra/
├── main.bicep                 # Main deployment orchestrator
├── main.parameters.json       # Parameter mappings
├── abbreviations.json         # Resource naming conventions
└── core/
    └── ai/
        └── ai-project.bicep   # AI Foundry provisioning module
```

### What the Infrastructure Provisions

The `core/ai/ai-project.bicep` module creates:
- **Microsoft.CognitiveServices/accounts** - AI Services account (Foundry)
- **Microsoft.CognitiveServices/accounts/projects** - Foundry project (nested resource)
- **Container Registry** - For agent container images
- **Application Insights** - Monitoring and logging
- **Log Analytics Workspace** - Log storage
- **Model Deployments** - GPT-4o, GPT-4o-mini, etc.
- **Capability Host** - For hosted agents

### Required Bicep Outputs

The main.bicep must output these environment variables for `azd ai` to work:

```bicep
// Required outputs - azd ai uses these to locate resources
output AZURE_RESOURCE_GROUP string = resourceGroupName
output AZURE_AI_ACCOUNT_ID string = aiProject.outputs.accountId
output AZURE_AI_PROJECT_ID string = aiProject.outputs.projectId
output AZURE_AI_ACCOUNT_NAME string = aiProject.outputs.aiServicesAccountName
output AZURE_AI_PROJECT_NAME string = aiProject.outputs.projectName

// Endpoints
output AZURE_AI_PROJECT_ENDPOINT string = aiProject.outputs.AZURE_AI_PROJECT_ENDPOINT
output AZURE_OPENAI_ENDPOINT string = aiProject.outputs.AZURE_OPENAI_ENDPOINT
output APPLICATIONINSIGHTS_CONNECTION_STRING string = aiProject.outputs.APPLICATIONINSIGHTS_CONNECTION_STRING

// Container Registry
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = aiProject.outputs.dependentResources.registry.loginServer
```

**Note:** The `AZURE_AI_PROJECT_ID` must be in the format:
```
/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}
```

Do NOT use `Microsoft.MachineLearningServices/workspaces` - this is a different resource type that won't work with `azd ai`.

### infra/main.parameters.json

## Model Deployment Configuration

The `deployments` section in `azure.yaml` under each service's `config` defines the AI models:

| Property | Description | Example |
|----------|-------------|---------|
| `name` | Deployment name | `gpt-4o-mini` |
| `model.format` | Model provider | `OpenAI` |
| `model.name` | Model identifier | `gpt-4o-mini` |
| `model.version` | Model version | `2024-07-18` |
| `sku.name` | SKU tier | `GlobalStandard` |
| `sku.capacity` | Tokens per minute (thousands) | `10` |

### Available Models

Common models for agents:
- `gpt-4o` (version: `2024-08-06`)
- `gpt-4o-mini` (version: `2024-07-18`)
- `gpt-4-turbo` (version: `2024-04-09`)

## Region Requirements for Hosted Agents

**IMPORTANT:** Hosted agents are only supported in specific Azure regions.

### Supported Regions (as of January 2026)
- **North Central US** ✅ (Default in templates)

The provided Bicep templates default to `northcentralus`. If you need to change the region, verify hosted agent support first.

## Deployment Commands

After scaffolding, users deploy with:

```bash
# Install the azd ai extension (if not installed)
azd extension install azure.ai.agents

# Login to Azure
azd auth login

# Initialize environment (creates .azure folder)
azd init

# Provision infrastructure and deploy agent
azd up
```

Or step-by-step:

```bash
azd provision    # Create Azure resources
azd deploy       # Deploy the agent
```

### Troubleshooting Deployment

If `azd deploy` times out waiting for the container:

1. **Check container logs** in Azure Portal:
   - Go to the AI Foundry project
   - Navigate to Agents section
   - Check container status and logs

2. **Common issues:**
   - Missing dependencies in `requirements.txt`
   - Import errors in agent code
   - Agent not listening on port 8088
   - Missing environment variables

3. **Test locally first:**
   ```bash
   cd src/YourAgent
   pip install -r requirements.txt
   python main.py
   ```

4. **Verify the agent starts a server:**
   The agent must call `from_agent_framework(agent).run_async()` to start the HTTP server.

## Guidelines for Converting Existing Agents

### From LangGraph/LangChain

1. Keep the graph/chain logic intact
2. Wrap it in the `AzureAIAgentClient` pattern
3. Expose tools as annotated functions
4. Use `from_agent_framework(agent).run_async()` to serve

### From Semantic Kernel

1. Convert plugins to tool functions
2. Use the same agent hosting pattern
3. Map kernel functions to `tools` list

### From AutoGen

1. Extract agent logic into tool functions
2. Define single agent using `AzureAIAgentClient`
3. Multi-agent patterns may need restructuring

## Common Customizations

### Adding Environment Variables

In `agent.yaml`:
```yaml
environment_variables:
  - name: CUSTOM_VAR
    value: ${MY_ENV_VAR}
```

In `azure.yaml` under service config:
```yaml
config:
  env:
    CUSTOM_VAR: "value"
```

### Adding Azure Resources (Connections)

For agents needing additional Azure services (search, storage, etc.), add to `azure.yaml`:

```yaml
config:
  resources:
    - resource: search
      connectionName: my-search-connection
    - resource: storage
      connectionName: my-storage-connection
```

Available resource types:
- `search` - Azure AI Search
- `storage` - Azure Storage
- `registry` - Azure Container Registry
- `bing_grounding` - Bing Search
- `bing_custom_grounding` - Bing Custom Search

### Scaling Configuration

```yaml
config:
  container:
    resources:
      cpu: "2"
      memory: 4Gi
    scale:
      minReplicas: 1
      maxReplicas: 10
```

## Greenfield Scaffolding (No Existing Code)

When a user has no existing code and wants to create a new agent from scratch, generate a complete working project.

### Quick Start Template

For users who say "create a new agent for azd ai" or "scaffold a new Foundry agent", generate this complete structure:

#### 1. Create Project Structure

```bash
mkdir -p my-agent/src/MyAgent my-agent/infra/core/ai
```

#### 2. azure.yaml (Project Root)

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

#### 3. src/MyAgent/agent.yaml

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

#### 4. src/MyAgent/main.py

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
    # Safe evaluation of basic math
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

#### 5. src/MyAgent/requirements.txt

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

#### 6. src/MyAgent/Dockerfile

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

#### 7. infra/main.bicep

Use the standard Bicep template from the Infrastructure section above, or point users to clone from the starter template:

```bash
# Alternative: Start from official template
azd init -t Azure-Samples/azd-ai-starter-basic
```

#### 8. infra/main.parameters.json

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

### Final Project Structure

```
my-agent/
├── azure.yaml
├── infra/
│   ├── main.bicep
│   ├── main.parameters.json
│   └── core/
│       └── ai/
│           └── ai-project.bicep
└── src/
    └── MyAgent/
        ├── agent.yaml
        ├── Dockerfile
        ├── main.py
        └── requirements.txt
```

### Deploy the Agent

```bash
cd my-agent

# Login to Azure
azd auth login

# Initialize environment (creates .azure folder)
azd init

# Deploy everything
azd up
```

The agent will be live at the Azure AI Foundry endpoint shown in the output.

---

## Example: Complete Scaffolding Session (Existing Code)

When a user says "prepare my calculator agent for azd ai":

1. **Analyze**: Find their `calculator.py` with add/multiply/divide functions
2. **Create structure**:
   - Create `src/CalculatorAgent/` directory
   - Move/adapt code to `main.py`
   - Create `agent.yaml` with metadata
   - Create `Dockerfile`
   - Create `requirements.txt`
3. **Create root configs**:
   - Create `azure.yaml` with service definition
   - Create `infra/` with Bicep files
4. **Provide next steps**: Tell user to run `azd up`

## References

- [Azure Developer CLI Documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [azd ai agent extension](https://github.com/Azure/azure-dev/tree/main/cli/azd/extensions/azure.ai.agents)
- [Azure AI Foundry](https://ai.azure.com)
- [Agent Framework Samples](https://github.com/azure-ai-foundry/foundry-samples)
- [azd-ai-starter-basic template](https://github.com/Azure-Samples/azd-ai-starter-basic)

## YAML Validation Checklist

**Before completing, always validate generated YAML files:**

1. **Quote all string values** that contain:
   - Colons (`:`)
   - Commas (`,`)
   - Special characters (`#`, `&`, `*`, `!`, `|`, `>`, `'`, `"`, `%`, `@`, `` ` ``)
   - Leading/trailing spaces

2. **Required quoting patterns:**
   ```yaml
   # CORRECT
   description: "A helpful agent that answers questions."
   content: "What is 2 + 2?"
   content: "Subject: Meeting - Let's discuss the project."
   
   # INCORRECT - will break parsing
   description: A helpful agent that answers questions.
   content: What is 2 + 2?
   content: Subject: Meeting - Let's discuss the project.
   ```

3. **Escape internal quotes:**
   ```yaml
   content: "He said \"hello\" to everyone."
   ```

4. **Validate YAML syntax** before finishing:
   ```bash
   # Python
   python -c "import yaml; yaml.safe_load(open('agent.yaml'))"
   
   # Node.js
   node -e "require('js-yaml').load(require('fs').readFileSync('agent.yaml'))"
   ```

5. **Check for common errors:**
   - Inconsistent indentation (use 2 or 4 spaces, not tabs)
   - Missing quotes around values with special characters
   - Trailing whitespace
   - Missing required fields
