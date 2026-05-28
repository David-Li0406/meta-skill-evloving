<?php
/**
 * Club Edit Page - V3 Unified Layout
 * Supports both editing existing clubs and creating new ones
 * Version: v2.0.0 [2025-12-13]
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Get club ID - 0 or null means creating new club
$id = isset($_GET['id']) && is_numeric($_GET['id']) ? intval($_GET['id']) : 0;
$isNew = ($id === 0);

// Default values for new club
$club = [
    'name' => '',
    'short_name' => '',
    'region' => '',
    'city' => '',
    'country' => 'Sverige',
    'website' => '',
    'logo' => '',
    'email' => '',
    'phone' => '',
    'contact_person' => '',
    'address' => '',
    'postal_code' => '',
    'description' => '',
    'facebook' => '',
    'instagram' => '',
    'youtube' => '',
    'tiktok' => '',
    'org_number' => '',
    'scf_id' => '',
    'scf_district' => '',
    'rf_registered' => 0,
    'rf_registered_year' => null,
    'swish_number' => '',
    'swish_name' => '',
    'payment_enabled' => 0,
    'active' => 1
];

// Fetch existing club data if editing
if (!$isNew) {
    $existingClub = $db->getRow("SELECT * FROM clubs WHERE id = ?", [$id]);

    if (!$existingClub) {
        $_SESSION['message'] = 'Klubb hittades inte';
        $_SESSION['messageType'] = 'error';
        header('Location: /admin/clubs.php');
        exit;
    }

    $club = array_merge($club, $existingClub);
}

// Initialize message variables
$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? 'save';

    // Handle delete action
    if ($action === 'delete' && !$isNew) {
        $riderCount = $db->getRow("SELECT COUNT(*) as cnt FROM riders WHERE club_id = ?", [$id])['cnt'] ?? 0;

        if ($riderCount > 0) {
            $message = "Kan inte ta bort klubb med $riderCount medlemmar. Flytta medlemmarna först.";
            $messageType = 'error';
        } else {
            try {
                $db->delete('clubs', 'id = ?', [$id]);
                header('Location: /admin/clubs.php?msg=deleted');
                exit;
            } catch (Exception $e) {
                $message = 'Fel vid borttagning: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } else {
        // Validate required fields
        $name = trim($_POST['name'] ?? '');

        if (empty($name)) {
            $message = 'Klubbnamn är obligatoriskt';
            $messageType = 'error';
        } else {
            // Prepare club data
            $logoValue = trim($_POST['logo'] ?? '');
            $clubData = [
                'name' => $name,
                'short_name' => trim($_POST['short_name'] ?? ''),
                'region' => trim($_POST['region'] ?? ''),
                'city' => trim($_POST['city'] ?? ''),
                'country' => trim($_POST['country'] ?? 'Sverige'),
                'website' => trim($_POST['website'] ?? ''),
                'logo' => $logoValue,
                'logo_url' => $logoValue, // Also save to logo_url column
                'email' => trim($_POST['email'] ?? ''),
                'phone' => trim($_POST['phone'] ?? ''),
                'contact_person' => trim($_POST['contact_person'] ?? ''),
                'address' => trim($_POST['address'] ?? ''),
                'postal_code' => trim($_POST['postal_code'] ?? ''),
                'description' => trim($_POST['description'] ?? ''),
                'facebook' => trim($_POST['facebook'] ?? ''),
                'instagram' => trim($_POST['instagram'] ?? ''),
                'youtube' => trim($_POST['youtube'] ?? ''),
                'tiktok' => trim($_POST['tiktok'] ?? ''),
                'org_number' => trim($_POST['org_number'] ?? ''),
                'scf_id' => trim($_POST['scf_id'] ?? ''),
                'scf_district' => trim($_POST['scf_district'] ?? '') ?: null,
                'rf_registered' => isset($_POST['rf_registered']) ? 1 : 0,
                'rf_registered_year' => !empty($_POST['rf_registered_year']) ? (int)$_POST['rf_registered_year'] : null,
                'swish_number' => trim($_POST['swish_number'] ?? '') ?: null,
                'swish_name' => trim($_POST['swish_name'] ?? '') ?: null,
                'payment_enabled' => isset($_POST['payment_enabled']) ? 1 : 0,
                'active' => isset($_POST['active']) ? 1 : 0,
            ];

            try {
                if ($isNew) {
                    $db->insert('clubs', $clubData);
                    $id = $db->lastInsertId();
                    header('Location: /admin/club-edit.php?id=' . $id . '&msg=created');
                    exit;
                } else {
                    $db->update('clubs', $clubData, 'id = ?', [$id]);
                    $message = 'Klubb uppdaterad!';
                    $messageType = 'success';

                    // Refresh club data
                    $club = $db->getRow("SELECT * FROM clubs WHERE id = ?", [$id]);
                }
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Handle URL messages
if (isset($_GET['msg'])) {
    switch ($_GET['msg']) {
        case 'created':
            $message = 'Klubb skapad!';
            $messageType = 'success';
            break;
    }
}

// Nationality code to country name mapping
$nationalityToCountry = [
    'SWE' => 'Sverige',
    'NOR' => 'Norge',
    'DNK' => 'Danmark',
    'FIN' => 'Finland',
    'DEU' => 'Tyskland',
    'FRA' => 'Frankrike',
    'CHE' => 'Schweiz',
    'AUT' => 'Österrike',
    'ITA' => 'Italien',
    'ESP' => 'Spanien',
    'GBR' => 'Storbritannien',
    'USA' => 'USA',
];

// Get rider count for this club
$riderCount = 0;
$riders = [];
$majorityNationality = null;
$majorityCountry = null;
if (!$isNew) {
    $riderCount = $db->getRow("SELECT COUNT(*) as count FROM riders WHERE club_id = ?", [$id])['count'] ?? 0;

    // Get first 10 riders for sidebar
    $riders = $db->getAll("
        SELECT id, firstname, lastname, gender, birth_year, active, nationality
        FROM riders
        WHERE club_id = ?
        ORDER BY lastname, firstname
        LIMIT 10
    ", [$id]);

    // Auto-detect majority nationality for club
    if ($riderCount > 0) {
        $nationalityCounts = $db->getAll("
            SELECT nationality, COUNT(*) as cnt
            FROM riders
            WHERE club_id = ? AND nationality IS NOT NULL AND nationality != ''
            GROUP BY nationality
            ORDER BY cnt DESC
            LIMIT 1
        ", [$id]);

        if (!empty($nationalityCounts)) {
            $majorityNat = $nationalityCounts[0]['nationality'];
            $majorityCount = $nationalityCounts[0]['cnt'];

            // Check if majority (>50%) have a non-SWE nationality
            if ($majorityNat !== 'SWE' && ($majorityCount / $riderCount) > 0.5) {
                $majorityNationality = $majorityNat;
                $majorityCountry = $nationalityToCountry[$majorityNat] ?? null;

                // Auto-update club country if different
                if ($majorityCountry && $club['country'] !== $majorityCountry) {
                    $db->update('clubs', ['country' => $majorityCountry], 'id = ?', [$id]);
                    $club['country'] = $majorityCountry;
                    $message = "Klubbens land har automatiskt uppdaterats till $majorityCountry baserat på medlemmarnas nationalitet.";
                    $messageType = 'success';
                }
            }
        }
    }
}

// Page config for admin layout
$page_title = $isNew ? 'Ny Klubb' : 'Redigera Klubb';
$breadcrumbs = [
    ['label' => 'Klubbar', 'url' => '/admin/clubs.php'],
    ['label' => $isNew ? 'Ny Klubb' : h($club['name'])]
];

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
    <div class="alert alert--<?= $messageType ?> mb-lg">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
        <?= h($message) ?>
    </div>
<?php endif; ?>

<!-- Form -->
<form method="POST">
  <?= csrf_field() ?>

  <div class="grid grid-cols-1 gs-lg-grid-cols-3 gap-lg">
  <!-- Main Content (2 columns) -->
  <div class="gs-lg-col-span-2">
   <!-- Basic Information -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="info"></i>
    Grundläggande information
    </h2>
   </div>
   <div class="card-body">
    <div class="grid grid-cols-1 gap-md">
    <!-- Name -->
    <div>
     <label for="name" class="label">
     Klubbnamn <span class="text-error">*</span>
     </label>
     <input
     type="text"
     id="name"
     name="name"
     class="input"
     required
     value="<?= h($club['name']) ?>"
     >
    </div>

    <!-- Short Name and SCF ID -->
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="short_name" class="label">Förkortning</label>
     <input
      type="text"
      id="short_name"
      name="short_name"
      class="input"
      value="<?= h($club['short_name'] ?? '') ?>"
      placeholder="T.ex. UCK, TGS"
     >
     </div>
     <div>
     <label for="scf_id" class="label">SCF Klubb-ID</label>
     <input
      type="text"
      id="scf_id"
      name="scf_id"
      class="input"
      value="<?= h($club['scf_id'] ?? '') ?>"
      placeholder="Svenska Cykelförbundets ID"
     >
     </div>
    </div>

    <!-- Org Number -->
    <div>
     <label for="org_number" class="label">Organisationsnummer</label>
     <input
     type="text"
     id="org_number"
     name="org_number"
     class="input"
     value="<?= h($club['org_number'] ?? '') ?>"
     placeholder="T.ex. 802000-0000"
     >
    </div>
    </div>
   </div>
   </div>

   <!-- Payment/Swish Settings -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="smartphone"></i>
    Betalning (Swish)
    </h2>
   </div>
   <div class="card-body">
    <p class="text-secondary mb-md">
    Om klubben arrangerar tävlingar kan betalning gå direkt till klubbens Swish.
    </p>
    <div class="grid gap-lg" style="grid-template-columns: repeat(2, 1fr);">
    <!-- Swish Number -->
    <div>
     <label for="swish_number" class="label">Swish-nummer</label>
     <input
     type="text"
     id="swish_number"
     name="swish_number"
     class="input"
     value="<?= h($club['swish_number'] ?? '') ?>"
     placeholder="070-123 45 67 eller 123-456 78 90"
     >
     <small class="text-secondary">Mobilnummer eller Swish-företagsnummer</small>
    </div>

    <!-- Swish Name -->
    <div>
     <label for="swish_name" class="label">Mottagarnamn</label>
     <input
     type="text"
     id="swish_name"
     name="swish_name"
     class="input"
     value="<?= h($club['swish_name'] ?? '') ?>"
     placeholder="Klubbens namn"
     >
     <small class="text-secondary">Visas för deltagare vid betalning</small>
    </div>

    <!-- Payment Enabled -->
    <div style="grid-column: span 2;">
     <label class="checkbox-label">
     <input type="checkbox" name="payment_enabled" value="1"
      <?= ($club['payment_enabled'] ?? 0) ? 'checked' : '' ?>>
     <span>Aktivera som betalningsmottagare</span>
     </label>
     <small class="text-secondary">Klubben kan väljas som mottagare för eventbetalningar</small>
    </div>
    </div>
   </div>
   </div>

   <!-- Description & Logo -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="file-text"></i>
    Övrigt
    </h2>
   </div>
   <div class="card-body">
    <div class="grid gap-lg" style="grid-template-columns: repeat(2, 1fr);">

    <!-- Description -->
    <div>
     <label for="description" class="label">Beskrivning</label>
     <textarea
     id="description"
     name="description"
     class="input"
     rows="4"
     placeholder="Beskriv klubben..."
     ><?= h($club['description'] ?? '') ?></textarea>
    </div>

    <!-- Logo Upload -->
    <div>
     <label class="label">Logotyp</label>
     <?php $logoUrl = $club['logo_url'] ?? $club['logo'] ?? ''; ?>
     <div class="flex items-start gap-md">
      <div class="club-logo-container" style="position: relative;">
       <div class="logo-preview" id="clubLogoPreview" style="width: 120px; height: 80px; border-radius: var(--radius-md); background: var(--color-bg-sunken); display: flex; align-items: center; justify-content: center; overflow: hidden; cursor: pointer; border: 2px dashed var(--color-border);" onclick="document.getElementById('clubLogoInput').click()">
        <?php if ($logoUrl): ?>
        <img src="<?= h($logoUrl) ?>" alt="Klubblogotyp" id="clubLogoImage" style="max-width: 100%; max-height: 100%; object-fit: contain;">
        <?php else: ?>
        <i data-lucide="image" style="width: 32px; height: 32px; color: var(--color-text-secondary);"></i>
        <?php endif; ?>
       </div>
       <div id="clubLogoLoading" style="display: none; position: absolute; inset: 0; background: rgba(0,0,0,0.6); border-radius: var(--radius-md); align-items: center; justify-content: center;">
        <div style="width: 24px; height: 24px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
       </div>
      </div>
      <div style="flex: 1;">
       <label class="btn btn-secondary btn--sm" style="cursor: pointer; display: inline-flex;">
        <i data-lucide="upload" style="width: 14px; height: 14px;"></i>
        Ladda upp
        <input type="file" id="clubLogoInput" accept="image/jpeg,image/png,image/gif,image/webp" style="display: none;">
       </label>
       <span id="clubLogoStatus" style="font-size: 0.75rem; display: block; margin-top: 0.5rem;"></span>
       <input type="hidden" name="logo" id="logoUrlInput" value="<?= h($logoUrl) ?>">
       <small class="text-secondary" style="display: block; margin-top: 0.5rem;">Max 2MB. JPG, PNG, GIF eller WebP.</small>
      </div>
     </div>
    </div>
    </div>
   </div>
   </div>

   <!-- Address -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="map-pin"></i>
    Adress
    </h2>
   </div>
   <div class="card-body">
    <div class="grid grid-cols-1 gap-md">
    <!-- Address -->
    <div>
     <label for="address" class="label">Gatuadress</label>
     <input
     type="text"
     id="address"
     name="address"
     class="input"
     value="<?= h($club['address'] ?? '') ?>"
     placeholder="T.ex. Storgatan 1"
     >
    </div>

    <!-- Postal Code and City -->
    <div class="grid grid-cols-3 gap-md">
     <div>
     <label for="postal_code" class="label">Postnummer</label>
     <input
      type="text"
      id="postal_code"
      name="postal_code"
      class="input"
      value="<?= h($club['postal_code'] ?? '') ?>"
      placeholder="123 45"
     >
     </div>
     <div class="gs-col-span-2">
     <label for="city" class="label">Stad</label>
     <input
      type="text"
      id="city"
      name="city"
      class="input"
      value="<?= h($club['city'] ?? '') ?>"
     >
     </div>
    </div>

    <!-- Region and Country -->
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="region" class="label">Region</label>
     <input
      type="text"
      id="region"
      name="region"
      class="input"
      value="<?= h($club['region'] ?? '') ?>"
      placeholder="T.ex. Västsverige"
     >
     </div>
     <div>
     <label for="country" class="label">Land</label>
     <select id="country" name="country" class="input">
      <option value="Sverige" <?= ($club['country'] ?? 'Sverige') === 'Sverige' ? 'selected' : '' ?>>Sverige</option>
      <option value="Norge" <?= ($club['country'] ?? '') === 'Norge' ? 'selected' : '' ?>>Norge</option>
      <option value="Danmark" <?= ($club['country'] ?? '') === 'Danmark' ? 'selected' : '' ?>>Danmark</option>
      <option value="Finland" <?= ($club['country'] ?? '') === 'Finland' ? 'selected' : '' ?>>Finland</option>
      <option value="Tyskland" <?= ($club['country'] ?? '') === 'Tyskland' ? 'selected' : '' ?>>Tyskland</option>
      <option value="Frankrike" <?= ($club['country'] ?? '') === 'Frankrike' ? 'selected' : '' ?>>Frankrike</option>
      <option value="Schweiz" <?= ($club['country'] ?? '') === 'Schweiz' ? 'selected' : '' ?>>Schweiz</option>
      <option value="Österrike" <?= ($club['country'] ?? '') === 'Österrike' ? 'selected' : '' ?>>Österrike</option>
      <option value="Italien" <?= ($club['country'] ?? '') === 'Italien' ? 'selected' : '' ?>>Italien</option>
      <option value="Spanien" <?= ($club['country'] ?? '') === 'Spanien' ? 'selected' : '' ?>>Spanien</option>
      <option value="Storbritannien" <?= ($club['country'] ?? '') === 'Storbritannien' ? 'selected' : '' ?>>Storbritannien</option>
      <option value="USA" <?= ($club['country'] ?? '') === 'USA' ? 'selected' : '' ?>>USA</option>
     </select>
     </div>
    </div>
    </div>
   </div>
   </div>

   <!-- RF/SCF Registration -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="award"></i>
    Förbundsregistrering
    </h2>
   </div>
   <div class="card-body">
    <div class="grid grid-cols-1 gap-md">

    <!-- SCF District -->
    <div>
     <label for="scf_district" class="label">SCF Distrikt</label>
     <select id="scf_district" name="scf_district" class="input">
      <option value="">-- Välj distrikt --</option>
      <?php
      $scfDistricts = [
          'Bohuslän-Dals Cykelförbund',
          'Dalarnas Cykelförbund',
          'Gästriklands Cykelförbund',
          'Göteborgs Cykelförbund',
          'Hallands Cykelförbund',
          'Hälsinglands Cykelförbund',
          'Jämtland-Härjedalens Cykelförbund',
          'Norrbottens Cykelförbund',
          'Skånes Cykelförbund',
          'Smålands Cykelförbund',
          'Stockholms Cykelförbund',
          'Södermanlands Cykelförbund',
          'Upplands Cykelförbund',
          'Värmlands Cykelförbund',
          'Västerbottens Cykelförbund',
          'Västergötlands Cykelförbund',
          'Västernorrlands Cykelförbund',
          'Västmanlands Cykelförbund',
          'Örebro Läns Cykelförbund',
          'Östergötlands Cykelförbund'
      ];
      foreach ($scfDistricts as $district):
      ?>
      <option value="<?= h($district) ?>" <?= ($club['scf_district'] ?? '') === $district ? 'selected' : '' ?>><?= h($district) ?></option>
      <?php endforeach; ?>
     </select>
     <p class="form-help">Svenska Cykelförbundets distriktstillhörighet</p>
    </div>

    <!-- RF Registration -->
    <div class="grid grid-cols-2 gap-md">
     <div>
      <label class="checkbox-label" style="display: flex; align-items: center; gap: var(--space-sm); cursor: pointer;">
       <input
        type="checkbox"
        id="rf_registered"
        name="rf_registered"
        value="1"
        <?= !empty($club['rf_registered']) ? 'checked' : '' ?>
        style="width: 18px; height: 18px;"
       >
       <span><strong>RF-registrerad</strong></span>
      </label>
      <p class="form-help">Aktiv klubb hos Riksidrottsförbundet</p>
     </div>
     <div>
      <label for="rf_registered_year" class="label">Registreringsår</label>
      <input
       type="number"
       id="rf_registered_year"
       name="rf_registered_year"
       class="input"
       value="<?= h($club['rf_registered_year'] ?? '') ?>"
       placeholder="<?= date('Y') ?>"
       min="2000"
       max="<?= date('Y') + 1 ?>"
      >
     </div>
    </div>

    </div>
   </div>
   </div>

   <!-- Contact Information -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="phone"></i>
    Kontaktinformation
    </h2>
   </div>
   <div class="card-body">
    <div class="grid grid-cols-1 gap-md">
    <!-- Contact Person -->
    <div>
     <label for="contact_person" class="label">Kontaktperson</label>
     <input
     type="text"
     id="contact_person"
     name="contact_person"
     class="input"
     value="<?= h($club['contact_person'] ?? '') ?>"
     placeholder="Namn på kontaktperson"
     >
    </div>

    <!-- Email and Phone -->
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="email" class="label">E-post</label>
     <input
      type="email"
      id="email"
      name="email"
      class="input"
      value="<?= h($club['email'] ?? '') ?>"
      placeholder="info@klubb.se"
     >
     </div>
     <div>
     <label for="phone" class="label">Telefon</label>
     <input
      type="tel"
      id="phone"
      name="phone"
      class="input"
      value="<?= h($club['phone'] ?? '') ?>"
      placeholder="070-123 45 67"
     >
     </div>
    </div>

    <!-- Website -->
    <div>
     <label for="website" class="label">Webbplats</label>
     <input
     type="url"
     id="website"
     name="website"
     class="input"
     value="<?= h($club['website'] ?? '') ?>"
     placeholder="https://klubb.se"
     >
    </div>

    <!-- Social Media -->
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="facebook" class="label">
      <i data-lucide="facebook" class="icon-sm"></i>
      Facebook
     </label>
     <input
      type="url"
      id="facebook"
      name="facebook"
      class="input"
      value="<?= h($club['facebook'] ?? '') ?>"
      placeholder="https://facebook.com/..."
     >
     </div>
     <div>
     <label for="instagram" class="label">
      <i data-lucide="instagram" class="icon-sm"></i>
      Instagram
     </label>
     <input
      type="text"
      id="instagram"
      name="instagram"
      class="input"
      value="<?= h($club['instagram'] ?? '') ?>"
      placeholder="@användarnamn"
     >
     </div>
    </div>
    <div class="grid grid-cols-2 gap-md mt-md">
     <div>
     <label for="youtube" class="label">
      <i data-lucide="youtube" class="icon-sm"></i>
      YouTube
     </label>
     <input
      type="url"
      id="youtube"
      name="youtube"
      class="input"
      value="<?= h($club['youtube'] ?? '') ?>"
      placeholder="https://youtube.com/..."
     >
     </div>
     <div>
     <label for="tiktok" class="label">
      <i data-lucide="music" class="icon-sm"></i>
      TikTok
     </label>
     <input
      type="text"
      id="tiktok"
      name="tiktok"
      class="input"
      value="<?= h($club['tiktok'] ?? '') ?>"
      placeholder="@användarnamn"
     >
     </div>
    </div>
    </div>
   </div>
   </div>
  </div>

  <!-- Sidebar (1 column) -->
  <div>
   <!-- Status -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="settings"></i>
    Status
    </h2>
   </div>
   <div class="card-body">
    <label class="checkbox-label" style="display: flex; align-items: center; gap: var(--space-sm); cursor: pointer;">
    <input
     type="checkbox"
     name="active"
     class="checkbox"
     <?= $club['active'] ? 'checked' : '' ?>
     style="width: 18px; height: 18px; accent-color: var(--color-accent);"
    >
    <span>Aktiv klubb</span>
    </label>
    <?php if (!$isNew): ?>
    <p class="text-secondary text-sm mt-md">
     <i data-lucide="users" class="icon-sm"></i>
     <?= $riderCount ?> aktiva medlemmar
    </p>
    <?php endif; ?>
   </div>
   </div>

   <!-- Actions -->
   <div class="card mb-lg">
   <div class="card-body">
    <button type="submit" class="btn btn--primary w-full mb-sm">
    <i data-lucide="save"></i>
    <?= $isNew ? 'Skapa klubb' : 'Spara ändringar' ?>
    </button>
    <?php if (!$isNew): ?>
    <a href="/club/<?= $id ?>" target="_blank" class="btn btn--secondary w-full mb-sm">
    <i data-lucide="eye"></i>
    Visa publik sida
    </a>
    <?php endif; ?>
    <a href="/admin/clubs.php" class="btn btn--secondary w-full">
    <i data-lucide="arrow-left"></i>
    Tillbaka till listan
    </a>
   </div>
   </div>

   <?php if (!$isNew): ?>
   <!-- Danger Zone -->
   <div class="card" style="border-color: var(--color-error);">
   <div class="card-header" style="background: rgba(239, 68, 68, 0.1);">
    <h2 style="color: var(--color-error);">
    <i data-lucide="alert-triangle"></i>
    Fara
    </h2>
   </div>
   <div class="card-body">
    <?php if ($riderCount > 0): ?>
    <p class="text-secondary text-sm mb-md">
     Klubben har <?= $riderCount ?> medlemmar och kan inte tas bort.
    </p>
    <button type="button" class="btn btn-danger w-full" disabled>
     <i data-lucide="trash-2"></i>
     Ta bort klubb
    </button>
    <?php else: ?>
    <p class="text-secondary text-sm mb-md">
     Denna åtgärd kan inte ångras.
    </p>
    <button type="submit" name="action" value="delete" class="btn btn-danger w-full"
     onclick="return confirm('Är du säker på att du vill ta bort denna klubb?')">
     <i data-lucide="trash-2"></i>
     Ta bort klubb
    </button>
    <?php endif; ?>
   </div>
   </div>
   <?php endif; ?>
  </div>
  </div>
 </form>

<?php if (!$isNew && !empty($riders)): ?>
<!-- Club Members -->
<div class="card mt-lg">
    <div class="card-header flex justify-between items-center">
        <h2>
            <i data-lucide="users"></i>
            Medlemmar (<?= $riderCount ?>)
        </h2>
        <a href="/admin/riders.php?club_id=<?= $id ?>" class="btn btn--secondary btn--sm">
            <i data-lucide="external-link"></i>
            Visa alla
        </a>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>Kön</th>
                        <th>Födelseår</th>
                        <th>Status</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($riders as $rider): ?>
                    <tr>
                        <td>
                            <strong><?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></strong>
                        </td>
                        <td><?= $rider['gender'] === 'M' ? 'Man' : ($rider['gender'] === 'F' ? 'Kvinna' : '-') ?></td>
                        <td><?= h($rider['birth_year']) ?: '-' ?></td>
                        <td>
                            <span class="badge <?= $rider['active'] ? 'badge-success' : 'badge-secondary' ?>">
                                <?= $rider['active'] ? 'Aktiv' : 'Inaktiv' ?>
                            </span>
                        </td>
                        <td>
                            <a href="/admin/rider-edit.php?id=<?= $rider['id'] ?>" class="btn btn--secondary btn--sm">
                                <i data-lucide="pencil"></i>
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if ($riderCount > 10): ?>
        <div class="text-center py-md border-t">
            <a href="/admin/riders.php?club_id=<?= $id ?>" class="text-accent">
                Visa alla <?= $riderCount ?> medlemmar
            </a>
        </div>
        <?php endif; ?>
    </div>
</div>
<?php endif; ?>

<style>
@keyframes spin { to { transform: rotate(360deg); } }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const logoInput = document.getElementById('clubLogoInput');
    const logoPreview = document.getElementById('clubLogoPreview');
    const logoLoading = document.getElementById('clubLogoLoading');
    const logoStatus = document.getElementById('clubLogoStatus');
    const urlInput = document.getElementById('logoUrlInput');
    const clubId = <?= intval($id) ?>;

    if (!logoInput || !clubId) return;

    logoInput.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            showStatus('Otillaten filtyp', 'error');
            return;
        }

        if (file.size > 2 * 1024 * 1024) {
            showStatus('Max 2MB', 'error');
            return;
        }

        logoLoading.style.display = 'flex';
        showStatus('Laddar upp...', 'info');

        const formData = new FormData();
        formData.append('logo', file);
        formData.append('club_id', clubId);

        try {
            const response = await fetch('/api/update-club-logo.php', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();

            if (result.success) {
                showStatus('Uppladdad!', 'success');
                updatePreview(result.logo_url);
                urlInput.value = result.logo_url;
            } else {
                showStatus(result.error || 'Fel', 'error');
            }
        } catch (error) {
            showStatus('Uppladdning misslyckades', 'error');
        } finally {
            logoLoading.style.display = 'none';
        }
    });

    function updatePreview(src) {
        logoPreview.innerHTML = '<img src="' + src + '" alt="Klubblogotyp" style="max-width: 100%; max-height: 100%; object-fit: contain;">';
        logoPreview.style.border = 'none';
    }

    function showStatus(msg, type) {
        logoStatus.textContent = msg;
        logoStatus.style.color = type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#6b7280';
        if (type === 'success') setTimeout(() => { logoStatus.textContent = ''; }, 3000);
    }

    // Re-init Lucide icons after page load
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
