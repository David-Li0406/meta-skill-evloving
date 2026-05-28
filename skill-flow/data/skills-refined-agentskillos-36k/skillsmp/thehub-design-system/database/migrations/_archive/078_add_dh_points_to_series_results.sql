-- Migration 078: Add run_1_points and run_2_points to series_results for DH series
-- This allows DH series to show Kval (qualification) and Final points separately

ALTER TABLE series_results
ADD COLUMN run_1_points DECIMAL(10,2) DEFAULT NULL AFTER points,
ADD COLUMN run_2_points DECIMAL(10,2) DEFAULT NULL AFTER run_1_points;

-- Add index for performance
ALTER TABLE series_results
ADD INDEX idx_series_results_runs (series_id, event_id, run_1_points, run_2_points);
