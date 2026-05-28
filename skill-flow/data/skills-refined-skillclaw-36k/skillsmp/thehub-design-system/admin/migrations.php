<?php
/**
 * Unified Migration Tool
 *
 * ETT verktyg för ALLA migrationer.
 * Auto-detekterar körda migrationer baserat på databastillstånd.
 * Mobilanpassat.
 *
 * @package TheHUB
 * @version 1.0
 */
require_once __DIR__ . '/../config.php';
require_admin();

$pdo = $GLOBALS['pdo'];

// ============================================================================
// CONFIGURATION
// ============================================================================
$migrationDir = __DIR__ . '/../Tools/migrations/';
$message = '';
$error = '';
$results = [];

// ============================================================================
// AUTO-DETECTION: Define what each migration creates
// ============================================================================
$migrationChecks = [
    '000_governance_core.sql' => [
        'tables' => ['rider_merge_map', 'rider_identity_audit', 'analytics_cron_runs']
    ],
    '001_analytics_tables.sql' => [
        'tables' => ['rider_yearly_stats', 'series_participation', 'analytics_snapshots']
    ],
    '002_series_extensions.php' => [
        'columns' => ['series.series_level', 'series.parent_series_id']
    ],
    '003_seed_series_levels.sql' => [
        'data' => ['series.series_level IS NOT NULL']
    ],
    '007_brands_tables.sql' => [
        'tables' => ['brands', 'brand_series_map']
    ],
    '009_first_season_journey.sql' => [
        'tables' => ['rider_first_season', 'first_season_aggregates', 'first_season_kpi_definitions']
    ],
    '010_longitudinal_journey.sql' => [
        'tables' => ['rider_journey_years', 'rider_journey_summary', 'cohort_longitudinal_aggregates']
    ],
    '011_journey_brand_dimension.sql' => [
        'columns' => ['rider_first_season.first_brand_id'],
        'tables' => ['brand_journey_aggregates']
    ],
    '012_event_participation_analysis.sql' => [
        'tables' => ['series_participation_distribution', 'event_unique_participants', 'event_retention_yearly']
    ],
    '014_performance_indexes.php' => [
        'columns' => [] // PHP migration handles its own checks
    ],
    '015_duplicate_ignores.sql' => [
        'tables' => ['rider_duplicate_ignores']
    ],
    '016_event_ratings.sql' => [
        'tables' => ['event_ratings', 'event_rating_questions', 'event_rating_answers']
    ],
    '017_news_hub_system.sql' => [
        'tables' => ['race_reports', 'race_report_tags', 'race_report_tag_relations', 'race_report_comments', 'race_report_likes', 'news_page_views', 'sponsor_settings']
    ],
    '018_news_hub_columns.sql' => [
        'columns' => ['race_reports.youtube_url', 'race_reports.moderated_by']
    ],
    '019_scf_license_sync.sql' => [
        'tables' => ['scf_license_cache', 'scf_license_history', 'scf_sync_log', 'scf_match_candidates'],
        'columns' => ['riders.scf_license_verified_at', 'riders.scf_license_year', 'riders.scf_license_type', 'riders.scf_disciplines', 'riders.scf_club_name']
    ],
    '020_merge_map_names.sql' => [
        'columns' => ['rider_merge_map.merged_firstname', 'rider_merge_map.merged_lastname', 'rider_merge_map.merged_license_number']
    ],
    '021_winback_survey.sql' => [
        'tables' => ['winback_campaigns', 'winback_questions', 'winback_responses', 'winback_answers']
    ],
    '022_winback_invitations.sql' => [
        'tables' => ['winback_invitations'],
        'columns' => ['winback_campaigns.owner_user_id', 'winback_campaigns.allow_promotor_access']
    ],
    '023_winback_audience_type.sql' => [
        'columns' => ['winback_campaigns.audience_type']
    ],
    '024_artist_name_linking.sql' => [
        'tables' => ['artist_name_claims'],
        'columns' => ['riders.is_anonymous', 'riders.anonymous_source', 'riders.merged_into_rider_id']
    ],
];

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================
function tableExists(PDO $pdo, string $table): bool {
    try {
        $stmt = $pdo->query("SELECT 1 FROM `$table` LIMIT 1");
        return true;
    } catch (Exception $e) {
        return false;
    }
}

