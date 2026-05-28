-- Migration: Extend venues table with additional fields
-- Date: 2025-12-13
-- Description: Add logo, contact info, social links, and facility info to venues

-- Add logo field
ALTER TABLE venues ADD COLUMN IF NOT EXISTS logo VARCHAR(500) NULL AFTER website;

-- Add contact fields
ALTER TABLE venues ADD COLUMN IF NOT EXISTS email VARCHAR(255) NULL AFTER logo;
ALTER TABLE venues ADD COLUMN IF NOT EXISTS phone VARCHAR(50) NULL AFTER email;
ALTER TABLE venues ADD COLUMN IF NOT EXISTS contact_person VARCHAR(255) NULL AFTER phone;

-- Add GPS fields if not exist (they might already be there)
ALTER TABLE venues ADD COLUMN IF NOT EXISTS gps_lat DECIMAL(10, 7) NULL AFTER contact_person;
ALTER TABLE venues ADD COLUMN IF NOT EXISTS gps_lng DECIMAL(10, 7) NULL AFTER gps_lat;

-- Add social media links
ALTER TABLE venues ADD COLUMN IF NOT EXISTS facebook VARCHAR(500) NULL AFTER gps_lng;
ALTER TABLE venues ADD COLUMN IF NOT EXISTS instagram VARCHAR(500) NULL AFTER facebook;
ALTER TABLE venues ADD COLUMN IF NOT EXISTS trailforks_url VARCHAR(500) NULL AFTER instagram;
ALTER TABLE venues ADD COLUMN IF NOT EXISTS strava_segment VARCHAR(500) NULL AFTER trailforks_url;

-- Add facility information
ALTER TABLE venues ADD COLUMN IF NOT EXISTS parking_info TEXT NULL AFTER strava_segment;
ALTER TABLE venues ADD COLUMN IF NOT EXISTS facilities TEXT NULL AFTER parking_info;
