# Token Usage Analyzer

## Overview

This analyzer helps identify token usage patterns in a session to improve efficiency and reduce costs. It focuses on detecting wasteful patterns and suggesting optimizations.

## Token Estimation Formula

Use rough approximations for quick analysis:

```
Estimated tokens ≈ (characters / 4)

Tool call overhead:
- Read: ~100 tokens base + file content tokens
- Grep: ~100 tokens base + matches tokens
- Edit: ~100 tokens base + old string + new string tokens
- Bash: ~100 tokens base + output tokens
- Write: ~100 tokens base + content tokens
- Task (Agent): ~500 tokens base + agent work tokens
```

## Analysis Categories

### 1. File Reading Efficiency

**Anti-Patterns to Detect:**

❌ **Reading large files multiple times**
- Same file read 2+ times in session
- Could cache information from first read
- Example: Reading `schema.prisma` twice when once would suffice

❌ **Full file reads when targeted search would work**
- Reading 1000+ line file to find one function
- Should use Grep first, then Read specific section
- Example: `Read package.json` when you only need to check one dependency

❌ **Reading generated/build artifacts**
- Reading node_modules files
- Reading build output files
- Reading .next or dist directories
- These are wasteful and rarely necessary

**Good Patterns to Recognize:**

✅ **Using offset/limit for large files**
- Reading files in chunks
- Only reading necessary sections

✅ **Using Grep before Read**
- Search first, read targeted sections
- Avoids loading unnecessary content

✅ **Caching information from earlier in conversation**
- Reference previous reads
- Don't re-read for same information

### 2. Search Pattern Efficiency

**Anti-Patterns to Detect:**

❌ **Redundant searches**
- Same Grep pattern used multiple times
- Same Glob pattern used multiple times
- Could cache and reference earlier results

❌ **Overly broad glob patterns**
- Using `**/*` when `**/*.ts` would work
- Searching entire codebase when subdirectory would suffice
- Example: Glob `**/*` then Glob `**/*.tsx` (should combine)

❌ **Sequential searches that could be combined**
- Multiple Grep calls that could use regex alternation
- Multiple Glob patterns that could use brace expansion
- Example: Glob `**/*.ts` then `**/*.tsx` (use `**/*.{ts,tsx}`)

**Good Patterns to Recognize:**

✅ **Targeted directory searches**
- Searching specific subdirectories
- Using appropriate file type filters

✅ **Combined patterns**
- Using brace expansion in Glob
- Using regex alternation in Grep

✅ **Context limits in Grep**
- Using appropriate -A, -B, -C flags
- Using head_limit to constrain results

### 3. Response Efficiency

**Anti-Patterns to Detect:**

❌ **Verbose explanations repeated multiple times**
- Explaining same concept 3+ times
- Could reference earlier explanation
- Could reference CLAUDE.md or project docs

❌ **Unnecessary multi-paragraph responses**
- >500 characters when <200 would suffice
- Over-explaining simple tasks
- Too much preamble before action

❌ **Redundant tool calls**
- Calling same tool with same parameters multiple times
- Not utilizing information from earlier calls

**Good Patterns to Recognize:**

✅ **Concise, actionable responses**
- Clear and brief
- Gets to the point quickly

✅ **Referencing earlier context**
- "As mentioned earlier..."
- "From the previous read..."

✅ **Using documentation references**
- Pointing to CLAUDE.md
- Referencing existing project docs

## Efficiency Scoring (0-100)

### Base Score Calculation

Start with: **100 points**

### Deductions

| Issue | Deduction | Notes |
|-------|-----------|-------|
| Duplicate file read | -5 per occurrence | Same file read 2+ times |
| Large file full read when Grep would work | -10 per occurrence | Files >500 lines |
| Redundant search | -3 per occurrence | Same pattern used 2+ times |
| Overly verbose response | -2 per occurrence | >500 chars when <200 sufficient |
| Reading generated files | -8 per occurrence | node_modules, build artifacts |
| Broad glob when specific would work | -3 per occurrence | Could narrow with file type |

### Bonuses

| Practice | Bonus | Notes |
|----------|-------|-------|
| Used Grep before Read | +2 per occurrence | Targeted searching |
| Used offset/limit for large files | +3 per occurrence | Efficient file reading |
| Cached information from earlier | +3 per occurrence | Referenced previous reads |
| Concise responses | +1 per occurrence | <200 chars, clear and complete |
| Combined search patterns | +2 per occurrence | Brace expansion, regex alternation |

### Final Score

```
Final Efficiency Score = max(0, min(100, Base Score + Bonuses - Deductions))
```

**Score Interpretation:**
- 90-100: Excellent efficiency
- 75-89: Good efficiency with minor optimization opportunities
- 60-74: Moderate efficiency, several improvements possible
- 40-59: Below average, significant waste identified
- 0-39: Poor efficiency, major optimization needed

## Report Format

When analyzing token usage, generate a report with this structure:

