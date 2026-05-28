<?php
/**
 * TheHUB Router
 * Handles URL routing for the SPA structure
 *
 * AUTHENTICATION: Most content pages are public. Only profile, checkout
 * and dashboard require login.
 */

// Ensure hub-config is loaded
$hubConfigPath = __DIR__ . '/hub-config.php';
if (file_exists($hubConfigPath)) {
    require_once $hubConfigPath;
}

// Fallback for hub_is_logged_in if not defined
if (!function_exists('hub_is_logged_in')) {
    function hub_is_logged_in() {
        return isset($_SESSION['rider_id']) && $_SESSION['rider_id'] > 0;
    }
}

// Ensure HUB_ROOT is defined
if (!defined('HUB_ROOT')) {
    define('HUB_ROOT', __DIR__);
}

/**
 * Check if the current page requires authentication
 * Returns true if user should be redirected to login
 */
function hub_requires_auth(string $page): bool {
    // Public pages - accessible without login
    $publicPages = [
        // Auth pages
        '', 'welcome', 'login', 'logout', 'forgot-password', 'reset-password', 'activate-account', 'index.php',
        // Public content pages
        'calendar', 'results', 'series', 'database', 'ranking',
        'rider', 'riders', 'event', 'club', 'clubs',
        'rider-register', 'club-points', 'achievements',
        // News/Blog
        'news',
        // Registration pages (login required but handled in page)
        'register'
    ];

    // Pages that require login
    // - profile (user's personal data)
    // - checkout (payment)
    // - dashboard (personal dashboard)

    return !in_array($page, $publicPages);
}

