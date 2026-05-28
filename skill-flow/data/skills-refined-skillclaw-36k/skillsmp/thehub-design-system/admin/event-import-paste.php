<?php
/**
 * Event Import - Paste Results
 * Quick import tool for pasting tab-separated results class by class
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/helpers.php';
require_once __DIR__ . '/../includes/club-matching.php';
require_once __DIR__ . '/../includes/club-membership.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

// Get event ID from URL
$eventId = (int)($_GET['event_id'] ?? 0);
if (!$eventId) {
    header('Location: /admin/events');
    exit;
}

// Get event info
$event = $db->getRow("SELECT * FROM events WHERE id = ?", [$eventId]);
if (!$event) {
    header('Location: /admin/events');
    exit;
}

$eventYear = (int)date('Y', strtotime($event['date']));

// Get existing classes for this event
$eventClasses = $db->getAll("
    SELECT DISTINCT c.id, c.display_name, c.name
    FROM classes c
    INNER JOIN results r ON r.class_id = c.id
    WHERE r.event_id = ?
    ORDER BY c.display_name
", [$eventId]);

// Get all available classes
$allClasses = $db->getAll("SELECT id, display_name, name FROM classes WHERE active = 1 ORDER BY display_name");

$message = '';
$messageType = 'info';
$stats = null;
$preview = null;

/**
 * Parse pasted data and extract results
 */
function parsePastedResults($text, $db) {
    $lines = preg_split('/\r?\n/', trim($text));
    $results = [];
    $errors = [];

    // Detect if first line is header
    $firstLine = strtolower($lines[0] ?? '');
    $hasHeader = (strpos($firstLine, 'plac') !== false ||
                  strpos($firstLine, 'startnr') !== false ||
                  strpos($firstLine, 'deltagare') !== false ||
                  strpos($firstLine, 'namn') !== false);

    $startLine = $hasHeader ? 1 : 0;

    for ($i = $startLine; $i < count($lines); $i++) {
        $line = trim($lines[$i]);
        if (empty($line)) continue;

        // Split by tab
        $cols = explode("\t", $line);

        // Need at least: position, startnr, name
        if (count($cols) < 3) {
            $errors[] = "Rad " . ($i + 1) . ": För få kolumner";
            continue;
        }

        // Parse position (can be DNS, DNF, DQ, or number)
        $posRaw = trim($cols[0]);
        $position = null;
        $status = 'finished';

        if (is_numeric($posRaw)) {
            $position = (int)$posRaw;
        } elseif (strtoupper($posRaw) === 'DNS') {
            $status = 'dns';
        } elseif (strtoupper($posRaw) === 'DNF') {
            $status = 'dnf';
        } elseif (strtoupper($posRaw) === 'DQ' || strtoupper($posRaw) === 'DSQ') {
            $status = 'dq';
        }

        // Parse bib number
        $bibNumber = trim($cols[1]);

        // Parse name - can be "Firstname LASTNAME" or "LASTNAME Firstname"
        $nameRaw = trim($cols[2]);
        $nameParts = preg_split('/\s+/', $nameRaw);

        // Detect format: if first word is ALL CAPS, it might be lastname first
        // Common format from timing: "Olof EKFJELL" (firstname + LASTNAME)
        $firstname = '';
        $lastname = '';

        if (count($nameParts) >= 2) {
            // Check if second part is uppercase (firstname + LASTNAME format)
            $lastPart = end($nameParts);
            if (preg_match('/^[A-ZÅÄÖ]+$/', $lastPart)) {
                // firstname + LASTNAME format
                $lastname = ucfirst(strtolower(array_pop($nameParts)));
                $firstname = implode(' ', array_map(function($p) {
                    return ucfirst(strtolower($p));
                }, $nameParts));
            } else {
                // Normal format or mixed
                $firstname = ucfirst(strtolower($nameParts[0]));
                $lastname = ucfirst(strtolower(implode(' ', array_slice($nameParts, 1))));
            }
        } else {
            $lastname = ucfirst(strtolower($nameRaw));
        }

        // UCI-ID (column 3)
        $uciId = isset($cols[3]) ? trim($cols[3]) : '';

        // Club (column 4)
        $clubName = isset($cols[4]) ? trim($cols[4]) : '';

        // Nationality (column 5) - extract 3-letter code
        $nationality = '';
        if (isset($cols[5])) {
            $natRaw = trim($cols[5]);
            // Extract 3-letter code from "Sverige SWE" or just "SWE"
            if (preg_match('/([A-Z]{3})/', $natRaw, $m)) {
                $nationality = $m[1];
            }
        }

        // Laps (column 6) - number of completed laps for XC
        $laps = null;
        if (isset($cols[6])) {
            $lapsRaw = trim($cols[6]);
            if (is_numeric($lapsRaw) && (int)$lapsRaw > 0) {
                $laps = (int)$lapsRaw;
            }
        }

        // Finish time (column 7)
        $finishTime = isset($cols[7]) ? trim($cols[7]) : '';
        // Clean up time - remove trailing stuff like "km/t"
        $finishTime = preg_replace('/\s+.*$/', '', $finishTime);
        if (empty($finishTime) || $finishTime === '-') {
            $finishTime = null;
        }

        // Lap/split times (columns 8+)
        $splitTimes = [];
        for ($s = 8; $s < min(count($cols), 24); $s++) {
            $splitTime = trim($cols[$s]);
            // Skip empty, speed columns, etc.
            if (empty($splitTime) || strpos($splitTime, 'km/t') !== false || $splitTime === '-') {
                continue;
            }
            // Only add if it looks like a time
            if (preg_match('/^\d+:\d+/', $splitTime) || preg_match('/^\d+\.\d+/', $splitTime)) {
                $splitTimes[] = $splitTime;
            }
        }

        $results[] = [
            'position' => $position,
            'status' => $status,
            'bib_number' => $bibNumber,
            'firstname' => $firstname,
            'lastname' => $lastname,
            'uci_id' => $uciId,
            'club_name' => $clubName,
            'nationality' => $nationality,
            'laps' => $laps,
            'finish_time' => $finishTime,
            'split_times' => $splitTimes
        ];
    }

    return ['results' => $results, 'errors' => $errors];
}

