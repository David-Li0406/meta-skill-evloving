/**
 * TheHUB V3 - PWA Functionality
 * Handles service worker registration, install prompts, and updates
 */

const HubPWA = (function() {
  'use strict';

  let deferredPrompt = null;
  let swRegistration = null;

  /**
   * Register service worker
   */
  async function registerServiceWorker() {
    if (!('serviceWorker' in navigator)) {
      console.log('[PWA] Service workers not supported');
      return;
    }

    try {
      swRegistration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/'
      });

      console.log('[PWA] Service worker registered:', swRegistration.scope);

      // Check for updates
      swRegistration.addEventListener('updatefound', () => {
        const newWorker = swRegistration.installing;

        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            // New version available
            showUpdateNotification();
          }
        });
      });

    } catch (error) {
      console.error('[PWA] Service worker registration failed:', error);
    }
  }

  /**
   * Handle beforeinstallprompt event
   */
  function handleInstallPrompt(e) {
    // Prevent Chrome's default prompt
    e.preventDefault();

    // Store the event for later
    deferredPrompt = e;

    // Show custom install UI
    showInstallButton();

    console.log('[PWA] Install prompt ready');
  }

  /**
   * Show install button in UI
   */
  function showInstallButton() {
    const installBtn = document.getElementById('pwa-install-btn');
    if (installBtn) {
      installBtn.classList.remove('hidden');
    }

    // Also show in header if exists
    const headerInstall = document.querySelector('.header-install');
    if (headerInstall) {
      headerInstall.classList.remove('hidden');
    }
  }

  /**
   * Hide install button
   */
  function hideInstallButton() {
    const installBtn = document.getElementById('pwa-install-btn');
    if (installBtn) {
      installBtn.classList.add('hidden');
    }

    const headerInstall = document.querySelector('.header-install');
    if (headerInstall) {
      headerInstall.classList.add('hidden');
    }
  }

  /**
   * Trigger install prompt
   */
  async function promptInstall() {
    if (!deferredPrompt) {
      console.log('[PWA] No install prompt available');
      return false;
    }

    // Show the prompt
    deferredPrompt.prompt();

    // Wait for user response
    const { outcome } = await deferredPrompt.userChoice;
    console.log('[PWA] Install prompt outcome:', outcome);

    // Clear the prompt
    deferredPrompt = null;
    hideInstallButton();

    return outcome === 'accepted';
  }

  /**
   * Show update notification
   */
  function showUpdateNotification() {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'pwa-update-notification';
    notification.innerHTML = `
      <span>En ny version av TheHUB finns tillgänglig</span>
      <button onclick="HubPWA.applyUpdate()">Uppdatera</button>
      <button onclick="this.parentElement.remove()" aria-label="Stäng">&#x2715;</button>
    `;
    document.body.appendChild(notification);

    // Animate in
    requestAnimationFrame(() => {
      notification.classList.add('visible');
    });
  }

  /**
   * Apply service worker update
   */
  function applyUpdate() {
    if (swRegistration && swRegistration.waiting) {
      swRegistration.waiting.postMessage('skipWaiting');
    }
    window.location.reload();
  }

  /**
   * Check if app is installed (running as PWA)
   */
  function isInstalled() {
    // Check display mode
    if (window.matchMedia('(display-mode: standalone)').matches) {
      return true;
    }

    // Check iOS standalone
    if (window.navigator.standalone === true) {
      return true;
    }

    // Check if launched from home screen on Android
    if (document.referrer.includes('android-app://')) {
      return true;
    }

    return false;
  }

  /**
   * Get install instructions for current platform
   */
  function getInstallInstructions() {
    const ua = navigator.userAgent;

    if (/iPhone|iPad|iPod/.test(ua)) {
      return {
        platform: 'iOS',
        steps: [
          'Tryck på dela-knappen i Safari',
          'Scrolla ner och tryck "Lägg till på hemskärmen"',
          'Tryck "Lägg till"'
        ]
      };
    }

    if (/Android/.test(ua)) {
      return {
        platform: 'Android',
        steps: [
          'Tryck på menyn i Chrome',
          'Välj "Lägg till på startskärmen"',
          'Tryck "Lägg till"'
        ]
      };
    }

    return {
      platform: 'Desktop',
      steps: [
        'Klicka på installera-ikonen i adressfältet',
        'Eller använd webbläsarmenyn - "Installera app"'
      ]
    };
  }

  /**
   * Show iOS install instructions modal
   */
  function showIOSInstallGuide() {
    const modal = document.createElement('div');
    modal.className = 'pwa-ios-modal';
    modal.innerHTML = `
      <div class="pwa-ios-modal-content">
        <button class="pwa-ios-modal-close" onclick="this.parentElement.parentElement.remove()">&#x2715;</button>
        <div class="pwa-ios-modal-icon">📲</div>
        <h2>Installera TheHUB</h2>
        <p>Lägg till appen på din hemskärm för bästa upplevelse:</p>
        <ol>
          <li>Tryck på <span class="pwa-ios-share-icon">&#x2B06;&#xFE0E;</span> dela-knappen i Safari</li>
          <li>Scrolla och tryck <strong>"Lägg till på hemskärmen"</strong></li>
          <li>Tryck <strong>"Lägg till"</strong></li>
        </ol>
        <button class="pwa-ios-modal-btn" onclick="this.parentElement.parentElement.remove()">Jag förstår</button>
      </div>
    `;
    document.body.appendChild(modal);

    // Animate in
    requestAnimationFrame(() => {
      modal.classList.add('visible');
    });
  }

  /**
   * Initialize PWA functionality
   */
  function init() {
    // Register service worker
    registerServiceWorker();

    // Listen for install prompt (Chrome, Edge, Samsung Internet)
    window.addEventListener('beforeinstallprompt', handleInstallPrompt);

    // Listen for successful install
    window.addEventListener('appinstalled', () => {
      console.log('[PWA] App installed successfully');
      hideInstallButton();
      deferredPrompt = null;
    });

    // Handle service worker updates on page load
    if (navigator.serviceWorker) {
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        window.location.reload();
      });
    }

    // Add installed class to body if running as PWA
    if (isInstalled()) {
      document.body.classList.add('pwa-installed');
      console.log('[PWA] Running as installed app');
    }

    // Bind install button click
    document.addEventListener('click', (e) => {
      const installBtn = e.target.closest('[data-pwa-install]');
      if (installBtn) {
        // iOS needs special handling
        if (/iPhone|iPad|iPod/.test(navigator.userAgent) && !window.navigator.standalone) {
          showIOSInstallGuide();
        } else if (deferredPrompt) {
          promptInstall();
        }
      }
    });
  }

  // Public API
  return {
    init,
    promptInstall,
    isInstalled,
    getInstallInstructions,
    showIOSInstallGuide,
    applyUpdate
  };
})();

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', HubPWA.init);
} else {
  HubPWA.init();
}
