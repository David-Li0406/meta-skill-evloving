<?php
/**
 * Admin Elimination Live Entry
 * Streamlined interface for entering results during an event
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;
$db = getDB();

$eventId = isset($_GET['event_id']) ? intval($_GET['event_id']) : 0;
if (!$eventId) {
    header('Location: /admin/elimination.php');
    exit;
}

// Get event info
$event = $db->getRow("SELECT e.*, s.name as series_name FROM events e LEFT JOIN series s ON e.series_id = s.id WHERE e.id = ?", [$eventId]);
if (!$event) {
    $_SESSION['error'] = 'Event hittades inte';
    header('Location: /admin/elimination.php');
    exit;
}

// Check if elimination tables exist
$tablesExist = true;
try {
    $pdo->query("SELECT 1 FROM elimination_qualifying LIMIT 1");
} catch (Exception $e) {
    $tablesExist = false;
}

// Get classes
$classes = $db->getAll("
    SELECT DISTINCT c.id, c.name, c.display_name
    FROM classes c
    WHERE c.active = 1
    ORDER BY c.sort_order, c.name
");

$selectedClassId = isset($_GET['class_id']) ? intval($_GET['class_id']) : ($classes[0]['id'] ?? 0);
$mode = $_GET['mode'] ?? 'qualifying'; // qualifying or bracket

// Get riders for autocomplete (those registered or with previous results)
$riders = $db->getAll("
    SELECT DISTINCT r.id, r.firstname, r.lastname, c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE r.active = 1
    ORDER BY r.lastname, r.firstname
    LIMIT 500
");

// Handle AJAX requests
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['ajax'])) {
    header('Content-Type: application/json');

    $action = $_POST['action'] ?? '';

    if ($action === 'save_qualifying') {
        $riderId = intval($_POST['rider_id'] ?? 0);
        $classId = intval($_POST['class_id'] ?? 0);
        // Handle both comma and dot as decimal separator
        $run1 = $_POST['run1'] !== '' ? floatval(str_replace(',', '.', $_POST['run1'])) : null;
        $run2 = $_POST['run2'] !== '' ? floatval(str_replace(',', '.', $_POST['run2'])) : null;
        $status = $_POST['status'] ?? 'finished';

        if (!$riderId || !$classId) {
            echo json_encode(['success' => false, 'error' => 'Åkare och klass krävs']);
            exit;
        }

        try {
            // Calculate best time
            $bestTime = null;
            if ($run1 !== null && $run2 !== null) {
                $bestTime = min($run1, $run2);
            } elseif ($run1 !== null) {
                $bestTime = $run1;
            } elseif ($run2 !== null) {
                $bestTime = $run2;
            }

            // Check if entry exists
            $existing = $db->getRow("SELECT id FROM elimination_qualifying WHERE event_id = ? AND class_id = ? AND rider_id = ?",
                [$eventId, $classId, $riderId]);

            if ($existing) {
                $stmt = $pdo->prepare("
                    UPDATE elimination_qualifying
                    SET run_1_time = ?, run_2_time = ?, best_time = ?, status = ?, updated_at = NOW()
                    WHERE id = ?
                ");
                $stmt->execute([$run1, $run2, $bestTime, $status, $existing['id']]);
            } else {
                $stmt = $pdo->prepare("
                    INSERT INTO elimination_qualifying
                    (event_id, class_id, rider_id, run_1_time, run_2_time, best_time, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ");
                $stmt->execute([$eventId, $classId, $riderId, $run1, $run2, $bestTime, $status]);
            }

            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        exit;
    }

    if ($action === 'save_heat') {
        $heatId = intval($_POST['heat_id'] ?? 0);
        // Handle both comma and dot as decimal separator
        $rider1Run1 = $_POST['rider1_run1'] !== '' ? floatval(str_replace(',', '.', $_POST['rider1_run1'])) : null;
        $rider1Run2 = $_POST['rider1_run2'] !== '' ? floatval(str_replace(',', '.', $_POST['rider1_run2'])) : null;
        $rider2Run1 = $_POST['rider2_run1'] !== '' ? floatval(str_replace(',', '.', $_POST['rider2_run1'])) : null;
        $rider2Run2 = $_POST['rider2_run2'] !== '' ? floatval(str_replace(',', '.', $_POST['rider2_run2'])) : null;

        if (!$heatId) {
            echo json_encode(['success' => false, 'error' => 'Heat-ID saknas']);
            exit;
        }

        try {
            $heat = $db->getRow("SELECT * FROM elimination_brackets WHERE id = ?", [$heatId]);
            if (!$heat) {
                echo json_encode(['success' => false, 'error' => 'Heat hittades inte']);
                exit;
            }

            $rider1Total = ($rider1Run1 ?? 0) + ($rider1Run2 ?? 0);
            $rider2Total = ($rider2Run1 ?? 0) + ($rider2Run2 ?? 0);

            $winnerId = null;
            $loserId = null;
            $status = 'in_progress';

            // Determine winner if both have times
            if ($rider1Total > 0 && $rider2Total > 0) {
                $status = 'completed';
                if ($rider1Total < $rider2Total) {
                    $winnerId = $heat['rider_1_id'];
                    $loserId = $heat['rider_2_id'];
                } else {
                    $winnerId = $heat['rider_2_id'];
                    $loserId = $heat['rider_1_id'];
                }
            }

            $stmt = $pdo->prepare("
                UPDATE elimination_brackets SET
                    rider_1_run1 = ?, rider_1_run2 = ?, rider_1_total = ?,
                    rider_2_run1 = ?, rider_2_run2 = ?, rider_2_total = ?,
                    winner_id = ?, loser_id = ?, status = ?
                WHERE id = ?
            ");
            $stmt->execute([
                $rider1Run1, $rider1Run2, $rider1Total > 0 ? $rider1Total : null,
                $rider2Run1, $rider2Run2, $rider2Total > 0 ? $rider2Total : null,
                $winnerId, $loserId, $status, $heatId
            ]);

            echo json_encode(['success' => true, 'winner_id' => $winnerId]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        exit;
    }

    if ($action === 'get_qualifying_list') {
        $classId = intval($_POST['class_id'] ?? 0);
        $results = $db->getAll("
            SELECT eq.*, r.firstname, r.lastname, c.name as club_name
            FROM elimination_qualifying eq
            JOIN riders r ON eq.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE eq.event_id = ? AND eq.class_id = ?
            ORDER BY eq.best_time ASC
        ", [$eventId, $classId]);
        echo json_encode(['success' => true, 'results' => $results]);
        exit;
    }

    if ($action === 'get_brackets') {
        $classId = intval($_POST['class_id'] ?? 0);
        $brackets = $db->getAll("
            SELECT eb.*,
                r1.firstname as rider1_firstname, r1.lastname as rider1_lastname,
                r2.firstname as rider2_firstname, r2.lastname as rider2_lastname
            FROM elimination_brackets eb
            LEFT JOIN riders r1 ON eb.rider_1_id = r1.id
            LEFT JOIN riders r2 ON eb.rider_2_id = r2.id
            WHERE eb.event_id = ? AND eb.class_id = ?
            ORDER BY eb.round_number ASC, eb.heat_number ASC
        ", [$eventId, $classId]);
        echo json_encode(['success' => true, 'brackets' => $brackets]);
        exit;
    }

    echo json_encode(['success' => false, 'error' => 'Okänd action']);
    exit;
}

// Page config
$page_title = 'Live Resultat - ' . $event['name'];
$breadcrumbs = [
    ['label' => 'Tävlingar', 'url' => '/admin/events.php'],
    ['label' => 'Elimination', 'url' => '/admin/elimination.php'],
    ['label' => $event['name'], 'url' => '/admin/elimination-manage.php?event_id=' . $eventId],
    ['label' => 'Live Entry']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if (!$tablesExist): ?>
    <div class="admin-card">
        <div class="admin-card-body">
            <div class="alert alert-warning">
                <i data-lucide="database"></i>
                <strong>Databastabeller saknas!</strong>
                <p>Kör migrationen först.</p>
                <a href="/admin/run-migrations.php" class="btn-admin btn-admin-primary mt-md">Kör Migrationer</a>
            </div>
        </div>
    </div>
<?php else: ?>

<div class="live-entry-container">
    <!-- Header with event info and mode switcher -->
    <div class="admin-card mb-md">
        <div class="admin-card-body">
            <div class="flex items-center justify-between flex-wrap gap-md">
                <div>
                    <h2 style="margin: 0; display: flex; align-items: center; gap: var(--space-sm);">
                        <span class="live-indicator"></span>
                        <?= h($event['name']) ?>
                    </h2>
                    <p style="margin: var(--space-xs) 0 0; color: var(--color-text-secondary);">
                        <?= date('Y-m-d', strtotime($event['date'])) ?>
                    </p>
                </div>
                <div class="flex gap-sm flex-wrap">
                    <select id="class-select" class="admin-form-select" style="min-width: 150px;">
                        <?php foreach ($classes as $class): ?>
                            <option value="<?= $class['id'] ?>" <?= $selectedClassId == $class['id'] ? 'selected' : '' ?>>
                                <?= h($class['display_name'] ?? $class['name']) ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                    <div class="btn-group">
                        <button type="button" class="btn-admin btn-admin-<?= $mode === 'qualifying' ? 'primary' : 'secondary' ?>" id="mode-qualifying">
                            <i data-lucide="timer"></i> Kval
                        </button>
                        <button type="button" class="btn-admin btn-admin-<?= $mode === 'bracket' ? 'primary' : 'secondary' ?>" id="mode-bracket">
                            <i data-lucide="git-branch"></i> Bracket
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- QUALIFYING MODE -->
    <div id="qualifying-mode" class="<?= $mode !== 'qualifying' ? 'hidden' : '' ?>">
        <!-- Quick Entry Form -->
        <div class="admin-card mb-md">
            <div class="admin-card-header">
                <h3><i data-lucide="plus-circle"></i> Lägg till kvalresultat</h3>
            </div>
            <div class="admin-card-body">
                <form id="qualifying-form" class="live-entry-form">
                    <div class="form-row">
                        <div class="form-group flex-2">
                            <label class="admin-form-label">Åkare</label>
                            <select id="rider-select" class="admin-form-select" required>
                                <option value="">Välj åkare...</option>
                                <?php foreach ($riders as $rider): ?>
                                    <option value="<?= $rider['id'] ?>" data-name="<?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>">
                                        <?= h($rider['lastname'] . ', ' . $rider['firstname']) ?>
                                        <?php if ($rider['club_name']): ?> (<?= h($rider['club_name']) ?>)<?php endif; ?>
                                    </option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="admin-form-label">Run 1</label>
                            <input type="text" id="run1-input" class="admin-form-input time-input" placeholder="00:00.000" pattern="[\d:.]+">
                        </div>
                        <div class="form-group">
                            <label class="admin-form-label">Run 2</label>
                            <input type="text" id="run2-input" class="admin-form-input time-input" placeholder="00:00.000" pattern="[\d:.]+">
                        </div>
                        <div class="form-group">
                            <label class="admin-form-label">Status</label>
                            <select id="status-select" class="admin-form-select">
                                <option value="finished">Finished</option>
                                <option value="dnf">DNF</option>
                                <option value="dns">DNS</option>
                                <option value="dq">DQ</option>
                            </select>
                        </div>
                        <div class="form-group form-group-btn">
                            <button type="submit" class="btn-admin btn-admin-primary">
                                <i data-lucide="save"></i> Spara
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <!-- Current Results List -->
        <div class="admin-card">
            <div class="admin-card-header">
                <h3><i data-lucide="list-ordered"></i> Kvalresultat</h3>
                <div class="flex gap-sm">
                    <button type="button" class="btn-admin btn-admin-secondary btn-admin-sm" id="refresh-qualifying">
                        <i data-lucide="refresh-cw"></i> Uppdatera
                    </button>
                    <a href="/admin/elimination-import-qualifying.php?event_id=<?= $eventId ?>&class_id=<?= $selectedClassId ?>" class="btn-admin btn-admin-secondary btn-admin-sm">
                        <i data-lucide="upload"></i> Importera CSV
                    </a>
                </div>
            </div>
            <div class="admin-card-body" style="padding: 0;">
                <div id="qualifying-list" class="admin-table-container">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th style="width: 50px;">#</th>
                                <th>Åkare</th>
                                <th>Klubb</th>
                                <th class="text-right">Run 1</th>
                                <th class="text-right">Run 2</th>
                                <th class="text-right">Bästa</th>
                                <th style="width: 80px;">Status</th>
                            </tr>
                        </thead>
                        <tbody id="qualifying-tbody">
                            <tr><td colspan="7" class="text-center" style="padding: var(--space-lg);">Laddar...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- BRACKET MODE -->
    <div id="bracket-mode" class="<?= $mode !== 'bracket' ? 'hidden' : '' ?>">
        <div class="admin-card">
            <div class="admin-card-header">
                <h3><i data-lucide="git-branch"></i> Bracket Heats</h3>
                <button type="button" class="btn-admin btn-admin-secondary btn-admin-sm" id="refresh-brackets">
                    <i data-lucide="refresh-cw"></i> Uppdatera
                </button>
            </div>
            <div class="admin-card-body">
                <div id="brackets-container">
                    <p class="text-center" style="padding: var(--space-lg); color: var(--color-text-secondary);">
                        Laddar brackets...
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.live-entry-container {
    max-width: 1200px;
}

.live-indicator {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: #ef4444;
    border-radius: 50%;
    animation: pulse-live 2s infinite;
}

@keyframes pulse-live {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
    50% { opacity: 0.8; box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
}

.live-entry-form .form-row {
    display: flex;
    gap: var(--space-md);
    align-items: flex-end;
    flex-wrap: wrap;
}

.live-entry-form .form-group {
    flex: 1;
    min-width: 100px;
}

.live-entry-form .form-group.flex-2 {
    flex: 2;
    min-width: 200px;
}

.live-entry-form .form-group-btn {
    flex: 0 0 auto;
}

.time-input {
    font-family: 'JetBrains Mono', monospace;
    text-align: right;
}

.btn-group {
    display: flex;
}

.btn-group .btn-admin:first-child {
    border-radius: var(--radius-md) 0 0 var(--radius-md);
}

.btn-group .btn-admin:last-child {
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    margin-left: -1px;
}

.hidden {
    display: none !important;
}

/* Bracket Heat Cards */
.heat-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-md);
}

