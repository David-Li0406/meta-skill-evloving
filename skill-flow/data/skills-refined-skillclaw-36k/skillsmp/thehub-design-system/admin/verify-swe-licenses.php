<?php
/**
 * Verify SWE Licenses Tool
 * Upload CSV to find and verify Swedish license numbers
 * Similar to search-uci-id.php but for SWE licenses
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$results = [];
$headers = [];
$matchStats = ['exact' => 0, 'fuzzy' => 0, 'partial' => 0, 'not_found' => 0, 'existing' => 0];
$message = '';
$messageType = '';

// Column mapping defaults
$colMapping = [
    'firstname' => 0,
    'lastname' => 1,
    'club' => 2,
    'birth_year' => 3,
    'license' => 4
];

/**
 * Find column index by possible header names
 */
function findColumn($headers, $possibleNames) {
    foreach ($headers as $index => $header) {
        $normalized = strtolower(trim($header));
        $normalized = str_replace([' ', '-', '_'], '', $normalized);
        foreach ($possibleNames as $name) {
            $nameNorm = str_replace([' ', '-', '_'], '', strtolower($name));
            if ($normalized === $nameNorm || strpos($normalized, $nameNorm) !== false) {
                return $index;
            }
        }
    }
    return 0;
}

/**
 * Normalize name for matching
 */
function normalizeName($name) {
    $name = mb_strtolower(trim($name), 'UTF-8');
    $name = preg_replace('/[^a-zåäöéü\s]/u', '', $name);
    return trim($name);
}

/**
 * Find rider in database by name matching
 */
