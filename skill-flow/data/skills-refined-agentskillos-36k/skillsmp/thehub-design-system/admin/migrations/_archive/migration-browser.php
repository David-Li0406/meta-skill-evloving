<?php
/**
 * Migration Browser - List and Run Database Migrations
 * TheHUB V3
 *
 * Lists all SQL migrations and lets admin choose which to run
 */
require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

// Migration directories
$migrationDirs = [
    'database/migrations' => __DIR__ . '/../../database/migrations',
    'admin/migrations' => __DIR__,
    'Tools/migrations' => __DIR__ . '/../../Tools/migrations',
    'analytics/migrations' => __DIR__ . '/../../analytics/migrations'
];

// Get all migration files
$migrations = [];
foreach ($migrationDirs as $label => $dir) {
    if (is_dir($dir)) {
        $files = glob($dir . '/*.sql');
        foreach ($files as $file) {
            $filename = basename($file);
            $migrations[] = [
                'filename' => $filename,
                'path' => $file,
                'dir' => $label,
                'size' => filesize($file),
                'modified' => filemtime($file)
            ];
        }

        // Also get PHP migrations
        $phpFiles = glob($dir . '/*.php');
        foreach ($phpFiles as $file) {
            $filename = basename($file);
            // Skip this file
            if ($filename === 'migration-browser.php') continue;

            $migrations[] = [
                'filename' => $filename,
                'path' => $file,
                'dir' => $label,
                'size' => filesize($file),
                'modified' => filemtime($file),
                'type' => 'php'
            ];
        }
    }
}

// Sort by filename
usort($migrations, function($a, $b) {
    return strcmp($a['filename'], $b['filename']);
});

// Handle viewing a migration
$viewFile = $_GET['view'] ?? null;
$viewContent = null;
if ($viewFile) {
    foreach ($migrations as $m) {
        if ($m['filename'] === $viewFile) {
            $viewContent = file_get_contents($m['path']);
            break;
        }
    }
}

// Handle running a SQL migration
$runFile = $_POST['run'] ?? null;
$runResult = null;
$runError = null;

if ($runFile && $_SERVER['REQUEST_METHOD'] === 'POST') {
    // Verify CSRF if available
    if (function_exists('checkCsrf')) {
        checkCsrf();
    }

    foreach ($migrations as $m) {
        if ($m['filename'] === $runFile && !isset($m['type'])) {
            // Only run .sql files this way
            $sql = file_get_contents($m['path']);

            try {
                // Split by semicolon but be careful with stored procedures
                $statements = array_filter(array_map('trim', explode(';', $sql)));
                $executed = 0;

                foreach ($statements as $statement) {
                    if (!empty($statement)) {
                        $db->query($statement);
                        $executed++;
                    }
                }

                $runResult = "Körde $executed SQL-satser från $runFile";
            } catch (Exception $e) {
                $runError = $e->getMessage();
            }
            break;
        }
    }
}

// Page title
$page_title = 'Migreringshanterare';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Migrationer']
];

include __DIR__ . '/../components/unified-layout.php';
?>

