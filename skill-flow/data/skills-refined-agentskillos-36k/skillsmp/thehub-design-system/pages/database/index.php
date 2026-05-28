<?php
/**
 * TheHUB V1.0 - Databas
 * Sök åkare och klubbar - inspirerad av V2 riders.php och clubs/leaderboard.php
 */

// Prevent direct access
if (!defined('HUB_ROOT')) {
    header('Location: /database');
    exit;
}

// Define page type for sponsor placements
define('HUB_PAGE_TYPE', 'database');

$pdo = hub_db();
$tab = $_GET['tab'] ?? 'riders';

// Load filter setting from admin configuration
$publicSettings = require HUB_ROOT . '/config/public_settings.php';
$filter = $publicSettings['public_riders_display'] ?? 'all';

// Get stats based on filter from admin settings
if ($filter === 'with_results') {
    $riderCount = $pdo->query("
        SELECT COUNT(DISTINCT r.id)
        FROM riders r
        INNER JOIN results res ON r.id = res.cyclist_id
        WHERE r.active = 1
    ")->fetchColumn();
    $clubCount = $pdo->query("
        SELECT COUNT(DISTINCT c.id)
        FROM clubs c
        INNER JOIN riders r ON c.id = r.club_id
        INNER JOIN results res ON r.id = res.cyclist_id
    ")->fetchColumn();
} else {
    $riderCount = $pdo->query("SELECT COUNT(*) FROM riders WHERE active = 1")->fetchColumn();
    $clubCount = $pdo->query("SELECT COUNT(*) FROM clubs")->fetchColumn();
}

// Count unique riders with wins and podiums (exclude motion classes via awards_points)
$ridersWithWins = $pdo->query("
    SELECT COUNT(DISTINCT res.cyclist_id)
    FROM results res
    INNER JOIN classes cls ON res.class_id = cls.id
    WHERE res.position = 1
      AND res.status = 'finished'
      AND COALESCE(cls.awards_points, 1) = 1
")->fetchColumn();

$ridersWithPodiums = $pdo->query("
    SELECT COUNT(DISTINCT res.cyclist_id)
    FROM results res
    INNER JOIN classes cls ON res.class_id = cls.id
    WHERE res.position <= 3
      AND res.status = 'finished'
      AND COALESCE(cls.awards_points, 1) = 1
")->fetchColumn();

// Get top riders from ranking snapshots or calculate from recent events
// Only count competitive classes (awards_points = 1)
$topRiders = [];

// Try to get from ranking snapshots first
try {
    $snapshotCheck = $pdo->query("SELECT COUNT(*) FROM ranking_snapshots WHERE discipline = 'GRAVITY'")->fetchColumn();
    if ($snapshotCheck > 0) {
        // Use ranking snapshots - but filter out riders who only have motion class results
        $topRiders = $pdo->query("
            SELECT
                rs.rider_id as id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                rs.total_ranking_points as ranking_score,
                rs.events_count as total_races,
                (SELECT COUNT(*) FROM results res2
                 INNER JOIN classes cls ON res2.class_id = cls.id
                 WHERE res2.cyclist_id = rs.rider_id AND res2.position = 1
                   AND res2.status = 'finished'
                   AND COALESCE(cls.awards_points, 1) = 1) as wins,
                (SELECT COUNT(*) FROM results res2
                 INNER JOIN classes cls ON res2.class_id = cls.id
                 WHERE res2.cyclist_id = rs.rider_id AND res2.position <= 3
                   AND res2.status = 'finished'
                   AND COALESCE(cls.awards_points, 1) = 1) as podiums
            FROM ranking_snapshots rs
            INNER JOIN riders r ON rs.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE rs.discipline = 'GRAVITY'
              AND rs.snapshot_date = (SELECT MAX(snapshot_date) FROM ranking_snapshots WHERE discipline = 'GRAVITY')
              AND EXISTS (
                  SELECT 1 FROM results res3
                  INNER JOIN classes cls3 ON res3.class_id = cls3.id
                  WHERE res3.cyclist_id = rs.rider_id
                    AND res3.status = 'finished'
                    AND COALESCE(cls3.awards_points, 1) = 1
              )
            ORDER BY rs.ranking_position ASC
            LIMIT 10
        ")->fetchAll(PDO::FETCH_ASSOC);
    }
} catch (Exception $e) {
    // Table doesn't exist, fallback below
}

// Fallback: Calculate from 10 most recent events with competitive classes
if (empty($topRiders)) {
    // Get 10 most recent events
    $recentEventIds = $pdo->query("
        SELECT id FROM events WHERE date <= CURDATE() ORDER BY date DESC LIMIT 10
    ")->fetchAll(PDO::FETCH_COLUMN);

    if (!empty($recentEventIds)) {
        $eventIdList = implode(',', array_map('intval', $recentEventIds));

        $topRiders = $pdo->query("
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                SUM(res.points) as ranking_score,
                COUNT(DISTINCT res.id) as total_races,
                COUNT(CASE WHEN res.position = 1
                    AND COALESCE(cls.awards_points, 1) = 1
                    THEN 1 END) as wins,
                COUNT(CASE WHEN res.position <= 3
                    AND COALESCE(cls.awards_points, 1) = 1
                    THEN 1 END) as podiums
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            INNER JOIN results res ON r.id = res.cyclist_id
            LEFT JOIN classes cls ON res.class_id = cls.id
            WHERE r.active = 1
              AND res.status = 'finished'
              AND res.event_id IN ({$eventIdList})
              AND COALESCE(cls.awards_points, 1) = 1
            GROUP BY r.id
            HAVING total_races >= 1
            ORDER BY ranking_score DESC
            LIMIT 10
        ")->fetchAll(PDO::FETCH_ASSOC);
    }
}

// Get club rankings from snapshots or fallback
$clubRankings = [];

// Try to get from club ranking snapshots first
try {
    $clubSnapshotCheck = $pdo->query("SELECT COUNT(*) FROM club_ranking_snapshots WHERE discipline = 'GRAVITY'")->fetchColumn();
    if ($clubSnapshotCheck > 0) {
        $clubRankings = $pdo->query("
            SELECT
                crs.club_id as id,
                c.name,
                c.city,
                crs.riders_count as riders_with_points,
                crs.total_ranking_points as total_points,
                (SELECT COUNT(*) FROM results res2
                 INNER JOIN riders r2 ON res2.cyclist_id = r2.id
                 INNER JOIN classes cls ON res2.class_id = cls.id
                 WHERE r2.club_id = crs.club_id AND res2.position <= 3
                   AND res2.status = 'finished'
                   AND COALESCE(cls.awards_points, 1) = 1) as podiums
            FROM club_ranking_snapshots crs
            INNER JOIN clubs c ON crs.club_id = c.id
            WHERE crs.discipline = 'GRAVITY'
              AND crs.snapshot_date = (SELECT MAX(snapshot_date) FROM club_ranking_snapshots WHERE discipline = 'GRAVITY')
            ORDER BY crs.ranking_position ASC
            LIMIT 10
        ")->fetchAll(PDO::FETCH_ASSOC);
    }
} catch (Exception $e) {
    // Table doesn't exist
}

// Fallback: Calculate clubs with competitive results only
if (empty($clubRankings)) {
    try {
        $clubRankings = $pdo->query("
            SELECT c.id, c.name, c.city,
                   COUNT(DISTINCT CASE WHEN res.points > 0 THEN r.id END) as riders_with_points,
                   COUNT(DISTINCT res.id) as total_starts,
                   COUNT(CASE WHEN res.position <= 3
                       AND COALESCE(cls.awards_points, 1) = 1
                       THEN 1 END) as podiums,
                   SUM(res.points) as total_points
            FROM clubs c
            LEFT JOIN riders r ON c.id = r.club_id AND r.active = 1
            LEFT JOIN results res ON r.id = res.cyclist_id
            LEFT JOIN classes cls ON res.class_id = cls.id
            WHERE COALESCE(cls.awards_points, 1) = 1
                  OR cls.id IS NULL
            GROUP BY c.id
            HAVING total_starts > 0
            ORDER BY podiums DESC, total_points DESC, total_starts DESC
            LIMIT 10
        ")->fetchAll(PDO::FETCH_ASSOC);
    } catch (Exception $e) {
        // Table might not exist
    }
}

?>

<div class="page-header">
    <h1 class="page-title">
        <i data-lucide="database" class="page-icon"></i>
        Databas
    </h1>
    <p class="page-subtitle">Sök bland åkare och klubbar</p>
</div>

<!-- Global Sponsor: Header Banner -->
<?= render_global_sponsors('database', 'header_banner', '') ?>

<!-- Global Sponsor: Content Top -->
<?= render_global_sponsors('database', 'content_top', '') ?>

<!-- Stats Cards -->
<div class="stats-grid">
    <div class="stat-card">
        <span class="stat-value"><?= number_format($riderCount) ?></span>
        <span class="stat-label">Åkare</span>
    </div>
    <div class="stat-card">
        <span class="stat-value"><?= number_format($clubCount) ?></span>
        <span class="stat-label">Klubbar</span>
    </div>
    <div class="stat-card">
        <span class="stat-value"><?= number_format($ridersWithWins) ?></span>
        <span class="stat-label">Med vinster</span>
    </div>
    <div class="stat-card">
        <span class="stat-value"><?= number_format($ridersWithPodiums) ?></span>
        <span class="stat-label">Med pallplatser</span>
    </div>
</div>

<!-- Search Section -->
<div class="search-card">
    <div class="tabs-nav">
        <button class="tab-pill active" data-tab="riders"><i data-lucide="users"></i> Sök Åkare</button>
        <button class="tab-pill" data-tab="clubs"><i data-lucide="shield"></i> Sök Klubbar</button>
    </div>

    <div class="search-box">
        <span class="search-icon"><i data-lucide="search"></i></span>
        <input type="text"
               id="database-search"
               class="search-input"
               placeholder="Skriv namn för att söka..."
               autocomplete="off"
               data-type="riders">
        <button type="button" class="search-clear hidden"><i data-lucide="x"></i></button>
    </div>

    <div class="search-results" id="search-results"></div>

    <div class="search-hint" id="search-hint">
        Skriv minst 2 tecken för att söka
    </div>
</div>

<!-- Two Column Layout -->
<div class="database-grid">
    <!-- Top Riders -->
    <div class="card">
        <h2 class="card-title"><i data-lucide="trophy"></i> Topprankade</h2>
        <div class="ranking-list">
            <?php foreach ($topRiders as $i => $rider): ?>
            <a href="/rider/<?= $rider['id'] ?>" class="ranking-item">
                <span class="ranking-pos <?= $i < 3 ? 'top-' . ($i + 1) : '' ?>">
                    <?php if ($i === 0): ?>
                        <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
                    <?php elseif ($i === 1): ?>
                        <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
                    <?php elseif ($i === 2): ?>
                        <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
                    <?php else: ?>
                        <?= $i + 1 ?>
                    <?php endif; ?>
                </span>
                <div class="ranking-info">
                    <span class="ranking-name"><?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?></span>
                    <span class="ranking-meta"><?= htmlspecialchars($rider['club_name'] ?? '-') ?></span>
                </div>
                <div class="ranking-stats">
                    <?php if ($rider['wins'] > 0): ?>
                        <span class="stat gold"><?= $rider['wins'] ?> Vinster</span>
                    <?php endif; ?>
                    <span class="stat"><?= $rider['podiums'] ?> pallplatser</span>
                </div>
            </a>
            <?php endforeach; ?>
        </div>
        <a href="/ranking" class="card-link">Visa fullständig ranking →</a>
    </div>

    <!-- Top Clubs -->
    <div class="card">
        <h2 class="card-title"><i data-lucide="shield"></i> Toppklubbar</h2>
        <div class="ranking-list">
            <?php foreach ($clubRankings as $i => $club): ?>
            <a href="/club/<?= $club['id'] ?>" class="ranking-item">
                <span class="ranking-pos <?= $i < 3 ? 'top-' . ($i + 1) : '' ?>">
                    <?php if ($i === 0): ?>
                        <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
                    <?php elseif ($i === 1): ?>
                        <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
                    <?php elseif ($i === 2): ?>
                        <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
                    <?php else: ?>
                        <?= $i + 1 ?>
                    <?php endif; ?>
                </span>
                <div class="ranking-info">
                    <span class="ranking-name"><?= htmlspecialchars($club['name']) ?></span>
                    <span class="ranking-meta"><?= $club['riders_with_points'] ?> åkare med poäng</span>
                </div>
                <div class="ranking-stats">
                    <span class="stat"><?= $club['podiums'] ?> pall</span>
                    <span class="stat"><?= number_format($club['total_points']) ?> poäng</span>
                </div>
            </a>
            <?php endforeach; ?>
        </div>
    </div>
</div>

<!-- Global Sponsor: Content Bottom -->
<?= render_global_sponsors('database', 'content_bottom', 'Tack till våra partners') ?>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('database-search');
    const searchResults = document.getElementById('search-results');
    const searchHint = document.getElementById('search-hint');
    const searchClear = document.querySelector('.search-clear');
    const searchTabs = document.querySelectorAll('.tab-pill');

    let searchTimeout;
    let currentType = 'riders';

    searchTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            searchTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            currentType = this.dataset.tab;
            searchInput.dataset.type = currentType;
            searchInput.placeholder = currentType === 'riders' ? 'Skriv namn för att söka åkare...' : 'Skriv namn för att söka klubbar...';
            searchInput.value = '';
            searchResults.innerHTML = '';
            searchHint.style.display = 'block';
            searchClear.style.display = 'none';
        });
    });

    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        searchClear.style.display = query ? 'block' : 'none';

        clearTimeout(searchTimeout);

        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchHint.style.display = 'block';
            searchHint.textContent = 'Skriv minst 2 tecken för att söka';
            return;
        }

        searchHint.style.display = 'block';
        searchHint.textContent = 'Söker...';

        searchTimeout = setTimeout(() => {
            fetch('/api/search.php?type=' + currentType + '&q=' + encodeURIComponent(query))
                .then(r => {
                    if (!r.ok) {
                        throw new Error('HTTP ' + r.status);
                    }
                    return r.json();
                })
                .then(data => {
                    searchHint.style.display = 'none';

                    if (data.results && data.results.length > 0) {
                        searchResults.innerHTML = data.results.map(item => {
                            if (currentType === 'riders') {
                                return '<a href="/rider/' + item.id + '" class="search-result">' +
                                    '<span class="search-result-avatar">' + ((item.firstname || '?')[0]).toUpperCase() + '</span>' +
                                    '<div class="search-result-info">' +
                                    '<span class="search-result-name">' + item.firstname + ' ' + item.lastname + '</span>' +
                                    '<span class="search-result-meta">' + (item.club_name || '-') + '</span>' +
                                    '</div></a>';
                            } else {
                                return '<a href="/club/' + item.id + '" class="search-result">' +
                                    '<span class="search-result-avatar"><i data-lucide="shield"></i></span>' +
                                    '<div class="search-result-info">' +
                                    '<span class="search-result-name">' + item.name + '</span>' +
                                    '<span class="search-result-meta">' + (item.member_count || 0) + ' medlemmar</span>' +
                                    '</div></a>';
                            }
                        }).join('');
                        // Re-init Lucide icons for dynamic content
                        if (typeof lucide !== 'undefined') lucide.createIcons();
                    } else {
                        searchResults.innerHTML = '<div class="search-hint">Inga resultat hittades</div>';
                    }
                })
                .catch(err => {
                    console.error('Search error:', err);
                    searchHint.style.display = 'block';
                    searchHint.textContent = 'Fel vid sökning: ' + err.message;
                });
        }, 300);
    });

    searchClear.addEventListener('click', function() {
        searchInput.value = '';
        searchResults.innerHTML = '';
        searchHint.style.display = 'block';
        searchHint.textContent = 'Skriv minst 2 tecken för att söka';
        this.style.display = 'none';
        searchInput.focus();
    });
});
</script>
