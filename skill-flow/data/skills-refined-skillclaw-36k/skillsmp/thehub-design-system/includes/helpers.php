<?php
// Core functions only

function h($str) {
  return htmlspecialchars($str ?? '', ENT_QUOTES, 'UTF-8');
}

/**
 * Normalize UCI-ID to standard format: XXX XXX XXX XX
 * Example:"10108943209" or"101-089-432-09" becomes"101 089 432 09"
 */
function normalizeUciId($uciId) {
  if (empty($uciId)) return '';

  // Strip all non-digits
  $digits = preg_replace('/[^0-9]/', '', $uciId);

  // If we have 11 digits, format as XXX XXX XXX XX
  if (strlen($digits) === 11) {
    return substr($digits, 0, 3) . ' ' .
        substr($digits, 3, 3) . ' ' .
        substr($digits, 6, 3) . ' ' .
        substr($digits, 9, 2);
  }

  // Otherwise return cleaned version (just digits)
  return $digits;
}

/**
 * Safe output for JavaScript contexts
 * Use this instead of addslashes() for JavaScript strings
 */
function js($str) {
  return json_encode($str ?? '', JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP);
}

function redirect($url) {
  if (strpos($url, '/') !== 0) {
    $url = '/' . $url;
  }
  header("Location:" . $url);
  exit;
}

function calculateAge($birthYear) {
  if (empty($birthYear)) return null;
  return date('Y') - $birthYear;
}

/**
 * Get branding settings from branding.json
 * @param string|null $key Optional specific key to return (e.g., 'logos.sidebar')
 * @return mixed Full branding array or specific value
 */
function getBranding($key = null) {
    static $branding = null;

    if ($branding === null) {
        $brandingFile = __DIR__ . '/../uploads/branding.json';
        if (file_exists($brandingFile)) {
            $data = json_decode(file_get_contents($brandingFile), true);
            $branding = is_array($data) ? $data : [];
        } else {
            $branding = [];
        }
    }

    if ($key === null) {
        return $branding;
    }

    // Support dot notation like 'logos.sidebar'
    $keys = explode('.', $key);
    $value = $branding;
    foreach ($keys as $k) {
        if (!isset($value[$k])) {
            return null;
        }
        $value = $value[$k];
    }
    return $value;
}

/**
 * Generate inline CSS from branding.json that overrides theme.css defaults
 * This is the BRIDGE between branding.json and the visual theme
 */
function generateBrandingCSS() {
    $branding = getBranding();

    // If no custom branding, return empty string (use theme.css defaults)
    if (empty($branding['colors'])) {
        return '';
    }

    $css = '<style id="branding-overrides">';

    // Generate CSS for dark theme
    if (!empty($branding['colors']['dark'])) {
        $css .= "\n:root, html[data-theme=\"dark\"] {\n";
        foreach ($branding['colors']['dark'] as $varName => $value) {
            // SECURITY: Variable name must start with --
            if (strpos($varName, '--') !== 0) continue;
            // SECURITY: Remove dangerous characters from value
            $safeValue = preg_replace('/[;<>{}]/', '', $value);
            $css .= "  {$varName}: {$safeValue};\n";
        }
        $css .= "}\n";
    }

    // Generate CSS for light theme
    if (!empty($branding['colors']['light'])) {
        $css .= "\nhtml[data-theme=\"light\"] {\n";
        foreach ($branding['colors']['light'] as $varName => $value) {
            // SECURITY: Variable name must start with --
            if (strpos($varName, '--') !== 0) continue;
            // SECURITY: Remove dangerous characters from value
            $safeValue = preg_replace('/[;<>{}]/', '', $value);
            $css .= "  {$varName}: {$safeValue};\n";
        }
        $css .= "}\n";
    }

    $css .= '</style>';
    return $css;
}

