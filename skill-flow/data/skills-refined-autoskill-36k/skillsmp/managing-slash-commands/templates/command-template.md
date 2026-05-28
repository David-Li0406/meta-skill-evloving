# Slash Command Template

Use this template when creating new slash commands. Delete sections and comments that don't apply.

---

## Template: Minimal Command (No Frontmatter)

Use for simple commands with no special requirements.

```markdown
[Clear, direct instruction for what the command should do]

[Optional: Context or constraints]

[Optional: Output format specification]
```

**Example**:
```markdown
Analyze the current codebase for performance issues and provide specific optimization recommendations with code examples.
```

---

## Template: Standard Command

Use for commands with description and basic metadata.

```markdown
---
description: [Brief description for /help display]
---

[Optional: Usage comment]
<!-- Usage: /command-name -->

[Clear instruction with context]

[Output specification]
```

**Example**:
```markdown
---
description: Analyzes code for TypeScript type safety issues
---

<!-- Usage: /check-types -->

Run TypeScript compiler in check mode and analyze all type errors.

Categorize errors by:
- Missing type annotations
- Type safety violations
- Configuration issues

Provide specific fixes for each category with code examples.
```

---

## Template: Command with Arguments

Use for commands that need user input.

```markdown
---
description: [Brief description]
argument-hint: [required-arg] <optional-arg>
---

<!-- Usage: /command-name [example-arg] -->
<!-- Example: /command-name src/main.ts -->

[Instruction using $1, $2, or $ARGUMENTS]

[Argument validation and edge case handling]

[Output specification]
```

**Example with Positional Arguments**:
```markdown
---
description: Compares two files for differences
argument-hint: [file1] [file2]
---

<!-- Usage: /compare src/v1.ts src/v2.ts -->

Compare @$1 with @$2 for:
- Functional differences
- Style differences
- Best practice adherence

If either file doesn't exist, list available files.

Present findings in table format.
```

**Example with $ARGUMENTS**:
```markdown
---
description: Researches topic and provides comprehensive analysis
argument-hint: [topic-or-question]
---

<!-- Usage: /research machine learning best practices -->

Conduct comprehensive research on: $ARGUMENTS

Include:
- Current state of the art
- Key trends and developments
- Practical recommendations
- Relevant resources

Format for technical audience with citations.
```

---

## Template: Command with Bash Execution

Use for commands that need to run bash commands.

```markdown
---
description: [Brief description]
argument-hint: [required-arg]
allowed-tools: Bash(command1:*), Bash(command2:*)
---

<!-- Usage: /command-name [example-arg] -->

[Optional: Initial bash command for context]
!bash-command $1

[Instruction for main task]

[Optional: Output bash command]
!bash-command $1 --flag "output"
```

**Example**:
```markdown
---
description: Reviews pull request and posts findings as comment
argument-hint: [pr-number]
allowed-tools: Bash(gh pr view:*), Bash(gh pr comment:*)
---

<!-- Usage: /review-pr 123 -->

First, view the PR details:
!gh pr view $1

Review the pull request for:
- Code quality issues
- Security vulnerabilities
- Best practice violations
- Test coverage gaps

For each issue, provide:
- Location (file:line)
- Description
- Recommended fix with code example

Post your review as a comment:
!gh pr comment $1 --body "[your review]"
```

---

## Template: Complex Command with Structure

Use for commands that need structured, detailed output.

```markdown
---
description: [Brief description]
argument-hint: [required-arg]
model: sonnet
---

<!-- Usage: /command-name [example-arg] -->

[Context and purpose]

[Main instruction with clear structure]

**Output Format**:

<section_one>
[What goes in section one]
</section_one>

<section_two>
[What goes in section two]
</section_two>

<section_three>
[What goes in section three]
</section_three>

[Additional formatting guidance]
```

**Example**:
```markdown
---
description: Generates comprehensive API documentation
argument-hint: [api-directory-path]
model: sonnet
---

<!-- Usage: /document-api src/api -->

Generate comprehensive API documentation for all files in @$1.

Analyze all exported functions, classes, and types.

**Output Format**:

<api_overview>
[High-level description of the API purpose and architecture]
</api_overview>

<endpoints>
For each endpoint:
- Path and method
- Parameters with types
- Response format
- Error codes
- Example request/response
</endpoints>

<authentication>
[Authentication requirements and examples]
</authentication>

<examples>
[Complete usage examples with code]
</examples>

<changelog>
[Recent changes if identifiable from git history]
</changelog>

Use clear markdown formatting with code blocks for examples.
Format for developer audience.
```

---

## Template Selection Guide

Choose the right template based on your needs:

**Minimal Command**:
- ✓ Simple, single instruction
- ✓ No arguments needed
- ✓ No special requirements
- ✓ Quick to implement

**Standard Command**:
- ✓ Needs description for /help
- ✓ No arguments or bash
- ✓ Straightforward output
- ✓ Single purpose

**Command with Arguments**:
- ✓ Needs user input
- ✓ Positional args or $ARGUMENTS
- ✓ Flexible operation
- ✓ Input validation needed

**Command with Bash**:
- ✓ GitHub CLI operations
- ✓ Git command context
- ✓ File system operations
- ✓ Output redirection

**Complex Command**:
- ✓ Structured output needed
- ✓ Multiple sections or phases
- ✓ Detailed analysis
- ✓ May need specific model

---

## Frontmatter Fields Reference

```yaml
---
# Brief description shown in /help output
description: [string, under 120 chars]

# Document expected arguments
argument-hint: [required] <optional>

# Specify allowed bash commands (if using !)
allowed-tools: Bash(command:pattern), Bash(command2:pattern)

# Specify model if needed (haiku, sonnet, opus)
model: [model-name]

# Prevent automatic invocation (rare)
disable-model-invocation: [true|false]
---
```

---

## Customization Checklist

When using a template, customize these parts:

- [ ] Replace [description] with actual description
- [ ] Replace [argument-hint] with actual arguments
- [ ] Update <!-- Usage --> comment with real example
- [ ] Replace placeholder instructions with actual task
- [ ] Update allowed-tools with commands you'll actually use
- [ ] Customize output format specification
- [ ] Add validation logic for arguments
- [ ] Add edge case handling
- [ ] Test with real usage

---

## Validation Before Saving

Quick checks before considering complete:

- [ ] File named with `.md` extension
- [ ] Lowercase-with-hyphens naming
- [ ] YAML frontmatter valid (if present)
- [ ] All arguments documented in argument-hint
- [ ] Bash commands listed in allowed-tools (if used)
- [ ] Clear, direct instructions
- [ ] Output format specified
- [ ] Edge cases handled
- [ ] Usage example provided
- [ ] Tested basic invocation

---

## Where to Save

**Project Command** (team-shared):
```
.claude/commands/command-name.md
```

**Personal Command** (individual use):
```
~/.claude/commands/command-name.md
```

**Namespaced Command** (organized by category):
```
.claude/commands/category/command-name.md
```

---

## Next Steps After Creation

1. **Verify**: Use Read tool to verify file created correctly
2. **Test**: Invoke with `/command-name [args]` to test
3. **Validate**: Run through validation checklist
4. **Iterate**: Refine based on testing
5. **Document**: Update team docs if project command
6. **Share**: Notify team if needed

---

## Example: Complete Command from Template

Starting with "Command with Arguments" template:

```markdown
---
description: [Brief description]
argument-hint: [required-arg] <optional-arg>
---

<!-- Usage: /command-name [example-arg] -->

[Instruction using $1, $2, or $ARGUMENTS]
[Argument validation]
[Output specification]
```

Customized to real command:

```markdown
---
description: Analyzes file for security vulnerabilities with configurable depth
argument-hint: [file-path] <analysis-depth>
---

<!-- Usage: /security-scan src/auth.ts deep -->

Analyze @$1 for security vulnerabilities.

Analysis depth: $2 (default: standard if not provided)
- standard: Common vulnerabilities (OWASP Top 10)
- deep: Comprehensive security audit

If @$1 doesn't exist, list available files in src/ directory.

**Focus Areas**:
1. Input validation (SQL injection, XSS, command injection)
2. Authentication and authorization issues
3. Data exposure and insecure cryptography
4. Security misconfiguration

**Output Format**:
For each vulnerability:
- Severity: Critical/High/Medium/Low
- Location: file:line
- Issue description
- Potential impact
- Specific fix with code example

If no vulnerabilities found, provide security posture assessment.
```

---

## Tips for Effective Commands

1. **Be Specific**: Clear instructions yield better results
2. **Provide Context**: Explain why and for whom
3. **Structure Output**: Use XML tags or sections
4. **Validate Inputs**: Handle edge cases gracefully
5. **Show Examples**: Include usage comments
6. **Test Thoroughly**: Try various inputs
7. **Keep Simple**: Complex logic should be skills
8. **Document Well**: Help text and comments
9. **Restrict Security**: Only allow necessary tools
10. **Iterate**: Improve based on usage

---

## When Command Becomes Too Complex

If your command has:
- [ ] More than 3-4 arguments
- [ ] Multiple conditional flows
- [ ] Several distinct steps/phases
- [ ] Needs supporting files
- [ ] Validation loops
- [ ] State management

**Consider converting to a skill instead** using the managing-agent-skills skill.