function findRiderByName($db, $firstname, $lastname, $club = '', $birthYear = '') {
    $firstNorm = normalizeName($firstname);
    $lastNorm = normalizeName($lastname);

    if (empty($firstNorm) || empty($lastNorm)) {
        return null;
    }

    // Try exact match first
    $rider = $db->getRow("
        SELECT r.*, c.name as club_name
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE LOWER(r.firstname) = ? AND LOWER(r.lastname) = ?
        ORDER BY r.license_number IS NOT NULL DESC, r.id DESC
        LIMIT 1
    ", [$firstNorm, $lastNorm]);

    if ($rider) {
        return ['rider' => $rider, 'match_type' => 'exact'];
    }

    // Try fuzzy match with birth year
    if (!empty($birthYear)) {
        $rider = $db->getRow("
            SELECT r.*, c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.birth_year = ?
            AND (
                SOUNDEX(r.firstname) = SOUNDEX(?) OR
                LEVENSHTEIN(LOWER(r.firstname), ?) <= 2
            )
            AND (
                SOUNDEX(r.lastname) = SOUNDEX(?) OR
                LEVENSHTEIN(LOWER(r.lastname), ?) <= 2
            )
            ORDER BY r.license_number IS NOT NULL DESC
            LIMIT 1
        ", [$birthYear, $firstname, $firstNorm, $lastname, $lastNorm]);

        if ($rider) {
            return ['rider' => $rider, 'match_type' => 'fuzzy'];
        }
    }

    // Try partial match (first letters + last name)
    $firstPrefix = mb_substr($firstNorm, 0, 3, 'UTF-8');
    if (strlen($firstPrefix) >= 2) {
        $rider = $db->getRow("
            SELECT r.*, c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE LOWER(r.firstname) LIKE ? AND LOWER(r.lastname) = ?
            ORDER BY r.license_number IS NOT NULL DESC
            LIMIT 1
        ", [$firstPrefix . '%', $lastNorm]);

        if ($rider) {
            return ['rider' => $rider, 'match_type' => 'partial'];
        }
    }

    return null;
}

/**
 * Validate SWE license format
 */
function validateSweLicense($license) {
    $license = trim($license);
    if (empty($license)) {
        return ['valid' => false, 'normalized' => '', 'error' => 'empty'];
    }

    // Remove common formatting
    $normalized = preg_replace('/[\s\-]/', '', $license);

    // Check if it starts with SWE
    if (preg_match('/^SWE\d{7,11}$/i', $normalized)) {
        return ['valid' => true, 'normalized' => strtoupper($normalized), 'format' => 'SWE-ID'];
    }

    // Check if it's just numbers (11 digits = personnummer)
    if (preg_match('/^\d{10,11}$/', $normalized)) {
        return ['valid' => true, 'normalized' => 'SWE' . $normalized, 'format' => 'Personnummer'];
    }

    // Check new format SWE-YYYY-NNNNN
    if (preg_match('/^SWE(\d{4})(\d{5})$/i', $normalized, $m)) {
        return ['valid' => true, 'normalized' => 'SWE-' . $m[1] . '-' . $m[2], 'format' => 'SWE-YYYY-ID'];
    }

    return ['valid' => false, 'normalized' => $normalized, 'error' => 'invalid_format'];
}

// Handle selection updates via AJAX
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'update_selection') {
    header('Content-Type: application/json');
    $selected = json_decode($_POST['selected'] ?? '[]', true);
    $_SESSION['swe_lookup_selected'] = $selected;
    echo json_encode(['success' => true]);
    exit;
}

// Handle CSV export
if (isset($_GET['export']) && !empty($_SESSION['swe_lookup_results'])) {
    $exportData = $_SESSION['swe_lookup_results'];
    $exportHeaders = $_SESSION['swe_lookup_headers'];
    $selected = $_SESSION['swe_lookup_selected'] ?? array_keys($exportData);

    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="riders_swe_licenses.csv"');

    $output = fopen('php://output', 'w');
    fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM

    // Write header
    fputcsv($output, $exportHeaders, ';');

    // Write only selected data
    foreach ($exportData as $index => $row) {
        if (in_array($index, $selected)) {
            fputcsv($output, $row['data'], ';');
        }
    }

    fclose($output);
    exit;
}

// Handle file upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_file'])) {
    checkCsrf();

    $file = $_FILES['csv_file'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        $message = 'Filuppladdning misslyckades';
        $messageType = 'error';
    } else {
        $content = file_get_contents($file['tmp_name']);

        // Detect encoding and convert to UTF-8
        $encoding = mb_detect_encoding($content, ['UTF-8', 'ISO-8859-1', 'Windows-1252'], true);
        if ($encoding && $encoding !== 'UTF-8') {
            $content = mb_convert_encoding($content, 'UTF-8', $encoding);
        }

        // Remove BOM if present
        $content = preg_replace('/^\xEF\xBB\xBF/', '', $content);

        $lines = explode("\n", $content);

        // Detect separator
        $firstLine = $lines[0] ?? '';
        $separator = ';';
        if (substr_count($firstLine, ',') > substr_count($firstLine, ';')) {
            $separator = ',';
        } elseif (substr_count($firstLine, "\t") > substr_count($firstLine, ';')) {
            $separator = "\t";
        }

        // Parse header
        $headers = str_getcsv(trim($lines[0]), $separator);
        $headers = array_map('trim', $headers);

        // Auto-detect columns
        $colMapping['firstname'] = findColumn($headers, ['förnamn', 'firstname', 'first_name', 'first name', 'fname']);
        $colMapping['lastname'] = findColumn($headers, ['efternamn', 'lastname', 'last_name', 'last name', 'surname', 'lname']);
        $colMapping['club'] = findColumn($headers, ['klubb', 'club', 'team', 'förening', 'organisation']);
        $colMapping['birth_year'] = findColumn($headers, ['födelseår', 'birthyear', 'birth_year', 'år', 'year', 'född']);
        $colMapping['license'] = findColumn($headers, ['licens', 'license', 'licensnummer', 'license_number', 'swe_id', 'sweid', 'uci_id']);

        // Add SWE License column to headers if not present
        $licenseColName = 'SWE_License';
        if (!in_array($licenseColName, $headers)) {
            $headers[] = $licenseColName;
            $colMapping['license'] = count($headers) - 1;
        }

        // Process data rows
        $processedResults = [];

        for ($i = 1; $i < count($lines); $i++) {
            $line = trim($lines[$i]);
            if (empty($line)) continue;

            $parts = str_getcsv($line, $separator);

            $firstname = trim($parts[$colMapping['firstname']] ?? '');
            $lastname = trim($parts[$colMapping['lastname']] ?? '');
            $club = trim($parts[$colMapping['club']] ?? '');
            $birthYear = trim($parts[$colMapping['birth_year']] ?? '');
            $existingLicense = trim($parts[$colMapping['license']] ?? '');

            if (empty($firstname) && empty($lastname)) {
                continue;
            }

            // Validate existing license
            $licenseValidation = validateSweLicense($existingLicense);

            // Initialize result
            $resultRow = [
                'data' => $parts,
                'firstname' => $firstname,
                'lastname' => $lastname,
                'club' => $club,
                'birth_year' => $birthYear,
                'input_license' => $existingLicense,
                'found_license' => '',
                'match_type' => 'not_found',
                'matched_rider' => null,
                'license_status' => 'missing'
            ];

            // If already has valid license
            if ($licenseValidation['valid']) {
                $resultRow['found_license'] = $licenseValidation['normalized'];
                $resultRow['license_status'] = 'valid';
                $resultRow['match_type'] = 'existing';
                $matchStats['existing']++;
            } else {
                // Search for rider in database
                $match = findRiderByName($db, $firstname, $lastname, $club, $birthYear);

                if ($match) {
                    $rider = $match['rider'];
                    $resultRow['matched_rider'] = $rider;
                    $resultRow['match_type'] = $match['match_type'];

                    if (!empty($rider['license_number'])) {
                        $resultRow['found_license'] = $rider['license_number'];
                        $resultRow['license_status'] = 'found';
                    } else {
                        $resultRow['license_status'] = 'rider_no_license';
                    }

                    $matchStats[$match['match_type']]++;
                } else {
                    $matchStats['not_found']++;
                }
            }

            // Update the license column in data
            while (count($resultRow['data']) <= $colMapping['license']) {
                $resultRow['data'][] = '';
            }
            if (!empty($resultRow['found_license'])) {
                $resultRow['data'][$colMapping['license']] = $resultRow['found_license'];
            }

            $processedResults[] = $resultRow;
        }

        // Store for export
        $_SESSION['swe_lookup_results'] = $processedResults;
        $_SESSION['swe_lookup_headers'] = $headers;
        $_SESSION['swe_lookup_selected'] = array_keys($processedResults);

        $results = $processedResults;

        $message = 'Bearbetade ' . count($results) . ' rader';
        $messageType = 'success';
    }
}

// Get stored results if available
if (empty($results) && !empty($_SESSION['swe_lookup_results'])) {
    $results = $_SESSION['swe_lookup_results'];
    $headers = $_SESSION['swe_lookup_headers'] ?? [];

    // Recalculate stats
    foreach ($results as $row) {
        if (isset($row['match_type'])) {
            $matchStats[$row['match_type']] = ($matchStats[$row['match_type']] ?? 0) + 1;
        }
    }
}

// Group results by match type for display
$groupedResults = [
    'partial' => [],
    'fuzzy' => [],
    'not_found' => [],
    'existing' => [],
    'exact' => []
];

foreach ($results as $index => $row) {
    $type = $row['match_type'] ?? 'not_found';
    if (isset($groupedResults[$type])) {
        $groupedResults[$type][$index] = $row;
    }
}

$displayOrder = ['partial', 'fuzzy', 'not_found', 'existing', 'exact'];
$groupLabels = [
    'partial' => ['label' => 'Delvis matchade', 'icon' => 'alert-triangle', 'badge' => 'badge-warning', 'desc' => 'Förnamn börjar lika, kontrollera manuellt'],
    'fuzzy' => ['label' => 'Fuzzy matchade', 'icon' => 'search', 'badge' => 'badge-info', 'desc' => 'Matchade via födelseår + liknande namn'],
    'not_found' => ['label' => 'Ej hittade', 'icon' => 'user-x', 'badge' => 'badge-danger', 'desc' => 'Finns ej i databasen'],
    'existing' => ['label' => 'Har redan licens', 'icon' => 'check-circle', 'badge' => 'badge-secondary', 'desc' => 'Redan giltig licens i filen'],
    'exact' => ['label' => 'Exakt matchade', 'icon' => 'user-check', 'badge' => 'badge-success', 'desc' => 'Perfekt namnmatchning']
];

// Page setup
$page_title = 'Verifiera SWE-licenser';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Verifiera SWE-licenser']
];
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Upload Form -->
<div class="card mb-lg">
    <div class="card-header">
        <h2>
            <i data-lucide="upload"></i>
            Ladda upp CSV-fil
        </h2>
    </div>
    <div class="card-body">
        <form method="POST" enctype="multipart/form-data" class="flex gap-md items-end flex-wrap">
            <?= csrf_field() ?>
            <div class="form-group" style="flex: 1; min-width: 250px;">
                <label class="label">CSV-fil med deltagare</label>
                <input type="file" name="csv_file" accept=".csv,.txt" class="input" required>
                <small class="text-secondary">Fil med kolumner: Förnamn, Efternamn, Klubb, Födelseår (valfritt), Licens (valfritt)</small>
            </div>
            <button type="submit" class="btn btn-primary">
                <i data-lucide="search"></i>
                Verifiera licenser
            </button>
        </form>
    </div>
