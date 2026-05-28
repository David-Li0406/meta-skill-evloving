---
name: consistency-review
description: |
  Code consistency and pattern adherence review skill.
  Naming conventions, style consistency, pattern usage, and project standards validation.
  Use during VERIFICATION to ensure codebase uniformity and maintainability.
---

# Consistency Review

Code consistency and project standards validation for ultrawork verification phase.

## What This Skill Provides

Systematic approach to checking:
- Naming conventions across the codebase
- Code style consistency
- Pattern adherence and repetition
- Project-specific standards
- Documentation consistency

## When to Use This Skill

**During VERIFICATION phase:**
- After workers complete tasks
- Before marking tasks as complete
- When multiple workers contribute to same feature
- Before final approval

**During PLANNING phase:**
- Validating design document format
- Ensuring task naming consistency
- Checking for adherence to project patterns

## Naming Conventions

### 1. Variable and Function Names

**Checklist:**

```
[ ] Consistent naming style (camelCase, PascalCase, snake_case)
[ ] Descriptive names (not x, tmp, data)
[ ] Boolean variables prefixed (is, has, should, can)
[ ] Functions are verbs (get, set, create, update, delete)
[ ] Constants are UPPER_SNAKE_CASE
[ ] Private members prefixed/suffixed (_, $)
[ ] Abbreviations used consistently
```

**Examples:**

```javascript
// ❌ Bad: Inconsistent naming
const UserData = "john";        // PascalCase for variable
function GetUser() {}           // PascalCase for function
const is_active = true;         // snake_case
const MAX_users = 100;          // Mixed case

// ✅ Good: Consistent naming
const userName = "john";        // camelCase
function getUser() {}           // camelCase
const isActive = true;          // camelCase, boolean prefix
const MAX_USERS = 100;          // UPPER_SNAKE_CASE
```

### 2. File and Directory Names

**Checklist:**

```
[ ] Consistent file naming (kebab-case or camelCase throughout)
[ ] Component files match component name
[ ] Test files follow naming convention (*.test.*, *.spec.*)
[ ] Index files used consistently
[ ] Directory structure follows project pattern
```

**Common Patterns:**

| Language/Framework | Convention | Example |
|-------------------|------------|---------|
| JavaScript/Node | kebab-case | `user-service.js` |
| React Components | PascalCase | `UserProfile.jsx` |
| TypeScript | camelCase or kebab-case | `userService.ts` |
| Tests | Same as source + suffix | `user-service.test.js` |

### 3. Class and Type Names

**Checklist:**

```
[ ] Classes are PascalCase
[ ] Interfaces prefixed or suffixed consistently (I or Interface)
[ ] Types are PascalCase
[ ] Enums are PascalCase
[ ] Generic type parameters are single uppercase or descriptive
```

**Examples:**

```typescript
// ❌ Bad: Inconsistent class/type naming
class userService {}            // Should be PascalCase
interface user {}               // Should be PascalCase
type paymentStatus = string;    // Should be PascalCase
enum order_status {}            // Should be PascalCase

// ✅ Good: Consistent naming
class UserService {}
interface IUser {}              // Or just User
type PaymentStatus = 'pending' | 'complete';
enum OrderStatus { Pending, Shipped, Delivered }
```

## Code Style Consistency

### 1. Formatting

**Checklist:**

```
[ ] Consistent indentation (2 or 4 spaces, never mixed)
[ ] Consistent quote style (single or double, not mixed)
[ ] Consistent semicolon usage (always or never)
[ ] Consistent brace style (same line or new line)
[ ] Consistent spacing around operators
[ ] Consistent line length (80, 100, 120 chars)
[ ] Consistent trailing commas
[ ] Consistent import ordering
```

**Tool Integration:**

```bash
# Use Prettier for automatic formatting
npm install --save-dev prettier

# .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}

# Format all files
npx prettier --write "src/**/*.{js,ts,jsx,tsx}"
```

### 2. Import Statements

**Checklist:**

```
[ ] Consistent import ordering (external, internal, types)
[ ] Consistent import style (named vs default)
[ ] No unused imports
[ ] Consistent path aliases (@/, ~/, etc.)
[ ] Grouped by type (libraries, components, utils)
```

**Examples:**

```javascript
// ❌ Bad: Random import order
import { Button } from './Button';
import React from 'react';
import type { User } from './types';
import axios from 'axios';

// ✅ Good: Organized imports
// 1. External libraries
import React from 'react';
import axios from 'axios';

// 2. Internal components/modules
import { Button } from './Button';

// 3. Types
import type { User } from './types';
```

