# Search Strategies

This document provides effective search techniques for codebase analysis using Grep, Glob, Read, and Bash tools. Master these strategies to find information quickly and comprehensively.

## Overview

Effective searching is critical for codebase research. This guide covers tool selection, search patterns, and optimization techniques for common research scenarios.

---

## Tool Selection Guide

### When to Use Each Tool

**Grep** - Content search
- Finding implementations, usages, patterns
- Searching for specific code constructs
- Discovering naming conventions
- Locating specific strings or regex patterns

**Glob** - File pattern matching
- Finding files by name pattern
- Discovering file organization
- Counting files of specific types
- Identifying file naming conventions

**Read** - File reading
- Reading specific known files
- Understanding implementations
- Analyzing examples
- Reading documentation

**Bash (ls)** - Directory operations
- Listing directory contents
- Understanding directory structure
- Quick file counts
- Directory organization analysis

**General rule**:
- **Find files** → Glob or ls
- **Find content** → Grep
- **Read specific files** → Read
- **Directory structure** → Bash (ls)

---

## Grep Strategies

### Basic Grep Patterns

#### 1. Finding Definitions

**Class definitions**:
```bash
# TypeScript/JavaScript
Grep: "class \w+" (output_mode: content, head_limit: 50)
Grep: "export class \w+" (output_mode: content)

# Python
Grep: "class \w+\(" (output_mode: content)
Grep: "^class \w+" (output_mode: content)
```

**Function definitions**:
```bash
# TypeScript/JavaScript
Grep: "function \w+|const \w+ = " (output_mode: content, head_limit: 50)
Grep: "export function \w+" (output_mode: content)
Grep: "async function \w+" (output_mode: content)

# Python
Grep: "def \w+\(" (output_mode: content, head_limit: 50)
Grep: "async def \w+\(" (output_mode: content)
```

**Interface/Type definitions**:
```bash
# TypeScript
Grep: "interface \w+" (output_mode: content)
Grep: "type \w+ = " (output_mode: content)
```

#### 2. Finding Usage

**Imports**:
```bash
# Find all imports of specific module
Grep: "import.*UserService" (output_mode: files_with_matches)
Grep: "from.*user.*import" (output_mode: content)

# Find where specific function is imported
Grep: "import.*{.*getUserById" (output_mode: content)
```

**Function calls**:
```bash
# Find calls to specific function
Grep: "getUserById\(" (output_mode: content)

# Find method calls on service
Grep: "userService\.\w+\(" (output_mode: content)
Grep: "this\.\w+Service\." (output_mode: content)
```

**Variable usage**:
```bash
# Find where variable is used
Grep: "\buser\b" (output_mode: files_with_matches)

# Note: \b for word boundaries to avoid matching "username", "userService", etc.
```

#### 3. Finding Patterns

**API endpoints**:
```bash
# Express/NestJS
Grep: "@Get|@Post|@Put|@Delete|@Patch" (output_mode: content)
Grep: "router\.get|app\.get|router\.post" (output_mode: content)

# FastAPI
Grep: "@app\.get|@app\.post|@router\.get" (output_mode: content)

# Find specific endpoint
Grep: '"/api.*users' (output_mode: content)
```

**Database queries**:
```bash
# ORM queries
Grep: "\.find|\.findOne|\.create|\.update|\.delete" (output_mode: content)

# SQL
Grep: "SELECT.*FROM|INSERT INTO|UPDATE.*SET" (output_mode: content)
```

**Error handling**:
```bash
# Try-catch blocks
Grep: "try \{|catch \(" (output_mode: content)

# Error throwing
Grep: "throw new \w+Error" (output_mode: content)
```

**Configuration**:
```bash
# Environment variables
Grep: "process\.env\.|os\.getenv" (output_mode: content)

# Config access
Grep: "config\.|configuration\." (output_mode: content)
```

### Advanced Grep Techniques

#### 1. Using Output Modes

**files_with_matches** (default) - Just file paths:
```bash
# Use when you want to know WHERE something exists
Grep: "UserService" (output_mode: files_with_matches)
→ Quick overview of affected files
```

