<?php
/**
 * Elimination Display Component
 * Include this file to display elimination brackets and qualifying results
 *
 * Required variables:
 * - $db: Database connection
 * - $eventId: Event ID
 * - $selectedClassId: (optional) Class to display, defaults to first class with data
 */

if (!isset($eventId)) {
    return;
}

// Use PDO from global scope (set by config.php)
$elimPdo = $GLOBALS['pdo'] ?? null;
if (!$elimPdo) {
    return;
}

// Check if elimination tables exist
$eliminationTablesExist = false;
try {
    $elimPdo->query("SELECT 1 FROM elimination_qualifying LIMIT 1");
    $eliminationTablesExist = true;
} catch (PDOException $e) {
    $eliminationTablesExist = false;
}

if (!$eliminationTablesExist) {
    return;
}

// Get classes with elimination data
$stmt = $elimPdo->prepare("
    SELECT c.id, c.name, c.display_name,
        COUNT(DISTINCT eq.id) as qual_count,
        COUNT(DISTINCT eb.id) as bracket_count
    FROM classes c
    LEFT JOIN elimination_qualifying eq ON c.id = eq.class_id AND eq.event_id = ?
    LEFT JOIN elimination_brackets eb ON c.id = eb.class_id AND eb.event_id = ?
    WHERE eq.id IS NOT NULL OR eb.id IS NOT NULL
    GROUP BY c.id, c.name, c.display_name, c.sort_order
    ORDER BY c.sort_order, c.name
");
$stmt->execute([$eventId, $eventId]);
$eliminationClasses = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (empty($eliminationClasses)) {
    return;
}

// Get selected class (from URL or default to first)
$elimClassId = isset($_GET['elim_class']) ? intval($_GET['elim_class']) : $eliminationClasses[0]['id'];

// Get qualifying results
$stmt = $elimPdo->prepare("
    SELECT eq.*, r.firstname, r.lastname, cl.name as club_name
    FROM elimination_qualifying eq
    JOIN riders r ON eq.rider_id = r.id
    LEFT JOIN clubs cl ON r.club_id = cl.id
    WHERE eq.event_id = ? AND eq.class_id = ?
    ORDER BY eq.seed_position ASC, eq.best_time ASC
");
$stmt->execute([$eventId, $elimClassId]);
$qualifyingResults = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Get bracket data grouped by round
$stmt = $elimPdo->prepare("
    SELECT eb.*,
        r1.firstname as rider1_firstname, r1.lastname as rider1_lastname,
        cl1.name as rider1_club,
        r2.firstname as rider2_firstname, r2.lastname as rider2_lastname,
        cl2.name as rider2_club,
        w.firstname as winner_firstname, w.lastname as winner_lastname
    FROM elimination_brackets eb
    LEFT JOIN riders r1 ON eb.rider_1_id = r1.id
    LEFT JOIN clubs cl1 ON r1.club_id = cl1.id
    LEFT JOIN riders r2 ON eb.rider_2_id = r2.id
    LEFT JOIN clubs cl2 ON r2.club_id = cl2.id
    LEFT JOIN riders w ON eb.winner_id = w.id
    WHERE eb.event_id = ? AND eb.class_id = ?
    ORDER BY eb.round_number ASC, eb.heat_number ASC
");
$stmt->execute([$eventId, $elimClassId]);
$bracketsRaw = $stmt->fetchAll(PDO::FETCH_ASSOC);

$brackets = [];
foreach ($bracketsRaw as $b) {
    $brackets[$b['round_name']][] = $b;
}

// Get final results
$stmt = $elimPdo->prepare("
    SELECT er.*, r.firstname, r.lastname, cl.name as club_name
    FROM elimination_results er
    JOIN riders r ON er.rider_id = r.id
    LEFT JOIN clubs cl ON r.club_id = cl.id
    WHERE er.event_id = ? AND er.class_id = ?
    ORDER BY er.final_position ASC
");
$stmt->execute([$eventId, $elimClassId]);
$finalResults = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Round name translations
$roundNames = [
    'round_of_32' => '32-delsfinal',
    'round_of_16' => '16-delsfinal',
    'quarterfinal' => 'Kvartsfinal',
    'semifinal' => 'Semifinal',
    'third_place' => 'Match om 3:e plats',
    'final' => 'Final',
    'b_semifinal' => 'B-Semifinal',
    'b_final' => 'B-Final',
];
?>

<div class="elimination-display">
    <!-- Class Selector -->
    <?php if (count($eliminationClasses) > 1): ?>
    <div class="class-selector mb-lg">
        <div class="class-tabs">
            <?php foreach ($eliminationClasses as $ec): ?>
                <a href="?id=<?= $eventId ?>&tab=elimination&elim_class=<?= $ec['id'] ?>"
                   class="class-tab <?= $elimClassId == $ec['id'] ? 'active' : '' ?>">
                    <?= h($ec['display_name'] ?? $ec['name']) ?>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
    <?php endif; ?>

    <!-- Sub-tabs: Kval | Bracket | Resultat -->
    <div class="elim-subtabs mb-lg">
        <button class="elim-subtab active" data-target="elim-qualifying">
            <i data-lucide="timer"></i> Kvalificering
        </button>
        <button class="elim-subtab" data-target="elim-bracket">
            <i data-lucide="git-branch"></i> Bracket
        </button>
        <?php if (!empty($finalResults)): ?>
        <button class="elim-subtab" data-target="elim-results">
            <i data-lucide="trophy"></i> Resultat
        </button>
        <?php endif; ?>
    </div>

    <!-- QUALIFYING SECTION -->
    <div class="elim-section" id="elim-qualifying">
        <?php if (empty($qualifyingResults)): ?>
            <div class="empty-state">
                <i data-lucide="timer"></i>
                <p>Inga kvalresultat tillgängliga.</p>
            </div>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table elimination-table">
                    <thead>
                        <tr>
                            <th class="col-pos">Seed</th>
                            <th class="col-bib">Nr</th>
                            <th class="col-name">Namn</th>
                            <th class="col-club">Klubb</th>
                            <th class="col-time text-right">Åk 1</th>
                            <th class="col-time text-right">Åk 2</th>
                            <th class="col-time text-right">Bäst</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($qualifyingResults as $idx => $qr): ?>
                            <tr class="<?= $qr['advances_to_bracket'] ? 'advances' : '' ?>">
                                <td class="col-pos">
                                    <span class="seed-badge"><?= $qr['seed_position'] ?? ($idx + 1) ?></span>
                                </td>
                                <td class="col-bib"><?= h($qr['bib_number'] ?? '-') ?></td>
                                <td class="col-name">
                                    <a href="/rider/<?= $qr['rider_id'] ?>" class="rider-link">
                                        <?= h($qr['firstname'] . ' ' . $qr['lastname']) ?>
                                    </a>
                                </td>
                                <td class="col-club"><?= h($qr['club_name'] ?? '-') ?></td>
                                <td class="col-time text-right"><?= $qr['run_1_time'] ? number_format($qr['run_1_time'], 3) : '-' ?></td>
                                <td class="col-time text-right"><?= $qr['run_2_time'] ? number_format($qr['run_2_time'], 3) : '-' ?></td>
                                <td class="col-time text-right best-time"><?= $qr['best_time'] ? number_format($qr['best_time'], 3) : '-' ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>

    <!-- BRACKET SECTION -->
    <div class="elim-section hidden" id="elim-bracket">
        <?php if (empty($brackets)): ?>
            <div class="empty-state">
                <i data-lucide="git-branch"></i>
                <p>Bracket har inte genererats än.</p>
            </div>
        <?php else: ?>
            <?php
            // Determine bracket structure
            $roundOrder = ['round_of_32', 'round_of_16', 'quarterfinal', 'semifinal', 'final'];
            $orderedBrackets = [];
            foreach ($roundOrder as $r) {
                if (isset($brackets[$r])) {
                    $orderedBrackets[$r] = $brackets[$r];
                }
            }
            $numRounds = count($orderedBrackets);
            $roundKeys = array_keys($orderedBrackets);
            ?>
            <div class="bracket-visual" data-rounds="<?= $numRounds ?>">
                <?php foreach ($orderedBrackets as $roundName => $heats): ?>
                    <?php $roundIndex = array_search($roundName, $roundKeys); ?>
                    <div class="bracket-round" data-round="<?= $roundIndex ?>">
                        <div class="round-header"><?= $roundNames[$roundName] ?? ucfirst(str_replace('_', ' ', $roundName)) ?></div>
                        <div class="round-matches">
                            <?php foreach ($heats as $heat): ?>
                                <div class="bracket-match <?= $heat['status'] ?>">
                                    <div class="match-slot <?= $heat['winner_id'] == $heat['rider_1_id'] ? 'winner' : '' ?>">
                                        <span class="slot-seed"><?= $heat['rider_1_seed'] ?: '-' ?></span>
                                        <span class="slot-name">
                                            <?php if ($heat['rider_1_id']): ?>
                                                <?= h($heat['rider1_firstname'] . ' ' . $heat['rider1_lastname']) ?>
                                            <?php else: ?>
                                                BYE
                                            <?php endif; ?>
                                        </span>
                                        <span class="slot-time"><?= $heat['rider_1_total'] ? number_format($heat['rider_1_total'], 3) : '' ?></span>
                                    </div>
                                    <div class="match-slot <?= $heat['winner_id'] == $heat['rider_2_id'] ? 'winner' : '' ?>">
                                        <span class="slot-seed"><?= $heat['rider_2_seed'] ?: '-' ?></span>
                                        <span class="slot-name">
                                            <?php if ($heat['rider_2_id']): ?>
                                                <?= h($heat['rider2_firstname'] . ' ' . $heat['rider2_lastname']) ?>
                                            <?php else: ?>
                                                BYE
                                            <?php endif; ?>
                                        </span>
                                        <span class="slot-time"><?= $heat['rider_2_total'] ? number_format($heat['rider_2_total'], 3) : '' ?></span>
                                    </div>
                                    <div class="match-connector"></div>
                                </div>
                            <?php endforeach; ?>
                        </div>
                    </div>
                <?php endforeach; ?>

                <!-- Winner slot -->
                <div class="bracket-round winner-round">
                    <div class="round-header">Vinnare</div>
                    <div class="round-matches">
                        <div class="bracket-match final-winner">
                            <div class="match-slot winner">
                                <span class="slot-seed"></span>
                                <span class="slot-name">
                                    <?php
                                    $finalHeat = end($orderedBrackets['final'] ?? []);
                                    if ($finalHeat && $finalHeat['winner_id']):
                                        echo h($finalHeat['winner_firstname'] . ' ' . $finalHeat['winner_lastname']);
                                    else:
                                        echo '-';
                                    endif;
                                    ?>
                                </span>
                                <span class="slot-time"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <?php endif; ?>
    </div>

    <!-- FINAL RESULTS SECTION -->
    <?php if (!empty($finalResults)): ?>
    <div class="elim-section hidden" id="elim-results">
        <div class="table-responsive">
            <table class="table elimination-table">
                <thead>
                    <tr>
                        <th class="col-pos">Plac</th>
                        <th class="col-name">Namn</th>
                        <th class="col-club">Klubb</th>
                        <th class="col-seed">Seed</th>
                        <th class="col-bracket text-center">Bracket</th>
                        <th class="col-points text-right">Poäng</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($finalResults as $result): ?>
                        <tr>
                            <td class="col-pos">
                                <?php if ($result['final_position'] <= 3): ?>
                                    <span class="position-medal position-<?= $result['final_position'] ?>"><?= $result['final_position'] ?></span>
                                <?php else: ?>
                                    <?= $result['final_position'] ?>
                                <?php endif; ?>
                            </td>
                            <td class="col-name">
                                <a href="/rider/<?= $result['rider_id'] ?>" class="rider-link">
                                    <?= h($result['firstname'] . ' ' . $result['lastname']) ?>
                                </a>
                            </td>
                            <td class="col-club"><?= h($result['club_name'] ?? '-') ?></td>
                            <td class="col-seed"><?= $result['qualifying_position'] ?? '-' ?></td>
                            <td class="col-bracket text-center">
                                <?php if ($result['bracket_type'] === 'consolation'): ?>
                                    <span class="badge badge-secondary">B</span>
                                <?php else: ?>
                                    <span class="badge badge-success">A</span>
                                <?php endif; ?>
                            </td>
                            <td class="col-points text-right"><?= $result['points'] ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
    <?php endif; ?>
</div>

<style>
/* Elimination Display Styles */
.elimination-display {
    margin-bottom: var(--space-lg);
}

.class-tabs {
    display: flex;
    gap: var(--space-xs);
    flex-wrap: wrap;
}

.class-tab {
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-secondary);
    border-radius: var(--radius-md);
    text-decoration: none;
    color: var(--color-text);
    font-size: var(--text-sm);
    transition: all 0.2s;
}

.class-tab:hover {
    background: var(--color-border);
}

.class-tab.active {
    background: var(--color-accent);
    color: white;
}

/* Sub-tabs */
.elim-subtabs {
    display: flex;
    gap: var(--space-xs);
    border-bottom: 2px solid var(--color-border);
    padding-bottom: var(--space-xs);
}

.elim-subtab {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    border: none;
    background: none;
    cursor: pointer;
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
}

.elim-subtab:hover {
    color: var(--color-text);
}

.elim-subtab.active {
    color: var(--color-accent);
    border-bottom-color: var(--color-accent);
}

.elim-subtab i {
    width: 16px;
    height: 16px;
}

.elim-section {
    padding-top: var(--space-md);
}

.elim-section.hidden {
    display: none;
}

/* Qualifying Table */
.elimination-table {
    width: 100%;
}

.elimination-table .col-pos { width: 50px; text-align: center; }
.elimination-table .col-bib { width: 50px; }
.elimination-table .col-time { width: 80px; }
.elimination-table .col-seed { width: 50px; }
.elimination-table .col-bracket { width: 60px; }
.elimination-table .col-points { width: 60px; }

.seed-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: var(--color-bg-secondary);
    border-radius: 50%;
    font-weight: 600;
    font-size: var(--text-sm);
}

tr.advances {
    background: rgba(97, 206, 112, 0.1);
}

tr.advances .seed-badge {
    background: var(--color-accent);
    color: white;
}

.best-time {
    font-weight: 600;
}

/* Visual Bracket Styles - Tournament Tree */
.bracket-visual {
    display: flex;
    gap: 0;
    overflow-x: auto;
    padding: var(--space-lg) var(--space-md);
    min-height: 400px;
}

.bracket-visual .bracket-round {
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    min-width: 180px;
}

.bracket-visual .round-header {
    text-align: center;
    font-size: var(--text-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--color-text-secondary);
    padding: var(--space-sm);
    background: var(--color-bg-secondary);
    border-bottom: 1px solid var(--color-border);
}

.bracket-visual .round-matches {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: var(--space-sm) 0;
}

.bracket-visual .bracket-match {
    position: relative;
    margin: var(--space-xs) 0;
}

.bracket-visual .match-slot {
    display: flex;
    align-items: center;
    background: white;
    border: 1px solid var(--color-border);
    padding: 6px 10px;
    font-size: var(--text-sm);
    min-height: 32px;
}

.bracket-visual .match-slot:first-child {
    border-bottom: none;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

.bracket-visual .match-slot:last-of-type {
    border-radius: 0 0 var(--radius-sm) var(--radius-sm);
}

.bracket-visual .match-slot.winner {
    background: var(--color-accent);
    color: white;
    border-color: var(--color-accent);
}

.bracket-visual .match-slot.bye-slot {
    background: var(--color-bg-secondary);
    color: var(--color-text-secondary);
    font-style: italic;
}

.bracket-visual .slot-seed {
    font-weight: 600;
    min-width: 20px;
    color: var(--color-text-secondary);
    font-size: var(--text-xs);
}

.bracket-visual .match-slot.winner .slot-seed {
    color: rgba(255,255,255,0.8);
}

.bracket-visual .slot-name {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: var(--space-xs);
}

.bracket-visual .slot-time {
    font-size: var(--text-xs);
    font-weight: 500;
    min-width: 45px;
    text-align: right;
}

/* Connector lines */
.bracket-visual .match-connector {
    position: absolute;
    right: -20px;
    top: 50%;
    width: 20px;
    height: 1px;
    background: var(--color-border);
}

.bracket-visual .match-connector::after {
    content: '';
    position: absolute;
    right: 0;
    width: 1px;
    background: var(--color-border);
}

/* Adjust connector heights based on round */
.bracket-visual .bracket-round[data-round="0"] .bracket-match:nth-child(odd) .match-connector::after {
    top: 0;
    height: calc(50% + var(--space-xs) + 14px);
}

.bracket-visual .bracket-round[data-round="0"] .bracket-match:nth-child(even) .match-connector::after {
    bottom: 0;
    height: calc(50% + var(--space-xs) + 14px);
}

.bracket-visual .bracket-round[data-round="1"] .bracket-match:nth-child(odd) .match-connector::after {
    top: 0;
    height: calc(100% + var(--space-md));
}

.bracket-visual .bracket-round[data-round="1"] .bracket-match:nth-child(even) .match-connector::after {
    bottom: 0;
    height: calc(100% + var(--space-md));
}

/* Winner round */
.bracket-visual .winner-round {
    min-width: 150px;
}

.bracket-visual .winner-round .match-slot {
    border: 2px solid var(--color-accent);
    background: rgba(97, 206, 112, 0.1);
    font-weight: 600;
}

.bracket-visual .final-winner .match-connector {
    display: none;
}

/* BYE styling */
.bracket-visual .bracket-match.bye .match-slot:last-child {
    color: var(--color-text-secondary);
    font-style: italic;
}

/* Responsive - stack on mobile */
@media (max-width: 767px) {
    .bracket-visual {
        flex-direction: column;
        gap: var(--space-lg);
        min-height: auto;
    }

    .bracket-visual .bracket-round {
        min-width: 100%;
    }

    .bracket-visual .match-connector {
        display: none;
    }

    .bracket-visual .round-matches {
        gap: var(--space-sm);
    }
}

/* Position medals */
.position-medal {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-weight: 600;
    color: white;
}

.position-1 { background: linear-gradient(135deg, #FFD700, #FFA500); color: #333; }
.position-2 { background: linear-gradient(135deg, #C0C0C0, #A0A0A0); color: #333; }
.position-3 { background: linear-gradient(135deg, #CD7F32, #A0522D); }

/* Responsive */
@media (max-width: 767px) {
    .bracket-container {
        flex-direction: column;
    }

    .bracket-round {
        min-width: 100%;
    }

    .elim-subtabs {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}
</style>

<script>
// Tab switching for elimination display - wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.elim-subtab').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.dataset.target;
            if (!targetId) return;

            // Update buttons
            document.querySelectorAll('.elim-subtab').forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            // Update sections
            document.querySelectorAll('.elim-section').forEach(s => s.classList.add('hidden'));
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.remove('hidden');
            }
        });
    });

    // Re-initialize Lucide icons if available
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

// Fallback: also run immediately in case DOM is already loaded
if (document.readyState !== 'loading') {
    document.querySelectorAll('.elim-subtab').forEach(btn => {
        if (!btn.hasAttribute('data-click-bound')) {
            btn.setAttribute('data-click-bound', 'true');
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.dataset.target;
                if (!targetId) return;

                document.querySelectorAll('.elim-subtab').forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                document.querySelectorAll('.elim-section').forEach(s => s.classList.add('hidden'));
                const targetSection = document.getElementById(targetId);
                if (targetSection) {
                    targetSection.classList.remove('hidden');
                }
            });
        }
    });
}
</script>
