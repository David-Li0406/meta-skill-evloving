---
id: multi-agent-systems
name: "Multi-Agent Systems"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Multi-Agent Systems

## Overview

Multi-agent systems coordinate multiple specialized AI agents to solve complex problems collaboratively. By dividing tasks among experts and enabling communication, these systems can tackle challenges beyond single-agent capabilities.

## When to Use

- Complex tasks requiring diverse expertise
- Problems with natural role divisions
- Debate and verification scenarios
- Creative collaboration
- Simulation and role-playing
- When single agents struggle with scope

## Key Concepts

### Coordination Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Sequential | Agents work in order | Pipelines, workflows |
| Parallel | Agents work simultaneously | Independent subtasks |
| Hierarchical | Manager delegates to workers | Complex projects |
| Debate | Agents argue positions | Verification, decisions |
| Collaborative | Agents work together | Creative tasks |

### Multi-Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│  - Task distribution                                         │
│  - Communication routing                                     │
│  - Conflict resolution                                       │
└─────────────────────────────────────────────────────────────┘
            │                    │                    │
    ┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
    │   AGENT A     │   │   AGENT B     │   │   AGENT C     │
    │  (Researcher) │   │  (Developer)  │   │  (Reviewer)   │
    └───────────────┘   └───────────────┘   └───────────────┘
```

## Implementation

### Basic Multi-Agent Framework

```python
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional, Any
from enum import Enum
from openai import OpenAI
import json

client = OpenAI()

@dataclass
class AgentConfig:
    name: str
    role: str
    system_prompt: str
    model: str = "gpt-4o"
    tools: List[Dict] = None

class Agent:
    """Individual agent in a multi-agent system."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.messages: List[Dict] = []
        self.reset()

    def reset(self):
        """Reset agent state."""
        self.messages = [
            {"role": "system", "content": self.config.system_prompt}
        ]

    def respond(self, message: str, context: Dict = None) -> str:
        """Generate a response to a message."""
        user_content = message
        if context:
            user_content = f"Context: {json.dumps(context)}\n\n{message}"

        self.messages.append({"role": "user", "content": user_content})

        response = client.chat.completions.create(
            model=self.config.model,
            messages=self.messages,
            tools=self.config.tools
        )

        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

class MultiAgentOrchestrator:
    """Orchestrates communication between agents."""

    def __init__(self, agents: List[Agent]):
        self.agents = {a.config.name: a for a in agents}
        self.conversation_history: List[Dict] = []

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        context: Dict = None
    ) -> str:
        """Send message from one agent to another."""
        if to_agent not in self.agents:
            raise ValueError(f"Unknown agent: {to_agent}")

        prefixed_message = f"[From {from_agent}]: {message}"

        response = self.agents[to_agent].respond(prefixed_message, context)

        self.conversation_history.append({
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "response": response
        })

        return response

    def broadcast(self, message: str, exclude: List[str] = None) -> Dict[str, str]:
        """Broadcast message to all agents."""
        exclude = exclude or []
        responses = {}

        for name, agent in self.agents.items():
            if name not in exclude:
                responses[name] = agent.respond(message)

        return responses

    def get_summary(self) -> str:
        """Get summary of conversation."""
        summary = "Conversation Summary:\n"
        for entry in self.conversation_history:
            summary += f"\n{entry['from']} -> {entry['to']}:\n"
            summary += f"  Message: {entry['message'][:100]}...\n"
            summary += f"  Response: {entry['response'][:100]}...\n"
        return summary
```

### Sequential Pipeline

```python
class SequentialPipeline:
    """Agents process tasks in sequence."""

    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, initial_input: str) -> Dict:
        """Run the pipeline."""
        current_output = initial_input
        results = []

        for agent in self.agents:
            response = agent.respond(current_output)
            results.append({
                "agent": agent.config.name,
                "input": current_output[:200],
                "output": response
            })
            current_output = response

        return {
            "final_output": current_output,
            "pipeline_results": results
        }

# Example: Research -> Write -> Edit pipeline
researcher = Agent(AgentConfig(
    name="Researcher",
    role="Research Specialist",
    system_prompt="You are a research specialist. Gather and summarize relevant information."
))

writer = Agent(AgentConfig(
    name="Writer",
    role="Content Writer",
    system_prompt="You are a content writer. Create engaging content from research findings."
))

editor = Agent(AgentConfig(
    name="Editor",
    role="Editor",
    system_prompt="You are an editor. Improve clarity, fix errors, and polish the content."
))

pipeline = SequentialPipeline([researcher, writer, editor])
result = pipeline.run("Write an article about AI agents")
```

### Hierarchical Manager-Worker

```python
class ManagerAgent(Agent):
    """Manager that delegates tasks to workers."""

    def __init__(self, config: AgentConfig, workers: List[Agent]):
        super().__init__(config)
        self.workers = {w.config.name: w for w in workers}

    def delegate(self, task: str) -> str:
        """Decompose task and delegate to workers."""
        # Ask manager to create plan
        plan_prompt = f"""Task: {task}

