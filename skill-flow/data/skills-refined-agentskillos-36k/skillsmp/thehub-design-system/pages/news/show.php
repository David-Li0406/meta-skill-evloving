<?php
/**
 * TheHUB V1.0 - News Article View
 * Individual race report/news article page
 */

// Prevent direct access
if (!defined('HUB_ROOT')) {
    header('Location: /news');
    exit;
}

// Define page type for sponsor placements
define('HUB_PAGE_TYPE', 'news_single');

$pdo = hub_db();

// Include RaceReportManager
require_once HUB_ROOT . '/includes/RaceReportManager.php';
$reportManager = new RaceReportManager($pdo);

// Get the slug from URL
$slug = $pageInfo['params']['slug'] ?? $pageInfo['params']['id'] ?? null;

if (!$slug) {
    header('Location: /news');
    exit;
}

// Get the report
$report = $reportManager->getReport($slug, true); // true = published only

if (!$report) {
    // Try to find by ID if numeric
    if (is_numeric($slug)) {
        $report = $reportManager->getReport((int)$slug, true);
    }

    if (!$report) {
        http_response_code(404);
        include HUB_ROOT . '/pages/404.php';
        return;
    }
}

// Current user for likes/comments
$currentUser = function_exists('hub_current_user') ? hub_current_user() : null;
$hasLiked = $currentUser ? $reportManager->hasLiked($report['id'], $currentUser['id']) : false;

// Get comments
$comments = $reportManager->getComments($report['id']);

// Get related reports (same event or same tags)
$relatedReports = [];
try {
    $tagIds = array_column($report['tags'] ?? [], 'id');
    $tagPlaceholders = !empty($tagIds) ? implode(',', array_fill(0, count($tagIds), '?')) : '0';

    $sql = "SELECT DISTINCT rr.*, r.firstname, r.lastname
            FROM race_reports rr
            INNER JOIN riders r ON rr.rider_id = r.id
            LEFT JOIN race_report_tag_relations rrtr ON rr.id = rrtr.report_id
            WHERE rr.id != ?
            AND rr.status = 'published'
            AND (
                rr.event_id = ?
                OR rrtr.tag_id IN ({$tagPlaceholders})
            )
            ORDER BY rr.published_at DESC
            LIMIT 4";

    $params = array_merge([$report['id'], $report['event_id'] ?: 0], $tagIds);
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $relatedReports = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Ignore
}

// Page title for SEO
$pageTitle = $report['title'];
$pageDescription = $report['meta_description'] ?? $report['excerpt'] ?? substr(strip_tags($report['content']), 0, 160);

// Author info
$authorName = $report['firstname'] ? $report['firstname'] . ' ' . $report['lastname'] : 'TheHUB';
$authorInitials = $report['firstname'] ? strtoupper(substr($report['firstname'], 0, 1) . substr($report['lastname'] ?? '', 0, 1)) : 'TH';

// Time helpers
function formatPublishDate($datetime) {
    $time = strtotime($datetime);
    $now = time();
    $diff = $now - $time;

    if ($diff < 86400) {
        return 'Idag ' . date('H:i', $time);
    } elseif ($diff < 172800) {
        return 'Igar ' . date('H:i', $time);
    }
    return date('j F Y', $time);
}
?>

<link rel="stylesheet" href="/assets/css/pages/news.css?v=<?= filemtime(HUB_ROOT . '/assets/css/pages/news.css') ?>">

<!-- Global Sponsor: Header Banner -->
<?= render_global_sponsors('news_single', 'header_banner', '') ?>

