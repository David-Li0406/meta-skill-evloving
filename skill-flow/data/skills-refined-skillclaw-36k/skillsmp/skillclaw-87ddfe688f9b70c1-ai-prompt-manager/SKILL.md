---
name: ai-prompt-manager
description: Use this skill when managing AI prompts, features, and configurations in the KR92 Bible Voice AI system, including creating prompts, configuring features, and managing prompt versions.
---

# AI Prompt Manager

## Capabilities
- Create new AI prompt templates with proper structure.
- Generate prompt versions with variable substitution.
- Set up feature bindings (vendor/model/environment).
- Validate prompt syntax and output schemas.
- Configure AI pricing and usage tracking.

## Core Workflow
1. **Create feature** → Define the AI capability needed.
2. **Create prompt template** → Write system/user prompts with `{{variables}}`.
3. **Create prompt version** → Implement the template (allows versioning).
4. **Bind to environment** → Connect prompt to dev/stage/prod.
5. **Configure provider** → Choose vendor and model.
6. **Test via Admin panel** → Validate response and cost.

## Database Schema Reference

### AI Prompt Tables
```sql
ai_prompt_templates (task, name, description)
ai_prompt_versions (template_id, version, system_prompt, user_prompt_template, output_schema, model_hints, status)
ai_prompt_bindings (task, env, prompt_version_id, enabled)
```

### AI Feature Tables
```sql
ai_features (key, description)
ai_feature_bindings (feature_key, env, ai_vendor, ai_model, param_overrides, is_active)
ai_pricing (ai_vendor, ai_model, input_usd_per_1k, output_usd_per_1k)
ai_usage_logs (user_id, feature, ai_vendor, ai_model, tokens, cost_usd, status)
```

## Prompt Design

### Variable Substitution
Use `{{variable}}` syntax for dynamic content:
```javascript
system_prompt: "You are a {{role}} assistant for Bible study."
user_prompt_template: "Analyze: {{verse_reference}}"

// At call time
await getPrompt('my_feature', {
  role: 'theological scholar',
  verse_reference: 'John 3:16'
}, 'prod');
```

### Output Schema
Define expected output structure to validate responses:
```json
{
  "type": "object",
  "properties": {
    "summary": {"type": "string"},
    "insights": {
      "type": "array",
      "items": {"type": "string"}
    },
    "references": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

### Temperature & Tokens
- **Temperature**: 0.0–0.3 (factual), 0.4–0.7 (balanced), 0.8–1.0 (creative).
- **max_tokens**: Set based on expected output length:
  - Verse lookup: ~50 tokens.
  - Short analysis: ~200 tokens.
  - Full commentary: ~1000+ tokens.

## Vendor & Model Configuration
Supported vendors include `lovable`, `openai`, `anthropic`, and `openrouter`.