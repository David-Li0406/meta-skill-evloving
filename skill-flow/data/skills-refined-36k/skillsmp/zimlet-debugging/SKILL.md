---
name: Zimlet Debugging
description: This skill should be used when the user asks about "zimlet sideloader", "debug zimlet", "zimlet not loading", "zimlet error", "zimlet console", "zimlet dev mode", "zimlet hot reload", "zimlet breakpoint", or mentions troubleshooting zimlet development. Covers debugging techniques for both Classic and Modern zimlets.
version: 1.0.0
---

# Zimlet Debugging

Comprehensive guide for debugging zimlets during development and troubleshooting production issues.

> **💡 Pro Tip:** Mastering Zimbra debugging requires being a "Full-Stack Detective" - errors can occur in the browser, network transport (SOAP/GraphQL), or deep in the Java server.

## The "Secret" URL Parameters

The most important debugging step is telling Zimbra to stop hiding its code:

| Parameter | Description |
|-----------|-------------|
| `?dev=1` | **Developer Mode** - Forces unminified source files so breakpoints work |
| `?debug=1` | Opens built-in Zimbra debug window showing SOAP traffic in real-time |
| `?debug=2` | More verbose debug output |
| `?debug=3` | Maximum verbosity for SOAP/request debugging |
| `?mode=mjsf` | **Multiple JS Files** - Loads every JS file separately for reliable breakpoints |
| `?zimletSlots=show` | **Modern UI** - Visualizes all available slot locations |

**Example URLs:**
```
https://mail.yourdomain.com/?dev=1
https://mail.yourdomain.com/?dev=1&debug=3
https://mail.yourdomain.com/modern/?zimletSlots=show
```

## Development Setup

### Modern Zimlets (Sideloader)

The sideloader enables local development without deploying to the server.

#### Install Sideloader Extension

1. Build the sideloader extension:
```bash
git clone https://github.com/Zimbra/zm-x-sideloader
cd zm-x-sideloader
npm install
npm run build
```

2. Load in Chrome:
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select `zm-x-sideloader/dist`

#### Configure Sideloader

1. Click the sideloader extension icon in Chrome
2. Add your local zimlet URL (e.g., `http://localhost:8081/index.js`)
3. Navigate to your Zimbra Modern Web Client
4. The sideloader injects your local zimlet code

#### Local Development Workflow

```bash
# Start zimlet dev server
cd my-zimlet
zimlet watch

# Output:
# Listening on http://localhost:8081
# Zimlet available at http://localhost:8081/index.js

# Add this URL to sideloader extension
# Refresh Zimbra web client to see changes
```

### Classic Zimlets (Dev Mode)

Enable unminified JavaScript:

```
https://mail.domain.com/?dev=1
```

Or set server-wide:

```bash
zmprov ms mail.domain.com zimbraZimletDevMode TRUE
zmmailboxdctl restart
```

## Browser Developer Tools

### Console Logging

#### Modern Zimlet Logging

```javascript
// Add logging throughout your code
export default function Zimlet(context) {
    console.log('[MyZimlet] Initializing with context:', context);

    const { plugins } = context;

    plugins.register('my-zimlet', {
        menu: {
            handler: function(menu, ctx) {
                console.log('[MyZimlet] Menu handler called');
                console.log('[MyZimlet] Current account:', ctx.account);
                return [];
            }
        }
    });
}
```

#### Classic Zimlet Logging

```javascript
com_mycompany_myzimlet_HandlerObject.prototype.init = function() {
    // Option 1: Standard console (appears in browser DevTools)
    console.log("[MyZimlet] init() called");

    // Option 2: Zimbra Status Message (appears in UI - recommended!)
    var appCtxt = this.getContext(); // or window.appCtxt
    appCtxt.setStatusMsg("MyZimlet initialized!", ZmStatusView.LEVEL_INFO);

    // Option 3: AjxDebug for verbose debugging
    DBG.println(AjxDebug.DBG1, "[MyZimlet] Debug level message");

    // Option 4: Debug window (requires ?debug=1 URL param)
    AjxDebug.println("[MyZimlet] User properties: " + this.getUserProperty("allProperties"));
};
```

**Tip:** Prefer `setStatusMsg()` over `console.log` for quick visual feedback during development.

### Network Tab Analysis

Monitor GraphQL and SOAP requests:

1. Open DevTools → Network tab
2. Filter by:
   - `graphql` for Modern zimlets
   - `service/soap` for Classic zimlets
3. Inspect request/response payloads
4. Check for error responses (look for `faultcode`)

