-- Migration: 095_add_social_columns_to_clubs
-- Description: Add youtube and tiktok social media columns to clubs table
-- Note: facebook and instagram columns already exist
-- Date: 2026-01-05

ALTER TABLE clubs ADD COLUMN IF NOT EXISTS youtube VARCHAR(255) NULL AFTER instagram;
ALTER TABLE clubs ADD COLUMN IF NOT EXISTS tiktok VARCHAR(100) NULL AFTER youtube;
