# How It Works

## How It Works

### Phase 1: Agent Architecture Design

```
User Request → Analyze:
- Single agent vs multi-agent system?
- Tools needed (Code Exec, Memory Bank, custom tools)?
- Orchestration pattern (Sequential, Parallel, Loop)?
- Integration with LangChain/Genkit?
- Deployment target (local, Agent Engine, Cloud Run)?
```

### Phase 2: ADK Agent Implementation

**Simple Agent (Python)**:
```python
from google import adk

# Define agent with tools
agent = adk.Agent(
    model="gemini-2.5-flash",
    tools=[
        adk.tools.CodeExecution(),  # Secure sandbox
        adk.tools.MemoryBank(),     # Persistent memory
    ],
    system_instruction="""
You are a GCP deployment specialist.
Help users deploy resources securely using gcloud commands.
    """
)

# Run agent
response = agent.run("Deploy a GKE cluster named prod in us-central1")
print(response)
```

**Multi-Agent Orchestrator (Python)**:
```python
from google import adk

# Define specialized sub-agents
validator_agent = adk.Agent(
    model="gemini-2.5-flash",
    system_instruction="Validate GCP configurations"
)

deployer_agent = adk.Agent(
    model="gemini-2.5-flash",
    tools=[adk.tools.CodeExecution()],
    system_instruction="Deploy validated GCP resources"
)

monitor_agent = adk.Agent(
    model="gemini-2.5-flash",
    system_instruction="Monitor deployment status"
)

# Orchestrate with Sequential pattern
orchestrator = adk.SequentialAgent(
    agents=[validator_agent, deployer_agent, monitor_agent],
    system_instruction="Coordinate validation → deployment → monitoring"
)

result = orchestrator.run("Deploy a production GKE cluster")
```

### Phase 3: Code Execution Integration

The Code Execution Sandbox provides:
- **Security**: Isolated environment, no access to your system
- **State Persistence**: 14-day memory, configurable TTL
- **Stateful Sessions**: Builds on previous executions

```python
# Agent with Code Execution
agent = adk.Agent(
    model="gemini-2.5-flash",
    tools=[adk.tools.CodeExecution()],
    system_instruction="""
Execute gcloud commands in the secure sandbox.
Remember previous operations in this session.
    """
)

# Turn 1: Create cluster
agent.run("Create GKE cluster named dev-cluster with 3 nodes")
# Sandbox executes: gcloud container clusters create dev-cluster --num-nodes=3

# Turn 2: Deploy to cluster (remembers cluster from Turn 1)
agent.run("Deploy my-app:latest to that cluster")
# Sandbox remembers dev-cluster, executes kubectl commands
```

### Phase 4: Memory Bank Integration

Persistent conversation memory across sessions:

```python
agent = adk.Agent(
    model="gemini-2.5-flash",
    tools=[adk.tools.MemoryBank()],
    system_instruction="Remember user preferences and project context"
)

# Session 1 (Monday)
agent.run("I prefer deploying to us-central1 region", session_id="user-123")

# Session 2 (Wednesday) - same session_id
agent.run("Deploy a Cloud Run service", session_id="user-123")
# Agent remembers: uses us-central1 automatically
```

### Phase 5: A2A Protocol Deployment

Deploy agent to Agent Engine with A2A endpoint:

```bash
# Install ADK
pip install google-adk

# Deploy with one command
adk deploy \
  --agent-file agent.py \
  --project-id my-project \
  --region us-central1 \
  --service-name gcp-deployer-agent
```

Agent Engine creates:
- **A2A Endpoint**: `https://gcp-deployer-agent-{hash}.run.app`
- **AgentCard**: `/.well-known/agent-card` metadata
- **Task API**: `/v1/tasks:send` for task submission
- **Status API**: `/v1/tasks/{task_id}` for polling

### Phase 6: Calling from Claude

Once deployed, Claude can invoke via A2A protocol:

```python
# In Claude Code plugin / external script
import requests

def invoke_adk_agent(message, session_id=None):
    """
    Call deployed ADK agent via A2A protocol.
    """
    response = requests.post(
        "https://gcp-deployer-agent-xyz.run.app/v1/tasks:send",
        json={
            "message": message,
            "session_id": session_id or "claude-session-123",
            "config": {
                "enable_code_execution": True,
                "enable_memory_bank": True,
            }
        },
        headers={"Authorization": f"Bearer {get_token()}"}
    )

    return response.json()

# Use from Claude
result = invoke_adk_agent("Deploy GKE cluster named prod-api")
```