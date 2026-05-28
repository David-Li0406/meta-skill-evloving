# Hybrid Architecture Guide

Integration patterns for combining Claude Agent SDK with Microsoft Agent Framework in IPA Platform.

## Overview

This guide describes how to combine:

- **Microsoft Agent Framework** - Structured multi-agent workflows (GroupChat, Handoff, Concurrent, Nested)
- **Claude Agent SDK** - Autonomous agents with independent reasoning

Together they create a **hybrid orchestration** system that handles both predictable workflows and unpredictable situations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        IPA Platform                                  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Orchestration Layer                        │   │
│  │                                                               │   │
│  │  ┌─────────────────────┐    ┌─────────────────────────────┐  │   │
│  │  │  Microsoft Agent    │    │  Claude Agent SDK           │  │   │
│  │  │  Framework          │    │                             │  │   │
│  │  │                     │    │                             │  │   │
│  │  │  - GroupChatBuilder │    │  - query()                  │  │   │
│  │  │  - HandoffBuilder   │    │  - ClaudeSDKClient          │  │   │
│  │  │  - ConcurrentBuilder│    │  - Built-in Tools           │  │   │
│  │  │  - MagenticBuilder  │    │  - Hooks                    │  │   │
│  │  │  - WorkflowExecutor │    │  - MCP Integration          │  │   │
│  │  │                     │    │  - Subagents                │  │   │
│  │  └─────────────────────┘    └─────────────────────────────┘  │   │
│  │            │                            │                     │   │
│  │            └────────────┬───────────────┘                     │   │
│  │                         │                                     │   │
│  │              ┌──────────▼──────────┐                          │   │
│  │              │  HybridOrchestrator │                          │   │
│  │              │                     │                          │   │
│  │              │  - Task Router      │                          │   │
│  │              │  - Fallback Logic   │                          │   │
│  │              │  - Error Recovery   │                          │   │
│  │              └─────────────────────┘                          │   │
│  │                                                               │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## When to Use Each

| Scenario | Agent Framework | Claude SDK | Hybrid |
|----------|-----------------|------------|--------|
| Predefined workflows | ✓ | | |
| Multi-agent chat | ✓ | | |
| Agent handoff | ✓ | | |
| Parallel execution | ✓ | | |
| Autonomous reasoning | | ✓ | |
| Tool usage + thinking | | ✓ | |
| Error investigation | | ✓ | |
| Complex debugging | | ✓ | |
| Unpredictable tasks | | ✓ | |
| Workflow + fallback | | | ✓ |
| Structured + adaptive | | | ✓ |

---

## Integration Patterns

### Pattern 1: Sequential Fallback

Try structured workflow first, fall back to autonomous agent if it fails.

```python
# backend/src/integrations/hybrid/sequential_fallback.py

from agent_framework import GroupChatBuilder
from claude_sdk import ClaudeSDKClient
from src.core.logging import get_logger

logger = get_logger(__name__)

class SequentialFallbackOrchestrator:
    """
    Try structured workflow first, fall back to Claude SDK if needed.

    Use when:
    - Task usually follows a pattern but sometimes needs flexibility
    - Error recovery requires investigation
    """

    def __init__(self):
        # Structured workflow
        self._workflow_builder = GroupChatBuilder()

        # Autonomous agent for fallback
        self._autonomous_client = ClaudeSDKClient(
            model="claude-sonnet-4-20250514",
            system_prompt="""
            You are an autonomous problem solver.
            The structured workflow failed. Investigate the issue and find a solution.
            Use available tools to understand and fix the problem.
            """
        )

    async def execute(self, task: str, context: dict = None) -> dict:
        """Execute task with fallback."""
        try:
            # Try structured workflow first
            logger.info(f"Attempting structured workflow for: {task}")
            result = await self._execute_workflow(task, context)
            return {"success": True, "source": "workflow", "result": result}

        except WorkflowError as e:
            # Workflow failed - fall back to autonomous agent
            logger.warning(f"Workflow failed: {e}. Falling back to autonomous agent.")

            autonomous_result = await self._execute_autonomous(
                task=task,
                error=str(e),
                context=context
            )

            return {
                "success": True,
                "source": "autonomous",
                "result": autonomous_result,
                "fallback_reason": str(e)
            }

    async def _execute_workflow(self, task: str, context: dict):
        workflow = self._workflow_builder.build()
        return await workflow.execute(task, context=context)

    async def _execute_autonomous(self, task: str, error: str, context: dict):
        async with self._autonomous_client.create_session() as session:
            prompt = f"""
            Task: {task}

            The structured workflow failed with error: {error}

            Context: {context}

            Please investigate and complete the task.
            """
            return await session.query(prompt)
```

