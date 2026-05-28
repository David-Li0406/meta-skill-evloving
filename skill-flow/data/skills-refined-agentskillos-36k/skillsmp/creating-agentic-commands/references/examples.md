# Command Examples

Complete, production-ready command configurations with best practices from Claude's agentic coding research.

## Example 1: Testing Command with Full Error Handling

`.opencode/command/test.md`:

```markdown
---
description: Run all tests with coverage, analyze failures, and suggest fixes
agent: build
---

Run the full test suite with coverage:

!`composer test -- --coverage`

Analyze the results carefully:

**If all tests pass:**

- Report success with coverage percentage
- If coverage >= 90%: Confirm quality standards met
- If coverage < 90%: Identify specific files/methods lacking coverage

**If tests fail:**

1. List each failing test with file:line reference
2. For each failure:
   - Show the assertion that failed
   - Identify the likely cause
   - Suggest a specific fix
3. After suggesting fixes, ask: "Should I implement these fixes?"

**If tests cannot run (setup error):**

- Identify the configuration or dependency issue
- Suggest resolution steps
```

## Example 2: Component Generation with Verification

`.opencode/command/component.md`:

````markdown
---
description: Create a new React component with TypeScript and Tailwind
agent: build
---

Create a React component named $ARGUMENTS with these requirements:

**Location:** resources/js/components/$ARGUMENTS.tsx

**Standards:**

1. React 19 function component (no FC type annotation)
2. TypeScript with full type annotations
3. Use `import type` for type-only imports
4. PropsWithChildren if it accepts children
5. Tailwind CSS v4 for all styling
6. JSDoc comment explaining the component purpose

**Structure:**

```tsx
import type { PropsWithChildren } from 'react';

interface ${ARGUMENTS}Props {
  // Define props here
}

/**
 * Brief description of what this component does.
 */
export function $ARGUMENTS({ ...props }: ${ARGUMENTS}Props) {
  return (
    // Component JSX
  );
}
```
````

**After creation:**

1. Verify the file was created at the correct path
2. Run TypeScript compilation to check for errors:
   !`npx tsc --noEmit resources/js/components/$ARGUMENTS.tsx`
3. If errors, fix them before completing
4. Show the complete file
5. Provide a usage example:
   ```tsx
   import { $ARGUMENTS } from '@/components/$ARGUMENTS'
   ```

````

Usage: `/component UserAvatar`

## Example 3: Quality Workflow with Iteration

`.opencode/command/quality.md`:

```markdown
---
description: Run all quality checks iteratively until all pass
agent: build
subtask: true
---

Execute the complete quality workflow. Each step must pass before proceeding.

**Step 1: Rector (Automated Refactoring)**
!`./vendor/bin/rector`
- If changes made: Review and re-run until no more changes
- If errors: Fix each error, then re-run

**Step 2: Pint (Code Formatting)**
!`./vendor/bin/pint`
- This should auto-fix; verify no errors

**Step 3: PHPStan (Static Analysis)**
!`./vendor/bin/phpstan analyse`
- If errors found:
  1. Fix the first error
  2. Re-run PHPStan
  3. Repeat until all errors resolved
  4. Track: "Fixed N PHPStan errors"

**Step 4: Frontend Checks**
!`npm run checks`
- If ESLint errors: Fix each, re-run
- If TypeScript errors: Fix each, re-run
- If Prettier issues: Run `npm run format`

**Step 5: Test Suite**
!`composer test -- --coverage`
- All tests must pass
- Coverage must be >= 90%

**Final Report:**
Summarize in this format:
- Rector: [changes made / clean]
- Pint: [formatted / clean]
- PHPStan: [N errors fixed / clean]
- Frontend: [N issues fixed / clean]
- Tests: [PASS/FAIL] Coverage: X%
- Overall: READY TO COMMIT / NEEDS ATTENTION
````

## Example 4: Filtered Test with Context

`.opencode/command/test-filter.md`:

```markdown
---
description: Run a specific test by name with detailed analysis
agent: build
---

