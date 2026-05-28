<?php
/**
 * TheHUB V1.0 - News Hub
 * Feber.se-inspired news page for race reports, videos, and photos
 */

// Prevent direct access
if (!defined('HUB_ROOT')) {
    header('Location: /news');
    exit;
}

// Define page type for sponsor placements
define('HUB_PAGE_TYPE', 'news');

$pdo = hub_db();

// Include RaceReportManager
require_once HUB_ROOT . '/includes/RaceReportManager.php';
$reportManager = new RaceReportManager($pdo);

// Get filter parameters
$page = max(1, intval($_GET['page'] ?? 1));
$perPage = 12;
$filterTag = $_GET['tag'] ?? null;
$filterType = $_GET['type'] ?? null;
$filterDiscipline = $_GET['discipline'] ?? null;
$filterEvent = $_GET['event'] ?? null;
$filterRider = $_GET['rider'] ?? null;
$sortBy = $_GET['sort'] ?? 'recent';
$searchQuery = trim($_GET['q'] ?? '');

// Build filters for listReports
$filters = [
    'page' => $page,
    'per_page' => $perPage,
    'order_by' => $sortBy
];

if ($filterTag) {
    $filters['tag'] = $filterTag;
}

if ($filterEvent && is_numeric($filterEvent)) {
    $filters['event_id'] = (int)$filterEvent;
}

if ($filterRider && is_numeric($filterRider)) {
    $filters['rider_id'] = (int)$filterRider;
}

if ($searchQuery) {
    $filters['search'] = $searchQuery;
}

// Get reports
$result = $reportManager->listReports($filters);
$reports = $result['reports'];
$totalReports = $result['total'];
$totalPages = $result['total_pages'];

// Get featured report (if on first page and no filters)
$featuredReport = null;
if ($page === 1 && !$filterTag && !$filterType && !$searchQuery) {
    $featuredResult = $reportManager->listReports([
        'featured' => true,
        'per_page' => 1
    ]);
    if (!empty($featuredResult['reports'])) {
        $featuredReport = $featuredResult['reports'][0];
        // Remove from main list if present
        // PHP 5.x/7.x compatible
        $featuredId = $featuredReport['id'];
        $reports = array_filter($reports, function($r) use ($featuredId) { return $r['id'] !== $featuredId; });
    }
}

// Get all tags for filter
$allTags = $reportManager->getAllTags();

// Get disciplines for filter
$disciplines = [
    'enduro' => ['name' => 'Enduro', 'color' => '#FFE009'],
    'downhill' => ['name' => 'Downhill', 'color' => '#FF6B35'],
    'xc' => ['name' => 'XC', 'color' => '#2E7D32'],
    'gravel' => ['name' => 'Gravel', 'color' => '#795548'],
    'dual' => ['name' => 'Dual Slalom', 'color' => '#E91E63']
];

