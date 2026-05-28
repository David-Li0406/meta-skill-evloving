<?php
/**
 * Admin Series Edit - V3 Unified Design System
 * Dedicated page for editing series (like event-edit.php)
 * Supports both admin and promotor access (via promotor_series)
 */
require_once __DIR__ . '/../config.php';

// Require login (admin OR promotor)
if (!isLoggedIn()) {
    header('Location: /login?redirect=' . urlencode($_SERVER['REQUEST_URI']));
    exit;
}

// Check access after we know the series ID (done below)
$db = getDB();

// Get series ID from URL (supports both /admin/series/edit/123 and ?id=123)
$id = 0;
if (isset($_GET['id'])) {
    $id = intval($_GET['id']);
} else {
    // Check for pretty URL format
    $uri = $_SERVER['REQUEST_URI'];
    if (preg_match('#/admin/series/edit/(\d+)#', $uri, $matches)) {
        $id = intval($matches[1]);
    }
}

// Check if creating new series
$isNew = ($id === 0 && isset($_GET['new']));

if ($id <= 0 && !$isNew) {
    $_SESSION['message'] = 'Ogiltigt serie-ID';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/series');
    exit;
}

// Check access: Admin can access all, promotors need to be linked via promotor_series
// For new series, only admins can create (promotors must be assigned by admin)
if ($isNew) {
    if (!hasRole('admin')) {
        $_SESSION['message'] = 'Du har inte behörighet att skapa nya serier';
        $_SESSION['messageType'] = 'error';
        header('Location: /admin/series');
        exit;
    }
} else {
    if (!canAccessSeries($id)) {
        $_SESSION['message'] = 'Du har inte behörighet att redigera denna serie';
        $_SESSION['messageType'] = 'error';
        header('Location: /admin/series');
        exit;
    }
}

// Check if user is promotor (limited editing)
$isPromotor = isRole('promotor');

// Set default values for new series (must be before POST handler)
// Note: Logo is inherited from brand, not stored per series
$series = [
    'id' => 0,
    'name' => '',
    'year' => date('Y'),
    'type' => '',
    'format' => 'Championship',
    'status' => 'planning',
    'start_date' => '',
    'end_date' => '',
    'description' => '',
    'organizer' => '',
    'brand_id' => null,
    'swish_number' => '',
    'swish_name' => '',
];

// Fetch series data if editing
if (!$isNew) {
    $fetchedSeries = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);

    if (!$fetchedSeries) {
        $_SESSION['message'] = 'Serie hittades inte';
        $_SESSION['messageType'] = 'error';
        header('Location: /admin/series');
        exit;
    }
    $series = array_merge($series, $fetchedSeries);
}

// Check if year column exists
$yearColumnExists = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'year'");
    if (empty($columns)) {
        // Add year column if it doesn't exist
        $db->query("ALTER TABLE series ADD COLUMN year INT DEFAULT NULL AFTER name");
        $yearColumnExists = true;
    } else {
        $yearColumnExists = true;
    }
} catch (Exception $e) {
    error_log("SERIES EDIT: Error checking/adding year column: " . $e->getMessage());
}

// Check if format column exists
$formatColumnExists = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");
    $formatColumnExists = !empty($columns);
} catch (Exception $e) {}

// Check if brand_id column exists and get brands
$brandColumnExists = false;
$brands = [];
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'brand_id'");
    $brandColumnExists = !empty($columns);
    if ($brandColumnExists) {
        $tables = $db->getAll("SHOW TABLES LIKE 'series_brands'");
        if (!empty($tables)) {
            $brands = $db->getAll("SELECT id, name FROM series_brands WHERE active = 1 ORDER BY display_order ASC, name ASC");
        }
    }
} catch (Exception $e) {}

// Check if swish columns exist
$swishColumnsExist = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'swish_number'");
    $swishColumnsExist = !empty($columns);
} catch (Exception $e) {}

// Check if payment_recipient_id column exists and get recipients
$paymentRecipientColumnExists = false;
$paymentRecipients = [];
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'payment_recipient_id'");
    $paymentRecipientColumnExists = !empty($columns);
    if ($paymentRecipientColumnExists) {
        $tables = $db->getAll("SHOW TABLES LIKE 'payment_recipients'");
        if (!empty($tables)) {
            $paymentRecipients = $db->getAll("SELECT id, name, swish_number, swish_name FROM payment_recipients WHERE active = 1 ORDER BY name ASC");
        }
    }
} catch (Exception $e) {}

// Check if stage_bonus_config column exists
$stageBonusColumnExists = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'stage_bonus_config'");
    $stageBonusColumnExists = !empty($columns);
} catch (Exception $e) {}

// Get all classes for stage bonus configuration
$allClasses = [];
try {
    $allClasses = $db->getAll("SELECT id, display_name, sort_order FROM classes WHERE active = 1 ORDER BY sort_order");
} catch (Exception $e) {}

// Default point scales for stage bonus
$stageBonusScales = [
    'top3' => ['name' => 'Topp 3', 'points' => [25, 20, 16]],
    'top5' => ['name' => 'Topp 5', 'points' => [25, 20, 16, 13, 11]],
    'top10' => ['name' => 'Topp 10', 'points' => [25, 20, 16, 13, 11, 10, 9, 8, 7, 6]],
    'top3_small' => ['name' => 'Topp 3 (liten)', 'points' => [10, 7, 5]],
    'top5_small' => ['name' => 'Topp 5 (liten)', 'points' => [10, 7, 5, 3, 2]],
];

// Function to save sponsor assignments
function saveSponsorAssignments($db, $seriesId, $postData) {
    $pdo = $db->getPdo();

    // First, delete existing sponsor assignments for this series
    $deleteStmt = $pdo->prepare("DELETE FROM series_sponsors WHERE series_id = ?");
    $deleteStmt->execute([$seriesId]);

    // Insert new assignments
    $insertStmt = $pdo->prepare("INSERT INTO series_sponsors (series_id, sponsor_id, placement, display_order) VALUES (?, ?, ?, ?)");

    // Header sponsor (single select)
    if (!empty($postData['sponsor_header'])) {
        $insertStmt->execute([$seriesId, (int)$postData['sponsor_header'], 'header', 0]);
    }

    // Content sponsors (multiple checkboxes)
    if (!empty($postData['sponsor_content']) && is_array($postData['sponsor_content'])) {
        $order = 0;
        foreach ($postData['sponsor_content'] as $sponsorId) {
            $insertStmt->execute([$seriesId, (int)$sponsorId, 'content', $order++]);
        }
    }

    // Sidebar/Results sponsor (single select)
    if (!empty($postData['sponsor_sidebar'])) {
        $insertStmt->execute([$seriesId, (int)$postData['sponsor_sidebar'], 'sidebar', 0]);
    }
}

// Initialize message variables
$message = '';
$messageType = 'info';

