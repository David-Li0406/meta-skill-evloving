# AI Performance Monitoring

Tracking latency, costs, and cache effectiveness for AI features.

## Table of Contents
1. [Performance Metrics](#performance-metrics)
2. [Cost Analysis](#cost-analysis)
3. [Cache Effectiveness](#cache-effectiveness)
4. [Error Rate Tracking](#error-rate-tracking)

## Performance Metrics

Monitor AI call latency and performance (last 7 days):

```sql
SELECT
  feature,
  ai_vendor,
  ai_model,
  COUNT(*) as call_count,
  ROUND(AVG(latency_ms), 2) as avg_latency_ms,
  ROUND(MAX(latency_ms), 2) as max_latency_ms,
  ROUND(MIN(latency_ms), 2) as min_latency_ms,
  ROUND(AVG(total_tokens), 0) as avg_tokens,
  COUNT(CASE WHEN status = 'error' THEN 1 END) as errors,
  ROUND(100.0 * COUNT(CASE WHEN status = 'error' THEN 1 END) / COUNT(*), 2) as error_rate_percent
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY feature, ai_vendor, ai_model
ORDER BY call_count DESC;
```

## Cost Analysis

Track high-cost AI operations:

```sql
-- Total costs by feature (last 7 days)
SELECT
  feature,
  ai_model,
  COUNT(*) as call_count,
  ROUND(SUM(cost_usd), 4) as total_cost_usd,
  ROUND(AVG(cost_usd), 6) as avg_cost_per_call,
  ROUND(AVG(total_tokens), 0) as avg_tokens
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY feature, ai_model
ORDER BY total_cost_usd DESC;

-- Slowest AI calls (last 24 hours)
SELECT
  feature,
  ai_model,
  latency_ms,
  total_tokens,
  cost_usd,
  context_ref,
  created_at,
  status,
  error_message
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '24 hours'
  AND status = 'success'
ORDER BY latency_ms DESC
LIMIT 20;

-- High-cost AI calls
SELECT
  feature,
  ai_model,
  cost_usd,
  total_tokens,
  latency_ms,
  context_ref,
  created_at
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY cost_usd DESC
LIMIT 20;
```

## Cache Effectiveness

Measure cache hit rates for AI translations:

```sql
WITH cache_stats AS (
  SELECT
    COUNT(*) as total_requests,
    COUNT(CASE WHEN source IN ('topic', 'manual') THEN 1 END) as cache_hits,
    COUNT(CASE WHEN source = 'ai' THEN 1 END) as ai_calls
  FROM bible_schema.term_translations
  WHERE created_at > NOW() - INTERVAL '30 days'
)
SELECT
  total_requests,
  cache_hits,
  ai_calls,
  ROUND(100.0 * cache_hits / total_requests, 2) as cache_hit_rate_percent,
  ROUND(100.0 * ai_calls / total_requests, 2) as ai_call_rate_percent
FROM cache_stats;

-- Cache effectiveness by translation type
SELECT
  source,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percent
FROM bible_schema.term_translations
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY source
ORDER BY count DESC;
```

## Error Rate Tracking

Monitor AI call failures and patterns:

```sql
-- Recent AI errors
SELECT
  feature,
  ai_model,
  status,
  error_message,
  COUNT(*) as error_count,
  MAX(created_at) as last_occurrence
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '24 hours'
  AND status != 'success'
GROUP BY feature, ai_model, status, error_message
ORDER BY error_count DESC
LIMIT 20;

-- Error rate by model
SELECT
  ai_model,
  COUNT(*) as total_calls,
  COUNT(CASE WHEN status = 'error' THEN 1 END) as error_count,
  ROUND(100.0 * COUNT(CASE WHEN status = 'error' THEN 1 END) / COUNT(*), 2) as error_rate_percent
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY ai_model
ORDER BY error_rate_percent DESC;
```

## Optimization Strategies

### Caching Layer
- Cache translation results in `term_translations` table
- Use `source` field to track cache vs AI-generated
- Monitor cache hit rate; low rates indicate need for warmup queries

### Model Selection
- Use cheaper models (Claude Haiku) for simple translations
- Reserve Claude Opus for complex tasks requiring reasoning
- Track cost per feature to justify model selection

### Token Limits
- Set `max_tokens` appropriately per feature
- Monitor `total_tokens` to identify runaway requests
- Implement request validation before calling AI

### Timeout Handling
- Set reasonable timeouts (default 30s for API calls)
- Implement retry logic with exponential backoff
- Log timeout events to identify systemic issues

### Batch Processing
- Batch multiple translation requests in single API call
- Use `BATCH_TRANSLATE` endpoint if available
- Monitor for diminishing returns (batch size vs latency)
