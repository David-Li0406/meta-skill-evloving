---
name: testing-patterns
description: Guide for writing tests. Vitest for unit tests, Playwright for E2E. Includes SEO and sitemap testing patterns.
---

# Testing Patterns Skill

## Purpose

Guide for writing unit tests (Vitest) and E2E tests (Playwright) following project conventions.

## Test Stack

| Tool                  | Purpose                | Config                 |
| --------------------- | ---------------------- | ---------------------- |
| Vitest                | Unit/integration tests | `vitest.config.ts`     |
| React Testing Library | Component tests        | Via Vitest             |
| Playwright            | E2E tests              | `playwright.config.ts` |
| jsdom                 | DOM environment        | Vitest config          |

## Commands

```bash
yarn test              # Run all unit tests
yarn test:watch        # Watch mode
yarn test:coverage     # With coverage report
yarn test:e2e          # Playwright E2E tests
yarn test:e2e:ui       # Playwright with UI
```

## Unit Test Location & Naming

- Location: `test/**/*.{test,spec}.{ts,tsx}`
- Naming: `<feature>.test.ts` or `<component>.spec.tsx`

```text
test/
├── filter-system.test.ts
├── url-parsing.test.ts
├── mocks/
│   ├── next-intl.ts
│   └── next-intl-server.ts
└── setup.ts
```

## E2E Test Location

- Location: `e2e/**/*.spec.ts`
- Naming: `<feature>.flow.spec.ts` or `<feature>.spec.ts`

## Writing Unit Tests

### Basic Structure

```typescript
import { describe, it, expect, vi } from "vitest";

describe("featureName", () => {
  describe("functionName", () => {
    it("should do something specific", () => {
      // Arrange
      const input = "test";

      // Act
      const result = functionName(input);

      // Assert
      expect(result).toBe("expected");
    });
  });
});
```

### Testing Utilities/Functions

```typescript
import { describe, it, expect } from "vitest";
import { buildCanonicalUrlDynamic } from "@utils/url-filters";

describe("buildCanonicalUrlDynamic", () => {
  it("should omit tots for date and category", () => {
    expect(buildCanonicalUrlDynamic("barcelona", "tots", "tots")).toBe(
      "/barcelona"
    );
  });

  it("should include date when not tots", () => {
    expect(buildCanonicalUrlDynamic("barcelona", "avui", "tots")).toBe(
      "/barcelona/avui"
    );
  });
});
```

### Mocking with Vitest

```typescript
import { vi, describe, it, expect, beforeEach } from "vitest";

// Mock a module
vi.mock("@utils/api-helpers", () => ({
  fetchWithHmac: vi.fn(),
}));

import { fetchWithHmac } from "@utils/api-helpers";

describe("myFunction", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should call fetchWithHmac", async () => {
    vi.mocked(fetchWithHmac).mockResolvedValue({ data: [] });

    await myFunction();

    expect(fetchWithHmac).toHaveBeenCalledWith(
      expect.stringContaining("/api/events")
    );
  });
});
```

### Testing React Components

```typescript
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MyComponent } from "@components/ui/MyComponent";

describe("MyComponent", () => {
  it("should render title", () => {
    render(<MyComponent title="Hello" />);

    expect(screen.getByText("Hello")).toBeInTheDocument();
  });

  it("should handle click", async () => {
    const onClick = vi.fn();
    render(<MyComponent onClick={onClick} />);

    await userEvent.click(screen.getByRole("button"));

    expect(onClick).toHaveBeenCalled();
  });
});
```

## Mocking next-intl

The project has pre-built mocks for next-intl:

```typescript
// test/mocks/next-intl.ts - For client hooks
// test/mocks/next-intl-server.ts - For server functions

// vitest.config.ts aliases these automatically
// Just import normally in tests:
import { useTranslations } from "next-intl";
```

## Writing E2E Tests

### E2E Test Structure

```typescript
import { test, expect } from "@playwright/test";

test.describe("Feature Name", () => {
  test("should do something", async ({ page }) => {
    await page.goto("/barcelona");

    await expect(
      page.getByRole("heading", { name: "Barcelona" })
    ).toBeVisible();
  });
});
```

### Common Patterns

```typescript
// Wait for navigation
await page.waitForURL(/\/barcelona\/avui/);

// Click and wait
await page.getByRole("link", { name: "Events" }).click();
await page.waitForLoadState("networkidle");

// Fill form
await page.getByLabel("Search").fill("concert");
await page.getByRole("button", { name: "Search" }).click();

// Assert element count
const cards = page.locator('[data-testid="event-card"]');
await expect(cards).toHaveCount(10);

// Check URL params
expect(page.url()).toContain("search=concert");
```

### Testing Responsive

```typescript
test.describe("Mobile", () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test("should show mobile menu", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("button", { name: "Menu" })).toBeVisible();
  });
});
```

## Remote E2E Testing

For testing against deployed environments:

```bash
PLAYWRIGHT_TEST_BASE_URL=https://staging.example.com yarn test:e2e
```

Uses `playwright.remote.config.ts` configuration.

## SEO & Metadata Testing

### Testing generateMetadata