Run the specific test matching: $ARGUMENTS

!`php artisan test --filter="$ARGUMENTS" -v`

**Analyze the results:**

**If test passes:**

- Confirm success
- Show test execution time
- If slow (>1s), suggest optimization

**If test fails:**

1. Show the full error message and stack trace
2. Identify the file and line where failure occurred
3. Read the relevant test file to understand the assertion
4. Check the implementation being tested
5. Explain why it failed
6. Suggest a fix with code example

**If no tests match:**

- List similar test names that exist
- Suggest the correct filter pattern
```

Usage: `/test-filter RegisterUserActionTest`

## Example 5: Intelligent Debug Command

`.opencode/command/debug.md`:

```markdown
---
description: Analyze application state, logs, and recent changes to diagnose issues
agent: build
---

Perform comprehensive debugging analysis:

**1. Check Recent Errors**
!`tail -n 100 storage/logs/laravel.log | grep -A 5 "ERROR\|Exception"`

**2. Recent Code Changes**
!`git log --oneline -5`
!`git diff HEAD~1 --stat`

**3. Current Test Status**
!`php artisan test --stop-on-failure 2>&1 | head -50`

**4. Application State**
!`php artisan about 2>&1 | head -20`

**Analysis:**

Based on the gathered information:

1. **Identify Issues:**
   - List each error/exception found with timestamp
   - Note any failing tests

2. **Correlate with Changes:**
   - Match errors to recent commits if possible
   - Identify if a recent change likely caused the issue

3. **Root Cause Analysis:**
   - Explain the most likely cause
   - Reference specific files and line numbers

4. **Recommended Actions:**
   - List steps to fix, in priority order
   - Provide code snippets where helpful

5. **Ask:** "Should I implement the suggested fixes?"
```

## Example 6: Code Review with Subagent

`.opencode/command/review.md`:

```markdown
---
description: Comprehensive code review of recent changes
agent: code-reviewer
subtask: true
---

Review all changes since the last commit:

!`git diff HEAD~1`

**Review Criteria:**

1. **Code Quality**
   - Clean, readable code
   - Proper naming conventions
   - DRY principle adherence
   - Single responsibility

2. **Security**
   - Input validation
   - SQL injection prevention
   - XSS prevention
   - Sensitive data handling

3. **Performance**
   - N+1 query potential
   - Unnecessary loops
   - Memory usage concerns

4. **Testing**
   - Are changes covered by tests?
   - Edge cases considered?

5. **Laravel/React Patterns**
   - Following framework conventions
   - Proper use of Actions, DTOs
   - React hooks usage

**Output Format:**

For each issue found:
```

[SEVERITY: Critical/Warning/Suggestion]
File: path/to/file.php:line
Issue: Brief description
Recommendation: How to fix

```

**Summary:**
- Critical issues: N
- Warnings: N
- Suggestions: N
- Overall assessment: [Approve / Request Changes / Needs Discussion]
```

## Example 7: Database Reset with Verification

`.opencode/command/fresh.md`:

```markdown
---
description: Reset database with fresh migrations, seeders, and verification
agent: build
---

Reset the database to a fresh state:

**Step 1: Run Fresh Migration**
!`php artisan migrate:fresh --seed 2>&1`

**Step 2: Verify Success**
!`php artisan db:show 2>&1 | head -30`

**Analysis:**

**If migration succeeded:**

- List tables created (count and names)
- Confirm seeders ran
- Report: "Database reset complete: N tables, seeded successfully"

**If migration failed:**

- Show the specific error
- Identify which migration failed
- Suggest fix:
  - If schema issue: Show the problematic migration
  - If seeder issue: Show the failing seeder
  - If connection issue: Check database config

**If seeder failed:**

- Identify which seeder failed
- Show the error
- Migrations are still applied; suggest `php artisan db:seed` after fixing

