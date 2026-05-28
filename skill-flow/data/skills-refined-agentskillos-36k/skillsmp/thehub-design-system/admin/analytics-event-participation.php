<?php
/**
 * Analytics - Event Participation Analysis
 *
 * Analyserar deltagarmonster pa event-niva.
 * Forenklad version: Valj varumarke + ar.
 *
 * @package TheHUB Analytics
 * @version 3.3
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;

// Parameters
$currentYear = (int)date('Y');
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $currentYear - 1;
$selectedBrandId = isset($_GET['brand']) ? (int)$_GET['brand'] : null;

// Fetch available brands from series_brands (the actual brand management table)
$brands = [];
try {
    $stmt = $pdo->query("
        SELECT sb.id, sb.name, sb.slug as short_code, sb.gradient_start as color_primary,
               COUNT(DISTINCT s.id) as series_count
        FROM series_brands sb
        LEFT JOIN series s ON s.brand_id = sb.id
        WHERE sb.active = 1
        GROUP BY sb.id
        ORDER BY sb.display_order, sb.name
    ");
    $brands = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Fallback
    try {
        $stmt = $pdo->query("SELECT id, name, slug as short_code, gradient_start as color_primary FROM series_brands WHERE active = 1 ORDER BY name");
        $brands = $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (Exception $e2) {}
}

// Fetch available years
$years = [];
try {
    $stmt = $pdo->query("
        SELECT DISTINCT YEAR(date) as year, COUNT(*) as event_count
        FROM events
        WHERE date IS NOT NULL AND active = 1
        GROUP BY YEAR(date)
        ORDER BY year DESC
    ");
    $years = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {}

// Validate year
$validYears = array_column($years, 'year');
if (!in_array($selectedYear, $validYears) && !empty($validYears)) {
    $selectedYear = $validYears[0];
}

// Fetch event participation data
$data = null;
$error = null;

try {
    // Bygg query baserat på filter
    $params = [$selectedYear];
    $brandJoin = '';
    $brandWhere = '';

    if ($selectedBrandId) {
        $brandJoin = "
            JOIN series_events se ON se.event_id = e.id
            JOIN series s ON s.id = se.series_id
        ";
        $brandWhere = "AND s.brand_id = ?";
        $params[] = $selectedBrandId;
    }

    // Hämta events med deltagare
    $sql = "
        SELECT
            e.id,
            e.name,
            e.date,
            e.location,
            COUNT(DISTINCT r.cyclist_id) as participants,
            COUNT(DISTINCT CASE WHEN r.position <= 3 THEN r.cyclist_id END) as podium_riders
        FROM events e
        JOIN results r ON r.event_id = e.id
        $brandJoin
        WHERE YEAR(e.date) = ?
        $brandWhere
        GROUP BY e.id
        ORDER BY e.date DESC
    ";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $events = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // För varje event, beräkna exklusiva deltagare (som ENDAST tävlade på detta event)
    // samt hur många av dem som även tävlade i annan serie
    foreach ($events as &$event) {
        // Hitta deltagare som ENDAST tävlade på detta event under året (inom vald serie/brand)
        $exclusiveSql = "
            SELECT r.cyclist_id
            FROM results r
            WHERE r.event_id = ?
            AND r.cyclist_id IN (
                -- Deltagare som endast har 1 event under året inom samma brand/serie
                SELECT sub_r.cyclist_id
                FROM results sub_r
                JOIN events sub_e ON sub_e.id = sub_r.event_id
                " . ($selectedBrandId ? "
                    JOIN series_events sub_se ON sub_se.event_id = sub_e.id
                    JOIN series sub_s ON sub_s.id = sub_se.series_id
                " : "") . "
                WHERE YEAR(sub_e.date) = ?
                " . ($selectedBrandId ? "AND sub_s.brand_id = ?" : "") . "
                GROUP BY sub_r.cyclist_id
                HAVING COUNT(DISTINCT sub_r.event_id) = 1
            )
        ";

        $exclusiveParams = [$event['id'], $selectedYear];
        if ($selectedBrandId) {
            $exclusiveParams[] = $selectedBrandId;
        }

        $stmt = $pdo->prepare($exclusiveSql);
        $stmt->execute($exclusiveParams);
        $exclusiveRiders = $stmt->fetchAll(PDO::FETCH_COLUMN);
        $event['exclusive_count'] = count($exclusiveRiders);

        // Av dessa exklusiva, hur många tävlade i ANNAN serie under året?
        $event['exclusive_other_series'] = 0;
        if (!empty($exclusiveRiders)) {
            $placeholders = implode(',', array_fill(0, count($exclusiveRiders), '?'));

            // Hitta deltagare som har resultat i en annan serie under samma år
            $otherSeriesSql = "
                SELECT COUNT(DISTINCT r.cyclist_id)
                FROM results r
                JOIN events e ON e.id = r.event_id
                JOIN series_events se ON se.event_id = e.id
                JOIN series s ON s.id = se.series_id
                WHERE YEAR(e.date) = ?
                AND r.cyclist_id IN ($placeholders)
                " . ($selectedBrandId ? "AND s.brand_id != ?" : "") . "
            ";

            $otherParams = [$selectedYear];
            $otherParams = array_merge($otherParams, $exclusiveRiders);
            if ($selectedBrandId) {
                $otherParams[] = $selectedBrandId;
            }

            $stmt = $pdo->prepare($otherSeriesSql);
            $stmt->execute($otherParams);
            $event['exclusive_other_series'] = (int)$stmt->fetchColumn();
        }
    }
    unset($event); // Bryt referensen

    // Beräkna statistik
    $totalParticipants = 0;
    $uniqueRiders = [];

    $riderSql = "
        SELECT DISTINCT r.cyclist_id
        FROM results r
        JOIN events e ON e.id = r.event_id
        $brandJoin
        WHERE YEAR(e.date) = ?
        $brandWhere
    ";
    $stmt = $pdo->prepare($riderSql);
    $stmt->execute($params);
    $uniqueRiders = $stmt->fetchAll(PDO::FETCH_COLUMN);

    // Deltagare per antal event
    $distributionSql = "
        SELECT
            events_attended,
            COUNT(*) as rider_count
        FROM (
            SELECT
                r.cyclist_id,
                COUNT(DISTINCT r.event_id) as events_attended
            FROM results r
            JOIN events e ON e.id = r.event_id
            $brandJoin
            WHERE YEAR(e.date) = ?
            $brandWhere
            GROUP BY r.cyclist_id
        ) rider_events
        GROUP BY events_attended
        ORDER BY events_attended
    ";
    $stmt = $pdo->prepare($distributionSql);
    $stmt->execute($params);
    $distribution = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $data = [
        'events' => $events,
        'total_events' => count($events),
        'total_participants' => array_sum(array_column($events, 'participants')),
        'unique_riders' => count($uniqueRiders),
        'distribution' => $distribution,
    ];

} catch (Exception $e) {
    $error = $e->getMessage();
}

// Page config
$page_title = 'Event Participation Analysis';
include __DIR__ . '/components/unified-layout.php';
?>

<style>
/* Filter Bar */
.filter-bar {
    display: flex;
    gap: var(--space-lg);
    margin-bottom: var(--space-xl);
    padding: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.filter-form {
    display: flex;
    gap: var(--space-lg);
    align-items: flex-end;
    flex-wrap: wrap;
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.filter-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    font-weight: var(--weight-medium);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

.stat-box {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    text-align: center;
}

.stat-box .value {
    font-family: var(--font-heading);
    font-size: var(--text-2xl);
    color: var(--color-accent);
}

.stat-box .label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: var(--space-2xs);
}

.distribution-chart {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.dist-row {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.dist-label {
    width: 80px;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.dist-bar-bg {
    flex: 1;
    height: 24px;
    background: var(--color-bg-surface);
    border-radius: var(--radius-sm);
    overflow: hidden;
}

.dist-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--color-accent), var(--color-accent-hover));
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    padding-left: var(--space-sm);
    color: white;
    font-size: var(--text-xs);
    font-weight: 600;
}

.dist-count {
    width: 60px;
    text-align: right;
    font-size: var(--text-sm);
    font-weight: 500;
}

/* Responsive */
@media (max-width: 767px) {
    .filter-bar {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
        width: calc(100% + 32px);
    }

    .filter-form {
        flex-direction: column;
        width: 100%;
    }

    .filter-group {
        width: 100%;
    }

    .filter-group select {
        width: 100%;
    }
}
</style>

<!-- Filter Bar -->
<div class="filter-bar">
    <form method="get" class="filter-form">
        <?php if (!empty($brands)): ?>
        <div class="filter-group">
            <label class="filter-label">Varumarke</label>
            <select name="brand" class="form-select" onchange="this.form.submit()">
                <option value="">Alla varumarken</option>
                <?php foreach ($brands as $brand): ?>
                    <option value="<?= $brand['id'] ?>" <?= $selectedBrandId == $brand['id'] ? 'selected' : '' ?>
                        <?php if (!empty($brand['color_primary'])): ?>style="border-left: 3px solid <?= htmlspecialchars($brand['color_primary']) ?>"<?php endif; ?>>
                        <?= htmlspecialchars($brand['name']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <?php endif; ?>

        <div class="filter-group">
            <label class="filter-label">Artal</label>
            <select name="year" class="form-select" onchange="this.form.submit()">
                <?php foreach ($years as $y): ?>
                    <option value="<?= $y['year'] ?>" <?= $selectedYear == $y['year'] ? 'selected' : '' ?>>
                        <?= $y['year'] ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
    </form>
</div>

<?php if ($selectedBrandId): ?>
    <?php
    $brandName = '';
    foreach ($brands as $b) {
        if ($b['id'] == $selectedBrandId) {
            $brandName = $b['name'];
            break;
        }
    }
    ?>
<div class="alert alert-info" style="margin-bottom: var(--space-lg);">
    <i data-lucide="filter"></i>
    <div>
        Visar event for <strong><?= htmlspecialchars($brandName) ?></strong>.
        <a href="?year=<?= $selectedYear ?>">Visa alla varumarken</a>
    </div>
</div>
<?php endif; ?>

<?php if ($error): ?>
<div class="alert alert-danger">
    <i data-lucide="alert-circle"></i>
    <?= htmlspecialchars($error) ?>
</div>
<?php elseif ($data): ?>

<!-- Stats Overview -->
<div class="stats-grid">
    <div class="stat-box">
        <div class="value"><?= number_format($data['total_events']) ?></div>
        <div class="label">Event</div>
    </div>
    <div class="stat-box">
        <div class="value"><?= number_format($data['unique_riders']) ?></div>
        <div class="label">Unika deltagare</div>
    </div>
    <div class="stat-box">
        <div class="value"><?= number_format($data['total_participants']) ?></div>
        <div class="label">Totalt starter</div>
    </div>
    <div class="stat-box">
        <div class="value"><?= $data['unique_riders'] > 0 ? round($data['total_participants'] / $data['unique_riders'], 1) : 0 ?></div>
        <div class="label">Snitt starter/person</div>
    </div>
</div>

<!-- Distribution Chart -->
<?php if (!empty($data['distribution'])): ?>
<div class="card">
    <div class="card-header">
        <h3>Deltagare per antal event</h3>
    </div>
    <div class="card-body">
        <div class="distribution-chart">
            <?php
            $maxCount = max(array_column($data['distribution'], 'rider_count'));
            $totalRiders = array_sum(array_column($data['distribution'], 'rider_count'));
            foreach ($data['distribution'] as $d):
                $pct = $totalRiders > 0 ? round(($d['rider_count'] / $totalRiders) * 100, 1) : 0;
                $barWidth = $maxCount > 0 ? ($d['rider_count'] / $maxCount) * 100 : 0;
            ?>
            <div class="dist-row">
                <div class="dist-label"><?= $d['events_attended'] ?> event</div>
                <div class="dist-bar-bg">
                    <div class="dist-bar" style="width: <?= $barWidth ?>%;">
                        <?= $pct ?>%
                    </div>
                </div>
                <div class="dist-count"><?= number_format($d['rider_count']) ?></div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Events Table -->
<div class="card">
    <div class="card-header">
        <h3>Event <?= $selectedYear ?></h3>
    </div>
    <div class="card-body" style="padding-bottom:0;">
        <p class="text-muted" style="font-size:var(--text-sm);margin:0 0 var(--space-sm) 0;">
            <strong>Endast detta:</strong> Antal deltagare som enbart tävlade på just detta event inom valt varumärke.
            <span style="opacity:0.8;">Siffran inom parentes anger hur många av dessa som även deltog i en annan serie.</span>
        </p>
    </div>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Event</th>
                    <th>Datum</th>
                    <th>Plats</th>
                    <th class="text-right">Deltagare</th>
                    <th class="text-right">
                        Endast detta
                        <span class="help-icon" title="Antal deltagare som ENDAST tävlade på just detta event inom vald serie/varumärke. Siffran inom parentes visar hur många av dessa som även tävlade i en annan serie.">
                            <i data-lucide="help-circle" style="width:14px;height:14px;opacity:0.6;vertical-align:middle;"></i>
                        </span>
                    </th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($data['events'] as $event): ?>
                <tr>
                    <td><strong><?= htmlspecialchars($event['name']) ?></strong></td>
                    <td><?= date('Y-m-d', strtotime($event['date'])) ?></td>
                    <td><?= htmlspecialchars($event['location'] ?: '-') ?></td>
                    <td class="text-right"><?= number_format($event['participants']) ?></td>
                    <td class="text-right">
                        <?php if ($event['exclusive_count'] > 0): ?>
                        <a href="#" class="exclusive-link" data-event-id="<?= $event['id'] ?>" data-event-name="<?= htmlspecialchars($event['name']) ?>" data-year="<?= $selectedYear ?>" data-brand="<?= $selectedBrandId ?: '' ?>">
                            <?= number_format($event['exclusive_count']) ?>
                            <?php if ($event['exclusive_other_series'] > 0): ?>
                                <span class="text-muted">(<?= $event['exclusive_other_series'] ?>)</span>
                            <?php endif; ?>
                        </a>
                        <?php else: ?>
                        0
                        <?php endif; ?>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</div>

<?php endif; ?>

<!-- Modal for exclusive riders -->
<div id="exclusiveModal" class="modal-overlay" style="display:none;">
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="modalTitle">Exklusiva deltagare</h3>
            <button type="button" class="modal-close" onclick="closeExclusiveModal()">&times;</button>
        </div>
        <div class="modal-body" id="modalBody">
            <div class="loading">Laddar...</div>
        </div>
    </div>
</div>

<style>
.exclusive-link {
    color: var(--color-accent);
    text-decoration: none;
    cursor: pointer;
}
.exclusive-link:hover {
    text-decoration: underline;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.6);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-md);
}

