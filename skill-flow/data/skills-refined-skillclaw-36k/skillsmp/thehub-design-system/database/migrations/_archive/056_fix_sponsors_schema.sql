-- Migration 056: Fix sponsors table schema
-- Creates sponsors table if missing, then adds columns the admin interface expects
-- Note: Must run before migrations that reference this table

-- First ensure sponsors table exists (copied from 057 for safety)
CREATE TABLE IF NOT EXISTS sponsors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100),
    logo VARCHAR(255),
    logo_dark VARCHAR(255),
    website VARCHAR(255),
    tier ENUM('title', 'gold', 'silver', 'bronze') DEFAULT 'bronze',
    description TEXT,
    active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Add contact fields (ignore errors if columns exist)
ALTER TABLE sponsors ADD COLUMN contact_name VARCHAR(255) NULL AFTER description;
ALTER TABLE sponsors ADD COLUMN contact_email VARCHAR(255) NULL AFTER contact_name;
ALTER TABLE sponsors ADD COLUMN contact_phone VARCHAR(50) NULL AFTER contact_email;

-- Add display order for sorting
ALTER TABLE sponsors ADD COLUMN display_order INT DEFAULT 0 AFTER contact_phone;

-- Add logo_media_id for media library integration
ALTER TABLE sponsors ADD COLUMN logo_media_id INT NULL AFTER logo_dark;
