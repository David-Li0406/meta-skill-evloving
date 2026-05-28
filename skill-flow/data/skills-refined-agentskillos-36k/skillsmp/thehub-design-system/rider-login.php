<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/includes/rider-auth.php';

// If already logged in, redirect to profile
if (is_rider_logged_in()) {
 header('Location: /rider-profile.php');
 exit;
}

$message = '';
$messageType = 'info';

// Handle login
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login'])) {
 checkCsrf();

 $email = trim($_POST['email'] ?? '');
 $password = $_POST['password'] ?? '';

 if (empty($email) || empty($password)) {
 $message = 'Fyll i både e-post och lösenord';
 $messageType = 'error';
 } else {
 $rememberMe = isset($_POST['remember_me']) && $_POST['remember_me'] == '1';
 $result = rider_login($email, $password, $rememberMe);

 if ($result['success']) {
  // Redirect to profile or original page
  $redirect = $_SESSION['redirect_after_login'] ?? '/rider-profile.php';
  unset($_SESSION['redirect_after_login']);
  header('Location: ' . $redirect);
  exit;
 } else {
  $message = $result['message'];
  $messageType = 'error';
 }
 }
}

$pageTitle = 'Logga in';
$pageType = 'public';
include __DIR__ . '/includes/layout-header.php';
?>

<main class="main-content">
 <div class="container gs-form-container">
 <div class="card">
  <div class="card-header text-center">
  <h1 class="text-primary">
   <i data-lucide="log-in"></i>
   Deltagare - Logga in
  </h1>
  <p class="text-secondary mt-sm">
   Logga in för att se din profil och anmäla dig till tävlingar
  </p>
  </div>

  <div class="card-body">
  <?php if ($message): ?>
   <div class="alert alert-<?= h($messageType) ?> mb-lg">
   <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
   <?= h($message) ?>
   </div>
  <?php endif; ?>

  <form method="POST">
   <?= csrf_field() ?>

   <div class="form-group">
   <label for="email" class="label">
    <i data-lucide="mail"></i>
    E-post
   </label>
   <input
    type="email"
    id="email"
    name="email"
    class="input"
    required
    value="<?= h($_POST['email'] ?? '') ?>"
    placeholder="din@email.com"
   >
   </div>

   <div class="form-group">
   <label for="password" class="label">
    <i data-lucide="lock"></i>
    Lösenord
   </label>
   <input
    type="password"
    id="password"
    name="password"
    class="input"
    required
    placeholder="Ditt lösenord"
   >
   </div>

   <div class="form-group">
    <label class="flex items-center gap-sm cursor-pointer">
     <input type="checkbox" name="remember_me" value="1" class="form-checkbox">
     <span class="text-sm">Kom ihåg mig i 30 dagar</span>
    </label>
   </div>

   <button type="submit" name="login" class="btn btn--primary btn-lg w-full mb-md">
   <i data-lucide="log-in"></i>
   Logga in
   </button>
  </form>

  <div class="text-center mt-lg section-divider">
   <p class="text-sm text-secondary mb-sm">
   Har du inget konto?
   </p>
   <a href="/rider-register.php" class="btn btn--secondary btn--sm">
   <i data-lucide="user-plus"></i>
   Skapa konto
   </a>
   <span class="gs-mx-sm text-secondary">|</span>
   <a href="/rider-reset-password.php" class="btn btn--secondary btn--sm">
   <i data-lucide="key"></i>
   Glömt lösenord?
   </a>
  </div>
  </div>
 </div>
 </div>
</main>

<script src="https://unpkg.com/lucide@latest"></script>
<script>
 lucide.createIcons();
</script>

<?php include __DIR__ . '/includes/layout-footer.php'; ?>
