<?php
/**
 * Enrich Riders Tool
 * Find and update riders with missing data
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';
$results = [];

// Handle enrichment
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'enrich_single') {
        $riderId = intval($_POST['rider_id']);
        $updates = [];

        if (!empty($_POST['birth_year'])) {
            $updates['birth_year'] = intval($_POST['birth_year']);
        }
        if (!empty($_POST['gender'])) {
            $updates['gender'] = $_POST['gender'];
        }
        if (!empty($_POST['club_id'])) {
            $updates['club_id'] = intval($_POST['club_id']);
        }
        if (!empty($_POST['nationality'])) {
            $updates['nationality'] = strtoupper(substr($_POST['nationality'], 0, 3));
        }

        if (!empty($updates)) {
            try {
                $db->update('riders', $updates, 'id = ?', [$riderId]);
                $message = 'Deltagare uppdaterad!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Find riders with missing data
$filter = $_GET['filter'] ?? 'missing_birth_year';

$filterConditions = [
    'missing_birth_year' => 'birth_year IS NULL OR birth_year = 0',
    'missing_gender' => "gender IS NULL OR gender = ''",
    'missing_club' => 'club_id IS NULL',
    'missing_nationality' => "nationality IS NULL OR nationality = ''",
    'has_swe_id' => "license_number LIKE 'SWE%'",
    'all_incomplete' => "(birth_year IS NULL OR birth_year = 0) OR (gender IS NULL OR gender = '') OR club_id IS NULL OR (nationality IS NULL OR nationality = '')"
];

$condition = $filterConditions[$filter] ?? $filterConditions['missing_birth_year'];

$riders = $db->getAll("
    SELECT r.*, c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE $condition
    ORDER BY r.lastname, r.firstname
    LIMIT 100
");

$clubs = $db->getAll("SELECT id, name FROM clubs WHERE active = 1 ORDER BY name");

// Stats
$stats = $db->getRow("
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN birth_year IS NULL OR birth_year = 0 THEN 1 ELSE 0 END) as missing_birth_year,
        SUM(CASE WHEN gender IS NULL OR gender = '' THEN 1 ELSE 0 END) as missing_gender,
        SUM(CASE WHEN club_id IS NULL THEN 1 ELSE 0 END) as missing_club,
        SUM(CASE WHEN nationality IS NULL OR nationality = '' THEN 1 ELSE 0 END) as missing_nationality
    FROM riders
");

$page_title = 'Berika Deltagardata';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Berika Deltagardata']
];
include __DIR__ . '/components/unified-layout.php';
?>

        <?php if ($message): ?>
        <div class="alert alert--<?= h($messageType) ?> mb-lg">
            <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
            <?= h($message) ?>
        </div>
        <?php endif; ?>

<!-- Stats -->
<div class="grid grid-cols-5 gap-md mb-lg">
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-primary"><?= $stats['total'] ?? 0 ?></div>
            <div class="text-sm text-secondary">Totalt deltagare</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-warning"><?= $stats['missing_birth_year'] ?? 0 ?></div>
            <div class="text-sm text-secondary">Saknar födelseår</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-warning"><?= $stats['missing_gender'] ?? 0 ?></div>
            <div class="text-sm text-secondary">Saknar kön</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-warning"><?= $stats['missing_club'] ?? 0 ?></div>
            <div class="text-sm text-secondary">Saknar klubb</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl text-warning"><?= $stats['missing_nationality'] ?? 0 ?></div>
            <div class="text-sm text-secondary">Saknar nationalitet</div>
        </div>
    </div>
</div>

        <!-- Filter -->
        <div class="card mb-lg">
            <div class="card-body">
                <form method="GET" class="flex gap-md items-end">
                    <div>
                        <label class="label">
                            <i data-lucide="filter"></i>
                            Visa deltagare som
                        </label>
                        <select name="filter" class="input" style="max-width: 250px;">
                            <option value="missing_birth_year" <?= $filter === 'missing_birth_year' ? 'selected' : '' ?>>Saknar födelseår</option>
                            <option value="missing_gender" <?= $filter === 'missing_gender' ? 'selected' : '' ?>>Saknar kön</option>
                            <option value="missing_club" <?= $filter === 'missing_club' ? 'selected' : '' ?>>Saknar klubb</option>
                            <option value="missing_nationality" <?= $filter === 'missing_nationality' ? 'selected' : '' ?>>Saknar nationalitet</option>
                            <option value="has_swe_id" <?= $filter === 'has_swe_id' ? 'selected' : '' ?>>Har SWE ID</option>
                            <option value="all_incomplete" <?= $filter === 'all_incomplete' ? 'selected' : '' ?>>Alla med saknad data</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="filter"></i>
                        Filtrera
                    </button>
                </form>
            </div>
        </div>

        <!-- Results -->
        <div class="card">
            <div class="card-header">
                <h2>
                    <i data-lucide="users"></i>
                    Deltagare att berika (<?= count($riders) ?>)
                </h2>
            </div>
            <div class="card-body">
                <?php if (empty($riders)): ?>
                <div class="text-center py-xl">
                    <i data-lucide="check-circle" style="width: 48px; height: 48px; color: var(--color-success);"></i>
                    <p class="text-secondary mt-md">Inga deltagare med saknad data hittades!</p>
                </div>
                <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Namn</th>
                                <th>Licensnummer</th>
                                <th>Födelseår</th>
                                <th>Kön</th>
                                <th>Nationalitet</th>
                                <th>Klubb</th>
                                <th class="text-right">Åtgärder</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($riders as $rider): ?>
                            <tr id="rider-<?= $rider['id'] ?>">
                                <td>
                                    <strong><?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></strong>
                                </td>
                                <td>
                                    <?php if ($rider['license_number']): ?>
                                    <code class="text-primary"><?= h($rider['license_number']) ?></code>
                                    <?php else: ?>
                                    <span class="text-secondary">-</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($rider['birth_year']): ?>
                                    <?= h($rider['birth_year']) ?>
                                    <?php else: ?>
                                    <span class="badge badge--warning">Saknas</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($rider['gender']): ?>
                                    <?= $rider['gender'] === 'M' ? 'Man' : 'Kvinna' ?>
                                    <?php else: ?>
                                    <span class="badge badge--warning">Saknas</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if (!empty($rider['nationality'])): ?>
                                    <?= h($rider['nationality']) ?>
                                    <?php else: ?>
                                    <span class="badge badge--warning">Saknas</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($rider['club_name']): ?>
                                    <?= h($rider['club_name']) ?>
                                    <?php else: ?>
                                    <span class="badge badge--warning">Saknas</span>
                                    <?php endif; ?>
                                </td>
                                <td class="text-right">
                                    <button type="button" class="btn btn--primary btn--sm" onclick="editRider(<?= $rider['id'] ?>, <?= htmlspecialchars(json_encode($rider), ENT_QUOTES) ?>)">
                                        <i data-lucide="edit"></i>
                                        Redigera
                                    </button>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</main>

<!-- Edit Modal -->
<div id="editModal" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center;">
    <div class="card" style="width: 100%; max-width: 500px; margin: 1rem;">
        <div class="card-header">
            <h3 id="modalTitle">Redigera deltagare</h3>
        </div>
        <div class="card-body">
            <form id="editForm" method="POST">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="enrich_single">
                <input type="hidden" name="rider_id" id="editRiderId">

                <div class="form-group mb-md">
                    <label class="label">Födelseår</label>
                    <input type="number" name="birth_year" id="editBirthYear" class="input" min="1900" max="<?= date('Y') ?>">
                </div>

                <div class="form-group mb-md">
                    <label class="label">Kön</label>
                    <select name="gender" id="editGender" class="input">
                        <option value="">Välj...</option>
                        <option value="M">Man</option>
                        <option value="F">Kvinna</option>
                    </select>
                </div>

                <div class="form-group mb-md">
                    <label class="label">Nationalitet</label>
                    <input type="text" name="nationality" id="editNationality" class="input" maxlength="3" placeholder="SWE, NOR, FIN..." style="text-transform: uppercase;">
                    <small class="text-secondary">3-bokstavskod (ISO 3166-1 alpha-3)</small>
                </div>

                <div class="form-group mb-md">
                    <label class="label">Klubb</label>
                    <select name="club_id" id="editClubId" class="input">
                        <option value="">Ingen klubb</option>
                        <?php foreach ($clubs as $club): ?>
                        <option value="<?= $club['id'] ?>"><?= h($club['name']) ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <div class="flex gap-md justify-end">
                    <button type="button" class="btn btn--secondary" onclick="closeModal()">Avbryt</button>
                    <button type="submit" class="btn btn--primary">Spara</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
function editRider(id, rider) {
    document.getElementById('editRiderId').value = id;
    document.getElementById('editBirthYear').value = rider.birth_year || '';
    document.getElementById('editGender').value = rider.gender || '';
    document.getElementById('editNationality').value = rider.nationality || '';
    document.getElementById('editClubId').value = rider.club_id || '';
    document.getElementById('modalTitle').textContent = 'Redigera ' + rider.firstname + ' ' + rider.lastname;
    document.getElementById('editModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

document.getElementById('editModal').addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
