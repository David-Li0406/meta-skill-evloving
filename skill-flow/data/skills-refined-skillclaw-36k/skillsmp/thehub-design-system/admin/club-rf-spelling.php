<?php
/**
 * Club Federation Spelling Check Tool
 * Compare club names against official SCF/NCF/DCU registries and update spellings
 * Version: v1.1.0 [2026-01-16]
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';

// Ensure required columns exist
try {
    $stmt = $db->query("SHOW COLUMNS FROM clubs LIKE 'name_locked'");
    if ($stmt->rowCount() === 0) {
        $db->exec("ALTER TABLE clubs ADD COLUMN name_locked TINYINT(1) DEFAULT 0 AFTER name");
    }
    $stmt = $db->query("SHOW COLUMNS FROM clubs LIKE 'federation'");
    if ($stmt->rowCount() === 0) {
        $db->exec("ALTER TABLE clubs ADD COLUMN federation VARCHAR(10) DEFAULT NULL AFTER scf_district");
        // Set federation for existing RF clubs
        $db->exec("UPDATE clubs SET federation = 'SCF' WHERE rf_registered = 1 AND scf_district IS NOT NULL AND scf_district != ''");
    }
} catch (Exception $e) {
    // Columns might already exist
}

// Build index of official names from all federations
$allFederationClubs = [];

// Load federation data file (shared between tools)
require_once __DIR__ . '/includes/federation-clubs-data.php';

// SCF (Swedish Cycling Federation)
foreach ($scf_districts as $district => $clubs) {
    foreach ($clubs as $clubName) {
        $allFederationClubs[mb_strtolower($clubName, 'UTF-8')] = [
            'name' => $clubName,
            'federation' => 'SCF',
            'district' => $district
        ];
    }
}

// NCF (Norwegian Cycling Federation)
if (isset($ncf_clubs)) {
    foreach ($ncf_clubs as $clubName) {
        $allFederationClubs[mb_strtolower($clubName, 'UTF-8')] = [
            'name' => $clubName,
            'federation' => 'NCF',
            'district' => 'Norge'
        ];
    }
}

// DCU (Danish Cycling Union)
if (isset($dcu_districts)) {
    foreach ($dcu_districts as $district => $clubs) {
        foreach ($clubs as $clubName) {
            $allFederationClubs[mb_strtolower($clubName, 'UTF-8')] = [
                'name' => $clubName,
                'federation' => 'DCU',
                'district' => $district
            ];
        }
    }
}

// Handle lock action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['lock_club'])) {
    checkCsrf();
    $clubId = (int)$_POST['lock_club'];
    $db->update('clubs', ['name_locked' => 1], 'id = ?', [$clubId]);
    $message = 'Klubbnamnet har låsts';
    $messageType = 'success';
}

// Handle unlock action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['unlock_club'])) {
    checkCsrf();
    $clubId = (int)$_POST['unlock_club'];
    $db->update('clubs', ['name_locked' => 0], 'id = ?', [$clubId]);
    $message = 'Klubbnamnet har låsts upp';
    $messageType = 'info';
}

// Handle update name action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['update_name'])) {
    checkCsrf();
    $clubId = (int)$_POST['club_id'];
    $newName = trim($_POST['new_name']);
    $federation = trim($_POST['federation'] ?? '');
    $lockAfter = isset($_POST['lock_after']);

    if ($clubId && $newName) {
        $updateData = ['name' => $newName];
        if ($federation) {
            $updateData['federation'] = $federation;
        }
        if ($lockAfter) {
            $updateData['name_locked'] = 1;
        }
        $db->update('clubs', $updateData, 'id = ?', [$clubId]);
        $message = "Uppdaterade klubbnamn till: $newName" . ($lockAfter ? ' (låst)' : '');
        $messageType = 'success';
    }
}

// Handle bulk update action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['bulk_update'])) {
    checkCsrf();
    $updates = $_POST['updates'] ?? [];
    $federations = $_POST['federations'] ?? [];
    $lockAll = isset($_POST['lock_all']);
    $updated = 0;

    foreach ($updates as $clubId => $newName) {
        if (!empty($newName)) {
            $updateData = ['name' => trim($newName)];
            if (isset($federations[$clubId])) {
                $updateData['federation'] = $federations[$clubId];
            }
            if ($lockAll) {
                $updateData['name_locked'] = 1;
            }
            $db->update('clubs', $updateData, 'id = ?', [(int)$clubId]);
            $updated++;
        }
    }

    if ($updated > 0) {
        $message = "Uppdaterade $updated klubbnamn" . ($lockAll ? ' och låste alla' : '');
        $messageType = 'success';
    }
}

// Get all RF-registered clubs from database
$clubs = $db->getAll("
    SELECT c.id, c.name, c.name_locked, c.scf_district, c.federation, c.rf_registered,
           COUNT(r.id) as rider_count
    FROM clubs c
    LEFT JOIN riders r ON c.id = r.club_id
    WHERE c.rf_registered = 1
    GROUP BY c.id
    ORDER BY c.name
");

// Find spelling differences
$spellingDiffs = [];
$exactMatches = [];
$notInRegistry = [];

foreach ($clubs as $club) {
    $clubNameLower = mb_strtolower($club['name'], 'UTF-8');
    $found = false;

    // Try exact match first
    if (isset($allFederationClubs[$clubNameLower])) {
        $club['matched_federation'] = $allFederationClubs[$clubNameLower]['federation'];
        $exactMatches[] = $club;
        $found = true;
    } else {
        // Try to find similar name
        foreach ($allFederationClubs as $fedLower => $fedData) {
            // Check if names are similar (one contains the other, or levenshtein is low)
            $lev = levenshtein(substr($clubNameLower, 0, 50), substr($fedLower, 0, 50));
            $maxLen = max(strlen($clubNameLower), strlen($fedLower));
            $similarity = (1 - ($lev / $maxLen)) * 100;

            if ($similarity >= 80 && $club['name'] !== $fedData['name']) {
                $spellingDiffs[] = [
                    'club' => $club,
                    'official_name' => $fedData['name'],
                    'federation' => $fedData['federation'],
                    'district' => $fedData['district'],
                    'similarity' => round($similarity)
                ];
                $found = true;
                break;
            }
        }
    }

    if (!$found) {
        $notInRegistry[] = $club;
    }
}

// Sort spelling diffs by similarity (most similar first)
usort($spellingDiffs, function($a, $b) {
    return $b['similarity'] - $a['similarity'];
});

/**
 * Get federation badge HTML
 */
