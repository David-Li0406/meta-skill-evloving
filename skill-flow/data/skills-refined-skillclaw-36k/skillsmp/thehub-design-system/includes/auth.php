<?php
/**
 * Authentication and session management
 */

// Ensure redirect function exists (fallback if helpers.php not loaded)
if (!function_exists('redirect')) {
    function redirect($url) {
        header('Location: ' . $url);
        exit;
    }
}

// Start session if not already started
if (session_status() === PHP_SESSION_NONE) {
    // Configure secure session parameters
    session_set_cookie_params([
        'lifetime' => defined('SESSION_LIFETIME') ? SESSION_LIFETIME : 86400,
        'path' => '/',
        'domain' => '',
        // Auto-detect HTTPS - secure flag only if using SSL
        'secure' => isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on',
        'httponly' => true,   // Prevent JavaScript access
        'samesite' => 'Lax' // CSRF protection (Lax allows same-site navigation)
    ]);

    if (defined('SESSION_NAME')) {
        session_name(SESSION_NAME);
    } else {
        session_name('thehub_session');
    }

    session_start();

    // Regenerate session ID on login to prevent fixation attacks
    if (isset($_SESSION['admin_logged_in']) && !isset($_SESSION['session_regenerated'])) {
        session_regenerate_id(true);
        $_SESSION['session_regenerated'] = true;
    }
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true;
}

/**
 * Require login
 */
function requireLogin() {
    // Prevent caching of admin pages
    header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
    header("Cache-Control: post-check=0, pre-check=0", false);
    header("Pragma: no-cache");

    if (!isLoggedIn()) {
        redirect('/admin/login.php');
    }

    // Session activity timeout
    // If "remember me" is set, use 30 days, otherwise 30 minutes
    $rememberMe = $_SESSION['remember_me'] ?? false;
    if ($rememberMe) {
        $timeout = 30 * 24 * 60 * 60; // 30 days
    } else {
        $timeout = defined('SESSION_ACTIVITY_TIMEOUT') ? SESSION_ACTIVITY_TIMEOUT : 1800; // 30 minutes
    }

    if (isset($_SESSION['last_activity']) && (time() - $_SESSION['last_activity'] > $timeout)) {
        logout();
        redirect('/admin/login.php?timeout=1');
    }
    $_SESSION['last_activity'] = time();

    // Refresh session cookie if remember me (extend expiry on each page load)
    if ($rememberMe) {
        setRememberMeSession();
    }
}

/**
 * Check if login attempts are rate limited
 */
function isLoginRateLimited($username) {
    $key = 'login_attempts_' . md5($username . $_SERVER['REMOTE_ADDR']);

    if (!isset($_SESSION[$key])) {
        $_SESSION[$key] = ['count' => 0, 'first_attempt' => time()];
    }

    $attempts = &$_SESSION[$key];

    // Reset after 15 minutes
    if (time() - $attempts['first_attempt'] > 900) {
        $attempts = ['count' => 0, 'first_attempt' => time()];
    }

    // Allow max 5 attempts per 15 minutes
    return $attempts['count'] >= 5;
}

/**
 * Record a failed login attempt
 */
function recordFailedLogin($username) {
    $key = 'login_attempts_' . md5($username . $_SERVER['REMOTE_ADDR']);

    if (!isset($_SESSION[$key])) {
        $_SESSION[$key] = ['count' => 0, 'first_attempt' => time()];
    }

    $_SESSION[$key]['count']++;
}

/**
 * Clear login attempts after successful login
 */
function clearLoginAttempts($username) {
    $key = 'login_attempts_' . md5($username . $_SERVER['REMOTE_ADDR']);
    unset($_SESSION[$key]);
}

/**
 * Login user
 * @param string $username
 * @param string $password
 * @param bool $rememberMe - If true, extends session to 30 days
 */
