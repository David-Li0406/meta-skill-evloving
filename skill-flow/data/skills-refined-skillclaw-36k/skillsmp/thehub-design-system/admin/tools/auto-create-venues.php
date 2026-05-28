<?php
/**
 * Auto-Create Venues Tool
 *
 * Skapar venues automatiskt baserat pa event-locations.
 * - Hittar events med location men utan venue_id
 * - Grupperar per location
 * - Skapar venues och kopplar till events
 *
 * @package TheHUB
 * @version 1.0
 */

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

// Handle message from redirect (PRG pattern)
$message = isset($_GET['msg']) ? $_GET['msg'] : '';
$messageType = isset($_GET['type']) ? $_GET['type'] : 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';
    $redirectMsg = '';
    $redirectType = 'info';

    // =========================================================================
    // CREATE VENUES - Batch create from selected locations
    // =========================================================================
    if ($action === 'create_venues') {
        $selectedLocations = $_POST['locations'] ?? [];

        if (empty($selectedLocations)) {
            $redirectMsg = 'Inga platser valda';
            $redirectType = 'warning';
        } else {
            $created = 0;
            $linked = 0;
            $errors = [];

            foreach ($selectedLocations as $location) {
                $location = trim($location);
                if (empty($location)) continue;

                try {
                    // Check if venue with this name already exists
                    $existing = $db->getRow(
                        "SELECT id FROM venues WHERE name = ?",
                        [$location]
                    );

                    if ($existing) {
                        $venueId = $existing['id'];
                    } else {
                        // Create new venue with location as name
                        $venueData = [
                            'name' => $location,
                            'city' => $location, // Use location as city initially
                            'country' => 'Sverige',
                            'active' => 1
                        ];
                        $db->insert('venues', $venueData);
                        $venueId = $db->lastInsertId();
                        $created++;
                    }

                    // Link all events with this location to the venue
                    $result = $db->query(
                        "UPDATE events SET venue_id = ? WHERE location = ? AND (venue_id IS NULL OR venue_id = 0)",
                        [$venueId, $location]
                    );
                    $linked += $result->rowCount();

                } catch (Exception $e) {
                    $errors[] = "$location: " . $e->getMessage();
                }
            }

            if ($created > 0 || $linked > 0) {
                $redirectMsg = "Skapade $created nya destinations och kopplade $linked events.";
                $redirectType = 'success';
            }

            if (!empty($errors)) {
                $redirectMsg .= " Fel: " . implode(', ', $errors);
                $redirectType = $created > 0 ? 'warning' : 'error';
            }
        }
    }

    // =========================================================================
    // LINK SINGLE - Link existing events to a specific venue
    // =========================================================================
    if ($action === 'link_to_venue') {
        $location = trim($_POST['location'] ?? '');
        $venueId = (int)($_POST['venue_id'] ?? 0);

        if (empty($location) || $venueId <= 0) {
            $redirectMsg = 'Ogiltig plats eller destination';
            $redirectType = 'error';
        } else {
            try {
                $result = $db->query(
                    "UPDATE events SET venue_id = ? WHERE location = ? AND (venue_id IS NULL OR venue_id = 0)",
                    [$venueId, $location]
                );
                $linked = $result->rowCount();
                $redirectMsg = "Kopplade $linked events till vald destination.";
                $redirectType = 'success';
            } catch (Exception $e) {
                $redirectMsg = 'Fel: ' . $e->getMessage();
                $redirectType = 'error';
            }
        }
    }

    // PRG pattern - redirect to avoid form resubmission and white page issue
    $redirectUrl = '/admin/tools/auto-create-venues.php';
    if ($redirectMsg) {
        $redirectUrl .= '?msg=' . urlencode($redirectMsg) . '&type=' . $redirectType;
    }
    header('Location: ' . $redirectUrl);
    exit;
}

