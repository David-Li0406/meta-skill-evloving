# Memory Integration Template for Commands

This template shows developers how to integrate session memory into new commands or modify existing command workflows.

## Quick Reference

Every command follows this pattern:

```
1. LOAD memory at START
2. Apply learned context during transformation
3. UPDATE memory at END
```

---

## Command START - Load Memory

**Goal**: Get user preferences and learned patterns before processing

### Single-Step Commands (transform-query, compress-context, etc.)

```python
# Step 1: Create memory directory
Bash(command="mkdir -p .claude/pseudo-code-prompting")

# Step 2: Load relevant memory files
# Choose based on what your command needs:

# For transform commands
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")  # User preferences
Read(file_path=".claude/pseudo-code-prompting/patterns.md")        # Learned patterns

# For validation commands
Read(file_path=".claude/pseudo-code-prompting/patterns.md")        # Validation patterns
Read(file_path=".claude/pseudo-code-prompting/progress.md")        # Validation history

# For optimization commands
Read(file_path=".claude/pseudo-code-prompting/patterns.md")        # Known optimizations
Read(file_path=".claude/pseudo-code-prompting/progress.md")        # Successful patterns

# For compression commands
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")  # Compression preferences

# Step 3: Extract needed information from loaded files
# - Look for user preferences in activeContext.md
# - Check for relevant patterns in patterns.md
# - Review history in progress.md
```

### Pipeline Commands (complete-process)

```python
# CRITICAL: Load memory ONCE at pipeline START, not in each step

# Step 1: Create memory directory
Bash(command="mkdir -p .claude/pseudo-code-prompting")

# Step 2: Load ALL 3 files before first step
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")
Read(file_path=".claude/pseudo-code-prompting/patterns.md")
Read(file_path=".claude/pseudo-code-prompting/progress.md")

# Step 3: Pass loaded context to first step
# (agents will update memory during execution)

# Step 4: Do NOT reload between steps
# (ensures consistency across Transform → Validate → Optimize)
```

---

## Command DURING - Use Loaded Context

### Example 1: Apply User Naming Preferences

**From activeContext.md, check User Preferences table:**

```python
# If you found:
# | Preference | Value | Source |
# | Naming Style | snake_case | Session 2026-01-20 |

# Then apply it in your transformation:
# Function names: snake_case
# Parameter names: snake_case
# Class names: PascalCase (Python convention overrides)
```

### Example 2: Apply Learned Patterns

**From patterns.md, check if similar pattern exists:**

```python
# If you found a REST API authentication pattern from previous session:
# "Authentication endpoints should have rate_limit={"max": 5, "window": "1h"}"

# Apply it in current transformation:
create_endpoint(
  path="/api/auth/login",
  rate_limit={"max": 5, "window": "1h"}  # Applied from learned pattern
)
```

### Example 3: Check Validation History

**From progress.md, look for recurring failures:**

```python
# If you see:
# "Security validation: 85% → 95% pass rate"
# "Common issue: Missing audit_log (2 cases)"

# Then validate this pseudo-code proactively:
# ✓ Does it have audit_log? (check before validating)
# ✓ Does it have all security parameters? (learned improvement)
```

---

## Command END - Update Memory

### Pattern 1: Single-Step Update (Most Commands)

**Read → Edit → Done**

```python
# Step 1: Read current memory file
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")

# Step 2: Update with new learning
Edit(file_path=".claude/pseudo-code-prompting/activeContext.md",
     old_string="## Recent Transformations",
     new_string="## Recent Transformations
- [Today's transform]: Input → Output (metrics: pass/compression_ratio)
- [Previous transformation 1]
- [Previous transformation 2]
[Keep last 10 only]")

# Step 3: Update timestamp
Edit(file_path=".claude/pseudo-code-prompting/activeContext.md",
     old_string="## Last Updated",
     new_string="## Last Updated
2026-01-22 14:30:00 - [Command name] completed")
```

### Pattern 2: Append Pattern Learning

**Read → Find section → Edit with append**

```python
# Step 1: Read patterns file
Read(file_path=".claude/pseudo-code-prompting/patterns.md")

# Step 2: Append new pattern to relevant section
Edit(file_path=".claude/pseudo-code-prompting/patterns.md",
     old_string="## REST API Patterns",
     new_string="## REST API Patterns

### [Pattern Name Discovered Today]
- [Pattern details]
- [Where it was applied]
- [Why it's important]

[Existing patterns below...]")
```

### Pattern 3: Update Progress Metrics

**Read → Update metrics → Update timestamp**

```python
# Step 1: Read progress file
Read(file_path=".claude/pseudo-code-prompting/progress.md")

# Step 2: Update transformation history
Edit(file_path=".claude/pseudo-code-prompting/progress.md",
     old_string="## Transformation History",
     new_string="## Transformation History
- [x] [Today's transformation] - [metrics: compression, validation result]
[Keep last 20 only]")

# Step 3: Update timestamp
Edit(file_path=".claude/pseudo-code-prompting/progress.md",
     old_string="## Last Updated",
     new_string="## Last Updated
2026-01-22 14:30:00")
```

---

## Which Memory File to Use?

### activeContext.md
**Load this when you need:**
- Current user preferences (naming style, security focus, verbosity)
- Recent transformations user has done
- What user is working on right now
- User's project context

**Update this when you discover:**
- New user preference (e.g., "user prefers snake_case")
- Pattern in recent transformations
- Decision user made that affects future work

### patterns.md
**Load this when you need:**
- Domain-specific patterns (REST API, authentication, database)
- Stack-specific conventions (Next.js, FastAPI, Go)
- Security patterns user has established
- Validation rules learned before

