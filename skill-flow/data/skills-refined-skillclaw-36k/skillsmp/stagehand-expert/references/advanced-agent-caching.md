# Advanced Agent Caching and Determinism (2026)

Caching is the key to cost-effective and ultra-fast E2E testing in 2026. Stagehand V3 introduces persistent decision caches.

## 1. The Decision Store

Stagehand caches LLM decisions for specific DOM snapshots.
-   **Structure**: A JSON map of `hash(DOM + Instruction) -> LLM Result`.
-   **Benefit**: Re-running the same test costs 0 tokens and completes in milliseconds.

## 2. Token Optimization via Context Builder

V3 uses a "Smart Context Builder" that only sends the minimal required DOM tree to the AI.
-   **Pruning**: Automatically removes scripts, styles, and non-visible elements.
-   **Semantic Compression**: Replaces long class names with short identifiers.

## 3. CI/CD Integration: The "Zero-LLM" Mode

1.  **Develop**: Run tests locally with a live LLM to generate the cache.
2.  **Commit**: Upload the `./cache/e2e` directory to Git.
3.  **Validate**: In CI, Stagehand runs in "Cached-Only" mode. If a cache miss occurs, the test fails, indicating a UI regression.

## 4. Cache Invalidation Patterns

-   **Manual**: `rm -rf ./cache`.
-   **Automated**: Invalidate specific entries based on CSS selector changes or version tags.

## 5. Security: Scrubbing the Cache

Ensure that PII (Passwords, Keys) are never saved in the cache files.
-   **Protocol**: Use `stagehand.act("...", { variables: { password: process.env.PWD } })`. Stagehand will mask the variable in the cache.

---
*Updated: January 22, 2026 - 21:15*
