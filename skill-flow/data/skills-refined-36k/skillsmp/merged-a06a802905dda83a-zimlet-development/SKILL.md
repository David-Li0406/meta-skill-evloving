---
name: zimlet-development
description: Use this skill when developing zimlets for Zimbra, whether for the Modern Web Client using Preact and GraphQL or for the Classic Web Client using XML and JavaScript.
---

# Zimlet Development

Guide for developing zimlets for Zimbra, covering both Modern Web Client (using Preact and GraphQL) and Classic Web Client (using XML and JavaScript).

## Architecture Overview

### Modern Zimlets

Modern zimlets are Preact-based web components structured as follows:

```
my-zimlet/
├── package.json
├── zimlet.json           # Zimlet manifest (v2 schema)
├── src/
│   ├── index.js          # Entry point
│   ├── components/       # Preact components
│   └── graphql/          # GraphQL queries
├── public/
│   └── icon.png
└── dist/                 # Built zimlet
```

### Classic Zimlets

Classic zimlets are XML-defined extensions with JavaScript handlers:

```
com_mycompany_myzimlet/
├── com_mycompany_myzimlet.xml    # Zimlet definition
├── com_mycompany_myzimlet.js     # JavaScript handler
├── com_mycompany_myzimlet.css    # Styles (optional)
└── img/                          # Images (optional)
    └── icon.png
```

## Key Technologies

- **Preact** - Lightweight framework for building UI components.
- **GraphQL** - For data fetching in Modern Zimlets.
- **XML** - For defining Classic Zimlet structure and behavior.
- **JavaScript** - For implementing logic in both types of zimlets.

## Project Setup

### Modern Zimlet Setup with zimlet-cli

```bash
# Install CLI
npm install -g @zimbra/zimlet-cli

# Create new zimlet
zimlet create my-zimlet
cd my-zimlet

# Development server
zimlet watch

# Build for production
zimlet build

# Package for deployment
zimlet package
```

### Classic Zimlet Structure

#### Zimlet XML Definition

```xml
<zimlet name="com_mycompany_myzimlet" version="1.0"
        description="My Zimlet Description"
        xmlns="urn:zimbraZimlet">
    <zimletPanelItem label="My Zimlet" icon="zimletIcon"/>
    <include>com_mycompany_myzimlet.js</include>
    <includeCSS>com_mycompany_myzimlet.css</includeCSS>
</zimlet>
```

## Development Patterns

### Modern Zimlet Entry Point

```javascript
import { createElement } from 'preact';
import { MenuItem } from '@zimbra-client/components';

export default function Zimlet(context) {
    const { plugins } = context;
    const exports = {};

    exports.menu = {
        handler: function MenuHandler(menu, context) {
            return [
                <MenuItem
                    icon="fa fa-star"
                    onClick={() => context.openSidebar('my-zimlet-panel')}
                >
                    My Zimlet
                </MenuItem>
            ];
        }
    };

    plugins.register('my-zimlet', exports);
}
```

### Classic Zimlet JavaScript Handler

```javascript
function com_mycompany_myzimlet_HandlerObject() {
}

com_mycompany_myzimlet_HandlerObject.prototype = new ZmZimletBase();

com_mycompany_myzimlet_HandlerObject.prototype.init = function() {
    this._registerListeners();
};

com_mycompany_myzimlet_HandlerObject.prototype.singleClicked = function() {
    this._showDialog();
};
```

## Context and APIs

### Accessing Context in Modern Zimlets

```javascript
export default function Zimlet(context) {
    const { account } = context;
    console.log('User:', account.name);
}
```

### Accessing Context in Classic Zimlets

```javascript
com_mycompany_myzimlet_HandlerObject.prototype.init = function() {
    this._mySetting = this.getUserProperty("mySetting") || "default";
};
```

## Deployment

### Modern Zimlet Deployment

```bash
# Production build
zimlet build

# Create deployment package
zimlet package
```

### Classic Zimlet Deployment

```bash
# Deploy zimlet
zmzimletctl deploy com_mycompany_myzimlet.zip

# Enable for COS
zmzimletctl enable com_mycompany_myzimlet
```

## Additional Resources

### Reference Files

- **`references/slot-api.md`** - Slot documentation for Modern Zimlets.
- **`references/zimlet-xml-elements.md`** - XML element reference for Classic Zimlets.
- **`references/dwt-widgets.md`** - DWT widget documentation for Classic Zimlets.

### Example Files

- **`examples/modern-menu-zimlet/`** - Menu integration example for Modern Zimlets.
- **`examples/basic-zimlet/`** - Minimal zimlet template for Classic Zimlets.

### Online Resources

- [Zimbra Zimlet Guide](https://github.com/Zimbra/zm-zimlet-guide)
- [Zimbra Wiki - ModernUI Zimlets](https://wiki.zimbra.com/wiki/ModernUI-Zimlets)
- [Preact Documentation](https://preactjs.com/guide/v10/getting-started)