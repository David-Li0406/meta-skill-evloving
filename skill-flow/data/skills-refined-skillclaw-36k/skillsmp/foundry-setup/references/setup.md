# Foundry Setup - Detailed Phase Instructions

## Phase 1: Pre-flight Checks

Run these checks in parallel to verify the environment:

1. Call `mcp__plugin_foundry_foundry-mcp__health action="liveness"` to verify MCP server connectivity
2. Call `mcp__plugin_foundry_foundry-mcp__environment action="verify-toolchain"` to check required tools (Python, git)
3. Call `mcp__plugin_foundry_foundry-mcp__environment action="verify-env"` to validate runtime versions

Present results in a status table:

```
## Pre-flight Checks

| Check | Status | Details |
|-------|--------|---------|
| MCP Server | [✓/✗] | foundry-mcp responding / connection failed |
| Python | [✓/✗] | version number |
| Git | [✓/✗] | version number |
```

**If MCP server check fails:** Stop and explain that foundry-mcp must be configured. Point to installation instructions:
- PyPI: `pip install foundry-mcp`
- Or: `uvx foundry-mcp`
- Configure in Claude Code MCP settings

**Recommended MCP configuration:**

```json
{
  "mcpServers": {
    "foundry-mcp": {
      "command": "python",
      "args": ["-m", "foundry_mcp.server"]
    }
  }
}
```

**If other checks fail:** Warn but continue - some features may not work.

**If `--check` or `--preflight` flag was provided:** Stop here. Display the pre-flight results summary and exit. Do not continue to Phase 2 or beyond.

---

## Phase 1.5: Permission Management

Claude Code requires explicit permissions for plugin tools. This phase automatically detects, compares, and configures the required permissions.

### Step 1: Run Permission Check

Execute the permission check script:

```bash
bash -c 'cd "$0" && WORKSPACE_DIR="$1" ./scripts/setup-permissions --diff' "${CLAUDE_PLUGIN_ROOT}" "$PWD"
```

Parse the JSON output to determine the permission status.

### Step 2: Handle Based on Status

**If status is `complete`:**

Display:
> "Permissions are configured correctly. All required plugin permissions are present."

Continue to Phase 2.

---

**If status is `no_file`:**

Explain:
> "The `.claude/settings.local.json` file doesn't exist in this project. This file controls which tools Claude Code can use without prompting.
>
> The plugin requires permissions for:
> - All foundry-mcp MCP tools
> - Git commands (status, diff, log, etc.)
> - Test execution (pytest)
> - AI provider CLIs (codex, claude, gemini, cursor-agent, opencode)
> - Read/write access to specs/ directories"

Use `AskUserQuestion`:
- Question: "Create `.claude/settings.local.json` with plugin permissions?"
- Options:
  - "Yes, create the file (recommended)"
  - "No, I'll configure this manually"

**If "Yes":** Run the script with `--create`:
```bash
bash -c 'cd "$0" && WORKSPACE_DIR="$1" ./scripts/setup-permissions --create' "${CLAUDE_PLUGIN_ROOT}" "$PWD"
```

Display: "Created `.claude/settings.local.json` with plugin permissions."

**If "No":** Ask if they want to continue without permissions, then proceed or exit.

---

**If status is `invalid`:**

Explain:
> "Found `.claude/settings.local.json` but it contains invalid JSON. The file will be backed up before replacement."

Use `AskUserQuestion`:
- Question: "Replace invalid file with valid permissions? (Original will be backed up)"
- Options:
  - "Yes, backup and replace"
  - "No, I'll fix it manually"

**If "Yes":** Run the script with `--apply` (which backs up invalid files automatically).

---

**If status is `missing`:**

Display the categorized diff from `missing_by_category` as a table:

```
## Permission Comparison

| Category | Status |
|----------|--------|
| MCP Tools | {count or checkmark} |
| Git Commands | {count or checkmark} |
| Testing | {count or checkmark} |
| Foundry CLI | {count or checkmark} |
| AI Providers | {count or checkmark} |
| Specs Write | {count or checkmark} |
| Specs Edit | {count or checkmark} |
| Deny Rules | {count or checkmark} |
```

For categories with missing permissions, show the specific permissions:

```
**Missing Git Commands:**
+ Bash(git status:*)
+ Bash(git diff:*)
...
```

