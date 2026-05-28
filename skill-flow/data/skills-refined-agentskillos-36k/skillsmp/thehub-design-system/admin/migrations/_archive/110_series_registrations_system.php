<?php
/**
 * Migration 110: Series Registrations System
 *
 * Creates tables for series (season pass) registrations:
 * - series_registrations: The actual purchase of a series pass
 * - series_registration_events: Links series registration to individual events
 *
 * When a rider buys a series pass, they automatically get registered
 * for ALL events in that series.
 *
 * @since 2026-01-11
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration 110: Series Registrations</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #0b131e; color: #f8f2f0; max-width: 900px; margin: 0 auto; }
    .success { color: #10b981; }
    .error { color: #ef4444; }
    .info { color: #38bdf8; }
    .warning { color: #fbbf24; }
    .box { background: #0e1621; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid rgba(55, 212, 214, 0.2); }
    h1 { color: #37d4d6; }
    h3 { color: #f8f2f0; margin-top: 0; }
    code { background: rgba(55, 212, 214, 0.1); padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
    .btn { display: inline-block; padding: 10px 20px; background: #37d4d6; color: #0b131e; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 20px; }
    pre { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; overflow-x: auto; font-size: 0.85em; }
</style>";
echo "</head><body>";
echo "<h1>Migration 110: Series Registrations System</h1>";
echo "<p class='info'>Skapar tabeller för serieanmälan (season pass)</p>";

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
    // PART 1: CREATE SERIES_REGISTRATIONS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>1. Skapa series_registrations tabell</h3>";
    echo "<p>Lagrar köp av serie-pass (season pass)</p>";

    if (!tableExists($db, 'series_registrations')) {
        $db->query("
            CREATE TABLE series_registrations (
                id INT AUTO_INCREMENT PRIMARY KEY,

                -- Core references
                rider_id INT NOT NULL,
                series_id INT NOT NULL,
                class_id INT NOT NULL,

                -- Pricing
                base_price DECIMAL(10,2) NOT NULL COMMENT 'Summa av alla event-priser',
                discount_percent DECIMAL(5,2) NULL COMMENT 'Serie-rabatt i procent',
                discount_amount DECIMAL(10,2) NULL COMMENT 'Rabattbelopp i kronor',
                final_price DECIMAL(10,2) NOT NULL COMMENT 'Slutpris efter rabatt',

                -- Payment (links to orders table)
                order_id INT NULL COMMENT 'FK till orders-tabellen',
                payment_status ENUM('pending', 'paid', 'refunded', 'cancelled') DEFAULT 'pending',
                payment_method ENUM('swish', 'card', 'manual', 'free') NULL,
                payment_reference VARCHAR(255) NULL,
                paid_at TIMESTAMP NULL,

                -- Status
                status ENUM('active', 'cancelled', 'expired') DEFAULT 'active',
                cancelled_at TIMESTAMP NULL,
                cancelled_reason TEXT NULL,

                -- Metadata
                registration_source ENUM('web', 'admin', 'organizer', 'api') DEFAULT 'web',
                registered_by_admin_id INT NULL COMMENT 'Admin som registrerade (om inte web)',
                notes TEXT NULL,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

                -- Foreign keys
                FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
                FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE RESTRICT,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,

                -- Unique constraint: One rider per series
                UNIQUE KEY unique_rider_series (rider_id, series_id),

                -- Indexes
                INDEX idx_series (series_id),
                INDEX idx_rider (rider_id),
                INDEX idx_class (class_id),
                INDEX idx_payment_status (payment_status),
                INDEX idx_status (status),
                INDEX idx_created (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            COMMENT='Serie-registreringar (season pass). En rad per cyklist per serie.'
        ");
        echo "<p class='success'>✓ Skapade tabell <code>series_registrations</code></p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell <code>series_registrations</code> finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 2: CREATE SERIES_REGISTRATION_EVENTS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>2. Skapa series_registration_events tabell</h3>";
    echo "<p>Kopplar serie-registrering till individuella event</p>";

    if (!tableExists($db, 'series_registration_events')) {
        $db->query("
            CREATE TABLE series_registration_events (
                id INT AUTO_INCREMENT PRIMARY KEY,

                -- Core references
                series_registration_id INT NOT NULL,
                event_id INT NOT NULL,

                -- Link to actual event registration (created automatically)
                event_registration_id INT NULL COMMENT 'FK till event_registrations om skapad',

                -- Status for this specific event
                status ENUM('registered', 'confirmed', 'checked_in', 'attended', 'dns', 'dnf', 'cancelled') DEFAULT 'registered',

                -- Check-in tracking
                checked_in TINYINT(1) DEFAULT 0,
                check_in_time TIMESTAMP NULL,
                checked_in_by INT NULL COMMENT 'Admin/marshal som checkade in',

                -- Bib number for this event (can vary per event)
                bib_number VARCHAR(20) NULL,

                -- Notes specific to this event
                notes TEXT NULL,

                -- Timestamps
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

                -- Foreign keys
                FOREIGN KEY (series_registration_id) REFERENCES series_registrations(id) ON DELETE CASCADE,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
                FOREIGN KEY (event_registration_id) REFERENCES event_registrations(id) ON DELETE SET NULL,

                -- Unique constraint: One entry per series registration per event
                UNIQUE KEY unique_series_reg_event (series_registration_id, event_id),

                -- Indexes
                INDEX idx_event (event_id),
                INDEX idx_series_reg (series_registration_id),
                INDEX idx_status (status),
                INDEX idx_event_reg (event_registration_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            COMMENT='Koppling mellan serie-registrering och individuella event.'
        ");
        echo "<p class='success'>✓ Skapade tabell <code>series_registration_events</code></p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell <code>series_registration_events</code> finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 3: ADD MISSING COLUMNS TO SERIES TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>3. Kontrollera series-tabellen</h3>";
    echo "<p>Lägger till saknade kolumner för serieanmälan</p>";

    // Check and add series_price_type column
    if (!columnExists($db, 'series', 'series_price_type')) {
        $db->query("ALTER TABLE series ADD COLUMN series_price_type ENUM('calculated', 'fixed') DEFAULT 'calculated' COMMENT 'Hur seriepris beräknas'");
        echo "<p class='success'>✓ Lade till kolumn <code>series_price_type</code></p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn <code>series_price_type</code> finns redan</p>";
    }

    // Ensure series_discount_percent exists with correct type
    if (!columnExists($db, 'series', 'series_discount_percent')) {
        $db->query("ALTER TABLE series ADD COLUMN series_discount_percent DECIMAL(5,2) DEFAULT 15.00 COMMENT 'Rabatt vid serieanmälan (%)'");
        echo "<p class='success'>✓ Lade till kolumn <code>series_discount_percent</code></p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn <code>series_discount_percent</code> finns redan</p>";
    }

    // Ensure full_series_price exists
    if (!columnExists($db, 'series', 'full_series_price')) {
        $db->query("ALTER TABLE series ADD COLUMN full_series_price DECIMAL(10,2) NULL COMMENT 'Fast pris för hela serien (om series_price_type=fixed)'");
        echo "<p class='success'>✓ Lade till kolumn <code>full_series_price</code></p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn <code>full_series_price</code> finns redan</p>";
    }

    // Ensure allow_series_registration exists
    if (!columnExists($db, 'series', 'allow_series_registration')) {
        $db->query("ALTER TABLE series ADD COLUMN allow_series_registration TINYINT(1) DEFAULT 0 COMMENT '1 = Tillåt serieanmälan'");
        echo "<p class='success'>✓ Lade till kolumn <code>allow_series_registration</code></p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn <code>allow_series_registration</code> finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 4: ADD SERIES_ID TO ORDERS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>4. Lägg till series_id i orders-tabellen</h3>";
    echo "<p>Möjliggör beställningar för serie-registreringar</p>";

    // Add series_id to orders
    if (!columnExists($db, 'orders', 'series_id')) {
        $db->query("ALTER TABLE orders ADD COLUMN series_id INT NULL AFTER event_id");
        $db->query("ALTER TABLE orders ADD FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL");
        $db->query("ALTER TABLE orders ADD INDEX idx_series (series_id)");
        echo "<p class='success'>✓ Lade till kolumn <code>series_id</code> i orders</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn <code>series_id</code> finns redan i orders</p>";
    }

    // Add series_registration_id to order_items
    if (!columnExists($db, 'order_items', 'series_registration_id')) {
        $db->query("ALTER TABLE order_items ADD COLUMN series_registration_id INT NULL AFTER registration_id");
        $db->query("ALTER TABLE order_items ADD FOREIGN KEY (series_registration_id) REFERENCES series_registrations(id) ON DELETE SET NULL");
        $db->query("ALTER TABLE order_items ADD INDEX idx_series_reg (series_registration_id)");
        echo "<p class='success'>✓ Lade till kolumn <code>series_registration_id</code> i order_items</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn <code>series_registration_id</code> finns redan i order_items</p>";
    }

    // Update item_type enum to include series_registration
    try {
        $db->query("ALTER TABLE order_items MODIFY COLUMN item_type ENUM('registration', 'series_registration', 'ticket', 'merchandise', 'other') DEFAULT 'registration'");
        echo "<p class='success'>✓ Uppdaterade <code>item_type</code> enum med 'series_registration'</p>";
    } catch (Exception $e) {
        echo "<p class='info'>ℹ <code>item_type</code> enum är redan uppdaterad eller fel vid uppdatering</p>";
    }

    echo "</div>";

    // =========================================
    // PART 5: CREATE VIEW FOR EASY QUERYING
    // =========================================
    echo "<div class='box'>";
    echo "<h3>5. Skapa vy för serie-registreringar</h3>";

    $db->query("DROP VIEW IF EXISTS v_series_registrations_complete");
    $db->query("
        CREATE VIEW v_series_registrations_complete AS
        SELECT
            sr.id,
            sr.rider_id,
            sr.series_id,
            sr.class_id,
            sr.base_price,
            sr.discount_percent,
            sr.discount_amount,
            sr.final_price,
            sr.payment_status,
            sr.payment_method,
            sr.status,
            sr.created_at,
            sr.paid_at,

            -- Rider info
            CONCAT(r.firstname, ' ', r.lastname) AS rider_name,
            r.email AS rider_email,
            r.license_number,
            r.gender AS rider_gender,

            -- Series info
            s.name AS series_name,
            s.year AS series_year,

            -- Class info
            c.name AS class_name,
            c.display_name AS class_display_name,

            -- Count of events
            (SELECT COUNT(*) FROM series_registration_events sre WHERE sre.series_registration_id = sr.id) AS event_count,
            (SELECT COUNT(*) FROM series_registration_events sre WHERE sre.series_registration_id = sr.id AND sre.status = 'attended') AS events_attended

        FROM series_registrations sr
        JOIN riders r ON sr.rider_id = r.id
        JOIN series s ON sr.series_id = s.id
        JOIN classes c ON sr.class_id = c.id
    ");
    echo "<p class='success'>✓ Skapade vy <code>v_series_registrations_complete</code></p>";

    echo "</div>";

    // =========================================
    // SUMMARY
    // =========================================
    echo "<div class='box'>";
    echo "<h3>Sammanfattning</h3>";

    if ($tablesCreated > 0 || $columnsAdded > 0) {
        echo "<p class='success'>✓ {$tablesCreated} tabeller skapade</p>";
        echo "<p class='success'>✓ {$columnsAdded} kolumner tillagda</p>";
    } else {
        echo "<p class='info'>ℹ Inga ändringar behövdes - allt fanns redan</p>";
    }

    echo "<h4>Tabellstruktur:</h4>";
    echo "<pre>";
    echo "series_registrations (Serie-pass köp)\n";
    echo "├── rider_id → riders\n";
    echo "├── series_id → series\n";
    echo "├── class_id → classes\n";
    echo "├── order_id → orders\n";
    echo "└── pricing info\n\n";
    echo "series_registration_events (Per-event status)\n";
    echo "├── series_registration_id → series_registrations\n";
    echo "├── event_id → events\n";
    echo "├── event_registration_id → event_registrations\n";
    echo "└── check-in status\n";
    echo "</pre>";

    echo "</div>";

    echo "<a href='/admin/dashboard.php' class='btn'>Tillbaka till Admin</a>";
    echo " <a href='/admin/migrations/migration-browser.php' class='btn'>Migreringar</a>";

} catch (Exception $e) {
    echo "<div class='box'>";
    echo "<p class='error'>✗ Fel vid migration: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
    echo "</div>";
}

echo "</body></html>";
