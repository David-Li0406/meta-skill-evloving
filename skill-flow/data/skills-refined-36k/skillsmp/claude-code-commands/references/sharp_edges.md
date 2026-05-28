# Claude Code Commands - Sharp Edges

## Command Location Priority

### **Id**
command-location-priority
### **Summary**
Commands in wrong location aren't discovered
### **Severity**
high
### **Situation**
Created command but /command doesn't appear
### **Why**
  Claude Code looks in specific locations with priority order.
  Project commands in .claude/commands/ (team-shared).
  Personal commands in ~/.claude/commands/ (user-only).
  Wrong location means command not found.
  
### **Solution**
  // Command location hierarchy and discovery
  
  // Project commands (checked into git, shared with team)
  .claude/commands/
  ├── feature.md      # /feature
  ├── review.md       # /review
  └── deploy.md       # /deploy
  
  // Personal commands (not in git, user-specific)
  ~/.claude/commands/
  ├── my-workflow.md  # /my-workflow
  └── scratch.md      # /scratch
  
  // Priority order:
  // 1. .claude/commands/ (project)
  // 2. ~/.claude/commands/ (personal)
  
  // If same name exists in both, project wins
  
  // Verify command is discovered:
  // Type / in Claude Code to see available commands
  // Commands appear in the autocomplete menu
  
  // Common mistakes:
  // WRONG: commands/.claude/feature.md
  // WRONG: .claude/command/feature.md (singular)
  // WRONG: claude/commands/feature.md (no dot)
  
  // CORRECT: .claude/commands/feature.md
  
### **Symptoms**
  - Command not appearing in / menu
  - "Unknown command" error
  - Works for you but not teammates
### **Detection Pattern**
commands/\\.|command/|claude/commands[^/]

## Arguments Not Substituting

### **Id**
arguments-not-substituting
### **Summary**
$ARGUMENTS appears literally instead of being replaced
### **Severity**
high
### **Situation**
Command shows $ARGUMENTS instead of user's input
### **Why**
  $ARGUMENTS must be exact - case sensitive, with dollar sign.
  Common typos prevent substitution.
  No error message when substitution fails.
  
### **Solution**
  // Correct $ARGUMENTS usage
  
  // CORRECT
  # Feature: $ARGUMENTS
  You will implement a feature: $ARGUMENTS
  
  // WRONG - won't substitute
  # Feature: $Arguments         # Wrong case
  # Feature: $ARGUMENT          # Missing S
  # Feature: ${ARGUMENTS}       # Wrong syntax
  # Feature: $arguments         # Wrong case
  # Feature: ARGUMENTS          # Missing $
  
  // Multiple uses work:
  The feature "$ARGUMENTS" will be implemented.
  First, research $ARGUMENTS in the codebase.
  Create branch feature/$ARGUMENTS.
  
  // Usage examples in command:
  ---
  # Usage: /feature add user avatars
  # $ARGUMENTS becomes: "add user avatars"
  
  // Handling optional arguments:
  # Command with optional argument
  
  ## Input
  Feature request: $ARGUMENTS
  
  If no arguments provided, ask the user what feature
  they want to implement.
  
  // Parsing complex arguments:
  # DB Command: $ARGUMENTS
  
  Parse $ARGUMENTS as follows:
  - First word: operation (migrate, seed, query)
  - Rest: parameters for that operation
  
  Example: "query SELECT * FROM users"
  - Operation: query
  - Parameters: SELECT * FROM users
  
### **Symptoms**
  - Literal $ARGUMENTS in output
  - Claude asks for feature name after invocation
  - Substitution works sometimes but not others
### **Detection Pattern**
\$[Aa]rguments|\$ARGUMENT[^S]|\$\{ARGUMENTS\}

## File Reference Not Loading

### **Id**
file-reference-not-loading
### **Summary**
@file reference doesn't include file contents
### **Severity**
medium
### **Situation**
File reference treated as literal text
### **Why**
  @file syntax only works in certain positions.
  File path must be relative to project root.
  File must exist at that path.
  
### **Solution**
  // @file reference patterns
  
  // CORRECT - on its own line
  @src/architecture.md
  
  // CORRECT - after section header
  ## Guidelines
  @docs/style-guide.md
  
  // MIGHT NOT WORK - inline
  Follow the rules in @src/rules.md and continue.
  
  // CORRECT - multiple files
  ## Reference Files
  @src/types.ts
  @src/config.ts
  @src/utils.ts
  
  // Path resolution:
  // Paths are relative to project root
  // NOT relative to the command file
  
  // Example structure:
  project/
  ├── .claude/commands/review.md    # Command file
  ├── src/architecture.md           # @src/architecture.md
  └── docs/style.md                 # @docs/style.md
  
  // In review.md:
  ## Architecture
  @src/architecture.md
  
  # NOT: @../src/architecture.md
  
  // Verify file exists:
  // If file doesn't exist, reference is ignored silently
  
  // Alternative: explicit read instruction
  ## Guidelines
  First, read the file at src/architecture.md and follow
  its patterns in this review.
  
