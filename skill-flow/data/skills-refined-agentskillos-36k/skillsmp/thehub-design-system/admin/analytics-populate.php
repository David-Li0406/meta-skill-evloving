<?php
/**
 * Populate Historical - Interactive Version (FIXED)
 *
 * Kor populate ar for ar med AJAX for att undvika timeout.
 * Visar progress i realtid.
 *
 * @package TheHUB Analytics
 */

// CRITICAL FIX: Set timeout limits FIRST before any other code
set_time_limit(30); // Max 30 seconds for initial page load
ini_set('max_execution_time', 30);

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_admin();

// Hantera AJAX-request for ett specifikt ar
if (isset($_GET['run_year'])) {
    // Extend timeout for AJAX processing
    set_time_limit(120);
    ini_set('max_execution_time', 120);

    header('Content-Type: application/json');

    $year = (int)$_GET['run_year'];
    $force = isset($_GET['force']);

    if ($year < 2000 || $year > 2050) {
        echo json_encode(['error' => 'Ogiltigt ar']);
        exit;
    }

    try {
        require_once __DIR__ . '/../analytics/includes/AnalyticsEngine.php';

        global $pdo;
        $engine = new AnalyticsEngine($pdo);
        $engine->enableNonBlockingMode();
        $engine->setForceRerun($force);

        // Anvand den snabba bulk-versionen
        $results = $engine->refreshAllStatsFast($year);
        $results['year'] = $year;

        $results['success'] = true;
        $results['total'] = array_sum(array_filter($results, 'is_numeric'));

        echo json_encode($results);

    } catch (Exception $e) {
        echo json_encode(['error' => $e->getMessage()]);
    }
    exit;
}

// Diagnostik-endpoint
if (isset($_GET['diagnose'])) {
    header('Content-Type: application/json');
    global $pdo;

    $results = [];

    // Test 1: Kolla om view finns
    try {
        $stmt = $pdo->query("SELECT COUNT(*) FROM v_canonical_riders LIMIT 1");
        $results['view_exists'] = true;
        $results['view_count'] = $stmt->fetchColumn();
    } catch (Exception $e) {
        $results['view_exists'] = false;
        $results['view_error'] = $e->getMessage();
    }

    // Test 2: Kolla kohorter
    try {
        $stmt = $pdo->query("
            SELECT YEAR(e.date) as yr, COUNT(DISTINCT res.cyclist_id) as cnt
            FROM results res
            JOIN events e ON res.event_id = e.id
            WHERE e.date IS NOT NULL
            GROUP BY YEAR(e.date)
            ORDER BY yr
        ");
        $results['cohorts'] = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);
    } catch (Exception $e) {
        $results['cohort_error'] = $e->getMessage();
    }

    // Test 3: DIREKT kontroll av rider_first_season tabellen
    try {
        $stmt = $pdo->query("
            SELECT cohort_year, COUNT(*) as cnt
            FROM rider_first_season
            GROUP BY cohort_year
            ORDER BY cohort_year DESC
        ");
        $results['rider_first_season'] = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);
    } catch (Exception $e) {
        $results['rfs_error'] = $e->getMessage();
    }

    // Test 4: Kontroll av rider_journey_years
    try {
        $stmt = $pdo->query("
            SELECT cohort_year, COUNT(*) as cnt
            FROM rider_journey_years
            GROUP BY cohort_year
            ORDER BY cohort_year DESC
        ");
        $results['rider_journey_years'] = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);
    } catch (Exception $e) {
        $results['rjy_error'] = $e->getMessage();
    }

    echo json_encode($results, JSON_PRETTY_PRINT);
    exit;
}

// Hantera AJAX-request for kohort journey-analys
if (isset($_GET['run_cohort'])) {
    // Extend timeout for heavy calculations
    set_time_limit(300);
    ini_set('max_execution_time', 300);

    header('Content-Type: application/json');

    $cohortYear = (int)$_GET['run_cohort'];

    if ($cohortYear < 2000 || $cohortYear > 2050) {
        echo json_encode(['error' => 'Ogiltigt kohort-ar']);
        exit;
    }

    try {
        require_once __DIR__ . '/../analytics/includes/AnalyticsEngine.php';

        global $pdo;
        $engine = new AnalyticsEngine($pdo);
        $engine->setForceRerun(true); // Always recalculate

        // Kor full journey-analys for kohorten
        $results = $engine->calculateFullJourneyAnalysis($cohortYear);
        $results['cohort_year'] = $cohortYear;
        $results['success'] = true;

        echo json_encode($results);

    } catch (Exception $e) {
        echo json_encode(['error' => $e->getMessage()]);
    } catch (Throwable $t) {
        echo json_encode(['error' => 'Fatal: ' . $t->getMessage()]);
    }
    exit;
}

