<?php
/**
 * Public Insights - Offentlig statistik
 *
 * Visar aggregerad statistik for allmanheten.
 * GDPR-kompatibel: Maskerar alla segment med < 10 deltagare.
 *
 * @package TheHUB Analytics
 * @version 1.0
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';
require_once __DIR__ . '/../analytics/includes/auth.php';

global $pdo;

// Konstant for GDPR-skydd
const PUBLIC_MIN_SEGMENT_SIZE = 10;

// Arval
$currentYear = (int)date('Y');
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $currentYear;

// Hamta tillgangliga ar (bara de med tillrackligt data)
$availableYears = [];
try {
    $stmt = $pdo->query("
        SELECT season_year, COUNT(*) as cnt
        FROM rider_yearly_stats
        GROUP BY season_year
        HAVING cnt >= " . PUBLIC_MIN_SEGMENT_SIZE . "
        ORDER BY season_year DESC
    ");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    $availableYears = [$currentYear];
}

// Initiera KPI Calculator
$kpiCalc = new KPICalculator($pdo);

// Hamta data
$totalRiders = 0;
$newRiders = 0;
$retentionRate = 0;
$growthRate = 0;
$crossRate = 0;
$avgAge = 0;
$ageDistribution = [];
$disciplineDistribution = [];
$topClubs = [];
$growthTrend = [];

try {
    $totalRiders = $kpiCalc->getTotalActiveRiders($selectedYear);
    $newRiders = $kpiCalc->getNewRidersCount($selectedYear);
    $retentionRate = $kpiCalc->getRetentionRate($selectedYear);
    $growthRate = $kpiCalc->getGrowthRate($selectedYear);
    $crossRate = $kpiCalc->getCrossParticipationRate($selectedYear);
    $avgAge = $kpiCalc->getAverageAge($selectedYear);

    // Filtrera bort sma segment (GDPR)
    $ageDistribution = array_filter(
        $kpiCalc->getAgeDistribution($selectedYear),
        fn($a) => $a['count'] >= PUBLIC_MIN_SEGMENT_SIZE
    );

    $disciplineDistribution = array_filter(
        $kpiCalc->getDisciplineDistribution($selectedYear),
        fn($d) => $d['count'] >= PUBLIC_MIN_SEGMENT_SIZE
    );

    // Top klubbar (bara de med tillrackligt manga)
    $allClubs = $kpiCalc->getTopClubs($selectedYear, 20);
    $topClubs = array_filter($allClubs, fn($c) => $c['active_riders'] >= PUBLIC_MIN_SEGMENT_SIZE);
    $topClubs = array_slice($topClubs, 0, 10);

    // Tillvaxttrender
    $growthTrend = $kpiCalc->getGrowthTrend(5);

} catch (Exception $e) {
    // Data inte tillganglig
}

// Page setup
$pageTitle = 'Insights - Svensk Cykling i Siffror';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="insights-page">
    <div class="insights-hero">
        <div class="container">
            <h1>Svensk Cykling i Siffror</h1>
            <p class="hero-subtitle">Aggregerad statistik fran svenska cykeltavlingar</p>

            <div class="year-selector">
                <?php foreach (array_slice($availableYears, 0, 5) as $year): ?>
                    <a href="?year=<?= $year ?>" class="year-btn <?= $year == $selectedYear ? 'active' : '' ?>">
                        <?= $year ?>
                    </a>
                <?php endforeach; ?>
            </div>
        </div>
    </div>

    <div class="container">
        <?php if ($totalRiders > 0): ?>

        <!-- Main Stats -->
        <div class="stats-grid">
            <div class="stat-card stat-card--highlight">
                <div class="stat-icon">
                    <i data-lucide="users"></i>
                </div>
                <div class="stat-value"><?= number_format($totalRiders) ?></div>
                <div class="stat-label">Aktiva tavlingsdeltagare</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">
                    <i data-lucide="user-plus"></i>
                </div>
                <div class="stat-value"><?= number_format($newRiders) ?></div>
                <div class="stat-label">Nya deltagare</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">
                    <i data-lucide="refresh-cw"></i>
                </div>
                <div class="stat-value"><?= number_format($retentionRate, 0) ?>%</div>
                <div class="stat-label">Atervandare</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">
                    <i data-lucide="<?= $growthRate >= 0 ? 'trending-up' : 'trending-down' ?>"></i>
                </div>
                <div class="stat-value"><?= $growthRate >= 0 ? '+' : '' ?><?= number_format($growthRate, 0) ?>%</div>
                <div class="stat-label">Tillvaxt</div>
            </div>
        </div>

        <!-- Growth Trend -->
        <?php if (!empty($growthTrend)): ?>
        <section class="insights-section">
            <h2>Utveckling over tid</h2>
            <div class="trend-chart-public">
                <?php
                $maxVal = max(array_column($growthTrend, 'total_riders')) ?: 1;
                foreach ($growthTrend as $t):
                    $height = ($t['total_riders'] / $maxVal) * 100;
                ?>
                <div class="trend-column">
                    <div class="trend-bar-wrapper">
                        <div class="trend-bar-public" style="height: <?= $height ?>%;">
                            <span class="trend-value-public"><?= number_format($t['total_riders']) ?></span>
                        </div>
                    </div>
                    <div class="trend-year"><?= $t['season_year'] ?></div>
                </div>
                <?php endforeach; ?>
            </div>
        </section>
        <?php endif; ?>

        <div class="insights-grid">
            <!-- Age Distribution -->
            <?php if (!empty($ageDistribution)): ?>
            <section class="insights-section">
                <h2>Aldersfordelning</h2>
                <div class="distribution-chart">
                    <?php
                    $maxAge = max(array_column($ageDistribution, 'count')) ?: 1;
                    foreach ($ageDistribution as $age):
                        $width = ($age['count'] / $maxAge) * 100;
                    ?>
                    <div class="distribution-row-public">
                        <span class="dist-label"><?= htmlspecialchars($age['age_group']) ?></span>
                        <div class="dist-bar-container">
                            <div class="dist-bar" style="width: <?= $width ?>%;"></div>
                        </div>
                        <span class="dist-value"><?= number_format($age['count']) ?></span>
                    </div>
                    <?php endforeach; ?>
                </div>
                <p class="avg-stat">Genomsnittsalder: <strong><?= number_format($avgAge, 0) ?> ar</strong></p>
            </section>
            <?php endif; ?>

            <!-- Discipline Distribution -->
            <?php if (!empty($disciplineDistribution)): ?>
            <section class="insights-section">
                <h2>Populara discipliner</h2>
                <div class="distribution-chart">
                    <?php
                    $maxDisc = max(array_column($disciplineDistribution, 'count')) ?: 1;
                    foreach (array_slice($disciplineDistribution, 0, 6) as $disc):
                        $width = ($disc['count'] / $maxDisc) * 100;
                    ?>
                    <div class="distribution-row-public">
                        <span class="dist-label"><?= htmlspecialchars($disc['discipline']) ?></span>
                        <div class="dist-bar-container">
                            <div class="dist-bar dist-bar--accent" style="width: <?= $width ?>%;"></div>
                        </div>
                        <span class="dist-value"><?= number_format($disc['count']) ?></span>
                    </div>
                    <?php endforeach; ?>
                </div>
            </section>
            <?php endif; ?>
        </div>

        <!-- Cross Participation -->
        <section class="insights-section insights-highlight">
            <div class="highlight-content">
                <div class="highlight-icon">
                    <i data-lucide="git-branch"></i>
                </div>
                <div class="highlight-text">
                    <div class="highlight-value"><?= number_format($crossRate, 0) ?>%</div>
                    <div class="highlight-label">av deltagarna tavlar i flera discipliner</div>
                </div>
            </div>
        </section>

        <!-- Top Clubs -->
        <?php if (!empty($topClubs)): ?>
        <section class="insights-section">
            <h2>Storsta klubbarna</h2>
            <div class="clubs-grid">
                <?php foreach (array_slice($topClubs, 0, 8) as $i => $club): ?>
                <div class="club-card">
                    <span class="club-rank"><?= $i + 1 ?></span>
                    <div class="club-info">
                        <span class="club-name"><?= htmlspecialchars($club['club_name']) ?></span>
                        <span class="club-city"><?= htmlspecialchars($club['city'] ?? '') ?></span>
                    </div>
                    <div class="club-stats">
                        <span class="club-riders"><?= number_format($club['active_riders']) ?></span>
                        <span class="club-label">deltagare</span>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </section>
        <?php endif; ?>

        <!-- Data Note -->
        <div class="data-note">
            <i data-lucide="info"></i>
            <p>
                Statistiken baseras pa aggregerade och anonymiserade data fran svenska cykeltavlingar.
                Sma segment (&lt;10 deltagare) visas inte for att skydda personlig integritet.
            </p>
        </div>

        <?php else: ?>
        <div class="no-data">
            <i data-lucide="bar-chart-2"></i>
            <h2>Ingen statistik tillganglig</h2>
            <p>Data for <?= $selectedYear ?> ar inte tillganglig annu.</p>
        </div>
        <?php endif; ?>
    </div>
</main>

<style>
/* Insights Page */
.insights-page {
    min-height: 100vh;
}