.heat-card.completed {
    border-color: var(--color-success);
    background: rgba(97, 206, 112, 0.05);
}

.heat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-sm);
    padding-bottom: var(--space-sm);
    border-bottom: 1px solid var(--color-border);
}

.heat-title {
    font-weight: 600;
    color: var(--color-text-primary);
}

.heat-status {
    font-size: var(--text-xs);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    background: var(--color-bg-hover);
}

.heat-status.completed {
    background: var(--color-success);
    color: white;
}

.heat-riders {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: var(--space-md);
    align-items: center;
}

.heat-rider {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.heat-rider-name {
    font-weight: 500;
    font-size: var(--text-sm);
}

.heat-rider-seed {
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
}

.heat-rider.winner .heat-rider-name {
    color: var(--color-success);
}

.heat-times {
    display: flex;
    gap: var(--space-xs);
}

.heat-times input {
    width: 80px;
    font-family: 'JetBrains Mono', monospace;
    text-align: right;
    font-size: var(--text-sm);
    padding: var(--space-xs) var(--space-sm);
}

.heat-vs {
    font-weight: 700;
    color: var(--color-text-secondary);
    font-size: var(--text-lg);
}

.heat-total {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: var(--text-sm);
    margin-top: var(--space-xs);
}

.heat-total.winner {
    color: var(--color-success);
}

.round-section {
    margin-bottom: var(--space-xl);
}

.round-title {
    font-size: var(--text-lg);
    font-weight: 600;
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 2px solid var(--color-accent);
}

@media (max-width: 768px) {
    .live-entry-form .form-row {
        flex-direction: column;
    }

    .live-entry-form .form-group {
        width: 100%;
    }

    .heat-riders {
        grid-template-columns: 1fr;
        gap: var(--space-sm);
    }

    .heat-vs {
        text-align: center;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const eventId = <?= $eventId ?>;
    let currentClassId = <?= $selectedClassId ?>;
    let currentMode = '<?= $mode ?>';

    const classSelect = document.getElementById('class-select');
    const modeQualifying = document.getElementById('mode-qualifying');
    const modeBracket = document.getElementById('mode-bracket');
    const qualifyingMode = document.getElementById('qualifying-mode');
    const bracketMode = document.getElementById('bracket-mode');
    const qualifyingForm = document.getElementById('qualifying-form');

    // Format time for display
    function formatTime(seconds) {
        if (!seconds) return '-';
        const mins = Math.floor(seconds / 60);
        const secs = (seconds % 60).toFixed(3);
        return mins > 0 ? `${mins}:${secs.padStart(6, '0')}` : secs;
    }

    // Parse time input to seconds
    function parseTime(input) {
        if (!input || input.trim() === '') return null;
        const parts = input.split(':');
        if (parts.length === 2) {
            return parseFloat(parts[0]) * 60 + parseFloat(parts[1]);
        }
        return parseFloat(input);
    }

    // Switch modes
    function switchMode(mode) {
        currentMode = mode;
        if (mode === 'qualifying') {
            qualifyingMode.classList.remove('hidden');
            bracketMode.classList.add('hidden');
            modeQualifying.classList.add('btn-admin-primary');
            modeQualifying.classList.remove('btn-admin-secondary');
            modeBracket.classList.remove('btn-admin-primary');
            modeBracket.classList.add('btn-admin-secondary');
            loadQualifying();
        } else {
            qualifyingMode.classList.add('hidden');
            bracketMode.classList.remove('hidden');
            modeBracket.classList.add('btn-admin-primary');
            modeBracket.classList.remove('btn-admin-secondary');
            modeQualifying.classList.remove('btn-admin-primary');
            modeQualifying.classList.add('btn-admin-secondary');
            loadBrackets();
        }
    }

    modeQualifying.addEventListener('click', () => switchMode('qualifying'));
    modeBracket.addEventListener('click', () => switchMode('bracket'));

    classSelect.addEventListener('change', function() {
        currentClassId = parseInt(this.value);
        if (currentMode === 'qualifying') {
            loadQualifying();
        } else {
            loadBrackets();
        }
    });

    // Load qualifying results
    async function loadQualifying() {
        const tbody = document.getElementById('qualifying-tbody');
        tbody.innerHTML = '<tr><td colspan="7" class="text-center" style="padding: var(--space-lg);">Laddar...</td></tr>';

        try {
            const response = await fetch('', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `ajax=1&action=get_qualifying_list&class_id=${currentClassId}`
            });
            const data = await response.json();

            if (data.success && data.results.length > 0) {
                tbody.innerHTML = data.results.map((r, i) => `
                    <tr>
                        <td><strong>${i + 1}</strong></td>
                        <td><strong>${r.firstname} ${r.lastname}</strong></td>
                        <td>${r.club_name || '-'}</td>
                        <td class="text-right font-mono">${formatTime(r.run_1_time)}</td>
                        <td class="text-right font-mono">${formatTime(r.run_2_time)}</td>
                        <td class="text-right font-mono" style="font-weight: 600; color: var(--color-success);">${formatTime(r.best_time)}</td>
                        <td><span class="admin-badge admin-badge-${r.status === 'finished' ? 'success' : 'warning'}">${r.status.toUpperCase()}</span></td>
                    </tr>
                `).join('');
            } else {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center" style="padding: var(--space-lg); color: var(--color-text-secondary);">Inga kvalresultat ännu</td></tr>';
            }
        } catch (e) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center" style="padding: var(--space-lg); color: var(--color-danger);">Fel vid laddning</td></tr>';
        }
    }

    // Load brackets
    async function loadBrackets() {
        const container = document.getElementById('brackets-container');
        container.innerHTML = '<p class="text-center" style="padding: var(--space-lg);">Laddar...</p>';

        try {
            const response = await fetch('', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `ajax=1&action=get_brackets&class_id=${currentClassId}`
            });
            const data = await response.json();

            if (data.success && data.brackets.length > 0) {
                // Group by round
                const rounds = {};
                data.brackets.forEach(b => {
                    if (!rounds[b.round_name]) rounds[b.round_name] = [];
                    rounds[b.round_name].push(b);
                });

                const roundNames = {
                    'round_of_32': '32-delsfinal',
                    'round_of_16': '16-delsfinal',
                    'quarterfinal': 'Kvartsfinal',
                    'semifinal': 'Semifinal',
                    'final': 'Final',
                    'consolation_final': 'B-Final'
                };

                let html = '';
                for (const [roundName, heats] of Object.entries(rounds)) {
                    html += `<div class="round-section">
                        <h4 class="round-title">${roundNames[roundName] || roundName}</h4>
                        <div class="heats-grid">`;

                    heats.forEach(heat => {
                        const isCompleted = heat.status === 'completed';
                        const r1Winner = heat.winner_id == heat.rider_1_id;
                        const r2Winner = heat.winner_id == heat.rider_2_id;

                        html += `
                        <div class="heat-card ${isCompleted ? 'completed' : ''}" data-heat-id="${heat.id}">
                            <div class="heat-header">
                                <span class="heat-title">Heat ${heat.heat_number}</span>
                                <span class="heat-status ${isCompleted ? 'completed' : ''}">${isCompleted ? 'Klar' : 'Pågår'}</span>
                            </div>
                            <div class="heat-riders">
                                <div class="heat-rider ${r1Winner ? 'winner' : ''}">
                                    <span class="heat-rider-seed">Seed #${heat.rider_1_seed || '?'}</span>
                                    <span class="heat-rider-name">${heat.rider1_firstname || '?'} ${heat.rider1_lastname || ''}</span>
                                    <div class="heat-times">
                                        <input type="text" class="admin-form-input" placeholder="Run 1" value="${heat.rider_1_run1 || ''}" data-field="rider1_run1">
                                        <input type="text" class="admin-form-input" placeholder="Run 2" value="${heat.rider_1_run2 || ''}" data-field="rider1_run2">
                                    </div>
                                    <div class="heat-total ${r1Winner ? 'winner' : ''}">${heat.rider_1_total ? formatTime(heat.rider_1_total) : '-'}</div>
                                </div>
                                <div class="heat-vs">VS</div>
                                <div class="heat-rider ${r2Winner ? 'winner' : ''}" style="text-align: right;">
                                    <span class="heat-rider-seed">Seed #${heat.rider_2_seed || '?'}</span>
                                    <span class="heat-rider-name">${heat.rider2_firstname || '?'} ${heat.rider2_lastname || ''}</span>
                                    <div class="heat-times" style="justify-content: flex-end;">
                                        <input type="text" class="admin-form-input" placeholder="Run 1" value="${heat.rider_2_run1 || ''}" data-field="rider2_run1">
                                        <input type="text" class="admin-form-input" placeholder="Run 2" value="${heat.rider_2_run2 || ''}" data-field="rider2_run2">
                                    </div>
                                    <div class="heat-total ${r2Winner ? 'winner' : ''}">${heat.rider_2_total ? formatTime(heat.rider_2_total) : '-'}</div>
                                </div>
                            </div>
                            <div style="margin-top: var(--space-md); text-align: center;">
                                <button type="button" class="btn-admin btn-admin-primary btn-admin-sm save-heat-btn">
                                    <i data-lucide="save"></i> Spara
                                </button>
                            </div>
                        </div>`;
                    });

                    html += '</div></div>';
                }

                container.innerHTML = html;

                // Re-init lucide icons
                if (window.lucide) lucide.createIcons();

                // Add save handlers
                container.querySelectorAll('.save-heat-btn').forEach(btn => {
                    btn.addEventListener('click', async function() {
                        const card = this.closest('.heat-card');
                        const heatId = card.dataset.heatId;
                        const data = {
                            ajax: 1,
                            action: 'save_heat',
                            heat_id: heatId,
                            rider1_run1: parseTime(card.querySelector('[data-field="rider1_run1"]').value) || '',
                            rider1_run2: parseTime(card.querySelector('[data-field="rider1_run2"]').value) || '',
                            rider2_run1: parseTime(card.querySelector('[data-field="rider2_run1"]').value) || '',
                            rider2_run2: parseTime(card.querySelector('[data-field="rider2_run2"]').value) || ''
                        };

                        try {
                            const response = await fetch('', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                                body: new URLSearchParams(data).toString()
                            });
                            const result = await response.json();

                            if (result.success) {
                                loadBrackets(); // Reload to show updated state
                            } else {
                                alert('Fel: ' + result.error);
                            }
                        } catch (e) {
                            alert('Nätverksfel');
                        }
                    });
                });

            } else {
                container.innerHTML = `<div class="admin-empty-state">
                    <i data-lucide="git-branch"></i>
                    <h3>Inget bracket</h3>
                    <p>Generera bracket från kvalresultaten först.</p>
                    <a href="/admin/elimination-manage.php?event_id=${eventId}&class_id=${currentClassId}" class="btn-admin btn-admin-primary mt-md">
                        Gå till Hantera Elimination
                    </a>
                </div>`;
                if (window.lucide) lucide.createIcons();
            }
        } catch (e) {
            container.innerHTML = '<p class="text-center" style="color: var(--color-danger);">Fel vid laddning</p>';
        }
    }

    // Handle qualifying form submit
    qualifyingForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const riderId = document.getElementById('rider-select').value;
        const run1 = parseTime(document.getElementById('run1-input').value);
        const run2 = parseTime(document.getElementById('run2-input').value);
        const status = document.getElementById('status-select').value;

        if (!riderId) {
            alert('Välj en åkare');
            return;
        }

        try {
            const response = await fetch('', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `ajax=1&action=save_qualifying&rider_id=${riderId}&class_id=${currentClassId}&run1=${run1 || ''}&run2=${run2 || ''}&status=${status}`
            });
            const data = await response.json();

            if (data.success) {
                // Clear form
                document.getElementById('rider-select').value = '';
                document.getElementById('run1-input').value = '';
                document.getElementById('run2-input').value = '';
                document.getElementById('status-select').value = 'finished';

                // Reload list
                loadQualifying();
            } else {
                alert('Fel: ' + data.error);
            }
        } catch (e) {
            alert('Nätverksfel');
        }
    });

    // Refresh buttons
    document.getElementById('refresh-qualifying').addEventListener('click', loadQualifying);
    document.getElementById('refresh-brackets').addEventListener('click', loadBrackets);

    // Initial load
    if (currentMode === 'qualifying') {
        loadQualifying();
    } else {
        loadBrackets();
    }
});
</script>

<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
