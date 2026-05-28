<?php
/**
 * Rider Update Import - Updates existing riders with UCI ID, email, birth year
 * and sets club membership for a specific season year
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/helpers.php';
require_once __DIR__ . '/../includes/club-membership.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

// Load import history helper functions
require_once __DIR__ . '/../includes/import-history.php';

$message = '';
$messageType = 'info';
$stats = null;
$errors = [];
$updated_riders = [];
$created_riders = [];
$skipped_riders = [];
$uci_conflicts = [];
$mapped_columns = [];

// Current year for default selection
$currentYear = (int)date('Y');
$availableYears = range($currentYear + 1, $currentYear - 5);

// Handle CSV upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['rider_file'])) {
    checkCsrf();

    $file = $_FILES['rider_file'];
    $seasonYear = (int)($_POST['season_year'] ?? $currentYear);
    $createMissing = isset($_POST['create_missing']);

    // Validate file
    if ($file['error'] !== UPLOAD_ERR_OK) {
        $message = 'Filuppladdning misslyckades';
        $messageType = 'error';
    } elseif ($file['size'] > MAX_UPLOAD_SIZE) {
        $message = 'Filen är för stor (max ' . (MAX_UPLOAD_SIZE / 1024 / 1024) . 'MB)';
        $messageType = 'error';
    } else {
        $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

        if ($extension !== 'csv') {
            $message = 'Ogiltigt filformat. Endast CSV tillåten.';
            $messageType = 'error';
        } else {
            $uploaded = UPLOADS_PATH . '/' . time() . '_rider_update_' . basename($file['name']);

            if (move_uploaded_file($file['tmp_name'], $uploaded)) {
                try {
                    // Start import history tracking
                    $importId = startImportHistory(
                        $db,
                        'rider_update',
                        $file['name'],
                        $file['size'],
                        $current_admin['username'] ?? 'admin'
                    );

                    // Perform import
                    $result = importRiderUpdates($uploaded, $db, $importId, $seasonYear, $createMissing);

                    $stats = $result['stats'];
                    $errors = $result['errors'];
                    $updated_riders = $result['updated'];
                    $created_riders = $result['created'];
                    $skipped_riders = $result['skipped'];
                    $uci_conflicts = $result['conflicts'] ?? [];
                    $mapped_columns = $result['mapped_columns'] ?? [];

                    // Update import history
                    $importStatus = ($stats['updated'] > 0 || $stats['created'] > 0) ? 'completed' : 'failed';
                    updateImportHistory($db, $importId, $stats, $errors, $importStatus);

                    if ($stats['updated'] > 0 || $stats['created'] > 0) {
                        $message = "Import klar! {$stats['updated']} uppdaterade, {$stats['created']} nya riders. Klubbtillhörighet satt för {$seasonYear}.";
                        if ($stats['conflicts'] > 0) {
                            $message .= " OBS: {$stats['conflicts']} UCI-ID konflikter kräver manuell hantering.";
                            $messageType = 'warning';
                        } else {
                            $messageType = 'success';
                        }
                    } else {
                        $message = "Ingen data importerades. Kontrollera filformatet.";
                        $messageType = 'error';
                    }

                } catch (Exception $e) {
                    $message = 'Import misslyckades: ' . $e->getMessage();
                    $messageType = 'error';

                    if (isset($importId)) {
                        updateImportHistory($db, $importId, ['total' => 0], [$e->getMessage()], 'failed');
                    }
                }

                @unlink($uploaded);
            } else {
                $message = 'Kunde inte ladda upp filen';
                $messageType = 'error';
            }
        }
    }
}

/**
 * Auto-detect CSV separator
 */
function detectCsvSeparator($file_path) {
    $handle = fopen($file_path, 'r');
    $first_line = fgets($handle);
    fclose($handle);

    $separators = [
        ',' => substr_count($first_line, ','),
        ';' => substr_count($first_line, ';'),
        "\t" => substr_count($first_line, "\t"),
    ];

    arsort($separators);
    return array_key_first($separators);
}

