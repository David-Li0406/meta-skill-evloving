# Modern Zimlet Code Patterns

Best practices and patterns for developing Zimbra Modern UI zimlets.

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | Preact | 10.x |
| Build | Zimlet CLI (Webpack) | 12.8.0+ |
| Editor | TinyMCE | Zimbra bundled |
| Styling | CSS Modules | - |
| State | Preact Hooks / Pub-Sub | - |

## Project Structure

```
my-zimlet/
├── src/
│   ├── index.js                    # Entry point, slot registration
│   │
│   ├── components/
│   │   ├── MainComponent.js        # Primary component
│   │   ├── Panel.js                # Panel/sidebar component
│   │   └── ui/                     # Reusable UI primitives
│   │       ├── Button.js
│   │       └── Panel.js
│   │
│   ├── services/
│   │   ├── index.js                # Module exports
│   │   ├── api.js                  # API calls
│   │   └── errors.js               # Error handling
│   │
│   ├── stores/                     # State management
│   │   ├── index.js                # Module exports
│   │   └── appStore.js             # App state
│   │
│   ├── hooks/                      # Custom Preact hooks
│   │   ├── index.js
│   │   └── useDebounce.js
│   │
│   ├── constants/
│   │   └── endpoints.js            # API endpoints
│   │
│   ├── utils/
│   │   └── helpers.js
│   │
│   └── intl/                       # Translations
│       ├── en_US.js
│       └── fr.js
│
├── package.json
└── zimlet.json
```

## Entry Point Pattern

```javascript
/**
 * Zimlet entry point
 * @param {Object} context - Zimbra context object
 */
export default function Zimlet(context) {
    const { plugins, zimbraOrigin, zimbra } = context;
    const exports = {};

    exports.init = function init() {
        // Register components to slots
        plugins.register('slot::composer', (props) => (
            <MyComponent {...props} context={context} />
        ));

        plugins.register('slot::rightside-zimlet-slot', () => (
            <SidePanel context={context} />
        ));

        plugins.register('slot::action-menu-mail-more', (props) => (
            <ActionMenuItem {...props} context={context} />
        ));
    };

    return exports;
}
```

## Component Patterns

### Class Component

```javascript
import { createElement, Component } from 'preact';
import style from './style.css';

/**
 * Component description
 * @slot slot::composer
 */
export default class MyComponent extends Component {
    constructor(props) {
        super(props);
        this.state = { isOpen: false };
    }

    componentDidMount() {
        // Setup listeners, fetch initial data
    }

    componentWillUnmount() {
        // Cleanup listeners
    }

    handleToggle = () => {
        this.setState({ isOpen: !this.state.isOpen });
    };

    render() {
        const { isOpen } = this.state;
        return (
            <div class={style.container}>
                <button onClick={this.handleToggle}>
                    {isOpen ? 'Close' : 'Open'}
                </button>
            </div>
        );
    }
}
```

### Functional Component with Hooks

```javascript
import { createElement } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import style from './style.css';

export function MyFunctionalComponent({ context }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Component mount logic
        return () => {
            // Cleanup
        };
    }, []);

    const handleAction = async () => {
        setLoading(true);
        try {
            const result = await fetchData();
            setData(result);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div class={style.wrapper}>
            {loading ? <span>Loading...</span> : <DataDisplay data={data} />}
        </div>
    );
}
```

## Store Pattern (Pub/Sub)

```javascript
// stores/appStore.js
function createStore(initialState) {
    let state = initialState;
    const listeners = new Set();

    return {
        getState: () => state,
        setState: (updates) => {
            state = { ...state, ...updates };
            listeners.forEach(listener => listener(state));
        },
        subscribe: (listener) => {
            listeners.add(listener);
            return () => listeners.delete(listener);
        },
    };
}

export const appStore = createStore({
    messages: [],
    isLoading: false,
    settings: {}
});

// Actions
export function addMessage(role, content) {
    const messages = [...appStore.getState().messages, { role, content }];
    appStore.setState({ messages });
}

export function setLoading(isLoading) {
    appStore.setState({ isLoading });
}

// Selectors
export const selectors = {
    getMessages: () => appStore.getState().messages,
    isLoading: () => appStore.getState().isLoading,
};
```

