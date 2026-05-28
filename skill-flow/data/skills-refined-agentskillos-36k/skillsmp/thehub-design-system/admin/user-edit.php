<?php
/**
 * Admin User Edit/Create
 * Only accessible by super_admin
 */
require_once __DIR__ . '/../config.php';
require_admin();

// Only super_admin can access this page
if (!hasRole('super_admin')) {
 http_response_code(403);
 die('Access denied: Only super administrators can manage users.');
}

$db = getDB();

// Get user ID (null for new user)
$id = isset($_GET['id']) && is_numeric($_GET['id']) ? intval($_GET['id']) : null;
$isNew = $id === null;

// Fetch user if editing
$user = null;
if (!$isNew) {
 $user = $db->getRow("SELECT * FROM admin_users WHERE id = ?", [$id]);
 if (!$user) {
 header('Location: /admin/users.php');
 exit;
 }
}

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? 'save';

 if ($action === 'delete' && !$isNew) {
 // Prevent deleting yourself
 $currentAdmin = getCurrentAdmin();
 if ($currentAdmin['id'] == $id) {
  $message = 'Du kan inte ta bort din egen användare!';
  $messageType = 'error';
 } else {
  try {
  $db->delete('admin_users', 'id = ?', [$id]);
  header('Location: /admin/users.php?deleted=1');
  exit;
  } catch (Exception $e) {
  $message = 'Kunde inte ta bort användaren: ' . $e->getMessage();
  $messageType = 'error';
  }
 }
 } else {
 // Validate required fields
 $username = trim($_POST['username'] ?? '');
 $email = trim($_POST['email'] ?? '');
 $fullName = trim($_POST['full_name'] ?? '');
 $role = trim($_POST['role'] ?? 'rider');
 $active = isset($_POST['active']) ? 1 : 0;
 $password = $_POST['password'] ?? '';
 $passwordConfirm = $_POST['password_confirm'] ?? '';

 $errors = [];

 if (empty($username)) {
  $errors[] = 'Användarnamn är obligatoriskt';
 } elseif (!preg_match('/^[a-zA-Z0-9_]+$/', $username)) {
  $errors[] = 'Användarnamn får bara innehålla bokstäver, siffror och understreck';
 }

 if (empty($email)) {
  $errors[] = 'E-post är obligatoriskt';
 } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
  $errors[] = 'Ogiltig e-postadress';
 }

 // Check if username already exists (for new users or changed username)
 if ($username && ($isNew || $user['username'] !== $username)) {
  $existing = $db->getRow("SELECT id FROM admin_users WHERE username = ? AND id != ?", [$username, $id ?? 0]);
  if ($existing) {
  $errors[] = 'Användarnamnet är redan upptaget';
  }
 }

 // Check if email already exists
 if ($email && ($isNew || $user['email'] !== $email)) {
  $existing = $db->getRow("SELECT id FROM admin_users WHERE email = ? AND id != ?", [$email, $id ?? 0]);
  if ($existing) {
  $errors[] = 'E-postadressen är redan registrerad';
  }
 }

 // Password validation
 if ($isNew && empty($password)) {
  $errors[] = 'Lösenord är obligatoriskt för nya användare';
 }

 if ($password && $password !== $passwordConfirm) {
  $errors[] = 'Lösenorden matchar inte';
 }

 if ($password && strlen($password) < 8) {
  $errors[] = 'Lösenordet måste vara minst 8 tecken';
 }

 if (!empty($errors)) {
  $message = implode('<br>', $errors);
  $messageType = 'error';
 } else {
  // Prepare user data
  $userData = [
  'username' => $username,
  'email' => $email,
  'full_name' => $fullName,
  'role' => $role,
  'active' => $active,
  ];

  // Add password hash if provided
  if ($password) {
  $userData['password_hash'] = password_hash($password, PASSWORD_DEFAULT);
  }

  try {
  if ($isNew) {
   $newId = $db->insert('admin_users', $userData);
   header('Location: /admin/user-edit.php?id=' . $newId . '&created=1');
   exit;
  } else {
   $db->update('admin_users', $userData, 'id = ?', [$id]);
   $message = 'Användare uppdaterad!';
   $messageType = 'success';

   // Refresh user data
   $user = $db->getRow("SELECT * FROM admin_users WHERE id = ?", [$id]);
  }
  } catch (Exception $e) {
  $message = 'Ett fel uppstod: ' . $e->getMessage();
  $messageType = 'error';
  }
 }
 }
}

// Show created message
if (isset($_GET['created'])) {
 $message = 'Användare skapad!';
 $messageType = 'success';
}

