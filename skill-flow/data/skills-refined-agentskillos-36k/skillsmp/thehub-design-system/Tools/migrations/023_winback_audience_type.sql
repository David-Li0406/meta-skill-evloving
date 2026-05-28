-- ============================================================================
-- Migration 023: Win-Back Audience Type
-- Adds support for targeting both churned AND active participants
-- ============================================================================

-- Add audience_type column to distinguish campaign targets
ALTER TABLE winback_campaigns
ADD COLUMN audience_type ENUM('churned', 'active') DEFAULT 'churned'
AFTER target_type;

-- Add index for audience filtering
ALTER TABLE winback_campaigns
ADD INDEX idx_audience (audience_type, is_active);

-- Update comment on target_year for clarity
ALTER TABLE winback_campaigns
MODIFY COLUMN target_year YEAR NOT NULL DEFAULT 2025
COMMENT 'For churned: year they did NOT compete. For active: year they DID compete';