Available workers:
{chr(10).join([f"- {w.config.name}: {w.config.role}" for w in self.workers.values()])}

Create a plan assigning subtasks to workers.
Return JSON: {{"assignments": [{{"worker": "name", "subtask": "description"}}]}}"""

        response = self.respond(plan_prompt)

        try:
            plan = json.loads(response)
            assignments = plan.get("assignments", [])
        except json.JSONDecodeError:
            return f"Failed to parse plan: {response}"

        # Execute assignments
        results = []
        for assignment in assignments:
            worker_name = assignment["worker"]
            subtask = assignment["subtask"]

            if worker_name in self.workers:
                worker_result = self.workers[worker_name].respond(subtask)
                results.append({
                    "worker": worker_name,
                    "task": subtask,
                    "result": worker_result
                })

        # Have manager synthesize results
        synthesis_prompt = f"""Original task: {task}

Worker results:
{json.dumps(results, indent=2)}

Synthesize these results into a final response."""

        return self.respond(synthesis_prompt)

# Example
manager = ManagerAgent(
    config=AgentConfig(
        name="ProjectManager",
        role="Project Manager",
        system_prompt="You are a project manager. Decompose tasks and coordinate workers."
    ),
    workers=[
        Agent(AgentConfig(
            name="Developer",
            role="Software Developer",
            system_prompt="You are a developer. Write and review code."
        )),
        Agent(AgentConfig(
            name="Designer",
            role="UI Designer",
            system_prompt="You are a UI designer. Create user interface designs."
        )),
        Agent(AgentConfig(
            name="Tester",
            role="QA Tester",
            system_prompt="You are a QA tester. Create test cases and find bugs."
        ))
    ]
)

result = manager.delegate("Build a simple todo app with tests")
```

### Debate System

```python
class DebateSystem:
    """Two agents debate a topic to reach better conclusions."""

    def __init__(
        self,
        proponent: Agent,
        opponent: Agent,
        judge: Agent,
        max_rounds: int = 3
    ):
        self.proponent = proponent
        self.opponent = opponent
        self.judge = judge
        self.max_rounds = max_rounds

    def debate(self, topic: str) -> Dict:
        """Run a debate on the topic."""
        debate_history = []

        # Initial positions
        pro_position = self.proponent.respond(
            f"Argue IN FAVOR of: {topic}\nProvide your strongest arguments."
        )
        con_position = self.opponent.respond(
            f"Argue AGAINST: {topic}\nProvide your strongest arguments."
        )

        debate_history.append({
            "round": 0,
            "proponent": pro_position,
            "opponent": con_position
        })

        # Debate rounds
        for round_num in range(1, self.max_rounds + 1):
            # Opponent responds to proponent
            con_response = self.opponent.respond(
                f"Counter the following argument:\n{pro_position}"
            )

            # Proponent responds to opponent
            pro_response = self.proponent.respond(
                f"Defend against and counter:\n{con_response}"
            )

            debate_history.append({
                "round": round_num,
                "proponent": pro_response,
                "opponent": con_response
            })

            pro_position = pro_response

        # Judge evaluates
        debate_summary = json.dumps(debate_history, indent=2)
        judgment = self.judge.respond(
            f"""Evaluate this debate and determine the stronger position.

Topic: {topic}

Debate:
{debate_summary}

