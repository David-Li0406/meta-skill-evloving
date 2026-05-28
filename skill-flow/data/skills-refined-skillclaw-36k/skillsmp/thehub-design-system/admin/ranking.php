<?php
/**
 * Admin Ranking Settings - V3 Design System
 * Manage the 24-month rolling ranking system for Enduro, Downhill, and Gravity
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_admin();

$db = getDB();

$message = '';
$messageType = 'info';

// Check if tables exist
if (!rankingTablesExist($db)) {
    $message = 'Rankingtabeller saknas. Kör migration 072_ranking_snapshots_system.sql för att skapa dem.';
    $messageType = 'warning';
}

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    if (isset($_POST['calculate'])) {
        // Run full ranking update
        try {
            $stats = runFullRankingUpdate($db, false);
            $message = "Beräkning klar! Tid: {$stats['total_time']}s. ";
            $message .= "Enduro: {$stats['enduro']['riders']} åkare, {$stats['enduro']['clubs']} klubbar. ";
            $message .= "DH: {$stats['dh']['riders']} åkare, {$stats['dh']['clubs']} klubbar. ";
            $message .= "Gravity: {$stats['gravity']['riders']} åkare, {$stats['gravity']['clubs']} klubbar.";
            $messageType = 'success';
        } catch (Exception $e) {
            $message = 'Fel vid beräkning: ' . $e->getMessage();
            $messageType = 'error';
        }

    } elseif (isset($_POST['save_multipliers'])) {
        try {
            $multipliers = [];
            for ($i = 1; $i <= 15; $i++) {
                $key = "mult_$i";
                if (isset($_POST[$key])) {
                    $multipliers[$i] = max(0, min(1, (float)$_POST[$key]));
                }
            }

            if (count($multipliers) === 15) {
                saveFieldMultipliers($db, $multipliers);
                $message = 'Fältstorleksmultiplikatorer sparade.';
                $messageType = 'success';
            } else {
                $message = 'Alla 15 multiplikatorer måste anges.';
                $messageType = 'error';
            }
        } catch (Exception $e) {
            $message = 'Fel vid sparande: ' . $e->getMessage();
            $messageType = 'error';
        }

    } elseif (isset($_POST['save_decay'])) {
        $timeDecay = [
            'months_1_12' => max(0, min(1, (float)$_POST['decay_1_12'])),
            'months_13_24' => max(0, min(1, (float)$_POST['decay_13_24'])),
            'months_25_plus' => max(0, min(1, (float)$_POST['decay_25_plus']))
        ];

        saveTimeDecay($db, $timeDecay);
        $message = 'Tidsviktning sparad.';
        $messageType = 'success';

    } elseif (isset($_POST['save_event_level'])) {
        $eventLevel = [
            'national' => max(0, min(1, (float)$_POST['level_national'])),
            'sportmotion' => max(0, min(1, (float)$_POST['level_sportmotion']))
        ];

        saveEventLevelMultipliers($db, $eventLevel);
        $message = 'Eventtypsviktning sparad.';
        $messageType = 'success';

    } elseif (isset($_POST['reset_defaults'])) {
        try {
            saveFieldMultipliers($db, getDefaultFieldMultipliers());
            saveTimeDecay($db, getDefaultTimeDecay());
            saveEventLevelMultipliers($db, getDefaultEventLevelMultipliers());
            $message = 'Inställningar återställda till standardvärden.';
            $messageType = 'success';
        } catch (Exception $e) {
            $message = 'Fel vid återställning: ' . $e->getMessage();
            $messageType = 'error';
        }

    } elseif (isset($_POST['recalc_event_points'])) {
        // Recalculate ranking points for a specific event
        $eventId = intval($_POST['event_id'] ?? 0);
        if ($eventId > 0) {
            try {
                // Get event info
                $event = $db->getRow("SELECT name, event_format FROM events WHERE id = ?", [$eventId]);
                $eventName = $event['name'] ?? "Event $eventId";
                $eventFormat = $event['event_format'] ?? 'ENDURO';

                // Use appropriate recalculation function based on event format
                if (strpos($eventFormat, 'DH') !== false) {
                    $useSwecupDh = ($eventFormat === 'DH_SWECUP');
                    $stats = recalculateDHEventResults($db, $eventId, null, $useSwecupDh);
                } else {
                    $stats = recalculateEventResults($db, $eventId);
                }

                $message = "Poäng beräknade för \"{$eventName}\": {$stats['points_updated']} resultat uppdaterade.";
                $messageType = 'success';

                if (!empty($stats['errors'])) {
                    $message .= " Fel: " . implode(', ', array_slice($stats['errors'], 0, 3));
                    $messageType = 'warning';
                }
            } catch (Exception $e) {
                $message = 'Fel vid poängberäkning: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Get current settings
$multipliers = getRankingFieldMultipliers($db);
$timeDecay = getRankingTimeDecay($db);
$eventLevelMultipliers = getEventLevelMultipliers($db);
$lastCalc = getLastRankingCalculation($db);
$disciplineStats = getRankingStats($db);

$latestSnapshot = $db->getRow("SELECT MAX(snapshot_date) as snapshot_date FROM ranking_snapshots");
$lastSnapshotDate = $latestSnapshot ? $latestSnapshot['snapshot_date'] : null;

// Get active events in ranking (24 months window)
$cutoffDate = date('Y-m-d', strtotime('-24 months'));
$activeEvents = $db->getAll("
    SELECT
        e.id,
        e.name,
        e.date,
        e.location,
        e.discipline,
        COALESCE(e.event_level, 'national') as event_level,
        COUNT(DISTINCT r.cyclist_id) as rider_count,
        COUNT(DISTINCT r.class_id) as class_count,
        CASE
            WHEN e.date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH) THEN '100%'
            ELSE '50%'
        END as time_weight
    FROM events e
    JOIN results r ON r.event_id = e.id
    JOIN classes cl ON r.class_id = cl.id
    WHERE e.discipline IN ('ENDURO', 'DH')
    AND e.date >= ?
    AND r.status = 'finished'
    AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
    AND COALESCE(cl.series_eligible, 1) = 1
    AND COALESCE(cl.awards_points, 1) = 1
    GROUP BY e.id
    ORDER BY e.date DESC
", [$cutoffDate]);

// Get events that SHOULD be in ranking but are missing (diagnostic)
$missingEvents = $db->getAll("
    SELECT
        e.id,
        e.name,
        e.date,
        e.location,
        e.discipline,
        e.event_format,
        COALESCE(e.event_level, 'national') as event_level,
        e.active as event_active,
        (SELECT COUNT(*) FROM results WHERE event_id = e.id) as total_results,
        (SELECT COUNT(*) FROM results WHERE event_id = e.id AND status = 'finished') as finished_results,
        (SELECT COUNT(*) FROM results WHERE event_id = e.id AND (points > 0 OR COALESCE(run_1_points, 0) > 0 OR COALESCE(run_2_points, 0) > 0)) as results_with_points,
        (SELECT GROUP_CONCAT(DISTINCT CONCAT(cl.name, ' (eligible:', COALESCE(cl.series_eligible,1), ',points:', COALESCE(cl.awards_points,1), ')') SEPARATOR ', ')
         FROM results r2
         JOIN classes cl ON r2.class_id = cl.id
         WHERE r2.event_id = e.id) as classes_info,
        CASE
            WHEN e.discipline NOT IN ('ENDURO', 'DH') THEN 'Fel disciplin'
            WHEN e.date < ? THEN 'Äldre än 24 mån'
            WHEN NOT EXISTS (SELECT 1 FROM results r WHERE r.event_id = e.id AND r.status = 'finished') THEN 'Inga finished-resultat'
            WHEN NOT EXISTS (SELECT 1 FROM results r WHERE r.event_id = e.id AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)) THEN 'Inga poäng tilldelade'
            WHEN NOT EXISTS (SELECT 1 FROM results r JOIN classes cl ON r.class_id = cl.id WHERE r.event_id = e.id AND COALESCE(cl.series_eligible, 1) = 1 AND COALESCE(cl.awards_points, 1) = 1) THEN 'Klasser saknar series_eligible/awards_points'
            ELSE 'Okänt'
        END as issue
    FROM events e
    WHERE e.date >= ?
    AND e.date <= CURDATE()
    AND e.id NOT IN (
        SELECT DISTINCT e2.id
        FROM events e2
        JOIN results r ON r.event_id = e2.id
        JOIN classes cl ON r.class_id = cl.id
        WHERE e2.discipline IN ('ENDURO', 'DH')
        AND e2.date >= ?
        AND r.status = 'finished'
        AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
        AND COALESCE(cl.series_eligible, 1) = 1
        AND COALESCE(cl.awards_points, 1) = 1
    )
    AND (e.discipline IN ('ENDURO', 'DH') OR e.event_format LIKE '%DH%' OR e.name LIKE '%SweCup%' OR e.name LIKE '%Enduro%')
    ORDER BY e.date DESC
    LIMIT 20
", [$cutoffDate, $cutoffDate, $cutoffDate]);

// Page config
$page_title = 'Ranking';
$breadcrumbs = [
    ['label' => 'Serier', 'url' => '/admin/series'],
    ['label' => 'Ranking']
];
$page_actions = '<a href="/ranking/" class="btn-admin btn-admin-secondary" target="_blank">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
    Publik vy
</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="admin-alert admin-alert-<?= $messageType ?>">
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Statistics Cards per Discipline -->
<div class="admin-stats-grid">
    <div class="admin-stat-card">
        <div class="admin-stat-value"><?= $disciplineStats['ENDURO']['riders'] ?></div>
        <div class="admin-stat-label">Enduro åkare</div>
        <div class="admin-stat-meta"><?= $disciplineStats['ENDURO']['clubs'] ?> klubbar • <?= $disciplineStats['ENDURO']['events'] ?> events</div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-value"><?= $disciplineStats['DH']['riders'] ?></div>
        <div class="admin-stat-label">Downhill åkare</div>
        <div class="admin-stat-meta"><?= $disciplineStats['DH']['clubs'] ?> klubbar • <?= $disciplineStats['DH']['events'] ?> events</div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-value"><?= $disciplineStats['GRAVITY']['riders'] ?></div>
        <div class="admin-stat-label">Gravity åkare</div>
        <div class="admin-stat-meta"><?= $disciplineStats['GRAVITY']['clubs'] ?> klubbar • <?= $disciplineStats['GRAVITY']['events'] ?> events</div>
    </div>
</div>

<!-- Active Events in Ranking -->
<div class="admin-card" style="margin-bottom: 1.5rem;">
    <div class="admin-card-header">
        <h3>Aktiva events i ranking (<?= count($activeEvents) ?>)</h3>
    </div>
    <div class="admin-card-body">
        <p class="admin-help-text">Events inom 24 månader som bidrar till rankingpoäng. Gul = 50% tidsvikt (13-24 mån).</p>

        <?php if (empty($activeEvents)): ?>
        <div class="admin-alert admin-alert-warning">Inga aktiva events hittades.</div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Event</th>
                        <th>Datum</th>
                        <th>Disciplin</th>
                        <th>Nivå</th>
                        <th>Åkare</th>
                        <th>Klasser</th>
                        <th>Tidsvikt</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($activeEvents as $event): ?>
                    <tr class="<?= $event['time_weight'] === '50%' ? 'row-faded' : '' ?>">
                        <td>
                            <a href="/admin/edit-results.php?event_id=<?= $event['id'] ?>" class="admin-link">
                                <?= h($event['name']) ?>
                            </a>
                            <?php if ($event['location']): ?>
                            <br><small class="text-muted"><?= h($event['location']) ?></small>
                            <?php endif; ?>
                        </td>
                        <td><?= date('Y-m-d', strtotime($event['date'])) ?></td>
                        <td>
                            <span class="admin-badge admin-badge-<?= $event['discipline'] === 'ENDURO' ? 'primary' : 'secondary' ?>">
                                <?= $event['discipline'] ?>
                            </span>
                        </td>
                        <td>
                            <span class="admin-badge admin-badge-<?= $event['event_level'] === 'national' ? 'success' : 'warning' ?>">
                                <?= $event['event_level'] === 'national' ? 'Nationell' : 'Sportmotion' ?>
                            </span>
                        </td>
                        <td><?= $event['rider_count'] ?></td>
                        <td><?= $event['class_count'] ?></td>
                        <td>
                            <span class="admin-badge admin-badge-<?= $event['time_weight'] === '100%' ? 'success' : 'warning' ?>">
                                <?= $event['time_weight'] ?>
                            </span>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Missing Events (Diagnostic) -->
<?php if (!empty($missingEvents)): ?>
<div class="admin-card" style="margin-bottom: 1.5rem;">
    <div class="admin-card-header" style="background: #fef3c7; border-bottom: 1px solid #f59e0b;">
        <h3 style="color: #92400e;">⚠️ Events som saknas i ranking (<?= count($missingEvents) ?>)</h3>
    </div>
    <div class="admin-card-body">
        <p class="admin-help-text">Dessa events matchar Enduro/DH eller SweCup men saknas i ranking. Klicka på "Åtgärd" för att fixa.</p>

        <div class="table-responsive">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Event</th>
                        <th>Datum</th>
                        <th>Disciplin</th>
                        <th>Format</th>
                        <th>Resultat</th>
                        <th>Problem</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($missingEvents as $event): ?>
                    <tr style="background: #fffbeb;">
                        <td>
                            <a href="/admin/event-edit.php?id=<?= $event['id'] ?>" class="admin-link">
                                <?= h($event['name']) ?>
                            </a>
                            <?php if ($event['location']): ?>
                            <br><small class="text-muted"><?= h($event['location']) ?></small>
                            <?php endif; ?>
                        </td>
                        <td><?= date('Y-m-d', strtotime($event['date'])) ?></td>
                        <td>
                            <span class="admin-badge <?= in_array($event['discipline'], ['ENDURO', 'DH']) ? 'admin-badge-success' : 'admin-badge-danger' ?>">
                                <?= h($event['discipline'] ?: 'EJ SATT') ?>
                            </span>
                        </td>
                        <td>
                            <span class="admin-badge admin-badge-secondary">
                                <?= h($event['event_format'] ?: '-') ?>
                            </span>
                        </td>
                        <td>
                            <small>
                                Totalt: <?= $event['total_results'] ?><br>
                                Finished: <?= $event['finished_results'] ?><br>
                                Med poäng: <?= $event['results_with_points'] ?>
                            </small>
                        </td>
                        <td>
                            <span class="admin-badge admin-badge-danger"><?= h($event['issue']) ?></span>
                            <?php if ($event['classes_info']): ?>
                            <br><small style="font-size: 0.65rem; color: #666;"><?= h($event['classes_info']) ?></small>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?php if ($event['issue'] === 'Fel disciplin'): ?>
                            <a href="/admin/event-edit.php?id=<?= $event['id'] ?>" class="btn-admin btn-admin-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.5rem;">
                                Sätt disciplin
                            </a>
                            <?php elseif ($event['issue'] === 'Inga poäng tilldelade'): ?>
                            <form method="POST" style="display: inline;">
                                <?= csrf_field() ?>
                                <input type="hidden" name="event_id" value="<?= $event['id'] ?>">
                                <button type="submit" name="recalc_event_points" class="btn-admin btn-admin-primary" style="font-size: 0.75rem; padding: 0.25rem 0.5rem;">
                                    Beräkna poäng
                                </button>
                            </form>
                            <?php elseif ($event['issue'] === 'Inga finished-resultat'): ?>
                            <a href="/admin/edit-results.php?event_id=<?= $event['id'] ?>" class="btn-admin btn-admin-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.5rem;">
                                Uppdatera status
                            </a>
                            <?php else: ?>
                            <a href="/admin/event-edit.php?id=<?= $event['id'] ?>" class="btn-admin btn-admin-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.5rem;">
                                Redigera
                            </a>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Info and Calculation Cards -->
<div class="admin-grid-2">
    <!-- Info Card -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h3>Om rankingsystemet</h3>
        </div>
        <div class="admin-card-body">
            <ul style="margin: 0; padding-left: 1.25rem; line-height: 1.8;">
                <li>Tre rankingar: <strong>Enduro</strong>, <strong>Downhill</strong>, <strong>Gravity</strong> (kombinerad)</li>
                <li>24 månaders rullande fönster</li>
                <li>Poäng viktas efter fältstorlek (antal deltagare i klassen)</li>
                <li>Nationella event: 100%, Sportmotion: 50% (justerbart)</li>
                <li>Senaste 12 månader: 100% av poängen</li>
                <li>Månad 13-24: 50% av poängen</li>
                <li>Klubbranking: Bästa åkare per klubb/event = 100%, 2:a = 50%</li>
            </ul>
        </div>
    </div>

    <!-- Calculation Card -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h3>Beräkning</h3>
        </div>
        <div class="admin-card-body">
            <p style="margin-bottom: 1rem;">
                <strong>Senaste beräkning:</strong><br>
                <?= $lastCalc['date'] ? date('Y-m-d H:i', strtotime($lastCalc['date'])) : 'Aldrig' ?>
                <?php if ($lastCalc['date'] && isset($lastCalc['stats']['total_time'])): ?>
                    (<?= $lastCalc['stats']['total_time'] ?>s)
                <?php endif; ?>
            </p>
            <p style="margin-bottom: 1rem;">
                <strong>Senaste snapshot:</strong><br>
                <?= $lastSnapshotDate ? date('Y-m-d', strtotime($lastSnapshotDate)) : 'Aldrig' ?>
            </p>

            <form method="POST" style="display: inline-block;">
                <?= csrf_field() ?>
                <button type="submit" name="calculate" class="btn-admin btn-admin-primary"
                    onclick="return confirm('Kör fullständig omräkning av alla rankingpoäng?')">
                    Kör beräkning
                </button>
            </form>
        </div>
    </div>
</div>

<!-- Event Level Multipliers -->
<div class="admin-card">
    <div class="admin-card-header">
        <h3>Eventtypsviktning</h3>
    </div>
    <div class="admin-card-body">
        <p class="admin-help-text">Nationella tävlingar ger fulla poäng. Sportmotion-event kan viktas ned.</p>

        <form method="POST">
            <?= csrf_field() ?>

            <div class="admin-form-row">
                <div class="admin-form-group">
                    <label class="admin-form-label">Nationell tävling</label>
                    <input type="number" name="level_national"
                        value="<?= number_format($eventLevelMultipliers['national'], 2) ?>"
                        min="0" max="1" step="0.01"
                        class="admin-form-input">
                    <span class="admin-form-hint">Standard 1.00 (100%)</span>
                </div>
                <div class="admin-form-group">
                    <label class="admin-form-label">Sportmotion</label>
                    <input type="number" name="level_sportmotion"
                        value="<?= number_format($eventLevelMultipliers['sportmotion'], 2) ?>"
                        min="0" max="1" step="0.01"
                        class="admin-form-input">
                    <span class="admin-form-hint">Standard 0.50 (50%)</span>
                </div>
            </div>

            <button type="submit" name="save_event_level" class="btn-admin btn-admin-primary">
                Spara eventtypsviktning
            </button>
        </form>
    </div>
</div>

<!-- Field Multipliers -->
<div class="admin-card">
    <div class="admin-card-header">
        <h3>Fältstorleksmultiplikatorer</h3>
    </div>
    <div class="admin-card-body">
        <p class="admin-help-text">Ju fler åkare i klassen, desto mer värda är poängen.</p>

        <form method="POST" id="multipliersForm">
            <?= csrf_field() ?>

            <!-- Visual bar chart -->
            <div class="multiplier-bars">
                <?php for ($i = 1; $i <= 15; $i++): ?>
                <?php $value = $multipliers[$i] ?? 0.75; ?>
                <div class="multiplier-bar-col">
                    <div class="multiplier-bar" id="bar_<?= $i ?>" style="height: <?= $value * 100 ?>px;"></div>
                    <span class="multiplier-label"><?= $i === 15 ? '15+' : $i ?></span>
                </div>
                <?php endfor; ?>
            </div>

            <!-- Input grid -->
            <div class="multiplier-inputs">
                <?php for ($i = 1; $i <= 15; $i++): ?>
                <div class="multiplier-input-col">
                    <label><?= $i === 15 ? '15+' : $i ?></label>
                    <input type="number"
                        name="mult_<?= $i ?>"
                        id="mult_<?= $i ?>"
                        value="<?= number_format($multipliers[$i] ?? 0.75, 2) ?>"
                        min="0" max="1" step="0.01"
                        class="admin-form-input"
                        oninput="updateBar(<?= $i ?>, this.value)">
                </div>
                <?php endfor; ?>
            </div>

            <button type="submit" name="save_multipliers" class="btn-admin btn-admin-primary">
                Spara multiplikatorer
            </button>
        </form>
    </div>
</div>

<!-- Time Decay Settings -->
<div class="admin-card">
    <div class="admin-card-header">
        <h3>Tidsviktning</h3>
    </div>
    <div class="admin-card-body">
        <form method="POST">
            <?= csrf_field() ?>

            <div class="admin-form-row">
                <div class="admin-form-group">
                    <label class="admin-form-label">Månad 1-12</label>
                    <input type="number" name="decay_1_12"
                        value="<?= number_format($timeDecay['months_1_12'], 2) ?>"
                        min="0" max="1" step="0.01"
                        class="admin-form-input">
                    <span class="admin-form-hint">Senaste 12 månaderna</span>
                </div>
                <div class="admin-form-group">
                    <label class="admin-form-label">Månad 13-24</label>
                    <input type="number" name="decay_13_24"
                        value="<?= number_format($timeDecay['months_13_24'], 2) ?>"
                        min="0" max="1" step="0.01"
                        class="admin-form-input">
                    <span class="admin-form-hint">Förra årets resultat</span>
                </div>
                <div class="admin-form-group">
                    <label class="admin-form-label">Månad 25+</label>
                    <input type="number" name="decay_25_plus"
                        value="<?= number_format($timeDecay['months_25_plus'], 2) ?>"
                        min="0" max="1" step="0.01"
                        class="admin-form-input">
                    <span class="admin-form-hint">Äldre resultat (förfaller)</span>
                </div>
            </div>

            <button type="submit" name="save_decay" class="btn-admin btn-admin-primary">
                Spara tidsviktning
            </button>
        </form>
    </div>
</div>

<!-- Reset Defaults -->
<div class="admin-card">
    <div class="admin-card-header">
        <h3>Återställ</h3>
    </div>
    <div class="admin-card-body">
        <p class="admin-help-text">Återställ alla inställningar till standardvärden. Kör ny beräkning efteråt.</p>

        <form method="POST">
            <?= csrf_field() ?>
            <button type="submit" name="reset_defaults" class="btn-admin btn-admin-secondary"
                onclick="return confirm('Återställ alla inställningar till standardvärden?')">
                Återställ till standard
            </button>
        </form>
    </div>
</div>

<style>
/* Active events table */
.table-responsive {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin: 0 -1rem;
    padding: 0 1rem;
}

