-- Migration: Add stage bonus configuration to series
-- Allows automatic bonus points for stage winners in a series

ALTER TABLE series
ADD COLUMN stage_bonus_config JSON NULL COMMENT 'JSON config for automatic stage bonus points'
AFTER count_best_results;

-- Example config structure:
-- {
--   "enabled": true,
--   "stage": "ss1",
--   "scale": "top3",
--   "points": [25, 20, 16],
--   "class_ids": [1, 2, 3] or null for all classes
-- }