Provide:
1. Summary of key arguments
2. Strengths and weaknesses of each side
3. Your judgment on which side argued more effectively
4. A synthesized conclusion incorporating the best points"""
        )

        return {
            "topic": topic,
            "debate_history": debate_history,
            "judgment": judgment
        }

# Example
debate = DebateSystem(
    proponent=Agent(AgentConfig(
        name="Proponent",
        role="Advocate",
        system_prompt="You are a skilled debater arguing in favor of positions. Be persuasive and logical."
    )),
    opponent=Agent(AgentConfig(
        name="Opponent",
        role="Critic",
        system_prompt="You are a skilled debater arguing against positions. Find weaknesses and counter-arguments."
    )),
    judge=Agent(AgentConfig(
        name="Judge",
        role="Impartial Judge",
        system_prompt="You are an impartial judge. Evaluate arguments fairly and provide balanced conclusions."
    ))
)

result = debate.debate("AI will create more jobs than it eliminates")
```

### Collaborative Agents

```python
class CollaborativeGroup:
    """Agents collaborate on a shared task."""

    def __init__(
        self,
        agents: List[Agent],
        coordinator_model: str = "gpt-4o"
    ):
        self.agents = {a.config.name: a for a in agents}
        self.coordinator_model = coordinator_model
        self.shared_workspace: Dict = {"notes": [], "artifacts": []}

    def collaborate(self, task: str, max_iterations: int = 5) -> Dict:
        """Run collaborative session."""
        # Initial brainstorm
        ideas = {}
        for name, agent in self.agents.items():
            idea = agent.respond(
                f"Task: {task}\n\nProvide your initial thoughts and approach."
            )
            ideas[name] = idea
            self.shared_workspace["notes"].append({
                "agent": name,
                "type": "initial_idea",
                "content": idea
            })

        # Collaborative refinement
        for iteration in range(max_iterations):
            # Each agent reviews and builds on others' work
            for name, agent in self.agents.items():
                other_ideas = {k: v for k, v in ideas.items() if k != name}

                prompt = f"""Task: {task}

Your previous idea: {ideas[name]}

Other team members' ideas:
{json.dumps(other_ideas, indent=2)}

Build on these ideas. What can you add or improve?
Collaborate by incorporating good points from others."""

                contribution = agent.respond(prompt)
                ideas[name] = contribution

                self.shared_workspace["notes"].append({
                    "agent": name,
                    "type": f"iteration_{iteration + 1}",
                    "content": contribution
                })

        # Final synthesis
        synthesis_prompt = f"""Task: {task}

Team contributions:
{json.dumps(ideas, indent=2)}

Create a final synthesized solution incorporating the best elements from all team members."""

        final_result = client.chat.completions.create(
            model=self.coordinator_model,
            messages=[{"role": "user", "content": synthesis_prompt}]
        ).choices[0].message.content

        return {
            "task": task,
            "individual_contributions": ideas,
            "workspace": self.shared_workspace,
            "final_result": final_result
        }
```

### AutoGen-Style Conversation

```python
class ConversationalAgents:
    """Agents that can freely converse to solve problems."""

    def __init__(
        self,
        agents: List[Agent],
        max_turns: int = 10,
        termination_phrase: str = "TASK_COMPLETE"
    ):
        self.agents = agents
        self.max_turns = max_turns
        self.termination_phrase = termination_phrase

    def chat(self, initial_message: str) -> Dict:
        """Run a free-form conversation."""
        conversation = []
        current_speaker_idx = 0
        last_message = initial_message

        for turn in range(self.max_turns):
            speaker = self.agents[current_speaker_idx]
            next_speaker_idx = (current_speaker_idx + 1) % len(self.agents)
            listener = self.agents[next_speaker_idx]

            # Build context
            recent_context = conversation[-3:] if conversation else []
            context_str = "\n".join([
                f"[{c['speaker']}]: {c['message']}"
                for c in recent_context
            ])

            prompt = f"""Conversation so far:
{context_str}

[{self.agents[next_speaker_idx].config.name}]: {last_message}

