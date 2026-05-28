# Tech Debt Issue Template

Use this template for improvements and refactoring to address later.

## Template

```markdown
**Title:** [Tech Debt] {Area} - {description}
**Labels:** tech-debt
**Priority:** Low (unless blocking)

## Current State (Auto-gathered)
**Files affected:**
- `{path/to/file.ts}` - {current problem}

**Code sample:**
```{language}
{Current problematic code}
```

**Why it's debt:**
{Inferred from code analysis}

## Desired State
{What it should look like}

## Impact
- Performance: {assessment}
- Maintainability: {assessment}
- Developer experience: {assessment}

## Effort
{Small/Medium/Large based on files affected}

## Blocked By
{Other issues that should be done first, if any}
```

## Example

**User says:** "We should migrate from moment.js to date-fns"

**Created issue:**
```markdown
**Title:** [Tech Debt] Date utilities - Migrate from moment.js to date-fns
**Labels:** tech-debt
**Priority:** Low

## Current State (Auto-gathered)
**Files affected:**
- `src/utils/dates.ts` - Main date utility functions
- `src/components/DatePicker.tsx` - Uses moment formatting
- `package.json` - moment.js adds 300kb to bundle

**Code sample:**
```typescript
// src/utils/dates.ts
import moment from 'moment';

export function formatDate(date: Date): string {
  return moment(date).format('YYYY-MM-DD');
}
```

**Why it's debt:**
- moment.js is deprecated
- Large bundle size (300kb gzipped)
- date-fns is tree-shakeable and modern

## Desired State
Replace all moment.js usage with date-fns equivalents.

```typescript
// src/utils/dates.ts
import { format } from 'date-fns';

export function formatDate(date: Date): string {
  return format(date, 'yyyy-MM-dd');
}
```

## Impact
- Performance: Better (smaller bundle)
- Maintainability: Better (actively maintained)
- Developer experience: Similar API

## Effort
Medium (12 files to update)

## Blocked By
None
```