**content** - Show matching lines:
```bash
# Use when you want to see HOW it's used
Grep: "UserService" (output_mode: content)
→ See actual code with context
```

**count** - Count matches:
```bash
# Use when you want to know HOW MUCH
Grep: "TODO" (output_mode: count)
→ See files with most TODOs
```

#### 2. Using Context Flags

**-A (After)** - Show lines after match:
```bash
# See what comes after function definition
Grep: "function getUserById" (output_mode: content, -A: 5)
→ See function body start
```

**-B (Before)** - Show lines before match:
```bash
# See decorators/comments before function
Grep: "async create\(" (output_mode: content, -B: 3)
→ See decorators like @Post, @UseGuards
```

**-C (Context)** - Show lines before AND after:
```bash
# See full context around match
Grep: "validateUser" (output_mode: content, -C: 5)
→ See 5 lines before and after
```

#### 3. Using head_limit

**Sampling large result sets**:
```bash
# See pattern without overwhelming results
Grep: "function \w+" (output_mode: content, head_limit: 20)
→ See first 20 matches to understand pattern

# Find most common pattern
Grep: "\.map\(|\.filter\(|\.reduce\(" (output_mode: content, head_limit: 50)
→ Sample functional programming usage
```

**Progressive refinement**:
```bash
# Step 1: See what's there
Grep: "user" (output_mode: files_with_matches, head_limit: 20)

# Step 2: Refine search
Grep: "class.*User" (output_mode: content, head_limit: 10)

# Step 3: Specific search
Grep: "class User extends" (output_mode: content)
```

#### 4. Case Sensitivity

**Case-insensitive** (-i flag):
```bash
# Find all variations
Grep: "error" -i (output_mode: files_with_matches)
→ Matches: error, Error, ERROR, eRRor

# Use for: Exploratory searches, finding all references
```

**Case-sensitive** (default):
```bash
# Find exact matches
Grep: "User" (output_mode: files_with_matches)
→ Only matches: User (not user, USER)

# Use for: Finding specific classes, types
```

#### 5. Filtering with Glob and Type

**Glob parameter** - Limit to specific files:
```bash
# Search only in TypeScript files
Grep: "interface" (glob: "*.ts", output_mode: content)

# Search in specific directory pattern
Grep: "UserService" (glob: "**/*service*.ts", output_mode: content)
```

**Type parameter** - Limit to file types:
```bash
# Search only JavaScript/TypeScript
Grep: "useState" (type: "js", output_mode: content)

# Search only Python
Grep: "def " (type: "py", output_mode: content)
```

#### 6. Multiline Patterns

**Enable multiline** for patterns spanning lines:
```bash
# Find multi-line patterns
Grep: "interface User \\{[\\s\\S]*?\\}" (multiline: true, output_mode: content)

# Find function with specific body pattern
Grep: "function create[\\s\\S]*?return" (multiline: true, output_mode: content)

# Note: Use sparingly - multiline searches are slower
```

### Grep Best Practices

**Do's**:
1. **Start broad, then narrow**:
   - First: `Grep: "user"` (find all)
   - Then: `Grep: "class User"` (narrow)
   - Finally: `Grep: "class User extends"` (specific)

2. **Use head_limit for sampling**:
   - Large result sets? Sample first with head_limit: 20
   - Understand pattern before full search

3. **Use appropriate output_mode**:
   - Discovery: `files_with_matches`
   - Analysis: `content`
   - Metrics: `count`

4. **Use word boundaries** (\b):
   - `Grep: "\buser\b"` matches "user"
   - Doesn't match "username", "userService"

5. **Escape special regex characters**:
   - Dot: `\.` not `.`
   - Parentheses: `\(` `\)` not `(` `)`
   - Brackets: `\[` `\]` not `[` `]`