If `user_custom` is not empty, note:
> "Your custom permissions will be preserved: {list}"

Use `AskUserQuestion`:
- Question: "How would you like to update permissions?"
- Options:
  - "Add all missing permissions (recommended)"
  - "Skip - I'll update manually"

**If "Add all missing":** Run the script with `--apply`:
```bash
bash -c 'cd "$0" && WORKSPACE_DIR="$1" ./scripts/setup-permissions --apply' "${CLAUDE_PLUGIN_ROOT}" "$PWD"
```

Display: "Permissions updated! Added {X} allow permissions and {Y} deny rules."

**If "Skip":** Warn that some features may require manual approval, then continue.

---

## Phase 2: Workspace Setup

1. Call `mcp__plugin_foundry_foundry-mcp__environment action="detect-topology"` to analyze the project structure
2. Call `mcp__plugin_foundry_foundry-mcp__spec action="list"` to check for existing specifications

### If specs/ directory does not exist:

Use `AskUserQuestion` to ask:
- Question: "Would you like to initialize the specs directory structure?"
- Options: "Yes, initialize" / "No, skip"

If yes: Call `mcp__plugin_foundry_foundry-mcp__environment action="init-workspace"` to create:
- specs/active/
- specs/pending/
- specs/completed/
- specs/archived/

### If foundry-mcp.toml does not exist:

Use `AskUserQuestion` to ask:
- Question: "Would you like to create a foundry-mcp.toml configuration file?"
- Options: "Yes, create with defaults" / "No, skip"

If yes: Call `mcp__plugin_foundry_foundry-mcp__environment action="setup"` with `dry_run=false`

Report what was created or skipped.

---

## Phase 2.1: Context Configuration

**Only run this phase if foundry-mcp.toml was created in Phase 2.**

This phase configures the `[context]` section for context monitoring behavior.

### Step 1: Check Existing Configuration

Read the `foundry-mcp.toml` file and check if it already contains a `[context]` section.

**If `[context]` section exists:** Skip this phase and display:
> "Context configuration already present in foundry-mcp.toml. Your existing settings are preserved."

Continue to Phase 2.2.

### Step 2: Add Context Section

Append the context section after `[features]`:

```toml

[context]
# Auto-compact mode affects context percentage calculation
# true (default): denominator is 155k (Claude compacts before hitting limit)
# false: denominator is 200k (full context window, no auto-compaction)
auto_compact = true
```

Use the Edit tool to update the file.

### Step 3: Display Results

```
## Context Configuration

Enabled context settings:
- auto_compact: true (context monitor uses 155k denominator)

Note: Set auto_compact = false in foundry-mcp.toml if you've disabled auto-compaction in Claude Code settings (uses 200k denominator).
```

---

## Phase 2.2: Implement Configuration

**Only run this phase if foundry-mcp.toml exists (either created in Phase 2 or already present).**

This phase configures the `[implement]` section for the `foundry-implement` command's default execution mode.

### Step 1: Check Existing Configuration

Read the `foundry-mcp.toml` file and check if it already contains an `[implement]` section.

**If `[implement]` section exists:** Skip this phase and display:
> "Implement configuration already present in foundry-mcp.toml. Your existing settings are preserved."

Continue to Phase 2.5.

### Step 2: Ask User for Preferred Defaults

Use `AskUserQuestion` to determine preferred execution mode:

```
"How should foundry-implement behave by default?"
Options:
- "Interactive, inline (Recommended)" → auto=false, delegate=false, parallel=false
- "Autonomous, inline" → auto=true, delegate=false, parallel=false
- "Interactive, delegated" → auto=false, delegate=true, parallel=false
- "Autonomous, delegated" → auto=true, delegate=true, parallel=false
- "Autonomous, parallel" → auto=true, delegate=true, parallel=true
```

### Step 3: Append Implement Section to TOML

Read the existing `foundry-mcp.toml` file content.

Append the implement configuration section after `[workflow]`:

```toml

[implement]
# Default flags for foundry-implement command (can be overridden via CLI flags)
auto = {auto_value}      # --auto: skip prompts between tasks
delegate = {delegate_value}  # --delegate: use subagent(s) for implementation
parallel = {parallel_value}  # --parallel: run subagents concurrently (implies delegate)
```

