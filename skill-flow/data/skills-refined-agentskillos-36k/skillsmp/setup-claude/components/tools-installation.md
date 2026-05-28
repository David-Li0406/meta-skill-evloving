# Tools Installation Component

This component handles checking and installing required global tools with a **CLI-first** approach.

## Core Philosophy

> **CLI over MCP**: CLIs are more token-efficient than MCPs.
> Install CLIs for services instead of enabling MCPs when possible.

## Required Global Tools

| Tool | Purpose | Check | Install |
|------|---------|-------|---------|
| Claude Code | Core CLI | `claude --version` | Usually pre-installed |
| GitHub CLI | Git operations & PRs | `which gh` | `brew install gh` |
| tmux | Persistent sessions | `which tmux` | `brew install tmux` |
| Agent Browser CLI | Browser automation | `which agent-browser` | `npm i -g agent-browser` |
| Ralph TUI | Task orchestration | `which ralph-tui` | `npm i -g ralph-tui` |

## Tool Details

### 1. tmux (Critical for Ralph Loops)

Terminal multiplexer that creates persistent sessions. **Required for Ralph loops** because:
- Sessions persist even if SSH disconnects
- Run multiple agents in parallel in different panes
- Monitor long-running tasks without keeping terminal open

**Check:**
```bash
which tmux && tmux -V
```

**Install:**
```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt install tmux

# Fedora
sudo dnf install tmux
```

**Essential Commands:**
```bash
# Create named session
tmux new-session -s ralph-feature

# Detach from session (keeps running)
Ctrl+b, then d

# List sessions
tmux list-sessions

# Reattach to session
tmux attach-session -t ralph-feature

# Kill session
tmux kill-session -t ralph-feature

# Split panes (for multiple agents)
Ctrl+b, then %  # vertical split
Ctrl+b, then "  # horizontal split
```

**Ralph Loop Workflow:**
```bash
# Start session for feature
tmux new-session -s my-feature

# Run Ralph in background
ralph-tui run

# Detach and come back later
Ctrl+b, d
tmux attach -t my-feature
```

### 2. Git Worktrees (Parallel Development)

Git worktrees let you have multiple branches checked out simultaneously in different directories. **Essential for running multiple Ralph loops in parallel**.

**Check:**
```bash
git worktree list
```

**Key Commands:**
```bash
# Create worktree for feature branch
git worktree add ../project-feature-x feature-x

# List all worktrees
git worktree list

# Remove worktree when done
git worktree remove ../project-feature-x
```

**Parallel Ralph Loops Pattern:**
```bash
# Main branch in /project
# Feature A in /project-feature-a (own tmux session)
# Feature B in /project-feature-b (own tmux session)

# Setup
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b

# Run Ralph loops in parallel
tmux new-session -s feature-a -d "cd ../project-feature-a && ralph-tui run"
tmux new-session -s feature-b -d "cd ../project-feature-b && ralph-tui run"

# Monitor both
tmux attach -t feature-a
```

### 3. GitHub CLI

Essential for GitHub integration - **use instead of GitHub MCP**.

**Check:**
```bash
which gh && gh --version
```

**Install:**
```bash
# macOS
brew install gh

# Other platforms
# See: https://cli.github.com/
```

**Authenticate:**
```bash
gh auth login
```

**Verify:**
```bash
gh auth status
```

**What it does:**
- Create PRs: `gh pr create`
- List issues: `gh issue list`
- View PR checks: `gh pr checks`
- API access: `gh api`

### 4. Agent Browser CLI

Browser automation tool for headless Chrome control and E2E testing.

**Check:**
```bash
which agent-browser && agent-browser --version
```

**Install:**
```bash
npm install -g agent-browser
```

**Verify:**
```bash
agent-browser --version
```

**What it does:**
- Headless browser automation
- Screenshot capture
- Web scraping
- E2E test automation
- Works with MCP tools in Claude

### 5. Ralph TUI

Task orchestration for running multi-step tasks from PRDs.

**Check:**
```bash
which ralph-tui && ralph-tui --version
```

**Install:**
```bash
# Via npm
npm install -g ralph-tui

# Or via npx
npx ralph-tui --help
```

**What it does:**
- Orchestrates multi-agent task execution
- Reads PRDs and beads for task definitions
- Manages parallel and sequential execution
- Tracks progress across implementations

**Template Setup:**
When Ralph TUI is installed, copy templates to project:
```bash
mkdir -p .ralph-tui/templates .ralph-tui/iterations
cp templates/ralph-tui/config.toml .ralph-tui/
cp templates/ralph-tui/prompt.hbs .ralph-tui/templates/
```

### 6. Claude Code

The CLI they're using. Check version for updates.

**Check:**
```bash
claude --version
```

**Upgrade (if needed):**
```bash
npm update -g @anthropic-ai/claude-code
```

---

## Installation Flow

### Step 1: Check All Tools

```bash
# Check each tool
echo "=== Checking Global Tools ==="
claude --version || echo "Claude Code: not installed"
which gh && gh --version || echo "GitHub CLI: not installed"
which tmux && tmux -V || echo "tmux: not installed"
which agent-browser && agent-browser --version || echo "Agent Browser: not installed"
which ralph-tui && ralph-tui --version || echo "Ralph TUI: not installed"
```

