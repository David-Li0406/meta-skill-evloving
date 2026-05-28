<?php
/**
 * Admin Tool - Run Database Migrations
 * TheHUB V3
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $GLOBALS['pdo'];
$message = '';
$error = '';
$results = [];

// Ensure migrations_log table exists
try {
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS migrations_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration_file VARCHAR(255) NOT NULL UNIQUE,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ");
} catch (Exception $e) {
    // Ignore if already exists
}

// Get executed migrations
$executedMigrations = [];
try {
    $stmt = $pdo->query("SELECT migration_file FROM migrations_log");
    $executedMigrations = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    // Table might not exist yet
}

// Get available migrations - check ALL directories and merge
$migrationDirs = [
    'database' => __DIR__ . '/../database/migrations/',
    'analytics' => __DIR__ . '/../analytics/migrations/',
    'root' => __DIR__ . '/../migrations/',
    'admin' => __DIR__ . '/migrations/',
];

$migrations = [];
$todaysMigrations = [];
$today = date('Y-m-d');
$dirSources = []; // Track which dir each file came from

foreach ($migrationDirs as $source => $dir) {
    if (!is_dir($dir)) continue;

    // Get both .sql and .php migration files
    $sqlFiles = glob($dir . '*.sql') ?: [];
    $phpFiles = glob($dir . '*.php') ?: [];

    // Filter out non-migration PHP files
    $phpFiles = array_filter($phpFiles, function($file) {
        $filename = basename($file);
        return preg_match('/^\d{3}_/', $filename);
    });

    $allFiles = array_merge($sqlFiles, $phpFiles);

    foreach ($allFiles as $file) {
        $filename = basename($file);
        $isExecuted = in_array($filename, $executedMigrations);
        $fileDate = date('Y-m-d', filemtime($file));
        $ext = pathinfo($file, PATHINFO_EXTENSION);

        $migrationData = [
            'file' => $filename,
            'path' => $file,
            'name' => pathinfo($file, PATHINFO_FILENAME),
            'executed' => $isExecuted,
            'date' => $fileDate,
            'type' => $ext,
            'source' => $source
        ];

        $migrations[] = $migrationData;
        $dirSources[$filename] = $dir;

        if ($fileDate === $today) {
            $todaysMigrations[] = $migrationData;
        }
    }
}

// Sort by filename
usort($migrations, fn($a, $b) => strcmp($a['file'], $b['file']));
usort($todaysMigrations, fn($a, $b) => strcmp($a['file'], $b['file']));

// Handle migration execution
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['run_migration'])) {
    $migrationFile = $_POST['migration_file'] ?? '';

    if (empty($migrationFile)) {
        $error = 'Ingen migration vald.';
    } else {
        // Find the full path from dirSources or search all dirs
        $fullPath = null;
        if (isset($dirSources[$migrationFile])) {
            $fullPath = $dirSources[$migrationFile] . basename($migrationFile);
        } else {
            // Search all directories
            foreach ($migrationDirs as $dir) {
                $testPath = $dir . basename($migrationFile);
                if (file_exists($testPath)) {
                    $fullPath = $testPath;
                    break;
                }
            }
        }

        if (!$fullPath || !file_exists($fullPath)) {
            $error = 'Migrationsfilen hittades inte: ' . htmlspecialchars($migrationFile);
        } else {
            $ext = pathinfo($fullPath, PATHINFO_EXTENSION);

            try {
                if ($ext === 'php') {
                    // PHP migration - include and run
                    ob_start();
                    include $fullPath;
                    $output = ob_get_clean();

                    $results[] = [
                        'status' => 'success',
                        'message' => 'PHP-migration kördes'
                    ];
                    if (!empty($output)) {
                        $results[] = [
                            'status' => 'info',
                            'message' => $output
                        ];
                    }

                    // Log successful migration
                    try {
                        $logStmt = $pdo->prepare("INSERT IGNORE INTO migrations_log (migration_file) VALUES (?)");
                        $logStmt->execute([$migrationFile]);
                    } catch (Exception $e) {}

                    $message = "PHP-migration '{$migrationFile}' kördes framgångsrikt!";
                    $executedMigrations[] = $migrationFile;

                } else {
                    // SQL migration
                    $sql = file_get_contents($fullPath);

                    // Remove comment lines (lines starting with --)
                    $sqlLines = explode("\n", $sql);
                    $sqlLines = array_filter($sqlLines, fn($line) => !preg_match('/^\s*--/', $line));
                    $sql = implode("\n", $sqlLines);

                    // Split into individual statements
                    $statements = array_filter(
                        array_map('trim', explode(';', $sql)),
                        fn($s) => !empty($s)
                    );

                    $successCount = 0;
                    $errorCount = 0;

                    foreach ($statements as $statement) {
                        if (empty(trim($statement))) continue;

                        try {
                            $pdo->exec($statement);
                            $successCount++;
                            $results[] = [
                                'status' => 'success',
                                'message' => substr($statement, 0, 80) . '...'
                            ];
                        } catch (Exception $e) {
                            $errMsg = $e->getMessage();
                            // Ignore common "already exists" errors
                            $ignorableErrors = [
                                'Duplicate column',
                                'Duplicate key name',
                                'Duplicate entry',
                                'already exists',
                                'check that column/key exists',
                                'Unknown column',
                                'Can\'t DROP',
                                'BLOB/TEXT column',
                            ];

                            $isIgnorable = false;
                            foreach ($ignorableErrors as $pattern) {
                                if (stripos($errMsg, $pattern) !== false) {
                                    $isIgnorable = true;
                                    break;
                                }
                            }

                            if ($isIgnorable) {
                                $results[] = [
                                    'status' => 'skipped',
                                    'message' => 'Redan utförd: ' . substr($statement, 0, 60) . '...'
                                ];
                            } else {
                                $errorCount++;
                                $results[] = [
                                    'status' => 'error',
                                    'message' => $errMsg
                                ];
                            }
                        }
                    }

                    if ($errorCount === 0) {
                        try {
                            $logStmt = $pdo->prepare("INSERT IGNORE INTO migrations_log (migration_file) VALUES (?)");
                            $logStmt->execute([$migrationFile]);
                        } catch (Exception $e) {}
                        $message = "Migration '{$migrationFile}' kördes framgångsrikt! ({$successCount} statements)";
                        $executedMigrations[] = $migrationFile;
                    } else {
                        $error = "Migration kördes med {$errorCount} fel.";
                    }
                }

            } catch (Exception $e) {
                $error = 'Kunde inte köra migration: ' . $e->getMessage();
            }
        }
    }
}

$current_admin_page = 'tools';
$page_title = 'Kör Migrationer';
include __DIR__ . '/components/unified-layout.php';
?>

<style>
/* Migration list */
.migration-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.migration-item {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.migration-item.not-executed {
    background: rgba(239, 68, 68, 0.05);
    border-color: rgba(239, 68, 68, 0.3);
}

.migration-item.today {
    border: 2px solid var(--color-warning);
}

.migration-radio {
    flex-shrink: 0;
}

.migration-radio input[type="radio"] {
    width: 24px;
    height: 24px;
    cursor: pointer;
    accent-color: var(--color-accent);
}

.migration-info {
    flex: 1;
    min-width: 0;
}

.migration-name {
    font-weight: 600;
    word-break: break-word;
    margin-bottom: 4px;
    cursor: pointer;
    display: block;
}

.migration-meta {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
}

.migration-actions {
    display: flex;
    gap: var(--space-xs);
    flex-shrink: 0;
}

.migration-status {
    flex-shrink: 0;
}

/* Form actions */
.form-actions {
    padding: var(--space-md) 0;
}

/* Preview code */
.preview-code {
    background: var(--color-bg-page);
    padding: var(--space-md);
    border-radius: var(--radius-md);
    overflow-x: auto;
    font-size: 12px;
    line-height: 1.5;
    max-height: 400px;
    overflow-y: auto;
}

/* Mobile responsiveness */
@media (max-width: 767px) {
    /* Edge-to-edge cards */
    .card,
    .alert {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0 !important;
        border-left: none !important;
        border-right: none !important;
        width: calc(100% + 32px);
    }

    .migration-item {
        flex-direction: column;
        align-items: stretch;
        gap: var(--space-sm);
        padding: var(--space-md);
    }

    .migration-item > * {
        width: 100%;
    }

    .migration-radio {
        position: absolute;
        right: var(--space-md);
        top: var(--space-md);
    }

    .migration-item {
        position: relative;
        padding-right: 60px;
    }

    .migration-status {
        order: -1;
    }

    .migration-actions {
        display: flex;
        gap: var(--space-sm);
        margin-top: var(--space-sm);
    }

    .migration-actions .btn,
    .migration-actions button {
        flex: 1;
        text-align: center;
        padding: var(--space-sm) var(--space-md);
    }

    .form-actions {
        padding: var(--space-md);
        margin-left: -16px;
        margin-right: -16px;
        width: calc(100% + 32px);
        background: var(--color-bg-surface);
        border-top: 1px solid var(--color-border);
        position: sticky;
        bottom: 0;
    }

    .form-actions .btn {
        width: 100%;
        padding: var(--space-md);
        font-size: var(--text-base);
    }

    .preview-code {
        font-size: 11px;
        padding: var(--space-sm);
        max-height: 300px;
    }

    .content-header {
        padding: var(--space-md) 0;
    }

    .content-header h1 {
        font-size: var(--text-xl);
    }
}

/* Extra small screens */
@media (max-width: 479px) {
    .migration-name {
        font-size: var(--text-sm);
    }

    .badge {
        font-size: 10px;
        padding: 2px 6px;
    }

    .preview-code {
        font-size: 10px;
    }
}
</style>

<div class="admin-content">
    <div class="content-header">
        <h1>Kör Migrationer</h1>
        <p class="text-muted">Uppdatera databasstrukturen</p>
    </div>

    <?php if ($message): ?>
        <div class="alert alert-success"><?= htmlspecialchars($message) ?></div>
    <?php endif; ?>

    <?php if ($error): ?>
        <div class="alert alert-error"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <?php if (!empty($todaysMigrations)): ?>
    <div class="card mb-lg" style="border: 2px solid var(--color-warning);">
        <div class="card-header" style="background: var(--color-warning); color: white;">
            <h3 class="m-0">Nya migrationer idag (<?= date('Y-m-d') ?>)</h3>
        </div>
        <div class="card-body">
            <p class="text-muted mb-md">Dessa migrationer skapades idag och bör köras:</p>
            <div class="migration-list">
                <?php foreach ($todaysMigrations as $migration): ?>
                    <div class="migration-item today <?= !$migration['executed'] ? 'not-executed' : '' ?>">
                        <div class="migration-status">
                            <?php if ($migration['executed']): ?>
                                <span class="badge" style="background: var(--color-success); color: white;">Körd</span>
                            <?php else: ?>
                                <span class="badge" style="background: var(--color-error); color: white;">Ej körd</span>
                            <?php endif; ?>
                        </div>
                        <div class="migration-info">
                            <div class="migration-name">
                                <?= htmlspecialchars($migration['name']) ?>
                                <span class="badge" style="background: <?= ($migration['type'] ?? 'sql') === 'php' ? 'var(--color-info)' : 'var(--color-accent)' ?>; color: white; font-size: 10px; margin-left: 4px;"><?= strtoupper($migration['type'] ?? 'sql') ?></span>
                            </div>
                        </div>
                        <div class="migration-actions">
                            <?php if (!$migration['executed']): ?>
                            <form method="POST" style="display: contents;">
                                <input type="hidden" name="migration_file" value="<?= htmlspecialchars($migration['file']) ?>">
                                <button type="submit" name="run_migration" class="btn btn-sm btn-primary" onclick="return confirm('Kör <?= htmlspecialchars($migration['file']) ?>?')">
                                    Kör nu
                                </button>
                            </form>
                            <?php endif; ?>
                            <a href="?preview=<?= urlencode($migration['file']) ?>" class="btn btn-sm btn-outline">Visa</a>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <?php if (!empty($results)): ?>
        <div class="card mb-lg">
            <div class="card-header">
                <h3>Resultat</h3>
            </div>
            <div class="card-body">
                <div class="migration-list">
                    <?php foreach ($results as $result): ?>
                        <div class="migration-item" style="padding: var(--space-sm);">
                            <div class="migration-status">
                                <?php if ($result['status'] === 'success'): ?>
                                    <span class="badge badge-success">OK</span>
                                <?php elseif ($result['status'] === 'skipped'): ?>
                                    <span class="badge badge-warning">Skip</span>
                                <?php else: ?>
                                    <span class="badge badge-error">Fel</span>
                                <?php endif; ?>
                            </div>
                            <div class="migration-info" style="flex: 1;">
                                <code style="font-size: 11px; word-break: break-all;"><?= htmlspecialchars($result['message']) ?></code>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>
    <?php endif; ?>

    <div class="card">
        <div class="card-header">
            <h3>Tillgängliga migrationer</h3>
        </div>
        <div class="card-body">
            <?php if (empty($migrations)): ?>
                <p class="text-muted">Inga migrationer hittades.</p>
            <?php else: ?>
                <form method="POST">
                    <div class="migration-list">
                        <?php foreach ($migrations as $migration): ?>
                            <div class="migration-item <?= !$migration['executed'] ? 'not-executed' : '' ?>">
                                <?php if (!$migration['executed']): ?>
                                <div class="migration-radio">
                                    <input type="radio" name="migration_file" value="<?= htmlspecialchars($migration['file']) ?>" id="mig_<?= md5($migration['name']) ?>">
                                </div>
                                <?php endif; ?>
                                <div class="migration-status">
                                    <?php if ($migration['executed']): ?>
                                        <span class="badge" style="background: var(--color-success); color: white;">Körd</span>
                                    <?php else: ?>
                                        <span class="badge" style="background: var(--color-error); color: white;">Ej körd</span>
                                    <?php endif; ?>
                                </div>
                                <div class="migration-info">
                                    <label class="migration-name" for="mig_<?= md5($migration['name']) ?>">
                                        <?= htmlspecialchars($migration['name']) ?>
                                    </label>
                                    <div class="migration-meta">
                                        <span class="badge" style="background: <?= ($migration['type'] ?? 'sql') === 'php' ? 'var(--color-info)' : 'var(--color-accent)' ?>; color: white; font-size: 10px;"><?= strtoupper($migration['type'] ?? 'sql') ?></span>
                                        <span class="badge" style="background: var(--color-bg-hover); font-size: 10px;"><?= htmlspecialchars($migration['source'] ?? '') ?></span>
                                        <?= $migration['date'] ?>
                                    </div>
                                </div>
                                <div class="migration-actions">
                                    <a href="?preview=<?= urlencode($migration['file']) ?>" class="btn btn-sm btn-outline">Visa</a>
                                </div>
                            </div>
                        <?php endforeach; ?>
                    </div>

                    <div class="form-actions mt-lg">
                        <button type="submit" name="run_migration" class="btn btn-primary" onclick="return confirm('Är du säker på att du vill köra denna migration?')">
                            Kör vald migration
                        </button>
                    </div>
                </form>
            <?php endif; ?>
        </div>
    </div>

    <?php if (isset($_GET['preview']) && !empty($_GET['preview'])): ?>
        <?php
        $previewFilename = basename($_GET['preview']);
        $previewFile = null;
        $previewSource = '';

        // Search all directories for the file
        if (isset($dirSources[$previewFilename])) {
            $previewFile = $dirSources[$previewFilename] . $previewFilename;
            $previewSource = array_search($dirSources[$previewFilename], $migrationDirs);
        } else {
            foreach ($migrationDirs as $src => $dir) {
                $testPath = $dir . $previewFilename;
                if (file_exists($testPath)) {
                    $previewFile = $testPath;
                    $previewSource = $src;
                    break;
                }
            }
        }

        if ($previewFile && file_exists($previewFile)):
            $previewContent = file_get_contents($previewFile);
        ?>
        <div class="card mt-lg">
            <div class="card-header">
                <h3>Förhandsgranskning: <?= htmlspecialchars($previewFilename) ?></h3>
                <span class="badge"><?= htmlspecialchars($previewSource) ?></span>
            </div>
            <div class="card-body">
                <pre class="preview-code"><?= htmlspecialchars($previewContent) ?></pre>
            </div>
        </div>
        <?php else: ?>
        <div class="alert alert-warning">Filen hittades inte: <?= htmlspecialchars($previewFilename) ?></div>
        <?php endif; ?>
    <?php endif; ?>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
