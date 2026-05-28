-- Migration 079: Create rider_claims table (if not exists)
-- Stores requests from users wanting to link their email to historical rider profiles

CREATE TABLE IF NOT EXISTS rider_claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    claimant_rider_id INT NULL,                 -- The rider making the claim (can be null for admin-created)
    target_rider_id INT NOT NULL,               -- The profile they want to claim
    claimant_email VARCHAR(255) NOT NULL,
    claimant_name VARCHAR(255),
    phone VARCHAR(50) DEFAULT NULL,
    instagram VARCHAR(100) DEFAULT NULL,
    facebook VARCHAR(255) DEFAULT NULL,
    reason TEXT,                                -- Optional: why they believe this is their profile
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    admin_notes TEXT,
    reviewed_by INT,
    reviewed_at DATETIME,
    created_by ENUM('user', 'admin') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_status (status),
    INDEX idx_created (created_at),
    INDEX idx_target_pending (target_rider_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
