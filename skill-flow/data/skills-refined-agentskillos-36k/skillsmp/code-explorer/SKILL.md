---
name: code-explorer
description: 'Hybrid search strategy for finding relevant code: fast targeted search, then deep analysis if needed.'
---

## Purpose

Given extracted keywords from an issue, locate the relevant code in the repository.

**Strategy:** Start fast and targeted, escalate to comprehensive if needed.

## Usage

Include this file when searching for code:

```
Use lib/code-explorer to find code related to [keywords]
```

## Phase 1: Targeted Search (30 seconds)

Use `Grep` and `Glob` tools for fast pattern matching.

### Step 1: Prepare Search Patterns

From parsed issue, create search patterns:

**Error messages → Grep patterns:**
```
"AuthenticationError" → grep for "AuthenticationError"
"token expired" → grep for "token.*expir|expir.*token"
```

**File paths → Glob patterns:**
```
"src/auth/middleware.ts" → glob for that exact file
"auth" → glob for "**/*auth*.{ts,js,py}"
```

**Function names → Grep patterns:**
```
"handleLogin" → grep for "function handleLogin|const handleLogin|handleLogin\s*[:=(]"
```

### Step 2: Execute Searches in Parallel

Run multiple searches simultaneously:

```bash
# Use Grep tool (NOT bash grep)
Grep pattern="AuthenticationError"
Grep pattern="token.*expir|expir.*token"
Grep pattern="function handleLogin|const handleLogin"

# Use Glob tool (NOT bash find)
Glob pattern="**/*auth*.{ts,js,py,go,rs}"
Glob pattern="**/*login*.{ts,js,py,go,rs}"
Glob pattern="**/middleware*.{ts,js,py,go,rs}"
```

**Important:** Run tools in parallel (single message, multiple tool calls) for speed.

### Step 3: Evaluate Results

Count highly relevant files (files matching multiple patterns):

```python
relevant_files = {}
for result in search_results:
    for file in result.files:
        relevant_files[file] = relevant_files.get(file, 0) + 1

high_relevance = [f for f, count in relevant_files.items() if count >= 2]
```

**Decision:**
- **≥3 high-relevance files:** Proceed to planning
- **<3 files OR unclear context:** Escalate to Phase 2

### Step 4: Read High-Relevance Files

If targeted search successful:

```bash
# Read the top relevant files
Read file_path="src/auth/middleware.ts"
Read file_path="src/auth/handlers.ts"
Read file_path="src/utils/token.ts"
```

Extract understanding:
- What's the current implementation?
- Where's the bug likely located?
- What needs to change?

---

## Phase 2: Deep Analysis (2-5 minutes)

If targeted search insufficient, spawn Explore agent.

### When to Escalate

- Found <3 relevant files
- Files found but context unclear (don't understand the connection)
- Keywords too generic (e.g., "error", "user")
- Complex architectural issue

### Step 1: Spawn Explore Agent

```markdown
Use Task tool with subagent_type=Explore

Prompt: "Analyze the codebase to understand [issue summary from title].

Focus areas:
- [keyword 1]
- [keyword 2]
- [keyword 3]

Specific questions:
1. Where in the code does [error] occur?
2. What's the root cause of [problem]?
3. What files need to change to fix this?

Trace execution flow from [entry point] to the error location."
```

### Step 2: Extract Agent Findings

Explore agent returns comprehensive analysis:

```markdown
**Agent findings:**
- Root cause: Session timeout hardcoded at 30s in src/auth/config.ts:12
- Related files: src/auth/middleware.ts uses the config
- Execution flow: Request → middleware → checkSession → timeout
- Recommendation: Make timeout configurable
```

### Step 3: Validate Findings

Read the specific files mentioned:

```bash
Read file_path="src/auth/config.ts"
Read file_path="src/auth/middleware.ts"
```

Confirm agent's analysis is correct.

---

## Output Format

After exploration, format findings for plan generation:

```markdown
## Code Exploration Results

**Search Strategy:** [Targeted / Deep Analysis]

**Root Cause:**
[What's causing the issue, specific file and line if found]

**Relevant Files:**
- `src/auth/config.ts:12` - Hardcoded timeout value
- `src/auth/middleware.ts:45-60` - Uses the timeout
- `tests/auth.test.ts` - Existing tests to update

**Understanding:**
[Explanation of how the code works and why the bug occurs]

**Confidence:** [High / Medium / Low]
- High: Found exact location, clear root cause
- Medium: Found area, but need to investigate during implementation
- Low: General area identified, implementation will refine understanding
```

## Examples

### Example 1: Successful Targeted Search

**Issue:** "Login fails with 'Session expired' after 30 seconds"

**Targeted search:**
```bash
Grep "session.*expir|expir.*session"
Grep "timeout.*30|30.*timeout"
Glob "**/*session*.{ts,js}"
Glob "**/*auth*.{ts,js}"
```

**Results:**
- 5 files found
- `auth/config.ts` matches 3 patterns (session, timeout, 30)
- `auth/middleware.ts` matches 2 patterns (session, auth)

**Outcome:** ✅ Proceed to planning with these files

### Example 2: Escalation to Deep Analysis

**Issue:** "Users can't access their profile"

**Targeted search:**
```bash
Grep "profile"
Glob "**/*profile*.{ts,js}"
```

**Results:**
- 15 files found (too many)
- No clear root cause
- Context unclear

**Outcome:** ⬆️ Escalate to Explore agent

**Deep analysis:**
```markdown
Task tool: "Analyze why users can't access profiles. Trace from route handler to database query."

Agent finds:
- Route: src/routes/profile.ts
- Controller: src/controllers/user.ts
- Issue: Missing authorization check in middleware
- Root cause: src/middleware/auth.ts:67 - doesn't verify user owns profile
```

**Outcome:** ✅ Proceed to planning with clear root cause

---

## Integration with handle-issue

```markdown
1. Parse issue (lib/issue-parser)
2. Explore code (lib/code-explorer) ← YOU ARE HERE
3. Generate plan (lib/plan-generator)
4. Post to GitHub
```

**Flow:**
```
Keywords from parser
    ↓
Targeted search (Grep/Glob)
    ↓
Evaluate results
    ↓
    ├─ ≥3 files → Read files → Generate plan
    └─ <3 files → Deep analysis → Generate plan
```

## Performance Considerations

**Targeted search:**
- Speed: ~30 seconds
- Cost: Low (few tool calls)
- Success rate: ~70% for well-described issues

**Deep analysis:**
- Speed: 2-5 minutes
- Cost: Higher (spawns agent)
- Success rate: ~90% overall

**Combined:** 95% success rate, avg 1-2 minutes

## Error Handling

**No results found:**
```markdown
Return to user:
"🔍 **Analysis Incomplete**

Searched for:
- Keywords: X, Y, Z
- File patterns: **/*pattern*

Couldn't locate relevant code. Please provide:
- Specific file names or paths
- Function/class names involved
- More detailed error messages"
```

**Ambiguous results:**
```markdown
"Found multiple potential locations:
1. src/auth/old-login.ts (deprecated?)
2. src/auth/login.ts (likely)
3. src/v2/auth/login.ts (new version?)

Please clarify which module is relevant."
```

## YAGNI Notes

**Not included:**
- AI-powered code understanding (use Explore agent)
- Caching search results (fresh search each time)
- Multi-repository search (single repo only)
- Semantic code search (pattern matching sufficient)

Keep it simple: fast search, escalate if needed.
