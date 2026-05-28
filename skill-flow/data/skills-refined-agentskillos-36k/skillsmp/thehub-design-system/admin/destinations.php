<?php
/**
 * Destinations Admin Page
 *
 * Hantera destinations (venues) - platser dar event arrangeras.
 * - Lista alla destinations
 * - Hitta och sla samman dubbletter
 * - Skapa nya destinations
 * - Se statistik per destination
 *
 * @package TheHUB
 * @version 1.0
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Handle messages from URL
if (isset($_GET['msg'])) {
    switch ($_GET['msg']) {
        case 'created':
            $message = 'Destination skapad!';
            $messageType = 'success';
            break;
        case 'deleted':
            $message = 'Destination borttagen!';
            $messageType = 'success';
            break;
        case 'merged':
            $message = 'Destinations sammanslagen!';
            $messageType = 'success';
            break;
    }
}

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    // Quick create destination
    if ($action === 'quick_create') {
        $name = trim($_POST['name'] ?? '');
        $city = trim($_POST['city'] ?? '');

        if (empty($name)) {
            $message = 'Namn ar obligatoriskt';
            $messageType = 'error';
        } else {
            try {
                $db->insert('venues', [
                    'name' => $name,
                    'city' => $city ?: $name,
                    'country' => 'Sverige',
                    'active' => 1
                ]);
                $message = "Destination '$name' skapad!";
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }

    // Merge destinations
    if ($action === 'merge') {
        $keepId = (int)($_POST['keep_id'] ?? 0);
        $mergeId = (int)($_POST['merge_id'] ?? 0);

        if ($keepId <= 0 || $mergeId <= 0 || $keepId === $mergeId) {
            $message = 'Ogiltiga destinations for sammanslagning';
            $messageType = 'error';
        } else {
            try {
                // Move all events from merge to keep
                $db->query(
                    "UPDATE events SET venue_id = ? WHERE venue_id = ?",
                    [$keepId, $mergeId]
                );

                // Delete the merged destination
                $db->delete('venues', 'id = ?', [$mergeId]);

                $message = 'Destinations sammanslagen!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel vid sammanslagning: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Search/filter
$search = trim($_GET['search'] ?? '');
$showInactive = isset($_GET['inactive']);
$sortBy = $_GET['sort'] ?? 'events';

// Build query
$where = [];
$params = [];

if (!$showInactive) {
    $where[] = "v.active = 1";
}

if ($search) {
    $where[] = "(v.name LIKE ? OR v.city LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

$whereClause = $where ? 'WHERE ' . implode(' AND ', $where) : '';

// Order by
$orderClause = match($sortBy) {
    'name' => 'ORDER BY v.name ASC',
    'city' => 'ORDER BY v.city ASC, v.name ASC',
    'recent' => 'ORDER BY last_event DESC NULLS LAST, v.name ASC',
    default => 'ORDER BY event_count DESC, v.name ASC'
};

// Fetch destinations with event counts
$destinations = $db->getAll("
    SELECT
        v.*,
        COUNT(DISTINCT e.id) as event_count,
        MAX(e.date) as last_event,
        MIN(e.date) as first_event,
        GROUP_CONCAT(DISTINCT YEAR(e.date) ORDER BY YEAR(e.date) DESC SEPARATOR ', ') as years
    FROM venues v
    LEFT JOIN events e ON e.venue_id = v.id
    $whereClause
    GROUP BY v.id
    $orderClause
", $params);

// Count events without destinations
$eventsWithoutDestination = $db->getRow("
    SELECT COUNT(*) as count
    FROM events
    WHERE (venue_id IS NULL OR venue_id = 0)
      AND location IS NOT NULL
      AND location != ''
")['count'] ?? 0;

// Find potential duplicates (similar names)
$potentialDuplicates = $db->getAll("
    SELECT
        v1.id as id1, v1.name as name1,
        v2.id as id2, v2.name as name2,
        (SELECT COUNT(*) FROM events WHERE venue_id = v1.id) as count1,
        (SELECT COUNT(*) FROM events WHERE venue_id = v2.id) as count2
    FROM venues v1
    JOIN venues v2 ON v1.id < v2.id
    WHERE (
        SOUNDEX(v1.name) = SOUNDEX(v2.name)
        OR LOWER(v1.name) = LOWER(v2.name)
        OR LEVENSHTEIN(LOWER(v1.name), LOWER(v2.name)) <= 3
        OR v1.city = v2.city AND v1.city != ''
    )
    LIMIT 20
");

// Stats
$totalDestinations = count($destinations);
$totalEvents = array_sum(array_column($destinations, 'event_count'));
$destinationsWithoutRegion = count(array_filter($destinations, fn($d) => empty($d['region'])));

// Page config
$page_title = 'Destinations';
$breadcrumbs = [
    ['label' => 'Destinations']
];
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
    <div class="alert alert--<?= $messageType ?> mb-lg">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<!-- Stats Cards -->
<div class="grid grid-stats grid-gap-md mb-lg">
    <div class="card" style="background: var(--color-bg-hover);">
        <div class="card-body text-center">
            <div class="text-3xl font-bold text-accent"><?= $totalDestinations ?></div>
            <div class="text-sm text-secondary">Destinations</div>
        </div>
    </div>
    <div class="card" style="background: var(--color-bg-hover);">
        <div class="card-body text-center">
            <div class="text-3xl font-bold text-primary"><?= $totalEvents ?></div>
            <div class="text-sm text-secondary">Events</div>
        </div>
    </div>
    <div class="card" style="background: var(--color-bg-hover);">
        <div class="card-body text-center">
            <div class="text-3xl font-bold <?= $eventsWithoutDestination > 0 ? 'text-warning' : 'text-success' ?>"><?= $eventsWithoutDestination ?></div>
            <div class="text-sm text-secondary">Utan destination</div>
        </div>
    </div>
    <div class="card" style="background: var(--color-bg-hover);">
        <div class="card-body text-center">
            <div class="text-3xl font-bold <?= count($potentialDuplicates) > 0 ? 'text-warning' : 'text-success' ?>"><?= count($potentialDuplicates) ?></div>
            <div class="text-sm text-secondary">Potentiella dubbletter</div>
        </div>
    </div>
    <div class="card" style="background: var(--color-bg-hover);">
        <div class="card-body text-center">
            <div class="text-3xl font-bold <?= $destinationsWithoutRegion > 0 ? 'text-warning' : 'text-success' ?>"><?= $destinationsWithoutRegion ?></div>
            <div class="text-sm text-secondary">Saknar region</div>
        </div>
    </div>
</div>

<!-- Quick Actions -->
<div class="card mb-lg">
    <div class="card-header">
        <h2>
            <i data-lucide="zap"></i>
            Snabbatgarder
        </h2>
    </div>
    <div class="card-body">
        <div class="grid grid-2 grid-gap-lg">
            <!-- Quick Create -->
            <form method="POST" class="flex gap-sm items-end">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="quick_create">
                <div class="flex-1">
                    <label class="label">Snabbskapa destination</label>
                    <div class="flex gap-sm">
                        <input type="text" name="name" class="input" placeholder="Namn (t.ex. Jarvso Bergscykelpark)" required>
                        <input type="text" name="city" class="input" placeholder="Stad (valfritt)" style="width: 150px;">
                        <button type="submit" class="btn btn--primary">
                            <i data-lucide="plus"></i>
                            Skapa
                        </button>
                    </div>
                </div>
            </form>

            <!-- Links -->
            <div>
                <label class="label">Verktyg</label>
                <div class="flex gap-sm flex-wrap">
                    <?php if ($eventsWithoutDestination > 0): ?>
                    <a href="/admin/tools/auto-create-venues.php" class="btn btn--secondary">
                        <i data-lucide="wand-2"></i>
                        Auto-skapa fran events (<?= $eventsWithoutDestination ?>)
                    </a>
                    <?php endif; ?>
                    <?php if ($destinationsWithoutRegion > 0): ?>
                    <a href="/admin/tools/auto-map-destination-regions.php" class="btn btn--secondary">
                        <i data-lucide="map"></i>
                        Koppla regioner (<?= $destinationsWithoutRegion ?>)
                    </a>
                    <?php endif; ?>
                    <a href="/admin/destination-edit.php" class="btn btn--primary">
                        <i data-lucide="plus"></i>
                        Ny Destination
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>

<?php if (count($potentialDuplicates) > 0): ?>
<!-- Potential Duplicates -->
<div class="card mb-lg" style="border-color: var(--color-warning);">
    <div class="card-header" style="background: rgba(251, 191, 36, 0.1);">
        <h2 style="color: var(--color-warning);">
            <i data-lucide="alert-triangle"></i>
            Potentiella Dubbletter (<?= count($potentialDuplicates) ?>)
        </h2>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Destination 1</th>
                        <th>Destination 2</th>
                        <th style="width: 150px;">Atgard</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($potentialDuplicates as $dup): ?>
                    <tr>
                        <td>
                            <strong><?= htmlspecialchars($dup['name1']) ?></strong>
                            <span class="badge badge--secondary ml-sm"><?= $dup['count1'] ?> events</span>
                        </td>
                        <td>
                            <strong><?= htmlspecialchars($dup['name2']) ?></strong>
                            <span class="badge badge--secondary ml-sm"><?= $dup['count2'] ?> events</span>
                        </td>
                        <td>
                            <form method="POST" class="flex gap-xs" onsubmit="return confirm('Sla samman dessa destinations?');">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="merge">
                                <input type="hidden" name="keep_id" value="<?= $dup['id1'] ?>">
                                <input type="hidden" name="merge_id" value="<?= $dup['id2'] ?>">
                                <button type="submit" class="btn btn--secondary btn--sm" title="Behall '<?= htmlspecialchars($dup['name1']) ?>'">
                                    <i data-lucide="merge"></i>
                                    Sla samman
                                </button>
                            </form>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Search and Filters -->
<div class="card mb-lg">
    <div class="card-body">
        <form method="GET" class="flex gap-md items-center flex-wrap">
            <div class="flex-1" style="min-width: 200px;">
                <input type="text" name="search" class="input" placeholder="Sok destination..."
                       value="<?= htmlspecialchars($search) ?>">
            </div>
            <select name="sort" class="input" style="width: 150px;" onchange="this.form.submit()">
                <option value="events" <?= $sortBy === 'events' ? 'selected' : '' ?>>Flest events</option>
                <option value="name" <?= $sortBy === 'name' ? 'selected' : '' ?>>Namn A-O</option>
                <option value="city" <?= $sortBy === 'city' ? 'selected' : '' ?>>Stad</option>
                <option value="recent" <?= $sortBy === 'recent' ? 'selected' : '' ?>>Senaste event</option>
            </select>
            <label class="checkbox-label">
                <input type="checkbox" name="inactive" class="checkbox" <?= $showInactive ? 'checked' : '' ?> onchange="this.form.submit()">
                <span>Visa inaktiva</span>
            </label>
            <button type="submit" class="btn btn--secondary">
                <i data-lucide="search"></i>
                Sok
            </button>
            <?php if ($search || $showInactive || $sortBy !== 'events'): ?>
            <a href="/admin/destinations.php" class="btn btn--ghost">
                <i data-lucide="x"></i>
                Rensa
            </a>
            <?php endif; ?>
        </form>
    </div>
</div>

<!-- Destinations List -->
<div class="card">
    <div class="card-header flex justify-between items-center">
        <h2>
            <i data-lucide="mountain"></i>
            Destinations (<?= count($destinations) ?>)
        </h2>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Destination</th>
                        <th>Stad</th>
                        <th>Region</th>
                        <th style="width: 80px;">Events</th>
                        <th style="width: 100px;">Senast</th>
                        <th style="width: 80px;">Status</th>
                        <th style="width: 100px;">Atgard</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (empty($destinations)): ?>
                    <tr>
                        <td colspan="7" class="text-center text-secondary py-lg">
                            Inga destinations hittades.
                            <a href="/admin/destination-edit.php">Skapa en ny?</a>
                        </td>
                    </tr>
                    <?php else: ?>
                    <?php foreach ($destinations as $dest): ?>
                    <tr>
                        <td>
                            <div class="flex items-center gap-sm">
                                <?php if ($dest['logo']): ?>
                                <img src="<?= htmlspecialchars($dest['logo']) ?>" alt="" style="height: 24px; border-radius: 4px;">
                                <?php else: ?>
                                <i data-lucide="mountain" class="text-secondary"></i>
                                <?php endif; ?>
                                <strong><?= htmlspecialchars($dest['name']) ?></strong>
                            </div>
                        </td>
                        <td class="text-secondary"><?= htmlspecialchars($dest['city'] ?? '') ?></td>
                        <td>
                            <?php if (!empty($dest['region'])): ?>
                            <span class="badge badge--secondary" title="<?= htmlspecialchars($dest['region']) ?>"><?= htmlspecialchars(mb_substr($dest['region'], 0, 12)) ?></span>
                            <?php else: ?>
                            <span class="text-warning" title="Saknar region">-</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?php if ($dest['event_count'] > 0): ?>
                            <span class="badge badge--accent"><?= $dest['event_count'] ?></span>
                            <?php else: ?>
                            <span class="badge badge--secondary">0</span>
                            <?php endif; ?>
                        </td>
                        <td class="text-secondary text-sm">
                            <?= $dest['last_event'] ? date('Y-m-d', strtotime($dest['last_event'])) : '-' ?>
                        </td>
                        <td>
                            <?php if ($dest['active']): ?>
                            <span class="badge badge--success">Aktiv</span>
                            <?php else: ?>
                            <span class="badge badge--secondary">Inaktiv</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <div class="flex gap-xs">
                                <a href="/admin/destination-edit.php?id=<?= $dest['id'] ?>" class="btn btn--secondary btn--sm" title="Redigera">
                                    <i data-lucide="pencil"></i>
                                </a>
                                <?php if ($dest['event_count'] > 0): ?>
                                <a href="/admin/events.php?venue_id=<?= $dest['id'] ?>" class="btn btn--secondary btn--sm" title="Visa events">
                                    <i data-lucide="calendar"></i>
                                </a>
                                <?php endif; ?>
                            </div>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
