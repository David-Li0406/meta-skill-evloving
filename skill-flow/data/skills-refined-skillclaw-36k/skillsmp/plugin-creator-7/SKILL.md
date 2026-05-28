---
name: plugin-creator
description: 'Orchestrates specialized agents to create high-quality Claude Code plugins. Delegates to researcher agents for domain knowledge, Explore agents for code discovery, validation agents for official docs verification, and review agents for quality checks. Use when creating new plugins or improving existing ones.'
---

# Claude Code Plugin Creator - Agentic Orchestration Workflow

This skill orchestrates specialized agents through a comprehensive plugin creation workflow. The orchestrator (you) delegates to sub-agents for research, discovery, validation, and implementation - never performing these tasks directly.

**Workflow Diagram**: See [workflow-diagram.md](./references/workflow-diagram.md) for mermaid flowcharts of the complete plugin creation flow.

---

## Orchestration Principles

<orchestration_rules>

**The orchestrator MUST delegate, not execute.**

| Task Type              | Delegate To           | Never Do Directly         |
| ---------------------- | --------------------- | ------------------------- |
| Domain research        | Explore agent         | Read docs yourself        |
| Code pattern discovery | Explore agent         | Grep/search yourself      |
| Official docs fetch    | WebFetch or Explore   | Assume from training data |
| Schema validation      | validation scripts    | Manually check fields     |
| Quality review         | plugin-assessor agent | Review your own work      |
| Documentation writing  | plugin-docs-writer    | Write README yourself     |

**Why delegation matters:**

1. Sub-agents have focused context and specialized prompts
2. Delegation creates audit trails of verified information
3. Prevents hallucination by requiring source verification
4. Enables parallel work and thoroughness

</orchestration_rules>

---

## Artifact System

<artifact_system>

**Maintain structured artifacts for crash recovery, audit trails, and context management.**

Create a work directory for each plugin project:

```text
.claude/plugin-work/{plugin-name}/
├── PROJECT.md                # Vision and goals (always loaded)
├── REQUIREMENTS.md           # Scoped deliverables
├── STATE.md                  # Decisions, blockers, current position
├── discuss-CONTEXT.md        # User preferences captured in discussion
├── research-FINDINGS.md      # 4-way parallel research results
├── design-PLAN.md            # Architecture with XML task specs
├── validation-REPORT.md      # Multi-layer verification results
└── SUMMARY.md                # Completion record
```

**STATE.md format** (persists across sessions):

```markdown
# Plugin State: {plugin-name}
Last Updated: {ISO timestamp}

## Decisions Made
- {decision}: {rationale}

## Current Position
- Phase: {current phase}
- Status: IN_PROGRESS | BLOCKED | COMPLETE

## Blockers
- {blocker}: {what's needed}

## Deviations from Plan
- {change}: {why}
```

**Recovery:** Read STATE.md to restore context after session crash.

</artifact_system>

---

## Parallel Agent Spawning

<parallel_execution>

**Spawn independent agents simultaneously to maximize throughput.**

**4-Way Parallel Research Pattern:**

```text
# Spawn all four researchers in a single message:

Task(subagent_type="Explore", prompt="EXISTING PLUGINS: Search plugins/ and ~/.claude/skills/ for similar functionality...")
Task(subagent_type="Explore", prompt="CLAUDE CODE FEATURES: What plugin capabilities exist? Dynamic context, hooks, MCP, LSP...")
Task(subagent_type="Explore", prompt="ARCHITECTURE PATTERNS: How do well-structured plugins organize skills, agents, references...")
Task(subagent_type="general-purpose", prompt="PITFALLS: Fetch official docs, identify common mistakes, schema gotchas...")
```

**All four run concurrently. Merge results into research-FINDINGS.md before planning.**

**Parallelization opportunities:**

| Phase         | Parallel Tasks                                             |
| ------------- | ---------------------------------------------------------- |
| Research      | 4 researchers (existing, features, architecture, pitfalls) |
| Validation    | Scripts + docs verification + quality assessment           |
| Documentation | README + skills.md + config guide                          |

