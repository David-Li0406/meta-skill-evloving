/**
 * TheHUB Badge Design System JavaScript
 * Handles theme-aware logo switching and badge interactions
 */

(function() {
    'use strict';

    /**
     * Switch badge logos based on current theme
     */
    function updateBadgeLogos() {
        const theme = document.documentElement.getAttribute('data-theme');
        const isDark = theme === 'dark' ||
            (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches);

        document.querySelectorAll('.badge-logo[data-light-src][data-dark-src]').forEach(logo => {
            const lightSrc = logo.getAttribute('data-light-src');
            const darkSrc = logo.getAttribute('data-dark-src');

            if (isDark && darkSrc) {
                logo.src = darkSrc;
            } else if (lightSrc) {
                logo.src = lightSrc;
            }
        });

        // Also handle series header logos
        document.querySelectorAll('.badge-series-header-logo[data-light-src][data-dark-src]').forEach(logo => {
            const lightSrc = logo.getAttribute('data-light-src');
            const darkSrc = logo.getAttribute('data-dark-src');

            if (isDark && darkSrc) {
                logo.src = darkSrc;
            } else if (lightSrc) {
                logo.src = lightSrc;
            }
        });
    }

    /**
     * Handle badge click tracking (for analytics)
     */
    function trackBadgeClick(badge) {
        const badgeType = badge.dataset.badgeType || 'unknown';
        const badgeId = badge.dataset.badgeId || '';
        const badgeName = badge.dataset.badgeName || '';

        // Send to analytics if available
        if (typeof gtag === 'function') {
            gtag('event', 'badge_click', {
                'badge_type': badgeType,
                'badge_id': badgeId,
                'badge_name': badgeName
            });
        }

        // Also log for debugging
        if (window.HUB_DEBUG) {
            console.log('Badge click:', { type: badgeType, id: badgeId, name: badgeName });
        }
    }

    /**
     * Handle sponsor click tracking
     */
    function trackSponsorClick(sponsor) {
        const sponsorName = sponsor.dataset.sponsorName || '';
        const sponsorTier = sponsor.dataset.tier || 'bronze';
        const placement = sponsor.dataset.placement || 'unknown';

        // Send to analytics if available
        if (typeof gtag === 'function') {
            gtag('event', 'sponsor_click', {
                'sponsor_name': sponsorName,
                'sponsor_tier': sponsorTier,
                'placement': placement
            });
        }

        // Also log for debugging
        if (window.HUB_DEBUG) {
            console.log('Sponsor click:', { name: sponsorName, tier: sponsorTier, placement: placement });
        }
    }

    /**
     * Add loading state to badges
     */
    function initBadgeLoading() {
        document.querySelectorAll('.badge-bold .badge-logo').forEach(logo => {
            const badge = logo.closest('.badge-bold');

            // Add skeleton class until loaded
            badge.classList.add('badge-loading');

            logo.addEventListener('load', () => {
                badge.classList.remove('badge-loading');
            });

            logo.addEventListener('error', () => {
                badge.classList.remove('badge-loading');
                // Show placeholder on error
                logo.style.display = 'none';
                const placeholder = document.createElement('div');
                placeholder.className = 'badge-logo-placeholder';
                placeholder.innerHTML = '<span>?</span>';
                logo.parentNode.appendChild(placeholder);
            });
        });
    }

    /**
     * Initialize badge click handlers
     */
    function initBadgeClicks() {
        // Track badge clicks
        document.querySelectorAll('.badge-bold').forEach(badge => {
            badge.addEventListener('click', () => trackBadgeClick(badge));
        });

        // Track sponsor clicks
        document.querySelectorAll('.badge-sponsor').forEach(sponsor => {
            sponsor.addEventListener('click', () => trackSponsorClick(sponsor));
        });
    }

    /**
     * Handle keyboard navigation for badges
     */
    function initBadgeKeyboard() {
        document.querySelectorAll('.badge-bold, .badge-sponsor').forEach(badge => {
            // Make focusable if not already a link
            if (!badge.hasAttribute('tabindex')) {
                badge.setAttribute('tabindex', '0');
            }

            // Handle Enter key
            badge.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    badge.click();
                }
            });
        });
    }

    /**
     * Lazy load badge images
     */
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        const src = img.dataset.src;

                        if (src) {
                            img.src = src;
                            img.removeAttribute('data-src');
                        }

                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            document.querySelectorAll('.badge-logo[data-src], .badge-sponsor-logo[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for older browsers
            document.querySelectorAll('.badge-logo[data-src], .badge-sponsor-logo[data-src]').forEach(img => {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        }
    }

    /**
     * Apply dynamic gradient colors to badges
     */
    function applyBadgeGradients() {
        document.querySelectorAll('.badge-bold[data-gradient-start][data-gradient-end]').forEach(badge => {
            const start = badge.dataset.gradientStart;
            const end = badge.dataset.gradientEnd;

            if (start && end) {
                badge.style.background = `linear-gradient(135deg, ${start} 0%, ${end} 100%)`;
            }
        });
    }

    /**
     * Initialize all badge functionality
     */
    function init() {
        // Update logos on init
        updateBadgeLogos();

        // Initialize features
        initBadgeLoading();
        initBadgeClicks();
        initBadgeKeyboard();
        initLazyLoading();
        applyBadgeGradients();

        // Listen for theme changes via MutationObserver
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'data-theme') {
                    updateBadgeLogos();
                }
            });
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-theme']
        });

        // Also update on system theme change
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateBadgeLogos);
        }
    }

    // Initialize on DOMContentLoaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose public API
    window.HUB_Badges = {
        updateLogos: updateBadgeLogos,
        applyGradients: applyBadgeGradients,
        trackClick: trackBadgeClick,
        trackSponsor: trackSponsorClick
    };

})();
