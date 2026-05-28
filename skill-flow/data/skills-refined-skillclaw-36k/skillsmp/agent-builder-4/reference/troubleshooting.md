# Agent Troubleshooting Guide

Common issues and solutions when working with Claude Code sub-agents.

## Issue: Agent Never Triggers

### Symptoms
- Agent doesn't activate when expected
- Claude doesn't recognize when to use agent
- Manual invocation works, automatic doesn't

### Diagnosis

1. **Check description specificity**:
   ```bash
   # Read your agent file
   head -20 .claude/agents/my-agent.md
   ```

   Look for:
   - Is description too generic?
   - Missing trigger keywords?
   - No action-oriented language?

2. **Test with explicit invocation**:
   ```
   "Use the my-agent agent to [task]"
   ```

   If this works, problem is in description/triggers.

### Solutions

**Solution 1: Add Specific Triggers**

❌ **Before**:
```yaml
description: Helps with code tasks
```

✅ **After**:
```yaml
description: Use PROACTIVELY after writing Rails controllers to review for RESTful patterns, security issues, and performance problems
```

**Solution 2: Use Trigger Keywords**

Add words like:
- `PROACTIVELY`
- `MUST BE USED`
- Specific technologies: "Rails", "SQL", "Docker"
- Specific actions: "review", "analyze", "debug"
- Specific contexts: "after writing", "when encountering", "before deploying"

**Solution 3: Add Conditional Language**

```yaml
description: Use when SQL queries are slow or EXPLAIN shows missing indexes. Do not use for application code optimization.
```

### Verification

Test automatic triggering:
```
# Don't name the agent, describe the task
"I just wrote a new Rails controller action. Can you review it?"
```

If agent triggers, issue is resolved.

---

## Issue: Agent Triggers Too Often

### Symptoms
- Agent activates for irrelevant tasks
- Wrong agent chosen for task
- Agent interferes with main conversation

### Diagnosis

Description is too broad or missing constraints.

### Solutions

**Solution 1: Narrow Scope**

❌ **Before**:
```yaml
description: Use for code review
```

✅ **After**:
```yaml
description: Use for Rails code review ONLY. Do not use for JavaScript, Python, or other languages.
```

**Solution 2: Add Exclusions**

```yaml
description: Use when debugging test failures in RSpec. Do not use for Jest, pytest, or other test frameworks.
```

**Solution 3: Make Prerequisites Explicit**

```yaml
description: Use when performance profiling shows database bottlenecks (slow queries, N+1 problems). Requires existing performance data.
```

### Verification

Test with edge cases:
- Tasks that should NOT trigger agent
- Similar but different domains
- Related but out-of-scope work

---

## Issue: Agent Has Wrong Permissions

### Symptoms
- "Tool not available" errors
- Agent can't complete task
- Agent attempts actions but fails

### Diagnosis

1. **Check tool configuration**:
   ```yaml
   tools: Read, Grep, Glob
   ```

2. **Identify what agent tried to do**:
   - Tried to edit files? (needs `Edit`)
   - Tried to run commands? (needs `Bash`)
   - Tried to create files? (needs `Write`)

### Solutions

**Solution 1: Grant Required Tools**

For code review (read-only):
```yaml
tools: Read, Grep, Glob
```

For debugging (read + execute):
```yaml
tools: Read, Bash, Grep, Glob
```

For code fixing (read + modify + execute):
```yaml
tools: Read, Edit, Bash, Grep, Glob
```

For creating new files:
```yaml
tools: Read, Write, Edit, Bash, Grep, Glob
```

**Solution 2: Grant All Tools**

If agent needs flexibility, omit tools field:
```yaml
---
name: my-agent
description: Agent description
# No tools field = inherits all tools
---
```

**Solution 3: Split Agent**

If one agent needs different permissions for different tasks:

Create two agents:
- `code-analyzer` (read-only)
- `code-fixer` (read + edit)

### Verification

Test all expected actions:
- [ ] Agent can read files
- [ ] Agent can search (if needed)
- [ ] Agent can edit (if needed)
- [ ] Agent can run commands (if needed)

---

## Issue: Agent Produces Wrong Output

### Symptoms
- Output format inconsistent
- Missing required information
- Wrong analysis or suggestions
- Output style doesn't match expectations

### Diagnosis

System prompt lacks specificity or examples.

### Solutions

**Solution 1: Define Explicit Output Format**

Add to system prompt:
```markdown
## Output Format

Use this exact structure:

# Analysis Result

## Summary
[One sentence]

## Details
- Point 1
- Point 2

## Recommendation
[Specific action]
```

**Solution 2: Add Examples**

```markdown
## Example Output

**Input**: SQL query with missing index
**Output**:
```
# Query Optimization

## Issue
Query scans full table (1M rows)

## Root Cause
Missing index on `user_id` column

