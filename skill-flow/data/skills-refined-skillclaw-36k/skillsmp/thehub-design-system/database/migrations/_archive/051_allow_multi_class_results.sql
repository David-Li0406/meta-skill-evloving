-- Migration 051: Allow multiple results per rider per event (one per class)
-- This enables riders to compete in two classes during the same event day
-- (e.g., racing in both "Herrar Elit" morning race and "Open" afternoon race)

-- Drop the existing unique constraint that only allows one result per rider per event
ALTER TABLE results DROP INDEX unique_event_cyclist;

-- Add new unique constraint that allows one result per rider per class per event
-- This means a rider can have multiple results in one event if they're in different classes
ALTER TABLE results ADD UNIQUE KEY unique_event_cyclist_class (event_id, cyclist_id, class_id);

-- Add index on class_id for better query performance
-- (checking if index exists first to avoid error)
SET @idx_exists = (
    SELECT COUNT(1)
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
    AND table_name = 'results'
    AND index_name = 'idx_class'
);
SET @sql = IF(@idx_exists = 0,
    'CREATE INDEX idx_class ON results(class_id)',
    'SELECT "Index idx_class already exists"'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
