-- Query: Content Theme Analysis
-- Purpose: Analyze video themes from descriptions and inferred prompts
-- Parameters:
--   $1: start_date (timestamptz) - Period start, inclusive
--   $2: end_date (timestamptz) - Period end, exclusive
--   $3: on_behalf_of (text) - User name filter
-- Returns: Videos with full content details for theme/pattern analysis

SELECT 
  a.civitai_id,
  'https://civitai.com/images/' || a.civitai_id AS civitai_url,
  va.description,
  va.inferred_prompt,
  va.tags,
  va.quality_score,
  va.motion_intensity,
  va.nsfw_score,
  va.duration_seconds,
  ast.like_count,
  ast.heart_count,
  ast.laugh_count,
  ast.comment_count,
  (ast.like_count + ast.heart_count + ast.laugh_count) as positive_engagement,
  (ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count) as total_engagement,
  ast.civitai_created_at,
  ROW_NUMBER() OVER (ORDER BY (ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count) DESC) as engagement_rank
FROM civitai.assets a
JOIN civitai.video_analysis va ON va.asset_id = a.id
JOIN civitai.asset_stats ast ON ast.asset_id = a.id
WHERE 
  a.asset_type = 'video'
  AND ast.civitai_created_at >= $1::timestamptz
  AND ast.civitai_created_at < $2::timestamptz
  AND ast.on_behalf_of = $3
ORDER BY total_engagement DESC
LIMIT 50;
