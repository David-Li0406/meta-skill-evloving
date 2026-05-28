-- Migration 080: Add address fields to riders for purchases/receipts
-- Date: 2025-12-29

-- Add shipping/billing address fields
ALTER TABLE riders
ADD COLUMN IF NOT EXISTS address VARCHAR(255) DEFAULT NULL COMMENT 'Street address for shipping/receipts',
ADD COLUMN IF NOT EXISTS postal_code VARCHAR(20) DEFAULT NULL COMMENT 'Postal/ZIP code',
ADD COLUMN IF NOT EXISTS postal_city VARCHAR(100) DEFAULT NULL COMMENT 'City for postal address';

-- Add index for city (useful for statistics)
ALTER TABLE riders ADD INDEX IF NOT EXISTS idx_postal_city (postal_city);
