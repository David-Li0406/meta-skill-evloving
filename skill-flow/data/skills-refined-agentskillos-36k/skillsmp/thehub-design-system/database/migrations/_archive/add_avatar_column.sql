-- Migration: Add avatar_url column to riders table
-- Date: 2025-12-25
-- Description: Adds column to store ImgBB avatar URLs for rider profiles

-- Add avatar_url column after email
ALTER TABLE riders ADD COLUMN avatar_url VARCHAR(500) DEFAULT NULL AFTER email;

-- Add index for faster lookups (optional, but good for performance)
ALTER TABLE riders ADD INDEX idx_avatar_url (avatar_url(255));
