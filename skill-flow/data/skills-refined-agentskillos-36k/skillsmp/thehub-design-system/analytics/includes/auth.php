<?php
/**
 * Analytics Authentication & Authorization
 *
 * KRITISKT: Alla funktioner tar PDO som parameter (ingen global $pdo!)
 *
 * Funktioner:
 * - requireAnalyticsAuth() - Krav inloggning med ratt roll
 * - requireCSRF() - Validera CSRF-token
 * - generateCSRF() - Generera CSRF-token
 * - logAnalyticsAccess() - Logga atkomst till analytics
 * - maskSmallSegments() - GDPR-maskering av sma segment
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

// Roller som har tillgang till analytics
define('ANALYTICS_ROLES', ['admin', 'super_admin', 'scf', 'club_admin', 'promotor']);

// Minimum segment-storlek for publika insikter (GDPR)
define('PUBLIC_MIN_SEGMENT_SIZE', 10);

/**
 * Sakerstall att session ar startad
 * Anvander samma sessionsnamn som config.php
 */
function ensureAnalyticsSession(): void {
    if (session_status() !== PHP_SESSION_ACTIVE) {
        session_name('thehub_session');
        session_start();
    }
}

/**
 * Krav inloggning med analytics-behorighet
 * Omdirigerar till login om ej inloggad
 */
function requireAnalyticsAuth(): void {
    ensureAnalyticsSession();

    // Kolla om inloggad
    if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
        $redirect = urlencode($_SERVER['REQUEST_URI']);
        header("Location: /admin/login.php?redirect=$redirect");
        exit;
    }

    // Kolla roll
    $role = $_SESSION['admin_role'] ?? null;

    if (!in_array($role, ANALYTICS_ROLES)) {
        http_response_code(403);
        die('Atkomst nekad: Din roll (' . htmlspecialchars($role ?? 'okand') . ') har inte behorighet till analytics.');
    }
}

/**
 * Krav CSRF-token for POST-requests
 * Anvander samma token-struktur som includes/auth.php
 */
function requireAnalyticsCSRF(): void {
    ensureAnalyticsSession();

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Hamta token fran POST eller header
        $token = $_POST['csrf_token']
            ?? $_SERVER['HTTP_X_CSRF_TOKEN']
            ?? null;

        if (!$token || !isset($_SESSION['csrf_token'])) {
            http_response_code(403);
            die('CSRF-validering misslyckades: Token saknas');
        }

        if (!hash_equals($_SESSION['csrf_token'], $token)) {
            http_response_code(403);
            die('CSRF-validering misslyckades: Ogiltig token');
        }
    }
}

/**
 * Generera CSRF-token
 * Kompatibel med includes/auth.php generate_csrf_token()
 *
 * @return string CSRF token
 */
function generateAnalyticsCSRF(): string {
    ensureAnalyticsSession();

    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }

    return $_SESSION['csrf_token'];
}

/**
 * Generera CSRF-input for formuler
 *
 * @return string HTML input-falt
 */
function csrfField(): string {
    $token = generateAnalyticsCSRF();
    return '<input type="hidden" name="csrf_token" value="' . htmlspecialchars($token) . '">';
}

/**
 * Hamta nuvarande anvandare
 *
 * @return array|null Anvandardata eller null
 */
function getCurrentAnalyticsUser(): ?array {
    ensureAnalyticsSession();

    if (!isset($_SESSION['admin_logged_in']) || !$_SESSION['admin_logged_in']) {
        return null;
    }

    return [
        'id' => $_SESSION['admin_id'] ?? null,
        'username' => $_SESSION['admin_username'] ?? null,
        'email' => $_SESSION['admin_email'] ?? null,
        'role' => $_SESSION['admin_role'] ?? null,
        'name' => $_SESSION['admin_name'] ?? null
    ];
}

/**
 * Kolla om anvandare har minst en viss roll
 *
 * @param string $requiredRole Minsta roll som kravs
 * @return bool True om anvandare har tillracklig behorighet
 */
function hasAnalyticsRole(string $requiredRole): bool {
    ensureAnalyticsSession();

    $currentRole = $_SESSION['admin_role'] ?? null;

    $roles = [
        'rider' => 1,
        'promotor' => 2,
        'club_admin' => 2,
        'scf' => 3,
        'admin' => 4,
        'super_admin' => 5
    ];

    return ($roles[$currentRole] ?? 0) >= ($roles[$requiredRole] ?? 999);
}

/**
 * Logga analytics-atkomst
 *
 * KRITISKT: Tar PDO som parameter - ingen global!
 *
 * @param PDO $pdo Databasanslutning
 * @param string $action Vad som gjordes (t.ex. 'view_dashboard', 'export_report')
 * @param array $details Extra detaljer
 * @return bool True om loggning lyckades
 */
