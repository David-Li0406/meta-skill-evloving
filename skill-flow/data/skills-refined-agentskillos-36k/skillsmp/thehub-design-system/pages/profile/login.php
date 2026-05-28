<?php
/**
 * TheHUB V1.0 - Login Page
 * Connects to WordPress/WooCommerce authentication
 */

// Already logged in?
if (hub_is_logged_in()) {
    header('Location: /profile');
    exit;
}

$redirect = $_GET['redirect'] ?? '/profile';
$error = $_GET['error'] ?? '';
?>

<div class="login-page">
    <div class="login-container">
        <div class="login-header">
            <h1>Logga in</h1>
            <p>Logga in för att hantera din profil, anmälningar och resultat.</p>
        </div>

        <?php if ($error): ?>
            <div class="alert alert-error">
                <?php
                $errors = [
                    'invalid' => 'Felaktigt användarnamn eller lösenord.',
                    'session' => 'Din session har gått ut. Logga in igen.',
                ];
                echo htmlspecialchars($errors[$error] ?? 'Ett fel uppstod.');
                ?>
            </div>
        <?php endif; ?>

        <form class="login-form" action="/rider-login.php" method="POST">
            <input type="hidden" name="redirect" value="<?= htmlspecialchars($redirect) ?>">

            <div class="form-group">
                <label for="email">E-postadress</label>
                <input type="email" id="email" name="email" required autocomplete="email" autofocus>
            </div>

            <div class="form-group">
                <label for="password">Lösenord</label>
                <input type="password" id="password" name="password" required autocomplete="current-password">
            </div>

            <button type="submit" class="btn btn--primary btn-lg btn-block">Logga in</button>

            <div class="login-links">
                <a href="/rider-forgot-password.php">Glömt lösenord?</a>
            </div>
        </form>

        <div class="login-divider">
            <span>eller</span>
        </div>

        <div class="login-alternatives">
            <a href="<?= WC_CHECKOUT_URL ?>?action=login" class="btn btn-outline btn-block">
                Logga in via butiken
            </a>
        </div>

        <div class="login-register">
            <p>Ny användare? <a href="/rider-register.php">Skapa konto</a></p>
        </div>
    </div>
</div>


<!-- CSS loaded from /assets/css/pages/profile-login.css -->