**Don'ts**:
1. **Don't search everything**: Use glob/type to limit scope
2. **Don't ignore case unnecessarily**: Be intentional with -i
3. **Don't use multiline by default**: Slower, use only when needed
4. **Don't forget to escape**: `user.service` won't match `user_service`
5. **Don't over-specify too early**: Start broad, refine progressively

---

## Glob Strategies

### File Pattern Discovery

#### 1. Finding All Files of Type

```bash
# All TypeScript files
Glob: "**/*.ts"

# All Python files
Glob: "**/*.py"

# All test files
Glob: "**/*.test.ts"
Glob: "**/test_*.py"

# All component files (React)
Glob: "**/*.tsx"
Glob: "**/*.component.tsx"
```

#### 2. Finding Files by Name Pattern

```bash
# All service files
Glob: "**/*service*"
Glob: "**/*.service.ts"

# All controller files
Glob: "**/*controller*"

# All model files
Glob: "**/models/*.ts"
Glob: "**/*model*.py"

# All config files
Glob: "**/*config*"
Glob: "**/config/*.ts"
```

#### 3. Finding Files in Specific Directories

```bash
# All files in src/users/
Glob: "src/users/*"

# All TypeScript files in services/
Glob: "src/services/*.ts"

# All files in any __tests__ directory
Glob: "**/__tests__/*"
```

#### 4. Complex Patterns

```bash
# Multiple extensions
Glob: "**/*.{ts,tsx,js,jsx}"

# Specific naming patterns
Glob: "**/*.{service,controller,repository}.ts"

# Exclude patterns (not directly supported - use path parameter)
# Instead: Use path to limit scope
Glob: "**/*.ts" (path: "src/")
```

### Glob Use Cases

**1. Discovering file organization**:
```bash
# Count services
Glob: "**/*service*.ts"
→ 47 matches indicates service-oriented architecture

# Find test organization
Glob: "**/*.test.ts"
Glob: "**/tests/**/*.ts"
→ Understand if tests are co-located or separate
```

**2. Finding examples**:
```bash
# Find service examples to understand pattern
Glob: "**/*service*.ts"
→ Read 2-3 to understand service pattern
```

**3. Identifying naming conventions**:
```bash
# Check file naming
Glob: "**/*.ts" (path: "src/services/")
→ See if kebab-case, PascalCase, snake_case
```

**4. Assessing codebase size**:
```bash
# Production code
Glob: "src/**/*.ts"

# Tests
Glob: "**/*.test.ts"

# Ratio reveals test coverage approach
```

### Glob Best Practices

**Do's**:
1. **Use ** for recursive search**: `**/*.ts` searches all subdirectories
2. **Combine with Read**: Glob to find, Read to understand
3. **Use for counting**: Quick metric on file organization
4. **Use for discovery**: Find files before Grep searching

**Don'ts**:
1. **Don't use for content search**: Use Grep instead
2. **Don't glob too broadly**: `**/*` can be overwhelming
3. **Don't forget path parameter**: Limit scope when possible

---

## Read Strategies

### Reading Order

#### 1. Documentation First

```markdown
Priority order for new project:
1. README.md - Project overview
2. CLAUDE.md or CONTRIBUTING.md - Development guide
3. docs/architecture/* - Architecture docs
4. package.json / pyproject.toml - Dependencies
5. Code files
```

#### 2. Code Reading Order

**For feature understanding**:
```markdown
1. Model/Entity (data structure)
2. Repository (data access)
3. Service (business logic)
4. Controller (API)
5. Tests (contracts and examples)
```

**For architecture understanding**:
```markdown
1. Entry point (main.ts, app.py)
2. Module/App configuration
3. Core models
4. Example service
5. Example controller
```

### Read Techniques

#### 1. Targeted Reading

**Read with purpose**:
```markdown
Before reading:
1. Know WHAT you're looking for
2. Know WHY you need it
3. Have specific questions

While reading:
1. Skip irrelevant sections
2. Focus on structure, not every line
3. Note patterns, not details
4. Document findings immediately
```