function logAnalyticsAccess(PDO $pdo, string $action, array $details = []): bool {
    ensureAnalyticsSession();

    // Kolla om tabellen finns
    $check = $pdo->query("
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'analytics_logs'
    ")->fetchColumn();

    if (!$check) {
        error_log("[Analytics] Logg-tabell saknas, kan ej logga: $action");
        return false;
    }

    try {
        $stmt = $pdo->prepare("
            INSERT INTO analytics_logs (level, job_name, message, context)
            VALUES ('info', 'access', ?, ?)
        ");

        $context = [
            'user_id' => $_SESSION['admin_id'] ?? null,
            'user_role' => $_SESSION['admin_role'] ?? null,
            'username' => $_SESSION['admin_username'] ?? null,
            'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown',
            'details' => $details
        ];

        $stmt->execute([
            $action,
            json_encode($context, JSON_UNESCAPED_UNICODE)
        ]);

        return true;
    } catch (PDOException $e) {
        error_log("[Analytics] Loggningsfel: " . $e->getMessage());
        return false;
    }
}

/**
 * Maskera data om segmentet ar for litet (GDPR)
 *
 * Segment med farre an PUBLIC_MIN_SEGMENT_SIZE (default 10) deltagare
 * slas ihop till "Ovrigt" for att skydda individers integritet.
 *
 * Standardiserat format: 'label' och 'count'
 *
 * @param array $data Data att maskera
 * @param string $countField Faltnamn for antal (default 'count')
 * @param string $labelField Faltnamn for etikett (default 'label')
 * @return array Maskerad data
 */
function maskSmallSegments(array $data, string $countField = 'count', string $labelField = 'label'): array {
    $masked = [];
    $otherCount = 0;

    foreach ($data as $row) {
        $count = (int)($row[$countField] ?? 0);

        if ($count >= PUBLIC_MIN_SEGMENT_SIZE) {
            $masked[] = $row;
        } else {
            $otherCount += $count;
        }
    }

    // Lagg till "Ovrigt" om det finns maskerade segment
    // Och endast om "Ovrigt" ocksa uppfyller minimikravet
    if ($otherCount >= PUBLIC_MIN_SEGMENT_SIZE) {
        $masked[] = [
            $labelField => 'Ovrigt',
            $countField => $otherCount
        ];
    }

    return $masked;
}

/**
 * Normalisera data till standardformat for maskering
 *
 * Konverterar data med varierande faltnamn till standardiserat
 * format med 'label' och 'count'.
 *
 * @param array $data Data att normalisera
 * @param string $sourceLabelField Ursprungligt faltnamn for etikett
 * @param string $sourceCountField Ursprungligt faltnamn for antal
 * @return array Normaliserad data
 */
function normalizeForMasking(array $data, string $sourceLabelField, string $sourceCountField): array {
    return array_map(function($row) use ($sourceLabelField, $sourceCountField) {
        return [
            'label' => $row[$sourceLabelField] ?? 'Okand',
            'count' => (int)($row[$sourceCountField] ?? 0),
            '_original' => $row  // Behall original for eventuell extra data
        ];
    }, $data);
}

/**
 * Kontrollera om anvandare har tillgang till en specifik klubbs data
 *
 * @param PDO $pdo Databasanslutning
 * @param int $clubId Klubb-ID
 * @return bool True om tillgang
 */
function canAccessClubAnalytics(PDO $pdo, int $clubId): bool {
    ensureAnalyticsSession();

    // Admin och super_admin har tillgang till allt
    if (hasAnalyticsRole('admin')) {
        return true;
    }

    $userId = $_SESSION['admin_id'] ?? null;
    $role = $_SESSION['admin_role'] ?? null;

    if (!$userId) {
        return false;
    }

    // Kolla om anvandare ar klubbadmin for denna klubb
    $stmt = $pdo->prepare("
        SELECT 1 FROM club_admins
        WHERE user_id = ? AND club_id = ?
        LIMIT 1
    ");
    $stmt->execute([$userId, $clubId]);

    return (bool)$stmt->fetch();
}

/**
 * Kontrollera om anvandare har tillgang till en specifik series data
 *
 * @param PDO $pdo Databasanslutning
 * @param int $seriesId Serie-ID
 * @return bool True om tillgang
 */
function canAccessSeriesAnalytics(PDO $pdo, int $seriesId): bool {
    ensureAnalyticsSession();

    // Admin och super_admin har tillgang till allt
    if (hasAnalyticsRole('admin')) {
        return true;
    }

    $userId = $_SESSION['admin_id'] ?? null;

    if (!$userId) {
        return false;
    }

    // Kolla om anvandare ar promotor for denna serie
    $stmt = $pdo->prepare("
        SELECT 1 FROM promotor_series
        WHERE user_id = ? AND series_id = ?
        LIMIT 1
    ");
    $stmt->execute([$userId, $seriesId]);

    return (bool)$stmt->fetch();
}
