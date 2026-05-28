# Re-render Optimization

Patterns to prevent unnecessary component re-renders.

## Table of Contents

1. [React.memo](#reactmemo)
2. [useMemo and useCallback](#usememo-and-usecallback)
3. [State Management Patterns](#state-management-patterns)
4. [Effect Dependencies](#effect-dependencies)

---

## React.memo

Wrap components that receive stable props but have expensive renders.

### Basic Usage

```javascript
const ExpensiveList = React.memo( ( { items, onSelect } ) => {
  return (
    <ul>
      { items.map( ( item ) => (
        <li key={ item.id } onClick={ () => onSelect( item.id ) }>
          { item.name }
        </li>
      ) ) }
    </ul>
  );
} );
```

### Custom Comparison

Use when default shallow comparison isn't sufficient:

```javascript
const DataGrid = React.memo(
  ( { data, columns, onSort } ) => {
    // Expensive render
    return <Grid data={ data } columns={ columns } onSort={ onSort } />;
  },
  ( prevProps, nextProps ) => {
    // Return true to skip re-render
    return (
      prevProps.data.length === nextProps.data.length &&
      prevProps.columns === nextProps.columns &&
      prevProps.data.every( ( item, i ) => item.id === nextProps.data[ i ]?.id )
    );
  }
);
```

### When NOT to Use memo

- Simple components with cheap renders
- Components that always receive new props
- Components with children that change frequently

---

## useMemo and useCallback

### useMemo for Expensive Computations

```javascript
const Component = ( { items, filter } ) => {
  // Memoize expensive filtering/sorting
  const filteredItems = useMemo( () => {
    return items
      .filter( ( item ) => item.type === filter )
      .sort( ( a, b ) => a.name.localeCompare( b.name ) );
  }, [ items, filter ] );

  return <List items={ filteredItems } />;
};
```

### useMemo for Stable Object References

```javascript
const Component = ( { userId } ) => {
  // Stable reference for child components
  const queryOptions = useMemo( () => ( {
    userId,
    includeArchived: false,
    limit: 50,
  } ), [ userId ] );

  return <DataFetcher options={ queryOptions } />;
};
```

### useCallback for Event Handlers

```javascript
const Component = ( { onSave } ) => {
  const [ value, setValue ] = useState( '' );

  // Stable callback reference
  const handleSubmit = useCallback( () => {
    onSave( value );
  }, [ onSave, value ] );

  // Stable setter for child - no deps needed
  const handleChange = useCallback( ( e ) => {
    setValue( e.target.value );
  }, [] );

  return (
    <form onSubmit={ handleSubmit }>
      <Input onChange={ handleChange } />
      <MemoizedButton onClick={ handleSubmit } />
    </form>
  );
};
```

---

## State Management Patterns

### Functional setState

Avoid stale closure issues and enable batching:

```javascript
// Bad - may use stale state
const increment = () => {
  setCount( count + 1 );
  setCount( count + 1 ); // Both use same stale count
};

// Good - functional update
const increment = () => {
  setCount( ( prev ) => prev + 1 );
  setCount( ( prev ) => prev + 1 ); // Correctly increments twice
};
```

### Lazy State Initialization

For expensive initial values:

```javascript
// Bad - runs every render
const [ state, setState ] = useState( expensiveComputation( props ) );

// Good - runs only on mount
const [ state, setState ] = useState( () => expensiveComputation( props ) );

// Good - with complex initial state
const [ form, setForm ] = useState( () => ( {
  values: parseInitialValues( props.data ),
  errors: {},
  touched: {},
} ) );
```

### Derived State

Don't store computed values in state:

```javascript
// Bad - redundant state
const [ items, setItems ] = useState( [] );
const [ filteredItems, setFilteredItems ] = useState( [] );

useEffect( () => {
  setFilteredItems( items.filter( ( i ) => i.active ) );
}, [ items ] );

// Good - derive during render
const [ items, setItems ] = useState( [] );
const filteredItems = useMemo(
  () => items.filter( ( i ) => i.active ),
  [ items ]
);
```

### Use Transitions for Non-Urgent Updates

```javascript
import { useTransition } from 'react';

const SearchComponent = () => {
  const [ query, setQuery ] = useState( '' );
  const [ results, setResults ] = useState( [] );
  const [ isPending, startTransition ] = useTransition();

  const handleSearch = ( value ) => {
    // Urgent: update input immediately
    setQuery( value );

    // Non-urgent: can be interrupted
    startTransition( () => {
      setResults( filterLargeDataset( value ) );
    } );
  };

  return (
    <>
      <Input value={ query } onChange={ ( e ) => handleSearch( e.target.value ) } />
      { isPending ? <Spinner /> : <Results items={ results } /> }
    </>
  );
};
```

---

## Effect Dependencies

### Narrow Dependencies to Primitives

```javascript
// Bad - object reference changes every render
useEffect( () => {
  fetchData( options );
}, [ options ] ); // options = { id, type } - new object each render

// Good - use primitive values
useEffect( () => {
  fetchData( { id: options.id, type: options.type } );
}, [ options.id, options.type ] );
```

### Extract Callback-Only Values

Don't subscribe to state only used in callbacks:

```javascript
// Bad - re-runs effect when count changes
const [ count, setCount ] = useState( 0 );

useEffect( () => {
  const handler = () => console.log( count );
  window.addEventListener( 'click', handler );
  return () => window.removeEventListener( 'click', handler );
}, [ count ] ); // Unnecessary re-subscription

// Good - use ref for callback-only values
const countRef = useRef( count );
countRef.current = count;

useEffect( () => {
  const handler = () => console.log( countRef.current );
  window.addEventListener( 'click', handler );
  return () => window.removeEventListener( 'click', handler );
}, [] ); // Stable subscription
```

### useLatest Pattern

Create stable callbacks that always access current values:

```javascript
const useLatest = ( value ) => {
  const ref = useRef( value );
  ref.current = value;
  return ref;
};

const Component = ( { onComplete, data } ) => {
  const latestData = useLatest( data );

  useEffect( () => {
    const timer = setTimeout( () => {
      onComplete( latestData.current ); // Always current
    }, 1000 );
    return () => clearTimeout( timer );
  }, [ onComplete ] ); // No need for data dependency
};
```
