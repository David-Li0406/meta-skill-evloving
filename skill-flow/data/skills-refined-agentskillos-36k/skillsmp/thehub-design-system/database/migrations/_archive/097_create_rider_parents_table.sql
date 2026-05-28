-- Create rider_parents table for parent-child relationships
-- Allows parents to manage their children's registrations

CREATE TABLE IF NOT EXISTS rider_parents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parent_rider_id INT NOT NULL,
    child_rider_id INT NOT NULL,
    relationship VARCHAR(50) DEFAULT 'parent',
    verified TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_parent_child (parent_rider_id, child_rider_id),
    KEY idx_parent (parent_rider_id),
    KEY idx_child (child_rider_id),
    CONSTRAINT fk_parent_rider FOREIGN KEY (parent_rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    CONSTRAINT fk_child_rider FOREIGN KEY (child_rider_id) REFERENCES riders(id) ON DELETE CASCADE
);
