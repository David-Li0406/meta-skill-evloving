-- Migration: 094_fix_club_admins_table
-- Description: Drop and recreate club_admins table with correct structure
-- Date: 2026-01-05

-- Drop the old table if it exists with wrong structure
DROP TABLE IF EXISTS club_admins;

-- Recreate club_admins table with correct structure
CREATE TABLE club_admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT 'References admin_users.id',
    club_id INT NOT NULL COMMENT 'References clubs.id',
    can_edit_profile TINYINT(1) DEFAULT 1 COMMENT 'Can edit club name, description, contact info',
    can_upload_logo TINYINT(1) DEFAULT 1 COMMENT 'Can upload/change club logo',
    can_manage_members TINYINT(1) DEFAULT 0 COMMENT 'Can add/remove club members',
    granted_by INT NULL COMMENT 'Admin user who granted this access',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY unique_user_club (user_id, club_id),
    INDEX idx_user_id (user_id),
    INDEX idx_club_id (club_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
