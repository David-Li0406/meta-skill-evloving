-- ============================================================================
-- ANALYTICS CORE TABLES
-- TheHUB Analytics Platform
-- Version: 1.0
-- Kor EFTER 000_governance_core.sql
-- ============================================================================

-- Arsstatistik per cyklist (pre-beraknad)
-- Lagrar aggregerad statistik per rider och ar for snabba lookups
CREATE TABLE IF NOT EXISTS rider_yearly_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL COMMENT 'Canonical rider_id',
    season_year INT NOT NULL,
    total_events INT DEFAULT 0 COMMENT 'Antal events deltagit i',
    total_series INT DEFAULT 0 COMMENT 'Antal unika serier',
    total_points DECIMAL(10,2) DEFAULT 0 COMMENT 'Totala poang',
    best_position INT NULL COMMENT 'Basta placering',
    avg_position DECIMAL(5,2) NULL COMMENT 'Genomsnittsplacering',
    primary_discipline VARCHAR(50) NULL COMMENT 'Huvuddisciplin (mest deltaganden)',
    primary_series_id INT NULL COMMENT 'Huvudserie (mest deltaganden)',
    is_rookie TINYINT(1) DEFAULT 0 COMMENT '1 = forsta aret',
    is_retained TINYINT(1) DEFAULT 0 COMMENT '1 = aterkom fran forra aret',
    calculation_version VARCHAR(20) DEFAULT 'v1',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_rider_year (rider_id, season_year),
    INDEX idx_season (season_year),
    INDEX idx_discipline (primary_discipline),
    INDEX idx_rookie (is_rookie, season_year),
    INDEX idx_retained (is_retained, season_year),
    INDEX idx_version (calculation_version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Serie-deltagande per cyklist och ar
-- Detaljerad data om varje riders deltagande i specifika serier
CREATE TABLE IF NOT EXISTS series_participation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL COMMENT 'Canonical rider_id',
    series_id INT NOT NULL,
    season_year INT NOT NULL,
    events_attended INT DEFAULT 0 COMMENT 'Antal events i serien',
    first_event_date DATE NULL COMMENT 'Forsta event',
    last_event_date DATE NULL COMMENT 'Sista event',
    total_points DECIMAL(10,2) DEFAULT 0,
    final_rank INT NULL COMMENT 'Slutplacering i serien',
    is_entry_series TINYINT(1) DEFAULT 0 COMMENT '1 = forsta serien nagonsin',
    calculation_version VARCHAR(20) DEFAULT 'v1',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_rider_series_year (rider_id, series_id, season_year),
    INDEX idx_series_year (series_id, season_year),
    INDEX idx_rider (rider_id),
    INDEX idx_entry (is_entry_series, season_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Floden mellan serier (cross-participation)
-- Sparar nar en rider deltar i flera serier eller byter serie
CREATE TABLE IF NOT EXISTS series_crossover (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL COMMENT 'Canonical rider_id',
    from_series_id INT NOT NULL COMMENT 'Ursprungsserie',
    to_series_id INT NOT NULL COMMENT 'Malserie',
    from_year INT NOT NULL,
    to_year INT NOT NULL,
    crossover_type ENUM('same_year', 'next_year', 'multi_year') DEFAULT 'same_year',
    calculation_version VARCHAR(20) DEFAULT 'v1',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_from_series (from_series_id, from_year),
    INDEX idx_to_series (to_series_id, to_year),
    INDEX idx_rider (rider_id),
    INDEX idx_crossover_type (crossover_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Klubbstatistik per ar
-- Aggregerad statistik per klubb for benchmarking
CREATE TABLE IF NOT EXISTS club_yearly_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT NOT NULL,
    season_year INT NOT NULL,
    active_riders INT DEFAULT 0 COMMENT 'Antal aktiva medlemmar',
    new_riders INT DEFAULT 0 COMMENT 'Nya medlemmar detta ar',
    retained_riders INT DEFAULT 0 COMMENT 'Aterkommande fran forra aret',
    churned_riders INT DEFAULT 0 COMMENT 'Forlorade till andra klubbar/inaktivitet',
    total_events_participation INT DEFAULT 0 COMMENT 'Totalt antal eventdeltaganden',
    total_points DECIMAL(10,2) DEFAULT 0,
    top_10_finishes INT DEFAULT 0,
    podiums INT DEFAULT 0,
    wins INT DEFAULT 0,
    primary_discipline VARCHAR(50) NULL COMMENT 'Vanligaste disciplin',
    calculation_version VARCHAR(20) DEFAULT 'v1',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_club_year (club_id, season_year),
    INDEX idx_season (season_year),
    INDEX idx_active (active_riders DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- Venue/Anlaggningsstatistik per ar
-- Statistik per anlaggning/venue
CREATE TABLE IF NOT EXISTS venue_yearly_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venue_id INT NOT NULL,
    season_year INT NOT NULL,
    total_events INT DEFAULT 0 COMMENT 'Antal events pa anlaggningen',
    total_participants INT DEFAULT 0 COMMENT 'Totalt antal deltagare',
    unique_riders INT DEFAULT 0 COMMENT 'Unika deltagare',
    avg_participants_per_event DECIMAL(6,2) NULL,
    disciplines JSON NULL COMMENT 'T.ex. {"enduro": 3, "downhill": 2}',
    series_hosted JSON NULL COMMENT 'Serie-IDs som haft event har',
    calculation_version VARCHAR(20) DEFAULT 'v1',
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_venue_year (venue_id, season_year),
    INDEX idx_season (season_year),
    INDEX idx_events (total_events DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

-- KPI-snapshots for historik
-- Sparar ögonblicksbilder av nyckeltal for trendanalys
CREATE TABLE IF NOT EXISTS analytics_snapshots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    snapshot_date DATE NOT NULL COMMENT 'Datum for snapshot',
    snapshot_type ENUM('daily', 'weekly', 'monthly', 'quarterly', 'yearly') NOT NULL,
    metrics JSON NOT NULL COMMENT 'Alla KPIer som JSON',
    calculation_version VARCHAR(20) DEFAULT 'v1',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_date_type (snapshot_date, snapshot_type),
    INDEX idx_type (snapshot_type, snapshot_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;
