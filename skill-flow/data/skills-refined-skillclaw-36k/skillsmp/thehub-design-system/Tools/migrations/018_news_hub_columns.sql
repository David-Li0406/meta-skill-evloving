-- Migration 018: Add missing columns to race_reports
-- Date: 2026-01-19
-- Description: Adds YouTube and moderation columns to existing race_reports table

-- ============================================================================
-- ADD MISSING COLUMNS (ignore errors if column already exists)
-- ============================================================================

-- YouTube support columns
ALTER TABLE race_reports ADD COLUMN youtube_url VARCHAR(255) NULL AFTER instagram_embed_code;
ALTER TABLE race_reports ADD COLUMN youtube_video_id VARCHAR(20) NULL AFTER youtube_url;
ALTER TABLE race_reports ADD COLUMN is_from_youtube TINYINT(1) DEFAULT 0 AFTER youtube_video_id;

-- Moderation columns
ALTER TABLE race_reports ADD COLUMN moderated_by INT NULL AFTER allow_comments;
ALTER TABLE race_reports ADD COLUMN moderated_at DATETIME NULL AFTER moderated_by;
ALTER TABLE race_reports ADD COLUMN moderation_notes TEXT NULL AFTER moderated_at;
