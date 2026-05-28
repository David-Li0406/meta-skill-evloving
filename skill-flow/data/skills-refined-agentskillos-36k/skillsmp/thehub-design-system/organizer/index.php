<?php
/**
 * Organizer App - Login
 * Inloggningssida för arrangörer
 */

require_once __DIR__ . '/config.php';

// Om redan inloggad, gå till dashboard
if (isLoggedIn() && hasRole('promotor')) {
    header('Location: dashboard.php');
    exit;
}

$error = '';

// Hantera inloggning
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';

    if (empty($username) || empty($password)) {
        $error = 'Fyll i både användarnamn och lösenord.';
    } elseif (isLoginRateLimited($username)) {
        $error = 'För många inloggningsförsök. Försök igen om 15 minuter.';
    } elseif (login($username, $password)) {
        // Kontrollera att användaren är arrangör eller högre
        if (hasRole('promotor')) {
            header('Location: dashboard.php');
            exit;
        } else {
            logout();
            $error = 'Du har inte behörighet att använda platsregistrering.';
        }
    } else {
        $error = 'Felaktigt användarnamn eller lösenord.';
    }
}

$pageTitle = 'Logga in';
?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title><?= $pageTitle ?> - <?= ORGANIZER_APP_NAME ?></title>

    <?php
    // Load favicon from branding
    $faviconUrl = '/assets/favicon.svg';
    $brandingFile = __DIR__ . '/../uploads/branding.json';
    if (file_exists($brandingFile)) {
        $brandingData = json_decode(file_get_contents($brandingFile), true);
        if (!empty($brandingData['logos']['favicon'])) {
            $faviconUrl = $brandingData['logos']['favicon'];
        }
    }
    $faviconExt = strtolower(pathinfo($faviconUrl, PATHINFO_EXTENSION));
    $faviconMime = match($faviconExt) {
        'svg' => 'image/svg+xml', 'ico' => 'image/x-icon', 'png' => 'image/png',
        'jpg', 'jpeg' => 'image/jpeg', 'webp' => 'image/webp', default => 'image/png'
    };
    ?>
    <link rel="icon" type="<?= $faviconMime ?>" href="<?= SITE_URL . htmlspecialchars($faviconUrl) ?>">
    <link rel="stylesheet" href="<?= SITE_URL ?>/assets/css/base.css">
    <link rel="stylesheet" href="<?= ORGANIZER_BASE_URL ?>/assets/css/organizer.css">
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
</head>
<body>
<div class="org-login">
    <div class="org-login__box">
        <div class="org-login__logo">
            <img src="<?= SITE_URL ?>/assets/images/logo.png" alt="<?= APP_NAME ?>" onerror="this.style.display='none'">
        </div>

        <h1 class="org-login__title"><?= ORGANIZER_APP_NAME ?></h1>
        <p class="org-login__subtitle">Logga in för att hantera anmälningar</p>

        <?php if ($error): ?>
            <div class="org-alert org-alert--error">
                <?= htmlspecialchars($error) ?>
            </div>
        <?php endif; ?>

        <form method="POST" autocomplete="off">
            <div class="org-form-group">
                <label class="org-label" for="username">Användarnamn</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    class="org-input org-input--large"
                    placeholder="Ditt användarnamn"
                    value="<?= htmlspecialchars($_POST['username'] ?? '') ?>"
                    autocomplete="username"
                    autocapitalize="none"
                    required
                    autofocus
                >
            </div>

            <div class="org-form-group">
                <label class="org-label" for="password">Lösenord</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    class="org-input org-input--large"
                    placeholder="Ditt lösenord"
                    autocomplete="current-password"
                    required
                >
            </div>

            <button type="submit" class="org-btn org-btn--primary org-btn--large org-btn--block">
                <i data-lucide="log-in"></i>
                Logga in
            </button>
        </form>

        <p class="org-text-center org-text-muted org-mt-lg" style="font-size: 14px;">
            Endast för arrangörer med behörighet
        </p>
    </div>
</div>

<script>
    lucide.createIcons();
</script>
</body>
</html>
