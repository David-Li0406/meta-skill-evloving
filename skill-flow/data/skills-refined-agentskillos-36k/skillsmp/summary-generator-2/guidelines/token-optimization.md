# Token Optimization Guidelines

## Overview

These guidelines help reduce token usage while maintaining quality and effectiveness. The goal is to be efficient without compromising on clarity or thoroughness.

## Core Principles

1. **Read Once, Reference Often** - Cache information in conversation context
2. **Search Before Reading** - Use Grep/Glob to target specific content
3. **Be Concise Yet Complete** - Clear and brief without losing substance
4. **Avoid Redundancy** - Don't repeat what's already been established
5. **Use Documentation** - Reference CLAUDE.md and project docs

## File Reading Optimization

### DO: Use Targeted Searches

✅ **Pattern: Grep → Read Specific Section**
```
1. Grep pattern="functionName" path="src/"
2. Read src/utils/helper.ts offset=50 limit=20
```

**Why:** Only loads the relevant portion, not entire file

✅ **Pattern: Use offset/limit for Large Files**
```
Read package.json offset=0 limit=50  # Just dependencies
Read schema.prisma offset=100 limit=100  # Specific model
```

**Why:** Avoids loading thousands of lines when you need dozens

### DON'T: Read Full Files Repeatedly

❌ **Anti-Pattern: Multiple Full Reads**
```
Read schema.prisma  # 1000 lines loaded
... 30 minutes later ...
Read schema.prisma  # Same 1000 lines loaded again
```

**Better:**
```
Read schema.prisma  # First read
... later ...
Grep pattern="StudentProfile" path="schema.prisma"  # Just check field exists
```

❌ **Anti-Pattern: Read When Grep Suffices**
```
Read src/config/database.ts  # 500 lines
# Only needed to check if connection string is configured
```

**Better:**
```
Grep pattern="connectionString" path="src/config/database.ts"
```

### DON'T: Read Generated Files

❌ **Anti-Pattern: Reading Build Artifacts**
```
Read node_modules/@types/react/index.d.ts
Read .next/server/pages/api/users.js
Read dist/bundle.js
```

**Why:** These are large, generated, and rarely useful. Use documentation instead.

**Better:**
- Reference official documentation
- Read source files, not compiled output
- Trust type definitions without reading them

## Search Pattern Optimization

### DO: Combine Patterns

✅ **Pattern: Use Brace Expansion**
```
Glob pattern="**/*.{ts,tsx,js,jsx}"
```

**Why:** One search instead of four

✅ **Pattern: Use Appropriate Scope**
```
Grep pattern="useState" path="app/ui/components/" type="tsx"
```

**Why:** Searches only relevant directory and file type

### DON'T: Sequential Similar Searches

❌ **Anti-Pattern: Multiple Similar Globs**
```
Glob pattern="**/*.ts"
Glob pattern="**/*.tsx"
Glob pattern="**/*.js"
```

**Better:**
```
Glob pattern="**/*.{ts,tsx,js}"
```

❌ **Anti-Pattern: Redundant Greps**
```
Grep pattern="import.*useState"
Grep pattern="import.*useEffect"
Grep pattern="import.*useMemo"
```

**Better:**
```
Grep pattern="import.*(useState|useEffect|useMemo)"
```

## Response Optimization

### DO: Be Concise

✅ **Pattern: Direct and Clear**
```
"Fixed import path from '@/lib/auth' to '@/lib/authz' in auto-assign/route.ts"
```

**Token Cost:** ~20 tokens

✅ **Pattern: Bullets Over Paragraphs**
```
Updated the auto-assignment algorithm:
- Added gender balance scoring (50% weight)
- Added age distribution balance (30% weight)
- Added capacity optimization (20% weight)
```

**Token Cost:** ~40 tokens

### DON'T: Over-Explain Simple Tasks

❌ **Anti-Pattern: Verbose Explanation**
```
"I notice there's an error in the import statement. The import is trying to use '@/lib/auth' but that module doesn't exist in the codebase. After searching through the project, I found that the correct path is '@/lib/authz' which contains the authentication and authorization utilities. I'll update this import to use the correct path so that the code can properly access the requireRole function."
```

**Token Cost:** ~100 tokens

**Better:**
```
"Fixed import path: '@/lib/auth' → '@/lib/authz'"
```

**Token Cost:** ~15 tokens

❌ **Anti-Pattern: Repeated Explanations**
```
# First time: Explain project structure (good)
# Second time: Explain project structure again (wasteful)
# Third time: Explain project structure again (very wasteful)
```

**Better:**
```
# First time: Explain project structure
# Later: "As mentioned earlier, the UI is in app/ui/"
# Or: "See CLAUDE.md for project structure"
```

## Agent Usage Optimization

### DO: Use Agents for Complex Tasks

✅ **Pattern: Explore Agent for Codebase Understanding**
```
Task: Use Explore agent to understand authentication flow
- Agent performs multiple searches
- Agent reads multiple files
- Returns synthesized understanding
```

**Why:** One agent spawn is cheaper than you doing 10 searches manually

### DON'T: Spawn Agents for Simple Lookups

❌ **Anti-Pattern: Agent for Single File**
```
Task: Use Explore agent to find if schema.prisma has StudentProfile model
```

**Better:**
```
Grep pattern="model StudentProfile" path="schema.prisma"
```

