# State Management - Sharp Edges

## Context Render Cascade

### **Id**
context-render-cascade
### **Summary**
Using React Context for frequently-changing state causes full tree re-renders
### **Severity**
critical
### **Situation**
  You use React Context to share state (theme, user, cart) across your app.
  State updates frequently. The entire component tree re-renders on every change.
  
### **Why**
  React Context has no built-in selector mechanism. When context value changes,
  EVERY component that uses useContext re-renders, even if they only need
  a small part of the value.
  
  This is invisible until your app gets slow. By then, you have Context
  scattered everywhere and migration is painful.
  
### **Solution**
  1. Split contexts by update frequency:
     // Separate rarely-changing from frequently-changing
     <AuthContext.Provider value={user}>      // Rarely changes
     <ThemeContext.Provider value={theme}>    // Rarely changes
     <CartContext.Provider value={cart}>      // Changes often - PROBLEM
  
  2. Use a proper state library for frequent updates:
     // Zustand - components only re-render when their slice changes
     const useCart = create((set) => ({
       items: [],
       addItem: (item) => set(s => ({ items: [...s.items, item] }))
     }));
  
     // Component subscribes to specific state
     const itemCount = useCart(state => state.items.length);
  
  3. If stuck with Context, use memo aggressively:
     const CartTotal = memo(function CartTotal() {
       const { total } = useContext(CartContext);
       return <span>{total}</span>;
     });
  
### **Symptoms**
  - App feels sluggish
  - React DevTools shows many re-renders
  - Typing in inputs feels laggy
  - Performance degrades as app grows
