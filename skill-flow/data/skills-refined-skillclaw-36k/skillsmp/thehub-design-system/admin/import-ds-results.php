<?php
/**
 * Import Dual Slalom Results
 * CSV format: Placering, Tävlingsklass, Namn, Klubb, Kvalpoängsklass
 * Points are calculated automatically from event settings
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/import-functions.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Download template
if (isset($_GET['download_template'])) {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="ds-resultat-mall.csv"');
    echo "Placering;Tävlingsklass;Namn;Klubb;Kvalpoängsklass\n";
    echo "1;Flickor 13-16;Ebba Myrefelt;Borgholm CK;Flickor 13-14\n";
    echo "2;Flickor 13-16;Elsa Sporre Friberg;CK Fix;Flickor 13-14\n";
    echo "3;Flickor 13-16;Sara Warnevik;;Flickor 13-14\n";
    echo "1;Pojkar 13-16;Theodor Ek;CK Fix;Pojkar 15-16\n";
    echo "2;Pojkar 13-16;Arvid Andersson;Falkenbergs CK;Pojkar 15-16\n";
    echo "1;Sportmotion Damer;Ella Mårtensson;Borås CA;Damer Junior\n";
    echo "1;Sportmotion Herrar;Ivan Bergström;RND Racing;Herrar Junior\n";
    exit;
}

// Get events
$events = $db->getAll("
    SELECT e.id, e.name, e.date, e.discipline
    FROM events e
    WHERE e.discipline = 'DS' OR e.name LIKE '%Dual%' OR e.name LIKE '%Slalom%'
    ORDER BY e.date DESC
    LIMIT 100
");

if (empty($events)) {
    $events = $db->getAll("
        SELECT id, name, date, discipline
        FROM events
        ORDER BY date DESC
        LIMIT 200
    ");
}

// Helper function to split name
function splitName($fullName) {
    $fullName = trim($fullName);
    $parts = preg_split('/\s+/', $fullName, 2);
    $firstName = $parts[0] ?? '';
    $lastName = $parts[1] ?? '';
    return [$firstName, $lastName];
}

// Handle import
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['import'])) {
    checkCsrf();

    $eventId = (int)$_POST['event_id'];
    $csvData = trim($_POST['csv_data']);

    if (!$eventId) {
        $message = 'Välj ett event';
        $messageType = 'error';
    } elseif (empty($csvData)) {
        $message = 'Klistra in CSV-data';
        $messageType = 'error';
    } else {
        $lines = explode("\n", $csvData);
        $imported = 0;
        $errors = [];
        $lastEventClass = ''; // For rows with empty event class

        // Detect delimiter - prioritize tab
        $firstLine = $lines[0];
        $tabCount = substr_count($firstLine, "\t");
        $semiCount = substr_count($firstLine, ';');
        $commaCount = substr_count($firstLine, ',');

        if ($tabCount >= 3) {
            $delimiter = "\t";
        } elseif ($semiCount > $commaCount) {
            $delimiter = ';';
        } else {
            $delimiter = ',';
        }

        // Check if first line is header
        $firstLineLower = strtolower($firstLine);
        $hasHeader = (strpos($firstLineLower, 'klass') !== false ||
                      strpos($firstLineLower, 'plac') !== false ||
                      strpos($firstLineLower, 'namn') !== false ||
                      strpos($firstLineLower, 'poäng') !== false);

        if ($hasHeader) {
            array_shift($lines);
        }

        foreach ($lines as $lineNum => $line) {
            $line = trim($line);
            if (empty($line)) continue;

            $cols = str_getcsv($line, $delimiter);

            // Skip rows with all empty values
            $nonEmpty = array_filter($cols, function($v) { return trim($v) !== ''; });
            if (count($nonEmpty) < 3) continue;

            // Format: Placering, Tävlingsklass, Namn, Klubb, Kvalpoängsklass
            $position = (int)trim($cols[0] ?? '');
            $eventClassName = trim($cols[1] ?? '');
            $fullName = trim($cols[2] ?? '');
            $clubName = trim($cols[3] ?? '');
            $seriesClassName = trim($cols[4] ?? '');

            // Use last event class if empty
            if (empty($eventClassName) && !empty($lastEventClass)) {
                $eventClassName = $lastEventClass;
            } elseif (!empty($eventClassName)) {
                $lastEventClass = $eventClassName;
            }

            // Split name
            list($firstName, $lastName) = splitName($fullName);

            if (empty($firstName)) {
                continue; // Skip rows without name
            }

            if ($position < 1 || $position > 200) {
                $errors[] = "Rad " . ($lineNum + 1) . ": Ogiltig placering: $position";
                continue;
            }

            if (empty($seriesClassName)) {
                $errors[] = "Rad " . ($lineNum + 1) . ": Saknar kvalpoängsklass för $fullName";
                continue;
            }

            try {
                // Find or create EVENT class
                $eventClass = $db->getRow(
                    "SELECT id FROM classes WHERE LOWER(display_name) = LOWER(?) OR LOWER(name) = LOWER(?)",
                    [$eventClassName, $eventClassName]
                );

                if (!$eventClass) {
                    $eventClassId = $db->insert('classes', [
                        'name' => strtolower(str_replace(' ', '_', $eventClassName)),
                        'display_name' => $eventClassName,
                        'active' => 1,
                        'sort_order' => 900
                    ]);
                } else {
                    $eventClassId = $eventClass['id'];
                }

                // Find or create SERIES class (normalize case)
                $seriesClassNormalized = ucfirst(strtolower($seriesClassName));
                $seriesClass = $db->getRow(
                    "SELECT id FROM classes WHERE LOWER(display_name) = LOWER(?) OR LOWER(name) = LOWER(?)",
                    [$seriesClassName, $seriesClassName]
                );

                if (!$seriesClass) {
                    $seriesClassId = $db->insert('classes', [
                        'name' => strtolower(str_replace(' ', '_', $seriesClassName)),
                        'display_name' => $seriesClassName,
                        'active' => 1,
                        'sort_order' => 950
                    ]);
                } else {
                    $seriesClassId = $seriesClass['id'];
                }

                // Find or create rider
                $rider = $db->getRow(
                    "SELECT id FROM riders WHERE UPPER(firstname) = UPPER(?) AND UPPER(lastname) = UPPER(?)",
                    [$firstName, $lastName]
                );

                if (!$rider) {
                    // Check if this name was previously merged
                    $mergedRider = null;
                    try {
                        $mergedRider = $db->getRow(
                            "SELECT canonical_rider_id FROM rider_merge_map WHERE UPPER(merged_firstname) = UPPER(?) AND UPPER(merged_lastname) = UPPER(?) AND status = 'approved'",
                            [$firstName, $lastName]
                        );
                    } catch (Exception $e) { /* Table might not exist yet */ }

                    if ($mergedRider) {
                        $riderId = $mergedRider['canonical_rider_id'];
                    } else {
                        $clubId = null;
                        if (!empty($clubName)) {
                            $club = $db->getRow("SELECT id FROM clubs WHERE LOWER(name) = LOWER(?)", [$clubName]);
                            if (!$club) {
                                $clubId = $db->insert('clubs', ['name' => $clubName, 'active' => 1]);
                            } else {
                                $clubId = $club['id'];
                            }
                        }

                        $riderId = $db->insert('riders', [
                            'firstname' => $firstName,
                            'lastname' => $lastName,
                            'club_id' => $clubId,
                            'active' => 1
                        ]);
                    }
                } else {
                    $riderId = $rider['id'];
                }

                // Check if result already exists
                $existing = $db->getRow(
                    "SELECT id FROM results WHERE event_id = ? AND cyclist_id = ?",
                    [$eventId, $riderId]
                );

                $resultData = [
                    'position' => $position,
                    'class_id' => $eventClassId,
                    'series_class_id' => $seriesClassId,
                    'status' => 'finished'
                ];

                if ($existing) {
                    $db->update('results', $resultData, 'id = ?', [$existing['id']]);
                } else {
                    $resultData['event_id'] = $eventId;
                    $resultData['cyclist_id'] = $riderId;
                    $db->insert('results', $resultData);
                }

                $imported++;

            } catch (Exception $e) {
                $errors[] = "Rad " . ($lineNum + 1) . ": " . $e->getMessage();
            }
        }

        if ($imported > 0) {
            // Calculate points based on event settings
            try {
                recalculateEventResults($db, $eventId);
                $message = "$imported resultat importerade och poäng beräknade!";
            } catch (Exception $e) {
                $message = "$imported resultat importerade. Poängberäkning misslyckades: " . $e->getMessage();
            }
            if (!empty($errors)) {
                $message .= " (" . count($errors) . " fel)";
            }
            $messageType = 'success';
        } else {
            $message = "Ingen data importerades. " . implode(", ", array_slice($errors, 0, 5));
            $messageType = 'error';
        }
    }
}