```markdown
### Token Usage Analysis

**Estimated Total Tokens:** ~XXX,XXX tokens
**Efficiency Score:** YY/100

#### Token Breakdown:
| Category | Tokens | Percentage |
|----------|--------|------------|
| File Operations | XX,XXX | XX% |
| Code Generation | XX,XXX | XX% |
| Planning/Design | XX,XXX | XX% |
| Explanations | XX,XXX | XX% |
| Search Operations | X,XXX | X% |

#### Optimization Opportunities:

1. ⚠️ **[Issue Type]**: [Specific description]
   - Current approach: [What was done]
   - Better approach: [Recommendation]
   - Potential savings: ~XXX tokens

2. ⚠️ **[Issue Type]**: [Specific description]
   - Current approach: [What was done]
   - Better approach: [Recommendation]
   - Potential savings: ~XXX tokens

[Continue for top 5 issues]

#### Good Practices:

1. ✅ **[Practice]**: [What worked well]
2. ✅ **[Practice]**: [What worked well]

[Continue for notable good practices]
```

## Analysis Guidelines

### How to Analyze

1. **Review conversation chronologically**
   - Scan all tool calls in order
   - Track file operations (Read, Write, Edit)
   - Track search operations (Grep, Glob)
   - Note response lengths

2. **Calculate token estimates**
   - Count characters in file reads
   - Count characters in tool outputs
   - Count characters in responses
   - Apply estimation formula (chars / 4)

3. **Identify patterns**
   - Look for duplicate operations
   - Find inefficient approaches
   - Spot good practices
   - Calculate category totals

4. **Prioritize by impact**
   - Focus on largest token consumers
   - Identify highest-impact optimizations
   - Note most frequent issues
   - Limit to top 5 opportunities

5. **Generate recommendations**
   - Be specific and actionable
   - Include examples from the session
   - Suggest concrete alternatives
   - Balance criticism with positive reinforcement

### Limit to Top 5

Only report the **5 most impactful** optimization opportunities:
- Prioritize by potential token savings
- Focus on patterns (not one-offs)
- Include teachable moments
- Skip minor inefficiencies

### Be Constructive

- Use ⚠️ for issues, ✅ for good practices
- Explain why something is inefficient
- Suggest specific improvements
- Acknowledge what worked well
- Focus on learning and improvement

## Examples

### Example 1: Duplicate File Read

❌ **Anti-Pattern Detected:**
```
Read app/db/prisma/schema.prisma (full file, 1000 lines) at timestamp 10:15
Read app/db/prisma/schema.prisma (full file, 1000 lines) at timestamp 10:45
```

**Analysis:**
- Issue: Duplicate file read
- Token cost: ~1,000 characters × 2 = 2,000 chars ≈ 500 tokens (wasted: 250 tokens)
- Better approach: Use Grep to verify field on second check

**Report Entry:**
```markdown
⚠️ **Duplicate File Read**: Read `schema.prisma` fully twice during implementation
- Current approach: Full file read at 10:15 and again at 10:45
- Better approach: Use Grep for second verification (e.g., `grep "isLockedForAutoAssign" schema.prisma`)
- Potential savings: ~250 tokens
```

### Example 2: Grep Before Read

✅ **Good Pattern Detected:**
```
Grep pattern="requireRole" path="app/ui/app/api" at timestamp 10:20
Read app/ui/app/api/admin/students/route.ts lines 1-50 at timestamp 10:22
```

**Analysis:**
- Good practice: Used Grep to find relevant files first
- Then targeted Read of specific section
- Efficient approach avoided reading multiple full files

**Report Entry:**
```markdown
✅ **Targeted Search**: Used Grep to locate `requireRole` usage before reading files
- Found the pattern in specific files
- Then read only relevant sections
- Avoided unnecessary full-file reads
```

### Example 3: Verbose Response

❌ **Anti-Pattern Detected:**
```
Response length: 800 characters explaining a simple typo fix
Simple task: Change "userId" to "user.id"
```

**Analysis:**
- Issue: Overly verbose for simple task
- Token cost: ~200 tokens
- Could be: ~50 tokens with concise response

**Report Entry:**
```markdown
⚠️ **Verbose Explanation**: 800-character explanation for simple property rename
- Current approach: Multi-paragraph explanation of userId → user.id change
- Better approach: Brief note "Fixed property access: userId → user.id"
- Potential savings: ~150 tokens
```

## Common Token-Heavy Operations

### Ranked by Typical Token Cost

1. **Full File Reads** - 500-5,000+ tokens each
2. **Code Generation** - 200-2,000+ tokens per file
3. **Agent Spawns** - 500-10,000+ tokens per agent
4. **Explanatory Responses** - 100-500 tokens each
5. **Search Results** - 50-500 tokens per operation

### Focus Analysis On

- File reading patterns (highest impact)
- Agent usage efficiency
- Code generation approach
- Response verbosity
- Search strategy