function getFederationBadge($federation) {
    $colors = [
        'SCF' => 'primary',    // Swedish - blue
        'NCF' => 'error',      // Norwegian - red
        'DCU' => 'warning'     // Danish - yellow/red
    ];
    $titles = [
        'SCF' => 'Svenska Cykelförbundet',
        'NCF' => 'Norges Cykleforbund',
        'DCU' => 'Danmarks Cykle Union'
    ];
    $color = $colors[$federation] ?? 'secondary';
    $title = $titles[$federation] ?? $federation;
    return '<span class="badge badge-' . $color . '" title="' . h($title) . '">' . h($federation) . '</span>';
}

// Page config for unified layout
$page_title = 'Förbundets Stavningskontroll';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Stavningskontroll']
];
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Header -->
<div class="flex justify-between items-center mb-lg">
    <div>
        <h1 class="">
            <i data-lucide="spell-check"></i>
            Förbundets Stavningskontroll
        </h1>
        <p class="text-secondary">
            Jämför klubbnamn mot officiella SCF/NCF/DCU-register och uppdatera stavningar
        </p>
    </div>
    <a href="/admin/clubs.php" class="btn btn--secondary">
        <i data-lucide="arrow-left"></i>
        Tillbaka
    </a>
</div>

<?php if ($message): ?>
    <div class="alert alert-<?= h($messageType) ?> mb-lg">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'info' ?>"></i>
        <?= h($message) ?>
    </div>
