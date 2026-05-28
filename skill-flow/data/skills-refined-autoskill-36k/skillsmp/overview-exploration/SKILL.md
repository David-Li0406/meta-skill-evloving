---
name: overview-exploration
description: "This skill should be used when performing quick project overview exploration at the start of ultrawork sessions. Executes directly without agent spawn for fast codebase understanding."
---

# Overview Exploration Skill

Quick project overview exploration executed directly without agent spawn.

## When to Use

- At the start of ultrawork sessions (exploration phase)
- When project structure understanding is needed
- Context collection before targeted exploration

---

## Execution Steps

### Step 1: Detect Project Type

Check for language/framework config files:

```python
Glob(pattern="package.json")      # Node.js/JS
Glob(pattern="go.mod")            # Go
Glob(pattern="requirements.txt")  # Python
Glob(pattern="Cargo.toml")        # Rust
Glob(pattern="pom.xml")           # Java/Maven
```

Read discovered files to understand dependencies and framework.

### Step 2: Explore Directory Structure

```python
# Top-level structure
Glob(pattern="*", path=".")

# Main source directories
Glob(pattern="src/*")
Glob(pattern="app/*")
Glob(pattern="lib/*")
```

### Step 3: Identify Entry Points and Patterns

```python
# Find entry points (language-specific)
Grep(pattern="export default|module.exports", type="ts")
Grep(pattern="def main|if __name__", type="py")
Grep(pattern="func main", type="go")

# Check for existing patterns
Grep(pattern="auth|login|session", output_mode="files_with_matches")
```

### Step 4: Read Documentation

```python
Read(file_path="README.md")
Read(file_path="CLAUDE.md")
```

---

## Output Format

Summarize findings in structured format:

```markdown
## Overview Exploration Results

**Project Type**: {framework/language}

**Tech Stack**:
- Language: {language and version}
- Framework: {framework}
- Database: {if found}
- Test: {test framework}

**Directory Structure**:
{tree representation}

**Key Entry Points**:
- {main files}

**Existing Patterns**:
- {auth, database, api patterns found}

**Relevant Files** (based on Goal):
- {files relevant to the user's goal}
```

See `references/templates.md` for complete template.

---

## Session Integration

When running within an ultrawork session:

1. **Update exploration stage** to `overview`
2. **Write** findings to `$SESSION_DIR/exploration/overview.md`
3. **Add** summary to `context.json`
4. **Advance** stage to `analyzing`

**Note**: `SESSION_DIR` is the session metadata directory (e.g., `~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}`), not the project working directory. All exploration artifacts are stored in the session directory to maintain session isolation.

```bash
# For ultrawork, use scripts written in Javascript/Bun
SCRIPTS="${CLAUDE_PLUGIN_ROOT}/src/scripts"

# Update stage
bun $SCRIPTS/session-update.js --session ${CLAUDE_SESSION_ID} --exploration-stage overview

# Get session directory and write findings
SESSION_DIR=~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}
mkdir -p "$SESSION_DIR/exploration"
# Write findings to $SESSION_DIR/exploration/overview.md using Write tool

# Add to context (file path is relative to SESSION_DIR)
bun $SCRIPTS/context-add.js --session ${CLAUDE_SESSION_ID} \
  --explorer-id "overview" \
  --file "exploration/overview.md" \
  --summary "{summary}" \
  --key-files "{files}" \
  --patterns "{patterns}"

# Advance stage
bun $SCRIPTS/session-update.js --session ${CLAUDE_SESSION_ID} --exploration-stage analyzing
```

---

## Time Budget

- **Target**: Complete within 30 seconds
- **Max Read**: 5-7 files
- **Max Glob**: 10 patterns

No excessive exploration - overview aims for quick understanding. Targeted exploration handles detailed investigation.

---

## Next Steps

After overview completion:

1. Analyze Goal + Overview → Generate targeted exploration hints
2. Detailed exploration via `Task(subagent_type="ultrawork:explorer")`
3. All exploration complete → Proceed to Planning phase

---

## Additional Resources

### Reference Files

- **`references/examples.md`** - Complete exploration examples for different project types
- **`references/templates.md`** - Output templates and session integration commands
