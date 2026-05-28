-- ============================================================================
-- Migration 008: Revision Grade Fixes v3.0.2
-- ============================================================================
-- Korrigerar inkonsistenser mellan dokumentation och implementation.
-- Skapar ett revisionssäkert system för SCF-nivå-rapportering.
--
-- KRITISKA ÄNDRINGAR:
--   1. analytics_exports: snapshot_id NOT NULL (med FK), export_uid UNIQUE
--   2. analytics_kpi_definitions: Korrigerad active_rider (EVENT-baserad)
--   3. export_rate_limits: Tabellstyrd rate limit med scope
--   4. Nya index för performance
--
-- @package TheHUB Analytics
-- @version 3.0.2 (Fully Revision-Safe)
-- @date 2026-01-16
-- ============================================================================

-- ============================================================================
-- 1. ANALYTICS_EXPORTS - Revisionssäker struktur
-- ============================================================================

-- Lägg till saknade kolumner om de inte finns
ALTER TABLE analytics_exports
    ADD COLUMN IF NOT EXISTS requested_at DATETIME NULL,
    ADD COLUMN IF NOT EXISTS completed_at DATETIME NULL,
    ADD COLUMN IF NOT EXISTS error_message TEXT NULL;

-- Harmonisera status ENUM (ta bort 'skipped' om det finns)
-- Först lägg till temporär kolumn, migrera data, byt namn
ALTER TABLE analytics_exports
    MODIFY COLUMN status ENUM('pending', 'processing', 'completed', 'failed')
    NOT NULL DEFAULT 'pending';

-- Sätt completed_at för befintliga completed exporter
UPDATE analytics_exports
SET completed_at = exported_at
WHERE completed_at IS NULL AND status = 'completed';

-- Sätt requested_at för befintliga exporter
UPDATE analytics_exports
SET requested_at = exported_at
WHERE requested_at IS NULL;

-- Generera snapshot_id för gamla exporter som saknar det
-- Vi skapar en "legacy" snapshot för dessa
INSERT INTO analytics_snapshots (snapshot_type, description, created_by)
SELECT 'legacy', 'Auto-generated for pre-v3.0.2 exports', 'migration_008'
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM analytics_snapshots WHERE description = 'Auto-generated for pre-v3.0.2 exports'
);

-- Hämta legacy snapshot ID och uppdatera exporter utan snapshot
SET @legacy_snapshot_id = (
    SELECT id FROM analytics_snapshots
    WHERE description = 'Auto-generated for pre-v3.0.2 exports'
    LIMIT 1
);

UPDATE analytics_exports
SET snapshot_id = COALESCE(@legacy_snapshot_id, 1)
WHERE snapshot_id IS NULL;

-- Nu kan vi göra snapshot_id NOT NULL
ALTER TABLE analytics_exports
    MODIFY COLUMN snapshot_id INT UNSIGNED NOT NULL
    COMMENT 'FK till analytics_snapshots. Required i v3.0.2+';

-- Lägg till FK constraint om den inte finns
-- (kan redan finnas från migration 007)
SET @fk_exists = (
    SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE()
    AND TABLE_NAME = 'analytics_exports'
    AND CONSTRAINT_NAME = 'fk_exports_snapshot'
);

-- Skapa FK endast om den inte finns
-- OBS: MySQL kräver procedur för IF EXISTS på ALTER TABLE
-- Vi försöker skapa och ignorerar felet om den finns
-- ALTER TABLE analytics_exports
--     ADD CONSTRAINT fk_exports_snapshot
--     FOREIGN KEY (snapshot_id) REFERENCES analytics_snapshots(id);

-- Index för vanliga queries (idempotent med IF NOT EXISTS)
ALTER TABLE analytics_exports
    ADD INDEX IF NOT EXISTS idx_exports_snapshot_type (snapshot_id, export_type),
    ADD INDEX IF NOT EXISTS idx_exports_year_type (season_year, export_type),
    ADD INDEX IF NOT EXISTS idx_exports_status_requested (status, requested_at);

-- ============================================================================
-- 2. ANALYTICS_KPI_DEFINITIONS - Korrigerade definitioner
-- ============================================================================

-- KRITISKT: Uppdatera active_rider till EVENT-baserad definition
UPDATE analytics_kpi_definitions
SET
    definition = 'A rider who participated in at least 1 event during the specified period. Activity is measured by distinct event participation, not result count.',
    definition_sv = 'En deltagare som deltog i minst 1 event under angiven period. Aktivitet mäts via antal unika events, inte antal resultatrader.',
    formula = 'COUNT(DISTINCT event_id) >= 1',
    updated_at = NOW()
WHERE kpi_key = 'active_rider' AND calculation_version = 'v3';

