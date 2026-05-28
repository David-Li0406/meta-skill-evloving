<?php
/**
 * Artist Name Linking Tool
 *
 * Admin tool for managing anonymous/artist name accounts from legacy data (2013-2018).
 * Allows linking artist names to real rider profiles.
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
requireAdmin();

global $pdo;

$message = '';
$error = '';

// Check if tables exist
$tablesExist = false;
try {
    $pdo->query("SELECT 1 FROM artist_name_claims LIMIT 1");
    $tablesExist = true;
} catch (Exception $e) {
    // Check if is_anonymous column exists
    try {
        $pdo->query("SELECT is_anonymous FROM riders LIMIT 1");
        $tablesExist = true;
    } catch (Exception $e2) {
        $tablesExist = false;
    }
}

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $tablesExist) {
    $action = $_POST['action'] ?? '';

    if ($action === 'mark_anonymous') {
        // Mark a rider as anonymous
        $riderId = (int)$_POST['rider_id'];
        $source = trim($_POST['source'] ?? '');
        $stmt = $pdo->prepare("UPDATE riders SET is_anonymous = 1, anonymous_source = ? WHERE id = ?");
        $stmt->execute([$source ?: null, $riderId]);
        $message = 'Deltagare markerad som anonym';

    } elseif ($action === 'unmark_anonymous') {
        // Remove anonymous flag
        $riderId = (int)$_POST['rider_id'];
        $stmt = $pdo->prepare("UPDATE riders SET is_anonymous = 0 WHERE id = ?");
        $stmt->execute([$riderId]);
        $message = 'Anonym-markering borttagen';

    } elseif ($action === 'approve_claim') {
        // Approve a claim and merge
        $claimId = (int)$_POST['claim_id'];
        $adminNotes = trim($_POST['admin_notes'] ?? '');

        // Get claim details
        $stmt = $pdo->prepare("SELECT * FROM artist_name_claims WHERE id = ?");
        $stmt->execute([$claimId]);
        $claim = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($claim && $claim['status'] === 'pending') {
            $pdo->beginTransaction();
            try {
                // Update claim status
                $stmt = $pdo->prepare("
                    UPDATE artist_name_claims
                    SET status = 'approved', admin_notes = ?, reviewed_at = NOW(), reviewed_by = ?
                    WHERE id = ?
                ");
                $stmt->execute([$adminNotes, $_SESSION['admin_user_id'] ?? null, $claimId]);

                // Merge results from anonymous rider to claiming rider
                if ($claim['claiming_rider_id']) {
                    // Move all results
                    $stmt = $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?");
                    $stmt->execute([$claim['claiming_rider_id'], $claim['anonymous_rider_id']]);

                    // Mark anonymous rider as merged
                    $stmt = $pdo->prepare("
                        UPDATE riders
                        SET merged_into_rider_id = ?, is_anonymous = 1, active = 0
                        WHERE id = ?
                    ");
                    $stmt->execute([$claim['claiming_rider_id'], $claim['anonymous_rider_id']]);

                    // Update claim to merged status
                    $stmt = $pdo->prepare("UPDATE artist_name_claims SET status = 'merged', merged_at = NOW() WHERE id = ?");
                    $stmt->execute([$claimId]);

                    // Log in rider_merge_map for audit
                    $stmt = $pdo->prepare("
                        INSERT INTO rider_merge_map (source_rider_id, target_rider_id, merge_reason, created_at)
                        VALUES (?, ?, 'Artist name claim approved', NOW())
                    ");
                    $stmt->execute([$claim['anonymous_rider_id'], $claim['claiming_rider_id']]);
                }

                $pdo->commit();
                $message = 'Claim godkand och resultat sammanfogade';
            } catch (Exception $e) {
                $pdo->rollBack();
                $error = 'Fel vid sammanslagning: ' . $e->getMessage();
            }
        }

    } elseif ($action === 'reject_claim') {
        $claimId = (int)$_POST['claim_id'];
        $adminNotes = trim($_POST['admin_notes'] ?? '');

        $stmt = $pdo->prepare("
            UPDATE artist_name_claims
            SET status = 'rejected', admin_notes = ?, reviewed_at = NOW(), reviewed_by = ?
            WHERE id = ?
        ");
        $stmt->execute([$adminNotes, $_SESSION['admin_user_id'] ?? null, $claimId]);
        $message = 'Claim avvisad';

    } elseif ($action === 'manual_link') {
        // Admin manually links an anonymous rider to a real rider
        $anonymousId = (int)$_POST['anonymous_rider_id'];
        $targetId = (int)$_POST['target_rider_id'];

        if ($anonymousId && $targetId && $anonymousId !== $targetId) {
            $pdo->beginTransaction();
            try {
                // Move all results
                $stmt = $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?");
                $stmt->execute([$targetId, $anonymousId]);

                // Mark anonymous rider as merged
                $stmt = $pdo->prepare("
                    UPDATE riders
                    SET merged_into_rider_id = ?, active = 0
                    WHERE id = ?
                ");
                $stmt->execute([$targetId, $anonymousId]);

                // Log in rider_merge_map
                $stmt = $pdo->prepare("
                    INSERT INTO rider_merge_map (source_rider_id, target_rider_id, merge_reason, created_at)
                    VALUES (?, ?, 'Manual artist name linking by admin', NOW())
                ");
                $stmt->execute([$anonymousId, $targetId]);

                $pdo->commit();
                $message = 'Artistnamn lankat till deltagare';
            } catch (Exception $e) {
                $pdo->rollBack();
                $error = 'Fel vid lankning: ' . $e->getMessage();
            }
        } else {
            $error = 'Ogiltiga rider IDs';
        }

    } elseif ($action === 'auto_detect') {
        // Auto-detect anonymous riders based on criteria
        $stmt = $pdo->prepare("
            UPDATE riders
            SET is_anonymous = 1
            WHERE (lastname IS NULL OR lastname = '')
              AND (birth_year IS NULL OR birth_year = 0)
              AND club_id IS NULL
              AND firstname IS NOT NULL AND firstname != ''
              AND is_anonymous = 0
              AND merged_into_rider_id IS NULL
        ");
        $stmt->execute();
        $count = $stmt->rowCount();
        $message = "$count nya anonyma deltagare identifierade";
    }
}

// Get statistics
$stats = [];
if ($tablesExist) {
    try {
        // Check if is_anonymous column exists
        $hasColumn = false;
        try {
            $pdo->query("SELECT is_anonymous FROM riders LIMIT 1");
            $hasColumn = true;
        } catch (Exception $e) {}

        if ($hasColumn) {
            $stats['anonymous_total'] = (int)$pdo->query("SELECT COUNT(*) FROM riders WHERE is_anonymous = 1 AND merged_into_rider_id IS NULL")->fetchColumn();
            $stats['merged_total'] = (int)$pdo->query("SELECT COUNT(*) FROM riders WHERE merged_into_rider_id IS NOT NULL")->fetchColumn();
        } else {
            // Estimate based on criteria
            $stats['anonymous_total'] = (int)$pdo->query("
                SELECT COUNT(*) FROM riders
                WHERE (lastname IS NULL OR lastname = '')
                  AND (birth_year IS NULL OR birth_year = 0)
                  AND club_id IS NULL
                  AND firstname IS NOT NULL AND firstname != ''
            ")->fetchColumn();
            $stats['merged_total'] = 0;
        }

        // Claims stats
        try {
            $stats['pending_claims'] = (int)$pdo->query("SELECT COUNT(*) FROM artist_name_claims WHERE status = 'pending'")->fetchColumn();
            $stats['approved_claims'] = (int)$pdo->query("SELECT COUNT(*) FROM artist_name_claims WHERE status IN ('approved', 'merged')")->fetchColumn();
        } catch (Exception $e) {
            $stats['pending_claims'] = 0;
            $stats['approved_claims'] = 0;
        }
    } catch (Exception $e) {
        $stats = ['anonymous_total' => 0, 'merged_total' => 0, 'pending_claims' => 0, 'approved_claims' => 0];
    }
}

// Get anonymous riders list
$anonymousRiders = [];
$pendingClaims = [];
if ($tablesExist) {
    try {
        // Get anonymous riders with result counts
        $hasColumn = false;
        try {
            $pdo->query("SELECT is_anonymous FROM riders LIMIT 1");
            $hasColumn = true;
        } catch (Exception $e) {}

        if ($hasColumn) {
            $anonymousRiders = $pdo->query("
                SELECT r.id, r.firstname, r.anonymous_source,
                       COUNT(DISTINCT res.id) as result_count,
                       MIN(YEAR(e.date)) as first_year,
                       MAX(YEAR(e.date)) as last_year,
                       GROUP_CONCAT(DISTINCT s.name ORDER BY s.name SEPARATOR ', ') as series_names
                FROM riders r
                LEFT JOIN results res ON r.id = res.cyclist_id
                LEFT JOIN events e ON res.event_id = e.id
                LEFT JOIN series s ON e.series_id = s.id
                WHERE r.is_anonymous = 1 AND r.merged_into_rider_id IS NULL
                GROUP BY r.id
                ORDER BY result_count DESC, r.firstname
                LIMIT 200
            ")->fetchAll(PDO::FETCH_ASSOC);
        } else {
            // Use criteria-based detection
            $anonymousRiders = $pdo->query("
                SELECT r.id, r.firstname, NULL as anonymous_source,
                       COUNT(DISTINCT res.id) as result_count,
                       MIN(YEAR(e.date)) as first_year,
                       MAX(YEAR(e.date)) as last_year,
                       GROUP_CONCAT(DISTINCT s.name ORDER BY s.name SEPARATOR ', ') as series_names
                FROM riders r
                LEFT JOIN results res ON r.id = res.cyclist_id
                LEFT JOIN events e ON res.event_id = e.id
                LEFT JOIN series s ON e.series_id = s.id
                WHERE (r.lastname IS NULL OR r.lastname = '')
                  AND (r.birth_year IS NULL OR r.birth_year = 0)
                  AND r.club_id IS NULL
                  AND r.firstname IS NOT NULL AND r.firstname != ''
                GROUP BY r.id
                ORDER BY result_count DESC, r.firstname
                LIMIT 200
            ")->fetchAll(PDO::FETCH_ASSOC);
        }

        // Get pending claims
        try {
            $pendingClaims = $pdo->query("
                SELECT ac.*,
                       ar.firstname as anonymous_name,
                       cr.firstname as claiming_firstname, cr.lastname as claiming_lastname,
                       u.username as claiming_username
                FROM artist_name_claims ac
                JOIN riders ar ON ac.anonymous_rider_id = ar.id
                LEFT JOIN riders cr ON ac.claiming_rider_id = cr.id
                LEFT JOIN users u ON ac.claiming_user_id = u.id
                WHERE ac.status = 'pending'
                ORDER BY ac.created_at DESC
            ")->fetchAll(PDO::FETCH_ASSOC);
        } catch (Exception $e) {
            $pendingClaims = [];
        }
    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}

// Search for potential matches
$searchResults = [];
$searchQuery = $_GET['search'] ?? '';
if ($searchQuery && strlen($searchQuery) >= 2) {
    $searchTerm = '%' . $searchQuery . '%';
    $stmt = $pdo->prepare("
        SELECT r.id, r.firstname, r.lastname, r.birth_year,
               c.name as club_name,
               COUNT(DISTINCT res.id) as result_count
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        LEFT JOIN results res ON r.id = res.cyclist_id
        WHERE (r.firstname LIKE ? OR r.lastname LIKE ? OR CONCAT(r.firstname, ' ', r.lastname) LIKE ?)
          AND r.lastname IS NOT NULL AND r.lastname != ''
        GROUP BY r.id
        ORDER BY result_count DESC
        LIMIT 20
    ");
    $stmt->execute([$searchTerm, $searchTerm, $searchTerm]);
    $searchResults = $stmt->fetchAll(PDO::FETCH_ASSOC);
}

$page_title = 'Artistnamn-koppling';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Artistnamn-koppling']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}
.stat-box {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    text-align: center;
}
.stat-box.warning { border-color: var(--color-warning); }
.stat-box.success { border-color: var(--color-success); }
.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-accent);
}
.stat-label {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
    margin-top: var(--space-xs);
}
.anonymous-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-sm);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-md);
}
.anonymous-info {
    flex: 1;
}
.anonymous-name {
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--color-text-primary);
}
.anonymous-meta {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}
.anonymous-actions {
    display: flex;
    gap: var(--space-xs);
    flex-shrink: 0;
}
.claim-card {
    background: var(--color-bg-surface);
    border: 2px solid var(--color-warning);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
}
.claim-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--space-md);
}
.search-result {
    padding: var(--space-sm);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.search-result:last-child { border-bottom: none; }
.search-result:hover { background: var(--color-bg-hover); }

/* Mobile Edge-to-Edge */
@media (max-width: 767px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--space-sm);
    }
    .stat-box {
        padding: var(--space-md);
    }
    .stat-value {
        font-size: 1.5rem;
    }
    .admin-card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
    .anonymous-card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
        flex-direction: column;
        align-items: stretch;
    }
    .anonymous-actions {
        margin-top: var(--space-sm);
        justify-content: flex-end;
    }
    .claim-card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
    .admin-table-container {
        margin-left: -16px;
        margin-right: -16px;
        overflow-x: auto;
    }
}
</style>

