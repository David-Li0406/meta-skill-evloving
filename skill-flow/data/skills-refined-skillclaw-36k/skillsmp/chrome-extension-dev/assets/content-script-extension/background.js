// Service worker for content script extension

// Listen for extension install
chrome.runtime.onInstalled.addListener(() => {
  console.log('Content Script Extension installed');
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getPageInfo') {
    console.log('Page info received:', request);
  }
});