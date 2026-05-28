# Agents Reference - JikiME-ADK Agent Catalog

Purpose: Complete reference catalog of JikiME-ADK's 26 specialized agents with `{domain}-{role}` naming convention and 7-tier hierarchy.

Last Updated: 2025-11-25
Version: 2.0.0

---

## Quick Reference (30 seconds)

The orchestrator delegates ALL tasks to specialized agents. 26 agents organized in 7 tiers:

Tier 1: `manager-*` (Command Processors) - Always Active
Tier 2: `manager-*` (Orchestration & Quality) - Auto-triggered
Tier 3: `{specialist}` (Domain Experts) - Lazy-loaded
Tier 4: `mcp-*` (MCP Integrators) - Resume-enabled
Tier 5: `*-builder` (Builder Agents) - Meta-development
Tier 6: `support-*` (Support Services) - On-demand
Tier 7: `ai-*` (AI & Specialized) - Specialized tasks

Agent Selection:
- Simple (1 file): 1-2 agents sequential
- Medium (3-5 files): 2-3 agents sequential
- Complex (10+ files): 5+ agents parallel/sequential

All agents use Task() delegation:
```python
result = Task(subagent_type="backend", prompt="...", context={...})
```

---

## Implementation Guide (5 minutes)

### Naming Convention: `{domain}-{role}`

All JikiME-ADK agents follow consistent naming:

| Domain | Purpose | Examples |
|--------|---------|----------|
| `manager-*` | Core workflow command processors & orchestration | manager-spec, manager-ddd, manager-quality |
| (no prefix) | Domain implementation experts | backend, frontend, architect, devops |
| (no prefix) | Security experts | security-auditor |
| `*-builder` | Meta-generation agents | agent-builder, skill-builder |

---

### Tier 1: Command Processors (Essential - Always Active)

Core command processors directly bound to JikiME commands.

| Agent | Command | Purpose |
|-------|---------|---------|
| `manager-project` | `/jikime:0-project` | Project initialization and setup |
| `manager-spec` | `/jikime:1-plan` | EARS SPEC generation and planning |
| `manager-ddd` | `/jikime:2-run` | DDD ANALYZE-PRESERVE-IMPROVE execution |
| `manager-docs` | `/jikime:3-sync` | Documentation generation and synchronization |

Loading: Always active (loaded on command invocation)

---

### Tier 2: Orchestration & Quality (Auto-triggered)

Orchestration and quality management agents.

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `planner` | `/jikime:2-run` Phase 1 | SPEC analysis and execution strategy |
| `manager-quality` | Post-implementation | TRUST 5 validation |
| `manager-git` | Git operations | Branch, commit, and PR management |

Loading: Auto-triggered based on workflow phase

---

### Tier 3: Domain Experts (Lazy-loaded)

Domain-specific implementation experts.

| Agent | Domain | Purpose |
|-------|--------|---------|
| `backend` | Backend | Backend architecture and API design |
| `frontend` | Frontend | Frontend UI/UX implementation |
| `devops` | Infrastructure | DevOps, monitoring, and performance |
| `security-auditor` | Security | Security analysis and OWASP validation |
| `architect` | Design | UI/UX, components, and accessibility |

Loading: Lazy-loaded based on keyword detection or SPEC requirements

Trigger Keywords:
- `backend`: "backend", "api", "server", "endpoint", "database", "schema", "migration", "query"
- `frontend`: "frontend", "ui", "component", "page"
- `devops`: "deploy", "ci/cd", "performance", "monitoring"
- `security-auditor`: "security", "auth", "encryption", "owasp"
- `architect`: "design", "ux", "accessibility", "component"

---

### MCP Tool Integration (Not Agents)

MCP tools are accessed directly via tool calls, not through agent delegation.
Available MCP tools: Context7, Sequential-Thinking, Playwright, etc.

Resume Pattern for Explore agent (40-60% token savings):
```python
# Initial call
result = Task(subagent_type="Explore", prompt="Research React 19 APIs")
agent_id = result.agent_id

# Resume with context
result2 = Task(subagent_type="Explore", prompt="Compare with React 18", resume=agent_id)
```

