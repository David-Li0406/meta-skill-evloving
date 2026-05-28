<?php
/**
 * TheHUB Icon-Only Navigation
 * Simplified sidebar navigation with icon-only design (72px width)
 * Using Lucide SVG icons
 */

$current_page = basename($_SERVER['PHP_SELF']);
$current_path = $_SERVER['PHP_SELF'];

// Check user roles properly
$is_logged_in = isLoggedIn();
$is_promotor = hasRole('promotor');  // promotor or higher
$is_admin = hasRole('admin');        // admin or higher
$is_super_admin = hasRole('super_admin');

/**
 * Get Lucide SVG icon
 */
function nav_icon($name, $class = 'sidebar-icon-svg') {
    $icons = [
        'home' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
        'calendar' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>',
        'trophy' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>',
        'flag' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/></svg>',
        'award' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>',
        'users' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        'building' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/></svg>',
        'trending-up' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
        'layout-dashboard' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>',
        'calendar-check' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="m9 16 2 2 4-4"/></svg>',
        'medal' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15"/><path d="M11 12 5.12 2.2"/><path d="m13 12 5.88-9.8"/><path d="M8 7h8"/><circle cx="12" cy="17" r="5"/><path d="M12 18v-2h-.5"/></svg>',
        'sliders' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/><line x1="2" x2="6" y1="14" y2="14"/><line x1="10" x2="14" y1="8" y2="8"/><line x1="18" x2="22" y1="16" y2="16"/></svg>',
        'upload' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>',
        'settings' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>',
        'log-out' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>',
        'log-in' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" x2="3" y1="12" y2="12"/></svg>',
    ];

    $svg = $icons[$name] ?? $icons['home'];
    return '<span class="sidebar-icon ' . $class . '" aria-hidden="true">' . $svg . '</span>';
}
?>