**Sequential requirements:**

- Discussion phase captures preferences BEFORE research
- Design phase depends on merged research findings
- Implementation depends on approved design
- Plan checker must pass BEFORE execution

</parallel_execution>

---

## Phase 0: RT-ICA Prerequisite Check

<prerequisite_checkpoint>

**STOP. Before creating any plugin, perform RT-ICA assessment.**

Invoke the `rt-ica` skill to verify prerequisites:

```text
RT-ICA SUMMARY
==============

Goal:
- Create a Claude Code plugin for [purpose]

Success Output:
- Functional plugin that [specific outcome]

Conditions (reverse prerequisites):
1. Purpose clarity | Requires: Clear problem statement | Why: Determines plugin scope
2. Target users | Requires: Who will use this | Why: Shapes UX decisions
3. Component selection | Requires: Skills vs Agents vs Hooks | Why: Architecture
4. Existing solutions | Requires: Check for similar plugins | Why: Avoid duplication
5. Source material | Requires: Documentation/APIs to encode | Why: Content accuracy
6. Verification method | Requires: How to test the plugin works | Why: Quality gate

Verification:
- [Check each condition: AVAILABLE / DERIVABLE / MISSING]

Decision:
- [APPROVED / BLOCKED]
```

**IF BLOCKED**: Request missing information before proceeding.

**IF APPROVED**: Continue to Discussion phase.

</prerequisite_checkpoint>

---

## Phase 0.5: Discussion (Capture Preferences)

<discussion_phase>

**BEFORE research, identify gray areas and capture user preferences.**

Ask targeted questions to eliminate ambiguity:

**For skill-focused plugins:**

- Activation triggers: When should Claude auto-load vs user-invoke?
- Tool restrictions: Full access or limited tools?
- Output format: Verbose explanations or terse instructions?
- Reference structure: Inline content or progressive disclosure?

**For agent-focused plugins:**

- Delegation scope: What tasks should agents handle?
- Return format: Summaries or detailed reports?
- Error handling: Retry, escalate, or fail fast?

**For hook-focused plugins:**

- Trigger events: Which tool/session events matter?
- Hook type: Command, prompt, or agent verification?
- Timeout handling: Fail silently or block?

**Save preferences to `discuss-CONTEXT.md`:**

```markdown
# Plugin Discussion: {plugin-name}
Date: {ISO timestamp}

## Scope Decisions
- {question}: {user preference}

## UX Preferences
- Invocation: {user-invoked | model-invoked | both}
- Verbosity: {terse | balanced | verbose}

## Technical Choices
- {choice}: {preference with rationale}
```

**These preferences guide all subsequent research and planning.**

</discussion_phase>

---

## Phase 1: Research (4-Way Parallel)

<research_phase>

**Spawn 4 parallel researchers in a single message.** Each investigates a different domain:

```text
# Launch all four simultaneously:

Task(subagent_type="Explore", prompt="
RESEARCHER 1: EXISTING SOLUTIONS
Search for plugins/skills similar to {plugin-name}:
- plugins/ directory
- ~/.claude/skills/
- GitHub repos with Claude Code plugins
REPORT: What exists, gaps to fill, patterns to follow/avoid")

Task(subagent_type="Explore", prompt="
RESEARCHER 2: CLAUDE CODE FEATURES
What capabilities should this plugin use?
- Dynamic context injection (!`command`)
- Subagent execution (context: fork)
- Hooks (which events?)
- MCP/LSP integration opportunities
REPORT: Recommended features with rationale")

Task(subagent_type="Explore", prompt="
RESEARCHER 3: ARCHITECTURE PATTERNS
How do well-structured plugins organize?
- Skill directory structure
- Reference file patterns
- Agent definitions
- Hook configurations
REPORT: Recommended structure based on similar plugins")

Task(subagent_type="general-purpose", prompt="
RESEARCHER 4: PITFALLS & OFFICIAL DOCS
Fetch https://code.claude.com/docs/en/plugins-reference.md
Fetch https://code.claude.com/docs/en/skills.md
IDENTIFY:
- Schema requirements (comma-separated strings NOT arrays)
- Common mistakes
- Deprecations or new features
REPORT: Gotchas to avoid, schema requirements")
```

