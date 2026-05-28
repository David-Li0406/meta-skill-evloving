-- Query: Top Performing Assets
-- Purpose: Get the best performing videos/images ranked by engagement
-- Parameters:
--   $1: start_date (timestamptz) - Period start, inclusive
--   $2: end_date (timestamptz) - Period end, exclusive
--   $3: civitai_account (text) - Account filter (default: 'c29')
-- Returns: Top 20 assets with Civitai URLs and all engagement metrics

SELECT 
  ast.on_behalf_of as uploader,
  ast.civitai_account,
  a.civitai_id,
  'https://civitai.com/images/' || a.civitai_id AS civitai_url,
  ast.civitai_created_at,
  ast.like_count,
  ast.heart_count,
  ast.laugh_count,
  ast.cry_count,
  ast.dislike_count,
  ast.comment_count,
  (ast.like_count + ast.heart_count + ast.laugh_count + ast.cry_count + ast.dislike_count + ast.comment_count) as total_engagement,
  (ast.like_count + ast.heart_count + ast.laugh_count) as positive_engagement
FROM civitai.asset_stats ast
JOIN civitai.assets a ON ast.asset_id = a.id
WHERE 
  ast.civitai_created_at >= $1::timestamptz
  AND ast.civitai_created_at < $2::timestamptz
  AND ast.civitai_account = $3
ORDER BY total_engagement DESC
LIMIT 20;
