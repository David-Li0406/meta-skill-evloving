-- Migration: 093_create_rider_profiles
-- Description: Create rider_profiles table to link admin_users to riders
-- Date: 2026-01-05

-- Create rider_profiles table (links admin users to their rider profiles)
-- This enables:
-- 1. Linking a user account to one or more rider profiles
-- 2. Managing permissions for what the user can do with each profile
-- 3. Supporting family accounts where one login manages multiple riders

CREATE TABLE IF NOT EXISTS rider_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT 'References admin_users.id',
    rider_id INT NOT NULL COMMENT 'References riders.id',
    is_primary TINYINT(1) DEFAULT 1 COMMENT 'Is this the primary profile for this user',
    can_edit_profile TINYINT(1) DEFAULT 1 COMMENT 'Can edit the rider profile',
    can_manage_club TINYINT(1) DEFAULT 0 COMMENT 'Can manage club settings if rider has a club',
    approved_by INT NULL COMMENT 'Admin user who approved this link',
    approved_at TIMESTAMP NULL COMMENT 'When the link was approved',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY unique_user_rider (user_id, rider_id),
    UNIQUE KEY unique_rider (rider_id) COMMENT 'Each rider can only be linked to one user',
    INDEX idx_user_id (user_id),
    INDEX idx_rider_id (rider_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
