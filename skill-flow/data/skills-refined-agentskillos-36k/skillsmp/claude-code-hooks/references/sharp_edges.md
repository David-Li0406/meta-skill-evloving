# Claude Code Hooks - Sharp Edges

## Hook Matcher Glob Syntax

### **Id**
hook-matcher-glob-syntax
### **Summary**
Hook matchers use glob patterns, not regex
### **Severity**
high
### **Situation**
Hook doesn't match expected tools, silently fails
### **Why**
  Matchers use glob-style patterns like "Bash(git*)" not regex.
  Using regex patterns causes no matches, hook never fires.
  No error message when matcher doesn't match anything.
  
### **Solution**
  // Correct glob patterns for hook matchers
  
  // WRONG - regex patterns don't work
  {
    "matcher": "Bash(git\\s+commit.*)"  // Won't match
  }
  
  // CORRECT - glob patterns
  {
    "matcher": "Bash(git commit*)"  // Matches git commit, git commit -m, etc.
  }
  
  // Common matcher patterns:
  {
    // Match specific tool
    "matcher": "Write",           // All Write operations
    "matcher": "Edit",            // All Edit operations
    "matcher": "Bash",            // All Bash commands
  
    // Match with file patterns
    "matcher": "Write(*.ts)",     // TypeScript files only
    "matcher": "Edit(src/**/*)",  // Files in src directory
    "matcher": "Write(.env*)",    // Environment files
  
    // Match command patterns
    "matcher": "Bash(npm*)",      // npm commands
    "matcher": "Bash(git push*)", // git push variations
  
    // Multiple patterns (use array)
    "matcher": ["Write(*.ts)", "Write(*.js)", "Edit(*.ts)", "Edit(*.js)"]
  }
  
  // Debug matchers with --mcp-debug flag:
  // claude --mcp-debug
  
### **Symptoms**
  - Hook never fires
  - No error messages
  - Works for some tools but not others
### **Detection Pattern**
matcher.*\\\\|matcher.*\\+|matcher.*\\?

## Hook Environment Variables

### **Id**
hook-environment-variables
### **Summary**
Wrong environment variable names in hooks
### **Severity**
high
### **Situation**
Hook script fails because variables are undefined
### **Why**
  Different hook events have different available variables.
  Using wrong variable name gives empty string, not error.
  Variable names are case-sensitive.
  
### **Solution**
  // Available environment variables by hook type
  
  // PreToolUse and PostToolUse:
  {
    "TOOL_NAME": "Write",              // Name of the tool
    "TOOL_INPUT_FILE_PATH": "/path",   // For file operations
    "TOOL_INPUT_COMMAND": "npm test",  // For Bash commands
    "TOOL_EXIT_CODE": "0",             // PostToolUse only
  
    // Hook context
    "HOOK_EVENT": "PreToolUse",        // Event type
    "SESSION_ID": "abc123"             // Current session
  }
  
  // SessionStart:
  {
    "WORKING_DIRECTORY": "/project",   // Project root
    "SESSION_ID": "abc123"
  }
  
  // Notification:
  {
    "NOTIFICATION_MESSAGE": "text",    // Notification content
    "SESSION_ID": "abc123"
  }
  
  // Stop:
  {
    "SESSION_ID": "abc123",
    "EXIT_REASON": "complete"          // Why session ended
  }
  
  // Safe variable access in shell:
  {
    "command": "sh -c '[ -n \"$TOOL_INPUT_FILE_PATH\" ] && prettier --write \"$TOOL_INPUT_FILE_PATH\"'"
  }
  
  // Debug variables:
  {
    "command": "env | grep -E '^(TOOL_|HOOK_|SESSION_)' >> /tmp/hook-debug.log"
  }
  
### **Symptoms**
  - Empty strings in hook output
  - Commands fail silently
  - Partial execution
### **Detection Pattern**
TOOL_PATH|TOOL_FILE|FILE_PATH[^_]

## Hook Json Escaping

### **Id**
hook-json-escaping
### **Summary**
JSON escaping breaks shell commands
### **Severity**
high
### **Situation**
Complex shell commands fail due to escaping issues
### **Why**
  Hooks are configured in JSON.
  Shell commands have their own escaping rules.
  Double-escaping creates garbled commands.
  
### **Solution**
  // Escaping levels in hook commands
  
  // PROBLEM: Double quotes inside command
  // WRONG
  {
    "command": "echo "Hello World""  // JSON syntax error
  }
  
  // CORRECT - escape inner quotes
  {
    "command": "echo \"Hello World\""
  }
  
  // PROBLEM: Dollar signs for variables
  // WRONG - JSON tries to interpret
  {
    "command": "echo $TOOL_INPUT_FILE_PATH"  // May not expand
  }
  
  // CORRECT - use sh -c wrapper
  {
    "command": "sh -c 'echo \"$TOOL_INPUT_FILE_PATH\"'"
  }
  
  // PROBLEM: Complex logic
  // WRONG - unreadable and error-prone
  {
    "command": "if [ -f /tmp/x ]; then echo \"yes\"; else echo \"no\" && exit 1; fi"
  }
  
  // CORRECT - use external script
  {
    "command": "./scripts/check-file.sh"
  }
  
  // The script (scripts/check-file.sh):
  #!/bin/bash
  if [ -f /tmp/x ]; then
    echo "yes"
  else
    echo "no"
    exit 1
  fi
  
  // BEST PRACTICE: Keep hook commands simple
  // - Single command or script call
  // - Use scripts for logic
  // - Avoid nested quotes when possible
  
### **Symptoms**
  - Syntax errors in hooks
  - Commands not executing as expected
  - Random characters in output
### **Detection Pattern**
command.*".*".*"|command.*\\$\\{|command.*`

