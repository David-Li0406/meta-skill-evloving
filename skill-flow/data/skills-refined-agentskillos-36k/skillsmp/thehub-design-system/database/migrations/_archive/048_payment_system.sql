-- Migration 048: Payment System
-- Date: 2025-12-05
-- Description: Adds payment configuration for events, series, and promotors.
--              Enables Swish payments directly to organizers.

-- ============================================================================
-- 1. UPDATE ADMIN_USERS - Add promotor role and payment fields
-- ============================================================================

-- Add promotor to role ENUM
ALTER TABLE admin_users
    MODIFY COLUMN role ENUM('super_admin', 'admin', 'editor', 'promotor') DEFAULT 'editor';

-- Add Swish payment fields to admin_users (for promotors)
ALTER TABLE admin_users
    ADD COLUMN swish_number VARCHAR(20) NULL AFTER full_name,
    ADD COLUMN swish_name VARCHAR(255) NULL AFTER swish_number;

-- ============================================================================
-- 2. PAYMENT_CONFIGS - Flexible payment configuration
-- ============================================================================
-- Can be attached to: event, series, or club
-- Priority: event > series > club > fallback to WooCommerce

CREATE TABLE IF NOT EXISTS payment_configs (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- What is this config for? (only ONE should be set)
    event_id INT NULL,
    series_id INT NULL,
    club_id INT NULL,
    promotor_user_id INT NULL,  -- admin_users.id for promotor

    -- Swish configuration
    swish_enabled TINYINT(1) DEFAULT 1,
    swish_number VARCHAR(20) NOT NULL,
    swish_name VARCHAR(255),  -- Display name for recipient

    -- Card payments via WooCommerce
    card_enabled TINYINT(1) DEFAULT 0,
    woo_vendor_id INT NULL,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign keys
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE,
    FOREIGN KEY (promotor_user_id) REFERENCES admin_users(id) ON DELETE CASCADE,

    -- Only one config per entity
    UNIQUE KEY unique_event (event_id),
    UNIQUE KEY unique_series (series_id),
    UNIQUE KEY unique_club (club_id),
    UNIQUE KEY unique_promotor (promotor_user_id),

    -- Indexes
    INDEX idx_swish_number (swish_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. ORDERS TABLE - Track all purchases
-- ============================================================================

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL,  -- Format: ORD-2025-000001

    -- Customer
    rider_id INT NULL,
    customer_email VARCHAR(255),
    customer_name VARCHAR(255),

    -- Event reference
    event_id INT NULL,

    -- Amounts
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
    discount DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'SEK',

    -- Payment
    payment_method ENUM('swish', 'card', 'manual', 'free') DEFAULT 'swish',
    payment_status ENUM('pending', 'paid', 'failed', 'refunded', 'cancelled') DEFAULT 'pending',
    payment_reference VARCHAR(100),  -- Swish reference or Stripe ID

    -- Swish specific
    swish_number VARCHAR(20),        -- Recipient's Swish number
    swish_message VARCHAR(50),       -- Payment message/reference

    -- Timestamps
    paid_at TIMESTAMP NULL,
    expires_at TIMESTAMP NULL,       -- Auto-cancel if not paid
    cancelled_at TIMESTAMP NULL,
    refunded_at TIMESTAMP NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign keys
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE SET NULL,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL,

    -- Indexes
    UNIQUE KEY unique_order_number (order_number),
    INDEX idx_rider (rider_id),
    INDEX idx_event (event_id),
    INDEX idx_payment_status (payment_status),
    INDEX idx_created (created_at),
    INDEX idx_swish_message (swish_message)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. ORDER_ITEMS TABLE - Individual items in an order
-- ============================================================================

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,

    -- What was purchased
    item_type ENUM('registration', 'ticket', 'merchandise', 'other') DEFAULT 'registration',
    registration_id INT NULL,        -- Link to event_registrations

    -- Description
    description VARCHAR(255) NOT NULL,

    -- Pricing
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INT DEFAULT 1,
    total_price DECIMAL(10,2) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (registration_id) REFERENCES event_registrations(id) ON DELETE SET NULL,

    -- Indexes
    INDEX idx_order (order_id),
    INDEX idx_registration (registration_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 5. ADD ORDER REFERENCE TO REGISTRATIONS
-- ============================================================================

ALTER TABLE event_registrations
    ADD COLUMN order_id INT NULL AFTER payment_status,
    ADD FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,
    ADD INDEX idx_order (order_id);

-- ============================================================================
-- 6. PROMOTOR_EVENTS - Add payment management permission
-- ============================================================================

ALTER TABLE promotor_events
    ADD COLUMN can_manage_payments TINYINT(1) DEFAULT 0 AFTER can_manage_registrations;
