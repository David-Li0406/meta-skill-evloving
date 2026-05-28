---
name: session-memory
description: "Session memory management for pseudo-code prompting - preserves transformation context, learned patterns, and user preferences across sessions"
allowed-tools: Read, Write, Edit, Bash
---

# Session Memory (Pseudo-Code Prompting)

## The Iron Law

```
EVERY WORKFLOW MUST:
1. LOAD memory at START (and before key decisions)
2. UPDATE memory at END (and after learnings/decisions)
```

### READ Side (Equally Important)
**If memory is not loaded:** You work blind, repeat mistakes, lose transformation patterns.
**If decisions made without checking memory:** You contradict prior user preferences, waste effort.

### WRITE Side
**If memory is not updated:** Next session loses learned patterns, user preferences, transformation history.
**If learnings not recorded:** Same optimization mistakes will be repeated.

**BOTH SIDES ARE NON-NEGOTIABLE.**

## Permission-Free Operations (CRITICAL)

**ALL memory operations are PERMISSION-FREE using the correct tools.**

| Operation | Tool | Permission |
|-----------|------|------------|
| Create memory directory | `Bash(command="mkdir -p .claude/pseudo-code-prompting")` | FREE |
| **Read memory files** | `Read(file_path=".claude/pseudo-code-prompting/activeContext.md")` | **FREE** |
| **Create NEW memory file** | `Write(file_path="...", content="...")` | **FREE** (file doesn't exist) |
| **Update EXISTING memory** | `Edit(file_path="...", old_string="...", new_string="...")` | **FREE** |

### CRITICAL: Write vs Edit

| Tool | Use For | Asks Permission? |
|------|---------|------------------|
| **Write** | Creating NEW files | NO (if file doesn't exist) |
| **Write** | Overwriting existing files | **YES - asks "Do you want to overwrite?"** |
| **Edit** | Updating existing files | **NO - always permission-free** |

**RULE: Use Write for NEW files, Edit for UPDATES.**

### CRITICAL: Use Read Tool, NOT Bash(cat)

**NEVER use Bash compound commands** (`mkdir && cat`) - they ASK PERMISSION.
**ALWAYS use Read tool** for reading files - it's PERMISSION-FREE.

```
# WRONG (asks permission - compound Bash command)
mkdir -p .claude/pseudo-code-prompting && cat .claude/pseudo-code-prompting/activeContext.md

# RIGHT (permission-free - separate tools)
Bash(command="mkdir -p .claude/pseudo-code-prompting")
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")
```

**NEVER use heredoc writes** (`cat > file << 'EOF'`) - they ASK PERMISSION.
**Use Write for NEW files, Edit for EXISTING files.**

```
# WRONG (asks permission - heredoc)
cat > .claude/pseudo-code-prompting/activeContext.md << 'EOF'
content here
EOF

# RIGHT for NEW files (permission-free)
Write(file_path=".claude/pseudo-code-prompting/activeContext.md", content="content here")

# RIGHT for EXISTING files (permission-free)
Edit(file_path=".claude/pseudo-code-prompting/activeContext.md",
     old_string="# Active Context",
     new_string="# Active Context\n\n[new content]")
```

## Why This Matters for Pseudo-Code Prompting

> "My memory resets between sessions. The Memory Bank is my ONLY link to previous transformations."

Without memory persistence:
- User preferences lost (naming style, security focus, verbosity level)
- Transformation patterns relearned from scratch
- Domain knowledge forgotten (REST API conventions, auth patterns)
- Quality improvements lost between sessions
- Same validation failures repeated

**Memory is the difference between a learning system and a forgetful system.**

## Memory Structure

```
.claude/
└── pseudo-code-prompting/
    ├── activeContext.md   # Current transformations + user preferences + recent decisions
    ├── patterns.md        # Learned transformation patterns + domain knowledge
    └── progress.md        # Transformation quality metrics + validation history
```

## Memory Schemas

### activeContext.md Schema

```markdown
# Active Context

## Project Path
Current Project: [absolute path to project directory]
Last Updated: [ISO timestamp]
Status: [same_project | auto_reset_from_previous_project]

## Current Transformation
[What requirement is being transformed right now]

## User Preferences
| Preference | Value | Source |
|------------|-------|--------|
| Naming Style | snake_case | Session 2024-01-20 |
| Security Focus | High | User explicit |
| Verbosity | Concise | Inferred from validations |
| Parameter Style | Named args | Consistent pattern |

## Recent Transformations
- [Transformation 1]: Input → Output (compression: 92%, validation: pass)
- [Transformation 2]: Input → Output (compression: 88%, validation: 2 warnings)
- ... (keep last 10)

## Active Patterns
| Domain | Pattern Detected | Confidence |
|--------|-----------------|------------|
| REST API | JWT auth by default | High |
| Database | Parameterized queries | High |
| Validation | Email regex + unique check | Medium |

## Learnings This Session
- User prefers explicit rate limiting on public endpoints
- Security validations should mention OWASP category
- Function names should indicate CRUD operation clearly

## Blockers / Issues
- None / [Active blocker description]

## Last Updated
[timestamp]
```

### patterns.md Schema

```markdown
# Transformation Patterns

## REST API Patterns
### Authentication Endpoints
```javascript
create_endpoint(
  path="/api/auth/[action]",
  method="POST",
  auth="none",
  rate_limit={"max": 10, "window": "1h"},
  security=["input_validation", "rate_limiting", "audit_log"]
)
```

### CRUD Endpoints
[Standard CRUD patterns learned from user's transformations]

## Authentication Patterns
### JWT Implementation
[Learned JWT patterns with security requirements]

### OAuth2 Flow
[Learned OAuth2 patterns]

## Database Patterns
### Query Construction
[Parameterized query patterns]

### Connection Handling
[Connection pool patterns]

## Validation Patterns
### Email Validation
[Email validation with uniqueness check]

### Password Requirements
[Password strength patterns discovered from user requirements]

## Security Patterns
### OWASP Top 10 Coverage
[Security patterns mapped to OWASP categories]

## User-Specific Conventions
### Naming Conventions
- Functions: snake_case
- Parameters: snake_case with descriptive names
- Response codes: Explicit error messages

### Error Handling
- Include error codes
- Provide actionable error messages
- Log security-relevant errors

## Tech Stack Patterns
### Next.js
[Next.js-specific transformation patterns]

### FastAPI
[FastAPI-specific transformation patterns]

### Go
[Go-specific transformation patterns]

## Common Gotchas
- Missing rate limiting on public endpoints
- Incomplete validation error messages
- Implicit vs explicit security requirements
```

### progress.md Schema

```markdown
# Progress Tracking

## Transformation Quality Metrics

### Compression Efficiency
| Session | Avg Compression | Range |
|---------|----------------|-------|
| 2024-01-20 | 91% | 85-95% |
| 2024-01-19 | 88% | 80-93% |

### Validation Pass Rate
| Session | Pass Rate | Common Failures |
|---------|-----------|-----------------|
| 2024-01-20 | 95% | Missing audit_log (2 cases) |
| 2024-01-19 | 87% | Security requirements (3 cases) |

## Transformation History
- [x] REST API registration endpoint - 95% compression, validation pass
- [x] Authentication flow - 92% compression, 1 warning (audit_log added)
- [x] Database CRUD operations - 88% compression, validation pass
- ... (keep last 20)

## Optimization Results
| Transformation | Before Optimization | After Optimization | Improvement |
|----------------|--------------------|--------------------|-------------|
| Auth endpoint | Missing security params | Complete OWASP coverage | +3 params |
| Database query | No parameterization | Parameterized + pool | +2 params |

## Validation Learnings
### Recurring Issues
- Rate limiting often missed on public endpoints (fixed in patterns.md)
- Audit logging needs explicit mention (added to auth patterns)
- Error response structure incomplete (standardized in patterns.md)

### Validation Improvements Over Time
- Security validation: 85% → 95% pass rate
- Completeness validation: 90% → 97% pass rate
- Edge case coverage: 75% → 88% pass rate

## Domain Knowledge Growth
| Domain | Patterns Learned | Quality |
|--------|------------------|---------|
| REST API | 12 | High confidence |
| Authentication | 8 | High confidence |
| Database | 6 | Medium confidence |
| Validation | 10 | High confidence |
```

## Memory Efficiency (Token-Aware Loading)

### Quick Index Pattern (OPTIONAL)

When a memory file exceeds ~200 lines, add a Quick Index at the top for faster scanning:

```markdown
## Quick Index
| Section | Summary | Lines |
|---------|---------|-------|
| Current Transformation | [1-line summary] | 5-15 |
| User Preferences | [count] preferences | 10-20 |
| Recent Transformations | Last 10 transformations | 30-60 |
| Active Patterns | [count] patterns detected | 15-30 |
| Learnings | [count] insights | 10-20 |

---
[Rest of file content below...]
```

**When to add Quick Index:**
- File exceeds 200 lines
- Multiple distinct transformation sessions
- Frequent partial reads needed

**When NOT needed:**
- File under 200 lines (most projects)
- Simple, focused transformations
- File rarely referenced

### Selective Loading

For large memory files (200+ lines), agents MAY load selectively:

```
# Step 1: Load first 50 lines (Quick Index + Current Context)
Read(file_path=".claude/pseudo-code-prompting/activeContext.md", limit=50)

# Step 2: Decide which sections are relevant to current transformation
# - New transformation → Load "User Preferences", "Active Patterns"
# - Validation → Load "Learnings", "Recent Transformations"
# - Optimization → Load "Patterns", "Optimization Results"

# Step 3: Load specific sections using offset/limit
Read(file_path=".claude/pseudo-code-prompting/activeContext.md", offset=100, limit=50)
```

**Selective Loading Decision Matrix:**
| Task Type | Load First | Then Load If Needed |
|-----------|------------|---------------------|
| TRANSFORM (new requirement) | User Preferences, Active Patterns | Recent Transformations |
| VALIDATE (check completeness) | Learnings, Validation History | Patterns |
| OPTIMIZE (enhance pseudo-code) | Patterns, Optimization Results | Recent Transformations |
| COMPRESS (reduce verbosity) | User Preferences, Compression Style | Recent Compressions |

**DEFAULT: For files under 200 lines, load the entire file. Selective loading adds complexity—only use when needed.**

### Pruning Guidelines

Keep memory files trim for token efficiency:

**When to prune (any file exceeding 200 lines):**

| Memory File | Prune By | Move To |
|-------------|----------|---------|
| **activeContext.md** | Archive old transformations | Keep last 10 only |
| **activeContext.md** | Promote stable patterns | Move to patterns.md |
| **patterns.md** | Archive rarely-used patterns | Keep frequently-used only |
| **progress.md** | Summarize old sessions | Keep last 5 sessions detailed |

**Pruning Rules:**
1. **Recent Transformations**: Keep last 10 entries. Older moves to progress.md summary.
2. **Active Patterns**: Promote to patterns.md when seen 3+ times.
3. **Learnings**: Integrate into patterns.md after validation.
4. **Progress Metrics**: Keep detailed last 5 sessions, summarize older.

## Project Context Auto-Reset Strategy

When loading memory, validate and auto-reset if switching projects:

### Implementation (Every Command START)

```python
# Step 1: Create memory directory
Bash(command="mkdir -p .claude/pseudo-code-prompting")

# Step 2: Load activeContext.md
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")

# Step 3: Extract "Project Path:" from activeContext.md
# Parse the file to find line: "Current Project: [path]"

# Step 4: Get current working directory
# cwd = os.path.abspath(os.getcwd())

# Step 5: Compare paths
# If stored_project_path != cwd:
#   AUTO-RESET activeContext to empty template with new Project Path
# Else:
#   Use context normally
```

### What Gets Reset on Project Switch

When user switches projects (cwd changes):

```markdown
# Active Context (AUTO-RESET)

## Project Path
Current Project: [new cwd]
Last Updated: [current timestamp]
Status: auto_reset_from_previous_project

## Current Transformation
[Empty - starting fresh in new project]

## User Preferences
[Empty - project-specific preferences don't carry over]

## Recent Transformations
[Empty - project-specific history reset]

## Active Patterns
[Empty - will rebuild patterns in new project]

## Learnings This Session
[Empty - starting fresh]

## Blockers / Issues
None

## Last Updated
[current timestamp]
```

### Why Auto-Reset on Project Switch?

Prevents stale preferences/patterns from affecting work in different project:

- **Naming Style**: "snake_case" preference from Python project shouldn't force Python naming in Node.js project
- **Patterns**: "JWT auth" pattern from API project shouldn't suggest JWT for database optimization
- **Context**: User preferences are per-project, not global across machines
- **Accuracy**: Ensures memory always reflects current project state

### Manual Override (Optional)

If user wants to preserve context across projects (rare):

```
# Don't auto-reset, keep previous project context
# User can manually copy patterns between projects if needed
```

---

## Pre-Compaction Memory Safety

### Context Length Awareness

Conversations auto-compact when they get too long. If memory isn't updated before compaction, transformation context is lost forever.

**The Risk:**
```
Long transformation session → Auto-compact → Memory NOT updated → Context LOST
```

### Proactive Update Triggers

Update memory IMMEDIATELY when you notice:
- Multiple transformations in single session (3+ transformations)
- Long optimization cycles (5+ optimization passes)
- Complex validation with many iterations
- Any session with 30+ tool calls
- User says "we've been at this a while"

### The Rule

**When in doubt, update memory NOW.**

Don't wait for workflow end. It's better to have duplicate entries than lost transformation patterns.

### Checkpoint Pattern

During long sessions, periodically checkpoint:
```
# After significant progress, even mid-transformation:
Edit(file_path=".claude/pseudo-code-prompting/activeContext.md",
     old_string="## Current Transformation",
     new_string="## Current Transformation

[Updated with recent progress]

### Checkpoint (mid-session)
- [Key pattern discovered]
- [User preference learned]
- [Optimization applied]")
```

### Red Flags - Update Memory NOW

| Situation | Action |
|-----------|--------|
| "User has specific naming preference" | Record in activeContext.md User Preferences |
| "Multiple transformations completed" | Update progress.md metrics |
| "Pattern detected across transformations" | Add to patterns.md |
| "Validation failed repeatedly on same issue" | Record learning in activeContext.md |

## File Purposes

### activeContext.md (Read/Write EVERY session)

**Current state of transformations - ALWAYS check this first:**

Use for:
- Current transformation context
- User preferences (naming, style, security focus)
- Recently discovered patterns
- Session learnings
- Active decisions affecting transformations

### patterns.md (Accumulates over time)

**Domain-specific transformation knowledge that persists:**

Use for:
- REST API transformation patterns
- Authentication patterns (JWT, OAuth2)
- Database query patterns
- Validation patterns (email, password, etc.)
- Security patterns (OWASP coverage)
- Tech stack patterns (Next.js, FastAPI, Go)
- Common transformation gotchas

### progress.md (Tracks quality)

**Transformation quality and history:**

Use for:
- Compression efficiency trends
- Validation pass rates
- Transformation history (last 20)
- Optimization effectiveness
- Domain knowledge growth metrics

## READ Triggers - When to Load Memory

### ALWAYS Read (Non-Negotiable)

| Trigger | Action | Why |
|---------|--------|-----|
| **Session start** | Load ALL 3 files | Fresh context needed |
| **New transformation** | Load ALL 3 files | Before transform pipeline |
| **Validation phase** | Load activeContext.md + patterns.md | Apply learned patterns |
| **Optimization phase** | Load patterns.md + progress.md | Use optimization history |

### Read BEFORE These Actions

| Before This Action | Read This File | Why |
|--------------------|----------------|-----|
| **Transforming requirement** | activeContext.md + patterns.md | Apply user preferences + domain patterns |
| **Validating pseudo-code** | patterns.md | Check against learned patterns |
| **Optimizing pseudo-code** | progress.md + patterns.md | Use successful optimizations |
| **Compressing verbose text** | activeContext.md | Apply user's compression preferences |
| **Making any decision** | activeContext.md | Check prior preferences |

### Read WHEN You Notice

| Situation | Action | Why |
|-----------|--------|-----|
| User corrects transformation | Load activeContext.md | Update preferences |
| Repeated validation failure | Load patterns.md | Check for known pattern |
| User specifies tech stack | Load patterns.md | Apply stack-specific patterns |
| Transformation seems familiar | Load progress.md | Check history |

### File Selection Matrix

```
What do I need?              → Which file?
─────────────────────────────────────────
Current transformation state → activeContext.md
User preferences             → activeContext.md (User Preferences)
Learned patterns             → patterns.md
Domain-specific patterns     → patterns.md (by domain)
Tech stack conventions       → patterns.md (Tech Stack Patterns)
Transformation history       → progress.md
Quality metrics              → progress.md
Optimization results         → progress.md
```

### Decision Integration

**Before ANY transformation decision, ask:**

1. **Did user express preference?** → Check activeContext.md User Preferences
2. **Is there a learned pattern?** → Check patterns.md
3. **Have we seen this before?** → Check progress.md history

**If memory has relevant info:**
- Apply user preference
- Use learned pattern
- Reference successful optimization

**If memory is empty/irrelevant:**
- Make decision based on best practices
- RECORD it in activeContext.md for next time

---

## Mandatory Operations

### At Workflow START (REQUIRED)

**Use separate tool calls (PERMISSION-FREE):**

```
# Step 1: Create directory (single Bash command - permission-free)
Bash(command="mkdir -p .claude/pseudo-code-prompting")

# Step 2: Load ALL 3 memory files using Read tool (permission-free)
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")
Read(file_path=".claude/pseudo-code-prompting/patterns.md")
Read(file_path=".claude/pseudo-code-prompting/progress.md")

# Step 3: Project Context - Understand current state (RECOMMENDED)
Bash(command="git status")                 # If in git repo
```

**NEVER use this (asks permission):**
```bash
# WRONG - compound command asks permission
mkdir -p .claude/pseudo-code-prompting && cat .claude/pseudo-code-prompting/activeContext.md
```

**If file doesn't exist:** Read tool returns an error - that's fine, means starting fresh.

### At Workflow END (REQUIRED)

**MUST update before completing ANY transformation workflow. Use Edit tool (NO permission prompt):**

```
# First, read the existing content
Read(file_path=".claude/pseudo-code-prompting/activeContext.md")

# Then use Edit to update (matches first line, replaces with updated content)
Edit(file_path=".claude/pseudo-code-prompting/activeContext.md",
     old_string="# Active Context",
     new_string="# Active Context

## Current Transformation
[What we just transformed / what's next]

## User Preferences
| Preference | Value | Source |
|------------|-------|--------|
[Updated preferences]

## Recent Transformations
- [New transformation added to list]

## Active Patterns
[Updated patterns]

## Learnings This Session
- [What we learned]

## Last Updated
[current date/time]")
```

**WHY Edit not Write?** Write asks "Do you want to overwrite?" for existing files. Edit is always permission-free.

### When Learning Patterns (APPEND)

**Read existing patterns.md, then append using Edit:**

```
# Read existing content
Read(file_path=".claude/pseudo-code-prompting/patterns.md")

# Append by matching section heading and adding new pattern
Edit(file_path=".claude/pseudo-code-prompting/patterns.md",
     old_string="## REST API Patterns",
     new_string="## REST API Patterns

### [New Pattern Name]
[Pattern details discovered from transformations]")
```

### When Recording Progress (UPDATE)

```
# Read progress.md, update metrics using Edit
Read(file_path=".claude/pseudo-code-prompting/progress.md")

Edit(file_path=".claude/pseudo-code-prompting/progress.md",
     old_string="## Transformation History",
     new_string="## Transformation History
- [x] [New transformation] - [metrics]
[existing history]")
```

## Integration with Agents

**ALL agents MUST:**

1. **START**: Load memory files before any transformation work
2. **DURING**: Note learnings, patterns, and user preferences
3. **END**: Update memory files with new context

**Failure to update memory = incomplete work.**

## Agent-Specific Memory Usage

### prompt-analyzer
- **Load**: activeContext.md (user preferences), patterns.md (known ambiguities)
- **Check**: Has user indicated verbosity preference? Domain-specific ambiguities?
- **Update**: Record recurring ambiguity patterns

### prompt-transformer
- **Load**: activeContext.md (naming preferences), patterns.md (domain patterns)
- **Check**: User's preferred naming style? Tech stack patterns?
- **Update**: Record new transformation patterns discovered

### prompt-optimizer
- **Load**: patterns.md (security patterns), progress.md (optimization history)
- **Check**: Common missing parameters? Security requirements?
- **Update**: Record successful optimizations

### requirement-validator
- **Load**: patterns.md (validation patterns), progress.md (validation history)
- **Check**: Known validation failures? Domain-specific requirements?
- **Update**: Record validation learnings

### context-compressor
- **Load**: activeContext.md (compression preferences)
- **Check**: User's preferred compression ratio? Verbosity level?
- **Update**: Record compression style preferences

## Red Flags - STOP IMMEDIATELY

If you catch yourself:
- Starting transformation WITHOUT loading memory
- Making decisions WITHOUT checking User Preferences
- Completing transformation WITHOUT updating memory
- Saying "I assume user wants X" instead of checking memory

**STOP. Load/update memory FIRST.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know what user prefers" | Check User Preferences table. |
| "Small transformation, no need" | Small transformations have patterns too. Always update. |
| "I'll remember" | You won't. Conversation compacts. Write it down. |
| "Memory is optional" | Memory is MANDATORY. No exceptions. |

## Verification Checklist

- [ ] Memory loaded at transformation start
- [ ] User preferences checked before decisions
- [ ] Patterns applied to transformation
- [ ] Learnings documented in activeContext.md
- [ ] Progress updated in progress.md

**Cannot check all boxes? Memory cycle incomplete.**

## The Bottom Line

```
START → Load Memory → Transform → Update Memory → END
         ↑              ↑              ↑
      MANDATORY    Check before    MANDATORY
                   decisions
```

**The Full Cycle:**
```
1. LOAD all memory (START)
2. CHECK memory before transformation decisions (DURING)
3. UPDATE memory with learnings and patterns (END)
```

**Memory persistence is not a feature. It's a requirement.**

Your effectiveness depends entirely on memory accuracy. Treat it with the same importance as the transformation itself.

READ without WRITE = Stale patterns.
WRITE without READ = Contradictory preferences.
**Both are equally critical.**
