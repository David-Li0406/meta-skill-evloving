<?php
/**
 * Migration 099: Multi-Gateway Payment System
 *
 * Adds support for multiple payment gateways (Swish Handel, Stripe Connect, etc)
 * This PHP migration safely adds columns that may already exist.
 *
 * @since 2026-01-08
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration 099: Multi-Gateway System</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #0b131e; color: #f8f2f0; max-width: 900px; margin: 0 auto; }
    .success { color: #10b981; }
    .error { color: #ef4444; }
    .info { color: #38bdf8; }
    .box { background: #0e1621; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid rgba(55, 212, 214, 0.2); }
    h1 { color: #37d4d6; }
    h3 { color: #f8f2f0; margin-top: 0; }
    .btn { display: inline-block; padding: 10px 20px; background: #37d4d6; color: #0b131e; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 20px; }
</style>";
echo "</head><body>";
echo "<h1>Migration 099: Multi-Gateway Payment System</h1>";

$tablesCreated = 0;
$columnsAdded = 0;
$errors = [];

/**
 * Helper: Check if column exists
 */
function columnExists($db, $table, $column) {
    $result = $db->getAll("SHOW COLUMNS FROM `{$table}` LIKE '{$column}'");
    return !empty($result);
}

/**
 * Helper: Check if index exists
 */
function indexExists($db, $table, $index) {
    $result = $db->getAll("SHOW INDEX FROM `{$table}` WHERE Key_name = '{$index}'");
    return !empty($result);
}

