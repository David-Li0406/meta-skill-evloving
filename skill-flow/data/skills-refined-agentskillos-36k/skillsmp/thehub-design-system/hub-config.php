<?php
/**
 * TheHUB Configuration
 *
 * Core configuration for TheHUB platform
 */

// Enable error reporting for debugging (remove in production)
error_reporting(E_ALL);
ini_set('display_errors', '1');

// ============================================================================
// DATABASE CONNECTION (uses parent config)
// ============================================================================
// Include the main config to get database connection
$parentConfig = __DIR__ . '/config.php';
if (file_exists($parentConfig)) {
    require_once $parentConfig;
} else {
    die('Error: Parent config.php not found at: ' . $parentConfig);
}

// Verify database connection exists
if (!isset($GLOBALS['pdo'])) {
    die('Error: Database connection not established');
}

// ============================================================================
// VERSION INFO
// ============================================================================
if (!defined('HUB_VERSION')) define('HUB_VERSION', '1.0.0');
if (!defined('CSS_VERSION')) define('CSS_VERSION', '1.0.0');
if (!defined('JS_VERSION')) define('JS_VERSION', '1.0.0');

if (!defined('HUB_ROOT')) define('HUB_ROOT', __DIR__);
if (!defined('HUB_URL')) define('HUB_URL', '');

// WooCommerce integration
if (!defined('WC_CHECKOUT_URL')) define('WC_CHECKOUT_URL', '/checkout');

// ============================================================================
// ROLE CONSTANTS (must be defined before functions that use them)
// ============================================================================
if (!defined('ROLE_RIDER')) {
    define('ROLE_RIDER', 1);
    define('ROLE_PROMOTOR', 2);
    define('ROLE_ADMIN', 3);
    define('ROLE_SUPER_ADMIN', 4);

    define('ROLE_NAMES', [
        ROLE_RIDER => 'Rider',
        ROLE_PROMOTOR => 'Promotor',
        ROLE_ADMIN => 'Admin',
        ROLE_SUPER_ADMIN => 'Super Admin'
    ]);
}

// ============================================================================
// NAVIGATION (6 main sections)
// ============================================================================
if (!defined('HUB_NAV')) {
    define('HUB_NAV', [
        ['id' => 'calendar', 'label' => 'Kalender', 'icon' => 'calendar', 'url' => '/calendar', 'aria' => 'Visa eventkalender'],
        ['id' => 'results', 'label' => 'Resultat', 'icon' => 'flag', 'url' => '/results', 'aria' => 'Visa tävlingsresultat'],
        ['id' => 'series', 'label' => 'Serier', 'icon' => 'trophy', 'url' => '/series', 'aria' => 'Visa tävlingsserier'],
        ['id' => 'news', 'label' => 'Nyheter', 'icon' => 'newspaper', 'url' => '/news', 'aria' => 'Visa nyheter och race reports'],
        ['id' => 'database', 'label' => 'Databas', 'icon' => 'search', 'url' => '/database', 'aria' => 'Sök åkare och klubbar'],
        ['id' => 'ranking', 'label' => 'Ranking', 'icon' => 'trending-up', 'url' => '/ranking', 'aria' => 'Visa ranking'],
        // 'Mitt' borttagen - nu i header istället
    ]);
}

// ============================================================================
// NAVIGATION HELPER
// ============================================================================
if (!function_exists('hub_is_nav_active')) {
    /**
     * Check if a navigation item should be marked as active
     *
     * @param string $navId The navigation item ID (calendar, results, series, etc.)
     * @param string $currentPage The current page identifier
     * @return bool True if this nav item should be active
     */
    function hub_is_nav_active(string $navId, string $currentPage): bool {
        // Get section from page info if available
        global $pageInfo;
        $section = $pageInfo['section'] ?? null;

        if ($section === $navId) return true;

        // Legacy mappings for backwards compatibility
        switch ($navId) {
            case 'calendar':
                return in_array($currentPage, ['calendar', 'calendar-event', 'calendar-index']);
            case 'results':
                return in_array($currentPage, ['results', 'event', 'results-event']);
            case 'series':
                return in_array($currentPage, ['series', 'series-index', 'series-show']);
            case 'database':
                return in_array($currentPage, ['database', 'riders', 'rider', 'clubs', 'club', 'database-rider', 'database-club']);
            case 'ranking':
                return str_starts_with($currentPage, 'ranking');
            case 'profile':
                return str_starts_with($currentPage, 'profile');
            default:
                return false;
        }
    }
}

