# Implementationsguide: Global Sponsor & Race Reports System

## Översikt
Detta system utökar TheHUBs befintliga sponsorsystem med:
- **Globala sponsorplatser** (ej event/serie-knutna)
- **Nya sponsornivåer** med tydliga rättigheter
- **Race Reports/Blogg** för deltagare att dela sina upplevelser

---

## Del 1: Databasinstallation

### Kör migration
```bash
mysql -u root -p thehub_db < 100_global_sponsors_system.sql
```

### Verifiera tabeller
Kontrollera att följande tabeller skapats:
- `sponsor_placements`
- `sponsor_tier_benefits`
- `race_reports`
- `race_report_tags`
- `race_report_tag_relations`
- `race_report_comments`
- `race_report_likes`
- `sponsor_analytics`
- `sponsor_settings`

---

## Del 2: PHP-integration

### Inkludera klasser
```php
<?php
// I din config.php eller där du initierar klasser
require_once __DIR__ . '/includes/GlobalSponsorManager.php';
require_once __DIR__ . '/includes/RaceReportManager.php';

// Initiera
$globalSponsors = new GlobalSponsorManager($db);
$raceReports = new RaceReportManager($db);
```

### Visa sponsorer på sidor

#### Startsida (index.php)
```php
<?php
// Header banner (stor banner överst)
echo $globalSponsors->renderSection('home', 'header_banner', '');

// Sidebar sponsorer
echo $globalSponsors->renderSection('home', 'sidebar_top', 'Våra partners');

// Content sponsorer
echo $globalSponsors->renderSection('home', 'content_bottom', 'Stöd av');
?>
```

#### Resultat-sida (pages/results.php)
```php
<?php
// Sidebar sponsorer
echo $globalSponsors->renderSection('results', 'sidebar_top', 'Partners');
?>
```

#### Serie-översikt (pages/series/index.php)
```php
<?php
echo $globalSponsors->renderSection('series_list', 'content_top');
?>
```

#### Enskild serie-sida (pages/series/show.php)
```php
<?php
// Hämta titelsponsor för serien
$seriesSponsor = $globalSponsors->getSeriesTitleSponsor($series_id);
if ($seriesSponsor) {
    echo '<div class="series-title-sponsor">';
    echo $globalSponsors->renderSponsor($seriesSponsor, 'header_banner');
    echo '</div>';
}

// Övriga sponsorer
echo $globalSponsors->renderSection('series_single', 'sidebar_mid', 'Partners');
?>
```

#### Databas-sidor (pages/database/index.php, riders.php, clubs.php)
```php
<?php
echo $globalSponsors->renderSection('database', 'sidebar_top', 'Branschpartners');
?>
```

#### Ranking (pages/ranking.php)
```php
<?php
echo $globalSponsors->renderSection('ranking', 'sidebar_mid', 'Sponsorer');
?>
```

---

## Del 3: Race Reports Implementation

