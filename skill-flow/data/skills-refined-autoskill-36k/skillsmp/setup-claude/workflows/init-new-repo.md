# Init Workflow: New Repository Setup

This workflow guides setting up a new or nearly-empty repository for optimal Claude Code usage with the **complete ecosystem**: skills, commands, subagents, hooks, rules, MCPs, and plugins.

## Core Principle

> **CLI-First**: Always prefer CLI tools over MCP (more token-efficient).
> Each MCP adds tool definitions to your context window. CLIs add nothing.

## Before Starting

Create a todo list with these 13 phases:

1. Environment & Global Tools Check
2. Project Scaffolding
3. Tech Stack Interview
4. CLI Discovery & Authentication
5. MCP Configuration (Context Window Aware)
6. Plugin Setup
7. Skills Installation
8. Subagent Configuration
9. Rules Configuration
10. Hooks Configuration
11. CLAUDE.md Generation
12. Ralph TUI Setup
13. Verification & Summary

---

## Phase 1: Environment & Global Tools Check

### Goal
Ensure required global tools are installed, up-to-date, and no global config conflicts exist.

### 1.1 Global CLAUDE.md Conflict Check (CRITICAL)

**Why this matters:** Global `~/.claude/CLAUDE.md` can override local project `CLAUDE.md` during Ralph loops, causing the model to receive wrong project context.

```bash
# Check for global CLAUDE.md
if [ -f ~/.claude/CLAUDE.md ]; then
  echo "⚠ WARNING: Global CLAUDE.md found at ~/.claude/CLAUDE.md"
  echo "Content preview:"
  head -20 ~/.claude/CLAUDE.md
  echo "---"
  wc -l ~/.claude/CLAUDE.md
else
  echo "✓ No global CLAUDE.md (good - local will be used)"
fi
```

**If global CLAUDE.md exists**, ask user:
```
AskUserQuestion: "Global CLAUDE.md detected. This can override your project's local CLAUDE.md during Ralph loops."
├── "Rename to .bak" (Recommended) → mv ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak
├── "Delete it" → rm ~/.claude/CLAUDE.md
├── "Keep it" → Continue (may cause issues)
└── "View full contents first" → Show file, then re-ask
```

### 1.2 Required Tools

| Tool | Check Command | Purpose |
|------|---------------|---------|
| Claude Code | `claude --version` | Core CLI |
| GitHub CLI | `which gh` | Git operations & PRs |
| tmux | `which tmux` | Persistent sessions for Ralph loops |
| Agent Browser CLI | `which agent-browser` | Browser automation |
| Ralph TUI | `which ralph-tui` | Task orchestration |

### Steps

1. **Check each tool**:
   ```bash
   # Claude Code
   claude --version 2>/dev/null || echo "Claude Code: not found"

   # GitHub CLI (for commits, PRs, issues)
   which gh && gh --version || echo "GitHub CLI: not installed"

   # tmux (required for persistent Ralph loop sessions)
   which tmux && tmux -V || echo "tmux: not installed"

   # Agent Browser CLI
   which agent-browser && agent-browser --version || echo "Agent Browser: not installed"

   # Ralph TUI
   which ralph-tui && ralph-tui --version || echo "Ralph TUI: not installed"
   ```