/* Hero */
.insights-hero {
    background: linear-gradient(135deg, var(--color-bg-surface) 0%, var(--color-bg-page) 100%);
    padding: var(--space-3xl) 0;
    text-align: center;
    border-bottom: 1px solid var(--color-border);
}

.insights-hero h1 {
    font-family: var(--font-heading);
    font-size: clamp(2rem, 5vw, 3rem);
    margin-bottom: var(--space-sm);
}

.hero-subtitle {
    color: var(--color-text-secondary);
    font-size: var(--text-lg);
    margin-bottom: var(--space-xl);
}

.year-selector {
    display: flex;
    justify-content: center;
    gap: var(--space-sm);
    flex-wrap: wrap;
}

.year-btn {
    padding: var(--space-sm) var(--space-lg);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-full);
    text-decoration: none;
    color: var(--color-text-primary);
    font-weight: var(--weight-medium);
    transition: all 0.15s ease;
}

.year-btn:hover {
    border-color: var(--color-accent);
}

.year-btn.active {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin: var(--space-xl) 0;
}

.stat-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-xl);
    text-align: center;
    transition: all 0.15s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.stat-card--highlight {
    background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-hover) 100%);
    border-color: var(--color-accent);
    color: white;
}

.stat-card--highlight .stat-label {
    color: rgba(255,255,255,0.8);
}