### **Detection Pattern**
useContext.*useState|createContext.*value=\\{\\{

## Stale Closure In Actions

### **Id**
stale-closure-in-actions
### **Summary**
Action callbacks capture stale state due to JavaScript closures
### **Severity**
critical
### **Situation**
  You create an action or callback that references state. The callback
  is memoized or stored. When called later, it uses old state values.
  
### **Why**
  JavaScript closures capture values at creation time. If you create a
  callback that reads state, it captures the state value from that moment.
  Later calls use the stale captured value, not current state.
  
  This is especially common with:
  - useCallback with missing dependencies
  - Event listeners added once
  - setTimeout/setInterval callbacks
  - Subscription handlers
  
### **Solution**
  1. Use functional updates:
     // Bad: Captures current count
     const increment = useCallback(() => {
       setCount(count + 1);  // count is stale!
     }, []);  // Missing dependency
  
     // Good: Functional update always has fresh state
     const increment = useCallback(() => {
       setCount(prev => prev + 1);
     }, []);
  
  2. Use refs for latest value:
     const countRef = useRef(count);
     countRef.current = count;  // Always fresh
  
     const logCount = useCallback(() => {
       console.log(countRef.current);  // Always current
     }, []);
  
  3. Zustand's get() always returns fresh state:
     const useStore = create((set, get) => ({
       count: 0,
       logCount: () => {
         console.log(get().count);  // Always fresh
       }
     }));
  
### **Symptoms**
  - Actions use old values
  - It works after I click twice
  - Race conditions in async code
  - Inconsistent state after rapid updates
### **Detection Pattern**
useCallback\\([^)]+state\\.|setTimeout.*state\\.

## Mutating Redux State

### **Id**
mutating-redux-state
### **Summary**
Accidentally mutating Redux state instead of returning new objects
### **Severity**
critical
### **Situation**
  In a Redux reducer, you modify state directly instead of returning
  a new object. Redux doesn't detect the change, UI doesn't update.
  
### **Why**
  Redux uses reference equality to detect changes. If you mutate the
  existing object, the reference stays the same. Redux thinks nothing
  changed. The UI shows stale data.
  
  This is a silent failure - no errors, just wrong behavior.
  
### **Solution**
  1. Use Redux Toolkit (uses Immer internally):
     // RTK reducers can "mutate" - Immer handles it
     const todoSlice = createSlice({
       name: 'todos',
       initialState: [],
       reducers: {
         addTodo: (state, action) => {
           state.push(action.payload);  // Safe with Immer!
         }
       }
     });
  
  2. Classic Redux - always spread:
     // Must return new references at every level
     case 'UPDATE_USER':
       return {
         ...state,
         user: {
           ...state.user,
           name: action.payload.name
         }
       };
  
  3. Use Immer explicitly:
     import produce from 'immer';
  
     case 'UPDATE_USER':
       return produce(state, draft => {
         draft.user.name = action.payload.name;
       });
  
  4. Enable strict mode to catch mutations:
     const store = configureStore({
       reducer: rootReducer,
       middleware: (getDefault) => getDefault({
         immutableCheck: true,
         serializableCheck: true,
       })
     });
  
### **Symptoms**
  - UI doesn't update after dispatch
  - It works after I dispatch twice
  - Redux DevTools shows action but state unchanged
  - Time-travel debugging breaks
### **Detection Pattern**
state\\.\\w+\\s*=|state\\.push|state\\.splice

## Selector Creates New Reference

### **Id**
selector-creates-new-reference
### **Summary**
Selector returns new object/array reference on every call
### **Severity**
high
### **Situation**
  Your selector filters or maps data, returning a new array each time.
  Every component using the selector re-renders on any state change.
  
### **Why**
  Selectors should be stable - return same reference if inputs haven't
  changed. If selector creates new array/object, reference changes even
  when data is same. This defeats memoization.
  
  Common culprits:
  - filter(): Always returns new array
  - map(): Always returns new array
  - Object spread: Always returns new object
  - Array slice: Always returns new array
  
### **Solution**
  1. Use createSelector for memoization:
     import { createSelector } from '@reduxjs/toolkit';
  
     // Bad: New array every time
     const selectActiveUsers = (state) =>
       state.users.filter(u => u.active);
  
     // Good: Memoized, same reference if users unchanged
     const selectActiveUsers = createSelector(
       [state => state.users],
       (users) => users.filter(u => u.active)
     );
  
  2. Zustand - use shallow equality:
     import { useShallow } from 'zustand/react/shallow';
  
     // Re-renders only if actual values change
     const { name, email } = useStore(
       useShallow(state => ({
         name: state.user.name,
         email: state.user.email
       }))
     );
  
  3. Use useMemo for inline transformations:
     const activeUsers = useMemo(
       () => users.filter(u => u.active),
       [users]
     );
  
### **Symptoms**
  - Components re-render when unrelated state changes
  - React DevTools shows unnecessary renders
  - Performance degrades with more state
### **Detection Pattern**
useSelector\\([^)]*filter|useSelector\\([^)]*map

## Async State Race Condition

### **Id**
async-state-race-condition
### **Summary**
Async operations complete out of order, showing stale data
### **Severity**
high
### **Situation**
  User types in search box. Each keystroke triggers API call. Responses
  come back out of order. UI shows results from earlier query.
  
### **Why**
  Network requests don't complete in order sent. If user types "abc":
  - Request for "a" → slow response
  - Request for "ab" → fast response (shows first)
  - Request for "abc" → medium response
  - Request for "a" completes last → overwrites "abc" results!
  
  The UI now shows results for "a" even though user searched "abc".
  
### **Solution**
  1. Cancel previous requests:
     const controllerRef = useRef<AbortController>();
  
     const search = async (query) => {
       // Cancel previous request
       controllerRef.current?.abort();
       controllerRef.current = new AbortController();
  
       try {
         const results = await api.search(query, {
           signal: controllerRef.current.signal
         });
         setResults(results);
       } catch (e) {
         if (e.name !== 'AbortError') throw e;
       }
     };
  
  2. Track request ID and ignore stale responses:
     const requestIdRef = useRef(0);
  
     const search = async (query) => {
       const requestId = ++requestIdRef.current;
  
       const results = await api.search(query);
  
       // Only update if this is still the latest request
       if (requestId === requestIdRef.current) {
         setResults(results);
       }
     };
  
  3. Use React Query (handles this automatically):
     const { data } = useQuery(['search', query], () =>
       api.search(query)
     );
  
### **Symptoms**
  - Wrong data shows briefly then corrects
  - Search shows results for previous query
  - Rapid actions cause flickering
  - Sometimes the data is wrong
### **Detection Pattern**
await.*set.*State|async.*dispatch

## Zustand Subscribe Memory Leak

### **Id**
zustand-subscribe-memory-leak
### **Summary**
Zustand subscriptions not cleaned up cause memory leaks
### **Severity**
high
### **Situation**
  You subscribe to Zustand store changes manually with subscribe().
  Component unmounts without unsubscribing. Memory leaks and stale
  callbacks fire.
  
### **Why**
  Manual subscriptions persist until explicitly unsubscribed. If component
  unmounts without cleanup, the subscription keeps running, holding
  references to unmounted component state.
  
### **Solution**
  Always return cleanup function:
  
  useEffect(() => {
    // subscribe() returns unsubscribe function
    const unsubscribe = useStore.subscribe(
      (state) => state.user,
      (user) => {
        console.log('User changed:', user);
      }
    );
  
    // Cleanup on unmount
    return unsubscribe;
  }, []);
  
  // Or use the hook form which handles cleanup:
  const user = useStore((state) => state.user);
  
### **Symptoms**
  - Memory usage grows over time
  - Console warnings about state updates on unmounted component
  - Callbacks fire for destroyed components
  - App slows down after navigation
### **Detection Pattern**
subscribe\\([^)]+\\)(?!.*return)

## Redux Action Type Collision

### **Id**
redux-action-type-collision
### **Summary**
Different reducers respond to same action type unexpectedly
### **Severity**
high
### **Situation**
  You dispatch an action. Multiple reducers handle it because they share
  the same action type string. State changes in unexpected places.
  
### **Why**
  Redux broadcasts actions to ALL reducers. If two reducers listen for
  'RESET' or 'UPDATE', both will run. This causes subtle bugs where
  unrelated state changes.
  
### **Solution**
  1. Use Redux Toolkit (namespaced by default):
     // Actions are automatically namespaced
     const userSlice = createSlice({
       name: 'user',
       reducers: {
         reset: (state) => initialState,
         // Actual type: 'user/reset'
       }
     });
  
  2. Prefix action types manually:
     // Bad
     const RESET = 'RESET';
  
     // Good
     const RESET_USER = 'user/RESET';
     const RESET_CART = 'cart/RESET';
  
  3. Avoid generic action names:
     // Bad: Too generic
     'SET_DATA', 'UPDATE', 'CLEAR'
  
     // Good: Specific
     'users/setList', 'cart/updateItem', 'filters/clear'
  
### **Symptoms**
  - Multiple state slices change from one dispatch
  - Why did this state change?
  - Action appears in wrong reducer's case
### **Detection Pattern**
case ['"]\w+['"]:|type:\s*['"]\w+['"]

## Storing Non Serializable State

### **Id**
storing-non-serializable-state
### **Summary**
Storing functions, class instances, or Dates in Redux store
### **Severity**
medium
### **Situation**
  You store Date objects, class instances, functions, or Maps/Sets
  in your Redux store. Serialization breaks, time-travel doesn't work.
  
### **Why**
  Redux stores should be serializable (JSON-compatible). Non-serializable
  values break:
  - Redux DevTools (can't inspect/export state)
  - Time-travel debugging
  - State persistence (localStorage)
  - State hydration (SSR)
  
  Redux Toolkit warns about this by default.
  
### **Solution**
  1. Convert to serializable formats:
     // Bad
     { createdAt: new Date() }
  
     // Good
     { createdAt: new Date().toISOString() }
     // or
     { createdAt: Date.now() }
  
  2. Store IDs, not instances:
     // Bad
     { selectedUser: userInstance }
  
     // Good
     { selectedUserId: userId }
     // Derive instance via selector
  
  3. Keep functions outside store:
     // Functions go in action creators or middleware, not state
  
  4. Disable check only if you understand the consequences:
     const store = configureStore({
       reducer: rootReducer,
       middleware: (getDefault) => getDefault({
         serializableCheck: false  // Last resort!
       })
     });
  
### **Symptoms**
  - Redux DevTools shows "[object Object]"
  - Serializable check warnings
  - localStorage persistence fails
  - State hydration errors
### **Detection Pattern**
new Date\\(\\)|new Map\\(|new Set\\(

## Prop Drilling State Down

### **Id**
prop-drilling-state-down
### **Summary**
Passing state through many component layers instead of using store
### **Severity**
medium
### **Situation**
  You pass state as props through 5+ levels of components. Middle
  components don't use the prop, just pass it down.
  
### **Why**
  Prop drilling creates:
  - Tight coupling between distant components
  - Maintenance burden when props change
  - Unnecessary re-renders of middle components
  - Verbose component signatures
  
  However, don't over-correct - not everything needs global state.
  
### **Solution**
  Identify if the state is truly global:
  
  1. Used by distant components? → Global store
     const user = useStore(state => state.user);
  
  2. Used by nearby components? → Lift to common parent
     // Parent holds state, passes to direct children
  
  3. Stable dependency (theme, i18n)? → Context is fine
     const theme = useContext(ThemeContext);
  
  4. Component composition can help:
     // Instead of drilling props through Header
     function Page({ user }) {
       return <Header userMenu={<UserMenu user={user} />} />;
     }
  
     // Header doesn't need to know about user
     function Header({ userMenu }) {
       return <nav>{userMenu}</nav>;
     }
  
### **Symptoms**
  - Props passed through 5+ levels
  - Middle components have props they don't use
  - Adding new prop requires editing many files
### **Detection Pattern**
props\\.\\w+.*props\\.\\w+.*props\\.\\w+

## Missing Loading Error States

### **Id**
missing-loading-error-states
### **Summary**
Async state without loading or error handling
### **Severity**
medium
### **Situation**
  You fetch data and store it. There's no loading indicator while
  fetching, no error handling if it fails. User sees blank or stale data.
  
### **Why**
  Async operations have three states: loading, success, error. If you
  only model success, users get confused when things take time or fail.
  
### **Solution**
  Model all async states:
  
  // Full async state shape
  interface AsyncState<T> {
    data: T | null;
    loading: boolean;
    error: Error | null;
  }
  
  // Redux Toolkit pattern
  const fetchUsers = createAsyncThunk('users/fetch', async () => {
    return await api.getUsers();
  });
  
  const usersSlice = createSlice({
    name: 'users',
    initialState: { data: [], loading: false, error: null },
    extraReducers: (builder) => {
      builder
        .addCase(fetchUsers.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(fetchUsers.fulfilled, (state, action) => {
          state.data = action.payload;
          state.loading = false;
        })
        .addCase(fetchUsers.rejected, (state, action) => {
          state.error = action.error;
          state.loading = false;
        });
    }
  });
  
  // Zustand pattern
  const useUsersStore = create((set) => ({
    users: [],
    loading: false,
    error: null,
    fetchUsers: async () => {
      set({ loading: true, error: null });
      try {
        const users = await api.getUsers();
        set({ users, loading: false });
      } catch (error) {
        set({ error, loading: false });
      }
    }
  }));
  
### **Symptoms**
  - Blank screen while loading
  - Silent failures
  - User doesn't know something's wrong
  - Stale data shown as current
### **Detection Pattern**
await.*set\\(\\{\\s*\\w+:|fetch.*then.*set