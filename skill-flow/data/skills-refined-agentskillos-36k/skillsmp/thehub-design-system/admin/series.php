<?php
/**
 * Admin Series - V3 Design System
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;
$db = getDB();

// Check if user is promotor only (not admin)
$isPromotorOnly = isRole('promotor') && !hasRole('admin');
$currentUserId = $_SESSION['admin_id'] ?? 0;

// Check if promotor_series table exists
$promotorSeriesTableExists = false;
try {
    $tables = $db->getAll("SHOW TABLES LIKE 'promotor_series'");
    $promotorSeriesTableExists = !empty($tables);
} catch (Exception $e) {}

// Initialize message variables
$message = '';
$messageType = 'info';

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'create' || $action === 'update') {
        // Validate required fields
        $name = trim($_POST['name'] ?? '');

        if (empty($name)) {
            $message = 'Namn är obligatoriskt';
            $messageType = 'error';
        } else {
            // Handle logo upload
            $logoPath = null;
            if (isset($_FILES['logo']) && $_FILES['logo']['error'] === UPLOAD_ERR_OK) {
                $uploadDir = __DIR__ . '/../uploads/series/';
                if (!is_dir($uploadDir)) {
                    mkdir($uploadDir, 0755, true);
                }

                $fileExtension = strtolower(pathinfo($_FILES['logo']['name'], PATHINFO_EXTENSION));
                $allowedExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'];

                if (in_array($fileExtension, $allowedExtensions)) {
                    $fileName = uniqid('series_') . '.' . $fileExtension;
                    $targetPath = $uploadDir . $fileName;

                    if (move_uploaded_file($_FILES['logo']['tmp_name'], $targetPath)) {
                        $logoPath = '/uploads/series/' . $fileName;
                    }
                }
            }

            // Prepare series data
            $seriesData = [
                'name' => $name,
                'type' => trim($_POST['type'] ?? ''),
                'status' => $_POST['status'] ?? 'planning',
                'start_date' => !empty($_POST['start_date']) ? trim($_POST['start_date']) : null,
                'end_date' => !empty($_POST['end_date']) ? trim($_POST['end_date']) : null,
                'description' => trim($_POST['description'] ?? ''),
                'organizer' => trim($_POST['organizer'] ?? ''),
            ];

            // Only add format if column exists
            $formatColumnExists = false;
            try {
                $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");
                $formatColumnExists = !empty($columns);
            } catch (Exception $e) {}

            if ($formatColumnExists) {
                $seriesData['format'] = $_POST['format'] ?? 'Championship';
            }

            // Add logo path if uploaded
            if ($logoPath) {
                $seriesData['logo'] = $logoPath;
            }

            try {
                if ($action === 'create') {
                    $db->insert('series', $seriesData);
                    $message = 'Serie skapad!';
                    $messageType = 'success';
                } else {
                    $id = intval($_POST['id']);
                    $db->update('series', $seriesData, 'id = ?', [$id]);
                    $message = 'Serie uppdaterad!';
                    $messageType = 'success';
                }
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'delete') {
        $id = intval($_POST['id']);
        try {
            $db->delete('series', 'id = ?', [$id]);
            $message = 'Serie borttagen!';
            $messageType = 'success';
        } catch (Exception $e) {
            $message = 'Ett fel uppstod: ' . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Redirect old edit URLs to new edit page
if (isset($_GET['edit']) && is_numeric($_GET['edit'])) {
    header('Location: /admin/series/edit/' . intval($_GET['edit']));
    exit;
}

// Get filter parameters
$filterYear = isset($_GET['year']) && is_numeric($_GET['year']) ? intval($_GET['year']) : null;
$filterBrand = isset($_GET['brand']) && is_numeric($_GET['brand']) ? intval($_GET['brand']) : null;

// Check if year column exists on series table
$yearColumnExists = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'year'");
    $yearColumnExists = !empty($columns);
} catch (Exception $e) {}

// Build WHERE clause - use series.year column if available, fallback to YEAR(start_date)
$where = [];
$params = [];

if ($filterYear) {
    if ($yearColumnExists) {
        // Use COALESCE to prefer series.year, fallback to YEAR(start_date)
        $where[] = "COALESCE(year, YEAR(start_date)) = ?";
    } else {
        $where[] = "YEAR(start_date) = ?";
    }
    $params[] = $filterYear;
}

if ($filterBrand) {
    $where[] = "brand_id = ?";
    $params[] = $filterBrand;
}

$whereClause = !empty($where) ? 'WHERE ' . implode(' AND ', $where) : '';

// Check if format column exists
$formatColumnExists = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");
    $formatColumnExists = !empty($columns);
} catch (Exception $e) {
    // Column doesn't exist, that's ok
}

// Check if series_events table exists
$seriesEventsTableExists = false;
try {
    $tables = $db->getAll("SHOW TABLES LIKE 'series_events'");
    $seriesEventsTableExists = !empty($tables);
} catch (Exception $e) {
    // Table doesn't exist, that's ok
}

// Check if brand_id column exists
$brandColumnExists = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'brand_id'");
    $brandColumnExists = !empty($columns);
} catch (Exception $e) {}

// Get series from database with brand info
$formatSelect = $formatColumnExists ? ', s.format' : ', "Championship" as format';
$yearSelect = $yearColumnExists ? ', s.year' : ', NULL as year';
$eventsCountSelect = $seriesEventsTableExists
    ? '(SELECT COUNT(*) FROM series_events WHERE series_id = s.id)'
    : '0';
// Count events that have at least one result
$eventsWithResultsSelect = $seriesEventsTableExists
    ? '(SELECT COUNT(DISTINCT se2.event_id) FROM series_events se2
        INNER JOIN results r ON r.event_id = se2.event_id
        WHERE se2.series_id = s.id AND r.status = "finished")'
    : '0';
$brandSelect = $brandColumnExists ? ', s.brand_id, sb.name as brand_name, sb.logo as brand_logo' : ', NULL as brand_id, NULL as brand_name, NULL as brand_logo';
$brandJoin = $brandColumnExists ? 'LEFT JOIN series_brands sb ON s.brand_id = sb.id' : '';

// Rebuild where clause for aliased table
$whereAliased = str_replace(['year', 'start_date', 'brand_id'], ['s.year', 's.start_date', 's.brand_id'], $whereClause);

// Add promotor filtering - only show series they have access to
$promotorJoin = '';
$promotorWhere = '';
if ($isPromotorOnly && $promotorSeriesTableExists && $currentUserId > 0) {
    $promotorJoin = "INNER JOIN promotor_series ps ON s.id = ps.series_id AND ps.user_id = " . intval($currentUserId);
}

$sql = "SELECT s.id, s.name, s.type{$formatSelect}{$yearSelect}, s.status, s.start_date, s.end_date, s.logo, s.organizer,
    {$eventsCountSelect} as events_count,
    {$eventsWithResultsSelect} as events_with_results{$brandSelect}
    FROM series s
    {$brandJoin}
    {$promotorJoin}
    {$whereAliased}
    ORDER BY sb.name ASC, s.year DESC, s.start_date DESC";

$series = $db->getAll($sql, $params);

// Get all years from series - use series.year column if available
if ($yearColumnExists) {
    $allYears = $db->getAll("SELECT DISTINCT COALESCE(year, YEAR(start_date)) as year FROM series WHERE year IS NOT NULL OR start_date IS NOT NULL ORDER BY year DESC");
} else {
    $allYears = $db->getAll("SELECT DISTINCT YEAR(start_date) as year FROM series WHERE start_date IS NOT NULL ORDER BY year DESC");
}

// Get all brands for filter
$allBrands = [];
if ($brandColumnExists) {
    $allBrands = $db->getAll("SELECT id, name FROM series_brands ORDER BY name ASC");
}

// Count unique participants in active series
$uniqueParticipants = 0;
if ($seriesEventsTableExists) {
    $participantCount = $db->getRow("
        SELECT COUNT(DISTINCT r.cyclist_id) as unique_riders
        FROM results r
        INNER JOIN series_events se ON r.event_id = se.event_id
        INNER JOIN series s ON se.series_id = s.id
        WHERE s.status = 'active'
    ");
    $uniqueParticipants = $participantCount['unique_riders'] ?? 0;
}

// Page config
$page_title = 'Serier';
$page_group = 'standings';

// Promotors can't create new series or manage brands - only edit their assigned series
if ($isPromotorOnly) {
    $page_actions = ''; // No actions for promotors
} else {
    $page_actions = '<a href="/admin/series/brands" class="btn-admin btn-admin-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
        Varumärken
    </a>
    <a href="/admin/series/edit?new=1" class="btn-admin btn-admin-primary">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
        Ny Serie
    </a>';
}

// Include unified layout (uses same layout as public site)
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

<!-- Stats Grid -->
<div class="grid grid-stats grid-gap-md">
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-info-light); color: var(--color-info);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= count($series) ?></div>
            <div class="admin-stat-label">Totalt serier</div>
        </div>
    </div>

    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-success-light); color: var(--color-success);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= count(array_filter($series, fn($s) => $s['status'] === 'active')) ?></div>
            <div class="admin-stat-label">Aktiva</div>
        </div>
    </div>

    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-accent-light); color: var(--color-accent);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= array_sum(array_column($series, 'events_count')) ?></div>
            <div class="admin-stat-label">Totalt events</div>
        </div>
    </div>

    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-warning-light); color: var(--color-warning);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= number_format($uniqueParticipants, 0, ',', ' ') ?></div>
            <div class="admin-stat-label">Unika deltagare</div>
        </div>
    </div>
</div>

<!-- Filter Section -->
<div class="admin-card">
    <div class="admin-card-body">
        <form method="GET" action="/admin/series" class="admin-form-row" style="display: flex; gap: var(--space-md); flex-wrap: wrap; align-items: flex-end;">
            <?php if (!empty($allBrands)): ?>
            <div class="admin-form-group" style="margin-bottom: 0; min-width: 200px;">
                <label for="brand-filter" class="admin-form-label">Huvudserie</label>
                <select id="brand-filter" name="brand" class="admin-form-select" onchange="this.form.submit()">
                    <option value="">Alla serier</option>
                    <?php foreach ($allBrands as $brand): ?>
                        <option value="<?= $brand['id'] ?>" <?= $filterBrand == $brand['id'] ? 'selected' : '' ?>>
                            <?= htmlspecialchars($brand['name']) ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <?php endif; ?>
            <div class="admin-form-group" style="margin-bottom: 0; min-width: 120px;">
                <label for="year-filter" class="admin-form-label">År</label>
                <select id="year-filter" name="year" class="admin-form-select" onchange="this.form.submit()">
                    <option value="">Alla år</option>
                    <?php foreach ($allYears as $yearRow): ?>
                        <option value="<?= $yearRow['year'] ?>" <?= $filterYear == $yearRow['year'] ? 'selected' : '' ?>>
                            <?= $yearRow['year'] ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>
        </form>

        <?php if ($filterYear || $filterBrand): ?>
            <div style="margin-top: var(--space-md); padding-top: var(--space-md); border-top: 1px solid var(--color-border); display: flex; align-items: center; gap: var(--space-sm); flex-wrap: wrap;">
                <span style="font-size: var(--text-sm); color: var(--color-text-secondary);">Visar:</span>
                <?php if ($filterBrand): ?>
                    <?php
                    $brandName = '';
                    foreach ($allBrands as $b) {
                        if ($b['id'] == $filterBrand) {
                            $brandName = $b['name'];
                            break;
                        }
                    }
                    ?>
                    <span class="admin-badge admin-badge-info"><?= htmlspecialchars($brandName) ?></span>
                <?php endif; ?>
                <?php if ($filterYear): ?>
                    <span class="admin-badge admin-badge-warning"><?= $filterYear ?></span>
                <?php endif; ?>
                <a href="/admin/series" class="btn-admin btn-admin-sm btn-admin-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                    Visa alla
                </a>
            </div>
        <?php endif; ?>
    </div>
</div>

<!-- Series Table -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><?= count($series) ?> serier</h2>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <?php if (empty($series)): ?>
            <div class="admin-empty-state">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                <h3>Inga serier hittades</h3>
                <p>Prova att ändra filtren eller skapa en ny serie.</p>
                <a href="/admin/series/edit?new=1" class="btn-admin btn-admin-primary">Skapa serie</a>
            </div>
        <?php else: ?>
            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Huvudserie</th>
                            <th>Säsong</th>
                            <th>År</th>
                            <th>Status</th>
                            <th>Resultat</th>
                            <th style="width: 150px;">Åtgärder</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($series as $serie): ?>
                            <?php
                            $statusMap = [
                                'planning' => ['class' => 'admin-badge-secondary', 'text' => 'Planering'],
                                'active' => ['class' => 'admin-badge-success', 'text' => 'Aktiv'],
                                'completed' => ['class' => 'admin-badge-info', 'text' => 'Avslutad'],
                                'cancelled' => ['class' => 'admin-badge-secondary', 'text' => 'Inställd']
                            ];
                            $statusInfo = $statusMap[$serie['status']] ?? ['class' => 'admin-badge-secondary', 'text' => ucfirst($serie['status'])];
                            ?>
                            <tr>
                                <td>
                                    <?php if (!empty($serie['brand_name'])): ?>
                                        <div style="display: flex; align-items: center; gap: var(--space-sm);">
                                            <?php if (!empty($serie['brand_logo'])): ?>
                                                <img src="<?= htmlspecialchars($serie['brand_logo']) ?>" alt="" style="max-width: 32px; max-height: 32px; object-fit: contain;">
                                            <?php endif; ?>
                                            <span style="font-weight: 500; color: var(--color-text);">
                                                <?= htmlspecialchars($serie['brand_name']) ?>
                                            </span>
                                        </div>
                                    <?php else: ?>
                                        <span style="color: var(--color-text-secondary); font-style: italic;">
                                            Ingen huvudserie
                                        </span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <a href="/admin/series/edit/<?= $serie['id'] ?>" style="color: var(--color-accent); text-decoration: none; font-weight: 500;">
                                        <?= htmlspecialchars($serie['name']) ?>
                                    </a>
                                    <?php if (!empty($serie['type'])): ?>
                                        <br><span style="font-size: 0.75rem; color: var(--color-text-secondary);"><?= htmlspecialchars($serie['type']) ?></span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if (!empty($serie['year'])): ?>
                                        <span class="admin-badge admin-badge-info"><?= $serie['year'] ?></span>
                                    <?php else: ?>
                                        <span style="color: var(--color-warning);">Saknas!</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php
                                    $eventsCount = (int)$serie['events_count'];
                                    $eventsWithResults = (int)$serie['events_with_results'];
                                    $allHaveResults = $eventsCount > 0 && $eventsWithResults >= $eventsCount;
                                    $isNotCompleted = $serie['status'] !== 'completed';
                                    $readyToComplete = $allHaveResults && $isNotCompleted;
                                    ?>
                                    <?php if ($readyToComplete): ?>
                                        <span class="admin-badge admin-badge-warning" title="Alla events har resultat - redo att avsluta!">
                                            Redo att avsluta
                                        </span>
                                    <?php else: ?>
                                        <span class="admin-badge <?= $statusInfo['class'] ?>">
                                            <?= $statusInfo['text'] ?>
                                        </span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($eventsCount > 0): ?>
                                        <span class="admin-badge <?= $allHaveResults ? 'admin-badge-success' : 'admin-badge-secondary' ?>"
                                              title="<?= $eventsWithResults ?> av <?= $eventsCount ?> har resultat">
                                            <?= $eventsWithResults ?>/<?= $eventsCount ?>
                                        </span>
                                    <?php else: ?>
                                        <span class="admin-badge admin-badge-secondary">0</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <div class="table-actions">
                                        <a href="/admin/series/manage/<?= $serie['id'] ?>" class="btn-admin btn-admin-sm btn-admin-primary" title="Hantera serie">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
                                            Hantera
                                        </a>
                                        <?php if (!$isPromotorOnly): ?>
                                        <button onclick="deleteSeries(<?= $serie['id'] ?>, '<?= addslashes($serie['name']) ?>')" class="btn-admin btn-admin-sm btn-admin-danger" title="Ta bort">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                                        </button>
                                        <?php endif; ?>
                                    </div>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
</div>

<!-- Series Modal -->
<div id="seriesModal" class="admin-modal hidden">
    <div class="admin-modal-overlay" onclick="closeSeriesModal()"></div>
    <div class="admin-modal-content">
        <div class="admin-modal-header">
            <h2 id="modalTitle">Ny Serie</h2>
            <button type="button" class="admin-modal-close" onclick="closeSeriesModal()">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>
        </div>
        <form method="POST" id="seriesForm" enctype="multipart/form-data">
            <?= csrf_field() ?>
            <input type="hidden" name="action" id="formAction" value="create">
            <input type="hidden" name="id" id="seriesId" value="">

            <div class="admin-modal-body">
                <div class="admin-form-group">
                    <label for="name" class="admin-form-label">Namn <span style="color: var(--color-error);">*</span></label>
                    <input type="text" id="name" name="name" class="admin-form-input" required placeholder="T.ex. GravitySeries 2025">
                </div>

                <div class="admin-form-row">
                    <div class="admin-form-group">
                        <label for="type" class="admin-form-label">Typ</label>
                        <input type="text" id="type" name="type" class="admin-form-input" placeholder="T.ex. XC, Landsväg, MTB">
                    </div>
                    <div class="admin-form-group">
                        <label for="format" class="admin-form-label">Format</label>
                        <select id="format" name="format" class="admin-form-select">
                            <option value="Championship">Championship</option>
                            <option value="Team">Team</option>
                        </select>
                    </div>
                </div>

                <div class="admin-form-group">
                    <label for="status" class="admin-form-label">Status</label>
                    <select id="status" name="status" class="admin-form-select">
                        <option value="planning">Planering</option>
                        <option value="active">Aktiv</option>
                        <option value="completed">Avslutad</option>
                        <option value="cancelled">Inställd</option>
                    </select>
                </div>

                <div class="admin-form-row">
                    <div class="admin-form-group">
                        <label for="start_date" class="admin-form-label">Startdatum</label>
                        <input type="date" id="start_date" name="start_date" class="admin-form-input">
                    </div>
                    <div class="admin-form-group">
                        <label for="end_date" class="admin-form-label">Slutdatum</label>
                        <input type="date" id="end_date" name="end_date" class="admin-form-input">
                    </div>
                </div>

                <div class="admin-form-group">
                    <label for="organizer" class="admin-form-label">Arrangör</label>
                    <input type="text" id="organizer" name="organizer" class="admin-form-input" placeholder="T.ex. Svenska Cykelförbundet">
                </div>

                <div class="admin-form-group">
                    <label for="description" class="admin-form-label">Beskrivning</label>
                    <textarea id="description" name="description" class="admin-form-textarea" rows="3" placeholder="Beskriv serien..."></textarea>
                </div>

                <div class="admin-form-group">
                    <label for="logo" class="admin-form-label">Logotyp</label>
                    <input type="file" id="logo" name="logo" class="admin-form-input" accept="image/*">
                    <div id="currentLogo" style="display: none; margin-top: var(--space-sm);">
                        <strong>Nuvarande:</strong><br>
                        <img id="currentLogoImg" src="" alt="Logotyp" style="max-width: 150px; max-height: 80px; margin-top: var(--space-xs);">
                    </div>
                </div>
            </div>

            <div class="admin-modal-footer">
                <button type="button" class="btn-admin btn-admin-secondary" onclick="closeSeriesModal()">Avbryt</button>
                <button type="submit" class="btn-admin btn-admin-primary" id="submitButton">Skapa</button>
            </div>
        </form>
    </div>
</div>

<script>
// Store CSRF token from PHP session
const csrfToken = '<?= htmlspecialchars(generate_csrf_token()) ?>';

function openSeriesModal() {
    document.getElementById('seriesModal').style.display = 'flex';
    document.getElementById('seriesForm').reset();
    document.getElementById('formAction').value = 'create';
    document.getElementById('seriesId').value = '';
    document.getElementById('modalTitle').textContent = 'Ny Serie';
    document.getElementById('submitButton').textContent = 'Skapa';
    document.getElementById('currentLogo').style.display = 'none';
}

function closeSeriesModal() {
    document.getElementById('seriesModal').style.display = 'none';
}

function deleteSeries(id, name) {
    if (!confirm('Är du säker på att du vill ta bort "' + name + '"?')) {
        return;
    }

    const form = document.createElement('form');
    form.method = 'POST';
    form.innerHTML = '<input type="hidden" name="action" value="delete">' +
                     '<input type="hidden" name="id" value="' + id + '">' +
                     '<input type="hidden" name="csrf_token" value="' + csrfToken + '">';
    document.body.appendChild(form);
    form.submit();
}


// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeSeriesModal();
    }
});
</script>

<style>
/* Modal styles */
.admin-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.admin-modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
}

