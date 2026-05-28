-- Migration 098: Add password reset columns to admin_users
-- This allows promotors and admins to reset their passwords

ALTER TABLE admin_users
    ADD COLUMN IF NOT EXISTS password_reset_token VARCHAR(255) DEFAULT NULL AFTER email,
    ADD COLUMN IF NOT EXISTS password_reset_expires DATETIME DEFAULT NULL AFTER password_reset_token;

-- Add index for token lookup
CREATE INDEX IF NOT EXISTS idx_admin_reset_token ON admin_users(password_reset_token);
