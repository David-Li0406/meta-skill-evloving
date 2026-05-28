/**
 * Popup Script
 */
document.addEventListener('DOMContentLoaded', async () => {
  const statusDot = document.querySelector('.status-dot');
  const statusText = document.getElementById('status-text');
  const actionBtn = document.getElementById('action-btn');
  const optionsLink = document.getElementById('options-link');

  // Load and display settings
  const loadStatus = async () => {
    try {
      const response = await chrome.runtime.sendMessage({ action: 'getSettings' });

      if (response.success) {
        const { enabled, apiKey } = response.settings;

        if (!apiKey) {
          statusDot.classList.add('error');
          statusText.textContent = 'API key not set';
          actionBtn.disabled = true;
        } else if (enabled) {
          statusDot.classList.add('active');
          statusText.textContent = 'Active';
          actionBtn.disabled = false;
        } else {
          statusText.textContent = 'Disabled';
          actionBtn.disabled = true;
        }
      }
    } catch (error) {
      statusDot.classList.add('error');
      statusText.textContent = 'Error loading status';
      console.error('[Popup] Error:', error);
    }
  };

  // Handle action button click
  actionBtn.addEventListener('click', async () => {
    actionBtn.disabled = true;
    actionBtn.textContent = 'Running...';

    try {
      // Get current tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      // Send message to content script or background
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'runAction' });

      if (response.success) {
        actionBtn.textContent = 'Done!';
        setTimeout(() => {
          actionBtn.textContent = 'Run Action';
          actionBtn.disabled = false;
        }, 1500);
      } else {
        throw new Error(response.error);
      }
    } catch (error) {
      console.error('[Popup] Action failed:', error);
      actionBtn.textContent = 'Failed';
      setTimeout(() => {
        actionBtn.textContent = 'Run Action';
        actionBtn.disabled = false;
      }, 1500);
    }
  });

  // Open options page
  optionsLink.addEventListener('click', (e) => {
    e.preventDefault();
    chrome.runtime.openOptionsPage();
  });

  // Initialize
  await loadStatus();
});
