---
name: test-story-coupling
description: Enforce tight coupling between components, tests, and stories with exact naming conventions. Use when creating new components, writing tests, or ensuring test/story files exist for all user-facing components.
---

# Test-Story Coupling

Enforce strict naming conventions and completeness requirements for tests and stories. Every user-facing component MUST have matching test and story files.

## Critical Naming Convention

File names MUST match exactly to maintain coupling and discoverability:

```
ComponentName.tsx          # The component
ComponentName.test.tsx     # Unit tests (EXACT name match)
ComponentName.stories.tsx  # Storybook stories (EXACT name match)
```

**Key Points:**

- Test files MUST match component filename exactly
- Story files MUST match component filename exactly
- No variations like kebab-case, snake_case, or different naming
- Extensions must be `.test.tsx` (React) or `.test.ts` (utilities)
- Story extensions must be `.stories.tsx`

## File Type Requirements

### User-Facing Components

**MUST have a story file AND EITHER a test file OR assertions in the story file**

Components can be tested in two ways:

1. **Traditional**: Separate `.test.tsx` file with unit tests
2. **Story-based**: `.stories.tsx` file with [interaction testing](https://storybook.js.org/docs/writing-tests/interaction-testing) using `play` functions

```bash
# ✅ Good: Complete set with separate test file
MusicBrainzArtistField.tsx
MusicBrainzArtistField.test.tsx
MusicBrainzArtistField.stories.tsx

# ✅ Good: Story file with assertions (no separate test file needed)
Button.tsx
Button.stories.tsx  # Contains play() functions with assertions

# ❌ Bad: Missing both test file and story assertions
MusicBrainzArtistField.tsx
MusicBrainzArtistField.stories.tsx  # No play() functions
# Missing: MusicBrainzArtistField.test.tsx

# ❌ Bad: Missing story file entirely
MusicBrainzArtistField.tsx
MusicBrainzArtistField.test.tsx
# Missing: MusicBrainzArtistField.stories.tsx
```

**Story-based testing example**:

```typescript
// Button.stories.tsx with assertions
import type { Meta, StoryObj } from '@storybook/react';
import { expect, userEvent, within } from '@storybook/test';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Default: Story = {
  args: {
    label: 'Click me',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    // Assertions in story file
    await expect(button).toBeInTheDocument();
    await userEvent.click(button);
    await expect(button).toHaveClass('clicked');
  },
};
```

# ❌ Bad: Name mismatch

MusicBrainzArtistField.tsx
musicbrainz-artist-field.test.tsx # Wrong case!
MusicBrainzArtistField.stories.tsx

````

### Utility Functions and Hooks
**MUST have test files, stories optional**

```bash
# ✅ Good: Utility with test
importAds.ts
importAds.test.ts

# ✅ Good: Hook with test
useArtistSearch.ts
useArtistSearch.test.ts

# ❌ Bad: Utility without test
formatDate.ts
# Missing formatDate.test.ts
````

### Migration Scripts

**MUST have test files**

```bash
# ✅ Good: Migration with test (from bin/migrations/)
bin/migrations/importSchedule.ts
bin/migrations/importSchedule.test.ts

# ❌ Bad: Migration without test
bin/migrations/importNewData.ts
# Missing importNewData.test.ts
```

## Examples from Codebase

### Good Examples

```bash
# Payload CMS Fields - Complete sets
payload/src/components/fields/MusicBrainzArtistField.tsx
payload/src/components/fields/MusicBrainzArtistField.stories.tsx

payload/src/components/fields/MusicBrainzReleaseField.tsx
payload/src/components/fields/MusicBrainzReleaseField.stories.tsx

payload/src/components/fields/MusicBrainzRecordingField.tsx
payload/src/components/fields/MusicBrainzRecordingField.stories.tsx

# Migration Scripts - Utilities with tests
bin/migrations/importAds.ts
bin/migrations/importAds.test.ts

bin/migrations/importDJs.ts
bin/migrations/importDJs.test.ts

# Shared Utilities - Complete coverage
bin/migrations/shared/artistCleaner.ts
bin/migrations/shared/artistCleaner.test.ts

bin/migrations/shared/validation.ts
bin/migrations/shared/validation.test.ts
```

### Bad Examples (Anti-patterns)

```bash
# ❌ Name mismatch - Wrong case
MyComponent.tsx
my-component.test.tsx        # Should be: MyComponent.test.tsx
MyComponent.stories.tsx

# ❌ Name mismatch - Different naming
ArtistCard.tsx
ArtistCardTests.test.tsx     # Should be: ArtistCard.test.tsx
ArtistCard.stories.tsx

# ❌ Missing test file
NewFeature.tsx
NewFeature.stories.tsx
# Missing: NewFeature.test.tsx

# ❌ Missing story file for user-facing component
Button.tsx
Button.test.tsx
# Missing: Button.stories.tsx
```

## Testing Patterns

### Component Tests

Use Vitest with jsdom for React component testing:

```typescript
// ArtistCard.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ArtistCard } from './ArtistCard';

describe('ArtistCard', () => {
  it('renders artist name', () => {
    render(<ArtistCard artist={{ name: 'Miles Davis' }} />);
    expect(screen.getByText('Miles Davis')).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    render(<ArtistCard artist={artist} onClick={handleClick} />);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

### Utility Tests

Test pure functions with clear inputs and outputs:

```typescript
// formatDate.test.ts
import { describe, it, expect } from 'vitest';
import { formatDate } from './formatDate';

describe('formatDate', () => {
  it('formats ISO date to MM/DD/YYYY', () => {
    expect(formatDate('2024-01-15')).toBe('01/15/2024');
  });

  it('handles invalid dates gracefully', () => {
    expect(formatDate('invalid')).toBe('Invalid Date');
  });
});
```

### Integration Tests

Test multiple units working together:

```typescript
// importDJs.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { importDJs } from './importDJs';
import * as payloadClient from './shared/payloadClient';

describe('importDJs', () => {
  beforeEach(() => {
    vi.spyOn(payloadClient, 'findOrCreatePerson');
  });

  it('should import new DJ successfully and create person', async () => {
    const result = await importDJs({ env: 'test', ids: [1] });

    expect(result.imported).toBe(1);
    expect(payloadClient.findOrCreatePerson).toHaveBeenCalled();
  });
});
```

## Storybook Patterns

### Component Stories

Document component variations and use cases:

```typescript
// ArtistCard.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ArtistCard } from './ArtistCard';

const meta: Meta<typeof ArtistCard> = {
  title: 'Components/ArtistCard',
  component: ArtistCard,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof ArtistCard>;

export const Default: Story = {
  args: {
    artist: {
      name: 'Miles Davis',
      genre: 'Jazz',
    },
  },
};

export const WithLongName: Story = {
  args: {
    artist: {
      name: 'Thelonious Sphere Monk',
      genre: 'Jazz',
    },
  },
};

export const Loading: Story = {
  args: {
    artist: null,
    loading: true,
  },
};
```

### Field Component Stories

For Payload CMS fields, show integration with Payload:

```typescript
// MusicBrainzArtistField.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { MusicBrainzArtistField } from './MusicBrainzArtistField';

const meta: Meta<typeof MusicBrainzArtistField> = {
  title: 'Payload/Fields/MusicBrainzArtistField',
  component: MusicBrainzArtistField,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof MusicBrainzArtistField>;

export const Empty: Story = {
  args: {
    value: '',
    onChange: () => {},
  },
};

export const WithValue: Story = {
  args: {
    value: 'Miles Davis',
    onChange: () => {},
  },
};
```

## Enforcement Strategy

### Pre-commit Hook

A custom script `bin/check-test-story-files.ts` validates file presence:

```typescript
/**
 * Pre-commit hook to check for missing test/story files
 * Run with: tsx bin/check-test-story-files.ts
 */

// Pseudo-code for validation logic:
// 1. Get staged .tsx files (components)
// 2. Check if matching .test.tsx exists
// 3. Check if matching .stories.tsx exists (for user-facing components)
// 4. Exit with code 1 if violations found
// 5. Allow --skip-check flag for emergency commits
```

### CI Validation

GitHub Actions should validate completeness:

```yaml
# .github/workflows/test.yml
- name: Check test-story coupling
  run: tsx bin/check-test-story-files.ts --all
```

## Coverage Requirements

From `vitest.config.ts`:

```typescript
coverage: {
  statements: 80,
  branches: 80,
  functions: 80,
  lines: 80,
}
```

All new code must meet these thresholds.

## When to Skip

### Legitimate Exceptions

- **Layout components**: `layout.tsx`, `page.tsx` (Next.js conventions)
- **Config files**: `vitest.config.ts`, `next.config.mjs`
- **Type-only files**: `types.ts`, `interfaces.ts`
- **Generated files**: Payload types, migration files

Use `--skip-check` flag for emergency commits, but fix violations ASAP.

## Quick Reference

### Checklist for New Components

- [ ] Component file: `ComponentName.tsx`
- [ ] Test file: `ComponentName.test.tsx` (EXACT name match)
- [ ] Story file: `ComponentName.stories.tsx` (EXACT name match)
- [ ] Tests cover key functionality
- [ ] Stories document variations
- [ ] Coverage thresholds met

### Checklist for New Utilities

- [ ] Utility file: `utilityName.ts`
- [ ] Test file: `utilityName.test.ts` (EXACT name match)
- [ ] Tests cover edge cases
- [ ] Coverage thresholds met

### Checklist for Migrations

- [ ] Migration file: `bin/migrations/importData.ts`
- [ ] Test file: `bin/migrations/importData.test.ts` (EXACT name match)
- [ ] Tests mock external dependencies
- [ ] Tests verify happy path and error cases

## Additional Resources

- [Vitest Documentation](https://vitest.dev/)
- [Storybook Documentation](https://storybook.js.org/)
- [Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- See existing test examples in `bin/migrations/**/*.test.ts`
