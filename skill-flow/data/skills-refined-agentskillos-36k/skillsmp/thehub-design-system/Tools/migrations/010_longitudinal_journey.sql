-- ============================================================================
-- Migration 010: Longitudinal Journey Analysis (Years 2-4)
-- Version: 3.1.0
-- Created: 2026-01-16
-- Fixed: 2026-01-16 - Removed DELIMITER/stored procedures for PHP compatibility
--
-- PURPOSE:
-- Extends First Season Journey to track riders over multiple seasons (Years 2-4).
-- Follows rookie cohorts longitudinally to understand long-term patterns.
--
-- KEY CONCEPT: Year Offset
-- - year_offset = 1: Rookie year (first season)
-- - year_offset = 2: Second season
-- - year_offset = 3: Third season
-- - year_offset = 4: Fourth season
--
-- GDPR COMPLIANCE:
-- - Same rules as migration 009
-- - Segments <10 must be hidden/aggregated
-- - Language focuses on "patterns" not "predictions"
--
-- NOTE: Stored procedures removed - all calculation logic is in KPICalculator.php
--
-- TABLES CREATED:
-- - rider_journey_years: Per-rider per-year metrics (years 1-4)
-- - cohort_longitudinal_aggregates: Aggregated year-over-year stats
-- - rider_journey_summary: Overall journey summary per rider
-- ============================================================================