// Page config for unified layout
$page_title = $isNew ? 'Skapa Användare' : 'Redigera Användare';
$breadcrumbs = [
    ['label' => 'System', 'url' => '/admin/users.php'],
    ['label' => $page_title]
];
$page_actions = '<a href="/admin/users.php" class="btn btn--secondary"><i data-lucide="arrow-left"></i> Tillbaka</a>';

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

 <div class="gs-max-w-900">
 <!-- Header Actions -->
 <div class="flex items-center justify-between mb-lg">
  <h1 class="">
  <i data-lucide="<?= $isNew ? 'user-plus' : 'user-cog' ?>"></i>
  <?= $isNew ? 'Skapa Användare' : 'Redigera Användare' ?>
  </h1>
  <a href="/admin/users.php" class="btn btn--secondary">
  <i data-lucide="arrow-left"></i>
  Tillbaka
  </a>
 </div>

 <!-- Message -->
 <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= $message ?>
  </div>
 <?php endif; ?>

 <!-- Edit Form -->
 <form method="POST" class="card">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="save">

  <div class="card-body">
  <div class="grid grid-cols-1 md-grid-cols-2 gap-lg">

   <!-- Account Information -->
   <div class="gs-md-col-span-2">
   <h2 class="text-primary mb-md">
    <i data-lucide="user"></i>
    Kontoinformation
   </h2>
   </div>

   <!-- Username -->
   <div>
   <label for="username" class="label">
    <i data-lucide="at-sign"></i>
    Användarnamn <span class="text-error">*</span>
   </label>
   <input
    type="text"
    id="username"
    name="username"
    class="input"
    required
    pattern="[a-zA-Z0-9_]+"
    value="<?= h($user['username'] ?? $_POST['username'] ?? '') ?>"
    placeholder="t.ex. johndoe"
   >
   <small class="text-secondary">Endast bokstäver, siffror och understreck</small>
   </div>

   <!-- Email -->
   <div>
   <label for="email" class="label">
    <i data-lucide="mail"></i>
    E-post <span class="text-error">*</span>
   </label>
   <input
    type="email"
    id="email"
    name="email"
    class="input"
    required
    value="<?= h($user['email'] ?? $_POST['email'] ?? '') ?>"
    placeholder="t.ex. john@example.com"
   >
   </div>

   <!-- Full Name -->
   <div>
   <label for="full_name" class="label">
    <i data-lucide="user"></i>
    Fullständigt namn
   </label>
   <input
    type="text"
    id="full_name"
    name="full_name"
    class="input"
    value="<?= h($user['full_name'] ?? $_POST['full_name'] ?? '') ?>"
    placeholder="t.ex. John Doe"
   >
   </div>

   <!-- Role -->
   <div>
   <label for="role" class="label">
    <i data-lucide="shield"></i>
    Roll <span class="text-error">*</span>
   </label>
   <select id="role" name="role" class="input" required>
    <option value="rider" <?= ($user['role'] ?? '') === 'rider' ? 'selected' : '' ?>>Rider</option>
    <option value="promotor" <?= ($user['role'] ?? '') === 'promotor' ? 'selected' : '' ?>>Promotor</option>
    <option value="admin" <?= ($user['role'] ?? '') === 'admin' ? 'selected' : '' ?>>Admin</option>
    <option value="super_admin" <?= ($user['role'] ?? '') === 'super_admin' ? 'selected' : '' ?>>Super Admin</option>
   </select>
   </div>

   <!-- Password Section -->
   <div class="gs-md-col-span-2 mt-lg">
   <h2 class="text-primary mb-md">
    <i data-lucide="lock"></i>
    <?= $isNew ? 'Lösenord' : 'Ändra lösenord' ?>
   </h2>
   <?php if (!$isNew): ?>
    <p class="text-sm text-secondary mb-md">Lämna tomt för att behålla nuvarande lösenord</p>
   <?php endif; ?>
   </div>

   <!-- Password -->
   <div>
   <label for="password" class="label">
    <i data-lucide="key"></i>
    <?= $isNew ? 'Lösenord' : 'Nytt lösenord' ?> <?= $isNew ? '<span class="text-error">*</span>' : '' ?>
   </label>
   <input
    type="password"
    id="password"
    name="password"
    class="input"
    <?= $isNew ? 'required' : '' ?>
    minlength="8"
    placeholder="Minst 8 tecken"
   >
   </div>

   <!-- Password Confirm -->
   <div>
   <label for="password_confirm" class="label">
    <i data-lucide="key"></i>
    Bekräfta lösenord <?= $isNew ? '<span class="text-error">*</span>' : '' ?>
   </label>
   <input
    type="password"
    id="password_confirm"
    name="password_confirm"
    class="input"
    <?= $isNew ? 'required' : '' ?>
    minlength="8"
    placeholder="Upprepa lösenordet"
   >
   </div>

   <!-- Status -->
   <div class="gs-md-col-span-2 mt-lg">
   <label class="checkbox flex items-center gap-sm">
    <input
    type="checkbox"
    name="active"
    value="1"
    <?= ($user['active'] ?? 1) ? 'checked' : '' ?>
    >
    <span>Aktiv användare</span>
   </label>
   <small class="text-secondary">Inaktiva användare kan inte logga in</small>
   </div>
  </div>
  </div>

  <div class="card-footer flex justify-between">
  <?php if (!$isNew): ?>
   <button type="button" class="btn btn-error" onclick="confirmDelete()">
   <i data-lucide="trash-2"></i>
   Ta bort
   </button>
  <?php else: ?>
   <div></div>
  <?php endif; ?>
  <div class="flex gap-md">
   <a href="/admin/users.php" class="btn btn--secondary">Avbryt</a>
   <button type="submit" class="btn btn--primary">
   <i data-lucide="save"></i>
   <?= $isNew ? 'Skapa användare' : 'Spara ändringar' ?>
   </button>
  </div>
  </div>
 </form>

 <?php if (!$isNew): ?>
 <!-- Role-specific actions -->
 <div class="card mt-lg">
  <div class="card-header">
  <h2 class="">Rollspecifika inställningar</h2>
  </div>
  <div class="card-body">
  <?php if ($user['role'] === 'promotor'): ?>
   <div class="flex items-center justify-between">
   <div>
    <h3 class="font-medium">Event-tilldelning</h3>
    <p class="text-sm text-secondary">Hantera vilka events denna promotor har tillgång till</p>
   </div>
   <a href="/admin/user-events.php?id=<?= $user['id'] ?>" class="btn btn--secondary">
    <i data-lucide="calendar"></i>
    Hantera events
   </a>
   </div>
  <?php elseif ($user['role'] === 'rider'): ?>
   <div class="flex items-center justify-between">
   <div>
    <h3 class="font-medium">Rider-koppling</h3>
    <p class="text-sm text-secondary">Koppla denna användare till en rider-profil</p>
   </div>
   <a href="/admin/user-rider.php?id=<?= $user['id'] ?>" class="btn btn--secondary">
    <i data-lucide="link"></i>
    Koppla rider
   </a>
   </div>
  <?php else: ?>
   <p class="text-secondary">Denna roll har inga extra inställningar.</p>
  <?php endif; ?>
  </div>
 </div>

 <!-- User Info -->
 <div class="card mt-lg">
  <div class="card-header">
  <h2 class="">Användarinformation</h2>
  </div>
  <div class="card-body">
  <div class="grid grid-cols-2 gap-md">
   <div>
   <span class="text-secondary text-sm">Skapad</span>
   <p><?= date('Y-m-d H:i', strtotime($user['created_at'])) ?></p>
   </div>
   <div>
   <span class="text-secondary text-sm">Uppdaterad</span>
   <p><?= date('Y-m-d H:i', strtotime($user['updated_at'])) ?></p>
   </div>
   <div>
   <span class="text-secondary text-sm">Senaste inloggning</span>
   <p><?= $user['last_login'] ? date('Y-m-d H:i', strtotime($user['last_login'])) : 'Aldrig' ?></p>
   </div>
  </div>
  </div>
 </div>
 <?php endif; ?>

 <!-- Delete form (hidden) -->
 <?php if (!$isNew): ?>
 <form id="deleteForm" method="POST" class="hidden">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="delete">
 </form>
 <?php endif; ?>
 </div>

<script>
function confirmDelete() {
 if (confirm('Är du säker på att du vill ta bort denna användare? Detta kan inte ångras.')) {
 document.getElementById('deleteForm').submit();
 }
}

// Password confirmation validation
document.getElementById('password_confirm')?.addEventListener('input', function() {
 const password = document.getElementById('password').value;
 if (this.value !== password) {
 this.setCustomValidity('Lösenorden matchar inte');
 } else {
 this.setCustomValidity('');
 }
});

document.getElementById('password')?.addEventListener('input', function() {
 const confirm = document.getElementById('password_confirm');
 if (confirm.value && confirm.value !== this.value) {
 confirm.setCustomValidity('Lösenorden matchar inte');
 } else {
 confirm.setCustomValidity('');
 }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
