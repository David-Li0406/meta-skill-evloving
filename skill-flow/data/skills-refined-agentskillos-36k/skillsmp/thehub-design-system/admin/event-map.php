<?php
/**
 * Admin Event Map Management - Multi-track support
 */
require_once __DIR__ . '/../config.php';
require_admin();
require_once INCLUDES_PATH . '/map_functions.php';

$db = getDB();
global $pdo;

// Get event ID
$eventId = intval($_GET['id'] ?? $_GET['event_id'] ?? 0);
if ($eventId <= 0) {
    set_flash('error', 'Ogiltigt event-ID');
    header('Location: /admin/events');
    exit;
}

$event = $db->getRow("SELECT id, name, date, karta_publish_at, map_image_url FROM events WHERE id = ?", [$eventId]);
if (!$event) {
    set_flash('error', 'Event hittades inte');
    header('Location: /admin/events');
    exit;
}

$message = '';
$messageType = '';

// Selected track for editing
$selectedTrackId = intval($_GET['track'] ?? 0);

// Handle POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $action = $_POST['action'] ?? '';

    try {
        switch ($action) {
            case 'upload_gpx':
                if (!isset($_FILES['gpx_file']) || $_FILES['gpx_file']['error'] !== UPLOAD_ERR_OK) {
                    throw new Exception('Ingen fil uppladdad');
                }
                $file = $_FILES['gpx_file'];
                if (strtolower(pathinfo($file['name'], PATHINFO_EXTENSION)) !== 'gpx') {
                    throw new Exception('Endast GPX-filer');
                }
                $uploadDir = getGpxUploadPath();
                $filename = 'event_' . $eventId . '_' . time() . '.gpx';
                $filepath = $uploadDir . '/' . $filename;
                if (!move_uploaded_file($file['tmp_name'], $filepath)) {
                    throw new Exception('Kunde inte spara');
                }
                $parsedData = parseGpxFile($filepath);
                $trackName = trim($_POST['track_name'] ?? '') ?: $event['name'];
                $options = [
                    'route_type' => trim($_POST['route_type'] ?? ''),
                    'route_label' => trim($_POST['route_label'] ?? '') ?: $trackName,
                    'color' => $_POST['track_color'] ?? '#3B82F6',
                    'is_primary' => !empty($_POST['is_primary'])
                ];
                $newTrackId = saveEventTrack($pdo, $eventId, $trackName, $filename, $parsedData, $options);
                $selectedTrackId = $newTrackId;
                $message = 'GPX uppladdad!';
                $messageType = 'success';
                break;

            case 'update_track':
                $trackId = intval($_POST['track_id'] ?? 0);
                if ($trackId > 0) {
                    updateTrack($pdo, $trackId, [
                        'name' => trim($_POST['track_name'] ?? ''),
                        'route_label' => trim($_POST['route_label'] ?? ''),
                        'color' => $_POST['track_color'] ?? '#3B82F6',
                        'is_primary' => !empty($_POST['is_primary'])
                    ]);
                    $message = 'Bana uppdaterad';
                    $messageType = 'success';
                }
                break;

            case 'delete_track':
                $trackId = intval($_POST['track_id'] ?? 0);
                if ($trackId > 0) {
                    deleteEventTrack($pdo, $trackId);
                    if ($selectedTrackId == $trackId) $selectedTrackId = 0;
                }
                $message = 'Bana borttagen';
                $messageType = 'success';
                break;

            case 'add_poi':
                $poiData = [
                    'poi_type' => $_POST['poi_type'] ?? '',
                    'label' => trim($_POST['poi_label'] ?? ''),
                    'lat' => floatval($_POST['poi_lat'] ?? 0),
                    'lng' => floatval($_POST['poi_lng'] ?? 0),
                ];
                if (empty($poiData['poi_type']) || $poiData['lat'] == 0) {
                    throw new Exception('Typ och koordinater krävs');
                }
                addEventPoi($pdo, $eventId, $poiData);
                $message = 'POI tillagd';
                $messageType = 'success';
                break;

            case 'delete_poi':
                $poiId = intval($_POST['poi_id'] ?? 0);
                if ($poiId > 0) deleteEventPoi($pdo, $poiId);
                $message = 'POI borttagen';
                $messageType = 'success';
                break;

            case 'delete_segment':
                $segmentId = intval($_POST['segment_id'] ?? 0);
                if ($segmentId > 0) {
                    $pdo->prepare("DELETE FROM event_track_segments WHERE id = ?")->execute([$segmentId]);
                }
                $message = 'Segment borttaget';
                $messageType = 'success';
                break;

            case 'update_segment_type':
                $segmentId = intval($_POST['segment_id'] ?? 0);
                $newType = $_POST['new_type'] ?? '';
                if ($segmentId > 0 && in_array($newType, ['stage', 'liaison', 'lift'])) {
                    $colors = ['stage' => '#EF4444', 'liaison' => '#61CE70', 'lift' => '#F59E0B'];
                    $pdo->prepare("UPDATE event_track_segments SET segment_type = ?, color = ? WHERE id = ?")
                        ->execute([$newType, $colors[$newType], $segmentId]);
                }
                $message = 'Sektionstyp uppdaterad';
                $messageType = 'success';
                break;

            case 'update_segment_name':
                $segmentId = intval($_POST['segment_id'] ?? 0);
                $newName = trim($_POST['new_name'] ?? '');
                if ($segmentId > 0) {
                    $pdo->prepare("UPDATE event_track_segments SET segment_name = ? WHERE id = ?")
                        ->execute([$newName, $segmentId]);
                }
                $message = 'Segmentnamn uppdaterat';
                $messageType = 'success';
                break;

            case 'update_segment_sponsor':
                $segmentId = intval($_POST['segment_id'] ?? 0);
                $sponsorId = !empty($_POST['sponsor_id']) ? intval($_POST['sponsor_id']) : null;
                if ($segmentId > 0) {
                    $pdo->prepare("UPDATE event_track_segments SET sponsor_id = ? WHERE id = ?")
                        ->execute([$sponsorId, $segmentId]);
                }
                $message = 'Sträcksponsor uppdaterad';
                $messageType = 'success';
                break;

            case 'add_segment_visual':
                $trackId = intval($_POST['track_id'] ?? 0);
                $segmentName = trim($_POST['segment_name'] ?? '');
                $segmentType = $_POST['segment_type'] ?? 'stage';
                $startIdx = intval($_POST['start_index'] ?? -1);
                $endIdx = intval($_POST['end_index'] ?? -1);
                if ($trackId <= 0 || $startIdx < 0 || $endIdx < 0 || $endIdx <= $startIdx) {
                    throw new Exception('Ogiltig sträckdata');
                }
                addSegmentByWaypointIndex($pdo, $trackId, [
                    'name' => $segmentName ?: ($segmentType === 'stage' ? 'SS' : 'Liaison'),
                    'type' => $segmentType,
                    'start_index' => $startIdx,
                    'end_index' => $endIdx
                ]);
                $message = 'Sträcka tillagd!';
                $messageType = 'success';
                break;

            case 'save_all_segments':
                $trackId = intval($_POST['track_id'] ?? 0);
                $segmentsJson = $_POST['segments_data'] ?? '[]';
                $segments = json_decode($segmentsJson, true);

                if ($trackId <= 0 || empty($segments)) {
                    throw new Exception('Ingen segmentdata');
                }

                // Delete existing segments for this track
                $pdo->prepare("DELETE FROM event_track_segments WHERE track_id = ?")->execute([$trackId]);

                // Add all new segments
                $ssCount = 0;
                $liftCount = 0;
                foreach ($segments as $seg) {
                    $type = $seg['type'] ?? 'liaison';
                    $name = '';
                    if ($type === 'stage') {
                        $ssCount++;
                        $name = 'SS' . $ssCount;
                    } elseif ($type === 'lift') {
                        $liftCount++;
                        $name = 'Lift ' . $liftCount;
                    } else {
                        $name = 'Transport';
                    }

                    addSegmentByWaypointIndex($pdo, $trackId, [
                        'name' => $name,
                        'type' => $type,
                        'start_index' => intval($seg['start']),
                        'end_index' => intval($seg['end'])
                    ]);
                }

                $message = count($segments) . ' sektioner sparade!';
                $messageType = 'success';
                break;

            case 'update_publish_date':
                $publishAt = !empty($_POST['karta_publish_at']) ? trim($_POST['karta_publish_at']) : null;
                $db->query("UPDATE events SET karta_publish_at = ? WHERE id = ?", [$publishAt, $eventId]);
                // Refresh event data
                $event['karta_publish_at'] = $publishAt;
                $message = $publishAt ? 'Publiceringstid sparad: ' . date('Y-m-d H:i', strtotime($publishAt)) : 'Kartan visas direkt';
                $messageType = 'success';
                break;

            case 'upload_static_map':
                // Handle static map image upload
                if (!isset($_FILES['static_map_image']) || $_FILES['static_map_image']['error'] === UPLOAD_ERR_NO_FILE) {
                    // Check if URL was provided instead
                    $mapUrl = trim($_POST['map_image_url'] ?? '');
                    if (!empty($mapUrl)) {
                        $db->query("UPDATE events SET map_image_url = ? WHERE id = ?", [$mapUrl, $eventId]);
                        $event['map_image_url'] = $mapUrl;
                        $message = 'Kartbild-URL sparad';
                        $messageType = 'success';
                    } else {
                        throw new Exception('Ingen bild vald');
                    }
                } else {
                    $file = $_FILES['static_map_image'];
                    if ($file['error'] !== UPLOAD_ERR_OK) {
                        throw new Exception('Fel vid uppladdning');
                    }

                    // Validate file type
                    $allowedTypes = ['image/png', 'image/jpeg', 'image/webp'];
                    $finfo = finfo_open(FILEINFO_MIME_TYPE);
                    $mimeType = finfo_file($finfo, $file['tmp_name']);
                    finfo_close($finfo);

                    if (!in_array($mimeType, $allowedTypes)) {
                        throw new Exception('Endast PNG, JPG eller WebP tillåts');
                    }

                    // Create upload directory
                    $uploadDir = ROOT_PATH . '/media/events';
                    if (!is_dir($uploadDir)) {
                        mkdir($uploadDir, 0755, true);
                    }

                    // Generate filename
                    $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
                    $filename = 'map_' . $eventId . '_' . time() . '.' . $ext;
                    $filepath = $uploadDir . '/' . $filename;

                    if (!move_uploaded_file($file['tmp_name'], $filepath)) {
                        throw new Exception('Kunde inte spara bilden');
                    }

                    // Save to database
                    $mapUrl = '/media/events/' . $filename;
                    $db->query("UPDATE events SET map_image_url = ? WHERE id = ?", [$mapUrl, $eventId]);
                    $event['map_image_url'] = $mapUrl;

                    $message = 'Kartbild uppladdad!';
                    $messageType = 'success';
                }
                break;

            case 'remove_static_map':
                $db->query("UPDATE events SET map_image_url = NULL WHERE id = ?", [$eventId]);
                $event['map_image_url'] = null;
                $message = 'Kartbild borttagen';
                $messageType = 'success';
                break;
        }
    } catch (Exception $e) {
        $message = $e->getMessage();
        $messageType = 'error';
    }
}

