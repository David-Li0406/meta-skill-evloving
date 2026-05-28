<?php
/**
 * Sponsor Management - Admin Page
 * TheHUB - Media & Sponsor System
 *
 * Manage sponsors, tiers, and assignments
 * Promotors can only see/edit sponsors for their own events
 */
require_once __DIR__ . '/../config.php';
require_admin();
require_once __DIR__ . '/../includes/sponsor-functions.php';
require_once __DIR__ . '/../includes/media-functions.php';

global $pdo;

// Check if user is a promotor (limited access)
$isPromotorOnly = isRole('promotor');
$promotorEventIds = [];
$promotorSeriesIds = [];

if ($isPromotorOnly) {
    $currentAdmin = getCurrentAdmin();
    $userId = $currentAdmin['id'];

    // Get series using same query as promotor-series.php (which works)
    $seriesResult = $pdo->prepare("
        SELECT DISTINCT s.id, s.name
        FROM series s
        LEFT JOIN promotor_series ps ON ps.series_id = s.id AND ps.user_id = ?
        LEFT JOIN events e ON e.series_id = s.id
        LEFT JOIN promotor_events pe ON pe.event_id = e.id AND pe.user_id = ?
        WHERE ps.user_id IS NOT NULL OR pe.user_id IS NOT NULL
        ORDER BY s.name
    ");
    $seriesResult->execute([$userId, $userId]);
    $promotorSeriesData = $seriesResult->fetchAll(PDO::FETCH_ASSOC);
    $promotorSeriesIds = array_column($promotorSeriesData, 'id');

    // Get event IDs for promotor (for backward compatibility)
    $promotorEvents = getPromotorEvents();
    $promotorEventIds = array_column($promotorEvents, 'id');
}

// Get filter parameters
$filterTier = $_GET['tier'] ?? null;
$filterSeries = isset($_GET['series']) ? (int)$_GET['series'] : null;
$filterActive = isset($_GET['active']) ? $_GET['active'] === '1' : null;
$searchQuery = $_GET['search'] ?? '';

// Get series for filter and form (limited for promotors)
$allSeries = [];
try {
    if ($isPromotorOnly) {
        // Use the series data we already fetched
        $allSeries = $promotorSeriesData ?? [];
    } else {
        $seriesStmt = $pdo->query("SELECT id, name FROM series ORDER BY name");
        $allSeries = $seriesStmt->fetchAll(PDO::FETCH_ASSOC);
    }
} catch (Exception $e) {
    error_log("Sponsors - could not load series: " . $e->getMessage());
}

// Get sponsors (with optional series filter)
// Promotors only see sponsors linked to their series
if ($isPromotorOnly && empty($promotorSeriesIds)) {
    // Promotor with no series - show empty
    $sponsors = [];
} elseif ($searchQuery) {
    $sponsors = search_sponsors($searchQuery, 100);
    // Filter search results for promotors
    if ($isPromotorOnly && !empty($promotorSeriesIds)) {
        $sponsors = array_filter($sponsors, function($sp) use ($pdo, $promotorSeriesIds) {
            $stmt = $pdo->prepare("SELECT 1 FROM series_sponsors WHERE sponsor_id = ? AND series_id IN (" . implode(',', $promotorSeriesIds) . ") LIMIT 1");
            $stmt->execute([$sp['id']]);
            return $stmt->fetch() !== false;
        });
        $sponsors = array_values($sponsors);
    }
} elseif ($filterSeries || ($isPromotorOnly && !empty($promotorSeriesIds))) {
    // Filter by series (or all promotor's series)
    $seriesFilter = $filterSeries ? [$filterSeries] : $promotorSeriesIds;
    $placeholders = implode(',', array_fill(0, count($seriesFilter), '?'));
    $stmt = $pdo->prepare("
        SELECT DISTINCT s.*, ss.series_id
        FROM sponsors s
        INNER JOIN series_sponsors ss ON s.id = ss.sponsor_id
        WHERE ss.series_id IN ($placeholders)
        " . ($filterTier ? " AND s.tier = ?" : "") . "
        " . ($filterActive !== null ? " AND s.active = ?" : "") . "
        ORDER BY s.display_order, s.name
    ");
    $params = $seriesFilter;
    if ($filterTier) $params[] = $filterTier;
    if ($filterActive !== null) $params[] = $filterActive ? 1 : 0;
    $stmt->execute($params);
    $sponsors = $stmt->fetchAll(PDO::FETCH_ASSOC);
    // Add logo_url
    foreach ($sponsors as &$sp) {
        $sp['logo_url'] = $sp['logo'] ? '/uploads/sponsors/' . $sp['logo'] : null;
    }
} else {
    $sponsors = get_sponsors($filterActive !== false, $filterTier);
}

// Get stats
$stats = get_sponsor_stats();
$totalSponsors = array_sum(array_column($stats, 'count'));
$activeSponsors = array_sum(array_column($stats, 'active_count'));

// Tier definitions
$tiers = [
    'title' => ['name' => 'Titelsponsor', 'color' => '#8B5CF6'],
    'gold' => ['name' => 'Guldsponsor', 'color' => '#F59E0B'],
    'silver' => ['name' => 'Silversponsor', 'color' => '#9CA3AF'],
    'bronze' => ['name' => 'Bronssponsor', 'color' => '#D97706']
];

// Page config - promotors see "Media", admins see "Sponsorer"
$page_title = $isPromotorOnly ? 'Media' : 'Sponsorer';
$breadcrumbs = [
    ['label' => $page_title]
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<style>
/* Sponsor page styles */
.sponsor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
    gap: var(--space-md);
}

.sponsor-stats {
    display: flex;
    gap: var(--space-lg);
}

.sponsor-stat {
    text-align: center;
}

.sponsor-stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-accent);
}