.modal-content {
    background: var(--color-bg-card);
    border-radius: var(--radius-lg);
    max-width: 600px;
    width: 100%;
    max-height: 80vh;
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow-lg);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
    margin: 0;
    font-size: var(--text-lg);
}

.modal-close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: var(--color-text-secondary);
    padding: 0;
    line-height: 1;
}

.modal-close:hover {
    color: var(--color-text-primary);
}

.modal-body {
    padding: var(--space-lg);
    overflow-y: auto;
    flex: 1;
}

.rider-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.rider-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-sm);
    background: var(--color-bg-surface);
    border-radius: var(--radius-sm);
}

.rider-item a {
    color: var(--color-accent);
    text-decoration: none;
}

.rider-item a:hover {
    text-decoration: underline;
}

.rider-item .class-badge {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
}

.rider-item .other-series {
    font-size: var(--text-xs);
    color: var(--color-warning);
}

.loading {
    text-align: center;
    color: var(--color-text-secondary);
    padding: var(--space-xl);
}

.class-summary {
    margin-bottom: var(--space-lg);
    padding-bottom: var(--space-md);
    border-bottom: 1px solid var(--color-border);
}

.class-summary h4 {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin: 0 0 var(--space-sm) 0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.class-summary-grid {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-xs);
}

