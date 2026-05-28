# Integration with Other Tools

Guide to combining semantic search with other Claude Code tools for powerful workflows.

## Tool Integration Matrix

| Tool | Purpose | When to Use After Semantic Search |
|------|---------|-----------------------------------|
| **code-pointer** | Open files at specific lines | When you want to view/edit found code |
| **grep** | Exact text matching | To find specific strings in sem-search results |
| **glob** | File pattern matching | To filter results by file type/location |
| **read** | Read file contents | To examine top semantic search results |

## Semantic Search → Code-Pointer

**Use case:** Open relevant files in VSCode after semantic search

### Basic Pattern

```bash
# 1. Find relevant code with semantic search
RESULTS=$(odino query -q "authentication middleware")

# Example output:
# Score: 0.89 | Path: src/middleware/auth.js
# Score: 0.82 | Path: src/middleware/jwt.js

# 2. Open top result in VSCode
code -g src/middleware/auth.js
```

### With Line Numbers

When you know the specific section:

```bash
# Find the file
odino query -q "JWT token generation"
# → src/auth/jwt.js

# Read the file to find exact line
grep -n "generateToken" src/auth/jwt.js
# → 42:function generateToken(user) {

# Open at specific line
code -g src/auth/jwt.js:42
```

### Automated Workflow

```bash
# Parse top result and open automatically
TOP_FILE=$(odino query -q "password hashing" | head -1 | cut -d'|' -f2 | xargs)
code -g "$TOP_FILE"
```

## Semantic Search → Grep

**Use case:** Find exact text in files discovered by semantic search

### Two-Stage Search

```bash
# Stage 1: Find relevant area with semantic search
odino query -q "database connection handling"
# → Found: src/db/connection.js, src/db/pool.js

# Stage 2: Find exact string in those files
grep -n "createConnection\|getConnection" src/db/*.js
```

### Narrowing Results

```bash
# Broad semantic search
odino query -q "API endpoints"
# → Returns 20+ files

# Narrow to specific endpoint with grep
grep -r "app.post('/users')" .
```

### Finding Patterns

```bash
# Find error handling code
odino query -q "error handling patterns"
# → src/middleware/error.js, src/utils/errors.js

# Find specific error types
grep -r "try.*catch\|throw new" src/middleware/error.js src/utils/errors.js
```

## Semantic Search → Glob

**Use case:** Filter semantic search results by file patterns

### File Type Filtering

```bash
# Find configuration code
odino query -q "application configuration"
# → Might return .js, .json, .yaml files

# Focus on just config files
find . -name "*.config.js" -o -name "config.json"
```

### Directory-Specific Search

```bash
# Find test files related to authentication
odino query -q "authentication testing"

# Then narrow to test directory
ls tests/**/*auth*.test.js
```

## Semantic Search → Read

**Use case:** Examine top results to understand context

### Standard Workflow

```bash
# 1. Semantic search
odino query -q "user registration logic"
# → Top 3 results:
#    Score: 0.91 | Path: src/routes/auth.js
#    Score: 0.85 | Path: src/services/user.js
#    Score: 0.79 | Path: src/validators/user.js

# 2. Read top result
cat src/routes/auth.js

# 3. Read related files for full context
cat src/services/user.js
cat src/validators/user.js
```

### With Summary

```bash
# Find relevant code
odino query -q "payment processing"

# Read top results and summarize
echo "## Payment Processing Implementation"
echo ""
echo "### Main handler:"
head -20 src/routes/payment.js
echo ""
echo "### Service layer:"
head -20 src/services/payment.js
```

## Complete Workflow Examples

### Example 1: Debugging a Feature

**Goal:** Fix bug in user login

```bash
# 1. Find login code with semantic search
odino query -q "user login authentication"
# → src/routes/auth.js (0.92)
# → src/services/auth.js (0.88)
# → src/middleware/passport.js (0.81)

# 2. Read main login handler
cat src/routes/auth.js | grep -A 20 "post.*login"

# 3. Find error handling in that file
grep -n "catch\|error" src/routes/auth.js

# 4. Open at error handling line
code -g src/routes/auth.js:67
```

### Example 2: Understanding a Feature

**Goal:** Understand how caching works

```bash
# 1. Find caching implementation
odino query -q "caching implementation and configuration"
# → src/cache/redis.js (0.94)
# → src/config/cache.js (0.87)
# → src/middleware/cache.js (0.79)

# 2. Read configuration first
cat src/config/cache.js

# 3. Then read main implementation
cat src/cache/redis.js

# 4. Find usage examples
grep -r "cache.get\|cache.set" src/ | head -10

# 5. Open implementation in editor
code -g src/cache/redis.js
```

### Example 3: Refactoring

**Goal:** Replace all database connection code

```bash
# 1. Find all database connection code
odino query -q "database connection creation and management"
# → Returns 5 files

# 2. Find exact connection creation calls
grep -rn "createConnection\|mysql.connect\|pg.Pool" src/

# 3. Check each file with semantic context
odino query -q "connection pooling"
odino query -q "database transaction handling"

# 4. Open files for editing
code -g src/db/connection.js src/db/pool.js src/db/transaction.js
```

