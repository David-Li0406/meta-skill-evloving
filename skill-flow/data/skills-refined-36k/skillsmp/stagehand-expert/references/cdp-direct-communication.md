# Direct CDP Communication in Stagehand V3 (2026)

In V3, Stagehand has moved beyond Playwright to communicate directly with the browser using the Chrome DevTools Protocol (CDP).

## 1. Why direct CDP?

-   **Speed**: 44% increase in interaction velocity.
-   **Lower Overhead**: No intermediate library layers.
-   **Deep Access**: Native control over network interception, console logs, and low-level rendering events.

## 2. Managing iframes and Shadow DOM

Stagehand V3 automatically flattens iframe and shadow DOM boundaries using CDP's `DOM.getDocument` and `DOM.getFlattenedDocument` methods.
-   **Action**: No need to manually switch frames. Use the standard `act` or `extract` primitives and Stagehand will find the target regardless of depth.

## 3. Network Interception for AI Agents

Leverage CDP to block noisy network traffic before the agent sees the page.

```typescript
await stagehand.page.network.intercept({
  urlPattern: "*analytics*",
  action: "block"
});
```

## 4. Performance: The "Vibe" Score

Stagehand uses CDP to measure "Layout Stability" and "DOM Settle" in real-time.
-   *Rule*: The agent waits for a specific **Vibe Score** (LCP/CLS stability) before attempting an interaction to ensure high-fidelity element targeting.

## 5. Debugging with CDP Logs

If a tool call fails, inspect the raw CDP protocol logs in `stagehand_debug.log` to see exactly what message was sent to the browser.

---
*Updated: January 22, 2026 - 21:15*
