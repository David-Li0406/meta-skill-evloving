<?php
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$isSuperAdmin = hasRole('super_admin');

// Get rider ID
$id = isset($_GET['id']) && is_numeric($_GET['id']) ? intval($_GET['id']) : null;

if (!$id) {
 header('Location: /admin/riders.php');
 exit;
}

// Fetch rider
$rider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$id]);

if (!$rider) {
 header('Location: /admin/riders.php');
 exit;
}

// Get club membership for current year from rider_club_seasons
$currentYear = (int)date('Y');
$yearlyClub = $db->getRow("
    SELECT rcs.*, c.name as club_name
    FROM rider_club_seasons rcs
    JOIN clubs c ON rcs.club_id = c.id
    WHERE rcs.rider_id = ? AND rcs.season_year = ?
", [$id, $currentYear]);

// Check if rider has a linked user account
$riderUser = $db->getRow("
 SELECT au.*, rp.can_edit_profile, rp.can_manage_club
 FROM rider_profiles rp
 JOIN admin_users au ON rp.user_id = au.id
 WHERE rp.rider_id = ?
", [$id]);

$message = '';
$messageType = 'info';


// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? 'save_rider';

 if ($action === 'save_rider') {
 // Validate required fields
 $firstname = trim($_POST['firstname'] ?? '');
 $lastname = trim($_POST['lastname'] ?? '');

 if (empty($firstname) || empty($lastname)) {
 $message = 'Förnamn och efternamn är obligatoriska';
 $messageType = 'error';
 } else {
 // Helper function to normalize social media links
 $normalizeSocial = function($value, $platform) {
  $value = trim($value);
  if (empty($value)) return '';

  // If it's already a URL, return as-is
  if (strpos($value, 'http://') === 0 || strpos($value, 'https://') === 0) {
   return $value;
  }

  // Remove @ prefix if present
  $username = ltrim($value, '@');

  switch ($platform) {
   case 'instagram':
    return 'https://instagram.com/' . $username;
   case 'facebook':
    return 'https://facebook.com/' . $username;
   case 'strava':
    // Could be athlete ID or URL path
    if (is_numeric($username)) {
     return 'https://www.strava.com/athletes/' . $username;
    }
    return 'https://www.strava.com/athletes/' . $username;
   case 'youtube':
    // Handle @username or channel name
    if (strpos($value, '@') === 0) {
     return 'https://youtube.com/' . $value;
    }
    return 'https://youtube.com/@' . $username;
   case 'tiktok':
    return 'https://tiktok.com/@' . $username;
   default:
    return $value;
  }
 };

 // Prepare rider data (read-only fields excluded: license_number, license_type, license_category, license_valid_until)
 // Note: discipline is editable by superadmin
 $riderData = [
 'firstname' => $firstname,
 'lastname' => $lastname,
 'birth_year' => !empty($_POST['birth_year']) ? intval($_POST['birth_year']) : null,
 'gender' => trim($_POST['gender'] ?? ''),
 'club_id' => !empty($_POST['club_id']) ? intval($_POST['club_id']) : null,
 'email' => trim($_POST['email'] ?? ''),
 'nationality' => trim($_POST['nationality'] ?? 'SWE'),
 'team' => trim($_POST['team'] ?? ''),
 'notes' => trim($_POST['notes'] ?? ''),
 'active' => isset($_POST['active']) ? 1 : 0,
 // Profile image URL
 'profile_image_url' => trim($_POST['profile_image_url'] ?? '') ?: null,
 // Social media links (normalized to full URLs)
 'social_instagram' => $normalizeSocial($_POST['social_instagram'] ?? '', 'instagram'),
 'social_facebook' => $normalizeSocial($_POST['social_facebook'] ?? '', 'facebook'),
 'social_strava' => $normalizeSocial($_POST['social_strava'] ?? '', 'strava'),
 'social_youtube' => $normalizeSocial($_POST['social_youtube'] ?? '', 'youtube'),
 'social_tiktok' => $normalizeSocial($_POST['social_tiktok'] ?? '', 'tiktok'),
 ];

 // Superadmin can edit disciplines
 if ($isSuperAdmin && isset($_POST['disciplines'])) {
  $disciplines = is_array($_POST['disciplines']) ? $_POST['disciplines'] : [];
  $riderData['discipline'] = implode(',', array_filter($disciplines));
 }

 try {
 // Debug logging
 error_log("RIDER EDIT: Saving rider ID {$id}");
 error_log("RIDER EDIT: club_id from POST = " . var_export($_POST['club_id'] ?? 'NOT SET', true));
 error_log("RIDER EDIT: club_id in riderData = " . var_export($riderData['club_id'], true));

 $updateResult = $db->update('riders', $riderData, 'id = ?', [$id]);
 error_log("RIDER EDIT: Update result (rows affected) = {$updateResult}");

 // Refresh rider data to verify the save worked
 $rider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$id]);

 // Verify club_id was actually saved
 $savedClubId = $rider['club_id'];
 $expectedClubId = $riderData['club_id']; // Use the actual data we tried to save

 if ($savedClubId != $expectedClubId) {
  $message = 'Varning: Klubben kunde inte sparas korrekt. Försökte sätta klubb-ID till ' . ($expectedClubId ?? 'null') . ' men värdet är ' . ($savedClubId ?? 'null');
  $messageType = 'warning';
  error_log("RIDER EDIT: Club save mismatch - expected: " . var_export($expectedClubId, true) . ", got: " . var_export($savedClubId, true));
 } else {
  $message = 'Deltagare uppdaterad!';
  $messageType = 'success';
 }
 } catch (Exception $e) {
 $message = 'Ett fel uppstod: ' . $e->getMessage();
 $messageType = 'error';
 error_log("RIDER EDIT: Exception - " . $e->getMessage());
 }
 }
 } elseif ($action === 'update_license' && hasRole('super_admin')) {
 // Superadmin can update license number
 $newLicense = trim($_POST['license_number'] ?? '');

 try {
  // Validate license format if not empty
  if (!empty($newLicense)) {
   // Normalize: remove spaces and dashes, uppercase
   $newLicense = strtoupper(preg_replace('/[\s\-]/', '', $newLicense));

   // Accept SWE format (SWE + 7-11 digits) or pure numeric (8-11 digits)
   if (!preg_match('/^(SWE\d{7,11}|\d{8,11})$/i', $newLicense)) {
    throw new Exception('Ogiltigt licensformat. Använd SWE-format (t.ex. SWE2500123) eller numeriskt (8-11 siffror).');
   }
  }

  $db->update('riders', ['license_number' => $newLicense ?: null], 'id = ?', [$id]);
  $rider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$id]);
  $message = 'Licensnummer uppdaterat till: ' . ($newLicense ?: '(tomt)');
  $messageType = 'success';
 } catch (Exception $e) {
  $message = $e->getMessage();
  $messageType = 'error';
 }
 } elseif ($action === 'create_account' && hasRole('super_admin')) {
 // Create user account for this rider
 $username = trim($_POST['new_username'] ?? '');
 $email = trim($_POST['new_email'] ?? '') ?: $rider['email'];
 $password = $_POST['new_password'] ?? '';

 $errors = [];
 if (empty($username)) $errors[] = 'Användarnamn krävs';
 if (empty($password)) $errors[] = 'Lösenord krävs';
 if (strlen($password) < 8) $errors[] = 'Lösenord måste vara minst 8 tecken';

 // Check if username exists
 if ($username) {
 $existing = $db->getRow("SELECT id FROM admin_users WHERE username = ?", [$username]);
 if ($existing) $errors[] = 'Användarnamnet är redan taget';
 }

 if (empty($errors)) {
 try {
 // Create user
 $db->insert('admin_users', [
  'username' => $username,
  'password_hash' => password_hash($password, PASSWORD_DEFAULT),
  'email' => $email,
  'full_name' => $rider['firstname'] . ' ' . $rider['lastname'],
  'role' => 'rider',
  'active' => 1
 ]);
 $newUserId = $db->lastInsertId();

 // Link to rider
 $currentAdmin = getCurrentAdmin();
 $db->insert('rider_profiles', [
  'user_id' => $newUserId,
  'rider_id' => $id,
  'can_edit_profile' => 1,
  'can_manage_club' => 0,
  'approved_by' => $currentAdmin['id'],
  'approved_at' => date('Y-m-d H:i:s')
 ]);

 $message = 'Användarkonto skapat!';
 $messageType = 'success';

 // Refresh rider user
 $riderUser = $db->getRow("
  SELECT au.*, rp.can_edit_profile, rp.can_manage_club
  FROM rider_profiles rp
  JOIN admin_users au ON rp.user_id = au.id
  WHERE rp.rider_id = ?
 ", [$id]);
 } catch (Exception $e) {
 $message = 'Kunde inte skapa konto: ' . $e->getMessage();
 $messageType = 'error';
 }
 } else {
 $message = implode('<br>', $errors);
 $messageType = 'error';
 }
 } elseif ($action === 'update_account' && hasRole('super_admin') && $riderUser) {
 // Update user account
 $email = trim($_POST['account_email'] ?? '');
 $password = $_POST['account_password'] ?? '';
 $canEditProfile = isset($_POST['can_edit_profile']) ? 1 : 0;
 $canManageClub = isset($_POST['can_manage_club']) ? 1 : 0;
 $accountActive = isset($_POST['account_active']) ? 1 : 0;

 try {
 $userData = [
 'email' => $email,
 'active' => $accountActive
 ];
 if ($password) {
 if (strlen($password) < 8) {
  throw new Exception('Lösenord måste vara minst 8 tecken');
 }
 $userData['password_hash'] = password_hash($password, PASSWORD_DEFAULT);
 }

 $db->update('admin_users', $userData, 'id = ?', [$riderUser['id']]);
 $db->update('rider_profiles', [
 'can_edit_profile' => $canEditProfile,
 'can_manage_club' => $canManageClub
 ], 'user_id = ? AND rider_id = ?', [$riderUser['id'], $id]);

 $message = 'Användarkonto uppdaterat!';
 $messageType = 'success';

 // Refresh rider user
 $riderUser = $db->getRow("
 SELECT au.*, rp.can_edit_profile, rp.can_manage_club
 FROM rider_profiles rp
 JOIN admin_users au ON rp.user_id = au.id
 WHERE rp.rider_id = ?
", [$id]);
 } catch (Exception $e) {
 $message = 'Kunde inte uppdatera konto: ' . $e->getMessage();
 $messageType = 'error';
 }
 } elseif ($action === 'delete_account' && hasRole('super_admin') && $riderUser) {
 try {
 $db->delete('rider_profiles', 'user_id = ? AND rider_id = ?', [$riderUser['id'], $id]);
 $db->delete('admin_users', 'id = ?', [$riderUser['id']]);
 $message = 'Användarkonto borttaget!';
 $messageType = 'success';
 $riderUser = null;
 } catch (Exception $e) {
 $message = 'Kunde inte ta bort konto: ' . $e->getMessage();
 $messageType = 'error';
 }
 } elseif ($action === 'upgrade_to_promotor' && hasRole('super_admin') && $riderUser) {
 // Upgrade rider user to promotor role
 try {
 $db->update('admin_users', ['role' => 'promotor'], 'id = ?', [$riderUser['id']]);
 $message = 'Användaren har uppgraderats till Promotör! Du kan nu tilldela events.';
 $messageType = 'success';

 // Refresh rider user
 $riderUser = $db->getRow("
  SELECT au.*, rp.can_edit_profile, rp.can_manage_club
  FROM rider_profiles rp
  JOIN admin_users au ON rp.user_id = au.id
  WHERE rp.rider_id = ?
 ", [$id]);
 } catch (Exception $e) {
 $message = 'Kunde inte uppgradera: ' . $e->getMessage();
 $messageType = 'error';
 }
 } elseif ($action === 'downgrade_to_rider' && hasRole('super_admin') && $riderUser) {
 // Downgrade promotor back to rider role
 try {
 // First remove any event assignments
 $db->delete('promotor_events', 'user_id = ?', [$riderUser['id']]);
 $db->delete('promotor_series', 'user_id = ?', [$riderUser['id']]);

 $db->update('admin_users', ['role' => 'rider'], 'id = ?', [$riderUser['id']]);
 $message = 'Användaren har nedgraderats till Rider.';
 $messageType = 'success';

 // Refresh rider user
 $riderUser = $db->getRow("
  SELECT au.*, rp.can_edit_profile, rp.can_manage_club
  FROM rider_profiles rp
  JOIN admin_users au ON rp.user_id = au.id
  WHERE rp.rider_id = ?
 ", [$id]);
 } catch (Exception $e) {
 $message = 'Kunde inte nedgradera: ' . $e->getMessage();
 $messageType = 'error';
 }
 } elseif ($action === 'assign_club_admin' && hasRole('super_admin') && $riderUser) {
 // Assign user as club admin
 $clubIdToAdmin = isset($_POST['club_admin_id']) ? intval($_POST['club_admin_id']) : 0;
 $canEditProfile = isset($_POST['club_can_edit']) ? 1 : 0;
 $canUploadLogo = isset($_POST['club_can_upload']) ? 1 : 0;
 $canManageMembers = isset($_POST['club_can_members']) ? 1 : 0;

 if ($clubIdToAdmin > 0) {
 try {
  $currentAdmin = getCurrentAdmin();

  // Check if assignment already exists
  $existing = $db->getRow("SELECT id FROM club_admins WHERE user_id = ? AND club_id = ?",
   [$riderUser['id'], $clubIdToAdmin]);

  if ($existing) {
   // Update existing
   $db->update('club_admins', [
    'can_edit_profile' => $canEditProfile,
    'can_upload_logo' => $canUploadLogo,
    'can_manage_members' => $canManageMembers
   ], 'id = ?', [$existing['id']]);
   $message = 'Klubb-admin behörigheter uppdaterade!';
  } else {
   // Create new
   $db->insert('club_admins', [
    'user_id' => $riderUser['id'],
    'club_id' => $clubIdToAdmin,
    'can_edit_profile' => $canEditProfile,
    'can_upload_logo' => $canUploadLogo,
    'can_manage_members' => $canManageMembers,
    'granted_by' => $currentAdmin['id']
   ]);
   $message = 'Användaren är nu admin för klubben!';
  }
  $messageType = 'success';
 } catch (Exception $e) {
  $message = 'Kunde inte tilldela klubb-admin: ' . $e->getMessage();
  $messageType = 'error';
 }
 }
 } elseif ($action === 'remove_club_admin' && hasRole('super_admin') && $riderUser) {
 $clubAdminId = isset($_POST['club_admin_assignment_id']) ? intval($_POST['club_admin_assignment_id']) : 0;
 if ($clubAdminId > 0) {
 try {
  $db->delete('club_admins', 'id = ?', [$clubAdminId]);
  $message = 'Klubb-admin tilldelning borttagen!';
  $messageType = 'success';
 } catch (Exception $e) {
  $message = 'Kunde inte ta bort tilldelning: ' . $e->getMessage();
  $messageType = 'error';
 }
 }
 }
}

// Get clubs for dropdown - include inactive clubs to show current assignment even if club is inactive
$clubs = $db->getAll("SELECT id, name, active FROM clubs ORDER BY active DESC, name");

// Get current club info (in case it's inactive and not in the main list)
$currentClub = null;
if (!empty($rider['club_id'])) {
    $currentClub = $db->getRow("SELECT id, name, active FROM clubs WHERE id = ?", [$rider['club_id']]);
}

// Get club history per year
require_once __DIR__ . '/../includes/club-membership.php';
$clubHistory = getRiderClubHistory($db, $id);

// Get years with results (for showing which years are locked)
$yearsWithResults = $db->getAll("
    SELECT DISTINCT YEAR(e.date) as year, COUNT(*) as result_count
    FROM results r
    JOIN events e ON r.event_id = e.id
    WHERE r.cyclist_id = ?
    GROUP BY YEAR(e.date)
    ORDER BY year DESC
", [$id]);
$yearsWithResultsMap = [];
foreach ($yearsWithResults as $yr) {
    $yearsWithResultsMap[$yr['year']] = $yr['result_count'];
}

// Handle club history update
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'update_club_year') {
    // Note: checkCsrf already called in main POST handler above
    $updateYear = (int)($_POST['year'] ?? 0);
    $updateClubId = (int)($_POST['club_id'] ?? 0);

    error_log("CLUB HISTORY: Updating year={$updateYear}, club_id={$updateClubId} for rider {$id}");

    if ($updateYear <= 0) {
        $message = 'Ogiltigt år valt';
        $messageType = 'error';
    } elseif ($updateClubId <= 0) {
        $message = 'Du måste välja en klubb';
        $messageType = 'error';
    } else {
        // Super admin can force update locked years
        $force = hasRole('super_admin');
        $result = setRiderClubForYear($db, $id, $updateClubId, $updateYear, $force);
        if ($result['success']) {
            $message = $result['message'];
            $messageType = 'success';
            // Refresh club history
            $clubHistory = getRiderClubHistory($db, $id);
            error_log("CLUB HISTORY: Successfully updated");
        } else {
            $message = $result['message'];
            $messageType = 'error';
            error_log("CLUB HISTORY: Failed - " . $result['message']);
        }
    }
}

// Page config for admin layout
$page_title = 'Redigera Deltagare';
$breadcrumbs = [
    ['label' => 'Deltagare', 'url' => '/admin/riders'],
    ['label' => h($rider['firstname'] . ' ' . $rider['lastname'])]
];

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Message -->
<?php if ($message): ?>
 <div class="alert alert--<?= h($messageType) ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Profile Image -->
 <div class="card mb-lg">
 <div class="card-body">
 <h2 class="text-primary mb-md">
  <i data-lucide="camera"></i>
  Profilbild
 </h2>
 <div class="flex items-center gap-lg flex-wrap">
  <?php
  $initials = strtoupper(substr($rider['firstname'] ?? '', 0, 1) . substr($rider['lastname'] ?? '', 0, 1));
  $imageUrl = $rider['avatar_url'] ?? $rider['profile_image_url'] ?? '';
  ?>
  <div class="admin-avatar-container" style="position: relative;">
   <div class="profile-image-preview" id="adminAvatarPreview" style="width: 120px; height: 120px; border-radius: var(--radius-md); background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; overflow: hidden; color: white; font-size: 2.5rem; font-weight: 700; cursor: pointer;" onclick="document.getElementById('adminAvatarInput').click()">
   <?php if ($imageUrl): ?>
   <img src="<?= h($imageUrl) ?>" alt="Profilbild" id="adminAvatarImage" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
   <span style="display: none;"><?= h($initials) ?></span>
   <?php else: ?>
   <span id="adminAvatarInitials"><?= h($initials) ?></span>
   <?php endif; ?>
   </div>
   <div id="adminAvatarLoading" style="display: none; position: absolute; inset: 0; background: rgba(0,0,0,0.6); border-radius: var(--radius-md); align-items: center; justify-content: center;">
    <div style="width: 32px; height: 32px; border: 3px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
   </div>
  </div>
  <div class="flex flex-col gap-sm" style="flex: 1; min-width: 200px;">
   <div class="flex gap-sm items-center flex-wrap">
    <label class="btn btn-secondary" style="cursor: pointer; margin: 0;">
     <i data-lucide="upload" style="width: 16px; height: 16px;"></i>
     Ladda upp bild
     <input type="file" id="adminAvatarInput" accept="image/jpeg,image/png,image/gif,image/webp" style="display: none;">
    </label>
    <span id="adminAvatarStatus" style="font-size: 0.875rem;"></span>
   </div>
   <div style="margin-top: 8px;">
    <label class="label">Eller ange bild-URL manuellt</label>
    <input type="text" name="profile_image_url" id="profileImageUrlInput" class="input" value="<?= h($imageUrl) ?>" placeholder="https://exempel.com/bild.jpg" form="rider-form">
   </div>
   <small class="text-secondary">Max 2MB. JPG, PNG, GIF eller WebP.</small>
  </div>
 </div>
 </div>
 </div>
 <style>
 @keyframes spin { to { transform: rotate(360deg); } }
 </style>
 <script>
 document.addEventListener('DOMContentLoaded', function() {
  const avatarInput = document.getElementById('adminAvatarInput');
  const avatarPreview = document.getElementById('adminAvatarPreview');
  const avatarLoading = document.getElementById('adminAvatarLoading');
  const avatarStatus = document.getElementById('adminAvatarStatus');
  const urlInput = document.getElementById('profileImageUrlInput');
  const riderId = <?= intval($id) ?>;

  if (!avatarInput) return;

  avatarInput.addEventListener('change', async function(e) {
   const file = e.target.files[0];
   if (!file) return;

   const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
   if (!allowedTypes.includes(file.type)) {
    showStatus('Otillåten filtyp', 'error');
    return;
   }

   if (file.size > 2 * 1024 * 1024) {
    showStatus('Max 2MB', 'error');
    return;
   }

   avatarLoading.style.display = 'flex';
   showStatus('Laddar upp...', 'info');

   const formData = new FormData();
   formData.append('avatar', file);
   formData.append('rider_id', riderId);

   try {
    const response = await fetch('/api/update-avatar.php', {
     method: 'POST',
     body: formData
    });
    const result = await response.json();

    if (result.success) {
     showStatus('Uppladdad!', 'success');
     updatePreview(result.avatar_url);
     urlInput.value = result.avatar_url;
    } else {
     showStatus(result.error || 'Fel', 'error');
    }
   } catch (error) {
    showStatus('Uppladdning misslyckades', 'error');
   } finally {
    avatarLoading.style.display = 'none';
   }
  });

  function updatePreview(src) {
   avatarPreview.innerHTML = '<img src="' + src + '" alt="Profilbild" style="width: 100%; height: 100%; object-fit: cover;">';
  }

  function showStatus(msg, type) {
   avatarStatus.textContent = msg;
   avatarStatus.style.color = type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#6b7280';
   if (type === 'success') setTimeout(() => { avatarStatus.textContent = ''; }, 3000);
  }
 });
 </script>

 <!-- Edit Form -->
 <form method="POST" class="card" id="rider-form">
 <?= csrf_field() ?>
 <input type="hidden" name="action" value="save_rider">

 <div class="card-body">
 <div class="grid gap-lg grid-2-col">
  <!-- Personal Information -->
  <div class="col-span-2">
  <h2 class="text-primary mb-md">
  <i data-lucide="user"></i>
  Personuppgifter
  </h2>
  </div>

  <!-- First Name (Required) -->
  <div>
  <label for="firstname" class="label">
  <i data-lucide="user"></i>
  Förnamn <span class="text-error">*</span>
  </label>
  <input
  type="text"
  id="firstname"
  name="firstname"
  class="input"
  required
  value="<?= h($rider['firstname']) ?>"
  >
  </div>

  <!-- Last Name (Required) -->
  <div>
  <label for="lastname" class="label">
  <i data-lucide="user"></i>
  Efternamn <span class="text-error">*</span>
  </label>
  <input
  type="text"
  id="lastname"
  name="lastname"
  class="input"
  required
  value="<?= h($rider['lastname']) ?>"
  >
  </div>

  <!-- Birth Year -->
  <div>
  <label for="birth_year" class="label">
  <i data-lucide="calendar"></i>
  Födelseår
  </label>
  <input
  type="number"
  id="birth_year"
  name="birth_year"
  class="input"
  min="1900"
  max="<?= date('Y') ?>"
  value="<?= h($rider['birth_year']) ?>"
  >
  </div>

  <!-- Gender -->
  <div>
  <label for="gender" class="label">
  <i data-lucide="users"></i>
  Kön
  </label>
  <select id="gender" name="gender" class="input">
  <option value="">Välj...</option>
  <option value="M" <?= $rider['gender'] === 'M' ? 'selected' : '' ?>>Man</option>
  <option value="F" <?= $rider['gender'] === 'F' ? 'selected' : '' ?>>Kvinna</option>
  </select>
  </div>

  <!-- License Information -->
  <div class="col-span-2 mt-lg">
  <h2 class="text-primary mb-md">
  <i data-lucide="award"></i>
  Licensinformation
  </h2>
  </div>

  <!-- Club -->
  <div>
  <label for="club_id" class="label">
  <i data-lucide="building"></i>
  Klubb
  </label>
  <select id="club_id" name="club_id" class="input">
  <option value="">Ingen klubb</option>
  <?php foreach ($clubs as $club): ?>
  <option value="<?= $club['id'] ?>" <?= $rider['club_id'] == $club['id'] ? 'selected' : '' ?><?= !$club['active'] ? ' class="text-secondary"' : '' ?>>
   <?= h($club['name']) ?><?= !$club['active'] ? ' (inaktiv)' : '' ?>
  </option>
  <?php endforeach; ?>
  </select>
  <?php if ($currentClub && !$currentClub['active']): ?>
  <small class="text-warning" style="display: block; margin-top: 0.25rem;">
   <i data-lucide="alert-triangle" class="icon-xs"></i>
   Nuvarande klubb "<?= h($currentClub['name']) ?>" är inaktiv
  </small>
  <?php endif; ?>
  </div>

  <!-- License Number -->
  <div>
  <label class="label">
  <i data-lucide="credit-card"></i>
  Licensnummer
  </label>
  <?php if (hasRole('super_admin')): ?>
  <div class="flex gap-sm items-center">
   <input
   type="text"
   id="license_number_edit"
   class="input"
   value="<?= h($rider['license_number'] ?: '') ?>"
   placeholder="SWE2500123"
   style="flex: 1;"
   >
   <button type="button" class="btn btn--primary btn--sm" onclick="updateLicense()">
   <i data-lucide="save"></i>
   </button>
  </div>
  <small class="text-secondary">Superadmin: Redigera licensnummer (SWE-format utan bindestreck)</small>
  <?php else: ?>
  <input
  type="text"
  class="input"
  value="<?= h($rider['license_number'] ?: '-') ?>"
  disabled
  >
  <small class="text-secondary">Importeras från SCF/UCI - kan inte ändras</small>
  <?php endif; ?>
  </div>

  <!-- License Category (read-only) -->
  <div>
  <label class="label">
  <i data-lucide="tag"></i>
  Licenskategori
  </label>
  <input
  type="text"
  class="input"
  value="<?= h($rider['license_category'] ?: '-') ?>"
  disabled
  >
  <small class="text-secondary">Importeras från SCF</small>
  </div>

  <!-- Nationality -->
  <div>
  <label for="nationality" class="label">
  <i data-lucide="flag"></i>
  Nationalitet
  </label>
  <select id="nationality" name="nationality" class="input">
  <option value="SWE" <?= ($rider['nationality'] ?? 'SWE') === 'SWE' ? 'selected' : '' ?>>🇸🇪 Sverige</option>
  <option value="NOR" <?= ($rider['nationality'] ?? '') === 'NOR' ? 'selected' : '' ?>>🇳🇴 Norge</option>
  <option value="DEN" <?= ($rider['nationality'] ?? '') === 'DEN' ? 'selected' : '' ?>>🇩🇰 Danmark</option>
  <option value="FIN" <?= ($rider['nationality'] ?? '') === 'FIN' ? 'selected' : '' ?>>🇫🇮 Finland</option>
  <option value="GBR" <?= ($rider['nationality'] ?? '') === 'GBR' ? 'selected' : '' ?>>🇬🇧 Storbritannien</option>
  </select>
  </div>

  <!-- Team -->
  <div>
  <label for="team" class="label">
  <i data-lucide="users"></i>
  Lagnamn
  </label>
  <input
  type="text"
  id="team"
  name="team"
  class="input"
  value="<?= h($rider['team'] ?? '') ?>"
  placeholder="Separat från klubb"
  >
  </div>

  <!-- Read-only Fields -->
  <div class="col-span-2 mt-lg">
  <h2 class="text-primary mb-md">
  <i data-lucide="database"></i>
  Systemdata (endast läsning)
  </h2>
  </div>

  <!-- SCF Verification Status -->
  <div class="col-span-2" style="background: var(--color-bg-hover); padding: var(--space-md); border-radius: var(--radius-md); margin-bottom: var(--space-md);">
  <div style="display: flex; align-items: center; gap: var(--space-sm); margin-bottom: var(--space-sm);">
    <i data-lucide="badge-check" style="color: var(--color-accent);"></i>
    <strong>SCF Licensverifiering</strong>
    <?php if (!empty($rider['scf_license_year']) && $rider['scf_license_year'] == date('Y')): ?>
    <span class="badge badge-success">Verifierad <?= $rider['scf_license_year'] ?></span>
    <?php elseif (!empty($rider['scf_license_year'])): ?>
    <span class="badge badge-warning">Verifierad <?= $rider['scf_license_year'] ?> (ej aktuellt år)</span>
    <?php else: ?>
    <span class="badge badge-danger">Ej verifierad</span>
    <?php endif; ?>
  </div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-md); font-size: var(--text-sm);">
    <div>
      <span class="text-muted">Licenstyp:</span>
      <strong><?= h($rider['scf_license_type'] ?? $rider['license_type'] ?? '-') ?></strong>
    </div>
    <div>
      <span class="text-muted">Licensklass:</span>
      <strong><?= h($rider['license_category'] ?? '-') ?></strong>
    </div>
    <div>
      <span class="text-muted">Disciplin:</span>
      <strong><?= h($rider['discipline'] ?? '-') ?></strong>
    </div>
    <div>
      <span class="text-muted">SCF Klubb:</span>
      <strong><?= h($rider['scf_club_name'] ?? '-') ?></strong>
    </div>
    <?php if ($yearlyClub): ?>
    <div>
      <span class="text-muted">Klubb <?= $currentYear ?>:</span>
      <strong><?= h($yearlyClub['club_name']) ?></strong>
      <?php if ($yearlyClub['locked']): ?>
      <span class="badge badge-success" style="margin-left: 4px; font-size: 10px;">Låst</span>
      <?php endif; ?>
    </div>
    <?php endif; ?>
    <?php if (!empty($rider['scf_license_verified_at'])): ?>
    <div>
      <span class="text-muted">Senast verifierad:</span>
      <strong><?= date('Y-m-d H:i', strtotime($rider['scf_license_verified_at'])) ?></strong>
    </div>
    <?php endif; ?>
  </div>
  </div>

  <!-- License Year (read-only) -->
  <div>
  <label class="label">
  <i data-lucide="calendar"></i>
  Licensår
  </label>
  <input
  type="text"
  class="input"
  value="<?= h($rider['license_year'] ?? '-') ?>"
  disabled
  >
  <small class="text-secondary">Importeras från SCF</small>
  </div>

  <!-- Gravity ID (read-only) -->
  <div>
  <label class="label">
  <i data-lucide="zap"></i>
  Gravity ID
  </label>
  <input
  type="text"
  class="input"
  value="<?= h($rider['gravity_id'] ?? '-') ?>"
  disabled
  >
  <small class="text-secondary">Tilldelas av systemet</small>
  </div>

  <!-- Disciplines Checkboxes (editable by superadmin) -->
  <div class="col-span-2">
  <label class="label">
  <i data-lucide="list"></i>
  Licensierade discipliner
  <?php if ($isSuperAdmin): ?><span class="badge badge-warning" style="margin-left: 0.5rem;">Redigerbar</span><?php endif; ?>
  </label>
  <?php
  // Use the actual discipline values from the database
  // These come from SCF/UCI imports: MTB, BMX, LVG (Landsväg), Para, Bana, etc.
  $allDisciplines = [
  'MTB' => 'MTB (Mountainbike)',
  'BMX' => 'BMX',
  'LVG' => 'Landsväg',
  'BANA' => 'Bana',
  'CX' => 'Cyclocross',
  'PARA' => 'Para-cykling',
  'TRIAL' => 'Trial',
  'E-CYCLING' => 'E-cycling',
  'GRAVEL' => 'Gravel'
  ];

  // Get the rider's discipline from the database (single value or comma-separated)
  $riderDiscipline = strtoupper(trim($rider['discipline'] ?? ''));
  $riderDisciplines = array_map('trim', explode(',', $riderDiscipline));

  // Also check the disciplines JSON if available
  $disciplinesJson = $rider['disciplines'] ? json_decode($rider['disciplines'], true) ?: [] : [];
  $riderDisciplines = array_merge($riderDisciplines, $disciplinesJson);
  $riderDisciplines = array_unique(array_filter(array_map('strtoupper', $riderDisciplines)));
  ?>
  <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 0.5rem;">
  <?php foreach ($allDisciplines as $code => $name): ?>
  <?php $isChecked = in_array(strtoupper($code), $riderDisciplines); ?>
  <label class="flex items-center gap-sm" style="padding: 0.5rem 0.75rem; background: <?= $isChecked ? 'rgba(97, 206, 112, 0.15)' : 'var(--color-bg-sunken)' ?>; border: 1px solid <?= $isChecked ? 'var(--color-accent)' : 'var(--color-border)' ?>; border-radius: var(--radius-md); cursor: <?= $isSuperAdmin ? 'pointer' : 'not-allowed' ?>; opacity: <?= $isChecked || $isSuperAdmin ? '1' : '0.6' ?>;">
  <input type="checkbox" name="disciplines[]" value="<?= $code ?>" <?= $isChecked ? 'checked' : '' ?> <?= $isSuperAdmin ? '' : 'disabled' ?> style="accent-color: var(--color-accent);">
  <span class="text-sm" style="color: <?= $isChecked ? 'var(--color-accent)' : 'var(--color-text-secondary)' ?>;"><?= h($name) ?></span>
  </label>
  <?php endforeach; ?>
  </div>
  <?php if (!empty($riderDiscipline) && $riderDiscipline !== ''): ?>
  <small class="text-secondary" style="display: block; margin-top: 0.5rem;">Från licens: <strong><?= h($rider['discipline']) ?></strong></small>
  <?php elseif (!$isSuperAdmin): ?>
  <small class="text-secondary" style="display: block; margin-top: 0.5rem;">Ingen disciplin registrerad i licensdatan.</small>
  <?php endif; ?>
  </div>

  <!-- Contact Information -->
  <div class="col-span-2 mt-lg">
  <h2 class="text-primary mb-md">
  <i data-lucide="mail"></i>
  Kontaktuppgifter
  </h2>
  </div>

  <!-- Email -->
  <div>
  <label for="email" class="label">
  <i data-lucide="mail"></i>
  E-post
  </label>
  <input
  type="email"
  id="email"
  name="email"
  class="input"
  value="<?= h($rider['email']) ?>"
  >
  </div>

  <!-- Active Status -->
  <div>
  <label class="checkbox-label">
  <input
  type="checkbox"
  id="active"
  name="active"
  class="checkbox"
  <?= $rider['active'] ? 'checked' : '' ?>
  >
  <span>
  <i data-lucide="check-circle"></i>
  Aktiv deltagare
  </span>
  </label>
  </div>

  <!-- Social Media Links -->
  <div class="col-span-2 mt-lg">
  <h2 class="text-primary mb-md">
  <i data-lucide="share-2"></i>
  Sociala medier
  </h2>
  </div>

  <!-- Instagram -->
  <div>
  <label for="social_instagram" class="label">
  <i data-lucide="instagram"></i>
  Instagram
  </label>
  <input
  type="text"
  id="social_instagram"
  name="social_instagram"
  class="input"
  value="<?= h($rider['social_instagram'] ?? '') ?>"
  placeholder="användarnamn eller URL"
  >
  </div>

  <!-- Facebook -->
  <div>
  <label for="social_facebook" class="label">
  <i data-lucide="facebook"></i>
  Facebook
  </label>
  <input
  type="text"
  id="social_facebook"
  name="social_facebook"
  class="input"
  value="<?= h($rider['social_facebook'] ?? '') ?>"
  placeholder="användarnamn eller URL"
  >
  </div>

  <!-- Strava -->
  <div>
  <label for="social_strava" class="label">
  <svg viewBox="0 0 24 24" class="icon-sm" style="fill: currentColor;"><path d="M15.387 17.944l-2.089-4.116h-3.065L15.387 24l5.15-10.172h-3.066m-7.008-5.599l2.836 5.598h4.172L10.463 0l-7 13.828h4.169"/></svg>
  Strava
  </label>
  <input
  type="text"
  id="social_strava"
  name="social_strava"
  class="input"
  value="<?= h($rider['social_strava'] ?? '') ?>"
  placeholder="Athlete ID eller URL"
  >
  </div>

  <!-- YouTube -->
  <div>
  <label for="social_youtube" class="label">
  <i data-lucide="youtube"></i>
  YouTube
  </label>
  <input
  type="text"
  id="social_youtube"
  name="social_youtube"
  class="input"
  value="<?= h($rider['social_youtube'] ?? '') ?>"
  placeholder="Kanalnamn eller URL"
  >
  </div>

  <!-- TikTok -->
  <div>
  <label for="social_tiktok" class="label">
  <svg viewBox="0 0 24 24" class="icon-sm" style="fill: currentColor;"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>
  TikTok
  </label>
  <input
  type="text"
  id="social_tiktok"
  name="social_tiktok"
  class="input"
  value="<?= h($rider['social_tiktok'] ?? '') ?>"
  placeholder="användarnamn eller URL"
  >
  </div>

  <!-- Notes -->
  <div class="col-span-2">
  <label for="notes" class="label">
  <i data-lucide="file-text"></i>
  Anteckningar
  </label>
  <textarea
  id="notes"
  name="notes"
  class="input"
  rows="3"
  ><?= h($rider['notes']) ?></textarea>
  </div>
 </div>
 </div>

 <div class="card-footer">
 <div class="flex gap-md justify-end">
  <a href="/admin/riders.php" class="btn btn--secondary">
  <i data-lucide="x"></i>
  Avbryt
  </a>
  <button type="submit" class="btn btn--primary">
  <i data-lucide="save"></i>
  Spara ändringar
  </button>
 </div>
 </div>
 </form>

 <!-- Club History per Year -->
 <div class="card mt-lg">
 <div class="card-header">
 <h2>
  <i data-lucide="history"></i>
  Klubbtillhörighet per år
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  Klubbtillhörighet låses per år när åkaren har resultat. Poäng och ranking följer klubben för respektive år.
 </p>

 <?php if (empty($clubHistory) && empty($yearsWithResultsMap)): ?>
  <div class="alert alert--info">
  <i data-lucide="info"></i>
  Ingen klubbhistorik finns ännu. Klubbtillhörighet skapas automatiskt vid import av resultat.
  </div>
 <?php else: ?>
  <div class="table-responsive">
  <table class="table">
  <thead>
  <tr>
   <th>År</th>
   <th>Klubb</th>
   <th>Resultat</th>
   <th>Status</th>
   <th>Åtgärd</th>
  </tr>
  </thead>
  <tbody>
  <?php
  // Combine club history with years that have results
  $allYears = [];
  foreach ($clubHistory as $ch) {
   $allYears[$ch['season_year']] = $ch;
  }
  foreach ($yearsWithResultsMap as $year => $count) {
   if (!isset($allYears[$year])) {
   $allYears[$year] = [
    'season_year' => $year,
    'club_id' => null,
    'club_name' => null,
    'locked' => 0,
    'results_count' => $count
   ];
   }
  }
  krsort($allYears);

  foreach ($allYears as $year => $data):
   $resultsCount = $data['results_count'] ?? ($yearsWithResultsMap[$year] ?? 0);
   // Only locked if: club is already set AND (explicitly locked OR has results)
   // If no club is set, allow setting one even if results exist
   $hasClubSet = !empty($data['club_id']);
   $isLocked = $hasClubSet && ($data['locked'] || $resultsCount > 0);
  ?>
  <tr>
   <td><strong><?= $year ?></strong></td>
   <td>
   <?php if ($data['club_name']): ?>
    <?= h($data['club_name']) ?>
   <?php else: ?>
    <span class="text-secondary">Ej satt</span>
   <?php endif; ?>
   </td>
   <td>
   <?php if ($resultsCount > 0): ?>
    <span class="badge badge-primary"><?= $resultsCount ?> resultat</span>
   <?php else: ?>
    <span class="badge badge-secondary">Inga resultat</span>
   <?php endif; ?>
   </td>
   <td>
   <?php if ($isLocked): ?>
    <span class="badge badge-success">
    <i data-lucide="lock" class="icon-xs"></i>
    Låst
    </span>
   <?php else: ?>
    <span class="badge badge-warning">
    <i data-lucide="unlock" class="icon-xs"></i>
    Kan ändras
    </span>
   <?php endif; ?>
   </td>
   <td>
   <?php if (!$isLocked || hasRole('super_admin')): ?>
    <form method="POST" class="flex items-center gap-sm">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="update_club_year">
    <input type="hidden" name="year" value="<?= $year ?>">
    <select name="club_id" class="input" style="min-width: 150px;" required>
     <option value="">Välj klubb...</option>
     <?php foreach ($clubs as $club): ?>
     <option value="<?= $club['id'] ?>" <?= ($data['club_id'] ?? '') == $club['id'] ? 'selected' : '' ?>>
      <?= h($club['name']) ?>
     </option>
     <?php endforeach; ?>
    </select>
    <button type="submit" class="btn btn--primary btn--sm" title="<?= $isLocked ? 'Super admin: Tvinga ändring' : 'Spara' ?>">
     <i data-lucide="save"></i>
    </button>
    <?php if ($isLocked): ?>
    <span class="text-warning text-xs">(admin)</span>
    <?php endif; ?>
    </form>
   <?php else: ?>
    <span class="text-secondary text-sm">Kan ej ändras</span>
   <?php endif; ?>
   </td>
  </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 <?php endif; ?>

 <!-- Add new year -->
 <div class="mt-lg" style="border-top: 1px solid var(--color-border); padding-top: var(--space-md);">
  <h4 class="mb-sm">Lägg till klubb för nytt år</h4>
  <?php
  // Make sure $allYears is initialized
  if (!isset($allYears)) {
   $allYears = [];
   foreach ($clubHistory as $ch) {
   $allYears[$ch['season_year']] = $ch;
   }
  }
  ?>
  <form method="POST" class="flex items-center gap-sm" style="flex-wrap: wrap;">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="update_club_year">
  <select name="year" class="input" style="width: 100px;">
   <?php for ($y = (int)date('Y'); $y >= 2020; $y--): ?>
   <?php if (!isset($allYears[$y])): ?>
   <option value="<?= $y ?>"><?= $y ?></option>
   <?php endif; ?>
   <?php endfor; ?>
  </select>
  <select name="club_id" class="input" style="min-width: 200px;" required>
   <option value="">Välj klubb...</option>
   <?php foreach ($clubs as $club): ?>
   <option value="<?= $club['id'] ?>"><?= h($club['name']) ?></option>
   <?php endforeach; ?>
  </select>
  <button type="submit" class="btn btn--secondary btn--sm">
   <i data-lucide="plus"></i>
   Lägg till
  </button>
  </form>
 </div>
 </div>
 </div>

 <?php if (hasRole('super_admin')): ?>
 <!-- User Account Section -->
 <div class="card mt-lg">
 <div class="card-header">
 <h2 class="">
  <i data-lucide="key"></i>
  Användarkonto
 </h2>
 </div>
 <div class="card-body">
 <?php if ($riderUser): ?>
  <!-- Existing Account -->
  <form method="POST">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="update_account">

  <div class="grid gap-lg grid-2-col">
  <div class="col-span-2">
  <div class="alert alert--info">
   <i data-lucide="user-check"></i>
   <span>Denna deltagare har ett användarkonto: <strong><?= h($riderUser['username']) ?></strong></span>
  </div>
  </div>

  <div>
  <label class="label">
   <i data-lucide="at-sign"></i>
   Användarnamn
  </label>
  <input type="text" class="input" value="<?= h($riderUser['username']) ?>" disabled>
  <small class="text-secondary">Kan inte ändras</small>
  </div>

  <div>
  <label for="account_email" class="label">
   <i data-lucide="mail"></i>
   E-post för inloggning
  </label>
  <input
   type="email"
   id="account_email"
   name="account_email"
   class="input"
   value="<?= h($riderUser['email']) ?>"
  >
  </div>

  <div>
  <label for="account_password" class="label">
   <i data-lucide="key"></i>
   Nytt lösenord
  </label>
  <input
   type="password"
   id="account_password"
   name="account_password"
   class="input"
   placeholder="Lämna tomt för att behålla"
   minlength="8"
  >
  <small class="text-secondary">Minst 8 tecken</small>
  </div>

  <div>
  <label class="label">Senaste inloggning</label>
  <input type="text" class="input" value="<?= $riderUser['last_login'] ? date('Y-m-d H:i', strtotime($riderUser['last_login'])) : 'Aldrig' ?>" disabled>
  </div>

  <div class="col-span-2">
  <label class="label">Behörigheter</label>
  <div class="flex gap-lg flex-wrap">
   <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="can_edit_profile" value="1" <?= $riderUser['can_edit_profile'] ? 'checked' : '' ?>>
   <span>Kan redigera sin profil</span>
   </label>
   <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="can_manage_club" value="1" <?= $riderUser['can_manage_club'] ? 'checked' : '' ?>>
   <span>Kan hantera sin klubb</span>
   </label>
   <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="account_active" value="1" <?= $riderUser['active'] ? 'checked' : '' ?>>
   <span>Konto aktivt</span>
   </label>
  </div>
  </div>
  </div>

  <div class="flex justify-between mt-lg">
  <button type="button" class="btn btn-error" onclick="confirmDeleteAccount()">
  <i data-lucide="trash-2"></i>
  Ta bort konto
  </button>
  <button type="submit" class="btn btn--primary">
  <i data-lucide="save"></i>
  Uppdatera konto
  </button>
  </div>
  </form>

  <form id="deleteAccountForm" method="POST" class="hidden">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="delete_account">
  </form>
 <?php else: ?>
  <!-- Create Account -->
  <form method="POST">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="create_account">

  <div class="alert alert--warning mb-lg">
  <i data-lucide="user-x"></i>
  <span>Denna deltagare har inget användarkonto. Skapa ett för att låta dem logga in.</span>
  </div>

  <div class="grid gap-lg grid-2-col">
  <div>
  <label for="new_username" class="label">
   <i data-lucide="at-sign"></i>
   Användarnamn <span class="text-error">*</span>
  </label>
  <input
   type="text"
   id="new_username"
   name="new_username"
   class="input"
   required
   pattern="[a-zA-Z0-9_]+"
   placeholder="t.ex. <?= strtolower(preg_replace('/[^a-zA-Z0-9]/', '', $rider['firstname'] . $rider['lastname'])) ?>"
  >
  <small class="text-secondary">Endast bokstäver, siffror och understreck</small>
  </div>

  <div>
  <label for="new_email" class="label">
   <i data-lucide="mail"></i>
   E-post
  </label>
  <input
   type="email"
   id="new_email"
   name="new_email"
   class="input"
   value="<?= h($rider['email']) ?>"
   placeholder="Använder rider-email om tom"
  >
  </div>

  <div>
  <label for="new_password" class="label">
   <i data-lucide="key"></i>
   Lösenord <span class="text-error">*</span>
  </label>
  <input
   type="password"
   id="new_password"
   name="new_password"
   class="input"
   required
   minlength="8"
   placeholder="Minst 8 tecken"
  >
  </div>

  <div class="flex" style="align-items: flex-end;">
  <button type="submit" class="btn btn--primary">
   <i data-lucide="user-plus"></i>
   Skapa användarkonto
  </button>
  </div>
  </div>
  </form>
 <?php endif; ?>
 </div>
 </div>

 <!-- Role Management Section (only if user has account) -->
 <?php if ($riderUser): ?>
 <div class="card mt-lg">
 <div class="card-header">
 <h2>
  <i data-lucide="shield"></i>
  Rollhantering
 </h2>
 </div>
 <div class="card-body">
 <?php
 $currentRole = $riderUser['role'] ?? 'rider';
 $roleLabels = [
  'rider' => 'Rider',
  'promotor' => 'Promotör',
  'admin' => 'Admin',
  'super_admin' => 'Super Admin'
 ];
 $roleBadges = [
  'rider' => 'badge-secondary',
  'promotor' => 'badge-primary',
  'admin' => 'badge-warning',
  'super_admin' => 'badge-danger'
 ];
 ?>
 <div class="flex items-center gap-md mb-lg flex-wrap">
  <span class="text-secondary">Nuvarande roll:</span>
  <span class="badge <?= $roleBadges[$currentRole] ?? 'badge-secondary' ?>">
   <?= $roleLabels[$currentRole] ?? $currentRole ?>
  </span>
 </div>

 <?php if ($currentRole === 'rider'): ?>
  <!-- Upgrade to Promotor -->
  <div class="alert alert--info mb-md">
  <i data-lucide="arrow-up-circle"></i>
  <div>
   <strong>Uppgradera till Promotör</strong>
   <p class="text-sm mt-xs">Som promotör kan användaren hantera events, registreringar och resultat för tilldelade tävlingar.</p>
  </div>
  </div>
  <form method="POST" class="mb-lg">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="upgrade_to_promotor">
  <button type="submit" class="btn btn--primary" onclick="return confirm('Vill du uppgradera denna användare till Promotör?')">
   <i data-lucide="arrow-up-circle"></i>
   Uppgradera till Promotör
  </button>
  </form>
 <?php elseif ($currentRole === 'promotor'): ?>
  <!-- Already promotor - show event management link -->
  <div class="flex items-center justify-between flex-wrap gap-md mb-lg">
  <div>
   <h3 class="font-medium">Event-tilldelning</h3>
   <p class="text-sm text-secondary">Hantera vilka events denna promotör har tillgång till</p>
  </div>
  <a href="/admin/user-events.php?id=<?= $riderUser['id'] ?>" class="btn btn--secondary">
   <i data-lucide="calendar"></i>
   Hantera events
  </a>
  </div>

  <!-- Downgrade option -->
  <div style="border-top: 1px solid var(--color-border); padding-top: var(--space-md); margin-top: var(--space-md);">
  <form method="POST">
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="downgrade_to_rider">
   <button type="submit" class="btn btn--secondary" onclick="return confirm('Vill du nedgradera denna användare till Rider? Alla event-tilldelningar tas bort.')">
   <i data-lucide="arrow-down-circle"></i>
   Nedgradera till Rider
   </button>
  </form>
  </div>
 <?php else: ?>
  <div class="alert alert--warning">
  <i data-lucide="alert-triangle"></i>
  <span>Denna användare har rollen <?= $roleLabels[$currentRole] ?? $currentRole ?> och kan inte ändras härifrån.</span>
  </div>
 <?php endif; ?>
 </div>
 </div>

 <!-- Club Admin Section -->
 <div class="card mt-lg">
 <div class="card-header">
 <h2>
  <i data-lucide="building"></i>
  Klubb-administration
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  Tilldela användaren som administratör för en eller flera klubbar. Detta låter dem redigera klubbinformation och ladda upp logotyper.
 </p>

 <?php
 // Get current club admin assignments for this user
 $clubAdminAssignments = $db->getAll("
  SELECT ca.*, c.name as club_name
  FROM club_admins ca
  JOIN clubs c ON ca.club_id = c.id
  WHERE ca.user_id = ?
  ORDER BY c.name
 ", [$riderUser['id']]);
 ?>

 <?php if (!empty($clubAdminAssignments)): ?>
 <div class="table-responsive mb-lg">
  <table class="table">
  <thead>
   <tr>
   <th>Klubb</th>
   <th>Redigera</th>
   <th>Logo</th>
   <th>Medlemmar</th>
   <th>Åtgärd</th>
   </tr>
  </thead>
  <tbody>
   <?php foreach ($clubAdminAssignments as $assignment): ?>
   <tr>
   <td><strong><?= h($assignment['club_name']) ?></strong></td>
   <td><?= $assignment['can_edit_profile'] ? '<i data-lucide="check" class="text-accent"></i>' : '<i data-lucide="x" class="text-secondary"></i>' ?></td>
   <td><?= $assignment['can_upload_logo'] ? '<i data-lucide="check" class="text-accent"></i>' : '<i data-lucide="x" class="text-secondary"></i>' ?></td>
   <td><?= $assignment['can_manage_members'] ? '<i data-lucide="check" class="text-accent"></i>' : '<i data-lucide="x" class="text-secondary"></i>' ?></td>
   <td>
    <form method="POST" style="display: inline;">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="remove_club_admin">
    <input type="hidden" name="club_admin_assignment_id" value="<?= $assignment['id'] ?>">
    <button type="submit" class="btn btn-error btn--sm" onclick="return confirm('Ta bort denna tilldelning?')">
     <i data-lucide="trash-2"></i>
    </button>
    </form>
   </td>
   </tr>
   <?php endforeach; ?>
  </tbody>
  </table>
 </div>
 <?php endif; ?>

 <!-- Add new club admin assignment -->
 <form method="POST" class="card" style="background: var(--color-bg-sunken); border: 1px dashed var(--color-border);">
  <div class="card-body">
  <h4 class="mb-md">Lägg till klubbtilldelning</h4>
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="assign_club_admin">

  <div class="grid gap-md" style="grid-template-columns: 1fr auto;">
   <div>
   <label for="club_admin_id" class="label">Välj klubb</label>
   <select name="club_admin_id" id="club_admin_id" class="input" required>
    <option value="">Välj klubb...</option>
    <?php
    // Filter out already assigned clubs
    $assignedClubIds = array_column($clubAdminAssignments, 'club_id');
    foreach ($clubs as $club):
     if (in_array($club['id'], $assignedClubIds)) continue;
    ?>
    <option value="<?= $club['id'] ?>"><?= h($club['name']) ?><?= !$club['active'] ? ' (inaktiv)' : '' ?></option>
    <?php endforeach; ?>
   </select>
   </div>
   <div style="display: flex; align-items: flex-end;">
   <button type="submit" class="btn btn--primary">
    <i data-lucide="plus"></i>
    Lägg till
   </button>
   </div>
  </div>

  <div class="flex gap-lg flex-wrap mt-md">
   <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="club_can_edit" value="1" checked>
   <span class="text-sm">Kan redigera klubbinfo</span>
   </label>
   <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="club_can_upload" value="1" checked>
   <span class="text-sm">Kan ladda upp logo</span>
   </label>
   <label class="checkbox flex items-center gap-sm">
   <input type="checkbox" name="club_can_members" value="1">
   <span class="text-sm">Kan hantera medlemmar</span>
   </label>
  </div>
  </div>
 </form>
 </div>
 </div>
 <?php endif; ?>
 <?php endif; ?>

<style>
@media (max-width: 768px) {
 .grid[style*="grid-template-columns: repeat(2, 1fr)"] {
  grid-template-columns: 1fr !important;
 }
 .grid [style*="grid-column: span 2"] {
  grid-column: span 1 !important;
 }
}
</style>

<script>
function confirmDeleteAccount() {
 if (confirm('Är du säker på att du vill ta bort användarkontot? Deltagarprofilen behålls.')) {
 document.getElementById('deleteAccountForm').submit();
 }
}

function updateLicense() {
 var newLicense = document.getElementById('license_number_edit').value.trim();
 if (confirm('Uppdatera licensnummer till: ' + (newLicense || '(tomt)') + '?')) {
 // Create and submit form
 var form = document.createElement('form');
 form.method = 'POST';
 form.innerHTML = '<?= csrf_field() ?>' +
  '<input type="hidden" name="action" value="update_license">' +
  '<input type="hidden" name="license_number" value="' + newLicense.replace(/"/g, '&quot;') + '">';
 document.body.appendChild(form);
 form.submit();
 }
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
