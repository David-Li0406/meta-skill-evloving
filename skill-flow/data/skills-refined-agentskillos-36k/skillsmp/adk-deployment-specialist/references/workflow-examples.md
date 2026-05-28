# Workflow Examples

## Workflow Examples

### Example 1: GCP Deployment Agent

**User**: "Create an ADK agent that deploys GCP resources"

**Implementation**:
```python
from google import adk

deployment_agent = adk.Agent(
    model="gemini-2.5-flash",
    tools=[
        adk.tools.CodeExecution(),
        adk.tools.MemoryBank(),
    ],
    system_instruction="""
You are a GCP deployment specialist.

CAPABILITIES:
- Deploy GKE clusters
- Deploy Cloud Run services
- Deploy Vertex AI Pipelines
- Manage IAM permissions
- Monitor deployments

SECURITY:
- Validate all configurations before deployment
- Use least-privilege IAM
- Log all operations
- Never expose credentials
    """
)

# Deploy to Agent Engine
# $ adk deploy --agent-file deployment_agent.py --service-name gcp-deployer
```

### Example 2: Multi-Agent RAG System

**User**: "Build a RAG system with ADK orchestrating a LangChain retriever"

**Implementation**:
```python
from google import adk
from langchain.retrievers import VertexAISearchRetriever

# Sub-Agent 1: LangChain RAG
class RAGAgent(adk.Agent):
    def __init__(self):
        self.retriever = VertexAISearchRetriever(...)
        super().__init__(model="gemini-2.5-flash")

    def retrieve_docs(self, query):
        return self.retriever.get_relevant_documents(query)

# Sub-Agent 2: ADK Answer Generator
answer_agent = adk.Agent(
    model="gemini-2.5-pro",  # More powerful for final answer
    system_instruction="Generate comprehensive answers from retrieved docs"
)

# Orchestrator
orchestrator = adk.SequentialAgent(
    agents=[RAGAgent(), answer_agent],
    system_instruction="First retrieve docs, then generate answer"
)
```

### Example 3: Async Deployment with Status Polling

**User**: "Deploy a GKE cluster and monitor progress"

**Implementation**:
```python
# Submit async task
task_response = invoke_adk_agent(
    "Deploy GKE cluster named prod-api with 5 nodes in us-central1"
)

task_id = task_response["task_id"]
print(f"✅ Task submitted: {task_id}")

# Poll for status
import time
while True:
    status = requests.get(
        f"https://gcp-deployer-agent-xyz.run.app/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {get_token()}"}
    ).json()

    if status["status"] == "SUCCESS":
        print(f"✅ Cluster deployed!")
        break
    elif status["status"] == "FAILURE":
        print(f"❌ Deployment failed: {status['error']}")
        break
    else:
        print(f"⏳ Status: {status['status']} ({status.get('progress', 0)*100}%)")
        time.sleep(10)
```