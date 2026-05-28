/**
 * Options Page Script
 */
document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('settings-form');
  const apiKeyInput = document.getElementById('api-key');
  const enabledCheckbox = document.getElementById('enabled');
  const messageDiv = document.getElementById('message');

  /**
   * Show message to user
   */
  const showMessage = (text, type) => {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.hidden = false;

    setTimeout(() => {
      messageDiv.hidden = true;
    }, 3000);
  };

  /**
   * Load current settings
   */
  const loadSettings = async () => {
    try {
      const response = await chrome.runtime.sendMessage({ action: 'getSettings' });

      if (response.success) {
        apiKeyInput.value = response.settings.apiKey || '';
        enabledCheckbox.checked = response.settings.enabled !== false;
      }
    } catch (error) {
      console.error('[Options] Error loading settings:', error);
      showMessage('Failed to load settings', 'error');
    }
  };

  /**
   * Validate API key format
   */
  const validateApiKey = (key) => {
    if (!key) return true; // Empty is allowed
    if (key.length < 10) return false;
    if (key.length > 200) return false;
    return true;
  };

  /**
   * Save settings
   */
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const apiKey = apiKeyInput.value.trim();
    const enabled = enabledCheckbox.checked;

    // Validate
    if (!validateApiKey(apiKey)) {
      showMessage('Invalid API key format', 'error');
      return;
    }

    try {
      const response = await chrome.runtime.sendMessage({
        action: 'saveSettings',
        settings: { apiKey, enabled }
      });

      if (response.success) {
        showMessage('Settings saved successfully', 'success');
      } else {
        throw new Error(response.error);
      }
    } catch (error) {
      console.error('[Options] Error saving settings:', error);
      showMessage('Failed to save settings', 'error');
    }
  });

  // Initialize
  await loadSettings();
});
