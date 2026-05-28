# CrewAI

**Category**: ai-ml/agents
**Description**: CrewAI multi-agent orchestration framework - role-based AI agent teams

## Package Detection

### PYPI
- `crewai`
- `crewai-tools`

### NPM
- `crewai` (if available)

## Agent Pattern Detection

### Python Patterns
File extensions: .py

**Pattern**: `from crewai import|import crewai`
- CrewAI imports
- Example: `from crewai import Agent, Task, Crew`

**Pattern**: `Agent\(\s*role=`
- Agent definition with role
- Example: `Agent(role="Researcher", goal="...", backstory="...")`

**Pattern**: `Task\(\s*description=`
- Task definitions
- Example: `Task(description="Research topic X", agent=researcher)`

**Pattern**: `Crew\(\s*agents=`
- Crew assembly
- Example: `Crew(agents=[agent1, agent2], tasks=[task1, task2])`

**Pattern**: `\.kickoff\(`
- Crew execution
- Example: `result = crew.kickoff()`

### Advanced Patterns

**Pattern**: `Process\.(sequential|hierarchical)`
- Process type specification
- Example: `Crew(..., process=Process.hierarchical)`

**Pattern**: `@tool|Tool\(\s*name=`
- Custom tool definitions
- Example: `@tool\ndef search_tool(query: str):`

**Pattern**: `manager_llm=|manager_agent=`
- Hierarchical crew management
- Example: `Crew(..., manager_llm=ChatOpenAI())`

## Agent Role Patterns

Common role patterns indicate usage type:
- **"Researcher"**: Information gathering agents
- **"Writer"**: Content creation agents
- **"Analyst"**: Data analysis agents
- **"Developer"**: Code generation agents
- **"Reviewer"**: Quality assurance agents

## Usage Classification

### Crew Types
- **Sequential Crew**: Tasks executed in order
- **Hierarchical Crew**: Manager agent delegates to workers
- **Parallel Crew**: Tasks executed concurrently

### Integration Indicators
- LLM provider (OpenAI, Anthropic, etc.)
- External tool integrations
- Memory/persistence usage

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Agent Pattern Detection**: 90% (HIGH)
- **Crew Structure Detection**: 85% (HIGH)
- **Role Analysis**: 75% (MEDIUM)

## Security Considerations

- Multi-agent systems can have complex permission models
- Agent delegation may bypass access controls
- Tool access should be reviewed per-agent
- Output validation critical for downstream actions