$page_title = 'Import DS Resultat';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import.php'],
    ['label' => 'Dual Slalom Resultat']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header" style="display:flex; justify-content:space-between; align-items:center;">
        <h2>
            <i data-lucide="git-branch"></i>
            Importera DS Resultat
        </h2>
        <a href="?download_template=1" class="btn btn--secondary btn--sm">
            <i data-lucide="download"></i>
            Ladda ner mall
        </a>
    </div>
    <div class="card-body">
        <div class="alert alert-info mb-lg">
            <strong>Format:</strong> Placering · Tävlingsklass · Namn · Klubb · Kvalpoängsklass<br>
            <small>Poäng beräknas automatiskt från eventets inställningar.</small>
        </div>

        <form method="POST">
            <?= csrf_field() ?>

            <div class="form-group mb-lg">
                <label class="label">1. Välj Event</label>
                <select name="event_id" class="input" required style="max-width: 400px;">
                    <option value="">-- Välj event --</option>
                    <?php foreach ($events as $e): ?>
                    <option value="<?= $e['id'] ?>">
                        <?= h($e['name']) ?> (<?= date('Y-m-d', strtotime($e['date'])) ?>)
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="form-group mb-lg">
                <label class="label">2. Klistra in data (kopiera från Excel/Sheets)</label>
                <textarea name="csv_data" class="input" rows="20" placeholder="Placering	Tävlingsklass	Namn	Klubb	Kvalpoängsklass
