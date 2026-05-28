<?php
/**
 * Migration 101: Pricing Templates System
 *
 * Creates pricing templates and event pricing rules tables
 * for the Economy tab system. Also adds pricing_template_id to events.
 *
 * @since 2026-01-10
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration 101: Pricing Templates</title>";
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
echo "<h1>Migration 101: Pricing Templates System</h1>";

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
    // PART 1: CREATE PRICING_TEMPLATES TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>1. Skapa pricing_templates tabell</h3>";

    if (!tableExists($db, 'pricing_templates')) {
        $db->query("
            CREATE TABLE pricing_templates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT NULL,
                is_default TINYINT(1) DEFAULT 0,
                early_bird_percent DECIMAL(5,2) DEFAULT 15.00,
                early_bird_days_before INT DEFAULT 21,
                late_fee_percent DECIMAL(5,2) DEFAULT 25.00,
                late_fee_days_before INT DEFAULT 3,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                created_by INT NULL,
                INDEX idx_is_default (is_default),
                INDEX idx_name (name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell pricing_templates</p>";
        $tablesCreated++;

        // Insert default template
        $db->query("
            INSERT INTO pricing_templates (name, description, is_default, early_bird_percent, early_bird_days_before)
            VALUES ('Standard Gravity', 'Standardmall för Enduro och DH tävlingar', 1, 15.00, 21)
        ");
        echo "<p class='success'>✓ Lade till standardmall</p>";
    } else {
        echo "<p class='info'>ℹ Tabell pricing_templates finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 2: CREATE PRICING_TEMPLATE_RULES TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>2. Skapa pricing_template_rules tabell</h3>";

    if (!tableExists($db, 'pricing_template_rules')) {
        $db->query("
            CREATE TABLE pricing_template_rules (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell pricing_template_rules</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell pricing_template_rules finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 3: CREATE EVENT_PRICING_RULES TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>3. Skapa event_pricing_rules tabell</h3>";

    if (!tableExists($db, 'event_pricing_rules')) {
        $db->query("
            CREATE TABLE event_pricing_rules (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT NOT NULL,
                class_id INT NOT NULL,
                base_price DECIMAL(10,2) NOT NULL DEFAULT 0,
                early_bird_discount_percent DECIMAL(5,2) DEFAULT 20.00,
                early_bird_end_date DATE NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
                UNIQUE KEY unique_event_class (event_id, class_id),
                INDEX idx_event (event_id),
                INDEX idx_class (class_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell event_pricing_rules</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell event_pricing_rules finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 4: ADD pricing_template_id TO EVENTS
    // =========================================
    echo "<div class='box'>";
    echo "<h3>4. Lägg till pricing_template_id i events</h3>";

    if (!columnExists($db, 'events', 'pricing_template_id')) {
        $db->query("ALTER TABLE events ADD COLUMN pricing_template_id INT NULL AFTER series_id");
        echo "<p class='success'>✓ Lade till kolumn pricing_template_id</p>";
        $columnsAdded++;

        // Add index
        $db->query("ALTER TABLE events ADD INDEX idx_pricing_template (pricing_template_id)");
        echo "<p class='success'>✓ Lade till index för pricing_template_id</p>";
    } else {
        echo "<p class='info'>ℹ Kolumn pricing_template_id finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // PART 5: ADD default_pricing_template_id TO SERIES
    // =========================================
    echo "<div class='box'>";
    echo "<h3>5. Lägg till default_pricing_template_id i series</h3>";

    if (!columnExists($db, 'series', 'default_pricing_template_id')) {
        $db->query("ALTER TABLE series ADD COLUMN default_pricing_template_id INT NULL");
        echo "<p class='success'>✓ Lade till kolumn default_pricing_template_id</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn default_pricing_template_id finns redan</p>";
    }

    echo "</div>";

    // =========================================
    // SUMMARY
    // =========================================
    echo "<div class='box'>";
    echo "<h3>Sammanfattning</h3>";
    echo "<p class='success'>✓ {$tablesCreated} tabeller skapade</p>";
    echo "<p class='success'>✓ {$columnsAdded} kolumner tillagda</p>";
    echo "<p class='info'>Nu kan du använda /admin/event-pricing.php</p>";
    echo "</div>";

    echo "<a href='/admin/pricing-templates.php' class='btn'>Gå till Prismallar</a>";

} catch (Exception $e) {
    echo "<div class='box'>";
    echo "<p class='error'>✗ Fel vid migration: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "</div>";
}

echo "</body></html>";