function columnExists(PDO $pdo, string $table, string $column): bool {
    try {
        $stmt = $pdo->prepare("
            SELECT COUNT(*) FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = ?
            AND COLUMN_NAME = ?
        ");
        $stmt->execute([$table, $column]);
        return $stmt->fetchColumn() > 0;
    } catch (Exception $e) {
        return false;
    }
}

function checkMigrationStatus(PDO $pdo, array $checks): array {
    $totalChecks = 0;
    $passedChecks = 0;
    $details = [];

    // Check tables
    if (!empty($checks['tables'])) {
        foreach ($checks['tables'] as $table) {
            $totalChecks++;
            $exists = tableExists($pdo, $table);
            if ($exists) $passedChecks++;
            $details[] = ['type' => 'table', 'name' => $table, 'exists' => $exists];
        }
    }

    // Check columns (format: "table.column")
    if (!empty($checks['columns'])) {
        foreach ($checks['columns'] as $col) {
            $totalChecks++;
            list($table, $column) = explode('.', $col);
            $exists = columnExists($pdo, $table, $column);
            if ($exists) $passedChecks++;
            $details[] = ['type' => 'column', 'name' => $col, 'exists' => $exists];
        }
    }

    // Check data conditions
    if (!empty($checks['data'])) {
        foreach ($checks['data'] as $condition) {
            $totalChecks++;
            try {
                // Parse "table.condition"
                $parts = explode('.', $condition, 2);
                $table = $parts[0];
                $where = $parts[1] ?? '1=1';
                $stmt = $pdo->query("SELECT COUNT(*) FROM `$table` WHERE $where");
                $exists = $stmt->fetchColumn() > 0;
            } catch (Exception $e) {
                $exists = false;
            }
            if ($exists) $passedChecks++;
            $details[] = ['type' => 'data', 'name' => $condition, 'exists' => $exists];
        }
    }

    return [
        'total' => $totalChecks,
        'passed' => $passedChecks,
        'status' => ($totalChecks > 0 && $passedChecks === $totalChecks) ? 'executed' :
                   ($passedChecks > 0 ? 'partial' : 'pending'),
        'details' => $details
    ];
}

// ============================================================================
// GET MIGRATIONS
// ============================================================================
$migrations = [];

if (is_dir($migrationDir)) {
    $files = glob($migrationDir . '*.{sql,php}', GLOB_BRACE);

    foreach ($files as $file) {
        $filename = basename($file);

        // Skip non-migration files
        if (!preg_match('/^\d{3}_/', $filename)) continue;

        $checks = $migrationChecks[$filename] ?? [];
        $status = !empty($checks) ? checkMigrationStatus($pdo, $checks) : [
            'status' => 'unknown',
            'total' => 0,
            'passed' => 0,
            'details' => []
        ];

        $migrations[] = [
            'file' => $filename,
            'path' => $file,
            'name' => pathinfo($filename, PATHINFO_FILENAME),
            'type' => pathinfo($filename, PATHINFO_EXTENSION),
            'size' => filesize($file),
            'modified' => filemtime($file),
            'status' => $status['status'],
            'checks' => $status
        ];
    }

    // Sort by filename
    usort($migrations, fn($a, $b) => strcmp($a['file'], $b['file']));
}

// ============================================================================
// HANDLE MIGRATION EXECUTION
// ============================================================================
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['run'])) {
    $filename = $_POST['file'] ?? '';
    $fullPath = $migrationDir . basename($filename);

    if (empty($filename) || !file_exists($fullPath)) {
        $error = 'Ogiltig migration: ' . htmlspecialchars($filename);
    } else {
        $ext = pathinfo($fullPath, PATHINFO_EXTENSION);

        try {
            if ($ext === 'php') {
                ob_start();
                include $fullPath;
                $output = ob_get_clean();
                $results[] = ['status' => 'success', 'message' => 'PHP körd'];
                if ($output) {
                    $results[] = ['status' => 'info', 'message' => $output];
                }
                $message = "Migration '$filename' körd!";
            } else {
                // SQL migration
                $sql = file_get_contents($fullPath);

                // Remove comments
                $sql = preg_replace('/--.*$/m', '', $sql);
                $sql = preg_replace('/\/\*.*?\*\//s', '', $sql);

                // Split statements
                $statements = array_filter(array_map('trim', explode(';', $sql)));

                $success = 0;
                $errors = 0;
                $skipped = 0;

                foreach ($statements as $stmt) {
                    if (empty($stmt)) continue;

                    try {
                        $pdo->exec($stmt);
                        $success++;
                    } catch (PDOException $e) {
                        $errMsg = $e->getMessage();

                        // Ignorable errors
                        $ignorable = ['already exists', 'Duplicate', 'Can\'t DROP'];
                        $isIgnorable = false;
                        foreach ($ignorable as $pattern) {
                            if (stripos($errMsg, $pattern) !== false) {
                                $isIgnorable = true;
                                break;
                            }
                        }

                        if ($isIgnorable) {
                            $skipped++;
                        } else {
                            $errors++;
                            $results[] = ['status' => 'error', 'message' => $errMsg];
                        }
                    }
                }

                if ($errors === 0) {
                    $message = "Migration '$filename' körd! ($success OK, $skipped skippade)";
                } else {
                    $error = "$errors fel uppstod.";
                }
            }
        } catch (Exception $e) {
            $error = 'Fel: ' . $e->getMessage();
        }

        // Refresh status
        header('Location: ' . $_SERVER['REQUEST_URI']);
        exit;
    }
}