// Fetch events grouped by location (without venue)
$locationGroups = $db->getAll("
    SELECT
        location,
        COUNT(*) as event_count,
        MIN(date) as first_event,
        MAX(date) as last_event,
        GROUP_CONCAT(DISTINCT YEAR(date) ORDER BY YEAR(date) SEPARATOR ', ') as years
    FROM events
    WHERE location IS NOT NULL
      AND location != ''
      AND (venue_id IS NULL OR venue_id = 0)
    GROUP BY location
    ORDER BY event_count DESC, location ASC
");

// Fetch existing venues for mapping dropdown
$venues = $db->getAll("
    SELECT id, name, city
    FROM venues
    WHERE active = 1
    ORDER BY name
");

// Count totals
$totalLocations = count($locationGroups);
$totalEventsWithoutVenue = array_sum(array_column($locationGroups, 'event_count'));

// Page config for unified layout
$page_title = 'Auto-skapa Destinations';
$breadcrumbs = [
    ['label' => 'Destinations', 'url' => '/admin/destinations.php'],
    ['label' => 'Auto-skapa fran Events']
];
include __DIR__ . '/../components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
    <div class="alert alert--<?= $messageType ?> mb-lg">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<!-- Summary Card -->
<div class="card mb-lg">
    <div class="card-header">
        <h2>
            <i data-lucide="mountain"></i>
            Destinations fran Event-platser
        </h2>
    </div>
    <div class="card-body">
        <p class="text-secondary mb-md">
            Detta verktyg hittar events som har en plats (location) men ingen kopplad destination.
            Du kan skapa destinations automatiskt baserat pa platsnamnet och koppla events till dem.
        </p>

        <div class="grid grid-stats grid-gap-md mb-lg">
            <div class="card" style="background: var(--color-bg-hover);">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-accent"><?= $totalLocations ?></div>
                    <div class="text-sm text-secondary">Unika platser</div>
                </div>
            </div>
            <div class="card" style="background: var(--color-bg-hover);">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-warning"><?= $totalEventsWithoutVenue ?></div>
                    <div class="text-sm text-secondary">Events utan destination</div>
                </div>
            </div>
            <div class="card" style="background: var(--color-bg-hover);">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-success"><?= count($venues) ?></div>
                    <div class="text-sm text-secondary">Existerande destinations</div>
                </div>
            </div>
        </div>

        <?php if ($totalLocations === 0): ?>
            <div class="alert alert--success">
                <i data-lucide="check-circle"></i>
                Alla events med plats har redan en kopplad destination!
            </div>
        <?php endif; ?>
    </div>
</div>

<?php if ($totalLocations > 0): ?>
<!-- Batch Create Form -->
<form method="POST" id="batch-form">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="create_venues">

    <div class="card mb-lg">
        <div class="card-header flex justify-between items-center">
            <h2>
                <i data-lucide="map-pin"></i>
                Platser utan Destination (<?= $totalLocations ?>)
            </h2>
            <div class="flex gap-sm">
                <button type="button" class="btn btn--secondary btn--sm" onclick="selectAll(true)">
                    <i data-lucide="check-square"></i>
                    Valj alla
                </button>
                <button type="button" class="btn btn--secondary btn--sm" onclick="selectAll(false)">
                    <i data-lucide="square"></i>
                    Avmarkera alla
                </button>
                <button type="submit" class="btn btn--primary btn--sm">
                    <i data-lucide="plus"></i>
                    Skapa valda som Destinations
                </button>
            </div>
        </div>
        <div class="card-body" style="padding: 0;">
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th style="width: 40px;">
                                <input type="checkbox" id="select-all" onchange="selectAll(this.checked)">
                            </th>
                            <th>Plats</th>
                            <th style="width: 100px;">Events</th>
                            <th style="width: 150px;">Ar</th>
                            <th style="width: 200px;">Koppla till befintlig</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($locationGroups as $loc): ?>
                        <tr>
                            <td>
                                <input type="checkbox" name="locations[]"
                                       value="<?= htmlspecialchars($loc['location']) ?>"
                                       class="location-checkbox">
                            </td>
                            <td>
                                <strong><?= htmlspecialchars($loc['location']) ?></strong>
                            </td>
                            <td>
                                <span class="badge badge--secondary"><?= $loc['event_count'] ?></span>
                            </td>
                            <td class="text-secondary text-sm">
                                <?= htmlspecialchars($loc['years']) ?>
                            </td>
                            <td>
                                <div class="flex gap-xs items-center">
                                    <select class="input input--sm link-venue-select" data-location="<?= htmlspecialchars($loc['location']) ?>" style="width: 120px;">
                                        <option value="">Valj...</option>
                                        <?php foreach ($venues as $v): ?>
                                        <option value="<?= $v['id'] ?>">
                                            <?= htmlspecialchars($v['name']) ?>
                                        </option>
                                        <?php endforeach; ?>
                                    </select>
                                    <button type="button" class="btn btn--secondary btn--sm link-venue-btn" data-location="<?= htmlspecialchars($loc['location']) ?>" title="Koppla">
                                        <i data-lucide="link"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</form>

<!-- Separate hidden form for linking to existing venue -->
<form method="POST" id="link-form" style="display: none;">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="link_to_venue">
    <input type="hidden" name="location" id="link-location" value="">
    <input type="hidden" name="venue_id" id="link-venue-id" value="">
</form>

<script>
function selectAll(checked) {
    document.querySelectorAll('.location-checkbox').forEach(cb => {
        cb.checked = checked;
    });
    document.getElementById('select-all').checked = checked;
}

// Handle link to existing venue buttons
document.querySelectorAll('.link-venue-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const location = this.dataset.location;
        const row = this.closest('tr');
        const select = row.querySelector('.link-venue-select');
        const venueId = select.value;

        if (!venueId) {
            alert('Valj en destination forst');
            return;
        }

        document.getElementById('link-location').value = location;
        document.getElementById('link-venue-id').value = venueId;
        document.getElementById('link-form').submit();
    });
});
</script>
<?php endif; ?>

<!-- Help Section -->
<div class="card">
    <div class="card-header">
        <h2>
            <i data-lucide="help-circle"></i>
            Hur fungerar det?
        </h2>
    </div>
    <div class="card-body">
        <div class="grid grid-2 grid-gap-lg">
            <div>
                <h3 class="text-accent mb-sm">Skapa nya destinations</h3>
                <ol class="text-secondary" style="padding-left: var(--space-md);">
                    <li>Markera platser du vill skapa destinations for</li>
                    <li>Klicka "Skapa valda som Destinations"</li>
                    <li>En ny destination skapas med platsnamnet</li>
                    <li>Alla events med den platsen kopplas automatiskt</li>
                </ol>
            </div>
            <div>
                <h3 class="text-accent mb-sm">Koppla till befintlig destination</h3>
                <ol class="text-secondary" style="padding-left: var(--space-md);">
                    <li>Om en destination redan finns, valj den i dropdown</li>
                    <li>Klicka lanken-ikonen</li>
                    <li>Alla events med den platsen kopplas till vald destination</li>
                </ol>
            </div>
        </div>

        <div class="alert alert--info mt-lg">
            <i data-lucide="info"></i>
            <strong>Tips:</strong> Efter att destinations skapats kan du redigera dem under
            <a href="/admin/destinations.php">Databas &gt; Destinations</a> for att lagga till mer information
            som GPS-koordinater, kontaktinfo och faciliteter.
        </div>
    </div>
</div>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
