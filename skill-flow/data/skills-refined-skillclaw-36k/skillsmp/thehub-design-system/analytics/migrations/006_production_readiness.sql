-- ============================================================================
-- Migration 006: Production Readiness - Snapshot v2 & Export Logging
-- ============================================================================
--
-- Denna migration implementerar:
-- 1. Utokad analytics_snapshots tabell (v2) for reproducerbarhet
-- 2. analytics_exports tabell for GDPR-loggning och sparbarhet
-- 3. data_quality_metrics tabell for datakvalitetsspårning
--
-- Krav enligt SCF-granskning 2026-01-16
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. UTOKA analytics_snapshots (v2)
-- ----------------------------------------------------------------------------

-- Lagg till nya kolumner for reproducerbarhet
ALTER TABLE analytics_snapshots
    ADD COLUMN IF NOT EXISTS generated_at TIMESTAMP NULL DEFAULT NULL COMMENT 'Exakt tidpunkt da snapshot genererades',
    ADD COLUMN IF NOT EXISTS season_year INT NULL COMMENT 'Vilket sasongsar snapshot galler',
    ADD COLUMN IF NOT EXISTS source_max_updated_at TIMESTAMP NULL DEFAULT NULL COMMENT 'MAX(updated_at) fran kalldata vid generering',
    ADD COLUMN IF NOT EXISTS code_version VARCHAR(20) NULL COMMENT 'Platform/berakningsversion (t.ex. 3.0.0)',
    ADD COLUMN IF NOT EXISTS calculation_params JSON NULL COMMENT 'Parametrar som anvandes vid berakning',
    ADD COLUMN IF NOT EXISTS data_fingerprint VARCHAR(64) NULL COMMENT 'SHA256 hash av metrics for verifiering';

-- Index for snabb uppslagning per ar och typ
CREATE INDEX IF NOT EXISTS idx_snapshots_season_type
    ON analytics_snapshots(season_year, snapshot_type);

-- Index for att hitta senaste snapshot
CREATE INDEX IF NOT EXISTS idx_snapshots_generated
    ON analytics_snapshots(generated_at DESC);

