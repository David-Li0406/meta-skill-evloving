# Audit Workflow: Existing Repository Analysis

This workflow guides analyzing and improving existing repositories for optimal Claude Code usage.

## Core Principle

> **CLI-First**: Always prefer CLI tools over MCP (more token-efficient).
> Audit should identify opportunities to replace MCPs with CLIs.

## Before Starting

Create a todo list with these 8 phases:

1. Environment Analysis
2. CLI Audit
3. Context Window Analysis
4. Gap Analysis
5. Recommendations Report
6. Interactive Fixes
7. Context Window Optimization
8. Summary & Verification

---

## Phase 1: Environment Analysis

### Goal
Understand the current state of the repository and its Claude configuration.

### Steps

1. **Tech stack detection**:
   ```bash
   # Package manager and dependencies
   cat package.json 2>/dev/null | head -50

   # TypeScript config
   cat tsconfig.json 2>/dev/null | head -30

   # Framework configs
   ls -la | grep -E "(next|vite|nuxt|svelte|astro)" || true
   ls convex/ 2>/dev/null || true

   # Formatter/linter configs
   ls -la | grep -E "(biome|eslint|prettier|ruff)" || true
   ```

2. **Claude config discovery**:
   ```bash
   # CLAUDE.md
   [ -f "CLAUDE.md" ] && echo "CLAUDE.md: exists" || echo "CLAUDE.md: missing"

   # .claude/ directory
   [ -d ".claude" ] && ls -la .claude/ || echo ".claude/: missing"

   # Settings
   [ -f ".claude/settings.json" ] && cat .claude/settings.json || echo "settings.json: missing"

   # Skills
   [ -d ".claude/skills" ] && ls .claude/skills/ || echo "skills/: missing"

   # Agents (subagents)
   [ -d ".claude/agents" ] && ls .claude/agents/ || echo "agents/: missing"

   # Rules
   [ -d ".claude/rules" ] && ls .claude/rules/ || echo "rules/: missing"
   ```

3. **MCP/Plugin discovery**:
   ```bash
   # Project MCPs
   [ -f ".mcp.json" ] && cat .mcp.json || echo ".mcp.json: missing"

   # Check global MCP config
   [ -f ~/.claude/.mcp.json ] && cat ~/.claude/.mcp.json || true
   ```

4. **Ralph TUI check** (verify template setup):
   ```bash
   [ -d ".ralph-tui" ] && echo "Ralph TUI: configured" || echo "Ralph TUI: not configured"
   [ -f ".ralph-tui/config.toml" ] && echo "  config.toml: exists" || true

   # Check configured template path
   [ -f ".ralph-tui/config.toml" ] && grep "prompt_template" .ralph-tui/config.toml || echo "  prompt_template: not set"

   # Verify template exists at configured path
   [ -f ".ralph-tui/templates/prompt.hbs" ] && echo "  prompt.hbs: exists at default location" || echo "  prompt.hbs: not at default location (may be custom path)"
   ```

5. **Ralph loop prerequisites check**:
   ```bash
   # tmux (required for persistent sessions)
   which tmux && tmux -V || echo "tmux: not installed (required for Ralph loops)"

   # Git worktrees (for parallel feature development)
   git worktree list 2>/dev/null || echo "Not a git repo or no worktrees"
   ```

