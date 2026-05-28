<?php
/**
 * Admin - Upload Icons/Images
 * Allows uploading images to /uploads/icons/
 */
require_once __DIR__ . '/../config.php';
require_admin();

$uploadDir = __DIR__ . '/../uploads/icons/';
$allowedTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/svg+xml', 'image/webp', 'image/x-icon'];
$allowedExtensions = ['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'ico'];
$maxFileSize = 5 * 1024 * 1024; // 5 MB

$message = '';
$messageType = '';

// Handle file upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['icon'])) {
 $file = $_FILES['icon'];

 if ($file['error'] === UPLOAD_ERR_OK) {
 $fileName = basename($file['name']);
 $fileExt = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));
 $fileType = mime_content_type($file['tmp_name']);

 // Custom filename if provided
 if (!empty($_POST['custom_name'])) {
  $customName = preg_replace('/[^a-zA-Z0-9_-]/', '', $_POST['custom_name']);
  if ($customName) {
  $fileName = $customName . '.' . $fileExt;
  }
 }

 // Validate file
 if (!in_array($fileExt, $allowedExtensions)) {
  $message ="Ogiltigt filformat. Tillåtna format:" . implode(', ', $allowedExtensions);
  $messageType = 'error';
 } elseif (!in_array($fileType, $allowedTypes) && $fileType !== 'image/vnd.microsoft.icon') {
  $message ="Ogiltigt filtyp: $fileType";
  $messageType = 'error';
 } elseif ($file['size'] > $maxFileSize) {
  $message ="Filen är för stor. Max storlek: 5 MB";
  $messageType = 'error';
 } else {
  $targetPath = $uploadDir . $fileName;

  // Check if overwriting
  $overwrite = isset($_POST['overwrite']) && $_POST['overwrite'] === '1';
  if (file_exists($targetPath) && !$overwrite) {
  $message ="Filen '$fileName' finns redan. Markera 'Ersätt befintlig fil' för att skriva över.";
  $messageType = 'warning';
  } elseif (move_uploaded_file($file['tmp_name'], $targetPath)) {
  $message ="Filen '$fileName' har laddats upp!";
  $messageType = 'success';
  } else {
  $message ="Kunde inte ladda upp filen. Kontrollera mappens skrivbehörigheter.";
  $messageType = 'error';
  }
 }
 } else {
 $uploadErrors = [
  UPLOAD_ERR_INI_SIZE => 'Filen överskrider max storlek (php.ini)',
  UPLOAD_ERR_FORM_SIZE => 'Filen överskrider max storlek (formulär)',
  UPLOAD_ERR_PARTIAL => 'Filen laddades bara delvis upp',
  UPLOAD_ERR_NO_FILE => 'Ingen fil valdes',
  UPLOAD_ERR_NO_TMP_DIR => 'Temporär mapp saknas',
  UPLOAD_ERR_CANT_WRITE => 'Kunde inte skriva filen',
 ];
 $message = $uploadErrors[$file['error']] ?? 'Okänt fel vid uppladdning';
 $messageType = 'error';
 }
}

// Handle file deletion
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete_file'])) {
 $deleteFile = basename($_POST['delete_file']);
 $deletePath = $uploadDir . $deleteFile;

 if (file_exists($deletePath) && is_file($deletePath)) {
 if (unlink($deletePath)) {
  $message ="Filen '$deleteFile' har tagits bort.";
  $messageType = 'success';
 } else {
  $message ="Kunde inte ta bort filen.";
  $messageType = 'error';
 }
 }
}

// Get existing files
$existingFiles = [];
if (is_dir($uploadDir)) {
 $files = scandir($uploadDir);
 foreach ($files as $file) {
 if ($file !== '.' && $file !== '..' && $file !== '.htaccess') {
  $filePath = $uploadDir . $file;
  if (is_file($filePath)) {
  $existingFiles[] = [
   'name' => $file,
   'size' => filesize($filePath),
   'modified' => filemtime($filePath),
   'url' => '/uploads/icons/' . $file
  ];
  }
 }
 }
 // Sort by name
 usort($existingFiles, fn($a, $b) => strcasecmp($a['name'], $b['name']));
}