1	Flickor 13-16	Ebba Myrefelt	Borgholm CK	Flickor 13-14
2	Flickor 13-16	Elsa Sporre Friberg	CK Fix	Flickor 13-14
..." style="font-family: monospace; font-size: 13px;"></textarea>
                <p class="text-sm text-secondary mt-sm">
                    Klistra in direkt från Excel/Google Sheets (tab-separerat).
                </p>
            </div>

            <button type="submit" name="import" class="btn btn--primary btn-lg">
                <i data-lucide="upload"></i>
                Importera
            </button>
        </form>
    </div>
</div>

<!-- Example -->
<div class="card mt-lg">
    <div class="card-header">
        <h3><i data-lucide="info"></i> Exempelformat</h3>
    </div>
    <div class="card-body">
        <pre class="gs-code-dark" style="font-size: 12px; overflow-x: auto;">Placering	Tävlingsklass	Namn	Klubb	Kvalpoängsklass
1	Flickor 13-16	Ebba Myrefelt	Borgholm CK	Flickor 13-14
2	Flickor 13-16	Elsa Sporre Friberg	CK Fix	Flickor 13-14
3	Flickor 13-16	Sara Warnevik		Flickor 13-14
1	Pojkar 13-16	Theodor Ek	CK Fix	Pojkar 15-16
2	Pojkar 13-16	Arvid Andersson	Falkenbergs CK	Pojkar 15-16
1	Sportmotion Damer	Ella Mårtensson	Borås CA	Damer Junior
1	Sportmotion Herrar	Ivan Bergström	RND Racing	Herrar Junior</pre>
        <p class="text-sm text-secondary mt-md">
            <strong>Tävlingsklass</strong> = Visas på resultatsidan<br>
            <strong>Kvalpoängsklass</strong> = Där poängen räknas i serietabellen<br>
            <strong>Poäng</strong> = Beräknas automatiskt från eventets poängskala
        </p>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