### Lista race reports
Skapa `pages/blog/index.php`:
```php
<?php
require_once __DIR__ . '/../../includes/db.php';
require_once __DIR__ . '/../../includes/RaceReportManager.php';

$raceReports = new RaceReportManager($db);

// Paginering och filtrering
$filters = [
    'page' => $_GET['page'] ?? 1,
    'per_page' => 12,
    'tag' => $_GET['tag'] ?? null,
    'order_by' => $_GET['order'] ?? 'recent'
];

$result = $raceReports->listReports($filters);
?>

<!DOCTYPE html>
<html>
<head>
    <title>Race Reports - TheHUB</title>
    <link rel="stylesheet" href="/assets/css/sponsor-blog-system.css">
</head>
<body>
    <div class="race-reports-container">
        <h1>Race Reports</h1>
        
        <!-- Filters -->
        <div class="race-reports-filters">
            <button class="race-reports-filter-btn <?= !isset($_GET['order']) ? 'active' : '' ?>" 
                    onclick="location.href='?order=recent'">Senaste</button>
            <button class="race-reports-filter-btn <?= ($_GET['order'] ?? '') === 'popular' ? 'active' : '' ?>" 
                    onclick="location.href='?order=popular'">Populära</button>
            <button class="race-reports-filter-btn <?= ($_GET['order'] ?? '') === 'liked' ? 'active' : '' ?>" 
                    onclick="location.href='?order=liked'">Mest gillad</button>
        </div>
        
        <!-- Reports Grid -->
        <div class="race-reports-grid">
            <?php foreach ($result['reports'] as $index => $report): ?>
                <a href="/blog/<?= $report['slug'] ?>" 
                   class="race-report-card <?= ($index === 0 && $result['page'] === 1) ? 'race-report-card-featured' : '' ?>">
                    
                    <?php if ($report['featured_image']): ?>
                        <img src="<?= htmlspecialchars($report['featured_image']) ?>" 
                             alt="<?= htmlspecialchars($report['title']) ?>"
                             class="race-report-image">
                    <?php endif; ?>
                    
                    <div class="race-report-content">
                        <div class="race-report-meta">
                            <div class="race-report-author">
                                <span><?= htmlspecialchars($report['first_name'] . ' ' . $report['last_name']) ?></span>
                            </div>
                            <span>•</span>
                            <span><?= date('j M Y', strtotime($report['published_at'])) ?></span>
                            <span>•</span>
                            <span><?= $report['reading_time_minutes'] ?> min</span>
                        </div>
                        
                        <h2 class="race-report-title"><?= htmlspecialchars($report['title']) ?></h2>
                        
                        <p class="race-report-excerpt"><?= htmlspecialchars($report['excerpt']) ?></p>
                        
                        <?php if (!empty($report['tags'])): ?>
                            <div class="race-report-tags">
                                <?php foreach ($report['tags'] as $tag): ?>
                                    <span class="race-report-tag"><?= htmlspecialchars($tag['name']) ?></span>
                                <?php endforeach; ?>
                            </div>
                        <?php endif; ?>
                        
                        <div class="race-report-stats">
                            <div class="race-report-stat">
                                <span>👁</span>
                                <span><?= number_format($report['views']) ?></span>
                            </div>
                            <div class="race-report-stat">
                                <span>❤️</span>
                                <span><?= number_format($report['likes']) ?></span>
                            </div>
                        </div>
                    </div>
                </a>
            <?php endforeach; ?>
        </div>
        
        <!-- Pagination -->
        <?php if ($result['total_pages'] > 1): ?>
            <div class="pagination">
                <?php for ($i = 1; $i <= $result['total_pages']; $i++): ?>
                    <a href="?page=<?= $i ?>" 
                       class="pagination-link <?= $i === $result['page'] ? 'active' : '' ?>">
                        <?= $i ?>
                    </a>
                <?php endfor; ?>
            </div>
        <?php endif; ?>
        
        <!-- Sponsorer -->
        <?php
        require_once __DIR__ . '/../../includes/GlobalSponsorManager.php';
        $globalSponsors = new GlobalSponsorManager($db);
        echo $globalSponsors->renderSection('blog', 'sidebar_top', 'Partners');
        ?>
    </div>
</body>
</html>
```

