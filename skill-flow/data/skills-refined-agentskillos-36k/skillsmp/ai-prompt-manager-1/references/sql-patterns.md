# AI Prompt SQL Patterns

Common SQL workflows for managing AI prompts, features, and bindings.

## Create New AI Feature

```sql
-- 1. Create feature
INSERT INTO bible_schema.ai_features (key, description)
VALUES ('feature_key', 'Feature description');

-- 2. Create prompt template
INSERT INTO bible_schema.ai_prompt_templates (task, name, description)
VALUES (
  'feature_key',
  'Display Name',
  'What this prompt does'
);

-- 3. Create prompt version
INSERT INTO bible_schema.ai_prompt_versions (
  template_id,
  version,
  system_prompt,
  user_prompt_template,
  output_schema,
  model_hints,
  status
) VALUES (
  (SELECT id FROM bible_schema.ai_prompt_templates WHERE task = 'feature_key'),
  1,
  'System instructions here...',
  'User prompt with {{variables}} here...',
  '{"type": "object", "properties": {"field": {"type": "string"}}}',
  '{"model_preference": "tier"}',
  'published'
);

-- 4. Bind to environment
INSERT INTO bible_schema.ai_prompt_bindings (task, env, prompt_version_id, enabled)
VALUES (
  'feature_key',
  'prod',
  (SELECT id FROM bible_schema.ai_prompt_versions WHERE template_id = (SELECT id FROM bible_schema.ai_prompt_templates WHERE task = 'feature_key') AND version = 1),
  true
);

-- 5. Configure feature binding
INSERT INTO bible_schema.ai_feature_bindings (
  feature_key,
  env,
  ai_vendor,
  ai_model,
  param_overrides,
  is_active
) VALUES (
  'feature_key',
  'prod',
  'vendor_name',
  'model_identifier',
  '{"temperature": 0.7, "max_tokens": 1000}',
  true
);
```

## Create New Prompt Version

```sql
-- Create new version
INSERT INTO bible_schema.ai_prompt_versions (
  template_id,
  version,
  system_prompt,
  user_prompt_template,
  output_schema,
  status
) VALUES (
  (SELECT id FROM bible_schema.ai_prompt_templates WHERE task = 'feature_key'),
  2,
  'Updated system prompt...',
  'Updated user prompt with {{variables}}...',
  '{"type": "object", "properties": {...}}',
  'draft'
);

-- Test in dev
UPDATE bible_schema.ai_prompt_bindings
SET prompt_version_id = (
  SELECT id FROM bible_schema.ai_prompt_versions
  WHERE template_id = (SELECT id FROM bible_schema.ai_prompt_templates WHERE task = 'feature_key')
  AND version = 2
)
WHERE task = 'feature_key' AND env = 'dev';

-- After testing, publish and promote to prod
UPDATE bible_schema.ai_prompt_versions
SET status = 'published'
WHERE template_id = (SELECT id FROM bible_schema.ai_prompt_templates WHERE task = 'feature_key')
AND version = 2;

UPDATE bible_schema.ai_prompt_bindings
SET prompt_version_id = (SELECT id FROM bible_schema.ai_prompt_versions WHERE template_id = (SELECT id FROM bible_schema.ai_prompt_templates WHERE task = 'feature_key') AND version = 2)
WHERE task = 'feature_key' AND env = 'prod';
```

## Switch AI Provider/Model

```sql
-- Update vendor and model for a feature
UPDATE bible_schema.ai_feature_bindings
SET
  ai_vendor = 'new_vendor',
  ai_model = 'new_model_id',
  param_overrides = '{"temperature": 0.7, "max_tokens": 2048}'
WHERE feature_key = 'feature_key' AND env = 'prod';

-- Ensure pricing is configured for the new vendor/model
INSERT INTO bible_schema.ai_pricing (ai_vendor, ai_model, input_usd_per_1k, output_usd_per_1k)
VALUES ('new_vendor', 'new_model_id', 0.001, 0.005)
ON CONFLICT (ai_vendor, ai_model) DO UPDATE
SET input_usd_per_1k = 0.001, output_usd_per_1k = 0.005;
```

## Query Current Configuration

```sql
-- View active feature configuration
SELECT
  f.key,
  f.description,
  fb.env,
  fb.ai_vendor,
  fb.ai_model,
  fb.param_overrides,
  fb.is_active
FROM bible_schema.ai_features f
LEFT JOIN bible_schema.ai_feature_bindings fb ON f.key = fb.feature_key
WHERE fb.is_active = true
ORDER BY f.key, fb.env;

-- View prompt versions and status
SELECT
  pt.task,
  pt.name,
  pv.version,
  pv.status,
  pb.env,
  pb.enabled
FROM bible_schema.ai_prompt_templates pt
LEFT JOIN bible_schema.ai_prompt_versions pv ON pt.id = pv.template_id
LEFT JOIN bible_schema.ai_prompt_bindings pb ON pv.id = pb.prompt_version_id
ORDER BY pt.task, pv.version DESC;

-- Check pricing for all active models
SELECT DISTINCT
  fb.ai_vendor,
  fb.ai_model,
  ap.input_usd_per_1k,
  ap.output_usd_per_1k,
  (ap.input_usd_per_1k + ap.output_usd_per_1k) AS total_cost_per_1k
FROM bible_schema.ai_feature_bindings fb
LEFT JOIN bible_schema.ai_pricing ap ON fb.ai_vendor = ap.ai_vendor AND fb.ai_model = ap.ai_model
WHERE fb.is_active = true
ORDER BY fb.ai_vendor, fb.ai_model;
```

## Monitor Usage

```sql
-- Check usage by feature and vendor
SELECT
  feature,
  ai_vendor,
  ai_model,
  COUNT(*) as call_count,
  SUM(tokens) as total_tokens,
  SUM(cost_usd) as total_cost,
  AVG(cost_usd) as avg_cost_per_call
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY feature, ai_vendor, ai_model
ORDER BY total_cost DESC;

-- Get user quota status
SELECT
  user_id,
  bible_schema.can_use_ai(user_id) as can_use,
  COUNT(*) as usage_count,
  SUM(cost_usd) as total_spent
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY user_id
HAVING COUNT(*) > 0
ORDER BY total_spent DESC;
```

## RLS & Access Control

All AI tables have RLS enabled. Typical access patterns:

```sql
-- Public read, admin write
SELECT * FROM bible_schema.ai_features;  -- All users can read

-- Authenticated read for usage logs (own data)
SELECT * FROM bible_schema.ai_usage_logs WHERE user_id = auth.uid();

-- Admin-only writes to prompt templates and bindings
INSERT INTO bible_schema.ai_prompt_templates...;  -- Admin only
```

See `Docs/context/security-matrix.md` for complete access matrix.
