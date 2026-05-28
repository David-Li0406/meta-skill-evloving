# Performance Patterns

Rendering performance and JavaScript micro-optimizations.

## Table of Contents

1. [Rendering Performance](#rendering-performance)
2. [JavaScript Optimizations](#javascript-optimizations)
3. [List Virtualization](#list-virtualization)

---

## Rendering Performance

### Hoist Static JSX

Move static elements outside components:

```javascript
// Bad - recreated every render
const Component = ( { data } ) => {
  const header = (
    <header className="p-4 border-b">
      <h1>Dashboard</h1>
      <p>Welcome to your dashboard</p>
    </header>
  );

  return (
    <div>
      { header }
      <Content data={ data } />
    </div>
  );
};

// Good - static, created once
const Header = (
  <header className="p-4 border-b">
    <h1>Dashboard</h1>
    <p>Welcome to your dashboard</p>
  </header>
);

const Component = ( { data } ) => (
  <div>
    { Header }
    <Content data={ data } />
  </div>
);
```

### Conditional Rendering

Use ternary over `&&` to avoid rendering falsy values:

```javascript
// Bad - renders "0" when count is 0
{ count && <Badge count={ count } /> }

// Bad - renders "false" in some edge cases
{ items.length && <List items={ items } /> }

// Good - explicit boolean check
{ count > 0 && <Badge count={ count } /> }

// Good - ternary for clarity
{ items.length > 0 ? <List items={ items } /> : null }

// Good - Boolean cast
{ Boolean( count ) && <Badge count={ count } /> }
```

### Avoid Inline Function Definitions in JSX

```javascript
// Bad - new function every render
<Button onClick={ () => handleClick( id ) } />

// Good - memoized handler
const handleButtonClick = useCallback( () => {
  handleClick( id );
}, [ id, handleClick ] );

<Button onClick={ handleButtonClick } />

// Good for lists - pass data, handle in parent
const ListItem = ( { item, onSelect } ) => (
  <button onClick={ onSelect } data-id={ item.id }>
    { item.name }
  </button>
);

const List = ( { items, onSelect } ) => {
  const handleClick = useCallback( ( e ) => {
    onSelect( e.target.dataset.id );
  }, [ onSelect ] );

  return items.map( ( item ) => (
    <ListItem key={ item.id } item={ item } onSelect={ handleClick } />
  ) );
};
```

### Content Visibility for Long Lists

Use CSS `content-visibility` for lists not requiring virtualization:

```javascript
const LongList = ( { items } ) => (
  <ul className="divide-y">
    { items.map( ( item ) => (
      <li
        key={ item.id }
        style={ { contentVisibility: 'auto', containIntrinsicSize: '0 50px' } }
        className="p-4"
      >
        <ItemContent item={ item } />
      </li>
    ) ) }
  </ul>
);
```

---

## JavaScript Optimizations

### Use Map/Set for O(1) Lookups

```javascript
// Bad - O(n) lookup in loop
const processItems = ( items, selectedIds ) => {
  return items.filter( ( item ) =>
    selectedIds.includes( item.id ) // O(n) each iteration
  );
};

// Good - O(1) lookup with Set
const processItems = ( items, selectedIds ) => {
  const selectedSet = new Set( selectedIds );
  return items.filter( ( item ) => selectedSet.has( item.id ) );
};
```

### Build Index Maps for Repeated Lookups

```javascript
// Bad - O(n) find in loop
const enrichItems = ( items, users ) => {
  return items.map( ( item ) => ( {
    ...item,
    user: users.find( ( u ) => u.id === item.userId ), // O(n) each
  } ) );
};

// Good - O(1) lookup with Map
const enrichItems = ( items, users ) => {
  const userMap = new Map( users.map( ( u ) => [ u.id, u ] ) );
  return items.map( ( item ) => ( {
    ...item,
    user: userMap.get( item.userId ),
  } ) );
};
```

### Early Returns

Exit functions early when possible:

```javascript
// Bad - deeply nested
const processData = ( data, options ) => {
  if ( data ) {
    if ( options.enabled ) {
      if ( data.items.length > 0 ) {
        // actual logic here
      }
    }
  }
};

// Good - early exits
const processData = ( data, options ) => {
  if ( !data ) return;
  if ( !options.enabled ) return;
  if ( data.items.length === 0 ) return;

  // actual logic here
};
```

### Combine Array Iterations

```javascript
// Bad - multiple iterations
const result = items
  .filter( ( item ) => item.active )
  .map( ( item ) => item.value )
  .reduce( ( sum, val ) => sum + val, 0 );

// Good - single iteration
const result = items.reduce( ( sum, item ) => {
  if ( item.active ) {
    return sum + item.value;
  }
  return sum;
}, 0 );
```

### Cache Property Access in Loops

```javascript
// Bad - repeated property access
for ( let i = 0; i < items.length; i++ ) {
  process( items[ i ], config.options.defaultValue );
}

// Good - cache accessed values
const { defaultValue } = config.options;
const len = items.length;
for ( let i = 0; i < len; i++ ) {
  process( items[ i ], defaultValue );
}
```

### Use toSorted() to Avoid Mutation

```javascript
// Bad - mutates original array
const sortedItems = items.sort( ( a, b ) => a.name.localeCompare( b.name ) );

// Good - returns new array (ES2023)
const sortedItems = items.toSorted( ( a, b ) => a.name.localeCompare( b.name ) );

// Good - spread for older environments
const sortedItems = [ ...items ].sort( ( a, b ) => a.name.localeCompare( b.name ) );
```

### Hoist RegExp Outside Functions

```javascript
// Bad - RegExp compiled every call
const sanitize = ( input ) => {
  return input.replace( /[<>&"']/g, '' );
};

// Good - compile once
const UNSAFE_CHARS = /[<>&"']/g;
const sanitize = ( input ) => {
  return input.replace( UNSAFE_CHARS, '' );
};
```

---

## List Virtualization

For very long lists (100+ items), use virtualization:

```javascript
import { FixedSizeList } from 'react-window';

const VirtualizedList = ( { items } ) => {
  const Row = ( { index, style } ) => (
    <div style={ style } className="p-4 border-b">
      { items[ index ].name }
    </div>
  );

  return (
    <FixedSizeList
      height={ 400 }
      itemCount={ items.length }
      itemSize={ 50 }
      width="100%"
    >
      { Row }
    </FixedSizeList>
  );
};
```

### When to Virtualize

| List Size | Approach |
|-----------|----------|
| < 50 items | Regular rendering |
| 50-100 items | `content-visibility` CSS |
| 100+ items | react-window virtualization |
| 1000+ items with search | Virtualization + debounced filtering |
