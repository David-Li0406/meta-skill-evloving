-- Migration 018: Allow Admin News Posts
-- Date: 2026-01-19
-- Description: Allows admin users to post news without rider profile

-- Allow rider_id to be NULL for admin-posted news
ALTER TABLE race_reports MODIFY COLUMN rider_id INT NULL;

-- Add admin_user_id for tracking who posted (if not a rider)
ALTER TABLE race_reports ADD COLUMN admin_user_id INT NULL AFTER rider_id;

-- Add index for admin posts
ALTER TABLE race_reports ADD INDEX idx_reports_admin (admin_user_id);
