<?php
/**
 * Migration 100: Global Sponsors & Race Reports System
 *
 * Creates tables for:
 * - sponsor_placements: Global sponsor ad placements
 * - sponsor_tier_benefits: Tier benefit definitions
 * - sponsor_analytics: Detailed tracking
 * - sponsor_settings: System configuration
 * - race_reports: Blog posts from riders
 * - race_report_tags: Tag categories
 * - race_report_tag_relations: Report-tag associations
 * - race_report_comments: Comments with threading
 * - race_report_likes: Like tracking
 *
 * Also extends the sponsors table with new tiers and global flag.
 *
 * @since 2026-01-10
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration 100: Global Sponsors & Race Reports</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #0b131e; color: #f8f2f0; max-width: 900px; margin: 0 auto; }
    .success { color: #10b981; }
    .error { color: #ef4444; }
    .info { color: #38bdf8; }
    .warning { color: #fbbf24; }
    .box { background: #0e1621; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid rgba(55, 212, 214, 0.2); }
    h1 { color: #37d4d6; }
    h3 { color: #f8f2f0; margin-top: 0; }
    pre { background: #0d1520; color: #c7cfdd; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 12px; }
    .btn { display: inline-block; padding: 10px 20px; background: #37d4d6; color: #0b131e; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 20px; }
    .btn:hover { background: #4ae0e2; }
</style>";
echo "</head><body>";
echo "<h1>Migration 100: Global Sponsors & Race Reports System</h1>";

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
    // PART 1: EXTEND SPONSORS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>1. Utöka sponsors-tabellen</h3>";

    // Check if we need to modify the tier enum
    $tierInfo = $db->getAll("SHOW COLUMNS FROM sponsors LIKE 'tier'");
    if (!empty($tierInfo)) {
        $currentType = $tierInfo[0]['Type'] ?? '';
        if (strpos($currentType, 'title_gravityseries') === false) {
            try {
                $db->query("ALTER TABLE sponsors MODIFY tier ENUM('title', 'title_gravityseries', 'title_series', 'gold', 'silver', 'bronze', 'branch') DEFAULT 'silver'");
                echo "<p class='success'>✓ Uppdaterade tier ENUM med nya värden</p>";
            } catch (Exception $e) {
                echo "<p class='warning'>⚠ Kunde inte uppdatera tier ENUM: " . htmlspecialchars($e->getMessage()) . "</p>";
            }
        } else {
            echo "<p class='info'>ℹ Tier ENUM har redan nya värden</p>";
        }
    }

    // Add is_global column
    if (!columnExists($db, 'sponsors', 'is_global')) {
        $db->query("ALTER TABLE sponsors ADD COLUMN is_global TINYINT(1) DEFAULT 0 AFTER active");
        echo "<p class='success'>✓ Lade till kolumn is_global</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn is_global finns redan</p>";
    }

    // Add display_priority column
    if (!columnExists($db, 'sponsors', 'display_priority')) {
        $db->query("ALTER TABLE sponsors ADD COLUMN display_priority INT DEFAULT 50 AFTER is_global");
        echo "<p class='success'>✓ Lade till kolumn display_priority</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn display_priority finns redan</p>";
    }

    // Add banner_image column (skip if exists)
    if (!columnExists($db, 'sponsors', 'banner_image')) {
        $db->query("ALTER TABLE sponsors ADD COLUMN banner_image VARCHAR(255) AFTER logo_dark");
        echo "<p class='success'>✓ Lade till kolumn banner_image</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn banner_image finns redan</p>";
    }

    // Add contact_email column
    if (!columnExists($db, 'sponsors', 'contact_email')) {
        $db->query("ALTER TABLE sponsors ADD COLUMN contact_email VARCHAR(255) AFTER website");
        echo "<p class='success'>✓ Lade till kolumn contact_email</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn contact_email finns redan</p>";
    }

    // Add contact_phone column
    if (!columnExists($db, 'sponsors', 'contact_phone')) {
        $db->query("ALTER TABLE sponsors ADD COLUMN contact_phone VARCHAR(50) AFTER contact_email");
        echo "<p class='success'>✓ Lade till kolumn contact_phone</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn contact_phone finns redan</p>";
    }

    // Add indexes
    if (!indexExists($db, 'sponsors', 'idx_global')) {
        $db->query("ALTER TABLE sponsors ADD INDEX idx_global (is_global)");
        echo "<p class='success'>✓ Lade till index idx_global</p>";
    }

    if (!indexExists($db, 'sponsors', 'idx_priority')) {
        $db->query("ALTER TABLE sponsors ADD INDEX idx_priority (display_priority)");
        echo "<p class='success'>✓ Lade till index idx_priority</p>";
    }

    echo "</div>";

    // =========================================
    // PART 2: SPONSOR PLACEMENTS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>2. sponsor_placements</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'sponsor_placements'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE sponsor_placements (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sponsor_id INT NOT NULL,
                page_type ENUM('home', 'results', 'series_list', 'series_single', 'database', 'ranking', 'calendar', 'blog', 'blog_single', 'all') NOT NULL,
                position ENUM('header_banner', 'sidebar_top', 'sidebar_mid', 'content_top', 'content_mid', 'content_bottom', 'footer') NOT NULL,
                display_order INT DEFAULT 0,
                is_active TINYINT(1) DEFAULT 1,
                start_date DATE NULL,
                end_date DATE NULL,
                impressions_target INT NULL,
                impressions_current INT DEFAULT 0,
                clicks INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (sponsor_id) REFERENCES sponsors(id) ON DELETE CASCADE,
                INDEX idx_placement_page (page_type, position),
                INDEX idx_placement_active (is_active, start_date, end_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell sponsor_placements</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell sponsor_placements finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // PART 3: SPONSOR TIER BENEFITS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>3. sponsor_tier_benefits</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'sponsor_tier_benefits'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE sponsor_tier_benefits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tier ENUM('title_gravityseries', 'title_series', 'gold', 'silver', 'branch') NOT NULL,
                benefit_key VARCHAR(100) NOT NULL,
                benefit_value TEXT NOT NULL,
                display_order INT DEFAULT 0,
                UNIQUE KEY unique_tier_benefit (tier, benefit_key)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell sponsor_tier_benefits</p>";
        $tablesCreated++;

        // Insert default benefits
        $db->query("
            INSERT INTO sponsor_tier_benefits (tier, benefit_key, benefit_value, display_order) VALUES
            ('title_gravityseries', 'branding', 'Varumärke i GravitySeries logotyp', 1),
            ('title_gravityseries', 'placement', 'Exklusiv startsidesplacering (header banner)', 2),
            ('title_gravityseries', 'all_pages', 'Header-placering på alla sidor', 3),
            ('title_gravityseries', 'max_placements', 'Max 10 sponsorplatser', 4),
            ('title_gravityseries', 'analytics', 'Dedikerad analytics-dashboard', 5),
            ('title_series', 'branding', 'Varumärke i serienamnet', 1),
            ('title_series', 'placement', 'Banner på seriesidor', 2),
            ('title_series', 'events', 'Branding på seriens evenemang', 3),
            ('title_series', 'max_placements', 'Max 5 sponsorplatser', 4),
            ('gold', 'sidebar', 'Sidebar startsida', 1),
            ('gold', 'results', 'Alla resultsidor', 2),
            ('gold', 'ranking', 'Ranking sidebar', 3),
            ('gold', 'max_placements', 'Max 3 sponsorplatser', 4),
            ('silver', 'selected', 'Valda sidor', 1),
            ('silver', 'content', 'Content bottom', 2),
            ('silver', 'max_placements', 'Max 2 sponsorplatser', 3),
            ('branch', 'database', 'Databas sidebar (relevant för cykelbutiker)', 1),
            ('branch', 'footer', 'Footer rotation', 2),
            ('branch', 'max_placements', 'Max 2 sponsorplatser', 3)
        ");
        echo "<p class='success'>✓ Infogade standard tier-förmåner</p>";
    } else {
        echo "<p class='info'>ℹ Tabell sponsor_tier_benefits finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // PART 4: SPONSOR ANALYTICS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>4. sponsor_analytics</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'sponsor_analytics'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE sponsor_analytics (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                sponsor_id INT NOT NULL,
                placement_id INT NULL,
                page_type VARCHAR(50) NOT NULL,
                page_id INT NULL,
                action_type ENUM('impression', 'click', 'conversion') NOT NULL,
                user_id INT NULL,
                ip_hash VARCHAR(64) NOT NULL,
                user_agent VARCHAR(500),
                referer VARCHAR(255),
                session_id VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_analytics_sponsor (sponsor_id, created_at),
                INDEX idx_analytics_placement (placement_id, created_at),
                INDEX idx_analytics_date (created_at),
                INDEX idx_analytics_action (action_type, created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell sponsor_analytics</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell sponsor_analytics finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // PART 5: SPONSOR SETTINGS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>5. sponsor_settings</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'sponsor_settings'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE sponsor_settings (
                setting_key VARCHAR(100) PRIMARY KEY,
                setting_value TEXT NOT NULL,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell sponsor_settings</p>";
        $tablesCreated++;

        // Insert default settings
        $db->query("
            INSERT INTO sponsor_settings (setting_key, setting_value, description) VALUES
            ('max_sponsors_per_page', '5', 'Max antal sponsorer per sida'),
            ('banner_rotation_seconds', '10', 'Rotation banner (sekunder)'),
            ('enable_analytics', '1', 'Aktivera sponsorstatistik'),
            ('require_approval_race_reports', '0', 'Kräv godkännande för race reports'),
            ('featured_reports_count', '3', 'Antal featured reports på startsida'),
            ('instagram_auto_import', '0', 'Auto-importera från Instagram'),
            ('public_enabled', '0', 'Visa globala sponsorer för besökare (0=endast admin, 1=alla)'),
            ('race_reports_public', '0', 'Visa race reports för besökare (0=endast admin, 1=alla)')
        ");
        echo "<p class='success'>✓ Infogade standard-inställningar</p>";
    } else {
        echo "<p class='info'>ℹ Tabell sponsor_settings finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // PART 6: RACE REPORTS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>6. race_reports</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'race_reports'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE race_reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rider_id INT NOT NULL,
                event_id INT NULL,
                title VARCHAR(255) NOT NULL,
                slug VARCHAR(255) NOT NULL UNIQUE,
                content LONGTEXT NOT NULL,
                excerpt TEXT,
                featured_image VARCHAR(255),
                status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
                instagram_url VARCHAR(255),
                instagram_embed_code TEXT,
                is_from_instagram TINYINT(1) DEFAULT 0,
                is_featured TINYINT(1) DEFAULT 0,
                views INT DEFAULT 0,
                likes INT DEFAULT 0,
                reading_time_minutes INT DEFAULT 1,
                allow_comments TINYINT(1) DEFAULT 1,
                published_at DATETIME NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
                INDEX idx_reports_status (status, published_at),
                INDEX idx_reports_rider (rider_id),
                INDEX idx_reports_event (event_id),
                INDEX idx_reports_featured (is_featured, published_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell race_reports</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell race_reports finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // PART 7: RACE REPORT TAGS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>7. race_report_tags</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'race_report_tags'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE race_report_tags (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                slug VARCHAR(100) NOT NULL UNIQUE,
                usage_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell race_report_tags</p>";
        $tablesCreated++;

        // Insert some default tags
        $db->query("
            INSERT INTO race_report_tags (name, slug) VALUES
            ('Enduro', 'enduro'),
            ('Downhill', 'downhill'),
            ('XC', 'xc'),
            ('Gravel', 'gravel'),
            ('Träning', 'traning'),
            ('Tävling', 'tavling'),
            ('Teknik', 'teknik'),
            ('Utrustning', 'utrustning')
        ");
        echo "<p class='success'>✓ Infogade standard-taggar</p>";
    } else {
        echo "<p class='info'>ℹ Tabell race_report_tags finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // PART 8: RACE REPORT TAG RELATIONS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>8. race_report_tag_relations</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'race_report_tag_relations'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE race_report_tag_relations (
                report_id INT NOT NULL,
                tag_id INT NOT NULL,
                PRIMARY KEY (report_id, tag_id),
                FOREIGN KEY (report_id) REFERENCES race_reports(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES race_report_tags(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell race_report_tag_relations</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell race_report_tag_relations finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // PART 9: RACE REPORT COMMENTS TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>9. race_report_comments</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'race_report_comments'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE race_report_comments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                report_id INT NOT NULL,
                rider_id INT NULL,
                parent_comment_id INT NULL,
                comment_text TEXT NOT NULL,
                is_approved TINYINT(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES race_reports(id) ON DELETE CASCADE,
                FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE SET NULL,
                FOREIGN KEY (parent_comment_id) REFERENCES race_report_comments(id) ON DELETE CASCADE,
                INDEX idx_comments_report (report_id, is_approved)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell race_report_comments</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell race_report_comments finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // PART 10: RACE REPORT LIKES TABLE
    // =========================================
    echo "<div class='box'>";
    echo "<h3>10. race_report_likes</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'race_report_likes'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE race_report_likes (
                report_id INT NOT NULL,
                rider_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (report_id, rider_id),
                FOREIGN KEY (report_id) REFERENCES race_reports(id) ON DELETE CASCADE,
                FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell race_report_likes</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell race_report_likes finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // SUMMARY
    // =========================================
    echo "<div class='box'>";
    echo "<h3>Sammanfattning</h3>";
    echo "<p class='success'>✓ {$tablesCreated} tabeller skapade</p>";
    echo "<p class='success'>✓ {$columnsAdded} kolumner tillagda i sponsors-tabellen</p>";

    if (!empty($errors)) {
        echo "<h4 class='error'>Fel:</h4>";
        foreach ($errors as $error) {
            echo "<p class='error'>✗ " . htmlspecialchars($error) . "</p>";
        }
    }

    echo "<p style='margin-top: 20px;'>Migrationens nya funktioner:</p>";
    echo "<ul>
        <li><strong>Globala sponsorplaceringar</strong> - Visa sponsorer på fasta sidor</li>
        <li><strong>Nya sponsornivåer</strong> - Title GS, Title Serie, Guld, Silver, Bransch</li>
        <li><strong>Sponsoranalytik</strong> - Visningar, klick, CTR</li>
        <li><strong>Race Reports</strong> - Riders kan blogga om sina tävlingar</li>
        <li><strong>Taggar & kommentarer</strong> - Interaktivitet i bloggen</li>
    </ul>";

    echo "<a href='/admin/sponsor-placements.php' class='btn'>Gå till Reklamplatser</a>";
    echo "</div>";

} catch (Exception $e) {
    echo "<div class='box'>";
    echo "<p class='error'>✗ Fel vid migration: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
    echo "</div>";
}

echo "</body></html>";
