<?php
/**
 * TheHUB Modern Header (V2.5)
 * Includes desktop navigation, theme switcher and profile dropdown
 */

// Include necessary helpers
if (!function_exists('get_current_rider')) {
    require_once __DIR__ . '/rider-auth.php';
}

$isLoggedIn = isset($_SESSION['rider_id']) && $_SESSION['rider_id'] > 0;
$currentUser = $isLoggedIn ? get_current_rider() : null;
$isAdmin = isset($_SESSION['admin_id']) && $_SESSION['admin_id'] > 0;

// Navigation items (samma som bottom nav)
$currentPage = basename($_SERVER['PHP_SELF']);
$currentPath = $_SERVER['PHP_SELF'];

$navItems = [
    ['id' => 'events', 'label' => 'Kalender', 'url' => '/events.php'],
    ['id' => 'results', 'label' => 'Resultat', 'url' => '/v3/results'],
    ['id' => 'series', 'label' => 'Serier', 'url' => '/v3/series'],
    ['id' => 'ranking', 'label' => 'Ranking', 'url' => '/v3/ranking'],
    ['id' => 'profile', 'label' => 'Profil', 'url' => '/profile.php'],
];
?>

<header class="header">
    <!-- Logo - klickbar till startsida -->
    <a href="/" class="header-brand">
        <svg class="header-logo" viewBox="0 0 40 40">
            <circle cx="20" cy="20" r="18" fill="currentColor" opacity="0.1"/>
            <circle cx="20" cy="20" r="18" fill="none" stroke="currentColor" stroke-width="2"/>
            <text x="20" y="25" text-anchor="middle" fill="currentColor" font-size="12" font-weight="bold">HUB</text>
        </svg>
        <span class="header-title">TheHUB</span>
    </a>

    <!-- Desktop navigation (dold på mobil) -->
    <nav class="header-nav" role="navigation">
        <?php foreach ($navItems as $item): ?>
            <?php
            // Determine if this item is active
            $isActive = false;
            if ($item['id'] === 'ranking' && ($currentPage === 'ranking.php' || strpos($currentPath, '/ranking/') !== false)) {
                $isActive = true;
            } elseif ($item['id'] === 'events' && ($currentPage === 'events.php' || $currentPage === 'calendar.php')) {
                $isActive = true;
            } elseif ($item['id'] === 'profile' && $currentPage === 'profile.php') {
                $isActive = true;
            } elseif ($item['id'] !== 'ranking' && $item['id'] !== 'profile') {
                $isActive = ($currentPage === $item['id'] . '.php');
            }
            ?>
            <a href="<?= $item['url'] ?>"
               class="header-nav-item <?= $isActive ? 'is-active' : '' ?>"
               <?= $isActive ? 'aria-current="page"' : '' ?>>
                <?= $item['label'] ?>
            </a>
        <?php endforeach; ?>
    </nav>

    <!-- Actions (tema, admin, login/profile) -->
    <div class="header-actions">
        <!-- Tema-switcher (endast desktop i header) -->
        <div class="theme-switcher theme-switcher--header">
            <button data-theme-set="light" class="theme-btn" title="Ljust tema" aria-label="Ljust tema">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="4"/>
                    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
                </svg>
            </button>
            <button data-theme-set="auto" class="theme-btn" title="Automatiskt" aria-label="Automatiskt tema">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect width="20" height="14" x="2" y="3" rx="2"/>
                    <line x1="8" x2="16" y1="21" y2="21"/>
                    <line x1="12" x2="12" y1="17" y2="21"/>
                </svg>
            </button>
            <button data-theme-set="dark" class="theme-btn" title="Mörkt tema" aria-label="Mörkt tema">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
                </svg>
            </button>
        </div>

        <?php if ($isLoggedIn && $currentUser): ?>
            <!-- Admin-länk -->
            <?php if ($isAdmin): ?>
            <a href="/admin/" class="header-icon-btn" title="Admin">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                    <circle cx="12" cy="12" r="3"/>
                </svg>
            </a>
            <?php endif; ?>

            <!-- User dropdown -->
            <div class="header-user-menu" data-dropdown>
                <button class="header-user-btn" aria-haspopup="true" aria-expanded="false">
                    <span class="header-user-name"><?= htmlspecialchars($currentUser['firstname'] ?? '') ?></span>
                    <div class="header-user-avatar">
                        <?= strtoupper(substr($currentUser['firstname'] ?? 'U', 0, 1)) ?>
                    </div>
                </button>

                <div class="header-dropdown">
                    <div class="header-dropdown-header">
                        <strong><?= htmlspecialchars(($currentUser['firstname'] ?? '') . ' ' . ($currentUser['lastname'] ?? '')) ?></strong>
                        <span class="text-secondary text-sm"><?= htmlspecialchars($currentUser['email'] ?? '') ?></span>
                    </div>

                    <div class="header-dropdown-divider"></div>

                    <a href="/profile.php" class="header-dropdown-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                        Min profil
                    </a>

                    <a href="/my-registrations.php" class="header-dropdown-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <rect x="3" y="4" width="18" height="18" rx="2"/>
                            <line x1="16" y1="2" x2="16" y2="6"/>
                            <line x1="8" y1="2" x2="8" y2="6"/>
                            <line x1="3" y1="10" x2="21" y2="10"/>
                        </svg>
                        Mina anmälningar
                    </a>

                    <a href="/my-results.php" class="header-dropdown-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
                            <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
                            <path d="M4 22h16"/>
                            <path d="M10 14.66V17"/>
                            <path d="M14 14.66V17"/>
                            <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
                        </svg>
                        Mina resultat
                    </a>

                    <div class="header-dropdown-divider"></div>

                    <a href="/rider-logout.php" class="header-dropdown-item text-error">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                            <polyline points="16 17 21 12 16 7"/>
                            <line x1="21" y1="12" x2="9" y2="12"/>
                        </svg>
                        Logga ut
                    </a>
                </div>
            </div>
        <?php endif; ?>
    </div>
</header>

<!-- Dropdown script -->
<script>
(function() {
    document.querySelectorAll('[data-dropdown]').forEach(dropdown => {
        const btn = dropdown.querySelector('.header-user-btn');
        const menu = dropdown.querySelector('.header-dropdown');

        btn?.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('is-open');
            btn.setAttribute('aria-expanded', dropdown.classList.contains('is-open'));
        });

        // Stäng vid klick utanför
        document.addEventListener('click', (e) => {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('is-open');
                btn?.setAttribute('aria-expanded', 'false');
            }
        });
    });
})();
</script>
