/**
 * TheHUB Viewport System - JavaScript Module
 *
 * Uppdaterar CSS custom properties baserat pa faktisk viewport-storlek.
 * Hanterar mobile browser chrome (adressfalt som andrar storlek).
 *
 * Anvandning:
 *   CSS: height: var(--vh-100);
 *   JS:  TheHUB.viewport.height  // Aktuell viewport-hojd i px
 *
 * @since 2025-12-14
 */

(function() {
    'use strict';

    // Skapa global namespace om det inte finns
    window.TheHUB = window.TheHUB || {};

    /**
     * Viewport Manager
     */
    const ViewportManager = {
        // Aktuella varden
        height: 0,
        width: 0,
        vh: 0,
        vw: 0,
        orientation: 'portrait',
        isTouch: false,
        isMobile: false,

        // Callbacks for listeners
        _listeners: [],

        /**
         * Initialisera viewport tracking
         */
        init: function() {
            // Detektera device-typ
            this.isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
            this.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

            // Initial uppdatering
            this.update();

            // Lyssna pa resize med throttling
            let resizeTimeout;
            window.addEventListener('resize', () => {
                if (resizeTimeout) cancelAnimationFrame(resizeTimeout);
                resizeTimeout = requestAnimationFrame(() => this.update());
            }, { passive: true });

            // Lyssna pa orientation change (mobile)
            window.addEventListener('orientationchange', () => {
                // Vanta pa att orientation ska stabiliseras
                setTimeout(() => this.update(), 100);
            }, { passive: true });

            // Visual Viewport API for mobile browsers (hanterar keyboard, address bar)
            if (window.visualViewport) {
                window.visualViewport.addEventListener('resize', () => {
                    this.update();
                }, { passive: true });
            }

            // Initial CSS klass for att indikera att JS ar laddat
            document.documentElement.classList.add('viewport-ready');

            console.log('[TheHUB] Viewport system initialized:', {
                width: this.width,
                height: this.height,
                isMobile: this.isMobile,
                isTouch: this.isTouch
            });
        },

        /**
         * Uppdatera viewport-varden och CSS-variabler
         */
        update: function() {
            // Anvand visualViewport om tillgangligt (bättre pa mobile)
            if (window.visualViewport) {
                this.height = window.visualViewport.height;
                this.width = window.visualViewport.width;
            } else {
                this.height = window.innerHeight;
                this.width = window.innerWidth;
            }

            // Berakna vh/vw enheter
            this.vh = this.height / 100;
            this.vw = this.width / 100;

            // Bestam orientation
            this.orientation = this.width > this.height ? 'landscape' : 'portrait';

            // Uppdatera CSS custom properties
            const root = document.documentElement;
            root.style.setProperty('--vh', `${this.vh}px`);
            root.style.setProperty('--vw', `${this.vw}px`);
            root.style.setProperty('--viewport-height', `${this.height}px`);
            root.style.setProperty('--viewport-width', `${this.width}px`);

            // Satt data-attribut for CSS-selectors
            root.dataset.orientation = this.orientation;
            root.dataset.viewportWidth = this.getBreakpoint();

            // Notifiera lyssnare
            this._notifyListeners();
        },

        /**
         * Bestam aktuell breakpoint
         */
        getBreakpoint: function() {
            if (this.width < 600) return 'mobile-portrait';
            if (this.width < 768) return 'mobile-landscape';
            if (this.width < 1024) return 'tablet';
            if (this.width < 1400) return 'desktop';
            return 'desktop-large';
        },

        /**
         * Hamta varde i px for en vh-procent
         */
        getVh: function(percent) {
            return this.vh * percent;
        },

        /**
         * Hamta varde i px for en vw-procent
         */
        getVw: function(percent) {
            return this.vw * percent;
        },

        /**
         * Registrera callback for viewport-andringar
         */
        onChange: function(callback) {
            if (typeof callback === 'function') {
                this._listeners.push(callback);
            }
            return this;
        },

        /**
         * Ta bort callback
         */
        offChange: function(callback) {
            this._listeners = this._listeners.filter(cb => cb !== callback);
            return this;
        },

        /**
         * Notifiera alla lyssnare
         */
        _notifyListeners: function() {
            const data = {
                height: this.height,
                width: this.width,
                vh: this.vh,
                vw: this.vw,
                orientation: this.orientation,
                breakpoint: this.getBreakpoint()
            };

            this._listeners.forEach(callback => {
                try {
                    callback(data);
                } catch (e) {
                    console.error('[TheHUB Viewport] Listener error:', e);
                }
            });
        },

        /**
         * Satt en elements hojd baserat pa viewport-procent
         * @param {HTMLElement|string} element - Element eller selector
         * @param {number} percent - Procent av viewport-hojd (0-100)
         * @param {object} options - { min: px, max: px, offset: px }
         */
        setElementHeight: function(element, percent, options = {}) {
            const el = typeof element === 'string' ? document.querySelector(element) : element;
            if (!el) return;

            const { min = 0, max = Infinity, offset = 0 } = options;
            let height = this.getVh(percent) - offset;
            height = Math.max(min, Math.min(max, height));

            el.style.height = `${height}px`;

            // Uppdatera automatiskt vid resize
            if (!el._viewportBound) {
                el._viewportBound = true;
                this.onChange(() => {
                    this.setElementHeight(el, percent, options);
                });
            }
        }
    };

    // Exportera till global namespace
    window.TheHUB.viewport = ViewportManager;

    // Auto-init nar DOM ar redo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => ViewportManager.init());
    } else {
        ViewportManager.init();
    }

    /**
     * Utility: Uppdatera alla element med data-vh-height attribut
     */
    function updateDataAttributes() {
        // Elements med data-vh-height="50" far 50vh hojd
        document.querySelectorAll('[data-vh-height]').forEach(el => {
            const percent = parseInt(el.dataset.vhHeight, 10) || 50;
            el.style.setProperty('--element-vh', percent);
        });

        document.querySelectorAll('[data-vh-min-height]').forEach(el => {
            const percent = parseInt(el.dataset.vhMinHeight, 10) || 30;
            el.style.setProperty('--element-vh-min', percent);
        });

        document.querySelectorAll('[data-vh-max-height]').forEach(el => {
            const percent = parseInt(el.dataset.vhMaxHeight, 10) || 80;
            el.style.setProperty('--element-vh-max', percent);
        });
    }

    // Kor efter init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateDataAttributes);
    } else {
        updateDataAttributes();
    }

})();
