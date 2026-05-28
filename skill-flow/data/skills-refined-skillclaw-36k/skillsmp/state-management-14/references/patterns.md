# State Management

## Patterns


---
  #### **Name**
Server State vs Client State Separation
  #### **Description**
    Distinguish between server state (cached API data) and client state
    (UI state, user preferences). Use different tools for each.
    
  #### **Example**
    // Server state - use React Query or SWR
    const { data: users } = useQuery(['users'], fetchUsers);
    
    // Client state - use Zustand or Redux
    const theme = useStore(state => state.theme);
    const toggleTheme = useStore(state => state.toggleTheme);
    
    // DON'T mix them in the same store
    // Bad: Redux store with API cache AND UI state
    
  #### **When**
Starting any new project with both API calls and UI state

---
  #### **Name**
Atomic State (Jotai/Recoil Pattern)
  #### **Description**
    Define state as independent atoms that can be composed. Each atom is
    its own subscription, preventing unnecessary re-renders.
    
  #### **Example**
    // Jotai atoms
    const userAtom = atom<User | null>(null);
    const themeAtom = atom<'light' | 'dark'>('light');
    
    // Derived atom - computed from other atoms
    const userDisplayNameAtom = atom(
      (get) => get(userAtom)?.displayName ?? 'Guest'
    );
    
    // Component only subscribes to what it needs
    function UserBadge() {
      const displayName = useAtomValue(userDisplayNameAtom);
      return <span>{displayName}</span>;
    }
    
  #### **When**
Need fine-grained reactivity, many independent pieces of state

---
  #### **Name**
Single Store with Slices (Redux/Zustand)
  #### **Description**
    Organize state into domain slices within a single store. Each slice
    manages its own actions and reducers.
    
  #### **Example**
    // Zustand with slices
    interface AppState {
      user: UserSlice;
      cart: CartSlice;
      ui: UISlice;
    }
    
    const useStore = create<AppState>()((...a) => ({
      user: createUserSlice(...a),
      cart: createCartSlice(...a),
      ui: createUISlice(...a),
    }));
    
    // userSlice.ts
    export const createUserSlice = (set, get) => ({
      user: null,
      login: async (credentials) => {
        const user = await authApi.login(credentials);
        set({ user });
      },
      logout: () => set({ user: null }),
    });
    
  #### **When**
Medium to large apps with clear domain boundaries

---
  #### **Name**
Selector Memoization
  #### **Description**
    Create memoized selectors to derive data from state without
    recalculating on every render.
    
  #### **Example**
    // Redux with Reselect
    import { createSelector } from '@reduxjs/toolkit';
    
    const selectCartItems = (state) => state.cart.items;
    const selectTaxRate = (state) => state.settings.taxRate;
    
    // Memoized - only recalculates when inputs change
    const selectCartTotal = createSelector(
      [selectCartItems, selectTaxRate],
      (items, taxRate) => {
        const subtotal = items.reduce((sum, item) =>
          sum + item.price * item.quantity, 0
        );
        return subtotal * (1 + taxRate);
      }
    );
    
    // Zustand equivalent
    const useCartTotal = () => useStore(
      useShallow(state => {
        const subtotal = state.cart.items.reduce(...);
        return subtotal * (1 + state.settings.taxRate);
      })
    );
    
  #### **When**
Expensive computations derived from state

---
  #### **Name**
Immer for Immutable Updates
  #### **Description**
    Use Immer to write mutable-looking code that produces immutable updates.
    Built into Redux Toolkit, available as middleware for Zustand.
    
  #### **Example**
    // Without Immer - verbose and error-prone
    const updateUser = (state, action) => ({
      ...state,
      user: {
        ...state.user,
        profile: {
          ...state.user.profile,
          address: {
            ...state.user.profile.address,
            city: action.payload.city
          }
        }
      }
    });
    
    // With Immer - write like mutations
    const updateUser = (state, action) => {
      state.user.profile.address.city = action.payload.city;
    };
    
    // Zustand with Immer middleware
    import { immer } from 'zustand/middleware/immer';
    
    const useStore = create(
      immer((set) => ({
        users: [],
        addUser: (user) => set((state) => {
          state.users.push(user);
        }),
      }))
    );
    
  #### **When**