**Merge all 4 reports into `research-FINDINGS.md` before proceeding to Design.**

### Research Findings Format

```markdown
# Research Findings: {plugin-name}
Date: {ISO timestamp}

## 1. Existing Solutions
{Researcher 1 findings}

## 2. Recommended Features
{Researcher 2 findings}

## 3. Architecture Patterns
{Researcher 3 findings}

## 4. Pitfalls & Requirements
{Researcher 4 findings}

## Synthesis
- Key insights: {combined learnings}
- Recommended approach: {synthesis}
```

</research_phase>

---

## Phase 2: Design (Plan + Verify Loop)

<design_phase>

**Design phase uses a PLAN → CHECK → ITERATE loop until verification passes.**

### 2a. Generate Plan with XML Task Specs

**Delegate to Plan agent:**

```
Task(
  subagent_type="Plan",
  prompt="Design plugin: {plugin-name}

  INPUTS:
  - User preferences: {from discuss-CONTEXT.md}
  - Research findings: {from research-FINDINGS.md}

  OUTPUT: XML task specifications for atomic implementation:

  <task id='1' type='auto'>
    <name>Create plugin.json manifest</name>
    <files>.claude-plugin/plugin.json</files>
    <action>Create manifest with name, version, description, skills array</action>
    <verify>jq '.name' .claude-plugin/plugin.json returns plugin name</verify>
    <done>Valid plugin.json exists with all required fields</done>
  </task>

  <task id='2' type='auto'>
    <name>Create main SKILL.md</name>
    <files>skills/{skill-name}/SKILL.md</files>
    <action>Create skill with frontmatter and core instructions</action>
    <verify>grep -q '^---' skills/{skill-name}/SKILL.md</verify>
    <done>SKILL.md has valid frontmatter and content under 500 lines</done>
  </task>

  Generate 2-5 atomic tasks. Each task must have:
  - Single responsibility
  - Testable <verify> command
  - Clear <done> criteria"
)
```

### 2b. Plan Checker Verification

**BEFORE execution, verify the plan achieves goals:**

```
Task(
  subagent_type="general-purpose",
  prompt="PLAN CHECKER: Verify this plan achieves the plugin goals.

  PLAN: {generated XML tasks}
  REQUIREMENTS: {from discuss-CONTEXT.md}
  RESEARCH: {key findings}

  VERIFY:
  1. Do tasks cover all required components?
  2. Are tasks truly atomic (single responsibility)?
  3. Are <verify> commands actually testable?
  4. Are there gaps between tasks?
  5. Does sequence respect dependencies?

  OUTPUT:
  - PASS: Plan is ready for execution
  - FAIL: {specific issues to fix}

  If FAIL, return to planner with feedback."
)
```

**Loop until plan checker returns PASS.**

### 2c. Save Approved Plan

Save to `design-PLAN.md`:

```markdown
# Design Plan: {plugin-name}
Date: {ISO timestamp}
Status: APPROVED

## Tasks

<task id='1'>...</task>
<task id='2'>...</task>

## Verification
Plan checker: PASS
Reviewer: {agent ID}
```

</design_phase>

---

## Phase 3: Implementation (Atomic Execution)

<implementation_phase>

**Execute each XML task atomically with per-task commits.**

### 3a. Task Execution Pattern

For each `<task>` in the approved plan:

```
Task(
  subagent_type="general-purpose",
  prompt="EXECUTOR: Implement this single task.

  <task id='{N}'>
    <name>{task name}</name>
    <files>{target files}</files>
    <action>{implementation instructions}</action>
    <verify>{test command}</verify>
    <done>{success criteria}</done>
  </task>

  CONTEXT:
  - User preferences: {from discuss-CONTEXT.md}
  - Research findings: {relevant sections}

  EXECUTE:
  1. Implement the <action>
  2. Run the <verify> command
  3. Confirm <done> criteria met

  OUTPUT:
  - Files created/modified
  - Verification result: PASS/FAIL
  - If FAIL: what went wrong"
)
```

