<?php
/**
 * ImgBB Avatar Upload Test Page
 *
 * Use this page to test the ImgBB integration independently.
 * Access: /test-avatar-upload.php
 *
 * DELETE THIS FILE IN PRODUCTION!
 */

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/includes/upload-avatar.php';
require_once __DIR__ . '/includes/get-avatar.php';

$testResult = null;
$uploadedUrl = null;

// Handle test upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['test_image'])) {
    $testResult = upload_avatar_to_imgbb($_FILES['test_image']);
    if ($testResult['success']) {
        $uploadedUrl = $testResult['url'];
    }
}

// Check API configuration
$apiConfigured = defined('IMGBB_API_KEY') && IMGBB_API_KEY !== 'YOUR_API_KEY_HERE';
?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImgBB Upload Test - TheHUB</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 40px 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #fff;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h1 {
            color: #171717;
            margin-bottom: 24px;
            font-size: 24px;
        }
        h2 {
            color: #323539;
            margin: 24px 0 16px;
            font-size: 18px;
        }
        .status-box {
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 24px;
        }
        .status-ok {
            background: rgba(97, 206, 112, 0.1);
            border: 1px solid #61CE70;
            color: #166534;
        }
        .status-error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid #ef4444;
            color: #991b1b;
        }
        .status-warning {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid #f59e0b;
            color: #92400e;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #323539;
        }
        input[type="file"] {
            display: block;
            width: 100%;
            padding: 12px;
            border: 2px dashed #e5e7eb;
            border-radius: 8px;
            background: #f9fafb;
            cursor: pointer;
        }
        input[type="file"]:hover {
            border-color: #61CE70;
        }
        button {
            background: #61CE70;
            color: #fff;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: #4eb85d;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .result {
            margin-top: 24px;
            padding: 16px;
            background: #f9fafb;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }
        .result img {
            max-width: 200px;
            border-radius: 50%;
            margin: 16px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .result pre {
            background: #1f2937;
            color: #f9fafb;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 13px;
            margin-top: 16px;
        }
        .info-list {
            list-style: none;
        }
        .info-list li {
            padding: 8px 0;
            border-bottom: 1px solid #e5e7eb;
        }
        .info-list li:last-child {
            border-bottom: none;
        }
        .info-list strong {
            color: #171717;
        }
        a {
            color: #61CE70;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .warning {
            background: #fef3c7;
            color: #92400e;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 24px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ImgBB Avatar Upload Test</h1>

        <div class="warning">
            <strong>OBS!</strong> Ta bort denna testfil i produktion.
        </div>

        <h2>Konfigurationsstatus</h2>

        <?php if ($apiConfigured): ?>
            <div class="status-box status-ok">
                <strong>API-nyckel konfigurerad</strong>
                <p>ImgBB API-nyckeln är inställd och redo att användas.</p>
            </div>
        <?php else: ?>
            <div class="status-box status-error">
                <strong>API-nyckel saknas</strong>
                <p>Konfigurera IMGBB_API_KEY i <code>/config/imgbb.php</code> eller som miljövariabel.</p>
                <p style="margin-top: 8px;">
                    <a href="https://api.imgbb.com/" target="_blank">Hämta gratis API-nyckel på api.imgbb.com</a>
                </p>
            </div>
        <?php endif; ?>

        <h2>Systeminformation</h2>
        <ul class="info-list">
            <li><strong>PHP Version:</strong> <?= phpversion() ?></li>
            <li><strong>cURL:</strong> <?= function_exists('curl_init') ? 'Tillgänglig' : 'Saknas' ?></li>
            <li><strong>Max Upload Size:</strong> <?= ini_get('upload_max_filesize') ?></li>
            <li><strong>Post Max Size:</strong> <?= ini_get('post_max_size') ?></li>
            <li><strong>Avatar Max Size:</strong> <?= defined('AVATAR_MAX_SIZE') ? (AVATAR_MAX_SIZE / 1024 / 1024) . 'MB' : '2MB (default)' ?></li>
        </ul>

        <h2>Testa uppladdning</h2>

        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label for="test_image">Välj en bild att ladda upp:</label>
                <input type="file" name="test_image" id="test_image" accept="image/jpeg,image/png,image/gif,image/webp" required>
            </div>
            <button type="submit" <?= !$apiConfigured ? 'disabled' : '' ?>>
                Ladda upp till ImgBB
            </button>
        </form>

        <?php if ($testResult !== null): ?>
            <div class="result">
                <h3>Resultat</h3>

                <?php if ($testResult['success']): ?>
                    <div class="status-box status-ok">
                        <strong>Uppladdning lyckades!</strong>
                    </div>

                    <?php if ($uploadedUrl): ?>
                        <p><strong>Bild-URL:</strong></p>
                        <p><a href="<?= htmlspecialchars($uploadedUrl) ?>" target="_blank"><?= htmlspecialchars($uploadedUrl) ?></a></p>

                        <p><strong>Förhandsvisning:</strong></p>
                        <img src="<?= htmlspecialchars($uploadedUrl) ?>" alt="Uppladdad bild">
                    <?php endif; ?>
                <?php else: ?>
                    <div class="status-box status-error">
                        <strong>Uppladdning misslyckades</strong>
                        <p><?= htmlspecialchars($testResult['error'] ?? 'Okänt fel') ?></p>
                    </div>
                <?php endif; ?>

                <p><strong>Fullständigt svar:</strong></p>
                <pre><?= htmlspecialchars(json_encode($testResult, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) ?></pre>
            </div>
        <?php endif; ?>

        <h2>Avatar Helper Test</h2>
        <?php
        // Test avatar helper with fake rider data
        $fakeRider = [
            'firstname' => 'Test',
            'lastname' => 'Användare',
            'avatar_url' => $uploadedUrl
        ];
        ?>
        <p><strong>get_rider_avatar() output:</strong></p>
        <pre><?= htmlspecialchars(get_rider_avatar($fakeRider, 200)) ?></pre>

        <p><strong>get_rider_initials() output:</strong></p>
        <pre><?= htmlspecialchars(get_rider_initials($fakeRider)) ?></pre>

        <p><strong>Rendered avatar (<?= $uploadedUrl ? 'med bild' : 'fallback' ?>):</strong></p>
        <div style="margin: 16px 0;">
            <?= render_rider_avatar($fakeRider, 100) ?>
        </div>

        <style><?= get_avatar_styles() ?></style>

        <p style="margin-top: 32px; color: #7a7a7a; font-size: 14px;">
            <a href="/">&larr; Tillbaka till TheHUB</a>
        </p>
    </div>
</body>
</html>
