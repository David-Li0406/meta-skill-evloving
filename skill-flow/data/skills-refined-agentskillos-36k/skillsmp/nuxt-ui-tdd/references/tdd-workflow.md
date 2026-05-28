# TDD Workflow for NuxtUI Components

## Overview

This guide documents the strict Test-Driven Development (TDD) workflow used in the Poche project for building Vue components with NuxtUI. The workflow is enforced by a TDD guard hook that prevents premature implementation and ensures proper RED-GREEN-REFACTOR cycles.

## The TDD Guard Hook

The TDD guard is a pre-tool-use hook that enforces TDD discipline by:

- **Blocking implementation without failing tests** - Cannot create component files without RED phase evidence
- **Preventing batch test creation** - Only ONE test can be added at a time
- **Enforcing test-first discipline** - Tests must fail before implementation
- **Tracking test state** - Uses `.claude/tdd-guard/data/test.json` to track RED/GREEN phases

### Common Guard Violations

1. **Multiple test addition** - Adding more than one test/story at a time
2. **Premature implementation** - Creating component files without failing tests
3. **Over-implementation** - Adding untested functionality during GREEN phase
4. **Missing RED phase evidence** - Implementing without capturing test failure

## The Complete TDD Cycle

### Step 1: Create ONE Test (RED Phase)

**Action**: Create a single Storybook story with one interaction test.

```typescript
// FormField.stories.ts
export const Default: Story = {
  args: {
    label: 'Email',
    name: 'email',
    placeholder: 'Enter your email',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = await canvas.findByPlaceholderText(/enter your email/i);
    await expect(input).toBeInTheDocument();
  },
};
```

**Critical Rules**:
- Only ONE story/test at a time
- One assertion per test initially
- Use descriptive, focused test names

### Step 2: Run Tests and Capture Failure (RED Phase Evidence)

**Action**: Run Storybook test-runner to capture the failure.

```bash
pnpm test:storybook:run -- [ComponentName]
```

**Expected**: Test should fail because component doesn't exist yet.

**Save Output**: Capture the failure output to a temporary file for evidence:

```bash
pnpm test:storybook:run -- SearchBar | tee /tmp/searchbar-red-phase.txt
```

### Step 3: Update test.json (RED Phase Tracking)

**Action**: Manually update `.claude/tdd-guard/data/test.json` to record the RED phase.

```json
{
  "verificationMode": false,
  "batchMode": false,
  "testModules": [
    {
      "moduleId": "/Users/tk/Code/poche/apps/web/components/molecules/SearchBar.stories.ts",
      "verificationMode": false,
      "batchMode": false,
      "tests": [
        {
          "name": "Default",
          "fullName": "Molecules/SearchBar › Default",
          "state": "failed",
          "note": "RED phase - component doesn't exist"
        }
      ]
    }
  ],
  "redPhaseEvidence": {
    "completed": true,
    "command": "pnpm test:storybook -- SearchBar",
    "exitCode": 1,
    "timestamp": "2025-11-02T13:52:00.000Z",
    "testSuitesFailed": 1,
    "testSuitesTotal": 1,
    "failureCount": 1,
    "totalTests": 1,
    "sampleErrors": [
      "FAIL browser: chromium components/molecules/SearchBar.stories.ts",
      "● Molecules/SearchBar › Default › play-test",
      "Failed to fetch dynamically imported module"
    ]
  },
  "unhandledErrors": [],
  "reason": "failed"
}
```

**Key Fields**:
- `state: "failed"` - Mark test as failing
- `redPhaseEvidence.completed: true` - Confirms RED phase
- `exitCode: 1` - Non-zero exit indicates failure
- `sampleErrors` - Include actual error messages

### Step 4: Implement Minimal Solution (GREEN Phase)

**Action**: Create the component with the minimal code needed to pass the test.

```vue
<!-- SearchBar.vue -->
<script setup lang="ts">
defineProps<{
  placeholder?: string;
}>();
</script>

<template>
  <UInput
    type="search"
    :placeholder="placeholder"
    leading-icon="i-lucide-search"
  />
</template>
```

**Critical Rules**:
- Implement ONLY what's needed to pass the current test
- Do NOT add untested props or functionality
- Keep it simple and minimal