### 3b. Atomic Git Commits

**Each task gets its own commit immediately after completion:**

```bash
git add {files from task}
git commit -m "task-{N}: {task name}"
```

**Benefits:**

- `git bisect` locates exact failing task
- Individual tasks revertable
- Clear history for debugging

### 3c. Parallel vs Sequential Execution

**Independent tasks** (no shared files): Execute in parallel

```text
# Tasks 1, 2, 3 have no dependencies - spawn all:
Task(prompt="EXECUTOR: task 1...")
Task(prompt="EXECUTOR: task 2...")
Task(prompt="EXECUTOR: task 3...")
```

**Dependent tasks** (task 2 needs task 1's output): Execute sequentially

### 3d. Scaffolding Script Option

For simple plugins, use the scaffolding script:

```bash
uv run scripts/create_plugin.py create my-plugin -d "Description" -s my-skill -o ./plugins
```

The script self-validates created files.

</implementation_phase>

---

## Phase 3b: Advanced Features Reference

The `create_plugin.py` script creates validated plugin structure:

```bash
# Create plugin with skill
uv run scripts/create_plugin.py create my-plugin -d "Description" -s my-skill -o ./plugins

# Create with multiple components
uv run scripts/create_plugin.py create my-plugin \
    -d "Multi-component plugin" \
    -s skill1 -s skill2 \
    -a agent1 \
    --hooks \
    -o ./plugins
```

The script self-validates all created files (CoVe pattern).

### Option B: Manual Implementation

<implementation_structure>

**Directory structure:**

```text
my-plugin/
├── .claude-plugin/           # REQUIRED: metadata directory
│   └── plugin.json          # REQUIRED: only file in .claude-plugin/
├── agents/                   # Optional: agent definitions (.md)
├── skills/                   # Optional: skill directories
│   └── my-skill/
│       ├── SKILL.md
│       └── references/      # Optional: detailed reference docs
├── hooks/                    # Optional: hook configurations
│   └── hooks.json
├── .mcp.json                # Optional: MCP server definitions
├── scripts/                 # Optional: helper scripts
├── LICENSE
└── README.md
```

**Critical Rules:**

1. `.claude-plugin/` contains ONLY `plugin.json`
2. All components go at plugin root, NOT inside `.claude-plugin/`
3. Commands in plugins are deprecated - use skills instead

</implementation_structure>

### plugin.json Schema

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does and trigger keywords",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "repository": "https://github.com/you/my-plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": ["./skills/my-skill"]
}
```

| Field          | Type           | Required | Purpose                                  |
| -------------- | -------------- | -------- | ---------------------------------------- |
| `name`         | string         | Yes      | Kebab-case identifier, max 64 chars      |
| `version`      | string         | No       | Semantic versioning (X.Y.Z)              |
| `description`  | string         | No       | Max 1024 chars, include trigger keywords |
| `author`       | object         | No       | `{name, email?, url?}`                   |
| `keywords`     | array          | No       | Discovery tags (JSON array)              |
| `agents`       | string\|array  | No       | Path(s) to agent files                   |
| `skills`       | string\|array  | No       | Path(s) to skill directories             |
| `hooks`        | string\|object | No       | Hook config path or inline               |
| `mcpServers`   | string\|object | No       | MCP config path or inline                |
| `lspServers`   | string\|object | No       | LSP config path or inline                |
| `outputStyles` | string\|array  | No       | Path(s) to output style files            |

**Source**: <https://code.claude.com/docs/en/plugins-reference.md#plugin-manifest-schema>

### SKILL.md Frontmatter

```yaml
---
name: my-skill
description: 'Detailed description including trigger keywords. Use when [situation].'
allowed-tools: Read, Grep, Glob
---
```

| Field                      | Type                   | Default         | Purpose                                    |
| -------------------------- | ---------------------- | --------------- | ------------------------------------------ |
| `name`                     | string                 | directory name  | Display name (lowercase, hyphens, max 64)  |
| `description`              | string                 | first paragraph | When to use; for auto-invocation           |
| `argument-hint`            | string                 | none            | Autocomplete hint (e.g., `[issue-number]`) |
| `allowed-tools`            | comma-separated string | none            | Tools without permission prompts           |
| `model`                    | string                 | default         | Model when skill is active                 |
| `context`                  | string                 | none            | `fork` for isolated subagent               |
| `agent`                    | string                 | general-purpose | Subagent type when `context: fork`         |
| `user-invocable`           | boolean                | true            | `false` hides from `/` menu                |
| `disable-model-invocation` | boolean                | false           | `true` prevents Claude auto-loading        |

**CRITICAL**: YAML frontmatter fields like `allowed-tools` MUST be comma-separated strings, NOT arrays.

**Source**: <https://code.claude.com/docs/en/skills.md>

---

## Phase 3b: Advanced Features Reference

<advanced_features>

This section documents powerful plugin capabilities the AI MUST consider when designing plugins. These features can transform a basic plugin into an exceptional one.

### Dynamic Context Injection

The `!`command`` syntax runs shell commands BEFORE skill content is sent to Claude. Output replaces the placeholder.

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh:*)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

**How it works:**

1. Each `!`command`` executes immediately (before Claude sees anything)
2. Output replaces the placeholder in skill content
3. Claude receives fully-rendered prompt with actual data

**Use cases:**

- Inject git status, branch info, or PR details
- Include current date/time or environment info
- Fetch live API data for context
- Run diagnostics before a task

**Source**: <https://code.claude.com/docs/en/skills.md#inject-dynamic-context>

### String Substitutions

Skills support these variables:

| Variable                | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| `$ARGUMENTS`            | Text passed when invoking the skill                     |
| `${CLAUDE_SESSION_ID}`  | Current session ID (for logging, correlating output)    |
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin directory (hooks, MCP, scripts) |

**Example:**

```yaml
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### Running Skills in Subagents

