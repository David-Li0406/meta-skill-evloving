-- Query: Tag Performance Analysis
-- Purpose: Analyze which tags correlate with highest engagement
-- Parameters:
--   $1: start_date (timestamptz) - Period start, inclusive
--   $2: end_date (timestamptz) - Period end, exclusive
--   $3: on_behalf_of (text) - User name filter
-- Returns: Tags ranked by avg engagement, with video count and quality metrics

SELECT 
  unnest(va.tags) as tag,
  COUNT(*) as video_count,
  ROUND(AVG(ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count), 2) as avg_total_engagement,
  ROUND(AVG(ast.like_count + ast.heart_count + ast.laugh_count), 2) as avg_positive_engagement,
  SUM(ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count) as total_engagement,
  ROUND(AVG(va.quality_score), 3) as avg_quality_score,
  ROUND(AVG(va.motion_intensity), 3) as avg_motion_intensity
FROM civitai.video_analysis va
JOIN civitai.assets a ON va.asset_id = a.id
JOIN civitai.asset_stats ast ON ast.asset_id = a.id
WHERE 
  ast.civitai_created_at >= $1::timestamptz
  AND ast.civitai_created_at < $2::timestamptz
  AND ast.on_behalf_of = $3
  AND va.tags IS NOT NULL
GROUP BY tag
HAVING COUNT(*) >= 2
ORDER BY avg_positive_engagement DESC
LIMIT 30;