/**
 * Ensure UTF-8 encoding
 */
function ensureUTF8($filepath) {
    $content = file_get_contents($filepath);

    // Remove BOM if present
    $content = preg_replace('/^\xEF\xBB\xBF/', '', $content);

    // Check if already valid UTF-8
    if (mb_check_encoding($content, 'UTF-8')) {
        // Check if it contains typical Windows-1252 sequences that look like corrupted Swedish chars
        // In Windows-1252: ö=0xF6, ä=0xE4, å=0xE5, Ö=0xD6, Ä=0xC4, Å=0xC5
        // These bytes are valid UTF-8 continuation bytes, so mb_check_encoding might pass
        // but the text looks corrupted (š instead of ö, etc.)

        // Look for Windows-1252 byte patterns for Swedish characters
        if (preg_match('/[\xC0-\xFF]/', $content) && !preg_match('/[\xC0-\xFF][\x80-\xBF]/', $content)) {
            // Contains high bytes but not proper UTF-8 multi-byte sequences
            // This is likely Windows-1252/ISO-8859-1
            $content = mb_convert_encoding($content, 'UTF-8', 'Windows-1252');
            file_put_contents($filepath, $content);
            return;
        }

        // Check for common Swedish words that appear corrupted
        // If we see "Fšrnamn" instead of "Förnamn", it's Windows-1252 misread as UTF-8
        if (preg_match('/F.rnamn|f.rnamn|.delseår|.delse.r/u', $content) &&
            !preg_match('/Förnamn|förnamn|Födelseår|födelseår/u', $content)) {
            // Looks like Windows-1252 content
            // Re-read as Windows-1252 and convert to UTF-8
            $content = file_get_contents($filepath);
            $content = mb_convert_encoding($content, 'UTF-8', 'Windows-1252');
            file_put_contents($filepath, $content);
            return;
        }

        // Already valid UTF-8
        file_put_contents($filepath, $content);
        return;
    }

    // Not valid UTF-8, try Windows-1252 (common for Swedish Excel exports)
    $content = mb_convert_encoding($content, 'UTF-8', 'Windows-1252');
    file_put_contents($filepath, $content);
}

/**
 * Import rider updates from CSV
 * Format: Startnr, Förnamn, Efternamn, Kön, Klubb/Företag, Klass, Födelsedag,
 *         Postnummer, Stad, Adress, Nationalitet (2), Nationalitet (3),
 *         Telefon, Email, Födelseår, ID Medlemsnummer (UCI)
 */