## Hook Timeout Behavior

### **Id**
hook-timeout-behavior
### **Summary**
Long-running hooks get killed silently
### **Severity**
medium
### **Situation**
Hook appears to complete but actually timed out
### **Why**
  Hooks have execution timeouts (typically 30 seconds).
  Timeout kills the process mid-execution.
  No clear error message, just incomplete results.
  
### **Solution**
  // Handle hook timeouts properly
  
  // Default timeout is ~30 seconds
  // Can't be extended in config
  
  // PATTERN 1: Fast-fail approach
  {
    "command": "timeout 5 npm test -- --bail || echo 'Tests taking too long, run manually'"
  }
  
  // PATTERN 2: Background process for long tasks
  {
    "command": "sh -c '(npm test > /tmp/test-output.log 2>&1 &) && echo \"Tests running in background\"'"
  }
  
  // PATTERN 3: Quick check, defer full run
  {
    "command": "sh -c 'if git diff --cached --name-only | grep -q \"\\.ts$\"; then echo \"TypeScript changed - run tests before push\"; fi'"
  }
  
  // PATTERN 4: Marker file approach
  // Instead of blocking on test completion:
  {
    "PostToolUse": [
      {
        "matcher": "Bash(npm test*)",
        "hooks": [
          {
            "command": "sh -c '[ $TOOL_EXIT_CODE -eq 0 ] && touch /tmp/tests-passed'"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash(git push*)",
        "hooks": [
          {
            "command": "sh -c '[ -f /tmp/tests-passed ] || (echo \"Run tests first\" && exit 1)'"
          }
        ]
      }
    ]
  }
  
  // ANTI-PATTERN: Long synchronous operations
  // DON'T:
  {
    "command": "npm run full-test-suite && npm run e2e && npm run lint"
  }
  
### **Symptoms**
  - Incomplete test runs
  - Hooks that "work sometimes"
  - Inconsistent state between runs
### **Detection Pattern**
command.*(&&.*){3,}|npm run.*&&.*npm run

## Hook Exit Code Meaning

### **Id**
hook-exit-code-meaning
### **Summary**
Exit codes affect hook behavior differently
### **Severity**
medium
### **Situation**
Non-zero exit doesn't block, or zero exit blocks unexpectedly
### **Why**
  PreToolUse: exit 1 = block the tool
  PostToolUse: exit 1 = log warning but continue
  Different semantics cause confusion.
  
### **Solution**
  // Exit code behavior by hook type
  
  // PreToolUse: Exit code determines if tool runs
  {
    "PreToolUse": [
      {
        "matcher": "Bash(git push*)",
        "hooks": [
          {
            // exit 0 = allow push
            // exit 1 = block push
            "command": "sh -c '[ -f /tmp/tests-passed ] && exit 0 || exit 1'"
          }
        ]
      }
    ]
  }
  
  // PostToolUse: Exit code is informational
  {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            // exit 1 logs warning but doesn't undo write
            // Tool already completed
            "command": "prettier --check \"$TOOL_INPUT_FILE_PATH\" || echo 'Format warning'"
          }
        ]
      }
    ]
  }
  
  // Notification/Stop: Exit code mostly ignored
  // These are fire-and-forget
  
  // IMPORTANT: Always provide clear message before exit
  {
    "command": "sh -c 'if ! npm test; then echo \"BLOCKED: Tests failed. Fix and retry.\"; exit 1; fi'"
  }
  
  // DON'T: Silent failures
  {
    "command": "npm test"  // No message if fails
  }
  
### **Symptoms**
  - Tool runs when it should be blocked
  - Confusing error messages
  - Actions blocked unexpectedly
### **Detection Pattern**
exit 1[^;"\n]|exit 0[^;"\n]

## Hook State Persistence

### **Id**
hook-state-persistence
### **Summary**
Hook state doesn't persist across sessions
### **Severity**
medium
### **Situation**
Marker files lost, hooks stop working after restart
### **Why**
  Hooks use /tmp for state (tests-passed markers, etc.).
  /tmp is cleared on reboot.
  Different sessions may have different state expectations.
  
### **Solution**
  // Manage hook state properly
  
  // PATTERN 1: Session-scoped state (default)
  // Good for: test gates within single session
  {
    "command": "sh -c 'touch /tmp/claude-tests-passed-$SESSION_ID'"
  }
  
  // Check session-scoped state
  {
    "command": "sh -c '[ -f /tmp/claude-tests-passed-$SESSION_ID ] || exit 1'"
  }
  
  // PATTERN 2: Project-scoped state
  // Good for: persistent markers
  {
    "command": "sh -c 'touch .claude-state/tests-passed'"
  }
  
  // Initialize in SessionStart
  {
    "SessionStart": [
      {
        "hooks": [
          { "command": "mkdir -p .claude-state" }
        ]
      }
    ]
  }
  
  // PATTERN 3: Git-based state
  // Good for: team-wide state
  {
    "command": "sh -c 'git stash list | grep -q claude-checkpoint && echo \"Has checkpoint\" || echo \"No checkpoint\"'"
  }
  
  // PATTERN 4: Time-based expiry
  // Good for: test results that expire
  {
    "command": "sh -c 'find /tmp -name \"tests-passed\" -mmin -10 | grep -q . || (echo \"Tests expired, rerun\" && exit 1)'"
  }
  
  // Clean up on session end
  {
    "Stop": [
      {
        "hooks": [
          { "command": "rm -f /tmp/claude-tests-passed-$SESSION_ID" }
        ]
      }
    ]
  }
  
### **Symptoms**
  - Hooks work then stop working
  - State leaks between sessions
  - Inconsistent behavior on restart
### **Detection Pattern**
touch /tmp/|/tmp/[^/]+[^"]