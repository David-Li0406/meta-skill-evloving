-- Migration 020: Rider Profile Redesign
-- Adds achievements system, social profiles, and cached statistics

-- Create rider_achievements table
CREATE TABLE IF NOT EXISTS rider_achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL,
    achievement_type VARCHAR(50) NOT NULL,
    achievement_value VARCHAR(100) DEFAULT NULL,
    series_id INT DEFAULT NULL,
    season_year INT DEFAULT NULL,
    earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rider_achievements_rider (rider_id),
    INDEX idx_rider_achievements_type (achievement_type),
    INDEX idx_rider_achievements_season (season_year),
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE
);

-- Add social profile columns to riders table
ALTER TABLE riders
    ADD COLUMN IF NOT EXISTS social_instagram VARCHAR(100) DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS social_facebook VARCHAR(255) DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS social_strava VARCHAR(50) DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS social_youtube VARCHAR(100) DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS social_tiktok VARCHAR(100) DEFAULT NULL;

-- Add cached stats columns for fast profile loading
ALTER TABLE riders
    ADD COLUMN IF NOT EXISTS stats_total_starts INT DEFAULT 0,
    ADD COLUMN IF NOT EXISTS stats_total_finished INT DEFAULT 0,
    ADD COLUMN IF NOT EXISTS stats_total_wins INT DEFAULT 0,
    ADD COLUMN IF NOT EXISTS stats_total_podiums INT DEFAULT 0,
    ADD COLUMN IF NOT EXISTS stats_total_points INT DEFAULT 0,
    ADD COLUMN IF NOT EXISTS stats_updated_at DATETIME DEFAULT NULL;

-- Add experience tracking columns
ALTER TABLE riders
    ADD COLUMN IF NOT EXISTS first_season INT DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS experience_level INT DEFAULT 1;

-- Create index for faster stats queries
CREATE INDEX IF NOT EXISTS idx_riders_stats ON riders(stats_total_points, stats_total_wins);
