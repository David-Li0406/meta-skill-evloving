/**
 * Background Script (Firefox)
 * Uses browser.* API with native Promise support
 */

// Extension installed/updated
browser.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('[Background] Extension installed');
    // Initialize default settings
    browser.storage.sync.set({
      enabled: true,
      apiKey: ''
    });
  } else if (details.reason === 'update') {
    console.log('[Background] Extension updated');
  }
});

// Message handler
browser.runtime.onMessage.addListener((request, sender) => {
  console.log('[Background] Message received:', request.action);

  switch (request.action) {
    case 'getData':
      return handleGetData(request);

    case 'getSettings':
      return handleGetSettings();

    case 'saveSettings':
      return handleSaveSettings(request.settings);

    default:
      return Promise.resolve({ success: false, error: 'Unknown action' });
  }
});

/**
 * Fetch data from external API
 */
const handleGetData = async (request) => {
  try {
    const { apiKey } = await browser.storage.sync.get(['apiKey']);

    if (!apiKey) {
      return { success: false, error: 'API key not configured' };
    }

    const response = await fetch('https://api.example.com/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({ url: request.url })
    });

    if (!response.ok) {
      return { success: false, error: `HTTP error: ${response.status}` };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

/**
 * Get settings from storage
 */
const handleGetSettings = async () => {
  try {
    const settings = await browser.storage.sync.get({
      enabled: true,
      apiKey: ''
    });
    return { success: true, settings };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

/**
 * Save settings to storage
 */
const handleSaveSettings = async (settings) => {
  try {
    await browser.storage.sync.set(settings);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