-- ============================================================================
-- TABLE: rider_journey_years
-- Tracks individual rider metrics for each year of their journey (1-4)
-- ============================================================================
CREATE TABLE IF NOT EXISTS rider_journey_years (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Identity
    rider_id INT NOT NULL,
    cohort_year YEAR NOT NULL,                    -- Original first season year
    year_offset TINYINT NOT NULL,                 -- 1=rookie, 2=year 2, 3=year 3, 4=year 4
    calendar_year YEAR NOT NULL,                  -- Actual calendar year (cohort_year + year_offset - 1)

    -- Activity Metrics for this specific year
    total_starts INT DEFAULT 0,
    total_events INT DEFAULT 0,
    total_finishes INT DEFAULT 0,
    total_dnf INT DEFAULT 0,
    dnf_rate DECIMAL(5,4) DEFAULT NULL,

    -- Result Quality for this year
    best_position INT DEFAULT NULL,
    avg_position DECIMAL(6,2) DEFAULT NULL,
    result_percentile DECIMAL(5,2) DEFAULT NULL,
    podium_count INT DEFAULT 0,
    top10_count INT DEFAULT 0,
    total_points INT DEFAULT 0,                   -- If points system exists

    -- Year-over-Year Comparison
    starts_delta INT DEFAULT NULL,                -- Change from previous year
    events_delta INT DEFAULT NULL,
    percentile_delta DECIMAL(5,2) DEFAULT NULL,
    points_delta INT DEFAULT NULL,

    -- Activity Pattern for this year
    was_active TINYINT(1) DEFAULT 0,              -- Had at least 1 start
    engagement_trend ENUM('increasing', 'stable', 'decreasing', 'inactive') DEFAULT NULL,

    -- Timing within this year
    first_event_date DATE DEFAULT NULL,
    last_event_date DATE DEFAULT NULL,
    days_active INT DEFAULT NULL,
    season_spread_score DECIMAL(5,4) DEFAULT NULL,

    -- Context
    club_id INT DEFAULT NULL,
    club_changed TINYINT(1) DEFAULT 0,            -- Changed club from previous year
    class_id INT DEFAULT NULL,
    class_changed TINYINT(1) DEFAULT 0,           -- Changed class (age progression)
    primary_discipline VARCHAR(50) DEFAULT NULL,

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    -- Indexes
    INDEX idx_rider_cohort (rider_id, cohort_year),
    INDEX idx_cohort_offset (cohort_year, year_offset),
    INDEX idx_calendar_year (calendar_year),
    INDEX idx_active (was_active, year_offset),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_rider_year (rider_id, cohort_year, year_offset),

    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE SET NULL
    -- NOTE: snapshot_id FK removed - analytics_snapshots may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: cohort_longitudinal_aggregates
-- Aggregated statistics per cohort per year_offset (minimum 10 riders)
-- ============================================================================
CREATE TABLE IF NOT EXISTS cohort_longitudinal_aggregates (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Segment Definition
    cohort_year YEAR NOT NULL,
    year_offset TINYINT NOT NULL,                 -- 1, 2, 3, or 4
    segment_type ENUM('overall', 'gender', 'first_season_engagement', 'first_season_percentile', 'discipline') NOT NULL,
    segment_value VARCHAR(100) DEFAULT NULL,

    -- Population
    total_riders_in_cohort INT NOT NULL,          -- Original cohort size
    active_riders_this_year INT NOT NULL,         -- Still active in this year_offset
    retention_rate DECIMAL(5,4) DEFAULT NULL,     -- active_this_year / total_in_cohort
    churn_rate DECIMAL(5,4) DEFAULT NULL,         -- 1 - retention_rate (cumulative)

    -- Activity Aggregates for active riders
    avg_starts DECIMAL(6,2) DEFAULT NULL,
    median_starts DECIMAL(6,2) DEFAULT NULL,
    avg_events DECIMAL(6,2) DEFAULT NULL,
    avg_dnf_rate DECIMAL(5,4) DEFAULT NULL,

    -- Result Aggregates for active riders
    avg_percentile DECIMAL(5,2) DEFAULT NULL,
    median_percentile DECIMAL(5,2) DEFAULT NULL,
    pct_improved_percentile DECIMAL(5,4) DEFAULT NULL,  -- % that improved vs previous year
    avg_percentile_change DECIMAL(5,2) DEFAULT NULL,    -- Avg change from previous year

    -- Progression Patterns
    pct_increased_activity DECIMAL(5,4) DEFAULT NULL,   -- % that started more than prev year
    pct_stable_activity DECIMAL(5,4) DEFAULT NULL,      -- % with similar activity
    pct_decreased_activity DECIMAL(5,4) DEFAULT NULL,   -- % that started less

    -- Year-over-Year Retention Detail
    pct_continuous DECIMAL(5,4) DEFAULT NULL,           -- Active every year so far
    pct_returning DECIMAL(5,4) DEFAULT NULL,            -- Returned after gap
    pct_dropped DECIMAL(5,4) DEFAULT NULL,              -- Not active this year

    -- First Season Correlation (patterns, not predictions)
    correlation_fs_starts_retention DECIMAL(5,4) DEFAULT NULL,   -- Pearson correlation
    correlation_fs_percentile_retention DECIMAL(5,4) DEFAULT NULL,
    correlation_fs_engagement_retention DECIMAL(5,4) DEFAULT NULL,

    -- Statistical Measures
    retention_ci_lower DECIMAL(5,4) DEFAULT NULL,       -- 95% CI
    retention_ci_upper DECIMAL(5,4) DEFAULT NULL,

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    INDEX idx_cohort_year (cohort_year, year_offset),
    INDEX idx_segment (segment_type, segment_value),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_cohort_segment_offset (cohort_year, year_offset, segment_type, segment_value, snapshot_id)
    -- NOTE: snapshot_id FK removed - analytics_snapshots may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: rider_journey_summary
-- Overall journey summary per rider (condensed view across all years)
-- ============================================================================
CREATE TABLE IF NOT EXISTS rider_journey_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Identity
    rider_id INT NOT NULL,
    cohort_year YEAR NOT NULL,

    -- Journey Duration
    total_seasons_active INT DEFAULT 0,           -- Out of possible 4
    last_active_year_offset TINYINT DEFAULT NULL, -- 1, 2, 3, or 4
    is_still_active TINYINT(1) DEFAULT NULL,      -- Active in most recent season

    -- Journey Pattern Classification
    journey_pattern ENUM(
        'continuous_4yr',           -- Active all 4 years
        'continuous_3yr',           -- Active years 1-3, may or may not be in year 4
        'continuous_2yr',           -- Active years 1-2 only
        'one_and_done',             -- Only active in rookie year
        'gap_returner',             -- Had gaps but returned
        'late_dropout'              -- Active 2+ years then stopped
    ) DEFAULT NULL,

    -- Aggregated Metrics Across All Years
    total_career_starts INT DEFAULT 0,
    total_career_events INT DEFAULT 0,
    total_career_finishes INT DEFAULT 0,
    career_dnf_rate DECIMAL(5,4) DEFAULT NULL,
    career_best_position INT DEFAULT NULL,
    career_avg_percentile DECIMAL(5,2) DEFAULT NULL,
    career_total_points INT DEFAULT 0,
    career_podium_count INT DEFAULT 0,

    -- Trajectory
    percentile_trajectory ENUM('improving', 'stable', 'declining', 'insufficient_data') DEFAULT NULL,
    activity_trajectory ENUM('increasing', 'stable', 'decreasing', 'sporadic') DEFAULT NULL,

    -- First Season Data (denormalized for quick access)
    fs_total_starts INT DEFAULT NULL,
    fs_result_percentile DECIMAL(5,2) DEFAULT NULL,
    fs_engagement_score DECIMAL(5,2) DEFAULT NULL,
    fs_activity_pattern VARCHAR(50) DEFAULT NULL,

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    INDEX idx_rider (rider_id),
    INDEX idx_cohort (cohort_year),
    INDEX idx_pattern (journey_pattern),
    INDEX idx_trajectory (percentile_trajectory, activity_trajectory),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_rider_cohort (rider_id, cohort_year),

    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE
    -- NOTE: snapshot_id FK removed - analytics_snapshots may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: longitudinal_kpi_definitions
-- Metadata for longitudinal journey KPIs
-- ============================================================================
CREATE TABLE IF NOT EXISTS longitudinal_kpi_definitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kpi_key VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(200) NOT NULL,
    description TEXT,
    category ENUM('retention', 'progression', 'activity', 'trajectory', 'correlation') NOT NULL,
    data_type ENUM('integer', 'decimal', 'percentage', 'boolean', 'category') NOT NULL,
    unit VARCHAR(50) DEFAULT NULL,
    formula TEXT DEFAULT NULL,
    higher_is_better TINYINT(1) DEFAULT NULL,
    typical_range VARCHAR(100) DEFAULT NULL,
    is_heuristic TINYINT(1) DEFAULT 0,
    requires_minimum_n INT DEFAULT 10,
    display_order INT DEFAULT 0,
    visible_in_ui TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERT: Longitudinal KPI Definitions
-- ============================================================================
INSERT INTO longitudinal_kpi_definitions
    (kpi_key, display_name, description, category, data_type, unit, formula, higher_is_better, typical_range, is_heuristic, requires_minimum_n, display_order)
VALUES
    -- Retention KPIs
    ('retention_rate_y2', 'Retentionsgrad år 2', 'Andel av kohorten som var aktiv i år 2', 'retention', 'percentage', '%', 'active_year2 / total_cohort', 1, '30-70%', 0, 10, 10),
    ('retention_rate_y3', 'Retentionsgrad år 3', 'Andel av kohorten som var aktiv i år 3', 'retention', 'percentage', '%', 'active_year3 / total_cohort', 1, '20-50%', 0, 10, 11),
    ('retention_rate_y4', 'Retentionsgrad år 4', 'Andel av kohorten som var aktiv i år 4', 'retention', 'percentage', '%', 'active_year4 / total_cohort', 1, '15-40%', 0, 10, 12),
    ('churn_rate_y2', 'Bortfall år 2', 'Andel som inte återkom efter år 1', 'retention', 'percentage', '%', '1 - retention_rate_y2', 0, '30-70%', 0, 10, 13),

    -- Progression KPIs
    ('pct_improved_y2', 'Förbättrade år 2', 'Andel som förbättrade sin percentil från år 1 till 2', 'progression', 'percentage', '%', 'COUNT(percentile_y2 > percentile_y1) / active_y2', 1, '30-60%', 1, 10, 20),
    ('avg_percentile_change_y2', 'Snitt percentilförändring år 2', 'Genomsnittlig förändring i percentil från år 1 till 2', 'progression', 'decimal', 'percentilenheter', 'AVG(percentile_y2 - percentile_y1)', 1, '-10 to +10', 1, 10, 21),
    ('pct_increased_activity', 'Ökad aktivitet', 'Andel som startade fler event än föregående år', 'progression', 'percentage', '%', 'COUNT(starts_y2 > starts_y1) / active_y2', 1, '20-50%', 1, 10, 22),

    -- Activity KPIs
    ('avg_starts_y2', 'Snitt starter år 2', 'Genomsnittligt antal starter i år 2 (för de aktiva)', 'activity', 'decimal', 'starter', 'AVG(starts) WHERE year_offset=2 AND active', 1, '2-8', 0, 10, 30),
    ('avg_starts_y3', 'Snitt starter år 3', 'Genomsnittligt antal starter i år 3 (för de aktiva)', 'activity', 'decimal', 'starter', 'AVG(starts) WHERE year_offset=3 AND active', 1, '3-10', 0, 10, 31),

    -- Trajectory KPIs
    ('pct_continuous_4yr', 'Kontinuerligt aktiva 4 år', 'Andel av kohorten aktiv alla 4 år', 'trajectory', 'percentage', '%', 'COUNT(active all 4 years) / total_cohort', 1, '10-30%', 1, 10, 40),
    ('pct_one_and_done', 'Endast rookiesäsong', 'Andel som endast var aktiv under första säsongen', 'trajectory', 'percentage', '%', 'COUNT(journey_pattern=one_and_done) / total_cohort', 0, '30-50%', 1, 10, 41),
    ('pct_gap_returner', 'Återvändare efter uppehåll', 'Andel som kom tillbaka efter minst ett års uppehåll', 'trajectory', 'percentage', '%', 'COUNT(journey_pattern=gap_returner) / total_cohort', NULL, '5-15%', 1, 10, 42),

    -- Correlation KPIs (HEURISTIC - patterns only)
    ('corr_fs_starts_retention', 'Korrelation: starter → retention', 'Korrelation mellan antal starter i år 1 och retention år 2+', 'correlation', 'decimal', 'r', 'Pearson(fs_starts, still_active_y2+)', NULL, '-0.5 to 0.5', 1, 30, 50),
    ('corr_fs_percentile_retention', 'Korrelation: percentil → retention', 'Korrelation mellan resultatpercentil år 1 och retention', 'correlation', 'decimal', 'r', 'Pearson(fs_percentile, still_active_y2+)', NULL, '-0.5 to 0.5', 1, 30, 51),
    ('corr_fs_engagement_retention', 'Korrelation: engagemang → retention', 'Korrelation mellan engagemangsscore år 1 och retention', 'correlation', 'decimal', 'r', 'Pearson(fs_engagement_score, still_active_y2+)', NULL, '-0.5 to 0.5', 1, 30, 52)
ON DUPLICATE KEY UPDATE
    display_name = VALUES(display_name),
    description = VALUES(description);

-- ============================================================================
-- VIEW: longitudinal_cohort_funnel
-- Funnel view showing retention at each year for each cohort
-- ============================================================================
CREATE OR REPLACE VIEW longitudinal_cohort_funnel AS
SELECT
    cla.cohort_year,
    MAX(CASE WHEN cla.year_offset = 1 THEN cla.total_riders_in_cohort END) AS year_1_total,
    MAX(CASE WHEN cla.year_offset = 1 THEN cla.active_riders_this_year END) AS year_1_active,
    MAX(CASE WHEN cla.year_offset = 2 THEN cla.active_riders_this_year END) AS year_2_active,
    MAX(CASE WHEN cla.year_offset = 2 THEN cla.retention_rate END) AS year_2_retention,
    MAX(CASE WHEN cla.year_offset = 3 THEN cla.active_riders_this_year END) AS year_3_active,
    MAX(CASE WHEN cla.year_offset = 3 THEN cla.retention_rate END) AS year_3_retention,
    MAX(CASE WHEN cla.year_offset = 4 THEN cla.active_riders_this_year END) AS year_4_active,
    MAX(CASE WHEN cla.year_offset = 4 THEN cla.retention_rate END) AS year_4_retention
FROM cohort_longitudinal_aggregates cla
WHERE cla.segment_type = 'overall'
GROUP BY cla.cohort_year
ORDER BY cla.cohort_year DESC;

-- ============================================================================
-- VIEW: journey_pattern_distribution
-- Distribution of journey patterns per cohort
-- ============================================================================
CREATE OR REPLACE VIEW journey_pattern_distribution AS
SELECT
    cohort_year,
    journey_pattern,
    COUNT(*) AS rider_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY cohort_year) AS percentage
FROM rider_journey_summary
GROUP BY cohort_year, journey_pattern
HAVING COUNT(*) >= 10  -- GDPR: minimum segment size
ORDER BY cohort_year DESC, rider_count DESC;

-- ============================================================================
-- VIEW: longitudinal_report_safe
-- Pre-filtered view for GDPR compliance (segments ≥10 only)
-- ============================================================================
CREATE OR REPLACE VIEW longitudinal_report_safe AS
SELECT
    cla.*,
    CASE WHEN cla.active_riders_this_year >= 10 THEN cla.retention_rate ELSE NULL END AS display_retention,
    CASE WHEN cla.active_riders_this_year >= 10 THEN cla.avg_percentile ELSE NULL END AS display_avg_percentile,
    cla.active_riders_this_year >= 10 AS is_displayable
FROM cohort_longitudinal_aggregates cla;

-- ============================================================================
-- Migration complete marker
-- ============================================================================
INSERT INTO analytics_system_config (config_key, config_value, description)
VALUES
    ('longitudinal_journey_version', '3.1.0', 'Longitudinal Journey module version'),
    ('longitudinal_max_years', '4', 'Maximum years to track in longitudinal analysis'),
    ('longitudinal_enabled', 'true', 'Enable Longitudinal Journey calculations')
ON DUPLICATE KEY UPDATE config_value = VALUES(config_value);

-- Record migration
INSERT INTO analytics_kpi_audit (kpi_key, old_definition, new_definition, change_type, changed_by, rationale)
VALUES ('_migration_010', NULL, 'Longitudinal Journey tables and procedures (Years 2-4)', 'migration', 'system', 'Migration 010 completed')
ON DUPLICATE KEY UPDATE changed_at = NOW();