Add `context: fork` to run a skill in an isolated subagent. The skill content becomes the subagent's prompt.

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

**When to use:**

- Long-running research tasks
- Tasks that need isolation from main conversation
- Read-only exploration (use Explore agent)
- Complex planning (use Plan agent)

**Available agent types:**

- `Explore` - Read-only tools for codebase exploration
- `Plan` - Architecture and planning tasks
- `general-purpose` - Full tool access

**Source**: <https://code.claude.com/docs/en/skills.md#run-skills-in-a-subagent>

### Visual Output - Bundled Scripts

Skills can bundle scripts in ANY language to generate visual output (HTML files that open in browser).

**Example: Codebase Visualizer**

```text
my-skill/
├── SKILL.md
└── scripts/
    └── visualize.py
```

**SKILL.md:**

```yaml
---
name: codebase-visualizer
description: Generate interactive tree visualization of codebase
allowed-tools: Bash(python:*)
---

# Codebase Visualizer

Run the visualization script from project root:

\`\`\`bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
\`\`\`

Creates codebase-map.html and opens it in browser.
```

**Pattern:** Script does heavy lifting, Claude orchestrates.

**Use cases:**

- Dependency graphs
- Test coverage reports
- API documentation
- Database schema visualizations
- Performance dashboards

**Source**: <https://code.claude.com/docs/en/skills.md#generate-visual-output>

### Hook Configuration

Plugins can provide event handlers that respond to Claude Code events.

**Hook types:**

| Type      | Purpose                           |
| --------- | --------------------------------- |
| `command` | Execute shell commands or scripts |
| `prompt`  | Evaluate a prompt with LLM        |
| `agent`   | Run agentic verifier with tools   |

**Available events:**