**Pro Tip - Replay Attacks:** If an API call fails, don't refresh the page repeatedly:
1. Right-click the request in Network tab
2. Select "Copy as cURL"
3. Paste into Postman or terminal
4. Tweak parameters until it works

### Apollo DevTools (Modern UI)

For Modern zimlets using GraphQL, install the **Apollo Client DevTools** browser extension:

1. Install from Chrome/Firefox extension store
2. Open DevTools → Apollo tab
3. View the GraphQL cache state in memory
4. Inspect all queries and their cached results
5. See exactly what data is available to your components

This is essential because you can't debug GraphQL just by looking at network requests - you need to see the cache!

### Breakpoint Debugging

#### Source Maps (Modern)

```bash
# Build with source maps
zimlet build --sourcemaps

# Or in zimlet watch mode (enabled by default)
zimlet watch
```

Then in DevTools:
1. Go to Sources tab
2. Find your source files under `webpack://`
3. Set breakpoints in original source code

#### Classic Zimlet Breakpoints

```javascript
// Add debugger statement
com_mycompany_myzimlet_HandlerObject.prototype.singleClicked = function() {
    debugger; // Browser pauses here when DevTools open
    this._showDialog();
};
```

Or set breakpoints directly in browser:
1. Sources → find `com_mycompany_myzimlet.js`
2. Click line number to set breakpoint

## Common Issues and Solutions

### Zimlet Not Loading

#### Modern Zimlet

**Symptoms**: No errors, zimlet simply doesn't appear

**Debugging steps**:
```javascript
// 1. Verify entry point is exporting correctly
export default function Zimlet(context) {
    console.log('[DEBUG] Zimlet function called');
    // ...
}

// 2. Check slot registration
plugins.register('my-zimlet', exports);
console.log('[DEBUG] Registered exports:', exports);

// 3. Verify slots are enabled in zimlet.json
// Check: "slots": { "menu": true }
```

**Common causes**:
- Missing `export default` on zimlet function
- Slot not enabled in `zimlet.json`
- JavaScript error preventing initialization
- Zimlet not enabled for user's COS

**Check zimlet is deployed**:
```bash
zmzimletctl listZimlets | grep my-zimlet
```

#### Classic Zimlet

**Debugging steps**:
```bash
# Check zimlet is deployed
zmzimletctl listZimlets

# Check zimlet is enabled for COS
zmprov gc default zimbraZimletAvailableZimlets | grep my-zimlet

# Check for JavaScript errors in console
# Enable dev mode: ?dev=1
```

### Slot Not Rendering

```javascript
// Debug slot handler
exports.menu = {
    handler: function(menu, context) {
        console.log('[DEBUG] Menu slot handler called');
        console.log('[DEBUG] Menu param:', menu);
        console.log('[DEBUG] Context:', context);

        const items = [
            <MenuItem onClick={() => console.log('clicked')}>
                Test Item
            </MenuItem>
        ];

        console.log('[DEBUG] Returning items:', items);
        return items;
    }
};
```

**Common causes**:
- Handler returning `null` or `undefined`
- Handler throwing exception (check console)
- Slot name mismatch between code and manifest
- Component import error

### GraphQL Errors

```javascript
// Add error handling to queries
function MyComponent() {
    const { data, loading, error } = useQuery(MY_QUERY);

    if (error) {
        console.error('[MyZimlet] GraphQL error:', error);
        console.error('[MyZimlet] GraphQL error details:', error.graphQLErrors);
        console.error('[MyZimlet] Network error:', error.networkError);
        return <div>Error: {error.message}</div>;
    }

    // ... rest of component
}
```

**Common GraphQL issues**:
- Invalid field names (check schema)
- Missing required variables
- Authentication expired
- Permission denied

### CORS Errors (External APIs)

```javascript
// Symptom: Network requests to external APIs fail with CORS error

// Solution 1: Use proxy through Zimbra server
const response = await fetch('/service/proxy?target=' + encodeURIComponent(externalUrl));

// Solution 2: Configure external service to allow CORS
// Add headers: Access-Control-Allow-Origin: https://mail.domain.com

// Solution 3: Use server-side extension (if available)
```

### State Not Updating

```javascript
// Debug state changes
const [myState, setMyState] = useState(initialValue);

useEffect(() => {
    console.log('[DEBUG] State changed:', myState);
}, [myState]);

const handleUpdate = (newValue) => {
    console.log('[DEBUG] Setting state to:', newValue);
    setMyState(newValue);
};
```

**Common causes**:
- Not using state setter function correctly
- Mutating state directly instead of creating new object
- useEffect dependency array issues

