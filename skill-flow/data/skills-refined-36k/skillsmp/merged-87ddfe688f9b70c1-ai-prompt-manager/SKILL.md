---
name: ai-prompt-manager
description: Use this skill when managing AI prompts, features, and configurations in the KR92 Bible Voice AI system, including creating templates, versions, and bindings across multiple vendors and models.
---

# AI Prompt Manager

## Capabilities
- Create new AI prompt templates with proper structure
- Generate prompt versions with variable substitution
- Set up feature bindings (vendor/model/environment)
- Validate prompt syntax and output schemas
- Configure AI pricing and usage tracking

## Quick Start

### Core Workflow
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

## Prompt Variable Substitution

Use `{{variable}}` syntax in prompts:

```javascript
// System prompt
"You are a {{role}} assistant. Translate from {{source_language}} to {{target_language}}."

// User prompt template
"Translate: {{term}}"

// Edge Function usage
const prompt = await getPrompt('translate_search_term', {
  role: 'theological translation',
  term: 'armo',
  source_language: 'Finnish',
  target_language: 'English'
}, 'prod');
```

## Supported AI Providers

| Vendor     | Endpoint              | Models                             |
|------------|-----------------------|------------------------------------|
| `lovable`  | ai.gateway.lovable.dev| google/gemini-2.5-flash, openai/gpt-4o |
| `openai`   | api.openai.com        | gpt-4o, gpt-4o-mini, o1, o3       |
| `anthropic`| api.anthropic.com     | claude-3-5-sonnet, claude-3-5-haiku |
| `openrouter`| openrouter.ai       | Various models                     |

## Model Parameter Guidelines

### Newer Models (GPT-5, O3, O4)
- Use `max_completion_tokens` (not `max_tokens`)
- No `temperature` parameter
- Example: `{"max_completion_tokens": 1000}`

### Legacy Models (GPT-4o, Gemini)
- Use `max_tokens`
- Support `temperature`
- Example: `{"max_tokens": 1000, "temperature": 0.7}`

## Environment Strategy

1. **dev** - Experimental prompts and features.
2. **stage** - Testing before production.
3. **prod** - Live user-facing features.

Always test in dev → stage → prod progression.

## Prompt Best Practices

1. **Clear instructions** - Be specific about the task.
2. **JSON output** - Define explicit output schema.
3. **Variable names** - Use descriptive `{{variable}}` names.
4. **Examples** - Include examples in system prompt when possible.
5. **Context** - Provide enough context for accurate responses.
6. **Token limits** - Set appropriate `max_tokens` for the task.
7. **Temperature** - Lower (0.3-0.5) for factual, higher (0.7-0.9) for creative.

## Cost Optimization

1. Use cheaper models (gemini-2.5-flash) for simple tasks.
2. Cache AI responses in `term_translations` table.
3. Set reasonable `max_tokens` limits.
4. Monitor usage in `ai_usage_logs`.
5. Use fallback prompts for critical features.

## Testing AI Features

Use the Admin AI page → Testaus tab:
1. Select feature.
2. Input test variables.
3. Review response, tokens, cost.
4. Iterate on prompt if needed.

## Related Documentation
- See `Docs/06-AI-ARCHITECTURE.md` for AI system details.
- See `Docs/context/db-schema-short.md` for database schema details.
- See `Docs/context/supabase-map.md` for Edge Functions & access matrix.