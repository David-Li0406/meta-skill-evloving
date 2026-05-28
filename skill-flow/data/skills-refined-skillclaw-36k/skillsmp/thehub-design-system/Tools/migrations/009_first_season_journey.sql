-- ============================================================================
-- Migration 009: First Season Journey Analysis
-- Version: 3.1.0
-- Created: 2026-01-16
-- Fixed: 2026-01-16 - Removed DELIMITER/stored procedures for PHP compatibility
--
-- PURPOSE:
-- Implements first season journey analysis for rookie riders.
-- Tracks patterns during first season that are associated with continued
-- participation or non-return.
--
-- GDPR COMPLIANCE:
-- - Uses "patterns associated with" language (not predictive/causal)
-- - Segments <10 individuals must be hidden/aggregated in UI
-- - No "at-risk" labels - uses "indicators of low continued activity"
-- - All data is aggregated/anonymized for reporting
--
-- NOTE: Stored procedures removed - all calculation logic is in KPICalculator.php
--
-- TABLES CREATED:
-- - rider_first_season: Individual rider first season metrics
-- - first_season_aggregates: Aggregated cohort statistics (segment ≥10)
-- - first_season_kpi_definitions: KPI metadata for journey analysis
-- ============================================================================

-- ============================================================================
-- TABLE: rider_first_season
-- Stores calculated first season metrics per rider
-- ============================================================================
CREATE TABLE IF NOT EXISTS rider_first_season (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Identity
    rider_id INT NOT NULL,
    cohort_year YEAR NOT NULL,                    -- MIN(season_year) from first event

    -- First Season Activity Metrics
    total_starts INT DEFAULT 0,                   -- COUNT(results) in first season
    total_events INT DEFAULT 0,                   -- COUNT(DISTINCT event_id)
    total_finishes INT DEFAULT 0,                 -- COUNT(results WHERE status='finished')
    total_dnf INT DEFAULT 0,                      -- COUNT(results WHERE status='DNF')
    dnf_rate DECIMAL(5,4) DEFAULT NULL,           -- total_dnf / total_starts

    -- Result Quality
    best_position INT DEFAULT NULL,               -- MIN(position) where finished
    avg_position DECIMAL(6,2) DEFAULT NULL,       -- AVG(position) where finished
    median_position DECIMAL(6,2) DEFAULT NULL,    -- MEDIAN(position) where finished
    result_percentile DECIMAL(5,2) DEFAULT NULL,  -- Avg percentile within class
    podium_count INT DEFAULT 0,                   -- COUNT(position <= 3)
    top10_count INT DEFAULT 0,                    -- COUNT(position <= 10)

    -- Timing Patterns
    first_event_date DATE DEFAULT NULL,
    last_event_date DATE DEFAULT NULL,
    days_in_season INT DEFAULT NULL,              -- DATEDIFF(last, first)
    avg_days_between_starts DECIMAL(6,2) DEFAULT NULL,
    max_gap_days INT DEFAULT NULL,                -- Longest gap between events

    -- Season Distribution
    early_season_starts INT DEFAULT 0,            -- Events in first 1/3 of season
    mid_season_starts INT DEFAULT 0,              -- Events in middle 1/3
    late_season_starts INT DEFAULT 0,             -- Events in last 1/3
    season_spread_score DECIMAL(5,4) DEFAULT NULL,-- How evenly distributed (0-1)

    -- Social Context
    club_id INT DEFAULT NULL,
    club_had_other_rookies TINYINT(1) DEFAULT 0,  -- Were there other rookies in same club?
    club_rookie_count INT DEFAULT 0,              -- How many rookies in club that year
    gender ENUM('M', 'F', 'U') DEFAULT 'U',
    age_at_first_start INT DEFAULT NULL,          -- Calculated from birth_year
    class_id INT DEFAULT NULL,                    -- Primary class raced

    -- Discipline Mix
    primary_discipline VARCHAR(50) DEFAULT NULL,  -- Most common discipline
    discipline_count INT DEFAULT 1,               -- Number of different disciplines

    -- Outcome (for historical analysis)
    returned_year2 TINYINT(1) DEFAULT NULL,       -- Did rider return in year 2?
    returned_year3 TINYINT(1) DEFAULT NULL,       -- Did rider return in year 3?
    total_career_seasons INT DEFAULT NULL,        -- Total seasons active (from stats)
    last_active_year YEAR DEFAULT NULL,           -- Most recent year with activity

    -- Calculated Indicators (NOT predictions - patterns only)
    engagement_score DECIMAL(5,2) DEFAULT NULL,   -- Composite engagement metric
    activity_pattern VARCHAR(50) DEFAULT NULL,    -- 'high_engagement', 'moderate', 'low_engagement'

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,
    data_quality_score DECIMAL(5,4) DEFAULT NULL, -- Data completeness (0-1)

    -- Indexes
    INDEX idx_cohort_year (cohort_year),
    INDEX idx_rider (rider_id),
    INDEX idx_club (club_id),
    INDEX idx_returned (returned_year2, returned_year3),
    INDEX idx_pattern (activity_pattern),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_rider_cohort (rider_id, cohort_year),

    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE SET NULL
    -- NOTE: snapshot_id FK removed - analytics_snapshots may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: first_season_aggregates
-- Aggregated statistics by cohort/segment (minimum 10 riders per segment)
-- Used for reporting to maintain GDPR compliance
-- ============================================================================
CREATE TABLE IF NOT EXISTS first_season_aggregates (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Segment Definition
    cohort_year YEAR NOT NULL,
    segment_type ENUM('overall', 'gender', 'age_group', 'club', 'discipline', 'class', 'engagement_level') NOT NULL,
    segment_value VARCHAR(100) DEFAULT NULL,      -- NULL for 'overall', specific value otherwise

    -- Population (must be ≥10 for display)
    total_riders INT NOT NULL,

    -- Activity Aggregates
    avg_total_starts DECIMAL(6,2) DEFAULT NULL,
    median_total_starts DECIMAL(6,2) DEFAULT NULL,
    avg_total_events DECIMAL(6,2) DEFAULT NULL,
    avg_dnf_rate DECIMAL(5,4) DEFAULT NULL,

    -- Result Aggregates
    avg_result_percentile DECIMAL(5,2) DEFAULT NULL,
    median_result_percentile DECIMAL(5,2) DEFAULT NULL,
    avg_best_position DECIMAL(6,2) DEFAULT NULL,
    pct_with_podium DECIMAL(5,4) DEFAULT NULL,    -- % of segment with at least 1 podium
    pct_with_top10 DECIMAL(5,4) DEFAULT NULL,     -- % with at least 1 top-10

    -- Timing Aggregates
    avg_days_in_season DECIMAL(6,2) DEFAULT NULL,
    avg_gap_between_events DECIMAL(6,2) DEFAULT NULL,
    avg_season_spread DECIMAL(5,4) DEFAULT NULL,

    -- Outcome Aggregates (patterns, not predictions)
    pct_returned_year2 DECIMAL(5,4) DEFAULT NULL, -- % that returned in year 2
    pct_returned_year3 DECIMAL(5,4) DEFAULT NULL, -- % that returned in year 3
    avg_career_seasons DECIMAL(4,2) DEFAULT NULL, -- Avg total seasons for those who started this cohort

    -- Distribution Buckets (for histograms)
    starts_distribution JSON DEFAULT NULL,        -- {"1": 45, "2-3": 30, "4-5": 15, "6+": 10}
    percentile_distribution JSON DEFAULT NULL,    -- {"0-25": 25, "26-50": 25, ...}

    -- Statistical Measures
    return_rate_ci_lower DECIMAL(5,4) DEFAULT NULL,  -- 95% CI lower bound
    return_rate_ci_upper DECIMAL(5,4) DEFAULT NULL,  -- 95% CI upper bound

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    INDEX idx_cohort_segment (cohort_year, segment_type),
    INDEX idx_segment_value (segment_type, segment_value),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_cohort_segment (cohort_year, segment_type, segment_value, snapshot_id)
    -- NOTE: snapshot_id FK removed - analytics_snapshots may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: first_season_kpi_definitions
-- Metadata for first season journey KPIs
-- ============================================================================
CREATE TABLE IF NOT EXISTS first_season_kpi_definitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kpi_key VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(200) NOT NULL,
    description TEXT,
    category ENUM('activity', 'results', 'timing', 'social', 'outcome', 'composite') NOT NULL,
    data_type ENUM('integer', 'decimal', 'percentage', 'boolean', 'category') NOT NULL,
    unit VARCHAR(50) DEFAULT NULL,

    -- SQL formula for calculation (documentation)
    formula TEXT DEFAULT NULL,

    -- Interpretation guidance
    higher_is_better TINYINT(1) DEFAULT NULL,     -- NULL = neutral
    typical_range VARCHAR(100) DEFAULT NULL,      -- e.g., "0-100", "1-15"

    -- Flags
    is_heuristic TINYINT(1) DEFAULT 0,            -- Pattern-based, not factual
    requires_minimum_n INT DEFAULT 10,            -- Minimum sample size for reporting
    gdpr_sensitive TINYINT(1) DEFAULT 0,          -- Requires extra care

    -- Display
    display_order INT DEFAULT 0,
    visible_in_ui TINYINT(1) DEFAULT 1,
    visible_in_export TINYINT(1) DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERT: KPI Definitions for First Season Journey
-- ============================================================================
INSERT INTO first_season_kpi_definitions
    (kpi_key, display_name, description, category, data_type, unit, formula, higher_is_better, typical_range, is_heuristic, requires_minimum_n, display_order)
VALUES
    -- Activity KPIs
    ('total_starts', 'Antal starter', 'Totalt antal starter under första säsongen', 'activity', 'integer', 'starter', 'COUNT(results) WHERE season = cohort_year', 1, '1-15', 0, 1, 10),
    ('total_events', 'Antal event', 'Antal unika tävlingar deltagna', 'activity', 'integer', 'event', 'COUNT(DISTINCT event_id)', 1, '1-10', 0, 1, 11),
    ('total_finishes', 'Antal målgångar', 'Starter som resulterade i placering', 'activity', 'integer', 'målgångar', 'COUNT(results WHERE status=finished)', 1, '1-15', 0, 1, 12),
    ('dnf_rate', 'DNF-andel', 'Andel starter som inte fullföljdes', 'activity', 'percentage', '%', 'total_dnf / total_starts', 0, '0-30%', 0, 1, 13),

    -- Result KPIs
    ('best_position', 'Bästa placering', 'Bästa uppnådda placering', 'results', 'integer', 'plats', 'MIN(position) WHERE finished', 1, '1-50', 0, 1, 20),
    ('result_percentile', 'Resultat-percentil', 'Genomsnittlig percentil inom klass (högre = bättre relativt andra)', 'results', 'percentage', '%', 'AVG((total_in_class - position) / total_in_class * 100)', 1, '0-100', 0, 1, 21),
    ('podium_count', 'Pallplatser', 'Antal topp-3 placeringar', 'results', 'integer', 'podier', 'COUNT(position <= 3)', 1, '0-5', 0, 1, 22),

    -- Timing KPIs
    ('days_in_season', 'Dagar i säsongen', 'Dagar mellan första och sista start', 'timing', 'integer', 'dagar', 'DATEDIFF(last_event, first_event)', NULL, '0-180', 0, 1, 30),
    ('avg_days_between_starts', 'Snitt dagar mellan starter', 'Genomsnittlig tid mellan tävlingar', 'timing', 'decimal', 'dagar', 'AVG(days between consecutive starts)', 0, '7-60', 0, 1, 31),
    ('season_spread_score', 'Säsongsspridning', 'Hur jämnt fördelat deltagandet var över säsongen (1.0 = helt jämnt)', 'timing', 'decimal', 'score', 'Normalized entropy of monthly distribution', 1, '0-1', 0, 1, 32),

    -- Social KPIs
    ('club_rookie_count', 'Klubbkamrater (rookies)', 'Antal andra förstaårscyklister i samma klubb', 'social', 'integer', 'cyklister', 'COUNT(other rookies in same club same year)', NULL, '0-10', 0, 1, 40),

    -- Outcome KPIs (HEURISTIC - patterns only)
    ('returned_year2', 'Återkom år 2', 'Om cyklisten hade minst 1 start år 2', 'outcome', 'boolean', NULL, 'EXISTS(results WHERE year = cohort_year + 1)', 1, 'ja/nej', 1, 10, 50),
    ('returned_year3', 'Återkom år 3', 'Om cyklisten hade minst 1 start år 3', 'outcome', 'boolean', NULL, 'EXISTS(results WHERE year = cohort_year + 2)', 1, 'ja/nej', 1, 10, 51),
    ('total_career_seasons', 'Totalt antal säsonger', 'Antal säsonger med minst 1 start', 'outcome', 'integer', 'säsonger', 'COUNT(DISTINCT season_year with activity)', 1, '1-10', 1, 10, 52),

    -- Composite KPIs (HEURISTIC)
    ('engagement_score', 'Engagemangsscore', 'Sammansatt mått på första säsongens engagemang (baserat på aktivitet, resultat och tidsspridning)', 'composite', 'decimal', 'score', 'Weighted combination: starts*0.3 + events*0.2 + spread*0.2 + percentile*0.3', 1, '0-100', 1, 10, 60),
    ('activity_pattern', 'Aktivitetsmönster', 'Klassificering baserad på första säsongens beteende', 'composite', 'category', NULL, 'CASE on engagement_score thresholds', NULL, 'high/moderate/low', 1, 10, 61)
ON DUPLICATE KEY UPDATE
    display_name = VALUES(display_name),
    description = VALUES(description);

-- ============================================================================
-- VIEW: first_season_report_safe
-- Pre-filtered view that only shows segments with ≥10 riders (GDPR)
-- ============================================================================
CREATE OR REPLACE VIEW first_season_report_safe AS
SELECT
    fsa.*,
    CASE
        WHEN fsa.total_riders >= 10 THEN fsa.total_riders
        ELSE NULL
    END AS display_count,
    CASE
        WHEN fsa.total_riders >= 10 THEN fsa.pct_returned_year2
        ELSE NULL
    END AS display_return_rate_y2,
    CASE
        WHEN fsa.total_riders >= 10 THEN fsa.pct_returned_year3
        ELSE NULL
    END AS display_return_rate_y3,
    fsa.total_riders >= 10 AS is_displayable
FROM first_season_aggregates fsa;

-- ============================================================================
-- VIEW: cohort_overview
-- Quick overview per cohort year
-- ============================================================================
CREATE OR REPLACE VIEW cohort_overview AS
SELECT
    cohort_year,
    COUNT(*) AS total_rookies,
    AVG(total_starts) AS avg_starts,
    AVG(total_events) AS avg_events,
    AVG(dnf_rate) AS avg_dnf_rate,
    AVG(result_percentile) AS avg_percentile,
    SUM(CASE WHEN returned_year2 = 1 THEN 1 ELSE 0 END) / COUNT(*) AS return_rate_year2,
    SUM(CASE WHEN returned_year3 = 1 THEN 1 ELSE 0 END) / COUNT(*) AS return_rate_year3,
    AVG(engagement_score) AS avg_engagement,
    MAX(calculated_at) AS last_calculated
FROM rider_first_season
GROUP BY cohort_year
ORDER BY cohort_year DESC;

-- ============================================================================
-- CREATE STUB TABLES IF NOT EXISTS (for independence)
-- ============================================================================
CREATE TABLE IF NOT EXISTS analytics_kpi_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kpi_key VARCHAR(100) NOT NULL,
    old_definition TEXT,
    new_definition TEXT,
    change_type VARCHAR(50),
    changed_by VARCHAR(100),
    rationale TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_kpi_key (kpi_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS analytics_system_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- INSERT: Analytics KPI audit for new journey KPIs
-- ============================================================================
INSERT INTO analytics_kpi_audit (kpi_key, old_definition, new_definition, change_type, changed_by, rationale)
SELECT
    kpi_key,
    NULL,
    CONCAT(display_name, ': ', description),
    'added',
    'migration_009',
    'First Season Journey module - tracking rookie patterns'
FROM first_season_kpi_definitions
WHERE kpi_key IN ('total_starts', 'returned_year2', 'engagement_score', 'activity_pattern')
ON DUPLICATE KEY UPDATE changed_at = NOW();

-- ============================================================================
-- Migration complete marker
-- ============================================================================
INSERT INTO analytics_system_config (config_key, config_value, description)
VALUES
    ('first_season_journey_version', '3.1.0', 'First Season Journey module version'),
    ('first_season_min_segment_size', '10', 'Minimum segment size for reporting (GDPR)'),
    ('first_season_enabled', 'true', 'Enable First Season Journey calculations')
ON DUPLICATE KEY UPDATE config_value = VALUES(config_value);

-- Record migration
INSERT INTO analytics_kpi_audit (kpi_key, old_definition, new_definition, change_type, changed_by, rationale)
VALUES ('_migration_009', NULL, 'First Season Journey tables and procedures', 'migration', 'system', 'Migration 009 completed')
ON DUPLICATE KEY UPDATE changed_at = NOW();