// Get recent events for sidebar
$recentEvents = [];
try {
    $stmt = $pdo->query("
        SELECT e.id, e.name, e.date, COUNT(rr.id) as report_count
        FROM events e
        INNER JOIN race_reports rr ON e.id = rr.event_id
        WHERE rr.status = 'published'
        GROUP BY e.id
        ORDER BY e.date DESC
        LIMIT 5
    ");
    $recentEvents = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Ignore
}

// Page title
$pageTitle = 'Nyheter';
if ($filterTag) {
    $pageTitle = 'Nyheter: #' . htmlspecialchars($filterTag);
}

// Current user for likes
$currentUser = function_exists('hub_current_user') ? hub_current_user() : null;
?>

<link rel="stylesheet" href="/assets/css/pages/news.css?v=<?= filemtime(HUB_ROOT . '/assets/css/pages/news.css') ?>">

<div class="page-header">
    <h1 class="page-title">
        <i data-lucide="newspaper" class="page-icon"></i>
        <?= $pageTitle ?>
    </h1>
    <p class="page-subtitle">Race reports, foton och videos fran communityn</p>
</div>

<!-- Global Sponsor: Header Banner -->
<?= render_global_sponsors('news', 'header_banner', '') ?>

<!-- Filter Bar -->
<div class="news-filter-bar">
    <div class="news-filter-scroll">
        <a href="/news" class="news-filter-chip <?= !$filterTag && !$filterType && !$filterDiscipline ? 'active' : '' ?>">
            <i data-lucide="layers"></i>
            Alla
        </a>

        <span class="news-filter-divider"></span>

        <?php foreach ($disciplines as $slug => $disc): ?>
        <a href="/news?discipline=<?= $slug ?>" class="news-filter-chip <?= $filterDiscipline === $slug ? 'active' : '' ?>" style="--chip-color: <?= $disc['color'] ?>">
            <?= htmlspecialchars($disc['name']) ?>
        </a>
        <?php endforeach; ?>

        <span class="news-filter-divider"></span>

        <a href="/news?type=photo_gallery" class="news-filter-chip <?= $filterType === 'photo_gallery' ? 'active' : '' ?>">
            <i data-lucide="camera"></i>
            Foton
        </a>
        <a href="/news?type=video" class="news-filter-chip <?= $filterType === 'video' ? 'active' : '' ?>">
            <i data-lucide="play"></i>
            Videos
        </a>
    </div>

    <div class="news-filter-actions">
        <div class="news-search">
            <form action="/news" method="GET" class="news-search-form">
                <input type="text" name="q" value="<?= htmlspecialchars($searchQuery) ?>" placeholder="Sok..." class="news-search-input">
                <button type="submit" class="news-search-btn">
                    <i data-lucide="search"></i>
                </button>
            </form>
        </div>
        <select class="news-sort-select" onchange="location.href='/news?sort='+this.value">
            <option value="recent" <?= $sortBy === 'recent' ? 'selected' : '' ?>>Senaste</option>
            <option value="popular" <?= $sortBy === 'popular' ? 'selected' : '' ?>>Mest lasta</option>
            <option value="liked" <?= $sortBy === 'liked' ? 'selected' : '' ?>>Mest gillade</option>
        </select>
    </div>
</div>

<div class="news-layout">
    <!-- Main Content -->
    <div class="news-main">
        <?php if (empty($reports) && !$featuredReport): ?>
            <div class="news-empty">
                <div class="news-empty-icon">
                    <i data-lucide="file-text"></i>
                </div>
                <h2>Inga nyheter hittades</h2>
                <p>Det finns inga publicerade nyheter just nu<?= $searchQuery ? ' som matchar "' . htmlspecialchars($searchQuery) . '"' : '' ?>.</p>
                <?php if ($currentUser): ?>
                <a href="/profile/race-reports" class="btn btn-primary mt-md">
                    <i data-lucide="plus"></i>
                    Skriv den forsta!
                </a>
                <?php endif; ?>
            </div>
        <?php else: ?>
            <!-- Featured Post (First Page Only) -->
            <?php if ($featuredReport): ?>
            <a href="/news/<?= htmlspecialchars($featuredReport['slug']) ?>" class="news-featured">
                <div class="news-featured-image">
                    <?php if ($featuredReport['featured_image']): ?>
                    <img src="<?= htmlspecialchars($featuredReport['featured_image']) ?>" alt="<?= htmlspecialchars($featuredReport['title']) ?>" loading="lazy">
                    <?php elseif ($featuredReport['youtube_video_id']): ?>
                    <img src="https://img.youtube.com/vi/<?= htmlspecialchars($featuredReport['youtube_video_id']) ?>/maxresdefault.jpg" alt="<?= htmlspecialchars($featuredReport['title']) ?>" loading="lazy">
                    <?php else: ?>
                    <div class="news-featured-placeholder">
                        <i data-lucide="image"></i>
                    </div>
                    <?php endif; ?>
                    <?php if ($featuredReport['is_from_youtube']): ?>
                    <div class="news-featured-play">
                        <i data-lucide="play"></i>
                    </div>
                    <?php endif; ?>
                    <span class="news-featured-badge">
                        <i data-lucide="star"></i>
                        Utvalt
                    </span>
                </div>
                <div class="news-featured-content">
                    <div class="news-featured-tags">
                        <?php foreach (array_slice($featuredReport['tags'] ?? [], 0, 3) as $tag): ?>
                        <span class="news-tag" style="--tag-color: <?= htmlspecialchars($tag['color'] ?? '#37d4d6') ?>"><?= htmlspecialchars($tag['name']) ?></span>
                        <?php endforeach; ?>
                    </div>
                    <h2 class="news-featured-title"><?= htmlspecialchars($featuredReport['title']) ?></h2>
                    <p class="news-featured-excerpt"><?= htmlspecialchars($featuredReport['excerpt'] ?? '') ?></p>
                    <div class="news-featured-meta">
                        <span class="news-meta-author">
                            <i data-lucide="user"></i>
                            <?= htmlspecialchars($featuredReport['firstname'] ? $featuredReport['firstname'] . ' ' . $featuredReport['lastname'] : 'TheHUB') ?>
                        </span>
                        <span class="news-meta-date">
                            <i data-lucide="calendar"></i>
                            <?= date('j M Y', strtotime($featuredReport['published_at'])) ?>
                        </span>
                        <span class="news-meta-stats">
                            <span><i data-lucide="eye"></i> <?= number_format($featuredReport['views']) ?></span>
                            <span><i data-lucide="heart"></i> <?= number_format($featuredReport['likes']) ?></span>
                        </span>
                    </div>
                </div>
            </a>
            <?php endif; ?>

            <!-- News Grid -->
            <div class="news-grid">
                <?php
                $adFrequency = 4; // Show ad every 4 posts
                $postIndex = 0;
                foreach ($reports as $report):
                    $postIndex++;

                    // Insert ad every N posts
                    if ($postIndex > 1 && ($postIndex - 1) % $adFrequency === 0):
                ?>
                <div class="news-ad-slot">
                    <?= render_global_sponsors('news', 'content_mid', '') ?>
                </div>
                <?php endif; ?>

                <a href="/news/<?= htmlspecialchars($report['slug']) ?>" class="news-card">
                    <div class="news-card-image">
                        <?php if ($report['featured_image']): ?>
                        <img src="<?= htmlspecialchars($report['featured_image']) ?>" alt="<?= htmlspecialchars($report['title']) ?>" loading="lazy">
                        <?php elseif ($report['youtube_video_id']): ?>
                        <img src="https://img.youtube.com/vi/<?= htmlspecialchars($report['youtube_video_id']) ?>/hqdefault.jpg" alt="<?= htmlspecialchars($report['title']) ?>" loading="lazy">
                        <?php else: ?>
                        <div class="news-card-placeholder">
                            <i data-lucide="image"></i>
                        </div>
                        <?php endif; ?>

                        <?php if ($report['is_from_youtube']): ?>
                        <div class="news-card-play">
                            <i data-lucide="play"></i>
                        </div>
                        <?php endif; ?>

                        <?php if ($report['is_from_instagram']): ?>
                        <div class="news-card-badge news-card-badge-instagram">
                            <i data-lucide="instagram"></i>
                        </div>
                        <?php endif; ?>

                        <?php if ($report['event_name']): ?>
                        <div class="news-card-event">
                            <i data-lucide="flag"></i>
                            <?= htmlspecialchars($report['event_name']) ?>
                        </div>
                        <?php endif; ?>
                    </div>

                    <div class="news-card-content">
                        <div class="news-card-tags">
                            <?php foreach (array_slice($report['tags'] ?? [], 0, 2) as $tag): ?>
                            <span class="news-tag news-tag-sm" style="--tag-color: <?= htmlspecialchars($tag['color'] ?? '#37d4d6') ?>"><?= htmlspecialchars($tag['name']) ?></span>
                            <?php endforeach; ?>
                        </div>

                        <h3 class="news-card-title"><?= htmlspecialchars($report['title']) ?></h3>

                        <div class="news-card-meta">
                            <span class="news-meta-author">
                                <?= htmlspecialchars($report['firstname'] ? $report['firstname'] . ' ' . substr($report['lastname'] ?? '', 0, 1) . '.' : 'TheHUB') ?>
                            </span>
                            <span class="news-meta-dot">·</span>
                            <span class="news-meta-time">
                                <?= timeAgo($report['published_at']) ?>
                            </span>
                        </div>

                        <div class="news-card-stats">
                            <span><i data-lucide="eye"></i> <?= formatNumber($report['views']) ?></span>
                            <span><i data-lucide="heart"></i> <?= formatNumber($report['likes']) ?></span>
                            <span><i data-lucide="clock"></i> <?= $report['reading_time_minutes'] ?> min</span>
                        </div>
                    </div>
                </a>
                <?php endforeach; ?>
            </div>

            <!-- Pagination -->
            <?php if ($totalPages > 1): ?>
            <div class="news-pagination">
                <?php if ($page > 1): ?>
                <a href="?page=<?= $page - 1 ?><?= $filterTag ? '&tag=' . urlencode($filterTag) : '' ?><?= $sortBy !== 'recent' ? '&sort=' . $sortBy : '' ?>" class="news-pagination-btn">
                    <i data-lucide="chevron-left"></i>
                    Foregaende
                </a>
                <?php endif; ?>

                <div class="news-pagination-info">
                    Sida <?= $page ?> av <?= $totalPages ?>
                </div>

                <?php if ($page < $totalPages): ?>
                <a href="?page=<?= $page + 1 ?><?= $filterTag ? '&tag=' . urlencode($filterTag) : '' ?><?= $sortBy !== 'recent' ? '&sort=' . $sortBy : '' ?>" class="news-pagination-btn">
                    Nasta
                    <i data-lucide="chevron-right"></i>
                </a>
                <?php endif; ?>
            </div>
            <?php endif; ?>

            <!-- Load More Button (Alternative to Pagination) -->
            <?php if ($page < $totalPages): ?>
            <div class="news-load-more">
                <button class="btn btn-secondary btn-lg" id="loadMoreBtn" data-page="<?= $page + 1 ?>">
                    <i data-lucide="plus"></i>
                    Ladda fler
                </button>
            </div>
            <?php endif; ?>
        <?php endif; ?>
    </div>

    <!-- Sidebar -->
    <aside class="news-sidebar">
        <!-- Write CTA -->
        <?php if ($currentUser): ?>
        <div class="news-sidebar-cta">
            <div class="news-sidebar-cta-icon">
                <i data-lucide="pen-tool"></i>
            </div>
            <h3>Dela din story</h3>
            <p>Skriv om din senaste tavling och dela med communityn!</p>
            <a href="/profile/race-reports" class="btn btn-primary btn-block">
                <i data-lucide="plus"></i>
                Skriv Race Report
            </a>
        </div>
        <?php else: ?>
        <div class="news-sidebar-cta">
            <div class="news-sidebar-cta-icon">
                <i data-lucide="user-plus"></i>
            </div>
            <h3>Bli en del av communityn</h3>
            <p>Logga in for att skriva egna race reports och interagera med andra.</p>
            <a href="/login?redirect=/profile/race-reports" class="btn btn-primary btn-block">
                <i data-lucide="log-in"></i>
                Logga in
            </a>
        </div>
        <?php endif; ?>

        <!-- Sponsor Sidebar Top -->
        <?= render_global_sponsors('news', 'sidebar_top', '') ?>

        <!-- Popular Tags -->
        <?php if (!empty($allTags)): ?>
        <div class="news-sidebar-section">
            <h3 class="news-sidebar-title">
                <i data-lucide="hash"></i>
                Populara taggar
            </h3>
            <div class="news-tags-cloud">
                <?php foreach (array_slice($allTags, 0, 12) as $tag): ?>
                <a href="/news?tag=<?= htmlspecialchars($tag['slug']) ?>" class="news-tag-link <?= $filterTag === $tag['slug'] ? 'active' : '' ?>">
                    #<?= htmlspecialchars($tag['name']) ?>
                    <span class="news-tag-count"><?= $tag['usage_count'] ?></span>
                </a>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endif; ?>

        <!-- Sponsor Sidebar Mid -->
        <?= render_global_sponsors('news', 'sidebar_mid', '') ?>

        <!-- Recent Events with Reports -->
        <?php if (!empty($recentEvents)): ?>
        <div class="news-sidebar-section">
            <h3 class="news-sidebar-title">
                <i data-lucide="flag"></i>
                Senaste tavlingar
            </h3>
            <ul class="news-event-list">
                <?php foreach ($recentEvents as $event): ?>
                <li>
                    <a href="/news?event=<?= $event['id'] ?>" class="news-event-link">
                        <span class="news-event-name"><?= htmlspecialchars($event['name']) ?></span>
                        <span class="news-event-meta">
                            <span class="news-event-date"><?= date('j M', strtotime($event['date'])) ?></span>
                            <span class="news-event-count"><?= $event['report_count'] ?> inlagg</span>
                        </span>
                    </a>
                </li>
                <?php endforeach; ?>
            </ul>
        </div>
        <?php endif; ?>

        <!-- Google Ads Placeholder -->
        <div class="news-sidebar-ad" id="google-ad-sidebar">
            <!-- Google AdSense placeholder -->
            <div class="news-ad-placeholder">
                <span>Annons</span>
            </div>
        </div>
    </aside>
</div>

<!-- Global Sponsor: Content Bottom -->
<?= render_global_sponsors('news', 'content_bottom', 'Tack till vara partners') ?>

<?php
// Helper functions
function timeAgo($datetime) {
    $time = strtotime($datetime);
    $diff = time() - $time;

    if ($diff < 60) return 'Just nu';
    if ($diff < 3600) return floor($diff / 60) . ' min';
    if ($diff < 86400) return floor($diff / 3600) . ' tim';
    if ($diff < 604800) return floor($diff / 86400) . ' dagar';
    return date('j M', $time);
}

function formatNumber($num) {
    if ($num >= 1000000) return round($num / 1000000, 1) . 'M';
    if ($num >= 1000) return round($num / 1000, 1) . 'k';
    return $num;
}
?>

<script>
// Load more functionality
document.getElementById('loadMoreBtn')?.addEventListener('click', async function() {
    const btn = this;
    const page = parseInt(btn.dataset.page);
    btn.disabled = true;
    btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Laddar...';

    try {
        const params = new URLSearchParams(window.location.search);
        params.set('page', page);
        params.set('ajax', '1');

        const response = await fetch('/api/news/load-more.php?' + params.toString());
        const data = await response.json();

        if (data.html) {
            const grid = document.querySelector('.news-grid');
            grid.insertAdjacentHTML('beforeend', data.html);

            if (data.hasMore) {
                btn.dataset.page = page + 1;
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="plus"></i> Ladda fler';
            } else {
                btn.parentElement.remove();
            }

            // Re-init Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    } catch (e) {
        console.error('Load more failed:', e);
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="alert-circle"></i> Forsok igen';
    }
});
</script>
