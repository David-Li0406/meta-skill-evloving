-- ============================================================================
-- GOVERNANCE CORE TABLES
-- TheHUB Analytics Platform
-- Version: 1.0
-- Kor FORE Steg 1
-- ============================================================================

-- Hantera dubbletter: Merge-mappning
-- Denna tabell haller reda pa vilka rider_id som ar dubbletter
-- och pekar till den kanoniska (huvudsakliga) rider_id.
CREATE TABLE IF NOT EXISTS rider_merge_map (
    id INT AUTO_INCREMENT PRIMARY KEY,
    canonical_rider_id INT NOT NULL COMMENT 'Huvudprofilen som behalles',
    merged_rider_id INT NOT NULL COMMENT 'Dubblettprofilen som pekar till canonical',
    reason VARCHAR(255) NULL COMMENT 'Anledning till merge (t.ex. same_uci_id, manual)',
    confidence DECIMAL(5,2) DEFAULT 100.00 COMMENT 'Konfidens 0-100%',
    status ENUM('pending','approved','rejected') DEFAULT 'approved',
    merged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    merged_by VARCHAR(100) NULL COMMENT 'Anvandare som skapade merge',
    reviewed_at TIMESTAMP NULL,
    reviewed_by VARCHAR(100) NULL,
    UNIQUE KEY uniq_merged (merged_rider_id),
    INDEX idx_canonical (canonical_rider_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Audit-logg for identity-andringar
-- Loggar alla forandringar av rider-identiteter for sparbarhet
CREATE TABLE IF NOT EXISTS rider_identity_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL COMMENT 'Rider som paverkades',
    action ENUM('merge','unmerge','update_identity','create','delete') NOT NULL,
    details JSON NULL COMMENT 'Detaljer om andringen',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NULL,
    INDEX idx_rider (rider_id),
    INDEX idx_action_time (action, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Klubbhistorik (ersatter riders.club_id for analytics)
-- Mojliggor analys av klubbyten over tid
CREATE TABLE IF NOT EXISTS rider_affiliations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL COMMENT 'Canonical rider_id',
    club_id INT NOT NULL,
    valid_from DATE NULL COMMENT 'Startdatum for medlemskap',
    valid_to DATE NULL COMMENT 'Slutdatum (NULL = fortfarande aktiv)',
    source ENUM('manual','derived','import','scf') DEFAULT 'derived',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rider (rider_id),
    INDEX idx_club (club_id),
    INDEX idx_rider_period (rider_id, valid_from, valid_to)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Cron-korningar med las mot dubbelkorning
-- Forhindrar att samma jobb kors samtidigt
CREATE TABLE IF NOT EXISTS analytics_cron_runs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_name VARCHAR(50) NOT NULL COMMENT 'T.ex. daily-stats, monthly-snapshot',
    run_key VARCHAR(50) NOT NULL COMMENT 'Unik nyckel for korningen (t.ex. 2025-01-13)',
    status ENUM('started','success','failed','skipped') DEFAULT 'started',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP NULL,
    duration_ms INT NULL COMMENT 'Tid i millisekunder',
    rows_affected INT DEFAULT 0,
    log JSON NULL COMMENT 'Detaljerad logg',
    UNIQUE KEY uniq_job_run (job_name, run_key),
    INDEX idx_job (job_name, started_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Generell loggning for analytics
CREATE TABLE IF NOT EXISTS analytics_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level ENUM('debug','info','warn','error','critical') DEFAULT 'info',
    job_name VARCHAR(100) NULL COMMENT 'Vilket jobb/script som loggade',
    message VARCHAR(500) NOT NULL,
    context JSON NULL COMMENT 'Extra data',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_level_time (level, created_at),
    INDEX idx_job (job_name, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- ============================================================================
-- VIEW: Canonical Riders
-- Anvands i alla analytics-queries for att alltid fa ratt rider_id
-- Om en rider har mergats, returneras canonical_rider_id istallet
-- ============================================================================

-- OBS: CREATE OR REPLACE VIEW fungerar inte i alla MySQL-versioner
-- Darfor droppar vi forst om den finns
DROP VIEW IF EXISTS v_canonical_riders;

CREATE VIEW v_canonical_riders AS
SELECT
    r.id AS original_rider_id,
    COALESCE(m.canonical_rider_id, r.id) AS canonical_rider_id,
    r.firstname,
    r.lastname,
    r.uci_id,
    r.license_number,
    r.club_id AS current_club_id,
    r.gender,
    r.birth_year
FROM riders r
LEFT JOIN rider_merge_map m ON r.id = m.merged_rider_id AND m.status = 'approved'
