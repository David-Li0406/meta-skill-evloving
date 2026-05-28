-- Migration: Add event_format column to events table

-- Check if column exists and add if not
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'events'
    AND COLUMN_NAME = 'event_format'
);

SET @sql = IF(
    @column_exists = 0,
    'ALTER TABLE events ADD COLUMN event_format VARCHAR(20) DEFAULT "ENDURO" AFTER discipline',
    'SELECT "Column event_format already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Create index
SET @index_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'events'
    AND INDEX_NAME = 'idx_event_format'
);

SET @sql = IF(
    @index_exists = 0,
    'CREATE INDEX idx_event_format ON events(event_format)',
    'SELECT "Index idx_event_format already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