// Check if we just saved
if (isset($_GET['saved']) && $_GET['saved'] == '1' && isset($_SESSION['message'])) {
    $message = $_SESSION['message'];
    $messageType = $_SESSION['messageType'] ?? 'success';
    unset($_SESSION['message'], $_SESSION['messageType']);
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $name = trim($_POST['name'] ?? '');

    $year = !empty($_POST['year']) ? intval($_POST['year']) : null;

    if (empty($name)) {
        $message = 'Namn är obligatoriskt';
        $messageType = 'error';
    } elseif (empty($year)) {
        $message = 'År är obligatoriskt - ange vilket år serien gäller';
        $messageType = 'error';
    } else {
        // Prepare series data (logo inherited from brand, not uploaded per series)
        $seriesData = [
            'name' => $name,
            'type' => trim($_POST['type'] ?? ''),
            'status' => $_POST['status'] ?? 'planning',
            'start_date' => !empty($_POST['start_date']) ? trim($_POST['start_date']) : null,
            'end_date' => !empty($_POST['end_date']) ? trim($_POST['end_date']) : null,
            'description' => trim($_POST['description'] ?? ''),
            'organizer' => trim($_POST['organizer'] ?? ''),
        ];

        // Year is always required now
        if ($yearColumnExists) {
            $seriesData['year'] = $year;
        }

        // Add format if column exists
        if ($formatColumnExists) {
            $seriesData['format'] = $_POST['format'] ?? 'Championship';
        }

        // Add brand_id if column exists
        if ($brandColumnExists) {
            $seriesData['brand_id'] = !empty($_POST['brand_id']) ? intval($_POST['brand_id']) : null;
        }

        // Add Swish payment fields if columns exist
        if ($swishColumnsExist) {
            $seriesData['swish_number'] = trim($_POST['swish_number'] ?? '') ?: null;
            $seriesData['swish_name'] = trim($_POST['swish_name'] ?? '') ?: null;
        }

        // Add payment_recipient_id if column exists
        if ($paymentRecipientColumnExists) {
            $seriesData['payment_recipient_id'] = !empty($_POST['payment_recipient_id']) ? intval($_POST['payment_recipient_id']) : null;
        }

        // Add gravity_id_discount (0 = disabled, >0 = discount amount in SEK)
        $seriesData['gravity_id_discount'] = floatval($_POST['gravity_id_discount'] ?? 0);

        // Add historical_data_verified
        $seriesData['historical_data_verified'] = isset($_POST['historical_data_verified']) ? 1 : 0;

        // Add stage_bonus_config if column exists
        if ($stageBonusColumnExists) {
            $stageBonusEnabled = isset($_POST['stage_bonus_enabled']) && $_POST['stage_bonus_enabled'] === '1';
            if ($stageBonusEnabled) {
                $stageBonusConfig = [
                    'enabled' => true,
                    'stage' => $_POST['stage_bonus_stage'] ?? 'ss1',
                    'scale' => $_POST['stage_bonus_scale'] ?? 'top3',
                    'points' => $stageBonusScales[$_POST['stage_bonus_scale'] ?? 'top3']['points'] ?? [25, 20, 16],
                    'class_ids' => !empty($_POST['stage_bonus_class_ids']) ? array_map('intval', $_POST['stage_bonus_class_ids']) : null,
                ];
                $seriesData['stage_bonus_config'] = json_encode($stageBonusConfig);
            } else {
                $seriesData['stage_bonus_config'] = null;
            }
        }

        try {
            // Check if we're marking as completed (and it wasn't before)
            $wasCompleted = !$isNew && ($series['status'] ?? '') === 'completed';
            $isNowCompleted = $seriesData['status'] === 'completed';
            $justCompleted = !$wasCompleted && $isNowCompleted;
            $calculateChampions = isset($_POST['calculate_champions']) && $_POST['calculate_champions'] === '1';

            if ($isNew) {
                $newId = $db->insert('series', $seriesData);

                // Save sponsor assignments for new series
                saveSponsorAssignments($db, $newId, $_POST);

                $_SESSION['message'] = 'Serie skapad!';
                $_SESSION['messageType'] = 'success';
                header('Location: /admin/series/edit/' . $newId . '?saved=1');
                exit;
            } else {
                $db->update('series', $seriesData, 'id = ?', [$id]);

                // Save sponsor assignments for existing series
                saveSponsorAssignments($db, $id, $_POST);

                // If just marked as completed and user confirmed to calculate champions
                if ($justCompleted && $calculateChampions) {
                    require_once __DIR__ . '/../includes/rebuild-rider-stats.php';
                    $pdo = $db->getPdo();

                    // Rebuild stats for all riders who have results in this series
                    $ridersStmt = $pdo->prepare("
                        SELECT DISTINCT r.cyclist_id
                        FROM results r
                        JOIN events e ON r.event_id = e.id
                        JOIN series_events se ON se.event_id = e.id
                        WHERE se.series_id = ? AND r.cyclist_id IS NOT NULL
                    ");
                    $ridersStmt->execute([$id]);
                    $riderIds = $ridersStmt->fetchAll(PDO::FETCH_COLUMN);

                    $championCount = 0;
                    foreach ($riderIds as $riderId) {
                        rebuildRiderStats($pdo, $riderId);
                        // Check if this rider got a championship for this series
                        $checkStmt = $pdo->prepare("
                            SELECT COUNT(*) FROM rider_achievements
                            WHERE rider_id = ? AND achievement_type = 'series_champion' AND series_id = ?
                        ");
                        $checkStmt->execute([$riderId, $id]);
                        if ($checkStmt->fetchColumn() > 0) {
                            $championCount++;
                        }
                    }

                    $_SESSION['message'] = "Serie avslutad! Beräknade {$championCount} seriemästare.";
                    $_SESSION['messageType'] = 'success';
                } else {
                    $_SESSION['message'] = 'Serie uppdaterad!';
                    $_SESSION['messageType'] = 'success';
                }

                header('Location: /admin/series/edit/' . $id . '?saved=1');
                exit;
            }
        } catch (Exception $e) {
            error_log("SERIES EDIT ERROR: " . $e->getMessage());
            $message = 'Ett fel uppstod: ' . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Re-fetch series data after potential update (for display)
if (!$isNew && $id > 0) {
    $fetchedSeries = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);
    if ($fetchedSeries) {
        $series = array_merge($series, $fetchedSeries);
    }
}

// Get all sponsors for selection
$allSponsors = [];
$seriesSponsors = ['header' => [], 'content' => [], 'sidebar' => []];
try {
    $allSponsors = $db->getAll("SELECT id, name, logo, tier FROM sponsors WHERE active = 1 ORDER BY tier ASC, name ASC");

    if (!$isNew && $id > 0) {
        $sponsorAssignments = $db->getAll("
            SELECT sponsor_id, placement
            FROM series_sponsors
            WHERE series_id = ?
        ", [$id]);
        foreach ($sponsorAssignments as $sa) {
            $placement = $sa['placement'] ?? 'sidebar';
            $seriesSponsors[$placement][] = (int)$sa['sponsor_id'];
        }
    }
} catch (Exception $e) {
    error_log("Could not load sponsors: " . $e->getMessage());
}

// Get events count and results status for this series
$eventsCount = 0;
$eventsWithResults = 0;
$readyToComplete = false;
if (!$isNew) {
    // Check if series_events table exists
    $seriesEventsExists = false;
    try {
        $tables = $db->getAll("SHOW TABLES LIKE 'series_events'");
        $seriesEventsExists = !empty($tables);
    } catch (Exception $e) {}

    if ($seriesEventsExists) {
        // Count events via junction table
        $eventsCount = $db->getValue("SELECT COUNT(*) FROM series_events WHERE series_id = ?", [$id]) ?: 0;
        // Count events with at least one finished result
        $eventsWithResults = $db->getValue("
            SELECT COUNT(DISTINCT se.event_id)
            FROM series_events se
            INNER JOIN results r ON r.event_id = se.event_id
            WHERE se.series_id = ? AND r.status = 'finished'
        ", [$id]) ?: 0;
    } else {
        $eventsCount = $db->getValue("SELECT COUNT(*) FROM events WHERE series_id = ?", [$id]) ?: 0;
    }

    // Check if ready to complete (all events have results but not marked completed)
    $readyToComplete = $eventsCount > 0
        && $eventsWithResults >= $eventsCount
        && ($series['status'] ?? '') !== 'completed';
}

// Page config
$page_title = $isNew ? 'Ny Serie' : 'Redigera Serie: ' . htmlspecialchars($series['name']);
$breadcrumbs = [
    ['label' => 'Serier', 'url' => '/admin/series'],
    ['label' => $isNew ? 'Ny' : htmlspecialchars($series['name'])]
];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?>">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <?php if ($messageType === 'success'): ?>
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
        <?php elseif ($messageType === 'error'): ?>
            <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>
        <?php else: ?>
            <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/>
        <?php endif; ?>
    </svg>
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<?php if ($readyToComplete): ?>
<div class="alert alert-warning flex items-center justify-between gap-md">
    <div class="flex items-center gap-sm">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md flex-shrink-0">
            <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
        </svg>
        <div>
            <strong>Alla <?= $eventsCount ?> events har resultat!</strong>
            <span class="text-secondary">
                Ändra status till "Avslutad" för att beräkna seriemästare.
            </span>
        </div>
    </div>
    <button type="button" onclick="document.getElementById('status').value='completed'; document.getElementById('status').dispatchEvent(new Event('change'));"
            class="btn-admin btn-admin-warning nowrap">
        Markera avslutad
    </button>
</div>
<?php endif; ?>

<?php
// Get current tab
$currentTab = $_GET['tab'] ?? 'info';
if (!in_array($currentTab, ['info', 'events', 'rules'])) {
    $currentTab = 'info';
}

// For new series, only show info tab
if ($isNew) {
    $currentTab = 'info';
}
?>

<!-- Tab Navigation -->
<?php if (!$isNew): ?>
<div class="admin-tabs mb-lg">
    <a href="?id=<?= $id ?>&tab=info" class="admin-tab <?= $currentTab === 'info' ? 'active' : '' ?>">
        <i data-lucide="settings"></i> Info
    </a>
    <a href="?id=<?= $id ?>&tab=events" class="admin-tab <?= $currentTab === 'events' ? 'active' : '' ?>">
        <i data-lucide="calendar"></i> Events (<?= $eventsCount ?>)
    </a>
    <a href="?id=<?= $id ?>&tab=rules" class="admin-tab <?= $currentTab === 'rules' ? 'active' : '' ?>">
        <i data-lucide="shield"></i> Regler
    </a>
</div>
<?php endif; ?>

<?php if ($currentTab === 'info'): ?>
<!-- INFO TAB -->
<form method="POST">
    <?= csrf_field() ?>
    <input type="hidden" name="calculate_champions" id="calculate_champions" value="0">

    <!-- Basic Info -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 20px; height: 20px;"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                Grundläggande information
            </h2>
        </div>
        <div class="admin-card-body">
            <?php if ($brandColumnExists && !empty($brands)): ?>
            <div class="admin-form-group admin-form-group--highlight mb-md">
                <label for="brand_id" class="admin-form-label font-semibold">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm inline align-middle mr-xs"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                    Huvudserie (Varumärke) <span class="text-error">*</span>
                </label>
                <select id="brand_id" name="brand_id" class="admin-form-select" required onchange="updateSeriesName()">
                    <option value="">-- Välj huvudserie --</option>
                    <?php foreach ($brands as $brand): ?>
                    <option value="<?= $brand['id'] ?>" data-name="<?= htmlspecialchars($brand['name']) ?>" <?= ($series['brand_id'] ?? '') == $brand['id'] ? 'selected' : '' ?>>
                        <?= htmlspecialchars($brand['name']) ?>
                    </option>
                    <?php endforeach; ?>
                </select>
                <small class="text-secondary text-xs">
                    Detta är den övergripande serien (t.ex. "Swecup", "GravitySeries Enduro").
                    <a href="/admin/series/brands" class="text-accent">Hantera huvudserier</a>
                </small>
            </div>
            <?php endif; ?>

            <div class="admin-form-row">
                <div class="admin-form-group flex-1">
                    <label for="year" class="admin-form-label">
                        Säsong/År <span class="text-error">*</span>
                    </label>
                    <input type="number" id="year" name="year" class="admin-form-input" required
                           value="<?= htmlspecialchars($series['year'] ?? date('Y')) ?>"
                           min="2000" max="2100">
                    <small class="text-secondary text-xs">
                        Vilket år gäller denna säsong? Avgör vilka event som tillhör serien.
                    </small>
                </div>
                <div class="admin-form-group flex-2">
                    <label for="name" class="admin-form-label">Serienamn <span class="text-error">*</span></label>
                    <input type="text" id="name" name="name" class="admin-form-input" required
                           value="<?= htmlspecialchars($series['name'] ?? '') ?>"
                           placeholder="T.ex. Swecup">
                    <small class="text-secondary text-xs">
                        År visas separat som badge - skriv ej år i namnet
                    </small>
                </div>
            </div>

            <div class="admin-form-row">
                <div class="admin-form-group">
                    <label for="type" class="admin-form-label">Typ</label>
                    <input type="text" id="type" name="type" class="admin-form-input"
                           value="<?= htmlspecialchars($series['type'] ?? '') ?>"
                           placeholder="T.ex. Enduro, DH, XC">
                </div>
                <?php if ($formatColumnExists): ?>
                <div class="admin-form-group">
                    <label for="format" class="admin-form-label">Format</label>
                    <select id="format" name="format" class="admin-form-select">
                        <option value="Championship" <?= ($series['format'] ?? '') === 'Championship' ? 'selected' : '' ?>>Championship</option>
                        <option value="Team" <?= ($series['format'] ?? '') === 'Team' ? 'selected' : '' ?>>Team</option>
                    </select>
                </div>
                <?php endif; ?>
                <div class="admin-form-group">
                    <label for="status" class="admin-form-label">Status</label>
                    <select id="status" name="status" class="admin-form-select">
                        <option value="planning" <?= ($series['status'] ?? '') === 'planning' ? 'selected' : '' ?>>Planering</option>
                        <option value="active" <?= ($series['status'] ?? '') === 'active' ? 'selected' : '' ?>>Aktiv</option>
                        <option value="completed" <?= ($series['status'] ?? '') === 'completed' ? 'selected' : '' ?>>Avslutad</option>
                        <option value="cancelled" <?= ($series['status'] ?? '') === 'cancelled' ? 'selected' : '' ?>>Inställd</option>
                    </select>
                    <small class="text-secondary text-xs">
                        "Avslutad" beräknar seriemästare automatiskt
                    </small>
                </div>
            </div>

            <?php if (($series['year'] ?? date('Y')) <= 2024): ?>
            <div class="admin-form-group mt-md">
                <label class="checkbox-label">
                    <input type="checkbox" name="historical_data_verified" value="1"
                           <?= !empty($series['historical_data_verified']) ? 'checked' : '' ?>>
                    <span>Historisk data verifierad</span>
                </label>
                <small class="text-secondary text-xs d-block mt-xs">
                    Bocka i när serietabellen är korrekt. Tar bort varningsmeddelandet för användare.
                </small>
            </div>
            <?php endif; ?>

            <details class="mt-sm">
                <summary class="cursor-pointer text-secondary text-sm">
                    Valfritt: Specifika datum (normalt beräknas detta från events)
                </summary>
                <div class="admin-form-row mt-sm">
                    <div class="admin-form-group">
                        <label for="start_date" class="admin-form-label">Startdatum</label>
                        <input type="date" id="start_date" name="start_date" class="admin-form-input"
                               value="<?= htmlspecialchars($series['start_date'] ?? '') ?>">
                        <small class="text-secondary text-xs">
                            Lämna tomt för att använda första eventets datum
                        </small>
                    </div>
                    <div class="admin-form-group">
                        <label for="end_date" class="admin-form-label">Slutdatum</label>
                        <input type="date" id="end_date" name="end_date" class="admin-form-input"
                               value="<?= htmlspecialchars($series['end_date'] ?? '') ?>">
                        <small class="text-secondary text-xs">
                            Lämna tomt för att använda sista eventets datum
                        </small>
                    </div>
                </div>
            </details>
        </div>
    </div>

    <!-- Organizer & Description -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 20px; height: 20px;"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                Arrangör & Beskrivning
            </h2>
        </div>
        <div class="admin-card-body">
            <div class="admin-form-group">
                <label for="organizer" class="admin-form-label">Arrangör</label>
                <input type="text" id="organizer" name="organizer" class="admin-form-input"
                       value="<?= htmlspecialchars($series['organizer'] ?? '') ?>"
                       placeholder="T.ex. Svenska Cykelförbundet">
            </div>

            <div class="admin-form-group">
                <label for="description" class="admin-form-label">Beskrivning</label>
                <textarea id="description" name="description" class="admin-form-textarea" rows="4"
                          placeholder="Beskriv serien..."><?= htmlspecialchars($series['description'] ?? '') ?></textarea>
            </div>
        </div>
    </div>

    <?php if ($paymentRecipientColumnExists && !empty($paymentRecipients)): ?>
    <!-- Payment Recipient (dropdown) -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg>
                Betalningsmottagare (Swish)
            </h2>
        </div>
        <div class="admin-card-body">
            <p class="text-secondary mb-md">
                Välj vem som tar emot Swish-betalningar för denna serie. Event utan egen mottagare använder seriens.
            </p>
            <div class="admin-form-group">
                <label for="payment_recipient_id" class="admin-form-label">Betalningsmottagare</label>
                <select id="payment_recipient_id" name="payment_recipient_id" class="admin-form-select">
                    <option value="">-- Ingen (betalning inaktiverad) --</option>
                    <?php foreach ($paymentRecipients as $recipient): ?>
                    <option value="<?= $recipient['id'] ?>" <?= ($series['payment_recipient_id'] ?? '') == $recipient['id'] ? 'selected' : '' ?>>
                        <?= htmlspecialchars($recipient['name']) ?> (<?= htmlspecialchars($recipient['swish_number']) ?>)
                    </option>
                    <?php endforeach; ?>
                </select>
                <small class="text-secondary">
                    <a href="/admin/payment-recipients" class="text-accent">Hantera betalningsmottagare</a>
                </small>
            </div>

            <?php
            // Show selected recipient details
            $selectedRecipient = null;
            if (!empty($series['payment_recipient_id'])) {
                foreach ($paymentRecipients as $r) {
                    if ($r['id'] == $series['payment_recipient_id']) {
                        $selectedRecipient = $r;
                        break;
                    }
                }
            }
            if ($selectedRecipient):
            ?>
            <div class="info-box mt-md">
                <div class="grid-2-col">
                    <div>
                        <span class="text-secondary text-xs">Swish-nummer:</span><br>
                        <strong><?= htmlspecialchars($selectedRecipient['swish_number']) ?></strong>
                    </div>
                    <div>
                        <span class="text-secondary text-xs">Visas som:</span><br>
                        <strong><?= htmlspecialchars($selectedRecipient['swish_name']) ?></strong>
                    </div>
                </div>
            </div>
            <?php endif; ?>
        </div>
    </div>
    <?php elseif ($swishColumnsExist): ?>
    <!-- Fallback: Manual Swish fields -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg>
                Betalning (Swish)
            </h2>
        </div>
        <div class="admin-card-body">
            <p class="text-secondary mb-md">
                Swish-uppgifter för serieanmälningar. Event kan välja att betalning går till serien.
            </p>
            <div class="admin-form-row">
                <div class="admin-form-group">
                    <label for="swish_number" class="admin-form-label">Swish-nummer</label>
                    <input type="text" id="swish_number" name="swish_number" class="admin-form-input"
                           value="<?= htmlspecialchars($series['swish_number'] ?? '') ?>"
                           placeholder="070-123 45 67 eller 123-456 78 90">
                    <small class="text-secondary">Mobilnummer eller Swish-företagsnummer</small>
                </div>
                <div class="admin-form-group">
                    <label for="swish_name" class="admin-form-label">Mottagarnamn</label>
                    <input type="text" id="swish_name" name="swish_name" class="admin-form-input"
                           value="<?= htmlspecialchars($series['swish_name'] ?? '') ?>"
                           placeholder="Seriens namn">
                    <small class="text-secondary">Visas för deltagare vid betalning</small>
                </div>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <!-- Gravity ID Discount -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <i data-lucide="badge-check" class="icon-md"></i>
                Gravity ID-rabatt
            </h2>
        </div>
        <div class="admin-card-body">
            <p class="text-secondary mb-md">
                Sätt rabatt för deltagare med Gravity ID. Lämna 0 för att inaktivera rabatten för denna serie.
            </p>
            <div class="admin-form-row">
                <div class="admin-form-group">
                    <label for="gravity_id_discount" class="admin-form-label">Rabatt (SEK)</label>
                    <input type="number" id="gravity_id_discount" name="gravity_id_discount" class="admin-form-input"
                           value="<?= htmlspecialchars($series['gravity_id_discount'] ?? 0) ?>"
                           min="0" step="1" placeholder="0">
                    <small class="text-secondary">0 = inaktiverat, t.ex. 50 = 50 kr rabatt</small>
                </div>
            </div>
            <?php
            // Show info about GID members
            try {
                $gidCount = $db->getRow("SELECT COUNT(*) as cnt FROM riders WHERE gravity_id IS NOT NULL AND gravity_id != ''");
                if ($gidCount && $gidCount['cnt'] > 0):
            ?>
            <div class="info-box mt-md">
                <span class="text-accent font-semibold"><?= $gidCount['cnt'] ?></span> åkare har Gravity ID.
                <a href="/admin/gravity-id.php" class="text-accent ml-sm">Hantera medlemmar</a>
            </div>
            <?php
                endif;
            } catch (Exception $e) {}
            ?>
        </div>
    </div>

    <!-- Sponsors -->
    <?php if (!empty($allSponsors)): ?>
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
                Sponsorer
            </h2>
        </div>
        <div class="admin-card-body">
            <p class="text-secondary text-sm mb-md">
                Välj sponsorer för denna serie. De visas på alla events i serien.
            </p>

            <div class="flex flex-col gap-lg">
                <!-- Header Banner Sponsor -->
                <div class="admin-form-group">
                    <label class="admin-form-label">Header-banner (stor banner högst upp)</label>
                    <select name="sponsor_header" class="admin-form-select">
                        <option value="">-- Ingen --</option>
                        <?php foreach ($allSponsors as $sp): ?>
                        <option value="<?= $sp['id'] ?>" <?= in_array((int)$sp['id'], $seriesSponsors['header']) ? 'selected' : '' ?>>
                            <?= htmlspecialchars($sp['name']) ?> (<?= ucfirst($sp['tier']) ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <!-- Content Logo Row -->
                <div class="admin-form-group">
                    <label class="admin-form-label">Logo-rad (under event-info)</label>
                    <div class="flex flex-wrap gap-sm">
                        <?php foreach ($allSponsors as $sp): ?>
                        <label class="checkbox-chip">
                            <input type="checkbox" name="sponsor_content[]" value="<?= $sp['id'] ?>" <?= in_array((int)$sp['id'], $seriesSponsors['content']) ? 'checked' : '' ?>>
                            <?= htmlspecialchars($sp['name']) ?>
                        </label>
                        <?php endforeach; ?>
                    </div>
                </div>

                <!-- Results Sponsor -->
                <div class="admin-form-group">
                    <label class="admin-form-label">Resultat-sponsor ("Resultat sponsrat av")</label>
                    <select name="sponsor_sidebar" class="admin-form-select">
                        <option value="">-- Ingen --</option>
                        <?php foreach ($allSponsors as $sp): ?>
                        <option value="<?= $sp['id'] ?>" <?= in_array((int)$sp['id'], $seriesSponsors['sidebar']) ? 'selected' : '' ?>>
                            <?= htmlspecialchars($sp['name']) ?> (<?= ucfirst($sp['tier']) ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <!-- Stage Bonus Configuration -->
    <?php if ($stageBonusColumnExists): ?>
    <?php
    // Parse existing stage bonus config
    $currentStageBonus = null;
    if (!empty($series['stage_bonus_config'])) {
        $currentStageBonus = json_decode($series['stage_bonus_config'], true);
    }
    $stageBonusEnabled = $currentStageBonus['enabled'] ?? false;
    $stageBonusStage = $currentStageBonus['stage'] ?? 'ss1';
    $stageBonusScale = $currentStageBonus['scale'] ?? 'top3';
    $stageBonusClassIds = $currentStageBonus['class_ids'] ?? [];
    ?>
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <i data-lucide="trophy" class="icon-md"></i>
                Sträckbonus (automatisk)
            </h2>
        </div>
        <div class="admin-card-body">
            <p class="text-secondary text-sm mb-md">
                Ge automatiskt bonuspoäng till snabbaste på en sträcka när resultat importeras.
            </p>

            <div class="admin-form-group mb-md">
                <label class="checkbox-label">
                    <input type="checkbox" name="stage_bonus_enabled" value="1"
                           <?= $stageBonusEnabled ? 'checked' : '' ?>
                           onchange="toggleStageBonusConfig(this.checked)">
                    <span>Aktivera automatisk sträckbonus</span>
                </label>
            </div>

            <div id="stage-bonus-config" style="<?= $stageBonusEnabled ? '' : 'display: none;' ?>">
                <div class="admin-form-row">
                    <div class="admin-form-group">
                        <label class="admin-form-label">Sträcka</label>
                        <select name="stage_bonus_stage" class="admin-form-select">
                            <?php for ($i = 1; $i <= 8; $i++): ?>
                            <option value="ss<?= $i ?>" <?= $stageBonusStage === "ss{$i}" ? 'selected' : '' ?>>
                                SS<?= $i ?> / PS<?= $i ?>
                            </option>
                            <?php endfor; ?>
                        </select>
                    </div>
                    <div class="admin-form-group">
                        <label class="admin-form-label">Poängskala</label>
                        <select name="stage_bonus_scale" class="admin-form-select">
                            <?php foreach ($stageBonusScales as $key => $scale): ?>
                            <option value="<?= $key ?>" <?= $stageBonusScale === $key ? 'selected' : '' ?>>
                                <?= htmlspecialchars($scale['name']) ?> (<?= implode(', ', $scale['points']) ?>)
                            </option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                </div>

                <div class="admin-form-group mt-md">
                    <label class="admin-form-label">Klasser (lämna tomt för alla)</label>
                    <div class="checkbox-grid">
                        <?php foreach ($allClasses as $class): ?>
                        <label class="checkbox-chip">
                            <input type="checkbox" name="stage_bonus_class_ids[]" value="<?= $class['id'] ?>"
                                   <?= in_array($class['id'], $stageBonusClassIds ?: []) ? 'checked' : '' ?>>
                            <?= htmlspecialchars($class['display_name']) ?>
                        </label>
                        <?php endforeach; ?>
                    </div>
                </div>

                <div class="alert alert-info mt-md text-sm">
                    <i data-lucide="info" class="icon-sm"></i>
                    <span>Bonuspoängen läggs automatiskt till när resultat importeras till ett event i denna serie.</span>
                </div>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <!-- Stats (only for existing series) -->
    <?php if (!$isNew): ?>
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
                Statistik
            </h2>
        </div>
        <div class="admin-card-body">
            <div class="grid grid-stats grid-gap-md">
                <div class="admin-stat-card">
                    <div class="admin-stat-content">
                        <div class="admin-stat-value"><?= $eventsCount ?></div>
                        <div class="admin-stat-label">Events</div>
                    </div>
                </div>
                <div class="admin-stat-card">
                    <div class="admin-stat-content">
                        <div class="admin-stat-value"><?= htmlspecialchars($series['year'] ?? '-') ?></div>
                        <div class="admin-stat-label">År</div>
                    </div>
                </div>
            </div>

            <div class="mt-lg">
                <a href="/admin/events?series_id=<?= $id ?>" class="btn-admin btn-admin-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>
                    Visa events i denna serie
                </a>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <!-- Actions -->
    <div class="admin-card">
        <div class="admin-card-body">
            <div class="flex items-center justify-between flex-wrap gap-md">
                <div class="flex gap-sm">
                    <a href="/admin/series" class="btn-admin btn-admin-secondary">Avbryt</a>
                    <button type="submit" class="btn-admin btn-admin-primary">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                        <?= $isNew ? 'Skapa Serie' : 'Spara Ändringar' ?>
                    </button>
                </div>

                <?php if (!$isNew): ?>
                <button type="button" onclick="deleteSeries(<?= $id ?>, '<?= addslashes($series['name']) ?>')"
                        class="btn-admin btn-admin-danger">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                    Ta bort serie
                </button>
                <?php endif; ?>
            </div>
        </div>
    </div>
</form>
<?php endif; // End INFO TAB ?>

<?php if ($currentTab === 'events' && !$isNew): ?>
<!-- EVENTS TAB -->
<?php
require_once __DIR__ . '/../includes/series-points.php';

// AUTO-SYNC: Add events locked to this series to series_events table
$lockedEvents = $db->getAll("
    SELECT e.id, e.date
    FROM events e
    WHERE e.series_id = ?
    AND e.id NOT IN (SELECT event_id FROM series_events WHERE series_id = ?)
", [$id, $id]);

foreach ($lockedEvents as $ev) {
    $existingCount = $db->getRow("SELECT COUNT(*) as cnt FROM series_events WHERE series_id = ?", [$id]);
    $db->insert('series_events', [
        'series_id' => $id,
        'event_id' => $ev['id'],
        'template_id' => null,
        'sort_order' => ($existingCount['cnt'] ?? 0) + 1
    ]);
}

// Re-sort all events by date
if (!empty($lockedEvents)) {
    $allSeriesEvents = $db->getAll("
        SELECT se.id, e.date
        FROM series_events se
        JOIN events e ON se.event_id = e.id
        WHERE se.series_id = ?
        ORDER BY e.date ASC
    ", [$id]);
    $sortOrder = 1;
    foreach ($allSeriesEvents as $se) {
        $db->update('series_events', ['sort_order' => $sortOrder], 'id = ?', [$se['id']]);
        $sortOrder++;
    }
}

// Handle events tab form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'add_event') {
        $eventId = intval($_POST['event_id']);
        $templateId = !empty($_POST['template_id']) ? intval($_POST['template_id']) : null;
        $existing = $db->getRow("SELECT id FROM series_events WHERE series_id = ? AND event_id = ?", [$id, $eventId]);
        if (!$existing) {
            $maxOrder = $db->getRow("SELECT MAX(sort_order) as max_order FROM series_events WHERE series_id = ?", [$id]);
            $db->insert('series_events', [
                'series_id' => $id,
                'event_id' => $eventId,
                'template_id' => $templateId,
                'sort_order' => ($maxOrder['max_order'] ?? 0) + 1
            ]);
            $event = $db->getRow("SELECT series_id FROM events WHERE id = ?", [$eventId]);
            if (empty($event['series_id'])) {
                $db->update('events', ['series_id' => $id], 'id = ?', [$eventId]);
            }
            if ($templateId) {
                recalculateSeriesEventPoints($db, $id, $eventId);
            }
        }
        header("Location: /admin/series/edit/{$id}?tab=events&saved=1");
        exit;
    } elseif ($action === 'update_template') {
        $seriesEventId = intval($_POST['series_event_id']);
        $templateId = !empty($_POST['template_id']) ? intval($_POST['template_id']) : null;
        $seriesEvent = $db->getRow("SELECT event_id FROM series_events WHERE id = ? AND series_id = ?", [$seriesEventId, $id]);
        if ($seriesEvent) {
            $db->update('series_events', ['template_id' => $templateId], 'id = ? AND series_id = ?', [$seriesEventId, $id]);
            recalculateSeriesEventPoints($db, $id, $seriesEvent['event_id']);
        }
        header("Location: /admin/series/edit/{$id}?tab=events&saved=1");
        exit;
    } elseif ($action === 'remove_event') {
        $seriesEventId = intval($_POST['series_event_id']);
        $seriesEvent = $db->getRow("SELECT event_id FROM series_events WHERE id = ? AND series_id = ?", [$seriesEventId, $id]);
        $db->delete('series_events', 'id = ? AND series_id = ?', [$seriesEventId, $id]);
        if ($seriesEvent) {
            $db->query("UPDATE events SET series_id = NULL WHERE id = ? AND series_id = ?", [$seriesEvent['event_id'], $id]);
        }
        header("Location: /admin/series/edit/{$id}?tab=events&saved=1");
        exit;
    } elseif ($action === 'update_count_best') {
        $countBest = $_POST['count_best_results'];
        $countBestValue = ($countBest === '' || $countBest === 'null') ? null : intval($countBest);
        $db->update('series', ['count_best_results' => $countBestValue], 'id = ?', [$id]);
        $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);
        header("Location: /admin/series/edit/{$id}?tab=events&saved=1");
        exit;
    } elseif ($action === 'recalculate_all') {
        recalculateAllSeriesPoints($db, $id);
        header("Location: /admin/series/edit/{$id}?tab=events&saved=1");
        exit;
    }
}

// Get events in this series
$seriesEvents = $db->getAll("
    SELECT se.*, e.name as event_name, e.date as event_date, e.location, e.discipline,
           e.series_id as event_series_id, e.active as event_active,
           ps.name as template_name
    FROM series_events se
    JOIN events e ON se.event_id = e.id
    LEFT JOIN point_scales ps ON se.template_id = ps.id
    WHERE se.series_id = ?
    ORDER BY e.date ASC
", [$id]);

// Get events not in this series (for adding)
$seriesYear = $series['year'] ?? null;
$eventsNotInSeries = $db->getAll("
    SELECT e.id, e.name, e.date, e.location, YEAR(e.date) as event_year
    FROM events e
    WHERE e.id NOT IN (SELECT event_id FROM series_events WHERE series_id = ?)
    AND e.active = 1
    ORDER BY e.date DESC
", [$id]);

$matchingYearEvents = [];
$otherYearEvents = [];
foreach ($eventsNotInSeries as $ev) {
    if ($seriesYear && $ev['event_year'] == $seriesYear) {
        $matchingYearEvents[] = $ev;
    } else {
        $otherYearEvents[] = $ev;
    }
}

// Get all point scales
$templates = $db->getAll("SELECT id, name FROM point_scales WHERE active = 1 ORDER BY name");
?>

<?php if (isset($_GET['saved'])): ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i> Ändringarna har sparats!
</div>
<?php endif; ?>

<div class="grid grid-cols-1 gs-lg-grid-cols-3 gap-lg">
    <!-- Left Column: Settings -->
    <div>
        <!-- Count Best Results -->
        <div class="admin-card mb-lg">
            <div class="admin-card-header">
                <h2><i data-lucide="calculator"></i> Poängräkning</h2>
            </div>
            <div class="admin-card-body">
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="update_count_best">
                    <div class="admin-form-group">
                        <label class="admin-form-label">Räkna bästa resultat</label>
                        <select name="count_best_results" class="admin-form-select" onchange="this.form.submit()">
                            <option value="null" <?= ($series['count_best_results'] ?? null) === null ? 'selected' : '' ?>>Alla resultat</option>
                            <?php for ($i = 1; $i <= 10; $i++): ?>
                            <option value="<?= $i ?>" <?= ($series['count_best_results'] ?? null) == $i ? 'selected' : '' ?>>
                                Bästa <?= $i ?> av <?= count($seriesEvents) ?>
                            </option>
                            <?php endfor; ?>
                        </select>
                        <small class="text-secondary text-xs">Övriga resultat visas med överstrykning</small>
                    </div>
                </form>
            </div>
        </div>

        <!-- Add Event -->
        <div class="admin-card">
            <div class="admin-card-header">
                <h2><i data-lucide="plus"></i> Lägg till Event</h2>
            </div>
            <div class="admin-card-body">
                <?php if (empty($eventsNotInSeries)): ?>
                <p class="text-secondary text-sm">Alla events är redan tillagda.</p>
                <?php else: ?>
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="add_event">
                    <div class="admin-form-group">
                        <label class="admin-form-label">Event</label>
                        <select name="event_id" class="admin-form-select" required>
                            <option value="">-- Välj event --</option>
                            <?php if (!empty($matchingYearEvents)): ?>
                            <optgroup label="Matchar serieåret (<?= $seriesYear ?>)">
                                <?php foreach ($matchingYearEvents as $event): ?>
                                <option value="<?= $event['id'] ?>">
                                    <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
                                </option>
                                <?php endforeach; ?>
                            </optgroup>
                            <?php endif; ?>
                            <?php if (!empty($otherYearEvents)): ?>
                            <optgroup label="Andra år">
                                <?php foreach ($otherYearEvents as $event): ?>
                                <option value="<?= $event['id'] ?>">
                                    <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
                                </option>
                                <?php endforeach; ?>
                            </optgroup>
                            <?php endif; ?>
                        </select>
                    </div>
                    <div class="admin-form-group">
                        <label class="admin-form-label">Poängmall</label>
                        <select name="template_id" class="admin-form-select">
                            <option value="">-- Ingen mall --</option>
                            <?php foreach ($templates as $template): ?>
                            <option value="<?= $template['id'] ?>"><?= h($template['name']) ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <button type="submit" class="btn-admin btn-admin-primary w-full">
                        <i data-lucide="plus"></i> Lägg till
                    </button>
                </form>
                <?php endif; ?>
            </div>
        </div>
    </div>

    <!-- Right Column: Events List -->
    <div class="gs-lg-col-span-2">
        <div class="admin-card">
            <div class="admin-card-header flex items-center justify-between">
                <h2><i data-lucide="list"></i> Events i serien (<?= count($seriesEvents) ?>)</h2>
                <form method="POST" class="inline">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="recalculate_all">
                    <button type="submit" class="btn-admin btn-admin-secondary btn-admin-sm" onclick="return confirm('Beräkna om alla seriepoäng?')">
                        <i data-lucide="refresh-cw"></i> Beräkna om poäng
                    </button>
                </form>
            </div>
            <div class="admin-card-body">
                <?php if (empty($seriesEvents)): ?>
                <p class="text-secondary">Inga events i serien än.</p>
                <?php else: ?>
                <div class="admin-table-container">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Event</th>
                                <th>Datum</th>
                                <th>Status</th>
                                <th>Poängmall</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php $eventNum = 1; foreach ($seriesEvents as $se): ?>
                            <tr>
                                <td><span class="badge badge-primary">#<?= $eventNum ?></span></td>
                                <td>
                                    <strong><?= h($se['event_name']) ?></strong>
                                    <?php if ($se['event_series_id'] == $id): ?>
                                    <span class="badge badge-success badge-sm"><i data-lucide="lock" style="width:10px;height:10px;"></i></span>
                                    <?php endif; ?>
                                </td>
                                <td><?= $se['event_date'] ? date('Y-m-d', strtotime($se['event_date'])) : '-' ?></td>
                                <td>
                                    <?php if ($se['event_active']): ?>
                                    <span class="badge badge-success">Aktiv</span>
                                    <?php else: ?>
                                    <span class="badge badge-warning">Inaktiv</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <form method="POST" class="flex gap-xs">
                                        <?= csrf_field() ?>
                                        <input type="hidden" name="action" value="update_template">
                                        <input type="hidden" name="series_event_id" value="<?= $se['id'] ?>">
                                        <select name="template_id" class="admin-form-select admin-form-select-sm" style="min-width:120px;">
                                            <option value="">-- Ingen --</option>
                                            <?php foreach ($templates as $template): ?>
                                            <option value="<?= $template['id'] ?>" <?= $se['template_id'] == $template['id'] ? 'selected' : '' ?>>
                                                <?= h($template['name']) ?>
                                            </option>
                                            <?php endforeach; ?>
                                        </select>
                                        <button type="submit" class="btn-admin btn-admin-primary btn-admin-sm" title="Spara">
                                            <i data-lucide="save"></i>
                                        </button>
                                    </form>
                                </td>
                                <td>
                                    <div class="flex gap-xs">
                                        <a href="/admin/event-edit.php?id=<?= $se['event_id'] ?>" class="btn-admin btn-admin-secondary btn-admin-sm" title="Redigera event">
                                            <i data-lucide="pencil"></i>
                                        </a>
                                        <form method="POST" class="inline" onsubmit="return confirm('Ta bort från serien?')">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="remove_event">
                                            <input type="hidden" name="series_event_id" value="<?= $se['id'] ?>">
                                            <button type="submit" class="btn-admin btn-admin-danger btn-admin-sm" title="Ta bort">
                                                <i data-lucide="trash-2"></i>
                                            </button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                            <?php $eventNum++; endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</div>
<?php endif; // End EVENTS TAB ?>

<?php if ($currentTab === 'rules' && !$isNew): ?>
<!-- RULES TAB -->
<?php
// Event classes
$eventClasses = [
    'national' => ['name' => 'Nationellt', 'desc' => 'Nationella tävlingar med full rankingpoäng och strikta licensregler', 'icon' => 'trophy', 'color' => 'warning'],
    'sportmotion' => ['name' => 'Sportmotion', 'desc' => 'Sportmotion-event med 50% rankingpoäng', 'icon' => 'bike', 'color' => 'info'],
    'motion' => ['name' => 'Motion', 'desc' => 'Motion-event utan rankingpoäng, öppet för alla', 'icon' => 'heart', 'color' => 'success']
];

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['event_class'])) {
    checkCsrf();
    $eventClass = $_POST['event_class'] ?? '';
    if (array_key_exists($eventClass, $eventClasses)) {
        $db->update('series', ['event_license_class' => $eventClass], 'id = ?', [$id]);
        $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);
        header("Location: /admin/series/edit/{$id}?tab=rules&saved=1");
        exit;
    }
}
?>

<?php if (isset($_GET['saved'])): ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i> Ändringarna har sparats!
</div>
<?php endif; ?>

<!-- Event Class Selection -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2><i data-lucide="shield"></i> Eventklass för <?= h($series['name']) ?></h2>
    </div>
    <div class="admin-card-body">
        <p class="text-secondary mb-lg">
            Välj vilken eventklass som gäller för serien. Detta styr vilka licenstyper som får anmäla sig.
        </p>

        <form method="POST">
            <?= csrf_field() ?>
            <div class="grid gap-md" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
                <?php foreach ($eventClasses as $key => $info):
                    $isSelected = ($series['event_license_class'] ?? '') === $key;
                ?>
                <label class="admin-card" style="cursor: pointer; border: 2px solid <?= $isSelected ? 'var(--color-accent)' : 'var(--color-border)' ?>; background: <?= $isSelected ? 'var(--color-accent-light)' : 'var(--color-bg-surface)' ?>;">
                    <div class="admin-card-body">
                        <div class="flex gap-md items-start">
                            <input type="radio" name="event_class" value="<?= $key ?>" <?= $isSelected ? 'checked' : '' ?> style="margin-top: 4px;">
                            <div>
                                <div class="flex items-center gap-sm mb-xs">
                                    <i data-lucide="<?= $info['icon'] ?>" style="width: 20px; height: 20px;"></i>
                                    <strong style="font-size: 1.1rem;"><?= h($info['name']) ?></strong>
                                </div>
                                <p class="text-secondary text-sm" style="margin: 0;"><?= h($info['desc']) ?></p>
                            </div>
                        </div>
                    </div>
                </label>
                <?php endforeach; ?>
            </div>

            <div class="mt-lg">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="save"></i> Spara eventklass
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Link to License Matrix -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="grid-3x3"></i> Licensregler</h2>
    </div>
    <div class="admin-card-body">
        <p class="text-secondary mb-lg">
            Licensreglerna (vilka licenstyper som får anmäla sig till vilka klasser) hanteras i
            <strong>Licens-Klass Matrisen</strong>. Samma regler gäller för alla serier med samma eventklass.
        </p>
        <?php $currentClass = $series['event_license_class'] ?? 'sportmotion'; ?>
        <a href="/admin/license-class-matrix.php?tab=<?= h($currentClass) ?>" class="btn-admin btn-admin-secondary">
            <i data-lucide="external-link"></i>
            Öppna Licens-Klass Matris (<?= h($eventClasses[$currentClass]['name'] ?? 'Sportmotion') ?>)
        </a>
    </div>
</div>
<?php endif; // End RULES TAB ?>

<script>
const csrfToken = '<?= htmlspecialchars(generate_csrf_token()) ?>';
const currentStatus = '<?= htmlspecialchars($series['status'] ?? 'planning') ?>';
const isNewSeries = <?= $isNew ? 'true' : 'false' ?>;

// Auto-generate series name from brand (without year - year shown as badge)
function updateSeriesName() {
    if (!isNewSeries) return; // Only auto-update for new series

    const brandSelect = document.getElementById('brand_id');
    const nameInput = document.getElementById('name');

    if (!brandSelect || !nameInput) return;

    const selectedOption = brandSelect.options[brandSelect.selectedIndex];
    const brandName = selectedOption?.dataset?.name || '';

    if (brandName) {
        nameInput.value = brandName;
    }
}

// Handle form submission - check if status changed to completed
document.querySelector('form').addEventListener('submit', function(e) {
    const statusSelect = document.getElementById('status');
    const newStatus = statusSelect.value;
    const calculateChampionsField = document.getElementById('calculate_champions');

    // Only show dialog if status is being changed TO completed (wasn't before)
    if (newStatus === 'completed' && currentStatus !== 'completed') {
        e.preventDefault();

        // Show confirmation dialog
        const confirmCalc = confirm(
            'Du markerar serien som AVSLUTAD.\n\n' +
            'Vill du räkna seriemästare nu?\n\n' +
            'OBS: Se till att ALLA resultat är importerade innan du bekräftar!\n\n' +
            'Klicka OK för att beräkna mästare, eller Avbryt för att bara spara status.'
        );

        calculateChampionsField.value = confirmCalc ? '1' : '0';

        // Submit the form
        this.submit();
    }
});

function toggleStageBonusConfig(enabled) {
    document.getElementById('stage-bonus-config').style.display = enabled ? '' : 'none';
}

<?php if (!$isNew): ?>
function deleteSeries(id, name) {
    if (!confirm('Är du säker på att du vill ta bort "' + name + '"?\n\nDetta kan inte ångras.')) {
        return;
    }

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/admin/series';
    form.innerHTML = '<input type="hidden" name="action" value="delete">' +
                     '<input type="hidden" name="id" value="' + id + '">' +
                     '<input type="hidden" name="csrf_token" value="' + csrfToken + '">';
    document.body.appendChild(form);
    form.submit();
}
<?php endif; ?>
</script>

<style>
.admin-form-textarea {
    width: 100%;
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-bg);
    color: var(--color-text);
    font-family: inherit;
    font-size: var(--text-sm);
    resize: vertical;
}

.admin-form-textarea:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px var(--color-accent-alpha);
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    cursor: pointer;
}
.checkbox-label input {
    width: 18px;
    height: 18px;
}
.checkbox-grid {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-xs);
    padding: var(--space-sm);
    background: var(--color-bg-surface, #f8f9fa);
    border-radius: var(--radius-md);
    max-height: 200px;
    overflow-y: auto;
}

/* Mobile adjustments */
@media (max-width: 600px) {
    .admin-form-row {
        flex-direction: column;
    }

    .admin-card-body > div[style*="display: flex"] {
        flex-direction: column;
        align-items: stretch !important;
    }

    .admin-card-body > div[style*="display: flex"] > div {
        width: 100%;
    }
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
