# Claude Code Hooks

## Patterns


---
  #### **Name**
Block-at-Submit Pattern
  #### **Description**
Validate before commit, not on every write
  #### **When To Use**
Enforcing test passage before commits
  #### **Implementation**
    // Block-at-Submit: Only check when committing, not on every write
    // This lets Claude finish its plan before validation
    
    // .claude/settings.local.json
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash(git commit*)",
            "hooks": [
              {
                "type": "command",
                "command": "sh -c '[ -f /tmp/tests-passed ] || (echo \"Tests must pass before commit. Run tests first.\" && exit 1)'"
              }
            ]
          }
        ],
        "PostToolUse": [
          {
            "matcher": "Bash(npm test*)",
            "hooks": [
              {
                "type": "command",
                "command": "sh -c 'if [ $TOOL_EXIT_CODE -eq 0 ]; then touch /tmp/tests-passed; else rm -f /tmp/tests-passed; fi'"
              }
            ]
          }
        ]
      }
    }
    
    // Result: Claude can write code freely, but must pass tests before commit
    // Creates a natural "test-and-fix" loop until build is green
    

---
  #### **Name**
Auto-Format on Write
  #### **Description**
Run formatters after every file edit
  #### **When To Use**
Ensuring consistent code style
  #### **Implementation**
    // Auto-format after every file write
    // PostToolUse runs after successful tool execution
    
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "prettier --write \"$TOOL_INPUT_FILE_PATH\" 2>/dev/null || true"
              }
            ]
          },
          {
            "matcher": "Write(*.py)|Edit(*.py)",
            "hooks": [
              {
                "type": "command",
                "command": "black \"$TOOL_INPUT_FILE_PATH\" 2>/dev/null || true"
              }
            ]
          }
        ]
      }
    }
    
    // Available environment variables:
    // $TOOL_INPUT_FILE_PATH - Path of file being written/edited
    // $TOOL_EXIT_CODE - Exit code of the tool (PostToolUse only)
    // $HOOK_EVENT - The event type (PreToolUse, PostToolUse, etc.)
    

---
  #### **Name**
Session Context Injection
  #### **Description**
Load context automatically at session start
  #### **When To Use**
Ensuring Claude always has project context
  #### **Implementation**
    // SessionStart hook to inject context
    // Runs once when Claude Code session begins
    
    {
      "hooks": {
        "SessionStart": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "cat ~/.claude/project-context.md"
              }
            ]
          },
          {
            "hooks": [
              {
                "type": "command",
                "command": "git log --oneline -10 2>/dev/null | head -5"
              }
            ]
          },
          {
            "hooks": [
              {
                "type": "command",
                "command": "jira-cli list --assignee=me --status='In Progress' 2>/dev/null || echo 'No active tickets'"
              }
            ]
          }
        ]
      }
    }
    
    // Project context file example (~/.claude/project-context.md):
    // # Current Sprint Goals
    // - Complete authentication flow
    // - Fix performance issues in dashboard
    //
    // # Team Conventions
    // - All PRs need 2 approvals
    // - Run `npm test` before committing
    

---
  #### **Name**
Dangerous Command Blocking
  #### **Description**
Prevent risky operations
  #### **When To Use**
Protecting production configs and sensitive files
  #### **Implementation**
    // Block dangerous operations before they happen
    // PreToolUse with exit code 1 blocks the action
    
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Write(.env*)|Edit(.env*)",
            "hooks": [
              {
                "type": "command",
                "command": "echo 'BLOCKED: Direct .env modification not allowed. Use environment management tools.' && exit 1"
              }
            ]
          },
          {
            "matcher": "Bash(rm -rf*)|Bash(sudo*)",
            "hooks": [
              {
                "type": "command",
                "command": "echo 'BLOCKED: Destructive command requires manual execution.' && exit 1"
              }
            ]
          },
          {
            "matcher": "Bash(git push*--force*)|Bash(git push*-f*)",
            "hooks": [
              {
                "type": "command",
                "command": "echo 'BLOCKED: Force push requires manual confirmation.' && exit 1"
              }
            ]
          },
          {
            "matcher": "Write(**/production/**)|Edit(**/production/**)",
            "hooks": [
              {
                "type": "command",
                "command": "echo 'BLOCKED: Production config changes require manual review.' && exit 1"
              }
            ]
          }
        ]
      }
    }
    

