# Slash Command Best Practices

Comprehensive best practices for authoring effective slash commands.

## Command Naming

### Format Rules
- **Lowercase only**: Use `review-pr`, not `Review-PR` or `reviewPR`
- **Hyphens for separation**: Use `analyze-code`, not `analyze_code` or `analyzeCode`
- **Verb-noun pattern**: Preferred format `action-target` (e.g., `check-models`, `review-notebook`)
- **Descriptive**: Name should indicate purpose clearly
- **Concise**: Keep under 32 characters when possible

### Good Examples
- `/optimize` - Simple, clear action
- `/review-pr` - Action + target
- `/strategic-brief` - Descriptive compound noun
- `/model-check` - Validation command
- `/notebook-review` - Analysis command

### Poor Examples
- `/helper` - Too vague
- `/do-stuff` - Unclear purpose
- `/theReviewCommand` - Wrong case format
- `/review_pull_request` - Use hyphens, not underscores

## Prompt Content

### Claude Best Practices

**Note**: For comprehensive prompt engineering guidance including context optimization, guardrails, hallucination prevention, and advanced patterns, consider using the **managing-prompts** skill.

**Be Explicit and Direct**
- State exactly what should be done
- Provide clear context and reasoning
- Use imperative voice: "Analyze X and report Y"
- Avoid vague requests: not "help with", but "implement"

**Structure with XML Tags**
- Use XML tags to organize complex information
- Consistent tag naming throughout
- Nest hierarchically for clarity
- Example: `<analysis></analysis>`, `<recommendations></recommendations>`

**Provide Context**
- Explain why the task matters
- Clarify output format expectations
- Specify audience (e.g., "for board-level presentation")
- Include relevant constraints

**Use Examples**
- Show desired output format
- Demonstrate edge case handling
- Illustrate style preferences
- Ensure examples match intent (Claude pays close attention)

**When to Use managing-prompts Skill**
- Command prompt needs optimization for consistency or quality
- Experiencing hallucinations or incorrect outputs
- Prompt exceeds 500 tokens and needs context optimization
- Need to implement guardrails (citations, quote-grounding)
- Updating prompts to follow current best practices
- Complex reasoning tasks requiring chain-of-thought
- Need to evaluate if logic should stay in prompt vs. extract to script

### Command-Specific Patterns

**Single Focus**: Each command should do one thing well
```markdown
Good: "Review this PR for security vulnerabilities"
Poor: "Review this PR and also refactor and add tests"
```

**Clear Instructions**: No ambiguity about expected actions
```markdown
Good: "Generate comprehensive test coverage report including untested files"
Poor: "Look at testing"
```

**Output Specification**: Define what user should receive
```markdown
Good: "Post findings as PR comment using: gh pr comment $PR_NUMBER --body 'review'"
Poor: "Share your analysis"
```

## YAML Frontmatter

### When to Use Frontmatter

**Use frontmatter when**:
- Command needs description for /help display
- Bash execution requires tool restrictions
- Arguments need documentation
- Specific model is required for complex reasoning
- Command should not be invoked programmatically

**Skip frontmatter when**:
- Simple prompt with no special needs
- No bash execution
- No arguments
- Default model is fine

**Include thinking keywords in prompt content when**:
- Task requires deep reasoning or analysis
- Complex problem-solving needed
- Combining with appropriate model (sonnet/opus)

### Frontmatter Fields

#### description
```yaml
description: Brief explanation shown in /help output
```
- Keep under 120 characters
- Describe what the command does
- Use third-person: "Validates model usage" not "Validate model usage"
- Be specific about purpose

**Good Examples**:
- `description: Comprehensive review of Jupyter notebooks and Python scripts`
- `description: Validate Claude model usage against current public models`
- `description: Generate strategic brief with financial and talent analysis`

**Poor Examples**:
- `description: Helper command` (too vague)
- `description: Does stuff` (meaningless)
- `description: Review things` (unclear what things)

#### allowed-tools

```yaml
allowed-tools: Bash(command:pattern), Bash(command2:pattern2)
```

**Format**: `Bash(command:pattern)` where:
- `command` is the bash command name
- `pattern` restricts arguments (use `*` for any, or specific patterns)