**Example**:
```markdown
Goal: Understand user authentication
Questions:
- How are passwords stored?
- What authentication method (JWT, session)?
- Where is auth middleware?

Read:
1. src/auth/auth.service.ts
   Focus: login method, token generation
   Skip: Unrelated helper methods

2. src/auth/jwt.strategy.ts
   Focus: Token validation approach
   Skip: Implementation details

Document:
- Uses JWT with 1-hour expiry
- Passwords hashed with bcrypt
- JWT strategy validates via UserService
```

#### 2. Comparative Reading

**Read multiple similar files**:
```markdown
Pattern: Read 2-3 examples to understand pattern

Example - Understanding service pattern:
1. Read: user.service.ts
2. Read: product.service.ts
3. Read: order.service.ts

Compare:
- All use dependency injection
- All have create, update, delete methods
- All delegate to repository
- All handle business logic

Document pattern for reuse
```

#### 3. Skimming vs Deep Reading

**Skim** (quick overview):
```markdown
Look for:
- Imports (dependencies)
- Class/function names (structure)
- Comments (high-level purpose)
- Public methods (API surface)

Skip:
- Implementation details
- Private methods
- Complex algorithms
```

**Deep read** (full understanding):
```markdown
Read:
- Every line
- Implementation logic
- Edge cases
- Error handling
- Comments explaining "why"

When:
- Understanding critical business logic
- Debugging specific issue
- Planning to modify this code
```

### Read Best Practices

**Do's**:
1. **Read docs before code**: Context helps understanding
2. **Read tests**: They reveal contracts and usage
3. **Read in logical order**: Follow dependency chains
4. **Take notes**: Don't rely on memory
5. **Read selectively**: Not every file needs deep reading

**Don'ts**:
1. **Don't read sequentially**: Prioritize important files
2. **Don't read without purpose**: Know what you're looking for
3. **Don't read everything**: Focus on relevant areas
4. **Don't skip tests**: They're documentation
5. **Don't trust comments**: Verify with code

---

## Bash (ls) Strategies

### Directory Structure Analysis

#### 1. Basic Listing

```bash
# List top-level
ls <project-root>
→ See main directories and files

# List with details
ls -la <project-root>
→ See permissions, sizes, dates

# List only directories
ls -d <project-root>/*/
→ See subdirectories only
```

#### 2. Structure Mapping

**Efficient directory mapping**:
```bash
# Phase 1: Top level
ls src/

# Phase 2: Second level
ls src/users/
ls src/products/
ls src/auth/

# Phase 3: Third level (if needed)
ls src/users/services/
ls src/users/models/
```

**Don't use**:
```bash
# SLOW - Don't use
find . -type d

# Use simple ls instead
ls -R (also slow for large trees)
```

#### 3. Quick Counts

```bash
# Count files in directory
ls src/services/ | wc -l

# Count subdirectories
ls -d src/*/ | wc -l
```

### Bash Best Practices

**Do's**:
1. **Use for structure understanding**: Quick directory overview
2. **Use ls -d */ for subdirectories**: Better than find
3. **Batch ls commands**: Run multiple in parallel
4. **Use relative paths in docs**: From project root

**Don'ts**:
1. **Don't use find**: ls is faster and simpler
2. **Don't use tree**: Not always available
3. **Don't list excluded dirs**: Skip node_modules, .venv, etc.

---

## Search Workflows

### Common Research Scenarios

#### 1. Understanding a New Codebase

```markdown
Step 1: Documentation
- Read: README.md
- Read: CONTRIBUTING.md
- Read: docs/architecture/

Step 2: Structure
- ls: src/
- ls: src/*/
- Glob: "**/*.ts" (count files)

Step 3: Patterns
- Grep: "class \w+Service" (find services, head_limit: 10)
- Read: 2-3 example services
- Grep: "interface \w+" (find interfaces, head_limit: 10)

Step 4: Entry Points
- Read: src/main.ts or src/app.py
- Read: package.json (scripts)
```

#### 2. Finding Similar Features

