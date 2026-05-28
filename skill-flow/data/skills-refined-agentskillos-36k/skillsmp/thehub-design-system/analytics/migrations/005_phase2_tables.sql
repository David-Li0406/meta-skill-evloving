-- ============================================================================
-- ANALYTICS PHASE 2 TABLES
-- TheHUB Analytics Platform
-- Version: 2.0
-- Kor EFTER 001_analytics_tables.sql
-- ============================================================================

-- Kohort-tabell for snabb lookup av rider cohort year
-- Optional: kan beraknas on-the-fly men denna tabell gor det snabbare
CREATE TABLE IF NOT EXISTS rider_cohorts (
    rider_id INT PRIMARY KEY COMMENT 'Canonical rider_id',
    cohort_year SMALLINT NOT NULL COMMENT 'Forsta sasong (MIN season_year)',
    first_series_id INT NULL COMMENT 'Forsta serie rider deltog i',
    first_discipline VARCHAR(50) NULL COMMENT 'Forsta disciplin',
    first_event_id INT NULL COMMENT 'Forsta event',
    total_seasons INT DEFAULT 1 COMMENT 'Antal sasonger aktiv',
    last_active_year SMALLINT NULL COMMENT 'Senaste aktiva ar',
    status ENUM('active', 'soft_churn', 'medium_churn', 'hard_churn') DEFAULT 'active',
    calculation_version VARCHAR(20) DEFAULT 'v2',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cohort_year (cohort_year),
    INDEX idx_status (status),
    INDEX idx_last_active (last_active_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Risk-scores for At-Risk/Churn-prediktion
-- Cache:ad data som fylls av cron-jobb
CREATE TABLE IF NOT EXISTS rider_risk_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL COMMENT 'Canonical rider_id',
    season_year SMALLINT NOT NULL COMMENT 'Ar beraknat for',
    risk_score TINYINT NOT NULL DEFAULT 0 COMMENT 'Total risk score (0-100)',
    risk_level ENUM('low', 'medium', 'high', 'critical') GENERATED ALWAYS AS (
        CASE
            WHEN risk_score >= 70 THEN 'critical'
            WHEN risk_score >= 50 THEN 'high'
            WHEN risk_score >= 30 THEN 'medium'
            ELSE 'low'
        END
    ) STORED COMMENT 'Riskniva baserad pa score',
    factors JSON NULL COMMENT 'Detaljerade riskfaktorer',
    declining_events TINYINT(1) DEFAULT 0 COMMENT 'Flagga: minskande events',
    no_recent_activity TINYINT(1) DEFAULT 0 COMMENT 'Flagga: ingen aktivitet',
    class_downgrade TINYINT(1) DEFAULT 0 COMMENT 'Flagga: klassnedflytt',
    single_series TINYINT(1) DEFAULT 0 COMMENT 'Flagga: bara en serie',
    low_tenure TINYINT(1) DEFAULT 0 COMMENT 'Flagga: kort karriar',
    high_age_in_class TINYINT(1) DEFAULT 0 COMMENT 'Flagga: hog alder i klass',
    calculation_version VARCHAR(20) DEFAULT 'v2',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_rider_year (rider_id, season_year),
    INDEX idx_risk_score (season_year, risk_score DESC),
    INDEX idx_risk_level (season_year, risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Regioner for geografisk analys
-- Statisk data for befolkning per region
CREATE TABLE IF NOT EXISTS regions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT 'Regionnamn',
    code VARCHAR(10) NOT NULL COMMENT 'Lanskod (AB, C, etc)',
    population INT DEFAULT 0 COMMENT 'Befolkning',
    area_km2 INT DEFAULT 0 COMMENT 'Yta i km2',
    updated_year SMALLINT DEFAULT 2025 COMMENT 'Ar for befolkningsdata',
    UNIQUE KEY unique_code (code),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Regional rider statistics
CREATE TABLE IF NOT EXISTS region_yearly_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region_code VARCHAR(10) NOT NULL COMMENT 'Lanskod',
    season_year SMALLINT NOT NULL,
    rider_count INT DEFAULT 0 COMMENT 'Antal aktiva riders',
    new_riders INT DEFAULT 0 COMMENT 'Nya riders detta ar',
    event_count INT DEFAULT 0 COMMENT 'Antal events i regionen',
    club_count INT DEFAULT 0 COMMENT 'Antal aktiva klubbar',
    riders_per_capita DECIMAL(10,6) NULL COMMENT 'Riders per 100k befolkning',
    growth_rate DECIMAL(5,2) NULL COMMENT 'Tillvaxt vs foregaende ar',
    calculation_version VARCHAR(20) DEFAULT 'v2',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_region_year (region_code, season_year),
    INDEX idx_year (season_year),
    INDEX idx_rider_count (season_year, rider_count DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Feeder trends (historisk data for trendanalys)
CREATE TABLE IF NOT EXISTS feeder_trends (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_series_id INT NOT NULL,
    to_series_id INT NOT NULL,
    season_year SMALLINT NOT NULL,
    flow_type ENUM('same_year', 'next_year') DEFAULT 'same_year',
    flow_count INT DEFAULT 0 COMMENT 'Antal riders i flodet',
    percentage DECIMAL(5,2) NULL COMMENT 'Procent av from_series',
    year_over_year_change DECIMAL(5,2) NULL COMMENT 'Forandring vs foregaende ar',
    calculation_version VARCHAR(20) DEFAULT 'v2',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_flow_year (from_series_id, to_series_id, season_year, flow_type),
    INDEX idx_year (season_year),
    INDEX idx_from (from_series_id, season_year),
    INDEX idx_to (to_series_id, season_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Analytics export log (for GDPR/audit)
CREATE TABLE IF NOT EXISTS analytics_exports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    export_type VARCHAR(50) NOT NULL COMMENT 'Typ av export',
    export_params JSON NULL COMMENT 'Parametrar for exporten',
    exported_by INT NULL COMMENT 'User ID som exporterade',
    exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    row_count INT DEFAULT 0 COMMENT 'Antal rader exporterade',
    ip_address VARCHAR(45) NULL,
    INDEX idx_type (export_type),
    INDEX idx_date (exported_at),
    INDEX idx_user (exported_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Seed regions data
INSERT IGNORE INTO regions (name, code, population, updated_year) VALUES
('Stockholm', 'AB', 2415139, 2025),
('Uppsala', 'C', 395026, 2025),
('Sodermanland', 'D', 301542, 2025),
('Ostergotland', 'E', 468339, 2025),
('Jonkoping', 'F', 366479, 2025),
('Kronoberg', 'G', 203527, 2025),
('Kalmar', 'H', 246641, 2025),
('Gotland', 'I', 60124, 2025),
('Blekinge', 'K', 159606, 2025),
('Skane', 'M', 1402425, 2025),
('Halland', 'N', 340243, 2025),
('Vastra Gotaland', 'O', 1751166, 2025),
('Varmland', 'S', 282414, 2025),
('Orebro', 'T', 305792, 2025),
('Vastmanland', 'U', 277052, 2025),
('Dalarna', 'W', 286547, 2025),
('Gavleborg', 'X', 286547, 2025),
('Vasternorrland', 'Y', 245572, 2025),
('Jamtland', 'Z', 131830, 2025),
('Vasterbotten', 'AC', 274153, 2025),
('Norrbotten', 'BD', 250497, 2025);

-- Add indexes to existing tables for better performance
-- rider_yearly_stats
ALTER TABLE rider_yearly_stats
    ADD INDEX IF NOT EXISTS idx_rider_year (rider_id, season_year),
    ADD INDEX IF NOT EXISTS idx_year_events (season_year, total_events DESC);

-- series_crossover
ALTER TABLE series_crossover
    ADD INDEX IF NOT EXISTS idx_year_type (from_year, crossover_type);
