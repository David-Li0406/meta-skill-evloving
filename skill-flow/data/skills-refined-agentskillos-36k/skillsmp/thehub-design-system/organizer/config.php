<?php
/**
 * Organizer Registration App - Configuration
 *
 * DEMO VERSION - Förenklat skal för demonstration
 * Full funktionalitet kommer efter anmälningsplattformen är klar
 */

// Ladda huvudkonfigurationen
require_once __DIR__ . '/../config.php';

// =============================================================================
// APP-KONFIGURATION
// =============================================================================

define('ORGANIZER_BASE_URL', SITE_URL . '/organizer');
define('ORGANIZER_APP_NAME', 'Platsregistrering');
define('ORGANIZER_SESSION_TIMEOUT', 28800); // 8 timmar

// =============================================================================
// DEMO DATA
// =============================================================================

/**
 * Hämta demo-event
 */
function getEventWithClasses(int $eventId): ?array {
    global $pdo;

    // Hämta riktigt event från databasen
    $stmt = $pdo->prepare("
        SELECT e.*, s.name as series_name
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        WHERE e.id = ?
    ");
    $stmt->execute([$eventId]);
    $event = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$event) {
        return null;
    }

    // Demo-klasser med priser
    $event['classes'] = [
        ['id' => 1, 'name' => 'Men Elite', 'display_name' => 'Herrar Elite', 'price' => 450, 'onsite_price' => 550],
        ['id' => 2, 'name' => 'Women Elite', 'display_name' => 'Damer Elite', 'price' => 450, 'onsite_price' => 550],
        ['id' => 3, 'name' => 'Men Sport', 'display_name' => 'Herrar Sport', 'price' => 350, 'onsite_price' => 450],
        ['id' => 4, 'name' => 'Women Sport', 'display_name' => 'Damer Sport', 'price' => 350, 'onsite_price' => 450],
        ['id' => 5, 'name' => 'Men Master', 'display_name' => 'Herrar Master 40+', 'price' => 350, 'onsite_price' => 450],
        ['id' => 6, 'name' => 'Juniors', 'display_name' => 'Juniorer U19', 'price' => 250, 'onsite_price' => 350],
    ];

    // Demo betalningskonfiguration
    $event['payment_config'] = [
        'swish_number' => '1234567890',
        'swish_name' => 'Demo Arrangör'
    ];

    return $event;
}

/**
 * Demo-statistik
 */
function countEventRegistrations(int $eventId): array {
    return [
        'total' => 47,
        'onsite' => 12,
        'online' => 35,
        'paid' => 42,
        'unpaid' => 5
    ];
}

/**
 * Sök åkare i databasen
 */
function searchRiders(string $query, int $limit = 20): array {
    global $pdo;

    $query = trim($query);
    if (strlen($query) < 2) {
        return [];
    }

    $searchTerm = '%' . $query . '%';

    $stmt = $pdo->prepare("
        SELECT r.id, r.firstname, r.lastname, r.birth_year, r.gender,
               r.license_number, r.email, r.phone, r.nationality,
               r.ice_name, r.ice_phone, c.name as club_name
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.active = 1
          AND (
              CONCAT(r.firstname, ' ', r.lastname) LIKE ?
              OR r.license_number LIKE ?
              OR r.firstname LIKE ?
              OR r.lastname LIKE ?
          )
        ORDER BY r.lastname, r.firstname
        LIMIT ?
    ");
    $stmt->execute([$searchTerm, $searchTerm, $searchTerm, $searchTerm, $limit]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Formatera Swish-nummer för visning
 */
function formatSwishNumber(string $number): string {
    $clean = preg_replace('/[^0-9]/', '', $number);
    if (strlen($clean) === 10 && substr($clean, 0, 1) === '0') {
        return substr($clean, 0, 3) . '-' . substr($clean, 3, 3) . ' ' . substr($clean, 6, 2) . ' ' . substr($clean, 8, 2);
    }
    return $number;
}

// =============================================================================
// AUTENTISERING (förenklad för demo)
// =============================================================================

/**
 * Kräv organizer-inloggning
 */
function requireOrganizer() {
    if (!isLoggedIn()) {
        header('Location: ' . ORGANIZER_BASE_URL . '/index.php');
        exit;
    }

    if (!hasRole('promotor')) {
        http_response_code(403);
        die('Endast arrangörer har tillgång till denna sida.');
    }
}

/**
 * Kräv tillgång till event (förenklad - alla inloggade har tillgång i demo)
 */
function requireEventAccess(int $eventId) {
    requireOrganizer();
}

/**
 * Hämta events som användaren har tillgång till via promotor_events
 */
function getAccessibleEvents(): array {
    global $pdo;

    $currentUser = getCurrentAdmin();
    $userId = $currentUser['id'] ?? 0;

    if (!$userId) {
        return [];
    }

    // Hämta endast events som användaren är kopplad till via promotor_events
    $stmt = $pdo->prepare("
        SELECT e.*, s.name as series_name,
               COALESCE(reg.registration_count, 0) as registration_count
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        JOIN promotor_events pe ON pe.event_id = e.id
        LEFT JOIN (
            SELECT event_id, COUNT(*) as registration_count
            FROM event_registrations
            GROUP BY event_id
        ) reg ON reg.event_id = e.id
        WHERE pe.user_id = ?
          AND e.active = 1
          AND e.date >= CURDATE() - INTERVAL 7 DAY
        ORDER BY e.date ASC
        LIMIT 20
    ");
    $stmt->execute([$userId]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}