```typescript
import { generateMetadata } from "@app/[place]/page";

describe("Page Metadata", () => {
  it("should generate correct metadata for place page", async () => {
    const metadata = await generateMetadata({
      params: Promise.resolve({ place: "barcelona" }),
    });

    expect(metadata.title).toContain("Barcelona");
    expect(metadata.description).toBeDefined();
    expect(metadata.openGraph?.url).toContain("/barcelona");
  });

  it("should include canonical URL", async () => {
    const metadata = await generateMetadata({
      params: Promise.resolve({ place: "barcelona" }),
    });

    expect(metadata.alternates?.canonical).toBe(
      "https://www.esdeveniments.cat/barcelona"
    );
  });
});
```

### E2E: Testing SEO Elements

```typescript
test("should have correct SEO meta tags", async ({ page }) => {
  await page.goto("/barcelona");

  // Canonical URL
  const canonical = page.locator('link[rel="canonical"]');
  await expect(canonical).toHaveAttribute(
    "href",
    "https://www.esdeveniments.cat/barcelona"
  );

  // Open Graph
  const ogTitle = page.locator('meta[property="og:title"]');
  await expect(ogTitle).toHaveAttribute("content", /Barcelona/);

  const ogUrl = page.locator('meta[property="og:url"]');
  await expect(ogUrl).toHaveAttribute("content", /\/barcelona/);
});
```

### E2E: Testing JSON-LD

```typescript
test("should have valid JSON-LD structured data", async ({ page }) => {
  await page.goto("/barcelona");

  // Get JSON-LD script content
  const jsonLd = await page.evaluate(() => {
    const script = document.querySelector('script[type="application/ld+json"]');
    return script ? JSON.parse(script.textContent || "{}") : null;
  });

  expect(jsonLd).toBeDefined();
  expect(jsonLd["@type"]).toBe("ItemList");
  expect(jsonLd.itemListElement).toBeInstanceOf(Array);
});
```

### E2E: Testing hreflang

```typescript
test("should have correct hreflang tags", async ({ page }) => {
  await page.goto("/barcelona");

  // Check all locale variants
  const hreflangCa = page.locator('link[hreflang="ca"]');
  const hreflangEs = page.locator('link[hreflang="es"]');
  const hreflangEn = page.locator('link[hreflang="en"]');

  await expect(hreflangCa).toHaveAttribute("href", /\/barcelona/);
  await expect(hreflangEs).toHaveAttribute("href", /\/es\/barcelona/);
  await expect(hreflangEn).toHaveAttribute("href", /\/en\/barcelona/);
});
```

## Sitemap & RSS Testing

### E2E: Testing Sitemap

```typescript
test.describe("Sitemaps", () => {
  test("should return valid sitemap index", async ({ request }) => {
    const response = await request.get("/sitemap.xml");

    expect(response.status()).toBe(200);
    expect(response.headers()["content-type"]).toContain("xml");

    const body = await response.text();
    expect(body).toContain("<sitemapindex");
    expect(body).toContain("<sitemap>");
  });

  test("should include event URLs in server sitemap", async ({ request }) => {
    const response = await request.get("/server-sitemap.xml");

    expect(response.status()).toBe(200);
    const body = await response.text();
    expect(body).toContain("<urlset");
    expect(body).toContain("<loc>");
  });

  test("should have correct cache headers", async ({ request }) => {
    const response = await request.get("/server-sitemap.xml");

    const cacheControl = response.headers()["cache-control"];
    expect(cacheControl).toContain("s-maxage");
  });
});
```

### E2E: Testing robots.txt

```typescript
test("should have correct robots.txt", async ({ request }) => {
  const response = await request.get("/robots.txt");

  expect(response.status()).toBe(200);

  const body = await response.text();
  expect(body).toContain("Allow: /");
  expect(body).toContain("Disallow: /_next/");
  expect(body).toContain("Disallow: /api/");
  expect(body).toContain("Sitemap:");
});
```

### E2E: Testing RSS Feed

```typescript
test("should return valid RSS feed", async ({ request }) => {
  const response = await request.get("/rss.xml");

  expect(response.status()).toBe(200);
  expect(response.headers()["content-type"]).toContain("xml");

  const body = await response.text();
  expect(body).toContain("<rss");
  expect(body).toContain("<channel>");
  expect(body).toContain("<item>");
});
```

## Test Setup

The `test/setup.ts` file:

- Seeds `HMAC_SECRET` for HMAC utilities
- Sets up global test environment

## Coverage Requirements

- Aim for meaningful coverage on new code
- Run `yarn test:coverage` to check
- Focus on critical paths (filters, URLs, API calls)

## Checklist Before Writing Tests

- [ ] Unit test in `test/` directory?
- [ ] E2E test in `e2e/` directory?
- [ ] Using correct file naming convention?
- [ ] Mocking external dependencies?
- [ ] Testing both success and error cases?
- [ ] Running `yarn test` before committing?

## Files to Reference

- [vitest.config.ts](../../../vitest.config.ts) - Unit test configuration
- [playwright.config.ts](../../../playwright.config.ts) - E2E configuration
- [test/setup.ts](../../../test/setup.ts) - Test bootstrap
- [test/mocks/](../../../test/mocks/) - Mock implementations
- [test/filter-system.test.ts](../../../test/filter-system.test.ts) - Example unit tests
