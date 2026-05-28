-- Reset Results and Import History
-- Delete all results and import tracking data
-- IMPORTANT: This cannot be undone!

START TRANSACTION;

-- Count before deletion (for reference)
SELECT
    (SELECT COUNT(*) FROM results) as 'Results',
    (SELECT COUNT(*) FROM import_history) as 'Import History',
    (SELECT COUNT(*) FROM import_records) as 'Import Records';

-- Delete all results
DELETE FROM results;

-- Delete all import records (tracking data)
DELETE FROM import_records;

-- Delete all import history
DELETE FROM import_history;

-- Show counts after deletion
SELECT
    (SELECT COUNT(*) FROM results) as 'Results After',
    (SELECT COUNT(*) FROM import_history) as 'Import History After',
    (SELECT COUNT(*) FROM import_records) as 'Import Records After';

-- Commit the transaction
COMMIT;

-- Done!
SELECT 'All results and import history deleted!' as 'Status';
