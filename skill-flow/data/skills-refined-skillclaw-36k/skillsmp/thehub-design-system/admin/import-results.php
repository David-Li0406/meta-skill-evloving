<?php
/**
 * Import Results - V1.0 Tabbed System
 * Supports: Enduro, Downhill, XC, Dual Slalom
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/import-history.php';
require_once __DIR__ . '/../includes/class-calculations.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_once __DIR__ . '/../includes/import-functions.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';

// Get active tab from URL or default to enduro
$activeTab = $_GET['tab'] ?? 'enduro';
$validTabs = ['enduro', 'dh', 'xc', 'dual_slalom'];
if (!in_array($activeTab, $validTabs)) {
    $activeTab = 'enduro';
}

// Handle template download
if (isset($_GET['template'])) {
    $format = $_GET['template'];
    header('Content-Type: text/csv; charset=utf-8');

    if ($format === 'enduro') {
        header('Content-Disposition: attachment; filename="resultat_enduro_mall.csv"');
        $output = fopen('php://output', 'w');
        fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));
        fputcsv($output, [
            'Category', 'PlaceByCategory', 'Bib no', 'FirstName', 'LastName', 'Club', 'UCI-ID',
            'NetTime', 'Status', 'SS1', 'SS2', 'SS3', 'SS4', 'SS5', 'SS6'
        ], ';');
        fputcsv($output, [
            'Herrar Elit', '1', '101', 'Erik', 'Svensson', 'Stockholm MTB', '10012345678',
            '15:42.33', 'FIN', '2:15.44', '1:52.11', '2:33.55', '2:18.22', '3:01.88', '3:21.13'
        ], ';');
    } elseif ($format === 'dh') {
        header('Content-Disposition: attachment; filename="resultat_dh_mall.csv"');
        $output = fopen('php://output', 'w');
        fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));
        fputcsv($output, [
            'Category', 'PlaceByCategory', 'Bib no', 'FirstName', 'LastName', 'Club', 'UCI-ID',
            'Run1', 'Run2', 'NetTime', 'Status'
        ], ';');
        fputcsv($output, [
            'Herrar Elit', '1', '101', 'Erik', 'Svensson', 'Stockholm MTB', '10012345678',
            '2:15.44', '2:12.33', '2:12.33', 'FIN'
        ], ';');
    } elseif ($format === 'xc') {
        header('Content-Disposition: attachment; filename="resultat_xc_mall.csv"');
        $output = fopen('php://output', 'w');
        fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));
        fputcsv($output, [
            'Category', 'PlaceByCategory', 'Bib no', 'FirstName', 'LastName', 'Club', 'UCI-ID',
            'NetTime', 'Status', 'Lap1', 'Lap2', 'Lap3', 'Lap4', 'Lap5'
        ], ';');
        fputcsv($output, [
            'Herrar Elit', '1', '101', 'Erik', 'Svensson', 'Stockholm MTB', '10012345678',
            '1:02:42.33', 'FIN', '12:15.44', '11:52.11', '12:33.55', '12:18.22', '13:43.01'
        ], ';');
    } elseif ($format === 'dual_slalom') {
        header('Content-Disposition: attachment; filename="resultat_ds_kval_mall.csv"');
        $output = fopen('php://output', 'w');
        fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));
        fputcsv($output, [
            'Category', 'Bib no', 'FirstName', 'LastName', 'Club',
            'Run1', 'Run2', 'BestTime', 'Status'
        ], ';');
        fputcsv($output, [
            'Herrar Elit', '101', 'Erik', 'Svensson', 'Stockholm MTB',
            '32.44', '31.22', '31.22', 'FIN'
        ], ';');
    }

    fclose($output);
    exit;
}

// Load existing events for dropdown with series info
$existingEvents = $db->getAll("
    SELECT e.id, e.name, e.date, e.location, YEAR(e.date) as event_year,
        e.discipline, e.event_format,
        GROUP_CONCAT(DISTINCT s.name ORDER BY s.name SEPARATOR ', ') as series_names
    FROM events e
    LEFT JOIN series_events se ON e.id = se.event_id
    LEFT JOIN series s ON se.series_id = s.id
    GROUP BY e.id
    ORDER BY e.date DESC
    LIMIT 500
");

// Get unique years for filter
$eventYears = array_unique(array_column($existingEvents, 'event_year'));
rsort($eventYears);

// Handle CSV upload - redirect to preview
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['import_file'])) {
    checkCsrf();

    $file = $_FILES['import_file'];
    $selectedEventId = !empty($_POST['event_id']) ? (int)$_POST['event_id'] : null;
    $importFormat = !empty($_POST['import_format']) ? $_POST['import_format'] : null;

    // Validate format and event selection
    if (!$importFormat || !in_array($importFormat, ['enduro', 'dh', 'xc'])) {
        $message = 'Du måste välja ett giltigt format';
        $messageType = 'error';
    } elseif (!$selectedEventId) {
        $message = 'Du måste välja ett event först';
        $messageType = 'error';
    } elseif ($file['error'] !== UPLOAD_ERR_OK) {
        $message = 'Filuppladdning misslyckades';
        $messageType = 'error';
    } elseif ($file['size'] > MAX_UPLOAD_SIZE) {
        $message = 'Filen är för stor (max ' . (MAX_UPLOAD_SIZE / 1024 / 1024) . 'MB)';
        $messageType = 'error';
    } else {
        $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

        if ($extension !== 'csv') {
            $message = 'Endast CSV-filer stöds för resultatimport';
            $messageType = 'error';
        } else {
            // Save file and redirect to preview
            $uploaded = UPLOADS_PATH . '/' . time() . '_preview_' . basename($file['name']);

            if (move_uploaded_file($file['tmp_name'], $uploaded)) {
                // Clear old preview data
                unset($_SESSION['import_preview_file']);
                unset($_SESSION['import_preview_filename']);
                unset($_SESSION['import_preview_data']);
                unset($_SESSION['import_events_summary']);
                unset($_SESSION['import_selected_event']);

                // Store in session and redirect to preview
                $_SESSION['import_preview_file'] = $uploaded;
                $_SESSION['import_preview_filename'] = $file['name'];
                $_SESSION['import_selected_event'] = $selectedEventId;
                $_SESSION['import_format'] = $importFormat;

                header('Location: /admin/import-results-preview.php');
                exit;
            } else {
                $message = 'Kunde inte ladda upp filen';
                $messageType = 'error';
            }
        }
    }
}

// Page config for unified layout
$page_title = 'Importera Resultat';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Resultat']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Tab Navigation -->
<div class="tabs mb-lg">
    <nav class="tabs-nav">
        <a href="?tab=enduro" class="tab <?= $activeTab === 'enduro' ? 'active' : '' ?>">
            <i data-lucide="mountain"></i>
            Enduro
        </a>
        <a href="?tab=dh" class="tab <?= $activeTab === 'dh' ? 'active' : '' ?>">
            <i data-lucide="arrow-down"></i>
            Downhill
        </a>
        <a href="?tab=xc" class="tab <?= $activeTab === 'xc' ? 'active' : '' ?>">
            <i data-lucide="circle"></i>
            XC
        </a>
        <a href="?tab=dual_slalom" class="tab <?= $activeTab === 'dual_slalom' ? 'active' : '' ?>">
            <i data-lucide="git-branch"></i>
            Dual Slalom
        </a>
    </nav>
</div>

<?php if ($activeTab === 'dual_slalom'): ?>
<!-- DUAL SLALOM TAB -->
<?php
// Handle DS Final Results import
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['import_ds_final'])) {
    checkCsrf();

    $eventId = (int)$_POST['event_id'];
    $csvData = trim($_POST['csv_data']);
    $clearExisting = isset($_POST['clear_existing']) && $_POST['clear_existing'] === '1';

    if (!$eventId) {
        $message = 'Välj ett event';
        $messageType = 'error';
    } elseif (empty($csvData)) {
        $message = 'Klistra in data';
        $messageType = 'error';
    } else {
        global $pdo;
        $lines = explode("\n", $csvData);
        $imported = 0;
        $errors = [];
        $lastEventClass = '';

        // Detect delimiter
        $firstLine = $lines[0];
        $tabCount = substr_count($firstLine, "\t");
        $semiCount = substr_count($firstLine, ';');
        $delimiter = ($tabCount >= 3) ? "\t" : (($semiCount > 2) ? ';' : ',');

        // Check for header - look for common header keywords
        $firstLineLower = strtolower($firstLine);
        $hasHeader = (strpos($firstLineLower, 'category') !== false ||
                      strpos($firstLineLower, 'placebycategory') !== false ||
                      strpos($firstLineLower, 'firstname') !== false ||
                      strpos($firstLineLower, 'bib') !== false ||
                      strpos($firstLineLower, 'qualification') !== false);
        if ($hasHeader) array_shift($lines);

        // Clear existing if requested
        if ($clearExisting) {
            $pdo->prepare("DELETE FROM results WHERE event_id = ?")->execute([$eventId]);
        }

        $classesToCalculate = [];

        foreach ($lines as $lineNum => $line) {
            $line = trim($line);
            if (empty($line)) continue;

            $cols = str_getcsv($line, $delimiter);
            $nonEmpty = array_filter($cols, function($v) { return trim($v) !== ''; });
            if (count($nonEmpty) < 4) continue;

            // NEW FORMAT: PlaceByCategory, Bib, Category, FirstName, LastName, Club, qualification points class
            $position = (int)trim($cols[0] ?? '');
            $bibNumber = trim($cols[1] ?? '');
            $eventClassName = trim($cols[2] ?? '');
            $firstName = trim($cols[3] ?? '');
            $lastName = trim($cols[4] ?? '');
            $clubName = trim($cols[5] ?? '');
            $seriesClassName = trim($cols[6] ?? '');

            // Use last event class if empty (for continuation rows)
            if (empty($eventClassName) && !empty($lastEventClass)) {
                $eventClassName = $lastEventClass;
            } elseif (!empty($eventClassName)) {
                $lastEventClass = $eventClassName;
            }

            if (empty($firstName) || $position < 1 || $position > 200) continue;
            if (empty($seriesClassName)) {
                $errors[] = "Rad " . ($lineNum + 1) . ": Saknar kvalpoängsklass för $firstName $lastName";
                continue;
            }

            try {
                // Find/create event class (tävlingsklass för visning)
                $eventClass = $db->getRow("SELECT id FROM classes WHERE LOWER(display_name) = LOWER(?) OR LOWER(name) = LOWER(?)", [$eventClassName, $eventClassName]);
                $eventClassId = $eventClass ? $eventClass['id'] : $db->insert('classes', ['name' => strtolower(str_replace(' ', '_', $eventClassName)), 'display_name' => $eventClassName, 'active' => 1, 'sort_order' => 900]);

                // Find/create series class (kvalpoängsklass för seriepoäng)
                $seriesClass = $db->getRow("SELECT id FROM classes WHERE LOWER(display_name) = LOWER(?) OR LOWER(name) = LOWER(?)", [$seriesClassName, $seriesClassName]);
                $seriesClassId = $seriesClass ? $seriesClass['id'] : $db->insert('classes', ['name' => strtolower(str_replace(' ', '_', $seriesClassName)), 'display_name' => $seriesClassName, 'active' => 1, 'sort_order' => 950]);

                // Find/create rider
                $rider = $db->getRow("SELECT id FROM riders WHERE UPPER(firstname) = UPPER(?) AND UPPER(lastname) = UPPER(?)", [$firstName, $lastName]);
                if (!$rider) {
                    // Check if this name was previously merged (to prevent recreating deleted duplicates)
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
                            $clubId = $club ? $club['id'] : $db->insert('clubs', ['name' => $clubName, 'active' => 1]);
                        }
                        $riderId = $db->insert('riders', ['firstname' => $firstName, 'lastname' => $lastName, 'club_id' => $clubId, 'active' => 1]);
                    }
                } else {
                    $riderId = $rider['id'];
                }

                // Check existing
                $existing = $db->getRow("SELECT id FROM results WHERE event_id = ? AND cyclist_id = ?", [$eventId, $riderId]);

                // Result data:
                // - class_id = Tävlingsklass (för VISNING i resultatlistan)
                // - series_class_id = Kvalpoängsklass (för SERIEPOÄNG i serietabellen)
                // - position = Placering i tävlingen (baserar poäng enligt DS-mall)
                $resultData = [
                    'position' => $position,
                    'class_id' => $eventClassId,
                    'series_class_id' => $seriesClassId,
                    'bib_number' => $bibNumber ?: null,
                    'status' => 'finished'
                ];

                if ($existing) {
                    $db->update('results', $resultData, 'id = ?', [$existing['id']]);
                } else {
                    $resultData['event_id'] = $eventId;
                    $resultData['cyclist_id'] = $riderId;
                    $db->insert('results', $resultData);
                }

                $classesToCalculate[$seriesClassId] = true;
                $imported++;
            } catch (Exception $e) {
                $errors[] = "Rad " . ($lineNum + 1) . ": " . $e->getMessage();
            }
        }

        if ($imported > 0) {
            try {
                // NOTE: For DS import, we do NOT call recalculateEventResults() because
                // it would overwrite our position values with time-based positions.
                // Instead, we only sync to series_results for points calculation.
                require_once INCLUDES_PATH . '/series-points.php';
                $syncStats = syncEventResultsToAllSeries($db, $eventId);

                $message = "$imported slutresultat importerade!";
                if (!empty($syncStats)) {
                    $totalInserted = array_sum(array_column($syncStats, 'inserted'));
                    $totalUpdated = array_sum(array_column($syncStats, 'updated'));
                    $message .= " Seriepoäng: {$totalInserted} nya, {$totalUpdated} uppdaterade.";
                }
                if (!empty($errors)) {
                    $message .= " (" . count($errors) . " rader hoppades över)";
                }
            } catch (Exception $e) {
                $message = "$imported resultat importerade. Seriepoäng: " . $e->getMessage();
            }
            $messageType = 'success';
        } else {
            $message = "Ingen data importerades. " . implode(", ", array_slice($errors, 0, 3));
            $messageType = 'error';
        }
    }
}

// Get DS events
$dsEvents = $db->getAll("
    SELECT e.id, e.name, e.date
    FROM events e
    WHERE e.discipline = 'DS' OR e.name LIKE '%Dual%' OR e.name LIKE '%Slalom%'
    ORDER BY e.date DESC
    LIMIT 100
");
if (empty($dsEvents)) {
    $dsEvents = $existingEvents;
}
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="git-branch"></i>
            Dual Slalom / Elimination
        </h2>
    </div>
    <div class="card-body">
        <!-- Sub-tabs for DS -->
        <div class="tabs mb-lg">
            <nav class="tabs-nav">
                <button class="tab active" data-ds-tab="final">
                    <i data-lucide="trophy"></i>
                    Slutresultat (Eliminering)
                </button>
                <button class="tab" data-ds-tab="qualifying">
                    <i data-lucide="timer"></i>
                    Kvalificering
                </button>
                <button class="tab" data-ds-tab="bracket">
                    <i data-lucide="git-merge"></i>
                    Bracket
                </button>
            </nav>
        </div>

        <!-- FINAL RESULTS TAB (Default) -->
        <div id="ds-tab-final" class="ds-tab-content">
            <div class="alert alert-info mb-lg">
                <strong>Importera slutresultat från eliminering:</strong><br>
                <ul style="margin: 8px 0 0 20px;">
                    <li><strong>PlaceByCategory</strong> = Placering i tävlingen (bestämmer poäng enligt DS-mall)</li>
                    <li><strong>Bib</strong> = Startnummer</li>
                    <li><strong>Category</strong> = Tävlingsklass (visas i resultatlistan)</li>
                    <li><strong>FirstName, LastName</strong> = Namn</li>
                    <li><strong>Club</strong> = Klubbtillhörighet</li>
                    <li><strong>qualification points class</strong> = Klass för seriepoäng (i serietabellen)</li>
                </ul>
            </div>

            <form method="POST">
                <?= csrf_field() ?>
                <input type="hidden" name="import_ds_final" value="1">

                <div class="form-group mb-lg">
                    <label class="label label-lg">
                        <span class="badge badge-primary mr-sm">1</span>
                        Välj Event
                    </label>
                    <select name="event_id" class="input input-lg" required style="max-width: 500px;">
                        <option value="">-- Välj event --</option>
                        <?php foreach ($dsEvents as $e): ?>
                        <option value="<?= $e['id'] ?>">
                            <?= h($e['name']) ?> (<?= date('Y-m-d', strtotime($e['date'])) ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <div class="form-group mb-lg">
                    <label class="checkbox-label">
                        <input type="checkbox" name="clear_existing" value="1">
                        <span>Rensa befintliga resultat först</span>
                    </label>
                </div>

                <div class="form-group mb-lg">
                    <label class="label label-lg">
                        <span class="badge badge-primary mr-sm">2</span>
                        Klistra in data (kopiera från Excel/Sheets)
                    </label>
                    <textarea name="csv_data" class="input" rows="15" placeholder="PlaceByCategory&#9;Bib&#9;Category&#9;FirstName&#9;LastName&#9;Club&#9;qualification points class
1&#9;1&#9;Flickor 13-16&#9;Ebba&#9;Myrefelt&#9;Borgholm CK&#9;Flickor 13-14
2&#9;3&#9;Flickor 13-16&#9;Elsa&#9;Sporre Friberg&#9;CK Fix&#9;Flickor 13-14
..." style="font-family: monospace; font-size: 13px;"></textarea>
                </div>

                <button type="submit" class="btn btn--primary btn-lg">
                    <i data-lucide="upload"></i>
                    Importera Slutresultat
                </button>
            </form>

            <details class="gs-details mt-lg">
                <summary class="text-sm text-primary">Visa exempelformat</summary>
                <pre class="gs-code-dark mt-md">PlaceByCategory	Bib	Category	FirstName	LastName	Club	qualification points class
1	1	Flickor 13-16	Ebba	Myrefelt	Borgholm CK	Flickor 13-14
2	3	Flickor 13-16	Elsa	Sporre Friberg	CK Fix	Flickor 13-14
3	42	Flickor 13-16	Sara	Warnevik		Flickor 13-14
1	5	Pojkar 13-16	Theodor	Ek	CK Fix	Pojkar 15-16
2	9	Pojkar 13-16	Arvid	Andersson	Falkenbergs CK	Pojkar 15-16
1	15	Sportmotion Damer	Ella	Mårtensson	Borås CA	Damer Junior
1	28	Sportmotion Herrar	Ivan	Bergström	RND Racing	Herrar Junior</pre>
            </details>

            <div class="alert alert-warning mt-lg">
                <strong>Så här fungerar det:</strong><br>
                <ul style="margin: 8px 0 0 20px;">
                    <li>Poäng beräknas efter <strong>PlaceByCategory</strong> enligt DS-poängmallen</li>
                    <li>I <strong>resultatlistan</strong> visas deltagaren i sin <strong>Category</strong> (tävlingsklass)</li>
                    <li>I <strong>serietabellen</strong> hamnar poängen i <strong>qualification points class</strong></li>
                </ul>
            </div>
        </div>

        <!-- QUALIFYING TAB -->
        <div id="ds-tab-qualifying" class="ds-tab-content" style="display: none;">
            <p class="mb-lg">Importera CSV med kvaltider för att seeda deltagare till bracket.</p>

            <a href="/admin/elimination-import-qualifying.php" class="btn btn--primary">
                <i data-lucide="file-plus"></i>
                Importera kvalresultat
            </a>

            <div class="mt-lg">
                <a href="?template=dual_slalom" class="btn btn--secondary btn--sm">
                    <i data-lucide="download"></i>
                    Ladda ner mall för kvalresultat
                </a>
            </div>

            <div class="alert alert--info mt-lg">
                <strong>CSV-format för kvalificering:</strong><br>
                <code>Category, Bib, FirstName, LastName, Club, Run1, Run2, BestTime, Status</code>
            </div>
        </div>

        <!-- BRACKET TAB -->
        <div id="ds-tab-bracket" class="ds-tab-content" style="display: none;">
            <p class="mb-lg">Hantera elimination-bracket och registrera resultat från omgångar.</p>

            <a href="/admin/elimination.php" class="btn btn--secondary">
                <i data-lucide="list"></i>
                Visa alla DS-events
            </a>
        </div>
    </div>
</div>

<script>
document.querySelectorAll('[data-ds-tab]').forEach(btn => {
    btn.addEventListener('click', function() {
        const tabId = this.dataset.dsTab;
        document.querySelectorAll('[data-ds-tab]').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        document.querySelectorAll('.ds-tab-content').forEach(c => c.style.display = 'none');
        document.getElementById('ds-tab-' + tabId).style.display = '';
    });
});
</script>

<?php else: ?>
<!-- ENDURO / DH / XC TABS -->
<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <?php if ($activeTab === 'enduro'): ?>
            <i data-lucide="mountain"></i> Importera Enduro-resultat
            <?php elseif ($activeTab === 'dh'): ?>
            <i data-lucide="arrow-down"></i> Importera Downhill-resultat
            <?php else: ?>
            <i data-lucide="circle"></i> Importera XC-resultat
            <?php endif; ?>
        </h2>
    </div>
    <div class="card-body">
        <form method="POST" enctype="multipart/form-data" class="gs-form">
            <?= csrf_field() ?>
            <input type="hidden" name="import_format" value="<?= $activeTab === 'xc' ? 'xc' : $activeTab ?>">

            <!-- Download Template -->
            <div class="form-group mb-lg">
                <a href="?template=<?= $activeTab ?>" class="btn btn--secondary btn--sm">
                    <i data-lucide="download"></i>
                    Ladda ner <?= $activeTab === 'enduro' ? 'Enduro' : ($activeTab === 'dh' ? 'DH' : 'XC') ?>-mall
                </a>
            </div>

            <!-- Step 1: Select Year -->
            <div class="form-group mb-lg">
                <label for="year_filter" class="label label-lg">
                    <span class="badge badge-primary mr-sm">1</span>
                    Välj år
                </label>
                <select id="year_filter" class="input input-lg">
                    <option value="">-- Alla år --</option>
                    <?php foreach ($eventYears as $year): ?>
                    <option value="<?= $year ?>" <?= $year == date('Y') ? 'selected' : '' ?>><?= $year ?></option>
                    <?php endforeach; ?>
                </select>
            </div>

            <!-- Step 2: Select Event -->
            <div class="form-group mb-lg">
                <label for="event_id" class="label label-lg">
                    <span class="badge badge-primary mr-sm">2</span>
                    Välj event
                </label>
                <select id="event_id" name="event_id" class="input input-lg" required>
                    <option value="">-- Välj ett event --</option>
                    <?php foreach ($existingEvents as $event): ?>
                    <option value="<?= $event['id'] ?>" data-year="<?= $event['event_year'] ?>">
                        <?php if ($event['series_names']): ?>[<?= h($event['series_names']) ?>] <?php endif; ?>
                        <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
                        <?php if ($event['location']): ?>- <?= h($event['location']) ?><?php endif; ?>
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <!-- Step 3: Select File -->
            <div class="form-group mb-lg">
                <label for="import_file" class="label label-lg">
                    <span class="badge badge-primary mr-sm">3</span>
                    Välj CSV-fil
                </label>
                <input type="file"
                    id="import_file"
                    name="import_file"
                    class="input input-lg"
                    accept=".csv"
                    required>
                <p class="text-sm text-secondary mt-sm">
                    Max filstorlek: <?= MAX_UPLOAD_SIZE / 1024 / 1024 ?>MB
                </p>
            </div>

            <!-- Step 4: Preview Button -->
            <div class="form-group">
                <button type="submit" class="btn btn--primary btn-lg w-full">
                    <i data-lucide="eye"></i>
                    <span class="badge badge-light mr-sm">4</span>
                    Förhandsgranska import
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Format Info Card -->
<div class="card mt-lg">
    <div class="card-header">
        <h3 class="text-primary">
            <i data-lucide="file-text"></i>
            CSV Format - <?= $activeTab === 'enduro' ? 'Enduro' : ($activeTab === 'dh' ? 'Downhill' : 'XC') ?>
        </h3>
    </div>
    <div class="card-body">
        <p class="text-sm mb-md"><strong>Obligatoriska kolumner:</strong></p>
        <code class="gs-code-block mb-md">
Category, PlaceByCategory, FirstName, LastName, Club, NetTime, Status
        </code>

        <?php if ($activeTab === 'enduro'): ?>
        <p class="text-sm mb-md"><strong>Enduro-specifika kolumner:</strong></p>
        <code class="gs-code-block mb-md">
SS1, SS2, SS3, SS4, SS5... (upp till SS15)
        </code>
        <p class="text-xs text-secondary">
            Stödjer även: Prostage, Powerstage, Stage1, Sträcka1
        </p>

        <?php elseif ($activeTab === 'dh'): ?>
        <p class="text-sm mb-md"><strong>DH-specifika kolumner:</strong></p>
        <code class="gs-code-block mb-md">
Run1, Run2
        </code>
        <p class="text-xs text-secondary">
            Bästa tid av två åk används. Stödjer även: Åk1, Åk2, Kval, Final
        </p>

        <?php else: ?>
        <p class="text-sm mb-md"><strong>XC-specifika kolumner:</strong></p>
        <code class="gs-code-block mb-md">
Lap1, Lap2, Lap3... (varvtider)
        </code>
        <p class="text-xs text-secondary">
            Stödjer även: Varv1, Varv2, Split1, Split2
        </p>
        <?php endif; ?>

        <details class="gs-details mt-lg">
            <summary class="text-sm text-primary">Visa exempel CSV</summary>
            <pre class="gs-code-dark mt-md"><?php
if ($activeTab === 'enduro') {
    echo 'Category,PlaceByCategory,FirstName,LastName,Club,UCI-ID,NetTime,Status,SS1,SS2,SS3
Damer Junior,1,Ella,MÅRTENSSON,Borås CA,10022510347,16:19.16,FIN,2:10.55,1:47.08,1:51.10
Herrar Elite,1,Johan,ANDERSSON,Stockholm CK,10011223344,14:16.42,FIN,1:58.22,1:38.55,1:42.33';
} elseif ($activeTab === 'dh') {
    echo 'Category,PlaceByCategory,FirstName,LastName,Club,UCI-ID,Run1,Run2,NetTime,Status
Herrar Elite,1,Erik,SVENSSON,Stockholm MTB,10012345678,2:15.44,2:12.33,2:12.33,FIN
Damer Elite,1,Anna,JOHANSSON,Göteborg CK,10087654321,2:45.22,2:42.11,2:42.11,FIN';
} else {
    echo 'Category,PlaceByCategory,FirstName,LastName,Club,UCI-ID,NetTime,Status,Lap1,Lap2,Lap3
Herrar Elite,1,Johan,ANDERSSON,Stockholm CK,10011223344,36:16.42,FIN,11:58.22,11:38.55,12:39.65
Damer Elite,1,Maria,SVENSSON,Göteborg CK,10087654321,42:05.67,FIN,13:45.22,14:08.33,14:12.12';
}
?></pre>
        </details>
    </div>
</div>
<?php endif; ?>

<!-- Tools Section -->
<div class="card mt-lg">
    <div class="card-header">
        <h3 class="text-primary">
            <i data-lucide="wrench"></i>
            Verktyg
        </h3>
    </div>
    <div class="card-body">
        <a href="/admin/fix-time-format.php" class="btn btn--secondary">
            <i data-lucide="clock"></i>
            Fixa tidsformat
        </a>
        <span class="text-secondary text-sm ml-sm">Korrigerar tider med fel format</span>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const yearFilter = document.getElementById('year_filter');
    const eventSelect = document.getElementById('event_id');

    if (yearFilter && eventSelect) {
        const allOptions = Array.from(eventSelect.querySelectorAll('option[data-year]'));

        function filterEvents() {
            const selectedYear = yearFilter.value;
            eventSelect.value = '';

            allOptions.forEach(option => {
                if (!selectedYear || option.dataset.year === selectedYear) {
                    option.style.display = '';
                    option.disabled = false;
                } else {
                    option.style.display = 'none';
                    option.disabled = true;
                }
            });
        }

        yearFilter.addEventListener('change', filterEvents);
        filterEvents();
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