Use the Edit tool to update the file.

### Step 4: Display Results

```
## Implement Configuration

Configured foundry-implement defaults:

| Flag | Default | Effect |
|------|---------|--------|
| --auto | {auto_value} | Skip prompts between tasks |
| --delegate | {delegate_value} | Use subagent(s) for implementation |
| --parallel | {parallel_value} | Run subagents concurrently |

You can override these via CLI flags, e.g., `foundry-implement --auto --delegate`.
```

---

## Phase 2.5: AI Provider Configuration

**Only run this phase if foundry-mcp.toml was created in Phase 2.**

This phase detects available AI providers and configures the `[consultation]` section for plan reviews and other multi-model features.

### Step 1: Discover Available Providers

Call `mcp__plugin_foundry_foundry-mcp__provider action="list"` to get all registered providers.

Parse the response and filter to providers where `available: true`.

### Step 2: Get Provider Metadata

For each available provider, call in parallel:
```
mcp__plugin_foundry_foundry-mcp__provider action="status" provider_id="<provider_id>"
```

Extract `data.metadata.default_model` from each response.

### Step 3: Build Consultation Priority List

Construct priority entries in format: `[cli]{provider_id}:{default_model}`

Example entries:
- `[cli]gemini:gemini-2.5-flash`
- `[cli]claude:claude-sonnet-4-20250514`
- `[cli]opencode:gpt-4`

Sort entries by provider priority from Step 1 (lower number = higher priority in list).

### Step 4: Append to TOML

Read the existing `foundry-mcp.toml` file.

**If the file already contains `[consultation]`:** Skip this step and inform the user that existing configuration is preserved.

**Otherwise:** Append the consultation section:

```toml

[consultation]
# Auto-generated based on detected providers
# Edit priority order or models as needed
priority = [
    "<entry1>",
    "<entry2>",
]
default_timeout = 300
```

Use the Write tool to save the updated file.

### Step 5: Display Results

Present configured providers in a table:

```
## AI Provider Configuration

Detected {N} available provider(s):

| Provider | Model | Priority |
|----------|-------|----------|
| gemini | gemini-2.5-flash | 1 |
| claude | claude-sonnet-4 | 2 |

Configuration written to foundry-mcp.toml.
```

**If no providers are available:**

```
## AI Provider Configuration

No AI providers detected. The [consultation] section was added with an empty priority list.

To enable multi-model features like plan reviews, install one of:
- gemini CLI: https://github.com/google-gemini/gemini-cli
- opencode CLI: https://github.com/opencode-ai/opencode
- codex CLI: https://github.com/openai/codex

Then re-run `foundry-setup` or manually edit foundry-mcp.toml.
```

---

## Phase 2.6: Research Configuration

**Only run this phase if foundry-mcp.toml exists (either created in Phase 2 or already present).**

This phase configures the `[research]` and `[research.deep]` sections for the research skill (chat, consensus, thinkdeep, ideate, deep workflows).

### Step 1: Check Existing Configuration

Read the `foundry-mcp.toml` file and check if it already contains a `[research]` section.

**If `[research]` section exists:** Skip this phase and display:
> "Research configuration already present in foundry-mcp.toml. Your existing settings are preserved."

Continue to Phase 2.7.

### Step 2: Build Research Configuration

Use the available providers from Phase 2.5 to configure research defaults.

**Format:** Use the same format as consultation: `[cli]provider:model`

Reuse the priority entries already built in Phase 2.5 for the consultation section.

Select the default provider (first entry from consultation priority list).

Build consensus_providers list from all entries in the consultation priority list (same as `[consultation].priority`).

### Step 3: Append Research Section to TOML

Read the existing `foundry-mcp.toml` file content.

Append the research configuration section:

```toml

[research]
# Research tool configuration (chat, consensus, thinkdeep, ideate, deep)
# Uses same format as consultation: "[cli]provider:model"
default_provider = "[cli]{provider}:{model}"
# Same list as [consultation].priority
consensus_providers = [
    "[cli]{provider1}:{model1}",
    "[cli]{provider2}:{model2}",
    ...
]
max_retries = 2
retry_delay = 5.0
fallback_enabled = true
cache_ttl = 3600

[research.deep]
# Deep research workflow settings
max_iterations = 3
max_sub_queries = 5
max_sources_per_query = 5
follow_links = true
max_concurrent = 3
timeout_per_operation = 120
```