2. **Report status**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   Global Tools Status
   ═══════════════════════════════════════════════════════════════════════════

   Global Config
   ───────────────────────────────────────────────────────────────────────────
   ~/.claude/CLAUDE.md    ✓ Not found (local will be used)
                          OR
                          ⚠ Found (may override local - action taken)

   Tools
   ───────────────────────────────────────────────────────────────────────────
   Claude Code        1.2.3           ✓ Installed
   GitHub CLI         2.40.0          ✓ Installed
   tmux               3.4             ✓ Installed
   Agent Browser CLI  0.8.0           ✓ Installed
   Ralph TUI          -               ✗ Not installed
   ```

3. **For missing tools**, ask user:
   ```
   AskUserQuestion: "Install missing tools?"
   ├── "Yes, install all" → Run npm install -g commands
   ├── "Let me install manually" → Show commands to copy
   └── "Skip for now" → Continue without installing
   ```

4. **Installation commands** (if approved):
   ```bash
   # GitHub CLI
   brew install gh && gh auth login

   # tmux (for persistent sessions)
   brew install tmux  # macOS
   # apt install tmux  # Ubuntu/Debian

   # Agent Browser CLI
   npm install -g agent-browser

   # Ralph TUI
   npm install -g ralph-tui
   # Or follow: https://github.com/subsy/ralph-tui
   ```

See: `components/tools-installation.md` for detailed guidance.

### Completion Criteria
- Global CLAUDE.md conflict resolved (if existed)
- All required tools installed OR user chose to skip
- Move to Phase 2

---

## Phase 2: Project Scaffolding

### Goal
Create standard folder structure for the project.

### Steps

1. **Interview project type**:
   ```
   AskUserQuestion: "What type of project is this?"
   ├── Frontend (React, Vue, Svelte)
   ├── Backend (API, server)
   ├── Fullstack (frontend + backend)
   ├── CLI tool
   └── Library/Package
   ```

2. **Create base folders** (always):
   ```bash
   mkdir -p src docs scripts .claude/{skills,commands,agents,rules}
   ```

3. **Create type-specific folders**:
   - **Frontend**: `src/components/`, `src/styles/`, `public/`
   - **Backend**: `src/routes/`, `src/services/`, `src/models/`
   - **Fullstack**: `apps/web/`, `apps/api/`, `packages/shared/`
   - **CLI**: `src/commands/`, `src/utils/`
   - **Library**: `src/lib/`, `examples/`

4. **Initialize git** if needed:
   ```bash
   git init 2>/dev/null || true
   echo -e "node_modules/\n.env\n.env.local\n.DS_Store\ndist/\n.turbo/" > .gitignore
   ```

5. **Create minimal README.md**:
   ```markdown
   # Project Name

   > Brief description

   ## Getting Started

   [Instructions will be added during setup]

   ## Development

   [Commands will be added during setup]
   ```

See: `components/folder-structure.md` for detailed templates.

### Completion Criteria
- All folders created
- Git initialized
- Basic README exists
- Move to Phase 3

---

## Phase 3: Tech Stack Interview

### Goal
Understand the technology choices for this project.

### Steps

1. **Auto-detect from config files**:
   ```bash
   # Check for existing config files
   [ -f "package.json" ] && echo "Node.js detected"
   [ -f "tsconfig.json" ] && echo "TypeScript detected"
   [ -f "next.config.js" ] || [ -f "next.config.mjs" ] || [ -f "next.config.ts" ] && echo "Next.js detected"
   [ -d "convex" ] && echo "Convex detected"
   [ -f "pyproject.toml" ] || [ -f "requirements.txt" ] && echo "Python detected"
   [ -f "Cargo.toml" ] && echo "Rust detected"
   [ -f "go.mod" ] && echo "Go detected"
   [ -f "biome.json" ] && echo "Biome detected"
   [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] && echo "ESLint detected"
   ```

2. **If not detected**, interview:

   **Primary Language:**
   ```
   AskUserQuestion: "What's the primary language?"
   ├── TypeScript (Recommended)
   ├── JavaScript
   ├── Python
   ├── Rust
   └── Go
   ```

   **Framework:**
   ```
   AskUserQuestion: "What framework will you use?"
   TypeScript/JS: Next.js, React, Express, Fastify, None
   Python: FastAPI, Django, Flask, None
   Rust: Axum, Actix, Tauri, None
   Go: Gin, Echo, Fiber, None
   ```

   **Formatter/Linter:**
   ```
   AskUserQuestion: "What formatter/linter?"
   ├── Biome (Recommended for TS/JS) - Fast, all-in-one
   ├── ESLint + Prettier
   ├── Ruff (Recommended for Python)
   ├── Black + Flake8
   └── Language default (rustfmt, gofmt)
   ```

3. **Store answers** for use in later phases

### Completion Criteria
- Tech stack understood (language, framework, formatter)
- Ready for CLI discovery
- Move to Phase 4

---

## Phase 4: CLI Discovery & Authentication ⭐ KEY PHASE

### Goal
Identify and configure CLIs for all external services (CLI-first approach).

### Steps

1. **Detect services from project**:
   ```bash
   # Check package.json dependencies
   cat package.json 2>/dev/null | grep -E "(supabase|stripe|sentry|convex|clerk|posthog)" || true

   # Check config files
   ls -la | grep -E "(convex|vercel|supabase)" || true

   # Check .env variable names
   grep -h "^[A-Z_]*=" .env .env.local .env.example 2>/dev/null | cut -d= -f1 || true
   ```

2. **Interview for additional services**:
   ```
   AskUserQuestion: "What external services will this project use?"
   (Multi-select)
   ├── Hosting: Vercel, AWS, Netlify, Railway
   ├── Database: Supabase, Convex, PlanetScale, Neon
   ├── Auth: Clerk, Auth0
   ├── Monitoring: Sentry, PostHog
   ├── Payments: Stripe
   └── Other (specify)
   ```

3. **For each service**, check CLI status:
   - Look up CLI in `reference/tech-stack-clis.md`
   - Check if installed: `which <cli>`
   - Check if authenticated: service-specific command

4. **Present CLI status**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   CLI Discovery Results
   ═══════════════════════════════════════════════════════════════════════════

   Service        CLI           Installed    Authenticated
   ───────────────────────────────────────────────────────────────────────────
   Vercel         vercel        ✓            ✓
   Supabase       supabase      ✓            ✗ Run: supabase login
   Convex         npx convex    ✓            ✓
   Stripe         stripe        ✗            -  Install: brew install stripe/stripe-cli/stripe
   GitHub         gh            ✓            ✓
   ```

