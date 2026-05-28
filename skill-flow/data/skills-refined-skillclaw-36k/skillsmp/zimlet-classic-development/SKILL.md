---
name: Zimlet Classic Development
description: This skill should be used when the user asks about "classic zimlet", "zimlet XML", "zimlet handler", "zimlet panels", "zimlet dialogs", "zimlet context menu", "zimlet keyboard shortcut", "com_zimbra zimlet", or mentions developing zimlets for Zimbra Classic Web Client. Covers XML-based zimlet development.
version: 1.0.0
---

# Zimlet Classic Development

Guide for developing zimlets for the Zimbra Classic Web Client using XML and JavaScript.

## Zimlet Architecture

Classic zimlets are XML-defined extensions with JavaScript handlers:

```
com_mycompany_myzimlet/
├── com_mycompany_myzimlet.xml    # Zimlet definition
├── com_mycompany_myzimlet.js     # JavaScript handler
├── com_mycompany_myzimlet.css    # Styles (optional)
└── img/                          # Images (optional)
    └── icon.png
```

### Naming Convention

- Package name: `com_<company>_<zimletname>` (lowercase, underscores)
- All files must match package name
- Example: `com_acme_tickettracker`

## Zimlet XML Definition

### Basic Structure

```xml
<zimlet name="com_mycompany_myzimlet" version="1.0"
        description="My Zimlet Description"
        xmlns="urn:zimbraZimlet">

    <!-- Panel item in side panel -->
    <zimletPanelItem label="My Zimlet" icon="zimletIcon">
        <toolTipText>Click to open My Zimlet</toolTipText>
    </zimletPanelItem>

    <!-- Include JavaScript handler -->
    <include>com_mycompany_myzimlet.js</include>

    <!-- Include CSS -->
    <includeCSS>com_mycompany_myzimlet.css</includeCSS>

    <!-- User properties (preferences) -->
    <userProperties>
        <property name="mySetting" type="string">default</property>
    </userProperties>

</zimlet>
```

### Content Objects (Regex Matching)

Highlight and add actions to matched text:

```xml
<zimlet>
    <contentObject>
        <!-- Match ticket numbers like TICKET-1234 -->
        <matchOn>
            <regex attrs="ig">TICKET-(\d+)</regex>
        </matchOn>

        <!-- Actions for matched content -->
        <onClick>
            <actionUrl target="_blank" method="GET">
                https://tickets.company.com/view/{$1}
            </actionUrl>
        </onClick>

        <!-- Tooltip preview -->
        <toolTip>
            <contentUrl>
                https://tickets.company.com/api/preview/{$1}
            </contentUrl>
        </toolTip>
    </contentObject>
</zimlet>
```

### Context Menu Integration

```xml
<zimlet>
    <!-- Add menu items to email context menu -->
    <contextMenu>
        <menuItem label="Create Ticket" id="CREATE_TICKET" icon="ticketIcon"/>
        <menuItem label="Search Related" id="SEARCH_RELATED"/>
    </contextMenu>
</zimlet>
```

## JavaScript Handler

### Basic Handler Structure

```javascript
/**
 * Zimlet handler class
 */
function com_mycompany_myzimlet_HandlerObject() {
}

// Extend base zimlet class
com_mycompany_myzimlet_HandlerObject.prototype = new ZmZimletBase();
com_mycompany_myzimlet_HandlerObject.prototype.constructor =
    com_mycompany_myzimlet_HandlerObject;

/**
 * Called when zimlet is initialized
 */
com_mycompany_myzimlet_HandlerObject.prototype.init = function() {
    // Load user properties
    this._mySetting = this.getUserProperty("mySetting") || "default";

    // Register listeners
    this._registerListeners();
};

/**
 * Called when panel item is single-clicked
 */
com_mycompany_myzimlet_HandlerObject.prototype.singleClicked = function() {
    this._showDialog();
};

/**
 * Called when panel item is double-clicked
 */
com_mycompany_myzimlet_HandlerObject.prototype.doubleClicked = function() {
    this._openSettings();
};
```

### Dialogs

