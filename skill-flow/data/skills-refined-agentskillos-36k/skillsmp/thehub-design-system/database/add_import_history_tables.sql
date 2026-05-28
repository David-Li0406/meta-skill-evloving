-- ============================================================================
-- Add Import History Tables for Rollback Functionality
-- Run this to add rollback support to existing database
-- ============================================================================

CREATE TABLE IF NOT EXISTS import_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_type ENUM('riders', 'results', 'events', 'clubs', 'uci', 'other') NOT NULL,
    filename VARCHAR(255),
    file_size INT,
    status ENUM('pending', 'processing', 'completed', 'failed', 'rolled_back') DEFAULT 'pending',
    total_records INT DEFAULT 0,
    success_count INT DEFAULT 0,
    updated_count INT DEFAULT 0,
    failed_count INT DEFAULT 0,
    skipped_count INT DEFAULT 0,
    error_summary TEXT,
    notes TEXT,
    imported_by VARCHAR(100),
    rolled_back_at TIMESTAMP NULL DEFAULT NULL,
    rolled_back_by VARCHAR(100) NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (import_type),
    INDEX idx_status (status),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS import_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_id INT NOT NULL,
    record_type ENUM('rider', 'result', 'event', 'club', 'venue', 'other') NOT NULL,
    record_id INT NOT NULL,
    action ENUM('created', 'updated', 'deleted') NOT NULL,
    old_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (import_id) REFERENCES import_history(id) ON DELETE CASCADE,
    INDEX idx_import (import_id),
    INDEX idx_record (record_type, record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
