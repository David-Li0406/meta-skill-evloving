# Multi-Agent Patterns

This guide covers common patterns and architectures for building multi-agent systems with the OpenAI Agents SDK.

## Architecture Patterns

### Sequential Workflow Pattern
Agents process tasks in sequence, each building on the previous agent's output.

```python
from agents import Agent, Runner, function_tool
import asyncio

# Define specialized agents
researcher = Agent(name="Researcher", instructions="Research topics", ...)
summarizer = Agent(name="Summarizer", instructions="Summarize information", ...)
analyst = Agent(name="Analyst", instructions="Analyze content", ...)

async def sequential_workflow(topic: str):
    """Sequential processing: Research → Summarize → Analyze"""
    # Step 1: Research
    research_result = await Runner.run(researcher, f"Research {topic}")

    # Step 2: Summarize
    summary_result = await Runner.run(
        summarizer,
        f"Summarize: {research_result.final_output}"
    )

    # Step 3: Analyze
    analysis_result = await Runner.run(
        analyst,
        f"Analyze: {summary_result.final_output}"
    )

    return analysis_result.final_output
```

### Parallel Processing Pattern
Multiple agents work simultaneously on different aspects of a task.

```python
import asyncio
from agents import Agent, Runner

async def parallel_processing(query: str):
    """Process query through multiple agents in parallel"""
    # Define specialized agents
    agents = {
        "technical": Agent(name="Technical Expert", ...),
        "creative": Agent(name="Creative Writer", ...),
        "analytical": Agent(name="Data Analyst", ...)
    }

    # Run all agents in parallel
    tasks = []
    for agent_name, agent in agents.items():
        task = Runner.run(
            agent,
            f"From your {agent_name} perspective: {query}"
        )
        tasks.append((agent_name, task))

    # Wait for all results
    results = {}
    for agent_name, task in tasks:
        result = await task
        results[agent_name] = result.final_output

    return results
```

### Supervisor Pattern
A supervisor agent coordinates multiple specialized agents.

```python
from agents import Agent, Runner, function_tool
from typing import Dict, List

class SupervisorSystem:
    def __init__(self):
        self.supervisor = Agent(
            name="Supervisor",
            instructions="Coordinate specialized agents based on task requirements",
            ...
        )

        self.specialists = {
            "research": Agent(name="Researcher", ...),
            "analysis": Agent(name="Analyst", ...),
            "synthesis": Agent(name="Synthesizer", ...)
        }

    async def process_task(self, task: str) -> Dict[str, str]:
        """Supervisor decides which specialists to use"""
        # Supervisor analyzes task
        supervisor_result = await Runner.run(
            self.supervisor,
            f"Analyze this task and decide which specialists to use: {task}"
        )

        # Parse supervisor's decision
        # (In reality, you'd parse the output to determine specialists)

        # Delegate to appropriate specialists
        specialist_results = {}
        for specialist_name, specialist in self.specialists.items():
            result = await Runner.run(
                specialist,
                f"{task} - provide your expertise as a {specialist_name}"
            )
            specialist_results[specialist_name] = result.final_output

        return specialist_results
```

### Hierarchical Pattern
Agents are organized in a hierarchy with different levels of abstraction.

```python
from agents import Agent, Runner

class HierarchicalSystem:
    def __init__(self):
        # High-level strategic agent
        self.strategic_agent = Agent(
            name="Strategic Planner",
            instructions="Plan high-level strategy and delegate to tactical agents",
            ...
        )

        # Mid-level tactical agents
        self.tactical_agents = {
            "implementation": Agent(name="Implementation Specialist", ...),
            "optimization": Agent(name="Optimization Specialist", ...),
            "validation": Agent(name="Validation Specialist", ...)
        }

        # Low-level execution agents
        self.execution_agents = {
            "coder": Agent(name="Code Generator", ...),
            "tester": Agent(name="Test Generator", ...),
            "documenter": Agent(name="Documentation Generator", ...)
        }

    async def execute_project(self, requirements: str):
        """Hierarchical execution from strategy to implementation"""
        # Strategic planning
        strategy = await Runner.run(
            self.strategic_agent,
            f"Plan strategy for: {requirements}"
        )

        # Tactical decomposition
        tactical_results = {}
        for tactical_name, tactical_agent in self.tactical_agents.items():
            tactical_task = f"Based on strategy '{strategy.final_output}', handle {tactical_name}"
            tactical_result = await Runner.run(tactical_agent, tactical_task)
            tactical_results[tactical_name] = tactical_result.final_output

        # Execution
        execution_results = {}
        for exec_name, exec_agent in self.execution_agents.items():
            exec_task = f"Execute {exec_name} tasks based on tactical plans"
            exec_result = await Runner.run(exec_agent, exec_task)
            execution_results[exec_name] = exec_result.final_output

        return {
            "strategy": strategy.final_output,
            "tactical": tactical_results,
            "execution": execution_results
        }
```

