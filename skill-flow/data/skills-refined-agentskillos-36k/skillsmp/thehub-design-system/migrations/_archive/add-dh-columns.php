<?php
/**
 * STANDALONE Migration for DH Support
 * Adds event_format and DH columns
 */

// Load config and require admin authentication
require_once __DIR__ . '/../config.php';
require_admin();

error_reporting(E_ALL);
ini_set('display_errors', 0); // Don't display errors in production

$pdo = null;
try {
 $pdo = new PDO(
 "mysql:host=" . DB_HOST .";dbname=" . DB_NAME .";charset=utf8mb4",
 DB_USER,
 DB_PASS,
 [
  PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
  PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
 ]
 );
} catch (PDOException $e) {
 die("Database connection failed:" . $e->getMessage());
}

$success = [];
$errors = [];

// Migration steps for Events table
$eventsMigrations = [
"ALTER TABLE events ADD COLUMN event_format VARCHAR(20) DEFAULT 'ENDURO' AFTER discipline" =>"Add event_format column to events",
];

// Migration steps for Results table
$resultsMigrations = [
"ALTER TABLE results ADD COLUMN run_1_time TIME NULL AFTER finish_time" =>"Add run_1_time for DH first run",
"ALTER TABLE results ADD COLUMN run_2_time TIME NULL AFTER run_1_time" =>"Add run_2_time for DH second run",
"ALTER TABLE results ADD COLUMN run_1_points INT DEFAULT 0 AFTER points" =>"Add run_1_points for DH first run points",
"ALTER TABLE results ADD COLUMN run_2_points INT DEFAULT 0 AFTER run_1_points" =>"Add run_2_points for DH second run points",
];

// Migration steps for Point Scale Values table (dual points for SweCUP DH)
$pointScaleValuesMigrations = [
"ALTER TABLE point_scale_values ADD COLUMN run_1_points DECIMAL(10,2) DEFAULT 0 AFTER points" =>"Add run_1_points for SweCUP DH Kval",
"ALTER TABLE point_scale_values ADD COLUMN run_2_points DECIMAL(10,2) DEFAULT 0 AFTER run_1_points" =>"Add run_2_points for SweCUP DH Final",
];

// Run events migrations
foreach ($eventsMigrations as $sql => $description) {
 try {
 $pdo->exec($sql);
 $success[] = $description;
 } catch (PDOException $e) {
 if ($e->getCode() == '42S21' || strpos($e->getMessage(), 'Duplicate column') !== false) {
  $success[] = $description ." (redan finns)";
 } else {
  $errors[] = $description .":" . $e->getMessage();
 }
 }
}

// Run results migrations
foreach ($resultsMigrations as $sql => $description) {
 try {
 $pdo->exec($sql);
 $success[] = $description;
 } catch (PDOException $e) {
 if ($e->getCode() == '42S21' || strpos($e->getMessage(), 'Duplicate column') !== false) {
  $success[] = $description ." (redan finns)";
 } else {
  $errors[] = $description .":" . $e->getMessage();
 }
 }
}

// Run point scale values migrations
foreach ($pointScaleValuesMigrations as $sql => $description) {
 try {
 $pdo->exec($sql);
 $success[] = $description;
 } catch (PDOException $e) {
 if ($e->getCode() == '42S21' || strpos($e->getMessage(), 'Duplicate column') !== false) {
  $success[] = $description ." (redan finns)";
 } else {
  $errors[] = $description .":" . $e->getMessage();
 }
 }
}

// Add indexes
$indexes = [
"CREATE INDEX idx_event_format ON events(event_format)" =>"Add event_format index",
];

foreach ($indexes as $sql => $description) {
 try {
 $pdo->exec($sql);
 $success[] = $description;
 } catch (PDOException $e) {
 if ($e->getCode() == '42000' || strpos($e->getMessage(), 'Duplicate key') !== false || strpos($e->getMessage(), 'already exists') !== false) {
  $success[] = $description ." (redan finns)";
 } else {
  $errors[] = $description .":" . $e->getMessage();
 }
 }
}

// Verify columns exist
$verifyQueries = [
"SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'events' AND COLUMN_NAME = 'event_format'" =>"Verify event_format exists",
"SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'results' AND COLUMN_NAME = 'run_1_time'" =>"Verify run_1_time exists",
"SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'results' AND COLUMN_NAME = 'run_2_time'" =>"Verify run_2_time exists",
"SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'results' AND COLUMN_NAME = 'run_1_points'" =>"Verify run_1_points exists",
"SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'results' AND COLUMN_NAME = 'run_2_points'" =>"Verify run_2_points exists",
"SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'point_scale_values' AND COLUMN_NAME = 'run_1_points'" =>"Verify point_scale_values.run_1_points exists",
"SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'point_scale_values' AND COLUMN_NAME = 'run_2_points'" =>"Verify point_scale_values.run_2_points exists",
];

