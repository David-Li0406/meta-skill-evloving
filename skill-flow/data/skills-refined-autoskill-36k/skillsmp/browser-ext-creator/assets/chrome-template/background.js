/**
 * Background Service Worker
 * Handles background tasks, API calls, and message passing
 */

// Extension installed/updated
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('[Background] Extension installed');
    // Initialize default settings
    chrome.storage.sync.set({
      enabled: true,
      apiKey: ''
    });
  } else if (details.reason === 'update') {
    console.log('[Background] Extension updated');
  }
});

// Message handler
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[Background] Message received:', request.action);

  switch (request.action) {
    case 'getData':
      handleGetData(request)
        .then((data) => sendResponse({ success: true, data }))
        .catch((error) => sendResponse({ success: false, error: error.message }));
      return true; // Keep message channel open for async response

    case 'getSettings':
      handleGetSettings()
        .then((settings) => sendResponse({ success: true, settings }))
        .catch((error) => sendResponse({ success: false, error: error.message }));
      return true;

    case 'saveSettings':
      handleSaveSettings(request.settings)
        .then(() => sendResponse({ success: true }))
        .catch((error) => sendResponse({ success: false, error: error.message }));
      return true;

    default:
      sendResponse({ success: false, error: 'Unknown action' });
      return false;
  }
});

/**
 * Fetch data from external API
 */
const handleGetData = async (request) => {
  const { apiKey } = await chrome.storage.sync.get(['apiKey']);

  if (!apiKey) {
    throw new Error('API key not configured');
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
    throw new Error(`HTTP error: ${response.status}`);
  }

  return response.json();
};

/**
 * Get settings from storage
 */
const handleGetSettings = async () => {
  return chrome.storage.sync.get({
    enabled: true,
    apiKey: ''
  });
};

/**
 * Save settings to storage
 */
const handleSaveSettings = async (settings) => {
  await chrome.storage.sync.set(settings);
};