**Warning:** This command destroys all data. Only use in development.
```

## Example 8: Action Creation with Full Stack

`.opencode/command/action.md`:

````markdown
---
description: Create a new Action class with DTO and tests following domain patterns
agent: build
---

Create an Action class for: $ARGUMENTS

**Parse the argument:**

- If format is `Domain/ActionName`: Use specified domain
- If format is `ActionName`: Infer domain from context or ask

**1. Create the Action**
Location: `app/Actions/{Domain}/$ARGUMENTS.php`

```php
<?php

declare(strict_types=1);

namespace App\Actions\{Domain};

final readonly class $ARGUMENTS
{
    public function __construct(
        // Inject dependencies
    ) {}

    public function execute({DTO}DTO $data): {ReturnType}
    {
        // Implementation
    }
}
```
````

**2. Create the DTO**
Location: `app/DTOs/{Domain}/{DTO}DTO.php`

```php
<?php

declare(strict_types=1);

namespace App\DTOs\{Domain};

final readonly class {DTO}DTO
{
    public function __construct(
        // Define properties
    ) {}
}
```

**3. Create Feature Test**
Location: `tests/Feature/Actions/{Domain}/$ARGUMENTSTest.php`

**After Creation:**

1. Verify all files exist
2. Run PHPStan on new files:
   !`./vendor/bin/phpstan analyse app/Actions/{Domain}/$ARGUMENTS.php`
3. Show all created files
4. Provide Controller integration example
5. Suggest FormRequest if user input is involved

````

Usage: `/action User/UpdateProfile` or `/action CreatePost`

## Example 9: Migration with Best Practices

`.opencode/command/migration.md`:

```markdown
---
description: Create a database migration with proper conventions and safety checks
agent: build
---

Create a migration for: $ARGUMENTS

**Determine Migration Type:**
- `create_X_table` → New table
- `add_X_to_Y_table` → Add column(s)
- `update_X_table` → Modify existing
- `drop_X_from_Y_table` → Remove column(s)

**Step 1: Create Migration**
!`php artisan make:migration $ARGUMENTS`

**Step 2: Edit Migration**
Apply these standards:
- Use appropriate column types (avoid string for everything)
- Add nullable() only when truly optional
- Add default values where sensible
- Add foreign keys with proper cascading
- Add indexes for:
  - Foreign keys (automatic in Laravel)
  - Columns used in WHERE clauses
  - Columns used in ORDER BY

**Step 3: Verify Syntax**
!`php artisan migrate --pretend`

**After Creation:**
1. Show the complete migration file
2. Explain each column choice
3. Warn about irreversible operations (dropColumn, etc.)
4. If adding foreign key: Verify referenced table exists
5. Suggest: "Run `php artisan migrate` to apply"

**Safety Notes:**
- For production: Consider if down() is truly reversible
- For large tables: Note potential locking issues
- For foreign keys: Ensure data integrity
````

Usage: `/migration create_posts_table`

## Example 10: Full Endpoint with All Layers

`.opencode/command/endpoint.md`:

```markdown
---
description: Create a complete API endpoint with Action, DTO, FormRequest, Controller, Route, and Tests
agent: build
subtask: true
---

Create a complete endpoint for: $ARGUMENTS

Think carefully about the domain and resource before implementing.

**Parse the argument:**

- Infer: Action type (Create, Update, Delete, Show, List)
- Infer: Resource name and domain
- Ask if ambiguous

**Generate these files in order:**

**1. DTO** (`app/DTOs/{Domain}/{Action}{Resource}DTO.php`)

- Immutable with readonly properties
- All properties typed

**2. FormRequest** (`app/Http/Requests/{Action}{Resource}Request.php`)

- Validation rules
- `toDTO()` method returning the DTO
- Authorization if needed

**3. Action** (`app/Actions/{Domain}/{Action}{Resource}Action.php`)

- Accept DTO as parameter
- Return typed result
- Single responsibility

**4. Controller** (`app/Http/Controllers/{Resource}Controller.php`)

- Add method if controller exists, else create
- Thin: only validate, call action, return response
- Return Inertia::render() or JSON

**5. Route** (add to `routes/web.php` or `routes/api.php`)

- RESTful naming
- Proper middleware (auth, verified, etc.)
- Route model binding if applicable

**6. Feature Test** (`tests/Feature/{Action}{Resource}Test.php`)

- Test happy path
- Test validation failures
- Test authorization (if applicable)
- Use factories for test data

**Verification:**

1. Run PHPStan on all new files
2. Run the new test:
   !`php artisan test --filter={Action}{Resource}Test`

**Final Output:**

- List all created files with paths
- Show route definition
- Provide curl/fetch example for testing
- Suggest React page to create next
```