.sponsor-stat-label {
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    text-transform: uppercase;
}

/* Filters */
.sponsor-filters {
    display: flex;
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
    align-items: center;
}

.sponsor-filters form {
    display: flex;
    gap: var(--space-sm);
    flex: 1;
    min-width: 200px;
}

.sponsor-filters input,
.sponsor-filters select {
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-surface);
    color: var(--color-text-primary);
}

.sponsor-filters input {
    flex: 1;
}

.tier-filter {
    display: flex;
    gap: var(--space-xs);
}

.tier-filter-btn {
    padding: var(--space-xs) var(--space-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-surface);
    color: var(--color-text-secondary);
    cursor: pointer;
    font-size: 0.75rem;
    text-decoration: none;
}

.tier-filter-btn:hover {
    background: var(--color-bg-hover);
}

.tier-filter-btn.active {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}

/* Sponsor grid */
.sponsor-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--space-lg);
}

.sponsor-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
    transition: all 0.15s;
}

.sponsor-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.sponsor-card-header {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    border-bottom: 1px solid var(--color-border);
}

.sponsor-logo {
    width: 60px;
    height: 60px;
    border-radius: var(--radius-sm);
    background: var(--color-bg-sunken);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
}

.sponsor-logo img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.sponsor-logo-placeholder {
    color: var(--color-text-secondary);
    font-size: 24px;
    font-weight: 700;
}

.sponsor-info {
    flex: 1;
    min-width: 0;
}

.sponsor-name {
    font-weight: 600;
    font-size: 1rem;
    margin: 0 0 var(--space-2xs);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sponsor-tier {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
}

.sponsor-status {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--color-error);
}

.sponsor-status.active {
    background: var(--color-success);
}

.sponsor-card-body {
    padding: var(--space-md);
}

.sponsor-meta {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}

.sponsor-meta-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.sponsor-meta-item svg {
    width: 14px;
    height: 14px;
    flex-shrink: 0;
}

.sponsor-card-footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-sunken);
    border-top: 1px solid var(--color-border);
}

/* Modal styles */
.modal {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.8);
    z-index: 1000;
    padding: var(--space-lg);
    overflow-y: auto;
}

.modal.active {
    display: flex;
    align-items: flex-start;
    justify-content: center;
}

.modal-content {
    background: var(--color-bg-surface);
    border-radius: var(--radius-lg);
    max-width: 600px;
    width: 100%;
    margin-top: var(--space-xl);
}

/* Mobile: Fullscreen modal */
@media (max-width: 599px) {
    .modal {
        padding: 0;
    }
    .modal-content {
        max-width: 100%;
        height: 100%;
        margin: 0;
        border-radius: 0;
        display: flex;
        flex-direction: column;
    }
    .modal-header {
        padding-top: calc(var(--space-md) + env(safe-area-inset-top, 0px));
        flex-shrink: 0;
    }
    .modal-body {
        flex: 1;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
    }
    .modal-footer {
        padding-bottom: calc(var(--space-md) + env(safe-area-inset-bottom, 0px));
        flex-shrink: 0;
    }
    .modal-close {
        min-width: 44px;
        min-height: 44px;
    }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.modal-close {
    background: none;
    border: none;
    padding: var(--space-xs);
    cursor: pointer;
    color: var(--color-text-secondary);
}

.modal-body {
    padding: var(--space-lg);
}

.form-group {
    margin-bottom: var(--space-md);
}

.form-label {
    display: block;
    font-weight: 500;
    margin-bottom: var(--space-xs);
    font-size: 0.875rem;
}

.form-input,
.form-select,
.form-textarea {
    width: 100%;
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-sunken);
    color: var(--color-text-primary);
}

.form-textarea {
    resize: vertical;
    min-height: 100px;
}

.form-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-md);
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
    padding: var(--space-md) var(--space-lg);
    background: var(--color-bg-sunken);
    border-top: 1px solid var(--color-border);
}