function importRiderUpdates($filepath, $db, $importId, $seasonYear, $createMissing = false) {
    $stats = [
        'total' => 0,
        'updated' => 0,
        'created' => 0,
        'skipped' => 0,
        'failed' => 0,
        'clubs_set' => 0,
        'conflicts' => 0
    ];
    $errors = [];
    $updated_riders = [];
    $created_riders = [];
    $skipped_riders = [];
    $conflicts = [];
    $clubCache = [];
    $mappedColumns = [];

    // Ensure UTF-8
    ensureUTF8($filepath);

    if (($handle = fopen($filepath, 'r')) === false) {
        throw new Exception('Kunde inte öppna filen');
    }

    // Detect separator
    $separator = detectCsvSeparator($filepath);

    // Read header row
    $header = fgetcsv($handle, 0, $separator);
    if (!$header) {
        fclose($handle);
        throw new Exception('Kunde inte läsa filens header');
    }

    // Normalize header names (use mb_strtolower for proper UTF-8 handling)
    $header = array_map(function($col) {
        $col = mb_strtolower(trim($col), 'UTF-8');
        $col = preg_replace('/^\xEF\xBB\xBF/', '', $col); // Remove BOM
        return $col;
    }, $header);

    // Map column indices
    $colMap = [];
    foreach ($header as $idx => $col) {
        // Map Swedish column names to our fields
        if (strpos($col, 'förnamn') !== false || strpos($col, 'fornamn') !== false) {
            $colMap['firstname'] = $idx;
        } elseif (strpos($col, 'efternamn') !== false) {
            $colMap['lastname'] = $idx;
        } elseif ($col === 'kön' || $col === 'kon') {
            $colMap['gender'] = $idx;
        } elseif (strpos($col, 'klubb') !== false || strpos($col, 'företag') !== false || strpos($col, 'foretag') !== false) {
            $colMap['club'] = $idx;
        } elseif (strpos($col, 'födelseår') !== false || strpos($col, 'fodelsear') !== false) {
            $colMap['birth_year'] = $idx;
        } elseif (strpos($col, 'födelsedag') !== false || strpos($col, 'fodelsedag') !== false) {
            $colMap['birthday'] = $idx;
        } elseif (strpos($col, 'email') !== false || strpos($col, 'e-post') !== false || strpos($col, 'epost') !== false) {
            $colMap['email'] = $idx;
        } elseif (strpos($col, 'medlemsnummer') !== false || strpos($col, 'id ') !== false || strpos($col, 'uci') !== false || strpos($col, 'licens') !== false) {
            $colMap['uci_id'] = $idx;
        } elseif (strpos($col, 'nationalitet') !== false && strpos($col, '3') !== false) {
            $colMap['nationality'] = $idx;
        } elseif (strpos($col, 'telefon') !== false || strpos($col, 'mobil') !== false || strpos($col, 'phone') !== false) {
            $colMap['phone'] = $idx;
        } elseif (strpos($col, 'postnummer') !== false || strpos($col, 'postnr') !== false) {
            $colMap['postal_code'] = $idx;
        } elseif (strpos($col, 'stad') !== false || strpos($col, 'ort') !== false || $col === 'city') {
            $colMap['city'] = $idx;
        } elseif (strpos($col, 'adress') !== false || $col === 'address') {
            $colMap['address'] = $idx;
        }
    }

    // Validate required columns
    if (!isset($colMap['firstname']) || !isset($colMap['lastname'])) {
        fclose($handle);
        throw new Exception('Saknar obligatoriska kolumner: Förnamn och Efternamn. Hittade kolumner: ' . implode(', ', $header));
    }

    // Store which columns were mapped for debugging/display
    foreach ($colMap as $field => $idx) {
        $mappedColumns[$field] = $header[$idx];
    }

    $lineNumber = 1;

    while (($row = fgetcsv($handle, 0, $separator)) !== false) {
        $lineNumber++;
        $stats['total']++;

        // Skip empty rows
        if (empty(array_filter($row, function($v) { return trim($v) !== ''; }))) {
            continue;
        }

        try {
            // Extract data
            $firstname = trim($row[$colMap['firstname']] ?? '');
            $lastname = trim($row[$colMap['lastname']] ?? '');

            if (empty($firstname) || empty($lastname)) {
                $stats['skipped']++;
                $skipped_riders[] = "Rad {$lineNumber}: Saknar namn";
                continue;
            }

            $gender = 'M';
            if (isset($colMap['gender'])) {
                $genderRaw = strtoupper(trim($row[$colMap['gender']] ?? ''));
                if (in_array($genderRaw, ['F', 'K', 'W'])) {
                    $gender = 'F';
                }
            }

            $clubName = isset($colMap['club']) ? trim($row[$colMap['club']] ?? '') : '';

            // Parse birth year - try direct column first, then birthday
            $birthYear = null;
            if (isset($colMap['birth_year']) && !empty($row[$colMap['birth_year']])) {
                $birthYear = (int)$row[$colMap['birth_year']];
            } elseif (isset($colMap['birthday']) && !empty($row[$colMap['birthday']])) {
                // Parse birthday (DD-MM-YYYY or YYYY-MM-DD)
                $bday = trim($row[$colMap['birthday']]);
                if (preg_match('/^(\d{2})-(\d{2})-(\d{4})$/', $bday, $m)) {
                    $birthYear = (int)$m[3];
                } elseif (preg_match('/^(\d{4})-(\d{2})-(\d{2})$/', $bday, $m)) {
                    $birthYear = (int)$m[1];
                }
            }

            $email = isset($colMap['email']) ? trim($row[$colMap['email']] ?? '') : '';
            $uciId = isset($colMap['uci_id']) ? trim($row[$colMap['uci_id']] ?? '') : '';
            $nationality = isset($colMap['nationality']) ? trim($row[$colMap['nationality']] ?? 'SWE') : 'SWE';
            $phone = isset($colMap['phone']) ? trim($row[$colMap['phone']] ?? '') : '';
            $postalCode = isset($colMap['postal_code']) ? trim($row[$colMap['postal_code']] ?? '') : '';
            $city = isset($colMap['city']) ? trim($row[$colMap['city']] ?? '') : '';
            $address = isset($colMap['address']) ? trim($row[$colMap['address']] ?? '') : '';

            // Find existing rider by name (and optionally birth year)
            $existing = null;

            // First try exact name + birth year match
            if ($birthYear) {
                $existing = $db->getRow(
                    "SELECT id, license_number, email, birth_year, club_id, nationality, phone, city FROM riders
                     WHERE LOWER(firstname) = LOWER(?) AND LOWER(lastname) = LOWER(?) AND birth_year = ?",
                    [$firstname, $lastname, $birthYear]
                );
            }

            // Try by UCI ID if provided
            if (!$existing && !empty($uciId)) {
                $uciIdClean = preg_replace('/[^0-9]/', '', $uciId);
                if (strlen($uciIdClean) >= 8) {
                    $existing = $db->getRow(
                        "SELECT id, license_number, email, birth_year, club_id, nationality, phone, city FROM riders
                         WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?",
                        [$uciIdClean]
                    );
                }
            }

            // Try by name only (less strict)
            if (!$existing) {
                $existing = $db->getRow(
                    "SELECT id, license_number, email, birth_year, club_id, nationality, phone, city FROM riders
                     WHERE LOWER(firstname) = LOWER(?) AND LOWER(lastname) = LOWER(?)",
                    [$firstname, $lastname]
                );
            }

            // Find or create club
            $clubId = null;
            if (!empty($clubName)) {
                if (isset($clubCache[$clubName])) {
                    $clubId = $clubCache[$clubName];
                } else {
                    $club = $db->getRow("SELECT id FROM clubs WHERE name = ?", [$clubName]);
                    if (!$club) {
                        $club = $db->getRow("SELECT id FROM clubs WHERE name LIKE ?", ['%' . $clubName . '%']);
                    }
                    if (!$club) {
                        // Create new club
                        $clubId = $db->insert('clubs', [
                            'name' => $clubName,
                            'country' => 'Sverige',
                            'active' => 1
                        ]);
                    } else {
                        $clubId = $club['id'];
                    }
                    $clubCache[$clubName] = $clubId;
                }
            }

            if ($existing) {
                // Update existing rider
                $updateData = [];
                $changes = [];

                // Update UCI ID if provided
                // Regler:
                // 1. Om nuvarande är tomt eller SWE-ID → uppdatera till UCI ID
                // 2. Om nuvarande redan är ett UCI ID → ALDRIG ändra
                // 3. Om konflikt (olika UCI ID) → logga som varning
                if (!empty($uciId)) {
                    $currentLicense = trim($existing['license_number'] ?? '');
                    $isSweId = empty($currentLicense) || strpos($currentLicense, 'SWE') === 0;

                    if ($isSweId) {
                        // SWE-ID ska alltid uppdateras till riktigt UCI ID
                        $updateData['license_number'] = $uciId;
                        $changes[] = "UCI-ID: {$currentLicense} → {$uciId}";
                    } elseif ($currentLicense !== $uciId) {
                        // Konflikt: Deltagaren har redan ett annat UCI ID
                        $conflicts[] = [
                            'rider_id' => $existing['id'],
                            'name' => "{$firstname} {$lastname}",
                            'current_uci' => $currentLicense,
                            'import_uci' => $uciId,
                            'line' => $lineNumber
                        ];
                    }
                    // Om currentLicense === uciId → inget att göra, redan korrekt
                }

                // Update email if provided and rider doesn't have one
                if (!empty($email) && empty($existing['email'])) {
                    $updateData['email'] = $email;
                    $changes[] = "Email: {$email}";
                }

                // Update birth year if provided and rider doesn't have one
                if ($birthYear && empty($existing['birth_year'])) {
                    $updateData['birth_year'] = $birthYear;
                    $changes[] = "Födelseår: {$birthYear}";
                }

                // Update gender
                $updateData['gender'] = $gender;

                // Update nationality if provided and different
                if (!empty($nationality) && $nationality !== ($existing['nationality'] ?? '')) {
                    $updateData['nationality'] = $nationality;
                    $changes[] = "Nationalitet: {$nationality}";
                }

                // Update phone if provided and rider doesn't have one
                if (!empty($phone) && empty($existing['phone'])) {
                    $updateData['phone'] = $phone;
                    $changes[] = "Telefon: {$phone}";
                }

                // Update city if provided and rider doesn't have one
                if (!empty($city) && empty($existing['city'])) {
                    $updateData['city'] = $city;
                    $changes[] = "Stad: {$city}";
                }

                // Save updates
                if (!empty($updateData)) {
                    $oldData = $db->getRow("SELECT * FROM riders WHERE id = ?", [$existing['id']]);
                    $db->update('riders', $updateData, 'id = ?', [$existing['id']]);

                    if ($importId) {
                        trackImportRecord($db, $importId, 'rider', $existing['id'], 'updated', $oldData);
                    }
                }

                // Set club membership for the season year
                if ($clubId) {
                    $result = setRiderClubForYear($db, $existing['id'], $clubId, $seasonYear);
                    if ($result['success']) {
                        $stats['clubs_set']++;
                        $changes[] = "Klubb {$seasonYear}: {$clubName}";
                    }
                }

                $stats['updated']++;
                $updated_riders[] = "{$firstname} {$lastname}" . (!empty($changes) ? " (" . implode(", ", $changes) . ")" : "");

            } elseif ($createMissing) {
                // Create new rider
                $newRiderData = [
                    'firstname' => $firstname,
                    'lastname' => $lastname,
                    'gender' => $gender,
                    'birth_year' => $birthYear,
                    'email' => !empty($email) ? $email : null,
                    'license_number' => !empty($uciId) ? $uciId : generateSweId($db),
                    'nationality' => $nationality ?: 'SWE',
                    'club_id' => $clubId,
                    'phone' => !empty($phone) ? $phone : null,
                    'city' => !empty($city) ? $city : null,
                    'active' => 1
                ];

                $riderId = $db->insert('riders', $newRiderData);

                if ($importId) {
                    trackImportRecord($db, $importId, 'rider', $riderId, 'created');
                }

                // Set club membership for the season year
                if ($clubId) {
                    setRiderClubForYear($db, $riderId, $clubId, $seasonYear);
                    $stats['clubs_set']++;
                }

                $stats['created']++;
                $created_riders[] = "{$firstname} {$lastname}";

            } else {
                // Rider not found and create_missing is false
                $stats['skipped']++;
                $skipped_riders[] = "{$firstname} {$lastname} (ej hittad)";
            }

        } catch (Exception $e) {
            $stats['failed']++;
            $errors[] = "Rad {$lineNumber}: " . $e->getMessage();
        }
    }

    fclose($handle);

    // Count conflicts
    $stats['conflicts'] = count($conflicts);

    return [
        'stats' => $stats,
        'errors' => $errors,
        'updated' => $updated_riders,
        'created' => $created_riders,
        'skipped' => $skipped_riders,
        'conflicts' => $conflicts,
        'mapped_columns' => $mappedColumns
    ];
}

