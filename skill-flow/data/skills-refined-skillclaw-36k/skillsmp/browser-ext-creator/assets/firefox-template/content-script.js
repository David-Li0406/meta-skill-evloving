/**
 * Content Script (Firefox)
 * Uses browser.* API with Promise support
 */
(() => {
  'use strict';

  const CONTAINER_ID = 'my-extension-container';

  /**
   * Initialize the extension UI on the page
   */
  const init = () => {
    // Avoid duplicate initialization
    if (document.querySelector(`#${CONTAINER_ID}`)) {
      return;
    }

    // Create container element
    const container = document.createElement('div');
    container.id = CONTAINER_ID;

    // Add your UI elements here
    const button = document.createElement('button');
    button.textContent = 'Extension Button';
    button.addEventListener('click', handleButtonClick);

    container.appendChild(button);
    document.body.appendChild(container);

    console.log('[Extension] Initialized');
  };

  /**
   * Handle button click
   */
  const handleButtonClick = async () => {
    try {
      // Firefox uses browser.* API with native Promise support
      const response = await browser.runtime.sendMessage({
        action: 'getData',
        url: window.location.href
      });

      if (response.success) {
        console.log('[Extension] Data received:', response.data);
      } else {
        console.error('[Extension] Error:', response.error);
      }
    } catch (error) {
      console.error('[Extension] Failed to send message:', error);
    }
  };

  /**
   * Clean up when extension is removed or page changes
   */
  const cleanup = () => {
    const container = document.querySelector(`#${CONTAINER_ID}`);
    if (container) {
      container.remove();
    }
  };

  // Initialize based on document state
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Handle SPA navigation (URL changes without page reload)
  let lastUrl = location.href;
  const observer = new MutationObserver(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      cleanup();
      init();
    }
  });

  observer.observe(document.body, {
    subtree: true,
    childList: true
  });
})();
