---
name: Gemini CLI Agent
description: Expert Gemini CLI sub-agent patterns for autonomous task execution, context management, and multi-agent orchestration. Activates with "/gemini" or when delegating tasks to Gemini CLI.
---

# 🤖 Gemini CLI Agent Skill

A comprehensive framework for creating, configuring, and orchestrating Gemini CLI sub-agents for autonomous task execution within the NEXUS project.

## Activation

This skill activates when:
1. User explicitly requests: `/gemini`, `create gemini agent`, or `delegate to gemini`
2. Task requires parallel agent execution
3. User wants to create a specialized sub-agent
4. Orchestrating complex multi-step workflows

---

## ✅ When to Use Gemini CLI

Use Gemini CLI as the **primary agent** when:

| Scenario | Why Gemini? |
|----------|-------------|
| **New screen creation** | UI/UX expertise, visual verification |
| **Component design/refactoring** | Understands component hierarchies |
| **Styling & layout work** | Strong with NativeWind/Tailwind |
| **UI bug fixes** | Can visualize component tree |
| **Cross-module UI features** | 1M token context handles entire codebase |
| **Responsive design** | Reasons about different screen sizes |
| **Animation/gestures** | Understands React Native Animated API |

**Component ownership:**
- `apps/manager/` → Gemini CLI
- `apps/driver/` → Gemini CLI

📚 **Full profile:** [docs/agents/agent-profiles.md](../../../docs/agents/agent-profiles.md)

---

## ❌ When NOT to Use Gemini CLI

Avoid Gemini CLI for:

| Task Type | Better Agent | Why? |
|-----------|--------------|------|
| **Backend-only tasks** | Claude Code | No UI to verify |
| **Convex mutations/queries** | Claude Code | Backend logic focus |
| **CI/CD configuration** | Codex | Strict workflow needed |
| **Git hooks setup** | Codex | Multi-step verification |
| **Systematic testing** | Codex | Thorough, structured approach |
| **Complex debugging (race conditions)** | Codex | Systematic root cause analysis |
| **Simple config file updates** | Claude Code | Overkill for simple changes |

**Anti-patterns:**
- ❌ Using Gemini for tasks with no visual component
- ❌ Expecting strict workflow adherence
- ❌ Using for simple one-file backend changes

📚 **Decision tree:** [docs/agents/decision-tree.md](../../../docs/agents/decision-tree.md)

---

## Core Concepts

### What is a Gemini CLI Agent?

A Gemini CLI Agent is a specialized sub-process that runs autonomously with:
- **Scoped Context**: Limited to specific files, directories, or concerns
- **Defined Persona**: Expert in a particular domain (backend, testing, docs)
- **Clear Objectives**: Single focused task or workflow
- **Isolated Execution**: Runs independently, reports back results

### Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Master Orchestrator                      │
│                    (This Agent / Claude)                     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Planning Agent│   │ Implement Agent│  │ Debug Agent   │
│ (gemini -p)   │   │ (gemini -p)    │  │ (gemini -p)   │
└───────────────┘   └───────────────┘   └───────────────┘
```

---

## Agent Types

### 1. Planning Agent
**Purpose:** Architectural analysis, task breakdown, dependency mapping

```yaml
# agents/planning_agent.yaml
name: planning_agent
persona: Senior Software Architect
expertise:
  - System design
  - Task decomposition
  - Dependency analysis
  - Risk assessment
context_files:
  - PRD.md
  - SPEC.md
  - docs/standards.md
output: implementation_plan.md
```

**Invocation:**
```powershell
gemini -p "As a Senior Software Architect, analyze the PRD.md and SPEC.md to create a detailed implementation plan for [FEATURE]. Focus on dependencies, risks, and task breakdown."
```

---

### 2. Implementation Agent
**Purpose:** Code writing, feature implementation, refactoring

```yaml
# agents/implementation_agent.yaml
name: implementation_agent
persona: Expert TypeScript Developer
expertise:
  - TypeScript/React Native
  - Convex backend
  - NativeWind styling
  - Genkit AI flows