.admin-modal-content {
    position: relative;
    background: var(--color-bg);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xl);
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

/* Mobile: Fullscreen modal */
@media (max-width: 599px) {
    .admin-modal {
        padding: 0;
    }
    .admin-modal-content {
        width: 100%;
        max-width: 100%;
        height: 100%;
        max-height: 100%;
        border-radius: 0;
    }
    .admin-modal-header {
        padding-top: calc(var(--space-lg) + env(safe-area-inset-top, 0px));
    }
    .admin-modal-footer {
        padding-bottom: calc(var(--space-md) + env(safe-area-inset-bottom, 0px));
    }
    .admin-modal-close {
        min-width: 44px;
        min-height: 44px;
    }
}

.admin-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.admin-modal-header h2 {
    margin: 0;
    font-size: var(--text-xl);
}

.admin-modal-close {
    background: none;
    border: none;
    padding: var(--space-xs);
    cursor: pointer;
    color: var(--color-text-secondary);
    border-radius: var(--radius-sm);
}

.admin-modal-close:hover {
    background: var(--color-bg-tertiary);
    color: var(--color-text);
}

.admin-modal-close svg {
    width: 20px;
    height: 20px;
}

.admin-modal-body {
    padding: var(--space-lg);
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    flex: 1;
}

.admin-modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
    padding: var(--space-lg);
    border-top: 1px solid var(--color-border);
}

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
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