// Get all tracks for event
$allTracks = getEventTracks($pdo, $eventId);
$pois = getEventPois($pdo, $eventId, false) ?: [];
$poiTypes = getPoiTypesForSelect() ?: [];

// Select first track if none selected
if ($selectedTrackId <= 0 && !empty($allTracks)) {
    $selectedTrackId = $allTracks[0]['id'];
}

// Get selected track details
$currentTrack = null;
$trackWaypoints = [];
foreach ($allTracks as $t) {
    if ($t['id'] == $selectedTrackId) {
        $currentTrack = $t;
        break;
    }
}

if ($currentTrack) {
    try {
        $trackWaypoints = getTrackWaypointsForEditor($pdo, $currentTrack['id']);
    } catch (Exception $e) {
        $trackWaypoints = [];
    }
}

// Get map data for display (all tracks)
$mapData = getEventMapDataMultiTrack($pdo, $eventId);

// Track colors for selection
$trackColors = [
    '#3B82F6' => 'Blå',
    '#61CE70' => 'Grön',
    '#EF4444' => 'Röd',
    '#F59E0B' => 'Orange',
    '#8B5CF6' => 'Lila',
    '#EC4899' => 'Rosa',
    '#14B8A6' => 'Teal',
    '#6B7280' => 'Grå'
];

// Get sponsors for segment dropdown (check if column AND table exist)
$sponsors = [];
$sponsorColumnExists = false;
try {
    $colCheck = $pdo->query("SHOW COLUMNS FROM event_track_segments LIKE 'sponsor_id'");
    $sponsorColumnExists = $colCheck->fetch() !== false;
    if ($sponsorColumnExists) {
        // Also check if sponsors table exists and get available columns
        $tableCheck = $pdo->query("SHOW TABLES LIKE 'sponsors'");
        if ($tableCheck->fetch() !== false) {
            // Get actual columns to avoid missing column errors
            $cols = $pdo->query("SHOW COLUMNS FROM sponsors");
            $sponsorCols = [];
            while ($col = $cols->fetch(PDO::FETCH_ASSOC)) {
                $sponsorCols[] = $col['Field'];
            }
            // Build dynamic SELECT
            $selectFields = ['id', 'name'];
            if (in_array('logo', $sponsorCols)) $selectFields[] = 'logo';
            $sponsorStmt = $pdo->query("SELECT " . implode(', ', $selectFields) . " FROM sponsors WHERE active = 1 ORDER BY name ASC");
            $sponsors = $sponsorStmt->fetchAll(PDO::FETCH_ASSOC);
        } else {
            $sponsorColumnExists = false; // Table doesn't exist, disable feature
        }
    }
} catch (Exception $e) {
    // Sponsors not available
    $sponsorColumnExists = false;
}

// Page setup
$page_title = 'Karta - ' . htmlspecialchars($event['name']);
$breadcrumbs = [
    ['label' => 'Events', 'url' => '/admin/events'],
    ['label' => htmlspecialchars($event['name']), 'url' => '/admin/events/edit/' . $eventId],
    ['label' => 'Karta']
];
$page_actions = '<a href="/admin/events/edit/' . $eventId . '" class="btn-admin btn-admin-secondary">Tillbaka</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'error' ? 'error' : 'success' ?>" class="mb-md">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Map Publish Settings -->
<div class="admin-card" class="mb-md">
    <div class="admin-card-body" style="display: flex; align-items: center; gap: var(--space-lg); flex-wrap: wrap;">
        <div class="flex-1" style="min-width: 200px;">
            <strong><i data-lucide="calendar-clock" class="icon-sm"></i> Karta publiceras</strong>
            <p class="text-sm text-secondary" class="m-0">
                <?php if (!empty($event['karta_publish_at'])): ?>
                    <?= date('Y-m-d H:i', strtotime($event['karta_publish_at'])) ?>
                    <?php if (strtotime($event['karta_publish_at']) > time()): ?>
                        <span class="badge badge-warning">Schemalagd</span>
                    <?php else: ?>
                        <span class="badge badge-success">Publicerad</span>
                    <?php endif; ?>
                <?php else: ?>
                    <span class="badge badge-success">Synlig direkt</span>
                <?php endif; ?>
            </p>
        </div>
        <form method="POST" class="flex gap-sm" class="items-center">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="update_publish_date">
            <input type="datetime-local" name="karta_publish_at" class="admin-form-input admin-form-input-sm"
                   class="w-auto"
                   value="<?= !empty($event['karta_publish_at']) ? date('Y-m-d\TH:i', strtotime($event['karta_publish_at'])) : '' ?>">
            <button type="submit" class="btn-admin btn-admin-primary btn-admin-sm">Spara</button>
            <?php if (!empty($event['karta_publish_at'])): ?>
            <button type="submit" class="btn-admin btn-admin-ghost btn-admin-sm" onclick="this.form.querySelector('[name=karta_publish_at]').value=''">Rensa</button>
            <?php endif; ?>
        </form>
    </div>
</div>

