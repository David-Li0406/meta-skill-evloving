-- Migration: 091_club_admins_and_logo
-- Description: Add club_admins table and logo_url column for image uploads
-- Date: 2025-12-31

-- Add logo_url column to clubs (for ImgBB uploaded images)
ALTER TABLE clubs ADD COLUMN IF NOT EXISTS logo_url VARCHAR(500) NULL AFTER website;

-- Create club_admins table (links users to clubs they can manage)
CREATE TABLE IF NOT EXISTS club_admins (
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

-- Add comment to explain the relationship
-- Note: club_admins allows any role (rider, promotor, admin) to manage specific clubs
-- This is separate from the rider_profiles.can_manage_club which is rider-specific
