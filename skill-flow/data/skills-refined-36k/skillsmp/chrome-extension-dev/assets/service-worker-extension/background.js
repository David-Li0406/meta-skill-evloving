// Service Worker Example

// Initialize on install
chrome.runtime.onInstalled.addListener((details) => {
  console.log('Service Worker Extension installed');
  
  // Set default values
  chrome.storage.local.set({
    alarmCount: 0,
    lastAlarm: null
  });
  
  // Create periodic alarm
  chrome.alarms.create('periodic', {
    delayInMinutes: 1,
    periodInMinutes: 1
  });
});

// Handle alarms
chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === 'periodic') {
    const data = await chrome.storage.local.get(['alarmCount']);
    const count = (data.alarmCount || 0) + 1;
    
    await chrome.storage.local.set({
      alarmCount: count,
      lastAlarm: Date.now()
    });
    
    console.log('Alarm triggered, count:', count);
    
    // Show notification every 5 alarms
    if (count % 5 === 0) {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: chrome.runtime.getURL('icons/icon48.png'),
        title: 'Service Worker Alert',
        message: `Alarm has triggered ${count} times`
      });
    }
  }
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getStatus') {
    chrome.storage.local.get(['alarmCount', 'lastAlarm'], (data) => {
      sendResponse({
        count: data.alarmCount || 0,
        lastAlarm: data.lastAlarm
      });
    });
    return true;
  }
});

// Cleanup on uninstall
chrome.runtime.onSuspend.addListener(() => {
  console.log('Service worker suspending');
});