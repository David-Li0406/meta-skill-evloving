# Multi-Agent Setup

SharedMemoryPool setup and agent coordination infrastructure.

## Basic Multi-Agent Pattern

```python
from kaizen.memory.shared_memory import SharedMemoryPool
from kaizen.core.base_agent import BaseAgent

# Create shared memory pool
shared_pool = SharedMemoryPool()

# Create coordinated agents
researcher = ResearcherAgent(config, shared_pool, agent_id="researcher")
analyst = AnalystAgent(config, shared_pool, agent_id="analyst")
writer = WriterAgent(config, shared_pool, agent_id="writer")

# Agents share insights
findings = researcher.research("AI trends 2025")
analysis = analyst.analyze(findings)
report = writer.write(analysis)
```

## SharedMemoryPool

Enables agents to share insights and coordinate.

**Features:**
- Write insights with tags
- Read relevant insights with filtering
- Exclude own insights
- Importance-based retrieval

## References
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 94-113
