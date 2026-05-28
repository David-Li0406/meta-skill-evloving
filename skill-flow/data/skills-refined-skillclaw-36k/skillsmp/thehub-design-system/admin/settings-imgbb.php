<?php
/**
 * ImgBB Settings - Admin Tool
 *
 * Configure ImgBB API key and test the connection
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_admin();

$pageTitle = 'ImgBB Inställningar';
$message = '';
$error = '';

// Path to imgbb config file
$configPath = __DIR__ . '/../config/imgbb.php';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'save_api_key') {
        $apiKey = trim($_POST['api_key'] ?? '');

        if (empty($apiKey)) {
            $error = 'API-nyckeln får inte vara tom.';
        } else {
            // Create/update the config file
            $configContent = '<?php
/**
 * ImgBB Configuration
 *
 * API key for uploading profile images to ImgBB
 * Get your free API key at: https://api.imgbb.com/
 *
 * Last updated: ' . date('Y-m-d H:i:s') . '
 */

// ImgBB API Key
if (!defined(\'IMGBB_API_KEY\')) {
    define(\'IMGBB_API_KEY\', \'' . addslashes($apiKey) . '\');
}

// ImgBB API endpoint
if (!defined(\'IMGBB_API_URL\')) {
    define(\'IMGBB_API_URL\', \'https://api.imgbb.com/1/upload\');
}

// Upload settings
if (!defined(\'AVATAR_MAX_SIZE\')) {
    define(\'AVATAR_MAX_SIZE\', 2 * 1024 * 1024); // 2MB max
}

if (!defined(\'AVATAR_ALLOWED_TYPES\')) {
    define(\'AVATAR_ALLOWED_TYPES\', [\'image/jpeg\', \'image/png\', \'image/gif\', \'image/webp\']);
}
';

            // Ensure config directory exists
            $configDir = dirname($configPath);
            if (!is_dir($configDir)) {
                mkdir($configDir, 0755, true);
            }

            // Write the config file
            if (file_put_contents($configPath, $configContent)) {
                $message = 'API-nyckeln har sparats!';
            } else {
                $error = 'Kunde inte spara konfigurationsfilen. Kontrollera filrättigheter.';
            }
        }
    }

    if ($action === 'test_api') {
        // Load the config
        if (file_exists($configPath)) {
            require_once $configPath;
        }

        if (!defined('IMGBB_API_KEY') || IMGBB_API_KEY === 'YOUR_API_KEY_HERE') {
            $error = 'Ingen API-nyckel konfigurerad. Spara en API-nyckel först.';
        } else {
            // Test the API with a simple request
            $testImage = base64_encode(file_get_contents(__DIR__ . '/../assets/favicon.svg') ?: 'test');

            $ch = curl_init();
            curl_setopt_array($ch, [
                CURLOPT_URL => 'https://api.imgbb.com/1/upload',
                CURLOPT_POST => true,
                CURLOPT_POSTFIELDS => [
                    'key' => IMGBB_API_KEY,
                    'image' => $testImage,
                    'name' => 'test_' . time()
                ],
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_TIMEOUT => 15
            ]);

            $response = curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $curlError = curl_error($ch);
            curl_close($ch);

            if ($curlError) {
                $error = 'Anslutningsfel: ' . $curlError;
            } else {
                $result = json_decode($response, true);
                if ($httpCode === 200 && isset($result['success']) && $result['success']) {
                    $message = 'API-anslutningen fungerar! Testbild uppladdad.';
                } else {
                    $errorMsg = $result['error']['message'] ?? 'Okänt fel';
                    $error = 'API-test misslyckades: ' . $errorMsg;
                }
            }
        }
    }
}

// Get current API key (masked)
$currentApiKey = '';
$apiKeyConfigured = false;
if (file_exists($configPath)) {
    require_once $configPath;
    if (defined('IMGBB_API_KEY') && IMGBB_API_KEY !== 'YOUR_API_KEY_HERE') {
        $currentApiKey = IMGBB_API_KEY;
        $apiKeyConfigured = true;
    }
}

// Mask the API key for display
$maskedApiKey = $apiKeyConfigured
    ? substr($currentApiKey, 0, 8) . str_repeat('*', max(0, strlen($currentApiKey) - 12)) . substr($currentApiKey, -4)
    : '';

include __DIR__ . '/../includes/admin-header.php';
?>

<div class="admin-content">
    <div class="page-header">
        <h1><i data-lucide="image"></i> <?= $pageTitle ?></h1>
        <p class="text-secondary">Konfigurera ImgBB för profilbildsuppladdning</p>
    </div>

    <?php if ($message): ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            <?= htmlspecialchars($message) ?>
        </div>
    <?php endif; ?>

    <?php if ($error): ?>
        <div class="alert alert-danger">
            <i data-lucide="alert-circle"></i>
            <?= htmlspecialchars($error) ?>
        </div>
    <?php endif; ?>

    <div class="card">
        <div class="card-header">
            <h3>Status</h3>
        </div>
        <div class="card-body">
            <table class="table">
                <tr>
                    <td><strong>API-nyckel</strong></td>
                    <td>
                        <?php if ($apiKeyConfigured): ?>
                            <span class="badge badge-success">Konfigurerad</span>
                            <code style="margin-left: 8px;"><?= htmlspecialchars($maskedApiKey) ?></code>
                        <?php else: ?>
                            <span class="badge badge-danger">Ej konfigurerad</span>
                        <?php endif; ?>
                    </td>
                </tr>
                <tr>
                    <td><strong>Konfigurationsfil</strong></td>
                    <td>
                        <?php if (file_exists($configPath)): ?>
                            <span class="badge badge-success">Finns</span>
                            <code style="margin-left: 8px;">/config/imgbb.php</code>
                        <?php else: ?>
                            <span class="badge badge-warning">Saknas</span>
                        <?php endif; ?>
                    </td>
                </tr>
                <tr>
                    <td><strong>cURL</strong></td>
                    <td>
                        <?php if (function_exists('curl_init')): ?>
                            <span class="badge badge-success">Tillgänglig</span>
                        <?php else: ?>
                            <span class="badge badge-danger">Saknas</span>
                        <?php endif; ?>
                    </td>
                </tr>
            </table>

            <?php if ($apiKeyConfigured): ?>
                <form method="POST" style="margin-top: 16px;">
                    <input type="hidden" name="action" value="test_api">
                    <button type="submit" class="btn btn-secondary">
                        <i data-lucide="zap"></i> Testa API-anslutning
                    </button>
                </form>
            <?php endif; ?>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h3>API-nyckel</h3>
        </div>
        <div class="card-body">
            <form method="POST">
                <input type="hidden" name="action" value="save_api_key">

                <div class="form-group">
                    <label for="api_key">ImgBB API-nyckel</label>
                    <input type="text"
                           id="api_key"
                           name="api_key"
                           class="form-input"
                           placeholder="Klistra in din API-nyckel här"
                           value="<?= $apiKeyConfigured ? htmlspecialchars($currentApiKey) : '' ?>">
                    <p class="form-help">
                        Hämta din gratis API-nyckel på
                        <a href="https://api.imgbb.com/" target="_blank" rel="noopener">api.imgbb.com</a>
                    </p>
                </div>

                <button type="submit" class="btn btn-primary">
                    <i data-lucide="save"></i> Spara API-nyckel
                </button>
            </form>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h3>Instruktioner</h3>
        </div>
        <div class="card-body">
            <ol style="line-height: 2; padding-left: 20px;">
                <li>Gå till <a href="https://imgbb.com/" target="_blank" rel="noopener">imgbb.com</a> och skapa ett gratis konto</li>
                <li>Gå till <a href="https://api.imgbb.com/" target="_blank" rel="noopener">api.imgbb.com</a></li>
                <li>Klicka på <strong>"Get API key"</strong></li>
                <li>Kopiera API-nyckeln och klistra in den ovan</li>
                <li>Klicka <strong>"Spara API-nyckel"</strong></li>
                <li>Klicka <strong>"Testa API-anslutning"</strong> för att verifiera</li>
            </ol>

            <div class="alert alert-info" style="margin-top: 16px;">
                <i data-lucide="info"></i>
                <strong>Bra att veta:</strong> ImgBB är gratis och har inga begränsningar på antal uppladdningar.
                Bilder lagras permanent om du inte raderar dem manuellt.
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h3>Verktyg</h3>
        </div>
        <div class="card-body">
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <a href="/admin/migrations/add_avatar_url.php" class="btn btn-secondary">
                    <i data-lucide="database"></i> Kör databasmigrering
                </a>
                <a href="/test-avatar-upload.php" class="btn btn-secondary" target="_blank">
                    <i data-lucide="upload"></i> Testa uppladdning
                </a>
                <a href="/profile/edit" class="btn btn-secondary" target="_blank">
                    <i data-lucide="user"></i> Redigera profil
                </a>
            </div>
        </div>
    </div>
</div>

<?php include __DIR__ . '/../includes/admin-footer.php'; ?>
