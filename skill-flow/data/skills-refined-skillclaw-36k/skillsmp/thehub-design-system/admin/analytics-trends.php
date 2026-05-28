<?php
/**
 * Analytics Trends - Historiska Trender
 *
 * Visar trender over flera sasonger for:
 * - Deltagare (total, nya, retained)
 * - Retention & Churn
 * - Cross-participation
 * - Demografi (alder, kon)
 * - Discipliner
 *
 * @package TheHUB Analytics
 * @version 1.0
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';

requireAnalyticsAccess();

global $pdo;

// Antal ar att visa (kan stallas in via URL)
$numYears = isset($_GET['years']) ? max(3, min(15, (int)$_GET['years'])) : 10;
$selectedBrand = isset($_GET['brand']) && $_GET['brand'] !== '' ? (int)$_GET['brand'] : null;

// Initiera KPI Calculator
$kpiCalc = new KPICalculator($pdo);

// Hamta alla varumarken for dropdown
$allBrands = [];
try {
    $allBrands = $kpiCalc->getAllBrands();
} catch (Exception $e) {
    // Tabellen kanske inte finns annu
}

// Hamta tillgangliga ar
$availableYears = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT season_year FROM rider_yearly_stats ORDER BY season_year ASC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    $error = $e->getMessage();
}

// Begransar till senaste N ar
$yearsToShow = array_slice($availableYears, -$numYears);

// Hamta all trenddata
$trendsData = [];
$retentionData = [];
$crossParticipationData = [];
$demographicsData = [];
$disciplineData = [];
$genderData = [];

try {
    // Grundlaggande tillvaxtdata
    foreach ($yearsToShow as $year) {
        $kpis = $kpiCalc->getAllKPIs($year, $selectedBrand);
        $trendsData[] = [
            'year' => $year,
            'total_riders' => $kpis['total_riders'],
            'new_riders' => $kpis['new_riders'],
            'retained_riders' => $kpis['retained_riders'],
            'retention_rate' => $kpis['retention_rate'],
            'churn_rate' => $kpis['churn_rate'],
            'growth_rate' => $kpis['growth_rate'],
            'cross_participation' => $kpis['cross_participation_rate'],
            'average_age' => $kpis['average_age'],
            'female_pct' => calculateFemalePct($kpis['gender_distribution'])
        ];
    }

    // Aldersfordelning per ar
    foreach ($yearsToShow as $year) {
        $ageDist = $kpiCalc->getAgeDistribution($year, $selectedBrand);
        $demographicsData[$year] = [];
        foreach ($ageDist as $ag) {
            $demographicsData[$year][$ag['age_group']] = $ag['count'];
        }
    }

    // Disciplinfordelning per ar (top 5)
    foreach ($yearsToShow as $year) {
        $discDist = $kpiCalc->getDisciplineDistribution($year, $selectedBrand);
        $disciplineData[$year] = array_slice($discDist, 0, 5);
    }

} catch (Exception $e) {
    $error = $e->getMessage();
}

function calculateFemalePct($gender) {
    $total = ($gender['M'] ?? 0) + ($gender['F'] ?? 0);
    return $total > 0 ? round(($gender['F'] ?? 0) / $total * 100, 1) : 0;
}

// Page config
$page_title = 'Historiska Trender';
$breadcrumbs = [
    ['label' => 'Dashboard', 'url' => '/admin/dashboard.php'],
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Historiska Trender']
];

$page_actions = '
<div class="btn-group">
    <a href="/admin/analytics-dashboard.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="bar-chart-3"></i> Dashboard
    </a>
    <a href="/admin/analytics-reports.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="file-text"></i> Rapporter
    </a>
</div>
';

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<!-- Filter Bar -->
<div class="filter-bar">
    <form method="get" class="filter-form">
        <?php if (!empty($allBrands)): ?>
        <div class="filter-group">
            <label class="filter-label">Varumarke</label>
            <select name="brand" class="form-select" onchange="this.form.submit()">
                <option value="">Alla varumarken</option>
                <?php foreach ($allBrands as $brand): ?>
                    <option value="<?= $brand['id'] ?>" <?= $selectedBrand == $brand['id'] ? 'selected' : '' ?>
                        <?php if (!empty($brand['accent_color'])): ?>style="border-left: 3px solid <?= htmlspecialchars($brand['accent_color']) ?>"<?php endif; ?>>
                        <?= htmlspecialchars($brand['name']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <?php endif; ?>

        <div class="filter-group">
            <label class="filter-label">Antal ar</label>
            <select name="years" class="form-select" onchange="this.form.submit()">
                <?php foreach ([5, 7, 10, 15] as $y): ?>
                    <option value="<?= $y ?>" <?= $y == $numYears ? 'selected' : '' ?>>
                        Senaste <?= $y ?> ar
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <div class="filter-info">
            <span class="badge"><?= count($yearsToShow) ?> ar data</span>
            <span class="text-muted"><?= min($yearsToShow) ?> - <?= max($yearsToShow) ?></span>
        </div>
    </form>
</div>

<?php if ($selectedBrand): ?>
    <?php
    $brandName = '';
    foreach ($allBrands as $b) {
        if ($b['id'] == $selectedBrand) {
            $brandName = $b['name'];
            break;
        }
    }
    ?>
<div class="alert alert-info" style="margin-bottom: var(--space-lg);">
    <i data-lucide="filter"></i>
    <div>
        Visar trender for <strong><?= htmlspecialchars($brandName) ?></strong>.
        <a href="?years=<?= $numYears ?>">Visa alla varumarken</a>
    </div>
</div>
<?php endif; ?>

<?php if (isset($error)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Ingen data tillganglig</strong><br>
        Kor <code>php analytics/populate-historical.php</code> for att generera historisk data.
        <br><small><?= htmlspecialchars($error) ?></small>
    </div>
</div>
<?php else: ?>

<!-- DELTAGARTRENDER -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="users"></i> Deltagarutveckling</h2>
        <span class="badge badge-primary"><?= count($yearsToShow) ?> sasonger</span>
    </div>
    <div class="admin-card-body">
        <div class="chart-container" style="height: 350px;">
            <canvas id="participantChart"></canvas>
        </div>
        <div class="chart-legend-custom">
            <div class="legend-item"><span class="legend-color" style="background: #37d4d6;"></span> Totalt aktiva</div>
            <div class="legend-item"><span class="legend-color" style="background: #10b981;"></span> Nya riders</div>
            <div class="legend-item"><span class="legend-color" style="background: #8b5cf6;"></span> Atervandare</div>
        </div>
    </div>
</div>

<!-- RETENTION & GROWTH -->
<div class="grid grid-2 grid-gap-lg">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="refresh-cw"></i> Retention Rate</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="retentionChart"></canvas>
            </div>
            <p class="chart-description">Andel riders som aterkom fran foregaende sasong</p>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="trending-up"></i> Tillvaxt</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="growthChart"></canvas>
            </div>
            <p class="chart-description">Arlig procentuell forandring i deltagarantal</p>
        </div>
    </div>
</div>

<!-- CROSS-PARTICIPATION & DEMOGRAPHICS -->
<div class="grid grid-2 grid-gap-lg">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="git-branch"></i> Cross-Participation</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="crossParticipationChart"></canvas>
            </div>
            <p class="chart-description">Andel riders som deltar i mer an en serie</p>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="users"></i> Konsfordelning</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="genderChart"></canvas>
            </div>
            <p class="chart-description">Andel kvinnliga deltagare over tid</p>
        </div>
    </div>
</div>

<!-- GENOMSNITTSALDER -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="calendar"></i> Genomsnittsalder</h2>
    </div>
    <div class="admin-card-body">
        <div class="chart-container" style="height: 280px;">
            <canvas id="ageChart"></canvas>
        </div>
        <p class="chart-description">Genomsnittsalder for aktiva deltagare per sasong</p>
    </div>
</div>

<!-- SAMMANFATTNINGSTABELL -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="table"></i> Detaljerad Data</h2>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Sasong</th>
                        <th class="text-right">Totalt</th>
                        <th class="text-right">Nya</th>
                        <th class="text-right">Atervandare</th>
                        <th class="text-right">Retention</th>
                        <th class="text-right">Tillvaxt</th>
                        <th class="text-right">Cross-Part.</th>
                        <th class="text-right">Snittaolder</th>
                        <th class="text-right">Kvinnor</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_reverse($trendsData) as $row): ?>
                    <tr>
                        <td><strong><?= $row['year'] ?></strong></td>
                        <td class="text-right"><?= number_format($row['total_riders']) ?></td>
                        <td class="text-right"><?= number_format($row['new_riders']) ?></td>
                        <td class="text-right"><?= number_format($row['retained_riders']) ?></td>
                        <td class="text-right">
                            <span class="badge <?= $row['retention_rate'] >= 60 ? 'badge-success' : ($row['retention_rate'] >= 40 ? 'badge-warning' : 'badge-danger') ?>">
                                <?= $row['retention_rate'] ?>%
                            </span>
                        </td>
                        <td class="text-right">
                            <span class="trend-indicator <?= $row['growth_rate'] >= 0 ? 'positive' : 'negative' ?>">
                                <?= $row['growth_rate'] >= 0 ? '+' : '' ?><?= $row['growth_rate'] ?>%
                            </span>
                        </td>
                        <td class="text-right"><?= $row['cross_participation'] ?>%</td>
                        <td class="text-right"><?= $row['average_age'] ?> ar</td>
                        <td class="text-right"><?= $row['female_pct'] ?>%</td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Export -->
<div class="action-bar">
    <a href="/admin/analytics-reports.php?type=summary" class="btn-admin btn-admin-secondary">
        <i data-lucide="download"></i> Exportera som CSV
    </a>
</div>

<?php endif; ?>

<style>
/* Filter Bar */
.filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
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
    align-items: center;
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