### Enskild race report
Skapa `pages/blog/show.php`:
```php
<?php
require_once __DIR__ . '/../../includes/db.php';
require_once __DIR__ . '/../../includes/RaceReportManager.php';

$raceReports = new RaceReportManager($db);
$slug = $_GET['slug'] ?? null;

if (!$slug) {
    header('Location: /blog');
    exit;
}

$report = $raceReports->getReport($slug);

if (!$report) {
    header('HTTP/1.0 404 Not Found');
    include __DIR__ . '/../404.php';
    exit;
}

// Hantera like
if ($_POST['action'] === 'like' && isset($_SESSION['rider_id'])) {
    $raceReports->toggleLike($report['id'], $_SESSION['rider_id']);
    header('Location: /blog/' . $slug);
    exit;
}

// Hantera kommentar
if ($_POST['action'] === 'comment' && isset($_SESSION['rider_id'])) {
    $raceReports->addComment(
        $report['id'],
        $_SESSION['rider_id'],
        $_POST['comment_text'],
        $_POST['parent_id'] ?? null
    );
    header('Location: /blog/' . $slug . '#comments');
    exit;
}

$comments = $raceReports->getComments($report['id']);
?>

<!DOCTYPE html>
<html>
<head>
    <title><?= htmlspecialchars($report['title']) ?> - TheHUB</title>
    <link rel="stylesheet" href="/assets/css/sponsor-blog-system.css">
</head>
<body>
    <article class="race-report-single">
        <header class="race-report-single-header">
            <div class="race-report-meta">
                <div class="race-report-author">
                    <span><?= htmlspecialchars($report['first_name'] . ' ' . $report['last_name']) ?></span>
                </div>
                <span>•</span>
                <span><?= date('j F Y', strtotime($report['published_at'])) ?></span>
                <span>•</span>
                <span><?= $report['reading_time_minutes'] ?> min läsning</span>
            </div>
            
            <h1 class="race-report-single-title"><?= htmlspecialchars($report['title']) ?></h1>
            
            <?php if ($report['event_name']): ?>
                <div class="race-report-event">
                    <a href="/event/<?= $report['event_id'] ?>">
                        <?= htmlspecialchars($report['event_name']) ?>
                    </a>
                </div>
            <?php endif; ?>
            
            <?php if (!empty($report['tags'])): ?>
                <div class="race-report-tags">
                    <?php foreach ($report['tags'] as $tag): ?>
                        <a href="/blog?tag=<?= $tag['slug'] ?>" class="race-report-tag">
                            <?= htmlspecialchars($tag['name']) ?>
                        </a>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>
        </header>
        
        <?php if ($report['featured_image']): ?>
            <img src="<?= htmlspecialchars($report['featured_image']) ?>" 
                 alt="<?= htmlspecialchars($report['title']) ?>"
                 class="race-report-single-image">
        <?php endif; ?>
        
        <div class="race-report-single-body">
            <?= $report['content'] ?>
        </div>
        
        <?php if ($report['is_from_instagram'] && $report['instagram_url']): ?>
            <div class="race-report-instagram">
                <a href="<?= htmlspecialchars($report['instagram_url']) ?>" target="_blank" rel="noopener">
                    Se originalet på Instagram →
                </a>
            </div>
        <?php endif; ?>
        
        <!-- Like Button -->
        <div class="race-report-actions">
            <form method="POST" style="display: inline;">
                <input type="hidden" name="action" value="like">
                <button type="submit" class="race-report-like-btn">
                    <span>❤️</span>
                    <span><?= number_format($report['likes']) ?> gillningar</span>
                </button>
            </form>
            
            <div class="race-report-views">
                <span>👁</span>
                <span><?= number_format($report['views']) ?> visningar</span>
            </div>
        </div>
        
        <!-- Comments -->
        <?php if ($report['allow_comments']): ?>
            <section class="race-report-comments" id="comments">
                <h2 class="race-report-comments-title">
                    Kommentarer (<?= count($comments) ?>)
                </h2>
                
                <!-- Comment Form -->
                <?php if (isset($_SESSION['rider_id'])): ?>
                    <form method="POST" class="race-report-comment-form">
                        <input type="hidden" name="action" value="comment">
                        <textarea name="comment_text" placeholder="Skriv en kommentar..." required></textarea>
                        <button type="submit" class="btn btn-primary">Skicka kommentar</button>
                    </form>
                <?php else: ?>
                    <p><a href="/login">Logga in</a> för att kommentera</p>
                <?php endif; ?>
                
                <!-- Comments List -->
                <?php foreach ($comments as $comment): ?>
                    <div class="race-report-comment">
                        <div class="race-report-comment-author">
                            <?= htmlspecialchars($comment['first_name'] . ' ' . $comment['last_name']) ?>
                        </div>
                        <div class="race-report-comment-text">
                            <?= nl2br(htmlspecialchars($comment['comment_text'])) ?>
                        </div>
                        <div class="race-report-comment-time">
                            <?= date('j M Y H:i', strtotime($comment['created_at'])) ?>
                        </div>
                        
                        <!-- Replies -->
                        <?php if (!empty($comment['replies'])): ?>
                            <?php foreach ($comment['replies'] as $reply): ?>
                                <div class="race-report-comment race-report-comment-reply">
                                    <div class="race-report-comment-author">
                                        <?= htmlspecialchars($reply['first_name'] . ' ' . $reply['last_name']) ?>
                                    </div>
                                    <div class="race-report-comment-text">
                                        <?= nl2br(htmlspecialchars($reply['comment_text'])) ?>
                                    </div>
                                    <div class="race-report-comment-time">
                                        <?= date('j M Y H:i', strtotime($reply['created_at'])) ?>
                                    </div>
                                </div>
                            <?php endforeach; ?>
                        <?php endif; ?>
                    </div>
                <?php endforeach; ?>
            </section>
        <?php endif; ?>
        
        <!-- Sponsorer -->
        <?php
        require_once __DIR__ . '/../../includes/GlobalSponsorManager.php';
        $globalSponsors = new GlobalSponsorManager($db);
        echo $globalSponsors->renderSection('blog_single', 'content_bottom', 'Tack till våra partners');
        ?>
    </article>
</body>
</html>
```