---
  #### **Name**
Security Scanning Hook
  #### **Description**
Run security checks on code changes
  #### **When To Use**
Catching security issues before they're committed
  #### **Implementation**
    // Security scan after file modifications
    // Integrate with tools like Gitleaks, Trivy, or Semgrep
    
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write(*.ts)|Write(*.js)|Write(*.py)",
            "hooks": [
              {
                "type": "command",
                "command": "gitleaks detect --source=\"$TOOL_INPUT_FILE_PATH\" --no-git 2>/dev/null && echo '✓ No secrets detected'"
              }
            ]
          }
        ],
        "PreToolUse": [
          {
            "matcher": "Bash(git commit*)",
            "hooks": [
              {
                "type": "command",
                "command": "semgrep scan --config=auto --error 2>/dev/null || (echo 'Security issues found. Fix before committing.' && exit 1)"
              }
            ]
          }
        ]
      }
    }
    

---
  #### **Name**
Notification Hook for Long Tasks
  #### **Description**
Alert when Claude needs attention
  #### **When To Use**
Background tasks that may require input
  #### **Implementation**
    // Notification hook to alert user
    // Runs when Claude needs permission or has a question
    
    {
      "hooks": {
        "Notification": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude needs your attention\" with title \"Claude Code\"' 2>/dev/null || notify-send 'Claude Code' 'Claude needs your attention' 2>/dev/null || echo 'Notification: Claude needs attention'"
              }
            ]
          }
        ],
        "Stop": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "echo 'Session complete' && say 'Claude Code has finished' 2>/dev/null || true"
              }
            ]
          }
        ]
      }
    }
    

## Anti-Patterns


---
  #### **Name**
Hook on Every Keystroke
  #### **Description**
Blocking or running heavy scripts on every small action
  #### **Why Bad**
    Creates friction, slows down Claude significantly, and can cause
    timeout issues. Claude may avoid using certain tools to bypass hooks.
    
  #### **What To Do Instead**
    Focus hooks on critical decision points: commit, deploy, push.
    Let Claude work freely, validate at submission boundaries.
    

---
  #### **Name**
Blocking Without Clear Message
  #### **Description**
Exiting with code 1 but not explaining why
  #### **Why Bad**
    Claude doesn't know what went wrong or how to fix it.
    Creates frustrating loops without progress.
    
  #### **What To Do Instead**
    Always echo a clear message before exit 1:
    echo "BLOCKED: Tests must pass. Run 'npm test' first." && exit 1
    

---
  #### **Name**
Complex Logic in Hook Commands
  #### **Description**
Writing elaborate shell one-liners in hooks
  #### **Why Bad**
    Hard to debug, maintain, and prone to escaping issues.
    JSON escaping combined with shell escaping is error-prone.
    
  #### **What To Do Instead**
    Create dedicated scripts and call them from hooks:
    "command": "./scripts/validate-commit.sh"
    

---
  #### **Name**
Ignoring Hook Timeouts
  #### **Description**
Running long-running processes in hooks
  #### **Why Bad**
    Hooks have timeouts. Long processes get killed, leaving
    inconsistent state.
    
  #### **What To Do Instead**
    Keep hooks fast (<5 seconds). For long tasks, spawn background
    processes or use async patterns.
    

---
  #### **Name**
Hooks as Only Validation
  #### **Description**
Relying solely on hooks without CLAUDE.md guidance
  #### **Why Bad**
    Hooks block but don't teach. Claude keeps hitting the same
    blocks without understanding why.
    
  #### **What To Do Instead**
    Combine hooks (enforcement) with CLAUDE.md (guidance).
    Explain patterns in CLAUDE.md, enforce in hooks.
    