# jQuery → React Migration Patterns

This module provides detailed conversion patterns from jQuery to React 19.

## Migration Philosophy

### Paradigm Shift

| jQuery (Imperative) | React (Declarative) |
|---------------------|---------------------|
| Direct DOM manipulation | State-driven UI |
| Event listeners attached manually | Event handlers as props |
| Manual DOM updates | Virtual DOM reconciliation |
| Global selectors | Component-scoped refs |
| Plugin-based extensions | Component composition |

### Key Mindset Changes

```markdown
1. DOM as Output: React renders DOM from state, don't manipulate directly
2. State is Truth: UI reflects state, not the other way around
3. Components Over Selectors: Use component hierarchy, not CSS selectors
4. Props Down, Events Up: Parent controls children via props
5. Side Effects in useEffect: Initialization, cleanup, external interactions
```

---

## DOM Selection & Manipulation

### Element Selection

**jQuery**:
```javascript
// Select elements
const $element = $('#myId');
const $elements = $('.myClass');
const $nested = $('#container .item');

// Check existence
if ($('#myId').length > 0) {
  // element exists
}
```

**React**:
```tsx
import { useRef } from 'react';

function Component() {
  const elementRef = useRef<HTMLDivElement>(null);

  // Access DOM node
  const element = elementRef.current;

  return <div ref={elementRef}>Content</div>;
}

// For multiple elements, use array of refs or callback refs
function ListComponent() {
  const itemRefs = useRef<Map<string, HTMLLIElement>>(new Map());

  const setItemRef = (id: string) => (el: HTMLLIElement | null) => {
    if (el) {
      itemRefs.current.set(id, el);
    } else {
      itemRefs.current.delete(id);
    }
  };

  return (
    <ul>
      {items.map(item => (
        <li key={item.id} ref={setItemRef(item.id)}>{item.name}</li>
      ))}
    </ul>
  );
}
```

### DOM Manipulation

**jQuery**:
```javascript
// Modify content
$('#title').text('New Title');
$('#content').html('<p>New content</p>');

// Modify attributes
$('#link').attr('href', 'https://example.com');
$('input').val('new value');

// Modify styles
$('#box').css('background-color', 'red');
$('#box').css({ width: '100px', height: '100px' });

// Add/remove classes
$('#element').addClass('active');
$('#element').removeClass('inactive');
$('#element').toggleClass('visible');
```

**React**:
```tsx
import { useState } from 'react';

function Component() {
  const [title, setTitle] = useState('Initial Title');
  const [content, setContent] = useState('<p>Initial content</p>');
  const [href, setHref] = useState('https://example.com');
  const [inputValue, setInputValue] = useState('');
  const [isActive, setIsActive] = useState(false);
  const [isVisible, setIsVisible] = useState(true);

  return (
    <>
      {/* Text content - just render state */}
      <h1>{title}</h1>

      {/* HTML content - use dangerouslySetInnerHTML (with caution!) */}
      <div dangerouslySetInnerHTML={{ __html: content }} />

      {/* Attributes - use props */}
      <a href={href}>Link</a>
      <input value={inputValue} onChange={e => setInputValue(e.target.value)} />

      {/* Styles - use style prop or CSS classes */}
      <div style={{ backgroundColor: 'red', width: 100, height: 100 }} />

      {/* Classes - use className with conditional logic */}
      <div className={`element ${isActive ? 'active' : ''}`} />
      <div className={isVisible ? 'visible' : 'hidden'} />
    </>
  );
}
```

### Show/Hide Elements

**jQuery**:
```javascript
$('#element').show();
$('#element').hide();
$('#element').toggle();
$('#element').fadeIn();
$('#element').fadeOut();
```

**React**:
```tsx
import { useState } from 'react';

function Component() {
  const [isVisible, setIsVisible] = useState(true);

  return (
    <>
      {/* Conditional rendering */}
      {isVisible && <div>Visible content</div>}

      {/* CSS-based hiding (preserves DOM) */}
      <div style={{ display: isVisible ? 'block' : 'none' }}>
        Content
      </div>

      {/* With CSS transitions */}
      <div
        className={`fade ${isVisible ? 'fade-in' : 'fade-out'}`}
      >
        Animated content
      </div>

      <button onClick={() => setIsVisible(v => !v)}>Toggle</button>
    </>
  );
}
```

