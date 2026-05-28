# Zimlet Sideloader Setup Guide

Complete guide for setting up the Zimbra zimlet sideloader for local development.

## Prerequisites

- Chrome or Firefox browser
- Node.js 14+ installed
- Access to Zimbra Modern Web Client
- Git for cloning repository

## Installation Methods

### Method 1: Build from Source (Recommended)

```bash
# Clone the sideloader repository
git clone https://github.com/Zimbra/zm-x-sideloader.git
cd zm-x-sideloader

# Install dependencies
npm install

# Build the extension
npm run build

# Output is in dist/ directory
```

### Method 2: Pre-built Release

Check [Zimbra releases](https://github.com/Zimbra/zm-x-sideloader/releases) for pre-built extension packages.

## Browser Installation

### Chrome

1. Open `chrome://extensions/`
2. Enable "Developer mode" (top-right toggle)
3. Click "Load unpacked"
4. Select the `zm-x-sideloader/dist` directory
5. Pin the extension icon for easy access

### Firefox

1. Open `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on..."
3. Select any file in `zm-x-sideloader/dist`
4. Note: Firefox temporary add-ons don't persist after restart

### Edge (Chromium)

1. Open `edge://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `zm-x-sideloader/dist` directory

## Configuration

### Basic Setup

1. Click sideloader extension icon
2. You'll see an empty list of sideloaded zimlets
3. Input field for adding zimlet URLs

### Adding a Local Zimlet

1. Start your local zimlet dev server:
   ```bash
   cd my-zimlet
   zimlet watch
   # Shows: Listening on http://localhost:8081
   ```

2. Click sideloader icon in browser
3. Enter URL: `http://localhost:8081/index.js`
4. Click "Add" or press Enter
5. Navigate to Zimbra Modern Web Client
6. Refresh the page

### Multiple Zimlets

You can sideload multiple zimlets simultaneously:
- Each on a different port (8081, 8082, etc.)
- Add each URL separately to sideloader

## Server CORS Configuration (Optional)

For some features, you may need to enable CORS on Zimbra:

```bash
# On Zimbra server (as zimbra user)
zmprov mcf +zimbraResponseHeader "Access-Control-Allow-Origin: *"
zmmailboxdctl restart
```

**Warning:** Only do this on development servers.

## Development Workflow

### Recommended Flow

```
Terminal 1: zimlet watch
Terminal 2: (optional) Additional tasks

Browser:
1. Sideloader configured with local URL
2. Zimbra Modern Web Client open
3. DevTools open for debugging

Edit Code → Auto-rebuild → Refresh Browser → Test
```

### Hot Reload

The `zimlet watch` command rebuilds automatically on file changes. After rebuild:
- Simple refresh (F5) usually picks up changes
- Hard refresh (Ctrl+Shift+R) for cached issues
- Clear browser cache if problems persist

## Troubleshooting

### Zimlet Not Loading

1. **Check dev server is running:**
   ```bash
   curl http://localhost:8081/index.js
   ```

2. **Verify sideloader configuration:**
   - Click extension icon
   - Confirm URL is in the list
   - Check for error indicators

3. **Check browser console:**
   - Look for CORS errors
   - Look for 404 errors
   - Look for JavaScript syntax errors

### CORS Errors

If seeing `Access-Control-Allow-Origin` errors:

**Option 1:** Configure Zimbra server (see above)

**Option 2:** Use CORS browser extension (dev only):
- Chrome: "CORS Unblock" or similar
- Enable only when developing

### Build Errors

```bash
# Clean and rebuild
rm -rf node_modules dist
npm install
npm run build
```

### Extension Not Working

1. Check extension permissions
2. Try reloading the extension
3. Rebuild from source
4. Check browser console for extension errors

## Verifying Sideloader Works

1. Add a simple `console.log` to your zimlet:
   ```javascript
   export default function Zimlet(context) {
       console.log('[MyZimlet] Sideloader working!');
       // ...
   }
   ```

2. Add URL to sideloader
3. Open Zimbra and browser DevTools
4. Look for your log message in console