## Coordination Patterns

### Handoff Pattern
Agents explicitly hand off tasks to other agents.

```python
from agents import Agent, Runner, handoff

@handoff(from_agent="Researcher", to_agent="Analyst")
async def research_and_analyze(topic: str):
    """Researcher hands off to Analyst after research"""
    research = await research_topic(topic)
    analysis = await analyze_research(research)
    return analysis
```

### Broadcast Pattern
One agent broadcasts to multiple agents simultaneously.

```python
async def broadcast_to_experts(question: str, expert_agents: List[Agent]):
    """Broadcast question to multiple expert agents"""
    tasks = []
    for expert in expert_agents:
        task = Runner.run(
            expert,
            f"As a {expert.name}, answer: {question}"
        )
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return [r.final_output for r in results]
```

### Consensus Pattern
Multiple agents vote or reach consensus.

```python
async def reach_consensus(question: str, voting_agents: List[Agent]):
    """Multiple agents vote on an answer"""
    answers = []
    for agent in voting_agents:
        result = await Runner.run(agent, question)
        answers.append(result.final_output)

    # Simple consensus (in reality, use more sophisticated logic)
    from collections import Counter
    answer_counts = Counter(answers)
    consensus = answer_counts.most_common(1)[0][0]

    return {
        "consensus": consensus,
        "votes": dict(answer_counts),
        "all_answers": answers
    }
```

## Communication Patterns

### Shared Context Pattern
Agents share context through persistent storage.

```python
import json
from typing import Dict, Any

class SharedContext:
    def __init__(self):
        self.context_store: Dict[str, Any] = {}

    async def process_with_context(self, agent: Agent, task: str, context_key: str):
        """Process task with shared context"""
        # Load existing context
        context = self.context_store.get(context_key, {})

        # Process with context
        result = await Runner.run(
            agent,
            f"Context: {json.dumps(context)}\n\nTask: {task}"
        )

        # Update context
        self.context_store[context_key] = {
            **context,
            "last_result": result.final_output,
            "timestamp": "current_time"
        }

        return result.final_output
```

### Message Passing Pattern
Agents communicate through structured messages.

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentMessage:
    sender: str
    recipient: str
    content: str
    metadata: Optional[dict] = None

class MessagePassingSystem:
    def __init__(self):
        self.message_queue: List[AgentMessage] = []
        self.agents: Dict[str, Agent] = {}

    async def send_message(self, message: AgentMessage):
        """Send message to recipient agent"""
        self.message_queue.append(message)

        if message.recipient in self.agents:
            agent = self.agents[message.recipient]
            response = await Runner.run(
                agent,
                f"Message from {message.sender}: {message.content}"
            )

            return AgentMessage(
                sender=message.recipient,
                recipient=message.sender,
                content=response.final_output
            )
```

## Error Handling Patterns

### Fallback Pattern
Primary agent fails → fallback agent takes over.

```python
async def execute_with_fallback(primary_agent: Agent, fallback_agent: Agent, task: str):
    """Try primary agent, fallback if it fails"""
    try:
        result = await Runner.run(primary_agent, task)
        return {"success": True, "agent": "primary", "result": result.final_output}
    except Exception as e:
        print(f"Primary agent failed: {e}, trying fallback...")
        try:
            result = await Runner.run(fallback_agent, task)
            return {"success": True, "agent": "fallback", "result": result.final_output}
        except Exception as e2:
            return {"success": False, "error": str(e2)}
```

### Retry Pattern
Retry failed agent operations.

```python
import asyncio
from typing import Optional

