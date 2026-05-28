<?php
// Defensive checks for functions
$currentUser = function_exists('hub_current_user') ? hub_current_user() : null;
$isLoggedIn = function_exists('hub_is_logged_in') ? hub_is_logged_in() : false;
$isAdmin = function_exists('hub_is_admin') ? hub_is_admin() : false;
// Promotors should NOT see full admin link - they get a simplified promotor panel instead
$isPromotorOnly = function_exists('isRole') && isRole('promotor');
if ($isPromotorOnly) {
    $isAdmin = false;
}
$hubUrl = defined('HUB_URL') ? HUB_URL : '';

// Check if super admin (for theme switcher access)
$isSuperAdmin = function_exists('hasRole') && hasRole('super_admin');

// Get sidebar logo from branding settings
$headerLogo = function_exists('getBranding') ? getBranding('logos.sidebar') : null;
?>

<header class="header" role="banner">
    <a href="<?= $hubUrl ?>/" class="header-brand" aria-label="TheHUB - Gå till startsidan">
        <?php if ($headerLogo): ?>
        <img src="<?= htmlspecialchars($headerLogo) ?>" alt="TheHUB" class="header-logo" width="40" height="40">
        <?php else: ?>
        <svg class="header-logo" viewBox="0 0 40 40" aria-hidden="true">
            <circle cx="20" cy="20" r="18" fill="currentColor" opacity="0.1"/>
            <circle cx="20" cy="20" r="18" fill="none" stroke="currentColor" stroke-width="2"/>
            <text x="20" y="25" text-anchor="middle" fill="currentColor" font-size="12" font-weight="bold">HUB</text>
        </svg>
        <?php endif; ?>
    </a>

    <!-- Header Inline Sponsor (between logo and actions) -->
    <?php
    if (function_exists('render_global_sponsors')) {
        echo render_global_sponsors('all', 'header_inline', '');
    }
    ?>

    <div class="header-actions">
        <?php if ($isLoggedIn && $currentUser): ?>

            <?php if ($isAdmin): ?>
            <a href="<?= $hubUrl ?>/admin" class="header-admin-link" title="Admin">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
                    <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                    <circle cx="12" cy="12" r="3"/>
                </svg>
            </a>
            <?php elseif ($isPromotorOnly): ?>
            <a href="<?= $hubUrl ?>/admin/promotor.php" class="header-admin-link" title="Mina tävlingar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
                    <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                    <circle cx="12" cy="12" r="3"/>
                </svg>
            </a>
            <?php endif; ?>

            <div class="header-user-menu" data-dropdown>
                <button class="header-user-btn" aria-expanded="false" aria-haspopup="true">
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

                    <a href="<?= $hubUrl ?>/profile" class="header-dropdown-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                        Min profil
                    </a>

                    <a href="<?= $hubUrl ?>/profile/registrations" class="header-dropdown-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <rect x="3" y="4" width="18" height="18" rx="2"/>
                            <line x1="16" y1="2" x2="16" y2="6"/>
                            <line x1="8" y1="2" x2="8" y2="6"/>
                            <line x1="3" y1="10" x2="21" y2="10"/>
                        </svg>
                        Mina anmälningar
                    </a>

                    <a href="<?= $hubUrl ?>/profile/results" class="header-dropdown-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
                            <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
                            <path d="M4 22h16"/>
                            <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
                            <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
                            <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
                        </svg>
                        Mina resultat
                    </a>

                    <div class="header-dropdown-divider"></div>

                    <?php if ($isAdmin): ?>
                    <a href="<?= $hubUrl ?>/admin" class="header-dropdown-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                            <circle cx="12" cy="12" r="3"/>
                        </svg>
                        Admin
                    </a>

                    <div class="header-dropdown-divider"></div>
                    <?php elseif ($isPromotorOnly): ?>
                    <a href="<?= $hubUrl ?>/admin/promotor.php" class="header-dropdown-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <rect x="3" y="4" width="18" height="18" rx="2"/>
                            <line x1="16" y1="2" x2="16" y2="6"/>
                            <line x1="8" y1="2" x2="8" y2="6"/>
                            <line x1="3" y1="10" x2="21" y2="10"/>
                            <path d="m9 16 2 2 4-4"/>
                        </svg>
                        Mina tävlingar
                    </a>
                    <div class="header-dropdown-divider"></div>
                    <?php endif; ?>

                    <?php if ($isSuperAdmin): ?>
                    <!-- Theme Switcher - only for super admins -->
                    <div class="header-dropdown-theme">
                        <div class="theme-label">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                                <circle cx="12" cy="12" r="4"/>
                                <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
                            </svg>
                            Tema
                        </div>
                        <div class="theme-options">
                            <button data-theme-set="light" class="theme-option-btn" title="Ljust tema">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="4"/>
                                    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
                                </svg>
                            </button>
                            <button data-theme-set="auto" class="theme-option-btn" title="Automatiskt">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect width="20" height="14" x="2" y="3" rx="2"/>
                                    <line x1="8" x2="16" y1="21" y2="21"/>
                                    <line x1="12" x2="12" y1="17" y2="21"/>
                                </svg>
                            </button>
                            <button data-theme-set="dark" class="theme-option-btn" title="Mörkt tema">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="header-dropdown-divider"></div>
                    <?php endif; ?>

                    <a href="<?= $hubUrl ?>/logout" class="header-dropdown-item text-error">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                            <polyline points="16 17 21 12 16 7"/>
                            <line x1="21" y1="12" x2="9" y2="12"/>
                        </svg>
                        Logga ut
                    </a>
                </div>
            </div>

        <?php else: ?>
            <a href="<?= $hubUrl ?>/login?redirect=<?= urlencode($_SERVER['REQUEST_URI']) ?>" class="btn btn-primary btn-sm">
                <?php require_once HUB_ROOT . '/components/icons.php'; ?>
                <?= hub_icon('log-in', 'icon-sm') ?>
                <span class="header-login-text">Logga in</span>
            </a>
        <?php endif; ?>
    </div>