try {
    // =========================================
    // PART 1: PAYMENT_RECIPIENTS COLUMNS
    // =========================================
    echo "<div class='box'>";
    echo "<h3>1. Lägg till kolumner i payment_recipients</h3>";

    // gateway_type
    if (!columnExists($db, 'payment_recipients', 'gateway_type')) {
        $db->query("ALTER TABLE payment_recipients ADD COLUMN gateway_type ENUM('manual', 'swish_handel', 'stripe') DEFAULT 'manual' AFTER active");
        echo "<p class='success'>✓ Lade till kolumn gateway_type</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn gateway_type finns redan</p>";
    }

    // gateway_config
    if (!columnExists($db, 'payment_recipients', 'gateway_config')) {
        $db->query("ALTER TABLE payment_recipients ADD COLUMN gateway_config JSON NULL AFTER gateway_type");
        echo "<p class='success'>✓ Lade till kolumn gateway_config</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn gateway_config finns redan</p>";
    }

    // gateway_enabled
    if (!columnExists($db, 'payment_recipients', 'gateway_enabled')) {
        $db->query("ALTER TABLE payment_recipients ADD COLUMN gateway_enabled TINYINT(1) DEFAULT 0 AFTER gateway_config");
        echo "<p class='success'>✓ Lade till kolumn gateway_enabled</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn gateway_enabled finns redan</p>";
    }

    // stripe_account_id
    if (!columnExists($db, 'payment_recipients', 'stripe_account_id')) {
        $db->query("ALTER TABLE payment_recipients ADD COLUMN stripe_account_id VARCHAR(100) NULL AFTER gateway_enabled");
        echo "<p class='success'>✓ Lade till kolumn stripe_account_id</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn stripe_account_id finns redan</p>";
    }

    // stripe_account_status
    if (!columnExists($db, 'payment_recipients', 'stripe_account_status')) {
        $db->query("ALTER TABLE payment_recipients ADD COLUMN stripe_account_status ENUM('pending', 'active', 'disabled') NULL AFTER stripe_account_id");
        echo "<p class='success'>✓ Lade till kolumn stripe_account_status</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn stripe_account_status finns redan</p>";
    }

    // Indexes
    if (!indexExists($db, 'payment_recipients', 'idx_gateway_type')) {
        $db->query("ALTER TABLE payment_recipients ADD INDEX idx_gateway_type (gateway_type)");
        echo "<p class='success'>✓ Lade till index idx_gateway_type</p>";
    }
    if (!indexExists($db, 'payment_recipients', 'idx_gateway_enabled')) {
        $db->query("ALTER TABLE payment_recipients ADD INDEX idx_gateway_enabled (gateway_enabled)");
        echo "<p class='success'>✓ Lade till index idx_gateway_enabled</p>";
    }
    if (!indexExists($db, 'payment_recipients', 'idx_stripe_account')) {
        $db->query("ALTER TABLE payment_recipients ADD INDEX idx_stripe_account (stripe_account_id)");
        echo "<p class='success'>✓ Lade till index idx_stripe_account</p>";
    }

    echo "</div>";

    // =========================================
    // PART 2: ORDERS COLUMNS
    // =========================================
    echo "<div class='box'>";
    echo "<h3>2. Lägg till kolumner i orders</h3>";

    // gateway_code
    if (!columnExists($db, 'orders', 'gateway_code')) {
        $db->query("ALTER TABLE orders ADD COLUMN gateway_code VARCHAR(20) NULL AFTER payment_method");
        echo "<p class='success'>✓ Lade till kolumn gateway_code</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn gateway_code finns redan</p>";
    }

    // gateway_transaction_id
    if (!columnExists($db, 'orders', 'gateway_transaction_id')) {
        $db->query("ALTER TABLE orders ADD COLUMN gateway_transaction_id VARCHAR(100) NULL AFTER payment_reference");
        echo "<p class='success'>✓ Lade till kolumn gateway_transaction_id</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn gateway_transaction_id finns redan</p>";
    }

    // gateway_metadata
    if (!columnExists($db, 'orders', 'gateway_metadata')) {
        $db->query("ALTER TABLE orders ADD COLUMN gateway_metadata JSON NULL AFTER gateway_transaction_id");
        echo "<p class='success'>✓ Lade till kolumn gateway_metadata</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn gateway_metadata finns redan</p>";
    }

    // callback_received_at
    if (!columnExists($db, 'orders', 'callback_received_at')) {
        $db->query("ALTER TABLE orders ADD COLUMN callback_received_at DATETIME NULL AFTER gateway_metadata");
        echo "<p class='success'>✓ Lade till kolumn callback_received_at</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn callback_received_at finns redan</p>";
    }

    // Indexes
    if (!indexExists($db, 'orders', 'idx_gateway_code')) {
        $db->query("ALTER TABLE orders ADD INDEX idx_gateway_code (gateway_code)");
        echo "<p class='success'>✓ Lade till index idx_gateway_code</p>";
    }
    if (!indexExists($db, 'orders', 'idx_gateway_transaction')) {
        $db->query("ALTER TABLE orders ADD INDEX idx_gateway_transaction (gateway_transaction_id)");
        echo "<p class='success'>✓ Lade till index idx_gateway_transaction</p>";
    }

    echo "</div>";

    // =========================================
    // PART 3: CREATE TABLES
    // =========================================
    echo "<div class='box'>";
    echo "<h3>3. Skapa tabeller</h3>";

    // payment_transactions
    $exists = $db->getAll("SHOW TABLES LIKE 'payment_transactions'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE payment_transactions (
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
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                INDEX idx_order (order_id),
                INDEX idx_gateway (gateway_code),
                INDEX idx_status (status),
                INDEX idx_created (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell payment_transactions</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell payment_transactions finns redan</p>";
    }

    // gateway_certificates
    $exists = $db->getAll("SHOW TABLES LIKE 'gateway_certificates'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE gateway_certificates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                payment_recipient_id INT NOT NULL,
                cert_type ENUM('swish_test', 'swish_production') NOT NULL,
                cert_data MEDIUMBLOB NOT NULL,
                cert_password VARCHAR(255) NULL,
                uploaded_by INT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at DATE NULL,
                active TINYINT(1) DEFAULT 1,
                FOREIGN KEY (payment_recipient_id) REFERENCES payment_recipients(id) ON DELETE CASCADE,
                FOREIGN KEY (uploaded_by) REFERENCES admin_users(id) ON DELETE SET NULL,
                INDEX idx_payment_recipient (payment_recipient_id),
                INDEX idx_cert_type (cert_type),
                INDEX idx_active (active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell gateway_certificates</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell gateway_certificates finns redan</p>";
    }

    // webhook_logs
    $exists = $db->getAll("SHOW TABLES LIKE 'webhook_logs'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE webhook_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                gateway_code VARCHAR(20) NOT NULL,
                webhook_type VARCHAR(50) NULL,
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell webhook_logs</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell webhook_logs finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // SUMMARY
    // =========================================
    echo "<div class='box'>";
    echo "<h3>Sammanfattning</h3>";
    echo "<p class='success'>✓ {$tablesCreated} tabeller skapade</p>";
    echo "<p class='success'>✓ {$columnsAdded} kolumner tillagda</p>";
    echo "</div>";

} catch (Exception $e) {
    echo "<div class='box'>";
    echo "<p class='error'>✗ Fel vid migration: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "</div>";
}

echo "</body></html>";
