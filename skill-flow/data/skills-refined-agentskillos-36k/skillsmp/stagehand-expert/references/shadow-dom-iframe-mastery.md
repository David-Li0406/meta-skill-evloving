# Shadow DOM and iframe Mastery (2026)

Handling encapsulated DOM structures is the biggest challenge in web automation. Stagehand V3 solves this via **DeepLocator**.

## 1. Boundary Jumping with `>>`

Use the `>>` operator to signal that Stagehand must cross a document boundary.

```typescript
// Jumping into a Shadow Root
await stagehand.act("Click 'Settings' inside #web-component >> .shadow-inner");
```

## 2. Global `observe` Across Boundaries

When you run `stagehand.observe()`, it recursively scans all accessible iframes and open shadow roots on the page.

## 3. Dealing with Restricted iframes

Some iframes (e.g., cross-origin Stripe components) have strict security policies.
-   **Solution**: Use `stagehand.agent({ cua: true })`. The CUA (Computer Use Agent) uses visual reasoning to find and interact with elements that are invisible to the DOM parser.

## 4. Flattening for Extraction

When using `extract()`, Stagehand creates a flattened semantic map of the entire page, merging data from all frames into a single Zod-validated object.

## 5. Performance Considerations

Scanning 50+ nested iframes is slow.
-   **Optimization**: Use a specific parent selector in your instruction to narrow the search scope.
-   *Good*: "Find the price inside #checkout-frame."

---
*Updated: January 22, 2026 - 21:15*