.filter-info {
    display: flex;
    gap: var(--space-sm);
    align-items: center;
}

/* Chart Container */
.chart-container {
    position: relative;
    width: 100%;
}

.chart-description {
    margin: var(--space-md) 0 0;
    font-size: var(--text-sm);
    color: var(--color-text-muted);
    text-align: center;
}

/* Custom Legend */
.chart-legend-custom {
    display: flex;
    justify-content: center;
    gap: var(--space-lg);
    margin-top: var(--space-md);
    flex-wrap: wrap;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.legend-color {
    width: 12px;
    height: 12px;
    border-radius: var(--radius-sm);
}

/* Grid */
.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.grid-gap-lg {
    gap: var(--space-lg);
}

/* Trend Indicator */
.trend-indicator {
    font-weight: var(--weight-semibold);
}

.trend-indicator.positive {
    color: var(--color-success);
}

.trend-indicator.negative {
    color: var(--color-error);
}

/* Badge variants */
.badge-success {
    background: rgba(34, 197, 94, 0.15);
    color: var(--color-success);
}

.badge-warning {
    background: rgba(251, 191, 36, 0.15);
    color: var(--color-warning);
}

.badge-danger {
    background: rgba(239, 68, 68, 0.15);
    color: var(--color-error);
}

.badge-primary {
    background: var(--color-accent-light);
    color: var(--color-accent);
}

/* Text utilities */
.text-right {
    text-align: right;
}

.text-muted {
    color: var(--color-text-muted);
    font-size: var(--text-sm);
}

/* Action Bar */
.action-bar {
    margin-top: var(--space-xl);
    display: flex;
    justify-content: flex-end;
    gap: var(--space-md);
}

/* Responsive */
@media (max-width: 899px) {
    .filter-bar {
        flex-direction: column;
        align-items: stretch;
    }

    .filter-form {
        flex-direction: column;
        align-items: stretch;
    }

    .grid-2 {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 767px) {
    .filter-bar {
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        border-radius: 0;
        border-left: none;
        border-right: none;
    }

    .admin-table {
        font-size: var(--text-xs);
    }

    .admin-table th,
    .admin-table td {
        padding: var(--space-xs);
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Data fran PHP
    const trendsData = <?= json_encode($trendsData) ?>;
    const years = trendsData.map(d => d.year);

    // Fargschema
    const colors = {
        primary: '#37d4d6',
        success: '#10b981',
        purple: '#8b5cf6',
        warning: '#fbbf24',
        error: '#ef4444',
        blue: '#38bdf8'
    };

    // Gemensamma chart-options
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(11, 19, 30, 0.9)',
                titleColor: '#f8f2f0',
                bodyColor: '#c7cfdd',
                borderColor: 'rgba(55, 212, 214, 0.3)',
                borderWidth: 1,
                padding: 12,
                displayColors: true,
                callbacks: {
                    title: function(items) {
                        return 'Sasong ' + items[0].label;
                    }
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(55, 212, 214, 0.1)'
                },
                ticks: {
                    color: '#868fa2'
                }
            },
            y: {
                grid: {
                    color: 'rgba(55, 212, 214, 0.1)'
                },
                ticks: {
                    color: '#868fa2'
                }
            }
        }
    };

    // 1. DELTAGARCHART
    new Chart(document.getElementById('participantChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Totalt aktiva',
                    data: trendsData.map(d => d.total_riders),
                    borderColor: colors.primary,
                    backgroundColor: colors.primary + '20',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 6
                },
                {
                    label: 'Nya riders',
                    data: trendsData.map(d => d.new_riders),
                    borderColor: colors.success,
                    backgroundColor: 'transparent',
                    tension: 0.3,
                    borderWidth: 2,
                    pointRadius: 3,
                    pointHoverRadius: 5
                },
                {
                    label: 'Atervandare',
                    data: trendsData.map(d => d.retained_riders),
                    borderColor: colors.purple,
                    backgroundColor: 'transparent',
                    tension: 0.3,
                    borderWidth: 2,
                    pointRadius: 3,
                    pointHoverRadius: 5
                }
            ]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toLocaleString() + ' riders';
                        }
                    }
                }
            }
        }
    });

    // 2. RETENTION CHART
    new Chart(document.getElementById('retentionChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'Retention Rate',
                data: trendsData.map(d => d.retention_rate),
                borderColor: colors.success,
                backgroundColor: colors.success + '20',
                fill: true,
                tension: 0.3,
                borderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    min: 0,
                    max: 100,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return 'Retention: ' + context.parsed.y + '%';
                        }
                    }
                }
            }
        }
    });

    // 3. GROWTH CHART (Bar)
    new Chart(document.getElementById('growthChart'), {
        type: 'bar',
        data: {
            labels: years,
            datasets: [{
                label: 'Tillvaxt',
                data: trendsData.map(d => d.growth_rate),
                backgroundColor: trendsData.map(d => d.growth_rate >= 0 ? colors.success + '80' : colors.error + '80'),
                borderColor: trendsData.map(d => d.growth_rate >= 0 ? colors.success : colors.error),
                borderWidth: 2,
                borderRadius: 4
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            const val = context.parsed.y;
                            return 'Tillvaxt: ' + (val >= 0 ? '+' : '') + val + '%';
                        }
                    }
                }
            }
        }
    });

    // 4. CROSS-PARTICIPATION CHART
    new Chart(document.getElementById('crossParticipationChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'Cross-Participation',
                data: trendsData.map(d => d.cross_participation),
                borderColor: colors.purple,
                backgroundColor: colors.purple + '20',
                fill: true,
                tension: 0.3,
                borderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    min: 0,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return 'Cross-participation: ' + context.parsed.y + '%';
                        }
                    }
                }
            }
        }
    });

    // 5. GENDER CHART
    new Chart(document.getElementById('genderChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'Andel kvinnor',
                data: trendsData.map(d => d.female_pct),
                borderColor: colors.warning,
                backgroundColor: colors.warning + '20',
                fill: true,
                tension: 0.3,
                borderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    min: 0,
                    max: 50,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return 'Andel kvinnor: ' + context.parsed.y + '%';
                        }
                    }
                }
            }
        }
    });

    // 6. AGE CHART
    new Chart(document.getElementById('ageChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'Genomsnittsalder',
                data: trendsData.map(d => d.average_age),
                borderColor: colors.blue,
                backgroundColor: colors.blue + '20',
                fill: true,
                tension: 0.3,
                borderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + ' ar'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return 'Genomsnittsalder: ' + context.parsed.y.toFixed(1) + ' ar';
                        }
                    }
                }
            }
        }
    });
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