```markdown
Step 1: Search by domain term
- Grep: "upload" -i (output_mode: files_with_matches)

Step 2: Narrow to relevant files
- Grep: "upload" (glob: "**/*service*.ts", output_mode: content)

Step 3: Read examples
- Read: src/services/file-upload.service.ts
- Read: src/controllers/upload.controller.ts

Step 4: Document pattern
- How is upload handled?
- What validation exists?
- How is storage managed?
```

#### 3. Impact Analysis for Changes

```markdown
Step 1: Find direct usage
- Grep: "import.*UserService" (output_mode: files_with_matches)

Step 2: Find method calls
- Grep: "userService\." (output_mode: content)

Step 3: Find tests
- Glob: "**/*user*.test.ts"
- Read: Representative tests

Step 4: Document impact
- X files import UserService
- Y methods call it
- Z tests cover it
```

#### 4. Discovering Conventions

```markdown
Step 1: Find examples
- Glob: "**/*service*.ts"

Step 2: Sample
- Read: 3 different services

Step 3: Find patterns
- Grep: "constructor\(" (glob: "**/*service*.ts", output_mode: content, head_limit: 10)

Step 4: Document conventions
- Naming: PascalCase + "Service" suffix
- DI: Constructor injection
- Methods: CRUD + business logic
```

---

## Optimization Techniques

### 1. Progressive Refinement

Start broad, narrow progressively:

```markdown
Round 1 (Broad):
Grep: "user" -i (output_mode: files_with_matches)
→ 200 files

Round 2 (Narrow):
Grep: "class.*User" (output_mode: files_with_matches)
→ 45 files

Round 3 (Specific):
Grep: "class User extends" (output_mode: content)
→ 3 relevant matches
```

### 2. Sampling with head_limit

Don't overwhelm with results:

```markdown
First: Sample
Grep: "function" (output_mode: content, head_limit: 20)
→ See pattern

Then: Full search if needed
Grep: "function create" (output_mode: content)
→ Find all create functions
```

### 3. Combining Tools

Use tools together:

```markdown
Glob → Find files
Read → Understand pattern
Grep → Find all usages

Example:
1. Glob: "**/*service*.ts"
   → Find all services

2. Read: user.service.ts
   → Understand service pattern

3. Grep: "extends.*Service" (output_mode: content)
   → Find service inheritance pattern
```

### 4. Scope Limiting

Limit search scope:

```markdown
# Limit by path
Grep: "UserService" (path: "src/controllers/", output_mode: content)

# Limit by glob
Grep: "validate" (glob: "**/*.dto.ts", output_mode: content)

# Limit by type
Grep: "class" (type: "py", output_mode: content)
```

---

## Common Search Patterns

### Pattern Library

**Find all services**:
```bash
Glob: "**/*service*.ts"
Grep: "class \w+Service" (output_mode: content)
```

**Find all controllers**:
```bash
Glob: "**/*controller*.ts"
Grep: "@Controller|class \w+Controller" (output_mode: content)
```

**Find all models/entities**:
```bash
Glob: "**/models/*.ts"
Grep: "@Entity|class \w+ extends Model" (output_mode: content)
```

**Find all API endpoints**:
```bash
Grep: "@Get|@Post|@Put|@Delete" (output_mode: content)
Grep: "router\.(get|post|put|delete)" (output_mode: content)
```

**Find all tests**:
```bash
Glob: "**/*.test.ts"
Glob: "**/test_*.py"
```

**Find configuration**:
```bash
Grep: "process\.env\." (output_mode: content)
Read: .env.example
```

**Find TODO/FIXME**:
```bash
Grep: "TODO|FIXME" (output_mode: content)
```

---

## Summary

Effective searching requires:
1. **Right tool** - Grep for content, Glob for files, Read for understanding, ls for structure
2. **Progressive refinement** - Broad to narrow
3. **Sampling** - Use head_limit to avoid overwhelming results
4. **Scope limiting** - Use path, glob, type parameters
5. **Tool combination** - Use multiple tools together
6. **Purpose** - Always search with clear goal

Master these strategies and codebase navigation becomes fast and efficient.