## Recommendation
```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

## Expected Impact
Query time: 2.5s → 50ms (98% faster)
```
```

**Solution 3: Add Constraints**

```markdown
## Constraints

- ALWAYS include specific file paths and line numbers
- NEVER suggest vague improvements like "optimize this"
- DO NOT provide multiple options - pick the best one
- MUST include before/after examples
```

**Solution 4: Improve Instructions**

Break down the process:
```markdown
## Analysis Process

1. Read the error message carefully
2. Identify the exact line that failed
3. Read 10 lines before and after for context
4. Check git blame for recent changes
5. Formulate hypothesis about root cause
6. Propose minimal fix with explanation
```

### Verification

Test with multiple inputs:
- [ ] Output follows format consistently
- [ ] All required sections present
- [ ] Quality meets expectations
- [ ] Style is appropriate

---

## Issue: Agent Not Found

### Symptoms
- "Agent not found" error
- Agent file exists but isn't recognized
- Manual attempts to invoke fail

### Diagnosis

1. **Check file location**:
   ```bash
   # Project agents
   ls -la .claude/agents/

   # User agents
   ls -la ~/.claude/agents/
   ```

2. **Check file naming**:
   - Must end in `.md`
   - Name should match YAML `name` field
   - Lowercase with hyphens

### Solutions

**Solution 1: Correct File Location**

Move to correct directory:
```bash
# For project agent
mv my-agent.md .claude/agents/my-agent.md

# For user agent
mv my-agent.md ~/.claude/agents/my-agent.md
```

**Solution 2: Fix File Name**

Ensure consistency:
```yaml
# In my-agent.md
---
name: my-agent  # Must match filename (without .md)
---
```

**Solution 3: Create Directory**

If directory doesn't exist:
```bash
# Project agents
mkdir -p .claude/agents

# User agents
mkdir -p ~/.claude/agents
```

**Solution 4: Check YAML Syntax**

Validate frontmatter:
```yaml
---
name: agent-name
description: Description here
tools: Read, Edit
model: sonnet
---
```

Common YAML errors:
- Missing opening `---`
- Missing closing `---`
- Incorrect indentation
- Missing quotes around special characters

### Verification

```bash
# List all agents Claude can see
/agents

# Try explicit invocation
"Use the my-agent agent to test"
```

---

## Issue: Agent Runs But Produces No Output

### Symptoms
- Agent starts successfully
- No errors reported
- But no useful output or response

### Diagnosis

Agent completed but didn't communicate results.

### Solutions

**Solution 1: Add Output Instructions**

```markdown
## Final Output

After completing analysis, ALWAYS provide a summary using this format:
[format specification]

Do not end without providing output.
```

**Solution 2: Check for Silent Failures**

Add error handling instructions:
```markdown
## Error Handling

If you encounter errors:
1. Clearly state what failed
2. Explain why it failed
3. Suggest workaround or next steps

Never fail silently.
```

**Solution 3: Require Summary**

```markdown
## Completion Requirement

You must always end with:

# Summary
- [What was done]
- [What was found]
- [What to do next]
```

### Verification

Test edge cases:
- Agent with no findings
- Agent that encounters errors
- Agent with partial results

All should produce output.

---

## Issue: Agent Takes Too Long

### Symptoms
- Agent runs but is very slow
- Times out or seems stuck
- Uses many tokens

### Diagnosis

Agent may be:
- Reading too many files
- Running expensive operations
- Lacking clear stopping criteria

### Solutions

**Solution 1: Add Scope Limits**

```markdown
## Scope

Analyze only:
- Files in `app/` directory
- Maximum 10 files
- Skip `node_modules/`, `vendor/`
```

**Solution 2: Prioritize Efficiently**

```markdown
## Process

1. Check git diff for changed files (start here)
2. Read only files with relevant patterns
3. Stop after finding 5 issues
4. Report findings incrementally
```

**Solution 3: Use Faster Model**

```yaml
model: haiku  # Faster for simple tasks
```

**Solution 4: Break Into Smaller Agents**

Instead of one "complete-analyzer":
- `quick-scanner` (initial pass)
- `deep-analyzer` (detailed review)
- `fix-applier` (apply changes)

### Verification

Measure performance:
- Time to completion
- Token usage
- Files accessed

Optimize as needed.

---

## Issue: Agent Conflicts With Main Conversation

### Symptoms
- Main Claude and agent give conflicting advice
- Confusion about which entity is responding
- Agent overrides main conversation decisions

### Diagnosis

Agent is too broadly scoped or triggers too easily.

### Solutions

**Solution 1: Narrow Agent Scope**

Make agent highly specific:
```yaml
description: Use ONLY for Rails model validations. Do not use for controllers, views, or other components.
```

**Solution 2: Add Deference Rule**

```markdown
## Priority