// FIX: Hamta tillgangliga ar MED timeout-skydd och felhantering
global $pdo;
$years = [];
$error = null;

try {
    // Add timeout to the query itself
    $pdo->setAttribute(PDO::ATTR_TIMEOUT, 5);

    $stmt = $pdo->prepare("
        SELECT DISTINCT YEAR(date) as year
        FROM events
        WHERE date IS NOT NULL
        ORDER BY year ASC
        LIMIT 50
    ");

    $stmt->execute();
    $years = $stmt->fetchAll(PDO::FETCH_COLUMN);

    // Fallback if no years found
    if (empty($years)) {
        $error = "Inga år hittades i events-tabellen";
    }

} catch (PDOException $e) {
    $error = "Databasfel: " . $e->getMessage();
    // Set some default years so page doesn't completely break
    $years = range(2015, date('Y'));
} catch (Exception $e) {
    $error = "Fel vid hämtning av år: " . $e->getMessage();
    $years = range(2015, date('Y'));
}

$page_title = 'Populate Historical Data';
$breadcrumbs = [
    ['label' => 'Tools', 'url' => '/admin/tools.php'],
    ['label' => 'Populate Historical']
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.populate-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-lg);
}
.year-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: var(--space-sm);
    margin: var(--space-lg) 0;
}
.year-item {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: var(--space-sm) var(--space-md);
    text-align: center;
    transition: all 0.2s;
}
.year-item.pending { opacity: 0.5; }
.year-item.running {
    border-color: var(--color-accent);
    background: var(--color-accent-light);
}
.year-item.done {
    border-color: var(--color-success);
    background: rgba(16, 185, 129, 0.1);
}
.year-item.error {
    border-color: var(--color-error);
    background: rgba(239, 68, 68, 0.1);
}
.year-item .year-label {
    font-weight: 600;
    font-size: var(--text-lg);
}
.year-item .year-status {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
    margin-top: var(--space-2xs);
}
.year-item.done .year-status { color: var(--color-success); }
.year-item.error .year-status { color: var(--color-error); }

.progress-bar {
    width: 100%;
    height: 8px;
    background: var(--color-bg-surface);
    border-radius: var(--radius-full);
    overflow: hidden;
    margin: var(--space-md) 0;
}
.progress-bar-fill {
    height: 100%;
    background: var(--color-accent);
    transition: width 0.3s;
    width: 0%;
}
.progress-text {
    text-align: center;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}
.log-output {
    background: var(--color-bg-page);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: var(--space-md);
    font-family: monospace;
    font-size: var(--text-sm);
    max-height: 300px;
    overflow-y: auto;
    white-space: pre-wrap;
}
.controls {
    display: flex;
    gap: var(--space-md);
    align-items: center;
    flex-wrap: wrap;
}
.warning-box {
    background: rgba(251, 191, 36, 0.1);
    border: 1px solid rgba(251, 191, 36, 0.3);
    border-radius: var(--radius-sm);
    padding: var(--space-md);
    margin-bottom: var(--space-lg);
    color: var(--color-warning);
}
</style>

<?php if (isset($error)): ?>
<div class="alert alert-danger">
    <i data-lucide="alert-circle"></i>
    <div><?= htmlspecialchars($error) ?></div>
</div>
<?php endif; ?>

<div class="warning-box">
    <strong>OBS:</strong> Denna sida kör tunga databasoperationer.
    Undvik att köra flera processer samtidigt då det kan låsa databasen.
</div>

<div class="populate-card">
    <h3>Generera Analytics-data</h3>
    <p style="color: var(--color-text-secondary);">
        Beraknar statistik for varje ar. Klicka "Starta" for att borja.
    </p>

    <div class="controls">
        <button id="startBtn" class="btn-admin btn-admin-primary" onclick="startPopulate(false)">
            <i data-lucide="play"></i> Starta
        </button>
        <button id="forceBtn" class="btn-admin btn-admin-secondary" onclick="startPopulate(true)">
            <i data-lucide="zap"></i> Force Re-run
        </button>
        <button id="stopBtn" class="btn-admin btn-admin-secondary" onclick="stopPopulate()" disabled>
            <i data-lucide="square"></i> Stoppa
        </button>
        <span id="statusText" style="color: var(--color-text-muted);"></span>
    </div>

    <div class="progress-bar">
        <div class="progress-bar-fill" id="progressFill"></div>
    </div>
    <div class="progress-text" id="progressText">Klicka for att starta</div>

    <div class="year-list" id="yearList">
        <?php if (!empty($years)): ?>
            <?php foreach ($years as $year): ?>
            <div class="year-item pending" id="year-<?= $year ?>" data-year="<?= $year ?>">
                <div class="year-label"><?= $year ?></div>
                <div class="year-status">Vantar...</div>
            </div>
            <?php endforeach; ?>
        <?php else: ?>
            <div style="grid-column: 1/-1; text-align: center; padding: var(--space-lg);">
                Inga år tillgängliga
            </div>
        <?php endif; ?>
    </div>

    <h4 style="margin-top: var(--space-xl);">Process Log</h4>
    <div class="log-output" id="logOutput"></div>