function login($username, $password, $rememberMe = false) {
    // Check for rate limiting
    if (isLoginRateLimited($username)) {
        return false;
    }

    // Check default admin credentials from config
    // WARNING: Change these in .env file for production!
    $defaultUsername = defined('DEFAULT_ADMIN_USERNAME') ? DEFAULT_ADMIN_USERNAME : 'admin';
    $defaultPassword = defined('DEFAULT_ADMIN_PASSWORD') ? DEFAULT_ADMIN_PASSWORD : 'admin';

    // Use constant-time comparison and hashed password for default admin
    $defaultPasswordHash = defined('DEFAULT_ADMIN_PASSWORD_HASH')
        ? DEFAULT_ADMIN_PASSWORD_HASH
        : password_hash($defaultPassword, PASSWORD_DEFAULT);

    if ($username === $defaultUsername && password_verify($password, $defaultPasswordHash)) {
        // Regenerate session ID to prevent session fixation
        session_regenerate_id(true);

        $_SESSION['admin_logged_in'] = true;
        $_SESSION['admin_id'] = 1;
        $_SESSION['admin_username'] = 'admin';
        $_SESSION['admin_role'] = 'super_admin';
        $_SESSION['admin_name'] = 'Administrator';
        $_SESSION['session_regenerated'] = true;
        $_SESSION['last_activity'] = time();
        $_SESSION['remember_me'] = $rememberMe;

        // If remember me, extend session cookie
        if ($rememberMe) {
            setRememberMeSession();
        }

        clearLoginAttempts($username);
        return true;
    }

    // Try database authentication
    global $pdo;

    if (!$pdo) {
        return false;
    }

    try {
        $sql = "SELECT id, username, password_hash, email, full_name, role, active
                FROM admin_users
                WHERE username = ? AND active = 1
                LIMIT 1";

        $stmt = $pdo->prepare($sql);
        $stmt->execute([$username]);
        $user = $stmt->fetch();

        // Also try to find by email (for promotors using their rider email as username)
        if (!$user) {
            $stmt = $pdo->prepare("SELECT id, username, password_hash, email, full_name, role, active
                FROM admin_users
                WHERE email = ? AND active = 1
                LIMIT 1");
            $stmt->execute([$username]);
            $user = $stmt->fetch();
        }

        if (!$user) {
            recordFailedLogin($username);
            return false;
        }

        $passwordVerified = false;

        // First try admin_users password_hash if set
        if (!empty($user['password_hash'])) {
            $passwordVerified = password_verify($password, $user['password_hash']);
        }

        // If admin_users password not set or didn't match, try linked rider password
        if (!$passwordVerified && !empty($user['email'])) {
            $riderStmt = $pdo->prepare("
                SELECT id, password
                FROM riders
                WHERE email = ? AND password IS NOT NULL AND password != ''
                LIMIT 1
            ");
            $riderStmt->execute([$user['email']]);
            $linkedRider = $riderStmt->fetch();

            if ($linkedRider && !empty($linkedRider['password'])) {
                $passwordVerified = password_verify($password, $linkedRider['password']);
            }
        }

        if (!$passwordVerified) {
            recordFailedLogin($username);
            return false;
        }

        // Regenerate session ID to prevent session fixation
        session_regenerate_id(true);

        // Set session
        $_SESSION['admin_logged_in'] = true;
        $_SESSION['admin_id'] = $user['id'];
        $_SESSION['admin_username'] = $user['username'];
        $_SESSION['admin_email'] = $user['email'] ?? '';
        $_SESSION['admin_role'] = $user['role'];
        $_SESSION['admin_name'] = $user['full_name'] ?? $user['username'];
        $_SESSION['session_regenerated'] = true;
        $_SESSION['last_activity'] = time();
        $_SESSION['remember_me'] = $rememberMe;

        // If remember me, extend session cookie
        if ($rememberMe) {
            setRememberMeSession();
        }

        // Update last login
        $stmt = $pdo->prepare("UPDATE admin_users SET last_login = NOW() WHERE id = ?");
        $stmt->execute([$user['id']]);

        clearLoginAttempts($username);
        return true;
    } catch (PDOException $e) {
        error_log("Login error: " . $e->getMessage());
        recordFailedLogin($username);
        return false;
    }
}

/**
 * Set extended session for "Remember Me"
 * Extends session cookie to 30 days
 */
function setRememberMeSession() {
    $lifetime = 30 * 24 * 60 * 60; // 30 days in seconds

    // Update session cookie parameters
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

/**
 * Logout user
 */
function logout() {
    $_SESSION = [];

    // Delete session cookie
    if (ini_get("session.use_cookies")) {
        $params = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000,
            $params["path"], $params["domain"],
            $params["secure"], $params["httponly"]
        );
    }

    // Destroy session
    session_destroy();
}

/**
 * Get current admin user
 */
function getCurrentAdmin() {
    if (!isLoggedIn()) {
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
 * Check if user has role
 * Role hierarchy: rider(1) < promotor(2) < admin(3) < super_admin(4)
 */
function hasRole($role) {
    if (!isLoggedIn()) {
        return false;
    }

    $currentRole = $_SESSION['admin_role'] ?? null;

    // Updated role hierarchy with new roles
    $roles = [
        'rider' => 1,
        'promotor' => 2,
        'admin' => 3,
        'super_admin' => 4,
        // Legacy support
        'editor' => 1
    ];

    return ($roles[$currentRole] ?? 0) >= ($roles[$role] ?? 999);
}

/**
 * Check if user is exactly a specific role (not higher)
 */
function isRole($role) {
    if (!isLoggedIn()) {
        return false;
    }
    return ($_SESSION['admin_role'] ?? null) === $role;
}

/**
 * Check if user has a specific permission
 */
function hasPermission($permissionName) {
    if (!isLoggedIn()) {
        return false;
    }

    // Super admin has all permissions
    if (isRole('super_admin')) {
        return true;
    }

    global $pdo;
    if (!$pdo) {
        return false;
    }

    try {
        $role = $_SESSION['admin_role'] ?? null;
        $sql = "SELECT 1 FROM role_permissions rp
                JOIN permissions p ON rp.permission_id = p.id
                WHERE rp.role = ? AND p.name = ?
                LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$role, $permissionName]);
        return $stmt->fetch() !== false;
    } catch (PDOException $e) {
        error_log("Permission check error: " . $e->getMessage());
        return false;
    }
}

/**
 * Check if promotor has access to a specific event
 */
function canAccessEvent($eventId) {
    if (!isLoggedIn()) {
        return false;
    }

    // Super admin and admin can access all events
    if (hasRole('admin')) {
        return true;
    }

    // Promotors can only access assigned events
    if (!isRole('promotor')) {
        return false;
    }

    global $pdo;
    if (!$pdo) {
        return false;
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;
        $sql = "SELECT 1 FROM promotor_events
                WHERE user_id = ? AND event_id = ?
                LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId, $eventId]);
        return $stmt->fetch() !== false;
    } catch (PDOException $e) {
        error_log("Event access check error: " . $e->getMessage());
        return false;
    }
}

