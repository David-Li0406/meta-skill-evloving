---
name: prompt-optimizer
description: Optimize Claude prompts for clarity and effectiveness. Use when creating, refining, or reviewing commands, agents, skills, or system prompts.
---

# Prompt Optimizer Skill

**Activation:** prompt engineering, improve prompt, refine prompt, command creation, agent instruction, skill writing, optimize instructions

## Overview

Optimize prompts for Claude to ensure clarity, effectiveness, and consistent behavior. Use when writing skills, commands, agent instructions, or any system prompts.

## Core Principles

### 1. Be Specific and Actionable

```markdown
# BAD - Vague
Consider using eager loading for better performance.

# GOOD - Specific
Use `selectinload()` to eager-load relationships:
```python
stmt = select(User).options(selectinload(User.posts))
```
```

### 2. Show, Don't Tell

```markdown
# BAD - Abstract
Handle errors appropriately.

# GOOD - Concrete example
Catch specific exceptions and return structured errors:
```python
try:
    result = await service.process(data)
except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))
except NotFoundError:
    raise HTTPException(status_code=404, detail="Resource not found")
```
```

### 3. Structure for Scanning

```markdown
# BAD - Wall of text
When implementing authentication you should first check if the user is logged in and then verify their permissions and finally return the appropriate response based on their access level.

# GOOD - Structured
## Authentication Flow

1. **Check login status** - Verify session/token exists
2. **Verify permissions** - Check user role against required permission
3. **Return response** - Success or 403 Forbidden
```

### 4. Provide Context Before Instructions

```markdown
# BAD - Instructions without context
Always use Docker for commands.

# GOOD - Context then instruction
> **Container-First Execution**
>
> This project requires all dev commands in Docker to ensure consistent
> Node/Python versions. Host may have incompatible tooling.
>
> ```bash
> # WRONG - will fail with Volta error
> pnpm lint
>
> # RIGHT - use Docker
> docker compose exec frontend pnpm lint
> ```
```

## Anti-Patterns to Avoid

### 1. Ambiguous Instructions

| Bad | Good |
|-----|------|
| "Use appropriate error handling" | "Raise HTTPException with status 404 for not found" |
| "Consider performance" | "Add index on `user_id` column for O(1) lookup" |
| "Follow best practices" | "Use `async with session.begin():` for transactions" |

### 2. Missing Escape Hatches

```markdown
# BAD - No escape
Never mock any services.

# GOOD - With exception
Never mock internal services. **Exception:** Mock external network APIs
(Tone3000, email) to avoid rate limits and flakiness.
```

### 3. Buried Critical Information

```markdown
# BAD - Critical info at end of paragraph
This skill helps with testing. It covers unit tests, integration tests,
and various patterns. Tests run in Docker containers only.

# GOOD - Critical info upfront
> **CRITICAL: Container-First Execution**
> All tests run in Docker. Never run `pytest` directly on host.
```

### 4. Over-Explanation

```markdown
# BAD - Too verbose
In order to create a new test file, you should navigate to the tests
directory and then create a new Python file with a name that starts
with test_ followed by the name of the module you are testing, for
example if you are testing the user module you would create a file
called test_user.py.

# GOOD - Concise
Create test file: `tests/unit/backend/test_{module}.py`
```

### 5. No Examples

```markdown
# BAD - Abstract only
Use Pydantic for validation.

# GOOD - With example
Use Pydantic for validation:
```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
```
```

## Before/After Optimization Examples

### Example 1: Skill Activation

**Before:**
```markdown
This skill is for frontend development.
```

**After:**
```markdown
**Activation:** Jinja2, HTMX, Alpine.js, Tailwind, template, page, UI, frontend
```

### Example 2: Command Documentation

**Before:**
```markdown
You can run tests with pytest.
```

**After:**
```markdown
## Running Tests

| Test Type | Command |
|-----------|---------|
| Unit | `docker compose exec backend pytest /tests/unit/backend/` |
| Integration | `docker compose exec backend pytest /tests/integration/backend/` |
| Smoke (fast) | `docker compose exec backend pytest -m smoke` |
```