</div>

<div class="populate-card">
    <h3>Journey-analys (Kohorter)</h3>
    <p style="color: var(--color-text-secondary);">
        Beraknar First Season Journey och Longitudinal Journey per kohort (startar).
        <strong>Krav:</strong> Kor "Generera Analytics-data" ovan forst.
    </p>

    <div class="controls">
        <button id="startCohortBtn" class="btn-admin btn-admin-primary" onclick="startCohortAnalysis()">
            <i data-lucide="users"></i> Generera Journey-data
        </button>
        <button id="stopCohortBtn" class="btn-admin btn-admin-secondary" onclick="stopCohortAnalysis()" disabled>
            <i data-lucide="square"></i> Stoppa
        </button>
        <span id="cohortStatusText" style="color: var(--color-text-muted);"></span>
    </div>

    <div class="progress-bar">
        <div class="progress-bar-fill" id="cohortProgressFill"></div>
    </div>
    <div class="progress-text" id="cohortProgressText">Klicka for att starta</div>

    <div class="year-list" id="cohortList">
        <?php if (!empty($years)): ?>
            <?php foreach ($years as $year): ?>
            <div class="year-item pending" id="cohort-<?= $year ?>" data-year="<?= $year ?>">
                <div class="year-label"><?= $year ?></div>
                <div class="year-status">Vantar...</div>
            </div>
            <?php endforeach; ?>
        <?php else: ?>
            <div style="grid-column: 1/-1; text-align: center; padding: var(--space-lg);">
                Inga kohorter tillgängliga
            </div>
        <?php endif; ?>
    </div>
</div>

<div class="populate-card">
    <h3>Nasta steg</h3>
    <div class="controls">
        <a href="/admin/analytics-first-season.php" class="btn-admin btn-admin-primary">
            <i data-lucide="baby"></i> First Season Journey
        </a>
        <a href="/admin/analytics-diagnose.php" class="btn-admin btn-admin-secondary">
            <i data-lucide="stethoscope"></i> Diagnostisera
        </a>
        <a href="/admin/analytics-trends.php" class="btn-admin btn-admin-secondary">
            <i data-lucide="trending-up"></i> Visa Trender
        </a>
    </div>
</div>

<script>
const years = <?= json_encode($years) ?>;
let isRunning = false;
let currentIndex = 0;
let forceMode = false;
let totalProcessed = 0;

function log(msg) {
    const el = document.getElementById('logOutput');
    const time = new Date().toLocaleTimeString();
    el.textContent += `[${time}] ${msg}\n`;
    el.scrollTop = el.scrollHeight;
}

function updateProgress() {
    const pct = years.length > 0 ? (currentIndex / years.length * 100) : 0;
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = `${currentIndex} / ${years.length} ar (${totalProcessed} rader totalt)`;
}

function setYearStatus(year, status, text) {
    const el = document.getElementById('year-' + year);
    if (el) {
        el.className = 'year-item ' + status;
        el.querySelector('.year-status').textContent = text;
    }
}

async function processYear(year) {
    setYearStatus(year, 'running', 'Bearbetar...');

    try {
        const url = `/admin/analytics-populate.php?run_year=${year}${forceMode ? '&force=1' : ''}`;

        // Add timeout to fetch request
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 min timeout

        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(timeoutId);

        const data = await response.json();

        if (data.error) {
            setYearStatus(year, 'error', data.error);
            log(`${year}: FEL - ${data.error}`);
            return false;
        }

        const total = data.total || 0;
        totalProcessed += total;

        if (total > 0) {
            setYearStatus(year, 'done', `${total} rader`);
            log(`${year}: ${data.yearly_stats} riders, ${data.series_participation} participations, ${data.club_stats} klubbar`);
        } else {
            setYearStatus(year, 'done', 'Redan klar');
            log(`${year}: Redan beraknat (hoppades over)`);
        }
        return true;

    } catch (e) {
        if (e.name === 'AbortError') {
            setYearStatus(year, 'error', 'Timeout');
            log(`${year}: TIMEOUT efter 2 minuter`);
        } else {
            setYearStatus(year, 'error', 'Natverksfel');
            log(`${year}: FEL - ${e.message}`);
        }
        return false;
    }
}

