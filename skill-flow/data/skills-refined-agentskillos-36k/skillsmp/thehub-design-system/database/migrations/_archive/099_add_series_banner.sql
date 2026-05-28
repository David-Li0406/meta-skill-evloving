-- Migration: 099_add_series_banner
-- Description: Add banner image support to series for promotor customization
-- Date: 2026-01-08

-- Add banner_media_id to series (references media library)
ALTER TABLE series ADD COLUMN IF NOT EXISTS banner_media_id INT NULL;

-- Add index for faster lookups
ALTER TABLE series ADD INDEX IF NOT EXISTS idx_series_banner (banner_media_id);

-- Add logo_media_id if not exists (for media library integration)
ALTER TABLE series ADD COLUMN IF NOT EXISTS logo_media_id INT NULL;