/**
 * Find or create rider
 */
function findOrCreateRider($db, $firstname, $lastname, $uciId, $nationality, $clubId) {
    // Normalize UCI ID
    $uciIdDigits = preg_replace('/[^0-9]/', '', $uciId);

    // Try UCI ID first
    if (!empty($uciIdDigits)) {
        $rider = $db->getRow(
            "SELECT id FROM riders WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?",
            [$uciIdDigits]
        );
        if ($rider) return $rider['id'];
    }

    // Try name match
    $rider = $db->getRow(
        "SELECT id FROM riders WHERE UPPER(firstname) = UPPER(?) AND UPPER(lastname) = UPPER(?)",
        [$firstname, $lastname]
    );
    if ($rider) {
        // Update UCI if missing
        if (!empty($uciId)) {
            $existing = $db->getRow("SELECT license_number FROM riders WHERE id = ?", [$rider['id']]);
            if (empty($existing['license_number'])) {
                $db->update('riders', ['license_number' => $uciId], 'id = ?', [$rider['id']]);
            }
        }
        return $rider['id'];
    }

    // Check if this name was previously merged (to prevent recreating deleted duplicates)
    try {
        $mergedRider = $db->getRow(
            "SELECT canonical_rider_id FROM rider_merge_map
             WHERE UPPER(merged_firstname) = UPPER(?) AND UPPER(merged_lastname) = UPPER(?)
             AND status = 'approved'",
            [$firstname, $lastname]
        );
        if ($mergedRider) {
            // This rider was previously merged - return the canonical rider instead
            return $mergedRider['canonical_rider_id'];
        }
    } catch (Exception $e) { /* Table might not exist yet */ }

    // Create new rider
    $licenseNumber = !empty($uciId) ? $uciId : generateSweId($db);

    $riderId = $db->insert('riders', [
        'firstname' => $firstname,
        'lastname' => $lastname,
        'license_number' => $licenseNumber,
        'nationality' => !empty($nationality) ? $nationality : null,
        'club_id' => $clubId,
        'gender' => 'M', // Default, will be corrected by class
        'active' => 1
    ]);

    return $riderId;
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? 'preview';
    $pastedData = $_POST['pasted_data'] ?? '';
    $classId = (int)($_POST['class_id'] ?? 0);
    $newClassName = trim($_POST['new_class_name'] ?? '');

    // Create new class if specified
    if (!$classId && !empty($newClassName)) {
        // Check if class exists
        $existingClass = $db->getRow(
            "SELECT id FROM classes WHERE LOWER(display_name) = LOWER(?) OR LOWER(name) = LOWER(?)",
            [$newClassName, $newClassName]
        );

        if ($existingClass) {
            $classId = $existingClass['id'];
        } else {
            $classId = $db->insert('classes', [
                'name' => strtolower(str_replace(' ', '_', $newClassName)),
                'display_name' => $newClassName,
                'active' => 1
            ]);
        }
    }

    if (empty($pastedData)) {
        $message = 'Ingen data inklistrad';
        $messageType = 'error';
    } elseif (!$classId) {
        $message = 'Välj eller skapa en klass';
        $messageType = 'error';
    } else {
        $parsed = parsePastedResults($pastedData, $db);

        if ($action === 'preview') {
            $preview = $parsed;
            $preview['class_id'] = $classId;

            // Get class name
            $classInfo = $db->getRow("SELECT display_name FROM classes WHERE id = ?", [$classId]);
            $preview['class_name'] = $classInfo['display_name'] ?? 'Okänd klass';

            // Look up existing riders for preview
            foreach ($preview['results'] as &$row) {
                $uciIdDigits = preg_replace('/[^0-9]/', '', $row['uci_id']);
                $found = false;

                if (!empty($uciIdDigits)) {
                    $rider = $db->getRow(
                        "SELECT id, firstname, lastname FROM riders WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?",
                        [$uciIdDigits]
                    );
                    if ($rider) {
                        $row['rider_id'] = $rider['id'];
                        $row['rider_match'] = 'UCI-ID';
                        $found = true;
                    }
                }

                if (!$found) {
                    $rider = $db->getRow(
                        "SELECT id FROM riders WHERE UPPER(firstname) = UPPER(?) AND UPPER(lastname) = UPPER(?)",
                        [$row['firstname'], $row['lastname']]
                    );
                    if ($rider) {
                        $row['rider_id'] = $rider['id'];
                        $row['rider_match'] = 'Namn';
                    } else {
                        $row['rider_id'] = null;
                        $row['rider_match'] = 'Ny';
                    }
                }
            }

        } else {
            // Do import
            $stats = [
                'total' => count($parsed['results']),
                'success' => 0,
                'updated' => 0,
                'failed' => 0,
                'riders_created' => 0,
                'clubs_created' => 0
            ];
            $errors = $parsed['errors'];

            foreach ($parsed['results'] as $row) {
                try {
                    // Find or create club
                    $clubId = null;
                    if (!empty($row['club_name'])) {
                        $club = findClubByName($db, $row['club_name']);
                        if ($club) {
                            $clubId = $club['id'];
                        } else {
                            $clubId = $db->insert('clubs', [
                                'name' => $row['club_name'],
                                'active' => 1
                            ]);
                            $stats['clubs_created']++;
                        }
                    }

                    // Find or create rider
                    $riderId = findOrCreateRider(
                        $db,
                        $row['firstname'],
                        $row['lastname'],
                        $row['uci_id'],
                        $row['nationality'],
                        $clubId
                    );

                    // Check if this is a new rider
                    static $existingRiderIds = null;
                    if ($existingRiderIds === null) {
                        $existingRiderIds = array_column($db->getAll("SELECT id FROM riders"), 'id');
                    }
                    if (!in_array($riderId, $existingRiderIds)) {
                        $stats['riders_created']++;
                        $existingRiderIds[] = $riderId;
                    }

                    // Update rider club for this year
                    if ($clubId) {
                        setRiderClubForYear($db, $riderId, $clubId, $eventYear);
                        lockRiderClubForYear($db, $riderId, $eventYear);
                        $db->update('riders', ['club_id' => $clubId], 'id = ?', [$riderId]);
                    }

                    // Check for existing result
                    $existingResult = $db->getRow(
                        "SELECT id FROM results WHERE event_id = ? AND cyclist_id = ? AND class_id = ?",
                        [$eventId, $riderId, $classId]
                    );

                    // Calculate points
                    $points = 0;
                    if ($row['status'] === 'finished' && $row['position']) {
                        $points = calculatePoints($db, $eventId, $row['position'], $row['status'], $classId);
                    }

                    // Prepare result data
                    $resultData = [
                        'event_id' => $eventId,
                        'cyclist_id' => $riderId,
                        'club_id' => $clubId,
                        'class_id' => $classId,
                        'bib_number' => $row['bib_number'],
                        'position' => $row['position'],
                        'finish_time' => $row['finish_time'],
                        'status' => $row['status'],
                        'laps' => $row['laps'],
                        'points' => $points
                    ];

                    // Add split times
                    foreach ($row['split_times'] as $idx => $time) {
                        $ssCol = 'ss' . ($idx + 1);
                        if ($idx < 15) { // ss1-ss15
                            $resultData[$ssCol] = $time;
                        }
                    }

                    if ($existingResult) {
                        $db->update('results', $resultData, 'id = ?', [$existingResult['id']]);
                        $stats['updated']++;
                    } else {
                        $db->insert('results', $resultData);
                        $stats['success']++;
                    }

                } catch (Exception $e) {
                    $stats['failed']++;
                    $errors[] = "{$row['firstname']} {$row['lastname']}: " . $e->getMessage();
                }
            }

            if ($stats['success'] > 0 || $stats['updated'] > 0) {
                $message = "Import klar! {$stats['success']} nya resultat, {$stats['updated']} uppdaterade.";
                if ($stats['riders_created'] > 0) {
                    $message .= " {$stats['riders_created']} nya åkare skapade.";
                }
                $messageType = 'success';
            } else {
                $message = "Ingen data importerades.";
                $messageType = 'warning';
            }

            if (!empty($errors)) {
                $message .= " " . count($errors) . " fel.";
            }
        }
    }
}

