-- ============================================================================
-- Migration 012: Event Participation Analysis
-- Version: 3.2.0
-- Created: 2026-01-16
--
-- PURPOSE:
-- Analyzes participation patterns at the EVENT level within series:
-- - How many events do participants attend per series/season?
-- - Which events attract "single-event" participants?
-- - Do single-event participants return to the same event year after year?
-- - Event-level retention rates
--
-- GDPR COMPLIANCE:
-- - Segments <10 individuals must be suppressed
-- - No individual rider identification in exports
--
-- DEPENDENCIES:
-- - Requires events table with venue_id, series_id
-- - Requires results table
-- - Benefits from brand_series_map for brand filtering
--
-- TABLES CREATED:
-- - series_participation_distribution: Per-series event frequency distribution
-- - event_unique_participants: Single-event participants per event
-- - event_retention_yearly: Year-over-year event retention
-- - event_loyal_riders: Multi-year same-event attendees
-- ============================================================================

-- ============================================================================
-- TABLE: series_participation_distribution
-- Tracks how many participants attend 1, 2, 3... N events per series/season
-- ============================================================================
CREATE TABLE IF NOT EXISTS series_participation_distribution (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Scope
    series_id INT NOT NULL,
    season_year YEAR NOT NULL,
    brand_id INT DEFAULT NULL,                  -- NULL = all brands in series

    -- Series context
    total_events_in_series INT NOT NULL,        -- How many events in this series
    total_participants INT NOT NULL,            -- Unique participants in series

    -- Distribution (JSON for flexibility)
    -- {"1": {"count": 450, "pct": 45.0}, "2": {"count": 250, "pct": 25.0}, ...}
    distribution JSON NOT NULL,

    -- Key metrics
    avg_events_per_rider DECIMAL(4,2) DEFAULT NULL,
    median_events_per_rider DECIMAL(4,2) DEFAULT NULL,
    single_event_count INT DEFAULT 0,           -- Participants with exactly 1 event
    single_event_pct DECIMAL(5,2) DEFAULT NULL, -- % single-event
    full_series_count INT DEFAULT 0,            -- Participants who did ALL events
    full_series_pct DECIMAL(5,2) DEFAULT NULL,  -- % full-series

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    INDEX idx_series_year (series_id, season_year),
    INDEX idx_brand (brand_id),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_series_year_brand (series_id, season_year, brand_id, snapshot_id),

    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE
    -- NOTE: snapshot_id FK removed - analytics_snapshots may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: event_unique_participants
-- Tracks participants who ONLY attended this specific event in the series
-- ============================================================================
CREATE TABLE IF NOT EXISTS event_unique_participants (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Scope
    event_id INT NOT NULL,
    season_year YEAR NOT NULL,

    -- Event context (denormalized for reporting)
    series_id INT DEFAULT NULL,
    venue_id INT DEFAULT NULL,
    event_name VARCHAR(255) DEFAULT NULL,
    event_date DATE DEFAULT NULL,

    -- Metrics
    total_participants INT NOT NULL,            -- All participants in this event
    unique_to_event INT NOT NULL,               -- Only attended THIS event in series
    unique_pct DECIMAL(5,2) DEFAULT NULL,       -- % unique

    -- Breakdown of unique participants
    unique_rookies INT DEFAULT 0,               -- First-year participants
    unique_veterans INT DEFAULT 0,              -- Multi-year participants
    unique_by_gender JSON DEFAULT NULL,         -- {"M": 45, "F": 12, "U": 3}

    -- Year-over-year for unique participants
    unique_returned_next_year INT DEFAULT NULL, -- How many unique came back next year
    unique_retention_rate DECIMAL(5,4) DEFAULT NULL,

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    INDEX idx_event (event_id),
    INDEX idx_series_year (series_id, season_year),
    INDEX idx_venue (venue_id),
    INDEX idx_unique_pct (unique_pct DESC),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_event_snapshot (event_id, snapshot_id),

    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL
    -- NOTE: venue_id and snapshot_id FKs removed - tables may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: event_retention_yearly
-- Tracks year-over-year retention for specific events
-- ============================================================================
CREATE TABLE IF NOT EXISTS event_retention_yearly (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Event identification
    event_id INT NOT NULL,                      -- Base event (from_year)
    matched_event_id INT DEFAULT NULL,          -- Matched event in to_year (same venue/series)

    -- Time scope
    from_year YEAR NOT NULL,
    to_year YEAR NOT NULL,

    -- Event context (denormalized)
    series_id INT DEFAULT NULL,
    venue_id INT DEFAULT NULL,
    event_name VARCHAR(255) DEFAULT NULL,

    -- Retention metrics
    participants_from_year INT NOT NULL,        -- Total in from_year
    returned_same_event INT DEFAULT 0,          -- Came back to same event
    returned_same_series INT DEFAULT 0,         -- Came back to series (different event)
    returned_any_event INT DEFAULT 0,           -- Came back to ANY event
    not_returned INT DEFAULT 0,                 -- Did not return at all

    -- Rates
    same_event_retention_rate DECIMAL(5,4) DEFAULT NULL,
    series_retention_rate DECIMAL(5,4) DEFAULT NULL,
    overall_retention_rate DECIMAL(5,4) DEFAULT NULL,

    -- New participants (for growth analysis)
    new_to_event INT DEFAULT 0,                 -- First time at this event
    new_to_series INT DEFAULT 0,                -- First time in series
    new_to_sport INT DEFAULT 0,                 -- Complete rookies

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    INDEX idx_event_years (event_id, from_year, to_year),
    INDEX idx_venue (venue_id),
    INDEX idx_series (series_id),
    INDEX idx_retention (same_event_retention_rate DESC),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_event_years_snapshot (event_id, from_year, to_year, snapshot_id),

    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (matched_event_id) REFERENCES events(id) ON DELETE SET NULL,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL
    -- NOTE: venue_id and snapshot_id FKs removed - tables may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: event_loyal_riders
-- Tracks riders who attend the same event multiple years in a row
-- ============================================================================
CREATE TABLE IF NOT EXISTS event_loyal_riders (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Rider and event
    rider_id INT NOT NULL,
    event_base_id INT NOT NULL,                 -- Representative event (latest)
    venue_id INT DEFAULT NULL,                  -- For venue-based matching
    series_id INT DEFAULT NULL,

    -- Loyalty metrics
    consecutive_years INT NOT NULL,             -- Years in a row attending
    total_years_attended INT NOT NULL,          -- Total years (may have gaps)
    first_year YEAR NOT NULL,
    last_year YEAR NOT NULL,

    -- Participation pattern
    years_attended JSON DEFAULT NULL,           -- [2020, 2021, 2022, 2023]
    events_attended JSON DEFAULT NULL,          -- [event_id_2020, event_id_2021, ...]

    -- Is this rider ONLY attending this event in the series?
    is_single_event_loyalist TINYINT(1) DEFAULT 0,

    -- Performance trend at this event
    avg_position_first_year DECIMAL(6,2) DEFAULT NULL,
    avg_position_last_year DECIMAL(6,2) DEFAULT NULL,
    has_improved TINYINT(1) DEFAULT NULL,

    -- Metadata
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    INDEX idx_rider (rider_id),
    INDEX idx_event (event_base_id),
    INDEX idx_venue (venue_id),
    INDEX idx_series (series_id),
    INDEX idx_consecutive (consecutive_years DESC),
    INDEX idx_loyalist (is_single_event_loyalist),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_rider_event_snapshot (rider_id, event_base_id, snapshot_id),

    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    FOREIGN KEY (event_base_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL
    -- NOTE: venue_id and snapshot_id FKs removed - tables may not exist yet
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: event_participation_kpi_definitions
-- Metadata for event participation KPIs
-- ============================================================================
CREATE TABLE IF NOT EXISTS event_participation_kpi_definitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kpi_key VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(200) NOT NULL,
    description TEXT,
    category ENUM('distribution', 'uniqueness', 'retention', 'loyalty') NOT NULL,
    data_type ENUM('integer', 'decimal', 'percentage', 'json') NOT NULL,
    unit VARCHAR(50) DEFAULT NULL,
    formula TEXT DEFAULT NULL,
    higher_is_better TINYINT(1) DEFAULT NULL,
    typical_range VARCHAR(100) DEFAULT NULL,
    requires_minimum_n INT DEFAULT 10,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERT: KPI Definitions
-- ============================================================================
INSERT INTO event_participation_kpi_definitions
    (kpi_key, display_name, description, category, data_type, unit, higher_is_better, typical_range, display_order)
VALUES
    -- Distribution KPIs
    ('single_event_pct', 'Single-Event Deltagare', 'Andel som bara deltar i 1 event per serie', 'distribution', 'percentage', '%', NULL, '30-60%', 10),
    ('full_series_pct', 'Hela Serien', 'Andel som deltar i alla event i serien', 'distribution', 'percentage', '%', 1, '5-20%', 11),
    ('avg_events_per_rider', 'Snitt Events/Deltagare', 'Genomsnittligt antal event per deltagare', 'distribution', 'decimal', 'events', 1, '1.5-4.0', 12),

    -- Uniqueness KPIs
    ('unique_to_event_pct', 'Unika till Event', 'Andel deltagare som BARA kommer till detta event', 'uniqueness', 'percentage', '%', NULL, '20-50%', 20),
    ('unique_retention_rate', 'Unik-Retention', 'Hur manga unika aterkom nasta ar', 'uniqueness', 'percentage', '%', 1, '20-40%', 21),

    -- Retention KPIs
    ('same_event_retention', 'Same-Event Retention', 'Andel som aterkom till samma event', 'retention', 'percentage', '%', 1, '40-70%', 30),
    ('series_retention', 'Serie-Retention', 'Andel som aterkom till serien (annan event ok)', 'retention', 'percentage', '%', 1, '50-80%', 31),
    ('new_to_event_pct', 'Nya till Event', 'Andel forstagangsdeltagare pa eventet', 'retention', 'percentage', '%', NULL, '20-50%', 32),

    -- Loyalty KPIs
    ('avg_consecutive_years', 'Snitt Ar i Rad', 'Genomsnittligt antal ar i rad for lojala deltagare', 'loyalty', 'decimal', 'ar', 1, '2-5', 40),
    ('single_event_loyalist_pct', 'Single-Event Lojala', 'Andel lojala som BARA kommer till detta event', 'loyalty', 'percentage', '%', NULL, '30-60%', 41)
ON DUPLICATE KEY UPDATE
    display_name = VALUES(display_name),
    description = VALUES(description);

-- ============================================================================
-- VIEW: event_participation_overview
-- Quick overview for dashboard
-- ============================================================================
CREATE OR REPLACE VIEW event_participation_overview AS
SELECT
    s.id AS series_id,
    s.name AS series_name,
    spd.season_year,
    spd.total_events_in_series,
    spd.total_participants,
    spd.avg_events_per_rider,
    spd.single_event_pct,
    spd.full_series_pct
FROM series_participation_distribution spd
JOIN series s ON spd.series_id = s.id
WHERE spd.brand_id IS NULL  -- Overall stats (no brand filter)
ORDER BY spd.season_year DESC, s.name;

-- ============================================================================
-- VIEW: top_unique_events
-- Events with highest percentage of unique-only participants
-- ============================================================================
CREATE OR REPLACE VIEW top_unique_events AS
SELECT
    eup.event_id,
    eup.event_name,
    eup.event_date,
    s.name AS series_name,
    v.name AS venue_name,
    v.city AS venue_city,
    eup.total_participants,
    eup.unique_to_event,
    eup.unique_pct,
    eup.unique_retention_rate
FROM event_unique_participants eup
LEFT JOIN series s ON eup.series_id = s.id
LEFT JOIN venues v ON eup.venue_id = v.id
WHERE eup.total_participants >= 10  -- GDPR minimum
ORDER BY eup.unique_pct DESC;

-- ============================================================================
-- VIEW: event_retention_leaders
-- Events with best year-over-year retention
-- ============================================================================
CREATE OR REPLACE VIEW event_retention_leaders AS
SELECT
    ery.event_id,
    ery.event_name,
    s.name AS series_name,
    v.name AS venue_name,
    ery.from_year,
    ery.to_year,
    ery.participants_from_year,
    ery.returned_same_event,
    ery.same_event_retention_rate,
    ery.series_retention_rate,
    ery.new_to_event
FROM event_retention_yearly ery
LEFT JOIN series s ON ery.series_id = s.id
LEFT JOIN venues v ON ery.venue_id = v.id
WHERE ery.participants_from_year >= 10  -- GDPR minimum
ORDER BY ery.same_event_retention_rate DESC;

-- ============================================================================
-- VIEW: loyal_rider_summary
-- Aggregated loyalty statistics per event
-- ============================================================================
CREATE OR REPLACE VIEW loyal_rider_summary AS
SELECT
    elr.event_base_id,
    e.name AS event_name,
    s.name AS series_name,
    v.name AS venue_name,
    COUNT(*) AS loyal_riders,
    AVG(elr.consecutive_years) AS avg_consecutive_years,
    MAX(elr.consecutive_years) AS max_consecutive_years,
    SUM(CASE WHEN elr.is_single_event_loyalist = 1 THEN 1 ELSE 0 END) AS single_event_loyalists,
    AVG(CASE WHEN elr.has_improved = 1 THEN 1 ELSE 0 END) AS pct_improved
FROM event_loyal_riders elr
JOIN events e ON elr.event_base_id = e.id
LEFT JOIN series s ON elr.series_id = s.id
LEFT JOIN venues v ON elr.venue_id = v.id
GROUP BY elr.event_base_id, e.name, s.name, v.name
HAVING loyal_riders >= 10  -- GDPR minimum
ORDER BY loyal_riders DESC;

-- ============================================================================
-- Migration complete marker
-- ============================================================================
INSERT INTO analytics_system_config (config_key, config_value, description)
VALUES
    ('event_participation_version', '3.2.0', 'Event Participation Analysis module version'),
    ('event_participation_min_segment', '10', 'Minimum segment size for reporting (GDPR)'),
    ('event_participation_enabled', 'true', 'Enable Event Participation Analysis')
ON DUPLICATE KEY UPDATE config_value = VALUES(config_value);

-- Record migration
INSERT INTO analytics_kpi_audit (kpi_key, old_definition, new_definition, change_type, changed_by, rationale)
VALUES ('_migration_012', NULL, 'Event Participation Analysis tables and views', 'migration', 'system', 'Migration 012 completed')
ON DUPLICATE KEY UPDATE changed_at = NOW();