### Step 2: Report Status

```
═══════════════════════════════════════════════════════════════════════════
Global Tools Status
═══════════════════════════════════════════════════════════════════════════

Tool               Version         Status
───────────────────────────────────────────────────────────────────────────
Claude Code        1.2.3           ✓ Installed
GitHub CLI         2.40.0          ✓ Installed (authenticated)
tmux               3.4             ✓ Installed
Agent Browser CLI  0.8.0           ✓ Installed
Ralph TUI          -               ✗ Not installed
```

### Step 3: Offer Installation

```
AskUserQuestion: "Install missing tools?"
├── "Yes, install all" → Run install commands
├── "Let me install manually" → Show commands
└── "Skip for now" → Continue without
```

### Step 4: Execute Installation

For each missing tool:

```
Installing Agent Browser CLI...
$ npm install -g agent-browser

Verifying...
$ agent-browser --version
agent-browser v0.8.0

✓ Success!
```

### Step 5: Configure Ralph TUI (if installed)

```
AskUserQuestion: "Configure Ralph TUI for this project?"
├── Yes, set up with defaults
├── Yes, let me customize
└── Skip for now

Creating .ralph-tui/ directory...
Copying config.toml template...
Copying prompt.hbs template...

✓ Ralph TUI configured
```

---

## Service-Specific CLIs

Beyond global tools, check for service CLIs based on project needs.

See `reference/tech-stack-clis.md` for complete list.

### Common Service CLIs

| Service | CLI | Install | Auth |
|---------|-----|---------|------|
| Vercel | `vercel` | `npm i -g vercel` | `vercel login` |
| Supabase | `supabase` | `npm i -g supabase` | `supabase login` |
| Stripe | `stripe` | `brew install stripe/stripe-cli/stripe` | `stripe login` |
| Sentry | `sentry-cli` | `npm i -g @sentry/cli` | `sentry-cli login` |

### CLI vs MCP Decision

| Service | Use CLI | Use MCP |
|---------|---------|---------|
| GitHub | ✓ (`gh`) | ✗ |
| Vercel | ✓ (`vercel`) | ✗ |
| Supabase | ✓ (`supabase`) | ✗ |
| Stripe | ✓ (`stripe`) | ✗ |
| Framework docs | ✗ | ✓ (context7) |
| UI components | ✗ | ✓ (shadcn) |

---

## Error Handling

### npm not available

```
Error: npm command not found

Node.js and npm are required.

Please install Node.js from: https://nodejs.org/

After installing, run /setup-claude again.
```

### Permission denied

```
Error: Permission denied during npm install

Solutions:
1. Fix npm permissions (recommended):
   https://docs.npmjs.com/resolving-eacces-permissions-errors

2. Use nvm (Node Version Manager):
   https://github.com/nvm-sh/nvm

3. Use sudo (if you trust the package):
   sudo npm install -g agent-browser
```

### Installation failed

```
Error: Installation failed

Command: npm install -g agent-browser
Error: [error message]

Solutions:
1. Check internet connection
2. Try again later
3. Install manually and re-run
```

---

## Tool Usage Tips

After installation:

### tmux
```
Quick usage:
- New session: tmux new-session -s feature-name
- Detach: Ctrl+b, then d
- Reattach: tmux attach -t feature-name
- List sessions: tmux list-sessions
- Kill session: tmux kill-session -t feature-name
```

### Git Worktrees
```
Quick usage:
- Create: git worktree add ../project-feature feature-branch
- List: git worktree list
- Remove: git worktree remove ../project-feature
```

### Agent Browser CLI
```
Quick usage:
- In Claude, use mcp__claude-in-chrome__* tools
- Direct: agent-browser navigate https://example.com
- Screenshot: agent-browser screenshot output.png
```

### Ralph TUI
```
Quick usage:
1. Create PRD: /prd
2. Convert to tasks: /ralph-tui-create-beads or /ralph-tui-create-json
3. Run: ralph-tui run

Config: .ralph-tui/config.toml
```

### GitHub CLI
```
Quick usage:
- Create PR: gh pr create
- View PR: gh pr view
- List issues: gh issue list
- API call: gh api repos/owner/repo
```

---

## Verification

After all installations:

```bash
echo "=== Tool Verification ===" && \
claude --version 2>/dev/null && echo "✓ Claude Code" || echo "✗ Claude Code" && \
gh --version 2>/dev/null && echo "✓ GitHub CLI" || echo "✗ GitHub CLI" && \
tmux -V 2>/dev/null && echo "✓ tmux" || echo "✗ tmux" && \
agent-browser --version 2>/dev/null && echo "✓ Agent Browser" || echo "✗ Agent Browser" && \
ralph-tui --version 2>/dev/null && echo "✓ Ralph TUI" || echo "✗ Ralph TUI"
```

Final report:
```
═══════════════════════════════════════════════════════════════════════════
Tools Verified
═══════════════════════════════════════════════════════════════════════════

✓ Claude Code v1.2.3
✓ GitHub CLI v2.40.0
✓ tmux v3.4
✓ Agent Browser CLI v0.8.0
✓ Ralph TUI v0.5.0

Your environment is ready for Ralph loops!

Note: Service CLIs (vercel, supabase, stripe) will be checked
during CLI Discovery phase based on your project's services.
```