/* Logo picker */
.logo-picker {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.logo-preview {
    width: 80px;
    height: 80px;
    background: var(--color-bg-sunken);
    border: 2px dashed var(--color-border);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.logo-preview img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.logo-preview:hover {
    border-color: var(--color-accent);
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: var(--space-2xl);
    color: var(--color-text-secondary);
}

.empty-state-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto var(--space-md);
    opacity: 0.5;
}

/* Event banner upload section for promotors */
.upload-section {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-xl);
}
.upload-section-title {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 var(--space-md) 0;
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}
.upload-section-title svg {
    width: 20px;
    height: 20px;
    color: var(--color-accent);
}
.upload-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: var(--space-md);
}
.upload-box {
    background: var(--color-bg-sunken);
    border: 2px dashed var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.upload-box:hover {
    border-color: var(--color-accent);
    background: var(--color-bg-hover);
}
.upload-box svg {
    width: 32px;
    height: 32px;
    color: var(--color-text-secondary);
    margin-bottom: var(--space-sm);
}
.upload-box-label {
    font-weight: 500;
    margin-bottom: var(--space-2xs);
}
.upload-box-hint {
    font-size: 0.75rem;
    color: var(--color-text-secondary);
}
.upload-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: var(--space-sm);
    margin-top: var(--space-md);
}
.upload-gallery-item {
    position: relative;
    background: var(--color-bg-sunken);
    border-radius: var(--radius-sm);
    overflow: hidden;
    aspect-ratio: 8/1;
}
.upload-gallery-item.logo {
    aspect-ratio: 4/1;
}
.upload-gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
.upload-gallery-item .delete-btn {
    position: absolute;
    top: 4px;
    right: 4px;
    background: rgba(0,0,0,0.7);
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    cursor: pointer;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.2s;
}
.upload-gallery-item:hover .delete-btn {
    opacity: 1;
}

/* Mobile edge-to-edge */
@media (max-width: 767px) {
    .upload-section,
    .sponsor-card {
        margin-left: calc(-1 * var(--space-md));
        margin-right: calc(-1 * var(--space-md));
        border-radius: 0;
        border-left: none;
        border-right: none;
        width: calc(100% + var(--space-md) * 2);
    }
    .sponsor-grid {
        gap: 0;
        grid-template-columns: 1fr;
    }
}
</style>

<?php if ($isPromotorOnly): ?>
<!-- Event Banner Upload Section -->
<div class="upload-section">
    <h3 class="upload-section-title">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
        Ladda upp bilder
    </h3>

    <!-- Serie-val för uppladdningar -->
    <div class="form-group" style="margin-bottom: var(--space-lg);">
        <label class="form-label">Välj serie för uppladdning</label>
        <select id="uploadSeriesSelect" class="form-select" style="max-width: 300px;">
            <?php if (count($allSeries) === 1): ?>
                <option value="<?= $allSeries[0]['id'] ?>"><?= htmlspecialchars($allSeries[0]['name']) ?></option>
            <?php else: ?>
                <option value="">-- Välj serie --</option>
                <?php foreach ($allSeries as $series): ?>
                <option value="<?= $series['id'] ?>"><?= htmlspecialchars($series['name']) ?></option>
                <?php endforeach; ?>
            <?php endif; ?>
        </select>
        <small style="color: var(--color-text-secondary); display: block; margin-top: var(--space-xs);">
            Uppladdade filer knyts till vald serie och sparas i serie-mappen.
        </small>
    </div>

    <div class="upload-grid">
        <div class="upload-box" onclick="triggerUpload('eventBannerUpload')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
            <div class="upload-box-label">Event-banner</div>
            <div class="upload-box-hint">1200×150px</div>
            <input type="file" id="eventBannerUpload" accept="image/*" style="display:none" onchange="uploadToFolder(this, 'events')">
        </div>

        <div class="upload-box" onclick="triggerUpload('sponsorBannerUpload')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
            <div class="upload-box-label">Sponsor-banner</div>
            <div class="upload-box-hint">1200×150px</div>
            <input type="file" id="sponsorBannerUpload" accept="image/*" style="display:none" onchange="uploadToFolder(this, 'sponsors')">
        </div>

        <div class="upload-box" onclick="triggerUpload('sponsorLogoUpload')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
            <div class="upload-box-label">Sponsor-logo</div>
            <div class="upload-box-hint">600×150px</div>
            <input type="file" id="sponsorLogoUpload" accept="image/*" style="display:none" onchange="uploadToFolder(this, 'sponsors')">
        </div>
    </div>

    <div id="recentUploads" class="upload-gallery" style="display: none;">
        <!-- Recent uploads will appear here -->
    </div>
</div>
<?php endif; ?>

