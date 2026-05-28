# Troubleshooting Slash Commands

Common issues and solutions when creating custom slash commands.

## Command Not Appearing in Menu

### Symptom
Command doesn't show up when typing `/` or in `/help` output.

### Causes and Solutions

#### Wrong Location

```bash
# Check if file is in correct location
ls -la .claude/commands/     # Project commands
ls -la ~/.claude/commands/   # User commands
```

**Fix:** Move file to `.claude/commands/` (project) or `~/.claude/commands/` (user).

#### Wrong File Extension

```bash
# Wrong
.claude/commands/review.txt
.claude/commands/review

# Correct
.claude/commands/review.md
```

**Fix:** Ensure file has `.md` extension.

#### Invalid Filename

```bash
# Wrong - spaces and uppercase
.claude/commands/Code Review.md
.claude/commands/CodeReview.md

# Correct - lowercase with hyphens
.claude/commands/code-review.md
```

**Fix:** Use lowercase letters, numbers, and hyphens only.

#### Syntax Error in Frontmatter

```yaml
# Wrong - missing closing dashes
---
description: Review code

# Wrong - bad YAML syntax
---
description: "Review code
---

# Correct
---
description: Review code
---
```

**Fix:** Ensure frontmatter has opening and closing `---` with valid YAML.

---

## Arguments Not Being Passed

### Symptom
`$ARGUMENTS` or `$1`, `$2` are empty or literal strings.

### Causes and Solutions

#### Using Wrong Placeholder

```markdown
# Wrong - these won't work
Review ${ARGUMENTS}
Review {$1}
Review %1

# Correct
Review $ARGUMENTS
Review $1
```

**Fix:** Use `$ARGUMENTS` for all args, `$1`, `$2`, etc. for positional.

#### Arguments in Wrong Position

```bash
# Wrong - arguments before command
123 /fix-issue

# Correct - arguments after command
/fix-issue 123
```

**Fix:** Arguments must come after the command name.

#### Quotes Causing Issues

```bash
# These all work the same
/fix-issue 123 high-priority
/fix-issue "123 high-priority"
```

Note: Quotes are stripped; content becomes `$ARGUMENTS`.

---

## Bash Execution Not Working

### Symptom
`!`command`` shows literal text instead of output.

### Causes and Solutions

#### Missing allowed-tools

```markdown
# Wrong - no bash permission
---
description: Show git status
---

Status: !`git status`

# Correct - bash explicitly allowed
---
allowed-tools: Bash(git status:*)
description: Show git status
---

Status: !`git status`
```

**Fix:** Add `allowed-tools` with appropriate Bash patterns.

#### Wrong Bash Pattern

```markdown
# Wrong - pattern doesn't match command
---
allowed-tools: Bash(git:*)
---

!`npm run build`  # Won't work - npm not allowed

# Correct
---
allowed-tools: Bash(git:*), Bash(npm:*)
---
```

**Fix:** Ensure bash pattern matches the commands you're running.

#### Command Fails Silently

```bash
# Check if command works outside Claude Code
git status
npm run build
```

**Fix:** Verify the command works in your terminal first.

---

## Frontmatter Syntax Errors

### Symptom
Command loads but frontmatter settings are ignored.

### Common Mistakes

#### Missing Dashes

```markdown
# Wrong
description: Review code
allowed-tools: Read

# Correct
---
description: Review code
allowed-tools: Read
---
```

#### Incorrect Array Syntax

```yaml
# Wrong - these formats don't work
allowed-tools: [Read, Write]  # brackets don't work
allowed-tools:
  - Read
  - Write  # YAML arrays don't work

# Correct - comma-separated string
allowed-tools: Read, Write, Edit
```

#### Incorrect Model Value

```yaml
# Wrong - invalid model strings
model: opus
model: fast
model: sonnet

# Correct - exact model ID
model: claude-sonnet-4-20250514
model: claude-3-5-haiku-20241022
```