**Examples**:
```yaml
# Allow any git status and specific git commit
allowed-tools: Bash(git status:*), Bash(git commit:*)

# Allow PR operations
allowed-tools: Bash(gh pr comment:*), Bash(gh pr diff:*), Bash(gh pr view:*)

# Allow echo with any arguments
allowed-tools: Bash(echo:*)
```

**Security Principle**: Only allow necessary commands with appropriate restrictions
- Don't use `Bash(*:*)` (unrestricted)
- List each command explicitly
- Use specific patterns when possible
- Review regularly for unnecessary permissions

#### argument-hint

```yaml
argument-hint: [pr-number] [priority] [assignee]
```

- Documents expected arguments for users
- Shown in autocomplete/help
- Use square brackets for required: `[arg]`
- Use angle brackets for optional: `<arg>`
- Be descriptive: `[file-path]` not just `[path]`

**Examples**:
```yaml
argument-hint: [pr-number]
argument-hint: [file-path] <output-format>
argument-hint: [topic] [analysis-depth]
```

#### model

```yaml
model: haiku
```

- Specify model for this command: `haiku`, `sonnet`, `opus`
- Use when specific model capabilities needed
- Default is user's current model if not specified
- Consider cost vs. capability tradeoffs

**When to specify**:
- Simple tasks: `model: haiku` (faster, cheaper)
- Complex analysis: `model: sonnet` or `model: opus`
- Default: omit field to use user's preference

#### disable-model-invocation

```yaml
disable-model-invocation: true
```

- Prevents SlashCommand tool from automatically invoking this command
- Use for commands that should only be manually invoked
- Rare use case; usually omit this field
- Reference **slashcommand-tool-reference.md** for comprehensive SlashCommand tool guidance including permissions and character budget limits

## Argument Handling

### Argument Patterns

**No Arguments**: Simple prompt with no user input needed
```markdown
Analyze the current codebase for performance issues and provide optimization recommendations.
```

**$ARGUMENTS**: Capture all arguments as single string
```markdown
Research the following topic and provide comprehensive analysis: $ARGUMENTS

Usage: /research machine learning best practices
Result: $ARGUMENTS = "machine learning best practices"
```

**Positional ($1, $2, etc.)**: Specific argument positions
```markdown
---
argument-hint: [pr-number] [priority]
---

Review PR #$1 with priority level $2 and provide detailed analysis.

Usage: /review-pr 123 high
Result: $1 = "123", $2 = "high"
```

### Argument Best Practices

**Document Arguments**: Always use argument-hint in frontmatter
```yaml
argument-hint: [file-path] [analysis-type]
```

**Validate in Prompt**: Include guidance for missing arguments
```markdown
Review file at path: $1

If no file path provided, list available files and ask user to specify.
```

**Provide Examples**: Show usage in comments
```markdown
<!-- Usage: /analyze-file src/main.py security -->
<!-- This analyzes src/main.py for security issues -->

Analyze file $1 for $2 issues...
```

**Handle Edge Cases**: Consider empty or invalid arguments
```markdown
Analyze $1 for issues. If $1 is empty, analyze the current working directory.
```

## Bash Execution

### When to Use Bash

**Appropriate uses**:
- GitHub CLI operations (`gh pr comment`, `gh pr diff`)
- Git commands for context (`git status`, `git diff`)
- File system queries (`ls`, `find` for specific needs)
- Output redirection for results

**Inappropriate uses**:
- File reading (use @ prefix or Read tool instead)
- Complex multi-step operations (use skill instead)
- Unrestricted command execution
- Operations better done by Claude directly

### Bash Prefix Pattern

Use `!` prefix for bash commands:
```markdown
!gh pr view $1
!git diff HEAD~1..HEAD
!echo "Analysis complete"
```

### Tool Restrictions

Always specify allowed-tools for bash:
```yaml
---
allowed-tools: Bash(gh pr view:*), Bash(git diff:*)
---
```

**Never** allow unrestricted bash:
```yaml
# WRONG - Too permissive
allowed-tools: Bash(*:*)
```