// ============================================================================
// PAGE OUTPUT
// ============================================================================
$page_title = 'Migrationer';
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.migration-grid {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.migration-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: var(--space-md);
    align-items: center;
}

.migration-card.status-executed {
    border-left: 4px solid var(--color-success);
}

.migration-card.status-pending {
    border-left: 4px solid var(--color-error);
    background: rgba(239, 68, 68, 0.05);
}

.migration-card.status-partial {
    border-left: 4px solid var(--color-warning);
    background: rgba(251, 191, 36, 0.05);
}

.migration-card.status-unknown {
    border-left: 4px solid var(--color-text-muted);
}

.migration-status {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.migration-status.executed { background: var(--color-success); color: white; }
.migration-status.pending { background: var(--color-error); color: white; }
.migration-status.partial { background: var(--color-warning); color: white; }
.migration-status.unknown { background: var(--color-text-muted); color: white; }

.migration-info {
    min-width: 0;
}

.migration-name {
    font-weight: 600;
    font-size: var(--text-base);
    margin-bottom: 2px;
    word-break: break-word;
}

.migration-meta {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
}

.migration-actions {
    flex-shrink: 0;
}

.btn-run {
    background: var(--color-accent);
    color: white;
    border: none;
    padding: var(--space-xs) var(--space-md);
    border-radius: var(--radius-sm);
    cursor: pointer;
    font-weight: 500;
    font-size: var(--text-sm);
}

.btn-run:hover {
    background: var(--color-accent-hover);
}

.btn-run:disabled {
    background: var(--color-text-muted);
    cursor: not-allowed;
}

.check-list {
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}

.check-item {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin-right: var(--space-sm);
}

.check-item.pass { color: var(--color-success); }
.check-item.fail { color: var(--color-error); }

/* Mobile */
@media (max-width: 767px) {
    .migration-card {
        grid-template-columns: auto 1fr;
        grid-template-rows: auto auto;
    }

    .migration-actions {
        grid-column: 1 / -1;
        display: flex;
        gap: var(--space-sm);
    }

    .migration-actions form,
    .migration-actions .btn-run {
        flex: 1;
    }

    .btn-run {
        width: 100%;
        padding: var(--space-sm);
    }
}

.alert {
    padding: var(--space-md);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-md);
}

.alert-success {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid var(--color-success);
    color: var(--color-success);
}