| Event                | When                      | Has Matcher |
| -------------------- | ------------------------- | ----------- |
| `PreToolUse`         | Before tool executes      | Yes         |
| `PostToolUse`        | After tool succeeds       | Yes         |
| `PostToolUseFailure` | After tool fails          | Yes         |
| `Stop`               | Claude finishes           | No          |
| `UserPromptSubmit`   | User submits prompt       | No          |
| `SessionStart`       | Session begins/resumes    | Yes         |
| `SessionEnd`         | Session ends              | No          |
| `SubagentStart`      | Subagent starts           | Yes         |
| `SubagentStop`       | Subagent stops            | Yes         |
| `Setup`              | Maintenance/init flags    | No          |
| `PreCompact`         | Before context compaction | No          |

**Example hooks/hooks.json:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**IMPORTANT:** Always use `${CLAUDE_PLUGIN_ROOT}` for script paths - it resolves to the correct cached location.

**Source**: <https://code.claude.com/docs/en/hooks.md>

### MCP Server Integration

Plugins can bundle MCP servers for external tool integration.

**Location:** `.mcp.json` at plugin root or inline in plugin.json

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

**Source**: <https://code.claude.com/docs/en/mcp.md>

### LSP Server Integration

Plugins can provide Language Server Protocol servers for code intelligence.

**Location:** `.lsp.json` at plugin root

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**LSP provides:**

- Instant diagnostics (errors/warnings after each edit)
- Code navigation (go to definition, find references)
- Type information and documentation

**Note:** Users must install the language server binary separately.

**Source**: <https://code.claude.com/docs/en/plugins-reference.md#lsp-servers>

### Plugin Caching Behavior

**Critical knowledge for plugin developers:**

Claude Code COPIES plugins to a cache directory rather than using them in-place.

**Implications:**

1. External files outside plugin directory are NOT copied
2. Use symlinks if you need external dependencies (symlinks are followed during copy)
3. `${CLAUDE_PLUGIN_ROOT}` always points to correct cached location

**Source**: <https://code.claude.com/docs/en/plugins-reference.md#plugin-caching-and-file-resolution>

### Path Behavior Rules

**Custom paths SUPPLEMENT default directories, they don't REPLACE them.**

```json
{
  "skills": ["./custom/skills/"]
}
```

This adds custom skills IN ADDITION TO `skills/` directory.

- All paths must be relative and start with `./`
- Multiple paths can be arrays for flexibility
- Same naming/namespacing rules apply

### Skill Invocation Control

Control who can invoke skills:

| Frontmatter                      | User | Claude | Use Case                    |
| -------------------------------- | ---- | ------ | --------------------------- |
| (default)                        | Yes  | Yes    | Most skills                 |
| `disable-model-invocation: true` | Yes  | No     | Workflows with side effects |
| `user-invocable: false`          | No   | Yes    | Background knowledge only   |

**Example - deploy skill only user can trigger:**

```yaml
---
name: deploy
description: Deploy application to production
disable-model-invocation: true
---
```

### Extended Thinking

Include "ultrathink" anywhere in skill content to enable extended thinking mode.

</advanced_features>

---

## Phase 4: Validation (Multi-Layer Verification)

<validation_phase>

**Four verification layers prevent bugs from reaching completion.**

### Layer 1: Automated Script Validation

```bash
# Run in parallel:
uv run scripts/create_plugin.py validate ./plugins/my-plugin
uv run scripts/validate_frontmatter.py batch ./plugins/my-plugin
```

### Layer 2: Official Docs Verification

```
Task(
  subagent_type="general-purpose",
  prompt="VERIFIER: Check plugin against official docs.

  FETCH:
  - https://code.claude.com/docs/en/plugins-reference.md
  - https://code.claude.com/docs/en/skills.md

  COMPARE ./plugins/my-plugin against schema requirements.

  REPORT:
  - PASS: All files compliant
  - FAIL: {specific violations with file:line}"
)
```

### Layer 3: Quality Assessment

```
Task(
  subagent_type="plugin-assessor",
  prompt="Assess ./plugins/my-plugin for marketplace readiness.

  CHECK:
  - Structural correctness
  - Frontmatter optimization
  - Documentation completeness
  - Cross-reference integrity

  SCORE: 1-10 with specific issues"
)
```