### 3. Comments and Documentation

**Checklist:**

```
[ ] Consistent comment style (// vs /* */)
[ ] JSDoc for public APIs
[ ] Inline comments for complex logic only
[ ] No commented-out code
[ ] No TODO/FIXME without tickets
[ ] Comments explain "why", not "what"
[ ] Documentation format consistent (Markdown, JSDoc)
```

**Examples:**

```javascript
// ❌ Bad: Obvious comment, no context
// Loop through users
for (const user of users) {
  // Check if active
  if (user.isActive) {
    // Send email
    sendEmail(user);
  }
}

// ✅ Good: Explains why, not what
// Only notify active users to reduce spam complaints
for (const user of users) {
  if (user.isActive) {
    sendEmail(user);
  }
}
```

## Pattern Adherence

### 1. Error Handling Patterns

**Checklist:**

```
[ ] Consistent error handling (try/catch vs callbacks vs promises)
[ ] Error objects have consistent structure
[ ] Error messages follow same format
[ ] Error logging uses same method
[ ] Custom errors extend base Error class
```

**Examples:**

```javascript
// ❌ Bad: Inconsistent error handling
async function getUserA() {
  try {
    return await db.getUser();
  } catch (e) {
    console.error(e);
    return null;
  }
}

async function getUserB() {
  const user = await db.getUser();
  if (!user) throw new Error('Not found');
  return user;
}

// ✅ Good: Consistent error handling
async function getUser(id) {
  try {
    const user = await db.users.findById(id);
    if (!user) {
      throw new NotFoundError(`User ${id} not found`);
    }
    return user;
  } catch (error) {
    logger.error('Failed to get user', { id, error });
    throw error;
  }
}
```

### 2. Async Patterns

**Checklist:**

```
[ ] Consistent async/await vs .then()/.catch()
[ ] Consistent Promise handling
[ ] Consistent error propagation
[ ] Consistent timeout handling
```

**Examples:**

```javascript
// ❌ Bad: Mixed patterns
const data1 = await fetch(url1);
fetch(url2).then(res => res.json()).then(data => process(data));

// ✅ Good: Consistent async/await
const data1 = await fetch(url1);
const response2 = await fetch(url2);
const data2 = await response2.json();
```

### 3. Data Validation Patterns

**Checklist:**

```
[ ] Consistent validation library (Zod, Joi, Yup)
[ ] Validation at consistent layer (routes, services, models)
[ ] Error messages follow same format
[ ] Validation schemas colocated
```

### 4. Testing Patterns

**Checklist:**

```
[ ] Consistent test structure (describe/it vs test)
[ ] Consistent assertion library
[ ] Consistent mocking approach
[ ] Test file naming consistent
[ ] Setup/teardown patterns consistent
```

**Examples:**

```javascript
// ❌ Bad: Inconsistent test structure
describe('UserService', () => {
  test('creates user', () => {});  // Using 'test'
});

describe('OrderService', () => {
  it('creates order', () => {});   // Using 'it'
});

// ✅ Good: Consistent structure
describe('UserService', () => {
  it('creates user', () => {});
  it('updates user', () => {});
});

describe('OrderService', () => {
  it('creates order', () => {});
  it('updates order', () => {});
});
```

## Project-Specific Standards

### 1. CLAUDE.md Adherence

**Checklist:**

```
[ ] Follows project conventions in CLAUDE.md
[ ] Adheres to defined coding standards
[ ] Uses project-specific patterns
[ ] Respects defined constraints
[ ] Matches project vocabulary
```

**How to Check:**

```bash
# Read project standards
Read("/path/to/project/CLAUDE.md")

# Check for violations
# - Compare code against stated standards
# - Verify pattern usage
# - Check terminology consistency
```

### 2. Directory Structure

**Checklist:**

```
[ ] New files in correct directories
[ ] Directory structure matches project pattern
[ ] No files in wrong layers
[ ] Feature folders organized consistently
```

### 3. Configuration Patterns

**Checklist:**

```
[ ] Environment variables named consistently
[ ] Configuration files follow project format
[ ] Secrets management consistent
[ ] Default values handled uniformly
```

## Consistency Scoring

### Category Weights

| Category | Weight | Score Range |
|----------|--------|-------------|
| Naming | 30% | 0-10 |
| Style | 25% | 0-10 |
| Patterns | 25% | 0-10 |
| Documentation | 20% | 0-10 |

