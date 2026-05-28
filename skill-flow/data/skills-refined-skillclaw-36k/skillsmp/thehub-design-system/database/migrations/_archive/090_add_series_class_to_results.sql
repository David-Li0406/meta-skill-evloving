-- Add series_class_id to results table
-- This allows event results to show one class (e.g. "Sportmotion Herr")
-- while series points go to another class (e.g. "Herrar Elite")

ALTER TABLE results
ADD COLUMN IF NOT EXISTS series_class_id INT NULL AFTER class_id;

-- Add index for performance
ALTER TABLE results
ADD INDEX IF NOT EXISTS idx_series_class (series_class_id);

-- Add foreign key (optional, may fail if classes table doesn't exist)
-- ALTER TABLE results
-- ADD CONSTRAINT fk_results_series_class FOREIGN KEY (series_class_id) REFERENCES classes(id) ON DELETE SET NULL;
