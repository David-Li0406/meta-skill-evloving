<?php
/**
 * SCF API Test Tool
 *
 * Simple tool to test SCF License Portal API connection
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Get API key
$apiKey = env('SCF_API_KEY', '');

$page_title = 'SCF API Test';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'SCF API Test']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.test-result {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
}
.test-result.success { border-color: var(--color-success); }
.test-result.error { border-color: var(--color-error); }
.test-result h4 { margin: 0 0 var(--space-sm); }
.api-response {
    background: var(--color-bg-hover);
    padding: var(--space-md);
    border-radius: var(--radius-sm);
    font-family: monospace;
    font-size: var(--text-sm);
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 400px;
    overflow-y: auto;
}
</style>

<div class="card">
    <div class="card-header">
        <h3>API Konfiguration</h3>
    </div>
    <div class="card-body">
        <table class="table">
            <tr>
                <td><strong>API Nyckel</strong></td>
                <td>
                    <?php if ($apiKey): ?>
                        <span class="badge badge-success">Konfigurerad</span>
                        <code><?= substr($apiKey, 0, 8) ?>...<?= substr($apiKey, -4) ?></code>
                    <?php else: ?>
                        <span class="badge badge-danger">Saknas</span>
                        <br><small class="text-secondary">Lägg till SCF_API_KEY i .env-filen</small>
                    <?php endif; ?>
                </td>
            </tr>
            <tr>
                <td><strong>API Endpoint</strong></td>
                <td><code>https://licens.scf.se/api/1.0</code></td>
            </tr>
        </table>
    </div>
</div>

<?php if (!$apiKey): ?>
<div class="alert alert-danger">
    API-nyckel saknas. Lägg till <code>SCF_API_KEY=din_nyckel</code> i <code>.env</code>-filen.
</div>
<?php else: ?>

<?php
// Handle test requests
$testResult = null;
$testError = null;
$testResponse = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['test_type'])) {
    $csrfToken = $_POST['csrf_token'] ?? '';
    if (!verify_csrf_token($csrfToken)) {
        $testError = 'CSRF-validering misslyckades.';
    } else {
        $testType = $_POST['test_type'];

        // Build API URL
        $baseUrl = 'https://licens.scf.se/api/1.0';
        $url = '';
        $params = [];

        switch ($testType) {
            case 'single_uci':
                // Test with a specific UCI ID
                $uciId = trim($_POST['uci_id'] ?? '');
                if (empty($uciId)) {
                    $testError = 'Ange ett UCI ID att testa med.';
                } else {
                    // Remove spaces and formatting
                    $uciIdClean = preg_replace('/[^0-9]/', '', $uciId);
                    $url = $baseUrl . '/ucilicenselookup';
                    $params = [
                        'uciids' => $uciIdClean,
                        'year' => date('Y')
                    ];
                }
                break;

            case 'batch_uci':
                // Test batch lookup with first 5 riders
                $riders = $db->getAll("
                    SELECT license_number FROM riders
                    WHERE license_number IS NOT NULL
                    AND license_number != ''
                    AND license_number NOT LIKE 'SWE%'
                    LIMIT 5
                ");
                if (empty($riders)) {
                    $testError = 'Inga deltagare med UCI ID hittades.';
                } else {
                    $uciIds = [];
                    foreach ($riders as $r) {
                        $uciIds[] = preg_replace('/[^0-9]/', '', $r['license_number']);
                    }
                    $url = $baseUrl . '/ucilicenselookup';
                    $params = [
                        'uciids' => implode(',', $uciIds),
                        'year' => date('Y')
                    ];
                }
                break;

            case 'search_name':
                // Test name search
                $firstname = trim($_POST['firstname'] ?? '');
                $lastname = trim($_POST['lastname'] ?? '');
                $gender = trim($_POST['gender'] ?? 'M');
                $birthdate = trim($_POST['birthdate'] ?? '');
                if (empty($firstname) || empty($lastname)) {
                    $testError = 'Ange både förnamn och efternamn.';
                } else {
                    $url = $baseUrl . '/licenselookup';
                    $params = [
                        'firstname' => $firstname,
                        'lastname' => $lastname,
                        'gender' => $gender,
                        'year' => date('Y')
                    ];
                    if (!empty($birthdate)) {
                        $params['birthdate'] = $birthdate;
                    }
                }
                break;
        }

        if ($url && !$testError) {
            // Make API request
            $fullUrl = $url . '?' . http_build_query($params);

            $ch = curl_init();
            curl_setopt_array($ch, [
                CURLOPT_URL => $fullUrl,
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_TIMEOUT => 30,
                CURLOPT_HTTPHEADER => [
                    'Authorization: Bearer ' . $apiKey,
                    'Accept: application/json',
                    'Content-Type: application/json'
                ],
                CURLOPT_SSL_VERIFYPEER => true,
                CURLOPT_FOLLOWLOCATION => true
            ]);

            $response = curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $curlError = curl_error($ch);
            $curlInfo = curl_getinfo($ch);
            curl_close($ch);

            $testResult = [
                'url' => $fullUrl,
                'http_code' => $httpCode,
                'curl_error' => $curlError,
                'response_time' => round($curlInfo['total_time'] * 1000) . 'ms',
                'response_size' => strlen($response) . ' bytes'
            ];

            if ($curlError) {
                $testError = 'CURL Error: ' . $curlError;
            } else {
                $testResponse = $response;
                // Try to pretty-print JSON
                $decoded = json_decode($response, true);
                if ($decoded !== null) {
                    $testResponse = json_encode($decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
                }
            }
        }
    }
}
?>

<!-- Test: Single UCI ID -->
<div class="card">
    <div class="card-header">
        <h3>Test 1: Hämta licens med UCI ID</h3>
    </div>
    <div class="card-body">
        <form method="post">
            <?= csrf_field() ?>
            <input type="hidden" name="test_type" value="single_uci">
            <div class="form-group">
                <label class="form-label">UCI ID</label>
                <input type="text" name="uci_id" class="form-input" placeholder="t.ex. 100 107 308 05 eller 10010730805"
                       value="<?= htmlspecialchars($_POST['uci_id'] ?? '') ?>">
                <small class="text-secondary">Ange ett UCI ID för att testa API-anropet</small>
            </div>
            <button type="submit" class="btn btn-primary">Testa API</button>
        </form>

        <?php
        // Get sample UCI IDs from database
        $sampleUcis = $db->getAll("
            SELECT id, firstname, lastname, license_number FROM riders
            WHERE license_number IS NOT NULL
            AND license_number != ''
            AND license_number NOT LIKE 'SWE%'
            LIMIT 5
        ");
        if ($sampleUcis): ?>
        <div style="margin-top: var(--space-md);">
            <strong>Exempel från databasen:</strong>
            <ul style="margin-top: var(--space-xs);">
                <?php foreach ($sampleUcis as $r): ?>
                <li><code><?= htmlspecialchars($r['license_number']) ?></code> - <?= htmlspecialchars($r['firstname'] . ' ' . $r['lastname']) ?></li>
                <?php endforeach; ?>
            </ul>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Test: Batch UCI IDs -->
<div class="card">
    <div class="card-header">
        <h3>Test 2: Batch-sökning (5 första UCI IDs)</h3>
    </div>
    <div class="card-body">
        <form method="post">
            <?= csrf_field() ?>
            <input type="hidden" name="test_type" value="batch_uci">
            <p class="text-secondary">Testar batch-anrop med de första 5 UCI IDs från databasen.</p>
            <button type="submit" class="btn btn-primary">Testa Batch API</button>
        </form>
    </div>
</div>

<!-- Test: Name Search -->
<div class="card">
    <div class="card-header">
        <h3>Test 3: Sök på namn</h3>
    </div>
    <div class="card-body">
        <form method="post">
            <?= csrf_field() ?>
            <input type="hidden" name="test_type" value="search_name">
            <div style="display: grid; grid-template-columns: 1fr 1fr 100px; gap: var(--space-md);">
                <div class="form-group">
                    <label class="form-label">Förnamn</label>
                    <input type="text" name="firstname" class="form-input" placeholder="t.ex. Erik"
                           value="<?= htmlspecialchars($_POST['firstname'] ?? '') ?>">
                </div>
                <div class="form-group">
                    <label class="form-label">Efternamn</label>
                    <input type="text" name="lastname" class="form-input" placeholder="t.ex. Svensson"
                           value="<?= htmlspecialchars($_POST['lastname'] ?? '') ?>">
                </div>
                <div class="form-group">
                    <label class="form-label">Kön</label>
                    <select name="gender" class="form-select">
                        <option value="M" <?= ($_POST['gender'] ?? 'M') === 'M' ? 'selected' : '' ?>>Man</option>
                        <option value="F" <?= ($_POST['gender'] ?? '') === 'F' ? 'selected' : '' ?>>Kvinna</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Födelsedatum (valfritt)</label>
                <input type="date" name="birthdate" class="form-input" style="max-width: 200px;"
                       value="<?= htmlspecialchars($_POST['birthdate'] ?? '') ?>">
                <small class="text-secondary">Rekommenderas för bättre träffsäkerhet</small>
            </div>
            <button type="submit" class="btn btn-primary">Sök i SCF</button>
        </form>
    </div>
</div>

<!-- Test Results -->
<?php if ($testError): ?>
<div class="test-result error">
    <h4 class="text-danger">Fel</h4>
    <p><?= htmlspecialchars($testError) ?></p>
</div>
<?php endif; ?>

<?php if ($testResult): ?>
<div class="test-result <?= ($testResult['http_code'] == 200) ? 'success' : 'error' ?>">
    <h4>Resultat</h4>
    <table class="table" style="margin-bottom: var(--space-md);">
        <tr><td><strong>URL</strong></td><td><code style="word-break: break-all;"><?= htmlspecialchars($testResult['url']) ?></code></td></tr>
        <tr><td><strong>HTTP Status</strong></td><td>
            <span class="badge <?= $testResult['http_code'] == 200 ? 'badge-success' : 'badge-danger' ?>">
                <?= $testResult['http_code'] ?>
            </span>
        </td></tr>
        <tr><td><strong>Svarstid</strong></td><td><?= $testResult['response_time'] ?></td></tr>
        <tr><td><strong>Storlek</strong></td><td><?= $testResult['response_size'] ?></td></tr>
    </table>

    <h4>API Svar</h4>
    <div class="api-response"><?= htmlspecialchars($testResponse ?? 'Inget svar') ?></div>
</div>
<?php endif; ?>

<?php endif; ?>

<script>
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
