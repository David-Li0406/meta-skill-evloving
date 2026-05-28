# Chrome Extension APIs Reference

Complete reference for Chrome Extension Manifest V3 APIs.

## Action API

Toolbar icon interaction and badge management.

```javascript
// Set badge text
chrome.action.setBadgeText({text: "1"});
chrome.action.setBadgeTextColor({color: "#FFFFFF"});
chrome.action.setBadgeBackgroundColor({color: "#FF0000"});

// Set icon
chrome.action.setIcon({
  path: {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png"
  }
});

// Open popup (programmatically)
chrome.action.openPopup();

// Handle icon click (when no popup)
chrome.action.onClicked.addListener((tab) => {
  console.log('Clicked on tab:', tab.id);
});
```

## Storage API

Persistent data storage with three types.

### Local Storage
```javascript
// Save data
chrome.storage.local.set({key: 'value', number: 123});

// Get data
chrome.storage.local.get(['key'], (result) => {
  console.log(result.key);
});

// Promise-based
chrome.storage.local.get(['key']).then((result) => {
  console.log(result.key);
});

// Get all data
chrome.storage.local.get(null, (result) => {
  console.log(result);
});

// Remove data
chrome.storage.local.remove(['key']);

// Clear all
chrome.storage.local.clear();

// Watch for changes
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.key) {
    console.log('Old value:', changes.key.oldValue);
    console.log('New value:', changes.key.newValue);
  }
});
```

### Sync Storage (synchronizes across devices)
```javascript
chrome.storage.sync.set({preferences: {theme: 'dark'}});
chrome.storage.sync.get(['preferences'], (result) => {
  console.log(result.preferences);
});

// Limit: 102,400 bytes (100KB)
```

### Session Storage (in-memory only)
```javascript
chrome.storage.session.set({tempData: 'value'});
chrome.storage.session.get(['tempData'], (result) => {
  console.log(result.tempData);
});
```

## Tabs API

Tab management and interaction.

```javascript
// Query tabs
chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
  const activeTab = tabs[0];
});

// Get specific tab
chrome.tabs.get(tabId, (tab) => {
  console.log(tab.url);
});

// Create new tab
chrome.tabs.create({url: 'https://example.com'});

// Update tab
chrome.tabs.update(tabId, {url: 'https://newurl.com'});

// Send message to content script
chrome.tabs.sendMessage(tabId, {action: 'getData'}, (response) => {
  console.log(response);
});

// React to tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    console.log('Tab loaded:', tab.url);
  }
});

// React to tab activation
chrome.tabs.onActivated.addListener((activeInfo) => {
  console.log('Tab activated:', activeInfo.tabId);
});
```

## Runtime API

Extension lifecycle and messaging.

### Messaging

```javascript
// Send message from content script to background
chrome.runtime.sendMessage({action: 'getData'}, (response) => {
  console.log(response);
});

// Listen for messages in background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'getData') {
    sendResponse({data: 'example'});
    return true; // Required for async response
  }
});

// Send message to specific tab
chrome.tabs.sendMessage(tabId, {greeting: 'hello'}, (response) => {
  console.log(response.farewell);
});
```

### Extension Information

```javascript
// Get extension URL
const iconUrl = chrome.runtime.getURL('icons/icon48.png');

// Get extension ID
const extensionId = chrome.runtime.id;

// Reload extension
document.location.reload(); // In extension page
chrome.runtime.reload(); // From script

// Connect long-lived port
const port = chrome.runtime.connect({name: 'my-port'});
port.postMessage({action: 'init'});
port.onMessage.addListener((message) => {
  console.log(message);
});
```

### On Install/Update

```javascript
// In service worker
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Extension installed');
    // Set default values
    chrome.storage.local.set({enabled: true});
  } else if (details.reason === 'update') {
    console.log('Updated from version:', details.previousVersion);
  }
});
```

## Scripting API

Dynamic script and style injection.

```javascript
// Inject function
chrome.scripting.executeScript({
  target: {tabId: tabId},
  func: () => {
    document.body.style.backgroundColor = 'red';
  }
});

// Inject script file
chrome.scripting.executeScript({
  target: {tabId: tabId},
  files: ['content.js']
});

// Inject multiple scripts
chrome.scripting.executeScript({
  target: {tabId: tabId},
  files: ['lib.js', 'content.js']
});

// Inject CSS
chrome.scripting.insertCSS({
  target: {tabId: tabId},
  css: 'body { background-color: red; }'
});

// Inject CSS file
chrome.scripting.insertCSS({
  target: {tabId: tabId},
  files: ['styles.css']
});

// Get all content scripts
chrome.scripting.getRegisteredContentScripts({
  tabId: tabId
}, (scripts) => {
  console.log(scripts);
});
```

## Alarms API

Scheduling tasks.

```javascript
// Create alarm
chrome.alarms.create('refresh', {
  delayInMinutes: 10,
  periodInMinutes: 60
});

// Listen for alarms
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'refresh') {
    console.log('Refreshing data...');
    // Perform task
  }
});

// Clear alarm
chrome.alarms.clear('refresh');

// Get all alarms
chrome.alarms.getAll((alarms) => {
  console.log(alarms);
});
```

## Notifications API

System notifications.

```json
// manifest.json
{
  "permissions": ["notifications"]
}
```

```javascript
// Create notification
chrome.notifications.create({
  type: 'basic',
  iconUrl: 'icons/icon48.png',
  title: 'Notification Title',
  message: 'Notification message content',
  priority: 2
});

// Listen for click
chrome.notifications.onClicked.addListener((notificationId) => {
  console.log('Clicked:', notificationId);
});
```

## Context Menus API

Right-click context menus.

```json
// manifest.json
{
  "permissions": ["contextMenus"]
}
```

```javascript
// Create menu item
chrome.contextMenus.create({
  id: 'my-menu',
  title: 'My Menu Item',
  contexts: ['selection', 'link']
});

// Listen for clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'my-menu') {
    console.log('Selected text:', info.selectionText);
  }
});

// Update menu
chrome.contextMenus.update('my-menu', {
  title: 'Updated Title'
});

// Remove menu
chrome.contextMenus.remove('my-menu');
```

## Web Navigation API

Navigation event monitoring.

```json
// manifest.json
{
  "permissions": ["webNavigation"]
}
```

```javascript
// Listen for navigation
chrome.webNavigation.onCompleted.addListener((details) => {
  if (details.frameId === 0) { // Main frame only
    console.log('Navigated to:', details.url);
  }
});

// Listen for errors
chrome.webNavigation.onErrorOccurred.addListener((details) => {
  console.log('Navigation error:', details.error);
});
```

## DevTools API

DevTools panel creation.

```json
// manifest.json
{
  "devtools_page": "devtools.html"
}
```

```javascript
// devtools.js
chrome.devtools.panels.create(
  'My Panel',
  'icons/icon16.png',
  'panel.html',
  (panel) => {
    console.log('Panel created');
  }
);
```

## Commands API

Keyboard shortcuts.

```json
// manifest.json
{
  "commands": {
    "run-command": {
      "suggested_key": {
        "default": "Ctrl+Shift+Y",
        "mac": "Command+Shift+Y"
      },
      "description": "Run my command"
    }
  }
}
```

```javascript
chrome.commands.onCommand.addListener((command) => {
  if (command === 'run-command') {
    console.log('Command executed');
  }
});
```
