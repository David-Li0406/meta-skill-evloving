---
name: parallel-agents
description: Use this skill when multiple independent tasks can run with different domain expertise or when comprehensive analysis requires multiple perspectives.
---

# Skill body

## Overview

This skill enables coordinating multiple specialized agents through a built-in agent system. Unlike external scripts, this approach keeps all orchestration within the control of the platform.

## When to Use Orchestration

✅ **Good for:**
- Complex tasks requiring multiple expertise domains
- Code analysis from security, performance, and quality perspectives
- Comprehensive reviews (architecture + security + testing)
- Feature implementation needing backend + frontend + database work

❌ **Not for:**
- Simple, single-domain tasks
- Quick fixes or small changes
- Tasks where one agent suffices

## Native Agent Invocation

### Single Agent
```
Use the security-auditor agent to review authentication.
```

### Sequential Chain
```
First, use the explorer-agent to discover project structure.
Then, use the backend-specialist to review API endpoints.
Finally, use the test-engineer to identify test gaps.
```

### With Context Passing
```
Use the frontend-specialist to analyze React components.
Based on those findings, have the test-engineer generate component tests.
```

### Resume Previous Work
```
Resume agent [agentId] and continue with additional requirements.
```

## Orchestration Patterns

### Pattern 1: Comprehensive Analysis
```
Agents: explorer-agent → [domain-agents] → synthesis

1. explorer-agent: Map codebase structure.
2. security-auditor: Security posture.
3. backend-specialist: API quality.
4. frontend-specialist: UI/UX patterns.
5. test-engineer: Test coverage.
6. Synthesize all findings.
```

### Pattern 2: Feature Review
```
Agents: affected-domain-agents → test-engineer

1. Identify affected domains (backend? frontend? both?).
2. Invoke relevant domain agents.
3. test-engineer verifies changes.
4. Synthesize recommendations.
```

### Pattern 3: Security Audit
```
Agents: security-auditor → penetration-tester → synthesis

1. security-auditor: Configuration and code review.
2. penetration-tester: Active vulnerability testing.
3. Synthesize with prioritized remediation.
```

## Available Agents

| Agent                   | Expertise        | Trigger Phrases                                    |
|------------------------|------------------|----------------------------------------------------|
| `orchestrator`         | Coordination      |                                                    |
| `security-auditor`     | Security          |                                                    |
| `backend-specialist`    | Backend Development|                                                   |
| `frontend-specialist`   | Frontend Development|                                                  |
| `test-engineer`        | Testing           |                                                    |
| `explorer-agent`       | Code Exploration   |                                                    |
| `penetration-tester`   | Security Testing   |                                                    |
```