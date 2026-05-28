# Usage Guide

Complete guide for using claude-km-skill in your development workflow.

## Table of Contents

- [Quick Start](#quick-start)
- [Session Management](#session-management)
- [Knowledge Capture (4-Layer System)](#knowledge-capture-4-layer-system)
- [Git & Code Commands](#git--code-commands)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Quick Start

### 5-Minute Setup

```bash
# 1. Clone the skill
git clone https://github.com/goffity/claude-km-skill.git ~/.claude/skills/claude-km-skill

# 2. Initialize in your project
cd /path/to/your/project
~/.claude/skills/claude-km-skill/scripts/init.sh .

# 3. Start using with Claude Code
claude
```

### Your First Session

```bash
# Start a new session
/recap                    # Check current state

# Set your task
/focus Add user login     # Creates GitHub issue + feature branch

# Work on your code...
# When you learn something useful:
/mem "JWT refresh token"  # Quick capture

# Ready to commit
/commit                   # Atomic commit

# Create PR with tests
/pr                       # Runs tests, build, review, creates PR

# End session
/td done                  # Creates retrospective
```

---

## Session Management

### `/recap` - Start Your Day

Load context from your previous session.

```bash
/recap
```

**What it does:**
1. Shows current focus state (STATE, TASK, ISSUE, BRANCH)
2. Displays recent activity log
3. Shows git status and recent commits
4. Asks if you want to continue or start new task

**Output example:**
```
## Session Recap

### Current Focus
STATE: working
TASK: Implement user authentication
SINCE: 2025-01-20 14:30
ISSUE: #42
BRANCH: feat/42-user-auth

### Recent Activity
2025-01-20 14:30 | working | Implement user authentication (#42)

### Git Status
Branch: feat/42-user-auth
Changes: 3 modified files

### Action Required
งานค้างอยู่: Implement user authentication
ต้องการ: ทำต่อ / เริ่มงานใหม่
```

---

### `/focus [task]` - Set Your Goal

Create a GitHub issue and start working.

```bash
/focus Implement dark mode toggle
```

**What it does:**
1. Asks for task details (type, overview, acceptance criteria)
2. Creates GitHub issue with structured format
3. Creates feature branch (`feat/123-dark-mode`)
4. Updates `docs/current.md` with focus state
5. Logs activity

**Interactive flow:**
```
งานนี้เป็นประเภทอะไร?
1. feat - Feature ใหม่
2. fix - Bug fix
3. refactor - Code restructure
4. docs - Documentation

[เลือก type]

Overview: อธิบายสั้นๆ ว่างานนี้คืออะไร
[ใส่คำอธิบาย]

Acceptance Criteria: เกณฑ์ทดสอบ
[ใส่ criteria]
```

**Result:**
```
## Focus Set

Issue Created: #123
Title: feat: Implement dark mode toggle
Branch: feat/123-dark-mode

STATE: working
TASK: Implement dark mode toggle
SINCE: 2025-01-20 15:00

พร้อมเริ่มงาน! ใช้ /td เมื่อจบ session
```

---

### `/td [status]` - End Your Session

Create retrospective and wrap up.

```bash
/td           # Interactive - asks for status
/td done      # Task completed
/td pending   # Work in progress, will continue later
/td blocked   # Stuck on something
```

**What it does:**
1. Gathers session info (what you did, test results)
2. Adds comment to GitHub issue
3. Creates retrospective file with Before/After context
4. Updates focus state
5. Commits documentation

**Template creates:**
```markdown
# Implement dark mode toggle

## Context: Before
- Problem: No dark mode support
- Existing Behavior: Only light theme available

## Context: After
- Solution: Added ThemeProvider with toggle
- New Behavior: Users can switch themes

## Lessons Learned
- CSS variables make theming easier
- Persist theme choice in localStorage
```

---

## Knowledge Capture (4-Layer System)

```
Layer 1: /mem      → Quick capture during work
Layer 2: /distill  → Extract patterns from learnings
Layer 3: /td       → Session retrospective
Layer 4: /improve  → Work on pending items
```

### `/mem [topic]` - Quick Capture (Layer 1)

Capture insights while you work. Fast and lightweight.

```bash
/mem JWT refresh token pattern
/mem "MongoDB connection pooling gotcha"
```

**Output:** `docs/learnings/YYYY-MM/DD/HH.MM_jwt-refresh-token.md`

**When to use:**
- Found a tricky bug solution
- Discovered a useful pattern
- Hit a gotcha worth remembering
- Learned something new

**Template:**
```markdown
# JWT Refresh Token Pattern

| Field | Value |
|-------|-------|
| Captured | 2025-01-20 15:30 |
| Branch | feat/42-user-auth |
| Context | Implementing token refresh |

## Key Insight

> Use sliding window for refresh tokens to prevent session hijacking

## What We Learned

- Refresh tokens should rotate on each use
- Store token family to detect reuse attacks

## Gotchas & Warnings

- Don't store refresh tokens in localStorage

## Tags

`jwt` `security` `authentication`
```

---

### `/distill [topic]` - Extract Patterns (Layer 2)

When you have 3+ learnings on the same topic, synthesize them.

```bash
/distill authentication-patterns
```

**Input:** Scans `docs/learnings/`
**Output:** `docs/knowledge-base/authentication-patterns.md`

**When to use:**
- Multiple learnings on same topic
- Found a reusable pattern
- Weekly knowledge review

**Template:**
```markdown
# Authentication Patterns

## The Problem

| Attempt | Result |
|---------|--------|
| Store tokens in localStorage | XSS vulnerability |
| Long-lived tokens | Security risk |

## The Solution

### Pattern: Secure Token Storage

```javascript
// Use httpOnly cookies for refresh tokens
res.cookie('refreshToken', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});
```

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| localStorage for sensitive tokens | httpOnly cookies |
| Never-expiring tokens | Short-lived + refresh |

## When to Apply

- Use when: Building user authentication
- Don't use when: Service-to-service auth (use API keys)
```

---

### `/improve` - Work on Pending Items (Layer 4)

Find and work on improvements from your knowledge base.

```bash
/improve
```

**Scans (in priority order):**
1. `docs/knowledge-base/` - Patterns to implement
2. `docs/retrospective/` - Future improvements (`- [ ]`)
3. `docs/learnings/` - Gotchas to fix

**Output:**
```markdown
## Pending Improvements

### From Knowledge Base - Priority 1
authentication-patterns.md:
1. [ ] Apply secure cookie pattern to all auth endpoints

### From Retrospectives - Priority 2
retrospective_2025-01-19.md:
2. [ ] Add rate limiting to login endpoint

เลือก item (หมายเลข, 'all', หรือ 'skip'):
```

---

## Git & Code Commands

### `/commit` - Atomic Commits

Create clean, focused commits.

```bash
/commit
```

**What it does:**
1. Analyzes staged/unstaged changes
2. Detects if changes should be split (mixed concerns)
3. Helps you commit atomically

**Best for:**
- Single logical changes
- After completing a feature chunk
- Before switching tasks

---

### `/pr` - Create Pull Request

Full PR workflow: test → build → review → create PR.

```bash
/pr
```

**What it does:**
1. Runs test suite (`make test`)
2. Runs build (`make build`)
3. Performs code review (using code-reviewer agent)
4. Creates PR with summary
5. Starts auto-respond daemon for review comments

**Prerequisites:**
- Tests must pass
- Build must succeed
- No critical code review issues

---

### `/review` - Manual Code Review

Get code reviewed before committing.

```bash
/review
```

**Uses code-reviewer agent to check:**
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code style and best practices

---

### `/pr-review` - Respond to PR Feedback

Handle reviewer comments on your PR.

```bash
/pr-review
```

**What it does:**
1. Fetches pending review comments
2. Analyzes feedback
3. Makes code changes
4. Replies to comments
5. Pushes updates

---

### `/pr-poll` - PR Review Polling

Manage automatic PR review monitoring.

```bash
/pr-poll start     # Start monitoring
/pr-poll stop      # Stop monitoring
/pr-poll status    # Check daemon status
/pr-poll auto      # Auto-respond to reviews
```

---

## Workflow Examples

### Example 1: Feature Development

Complete workflow for adding a new feature.

```bash
# 1. Start session
/recap                              # Check previous state

# 2. Set focus
/focus Add user profile page        # Creates issue #50, branch feat/50-profile

# 3. Work on feature
# ... write code ...

# 4. Capture insights
/mem "Avatar upload needs resize"   # Quick learning

# 5. Commit progress
/commit                             # Atomic commit

# 6. More work...
# ... continue coding ...

# 7. Ready for PR
/pr                                 # Tests, build, review, create PR

# 8. End session
/td done                            # Retrospective, closes session
```

---

### Example 2: Bug Fix

Quick bug fix workflow.

```bash
# 1. Start
/recap

# 2. Set focus
/focus Fix login timeout issue      # Creates issue #51, branch fix/51-login-timeout

# 3. Investigate and fix
# ... debug and fix ...

# 4. If learned something
/mem "Connection pool exhaustion"

# 5. Commit and PR
/commit
/pr

# 6. Done
/td done
```

---

### Example 3: Knowledge Review (Weekly)

Review and consolidate learnings.

```bash
# 1. Check pending learnings
ls docs/learnings/

# 2. Distill related learnings
/distill error-handling-patterns    # Combine 3+ related learnings

# 3. Work on improvements
/improve                            # Find pending items from knowledge base

# 4. Capture the review session
/td done
```

---

### Example 4: Continuing Previous Work

Resume work from a previous session.

```bash
# 1. Start session
/recap                              # Shows pending task

# Output:
# งานค้างอยู่: Implement dark mode
# ตั้งแต่: 2025-01-19 16:00
#
# ต้องการ: ทำต่อ / เริ่มงานใหม่

# 2. Choose "ทำต่องานเดิม"
# Switches to correct branch automatically

# 3. Continue working
# ...

# 4. Finish
/pr
/td done
```

---

### Example 5: Multi-Tab Development

Work on multiple tasks in parallel using terminal tabs.

```bash
# Terminal 1: Feature A
cd ~/project-feature-a
claude
/focus Feature A

# Terminal 2: Bug fix
cd ~/project-bugfix
claude
/focus Fix critical bug

# Notifications alert you when Claude needs input
# Switch tabs as needed
```

**Setup git worktrees for parallel development:**
```bash
git worktree add ../project-feature-a -b feature-a
git worktree add ../project-bugfix -b bugfix-123
```

---

## Best Practices

### Do's

| Practice | Why |
|----------|-----|
| Start with `/recap` | Know your context before working |
| Use `/focus` for every task | Creates proper tracking (issue, branch) |
| Capture learnings with `/mem` | Build your knowledge base |
| End sessions with `/td` | Create retrospectives for future reference |
| Use `/commit` frequently | Small, atomic commits are easier to review |
| Run `/pr` before pushing | Catch issues early |

### Don'ts

| Avoid | Why |
|-------|-----|
| Skipping `/focus` | No issue tracking, no proper branch |
| Long sessions without `/mem` | Lost learnings |
| Pushing without `/pr` | Skip tests/review |
| Forgetting `/td` | No session record |
| Working on main branch | Always use feature branches |

### Command Quick Reference

| Phase | Command | Purpose |
|-------|---------|---------|
| Start | `/recap` | Load context |
| Plan | `/focus [task]` | Set goal, create issue |
| Work | `/mem [topic]` | Capture insights |
| Work | `/commit` | Atomic commits |
| Work | `/review` | Manual code review |
| Ship | `/pr` | Test + build + PR |
| End | `/td [status]` | Retrospective |
| Improve | `/distill` | Extract patterns |
| Improve | `/improve` | Work on pending items |

---

## File Structure

After using the skill, your project will have:

```
project/
├── .claude/
│   ├── commands/          # Slash commands
│   └── agents/            # AI agents
└── docs/
    ├── current.md         # Current focus state
    ├── WIP.md            # Paused tasks
    ├── logs/
    │   └── activity.log  # Activity history
    ├── learnings/        # Layer 1: Quick captures
    │   └── YYYY-MM/
    │       └── DD/
    │           └── HH.MM_topic.md
    ├── knowledge-base/   # Layer 2: Patterns
    │   └── topic.md
    └── retrospective/    # Layer 3: Session reviews
        └── YYYY-MM/
            └── retrospective_YYYY-MM-DD_hhmmss.md
```

---

## Getting Help

- View all commands: Check `assets/commands/` in the skill directory
- GitHub Issues: [github.com/goffity/claude-km-skill/issues](https://github.com/goffity/claude-km-skill/issues)
- README: See [README.md](README.md) for installation and advanced features