<?php if (!$tablesExist): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Migrering kravs</strong><br>
        Kor migrering <code>024_artist_name_linking.sql</code> via
        <a href="/admin/migrations.php">Migrationsverktyget</a>.
    </div>
</div>
<?php else: ?>

<?php if ($message): ?>
    <div class="alert alert-success" style="margin-bottom: var(--space-md);"><?= htmlspecialchars($message) ?></div>
<?php endif; ?>
<?php if ($error): ?>
    <div class="alert alert-danger" style="margin-bottom: var(--space-md);"><?= htmlspecialchars($error) ?></div>
<?php endif; ?>

<!-- Statistics -->
<div class="stats-grid">
    <div class="stat-box warning">
        <div class="stat-value"><?= number_format($stats['anonymous_total']) ?></div>
        <div class="stat-label">Anonyma deltagare</div>
    </div>
    <div class="stat-box">
        <div class="stat-value"><?= number_format($stats['pending_claims']) ?></div>
        <div class="stat-label">Vantande claims</div>
    </div>
    <div class="stat-box success">
        <div class="stat-value"><?= number_format($stats['approved_claims']) ?></div>
        <div class="stat-label">Godkanda</div>
    </div>
    <div class="stat-box success">
        <div class="stat-value"><?= number_format($stats['merged_total']) ?></div>
        <div class="stat-label">Sammanfogade</div>
    </div>