// Page config
$page_title = 'Uppdatera Riders';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Uppdatera Riders']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?> mb-lg">
    <p><strong><?= $message ?></strong></p>

    <?php if ($stats): ?>
    <div class="mt-md">
        <p><i data-lucide="bar-chart" class="icon-xs"></i> <strong>Statistik:</strong></p>
        <ul class="ml-lg mt-sm">
            <li>Totalt rader: <?= $stats['total'] ?></li>
            <li class="text-accent">Uppdaterade: <?= $stats['updated'] ?></li>
            <li class="text-success">Nya riders: <?= $stats['created'] ?></li>
            <li class="text-secondary">Överhoppade: <?= $stats['skipped'] ?></li>
            <li class="text-error">Misslyckade: <?= $stats['failed'] ?></li>
            <li style="color: var(--color-gs-blue);">Klubbtillhörigheter satta: <?= $stats['clubs_set'] ?></li>
        </ul>
    </div>
    <?php endif; ?>

    <?php if (!empty($mapped_columns)): ?>
    <details class="mt-md">
        <summary class="cursor-pointer"><i data-lucide="table" class="icon-xs"></i> Matchade kolumner (<?= count($mapped_columns) ?>)</summary>
        <div class="ml-lg mt-sm text-sm grid-2-col" style="gap: var(--space-xs);">
            <?php foreach ($mapped_columns as $field => $colName): ?>
            <div><strong><?= h($field) ?></strong>: <?= h($colName) ?></div>
            <?php endforeach; ?>
        </div>
    </details>
    <?php endif; ?>

    <?php if (!empty($updated_riders)): ?>
    <details class="mt-md">
        <summary class="cursor-pointer"><?= count($updated_riders) ?> uppdaterade riders</summary>
        <ul class="ml-lg mt-sm text-sm">
            <?php foreach (array_slice($updated_riders, 0, 30) as $rider): ?>
            <li><?= h($rider) ?></li>
            <?php endforeach; ?>
            <?php if (count($updated_riders) > 30): ?>
            <li><em>... och <?= count($updated_riders) - 30 ?> till</em></li>
            <?php endif; ?>
        </ul>
    </details>
    <?php endif; ?>

    <?php if (!empty($created_riders)): ?>
    <details class="mt-md">
        <summary class="cursor-pointer text-success"><?= count($created_riders) ?> nya riders</summary>
        <ul class="ml-lg mt-sm text-sm">
            <?php foreach (array_slice($created_riders, 0, 30) as $rider): ?>
            <li><?= h($rider) ?></li>
            <?php endforeach; ?>
            <?php if (count($created_riders) > 30): ?>
            <li><em>... och <?= count($created_riders) - 30 ?> till</em></li>
            <?php endif; ?>
        </ul>
    </details>
    <?php endif; ?>

    <?php if (!empty($skipped_riders)): ?>
    <details class="mt-md">
        <summary class="cursor-pointer text-secondary"><?= count($skipped_riders) ?> överhoppade</summary>
        <ul class="ml-lg mt-sm text-sm">
            <?php foreach (array_slice($skipped_riders, 0, 30) as $rider): ?>
            <li><?= h($rider) ?></li>
            <?php endforeach; ?>
            <?php if (count($skipped_riders) > 30): ?>
            <li><em>... och <?= count($skipped_riders) - 30 ?> till</em></li>
            <?php endif; ?>
        </ul>
    </details>
    <?php endif; ?>

    <?php if (!empty($uci_conflicts)): ?>
    <div class="mt-lg" style="background: rgba(245, 158, 11, 0.1); border: 1px solid var(--color-warning); border-radius: var(--radius-md); padding: var(--space-md);">
        <h4 class="flex items-center gap-sm mb-md" style="color: var(--color-warning);">
            <i data-lucide="alert-triangle"></i>
            UCI-ID Konflikter (<?= count($uci_conflicts) ?>)
        </h4>
        <p class="text-sm text-secondary mb-md">
            Dessa deltagare har redan ett UCI-ID som skiljer sig från filen. Klicka på "Redigera" för att granska manuellt.
        </p>
        <div class="table-responsive">
            <table class="table text-sm">
                <thead>
                    <tr>
                        <th>Rad</th>
                        <th>Namn</th>
                        <th>Nuvarande UCI-ID</th>
                        <th>UCI-ID i fil</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($uci_conflicts as $conflict): ?>
                    <tr>
                        <td><?= $conflict['line'] ?></td>
                        <td><strong><?= h($conflict['name']) ?></strong></td>
                        <td><code><?= h($conflict['current_uci']) ?></code></td>
                        <td><code style="color: var(--color-warning);"><?= h($conflict['import_uci']) ?></code></td>
                        <td>
                            <a href="/admin/rider-edit.php?id=<?= $conflict['rider_id'] ?>" class="btn btn--sm btn--secondary" target="_blank">
                                <i data-lucide="external-link"></i>
                                Redigera
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
    <?php endif; ?>

    <?php if (!empty($errors)): ?>
    <details class="mt-md">
        <summary class="cursor-pointer text-error"><?= count($errors) ?> fel</summary>
        <ul class="ml-lg mt-sm text-sm">
            <?php foreach (array_slice($errors, 0, 20) as $error): ?>
            <li><?= h($error) ?></li>
            <?php endforeach; ?>
            <?php if (count($errors) > 20): ?>
            <li><em>... och <?= count($errors) - 20 ?> fler fel</em></li>
            <?php endif; ?>
        </ul>
    </details>
    <?php endif; ?>
