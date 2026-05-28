<?php
require_once __DIR__ . '/config.php';

$db = getDB();

// Get rider ID from URL
$riderId = isset($_GET['id']) ? (int)$_GET['id'] : 0;

if (!$riderId) {
 header('Location: /riders.php');
 exit;
}

// Fetch rider details with class information
$rider = $db->getRow("
 SELECT
 r.*,
 c.name as club_name,
 c.logo as club_logo
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE r.id = ?
", [$riderId]);

if (!$rider) {
 header('Location: /riders.php');
 exit;
}

// Calculate age and determine current class
$currentYear = date('Y');
$age = $currentYear - ($rider['birth_year'] ?? 0);
$currentClass = null;
$currentClassName = null;

if ($rider['birth_year'] && $rider['gender']) {
 require_once __DIR__ . '/includes/class-calculations.php';
 $classId = determineRiderClass($db, $rider['birth_year'], $rider['gender'], date('Y-m-d'));
 if ($classId) {
 $class = $db->getRow("SELECT name, display_name FROM classes WHERE id = ?", [$classId]);
 $currentClass = $class['name'];
 $currentClassName = $class['display_name'];
 }
}

$pageTitle = 'Licens - ' . $rider['firstname'] . ' ' . $rider['lastname'];
$pageType = 'public';
?>
<!DOCTYPE html>
<html lang="sv">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title><?= h($pageTitle) ?></title>
 <style>
 * {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
 }

 body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
 }

 .license-card-container {
  perspective: 1000px;
 }

 .license-card {
  width: 856px;
  height: 540px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  transform-style: preserve-3d;
  transition: transform 0.6s;
 }

 .license-card:hover {
  transform: rotateY(5deg) rotateX(2deg);
 }

 /* UCI Stripe */
 .uci-stripe {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 8px;
  background: linear-gradient(90deg,
  #E31E24 0% 20%,
  #000000 20% 40%,
  #FFD700 40% 60%,
  #0066CC 60% 80%,
  #009B3A 80% 100%
  );
 }

 /* Header */
 .license-header {
  padding: 30px 40px;
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  color: white;
  position: relative;
 }

 .license-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
 }

 .license-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
 }

 .license-season {
  font-size: 20px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 20px;
  border-radius: 30px;
 }

 /* Main Content */
 .license-content {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 40px;
  padding: 40px;
 }

 /* Photo Section */
 .license-photo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
 }

 .photo-frame {
  width: 180px;
  height: 240px;
  background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
 }

 .photo-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
 }

 .photo-placeholder {
  font-size: 64px;
  color: #999;
 }

 .qr-code {
  width: 120px;
  height: 120px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #999;
  text-align: center;
  padding: 10px;
 }

 /* Info Section */
 .license-info {
  display: flex;
  flex-direction: column;
  gap: 25px;
 }

 .rider-name {
  font-size: 42px;
  font-weight: 800;
  color: #1a202c;
  line-height: 1.2;
  text-transform: uppercase;
  letter-spacing: -0.5px;
 }

 .info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
 }

 .info-field {
  background: white;
  padding: 15px 20px;
  border-radius: 10px;
  border-left: 4px solid #667eea;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
 }

 .info-label {
  font-size: 11px;
  color: #718096;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
 }

 .info-value {
  font-size: 20px;
  color: #1a202c;
  font-weight: 700;
 }

 /* Class Badge */
 .class-badge {
  grid-column: span 2;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 30px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
 }

 .class-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
 }

 .class-label {
  font-size: 12px;
  opacity: 0.9;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
 }

 .class-name {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -0.5px;
 }

 .class-code {
  background: rgba(255, 255, 255, 0.25);
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 2px;
 }

 /* Footer */
 .license-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 15px 40px;
  background: rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: #718096;
 }

 .club-logo {
  height: 30px;
  width: auto;
 }

 /* Print Styles */
 @media print {
  body {
  background: white;
  padding: 0;
  }

  .license-card {
  box-shadow: none;
  border: 1px solid #e0e0e0;
  }

  .license-card:hover {
  transform: none;
  }
 }

 /* Back Button */
 .back-button {
  position: fixed;
  top: 20px;
  left: 20px;
  background: white;
  color: #667eea;
  padding: 12px 24px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
 }

 .back-button:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
 }

 @media print {
  .back-button {
  display: none;
  }
 }

 /* Mobile Responsive */
 @media (max-width: 900px) {
  body {
  padding: 1rem;
  }

  .license-card {
  width: 100%;
  max-width: 100%;
  height: auto;
  min-height: auto;
  }

  .license-card:hover {
  transform: none;
  }

  .license-header {
  padding: 20px;
  }

  .license-title {
  font-size: 20px;
  }

  .license-season {
  font-size: 16px;
  padding: 6px 16px;
  }

  .license-content {
  grid-template-columns: 1fr;
  gap: 25px;
  padding: 25px 20px;
  }

  .license-photo {
  flex-direction: row;
  justify-content: center;
  gap: 15px;
  }

  .photo-frame {
  width: 120px;
  height: 160px;
  }

  .qr-code {
  width: 100px;
  height: 100px;
  font-size: 9px;
  }

  .rider-name {
  font-size: 28px;
  text-align: center;
  }

  .info-grid {
  grid-template-columns: 1fr;
  gap: 12px;
  }

  .info-field {
  padding: 12px 16px;
  }

  .info-label {
  font-size: 10px;
  }

  .info-value {
  font-size: 16px;
  }

  .class-badge {
  flex-direction: column;
  padding: 16px 20px;
  gap: 12px;
  text-align: center;
  }

  .class-label {
  font-size: 11px;
  }

  .class-name {
  font-size: 24px;
  }

  .class-code {
  padding: 10px 20px;
  font-size: 20px;
  }

  .license-footer {
  padding: 12px 20px;
  font-size: 10px;
  flex-direction: column;
  gap: 8px;
  text-align: center;
  }

  .back-button {
  top: 10px;
  left: 10px;
  padding: 10px 20px;
  font-size: 14px;
  }
 }

 @media (max-width: 480px) {
  body {
  padding: 0.5rem;
  }

  .license-header {
  padding: 15px;
  }

  .license-title {
  font-size: 18px;
  }

  .license-season {
  font-size: 14px;
  padding: 5px 12px;
  }

  .license-content {
  padding: 20px 15px;
  gap: 20px;
  }

  .license-photo {
  flex-direction: column;
  align-items: center;
  }

  .photo-frame {
  width: 100px;
  height: 133px;
  }

  .qr-code {
  width: 80px;
  height: 80px;
  font-size: 8px;
  }

  .rider-name {
  font-size: 24px;
  }

  .info-value {
  font-size: 14px;
  }

  .class-name {
  font-size: 20px;
  }

  .class-code {
  font-size: 18px;
  }
 }
 </style>
