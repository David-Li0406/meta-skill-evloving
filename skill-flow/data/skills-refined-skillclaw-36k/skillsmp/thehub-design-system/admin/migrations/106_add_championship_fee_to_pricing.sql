-- Migration 106: Add championship fee to pricing templates
-- Automatic price supplement for events marked as Swedish Championship (SM)

-- Add championship fee column to pricing_templates
ALTER TABLE pricing_templates ADD COLUMN IF NOT EXISTS championship_fee DECIMAL(10,2) DEFAULT 0.00;

-- Add championship fee description for clarity
ALTER TABLE pricing_templates ADD COLUMN IF NOT EXISTS championship_fee_description VARCHAR(255) NULL;
