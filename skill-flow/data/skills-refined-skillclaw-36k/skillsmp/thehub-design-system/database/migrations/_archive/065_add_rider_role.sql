-- Migration 065: Add rider role to admin_users
-- Date: 2025-12-16
-- Description: Adds 'rider' to the role ENUM so users can be created with rider role

ALTER TABLE admin_users
    MODIFY COLUMN role ENUM('super_admin', 'admin', 'editor', 'promotor', 'rider') DEFAULT 'rider';
