-- Migration 110: Add YouTube support to race_reports
-- Allows linking YouTube videos in race reports

ALTER TABLE race_reports ADD COLUMN IF NOT EXISTS youtube_url VARCHAR(255) NULL AFTER instagram_embed_code;
ALTER TABLE race_reports ADD COLUMN IF NOT EXISTS youtube_video_id VARCHAR(20) NULL AFTER youtube_url;
ALTER TABLE race_reports ADD COLUMN IF NOT EXISTS is_from_youtube TINYINT(1) DEFAULT 0 AFTER youtube_video_id;

-- Add index for filtering YouTube reports
CREATE INDEX IF NOT EXISTS idx_reports_youtube ON race_reports(is_from_youtube);