**Security checklist**:
- [ ] Only necessary commands allowed
- [ ] Patterns restrict argument usage appropriately
- [ ] No dangerous commands (rm, dd, etc.)
- [ ] Review what command can actually do with given pattern

## File References

### @ Prefix Pattern

Use `@` to reference file contents:
```markdown
Review the code in @src/main.py and suggest improvements.

Compare @package.json with @package-lock.json for version mismatches.
```

### Best Practices for File References

**Be Specific**: Use explicit paths
```markdown
Good: @src/components/Header.tsx
Poor: @*.tsx (too broad)
```

**Multiple Files**: Reference several if needed
```markdown
Analyze @src/api/client.ts and @src/api/server.ts for consistency.
```

**Conditional References**: Guide user if file doesn't exist
```markdown
Review @README.md for documentation quality. If README.md doesn't exist, recommend creating one.
```

## Organization and Namespacing

### Directory Structure

**Flat structure** for simple projects:
```
.claude/commands/
├── review-pr.md
├── optimize.md
└── test-coverage.md
```

**Namespaced structure** for complex projects:
```
.claude/commands/
├── frontend/
│   ├── component-review.md
│   └── style-check.md
├── backend/
│   ├── api-review.md
│   └── db-migration.md
└── docs/
    └── doc-review.md
```

### Namespace Benefits

- **Organization**: Related commands grouped together
- **Clarity**: Context visible in help output
- **Discoverability**: Users can explore by category
- **No Conflicts**: Same base name in different namespaces

### Invocation with Namespaces

Commands in subdirectories show namespace:
```
/component-review (project:frontend)
/api-review (project:backend)
```

Invoke normally:
```
/component-review
/api-review
```

## Testing and Validation

### Pre-Deployment Testing

**Basic Functionality**:
- [ ] Command invokes without errors
- [ ] Output matches expectations
- [ ] Arguments substitute correctly
- [ ] Bash commands execute as expected
- [ ] File references work

**Edge Cases**:
- [ ] Missing arguments handled gracefully
- [ ] Invalid arguments produce helpful errors
- [ ] Missing files handled appropriately
- [ ] Unexpected input managed well

**Integration**:
- [ ] Works with git workflow
- [ ] Integrates with GitHub CLI if applicable
- [ ] Plays well with other commands
- [ ] No conflicts with existing commands

### Validation Checklist

Run through before finalizing:
- [ ] File named correctly (.md extension, lowercase-with-hyphens)
- [ ] Location correct (.claude/commands/ or ~/.claude/commands/)
- [ ] YAML frontmatter valid if present
- [ ] Prompt content clear and direct
- [ ] Arguments documented and tested
- [ ] Bash restrictions appropriate
- [ ] File references work
- [ ] Follows Claude best practices
- [ ] If prompt is complex (>300 tokens) or needs optimization: consider managing-prompts skill
- [ ] Tested with real usage scenarios

## Common Mistakes to Avoid

### Mistake 1: Command vs. Skill Confusion

**Problem**: Creating complex multi-step workflow as command
```markdown
<!-- WRONG - This should be a skill -->
Step 1: Analyze codebase
Step 2: Generate report
Step 3: Create tickets
Step 4: Update documentation
Step 5: Notify team
```

**Solution**: Use skill for complex workflows, command for simple prompts

### Mistake 2: Overly Permissive Tools

**Problem**: Unrestricted bash access
```yaml
# WRONG
allowed-tools: Bash(*:*)
```

**Solution**: Specify exact commands needed
```yaml
# CORRECT
allowed-tools: Bash(gh pr comment:*), Bash(git status:*)
```

### Mistake 3: Vague Prompts

**Problem**: Unclear instructions
```markdown
<!-- WRONG -->
Look at the code and make it better
```

**Solution**: Specific, actionable instructions
```markdown
<!-- CORRECT -->
Analyze code in @src/ for:
1. Performance bottlenecks
2. Memory leaks
3. Security vulnerabilities

Provide specific recommendations with code examples.
```

### Mistake 4: Missing Argument Documentation

**Problem**: Arguments used but not documented
```markdown
Review PR #$1 with priority $2
<!-- No argument-hint in frontmatter -->
```