<!-- Static Map Image Section -->
<div class="admin-card mb-md">
    <div class="admin-card-body">
        <div class="flex justify-between items-start gap-lg flex-wrap">
            <div class="flex-1" style="min-width: 250px;">
                <strong><i data-lucide="image" class="icon-sm"></i> Statisk kartbild</strong>
                <p class="text-sm text-secondary m-0 mt-xs">
                    Använd en statisk bild istället för interaktiv karta. Perfekt för enklare evenemang.
                </p>
            </div>
            <div class="flex-1" style="min-width: 300px;">
                <?php if (!empty($event['map_image_url'])): ?>
                <div class="flex gap-md items-start mb-md">
                    <img src="<?= htmlspecialchars($event['map_image_url']) ?>" alt="Kartbild"
                         style="max-width: 200px; max-height: 120px; border-radius: var(--radius-sm); border: 1px solid var(--color-border);">
                    <div>
                        <span class="badge badge-success mb-xs">Aktiv</span>
                        <p class="text-xs text-secondary m-0"><?= htmlspecialchars($event['map_image_url']) ?></p>
                        <form method="POST" class="mt-sm">
                            <?= csrf_field() ?>
                            <input type="hidden" name="action" value="remove_static_map">
                            <button type="submit" class="btn-admin btn-admin-danger btn-admin-xs" onclick="return confirm('Ta bort kartbild?')">
                                <i data-lucide="trash-2" class="icon-xs"></i> Ta bort
                            </button>
                        </form>
                    </div>
                </div>
                <?php endif; ?>

                <form method="POST" enctype="multipart/form-data">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="upload_static_map">
                    <div class="flex gap-sm items-end flex-wrap">
                        <div class="form-group mb-0" style="flex: 1; min-width: 200px;">
                            <label class="form-label text-sm mb-xs">Ladda upp bild</label>
                            <input type="file" name="static_map_image" accept="image/png,image/jpeg,image/webp"
                                   class="admin-form-input admin-form-input-sm">
                        </div>
                        <span class="text-secondary text-sm">eller</span>
                        <div class="form-group mb-0" style="flex: 1; min-width: 200px;">
                            <label class="form-label text-sm mb-xs">Ange URL</label>
                            <input type="url" name="map_image_url" placeholder="https://... eller /media/..."
                                   class="admin-form-input admin-form-input-sm"
                                   value="<?= htmlspecialchars($event['map_image_url'] ?? '') ?>">
                        </div>
                        <button type="submit" class="btn-admin btn-admin-primary btn-admin-sm">
                            <i data-lucide="upload" class="icon-sm"></i> Spara
                        </button>
                    </div>
                    <small class="form-help text-xs mt-sm block">PNG, JPG eller WebP. Rekommenderad storlek: 1200x800 px.</small>
                </form>
            </div>
        </div>
    </div>
</div>