<aside class="sidebar" role="navigation" aria-label="Huvudnavigering">
    <!-- Logo from branding settings -->
    <?php
    $sidebarLogo = getBranding('logos.sidebar');
    if ($sidebarLogo):
    ?>
    <a href="/" class="sidebar-logo" aria-label="TheHUB Hem">
        <img src="<?= h($sidebarLogo) ?>" alt="TheHUB" width="40" height="40">
    </a>
    <?php endif; ?>

    <nav class="sidebar-nav">
        <!-- PUBLIC NAVIGATION -->
        <a href="/"
           class="sidebar-link<?= $current_page == 'index.php' && strpos($current_path, '/admin/') === false ? ' is-active' : '' ?>"
           aria-label="Hem"
           <?= $current_page == 'index.php' && strpos($current_path, '/admin/') === false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('home') ?>
            <span class="sidebar-label">Hem</span>
        </a>

        <a href="/calendar"
           class="sidebar-link<?= $current_page == 'events.php' && strpos($current_path, '/admin/') === false ? ' is-active' : '' ?>"
           aria-label="Kalender"
           <?= $current_page == 'events.php' && strpos($current_path, '/admin/') === false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('calendar') ?>
            <span class="sidebar-label">Kalender</span>
        </a>

        <a href="/results"
           class="sidebar-link<?= $current_page == 'results.php' && strpos($current_path, '/admin/') === false ? ' is-active' : '' ?>"
           aria-label="Resultat"
           <?= $current_page == 'results.php' && strpos($current_path, '/admin/') === false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('flag') ?>
            <span class="sidebar-label">Resultat</span>
        </a>

        <a href="/series"
           class="sidebar-link<?= $current_page == 'series.php' && strpos($current_path, '/admin/') === false ? ' is-active' : '' ?>"
           aria-label="Serier"
           <?= $current_page == 'series.php' && strpos($current_path, '/admin/') === false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('trophy') ?>
            <span class="sidebar-label">Serier</span>
        </a>

        <a href="/database"
           class="sidebar-link<?= $current_page == 'riders.php' && strpos($current_path, '/admin/') === false ? ' is-active' : '' ?>"
           aria-label="Databas"
           <?= $current_page == 'riders.php' && strpos($current_path, '/admin/') === false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('users') ?>
            <span class="sidebar-label">Databas</span>
        </a>

        <a href="/ranking"
           class="sidebar-link<?= strpos($current_path, '/ranking/') !== false && strpos($current_path, '/admin/') === false ? ' is-active' : '' ?>"
           aria-label="Ranking"
           <?= strpos($current_path, '/ranking/') !== false && strpos($current_path, '/admin/') === false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('trending-up') ?>
            <span class="sidebar-label">Ranking</span>
        </a>

        <?php if ($is_promotor && !$is_admin): ?>
        <!-- PROMOTOR NAVIGATION (promotor only, not admin/super_admin) -->
        <div class="sidebar-divider"></div>

        <a href="/admin/dashboard.php"
           class="sidebar-link<?= strpos($current_path, '/admin/dashboard.php') !== false ? ' is-active' : '' ?>"
           aria-label="Dashboard"
           <?= strpos($current_path, '/admin/dashboard.php') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('layout-dashboard') ?>
            <span class="sidebar-label">Dashboard</span>
        </a>

        <a href="/admin/events.php"
           class="sidebar-link<?= strpos($current_path, '/admin/events') !== false || strpos($current_path, '/admin/results') !== false || strpos($current_path, '/admin/event-') !== false ? ' is-active' : '' ?>"
           aria-label="Tävlingar"
           <?= strpos($current_path, '/admin/events') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('calendar-check') ?>
            <span class="sidebar-label">Tävlingar</span>
        </a>

        <a href="/admin/series.php"
           class="sidebar-link<?= strpos($current_path, '/admin/series') !== false || strpos($current_path, '/admin/ranking') !== false ? ' is-active' : '' ?>"
           aria-label="Serier"
           <?= strpos($current_path, '/admin/series') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('medal') ?>
            <span class="sidebar-label">Serier</span>
        </a>

        <?php endif; ?>

        <?php if ($is_admin): ?>
        <!-- ADMIN NAVIGATION (admin and super_admin only) -->
        <div class="sidebar-divider"></div>

        <a href="/admin/dashboard.php"
           class="sidebar-link<?= strpos($current_path, '/admin/dashboard.php') !== false ? ' is-active' : '' ?>"
           aria-label="Dashboard"
           <?= strpos($current_path, '/admin/dashboard.php') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('layout-dashboard') ?>
            <span class="sidebar-label">Dashboard</span>
        </a>

        <a href="/admin/events.php"
           class="sidebar-link<?= strpos($current_path, '/admin/events') !== false || strpos($current_path, '/admin/results') !== false || strpos($current_path, '/admin/venues') !== false || strpos($current_path, '/admin/ticket') !== false ? ' is-active' : '' ?>"
           aria-label="Tävlingar"
           <?= strpos($current_path, '/admin/events') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('calendar-check') ?>
            <span class="sidebar-label">Tävlingar</span>
        </a>

        <a href="/admin/series.php"
           class="sidebar-link<?= strpos($current_path, '/admin/series') !== false || strpos($current_path, '/admin/ranking') !== false || strpos($current_path, '/admin/club-points') !== false ? ' is-active' : '' ?>"
           aria-label="Serier"
           <?= strpos($current_path, '/admin/series') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('medal') ?>
            <span class="sidebar-label">Serier</span>
        </a>

        <a href="/admin/riders.php"
           class="sidebar-link<?= strpos($current_path, '/admin/riders') !== false || strpos($current_path, '/admin/clubs') !== false || strpos($current_path, '/admin/find-duplicates') !== false || strpos($current_path, '/admin/cleanup-') !== false ? ' is-active' : '' ?>"
           aria-label="Databas"
           <?= strpos($current_path, '/admin/riders') !== false || strpos($current_path, '/admin/clubs') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('users') ?>
            <span class="sidebar-label">Databas</span>
        </a>

        <a href="/admin/classes.php"
           class="sidebar-link<?= strpos($current_path, '/admin/classes') !== false || strpos($current_path, '/admin/license') !== false || strpos($current_path, '/admin/point-') !== false || strpos($current_path, '/admin/registration-rules') !== false || strpos($current_path, '/admin/public-settings') !== false || strpos($current_path, '/admin/global-texts') !== false ? ' is-active' : '' ?>"
           aria-label="Konfiguration"
           <?= strpos($current_path, '/admin/classes') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('sliders') ?>
            <span class="sidebar-label">Config</span>
        </a>

        <a href="/admin/import.php"
           class="sidebar-link<?= strpos($current_path, '/admin/import') !== false ? ' is-active' : '' ?>"
           aria-label="Import"
           <?= strpos($current_path, '/admin/import') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('upload') ?>
            <span class="sidebar-label">Import</span>
        </a>

        <?php if ($is_super_admin): ?>
        <a href="/admin/users.php"
           class="sidebar-link<?= strpos($current_path, '/admin/users') !== false || strpos($current_path, '/admin/role-') !== false || strpos($current_path, '/admin/system-') !== false || strpos($current_path, '/admin/settings') !== false || strpos($current_path, '/admin/setup-') !== false || strpos($current_path, '/admin/run-') !== false || strpos($current_path, '/admin/tools') !== false ? ' is-active' : '' ?>"
           aria-label="System"
           <?= strpos($current_path, '/admin/users') !== false ? 'aria-current="page"' : '' ?>>
            <?= nav_icon('settings') ?>
            <span class="sidebar-label">System</span>
        </a>
        <?php endif; ?>
        <?php endif; ?>
    </nav>
