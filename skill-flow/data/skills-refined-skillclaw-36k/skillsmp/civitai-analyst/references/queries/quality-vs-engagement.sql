-- Query: Quality Score vs Engagement Analysis
-- Purpose: Analyze correlation between quality_score and engagement
-- Parameters:
--   $1: start_date (timestamptz) - Period start, inclusive
--   $2: end_date (timestamptz) - Period end, exclusive
--   $3: on_behalf_of (text) - User name filter
-- Returns: Quality score buckets with avg engagement, identifies optimal ranges

WITH video_metrics AS (
  SELECT 
    va.quality_score,
    va.motion_intensity,
    (ast.like_count + ast.heart_count + ast.laugh_count) as positive_engagement,
    (ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count) as total_engagement,
    CASE 
      WHEN va.quality_score >= 0.9 THEN '0.90-1.00 (Excellent)'
      WHEN va.quality_score >= 0.8 THEN '0.80-0.89 (Very Good)'
      WHEN va.quality_score >= 0.7 THEN '0.70-0.79 (Good)'
      WHEN va.quality_score >= 0.6 THEN '0.60-0.69 (Fair)'
      WHEN va.quality_score >= 0.5 THEN '0.50-0.59 (Average)'
      ELSE '0.00-0.49 (Below Average)'
    END as quality_bucket
  FROM civitai.video_analysis va
  JOIN civitai.assets a ON va.asset_id = a.id
  JOIN civitai.asset_stats ast ON ast.asset_id = a.id
  WHERE 
    a.asset_type = 'video'
    AND ast.civitai_created_at >= $1::timestamptz
    AND ast.civitai_created_at < $2::timestamptz
    AND ast.on_behalf_of = $3
    AND va.quality_score IS NOT NULL
)
SELECT 
  quality_bucket,
  COUNT(*) as video_count,
  ROUND(AVG(quality_score), 3) as avg_quality_score,
  ROUND(AVG(motion_intensity), 3) as avg_motion_intensity,
  ROUND(AVG(positive_engagement), 2) as avg_positive_engagement,
  ROUND(AVG(total_engagement), 2) as avg_total_engagement,
  SUM(total_engagement) as sum_total_engagement,
  ROUND(AVG(total_engagement) / NULLIF(AVG(quality_score), 0), 2) as engagement_per_quality_point
FROM video_metrics
GROUP BY quality_bucket
ORDER BY quality_bucket DESC;
