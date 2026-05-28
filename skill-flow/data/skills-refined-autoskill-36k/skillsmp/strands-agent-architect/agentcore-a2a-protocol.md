# Agent-to-Agent (A2A) Protocol with Amazon Bedrock AgentCore

This document covers the A2A protocol for multi-agent coordination, with emphasis on using Google ADK as an orchestrator agent within the AgentCore ecosystem.

## 1. Introduction to A2A Protocol

### What is A2A?

The Agent-to-Agent (A2A) protocol is an open standard that enables AI agents built on different frameworks to communicate, coordinate, and collaborate. It addresses a distinct coordination challenge from MCP:

| Protocol | Purpose | Connection Type |
|----------|---------|-----------------|
| **MCP** | Agent-to-Resource | Connects agents to tools, APIs, and data sources |
| **A2A** | Agent-to-Agent | Enables agents to coordinate with other agents |

### Key Capabilities

- **Standardized Agent Cards**: JSON metadata describing capabilities, skills, and communication endpoints
- **Cross-Framework Interoperability**: Agents from Google ADK, Strands, OpenAI SDK, LangGraph can collaborate
- **JSON-RPC 2.0 Communication**: Standard message format over HTTP/S or Server-Sent Events
- **OAuth 2.0 Security**: Secure authentication between agents

### When to Use A2A

Use A2A when you need:
- Multiple specialized agents working together
- Cross-framework agent coordination
- Task delegation and orchestration
- Separation of concerns across agent boundaries

---

## 2. Architecture Patterns

### Hub-and-Spoke Architecture

The most common pattern uses a **Host Agent** (orchestrator) that delegates tasks to **Specialized Agents**:

```
                    ┌─────────────────────┐
                    │   Host Agent        │
                    │   (Google ADK)      │
                    │   - Orchestration   │
                    │   - Task routing    │
                    └──────────┬──────────┘
                               │ A2A Protocol
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Monitoring Agent │ │ Remediation Agent│ │ Search Agent     │
│ (Strands SDK)    │ │ (OpenAI SDK)     │ │ (LangGraph)      │
│ - CloudWatch     │ │ - Fix strategies │ │ - Web search     │
│ - Logs analysis  │ │ - Automation     │ │ - Documentation  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### Agent Roles

| Role | Description | Behavior |
|------|-------------|----------|
| **A2A Server** | Exposes capabilities via Agent Card | Receives and processes delegated tasks |
| **A2A Client** | Discovers and invokes other agents | Sends tasks to specialized agents |
| **Host Agent** | Acts as both client and orchestrator | Routes tasks, aggregates responses |

---

## 3. Agent Card Schema

Every A2A-enabled agent publishes an **Agent Card** - a JSON metadata file that advertises its identity, capabilities, and endpoints.

### Agent Card Structure

```json
{
  "name": "monitoring-agent",
  "description": "Handles AWS metrics and logs analysis across accounts",
  "version": "1.0.0",
  "capabilities": [
    {
      "name": "analyze_metrics",
      "description": "Analyze CloudWatch metrics for anomalies",
      "inputSchema": {
        "type": "object",
        "properties": {
          "metric_namespace": { "type": "string" },
          "time_range": { "type": "string" }
        },
        "required": ["metric_namespace"]
      }
    },
    {
      "name": "query_logs",
      "description": "Query CloudWatch Logs with insights",
      "inputSchema": {
        "type": "object",
        "properties": {
          "log_group": { "type": "string" },
          "query": { "type": "string" }
        },
        "required": ["log_group", "query"]
      }
    }
  ],
  "endpoint": "https://bedrock-agentcore.us-east-2.amazonaws.com/runtimes/...",
  "authentication": {
    "type": "oauth2",
    "tokenUrl": "https://cognito-idp.us-east-2.amazonaws.com/..."
  }
}
```

### Agent Card Discovery

Agents discover each other through:
1. **Static Configuration**: Agent Cards stored in known locations
2. **Registry Service**: Centralized agent discovery service
3. **AgentCore Gateway**: Gateway can proxy A2A discovery

---

## 4. Google ADK as A2A Host Agent

Google ADK is well-suited for the Host Agent role due to its:
- Native async support
- Flexible tool integration
- Strong orchestration capabilities

### Host Agent Implementation

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import aiohttp
import json

APP_NAME = "incident_response_orchestrator"

# A2A Client Tool - Delegates tasks to specialized agents
async def delegate_to_agent(
    agent_endpoint: str,
    capability: str,
    parameters: dict,
    auth_token: str
) -> dict:
    """
    Delegate a task to another agent via A2A protocol.

    Args:
        agent_endpoint: The A2A server endpoint URL
        capability: The capability/skill to invoke
        parameters: Input parameters for the capability
        auth_token: OAuth bearer token for authentication

    Returns:
        Agent response as dictionary
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tasks/send",
        "params": {
            "capability": capability,
            "input": parameters
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            agent_endpoint,
            json=payload,
            headers={
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
        ) as response:
            return await response.json()


# Define A2A delegation tool for ADK agent
def create_a2a_delegate_tool(agent_registry: dict):
    """Create an ADK tool that delegates to registered A2A agents."""

    async def a2a_delegate(
        agent_name: str,
        capability: str,
        parameters: dict
    ) -> str:
        """
        Delegate a task to a specialized agent.

        Args:
            agent_name: Name of the target agent (monitoring, remediation, search)
            capability: The capability to invoke on the target agent
            parameters: Input parameters for the capability

        Returns:
            Result from the specialized agent
        """
        if agent_name not in agent_registry:
            return f"Error: Agent '{agent_name}' not found in registry"

        agent_info = agent_registry[agent_name]
        result = await delegate_to_agent(
            agent_endpoint=agent_info["endpoint"],
            capability=capability,
            parameters=parameters,
            auth_token=agent_info["token"]
        )

        return json.dumps(result.get("result", result))

    return a2a_delegate


# Agent Registry - Known specialized agents
AGENT_REGISTRY = {
    "monitoring": {
        "endpoint": "https://bedrock-agentcore.../monitoring-agent/invocations",
        "token": "${MONITORING_AGENT_TOKEN}",
        "capabilities": ["analyze_metrics", "query_logs", "get_alarms"]
    },
    "remediation": {
        "endpoint": "https://bedrock-agentcore.../remediation-agent/invocations",
        "token": "${REMEDIATION_AGENT_TOKEN}",
        "capabilities": ["suggest_fix", "apply_remediation", "rollback"]
    },
    "search": {
        "endpoint": "https://bedrock-agentcore.../search-agent/invocations",
        "token": "${SEARCH_AGENT_TOKEN}",
        "capabilities": ["web_search", "doc_search", "best_practices"]
    }
}

# Host Agent Definition
host_agent = Agent(
    model="gemini-3-pro",
    name="incident_response_host",
    description="Orchestrates incident response by coordinating specialized agents",
    instruction="""
You are an incident response orchestrator. When investigating issues:

1. Use the monitoring agent to gather metrics and logs
2. Use the search agent to find relevant documentation and best practices
3. Use the remediation agent to suggest and apply fixes

Always gather sufficient context before suggesting remediation.
Coordinate agents efficiently - parallelize independent tasks.
Synthesize results from multiple agents into clear recommendations.
""",
    tools=[create_a2a_delegate_tool(AGENT_REGISTRY)]
)
```

