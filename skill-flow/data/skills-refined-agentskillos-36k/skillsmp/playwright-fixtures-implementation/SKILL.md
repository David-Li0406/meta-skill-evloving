---
name: playwright-fixtures-implementation
description: Guide for creating and using Playwright fixtures for E2E testing. Use when implementing test utilities or Page Object Models.
---

# Playwright Fixtures Implementation Skill

Guide for creating and using Playwright fixtures for E2E testing with Nuxt hydration handling.

## Purpose

USE this skill when:
- Creating reusable test utilities
- Implementing Page Object Models
- Setting up test fixtures for features
- Need Nuxt-specific testing patterns

## Core Principles

- USE Playwright's `test.extend()` API for reusable utilities
- IMPLEMENT Page Object Models as fixtures, not standalone classes
- ALWAYS import `test` and `expect` from `tests/fixtures/index.ts`
- ADD data-testid attributes during component development

## Fixture Organization

```
tests/
├── fixtures/
│   ├── index.ts              # Merged fixtures (import from here)
│   ├── auth-fixtures.ts      # Authentication utilities
│   ├── speakers-fixtures.ts  # Feature utilities
│   └── test-accounts.json    # Test data
├── e2e/
│   └── speakers.spec.ts      # Import from "../fixtures"
```

## Import Pattern (CRITICAL)

```typescript
// ✅ Correct: Import from merged fixtures
import { test, expect } from "../fixtures"

// ❌ Wrong: Direct import bypasses custom fixtures
import { test, expect } from "@playwright/test"
```

## Creating Fixtures

### Basic Fixture

```typescript
// tests/fixtures/speakers-fixtures.ts
import { test as base } from "@playwright/test"

export const test = base.extend({
  speakersPage: async ({ page }, use) => {
    await page.goto("http://localhost:3000/speakers")
    await page.waitForLoadState("networkidle")
    await use(page)
  },
})

export { expect } from "@playwright/test"
```

### Page Object Model Fixture

```typescript
// tests/fixtures/speakers-fixtures.ts
class SpeakersPage {
  constructor(public readonly page: Page) {}

  async goto() {
    await this.page.goto("http://localhost:3000/speakers")
    await this.page.waitForLoadState("networkidle")
  }

  async createSpeaker(data: { firstName: string; lastName: string }) {
    await this.page.getByTestId("speakers-create-button").click()
    await this.page.getByTestId("speaker-first-name-input").fill(data.firstName)
    await this.page.getByTestId("speaker-last-name-input").fill(data.lastName)
    await this.page.getByTestId("speaker-submit-button").click()
  }

  async getSpeakerCard(name: string) {
    return this.page.getByTestId("speaker-card").filter({ hasText: name })
  }
}

export const test = base.extend<{ speakersPage: SpeakersPage }>({
  speakersPage: async ({ page }, use) => {
    const speakersPage = new SpeakersPage(page)
    await speakersPage.goto()
    await use(speakersPage)
  },
})
```

## Merging Fixtures

### index.ts Pattern

```typescript
// tests/fixtures/index.ts
import { mergeTests, mergeExpects } from "@playwright/test"
import { test as authTest, expect as authExpect } from "./auth-fixtures"
import { test as speakersTest, expect as speakersExpect } from "./speakers-fixtures"

export const test = mergeTests(authTest, speakersTest)
export const expect = mergeExpects(authExpect, speakersExpect)
```

## Nuxt Hydration Handling

### Auto-Wait Fixture

```typescript
// tests/fixtures/nuxt-fixtures.ts
import { test as base } from "@playwright/test"

export const test = base.extend({
  page: async ({ page }, use) => {
    // Extend page with Nuxt-aware navigation
    const originalGoto = page.goto.bind(page)
    page.goto = async (url, options) => {
      const response = await originalGoto(url, options)
      await page.waitForLoadState("networkidle")
      await page.waitForFunction(() => window.__NUXT__?.isHydrating === false)
      return response
    }
    await use(page)
  },
})
```

## Test Selector Strategy

### data-testid Requirements

```vue
<!-- Component -->
<template>
  <UCard data-testid="speaker-card">
    <UButton
      data-testid="speaker-edit-button"
      @click="handleEdit" />
    <UButton
      data-testid="speaker-delete-button"
      @click="handleDelete" />
  </UCard>
</template>
```

### Using in Tests

```typescript
// tests/e2e/speakers.spec.ts
import { test, expect } from "../fixtures"

test("edit speaker", async ({ speakersPage }) => {
  await speakersPage.page.getByTestId("speaker-edit-button").first().click()
  await speakersPage.page.getByTestId("speaker-first-name-input").fill("Updated")
  await speakersPage.page.getByTestId("speaker-submit-button").click()
  
  await expect(
    speakersPage.page.getByTestId("speaker-card")
  ).toContainText("Updated")
})
```

## Naming Convention

- USE kebab-case: `{feature}-{element}-{type}`
- EXAMPLES:
  - `speakers-create-button`
  - `speaker-first-name-input`
  - `speaker-card`
  - `talk-schedule-dialog`

## Anti-Patterns

❌ Importing from @playwright/test directly
❌ Using CSS classes or text as selectors
❌ Not waiting for Nuxt hydration
❌ Creating standalone Page Object classes (use fixtures)
❌ Forgetting data-testid attributes

## References

- Full patterns: `.agents/e2e-testing-patterns.md`
- Test checklist: `.agents/test-ready-component-checklist.md`