### Step 5: Verify Test Passes (GREEN Phase Verification)

**Action**: Run tests again to confirm they pass.

```bash
pnpm test:storybook:run -- [ComponentName]
```

**Expected**: Test should now pass (GREEN).

### Step 6: Update test.json (GREEN Phase Tracking)

**Action**: Update test state to `"passed"` in test.json.

```json
{
  "tests": [
    {
      "name": "Default",
      "state": "passed",
      "note": "GREEN phase - basic SearchBar with search icon"
    }
  ]
}
```

### Step 7: Repeat for Next Test

**Action**: Return to Step 1 and add the NEXT test.

**Example Second Test**:
```typescript
export const Loading: Story = {
  args: {
    placeholder: 'Searching...',
    loading: true,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = await canvas.findByPlaceholderText(/searching/i);
    await expect(input).toBeInTheDocument();

    const container = input.parentElement;
    const spinner = container?.querySelector('[class*="i-lucide"][class*="loader-circle"]');
    await expect(spinner).toBeInTheDocument();
  },
};
```

Then repeat Steps 2-6 for this new test.

## NuxtUI Component Patterns

### Wrapping UInput

```vue
<script setup lang="ts">
defineProps<{
  placeholder?: string;
  loading?: boolean;
  disabled?: boolean;
}>();
</script>

<template>
  <UInput
    :placeholder="placeholder"
    :loading="loading"
    :disabled="disabled"
    type="search"
    leading-icon="i-lucide-search"
  />
</template>
```

### Wrapping UFormField + UInput

```vue
<script setup lang="ts">
defineProps<{
  label?: string;
  name?: string;
  placeholder?: string;
  required?: boolean;
}>();
</script>

<template>
  <UFormField :label="label" :name="name" :required="required">
    <UInput :placeholder="placeholder" :name="name" :required="required" />
  </UFormField>
</template>
```

### Common NuxtUI Props to Support

- `size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'` - Component size
- `color?: 'primary' | 'secondary' | 'success' | 'error'` - Color scheme
- `variant?: 'solid' | 'outline' | 'soft' | 'ghost'` - Visual style
- `loading?: boolean` - Loading state
- `disabled?: boolean` - Disabled state
- `required?: boolean` - Required field indicator

## Storybook Testing Patterns

### Finding Elements

```typescript
// By placeholder text
const input = await canvas.findByPlaceholderText(/search articles/i);

// By label text
const label = await canvas.findByLabelText(/email address/i);

// By text content
const error = await canvas.findByText(/valid email address/i);

// By role
const button = await canvas.findByRole('button', { name: /submit/i });
```

### Assertions

```typescript
// Element existence
await expect(input).toBeInTheDocument();

// Attribute checks
await expect(input).toHaveAttribute('required');
await expect(input).toHaveAttribute('type', 'search');

// Class checks (for icons/spinners)
const spinner = container?.querySelector('[class*="i-lucide"][class*="loader-circle"]');
await expect(spinner).toBeInTheDocument();
```

### Testing Icon/Spinner Presence

NuxtUI uses Iconify classes that require attribute selector patterns:

```typescript
// Correct: Use attribute selectors
const icon = container?.querySelector('[class*="i-lucide"][class*="search"]');

// Incorrect: Escaped colon syntax (will fail)
const icon = container?.querySelector('.iconify.i-lucide\\\\:search');
```

## Common Pitfalls and Solutions

### Pitfall 1: Adding Multiple Tests at Once

**Problem**: TDD guard blocks when trying to add multiple stories/tests simultaneously.

**Solution**: Add ONE test at a time, complete the full RED-GREEN cycle, then add the next test.

### Pitfall 2: Implementing Without RED Phase

**Problem**: TDD guard blocks implementation saying "missing failing test" even though test ran and failed.

**Solution**: Manually update test.json with RED phase evidence including exit code, failure count, and error messages.

### Pitfall 3: Over-Implementation

**Problem**: Adding props or features that aren't tested yet, guard blocks as "over-implementation."

**Solution**: Only implement what's needed for the current failing test. Add new tests for additional features.

### Pitfall 4: Storybook Hot Reload Issues