</div>

<!-- Auto-detect button -->
<div class="admin-card" style="margin-bottom: var(--space-lg);">
    <div class="admin-card-body" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:var(--space-md);">
        <div>
            <strong>Auto-detektera anonyma deltagare</strong>
            <p style="margin:var(--space-xs) 0 0;color:var(--color-text-secondary);font-size:0.875rem;">
                Hitta deltagare med endast fornamn (inget efternamn, fodelsar eller klubb)
            </p>
        </div>
        <form method="POST" style="display:inline;">
            <input type="hidden" name="action" value="auto_detect">
            <button type="submit" class="btn-admin btn-admin-secondary">
                <i data-lucide="scan"></i> Skanna databas
            </button>
        </form>
    </div>
</div>

<!-- Pending Claims -->
<?php if (!empty($pendingClaims)): ?>
<div class="admin-card" style="margin-bottom: var(--space-lg);">
    <div class="admin-card-header">
        <h2><i data-lucide="inbox"></i> Vantande claims (<?= count($pendingClaims) ?>)</h2>
    </div>
    <div class="admin-card-body">
        <?php foreach ($pendingClaims as $claim): ?>
        <div class="claim-card">
            <div class="claim-header">
                <div>
                    <div style="font-weight:600;font-size:1.1rem;">
                        "<?= htmlspecialchars($claim['anonymous_name']) ?>"
                        <i data-lucide="arrow-right" style="width:16px;height:16px;"></i>
                        <?= htmlspecialchars($claim['claiming_firstname'] . ' ' . $claim['claiming_lastname']) ?>
                    </div>
                    <div style="color:var(--color-text-secondary);font-size:0.875rem;margin-top:var(--space-xs);">
                        Skapad: <?= date('Y-m-d H:i', strtotime($claim['created_at'])) ?>
                        <?php if ($claim['claiming_username']): ?>
                        | Anvandare: <?= htmlspecialchars($claim['claiming_username']) ?>
                        <?php endif; ?>
                    </div>
                </div>
                <span class="badge badge-warning">Vantar</span>
            </div>

            <?php if ($claim['evidence']): ?>
            <div style="background:var(--color-bg-page);padding:var(--space-md);border-radius:var(--radius-sm);margin-bottom:var(--space-md);">
                <strong>Motivering:</strong><br>
                <?= nl2br(htmlspecialchars($claim['evidence'])) ?>
            </div>
            <?php endif; ?>

            <div style="display:flex;gap:var(--space-md);flex-wrap:wrap;">
                <form method="POST" style="flex:1;min-width:200px;">
                    <input type="hidden" name="action" value="approve_claim">
                    <input type="hidden" name="claim_id" value="<?= $claim['id'] ?>">
                    <input type="text" name="admin_notes" class="form-input" placeholder="Admin-anteckning (valfritt)" style="margin-bottom:var(--space-xs);">
                    <button type="submit" class="btn-admin btn-admin-primary" onclick="return confirm('Godkann och slå samman resultat?')">
                        <i data-lucide="check"></i> Godkann & Sammanfoga
                    </button>
                </form>
                <form method="POST">
                    <input type="hidden" name="action" value="reject_claim">
                    <input type="hidden" name="claim_id" value="<?= $claim['id'] ?>">
                    <button type="submit" class="btn-admin btn-admin-danger" onclick="return confirm('Avvisa denna claim?')">
                        <i data-lucide="x"></i> Avvisa
                    </button>
                </form>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php endif; ?>