**Why:** Grep is ~100 tokens, Agent spawn is ~500+ tokens

## Code Generation Optimization

### DO: Generate Complete, Correct Code

✅ **Pattern: One-Shot Implementation**
```
Write complete component with:
- All imports
- Full type definitions
- Complete implementation
- No placeholders
```

**Why:** Generating once is cheaper than generating, fixing, regenerating

✅ **Pattern: Read Types Before Implementing**
```
1. Read existing component interfaces
2. Generate new component matching patterns
3. No type errors, no rework
```

**Why:** Prevents costly regeneration due to type mismatches

### DON'T: Generate Incrementally for Simple Code

❌ **Anti-Pattern: Multiple Small Generations**
```
1. Generate function signature
2. Generate function body
3. Generate type definition
4. Generate tests
```

**Better:**
```
1. Generate complete function with types and implementation
```

**Why:** Each generation has overhead; consolidating is more efficient

## Caching and Referencing

### DO: Reference Earlier Context

✅ **Pattern: Reference Previous Work**
```
"Using the same pattern we established in the auto-assignment algorithm..."
"As shown in the earlier Read of schema.prisma, the field is..."
```

**Why:** Avoids re-reading or re-explaining

✅ **Pattern: Use Project Documentation**
```
"See CLAUDE.md for the i18n pattern"
"Following the API route pattern documented in CLAUDE.md"
```

**Why:** Documentation is already in context, no need to re-read files

### DON'T: Re-Establish Known Information

❌ **Anti-Pattern: Re-Reading for Confirmation**
```
# You already read schema.prisma earlier
# You know the field exists
# But you read it again to confirm
```

**Better:**
```
# Trust earlier read
# Reference conversation history
# Only re-read if structure might have changed
```

## Planning Optimization

### DO: Plan Before Implementing

✅ **Pattern: Think First, Code Second**
```
1. Understand requirements
2. Ask clarifying questions
3. Create plan
4. Implement systematically
```

**Why:** Prevents rework, false starts, and wasted generation

### DON'T: Code-Fix-Code Cycle

❌ **Anti-Pattern: Trial and Error**
```
1. Generate code (guess at structure)
2. TypeScript errors
3. Fix errors
4. More errors
5. Fix again
6. Finally works
```

**Better:**
```
1. Read existing patterns
2. Read type definitions
3. Generate correct code first time
```

**Why:** Each generation/fix cycle costs tokens

## Explanation Optimization

### DO: Explain Decisions, Not Actions

✅ **Pattern: Explain Why, Not What**
```
"Using balance scoring (50% gender, 30% age, 20% capacity) because it prioritizes gender equity while maintaining reasonable age distribution."
```

**Why:** Adds value beyond what's visible in the code

### DON'T: Narrate Every Action

❌ **Anti-Pattern: Play-by-Play**
```
"Now I'm going to use the Read tool to read the file. After reading the file, I'll look for the function. Once I find the function, I'll use the Edit tool to modify it. After editing, I'll verify the changes..."
```

**Better:**
```
"Reading file to locate function for modification."
```

**Why:** Actions are self-evident from tool calls

## Practical Guidelines

### Before Each Action

Ask yourself:
1. **Do I need to read this file?** Could Grep answer my question?
2. **Have I already read this?** Can I reference earlier context?
3. **Is this the minimal search?** Can I narrow the scope?
4. **Is this explanation necessary?** Is it self-evident?
5. **Can I combine operations?** Multiple patterns in one call?

### Token Budget Awareness

Think of tokens as a budget:
- **Large Files:** 500-5000 tokens each
- **Agent Spawns:** 500-10,000 tokens
- **Code Generation:** 200-2000 tokens
- **Explanations:** 100-500 tokens
- **Simple Responses:** 20-100 tokens

Spend wisely on what adds most value.

### Quality vs Efficiency

**Never Sacrifice:**
- Correctness
- Security
- User clarity
- Critical explanations

**Always Optimize:**
- Redundant operations
- Unnecessary verbosity
- Repeated searches
- Over-documentation

## Efficiency Checklist

Use this checklist during sessions:

**File Operations:**
- [ ] Used Grep before Read when searching
- [ ] Used offset/limit for large files
- [ ] Avoided re-reading same file
- [ ] Didn't read generated/build files

**Search Operations:**
- [ ] Combined similar patterns
- [ ] Scoped to relevant directories
- [ ] Used appropriate file type filters
- [ ] Cached search results

**Responses:**
- [ ] Kept responses concise
- [ ] Used bullets over paragraphs
- [ ] Referenced earlier explanations
- [ ] Avoided narrating actions

**Code Generation:**
- [ ] Read types/patterns first
- [ ] Generated complete code
- [ ] Avoided incremental generation
- [ ] Minimized rework

**Planning:**
- [ ] Asked questions upfront
- [ ] Created clear plan
- [ ] Understood requirements
- [ ] Avoided trial-and-error

## Target Efficiency

**Aim for:**
- Efficiency Score: 85+
- <10% redundant operations
- <5 duplicate file reads
- Concise responses (<200 chars for simple tasks)
- High first-attempt success rate

**Signs of Good Efficiency:**
- Minimal rework
- Few retries
- Targeted searches
- Brief, clear communication
- Systematic progression

## Remember

Efficiency is about **maximizing value per token**, not minimizing explanation or rushing through work. Take time to plan, ask questions, and understand requirements—this prevents costly rework later.
