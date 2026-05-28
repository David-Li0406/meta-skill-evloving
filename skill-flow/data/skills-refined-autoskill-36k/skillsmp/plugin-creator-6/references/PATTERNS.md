# Common Plugin Patterns

Established patterns for combining plugin components effectively.

## Pattern 1: Command + Agent

Use a command to trigger an agent for complex tasks.

### Structure

```
plugin/
├── commands/
│   └── analyze.md
└── agents/
    └── analyzer.md
```

### Implementation

```markdown
<!-- commands/analyze.md -->
---
description: Perform deep codebase analysis
---

Launch the analyzer agent to perform comprehensive analysis.

Use the Task tool:
- subagent_type: "analyzer"
- description: "Analyze codebase structure and dependencies"
```

```markdown
<!-- agents/analyzer.md -->
---
description: Deep codebase analysis. Launch when user asks to analyze, understand, or explore the codebase structure
color: purple
tools:
  - Read
  - Glob
  - Grep
examples:
  - trigger: "Analyze this codebase"
    action: "Launch comprehensive codebase analysis"
---

You are a codebase analyst.

## Your Process

1. Scan directory structure
2. Identify entry points
3. Map dependencies
4. Generate architecture report
```

### When to Use

- Complex multi-step tasks
- Tasks requiring autonomous exploration
- Analysis that benefits from specialized agent

### Benefits

- Separates user interface (command) from execution (agent)
- Allows complex workflows
- Agent can be triggered manually or automatically

---

## Pattern 2: Skill + Command

Provide specialized knowledge via skill, invoke with command.

### Structure

```
plugin/
├── commands/
│   └── review.md
└── skills/
    └── review-guidelines.md
```

### Implementation

```markdown
<!-- commands/review.md -->
---
description: Review code using best practices
---

Use the Skill tool to invoke "review-guidelines".

Then apply the guidelines to review the code:
1. Load the skill
2. Check code against guidelines
3. Provide actionable feedback
```

```markdown
<!-- skills/review-guidelines.md -->
---
description: Code review best practices and checklist. Use when reviewing code changes, pull requests, or conducting code audits
---

# Code Review Guidelines

## Security

- Check for SQL injection
- Verify input validation
- Review authentication logic

## Performance

- Identify N+1 queries
- Check for unnecessary loops
- Review caching strategy

## Readability

- Verify naming conventions
- Check for complex logic
- Review comments
```

### When to Use

- Knowledge-based tasks
- Standardized workflows
- Best practice enforcement

### Benefits

- Reusable knowledge
- Consistent application of standards
- Skill can be used independently

---

## Pattern 3: Hook + Validation

Use hooks to enforce standards automatically.

### Structure

```
plugin/
├── hooks/
│   └── pre-tool-use/
│       └── git-safety.md
```

### Implementation

```markdown
<!-- hooks/pre-tool-use/git-safety.md -->
---
description: Prevent dangerous git operations
---

# Git Safety Hook

When Bash tool is used with git commands:

## Behavior

Check if command contains dangerous patterns:
- `git push --force`
- `git clean -fd`
- `git reset --hard`

## Action

If dangerous pattern detected:
1. Block the operation
2. Warn user about risk
3. Suggest safer alternative

## Example Warning

"Blocking dangerous operation: git push --force to main.
Consider: git push --force-with-lease"
```

### When to Use

- Safety-critical operations
- Standard enforcement
- Automatic validation

### Benefits

- Automatic protection
- Non-intrusive
- Always active

---

## Pattern 4: Multi-Component Plugin

Combine all components for comprehensive functionality.

### Structure

```
code-reviewer/
├── .plugin.json
├── README.md
├── commands/
│   ├── review.md
│   └── analyze.md
├── agents/
│   └── reviewer.md
├── skills/
│   └── review-standards.md
└── hooks/
    └── post-tool-use/
        └── log-review.md
```

### Implementation

**Command**: Entry point for users
**Agent**: Performs complex review
**Skill**: Provides review standards
**Hook**: Logs review actions

```json
{
  "name": "code-reviewer",
  "version": "1.0.0",
  "description": "Automated code review plugin",
  "commands": ["review", "analyze"],
  "agents": ["reviewer"],
  "skills": ["review-standards"],
  "hooks": {
    "PostToolUse": ["log-review"]
  }
}
```

### When to Use

- Complex feature sets
- Multiple user workflows
- Comprehensive tooling

### Benefits

- All functionality in one plugin
- Components work together
- Consistent user experience

---

## Pattern 5: Configuration + Component

Use local configuration to customize component behavior.

### Structure

```
plugin/
├── commands/
│   └── format.md
└── .local.md (user-created)
```

### Implementation

```markdown
<!-- commands/format.md -->
---
description: Format code using configured formatter
---

Read configuration from:
${CLAUDE_PLUGIN_ROOT}/../formatter.local.md

Apply formatting based on user preferences:
- formatter: prettier/black
- options: from config
```

