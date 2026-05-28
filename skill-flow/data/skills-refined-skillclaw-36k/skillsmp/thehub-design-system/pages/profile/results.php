<?php
/**
 * TheHUB V1.0 - My Results
 */

$currentUser = hub_current_user();
if (!$currentUser) {
    header('Location: /profile/login');
    exit;
}

$pdo = hub_db();

// Get available years for filter
$yearsStmt = $pdo->prepare("
    SELECT DISTINCT YEAR(e.date) as year
    FROM results res
    JOIN events e ON res.event_id = e.id
    WHERE res.cyclist_id = ?
    ORDER BY year DESC
");
$yearsStmt->execute([$currentUser['id']]);
$availableYears = $yearsStmt->fetchAll(PDO::FETCH_COLUMN);

// Get available series for filter
$seriesStmt = $pdo->prepare("
    SELECT DISTINCT s.id, sb.name as brand_name, sb.accent_color
    FROM results res
    JOIN events e ON res.event_id = e.id
    JOIN series s ON e.series_id = s.id
    LEFT JOIN series_brands sb ON s.brand_id = sb.id
    WHERE res.cyclist_id = ?
    ORDER BY sb.name
");
$seriesStmt->execute([$currentUser['id']]);
$availableSeries = $seriesStmt->fetchAll(PDO::FETCH_ASSOC);

// Get selected year and series from URL
$selectedYear = isset($_GET['year']) && is_numeric($_GET['year']) ? intval($_GET['year']) : null;
$selectedSeries = isset($_GET['series']) && is_numeric($_GET['series']) ? intval($_GET['series']) : null;

// Build query with filters
$sql = "
    SELECT res.*, e.name as event_name, e.date as event_date,
           cls.display_name as class_name, s.name as series_name, s.id as series_id,
           sb.name as brand_name
    FROM results res
    JOIN events e ON res.event_id = e.id
    LEFT JOIN classes cls ON res.class_id = cls.id
    LEFT JOIN series s ON e.series_id = s.id
    LEFT JOIN series_brands sb ON s.brand_id = sb.id
    WHERE res.cyclist_id = ?
";
$params = [$currentUser['id']];

if ($selectedYear) {
    $sql .= " AND YEAR(e.date) = ?";
    $params[] = $selectedYear;
}

if ($selectedSeries) {
    $sql .= " AND s.id = ?";
    $params[] = $selectedSeries;
}

$sql .= " ORDER BY e.date DESC";

$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$results = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Calculate stats
$totalEvents = count($results);
$podiums = count(array_filter($results, fn($r) => $r['position'] <= 3));
$wins = count(array_filter($results, fn($r) => $r['position'] === 1));
$totalPoints = array_sum(array_column($results, 'points'));
?>

<div class="page-header">
    <nav class="breadcrumb">
        <a href="/profile">Min Sida</a>
        <span class="breadcrumb-sep">›</span>
        <span>Mina resultat</span>
    </nav>
    <h1 class="page-title">
        <i data-lucide="flag" class="page-icon"></i>
        Mina resultat
    </h1>
</div>

<!-- Stats -->
<div class="stats-grid">
    <div class="stat-card">
        <span class="stat-value"><?= $totalEvents ?></span>
        <span class="stat-label">Tävlingar</span>
    </div>
    <div class="stat-card">
        <span class="stat-value"><?= $wins ?></span>
        <span class="stat-label">Segrar</span>
    </div>
    <div class="stat-card">
        <span class="stat-value"><?= $podiums ?></span>
        <span class="stat-label">Pallplatser</span>
    </div>
    <div class="stat-card">
        <span class="stat-value"><?= number_format($totalPoints) ?></span>
        <span class="stat-label">Poäng</span>
    </div>
</div>

<!-- Year Filter Links -->
<?php if (count($availableYears) > 1): ?>
<div class="filter-tabs mb-md">
    <span class="filter-label">År:</span>
    <a href="/profile/results<?= $selectedSeries ? '?series=' . $selectedSeries : '' ?>"
       class="filter-tab <?= !$selectedYear ? 'active' : '' ?>">
        Alla
    </a>
    <?php foreach ($availableYears as $year): ?>
    <a href="/profile/results?year=<?= $year ?><?= $selectedSeries ? '&series=' . $selectedSeries : '' ?>"
       class="filter-tab <?= $selectedYear == $year ? 'active' : '' ?>">
        <?= $year ?>
    </a>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<!-- Series Filter Links -->
<?php if (count($availableSeries) > 1): ?>
<div class="filter-tabs mb-lg">
    <span class="filter-label">Serie:</span>
    <a href="/profile/results<?= $selectedYear ? '?year=' . $selectedYear : '' ?>"
       class="filter-tab <?= !$selectedSeries ? 'active' : '' ?>">
        Alla
    </a>
    <?php foreach ($availableSeries as $series): ?>
    <a href="/profile/results?<?= $selectedYear ? 'year=' . $selectedYear . '&' : '' ?>series=<?= $series['id'] ?>"
       class="filter-tab <?= $selectedSeries == $series['id'] ? 'active' : '' ?>"
       style="<?= $selectedSeries == $series['id'] && $series['accent_color'] ? '--tab-accent: ' . htmlspecialchars($series['accent_color']) : '' ?>">
        <?= htmlspecialchars($series['brand_name'] ?: 'Serie ' . $series['id']) ?>
    </a>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<!-- Results List -->
<?php if (empty($results)): ?>
    <div class="empty-state">
        <div class="empty-icon"><i data-lucide="flag" class="icon-xl"></i></div>
        <h3>Inga resultat ännu</h3>
        <p>Dina tävlingsresultat kommer visas här efter att du tävlat.</p>
    </div>
<?php else: ?>
    <div class="results-list">
        <?php
        $currentYear = null;
        foreach ($results as $result):
            $year = date('Y', strtotime($result['event_date']));
            if ($year !== $currentYear):
                $currentYear = $year;
        ?>
            <h2 class="year-header"><?= $year ?></h2>
        <?php endif; ?>

            <a href="/results/<?= $result['event_id'] ?>" class="result-card">
                <div class="result-position">
                    <?php if ($result['position'] == 1): ?>
                        <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
                    <?php elseif ($result['position'] == 2): ?>
                        <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
                    <?php elseif ($result['position'] == 3): ?>
                        <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
                    <?php else: ?>
                        <span class="position-number">#<?= $result['position'] ?></span>
                    <?php endif; ?>
                </div>
                <div class="result-info">
                    <span class="result-event"><?= htmlspecialchars($result['event_name']) ?></span>
                    <span class="result-meta">
                        <?= date('j M', strtotime($result['event_date'])) ?>
                        <?php if ($result['class_name']): ?>
                            • <?= htmlspecialchars($result['class_name']) ?>
                        <?php endif; ?>
                    </span>
                </div>
                <div class="result-points">
                    <?php if ($result['points']): ?>
                        +<?= $result['points'] ?>p
                    <?php endif; ?>
                </div>
            </a>
        <?php endforeach; ?>
    </div>
<?php endif; ?>


<!-- CSS loaded from /assets/css/pages/profile-results.css -->