6. **Present environment summary**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   Environment Analysis
   ═══════════════════════════════════════════════════════════════════════════

   Tech Stack:
   ├── Language: TypeScript
   ├── Framework: Next.js 14
   ├── Database: Convex
   ├── Formatter: Biome
   └── Package Manager: pnpm

   Claude Config:
   ├── CLAUDE.md: ✓ exists (45 lines)
   ├── .claude/: ✓ exists
   │   ├── settings.json: ✓ (3 hooks configured)
   │   ├── skills/: ✓ (2 skills)
   │   ├── agents/: ✗ missing
   │   └── rules/: ✗ missing
   ├── .mcp.json: ✓ (4 MCPs enabled)
   └── .ralph-tui/: ✗ not configured

   Ralph Loop Prerequisites:
   ├── tmux: ✓ installed (v3.4)
   └── Git worktrees: 1 active
   ```

### Completion Criteria
- Full understanding of current setup
- Move to Phase 2

---

## Phase 2: CLI Audit ⭐ KEY PHASE

### Goal
Identify external services and verify CLI coverage.

### Steps

1. **Detect services from multiple sources**:
   ```bash
   # From package.json dependencies
   cat package.json 2>/dev/null | grep -E '"(@supabase|stripe|@sentry|convex|@clerk|posthog|@vercel|@netlify|@aws-sdk)' || true

   # From config files
   ls -la | grep -E "(convex|vercel|supabase|netlify|firebase|railway)" || true

   # From .env variable names
   grep -h "^[A-Z_]*=" .env .env.local .env.example 2>/dev/null | cut -d= -f1 | grep -E "(SUPABASE|STRIPE|SENTRY|CONVEX|CLERK|POSTHOG|VERCEL|NETLIFY|AWS)" || true

   # From code imports (sample)
   grep -r "from ['\"]@supabase" src/ 2>/dev/null | head -3 || true
   grep -r "from ['\"]stripe" src/ 2>/dev/null | head -3 || true
   ```

2. **For each detected service**, check CLI status:
   ```bash
   # Example checks
   which vercel && vercel whoami 2>/dev/null || echo "Vercel CLI: not ready"
   which supabase && supabase projects list 2>/dev/null | head -1 || echo "Supabase CLI: not ready"
   npx convex --version 2>/dev/null || echo "Convex CLI: not ready"
   which stripe && stripe config --list 2>/dev/null | head -1 || echo "Stripe CLI: not ready"
   which gh && gh auth status 2>/dev/null || echo "GitHub CLI: not ready"
   ```

3. **Present CLI status**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   CLI Audit Results
   ═══════════════════════════════════════════════════════════════════════════

   Service        CLI           Installed    Authenticated
   ───────────────────────────────────────────────────────────────────────────
   Vercel         vercel        ✓            ✓
   Supabase       supabase      ✓            ✗ Run: supabase login
   Convex         npx convex    ✓            ✓
   Stripe         stripe        ✗            -  Install: brew install stripe/stripe-cli/stripe
   GitHub         gh            ✓            ✓
   Sentry         sentry-cli    ✗            -  Install: npm i -g @sentry/cli

   ───────────────────────────────────────────────────────────────────────────
   Summary: 4/6 installed, 3/4 authenticated
   Recommendation: Install 2 CLIs, authenticate 1 CLI
   ```

4. **Check for MCP redundancy**:
   ```
   MCP vs CLI Analysis:
   ├── supabase MCP enabled but supabase CLI available → Remove MCP
   ├── stripe MCP enabled but stripe CLI available → Remove MCP
   └── context7 MCP → Keep (no CLI equivalent)
   ```

### Completion Criteria
- All services identified
- CLI gaps documented
- MCP redundancies identified
- Move to Phase 3

---

## Phase 3: Context Window Analysis ⭐ NEW PHASE

### Goal
Analyze context window usage and identify optimization opportunities.

### Steps

1. **Count enabled MCPs**:
   ```bash
   # Count MCPs in .mcp.json
   cat .mcp.json 2>/dev/null | grep -c '"command"' || echo "0"

   # Check global MCPs
   cat ~/.claude/.mcp.json 2>/dev/null | grep -c '"command"' || echo "0"
   ```

2. **Estimate tool count**:
   ```
   Typical tool counts per MCP:
   - context7: ~5 tools
   - shadcn: ~3 tools
   - supabase MCP: ~15 tools
   - filesystem MCP: ~10 tools
   - github MCP: ~20 tools
   ```

3. **Check for bloat indicators**:
   - More than 10 MCPs enabled
   - MCPs for services with CLIs
   - Unused MCPs (services not in dependencies)

