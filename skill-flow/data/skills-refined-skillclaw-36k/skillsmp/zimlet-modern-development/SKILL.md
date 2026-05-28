---
name: Zimlet Modern Development
description: This skill should be used when the user asks about "modern zimlet", "Preact zimlet", "React zimlet", "zimlet GraphQL", "zimlet slots", "zimlet CLI", "Zimbra X zimlet", "zm-x-web", "zimlet-cli", or mentions developing zimlets for Zimbra Modern Web Client. Covers component-based zimlet development.
version: 1.0.0
---

# Zimlet Modern Development

Guide for developing zimlets for the Zimbra Modern Web Client using Preact, GraphQL, and the zimlet-cli toolchain.

> **💡 Essential Tip:** Add `?zimletSlots=show` to your Zimbra URL to visualize all available slot locations in the UI!

## Architecture Overview

Modern zimlets are Preact-based web components:

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

### Key Technologies

- **Preact** - React-compatible lightweight framework
- **GraphQL** - Data fetching from Zimbra
- **zimlet-cli** - Build and development tooling
- **Slot system** - UI injection points

## Project Setup

### Using zimlet-cli

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

### zimlet.json Manifest

```json
{
  "name": "my-zimlet",
  "version": "1.0.0",
  "description": "My Modern Zimlet",
  "label": "My Zimlet",
  "icon": "icon.png",
  "host": "https://mail.domain.com",
  "slots": {
    "menu": true,
    "routes": true,
    "compose-attachment-buttons": true
  }
}
```

### package.json

```json
{
  "name": "my-zimlet",
  "version": "1.0.0",
  "main": "src/index.js",
  "scripts": {
    "build": "zimlet build",
    "watch": "zimlet watch",
    "package": "zimlet package"
  },
  "dependencies": {
    "@zimbra-client/components": "^1.0.0",
    "@zimbra-client/graphql": "^1.0.0",
    "preact": "^10.0.0"
  }
}
```

## Entry Point and Slots

### src/index.js

```javascript
import { createElement } from 'preact';
import { useCallback, useState } from 'preact/hooks';
import { MenuItem } from '@zimbra-client/components';

// Register zimlet with all slot handlers
export default function Zimlet(context) {
    const { plugins } = context;
    const exports = {};

    // Menu slot - add item to hamburger menu
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

    // Routes slot - add custom routes
    exports.routes = {
        handler: function RouteHandler() {
            return [
                {
                    path: '/my-zimlet',
                    component: () => import('./components/MainView')
                }
            ];
        }
    };

    // Sidebar slot
    exports.sidebars = {
        handler: function SidebarHandler() {
            return {
                'my-zimlet-panel': () => import('./components/Sidebar')
            };
        }
    };

    // Compose attachment buttons
    exports['compose-attachment-buttons'] = {
        handler: function AttachmentHandler(props) {
            return [
                <button onClick={() => props.onAttach({ type: 'my-service' })}>
                    Attach from My Service
                </button>
            ];
        }
    };

    // Register with plugin system
    plugins.register('my-zimlet', exports);
}
```

## Available Slots

Modern Web Client provides these injection points:

| Slot | Location | Use Case |
|------|----------|----------|
| `menu` | Hamburger menu | Add navigation items |
| `routes` | App routing | Custom views/pages |
| `sidebars` | Side panels | Contextual panels |
| `compose-attachment-buttons` | Compose toolbar | Custom attachments |
| `mail-action-menu` | Email context menu | Message actions |
| `calendar-action-menu` | Calendar context menu | Event actions |
| `contact-action-menu` | Contact context menu | Contact actions |
| `composer-toolbar` | Rich editor toolbar | Formatting tools |
| `search-bar` | Search area | Search enhancements |

### Slot Handler Patterns

```javascript
// Simple handler returning components
exports['slot-name'] = {
    handler: function(props, context) {
        return <Component {...props} />;
    }
};

// Async component loading
exports['slot-name'] = {
    handler: function() {
        return import('./components/MyComponent').then(m => m.default);
    }
};

// Conditional rendering
exports['slot-name'] = {
    handler: function(props, context) {
        if (!context.account.features.includes('myFeature')) {
            return null;
        }
        return <Component />;
    }
};
```

## Preact Components

### Basic Component

```javascript
// src/components/MainView.js
import { createElement } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import { useGraphQL } from '@zimbra-client/graphql';

export default function MainView({ context }) {
    const [data, setData] = useState(null);

    useEffect(() => {
        // Load data on mount
        fetchData();
    }, []);

    return (
        <div class="my-zimlet-main">
            <h1>My Zimlet</h1>
            {data ? (
                <DataList items={data} />
            ) : (
                <Loading />
            )}
        </div>
    );
}
```

### Using Zimbra Components