</div>
<?php endif; ?>

<!-- Format Information -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="info"></i>
            Anmälningsexport-format
        </h2>
    </div>
    <div class="admin-card-body">
        <p class="mb-md">
            Denna import uppdaterar befintliga riders med UCI-ID, e-post och födelseår.
            Klubbtillhörighet sätts för valt säsongsår.
        </p>

        <h4 style="margin-bottom: var(--space-sm); color: var(--color-text);">Förväntade kolumner (med header):</h4>
        <div style="overflow-x: auto; margin-bottom: var(--space-md);">
            <table class="table text-sm">
                <thead>
                    <tr>
                        <th>Kolumnnamn</th>
                        <th>Beskrivning</th>
                        <th>Obligatorisk</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><code>Förnamn</code></td><td>Riderens förnamn</td><td><strong>Ja</strong></td></tr>
                    <tr><td><code>Efternamn</code></td><td>Riderens efternamn</td><td><strong>Ja</strong></td></tr>
                    <tr><td><code>Kön</code></td><td>M eller F/K</td><td>Nej</td></tr>
                    <tr><td><code>Klubb/Företag</code></td><td>Klubbnamn (skapas om den inte finns)</td><td>Nej</td></tr>
                    <tr><td><code>Födelseår</code></td><td>År (t.ex. 1992)</td><td>Nej</td></tr>
                    <tr><td><code>Födelsedag</code></td><td>Datum (DD-MM-YYYY)</td><td>Nej</td></tr>
                    <tr><td><code>Nationalitet (3-letter)</code></td><td>Landskod (SWE, NOR, etc.)</td><td>Nej</td></tr>
                    <tr><td><code>Deltagarens email</code></td><td>E-postadress</td><td>Nej</td></tr>
                    <tr><td><code>Telefon</code></td><td>Telefonnummer</td><td>Nej</td></tr>
                    <tr><td><code>Stad</code></td><td>Stad/Ort</td><td>Nej</td></tr>
                    <tr><td><code>Postnummer</code></td><td>Postnummer</td><td>Nej</td></tr>
                    <tr><td><code>ID Medlemsnummer</code></td><td>UCI-ID (11 siffror)</td><td>Nej</td></tr>
                </tbody>
            </table>
        </div>

        <div class="info-box">
            <p class="text-secondary text-sm" class="mb-sm"><strong>Exempel på CSV (tab-separerad):</strong></p>
            <pre class="text-xs" style="overflow-x: auto; white-space: pre-wrap;">Startnr.	Förnamn	Efternamn	Kön	Klubb/Företag	Klass	Födelsedag	...	Deltagarens email	Födelseår	ID Medlemsnummer
	Zakarias Blom	JOHANSEN	M	Ibis enduro racing team	Tävling Herrar	25-11-1992	...	zakarias@email.com	1992	10006911232