**Check available models:** See [Models overview](https://docs.claude.com/en/docs/about-claude/models/overview)

---

## Command Overriding Issues

### Symptom
Running `/deploy` executes the wrong command.

### Understanding Precedence

1. **Project commands** (`.claude/commands/`) override user commands
2. **Same-name commands** in different subdirectories coexist

```
.claude/commands/deploy.md          # Wins over user
~/.claude/commands/deploy.md        # Silently ignored

.claude/commands/frontend/test.md   # Shows as (project:frontend)
.claude/commands/backend/test.md    # Shows as (project:backend)
# Both coexist - user picks from description
```

### Solutions

#### Check Which Command Is Active

```bash
# Run /help and look for your command
/help

# Look for (project) or (user) suffix
/deploy ... (project)
/deploy ... (user)
```

#### Rename Conflicting Commands

```bash
# Instead of same name
mv ~/.claude/commands/deploy.md ~/.claude/commands/personal-deploy.md
```

---

## SlashCommand Tool Not Using Command

### Symptom
Claude doesn't invoke command via SlashCommand tool when it should.

### Causes and Solutions

#### Missing Description

```markdown
# Wrong - no description
Review this code for issues.

# Correct - has description
---
description: Review code for security and performance
---

Review this code for issues.
```

**Fix:** Add `description` in frontmatter.

#### Command Explicitly Disabled

```yaml
# This prevents SlashCommand tool access
---
disable-model-invocation: true
---
```

**Fix:** Remove `disable-model-invocation` if you want Claude to use it.

#### SlashCommand Tool Denied

```bash
# Check permissions
/permissions

# Look for SlashCommand in deny rules
```

**Fix:** Remove `SlashCommand` from deny rules if present.

#### Character Budget Exceeded

Too many commands can exhaust the context budget.

```bash
# Check context usage
/context

# Look for "M of N commands" warning
```

**Fix:** Reduce command count or set `SLASH_COMMAND_TOOL_CHAR_BUDGET` higher.

---

## File References Not Working

### Symptom
`@path/to/file` shows literal text instead of file contents.

### Causes and Solutions

#### File Doesn't Exist

```markdown
# Check path is correct
@src/utils/helpers.js  # Relative to project root
```

**Fix:** Verify file exists at specified path.

#### Using with Arguments

```markdown
# Wrong - variable in wrong position
Review @$1  # May not work reliably

# Better - use Read tool
---
allowed-tools: Read
---

Read and review: $1
```

---

## Performance Issues

### Symptom
Command takes too long or times out.

### Solutions

#### Reduce Bash Command Output

```markdown
# Wrong - could return huge output
!`git log`
!`find . -type f`

# Correct - limit output
!`git log --oneline -10`
!`find . -type f -name "*.ts" | head -20`
```

#### Use Faster Model for Simple Commands

```yaml
---
model: claude-3-5-haiku-20241022
description: Quick lookup
---
```

---

## Debugging Tips

### Check Command Parsing

```bash
# Run Claude with debug mode
claude --debug
```

Look for:
- Command file loading
- Frontmatter parsing
- Argument substitution

### Verify File Permissions

```bash
# Ensure file is readable
ls -la .claude/commands/
chmod 644 .claude/commands/my-command.md
```

### Test Incrementally

1. Start with minimal command (no frontmatter)
2. Add frontmatter one field at a time
3. Add bash execution last
4. Test after each addition

### Check for Hidden Characters

```bash
# Look for BOM or other hidden chars
file .claude/commands/my-command.md
# Should show: UTF-8 text

# View hex dump of first bytes
xxd .claude/commands/my-command.md | head -1
```

---

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Command not found" | File not in correct location | Move to `.claude/commands/` |
| "Invalid frontmatter" | YAML syntax error | Check dashes and colons |
| "Tool not allowed" | Bash command without permission | Add to `allowed-tools` |
| "File not found" | `@path` references missing file | Verify file path |

---

## Getting Help

1. Check `/help` for command listing
2. Run `/context` to see token usage
3. Use `claude --debug` for detailed logs
4. Verify YAML at [yamllint.com](https://yamllint.com)
