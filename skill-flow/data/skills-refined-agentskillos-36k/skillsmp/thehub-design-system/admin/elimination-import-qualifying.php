<?php
/**
 * Import Qualifying Results for Elimination Events
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;
$db = getDB();

$eventId = isset($_GET['event_id']) ? intval($_GET['event_id']) : 0;
$classId = isset($_GET['class_id']) ? intval($_GET['class_id']) : 0;

if (!$eventId) {
    header('Location: /admin/elimination.php');
    exit;
}

// Get event info
$event = $db->getRow("SELECT * FROM events WHERE id = ?", [$eventId]);
if (!$event) {
    $_SESSION['error'] = 'Event hittades inte';
    header('Location: /admin/elimination.php');
    exit;
}

// Get all classes
$classes = $db->getAll("
    SELECT id, name, display_name FROM classes
    WHERE active = 1
    ORDER BY sort_order, name
");

// Handle CSV upload
$importResults = null;
$previewData = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['action']) && $_POST['action'] === 'preview' && isset($_FILES['csv_file'])) {
        $file = $_FILES['csv_file'];

        if ($file['error'] === UPLOAD_ERR_OK) {
            $content = file_get_contents($file['tmp_name']);
            // Detect encoding and convert to UTF-8
            $encoding = mb_detect_encoding($content, ['UTF-8', 'ISO-8859-1', 'Windows-1252'], true);
            if ($encoding && $encoding !== 'UTF-8') {
                $content = mb_convert_encoding($content, 'UTF-8', $encoding);
            }

            // Parse CSV
            $lines = array_filter(explode("\n", $content));
            $delimiter = strpos($lines[0], "\t") !== false ? "\t" : (strpos($lines[0], ';') !== false ? ';' : ',');

            $headers = str_getcsv(array_shift($lines), $delimiter);
            $headers = array_map('trim', $headers);
            $headers = array_map('strtolower', $headers);

            // Map common column names
            $columnMap = [
                'startnr' => 'bib',
                'startnummer' => 'bib',
                'bib' => 'bib',
                'nr' => 'bib',
                'namn' => 'name',
                'name' => 'name',
                'förnamn' => 'firstname',
                'firstname' => 'firstname',
                'efternamn' => 'lastname',
                'lastname' => 'lastname',
                'klubb' => 'club',
                'club' => 'club',
                'cykelklubb' => 'club',
                'klass' => 'class',
                'class' => 'class',
                'tävlingsklass' => 'class',
                'category' => 'class',
                // Series points class (for Dual Slalom youth classes)
                'serieklass' => 'series_class',
                'serie klass' => 'series_class',
                'series_class' => 'series_class',
                'seriepoängklass' => 'series_class',
                'poängklass' => 'series_class',
                'kval 1' => 'run1',
                'kval1' => 'run1',
                'run1' => 'run1',
                'run 1' => 'run1',
                'åk 1' => 'run1',
                'åk1' => 'run1',
                'kval 2' => 'run2',
                'kval2' => 'run2',
                'run2' => 'run2',
                'run 2' => 'run2',
                'åk 2' => 'run2',
                'åk2' => 'run2',
                'tid' => 'best',
                'tid:' => 'best',
                'best' => 'best',
                'bäst' => 'best',
                'totaltid' => 'best',
                // Final position for completed events
                'slutplacering' => 'final_position',
                'final_position' => 'final_position',
                'final' => 'final_position',
                'placering' => 'final_position',
                'plats' => 'final_position',
                'position' => 'final_position',
            ];

            $mappedHeaders = [];
            foreach ($headers as $idx => $h) {
                $normalized = strtolower(trim($h));
                $mappedHeaders[$idx] = $columnMap[$normalized] ?? $normalized;
            }

            // Parse rows
            foreach ($lines as $line) {
                $line = trim($line);
                if (empty($line)) continue;

                $cols = str_getcsv($line, $delimiter);
                $row = [];

                foreach ($cols as $idx => $val) {
                    $key = $mappedHeaders[$idx] ?? "col_$idx";
                    $row[$key] = trim($val);
                }

                // Parse times (handle comma decimals)
                if (isset($row['run1'])) {
                    $row['run1'] = floatval(str_replace(',', '.', $row['run1']));
                }
                if (isset($row['run2'])) {
                    $row['run2'] = floatval(str_replace(',', '.', $row['run2']));
                }
                if (isset($row['best'])) {
                    $row['best'] = floatval(str_replace(',', '.', $row['best']));
                }

                // Parse final position for completed events
                if (isset($row['final_position'])) {
                    $row['final_position'] = intval($row['final_position']);
                }

                // Calculate best time if not provided
                if (empty($row['best']) && !empty($row['run1'])) {
                    $row['best'] = $row['run1'];
                    if (!empty($row['run2']) && $row['run2'] < $row['best']) {
                        $row['best'] = $row['run2'];
                    }
                }

                // Handle combined name field
                if (!empty($row['name']) && empty($row['firstname'])) {
                    $parts = explode(' ', $row['name'], 2);
                    $row['firstname'] = $parts[0] ?? '';
                    $row['lastname'] = $parts[1] ?? '';
                }

                if (!empty($row['firstname']) || !empty($row['name'])) {
                    $previewData[] = $row;
                }
            }

            // Store in session for import
            $_SESSION['elimination_import_preview'] = $previewData;
            $_SESSION['elimination_import_event'] = $eventId;
        }
    }

    if (isset($_POST['action']) && $_POST['action'] === 'import') {
        $fallbackClassId = intval($_POST['class_id'] ?? 0);
        $previewData = $_SESSION['elimination_import_preview'] ?? [];
        $clearExisting = isset($_POST['clear_existing']) && $_POST['clear_existing'] === '1';

        if (!empty($previewData)) {
            $imported = 0;
            $errors = [];
            $classesImported = [];
            $classesWithFinalResults = [];
            $classCache = [];

            // Build class lookup cache with multiple variants
            foreach ($classes as $c) {
                $classCache[strtolower($c['name'])] = $c['id'];
                if (!empty($c['display_name'])) {
                    $classCache[strtolower($c['display_name'])] = $c['id'];
                }
            }

            // Get class mapping from form
            $classMap = $_POST['class_map'] ?? [];
            $createdClasses = [];

            // Pre-create any new classes
            foreach ($classMap as $csvClassName => $targetId) {
                if ($targetId === '__CREATE__') {
                    $stmt = $pdo->prepare("INSERT INTO classes (name, display_name, discipline, active) VALUES (?, ?, 'DUAL_SLALOM', 1)");
                    $stmt->execute([strtolower(str_replace(' ', '_', $csvClassName)), $csvClassName]);
                    $createdClasses[$csvClassName] = $pdo->lastInsertId();
                }
            }

            // Collect all class IDs that will be imported
            $classesToClear = [];
            if ($fallbackClassId) {
                $classesToClear[$fallbackClassId] = true;
            }
            foreach ($previewData as $row) {
                if (!empty($row['class'])) {
                    $csvClassName = $row['class'];
                    if (isset($createdClasses[$csvClassName])) {
                        $classesToClear[$createdClasses[$csvClassName]] = true;
                    } elseif (isset($classMap[$csvClassName]) && $classMap[$csvClassName] !== '__CREATE__') {
                        $classesToClear[(int)$classMap[$csvClassName]] = true;
                    }
                }
            }

            // Clear existing data if requested
            if ($clearExisting && !empty($classesToClear)) {
                foreach (array_keys($classesToClear) as $clsId) {
                    $pdo->prepare("DELETE FROM elimination_brackets WHERE event_id = ? AND class_id = ?")->execute([$eventId, $clsId]);
                    $pdo->prepare("DELETE FROM elimination_qualifying WHERE event_id = ? AND class_id = ?")->execute([$eventId, $clsId]);
                    $pdo->prepare("DELETE FROM elimination_results WHERE event_id = ? AND class_id = ?")->execute([$eventId, $clsId]);
                    $pdo->prepare("DELETE FROM results WHERE event_id = ? AND class_id = ?")->execute([$eventId, $clsId]);
                }
            }

            foreach ($previewData as $idx => $row) {
                try {
                    // Determine class_id from mapping or fallback
                    $rowClassId = $fallbackClassId;
                    if (!empty($row['class'])) {
                        $csvClassName = $row['class'];
                        if (isset($createdClasses[$csvClassName])) {
                            $rowClassId = $createdClasses[$csvClassName];
                        } elseif (isset($classMap[$csvClassName]) && $classMap[$csvClassName] !== '__CREATE__') {
                            $rowClassId = (int)$classMap[$csvClassName];
                        }
                    }

                    if (!$rowClassId) {
                        $errors[] = "Rad " . ($idx + 1) . ": Ingen klass vald för '{$row['class']}'";
                        continue;
                    }

                    // Find or create rider
                    $firstname = $row['firstname'] ?? '';
                    $lastname = $row['lastname'] ?? '';

                    if (empty($firstname) && !empty($row['name'])) {
                        $parts = explode(' ', $row['name'], 2);
                        $firstname = $parts[0] ?? '';
                        $lastname = $parts[1] ?? '';
                    }

                    if (empty($firstname)) continue;

                    // Try to find existing rider
                    $rider = $db->getRow(
                        "SELECT id FROM riders WHERE firstname = ? AND lastname = ? LIMIT 1",
                        [$firstname, $lastname]
                    );

                    if (!$rider) {
                        // Create new rider
                        $clubId = null;
                        if (!empty($row['club'])) {
                            $club = $db->getRow("SELECT id FROM clubs WHERE name LIKE ? LIMIT 1", ['%' . $row['club'] . '%']);
                            $clubId = $club ? $club['id'] : null;
                        }

                        $stmt = $pdo->prepare("INSERT INTO riders (firstname, lastname, club_id, active) VALUES (?, ?, ?, 1)");
                        $stmt->execute([$firstname, $lastname, $clubId]);
                        $riderId = $pdo->lastInsertId();
                    } else {
                        $riderId = $rider['id'];
                    }

                    // Calculate best time
                    $run1 = floatval($row['run1'] ?? 0);
                    $run2 = floatval($row['run2'] ?? 0);
                    $best = floatval($row['best'] ?? 0);

                    if ($best <= 0) {
                        $best = $run1;
                        if ($run2 > 0 && $run2 < $best) {
                            $best = $run2;
                        }
                    }

                    // Insert qualifying result
                    $stmt = $pdo->prepare("
                        INSERT INTO elimination_qualifying
                        (event_id, class_id, rider_id, bib_number, run_1_time, run_2_time, best_time, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'finished')
                        ON DUPLICATE KEY UPDATE
                        bib_number = VALUES(bib_number),
                        run_1_time = VALUES(run_1_time),
                        run_2_time = VALUES(run_2_time),
                        best_time = VALUES(best_time)
                    ");
                    $stmt->execute([
                        $eventId,
                        $rowClassId,
                        $riderId,
                        $row['bib'] ?? null,
                        $run1 > 0 ? $run1 : null,
                        $run2 > 0 ? $run2 : null,
                        $best > 0 ? $best : null
                    ]);

                    // If final position is provided, insert into elimination_results
                    $finalPos = intval($row['final_position'] ?? 0);
                    if ($finalPos > 0) {
                        $stmt = $pdo->prepare("
                            INSERT INTO elimination_results
                            (event_id, class_id, rider_id, final_position)
                            VALUES (?, ?, ?, ?)
                            ON DUPLICATE KEY UPDATE
                            final_position = VALUES(final_position)
                        ");
                        $stmt->execute([$eventId, $rowClassId, $riderId, $finalPos]);

                        // Track that this class has final results
                        if (!isset($classesWithFinalResults[$rowClassId])) {
                            $classesWithFinalResults[$rowClassId] = true;
                        }
                    }

                    $classesImported[$rowClassId] = true;
                    $imported++;
                } catch (Exception $e) {
                    $errors[] = "Rad " . ($idx + 1) . ": " . $e->getMessage();
                }
            }

            // Get class mappings for this event (DS class -> series class)
            $classMappings = [];
            try {
                $mappingsRaw = $db->getAll("
                    SELECT ds_class_id, series_class_id FROM elimination_class_mapping
                    WHERE event_id = ?
                ", [$eventId]);
                foreach ($mappingsRaw as $m) {
                    $classMappings[$m['ds_class_id']] = $m['series_class_id'];
                }
            } catch (Exception $e) {
                // Table might not exist yet
            }

            // Update seed positions and sync to results table for all imported classes
            foreach (array_keys($classesImported) as $impClassId) {
                $qualifiers = $db->getAll("
                    SELECT eq.id, eq.rider_id, eq.bib_number, eq.best_time
                    FROM elimination_qualifying eq
                    WHERE eq.event_id = ? AND eq.class_id = ?
                    ORDER BY eq.best_time ASC
                ", [$eventId, $impClassId]);

                // Determine which class to use for series points (mapped or same)
                $seriesClassId = $classMappings[$impClassId] ?? $impClassId;

                $pos = 1;
                foreach ($qualifiers as $q) {
                    // Update seed position
                    $pdo->prepare("UPDATE elimination_qualifying SET seed_position = ? WHERE id = ?")->execute([$pos, $q['id']]);
                    $pos++;
                }

                // Sync to results - use final positions if imported, otherwise use seed positions
                if (isset($classesWithFinalResults[$impClassId])) {
                    // Use final_position from elimination_results
                    $finalResults = $db->getAll("
                        SELECT er.rider_id, er.final_position, eq.bib_number, eq.best_time
                        FROM elimination_results er
                        JOIN elimination_qualifying eq ON eq.event_id = er.event_id
                            AND eq.class_id = er.class_id AND eq.rider_id = er.rider_id
                        WHERE er.event_id = ? AND er.class_id = ?
                        ORDER BY er.final_position ASC
                    ", [$eventId, $impClassId]);

                    foreach ($finalResults as $fr) {
                        $stmt = $pdo->prepare("
                            INSERT INTO results (event_id, class_id, cyclist_id, position, finish_time, bib_number, status)
                            VALUES (?, ?, ?, ?, ?, ?, 'finished')
                            ON DUPLICATE KEY UPDATE
                            position = VALUES(position),
                            finish_time = VALUES(finish_time),
                            bib_number = VALUES(bib_number),
                            status = VALUES(status)
                        ");
                        $stmt->execute([
                            $eventId,
                            $seriesClassId,
                            $fr['rider_id'],
                            $fr['final_position'],
                            $fr['best_time'],
                            $fr['bib_number']
                        ]);
                    }
                } else {
                    // No final results - use seed positions (qualifying only)
                    $seedPos = 1;
                    foreach ($qualifiers as $q) {
                        $stmt = $pdo->prepare("
                            INSERT INTO results (event_id, class_id, cyclist_id, position, finish_time, bib_number, status)
                            VALUES (?, ?, ?, ?, ?, ?, 'finished')
                            ON DUPLICATE KEY UPDATE
                            position = VALUES(position),
                            finish_time = VALUES(finish_time),
                            bib_number = VALUES(bib_number),
                            status = VALUES(status)
                        ");
                        $stmt->execute([
                            $eventId,
                            $seriesClassId,
                            $q['rider_id'],
                            $seedPos,
                            $q['best_time'],
                            $q['bib_number']
                        ]);
                        $seedPos++;
                    }
                }
            }

            $numClasses = count($classesImported);
            $numFinalClasses = count($classesWithFinalResults);
            if ($numFinalClasses > 0) {
                $_SESSION['success'] = "Importerade $imported resultat med slutplaceringar i $numFinalClasses klass(er)! Resultaten är nu synkade.";
            } else {
                $_SESSION['success'] = "Importerade $imported kvalificeringsresultat i $numClasses klass(er)! Resultaten är nu synkade.";
            }
            if (!empty($errors)) {
                $_SESSION['warning'] = implode('<br>', array_slice($errors, 0, 5));
            }

            unset($_SESSION['elimination_import_preview']);
            unset($_SESSION['elimination_import_event']);

            $redirectClassId = $fallbackClassId ?: array_key_first($classesImported);
            header("Location: /admin/elimination-manage.php?event_id={$eventId}&class_id={$redirectClassId}");
            exit;
        }
    }
}

// Page config
$page_title = 'Importera DS-resultat';
$breadcrumbs = [
    ['label' => 'Elimination', 'url' => '/admin/elimination.php'],
    ['label' => $event['name'], 'url' => "/admin/elimination-manage.php?event_id={$eventId}"],
    ['label' => 'Importera']
];

include __DIR__ . '/components/unified-layout.php';
?>

<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h3>Importera DS-resultat</h3>
    </div>
    <div class="admin-card-body">
        <p class="mb-md">Ladda upp en CSV-fil med kvalificeringstider och/eller slutresultat. Filen ska innehålla kolumner för:</p>
        <ul class="mb-lg" style="margin-left: var(--space-lg); color: var(--color-text-secondary);">
            <li><strong>Startnr</strong> (valfritt) - Startnummer</li>
            <li><strong>Namn</strong> eller <strong>Förnamn + Efternamn</strong> - Deltagarens namn</li>
            <li><strong>Klubb</strong> (valfritt) - Cykelklubb</li>
            <li><strong>Klass</strong> (valfritt) - Tävlingsklass</li>
            <li><strong>Serieklass</strong> (valfritt) - Klass för seriepoäng (om annan än tävlingsklass)</li>
            <li><strong>Kval 1</strong> - Tid för första kvalåket</li>
            <li><strong>Kval 2</strong> (valfritt) - Tid för andra kvalåket</li>
            <li><strong>Bäst</strong> (valfritt) - Bästa tid (beräknas automatiskt om ej angiven)</li>
            <li><strong>Slutplacering</strong> (valfritt) - Slutplacering från bracket (för avverkade event)</li>
        </ul>

        <form method="POST" enctype="multipart/form-data">
            <input type="hidden" name="action" value="preview">

            <div class="admin-form-group">
                <label class="admin-form-label">Välj CSV-fil</label>
                <input type="file" name="csv_file" accept=".csv,.txt" class="admin-form-input" required>
                <p class="form-help">Stöder CSV med komma, semikolon eller tab som separator.</p>
            </div>

            <button type="submit" class="btn-admin btn-admin-primary">
                <i data-lucide="eye"></i> Förhandsgranska
            </button>
        </form>
    </div>
</div>

<?php if (!empty($previewData)):
    // Check if CSV has class data and match to existing classes
    $hasClassData = false;
    $csvClasses = [];
    $classMatches = []; // CSV class name => ['count' => N, 'matched_id' => X or null, 'matched_name' => Y]

    // Build class lookup
    $classLookup = [];
    foreach ($classes as $c) {
        $classLookup[strtolower($c['name'])] = $c;
        if (!empty($c['display_name'])) {
            $classLookup[strtolower($c['display_name'])] = $c;
        }
    }

    // Helper to find matching class
    $findMatchingClass = function($csvClassName) use ($classes, $classLookup) {
        $csvLower = strtolower(trim($csvClassName));
        if (isset($classLookup[$csvLower])) {
            return $classLookup[$csvLower];
        }
        // Partial match
        foreach ($classes as $c) {
            $dbName = strtolower($c['name']);
            $dbDisplay = strtolower($c['display_name'] ?? '');
            if (strpos($dbName, $csvLower) !== false || strpos($csvLower, $dbName) !== false) {
                return $c;
            }
            if ($dbDisplay && (strpos($dbDisplay, $csvLower) !== false || strpos($csvLower, $dbDisplay) !== false)) {
                return $c;
            }
        }
        return null;
    };

    foreach ($previewData as $row) {
        if (!empty($row['class'])) {
            $hasClassData = true;
            $className = $row['class'];
            if (!isset($classMatches[$className])) {
                $match = $findMatchingClass($className);
                $classMatches[$className] = [
                    'count' => 0,
                    'matched_id' => $match ? $match['id'] : null,
                    'matched_name' => $match ? ($match['display_name'] ?? $match['name']) : null
                ];
            }
            $classMatches[$className]['count']++;
        }
    }
?>
<div class="admin-card">
    <div class="admin-card-header">
        <h3>Förhandsgranskning (<?= count($previewData) ?> rader)</h3>
    </div>
    <div class="admin-card-body">
        <form method="POST">
            <input type="hidden" name="action" value="import">

            <?php if ($hasClassData): ?>
            <div class="mb-lg">
                <h4 class="mb-sm">Klassmatchning</h4>
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Klass i CSV</th>
                            <th>Antal</th>
                            <th>Mappa till</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($classMatches as $csvName => $info): ?>
                        <tr>
                            <td><strong><?= h($csvName) ?></strong></td>
                            <td><?= $info['count'] ?></td>
                            <td>
                                <select name="class_map[<?= h($csvName) ?>]" class="form-select form-select-sm">
                                    <option value="__CREATE__" <?= !$info['matched_id'] ? 'selected' : '' ?>>
                                        + Skapa ny klass "<?= h($csvName) ?>"
                                    </option>
                                    <?php foreach ($classes as $c): ?>
                                    <option value="<?= $c['id'] ?>" <?= $info['matched_id'] == $c['id'] ? 'selected' : '' ?>>
                                        <?= h($c['display_name'] ?? $c['name']) ?>
                                    </option>
                                    <?php endforeach; ?>
                                </select>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            <input type="hidden" name="class_id" value="0">
            <?php else: ?>
            <div class="admin-form-group mb-lg">
                <label class="admin-form-label">Importera till klass (CSV saknar klassinfo)</label>
                <select name="class_id" class="admin-form-select" required>
                    <option value="">-- Välj klass --</option>
                    <?php foreach ($classes as $c): ?>
                        <option value="<?= $c['id'] ?>" <?= $classId == $c['id'] ? 'selected' : '' ?>>
                            <?= h($c['display_name'] ?? $c['name']) ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <?php endif; ?>

            <?php
            // Check if any row has final_position
            $hasFinalPositions = false;
            foreach ($previewData as $row) {
                if (!empty($row['final_position'])) {
                    $hasFinalPositions = true;
                    break;
                }
            }
            ?>
            <div class="admin-table-container mb-lg">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Nr</th>
                            <th>Namn</th>
                            <th>Klubb</th>
                            <th>Klass (CSV)</th>
                            <th class="text-right">Kval 1</th>
                            <th class="text-right">Kval 2</th>
                            <th class="text-right">Bäst</th>
                            <?php if ($hasFinalPositions): ?>
                            <th class="text-right">Slutplac.</th>
                            <?php endif; ?>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($previewData as $idx => $row): ?>
                            <tr>
                                <td><?= $idx + 1 ?></td>
                                <td><?= h($row['bib'] ?? '-') ?></td>
                                <td>
                                    <?php
                                    $name = '';
                                    if (!empty($row['firstname'])) {
                                        $name = $row['firstname'] . ' ' . ($row['lastname'] ?? '');
                                    } elseif (!empty($row['name'])) {
                                        $name = $row['name'];
                                    }
                                    echo h($name);
                                    ?>
                                </td>
                                <td><?= h($row['club'] ?? '-') ?></td>
                                <td><?= h($row['class'] ?? '-') ?></td>
                                <td class="text-right"><?= isset($row['run1']) && $row['run1'] > 0 ? number_format($row['run1'], 3) : '-' ?></td>
                                <td class="text-right"><?= isset($row['run2']) && $row['run2'] > 0 ? number_format($row['run2'], 3) : '-' ?></td>
                                <td class="text-right"><strong><?= isset($row['best']) && $row['best'] > 0 ? number_format($row['best'], 3) : '-' ?></strong></td>
                                <?php if ($hasFinalPositions): ?>
                                <td class="text-right"><?= !empty($row['final_position']) ? $row['final_position'] : '-' ?></td>
                                <?php endif; ?>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <div class="admin-form-group mb-lg">
                <label class="admin-form-label" style="display: flex; align-items: center; gap: var(--space-sm); cursor: pointer;">
                    <input type="checkbox" name="clear_existing" value="1" checked style="width: 18px; height: 18px;">
                    <span>Rensa befintliga resultat för dessa klasser innan import</span>
                </label>
                <p class="form-help" style="margin-left: 26px;">Rekommenderas för att undvika dubbletter. Rensar kvalificering, bracket och huvudresultat.</p>
            </div>

            <div class="flex gap-md">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="upload"></i> Importera <?= count($previewData) ?> resultat
                </button>
                <a href="/admin/elimination-import-qualifying.php?event_id=<?= $eventId ?>" class="btn-admin btn-admin-secondary">
                    Avbryt
                </a>
            </div>
        </form>
    </div>
</div>
<?php endif; ?>

<!-- Example Format -->
<div class="admin-card mt-lg">
    <div class="admin-card-header">
        <h3>Exempelformat</h3>
    </div>
    <div class="admin-card-body">
        <p class="mb-md"><strong>Bara kvalificering</strong> (för att sedan köra bracket i systemet):</p>
        <pre style="background: var(--color-bg-secondary); padding: var(--space-md); border-radius: var(--radius-md); overflow-x: auto; font-size: var(--text-sm); margin-bottom: var(--space-md);">Startnr;Namn;Klubb;Klass;Kval 1;Kval 2;Bäst
5;Theodor Ek;CK Fix;Ungdom Pojkar;12,977;13,051;12,977
9;Arvid Andersson;Falkenbergs CK;Ungdom Pojkar;13,625;13,407;13,407
14;Leo Drotz;Mera Lera MTB;Ungdom Pojkar;13,477;13,950;13,477</pre>

        <p class="mb-md"><strong>Avverkat event med slutplaceringar</strong> (hoppar över bracket):</p>
        <pre style="background: var(--color-bg-secondary); padding: var(--space-md); border-radius: var(--radius-md); overflow-x: auto; font-size: var(--text-sm);">Startnr;Namn;Klubb;Klass;Serieklass;Kval 1;Kval 2;Bäst;Slutplacering
5;Theodor Ek;CK Fix;Ungdom Pojkar;Pojkar U15;12,977;13,051;12,977;1
9;Arvid Andersson;Falkenbergs CK;Ungdom Pojkar;Pojkar U15;13,625;13,407;13,407;2
14;Leo Drotz;Mera Lera MTB;Ungdom Pojkar;Pojkar U15;13,477;13,950;13,477;3
22;Erik Svensson;SISU CK;Ungdom Pojkar;Pojkar U15;14,125;14,250;14,125;4</pre>
        <p class="form-help mt-sm">
            <a href="/templates/import-ds-complete-template.csv" download>
                <i data-lucide="download" style="width: 14px; height: 14px;"></i>
                Ladda ner mall för avverkade event
            </a>
        </p>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
