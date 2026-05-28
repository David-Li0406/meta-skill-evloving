<?php
/**
 * Admin Tools - Simplified & Clean
 * TheHUB V3 - Only essential tools
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Get statistics
$stats = [
    'potential_duplicates' => 0,
    'empty_clubs' => 0,
    'total_riders' => 0,
    'total_results' => 0
];

try {
    $result = $db->query("SELECT COUNT(*) FROM (SELECT UPPER(firstname), UPPER(lastname) FROM riders GROUP BY UPPER(firstname), UPPER(lastname) HAVING COUNT(*) > 1) as dups");
    if ($result) $stats['potential_duplicates'] = $result->fetchColumn() ?: 0;

    $result = $db->query("SELECT COUNT(*) FROM clubs c WHERE NOT EXISTS (SELECT 1 FROM riders r WHERE r.club_id = c.id)");
    if ($result) $stats['empty_clubs'] = $result->fetchColumn() ?: 0;

    $result = $db->query("SELECT COUNT(*) FROM riders");
    if ($result) $stats['total_riders'] = $result->fetchColumn() ?: 0;

    $result = $db->query("SELECT COUNT(*) FROM results");
    if ($result) $stats['total_results'] = $result->fetchColumn() ?: 0;
} catch (Exception $e) {
    error_log("Tools stats error: " . $e->getMessage());
}

$page_title = 'Verktyg';
$breadcrumbs = [
    ['label' => 'System', 'url' => '/admin/settings'],
    ['label' => 'Verktyg']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-md);
}
@media (max-width: 767px) {
    .tools-grid {
        grid-template-columns: 1fr;
        gap: var(--space-sm);
    }
}
.tools-grid .card {
    margin-bottom: 0;
}
.tool-header {
    display: flex;
    align-items: flex-start;
    gap: var(--space-md);
    margin-bottom: var(--space-md);
}
.tool-icon {
    width: 40px;
    height: 40px;
    background: var(--color-accent-light);
    color: var(--color-accent);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.tool-icon svg { width: 20px; height: 20px; }
.tool-icon.warning { background: rgba(217, 119, 6, 0.15); color: var(--color-warning); }
.tool-icon.danger { background: rgba(239, 68, 68, 0.15); color: var(--color-error); }
.tool-title { font-weight: 600; margin: 0 0 var(--space-2xs); color: var(--color-text-primary); }
.tool-description { color: var(--color-text-secondary); font-size: var(--text-sm); margin: 0; }
.tool-stat { display: inline-block; padding: var(--space-xs) var(--space-sm); background: var(--color-bg-hover); border-radius: var(--radius-sm); font-size: var(--text-sm); margin-top: var(--space-sm); }
.tool-stat.warning { background: rgba(217, 119, 6, 0.15); color: var(--color-warning); }
.tool-actions { margin-top: var(--space-md); display: flex; flex-wrap: wrap; gap: var(--space-xs); }
.section-title {
    font-size: var(--text-lg);
    font-weight: 600;
    margin: var(--space-xl) 0 var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 2px solid var(--color-border);
    color: var(--color-text-primary);
}
.section-title:first-child { margin-top: 0; }
</style>

<!-- ========== SÄSONGSHANTERING ========== -->
<h3 class="section-title">Säsongshantering</h3>
<div class="tools-grid">

    <!-- Yearly Rebuild -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="calendar-cog"></i></div>
            <div>
                <h4 class="tool-title">Årsåterställning</h4>
                <p class="tool-description">Återställ data för ny säsong</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/tools/yearly-rebuild.php" class="btn-admin btn-admin-warning">Öppna</a>
        </div>
    </div>

    <!-- Yearly Import Review -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="file-search"></i></div>
            <div>
                <h4 class="tool-title">Granska årsimport</h4>
                <p class="tool-description">Granska och godkänn importerad data</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/tools/yearly-import-review.php" class="btn-admin btn-admin-secondary">Granska</a>
        </div>
    </div>

</div>

<!-- ========== KLUBBAR & ÅKARE ========== -->
<h3 class="section-title">Klubbar & Åkare</h3>
<div class="tools-grid">

    <!-- Sync Club Membership -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="link"></i></div>
            <div>
                <h4 class="tool-title">Synka klubbtillhörighet</h4>
                <p class="tool-description">Återskapa och lås klubbkopplingar</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/sync-club-membership.php" class="btn-admin btn-admin-primary">Synka</a>
        </div>
    </div>

    <!-- Sync Rider Clubs -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="users"></i></div>
            <div>
                <h4 class="tool-title">Synka åkare-klubbar</h4>
                <p class="tool-description">Uppdatera åkarnas klubbtillhörighet</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/sync-rider-clubs.php" class="btn-admin btn-admin-primary">Synka</a>
        </div>
    </div>

    <!-- Fix Result Club IDs -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="wrench"></i></div>
            <div>
                <h4 class="tool-title">Fixa klubb-ID i resultat</h4>
                <p class="tool-description">Korrigera felaktiga klubbreferenser</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/fix-result-club-ids.php" class="btn-admin btn-admin-warning">Fixa</a>
        </div>
    </div>

    <!-- Normalize Names -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="case-sensitive"></i></div>
            <div>
                <h4 class="tool-title">Normalisera namn</h4>
                <p class="tool-description">Rätta stavning och versaler</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/normalize-names.php" class="btn-admin btn-admin-secondary">Normalisera</a>
        </div>
    </div>

    <!-- Search UCI ID -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="globe"></i></div>
            <div>
                <h4 class="tool-title">Sök UCI-ID</h4>
                <p class="tool-description">Hitta och tilldela UCI-ID</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/search-uci-id.php" class="btn-admin btn-admin-secondary">Sök</a>
        </div>
    </div>

    <!-- Fix UCI Conflicts -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="alert-triangle"></i></div>
            <div>
                <h4 class="tool-title">Fixa UCI-konflikter</h4>
                <p class="tool-description">Lös dubbletter och konflikter</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/tools/fix-uci-conflicts.php" class="btn-admin btn-admin-warning">Fixa</a>
        </div>
    </div>

    <!-- Fix UCI Format -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="hash"></i></div>
            <div>
                <h4 class="tool-title">Normalisera UCI-ID</h4>
                <p class="tool-description">Konvertera till standardformat XXX XXX XXX XX</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/fix-uci-format.php" class="btn-admin btn-admin-secondary">Normalisera</a>
        </div>
    </div>

    <!-- Assign Missing SWE-ID -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="id-card"></i></div>
            <div>
                <h4 class="tool-title">Tilldela SWE-ID</h4>
                <p class="tool-description">Ge SWE-ID till deltagare som saknar licens</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/assign-missing-swe-id.php" class="btn-admin btn-admin-warning">Tilldela</a>
        </div>
    </div>

    <!-- Artist Name Linking -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="user-round-search"></i></div>
            <div>
                <h4 class="tool-title">Artistnamn-koppling</h4>
                <p class="tool-description">Koppla anonyma artistnamn till riktiga profiler</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/artist-name-linking.php" class="btn-admin btn-admin-primary">Oppna</a>
        </div>
    </div>

</div>

<!-- ========== DATAHANTERING ========== -->
<h3 class="section-title">Datahantering</h3>
<div class="tools-grid">

    <!-- Data Explorer -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="table-2"></i></div>
            <div>
                <h4 class="tool-title">Data Explorer</h4>
                <p class="tool-description">Bläddra och sök i databastabeller</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/data-explorer.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Rebuild Stats -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="refresh-cw"></i></div>
            <div>
                <h4 class="tool-title">Uppdatera statistik</h4>
                <p class="tool-description">Räkna om åkarstatistik och utmärkelser</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/rebuild-stats.php" class="btn-admin btn-admin-primary">Kör</a>
        </div>
    </div>

    <!-- Fix Swapped Classes -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="shuffle"></i></div>
            <div>
                <h4 class="tool-title">Byt Klasser</h4>
                <p class="tool-description">Byt plats på två klasser i ett event</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/tools/fix-swapped-classes.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Find Duplicates -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="copy"></i></div>
            <div>
                <h4 class="tool-title">Hitta dubbletter</h4>
                <p class="tool-description">Sök och hantera dubbletter</p>
            </div>
        </div>
        <?php if ($stats['potential_duplicates'] > 0): ?>
        <div class="tool-stat warning"><?= number_format($stats['potential_duplicates']) ?> möjliga dubbletter</div>
        <?php endif; ?>
        <div class="tool-actions">
            <a href="/admin/find-duplicates.php" class="btn-admin btn-admin-secondary">Sök</a>
            <a href="/admin/cleanup-duplicates.php" class="btn-admin btn-admin-secondary">Hantera</a>
        </div>
    </div>

    <!-- Cleanup Clubs -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="building"></i></div>
            <div>
                <h4 class="tool-title">Rensa klubbar</h4>
                <p class="tool-description">Ta bort tomma klubbar</p>
            </div>
        </div>
        <?php if ($stats['empty_clubs'] > 0): ?>
        <div class="tool-stat warning"><?= number_format($stats['empty_clubs']) ?> tomma klubbar</div>
        <?php endif; ?>
        <div class="tool-actions">
            <a href="/admin/cleanup-clubs.php" class="btn-admin btn-admin-secondary">Rensa</a>
        </div>
    </div>

    <!-- RF Registration -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon" style="background: linear-gradient(135deg, #006aa7 50%, #fecc00 50%);"><i data-lucide="shield-check" style="color: #fff;"></i></div>
            <div>
                <h4 class="tool-title">RF-registrering</h4>
                <p class="tool-description">Synka klubbar med SCF/NCF</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/club-rf-registration.php" class="btn-admin btn-admin-primary">Synka</a>
        </div>
    </div>

    <!-- RF Spelling Check -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon" style="background: linear-gradient(135deg, #006aa7 50%, #fecc00 50%);"><i data-lucide="spell-check" style="color: #fff;"></i></div>
            <div>
                <h4 class="tool-title">RF Stavningskontroll</h4>
                <p class="tool-description">Jämför klubbnamn mot officiellt register</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/club-rf-spelling.php" class="btn-admin btn-admin-secondary">Kontrollera</a>
        </div>
    </div>

</div>

<!-- ========== IMPORT & RESULTAT ========== -->
<h3 class="section-title">Import & Resultat</h3>
<div class="tools-grid">

    <!-- Import Results -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="upload"></i></div>
            <div>
                <h4 class="tool-title">Importera resultat</h4>
                <p class="tool-description">Importera från CSV</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/import-results.php" class="btn-admin btn-admin-primary">Importera</a>
        </div>
    </div>

    <!-- Clear Event Results -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon danger"><i data-lucide="trash-2"></i></div>
            <div>
                <h4 class="tool-title">Rensa resultat</h4>
                <p class="tool-description">Ta bort resultat från event</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/clear-event-results.php" class="btn-admin btn-admin-danger">Rensa</a>
        </div>
    </div>

    <!-- Import History -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="history"></i></div>
            <div>
                <h4 class="tool-title">Import-historik</h4>
                <p class="tool-description">Se tidigare importer</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/import-history.php" class="btn-admin btn-admin-secondary">Visa</a>
        </div>
    </div>

    <!-- Recalculate Points -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="calculator"></i></div>
            <div>
                <h4 class="tool-title">Räkna om poäng</h4>
                <p class="tool-description">Beräkna om alla poäng</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/recalculate-all-points.php" class="btn-admin btn-admin-warning">Kör</a>
        </div>
    </div>

</div>

<!-- ========== FELSÖKNING ========== -->
<h3 class="section-title">Felsökning</h3>
<div class="tools-grid">

    <!-- Data Quality -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon danger"><i data-lucide="search-x"></i></div>
            <div>
                <h4 class="tool-title">Datakvalitetsanalys</h4>
                <p class="tool-description">Hitta korrupt data</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/tools/analyze-data-quality.php" class="btn-admin btn-admin-danger">Analysera</a>
        </div>
    </div>

    <!-- Fix Series Points -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="wrench"></i></div>
            <div>
                <h4 class="tool-title">Fixa seriepoäng</h4>
                <p class="tool-description">Diagnostisera och fixa</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/fix-series-points.php" class="btn-admin btn-admin-warning">Fixa</a>
        </div>
    </div>

    <!-- Fix Time Format -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="clock"></i></div>
            <div>
                <h4 class="tool-title">Fixa tidsformat</h4>
                <p class="tool-description">Korrigera felaktiga tider</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/fix-time-format.php" class="btn-admin btn-admin-warning">Fixa</a>
        </div>
    </div>

    <!-- Diagnose Series -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="stethoscope"></i></div>
            <div>
                <h4 class="tool-title">Diagnostik</h4>
                <p class="tool-description">Serie- och klassdiagnostik</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/diagnose-series.php" class="btn-admin btn-admin-secondary">Serier</a>
            <a href="/admin/tools/diagnose-class-errors.php" class="btn-admin btn-admin-secondary">Klasser</a>
        </div>
    </div>

</div>

<!-- ========== ANALYTICS - SETUP ========== -->
<h3 class="section-title">Analytics - Setup</h3>
<div class="tools-grid">

    <!-- Analytics Setup -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="settings"></i></div>
            <div>
                <h4 class="tool-title">Analytics Setup</h4>
                <p class="tool-description">Skapa tabeller och views (kör först!)</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/analytics/setup-governance.php" class="btn-admin btn-admin-warning">1. Governance</a>
            <a href="/analytics/setup-tables.php" class="btn-admin btn-admin-warning">2. Tabeller</a>
        </div>
    </div>

    <!-- Populate Historical -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="database"></i></div>
            <div>
                <h4 class="tool-title">Populate Historical</h4>
                <p class="tool-description">Generera historisk analytics-data</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-populate.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Analytics Diagnostik -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="stethoscope"></i></div>
            <div>
                <h4 class="tool-title">Analytics Diagnostik</h4>
                <p class="tool-description">Felsök datadiskrepanser</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-diagnose.php" class="btn-admin btn-admin-warning">Diagnostisera</a>
        </div>
    </div>

    <!-- Data Quality -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="check-circle"></i></div>
            <div>
                <h4 class="tool-title">Datakvalitet</h4>
                <p class="tool-description">Analysera datakvalitet för analytics</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-data-quality.php" class="btn-admin btn-admin-secondary">Analysera</a>
        </div>
    </div>

    <!-- Reset Analytics -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon danger"><i data-lucide="rotate-ccw"></i></div>
            <div>
                <h4 class="tool-title">Reset Analytics</h4>
                <p class="tool-description">Rensa och kör om beräkningar</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-reset.php" class="btn-admin btn-admin-danger">Reset</a>
        </div>
    </div>

</div>

<!-- ========== ANALYTICS - RAPPORTER ========== -->
<h3 class="section-title">Analytics - Rapporter</h3>
<div class="tools-grid">

    <!-- Analytics Dashboard -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="layout-dashboard"></i></div>
            <div>
                <h4 class="tool-title">Dashboard</h4>
                <p class="tool-description">KPI-översikt och statistik</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-dashboard.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Historical Trends -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="trending-up"></i></div>
            <div>
                <h4 class="tool-title">Historiska Trender</h4>
                <p class="tool-description">Analysera trender över flera säsonger</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-trends.php" class="btn-admin btn-admin-primary">Visa</a>
        </div>
    </div>

    <!-- First Season Journey -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="baby"></i></div>
            <div>
                <h4 class="tool-title">First Season Journey</h4>
                <p class="tool-description">Analysera nya deltagares första säsong</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-first-season.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Event Participation -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="calendar-days"></i></div>
            <div>
                <h4 class="tool-title">Event Participation</h4>
                <p class="tool-description">Deltagarmönster per event och serie</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-event-participation.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Cohort Analysis -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="users"></i></div>
            <div>
                <h4 class="tool-title">Kohorter</h4>
                <p class="tool-description">Kohortanalys och retention</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-cohorts.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Win-Back Analytics -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="user-minus"></i></div>
            <div>
                <h4 class="tool-title">Win-Back</h4>
                <p class="tool-description">Churned vs aktiva deltagare</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/winback-analytics.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Club Analytics -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="building-2"></i></div>
            <div>
                <h4 class="tool-title">Klubbanalys</h4>
                <p class="tool-description">Statistik per klubb</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-clubs.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Geography -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="map"></i></div>
            <div>
                <h4 class="tool-title">Geografi</h4>
                <p class="tool-description">Geografisk spridning och analys</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-geography.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Series Compare -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="git-compare"></i></div>
            <div>
                <h4 class="tool-title">Jämför Serier</h4>
                <p class="tool-description">Jämför statistik mellan serier</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-series-compare.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Flow Analysis -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="workflow"></i></div>
            <div>
                <h4 class="tool-title">Flödesanalys</h4>
                <p class="tool-description">Deltagarflöden mellan serier/event</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-flow.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Reports -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="file-text"></i></div>
            <div>
                <h4 class="tool-title">Rapporter</h4>
                <p class="tool-description">Generera och hantera rapporter</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-reports.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Export Center -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="download"></i></div>
            <div>
                <h4 class="tool-title">Export Center</h4>
                <p class="tool-description">Exportera analytics-data</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/analytics-export-center.php" class="btn-admin btn-admin-secondary">Öppna</a>
        </div>
    </div>

    <!-- Participant Analysis -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="user-search"></i></div>
            <div>
                <h4 class="tool-title">Deltagaranalys</h4>
                <p class="tool-description">Hitta churned riders och serie-luckor</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/participant-analysis.php" class="btn-admin btn-admin-primary">Oppna</a>
        </div>
    </div>

    <!-- Win-Back Campaigns -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="heart-handshake"></i></div>
            <div>
                <h4 class="tool-title">Win-Back Kampanjer</h4>
                <p class="tool-description">Enkater och rabattkoder for churned riders</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/winback-campaigns.php" class="btn-admin btn-admin-primary">Oppna</a>
        </div>
    </div>

</div>

<!-- ========== SCF LICENSSYNK ========== -->
<h3 class="section-title">SCF Licenssynk</h3>
<div class="tools-grid">

    <!-- SCF Sync Status -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon" style="background: linear-gradient(135deg, #006aa7 50%, #fecc00 50%);"><i data-lucide="badge-check" style="color: #fff;"></i></div>
            <div>
                <h4 class="tool-title">Synkstatus</h4>
                <p class="tool-description">SCF License Portal integration</p>
            </div>
        </div>
        <?php
        $scfPending = 0;
        try {
            $result = $db->query("SELECT COUNT(*) FROM scf_match_candidates WHERE status = 'pending'");
            if ($result) $scfPending = $result->fetchColumn() ?: 0;
        } catch (Exception $e) {}
        if ($scfPending > 0): ?>
        <div class="tool-stat warning"><?= number_format($scfPending) ?> matchningar att granska</div>
        <?php endif; ?>
        <div class="tool-actions">
            <a href="/admin/scf-sync-status.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- SCF Match Review -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="user-check"></i></div>
            <div>
                <h4 class="tool-title">Granska matchningar</h4>
                <p class="tool-description">Bekräfta/avvisa UCI ID-matchningar</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/scf-match-review.php" class="btn-admin btn-admin-secondary">Granska</a>
        </div>
    </div>

    <!-- SCF Batch Verify -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon success"><i data-lucide="check-circle"></i></div>
            <div>
                <h4 class="tool-title">Batch-verifiering</h4>
                <p class="tool-description">Verifiera alla UCI ID mot SCF</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/scf-batch-verify.php" class="btn-admin btn-admin-success">Verifiera</a>
        </div>
    </div>

    <!-- SCF Name Search -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="search"></i></div>
            <div>
                <h4 class="tool-title">Namnsok</h4>
                <p class="tool-description">Sok cyklister utan UCI ID via namn</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/scf-name-search.php" class="btn-admin btn-admin-primary">Sok</a>
        </div>
    </div>

    <!-- SCF Import Riders -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="user-plus"></i></div>
            <div>
                <h4 class="tool-title">Importera fran SCF</h4>
                <p class="tool-description">Sok och importera nya cyklister</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/scf-import-riders.php" class="btn-admin btn-admin-primary">Importera</a>
        </div>
    </div>

    <!-- SCF API Test -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon warning"><i data-lucide="plug"></i></div>
            <div>
                <h4 class="tool-title">API Test</h4>
                <p class="tool-description">Testa SCF API-anslutning</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/scf-api-test.php" class="btn-admin btn-admin-warning">Testa</a>
        </div>
    </div>

</div>

<!-- ========== SYSTEM ========== -->
<h3 class="section-title">System</h3>
<div class="tools-grid">

    <!-- Clear Cache -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="refresh-cw"></i></div>
            <div>
                <h4 class="tool-title">Rensa cache</h4>
                <p class="tool-description">Töm systemcache</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/clear-cache.php" class="btn-admin btn-admin-secondary">Rensa</a>
        </div>
    </div>

    <!-- Backup -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="hard-drive-download"></i></div>
            <div>
                <h4 class="tool-title">Backup</h4>
                <p class="tool-description">Skapa backup</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/backup.php" class="btn-admin btn-admin-primary">Skapa</a>
        </div>
    </div>

    <!-- Migrations -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon"><i data-lucide="database"></i></div>
            <div>
                <h4 class="tool-title">Databasmigrationer</h4>
                <p class="tool-description">Kör och hantera SQL-migrationer</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/migrations.php" class="btn-admin btn-admin-primary">Öppna</a>
        </div>
    </div>

    <!-- Reset Data -->
    <div class="card">
        <div class="tool-header">
            <div class="tool-icon danger"><i data-lucide="trash-2"></i></div>
            <div>
                <h4 class="tool-title">Återställ data</h4>
                <p class="tool-description">FARLIGT - Rensa tabeller</p>
            </div>
        </div>
        <div class="tool-actions">
            <a href="/admin/reset-data.php" class="btn-admin btn-admin-danger">Återställ</a>
        </div>
    </div>

</div>

<!-- Warning -->
<div class="alert alert-warning" style="margin-top: var(--space-xl);">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Varning:</strong> Vissa verktyg gör permanenta ändringar. Säkerhetskopiera alltid innan!
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