```markdown
<!-- ~/.claude/formatter.local.md -->
---
formatter: prettier
options:
  semi: true
  singleQuote: true
trailingComma: es5
```

### When to Use

- User-specific settings
- Customizable behavior
- Environment-specific config

### Benefits

- Flexible configuration
- No hardcoded values
- User control

---

## Pattern 6: Progressive Disclosure

Organize knowledge across multiple files for efficiency.

### Structure

```
plugin/
├── skills/
│   ├── main.md (SKILL.md)
│   └── references/
│       ├── basics.md
│       ├── advanced.md
│       └── examples.md
```

### Implementation

```markdown
<!-- skills/main.md -->
---
description: React development guide. Use when working with React components, hooks, or patterns
---

# React Guide

## Quick Start

```jsx
function App() {
  return <div>Hello</div>;
}
```

## Advanced Features

- **Advanced patterns**: See [ADVANCED.md](references/ADVANCED.md)
- **Performance**: See [PERFORMANCE.md](references/PERFORMANCE.md)
- **Examples**: See [EXAMPLES.md](references/EXAMPLES.md)
```

### When to Use

- Large knowledge bases
- Multiple expertise levels
- Specialized topics

### Benefits

- Lean main file
- Efficient token usage
- Load only what's needed

---

## Pattern 7: MCP Integration

Integrate external services via MCP.

### Structure

```
plugin/
├── .plugin.json
├── .mcp.json
├── commands/
│   └── query-api.md
```

### Implementation

```json
<!-- .mcp.json -->
{
  "mcpServers": {
    "github-api": {
      "type": "http",
      "url": "https://api.github.com",
      "description": "GitHub API for repository operations"
    }
  }
}
```

```markdown
<!-- commands/query-api.md -->
---
description: Query GitHub API for repository information
---

Use the GitHub MCP server to:
1. Fetch repository details
2. List issues
3. Get pull request status
```

### When to Use

- External API integration
- Real-time data
- Service connections

### Benefits

- Clean integration
- Standardized protocol
- Reusable servers

---

## Pattern 8: Conditional Hooks

Use hooks with conditional logic.

### Implementation

```markdown
<!-- hooks/pre-tool-use/conditional-validator.md -->
---
description: Validate operations conditionally based on context
---

# Conditional Validator

Check conditions before executing tools:

## Behavior

If tool is Bash AND command contains "rm":
  Check if path contains "important-data/"
  If yes: Block and warn user
  If no: Allow operation

If tool is Write AND file is ".env":
  Check if adding API_KEY
  If yes: Warn about security
```

### When to Use

- Context-aware validation
- Selective blocking
- Smart warnings

### Benefits

- Intelligent protection
- Context-aware
- Flexible rules

---

## Pattern 9: Session State Management

Use hooks to manage session state.

### Structure

```
plugin/
└── hooks/
    ├── session-start/
    │   └── init.md
    └── session-end/
        └── save.md
```

### Implementation

```markdown
<!-- hooks/session-start/init.md -->
---
description: Initialize session state
---

On session start:
1. Load previous session state
2. Initialize tracking variables
3. Display welcome message
```

```markdown
<!-- hooks/session-end/save.md -->
---
description: Save session state
---

On session end:
1. Collect session statistics
2. Save state to file
3. Generate session summary
```

### When to Use

- Persistent context
- Session tracking
- Usage analytics

### Benefits

- Continuity between sessions
- User experience improvement
- Data collection

---

## Pattern 10: Tool Wrapper

Create commands that wrap complex tool sequences.

### Implementation

```markdown
<!-- commands/deploy.md -->
---
description: Deploy application with full workflow
---

Execute complete deployment workflow:

1. **Build**: Run build commands
   ```bash
   npm run build
   ```

2. **Test**: Run test suite
   ```bash
   npm test
   ```

3. **Deploy**: Deploy to production
   ```bash
   npm run deploy
   ```

4. **Verify**: Check deployment
   ```bash
   curl https://app.example.com
   ```
```

### When to Use

- Common workflows
- Multi-step processes
- Repetitive tasks

### Benefits

- Single command for complex tasks
- Consistent execution
- Error handling included

---

## Choosing the Right Pattern

### Simple Tasks
- Use **Command** alone

### Knowledge-Based Tasks
- Use **Skill** alone or **Skill + Command**

### Complex Autonomous Tasks
- Use **Agent** alone or **Command + Agent**

### Automatic Enforcement
- Use **Hook** alone

### Comprehensive Features
- Use **Multi-Component Plugin**

### Customization Needed
- Use **Configuration + Component**

### Large Knowledge Base
- Use **Progressive Disclosure**

### External Integration
- Use **MCP Integration**