context_files:
  - convex/schema.ts
  - convex/SPEC.md
  - apps/*/SPEC.md
constraints:
  - Follow docs/standards.md
  - Use existing patterns
  - No breaking changes without approval
```

**Invocation:**
```powershell
gemini -p "Implement [FEATURE] following the patterns in convex/SPEC.md. Create the schema, queries, mutations, and actions. Follow docs/standards.md strictly."
```

---

### 3. Debug Agent
**Purpose:** Root cause analysis, error fixing, test generation

```yaml
# agents/debug_agent.yaml
name: debug_agent
persona: Senior Debug Engineer
expertise:
  - TypeScript error diagnosis
  - Convex debugging
  - React Native troubleshooting
  - Test failure analysis
tools:
  - grep_search
  - view_file
  - run_command (tsc, vitest)
```

**Invocation:**
```powershell
gemini -p "Debug this error: [ERROR_MESSAGE]. Analyze the stack trace, identify root cause, and propose a fix. Verify the fix compiles correctly."
```

---

### 4. Docs Agent
**Purpose:** Documentation maintenance, context updates, report generation

```yaml
# agents/docs_agent.yaml
name: docs_agent
persona: Technical Writer
expertise:
  - API documentation
  - README maintenance
  - CHANGELOG updates
  - Architecture diagrams
context_files:
  - README.md
  - GEMINI.md
  - docs/*.md
output_formats:
  - markdown
  - mermaid diagrams
```

**Invocation:**
```powershell
gemini -p "Update the documentation in docs/ to reflect the recent changes to [COMPONENT]. Generate API docs and update the architecture diagram."
```

---

### 5. Testing Agent
**Purpose:** Test creation, coverage improvement, validation

```yaml
# agents/testing_agent.yaml
name: testing_agent
persona: QA Engineer
expertise:
  - Vitest unit tests
  - Integration testing
  - E2E testing patterns
  - Coverage analysis
context_files:
  - vitest.config.ts
  - tests/**/*.test.ts
commands:
  - npm run test
  - npm run test:coverage
```

**Invocation:**
```powershell
gemini -p "Create comprehensive tests for [COMPONENT]. Include unit tests, edge cases, and integration tests. Aim for >80% coverage."
```

---

## Prompt Engineering Patterns

### The ARCS Framework

Every agent prompt should follow **ARCS**:

```
A - Action: What specific task to perform
R - Role: What persona/expertise to adopt
C - Context: What files/information are relevant
S - Success: What does a successful output look like
```

**Example:**
```powershell
gemini -p "
[ACTION] Create CRUD operations for the Customers table
[ROLE] As an expert Convex developer following NEXUS patterns
[CONTEXT] Reference convex/schema.ts and convex/shipments.ts for patterns
[SUCCESS] Deliver customers.ts with:
  - Schema type definitions
  - listCustomers query (paginated, filtered by companyId)
  - getCustomer query (by ID)
  - createCustomer mutation (with validation)
  - updateCustomer mutation (with audit logging)
  - deleteCustomer mutation (soft delete)
"
```

---

### Context Injection Patterns

**Pattern 1: File Reference**
```powershell
gemini -p "Review these files: ./convex/schema.ts, ./apps/manager/SPEC.md and implement [TASK]"
```

**Pattern 2: Inline Context**
```powershell
gemini -p "Given this schema:
$(cat convex/schema.ts | head -50)

Implement the queries for the vehicles table."
```

**Pattern 3: Brain MCP Context**
```powershell
# First, recall relevant memory
$context = gemini -q "Use mcp_brain-mcp_agentos_memory to recall 'architecture-decisions'"
gemini -p "Using this context: $context, implement [FEATURE]"
```

---

### Safety Constraints

Always include safety rails in prompts:

```
CONSTRAINTS:
- Do NOT modify files outside of [SCOPE]
- Do NOT delete or overwrite existing implementations
- Do NOT change public APIs without explicit approval
- ALWAYS run TypeScript compilation check before completing
- ALWAYS follow docs/standards.md patterns
```

---

## Execution Patterns

### Sequential Execution
When tasks have dependencies:

```powershell
# Step 1: Planning
gemini -p "Plan the implementation of [FEATURE]" > plan.md

# Step 2: Implementation (depends on plan)
gemini -p "Implement based on this plan: $(cat plan.md)"

# Step 3: Testing (depends on implementation)
gemini -p "Write tests for the implementation"
```

### Parallel Execution
When tasks are independent:

```powershell
# Run in parallel (PowerShell)
Start-Job { gemini -p "Implement component A" }
Start-Job { gemini -p "Implement component B" }
Start-Job { gemini -p "Update documentation" }
Get-Job | Wait-Job | Receive-Job
```

---

## State Management

### Using Brain MCP for State

```powershell
# Save state
gemini -p "Use mcp_brain-mcp_agentos_memory to remember key='current-task' value='implementing-auth'"

# Recall state
gemini -p "Use mcp_brain-mcp_agentos_memory to recall key='current-task'"

# Task tracking
gemini -p "Use mcp_brain-mcp_agentos_task to add task description='Implement login screen' priority='high'"
```

### File-Based State

```markdown
<!-- .agentos/state.md -->
## Current Agent State

### Active Task
- ID: auth-implementation
- Phase: EXECUTION
- Progress: 3/7 files completed

### Completed
- [x] convex/auth.ts
- [x] apps/manager/hooks/useAuth.ts
- [x] apps/manager/screens/LoginScreen.tsx