### **Symptoms**
  - File contents not appearing in context
  - "@filename" treated as literal text
  - Works in some commands but not others
### **Detection Pattern**
@\\./|@\\.\\./

## Command Markdown Rendering

### **Id**
command-markdown-rendering
### **Summary**
Markdown in commands renders unexpectedly
### **Severity**
medium
### **Situation**
Command formatting breaks or behaves oddly
### **Why**
  Commands are markdown files.
  Code blocks, headers, and formatting are interpreted.
  Some markdown affects how Claude processes the command.
  
### **Solution**
  // Markdown in commands - what matters
  
  // HEADERS - structure the command
  # Main Title (usually command name)
  ## Sections (workflow steps)
  ### Subsections (details)
  
  // CODE BLOCKS - treated as executable
  ```bash
  npm test
  ```
  // Claude may run this or show it to user
  
  // Make it clear if code should run:
  Run this command:
  ```bash
  npm test
  ```
  
  // Or if it's just an example:
  Example output format (do not run):
  ```json
  {"status": "ok"}
  ```
  
  // CHECKLISTS - Claude tracks these
  - [ ] First task
  - [ ] Second task
  
  // Claude will try to complete checkboxes
  
  // HORIZONTAL RULES - can separate sections
  ---
  // Often used before "Usage:" comments
  
  // EMPHASIS - interpreted but subtle
  **Important**: Do not skip this step.
  *Optional*: You may also...
  
  // ESCAPING - when needed
  Show the literal text: `$ARGUMENTS`
  // Backticks prevent substitution
  
  // LINKS - typically ignored
  [Documentation](https://...)
  // Claude won't fetch these
  
  // TABLES - work but complex
  | Column | Column |
  |--------|--------|
  | Data   | Data   |
  
### **Symptoms**
  - Unexpected code execution
  - Lost formatting in output
  - Sections merged or separated wrong
### **Detection Pattern**
```.*```.*```|# #|---.*---

## Command Length Limits

### **Id**
command-length-limits
### **Summary**
Very long commands get truncated or cause issues
### **Severity**
medium
### **Situation**
Complex command doesn't execute completely
### **Why**
  Commands add to context window.
  Very long commands crowd out conversation.
  Claude may not process all sections.
  
### **Solution**
  // Managing command length
  
  // PROBLEM: Huge command with everything
  // .claude/commands/full-workflow.md (500+ lines)
  # Complete Development Workflow
  ## Research... (100 lines)
  ## Design... (100 lines)
  ## Implement... (100 lines)
  ## Test... (100 lines)
  ## Deploy... (100 lines)
  
  // SOLUTION: Modular commands
  // .claude/commands/research.md
  # Research: $ARGUMENTS
  [focused research workflow]
  
  // .claude/commands/implement.md
  # Implement: $ARGUMENTS
  [focused implementation workflow]
  
  // .claude/commands/test.md
  # Test: $ARGUMENTS
  [focused testing workflow]
  
  // PATTERN: Index command that chains
  // .claude/commands/workflow.md
  # Full Workflow: $ARGUMENTS
  
  This workflow consists of these steps:
  1. /research $ARGUMENTS
  2. /implement $ARGUMENTS
  3. /test $ARGUMENTS
  
  Start with step 1.
  
  // PATTERN: Reference files instead of inline
  // Instead of 100 lines of checklist:
  ## Review Checklist
  @.claude/checklists/security-review.md
  
  // GUIDELINE: Commands should be <100 lines
  // If longer, consider splitting or using @references
  
### **Symptoms**
  - Claude ignores later sections
  - Context window fills up fast
  - Slow command execution
### **Detection Pattern**


## Command Conflict With Builtin

### **Id**
command-conflict-with-builtin
### **Summary**
Custom command shadows built-in command
### **Severity**
low
### **Situation**
Built-in feature stops working after adding command
### **Why**
  Some slash names are reserved.
  Custom commands can shadow built-ins.
  No warning when conflict occurs.
  
### **Solution**
  // Reserved command names to avoid
  
  // BUILT-IN COMMANDS (don't override):
  /help          # Shows help
  /clear         # Clears conversation
  /config        # Configuration
  /memory        # Memory management
  /compact       # Compact conversation
  /model         # Model selection
  /bug           # Bug reporting
  /hooks         # Hook management
  /mcp           # MCP server management
  /permissions   # Permission management
  /init          # Initialize Claude Code
  
  // SAFE TO USE:
  /feature       # Custom
  /review        # Custom
  /deploy        # Custom
  /db            # Custom
  /test          # Custom (different from test command)
  /debug         # Custom
  /issue         # Custom
  
  // NAMING CONVENTIONS:
  // Use descriptive names: /code-review not /cr
  // Use kebab-case: /security-scan not /securityScan
  // Prefix team commands: /team-deploy, /team-release
  
  // If you accidentally override:
  // Rename your command file
  // .claude/commands/my-help.md instead of help.md
  
### **Symptoms**
  - Built-in feature doesn't work
  - Wrong command executes
  - Help shows wrong content
### **Detection Pattern**
help\\.md|clear\\.md|config\\.md|memory\\.md