<div class="admin-grid admin-grid-sidebar">
    <!-- Sidebar: Controls -->
    <div class="admin-sidebar-narrow">
        <!-- Banor -->
        <div class="admin-card admin-card-compact">
            <div class="admin-card-header">
                <h2>Banor (<?= count($allTracks) ?>)</h2>
            </div>
            <div class="admin-card-body">
                <?php if (!empty($allTracks)): ?>
                <div class="admin-list admin-list-compact">
                    <?php foreach ($allTracks as $t): ?>
                    <div class="admin-list-item <?= $t['id'] == $selectedTrackId ? 'active' : '' ?>">
                        <span class="color-dot" style="background: <?= htmlspecialchars($t['color'] ?? '#3B82F6') ?>;"></span>
                        <span class="admin-list-item-text"><?= htmlspecialchars($t['route_label'] ?? $t['name']) ?></span>
                        <span class="admin-text-muted"><?= number_format($t['total_distance_km'], 1) ?>km</span>
                        <?php if ($t['id'] != $selectedTrackId): ?>
                        <a href="?id=<?= $eventId ?>&track=<?= $t['id'] ?>" class="btn-admin btn-admin-ghost btn-admin-xs">Välj</a>
                        <?php endif; ?>
                        <form method="POST" class="inline-form">
                            <?= csrf_field() ?>
                            <input type="hidden" name="action" value="delete_track">
                            <input type="hidden" name="track_id" value="<?= $t['id'] ?>">
                            <button type="submit" class="btn-admin btn-admin-ghost btn-admin-xs btn-admin-danger" onclick="return confirm('Ta bort?')">×</button>
                        </form>
                    </div>
                    <?php endforeach; ?>
                </div>
                <?php endif; ?>

                <details class="admin-details" <?= empty($allTracks) ? 'open' : '' ?>>
                    <summary>+ Ladda upp GPX</summary>
                    <form method="POST" enctype="multipart/form-data" class="admin-form-compact">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="upload_gpx">
                        <div class="admin-form-group">
                            <input type="text" name="track_name" class="admin-form-input admin-form-input-sm" placeholder="Bannamn">
                        </div>
                        <div class="admin-form-row">
                            <select name="track_color" class="admin-form-select admin-form-select-sm">
                                <?php foreach ($trackColors as $hex => $name): ?>
                                <option value="<?= $hex ?>"><?= $name ?></option>
                                <?php endforeach; ?>
                            </select>
                            <label class="admin-checkbox-inline">
                                <input type="checkbox" name="is_primary" value="1" <?= empty($allTracks) ? 'checked' : '' ?>>
                                Primär
                            </label>
                        </div>
                        <div class="admin-form-group">
                            <input type="file" name="gpx_file" accept=".gpx" required class="admin-form-input admin-form-input-sm">
                        </div>
                        <button type="submit" class="btn-admin btn-admin-primary btn-admin-sm btn-admin-block">Ladda upp</button>
                    </form>
                </details>
            </div>
        </div>

        <?php if ($currentTrack): ?>
        <!-- Redigera bana -->
        <div class="admin-card admin-card-compact">
            <div class="admin-card-header">
                <h2>
                    <span class="color-dot" style="background: <?= htmlspecialchars($currentTrack['color'] ?? '#3B82F6') ?>;"></span>
                    <?= htmlspecialchars($currentTrack['route_label'] ?? $currentTrack['name']) ?>
                </h2>
            </div>
            <div class="admin-card-body">
                <details class="admin-details">
                    <summary>⚙️ Inställningar</summary>
                    <form method="POST" class="admin-form-compact">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="update_track">
                        <input type="hidden" name="track_id" value="<?= $currentTrack['id'] ?>">
                        <div class="admin-form-group">
                            <input type="text" name="track_name" class="admin-form-input admin-form-input-sm" value="<?= htmlspecialchars($currentTrack['name']) ?>">
                        </div>
                        <div class="admin-form-row">
                            <select name="track_color" class="admin-form-select admin-form-select-sm">
                                <?php foreach ($trackColors as $hex => $name): ?>
                                <option value="<?= $hex ?>" <?= ($currentTrack['color'] ?? '#3B82F6') === $hex ? 'selected' : '' ?>><?= $name ?></option>
                                <?php endforeach; ?>
                            </select>
                            <label class="admin-checkbox-inline">
                                <input type="checkbox" name="is_primary" value="1" <?= $currentTrack['is_primary'] ? 'checked' : '' ?>>
                                Primär
                            </label>
                        </div>
                        <button type="submit" class="btn-admin btn-admin-secondary btn-admin-sm btn-admin-block">Spara</button>
                    </form>
                </details>
            </div>
        </div>

        <!-- Sektioner - Multi-point editor -->
        <div class="admin-card admin-card-compact">
            <div class="admin-card-header">
                <h2>Sektioner</h2>
            </div>
            <div class="admin-card-body">
                <div id="segment-status" class="admin-status-box">
                    <strong>Steg 1:</strong> Klicka på banan för att sätta ut delningspunkter
                </div>

                <div id="markers-info" class="admin-info-box" class="hidden">
                    <span id="markers-count">0 punkter</span>
                    <button type="button" onclick="clearAllMarkers()" class="btn-admin btn-admin-ghost btn-admin-xs">Rensa alla</button>
                </div>

                <!-- Segment list - dynamically updated -->
                <div id="segments-list" class="admin-segment-list">
                    <p class="admin-text-muted admin-text-sm">Sätt ut minst 1 punkt för att skapa sektioner</p>
                </div>

                <!-- Save button -->
                <div id="save-actions" style="display: none; margin-top: var(--space-sm);">
                    <button type="button" onclick="saveAllSegments()" class="btn-admin btn-admin-primary btn-admin-block">
                        <i data-lucide="save" class="icon-xs"></i> Spara alla sektioner
                    </button>
                </div>

                <!-- Existing segments (saved) -->
                <?php if (!empty($currentTrack['segments'])): ?>
                <div class="admin-existing-segments" style="margin-top: var(--space-md); padding-top: var(--space-md); border-top: 1px solid var(--color-border);">
                    <div class="admin-text-muted admin-text-sm" class="mb-xs">Sparade sektioner:</div>
                    <?php foreach ($currentTrack['segments'] as $segIdx => $seg):
                        $iconName = $seg['segment_type'] === 'stage' ? 'flag' : ($seg['segment_type'] === 'lift' ? 'cable-car' : 'route');
                        $hasSponsor = !empty($seg['sponsor_name']);
                        $segStart = intval($seg['start_index'] ?? 0);
                        $segEnd = intval($seg['end_index'] ?? 0);
                        $typeLabel = $seg['segment_type'] === 'stage' ? 'SS' : ($seg['segment_type'] === 'lift' ? 'Lift' : 'Transport');
                        $segDisplayName = !empty($seg['segment_name']) ? $seg['segment_name'] : "Sektion " . ($segIdx + 1);
                    ?>
                    <div class="admin-segment-item <?= $hasSponsor ? 'has-sponsor' : '' ?>"
                         onclick="selectSegment(<?= $segIdx ?>, <?= $segStart ?>, <?= $segEnd ?>)"
                         style="cursor: pointer;"
                         data-start="<?= $segStart ?>"
                         data-end="<?= $segEnd ?>"
                         data-segment-id="<?= $seg['id'] ?>">
                        <span class="color-dot" style="background: <?= htmlspecialchars($seg['color']) ?>;"></span>
                        <i data-lucide="<?= $iconName ?>" class="icon-xs" style="flex-shrink: 0;"></i>
                        <input type="text" class="admin-segment-name-input" value="<?= htmlspecialchars($seg['segment_name'] ?? '') ?>" placeholder="Namn..." onclick="event.stopPropagation()" onchange="changeSegmentName(<?= $seg['id'] ?>, this.value)" title="Segmentnamn (t.ex. SS1, Powerstage)">
                        <?php if ($hasSponsor): ?>
                        <span class="segment-sponsor-badge" title="<?= htmlspecialchars($seg['sponsor_name']) ?>">
                            <span class="sponsor-by">by</span>
                            <?php if (!empty($seg['sponsor_logo'])): ?>
                            <img src="<?= htmlspecialchars($seg['sponsor_logo']) ?>" alt="<?= htmlspecialchars($seg['sponsor_name']) ?>" class="sponsor-logo-mini">
                            <?php else: ?>
                            <span class="sponsor-name-mini"><?= htmlspecialchars($seg['sponsor_name']) ?></span>
                            <?php endif; ?>
                        </span>
                        <?php endif; ?>
                        <span class="admin-text-muted segment-distance"><?= number_format($seg['distance_km'], 1) ?>km</span>
                        <select onclick="event.stopPropagation()" onchange="changeSegmentType(<?= $seg['id'] ?>, this.value)" class="admin-form-select admin-form-select-xs">
                            <option value="liaison" <?= $seg['segment_type'] === 'liaison' ? 'selected' : '' ?>>Transport</option>
                            <option value="stage" <?= $seg['segment_type'] === 'stage' ? 'selected' : '' ?>>Sträcka</option>
                            <option value="lift" <?= $seg['segment_type'] === 'lift' ? 'selected' : '' ?>>Lift</option>
                        </select>
                        <?php if ($sponsorColumnExists && !empty($sponsors) && $seg['segment_type'] === 'stage'): ?>
                        <select onclick="event.stopPropagation()" onchange="changeSegmentSponsor(<?= $seg['id'] ?>, this.value)" class="admin-form-select admin-form-select-xs" title="Sträcksponsor">
                            <option value="">Sponsor</option>
                            <?php foreach ($sponsors as $sp): ?>
                            <option value="<?= $sp['id'] ?>" <?= ($seg['sponsor_id'] ?? '') == $sp['id'] ? 'selected' : '' ?>><?= htmlspecialchars($sp['name']) ?></option>
                            <?php endforeach; ?>
                        </select>
                        <?php endif; ?>
                        <form method="POST" class="inline-form" onclick="event.stopPropagation()">
                            <?= csrf_field() ?>
                            <input type="hidden" name="action" value="delete_segment">
                            <input type="hidden" name="segment_id" value="<?= $seg['id'] ?>">
                            <button type="submit" class="btn-admin btn-admin-ghost btn-admin-xs btn-admin-danger" onclick="return confirm('Ta bort?')">×</button>
                        </form>
                    </div>
                    <?php endforeach; ?>
                    <button type="button" onclick="editExistingSegments()" class="btn-admin btn-admin-secondary btn-admin-sm btn-admin-block" class="mt-sm">
                        <i data-lucide="pencil" class="icon-xs"></i> Redigera sektioner
                    </button>
                </div>
                <?php endif; ?>

                <!-- Hidden form for saving -->
                <form method="POST" id="save-segments-form" class="hidden">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="save_all_segments">
                    <input type="hidden" name="track_id" value="<?= $currentTrack['id'] ?>">
                    <input type="hidden" name="segments_data" id="segments-data" value="[]">
                </form>
                <form method="POST" id="update-type-form" class="hidden">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="update_segment_type">
                    <input type="hidden" name="segment_id" id="update-seg-id" value="">
                    <input type="hidden" name="new_type" id="update-new-type" value="">
                </form>
                <form method="POST" id="update-name-form" class="hidden">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="update_segment_name">
                    <input type="hidden" name="segment_id" id="update-name-seg-id" value="">
                    <input type="hidden" name="new_name" id="update-new-name" value="">
                </form>
                <form method="POST" id="update-sponsor-form" class="hidden">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="update_segment_sponsor">
                    <input type="hidden" name="segment_id" id="update-sponsor-seg-id" value="">
                    <input type="hidden" name="sponsor_id" id="update-sponsor-id" value="">
                </form>
            </div>
        </div>
        <?php endif; ?>

        <!-- POIs -->
        <div class="admin-card admin-card-compact">
            <div class="admin-card-header">
                <h2>POIs (<?= count($pois) ?>)</h2>
            </div>
            <div class="admin-card-body">
                <?php if (!empty($pois)): ?>
                <div class="admin-list admin-list-compact">
                    <?php foreach ($pois as $poi): ?>
                    <div class="admin-list-item">
                        <i data-lucide="<?= htmlspecialchars($poi['type_icon'] ?? 'map-pin') ?>" class="icon-xs"></i>
                        <span class="admin-list-item-text"><?= htmlspecialchars($poi['label'] ?: $poi['type_label'] ?? $poi['poi_type']) ?></span>
                        <form method="POST" class="inline-form">
                            <?= csrf_field() ?>
                            <input type="hidden" name="action" value="delete_poi">
                            <input type="hidden" name="poi_id" value="<?= $poi['id'] ?>">
                            <button type="submit" class="btn-admin btn-admin-ghost btn-admin-xs btn-admin-danger" onclick="return confirm('Ta bort?')">×</button>
                        </form>
                    </div>
                    <?php endforeach; ?>
                </div>
                <?php endif; ?>

                <details class="admin-details">
                    <summary>+ Lägg till POI</summary>
                    <form method="POST" id="poi-form" class="admin-form-compact">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="add_poi">
                        <input type="hidden" name="poi_lat" id="poi-lat">
                        <input type="hidden" name="poi_lng" id="poi-lng">
                        <div class="admin-form-row">
                            <select name="poi_type" class="admin-form-select admin-form-select-sm" required>
                                <option value="">Typ...</option>
                                <?php foreach ($poiTypes as $key => $label): ?>
                                <option value="<?= htmlspecialchars($key) ?>"><?= htmlspecialchars($label) ?></option>
                                <?php endforeach; ?>
                            </select>
                            <input type="text" name="poi_label" class="admin-form-input admin-form-input-sm" placeholder="Etikett">
                        </div>
                        <p class="admin-text-muted admin-text-sm">Klicka på kartan för position</p>
                        <button type="submit" id="poi-btn" disabled class="btn-admin btn-admin-primary btn-admin-sm btn-admin-block">Lägg till</button>
                    </form>
                </details>
            </div>
        </div>
    </div>

    <!-- Main: Map -->
    <div class="admin-main-content">
        <!-- Sponsor Banner (shown when segment with sponsor is selected) -->
        <div id="sponsor-banner" class="sponsor-banner" class="hidden">
            <div class="sponsor-banner-content">
                <span class="sponsor-banner-label">Sponsrad av</span>
                <img id="sponsor-banner-logo" src="" alt="" class="sponsor-banner-logo">
                <span id="sponsor-banner-name" class="sponsor-banner-name"></span>
            </div>
        </div>

        <div class="admin-card">
            <div class="admin-card-body p-0" style="position: relative;">
                <!-- Segment info overlay (mobile) -->
                <div id="segment-info-overlay" class="segment-info-overlay" class="hidden">
                    <div class="segment-info-content">
                        <i data-lucide="flag" id="segment-info-icon"></i>
                        <span id="segment-info-name"></span>
                        <span id="segment-info-distance" class="segment-info-distance"></span>
                    </div>
                </div>
                <div id="map" style="height: calc(100vh - 280px); min-height: 500px;"></div>
            </div>
        </div>
    </div>
