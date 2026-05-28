-- Migration 077: Update rider_claims table for new approval flow
-- Add contact info columns and make claimant_rider_id nullable (for admin-created claims)

ALTER TABLE rider_claims
    MODIFY COLUMN claimant_rider_id INT NULL,
    ADD COLUMN IF NOT EXISTS phone VARCHAR(50) DEFAULT NULL AFTER claimant_name,
    ADD COLUMN IF NOT EXISTS instagram VARCHAR(100) DEFAULT NULL AFTER phone,
    ADD COLUMN IF NOT EXISTS facebook VARCHAR(255) DEFAULT NULL AFTER instagram,
    ADD COLUMN IF NOT EXISTS created_by ENUM('user', 'admin') DEFAULT 'user' AFTER facebook;

-- Drop the unique constraint that requires claimant_rider_id
ALTER TABLE rider_claims DROP INDEX IF EXISTS unique_pending_claim;

-- Add new index for pending claims by target
CREATE INDEX IF NOT EXISTS idx_target_pending ON rider_claims(target_rider_id, status);