// Page config
$page_title = 'Importera resultat - ' . h($event['name']);
$breadcrumbs = [
    ['label' => 'Events', 'url' => '/admin/events'],
    ['label' => $event['name'], 'url' => '/admin/event/edit/' . $eventId],
    ['label' => 'Importera resultat']
];

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Message -->
<?php if ($message): ?>
<div class="alert alert-<?= h($messageType) ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Event Info -->
<div class="admin-card mb-lg">
    <div class="admin-card-body" style="display: flex; align-items: center; gap: var(--space-lg);">
        <div>
            <h2 style="margin: 0;"><?= h($event['name']) ?></h2>
            <p class="text-secondary" style="margin: var(--space-xs) 0 0 0;">
                <?= date('Y-m-d', strtotime($event['date'])) ?>
                <?php if ($event['location']): ?>
                    &bull; <?= h($event['location']) ?>
                <?php endif; ?>
            </p>
        </div>
        <?php if (!empty($eventClasses)): ?>
        <div class="text-secondary" style="margin-left: auto;">
            <i data-lucide="users"></i>
            <?= count($eventClasses) ?> klasser importerade
        </div>
        <?php endif; ?>
    </div>
</div>

<?php if ($preview): ?>
<!-- Preview -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="eye"></i>
            Förhandsgranskning - <?= h($preview['class_name']) ?>
        </h2>
    </div>
    <div class="admin-card-body">
        <p class="mb-md">
            <strong><?= count($preview['results']) ?></strong> resultat hittades.
            Granska och bekräfta importen.
        </p>

        <?php if (!empty($preview['errors'])): ?>
        <div class="alert alert-warning mb-md">
            <strong>Varningar:</strong>
            <ul style="margin: var(--space-xs) 0 0 0; padding-left: var(--space-lg);">
                <?php foreach ($preview['errors'] as $err): ?>
                <li><?= h($err) ?></li>
                <?php endforeach; ?>
            </ul>
        </div>
        <?php endif; ?>

        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th style="width: 60px;">Plac</th>
                        <th style="width: 80px;">Startnr</th>
                        <th>Namn</th>
                        <th>UCI-ID</th>
                        <th>Klubb</th>
                        <th style="width: 80px;">Land</th>
                        <th style="width: 60px;">Varv</th>
                        <th>Tid</th>
                        <th style="width: 100px;">Match</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($preview['results'] as $row): ?>
                    <tr>
                        <td>
                            <?php if ($row['status'] !== 'finished'): ?>
                                <span class="badge badge-warning"><?= strtoupper($row['status']) ?></span>
                            <?php else: ?>
                                <?= $row['position'] ?>
                            <?php endif; ?>
                        </td>
                        <td><?= h($row['bib_number']) ?></td>
                        <td><strong><?= h($row['firstname'] . ' ' . $row['lastname']) ?></strong></td>
                        <td><code class="text-sm"><?= h($row['uci_id']) ?></code></td>
                        <td><?= h($row['club_name']) ?></td>
                        <td><?= h($row['nationality']) ?></td>
                        <td><?= $row['laps'] ?? '-' ?></td>
                        <td><?= h($row['finish_time'] ?? '-') ?></td>
                        <td>
                            <?php if ($row['rider_match'] === 'Ny'): ?>
                                <span class="badge badge-info">Ny</span>
                            <?php elseif ($row['rider_match'] === 'UCI-ID'): ?>
                                <span class="badge badge-success">UCI-ID</span>
                            <?php else: ?>
                                <span class="badge badge-secondary">Namn</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>

        <form method="POST" style="margin-top: var(--space-lg);">
            <?= csrf_field() ?>
            <input type="hidden" name="pasted_data" value="<?= h($_POST['pasted_data'] ?? '') ?>">
            <input type="hidden" name="class_id" value="<?= $preview['class_id'] ?>">
            <input type="hidden" name="action" value="import">

            <div style="display: flex; gap: var(--space-md);">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="download"></i>
                    Importera <?= count($preview['results']) ?> resultat
                </button>
                <a href="?event_id=<?= $eventId ?>" class="btn-admin btn-admin-secondary">
                    <i data-lucide="arrow-left"></i>
                    Tillbaka
                </a>
            </div>
        </form>
    </div>