**Problem**: Tests continue failing after creating component file, showing "failed to fetch" errors.

**Solution**: Kill and restart Storybook server, wait for full rebuild before running tests.

### Pitfall 5: Vue Prop Forwarding vs Explicit Props

**Problem**: Some props (like `error`) work via Vue's automatic forwarding without explicit declaration.

**Solution**: Only add explicit prop declarations when tests require them. Leverage Vue's forwarding when appropriate.

## Test Organization

### Story File Structure

```typescript
import type { Meta, StoryObj } from '@storybook/vue3';
import { expect, within } from '@storybook/test';
import ComponentName from './ComponentName.vue';

const meta = {
  title: 'Molecules/ComponentName',  // Category/Name
  component: ComponentName,
  tags: ['autodocs'],
  argTypes: {
    // Define controls and descriptions
    propName: {
      control: 'text',
      description: 'Prop description',
    },
  },
} satisfies Meta<typeof ComponentName>;

export default meta;
type Story = StoryObj<typeof meta>;

// Story names use PascalCase
export const Default: Story = { ... };
export const WithError: Story = { ... };
export const Loading: Story = { ... };
```

### Story Naming Conventions

- **Default** - Basic usage with minimal props
- **With[Feature]** - Component with specific feature enabled (e.g., WithError, WithIcon)
- **[State]** - Component in specific state (e.g., Loading, Disabled, Required)
- **[Variant]** - Component variant (e.g., Outline, Soft, Ghost)

## Refactoring Phase

### When to Refactor

- After achieving GREEN phase
- When duplicate code appears
- When readability can be improved
- When TypeScript types need refinement

### What Can Be Refactored

- Code structure and organization
- Variable names and clarity
- TypeScript type definitions
- Component composition
- Duplicate logic extraction

### What Cannot Be Added During Refactor

- New props without tests
- New functionality without tests
- New behavior without tests
- Breaking changes without tests

## Success Criteria

A component is complete when:

1. **All planned tests pass** - 100% GREEN
2. **Component follows naming conventions** - Per NAMING_CONVENTIONS.md
3. **Props are properly typed** - TypeScript interfaces with JSDoc
4. **Stories are documented** - Storybook autodocs enabled
5. **Atomic design level is correct** - Proper categorization (atoms/molecules/organisms)

## Test Coverage Guidelines

### Minimum Test Coverage for Each Component

- **Atoms**: 2-3 tests (Default, Disabled, Loading/Error state)
- **Molecules**: 3-5 tests (Default, With[Feature], [State] variations)
- **Organisms**: 5-10 tests (Multiple features, interactions, edge cases)

### What to Test

1. **Basic rendering** - Component renders with default props
2. **Props effect** - Props change component appearance/behavior
3. **States** - Loading, disabled, error, empty, success states
4. **Interactions** - Click, focus, input, hover behaviors (if applicable)
5. **Validation** - Error messages, required fields, validation feedback
6. **Accessibility** - Proper ARIA attributes, keyboard navigation

## Running Tests

### Run All Storybook Tests

```bash
pnpm test:storybook:run
```

### Run Tests for Specific Component

```bash
pnpm test:storybook:run -- ComponentName
```

### Run Tests in Watch Mode (Development)

```bash
pnpm test:storybook
```

### Run Tests with Coverage

```bash
pnpm test:storybook:run --coverage
```

## TDD Workflow Checklist

For each new test:

- [ ] Create ONE test/story with focused assertion
- [ ] Run test and confirm failure (RED)
- [ ] Save failure output to temporary file
- [ ] Update test.json with RED phase evidence
- [ ] Implement minimal code to pass test
- [ ] Run test and confirm success (GREEN)
- [ ] Update test.json with GREEN phase
- [ ] Consider refactoring (optional)
- [ ] Repeat for next test

## Additional Resources

- See `references/naming-conventions.md` for component naming patterns
- See `assets/story-template.ts` for Storybook story template
- See `assets/component-template.vue` for Vue component template
- Refer to [NuxtUI Documentation](https://ui.nuxt.com/) for component props and patterns
- Refer to [Storybook Testing Docs](https://storybook.js.org/docs/vue/writing-tests/interaction-testing) for testing patterns