5. **Offer installation/authentication**:
   ```
   AskUserQuestion: "Install missing CLIs and authenticate?"
   ├── "Yes, handle all" → Run install + auth commands
   ├── "Just show commands" → Display commands for manual execution
   └── "Skip for now" → Continue
   ```

6. **Run authentication interactively** (if approved):
   ```bash
   # These are interactive - run one at a time
   vercel login
   supabase login
   stripe login
   ```

**Important**: Only fall back to MCP when no CLI exists for a service.

See: `components/cli-discovery.md` and `reference/tech-stack-clis.md`

### Completion Criteria
- All services identified
- CLIs installed and authenticated (or skipped)
- Move to Phase 5

---

## Phase 5: MCP Configuration (Context Window Aware) ⭐ KEY PHASE

### Goal
Configure MCP servers for services that need them, while managing context window usage.

### Context Window Warning

> **Critical**: Each MCP consumes context window tokens.
> - Recommended: Under 10 MCPs enabled
> - Recommended: Under 80 total tools active
> MCPs should only be used when CLI doesn't exist or is insufficient.

### Steps

1. **Determine which MCPs are actually needed**:

   | Service | CLI Sufficient? | MCP Needed? |
   |---------|-----------------|-------------|
   | Vercel | Yes (`vercel`) | No |
   | Supabase | Yes (`supabase`) | No |
   | Stripe | Yes (`stripe`) | No |
   | GitHub | Yes (`gh`) | No |
   | Framework docs | N/A | Yes (context7) |
   | UI components | N/A | Yes (shadcn) if using shadcn |

2. **Create `.mcp.json`** in project root:
   ```json
   {
     "mcpServers": {
       "context7": {
         "command": "npx",
         "args": ["-y", "@anthropic-ai/context7-mcp"]
       }
     },
     "disabledMcpServers": []
   }
   ```