4. **Present analysis**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   Context Window Analysis
   ═══════════════════════════════════════════════════════════════════════════

   Current State:
   ├── MCPs enabled: 12 ⚠ (recommended: <10)
   ├── Estimated tools: ~95 ⚠ (recommended: <80)
   └── Redundant MCPs: 4 (have CLI equivalents)

   Issues Found:
   ├── supabase MCP: Redundant (CLI available)
   ├── stripe MCP: Redundant (CLI available)
   ├── github MCP: Redundant (gh CLI available)
   └── firebase MCP: Unused (not in dependencies)

   Recommendation:
   ├── Disable 4 redundant/unused MCPs
   ├── Expected tools after: ~45 ✓
   └── Context savings: ~50 tools
   ```

### Completion Criteria
- Context window impact quantified
- Optimization opportunities identified
- Move to Phase 4

---

## Phase 4: Gap Analysis

### Goal
Identify all gaps between current state and best practices.

### Steps

1. **Check for critical issues**:

   | Check | Status | Impact |
   |-------|--------|--------|
   | CLAUDE.md exists | ✓/✗ | Claude has no project context |
   | .claude/ directory | ✓/✗ | No config structure |
   | Hooks configured | ✓/✗ | Files not auto-formatted |

2. **Check for important improvements**:

   | Check | Status | Recommendation |
   |-------|--------|----------------|
   | Mandatory skills (prd, agent-browser) | ✓/✗ | Install skills |
   | Tech-stack skills | ✓/✗ | Add react-best-practices |
   | Subagents configured | ✓/✗ | Add planner, code-reviewer |
   | Rules configured | ✓/✗ | Add security.md |
   | CLIs installed | ✓/✗ | Install stripe CLI |
   | CLIs authenticated | ✓/✗ | Run supabase login |
   | Context window healthy | ✓/✗ | Remove redundant MCPs |
   | tmux installed | ✓/✗ | Required for Ralph loops |
   | Ralph TUI setup | ✓/✗ | Add .ralph-tui/ |

3. **Check for minor suggestions**:

   | Check | Status | Suggestion |
   |-------|--------|------------|
   | CLAUDE.md sections complete | ✓/✗ | Add MCP section |
   | Additional hooks | ✓/✗ | Add console.log warning |
   | Useful plugins | ✓/✗ | Consider hookify |

4. **Categorize by severity**:
   ```
   Gap Analysis Results:

   🔴 Critical Issues (2):
   1. No CLAUDE.md file
   2. No hooks configured

   🟡 Important Improvements (5):
   1. Missing mandatory skill: agent-browser
   2. Supabase CLI not authenticated
   3. Stripe CLI not installed
   4. 4 redundant MCPs consuming context
   5. No subagents configured

   🟢 Minor Suggestions (3):
   1. CLAUDE.md missing "MCP Servers" section
   2. Could add console.log warning hook
   3. Ralph TUI not configured
   ```

### Completion Criteria
- All gaps identified and categorized
- Move to Phase 5

---

## Phase 5: Recommendations Report

### Goal
Present a clear, actionable report of all findings.

### Steps

1. **Generate formatted report**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   Audit Results for [project-name]
   ═══════════════════════════════════════════════════════════════════════════

   ## Summary
   - Critical issues: 2
   - Important improvements: 5
   - Minor suggestions: 3

   ## Critical Issues

   ### 1. No CLAUDE.md file
   **Impact**: Claude has no context about your project. It doesn't know your
   commands, conventions, or warnings.

   **Fix**: Create CLAUDE.md with:
   - Project description
   - Dev/test/build commands
   - Coding conventions
   - Important warnings

   **Effort**: Medium (interview required)

   ### 2. No hooks configured
   **Impact**: Files are not auto-formatted after Claude edits them.

   **Detected formatter**: Biome (from biome.json)

   **Fix**: Add to .claude/settings.json:
   {
     "hooks": {
       "PostToolUse": [{
         "matcher": "Edit|Write",
         "hooks": [{"type": "command", "command": "biome check --write $CLAUDE_FILE_PATHS"}]
       }]
     }
   }

   **Effort**: Low (automated)

   ## Important Improvements

   ### 1. Missing CLI: Stripe
   **Detected**: stripe package in package.json
   **Current**: Using Stripe MCP (consumes ~15 tools)

   **Fix**:
   brew install stripe/stripe-cli/stripe
   stripe login

   **Benefit**: Remove MCP, save ~15 tools from context

   [... continue for all issues ...]
   ```

2. **Wait for user to review** before proceeding

### Completion Criteria
- User has reviewed recommendations
- Move to Phase 6

---

## Phase 6: Interactive Fixes

### Goal
Apply fixes with user approval.

### Steps

1. **Process fixes in priority order** (critical first):

   For each fix:
   ```
   AskUserQuestion: "Apply this fix?"

   Fix: Create CLAUDE.md
   What will happen:
   - Interview you for project details
   - Generate CLAUDE.md with all 10 sections
   - You can review before saving

   Options:
   ├── "Yes, apply it"
   ├── "Skip this one"
   └── "Let me customize first"
   ```

2. **Handle different fix types**:

   **Create CLAUDE.md**:
   - Run interview from components/claudemd-writing.md
   - Generate content
   - Review with user
   - Write file

   **Create/update settings.json**:
   - Create backup: `cp .claude/settings.json .claude/settings.json.backup`
   - Merge new hooks with existing
   - Write updated file

   **Install skills**:
   - Copy to .claude/skills/
   - Update CLAUDE.md skills section

   **Configure subagents**:
   - Copy templates to .claude/agents/
   - Customize tool scoping

   **Set up rules**:
   - Copy templates to .claude/rules/
   - Customize for project

   **Install/auth CLIs**:
   ```bash
   # Interactive - run one at a time
   brew install stripe/stripe-cli/stripe
   stripe login
   ```

   **Configure MCPs**:
   - Update .mcp.json
   - Add to disabledMcpServers if removing

   **Disable unused MCPs**:
   - Update disabledMcpServers in .mcp.json

   **Set up Ralph TUI**:
   - Create .ralph-tui/ structure with templates/ subdirectory
   - Copy config.toml to .ralph-tui/
   - Copy prompt.hbs to .ralph-tui/templates/
   - Verify config.toml `prompt_template` setting matches your template location
   - If using custom template path, update `prompt_template` in config.toml accordingly

