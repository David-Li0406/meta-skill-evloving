# Claude Code Commands - Validations

## Command Without Usage Documentation

### **Id**
missing-usage-comment
### **Severity**
medium
### **Type**
regex
### **Pattern**
^\s*#.*\$ARGUMENTS
### **Negative Pattern**
#\s*Usage:|#\s*Example:
### **Message**
Command uses $ARGUMENTS but lacks usage documentation.
### **Fix Action**
Add usage comment: # Usage: /command-name argument-description
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md

## Incorrect Arguments Variable

### **Id**
wrong-arguments-syntax
### **Severity**
high
### **Type**
regex
### **Pattern**
\$[Aa]rgument[^sS]|\$ARGUMENT\s|\$\{ARGUMENTS\}|\$[Aa]rguments
### **Message**
Wrong $ARGUMENTS syntax. Must be exactly $ARGUMENTS (all caps, with S).
### **Fix Action**
Use $ARGUMENTS exactly as written
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md

## Relative Path in File Reference

### **Id**
relative-file-reference
### **Severity**
medium
### **Type**
regex
### **Pattern**
@\\.\\.?/
### **Message**
@file paths should be relative to project root, not the command file.
### **Fix Action**
Use @src/file.md not @../src/file.md
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md

## Override of Built-in Command

### **Id**
builtin-command-override
### **Severity**
high
### **Type**
filename
### **Pattern**
(help|clear|config|memory|compact|model|bug|hooks|mcp|permissions|init)\\.md$
### **Message**
Command file may override built-in Claude Code command.
### **Fix Action**
Rename to avoid conflict with built-in commands
### **Applies To**
  - .claude/commands/
  - **/commands/

## Command Without Output Format

### **Id**
no-output-format
### **Severity**
low
### **Type**
regex
### **Pattern**
##.*Workflow|##.*Process|##.*Steps
### **Negative Pattern**
##.*Output|##.*Format|##.*Response
### **Message**
Command has workflow steps but no specified output format.
### **Fix Action**
Add ## Output Format section specifying expected response structure
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md

## Code Block Without Execution Guidance

### **Id**
executable-code-without-context
### **Severity**
low
### **Type**
regex
### **Pattern**
```bash\n[^`]+```
### **Negative Pattern**
Run this|Execute|Don.*t run|Example
### **Message**
Code block without clear guidance on whether to execute it.
### **Fix Action**
Add 'Run this command:' or 'Example (don't execute):' before code blocks
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md

## Command Exceeds Recommended Length

### **Id**
very-long-command
### **Severity**
low
### **Type**
line_count
### **Threshold**

### **Message**
Command is very long (>150 lines). Consider splitting into smaller commands.
### **Fix Action**
Break into modular commands or use @file references
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md

## Command Without Title Header

### **Id**
missing-title
### **Severity**
medium
### **Type**
regex
### **Pattern**
^[^#]
### **Message**
Command doesn't start with a title header.
### **Fix Action**
Start command with # Title describing the workflow
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md

## Hardcoded Absolute Path in Command

### **Id**
hardcoded-absolute-path
### **Severity**
medium
### **Type**
regex
### **Pattern**
(/Users/|/home/|C:\\\\|/var/)
### **Message**
Hardcoded absolute path won't work on other machines.
### **Fix Action**
Use relative paths or $ARGUMENTS for dynamic paths
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md

## Checklist Items All Unchecked

### **Id**
unclosed-checklist
### **Severity**
low
### **Type**
regex
### **Pattern**
- \\[ \\].*\n- \\[ \\].*\n- \\[ \\]
### **Negative Pattern**
- \\[x\\]
### **Message**
Multiple unchecked items. Claude will try to complete these - ensure that's intended.
### **Fix Action**
Verify checklist items are meant to be completed by Claude
### **Applies To**
  - .claude/commands/*.md
  - **/commands/*.md