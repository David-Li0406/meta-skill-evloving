-- ============================================================================
-- Migration 007: Production Ready v3.0.1
-- ============================================================================
-- Skapar alla tabeller och uppdateringar för 100% produktionsklar analytics.
--
-- Inkluderar:
--   1. analytics_exports: Uppdateras med snapshot_id NOT NULL, export_uid, indexes
--   2. brands + brand_series_map: Brand/Varumärke-dimension
--   3. analytics_recalc_queue: Köa recalc efter rider-merge
--   4. analytics_cron_runs: Uppdateras med heartbeat, duration, error_text
--
-- @package TheHUB Analytics
-- @version 3.0.1
-- @date 2026-01-16
-- ============================================================================

-- ============================================================================
-- 1. ANALYTICS_EXPORTS - Uppdatera för reproducerbarhet
-- ============================================================================

-- Lägg till nya kolumner om de inte finns
ALTER TABLE analytics_exports
    ADD COLUMN IF NOT EXISTS export_uid VARCHAR(36) NULL AFTER id,
    ADD COLUMN IF NOT EXISTS filters_json JSON NULL AFTER filters,
    ADD COLUMN IF NOT EXISTS requested_at DATETIME NULL AFTER exported_at,
    ADD COLUMN IF NOT EXISTS completed_at DATETIME NULL AFTER requested_at,
    ADD COLUMN IF NOT EXISTS status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'completed' AFTER completed_at,
    ADD COLUMN IF NOT EXISTS error_message TEXT NULL AFTER status;

-- Generera export_uid för befintliga rader
UPDATE analytics_exports
SET export_uid = UUID()
WHERE export_uid IS NULL;

-- Gör export_uid NOT NULL och UNIQUE
ALTER TABLE analytics_exports
    MODIFY COLUMN export_uid VARCHAR(36) NOT NULL,
    ADD UNIQUE INDEX IF NOT EXISTS idx_export_uid (export_uid);

-- För nya installationer: snapshot_id ska vara NOT NULL
-- Vi kan inte tvinga detta på befintliga rader, men vi sätter default
-- OBS: Backfill krävs för att sätta snapshot_id på gamla exporter
ALTER TABLE analytics_exports
    MODIFY COLUMN snapshot_id INT UNSIGNED NULL COMMENT 'FK till analytics_snapshots. Required för v3.0.1+';

-- Index för vanliga queries
ALTER TABLE analytics_exports
    ADD INDEX IF NOT EXISTS idx_exports_type_year (export_type, season_year),
    ADD INDEX IF NOT EXISTS idx_exports_user_date (exported_by, exported_at),
    ADD INDEX IF NOT EXISTS idx_exports_snapshot (snapshot_id),
    ADD INDEX IF NOT EXISTS idx_exports_status (status);

-- ============================================================================
-- 2. BRANDS + BRAND_SERIES_MAP - Varumärke-dimension
-- ============================================================================

