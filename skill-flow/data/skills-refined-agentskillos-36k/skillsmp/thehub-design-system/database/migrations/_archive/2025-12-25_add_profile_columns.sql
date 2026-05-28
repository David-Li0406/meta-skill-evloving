-- Migration: Add all profile columns to riders table
-- TheHUB V3.5 - Profile editing support
-- Date: 2025-12-25

-- Social profiles
ALTER TABLE riders ADD COLUMN social_instagram VARCHAR(100) DEFAULT NULL COMMENT 'Instagram användarnamn';
ALTER TABLE riders ADD COLUMN social_strava VARCHAR(100) DEFAULT NULL COMMENT 'Strava profil';
ALTER TABLE riders ADD COLUMN social_facebook VARCHAR(255) DEFAULT NULL COMMENT 'Facebook profil';
ALTER TABLE riders ADD COLUMN social_youtube VARCHAR(100) DEFAULT NULL COMMENT 'YouTube kanal';
ALTER TABLE riders ADD COLUMN social_tiktok VARCHAR(100) DEFAULT NULL COMMENT 'TikTok användarnamn';

-- Contact info
ALTER TABLE riders ADD COLUMN phone VARCHAR(50) DEFAULT NULL COMMENT 'Telefonnummer';

-- Emergency contact (ICE - In Case of Emergency)
ALTER TABLE riders ADD COLUMN ice_name VARCHAR(255) DEFAULT NULL COMMENT 'Nödkontakt namn';
ALTER TABLE riders ADD COLUMN ice_phone VARCHAR(50) DEFAULT NULL COMMENT 'Nödkontakt telefon';

-- Profile image
ALTER TABLE riders ADD COLUMN avatar_url VARCHAR(500) DEFAULT NULL COMMENT 'Profilbild URL (ImgBB)';
ALTER TABLE riders ADD COLUMN profile_image_url VARCHAR(500) DEFAULT NULL COMMENT 'Profilbild URL (alternativ)';

-- Additional fields
ALTER TABLE riders ADD COLUMN uci_id VARCHAR(50) DEFAULT NULL COMMENT 'UCI ID';