### Layer 4: Automatic Debugging (if failures)

**If any layer returns FAIL, spawn debugger:**

```
Task(
  subagent_type="general-purpose",
  prompt="DEBUGGER: Diagnose validation failure.

  FAILURE: {failure details from verifier}
  PLUGIN: ./plugins/my-plugin

  INVESTIGATE:
  1. Read the failing file(s)
  2. Identify root cause
  3. Generate fix plan

  OUTPUT:
  <fix>
    <file>{path}</file>
    <issue>{what's wrong}</issue>
    <action>{how to fix}</action>
  </fix>

  Return fix plan for re-execution."
)
```

**Loop: Fix → Re-validate → until all layers PASS.**

### Save Validation Report

Save to `validation-REPORT.md`:

```markdown
# Validation Report: {plugin-name}
Date: {ISO timestamp}

## Layer 1: Scripts
Status: PASS/FAIL
Output: {script output}

## Layer 2: Official Docs
Status: PASS/FAIL
Findings: {compliance details}

## Layer 3: Quality
Score: {N}/10
Issues: {list}

## Layer 4: Debug Cycles
Iterations: {N}
Fixes applied: {list}

## Final Status: PASS
```

</validation_phase>

---

## Phase 5: Documentation (Delegate to Docs Agent)

<documentation_phase>

**Delegate to plugin-docs-writer agent:**

```
Task(
  subagent_type="plugin-docs-writer",
  prompt="Generate comprehensive documentation for the plugin at ./plugins/my-plugin.

  CREATE:
  - README.md with installation, usage, and examples
  - docs/skills.md if multiple skills
  - Configuration guide if hooks or MCP servers included

  ENSURE:
  - All features documented
  - Installation instructions accurate
  - Examples are runnable"
)
```

</documentation_phase>

---

## Phase 6: Final Verification

<final_checkpoint>

**STOP. Before claiming complete, verify with evidence.**

### Invoke verify Skill

```text
VERIFICATION SUMMARY:
Task Type: FEATURE
Works Check: [PASS/FAIL] - Evidence: validation script output
Quality Gates: [PASS/FAIL] - Evidence: plugin-assessor report
Docs Check: [PASS/FAIL] - Evidence: README.md exists and accurate
Honesty Check: [PASS/FAIL] - Evidence: all claims cite sources

VERDICT: [COMPLETE / NOT COMPLETE - reason]
```

**Only mark complete when:**

1. All automated validation scripts pass
2. plugin-assessor reports no critical issues
3. Official docs verification found no schema violations
4. All factual claims in skills cite sources

</final_checkpoint>

---

## Quick Reference: Agent Delegation

| Phase    | Agent Type           | Purpose                                   |
| -------- | -------------------- | ----------------------------------------- |
| Research | `Explore`            | Code discovery, pattern analysis          |
| Research | `general-purpose`    | Fetch and analyze official documentation  |
| Design   | `Plan`               | Architecture decisions, content structure |
| Validate | validation scripts   | Schema and structure validation           |
| Validate | `plugin-assessor`    | Quality assessment                        |
| Document | `plugin-docs-writer` | README and documentation generation       |

---

## Tooling

| Script                              | Purpose                             |
| ----------------------------------- | ----------------------------------- |
| `scripts/create_plugin.py create`   | Scaffold new plugin with validation |
| `scripts/create_plugin.py validate` | Check existing plugin structure     |
| `scripts/validate_frontmatter.py`   | Validate frontmatter against schema |

Scripts use PEP 723 inline metadata - dependencies install automatically via `uv run`.

---

## Sources

Official Claude Code documentation (verified January 2026):

- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference) - Complete schema
- [Skills Documentation](https://code.claude.com/docs/en/skills) - SKILL.md format
- [Hooks Reference](https://code.claude.com/docs/en/hooks) - Hook configuration
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) - Distribution
- [Documentation Index](https://code.claude.com/docs/llms.txt) - Check for new features