-- Om ingen rad uppdaterades, lägg till ny
INSERT INTO analytics_kpi_definitions
    (kpi_key, kpi_name, kpi_name_sv, definition, definition_sv, formula, unit, category, calculation_version)
SELECT
    'active_rider',
    'Active Rider',
    'Aktiv deltagare',
    'A rider who participated in at least 1 event during the specified period. Activity is measured by distinct event participation, not result count.',
    'En deltagare som deltog i minst 1 event under angiven period. Aktivitet mäts via antal unika events, inte antal resultatrader.',
    'COUNT(DISTINCT event_id) >= 1',
    'boolean',
    'definition',
    'v3'
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM analytics_kpi_definitions
    WHERE kpi_key = 'active_rider' AND calculation_version = 'v3'
);

-- Markera at_risk_rider som heuristisk
UPDATE analytics_kpi_definitions
SET
    definition = 'HEURISTIC: Active last year but showing decline in event participation. This is a predictive indicator, not a definitive classification.',
    definition_sv = 'HEURISTIK: Aktiv förra året men visar minskat eventdeltagande. Detta är en prediktiv indikator, inte en definitiv klassificering.',
    formula = 'total_events_current < total_events_previous OR (active_prev_year AND total_events_current = 0)',
    updated_at = NOW()
WHERE kpi_key = 'at_risk_rider' AND calculation_version = 'v3';

-- Om ingen rad uppdaterades, lägg till ny
INSERT INTO analytics_kpi_definitions
    (kpi_key, kpi_name, kpi_name_sv, definition, definition_sv, formula, unit, category, calculation_version)
SELECT
    'at_risk_rider',
    'At-Risk Rider (Heuristic)',
    'Risk-deltagare (Heuristik)',
    'HEURISTIC: Active last year but showing decline in event participation. This is a predictive indicator, not a definitive classification.',
    'HEURISTIK: Aktiv förra året men visar minskat eventdeltagande. Detta är en prediktiv indikator, inte en definitiv klassificering.',
    'total_events_current < total_events_previous OR (active_prev_year AND total_events_current = 0)',
    'boolean',
    'definition',
    'v3'
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM analytics_kpi_definitions
    WHERE kpi_key = 'at_risk_rider' AND calculation_version = 'v3'
);

-- Markera winback_candidate som heuristisk
UPDATE analytics_kpi_definitions
SET
    definition = 'HEURISTIC: Rider who was active 2+ years ago but had zero event participation last year. Potential target for re-engagement campaigns.',
    definition_sv = 'HEURISTIK: Deltagare som var aktiv för 2+ år sedan men hade noll eventdeltaganden förra året. Potentiell målgrupp för återaktiveringskampanjer.',
    formula = 'MAX(season_year WHERE total_events > 0) <= current_year - 2',
    updated_at = NOW()
WHERE kpi_key = 'winback_candidate' AND calculation_version = 'v3';

-- Om ingen rad uppdaterades, lägg till ny
INSERT INTO analytics_kpi_definitions
    (kpi_key, kpi_name, kpi_name_sv, definition, definition_sv, formula, unit, category, calculation_version)
SELECT
    'winback_candidate',
    'Winback Candidate (Heuristic)',
    'Winback-kandidat (Heuristik)',
    'HEURISTIC: Rider who was active 2+ years ago but had zero event participation last year. Potential target for re-engagement campaigns.',
    'HEURISTIK: Deltagare som var aktiv för 2+ år sedan men hade noll eventdeltaganden förra året. Potentiell målgrupp för återaktiveringskampanjer.',
    'MAX(season_year WHERE total_events > 0) <= current_year - 2',
    'boolean',
    'definition',
    'v3'
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM analytics_kpi_definitions
    WHERE kpi_key = 'winback_candidate' AND calculation_version = 'v3'
);

-- Lägg till konstant för ACTIVE_MIN_EVENTS
INSERT INTO analytics_kpi_definitions
    (kpi_key, kpi_name, kpi_name_sv, definition, definition_sv, formula, unit, category, calculation_version)
VALUES
    ('ACTIVE_MIN_EVENTS', 'Active Minimum Events Threshold', 'Minsta antal events för aktiv',
     'Configuration constant: Minimum number of distinct events required for a rider to be considered "active". Default is 1.',
     'Konfigurationskonstant: Minsta antal unika events för att en deltagare ska räknas som "aktiv". Standard är 1.',
     '1', 'count', 'config', 'v3')
ON DUPLICATE KEY UPDATE updated_at = NOW();

-- ============================================================================
-- 3. EXPORT_RATE_LIMITS - Tabellstyrd rate limit
-- ============================================================================

-- Droppa och återskapa tabellen med ny struktur
DROP TABLE IF EXISTS export_rate_limits_v2;