### Pattern 2: Task Router

Route tasks to appropriate executor based on characteristics.

```python
# backend/src/integrations/hybrid/task_router.py

from enum import Enum
from typing import Optional
from agent_framework import GroupChatBuilder, ConcurrentBuilder
from claude_sdk import ClaudeSDKClient

class TaskType(Enum):
    STRUCTURED = "structured"
    AUTONOMOUS = "autonomous"
    HYBRID = "hybrid"

class TaskRouter:
    """
    Route tasks to appropriate executor.

    Use when:
    - Different task types require different execution strategies
    - You want to optimize for each task type
    """

    def __init__(self):
        self._classifiers = [
            self._check_structured_keywords,
            self._check_autonomous_keywords,
            self._check_complexity,
        ]

        # Executors
        self._structured_executor = GroupChatBuilder()
        self._autonomous_executor = ClaudeSDKClient(
            model="claude-sonnet-4-20250514"
        )

    def classify(self, task: str, context: dict = None) -> TaskType:
        """Classify task type."""
        scores = {
            TaskType.STRUCTURED: 0,
            TaskType.AUTONOMOUS: 0,
        }

        for classifier in self._classifiers:
            result = classifier(task, context)
            for task_type, score in result.items():
                scores[task_type] += score

        # Determine winner
        if scores[TaskType.STRUCTURED] > scores[TaskType.AUTONOMOUS]:
            return TaskType.STRUCTURED
        elif scores[TaskType.AUTONOMOUS] > scores[TaskType.STRUCTURED]:
            return TaskType.AUTONOMOUS
        else:
            return TaskType.HYBRID

    async def execute(self, task: str, context: dict = None) -> dict:
        """Route and execute task."""
        task_type = self.classify(task, context)

        if task_type == TaskType.STRUCTURED:
            return await self._execute_structured(task, context)
        elif task_type == TaskType.AUTONOMOUS:
            return await self._execute_autonomous(task, context)
        else:  # HYBRID
            return await self._execute_hybrid(task, context)

    def _check_structured_keywords(self, task: str, context: dict) -> dict:
        """Check for structured workflow keywords."""
        structured_keywords = [
            "workflow", "process", "sequence", "step by step",
            "pipeline", "handoff", "parallel", "concurrent"
        ]

        score = sum(1 for kw in structured_keywords if kw in task.lower())
        return {TaskType.STRUCTURED: score}

    def _check_autonomous_keywords(self, task: str, context: dict) -> dict:
        """Check for autonomous reasoning keywords."""
        autonomous_keywords = [
            "debug", "investigate", "analyze", "figure out",
            "why", "how", "explore", "find the cause",
            "troubleshoot", "diagnose"
        ]

        score = sum(1 for kw in autonomous_keywords if kw in task.lower())
        return {TaskType.AUTONOMOUS: score}

    def _check_complexity(self, task: str, context: dict) -> dict:
        """Estimate task complexity."""
        # Simple heuristic: longer tasks tend to be more complex
        word_count = len(task.split())

        if word_count > 50:
            return {TaskType.AUTONOMOUS: 2}
        elif word_count < 10:
            return {TaskType.STRUCTURED: 1}
        return {}

    async def _execute_structured(self, task: str, context: dict):
        workflow = self._structured_executor.build()
        result = await workflow.execute(task, context=context)
        return {"source": "structured", "result": result}

    async def _execute_autonomous(self, task: str, context: dict):
        async with self._autonomous_executor.create_session() as session:
            result = await session.query(task)
            return {"source": "autonomous", "result": result}

    async def _execute_hybrid(self, task: str, context: dict):
        # Run both and combine results
        structured_result = await self._execute_structured(task, context)
        autonomous_result = await self._execute_autonomous(task, context)

        return {
            "source": "hybrid",
            "structured_result": structured_result,
            "autonomous_result": autonomous_result
        }
```

### Pattern 3: Claude as Workflow Participant

Use Claude SDK agent as a participant in Agent Framework workflow.