```javascript
/**
 * Show a custom dialog
 */
com_mycompany_myzimlet_HandlerObject.prototype._showDialog = function() {
    if (this._dialog) {
        this._dialog.popup();
        return;
    }

    var view = new DwtComposite(this.getShell());
    view.setSize("400", "300");
    view.getHtmlElement().innerHTML = this._createDialogContent();

    this._dialog = new ZmDialog({
        title: "My Zimlet",
        view: view,
        parent: this.getShell(),
        standardButtons: [DwtDialog.OK_BUTTON, DwtDialog.CANCEL_BUTTON],
        disposeOnPopDown: false
    });

    this._dialog.setButtonListener(DwtDialog.OK_BUTTON,
        new AjxListener(this, this._onOkClick));

    this._dialog.popup();
};

com_mycompany_myzimlet_HandlerObject.prototype._createDialogContent = function() {
    return '<div class="myzimlet-container">' +
           '<label>Enter value:</label>' +
           '<input type="text" id="myzimlet-input" />' +
           '</div>';
};

com_mycompany_myzimlet_HandlerObject.prototype._onOkClick = function() {
    var input = document.getElementById("myzimlet-input");
    var value = input ? input.value : "";

    // Process value...

    this._dialog.popdown();
};
```

### Context Menu Handling

```javascript
/**
 * Called when context menu item is selected
 */
com_mycompany_myzimlet_HandlerObject.prototype.menuItemSelected =
function(itemId, item, ev) {
    switch(itemId) {
        case "CREATE_TICKET":
            this._createTicket(item);
            break;
        case "SEARCH_RELATED":
            this._searchRelated(item);
            break;
    }
};

com_mycompany_myzimlet_HandlerObject.prototype._createTicket = function(item) {
    // Get email details
    var msg = item;
    var subject = msg.subject;
    var from = msg.getAddress(AjxEmailAddress.FROM).toString();

    // Open ticket creation URL
    var url = "https://tickets.company.com/create?" +
              "subject=" + encodeURIComponent(subject) +
              "&from=" + encodeURIComponent(from);

    window.open(url, "_blank");
};
```

### Making SOAP Requests

```javascript
/**
 * Make SOAP request to Zimbra
 */
com_mycompany_myzimlet_HandlerObject.prototype._makeRequest = function() {
    var soapDoc = AjxSoapDoc.create("GetInfoRequest", "urn:zimbraAccount");

    var callback = new AjxCallback(this, this._handleResponse);
    var errorCallback = new AjxCallback(this, this._handleError);

    appCtxt.getAppController().sendRequest({
        soapDoc: soapDoc,
        asyncMode: true,
        callback: callback,
        errorCallback: errorCallback
    });
};

com_mycompany_myzimlet_HandlerObject.prototype._handleResponse = function(result) {
    var response = result.getResponse();
    console.log("Response:", response);
};

com_mycompany_myzimlet_HandlerObject.prototype._handleError = function(error) {
    this.displayErrorMessage("Request failed: " + error.msg);
};
```

### User Preferences

```javascript
/**
 * Save user preference
 */
com_mycompany_myzimlet_HandlerObject.prototype._saveSetting = function(value) {
    this.setUserProperty("mySetting", value, true); // true = save to server
};

/**
 * Load user preference
 */
com_mycompany_myzimlet_HandlerObject.prototype._loadSetting = function() {
    return this.getUserProperty("mySetting") || "default";
};
```

## Slots and Injection Points

Classic zimlets can inject into specific UI areas:

### Tab Integration

```xml
<zimlet>
    <!-- Add as application tab -->
    <zimletPanelItem label="My App" icon="myIcon">
        <toolTipText>My Application</toolTipText>
    </zimletPanelItem>
</zimlet>
```

```javascript
// Create tab application
com_mycompany_myzimlet_HandlerObject.prototype._createApp = function() {
    var app = this.createApp("My App", "myIcon", "My Application");
    return app;
};
```

### Toolbar Buttons

