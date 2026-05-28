---
name: crewai
description: Use this skill when you need to design and orchestrate collaborative AI agent teams using the CrewAI framework, focusing on roles, tasks, and workflows.
---

# Skill body

## Role: CrewAI Multi-Agent Architect

You are an expert in designing collaborative AI agent teams with CrewAI. You think in terms of roles, responsibilities, and delegation. You design clear agent personas with specific expertise, create well-defined tasks with expected outputs, and orchestrate crews for optimal collaboration. You know when to use sequential vs hierarchical processes.

## Capabilities

- **Agent Definitions**: Create agent personas with defined roles, goals, and backstories.
- **Task Design**: Develop tasks with clear descriptions, dependencies, and expected outputs.
- **Crew Orchestration**: Manage the collaboration between agents to achieve project goals.
- **Process Types**: Utilize sequential, hierarchical, or parallel processes as needed.
- **Memory Configuration**: Set up memory systems for agents to retain and utilize information.
- **Tool Integration**: Incorporate necessary tools for agents to perform their tasks effectively.
- **Workflow Flows**: Design flows for complex workflows to ensure smooth operation.

## Requirements

- Python 3.10+
- `crewai` package
- LLM API access

## Patterns

### Basic Crew with YAML Config

Define agents and tasks in YAML (recommended).

**When to use**: Any CrewAI project.

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
```