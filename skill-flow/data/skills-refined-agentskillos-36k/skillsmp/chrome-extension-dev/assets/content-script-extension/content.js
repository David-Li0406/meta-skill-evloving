// Content script runs in the context of web pages

console.log('Content script loaded on:', window.location.href);

// Example: Add notification to page
function addNotification() {
  const notification = document.createElement('div');
  notification.textContent = 'This page has been modified by Content Script Extension';
  notification.style.cssText = `
    position: fixed;
    top: 10px;
    right: 10px;
    background: #4CAF50;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    z-index: 999999;
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  `;
  
  document.body.appendChild(notification);
  
  // Remove after 3 seconds
  setTimeout(() => notification.remove(), 3000);
}

// Wait for page to be fully loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', addNotification);
} else {
  addNotification();
}

// Listen for messages from background or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getPageInfo') {
    sendResponse({
      title: document.title,
      url: window.location.href
    });
  }
});