---

## Event Handling

### Click Events

**jQuery**:
```javascript
$('#button').click(function() {
  console.log('Clicked!');
});

$('#button').on('click', function(e) {
  e.preventDefault();
  console.log('Clicked with event:', e);
});

// Event delegation
$('#container').on('click', '.item', function() {
  console.log('Item clicked:', $(this).data('id'));
});
```

**React**:
```tsx
function Component() {
  const handleClick = () => {
    console.log('Clicked!');
  };

  const handleClickWithEvent = (e: React.MouseEvent) => {
    e.preventDefault();
    console.log('Clicked with event:', e);
  };

  // Event delegation is usually not needed - attach handlers directly
  const handleItemClick = (id: string) => () => {
    console.log('Item clicked:', id);
  };

  return (
    <>
      <button onClick={handleClick}>Click me</button>
      <a href="#" onClick={handleClickWithEvent}>Link</a>

      {/* Direct handlers instead of delegation */}
      <div id="container">
        {items.map(item => (
          <div
            key={item.id}
            className="item"
            onClick={handleItemClick(item.id)}
          >
            {item.name}
          </div>
        ))}
      </div>
    </>
  );
}
```

### Form Events

**jQuery**:
```javascript
$('#form').submit(function(e) {
  e.preventDefault();
  const formData = $(this).serialize();
  console.log(formData);
});

$('#input').on('input', function() {
  console.log('Value:', $(this).val());
});

$('#input').on('change', function() {
  console.log('Changed to:', $(this).val());
});

$('#input').on('focus blur', function(e) {
  console.log(e.type);
});
```

**React**:
```tsx
import { useState, FormEvent, ChangeEvent, FocusEvent } from 'react';

function Form() {
  const [value, setValue] = useState('');

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    console.log(Object.fromEntries(formData));
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
    console.log('Value:', e.target.value);
  };

  const handleFocus = (e: FocusEvent<HTMLInputElement>) => {
    console.log(e.type); // 'focus' or 'blur'
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={value}
        onChange={handleChange}
        onFocus={handleFocus}
        onBlur={handleFocus}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Keyboard Events

**jQuery**:
```javascript
$(document).on('keydown', function(e) {
  if (e.key === 'Enter') {
    console.log('Enter pressed');
  }
  if (e.key === 'Escape') {
    console.log('Escape pressed');
  }
});

$('#input').on('keyup', function(e) {
  if (e.key === 'Enter') {
    $(this).closest('form').submit();
  }
});
```

**React**:
```tsx
import { useEffect, KeyboardEvent } from 'react';