.class-summary-item {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-xs) var(--space-sm);
    background: var(--color-bg-surface);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
}

.class-summary-item .class-name {
    color: var(--color-text-secondary);
}

.class-summary-item .class-count {
    font-weight: 600;
    color: var(--color-accent);
    background: var(--color-accent-light);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
}

.rider-list h4 {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin: 0 0 var(--space-sm) 0;
}
</style>

<script>
function openExclusiveModal(eventId, eventName, year, brandId) {
    document.getElementById('exclusiveModal').style.display = 'flex';
    document.getElementById('modalTitle').textContent = 'Exklusiva deltagare - ' + eventName;
    document.getElementById('modalBody').innerHTML = '<div class="loading">Laddar...</div>';

    // Fetch riders via AJAX
    const params = new URLSearchParams({
        action: 'get_exclusive_riders',
        event_id: eventId,
        year: year,
        brand_id: brandId || ''
    });

    fetch('/admin/api/analytics-exclusive-riders.php?' + params.toString())
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('modalBody').innerHTML = '<div class="alert alert-danger">' + data.error + '</div>';
                return;
            }

            let html = '';
            if (data.riders.length === 0) {
                html += '<p class="text-secondary">Inga exklusiva deltagare hittades.</p>';
            } else {
                // Sammanställning per klass
                if (data.class_counts && data.class_counts.length > 0) {
                    html += '<div class="class-summary">';
                    html += '<h4>Fördelning per klass</h4>';
                    html += '<div class="class-summary-grid">';
                    data.class_counts.forEach(cc => {
                        html += '<div class="class-summary-item">';
                        html += '<span class="class-name">' + cc.name + '</span>';
                        html += '<span class="class-count">' + cc.count + '</span>';
                        html += '</div>';
                    });
                    html += '</div>';
                    html += '</div>';
                }

                // Lista med deltagare
                html += '<div class="rider-list">';
                html += '<h4>' + data.riders.length + ' deltagare</h4>';
                data.riders.forEach(rider => {
                    html += '<div class="rider-item">';
                    html += '<div>';
                    html += '<a href="/rider/' + rider.id + '" target="_blank">' + rider.name + '</a>';
                    if (rider.class_name) {
                        html += ' <span class="class-badge">(' + rider.class_name + ')</span>';
                    }
                    if (rider.other_series) {
                        html += ' <span class="other-series" title="Tävlade även i: ' + rider.other_series + '">+annan serie</span>';
                    }
                    html += '</div>';
                    html += '</div>';
                });
                html += '</div>';
            }
            document.getElementById('modalBody').innerHTML = html;
        })
        .catch(err => {
            document.getElementById('modalBody').innerHTML = '<div class="alert alert-danger">Kunde inte ladda data: ' + err.message + '</div>';
        });
}

function closeExclusiveModal() {
    document.getElementById('exclusiveModal').style.display = 'none';
}

// Close on overlay click
document.getElementById('exclusiveModal').addEventListener('click', function(e) {
    if (e.target === this) closeExclusiveModal();
});

// Close on ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeExclusiveModal();
});

// Attach click handlers
document.querySelectorAll('.exclusive-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        openExclusiveModal(
            this.dataset.eventId,
            this.dataset.eventName,
            this.dataset.year,
            this.dataset.brand
        );
    });
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
