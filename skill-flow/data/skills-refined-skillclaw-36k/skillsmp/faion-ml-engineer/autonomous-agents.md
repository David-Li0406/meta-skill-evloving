---
id: autonomous-agents
name: "Autonomous Agents"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Autonomous Agents

## Overview

Autonomous agents are LLM-powered systems that can independently plan, execute tasks, use tools, and iterate toward goals. They combine reasoning, memory, and action capabilities to accomplish complex objectives with minimal human intervention.

## When to Use

- Complex multi-step tasks
- Tasks requiring tool orchestration
- Research and analysis workflows
- Code generation and execution
- When tasks require iteration and self-correction
- Automating knowledge work

## Key Concepts

### Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS AGENT                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   MEMORY    │  │   PLANNING  │  │    TOOLS    │         │
│  │ - Short-term│  │ - Task decomp│  │ - Web search│         │
│  │ - Long-term │  │ - Prioritize│  │ - Code exec │         │
│  │ - Episodic  │  │ - Reflect   │  │ - File I/O  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│                   ┌──────▼──────┐                           │
│                   │     LLM     │                           │
│                   │   (Brain)   │                           │
│                   └──────┬──────┘                           │
│                          │                                  │
│                   ┌──────▼──────┐                           │
│                   │   ACTION    │                           │
│                   │  EXECUTOR   │                           │
│                   └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### Agent Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| ReAct | Reason + Act loop | General tasks |
| Plan-and-Execute | Plan first, then execute | Complex projects |
| Reflexion | Self-critique and improve | Learning tasks |
| AutoGPT-style | Full autonomy with goals | Research, automation |

## Implementation

### Basic ReAct Agent

```python
from openai import OpenAI
from typing import List, Dict, Callable, Any
import json

client = OpenAI()

class Tool:
    """Represents an agent tool."""

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: dict
    ):
        self.name = name
        self.description = description
        self.function = function
        self.parameters = parameters

    def to_openai_format(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    def execute(self, **kwargs) -> str:
        try:
            result = self.function(**kwargs)
            return json.dumps(result) if not isinstance(result, str) else result
        except Exception as e:
            return f"Error: {str(e)}"

class ReActAgent:
    """Simple ReAct agent implementation."""

    def __init__(
        self,
        tools: List[Tool],
        model: str = "gpt-4o",
        max_iterations: int = 10,
        system_prompt: str = None
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.max_iterations = max_iterations
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.messages = []

    def _default_system_prompt(self) -> str:
        return """You are a helpful AI assistant with access to tools.

When you need to accomplish a task:
1. Think about what you need to do
2. Use available tools when needed
3. Analyze tool results
4. Continue until the task is complete

Always explain your reasoning before taking actions."""

    def run(self, task: str) -> str:
        """Run the agent on a task."""
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task}
        ]

        for iteration in range(self.max_iterations):
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=[t.to_openai_format() for t in self.tools.values()],
                tool_choice="auto"
            )

            message = response.choices[0].message

            # No tool calls - task complete
            if not message.tool_calls:
                return message.content

            # Process tool calls
            self.messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"[Tool] {tool_name}: {arguments}")

                if tool_name in self.tools:
                    result = self.tools[tool_name].execute(**arguments)
                else:
                    result = f"Unknown tool: {tool_name}"

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return "Max iterations reached without completion."
```

### Plan-and-Execute Agent

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Task:
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None
    dependencies: List[int] = None