<article class="news-article">
    <!-- Article Header -->
    <header class="news-article-header">
        <!-- Breadcrumb -->
        <nav class="news-breadcrumb">
            <a href="/news">Nyheter</a>
            <?php if ($report['event_name']): ?>
            <span class="news-breadcrumb-sep"><i data-lucide="chevron-right"></i></span>
            <a href="/news?event=<?= $report['event_id'] ?>"><?= htmlspecialchars($report['event_name']) ?></a>
            <?php endif; ?>
            <?php if (!empty($report['tags'])): ?>
            <span class="news-breadcrumb-sep"><i data-lucide="chevron-right"></i></span>
            <a href="/news?tag=<?= htmlspecialchars($report['tags'][0]['slug']) ?>"><?= htmlspecialchars($report['tags'][0]['name']) ?></a>
            <?php endif; ?>
        </nav>

        <!-- Tags -->
        <div class="news-article-tags">
            <?php foreach ($report['tags'] ?? [] as $tag): ?>
            <a href="/news?tag=<?= htmlspecialchars($tag['slug']) ?>" class="news-tag" style="--tag-color: <?= htmlspecialchars($tag['color'] ?? '#37d4d6') ?>">
                <?php if ($tag['icon']): ?><i data-lucide="<?= htmlspecialchars($tag['icon']) ?>"></i><?php endif; ?>
                <?= htmlspecialchars($tag['name']) ?>
            </a>
            <?php endforeach; ?>
        </div>

        <!-- Title -->
        <h1 class="news-article-title"><?= htmlspecialchars($report['title']) ?></h1>

        <!-- Meta -->
        <div class="news-article-meta">
            <?php if ($report['rider_id']): ?>
            <a href="/rider/<?= $report['rider_id'] ?>" class="news-article-author">
            <?php else: ?>
            <span class="news-article-author">
            <?php endif; ?>
                <div class="news-article-author-avatar">
                    <?= $authorInitials ?>
                </div>
                <div class="news-article-author-info">
                    <span class="news-article-author-name"><?= htmlspecialchars($authorName) ?></span>
                    <?php if ($report['club_name']): ?>
                    <span class="news-article-author-club"><?= htmlspecialchars($report['club_name']) ?></span>
                    <?php endif; ?>
                </div>
            <?php if ($report['rider_id']): ?>
            </a>
            <?php else: ?>
            </span>
            <?php endif; ?>

            <div class="news-article-meta-sep"></div>

            <div class="news-article-meta-item">
                <i data-lucide="calendar"></i>
                <span><?= formatPublishDate($report['published_at']) ?></span>
            </div>

            <div class="news-article-meta-item">
                <i data-lucide="clock"></i>
                <span><?= $report['reading_time_minutes'] ?> min lasning</span>
            </div>

            <div class="news-article-meta-item">
                <i data-lucide="eye"></i>
                <span><?= number_format($report['views']) ?> visningar</span>
            </div>
        </div>
    </header>

    <div class="news-article-layout">
        <!-- Main Content -->
        <div class="news-article-main">
            <!-- Featured Image / Video -->
            <?php if ($report['is_from_youtube'] && $report['youtube_video_id']): ?>
            <div class="news-article-video">
                <div class="news-video-wrapper">
                    <iframe
                        src="https://www.youtube.com/embed/<?= htmlspecialchars($report['youtube_video_id']) ?>"
                        title="<?= htmlspecialchars($report['title']) ?>"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen>
                    </iframe>
                </div>
            </div>
            <?php elseif ($report['is_from_instagram'] && $report['instagram_url']): ?>
            <div class="news-article-instagram">
                <blockquote class="instagram-media" data-instgrm-captioned data-instgrm-permalink="<?= htmlspecialchars($report['instagram_url']) ?>" data-instgrm-version="14"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
            </div>
            <?php elseif ($report['featured_image']): ?>
            <figure class="news-article-hero">
                <img src="<?= htmlspecialchars($report['featured_image']) ?>" alt="<?= htmlspecialchars($report['title']) ?>">
            </figure>
            <?php endif; ?>

            <!-- Global Sponsor: Content Top -->
            <?= render_global_sponsors('news_single', 'content_top', '') ?>

            <!-- Article Content -->
            <div class="news-article-content">
                <?= nl2br(htmlspecialchars($report['content'])) ?>
            </div>

            <!-- Event Link -->
            <?php if ($report['event_id'] && $report['event_name']): ?>
            <div class="news-article-event-link">
                <a href="/event/<?= $report['event_id'] ?>" class="news-event-card">
                    <div class="news-event-card-icon">
                        <i data-lucide="flag"></i>
                    </div>
                    <div class="news-event-card-info">
                        <span class="news-event-card-label">Fran tavlingen</span>
                        <span class="news-event-card-name"><?= htmlspecialchars($report['event_name']) ?></span>
                        <?php if ($report['event_date']): ?>
                        <span class="news-event-card-date"><?= date('j F Y', strtotime($report['event_date'])) ?></span>
                        <?php endif; ?>
                    </div>
                    <div class="news-event-card-arrow">
                        <i data-lucide="arrow-right"></i>
                    </div>
                </a>
            </div>
            <?php endif; ?>

            <!-- Actions (Like, Share) -->
            <div class="news-article-actions">
                <button class="news-action-btn <?= $hasLiked ? 'liked' : '' ?>" id="likeBtn" data-report-id="<?= $report['id'] ?>">
                    <i data-lucide="heart" <?= $hasLiked ? 'fill="currentColor"' : '' ?>></i>
                    <span id="likeCount"><?= number_format($report['likes']) ?></span>
                </button>

                <button class="news-action-btn" onclick="shareArticle()">
                    <i data-lucide="share-2"></i>
                    <span>Dela</span>
                </button>

                <?php if ($currentUser && $currentUser['id'] == $report['rider_id']): ?>
                <a href="/profile/race-reports?edit=<?= $report['id'] ?>" class="news-action-btn">
                    <i data-lucide="edit-2"></i>
                    <span>Redigera</span>
                </a>
                <?php endif; ?>
            </div>

            <!-- Global Sponsor: Content Mid -->
            <?= render_global_sponsors('news_single', 'content_mid', '') ?>

            <!-- Comments Section -->
            <?php if ($report['allow_comments']): ?>
            <section class="news-comments" id="comments">
                <h2 class="news-comments-title">
                    <i data-lucide="message-square"></i>
                    Kommentarer (<?= count($comments) ?>)
                </h2>

                <?php if ($currentUser): ?>
                <form class="news-comment-form" id="commentForm" data-report-id="<?= $report['id'] ?>">
                    <textarea name="comment" class="news-comment-input" placeholder="Skriv en kommentar..." rows="3" required></textarea>
                    <button type="submit" class="btn btn-primary">
                        <i data-lucide="send"></i>
                        Skicka
                    </button>
                </form>
                <?php else: ?>
                <div class="news-comment-login">
                    <p><a href="/login?redirect=/news/<?= htmlspecialchars($report['slug']) ?>#comments">Logga in</a> for att kommentera.</p>
                </div>
                <?php endif; ?>

                <?php if (!empty($comments)): ?>
                <div class="news-comment-list">
                    <?php foreach ($comments as $comment): ?>
                    <div class="news-comment">
                        <div class="news-comment-avatar">
                            <?= strtoupper(substr($comment['firstname'] ?? 'A', 0, 1)) ?>
                        </div>
                        <div class="news-comment-content">
                            <div class="news-comment-header">
                                <span class="news-comment-author">
                                    <?= htmlspecialchars(($comment['firstname'] ?? 'Anonym') . ' ' . ($comment['lastname'] ?? '')) ?>
                                </span>
                                <span class="news-comment-date">
                                    <?= date('j M Y H:i', strtotime($comment['created_at'])) ?>
                                </span>
                            </div>
                            <p class="news-comment-text"><?= nl2br(htmlspecialchars($comment['comment_text'])) ?></p>
                        </div>
                    </div>
                    <?php endforeach; ?>
                </div>
                <?php elseif (empty($comments)): ?>
                <div class="news-comments-empty">
                    <i data-lucide="message-circle"></i>
                    <p>Inga kommentarer an. Bli forst att kommentera!</p>
                </div>
                <?php endif; ?>
            </section>
            <?php endif; ?>

            <!-- Global Sponsor: Content Bottom -->
            <?= render_global_sponsors('news_single', 'content_bottom', '') ?>
        </div>

        <!-- Sidebar -->
        <aside class="news-article-sidebar">
            <!-- Sponsor Sidebar Top -->
            <?= render_global_sponsors('news_single', 'sidebar_top', '') ?>

            <!-- Author Card -->
            <div class="news-author-card">
                <div class="news-author-card-avatar">
                    <?= $authorInitials ?>
                </div>
                <h3 class="news-author-card-name"><?= htmlspecialchars($authorName) ?></h3>
                <?php if ($report['club_name']): ?>
                <p class="news-author-card-club"><?= htmlspecialchars($report['club_name']) ?></p>
                <?php endif; ?>
                <?php if ($report['rider_id']): ?>
                <a href="/rider/<?= $report['rider_id'] ?>" class="btn btn-secondary btn-sm btn-block">
                    <i data-lucide="user"></i>
                    Visa profil
                </a>
                <a href="/news?rider=<?= $report['rider_id'] ?>" class="btn btn-ghost btn-sm btn-block">
                    <i data-lucide="file-text"></i>
                    Fler inlagg
                </a>
                <?php endif; ?>
            </div>

            <!-- Sponsor Sidebar Mid -->
            <?= render_global_sponsors('news_single', 'sidebar_mid', '') ?>

            <!-- Related Posts -->
            <?php if (!empty($relatedReports)): ?>
            <div class="news-related">
                <h3 class="news-related-title">Relaterade inlagg</h3>
                <div class="news-related-list">
                    <?php foreach ($relatedReports as $related): ?>
                    <a href="/news/<?= htmlspecialchars($related['slug']) ?>" class="news-related-item">
                        <div class="news-related-image">
                            <?php if ($related['featured_image']): ?>
                            <img src="<?= htmlspecialchars($related['featured_image']) ?>" alt="" loading="lazy">
                            <?php else: ?>
                            <div class="news-related-placeholder">
                                <i data-lucide="image"></i>
                            </div>
                            <?php endif; ?>
                        </div>
                        <div class="news-related-info">
                            <span class="news-related-item-title"><?= htmlspecialchars($related['title']) ?></span>
                            <span class="news-related-item-meta">
                                <?= htmlspecialchars($related['firstname'] . ' ' . substr($related['lastname'], 0, 1) . '.') ?>
                            </span>
                        </div>
                    </a>
                    <?php endforeach; ?>
                </div>
            </div>
            <?php endif; ?>

            <!-- Google Ads Placeholder -->
            <div class="news-sidebar-ad" id="google-ad-sidebar">
                <div class="news-ad-placeholder">
                    <span>Annons</span>
                </div>
            </div>
        </aside>
    </div>