</div>

<?php if (!empty($results)): ?>

<!-- Stats -->
<div class="grid grid-cols-2 gs-md-grid-cols-5 gap-md mb-lg">
    <div class="stat-card">
        <div class="stat-number"><?= count($results) ?></div>
        <div class="stat-label">Totalt</div>
    </div>
    <div class="stat-card" style="border-left: 3px solid var(--color-success);">
        <div class="stat-number text-success"><?= $matchStats['exact'] ?? 0 ?></div>
        <div class="stat-label">Exakta</div>
    </div>
    <div class="stat-card" style="border-left: 3px solid var(--color-warning);">
        <div class="stat-number text-warning"><?= ($matchStats['fuzzy'] ?? 0) + ($matchStats['partial'] ?? 0) ?></div>
        <div class="stat-label">Fuzzy/Delvis</div>
    </div>
    <div class="stat-card" style="border-left: 3px solid var(--color-secondary);">
        <div class="stat-number"><?= $matchStats['existing'] ?? 0 ?></div>
        <div class="stat-label">Redan licens</div>
    </div>
    <div class="stat-card" style="border-left: 3px solid var(--color-danger);">
        <div class="stat-number text-danger"><?= $matchStats['not_found'] ?? 0 ?></div>
        <div class="stat-label">Ej hittade</div>
    </div>