.admin-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
    min-width: 600px;
}

.admin-table th,
.admin-table td {
    padding: 0.75rem 0.5rem;
    text-align: left;
    border-bottom: 1px solid var(--admin-border, #e2e8f0);
    white-space: nowrap;
}

.admin-table th {
    font-weight: 600;
    background: var(--admin-bg-muted, #f7fafc);
    color: var(--admin-text-muted, #718096);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.admin-table tbody tr:hover {
    background: var(--admin-bg-hover, #f7fafc);
}

.admin-table .row-faded {
    background: #fffbeb;
}

.admin-table .row-faded:hover {
    background: #fef3c7;
}

.admin-link {
    color: var(--admin-primary, #0066cc);
    text-decoration: none;
}

.admin-link:hover {
    text-decoration: underline;
}

.text-muted {
    color: var(--admin-text-muted, #718096);
}

.admin-badge {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
}

.admin-badge-primary {
    background: #dbeafe;
    color: #1e40af;
}

.admin-badge-secondary {
    background: #e2e8f0;
    color: #475569;
}

.admin-badge-success {
    background: #dcfce7;
    color: #166534;
}

.admin-badge-warning {
    background: #fef3c7;
    color: #92400e;
}

@media (max-width: 768px) {
    .admin-table {
        font-size: 0.75rem;
    }

    .admin-table th,
    .admin-table td {
        padding: 0.5rem 0.4rem;
    }

    /* Hide less important columns on mobile */
    .admin-table th:nth-child(4),
    .admin-table td:nth-child(4),
    .admin-table th:nth-child(6),
    .admin-table td:nth-child(6) {
        display: none;
    }
}

.admin-stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.admin-stat-card {
    background: var(--admin-card-bg, #fff);
    border: 1px solid var(--admin-border, #e2e8f0);
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
}

.admin-stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--admin-primary, #0066cc);
}

.admin-stat-label {
    font-weight: 600;
    color: var(--admin-text, #1a202c);
    margin-bottom: 0.25rem;
}

.admin-stat-meta {
    font-size: 0.75rem;
    color: var(--admin-text-muted, #718096);
}

.admin-grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.admin-help-text {
    color: var(--admin-text-muted, #718096);
    font-size: 0.875rem;
    margin-bottom: 1rem;
}

.admin-form-hint {
    font-size: 0.75rem;
    color: var(--admin-text-muted, #718096);
    display: block;
    margin-top: 0.25rem;
}

/* Multiplier bar chart */
.multiplier-bars {
    display: flex;
    align-items: flex-end;
    gap: 4px;
    height: 100px;
    margin-bottom: 1rem;
    padding: 0 0.5rem;
}

.multiplier-bar-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.multiplier-bar {
    width: 100%;
    background: var(--admin-primary, #0066cc);
    border-radius: 2px 2px 0 0;
    transition: height 0.2s ease;
    min-height: 5px;
}

.multiplier-label {
    font-size: 0.625rem;
    color: var(--admin-text-muted, #718096);
    margin-top: 4px;
}

/* Multiplier inputs */
.multiplier-inputs {
    display: grid;
    grid-template-columns: repeat(15, 1fr);
    gap: 4px;
    margin-bottom: 1rem;
}

.multiplier-input-col {
    text-align: center;
}

.multiplier-input-col label {
    display: block;
    font-size: 0.625rem;
    color: var(--admin-text-muted, #718096);
    margin-bottom: 2px;
}

.multiplier-input-col input {
    padding: 4px 2px;
    text-align: center;
    font-size: 0.75rem;
}

/* Responsive */
@media (max-width: 768px) {
    .admin-stats-grid {
        grid-template-columns: 1fr;
    }

    .admin-grid-2 {
        grid-template-columns: 1fr;
    }

    .multiplier-inputs {
        grid-template-columns: repeat(5, 1fr);
    }

    .multiplier-bars {
        height: 60px;
    }
}
</style>

<script>
function updateBar(index, value) {
    const bar = document.getElementById('bar_' + index);
    if (bar) {
        const height = Math.max(5, parseFloat(value) * 100);
        bar.style.height = height + 'px';
    }
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