<style>
.migration-list {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.migration-item {
    display: flex;
    align-items: center;
    padding: var(--space-md);
    border-bottom: 1px solid var(--color-border);
    gap: var(--space-md);
}

.migration-item:last-child {
    border-bottom: none;
}

.migration-item:hover {
    background: var(--color-bg-hover);
}

.migration-icon {
    width: 40px;
    height: 40px;
    background: var(--color-bg-sunken);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.migration-icon svg {
    width: 20px;
    height: 20px;
    color: var(--color-text-secondary);
}

.migration-icon.sql {
    background: #DBEAFE;
    color: #2563EB;
}

.migration-icon.sql svg {
    color: #2563EB;
}

.migration-icon.php {
    background: #F3E8FF;
    color: #7C3AED;
}

.migration-icon.php svg {
    color: #7C3AED;
}

.migration-info {
    flex: 1;
    min-width: 0;
}

.migration-name {
    font-weight: 600;
    font-size: var(--text-sm);
    word-break: break-all;
}

.migration-meta {
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    margin-top: 2px;
}

.migration-actions {
    display: flex;
    gap: var(--space-sm);
    flex-shrink: 0;
}

.code-preview {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: var(--space-lg);
    border-radius: var(--radius-lg);
    overflow-x: auto;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 13px;
    line-height: 1.5;
    max-height: 500px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-md);
}

.dir-label {
    font-size: var(--text-xs);
    background: var(--color-bg-sunken);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    color: var(--color-text-secondary);
}
</style>

<?php if ($runResult): ?>
<div class="alert alert-success" style="margin-bottom: var(--space-lg);">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
    </svg>
    <?= htmlspecialchars($runResult) ?>
</div>
<?php endif; ?>

<?php if ($runError): ?>
<div class="alert alert-danger" style="margin-bottom: var(--space-lg);">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
    </svg>
    <strong>Fel:</strong> <?= htmlspecialchars($runError) ?>
</div>
<?php endif; ?>

<?php if ($viewContent !== null): ?>
<!-- View Migration Content -->
<div class="admin-card" style="margin-bottom: var(--space-lg);">
    <div class="admin-card-header">
        <h2>Innehåll: <?= htmlspecialchars($viewFile) ?></h2>
        <a href="/admin/migrations/migration-browser.php" class="btn-admin btn-admin-secondary btn-admin-sm">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
            Tillbaka
        </a>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <pre class="code-preview"><?= htmlspecialchars($viewContent) ?></pre>
    </div>
</div>
<?php endif; ?>

<!-- Warning -->
<div class="alert alert-warning" style="margin-bottom: var(--space-lg);">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
        <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
    <div>
        <strong>Varning:</strong> Migrationer kan göra permanenta ändringar i databasen.
        Granska alltid innehållet innan du kör en migrering. Säkerhetskopiera databasen först!
    </div>
</div>

<!-- Analytics Migrations (Quickstart) -->
<?php
$analyticsMigrations = array_filter($migrations, fn($m) => $m['dir'] === 'Tools/migrations' || $m['dir'] === 'analytics/migrations');
if (!empty($analyticsMigrations)):
?>
<div class="admin-card" style="margin-bottom: var(--space-lg); border: 2px solid var(--color-accent);">
    <div class="admin-card-header" style="background: var(--color-accent-light);">
        <h2 style="color: var(--color-accent);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 20px; height: 20px; vertical-align: middle;">
                <path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>
            </svg>
            Analytics Migrations
        </h2>
    </div>
    <div class="admin-card-body">
        <p style="margin-bottom: var(--space-md);">Kor alla analytics-migrations i ratt ordning:</p>
        <div style="display: flex; gap: var(--space-md); flex-wrap: wrap;">
            <a href="/Tools/migrations/run-migrations.php" target="_blank" class="btn-admin btn-admin-primary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                Kor alla migrations
            </a>
            <a href="/analytics/populate-historical.php" target="_blank" class="btn-admin btn-admin-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>
                Generera historisk data
            </a>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Database Migrations -->
<div class="section-header">
    <h3>SQL-migrationer (database/migrations)</h3>
    <span class="dir-label"><?= count(array_filter($migrations, fn($m) => $m['dir'] === 'database/migrations' && !isset($m['type']))) ?> filer</span>
</div>

<div class="migration-list" style="margin-bottom: var(--space-xl);">
    <?php
    $dbMigrations = array_filter($migrations, fn($m) => $m['dir'] === 'database/migrations' && !isset($m['type']));
    if (empty($dbMigrations)):
    ?>
        <div class="migration-item">
            <em style="color: var(--color-text-secondary);">Inga SQL-migrationer hittades</em>
        </div>
    <?php else: ?>
        <?php foreach ($dbMigrations as $m): ?>
        <div class="migration-item">
            <div class="migration-icon sql">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M3 5V19A9 3 0 0 0 21 19V5"/>
                    <path d="M3 12A9 3 0 0 0 21 12"/>
                </svg>
            </div>
            <div class="migration-info">
                <div class="migration-name"><?= htmlspecialchars($m['filename']) ?></div>
                <div class="migration-meta">
                    <?= number_format($m['size']) ?> bytes ·
                    <?= date('Y-m-d H:i', $m['modified']) ?>
                </div>
            </div>
            <div class="migration-actions">
                <a href="?view=<?= urlencode($m['filename']) ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                    Visa
                </a>
                <form method="POST" style="display: inline;" onsubmit="return confirm('Är du säker på att du vill köra denna migrering?\n\n<?= htmlspecialchars($m['filename']) ?>\n\nDetta kan inte ångras!');">
                    <?php if (function_exists('csrf_field')) echo csrf_field(); ?>
                    <input type="hidden" name="run" value="<?= htmlspecialchars($m['filename']) ?>">
                    <button type="submit" class="btn-admin btn-admin-sm btn-admin-danger">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                        Kör
                    </button>
                </form>
            </div>
        </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<!-- PHP Migrations -->
<div class="section-header">
    <h3>PHP-migrationer (admin/migrations)</h3>
    <span class="dir-label"><?= count(array_filter($migrations, fn($m) => $m['dir'] === 'admin/migrations')) ?> filer</span>
</div>

<div class="migration-list">
    <?php
    $adminMigrations = array_filter($migrations, fn($m) => $m['dir'] === 'admin/migrations');
    if (empty($adminMigrations)):
    ?>
        <div class="migration-item">
            <em style="color: var(--color-text-secondary);">Inga PHP-migrationer hittades</em>
        </div>
    <?php else: ?>
        <?php foreach ($adminMigrations as $m): ?>
        <div class="migration-item">
            <div class="migration-icon <?= isset($m['type']) && $m['type'] === 'php' ? 'php' : 'sql' ?>">
                <?php if (isset($m['type']) && $m['type'] === 'php'): ?>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>
                </svg>
                <?php else: ?>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M3 5V19A9 3 0 0 0 21 19V5"/>
                </svg>
                <?php endif; ?>
            </div>
            <div class="migration-info">
                <div class="migration-name"><?= htmlspecialchars($m['filename']) ?></div>
                <div class="migration-meta">
                    <?= number_format($m['size']) ?> bytes ·
                    <?= date('Y-m-d H:i', $m['modified']) ?>
                    <?php if (isset($m['type']) && $m['type'] === 'php'): ?>
                    · <strong>PHP-script</strong>
                    <?php endif; ?>
                </div>
            </div>
            <div class="migration-actions">
                <a href="?view=<?= urlencode($m['filename']) ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                    Visa
                </a>
                <?php if (isset($m['type']) && $m['type'] === 'php'): ?>
                <a href="/admin/migrations/<?= htmlspecialchars($m['filename']) ?>" class="btn-admin btn-admin-sm btn-admin-warning" onclick="return confirm('Öppna PHP-migreringen?\n\nDenna kommer köras direkt när du öppnar sidan!');">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    Öppna
                </a>
                <?php else: ?>
                <form method="POST" style="display: inline;" onsubmit="return confirm('Är du säker på att du vill köra denna migrering?');">
                    <?php if (function_exists('csrf_field')) echo csrf_field(); ?>
                    <input type="hidden" name="run" value="<?= htmlspecialchars($m['filename']) ?>">
                    <button type="submit" class="btn-admin btn-admin-sm btn-admin-danger">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                        Kör
                    </button>
                </form>
                <?php endif; ?>
            </div>
        </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<!-- Tools/migrations -->
<div class="section-header" style="margin-top: var(--space-xl);">
    <h3>Analytics Migrations (Tools/migrations)</h3>
    <span class="dir-label"><?= count(array_filter($migrations, fn($m) => $m['dir'] === 'Tools/migrations')) ?> filer</span>
</div>

<div class="migration-list" style="margin-bottom: var(--space-xl);">
    <?php
    $toolsMigrations = array_filter($migrations, fn($m) => $m['dir'] === 'Tools/migrations');
    if (empty($toolsMigrations)):
    ?>
        <div class="migration-item">
            <em style="color: var(--color-text-secondary);">Inga migrations hittades</em>
        </div>
    <?php else: ?>
        <?php foreach ($toolsMigrations as $m): ?>
        <div class="migration-item">
            <div class="migration-icon <?= isset($m['type']) && $m['type'] === 'php' ? 'php' : 'sql' ?>">
                <?php if (isset($m['type']) && $m['type'] === 'php'): ?>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>
                </svg>
                <?php else: ?>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M3 5V19A9 3 0 0 0 21 19V5"/>
                </svg>
                <?php endif; ?>
            </div>
            <div class="migration-info">
                <div class="migration-name"><?= htmlspecialchars($m['filename']) ?></div>
                <div class="migration-meta">
                    <?= number_format($m['size']) ?> bytes ·
                    <?= date('Y-m-d H:i', $m['modified']) ?>
                </div>
            </div>
            <div class="migration-actions">
                <a href="?view=<?= urlencode($m['filename']) ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                    Visa
                </a>
                <?php if (isset($m['type']) && $m['type'] === 'php'): ?>
                <a href="/Tools/migrations/<?= htmlspecialchars($m['filename']) ?>" class="btn-admin btn-admin-sm btn-admin-warning" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    Kor
                </a>
                <?php else: ?>
                <form method="POST" style="display: inline;" onsubmit="return confirm('Ar du saker pa att du vill kora denna migrering?');">
                    <?php if (function_exists('csrf_field')) echo csrf_field(); ?>
                    <input type="hidden" name="run" value="<?= htmlspecialchars($m['filename']) ?>">
                    <button type="submit" class="btn-admin btn-admin-sm btn-admin-danger">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                        Kor
                    </button>
                </form>
                <?php endif; ?>
            </div>
        </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<!-- analytics/migrations -->
<div class="section-header">
    <h3>Analytics Source (analytics/migrations)</h3>
    <span class="dir-label"><?= count(array_filter($migrations, fn($m) => $m['dir'] === 'analytics/migrations')) ?> filer</span>
</div>

<div class="migration-list">
    <?php
    $analyticsSrcMigrations = array_filter($migrations, fn($m) => $m['dir'] === 'analytics/migrations');
    if (empty($analyticsSrcMigrations)):
    ?>
        <div class="migration-item">
            <em style="color: var(--color-text-secondary);">Inga migrations hittades</em>
        </div>
    <?php else: ?>
        <?php foreach ($analyticsSrcMigrations as $m): ?>
        <div class="migration-item">
            <div class="migration-icon <?= isset($m['type']) && $m['type'] === 'php' ? 'php' : 'sql' ?>">
                <?php if (isset($m['type']) && $m['type'] === 'php'): ?>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>
                </svg>
                <?php else: ?>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M3 5V19A9 3 0 0 0 21 19V5"/>
                </svg>
                <?php endif; ?>
            </div>
            <div class="migration-info">
                <div class="migration-name"><?= htmlspecialchars($m['filename']) ?></div>
                <div class="migration-meta">
                    <?= number_format($m['size']) ?> bytes ·
                    <?= date('Y-m-d H:i', $m['modified']) ?>
                </div>
            </div>
            <div class="migration-actions">
                <a href="?view=<?= urlencode($m['filename']) ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                    Visa
                </a>
            </div>
        </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
