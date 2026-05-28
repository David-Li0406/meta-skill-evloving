# Common Patterns & Foundations

## Table of Contents

- [Core Philosophy](#core-philosophy)
- [Three Core Principles](#three-core-principles)
- [Progressive Disclosure](#progressive-disclosure)
- [Core Values Framework](#core-values-framework)
- [Frontmatter Specification](#frontmatter-specification)
- [Structural Patterns](#structural-patterns)
- [Black Box Scripts Pattern](#black-box-scripts-pattern)
- [Plan-Validate-Execute Pattern](#plan-validate-execute-pattern)
- [Trust the Agent's Native Capacities](#trust-the-agents-native-capacities)
- [Writing Style Requirements](#writing-style-requirements)
- [File References](#file-references)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

> Shared principles, design wisdom, and patterns used across all customization layers.

> **For layer-specific guidance**: See [layer-selection.md](layer-selection.md)

---

## Core Philosophy

### The Delta Standard

> **Good Customization = Expert-only Knowledge − What Claude Already Knows**

A customization's value is measured by its **knowledge delta** — the gap between what it provides and what the model already knows.

- **Expert-only knowledge**: Decision trees, trade-offs, edge cases, anti-patterns, domain-specific thinking frameworks
- **What Claude already knows**: Basic concepts, standard library usage, common programming patterns

When customization explains "what is PDF" or "how to write a for-loop", it's compressing knowledge Claude already has. This is **token waste**.

**The Delta Question**: "Would any agent know this?" If yes, don't write it.

---

## Three Core Principles

### 1. Simplicity Over Fragmentation

Agents must read full customization context to execute effectively. Fragmentation across multiple files should be rare:

**When to disperse**:
- SKILL.md exceeds 35,000 characters OR
- Highly situational edge cases (<5% of tasks)

**Default**: Keep core knowledge in SKILL.md

### 2. Set Appropriate Degrees of Freedom

Match specificity to task fragility and variability.

**Narrow Bridge** (Low Freedom):
- One safe path exists, operations are fragile
- Use exact instructions with minimal parameters
- Example: Database migrations

**Open Field** (High Freedom):
- Many valid paths exist, context-dependent decisions
- Give general direction with heuristic principles
- Example: Code reviews

### 3. Match Autonomy to Task

Use the **Criticality + Variability** framework:

| Task Type | Criticality | Variability | Autonomy | Pattern |
|-----------|------------|-------------|----------|---------|
| Database migrations | High | Low | Protocol | Exact steps |
| Code reviews | Medium | High | Guided | Heuristics |
| Creative writing | Low | High | Heuristic | Principles |

### 4. Minimize Iteration Burden

**Design for determinism**: Encode constraints and decision trees upfront so typical units of work complete in fewer correction cycles.

**The iteration efficiency equation:**
```
Completed Unit = Feature implemented + Tests updated + Tests pass
Total Cost = Number of top-level prompts + Number of subagent runs

Target Budget: 1-2 top-level prompts per unit
Max Tolerable: 3+ top-level prompts indicates design flaw
```

**Hard Stop Rules (MANDATORY)**:
- Max 3 subagent spawns per work unit
- Max 2 correction cycles on any single file
- Immediate termination when success criteria met

---

## Progressive Disclosure

Customizations use tiered loading for optimal token economics:

**Tier 1: Metadata** (~100 tokens)
- Name and description
- Always loaded for discovery

**Tier 2: SKILL.md** (<35,000 characters)
- Complete operational instructions
- Loaded when skill is invoked

**Tier 3: Resources** (as needed)
- Files in references/ or scripts/
- Loaded on specific demand only

**When to disperse content**:
- SKILL.md exceeds 35,000 characters OR
- Highly situational edge cases (<5% of tasks) OR
- Content causes repeated back-and-forth clarifications

---

## Context Window Management

### The "Scope-Based MCP" Strategy

**Problem**: Too many MCP servers configured simultaneously causes:
- Tool definitions consuming 10%+ of context window
- Automatic Tool Search activation (adds overhead)
- Degraded quality/reliability during plugin development

**Solution**: Configure MCPs at appropriate **scopes** rather than enabling everything globally.

**Official Documentation**: https://code.claude.com/docs/en/mcp

### MCP Scopes Explained

| Scope | Location | Use For | Availability |
|-------|----------|---------|--------------|
| **Project** | `.mcp.json` at project root | Team-shared, project-specific MCPs | Everyone in project |
| **Local** | `~/.claude.json` (project path) | Personal, project-specific MCPs | You only, this project |
| **User** | `~/.claude.json` (global) | Cross-project utilities | You, all projects |

**Precedence**: Local > Project > User (local overrides when same name exists)

### Scope-Based MCP Management Decision Tree

```
Task Start: What MCPs does this project need?
│
├─ "Plugin development (authoring)"
│  └─→ Project scope: file-search, simplewebfetch only
│     └─ Local scope: personal tools (avoid user scope)
│
├─ "Web research / verification"
│  └─→ Project scope: browser, deepwiki, simplewebfetch
│     └─ Disable other project MCPs temporarily
│
├─ "Code analysis / validation"
│  └─→ Project scope: file-search, LSP (if needed)
│     └─ User scope: ONLY for utilities used across ALL projects
│
└─ "Multi-phase workflow"
   └─→ Use ENABLE_TOOL_SEARCH environment variable
      └─ Or manually comment out unused MCPs in .mcp.json
```

### Configuration Guidelines

**Project `.mcp.json`** (shared, version-controlled):
```json
{
  "mcpServers": {
    "file-search": { "command": "file-search-server" },
    "simplewebfetch": { "command": "webfetch-server" }
  }
}
```

**Local scope** (personal, not shared):
```bash
# Add MCP only for current project
claude mcp add --transport http personal-tool https://api.example.com/mcp --scope local
```

**User scope** (cross-project - use sparingly):
```bash
# Only for utilities used across ALL projects
claude mcp add --transport http universal-tool https://api.example.com/mcp --scope user
```

### Tool Management Checklist

**Project Setup:**
- [ ] Identify project-specific MCP needs (authoring vs research vs analysis)
- [ ] Configure only project-needed MCPs in `.mcp.json`
- [ ] Use local scope for personal tools (don't pollute user scope)
- [ ] Reserve user scope for truly universal utilities

**During Development:**
- [ ] Monitor for "tool definitions exceed 10% context" warnings
- [ ] If Tool Search activates, consider reducing configured MCPs
- [ ] Comment out unused MCPs from `.mcp.json` when not needed
- [ ] Restart Claude Code after `.mcp.json` changes

**Anti-patterns:**
- ❌ User scope filled with project-specific MCPs
- ❌ Leaving research MCPs configured during pure authoring
- ❌ "I'll add this to user scope just in case"
- ✅ "Configure at the most restrictive scope possible"

### MCP Tool Search

When tool definitions exceed 10% of context, Claude automatically enables **Tool Search**:
- MCP tools are loaded on-demand instead of upfront
- Reduces initial context cost
- Adds slight overhead when tools are first used

**Control Tool Search** via environment variable:

**Verify current value**:
```bash
echo $ENABLE_TOOL_SEARCH
```

**Edit shell configuration** (default: `~/.zshrc` or `~/.bashrc`):
```bash
# Auto mode (default): activates at 10% threshold
export ENABLE_TOOL_SEARCH=auto

# Custom threshold (activates earlier, at 5%)
export ENABLE_TOOL_SEARCH=auto:5

# Disable entirely (all MCP tools loaded upfront)
export ENABLE_TOOL_SEARCH=false
```

**When to adjust**:
- **Default (`auto`)**: Most users, activates at 10% context threshold
- **Lower threshold (`auto:5`)**: Many MCPs, want earlier Tool Search activation
- **Disabled (`false`)**: Few MCPs, prefer all tools loaded upfront

**Apply changes**: Restart terminal or run `source ~/.zshrc`

### Session Phase MCP Strategy

| Phase | Project MCPs | Action |
|-------|-------------|--------|
| **Authoring** | file-search, simplewebfetch | Comment out others in `.mcp.json` |
| **Research** | browser, deepwiki, simplewebfetch | Swap into `.mcp.json` temporarily |
| **Validation** | file-search, LSP | Minimal configuration |
| **Orchestration** | All workflow MCPs | Accept Tool Search overhead |

### Why This Matters

**Context efficiency**:
- Tool definitions don't crowd context window
- Tool Search only activates when truly needed
- Faster loading and response times

**Reliability**:
- Fewer "too many tools" scenarios
- Predictable tool availability per project
- Easier troubleshooting

**For integration**: See [layer-selection.md](layer-selection.md) for task-to-MCP mapping.

---

## Core Values Framework

Each value represents a **design approach**, not a rigid category. Trust task characteristics.

| Value | Design Focus | When to Apply |
|-------|-------------|---------------|
| **Reliability** | Deterministic execution with validation | "I need this done the same way, every time" |
| **Wisdom** | Decision frameworks and trade-off analysis | "I need expert judgment" |
| **Consistency** | Templates and standardized patterns | "Everything must look the same" |
| **Coordination** | Routing logic and state management | "Many parts, one symphony" |
| **Simplicity** | Direct path with minimal overhead | "Keep it simple" (3 steps or fewer) |

**For detailed guidance**: See [skills.md](skills.md)

---

## Frontmatter Specification

**Required fields:**

**`name`**:
- Max 64 characters
- Lowercase letters, numbers, and hyphens only
- Must not start or end with hyphen
- Must not contain consecutive hyphens (--)
- Must match the parent directory name
- **CRITICAL: Use gerund/active form** (analyzing, extracting, processing, validating)

**`description`**:
- 1-1024 characters
- Format: `"{{CAPABILITY}}. Use when {{TRIGGERS}}. Do not use for {{EXCLUSIONS}}."`
- Use third person ("This skill should be used when...")
- Include specific keywords for agent identification
- **MANDATORY: Context anchoring** - Explicitly mention file extensions (.pdf, .xlsx, .csv) or specific tools
- **MANDATORY: Negative constraints** - State what NOT to use this Skill for

**Optional fields:**

**`license`**: License name or reference to bundled license file

**`compatibility`**: Environment requirements (1-500 characters)

**`metadata`**: Arbitrary key-value mapping for additional metadata

**`allowed-tools`**: Space-delimited list of pre-approved tools (commands only)

---

## Structural Patterns

### A. Workflow-Based (Sequential Process)
**Definition**: Sequential processes requiring strict order
- **Structure**: Overview → Decision Tree → Step 1 → Step 2 → Validation
- **Use cases**: Database migrations, code reviews, complex report generation
- **Example**: Invoice organizer (Analyze → Extract → Rename → Classify)
- **When to use**: Tasks where skipping or reordering steps causes failures

### B. Task-Based (Toolbox / à la Carte)
**Definition**: Swiss army knife - multiple independent operations
- **Structure**: Quick Start → Action A → Action B → Action C
- **Use cases**: File manipulation (PDF, Excel), image processing
- **Example**: Slack GIF creator (Shake, Bounce, Spin primitives)
- **When to use**: When users need flexible, independent operations

### C. Reference/Guidelines (Expert Consultant)
**Definition**: Rules, standards, and specifications for Claude to apply
- **Structure**: Principles → Specific Rules → Good Examples → Bad Examples
- **Use cases**: Brand guidelines, coding standards, technical documentation
- **Example**: Brand guidelines (hex colors, fonts, tone guidelines)
- **When to use**: Quality/design standards, compliance requirements

### D. Capabilities-Based (Integrated Systems)
**Definition**: Interfacing with complex external systems via MCP
- **Structure**: Core Capabilities → Numbered feature list
- **Use cases**: Project management (Jira/Linear), database interaction (BigQuery)
- **Critical nuance**: **Don't blindly enforce scripts for simple operations**
  - If capability = "read/edit/create files" → Claude already knows this natively
  - Only use scripts for **complex** operations (API calls, data transformations, specialized tools)
- **When to use**: Complex external system integration

---

## Black Box Scripts Pattern

- Scripts should output JSON to stdout
- Agent never needs to read script source code
- Every constant must be justified in comments
- **Zero-Voodoo Rule**: If an agent cannot explain why a timeout is 30s, it cannot adjust it properly
- **Solve, Don't Punt Rule**: Handle exceptions in Python code, don't let scripts crash
- Scripts return machine-verifiable results

---

## Plan-Validate-Execute Pattern

**MANDATORY for High Criticality + Low Variability tasks** (migrations, security operations, compliance checks):

**Phase 1: Planning**
- Agent generates `plan.json` with structured action list
- Each action includes: purpose, target, rollback strategy

**Phase 2: Validation**
- Execute `scripts/validate_plan.py` script
- Validates: syntax, permissions, dependencies, reversibility
- Returns machine-verifiable success/failure code
- **NO EXECUTION without validation success**

**Phase 3: Execution**
- Only proceeds if validation passes
- Each step logged with checkpoints
- Automatic rollback on failure

---

## Trust the Agent's Native Capacities

The agent already knows how to:
- Read and write files
- Run bash commands
- Parse data structures
- Format output
- Organize directories
- Search and analyze code

**Question to ask**: "Can the agent do this with existing tools?"

If yes → Let the agent write it directly
If no → Provide a script (rare)

---

## Writing Style Requirements

### Imperative/Infinitive Form

Write using verb-first instructions, not second person:

**Correct (imperative)**:
```
To create a hook, define the event type.
Configure the MCP server with authentication.
Validate settings before use.
```

**Incorrect (second person)**:
```
You should create a hook by defining the event type.
You need to configure the MCP server.
You must validate settings before use.
```

### Third-Person in Description

The frontmatter description must use third person:

**Correct**:
```yaml
description: This skill should be used when the user asks to "create X", "configure Y"...
```

**Incorrect**:
```yaml
description: Use this skill when you want to create X...
description: Load this skill when user asks...
```

---

## File References

When referencing files in your customization:

- Use relative paths from the root
- Keep file references one level deep from main file
- Avoid deeply nested chains (>1 level)

**Correct**:
```markdown
See [the guide](references/api.md)
Run `scripts/deploy.sh`
```

**Incorrect**:
```markdown
See [the guide](references/api.md)  # leading slash
See [guide](references/subdir/api.md)  # nested
```

---

## Anti-Patterns to Avoid

### Development Anti-Patterns

- **Deep Nesting** - `references/v1/setup/config.md` → Flatten to `references/setup-config.md`
- **Vague Description** - "Helps with coding." → Use clear capability + use case
- **Over-Engineering** - Scripts for simple tasks → Use Native-First Principle
- **Code Blocks in Body** - Large code blocks in SKILL.md → Move to examples/ or scripts/

### Common Anti-Patterns

- **The "Kitchen Sink"** - One skill tries to do everything → Split into focused, single-purpose skills
- **The "Indecisive Orchestrator"** - Too many paths, unclear direction → Pick a primary use case
- **The "Pretend Executor"** - Scripts that require constant guidance → Use guided workflows instead
- **The "Argumentative Consultant"** - Opinions without expertise → Back claims with references and examples

### Mega-Skill Anti-Pattern
- Problem: Multiple unrelated domains
- Failure: Poor activation, context bloat
- Solution: Atomic boundaries + pipeline orchestration

### Script Envy Anti-Pattern
- Problem: Using scripts for operations Claude natively handles
- Example: Creating a script to read a file when `Read` tool exists
- Solution: Only use scripts for **complex** operations (APIs, transformations, specialized tools)

### Iteration-Heavy Anti-Pattern
- Problem: Customization design that requires repeated clarification cycles
- Example: "Ask user for each step" vs. "Execute complete workflow"
- Impact: Burns through quota rapidly (~15 calls per prompt)
- Solution: Encode decision trees and constraints in customization; use AskUserQuestion only for genuine unknowns