<!-- Header -->
<div class="sponsor-header">
    <div class="sponsor-stats">
        <div class="sponsor-stat">
            <div class="sponsor-stat-value"><?= $totalSponsors ?></div>
            <div class="sponsor-stat-label">Totalt</div>
        </div>
        <div class="sponsor-stat">
            <div class="sponsor-stat-value"><?= $activeSponsors ?></div>
            <div class="sponsor-stat-label">Aktiva</div>
        </div>
    </div>

    <button class="btn btn-primary" onclick="openCreateModal()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></svg>
        Ny sponsor
    </button>
</div>

<!-- Filters -->
<div class="sponsor-filters">
    <form method="get" action="/admin/sponsors.php">
        <input type="text" name="search" placeholder="Sök sponsorer..." value="<?= htmlspecialchars($searchQuery) ?>">
        <button type="submit" class="btn btn-secondary">Sök</button>
    </form>

    <select class="form-select" onchange="filterBySeries(this.value)" style="min-width: 150px;">
        <option value="">Alla serier</option>
        <?php foreach ($allSeries as $series): ?>
        <option value="<?= $series['id'] ?>" <?= $filterSeries === (int)$series['id'] ? 'selected' : '' ?>>
            <?= htmlspecialchars($series['name']) ?>
        </option>
        <?php endforeach; ?>
    </select>

    <?php if (!$isPromotorOnly): ?>
    <div class="tier-filter">
        <a href="/admin/sponsors<?= $filterSeries ? "?series=$filterSeries" : '' ?>" class="tier-filter-btn <?= !$filterTier ? 'active' : '' ?>">Alla</a>
        <?php foreach ($tiers as $tierKey => $tier): ?>
        <a href="/admin/sponsors?tier=<?= $tierKey ?><?= $filterSeries ? "&series=$filterSeries" : '' ?>" class="tier-filter-btn <?= $filterTier === $tierKey ? 'active' : '' ?>" style="<?= $filterTier === $tierKey ? "background: {$tier['color']}; border-color: {$tier['color']};" : '' ?>">
            <?= $tier['name'] ?>
        </a>
        <?php endforeach; ?>
    </div>
    <?php endif; ?>
</div>

<!-- Sponsor Grid -->
<?php if (empty($sponsors)): ?>
<div class="empty-state">
    <svg class="empty-state-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20.42 4.58a5.4 5.4 0 0 0-7.65 0l-.77.78-.77-.78a5.4 5.4 0 0 0-7.65 0C1.46 6.7 1.33 10.28 4 13l8 8 8-8c2.67-2.72 2.54-6.3.42-8.42z"/>
    </svg>
    <h3>Inga sponsorer</h3>
    <p><?= $searchQuery ? 'Inga sponsorer matchar din sökning' : 'Lägg till din första sponsor genom att klicka på "Ny sponsor"' ?></p>
</div>
<?php else: ?>
<div class="sponsor-grid">
    <?php foreach ($sponsors as $sponsor): ?>
    <div class="sponsor-card" data-id="<?= $sponsor['id'] ?>">
        <div class="sponsor-card-header">
            <div class="sponsor-logo">
                <?php if ($sponsor['logo_url']): ?>
                    <img src="<?= htmlspecialchars($sponsor['logo_url']) ?>" alt="<?= htmlspecialchars($sponsor['name']) ?>">
                <?php else: ?>
                    <span class="sponsor-logo-placeholder"><?= strtoupper(substr($sponsor['name'], 0, 2)) ?></span>
                <?php endif; ?>
            </div>
            <div class="sponsor-info">
                <h3 class="sponsor-name"><?= htmlspecialchars($sponsor['name']) ?></h3>
                <span class="sponsor-tier" style="background: <?= $tiers[$sponsor['tier']]['color'] ?>; color: white;">
                    <?= $tiers[$sponsor['tier']]['name'] ?>
                </span>
            </div>
            <div class="sponsor-status <?= $sponsor['active'] ? 'active' : '' ?>" title="<?= $sponsor['active'] ? 'Aktiv' : 'Inaktiv' ?>"></div>
        </div>

        <div class="sponsor-card-body">
            <div class="sponsor-meta">
                <?php if ($sponsor['website']): ?>
                <div class="sponsor-meta-item">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" x2="22" y1="12" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                    <a href="<?= htmlspecialchars($sponsor['website']) ?>" target="_blank" rel="noopener"><?= htmlspecialchars(parse_url($sponsor['website'], PHP_URL_HOST) ?: $sponsor['website']) ?></a>
                </div>
                <?php endif; ?>

                <?php if ($sponsor['contact_email']): ?>
                <div class="sponsor-meta-item">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                    <?= htmlspecialchars($sponsor['contact_email']) ?>
                </div>
                <?php endif; ?>

                <?php if ($sponsor['contact_name']): ?>
                <div class="sponsor-meta-item">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    <?= htmlspecialchars($sponsor['contact_name']) ?>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <div class="sponsor-card-footer">
            <button class="btn btn-sm btn-ghost" onclick="editSponsor(<?= $sponsor['id'] ?>)">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
                Redigera
            </button>
            <button class="btn btn-sm btn-danger" onclick="deleteSponsor(<?= $sponsor['id'] ?>, '<?= htmlspecialchars(addslashes($sponsor['name'])) ?>')">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                Radera
            </button>
        </div>
    </div>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<!-- Create/Edit Modal -->