// Valid pages/routes
if (!defined('HUB_VALID_PAGES')) {
    define('HUB_VALID_PAGES', [
        'dashboard',
        // Calendar
        'calendar', 'calendar-event',
        // Results
        'results', 'results-event',
        // Series
        'series', 'series-index', 'series-show',
        // Database
        'database', 'database-rider', 'database-club',
        // Ranking
        'ranking', 'ranking-riders', 'ranking-clubs', 'ranking-events',
        // Profile
        'profile', 'profile-edit', 'profile-children', 'profile-club-admin',
        'profile-registrations', 'profile-results', 'profile-receipts', 'profile-login',
        // Legacy support
        'series', 'series-single', 'event', 'riders', 'rider', 'clubs', 'club',
        '404'
    ]);
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================
if (!function_exists('hub_get_theme')) {
    function hub_get_theme(): string {
        $theme = $_COOKIE['hub_theme'] ?? 'auto';
        return in_array($theme, ['light', 'dark', 'auto']) ? $theme : 'auto';
    }
}

if (!function_exists('hub_asset')) {
    function hub_asset(string $path): string {
        $version = (strpos($path, '.css') !== false) ? CSS_VERSION : JS_VERSION;
        return HUB_URL . '/assets/' . $path . '?v=' . $version;
    }
}

if (!function_exists('hub_db')) {
    /**
     * Get database connection (PDO)
     * @return PDO
     */
    function hub_db(): PDO {
        return $GLOBALS['pdo'];
    }
}

// ============================================================================
// AUTHENTICATION FUNCTIONS
// ============================================================================

if (!function_exists('hub_is_logged_in')) {
    /**
     * Check if user is logged in (via WooCommerce/WordPress or session)
     */
    function hub_is_logged_in(): bool {
        if (function_exists('is_user_logged_in')) {
            return is_user_logged_in();
        }
        // Check admin login (from includes/auth.php)
        if (isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true) {
            return true;
        }
        // Check if login timestamp exists (set on successful login)
        if (isset($_SESSION['hub_logged_in_at']) && $_SESSION['hub_logged_in_at'] > 0) {
            return true;
        }
        // Check V3 session (rider id >= 0, 0 = admin fallback)
        if (isset($_SESSION['hub_user_id']) && is_numeric($_SESSION['hub_user_id'])) {
            return true;
        }
        // Check V2 rider session (backwards compatibility)
        if (isset($_SESSION['rider_id']) && $_SESSION['rider_id'] > 0) {
            return true;
        }
        // Check for "remember me" token and auto-login
        if (function_exists('rider_check_remember_token') && rider_check_remember_token()) {
            return true;
        }
        return false;
    }
}

if (!function_exists('hub_current_user')) {
    /**
     * Get current logged in user's rider profile
     */
    function hub_current_user(): ?array {
        if (!hub_is_logged_in()) return null;

        if (function_exists('wp_get_current_user')) {
            $wp_user = wp_get_current_user();
            return hub_get_rider_by_email($wp_user->user_email);
        }

        // Check admin session (from includes/auth.php)
        if (isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true) {
            // Map admin_role string to role_id
            $roleMap = [
                'super_admin' => ROLE_SUPER_ADMIN,
                'admin' => ROLE_ADMIN,
                'promotor' => ROLE_PROMOTOR,
            ];
            $adminRole = $_SESSION['admin_role'] ?? 'admin';
            $roleId = $roleMap[$adminRole] ?? ROLE_ADMIN;

            // Parse name into first/last
            $fullName = $_SESSION['admin_name'] ?? 'Admin';
            $nameParts = explode(' ', $fullName, 2);

            return [
                'id' => $_SESSION['admin_id'] ?? 0,
                'email' => $_SESSION['admin_email'] ?? '',
                'firstname' => $nameParts[0] ?? 'Admin',
                'lastname' => $nameParts[1] ?? '',
                'role_id' => $roleId,
                'is_admin' => $roleId >= ROLE_ADMIN ? 1 : 0,
                'active' => 1
            ];
        }

        // Check V3 session first
        if (isset($_SESSION['hub_user_id'])) {
            $userId = $_SESSION['hub_user_id'];

            // Admin fallback user (id=0) - return session data instead of DB lookup
            if ($userId === 0 || $userId === '0') {
                return [
                    'id' => 0,
                    'email' => $_SESSION['hub_user_email'] ?? 'admin@thehub.se',
                    'firstname' => 'Admin',
                    'lastname' => '',
                    'role_id' => $_SESSION['hub_user_role'] ?? ROLE_SUPER_ADMIN,
                    'is_admin' => 1,
                    'active' => 1
                ];
            }

            return hub_get_rider_by_id($userId);
        }

        // Check V2 rider session
        if (isset($_SESSION['rider_id'])) {
            return hub_get_rider_by_id($_SESSION['rider_id']);
        }

        return null;
    }
}

if (!function_exists('hub_get_rider_by_id')) {
    function hub_get_rider_by_id(int $id): ?array {
        $stmt = hub_db()->prepare("SELECT * FROM riders WHERE id = ?");
        $stmt->execute([$id]);
        return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
    }
}

if (!function_exists('hub_get_rider_by_email')) {
    function hub_get_rider_by_email(string $email): ?array {
        $stmt = hub_db()->prepare("SELECT * FROM riders WHERE email = ?");
        $stmt->execute([$email]);
        return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
    }
}

// ============================================================================
// PARENT/CHILD & PERMISSIONS
// ============================================================================

if (!function_exists('hub_is_parent_of')) {
    function hub_is_parent_of(int $parentId, int $childId): bool {
        try {
            $stmt = hub_db()->prepare("SELECT 1 FROM rider_parents WHERE parent_rider_id = ? AND child_rider_id = ?");
            $stmt->execute([$parentId, $childId]);
            return (bool) $stmt->fetch();
        } catch (PDOException $e) {
            // Table doesn't exist yet
            return false;
        }
    }
}

if (!function_exists('hub_get_linked_children')) {
    function hub_get_linked_children(int $parentId): array {
        try {
            $stmt = hub_db()->prepare("
                SELECT r.* FROM riders r
                JOIN rider_parents rp ON r.id = rp.child_rider_id
                WHERE rp.parent_rider_id = ?
            ");
            $stmt->execute([$parentId]);
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            // Table doesn't exist yet
            return [];
        }
    }
}

if (!function_exists('hub_can_edit_profile')) {
    function hub_can_edit_profile(int $profileId): bool {
        $user = hub_current_user();
        if (!$user) return false;
        if ($user['id'] === $profileId) return true;
        if (hub_is_parent_of($user['id'], $profileId)) return true;
        return false;
    }
}

if (!function_exists('hub_can_edit_club')) {
    function hub_can_edit_club(int $clubId): bool {
        $user = hub_current_user();
        if (!$user) return false;

        try {
            $stmt = hub_db()->prepare("SELECT 1 FROM club_admins WHERE rider_id = ? AND club_id = ?");
            $stmt->execute([$user['id'], $clubId]);
            return (bool) $stmt->fetch();
        } catch (PDOException $e) {
            // Table doesn't exist yet
            return false;
        }
    }
}

if (!function_exists('hub_get_admin_clubs')) {
    function hub_get_admin_clubs(int $riderId): array {
        try {
            $stmt = hub_db()->prepare("
                SELECT c.* FROM clubs c
                JOIN club_admins ca ON c.id = ca.club_id
                WHERE ca.rider_id = ?
            ");
            $stmt->execute([$riderId]);
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            // Table doesn't exist yet
            return [];
        }
    }
}

if (!function_exists('hub_is_admin')) {
    /**
     * Check if current user is an admin (role level 3+)
     */
    function hub_is_admin(?int $userId = null): bool {
        // Check legacy admin session (from includes/auth.php)
        if ($userId === null && isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true) {
            return true;
        }

        // Check session role first
        if ($userId === null && isset($_SESSION['hub_user_role'])) {
            return $_SESSION['hub_user_role'] >= ROLE_ADMIN;
        }

        // Check database role
        if ($userId !== null || isset($_SESSION['hub_user_id'])) {
            $checkId = $userId ?? $_SESSION['hub_user_id'];
            return hub_has_role(ROLE_ADMIN, $checkId);
        }

        $user = hub_current_user();
        if (!$user) return false;

        // Check role_id in riders table
        if (isset($user['role_id']) && $user['role_id'] >= ROLE_ADMIN) {
            return true;
        }

        // Fallback: check is_admin flag in riders table (legacy)
        if (isset($user['is_admin']) && $user['is_admin']) {
            return true;
        }

        // Check WordPress role if available
        if (function_exists('current_user_can')) {
            return current_user_can('manage_options') || current_user_can('edit_others_posts');
        }

        return false;
    }
}

if (!function_exists('hub_attempt_login')) {
    /**
     * Attempt to log in a user with email/password
     * Works with the riders table using password_hash
     * Also supports admin_users table and default admin login from config.php
     */
    function hub_attempt_login(string $email, string $password, bool $rememberMe = false): array {
        $pdo = hub_db();

        // NOTE: Remember me is handled in hub_set_user_session() where we
        // set $_SESSION['remember_me'] and extend the session cookie

        // =====================================================================
        // FALLBACK: Check default admin credentials from config.php
        // This allows login even if no rider accounts have passwords set
        // =====================================================================
        $defaultUsername = defined('DEFAULT_ADMIN_USERNAME') ? DEFAULT_ADMIN_USERNAME : null;
        $defaultPassword = defined('DEFAULT_ADMIN_PASSWORD') ? DEFAULT_ADMIN_PASSWORD : null;

        if ($defaultUsername && $defaultPassword) {
            // Admin can log in with username OR email = username (case-insensitive)
            $emailLower = strtolower($email);
            $usernameLower = strtolower($defaultUsername);
            if (($emailLower === $usernameLower || $emailLower === $usernameLower . '@thehub.se') && $password === $defaultPassword) {
                // Create admin session
                $adminUser = [
                    'id' => 0,
                    'email' => $defaultUsername . '@thehub.se',
                    'firstname' => 'Admin',
                    'lastname' => $defaultUsername,
                    'is_admin' => 1,
                    'role_id' => ROLE_SUPER_ADMIN
                ];
                hub_set_user_session($adminUser, [], $rememberMe);
                return ['success' => true, 'user' => $adminUser];
            }
        }

        // =====================================================================
        // Check admin_users table (by username or email)
        // =====================================================================
        try {
            $stmt = $pdo->prepare("
                SELECT id, username, email, password_hash, full_name, role, active
                FROM admin_users
                WHERE (username = ? OR email = ?)
                LIMIT 1
            ");
            $stmt->execute([$email, $email]);
            $adminUser = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($adminUser) {
                // Check if user is active
                if (!$adminUser['active']) {
                    return ['success' => false, 'error' => 'Kontot är inaktiverat. Kontakta administratören.'];
                }

                $passwordVerified = false;

                // First try admin_users password_hash if set
                if (!empty($adminUser['password_hash'])) {
                    $passwordVerified = password_verify($password, $adminUser['password_hash']);
                }

                // If admin_users password not set or didn't match, try linked rider password
                if (!$passwordVerified && !empty($adminUser['email'])) {
                    $riderStmt = $pdo->prepare("
                        SELECT id, password
                        FROM riders
                        WHERE email = ? AND password IS NOT NULL AND password != ''
                        LIMIT 1
                    ");
                    $riderStmt->execute([$adminUser['email']]);
                    $linkedRider = $riderStmt->fetch(PDO::FETCH_ASSOC);

                    if ($linkedRider && !empty($linkedRider['password'])) {
                        $passwordVerified = password_verify($password, $linkedRider['password']);
                    }
                }

                // Verify password
                if ($passwordVerified) {
                    // Map admin role to role_id
                    $roleMap = [
                        'super_admin' => ROLE_SUPER_ADMIN,
                        'admin' => ROLE_ADMIN,
                        'promotor' => ROLE_PROMOTOR,
                        'editor' => ROLE_RIDER,
                        'rider' => ROLE_RIDER
                    ];
                    $roleId = $roleMap[$adminUser['role']] ?? ROLE_RIDER;

                    // Parse full_name into firstname/lastname
                    $nameParts = explode(' ', $adminUser['full_name'] ?? $adminUser['username'], 2);
                    $firstname = $nameParts[0] ?? $adminUser['username'];
                    $lastname = $nameParts[1] ?? '';

                    $user = [
                        'id' => $adminUser['id'],
                        'email' => $adminUser['email'],
                        'firstname' => $firstname,
                        'lastname' => $lastname,
                        'is_admin' => $roleId >= ROLE_ADMIN ? 1 : 0,
                        'role_id' => $roleId,
                        'admin_user' => true,  // Flag to identify admin_users
                        'admin_role' => $adminUser['role']
                    ];

                    hub_set_user_session($user, [], $rememberMe);

                    // Update last login
                    $stmt = $pdo->prepare("UPDATE admin_users SET last_login = NOW() WHERE id = ?");
                    $stmt->execute([$adminUser['id']]);

                    return ['success' => true, 'user' => $user];
                }
                // Password didn't match - continue to check riders table
            }
        } catch (PDOException $e) {
            error_log("Admin login error: " . $e->getMessage());
            // Continue to riders table check
        }

        // =====================================================================
        // Normal rider login from database
        // Check ALL riders with this email (handles multiple profiles)
        // Also loads linked profiles after successful login
        // =====================================================================

        // Find all riders by email (primary accounts with passwords)
        $stmt = $pdo->prepare("
            SELECT id, email, password, firstname, lastname, is_admin, role_id, linked_to_rider_id
            FROM riders
            WHERE email = ? AND active = 1
            ORDER BY password IS NOT NULL DESC, id
        ");
        $stmt->execute([$email]);
        $riders = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($riders)) {
            return ['success' => false, 'error' => 'Ogiltig e-post eller lösenord.'];
        }

        // Try password against each matching rider profile (primary accounts)
        $hasActivatedAccount = false;
        foreach ($riders as $rider) {
            if (!empty($rider['password'])) {
                $hasActivatedAccount = true;
                if (password_verify($password, $rider['password'])) {
                    // Login successful - load all linked profiles
                    $linkedProfiles = [];

                    // Get all profiles linked to this primary account
                    $linkedStmt = $pdo->prepare("
                        SELECT id, firstname, lastname, birth_year, club_id
                        FROM riders
                        WHERE linked_to_rider_id = ? AND active = 1
                        ORDER BY lastname, firstname
                    ");
                    $linkedStmt->execute([$rider['id']]);
                    $linkedProfiles = $linkedStmt->fetchAll(PDO::FETCH_ASSOC);

                    // Also get profiles with same email (for backwards compatibility)
                    $sameEmailStmt = $pdo->prepare("
                        SELECT id, firstname, lastname, birth_year, club_id
                        FROM riders
                        WHERE email = ? AND id != ? AND linked_to_rider_id IS NULL AND active = 1
                        ORDER BY lastname, firstname
                    ");
                    $sameEmailStmt->execute([$rider['email'], $rider['id']]);
                    $sameEmailProfiles = $sameEmailStmt->fetchAll(PDO::FETCH_ASSOC);

                    // Merge linked profiles
                    $allLinkedIds = [$rider['id']];
                    foreach ($linkedProfiles as $lp) {
                        $allLinkedIds[] = $lp['id'];
                    }
                    foreach ($sameEmailProfiles as $sep) {
                        if (!in_array($sep['id'], $allLinkedIds)) {
                            $allLinkedIds[] = $sep['id'];
                            $linkedProfiles[] = $sep;
                        }
                    }

                    // Create session with linked profiles
                    hub_set_user_session($rider, $linkedProfiles, $rememberMe);

                    // Update last login
                    $stmt = $pdo->prepare("UPDATE riders SET last_login = NOW() WHERE id = ?");
                    $stmt->execute([$rider['id']]);

                    return ['success' => true, 'user' => $rider, 'linked_profiles' => $linkedProfiles];
                }
            }
        }

        // No password matched
        if ($hasActivatedAccount) {
            return ['success' => false, 'error' => 'Ogiltig e-post eller lösenord.'];
        } else {
            return ['success' => false, 'error' => 'Du har inte satt ett lösenord ännu. Klicka på "Aktivera konto" för att skapa ett.'];
        }
    }
}

if (!function_exists('hub_set_user_session')) {
    /**
     * Set user session after successful login
     * Sets both V3 hub_* variables AND admin_* variables for admin panel compatibility
     *
     * @param array $user Primary user data
     * @param array $linkedProfiles Optional array of linked rider profiles
     * @param bool $rememberMe If true, extends session to 30 days
     */
    function hub_set_user_session(array $user, array $linkedProfiles = [], bool $rememberMe = false): void {
        $roleId = (int) ($user['role_id'] ?? ROLE_RIDER);
        $userName = ($user['firstname'] ?? '') . ' ' . ($user['lastname'] ?? '');

        // V3 session variables
        $_SESSION['hub_user_id'] = $user['id'];
        $_SESSION['hub_user_email'] = $user['email'];
        $_SESSION['hub_user_name'] = $userName;
        $_SESSION['hub_user_role'] = $roleId;
        $_SESSION['hub_logged_in_at'] = time();

        // Remember me - CRITICAL for session persistence
        $_SESSION['remember_me'] = $rememberMe;
        if ($rememberMe) {
            // Extend session cookie to 30 days
            $lifetime = 30 * 24 * 60 * 60;
            $params = session_get_cookie_params();
            setcookie(
                session_name(),
                session_id(),
                [
                    'expires' => time() + $lifetime,
                    'path' => $params['path'],
                    'domain' => $params['domain'],
                    'secure' => $params['secure'],
                    'httponly' => $params['httponly'],
                    'samesite' => $params['samesite'] ?? 'Lax'
                ]
            );
        }

        // Store linked profiles for profile switching
        $_SESSION['hub_linked_profiles'] = $linkedProfiles;
        $_SESSION['hub_active_rider_id'] = $user['id']; // Currently active rider profile

        // Build list of all accessible rider IDs
        $allRiderIds = [$user['id']];
        foreach ($linkedProfiles as $profile) {
            $allRiderIds[] = $profile['id'];
        }
        $_SESSION['hub_all_rider_ids'] = $allRiderIds;

        // Backwards compatibility - is_admin based on role
        $_SESSION['hub_is_admin'] = $roleId >= ROLE_ADMIN;

        // Also set rider_* for backwards compatibility with V2 code
        $_SESSION['rider_id'] = $user['id'];
        $_SESSION['rider_email'] = $user['email'];
        $_SESSION['rider_name'] = $userName;

        // =====================================================================
        // ADMIN PANEL COMPATIBILITY
        // Set admin_* session variables so /admin/ pages recognize the login
        // For admin_users table: always set (they're admin panel users)
        // For riders table: only if role >= ROLE_ADMIN
        // =====================================================================
        $isAdminUser = !empty($user['admin_user']);  // Flag from admin_users table
        $hasAdminRole = $roleId >= ROLE_ADMIN;

        if ($isAdminUser || $hasAdminRole) {
            $_SESSION['admin_logged_in'] = true;
            $_SESSION['admin_id'] = $user['id'];
            $_SESSION['admin_username'] = $user['email'] ?? $user['username'] ?? '';
            $_SESSION['admin_name'] = $userName;
            $_SESSION['last_activity'] = time();

            // Use admin_role from user if available (from admin_users table)
            // Otherwise map from role_id
            if (!empty($user['admin_role'])) {
                $_SESSION['admin_role'] = $user['admin_role'];
            } else {
                $roleMap = [
                    ROLE_RIDER => 'rider',
                    ROLE_PROMOTOR => 'promotor',
                    ROLE_ADMIN => 'admin',
                    ROLE_SUPER_ADMIN => 'super_admin'
                ];
                $_SESSION['admin_role'] = $roleMap[$roleId] ?? 'rider';
            }
        }
    }
}

if (!function_exists('hub_logout')) {
    /**
     * Log out the current user
     * Clears all session types: V3, V2, and Admin
     */
    function hub_logout(): void {
        // Clear V3 session
        unset($_SESSION['hub_user_id']);
        unset($_SESSION['hub_user_email']);
        unset($_SESSION['hub_user_name']);
        unset($_SESSION['hub_user_role']);
        unset($_SESSION['hub_is_admin']);
        unset($_SESSION['hub_logged_in_at']);

        // Clear V2 rider session
        unset($_SESSION['rider_id']);
        unset($_SESSION['rider_email']);
        unset($_SESSION['rider_name']);

        // Clear admin session
        unset($_SESSION['admin_logged_in']);
        unset($_SESSION['admin_id']);
        unset($_SESSION['admin_username']);
        unset($_SESSION['admin_name']);
        unset($_SESSION['admin_role']);
        unset($_SESSION['last_activity']);
    }
}

if (!function_exists('hub_require_login')) {
    /**
     * Require user to be logged in, redirect to login if not
     */
    function hub_require_login(?string $redirect = null): void {
        if (!hub_is_logged_in()) {
            $redirect = $redirect ?? $_SERVER['REQUEST_URI'];
            header('Location: ' . HUB_URL . '/login?redirect=' . urlencode($redirect));
            exit;
        }
    }
}

if (!function_exists('hub_require_admin')) {
    /**
     * Require user to be admin, redirect if not
     */
    function hub_require_admin(): void {
        hub_require_login();

        if (!hub_is_admin()) {
            header('Location: ' . HUB_URL . '/?error=access_denied');
            exit;
        }
    }
}

// ============================================================================
// ROLE-BASED PERMISSION SYSTEM
// ============================================================================

if (!function_exists('hub_get_user_role')) {
    /**
     * Get user's role level
     */
    function hub_get_user_role(?int $userId = null): int {
        if ($userId === null) {
            // Check V3 hub session first
            if (isset($_SESSION['hub_user_role'])) {
                return $_SESSION['hub_user_role'];
            }

            // Fallback to admin session (from includes/auth.php login)
            if (isset($_SESSION['admin_role'])) {
                $roleMap = [
                    'super_admin' => ROLE_SUPER_ADMIN,
                    'admin' => ROLE_ADMIN,
                    'promotor' => ROLE_PROMOTOR,
                ];
                return $roleMap[$_SESSION['admin_role']] ?? ROLE_RIDER;
            }

            return ROLE_RIDER;
        }

        static $cache = [];
        if (!isset($cache[$userId])) {
            $stmt = hub_db()->prepare("SELECT role_id FROM riders WHERE id = ?");
            $stmt->execute([$userId]);
            $cache[$userId] = (int) ($stmt->fetchColumn() ?: ROLE_RIDER);
        }

        return $cache[$userId];
    }
}

if (!function_exists('hub_get_role_name')) {
    /**
     * Get role display name
     */
    function hub_get_role_name(int $roleId): string {
        return ROLE_NAMES[$roleId] ?? 'Okänd';
    }
}

if (!function_exists('hub_has_role')) {
    /**
     * Check if user has at least a certain role level
     */
    function hub_has_role(int $requiredRole, ?int $userId = null): bool {
        $userRole = hub_get_user_role($userId);
        return $userRole >= $requiredRole;
    }
}

if (!function_exists('hub_is_role')) {
    /**
     * Check if user is exactly a certain role
     */
    function hub_is_role(int $role, ?int $userId = null): bool {
        return hub_get_user_role($userId) === $role;
    }
}

if (!function_exists('hub_is_promotor')) {
    /**
     * Check if user is promotor or higher
     */
    function hub_is_promotor(?int $userId = null): bool {
        return hub_has_role(ROLE_PROMOTOR, $userId);
    }
}

if (!function_exists('hub_is_super_admin')) {
    /**
     * Check if user is super admin
     */
    function hub_is_super_admin(?int $userId = null): bool {
        return hub_has_role(ROLE_SUPER_ADMIN, $userId);
    }
}

if (!function_exists('hub_can_manage_event')) {
    /**
     * Check if user can manage a specific event
     */
    function hub_can_manage_event(int $eventId, ?int $userId = null): bool {
        $userId = $userId ?? ($_SESSION['hub_user_id'] ?? 0);

        if (!$userId) return false;

        // Admin and Super Admin can manage all events
        if (hub_has_role(ROLE_ADMIN, $userId)) {
            return true;
        }

        // Promotor - check specific assignment
        if (hub_is_promotor($userId)) {
            $pdo = hub_db();

            // Check direct event assignment
            $stmt = $pdo->prepare("SELECT 1 FROM promotor_events WHERE user_id = ? AND event_id = ?");
            $stmt->execute([$userId, $eventId]);
            if ($stmt->fetchColumn()) {
                return true;
            }

            // Check series assignment
            $stmt = $pdo->prepare("
                SELECT 1 FROM promotor_series ps
                JOIN events e ON e.series_id = ps.series_id
                WHERE ps.user_id = ? AND e.id = ?
            ");
            $stmt->execute([$userId, $eventId]);
            if ($stmt->fetchColumn()) {
                return true;
            }
        }

        return false;
    }
}

if (!function_exists('hub_can_manage_series')) {
    /**
     * Check if user can manage a specific series
     */
    function hub_can_manage_series(int $seriesId, ?int $userId = null): bool {
        $userId = $userId ?? ($_SESSION['hub_user_id'] ?? 0);

        if (!$userId) return false;

        // Admin and Super Admin can manage all series
        if (hub_has_role(ROLE_ADMIN, $userId)) {
            return true;
        }

        // Promotor - check specific assignment
        if (hub_is_promotor($userId)) {
            $stmt = hub_db()->prepare("SELECT 1 FROM promotor_series WHERE user_id = ? AND series_id = ?");
            $stmt->execute([$userId, $seriesId]);
            return (bool) $stmt->fetchColumn();
        }

        return false;
    }
}

if (!function_exists('hub_get_promotor_events')) {
    /**
     * Get all events a promotor can manage
     */
    function hub_get_promotor_events(int $userId): array {
        $pdo = hub_db();

        if (hub_has_role(ROLE_ADMIN, $userId)) {
            // Admin sees all events
            return $pdo->query("
                SELECT e.*, s.name as series_name
                FROM events e
                LEFT JOIN series s ON e.series_id = s.id
                WHERE e.date >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
                ORDER BY e.date DESC
            ")->fetchAll(PDO::FETCH_ASSOC);
        }

        // Promotor sees assigned events
        $stmt = $pdo->prepare("
            SELECT DISTINCT e.*, s.name as series_name,
                   CASE WHEN pe.id IS NOT NULL THEN 'event' ELSE 'series' END as assigned_via
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN promotor_events pe ON pe.event_id = e.id AND pe.user_id = ?
            LEFT JOIN promotor_series ps ON ps.series_id = e.series_id AND ps.user_id = ?
            WHERE (pe.id IS NOT NULL OR ps.id IS NOT NULL)
            ORDER BY e.date DESC
        ");
        $stmt->execute([$userId, $userId]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}

if (!function_exists('hub_require_role')) {
    /**
     * Require specific role level, redirect if not authorized
     */
    function hub_require_role(int $role, ?string $redirect = null): void {
        hub_require_login();

        if (!hub_has_role($role)) {
            $redirect = $redirect ?? HUB_URL . '/?error=access_denied';
            header('Location: ' . $redirect);
            exit;
        }
    }
}

if (!function_exists('hub_require_event_access')) {
    /**
     * Require access to specific event
     */
    function hub_require_event_access(int $eventId): void {
        hub_require_login();

        if (!hub_can_manage_event($eventId)) {
            header('Location: ' . HUB_URL . '/admin?error=no_access');
            exit;
        }
    }
}

// ============================================================================
// DATE FORMATTING (strftime is deprecated in PHP 8.1+)
// ============================================================================

if (!function_exists('hub_month_short')) {
    /**
     * Get short Swedish month name (jan, feb, mar, etc.)
     */
    function hub_month_short($date): string {
        $months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'];
        $timestamp = is_numeric($date) ? $date : strtotime($date);
        return $months[(int)date('n', $timestamp) - 1];
    }
}

if (!function_exists('hub_month_full')) {
    /**
     * Get full Swedish month name (januari, februari, etc.)
     */
    function hub_month_full($date): string {
        $months = ['januari', 'februari', 'mars', 'april', 'maj', 'juni', 'juli', 'augusti', 'september', 'oktober', 'november', 'december'];
        $timestamp = is_numeric($date) ? $date : strtotime($date);
        return $months[(int)date('n', $timestamp) - 1];
    }
}

if (!function_exists('hub_day_short')) {
    /**
     * Get short Swedish day name (mån, tis, ons, etc.)
     */
    function hub_day_short($date): string {
        $days = ['sön', 'mån', 'tis', 'ons', 'tor', 'fre', 'lör'];
        $timestamp = is_numeric($date) ? $date : strtotime($date);
        return $days[(int)date('w', $timestamp)];
    }
}

if (!function_exists('hub_format_month_year')) {
    /**
     * Format date as "Januari 2024"
     */
    function hub_format_month_year($date): string {
        $timestamp = is_numeric($date) ? $date : strtotime($date);
        return ucfirst(hub_month_full($timestamp)) . ' ' . date('Y', $timestamp);
    }
}

// ============================================================================
// IMAGE HANDLING
// ============================================================================

if (!function_exists('hub_get_image')) {
    /**
     * Get image URL with theme variant support
     * Returns the appropriate image URL for the current theme, or data attributes
     * for JavaScript to handle theme switching.
     *
     * @param string $type Type of image (series, club, sponsor, site)
     * @param int $entityId ID of the entity
     * @param string $fallback Fallback URL if no image found
     * @return string Image URL or data attributes
     */
    function hub_get_image(string $type, int $entityId, string $fallback = ''): string {
        static $cache = [];
        $cacheKey = "{$type}-{$entityId}";

        if (!isset($cache[$cacheKey])) {
            try {
                $stmt = hub_db()->prepare("
                    SELECT variant, filename FROM images
                    WHERE type = ? AND entity_id = ?
                ");
                $stmt->execute([$type, $entityId]);
                $cache[$cacheKey] = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);
            } catch (Exception $e) {
                $cache[$cacheKey] = [];
            }
        }

        $images = $cache[$cacheKey];
        if (empty($images)) {
            return $fallback;
        }

        $default = $images['default'] ?? '';
        $light = $images['light'] ?? $default;
        $dark = $images['dark'] ?? $default;

        // If only one image or same for both, return simple URL
        if ($light === $dark && $default) {
            return HUB_URL . '/uploads/images/' . $default;
        }

        // Return the default/light version as src, with data attributes for JS
        $src = HUB_URL . '/uploads/images/' . ($light ?: $default);
        return $src;
    }
}

if (!function_exists('hub_get_image_attrs')) {
    /**
     * Get image attributes for theme-aware images
     * Use this when you need data attributes for JavaScript theme switching
     *
     * @param string $type Type of image
     * @param int $entityId ID of the entity
     * @param string $fallback Fallback URL
     * @return array Array with 'src', 'light', 'dark' keys
     */
    function hub_get_image_attrs(string $type, int $entityId, string $fallback = ''): array {
        static $cache = [];
        $cacheKey = "{$type}-{$entityId}";

        if (!isset($cache[$cacheKey])) {
            try {
                $stmt = hub_db()->prepare("
                    SELECT variant, filename FROM images
                    WHERE type = ? AND entity_id = ?
                ");
                $stmt->execute([$type, $entityId]);
                $cache[$cacheKey] = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);
            } catch (Exception $e) {
                $cache[$cacheKey] = [];
            }
        }

        $images = $cache[$cacheKey];
        if (empty($images)) {
            return ['src' => $fallback, 'light' => '', 'dark' => ''];
        }

        $baseUrl = HUB_URL . '/uploads/images/';
        $default = isset($images['default']) ? $baseUrl . $images['default'] : $fallback;
        $light = isset($images['light']) ? $baseUrl . $images['light'] : $default;
        $dark = isset($images['dark']) ? $baseUrl . $images['dark'] : $default;

        return [
            'src' => $light ?: $default,
            'light' => $light,
            'dark' => $dark
        ];
    }
}