3. **Ask about optional MCPs**:
   ```
   AskUserQuestion: "Enable documentation MCPs?"
   ├── context7 - Framework/package documentation (Recommended)
   ├── shadcn - UI component documentation (if using shadcn/ui)
   └── None - I'll use web search
   ```

4. **Show context window impact**:
   ```
   MCP Configuration Summary:
   ├── Enabled: 2 (context7, shadcn)
   ├── Estimated tools added: ~15
   └── Status: ✓ Within recommended limits

   Note: CLIs (vercel, supabase, stripe, gh) add 0 tools to context
   ```

See: `components/mcp-management.md` and `reference/mcp-servers.md`

### Completion Criteria
- `.mcp.json` created with minimal necessary MCPs
- User understands context window tradeoffs
- Move to Phase 6

---

## Phase 6: Plugin Setup

### Goal
Configure essential Claude Code plugins.

### Steps

1. **Present plugin recommendations**:
   ```
   AskUserQuestion: "Install recommended plugins?"
   (Multi-select, show context impact)
   ├── hookify - Create hooks conversationally (Low impact)
   ├── typescript-lsp - TypeScript intelligence (Medium impact) [if TS project]
   ├── pyright-lsp - Python type checking (Medium impact) [if Python project]
   ├── mgrep - Better search than grep (Low impact)
   └── None
   ```

2. **Show context impact**:
   ```
   Plugin Context Impact:
   ├── hookify: ~3 tools
   ├── typescript-lsp: ~8 tools
   └── mgrep: ~2 tools

   Total with current MCPs: ~28 tools (✓ well under 80)
   ```

3. **Install selected plugins**:
   ```bash
   # Plugin installation varies - check plugin documentation
   ```

See: `components/plugin-setup.md` and `reference/essential-plugins.md`

### Completion Criteria
- Selected plugins installed
- Context impact documented
- Move to Phase 7

---

## Phase 7: Skills Installation

### Goal
Install relevant skills for the project.

### Steps

1. **Install mandatory skills** (always):
   - `prd` - Product requirements documents
   - `agent-browser` - Browser automation

   ```bash
   # Copy from cc-guide if available
   cp -r ~/Documents/cc-guide/skills/prd .claude/skills/
   cp -r ~/Documents/cc-guide/skills/agent-browser .claude/skills/
   ```

2. **Map tech stack to skills** using `reference/tech-stack-skills.md`:

   | Tech Stack | Recommended Skills |
   |------------|-------------------|
   | Next.js | react-best-practices, tailwind-shadcn, nextjs-patterns |
   | Convex | convex-patterns |
   | Python | python-best-practices |
   | Git | git-workflow |

3. **Present recommendations**:
   ```
   Based on your tech stack (Next.js + Convex), I recommend:

   1. react-best-practices - React/Next.js performance patterns
   2. nextjs-patterns - App Router patterns
   3. convex-patterns - Convex database patterns
   4. tailwind-shadcn - Tailwind CSS and shadcn/ui
   5. git-workflow - Git conventions

   AskUserQuestion: "Install these skills?"
   ├── "Yes, install all recommended"
   ├── "Let me select individually"
   └── "Skip, just mandatory"
   ```

4. **Ensure skills are user-invokable** (not preloaded):
   - Skills are triggered by `/skillname` commands
   - Listed in CLAUDE.md with trigger patterns

See: `components/skills-discovery.md`, `reference/mandatory-skills.md`, `reference/tech-stack-skills.md`

### Completion Criteria
- Mandatory skills installed
- Tech-stack skills installed (if selected)
- Move to Phase 8

---

## Phase 8: Subagent Configuration

### Goal
Set up subagents for common workflows.

### Steps

1. **Explain subagents**:
   ```
   Subagents are specialized Claude instances with scoped tools.
   They help with focused tasks like planning, reviewing, or testing.
   ```

