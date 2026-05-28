<?php
/**
 * Migration 103: Gravity ID & Discount Codes System
 *
 * Adds:
 * 1. Gravity ID columns to riders table
 * 2. Discount codes system for registrations
 * 3. Series membership/registration support
 * 4. Gravity ID settings for event-level discounts
 *
 * @since 2026-01-10
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration 103: Gravity ID & Discount Codes</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #0b131e; color: #f8f2f0; max-width: 900px; margin: 0 auto; }
    .success { color: #10b981; }
    .error { color: #ef4444; }
    .info { color: #38bdf8; }
    .warning { color: #fbbf24; }
    .box { background: #0e1621; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid rgba(55, 212, 214, 0.2); }
    h1 { color: #37d4d6; }
    h3 { color: #f8f2f0; margin-top: 0; }
    .btn { display: inline-block; padding: 10px 20px; background: #37d4d6; color: #0b131e; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 20px; }
    code { background: #1a2332; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
</style>";
echo "</head><body>";
echo "<h1>Migration 103: Gravity ID & Discount Codes System</h1>";

$tablesCreated = 0;
$columnsAdded = 0;
$errors = [];

/**
 * Helper: Check if table exists
 */
function tableExists($db, $table) {
    $result = $db->getAll("SHOW TABLES LIKE '{$table}'");
    return !empty($result);
}

/**
 * Helper: Check if column exists
 */
function columnExists($db, $table, $column) {
    $result = $db->getAll("SHOW COLUMNS FROM `{$table}` LIKE '{$column}'");
    return !empty($result);
}

