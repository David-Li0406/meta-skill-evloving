-- ============================================================
-- SCF License Portal Integration
-- Migration 019: SCF License Sync Tables
--
-- Creates tables for:
-- - Caching license data from SCF API
-- - Tracking license history per rider
-- - Sync operation logging
-- - Match candidates for riders without UCI ID
-- ============================================================

-- 1. SCF License Cache
-- Caches responses from SCF License Portal API
CREATE TABLE IF NOT EXISTS scf_license_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uci_id VARCHAR(20) NOT NULL COMMENT 'UCI ID in normalized format (XXX XXX XXX XX)',
    year SMALLINT NOT NULL COMMENT 'License year',
    firstname VARCHAR(100) DEFAULT NULL,
    lastname VARCHAR(100) DEFAULT NULL,
    gender ENUM('M', 'F') DEFAULT NULL,
    birthdate DATE DEFAULT NULL,
    nationality VARCHAR(3) DEFAULT NULL COMMENT 'ISO 3166-1 alpha-3',
    club_name VARCHAR(200) DEFAULT NULL COMMENT 'Club name from SCF',
    license_type VARCHAR(50) DEFAULT NULL COMMENT 'Type of license (Elite, Junior, etc)',
    disciplines JSON DEFAULT NULL COMMENT 'Array of active disciplines',
    raw_data JSON DEFAULT NULL COMMENT 'Full API response for debugging',
    verified_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When data was fetched',
    expires_at DATE DEFAULT NULL COMMENT 'When license expires',
    UNIQUE KEY uk_uci_year (uci_id, year),
    INDEX idx_year (year),
    INDEX idx_nationality (nationality),
    INDEX idx_verified (verified_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. SCF License History
-- Tracks license status changes over time for each rider
CREATE TABLE IF NOT EXISTS scf_license_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL COMMENT 'Reference to riders.id',
    uci_id VARCHAR(20) DEFAULT NULL COMMENT 'UCI ID at time of recording',
    year SMALLINT NOT NULL COMMENT 'License year',
    license_type VARCHAR(50) DEFAULT NULL,
    disciplines JSON DEFAULT NULL,
    club_name VARCHAR(200) DEFAULT NULL,
    nationality VARCHAR(3) DEFAULT NULL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_rider_year (rider_id, year),
    INDEX idx_uci_id (uci_id),
    INDEX idx_year (year),
    CONSTRAINT fk_license_history_rider FOREIGN KEY (rider_id)
        REFERENCES riders(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. SCF Sync Log
-- Tracks all sync operations for monitoring and debugging
CREATE TABLE IF NOT EXISTS scf_sync_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sync_type ENUM('full', 'incremental', 'manual', 'match_search') NOT NULL,
    year SMALLINT NOT NULL,
    started_at DATETIME NOT NULL,
    completed_at DATETIME DEFAULT NULL,
    status ENUM('running', 'completed', 'failed', 'cancelled') DEFAULT 'running',
    total_riders INT DEFAULT 0 COMMENT 'Total riders to process',
    processed INT DEFAULT 0 COMMENT 'Riders processed so far',
    found INT DEFAULT 0 COMMENT 'Riders found in SCF',
    updated INT DEFAULT 0 COMMENT 'Riders updated with new data',
    errors INT DEFAULT 0 COMMENT 'Number of API/processing errors',
    error_message TEXT DEFAULT NULL COMMENT 'Last error message if failed',
    options JSON DEFAULT NULL COMMENT 'Options used for this sync',
    INDEX idx_started (started_at DESC),
    INDEX idx_status (status),
    INDEX idx_year (year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. SCF Match Candidates
-- Stores potential matches for riders without UCI ID
CREATE TABLE IF NOT EXISTS scf_match_candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL COMMENT 'TheHUB rider ID',
    hub_firstname VARCHAR(100) DEFAULT NULL,
    hub_lastname VARCHAR(100) DEFAULT NULL,
    hub_gender VARCHAR(1) DEFAULT NULL,
    hub_birthdate DATE DEFAULT NULL,
    hub_birth_year INT DEFAULT NULL,
    scf_uci_id VARCHAR(20) DEFAULT NULL,
    scf_firstname VARCHAR(100) DEFAULT NULL,
    scf_lastname VARCHAR(100) DEFAULT NULL,
    scf_club VARCHAR(200) DEFAULT NULL,
    scf_nationality VARCHAR(3) DEFAULT NULL,
    match_score DECIMAL(5,2) DEFAULT 0 COMMENT 'Confidence score 0-100',
    match_reason TEXT DEFAULT NULL COMMENT 'Explanation of score factors',
    status ENUM('pending', 'confirmed', 'rejected', 'auto_confirmed') DEFAULT 'pending',
    reviewed_by INT DEFAULT NULL COMMENT 'Admin user who reviewed',
    reviewed_at DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rider (rider_id),
    INDEX idx_status (status),
    INDEX idx_score (match_score DESC),
    INDEX idx_created (created_at DESC),
    CONSTRAINT fk_match_rider FOREIGN KEY (rider_id)
        REFERENCES riders(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Add SCF-specific columns to riders table
-- These store the current verified license status
ALTER TABLE riders
    ADD COLUMN IF NOT EXISTS scf_license_verified_at DATETIME DEFAULT NULL
        COMMENT 'When license was last verified against SCF',
    ADD COLUMN IF NOT EXISTS scf_license_year SMALLINT DEFAULT NULL
        COMMENT 'Year of verified license',
    ADD COLUMN IF NOT EXISTS scf_license_type VARCHAR(50) DEFAULT NULL
        COMMENT 'License type from SCF',
    ADD COLUMN IF NOT EXISTS scf_disciplines JSON DEFAULT NULL
        COMMENT 'Active disciplines from SCF',
    ADD COLUMN IF NOT EXISTS scf_club_name VARCHAR(200) DEFAULT NULL
        COMMENT 'Club name from SCF (may differ from TheHUB)';

-- Add index for finding unverified riders
CREATE INDEX IF NOT EXISTS idx_riders_scf_verified
    ON riders(scf_license_verified_at);

-- Add index for license year filtering
CREATE INDEX IF NOT EXISTS idx_riders_scf_year
    ON riders(scf_license_year);