2. **Present subagent options**:
   ```
   AskUserQuestion: "Set up subagents for common workflows?"
   (Multi-select)
   ├── planner - Feature implementation planning
   ├── code-reviewer - Quality/security review
   ├── tdd-guide - Test-driven development
   ├── refactor-cleaner - Dead code removal
   └── None - I'll add later
   ```

3. **Copy selected templates** to `.claude/agents/`:
   ```bash
   # Example for planner
   cp templates/subagents/planner.md .claude/agents/
   ```

4. **Explain scoped tools**:
   ```
   Each subagent has limited tools for focused execution:

   planner: Read, Glob, Grep (research only)
   code-reviewer: Read, Glob, Grep (no editing)
   tdd-guide: Read, Write, Edit, Bash (full dev)
   refactor-cleaner: Read, Edit, Grep (modify only)
   ```

See: `components/subagent-setup.md`, `reference/subagent-templates.md`, `templates/subagents/`

### Completion Criteria
- Selected subagents configured
- User understands subagent scoping
- Move to Phase 9

---

## Phase 9: Rules Configuration

### Goal
Set up modular rules for consistent Claude behavior.

### Steps

1. **Explain modular rules**:
   ```
   Rules are always-active guidelines stored in .claude/rules/
   Unlike CLAUDE.md (context), rules are behavioral constraints.
   ```

2. **Present rule options**:
   ```
   AskUserQuestion: "Set up modular rules?"
   (Multi-select)
   ├── security.md - No hardcoded secrets, validate inputs
   ├── coding-style.md - File organization, naming conventions
   ├── testing.md - TDD workflow, coverage requirements
   ├── git-workflow.md - Commit format, PR process
   └── None - I'll add custom rules later
   ```

3. **Copy selected templates** to `.claude/rules/`:
   ```bash
   cp templates/rules/security.md .claude/rules/
   cp templates/rules/coding-style.md .claude/rules/
   ```

4. **Customize if requested**:
   - Ask about project-specific security concerns
   - Ask about naming conventions
   - Ask about test coverage requirements

See: `components/rules-configuration.md`, `templates/rules/`

### Completion Criteria
- Selected rules configured
- Rules customized for project
- Move to Phase 10

---

## Phase 10: Hooks Configuration

### Goal
Set up automatic formatting, linting, and workflow hooks.

### Steps

1. **Present hook options** based on tech stack:
   ```
   AskUserQuestion: "Which hooks to enable?"
   (Multi-select)
   ├── Format on save (biome check --write) [Recommended]
   ├── Type check after edits (tsc --noEmit)
   ├── Lint check (eslint --fix)
   ├── tmux reminder for long commands
   ├── Block .md file creation (except README/CLAUDE)
   ├── Console.log warning
   └── Review before git push
   ```

2. **Generate `.claude/settings.json`**:
   ```json
   {
     "permissions": {
       "defaultMode": "bypassPermissions"
     },
     "hooks": {
       "PostToolUse": [
         {
           "matcher": "Edit|Write",
           "hooks": [
             {
               "type": "command",
               "command": "biome check --write $CLAUDE_FILE_PATHS"
             }
           ]
         }
       ]
     }
   }
   ```

3. **Explain hook types**:
   - **PreToolUse**: Before tool runs (can block)
   - **PostToolUse**: After tool completes (auto-fix)
   - **Notification**: User notifications

4. **Offer hookify**:
   ```
   Tip: Use /hookify to create custom hooks conversationally.
   ```

See: `components/hooks-configuration.md`, `reference/hook-patterns.md`, `reference/hook-templates.md`

### Completion Criteria
- settings.json created with selected hooks
- User understands hook system
- Move to Phase 11

---

## Phase 11: CLAUDE.md Generation

### Goal
Create comprehensive CLAUDE.md with all 10 required sections.

### Required Sections

