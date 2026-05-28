<?php
/**
 * TEST: normalizeRiderName funktion
 */
require_once __DIR__ . '/../config.php';
require_admin();

// ============================================
// NAMN-NORMALISERING FUNKTION
// ============================================
function normalizeRiderName($name) {
  if (!$name) return '';
  
  $name = trim(strtoupper($name));
  
  $swedishEndings = [
    'SSON', 'SEN', 'MANN', 'BERG', 'GREN', 'LUND', 'STROM', 'STRÖM',
    'HALL', 'DAHL', 'HOLM', 'NORÉN', 'NOREN', 'ÅBERG', 'ABERG',
    'QUIST', 'HUND', 'LING', 'BLAD', 'VALL', 'MARK', 'BERG',
    'STRAND', 'QVIST', 'STAD', 'TORP', 'HULT', 'FORS'
  ];
  
  $parts = preg_split('/\s+/', $name);
  
  if (count($parts) > 1) {
    $lastName = end($parts);
    
    foreach ($swedishEndings as $ending) {
      if (str_ends_with($lastName, $ending)) {
        array_pop($parts);
        break;
      }
    }
  }
  
  $normalized = implode(' ', $parts);
  $normalized = str_replace('-', ' ', $normalized);
  $normalized = preg_replace('/\s+/', ' ', $normalized);
  
  return trim($normalized);
}

// Test-data
$tests = [
  'ANDERS JONSSON',
  'ANDERS',
  'ANDERS BERTIL JONSSON',
  'ANDERS BERTIL',
  'JOHAN ANDERSSON',
  'JOHAN',
  'MARIA HANSEN',
  'MARIA',
  'PER-ERIK LUNDGREN',
  'PER-ERIK',
];

?>
<!DOCTYPE html>
<html>
<head>
    <title>Test normalizeRiderName</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
        .match { background-color: #90EE90; }
    </style>
</head>
<body>
    <h1>Test: normalizeRiderName funktion</h1>
    
    <h2>Individuella test</h2>
    <table>
        <tr>
            <th>Original namn</th>
            <th>Normaliserat</th>
        </tr>
        <?php foreach ($tests as $name): ?>
            <tr>
                <td><strong><?= h($name) ?></strong></td>
                <td><code><?= h(normalizeRiderName($name)) ?></code></td>
            </tr>
        <?php endforeach; ?>
    </table>
    
    <h2>Jämförelse-test (samma person?)</h2>
    <table>
        <tr>
            <th>Namn 1</th>
            <th>Norm 1</th>
            <th>Namn 2</th>
            <th>Norm 2</th>
            <th>Matchar?</th>
        </tr>
        <tr>
            <td>ANDERS JONSSON</td>
            <td><code><?= normalizeRiderName('ANDERS JONSSON') ?></code></td>
            <td>ANDERS</td>
            <td><code><?= normalizeRiderName('ANDERS') ?></code></td>
            <td class="<?= normalizeRiderName('ANDERS JONSSON') === normalizeRiderName('ANDERS') ? 'match' : '' ?>">
                <?= normalizeRiderName('ANDERS JONSSON') === normalizeRiderName('ANDERS') ? '✓ JA' : '✗ NEJ' ?>
            </td>
        </tr>
        <tr>
            <td>ANDERS BERTIL JONSSON</td>
            <td><code><?= normalizeRiderName('ANDERS BERTIL JONSSON') ?></code></td>
            <td>ANDERS BERTIL</td>
            <td><code><?= normalizeRiderName('ANDERS BERTIL') ?></code></td>
            <td class="<?= normalizeRiderName('ANDERS BERTIL JONSSON') === normalizeRiderName('ANDERS BERTIL') ? 'match' : '' ?>">
                <?= normalizeRiderName('ANDERS BERTIL JONSSON') === normalizeRiderName('ANDERS BERTIL') ? '✓ JA' : '✗ NEJ' ?>
            </td>
        </tr>
    </table>
    
    <h2>Database test</h2>
    <?php
    try {
        $db = getDB();
        
        // Hämta några riders
        $riders = $db->getAll("
            SELECT id, firstname, lastname
            FROM riders
            LIMIT 10
        ");
        
        echo '<p>Hittade ' . count($riders) . ' riders i databas</p>';
        echo '<table>';
        echo '<tr><th>ID</th><th>Namn (original)</th><th>Namn (normaliserat)</th></tr>';
        
        foreach ($riders as $rider) {
            $fullName = $rider['firstname'] . ' ' . $rider['lastname'];
            $normalized = normalizeRiderName($fullName);
            echo '<tr>';
            echo '<td>' . $rider['id'] . '</td>';
            echo '<td>' . h($fullName) . '</td>';
            echo '<td><code>' . h($normalized) . '</code></td>';
            echo '</tr>';
        }
        
        echo '</table>';
        
    } catch (Exception $e) {
        echo '<p style="color: red;"><strong>Databas-fel:</strong> ' . h($e->getMessage()) . '</p>';
        echo '<pre>' . h($e->getTraceAsString()) . '</pre>';
    }
    ?>
    
</body>
</html>
