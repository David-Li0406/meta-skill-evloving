# AI Provider Configuration

Configuration guide for AI vendors and model selection.

## Supported Vendor Endpoints

| Vendor | Endpoint | Configuration |
|--------|----------|----------------|
| `lovable` | ai.gateway.lovable.dev | Internal gateway routing various models |
| `openai` | api.openai.com | OpenAI models via official API |
| `anthropic` | api.anthropic.com | Anthropic models via official API |
| `openrouter` | openrouter.ai | Model aggregator with fallback support |

## Model Selection Strategy

Choose vendors and models based on:

1. **Task Type**
   - **Factual/Bible content**: Lower temperature, deterministic models
   - **Creative analysis**: Higher temperature, reasoning-capable models
   - **Code/structured output**: Models with strong JSON schema support

2. **Cost Optimization**
   - Check current pricing in `ai_pricing` table
   - Use cheaper models for simple tasks (classification, lookup)
   - Reserve higher-tier models for complex reasoning

3. **Latency Requirements**
   - Simple tasks: Use faster inference providers
   - User-facing features: Prioritize low latency
   - Batch/background: Can use slower, cheaper options

4. **Availability & Fallbacks**
   - Configure feature bindings per environment (dev/stage/prod)
   - Use OpenRouter for automatic fallback chains
   - Test model availability in dev environment first

## Parameter Configuration

### Temperature
- **0.0-0.3**: Deterministic, factual (Bible verse lookup, terminology)
- **0.4-0.7**: Balanced (analysis, summaries, suggestions)
- **0.8-1.0**: Creative, variable (commentary, interpretation)

### Token Limits

Define `max_tokens` based on expected output:

```javascript
// Guidance for token counting
// Typical Bible content
- Single verse: ~50 tokens
- Verse comparison: ~200 tokens
- Chapter analysis: ~500 tokens
- Full commentary: ~1000+ tokens
```

### Supported Parameter Keys

Check vendor documentation for latest parameters. Common ones:

```javascript
// Most vendors support
{
  "temperature": 0.7,
  "max_tokens": 1000,
  "top_p": 0.9
}

// Some newer models may use different naming
// Refer to vendor API docs when configuring
```

## Environment Strategy

1. **dev** - Experimental prompts, test new vendors
2. **stage** - Pre-production testing, validate cost estimates
3. **prod** - Stable, cost-optimized features

Always follow: dev → stage → prod progression.

## Configuring New Vendor/Model

1. Add credentials to Supabase secrets
2. Insert pricing into `ai_pricing` table
3. Create feature binding in `ai_feature_bindings` with test environment
4. Test via Admin panel (Testaus tab)
5. Validate cost tracking in `ai_usage_logs`
6. Promote to prod after validation

## Cost Monitoring

Query `ai_usage_logs` to track spending:

```sql
SELECT
  ai_vendor,
  ai_model,
  COUNT(*) as calls,
  SUM(tokens) as total_tokens,
  SUM(cost_usd) as total_cost
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY ai_vendor, ai_model
ORDER BY total_cost DESC;
```

See `references/sql-patterns.md` for more queries.

## Fallback Strategy

For critical features, configure multiple providers:

```sql
-- Primary in prod
UPDATE bible_schema.ai_feature_bindings
SET ai_vendor = 'primary_vendor', ai_model = 'primary_model'
WHERE feature_key = 'critical_feature' AND env = 'prod';

-- Configure fallback via OpenRouter or similar
UPDATE bible_schema.ai_feature_bindings
SET ai_vendor = 'openrouter', ai_model = 'fallback_model_chain'
WHERE feature_key = 'critical_feature_fallback' AND env = 'prod';
```

## Related Documentation

- **Pricing & usage**: Check `Docs/context/db-schema-short.md` for schema details
- **Testing features**: Use Admin panel → Testaus tab
- **Cost optimization**: See subscription-system skill for quota enforcement
- **Current configuration**: Query `ai_features` and `ai_feature_bindings` tables