$verified = [];
foreach ($verifyQueries as $sql => $description) {
 try {
 $result = $pdo->query($sql)->fetch();
 if ($result['count'] > 0) {
  $verified[] = $description ." ✅";
 } else {
  $verified[] = $description ." ❌";
 }
 } catch (PDOException $e) {
 $verified[] = $description ." - Error:" . $e->getMessage();
 }
}
?>
<!DOCTYPE html>
<html lang="sv">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>DH Migration Results</title>
 <style>
 * { margin: 0; padding: 0; box-sizing: border-box; }
 body {
  font-family: -apple-system, BlinkMacSystemFont,"Segoe UI", Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 40px 20px;
 }
 .container {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  overflow: hidden;
 }
 .header {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  color: white;
  padding: 30px;
  text-align: center;
 }
 .header h1 {
  font-size: 28px;
  margin-bottom: 10px;
 }
 .header p {
  opacity: 0.9;
  font-size: 14px;
 }
 .content {
  padding: 30px;
 }
 .section {
  margin-bottom: 30px;
 }
 .section h2 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #2d3748;
 }
 .success-box {
  background: #d1fae5;
  border-left: 4px solid #10b981;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 20px;
 }
 .error-box {
  background: #fee;
  border-left: 4px solid #ef4444;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 20px;
 }
 .verify-box {
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 20px;
 }
 .item {
  padding: 10px;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
 }
 .item:last-child {
  border-bottom: none;
 }
 .stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
 }
 .stat {
  background: #f3f4f6;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
 }
 .stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
 }
 .stat-label {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  margin-top: 5px;
 }
 .btn {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 12px 24px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
  margin: 5px;
 }
 .btn:hover {
  background: #5568d3;
 }
 .btn-success {
  background: #10b981;
 }
 .btn-success:hover {
  background: #059669;
 }
 .footer {
  background: #f9fafb;
  padding: 20px 30px;
  text-align: center;
  font-size: 14px;
  color: #6b7280;
 }
 .alert {
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
 }
 .alert-success {
  background: #d1fae5;
  border: 1px solid #10b981;
  color: #065f46;
 }
 .alert-error {
  background: #fee;
  border: 1px solid #ef4444;
  color: #991b1b;
 }

 /* Mobile Responsive */
 @media (max-width: 640px) {
  body {
  padding: 20px 10px;
  }

  .container {
  border-radius: 8px;
  }

  .header {
  padding: 20px 15px;
  }

  .header h1 {
  font-size: 22px;
  }

  .header p {
  font-size: 13px;
  }

  .content {
  padding: 20px 15px;
  }

  .section h2 {
  font-size: 16px;
  }

  .stats {
  grid-template-columns: 1fr;
  gap: 10px;
  }

  .stat {
  padding: 15px;
  }

  .stat-number {
  font-size: 24px;
  }

  .stat-label {
  font-size: 11px;
  }

  .item {
  padding: 8px;
  font-size: 13px;
  }

  .btn {
  padding: 10px 20px;
  font-size: 14px;
  }
 }

 @media (min-width: 641px) and (max-width: 768px) {
  .stats {
  grid-template-columns: repeat(2, 1fr);
  }
 }
 </style>
</head>
<body>
 <div class="container">
 <div class="header">
  <h1>🏔️ DH Support Migration</h1>
  <p>Lägger till event_format och DH-specifika kolumner</p>
 </div>

 <div class="content">
  <div class="stats">
  <div class="stat">
   <div class="stat-number"><?= count($success) ?></div>
   <div class="stat-label">Lyckade</div>
  </div>
  <div class="stat">
   <div class="stat-number"><?= count($errors) ?></div>
   <div class="stat-label">Fel</div>
  </div>
  <div class="stat">
   <div class="stat-number"><?= count($eventsMigrations) + count($resultsMigrations) + count($pointScaleValuesMigrations) ?></div>
   <div class="stat-label">Totalt steg</div>
  </div>
  </div>

  <?php if (!empty($success)): ?>
  <div class="section">
   <h2>✅ Lyckade operationer</h2>
   <div class="success-box">
   <?php foreach ($success as $item): ?>
    <div class="item">✓ <?= htmlspecialchars($item) ?></div>
   <?php endforeach; ?>
   </div>
  </div>
  <?php endif; ?>

  <?php if (!empty($errors)): ?>
  <div class="section">
   <h2>❌ Fel</h2>
   <div class="error-box">
   <?php foreach ($errors as $error): ?>
    <div class="item">✗ <?= htmlspecialchars($error) ?></div>
   <?php endforeach; ?>
   </div>
  </div>
  <?php endif; ?>

  <?php if (!empty($verified)): ?>
  <div class="section">
   <h2>🔍 Verifiering av kolumner</h2>
   <div class="verify-box">
   <?php foreach ($verified as $item): ?>
    <div class="item"><?= htmlspecialchars($item) ?></div>
   <?php endforeach; ?>
   </div>
  </div>
  <?php endif; ?>

  <?php if (count($errors) === 0): ?>
  <div class="alert alert-success">
   <strong>🎉 Migration klar!</strong><br>
   Alla DH-kolumner har lagts till. Du kan nu skapa events med DH-format och importera DH-resultat.
  </div>
  <div class="gs-center-p20">
   <a href="/admin/events.php" class="btn btn-success">
   Gå till Events
   </a>
   <a href="/admin/event-create.php" class="btn">
   Skapa nytt event
   </a>
  </div>
  <?php else: ?>
  <div class="alert alert-error">
   <strong>⚠️ Migration avslutades med fel</strong><br>
   Kontrollera felen ovan. Några kolumner kan ha lagts till men andra misslyckades.
  </div>
  <?php endif; ?>
 </div>

 <div class="footer">
  Migration kördes <?= date('Y-m-d H:i:s') ?>
 </div>
 </div>
</body>
</html>