</header>

<style>
/* Header Inline Sponsor */
.sponsor-section-header_inline {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    max-height: 40px;
    overflow: hidden;
    margin: 0 var(--space-md);
}

.sponsor-section-header_inline .sponsor-grid {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-sm);
}

.sponsor-section-header_inline .sponsor-item {
    max-height: 32px;
    display: flex;
    align-items: center;
}

.sponsor-section-header_inline .sponsor-logo {
    max-height: 28px;
    max-width: 120px;
    width: auto;
    object-fit: contain;
}

.sponsor-section-header_inline .sponsor-banner {
    max-height: 36px;
    max-width: 300px;
    width: auto;
    object-fit: contain;
}

.sponsor-section-header_inline .sponsor-name {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
}

/* Hide on mobile */
@media (max-width: 768px) {
    .sponsor-section-header_inline {
        display: none;
    }
}

/* Header User Actions */
.header-actions {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.header-admin-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: var(--radius-full);
    color: var(--color-text-secondary);
    transition: all var(--transition-fast);
}

.header-admin-link:hover {
    background: var(--color-bg-hover);
    color: var(--color-accent);
}

/* User Menu */
.header-user-menu {
    position: relative;
}

.header-user-btn {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-xs) var(--space-sm);
    background: transparent;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-full);
    cursor: pointer;
    transition: all var(--transition-fast);
    color: inherit;
    font: inherit;
}

.header-user-btn:hover {
    border-color: var(--color-border-strong);
    background: var(--color-bg-hover);
}

.header-user-name {
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
    display: none;
}

@media (min-width: 640px) {
    .header-user-name {
        display: block;
    }
}

.header-user-avatar {
    width: 28px;
    height: 28px;
    border-radius: var(--radius-full);
    background: var(--color-accent);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--text-xs);
    font-weight: var(--weight-bold);
}

/* Dropdown */
.header-dropdown {
    position: absolute;
    top: calc(100% + var(--space-xs));
    right: 0;
    min-width: 220px;
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-lg);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-8px);
    transition: all var(--transition-fast);
    z-index: var(--z-dropdown, 100);
}

.header-user-menu.is-open .header-dropdown {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.header-dropdown-header {
    padding: var(--space-md);
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.header-dropdown-divider {
    height: 1px;
    background: var(--color-border);
    margin: var(--space-xs) 0;
}

.header-dropdown-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    color: var(--color-text-primary);
    text-decoration: none;
    transition: background var(--transition-fast);
}

.header-dropdown-item:hover {
    background: var(--color-bg-hover);
}

.header-dropdown-item.text-error {
    color: var(--color-error);
}

.header-dropdown-item svg {
    color: var(--color-text-muted);
}

.header-dropdown-item.text-error svg {
    color: var(--color-error);
}

/* Theme Switcher i Dropdown */
.header-dropdown-theme {
    padding: var(--space-sm) var(--space-md);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-md);
}

.theme-label {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    font-size: var(--text-sm);
    color: var(--color-text-primary);
}

.theme-label svg {
    color: var(--color-text-muted);
}

.theme-options {
    display: flex;
    gap: var(--space-2xs);
}

.theme-option-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border: 1px solid var(--color-border);
    background: transparent;
    border-radius: var(--radius-md);
    color: var(--color-text-muted);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.theme-option-btn svg {
    width: 16px;
    height: 16px;
}

.theme-option-btn:hover {
    background: var(--color-bg-hover);
    color: var(--color-text-primary);
    border-color: var(--color-border-strong);
}

.theme-option-btn.is-active {
    background: var(--color-accent-light);
    color: var(--color-accent);
    border-color: var(--color-accent);
    box-shadow: var(--shadow-glow);
}

.text-secondary {
    color: var(--color-text-secondary);
}

.text-sm {
    font-size: var(--text-sm);
}

/* Login button */
.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    background: var(--color-accent);
    color: white;
    padding: var(--space-xs) var(--space-md);
    border-radius: var(--radius-md);
    text-decoration: none;
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
}

.btn-primary .icon-sm {
    width: 16px;
    height: 16px;
}

.btn-primary:hover {
    opacity: 0.9;
}

.header-login-text {
    display: none;
}

@media (min-width: 480px) {
    .header-login-text {
        display: inline;
    }
}
</style>

<script>
// Dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-dropdown]').forEach(function(dropdown) {
        var btn = dropdown.querySelector('button');
        if (btn) {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                var isOpen = dropdown.classList.toggle('is-open');
                btn.setAttribute('aria-expanded', isOpen);

                // Close other dropdowns
                document.querySelectorAll('[data-dropdown].is-open').forEach(function(d) {
                    if (d !== dropdown) {
                        d.classList.remove('is-open');
                        var b = d.querySelector('button');
                        if (b) b.setAttribute('aria-expanded', 'false');
                    }
                });
            });
        }
    });

    // Close on click outside
    document.addEventListener('click', function() {
        document.querySelectorAll('[data-dropdown].is-open').forEach(function(d) {
            d.classList.remove('is-open');
            var b = d.querySelector('button');
            if (b) b.setAttribute('aria-expanded', 'false');
        });
    });

    // Close on ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('[data-dropdown].is-open').forEach(function(d) {
                d.classList.remove('is-open');
                var b = d.querySelector('button');
                if (b) b.setAttribute('aria-expanded', 'false');
            });
        }
    });
});
</script>