Benefits:
- Token savings: 40-60% reduction vs. fresh context
- Context accuracy: 95%+ in resumed sessions
- Multi-day analysis: Support for long-running tasks

---

### Tier 5: Factory Agents (Meta-development)

Meta-generation agents for JikiME-ADK development.

| Agent | Purpose |
|-------|---------|
| `agent-builder` | New agent creation and configuration |
| `skill-builder` | Skill definition creation and management |
| `command-builder` | Custom slash command creation and optimization |

Use Case: When developing JikiME-ADK itself (not for end-user projects)

---

### Tier 6: Support (On-demand)

Support and utility services.

| Agent | Purpose |
|-------|---------|
| `debugger` | Error analysis and diagnostic support |

Loading: On-demand when errors occur or configuration changes needed

---

---

### System Agents

Built-in system agents for codebase exploration.

| Agent | Purpose |
|-------|---------|
| `Explore` | Codebase exploration and file system analysis |
| `Plan` | Strategic decomposition and planning |

Note: These are Claude Code built-in agents, not JikiME-ADK custom agents.

---

## Advanced Implementation (10+ minutes)

### Agent Selection Criteria

| Task Complexity | Files | Architecture Impact | Agents | Strategy |
|----------------|-------|---------------------|--------|----------|
| Simple | 1 file | No impact | 1-2 agents | Sequential |
| Medium | 3-5 files | Moderate | 2-3 agents | Sequential |
| Complex | 10+ files | High impact | 5+ agents | Mixed parallel/sequential |

Decision Tree:
```
Is this a new feature or architecture change?
 YES, 10+ files → Complex (5+ agents, parallel/sequential)
 YES, 3-5 files → Medium (2-3 agents, sequential)
 NO, 1-2 files → Simple (1-2 agents, sequential)
```

---

### Delegation Principles

1. Agent-First: The orchestrator NEVER executes tasks directly. ALWAYS delegates via Task()

2. Naming Consistency: All agents follow `{domain}-{role}` pattern
 - Lowercase only
 - Hyphen separator
 - Domain prefix indicates tier

3. Context Passing: Pass each agent's results as context to the next agent
 ```python
 result1 = Task("backend", "Design API")
 result2 = Task("frontend", "Implement UI", context={"api_design": result1})
 ```

4. Sequential vs Parallel:
 - Sequential: When dependencies exist between agents
 - Parallel: When agents work independently

---

### Merged Agents (Historical Reference)

The following agents were merged to reduce complexity:

| Old Agent | Merged Into | Reason |
|-----------|-------------|--------|
| doc-syncer | manager-docs | Documentation consolidation |
| trust-checker | manager-quality | Quality gate unification |
| api-designer | backend | Backend expertise consolidation |
| migration-expert | backend | Data operations unification |
| monitoring-expert | infra-devops | Infrastructure consolidation |
| performance-engineer | infra-devops | Infrastructure consolidation |
| component-designer | architect | Design system unification |
| accessibility-expert | architect | Design system unification |

Total Agents: 26 (down from 35, -26% reduction)

---

### Removed Agents

| Agent | Reason |
|-------|--------|
| format-expert | Replaced by direct linter usage (ruff, prettier) |
| sync-manager | Redundant with manager-docs |

---

### Skill Architecture Reference

The following skills are organized for token efficiency and domain specialization:

| Category | Skills | Purpose |
|----------|--------|---------|
| Language (Separated) | jikime-lang-python, jikime-lang-typescript, jikime-lang-go, jikime-lang-java, jikime-lang-javascript, jikime-lang-flutter, jikime-lang-php | Domain-specific language skills for 40-60% token savings |
| Platform (Separated) | jikime-platform-clerk, jikime-platform-supabase, jikime-platform-vercel | Domain-specific platform skills for 30-50% token savings |
| Foundation | jikime-foundation-core, jikime-foundation-claude, jikime-foundation-context, jikime-foundation-quality | Core principles and quality gates |

