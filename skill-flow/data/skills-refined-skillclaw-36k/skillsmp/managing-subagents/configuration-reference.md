# Configuration Reference: Complete Field Guide

All available configuration fields for subagent YAML frontmatter.

## Required Fields

### name
**Type**: String
**Format**: lowercase-with-hyphens, under 64 characters
**Example**: `security-auditor`, `api-explorer`, `data-analyzer`
**Validation**: Must be unique within agent scope (project-level or user-level)
**Purpose**: Identifier for subagent, used in invocations

```yaml
name: my-custom-agent
```

### description
**Type**: String
**Length**: Under 1024 characters
**Requirements**:
- Include 5+ specific trigger keywords
- Specify data types/formats (JSON, Python, SQL, config files, etc.)
- Include action verbs (analyzes, audits, searches, validates, etc.)
- List concrete use cases
- Indicate when agent should activate

**Example**:
```yaml
description: Audits Python code for security vulnerabilities including SQL injection, command injection, and hardcoded credentials. Searches for authentication flaws, cryptography issues, and OWASP Top 10 patterns. Use when reviewing code security, performing audits, or when user mentions "security", "vulnerabilities", or "exploit".
```

**Poor example** (avoid):
```yaml
description: Helps with security tasks
```

---

## Optional Fields

### tools
**Type**: Comma-separated list
**Default**: Inherits ALL tools (core + MCP)
**Purpose**: Restrict tool access for security or focus

**Core Tools**:
- Read, Write, Edit, Glob, Grep, Bash
- Task, NotebookEdit
- WebFetch, WebSearch

**MCP Tools** (if configured):
- Inherited automatically when tools field **omitted**
- Must be explicitly listed to use when tools field **specified**
- Format: `mcp__servername:tool_name`

**Example - Read-only analysis**:
```yaml
tools: Read, Glob, Grep
```

**Example - Read + write operations**:
```yaml
tools: Read, Write, Edit, Glob, Grep, Bash
```

**Example - Including MCP tools**:
```yaml
tools: Read, Glob, Grep, mcp__database:query, mcp__api:fetch
```

**Important**: If tools field specified, MCP tools NOT inherited unless explicitly listed. Best practice: omit tools field if agent might need MCP tool flexibility.

### model
**Type**: Model alias or inherit
**Options**: `haiku`, `sonnet`, `opus`, `inherit`
**Default**: System configured subagent model (typically Sonnet)
**Purpose**: Override default model for this agent

**When to use each**:
- `haiku`: Simple searches, fast pattern matching, cost optimization
- `sonnet`: Moderate complexity, code analysis, most general-purpose tasks
- `opus`: Complex reasoning, sophisticated generation (rare)
- `inherit`: Use main conversation's model for consistency

**Example**:
```yaml
model: haiku
```

**Rationale guidance**:
- Keep default (omit) for standard analysis tasks
- Use inherit if agent purpose matches main conversation
- Downgrade to haiku for simple search operations
- Upgrade to sonnet for nuanced judgment or code generation

### permissionMode
**Type**: Permission control value
**Options**: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore`
**Default**: `default`
**Purpose**: Controls how agent handles permission requests

**Mode Descriptions**:

**default**
- Agent asks for permission on sensitive operations
- User approves/denies each protected operation
- Safest option for untrusted workflows
```yaml
permissionMode: default
```

**acceptEdits**
- Agent auto-accepts file edit requests
- Useful for refactoring agents that modify code
- Still asks for permission on other operations
```yaml
permissionMode: acceptEdits
```

**bypassPermissions**
- Agent bypasses all permission checks
- Only use for fully trusted workflows
- High risk - use sparingly
```yaml
permissionMode: bypassPermissions
```

**plan**
- Automatically switches to plan mode
- Agent operates in planning context
- Returns plan without execution
```yaml
permissionMode: plan
```

**ignore**
- Agent ignores permission requests
- Equivalent to bypassPermissions but for specific operations
```yaml
permissionMode: ignore
```

**Selection criteria**:
- Start with `default` (safest)
- Use `acceptEdits` for trusted code refactoring agents
- Use `bypassPermissions` only for fully trusted, repeated workflows
- Use `plan` for planning-specific agents

### skills
**Type**: Comma-separated list of skill names
**Default**: None (no auto-loading)
**Purpose**: Pre-load domain-specific skills when agent starts

**Usage**: When agent benefits from having specific skills available in its context

**Example - Data analysis agent with data processing skill**:
```yaml
skills: data-processor, statistical-analysis
```

**Example - Security audit agent with vulnerability patterns skill**:
```yaml
skills: security-patterns, owasp-top-10
```

**Advantages**:
- Skills automatically loaded, available from agent startup
- Reduces token usage (skills already in context)
- Specializes agent without duplicating content
- Team can share standardized skill sets

**When to use**:
- Agent's domain has companion skill
- Agent repeatedly uses specific patterns/knowledge
- Team needs consistent skill loading
- Reducing token overhead for frequently used agents

**How it works**:
1. Agent starts with skill context pre-loaded
2. Agent has access to skill's tools and knowledge
3. No additional prompt needed to access skill
4. Improves agent focus and efficiency

---

## Complete Configuration Example

### Minimal Agent (Required fields only)
```yaml
---
name: file-finder
description: Searches codebase for files matching patterns, glob expressions, and naming conventions. Use when finding specific file types, locating configuration files, or when user mentions "find files" or "locate".
---

Search the provided codebase for files matching patterns.

## Workflow
1. Use Glob to find matching files
2. Report: file paths, counts, organization
3. Filter by criteria if specified

## Output
- List matching file paths
- Total count
- Organization by type or directory
```

### Full Configuration (All optional fields)
```yaml
---
name: python-security-auditor
description: Audits Python code for OWASP Top 10 vulnerabilities including SQL injection, command injection, insecure deserialization, authentication flaws, and hardcoded credentials. Analyzes databases queries, input handling, and cryptography usage. Use when reviewing Python code security, performing security audits, or when user mentions "security audit" or "vulnerability scan".
tools: Read, Glob, Grep, Bash
model: sonnet
permissionMode: default
skills: owasp-patterns, secure-coding
---

## Purpose
Audit Python code for security vulnerabilities across OWASP Top 10 categories.

## Workflow
1. Use Glob to find Python files: **/*.py
2. Use Grep to search for vulnerability patterns
3. For matches, use Read to examine context
4. Classify by severity: Critical, High, Medium, Low
5. Generate fix recommendations

## Output Format
## Summary
Files scanned: [X] | Issues: [Y]

### Critical
[file:line | vulnerability type | recommendation]

[Continue for High, Medium, Low]
```

---

## Field Priority

**Must Have** (every agent):
- name
- description

**Strongly Recommended** (for most agents):
- tools (if restrictions beneficial for focus/security)

**Use When Applicable**:
- model (if non-default needed)
- permissionMode (for special operation handling)
- skills (if companion skills exist)

## Migration Guide

If updating agent configurations:

**From old format without permissionMode/skills:**
```yaml
---
name: my-agent
description: Old description
tools: Read, Grep
model: sonnet
---
```

**To complete format:**
```yaml
---
name: my-agent
description: Enhanced description with more keywords and use cases
tools: Read, Glob, Grep
model: sonnet
permissionMode: default
skills: domain-specific-skill
---
```