</div>

<?php else: ?>
<!-- Import Form -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="clipboard-paste"></i>
            Klistra in resultat
        </h2>
    </div>
    <div class="admin-card-body">
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="preview">

            <!-- Class Selection -->
            <div class="admin-form-group">
                <label class="admin-form-label">
                    <i data-lucide="tag"></i>
                    Välj klass
                </label>
                <div style="display: flex; gap: var(--space-md); flex-wrap: wrap;">
                    <select name="class_id" class="admin-form-select" style="flex: 1; min-width: 200px;" id="classSelect">
                        <option value="">-- Välj befintlig klass --</option>
                        <?php if (!empty($eventClasses)): ?>
                        <optgroup label="Klasser i detta event">
                            <?php foreach ($eventClasses as $c): ?>
                            <option value="<?= $c['id'] ?>"><?= h($c['display_name']) ?></option>
                            <?php endforeach; ?>
                        </optgroup>
                        <?php endif; ?>
                        <optgroup label="Alla klasser">
                            <?php foreach ($allClasses as $c): ?>
                            <option value="<?= $c['id'] ?>"><?= h($c['display_name']) ?></option>
                            <?php endforeach; ?>
                        </optgroup>
                    </select>
                    <span class="text-secondary" style="align-self: center;">eller</span>
                    <input type="text" name="new_class_name" class="admin-form-input"
                           style="flex: 1; min-width: 200px;"
                           placeholder="Skapa ny klass..."
                           id="newClassInput">
                </div>
            </div>

            <!-- Paste Area -->
            <div class="admin-form-group">
                <label class="admin-form-label">
                    <i data-lucide="file-text"></i>
                    Klistra in data (tab-separerad)
                </label>
                <textarea name="pasted_data" class="admin-form-textarea"
                          rows="15"
                          placeholder="Klistra in resultat här...

