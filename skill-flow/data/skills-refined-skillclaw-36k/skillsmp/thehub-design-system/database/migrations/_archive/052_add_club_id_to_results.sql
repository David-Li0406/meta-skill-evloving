-- Migration 052: Add club_id to results table and rider_club_seasons for year-based tracking
-- This allows tracking which club a rider was a member of when they achieved a result
-- Points and rankings will then follow the club they were with at that time,
-- not their current club
--
-- Club membership is locked per year/season:
-- - A rider cannot change club during a season
-- - A rider can change clubs between seasons

-- ============================================================================
-- STEP 1: Add club_id column to results table
-- ============================================================================
ALTER TABLE results ADD COLUMN club_id INT NULL AFTER cyclist_id;

-- Add foreign key constraint
ALTER TABLE results ADD CONSTRAINT fk_results_club
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE SET NULL;

-- Add index for better query performance
CREATE INDEX idx_results_club ON results(club_id);

-- ============================================================================
-- STEP 2: Create rider_club_seasons table
-- ============================================================================
-- This table tracks which club a rider was a member of during each season/year
-- Once set for a year, it's locked and cannot be changed
CREATE TABLE IF NOT EXISTS rider_club_seasons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL,
    club_id INT NOT NULL,
    season_year INT NOT NULL,
    locked TINYINT(1) DEFAULT 1,  -- 1 = locked (has results), 0 = can still change
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_rider_season (rider_id, season_year),
    INDEX idx_rider (rider_id),
    INDEX idx_club (club_id),
    INDEX idx_season (season_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- STEP 3: Backfill rider_club_seasons from existing results
-- ============================================================================
-- For each rider, for each year they have results, use their current club
INSERT IGNORE INTO rider_club_seasons (rider_id, club_id, season_year, locked)
SELECT DISTINCT
    r.cyclist_id,
    rd.club_id,
    YEAR(e.date),
    1  -- locked since they have results
FROM results r
JOIN riders rd ON r.cyclist_id = rd.id
JOIN events e ON r.event_id = e.id
WHERE rd.club_id IS NOT NULL;

-- ============================================================================
-- STEP 4: Backfill club_id on results from rider_club_seasons
-- ============================================================================
UPDATE results r
JOIN events e ON r.event_id = e.id
JOIN rider_club_seasons rcs ON r.cyclist_id = rcs.rider_id AND YEAR(e.date) = rcs.season_year
SET r.club_id = rcs.club_id
WHERE r.club_id IS NULL;

-- Fallback: For any results that still don't have a club, use rider's current club
UPDATE results r
JOIN riders rd ON r.cyclist_id = rd.id
SET r.club_id = rd.club_id
WHERE r.club_id IS NULL AND rd.club_id IS NOT NULL;
