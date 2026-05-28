<?php
/**
 * Event Payment Setup
 * Consolidated page for payment/ticketing configuration
 * Uses Economy Tab System
 */

require_once __DIR__ . '/../config.php';
require_admin();

// Check if payment.php exists before including
$paymentFunctionsAvailable = false;
if (file_exists(__DIR__ . '/../includes/payment.php')) {
    require_once __DIR__ . '/../includes/payment.php';
    $paymentFunctionsAvailable = true;
}

$db = getDB();

// Ensure required tables and columns exist
$setupErrors = [];
try {
    // Check/create payment_configs table
    $tables = $db->getAll("SHOW TABLES LIKE 'payment_configs'");
    if (empty($tables)) {
        $db->query("
            CREATE TABLE IF NOT EXISTS payment_configs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT NULL,
                series_id INT NULL,
                promotor_user_id INT NULL,
                swish_enabled TINYINT(1) DEFAULT 0,
                swish_number VARCHAR(50) NULL,
                swish_name VARCHAR(255) NULL,
                card_enabled TINYINT(1) DEFAULT 0,
                woo_vendor_id VARCHAR(50) NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_event (event_id),
                INDEX idx_series (series_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ");
    }

    // Check/create event_pricing_rules table
    $tables = $db->getAll("SHOW TABLES LIKE 'event_pricing_rules'");
    if (empty($tables)) {
        $db->query("
            CREATE TABLE IF NOT EXISTS event_pricing_rules (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT NOT NULL,
                class_id INT NOT NULL,
                base_price DECIMAL(10,2) NOT NULL DEFAULT 0,
                early_bird_discount_percent DECIMAL(5,2) DEFAULT 20,
                early_bird_end_date DATE NULL,
                late_registration_fee DECIMAL(10,2) DEFAULT 0,
                late_registration_start DATE NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_event_class (event_id, class_id),
                INDEX idx_event (event_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ");
    }

    // Check/create orders table
    $tables = $db->getAll("SHOW TABLES LIKE 'orders'");
    if (empty($tables)) {
        $db->query("
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT NOT NULL,
                user_id INT NULL,
                total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
                payment_status ENUM('pending','paid','cancelled','refunded') DEFAULT 'pending',
                payment_method VARCHAR(50) NULL,
                payment_reference VARCHAR(255) NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_event (event_id),
                INDEX idx_status (payment_status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ");
    }

    // Check/add required columns to events table
    $eventColumns = $db->getAll("SHOW COLUMNS FROM events");
    $existingCols = array_column($eventColumns, 'Field');

    if (!in_array('ticketing_enabled', $existingCols)) {
        $db->query("ALTER TABLE events ADD COLUMN ticketing_enabled TINYINT(1) DEFAULT 0");
    }
    if (!in_array('ticket_deadline_days', $existingCols)) {
        $db->query("ALTER TABLE events ADD COLUMN ticket_deadline_days INT DEFAULT 7");
    }
    if (!in_array('payment_recipient', $existingCols)) {
        $db->query("ALTER TABLE events ADD COLUMN payment_recipient VARCHAR(50) DEFAULT 'series'");
    }

} catch (Exception $e) {
    $setupErrors[] = "Databasfel vid setup: " . $e->getMessage();
    error_log("EVENT PAYMENT SETUP ERROR: " . $e->getMessage());
}

// Get event ID (supports both 'id' and 'event_id')
$eventId = isset($_GET['id']) ? intval($_GET['id']) : (isset($_GET['event_id']) ? intval($_GET['event_id']) : 0);

if ($eventId <= 0) {
    $_SESSION['flash_message'] = 'Ogiltigt event-ID';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/events.php');
    exit;
}

// Fetch event with series info
$event = $db->getRow("
    SELECT e.*, s.name as series_name, s.id as series_id
    FROM events e
    LEFT JOIN series s ON e.series_id = s.id
    WHERE e.id = ?
", [$eventId]);

if (!$event) {
    $_SESSION['flash_message'] = 'Event hittades inte';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/events.php');
    exit;
}

// Get current payment config (may be inherited)
$paymentConfig = null;
$configSource = 'woocommerce';
$sourceName = 'WooCommerce';
if ($paymentFunctionsAvailable && function_exists('getPaymentConfig')) {
    try {
        $paymentConfig = getPaymentConfig($eventId);
        $configSource = $paymentConfig['config_source'] ?? 'woocommerce';
        $sourceName = $paymentConfig['source_name'] ?? 'WooCommerce';
    } catch (Exception $e) {
        $setupErrors[] = "Kunde inte hämta betalningskonfiguration: " . $e->getMessage();
    }
}

// Get event-specific config (if exists)
$eventPaymentConfig = null;
try {
    $eventPaymentConfig = $db->getRow("SELECT * FROM payment_configs WHERE event_id = ?", [$eventId]);
} catch (Exception $e) {
    // Table might not exist
}

// Get series config (if event belongs to series)
$seriesPaymentConfig = null;
if ($event['series_id']) {
    $seriesPaymentConfig = $db->getRow("SELECT * FROM payment_configs WHERE series_id = ?", [$event['series_id']]);
}

// Initialize message
$message = '';
$messageType = 'info';

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'save_settings') {
        // Save ticketing settings
        $enabled = isset($_POST['ticketing_enabled']) ? 1 : 0;
        $deadlineDays = intval($_POST['ticket_deadline_days'] ?? 7);

        $db->update('events', [
            'ticketing_enabled' => $enabled,
            'ticket_deadline_days' => $deadlineDays
        ], 'id = ?', [$eventId]);

        $message = 'Grundinställningar sparade!';
        $messageType = 'success';

        // Refresh event data
        $event = $db->getRow("SELECT e.*, s.name as series_name FROM events e LEFT JOIN series s ON e.series_id = s.id WHERE e.id = ?", [$eventId]);

    } elseif ($action === 'save_payment_recipient') {
        // Save payment recipient choice (series, organizer, or custom)
        $recipient = $_POST['payment_recipient'] ?? 'series';
        $organizerClubId = !empty($_POST['organizer_club_id']) ? intval($_POST['organizer_club_id']) : null;

        // Validate recipient value
        if (!in_array($recipient, ['series', 'organizer', 'custom'])) {
            $recipient = 'series';
        }

        $db->update('events', [
            'payment_recipient' => $recipient,
            'organizer_club_id' => $organizerClubId
        ], 'id = ?', [$eventId]);

        // If custom, also save the custom Swish settings
        if ($recipient === 'custom') {
            $swishNumber = trim($_POST['custom_swish_number'] ?? '');
            $swishName = trim($_POST['custom_swish_name'] ?? '');

            if ($swishNumber) {
                if ($eventPaymentConfig) {
                    $db->update('payment_configs', [
                        'swish_enabled' => 1,
                        'swish_number' => $swishNumber,
                        'swish_name' => $swishName
                    ], 'id = ?', [$eventPaymentConfig['id']]);
                } else {
                    $db->insert('payment_configs', [
                        'event_id' => $eventId,
                        'swish_enabled' => 1,
                        'swish_number' => $swishNumber,
                        'swish_name' => $swishName
                    ]);
                }
            }
        }

        $message = 'Betalningsval sparat!';
        $messageType = 'success';

        // Refresh data
        $event = $db->getRow("SELECT e.*, s.name as series_name, s.id as series_id FROM events e LEFT JOIN series s ON e.series_id = s.id WHERE e.id = ?", [$eventId]);
        $eventPaymentConfig = $db->getRow("SELECT * FROM payment_configs WHERE event_id = ?", [$eventId]);
        $paymentConfig = getPaymentConfig($eventId);

    } elseif ($action === 'save_payment_config') {
        // Save event-specific payment configuration
        $useEventConfig = isset($_POST['use_event_config']) ? 1 : 0;

        if ($useEventConfig) {
            $swishEnabled = isset($_POST['swish_enabled']) ? 1 : 0;
            $swishNumber = trim($_POST['swish_number'] ?? '');
            $swishName = trim($_POST['swish_name'] ?? '');
            $cardEnabled = isset($_POST['card_enabled']) ? 1 : 0;
            $wooProductId = trim($_POST['woo_product_id'] ?? '') ?: null;

            if ($eventPaymentConfig) {
                // Update existing
                $db->update('payment_configs', [
                    'swish_enabled' => $swishEnabled,
                    'swish_number' => $swishNumber ?: null,
                    'swish_name' => $swishName ?: null,
                    'card_enabled' => $cardEnabled,
                    'woo_vendor_id' => $wooProductId
                ], 'id = ?', [$eventPaymentConfig['id']]);
            } else {
                // Create new
                $db->insert('payment_configs', [
                    'event_id' => $eventId,
                    'swish_enabled' => $swishEnabled,
                    'swish_number' => $swishNumber ?: null,
                    'swish_name' => $swishName ?: null,
                    'card_enabled' => $cardEnabled,
                    'woo_vendor_id' => $wooProductId
                ]);
            }

            // Also update woo_product_id on event
            $db->update('events', ['woo_product_id' => $wooProductId], 'id = ?', [$eventId]);

            $message = 'Betalningsinställningar sparade!';
            $messageType = 'success';
        } else {
            // Remove event-specific config (inherit from series/promotor)
            if ($eventPaymentConfig) {
                $db->execute("DELETE FROM payment_configs WHERE id = ?", [$eventPaymentConfig['id']]);
            }
            $message = 'Eventet ärver nu betalningsinställningar.';
            $messageType = 'success';
        }

        // Refresh configs
        $eventPaymentConfig = $db->getRow("SELECT * FROM payment_configs WHERE event_id = ?", [$eventId]);
        $paymentConfig = getPaymentConfig($eventId);
        $configSource = $paymentConfig['config_source'] ?? 'woocommerce';

    } elseif ($action === 'save_pricing') {
        // Save pricing rules
        $classIds = $_POST['class_id'] ?? [];
        $basePrices = $_POST['base_price'] ?? [];
        $earlyBirdDiscounts = $_POST['early_bird_discount'] ?? [];
        $earlyBirdEndDates = $_POST['early_bird_end_date'] ?? [];

        $saved = 0;
        foreach ($classIds as $index => $classId) {
            $basePrice = floatval($basePrices[$index] ?? 0);
            $earlyBirdDiscount = floatval($earlyBirdDiscounts[$index] ?? 0);
            $earlyBirdEndDate = trim($earlyBirdEndDates[$index] ?? '');

            if ($basePrice > 0) {
                $existing = $db->getRow("SELECT id FROM event_pricing_rules WHERE event_id = ? AND class_id = ?", [$eventId, $classId]);

                if ($existing) {
                    $db->execute("UPDATE event_pricing_rules SET base_price = ?, early_bird_discount_percent = ?, early_bird_end_date = ?, updated_at = NOW() WHERE id = ?",
                        [$basePrice, $earlyBirdDiscount, $earlyBirdEndDate ?: null, $existing['id']]);
                } else {
                    $db->execute("INSERT INTO event_pricing_rules (event_id, class_id, base_price, early_bird_discount_percent, early_bird_end_date, created_at) VALUES (?, ?, ?, ?, ?, NOW())",
                        [$eventId, $classId, $basePrice, $earlyBirdDiscount, $earlyBirdEndDate ?: null]);
                }
                $saved++;
            } else {
                // Delete if price is 0
                $db->execute("DELETE FROM event_pricing_rules WHERE event_id = ? AND class_id = ?", [$eventId, $classId]);
            }
        }

        $message = "Sparade {$saved} priser!";
        $messageType = 'success';
    }
}

// Get classes with pricing
$classes = $db->getAll("
    SELECT c.id, c.name, c.display_name, c.sort_order,
           epr.base_price, epr.early_bird_discount_percent, epr.early_bird_end_date
    FROM classes c
    LEFT JOIN event_pricing_rules epr ON c.id = epr.class_id AND epr.event_id = ?
    ORDER BY c.sort_order ASC
", [$eventId]);

// Get order statistics
$orderStats = ['total_orders' => 0, 'pending_orders' => 0, 'paid_orders' => 0, 'cancelled_orders' => 0, 'total_revenue' => 0];
try {
    $result = $db->getRow("
        SELECT
            COUNT(*) as total_orders,
            SUM(CASE WHEN payment_status = 'pending' THEN 1 ELSE 0 END) as pending_orders,
            SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) as paid_orders,
            SUM(CASE WHEN payment_status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_orders,
            SUM(CASE WHEN payment_status = 'paid' THEN total_amount ELSE 0 END) as total_revenue
        FROM orders
        WHERE event_id = ?
    ", [$eventId]);
    if ($result) {
        $orderStats = $result;
    }
} catch (Exception $e) {
    // Orders table might not exist
}

// Calculate default early-bird end date (event date - 14 days)
$eventDate = new DateTime($event['date']);
$defaultEarlyBirdEnd = clone $eventDate;
$defaultEarlyBirdEnd->modify('-14 days');

// Get clubs with payment enabled (for organizer dropdown)
$clubsWithPayment = $db->getAll("
    SELECT id, name, swish_number, swish_name
    FROM clubs
    WHERE active = 1 AND (swish_number IS NOT NULL AND swish_number != '')
    ORDER BY name
");

// Get all active clubs (in case organizer club doesn't have payment yet)
$allClubs = $db->getAll("SELECT id, name FROM clubs WHERE active = 1 ORDER BY name");

// Get series payment info
$seriesPaymentInfo = null;
if ($event['series_id']) {
    $seriesPaymentInfo = $db->getRow("
        SELECT s.id, s.name, s.swish_number, s.swish_name
        FROM series s
        WHERE s.id = ?
    ", [$event['series_id']]);
}

// Get current organizer club info
$organizerClubInfo = null;
if (!empty($event['organizer_club_id'])) {
    $organizerClubInfo = $db->getRow("
        SELECT id, name, swish_number, swish_name
        FROM clubs
        WHERE id = ?
    ", [$event['organizer_club_id']]);
}

// Determine current payment recipient (default to 'series')
$currentRecipient = $event['payment_recipient'] ?? 'series';

// Set page variables for economy layout
$economy_page_title = 'Betalning';

include __DIR__ . '/components/economy-layout.php';
?>

        <!-- Setup Errors -->
        <?php if (!empty($setupErrors)): ?>
        <div class="alert alert-error mb-lg">
            <i data-lucide="alert-triangle"></i>
            <strong>Databasfel:</strong>
            <ul style="margin: var(--space-sm) 0 0 var(--space-lg);">
            <?php foreach ($setupErrors as $err): ?>
                <li><?= h($err) ?></li>
            <?php endforeach; ?>
            </ul>
        </div>
        <?php endif; ?>

        <!-- Message -->
        <?php if ($message): ?>
        <div class="alert alert-<?= h($messageType) ?> mb-lg">
            <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
            <?= h($message) ?>
        </div>
        <?php endif; ?>

        <!-- Stats -->
        <div class="grid grid-4 gap-md mb-lg">
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-warning"><?= $orderStats['pending_orders'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Väntar på betalning</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-success"><?= $orderStats['paid_orders'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Betalda ordrar</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-secondary"><?= $orderStats['cancelled_orders'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Avbrutna</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold"><?= number_format($orderStats['total_revenue'] ?? 0, 0, ',', ' ') ?> kr</div>
                    <div class="text-sm text-secondary">Totalt inbetalt</div>
                </div>
            </div>
        </div>

        <!-- Basic Settings -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2>
                    <i data-lucide="settings"></i>
                    Grundinställningar
                </h2>
            </div>
            <div class="card-body">
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="save_settings">

                    <div class="grid grid-2 gap-lg">
                        <div class="form-group">
                            <label class="checkbox-label">
                                <input type="checkbox" name="ticketing_enabled" value="1"
                                    <?= ($event['ticketing_enabled'] ?? 0) ? 'checked' : '' ?>>
                                <span>Aktivera betalning/biljetter</span>
                            </label>
                            <small class="text-secondary">Visar prisinfo och möjliggör betalning vid anmälan</small>
                        </div>

                        <div class="form-group">
                            <label class="label">Anmälningsfrist (dagar före event)</label>
                            <input type="number" name="ticket_deadline_days" class="input"
                                   value="<?= $event['ticket_deadline_days'] ?? 7 ?>" min="0" max="90">
                            <small class="text-secondary">Anmälan stänger detta antal dagar före eventdatum</small>
                        </div>
                    </div>

                    <div class="mt-md">
                        <button type="submit" class="btn btn--primary">
                            <i data-lucide="save"></i>
                            Spara
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Payment Recipient Selection -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2>
                    <i data-lucide="wallet"></i>
                    Betalning till
                </h2>
            </div>
            <div class="card-body">
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="save_payment_recipient">

                    <div class="grid gap-md mb-lg">
                        <!-- Option: Series -->
                        <label class="p-md rounded-md border cursor-pointer <?= $currentRecipient === 'series' ? 'border-primary bg-primary-light' : 'border-default' ?>" style="display: block;">
                            <div class="flex items-center gap-md">
                                <input type="radio" name="payment_recipient" value="series"
                                    <?= $currentRecipient === 'series' ? 'checked' : '' ?>
                                    onchange="updateRecipientUI()">
                                <div class="flex-1">
                                    <strong>Serie</strong>
                                    <?php if ($seriesPaymentInfo): ?>
                                        <span class="text-secondary"> - <?= h($seriesPaymentInfo['name']) ?></span>
                                    <?php endif; ?>
                                    <div class="text-sm text-secondary mt-xs">
                                        <?php if ($seriesPaymentInfo && $seriesPaymentInfo['swish_number']): ?>
                                            <i data-lucide="smartphone" style="width: 14px; height: 14px;"></i>
                                            Swish: <?= h($seriesPaymentInfo['swish_number']) ?>
                                            <?php if ($seriesPaymentInfo['swish_name']): ?>
                                                (<?= h($seriesPaymentInfo['swish_name']) ?>)
                                            <?php endif; ?>
                                        <?php elseif ($seriesPaymentInfo): ?>
                                            <span class="text-warning">⚠️ Serien har inga betalningsuppgifter konfigurerade</span>
                                        <?php else: ?>
                                            <span class="text-secondary">Eventet tillhör ingen serie</span>
                                        <?php endif; ?>
                                    </div>
                                </div>
                            </div>
                        </label>

                        <!-- Option: Organizer -->
                        <label class="p-md rounded-md border cursor-pointer <?= $currentRecipient === 'organizer' ? 'border-primary bg-primary-light' : 'border-default' ?>" style="display: block;">
                            <div class="flex items-center gap-md">
                                <input type="radio" name="payment_recipient" value="organizer"
                                    <?= $currentRecipient === 'organizer' ? 'checked' : '' ?>
                                    onchange="updateRecipientUI()">
                                <div class="flex-1">
                                    <strong>Arrangör (klubb)</strong>
                                    <div class="text-sm text-secondary mt-xs">
                                        Betalning går direkt till arrangörens Swish
                                    </div>
                                </div>
                            </div>
                            <!-- Organizer club selector (shown when organizer is selected) -->
                            <div id="organizer-club-selector" class="mt-md pl-lg <?= $currentRecipient === 'organizer' ? '' : 'hidden' ?>">
                                <label class="label">Välj arrangörsklubb</label>
                                <select name="organizer_club_id" class="input">
                                    <option value="">-- Välj klubb --</option>
                                    <?php foreach ($allClubs as $club): ?>
                                        <?php
                                        $hasPayment = false;
                                        foreach ($clubsWithPayment as $cp) {
                                            if ($cp['id'] == $club['id']) {
                                                $hasPayment = true;
                                                break;
                                            }
                                        }
                                        ?>
                                        <option value="<?= $club['id'] ?>"
                                            <?= ($event['organizer_club_id'] ?? '') == $club['id'] ? 'selected' : '' ?>
                                            <?= !$hasPayment ? 'style="color: #999;"' : '' ?>>
                                            <?= h($club['name']) ?><?= !$hasPayment ? ' (saknar Swish)' : '' ?>
                                        </option>
                                    <?php endforeach; ?>
                                </select>
                                <?php if ($organizerClubInfo && $organizerClubInfo['swish_number']): ?>
                                    <div class="mt-sm text-sm">
                                        <i data-lucide="smartphone" style="width: 14px; height: 14px;"></i>
                                        Swish: <?= h($organizerClubInfo['swish_number']) ?>
                                        <?php if ($organizerClubInfo['swish_name']): ?>
                                            (<?= h($organizerClubInfo['swish_name']) ?>)
                                        <?php endif; ?>
                                    </div>
                                <?php elseif ($organizerClubInfo): ?>
                                    <div class="mt-sm text-sm text-warning">
                                        ⚠️ Vald klubb saknar Swish-uppgifter.
                                        <a href="/admin/club-edit.php?id=<?= $organizerClubInfo['id'] ?>">Lägg till här</a>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </label>

                        <!-- Option: Custom -->
                        <label class="p-md rounded-md border cursor-pointer <?= $currentRecipient === 'custom' ? 'border-primary bg-primary-light' : 'border-default' ?>" style="display: block;">
                            <div class="flex items-center gap-md">
                                <input type="radio" name="payment_recipient" value="custom"
                                    <?= $currentRecipient === 'custom' ? 'checked' : '' ?>
                                    onchange="updateRecipientUI()">
                                <div class="flex-1">
                                    <strong>Anpassad</strong>
                                    <div class="text-sm text-secondary mt-xs">
                                        Ange egna Swish-uppgifter för detta event
                                    </div>
                                </div>
                            </div>
                            <!-- Custom Swish fields (shown when custom is selected) -->
                            <div id="custom-swish-fields" class="mt-md pl-lg <?= $currentRecipient === 'custom' ? '' : 'hidden' ?>">
                                <div class="grid grid-2 gap-md">
                                    <div class="form-group">
                                        <label class="label">Swish-nummer</label>
                                        <input type="text" name="custom_swish_number" class="input"
                                            value="<?= h($eventPaymentConfig['swish_number'] ?? '') ?>"
                                            placeholder="070-123 45 67">
                                    </div>
                                    <div class="form-group">
                                        <label class="label">Mottagarnamn</label>
                                        <input type="text" name="custom_swish_name" class="input"
                                            value="<?= h($eventPaymentConfig['swish_name'] ?? '') ?>"
                                            placeholder="Namn på mottagare">
                                    </div>
                                </div>
                            </div>
                        </label>
                    </div>

                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="save"></i>
                        Spara betalningsval
                    </button>
                </form>
            </div>
        </div>

        <script>
        function updateRecipientUI() {
            const selected = document.querySelector('input[name="payment_recipient"]:checked').value;

            // Update card styling
            document.querySelectorAll('input[name="payment_recipient"]').forEach(radio => {
                const card = radio.closest('label');
                if (radio.checked) {
                    card.classList.add('border-primary', 'bg-primary-light');
                    card.classList.remove('border-default');
                } else {
                    card.classList.remove('border-primary', 'bg-primary-light');
                    card.classList.add('border-default');
                }
            });

            // Show/hide organizer club selector
            const organizerSelector = document.getElementById('organizer-club-selector');
            if (selected === 'organizer') {
                organizerSelector.classList.remove('hidden');
            } else {
                organizerSelector.classList.add('hidden');
            }

            // Show/hide custom swish fields
            const customFields = document.getElementById('custom-swish-fields');
            if (selected === 'custom') {
                customFields.classList.remove('hidden');
            } else {
                customFields.classList.add('hidden');
            }
        }
        </script>

        <!-- Payment Configuration -->
        <div class="card mb-lg">
            <div class="card-header">
                <div class="flex justify-between items-center">
                    <h2>
                        <i data-lucide="credit-card"></i>
                        Betalningsmetoder
                    </h2>
                    <?php if (!$eventPaymentConfig && $paymentConfig): ?>
                    <span class="badge badge-info">
                        Ärver från: <?= htmlspecialchars($sourceName ?: ucfirst($configSource)) ?>
                    </span>
                    <?php endif; ?>
                </div>
            </div>
            <div class="card-body">
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="save_payment_config">

                    <!-- Toggle: Use event-specific config -->
                    <div class="form-group mb-lg">
                        <label class="checkbox-label">
                            <input type="checkbox" name="use_event_config" value="1" id="use-event-config"
                                <?= $eventPaymentConfig ? 'checked' : '' ?>
                                onchange="toggleEventConfig(this.checked)">
                            <span><strong>Använd event-specifik konfiguration</strong></span>
                        </label>
                        <small class="text-secondary">
                            <?php if ($event['series_name']): ?>
                                Om avmarkerat ärver eventet inställningar från serien "<?= htmlspecialchars($event['series_name']) ?>"
                            <?php else: ?>
                                Om avmarkerat används systemets standardinställningar (WooCommerce)
                            <?php endif; ?>
                        </small>
                    </div>

                    <!-- Event-specific config fields -->
                    <div id="event-config-fields" class="<?= $eventPaymentConfig ? '' : 'hidden' ?>">
                        <div class="p-md bg-muted rounded-md mb-lg">
                            <!-- Swish Settings -->
                            <h3 class="text-base font-medium mb-md">
                                <i data-lucide="smartphone"></i>
                                Swish
                            </h3>
                            <div class="grid grid-3 gap-md mb-lg">
                                <div class="form-group">
                                    <label class="checkbox-label">
                                        <input type="checkbox" name="swish_enabled" value="1"
                                            <?= ($eventPaymentConfig['swish_enabled'] ?? $paymentConfig['swish_enabled'] ?? 0) ? 'checked' : '' ?>>
                                        <span>Aktivera Swish</span>
                                    </label>
                                </div>
                                <div class="form-group">
                                    <label class="label">Swish-nummer</label>
                                    <input type="text" name="swish_number" class="input"
                                           value="<?= htmlspecialchars($eventPaymentConfig['swish_number'] ?? $paymentConfig['swish_number'] ?? '') ?>"
                                           placeholder="070-123 45 67">
                                </div>
                                <div class="form-group">
                                    <label class="label">Mottagarnamn</label>
                                    <input type="text" name="swish_name" class="input"
                                           value="<?= htmlspecialchars($eventPaymentConfig['swish_name'] ?? $paymentConfig['swish_name'] ?? '') ?>"
                                           placeholder="Klubbnamn">
                                </div>
                            </div>

                            <!-- Card Settings -->
                            <h3 class="text-base font-medium mb-md">
                                <i data-lucide="credit-card"></i>
                                Kortbetalning
                            </h3>
                            <div class="grid grid-2 gap-md">
                                <div class="form-group">
                                    <label class="checkbox-label">
                                        <input type="checkbox" name="card_enabled" value="1"
                                            <?= ($eventPaymentConfig['card_enabled'] ?? 0) ? 'checked' : '' ?>>
                                        <span>Aktivera kortbetalning (WooCommerce)</span>
                                    </label>
                                </div>
                                <div class="form-group">
                                    <label class="label">WooCommerce Produkt-ID</label>
                                    <input type="text" name="woo_product_id" class="input"
                                           value="<?= htmlspecialchars($event['woo_product_id'] ?? '') ?>"
                                           placeholder="12345">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Show inherited config when not using event-specific -->
                    <?php if (!$eventPaymentConfig && $paymentConfig): ?>
                    <div id="inherited-config-display" class="p-md bg-muted rounded-md mb-lg">
                        <h4 class="text-sm font-medium text-secondary mb-sm">Ärvda inställningar:</h4>
                        <div class="grid grid-2 gap-sm text-sm">
                            <div>
                                <span class="text-secondary">Swish:</span>
                                <?= $paymentConfig['swish_enabled'] ? '<span class="badge badge-success">Aktivt</span>' : '<span class="badge badge-secondary">Inaktivt</span>' ?>
                            </div>
                            <?php if ($paymentConfig['swish_number']): ?>
                            <div>
                                <span class="text-secondary">Nummer:</span>
                                <strong><?= htmlspecialchars($paymentConfig['swish_number']) ?></strong>
                            </div>
                            <?php endif; ?>
                            <?php if ($paymentConfig['swish_name']): ?>
                            <div>
                                <span class="text-secondary">Mottagare:</span>
                                <strong><?= htmlspecialchars($paymentConfig['swish_name']) ?></strong>
                            </div>
                            <?php endif; ?>
                        </div>
                    </div>
                    <?php endif; ?>

                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="save"></i>
                        Spara betalningsinställningar
                    </button>
                </form>
            </div>
        </div>

        <!-- Pricing -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2>
                    <i data-lucide="tag"></i>
                    Prissättning per klass
                </h2>
            </div>
            <div class="card-body">
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="save_pricing">

                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Klass</th>
                                    <th style="width: 120px;">Pris (kr)</th>
                                    <th style="width: 100px;">Early bird %</th>
                                    <th style="width: 150px;">Early bird t.o.m.</th>
                                    <th style="width: 100px;">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($classes as $class): ?>
                                <tr>
                                    <td>
                                        <input type="hidden" name="class_id[]" value="<?= $class['id'] ?>">
                                        <strong><?= htmlspecialchars($class['display_name']) ?></strong>
                                        <span class="text-secondary text-xs">(<?= htmlspecialchars($class['name']) ?>)</span>
                                    </td>
                                    <td>
                                        <input type="number" name="base_price[]" class="input input--sm"
                                               value="<?= $class['base_price'] ?? '' ?>"
                                               placeholder="0" min="0" step="10">
                                    </td>
                                    <td>
                                        <input type="number" name="early_bird_discount[]" class="input input--sm"
                                               value="<?= $class['early_bird_discount_percent'] ?? '20' ?>"
                                               placeholder="20" min="0" max="100">
                                    </td>
                                    <td>
                                        <input type="date" name="early_bird_end_date[]" class="input input--sm"
                                               value="<?= $class['early_bird_end_date'] ?? $defaultEarlyBirdEnd->format('Y-m-d') ?>">
                                    </td>
                                    <td>
                                        <?php if ($class['base_price'] > 0): ?>
                                            <span class="badge badge-success">Aktiv</span>
                                        <?php else: ?>
                                            <span class="badge badge-secondary">Ej satt</span>
                                        <?php endif; ?>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>

                    <div class="mt-lg">
                        <button type="submit" class="btn btn--primary">
                            <i data-lucide="save"></i>
                            Spara priser
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Quick Links -->
        <div class="card">
            <div class="card-header">
                <h2>
                    <i data-lucide="link"></i>
                    Snabblänkar
                </h2>
            </div>
            <div class="card-body">
                <div class="flex gap-md flex-wrap">
                    <a href="/admin/event-tickets.php?id=<?= $eventId ?>" class="btn btn--secondary">
                        <i data-lucide="ticket"></i>
                        Hantera biljetter
                    </a>
                    <a href="/event/<?= $eventId ?>?tab=biljetter" class="btn btn--secondary" target="_blank">
                        <i data-lucide="external-link"></i>
                        Förhandsgranska publik sida
                    </a>
                    <?php if ($event['series_id']): ?>
                    <a href="/admin/payment-settings.php" class="btn btn--secondary">
                        <i data-lucide="settings"></i>
                        Serie-betalningsinställningar
                    </a>
                    <?php endif; ?>
                </div>
            </div>
        </div>

<style>
/* Match orders.php styling */
.bg-muted {
    background: var(--color-bg-card);
}
.hidden {
    display: none !important;
}
.input--sm {
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--text-sm);
}
.badge-warning {
    background: rgba(234, 179, 8, 0.2);
    color: #ca8a04;
}
.badge-success {
    background: rgba(34, 197, 94, 0.2);
    color: #16a34a;
}
.badge-info {
    background: rgba(59, 130, 246, 0.2);
    color: #2563eb;
}
</style>

<script>
function toggleEventConfig(checked) {
    const fields = document.getElementById('event-config-fields');
    const inherited = document.getElementById('inherited-config-display');

    if (checked) {
        fields.classList.remove('hidden');
        if (inherited) inherited.classList.add('hidden');
    } else {
        fields.classList.add('hidden');
        if (inherited) inherited.classList.remove('hidden');
    }
}

// Initialize Lucide icons
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/economy-layout-footer.php'; ?>