</div>

<style>
/* Compact map editor styles */
.admin-grid-sidebar {
    display: grid;
    grid-template-columns: 400px 1fr;
    gap: var(--space-lg);
}
.admin-sidebar-narrow {
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
}
.admin-card-compact .admin-card-header {
    padding: var(--space-sm) var(--space-md);
}
.admin-card-compact .admin-card-header h2 {
    font-size: var(--text-sm);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}
.admin-card-compact .admin-card-body {
    padding: var(--space-md);
}
.color-dot {
    width: 10px;
    height: 10px;
    border-radius: 2px;
    flex-shrink: 0;
}
.admin-list-compact {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
    margin-bottom: var(--space-md);
}
.admin-list-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-xs) var(--space-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
}
.admin-list-item.active {
    border-color: var(--color-accent);
    background: rgba(97, 206, 112, 0.1);
}
.admin-list-item-text {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.admin-details {
    margin-top: var(--space-sm);
}
.admin-details summary {
    cursor: pointer;
    color: var(--color-accent);
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
}
.admin-details[open] summary {
    margin-bottom: var(--space-sm);
}
.admin-form-compact .admin-form-group {
    margin-bottom: var(--space-sm);
}
.admin-form-row {
    display: flex;
    gap: var(--space-sm);
    align-items: center;
    margin-bottom: var(--space-sm);
}
.admin-form-input-sm,
.admin-form-select-sm {
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--text-sm);
}
.admin-form-select-xs {
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--text-sm);
    border-radius: var(--radius-sm);
    min-width: 90px;
}
.segment-type-select {
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--text-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: white;
    min-width: 90px;
}
.admin-checkbox-inline {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: var(--text-sm);
    white-space: nowrap;
}
.btn-admin-block {
    width: 100%;
}
.btn-admin-xs {
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--text-sm);
}
.inline-form {
    display: inline;
    margin: 0;
}
.admin-status-box {
    padding: var(--space-xs) var(--space-sm);
    background: var(--color-bg-sunken);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
    margin-bottom: var(--space-sm);
}
.admin-info-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-xs) var(--space-sm);
    background: rgba(59, 130, 246, 0.1);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
    margin-bottom: var(--space-sm);
}
.segment-type-select {
    padding: 2px 4px;
    font-size: var(--text-xs);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: white;
}
.admin-pending-box {
    padding: var(--space-sm);
    background: rgba(59, 130, 246, 0.1);
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-sm);
}
.admin-pending-box span {
    display: block;
    font-size: var(--text-sm);
    margin-bottom: var(--space-xs);
}
.admin-btn-group {
    display: flex;
    gap: var(--space-xs);
}
.admin-segment-list {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
}
.admin-segment-item {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-md);
    border-bottom: 1px solid var(--color-border);
    font-size: var(--text-sm);
    transition: background-color 0.15s ease;
}
.admin-segment-item:hover {
    background-color: var(--color-star-fade);
}
.admin-segment-item:last-child {
    border-bottom: none;
}
.admin-segment-item.has-sponsor {
    background: rgba(97, 206, 112, 0.05);
}
.segment-sponsor-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-xs) var(--space-sm);
    background: var(--color-star-fade);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    white-space: nowrap;
}
.sponsor-by {
    color: var(--color-text);
    font-style: italic;
}
.sponsor-logo-mini {
    height: 14px;
    width: auto;
    max-width: 40px;
    object-fit: contain;
}
.sponsor-name-mini {
    font-weight: var(--weight-medium);
    color: var(--color-primary);
    max-width: 60px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.admin-segment-name {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}
.admin-segment-name svg {
    flex-shrink: 0;
}
.admin-text-sm {
    font-size: var(--text-sm);
}
.admin-text-xs {
    font-size: var(--text-xs);
}
.admin-segment-name-input {
    flex: 1;
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--text-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    min-width: 100px;
    max-width: 160px;
}
.admin-segment-name-input:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 2px rgba(97, 206, 112, 0.15);
}

/* Sponsor Banner */
.sponsor-banner {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    color: white;
    padding: var(--space-sm) var(--space-md);
    margin-bottom: var(--space-sm);
    border-radius: var(--radius-md);
    animation: slideDown 0.3s ease;
}
@keyframes slideDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
.sponsor-banner-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-md);
}
.sponsor-banner-label {
    font-size: var(--text-sm);
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.sponsor-banner-logo {
    height: 32px;
    width: auto;
    max-width: 120px;
    object-fit: contain;
    background: white;
    padding: 4px 8px;
    border-radius: var(--radius-sm);
}
.sponsor-banner-name {
    font-weight: var(--weight-semibold);
    font-size: var(--text-base);
}

/* Segment Info Overlay (on map) */
.segment-info-overlay {
    position: absolute;
    top: var(--space-sm);
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    background: rgba(23, 23, 23, 0.9);
    color: white;
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-md);
    backdrop-filter: blur(4px);
    animation: fadeIn 0.2s ease;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.segment-info-content {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
}
.segment-info-content svg {
    width: 16px;
    height: 16px;
}
.segment-info-distance {
    opacity: 0.7;
    font-weight: normal;
}
.segment-distance {
    font-weight: var(--weight-medium);
    color: var(--color-text-secondary);
    white-space: nowrap;
}

/* Selected segment in list */
.admin-segment-item.selected {
    background: rgba(97, 206, 112, 0.15) !important;
    border-left: 3px solid var(--color-accent);
    border-radius: var(--radius-sm);
}
.admin-segment-item.selected .admin-text-muted {
    color: var(--color-text-secondary);
}
.admin-segment-item.selected .color-dot {
    box-shadow: 0 0 0 2px var(--color-accent);
}

/* Tablet responsive */
@media (max-width: 1024px) {
    .admin-grid-sidebar {
        grid-template-columns: 350px 1fr;
    }
}

/* Mobile responsive */
@media (max-width: 768px) {
    .admin-grid-sidebar {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }
    .admin-sidebar-narrow {
        order: 2;
    }
    .admin-main-content {
        order: 1;
    }
    #map {
        height: 50vh !important;
        min-height: 300px !important;
    }
    .admin-segment-item {
        flex-wrap: wrap;
        gap: var(--space-sm);
        padding: var(--space-md);
    }
    .admin-segment-item.selected {
        margin: 0;
        padding-left: calc(var(--space-md) - 3px);
    }
    .admin-segment-name {
        width: 100%;
        order: 1;
    }
    .admin-segment-name-input {
        max-width: none;
        flex: 1;
    }
    .segment-distance {
        display: block;
    }
    .sponsor-banner {
        margin: 0 calc(var(--space-md) * -1) var(--space-sm);
        border-radius: 0;
    }
    .sponsor-banner-logo {
        height: 28px;
    }
}
</style>

<!-- Elevation Profile -->
<?php if ($currentTrack): ?>
<div class="admin-card mt-lg" id="elevation-card">
    <div class="admin-card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <h2 id="elevation-title">Höjdprofil</h2>
        <button type="button" onclick="showFullTrack()" class="btn btn-ghost btn-sm" style="display: flex; align-items: center; gap: var(--space-xs);">
            <i data-lucide="maximize-2" class="icon-xs"></i>
            Visa hela
        </button>
    </div>
    <div class="admin-card-body" style="padding: var(--space-sm);">
        <canvas id="elevation-canvas" style="width: 100%; height: 150px; display: block;"></canvas>
    </div>
</div>
<?php endif; ?>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script>
const mapData = <?= json_encode($mapData) ?>;
const waypoints = <?= json_encode($trackWaypoints) ?>;
const currentTrackId = <?= $selectedTrackId ?: 'null' ?>;
const savedSegments = <?= json_encode($currentTrack['segments'] ?? []) ?>;
console.log('EVENT-MAP DEBUG:', {
    waypointsCount: waypoints?.length || 0,
    currentTrackId: currentTrackId,
    hasMapData: !!mapData,
    tracksCount: mapData?.tracks?.length || 0,
    savedSegmentsCount: savedSegments?.length || 0
});
let map, baseTrackLine, tempMarker;
let highlightedSegmentLine = null;
let startMarker = null;
let finishMarker = null;
let selectedSegmentIdx = null;

