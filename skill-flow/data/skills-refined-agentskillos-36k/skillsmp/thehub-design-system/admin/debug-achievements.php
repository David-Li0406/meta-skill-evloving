<?php
/**
 * Debug Achievements - Check rider ID mismatches
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Page config
$page_title = 'Debug: Utmärkelser';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Debug: Utmärkelser']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php try { ?>
    <div class="card">
        <div class="card-header">
            <h3>Databas-status</h3>
        </div>
        <div class="card-body">
            <?php
            // Count tables
            $riderCount = $db->query("SELECT COUNT(*) FROM riders")->fetchColumn();
            $achievementCount = $db->query("SELECT COUNT(*) FROM rider_achievements")->fetchColumn();
            $resultCount = $db->query("SELECT COUNT(*) FROM results WHERE cyclist_id IS NOT NULL")->fetchColumn();

            echo "<p><strong>Antal riders:</strong> {$riderCount}</p>";
            echo "<p><strong>Antal achievements:</strong> {$achievementCount}</p>";
            echo "<p><strong>Antal resultat med cyclist_id:</strong> {$resultCount}</p>";
            ?>
        </div>
    </div>

    <div class="card" style="margin-top: var(--space-md);">
        <div class="card-header">
            <h3>Rider ID-intervall</h3>
        </div>
        <div class="card-body">
            <?php
            $minMaxRiders = $db->query("SELECT MIN(id) as min_id, MAX(id) as max_id FROM riders")->fetch(PDO::FETCH_ASSOC);
            $minMaxResults = $db->query("SELECT MIN(cyclist_id) as min_id, MAX(cyclist_id) as max_id FROM results WHERE cyclist_id IS NOT NULL")->fetch(PDO::FETCH_ASSOC);
            $minMaxAchievements = $db->query("SELECT MIN(rider_id) as min_id, MAX(rider_id) as max_id FROM rider_achievements")->fetch(PDO::FETCH_ASSOC);

            echo "<table class='table'>";
            echo "<thead><tr><th>Tabell</th><th>Min ID</th><th>Max ID</th></tr></thead>";
            echo "<tbody>";
            echo "<tr><td>riders.id</td><td>{$minMaxRiders['min_id']}</td><td>{$minMaxRiders['max_id']}</td></tr>";
            echo "<tr><td>results.cyclist_id</td><td>{$minMaxResults['min_id']}</td><td>{$minMaxResults['max_id']}</td></tr>";
            echo "<tr><td>rider_achievements.rider_id</td><td>{$minMaxAchievements['min_id']}</td><td>{$minMaxAchievements['max_id']}</td></tr>";
            echo "</tbody></table>";
            ?>
        </div>
    </div>

    <div class="card" style="margin-top: var(--space-md);">
        <div class="card-header">
            <h3>Kolla specifik rider</h3>
        </div>
        <div class="card-body">
            <?php
            $checkId = $_GET['check_id'] ?? '';
            ?>
            <form method="get" style="margin-bottom: var(--space-md);">
                <div class="form-group" style="display: flex; gap: var(--space-sm);">
                    <input type="number" name="check_id" class="form-input" placeholder="Rider ID" value="<?= htmlspecialchars($checkId) ?>" style="max-width: 200px;">
                    <button type="submit" class="btn btn-primary">Kolla</button>
                </div>
            </form>

            <?php if ($checkId): ?>
                <?php
                // Check if rider exists
                $stmt = $db->prepare("SELECT * FROM riders WHERE id = ?");
                $stmt->execute([$checkId]);
                $rider = $stmt->fetch(PDO::FETCH_ASSOC);

                if ($rider) {
                    echo "<div class='alert alert-success'>Rider {$checkId} finns: {$rider['firstname']} {$rider['lastname']}</div>";

                    // Check achievements
                    $stmt = $db->prepare("SELECT * FROM rider_achievements WHERE rider_id = ?");
                    $stmt->execute([$checkId]);
                    $achievements = $stmt->fetchAll(PDO::FETCH_ASSOC);

                    echo "<p><strong>Achievements:</strong> " . count($achievements) . "</p>";
                    if (!empty($achievements)) {
                        echo "<ul>";
                        foreach ($achievements as $a) {
                            echo "<li>{$a['achievement_type']}: {$a['achievement_value']} (year: {$a['season_year']})</li>";
                        }
                        echo "</ul>";
                    }

                    // Check results
                    $stmt = $db->prepare("SELECT COUNT(*) FROM results WHERE cyclist_id = ?");
                    $stmt->execute([$checkId]);
                    $resultCount = $stmt->fetchColumn();
                    echo "<p><strong>Resultat:</strong> {$resultCount}</p>";
                } else {
                    echo "<div class='alert alert-danger'>Rider {$checkId} finns INTE i databasen</div>";

                    // Check if this ID exists in results
                    $stmt = $db->prepare("SELECT COUNT(*) FROM results WHERE cyclist_id = ?");
                    $stmt->execute([$checkId]);
                    $resultCount = $stmt->fetchColumn();

                    if ($resultCount > 0) {
                        echo "<div class='alert alert-warning'>Men det finns {$resultCount} resultat med cyclist_id={$checkId}</div>";
                    }

                    // Check if this ID exists in achievements
                    $stmt = $db->prepare("SELECT COUNT(*) FROM rider_achievements WHERE rider_id = ?");
                    $stmt->execute([$checkId]);
                    $achCount = $stmt->fetchColumn();

                    if ($achCount > 0) {
                        echo "<div class='alert alert-warning'>Och det finns {$achCount} achievements med rider_id={$checkId}</div>";
                    }
                }
                ?>
            <?php endif; ?>
        </div>
    </div>

    <div class="card" style="margin-top: var(--space-md);">
        <div class="card-header">
            <h3>Orphaned Achievements (rider_id finns inte i riders)</h3>
        </div>
        <div class="card-body">
            <?php
            $orphaned = $db->query("
                SELECT ra.rider_id, COUNT(*) as count
                FROM rider_achievements ra
                LEFT JOIN riders r ON ra.rider_id = r.id
                WHERE r.id IS NULL
                GROUP BY ra.rider_id
                ORDER BY ra.rider_id
                LIMIT 20
            ")->fetchAll(PDO::FETCH_ASSOC);

            $totalOrphaned = 0;
            if (empty($orphaned)) {
                echo "<p class='text-success'>Inga orphaned achievements hittades - alla rider_id matchar riders.id</p>";
            } else {
                foreach ($orphaned as $o) {
                    $totalOrphaned += $o['count'];
                }
                echo "<p class='text-danger'>Varning: {$totalOrphaned} achievements med rider_id som inte finns i riders:</p>";
                echo "<table class='table'>";
                echo "<thead><tr><th>rider_id</th><th>Antal achievements</th></tr></thead>";
                echo "<tbody>";
                foreach ($orphaned as $o) {
                    echo "<tr><td>{$o['rider_id']}</td><td>{$o['count']}</td></tr>";
                }
                echo "</tbody></table>";

                echo "<form method='post' style='margin-top: var(--space-md);' onsubmit='return confirm(\"Radera alla orphaned achievements?\");'>";
                echo "<input type='hidden' name='action' value='clean_orphaned_achievements'>";
                echo "<button type='submit' class='btn btn-danger'>Radera {$totalOrphaned} orphaned achievements</button>";
                echo "</form>";
            }
            ?>
        </div>
    </div>

    <div class="card" style="margin-top: var(--space-md);">
        <div class="card-header">
            <h3>Orphaned Results (cyclist_id finns inte i riders)</h3>
        </div>
        <div class="card-body">
            <?php
            $orphanedResults = $db->query("
                SELECT r.cyclist_id, COUNT(*) as count
                FROM results r
                LEFT JOIN riders rd ON r.cyclist_id = rd.id
                WHERE rd.id IS NULL AND r.cyclist_id IS NOT NULL
                GROUP BY r.cyclist_id
                ORDER BY r.cyclist_id
                LIMIT 20
            ")->fetchAll(PDO::FETCH_ASSOC);

            $totalOrphanedResults = 0;
            if (empty($orphanedResults)) {
                echo "<p class='text-success'>Inga orphaned results hittades - alla cyclist_id matchar riders.id</p>";
            } else {
                foreach ($orphanedResults as $o) {
                    $totalOrphanedResults += $o['count'];
                }
                echo "<p class='text-danger'>Varning: {$totalOrphanedResults} resultat med cyclist_id som inte finns i riders:</p>";
                echo "<table class='table'>";
                echo "<thead><tr><th>cyclist_id</th><th>Antal resultat</th></tr></thead>";
                echo "<tbody>";
                foreach ($orphanedResults as $o) {
                    echo "<tr><td>{$o['cyclist_id']}</td><td>{$o['count']}</td></tr>";
                }
                echo "</tbody></table>";

                echo "<div class='alert alert-warning' style='margin-top: var(--space-md);'>";
                echo "<strong>Detta är grundproblemet!</strong><br>";
                echo "Results-tabellen innehåller cyclist_id värden som inte matchar riders.id.<br>";
                echo "Detta sker när import använder externa ID istället för interna rider IDs.<br><br>";
                echo "<strong>Lösningar:</strong>";
                echo "<ol>";
                echo "<li>Kör om importen med korrekt rider-matchning</li>";
                echo "<li>Uppdatera cyclist_id i results manuellt</li>";
                echo "<li>Radera orphaned results om de inte behövs</li>";
                echo "</ol>";
                echo "</div>";
            }
            ?>
        </div>
    </div>

    <div class="card" style="margin-top: var(--space-md);">
        <div class="card-header">
            <h3>Achievements per typ</h3>
        </div>
        <div class="card-body">
            <?php
            $byType = $db->query("
                SELECT achievement_type, COUNT(*) as count
                FROM rider_achievements
                GROUP BY achievement_type
                ORDER BY count DESC
            ")->fetchAll(PDO::FETCH_ASSOC);

            echo "<table class='table'>";
            echo "<thead><tr><th>Typ</th><th>Antal</th></tr></thead>";
            echo "<tbody>";
            foreach ($byType as $t) {
                echo "<tr><td>{$t['achievement_type']}</td><td>{$t['count']}</td></tr>";
            }
            echo "</tbody></table>";
            ?>
        </div>
    </div>

    <div class="card" style="margin-top: var(--space-md);">
        <div class="card-header">
            <h3>Series Champions med klubb</h3>
        </div>
        <div class="card-body">
            <?php
            $seriesChamps = $db->query("
                SELECT
                    ra.rider_id,
                    r.firstname,
                    r.lastname,
                    r.club_id,
                    c.name as club_name,
                    ra.achievement_value,
                    ra.season_year
                FROM rider_achievements ra
                JOIN riders r ON ra.rider_id = r.id
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE ra.achievement_type = 'series_champion'
                ORDER BY ra.season_year DESC
                LIMIT 20
            ")->fetchAll(PDO::FETCH_ASSOC);

            if (empty($seriesChamps)) {
                echo "<p>Inga series_champion achievements hittades.</p>";
            } else {
                echo "<table class='table'>";
                echo "<thead><tr><th>Rider ID</th><th>Namn</th><th>Klubb</th><th>Serie</th><th>År</th></tr></thead>";
                echo "<tbody>";
                foreach ($seriesChamps as $sc) {
                    $clubInfo = $sc['club_name'] ?? "Ingen klubb (club_id: {$sc['club_id']})";
                    echo "<tr>";
                    echo "<td><a href='/rider/{$sc['rider_id']}'>{$sc['rider_id']}</a></td>";
                    echo "<td>{$sc['firstname']} {$sc['lastname']}</td>";
                    echo "<td>{$clubInfo}</td>";
                    echo "<td>{$sc['achievement_value']}</td>";
                    echo "<td>{$sc['season_year']}</td>";
                    echo "</tr>";
                }
                echo "</tbody></table>";
            }
            ?>
        </div>
    </div>

    <div class="card" style="margin-top: var(--space-md);">
        <div class="card-header">
            <h3>Kolla klubb achievements</h3>
        </div>
        <div class="card-body">
            <?php
            $clubId = $_GET['club_id'] ?? '';
            ?>
            <form method="get" style="margin-bottom: var(--space-md);">
                <div class="form-group" style="display: flex; gap: var(--space-sm);">
                    <input type="number" name="club_id" class="form-input" placeholder="Club ID" value="<?= htmlspecialchars($clubId) ?>" style="max-width: 200px;">
                    <button type="submit" class="btn btn-primary">Kolla klubb</button>
                </div>
            </form>

            <?php if ($clubId): ?>
                <?php
                // Check club
                $stmt = $db->prepare("SELECT * FROM clubs WHERE id = ?");
                $stmt->execute([$clubId]);
                $club = $stmt->fetch(PDO::FETCH_ASSOC);

                if ($club) {
                    echo "<div class='alert alert-success'>Klubb: {$club['name']}</div>";

                    // Get members with achievements
                    $stmt = $db->prepare("
                        SELECT
                            r.id as rider_id,
                            r.firstname,
                            r.lastname,
                            ra.achievement_type,
                            ra.achievement_value,
                            ra.season_year
                        FROM riders r
                        JOIN rider_achievements ra ON r.id = ra.rider_id
                        WHERE r.club_id = ?
                        AND ra.achievement_type IN ('series_champion', 'swedish_champion')
                        ORDER BY ra.season_year DESC
                    ");
                    $stmt->execute([$clubId]);
                    $memberAchievements = $stmt->fetchAll(PDO::FETCH_ASSOC);

                    echo "<p><strong>Medlemmar med series_champion eller swedish_champion:</strong> " . count($memberAchievements) . "</p>";

                    if (!empty($memberAchievements)) {
                        echo "<table class='table'>";
                        echo "<thead><tr><th>Rider ID</th><th>Namn</th><th>Typ</th><th>Värde</th><th>År</th></tr></thead>";
                        echo "<tbody>";
                        foreach ($memberAchievements as $ma) {
                            echo "<tr>";
                            echo "<td><a href='/rider/{$ma['rider_id']}'>{$ma['rider_id']}</a></td>";
                            echo "<td>{$ma['firstname']} {$ma['lastname']}</td>";
                            echo "<td>{$ma['achievement_type']}</td>";
                            echo "<td>{$ma['achievement_value']}</td>";
                            echo "<td>{$ma['season_year']}</td>";
                            echo "</tr>";
                        }
                        echo "</tbody></table>";
                    } else {
                        echo "<p>Inga members med dessa achievements.</p>";

                        // Check how many members exist
                        $stmt = $db->prepare("SELECT COUNT(*) FROM riders WHERE club_id = ?");
                        $stmt->execute([$clubId]);
                        $memberCount = $stmt->fetchColumn();
                        echo "<p>Klubben har {$memberCount} medlemmar totalt.</p>";
                    }
                } else {
                    echo "<div class='alert alert-danger'>Klubb {$clubId} finns inte</div>";
                }
                ?>
            <?php endif; ?>
        </div>
    </div>
<?php } catch (Exception $e) { ?>
<div class="alert alert-danger">
    <strong>Databasfel:</strong> <?= htmlspecialchars($e->getMessage()) ?>
</div>
<?php } ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
