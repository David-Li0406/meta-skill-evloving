# Commands Reference - JikiME-ADK Core Commands

Purpose: Complete reference for JikiME-ADK's 6 core commands used in SPEC-First DDD workflow.

Last Updated: 2025-11-25
Version: 2.0.0

---

## Quick Reference (30 seconds)

JikiME-ADK provides 6 core commands for SPEC-First DDD execution:

| Command            | Purpose                | Phase         |
| ------------------ | ---------------------- | ------------- |
| `/jikime:0-project`  | Project initialization | Setup         |
| `/jikime:1-plan`     | SPEC generation        | Planning      |
| `/jikime:2-run`      | DDD implementation     | Development   |
| `/jikime:3-sync`     | Documentation sync     | Documentation |

Required Workflow:
```
1. /jikime:0-project # Initialize
2. /jikime:1-plan "description" # Generate SPEC
3. /clear # Clear context (REQUIRED)
4. /jikime:2-run SPEC-001 # Implement
5. /jikime:3-sync SPEC-001 # Document
```

Critical Rule: Execute `/clear` after `/jikime:1-plan` (saves 45-50K tokens)

---

## Implementation Guide (5 minutes)

### `/jikime:0-project` - Project Initialization

Purpose: Initialize project structure and generate configuration

Agent Delegation: `manager-project`

Usage:
```bash
/jikime:0-project
/jikime:0-project --with-git
```

What It Does:
1. Creates `.jikime/` directory structure
2. Generates `config.json` with default settings
3. Initializes Git repository (if `--with-git` flag provided)
4. Sets up JikiME-ADK workflows

Output:
- `.jikime/` directory
- `.jikime/config/config.yaml`
- `.jikime/memory/` (empty, ready for session state)
- `.jikime/logs/` (empty, ready for logging)

Next Step: Ready for SPEC generation via `/jikime:1-plan`

Example:
```
User: /jikime:0-project
Orchestrator: Project initialized successfully.
 - .jikime/config/config.yaml created
 - Git workflow set to 'manual' mode
 Ready for SPEC generation.
```

---

### `/jikime:1-plan` - SPEC Generation

Purpose: Generate SPEC document in EARS format

Agent Delegation: `manager-spec`

Usage:
```bash
/jikime:1-plan "Implement user authentication endpoint (JWT)"
/jikime:1-plan "Add dark mode toggle to settings page"
```

What It Does:
1. Analyzes user request
2. Generates EARS format SPEC document
3. Creates `.jikime/specs/SPEC-XXX/` directory
4. Saves `spec.md` with requirements

EARS Format (5 sections):
- WHEN (trigger conditions)
- IF (preconditions)
- THE SYSTEM SHALL (functional requirements)
- WHERE (constraints)
- UBIQUITOUS (quality requirements)

Output:
- `.jikime/specs/SPEC-001/spec.md` (EARS document)
- SPEC ID assigned (auto-incremented)

CRITICAL: Execute `/clear` immediately after completion
- Saves 45-50K tokens
- Prepares clean context for implementation

Example:
```
User: /jikime:1-plan "Implement user authentication endpoint (JWT)"
Orchestrator: SPEC-001 generated successfully.
 Location: .jikime/specs/SPEC-001/spec.md

 IMPORTANT: Execute /clear now to free 45-50K tokens.
```

---

### `/jikime:2-run` - DDD Implementation

Purpose: Execute ANALYZE-PRESERVE-IMPROVE cycle

Agent Delegation: `manager-ddd`

Usage:
```bash
/jikime:2-run SPEC-001
/jikime:2-run SPEC-002
```

What It Does:
1. Reads SPEC document
2. Executes DDD cycle in 3 phases:
 - RED: Write failing tests
 - GREEN: Implement minimal code to pass tests
 - REFACTOR: Optimize and clean up code
3. Validates TRUST 5 quality gates
4. Generates implementation report

DDD Process:
```
Phase 1 (RED):
 - Write failing tests for each requirement
 - Run tests → ALL FAIL (expected)

Phase 2 (GREEN):
 - Implement minimal code to pass tests
 - Run tests → ALL PASS

Phase 3 (REFACTOR):
 - Optimize code structure
 - Improve readability
 - Remove duplication
 - Run tests → ALL PASS (maintained)
```

Output:
- Implemented code (in source directories)
- Test files (in test directories)
- Quality report (TRUST 5 validation)

Requirement: Test coverage ≥ 85% (TRUST 5)

Example:
```
User: /jikime:2-run SPEC-001
Orchestrator: DDD implementation cycle started for SPEC-001.

 RED: 12 failing tests written
 GREEN: Implementation complete, all tests passing
 REFACTOR: Code optimized

 Test Coverage: 92% ( meets 85% threshold)
 TRUST 5: All gates passed
```

---

### `/jikime:3-sync` - Documentation Synchronization

Purpose: Auto-generate API documentation and project artifacts

Agent Delegation: `manager-docs`

Usage:
```bash
/jikime:3-sync SPEC-001
/jikime:3-sync SPEC-002
```

What It Does:
1. Reads implemented code
2. Generates API documentation (OpenAPI format)
3. Creates architecture diagrams
4. Produces project completion report

Output:
- API documentation (OpenAPI/Swagger format)
- Architecture diagrams (Mermaid)
- `.jikime/docs/SPEC-001/` directory
- Project report