.stat-icon {
    display: flex;
    justify-content: center;
    margin-bottom: var(--space-md);
}

.stat-icon i {
    width: 32px;
    height: 32px;
    color: var(--color-accent);
}

.stat-card--highlight .stat-icon i {
    color: white;
}

.stat-value {
    font-size: var(--text-3xl);
    font-weight: var(--weight-bold);
    margin-bottom: var(--space-xs);
}

.stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

/* Insights Section */
.insights-section {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-xl);
    margin-bottom: var(--space-lg);
}

.insights-section h2 {
    font-size: var(--text-xl);
    margin-bottom: var(--space-lg);
    padding-bottom: var(--space-md);
    border-bottom: 1px solid var(--color-border);
}

.insights-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: var(--space-lg);
}

/* Trend Chart */
.trend-chart-public {
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    height: 200px;
    gap: var(--space-md);
    padding: var(--space-md);
}

.trend-column {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 100px;
}

.trend-bar-wrapper {
    width: 100%;
    height: 150px;
    display: flex;
    align-items: flex-end;
}

.trend-bar-public {
    width: 100%;
    background: linear-gradient(180deg, var(--color-accent), var(--color-accent-hover));
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: var(--space-xs);
    min-height: 30px;
}

.trend-value-public {
    font-size: var(--text-xs);
    font-weight: var(--weight-bold);
    color: white;
}

