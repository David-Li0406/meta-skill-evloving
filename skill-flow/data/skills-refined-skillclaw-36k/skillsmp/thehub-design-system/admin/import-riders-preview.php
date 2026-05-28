<?php
/**
 * Import Riders Preview - Förhandsgranskning innan import
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/helpers.php';
require_once __DIR__ . '/../includes/club-membership.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';

// Check if we have a file to preview
if (!isset($_SESSION['import_riders_file']) || !file_exists($_SESSION['import_riders_file'])) {
    header('Location: /admin/import/riders');
    exit;
}

$seasonYear = $_SESSION['import_riders_season'] ?? (int)date('Y');
$createMissing = $_SESSION['import_riders_create_missing'] ?? true;

// Parse CSV and analyze
$previewData = [];
$matchingStats = [
    'total_rows' => 0,
    'riders_existing' => 0,
    'riders_new' => 0,
    'riders_update' => 0,
    'clubs_existing' => 0,
    'clubs_new' => 0,
    'clubs_list' => [],
    'uci_found' => 0,
    'uci_existing' => 0,
    'uci_not_found' => 0
];

/**
 * Normalize string for comparison (for UCI ID lookup)
 */
function normalizeStringForSearch($str) {
    $str = mb_strtolower(trim($str), 'UTF-8');
    $str = preg_replace('/[åä]/u', 'a', $str);
    $str = preg_replace('/[ö]/u', 'o', $str);
    $str = preg_replace('/[é]/u', 'e', $str);
    $str = preg_replace('/[^a-z0-9]/u', '', $str);
    return $str;
}

/**
 * Find rider in database to get UCI ID (license_number)
 */