function Component() {
  // Global keyboard listener
  useEffect(() => {
    const handleKeyDown = (e: globalThis.KeyboardEvent) => {
      if (e.key === 'Enter') console.log('Enter pressed');
      if (e.key === 'Escape') console.log('Escape pressed');
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Element-specific handler
  const handleKeyUp = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      // Submit form or trigger action
    }
  };

  return <input onKeyUp={handleKeyUp} />;
}
```

---

## AJAX & Data Fetching

### GET Request

**jQuery**:
```javascript
$.get('/api/users', function(data) {
  console.log(data);
});

$.ajax({
  url: '/api/users',
  method: 'GET',
  success: function(data) {
    $('#users').html(renderUsers(data));
  },
  error: function(xhr, status, error) {
    console.error('Error:', error);
  }
});

// With loading state
$('#loading').show();
$.get('/api/data')
  .done(function(data) {
    $('#content').html(data);
  })
  .fail(function() {
    $('#error').show();
  })
  .always(function() {
    $('#loading').hide();
  });
```

**React**:
```tsx
import { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
}

function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let ignore = false;

    async function fetchUsers() {
      try {
        const response = await fetch('/api/users');
        if (!response.ok) throw new Error('Failed to fetch');
        const data = await response.json();

        if (!ignore) {
          setUsers(data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err instanceof Error ? err.message : 'Unknown error');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    fetchUsers();

    // Cleanup to prevent race conditions
    return () => {
      ignore = true;
    };
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### POST Request

**jQuery**:
```javascript
$.post('/api/users', { name: 'John', email: 'john@example.com' })
  .done(function(response) {
    console.log('Created:', response);
  });

$.ajax({
  url: '/api/users',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({ name: 'John', email: 'john@example.com' }),
  success: function(response) {
    console.log('Created:', response);
  }
});
```

**React**:
```tsx
import { useState } from 'react';

function CreateUserForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email }),
      });

      if (!response.ok) throw new Error('Failed to create user');

      const data = await response.json();
      console.log('Created:', data);

      // Reset form
      setName('');
      setEmail('');
    } catch (error) {
      console.error(error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit" disabled={submitting}>
        {submitting ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

---

## Document Ready & Lifecycle

### Document Ready

**jQuery**:
```javascript
$(document).ready(function() {
  // Initialize app
  initializePlugins();
  setupEventHandlers();
  loadInitialData();
});

// Shorthand
$(function() {
  console.log('DOM ready');
});
```

**React**:
```tsx
import { useEffect } from 'react';

function App() {
  // Runs after component mounts (similar to document.ready)
  useEffect(() => {
    console.log('Component mounted');

    // Initialize
    initializePlugins();
    loadInitialData();

    // Cleanup on unmount
    return () => {
      console.log('Component will unmount');
      cleanupPlugins();
    };
  }, []); // Empty deps = run once on mount

  return <div>App Content</div>;
}
```

### Window Events

**jQuery**:
```javascript
$(window).on('resize', function() {
  console.log('Window resized:', $(window).width());
});

$(window).on('scroll', function() {
  console.log('Scroll position:', $(window).scrollTop());
});

$(window).on('beforeunload', function() {
  return 'Are you sure you want to leave?';
});
```

**React**:
```tsx
import { useState, useEffect } from 'react';

function useWindowSize() {
  const [size, setSize] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const handleResize = () => {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };

    handleResize(); // Initial size
    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
}

function useScrollPosition() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return scrollY;
}

function useBeforeUnload(message: string, when: boolean) {
  useEffect(() => {
    if (!when) return;

    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = message;
      return message;
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [message, when]);
}
```

---

## Animation

### Basic Animations

**jQuery**:
```javascript
$('#element').fadeIn(400);
$('#element').fadeOut(400);
$('#element').slideDown(400);
$('#element').slideUp(400);
$('#element').animate({ opacity: 0.5, left: '+=50' }, 1000);
```

**React (CSS Transitions)**:
```tsx
import { useState } from 'react';

// CSS
// .fade-enter { opacity: 0; }
// .fade-enter-active { opacity: 1; transition: opacity 400ms; }
// .fade-exit { opacity: 1; }
// .fade-exit-active { opacity: 0; transition: opacity 400ms; }

function AnimatedComponent() {
  const [isVisible, setIsVisible] = useState(true);

  return (
    <>
      <div
        style={{
          opacity: isVisible ? 1 : 0,
          transition: 'opacity 400ms ease-in-out',
        }}
      >
        Fade content
      </div>

      <div
        style={{
          maxHeight: isVisible ? '1000px' : '0',
          overflow: 'hidden',
          transition: 'max-height 400ms ease-in-out',
        }}
      >
        Slide content
      </div>

      <button onClick={() => setIsVisible(v => !v)}>Toggle</button>
    </>
  );
}
```

**React (Framer Motion - Recommended)**:
```tsx
import { motion, AnimatePresence } from 'framer-motion';

function AnimatedList({ items }) {
  return (
    <AnimatePresence>
      {items.map(item => (
        <motion.div
          key={item.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {item.name}
        </motion.div>
      ))}
    </AnimatePresence>
  );
}
```

---

## Plugin Migration Strategy

### jQuery Plugin → React Component

**jQuery Plugin Pattern**:
```javascript
// jQuery plugin
(function($) {
  $.fn.myPlugin = function(options) {
    const settings = $.extend({
      color: 'blue',
      size: 'medium'
    }, options);

    return this.each(function() {
      $(this).css('color', settings.color);
      $(this).addClass(settings.size);
    });
  };
})(jQuery);

// Usage
$('#element').myPlugin({ color: 'red', size: 'large' });
```

**React Component**:
```tsx
interface MyComponentProps {
  color?: string;
  size?: 'small' | 'medium' | 'large';
  children: React.ReactNode;
}

function MyComponent({
  color = 'blue',
  size = 'medium',
  children
}: MyComponentProps) {
  return (
    <div style={{ color }} className={size}>
      {children}
    </div>
  );
}

// Usage
<MyComponent color="red" size="large">
  Content
</MyComponent>
```

### Common jQuery Plugins → React Alternatives

| jQuery Plugin | React Alternative |
|---------------|-------------------|
| jQuery UI Datepicker | react-datepicker, @mui/x-date-pickers |
| jQuery Validation | react-hook-form, formik + yup/zod |
| Select2 | react-select |
| DataTables | TanStack Table (react-table) |
| Slick Carousel | swiper, embla-carousel |
| Lightbox | yet-another-react-lightbox |
| jQuery UI Sortable | @dnd-kit/sortable |
| Tooltipster | @floating-ui/react, @radix-ui/react-tooltip |

---

## Incremental Migration Strategy

### Phase 1: Coexistence Setup

Set up React alongside existing jQuery code:

```html
<!-- index.html -->
<div id="jquery-app">
  <!-- Existing jQuery code -->
</div>

<div id="react-root">
  <!-- New React components -->
</div>

<script src="jquery.min.js"></script>
<script src="legacy-app.js"></script>
<script type="module" src="react-app.js"></script>
```

```tsx
// react-app.tsx
import { createRoot } from 'react-dom/client';
import App from './App';

const container = document.getElementById('react-root');
if (container) {
  const root = createRoot(container);
  root.render(<App />);
}
```

### Phase 2: jQuery-React Bridge

Create wrapper for jQuery plugins in React:

```tsx
import { useRef, useEffect } from 'react';

interface JQueryWrapperProps {
  pluginName: string;
  options?: Record<string, unknown>;
}

function JQueryPluginWrapper({ pluginName, options }: JQueryWrapperProps) {
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const $element = $(elementRef.current);

    // Initialize jQuery plugin
    if ($element[pluginName]) {
      $element[pluginName](options);
    }

    // Cleanup
    return () => {
      if ($element[pluginName] && typeof $element[pluginName]('destroy') === 'function') {
        $element[pluginName]('destroy');
      }
    };
  }, [pluginName, options]);

  return <div ref={elementRef} />;
}
```

### Phase 3: Component-by-Component Migration

1. **Identify Leaf Components**: Start with simple, isolated UI components
2. **Create React Equivalents**: Build React components with same functionality
3. **Replace jQuery Code**: Swap jQuery implementations one at a time
4. **Test Thoroughly**: Verify behavior matches original
5. **Remove jQuery Dependency**: Once all components migrated, remove jQuery

### Migration Checklist

- [ ] Set up React build pipeline (Vite, webpack)
- [ ] Install React and dependencies
- [ ] Create coexistence structure
- [ ] Identify migration order (simple → complex)
- [ ] Migrate static components first
- [ ] Migrate form components with state
- [ ] Migrate AJAX/data fetching components
- [ ] Replace jQuery plugins with React alternatives
- [ ] Remove jQuery dependency
- [ ] Clean up legacy code

---

## Common Pitfalls

### 1. Direct DOM Manipulation

```tsx
// ❌ WRONG: jQuery-style DOM manipulation
function BadComponent() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Don't do this!
    ref.current!.innerHTML = '<p>New content</p>';
    ref.current!.style.color = 'red';
  }, []);

  return <div ref={ref} />;
}

// ✅ CORRECT: State-driven rendering
function GoodComponent() {
  const [content, setContent] = useState('New content');
  const [color, setColor] = useState('red');

  return <div style={{ color }}><p>{content}</p></div>;
}
```

### 2. Missing Cleanup

```tsx
// ❌ WRONG: No cleanup
useEffect(() => {
  window.addEventListener('resize', handleResize);
}, []);

// ✅ CORRECT: With cleanup
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

### 3. Event Handler Performance

```tsx
// ❌ WRONG: New function every render
<button onClick={() => handleClick(id)}>Click</button>

// ✅ CORRECT: Memoized or handler factory
const handleClick = useCallback((id: string) => {
  console.log('Clicked:', id);
}, []);

// Or pass id as data attribute
<button data-id={id} onClick={handleClick}>Click</button>
```

---

Version: 1.0.0
Last Updated: 2026-01-25
Source: Context7 React Documentation + jQuery Migration Best Practices