Format som stöds:
Plac.  Startnr.  Deltagare  UCI-ID  Klubb  Land  Varv  Tid  Varv1  Varv2...

Exempel:
1  531  Olof EKFJELL  10006446036  Alingsås SC  Sverige SWE  5  1:02:54  11:55  12:16
2  535  Niklas HERMANSSON  10103287301  Trollhättans SOK  Sverige SWE  5  1:06:28  12:42  13:08
DNS  533  Christian NILSSON  10058874031  CK Master  Sverige SWE  0"
                          style="font-family: monospace; font-size: 0.85rem;"
                ><?= h($_POST['pasted_data'] ?? '') ?></textarea>
            </div>

            <button type="submit" class="btn-admin btn-admin-primary">
                <i data-lucide="eye"></i>
                Förhandsgranska
            </button>
        </form>
    </div>
</div>

<!-- Format Help -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="help-circle"></i>
            Format
        </h2>
    </div>
    <div class="admin-card-body">
        <p class="text-secondary mb-md">
            Kopiera resultat från timing-system, Excel eller webbsida och klistra in.
            Tab-separerade kolumner stöds.
        </p>

        <h3 class="mb-sm">Kolumner som känns igen:</h3>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Kolumn</th>
                        <th>Beskrivning</th>
                        <th>Exempel</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>Plac.</code></td>
                        <td>Placering (1, 2, 3...) eller DNS/DNF/DQ</td>
                        <td>1, DNS, DNF</td>
                    </tr>
                    <tr>
                        <td><code>Startnr.</code></td>
                        <td>Nummerlapp</td>
                        <td>531</td>
                    </tr>
                    <tr>
                        <td><code>Deltagare</code></td>
                        <td>Namn (Förnamn EFTERNAMN)</td>
                        <td>Olof EKFJELL</td>
                    </tr>
                    <tr>
                        <td><code>UCI-ID</code></td>
                        <td>UCI-licensnummer</td>
                        <td>10006446036</td>
                    </tr>
                    <tr>
                        <td><code>Klubb</code></td>
                        <td>Klubbnamn</td>
                        <td>Alingsås SC</td>
                    </tr>
                    <tr>
                        <td><code>Land</code></td>
                        <td>Nationalitet (extraherar 3-bokstavskod)</td>
                        <td>Sverige SWE</td>
                    </tr>
                    <tr>
                        <td><code>Varv</code></td>
                        <td>Antal genomförda varv (XC/MTB)</td>
                        <td>5</td>
                    </tr>
                    <tr>
                        <td><code>Tid</code></td>
                        <td>Sluttid</td>
                        <td>1:02:54</td>
                    </tr>
                    <tr>
                        <td><code>Varv 1, 2, 3...</code></td>
                        <td>Split-tider/varvtider</td>
                        <td>11:55, 12:16</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="alert alert-info mt-lg">
            <i data-lucide="info"></i>
            <strong>Tips:</strong> Header-raden är valfri och ignoreras automatiskt.
        </div>
    </div>
</div>
<?php endif; ?>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const classSelect = document.getElementById('classSelect');
    const newClassInput = document.getElementById('newClassInput');

    // Clear new class input when selecting existing class
    if (classSelect && newClassInput) {
        classSelect.addEventListener('change', function() {
            if (this.value) {
                newClassInput.value = '';
            }
        });

        newClassInput.addEventListener('input', function() {
            if (this.value) {
                classSelect.value = '';
            }
        });
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