1. Project Description
2. Development Workflow
3. Things NOT to Do
4. Common Code Practices
5. Commands (dev, test, build, lint)
6. Available Skills (with triggers)
7. MCP Servers (enabled + when to use)
8. Documentation Methods
9. Subagents (when to delegate)
10. General Guidelines

### Steps

1. **Interview for content**:

   **Project Description:**
   ```
   AskUserQuestion: "Describe this project in 2-3 sentences"
   (Free text)
   ```

   **Build/Run Commands:**
   ```
   AskUserQuestion: "What are the key commands?"
   ├── Dev: npm run dev
   ├── Test: npm test
   ├── Build: npm run build
   ├── Lint: npm run lint
   ```

   **Things NOT to Do:**
   ```
   AskUserQuestion: "Any critical warnings?"
   Examples:
   - Don't modify files in /legacy
   - Never commit .env files
   - Don't use deprecated API v1
   ```

   **Coding Conventions:**
   ```
   AskUserQuestion: "Key coding conventions?"
   ├── Use functional components
   ├── Prefer composition over inheritance
   ├── Use async/await
   └── Custom: [free text]
   ```

2. **Generate CLAUDE.md** with all sections from interview + previous phases

3. **Review with user** before writing

See: `components/claudemd-writing.md`, `templates/claude-md/complete-template.md`

### Completion Criteria
- CLAUDE.md created with all 10 sections
- User approved content
- Move to Phase 12

---

## Phase 12: Ralph TUI Setup

### Goal
Configure Ralph TUI for autonomous task execution with custom prompt template and verify all paths are correct.

### Critical Configuration Points

Ralph TUI requires several files to work correctly together:

| Component | Location | Purpose |
|-----------|----------|---------|
| config.toml | `.ralph-tui/config.toml` | Main configuration |
| prompt.hbs | Path from `prompt_template` | Prompt template |
| prd.json | Path from `prdPath` | Task definitions |
| progress.md | `.ralph-tui/progress.md` | Cross-iteration memory |

**Common failure modes:**
1. `prompt_template` path doesn't match actual file location → falls back to default template
2. Global CLAUDE.md overrides local → wrong project context (checked in Phase 1)
3. Tasks in prd.json not in description field → tasks don't render in prompt

### Steps

1. **Create `.ralph-tui/` structure**:
   ```bash
   mkdir -p .ralph-tui/templates .ralph-tui/iterations
   ```

2. **Copy config and template**:
   ```bash
   # Copy config to .ralph-tui/
   cp templates/ralph-tui/config.toml .ralph-tui/

   # Copy prompt.hbs to .ralph-tui/templates/
   cp templates/ralph-tui/prompt.hbs .ralph-tui/templates/
   ```

3. **Verify template is being used** (CRITICAL):
   ```bash
   # Run ralph-tui template show to see where it's loading from
   ralph-tui template show | head -10

   # Should show content from YOUR template, not the default
   # If it shows different content, the path is wrong
   ```

4. **Check config.toml paths**:
   ```bash
   # Verify prompt_template path
   grep "prompt_template" .ralph-tui/config.toml
   # Must match: .ralph-tui/templates/prompt.hbs

   # Verify the file exists
   ls -la .ralph-tui/templates/prompt.hbs

   # Check prdPath setting
   grep "prdPath\|path" .ralph-tui/config.toml
   ```

5. **Customize config.toml**:
   ```
   AskUserQuestion: "Ralph TUI preferences?"
   ├── Model: Opus (highest quality, recommended) / Sonnet (balanced)
   ├── Auto-commit: Yes (recommended) / No
   └── Max iterations: 70 (default)
   ```

6. **Verify template has required variables**:

   Check the template includes these sections:
   ```bash
   # PRD context variables (must include currentIteration)
   grep -E "prdName|prdDescription|prdCompletedCount|currentIteration" .ralph-tui/templates/prompt.hbs

   # Task variables
   grep -E "taskId|taskTitle|taskDescription|acceptanceCriteria" .ralph-tui/templates/prompt.hbs

   # Template should NOT have recentProgress (agent reads file directly)
   grep "recentProgress" .ralph-tui/templates/prompt.hbs && echo "WARNING: Remove recentProgress - it's redundant"
   ```

