---
name: search-model
description: Search OpenRouter API for AI models and get pricing/capability details for model-reference.md
---

# Search OpenRouter Models

Search the OpenRouter API for AI models and retrieve detailed information including pricing, context length, and capabilities. Use this to research models before adding them to `docs/model-reference.md`.

## Instructions

### 1. Fetch all models from OpenRouter

```bash
curl -s https://openrouter.ai/api/v1/models | jq '.'
```

This returns a JSON object with a `data` array containing all available models.

### 2. Search for specific models

```bash
# Search by provider (e.g., anthropic, openai, google)
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | select(.id | contains("anthropic"))'

# Search by model name (e.g., claude, gpt, gemini)
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | select(.id | contains("claude"))'

# Get specific model by exact ID
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | select(.id == "anthropic/claude-opus-4.5")'
```

### 3. Extract key information

For each model, the API returns:

```json
{
  "id": "anthropic/claude-opus-4.5",
  "name": "Claude Opus 4.5",
  "description": "Anthropic's most capable model...",
  "context_length": 200000,
  "pricing": {
    "prompt": "0.000015", // Price per token (input)
    "completion": "0.000075" // Price per token (output)
  },
  "top_provider": {
    "context_length": 200000,
    "is_moderated": false
  }
}
```

### 4. Calculate pricing in standard format

Convert per-token pricing to per-1M tokens for documentation:

```bash
# Get model and calculate pricing
MODEL_ID="anthropic/claude-opus-4.5"
curl -s https://openrouter.ai/api/v1/models | jq --arg id "$MODEL_ID" '
  .data[]
  | select(.id == $id)
  | {
      id: .id,
      name: .name,
      description: .description,
      context_length: .context_length,
      pricing_per_1m: {
        input: (.pricing.prompt | tonumber * 1000000),
        output: (.pricing.completion | tonumber * 1000000)
      }
    }
'
```

### 5. Compare multiple models

```bash
# Compare all Claude 4.5 models
curl -s https://openrouter.ai/api/v1/models | jq '
  [.data[] | select(.id | contains("claude") and contains("4.5"))]
  | map({
      id: .id,
      name: .name,
      input_per_1m: (.pricing.prompt | tonumber * 1000000),
      output_per_1m: (.pricing.completion | tonumber * 1000000),
      context: .context_length
    })
  | sort_by(.input_per_1m)
'
```

## Output Format for model-reference.md

When you find a model to add, format it like this:

```markdown
### openrouter:provider/model-name

**Name:** Model Display Name

**Description:** [1-2 sentences about the model's strengths]

**Typical cost:** ~$X.XX per 1M input tokens, ~$X.XX per 1M output tokens

**When to use:**

- Use case 1
- Use case 2
- Use case 3

**Use instead of:** `older-model-1`, `older-model-2`
```

**Note:** OpenRouter uses simple version numbers (e.g., `claude-sonnet-4.5`), NOT date-suffixed versions (e.g., `claude-sonnet-4-20250514`).

## Examples

**Find all Claude models with pricing:**

```bash
curl -s https://openrouter.ai/api/v1/models | jq '
  [.data[] | select(.id | contains("anthropic/claude"))]
  | map({
      id: .id,
      name: .name,
      input_per_1m: ((.pricing.prompt | tonumber) * 1000000 | round),
      output_per_1m: ((.pricing.completion | tonumber) * 1000000 | round)
    })
  | sort_by(.input_per_1m)
'
```

**Get details for a specific model:**

```bash
MODEL="anthropic/claude-opus-4.5"
curl -s https://openrouter.ai/api/v1/models | jq --arg m "$MODEL" '
  .data[]
  | select(.id == $m)
  | {
      id,
      name,
      description,
      context: .context_length,
      "pricing (per 1M tokens)": {
        input: ((.pricing.prompt | tonumber) * 1000000),
        output: ((.pricing.completion | tonumber) * 1000000)
      }
    }
'
```

**Compare OpenAI vs Claude pricing:**

```bash
curl -s https://openrouter.ai/api/v1/models | jq '
  [.data[] | select(.id | test("openai/gpt-4|anthropic/claude-.*-4"))]
  | map({
      id: .id,
      input_cost: ((.pricing.prompt | tonumber) * 1000000 | round),
      output_cost: ((.pricing.completion | tonumber) * 1000000 | round)
    })
  | sort_by(.input_cost)
'
```

## Common Use Cases

**Finding the cheapest Claude model:**

```bash
curl -s https://openrouter.ai/api/v1/models | jq '
  [.data[] | select(.id | contains("anthropic/claude-"))]
  | sort_by(.pricing.prompt | tonumber)
  | first
  | {id, name, input_per_1m: ((.pricing.prompt | tonumber) * 1000000)}
'
```

**Checking if a model exists:**

```bash
MODEL="anthropic/claude-opus-4.5"
curl -s https://openrouter.ai/api/v1/models | jq --arg m "$MODEL" '
  .data[] | select(.id == $m) | .id
'
```

**Finding all embedding models:**

```bash
curl -s https://openrouter.ai/api/v1/models | jq '
  [.data[] | select(.id | contains("embedding"))]
  | map({id, name, pricing: .pricing})
'
```

## Tips

1. **Save results to file** if doing multiple queries:

   ```bash
   curl -s https://openrouter.ai/api/v1/models > /tmp/openrouter-models.json
   cat /tmp/openrouter-models.json | jq '.data[] | select(.id | contains("claude"))'
   ```

2. **Check model availability** before adding to model-reference.md

3. **Round pricing** to 2 decimal places for readability:

   ```bash
   jq '(.pricing.prompt | tonumber * 1000000 * 100 | round / 100)'
   ```

4. **Model ID format** in model-reference.md is always `openrouter:provider/model-name`

## After Finding a Model

1. Note the exact model ID (e.g., `anthropic/claude-opus-4.5`)
2. Calculate pricing per 1M tokens
3. Read the description to understand use cases
4. Manually add entry to `docs/model-reference.md` using the format above
5. Consider what older models it should replace (add to "Use instead of")
6. Update the "Last updated" date in model-reference.md
