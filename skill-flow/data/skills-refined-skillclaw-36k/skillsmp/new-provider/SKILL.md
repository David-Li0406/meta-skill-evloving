---
name: new-provider
description: Scaffold a new model provider for obot-tools
version: 1.0.0
author: AI Team
tags: [scaffold, obot, provider]
---

# New Model Provider

Create a new model provider following established patterns.

## When to Use

- Adding support for a new LLM provider (Anthropic, Mistral, etc.)
- Creating a custom model provider
- Understanding model provider structure

## Available Operations

1. **Scaffold**: Create directory structure from template
2. **Configure**: Set up tool.gpt and credentials
3. **Implement**: Write provider-specific code
4. **Test**: Validate the implementation

## Instructions

### Step 1: Gather Information

Required:

- Provider name (e.g., "anthropic", "mistral")
- API base URL
- Authentication method (API key, OAuth)

### Step 2: Copy Template

```bash
cp -r obot-tools/openai-model-provider obot-tools/{name}-model-provider
```

### Step 3: Update tool.gpt

See `references/tool-gpt-template.md` for format:

- Change `Name:` to `{Name} Model Provider`
- Update `Description:`
- Update credential if different auth method

### Step 4: Update Go Code

- Rename package
- Update API endpoint
- Adjust request/response mapping if API differs

### Step 5: Update index.yaml

Add to `modelProviders:` section:

```yaml
- name: {name}-model-provider
  description: {Name} model provider for Obot
  path: ./{name}-model-provider
```

### Step 6: Test

```bash
cd obot-tools/{name}-model-provider
export OBOT_{NAME}_MODEL_PROVIDER_API_KEY=...
go run . validate
```

## Resources

Load these Level 3 resources as needed:

- `references/tool-gpt-template.md` - GPTScript template for model providers
- `references/provider-patterns.md` - Common provider implementation patterns
- `assets/main.go.tmpl` - Go main.go template

## Examples

### Example: Anthropic Provider

**User asks:** "Create an Anthropic model provider"

**Response:**

1. Copy openai-model-provider
2. Update Name to "Anthropic Model Provider"
3. Update API endpoint to api.anthropic.com
4. Adjust message format for Claude API
5. Test with validate command

### Example: Mistral Provider

**User asks:** "Add Mistral AI support"

**Response:**

1. Copy openai-model-provider (Mistral is OpenAI-compatible)
2. Update Name to "Mistral Model Provider"
3. Update base URL to api.mistral.ai
4. Minimal code changes (OpenAI compatible)
5. Test with validate command

## Checklist

Before committing:

- [ ] tool.gpt has correct Name, Description, Tools
- [ ] Environment variable follows pattern: `OBOT_{NAME}_MODEL_PROVIDER_*`
- [ ] Implements OpenAI-compatible `/v1/chat/completions` endpoint
- [ ] Error responses are user-friendly
- [ ] Added to index.yaml
- [ ] Tested with `go run . validate`

## Notes

- Most providers follow OpenAI-compatible format
- Check if provider has OpenAI-compatible endpoint first
- Environment variables follow pattern: `OBOT_{NAME}_MODEL_PROVIDER_*`