.alert-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid var(--color-error);
    color: var(--color-error);
}

.summary-bar {
    display: flex;
    gap: var(--space-lg);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}

.summary-item {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}

.summary-count {
    font-weight: 700;
    font-size: var(--text-xl);
}

.summary-label {
    color: var(--color-text-muted);
    font-size: var(--text-sm);
}
</style>

<div class="admin-content">
    <h1 style="margin-bottom: var(--space-lg);">Migrationer</h1>

    <?php if ($message): ?>
        <div class="alert alert-success"><?= htmlspecialchars($message) ?></div>
    <?php endif; ?>

    <?php if ($error): ?>
        <div class="alert alert-error"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <?php
    $executed = count(array_filter($migrations, fn($m) => $m['status'] === 'executed'));
    $pending = count(array_filter($migrations, fn($m) => $m['status'] === 'pending'));
    $partial = count(array_filter($migrations, fn($m) => $m['status'] === 'partial'));
    ?>

    <div class="summary-bar">
        <div class="summary-item">
            <span class="summary-count" style="color: var(--color-success);"><?= $executed ?></span>
            <span class="summary-label">Körda</span>
        </div>
        <div class="summary-item">
            <span class="summary-count" style="color: var(--color-error);"><?= $pending ?></span>
            <span class="summary-label">Väntande</span>
        </div>
        <?php if ($partial > 0): ?>
        <div class="summary-item">
            <span class="summary-count" style="color: var(--color-warning);"><?= $partial ?></span>
            <span class="summary-label">Delvis</span>
        </div>
        <?php endif; ?>
        <div class="summary-item">
            <span class="summary-count"><?= count($migrations) ?></span>
            <span class="summary-label">Totalt</span>
        </div>
    </div>

    <?php if (empty($migrations)): ?>
        <p style="color: var(--color-text-muted);">Inga migrationer hittades i <code><?= htmlspecialchars($migrationDir) ?></code></p>
    <?php else: ?>
        <div class="migration-grid">
            <?php foreach ($migrations as $m): ?>
                <div class="migration-card status-<?= $m['status'] ?>">
                    <div class="migration-status <?= $m['status'] ?>">
                        <?php if ($m['status'] === 'executed'): ?>
                            <i data-lucide="check" style="width:18px;height:18px;"></i>
                        <?php elseif ($m['status'] === 'pending'): ?>
                            <i data-lucide="clock" style="width:18px;height:18px;"></i>
                        <?php elseif ($m['status'] === 'partial'): ?>
                            <i data-lucide="alert-triangle" style="width:18px;height:18px;"></i>
                        <?php else: ?>
                            <i data-lucide="help-circle" style="width:18px;height:18px;"></i>
                        <?php endif; ?>
                    </div>

                    <div class="migration-info">
                        <div class="migration-name"><?= htmlspecialchars($m['name']) ?></div>
                        <div class="migration-meta">
                            <?= strtoupper($m['type']) ?> ·
                            <?= number_format($m['size'] / 1024, 1) ?> KB ·
                            <?= date('Y-m-d', $m['modified']) ?>
                        </div>
                        <?php if (!empty($m['checks']['details'])): ?>
                            <div class="check-list">
                                <?php foreach ($m['checks']['details'] as $check): ?>
                                    <span class="check-item <?= $check['exists'] ? 'pass' : 'fail' ?>">
                                        <?= $check['exists'] ? '✓' : '✗' ?> <?= htmlspecialchars($check['name']) ?>
                                    </span>
                                <?php endforeach; ?>
                            </div>
                        <?php endif; ?>
                    </div>

                    <div class="migration-actions">
                        <?php if ($m['status'] !== 'executed'): ?>
                            <form method="POST" onsubmit="return confirm('Kör <?= htmlspecialchars($m['file']) ?>?')">
                                <input type="hidden" name="file" value="<?= htmlspecialchars($m['file']) ?>">
                                <button type="submit" name="run" class="btn-run">Kör</button>
                            </form>
                        <?php else: ?>
                            <button class="btn-run" disabled>Körd</button>
                        <?php endif; ?>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
