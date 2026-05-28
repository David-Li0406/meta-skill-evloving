-- ============================================================================
-- Migration 015: Win-Back Invitation System
-- Adds promotor ownership, invitation tracking and contact management
-- ============================================================================

-- Add promotor ownership to campaigns
ALTER TABLE winback_campaigns
    ADD COLUMN IF NOT EXISTS owner_user_id INT UNSIGNED NULL COMMENT 'Admin user who owns this campaign',
    ADD COLUMN IF NOT EXISTS allow_promotor_access TINYINT(1) DEFAULT 0 COMMENT 'Allow promotors to see results',
    ADD INDEX IF NOT EXISTS idx_owner (owner_user_id);

-- Invitation log - tracks all sent invitations
CREATE TABLE IF NOT EXISTS winback_invitations (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT UNSIGNED NOT NULL,
    rider_id INT NOT NULL,

    -- Invitation details
    email_address VARCHAR(255) NULL,
    invitation_method ENUM('email', 'manual', 'bulk') DEFAULT 'email',
    invitation_status ENUM('pending', 'sent', 'failed', 'bounced', 'opened', 'clicked') DEFAULT 'pending',

    -- Tracking
    sent_at DATETIME NULL,
    sent_by INT UNSIGNED NULL COMMENT 'Admin user who sent invitation',
    opened_at DATETIME NULL,
    clicked_at DATETIME NULL,

    -- For email tracking
    tracking_token VARCHAR(64) NULL UNIQUE,

    -- Error handling
    error_message TEXT NULL,
    retry_count INT DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_campaign_rider (campaign_id, rider_id),
    INDEX idx_status (invitation_status),
    INDEX idx_sent_at (sent_at),
    INDEX idx_tracking (tracking_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add email template for win-back invitations
-- (This will be handled in PHP code, not SQL)