<?php endif; ?>

<!-- Stats -->
<div class="grid grid-cols-2 gs-md-grid-cols-4 gap-md mb-lg">
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-primary"><?= count($clubs) ?></div>
            <div class="text-sm text-secondary">Förbundsregistrerade</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-success"><?= count($exactMatches) ?></div>
            <div class="text-sm text-secondary">Korrekt stavning</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-warning"><?= count($spellingDiffs) ?></div>
            <div class="text-sm text-secondary">Avvikande stavning</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-muted"><?= count($notInRegistry) ?></div>
            <div class="text-sm text-secondary">Ej i registret</div>
        </div>
    </div>
</div>

<!-- Federation legend -->
<div class="card mb-lg">
    <div class="card-body flex gap-lg items-center">
        <span class="text-secondary">Förbund:</span>
        <?= getFederationBadge('SCF') ?> <span class="text-sm">Svenska Cykelförbundet</span>
        <?= getFederationBadge('NCF') ?> <span class="text-sm">Norges Cykleforbund</span>
        <?= getFederationBadge('DCU') ?> <span class="text-sm">Danmarks Cykle Union</span>
    </div>
</div>

<?php if (!empty($spellingDiffs)): ?>
<!-- Spelling Differences -->
<div class="card mb-lg">
    <div class="card-header flex justify-between items-center">
        <h2 class="">
            <i data-lucide="alert-triangle"></i>
            Avvikande stavningar (<?= count($spellingDiffs) ?>)
        </h2>
    </div>
    <div class="card-body">
        <form method="POST">
            <?= csrf_field() ?>

            <div class="table-responsive mb-md">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Nuvarande namn</th>
                            <th>Officiellt namn</th>
                            <th>Förbund</th>
                            <th>Likhet</th>
                            <th>Deltagare</th>
                            <th>Uppdatera till</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($spellingDiffs as $diff): ?>
                            <tr class="<?= $diff['club']['name_locked'] ? 'gs-bg-success-light' : '' ?>">
                                <td>
                                    <strong><?= h($diff['club']['name']) ?></strong>
                                    <?php if ($diff['club']['name_locked']): ?>
                                        <span class="badge badge-success badge-sm" title="Låst namn">
                                            <i data-lucide="lock" class="icon-xs"></i>
                                        </span>
                                    <?php endif; ?>
                                    <?php if ($diff['club']['federation']): ?>
                                        <?= getFederationBadge($diff['club']['federation']) ?>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <strong class="text-accent"><?= h($diff['official_name']) ?></strong>
                                </td>
                                <td>
                                    <?= getFederationBadge($diff['federation']) ?>
                                    <span class="text-sm text-secondary d-block"><?= h($diff['district']) ?></span>
                                </td>
                                <td>
                                    <span class="badge badge-<?= $diff['similarity'] >= 90 ? 'success' : 'warning' ?>">
                                        <?= $diff['similarity'] ?>%
                                    </span>
                                </td>
                                <td>
                                    <?php if ($diff['club']['rider_count'] > 0): ?>
                                        <strong><?= $diff['club']['rider_count'] ?></strong>
                                    <?php else: ?>
                                        <span class="text-muted">0</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if (!$diff['club']['name_locked']): ?>
                                        <input type="hidden" name="updates[<?= $diff['club']['id'] ?>]" value="">
                                        <input type="hidden" name="federations[<?= $diff['club']['id'] ?>]" value="<?= h($diff['federation']) ?>">
                                        <label class="flex items-center gap-xs">
                                            <input type="checkbox"
                                                   onchange="this.parentElement.previousElementSibling.previousElementSibling.value = this.checked ? '<?= h(addslashes($diff['official_name'])) ?>' : ''">
                                            <span class="text-sm">Uppdatera</span>
                                        </label>
                                    <?php else: ?>
                                        <span class="text-muted text-sm">Låst</span>
                                    <?php endif; ?>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <div class="flex gap-md items-center">
                <button type="submit" name="bulk_update" value="1" class="btn btn-primary">
                    <i data-lucide="check"></i>
                    Uppdatera markerade
                </button>
                <label class="flex items-center gap-xs">
                    <input type="checkbox" name="lock_all" value="1">
                    <span>Lås alla uppdaterade namn</span>
                </label>
            </div>
        </form>
    </div>