```python
# backend/src/integrations/hybrid/claude_agent_adapter.py

from agent_framework import ChatAgent
from claude_sdk import ClaudeSDKClient

class ClaudeAgentAdapter(ChatAgent):
    """
    Adapt Claude SDK to Agent Framework ChatAgent interface.

    Use when:
    - You want to use Claude SDK's capabilities in GroupChat
    - Mixing Claude and other agents in same workflow
    """

    def __init__(
        self,
        name: str,
        system_prompt: str,
        tools: list = None,
        **kwargs
    ):
        self.name = name
        self._client = ClaudeSDKClient(
            model="claude-sonnet-4-20250514",
            system_prompt=system_prompt,
            tools=tools or []
        )
        self._session = None

    async def run(self, messages: list, **kwargs) -> str:
        """Execute using Claude SDK."""
        if not self._session:
            self._session = await self._client.create_session()

        # Convert Agent Framework messages to prompt
        prompt = self._format_messages(messages)

        # Execute with Claude SDK
        result = await self._session.query(prompt)
        return result.content

    def _format_messages(self, messages: list) -> str:
        """Format messages for Claude SDK."""
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)

    async def close(self):
        """Cleanup session."""
        if self._session:
            await self._session.close()


# Usage in GroupChat
from agent_framework import GroupChatBuilder

# Create Claude-powered agent
investigator = ClaudeAgentAdapter(
    name="investigator",
    system_prompt="You are a security investigator. Analyze code for vulnerabilities.",
    tools=["Read", "Grep", "Glob"]
)

# Create standard agents
reviewer = ChatAgent(
    name="reviewer",
    chat_client=azure_client,
    instructions="Review code quality"
)

# Combine in GroupChat
builder = GroupChatBuilder()
builder.add_participant(investigator)
builder.add_participant(reviewer)

workflow = builder.build()
```

### Pattern 4: Autonomous Error Recovery

Use Claude SDK for intelligent error recovery in workflows.

```python
# backend/src/integrations/hybrid/error_recovery.py

from agent_framework import WorkflowExecutor, WorkflowError
from claude_sdk import ClaudeSDKClient

class SmartErrorRecovery:
    """
    Intelligent error recovery using Claude SDK.

    Use when:
    - Workflow errors need investigation
    - Standard retry logic isn't sufficient
    - Root cause analysis is needed
    """

    def __init__(self):
        self._workflow_executor = WorkflowExecutor()
        self._recovery_agent = ClaudeSDKClient(
            model="claude-sonnet-4-20250514",
            system_prompt="""
            You are an expert at diagnosing and fixing workflow errors.

            When given an error:
            1. Analyze the error message and context
            2. Investigate using available tools
            3. Determine the root cause
            4. Suggest or implement a fix
            5. Verify the fix works
            """,
            tools=["Read", "Grep", "Glob", "Bash"]
        )

    async def execute_with_recovery(
        self,
        workflow,
        task: str,
        max_recovery_attempts: int = 3
    ) -> dict:
        """Execute workflow with intelligent recovery."""
        last_error = None

        for attempt in range(max_recovery_attempts + 1):
            try:
                if attempt == 0:
                    # First attempt - normal execution
                    result = await self._workflow_executor.execute(workflow, task)
                    return {"success": True, "result": result, "attempts": 1}
                else:
                    # Recovery attempt
                    recovery_result = await self._attempt_recovery(
                        task=task,
                        error=last_error,
                        attempt=attempt
                    )

                    if recovery_result.get("fixed"):
                        # Try workflow again
                        result = await self._workflow_executor.execute(workflow, task)
                        return {
                            "success": True,
                            "result": result,
                            "attempts": attempt + 1,
                            "recovery_applied": recovery_result.get("fix_description")
                        }

            except WorkflowError as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")

        # All recovery attempts failed
        return {
            "success": False,
            "error": str(last_error),
            "attempts": max_recovery_attempts + 1,
            "recovery_attempts": max_recovery_attempts
        }

    async def _attempt_recovery(
        self,
        task: str,
        error: Exception,
        attempt: int
    ) -> dict:
        """Attempt intelligent recovery."""
        async with self._recovery_agent.create_session() as session:
            prompt = f"""
            Workflow Error Analysis (Attempt {attempt})

            Task: {task}

            Error: {error}

            Please:
            1. Investigate the root cause
            2. Determine if the error is recoverable
            3. If recoverable, implement a fix
            4. Return whether the fix was successful

            Use available tools to investigate and fix.
            """

            result = await session.query(prompt)

            # Parse recovery result
            return {
                "fixed": "fixed" in result.content.lower() or "resolved" in result.content.lower(),
                "fix_description": result.content,
                "tool_calls": [tc.to_dict() for tc in result.tool_calls]
            }
```

---

## Project Structure