function findRiderForUciId($db, $firstname, $lastname, $club, $birthYear = null) {
    $normFirstname = normalizeStringForSearch($firstname);
    $normLastname = normalizeStringForSearch($lastname);
    $normClub = normalizeStringForSearch($club);

    // Strategy 1: Exact match with birth year
    if ($birthYear) {
        try {
            $riders = $db->getAll("
                SELECT r.id, r.firstname, r.lastname, r.license_number,
                    r.birth_year, c.name as club_name
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE LOWER(r.firstname) = ?
                    AND LOWER(r.lastname) = ?
                    AND r.birth_year = ?
                    AND r.license_number IS NOT NULL
                    AND r.license_number != ''
                ORDER BY r.license_year DESC
                LIMIT 1
            ", [strtolower($firstname), strtolower($lastname), $birthYear]);

            if (!empty($riders)) {
                return array_merge($riders[0], ['match_type' => 'exact', 'confidence' => 100]);
            }
        } catch (Exception $e) {}
    }

    // Strategy 2: Exact match with club
    if (!empty($club)) {
        try {
            $riders = $db->getAll("
                SELECT r.id, r.firstname, r.lastname, r.license_number,
                    r.birth_year, c.name as club_name
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE LOWER(r.firstname) = ?
                    AND LOWER(r.lastname) = ?
                    AND LOWER(c.name) LIKE ?
                    AND r.license_number IS NOT NULL
                    AND r.license_number != ''
                ORDER BY r.license_year DESC
                LIMIT 1
            ", [strtolower($firstname), strtolower($lastname), '%' . strtolower($club) . '%']);

            if (!empty($riders)) {
                return array_merge($riders[0], ['match_type' => 'exact', 'confidence' => 95]);
            }
        } catch (Exception $e) {}
    }

    // Strategy 3: Exact name match (any club)
    try {
        $riders = $db->getAll("
            SELECT r.id, r.firstname, r.lastname, r.license_number,
                r.birth_year, c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE LOWER(r.firstname) = ?
                AND LOWER(r.lastname) = ?
                AND r.license_number IS NOT NULL
                AND r.license_number != ''
            ORDER BY r.license_year DESC
            LIMIT 1
        ", [strtolower($firstname), strtolower($lastname)]);

        if (!empty($riders)) {
            $rider = $riders[0];
            $confidence = empty($club) ? 90 : (stripos($rider['club_name'] ?? '', $club) !== false ? 95 : 80);
            return array_merge($rider, ['match_type' => 'exact', 'confidence' => $confidence]);
        }
    } catch (Exception $e) {}

    // Strategy 4: Fuzzy match (normalized names)
    try {
        $riders = $db->getAll("
            SELECT r.id, r.firstname, r.lastname, r.license_number,
                r.birth_year, c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.license_number IS NOT NULL
                AND r.license_number != ''
            ORDER BY r.license_year DESC
            LIMIT 500
        ", []);

        $bestMatch = null;
        $bestScore = 0;

        foreach ($riders as $rider) {
            $riderNormFirst = normalizeStringForSearch($rider['firstname']);
            $riderNormLast = normalizeStringForSearch($rider['lastname']);

            if ($riderNormFirst === $normFirstname && $riderNormLast === $normLastname) {
                $score = 85;
                if (!empty($normClub) && !empty($rider['club_name'])) {
                    $riderNormClub = normalizeStringForSearch($rider['club_name']);
                    if (strpos($riderNormClub, $normClub) !== false || strpos($normClub, $riderNormClub) !== false) {
                        $score = 90;
                    }
                }
                if ($birthYear && $rider['birth_year'] == $birthYear) {
                    $score = 95;
                }
                if ($score > $bestScore) {
                    $bestScore = $score;
                    $bestMatch = array_merge($rider, ['match_type' => 'fuzzy', 'confidence' => $score]);
                }
            }
        }

        if ($bestMatch) {
            return $bestMatch;
        }
    } catch (Exception $e) {}

    return null;
}

/**
 * Auto-detect CSV separator
 */
function detectSeparator($filepath) {
    $handle = fopen($filepath, 'r');
    $firstLine = fgets($handle);
    fclose($handle);

    $separators = [
        ',' => substr_count($firstLine, ','),
        ';' => substr_count($firstLine, ';'),
        "\t" => substr_count($firstLine, "\t"),
    ];

    arsort($separators);
    return array_key_first($separators);
}

/**
 * Ensure UTF-8 encoding
 */
function ensureUTF8Preview($filepath) {
    $content = file_get_contents($filepath);
    $content = preg_replace('/^\xEF\xBB\xBF/', '', $content);

    if (mb_check_encoding($content, 'UTF-8')) {
        if (preg_match('/[\xC0-\xFF]/', $content) && !preg_match('/[\xC0-\xFF][\x80-\xBF]/', $content)) {
            $content = mb_convert_encoding($content, 'UTF-8', 'Windows-1252');
            file_put_contents($filepath, $content);
        }
    } else {
        $content = mb_convert_encoding($content, 'UTF-8', 'Windows-1252');
        file_put_contents($filepath, $content);
    }
}

try {
    ensureUTF8Preview($_SESSION['import_riders_file']);

    $handle = fopen($_SESSION['import_riders_file'], 'r');
    if (!$handle) {
        throw new Exception('Kunde inte öppna filen');
    }

    $separator = detectSeparator($_SESSION['import_riders_file']);
    $header = fgetcsv($handle, 0, $separator);

    if (!$header) {
        throw new Exception('Tom fil eller ogiltigt format');
    }

    // Store original headers for display
    $originalHeader = $header;

    // Normalize header
    $header = array_map(function($col) {
        $col = mb_strtolower(trim($col), 'UTF-8');
        $col = preg_replace('/^\xEF\xBB\xBF/', '', $col);
        return $col;
    }, $header);

    // Define all possible column mappings with their matching patterns
    $columnPatterns = [
        'firstname' => ['förnamn', 'fornamn', 'firstname', 'first_name', 'first name', 'fname', 'given name', 'givenname'],
        'lastname' => ['efternamn', 'lastname', 'last_name', 'last name', 'lname', 'surname', 'family name', 'familyname'],
        'fullname' => ['namn', 'name', 'fullname', 'full name', 'åkare', 'akare', 'rider', 'deltagare', 'participant'],
        'gender' => ['kön', 'kon', 'gender', 'sex'],
        'club' => ['klubb', 'club', 'team', 'förening', 'forening', 'organisation', 'huvudförening', 'huvudforening'],
        'birth_year' => ['födelseår', 'fodelsear', 'birthyear', 'birth_year', 'year', 'år', 'ar', 'född', 'fodd', 'ålder', 'alder', 'age'],
        'birthday' => ['födelsedatum', 'födelsdag', 'birthday', 'birthdate', 'date of birth', 'dob'],
        'email' => ['email', 'e-post', 'epost', 'epostadress', 'mail', 'e-mail'],
        'uci_id' => ['medlemsnummer', 'uci', 'ucikod', 'licens', 'license', 'license_number', 'licensnummer', 'uci_id', 'uciid', 'id'],
        'nationality' => ['nationalitet', 'nationality', 'land', 'country', 'nation'],
        'district' => ['distrikt', 'district', 'region', 'län', 'lan'],
        // License fields
        'license_type' => ['licenstyp', 'license_type', 'licensetype', 'licensetyp', 'typ', 'type'],
        'license_year' => ['licensår', 'licensar', 'license_year', 'licenseyear', 'licensyear', 'licyear'],
        'license_category' => ['licenskategori', 'license_category', 'licensecategory', 'kategori', 'category'],
        'discipline' => ['gren', 'discipline', 'disciplin', 'sport'],
        // SCF discipline columns (individual checkboxes)
        'discipline_road' => ['road'],
        'discipline_track' => ['track'],
        'discipline_bmx' => ['bmx'],
        'discipline_cx' => ['cx'],
        'discipline_trial' => ['trial'],
        'discipline_para' => ['para'],
        'discipline_mtb' => ['mtb'],
        'discipline_ecycling' => ['e-cycling', 'ecycling'],
        'discipline_gravel' => ['gravel']
    ];

    // Auto-detect column mappings
    $colMap = [];
    $detectedColumns = []; // Track what was auto-detected

    foreach ($header as $idx => $col) {
        $colNorm = str_replace([' ', '-', '_'], '', $col);
        foreach ($columnPatterns as $field => $patterns) {
            if (!isset($colMap[$field])) {
                foreach ($patterns as $pattern) {
                    $patternNorm = str_replace([' ', '-', '_'], '', $pattern);
                    if ($colNorm === $patternNorm || strpos($colNorm, $patternNorm) !== false || strpos($patternNorm, $colNorm) !== false) {
                        $colMap[$field] = $idx;
                        $detectedColumns[$field] = $originalHeader[$idx];
                        break 2;
                    }
                }
            }
        }
    }

    // Check if user has overridden mappings via POST
    if (isset($_POST['col_mapping']) && is_array($_POST['col_mapping'])) {
        foreach ($_POST['col_mapping'] as $field => $idx) {
            if ($idx !== '' && $idx !== '-1') {
                $colMap[$field] = (int)$idx;
            } elseif ($idx === '-1') {
                unset($colMap[$field]);
            }
        }
    }

    // Store column info for template
    $columnInfo = [
        'original_headers' => $originalHeader,
        'detected' => $detectedColumns,
        'mapping' => $colMap,
        'patterns' => $columnPatterns
    ];

    // Cache for lookups
    $clubCache = [];
    $riderCache = [];

    $lineNumber = 1;
    while (($row = fgetcsv($handle, 0, $separator)) !== false) {
        $lineNumber++;
        $matchingStats['total_rows']++;

        if (empty(array_filter($row, function($v) { return trim($v) !== ''; }))) {
            continue;
        }

        $firstname = trim($row[$colMap['firstname']] ?? '');
        $lastname = trim($row[$colMap['lastname']] ?? '');

        if (empty($firstname) || empty($lastname)) {
            continue;
        }

        // Gender
        $gender = 'M';
        if (isset($colMap['gender'])) {
            $genderRaw = strtoupper(trim($row[$colMap['gender']] ?? ''));
            if (in_array($genderRaw, ['F', 'K', 'W'])) {
                $gender = 'F';
            }
        }

        // Birth year
        $birthYear = null;
        if (isset($colMap['birth_year']) && !empty($row[$colMap['birth_year']])) {
            $birthYear = (int)$row[$colMap['birth_year']];
        } elseif (isset($colMap['birthday']) && !empty($row[$colMap['birthday']])) {
            $bday = trim($row[$colMap['birthday']]);
            if (preg_match('/(\d{4})/', $bday, $m)) {
                $birthYear = (int)$m[1];
            }
        }

        // Club
        $clubName = isset($colMap['club']) ? trim($row[$colMap['club']] ?? '') : '';
        $clubStatus = 'none';

        if (!empty($clubName)) {
            if (!isset($clubCache[$clubName])) {
                $club = $db->getRow("SELECT id, name FROM clubs WHERE name = ? OR name LIKE ?", [$clubName, '%' . $clubName . '%']);
                $clubCache[$clubName] = $club ? $club : null;
            }

            if ($clubCache[$clubName]) {
                $clubStatus = 'existing';
                if (!in_array($clubName, array_column($matchingStats['clubs_list'], 'name'))) {
                    $matchingStats['clubs_list'][] = ['name' => $clubName, 'status' => 'existing', 'matched' => $clubCache[$clubName]['name']];
                }
                $matchingStats['clubs_existing']++;
            } else {
                $clubStatus = 'new';
                if (!in_array($clubName, array_column($matchingStats['clubs_list'], 'name'))) {
                    $matchingStats['clubs_list'][] = ['name' => $clubName, 'status' => 'new', 'matched' => null];
                }
                $matchingStats['clubs_new']++;
            }
        }

        // UCI ID - check in CSV first, then search if missing
        $uciId = isset($colMap['uci_id']) ? trim($row[$colMap['uci_id']] ?? '') : '';
        $uciIdSource = 'csv'; // 'csv', 'found', or 'not_found'
        $uciIdMatch = null;

        if (!empty($uciId)) {
            // Normalize existing UCI ID
            $uciId = normalizeUciId($uciId);
            $uciIdSource = 'csv';
            $matchingStats['uci_existing']++;
        } else {
            // Search for UCI ID in database
            $uciIdMatch = findRiderForUciId($db, $firstname, $lastname, $clubName, $birthYear);
            if ($uciIdMatch && !empty($uciIdMatch['license_number'])) {
                $uciId = normalizeUciId($uciIdMatch['license_number']);
                $uciIdSource = 'found';
                $matchingStats['uci_found']++;
            } else {
                $uciIdSource = 'not_found';
                $matchingStats['uci_not_found']++;
            }
        }

        // Check if rider exists
        $riderKey = strtolower($firstname . '_' . $lastname . '_' . $birthYear);
        $riderStatus = 'new';
        $existingRider = null;

        // Check by name + birth year
        if ($birthYear) {
            $existingRider = $db->getRow(
                "SELECT id, firstname, lastname, license_number, club_id FROM riders
                 WHERE LOWER(firstname) = LOWER(?) AND LOWER(lastname) = LOWER(?) AND birth_year = ?",
                [$firstname, $lastname, $birthYear]
            );
        }

        // Check by name only
        if (!$existingRider) {
            $existingRider = $db->getRow(
                "SELECT id, firstname, lastname, license_number, club_id FROM riders
                 WHERE LOWER(firstname) = LOWER(?) AND LOWER(lastname) = LOWER(?)",
                [$firstname, $lastname]
            );
        }

        // Check by UCI ID
        if (!$existingRider && !empty($uciId)) {
            $uciIdClean = preg_replace('/[^0-9]/', '', $uciId);
            if (strlen($uciIdClean) >= 8) {
                $existingRider = $db->getRow(
                    "SELECT id, firstname, lastname, license_number, club_id FROM riders
                     WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?",
                    [$uciIdClean]
                );
            }
        }

        if ($existingRider) {
            $riderStatus = 'existing';
            $matchingStats['riders_existing']++;
        } else {
            $matchingStats['riders_new']++;
        }

        $previewData[] = [
            'line' => $lineNumber,
            'firstname' => $firstname,
            'lastname' => $lastname,
            'gender' => $gender,
            'birth_year' => $birthYear,
            'club' => $clubName,
            'club_status' => $clubStatus,
            'uci_id' => $uciId,
            'uci_id_source' => $uciIdSource,
            'uci_id_match' => $uciIdMatch,
            'rider_status' => $riderStatus,
            'existing_rider' => $existingRider
        ];
    }

    fclose($handle);

} catch (Exception $e) {
    $message = 'Parsning misslyckades: ' . $e->getMessage();
    $messageType = 'error';
}

// Handle confirm import
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['confirm_import'])) {
    checkCsrf();

    // Redirect to actual import with confirmed flag
    $_SESSION['import_riders_confirmed'] = true;
    header('Location: /admin/import/riders?do_import=1');
    exit;
}

// Handle cancel
if (isset($_GET['cancel'])) {
    if (isset($_SESSION['import_riders_file']) && file_exists($_SESSION['import_riders_file'])) {
        @unlink($_SESSION['import_riders_file']);
    }
    unset($_SESSION['import_riders_file']);
    unset($_SESSION['import_riders_season']);
    unset($_SESSION['import_riders_create_missing']);
    header('Location: /admin/import/riders');
    exit;
}

// Page config
$page_title = 'Förhandsgranska Import';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Deltagare', 'url' => '/admin/import/riders'],
    ['label' => 'Förhandsgranska']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'error' ? 'error' : 'info' ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Summary Stats -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="bar-chart-2"></i>
            Sammanfattning
        </h2>
    </div>
    <div class="admin-card-body">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: var(--space-md);">
            <div class="admin-stat-card">
                <div class="admin-stat-value"><?= number_format($matchingStats['total_rows']) ?></div>
                <div class="admin-stat-label">Totalt rader</div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-value text-success"><?= number_format($matchingStats['riders_existing']) ?></div>
                <div class="admin-stat-label">Befintliga deltagare</div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-value" style="color: var(--color-gs-blue);"><?= number_format($matchingStats['riders_new']) ?></div>
                <div class="admin-stat-label">Nya deltagare</div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-value"><?= number_format($matchingStats['clubs_existing']) ?></div>
                <div class="admin-stat-label">Befintliga klubbar</div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-value" style="color: var(--color-warning);"><?= number_format($matchingStats['clubs_new']) ?></div>
                <div class="admin-stat-label">Nya klubbar</div>
            </div>
        </div>

        <!-- UCI ID Stats -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: var(--space-md); margin-top: var(--space-md); padding-top: var(--space-md); border-top: 1px solid var(--color-border);">
            <div class="admin-stat-card">
                <div class="admin-stat-value"><?= number_format($matchingStats['uci_existing']) ?></div>
                <div class="admin-stat-label">UCI-ID i fil</div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-value text-success"><?= number_format($matchingStats['uci_found']) ?></div>
                <div class="admin-stat-label">UCI-ID hittade</div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-value text-secondary"><?= number_format($matchingStats['uci_not_found']) ?></div>
                <div class="admin-stat-label">UCI-ID saknas</div>
            </div>
        </div>

        <div class="mt-lg" style="background: var(--color-bg-muted); padding: var(--space-md); border-radius: var(--radius-md);">
            <p class="text-sm">
                <strong>Säsong:</strong> <?= $seasonYear ?><br>
                <strong>Skapa nya deltagare:</strong> <?= $createMissing ? 'Ja' : 'Nej' ?>
            </p>
        </div>
    </div>
</div>

<!-- Column Mapping -->
<?php if (isset($columnInfo)): ?>
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="columns"></i>
            Kolumnmappning
            <?php
            $requiredFields = ['firstname', 'lastname'];
            $missingRequired = array_diff($requiredFields, array_keys($columnInfo['mapping']));
            if (!empty($missingRequired)): ?>
            <span class="badge badge-danger ml-sm">Saknas: <?= implode(', ', $missingRequired) ?></span>
            <?php endif; ?>
        </h2>
    </div>
    <div class="admin-card-body">
        <p class="text-sm text-secondary mb-md">
            Systemet detekterade följande kolumner automatiskt. Om det ser fel ut kan du ändra mappningen nedan.
        </p>

        <form method="POST" id="columnMappingForm">
            <?= csrf_field() ?>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--space-md);">
                <?php
                $fieldLabels = [
                    'firstname' => ['label' => 'Förnamn', 'required' => true],
                    'lastname' => ['label' => 'Efternamn', 'required' => true],
                    'fullname' => ['label' => 'Fullständigt namn', 'required' => false],
                    'gender' => ['label' => 'Kön', 'required' => false],
                    'club' => ['label' => 'Klubb', 'required' => false],
                    'birth_year' => ['label' => 'Födelseår', 'required' => false],
                    'birthday' => ['label' => 'Födelsedatum', 'required' => false],
                    'email' => ['label' => 'E-post', 'required' => false],
                    'uci_id' => ['label' => 'Licensnummer/UCI-ID', 'required' => false],
                    'nationality' => ['label' => 'Nationalitet', 'required' => false]
                ];
                ?>
                <?php foreach ($fieldLabels as $field => $info): ?>
                <div class="form-group">
                    <label class="label" style="font-size: 0.85rem;">
                        <?= $info['label'] ?>
                        <?php if ($info['required']): ?>
                        <span class="text-danger">*</span>
                        <?php endif; ?>
                    </label>
                    <select name="col_mapping[<?= $field ?>]" class="input" style="font-size: 0.9rem;" onchange="document.getElementById('columnMappingForm').submit()">
                        <option value="-1">-- Inte mappad --</option>
                        <?php foreach ($columnInfo['original_headers'] as $idx => $colName): ?>
                        <option value="<?= $idx ?>"
                            <?= (isset($columnInfo['mapping'][$field]) && $columnInfo['mapping'][$field] === $idx) ? 'selected' : '' ?>>
                            <?= h($colName) ?> (kolumn <?= $idx + 1 ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                    <?php if (isset($columnInfo['detected'][$field])): ?>
                    <small class="text-success" style="display: block; margin-top: 2px;">
                        <i data-lucide="check" style="width: 12px; height: 12px;"></i>
                        Auto-detekterad
                    </small>
                    <?php endif; ?>
                </div>
                <?php endforeach; ?>
            </div>
        </form>

        <!-- Show original headers for reference -->
        <details class="mt-lg">
            <summary class="text-sm" style="cursor: pointer; color: var(--color-text-secondary);">
                <i data-lucide="eye"></i> Visa alla kolumner i filen (<?= count($columnInfo['original_headers']) ?> st)
            </summary>
            <div class="mt-sm" style="background: var(--color-bg-sunken); padding: var(--space-sm); border-radius: var(--radius-sm);">
                <?php foreach ($columnInfo['original_headers'] as $idx => $colName): ?>
                <span class="badge badge-secondary mr-xs mb-xs"><?= $idx + 1 ?>: <?= h($colName) ?></span>
                <?php endforeach; ?>
            </div>
        </details>
    </div>
</div>
<?php endif; ?>

<!-- Clubs Analysis -->
<?php if (!empty($matchingStats['clubs_list'])): ?>
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="building"></i>
            Klubbar (<?= count($matchingStats['clubs_list']) ?>)
        </h2>
    </div>
    <div class="admin-card-body">
        <div class="table-responsive">
            <table class="table text-sm">
                <thead>
                    <tr>
                        <th>Klubb i fil</th>
                        <th>Status</th>
                        <th>Matchad till</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($matchingStats['clubs_list'] as $club): ?>
                    <tr>
                        <td><?= h($club['name']) ?></td>
                        <td>
                            <?php if ($club['status'] === 'existing'): ?>
                            <span class="badge badge-success">Finns</span>
                            <?php else: ?>
                            <span class="badge badge-warning">Ny</span>
                            <?php endif; ?>
                        </td>
                        <td><?= $club['matched'] ? h($club['matched']) : '<em class="text-secondary">Skapas</em>' ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Preview Data -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="users"></i>
            Deltagare (första 100)
        </h2>
    </div>
    <div class="admin-card-body">
        <div class="table-responsive">
            <table class="table text-sm">
                <thead>
                    <tr>
                        <th>Rad</th>
                        <th>Namn</th>
                        <th>Födelseår</th>
                        <th>Kön</th>
                        <th>Klubb</th>
                        <th>UCI-ID</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($previewData, 0, 100) as $row): ?>
                    <tr>
                        <td><?= $row['line'] ?></td>
                        <td>
                            <strong><?= h($row['firstname']) ?> <?= h($row['lastname']) ?></strong>
                            <?php if ($row['existing_rider']): ?>
                            <br><small class="text-secondary">ID: <?= $row['existing_rider']['id'] ?></small>
                            <?php endif; ?>
                        </td>
                        <td><?= $row['birth_year'] ?: '-' ?></td>
                        <td><?= $row['gender'] ?></td>
                        <td>
                            <?= h($row['club']) ?: '-' ?>
                            <?php if ($row['club_status'] === 'new'): ?>
                            <span class="badge badge-warning" style="font-size: 0.65rem;">NY</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?php if (!empty($row['uci_id'])): ?>
                                <?php if ($row['uci_id_source'] === 'found'): ?>
                                    <code class="text-xs text-success" style="font-weight: 600;"><?= h($row['uci_id']) ?></code>
                                    <span class="badge badge-success" style="font-size: 0.6rem; margin-left: 4px;">
                                        <i data-lucide="search" style="width: 10px; height: 10px;"></i>
                                        Hittad
                                    </span>
                                    <?php if ($row['uci_id_match']): ?>
                                    <br><small class="text-secondary" style="font-size: 0.7rem;">
                                        via <?= h($row['uci_id_match']['firstname'] . ' ' . $row['uci_id_match']['lastname']) ?>
                                        <?php if ($row['uci_id_match']['confidence'] < 100): ?>
                                        (<?= $row['uci_id_match']['confidence'] ?>%)
                                        <?php endif; ?>
                                    </small>
                                    <?php endif; ?>
                                <?php else: ?>
                                    <code class="text-xs"><?= h($row['uci_id']) ?></code>
                                <?php endif; ?>
                            <?php else: ?>
                                <span class="text-secondary">-</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?php if ($row['rider_status'] === 'existing'): ?>
                            <span class="badge badge-success">Uppdateras</span>
                            <?php else: ?>
                            <span class="badge" style="background: var(--color-gs-blue); color: white;">Ny</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if (count($previewData) > 100): ?>
        <p class="text-sm text-secondary mt-md">
            Visar 100 av <?= count($previewData) ?> rader
        </p>
        <?php endif; ?>
    </div>
</div>

<!-- Actions -->
<div class="admin-card">
    <div class="admin-card-body">
        <form method="POST" style="display: flex; gap: var(--space-md); align-items: center;">
            <?= csrf_field() ?>

            <button type="submit" name="confirm_import" class="btn-admin btn-admin-primary">
                <i data-lucide="check"></i>
                Bekräfta och importera
            </button>

            <a href="?cancel=1" class="btn-admin btn-admin-secondary">
                <i data-lucide="x"></i>
                Avbryt
            </a>

            <span class="text-secondary text-sm" style="margin-left: auto;">
                <?= $matchingStats['riders_existing'] ?> uppdateras, <?= $matchingStats['riders_new'] ?> nya skapas
            </span>
        </form>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