/**
 * Check if promotor can access a specific series
 * Returns true if user is admin OR if promotor is linked via promotor_series
 */
function canAccessSeries($seriesId) {
    if (!isLoggedIn()) {
        return false;
    }

    // Admin and above can access any series
    if (hasRole('admin')) {
        return true;
    }

    // Promotors can only access assigned series
    if (!isRole('promotor')) {
        return false;
    }

    global $pdo;
    if (!$pdo) {
        return false;
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;
        $sql = "SELECT 1 FROM promotor_series
                WHERE user_id = ? AND series_id = ?
                LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId, $seriesId]);
        return $stmt->fetch() !== false;
    } catch (PDOException $e) {
        error_log("Series access check error: " . $e->getMessage());
        return false;
    }
}

/**
 * Get all series a promotor can access
 */
function getPromotorSeries() {
    if (!isLoggedIn()) {
        return [];
    }

    global $pdo;
    if (!$pdo) {
        return [];
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;
        $sql = "SELECT s.*, ps.can_edit, ps.can_manage_results, ps.can_manage_registrations
                FROM series s
                JOIN promotor_series ps ON s.id = ps.series_id
                WHERE ps.user_id = ?
                ORDER BY s.year DESC, s.name ASC";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        error_log("Get promotor series error: " . $e->getMessage());
        return [];
    }
}

/**
 * Get all events a promotor can access
 */
function getPromotorEvents() {
    if (!isLoggedIn()) {
        return [];
    }

    global $pdo;
    if (!$pdo) {
        return [];
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;
        $sql = "SELECT e.*, pe.can_edit, pe.can_manage_results, pe.can_manage_registrations
                FROM events e
                JOIN promotor_events pe ON e.id = pe.event_id
                WHERE pe.user_id = ?
                ORDER BY e.date DESC";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        error_log("Get promotor events error: " . $e->getMessage());
        return [];
    }
}

/**
 * Check if rider user can edit their own profile
 */
