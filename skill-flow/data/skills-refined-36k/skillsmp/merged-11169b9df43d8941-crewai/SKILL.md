---
name: crewai
description: Use this skill when designing collaborative AI agent teams with CrewAI, focusing on roles, task definitions, and orchestration for complex workflows.
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

## Patterns

### Basic Crew with YAML Config

Define agents and tasks in YAML (recommended)

**When to use**: Any CrewAI project

```yaml
# config/agents.yaml
researcher:
  role: "Senior Research Analyst"
  goal: "Find comprehensive, accurate information on {topic}"
  backstory: |
    You are an expert researcher with years of experience
    in gathering and analyzing information. You're known
    for your thorough and accurate research.
  tools:
    - SerperDevTool
    - WebsiteSearchTool
  verbose: true

writer:
  role: "Content Writer"
  goal: "Create engaging, well-structured content"
  backstory: |
    You are a skilled writer who transforms research
    into compelling narratives. You focus on clarity
    and engagement.
  verbose: true

# config/tasks.yaml
research_task:
  description: |
    Research the topic: {topic}

    Focus on:
    1. Key facts and statistics
    2. Recent developments
    3. Expert opinions
    4. Contrarian viewpoints

    Be thorough and cite sources.
  agent: researcher
  expected_output: |
    A comprehensive research report with:
    - Executive summary
    - Key findings (bulleted)
    - Sources cited

writing_task:
  description: |
    Using the research provided, write an article about {topic}.

    Requirements:
    - 800-1000 words
    - Engaging introduction
    - Clear structure with headers
    - Actionable conclusion
  agent: writer
  expected_output: "A polished article ready for publication"
  context:
    - research_task  # Uses output from research
```

### Hierarchical Process

Manager agent delegates to workers

**When to use**: Complex tasks needing coordination

```python
from crewai import Crew, Process

# Define specialized agents
researcher = Agent(
    role="Research Specialist",
    goal="Find accurate information",
    backstory="Expert researcher..."
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and interpret data",
    backstory="Expert analyst..."
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging content",
    backstory="Expert writer..."
)

# Hierarchical crew - manager coordinates
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o"),  # Manager model
    verbose=True
)

result = crew.kickoff()
```

### Planning Feature

Generate execution plan before running

**When to use**: Complex workflows needing structure

```python
from crewai import Crew, Process

# Enable planning
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research, write, review],
    process=Process.sequential,
    planning=True,  # Enable planning
    planning_llm=ChatOpenAI(model="gpt-4o")  # Planner model
)

result = crew.kickoff()

# Access the plan
print(crew.plan)
```

## Anti-Patterns

### ❌ Vague Agent Roles

**Why bad**: Agent doesn't know its specialty. Overlapping responsibilities lead to poor task delegation.

**Instead**: Be specific:
- "Senior React Developer" not "Developer"
- "Financial Analyst specializing in crypto" not "Analyst"

### ❌ Missing Expected Outputs

**Why bad**: Agent doesn't know done criteria, leading to inconsistent outputs.

**Instead**: Always specify expected_output:
```yaml
expected_output: |
  A JSON object with:
  - summary: string (100 words max)
  - key_points: list of strings
  - confidence: float 0-1
```

### ❌ Too Many Agents

**Why bad**: Coordination overhead and inconsistent communication slow execution.

**Instead**: Limit to 3-5 agents with clear roles. One agent can handle multiple related tasks.

## Limitations

- Python-only
- Best for structured workflows
- Can be verbose for simple cases
- Flows are newer feature

## Related Skills

Works well with: `langgraph`, `autonomous-agents`, `langfuse`, `structured-output`