```javascript
// Add toolbar button
com_mycompany_myzimlet_HandlerObject.prototype._addToolbarButton = function() {
    var toolbar = appCtxt.getCurrentView().getToolbar();

    var button = new ZmToolBarButton({
        parent: toolbar,
        text: "My Action",
        tooltip: "Perform my action"
    });

    button.addSelectionListener(new AjxListener(this, this._onToolbarClick));
};
```

## Deployment

### Package as ZIP

```bash
cd com_mycompany_myzimlet/
zip -r ../com_mycompany_myzimlet.zip *
```

### Deploy via zmzimletctl

```bash
# Deploy zimlet
zmzimletctl deploy com_mycompany_myzimlet.zip

# Enable for COS
zmzimletctl enable com_mycompany_myzimlet

# List installed zimlets
zmzimletctl listZimlets

# Undeploy
zmzimletctl undeploy com_mycompany_myzimlet
```

## DWT Widget Library (Discrete Widget Toolkit)

Classic zimlets use Zimbra's proprietary DWT library for UI components. Understanding DWT is essential for building Classic zimlets.

### Key Widget Classes

| Widget | Purpose | Usage |
|--------|---------|-------|
| `DwtControl` | Base class | Everything extends this |
| `DwtButton` | Clickable button | `new DwtButton({parent: shell})` |
| `DwtToolBarButton` | Toolbar button | `new DwtToolBarButton({parent: toolbar})` |
| `DwtListView` | List display | For displaying items in a list |
| `DwtMenu` | Dropdown menu | For context menus |
| `DwtDialog` | Modal dialog | `new ZmDialog({...})` |
| `DwtComposite` | Container | Group child widgets |
| `ZmToast` | Notifications | Popup messages |

### Creating a Button

```javascript
// Create a button in the toolbar
com_mycompany_myzimlet_HandlerObject.prototype.initializeToolbar =
function(app, toolbar, controller, viewId) {
    // Check we're in the Mail view
    if (viewId.indexOf("ZM_MAIL") >= 0) {
        // Create the button
        var button = new DwtToolBarButton({parent: toolbar});
        button.setText("My Action");
        button.setImage("MyIcon");

        // Attach click listener (note: must bind 'this' with AjxListener)
        button.addSelectionListener(
            new AjxListener(this, this._handleButtonClick)
        );
    }
};

com_mycompany_myzimlet_HandlerObject.prototype._handleButtonClick = function(ev) {
    // Use Zimbra's status message instead of console.log
    appCtxt.setStatusMsg("Button clicked!", ZmStatusView.LEVEL_INFO);
};
```

### Namespace Safety

**Important:** Classic UI uses global CSS. Always prefix your CSS classes:

```css
/* WRONG - can break Zimbra layout */
.container { padding: 10px; }

/* CORRECT - namespaced */
.Com_MyCompany_MyZimlet_container { padding: 10px; }
```

```javascript
// WRONG - global variable pollution
var myVar = "value";

// CORRECT - use prototype
Com_MyCompany_MyZimlet.prototype.myVar = "value";
```

## Debugging

### URL Parameters for Debug Mode

```
https://mail.domain.com/?dev=1          # Developer mode (unminified)
https://mail.domain.com/?debug=1        # SOAP debug window
https://mail.domain.com/?mode=mjsf      # Individual JS files for breakpoints
```

### Browser Console

```javascript
// Option 1: Standard console
console.log("[MyZimlet] Initializing...");

// Option 2: Zimbra Status Message (visible in UI - recommended)
var appCtxt = this.getContext();
appCtxt.setStatusMsg("MyZimlet initialized!", ZmStatusView.LEVEL_INFO);

// Option 3: AjxDebug (appears in debug window with ?debug=1)
AjxDebug.println("[MyZimlet] User property: " + this.getUserProperty("mySetting"));
```

## Additional Resources

### Reference Files

- **`references/zimlet-xml-elements.md`** - Complete XML element reference
- **`references/dwt-widgets.md`** - DWT widget documentation

### Example Files

- **`examples/basic-zimlet/`** - Minimal zimlet template
- **`examples/content-object-zimlet/`** - Regex matching example
- **`examples/dialog-zimlet/`** - Custom dialog example