**Solution**: Document in frontmatter
```yaml
---
argument-hint: [pr-number] [priority]
---
```

### Mistake 5: No Context Provided

**Problem**: Bare instructions without context
```markdown
Generate report
```

**Solution**: Include purpose and format
```markdown
Generate comprehensive security audit report for board-level presentation. Include:
- Executive summary with key findings
- Detailed vulnerability analysis
- Remediation recommendations with priority levels
- Compliance status

Format as markdown with clear sections.
```

## Extended Thinking for Complex Reasoning

Commands can trigger extended thinking for complex reasoning tasks by including extended thinking keywords in the prompt. This enables Claude to perform deeper analysis and reasoning.

### When to Use Extended Thinking

**Use extended thinking for**:
- Complex multi-step problem solving
- Detailed code analysis and debugging
- Strategic planning with multiple considerations
- Security analysis and vulnerability assessment
- Mathematical or algorithmic reasoning
- Architecture and design decisions

**Example**:
```markdown
---
description: Perform deep code review with comprehensive analysis
---

Perform a thorough code review of the provided implementation.
Think carefully about:
1. Correctness of logic
2. Edge cases and error handling
3. Performance implications
4. Security vulnerabilities
5. Maintainability and best practices

Provide detailed analysis for each area.
```

### Implementation

Include thinking-related keywords naturally in your prompt content. Claude automatically recognizes these patterns and enables extended thinking.

### Considerations

- **Token Usage**: Extended thinking increases token consumption but improves answer quality for complex tasks
- **Task Fit**: Only use for truly complex reasoning; simple tasks don't benefit
- **Model Dependency**: Ensure model supports thinking (Claude 4.5 and later)
- **Combine with Model Selection**: Use `model: sonnet` or `model: opus` for complex reasoning tasks

For detailed thinking mode guidance, reference the **managing-prompts** skill.

---

## Performance Considerations

### Command Efficiency

**Fast Commands** (Haiku-appropriate):
- Simple prompts with clear instructions
- Basic analysis tasks
- Template generation
- Quick reviews

**Complex Commands** (Sonnet/Opus-appropriate):
- Deep code analysis
- Strategic planning
- Multi-factor decision making
- Complex reasoning tasks

### Model Selection

Specify model in frontmatter based on complexity:
```yaml
# Simple formatting task
model: haiku

# Standard analysis
# (omit to use user's default)

# Complex reasoning
model: sonnet
```

## Advanced Features

### Programmatic Command Invocation

Custom slash commands can be invoked programmatically via the SlashCommand tool, allowing Claude to execute commands automatically in workflows and skills.

**Key considerations**:
- Commands must have a `description` frontmatter field to be available for programmatic invocation
- Disable programmatic invocation with `disable-model-invocation: true` if needed
- Use clear, descriptive names to help Claude recognize when to invoke

For detailed SlashCommand tool guidance including permissions, character budget, and ecosystem integration (plugin commands, MCP commands), reference **slashcommand-tool-reference.md**.

### Plugin Distribution

Commands can be distributed as part of plugins through Claude Code's plugin marketplace. Plugin commands support all standard features with plugin-scoped namespacing.

For creating commands within plugins, reference the **managing-plugins** skill.

### MCP Server Integration

MCP servers can expose prompts as slash commands for integration with Claude Code. This enables dynamic command discovery from connected servers.

For working with MCP-exposed commands, reference the **managing-mcps** skill.

---

## Maintenance

### Regular Reviews

Periodically review commands for:
- **Outdated references**: Tools, URLs, model names
- **Deprecated patterns**: Old prompting approaches
- **Unused commands**: Remove if not valuable
- **Security**: Ensure tool restrictions still appropriate

### Version History

For significant changes, consider adding comments:
```markdown
---
description: Review PR for quality and security
---

<!-- Updated 2025-01: Added security focus, updated gh CLI patterns -->

Review PR #$1 for...
```

### Documentation

Keep team informed:
- Document new commands in README
- Share best examples
- Update onboarding materials
- Maintain command catalog

## Examples Section

See examples.md for annotated real-world examples demonstrating these best practices in action.