If main conversation has already addressed this:
- Acknowledge their approach
- Only add value if you have specific domain expertise
- Don't repeat what's already been said
```

**Solution 3: Use Manual Invocation**

Remove automatic trigger words:
```yaml
# Before (automatic)
description: Use PROACTIVELY for code review

# After (manual only)
description: Review code for style and security issues when explicitly invoked
```

### Verification

- [ ] Agent only responds when appropriate
- [ ] No conflicts with main Claude
- [ ] Agent adds value, doesn't duplicate

---

## Issue: YAML Parsing Errors

### Symptoms
- "Invalid YAML" error
- Agent file not loaded
- Frontmatter not recognized

### Common YAML Mistakes

**Mistake 1: Missing Delimiters**

❌ **Wrong**:
```
name: my-agent
description: Agent description

# System Prompt
```

✅ **Correct**:
```yaml
---
name: my-agent
description: Agent description
---

# System Prompt
```

**Mistake 2: Unquoted Special Characters**

❌ **Wrong**:
```yaml
description: Use for code: review & testing
```

✅ **Correct**:
```yaml
description: "Use for code: review & testing"
```

**Mistake 3: Multiline Without Pipe**

❌ **Wrong**:
```yaml
description: This is a very long description
that spans multiple lines
```

✅ **Correct**:
```yaml
description: |
  This is a very long description
  that spans multiple lines
```

Or:
```yaml
description: "This is a very long description that spans multiple lines"
```

**Mistake 4: Incorrect Indentation**

❌ **Wrong**:
```yaml
name: my-agent
 description: Agent description  # Extra space
```

✅ **Correct**:
```yaml
name: my-agent
description: Agent description
```

### Validation

Use YAML validator:
```bash
# Install yq if needed
brew install yq

# Validate YAML
yq eval '.claude/agents/my-agent.md'

# Or use online validator
# https://www.yamllint.com/
```

---

## Issue: Agent Works Locally But Not for Team

### Symptoms
- Agent works for you
- Teammates report agent not found
- Inconsistent behavior across machines

### Diagnosis

Agent in wrong location or not committed.

### Solutions

**Solution 1: Move to Project Location**

```bash
# Move from user agents to project agents
mv ~/.claude/agents/my-agent.md .claude/agents/my-agent.md

# Commit to version control
git add .claude/agents/my-agent.md
git commit -m "Add my-agent for team use"
git push
```

**Solution 2: Document in README**

```markdown
## Available Agents

### my-agent
Use for: [description]
Invoke with: "Use my-agent to [task]"
```

**Solution 3: Share User Agent Template**

If keeping as user agent:
1. Create template in docs/
2. Team members copy to ~/.claude/agents/
3. Customize as needed

### Verification

Have teammate:
1. Pull latest code
2. Check `.claude/agents/` exists
3. Try invoking agent

---

## Debugging Tips

### Enable Verbose Output

Request detailed reasoning:
```
"Use the my-agent agent to [task]. Please explain your reasoning step by step."
```

### Check Agent Configuration

```bash
# View agent file
cat .claude/agents/my-agent.md

# Check YAML is valid
head -10 .claude/agents/my-agent.md
```

### Test Incrementally

1. Test with minimal input
2. Test with complex input
3. Test edge cases
4. Test error conditions

### Compare With Working Agent

If you have a working agent:
1. Compare configuration
2. Compare system prompt structure
3. Identify differences
4. Apply successful patterns

### Simplify and Rebuild

If agent is complex and broken:
1. Start with minimal version
2. Test basic functionality
3. Add features incrementally
4. Test after each addition

---

## Getting Help

### Information to Provide

When asking for help, include:

1. **Agent File**:
   ```bash
   cat .claude/agents/my-agent.md
   ```

2. **What You're Trying**:
   - Exact command or request
   - Expected behavior
   - Actual behavior

3. **Error Messages**:
   - Full error text
   - When it occurs

4. **Environment**:
   - Project type (Rails, Node, etc.)
   - Agent location (project vs user)
   - Claude Code version

### Where to Ask

- Claude Code documentation
- Project team (for project agents)
- Claude Code community forums
- GitHub issues (if applicable)

---

## Prevention Checklist

Avoid issues by following this checklist when creating agents:

- [ ] Name is lowercase-with-hyphens
- [ ] YAML frontmatter is valid
- [ ] Description is specific and action-oriented
- [ ] Tools are appropriate for task
- [ ] System prompt is detailed
- [ ] Output format is defined
- [ ] Examples are included
- [ ] Constraints are explicit
- [ ] File is in correct location
- [ ] Tested with multiple inputs
- [ ] Documented for team (if shared)

---

**See Also**:
- [Configuration Guide](./configuration-guide.md)
- [Best Practices](./best-practices.md)
- [Agent Examples](./agent-examples.md)
