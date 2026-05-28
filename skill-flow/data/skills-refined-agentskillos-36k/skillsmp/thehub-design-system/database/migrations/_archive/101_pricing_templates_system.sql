-- Migration 101: Pricing Templates System
-- Date: 2026-01-10
-- Description: Creates pricing templates and event pricing rules tables
--              for the Economy tab system.

-- ============================================================================
-- 1. PRICING_TEMPLATES - Reusable pricing templates
-- ============================================================================

CREATE TABLE IF NOT EXISTS pricing_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    is_default TINYINT(1) DEFAULT 0,

    -- Early bird settings
    early_bird_percent DECIMAL(5,2) DEFAULT 15.00,
    early_bird_days_before INT DEFAULT 21,

    -- Late fee settings
    late_fee_percent DECIMAL(5,2) DEFAULT 25.00,
    late_fee_days_before INT DEFAULT 3,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT NULL,

    INDEX idx_is_default (is_default),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. PRICING_TEMPLATE_RULES - Prices per class in a template
-- ============================================================================

CREATE TABLE IF NOT EXISTS pricing_template_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    template_id INT NOT NULL,
    class_id INT NOT NULL,
    base_price DECIMAL(10,2) NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (template_id) REFERENCES pricing_templates(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,

    UNIQUE KEY unique_template_class (template_id, class_id),
    INDEX idx_template (template_id),
    INDEX idx_class (class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. EVENT_PRICING_RULES - Event-specific pricing overrides
-- ============================================================================

CREATE TABLE IF NOT EXISTS event_pricing_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    class_id INT NOT NULL,
    base_price DECIMAL(10,2) NOT NULL DEFAULT 0,

    -- Early bird override for this specific event/class
    early_bird_discount_percent DECIMAL(5,2) DEFAULT 20.00,
    early_bird_end_date DATE NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,

    UNIQUE KEY unique_event_class (event_id, class_id),
    INDEX idx_event (event_id),
    INDEX idx_class (class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. ADD pricing_template_id TO EVENTS TABLE
-- ============================================================================

-- Note: This uses ALTER TABLE which may fail if column exists.
-- For safe column addition, use the PHP migration instead.

-- ============================================================================
-- 5. INSERT DEFAULT TEMPLATE
-- ============================================================================

INSERT IGNORE INTO pricing_templates (id, name, description, is_default, early_bird_percent, early_bird_days_before)
VALUES (1, 'Standard Gravity', 'Standardmall för Enduro och DH tävlingar', 1, 15.00, 21);