async function runLoop() {
    while (isRunning && currentIndex < years.length) {
        const year = years[currentIndex];
        await processYear(year);
        currentIndex++;
        updateProgress();

        // Liten paus mellan ar for att inte overbelasta servern
        await new Promise(r => setTimeout(r, 100));
    }

    if (currentIndex >= years.length) {
        log('=== KLAR! ===');
        document.getElementById('statusText').textContent = 'Klar!';
    }

    isRunning = false;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('forceBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
}

function startPopulate(force) {
    if (isRunning) return;

    forceMode = force;
    isRunning = true;
    currentIndex = 0;
    totalProcessed = 0;

    // Reset UI
    document.getElementById('logOutput').textContent = '';
    years.forEach(y => setYearStatus(y, 'pending', 'Vantar...'));

    document.getElementById('startBtn').disabled = true;
    document.getElementById('forceBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;
    document.getElementById('statusText').textContent = force ? 'Kor med Force...' : 'Kor...';

    log(force ? '=== STARTAR (FORCE MODE) ===' : '=== STARTAR ===');
    log(`Bearbetar ${years.length} ar...`);
    log('');

    updateProgress();
    runLoop();
}

function stopPopulate() {
    isRunning = false;
    document.getElementById('statusText').textContent = 'Stoppad';
    log('--- Stoppad av anvandaren ---');
}

// ===== COHORT JOURNEY ANALYSIS =====
let isCohortRunning = false;
let cohortIndex = 0;

function setCohortStatus(year, status, text) {
    const el = document.getElementById('cohort-' + year);
    if (el) {
        el.className = 'year-item ' + status;
        el.querySelector('.year-status').textContent = text;
    }
}

function updateCohortProgress() {
    const pct = years.length > 0 ? (cohortIndex / years.length * 100) : 0;
    document.getElementById('cohortProgressFill').style.width = pct + '%';
    document.getElementById('cohortProgressText').textContent = `${cohortIndex} / ${years.length} kohorter`;
}

async function processCohort(year) {
    setCohortStatus(year, 'running', 'Bearbetar...');

    try {
        const url = `/admin/analytics-populate.php?run_cohort=${year}`;
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 min timeout

        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(timeoutId);
        const data = await response.json();

        if (data.error) {
            setCohortStatus(year, 'error', data.error.substring(0, 30));
            log(`Kohort ${year}: FEL - ${data.error}`);
            return false;
        }

        const fs = data.first_season || 0;
        const fsa = data.first_season_aggregates || 0;
        const long = data.longitudinal || 0;
        const brand = data.brand_aggregates || 0;

        setCohortStatus(year, 'done', `${fs} riders`);
        log(`Kohort ${year}: first_season=${fs}, aggregates=${fsa}, longitudinal=${long}, brand=${brand}`);
        return true;

    } catch (e) {
        if (e.name === 'AbortError') {
            setCohortStatus(year, 'error', 'Timeout');
            log(`Kohort ${year}: TIMEOUT efter 5 minuter`);
        } else {
            setCohortStatus(year, 'error', 'Natverksfel');
            log(`Kohort ${year}: FEL - ${e.message}`);
        }
        return false;
    }
}

async function runCohortLoop() {
    while (isCohortRunning && cohortIndex < years.length) {
        const year = years[cohortIndex];
        await processCohort(year);
        cohortIndex++;
        updateCohortProgress();

        // Langre paus for tunga berakningar
        await new Promise(r => setTimeout(r, 500));
    }

    if (cohortIndex >= years.length) {
        log('=== JOURNEY-ANALYS KLAR! ===');
        document.getElementById('cohortStatusText').textContent = 'Klar!';
    }

    isCohortRunning = false;
    document.getElementById('startCohortBtn').disabled = false;
    document.getElementById('stopCohortBtn').disabled = true;
}

function startCohortAnalysis() {
    if (isCohortRunning) return;

    isCohortRunning = true;
    cohortIndex = 0;

    // Reset UI
    years.forEach(y => setCohortStatus(y, 'pending', 'Vantar...'));

    document.getElementById('startCohortBtn').disabled = true;
    document.getElementById('stopCohortBtn').disabled = false;
    document.getElementById('cohortStatusText').textContent = 'Kor journey-analys...';

    log('');
    log('=== STARTAR JOURNEY-ANALYS ===');
    log(`Bearbetar ${years.length} kohorter...`);
    log('');

    updateCohortProgress();
    runCohortLoop();
}

function stopCohortAnalysis() {
    isCohortRunning = false;
    document.getElementById('cohortStatusText').textContent = 'Stoppad';
    log('--- Journey-analys stoppad ---');
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