7. **Run ralph-tui doctor** to validate:
   ```bash
   ralph-tui doctor
   ```

### Template Variable Mapping

Understanding how prd.json maps to prompt.hbs:

| prd.json Field | Template Variable | Notes |
|----------------|-------------------|-------|
| `name` | `{{prdName}}` | Project identifier |
| `description` | `{{prdDescription}}` | Project context |
| Calculated | `{{prdCompletedCount}}` | Completed story count |
| Calculated | `{{prdTotalCount}}` | Total story count |
| Calculated | `{{currentIteration}}` | Current iteration number (REQUIRED) |
| `userStories[].id` | `{{taskId}}` | e.g., US-001 |
| `userStories[].title` | `{{taskTitle}}` | Story title |
| `userStories[].description` | `{{taskDescription}}` | **Tasks must be embedded here** |
| `userStories[].acceptanceCriteria` | `{{acceptanceCriteria}}` | Array → auto-formatted checkboxes |
| `userStories[].notes` | `{{notes}}` | File paths, warnings |
| `userStories[].dependsOn` | `{{dependsOn}}` | Prerequisites |
| From progress.md | `{{codebasePatterns}}` | Discovered patterns (optional) |

**DEPRECATED - Do NOT use:**
| Variable | Reason |
|----------|--------|
| `{{recentProgress}}` | Agent reads `.ralph-tui/progress.md` directly as first action every iteration |

**IMPORTANT:** Tasks are NOT a separate template variable. They must be embedded in the `description` field:

```json
{
  "description": "What this story accomplishes.\n\n**Tasks:**\n1. First task\n2. Second task\n3. Third task"
}
```

### Template Verification Checklist (Optimized v2)

Before moving on, verify with `ralph-tui template show`:
- [ ] Template loads from `.ralph-tui/templates/prompt.hbs` (not default)
- [ ] Template does NOT include `{{recentProgress}}` (agent reads file directly)
- [ ] Template includes `{{currentIteration}}` in header
- [ ] Template has "Context Files (Read These First)" section with explicit paths
- [ ] Template has 3-phase workflow: Context Gathering → Implementation → Documentation
- [ ] Template has gibberish cleanup instructions in Phase 3
- [ ] Template has verbose progress entry format with 4 sections (What/Files/Learnings/Quality)
- [ ] Template says "Be verbose and thorough - future iterations start with no memory"
- [ ] Template has completion signals (COMPLETE, BLOCKED, SKIP, EJECT)
- [ ] Template references CLAUDE.md for project context
- [ ] Template references progress.md for iteration context

### Template Anti-Pattern Detection

Flag these issues if found:

| Issue | Problem | Fix |
|-------|---------|-----|
| `{{recentProgress}}` in template | Redundant - agent reads file directly | Remove the section |
| No `{{currentIteration}}` | Can't track which iteration in logs | Add to header |
| No gibberish cleanup instruction | JSON fragments accumulate in progress.md | Add Phase 3 step |
| Simple progress format | Future iterations lack context | Use verbose 4-section format |

### Additional Context for Model

The optimized v2 template includes explicit paths:
- Path to PRD.md for big-picture context: `docs/prds/[name]/PRD.md`
- Path to progress.md: `.ralph-tui/progress.md`
- Path to iterations folder: `.ralph-tui/iterations/`

This lets the model investigate context when confused.

### Completion Criteria
- `.ralph-tui/` directory created with proper structure
- Config customized with correct paths
- `ralph-tui template show` confirms correct template is loaded
- `ralph-tui doctor` passes
- Move to Phase 13

---

## Phase 13: Verification & Summary

### Goal
Verify setup and provide comprehensive summary.

### Steps

