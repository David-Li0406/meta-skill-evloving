-- Rider Claims / Merge Requests Table
-- Stores requests from users wanting to merge their new profile with historical data
-- claimant_rider_id = the logged-in user's rider profile (new, has email)
-- target_rider_id = the historical profile they want to claim (old, may lack email)

CREATE TABLE IF NOT EXISTS rider_claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    claimant_rider_id INT NOT NULL,       -- The rider making the claim (logged in user)
    target_rider_id INT NOT NULL,          -- The profile they want to merge with
    claimant_email VARCHAR(255) NOT NULL,
    claimant_name VARCHAR(255),
    reason TEXT,                           -- Optional: why they believe this is their profile
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    admin_notes TEXT,
    reviewed_by INT,
    reviewed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (claimant_rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    FOREIGN KEY (target_rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES admin_users(id) ON DELETE SET NULL,

    UNIQUE KEY unique_pending_claim (claimant_rider_id, target_rider_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