</article>

<!-- Back to News -->
<div class="news-back-link">
    <a href="/news" class="btn btn-ghost">
        <i data-lucide="arrow-left"></i>
        Tillbaka till nyheter
    </a>
</div>

<script>
// Like functionality
document.getElementById('likeBtn')?.addEventListener('click', async function() {
    <?php if (!$currentUser): ?>
    window.location.href = '/login?redirect=/news/<?= htmlspecialchars($report['slug']) ?>';
    return;
    <?php endif; ?>

    const btn = this;
    const reportId = btn.dataset.reportId;
    const countEl = document.getElementById('likeCount');
    const icon = btn.querySelector('i');

    btn.disabled = true;

    try {
        const response = await fetch('/api/news/like.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ report_id: reportId })
        });

        const data = await response.json();

        if (data.success) {
            countEl.textContent = data.likes;
            if (data.liked) {
                btn.classList.add('liked');
                icon.setAttribute('fill', 'currentColor');
            } else {
                btn.classList.remove('liked');
                icon.removeAttribute('fill');
            }
        }
    } catch (e) {
        console.error('Like failed:', e);
    }

    btn.disabled = false;
});

// Comment form
document.getElementById('commentForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const form = this;
    const textarea = form.querySelector('textarea');
    const comment = textarea.value.trim();

    if (!comment) return;

    const btn = form.querySelector('button');
    btn.disabled = true;

    try {
        const response = await fetch('/api/news/comment.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                report_id: form.dataset.reportId,
                comment: comment
            })
        });

        const data = await response.json();

        if (data.success) {
            // Reload page to show new comment
            window.location.reload();
        } else {
            alert(data.error || 'Kunde inte skicka kommentar');
        }
    } catch (e) {
        console.error('Comment failed:', e);
        alert('Ett fel uppstod');
    }

    btn.disabled = false;
});

// Share functionality
function shareArticle() {
    const url = window.location.href;
    const title = <?= json_encode($report['title']) ?>;

    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(url).then(() => {
            alert('Lanken har kopierats!');
        });
    }
}
</script>
