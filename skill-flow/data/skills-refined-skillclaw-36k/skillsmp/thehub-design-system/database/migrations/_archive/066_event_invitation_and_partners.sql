-- Migration: Add invitation field and partner sponsors support
-- Date: 2025-12-16

-- Add invitation field to events table (shown at top of Inbjudan/Information tab)
ALTER TABLE events ADD COLUMN IF NOT EXISTS invitation TEXT NULL COMMENT 'Inbjudningstext för eventet';
ALTER TABLE events ADD COLUMN IF NOT EXISTS invitation_use_global TINYINT(1) DEFAULT 0 COMMENT 'Använd global inbjudningstext';

-- Ensure event_sponsors placement ENUM includes 'partner' for bottom logo row
ALTER TABLE event_sponsors MODIFY COLUMN placement ENUM('header', 'sidebar', 'footer', 'content', 'partner') DEFAULT 'sidebar';

-- Also update series_sponsors to support partner placement
ALTER TABLE series_sponsors MODIFY COLUMN placement ENUM('header', 'sidebar', 'footer', 'content', 'partner') DEFAULT 'sidebar';