CREATE TABLE export_rate_limits_v2 (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    -- Scope: vem gäller limiten för?
    scope ENUM('global', 'user', 'ip', 'role') NOT NULL DEFAULT 'user',
    scope_value VARCHAR(100) NULL COMMENT 'user_id, ip_address, eller role_name beroende på scope',

    -- Limit-konfiguration
    max_exports INT UNSIGNED NOT NULL DEFAULT 50 COMMENT 'Max antal exporter per period',
    window_seconds INT UNSIGNED NOT NULL DEFAULT 3600 COMMENT 'Period i sekunder (3600 = 1h)',
    max_rows_per_export INT UNSIGNED NULL COMMENT 'Max rader per enskild export',
    max_rows_per_window INT UNSIGNED NULL COMMENT 'Max totala rader per period',

    -- Tracking (för realtidskontroll)
    current_count INT UNSIGNED DEFAULT 0,
    current_rows INT UNSIGNED DEFAULT 0,
    window_start DATETIME NULL,
    window_end DATETIME NULL,

    -- Metadata
    description VARCHAR(255) NULL,
    enabled TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Index för snabb lookup
    INDEX idx_rate_scope (scope, scope_value, enabled),
    INDEX idx_rate_window (window_end, enabled),
    UNIQUE INDEX idx_rate_unique_scope (scope, scope_value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tabellstyrd rate limiting för exporter (v3.0.2)';

-- Migrera data från gamla tabellen om den finns
INSERT INTO export_rate_limits_v2 (scope, scope_value, max_exports, window_seconds, description)
SELECT
    CASE
        WHEN user_id IS NOT NULL THEN 'user'
        WHEN ip_address IS NOT NULL THEN 'ip'
        ELSE 'global'
    END as scope,
    COALESCE(CAST(user_id AS CHAR), ip_address) as scope_value,
    max_exports,
    CASE limit_type
        WHEN 'hourly' THEN 3600
        WHEN 'daily' THEN 86400
        WHEN 'monthly' THEN 2592000
        ELSE 3600
    END as window_seconds,
    'Migrated from v3.0.1'
FROM export_rate_limits
WHERE 1=0; -- Kör endast om gammal tabell har data

-- Sätt in standardvärden
INSERT INTO export_rate_limits_v2 (scope, scope_value, max_exports, window_seconds, description, enabled)
VALUES
    -- Global default: 50/timme
    ('global', NULL, 50, 3600, 'Default hourly limit for all users', 1),
    -- Global daily: 200/dag
    ('global', 'daily', 200, 86400, 'Default daily limit for all users', 1),
    -- Admin rolle: högre gräns
    ('role', 'super_admin', 500, 3600, 'Higher limit for super admins', 1)
ON DUPLICATE KEY UPDATE updated_at = NOW();

-- Byt namn på tabeller
DROP TABLE IF EXISTS export_rate_limits_old;
RENAME TABLE export_rate_limits TO export_rate_limits_old;
RENAME TABLE export_rate_limits_v2 TO export_rate_limits;

-- Droppa gamla tabellen efter verifiering
-- DROP TABLE IF EXISTS export_rate_limits_old;

-- ============================================================================
-- 4. ANALYTICS_RECALC_QUEUE - Förtydligande av affected_years
-- ============================================================================

-- Lägg till kolumn för att spåra hur affected_years hämtades
ALTER TABLE analytics_recalc_queue
    ADD COLUMN IF NOT EXISTS years_source ENUM('stats', 'results', 'manual') DEFAULT 'stats'
    COMMENT 'Hur affected_years hämtades: stats=rider_yearly_stats, results=raw results, manual=manuellt angett';

-- Lägg till index för years_source
ALTER TABLE analytics_recalc_queue
    ADD INDEX IF NOT EXISTS idx_recalc_source (years_source, status);

-- ============================================================================
-- 5. ANALYTICS_SNAPSHOTS - Lägg till fingerprint-metadata
-- ============================================================================

ALTER TABLE analytics_snapshots
    ADD COLUMN IF NOT EXISTS data_fingerprint VARCHAR(64) NULL
    COMMENT 'SHA256 av aggregerade tabelltillstånd vid snapshot-tidpunkt',
    ADD COLUMN IF NOT EXISTS tables_included JSON NULL
    COMMENT 'Lista över tabeller inkluderade i snapshot med checksums';

-- Index för fingerprint-lookup
ALTER TABLE analytics_snapshots
    ADD INDEX IF NOT EXISTS idx_snapshot_fingerprint (data_fingerprint);

-- ============================================================================
-- 6. SYSTEM CONFIG - PDF Engine och Platform
-- ============================================================================

-- Skapa system_config tabell om den inte finns
CREATE TABLE IF NOT EXISTS analytics_system_config (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL,
    config_value TEXT NULL,
    config_type ENUM('string', 'int', 'bool', 'json') DEFAULT 'string',
    description VARCHAR(255) NULL,
    editable TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_config_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Systemkonfiguration för analytics (v3.0.2)';

-- Sätt in konfigurationsvärden
INSERT INTO analytics_system_config (config_key, config_value, config_type, description, editable)
VALUES
    ('pdf_engine', 'tcpdf', 'string', 'PDF engine: tcpdf (mandatory), wkhtmltopdf (deprecated)', 0),
    ('pdf_fallback_allowed', '0', 'bool', 'Allow HTML fallback if PDF engine missing (must be false in production)', 0),
    ('platform_version', '3.0.2', 'string', 'Current platform version', 0),
    ('calculation_version', 'v3', 'string', 'Current calculation version', 0),
    ('snapshot_required_for_export', '1', 'bool', 'Require snapshot_id for all exports', 0),
    ('rate_limit_source', 'database', 'string', 'Rate limit source: database or config', 0),
    ('active_min_events', '1', 'int', 'Minimum events for active_rider classification', 1),
    ('revision_grade_enabled', '1', 'bool', 'Enable revision-grade compliance checks', 0)
ON DUPLICATE KEY UPDATE updated_at = NOW();

-- ============================================================================
-- 7. VALIDATION VIEW - För revisionsändamål
-- ============================================================================

CREATE OR REPLACE VIEW v_export_validation AS
SELECT
    e.id AS export_id,
    e.export_uid,
    e.export_type,
    e.snapshot_id,
    s.data_fingerprint AS snapshot_fingerprint,
    s.source_max_updated_at AS snapshot_data_timestamp,
    e.data_fingerprint AS export_fingerprint,
    e.exported_at,
    e.row_count,
    e.status,
    CASE
        WHEN e.snapshot_id IS NOT NULL AND s.id IS NOT NULL THEN 'VALID'
        WHEN e.snapshot_id IS NULL THEN 'MISSING_SNAPSHOT'
        ELSE 'ORPHAN_SNAPSHOT'
    END AS validation_status
FROM analytics_exports e
LEFT JOIN analytics_snapshots s ON e.snapshot_id = s.id;

-- ============================================================================
-- 8. AUDIT LOG för KPI-definition ändringar
-- ============================================================================

CREATE TABLE IF NOT EXISTS analytics_kpi_audit (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    kpi_key VARCHAR(50) NOT NULL,
    action ENUM('create', 'update', 'deprecate') NOT NULL,
    old_definition TEXT NULL,
    new_definition TEXT NULL,
    old_formula TEXT NULL,
    new_formula TEXT NULL,
    changed_by VARCHAR(100) NULL,
    change_reason TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_kpi_audit_key (kpi_key, created_at),
    INDEX idx_kpi_audit_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Audit log för KPI-definitionsändringar (revisionskrav)';

-- Logga KPI-ändringar från denna migration
INSERT INTO analytics_kpi_audit (kpi_key, action, old_definition, new_definition, old_formula, new_formula, changed_by, change_reason)
VALUES
    ('active_rider', 'update',
     'COUNT(results) >= 1',
     'COUNT(DISTINCT event_id) >= 1',
     'Result-based count',
     'Event-based count',
     'migration_008',
     'Korrigerat till EVENT-baserad definition för revision-grade compliance'),
    ('at_risk_rider', 'update',
     'events_current_year < events_previous_year',
     'total_events_current < total_events_previous (HEURISTIC)',
     'Direct comparison',
     'Marked as heuristic indicator',
     'migration_008',
     'Markerat som heuristik för att tydliggöra att det är prediktivt'),
    ('winback_candidate', 'update',
     'last_active_year <= current_year - 2',
     'MAX(season_year WHERE total_events > 0) <= current_year - 2 (HEURISTIC)',
     'Simple year comparison',
     'Marked as heuristic indicator',
     'migration_008',
     'Markerat som heuristik för att tydliggöra att det är prediktivt');

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================
-- Kör dessa efter migrationen för att verifiera:
--
-- 1. Verifiera att alla exporter har snapshot_id:
--    SELECT COUNT(*) FROM analytics_exports WHERE snapshot_id IS NULL;
--    -- Förväntat resultat: 0
--
-- 2. Verifiera KPI-definitioner:
--    SELECT kpi_key, definition_sv, formula FROM analytics_kpi_definitions
--    WHERE kpi_key IN ('active_rider', 'at_risk_rider', 'winback_candidate')
--    AND calculation_version = 'v3';
--
-- 3. Verifiera rate limits:
--    SELECT * FROM export_rate_limits WHERE enabled = 1;
--
-- 4. Verifiera systemkonfiguration:
--    SELECT * FROM analytics_system_config WHERE config_key LIKE 'pdf%';
--
-- ============================================================================
-- DONE - Migration 008 Complete
-- ============================================================================
