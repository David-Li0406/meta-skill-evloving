-- Query: Weekly Feedback Statistics
-- Purpose: Aggregate engagement metrics by uploader for a date range
-- Parameters:
--   $1: start_date (timestamptz) - Period start, inclusive
--   $2: end_date (timestamptz) - Period end, exclusive
--   $3: civitai_account (text) - Account filter (default: 'c29')
-- Returns: Uploader stats with engagement totals and rates

WITH weekly_stats AS (
  SELECT 
    ast.on_behalf_of,
    ast.civitai_account,
    COUNT(DISTINCT ast.asset_id) as total_assets,
    COUNT(DISTINCT ast.post_id) as total_posts,
    SUM(ast.like_count) as total_likes,
    SUM(ast.heart_count) as total_hearts,
    SUM(ast.laugh_count) as total_laughs,
    SUM(ast.cry_count) as total_cries,
    SUM(ast.dislike_count) as total_dislikes,
    SUM(ast.comment_count) as total_comments,
    SUM(ast.like_count + ast.heart_count + ast.laugh_count) as total_positive_engagement,
    SUM(ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count) as total_engagement
  FROM civitai.asset_stats ast
  WHERE 
    ast.civitai_created_at >= $1::timestamptz
    AND ast.civitai_created_at < $2::timestamptz
    AND ast.on_behalf_of IS NOT NULL
    AND ast.civitai_account = $3
  GROUP BY ast.on_behalf_of, ast.civitai_account
)
SELECT 
  on_behalf_of as uploader,
  civitai_account,
  total_assets,
  total_posts,
  total_likes,
  total_hearts,
  total_laughs,
  total_cries,
  total_dislikes,
  total_comments,
  total_positive_engagement,
  total_engagement,
  ROUND(total_engagement::numeric / NULLIF(total_assets, 0), 2) as avg_engagement_per_asset,
  ROUND((total_positive_engagement::numeric / NULLIF(total_engagement, 0) * 100), 2) as positive_engagement_rate
FROM weekly_stats
ORDER BY total_engagement DESC;
