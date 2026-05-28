-- Migration 092: Add linked rider profiles support
-- Allows multiple rider profiles to share one login account
-- This is useful for parents managing their children's accounts

-- Add column to link riders to a primary account holder
ALTER TABLE riders ADD COLUMN IF NOT EXISTS linked_to_rider_id INT UNSIGNED NULL DEFAULT NULL;

-- Add index for faster lookups
ALTER TABLE riders ADD INDEX IF NOT EXISTS idx_linked_rider (linked_to_rider_id);

-- Add foreign key (optional, for data integrity)
-- Note: Using SET NULL on delete so linked accounts don't break if primary is deleted
ALTER TABLE riders
    ADD CONSTRAINT fk_linked_rider
    FOREIGN KEY (linked_to_rider_id) REFERENCES riders(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

-- Comment explaining the column
-- linked_to_rider_id: Points to the primary rider account that holds the password.
-- When a user activates an account with email X, if multiple riders have email X,
-- the selected rider becomes the "primary" (has password set, linked_to_rider_id = NULL),
-- and all other riders with email X get linked_to_rider_id = primary_rider_id.
-- On login, the system authenticates against the primary and loads all linked profiles.