```javascript
import {
    Button,
    Card,
    Dialog,
    Icon,
    MenuItem,
    Sidebar,
    TextInput
} from '@zimbra-client/components';

function MyDialog({ visible, onClose }) {
    return (
        <Dialog
            visible={visible}
            title="My Dialog"
            onClose={onClose}
            buttons={[
                { label: 'Cancel', onClick: onClose },
                { label: 'Save', primary: true, onClick: handleSave }
            ]}
        >
            <TextInput
                label="Name"
                value={name}
                onChange={e => setName(e.target.value)}
            />
        </Dialog>
    );
}
```

## GraphQL Integration

### Basic Query

```javascript
import { useQuery } from '@zimbra-client/graphql';
import gql from 'graphql-tag';

const GET_FOLDERS = gql`
    query GetFolders {
        getFolder {
            folders {
                id
                name
                unread
                view
            }
        }
    }
`;

function FolderList() {
    const { data, loading, error } = useQuery(GET_FOLDERS);

    if (loading) return <Loading />;
    if (error) return <Error message={error.message} />;

    return (
        <ul>
            {data.getFolder.folders.map(folder => (
                <li key={folder.id}>
                    {folder.name} ({folder.unread})
                </li>
            ))}
        </ul>
    );
}
```

### Search Messages

```javascript
const SEARCH_MESSAGES = gql`
    query SearchMessages($query: String!, $limit: Int) {
        search(query: $query, types: MESSAGE, limit: $limit) {
            messages {
                id
                subject
                date
                from {
                    address
                    name
                }
            }
        }
    }
`;

function MessageSearch({ searchTerm }) {
    const { data } = useQuery(SEARCH_MESSAGES, {
        variables: { query: searchTerm, limit: 50 }
    });

    return (
        <MessageList messages={data?.search?.messages || []} />
    );
}
```

### Mutations

```javascript
const SEND_MESSAGE = gql`
    mutation SendMessage($message: SendMessageInput!) {
        sendMessage(message: $message) {
            id
        }
    }
`;

function ComposeForm() {
    const [sendMessage] = useMutation(SEND_MESSAGE);

    const handleSend = async () => {
        await sendMessage({
            variables: {
                message: {
                    to: [{ address: 'recipient@example.com' }],
                    subject: 'Hello',
                    text: 'Message body'
                }
            }
        });
    };

    return <button onClick={handleSend}>Send</button>;
}
```

## Context and APIs

### Access Context

```javascript
export default function Zimlet(context) {
    const {
        plugins,         // Plugin registration
        account,         // Current user account
        getApolloClient, // GraphQL client
        store,           // Redux store
        config,          // App configuration
        intl             // Internationalization
    } = context;

    // Use account info
    console.log('User:', account.name);
    console.log('Email:', account.email);
}
```

### Make External API Calls

```javascript
async function fetchExternalData(context) {
    // Get auth token for external APIs
    const authToken = context.account.authToken;

    const response = await fetch('https://api.myservice.com/data', {
        headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
        }
    });

    return response.json();
}
```

## Styling

### CSS Modules

```javascript
// src/components/MyComponent.js
import style from './MyComponent.less';

function MyComponent() {
    return (
        <div class={style.container}>
            <h1 class={style.title}>Hello</h1>
        </div>
    );
}
```

```less
// src/components/MyComponent.less
.container {
    padding: 16px;
}

.title {
    color: #333;
    font-size: 24px;
}
```

### Zimbra Theme Variables

```less
@import '~@zimbra-client/styles/variables';

.myButton {
    background-color: @primary-color;
    border-radius: @border-radius;
    padding: @spacing-md;
}
```

## Deployment

### Build and Package

```bash
# Production build
zimlet build

# Create deployment package
zimlet package
# Creates my-zimlet.zip
```

### Deploy to Zimbra

```bash
# Copy to server
scp my-zimlet.zip zimbra@mail.domain.com:/tmp/

# On server (as zimbra user)
zmzimletctl deploy /tmp/my-zimlet.zip

# Enable for all users
zmprov mc default +zimbraZimletAvailableZimlets my-zimlet

# Verify
zmzimletctl listZimlets
```

## Additional Resources

### Reference Files

- **`references/slot-api.md`** - Complete 50+ slot documentation with categories, patterns, and discovery tips
- **`references/code-patterns.md`** - Best practices for project structure, components, stores, and services
- **`references/graphql-schema.md`** - Zimbra GraphQL schema

### Example Files

- **`examples/modern-menu-zimlet/`** - Menu integration example
- **`examples/modern-sidebar-zimlet/`** - Sidebar panel example
- **`examples/modern-graphql-zimlet/`** - GraphQL data fetching

### Online Resources

- [Zimbra Zimlet Guide](https://github.com/Zimbra/zm-zimlet-guide)
- [Zimbra Wiki - ModernUI Zimlets](https://wiki.zimbra.com/wiki/ModernUI-Zimlets)
- [Zimbra Zimlet Gallery](https://gallery.zetalliance.org/extend/category/modern)
- [Preact Documentation](https://preactjs.com/guide/v10/getting-started)