---

## Del 4: Admin-gränssnitt

### Sponsor Management (admin/sponsors.php)

Se befintlig `admin/sponsors.php` och utöka med:

1. **Global Placement Manager**
2. **Tier Benefits Editor**
3. **Analytics Dashboard**

### Race Reports Management (admin/race-reports.php)
```php
<?php
// Lista alla reports med moderering
// Hantera featured reports
// Visa statistik
?>
```

---

## Del 5: JavaScript för tracking

Lägg till i `assets/js/app.js`:
```javascript
// Track sponsor clicks
function trackSponsorClick(sponsorId) {
    fetch('/api/sponsors/track-click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sponsor_id: sponsorId })
    });
}

// Track sponsor impressions on scroll
const sponsorObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const sponsorId = entry.target.dataset.sponsorId;
            fetch('/api/sponsors/track-impression', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sponsor_id: sponsorId })
            });
            sponsorObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

// Observe all sponsor items
document.querySelectorAll('.sponsor-item').forEach(item => {
    sponsorObserver.observe(item);
});
```

---

## Del 6: Sälja Sponsorpaket

### Pris-guide (exempel)

**Titelsponsor GravitySeries** - 200.000 kr/år
- Varumärke i GravitySeries logotyp
- Exklusiv placering startsida
- Header alla sidor
- 10 sponsorplatser
- Integration i tröjor/priser

**Titelsponsor Serie** - 75.000 kr/år per serie
- Varumärke i serienamn (ex: "XYZ-cupen powered by Sponsor")
- Banner på alla seriesidor
- Branding på eventmaterial
- 5 sponsorplatser

**Guldsponsor** - 40.000 kr/år
- Sidebar startsida
- Alla resultsidor
- Ranking sidebar
- 3 sponsorplatser

**Silversponsor** - 20.000 kr/år
- Valda sidor
- Content bottom
- 2 sponsorplatser

**Branschsponsor** - 10.000 kr/år
- Databas sidebar (relevant för cykelbutiker/verkstäder)
- Footer rotation
- 2 sponsorplatser

---

## Del 7: Nästa steg

1. **Instagram API-integration** för auto-import av race reports
2. **Email-notiser** när nya reports publiceras
3. **RSS-feed** för race reports
4. **Newsletter-integration** med featured reports
5. **Sponsor ROI-dashboard** med avancerad analytics

---

## Support & Frågor

Kontakta utvecklare vid frågor eller för ytterligare anpassningar.