### Running the Host Agent on AgentCore

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import asyncio

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload: dict, context) -> dict:
    """
    Main entrypoint for the A2A Host Agent.
    """
    query = payload.get("prompt", "")
    user_id = payload.get("user_id", "anonymous")
    session_id = getattr(context, "session_id", "default")

    # Run the host agent
    result = asyncio.run(run_host_agent(query, user_id, session_id))

    return {"result": result}


async def run_host_agent(query: str, user_id: str, session_id: str) -> str:
    """Execute the host agent with A2A delegation capabilities."""
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )

    runner = Runner(
        agent=host_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    content = types.Content(
        role='user',
        parts=[types.Part(text=query)]
    )

    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )

    async for event in events:
        if event.is_final_response():
            return event.content.parts[0].text

    return "No response generated"


if __name__ == "__main__":
    app.run()
```

---

## 5. A2A Server Implementation (Specialized Agent)

Specialized agents run as A2A servers, exposing capabilities via the protocol.

### Strands-Based Monitoring Agent

```python
from strands import Agent
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import json

# Monitoring tools
def analyze_cloudwatch_metrics(namespace: str, metric_name: str, period: str) -> str:
    """Analyze CloudWatch metrics for the specified namespace."""
    # Implementation would query CloudWatch
    return json.dumps({
        "namespace": namespace,
        "metric": metric_name,
        "anomalies": [],
        "trend": "stable"
    })

def query_cloudwatch_logs(log_group: str, query: str, time_range: str) -> str:
    """Query CloudWatch Logs using Insights."""
    # Implementation would run CloudWatch Logs Insights query
    return json.dumps({
        "log_group": log_group,
        "results": [],
        "matched_events": 0
    })

# Strands Agent
monitoring_agent = Agent(
    model=BedrockModel(model_id="anthropic.claude-sonnet-4-5-20250929-v1:0"),
    tools=[analyze_cloudwatch_metrics, query_cloudwatch_logs]
)

# A2A Server Entrypoint
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload: dict, context) -> dict:
    """
    A2A Server entrypoint for monitoring agent.

    Handles both direct invocations and A2A protocol messages.
    """
    # Check if this is an A2A protocol message
    if "jsonrpc" in payload:
        return handle_a2a_request(payload)

    # Direct invocation
    prompt = payload.get("prompt", "")
    response = monitoring_agent(prompt)
    return {"result": response.message}


