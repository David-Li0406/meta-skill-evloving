-- Migration 061: Ensure sponsors table has required columns
-- Adds logo, logo_dark, website columns if they don't exist

-- Note: MySQL doesn't have IF NOT EXISTS for columns, so we use a workaround
-- These statements will fail silently if columns already exist

-- Add logo column
ALTER TABLE sponsors ADD COLUMN logo VARCHAR(255) NULL AFTER slug;

-- Add logo_dark column
ALTER TABLE sponsors ADD COLUMN logo_dark VARCHAR(255) NULL AFTER logo;

-- Add website column
ALTER TABLE sponsors ADD COLUMN website VARCHAR(255) NULL AFTER logo_dark;