function hub_get_current_page(): array {
    $raw = trim($_GET['page'] ?? '', '/');
    $section = explode('/', $raw)[0] ?? '';

    // =========================================================================
    // AUTHENTICATION CHECK - Require login for all pages except public ones
    // =========================================================================
    if (hub_requires_auth($section) && !hub_is_logged_in()) {
        // Store the requested URL for redirect after login
        $redirect = '/' . $raw;
        header('Location: /login?redirect=' . urlencode($redirect));
        exit;
    }

    // Root route - show welcome page for ALL users (same great design for everyone)
    // Welcome page adapts content based on login status
    if ($raw === '' || $raw === 'index.php') {
        return ['page' => 'welcome', 'section' => null, 'params' => [], 'file' => HUB_ROOT . '/pages/welcome.php'];
    }

    $segments = explode('/', $raw);
    $section = $segments[0];
    $subpage = $segments[1] ?? 'index';
    $id = $segments[2] ?? ($segments[1] ?? null);

    // Simple pages (login, logout, password reset, etc.)
    $simplePages = [
        'login' => '/pages/login.php',
        'logout' => '/pages/logout.php',
        'forgot-password' => '/pages/forgot-password.php',
        'reset-password' => '/pages/reset-password.php',
        'activate-account' => '/pages/activate-account.php',
        'checkout' => '/pages/checkout.php',
    ];

    if (isset($simplePages[$section])) {
        return [
            'page' => $section,
            'section' => $section,
            'params' => [],
            'file' => HUB_ROOT . $simplePages[$section]
        ];
    }

    // New V1.0 section-based routing
    $sectionRoutes = [
        'calendar' => [
            'index' => '/pages/calendar/index.php',
            'event' => '/pages/event.php'  // Use full event page for calendar too
        ],
        'results' => [
            'index' => '/pages/results.php',  // Legacy - will move to /pages/results/index.php
            'event' => '/pages/event.php'     // Legacy
        ],
        'series' => [
            'index' => '/pages/series/index.php',
            'show' => '/pages/series/show.php'
        ],
        'database' => [
            'index' => '/pages/database/index.php',
            'rider' => '/pages/rider.php',    // Legacy - will move
            'club' => '/pages/club.php'       // Legacy
        ],
        'ranking' => [
            'index' => '/pages/ranking.php',  // Legacy
            'riders' => '/pages/ranking.php',
            'clubs' => '/pages/ranking.php',
            'events' => '/pages/ranking.php'
        ],
        'profile' => [
            'index' => '/pages/profile/index.php',
            'edit' => '/pages/profile/edit.php',
            'children' => '/pages/profile/children.php',
            'club-admin' => '/pages/profile/club-admin.php',
            'registrations' => '/pages/profile/registrations.php',
            'results' => '/pages/profile/results.php',
            'receipts' => '/pages/profile/receipts.php',
            'race-reports' => '/pages/profile/race-reports.php',
            'event-ratings' => '/pages/profile/event-ratings.php',
            'tickets' => '/pages/profile/tickets.php',
            'login' => '/pages/profile/login.php'
        ],
        'register' => [
            'index' => '/pages/register/index.php',
            'series' => '/pages/register/series.php',
            'event' => '/pages/register/event.php'
        ],
        'news' => [
            'index' => '/pages/news/index.php',
            'show' => '/pages/news/show.php',
            'tag' => '/pages/news/index.php',
            'event' => '/pages/news/index.php',
            'rider' => '/pages/news/index.php'
        ]
    ];

    // Check if this is a V1.0 section route
    if (isset($sectionRoutes[$section])) {
        // If second segment is numeric, it's an ID
        if (isset($segments[1]) && is_numeric($segments[1])) {
            $id = $segments[1];
            // Determine detail page based on section
            $detailPages = [
                'calendar' => 'event',
                'results' => 'event',
                'series' => 'show',
                'database' => 'rider',
                'ranking' => 'riders',
                'register' => 'series',  // /register/5 -> /register/series/5
                'news' => 'show'  // /news/slug -> /pages/news/show.php
            ];
            $subpage = $detailPages[$section] ?? 'index';
        } elseif (isset($segments[1]) && !is_numeric($segments[1])) {
            $subpage = $segments[1];
            $id = $segments[2] ?? null;

            // Special handling for news: if subpage is not a known route, treat as slug
            if ($section === 'news' && !isset($sectionRoutes['news'][$subpage])) {
                $subpage = 'show';
                $id = $segments[1]; // The slug
            }
        } else {
            $subpage = 'index';
        }

        $file = HUB_ROOT . ($sectionRoutes[$section][$subpage] ?? $sectionRoutes[$section]['index']);

        // For news show page, pass slug parameter
        $params = [];
        if ($id) {
            $params = ($section === 'news' && $subpage === 'show') ? ['slug' => $id] : ['id' => $id];
        }

        return [
            'page' => $section . '-' . $subpage,
            'section' => $section,
            'subpage' => $subpage,
            'params' => $params,
            'file' => $file
        ];
    }

    // Rider registration page (rider-register/123)
    if ($section === 'rider-register' && isset($segments[1])) {
        return [
            'page' => 'rider-register',
            'section' => 'database',
            'params' => ['id' => $segments[1]],
            'file' => HUB_ROOT . '/pages/rider-register.php'
        ];
    }

    // Legacy single-item pages (rider/123, event/456, club/789)
    $singlePages = ['rider', 'event', 'club'];
    if (in_array($section, $singlePages) && isset($segments[1])) {
        return [
            'page' => $section,
            'section' => $section === 'rider' || $section === 'club' ? 'database' : 'results',
            'params' => ['id' => $segments[1]],
            'file' => HUB_ROOT . '/pages/' . $section . '.php'
        ];
    }

    // Legacy list pages
    $legacyPages = [
        'riders' => ['section' => 'database', 'file' => '/pages/riders.php'],
        'clubs' => ['section' => 'database', 'file' => '/pages/clubs.php'],
        'club-points' => ['section' => 'series', 'file' => '/pages/club-points.php'],
        'results' => ['section' => 'results', 'file' => '/pages/results.php'],
        'ranking' => ['section' => 'ranking', 'file' => '/pages/ranking.php'],
        'achievements' => ['section' => 'database', 'file' => '/pages/achievements.php']
    ];

    if (isset($legacyPages[$section])) {
        return [
            'page' => $section,
            'section' => $legacyPages[$section]['section'],
            'params' => [],
            'file' => HUB_ROOT . $legacyPages[$section]['file']
        ];
    }

    // Dashboard
    if ($section === 'dashboard') {
        return ['page' => 'dashboard', 'section' => 'dashboard', 'params' => [], 'file' => HUB_ROOT . '/pages/dashboard.php'];
    }

    // 404
    return ['page' => '404', 'section' => null, 'params' => ['requested' => $raw], 'file' => HUB_ROOT . '/pages/404.php'];
}

function hub_is_ajax(): bool {
    return !empty($_SERVER['HTTP_X_REQUESTED_WITH']) &&
           strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest';
}

if (!function_exists('hub_is_nav_active')) {
    function hub_is_nav_active(string $navId, string $currentPage): bool {
        // Get section from page info
        global $pageInfo;
        $section = $pageInfo['section'] ?? null;

        if ($section === $navId) return true;

        // Legacy mappings
        if ($navId === 'calendar' && in_array($currentPage, ['calendar', 'calendar-event', 'calendar-index'])) return true;
        if ($navId === 'results' && in_array($currentPage, ['results', 'event', 'results-event'])) return true;
        if ($navId === 'series' && in_array($currentPage, ['series', 'series-index', 'series-show'])) return true;
        if ($navId === 'database' && in_array($currentPage, ['database', 'riders', 'rider', 'clubs', 'club', 'database-rider', 'database-club'])) return true;
        if ($navId === 'ranking' && str_starts_with($currentPage, 'ranking')) return true;
        if ($navId === 'profile' && str_starts_with($currentPage, 'profile')) return true;
        if ($navId === 'news' && str_starts_with($currentPage, 'news')) return true;

        return false;
    }
}
