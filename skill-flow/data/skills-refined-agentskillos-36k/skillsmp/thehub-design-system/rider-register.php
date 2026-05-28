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

// Handle registration
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $email = trim($_POST['email'] ?? '');
 $password = $_POST['password'] ?? '';
 $confirmPassword = $_POST['confirm_password'] ?? '';

 if (empty($email) || empty($password) || empty($confirmPassword)) {
 $message = 'Fyll i alla fält';
 $messageType = 'error';
 } elseif ($password !== $confirmPassword) {
 $message = 'Lösenorden matchar inte';
 $messageType = 'error';
 } elseif (strlen($password) < 8) {
 $message = 'Lösenordet måste vara minst 8 tecken';
 $messageType = 'error';
 } else {
 $result = rider_register($email, $password);

 if ($result['success']) {
  // Redirect to profile after successful registration
  header('Location: /rider-profile.php?welcome=1');
  exit;
 } else {
  $message = $result['message'];
  $messageType = 'error';
 }
 }
}

$pageTitle = 'Skapa konto';
$pageType = 'public';
include __DIR__ . '/includes/layout-header.php';
?>

<main class="main-content">
 <div class="container gs-form-container">
 <div class="card">
  <div class="card-header text-center">
  <h1 class="text-primary">
   <i data-lucide="user-plus"></i>
   Skapa deltagarkonto
  </h1>
  <p class="text-secondary mt-sm">
   Använd din registrerade e-postadress för att skapa ett konto
  </p>
  </div>

  <div class="card-body">
  <?php if ($message): ?>
   <div class="alert alert-<?= h($messageType) ?> mb-lg">
   <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
   <?= h($message) ?>
   </div>
  <?php endif; ?>

  <div class="alert alert--info mb-lg">
   <i data-lucide="info"></i>
   <strong>Obs!</strong> Du måste redan vara registrerad som deltagare med en e-postadress.
   Kontakta administratören om din e-post inte finns i systemet.
  </div>

  <form method="POST">
   <?= csrf_field() ?>

   <div class="form-group">
   <label for="email" class="label">
    <i data-lucide="mail"></i>
    E-post (redan registrerad)
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
   <small class="text-sm text-secondary">
    Samma e-post som användes vid din registrering
   </small>
   </div>

   <div class="form-group">
   <label for="password" class="label">
    <i data-lucide="lock"></i>
    Välj lösenord
   </label>
   <input
    type="password"
    id="password"
    name="password"
    class="input"
    required
    minlength="8"
    placeholder="Minst 8 tecken"
   >
   </div>

   <div class="form-group">
   <label for="confirm_password" class="label">
    <i data-lucide="lock"></i>
    Bekräfta lösenord
   </label>
   <input
    type="password"
    id="confirm_password"
    name="confirm_password"
    class="input"
    required
    minlength="8"
    placeholder="Upprepa lösenordet"
   >
   </div>

   <button type="submit" class="btn btn--primary btn-lg w-full mb-md">
   <i data-lucide="user-plus"></i>
   Skapa konto
   </button>
  </form>

  <div class="text-center mt-lg section-divider">
   <p class="text-sm text-secondary mb-sm">
   Har du redan ett konto?
   </p>
   <a href="/rider-login.php" class="btn btn--secondary btn--sm">
   <i data-lucide="log-in"></i>
   Logga in
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