</head>
<body>
 <a href="/rider.php?id=<?= $riderId ?>" class="back-button">
 ← Tillbaka till profil
 </a>

 <div class="license-card-container">
 <div class="license-card">
  <!-- UCI Color Stripe -->
  <div class="uci-stripe"></div>

  <!-- Header -->
  <div class="license-header">
  <div class="license-header-content">
   <div class="license-title">Cycling License</div>
   <div class="license-season"><?= $currentYear ?></div>
  </div>
  </div>

  <!-- Main Content -->
  <div class="license-content">
  <!-- Photo & QR Section -->
  <div class="license-photo">
   <div class="photo-frame">
   <?php if (!empty($rider['photo'])): ?>
    <img src="<?= h($rider['photo']) ?>" alt="<?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>">
   <?php else: ?>
    <div class="photo-placeholder">👤</div>
   <?php endif; ?>
   </div>
   <div class="qr-code">
   QR-kod<br>
   <?= h($rider['license_number'] ??'ID: ' . $riderId) ?>
   </div>
  </div>

  <!-- Info Section -->
  <div class="license-info">
   <div class="rider-name">
   <?= h($rider['firstname']) ?><br>
   <?= h($rider['lastname']) ?>
   </div>

   <div class="info-grid">
   <div class="info-field">
    <div class="info-label">Födelsedatum</div>
    <div class="info-value">
    <?= $rider['birth_year'] ? $rider['birth_year'] . '-XX-XX' : '–' ?>
    </div>
   </div>

   <div class="info-field">
    <div class="info-label">Ålder</div>
    <div class="info-value">
    <?= $age ?> år
    </div>
   </div>

   <div class="info-field">
    <div class="info-label">Kön</div>
    <div class="info-value">
    <?= $rider['gender'] === 'M' ? 'Man' : ($rider['gender'] === 'K' ? 'Kvinna' : '–') ?>
    </div>
   </div>

   <div class="info-field">
    <div class="info-label">Licens #</div>
    <div class="info-value">
    <?= h($rider['license_number']) ?: sprintf('#%04d', $riderId) ?>
    </div>
   </div>

   <?php if ($rider['club_name']): ?>
    <div class="info-field gs-col-span-2">
    <div class="info-label">Klubb</div>
    <div class="info-value"><?= h($rider['club_name']) ?></div>
    </div>
   <?php endif; ?>

   <?php if ($currentClass): ?>
    <div class="class-badge">
    <div class="class-info">
     <div class="class-label">Tävlingsklass <?= $currentYear ?></div>
     <div class="class-name"><?= h($currentClassName) ?></div>
    </div>
    <div class="class-code"><?= h($currentClass) ?></div>
    </div>
   <?php endif; ?>
   </div>
  </div>
  </div>

  <!-- Footer -->
  <div class="license-footer">
  <div>
   <?php if ($rider['club_logo']): ?>
   <img src="<?= h($rider['club_logo']) ?>" alt="<?= h($rider['club_name']) ?>" class="club-logo">
   <?php else: ?>
   TheHUB Cycling Management
   <?php endif; ?>
  </div>
  <div>
   Giltig: <?= $currentYear ?>-01-01 till <?= $currentYear ?>-12-31
  </div>
  </div>
 </div>
 </div>

 <script src="https://unpkg.com/lucide@latest"></script>
 <script>lucide.createIcons();</script>
</body>
</html>
