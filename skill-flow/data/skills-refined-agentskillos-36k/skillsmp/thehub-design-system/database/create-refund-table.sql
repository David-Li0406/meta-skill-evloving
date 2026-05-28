-- Create event_refund_requests table if it doesn't exist
CREATE TABLE IF NOT EXISTS event_refund_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    rider_id INT NOT NULL,
    reason TEXT,
    refund_amount DECIMAL(10,2),
    status ENUM('pending', 'approved', 'denied') DEFAULT 'pending',
    admin_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,

    INDEX idx_ticket_id (ticket_id),
    INDEX idx_rider_id (rider_id),
    INDEX idx_status (status),

    FOREIGN KEY (ticket_id) REFERENCES event_tickets(id) ON DELETE CASCADE,
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
