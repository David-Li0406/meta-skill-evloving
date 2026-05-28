# Context Caching: Optimizing Long-Form Context (2026)

Context Caching is a game-changer for applications dealing with large codebases, long videos, or massive document sets. It reduces latency and cost for repeated queries over the same data.

## 1. How it Works

Instead of sending 1 million tokens with every request, you upload the tokens once, create a cache, and then reference that cache in subsequent requests.

-   **Persistence**: Caches are typically stored for a few hours (TTL) and can be refreshed.
-   **Minimum Size**: Caching is most effective for contexts larger than 32,000 tokens.

## 2. Implementation Flow

### Step 1: Create the Cache
```typescript
const cache = await client.createContextCache({
  model: "gemini-3-pro",
  contents: [
    { role: "user", parts: [{ text: "Here is the entire codebase context..." }] }
  ],
  ttlSeconds: 3600 // 1 hour
});
```

### Step 2: Use the Cache
```typescript
const result = await model.generateContent({
  contents: [{ role: "user", parts: [{ text: "Find the bug in the auth flow." }] }],
  cachedContent: cache.name
});
```

## 3. Cost Analysis (2026 Tiers)

-   **Storage Fee**: Based on the number of tokens cached per hour.
-   **Processing Fee**: A reduced rate compared to standard token input.
-   **Efficiency**: If you make >5 queries on the same context, caching pays for itself.

## 4. Best Practices

-   **Shared Caches**: Use a single cache for multiple users if they are querying the same dataset (e.g., a shared PDF library).
-   **TTL Management**: Set short TTLs for dynamic data and long TTLs for static references (e.g., historical archives).
-   **Warm-up**: For ultra-low latency, "warm" the cache by performing a dummy query immediately after creation.

## 5. Limitations

-   **Model Specific**: Caches are tied to a specific model version. Upgrading the model requires re-caching.
-   **Token Limit**: While context windows are 2M+, caches also have upper limits (check your quota).

---
*Updated: January 22, 2026 - 17:15*
