# Issue Fixing Workflow - Complete Guide

This document provides detailed instructions for all seven phases of the systematic issue-fixing process.

## Phase 1: Issue Registration

### 1.1 Parse User Instruction

Extract the following information from user input:
- Issue title/description
- Affected components (frontend/backend/both/config)
- Expected vs actual behavior
- Error messages or logs (if provided)

### 1.2 Check Existing Issues

Read `.issues/opening.md` and search for keywords from the issue description:
- If issue exists: Note the issue number and proceed to Phase 2
- If issue NOT found: Add new issue entry

### 1.3 Issue Entry Format

When adding a new issue to `.issues/opening.md`:

```markdown
## [#N] Issue Title
- **Status**: Investigating
- **Component**: [Frontend/Backend/Both/Config]
- **Severity**: [Critical/High/Medium/Low]
- **Description**: Brief description of the issue
- **Reporter**: Copilot Fixer Agent
- **Created**: YYYY-MM-DD HH:MM
```

## Phase 2: Investigation

### 2.1 Code Discovery

Use parallel exploration to find related code:

1. **Search by keywords** from issue description:
   - Use `grep` for error messages, function names, component names
   - Search in both frontend and backend directories
   - Include test files in search

2. **Identify affected files**:
   - List all files containing relevant code
   - Categorize by: Frontend, Backend, Tests, Config
   - Note dependencies between files

3. **Read critical files**:
   - Open and analyze main affected files
   - Understand current implementation
   - Identify root cause of the issue

### 2.2 Root Cause Analysis

1. **Trace the error path**:
   - **Frontend**: Component → Hook → API call → State
   - **Backend**: Endpoint → Service → Repository → Database
   - **Integration**: Request → Response → Error handling

2. **Document findings**:
   - Root cause of the issue
   - Why current code doesn't work
   - Side effects of potential fixes

## Phase 3: Impact Assessment

### 3.1 Evaluate Fix Complexity

Calculate impact score based on:

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| **Files to modify** | 1-2 files | 3-5 files | 6+ files |
| **LOC changes** | <50 lines | 50-200 lines | 200+ lines |
| **Architecture changes** | None | Minor refactor | Major refactor |
| **Breaking changes** | None | Backward compatible | Breaking |

### 3.2 Decision Point

**If impact is HIGH** (score >= 3 Medium or 1+ High):
1. Create a feature plan in `.features/` directory
2. Use format: `fix-[issue-slug].md`
3. Include:
   - Issue reference
   - Root cause analysis
   - Proposed solution architecture
   - Files to be modified
   - Migration strategy (if needed)
   - Testing strategy
4. Update issue status to "Planned - Feature Required"
5. Suggest handoff to `speckit.plan` agent
6. **STOP** - Do not proceed with implementation

**If impact is LOW or MEDIUM**:
- Proceed to Phase 4 (Implementation)

## Phase 4: Implementation

### 4.1 Pre-Implementation Checklist

1. **Review project standards**:
   - Read `.github/instructions/backend.instructions.md` (if backend fix)
   - Read `.github/instructions/frontend.instructions.md` (if frontend fix)
   - Read `.github/instructions/python_standard.instructions.md` (if Python code)
   - Read `.github/instructions/ts_standard.instructions.md` (if TypeScript code)

2. **Create a fix plan**:
   - List files to modify in order
   - Describe specific changes for each file
   - Note any new files needed

### 4.2 Apply Fixes

**CRITICAL PRINCIPLES**:
- **Minimal changes**: Modify only what's necessary
- **No unrelated changes**: Don't fix other issues
- **Preserve working code**: Don't delete functioning code
- **Follow existing patterns**: Match the project's style
- **Type safety**: Maintain or improve type annotations
- **Error handling**: Add proper error handling if missing

**Backend fixes** (order of changes):
1. Service layer first (business logic)
2. API layer second (endpoints)
3. Models/schemas third (data structures)
4. Update tests last

**Frontend fixes** (order of changes):
1. Utility/helper functions first
2. Hooks/context second
3. Components third
4. Update tests last

**For each file modification**:
1. Read the full file first
2. Identify the exact section to change
3. Apply surgical edits using `edit` tool
4. Add inline comments for complex logic ONLY if necessary

### 4.3 Configuration Changes

If config files need updates:
- `.env` / `.env.example`: Update with clear comments
- `package.json` / `pyproject.toml`: Update dependencies
- `docker-compose.yml`: Update service configurations
- TypeScript configs: Update compiler options
- ESLint/Prettier: Update linting rules

## Phase 5: Validation

### 5.1 Code Quality Checks

**For Backend (Python) changes**:
```bash
# Type checking (MUST pass with 0 errors)
python -m pyright app/

# Formatting
ruff format app/

# Linting
ruff check app/ --fix

# If any errors, fix them before proceeding
```

**For Frontend (TypeScript) changes**:
```bash
# Build (includes type check and lint)
cd frontend && npm run build

# If errors, fix them before proceeding
```

### 5.2 Unit Tests

**Backend tests**:
```bash
cd backend
pytest tests/ -v -k "test_related_to_fix"
```

**Frontend tests** (if available):
```bash
cd frontend
npm test -- --testPathPattern="component.test"
```

**If tests fail**:
1. Analyze the failure
2. Fix the code or update the test
3. Re-run until all pass

### 5.3 Add New Tests

**When to add tests**:
- New functions or methods
- Bug fixes (regression test)
- Changed behavior

**Backend test structure**:
```python
# tests/test_[module].py
import pytest
from app.services.your_service import YourService

def test_fixed_behavior():
    """Test that verifies the fix works correctly."""
    # Arrange
    service = YourService()
    
    # Act
    result = service.fixed_method()
    
    # Assert
    assert result == expected_value
```