## Performance Debugging

### Profile Renders

```javascript
import { Component } from 'preact';

class ProfiledComponent extends Component {
    componentDidUpdate(prevProps) {
        console.log('[PERF] Component updated');
        console.log('[PERF] Previous props:', prevProps);
        console.log('[PERF] New props:', this.props);
    }

    render() {
        console.log('[PERF] Rendering component');
        return <div>{/* ... */}</div>;
    }
}
```

### Check Bundle Size

```bash
# Analyze bundle
zimlet build --analyze

# Opens webpack-bundle-analyzer showing module sizes
```

### Memory Leaks

```javascript
// Clean up subscriptions and timers
function MyComponent() {
    useEffect(() => {
        const timer = setInterval(() => {
            console.log('tick');
        }, 1000);

        // Cleanup function
        return () => {
            console.log('[DEBUG] Cleaning up timer');
            clearInterval(timer);
        };
    }, []);
}
```

## Server-Side Debugging

### Enable Debug Logging for Specific Account

Turn on debug logging for a specific user without restarting the server:

```bash
# Enable debug logging for zimlet operations
zmprov addAccountLogger user@domain.com zimbra.zimlet debug

# View logs in real-time
tail -f /opt/zimbra/log/mailbox.log | grep -i "your_zimlet_name"

# Remove debug logging when done
zmprov removeAccountLogger user@domain.com zimbra.zimlet
```

### Check Zimlet Logs

```bash
# Zimlet deployment logs
tail -f /opt/zimbra/log/mailbox.log | grep -i zimlet

# Search for specific zimlet
grep "my-zimlet" /opt/zimbra/log/mailbox.log

# Watch for errors in real-time
tail -f /opt/zimbra/log/mailbox.log | grep -E "(ERROR|WARN|zimlet)"
```

### Verify Zimlet Configuration

```bash
# List deployed zimlets
zmzimletctl listZimlets

# Check zimlet properties
zmprov gaz my-zimlet

# Check zimlet enabled for COS
zmprov gc default zimbraZimletAvailableZimlets

# Check zimlet config
zmprov gcz com_mycompany_myzimlet
```

### Redeploy Zimlet

```bash
# Undeploy first
zmzimletctl undeploy my-zimlet

# Clear cache
zmprov fc all

# Redeploy
zmzimletctl deploy my-zimlet.zip

# Restart mailbox (if needed)
zmmailboxdctl restart
```

## Debug Checklist

### Modern Zimlet Not Working

- [ ] Sideloader extension installed and enabled
- [ ] Local URL added to sideloader
- [ ] `zimlet watch` running without errors
- [ ] Console shows "Zimlet function called"
- [ ] No JavaScript errors in console
- [ ] Slots enabled in `zimlet.json`
- [ ] `export default` present on main function
- [ ] Zimlet registered with `plugins.register()`

### Classic Zimlet Not Working

- [ ] Zimlet deployed: `zmzimletctl listZimlets`
- [ ] Enabled for COS: `zmprov gc default zimbraZimletAvailableZimlets`
- [ ] No XML syntax errors (check mailbox.log)
- [ ] Handler class name matches package name
- [ ] `init()` function called (add console.log)
- [ ] No JavaScript errors in console

## Quick Troubleshooting Table

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Zimlet doesn't appear | Cache or permissions | Run `zmprov fc zimlet` and check User Preferences → Zimlets tab |
| "Permission Denied" | `allowedDomains` not set | Check `config_template.xml` and whitelist the domain |
| JS changes not showing | Browser caching | Use `?dev=1` or hard-refresh (Ctrl+F5) |
| SOAP Error 500 | Bad XML/JSON | Inspect Network tab for missing required SOAP headers |
| External API fails | CORS blocked | Route through Zimbra proxy or whitelist in `config_template.xml` |
| White screen after load | JS syntax error | Check for `debugger;` statements in production code |
| Slot not rendering | Wrong slot name | Use `?zimletSlots=show` to verify slot names |
| "undefined is not a function" | Minification issue | Test with `?mode=mjsf` to load individual files |

## Additional Resources

### Reference Files

- **`references/sideloader-setup.md`** - Detailed sideloader configuration
- **`references/common-errors.md`** - Error message reference

### Example Files

- **`examples/debug-logging.js`** - Comprehensive logging setup
- **`examples/error-boundary.js`** - Error handling component

### Browser Extensions

- **Preact DevTools** - Inspect component state and props
- **Apollo Client DevTools** - Debug GraphQL cache and queries
- **React Developer Tools** - Works with Preact compatibility layer
