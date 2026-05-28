<?php
/**
 * API: Load More News Posts (for infinite scroll)
 * GET /api/news/load-more.php
 */

header('Content-Type: application/json');

require_once __DIR__ . '/../../hub-config.php';

$pdo = hub_db();

// Include RaceReportManager
require_once HUB_ROOT . '/includes/RaceReportManager.php';
$reportManager = new RaceReportManager($pdo);

// Get filter parameters
$page = max(1, intval($_GET['page'] ?? 1));
$perPage = 12;
$filterTag = $_GET['tag'] ?? null;
$filterType = $_GET['type'] ?? null;
$filterEvent = $_GET['event'] ?? null;
$filterRider = $_GET['rider'] ?? null;
$sortBy = $_GET['sort'] ?? 'recent';

// Build filters
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

// Get reports
$result = $reportManager->listReports($filters);
$reports = $result['reports'];
$hasMore = $page < $result['total_pages'];

// Generate HTML for each report card
$html = '';
foreach ($reports as $report) {
    $html .= renderNewsCard($report);
}

echo json_encode([
    'success' => true,
    'html' => $html,
    'hasMore' => $hasMore,
    'page' => $page,
    'totalPages' => $result['total_pages']
]);

/**
 * Render a news card HTML
 */
function renderNewsCard($report) {
    $slug = htmlspecialchars($report['slug']);
    $title = htmlspecialchars($report['title']);
    $author = htmlspecialchars($report['firstname'] . ' ' . substr($report['lastname'], 0, 1) . '.');
    $image = htmlspecialchars($report['featured_image'] ?? '');
    $youtubeId = htmlspecialchars($report['youtube_video_id'] ?? '');
    $eventName = htmlspecialchars($report['event_name'] ?? '');
    $views = formatNumber($report['views']);
    $likes = formatNumber($report['likes']);
    $readTime = $report['reading_time_minutes'];
    $timeAgo = timeAgo($report['published_at']);

    $imageHtml = '';
    if ($image) {
        $imageHtml = '<img src="' . $image . '" alt="' . $title . '" loading="lazy">';
    } elseif ($youtubeId) {
        $imageHtml = '<img src="https://img.youtube.com/vi/' . $youtubeId . '/hqdefault.jpg" alt="' . $title . '" loading="lazy">';
    } else {
        $imageHtml = '<div class="news-card-placeholder"><i data-lucide="image"></i></div>';
    }

    $playIcon = $report['is_from_youtube'] ? '<div class="news-card-play"><i data-lucide="play"></i></div>' : '';
    $instagramBadge = $report['is_from_instagram'] ? '<div class="news-card-badge news-card-badge-instagram"><i data-lucide="instagram"></i></div>' : '';
    $eventBadge = $eventName ? '<div class="news-card-event"><i data-lucide="flag"></i>' . $eventName . '</div>' : '';

    $tagsHtml = '';
    foreach (array_slice($report['tags'] ?? [], 0, 2) as $tag) {
        $tagColor = htmlspecialchars($tag['color'] ?? '#37d4d6');
        $tagName = htmlspecialchars($tag['name']);
        $tagsHtml .= '<span class="news-tag news-tag-sm" style="--tag-color: ' . $tagColor . '">' . $tagName . '</span>';
    }

    return <<<HTML
<a href="/news/{$slug}" class="news-card">
    <div class="news-card-image">
        {$imageHtml}
        {$playIcon}
        {$instagramBadge}
        {$eventBadge}
    </div>
    <div class="news-card-content">
        <div class="news-card-tags">{$tagsHtml}</div>
        <h3 class="news-card-title">{$title}</h3>
        <div class="news-card-meta">
            <span class="news-meta-author">{$author}</span>
            <span class="news-meta-dot">·</span>
            <span class="news-meta-time">{$timeAgo}</span>
        </div>
        <div class="news-card-stats">
            <span><i data-lucide="eye"></i> {$views}</span>
            <span><i data-lucide="heart"></i> {$likes}</span>
            <span><i data-lucide="clock"></i> {$readTime} min</span>
        </div>
    </div>
</a>
HTML;
}

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