<div class="modal" id="sponsorModal">
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="modalTitle">Ny sponsor</h3>
            <button class="modal-close" onclick="closeModal()">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-lg"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
            </button>
        </div>
        <form id="sponsorForm" onsubmit="saveSponsor(event)" enctype="multipart/form-data">
            <input type="hidden" id="sponsorId" name="id">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Namn *</label>
                    <input type="text" class="form-input" id="sponsorName" name="name" required>
                </div>

                <?php if (!$isPromotorOnly): ?>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Nivå</label>
                        <select class="form-select" id="sponsorTier" name="tier">
                            <?php foreach ($tiers as $tierKey => $tier): ?>
                            <option value="<?= $tierKey ?>"><?= $tier['name'] ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Status</label>
                        <select class="form-select" id="sponsorActive" name="active">
                            <option value="1">Aktiv</option>
                            <option value="0">Inaktiv</option>
                        </select>
                    </div>
                </div>
                <?php else: ?>
                <input type="hidden" id="sponsorTier" name="tier" value="bronze">
                <input type="hidden" id="sponsorActive" name="active" value="1">
                <?php endif; ?>

                <div class="form-group">
                    <label class="form-label">Serier</label>
                    <div class="series-checkboxes" id="seriesCheckboxes" style="display: flex; flex-wrap: wrap; gap: var(--space-sm);">
                        <?php foreach ($allSeries as $series): ?>
                        <label style="display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; background: var(--color-bg-sunken); border-radius: var(--radius-sm); cursor: pointer; font-size: 0.875rem;">
                            <input type="checkbox" name="series[]" value="<?= $series['id'] ?>" class="series-checkbox">
                            <?= htmlspecialchars($series['name']) ?>
                        </label>
                        <?php endforeach; ?>
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Webbplats <?php if ($isPromotorOnly): ?><span style="color: var(--color-error);">*</span><?php endif; ?></label>
                    <input type="url" class="form-input" id="sponsorWebsite" name="website" placeholder="https://..." <?= $isPromotorOnly ? 'required' : '' ?>>
                    <?php if ($isPromotorOnly): ?>
                    <small style="color: var(--color-text-secondary);">Obligatoriskt - logotypen länkas till denna adress</small>
                    <?php endif; ?>
                </div>

                <?php if (!$isPromotorOnly): ?>
                <div class="form-group">
                    <label class="form-label">Beskrivning</label>
                    <textarea class="form-textarea" id="sponsorDescription" name="description" rows="3"></textarea>
                </div>
                <?php endif; ?>

                <!-- Logo section - simplified -->
                <div style="background: var(--color-bg-sunken); padding: var(--space-md); border-radius: var(--radius-md); margin-bottom: var(--space-md);">
                    <h4 style="margin: 0 0 var(--space-md) 0; font-size: 0.9rem;">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm" style="display: inline; vertical-align: middle; margin-right: 4px;"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                        Logotyper
                    </h4>
                    <p style="font-size: 0.8rem; color: var(--color-text-secondary); margin-bottom: var(--space-md);">
                        Ladda upp logotyp direkt eller välj från mediabiblioteket.
                    </p>

                    <!-- Banner (1200x150) -->
                    <div class="form-group">
                        <label class="form-label">
                            Banner <code style="background: var(--color-bg); padding: 2px 6px; border-radius: 4px; font-size: 0.75rem;">1200×150px</code>
                        </label>
                        <div class="logo-picker">
                            <div class="logo-preview" id="logoBannerPreview" style="width: 200px; height: 25px;">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                            </div>
                            <input type="hidden" id="logoBannerId" name="logo_banner_id">
                            <input type="file" id="bannerUpload" accept="image/*" style="display:none" onchange="uploadLogoFile(this, 'banner')">
                            <button type="button" class="btn btn-sm btn-primary" onclick="document.getElementById('bannerUpload').click()">Ladda upp</button>
                            <button type="button" class="btn btn-sm btn-secondary" onclick="openMediaPicker('banner')">Välj från media</button>
                            <button type="button" class="btn btn-sm btn-ghost" onclick="clearLogoField('banner')">Ta bort</button>
                        </div>
                        <small class="text-secondary">Stor banner för event-sidan</small>
                    </div>

                    <!-- Logo (4:1 ratio - auto-scales) -->
                    <div class="form-group">
                        <label class="form-label">
                            Logo <code style="background: var(--color-bg); padding: 2px 6px; border-radius: 4px; font-size: 0.75rem;">600×150px</code>
                        </label>
                        <div class="logo-picker">
                            <div class="logo-preview" id="logoPreview" style="width: 120px; height: 30px;">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                            </div>
                            <input type="hidden" id="logoId" name="logo_media_id">
                            <input type="file" id="logoUpload" accept="image/*" style="display:none" onchange="uploadLogoFile(this, 'logo')">
                            <button type="button" class="btn btn-sm btn-primary" onclick="document.getElementById('logoUpload').click()">Ladda upp</button>
                            <button type="button" class="btn btn-sm btn-secondary" onclick="openMediaPicker('logo')">Välj från media</button>
                            <button type="button" class="btn btn-sm btn-ghost" onclick="clearLogoField('logo')">Ta bort</button>
                        </div>
                        <small class="text-secondary">Auto-skalas till 300×75, 240×60, 160×40</small>
                    </div>
                </div>

                <?php if (!$isPromotorOnly): ?>
                <hr style="margin: var(--space-lg) 0; border: none; border-top: 1px solid var(--color-border);">

                <h4 class="mb-md">Kontaktperson</h4>

                <div class="form-group">
                    <label class="form-label">Namn</label>
                    <input type="text" class="form-input" id="contactName" name="contact_name">
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">E-post</label>
                        <input type="email" class="form-input" id="contactEmail" name="contact_email">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Telefon</label>
                        <input type="tel" class="form-input" id="contactPhone" name="contact_phone">
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Sorteringsordning</label>
                    <input type="number" class="form-input" id="displayOrder" name="display_order" value="0" min="0">
                </div>
                <?php endif; ?>
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Avbryt</button>
                <button type="submit" class="btn btn-primary">Spara</button>
            </div>
        </form>
    </div>