function checkLicense($rider) {
  $currentYear = (int)date('Y');

  // Check license_year first (preferred for UCI registrations)
  if (!empty($rider['license_year'])) {
    $licenseYear = (int)$rider['license_year'];

    if ($licenseYear == $currentYear) {
      return array('class' => 'badge-success', 'message' => 'Giltig ' . $currentYear, 'valid' => true);
    } elseif ($licenseYear > $currentYear) {
      return array('class' => 'badge-success', 'message' => 'Giltig ' . $licenseYear, 'valid' => true);
    } else {
      return array('class' => 'badge-danger', 'message' => 'Utgången ' . $licenseYear, 'valid' => false);
    }
  }

  // Fallback to license_valid_until (for manually entered licenses)
  if (empty($rider['license_valid_until']) || $rider['license_valid_until'] === '0000-00-00') {
    return array('class' => 'badge-secondary', 'message' => 'Ingen giltighetstid', 'valid' => false);
  }

  $validUntil = strtotime($rider['license_valid_until']);
  $now = time();

  if ($validUntil < $now) {
    return array('class' => 'badge-danger', 'message' => 'Utgången', 'valid' => false);
  } elseif ($validUntil < strtotime('+30 days')) {
    return array('class' => 'badge-warning', 'message' => 'Löper snart ut', 'valid' => true);
  } else {
    return array('class' => 'badge-success', 'message' => 'Giltig', 'valid' => true);
  }
}

/**
 * Generate a unique advent_id for an event
 * Format: event-YYYY-NNN where YYYY is year and NNN is sequential number
 *
 * @param PDO $pdo Database connection
 * @param string $year Year for the event (YYYY format)
 * @return string Generated advent_id
 */
