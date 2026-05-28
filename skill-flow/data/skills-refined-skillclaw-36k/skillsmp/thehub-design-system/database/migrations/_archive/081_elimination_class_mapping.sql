-- Elimination Series Class per Rider
-- Each rider can have their own series class for points
-- Example: In "Ungdom Pojkar" DS class:
--   - 14-year-old rider -> gets points in "Herr Junior"
--   - 12-year-old rider -> gets points in "Pojkar"
-- Created: 2025-12-29

-- Add series_class_id column to elimination_qualifying
-- This allows each rider to have their own series class for points
ALTER TABLE elimination_qualifying
    ADD COLUMN IF NOT EXISTS series_class_id INT NULL AFTER class_id,
    ADD CONSTRAINT fk_eq_series_class FOREIGN KEY (series_class_id) REFERENCES classes(id) ON DELETE SET NULL;