</div>

<!-- Media Picker Modal -->
<div class="modal" id="mediaPickerModal">
    <div class="modal-content" style="max-width: 800px;">
        <div class="modal-header">
            <h3>Välj bild från Mediabiblioteket</h3>
            <button type="button" class="close-btn" onclick="closeMediaModal()">&times;</button>
        </div>
        <div class="modal-body" style="max-height: 60vh; overflow-y: auto;">
            <div id="mediaGrid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 12px;">
                <!-- Media items will be loaded here -->
            </div>
        </div>
        <div class="modal-footer">
            <a href="/admin/media.php?folder=sponsors" target="_blank" class="btn btn-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm" style="margin-right: 4px;"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>
                Öppna Mediabiblioteket
            </a>
            <button type="button" class="btn btn-ghost" onclick="closeMediaModal()">Avbryt</button>
        </div>
    </div>
</div>

<script>
let currentSponsorId = null;
let currentLogoField = null;
let mediaData = [];
const isPromotorOnly = <?= $isPromotorOnly ? 'true' : 'false' ?>;

function filterBySeries(seriesId) {
    const url = new URL(window.location.href);
    if (seriesId) {
        url.searchParams.set('series', seriesId);
    } else {
        url.searchParams.delete('series');
    }
    window.location.href = url.toString();
}

function openCreateModal() {
    currentSponsorId = null;
    document.getElementById('modalTitle').textContent = 'Ny sponsor';
    document.getElementById('sponsorForm').reset();
    document.getElementById('sponsorId').value = '';
    document.getElementById('sponsorTier').value = 'bronze';
    document.getElementById('sponsorActive').value = '1';
    document.querySelectorAll('.series-checkbox').forEach(cb => cb.checked = false);
    clearLogoField('banner');
    clearLogoField('logo');
    document.getElementById('sponsorModal').classList.add('active');
}

async function editSponsor(id) {
    try {
        const response = await fetch(`/api/sponsors.php?action=get&id=${id}`);
        const result = await response.json();

        if (!result.success) {
            alert(result.error);
            return;
        }

        const sponsor = result.data;
        currentSponsorId = id;

        document.getElementById('modalTitle').textContent = 'Redigera sponsor';
        document.getElementById('sponsorId').value = id;
        document.getElementById('sponsorName').value = sponsor.name || '';
        document.getElementById('sponsorTier').value = sponsor.tier || 'bronze';
        document.getElementById('sponsorActive').value = sponsor.active ? '1' : '0';
        document.getElementById('sponsorWebsite').value = sponsor.website || '';

        // These fields only exist for non-promotor users
        if (!isPromotorOnly) {
            document.getElementById('sponsorDescription').value = sponsor.description || '';
            document.getElementById('contactName').value = sponsor.contact_name || '';
            document.getElementById('contactEmail').value = sponsor.contact_email || '';
            document.getElementById('contactPhone').value = sponsor.contact_phone || '';
            document.getElementById('displayOrder').value = sponsor.display_order || 0;
        }

        // Set logo fields
        clearLogoField('banner');
        clearLogoField('logo');

        if (sponsor.logo_banner_id) {
            setLogoFieldById('banner', sponsor.logo_banner_id, sponsor.banner_logo_url);
        }
        if (sponsor.logo_media_id) {
            setLogoFieldById('logo', sponsor.logo_media_id, sponsor.logo_url);
        }

        // Fallback to legacy logo field
        if (!sponsor.logo_media_id && sponsor.logo) {
            const legacyUrl = '/uploads/sponsors/' + sponsor.logo;
            setLogoFieldByUrl('logo', legacyUrl);
        }

        document.querySelectorAll('.series-checkbox').forEach(cb => {
            cb.checked = sponsor.series_ids && sponsor.series_ids.includes(parseInt(cb.value));
        });

        document.getElementById('sponsorModal').classList.add('active');
    } catch (error) {
        console.error('Error loading sponsor:', error);
        alert('Kunde inte ladda sponsordata');
    }
}