Example:
```
User: /jikime:3-sync SPEC-001
Orchestrator: Documentation synchronized for SPEC-001.

 Generated:
 - API documentation: .jikime/docs/SPEC-001/api.yaml
 - Architecture diagram: .jikime/docs/SPEC-001/architecture.md
 - Completion report: .jikime/docs/SPEC-001/report.md
```

---

## Advanced Implementation (10+ minutes)

### Context Initialization Rules

Rule 1: Execute `/clear` AFTER `/jikime:1-plan` (mandatory)
- SPEC generation uses 45-50K tokens
- `/clear` frees this context for implementation phase
- Prevents context overflow

Rule 2: Execute `/clear` when context > 150K tokens
- Monitor context usage via `/context` command
- Prevents token limit exceeded errors

Rule 3: Execute `/clear` after 50+ conversation messages
- Accumulated context from conversation history
- Reset for fresh context

Why `/clear` is critical:
```
Without /clear:
 SPEC generation: 50K tokens
 Implementation: 100K tokens
 Total: 150K tokens (approaching 200K limit)

With /clear:
 SPEC generation: 50K tokens
 /clear: 0K tokens (reset)
 Implementation: 100K tokens
 Total: 100K tokens (50K budget remaining)
```

---

### Command Delegation Patterns

Each command delegates to a specific agent:

| Command            | Agent              | Agent Type              |
| ------------------ | ------------------ | ----------------------- |
| `/jikime:0-project`  | `manager-project` | Tier 1 (Always Active)  |
| `/jikime:1-plan`     | `manager-spec`    | Tier 1 (Always Active)  |
| `/jikime:2-run`      | `manager-ddd`     | Tier 1 (Always Active)  |
| `/jikime:3-sync`     | `manager-docs`    | Tier 1 (Always Active)  |

Delegation Flow:
```
User executes command
 ↓
Orchestrator receives command
 ↓
Command processor agent invoked
 ↓
Agent executes workflow
 ↓
Results reported to user
```

---

### Token Budget by Command

| Command        | Average Tokens | Phase Budget                          |
| -------------- | -------------- | ------------------------------------- |
| `/jikime:1-plan` | 45-50K         | Planning Phase (30K allocated)        |
| `/jikime:2-run`  | 80-100K        | Implementation Phase (180K allocated) |
| `/jikime:3-sync` | 20-25K         | Documentation Phase (40K allocated)   |
| Total          | 145-175K       | 250K per feature                      |

Optimization:
- Use Haiku 4.5 for `/jikime:2-run` (fast, cost-effective)
- Use Sonnet 4.5 for `/jikime:1-plan` (high-quality SPEC)
- Execute `/clear` between phases (critical)

---

### Error Handling

Common Errors:

| Error                     | Command                | Solution                                    |
| ------------------------- | ---------------------- | ------------------------------------------- |
| "Project not initialized" | `/jikime:1-plan`         | Run `/jikime:0-project` first                 |
| "SPEC not found"          | `/jikime:2-run SPEC-999` | Verify SPEC ID exists                       |
| "Token limit exceeded"    | Any                    | Execute `/clear` immediately                |
| "Test coverage < 85%"     | `/jikime:2-run`          | `manager-quality` auto-generates missing tests |

Recovery Pattern:
```bash
# Error: Token limit exceeded
1. /clear # Reset context
2. /jikime:2-run SPEC-001 # Retry with clean context
```

---

### Workflow Variations

Standard Workflow (Full SPEC):
```
/jikime:0-project → /jikime:1-plan → /clear → /jikime:2-run → /jikime:3-sync
```

Quick Workflow (No SPEC for simple tasks):
```
/jikime:0-project → Direct implementation (for 1-2 file changes)
```

Iterative Workflow (Multiple SPECs):
```
/jikime:1-plan "Feature A" → /clear → /jikime:2-run SPEC-001 → /jikime:3-sync SPEC-001
/jikime:1-plan "Feature B" → /clear → /jikime:2-run SPEC-002 → /jikime:3-sync SPEC-002
```

---

### Integration with Git Workflow

Commands automatically integrate with Git based on `config.json` settings:

Manual Mode (Local Git):
- `/jikime:1-plan`: Prompts for branch creation
- `/jikime:2-run`: Auto-commits to local branch
- No auto-push

Personal Mode (GitHub Individual):
- `/jikime:1-plan`: Auto-creates feature branch + auto-push
- `/jikime:2-run`: Auto-commits + auto-push
- `/jikime:3-sync`: Suggests PR creation (user choice)

Team Mode (GitHub Team):
- `/jikime:1-plan`: Auto-creates feature branch + Draft PR
- `/jikime:2-run`: Auto-commits + auto-push
- `/jikime:3-sync`: Prepares PR for team review

---

## Works Well With

Skills:
- [jikime-foundation-core](../SKILL.md) - Parent skill
- [jikime-foundation-context](../../jikime-foundation-context/SKILL.md) - Token budget management

Other Modules:
- [spec-first-ddd.md](spec-first-ddd.md) - Detailed SPEC-First DDD process
- [token-optimization.md](token-optimization.md) - /clear execution strategies
- [agents-reference.md](agents-reference.md) - Agent catalog

Agents:
- [manager-project](agents-reference.md#tier-1-command-processors) - `/jikime:0-project`
- [manager-spec](agents-reference.md#tier-1-command-processors) - `/jikime:1-plan`
- [manager-ddd](agents-reference.md#tier-1-command-processors) - `/jikime:2-run`
- [manager-docs](agents-reference.md#tier-1-command-processors) - `/jikime:3-sync`

---

Maintained by: JikiME-ADK Team
Status: Production Ready