<!-- Manual Linking Tool -->
<div class="admin-card" style="margin-bottom: var(--space-lg);">
    <div class="admin-card-header">
        <h2><i data-lucide="link"></i> Manuell koppling</h2>
    </div>
    <div class="admin-card-body">
        <p style="color:var(--color-text-secondary);margin-bottom:var(--space-md);">
            Sok efter en deltagare for att linka ett artistnamn till deras profil.
        </p>

        <form method="GET" style="display:flex;gap:var(--space-md);margin-bottom:var(--space-lg);">
            <input type="text" name="search" class="form-input" value="<?= htmlspecialchars($searchQuery) ?>"
                   placeholder="Sok deltagare (fornamn, efternamn)..." style="flex:1;">
            <button type="submit" class="btn-admin btn-admin-primary">
                <i data-lucide="search"></i> Sok
            </button>
        </form>

        <?php if (!empty($searchResults)): ?>
        <div style="background:var(--color-bg-page);border-radius:var(--radius-md);max-height:300px;overflow-y:auto;">
            <?php foreach ($searchResults as $r): ?>
            <div class="search-result">
                <div>
                    <strong><?= htmlspecialchars($r['firstname'] . ' ' . $r['lastname']) ?></strong>
                    <?php if ($r['birth_year']): ?>
                    <span style="color:var(--color-text-muted);">(<?= $r['birth_year'] ?>)</span>
                    <?php endif; ?>
                    <?php if ($r['club_name']): ?>
                    <br><span style="font-size:0.875rem;color:var(--color-text-secondary);"><?= htmlspecialchars($r['club_name']) ?></span>
                    <?php endif; ?>
                </div>
                <div style="display:flex;align-items:center;gap:var(--space-sm);">
                    <span class="badge"><?= $r['result_count'] ?> resultat</span>
                    <button type="button" class="btn-admin btn-admin-sm btn-admin-secondary"
                            onclick="selectTargetRider(<?= $r['id'] ?>, '<?= htmlspecialchars(addslashes($r['firstname'] . ' ' . $r['lastname'])) ?>')">
                        Valj
                    </button>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php elseif ($searchQuery): ?>
        <p style="text-align:center;color:var(--color-text-muted);padding:var(--space-lg);">
            Inga resultat for "<?= htmlspecialchars($searchQuery) ?>"
        </p>
        <?php endif; ?>

        <!-- Link form (shown when target is selected) -->
        <div id="link-form" style="display:none;margin-top:var(--space-lg);padding:var(--space-lg);background:var(--color-accent-light);border-radius:var(--radius-md);">
            <form method="POST">
                <input type="hidden" name="action" value="manual_link">
                <input type="hidden" name="target_rider_id" id="target-rider-id">

                <div style="margin-bottom:var(--space-md);">
                    <strong>Maldeltagare:</strong> <span id="target-rider-name"></span>
                </div>

                <div class="form-group" style="margin-bottom:var(--space-md);">
                    <label class="form-label">Valj artistnamn att linka:</label>
                    <select name="anonymous_rider_id" class="form-select" required>
                        <option value="">-- Valj artistnamn --</option>
                        <?php foreach ($anonymousRiders as $ar): ?>
                        <option value="<?= $ar['id'] ?>">
                            <?= htmlspecialchars($ar['firstname']) ?>
                            (<?= $ar['result_count'] ?> resultat, <?= $ar['first_year'] ?>-<?= $ar['last_year'] ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <button type="submit" class="btn-admin btn-admin-primary" onclick="return confirm('Sammanfoga alla resultat fran artistnamnet till den valda deltagaren?')">
                    <i data-lucide="merge"></i> Sammanfoga
                </button>
                <button type="button" class="btn-admin btn-admin-secondary" onclick="cancelLink()">Avbryt</button>
            </form>
        </div>
    </div>
</div>

<!-- Anonymous Riders List -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="users"></i> Anonyma deltagare (<?= count($anonymousRiders) ?>)</h2>
    </div>
    <div class="admin-card-body">
        <?php if (empty($anonymousRiders)): ?>
        <p style="text-align:center;color:var(--color-text-muted);padding:var(--space-2xl);">
            Inga anonyma deltagare hittades. Klicka "Skanna databas" for att identifiera dem.
        </p>
        <?php else: ?>
        <div style="max-height:500px;overflow-y:auto;">
            <?php foreach ($anonymousRiders as $ar): ?>
            <div class="anonymous-card">
                <div class="anonymous-info">
                    <div class="anonymous-name">
                        <a href="/rider/<?= $ar['id'] ?>" target="_blank"><?= htmlspecialchars($ar['firstname']) ?></a>
                    </div>
                    <div class="anonymous-meta">
                        <?= $ar['result_count'] ?> resultat |
                        <?= $ar['first_year'] ?>-<?= $ar['last_year'] ?>
                        <?php if ($ar['series_names']): ?>
                        | <?= htmlspecialchars($ar['series_names']) ?>
                        <?php endif; ?>
                        <?php if ($ar['anonymous_source']): ?>
                        <br><em>Kalla: <?= htmlspecialchars($ar['anonymous_source']) ?></em>
                        <?php endif; ?>
                    </div>
                </div>
                <div class="anonymous-actions">
                    <a href="/rider/<?= $ar['id'] ?>" target="_blank" class="btn-admin btn-admin-sm btn-admin-ghost" title="Visa profil">
                        <i data-lucide="external-link"></i>
                    </a>
                    <button type="button" class="btn-admin btn-admin-sm btn-admin-secondary"
                            onclick="quickLink(<?= $ar['id'] ?>, '<?= htmlspecialchars(addslashes($ar['firstname'])) ?>')">
                        <i data-lucide="link"></i> Linka
                    </button>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Quick Link Modal -->
<div id="quick-link-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:1000;align-items:center;justify-content:center;">
    <div style="background:var(--color-bg-surface);border-radius:var(--radius-lg);padding:var(--space-xl);max-width:500px;width:90%;max-height:90vh;overflow-y:auto;">
        <h3 style="margin-bottom:var(--space-lg);">
            <i data-lucide="link" style="width:20px;height:20px;vertical-align:middle;margin-right:var(--space-xs);"></i>
            Linka artistnamn
        </h3>
        <form method="POST" id="quick-link-form">
            <input type="hidden" name="action" value="manual_link">
            <input type="hidden" name="anonymous_rider_id" id="quick-anonymous-id">

            <div class="form-group" style="margin-bottom:var(--space-md);">
                <label class="form-label">Artistnamn</label>
                <input type="text" id="quick-anonymous-name" class="form-input" readonly style="background:var(--color-bg-page);">
            </div>

            <div class="form-group" style="margin-bottom:var(--space-md);">
                <label class="form-label">Sok maldeltagare</label>
                <input type="text" id="quick-search" class="form-input" placeholder="Sok pa namn..." onkeyup="quickSearch(this.value)">
            </div>

            <div id="quick-search-results" style="max-height:200px;overflow-y:auto;background:var(--color-bg-page);border-radius:var(--radius-sm);margin-bottom:var(--space-md);">
                <p style="text-align:center;color:var(--color-text-muted);padding:var(--space-md);">
                    Skriv minst 2 tecken for att soka...
                </p>
            </div>

            <input type="hidden" name="target_rider_id" id="quick-target-id">
            <div id="quick-selected" style="display:none;padding:var(--space-md);background:var(--color-accent-light);border-radius:var(--radius-sm);margin-bottom:var(--space-md);">
                <strong>Vald:</strong> <span id="quick-selected-name"></span>
            </div>

            <div style="display:flex;gap:var(--space-md);justify-content:flex-end;">
                <button type="button" class="btn-admin btn-admin-secondary" onclick="closeQuickLink()">Avbryt</button>
                <button type="submit" id="quick-submit" class="btn-admin btn-admin-primary" disabled onclick="return confirm('Sammanfoga alla resultat?')">
                    <i data-lucide="merge"></i> Sammanfoga
                </button>
            </div>
        </form>
    </div>
</div>

<script>
function selectTargetRider(id, name) {
    document.getElementById('target-rider-id').value = id;
    document.getElementById('target-rider-name').textContent = name;
    document.getElementById('link-form').style.display = 'block';
}

function cancelLink() {
    document.getElementById('link-form').style.display = 'none';
}

function quickLink(anonymousId, anonymousName) {
    document.getElementById('quick-anonymous-id').value = anonymousId;
    document.getElementById('quick-anonymous-name').value = anonymousName;
    document.getElementById('quick-target-id').value = '';
    document.getElementById('quick-selected').style.display = 'none';
    document.getElementById('quick-submit').disabled = true;
    document.getElementById('quick-search').value = '';
    document.getElementById('quick-search-results').innerHTML = '<p style="text-align:center;color:var(--color-text-muted);padding:var(--space-md);">Skriv minst 2 tecken for att soka...</p>';
    document.getElementById('quick-link-modal').style.display = 'flex';
}

function closeQuickLink() {
    document.getElementById('quick-link-modal').style.display = 'none';
}

let searchTimeout;
function quickSearch(query) {
    clearTimeout(searchTimeout);
    if (query.length < 2) {
        document.getElementById('quick-search-results').innerHTML = '<p style="text-align:center;color:var(--color-text-muted);padding:var(--space-md);">Skriv minst 2 tecken for att soka...</p>';
        return;
    }

    searchTimeout = setTimeout(() => {
        fetch('/admin/artist-name-linking.php?search=' + encodeURIComponent(query) + '&ajax=1')
            .then(r => r.text())
            .then(html => {
                // Parse the search results from the page
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const results = doc.querySelectorAll('.search-result');

                if (results.length === 0) {
                    document.getElementById('quick-search-results').innerHTML = '<p style="text-align:center;color:var(--color-text-muted);padding:var(--space-md);">Inga resultat</p>';
                    return;
                }

                let resultHtml = '';
                results.forEach(r => {
                    const btn = r.querySelector('button');
                    if (btn) {
                        const onclick = btn.getAttribute('onclick');
                        const match = onclick.match(/selectTargetRider\((\d+),\s*'([^']+)'\)/);
                        if (match) {
                            const id = match[1];
                            const name = match[2];
                            resultHtml += `
                                <div style="padding:var(--space-sm);border-bottom:1px solid var(--color-border);display:flex;justify-content:space-between;align-items:center;cursor:pointer;"
                                     onclick="selectQuickTarget(${id}, '${name}')">
                                    <span>${name}</span>
                                    <i data-lucide="chevron-right" style="width:16px;height:16px;"></i>
                                </div>
                            `;
                        }
                    }
                });

                document.getElementById('quick-search-results').innerHTML = resultHtml || '<p style="text-align:center;color:var(--color-text-muted);padding:var(--space-md);">Inga resultat</p>';
                lucide.createIcons();
            });
    }, 300);
}

function selectQuickTarget(id, name) {
    document.getElementById('quick-target-id').value = id;
    document.getElementById('quick-selected-name').textContent = name;
    document.getElementById('quick-selected').style.display = 'block';
    document.getElementById('quick-submit').disabled = false;
}

// Close modal on outside click
document.getElementById('quick-link-modal')?.addEventListener('click', function(e) {
    if (e.target === this) closeQuickLink();
});
</script>

<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
