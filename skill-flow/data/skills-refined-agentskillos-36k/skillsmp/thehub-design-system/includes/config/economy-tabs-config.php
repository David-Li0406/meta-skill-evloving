<?php
/**
 * EKONOMI TAB SYSTEM
 * Dedikerad konfiguration för biljett-, anmälnings- och betalningshantering
 *
 * TRE KONTEXTER:
 * 1. GLOBAL   - Övergripande ordrar, mallar, rapporter (ingen ID-kontext)
 * 2. EVENT    - Event-specifik ekonomi (kräver event_id)
 * 3. SERIES   - Serie-specifik ekonomi (kräver series_id)
 *
 * Varje kontext har sina egna flikar och sidor.
 */

// ============================================================================
// GLOBAL EKONOMI - Ingen kontext krävs
// ============================================================================
$ECONOMY_GLOBAL = [
    'title' => 'Ekonomi',
    'icon' => 'wallet',
    'base_url' => '/admin/economy/',
    'tabs' => [
        [
            'id' => 'orders',
            'label' => 'Ordrar',
            'icon' => 'receipt',
            'url' => '/admin/orders.php',
            'description' => 'Alla ordrar i systemet'
        ],
        [
            'id' => 'recipients',
            'label' => 'Mottagare',
            'icon' => 'smartphone',
            'url' => '/admin/payment-recipients.php',
            'description' => 'Swish-mottagare och gateways'
        ],
        [
            'id' => 'templates',
            'label' => 'Prismallar',
            'icon' => 'file-text',
            'url' => '/admin/pricing-templates.php',
            'description' => 'Återanvändbara prismallar'
        ],
        [
            'id' => 'settings',
            'label' => 'Inställningar',
            'icon' => 'settings',
            'url' => '/admin/payment-settings.php',
            'description' => 'Globala betalningsinställningar'
        ]
    ]
];

// ============================================================================
// EVENT EKONOMI - Kräver event_id
// ============================================================================
$ECONOMY_EVENT = [
    'title' => 'Event Ekonomi',
    'icon' => 'calendar-check',
    'context' => 'event_id',
    'tabs' => [
        [
            'id' => 'overview',
            'label' => 'Översikt',
            'icon' => 'layout-dashboard',
            'url' => '/admin/event-economy.php',
            'description' => 'Statistik och snabbåtgärder'
        ],
        [
            'id' => 'registrations',
            'label' => 'Anmälningar',
            'icon' => 'users',
            'url' => '/admin/event-registrations.php',
            'description' => 'Hantera anmälningar'
        ],
        [
            'id' => 'orders',
            'label' => 'Ordrar',
            'icon' => 'receipt',
            'url' => '/admin/event-orders.php',
            'description' => 'Event-specifika ordrar'
        ],
        [
            'id' => 'pricing',
            'label' => 'Prissättning',
            'icon' => 'tag',
            'url' => '/admin/event-pricing.php',
            'description' => 'Priser per klass'
        ],
        [
            'id' => 'settings',
            'label' => 'Betalning',
            'icon' => 'credit-card',
            'url' => '/admin/event-payment.php',
            'description' => 'Swish, kort, WooCommerce'
        ]
    ]
];

// ============================================================================
// SERIES EKONOMI - Kräver series_id
// ============================================================================
$ECONOMY_SERIES = [
    'title' => 'Serie Ekonomi',
    'icon' => 'medal',
    'context' => 'series_id',
    'tabs' => [
        [
            'id' => 'overview',
            'label' => 'Översikt',
            'icon' => 'layout-dashboard',
            'url' => '/admin/series-economy.php',
            'description' => 'Statistik för serien'
        ],
        [
            'id' => 'pricing',
            'label' => 'Prissättning',
            'icon' => 'tag',
            'url' => '/admin/series-pricing.php',
            'description' => 'Standard priser per klass'
        ],
        [
            'id' => 'rules',
            'label' => 'Regler',
            'icon' => 'shield-check',
            'url' => '/admin/registration-rules.php',
            'description' => 'Anmälningsregler'
        ]
    ]
];

// ============================================================================
// HJÄLPFUNKTIONER
// ============================================================================

/**
 * Hämta ekonomi-kontext baserat på URL-parametrar
 *
 * @return array ['type' => 'global'|'event'|'series', 'id' => int|null, 'config' => array]
 */
function get_economy_context() {
    global $ECONOMY_GLOBAL, $ECONOMY_EVENT, $ECONOMY_SERIES;

    // Support both 'event_id' and 'id' for backward compatibility
    $event_id = isset($_GET['event_id']) ? (int)$_GET['event_id'] : (isset($_GET['id']) ? (int)$_GET['id'] : null);
    $series_id = isset($_GET['series_id']) ? (int)$_GET['series_id'] : null;

    if ($event_id) {
        return [
            'type' => 'event',
            'id' => $event_id,
            'config' => $ECONOMY_EVENT
        ];
    }

    if ($series_id) {
        return [
            'type' => 'series',
            'id' => $series_id,
            'config' => $ECONOMY_SERIES
        ];
    }

    return [
        'type' => 'global',
        'id' => null,
        'config' => $ECONOMY_GLOBAL
    ];
}

/**
 * Generera tab-URL med rätt kontext
 *
 * @param string $base_url Tab-ens bas-URL
 * @param string $context_type 'event'|'series'|'global'
 * @param int|null $context_id Event eller serie ID
 * @return string Komplett URL med kontext
 */
