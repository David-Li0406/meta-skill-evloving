---
name: swarm-orchestration
description: Use this skill to orchestrate multiple AI agents for complex tasks, enabling parallel execution and dynamic coordination across various topologies.
---

# Skill body

## Overview

This skill enables the orchestration of multi-agent swarms for complex workflows using advanced coordination systems. It supports various topologies, including mesh, hierarchical, and adaptive, allowing for intelligent task distribution and parallel execution.

## When to Use

- When scaling beyond single agents for complex workflows.
- For tasks requiring multiple specialized agents (e.g., coder, tester, reviewer).
- To implement parallel execution for independent subtasks.
- For dynamic task orchestration based on task complexity or agent capabilities.
- In scenarios requiring distributed information gathering or coordinated problem-solving.

## Prerequisites

- Agentic-flow or Claude Flow MCP server configured.
- Understanding of swarm topologies and distributed systems.
- Familiarity with agent types and capabilities.

## Quick Start

```bash
# Initialize a swarm for complex tasks
npx agentic-flow hooks swarm-init --topology hierarchical --max-agents 5

# Spawn specialized agents
npx agentic-flow hooks agent-spawn --type coder
npx agentic-flow hooks agent-spawn --type tester
npx agentic-flow hooks agent-spawn --type reviewer

# Orchestrate the task
npx agentic-flow hooks task-orchestrate --task "Build REST API with tests" --mode parallel
```

## Topology Patterns

### 1. Mesh (Peer-to-Peer)
```typescript
// Equal peers, distributed decision-making
await swarm.init({
  topology: 'mesh',
  agents: ['coder', 'tester', 'reviewer'],
  communication: 'broadcast'
});
```

### 2. Hierarchical (Queen-Worker)
```typescript
// Centralized coordination, specialized workers
await swarm.init({
  topology: 'hierarchical',
  queen: 'architect',
  workers: ['backend-dev', 'frontend-dev', 'db-designer']
});
```

### 3. Adaptive (Dynamic)
```typescript
// Automatically switches topology based on task
await swarm.init({
  topology: 'adaptive',
  optimization: 'task-complexity'
});
```

## Task Orchestration

### Parallel Execution
```typescript
// Execute tasks concurrently
const results = await swarm.execute({
  tasks: [
    { agent: 'coder', task: 'Implement API endpoints' },
    { agent: 'frontend', task: 'Build UI components' },
    { agent: 'tester', task: 'Write test suite' }
  ],
  mode: 'parallel',
  timeout: 300000 // 5 minutes
});
```

### Pipeline Execution
```typescript
// Sequential pipeline with dependencies
await swarm.pipeline([
  { stage: 'design', agent: 'architect' },
  { stage: 'implement', agent: 'coder', after: 'design' },
  { stage: 'test', agent: 'tester', after: 'implement' },
  { stage: 'review', agent: 'reviewer', after: 'test' }
]);
```