Use the Write tool to save the updated file.

### Step 4: Display Results

```
## Research Configuration

Configured research defaults:

| Setting | Value |
|---------|-------|
| Default Provider | [cli]{provider}:{model} |
| Consensus Providers | (same as consultation priority list) |

Deep research defaults:

| Setting | Value |
|---------|-------|
| max_iterations | 3 |
| max_sub_queries | 5 |
| max_sources_per_query | 5 |

Research workflows (chat, consensus, thinkdeep, ideate, deep) are now configured.
```

---

## Phase 2.7: Test Configuration

**Only run this phase if foundry-mcp.toml exists (either created in Phase 2 or already present).**

This phase detects the appropriate test runner for the project and optionally configures the `[test]` section.

### Step 1: Check Existing Configuration

Read the `foundry-mcp.toml` file and check if it already contains a `[test]` section.

**If `[test]` section exists:** Skip this phase and display:
> "Test configuration already present in foundry-mcp.toml. Your existing settings are preserved."

Continue to Setup Complete.

### Step 2: Detect Test Runner

Call `mcp__plugin_foundry_foundry-mcp__environment action="detect-test-runner"` to analyze the project.

Parse the response to get:
- `detected_runners`: Array of detected runners with confidence levels
- `recommended_default`: The recommended runner based on project type

### Step 3: Present Results and Get User Choice

**If runners were detected:**

Display the detection results:

```
## Test Runner Detection

Detected test runner(s) for this project:

| Runner | Project Type | Confidence | Reason |
|--------|--------------|------------|--------|
| pytest | python | high | pyproject.toml found |
```

Use `AskUserQuestion`:
- Question: "Configure test runner in foundry-mcp.toml?"
- Options:
  - "Yes, use {recommended_default} (recommended)"
  - "Skip test configuration"

**If "Yes":** Proceed to Step 4.
**If "Skip":** Continue to Setup Complete.

---

**If no runners were detected:**

Display:
> "No test runners detected for this project. You can manually configure the `[test]` section in foundry-mcp.toml if needed."

Continue to Setup Complete.

### Step 4: Append Test Section to TOML

Read the existing `foundry-mcp.toml` file content.

Append the test configuration section using textual append (preserves comments and formatting):

```toml

[test]
# Auto-configured based on project detection
default_runner = "{recommended_default}"
```

Use the Write tool to save the updated file.

Display:
> "Added [test] section to foundry-mcp.toml with default_runner = \"{recommended_default}\""

---

## Phase 2.8: Git Configuration

**Only run this phase if foundry-mcp.toml exists (either created in Phase 2 or already present).**

This phase configures the `[git]` section for automatic commit behavior during spec-driven workflows.

### Step 1: Check Existing Configuration

Read the `foundry-mcp.toml` file and check if it already contains a `[git]` section.

**If `[git]` section exists:** Skip this phase and display:
> "Git configuration already present in foundry-mcp.toml. Your existing settings are preserved."

Continue to Setup Complete.

### Step 2: Check Git Repository Status

Run `git rev-parse --is-inside-work-tree` to verify this is a git repository.

**If not a git repo:** Display:
> "Not a git repository. Skipping git configuration."

Continue to Setup Complete.

### Step 3: Ask User for Commit Cadence

Use `AskUserQuestion`:
- Question: "When should foundry auto-commit your changes?"
- Options:
  - "Manual (default)" → commit_cadence = "manual"
  - "After each task" → commit_cadence = "task"
  - "After each phase" → commit_cadence = "phase"

### Step 4: Append Git Section to TOML

Read the existing `foundry-mcp.toml` file content.

Append the git configuration section:

```toml

[git]
# Git workflow configuration
enabled = true
commit_cadence = "{selected_cadence}"
```

Use the Edit tool to update the file.

### Step 5: Display Results

```
## Git Configuration

Configured git settings:

| Setting | Value |
|---------|-------|
| enabled | true |
| commit_cadence | {selected_cadence} |

Commits will be created automatically {cadence_description}.
```

Where `cadence_description` is:
- manual: "only when you explicitly request them"
- task: "after each task is completed"
- phase: "after each phase is completed"

---

