/**
 * TheHUB Theme Switcher
 * Hanterar light/dark/auto theme switching
 */
const HubTheme = (function() {
  'use strict';
  
  const STORAGE_KEY = 'thehub-theme';
  const COOKIE = 'hub_theme';
  
  /**
   * Hämta sparad theme preference
   */
  function getSaved() {
    // Try localStorage first (faster, better)
    try {
      const ls = localStorage.getItem(STORAGE_KEY);
      if (ls) return ls;
    } catch (e) {}
    
    // Fallback to cookie
    const match = document.cookie.match(new RegExp('(^| )' + COOKIE + '=([^;]+)'));
    return match ? match[2] : 'auto';
  }
  
  /**
   * Spara theme preference
   */
  function save(theme) {
    // Save to both localStorage and cookie for compatibility
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {}
    
    document.cookie = COOKIE + '=' + theme + '; path=/; max-age=31536000; SameSite=Lax';
  }
  
  /**
   * Hämta system theme preference
   */
  function getSystem() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  
  /**
   * Applicera theme
   */
  function apply(theme) {
    const resolved = theme === 'auto' ? getSystem() : theme;
    
    // Sätt data-theme på <html>
    document.documentElement.setAttribute('data-theme', resolved);
    
    // Uppdatera alla theme-knappar
    document.querySelectorAll('.theme-btn, .theme-option-btn, [data-theme-set]').forEach(btn => {
      const btnTheme = btn.getAttribute('data-theme-set');
      if (btnTheme === theme) {
        btn.classList.add('is-active');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.classList.remove('is-active');
        btn.setAttribute('aria-pressed', 'false');
      }
    });
    
    // Uppdatera meta theme-color för browser UI
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', resolved === 'dark' ? '#0b131e' : '#f8f9fa');
    }
  }
  
  /**
   * Sätt theme och spara
   */
  function set(theme) {
    if (!['light', 'dark', 'auto'].includes(theme)) {
      theme = 'auto';
    }
    
    save(theme);
    apply(theme);
    announce(theme);
  }
  
  /**
   * Announce theme change för screen readers
   */
  function announce(theme) {
    const labels = {
      light: 'Ljust tema',
      dark: 'Mörkt tema',
      auto: 'Automatiskt tema'
    };
    
    let el = document.getElementById('theme-announcement');
    if (!el) {
      el = document.createElement('div');
      el.id = 'theme-announcement';
      el.setAttribute('role', 'status');
      el.setAttribute('aria-live', 'polite');
      el.className = 'sr-only';
      el.style.cssText = 'position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden;';
      document.body.appendChild(el);
    }
    
    el.textContent = labels[theme] + ' aktiverat';
  }
  
  /**
   * Initialize theme system
   */
  function init() {
    // Applicera sparad theme
    const saved = getSaved();
    apply(saved);
    
    // Lyssna på system theme changes (för auto mode)
    const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    darkModeQuery.addEventListener('change', () => {
      if (getSaved() === 'auto') {
        apply('auto');
      }
    });
    
    // Lyssna på alla theme-btn klick
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.theme-btn, .theme-option-btn, [data-theme-set]');
      if (btn && btn.hasAttribute('data-theme-set')) {
        e.preventDefault();
        e.stopPropagation();
        const theme = btn.getAttribute('data-theme-set');
        set(theme);
      }
    });
    
    console.log('🎨 Theme system initialized:', saved);
  }
  
  // Public API
  return {
    init: init,
    setTheme: set,
    getTheme: getSaved
  };
})();

// Auto-initialize
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', HubTheme.init);
} else {
  HubTheme.init();
}