```
backend/src/integrations/
├── agent_framework/           # Microsoft Agent Framework adapters
│   └── builders/
│       ├── groupchat.py
│       ├── handoff.py
│       └── ...
│
├── claude_sdk/                # Claude Agent SDK integration
│   ├── __init__.py
│   ├── client.py              # ClaudeSDKAdapter
│   ├── hooks/
│   │   ├── __init__.py
│   │   ├── approval.py        # Approval hook
│   │   ├── audit.py           # Audit hook
│   │   └── sandbox.py         # Sandbox hook
│   └── mcp/
│       ├── __init__.py
│       └── servers.py         # MCP server configs
│
└── hybrid/                    # Hybrid orchestration
    ├── __init__.py
    ├── orchestrator.py        # HybridOrchestrator
    ├── router.py              # TaskRouter
    ├── fallback.py            # SequentialFallbackOrchestrator
    ├── recovery.py            # SmartErrorRecovery
    └── adapters.py            # ClaudeAgentAdapter
```

---

## Configuration

### Environment Variables

```bash
# Microsoft Agent Framework
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5.2

# Claude Agent SDK
ANTHROPIC_API_KEY=sk-ant-xxx
CLAUDE_MODEL=claude-sonnet-4-20250514

# Hybrid Settings
HYBRID_DEFAULT_EXECUTOR=structured  # structured, autonomous, hybrid
HYBRID_FALLBACK_ENABLED=true
HYBRID_MAX_RECOVERY_ATTEMPTS=3
```

### Configuration File

```yaml
# config/hybrid.yaml
orchestration:
  default_executor: structured
  fallback_enabled: true
  max_recovery_attempts: 3

routing:
  structured_keywords:
    - workflow
    - process
    - sequence
    - pipeline

  autonomous_keywords:
    - debug
    - investigate
    - analyze
    - troubleshoot

claude_sdk:
  model: claude-sonnet-4-20250514
  max_tokens: 8192
  tools:
    - Read
    - Write
    - Edit
    - Bash
    - Grep
    - Glob

  hooks:
    - approval:
        tools: [Write, Edit, Bash]
    - audit:
        log_file: ./logs/claude-sdk.log
```

---

## Best Practices

### 1. Clear Separation of Concerns

```python
# Good - clear boundaries
class HybridOrchestrator:
    def __init__(self):
        self._workflow = WorkflowBuilder()  # Structured
        self._autonomous = ClaudeSDKClient()  # Autonomous

    async def execute(self, task):
        # Clear routing logic
        if self._is_structured(task):
            return await self._workflow.execute(task)
        else:
            return await self._autonomous.query(task)
```

### 2. Consistent Error Handling

```python
# Good - consistent error handling
try:
    result = await orchestrator.execute(task)
except WorkflowError as e:
    # Log and handle workflow errors
    logger.error(f"Workflow error: {e}")
except ClaudeSDKError as e:
    # Log and handle SDK errors
    logger.error(f"SDK error: {e}")
```

### 3. Logging and Monitoring

```python
class HybridOrchestrator:
    async def execute(self, task):
        start_time = time.time()

        try:
            result = await self._execute(task)
            self._log_success(task, result, time.time() - start_time)
            return result
        except Exception as e:
            self._log_failure(task, e, time.time() - start_time)
            raise

    def _log_success(self, task, result, duration):
        logger.info(
            "Task completed",
            extra={
                "task": task[:100],
                "source": result.get("source"),
                "duration": duration
            }
        )
```

### 4. Testing Hybrid Flows

```python
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def orchestrator():
    return HybridOrchestrator()

async def test_structured_task_uses_workflow(orchestrator):
    task = "Execute the standard data pipeline workflow"
    result = await orchestrator.execute(task)
    assert result["source"] == "structured"

async def test_autonomous_task_uses_claude(orchestrator):
    task = "Debug why the authentication is failing and fix it"
    result = await orchestrator.execute(task)
    assert result["source"] == "autonomous"

async def test_fallback_on_workflow_failure(orchestrator):
    # Mock workflow to fail
    orchestrator._workflow_executor.execute = AsyncMock(
        side_effect=WorkflowError("Step 3 failed")
    )

    task = "Process the data"
    result = await orchestrator.execute(task)

    assert result["source"] == "autonomous"
    assert "fallback_reason" in result
```

---

## Migration Guide

### From Pure Agent Framework

1. Add Claude SDK dependency
2. Create hybrid orchestrator
3. Identify autonomous use cases
4. Add fallback logic
5. Test hybrid flows

### From Pure Claude SDK

1. Add Agent Framework adapters
2. Identify structured workflows
3. Create workflow definitions
4. Route structured tasks to workflows
5. Keep autonomous for remaining tasks