| Workflow | jikime-workflow-spec, jikime-workflow-project, jikime-workflow-testing, jikime-workflow-jit-docs | Workflow automation and testing |
| Domain | jikime-domain-backend, jikime-domain-frontend, jikime-domain-database, jikime-domain-uiux | Domain expertise patterns |

Language Skills Selection Guide:

| Language Skill | Coverage | Use When |
|----------------|----------|----------|
| jikime-lang-python | Python 3.13, FastAPI, Django, pytest | Backend APIs, data science, automation |
| jikime-lang-typescript | TypeScript 5.9, React 19, Next.js 16, tRPC | Frontend, full-stack web development |
| jikime-lang-go | Go 1.23, Fiber, Gin, GORM | Microservices, CLI tools, cloud-native |
| jikime-lang-java | Java 21, Spring Boot 3.3, virtual threads | Enterprise applications, microservices |
| jikime-lang-javascript | Node.js 22, Bun, Deno, Express, Fastify | Backend services, scripting |
| jikime-lang-flutter | Flutter 3.24, Dart 3.5, Riverpod | Cross-platform mobile and desktop apps |
| jikime-lang-php | PHP 8.3, Laravel 11, Symfony 7 | Web applications, CMS development |

Platform Skills Selection Guide:

| Platform Skill | Providers | Use When |
|----------------|-----------|----------|
| jikime-platform-clerk | Clerk | Modern authentication, WebAuthn, passkeys |
| jikime-platform-supabase | Supabase | PostgreSQL, real-time, RLS, Edge Functions |
| jikime-platform-vercel | Vercel | Edge deployment, Next.js hosting, ISR |

Note: Agents now use specific skills based on their domain. Cross-language agents include jikime-lang-python and jikime-lang-typescript by default.

---

### Tier Loading Strategy

| Tier | Loading | Context Budget | Trigger |
|------|---------|----------------|---------|
| Tier 1 | Always active | 30% | Command invocation |
| Tier 2 | Auto-trigger | 20% | Quality gates, orchestration |
| Tier 3 | Lazy-load | 30% | Keyword detection, SPEC analysis |
| Tier 4 | On-demand | 10% | MCP operations |
| Tier 5 | On-demand | 5% | Meta-generation |
| Tier 6 | On-demand | 3% | Errors, configuration |
| Tier 7 | On-demand | 2% | AI model integration |

Total Budget: 100% of available context per workflow phase

---

### Error Handling

Common Errors:

| Error | Solution |
|-------|----------|
| "Agent not found" | Verify agent name follows `{domain}-{role}` (lowercase, hyphenated) |
| "Agent not responding" | Check agent permissions in settings.json |
| "Context overflow" | Execute /clear and retry with smaller context |
| "Permission denied" | Update IAM rules in .claude/settings.json |

Error Recovery Pattern:
```python
try:
 result = Task("backend", "Implement feature")
except AgentNotFoundError:
 # Check agent name format
 result = Task("backend", "Implement feature") # Corrected name
except PermissionError:
 # Update settings.json IAM rules
 result = Task("backend", "Implement feature", permissions=["write"])
```

---

## Works Well With

Skills:
- [jikime-foundation-core](../SKILL.md) - Parent skill (this module is part of it)
- [jikime-foundation-context](../../jikime-foundation-context/SKILL.md) - Token budget and session state
- [jikime-foundation-claude](../../jikime-foundation-claude/SKILL.md) - Claude Code configuration

Other Modules:
- [delegation-patterns.md](delegation-patterns.md) - Delegation strategies
- [token-optimization.md](token-optimization.md) - Token budget management
- [execution-rules.md](execution-rules.md) - Security and permissions

Commands:
- `/jikime:0-project` → `manager-project`
- `/jikime:1-plan` → `manager-spec`
- `/jikime:2-run` → `manager-ddd`
- `/jikime:3-sync` → `manager-docs`

---

Total Agents: 26 active agents (down from 35, -26% reduction)
Maintained by: JikiME-ADK Team
Status: Production Ready
