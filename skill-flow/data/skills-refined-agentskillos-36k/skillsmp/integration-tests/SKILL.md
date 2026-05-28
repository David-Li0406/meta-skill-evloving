---
name: integration-tests
description: Use this skill when writing or running integration tests. Provides approved model names and integration test guidelines.
---

# Integration Test Guidelines

Guidelines for writing and running integration tests that make real API calls.

## Approved Models

Use these models for integration tests:

| Provider | Model Name | API Key Env Var |
|----------|------------|-----------------|
| Anthropic | `claude-haiku-4-5-20251001` | `ANTHROPIC_API_KEY` |
| OpenAI | `gpt-5-mini` | `OPENAI_API_KEY` |
| Google | `gemini-3-flash` | `GOOGLE_API_KEY` |

### Why These Models?

- **Fast**: Optimized for low latency
- **Cost-effective**: Cheapest tier for each provider
- **Capable**: Still highly capable for test scenarios

## Writing Integration Tests

### Example Vibe Code

```vibe
// Anthropic
model anthropic = { name: "claude-haiku-4-5-20251001", apiKey: env("ANTHROPIC_API_KEY") }

// OpenAI
model openai = { name: "gpt-5-mini", apiKey: env("OPENAI_API_KEY") }

// Google
model google = { name: "gemini-3-flash", apiKey: env("GOOGLE_API_KEY") }
```

### Test File Location

Integration tests live in: `tests/integration/`

### Running Integration Tests

```bash
# Run all integration tests (costs money, ~40s)
bun run test:integration

# Run a single integration test
bun test tests/integration/specific-test.test.ts
```

## Important Notes

1. **Do NOT run full integration suite routinely** - it costs money
2. **Use unit tests first** - `bun run test` is fast and free
3. **Run targeted integration tests** when verifying specific provider behavior
4. **Update model names** when providers release new versions