def handle_a2a_request(payload: dict) -> dict:
    """Handle A2A JSON-RPC requests."""
    method = payload.get("method", "")
    params = payload.get("params", {})
    request_id = payload.get("id", 1)

    if method == "tasks/send":
        capability = params.get("capability", "")
        input_data = params.get("input", {})

        # Route to appropriate capability
        if capability == "analyze_metrics":
            result = analyze_cloudwatch_metrics(**input_data)
        elif capability == "query_logs":
            result = query_cloudwatch_logs(**input_data)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Unknown capability: {capability}"}
            }

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": json.loads(result)
        }

    elif method == "agent/card":
        # Return Agent Card for discovery
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "name": "monitoring-agent",
                "description": "AWS monitoring and log analysis",
                "capabilities": ["analyze_metrics", "query_logs"]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"}
    }


if __name__ == "__main__":
    app.run()
```

---

## 6. Authentication for A2A

### OAuth 2.0 Flow

A2A uses OAuth 2.0 for secure agent-to-agent authentication:

```python
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

async def get_agent_token(agent_name: str, client_info: dict) -> str:
    """
    Get OAuth token for authenticating with another agent.

    Uses AgentCore Identity service for token management.
    """
    client = GatewayClient(region_name="us-east-2")
    token = client.get_access_token_for_cognito(client_info)
    return token
```

### Token Propagation

When the host agent delegates to specialized agents, it propagates authentication:

```python
# Host agent receives user's token
user_token = context.get("authorization_token")

# For service-to-service calls, use dedicated agent credentials
agent_token = await get_agent_token("monitoring", AGENT_CREDENTIALS)

# Include token in A2A request
headers = {
    "Authorization": f"Bearer {agent_token}",
    "X-Original-User-Token": user_token  # For audit trail
}
```

---

## 7. Deployment Configuration

### Deploy Host Agent

```bash
cd host_agent/
agentcore configure -e main.py
agentcore deploy --env MONITORING_AGENT_ENDPOINT=... \
                 --env REMEDIATION_AGENT_ENDPOINT=... \
                 --env SEARCH_AGENT_ENDPOINT=...
```

### Deploy Specialized Agents

```bash
# Deploy each agent independently
cd monitoring_agent/
agentcore configure -e main.py
agentcore deploy

cd ../remediation_agent/
agentcore configure -e main.py
agentcore deploy

cd ../search_agent/
agentcore configure -e main.py
agentcore deploy
```

### Terraform Configuration

```hcl
# Multi-agent A2A deployment
resource "aws_bedrock_agentcore_runtime" "host_agent" {
  name = "incident-response-host"

  container_config {
    image_uri = "${aws_ecr_repository.host_agent.repository_url}:latest"
  }

  environment_variables = {
    MONITORING_AGENT_ENDPOINT  = aws_bedrock_agentcore_runtime.monitoring_agent.endpoint
    REMEDIATION_AGENT_ENDPOINT = aws_bedrock_agentcore_runtime.remediation_agent.endpoint
    SEARCH_AGENT_ENDPOINT      = aws_bedrock_agentcore_runtime.search_agent.endpoint
  }
}

resource "aws_bedrock_agentcore_runtime" "monitoring_agent" {
  name = "monitoring-agent"
  # ... configuration
}

resource "aws_bedrock_agentcore_runtime" "remediation_agent" {
  name = "remediation-agent"
  # ... configuration
}

resource "aws_bedrock_agentcore_runtime" "search_agent" {
  name = "search-agent"
  # ... configuration
}
```

---

## 8. Best Practices

### Design Principles

1. **Single Responsibility**: Each agent should have a focused domain
2. **Idempotency**: Agent operations should be safely retryable
3. **Graceful Degradation**: Host should handle agent failures gracefully
4. **Observability**: Log all A2A interactions for debugging

### Error Handling

```python
async def safe_delegate(agent_name: str, capability: str, params: dict) -> dict:
    """Delegate with error handling and fallback."""
    try:
        result = await delegate_to_agent(agent_name, capability, params)
        return {"success": True, "result": result}
    except TimeoutError:
        return {"success": False, "error": f"Agent {agent_name} timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Performance Optimization

```python
import asyncio

async def parallel_delegation(tasks: list[dict]) -> list[dict]:
    """Execute multiple A2A delegations in parallel."""
    coroutines = [
        delegate_to_agent(
            task["agent"],
            task["capability"],
            task["params"]
        )
        for task in tasks
    ]
    return await asyncio.gather(*coroutines, return_exceptions=True)
```

---

## 9. References

- [A2A Protocol Announcement](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)
- [A2A Multi-Agent Sample](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/02-use-cases/A2A-multi-agent-incident-response)
- [AgentCore Runtime Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
