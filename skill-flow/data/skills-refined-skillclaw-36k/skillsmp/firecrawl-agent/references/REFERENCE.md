# Firecrawl Agent API Reference

This document provides detailed documentation for all parameters and options available in the Firecrawl Agent API.

## Overview

The Firecrawl Agent (`/agent` endpoint) is an autonomous web research agent that can search, navigate, and extract data from websites without requiring URLs upfront. It uses AI to understand queries and find relevant information across the web.

## API Endpoint

```
POST https://api.firecrawl.dev/v1/agent
```

## Authentication

All requests require an API key passed in the `Authorization` header:

```
Authorization: Bearer fc-your_api_key_here
```

Get your API key at: https://www.firecrawl.dev/

## Parameters

### Required Parameters

#### `prompt`
- **Type**: `string`
- **Max Length**: 10,000 characters
- **Description**: Natural language description of what you want to research or extract

**Examples**:
```
"Find the founders of Anthropic and when the company was founded"
"Compare the pricing of Notion, Coda, and Obsidian"
"Extract all product features from the Stripe website"
```

**Best Practices**:
- Be specific about what information you need
- Include context that helps narrow the search
- Mention specific aspects (founders, pricing, features, etc.)

### Optional Parameters

#### `model`
- **Type**: `string`
- **Options**: `"spark-1-mini"` | `"spark-1-pro"`
- **Default**: `"spark-1-mini"`
- **Description**: The AI model to use for the research task

| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| `spark-1-mini` | Faster | Lower | Simple queries, basic lookups |
| `spark-1-pro` | Slower | Higher | Complex research, multi-site analysis |

#### `schema`
- **Type**: `object` (JSON Schema)
- **Default**: `null`
- **Description**: JSON schema defining the structure of the output data

**Example Schema**:
```json
{
  "company_name": "string",
  "founded_year": "number",
  "founders": ["string"],
  "funding": {
    "total": "string",
    "latest_round": "string"
  }
}
```

**Supported Types**:
- `"string"` - Text values
- `"number"` - Numeric values (integers or floats)
- `"boolean"` - True/false values
- `["string"]` - Array of strings
- `[{"key": "type"}]` - Array of objects
- Nested objects for complex structures

#### `urls`
- **Type**: `array[string]`
- **Default**: `null`
- **Description**: Optional starting URLs to focus the agent's search

**Example**:
```json
["https://stripe.com", "https://stripe.com/pricing"]
```

**When to Use**:
- You know specific pages contain the information
- You want to focus on particular websites
- You're extracting data from known URLs

#### `maxCredits`
- **Type**: `integer`
- **Default**: Varies by plan
- **Description**: Maximum credits the agent can spend on this research task

**Credit Guidelines**:
- Simple queries: 10-25 credits
- Moderate research: 25-50 credits
- Complex analysis: 50-100+ credits

## Response Format

### Success Response

```json
{
  "success": true,
  "status": "completed",
  "data": {
    // Extracted data matching your schema (if provided)
    // Or unstructured research results
  },
  "sources": [
    "https://example.com/page1",
    "https://example.com/page2"
  ],
  "creditsUsed": 15
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `RATE_LIMITED` | Too many requests | Wait and retry |
| `CREDIT_LIMIT_EXCEEDED` | maxCredits limit reached | Increase limit or simplify query |
| `INVALID_SCHEMA` | Schema format is invalid | Check JSON syntax |
| `PROMPT_TOO_LONG` | Prompt exceeds 10,000 chars | Shorten the prompt |
| `UNAUTHORIZED` | Invalid API key | Check your API key |

## Rate Limits

| Plan | Requests/Minute | Daily Runs |
|------|-----------------|------------|
| Free | 5 | 5 |
| Starter | 20 | Unlimited |
| Growth | 50 | Unlimited |
| Enterprise | Custom | Unlimited |

## Pricing

- **Research Preview**: Pricing is dynamic based on complexity
- **Credit consumption**: Varies based on:
  - Number of pages visited
  - Complexity of extraction
  - Model used (pro uses more credits)

## Code Examples

### Python (using firecrawl-py)

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-your_key")

# Basic query
result = app.agent(
    prompt="Find the founders of Anthropic"
)

# With schema
result = app.agent(
    prompt="Find company information",
    schema={
        "name": "string",
        "founders": ["string"],
        "founded": "number"
    },
    model="spark-1-mini",
    maxCredits=50
)
```

### cURL

```bash
curl -X POST https://api.firecrawl.dev/v1/agent \
  -H "Authorization: Bearer fc-your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Find the founders of Anthropic",
    "model": "spark-1-mini",
    "maxCredits": 50
  }'
```

### JavaScript/TypeScript

```typescript
import Firecrawl from '@mendable/firecrawl-js';

const app = new Firecrawl({ apiKey: 'fc-your_key' });

const result = await app.agent({
  prompt: 'Find the founders of Anthropic',
  schema: {
    founders: ['string'],
    founded_year: 'number'
  }
});
```

## Best Practices

### Writing Effective Prompts

1. **Be specific**: "Find the pricing tiers for Notion" > "Find Notion info"
2. **Include context**: "Find Anthropic's Series B funding round details"
3. **List what you need**: "Find: founders, funding, employee count, products"

### Using Schemas Effectively

1. **Match data structure**: Design schemas that match expected data format
2. **Use arrays for lists**: `["string"]` for multiple values
3. **Nest for complex data**: Use objects within objects
4. **Keep it focused**: Only include fields you actually need

### Managing Costs

1. **Start with mini**: Use `spark-1-mini` first, upgrade to pro if needed
2. **Set credit limits**: Always set `maxCredits` to avoid surprises
3. **Provide URLs when known**: Reduces search time and credits
4. **Use schemas**: Structured output can be more efficient
