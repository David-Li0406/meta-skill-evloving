-- Query: Week-over-Week Comparison
-- Purpose: Compare engagement metrics between two weeks
-- Parameters:
--   $1: last_week_start (timestamptz) - Current/recent week start
--   $2: last_week_end (timestamptz) - Current/recent week end
--   $3: prev_week_start (timestamptz) - Previous week start
--   $4: prev_week_end (timestamptz) - Previous week end
--   $5: civitai_account (text) - Account filter (default: 'c29')
-- Returns: Both weeks' metrics with changes, growth %, and trend indicator

WITH last_week_stats AS (
  SELECT 
    ast.on_behalf_of,
    ast.civitai_account,
    COUNT(DISTINCT ast.asset_id) as assets_count,
    SUM(ast.like_count) as likes,
    SUM(ast.heart_count) as hearts,
    SUM(ast.laugh_count) as laughs,
    SUM(ast.cry_count) as cries,
    SUM(ast.dislike_count) as dislikes,
    SUM(ast.comment_count) as comments,
    SUM(ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count) as total_engagement
  FROM civitai.asset_stats ast
  WHERE 
    ast.civitai_created_at >= $1::timestamptz
    AND ast.civitai_created_at < $2::timestamptz
    AND ast.on_behalf_of IS NOT NULL
  GROUP BY ast.on_behalf_of, ast.civitai_account
),
previous_week_stats AS (
  SELECT 
    ast.on_behalf_of,
    ast.civitai_account,
    COUNT(DISTINCT ast.asset_id) as assets_count,
    SUM(ast.like_count) as likes,
    SUM(ast.heart_count) as hearts,
    SUM(ast.laugh_count) as laughs,
    SUM(ast.cry_count) as cries,
    SUM(ast.dislike_count) as dislikes,
    SUM(ast.comment_count) as comments,
    SUM(ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count) as total_engagement
  FROM civitai.asset_stats ast
  WHERE 
    ast.civitai_created_at >= $3::timestamptz
    AND ast.civitai_created_at < $4::timestamptz
    AND ast.on_behalf_of IS NOT NULL
    AND ast.civitai_account = $5
  GROUP BY ast.on_behalf_of, ast.civitai_account
)
SELECT 
  COALESCE(lw.on_behalf_of, pw.on_behalf_of) as uploader,
  COALESCE(lw.civitai_account, pw.civitai_account) as civitai_account,
  COALESCE(lw.assets_count, 0) as last_week_assets,
  COALESCE(lw.total_engagement, 0) as last_week_engagement,
  COALESCE(lw.likes, 0) as last_week_likes,
  COALESCE(lw.hearts, 0) as last_week_hearts,
  COALESCE(lw.comments, 0) as last_week_comments,
  COALESCE(pw.assets_count, 0) as prev_week_assets,
  COALESCE(pw.total_engagement, 0) as prev_week_engagement,
  COALESCE(pw.likes, 0) as prev_week_likes,
  COALESCE(pw.hearts, 0) as prev_week_hearts,
  COALESCE(pw.comments, 0) as prev_week_comments,
  (COALESCE(lw.assets_count, 0) - COALESCE(pw.assets_count, 0)) as assets_change,
  (COALESCE(lw.total_engagement, 0) - COALESCE(pw.total_engagement, 0)) as engagement_change,
  CASE 
    WHEN COALESCE(pw.total_engagement, 0) = 0 THEN 
      CASE WHEN COALESCE(lw.total_engagement, 0) > 0 THEN 100.00 ELSE 0.00 END
    ELSE 
      ROUND(((COALESCE(lw.total_engagement, 0) - COALESCE(pw.total_engagement, 0))::numeric / pw.total_engagement * 100), 2)
  END as engagement_growth_pct,
  CASE 
    WHEN COALESCE(pw.likes, 0) = 0 THEN 
      CASE WHEN COALESCE(lw.likes, 0) > 0 THEN 100.00 ELSE 0.00 END
    ELSE 
      ROUND(((COALESCE(lw.likes, 0) - COALESCE(pw.likes, 0))::numeric / pw.likes * 100), 2)
  END as likes_growth_pct,
  CASE 
    WHEN COALESCE(pw.hearts, 0) = 0 THEN 
      CASE WHEN COALESCE(lw.hearts, 0) > 0 THEN 100.00 ELSE 0.00 END
    ELSE 
      ROUND(((COALESCE(lw.hearts, 0) - COALESCE(pw.hearts, 0))::numeric / pw.hearts * 100), 2)
  END as hearts_growth_pct,
  CASE 
    WHEN COALESCE(pw.comments, 0) = 0 THEN 
      CASE WHEN COALESCE(lw.comments, 0) > 0 THEN 100.00 ELSE 0.00 END
    ELSE 
      ROUND(((COALESCE(lw.comments, 0) - COALESCE(pw.comments, 0))::numeric / pw.comments * 100), 2)
  END as comments_growth_pct,
  CASE 
    WHEN COALESCE(lw.total_engagement, 0) > COALESCE(pw.total_engagement, 0) THEN 'Growing'
    WHEN COALESCE(lw.total_engagement, 0) < COALESCE(pw.total_engagement, 0) THEN 'Declining'
    ELSE 'Stable'
  END as trend
FROM last_week_stats lw
FULL OUTER JOIN previous_week_stats pw 
  ON lw.on_behalf_of = pw.on_behalf_of 
  AND lw.civitai_account = pw.civitai_account
ORDER BY 
  COALESCE(lw.total_engagement, 0) DESC;
