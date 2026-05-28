/**
 * Admin Panel JavaScript
 * Handles sidebar, dropdowns, submenus, and theme switching
 */

// ========================================================================
// SIDEBAR FUNCTIONS
// ========================================================================

/**
 * Toggle admin sidebar (mobile)
 */
function toggleAdminSidebar() {
    const sidebar = document.getElementById('adminSidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (sidebar) {
        sidebar.classList.toggle('open');
    }
    if (overlay) {
        overlay.classList.toggle('active');
    }

    // Prevent body scroll when sidebar is open on mobile
    document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';
}

/**
 * Close admin sidebar
 */
function closeAdminSidebar() {
    const sidebar = document.getElementById('adminSidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (sidebar) {
        sidebar.classList.remove('open');
    }
    if (overlay) {
        overlay.classList.remove('active');
    }

    document.body.style.overflow = '';
}

/**
 * Toggle submenu in sidebar
 */
function toggleSubmenu(menuId) {
    const submenu = document.getElementById('submenu-' + menuId);
    const navGroup = submenu ? submenu.closest('.nav-item-group') : null;

    if (!submenu) return;

    // Close other submenus first (optional - remove for accordion behavior)
    // document.querySelectorAll('.nav-submenu.open').forEach(function(el) {
    //     if (el.id !== 'submenu-' + menuId) {
    //         el.classList.remove('open');
    //         el.closest('.nav-item-group').classList.remove('active');
    //     }
    // });

    // Toggle this submenu
    submenu.classList.toggle('open');
    if (navGroup) {
        navGroup.classList.toggle('active');
    }
}

// ========================================================================
// USER MENU FUNCTIONS
// ========================================================================

/**
 * Toggle user dropdown menu
 */
function toggleUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    const userMenu = dropdown ? dropdown.closest('.user-menu') : null;

    if (dropdown) {
        dropdown.classList.toggle('show');
    }
    if (userMenu) {
        userMenu.classList.toggle('open');
    }
}

// ========================================================================
// MOBILE NAV FUNCTIONS
// ========================================================================
function initMobileNavScrollIndicators() {
    const nav = document.querySelector('.admin-mobile-nav');
    const inner = document.querySelector('.admin-mobile-nav-inner');

    if (!nav || !inner) return;

    function updateScrollIndicators() {
        const canScrollLeft = inner.scrollLeft > 10;
        const canScrollRight = inner.scrollLeft < (inner.scrollWidth - inner.clientWidth - 10);

        nav.classList.toggle('can-scroll-left', canScrollLeft);
        nav.classList.toggle('can-scroll-right', canScrollRight);
    }

    inner.addEventListener('scroll', updateScrollIndicators);
    window.addEventListener('resize', updateScrollIndicators);

    // Initial check
    setTimeout(updateScrollIndicators, 100);

    // Scroll active item into view on load
    const activeLink = inner.querySelector('.admin-mobile-nav-link.active');
    if (activeLink) {
        activeLink.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
}

// ========================================================================
// EVENT LISTENERS
// ========================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Theme is handled by /assets/js/theme.js

    // Initialize mobile nav scroll indicators
    initMobileNavScrollIndicators();

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(event) {
        // Close user dropdown
        if (!event.target.closest('.user-menu')) {
            const dropdown = document.getElementById('userDropdown');
            const userMenu = dropdown ? dropdown.closest('.user-menu') : null;

            if (dropdown) {
                dropdown.classList.remove('show');
            }
            if (userMenu) {
                userMenu.classList.remove('open');
            }
        }

        // Close sidebar on mobile when clicking outside
        if (window.innerWidth <= 1024) {
            const sidebar = document.getElementById('adminSidebar');
            const toggle = document.querySelector('.mobile-menu-toggle');

            if (sidebar && sidebar.classList.contains('open')) {
                if (!event.target.closest('.admin-sidebar') && !event.target.closest('.mobile-menu-toggle')) {
                    closeAdminSidebar();
                }
            }
        }
    });

    // Handle escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            // Close user dropdown
            const dropdown = document.getElementById('userDropdown');
            if (dropdown && dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
                const userMenu = dropdown.closest('.user-menu');
                if (userMenu) userMenu.classList.remove('open');
            }

            // Close sidebar on mobile
            if (window.innerWidth <= 1024) {
                closeAdminSidebar();
            }
        }
    });

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            // Close sidebar on desktop
            if (window.innerWidth > 1024) {
                closeAdminSidebar();
            }
        }, 250);
    });

    // System theme changes handled by /assets/js/theme.js
});

// ========================================================================
// UTILITY FUNCTIONS
// ========================================================================

/**
 * Show confirmation dialog before delete actions
 */
function confirmDelete(message) {
    return confirm(message || 'Är du säker på att du vill ta bort detta?');
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Kopierat!', 'success');
        }).catch(function() {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast('Kopierat!', 'success');
}

/**
 * Show toast notification
 */
function showToast(message, type) {
    type = type || 'info';

    // Remove existing toast
    const existing = document.querySelector('.admin-toast');
    if (existing) {
        existing.remove();
    }

    // Create toast
    const toast = document.createElement('div');
    toast.className = 'admin-toast admin-toast-' + type;
    toast.textContent = message;

    // Add styles if not already present
    if (!document.querySelector('#admin-toast-styles')) {
        const style = document.createElement('style');
        style.id = 'admin-toast-styles';
        style.textContent = `
            .admin-toast {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                color: white;
                font-size: 14px;
                z-index: 9999;
                animation: slideIn 0.3s ease;
            }
            .admin-toast-success { background: #22c55e; }
            .admin-toast-error { background: #ef4444; }
            .admin-toast-warning { background: #f59e0b; }
            .admin-toast-info { background: #3b82f6; }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(toast);

    // Remove after 3 seconds
    setTimeout(function() {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 3000);
}

/**
 * Format number with thousand separators
 */
function formatNumber(num) {
    return new Intl.NumberFormat('sv-SE').format(num);
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            func.apply(context, args);
        }, wait);
    };
}