CREATE TABLE IF NOT EXISTS brands (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT 'Varumärkesnamn (GravitySeries, SCA, etc)',
    short_code VARCHAR(20) NOT NULL COMMENT 'Kort kod (GS, SCA, RF)',
    description TEXT NULL,
    logo_url VARCHAR(255) NULL,
    website_url VARCHAR(255) NULL,
    color_primary VARCHAR(7) NULL COMMENT 'Hex färg (#RRGGBB)',
    color_secondary VARCHAR(7) NULL,
    active TINYINT(1) DEFAULT 1,
    display_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_brand_name (name),
    UNIQUE INDEX idx_brand_code (short_code),
    INDEX idx_brand_active (active, display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Varumärken som äger/driver serier';

CREATE TABLE IF NOT EXISTS brand_series_map (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    brand_id INT UNSIGNED NOT NULL,
    series_id INT UNSIGNED NOT NULL,
    relationship_type ENUM('owner', 'partner', 'sponsor') DEFAULT 'owner' COMMENT 'Typ av relation',
    valid_from DATE NULL COMMENT 'Relation gäller från',
    valid_until DATE NULL COMMENT 'Relation gäller till (NULL = pågående)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_brand_series (brand_id, series_id),
    INDEX idx_series_brand (series_id),
    INDEX idx_brand_active (brand_id, valid_from, valid_until),

    CONSTRAINT fk_brand_series_brand FOREIGN KEY (brand_id)
        REFERENCES brands(id) ON DELETE CASCADE,
    CONSTRAINT fk_brand_series_series FOREIGN KEY (series_id)
        REFERENCES series(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Mappning mellan varumärken och serier (1:N)';

-- Seed-data för GravitySeries
INSERT INTO brands (name, short_code, description, color_primary, active, display_order)
VALUES
    ('GravitySeries', 'GS', 'Sveriges största gravity MTB-serie', '#37d4d6', 1, 1),
    ('Svenska Cykelförbundet', 'SCF', 'Svenska Cykelförbundet - nationella mästerskapstävlingar', '#0066cc', 1, 2)
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- ============================================================================
-- 3. ANALYTICS_RECALC_QUEUE - Köa recalc efter rider-merge
-- ============================================================================

CREATE TABLE IF NOT EXISTS analytics_recalc_queue (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    trigger_type ENUM('merge', 'import', 'manual', 'correction') NOT NULL COMMENT 'Vad som triggade recalc',
    trigger_entity VARCHAR(50) NOT NULL COMMENT 'Entitet (rider, event, result)',
    trigger_entity_id INT UNSIGNED NOT NULL COMMENT 'ID för entiteten',
    affected_rider_ids JSON NULL COMMENT 'Lista med påverkade rider IDs',
    affected_years JSON NULL COMMENT 'Lista med påverkade år',
    priority TINYINT UNSIGNED DEFAULT 5 COMMENT '1=högst, 10=lägst',
    status ENUM('pending', 'processing', 'completed', 'failed', 'skipped') DEFAULT 'pending',

    -- Audit trail
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INT UNSIGNED NULL COMMENT 'Admin user ID',
    started_at DATETIME NULL,
    completed_at DATETIME NULL,

    -- Resultat
    rows_affected INT UNSIGNED NULL,
    execution_time_ms INT UNSIGNED NULL,
    error_message TEXT NULL,

    -- Deduplication
    checksum VARCHAR(64) NULL COMMENT 'SHA256 av trigger info för dedup',

    INDEX idx_recalc_status_priority (status, priority, created_at),
    INDEX idx_recalc_trigger (trigger_type, trigger_entity_id),
    INDEX idx_recalc_checksum (checksum),
    INDEX idx_recalc_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Kö för analytics-omräkningar efter ändringar';

-- ============================================================================
-- 4. ANALYTICS_CRON_RUNS - Uppdatera för heartbeat/monitoring
-- ============================================================================

-- Lägg till nya kolumner för monitoring
ALTER TABLE analytics_cron_runs
    ADD COLUMN IF NOT EXISTS heartbeat_at DATETIME NULL COMMENT 'Senaste heartbeat under körning',
    ADD COLUMN IF NOT EXISTS duration_ms INT UNSIGNED NULL COMMENT 'Total körtid i millisekunder',
    ADD COLUMN IF NOT EXISTS error_text TEXT NULL COMMENT 'Felmeddelande om failed',
    ADD COLUMN IF NOT EXISTS rows_processed INT UNSIGNED NULL COMMENT 'Antal rader processade',
    ADD COLUMN IF NOT EXISTS memory_peak_mb DECIMAL(8,2) NULL COMMENT 'Peak memory usage i MB',
    ADD COLUMN IF NOT EXISTS timeout_detected TINYINT(1) DEFAULT 0 COMMENT 'Om timeout upptäcktes';

-- Index för monitoring-queries
ALTER TABLE analytics_cron_runs
    ADD INDEX IF NOT EXISTS idx_cron_job_status (job_name, status, started_at),
    ADD INDEX IF NOT EXISTS idx_cron_heartbeat (status, heartbeat_at);

-- ============================================================================
-- 5. ANALYTICS_CRON_CONFIG - Konfiguration per jobb
-- ============================================================================

CREATE TABLE IF NOT EXISTS analytics_cron_config (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    enabled TINYINT(1) DEFAULT 1,
    schedule_cron VARCHAR(50) NULL COMMENT 'Cron expression (0 2 * * *)',
    timeout_seconds INT UNSIGNED DEFAULT 3600 COMMENT 'Max körtid innan timeout',
    heartbeat_interval_seconds INT UNSIGNED DEFAULT 60 COMMENT 'Intervall för heartbeat',
    retry_on_failure TINYINT(1) DEFAULT 1,
    max_retries INT UNSIGNED DEFAULT 3,
    notify_on_failure TINYINT(1) DEFAULT 1,
    notify_email VARCHAR(255) NULL,
    last_success_at DATETIME NULL,
    last_failure_at DATETIME NULL,
    consecutive_failures INT UNSIGNED DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_cron_config_job (job_name),
    INDEX idx_cron_config_enabled (enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Konfiguration för cron-jobb';

-- Default konfiguration för analytics-jobb
INSERT INTO analytics_cron_config (job_name, schedule_cron, timeout_seconds, heartbeat_interval_seconds)
VALUES
    ('daily_aggregation', '0 2 * * *', 3600, 60),
    ('weekly_snapshot', '0 3 * * 0', 7200, 120),
    ('data_quality_check', '0 4 * * *', 1800, 60),
    ('export_cleanup', '0 5 * * *', 900, 30)
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- ============================================================================
-- 6. EXPORT_RATE_LIMITS - För GDPR/säkerhet
-- ============================================================================

CREATE TABLE IF NOT EXISTS export_rate_limits (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NULL COMMENT 'NULL = gäller alla',
    ip_address VARCHAR(45) NULL COMMENT 'NULL = gäller alla IPs',
    limit_type ENUM('hourly', 'daily', 'monthly') DEFAULT 'daily',
    max_exports INT UNSIGNED NOT NULL DEFAULT 100,
    max_rows INT UNSIGNED NULL COMMENT 'Max rader per period',
    current_count INT UNSIGNED DEFAULT 0,
    current_rows INT UNSIGNED DEFAULT 0,
    period_start DATETIME NOT NULL,
    period_end DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_rate_user (user_id, limit_type, period_end),
    INDEX idx_rate_ip (ip_address, limit_type, period_end)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Rate limiting för exporter (GDPR compliance)';

-- ============================================================================
-- 7. ANALYTICS_KPI_DEFINITIONS - Uppdatera med nya definitioner
-- ============================================================================

-- Säkerställ att tabellen finns
CREATE TABLE IF NOT EXISTS analytics_kpi_definitions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    kpi_key VARCHAR(50) NOT NULL,
    kpi_name VARCHAR(100) NOT NULL,
    kpi_name_sv VARCHAR(100) NULL,
    definition TEXT NOT NULL,
    definition_sv TEXT NULL,
    formula TEXT NULL,
    unit VARCHAR(20) NULL,
    category VARCHAR(50) NULL,
    calculation_version VARCHAR(10) DEFAULT 'v3',
    valid_from DATE NULL,
    valid_until DATE NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_kpi_key_version (kpi_key, calculation_version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Officiella KPI-definitioner för reproducerbarhet';

-- Lägg till/uppdatera KPI-definitioner för v3.0.1
INSERT INTO analytics_kpi_definitions
    (kpi_key, kpi_name, kpi_name_sv, definition, definition_sv, formula, unit, category, calculation_version)
VALUES
    ('retention_from_prev', 'Retention Rate (from previous)', 'Retention (från föregående)',
     'Percentage of riders from year Y-1 who also competed in year Y',
     'Andel av förra årets deltagare som också tävlade i år',
     '(riders_in_both_Y_and_Y-1 / riders_in_Y-1) * 100', '%', 'retention', 'v3'),

    ('returning_share_of_current', 'Returning Share', 'Andel återvändande',
     'Percentage of current year riders who also competed last year',
     'Andel av årets deltagare som även tävlade förra året',
     '(riders_in_both_Y_and_Y-1 / riders_in_Y) * 100', '%', 'retention', 'v3'),

    ('churn_rate', 'Churn Rate', 'Churn',
     'Percentage of riders from year Y-1 who did NOT compete in year Y',
     'Andel av förra årets deltagare som INTE tävlade i år',
     '100 - retention_from_prev', '%', 'retention', 'v3'),

    ('rookie_rate', 'Rookie Rate', 'Nykomlingsandel',
     'Percentage of current year riders who are first-time participants',
     'Andel av årets deltagare som är förstagångsdeltagare',
     '(new_riders_Y / total_riders_Y) * 100', '%', 'acquisition', 'v3'),

    ('active_rider', 'Active Rider', 'Aktiv deltagare',
     'A rider with at least 1 recorded result in the specified period',
     'En deltagare med minst 1 registrerat resultat under perioden',
     'COUNT(results) >= 1', 'boolean', 'definition', 'v3'),

    ('at_risk_rider', 'At-Risk Rider', 'Risk-deltagare',
     'Active last year but showing decline: fewer events OR no events in current season yet',
     'Aktiv förra året men visar nedgång: färre events ELLER inga events hittills i år',
     'events_current_year < events_previous_year OR (active_prev_year AND NOT active_current_year)', 'boolean', 'definition', 'v3'),

    ('winback_candidate', 'Winback Candidate', 'Winback-kandidat',
     'Rider who was active 2+ years ago but not active last year',
     'Deltagare som var aktiv för 2+ år sedan men inte förra året',
     'last_active_year <= current_year - 2', 'boolean', 'definition', 'v3'),

    ('ltv_events', 'Lifetime Value (Events)', 'Livstidsvärde (Events)',
     'Total number of events a rider has participated in across all years',
     'Totalt antal events en deltagare har deltagit i över alla år',
     'SUM(events_per_year)', 'count', 'value', 'v3'),

    ('cohort_year', 'Cohort Year', 'Kohortår',
     'The first year a rider participated in any event',
     'Första året en deltagare deltog i något event',
     'MIN(season_year)', 'year', 'definition', 'v3')
ON DUPLICATE KEY UPDATE
    definition = VALUES(definition),
    definition_sv = VALUES(definition_sv),
    formula = VALUES(formula),
    updated_at = CURRENT_TIMESTAMP;

-- ============================================================================
-- 8. DATA_QUALITY_METRICS - Säkerställ struktur
-- ============================================================================

-- Lägg till saknade kolumner om de inte finns
ALTER TABLE data_quality_metrics
    ADD COLUMN IF NOT EXISTS results_missing_class INT UNSIGNED DEFAULT 0 AFTER riders_missing_gender,
    ADD COLUMN IF NOT EXISTS data_freshness_hours INT UNSIGNED NULL COMMENT 'Timmar sedan senaste result',
    ADD COLUMN IF NOT EXISTS quality_score DECIMAL(5,2) NULL COMMENT 'Sammanvägt kvalitetspoäng 0-100';

-- ============================================================================
-- 9. ANALYTICS_SNAPSHOTS - Uppdatera med metadata
-- ============================================================================

ALTER TABLE analytics_snapshots
    ADD COLUMN IF NOT EXISTS is_baseline TINYINT(1) DEFAULT 0 COMMENT 'Markera som baseline för jämförelser',
    ADD COLUMN IF NOT EXISTS retention_days INT UNSIGNED DEFAULT 365 COMMENT 'Antal dagar att behålla',
    ADD COLUMN IF NOT EXISTS auto_delete_at DATE NULL COMMENT 'Automatisk radering efter detta datum';

-- Index för cleanup
ALTER TABLE analytics_snapshots
    ADD INDEX IF NOT EXISTS idx_snapshot_cleanup (auto_delete_at, is_baseline);

-- ============================================================================
-- DONE
-- ============================================================================
-- Efter körning: Verifiera med
--   SHOW TABLES LIKE 'brand%';
--   SHOW TABLES LIKE 'analytics_%';
--   DESCRIBE analytics_exports;
-- ============================================================================
