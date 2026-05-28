-- Add theme_preference column to riders table
-- V2.5 - Theme System Update

ALTER TABLE riders
ADD COLUMN theme_preference VARCHAR(10) DEFAULT 'auto'
COMMENT 'User theme preference: light, dark, or auto (follows system)';

-- Create index for faster lookups (optional but recommended)
CREATE INDEX idx_theme_preference ON riders(theme_preference);