Usage: `/endpoint CreatePost` or `/endpoint User/UpdateSettings`

## Example 11: Commit with Conventional Format

`.opencode/command/commit.md`:

```markdown
---
description: Create a well-formatted git commit with conventional commit message
agent: build
---

Analyze staged changes and create a commit:

!`git diff --cached --stat`
!`git diff --cached`

**Analyze the changes:**

1. Identify the type of change:
   - `feat`: New feature
   - `fix`: Bug fix
   - `refactor`: Code restructuring
   - `docs`: Documentation
   - `test`: Tests
   - `chore`: Maintenance

2. Identify the scope (optional):
   - Component/module affected
   - e.g., `auth`, `users`, `api`

3. Write commit message:
   - Subject: <type>(<scope>): <description> (max 72 chars)
   - Body: Explain WHY, not WHAT (the diff shows what)
   - Footer: Reference issues if applicable

**Safety Checks:**

- If .env, credentials, or secrets staged: STOP and warn
- If unrelated changes mixed: Suggest splitting commits

**If changes look good:**
```

git commit -m "<type>(<scope>): <subject>

<body explaining the why>

<footer with issue refs if any>"
```

**After commit:**

- Show the commit hash
- Suggest: "Push with `git push` or continue working"

````

## Example 12: CI-Safe Quality Check (Headless)

`.opencode/command/ci-check.md`:

```markdown
---
description: Run quality checks in CI mode (no interactive prompts, structured output)
agent: build
---

Run all quality checks and report results in CI-parseable format.

!`composer run checks 2>&1`
!`npm run checks 2>&1`

**Output Format (for CI parsing):**

````

STATUS: PASS|FAIL
RECTOR: PASS|FAIL [details if fail]
PINT: PASS|FAIL [details if fail]
PHPSTAN: PASS|FAIL [N errors if fail]
ESLINT: PASS|FAIL [N errors if fail]
TYPESCRIPT: PASS|FAIL [N errors if fail]
TESTS: PASS|FAIL [N passed, M failed]
COVERAGE: XX% [PASS if >= 90%, FAIL otherwise]

```

**Rules:**
- Do NOT ask questions
- Do NOT make changes
- Do NOT suggest fixes
- ONLY report status

Exit with summary line:
`RESULT: [PASS|FAIL] - [summary of issues if any]`
```

## Example 13: PR Creation

`.opencode/command/pr.md`:

```markdown
---
description: Create a pull request with comprehensive description
agent: build
---

Create a pull request for the current branch:

**Gather context:**
!`git branch --show-current`
!`git log main..HEAD --oneline`
!`git diff main..HEAD --stat`

**Analyze changes:**

1. Identify the main purpose of changes
2. List files modified, added, deleted
3. Identify breaking changes if any
4. Note testing done

**Generate PR:**
!`gh pr create --title "<type>: <brief description>" --body "## Summary
<1-3 bullet points of what this PR does>

## Changes

<list of significant changes>

## Testing

- [ ] Tests added/updated
- [ ] Manual testing completed
- [ ] CI passing

## Related Issues

Closes #<issue> (if applicable)
"`

**After PR created:**

- Show the PR URL
- Suggest reviewers based on files changed
- Note if CI is running
```
