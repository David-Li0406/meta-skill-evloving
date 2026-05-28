<?php
/**
 * Link User to Rider Profile
 * Only accessible by super_admin
 */
require_once __DIR__ . '/../config.php';
require_admin();

// Only super_admin can access this page
if (!hasRole('super_admin')) {
 http_response_code(403);
 die('Access denied: Only super administrators can link rider profiles.');
}

$db = getDB();

// Get user ID
$id = isset($_GET['id']) && is_numeric($_GET['id']) ? intval($_GET['id']) : null;

if (!$id) {
 header('Location: /admin/users.php');
 exit;
}

// Fetch user
$user = $db->getRow("SELECT * FROM admin_users WHERE id = ?", [$id]);

if (!$user || $user['role'] !== 'rider') {
 header('Location: /admin/users.php');
 exit;
}

$message = '';
$messageType = 'info';

// Get current rider link
$riderProfile = $db->getRow("
 SELECT rp.*, r.firstname, r.lastname, r.license_number, c.name as club_name
 FROM rider_profiles rp
 JOIN riders r ON rp.rider_id = r.id
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE rp.user_id = ?
", [$id]);

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';

 if ($action === 'link') {
 $riderId = isset($_POST['rider_id']) ? intval($_POST['rider_id']) : 0;
 $canEditProfile = isset($_POST['can_edit_profile']) ? 1 : 0;
 $canManageClub = isset($_POST['can_manage_club']) ? 1 : 0;

 if ($riderId) {
 try {
 // Check if rider is already linked to another user
 $existingLink = $db->getRow(
 "SELECT user_id FROM rider_profiles WHERE rider_id = ? AND user_id != ?",
  [$riderId, $id]
 );

 if ($existingLink) {
  $message = 'Denna rider är redan kopplad till en annan användare!';
  $messageType = 'error';
 } else {
  $currentAdmin = getCurrentAdmin();

  // Remove existing link if any
  $db->delete('rider_profiles', 'user_id = ?', [$id]);

  // Create new link
  $db->insert('rider_profiles', [
  'user_id' => $id,
  'rider_id' => $riderId,
  'can_edit_profile' => $canEditProfile,
  'can_manage_club' => $canManageClub,
  'approved_by' => $currentAdmin['id'],
  'approved_at' => date('Y-m-d H:i:s')
  ]);

  $message = 'Rider-profil kopplad!';
  $messageType = 'success';

  // Refresh rider profile
  $riderProfile = $db->getRow("
  SELECT rp.*, r.firstname, r.lastname, r.license_number, c.name as club_name
  FROM rider_profiles rp
  JOIN riders r ON rp.rider_id = r.id
  LEFT JOIN clubs c ON r.club_id = c.id
  WHERE rp.user_id = ?
 ", [$id]);
 }
 } catch (Exception $e) {
 $message = 'Ett fel uppstod: ' . $e->getMessage();
 $messageType = 'error';
 }
 }
 } elseif ($action === 'unlink') {
 try {
 $db->delete('rider_profiles', 'user_id = ?', [$id]);
 $message = 'Rider-koppling borttagen!';
 $messageType = 'success';
 $riderProfile = null;
 } catch (Exception $e) {
 $message = 'Ett fel uppstod: ' . $e->getMessage();
 $messageType = 'error';
 }
 } elseif ($action === 'update') {
 $canEditProfile = isset($_POST['can_edit_profile']) ? 1 : 0;
 $canManageClub = isset($_POST['can_manage_club']) ? 1 : 0;

 try {
 $db->update('rider_profiles', [
 'can_edit_profile' => $canEditProfile,
 'can_manage_club' => $canManageClub
 ], 'user_id = ?', [$id]);

 $message = 'Behörigheter uppdaterade!';
 $messageType = 'success';

 // Refresh rider profile
 $riderProfile = $db->getRow("
 SELECT rp.*, r.firstname, r.lastname, r.license_number, c.name as club_name
 FROM rider_profiles rp
 JOIN riders r ON rp.rider_id = r.id
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE rp.user_id = ?
", [$id]);
 } catch (Exception $e) {
 $message = 'Ett fel uppstod: ' . $e->getMessage();
 $messageType = 'error';
 }
 }
}

$pageTitle = 'Koppla Rider-profil';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container gs-max-w-900">
 <!-- Header -->
 <div class="flex items-center justify-between mb-lg">
 <div>
 <h1 class="">
  <i data-lucide="link"></i>
  Rider-koppling
 </h1>
 <p class="text-secondary">
  Koppla användare <strong><?= h($user['full_name'] ?: $user['username']) ?></strong> till en rider-profil
 </p>
 </div>
 <a href="/admin/user-edit.php?id=<?= $id ?>" class="btn btn--secondary">
 <i data-lucide="arrow-left"></i>
 Tillbaka
 </a>
 </div>

 <!-- Message -->
 <?php if ($message): ?>
 <div class="alert alert-<?= h($messageType) ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <?php if ($riderProfile): ?>
 <!-- Current Link -->
 <div class="card mb-lg">
 <div class="card-header">
  <h2 class="">
  <i data-lucide="user-check"></i>
  Kopplad rider-profil
  </h2>
 </div>
 <div class="card-body">
  <div class="flex items-center gap-lg mb-lg">
  <div class="gs-avatar gs-avatar-lg">
  <?= strtoupper(substr($riderProfile['firstname'], 0, 1) . substr($riderProfile['lastname'], 0, 1)) ?>
  </div>
  <div>
  <h3 class=""><?= h($riderProfile['firstname'] . ' ' . $riderProfile['lastname']) ?></h3>
  <p class="text-secondary">
  <?php if ($riderProfile['license_number']): ?>
   Licens: <?= h($riderProfile['license_number']) ?><br>
  <?php endif; ?>
  <?php if ($riderProfile['club_name']): ?>
   Klubb: <?= h($riderProfile['club_name']) ?>
  <?php endif; ?>
  </p>
  </div>
  </div>

  <form method="POST">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="update">

  <div class="mb-md">
  <label class="label">Behörigheter</label>
  <div class="flex flex-col gap-sm">
  <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="can_edit_profile" value="1" <?= $riderProfile['can_edit_profile'] ? 'checked' : '' ?>>
   <span>Kan redigera sin rider-profil</span>
  </label>
  <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="can_manage_club" value="1" <?= $riderProfile['can_manage_club'] ? 'checked' : '' ?>>
   <span>Kan hantera sin klubb</span>
  </label>
  </div>
  </div>

  <div class="flex gap-md">
  <button type="submit" class="btn btn--primary">
  <i data-lucide="save"></i>
  Uppdatera behörigheter
  </button>
  </div>
  </form>
 </div>
 <div class="card-footer">
  <form method="POST" onsubmit="return confirm('Är du säker på att du vill ta bort kopplingen?')">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="unlink">
  <button type="submit" class="btn btn-error">
  <i data-lucide="unlink"></i>
  Ta bort koppling
  </button>
  </form>
 </div>
 </div>
 <?php else: ?>
 <!-- Search and Link -->
 <div class="card">
 <div class="card-header">
  <h2 class="">
  <i data-lucide="search"></i>
  Sök och koppla rider
  </h2>
 </div>
 <div class="card-body">
  <div class="mb-lg">
  <label for="riderSearch" class="label">Sök rider</label>
  <div class="input-group">
  <i data-lucide="search"></i>
  <input
  type="text"
  id="riderSearch"
  class="input"
  placeholder="Skriv namn eller licensnummer..."
  autocomplete="off"
  >
  </div>
  </div>

  <div id="searchResults" class="mb-lg" class="hidden">
  <label class="label">Sökresultat</label>
  <div id="resultsList" class="border gs-rounded" style="max-height: 300px; overflow-y: auto;"></div>
  </div>

  <form method="POST" id="linkForm" class="hidden">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="link">
  <input type="hidden" name="rider_id" id="selectedRiderId">

  <div class="alert alert--info mb-md">
  <i data-lucide="user"></i>
  <span>Vald rider: <strong id="selectedRiderName"></strong></span>
  </div>

  <div class="mb-md">
  <label class="label">Behörigheter</label>
  <div class="flex flex-col gap-sm">
  <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="can_edit_profile" value="1" checked>
   <span>Kan redigera sin rider-profil</span>
  </label>
  <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="can_manage_club" value="1">
   <span>Kan hantera sin klubb</span>
  </label>
  </div>
  </div>

  <button type="submit" class="btn btn--primary">
  <i data-lucide="link"></i>
  Koppla rider
  </button>
  </form>
 </div>
 </div>
 <?php endif; ?>

 <!-- Help Text -->
 <div class="card mt-lg">
 <div class="card-body">
 <h3 class="font-medium mb-sm">Om rider-koppling</h3>
 <ul class="text-sm text-secondary" style="list-style: disc; padding-left: 1.5rem;">
  <li>En rider-profil kan endast kopplas till en användare</li>
  <li><strong>Redigera profil</strong> - Användaren kan uppdatera sin rider-information</li>
  <li><strong>Hantera klubb</strong> - Användaren kan redigera sin klubbs information (om rider är kopplad till en klubb)</li>
 </ul>
 </div>
 </div>
 </div>
</main>

<style>
.gs-avatar-lg {
 width: 64px;
 height: 64px;
 font-size: 20px;
}
.rider-result {
 padding: 12px 16px;
 border-bottom: 1px solid var(--border);
 cursor: pointer;
 transition: background-color 0.2s;
}
.rider-result:hover {
 background-color: var(--gs-bg-secondary);
}
.rider-result:last-child {
 border-bottom: none;
}
.rider-result.selected {
 background-color: var(--primary-light);
}
</style>

<script>
let searchTimeout;
const searchInput = document.getElementById('riderSearch');
const searchResults = document.getElementById('searchResults');
const resultsList = document.getElementById('resultsList');
const linkForm = document.getElementById('linkForm');
const selectedRiderId = document.getElementById('selectedRiderId');
const selectedRiderName = document.getElementById('selectedRiderName');

searchInput?.addEventListener('input', function() {
 clearTimeout(searchTimeout);
 const query = this.value.trim();

 if (query.length < 2) {
 searchResults.style.display = 'none';
 return;
 }

 searchTimeout = setTimeout(() => {
 fetch(`/api/search-riders.php?q=${encodeURIComponent(query)}&limit=20`)
 .then(response => response.json())
 .then(data => {
 if (data.riders && data.riders.length > 0) {
  resultsList.innerHTML = data.riders.map(rider => `
  <div class="rider-result" onclick="selectRider(${rider.id}, '${escapeHtml(rider.firstname + ' ' + rider.lastname)}')">
  <div class="font-medium">${escapeHtml(rider.firstname)} ${escapeHtml(rider.lastname)}</div>
  <div class="text-xs text-secondary">
  ${rider.license_number ? 'Licens: ' + escapeHtml(rider.license_number) : ''}
  ${rider.club_name ? ' • ' + escapeHtml(rider.club_name) : ''}
  </div>
  </div>
  `).join('');
  searchResults.style.display = 'block';
 } else {
  resultsList.innerHTML = '<div class="p-md text-center text-secondary">Inga riders hittades</div>';
  searchResults.style.display = 'block';
 }
 })
 .catch(error => {
 console.error('Search error:', error);
 });
 }, 300);
});

function selectRider(id, name) {
 selectedRiderId.value = id;
 selectedRiderName.textContent = name;
 linkForm.style.display = 'block';

 // Highlight selected
 document.querySelectorAll('.rider-result').forEach(el => el.classList.remove('selected'));
 event.currentTarget.classList.add('selected');
}

function escapeHtml(text) {
 const div = document.createElement('div');
 div.textContent = text;
 return div.innerHTML;
}
</script>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