</aside>

<style>
/* ========================================================================
   SIDEBAR - Icon-only with tooltips (70px wide)
   Matching components/sidebar.php styling
   ======================================================================== */

/* Sidebar icon styling for Lucide SVGs */
.sidebar-icon-svg {
    width: 22px;
    height: 22px;
    color: inherit;
    stroke: currentColor;
}

/* Sidebar link - icon with label below */
.sidebar-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    padding: var(--space-sm) var(--space-xs);
    margin: 0 auto;
    color: var(--color-text-secondary);
    text-decoration: none;
    border-radius: var(--radius-md);
    transition: all 0.2s ease;
    position: relative;
}

.sidebar-link:hover {
    color: var(--color-text-primary);
    background: var(--color-bg-hover);
}

.sidebar-link:hover .sidebar-icon-svg {
    color: var(--color-text-primary);
}

/* Active state for is-active class */
.sidebar-link.is-active {
    background: var(--color-accent-light);
    color: var(--color-accent-text);
}

.sidebar-link.is-active .sidebar-icon-svg {
    color: var(--color-accent-text);
}

/* Active indicator bar */
.sidebar-link.is-active::before {
    content: '';
    position: absolute;
    left: -12px;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 24px;
    background: var(--color-accent);
    border-radius: 0 2px 2px 0;
}

.sidebar-icon svg {
    color: inherit;
    stroke: currentColor;
}

/* Label under icon */
.sidebar-label {
    display: block;
    font-size: 10px;
    font-weight: var(--weight-medium);
    line-height: 1.2;
    text-align: center;
    margin-top: 2px;
}

/* Tooltip disabled - labels are visible */
.sidebar-link::after {
    display: none;
}

/* Sidebar Sections */
.sidebar-section {
    margin-bottom: var(--space-xs);
}

.sidebar-section-title {
    font-size: 9px;
    font-weight: var(--weight-semibold);
    color: var(--color-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: var(--space-xs) var(--space-sm);
    text-align: center;
}

.sidebar-divider {
    height: 1px;
    background: var(--color-border);
    margin: var(--space-xs) var(--space-sm);
}

/* Admin link styling */
.sidebar-link--admin {
    color: var(--color-accent-text) !important;
}

/* Notification badge on sidebar icons */
.sidebar-icon {
    position: relative;
}

.sidebar-badge {
    position: absolute;
    top: -6px;
    right: -8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 16px;
    height: 16px;
    padding: 0 4px;
    font-size: 10px;
    font-weight: 600;
    line-height: 1;
    border-radius: 8px;
    background: var(--color-text-secondary);
    color: white;
}

.sidebar-badge--alert {
    background: #ef4444;
    animation: pulse-badge 2s infinite;
}

@keyframes pulse-badge {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.sidebar-link.has-badge .sidebar-icon-svg {
    color: #ef4444;
}

/* ========================================================================
   MOBILE PORTRAIT - Slide-out menu with horizontal links
   ======================================================================== */
@media (max-width: 899px) and (orientation: portrait) {
    .sidebar-link {
        flex-direction: row;
        justify-content: flex-start;
        width: 100%;
        height: auto;
        gap: var(--space-md);
        padding: var(--space-md) var(--space-lg);
        margin: 0;
    }

    .sidebar-label {
        display: block;
        font-size: var(--text-sm);
    }

    .sidebar-link::after {
        display: none;
    }

    .sidebar-link.is-active::before {
        left: 0;
    }
}

/* ========================================================================
   MOBILE/TABLET LANDSCAPE - Compact icon-only sidebar flush to left
   ======================================================================== */
@media (max-width: 1023px) and (orientation: landscape) {
    /* Sidebar must be flush to left edge */
    .sidebar {
        position: fixed !important;
        top: var(--header-height, 60px) !important;
        left: 0 !important;
        right: auto !important;
        margin: 0 !important;
        margin-left: 0 !important;
        transform: none !important;
        width: 64px !important;
        padding: 4px 0 !important;
    }

    .sidebar-link {
        flex-direction: column !important;
        padding: 6px 4px !important;
        gap: 1px !important;
        margin: 0 !important;
        width: auto !important;
    }

    .sidebar-label {
        display: none !important;
    }

    .sidebar-icon-svg {
        width: 24px !important;
        height: 24px !important;
    }

    .sidebar-link.is-active::before {
        left: -4px !important;
        height: 20px !important;
    }
}
</style>