function closeModal() {
    document.getElementById('sponsorModal').classList.remove('active');
    currentSponsorId = null;
}

function closeMediaModal() {
    document.getElementById('mediaPickerModal').classList.remove('active');
    currentLogoField = null;
}

async function saveSponsor(event) {
    event.preventDefault();

    const form = document.getElementById('sponsorForm');
    const formData = new FormData(form);

    const selectedSeries = [];
    document.querySelectorAll('.series-checkbox:checked').forEach(cb => {
        selectedSeries.push(parseInt(cb.value));
    });

    const data = {
        name: formData.get('name'),
        tier: formData.get('tier') || 'bronze',
        active: formData.get('active') === '1',
        website: formData.get('website') || null,
        description: isPromotorOnly ? null : (formData.get('description') || null),
        contact_name: isPromotorOnly ? null : (formData.get('contact_name') || null),
        contact_email: isPromotorOnly ? null : (formData.get('contact_email') || null),
        contact_phone: isPromotorOnly ? null : (formData.get('contact_phone') || null),
        display_order: isPromotorOnly ? 0 : (parseInt(formData.get('display_order')) || 0),
        logo_banner_id: formData.get('logo_banner_id') || null,
        logo_media_id: formData.get('logo_media_id') || null,
        series_ids: selectedSeries
    };

    try {
        let response;
        if (currentSponsorId) {
            data.id = currentSponsorId;
            response = await fetch('/api/sponsors.php?action=update', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch('/api/sponsors.php?action=create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        const result = await response.json();
        if (result.success) {
            closeModal();
            location.reload();
        } else {
            alert(result.error || 'Kunde inte spara');
        }
    } catch (error) {
        console.error('Error saving sponsor:', error);
        alert('Kunde inte spara');
    }
}

async function deleteSponsor(id, name) {
    if (!confirm(`Vill du radera sponsorn "${name}"?`)) return;

    try {
        const response = await fetch(`/api/sponsors.php?action=delete&id=${id}`, { method: 'DELETE' });
        const result = await response.json();
        if (result.success) {
            location.reload();
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Error deleting sponsor:', error);
        alert('Kunde inte radera');
    }
}

// Media picker functions
async function openMediaPicker(field) {
    currentLogoField = field;
    const modal = document.getElementById('mediaPickerModal');
    const grid = document.getElementById('mediaGrid');

    grid.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--color-text-secondary);">Laddar media...</div>';
    modal.classList.add('active');

    try {
        const response = await fetch('/api/media.php?action=list&folder=sponsors&limit=100');
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            mediaData = result.data;
            renderMediaGrid();
        } else {
            grid.innerHTML = `
                <div style="text-align: center; padding: 40px; color: var(--color-text-secondary);">
                    <p>Inga bilder i sponsormappen.</p>
                    <a href="/admin/media.php?folder=sponsors" target="_blank" class="btn btn-primary" style="margin-top: 16px;">
                        Gå till Mediabiblioteket
                    </a>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading media:', error);
        grid.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--color-danger);">Kunde inte ladda media</div>';
    }
}

function renderMediaGrid() {
    const grid = document.getElementById('mediaGrid');
    grid.innerHTML = mediaData.map(media => `
        <div class="media-item" onclick="selectMedia(${media.id}, '${media.filepath}')" style="cursor: pointer; border: 2px solid transparent; border-radius: 8px; padding: 8px; transition: border-color 0.2s;">
            <img src="/${media.filepath}" alt="${media.original_filename || ''}" style="width: 100%; height: 80px; object-fit: contain; background: var(--color-bg-sunken); border-radius: 4px;">
            <div style="font-size: 0.75rem; color: var(--color-text-secondary); margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                ${media.original_filename || 'Bild'}
            </div>
        </div>
    `).join('');
}

function selectMedia(mediaId, filepath) {
    if (!currentLogoField) return;

    const { previewId, inputId } = getLogoFieldIds(currentLogoField);

    document.getElementById(inputId).value = mediaId;
    document.getElementById(previewId).innerHTML = `<img src="/${filepath}" alt="Logo" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;

    closeMediaModal();
}

function setLogoFieldById(field, mediaId, url) {
    const { previewId, inputId } = getLogoFieldIds(field);

    document.getElementById(inputId).value = mediaId;
    if (url) {
        document.getElementById(previewId).innerHTML = `<img src="/${url.replace(/^\//, '')}" alt="Logo" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;
    }
}

function getLogoFieldIds(field) {
    // Special case for 'logo' field (not 'logoLogo')
    if (field === 'logo') {
        return { previewId: 'logoPreview', inputId: 'logoId' };
    }
    // Standard pattern for banner
    return {
        previewId: 'logo' + field.charAt(0).toUpperCase() + field.slice(1) + 'Preview',
        inputId: 'logo' + field.charAt(0).toUpperCase() + field.slice(1) + 'Id'
    };
}

// Direct upload for logo files
async function uploadLogoFile(input, field) {
    const file = input.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
        alert('Välj en bildfil (JPG, PNG, etc.)');
        return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        alert('Filen är för stor. Max 10MB.');
        return;
    }

    const { previewId } = getLogoFieldIds(field);
    const preview = document.getElementById(previewId);

    // Show loading state
    preview.innerHTML = '<span style="font-size: 10px;">Laddar upp...</span>';

    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('folder', 'sponsors');

        const response = await fetch('/api/media.php?action=upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success && result.media) {
            setLogoFieldById(field, result.media.id, result.media.filepath);
        } else {
            alert('Uppladdning misslyckades: ' + (result.error || 'Okänt fel'));
            preview.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>';
        }
    } catch (error) {
        console.error('Upload error:', error);
        alert('Ett fel uppstod vid uppladdning');
        preview.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>';
    }

    // Clear input so same file can be re-selected
    input.value = '';
}

function setLogoFieldByUrl(field, url) {
    const { previewId } = getLogoFieldIds(field);
    if (url) {
        document.getElementById(previewId).innerHTML = `<img src="${url}" alt="Logo" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;
    }
}

function clearLogoField(field) {
    const { previewId, inputId } = getLogoFieldIds(field);
    const preview = document.getElementById(previewId);
    const input = document.getElementById(inputId);

    if (input) input.value = '';
    if (preview) preview.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
    `;
}

// Check series selection and trigger file upload
function triggerUpload(inputId) {
    const seriesSelect = document.getElementById('uploadSeriesSelect');
    if (seriesSelect && !seriesSelect.value) {
        alert('Välj en serie innan du laddar upp filer.');
        seriesSelect.focus();
        return;
    }
    document.getElementById(inputId).click();
}

// Upload to specific folder with series association (for promotor upload section)
async function uploadToFolder(input, folder) {
    const file = input.files[0];
    if (!file) return;

    // Get selected series
    const seriesSelect = document.getElementById('uploadSeriesSelect');
    const seriesId = seriesSelect ? seriesSelect.value : null;
    const seriesName = seriesSelect ? seriesSelect.options[seriesSelect.selectedIndex].text : '';

    if (!seriesId) {
        alert('Välj en serie innan du laddar upp filer.');
        input.value = '';
        return;
    }

    if (!file.type.startsWith('image/')) {
        alert('Välj en bildfil (JPG, PNG, etc.)');
        input.value = '';
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert('Filen är för stor. Max 10MB.');
        input.value = '';
        return;
    }

    // Show uploading state
    const uploadBox = input.parentElement;
    const originalContent = uploadBox.innerHTML;
    uploadBox.innerHTML = '<span style="color: var(--color-text-secondary);">Laddar upp...</span>' +
        '<input type="file" style="display:none">';

    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('folder', folder);
        formData.append('series_id', seriesId);

        const response = await fetch('/api/media.php?action=upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success && result.media) {
            // Show success and add to recent uploads
            uploadBox.innerHTML = originalContent;
            showRecentUpload(result.media);
            alert('Uppladdning lyckades!\nFil: ' + file.name + '\nSerie: ' + seriesName + '\nMapp: ' + folder);
        } else {
            uploadBox.innerHTML = originalContent;
            alert('Uppladdning misslyckades: ' + (result.error || 'Okänt fel'));
        }
    } catch (error) {
        console.error('Upload error:', error);
        uploadBox.innerHTML = originalContent;
        alert('Ett fel uppstod vid uppladdning');
    }

    input.value = '';
}

function showRecentUpload(media) {
    const gallery = document.getElementById('recentUploads');
    if (!gallery) return;

    gallery.style.display = 'grid';

    const item = document.createElement('div');
    item.className = 'upload-gallery-item' + (media.filepath.includes('logo') ? ' logo' : '');
    item.innerHTML = `
        <img src="/${media.filepath}" alt="${media.original_filename || 'Uploaded image'}">
    `;
    gallery.insertBefore(item, gallery.firstChild);
}

// Close modals on escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
        closeMediaModal();
    }
});

document.getElementById('sponsorModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('sponsorModal')) closeModal();
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