1. **Summarize all created items**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   Setup Complete!
   ═══════════════════════════════════════════════════════════════════════════

   Folders Created:
   ├── src/, docs/, scripts/
   └── .claude/{skills,commands,agents,rules}

   Global Tools:
   ├── Claude Code: v1.2.3 ✓
   ├── GitHub CLI: v2.40.0 ✓
   ├── tmux: v3.4 ✓
   ├── Agent Browser CLI: v0.8.0 ✓
   └── Ralph TUI: v0.5.0 ✓

   CLIs Authenticated:
   ├── Vercel ✓
   ├── Supabase ✓
   └── Stripe ✓

   MCPs Configured: 2
   ├── context7 (framework docs)
   └── shadcn (UI components)

   Skills Installed: 5
   ├── prd (/prd)
   ├── agent-browser (/agent-browser)
   ├── react-best-practices
   ├── convex-patterns
   └── git-workflow

   Subagents Configured: 2
   ├── planner
   └── code-reviewer

   Rules Configured: 3
   ├── security.md
   ├── coding-style.md
   └── testing.md

   Hooks Configured:
   ├── Format on save ✓
   ├── Type check ✓
   └── Console.log warning ✓

   Files Created:
   ├── CLAUDE.md (10 sections)
   ├── .claude/settings.json
   ├── .mcp.json
   └── .ralph-tui/config.toml

   Context Window Status:
   ├── MCPs enabled: 2 ✓
   └── Estimated tools: ~28 ✓
   ```

2. **Offer validation**:
   ```
   AskUserQuestion: "Run validation?"
   ├── "Yes, run format + type check"
   └── "No, I'll do it manually"
   ```

3. **Suggest next steps**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   Next Steps
   ═══════════════════════════════════════════════════════════════════════════

   1. Review CLAUDE.md and customize further
   2. Run /prd to plan your first feature
   3. Run /ralph-preflight to verify everything is ready
   4. Start your Ralph loop

   Quick Commands:
   ├── /prd                  - Create a PRD for a feature
   ├── /ralph-preflight      - Pre-flight check before Ralph loop
   ├── /agent-browser        - Browser automation
   └── /setup-claude audit   - Re-analyze setup later

   ═══════════════════════════════════════════════════════════════════════════
   Ralph Loop Workflow
   ═══════════════════════════════════════════════════════════════════════════

   Option A: Simple Branch (single feature at a time)
   ───────────────────────────────────────────────────────────────────────────
   # 1. Create PRD
   /prd

   # 2. Run pre-flight check
   /ralph-preflight

   # 3. Create feature branch
   git checkout -b feature/your-feature-name

   # 4. Start tmux session and Ralph loop
   tmux new-session -d -s ralph-feature "ralph-tui run --prd path/to/prd.json"
   tmux attach-session -t ralph-feature
   # Press 's' to start, then Ctrl+B D to detach

   Option B: Git Worktree (parallel development)
   ───────────────────────────────────────────────────────────────────────────
   # 1. Create PRD
   /prd

   # 2. Create worktree (isolated directory with its own branch)
   git worktree add ../myproject-feature feature/feature-name

   # 3. Navigate to worktree
   cd ../myproject-feature

   # 4. Run pre-flight in worktree
   /ralph-preflight

   # 5. Start tmux session and Ralph loop
   tmux new-session -d -s ralph-feature "ralph-tui run --prd path/to/prd.json"
   tmux attach-session -t ralph-feature

   Monitoring Your Ralph Loop:
   ───────────────────────────────────────────────────────────────────────────
   # Check tmux sessions
   tmux list-sessions

   # Reattach to a session
   tmux attach-session -t ralph-feature

   # Detach (keep running)
   Ctrl+B, then D

   # Check progress
   cat .ralph-tui/progress.md

   # View Ralph status
   ralph-tui status
   ```

### Completion Criteria
- User has clear summary
- Validation passed (if run)
- User knows next steps and Ralph loop workflow
- **Workflow complete**
