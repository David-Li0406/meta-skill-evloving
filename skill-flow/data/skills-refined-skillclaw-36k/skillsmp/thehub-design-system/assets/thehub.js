/**
 * TheHUB JavaScript
 * Main JavaScript file for TheHUB platform
 */

(function() {
    'use strict';

    // Initialize Lucide Icons
    function initIcons() {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    // Mobile Menu Toggle
    function initMobileMenu() {
        const toggleBtn = document.getElementById('mobile-menu-toggle');
        const sidebar = document.querySelector('.gs-sidebar');
        const overlay = document.getElementById('mobile-overlay');

        if (!toggleBtn || !sidebar) return;

        // Toggle menu
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            if (overlay) {
                overlay.classList.toggle('open');
            }
        });

        // Close menu when clicking overlay
        if (overlay) {
            overlay.addEventListener('click', function() {
                sidebar.classList.remove('open');
                overlay.classList.remove('open');
            });
        }

        // Close menu when clicking a link (for mobile)
        const menuLinks = sidebar.querySelectorAll('.gs-menu a');
        menuLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('open');
                    if (overlay) {
                        overlay.classList.remove('open');
                    }
                }
            });
        });
    }

    // Form Loading State
    function initFormLoadingStates() {
        const forms = document.querySelectorAll('form[data-loading]');

        forms.forEach(function(form) {
            form.addEventListener('submit', function(e) {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.classList.add('gs-loading');
                    submitBtn.disabled = true;
                }
            });
        });
    }

    // Auto-dismiss alerts
    function initAlerts() {
        const alerts = document.querySelectorAll('.gs-alert[data-dismiss]');

        alerts.forEach(function(alert) {
            const dismissTime = parseInt(alert.dataset.dismiss) || 5000;

            setTimeout(function() {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.3s ease-out';

                setTimeout(function() {
                    alert.remove();
                }, 300);
            }, dismissTime);
        });
    }

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        initIcons();
        initMobileMenu();
        initFormLoadingStates();
        initAlerts();
    });

    // Re-initialize icons after dynamic content loads
    window.reinitIcons = initIcons;

})();