// Segment colors
const SEGMENT_COLORS = {
    stage: '#EF4444',    // Red
    liaison: '#61CE70',  // Green
    lift: '#F59E0B'      // Orange/Yellow
};

// Multi-point editor state
let splitMarkers = [];      // Array of {marker, index, id}
let segmentLines = [];      // Array of polylines between markers
let segmentTypes = [];      // Array of segment types (liaison/stage/lift)
let segmentBounds = [];     // Array of bounds for each segment (for zoom)

// Icon SVGs for segment types (no emojis!)
const SEGMENT_ICONS = {
    liaison: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="5" r="3"/><path d="M12 8v4"/><path d="m5 21 7-4 7 4"/><path d="M12 12v5"/></svg>',
    stage: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/></svg>',
    lift: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16"/><path d="M6 4v16"/><path d="M18 4v16"/><rect x="8" y="8" width="8" height="6" rx="1"/></svg>'
};

function init() {
    map = L.map('map').setView([62, 15], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    if (mapData && mapData.tracks) {
        mapData.tracks.forEach(track => {
            if (track.geojson && track.geojson.features) {
                track.geojson.features.forEach(feature => {
                    const props = feature.properties;
                    const isBase = props.type === 'base_track';
                    const isCurrent = track.id === currentTrackId;
                    L.geoJSON(feature, {
                        style: () => ({
                            color: props.color || track.color,
                            weight: isBase ? 4 : 6,
                            opacity: isCurrent ? (isBase ? 0.6 : 1) : 0.4
                        })
                    }).addTo(map);
                });
            }
        });

        if (mapData.pois) {
            mapData.pois.forEach(p => {
                L.marker([p.lat, p.lng])
                    .bindPopup(p.label || p.type_label || p.poi_type)
                    .addTo(map);
            });
        }

        if (mapData.bounds) map.fitBounds(mapData.bounds, {padding: [30, 30]});
    }

    // Draw invisible clickable track for segment selection (wide hit area)
    if (waypoints && waypoints.length) {
        const coords = waypoints.map(w => [w.lat, w.lng]);
        baseTrackLine = L.polyline(coords, {
            color: 'transparent',
            weight: 20,  // Wide for easy clicking
            opacity: 0,
            className: 'clickable-track'
        }).addTo(map);
        baseTrackLine.on('click', onTrackClick);
    }

    map.on('click', onMapClick);
}

// Handle click on track - add a split point
function onTrackClick(e) {
    L.DomEvent.stopPropagation(e);
    const nearest = findNearest(e.latlng);
    if (!nearest) return;

    // Check if there's already a marker very close to this index
    const existingIdx = splitMarkers.findIndex(m => Math.abs(m.index - nearest.index) < 20);
    if (existingIdx >= 0) {
        // Remove that marker instead of adding new
        removeMarker(existingIdx);
        return;
    }

    // Add new split marker
    addMarker(nearest.index, nearest.wp);
}

function addMarker(index, wp) {
    const markerId = Date.now();

    const marker = L.marker([wp.lat, wp.lng], {
        draggable: true,
        icon: L.divIcon({
            className: 'split-marker',
            html: `<div style="width: 24px; height: 24px; background: #3B82F6; border: 3px solid white; border-radius: 50%; box-shadow: 0 2px 8px rgba(0,0,0,0.4); cursor: grab; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: bold;">${splitMarkers.length + 1}</div>`,
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        })
    }).addTo(map);

    marker.on('drag', (e) => onMarkerDrag(markerId, e));
    marker.on('dragend', (e) => onMarkerDragEnd(markerId, e));

    // Insert marker in sorted position
    const newMarker = { marker, index, id: markerId };
    splitMarkers.push(newMarker);
    splitMarkers.sort((a, b) => a.index - b.index);

    // Default type for new segment is liaison
    updateSegmentTypes();
    updateUI();
    drawSegmentLines();
}

function removeMarker(idx) {
    const m = splitMarkers[idx];
    if (m) {
        map.removeLayer(m.marker);
        splitMarkers.splice(idx, 1);
    }
    updateSegmentTypes();
    updateUI();
    drawSegmentLines();
    updateMarkerNumbers();
}

function updateMarkerNumbers() {
    splitMarkers.forEach((m, i) => {
        const el = m.marker.getElement();
        if (el) {
            const div = el.querySelector('div');
            if (div) div.textContent = i + 1;
        }
    });
}

function onMarkerDrag(markerId, e) {
    const nearest = findNearest(e.latlng);
    if (nearest) {
        const idx = splitMarkers.findIndex(m => m.id === markerId);
        if (idx >= 0) {
            // Check bounds - can't go past neighbors
            const prevIdx = idx > 0 ? splitMarkers[idx - 1].index : -1;
            const nextIdx = idx < splitMarkers.length - 1 ? splitMarkers[idx + 1].index : waypoints.length;

            if (nearest.index > prevIdx && nearest.index < nextIdx) {
                splitMarkers[idx].index = nearest.index;
                drawSegmentLines();
                updateSegmentListDistances();
            }
        }
    }
}

function onMarkerDragEnd(markerId, e) {
    const nearest = findNearest(e.target.getLatLng());
    const idx = splitMarkers.findIndex(m => m.id === markerId);

    if (nearest && idx >= 0) {
        const prevIdx = idx > 0 ? splitMarkers[idx - 1].index : -1;
        const nextIdx = idx < splitMarkers.length - 1 ? splitMarkers[idx + 1].index : waypoints.length;

        if (nearest.index > prevIdx && nearest.index < nextIdx) {
            splitMarkers[idx].index = nearest.index;
            splitMarkers[idx].marker.setLatLng([nearest.wp.lat, nearest.wp.lng]);
        } else {
            // Snap back to previous valid position
            const wp = waypoints[splitMarkers[idx].index];
            splitMarkers[idx].marker.setLatLng([wp.lat, wp.lng]);
        }
    }
    drawSegmentLines();
    updateUI();
}

function updateSegmentTypes() {
    // Ensure we have the right number of segment types
    const numSegments = splitMarkers.length + 1; // segments = markers + 1
    while (segmentTypes.length < numSegments) {
        segmentTypes.push('liaison'); // Default to transport
    }
    while (segmentTypes.length > numSegments) {
        segmentTypes.pop();
    }
}

function drawSegmentLines() {
    // Remove old lines
    segmentLines.forEach(line => map.removeLayer(line));
    segmentLines = [];
    segmentBounds = [];

    if (splitMarkers.length === 0) return;

    // Build segment ranges
    const ranges = [];
    let start = 0;

    for (let i = 0; i <= splitMarkers.length; i++) {
        const end = i < splitMarkers.length ? splitMarkers[i].index : waypoints.length - 1;
        const type = segmentTypes[i] || 'liaison';

        if (end > start) {
            const coords = waypoints.slice(start, end + 1).map(w => [w.lat, w.lng]);
            const line = L.polyline(coords, {
                color: SEGMENT_COLORS[type],
                weight: 6,
                opacity: 0.9,
                interactive: false  // Let clicks pass through to base track
            }).addTo(map);
            segmentLines.push(line);
            segmentBounds.push(L.latLngBounds(coords));
            ranges.push({ start, end, type });
        }

        start = end;
    }
}

function updateUI() {
    const markersInfo = document.getElementById('markers-info');
    const segmentsList = document.getElementById('segments-list');
    const saveActions = document.getElementById('save-actions');
    const statusBox = document.getElementById('segment-status');

    if (splitMarkers.length === 0) {
        markersInfo.style.display = 'none';
        saveActions.style.display = 'none';
        segmentsList.innerHTML = '<p class="admin-text-muted admin-text-sm">Sätt ut minst 1 punkt för att skapa sektioner</p>';
        statusBox.innerHTML = '<strong>Steg 1:</strong> Klicka på banan för att sätta ut delningspunkter';
        return;
    }

    markersInfo.style.display = 'flex';
    document.getElementById('markers-count').textContent = splitMarkers.length + ' punkt' + (splitMarkers.length > 1 ? 'er' : '');

    // Build segment list
    let html = '';
    let start = 0;

    for (let i = 0; i <= splitMarkers.length; i++) {
        const end = i < splitMarkers.length ? splitMarkers[i].index : waypoints.length - 1;
        const type = segmentTypes[i] || 'liaison';
        const dist = (waypoints[end].distance_km - waypoints[start].distance_km).toFixed(1);

        html += `
        <div class="admin-segment-item" data-segment-idx="${i}" onclick="zoomToSegment(${i})" style="cursor: pointer;">
            <span class="color-dot" style="background: ${SEGMENT_COLORS[type]};"></span>
            <span class="admin-segment-name">${SEGMENT_ICONS[type]} Sektion ${i + 1}</span>
            <span class="admin-text-muted">${dist}km</span>
            <select onclick="event.stopPropagation()" onchange="changeType(${i}, this.value)" class="segment-type-select">
                <option value="liaison" ${type === 'liaison' ? 'selected' : ''}>Transport</option>
                <option value="stage" ${type === 'stage' ? 'selected' : ''}>Sträcka</option>
                <option value="lift" ${type === 'lift' ? 'selected' : ''}>Lift</option>
            </select>
        </div>`;

        start = end;
    }

    segmentsList.innerHTML = html;
    saveActions.style.display = 'block';
    statusBox.innerHTML = '<strong>Steg 2:</strong> Välj typ för varje sektion, sen spara';
}

function zoomToSegment(idx) {
    if (segmentBounds[idx]) {
        map.fitBounds(segmentBounds[idx], { padding: [50, 50] });

        // Update elevation profile for this segment
        let start = 0;
        for (let i = 0; i < idx; i++) {
            start = splitMarkers[i].index;
        }
        const end = idx < splitMarkers.length ? splitMarkers[idx].index : waypoints.length - 1;
        const type = segmentTypes[idx] || 'liaison';
        const typeLabel = type === 'stage' ? 'SS' : (type === 'lift' ? 'Lift' : 'Transport');
        drawElevationProfile(start, end, `Sektion ${idx + 1} (${typeLabel})`);

        // Highlight selected segment in list
        document.querySelectorAll('.admin-segment-item').forEach((item, i) => {
            item.style.background = i === idx ? 'var(--color-star-fade)' : '';
        });
    }
}

function showFullTrack() {
    // Zoom to full track
    if (baseTrackLine) {
        map.fitBounds(baseTrackLine.getBounds(), { padding: [50, 50] });
    }
    // Show full elevation profile
    drawElevationProfile(0, null, 'Hela banan');
    // Clear selection
    clearSegmentSelection();
}

// Clear segment selection UI
function clearSegmentSelection() {
    selectedSegmentIdx = null;
    // Remove highlight from list
    document.querySelectorAll('.admin-segment-item').forEach(item => {
        item.classList.remove('selected');
    });
    // Hide sponsor banner
    document.getElementById('sponsor-banner').style.display = 'none';
    // Hide segment info overlay
    document.getElementById('segment-info-overlay').style.display = 'none';
    // Remove highlighted line
    if (highlightedSegmentLine) {
        map.removeLayer(highlightedSegmentLine);
        highlightedSegmentLine = null;
    }
    // Remove start/finish markers
    if (startMarker) {
        map.removeLayer(startMarker);
        startMarker = null;
    }
    if (finishMarker) {
        map.removeLayer(finishMarker);
        finishMarker = null;
    }
}

// Select a segment - show sponsor banner, highlight on map, show start/finish
function selectSegment(segIdx, startIdx, endIdx) {
    if (!waypoints || waypoints.length < 2) return;
    if (!savedSegments || !savedSegments[segIdx]) return;

    const segment = savedSegments[segIdx];
    console.log('selectSegment:', { segIdx, segment });

    // Clear previous selection
    clearSegmentSelection();
    selectedSegmentIdx = segIdx;

    // Validate indices
    startIdx = Math.max(0, Math.min(startIdx, waypoints.length - 1));
    endIdx = Math.max(0, Math.min(endIdx, waypoints.length - 1));
    if (startIdx >= endIdx) return;

    // Highlight in list
    document.querySelectorAll('.admin-existing-segments .admin-segment-item').forEach((item, idx) => {
        if (idx === segIdx) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });

    // Show sponsor banner if segment has sponsor
    if (segment.sponsor_name) {
        const banner = document.getElementById('sponsor-banner');
        const logoEl = document.getElementById('sponsor-banner-logo');
        const nameEl = document.getElementById('sponsor-banner-name');

        if (segment.sponsor_logo) {
            logoEl.src = segment.sponsor_logo;
            logoEl.alt = segment.sponsor_name;
            logoEl.style.display = 'block';
            nameEl.style.display = 'none';
        } else {
            logoEl.style.display = 'none';
            nameEl.textContent = segment.sponsor_name;
            nameEl.style.display = 'block';
        }
        banner.style.display = 'block';
    }

    // Show segment info overlay
    const overlay = document.getElementById('segment-info-overlay');
    const typeLabels = { stage: 'SS', liaison: 'Transport', lift: 'Lift' };
    const segName = segment.segment_name || ('Sektion ' + (segIdx + 1));
    const typeLabel = typeLabels[segment.segment_type] || 'SS';
    document.getElementById('segment-info-name').textContent = segName;
    document.getElementById('segment-info-distance').textContent = parseFloat(segment.distance_km).toFixed(1) + ' km';
    overlay.style.display = 'block';

    // Get segment waypoints
    const segWaypoints = waypoints.slice(startIdx, endIdx + 1);
    if (segWaypoints.length < 2) return;

    // Create highlighted polyline (thicker, with glow effect)
    const latlngs = segWaypoints.map(w => [w.lat, w.lng]);
    highlightedSegmentLine = L.polyline(latlngs, {
        color: segment.color || '#EF4444',
        weight: 8,
        opacity: 1,
        lineCap: 'round',
        lineJoin: 'round'
    }).addTo(map);

    // Add start marker (green circle)
    const startPoint = segWaypoints[0];
    startMarker = L.circleMarker([startPoint.lat, startPoint.lng], {
        radius: 10,
        fillColor: '#22C55E',
        fillOpacity: 1,
        color: '#fff',
        weight: 3
    }).addTo(map).bindTooltip('Start', { permanent: false, direction: 'top' });

    // Add finish marker (checkered flag style - red circle)
    const endPoint = segWaypoints[segWaypoints.length - 1];
    finishMarker = L.circleMarker([endPoint.lat, endPoint.lng], {
        radius: 10,
        fillColor: '#EF4444',
        fillOpacity: 1,
        color: '#fff',
        weight: 3
    }).addTo(map).bindTooltip('Mål', { permanent: false, direction: 'top' });

    // Calculate bounds and zoom
    const lats = segWaypoints.map(w => w.lat);
    const lngs = segWaypoints.map(w => w.lng);
    const bounds = L.latLngBounds(
        [Math.min(...lats), Math.min(...lngs)],
        [Math.max(...lats), Math.max(...lngs)]
    );
    map.fitBounds(bounds, { padding: [60, 60] });

    // Draw elevation profile
    drawElevationProfile(startIdx, endIdx, segName);
}

// Zoom to an existing/saved segment using start/end waypoint indices (legacy, now calls selectSegment)
function zoomToExistingSegment(startIdx, endIdx, title) {
    console.log('zoomToExistingSegment called:', {startIdx, endIdx, title, waypointsLength: waypoints?.length});
    if (!waypoints || waypoints.length < 2) {
        console.log('No waypoints available');
        return;
    }

    // Validate indices
    startIdx = Math.max(0, Math.min(startIdx, waypoints.length - 1));
    endIdx = Math.max(0, Math.min(endIdx, waypoints.length - 1));
    if (startIdx >= endIdx) return;

    // Calculate bounds from waypoints in this segment
    const segWaypoints = waypoints.slice(startIdx, endIdx + 1);
    if (segWaypoints.length < 2) return;

    const lats = segWaypoints.map(w => w.lat);
    const lngs = segWaypoints.map(w => w.lng);
    const bounds = L.latLngBounds(
        [Math.min(...lats), Math.min(...lngs)],
        [Math.max(...lats), Math.max(...lngs)]
    );

    // Zoom map to segment
    map.fitBounds(bounds, { padding: [50, 50] });

    // Draw elevation profile for this segment
    drawElevationProfile(startIdx, endIdx, title || 'Sektion');

    // Highlight selected segment in list (for existing segments only)
    document.querySelectorAll('.admin-existing-segments .admin-segment-item').forEach(item => {
        const itemStart = parseInt(item.dataset.start || '0');
        const itemEnd = parseInt(item.dataset.end || '0');
        if (itemStart === startIdx && itemEnd === endIdx) {
            item.style.background = 'var(--color-star-fade)';
        } else {
            item.style.background = '';
        }
    });
}

function updateSegmentListDistances() {
    // Quick update of distances during drag
    let start = 0;
    const items = document.querySelectorAll('[data-segment-idx]');

    items.forEach((item, i) => {
        const end = i < splitMarkers.length ? splitMarkers[i].index : waypoints.length - 1;
        const dist = (waypoints[end].distance_km - waypoints[start].distance_km).toFixed(1);
        const distSpan = item.querySelector('.admin-text-muted');
        if (distSpan) distSpan.textContent = dist + 'km';
        start = end;
    });
}

function changeType(segIdx, newType) {
    segmentTypes[segIdx] = newType;
    drawSegmentLines();
    updateUI();
}

function clearAllMarkers() {
    if (!confirm('Ta bort alla punkter?')) return;
    splitMarkers.forEach(m => map.removeLayer(m.marker));
    splitMarkers = [];
    segmentTypes = [];
    drawSegmentLines();
    updateUI();
}

function saveAllSegments() {
    if (splitMarkers.length === 0) {
        alert('Sätt ut minst en punkt först');
        return;
    }

    // Build segments data
    const segments = [];
    let start = 0;

    for (let i = 0; i <= splitMarkers.length; i++) {
        const end = i < splitMarkers.length ? splitMarkers[i].index : waypoints.length - 1;
        const type = segmentTypes[i] || 'liaison';

        if (end > start) {
            segments.push({ start, end, type });
        }
        start = end;
    }

    document.getElementById('segments-data').value = JSON.stringify(segments);
    document.getElementById('save-segments-form').submit();
}

function editExistingSegments() {
    // Load existing segments into the editor
    <?php if ($currentTrack && !empty($currentTrack['segments'])): ?>
    const existingSegments = <?= json_encode(array_map(function($s) {
        return [
            'start' => $s['start_index'] ?? 0,
            'end' => $s['end_index'] ?? 0,
            'type' => $s['segment_type'] ?? 'liaison'
        ];
    }, $currentTrack['segments'])) ?>;

    // Clear current markers
    splitMarkers.forEach(m => map.removeLayer(m.marker));
    splitMarkers = [];
    segmentTypes = [];

    // Add markers at each split point (end of each segment except last)
    existingSegments.forEach((seg, i) => {
        if (i < existingSegments.length - 1 && seg.end > 0 && seg.end < waypoints.length) {
            const wp = waypoints[seg.end];
            if (wp) addMarker(seg.end, wp);
        }
        segmentTypes.push(seg.type);
    });

    updateUI();
    drawSegmentLines();
    <?php endif; ?>
}

function onMapClick(e) {
    const poiLat = document.getElementById('poi-lat');
    const poiLng = document.getElementById('poi-lng');
    const poiBtn = document.getElementById('poi-btn');

    if (poiLat && poiLng && poiBtn) {
        poiLat.value = e.latlng.lat;
        poiLng.value = e.latlng.lng;
        poiBtn.disabled = false;
        if (tempMarker) map.removeLayer(tempMarker);
        tempMarker = L.circleMarker(e.latlng, {radius: 6, color: '#3B82F6', fillOpacity: 1}).addTo(map);
    }
}

function findNearest(latlng) {
    if (!waypoints || !waypoints.length) return null;
    let best = {dist: Infinity};
    waypoints.forEach((wp, i) => {
        const d = latlng.distanceTo(L.latLng(wp.lat, wp.lng));
        if (d < best.dist) best = {index: i, wp: wp, dist: d};
    });
    return best.dist < 300 ? best : null;
}

function changeSegmentType(segId, newType) {
    document.getElementById('update-seg-id').value = segId;
    document.getElementById('update-new-type').value = newType;
    document.getElementById('update-type-form').submit();
}

function changeSegmentName(segId, newName) {
    document.getElementById('update-name-seg-id').value = segId;
    document.getElementById('update-new-name').value = newName;
    document.getElementById('update-name-form').submit();
}

function changeSegmentSponsor(segId, sponsorId) {
    document.getElementById('update-sponsor-seg-id').value = segId;
    document.getElementById('update-sponsor-id').value = sponsorId;
    document.getElementById('update-sponsor-form').submit();
}

// Elevation profile rendering
function drawElevationProfile(startIdx = 0, endIdx = null, title = 'Höjdprofil') {
    const canvas = document.getElementById('elevation-canvas');
    if (!canvas || !waypoints || waypoints.length < 2) return;

    // Update title in header
    const headerTitle = document.getElementById('elevation-title');
    if (headerTitle) headerTitle.textContent = title;

    // Slice waypoints if filtering to a section
    const wps = endIdx !== null ? waypoints.slice(startIdx, endIdx + 1) : waypoints;
    if (wps.length < 2) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    // Set canvas size based on container
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width;
    const height = rect.height;
    const padding = { top: 20, right: 20, bottom: 30, left: 50 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    // Extract elevation data
    const elevations = wps.map(w => w.elevation || 0);
    const distances = wps.map(w => w.distance_km || 0);
    const baseDistance = distances[0];

    if (elevations.every(e => e === 0)) {
        // No elevation data available
        ctx.fillStyle = '#7A7A7A';
        ctx.font = '12px system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Ingen höjddata tillgänglig', width / 2, height / 2);
        return;
    }

    const minEle = Math.min(...elevations);
    const maxEle = Math.max(...elevations);
    const eleRange = maxEle - minEle || 100;
    const minDist = distances[0];
    const maxDist = distances[distances.length - 1];
    const distRange = maxDist - minDist || 1;

    // Clear canvas
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, width, height);

    // Draw grid lines
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = padding.top + (chartHeight * i / 4);
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(width - padding.right, y);
        ctx.stroke();
    }

    // Draw elevation profile with gradient fill
    ctx.beginPath();
    ctx.moveTo(padding.left, padding.top + chartHeight);

    wps.forEach((wp, i) => {
        const x = padding.left + ((distances[i] - minDist) / distRange) * chartWidth;
        const y = padding.top + chartHeight - ((elevations[i] - minEle) / eleRange) * chartHeight;
        ctx.lineTo(x, y);
    });

    ctx.lineTo(padding.left + chartWidth, padding.top + chartHeight);
    ctx.closePath();

    // Gradient fill
    const gradient = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartHeight);
    gradient.addColorStop(0, 'rgba(97, 206, 112, 0.6)');
    gradient.addColorStop(1, 'rgba(97, 206, 112, 0.1)');
    ctx.fillStyle = gradient;
    ctx.fill();

    // Draw elevation line on top
    ctx.beginPath();
    wps.forEach((wp, i) => {
        const x = padding.left + ((distances[i] - minDist) / distRange) * chartWidth;
        const y = padding.top + chartHeight - ((elevations[i] - minEle) / eleRange) * chartHeight;
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.strokeStyle = '#61CE70';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw Y-axis labels (elevation)
    ctx.fillStyle = '#7A7A7A';
    ctx.font = '10px system-ui, sans-serif';
    ctx.textAlign = 'right';
    for (let i = 0; i <= 4; i++) {
        const ele = minEle + (eleRange * (4 - i) / 4);
        const y = padding.top + (chartHeight * i / 4);
        ctx.fillText(Math.round(ele) + 'm', padding.left - 5, y + 3);
    }

    // Draw X-axis labels (distance)
    ctx.textAlign = 'center';
    for (let i = 0; i <= 4; i++) {
        const dist = (maxDist * i / 4).toFixed(1);
        const x = padding.left + (chartWidth * i / 4);
        ctx.fillText(dist + 'km', x, height - 10);
    }

    // Draw stats
    const totalClimb = calculateClimb(elevations);
    ctx.fillStyle = '#171717';
    ctx.font = '11px system-ui, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`↑ ${Math.round(totalClimb)}m höjdmeter`, padding.left, 12);
    ctx.textAlign = 'right';
    ctx.fillText(`${Math.round(minEle)}m - ${Math.round(maxEle)}m`, width - padding.right, 12);
}

function calculateClimb(elevations) {
    let climb = 0;
    for (let i = 1; i < elevations.length; i++) {
        const diff = elevations[i] - elevations[i - 1];
        if (diff > 0) climb += diff;
    }
    return climb;
}

document.addEventListener('DOMContentLoaded', () => {
    init();
    // Delay elevation profile to ensure canvas has proper dimensions
    setTimeout(() => drawElevationProfile(), 100);
});
window.addEventListener('resize', () => drawElevationProfile());
window.addEventListener('load', () => drawElevationProfile());
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