### Using Store in Components

```javascript
import { useState, useEffect } from 'preact/hooks';
import { appStore, selectors } from '../stores';

export function useAppStore() {
    const [state, setState] = useState(appStore.getState());

    useEffect(() => {
        return appStore.subscribe(setState);
    }, []);

    return { ...state, ...selectors };
}
```

## Service Layer Pattern

```javascript
// services/errors.js
export class APIError extends Error {
    constructor(message, status, details) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.details = details;
    }
}

// services/api.js
import { APIError } from './errors';

const BASE_URL = 'https://api.example.com';

export async function fetchData(endpoint, options = {}) {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new APIError(
                'Request failed',
                response.status,
                await response.text()
            );
        }

        return response.json();
    } catch (error) {
        console.error('[API] Error:', error);
        throw error instanceof APIError ? error : new APIError(error.message);
    }
}
```

## Import Order Convention

```javascript
// 1. External libraries
import { createElement, Component } from 'preact';
import { useState, useEffect } from 'preact/hooks';

// 2. Services and utilities
import { fetchData, APIError } from '../services/api';
import { formatDate } from '../utils/helpers';

// 3. Stores and hooks
import { useAppStore } from '../stores';
import { useDebounce } from '../hooks';

// 4. Components
import Panel from './Panel';

// 5. Styles
import style from './style.css';
```

## Module Exports Pattern

```javascript
// components/ui/index.js - Clean re-exports
export { Button } from './Button';
export { Panel } from './Panel';
export { Modal } from './Modal';

// Usage in other files
import { Button, Panel, Modal } from '../components/ui';
```

## Internationalization

```javascript
import { withIntl } from '@zimbra-client/enhancers';

class MyComponent extends Component {
    render() {
        const { intl } = this.props;
        return (
            <div>
                {intl.formatMessage({ id: 'myZimlet.greeting' })}
            </div>
        );
    }
}

export default withIntl()(MyComponent);

// intl/en_US.js
export default {
    'myZimlet.greeting': 'Hello',
    'myZimlet.action': 'Click here'
};
```

## Best Practices

### Always Do

- Use `class` not `className` (Preact convention)
- Clean up event listeners in `componentWillUnmount`
- Use CSS Modules for scoped styling
- Handle errors with custom error classes
- Import from module index files: `from '../stores'` not `from '../stores/appStore'`
- Pass context through to child components when needed

### Avoid

- Direct DOM manipulation (use Preact state)
- Storing API keys in frontend code
- Duplicating Zimbra-provided dependencies (Preact is shimmed)
- Creating `package-lock.json` (use zimlet CLI's bundling)

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Zimlet not loading | Check sideloader URL, verify `npm run watch` running |
| Component not updating | Use proper setState, avoid direct state mutation |
| CORS errors | Configure backend with Zimbra origin |
| Styles not applying | Import CSS modules, use `class` not `className` |
| Context undefined | Pass context from entry point through props |

## Development Commands

```bash
# Start development server with hot reload
npm run watch

# Build for production
npm run build

# Package for Zimbra deployment
npm run package

# Lint code
npm run lint
npm run lint:fix
```

## Testing Checklist

Before deploying:
- [ ] `npm run build` succeeds without errors
- [ ] `npm run lint` passes
- [ ] Test via sideloader in browser
- [ ] Check browser console for errors
- [ ] Verify all slots render correctly
- [ ] Test error handling paths
- [ ] Verify i18n strings display correctly

## References

- [Preact Documentation](https://preactjs.com/guide/v10/getting-started)
- [Preact Hooks](https://preactjs.com/guide/v10/hooks)
- [Zimbra Zimlet CLI](https://github.com/Zimbra/zimlet-cli)
