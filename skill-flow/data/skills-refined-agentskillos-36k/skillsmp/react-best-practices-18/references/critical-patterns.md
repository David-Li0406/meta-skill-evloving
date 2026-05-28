# Critical Performance Patterns

High-impact optimizations for waterfall elimination and bundle size.

## Table of Contents

1. [Waterfall Elimination](#waterfall-elimination)
2. [Bundle Size Optimization](#bundle-size-optimization)

---

## Waterfall Elimination

Sequential async operations are the #1 cause of slow page loads.

### Parallel API Calls

```javascript
// Bad - sequential (waterfall)
const handleSubmit = async () => {
  const user = await fetchUser( userId );
  const settings = await fetchSettings( userId );
  const notifications = await fetchNotifications( userId );
  // Total time: sum of all requests
};

// Good - parallel
const handleSubmit = async () => {
  const [ user, settings, notifications ] = await Promise.all( [
    fetchUser( userId ),
    fetchSettings( userId ),
    fetchNotifications( userId ),
  ] );
  // Total time: longest single request
};
```

### Defer Await to Branch

Only await when the value is actually needed:

```javascript
// Bad - blocks unnecessarily
const processData = async ( shouldSave ) => {
  const data = await fetchData();
  if ( shouldSave ) {
    await saveData( data );
  }
  return data;
};

// Good - defer await
const processData = async ( shouldSave ) => {
  const dataPromise = fetchData();
  if ( shouldSave ) {
    const data = await dataPromise;
    await saveData( data );
    return data;
  }
  return dataPromise;
};
```

### React Query Parallel Queries

```javascript
// Bad - sequential queries
const Component = ( { userId } ) => {
  const { data: user } = useUser( userId );
  const { data: posts } = usePosts( userId ); // Waits for user

  // ...
};

// Good - parallel queries (both start immediately)
const Component = ( { userId } ) => {
  const userQuery = useUser( userId );
  const postsQuery = usePosts( userId );

  if ( userQuery.isLoading || postsQuery.isLoading ) {
    return <Loading />;
  }

  // ...
};
```

### Dependent Queries (When Needed)

Use `enabled` for genuinely dependent data:

```javascript
const Component = ( { userId } ) => {
  const { data: user } = useUser( userId );

  // Only fetch org after user loads (needs user.orgId)
  const { data: org } = useOrganization( user?.orgId, {
    enabled: Boolean( user?.orgId ),
  } );

  // ...
};
```

---

## Bundle Size Optimization

### Direct Imports Over Barrel Files

Barrel files (`index.js` re-exports) can import thousands of unused modules.

```javascript
// Bad - barrel import loads entire module tree
import { Button, Modal } from '@/components';
import { formatDate, parseDate } from '@/utils';

// Good - direct imports
import { Button } from '@/components/Button/Button';
import { Modal } from '@/components/Modal/Modal';
import { formatDate } from '@/utils/dates/formatDate';
```

### Dynamic Imports with React.lazy

Split large components that aren't needed immediately:

```javascript
import React, { Suspense, lazy } from 'react';

// Heavy components loaded on demand
const RichTextEditor = lazy( () => import( './RichTextEditor' ) );
const VideoPlayer = lazy( () => import( './VideoPlayer' ) );
const ChartDashboard = lazy( () => import( './ChartDashboard' ) );

const Component = ( { showEditor, showVideo, showCharts } ) => (
  <Suspense fallback={ <Loading /> }>
    { showEditor && <RichTextEditor /> }
    { showVideo && <VideoPlayer /> }
    { showCharts && <ChartDashboard /> }
  </Suspense>
);
```

### Defer Third-Party Libraries

Load non-critical libraries after initial render:

```javascript
// Bad - blocks initial render
import Pusher from 'pusher-js';
import { IntercomProvider } from 'react-use-intercom';

// Good - defer loading
const Component = () => {
  const [ pusher, setPusher ] = useState( null );

  useEffect( () => {
    // Load after mount
    import( 'pusher-js' ).then( ( module ) => {
      setPusher( new module.default( APP_KEY ) );
    } );
  }, [] );

  // ...
};
```

### Conditional Module Loading

Only load modules when features are enabled:

```javascript
const Component = ( { analyticsEnabled, debugEnabled } ) => {
  useEffect( () => {
    if ( analyticsEnabled ) {
      import( './analytics' ).then( ( { init } ) => init() );
    }
  }, [ analyticsEnabled ] );

  useEffect( () => {
    if ( debugEnabled && process.env.NODE_ENV === 'development' ) {
      import( './devTools' ).then( ( { setup } ) => setup() );
    }
  }, [ debugEnabled ] );

  // ...
};
```

### Heavy Dependency Alternatives

Consider lighter alternatives:

| Heavy Library | Lighter Alternative | Savings |
|--------------|---------------------|---------|
| moment.js | date-fns | ~70% smaller |
| lodash (full) | lodash-es (tree-shakeable) | Variable |
| chart.js | lightweight-charts | ~50% smaller |

```javascript
// Bad - imports entire lodash
import _ from 'lodash';
_.debounce( fn, 300 );

// Good - import specific function
import debounce from 'lodash/debounce';
debounce( fn, 300 );
```