</div>
<?php endif; ?>

<?php if (!empty($exactMatches)): ?>
<!-- Exact Matches -->
<div class="card mb-lg">
    <div class="card-header">
        <h2 class="">
            <i data-lucide="check-circle"></i>
            Korrekt stavning (<?= count($exactMatches) ?>)
        </h2>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Klubbnamn</th>
                        <th>Förbund</th>
                        <th>Distrikt</th>
                        <th>Deltagare</th>
                        <th>Status</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($exactMatches as $club): ?>
                        <tr>
                            <td>
                                <strong><?= h($club['name']) ?></strong>
                            </td>
                            <td>
                                <?= getFederationBadge($club['matched_federation'] ?? $club['federation'] ?? 'SCF') ?>
                            </td>
                            <td class="text-sm text-secondary"><?= h($club['scf_district'] ?? '-') ?></td>
                            <td>
                                <?php if ($club['rider_count'] > 0): ?>
                                    <strong><?= $club['rider_count'] ?></strong>
                                <?php else: ?>
                                    <span class="text-muted">0</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php if ($club['name_locked']): ?>
                                    <span class="badge badge-success">
                                        <i data-lucide="lock" class="icon-xs"></i> Låst
                                    </span>
                                <?php else: ?>
                                    <span class="badge badge-secondary">Olåst</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <form method="POST" style="display: inline;">
                                    <?= csrf_field() ?>
                                    <?php if ($club['name_locked']): ?>
                                        <button type="submit" name="unlock_club" value="<?= $club['id'] ?>"
                                                class="btn btn--sm btn--secondary">
                                            <i data-lucide="unlock"></i>
                                            Lås upp
                                        </button>
                                    <?php else: ?>
                                        <button type="submit" name="lock_club" value="<?= $club['id'] ?>"
                                                class="btn btn--sm btn-success">
                                            <i data-lucide="lock"></i>
                                            Lås
                                        </button>
                                    <?php endif; ?>
                                </form>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<?php if (!empty($notInRegistry)): ?>
<!-- Not in Registry -->
<div class="card mb-lg">
    <div class="card-header">
        <h2 class="">
            <i data-lucide="help-circle"></i>
            Förbundsmarkerade men ej i registret (<?= count($notInRegistry) ?>)
        </h2>
    </div>
    <div class="card-body">
        <p class="text-secondary mb-md">
            Dessa klubbar är markerade som förbundsregistrerade men matchar inte något namn i de officiella registren.
        </p>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Klubbnamn</th>
                        <th>Förbund</th>
                        <th>Registrerat distrikt</th>
                        <th>Deltagare</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($notInRegistry as $club): ?>
                        <tr>
                            <td>
                                <strong><?= h($club['name']) ?></strong>
                                <?php if ($club['name_locked']): ?>
                                    <span class="badge badge-success badge-sm">
                                        <i data-lucide="lock" class="icon-xs"></i>
                                    </span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php if ($club['federation']): ?>
                                    <?= getFederationBadge($club['federation']) ?>
                                <?php else: ?>
                                    <span class="text-muted">-</span>
                                <?php endif; ?>
                            </td>
                            <td class="text-sm text-secondary"><?= h($club['scf_district'] ?: '-') ?></td>
                            <td>
                                <?php if ($club['rider_count'] > 0): ?>
                                    <strong><?= $club['rider_count'] ?></strong>
                                <?php else: ?>
                                    <span class="text-muted">0</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <span class="badge badge-warning">Kontrollera manuellt</span>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<div class="gs-py-sm">
    <small class="text-secondary">Förbundets Stavningskontroll v1.1.0 [2026-01-16]</small>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