-- ----------------------------------------------------------------------------
-- 2. SKAPA analytics_exports (for GDPR och sparbarhet)
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS analytics_exports (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Exportmetadata
    export_type VARCHAR(50) NOT NULL COMMENT 'Typ: riders_at_risk, cohort, winback, etc.',
    export_format VARCHAR(20) NOT NULL DEFAULT 'csv' COMMENT 'Format: csv, pdf, json',
    filename VARCHAR(255) NULL COMMENT 'Genererat filnamn',

    -- Vem och nar
    exported_by INT NULL COMMENT 'User ID som exporterade',
    exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL COMMENT 'IP-adress (for GDPR)',

    -- Filter och parametrar
    season_year INT NULL COMMENT 'Vilket ar som exporterades',
    series_id INT NULL COMMENT 'Filtrering pa serie (om relevant)',
    filters JSON NULL COMMENT 'Alla filter som anvandes',

    -- Innehall
    row_count INT NOT NULL DEFAULT 0 COMMENT 'Antal rader i exporten',
    contains_pii TINYINT(1) NOT NULL DEFAULT 0 COMMENT '1 om exporten innehaller persondata',

    -- Reproducerbarhet
    snapshot_id INT NULL COMMENT 'Referens till snapshot som anvandes',
    data_fingerprint VARCHAR(64) NULL COMMENT 'SHA256 hash av exportdata',
    source_query_hash VARCHAR(64) NULL COMMENT 'Hash av SQL-query for reproducerbarhet',

    -- Manifest for full sparbarhet
    manifest JSON NULL COMMENT 'Komplett manifest med alla detaljer',

    -- Index
    INDEX idx_exports_user (exported_by),
    INDEX idx_exports_date (exported_at),
    INDEX idx_exports_type (export_type),
    INDEX idx_exports_year (season_year),
    INDEX idx_exports_pii (contains_pii),

    -- Foreign keys (soft - inga constraints for flexibilitet)
    INDEX idx_exports_snapshot (snapshot_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Logg over alla analytics-exporter for GDPR och reproducerbarhet';

-- ----------------------------------------------------------------------------
-- 3. SKAPA data_quality_metrics (for datakvalitetspanel)
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS data_quality_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Nar och for vilket ar
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    season_year INT NOT NULL COMMENT 'Sasong som mats',

    -- Tacking per falt (procent 0-100)
    birth_year_coverage DECIMAL(5,2) NULL COMMENT '% riders med birth_year',
    club_coverage DECIMAL(5,2) NULL COMMENT '% riders med club_id',
    region_coverage DECIMAL(5,2) NULL COMMENT '% riders med region',
    class_coverage DECIMAL(5,2) NULL COMMENT '% results med class_id',
    gender_coverage DECIMAL(5,2) NULL COMMENT '% riders med gender',
    event_date_coverage DECIMAL(5,2) NULL COMMENT '% events med datum',

    -- Absoluta tal
    total_riders INT NULL COMMENT 'Totalt antal riders for aret',
    riders_missing_birth_year INT NULL,
    riders_missing_club INT NULL,
    riders_missing_region INT NULL,
    riders_missing_gender INT NULL,
    results_missing_class INT NULL,
    events_missing_date INT NULL,

    -- Dubbletter och identity issues
    potential_duplicates INT NULL COMMENT 'Antal potentiella dubbletter',
    merged_riders INT NULL COMMENT 'Antal sammanslagna riders',
    orphan_results INT NULL COMMENT 'Resultat utan giltig rider',

    -- Metadata
    calculation_version VARCHAR(20) NULL,

    -- Index
    UNIQUE KEY uk_quality_year (season_year, DATE(measured_at)),
    INDEX idx_quality_date (measured_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Daglig datakvalitetsmatning per sasong';

-- ----------------------------------------------------------------------------
-- 4. SKAPA analytics_kpi_definitions (for dokumentation)
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS analytics_kpi_definitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kpi_code VARCHAR(50) NOT NULL UNIQUE COMMENT 'Unik KPI-kod (t.ex. retention_from_prev)',
    kpi_name VARCHAR(100) NOT NULL COMMENT 'Lasbart namn',
    kpi_category VARCHAR(50) NOT NULL COMMENT 'Kategori: retention, growth, demographics, etc.',
    description TEXT NOT NULL COMMENT 'Fullstandig beskrivning av KPI',
    formula TEXT NULL COMMENT 'Matematisk formel',
    numerator_desc VARCHAR(255) NULL COMMENT 'Beskrivning av taljare',
    denominator_desc VARCHAR(255) NULL COMMENT 'Beskrivning av namnare',
    unit VARCHAR(20) NULL COMMENT 'Enhet: %, antal, etc.',
    implementation_method VARCHAR(100) NULL COMMENT 'PHP-metod som implementerar KPI',
    valid_from DATE NULL COMMENT 'Giltig fran datum',
    valid_to DATE NULL COMMENT 'Giltig till datum (null = aktiv)',
    notes TEXT NULL COMMENT 'Extra anteckningar',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Dokumentation av alla KPI-definitioner';

-- Lagg in standarddefinitioner
INSERT INTO analytics_kpi_definitions (kpi_code, kpi_name, kpi_category, description, formula, numerator_desc, denominator_desc, unit, implementation_method) VALUES
('retention_from_prev', 'Retention Rate', 'retention',
 'Andel av forra arets riders som aterkommer detta ar. Svarar pa: Hur manga av forra arets deltagare kom tillbaka?',
 '(riders i bade ar N och N-1) / (riders i ar N-1) * 100',
 'Riders som deltog bade ar N och ar N-1',
 'Riders som deltog ar N-1',
 '%', 'KPICalculator::getRetentionRate'),

('returning_share', 'Returning Share', 'retention',
 'Andel av arets riders som ocksa deltog forra aret. Svarar pa: Hur stor del av arets deltagare ar aterkommande?',
 '(riders i bade ar N och N-1) / (riders i ar N) * 100',
 'Riders som deltog bade ar N och ar N-1',
 'Riders som deltog ar N',
 '%', 'KPICalculator::getReturningShareOfCurrent'),

('churn_rate', 'Churn Rate', 'retention',
 'Andel av forra arets riders som INTE aterkommer. Svarar pa: Hur manga av forra arets deltagare forsvann?',
 '100 - retention_from_prev',
 'Riders i ar N-1 som EJ finns i ar N',
 'Riders som deltog ar N-1',
 '%', 'KPICalculator::getChurnRate'),

('rookie_rate', 'Rookie Rate', 'growth',
 'Andel av arets riders som ar nya (forsta aret). Svarar pa: Hur stor andel ar nyborjare?',
 '(riders dar MIN(season_year) = N) / (alla riders ar N) * 100',
 'Riders med forsta sasong ar N',
 'Alla riders ar N',
 '%', 'KPICalculator::getRookieRate'),

('growth_rate', 'Growth Rate', 'growth',
 'Procentuell forandring i antal aktiva riders jamfort med forra aret.',
 '((riders ar N) - (riders ar N-1)) / (riders ar N-1) * 100',
 'Skillnad i antal riders',
 'Riders forra aret',
 '%', 'KPICalculator::getGrowthRate'),

('active_riders', 'Active Riders', 'core',
 'Antal unika riders med minst 1 event-deltagande under aret.',
 'COUNT(DISTINCT rider_id) WHERE events >= ACTIVE_MIN_EVENTS',
 NULL, NULL,
 'antal', 'KPICalculator::getTotalActiveRiders')

ON DUPLICATE KEY UPDATE
    description = VALUES(description),
    formula = VALUES(formula),
    updated_at = CURRENT_TIMESTAMP;

-- ----------------------------------------------------------------------------
-- 5. INDEX for battre performance
-- ----------------------------------------------------------------------------

-- Index for snabbare retention-berakningar
CREATE INDEX IF NOT EXISTS idx_rys_rider_year
    ON rider_yearly_stats(rider_id, season_year);

-- Index for snabbare cohort-lookups
CREATE INDEX IF NOT EXISTS idx_rys_rookie_year
    ON rider_yearly_stats(is_rookie, season_year);

-- ----------------------------------------------------------------------------
-- Klar!
-- ----------------------------------------------------------------------------