### Remaining
- [ ] apps/driver/hooks/useAuth.ts
- [ ] apps/driver/screens/LoginScreen.tsx
- [ ] Tests
- [ ] Documentation
```

---

## Output Templates

### Agent Report Template

```markdown
## 🤖 Agent Execution Report

**Agent:** [agent_name]
**Task:** [task_description]
**Status:** ✅ Complete / ⚠️ Partial / ❌ Failed

### Files Modified
- `path/to/file1.ts` - [change description]
- `path/to/file2.ts` - [change description]

### Actions Taken
1. [action 1]
2. [action 2]
3. [action 3]

### Verification
- TypeScript: ✅ No errors
- Tests: ✅ 15/15 passing
- Lint: ⚠️ 2 warnings (non-blocking)

### Notes
[Any important observations or recommendations]

### Next Steps
- [ ] [suggested follow-up 1]
- [ ] [suggested follow-up 2]
```

---

## Integration with NEXUS Workflows

### With /convex-feature Workflow

```powershell
# Delegate schema creation to Gemini
gemini -p "Following /convex-feature workflow, create schema for [ENTITY] in convex/schema.ts"
```

### With /mobile-screen Workflow

```powershell
# Delegate screen creation to Gemini
gemini -p "Following /mobile-screen workflow, create [SCREEN] for manager app with NativeWind styling"
```

### With /ai-feature Workflow

```powershell
# Delegate Genkit flow creation to Gemini
gemini -p "Following /ai-feature workflow, create a Genkit flow for [AI_CAPABILITY]"
```

---

## Troubleshooting

### Common Issues

**Issue: Agent loses context**
```
🔧 Solution: Break task into smaller chunks, provide explicit file references
```

**Issue: Agent makes breaking changes**
```
🔧 Solution: Add explicit constraints about what NOT to modify
```

**Issue: Agent output is incomplete**
```
🔧 Solution: Define explicit success criteria in the prompt
```

**Issue: Agent creates duplicate code**
```
🔧 Solution: Reference existing patterns with "Follow the pattern in [FILE]"
```

---

## Best Practices

### DO ✅
- Provide clear, scoped tasks
- Include explicit success criteria
- Reference existing patterns
- Set safety constraints
- Request verification steps

### DON'T ❌
- Give vague instructions like "fix the bugs"
- Allow unrestricted file access
- Skip context injection
- Forget to request compilation checks
- Chain too many dependent operations

---

## Quick Reference

### Invocation Commands

```powershell
# Basic execution
gemini -p "Your prompt here"

# With specific context
gemini -p "Context: $(cat file.md). Task: [TASK]"

# Autonomous mode (use carefully)
gemini -y -p "Autonomous task with auto-approval"
```

### Common Flags

| Flag | Purpose |
|------|---------|
| `-p` | Provide prompt directly |
| `-y` | Auto-approve (dangerous) |
| `-q` | Quiet mode, output only |
| `--model` | Specify model variant |

---

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| Max concurrent agents | 3 | Avoid API rate limits |
| Context file limit | 10 | Keep context focused |
| Output verification | On | Always verify compilation |
| Auto-commit | Off | Require manual review |

---

## Example Full Session

```
User: Create a new Convex feature for fleet tracking

🤖 [Gemini CLI Agent Mode Activated]
   
   I'll orchestrate this with specialized agents:
   
   **Phase 1: Planning**
   Delegating to planning_agent...
   
   gemini -p "Analyze SPEC.md and create implementation plan for fleet tracking feature"
   
   ✅ Plan created: .agentos/plans/fleet-tracking.md
   
   **Phase 2: Implementation**
   Delegating to implementation_agent...
   
   gemini -p "Implement fleet tracking following plan in .agentos/plans/fleet-tracking.md"
   
   ✅ Files created:
   - convex/fleetTracking.ts
   - convex/schema.ts (updated)
   
   **Phase 3: Testing**
   Delegating to testing_agent...
   
   gemini -p "Create tests for convex/fleetTracking.ts"
   
   ✅ Tests created: tests/convex/fleetTracking.test.ts
   
   **Phase 4: Documentation**
   Delegating to docs_agent...
   
   gemini -p "Update docs/API.md with fleet tracking endpoints"
   
   ✅ Documentation updated
   
   [Session Complete] 
   All agents executed successfully. Ready for review.
```

---

## When to Exit Agent Mode

- Task is complete → Generate summary report
- User requests manual control
- Agent encounters blocking error requiring human decision
- Scope creep detected → Request clarification

```
🤖 Agent session complete!
   
   📊 Summary:
   - Files created: 4
   - Tests passing: 12/12
   - TypeScript: ✅ Clean
   
   Would you like me to commit these changes? [Y/n]
   
   [Exiting Gemini CLI Agent Mode]
```
