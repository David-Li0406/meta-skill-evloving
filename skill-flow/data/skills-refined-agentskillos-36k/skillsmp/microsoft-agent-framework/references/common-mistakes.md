# Common Mistakes to Avoid

This document lists anti-patterns and incorrect implementations. **DO NOT** use these patterns.

---

## ❌ Creating Custom Agent Classes

**WRONG:**
```python
# DO NOT create custom agent base classes
class MyAgent:
    def __init__(self, model_client):
        self.client = model_client
        self.history = []
    
    async def chat(self, message):
        self.history.append(message)
        response = await self.client.complete(self.history)
        return response

class SpecializedAgent(MyAgent):
    def __init__(self, model_client, specialty):
        super().__init__(model_client)
        self.specialty = specialty
```

**CORRECT:**
```python
from agent_framework import ChatAgent

# Use ChatAgent with custom instructions
agent = ChatAgent(
    chat_client=client,
    instructions="You are a specialized assistant for X.",
    name="specialized-agent"
)
```

---

## ❌ Building Custom Orchestration Logic

**WRONG:**
```python
# DO NOT build custom orchestrators
class AgentPipeline:
    def __init__(self, agents):
        self.agents = agents
    
    async def run(self, input):
        result = input
        for agent in self.agents:
            result = await agent.run(result)
        return result

class ParallelAgents:
    async def run_all(self, agents, input):
        tasks = [agent.run(input) for agent in agents]
        return await asyncio.gather(*tasks)
```

**CORRECT:**
```python
from agent_framework.workflows import Workflow, AgentExecutor, Edge
from agent_framework.workflows.orchestrations import (
    SequentialOrchestration,
    ConcurrentOrchestration
)

# Sequential
sequential = SequentialOrchestration(agents=[agent1, agent2, agent3])

# Parallel
parallel = ConcurrentOrchestration(
    agents=[agent1, agent2, agent3],
    aggregator=summarizer
)

# Custom workflow
workflow = Workflow(
    executors=[
        AgentExecutor(agent=agent1, name="step1"),
        AgentExecutor(agent=agent2, name="step2"),
    ],
    edges=[
        Edge(source="start", target="step1"),
        Edge(source="step1", target="step2"),
    ]
)
```

---

## ❌ Manual Conversation History Management

**WRONG:**
```python
# DO NOT manage history manually
messages = []

async def chat(user_input):
    messages.append({"role": "user", "content": user_input})
    response = await client.complete(messages)
    messages.append({"role": "assistant", "content": response})
    return response
```

**CORRECT:**
```python
from agent_framework import ChatAgent, AgentThread

agent = ChatAgent(chat_client=client, instructions="...")
thread = AgentThread()  # MAF manages history

result1 = await agent.run("Hello", thread=thread)
result2 = await agent.run("Follow up", thread=thread)  # Has context
```

---

## ❌ Custom Tool Wrappers

**WRONG:**
```python
# DO NOT create custom tool abstractions
class Tool:
    def __init__(self, name, func, description):
        self.name = name
        self.func = func
        self.description = description
    
    def to_schema(self):
        return {"name": self.name, "description": self.description}

tools = [
    Tool("weather", get_weather, "Get weather"),
    Tool("search", search_web, "Search the web"),
]
```

**CORRECT:**
```python
from typing import Annotated
from pydantic import Field

# Just use annotated functions directly
def get_weather(
    location: Annotated[str, Field(description="City name")]
) -> str:
    """Get weather for a location."""  # Description from docstring
    return f"Weather in {location}: sunny"

agent = ChatAgent(
    chat_client=client,
    tools=[get_weather, search_web]  # Pass functions directly
)
```

---

## ❌ Forgetting Context Managers

**WRONG:**
```python
# MCP tools MUST use async with
mcp = MCPStdioTool(name="fs", command="uvx", args=["mcp-server-fs"])
result = await agent.run("query", tools=mcp)  # ERROR: Not connected!
```

**CORRECT:**
```python
async with MCPStdioTool(
    name="fs",
    command="uvx", 
    args=["mcp-server-fs"]
) as mcp:
    result = await agent.run("query", tools=mcp)
# Connection properly closed
```

---

## ❌ Sharing Workflow Instances

**WRONG:**
```python
# DO NOT share workflow instances across requests
workflow = Workflow(...)  # Created once

@app.post("/process")
async def handle_request(data):
    # Multiple concurrent requests share same instance!
    return await workflow.run(data)
```

**CORRECT:**
```python
def create_workflow():
    return Workflow(
        executors=[...],
        edges=[...]
    )

@app.post("/process")
async def handle_request(data):
    workflow = create_workflow()  # New instance per request
    return await workflow.run(data)
```

---

## ❌ Ignoring Type Safety in Workflows

**WRONG:**
```python
# Passing untyped dicts between executors
@Executor.register
class Step1(Executor):
    async def execute(self, input, context):
        return {"result": "something"}  # Untyped

@Executor.register  
class Step2(Executor):
    async def execute(self, input, context):
        # What fields does input have? Unknown!
        return input["result"]
```

**CORRECT:**
```python
from pydantic import BaseModel

class Step1Output(BaseModel):
    result: str
    confidence: float

class Step2Input(BaseModel):
    result: str
    confidence: float

@Executor.register
class Step1(Executor[dict, Step1Output]):
    async def execute(self, input, context) -> Step1Output:
        return Step1Output(result="something", confidence=0.9)

@Executor.register
class Step2(Executor[Step2Input, str]):
    async def execute(self, input: Step2Input, context) -> str:
        # Type-safe access
        return f"Got {input.result} with {input.confidence}"
```