Respond to continue the conversation. If the task is complete, include '{self.termination_phrase}' in your response."""

            response = speaker.respond(prompt)

            conversation.append({
                "turn": turn,
                "speaker": speaker.config.name,
                "message": response
            })

            # Check termination
            if self.termination_phrase in response:
                return {
                    "status": "completed",
                    "conversation": conversation,
                    "turns": turn + 1
                }

            last_message = response
            current_speaker_idx = next_speaker_idx

        return {
            "status": "max_turns_reached",
            "conversation": conversation,
            "turns": self.max_turns
        }
```

### Production Multi-Agent System

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
import logging
import asyncio

class CommunicationType(Enum):
    DIRECT = "direct"
    BROADCAST = "broadcast"
    REQUEST = "request"

@dataclass
class Message:
    sender: str
    receiver: str
    content: str
    msg_type: CommunicationType
    metadata: Dict = None

class MessageBus:
    """Central message bus for agent communication."""

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Message] = []

    def subscribe(self, agent_name: str, handler: Callable):
        """Subscribe agent to messages."""
        if agent_name not in self.subscribers:
            self.subscribers[agent_name] = []
        self.subscribers[agent_name].append(handler)

    async def send(self, message: Message):
        """Send message to recipient(s)."""
        self.message_history.append(message)

        if message.msg_type == CommunicationType.BROADCAST:
            # Send to all except sender
            for agent_name, handlers in self.subscribers.items():
                if agent_name != message.sender:
                    for handler in handlers:
                        await handler(message)
        else:
            # Send to specific receiver
            if message.receiver in self.subscribers:
                for handler in self.subscribers[message.receiver]:
                    await handler(message)

class ProductionMultiAgentSystem:
    """Production-ready multi-agent system."""

    def __init__(
        self,
        agents: List[Agent],
        orchestration_model: str = "gpt-4o"
    ):
        self.agents = {a.config.name: a for a in agents}
        self.orchestration_model = orchestration_model
        self.message_bus = MessageBus()
        self.logger = logging.getLogger(__name__)

        # Setup message handlers
        for name, agent in self.agents.items():
            self.message_bus.subscribe(
                name,
                self._create_handler(agent)
            )

    def _create_handler(self, agent: Agent):
        """Create message handler for agent."""
        async def handler(message: Message):
            response = agent.respond(message.content)
            self.logger.info(f"{agent.config.name} responded to {message.sender}")
            return response
        return handler

    async def run_task(self, task: str, strategy: str = "hierarchical") -> Dict:
        """Run a task with specified coordination strategy."""
        if strategy == "hierarchical":
            return await self._hierarchical_execution(task)
        elif strategy == "parallel":
            return await self._parallel_execution(task)
        elif strategy == "sequential":
            return await self._sequential_execution(task)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    async def _hierarchical_execution(self, task: str) -> Dict:
        """Execute with hierarchical coordination."""
        # Orchestrator creates plan
        plan = await self._create_plan(task)

        results = []
        for assignment in plan.get("assignments", []):
            agent_name = assignment["agent"]
            subtask = assignment["task"]

            if agent_name in self.agents:
                result = self.agents[agent_name].respond(subtask)
                results.append({
                    "agent": agent_name,
                    "task": subtask,
                    "result": result
                })

        # Synthesize
        return await self._synthesize_results(task, results)

    async def _parallel_execution(self, task: str) -> Dict:
        """Execute subtasks in parallel."""
        plan = await self._create_plan(task)

        # Execute in parallel
        async def execute_assignment(assignment):
            agent_name = assignment["agent"]
            subtask = assignment["task"]
            if agent_name in self.agents:
                return {
                    "agent": agent_name,
                    "result": self.agents[agent_name].respond(subtask)
                }
            return None

        tasks = [execute_assignment(a) for a in plan.get("assignments", [])]
        results = await asyncio.gather(*tasks)
        results = [r for r in results if r]

        return await self._synthesize_results(task, results)

    async def _sequential_execution(self, task: str) -> Dict:
        """Execute agents in sequence."""
        current_output = task
        results = []

        for name, agent in self.agents.items():
            result = agent.respond(current_output)
            results.append({"agent": name, "result": result})
            current_output = result

        return {"results": results, "final": current_output}

    async def _create_plan(self, task: str) -> Dict:
        """Create execution plan."""
        agents_info = "\n".join([
            f"- {name}: {agent.config.role}"
            for name, agent in self.agents.items()
        ])

        prompt = f"""Task: {task}

Available agents:
{agents_info}

Create a plan with task assignments.
Return JSON: {{"assignments": [{{"agent": "name", "task": "description"}}]}}"""

        response = client.chat.completions.create(
            model=self.orchestration_model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    async def _synthesize_results(self, task: str, results: List[Dict]) -> Dict:
        """Synthesize results from multiple agents."""
        prompt = f"""Task: {task}

Agent results:
{json.dumps(results, indent=2)}

Synthesize into a coherent final result."""

        response = client.chat.completions.create(
            model=self.orchestration_model,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "individual_results": results,
            "synthesis": response.choices[0].message.content
        }
```

## Best Practices

1. **Agent Specialization**
   - Clear, focused roles
   - Non-overlapping responsibilities
   - Appropriate expertise levels

2. **Communication Design**
   - Clear message protocols
   - Structured information exchange
   - Conflict resolution mechanisms

3. **Coordination**
   - Choose appropriate pattern for task
   - Minimize unnecessary communication
   - Handle failures gracefully

4. **Monitoring**
   - Log all inter-agent messages
   - Track individual agent performance
   - Monitor for deadlocks

5. **Testing**
   - Test agents individually
   - Test coordination logic
   - Simulate edge cases

## Common Pitfalls

1. **Role Confusion** - Overlapping agent responsibilities
2. **Communication Overhead** - Too much back-and-forth
3. **Deadlocks** - Agents waiting on each other
4. **Echo Chambers** - Agents reinforcing mistakes
5. **Coordination Failure** - No clear decision making
6. **Resource Waste** - Redundant agent work

## References

- [AutoGen](https://microsoft.github.io/autogen/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [MetaGPT](https://github.com/geekan/MetaGPT)
- [Multi-Agent Survey](https://arxiv.org/abs/2308.08155)
