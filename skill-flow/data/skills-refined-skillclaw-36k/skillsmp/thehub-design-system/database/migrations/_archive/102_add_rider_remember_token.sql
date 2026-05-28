-- Migration 102: Add Remember Token to Riders
-- Date: 2026-01-10
-- Description: Adds remember_token columns for "kom ihåg mig" functionality

-- Add remember token columns to riders table
-- Note: Using ALTER TABLE which may fail if columns exist.
-- For safe column addition, use the PHP migration instead.

-- ALTER TABLE riders ADD COLUMN remember_token VARCHAR(64) NULL;
-- ALTER TABLE riders ADD COLUMN remember_token_expires DATETIME NULL;
-- ALTER TABLE riders ADD INDEX idx_remember_token (remember_token);

-- See /admin/migrations/102_add_rider_remember_token.php for safe migration
