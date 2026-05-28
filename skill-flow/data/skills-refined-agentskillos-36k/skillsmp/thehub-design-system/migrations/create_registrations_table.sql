-- Create event registrations table
-- This table stores event registrations from participants

CREATE TABLE IF NOT EXISTS event_registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    rider_id INT NULL COMMENT 'NULL if not yet matched to existing rider',

    -- Registration info
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    birth_year INT,
    gender ENUM('M', 'F', 'Other'),

    -- Club and license
    club_name VARCHAR(255),
    license_number VARCHAR(100),
    uci_id VARCHAR(50),

    -- Registration details
    category VARCHAR(100) COMMENT 'Requested race category',
    emergency_contact VARCHAR(255),
    emergency_phone VARCHAR(50),
    medical_info TEXT COMMENT 'Medical conditions, allergies',

    -- Status
    status ENUM('pending', 'confirmed', 'cancelled', 'waitlist') DEFAULT 'pending',
    payment_status ENUM('unpaid', 'paid', 'refunded') DEFAULT 'unpaid',
    bib_number INT NULL COMMENT 'Assigned bib/start number',

    -- Metadata
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    confirmed_date DATETIME NULL,
    notes TEXT COMMENT 'Admin notes',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE SET NULL,

    INDEX idx_event_registrations_event (event_id),
    INDEX idx_event_registrations_rider (rider_id),
    INDEX idx_event_registrations_status (status),
    INDEX idx_event_registrations_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