Deeply nested state updates

---
  #### **Name**
Persistence Middleware
  #### **Description**
    Persist state to localStorage/sessionStorage with automatic
    rehydration on app load.
    
  #### **Example**
    // Zustand with persist
    import { persist } from 'zustand/middleware';
    
    const useStore = create(
      persist(
        (set) => ({
          theme: 'light',
          setTheme: (theme) => set({ theme }),
        }),
        {
          name: 'app-settings',
          partialize: (state) => ({ theme: state.theme }),
          // Only persist theme, not other state
        }
      )
    );
    
    // Redux with redux-persist
    import { persistStore, persistReducer } from 'redux-persist';
    import storage from 'redux-persist/lib/storage';
    
    const persistConfig = {
      key: 'root',
      storage,
      whitelist: ['settings', 'auth'],
    };
    
    const persistedReducer = persistReducer(persistConfig, rootReducer);
    
  #### **When**
User preferences, auth tokens, draft content

---
  #### **Name**
Optimistic Updates
  #### **Description**
    Update UI immediately before server confirms, then reconcile.
    Provides snappy UX while maintaining data integrity.
    
  #### **Example**
    // Zustand optimistic update
    const useStore = create((set, get) => ({
      todos: [],
    
      addTodo: async (text) => {
        const optimisticTodo = {
          id: crypto.randomUUID(),
          text,
          completed: false,
          _optimistic: true,
        };
    
        // Update immediately
        set((state) => ({
          todos: [...state.todos, optimisticTodo]
        }));
    
        try {
          // Sync with server
          const realTodo = await api.createTodo(text);
          set((state) => ({
            todos: state.todos.map(t =>
              t.id === optimisticTodo.id ? realTodo : t
            )
          }));
        } catch (error) {
          // Rollback on failure
          set((state) => ({
            todos: state.todos.filter(t => t.id !== optimisticTodo.id)
          }));
          throw error;
        }
      },
    }));
    
  #### **When**
User actions that should feel instant

---
  #### **Name**
Action Creators with Thunks
  #### **Description**
    Encapsulate async logic in action creators/thunks rather than
    components. Keeps components focused on UI.
    
  #### **Example**
    // Redux Toolkit async thunk
    export const fetchUser = createAsyncThunk(
      'user/fetch',
      async (userId: string, { rejectWithValue }) => {
        try {
          const response = await api.getUser(userId);
          return response.data;
        } catch (error) {
          return rejectWithValue(error.response.data);
        }
      }
    );
    
    // Handles pending, fulfilled, rejected automatically
    const userSlice = createSlice({
      name: 'user',
      initialState: { user: null, loading: false, error: null },
      reducers: {},
      extraReducers: (builder) => {
        builder
          .addCase(fetchUser.pending, (state) => {
            state.loading = true;
          })
          .addCase(fetchUser.fulfilled, (state, action) => {
            state.user = action.payload;
            state.loading = false;
          })
          .addCase(fetchUser.rejected, (state, action) => {
            state.error = action.payload;
            state.loading = false;
          });
      },
    });
    
  #### **When**
Complex async operations with loading/error states

---
  #### **Name**
Context for Dependency Injection
  #### **Description**
    Use React Context for dependency injection (services, config) rather
    than frequently-changing state. Context is for stable values.
    
  #### **Example**
    // Good: Stable dependencies via Context
    const ApiContext = createContext<ApiClient | null>(null);
    
    function ApiProvider({ children }) {
      const client = useMemo(() => new ApiClient(), []);
      return (
        <ApiContext.Provider value={client}>
          {children}
        </ApiContext.Provider>
      );
    }
    
    // Bad: Frequently changing state via Context
    // This causes ALL consumers to re-render on every change
    const ThemeContext = createContext({ theme: 'light' });
    
    // Better: Use Zustand/Jotai for frequently changing state
    const useTheme = create((set) => ({
      theme: 'light',
      toggle: () => set(s => ({
        theme: s.theme === 'light' ? 'dark' : 'light'
      }))
    }));
    
  #### **When**