class PlanAndExecuteAgent:
    """Agent that creates a plan before executing."""

    def __init__(
        self,
        tools: List[Tool],
        model: str = "gpt-4o",
        planner_model: str = "gpt-4o"
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.planner_model = planner_model
        self.plan: List[Task] = []

    def create_plan(self, goal: str) -> List[Task]:
        """Create a plan to achieve the goal."""
        tools_description = "\n".join([
            f"- {t.name}: {t.description}"
            for t in self.tools.values()
        ])

        prompt = f"""Create a step-by-step plan to achieve this goal.

Goal: {goal}

Available tools:
{tools_description}

Return a JSON array of tasks:
[{{"description": "task description", "dependencies": [0, 1]}}]

Dependencies are indices of tasks that must complete first.
Keep the plan focused and minimal."""

        response = client.chat.completions.create(
            model=self.planner_model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        tasks_data = json.loads(response.choices[0].message.content)

        self.plan = [
            Task(
                description=t["description"],
                dependencies=t.get("dependencies", [])
            )
            for t in tasks_data.get("tasks", tasks_data)
        ]

        return self.plan

    def execute_task(self, task: Task) -> str:
        """Execute a single task."""
        task.status = "in_progress"

        # Get context from completed dependencies
        context = ""
        if task.dependencies:
            context = "Previous task results:\n"
            for dep_idx in task.dependencies:
                if dep_idx < len(self.plan):
                    context += f"- {self.plan[dep_idx].description}: {self.plan[dep_idx].result}\n"

        prompt = f"""{context}

Current task: {task.description}

Complete this task using available tools. Explain your approach."""

        messages = [
            {"role": "system", "content": "You are an AI assistant executing a plan."},
            {"role": "user", "content": prompt}
        ]

        # Execute with tools
        for _ in range(5):  # Max iterations per task
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[t.to_openai_format() for t in self.tools.values()],
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                task.result = message.content
                task.status = "completed"
                return message.content

            messages.append(message)

            for tool_call in message.tool_calls:
                result = self.tools[tool_call.function.name].execute(
                    **json.loads(tool_call.function.arguments)
                )
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        task.status = "failed"
        return "Task execution timeout"

    def run(self, goal: str) -> str:
        """Run the full plan-and-execute loop."""
        # Create plan
        self.create_plan(goal)
        print(f"Created plan with {len(self.plan)} tasks")

        # Execute tasks in order (respecting dependencies)
        results = []

        while any(t.status == "pending" for t in self.plan):
            for i, task in enumerate(self.plan):
                if task.status != "pending":
                    continue

                # Check dependencies
                deps_complete = all(
                    self.plan[d].status == "completed"
                    for d in task.dependencies
                    if d < len(self.plan)
                )

                if deps_complete:
                    print(f"Executing task {i + 1}: {task.description}")
                    result = self.execute_task(task)
                    results.append(f"Task {i + 1}: {result}")

        return "\n\n".join(results)
```

### Reflexion Agent

```python
class ReflexionAgent:
    """Agent that learns from mistakes through self-reflection."""

    def __init__(
        self,
        tools: List[Tool],
        model: str = "gpt-4o",
        max_attempts: int = 3
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.max_attempts = max_attempts
        self.reflections: List[str] = []

    def attempt_task(self, task: str, previous_attempts: List[dict] = None) -> dict:
        """Make one attempt at the task."""
        context = ""
        if previous_attempts:
            context = "Previous attempts and reflections:\n"
            for attempt in previous_attempts:
                context += f"\nAttempt: {attempt['action']}\n"
                context += f"Result: {attempt['result']}\n"
                context += f"Reflection: {attempt['reflection']}\n"

        messages = [
            {
                "role": "system",
                "content": f"""You are an AI agent that learns from mistakes.
{context}

Based on previous attempts (if any), improve your approach.
Explain your reasoning before taking action."""
            },
            {"role": "user", "content": task}
        ]

        # Execute with tools
        action_log = []
        for _ in range(5):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[t.to_openai_format() for t in self.tools.values()]
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return {
                    "action": "\n".join(action_log),
                    "result": message.content,
                    "success": True
                }

            messages.append(message)

            for tool_call in message.tool_calls:
                action = f"{tool_call.function.name}({tool_call.function.arguments})"
                action_log.append(action)

                result = self.tools[tool_call.function.name].execute(
                    **json.loads(tool_call.function.arguments)
                )

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return {
            "action": "\n".join(action_log),
            "result": "Max iterations reached",
            "success": False
        }

    def reflect(self, task: str, attempt: dict) -> str:
        """Reflect on an attempt to improve future attempts."""
        prompt = f"""Reflect on this attempt at the task.

Task: {task}

Actions taken:
{attempt['action']}

Result:
{attempt['result']}

Was this successful? What could be improved?
What should be done differently next time?

Provide a brief, actionable reflection."""

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def run(self, task: str, success_check: Callable = None) -> str:
        """Run with reflection and retry."""
        attempts = []

        for attempt_num in range(self.max_attempts):
            print(f"Attempt {attempt_num + 1}/{self.max_attempts}")

            # Make attempt
            attempt = self.attempt_task(task, attempts)

            # Check success
            if success_check:
                success = success_check(attempt["result"])
            else:
                success = attempt["success"]

            if success:
                return attempt["result"]

            # Reflect on failure
            reflection = self.reflect(task, attempt)
            attempt["reflection"] = reflection
            attempts.append(attempt)
            self.reflections.append(reflection)

            print(f"Reflection: {reflection}")

        return f"Failed after {self.max_attempts} attempts. Last result: {attempts[-1]['result']}"
```

### Memory System

```python
from datetime import datetime
from typing import List, Dict, Optional
import numpy as np

class Memory:
    """Agent memory system with short-term and long-term storage."""

    def __init__(
        self,
        embedding_func: Callable,
        max_short_term: int = 10,
        relevance_threshold: float = 0.7
    ):
        self.embedding_func = embedding_func
        self.max_short_term = max_short_term
        self.relevance_threshold = relevance_threshold

        self.short_term: List[Dict] = []
        self.long_term: List[Dict] = []  # Would use vector DB in production

    def add(self, content: str, metadata: Dict = None):
        """Add memory entry."""
        entry = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "embedding": self.embedding_func(content)
        }

        self.short_term.append(entry)

        # Move old memories to long-term
        if len(self.short_term) > self.max_short_term:
            old_entry = self.short_term.pop(0)
            self.long_term.append(old_entry)

    def recall(self, query: str, k: int = 5) -> List[Dict]:
        """Recall relevant memories."""
        query_embedding = self.embedding_func(query)
        all_memories = self.short_term + self.long_term

        if not all_memories:
            return []

        # Calculate similarities
        similarities = []
        for memory in all_memories:
            sim = np.dot(query_embedding, memory["embedding"]) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(memory["embedding"])
            )
            similarities.append((memory, sim))

        # Filter and sort
        relevant = [
            (m, s) for m, s in similarities
            if s >= self.relevance_threshold
        ]
        relevant.sort(key=lambda x: x[1], reverse=True)

        return [m for m, _ in relevant[:k]]

    def summarize_recent(self) -> str:
        """Summarize recent memories."""
        if not self.short_term:
            return "No recent memories."

        recent = self.short_term[-5:]
        return "\n".join([m["content"] for m in recent])

class AgentWithMemory:
    """Agent with memory capabilities."""

    def __init__(
        self,
        tools: List[Tool],
        embedding_func: Callable,
        model: str = "gpt-4o"
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.memory = Memory(embedding_func)

    def run(self, task: str) -> str:
        """Run agent with memory context."""
        # Recall relevant memories
        relevant_memories = self.memory.recall(task, k=3)
        memory_context = ""
        if relevant_memories:
            memory_context = "\nRelevant past experiences:\n"
            for mem in relevant_memories:
                memory_context += f"- {mem['content']}\n"

        system_prompt = f"""You are an AI assistant with memory.
{memory_context}

Use your past experiences to inform your decisions."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ]

        # Execute (simplified)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=[t.to_openai_format() for t in self.tools.values()]
        )

        result = response.choices[0].message.content or "Task completed"

        # Store experience
        self.memory.add(
            f"Task: {task}\nResult: {result}",
            metadata={"type": "task_completion"}
        )

        return result
```

### Production Agent Framework

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Callable
from enum import Enum
import logging
import asyncio

class AgentState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    COMPLETE = "complete"
    FAILED = "failed"

@dataclass
class AgentConfig:
    model: str = "gpt-4o"
    max_iterations: int = 20
    max_tool_calls_per_iteration: int = 5
    timeout_seconds: int = 300
    enable_reflection: bool = True
    enable_memory: bool = True

class ProductionAgent:
    """Production-ready autonomous agent."""

    def __init__(
        self,
        tools: List[Tool],
        config: Optional[AgentConfig] = None,
        embedding_func: Callable = None
    ):
        self.tools = {t.name: t for t in tools}
        self.config = config or AgentConfig()
        self.logger = logging.getLogger(__name__)

        self.state = AgentState.IDLE
        self.messages: List[Dict] = []
        self.execution_log: List[Dict] = []

        if self.config.enable_memory and embedding_func:
            self.memory = Memory(embedding_func)
        else:
            self.memory = None

    async def run(self, goal: str) -> Dict[str, Any]:
        """Run the agent asynchronously."""
        self.state = AgentState.PLANNING
        self.messages = []
        self.execution_log = []

        try:
            result = await asyncio.wait_for(
                self._execute_goal(goal),
                timeout=self.config.timeout_seconds
            )
            self.state = AgentState.COMPLETE
            return {"success": True, "result": result, "log": self.execution_log}

        except asyncio.TimeoutError:
            self.state = AgentState.FAILED
            return {"success": False, "error": "Timeout", "log": self.execution_log}

        except Exception as e:
            self.state = AgentState.FAILED
            self.logger.error(f"Agent error: {e}")
            return {"success": False, "error": str(e), "log": self.execution_log}

    async def _execute_goal(self, goal: str) -> str:
        """Execute the goal."""
        # Build context
        context = self._build_context(goal)

        self.messages = [
            {"role": "system", "content": context["system_prompt"]},
            {"role": "user", "content": goal}
        ]

        self.state = AgentState.EXECUTING

        for iteration in range(self.config.max_iterations):
            self.logger.info(f"Iteration {iteration + 1}")

            response = await self._call_llm()
            message = response.choices[0].message

            # Log iteration
            self.execution_log.append({
                "iteration": iteration + 1,
                "content": message.content,
                "tool_calls": [tc.function.name for tc in (message.tool_calls or [])]
            })

            # No tool calls - check if complete
            if not message.tool_calls:
                if self.config.enable_reflection:
                    self.state = AgentState.REFLECTING
                    is_complete = await self._reflect_on_completion(goal, message.content)
                    if is_complete:
                        return message.content
                    # Continue if reflection says not complete
                    self.state = AgentState.EXECUTING
                else:
                    return message.content

            # Process tool calls
            self.messages.append(message)
            await self._process_tool_calls(message.tool_calls)

        return "Max iterations reached"

    def _build_context(self, goal: str) -> Dict:
        """Build context for the agent."""
        memory_context = ""
        if self.memory:
            relevant = self.memory.recall(goal, k=3)
            if relevant:
                memory_context = "\nRelevant past experiences:\n" + \
                    "\n".join([f"- {m['content'][:200]}" for m in relevant])

        system_prompt = f"""You are an autonomous AI agent working to achieve goals.

{memory_context}

Guidelines:
1. Think step by step before acting
2. Use tools when needed
3. Verify your progress
4. Ask for clarification only when truly stuck

Available tools will be provided. Use them wisely."""

        return {"system_prompt": system_prompt}

    async def _call_llm(self):
        """Call the LLM."""
        return client.chat.completions.create(
            model=self.config.model,
            messages=self.messages,
            tools=[t.to_openai_format() for t in self.tools.values()],
            tool_choice="auto"
        )

    async def _process_tool_calls(self, tool_calls):
        """Process tool calls."""
        for tool_call in tool_calls[:self.config.max_tool_calls_per_iteration]:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            self.logger.info(f"Tool call: {tool_name}")

            if tool_name in self.tools:
                result = self.tools[tool_name].execute(**arguments)
            else:
                result = f"Unknown tool: {tool_name}"

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    async def _reflect_on_completion(self, goal: str, result: str) -> bool:
        """Reflect on whether the goal is achieved."""
        prompt = f"""Goal: {goal}

Current result: {result}

Has the goal been fully achieved? Respond with JSON:
{{"complete": true/false, "reason": "..."}}"""

        response = client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        reflection = json.loads(response.choices[0].message.content)
        return reflection.get("complete", False)
```

## Best Practices

1. **Clear Goal Definition**
   - Specific, measurable objectives
   - Clear success criteria
   - Bounded scope

2. **Tool Design**
   - Clear descriptions
   - Proper error handling
   - Appropriate granularity

3. **Safety**
   - Limit iterations
   - Sandbox code execution
   - Human approval for critical actions

4. **Monitoring**
   - Log all actions
   - Track token usage
   - Alert on failures

5. **Memory Management**
   - Summarize long histories
   - Use relevance filtering
   - Clear stale memories

## Common Pitfalls

1. **Infinite Loops** - No iteration limits
2. **Tool Abuse** - Calling same tool repeatedly
3. **Context Overflow** - Too much history
4. **Hallucinated Actions** - Acting on made-up information
5. **No Guardrails** - Unsafe tool execution
6. **Poor Error Recovery** - Failing on first error

## References

- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Reflexion Paper](https://arxiv.org/abs/2303.11366)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
