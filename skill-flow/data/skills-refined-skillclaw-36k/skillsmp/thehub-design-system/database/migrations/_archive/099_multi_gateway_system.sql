-- Migration 099: Multi-Gateway Payment System
-- Date: 2026-01-08
-- Description: Adds support for multiple payment gateways (Swish Handel, Stripe Connect, etc)
--
-- NOTE: This migration only creates tables. For column additions to
-- payment_recipients and orders tables, run the PHP migration instead:
-- /admin/migrations/099_multi_gateway_system.php

-- ============================================================================
-- 1. CREATE PAYMENT_TRANSACTIONS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS payment_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    gateway_code VARCHAR(20) NOT NULL,
    transaction_type ENUM('payment', 'refund', 'cancel', 'status_check') DEFAULT 'payment',
    request_data JSON NULL,
    response_data JSON NULL,
    status ENUM('pending', 'success', 'failed', 'cancelled') DEFAULT 'pending',
    error_code VARCHAR(50) NULL,
    error_message TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME NULL,
    INDEX idx_order (order_id),
    INDEX idx_gateway (gateway_code),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. CREATE GATEWAY_CERTIFICATES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS gateway_certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payment_recipient_id INT NOT NULL,
    cert_type ENUM('swish_test', 'swish_production') NOT NULL,
    cert_data MEDIUMBLOB NOT NULL COMMENT 'Certificate file content',
    cert_password VARCHAR(255) NULL COMMENT 'Encrypted certificate password',
    uploaded_by INT NULL COMMENT 'admin_users.id',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at DATE NULL,
    active TINYINT(1) DEFAULT 1,
    INDEX idx_payment_recipient (payment_recipient_id),
    INDEX idx_cert_type (cert_type),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. CREATE WEBHOOK_LOGS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS webhook_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gateway_code VARCHAR(20) NOT NULL,
    webhook_type VARCHAR(50) NULL COMMENT 'e.g. payment.succeeded, payment.failed',
    payload JSON NOT NULL,
    headers JSON NULL,
    signature VARCHAR(500) NULL,
    processed TINYINT(1) DEFAULT 0,
    order_id INT NULL,
    error_message TEXT NULL,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,
    INDEX idx_gateway (gateway_code),
    INDEX idx_processed (processed),
    INDEX idx_order (order_id),
    INDEX idx_received (received_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- NOTE: COLUMN ADDITIONS REQUIRE PHP MIGRATION
-- ============================================================================
-- The following columns need to be added to payment_recipients and orders:
-- Run /admin/migrations/099_multi_gateway_system.php for safe column additions.
--
-- payment_recipients columns:
--   gateway_type, gateway_config, gateway_enabled, stripe_account_id, stripe_account_status
--
-- orders columns:
--   gateway_code, gateway_transaction_id, gateway_metadata, callback_received_at
-- ============================================================================