function generateEventAdventId($pdo, $year = null) {
  if ($year === null) {
    $year = date('Y');
  }

  // Find the highest number used for this year
  $stmt = $pdo->prepare("
    SELECT advent_id
    FROM events
    WHERE advent_id LIKE ?
    ORDER BY advent_id DESC
    LIMIT 1
  ");
  $stmt->execute(["event-$year-%"]);
  $existing = $stmt->fetch(PDO::FETCH_ASSOC);

  if ($existing && preg_match('/event-\d{4}-(\d+)/', $existing['advent_id'], $matches)) {
    $nextNum = intval($matches[1]) + 1;
  } else {
    $nextNum = 1;
  }

  // Format with leading zeros (3 digits)
  return sprintf('event-%s-%03d', $year, $nextNum);
}

/**
 * Generate a unique SWE license number for riders without UCI ID
 * Format: SWE25XXXXX (where 25 is year, XXXXX is 5-digit sequential number)
 *
 * @param object $db Database wrapper instance
 * @param int|null $year Year for the ID (defaults to current year)
 * @return string Generated license number
 */
function generateSweLicenseNumber($db, $year = null) {
  if ($year === null) {
    $year = date('y'); // 2-digit year
  } else {
    $year = substr($year, -2); // Get last 2 digits
  }

  $prefix ="SWE{$year}";

  // Find the highest number used for this year prefix
  $existing = $db->getRow("
    SELECT license_number
    FROM riders
    WHERE license_number LIKE ?
    ORDER BY license_number DESC
    LIMIT 1
  ", [$prefix . '%']);

  if ($existing && preg_match('/SWE\d{2}(\d+)/', $existing['license_number'], $matches)) {
    $nextNum = intval($matches[1]) + 1;
  } else {
    $nextNum = 1;
  }

  // Format with leading zeros (5 digits)
  return sprintf('%s%05d', $prefix, $nextNum);
}

/**
 * Generate a unique SWE-ID for riders without UCI ID (engångslicens)
 * Format: SWE-YYYY-NNNNN (e.g., SWE-2025-00001)
 *
 * Uses a static counter to track IDs generated within the same request/session,
 * preventing duplicates when multiple riders are created in a batch import.
 *
 * @param object $db Database wrapper instance
 * @return string Generated SWE-ID
 */
function generateSweId($db) {
  static $sessionCounter = null;
  static $baseNumber = null;

  $year = date('Y');

  // Initialize on first call - get highest from database
  if ($baseNumber === null) {
    $lastSweId = $db->getValue("
      SELECT MAX(CAST(SUBSTRING(license_number, 10) AS UNSIGNED))
      FROM riders
      WHERE license_number LIKE ?
    ", ["SWE-$year-%"]);

    $baseNumber = $lastSweId ? $lastSweId : 0;
    $sessionCounter = 0;
  }

  // Increment session counter for each call
  $sessionCounter++;
  $nextNumber = $baseNumber + $sessionCounter;

  return sprintf("SWE-%d-%05d", $year, $nextNumber);
}

class DatabaseWrapper {
  private $pdo;

  public function __construct($pdo) {
    $this->pdo = $pdo;
  }

  /**
   * Get the underlying PDO instance
   *
   * @return PDO
   */
  public function getPdo() {
    return $this->pdo;
  }

  public function query($sql, $params = array()) {
    try {
      $stmt = $this->pdo->prepare($sql);
      $stmt->execute($params);
      return $stmt;
    } catch (PDOException $e) {
      error_log("Query failed: " . $e->getMessage() . " | SQL: " . $sql);
      return false;
    }
  }

  public function getAll($sql, $params = array()) {
    $stmt = $this->query($sql, $params);
    if (!$stmt) return [];
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
  }

  public function getRow($sql, $params = array()) {
    $stmt = $this->query($sql, $params);
    if (!$stmt) return [];
    $result = $stmt->fetch(PDO::FETCH_ASSOC);
    return $result ?: [];
  }

  public function getValue($sql, $params = array()) {
    $stmt = $this->query($sql, $params);
    if (!$stmt) return null;
    return $stmt->fetchColumn();
  }

  public function getOne($sql, $params = array()) {
    return $this->getValue($sql, $params);
  }

  public function insert($table, $data) {
    $fields = array_keys($data);
    $placeholders = array_fill(0, count($fields), '?');

    $sql = "INSERT INTO " . $table . " (" . implode(', ', $fields) . ") VALUES (" . implode(', ', $placeholders) . ")";
    $stmt = $this->query($sql, array_values($data));
    if (!$stmt) return 0;
    return $this->pdo->lastInsertId();
  }

  public function update($table, $data, $where, $params = array()) {
    $sets = array();
    $values = array();

    foreach ($data as $key => $value) {
      $sets[] = $key . " = ?";
      $values[] = $value;
    }

    $sql = "UPDATE " . $table . " SET " . implode(', ', $sets) . " WHERE " . $where;
    $stmt = $this->query($sql, array_merge($values, $params));
    if (!$stmt) return 0;
    return $stmt->rowCount();
  }

  public function delete($table, $where, $params = array()) {
    $sql = "DELETE FROM " . $table . " WHERE " . $where;
    $stmt = $this->query($sql, $params);
    if (!$stmt) return 0;
    return $stmt->rowCount();
  }

  public function beginTransaction() {
    return $this->pdo->beginTransaction();
  }

  public function commit() {
    return $this->pdo->commit();
  }

  public function rollback() {
    return $this->pdo->rollBack();
  }
}

function getDB() {
  global $pdo;
  static $db = null;
  
  if ($db === null) {
    $db = new DatabaseWrapper($pdo);
  }
  
  return $db;
}

function checkCsrf() {
  return check_csrf();
}

function get_current_admin() {
  return get_admin_user();
}

/**
 * Paginate results
 *
 * @param int $totalItems Total number of items
 * @param int $perPage Items per page
 * @param int $currentPage Current page number
 * @return array Pagination data
 */
function paginate($totalItems, $perPage, $currentPage = 1) {
  $totalPages = max(1, ceil($totalItems / $perPage));
  $currentPage = max(1, min($currentPage, $totalPages));

  return [
    'total_items' => $totalItems,
    'per_page' => $perPage,
    'current_page' => $currentPage,
    'total_pages' => $totalPages,
    'has_prev' => $currentPage > 1,
    'has_next' => $currentPage < $totalPages,
    'prev_page' => max(1, $currentPage - 1),
    'next_page' => min($totalPages, $currentPage + 1),
    'offset' => ($currentPage - 1) * $perPage
  ];
}

/**
 * Get version and deployment information
 *
 * @return array Version information
 */
function getVersionInfo() {
  // Try to get git commit count
  $gitCommits = 0;
  try {
    if (function_exists('shell_exec')) {
      $output = @shell_exec('cd ' . ROOT_PATH . ' && git rev-list --count HEAD 2>/dev/null');
      if ($output !== null) {
        $gitCommits = (int)trim($output);
      }
    }
  } catch (Exception $e) {
    // Silently fail if git is not available
  }

  // Calculate total deployments
  $totalDeployments = $gitCommits + DEPLOYMENT_OFFSET;

  // Get short commit hash
  $commitHash = '';
  try {
    if (function_exists('shell_exec')) {
      $output = @shell_exec('cd ' . ROOT_PATH . ' && git rev-parse --short HEAD 2>/dev/null');
      if ($output !== null) {
        $commitHash = trim($output);
      }
    }
  } catch (Exception $e) {
    // Silently fail
  }

  return [
    'version' => APP_VERSION,
    'name' => APP_VERSION_NAME,
    'build' => defined('APP_BUILD') ? APP_BUILD : '',
    'deployment' => $totalDeployments,
    'commit' => $commitHash
  ];
}

/**
 * Render global sponsors for a page
 * Only shows to admins unless public_enabled is on
 *
 * @param string $pageType Page type (home, results, series_list, etc)
 * @param string $position Position (header_banner, sidebar_top, etc)
 * @param string $title Optional section title
 * @return string HTML output
 */
function render_global_sponsors($pageType, $position, $title = 'Sponsorer') {
    global $pdo;

    // Check user roles - super_admin ALWAYS sees sponsors
    $isSuperAdmin = function_exists('hasRole') && hasRole('super_admin');
    $isAdmin = function_exists('hasRole') && (hasRole('admin') || hasRole('super_admin'));

    // Check public_enabled and hide_empty_for_admin settings
    $publicEnabled = false;
    $hideEmptyForAdmin = false;
    try {
        $stmt = $pdo->query("SELECT setting_key, setting_value FROM sponsor_settings WHERE setting_key IN ('public_enabled', 'hide_empty_for_admin')");
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            if ($row['setting_key'] === 'public_enabled') {
                $publicEnabled = ($row['setting_value'] == '1');
            } elseif ($row['setting_key'] === 'hide_empty_for_admin') {
                $hideEmptyForAdmin = ($row['setting_value'] == '1');
            }
        }
    } catch (Exception $e) {
        // Table might not exist yet - super_admin can still see placeholders
        if (!$isSuperAdmin) {
            return '';
        }
    }

    // Super admin ALWAYS sees sponsors (for testing)
    // Others only see if public is enabled
    if (!$isSuperAdmin && !$publicEnabled) {
        return '';
    }

    // Load sponsor manager
    require_once __DIR__ . '/GlobalSponsorManager.php';
    $sponsorManager = new GlobalSponsorManager($pdo);

    // Get sponsors for this placement
    $sponsors = $sponsorManager->getSponsorsForPlacement($pageType, $position);

    if (empty($sponsors)) {
        // Show placeholder for super_admin if no sponsors configured
        // BUT only if hide_empty_for_admin is NOT enabled
        if ($isSuperAdmin && !$hideEmptyForAdmin) {
            return '<div class="sponsor-section sponsor-section-' . h($position) . '" style="border: 2px dashed var(--color-border); padding: var(--space-md); text-align: center; opacity: 0.6;">
                <small style="color: var(--color-text-muted);">
                    <i data-lucide="image" style="width: 16px; height: 16px; vertical-align: middle;"></i>
                    Sponsorplats: ' . h($pageType) . ' / ' . h($position) . ' (endast synlig för super_admin)
                </small>
            </div>';
        }
        return '';
    }

    // Render sponsors
    return $sponsorManager->renderSection($pageType, $position, $title);
}
?>