$pageTitle = 'Ladda upp ikoner';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <h1 class="mb-lg">
  <i data-lucide="image"></i>
  Ladda upp ikoner
 </h1>

 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-lg">
  <?= htmlspecialchars($message) ?>
 </div>
 <?php endif; ?>

 <!-- Upload Form -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="">Ladda upp ny bild</h2>
  </div>
  <div class="card-body">
  <form method="post" enctype="multipart/form-data">
   <div class="form-group">
   <label class="label" for="icon">Välj bild</label>
   <input type="file" name="icon" id="icon" accept=".png,.jpg,.jpeg,.gif,.svg,.webp,.ico" class="input" required>
   <small class="text-muted">Tillåtna format: PNG, JPG, GIF, SVG, WebP, ICO. Max 5 MB.</small>
   </div>

   <div class="form-group">
   <label class="label" for="custom_name">Anpassat filnamn (valfritt)</label>
   <input type="text" name="custom_name" id="custom_name" class="input" placeholder="t.ex. logo-512">
   <small class="text-muted">Lämna tomt för att använda originalnamnet. Endast bokstäver, siffror, bindestreck och understreck.</small>
   </div>

   <div class="form-group">
   <label class="checkbox">
    <input type="checkbox" name="overwrite" value="1">
    <span>Ersätt befintlig fil om den finns</span>
   </label>
   </div>

   <button type="submit" class="btn btn--primary">
   <i data-lucide="upload"></i>
   Ladda upp
   </button>
  </form>
  </div>
 </div>

 <!-- Existing Files -->
 <div class="card">
  <div class="card-header">
  <h2 class="">Uppladdade filer (<?= count($existingFiles) ?>)</h2>
  </div>
  <div class="card-body">
  <?php if (empty($existingFiles)): ?>
   <p class="text-muted">Inga filer uppladdade ännu.</p>
  <?php else: ?>
   <div class="table-responsive">
   <table class="table">
    <thead>
    <tr>
     <th style="width: 80px;">Förhandsgr.</th>
     <th>Filnamn</th>
     <th>Storlek</th>
     <th>URL</th>
     <th style="width: 100px;">Åtgärder</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach ($existingFiles as $file): ?>
    <tr>
     <td>
     <img src="<?= htmlspecialchars($file['url']) ?>" alt=""
      style="max-width: 60px; max-height: 60px; object-fit: contain; background: #f0f0f0; border-radius: 4px;">
     </td>
     <td>
     <strong><?= htmlspecialchars($file['name']) ?></strong>
     </td>
     <td>
     <?php
     $size = $file['size'];
     if ($size >= 1048576) {
      echo number_format($size / 1048576, 2) . ' MB';
     } elseif ($size >= 1024) {
      echo number_format($size / 1024, 1) . ' KB';
     } else {
      echo $size . ' B';
     }
     ?>
     </td>
     <td>
     <code class="gs-code" style="font-size: 12px;"><?= htmlspecialchars($file['url']) ?></code>
     <button type="button" class="btn btn--sm btn-ghost" onclick="navigator.clipboard.writeText('<?= htmlspecialchars($file['url']) ?>')" title="Kopiera URL">
      <i data-lucide="copy" style="width: 14px; height: 14px;"></i>
     </button>
     </td>
     <td>
     <form method="post" style="display: inline;" onsubmit="return confirm('Vill du verkligen ta bort denna fil?')">
      <input type="hidden" name="delete_file" value="<?= htmlspecialchars($file['name']) ?>">
      <button type="submit" class="btn btn--sm btn-danger">
      <i data-lucide="trash-2" style="width: 14px; height: 14px;"></i>
      </button>
     </form>
     </td>
    </tr>
    <?php endforeach; ?>
    </tbody>
   </table>
   </div>
  <?php endif; ?>
  </div>
 </div>

 <!-- PWA Icons Info -->
 <div class="card mt-lg">
  <div class="card-header">
  <h2 class="">PWA Ikoner (V3)</h2>
  </div>
  <div class="card-body">
  <p class="text-muted mb-md">
   V3 PWA-ikoner finns i <code>/v3/assets/icons/</code>. Om du vill ersätta dem, ladda upp nya ikoner här och kopiera sedan filerna manuellt, eller kontakta administratören.
  </p>
  <p class="text-muted">
   Rekommenderade storlekar för PWA-ikoner:
  </p>
  <ul class="text-muted" style="margin-left: 20px;">
   <li><strong>icon-192.png</strong> - 192x192 px</li>
   <li><strong>icon-512.png</strong> - 512x512 px</li>
   <li><strong>icon-maskable-192.png</strong> - 192x192 px (med säkert område)</li>
   <li><strong>icon-maskable-512.png</strong> - 512x512 px (med säkert område)</li>
  </ul>
  </div>
 </div>

 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