**Overall Score = Weighted Average**

- **9-10**: Excellent consistency, matches project standards
- **7-8**: Good consistency, minor deviations
- **5-6**: Fair consistency, notable inconsistencies
- **0-4**: Poor consistency, major refactoring needed

## Review Process

### Step 1: Automated Checks

```bash
# Linting
npm run lint

# Formatting check
npx prettier --check "src/**/*.{js,ts}"

# Type checking (TypeScript)
npm run type-check
```

### Step 2: Pattern Analysis

Compare new code against existing patterns:
- Find similar components
- Check if patterns are replicated
- Verify naming matches conventions
- Ensure structure aligns

```bash
# Find similar files for comparison
find src -name "*Service.ts" | head -5
find src -name "*.test.ts" | head -5
```

### Step 3: Documentation Review

Check:
- README updated if needed
- API docs consistent with changes
- Comments follow project style
- CHANGELOG updated

### Step 4: Naming Audit

Review all new identifiers:
- Variables follow convention
- Functions follow convention
- Classes follow convention
- Files follow convention

## Common Inconsistencies

| Inconsistency | Impact | Fix |
|---------------|--------|-----|
| Mixed naming styles | Confusion, hard to search | Choose one style, apply everywhere |
| Inconsistent imports | Hard to read | Enforce import ordering |
| Mixed error handling | Unpredictable behavior | Standardize error pattern |
| Different test styles | Maintainability issues | Pick one test structure |
| Varied formatting | Merge conflicts | Use Prettier/ESLint |
| Mixed quotes | Visual noise | Configure auto-formatter |

## Project Vocabulary Consistency

### ultrawork Example

**Standard vocabulary (from CLAUDE.md):**

| Use ✅ | Avoid ❌ |
|--------|----------|
| evidence | proof, confirmation |
| criterion (singular) | criteria (singular) |
| criteria (plural) | criterias, criterions |
| resolved | complete, done, closed |
| PASS / FAIL | passed / failed |
| exit code 0 | return code 0, status 0 |

### Checking Vocabulary

```bash
# Search for non-standard terms
grep -r "criterias\|proof\|done\|complete\|passed" src/

# Should use: criteria, evidence, resolved, PASS
```

## Evidence Collection

When reviewing consistency:

```bash
# Add consistency assessment to evidence
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id verify \
  --add-evidence "Consistency Review: 8/10" \
  --add-evidence "- Naming conventions: ✓" \
  --add-evidence "- Style consistent: ✓" \
  --add-evidence "- Patterns followed: ✓" \
  --add-evidence "- Minor: Mixed quote style in test files"
```

## Tools and Automation

### Linters and Formatters

```bash
# ESLint for linting
npm install --save-dev eslint

# Prettier for formatting
npm install --save-dev prettier

# Combine with husky for pre-commit hooks
npm install --save-dev husky lint-staged
```

### Pre-commit Hooks

```json
// package.json
{
  "lint-staged": {
    "*.{js,ts,jsx,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

### Configuration Files

**ESLint (.eslintrc.json):**

```json
{
  "extends": ["eslint:recommended"],
  "rules": {
    "camelcase": "error",
    "quotes": ["error", "single"],
    "semi": ["error", "always"]
  }
}
```

**Prettier (.prettierrc):**

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

## Integration with Ultrawork

### During Task Execution

Workers should:
- Follow existing patterns
- Match naming conventions
- Use consistent style
- Check project CLAUDE.md

### During Verification

Verifier should:
- Check consistency score
- Identify deviations
- Suggest corrections
- Block if major inconsistencies

```bash
# Example: Block on consistency failure
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id verify \
  --status resolved \
  --add-evidence "VERDICT: FAIL - Consistency issues" \
  --add-evidence "Mixed naming: camelCase and snake_case in same file" \
  --add-evidence "Inconsistent error handling patterns"
```

## Quick Reference

**Must-have consistency:**
- Single naming convention throughout
- Consistent code formatting (use Prettier)
- Uniform error handling pattern
- Consistent test structure
- Follow project CLAUDE.md standards

**Quick checks:**
1. Run linter: `npm run lint`
2. Check formatting: `npx prettier --check .`
3. Compare to existing similar files
4. Verify project vocabulary usage
5. Check directory structure alignment

**When in doubt:**
- Look at existing code for patterns
- Check project CLAUDE.md
- Ask for clarification
- Prefer consistency over personal preference
