<?php
/**
 * Sync Club Membership 2025
 *
 * Finds riders who have a club in rider_club_seasons for 2025
 * but their riders.club_id is NULL or different.
 * Syncs the riders.club_id to match their 2025 membership.
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Only super_admin can run this
if (!hasRole('super_admin')) {
    die('Endast super_admin kan köra detta script');
}

$currentYear = date('Y');
$targetYear = isset($_GET['year']) ? (int)$_GET['year'] : (int)$currentYear;
$dryRun = !isset($_GET['execute']);
$direction = $_GET['direction'] ?? 'season_to_rider'; // or 'rider_to_season' or 'rebuild_all_from_results' or 'cleanup_orphans'

// Handle cleanup of orphan club seasons (entries without results)
// ONLY deletes entries from old years (before 2024) to preserve recent verified data
if ($direction === 'cleanup_orphans' && !$dryRun) {
    $safeYear = 2024; // Don't delete 2024 or later - has verified UCI data

    // Find and delete rider_club_seasons entries where:
    // 1. The rider has no results that year
    // 2. The year is before 2024 (older, unverified data)
    $deleted = $db->query("
        DELETE rcs FROM rider_club_seasons rcs
        WHERE rcs.season_year < ?
        AND NOT EXISTS (
            SELECT 1 FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE r.cyclist_id = rcs.rider_id
            AND YEAR(e.date) = rcs.season_year
        )
    ", [$safeYear]);

    $deletedCount = $deleted ? $deleted->rowCount() : 0;

    $_SESSION['cleanup_result'] = ['deleted' => $deletedCount, 'before_year' => $safeYear];
    header("Location: ?year={$targetYear}&cleaned=1");
    exit;
}

// Handle complete rebuild from results
if ($direction === 'rebuild_all_from_results' && !$dryRun) {
    // Get all distinct years from results
    $years = $db->getAll("
        SELECT DISTINCT YEAR(e.date) as year
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE r.club_id IS NOT NULL
        ORDER BY year ASC
    ");

    $totalRebuilt = 0;
    $yearStats = [];

    foreach ($years as $yearRow) {
        $year = (int)$yearRow['year'];
        if ($year < 2000 || $year > 2100) continue; // Sanity check

        // Get first result's club for each rider in this year
        // Using MIN(e.date) to find the first race
        $firstClubs = $db->getAll("
            SELECT
                r.cyclist_id as rider_id,
                r.club_id,
                MIN(e.date) as first_race_date
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE YEAR(e.date) = ?
              AND r.club_id IS NOT NULL
            GROUP BY r.cyclist_id, r.club_id
            HAVING first_race_date = (
                SELECT MIN(e2.date)
                FROM results r2
                JOIN events e2 ON r2.event_id = e2.id
                WHERE r2.cyclist_id = r.cyclist_id
                  AND YEAR(e2.date) = ?
                  AND r2.club_id IS NOT NULL
            )
        ", [$year, $year]);

        $yearCount = 0;
        foreach ($firstClubs as $fc) {
            // Insert or update rider_club_seasons
            $existing = $db->getRow(
                "SELECT id FROM rider_club_seasons WHERE rider_id = ? AND season_year = ?",
                [$fc['rider_id'], $year]
            );

            if ($existing) {
                $db->update('rider_club_seasons',
                    ['club_id' => $fc['club_id'], 'locked' => 1],
                    'id = ?',
                    [$existing['id']]
                );
            } else {
                $db->query(
                    "INSERT INTO rider_club_seasons (rider_id, club_id, season_year, locked) VALUES (?, ?, ?, 1)",
                    [$fc['rider_id'], $fc['club_id'], $year]
                );
            }
            $yearCount++;
        }

        $yearStats[$year] = $yearCount;
        $totalRebuilt += $yearCount;
    }

    // Also update riders.club_id to latest year's club
    $latestYear = max(array_keys($yearStats));
    $db->query("
        UPDATE riders r
        SET r.club_id = (
            SELECT rcs.club_id
            FROM rider_club_seasons rcs
            WHERE rcs.rider_id = r.id AND rcs.season_year = ?
        )
        WHERE EXISTS (
            SELECT 1 FROM rider_club_seasons rcs2
            WHERE rcs2.rider_id = r.id AND rcs2.season_year = ?
        )
    ", [$latestYear, $latestYear]);

    $_SESSION['rebuild_result'] = [
        'total' => $totalRebuilt,
        'years' => $yearStats
    ];

    header("Location: ?year={$targetYear}&rebuilt=1");
    exit;
}

// Find orphan club seasons (entries without any results that year)
// Only show pre-2024 years - 2024+ has verified UCI data that should be kept
$safeYearForPreview = 2024;
$orphanSeasons = $db->getAll("
    SELECT
        rcs.id,
        rcs.rider_id,
        rcs.season_year,
        rcs.club_id,
        r.firstname,
        r.lastname,
        c.name as club_name
    FROM rider_club_seasons rcs
    JOIN riders r ON rcs.rider_id = r.id
    JOIN clubs c ON rcs.club_id = c.id
    WHERE rcs.season_year < ?
    AND NOT EXISTS (
        SELECT 1 FROM results res
        JOIN events e ON res.event_id = e.id
        WHERE res.cyclist_id = rcs.rider_id
        AND YEAR(e.date) = rcs.season_year
    )
    ORDER BY rcs.season_year DESC, r.lastname, r.firstname
    LIMIT 500
", [$safeYearForPreview]);

// Find mismatches: riders with 2025 season club but different/null rider.club_id
$mismatches = $db->getAll("
    SELECT
        r.id as rider_id,
        r.firstname,
        r.lastname,
        r.club_id as current_club_id,
        c_current.name as current_club_name,
        rcs.club_id as season_club_id,
        c_season.name as season_club_name,
        rcs.locked,
        (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as total_results,
        (SELECT COUNT(*) FROM results res
         JOIN events e ON res.event_id = e.id
         WHERE res.cyclist_id = r.id AND YEAR(e.date) = ?) as year_results
    FROM rider_club_seasons rcs
    JOIN riders r ON rcs.rider_id = r.id
    JOIN clubs c_season ON rcs.club_id = c_season.id
    LEFT JOIN clubs c_current ON r.club_id = c_current.id
    WHERE rcs.season_year = ?
    AND (r.club_id IS NULL OR r.club_id != rcs.club_id)
    ORDER BY r.lastname, r.firstname
", [$targetYear, $targetYear]);

// Also find: riders with club_id but NO season entry for target year
$noSeasonEntry = $db->getAll("
    SELECT
        r.id as rider_id,
        r.firstname,
        r.lastname,
        r.club_id as current_club_id,
        c.name as current_club_name,
        (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as total_results,
        (SELECT COUNT(*) FROM results res
         JOIN events e ON res.event_id = e.id
         WHERE res.cyclist_id = r.id AND YEAR(e.date) = ?) as year_results
    FROM riders r
    JOIN clubs c ON r.club_id = c.id
    LEFT JOIN rider_club_seasons rcs ON r.id = rcs.rider_id AND rcs.season_year = ?
    WHERE r.club_id IS NOT NULL
    AND rcs.id IS NULL
    ORDER BY r.lastname, r.firstname
    LIMIT 500
", [$targetYear, $targetYear]);

// Find riders with results this year but club in results differs from rider_club_seasons
$resultsWithDifferentClub = $db->getAll("
    SELECT
        r.id as rider_id,
        r.firstname,
        r.lastname,
        rcs.club_id as season_club_id,
        c_season.name as season_club_name,
        rcs.locked,
        res.club_id as result_club_id,
        c_result.name as result_club_name,
        COUNT(res.id) as result_count
    FROM riders r
    JOIN results res ON r.id = res.cyclist_id
    JOIN events e ON res.event_id = e.id
    LEFT JOIN rider_club_seasons rcs ON r.id = rcs.rider_id AND rcs.season_year = ?
    LEFT JOIN clubs c_season ON rcs.club_id = c_season.id
    JOIN clubs c_result ON res.club_id = c_result.id
    WHERE YEAR(e.date) = ?
      AND res.club_id IS NOT NULL
      AND (rcs.club_id IS NULL OR rcs.club_id != res.club_id)
    GROUP BY r.id, rcs.club_id, res.club_id
    ORDER BY r.lastname, r.firstname
    LIMIT 500
", [$targetYear, $targetYear]);

$syncResult = null;
if (!$dryRun) {
    $synced = 0;

    if ($direction === 'season_to_rider') {
        // Update riders.club_id to match their season club
        foreach ($mismatches as $m) {
            $db->update('riders',
                ['club_id' => $m['season_club_id']],
                'id = ?',
                [$m['rider_id']]
            );
            $synced++;
        }
    } elseif ($direction === 'rider_to_season') {
        // Create season entries from riders.club_id
        foreach ($noSeasonEntry as $r) {
            $db->query(
                "INSERT IGNORE INTO rider_club_seasons (rider_id, club_id, season_year, locked) VALUES (?, ?, ?, 0)",
                [$r['rider_id'], $r['current_club_id'], $targetYear]
            );
            $synced++;
        }
    } elseif ($direction === 'results_to_season') {
        // Create/update season entries from results.club_id
        // This takes the club from the results and sets it as the season club
        foreach ($resultsWithDifferentClub as $r) {
            // Check if entry exists
            $existing = $db->getRow(
                "SELECT id, locked FROM rider_club_seasons WHERE rider_id = ? AND season_year = ?",
                [$r['rider_id'], $targetYear]
            );

            if ($existing) {
                // Only update if not locked (or force)
                if (!$existing['locked']) {
                    $db->update('rider_club_seasons',
                        ['club_id' => $r['result_club_id']],
                        'id = ?',
                        [$existing['id']]
                    );
                    $synced++;
                }
            } else {
                // Create new entry with club from results
                $db->query(
                    "INSERT INTO rider_club_seasons (rider_id, club_id, season_year, locked) VALUES (?, ?, ?, 1)",
                    [$r['rider_id'], $r['result_club_id'], $targetYear]
                );
                $synced++;
            }

            // Also update the rider's profile club
            $db->update('riders', ['club_id' => $r['result_club_id']], 'id = ?', [$r['rider_id']]);
        }
    }

    $syncResult = ['synced' => $synced, 'direction' => $direction];

    // Reload data
    header("Location: ?year={$targetYear}");
    exit;
}

// Page output
$page_title = 'Synka klubbmedlemskap ' . $targetYear;
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Synka klubbmedlemskap']
];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($syncResult): ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>Klart!</strong> <?= $syncResult['synced'] ?> poster synkade
    (<?= $syncResult['direction'] === 'season_to_rider' ? 'säsong → profil' : 'profil → säsong' ?>).
</div>
<?php endif; ?>

<?php if (isset($_GET['cleaned']) && isset($_SESSION['cleanup_result'])): ?>
<?php $cleanupResult = $_SESSION['cleanup_result']; unset($_SESSION['cleanup_result']); ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="trash-2"></i>
    <strong>Städning klar!</strong>
    <?= $cleanupResult['deleted'] ?> klubbtillhörigheter utan resultat har raderats.
</div>
<?php endif; ?>

<?php if (isset($_GET['rebuilt']) && isset($_SESSION['rebuild_result'])): ?>
<?php $rebuildResult = $_SESSION['rebuild_result']; unset($_SESSION['rebuild_result']); ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>Komplett ombyggnad klar!</strong><br>
    Totalt <?= $rebuildResult['total'] ?> klubbtillhörigheter uppdaterade.<br>
    <small>
        Per år:
        <?php foreach ($rebuildResult['years'] as $year => $count): ?>
            <?= $year ?>: <?= $count ?> st<?= array_key_last($rebuildResult['years']) !== $year ? ', ' : '' ?>
        <?php endforeach; ?>
    </small>
</div>
<?php endif; ?>

<div class="alert alert-info mb-lg">
    <i data-lucide="info"></i>
    <strong>Klubbmedlemskap för <?= $targetYear ?></strong><br>
    Hittar åkare där <code>riders.club_id</code> inte matchar <code>rider_club_seasons</code> för <?= $targetYear ?>.
    <br>Detta är kritiskt för klubbmästerskap!
</div>

<!-- Complete Rebuild Card -->
<div class="card mb-lg" style="border: 2px solid var(--color-danger);">
    <div class="card-header" style="background: rgba(239, 68, 68, 0.1);">
        <h3><i data-lucide="rotate-ccw"></i> Komplett ombyggnad av klubbtillhörigheter</h3>
        <p class="text-secondary" style="margin: 0; font-size: 13px;">
            Bygger om ALLA klubbtillhörigheter för ALLA år baserat på resultatdata
        </p>
    </div>
    <div class="card-body">
        <div class="alert alert-warning mb-md">
            <i data-lucide="alert-triangle"></i>
            <strong>Varning!</strong> Detta ersätter alla befintliga klubbtillhörigheter.
            <ul style="margin: var(--space-sm) 0 0; padding-left: var(--space-lg);">
                <li>För varje åkare och år: klubben från <strong>första tävlingen</strong> det året används</li>
                <li>Alla poster markeras som låsta (har resultat)</li>
                <li><code>riders.club_id</code> uppdateras till senaste årets klubb</li>
            </ul>
        </div>
        <a href="?execute=1&direction=rebuild_all_from_results"
           class="btn btn-danger"
           onclick="return confirm('VARNING: Detta kommer att:\n\n1. Ersätta ALLA klubbtillhörigheter (rider_club_seasons)\n2. Basera klubb på första resultatet varje år\n3. Uppdatera riders.club_id till senaste årets klubb\n\nDetta kan inte ångras enkelt.\n\nÄr du säker?')">
            <i data-lucide="database"></i>
            Bygg om alla klubbtillhörigheter från resultat
        </a>
    </div>
</div>

<!-- Cleanup Orphan Seasons -->
<?php if (!empty($orphanSeasons)): ?>
<div class="card mb-lg" style="border: 2px solid var(--color-warning);">
    <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; background: rgba(245, 158, 11, 0.1);">
        <div>
            <h3><i data-lucide="trash-2"></i> Klubbtillhörigheter utan resultat - före 2024 (<?= count($orphanSeasons) ?>)</h3>
            <p class="text-secondary" style="margin: 0; font-size: 13px;">
                Poster från 2016-2023 utan resultat. Data från 2024+ bevaras (verifierad via UCI).
            </p>
        </div>
        <a href="?execute=1&direction=cleanup_orphans"
           class="btn btn-warning"
           onclick="return confirm('Radera <?= count($orphanSeasons) ?> klubbtillhörigheter från 2016-2023 utan resultat?\n\nEndast poster FÖRE 2024 raderas.\nData från 2024 och framåt bevaras.')">
            <i data-lucide="trash-2"></i>
            Radera alla (<?= count($orphanSeasons) ?>)
        </a>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Åkare</th>
                        <th>År</th>
                        <th>Klubb</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($orphanSeasons, 0, 50) as $o): ?>
                    <tr>
                        <td>
                            <a href="/admin/rider-edit/<?= $o['rider_id'] ?>">
                                <?= h($o['firstname'] . ' ' . $o['lastname']) ?>
                            </a>
                        </td>
                        <td><?= $o['season_year'] ?></td>
                        <td><?= h($o['club_name']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if (count($orphanSeasons) > 50): ?>
        <p class="text-secondary">Visar 50 av <?= count($orphanSeasons) ?></p>
        <?php endif; ?>
    </div>
</div>
<?php endif; ?>

<!-- Year selector -->
<div class="card mb-lg">
    <div class="card-body">
        <form method="get" style="display: flex; gap: var(--space-md); align-items: center;">
            <label class="form-label" style="margin: 0;">Välj år:</label>
            <select name="year" class="form-select" style="width: auto;" onchange="this.form.submit()">
                <?php for ($y = (int)$currentYear + 1; $y >= 2015; $y--): ?>
                <option value="<?= $y ?>" <?= $y == $targetYear ? 'selected' : '' ?>><?= $y ?></option>
                <?php endfor; ?>
            </select>
        </form>
    </div>
</div>

<!-- Problem 1: Season club differs from rider.club_id -->
<div class="card mb-lg">
    <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3>Säsongsmedlemskap skiljer sig från profil (<?= count($mismatches) ?>)</h3>
            <p class="text-secondary" style="margin: 0; font-size: 13px;">
                Dessa har <?= $targetYear ?>-medlemskap i historiken men annan/tom klubb i profilen
            </p>
        </div>
        <?php if (!empty($mismatches)): ?>
        <a href="?year=<?= $targetYear ?>&execute=1&direction=season_to_rider"
           class="btn btn-primary"
           onclick="return confirm('Uppdatera <?= count($mismatches) ?> åkares profil-klubb till deras <?= $targetYear ?>-medlemskap?')">
            <i data-lucide="refresh-cw"></i>
            Synka alla till profil (<?= count($mismatches) ?>)
        </a>
        <?php endif; ?>
    </div>
    <div class="card-body">
        <?php if (empty($mismatches)): ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Alla med <?= $targetYear ?>-medlemskap har korrekt klubb i profilen!
        </div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Åkare</th>
                        <th>Nuvarande (profil)</th>
                        <th></th>
                        <th><?= $targetYear ?> (säsong)</th>
                        <th>Resultat <?= $targetYear ?></th>
                        <th>Låst</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($mismatches, 0, 100) as $m): ?>
                    <tr>
                        <td>
                            <a href="/admin/rider-edit/<?= $m['rider_id'] ?>">
                                <?= h($m['firstname'] . ' ' . $m['lastname']) ?>
                            </a>
                        </td>
                        <td>
                            <?php if ($m['current_club_name']): ?>
                                <span class="text-danger"><?= h($m['current_club_name']) ?></span>
                            <?php else: ?>
                                <span class="text-secondary">Ingen klubb</span>
                            <?php endif; ?>
                        </td>
                        <td><i data-lucide="arrow-right" style="width: 16px; color: var(--color-accent);"></i></td>
                        <td><span class="text-success"><strong><?= h($m['season_club_name']) ?></strong></span></td>
                        <td><?= $m['year_results'] ?></td>
                        <td>
                            <?php if ($m['locked']): ?>
                                <span class="badge badge-warning">Låst</span>
                            <?php else: ?>
                                <span class="badge badge-secondary">Ej låst</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if (count($mismatches) > 100): ?>
        <p class="text-secondary">Visar 100 av <?= count($mismatches) ?></p>
        <?php endif; ?>
        <?php endif; ?>
    </div>
</div>

<!-- Problem 2: Has club in profile but no season entry -->
<div class="card mb-lg">
    <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3>Har klubb i profil men saknar <?= $targetYear ?>-medlemskap (<?= count($noSeasonEntry) ?>)</h3>
            <p class="text-secondary" style="margin: 0; font-size: 13px;">
                Dessa har klubb i profilen men ingen post i rider_club_seasons för <?= $targetYear ?>
            </p>
        </div>
        <?php if (!empty($noSeasonEntry)): ?>
        <a href="?year=<?= $targetYear ?>&execute=1&direction=rider_to_season"
           class="btn btn-secondary"
           onclick="return confirm('Skapa <?= $targetYear ?>-medlemskap för <?= count($noSeasonEntry) ?> åkare baserat på deras profilklubb?')">
            <i data-lucide="plus"></i>
            Skapa säsongsposter (<?= count($noSeasonEntry) ?>)
        </a>
        <?php endif; ?>
    </div>
    <div class="card-body">
        <?php if (empty($noSeasonEntry)): ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Alla med klubb i profilen har <?= $targetYear ?>-medlemskap!
        </div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Åkare</th>
                        <th>Klubb (profil)</th>
                        <th>Resultat <?= $targetYear ?></th>
                        <th>Totalt resultat</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($noSeasonEntry, 0, 100) as $r): ?>
                    <tr>
                        <td>
                            <a href="/admin/rider-edit/<?= $r['rider_id'] ?>">
                                <?= h($r['firstname'] . ' ' . $r['lastname']) ?>
                            </a>
                        </td>
                        <td><?= h($r['current_club_name']) ?></td>
                        <td><?= $r['year_results'] ?></td>
                        <td><?= $r['total_results'] ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if (count($noSeasonEntry) > 100): ?>
        <p class="text-secondary">Visar 100 av <?= count($noSeasonEntry) ?></p>
        <?php endif; ?>
        <?php endif; ?>
    </div>
</div>

<!-- Problem 3: Results have club but rider_club_seasons differs -->
<div class="card mb-lg">
    <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3>Klubb i resultat skiljer sig från säsong (<?= count($resultsWithDifferentClub) ?>)</h3>
            <p class="text-secondary" style="margin: 0; font-size: 13px;">
                Dessa har resultat <?= $targetYear ?> med en klubb som skiljer sig från rider_club_seasons
            </p>
        </div>
        <?php if (!empty($resultsWithDifferentClub)): ?>
        <a href="?year=<?= $targetYear ?>&execute=1&direction=results_to_season"
           class="btn btn-warning"
           onclick="return confirm('Synka <?= count($resultsWithDifferentClub) ?> åkares säsongsklubb från deras resultat?\n\nDetta uppdaterar både rider_club_seasons OCH riders.club_id till klubben från resultaten.')">
            <i data-lucide="database"></i>
            Bygg från resultat (<?= count($resultsWithDifferentClub) ?>)
        </a>
        <?php endif; ?>
    </div>
    <div class="card-body">
        <?php if (empty($resultsWithDifferentClub)): ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Alla resultat matchar rider_club_seasons för <?= $targetYear ?>!
        </div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Åkare</th>
                        <th>Säsongsklubb</th>
                        <th></th>
                        <th>Klubb i resultat</th>
                        <th>Antal resultat</th>
                        <th>Låst</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($resultsWithDifferentClub, 0, 100) as $r): ?>
                    <tr>
                        <td>
                            <a href="/admin/rider-edit/<?= $r['rider_id'] ?>">
                                <?= h($r['firstname'] . ' ' . $r['lastname']) ?>
                            </a>
                        </td>
                        <td>
                            <?php if ($r['season_club_name']): ?>
                                <span class="text-danger"><?= h($r['season_club_name']) ?></span>
                            <?php else: ?>
                                <span class="text-secondary">Ingen</span>
                            <?php endif; ?>
                        </td>
                        <td><i data-lucide="arrow-right" style="width: 16px; color: var(--color-warning);"></i></td>
                        <td><span class="text-success"><strong><?= h($r['result_club_name']) ?></strong></span></td>
                        <td><?= $r['result_count'] ?></td>
                        <td>
                            <?php if ($r['locked']): ?>
                                <span class="badge badge-warning">Låst</span>
                            <?php else: ?>
                                <span class="badge badge-secondary">Ej låst</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if (count($resultsWithDifferentClub) > 100): ?>
        <p class="text-secondary">Visar 100 av <?= count($resultsWithDifferentClub) ?></p>
        <?php endif; ?>
        <?php endif; ?>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
