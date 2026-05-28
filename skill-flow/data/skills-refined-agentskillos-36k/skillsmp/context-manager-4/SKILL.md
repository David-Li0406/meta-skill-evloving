---
name: context-manager
description: Context management specialist for multi-agent workflows and long-running tasks. Use PROACTIVELY for complex projects, session coordination, and when context preservation is needed across multiple agents. (project)
allowed-tools: Read, Write, Edit, TodoWrite, mcp__memory__create_entities, mcp__memory__add_observations, mcp__memory__search_nodes
---

# Context Manager Skill

Context management specialist for Faiston NEXO multi-agent workflows and long-running tasks.

## Faiston NEXO Architecture Context

| Layer | Components | Key Files |
|-------|------------|-----------|
| Frontend | React, TypeScript, TanStack Query | `client/` |
| Backend | FastAPI, Python, Mangum | `server/main.py` |
| AI Agents | Google ADK, Gemini 3.0 Pro | `server/agentcore/` |
| Infrastructure | Terraform, AWS Lambda, S3, DynamoDB | `terraform/` |
| CI/CD | GitHub Actions | `.github/workflows/` |

## Primary Functions

### Context Capture

1. Extract key decisions and rationale from agent outputs
2. Identify reusable patterns and solutions
3. Document integration points between components
4. Track unresolved issues and TODOs
5. **Faiston-specific**: Track AgentCore session IDs and Cognito auth state

### Context Distribution

1. Prepare minimal, relevant context for each agent
2. Create agent-specific briefings
3. Maintain a context index for quick retrieval
4. Prune outdated or irrelevant information

### Memory Management (MCP Memory)

Use MCP Memory tools to persist critical context:

```
mcp__memory__create_entities    → Store new decisions/patterns
mcp__memory__add_observations   → Add details to existing entities
mcp__memory__search_nodes       → Retrieve relevant context
```

## Faiston NEXO Context Templates

### Quick Context (< 500 tokens)

```markdown
## Current Task
[What we're working on]

## Recent Decisions
- [Decision 1 with rationale]
- [Decision 2 with rationale]

## Active Blockers
- [Blocker and owner]

## Key Files Modified
- `path/to/file.ts` - [change description]
```

### Full Context (< 2000 tokens)

```markdown
## Project State
- **Frontend**: [current status]
- **Backend**: [current status]
- **AgentCore**: [current status]
- **Infrastructure**: [current status]

## Architecture Decisions
| Decision | Rationale | Date |
|----------|-----------|------|
| Use Gemini 3.0 Pro | Claude was collapsing structures | 2025-12 |
| S3 regional endpoint | Fix 307 CORS redirect | 2025-12 |

## Integration Points
- Frontend → AgentCore: Cognito JWT + `agentcore.ts`
- AgentCore → Gemini: Google ADK Agent class
- Backend → S3: Presigned URLs with s3v4

## Active Work Streams
1. [Stream 1]
2. [Stream 2]
```

### AgentCore Session Context

```markdown
## AgentCore State
- **Runtime**: faiston_nexo_agents-WNYXe1CyLz
- **Memory ID**: faiston_nexo_agents_mem-2LaTp8COvj
- **Auth**: Cognito JWT (pool: us-east-2_6Vzhr0J6M)

## Active Agents
| Agent | Last Invoked | Status |
|-------|--------------|--------|
| NEXOAgent | [time] | [status] |
| FlashcardsAgent | [time] | [status] |
```

## Workflow Integration

When activated:

1. **Review** current conversation and agent outputs
2. **Extract** important context using templates above
3. **Store** in MCP Memory if critical decision
4. **Create** summary for next agent/session
5. **Update** `docs/KNOWN_ISSUES.md` if bugs found
6. **Suggest** context compression when needed

## Cross-Skill Context Handoff

| From Skill | To Skill | Context Needed |
|------------|----------|----------------|
| bug-detective | test-engineer | Error reproduction steps |
| ai-engineer | frontend-builder | New agent actions/responses |
| backend-architect | prompt-engineer | API contract changes |
| workflow-architect | context-manager | Task decomposition |

## Memory Entities to Track

```
Entity: FaistonNEXO_Decision
Type: architectural_decision
Observations:
  - "2025-12: Migrated to Gemini 3.0 Pro for better structure"
  - "2025-12: S3 presigned URLs use regional endpoint"

Entity: FaistonNEXO_KnownIssue
Type: bug
Observations:
  - "S3 307 redirect: Use s3v4 signature with virtual addressing"
  - "Session ID must be >= 33 characters"
```

Always optimize for relevance over completeness. Good context accelerates work; bad context creates confusion.