### Example 3: Error Handling

**Before:**
```markdown
Make sure to handle errors properly in your code.
```

**After:**
```markdown
## Error Handling

```python
@router.get("/{id}")
async def get_item(id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(Item, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {id} not found"
        )
    return item
```
```

### Example 4: Workflow Instructions

**Before:**
```markdown
Create a PR when you're done with your changes.
```

**After:**
```markdown
## Creating Pull Requests

1. Run quality gates: `just check`
2. Push changes: `git push`
3. Create PR:
   ```bash
   gh pr create --repo krazyuniks/guitar-tone-shootout \
     --title "feat: Add user profile page" \
     --body "## Summary\n- Added profile page\n- Integrated with auth"
   ```
```

## Prompt Review Checklist

- [ ] **Frontmatter complete** - name, description with trigger keywords
- [ ] **Activation triggers** - Keywords users would actually say
- [ ] **Critical info upfront** - Warnings/requirements in callout boxes
- [ ] **Examples are complete** - Copy-paste ready, not pseudocode
- [ ] **Progressive disclosure** - Quick patterns in main, deep dives in resources
- [ ] **Tables for reference** - Commands, options, patterns
- [ ] **Escape hatches** - Exceptions documented
- [ ] **Under 500 lines** - Move extras to resources/
- [ ] **No ambiguity** - Specific, actionable instructions
- [ ] **Tested activation** - Verify skill triggers on relevant prompts

## Structural Patterns

### Pattern: Quick Reference Table

```markdown
| You Want To... | Command |
|----------------|---------|
| Run tests | `docker compose exec backend pytest tests/` |
| Lint code | `docker compose exec backend ruff check app/` |
| Create migration | `docker compose exec backend alembic revision -m "..."` |
```

### Pattern: Decision Matrix

```markdown
| Scenario | Approach |
|----------|----------|
| Simple CRUD | Direct repository call |
| Business logic | Service layer |
| Cross-cutting | Middleware/dependency |
```

### Pattern: Code Block with Context

```markdown
### Creating a Service

Services own business logic and transactions:

```python
class ShootoutService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: ShootoutCreate, user_id: int) -> Shootout:
        async with self.db.begin():
            shootout = Shootout(**data.model_dump(), user_id=user_id)
            self.db.add(shootout)
            return shootout
```
```

### Pattern: Warning Callout

```markdown
> **WARNING:** Never commit directly to main. Always use feature branches.
```

### Pattern: Critical Callout

```markdown
> **CRITICAL: No Mocking in E2E Tests**
>
> E2E tests MUST hit real backend. Never use `page.route()` to mock APIs.
```

## Writing Effective Descriptions

The `description` field in frontmatter drives skill activation:

```yaml
# BAD - Too generic
description: Helps with testing.

# GOOD - Specific with trigger words
description: Test development with pytest, fixtures, and integration testing.
Use for writing tests, test patterns, coverage, parametrization, and
debugging test failures.
```

**Include:**
- Technologies/frameworks (pytest, vitest, Playwright)
- Actions users would request (writing tests, debugging)
- Concepts (fixtures, coverage, parametrization)
- Max 1024 characters

## Example Invocations

### Optimize an Existing Skill
```
"Improve the testing skill to be more scannable"
-> Review against checklist
-> Add tables for commands
-> Move verbose sections to resources/
-> Add activation triggers
```

### Write New Skill Instructions
```
"Create instructions for a new database migration skill"
-> Start with frontmatter (name, description)
-> Add activation triggers
-> Include quick reference table
-> Provide complete code examples
-> Add critical callouts for common mistakes
```

### Review Agent Prompt
```
"Review this agent prompt for clarity"
-> Check for ambiguous instructions
-> Verify examples are complete
-> Ensure critical info is visible
-> Add escape hatches for edge cases
```
