# Browser Extension Builder

## Patterns


---
  #### **Name**
Extension Architecture
  #### **Description**
Structure for modern browser extensions
  #### **When To Use**
When starting a new extension
  #### **Implementation**
    ## Extension Architecture
    
    ### Project Structure
    ```
    extension/
    ├── manifest.json      # Extension config
    ├── popup/
    │   ├── popup.html     # Popup UI
    │   ├── popup.css
    │   └── popup.js
    ├── content/
    │   └── content.js     # Runs on web pages
    ├── background/
    │   └── service-worker.js  # Background logic
    ├── options/
    │   ├── options.html   # Settings page
    │   └── options.js
    └── icons/
        ├── icon16.png
        ├── icon48.png
        └── icon128.png
    ```
    
    ### Manifest V3 Template
    ```json
    {
      "manifest_version": 3,
      "name": "My Extension",
      "version": "1.0.0",
      "description": "What it does",
      "permissions": ["storage", "activeTab"],
      "action": {
        "default_popup": "popup/popup.html",
        "default_icon": {
          "16": "icons/icon16.png",
          "48": "icons/icon48.png",
          "128": "icons/icon128.png"
        }
      },
      "content_scripts": [{
        "matches": ["<all_urls>"],
        "js": ["content/content.js"]
      }],
      "background": {
        "service_worker": "background/service-worker.js"
      },
      "options_page": "options/options.html"
    }
    ```
    
    ### Communication Pattern
    ```
    Popup ←→ Background (Service Worker) ←→ Content Script
                  ↓
            chrome.storage
    ```
    

---
  #### **Name**
Content Scripts
  #### **Description**
Code that runs on web pages
  #### **When To Use**
When modifying or reading page content
  #### **Implementation**
    ## Content Scripts
    
    ### Basic Content Script
    ```javascript
    // content.js - Runs on every matched page
    
    // Wait for page to load
    document.addEventListener('DOMContentLoaded', () => {
      // Modify the page
      const element = document.querySelector('.target');
      if (element) {
        element.style.backgroundColor = 'yellow';
      }
    });
    
    // Listen for messages from popup/background
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (message.action === 'getData') {
        const data = document.querySelector('.data')?.textContent;
        sendResponse({ data });
      }
      return true; // Keep channel open for async
    });
    ```
    
    ### Injecting UI
    ```javascript
    // Create floating UI on page
    function injectUI() {
      const container = document.createElement('div');
      container.id = 'my-extension-ui';
      container.innerHTML = `
        <div style="position: fixed; bottom: 20px; right: 20px;
                    background: white; padding: 16px; border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 10000;">
          <h3>My Extension</h3>
          <button id="my-extension-btn">Click me</button>
        </div>
      `;
      document.body.appendChild(container);
    
      document.getElementById('my-extension-btn').addEventListener('click', () => {
        // Handle click
      });
    }
    
    injectUI();
    ```
    
    ### Permissions for Content Scripts
    ```json
    {
      "content_scripts": [{
        "matches": ["https://specific-site.com/*"],
        "js": ["content.js"],
        "run_at": "document_end"
      }]
    }
    ```
    

---
  #### **Name**
Storage and State
  #### **Description**
Persisting extension data
  #### **When To Use**
When saving user settings or data
  #### **Implementation**
    ## Storage and State
    
    ### Chrome Storage API
    ```javascript
    // Save data
    chrome.storage.local.set({ key: 'value' }, () => {
      console.log('Saved');
    });
    
    // Get data
    chrome.storage.local.get(['key'], (result) => {
      console.log(result.key);
    });
    
    // Sync storage (syncs across devices)
    chrome.storage.sync.set({ setting: true });
    
    // Watch for changes
    chrome.storage.onChanged.addListener((changes, area) => {
      if (changes.key) {
        console.log('key changed:', changes.key.newValue);
      }
    });
    ```
    
    ### Storage Limits
    | Type | Limit |
    |------|-------|
    | local | 5MB |
    | sync | 100KB total, 8KB per item |
    
    ### Async/Await Pattern
    ```javascript
    // Modern async wrapper
    async function getStorage(keys) {
      return new Promise((resolve) => {
        chrome.storage.local.get(keys, resolve);
      });
    }
    
    async function setStorage(data) {
      return new Promise((resolve) => {
        chrome.storage.local.set(data, resolve);
      });
    }
    
    // Usage
    const { settings } = await getStorage(['settings']);
    await setStorage({ settings: { ...settings, theme: 'dark' } });
    ```
    

---
  #### **Name**
Extension Monetization
  #### **Description**
Making money from extensions
  #### **When To Use**
When planning extension revenue
  #### **Implementation**
    ## Extension Monetization
    
    ### Revenue Models
    | Model | How It Works |
    |-------|--------------|
    | Freemium | Free basic, paid features |
    | One-time | Pay once, use forever |
    | Subscription | Monthly/yearly access |
    | Donations | Tip jar / Buy me a coffee |
    | Affiliate | Recommend products |
    
    ### Payment Integration
    ```javascript
    // Use your backend for payments
    // Extension can't directly use Stripe
    
    // 1. User clicks "Upgrade" in popup
    // 2. Open your website with user ID
    chrome.tabs.create({
      url: `https://your-site.com/upgrade?user=${userId}`
    });
    
    // 3. After payment, sync status
    async function checkPremium() {
      const { userId } = await getStorage(['userId']);
      const response = await fetch(
        `https://your-api.com/premium/${userId}`
      );
      const { isPremium } = await response.json();
      await setStorage({ isPremium });
      return isPremium;
    }
    ```
    
    ### Feature Gating
    ```javascript
    async function usePremiumFeature() {
      const { isPremium } = await getStorage(['isPremium']);
      if (!isPremium) {
        showUpgradeModal();
        return;
      }
      // Run premium feature
    }
    ```
    
    ### Chrome Web Store Payments
    - Chrome discontinued built-in payments
    - Use your own payment system
    - Link to external checkout page
    

## Anti-Patterns


---
  #### **Name**
Requesting All Permissions
  #### **Description**
Asking for permissions you don't need
  #### **Why Bad**
    Users won't install.
    Store may reject.
    Security risk.
    Bad reviews.
    
  #### **What To Do Instead**
    Request minimum needed.
    Use optional permissions.
    Explain why in description.
    Request at time of use.
    

---
  #### **Name**
Heavy Background Processing
  #### **Description**
Service worker doing too much
  #### **Why Bad**
    MV3 terminates idle workers.
    Battery drain.
    Browser slows down.
    Users uninstall.
    
  #### **What To Do Instead**
    Keep background minimal.
    Use alarms for periodic tasks.
    Offload to content scripts.
    Cache aggressively.
    

---
  #### **Name**
Breaking on Updates
  #### **Description**
Extension breaks when sites update
  #### **Why Bad**
    Selectors change.
    APIs change.
    Angry users.
    Bad reviews.
    
  #### **What To Do Instead**
    Use stable selectors.
    Add error handling.
    Monitor for breakage.
    Update quickly when broken.
    