function canEditRiderProfile($riderId) {
    if (!isLoggedIn()) {
        return false;
    }

    // Admin and above can edit any profile
    if (hasRole('admin')) {
        return true;
    }

    global $pdo;
    if (!$pdo) {
        return false;
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;
        $sql = "SELECT can_edit_profile FROM rider_profiles
                WHERE user_id = ? AND rider_id = ? AND can_edit_profile = 1
                LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId, $riderId]);
        return $stmt->fetch() !== false;
    } catch (PDOException $e) {
        error_log("Rider profile access check error: " . $e->getMessage());
        return false;
    }
}

/**
 * Check if user can manage a specific club
 * Checks both club_admins table and legacy rider_profiles.can_manage_club
 */
function canManageClub($clubId) {
    if (!isLoggedIn()) {
        return false;
    }

    // Admin and above can manage any club
    if (hasRole('admin')) {
        return true;
    }

    global $pdo;
    if (!$pdo) {
        return false;
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;

        // Check club_admins table first (new system)
        $sql = "SELECT can_edit_profile FROM club_admins
                WHERE user_id = ? AND club_id = ?
                LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId, $clubId]);
        $clubAdmin = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($clubAdmin && $clubAdmin['can_edit_profile']) {
            return true;
        }

        // Fallback to legacy rider_profiles system
        $sql = "SELECT 1 FROM rider_profiles rp
                JOIN riders r ON rp.rider_id = r.id
                WHERE rp.user_id = ? AND r.club_id = ? AND rp.can_manage_club = 1
                LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId, $clubId]);
        return $stmt->fetch() !== false;
    } catch (PDOException $e) {
        error_log("Club access check error: " . $e->getMessage());
        return false;
    }
}

/**
 * Get club admin permissions for a user and club
 * Returns permissions array or false if no access
 */
function getClubAdminPermissions($clubId) {
    if (!isLoggedIn()) {
        return false;
    }

    // Admin and above have all permissions
    if (hasRole('admin')) {
        return [
            'can_edit_profile' => true,
            'can_upload_logo' => true,
            'can_manage_members' => true
        ];
    }

    global $pdo;
    if (!$pdo) {
        return false;
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;

        $sql = "SELECT can_edit_profile, can_upload_logo, can_manage_members
                FROM club_admins
                WHERE user_id = ? AND club_id = ?
                LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId, $clubId]);
        $perms = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($perms) {
            return [
                'can_edit_profile' => (bool)$perms['can_edit_profile'],
                'can_upload_logo' => (bool)$perms['can_upload_logo'],
                'can_manage_members' => (bool)$perms['can_manage_members']
            ];
        }

        return false;
    } catch (PDOException $e) {
        error_log("Get club admin permissions error: " . $e->getMessage());
        return false;
    }
}

/**
 * Get all clubs a user can manage
 */
function getUserManagedClubs() {
    if (!isLoggedIn()) {
        return [];
    }

    global $pdo;
    if (!$pdo) {
        return [];
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;

        // If admin, they can manage all clubs
        if (hasRole('admin')) {
            $sql = "SELECT id, name, short_name, logo_url, city, country, active
                    FROM clubs
                    ORDER BY name";
            $stmt = $pdo->prepare($sql);
            $stmt->execute();
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        }

        // Get clubs from club_admins table
        $sql = "SELECT c.id, c.name, c.short_name, c.logo_url, c.city, c.country, c.active,
                       ca.can_edit_profile, ca.can_upload_logo, ca.can_manage_members
                FROM clubs c
                JOIN club_admins ca ON c.id = ca.club_id
                WHERE ca.user_id = ?
                ORDER BY c.name";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        error_log("Get user managed clubs error: " . $e->getMessage());
        return [];
    }
}

/**
 * Check if user can access a specific admin page
 */
function canAccessPage($pageKey) {
    if (!isLoggedIn()) {
        return false;
    }

    // Super admin can access all pages
    if (isRole('super_admin')) {
        return true;
    }

    global $pdo;
    if (!$pdo) {
        return false;
    }

    try {
        $userId = $_SESSION['admin_id'] ?? null;
        $currentRole = $_SESSION['admin_role'] ?? null;

        // First check if there's a specific override for this user
        $sql = "SELECT upa.has_access FROM user_page_access upa
                JOIN admin_pages ap ON upa.page_id = ap.id
                WHERE upa.user_id = ? AND ap.page_key = ?
                LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$userId, $pageKey]);
        $override = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($override !== false) {
            return (bool)$override['has_access'];
        }

        // Check based on role minimum requirement
        $roles = ['rider' => 1, 'promotor' => 2, 'admin' => 3, 'super_admin' => 4];
        $sql = "SELECT min_role FROM admin_pages WHERE page_key = ? AND is_active = 1 LIMIT 1";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$pageKey]);
        $page = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($page === false) {
            return false;
        }

        return ($roles[$currentRole] ?? 0) >= ($roles[$page['min_role']] ?? 999);
    } catch (PDOException $e) {
        error_log("Page access check error: " . $e->getMessage());
        return false;
    }
}