3. **Track all changes** for summary

### Completion Criteria
- All approved fixes applied
- Skipped items documented
- Move to Phase 7

---

## Phase 7: Context Window Optimization ⭐ NEW PHASE

### Goal
Optimize context window usage.

### Steps

1. **If context issues were identified**:
   ```
   AskUserQuestion: "Optimize context window?"

   Current state:
   - MCPs enabled: 12
   - Estimated tools: ~95

   Recommended changes:
   1. Disable supabase MCP (CLI available) → -15 tools
   2. Disable stripe MCP (CLI available) → -15 tools
   3. Disable github MCP (gh CLI available) → -20 tools
   4. Disable firebase MCP (unused) → -10 tools

   After optimization:
   - MCPs enabled: 8 ✓
   - Estimated tools: ~35 ✓

   Options:
   ├── "Yes, apply all"
   ├── "Let me select"
   └── "Skip optimization"
   ```

2. **Apply selected optimizations**:
   ```json
   // Update .mcp.json
   {
     "mcpServers": { ... },
     "disabledMcpServers": [
       "supabase",
       "stripe",
       "github",
       "firebase"
     ]
   }
   ```

3. **Verify context window health**:
   ```
   Context Window After Optimization:
   ├── MCPs enabled: 8 ✓ (was 12)
   ├── Estimated tools: ~35 ✓ (was ~95)
   └── Status: Healthy
   ```

### Completion Criteria
- Context window optimized (or skipped)
- Move to Phase 8

---

## Phase 8: Summary & Verification

### Goal
Summarize changes and verify setup.

### Steps

1. **Summarize all changes**:
   ```
   ═══════════════════════════════════════════════════════════════════════════
   Audit Complete!
   ═══════════════════════════════════════════════════════════════════════════

   Changes Made:
   ├── Created CLAUDE.md (10 sections)
   ├── Added hooks to settings.json
   │   ├── Format on save (Biome)
   │   ├── Type check (tsc)
   │   └── Console.log warning
   ├── Installed skills:
   │   ├── agent-browser
   │   └── react-best-practices
   ├── Configured subagents:
   │   ├── planner
   │   └── code-reviewer
   ├── Added rules:
   │   └── security.md
   ├── CLI changes:
   │   ├── Installed: stripe
   │   └── Authenticated: supabase
   ├── Disabled MCPs:
   │   ├── supabase (using CLI)
   │   ├── stripe (using CLI)
   │   └── github (using gh CLI)
   └── Set up Ralph TUI

   Skipped (by choice):
   ├── Additional rules (testing.md, git-workflow.md)
   └── tdd-guide subagent

   Backups Created:
   └── .claude/settings.json.backup
   ```

2. **Show before/after comparison**:
   ```
   Before → After:
   ├── CLAUDE.md: ✗ → ✓ (10 sections)
   ├── Hooks: 0 → 3
   ├── Skills: 1 → 3
   ├── Subagents: 0 → 2
   ├── Rules: 0 → 1
   ├── MCPs: 12 → 8
   └── Est. tools: ~95 → ~35
   ```

3. **Offer verification**:
   ```
   AskUserQuestion: "Run verification?"
   ├── "Yes, verify setup"
   └── "No, I'll test manually"
   ```

4. **If verification requested**:
   ```bash
   # Test formatter hook
   echo "// test" >> test-hook.ts
   rm test-hook.ts

   # Verify skills
   ls .claude/skills/

   # Verify CLAUDE.md
   wc -l CLAUDE.md
   ```

5. **Suggest next steps**:
   ```
   Next Steps:
   1. Review CLAUDE.md and add project-specific details
   2. Test hooks by editing a file
   3. Run /prd to try the PRD skill
   4. Run /setup-claude audit again after making changes

   Tips:
   - Use /hookify to create custom hooks
   - Run validation before commits: npm run lint && npm run typecheck
   - Context window is now healthy (~35 tools)

   Git Worktrees (for parallel Ralph loops):
   # Create a worktree for a feature branch
   git worktree add ../project-feature-name feature-branch

   # Each worktree can run its own tmux session with Ralph
   tmux new-session -s feature-name
   cd ../project-feature-name && ralph-tui run
   ```

### Completion Criteria
- User has clear summary of changes
- Verification passed (if run)
- User knows next steps
- **Workflow complete**