**Frontend test structure**:
```typescript
// component.test.tsx
import { render, screen } from '@testing-library/react';
import YourComponent from './YourComponent';

test('renders correctly after fix', () => {
  render(<YourComponent />);
  expect(screen.getByText(/expected text/i)).toBeInTheDocument();
});
```

## Phase 6: E2E Testing (Full-Stack Fixes Only)

**When to create E2E tests**:
- Issue involves both frontend and backend
- User-facing feature or workflow
- API integration changes

### 6.1 Manual Testing with Browser

**IMPORTANT**: Test manually first before creating E2E tests

1. **Start services**:
   ```bash
   # Terminal 1: Backend
   cd backend && source .venv/bin/activate && uvicorn app.main:app --reload
   
   # Terminal 2: Frontend
   cd frontend && npm run dev
   
   # Terminal 3: Database
   docker-compose up -d neo4j
   ```

2. **Manual testing workflow**:
   - Open browser to `http://localhost:3000`
   - Navigate to affected feature
   - Perform the actions that previously failed
   - Verify the fix works as expected
   - Note all steps taken for E2E test

3. **Document the test scenario**:
   - User actions (clicks, inputs, navigation)
   - Expected outcomes at each step
   - API calls made (check network tab)
   - State changes (check React DevTools)

### 6.2 Create E2E Test

Create test file in `frontend/e2e/[feature-name].spec.ts`:

```typescript
import { test, expect, Page } from '@playwright/test';
import { registerAndLogin } from './helpers/auth';

test.describe('[Feature Name] - [Issue Description]', () => {
  // Helper functions
  async function navigateToFeature(page: Page): Promise<void> {
    await page.waitForSelector('.ant-menu', { timeout: 5000 });
    await page.goto('/feature-path');
    await page.waitForLoadState('networkidle');
  }

  test.beforeEach(async ({ page }) => {
    await registerAndLogin(page);
    await navigateToFeature(page);
  });

  test('should [describe expected behavior]', async ({ page }) => {
    // Step 1: Setup
    // ... initial state preparation
    
    // Step 2: Action
    // ... user actions that trigger the fix
    
    // Step 3: Verification
    // ... assertions that verify the fix
    
    // Step 4: Cleanup (if needed)
    // ... clean up test data
  });
  
  test('should handle [edge case]', async ({ page }) => {
    // Test edge cases related to the fix
  });
});
```

**Key patterns to follow**:
- Use `data-testid` attributes for stable selectors
- Use `page.waitForSelector()` for dynamic elements
- Use `page.waitForLoadState('networkidle')` after navigation
- Use `registerAndLogin()` helper for authentication
- Group related tests in `describe` blocks
- Add meaningful test descriptions

### 6.3 Run E2E Tests

```bash
cd frontend

# Run in headless mode (WSL/CI compatible)
npm run test:e2e:headless

# Run specific test file
npx playwright test e2e/[feature-name].spec.ts --headed

# Debug mode
npx playwright test e2e/[feature-name].spec.ts --debug
```

**If tests fail**:
1. Check the trace: `npx playwright show-report`
2. Fix the issue or adjust the test
3. Re-run until passing

## Phase 7: Final Steps

### 7.1 Update Issue Status

Update `.issues/opening.md`:

```markdown
## [#N] Issue Title
- **Status**: ✅ Fixed
- **Component**: [Frontend/Backend/Both/Config]
- **Severity**: [Critical/High/Medium/Low]
- **Description**: Brief description of the issue
- **Reporter**: Copilot Fixer Agent
- **Created**: YYYY-MM-DD HH:MM
- **Fixed**: YYYY-MM-DD HH:MM
- **Solution**: Brief description of the fix applied
- **Files Modified**: List of modified files
- **Tests Added**: List of new test files (if any)
```

### 7.2 Move to Resolved

If requested, move issue to `.issues/resolved.md`:
- Copy the updated entry
- Add to resolved.md
- Remove from opening.md

### 7.3 Generate Summary

Provide a concise summary:

```markdown
## Fix Summary

**Issue**: [#N] Issue Title
**Status**: ✅ Fixed
**Impact**: [Low/Medium] - [X] files modified, [Y] lines changed

### Changes Made:
- [File 1]: [Brief description]
- [File 2]: [Brief description]

### Tests:
- ✅ Type checks passed
- ✅ Linting passed
- ✅ Unit tests passed ([X] tests)
- ✅ E2E tests passed ([Y] tests) [if applicable]

### Verification:
- Manual testing completed
- All quality checks passed
- Standards compliance verified

### Next Steps:
- [Any follow-up tasks]
- [Documentation updates needed]
```

## Error Handling

**If any step fails**:
1. Log the error clearly
2. Update issue status to "Blocked - [Reason]"
3. Document the blocker in the issue entry
4. Suggest next steps or manual intervention needed
5. Do NOT proceed with broken code

**Common blockers**:
- Cannot determine root cause → Need human expertise
- Fix requires breaking changes → Create feature plan
- Tests cannot be written → Document why and mark as manual test required
- Dependencies missing → Update environment setup docs

## Best Practices

1. **Always start with investigation** - Don't jump to solutions
2. **Test incrementally** - Run checks after each file modification
3. **Keep changes minimal** - Resist the urge to refactor everything
4. **Document decisions** - Add comments explaining non-obvious fixes
5. **Think about edge cases** - What could break this fix?
6. **Respect the architecture** - Follow existing patterns
7. **Ask when uncertain** - Better to pause than break more things