function economy_tab_url($base_url, $context_type, $context_id = null) {
    if ($context_type === 'global' || !$context_id) {
        return $base_url;
    }

    // Use 'id' for event pages (backward compatible) and 'series_id' for series
    $param = $context_type === 'event' ? 'id' : 'series_id';
    $separator = strpos($base_url, '?') !== false ? '&' : '?';

    return $base_url . $separator . $param . '=' . $context_id;
}

/**
 * Hämta aktiv tab baserat på nuvarande sida
 *
 * @param array $tabs Tab-konfiguration
 * @return string|null Aktiv tab ID
 */
function get_active_economy_tab($tabs) {
    $current_page = basename($_SERVER['PHP_SELF']);

    foreach ($tabs as $tab) {
        $tab_page = basename(parse_url($tab['url'], PHP_URL_PATH));
        if ($tab_page === $current_page) {
            return $tab['id'];
        }
    }

    return $tabs[0]['id'] ?? null;
}

/**
 * Hämta event-info för breadcrumb
 *
 * @param int $event_id
 * @return array|null ['name' => string, 'date' => string]
 */
function get_economy_event_info($event_id) {
    global $pdo;

    // Om $pdo inte är satt, försök hämta via hub_db()
    if (!$pdo && function_exists('hub_db')) {
        $pdo = hub_db();
    }

    if (!$pdo || !$event_id) {
        return null;
    }

    try {
        $stmt = $pdo->prepare("SELECT name, date FROM events WHERE id = ?");
        $stmt->execute([$event_id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    } catch (Exception $e) {
        return null;
    }
}

/**
 * Hämta serie-info för breadcrumb
 *
 * @param int $series_id
 * @return array|null ['name' => string, 'year' => int]
 */
function get_economy_series_info($series_id) {
    global $pdo;

    // Om $pdo inte är satt, försök hämta via hub_db()
    if (!$pdo && function_exists('hub_db')) {
        $pdo = hub_db();
    }

    if (!$pdo || !$series_id) {
        return null;
    }

    try {
        $stmt = $pdo->prepare("SELECT name, year FROM series WHERE id = ?");
        $stmt->execute([$series_id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    } catch (Exception $e) {
        return null;
    }
}

/**
 * Kontrollera om användare har tillgång till event-ekonomi
 *
 * @param int $event_id
 * @return bool
 */
function can_access_event_economy($event_id) {
    // Super admin har alltid tillgång
    if (function_exists('hasRole') && hasRole('super_admin')) {
        return true;
    }

    // Admin har alltid tillgång (fallback för när roller inte är konfigurerade)
    if (function_exists('is_admin') && is_admin()) {
        return true;
    }

    // Om användaren är inloggad som admin, ge tillgång
    if (!empty($_SESSION['admin_user_id']) || !empty($_SESSION['admin_logged_in'])) {
        return true;
    }

    // Kontrollera promotor-koppling
    global $pdo;
    $user_id = $_SESSION['admin_user_id'] ?? null;

    // Om $pdo inte är satt, försök hämta via hub_db()
    if (!$pdo && function_exists('hub_db')) {
        $pdo = hub_db();
    }

    if (!$pdo || !$user_id || !$event_id) {
        // Om ingen PDO men användare är inloggad, ge tillgång ändå
        if (!empty($_SESSION['admin_logged_in'])) {
            return true;
        }
        return false;
    }

    try {
        // Kolla om event ägs av användaren (created_by) eller via promotor_events
        $stmt = $pdo->prepare("
            SELECT 1 FROM events
            WHERE id = ? AND created_by = ?
            UNION
            SELECT 1 FROM promotor_events
            WHERE event_id = ? AND user_id = ?
            LIMIT 1
        ");
        $stmt->execute([$event_id, $user_id, $event_id, $user_id]);
        return $stmt->fetch() !== false;
    } catch (Exception $e) {
        return false;
    }
}

/**
 * Kontrollera om användare har tillgång till serie-ekonomi
 *
 * @param int $series_id
 * @return bool
 */
function can_access_series_economy($series_id) {
    // Super admin har alltid tillgång
    if (function_exists('hasRole') && hasRole('super_admin')) {
        return true;
    }

    // Admin har alltid tillgång (fallback för när roller inte är konfigurerade)
    if (function_exists('is_admin') && is_admin()) {
        return true;
    }

    // Om användaren är inloggad som admin, ge tillgång
    if (!empty($_SESSION['admin_user_id']) || !empty($_SESSION['admin_logged_in'])) {
        return true;
    }

    // Kontrollera promotor-koppling via events
    global $pdo;
    $user_id = $_SESSION['admin_user_id'] ?? null;

    // Om $pdo inte är satt, försök hämta via hub_db()
    if (!$pdo && function_exists('hub_db')) {
        $pdo = hub_db();
    }

    if (!$pdo || !$user_id || !$series_id) {
        // Om ingen PDO men användare är inloggad, ge tillgång ändå
        if (!empty($_SESSION['admin_logged_in'])) {
            return true;
        }
        return false;
    }

    try {
        // Promotor har tillgång om de har minst ett event i serien
        $stmt = $pdo->prepare("
            SELECT 1 FROM events e
            LEFT JOIN promotor_events pe ON pe.event_id = e.id
            WHERE e.series_id = ?
            AND (e.created_by = ? OR pe.user_id = ?)
            LIMIT 1
        ");
        $stmt->execute([$series_id, $user_id, $user_id]);
        return $stmt->fetch() !== false;
    } catch (Exception $e) {
        return false;
    }
}