Providing services/config that rarely change

## Anti-Patterns


---
  #### **Name**
Storing Derived State
  #### **Description**
Storing computed values that can be derived from other state
  #### **Why**
    Creates synchronization problems. If source state changes and derived
    state isn't updated, you have inconsistent state.
    
  #### **Instead**
    Use selectors or computed values:
    
    // Bad: Stored derived state
    const store = {
      items: [],
      itemCount: 0,  // Derived from items.length
      totalPrice: 0, // Derived from items
    };
    
    // Good: Compute on read
    const selectItemCount = (state) => state.items.length;
    const selectTotalPrice = createSelector(
      [selectItems],
      (items) => items.reduce((sum, i) => sum + i.price, 0)
    );
    

---
  #### **Name**
Putting Everything in Global State
  #### **Description**
Moving all state to global store, including local UI state
  #### **Why**
    Makes components less reusable, harder to test, and creates unnecessary
    coupling. Not all state needs to be global.
    
  #### **Instead**
    Use the right level of state:
    - Component state: useState for UI like open/closed, hover
    - Lifted state: Parent component for sibling communication
    - Context: Scoped global for feature areas
    - Global store: Truly app-wide state (auth, theme, cart)
    
    # Decision tree
    Is it used by multiple distant components? → Global store
    Is it used by nearby components? → Lift to common parent
    Is it only used here? → Local useState
    

---
  #### **Name**
Mutating State Directly
  #### **Description**
Modifying state objects without creating new references
  #### **Why**
    React and state libraries rely on reference equality to detect changes.
    Mutations are invisible, causing stale UI and bugs.
    
  #### **Instead**
    Always create new references:
    
    // Bad
    state.user.name = 'New Name';
    setState(state);
    
    // Good
    setState({
      ...state,
      user: { ...state.user, name: 'New Name' }
    });
    
    // Better: Use Immer
    setState(produce(state, draft => {
      draft.user.name = 'New Name';
    }));
    

---
  #### **Name**
Selector in Render
  #### **Description**
Creating selector functions inside render
  #### **Why**
    Creates new function reference every render, breaking memoization
    and causing unnecessary re-renders.
    
  #### **Instead**
    // Bad: New selector every render
    function UserList() {
      const users = useSelector(state =>
        state.users.filter(u => u.active)
      );
    }
    
    // Good: Stable selector reference
    const selectActiveUsers = createSelector(
      [state => state.users],
      (users) => users.filter(u => u.active)
    );
    
    function UserList() {
      const users = useSelector(selectActiveUsers);
    }
    

---
  #### **Name**
Over-normalizing State
  #### **Description**
Normalizing all data into ID-lookup tables prematurely
  #### **Why**
    Normalization adds complexity. Only normalize when you have actual
    problems with data duplication or update consistency.
    
  #### **Instead**
    Start simple, normalize when needed:
    
    // Start here
    { users: [{ id: 1, name: 'Alice' }] }
    
    // Normalize if:
    // - Same entity appears in multiple places
    // - Updates need to reflect everywhere
    // - You have relational data (users + posts + comments)
    
    // Normalized structure
    {
      users: { byId: { 1: {...} }, allIds: [1] },
      posts: { byId: { ... }, allIds: [...] }
    }
    

---
  #### **Name**
Redux for Simple Apps
  #### **Description**
Using Redux for small apps with minimal state
  #### **Why**
    Redux has boilerplate overhead. For simple apps, the ceremony of
    actions, reducers, and types isn't worth it.
    
  #### **Instead**
    Match tool to complexity:
    
    - 1-5 pieces of global state → Zustand or Jotai
    - Medium app with clear slices → Redux Toolkit or Zustand
    - Large team, complex flows → Redux Toolkit with strict patterns
    - Server state heavy → React Query + minimal client state
    