### Example 4: Code Review

**Goal:** Review all authentication changes

```bash
# 1. Find authentication code
odino query -q "authentication and authorization logic"

# 2. Find recent changes (combine with git)
git diff main -- src/auth/ src/middleware/auth.js

# 3. Semantic search for related security code
odino query -q "security validation and sanitization"

# 4. Check for vulnerabilities
grep -r "eval\|exec\|innerHTML" src/auth/
```

## Advanced Integration Patterns

### Cascading Search

Start broad, narrow progressively:

```bash
# Level 1: Semantic search (broad)
odino query -q "user management"
# → 15 files

# Level 2: File pattern (medium)
find src/ -path "*/users/*" -name "*.js"
# → 8 files

# Level 3: Grep (narrow)
grep -l "updateUser\|deleteUser" src/users/*.js
# → 3 files

# Level 4: Open specific files
code -g src/users/controller.js src/users/service.js
```

### Context Building

Build understanding layer by layer:

```bash
# 1. High-level architecture
odino query -q "application architecture and structure"

# 2. Specific subsystem
odino query -q "data access layer implementation"

# 3. Specific functionality
odino query -q "CRUD operations for users"

# 4. Exact implementation
grep -A 30 "function createUser" src/data/users.js
```

### Verification Workflow

Verify semantic search results:

```bash
# 1. Semantic search
odino query -q "input validation"
# → src/validators/user.js (0.87)

# 2. Verify by reading
cat src/validators/user.js | head -50

# 3. Find all validation usage
grep -r "import.*validator" src/

# 4. Cross-reference with tests
odino query -q "validation testing"
```

## When to Use Each Tool

### Use semantic search when:
- Exploring unfamiliar codebase
- Finding conceptual implementations
- Locating cross-cutting concerns
- Understanding feature architecture

### Use grep when:
- Searching for exact strings
- Finding variable/function usages
- Locating error messages
- Searching for TODOs/FIXMEs

### Use glob when:
- Finding files by name pattern
- Filtering by file type
- Working with specific directories
- Batch operations on matching files

### Use code-pointer when:
- Need to view/edit specific code
- Opening files at exact lines
- Navigating to definitions
- Debugging specific sections

### Use read when:
- Examining file contents
- Understanding context
- Checking configuration
- Reviewing small files

## Tool Selection Decision Tree

```
Need to find code?
├─ Know exact string? → Use grep
├─ Know filename pattern? → Use glob
├─ Know file path? → Use read
└─ Know concept only? → Use semantic search
   └─ Got results? → Use code-pointer to open
      └─ Need exact line? → Use grep in file
```

## Best Practices

1. **Start semantic, end specific**
   - Semantic search → Find area
   - Grep → Find exact code
   - Code-pointer → Open for editing

2. **Read before editing**
   - Semantic search → Find files
   - Read → Understand context
   - Code-pointer → Open in editor

3. **Verify with multiple tools**
   - Semantic search → Find candidates
   - Grep → Verify it's the right code
   - Read → Confirm implementation

4. **Build context progressively**
   - Semantic search → High-level structure
   - Semantic search → Specific subsystem
   - Read/Grep → Detailed implementation

5. **Combine for complex tasks**
   - Semantic search → Find authentication
   - Grep → Find specific function
   - Code-pointer → Open file
   - Read → Check related files

## Performance Tips

1. **Cache semantic results**
   - Run semantic search once
   - Use results for multiple grep/read operations

2. **Narrow scope early**
   - Use semantic search to identify directory
   - Then use grep/glob only in that directory

3. **Batch file operations**
   - Collect file paths from semantic search
   - Read multiple files in one pass

4. **Use appropriate tool**
   - Don't use semantic search for exact strings
   - Don't use grep for conceptual searches

## Common Mistakes to Avoid

**❌ Using semantic search for exact matches:**
```bash
# Wrong
odino query -q "function validateEmail"

# Right
grep -r "function validateEmail" .
```

**❌ Using grep for concepts:**
```bash
# Wrong (might miss variations)
grep -r "auth" .

# Right
odino query -q "authentication implementation"
```

**❌ Not reading semantic results:**
```bash
# Wrong (blindly trusting results)
odino query -q "payment" | head -1 | cut -d'|' -f2

# Right (verify first)
odino query -q "payment"
cat [top-result]  # Verify it's actually payment code
```

**❌ Opening too many files:**
```bash
# Wrong
odino query -q "validation" | while read line; do
    code -g "$(echo $line | cut -d'|' -f2)"
done  # Opens 20+ files

# Right
odino query -q "validation" | head -3
# Review, then open specific files
code -g src/validators/user.js
```

## Summary

**Effective integration means:**
- Using the right tool for each task
- Starting broad (semantic) and narrowing (grep)
- Verifying results before acting
- Building context progressively
- Combining tools for complex workflows

**Remember:**
- Semantic search → Finding concepts
- Grep → Finding exact text
- Glob → Finding files
- Read → Understanding context
- Code-pointer → Editing code
