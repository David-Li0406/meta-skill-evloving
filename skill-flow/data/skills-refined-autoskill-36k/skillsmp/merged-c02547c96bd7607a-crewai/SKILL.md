---
name: crewai
description: Use this skill to build and orchestrate multi-agent AI systems with CrewAI, focusing on agent design, task definition, and collaborative workflows.
---

# CrewAI

**Role**: CrewAI Multi-Agent Architect

You are an expert in designing collaborative AI agent teams with CrewAI. You think in terms of roles, responsibilities, and delegation. You design clear agent personas with specific expertise, create well-defined tasks with expected outputs, and orchestrate crews for optimal collaboration. You know when to use sequential vs hierarchical processes.

## Capabilities

- Agent definitions (role, goal, backstory)
- Task design and dependencies
- Crew orchestration
- Process types (sequential, hierarchical, parallel)
- Memory configuration
- Tool integration
- Flows for complex workflows

## Requirements

- Python 3.10+
- crewai package
- LLM API access

## Installation

```bash
pip install crewai crewai-tools
```

## Basic Concepts

### Agents

Define agents with specific roles and goals.

```python
from crewai import Agent, LLM

# Define LLM
llm = LLM(model="openai/gpt-4o", temperature=0.7)

# Create agent
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and data science",
    backstory="You work at a leading tech think tank. Your expertise lies in identifying emerging trends and technologies.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writer = Agent(
    role="Tech Content Writer",
    goal="Write compelling content about AI advancements",
    backstory="You are a renowned content writer specializing in technology and AI.",
    verbose=True,
    allow_delegation=True,
    llm=llm
)
```

### Tasks

Define tasks with clear descriptions and expected outputs.

```python
from crewai import Task

research_task = Task(
    description="Conduct comprehensive research on the latest developments in AI agents technology.",
    expected_output="A detailed 3-paragraph report covering key trends and technologies.",
    agent=researcher
)

write_task = Task(
    description="Using the research findings, write a blog post about AI agents.",
    expected_output="A 4-paragraph blog post in markdown format.",
    agent=writer,
    context=[research_task]  # Depends on research task
)
```

### Crew

Orchestrate agents and tasks into a crew.

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # or Process.hierarchical
    verbose=True
)

# Run the crew
result = crew.kickoff()
print(result)
```

## Advanced Patterns

### Hierarchical Process

Use a manager agent to delegate tasks among workers.

```python
manager = Agent(
    role="Project Manager",
    goal="Coordinate the team to deliver high-quality results.",
    backstory="Experienced manager who ensures efficient collaboration.",
    allow_delegation=True
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.hierarchical,
    manager_agent=manager,
    verbose=True
)
```

### Memory

Enable memory for agents to retain information across tasks.

```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    memory=True,  # Enable memory
    embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}}
)
```

## Anti-Patterns

### ❌ Vague Agent Roles

**Why bad**: Agents lack clarity on their specialties, leading to poor task delegation.

**Instead**: Be specific in defining roles.

### ❌ Missing Expected Outputs

**Why bad**: Agents do not know the criteria for completion, resulting in inconsistent outputs.

**Instead**: Always specify expected outputs clearly.

### ❌ Too Many Agents

**Why bad**: Coordination overhead can slow down execution.

**Instead**: Limit the number of agents to 3-5 with clear roles.

## Limitations

- Python-only
- Best for structured workflows
- Can be verbose for simple cases

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI Tools](https://github.com/crewAIInc/crewAI-tools)