async def retry_agent(agent: Agent, task: str, max_retries: int = 3):
    """Retry agent execution on failure"""
    for attempt in range(max_retries):
        try:
            result = await Runner.run(agent, task)
            return {"success": True, "attempt": attempt + 1, "result": result.final_output}
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                await asyncio.sleep(wait_time)

    return {"success": False, "error": f"Failed after {max_retries} attempts"}
```

## Performance Optimization Patterns

### Caching Pattern
Cache agent responses for repeated queries.

```python
from functools import lru_cache
import hashlib

class CachedAgentSystem:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.cache = {}

    async def run_cached(self, task: str) -> str:
        """Run agent with caching"""
        # Create cache key
        cache_key = hashlib.md5(task.encode()).hexdigest()

        # Check cache
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Run agent
        result = await Runner.run(self.agent, task)

        # Cache result
        self.cache[cache_key] = result.final_output

        return result.final_output
```

### Batch Processing Pattern
Process multiple tasks in batches.

```python
async def batch_process(agent: Agent, tasks: List[str], batch_size: int = 5):
    """Process tasks in batches"""
    results = []

    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{len(tasks)//batch_size + 1}")

        batch_tasks = []
        for task in batch:
            batch_tasks.append(Runner.run(agent, task))

        batch_results = await asyncio.gather(*batch_tasks)
        results.extend([r.final_output for r in batch_results])

    return results
```

## Specialized Use Cases

### Code Review System
```python
class CodeReviewSystem:
    def __init__(self):
        self.reviewers = {
            "syntax": Agent(name="Syntax Reviewer", ...),
            "security": Agent(name="Security Reviewer", ...),
            "performance": Agent(name="Performance Reviewer", ...),
            "style": Agent(name="Style Reviewer", ...)
        }
        self.integrator = Agent(name="Review Integrator", ...)

    async def review_code(self, code: str):
        """Multi-agent code review"""
        # Parallel reviews
        review_tasks = []
        for reviewer_name, reviewer in self.reviewers.items():
            task = Runner.run(
                reviewer,
                f"Review this code from {reviewer_name} perspective:\n{code}"
            )
            review_tasks.append((reviewer_name, task))

        # Gather reviews
        reviews = {}
        for reviewer_name, task in review_tasks:
            result = await task
            reviews[reviewer_name] = result.final_output

        # Integrate reviews
        integration_result = await Runner.run(
            self.integrator,
            f"Integrate these code reviews:\n{json.dumps(reviews, indent=2)}"
        )

        return {
            "individual_reviews": reviews,
            "integrated_review": integration_result.final_output
        }
```

### Content Creation Pipeline
```python
class ContentPipeline:
    def __init__(self):
        self.agents = {
            "researcher": Agent(name="Content Researcher", ...),
            "writer": Agent(name="Content Writer", ...),
            "editor": Agent(name="Content Editor", ...),
            "optimizer": Agent(name="SEO Optimizer", ...)
        }

    async def create_content(self, topic: str):
        """Multi-agent content creation pipeline"""
        # Research
        research = await Runner.run(
            self.agents["researcher"],
            f"Research content ideas for: {topic}"
        )

        # Write
        draft = await Runner.run(
            self.agents["writer"],
            f"Write content based on research:\n{research.final_output}"
        )

        # Edit
        edited = await Runner.run(
            self.agents["editor"],
            f"Edit and improve this content:\n{draft.final_output}"
        )

        # Optimize
        optimized = await Runner.run(
            self.agents["optimizer"],
            f"Optimize for SEO:\n{edited.final_output}"
        )

        return {
            "research": research.final_output,
            "draft": draft.final_output,
            "edited": edited.final_output,
            "optimized": optimized.final_output
        }
```

## Best Practices

### 1. Agent Specialization
- Each agent should have a clear, specific role
- Avoid overlap in agent responsibilities
- Match agent capabilities to task requirements

### 2. Error Recovery
- Implement fallback mechanisms
- Log errors for debugging
- Provide meaningful error messages

### 3. Resource Management
- Limit concurrent agent executions
- Implement rate limiting
- Monitor API usage and costs

### 4. Testing
- Test individual agents independently
- Test agent interactions
- Monitor performance and accuracy

### 5. Monitoring
- Track agent success rates
- Monitor response times
- Log interactions for analysis

See the `scripts/multi_agent_workflow.py` for complete working examples of these patterns.