.trend-year {
    margin-top: var(--space-sm);
    font-weight: var(--weight-semibold);
}

/* Distribution Chart */
.distribution-chart {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.distribution-row-public {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.dist-label {
    flex: 0 0 80px;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.dist-bar-container {
    flex: 1;
    height: 24px;
    background: var(--color-bg-hover);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.dist-bar {
    height: 100%;
    background: var(--color-success);
    border-radius: var(--radius-md);
    transition: width 0.3s ease;
}

.dist-bar--accent {
    background: var(--color-accent);
}

.dist-value {
    flex: 0 0 60px;
    text-align: right;
    font-weight: var(--weight-semibold);
}

.avg-stat {
    margin-top: var(--space-lg);
    padding-top: var(--space-md);
    border-top: 1px solid var(--color-border);
    text-align: center;
    color: var(--color-text-secondary);
}

/* Highlight Section */
.insights-highlight {
    background: var(--color-accent-light);
    border-color: var(--color-accent);
}

.highlight-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-xl);
}

.highlight-icon i {
    width: 48px;
    height: 48px;
    color: var(--color-accent);
}

.highlight-value {
    font-size: var(--text-4xl);
    font-weight: var(--weight-bold);
    color: var(--color-accent);
}

.highlight-label {
    font-size: var(--text-lg);
    color: var(--color-text-secondary);
}

/* Clubs Grid */
.clubs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-md);
}

.club-card {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
    transition: all 0.15s ease;
}

.club-card:hover {
    background: var(--color-bg-hover);
}

.club-rank {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: var(--color-accent-light);
    color: var(--color-accent);
    border-radius: 50%;
    font-weight: var(--weight-bold);
    font-size: var(--text-sm);
}

.club-info {
    flex: 1;
}

.club-name {
    display: block;
    font-weight: var(--weight-semibold);
}

.club-city {
    display: block;
    font-size: var(--text-sm);
    color: var(--color-text-muted);
}

.club-stats {
    text-align: right;
}

.club-riders {
    display: block;
    font-size: var(--text-xl);
    font-weight: var(--weight-bold);
    color: var(--color-accent);
}

.club-label {
    display: block;
    font-size: var(--text-xs);
    color: var(--color-text-muted);
}

/* Data Note */
.data-note {
    display: flex;
    align-items: flex-start;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    margin-top: var(--space-xl);
    margin-bottom: var(--space-xl);
}

.data-note i {
    width: 20px;
    height: 20px;
    color: var(--color-text-muted);
    flex-shrink: 0;
    margin-top: 2px;
}

.data-note p {
    margin: 0;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

/* No Data */
.no-data {
    text-align: center;
    padding: var(--space-3xl);
}

.no-data i {
    width: 64px;
    height: 64px;
    color: var(--color-text-muted);
    margin-bottom: var(--space-lg);
}

.no-data h2 {
    margin-bottom: var(--space-sm);
}

.no-data p {
    color: var(--color-text-secondary);
}

/* Responsive */
@media (max-width: 767px) {
    .insights-hero {
        padding: var(--space-xl) 0;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .stat-card {
        padding: var(--space-md);
    }

    .stat-value {
        font-size: var(--text-2xl);
    }

    .insights-grid {
        grid-template-columns: 1fr;
    }

    .highlight-content {
        flex-direction: column;
        text-align: center;
    }

    .clubs-grid {
        grid-template-columns: 1fr;
    }

    .trend-chart-public {
        height: 150px;
    }

    .trend-bar-wrapper {
        height: 100px;
    }
}
</style>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
