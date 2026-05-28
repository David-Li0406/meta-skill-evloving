<?php
/**
 * Bulk Import Results - Import multiple CSV files at once
 * Allows mapping CSV files to events and processing in batch
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/import-history.php';
require_once __DIR__ . '/../includes/class-calculations.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_once __DIR__ . '/../includes/import-functions.php';
require_once __DIR__ . '/../includes/series-points.php';
require_once __DIR__ . '/../includes/rebuild-rider-stats.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';

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
    LIMIT 1000
");

// Get unique years for filter
$eventYears = array_unique(array_column($existingEvents, 'event_year'));
rsort($eventYears);

// Handle file upload for bulk import
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_files'])) {
    checkCsrf();

    $uploadedFiles = [];
    $files = $_FILES['csv_files'];

    // Reorg files array for easier processing
    $fileCount = count($files['name']);
    for ($i = 0; $i < $fileCount; $i++) {
        if ($files['error'][$i] === UPLOAD_ERR_OK) {
            $extension = strtolower(pathinfo($files['name'][$i], PATHINFO_EXTENSION));
            if ($extension === 'csv') {
                $tempPath = UPLOADS_PATH . '/' . time() . '_bulk_' . $i . '_' . basename($files['name'][$i]);
                if (move_uploaded_file($files['tmp_name'][$i], $tempPath)) {
                    $uploadedFiles[] = [
                        'original_name' => $files['name'][$i],
                        'temp_path' => $tempPath,
                        'size' => $files['size'][$i]
                    ];
                }
            }
        }
    }

    if (count($uploadedFiles) > 0) {
        $_SESSION['bulk_import_files'] = $uploadedFiles;
        $message = count($uploadedFiles) . ' CSV-filer uppladdade. Mappa varje fil till ett event nedan.';
        $messageType = 'success';
    } else {
        $message = 'Inga giltiga CSV-filer hittades.';
        $messageType = 'error';
    }
}

// Handle mapping confirmation
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['start_bulk_import'])) {
    checkCsrf();

    $mappings = $_POST['file_mapping'] ?? [];
    $formats = $_POST['file_format'] ?? [];

    // Validate mappings
    $validMappings = [];
    foreach ($mappings as $fileIndex => $eventId) {
        if (!empty($eventId) && isset($_SESSION['bulk_import_files'][$fileIndex])) {
            $validMappings[$fileIndex] = [
                'event_id' => (int)$eventId,
                'format' => $formats[$fileIndex] ?? 'enduro',
                'file' => $_SESSION['bulk_import_files'][$fileIndex]
            ];
        }
    }

    if (count($validMappings) > 0) {
        $_SESSION['bulk_import_queue'] = $validMappings;
        $_SESSION['bulk_import_results'] = [];
    } else {
        $message = 'Inga giltiga mappningar. Välj event för minst en fil.';
        $messageType = 'error';
    }
}

// Handle single file processing via AJAX
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['process_file'])) {
    header('Content-Type: application/json');

    $fileIndex = (int)$_POST['file_index'];
    $eventId = (int)$_POST['event_id'];
    $format = $_POST['format'] ?? 'enduro';
    $filePath = $_POST['file_path'] ?? '';
    $fileName = $_POST['file_name'] ?? '';

    if (!file_exists($filePath)) {
        echo json_encode(['success' => false, 'error' => 'Filen hittades inte']);
        exit;
    }

    try {
        // Get event info
        $event = $db->getRow("SELECT * FROM events WHERE id = ?", [$eventId]);
        if (!$event) {
            echo json_encode(['success' => false, 'error' => 'Event hittades inte']);
            exit;
        }

        // Create event mapping
        $eventMapping = ['Välj event för alla resultat' => $eventId];

        // Start import
        $importId = startImportHistory(
            $db,
            'results',
            $fileName,
            filesize($filePath),
            $current_admin['username'] ?? 'admin'
        );

        $result = importResultsFromCSVWithMapping(
            $filePath,
            $db,
            $importId,
            $eventMapping,
            null,
            false
        );

        $stats = $result['stats'];
        $matching_stats = $result['matching'];
        $errors = $result['errors'];

        // Auto-save stage names
        if (!empty($result['stage_names'])) {
            $db->update('events', [
                'stage_names' => json_encode($result['stage_names'])
            ], 'id = ?', [$eventId]);
        }

        // Update import history
        $importStatus = ($stats['success'] > 0) ? 'completed' : 'failed';
        updateImportHistory($db, $importId, $stats, $errors, $importStatus);

        // Recalculate results
        $isDH = ($event['discipline'] ?? '') === 'DH' || strpos($event['event_format'] ?? '', 'DH') !== false;
        if ($isDH) {
            $useSwecupDh = ($event['event_format'] ?? '') === 'DH_SWECUP';
            recalculateDHEventResults($db, $eventId, null, $useSwecupDh);
        } else {
            recalculateEventResults($db, $eventId);
        }

        // Sync series results
        syncEventResultsToAllSeries($db, $eventId);

        // Rebuild rider stats
        rebuildEventRiderStats($db->getPdo(), $eventId);

        // Clean up file
        @unlink($filePath);

        echo json_encode([
            'success' => true,
            'stats' => $stats,
            'matching' => $matching_stats,
            'errors' => array_slice($errors, 0, 5), // First 5 errors
            'event_name' => $event['name']
        ]);

    } catch (Exception $e) {
        echo json_encode(['success' => false, 'error' => $e->getMessage()]);
    }

    exit;
}

// Clear bulk import session
if (isset($_GET['clear'])) {
    // Clean up uploaded files
    if (isset($_SESSION['bulk_import_files'])) {
        foreach ($_SESSION['bulk_import_files'] as $file) {
            if (file_exists($file['temp_path'])) {
                @unlink($file['temp_path']);
            }
        }
    }
    unset($_SESSION['bulk_import_files']);
    unset($_SESSION['bulk_import_queue']);
    unset($_SESSION['bulk_import_results']);
    header('Location: /admin/import-bulk-results.php');
    exit;
}

// Page config
$page_title = 'Bulk-import Resultat';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Bulk-import Resultat']
];

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<?php if (isset($_SESSION['bulk_import_queue']) && count($_SESSION['bulk_import_queue']) > 0): ?>
<!-- PROCESSING VIEW -->
<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="loader"></i>
            Importerar <?= count($_SESSION['bulk_import_queue']) ?> filer...
        </h2>
    </div>
    <div class="card-body">
        <div id="import-progress" class="mb-lg">
            <div class="progress-bar">
                <div class="progress-bar-fill" style="width: 0%"></div>
            </div>
            <p class="text-center mt-sm">
                <span id="progress-current">0</span> / <span id="progress-total"><?= count($_SESSION['bulk_import_queue']) ?></span> filer
            </p>
        </div>

        <div id="import-log" class="gs-code-dark" style="height: 400px; overflow-y: auto; padding: var(--space-md); font-size: 13px;">
            <p class="text-secondary">Startar import...</p>
        </div>

        <div id="import-summary" class="mt-lg" style="display: none;">
            <div class="alert alert--success">
                <i data-lucide="check-circle"></i>
                <div>
                    <strong>Import klar!</strong><br>
                    <span id="summary-text"></span>
                </div>
            </div>
            <div class="mt-md">
                <a href="/admin/import-bulk-results.php?clear=1" class="btn btn--primary">
                    <i data-lucide="plus"></i>
                    Importera fler filer
                </a>
                <a href="/admin/results.php" class="btn btn--secondary ml-sm">
                    <i data-lucide="list"></i>
                    Visa resultat
                </a>
            </div>
        </div>
    </div>
</div>

<style>
.progress-bar {
    background: var(--color-border);
    border-radius: var(--radius-full);
    height: 24px;
    overflow: hidden;
}
.progress-bar-fill {
    background: var(--color-accent);
    height: 100%;
    transition: width 0.3s ease;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const queue = <?= json_encode(array_values($_SESSION['bulk_import_queue'])) ?>;
    const log = document.getElementById('import-log');
    const progressFill = document.querySelector('.progress-bar-fill');
    const progressCurrent = document.getElementById('progress-current');
    const progressTotal = document.getElementById('progress-total');
    const summary = document.getElementById('import-summary');
    const summaryText = document.getElementById('summary-text');

    let currentIndex = 0;
    let totalSuccess = 0;
    let totalFailed = 0;
    let totalRows = 0;

    function logMessage(text, type = 'info') {
        const p = document.createElement('p');
        p.className = type === 'error' ? 'text-danger' : (type === 'success' ? 'text-success' : '');
        p.textContent = text;
        log.appendChild(p);
        log.scrollTop = log.scrollHeight;
    }

    async function processNext() {
        if (currentIndex >= queue.length) {
            // Done!
            progressFill.style.width = '100%';
            summary.style.display = 'block';
            summaryText.textContent = `${totalSuccess} filer importerade, ${totalFailed} misslyckades. Totalt ${totalRows} resultat.`;

            // Clear session queue
            fetch('/admin/import-bulk-results.php?clear_queue=1');
            return;
        }

        const item = queue[currentIndex];
        const fileName = item.file.original_name;

        logMessage(`[${currentIndex + 1}/${queue.length}] Importerar: ${fileName}...`);

        try {
            const formData = new FormData();
            formData.append('process_file', '1');
            formData.append('file_index', currentIndex);
            formData.append('event_id', item.event_id);
            formData.append('format', item.format);
            formData.append('file_path', item.file.temp_path);
            formData.append('file_name', fileName);

            const response = await fetch('/admin/import-bulk-results.php', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                const stats = result.stats;
                totalRows += stats.success + stats.updated;
                logMessage(`  OK: ${stats.success} nya, ${stats.updated} uppdaterade, ${stats.skipped} hoppade, ${stats.failed} misslyckade`, 'success');
                totalSuccess++;
            } else {
                logMessage(`  FEL: ${result.error}`, 'error');
                totalFailed++;
            }

        } catch (e) {
            logMessage(`  FEL: ${e.message}`, 'error');
            totalFailed++;
        }

        currentIndex++;
        progressCurrent.textContent = currentIndex;
        progressFill.style.width = ((currentIndex / queue.length) * 100) + '%';

        // Process next with small delay
        setTimeout(processNext, 100);
    }

    // Start processing
    processNext();
});
</script>

<?php
// Clear queue after rendering
unset($_SESSION['bulk_import_queue']);
?>

<?php elseif (isset($_SESSION['bulk_import_files']) && count($_SESSION['bulk_import_files']) > 0): ?>
<!-- MAPPING VIEW -->
<div class="card">
    <div class="card-header">
        <div class="flex justify-between items-center">
            <h2 class="text-primary">
                <i data-lucide="link"></i>
                Mappa filer till events
            </h2>
            <a href="/admin/import-bulk-results.php?clear=1" class="btn btn--ghost btn--sm">
                <i data-lucide="x"></i>
                Avbryt
            </a>
        </div>
    </div>
    <div class="card-body">
        <p class="mb-lg"><?= count($_SESSION['bulk_import_files']) ?> filer uppladdade. Mappa varje fil till ett event:</p>

        <form method="POST" id="mapping-form">
            <?= csrf_field() ?>

            <!-- Year filter -->
            <div class="form-group mb-lg" style="max-width: 200px;">
                <label class="label">Filtrera events efter år:</label>
                <select id="year-filter" class="input">
                    <option value="">Alla år</option>
                    <?php foreach ($eventYears as $year): ?>
                    <option value="<?= $year ?>" <?= $year == date('Y') ? 'selected' : '' ?>><?= $year ?></option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th style="width: 30px;">
                                <input type="checkbox" id="select-all" checked>
                            </th>
                            <th>Fil</th>
                            <th>Format</th>
                            <th>Event</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($_SESSION['bulk_import_files'] as $index => $file): ?>
                        <tr>
                            <td>
                                <input type="checkbox" class="file-select" data-index="<?= $index ?>" checked>
                            </td>
                            <td>
                                <strong><?= h($file['original_name']) ?></strong>
                                <br><span class="text-sm text-secondary"><?= number_format($file['size'] / 1024, 1) ?> KB</span>
                            </td>
                            <td>
                                <select name="file_format[<?= $index ?>]" class="input input-sm" style="width: 120px;">
                                    <option value="enduro">Enduro</option>
                                    <option value="dh">Downhill</option>
                                    <option value="xc">XC</option>
                                </select>
                            </td>
                            <td>
                                <select name="file_mapping[<?= $index ?>]" class="input event-select" data-index="<?= $index ?>" style="min-width: 300px;">
                                    <option value="">-- Välj event --</option>
                                    <?php foreach ($existingEvents as $event): ?>
                                    <option value="<?= $event['id'] ?>" data-year="<?= $event['event_year'] ?>">
                                        <?php if ($event['series_names']): ?>[<?= h($event['series_names']) ?>] <?php endif; ?>
                                        <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
                                    </option>
                                    <?php endforeach; ?>
                                </select>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <div class="mt-lg flex gap-md">
                <button type="submit" name="start_bulk_import" class="btn btn--primary btn-lg">
                    <i data-lucide="play"></i>
                    Starta import av valda filer
                </button>
                <a href="/admin/import-bulk-results.php?clear=1" class="btn btn--secondary btn-lg">
                    <i data-lucide="x"></i>
                    Avbryt
                </a>
            </div>
        </form>
    </div>
</div>

<!-- Quick Match Section -->
<div class="card mt-lg">
    <div class="card-header">
        <h3 class="text-primary">
            <i data-lucide="zap"></i>
            Auto-matcha efter filnamn
        </h3>
    </div>
    <div class="card-body">
        <p class="text-sm text-secondary mb-md">
            Tryck för att automatiskt matcha filer mot events baserat på filnamn.
            Fungerar bäst om filnamnen innehåller eventnamn eller datum.
        </p>
        <button type="button" id="auto-match" class="btn btn--secondary">
            <i data-lucide="wand-2"></i>
            Auto-matcha
        </button>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const yearFilter = document.getElementById('year-filter');
    const eventSelects = document.querySelectorAll('.event-select');
    const selectAll = document.getElementById('select-all');
    const fileSelects = document.querySelectorAll('.file-select');
    const autoMatchBtn = document.getElementById('auto-match');

    // Year filter
    function filterEvents() {
        const year = yearFilter.value;
        eventSelects.forEach(select => {
            const options = select.querySelectorAll('option[data-year]');
            options.forEach(opt => {
                if (!year || opt.dataset.year === year) {
                    opt.style.display = '';
                    opt.disabled = false;
                } else {
                    opt.style.display = 'none';
                    opt.disabled = true;
                }
            });
        });
    }
    yearFilter.addEventListener('change', filterEvents);
    filterEvents();

    // Select all
    selectAll.addEventListener('change', function() {
        fileSelects.forEach(cb => cb.checked = this.checked);
        updateMappingState();
    });

    fileSelects.forEach(cb => {
        cb.addEventListener('change', updateMappingState);
    });

    function updateMappingState() {
        fileSelects.forEach(cb => {
            const index = cb.dataset.index;
            const select = document.querySelector(`select[name="file_mapping[${index}]"]`);
            const formatSelect = document.querySelector(`select[name="file_format[${index}]"]`);
            if (select) select.disabled = !cb.checked;
            if (formatSelect) formatSelect.disabled = !cb.checked;
        });
    }

    // Auto-match
    autoMatchBtn.addEventListener('click', function() {
        const files = <?= json_encode(array_column($_SESSION['bulk_import_files'], 'original_name')) ?>;
        const events = <?= json_encode(array_map(function($e) {
            return ['id' => $e['id'], 'name' => $e['name'], 'date' => $e['date']];
        }, $existingEvents)) ?>;

        let matched = 0;

        files.forEach((fileName, index) => {
            const select = document.querySelector(`select[name="file_mapping[${index}]"]`);
            if (!select || select.value) return; // Skip if already matched

            const fileNameLower = fileName.toLowerCase();

            // Try to match by event name
            for (const event of events) {
                const eventNameParts = event.name.toLowerCase().split(/[\s-]+/);
                let matchScore = 0;

                for (const part of eventNameParts) {
                    if (part.length > 3 && fileNameLower.includes(part)) {
                        matchScore++;
                    }
                }

                // Also check for date match (YYYY-MM-DD or YYYYMMDD)
                const dateMatch = event.date.replace(/-/g, '');
                if (fileNameLower.includes(event.date) || fileNameLower.includes(dateMatch)) {
                    matchScore += 3;
                }

                if (matchScore >= 2) {
                    select.value = event.id;
                    matched++;
                    break;
                }
            }
        });

        alert(`Auto-matchade ${matched} filer.`);
    });
});
</script>

<?php else: ?>
<!-- UPLOAD VIEW -->
<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="upload"></i>
            Ladda upp CSV-filer
        </h2>
    </div>
    <div class="card-body">
        <form method="POST" enctype="multipart/form-data">
            <?= csrf_field() ?>

            <div class="form-group mb-lg">
                <label class="label label-lg">
                    Välj en eller flera CSV-filer:
                </label>
                <input type="file"
                    name="csv_files[]"
                    class="input input-lg"
                    accept=".csv"
                    multiple
                    required>
                <p class="text-sm text-secondary mt-sm">
                    Du kan välja upp till 200 filer samtidigt. Max <?= MAX_UPLOAD_SIZE / 1024 / 1024 ?>MB per fil.
                </p>
            </div>

            <button type="submit" class="btn btn--primary btn-lg">
                <i data-lucide="upload"></i>
                Ladda upp filer
            </button>
        </form>
    </div>
</div>

<!-- Info Card -->
<div class="card mt-lg">
    <div class="card-header">
        <h3 class="text-primary">
            <i data-lucide="info"></i>
            Hur det fungerar
        </h3>
    </div>
    <div class="card-body">
        <ol class="space-y-md">
            <li><strong>1. Ladda upp</strong> - Välj alla CSV-filer du vill importera</li>
            <li><strong>2. Mappa</strong> - Koppla varje fil till rätt event</li>
            <li><strong>3. Importera</strong> - Alla filer processas automatiskt</li>
        </ol>

        <div class="alert alert--info mt-lg">
            <i data-lucide="lightbulb"></i>
            <div>
                <strong>Tips:</strong> Namnge dina filer med eventnamn eller datum (t.ex. "2024-05-15_Åre_Enduro.csv")
                så kan systemet automatiskt matcha dem mot rätt event.
            </div>
        </div>
    </div>
</div>

<!-- Link to single import -->
<div class="card mt-lg">
    <div class="card-body">
        <p class="text-secondary">
            Vill du importera en enda fil med förhandsgranskning?
            <a href="/admin/import-results.php" class="text-primary">Använd vanlig import</a>
        </p>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