1	Thorwout	WARNTJES	M	Mera lera MTB	Tävling Herrar	21-06-2001	...	thorwout@email.com	2001	10022409711</pre>
        </div>

        <div class="alert alert-success mt-md">
            <p class="text-sm">
                <strong>Vad som uppdateras:</strong><br>
                - <strong>UCI-ID</strong> → uppdateras om rider har SWE-ID eller saknar licensnummer<br>
                - <strong>E-post</strong> → uppdateras om rider saknar e-post<br>
                - <strong>Födelseår</strong> → uppdateras om rider saknar födelseår<br>
                - <strong>Nationalitet</strong> → uppdateras om den skiljer sig från befintlig<br>
                - <strong>Telefon</strong> → uppdateras om rider saknar telefon<br>
                - <strong>Stad</strong> → uppdateras om rider saknar stad<br>
                - <strong>Klubbtillhörighet</strong> → sätts för valt säsongsår (kan inte ändras om rider har resultat det året)
            </p>
        </div>
    </div>
</div>

<!-- Upload Form -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="upload"></i>
            Ladda upp fil
        </h2>
    </div>
    <div class="admin-card-body">
        <form method="POST" enctype="multipart/form-data">
            <?= csrf_field() ?>

            <div class="grid-2-col">
                <div class="admin-form-group">
                    <label class="admin-form-label">
                        <i data-lucide="file-text"></i>
                        CSV-fil med anmälningar
                    </label>
                    <input type="file" name="rider_file" accept=".csv" class="admin-form-input" required>
                    <small class="text-secondary">
                        Endast CSV-filer. Max <?= MAX_UPLOAD_SIZE / 1024 / 1024 ?>MB.
                    </small>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">
                        <i data-lucide="calendar"></i>
                        Säsongsår för klubbtillhörighet
                    </label>
                    <select name="season_year" class="admin-form-select">
                        <?php foreach ($availableYears as $year): ?>
                        <option value="<?= $year ?>" <?= $year === $currentYear ? 'selected' : '' ?>>
                            <?= $year ?>
                        </option>
                        <?php endforeach; ?>
                    </select>
                    <small class="text-secondary">
                        Klubbtillhörighet sätts för detta år. Kan inte ändras om rider har resultat.
                    </small>
                </div>
            </div>

            <div class="admin-form-group mt-md">
                <label class="flex items-center gap-sm cursor-pointer">
                    <input type="checkbox" name="create_missing" checked>
                    <span>Skapa nya riders om de inte hittas</span>
                </label>
                <small class="text-secondary" style="margin-left: 24px;">
                    Riders med UCI-ID och fullständig data skapas automatiskt. Avmarkera för att bara uppdatera befintliga.
                </small>
            </div>

            <div class="flex gap-md mt-lg">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="upload"></i>
                    Importera och uppdatera
                </button>
                <a href="/admin/riders.php" class="btn-admin btn-admin-secondary">
                    <i data-lucide="arrow-left"></i>
                    Tillbaka till riders
                </a>
            </div>
        </form>
    </div>
</div>

<!-- Quick Links -->
<div class="grid" style="grid-template-columns: repeat(2, 1fr); gap: var(--space-lg);">
    <div class="admin-card">
        <div class="admin-card-body">
            <h4 class="mb-sm">
                <i data-lucide="history"></i>
                Importhistorik
            </h4>
            <p class="text-secondary text-sm" class="mb-md">
                Se tidigare importer och ångra vid behov.
            </p>
            <a href="/admin/import-history.php" class="btn-admin btn-admin-secondary btn-admin-sm">
                <i data-lucide="history"></i>
                Visa historik
            </a>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-body">
            <h4 class="mb-sm">
                <i data-lucide="users"></i>
                Alla riders
            </h4>
            <p class="text-secondary text-sm" class="mb-md">
                Granska och redigera riders manuellt.
            </p>
            <a href="/admin/riders.php" class="btn-admin btn-admin-secondary btn-admin-sm">
                <i data-lucide="users"></i>
                Visa riders
            </a>
        </div>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