**Update this when you discover:**
- New architectural pattern
- New security requirement pattern
- Stack-specific convention
- Domain best practice

### progress.md
**Load this when you need:**
- What transformations succeeded before
- What validations passed/failed
- Optimization effectiveness history
- Quality metrics trends

**Update this when you want to record:**
- Transformation results
- Validation learnings
- Optimization success
- Quality improvements

---

## Memory Integration Matrix

Quick reference for which file to load/update for each command:

| Command | Load at START | Update at END | Why |
|---------|---------------|---------------|-----|
| transform-query | activeContext, patterns | activeContext, patterns | Need user naming prefs, apply/learn patterns |
| compress-context | activeContext | activeContext | Learn compression style preference |
| context-aware-transform | patterns, activeContext | patterns, activeContext | Apply architecture patterns, learn new ones |
| optimize-prompt | patterns, progress | patterns, progress | Use successful optimizations, record results |
| validate-requirements | patterns, progress | patterns, progress | Check patterns, record validation learnings |
| complete-process | ALL 3 (once at start) | ALL 3 (once at end) | Pipeline needs all context, finalizes all updates |

---

## Common Mistakes to Avoid

### ❌ WRONG: Load memory in middle of transformation

```python
transform_query()
Read(file_path="...")  # WRONG - loads during processing
apply_pattern()
```

**Why it's wrong**: Slow, inconsistent, defeats the purpose

**✅ FIX**: Load at START, apply during, update at END

```python
Read(file_path="...")  # RIGHT - load first
transform_query()
apply_pattern()
Update(...)
```

---

### ❌ WRONG: Use Write to update existing files

```python
Write(file_path=".claude/pseudo-code-prompting/activeContext.md",
      content=new_content)  # WRONG - asks for permission
```

**Why it's wrong**: Asks user "Do you want to overwrite?" - disrupts automation

**✅ FIX**: Use Edit for updates

```python
Edit(file_path=".claude/pseudo-code-prompting/activeContext.md",
     old_string="...",
     new_string=new_content)  # RIGHT - no permission needed
```

---

### ❌ WRONG: Use Bash compound commands for memory operations

```python
Bash(command="mkdir -p .claude/pseudo-code-prompting && cat file.md")  # WRONG
```

**Why it's wrong**: Compound commands ask for permission

**✅ FIX**: Use separate tool calls

```python
Bash(command="mkdir -p .claude/pseudo-code-prompting")  # RIGHT
Read(file_path=".claude/pseudo-code-prompting/file.md")  # RIGHT
```

---

### ❌ WRONG: Load memory multiple times in pipeline

```python
# In Transform step
Read(file_path="...")
# In Validate step
Read(file_path="...")  # WRONG - reloads, inconsistent
# In Optimize step
Read(file_path="...")  # WRONG - reloads, inconsistent
```

**Why it's wrong**: Different versions of memory loaded at different times, inconsistency

**✅ FIX**: Load once at pipeline START

```python
# Before Transform step
Read(file_path="...")  # RIGHT - load once
# Transform, Validate, Optimize use same memory
# Update once at END
```

---

### ❌ WRONG: Don't update memory after transformation

```python
transform_query()
return result  # WRONG - no update
```

**Why it's wrong**: Learning is lost, next session starts blind again

**✅ FIX**: Always update at END

```python
transform_query()
Edit(file_path="...")  # RIGHT - record learning
return result
```

---

## Testing Your Memory Integration

### Test 1: Memory Loads Successfully

```
❌ FAIL: FileNotFoundError when reading activeContext.md
✅ PASS: File read successfully (or creates empty template on first run)
```

### Test 2: User Preferences Applied

```
Session 1:
/transform-query add user authentication
→ Observe: "snake_case" naming used

Session 2 (later):
/transform-query add product listing
→ Observe: "snake_case" naming applied automatically (loaded from memory)
```

### Test 3: Patterns Accumulate

```
Session 1:
/transform-query implement REST API
→ Pattern recorded: "REST API with rate_limiting"

Session 2:
/transform-query add authentication endpoint
→ Observe: Rate limiting suggestion auto-applies (from learned pattern)
```

### Test 4: Pipeline Memory Consistency

```
/complete-process [complex requirement]
→ Observe: Transform → Validate → Optimize all use same loaded context
→ Memory updated once at end
→ Timestamp reflects pipeline completion, not individual steps
```

### Test 5: Project Context Validation

```
In Project A:
/transform-query implement feature
→ Memory recorded with "Current Project: /path/A"

Switch to Project B:
/transform-query implement feature
→ Hook warns: "PROJECT_CONTEXT_CHANGE_DETECTED"
→ Command resets context on START (auto-reset strategy)
```

---

## Implementation Checklist

When adding memory to a new command:

- [ ] Load memory files at command START (before main logic)
- [ ] Extract relevant information from loaded files
- [ ] Apply learnings during transformation/validation/optimization
- [ ] Update memory files at command END with new insights
- [ ] Use Edit (not Write) for updates to existing files
- [ ] Use separate Bash and Read calls (not compound commands)
- [ ] For pipelines: Load ONCE at start, update ONCE at end
- [ ] Add Project Path check for multi-project support (auto-reset)
- [ ] Update timestamp in memory before completing

---

## Success Criteria

Your memory integration is working when:

✅ User preferences learned in one session apply in next session
✅ Patterns accumulate and improve transformation quality
✅ Validation failures decrease over time (learnings applied)
✅ Optimization suggestions get better (history applied)
✅ Project context switches detected (warning shown)
✅ Memory survives conversation auto-compaction
✅ No permission prompts during memory operations
✅ Memory files stay under 200 lines (trim if needed)