/**
 * Require specific role to continue
 */
function requireRole($role) {
    if (!hasRole($role)) {
        http_response_code(403);
        die('Access denied: Insufficient permissions');
    }
}

/**
 * Require Analytics access
 * Access granted if: super_admin OR has 'statistics' permission
 */
function requireAnalyticsAccess() {
    requireLogin();

    // Super admin always has access
    if (isRole('super_admin')) {
        return true;
    }

    // Check for statistics permission
    if (hasPermission('statistics')) {
        return true;
    }

    // No access
    http_response_code(403);
    die('Access denied: Analytics kraver super_admin eller statistics-behorighet');
}

/**
 * Check if user has Analytics access (without dying)
 * @return bool
 */
function hasAnalyticsAccess() {
    if (!isLoggedIn()) {
        return false;
    }

    // Super admin always has access
    if (isRole('super_admin')) {
        return true;
    }

    // Check for statistics permission
    return hasPermission('statistics');
}

/**
 * Require permission to continue
 */
function requirePermission($permissionName) {
    if (!hasPermission($permissionName)) {
        http_response_code(403);
        die('Access denied: Missing permission - ' . htmlspecialchars($permissionName));
    }
}

// ==============================================
// LEGACY FUNCTION ALIASES
// For backward compatibility with old code
// ==============================================

/**
 * Alias for requireLogin()
 */
function require_admin() {
    return requireLogin();
}

/**
 * Alias for requireLogin() - camelCase version
 */
function requireAdmin() {
    return requireLogin();
}

/**
 * Alias for isLoggedIn()
 */
function is_admin() {
    return isLoggedIn();
}

/**
 * Alias for login()
 */
function login_admin($username, $password) {
    return login($username, $password);
}

/**
 * Alias for logout()
 */
function logout_admin() {
    return logout();
}

/**
 * Alias for getCurrentAdmin()
 */
function get_admin_user() {
    return getCurrentAdmin();
}

/**
 * Alias for hasRole()
 */
function has_admin_role($role) {
    return hasRole($role);
}

// ==============================================
// CSRF PROTECTION FUNCTIONS
// ==============================================

/**
 * Generate CSRF token
 */
function generate_csrf_token() {
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Verify CSRF token
 */
function verify_csrf_token($token) {
    if (!isset($_SESSION['csrf_token'])) {
        return false;
    }
    return hash_equals($_SESSION['csrf_token'], $token);
}

/**
 * Check CSRF token from POST request
 */
function check_csrf() {
    $token = $_POST['csrf_token'] ?? '';
    
    if (!verify_csrf_token($token)) {
        die('CSRF token validation failed');
    }
}

/**
 * Generate CSRF field for forms
 */
function csrf_field() {
    $token = generate_csrf_token();
    return '<input type="hidden" name="csrf_token" value="' . htmlspecialchars($token) . '">';
}

/**
 * Get CSRF token (for AJAX)
 */
function get_csrf_token() {
    return generate_csrf_token();
}

// ==============================================
// FLASH MESSAGE FUNCTIONS
// ==============================================

/**
 * Set flash message
 */
function set_flash($type, $message) {
    if (!isset($_SESSION['flash'])) {
        $_SESSION['flash'] = [];
    }
    $_SESSION['flash'][$type] = $message;
}

/**
 * Get and clear flash message
 */
function get_flash($type) {
    if (!isset($_SESSION['flash'][$type])) {
        return null;
    }
    
    $message = $_SESSION['flash'][$type];
    unset($_SESSION['flash'][$type]);
    
    return $message;
}

/**
 * Check if flash message exists
 */
function has_flash($type) {
    return isset($_SESSION['flash'][$type]);
}

/**
 * Get all flash messages and clear them
 */
function get_all_flashes() {
    $flashes = $_SESSION['flash'] ?? [];
    unset($_SESSION['flash']);
    return $flashes;
}