## Phase 3: CLAUDE.md Configuration

This phase creates or updates the project's CLAUDE.md file with Foundry SDD workflow guidance. This helps ensure Claude uses the correct skills and tools for spec-driven development.

### Step 1: Check for Existing CLAUDE.md

Use the Read tool to check if `CLAUDE.md` exists in the project root.

**If file exists:** Check if it contains the `<!-- foundry-sdd-start -->` marker.

### Step 2: Handle Based on Status

**If no CLAUDE.md exists:**

Use `AskUserQuestion`:
- Question: "Create CLAUDE.md with Foundry SDD workflow guidance?"
- Options:
  - "Yes, create it (recommended)"
  - "No, skip"

**If "Yes":** Create the file with the template content below.

---

**If CLAUDE.md exists but no marker:**

Use `AskUserQuestion`:
- Question: "Append Foundry SDD section to existing CLAUDE.md?"
- Options:
  - "Yes, append (recommended)"
  - "No, skip"

**If "Yes":** Append the template content below to the end of the existing file.

---

**If marker already exists:**

Display:
> "Foundry SDD guidance already present in CLAUDE.md. Skipping."

Continue to Setup Complete.

### Template Content

Use marker comments for idempotent updates:

```markdown
<!-- foundry-sdd-start -->
## Foundry SDD Workflow

| When you need to... | Use |
|---------------------|-----|
| Create/review/modify a spec | `foundry-spec` skill |
| Find next task, implement | `foundry-implement` skill |
| Verify implementation | `foundry-review` skill |
| Run tests and debug | `foundry-test` skill |
| Create PR with spec context | `foundry-pr` skill |
| Safe refactoring with LSP | `foundry-refactor` skill |

### Key Rules

**Always use skills over direct MCP calls:**
- Skills provide workflow orchestration, error handling, and context
- Do NOT call `mcp__plugin_foundry_foundry-mcp__authoring` directly
- Do NOT call `mcp__plugin_foundry_foundry-mcp__task` directly
- For phases with tasks, use `phase-add-bulk` (not `phase-add`)

**Use Explore subagent before skills:**
- Before `foundry-spec`: Understand codebase architecture and existing patterns
- Before `foundry-implement`: Find related code, test files, dependencies
- Thoroughness levels: `quick` (single file), `medium` (related files), `very thorough` (subsystem)

**Task completion gates - NEVER mark complete if:**
- Tests are failing (unless phase has separate verify task)
- Implementation is partial or incomplete
- Unresolved errors encountered
- Required files or dependencies missing
- Instead: keep `in_progress` and document blocker

**LSP pre-checks for speed:**
- Use `documentSymbol` before expensive AI reviews (foundry-review)
- Use `findReferences` to assess impact before refactoring (foundry-refactor)
- LSP catches structural issues in seconds vs minutes for full analysis

**Research tool defaults - let config decide:**
- Do NOT specify `timeout_per_provider` or `timeout_per_operation` - use `foundry-mcp.toml` defaults
- Do NOT specify `providers` - use configured consensus providers
- Only override when user explicitly requests different behavior
- Minimal call: `action="consensus" prompt="..." strategy="synthesize"`
<!-- foundry-sdd-end -->
```

### Step 3: Display Results

**If created:**
> "Created CLAUDE.md with Foundry SDD workflow guidance."

**If appended:**
> "Appended Foundry SDD section to existing CLAUDE.md."

**If skipped:**
> "CLAUDE.md configuration skipped."

---

## Setup Complete

Summarize what was configured:
- Pre-flight check results (what passed/failed)
- Permissions status (created/updated/skipped)
- Workspace setup (specs directory, foundry-mcp.toml)
- Context settings (auto_compact value, or note if already configured)
- Implement defaults (auto/delegate/parallel flags, or note if already configured)
- AI providers configured (list providers added to consultation priority, or note if skipped)
- Research configuration (default provider, consensus providers, deep research settings, or note if skipped/already configured)
- Test runner configured (runner name, or note if skipped/already configured)
- Git configuration (commit_cadence value, or note if skipped/already configured)
- CLAUDE.md (created/updated/skipped)

**Important:** If permissions were added or modified, display:
> "**Restart Claude Code** for the permission changes to take effect."

If no permissions were changed, end with:
> "Setup complete!"