---

## ❌ Too Many Tools Per Agent

**WRONG:**
```python
# DO NOT overload agents with tools
agent = ChatAgent(
    chat_client=client,
    tools=[tool1, tool2, tool3, ... tool50]  # Too many!
)
```

**CORRECT:**
```python
# Use workflows for complex tool sets
# Or use specialized agents
general_agent = ChatAgent(
    chat_client=client,
    tools=[common_tool1, common_tool2]  # Keep under 20
)

# Complex tasks: use orchestration
workflow = Workflow(
    executors=[
        AgentExecutor(agent=search_agent, name="search"),
        AgentExecutor(agent=analysis_agent, name="analyze"),
        AgentExecutor(agent=output_agent, name="output"),
    ],
    ...
)
```

---

## ❌ Direct LLM Calls in Agent Logic

**WRONG:**
```python
# DO NOT bypass MAF for LLM calls
class MyService:
    async def process(self, input):
        # Direct OpenAI call - loses all MAF features
        response = await openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": input}]
        )
        return response.choices[0].message.content
```

**CORRECT:**
```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

class MyService:
    def __init__(self):
        self.agent = ChatAgent(
            chat_client=OpenAIChatClient(),
            instructions="You process requests."
        )
    
    async def process(self, input):
        result = await self.agent.run(input)
        return result.text
```

---

## ❌ Hardcoding Model in Multiple Places

**WRONG:**
```python
# Model config scattered everywhere
agent1 = ChatAgent(chat_client=OpenAIChatClient(model_id="gpt-4o"), ...)
agent2 = ChatAgent(chat_client=OpenAIChatClient(model_id="gpt-4o"), ...)
agent3 = ChatAgent(chat_client=OpenAIChatClient(model_id="gpt-4o"), ...)
```

**CORRECT:**
```python
# Centralize client configuration
def create_chat_client():
    return OpenAIChatClient(
        base_url=settings.MODEL_ENDPOINT,
        api_key=settings.API_KEY,
        model_id=settings.MODEL_NAME
    )

client = create_chat_client()

agent1 = ChatAgent(chat_client=client, instructions="Agent 1")
agent2 = ChatAgent(chat_client=client, instructions="Agent 2")
agent3 = ChatAgent(chat_client=client, instructions="Agent 3")
```

---

## ❌ Not Using Factory Methods

**WRONG:**
```python
# Verbose agent creation
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient()
agent = ChatAgent(
    chat_client=client,
    instructions="You help with code."
)
```

**CORRECT (when simpler):**
```python
from agent_framework.openai import OpenAIChatClient

# Use factory method
agent = OpenAIChatClient().create_agent(
    instructions="You help with code."
)
```

---

---

## ❌ Creating Custom Builder Classes (MOST CRITICAL)

**WRONG:**
```python
# DO NOT implement builders from scratch
class ConcurrentBuilderAdapter:
    def __init__(self):
        self._tasks = []  # Custom implementation

    def build(self):
        # Custom workflow construction
        return CustomWorkflow(self._tasks)

class _MockGroupChatWorkflow:
    # Custom group chat implementation
    pass

class MagenticManagerBase(ABC):
    # Custom manager base class definition
    @abstractmethod
    async def plan(self, context):
        ...
```

**CORRECT:**
```python
from agent_framework import (
    ConcurrentBuilder,
    GroupChatBuilder,
    MagenticBuilder,
    MagenticManagerBase,  # Import, don't define
)

class ConcurrentBuilderAdapter:
    def __init__(self):
        self._builder = ConcurrentBuilder()  # Use official builder

    def build(self):
        return self._builder.build()  # Call official API

# Extend official base class, don't redefine
class CustomManager(MagenticManagerBase):  # ✅ Extends official
    async def plan(self, context):
        ...
```

---

## ❌ Missing Official Builder Import

**WRONG:**
```python
# No import from agent_framework
class WorkflowExecutorAdapter:
    def __init__(self, workflow, id):
        self.workflow = workflow
        self.id = id
```

**CORRECT:**
```python
from agent_framework import WorkflowExecutor

class WorkflowExecutorAdapter(WorkflowExecutor):
    def __init__(self, workflow, id, **kwargs):
        super().__init__(workflow=workflow, id=id, **kwargs)
```

---

## Summary: When You See These Patterns, Stop

| If you're about to... | Stop and use... |
|-----------------------|-----------------|
| Create a custom `Agent` class | `ChatAgent` |
| Build a `Pipeline` or `Orchestrator` | `Workflow` or built-in orchestrations |
| Manage `messages = []` list | `AgentThread` |
| Create a `Tool` class | Annotated functions |
| Call OpenAI directly | `ChatAgent` with appropriate client |
| Share workflow instances | Create new instance per request |
| **Implement `ConcurrentBuilder`** | `from agent_framework import ConcurrentBuilder` |
| **Implement `GroupChatBuilder`** | `from agent_framework import GroupChatBuilder` |
| **Implement `HandoffBuilder`** | `from agent_framework import HandoffBuilder` |
| **Implement `MagenticBuilder`** | `from agent_framework import MagenticBuilder` |
| **Define `MagenticManagerBase`** | `from agent_framework import MagenticManagerBase` |
| **Create `WorkflowExecutor`** | `from agent_framework import WorkflowExecutor` |

---

## Verification

Always run after implementing builders:
```bash
cd backend && python scripts/verify_official_api_usage.py
# Must show: 5/5 checks passed
```
