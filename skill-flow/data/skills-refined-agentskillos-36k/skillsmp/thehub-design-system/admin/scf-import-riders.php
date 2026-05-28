<?php
/**
 * SCF Import Riders Tool
 *
 * Search SCF License Portal for cyclists and import them into TheHUB.
 * Includes duplicate detection and manual review before creation.
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$apiKey = env('SCF_API_KEY', '');
$year = (int)($_GET['year'] ?? date('Y'));

// Initialize SCF service
require_once __DIR__ . '/../includes/SCFLicenseService.php';
$scfService = null;
if ($apiKey) {
    $scfService = new SCFLicenseService($apiKey, $db);
}

$page_title = 'Importera fran SCF';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Importera fran SCF']
];

// Handle actions
$message = '';
$messageType = 'info';
$searchResults = [];
$duplicateWarnings = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $apiKey) {
    $csrfToken = $_POST['csrf_token'] ?? '';
    if (!verify_csrf_token($csrfToken)) {
        $message = 'CSRF-validering misslyckades.';
        $messageType = 'error';
    } else {
        $action = $_POST['action'] ?? '';

        if ($action === 'search') {
            // Search SCF by name
            $firstname = trim($_POST['firstname'] ?? '');
            $lastname = trim($_POST['lastname'] ?? '');
            $gender = trim($_POST['gender'] ?? 'M');

            if (empty($firstname) && empty($lastname)) {
                $message = 'Ange minst fornamn eller efternamn.';
                $messageType = 'warning';
            } else {
                $apiResults = $scfService->lookupByName($firstname, $lastname, $gender, null, $year);

                if (!empty($apiResults)) {
                    foreach ($apiResults as $scfData) {
                        // Check if already exists in TheHUB
                        $existingByUci = null;
                        $existingByName = null;

                        if (!empty($scfData['uci_id'])) {
                            $uciClean = preg_replace('/[^0-9]/', '', $scfData['uci_id']);
                            $existingByUci = $db->getRow("
                                SELECT id, firstname, lastname, license_number
                                FROM riders
                                WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?
                            ", [$uciClean]);
                        }

                        if (!$existingByUci) {
                            $existingByName = $db->getRow("
                                SELECT id, firstname, lastname, license_number, birth_year
                                FROM riders
                                WHERE LOWER(firstname) = LOWER(?)
                                AND LOWER(lastname) = LOWER(?)
                            ", [$scfData['firstname'], $scfData['lastname']]);
                        }

                        $searchResults[] = [
                            'scf' => $scfData,
                            'existing_by_uci' => $existingByUci,
                            'existing_by_name' => $existingByName
                        ];
                    }

                    $message = "Hittade " . count($apiResults) . " resultat i SCF.";
                    $messageType = 'success';
                } else {
                    $message = "Inga resultat hittades i SCF.";
                    $messageType = 'warning';
                }
            }
        }

        if ($action === 'search_uci') {
            // Search by UCI ID
            $uciId = trim($_POST['uci_id'] ?? '');
            $uciIdClean = preg_replace('/[^0-9]/', '', $uciId);

            if (empty($uciIdClean) || strlen($uciIdClean) < 8) {
                $message = 'Ange ett giltigt UCI ID.';
                $messageType = 'warning';
            } else {
                $apiResults = $scfService->lookupByUciIds([$uciIdClean], $year);

                if (!empty($apiResults)) {
                    foreach ($apiResults as $scfData) {
                        // Check if already exists
                        $existingByUci = $db->getRow("
                            SELECT id, firstname, lastname, license_number
                            FROM riders
                            WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?
                        ", [$uciIdClean]);

                        $searchResults[] = [
                            'scf' => $scfData,
                            'existing_by_uci' => $existingByUci,
                            'existing_by_name' => null
                        ];
                    }

                    $message = "Hittade cyklist i SCF.";
                    $messageType = 'success';
                } else {
                    $message = "UCI ID hittades inte i SCF.";
                    $messageType = 'warning';
                }
            }
        }

        if ($action === 'import') {
            // Import a rider from SCF
            $uciId = trim($_POST['import_uci_id'] ?? '');
            $firstname = trim($_POST['import_firstname'] ?? '');
            $lastname = trim($_POST['import_lastname'] ?? '');
            $gender = trim($_POST['import_gender'] ?? '');
            $birthYear = (int)($_POST['import_birth_year'] ?? 0);
            $nationality = trim($_POST['import_nationality'] ?? '');
            $clubName = trim($_POST['import_club'] ?? '');

            if (empty($firstname) || empty($lastname)) {
                $message = 'Namn saknas.';
                $messageType = 'error';
            } else {
                // Double-check for duplicates
                $uciClean = preg_replace('/[^0-9]/', '', $uciId);
                $existing = null;

                if (!empty($uciClean)) {
                    $existing = $db->getRow("
                        SELECT id, firstname, lastname
                        FROM riders
                        WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?
                    ", [$uciClean]);
                }

                if ($existing) {
                    $message = "Cyklist med detta UCI ID finns redan: {$existing['firstname']} {$existing['lastname']} (ID: {$existing['id']})";
                    $messageType = 'error';
                } else {
                    // Find or create club
                    $clubId = null;
                    if (!empty($clubName)) {
                        $existingClub = $db->getRow("SELECT id FROM clubs WHERE LOWER(name) = LOWER(?)", [$clubName]);
                        if ($existingClub) {
                            $clubId = $existingClub['id'];
                        } else {
                            // Create club
                            $db->query("INSERT INTO clubs (name, country, active) VALUES (?, 'SWE', 1)", [$clubName]);
                            $clubId = $db->lastInsertId();
                        }
                    }

                    // Create rider
                    $db->query("
                        INSERT INTO riders (
                            firstname, lastname, license_number, gender, birth_year,
                            nationality, club_id, active, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, NOW(), NOW())
                    ", [
                        $firstname,
                        $lastname,
                        $uciId ?: null,
                        $gender ?: null,
                        $birthYear ?: null,
                        $nationality ?: null,
                        $clubId
                    ]);

                    $newRiderId = $db->lastInsertId();

                    // If we have UCI ID, verify and sync license data
                    if (!empty($uciClean)) {
                        $apiResults = $scfService->lookupByUciIds([$uciClean], $year);
                        $licenseData = reset($apiResults);

                        if ($licenseData) {
                            $scfService->updateRiderLicense($newRiderId, $licenseData, $year);
                            $scfService->cacheLicense($licenseData, $year);
                        }
                    }

                    $message = "Cyklist \"{$firstname} {$lastname}\" skapad med ID {$newRiderId}!";
                    $messageType = 'success';
                }
            }
        }

        if ($action === 'link_existing') {
            // Link an SCF record to an existing rider
            $riderId = (int)($_POST['rider_id'] ?? 0);
            $uciId = trim($_POST['link_uci_id'] ?? '');

            if ($riderId && !empty($uciId)) {
                // Update rider with UCI ID
                $db->query("
                    UPDATE riders
                    SET license_number = ?,
                        updated_at = NOW()
                    WHERE id = ?
                ", [$uciId, $riderId]);

                // Verify and sync license data
                $uciClean = preg_replace('/[^0-9]/', '', $uciId);
                $apiResults = $scfService->lookupByUciIds([$uciClean], $year);
                $licenseData = reset($apiResults);

                if ($licenseData) {
                    $scfService->updateRiderLicense($riderId, $licenseData, $year);
                    $scfService->cacheLicense($licenseData, $year);
                }

                $rider = $db->getRow("SELECT firstname, lastname FROM riders WHERE id = ?", [$riderId]);
                $message = "UCI ID {$uciId} kopplat till \"{$rider['firstname']} {$rider['lastname']}\"!";
                $messageType = 'success';
            }
        }
    }
}

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.search-forms {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--space-lg);
    margin-bottom: var(--space-lg);
}

.result-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-md);
}

.result-card.has-duplicate {
    border-color: var(--color-warning);
    background: rgba(251, 191, 36, 0.05);
}

.result-card.is-new {
    border-color: var(--color-success);
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--space-sm);
}

.result-name {
    font-size: var(--text-lg);
    font-weight: 600;
}

.result-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
    font-size: var(--text-sm);
}

.result-detail {
    display: flex;
    flex-direction: column;
}

.result-detail-label {
    color: var(--color-text-muted);
    font-size: var(--text-xs);
    text-transform: uppercase;
}

.result-detail-value {
    font-weight: 500;
}

.duplicate-warning {
    background: rgba(251, 191, 36, 0.1);
    border: 1px solid var(--color-warning);
    border-radius: var(--radius-sm);
    padding: var(--space-sm);
    margin-bottom: var(--space-md);
    font-size: var(--text-sm);
}

.result-actions {
    display: flex;
    gap: var(--space-sm);
    flex-wrap: wrap;
}
</style>

<?php if (!$apiKey): ?>
<div class="alert alert-danger">
    API-nyckel saknas. Lagg till <code>SCF_API_KEY=din_nyckel</code> i <code>.env</code>-filen.
</div>
<?php else: ?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?>">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Search Forms -->
<div class="search-forms">
    <!-- Search by Name -->
    <div class="card">
        <div class="card-header">
            <h3>Sok pa namn</h3>
        </div>
        <div class="card-body">
            <form method="post">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="search">

                <div class="form-group">
                    <label class="form-label">Fornamn</label>
                    <input type="text" name="firstname" class="form-input" value="<?= htmlspecialchars($_POST['firstname'] ?? '') ?>">
                </div>

                <div class="form-group">
                    <label class="form-label">Efternamn</label>
                    <input type="text" name="lastname" class="form-input" value="<?= htmlspecialchars($_POST['lastname'] ?? '') ?>">
                </div>

                <div class="form-group">
                    <label class="form-label">Kon</label>
                    <select name="gender" class="form-select">
                        <option value="M" <?= ($_POST['gender'] ?? 'M') === 'M' ? 'selected' : '' ?>>Man</option>
                        <option value="F" <?= ($_POST['gender'] ?? '') === 'F' ? 'selected' : '' ?>>Kvinna</option>
                    </select>
                </div>

                <button type="submit" class="btn btn-primary">
                    <i data-lucide="search"></i> Sok i SCF
                </button>
            </form>
        </div>
    </div>

    <!-- Search by UCI ID -->
    <div class="card">
        <div class="card-header">
            <h3>Sok pa UCI ID</h3>
        </div>
        <div class="card-body">
            <form method="post">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="search_uci">

                <div class="form-group">
                    <label class="form-label">UCI ID</label>
                    <input type="text" name="uci_id" class="form-input" placeholder="t.ex. 100 107 308 05"
                           value="<?= htmlspecialchars($_POST['uci_id'] ?? '') ?>">
                    <small class="text-secondary">Mellanslag och bindestreck ignoreras</small>
                </div>

                <button type="submit" class="btn btn-primary">
                    <i data-lucide="search"></i> Sok i SCF
                </button>
            </form>
        </div>
    </div>
</div>

<!-- Search Results -->
<?php if (!empty($searchResults)): ?>
<div class="card">
    <div class="card-header">
        <h3>Sokresultat (<?= count($searchResults) ?>)</h3>
    </div>
    <div class="card-body">
        <?php foreach ($searchResults as $result): ?>
        <?php
        $scf = $result['scf'];
        $existingByUci = $result['existing_by_uci'];
        $existingByName = $result['existing_by_name'];
        $hasDuplicate = $existingByUci || $existingByName;
        ?>
        <div class="result-card <?= $hasDuplicate ? 'has-duplicate' : 'is-new' ?>">
            <div class="result-header">
                <div>
                    <div class="result-name"><?= htmlspecialchars($scf['firstname'] . ' ' . $scf['lastname']) ?></div>
                    <?php if (!empty($scf['uci_id'])): ?>
                    <code><?= htmlspecialchars($scf['uci_id']) ?></code>
                    <?php endif; ?>
                </div>
                <?php if ($hasDuplicate): ?>
                    <span class="badge badge-warning">Potentiell dubblett</span>
                <?php else: ?>
                    <span class="badge badge-success">Ny</span>
                <?php endif; ?>
            </div>

            <div class="result-details">
                <?php if (!empty($scf['gender'])): ?>
                <div class="result-detail">
                    <span class="result-detail-label">Kon</span>
                    <span class="result-detail-value"><?= $scf['gender'] === 'M' ? 'Man' : 'Kvinna' ?></span>
                </div>
                <?php endif; ?>

                <?php if (!empty($scf['birth_year'])): ?>
                <div class="result-detail">
                    <span class="result-detail-label">Fodelsear</span>
                    <span class="result-detail-value"><?= $scf['birth_year'] ?></span>
                </div>
                <?php endif; ?>

                <?php if (!empty($scf['nationality'])): ?>
                <div class="result-detail">
                    <span class="result-detail-label">Nationalitet</span>
                    <span class="result-detail-value"><?= htmlspecialchars($scf['nationality']) ?></span>
                </div>
                <?php endif; ?>

                <?php if (!empty($scf['club_name'])): ?>
                <div class="result-detail">
                    <span class="result-detail-label">Klubb</span>
                    <span class="result-detail-value"><?= htmlspecialchars($scf['club_name']) ?></span>
                </div>
                <?php endif; ?>

                <?php if (!empty($scf['license_type'])): ?>
                <div class="result-detail">
                    <span class="result-detail-label">Licenstyp</span>
                    <span class="result-detail-value"><?= htmlspecialchars($scf['license_type']) ?></span>
                </div>
                <?php endif; ?>

                <?php if (!empty($scf['license_category'])): ?>
                <div class="result-detail">
                    <span class="result-detail-label">Klass</span>
                    <span class="result-detail-value"><?= htmlspecialchars($scf['license_category']) ?></span>
                </div>
                <?php endif; ?>

                <?php if (!empty($scf['discipline'])): ?>
                <div class="result-detail">
                    <span class="result-detail-label">Disciplin</span>
                    <span class="result-detail-value"><?= htmlspecialchars($scf['discipline']) ?></span>
                </div>
                <?php endif; ?>
            </div>

            <?php if ($existingByUci): ?>
            <div class="duplicate-warning">
                <strong>Finns redan med samma UCI ID:</strong>
                <a href="/rider/<?= $existingByUci['id'] ?>" class="color-accent" target="_blank">
                    <?= htmlspecialchars($existingByUci['firstname'] . ' ' . $existingByUci['lastname']) ?>
                </a>
                (ID: <?= $existingByUci['id'] ?>)
            </div>
            <?php elseif ($existingByName): ?>
            <div class="duplicate-warning">
                <strong>Potentiell dubblett (samma namn):</strong>
                <a href="/rider/<?= $existingByName['id'] ?>" class="color-accent" target="_blank">
                    <?= htmlspecialchars($existingByName['firstname'] . ' ' . $existingByName['lastname']) ?>
                </a>
                (ID: <?= $existingByName['id'] ?>, Licens: <?= $existingByName['license_number'] ?: 'Saknas' ?>)
                <br><small>Kontrollera om detta ar samma person innan du importerar.</small>
            </div>
            <?php endif; ?>

            <div class="result-actions">
                <?php if (!$existingByUci): ?>
                    <?php if ($existingByName && !empty($scf['uci_id'])): ?>
                    <!-- Option to link to existing -->
                    <form method="post" style="display: inline;">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="link_existing">
                        <input type="hidden" name="rider_id" value="<?= $existingByName['id'] ?>">
                        <input type="hidden" name="link_uci_id" value="<?= htmlspecialchars($scf['uci_id']) ?>">
                        <button type="submit" class="btn btn-warning" onclick="return confirm('Koppla UCI ID till befintlig cyklist?')">
                            <i data-lucide="link"></i> Koppla till befintlig
                        </button>
                    </form>
                    <?php endif; ?>

                    <!-- Import as new -->
                    <form method="post" style="display: inline;">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="import">
                        <input type="hidden" name="import_uci_id" value="<?= htmlspecialchars($scf['uci_id'] ?? '') ?>">
                        <input type="hidden" name="import_firstname" value="<?= htmlspecialchars($scf['firstname'] ?? '') ?>">
                        <input type="hidden" name="import_lastname" value="<?= htmlspecialchars($scf['lastname'] ?? '') ?>">
                        <input type="hidden" name="import_gender" value="<?= htmlspecialchars($scf['gender'] ?? '') ?>">
                        <input type="hidden" name="import_birth_year" value="<?= htmlspecialchars($scf['birth_year'] ?? '') ?>">
                        <input type="hidden" name="import_nationality" value="<?= htmlspecialchars($scf['nationality'] ?? '') ?>">
                        <input type="hidden" name="import_club" value="<?= htmlspecialchars($scf['club_name'] ?? '') ?>">
                        <button type="submit" class="btn btn-primary" onclick="return confirm('<?= $existingByName ? 'Det finns en potentiell dubblett. ' : '' ?>Skapa ny cyklist?')">
                            <i data-lucide="user-plus"></i> Importera som ny
                        </button>
                    </form>
                <?php else: ?>
                    <a href="/rider/<?= $existingByUci['id'] ?>" class="btn btn-secondary" target="_blank">
                        <i data-lucide="external-link"></i> Visa befintlig profil
                    </a>
                <?php endif; ?>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h3>Information</h3>
    </div>
    <div class="card-body">
        <p>Detta verktyg later dig soka i SCF License Portal och importera cyklister till TheHUB.</p>
        <ul>
            <li><strong>Dubblettdetektering:</strong> Verktyget varnar om det finns potentiella dubbletter baserat pa UCI ID eller namn.</li>
            <li><strong>Koppla till befintlig:</strong> Om en cyklist redan finns utan UCI ID kan du koppla SCF-profilen till den befintliga.</li>
            <li><strong>Automatisk synk:</strong> Vid import hamtas all licensinformation automatiskt fran SCF.</li>
        </ul>
    </div>
</div>

<?php endif; ?>

<script>
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
