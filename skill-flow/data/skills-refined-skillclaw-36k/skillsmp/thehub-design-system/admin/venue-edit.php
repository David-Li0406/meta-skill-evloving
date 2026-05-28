<?php
/**
 * Venue Edit - REDIRECT till Destination Edit
 * Behalles for bakatkompatibilitet
 */
$id = isset($_GET['id']) ? '?id=' . intval($_GET['id']) : '';
header('Location: /admin/destination-edit.php' . $id);
exit;

$db = getDB();

// Get venue ID - 0 or null means creating new venue
$id = isset($_GET['id']) && is_numeric($_GET['id']) ? intval($_GET['id']) : 0;
$isNew = ($id === 0);

// Default values for new venue
$venue = [
    'name' => '',
    'city' => '',
    'region' => '',
    'country' => 'Sverige',
    'address' => '',
    'description' => '',
    'website' => '',
    'logo' => '',
    'email' => '',
    'phone' => '',
    'contact_person' => '',
    'gps_lat' => '',
    'gps_lng' => '',
    'facebook' => '',
    'instagram' => '',
    'trailforks_url' => '',
    'strava_segment' => '',
    'parking_info' => '',
    'facilities' => '',
    'active' => 1
];

// Fetch existing venue data if editing
if (!$isNew) {
    $existingVenue = $db->getRow("SELECT * FROM venues WHERE id = ?", [$id]);

    if (!$existingVenue) {
        $_SESSION['message'] = 'Anläggning hittades inte';
        $_SESSION['messageType'] = 'error';
        header('Location: /admin/venues.php');
        exit;
    }

    $venue = array_merge($venue, $existingVenue);
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
        $eventCount = $db->getRow("SELECT COUNT(*) as cnt FROM events WHERE venue_id = ?", [$id])['cnt'] ?? 0;

        if ($eventCount > 0) {
            $message = "Kan inte ta bort anläggning med $eventCount kopplade events. Flytta eventen först.";
            $messageType = 'error';
        } else {
            try {
                $db->delete('venues', 'id = ?', [$id]);
                header('Location: /admin/venues.php?msg=deleted');
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
            $message = 'Namn på anläggning är obligatoriskt';
            $messageType = 'error';
        } else {
            // Prepare venue data
            $venueData = [
                'name' => $name,
                'city' => trim($_POST['city'] ?? ''),
                'region' => trim($_POST['region'] ?? ''),
                'country' => trim($_POST['country'] ?? 'Sverige'),
                'address' => trim($_POST['address'] ?? ''),
                'description' => trim($_POST['description'] ?? ''),
                'website' => trim($_POST['website'] ?? ''),
                'logo' => trim($_POST['logo'] ?? ''),
                'email' => trim($_POST['email'] ?? ''),
                'phone' => trim($_POST['phone'] ?? ''),
                'contact_person' => trim($_POST['contact_person'] ?? ''),
                'gps_lat' => !empty($_POST['gps_lat']) ? floatval($_POST['gps_lat']) : null,
                'gps_lng' => !empty($_POST['gps_lng']) ? floatval($_POST['gps_lng']) : null,
                'facebook' => trim($_POST['facebook'] ?? ''),
                'instagram' => trim($_POST['instagram'] ?? ''),
                'trailforks_url' => trim($_POST['trailforks_url'] ?? ''),
                'strava_segment' => trim($_POST['strava_segment'] ?? ''),
                'parking_info' => trim($_POST['parking_info'] ?? ''),
                'facilities' => trim($_POST['facilities'] ?? ''),
                'active' => isset($_POST['active']) ? 1 : 0,
            ];

            try {
                if ($isNew) {
                    $db->insert('venues', $venueData);
                    $id = $db->lastInsertId();
                    header('Location: /admin/venue-edit.php?id=' . $id . '&msg=created');
                    exit;
                } else {
                    $db->update('venues', $venueData, 'id = ?', [$id]);
                    $message = 'Anläggning uppdaterad!';
                    $messageType = 'success';

                    // Refresh venue data
                    $venue = $db->getRow("SELECT * FROM venues WHERE id = ?", [$id]);
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
            $message = 'Anläggning skapad!';
            $messageType = 'success';
            break;
    }
}

// Get event count and events for this venue
$eventCount = 0;
$events = [];
if (!$isNew) {
    $eventCount = $db->getRow("SELECT COUNT(*) as count FROM events WHERE venue_id = ?", [$id])['count'] ?? 0;

    // Get recent events
    $events = $db->getAll("
        SELECT id, name, date, series_id
        FROM events
        WHERE venue_id = ?
        ORDER BY date DESC
        LIMIT 10
    ", [$id]);
}

// Page config for admin layout
$page_title = $isNew ? 'Ny Anläggning' : 'Redigera Anläggning';
$breadcrumbs = [
    ['label' => 'Anläggningar', 'url' => '/admin/venues.php'],
    ['label' => $isNew ? 'Ny Anläggning' : h($venue['name'])]
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
    <i data-lucide="mountain"></i>
    Grundläggande information
    </h2>
   </div>
   <div class="card-body">
    <div class="grid grid-cols-1 gap-md">
    <!-- Name -->
    <div>
     <label for="name" class="admin-form-label">
     Namn <span class="text-error">*</span>
     </label>
     <input
     type="text"
     id="name"
     name="name"
     class="admin-form-input"
     required
     value="<?= h($venue['name']) ?>"
     placeholder="T.ex. Järvsö Bergscykelpark"
     >
    </div>

    <!-- City and Region -->
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="city" class="admin-form-label">Stad</label>
     <input
      type="text"
      id="city"
      name="city"
      class="admin-form-input"
      value="<?= h($venue['city'] ?? '') ?>"
      placeholder="T.ex. Järvsö"
     >
     </div>
     <div>
     <label for="region" class="admin-form-label">Region/Län</label>
     <input
      type="text"
      id="region"
      name="region"
      class="admin-form-input"
      value="<?= h($venue['region'] ?? '') ?>"
      placeholder="T.ex. Gävleborg"
     >
     </div>
    </div>

    <!-- Country and Address -->
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="country" class="admin-form-label">Land</label>
     <input
      type="text"
      id="country"
      name="country"
      class="admin-form-input"
      value="<?= h($venue['country'] ?? 'Sverige') ?>"
     >
     </div>
     <div>
     <label for="address" class="admin-form-label">Adress</label>
     <input
      type="text"
      id="address"
      name="address"
      class="admin-form-input"
      value="<?= h($venue['address'] ?? '') ?>"
      placeholder="Gatuadress"
     >
     </div>
    </div>
    </div>
   </div>
   </div>

   <!-- GPS Coordinates -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="map-pin"></i>
    GPS-koordinater
    </h2>
   </div>
   <div class="card-body">
    <p class="text-secondary mb-md">
    Används för att visa anläggningen på kartor och navigering.
    </p>
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="gps_lat" class="admin-form-label">Latitud</label>
     <input
      type="number"
      step="0.0000001"
      id="gps_lat"
      name="gps_lat"
      class="admin-form-input"
      value="<?= h($venue['gps_lat'] ?? '') ?>"
      placeholder="61.7218"
     >
     </div>
     <div>
     <label for="gps_lng" class="admin-form-label">Longitud</label>
     <input
      type="number"
      step="0.0000001"
      id="gps_lng"
      name="gps_lng"
      class="admin-form-input"
      value="<?= h($venue['gps_lng'] ?? '') ?>"
      placeholder="16.1506"
     >
     </div>
    </div>
    <?php if (!empty($venue['gps_lat']) && !empty($venue['gps_lng'])): ?>
    <div class="mt-md">
     <a href="https://www.google.com/maps?q=<?= $venue['gps_lat'] ?>,<?= $venue['gps_lng'] ?>" target="_blank" class="btn btn--secondary btn--sm">
      <i data-lucide="external-link"></i>
      Visa på Google Maps
     </a>
    </div>
    <?php endif; ?>
   </div>
   </div>

   <!-- Description & Logo -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="file-text"></i>
    Beskrivning & Media
    </h2>
   </div>
   <div class="card-body">
    <div class="grid gap-lg">
    <!-- Description -->
    <div>
     <label for="description" class="admin-form-label">Beskrivning</label>
     <textarea
     id="description"
     name="description"
     class="admin-form-input"
     rows="4"
     placeholder="Beskriv anläggningen, banorna, terrängen..."
     ><?= h($venue['description'] ?? '') ?></textarea>
    </div>

    <!-- Logo URL -->
    <div>
     <label for="logo" class="admin-form-label">Logotyp (URL)</label>
     <input
     type="url"
     id="logo"
     name="logo"
     class="admin-form-input"
     value="<?= h($venue['logo'] ?? '') ?>"
     placeholder="https://example.com/logo.png"
     >
     <?php if (!empty($venue['logo'])): ?>
     <div class="mt-sm">
      <img src="<?= h($venue['logo']) ?>" alt="Anläggningslogo" style="max-height: 60px; border-radius: 4px;">
     </div>
     <?php endif; ?>
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
     <label for="contact_person" class="admin-form-label">Kontaktperson</label>
     <input
     type="text"
     id="contact_person"
     name="contact_person"
     class="admin-form-input"
     value="<?= h($venue['contact_person'] ?? '') ?>"
     placeholder="Namn på kontaktperson"
     >
    </div>

    <!-- Email and Phone -->
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="email" class="admin-form-label">E-post</label>
     <input
      type="email"
      id="email"
      name="email"
      class="admin-form-input"
      value="<?= h($venue['email'] ?? '') ?>"
      placeholder="info@anlaggning.se"
     >
     </div>
     <div>
     <label for="phone" class="admin-form-label">Telefon</label>
     <input
      type="tel"
      id="phone"
      name="phone"
      class="admin-form-input"
      value="<?= h($venue['phone'] ?? '') ?>"
      placeholder="070-123 45 67"
     >
     </div>
    </div>

    <!-- Website -->
    <div>
     <label for="website" class="admin-form-label">Webbplats</label>
     <input
     type="url"
     id="website"
     name="website"
     class="admin-form-input"
     value="<?= h($venue['website'] ?? '') ?>"
     placeholder="https://anlaggning.se"
     >
    </div>
    </div>
   </div>
   </div>

   <!-- Links & Social Media -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="link"></i>
    Länkar & Sociala medier
    </h2>
   </div>
   <div class="card-body">
    <div class="grid grid-cols-2 gap-md">
     <div>
     <label for="facebook" class="admin-form-label">
      <i data-lucide="facebook" class="icon-sm"></i>
      Facebook
     </label>
     <input
      type="url"
      id="facebook"
      name="facebook"
      class="admin-form-input"
      value="<?= h($venue['facebook'] ?? '') ?>"
      placeholder="https://facebook.com/..."
     >
     </div>
     <div>
     <label for="instagram" class="admin-form-label">
      <i data-lucide="instagram" class="icon-sm"></i>
      Instagram
     </label>
     <input
      type="url"
      id="instagram"
      name="instagram"
      class="admin-form-input"
      value="<?= h($venue['instagram'] ?? '') ?>"
      placeholder="https://instagram.com/..."
     >
     </div>
     <div>
     <label for="trailforks_url" class="admin-form-label">
      <i data-lucide="map" class="icon-sm"></i>
      Trailforks
     </label>
     <input
      type="url"
      id="trailforks_url"
      name="trailforks_url"
      class="admin-form-input"
      value="<?= h($venue['trailforks_url'] ?? '') ?>"
      placeholder="https://trailforks.com/region/..."
     >
     </div>
     <div>
     <label for="strava_segment" class="admin-form-label">
      <i data-lucide="activity" class="icon-sm"></i>
      Strava Segment
     </label>
     <input
      type="url"
      id="strava_segment"
      name="strava_segment"
      class="admin-form-input"
      value="<?= h($venue['strava_segment'] ?? '') ?>"
      placeholder="https://strava.com/segments/..."
     >
     </div>
    </div>
   </div>
   </div>

   <!-- Facilities -->
   <div class="card mb-lg">
   <div class="card-header">
    <h2 class="text-primary">
    <i data-lucide="info"></i>
    Praktisk information
    </h2>
   </div>
   <div class="card-body">
    <div class="grid gap-md">
     <div>
     <label for="parking_info" class="admin-form-label">Parkering</label>
     <textarea
      id="parking_info"
      name="parking_info"
      class="admin-form-input"
      rows="2"
      placeholder="Information om parkering..."
     ><?= h($venue['parking_info'] ?? '') ?></textarea>
     </div>
     <div>
     <label for="facilities" class="admin-form-label">Faciliteter</label>
     <textarea
      id="facilities"
      name="facilities"
      class="admin-form-input"
      rows="3"
      placeholder="Beskriv faciliteter (omklädningsrum, dusch, café, etc.)..."
     ><?= h($venue['facilities'] ?? '') ?></textarea>
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
     <?= $venue['active'] ? 'checked' : '' ?>
     style="width: 18px; height: 18px; accent-color: var(--color-accent);"
    >
    <span>Aktiv anläggning</span>
    </label>
    <?php if (!$isNew): ?>
    <p class="text-secondary text-sm mt-md">
     <i data-lucide="calendar" class="icon-sm"></i>
     <?= $eventCount ?> kopplade events
    </p>
    <?php endif; ?>
   </div>
   </div>

   <!-- Actions -->
   <div class="card mb-lg">
   <div class="card-body">
    <button type="submit" class="btn btn--primary w-full mb-sm">
    <i data-lucide="save"></i>
    <?= $isNew ? 'Skapa anläggning' : 'Spara ändringar' ?>
    </button>
    <a href="/admin/venues.php" class="btn btn--secondary w-full">
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
    <?php if ($eventCount > 0): ?>
    <p class="text-secondary text-sm mb-md">
     Anläggningen har <?= $eventCount ?> kopplade events och kan inte tas bort.
    </p>
    <button type="button" class="btn btn-danger w-full" disabled>
     <i data-lucide="trash-2"></i>
     Ta bort anläggning
    </button>
    <?php else: ?>
    <p class="text-secondary text-sm mb-md">
     Denna åtgärd kan inte ångras.
    </p>
    <button type="submit" name="action" value="delete" class="btn btn-danger w-full"
     onclick="return confirm('Är du säker på att du vill ta bort denna anläggning?')">
     <i data-lucide="trash-2"></i>
     Ta bort anläggning
    </button>
    <?php endif; ?>
   </div>
   </div>
   <?php endif; ?>
  </div>
  </div>
 </form>

<?php if (!$isNew && !empty($events)): ?>
<!-- Events at this venue -->
<div class="card mt-lg">
    <div class="card-header flex justify-between items-center">
        <h2>
            <i data-lucide="calendar"></i>
            Events på denna anläggning (<?= $eventCount ?>)
        </h2>
        <a href="/admin/events.php?venue_id=<?= $id ?>" class="btn btn--secondary btn--sm">
            <i data-lucide="external-link"></i>
            Visa alla
        </a>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Event</th>
                        <th>Datum</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($events as $event): ?>
                    <tr>
                        <td>
                            <strong><?= h($event['name']) ?></strong>
                        </td>
                        <td><?= $event['date'] ? date('Y-m-d', strtotime($event['date'])) : '-' ?></td>
                        <td>
                            <a href="/admin/event-edit.php?id=<?= $event['id'] ?>" class="btn btn--secondary btn--sm">
                                <i data-lucide="pencil"></i>
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if ($eventCount > 10): ?>
        <div class="text-center py-md border-t">
            <a href="/admin/events.php?venue_id=<?= $id ?>" class="text-accent">
                Visa alla <?= $eventCount ?> events
            </a>
        </div>
        <?php endif; ?>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