try {
    // =========================================
    // PART 1: ADD GRAVITY ID TO RIDERS
    // =========================================
    echo "<div class='box'>";
    echo "<h3>1. Lägg till Gravity ID-kolumner i riders</h3>";

    if (!columnExists($db, 'riders', 'gravity_id')) {
        $db->query("ALTER TABLE riders ADD COLUMN gravity_id VARCHAR(20) NULL AFTER uci_id");
        echo "<p class='success'>✓ Lade till <code>gravity_id</code> kolumn</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn <code>gravity_id</code> finns redan</p>";
    }

    if (!columnExists($db, 'riders', 'gravity_id_since')) {
        $db->query("ALTER TABLE riders ADD COLUMN gravity_id_since DATE NULL AFTER gravity_id");
        echo "<p class='success'>✓ Lade till <code>gravity_id_since</code> kolumn</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn <code>gravity_id_since</code> finns redan</p>";
    }

    if (!columnExists($db, 'riders', 'gravity_id_valid_until')) {
        $db->query("ALTER TABLE riders ADD COLUMN gravity_id_valid_until DATE NULL AFTER gravity_id_since");
        echo "<p class='success'>✓ Lade till <code>gravity_id_valid_until</code> kolumn</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn <code>gravity_id_valid_until</code> finns redan</p>";
    }

    // Add index for gravity_id lookups
    try {
        $db->query("CREATE INDEX idx_riders_gravity_id ON riders(gravity_id)");
        echo "<p class='success'>✓ Skapade index för gravity_id</p>";
    } catch (Exception $e) {
        echo "<p class='info'>→ Index finns redan eller kunde inte skapas</p>";
    }

    echo "</div>";

    // =========================================
    // PART 2: CREATE DISCOUNT_CODES TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>2. Skapa rabattkodstabell</h3>";

    if (!tableExists($db, 'discount_codes')) {
        $db->query("
            CREATE TABLE discount_codes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(50) NOT NULL UNIQUE,
                description VARCHAR(255) NULL,

                -- Discount type and value
                discount_type ENUM('percentage', 'fixed') NOT NULL DEFAULT 'fixed',
                discount_value DECIMAL(10,2) NOT NULL,

                -- Usage limits
                max_uses INT NULL COMMENT 'NULL = unlimited',
                current_uses INT NOT NULL DEFAULT 0,
                max_uses_per_user INT NULL DEFAULT 1,

                -- Validity period
                valid_from DATETIME NULL,
                valid_until DATETIME NULL,

                -- Restrictions
                min_order_amount DECIMAL(10,2) NULL,
                applicable_to ENUM('all', 'event', 'series') NOT NULL DEFAULT 'all',
                event_id INT NULL,
                series_id INT NULL,

                -- Sponsor/partner link
                sponsor_id INT NULL,

                -- Status
                is_active TINYINT(1) NOT NULL DEFAULT 1,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                created_by INT NULL,

                INDEX idx_code (code),
                INDEX idx_active (is_active, valid_from, valid_until),
                INDEX idx_event (event_id),
                INDEX idx_series (series_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ");
        echo "<p class='success'>✓ Skapade <code>discount_codes</code> tabell</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>→ Tabell <code>discount_codes</code> finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 3: CREATE DISCOUNT_CODE_USAGE TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>3. Skapa rabattkodsanvändning-tabell</h3>";

    if (!tableExists($db, 'discount_code_usage')) {
        $db->query("
            CREATE TABLE discount_code_usage (
                id INT AUTO_INCREMENT PRIMARY KEY,
                discount_code_id INT NOT NULL,
                order_id INT NOT NULL,
                rider_id INT NULL,
                discount_amount DECIMAL(10,2) NOT NULL,
                used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (discount_code_id) REFERENCES discount_codes(id) ON DELETE CASCADE,
                INDEX idx_code (discount_code_id),
                INDEX idx_order (order_id),
                INDEX idx_rider (rider_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ");
        echo "<p class='success'>✓ Skapade <code>discount_code_usage</code> tabell</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>→ Tabell <code>discount_code_usage</code> finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 4: ADD GRAVITY ID SETTINGS TO EVENTS
    // =========================================
    echo "<div class='box'>";
    echo "<h3>4. Lägg till Gravity ID-inställningar för events</h3>";

    if (!columnExists($db, 'events', 'gravity_id_discount')) {
        $db->query("ALTER TABLE events ADD COLUMN gravity_id_discount DECIMAL(10,2) NULL DEFAULT 50.00 COMMENT 'Rabatt för Gravity ID-medlemmar i SEK'");
        echo "<p class='success'>✓ Lade till <code>gravity_id_discount</code> kolumn (default 50 kr)</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn <code>gravity_id_discount</code> finns redan</p>";
    }

    if (!columnExists($db, 'events', 'gravity_id_required')) {
        $db->query("ALTER TABLE events ADD COLUMN gravity_id_required TINYINT(1) NOT NULL DEFAULT 0 COMMENT '1 = Gravity ID krävs för anmälan'");
        echo "<p class='success'>✓ Lade till <code>gravity_id_required</code> kolumn</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn <code>gravity_id_required</code> finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 5: ADD GRAVITY ID SETTINGS TO SERIES
    // =========================================
    echo "<div class='box'>";
    echo "<h3>5. Lägg till Gravity ID-inställningar för serier</h3>";

    if (!columnExists($db, 'series', 'gravity_id_discount')) {
        $db->query("ALTER TABLE series ADD COLUMN gravity_id_discount DECIMAL(10,2) NULL DEFAULT 50.00");
        echo "<p class='success'>✓ Lade till <code>gravity_id_discount</code> till series</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn finns redan</p>";
    }

    if (!columnExists($db, 'series', 'gravity_id_enabled')) {
        $db->query("ALTER TABLE series ADD COLUMN gravity_id_enabled TINYINT(1) NOT NULL DEFAULT 1 COMMENT '1 = Gravity ID-rabatt aktiv för serien'");
        echo "<p class='success'>✓ Lade till <code>gravity_id_enabled</code> till series</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 6: CREATE SERIES_MEMBERSHIPS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>6. Skapa seriemedlemskap-tabell</h3>";

    if (!tableExists($db, 'series_memberships')) {
        $db->query("
            CREATE TABLE series_memberships (
                id INT AUTO_INCREMENT PRIMARY KEY,
                series_id INT NOT NULL,
                rider_id INT NOT NULL,

                -- Membership type
                membership_type ENUM('full', 'partial', 'single') NOT NULL DEFAULT 'full',

                -- Pricing
                paid_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
                discount_applied DECIMAL(10,2) NOT NULL DEFAULT 0,

                -- Status
                status ENUM('pending', 'active', 'cancelled', 'expired') NOT NULL DEFAULT 'pending',

                -- Payment link
                order_id INT NULL,

                -- Events included (NULL = all events in series)
                included_events JSON NULL COMMENT 'Array of event IDs if partial membership',

                -- Validity
                valid_from DATE NULL,
                valid_until DATE NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

                UNIQUE KEY unique_series_rider (series_id, rider_id),
                INDEX idx_rider (rider_id),
                INDEX idx_status (status),
                INDEX idx_series (series_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ");
        echo "<p class='success'>✓ Skapade <code>series_memberships</code> tabell</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>→ Tabell <code>series_memberships</code> finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 7: ADD SERIES PRICING COLUMNS
    // =========================================
    echo "<div class='box'>";
    echo "<h3>7. Lägg till seriepriskolumner</h3>";

    if (!columnExists($db, 'series', 'full_series_price')) {
        $db->query("ALTER TABLE series ADD COLUMN full_series_price DECIMAL(10,2) NULL COMMENT 'Pris för hela serien'");
        echo "<p class='success'>✓ Lade till <code>full_series_price</code></p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn finns redan</p>";
    }

    if (!columnExists($db, 'series', 'series_discount_percent')) {
        $db->query("ALTER TABLE series ADD COLUMN series_discount_percent INT NULL DEFAULT 15 COMMENT 'Rabatt vid serieanmälan (%)'");
        echo "<p class='success'>✓ Lade till <code>series_discount_percent</code></p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn finns redan</p>";
    }

    if (!columnExists($db, 'series', 'allow_series_registration')) {
        $db->query("ALTER TABLE series ADD COLUMN allow_series_registration TINYINT(1) NOT NULL DEFAULT 0 COMMENT '1 = Tillåt serieanmälan'");
        echo "<p class='success'>✓ Lade till <code>allow_series_registration</code></p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 8: ADD DISCOUNT CODE TO ORDERS
    // =========================================
    echo "<div class='box'>";
    echo "<h3>8. Lägg till rabattkod-referens till orders</h3>";

    if (!columnExists($db, 'orders', 'discount_code_id')) {
        $db->query("ALTER TABLE orders ADD COLUMN discount_code_id INT NULL AFTER discount");
        echo "<p class='success'>✓ Lade till <code>discount_code_id</code> till orders</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn finns redan</p>";
    }

    if (!columnExists($db, 'orders', 'gravity_id_discount')) {
        $db->query("ALTER TABLE orders ADD COLUMN gravity_id_discount DECIMAL(10,2) NULL DEFAULT 0 AFTER discount_code_id");
        echo "<p class='success'>✓ Lade till <code>gravity_id_discount</code> till orders</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>→ Kolumn finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 9: CREATE GRAVITY ID SETTINGS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>9. Skapa Gravity ID-inställningstabell</h3>";

    if (!tableExists($db, 'gravity_id_settings')) {
        $db->query("
            CREATE TABLE gravity_id_settings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(50) NOT NULL UNIQUE,
                setting_value TEXT NULL,
                description VARCHAR(255) NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ");

        // Insert default settings
        $db->query("
            INSERT INTO gravity_id_settings (setting_key, setting_value, description) VALUES
            ('default_discount', '50', 'Standard Gravity ID-rabatt i SEK'),
            ('valid_for_years', '1', 'Antal år ett Gravity ID är giltigt'),
            ('enabled', '1', 'Aktivera Gravity ID-systemet'),
            ('import_source', 'csv', 'Importkälla (csv/api)'),
            ('last_import', NULL, 'Datum för senaste import')
        ");

        echo "<p class='success'>✓ Skapade <code>gravity_id_settings</code> tabell med standardvärden</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>→ Tabell <code>gravity_id_settings</code> finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // SUMMARY
    // =========================================
    echo "<div class='box' style='border-color: #10b981;'>";
    echo "<h3>Sammanfattning</h3>";
    echo "<p><strong>Tabeller skapade:</strong> {$tablesCreated}</p>";
    echo "<p><strong>Kolumner tillagda:</strong> {$columnsAdded}</p>";

    if (!empty($errors)) {
        echo "<h4 class='error'>Fel:</h4>";
        foreach ($errors as $err) {
            echo "<p class='error'>• {$err}</p>";
        }
    } else {
        echo "<p class='success'>✓ Migrering slutförd utan fel!</p>";
    }
    echo "</div>";

    echo "<a href='/admin/' class='btn'>← Tillbaka till Admin</a>";

} catch (Exception $e) {
    echo "<div class='box' style='border-color: #ef4444;'>";
    echo "<h3 class='error'>Kritiskt fel</h3>";
    echo "<p class='error'>" . htmlspecialchars($e->getMessage()) . "</p>";
    echo "</div>";
}

echo "</body></html>";