</div>

<!-- Export Button -->
<div class="flex gap-md mb-lg justify-end">
    <a href="?export=1" class="btn btn-success">
        <i data-lucide="download"></i>
        Exportera CSV med licenser
    </a>
    <form method="POST" style="display: inline;">
        <?= csrf_field() ?>
        <button type="submit" name="clear" class="btn btn-secondary">
            <i data-lucide="x"></i>
            Rensa
        </button>
    </form>
</div>

<!-- Results grouped by match type -->
<?php foreach ($displayOrder as $type): ?>
    <?php
    $group = $groupedResults[$type];
    if (empty($group)) continue;
    $info = $groupLabels[$type];
    ?>

    <div class="card mb-lg">
        <div class="card-header">
            <h3>
                <i data-lucide="<?= $info['icon'] ?>"></i>
                <?= $info['label'] ?>
                <span class="badge <?= $info['badge'] ?> ml-sm"><?= count($group) ?></span>
            </h3>
            <small class="text-secondary"><?= $info['desc'] ?></small>
        </div>
        <div class="card-body" style="padding: 0;">
            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th style="width: 40px;">
                                <input type="checkbox" checked class="group-checkbox" data-group="<?= $type ?>">
                            </th>
                            <th>Namn i fil</th>
                            <th>Klubb</th>
                            <th>Födelseår</th>
                            <th>Matchad åkare</th>
                            <th>Licens</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($group as $index => $row): ?>
                        <tr>
                            <td>
                                <input type="checkbox" name="selected[]" value="<?= $index ?>" checked class="row-checkbox" data-index="<?= $index ?>">
                            </td>
                            <td>
                                <strong><?= h($row['firstname'] . ' ' . $row['lastname']) ?></strong>
                            </td>
                            <td><?= h($row['club'] ?: '-') ?></td>
                            <td><?= h($row['birth_year'] ?: '-') ?></td>
                            <td>
                                <?php if ($row['matched_rider']): ?>
                                    <a href="/rider.php?id=<?= $row['matched_rider']['id'] ?>" target="_blank" class="text-primary" style="font-weight: 600;">
                                        <?= h($row['matched_rider']['firstname'] . ' ' . $row['matched_rider']['lastname']) ?>
                                    </a>
                                    <?php if (!empty($row['matched_rider']['club_name'])): ?>
                                    <br><small class="text-secondary"><?= h($row['matched_rider']['club_name']) ?></small>
                                    <?php endif; ?>
                                <?php elseif ($type === 'existing'): ?>
                                    <span class="text-secondary">-</span>
                                <?php else: ?>
                                    <span class="text-danger">Ej i databas</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php if (!empty($row['found_license'])): ?>
                                    <code class="text-success" style="font-weight: 600;"><?= h($row['found_license']) ?></code>
                                <?php elseif ($row['license_status'] === 'rider_no_license'): ?>
                                    <span class="badge badge-warning">Åkare saknar licens</span>
                                <?php else: ?>
                                    <span class="text-secondary">-</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
<?php endforeach; ?>

<script>
// Handle group checkboxes
document.querySelectorAll('.group-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        const group = this.dataset.group;
        const rows = this.closest('.card').querySelectorAll('.row-checkbox');
        rows.forEach(row => row.checked = this.checked);
        updateSelection();
    });
});

// Handle individual checkboxes
document.querySelectorAll('.row-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', updateSelection);
});

function updateSelection() {
    const selected = [];
    document.querySelectorAll('.row-checkbox:checked').forEach(cb => {
        selected.push(parseInt(cb.dataset.index));
    });

    // Send to server
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'action=update_selection&selected=' + encodeURIComponent(JSON.stringify(selected)) + '&csrf_token=<?= csrf_token() ?>'
    });
}
</script>

<?php endif; ?>

<?php if (isset($_POST['clear'])): ?>
<?php
unset($_SESSION['swe_lookup_results']);
unset($_SESSION['swe_lookup_headers']);
unset($_SESSION['swe_lookup_selected']);
header('Location: /admin/verify-swe-licenses.php');
exit;
?>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
