---
name: swe-swarm-analyze
version: 1.0.0
description: DAA-powered codebase analysis using swarm agents. Use for deep analysis of large codebases.
workflow:
  aware: true
  callable_from:
    - WF_ONBOARD
    - WF_RESEARCH
    - WF_SWARM_ORCHESTRATE
  default_return: WF_DETECT_REQ
  supports_standalone: true
  auto_transition: false
allowed-tools: Read, Grep, Glob, mcp__ruv-swarm__*, mcp__claude-flow__*
---

# Swarm Analyze Skill

Deep codebase analysis using Decentralized Autonomous Agents (DAA).

## When to Use

- Large codebases (1000+ files)
- Complex multi-module projects
- When detailed DOM_* and SYS_* memories are needed
- Feature onboarding with full analysis mode

## MCP Requirements

**Required (one of):**
- `ruv-swarm` MCP (preferred for DAA learning)
- `claude-flow` MCP (alternative)

**Fallback:** Sequential analysis if no swarm MCP available

## Agent Types

| Agent ID | Purpose | Cognitive Pattern |
|----------|---------|-------------------|
| config-analyzer | Parse config files | convergent |
| architecture-mapper | Detect layers | systems |
| pattern-detector | Find conventions | lateral |
| domain-extractor | Extract domains | divergent |
| system-finder | Identify systems | systems |
| test-analyzer | Test patterns | critical |
| import-tracer | Dependency graph | convergent |
| convention-learner | Style detection | adaptive |
| file-indexer | File inventory | convergent |
| synthesizer | Compile results | systems |

## Process

### Step 1: Initialize Swarm

```javascript
// Prefer RUV-Swarm for DAA learning
if (mcp_available("ruv-swarm")) {
  mcp__ruv-swarm__daa_init({
    enableLearning: true,
    enableCoordination: true,
    persistenceMode: "auto"
  });
} else if (mcp_available("claude-flow")) {
  mcp__claude-flow__swarm_init({
    topology: "mesh",
    maxAgents: 10
  });
}
```

### Step 2: Spawn Analysis Agents

**CRITICAL: Spawn ALL agents in ONE message for parallelism**

```javascript
// RUV-Swarm DAA agents
const agents = [
  { id: "config-analyzer", cognitivePattern: "convergent" },
  { id: "architecture-mapper", cognitivePattern: "systems" },
  { id: "pattern-detector", cognitivePattern: "lateral" },
  { id: "domain-extractor", cognitivePattern: "divergent" },
  { id: "system-finder", cognitivePattern: "systems" },
  { id: "test-analyzer", cognitivePattern: "critical" },
  { id: "import-tracer", cognitivePattern: "convergent" },
  { id: "convention-learner", cognitivePattern: "adaptive" },
  { id: "file-indexer", cognitivePattern: "convergent" },
  { id: "synthesizer", cognitivePattern: "systems" }
];

// Spawn all in parallel
agents.forEach(a => mcp__ruv-swarm__daa_agent_create({
  id: a.id,
  cognitivePattern: a.cognitivePattern,
  enableMemory: true,
  learningRate: 0.8
}));
```

### Step 3: Orchestrate Analysis

```javascript
mcp__ruv-swarm__task_orchestrate({
  task: "Analyze codebase structure, patterns, domains, and systems",
  strategy: "parallel",
  maxAgents: 10,
  priority: "high"
});
```

### Step 4: Collect Results

Each agent produces structured findings:
- **config-analyzer**: package.json, framework configs
- **architecture-mapper**: layers, directories, data flow
- **pattern-detector**: naming conventions, import patterns
- **domain-extractor**: business domains, entities
- **system-finder**: external integrations, APIs
- **test-analyzer**: test framework, coverage patterns
- **import-tracer**: dependency graph
- **convention-learner**: code style, formatting
- **file-indexer**: file inventory by type
- **synthesizer**: combined analysis

### Step 5: Generate Memories

Based on synthesized results, create:

1. **FEATURE_[KEY]** - Main feature memory
2. **DOM_[KEY]_[domain]** - For each detected domain
3. **SYS_[KEY]_[system]** - For each detected system
4. **Update INDEX_FEATURES** - Add feature entry
5. **Update ARCH_INDEX** - Add architecture details

### Step 6: DAA Learning

Record analysis success for future improvement:

```javascript
mcp__ruv-swarm__daa_agent_adapt({
  agentId: "synthesizer",
  performanceScore: 0.9,
  feedback: "Analysis complete"
});

mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "synthesizer",
  targetAgentIds: ["config-analyzer", "architecture-mapper"],
  knowledgeDomain: "codebase-patterns"
});
```

## Output Format

**SWARM ANALYSIS COMPLETE**

| Metric | Value |
|--------|-------|
| Agents Used | 10 |
| Analysis Time | [duration] |

**Detected:**
- Language: [primary]
- Framework: [name]
- Layers: [count]
- Domains: [count]
- Systems: [count]

**Memories Created:**
- FEATURE_[KEY]
- DOM_[KEY]_[domain1]
- DOM_[KEY]_[domain2]
- SYS_[KEY]_[system1]
- INDEX_FEATURES (updated)
- ARCH_INDEX (updated)

**DAA Learning:**
- Patterns stored: [count]
- Confidence: [score]

## Skill Return Format

```markdown
## Skill Return
- **Skill**: swe-swarm-analyze
- **Status**: [success|success_with_findings|blocked]
- **Agents Used**: [count]
- **Memories Created**: [list]
- **Domains Found**: [count]
- **Systems Found**: [count]
- **Next Step Hint**: WF_DETECT_REQ
```

## Fallback: Sequential Analysis

If no swarm MCP available:

```
⚠️ No swarm MCP detected. Running sequential analysis.

This will take longer but produce similar results.

Progress:
[1/10] Analyzing config files...
[2/10] Mapping architecture...
...
```

## Exit

`> **Skill /swe-swarm-analyze complete** - [count] memories created via DAA analysis`
