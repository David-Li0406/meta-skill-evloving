# Effective Semantic Search Patterns

Guide to crafting effective semantic search queries and interpreting results.

## Query Design Principles

### Be Conceptual, Not Literal

Semantic search works best with conceptual queries that describe **what the code does**, not what it's named.

**❌ Poor queries (too literal):**
- "validateEmail" → Use grep instead
- "config.js" → Use glob instead
- "class AuthService" → Use grep instead
- "TODO" → Use grep instead

**✅ Good queries (conceptual):**
- "email validation logic"
- "configuration loading and parsing"
- "authentication service implementation"
- "incomplete features or pending work"

### Use Natural Language

Write queries as you would explain the concept to a colleague.

**❌ Keyword stuffing:**
- "db connect pool config"

**✅ Natural language:**
- "database connection pooling configuration"

### Be Specific When Needed

Balance specificity with generality based on what you're looking for.

**Too general:**
- "functions" → Will match everything
- "code" → Will match everything

**Too specific:**
- "JWT token validation using bcrypt with salt rounds set to 10" → Too narrow

**Just right:**
- "JWT token validation"
- "password hashing and verification"

## Common Query Patterns

### Finding Implementation

**Pattern:** "[concept] implementation" or "how [feature] works"

```bash
odino query -q "authentication implementation"
odino query -q "how caching works"
odino query -q "error handling implementation"
```

### Finding Configuration

**Pattern:** "[system/feature] configuration" or "[thing] setup"

```bash
odino query -q "database configuration"
odino query -q "API endpoint setup"
odino query -q "logging configuration"
```

### Finding Patterns

**Pattern:** "[pattern/technique] usage" or "examples of [pattern]"

```bash
odino query -q "middleware usage patterns"
odino query -q "dependency injection examples"
odino query -q "async/await error handling"
```

### Finding by Purpose

**Pattern:** "code that [does something]" or "[action] logic"

```bash
odino query -q "code that validates user input"
odino query -q "file upload logic"
odino query -q "payment processing"
```

### Finding Documentation

**Pattern:** "[topic] documentation" or "how to [task]"

```bash
odino query -q "API documentation"
odino query -q "how to deploy the application"
odino query -q "setup instructions"
```

## Result Interpretation

### Understanding Scores

Odino returns results with similarity scores (0.0 to 1.0):

- **0.85-1.0**: Highly relevant, almost certainly what you're looking for
- **0.70-0.84**: Likely relevant, worth checking
- **0.60-0.69**: Possibly relevant, may contain related concepts
- **<0.60**: Weakly related, probably not useful

**Example output:**
```
Score: 0.92 | Path: src/auth/jwt.js          # Definitely check this
Score: 0.78 | Path: src/middleware/auth.js   # Likely relevant
Score: 0.64 | Path: src/utils/crypto.js      # Maybe related
Score: 0.51 | Path: src/config/index.js      # Probably not it
```

### When to Read Files

**Always read:** Top 1-2 results (score > 0.80)
**Sometimes read:** Next 2-3 results (score 0.65-0.80) for context
**Rarely read:** Results with score < 0.65

### Combining Results

Often the answer spans multiple files:

```bash
odino query -q "user authentication flow"

# Results might include:
# - Login endpoint (score: 0.89)
# - JWT generation (score: 0.85)
# - Password verification (score: 0.82)
# - Session management (score: 0.76)
```

Read top results to understand the complete picture.

## Refinement Strategies

### Too Many Results

Make query more specific:

```bash
# Too broad
odino query -q "validation"

# Better
odino query -q "email format validation"
```

### Too Few Results

Make query more general:

```bash
# Too narrow
odino query -q "SHA256 password hashing with bcrypt"

# Better
odino query -q "password hashing"
```

### Wrong Results

Try different phrasing:

```bash
# If "API endpoint handlers" doesn't work well
odino query -q "route definitions"
odino query -q "HTTP request handlers"
odino query -q "REST API implementation"
```

## Advanced Patterns

### Multi-Concept Queries

Combine related concepts for broader coverage:

```bash
odino query -q "authentication and authorization logic"
odino query -q "database queries and ORM usage"
odino query -q "error handling and logging"
```

### Feature-Specific Queries

Target specific features or subsystems:

```bash
odino query -q "user registration feature"
odino query -q "shopping cart functionality"
odino query -q "notification system"
```

### Cross-Cutting Concerns

Find patterns that span the codebase:

```bash
odino query -q "error handling patterns"
odino query -q "input validation across endpoints"
odino query -q "database transaction usage"
```

## Query Examples by Use Case

### Code Exploration

"I'm new to this codebase, where do I start?"

```bash
odino query -q "main application entry point"
odino query -q "core business logic"
odino query -q "primary data models"
```

### Bug Hunting

"There's a bug in feature X, where's the code?"

```bash
odino query -q "user login functionality"
odino query -q "payment processing logic"
odino query -q "email sending implementation"
```

### Refactoring

"I need to change how we do X across the codebase"

```bash
odino query -q "database connection creation"
odino query -q "API key validation"
odino query -q "date formatting and parsing"
```

### Learning Patterns

"How does this codebase handle X?"

```bash
odino query -q "dependency injection patterns"
odino query -q "testing approach and examples"
odino query -q "configuration management"
```

## When Semantic Search Doesn't Help

Use other tools when:

1. **Exact string needed** - Use `grep`
   ```bash
   grep -r "validateEmail" .
   ```

2. **Filename patterns** - Use `glob` or `find`
   ```bash
   find . -name "*config*.js"
   ```

3. **Known file location** - Use `read` directly
   ```bash
   # Just read the file
   cat src/config/database.js
   ```

4. **Symbol definitions** - Use language-specific tools
   ```bash
   # For Python
   grep -r "class AuthService" .

   # For JavaScript
   grep -r "export.*AuthService" .
   ```

## Combining Tools Workflow

**Best practice:** Start semantic, narrow with grep/glob

```bash
# 1. Find the general area with semantic search
odino query -q "database migrations"
# → Found: migrations/2024-01-15-add-users.sql

# 2. Narrow to specific files/patterns
find migrations/ -name "*users*"

# 3. Search for exact strings in those files
grep -n "CREATE TABLE" migrations/*users*.sql
```

## Tips for Better Results

1. **Use verbs and nouns** - "validates user input" not just "validation"
2. **Include context** - "email validation in registration" not just "email"
3. **Think about purpose** - What does the code **do**, not what it's **called**
4. **Try synonyms** - "authentication" vs "login" vs "sign in"
5. **Be patient** - Try 2-3 query variations if first doesn't work
6. **Check top 3-5 results** - Sometimes #3 is the best match
7. **Combine with file reading** - Read top results to confirm relevance

## Anti-Patterns to Avoid

**❌ Searching for variable names:**
```bash
odino query -q "userEmail" # Use grep instead
```

**❌ Searching for exact error messages:**
```bash
odino query -q "Error: Connection refused" # Use grep instead
```

**❌ Searching for file paths:**
```bash
odino query -q "src/utils/validation.js" # Use find/glob instead
```

**❌ Searching for TODOs/comments:**
```bash
odino query -q "TODO fix this" # Use grep instead
```

**❌ Overly generic queries:**
```bash
odino query -q "code" # Way too broad
```

## Summary

**Good semantic queries are:**
- Conceptual, not literal
- Natural language, not keywords
- Focused on purpose/behavior
- Appropriately specific

**After getting results:**
- Check scores (> 0.70 is good)
- Read top 2-3 files for context
- Combine with grep/glob for precision
- Iterate query if needed
