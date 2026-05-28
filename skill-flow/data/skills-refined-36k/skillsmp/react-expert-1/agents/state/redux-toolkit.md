---
name: redux-toolkit
description: Redux Toolkit for complex state management
workflows:
  - id: redux-setup
    template: wf-creation
    phase: Production
    name: Setup Redux Toolkit
    duration: 1-2 jours
---

# Redux Toolkit - State Management Avancé

## Rôle

Implémentation de Redux Toolkit (RTK) pour la gestion d'état complexe dans les applications React.

## Tu NE fais PAS

- ❌ Gérer le server state (préférer RTK Query ou React Query) → `../data/`
- ❌ Implémenter l'UI des composants → `../components/`
- ❌ Implémenter le backend → `backend-developer`
- ❌ Définir la stratégie de tests → `testing-process`

## Installation

```bash
npm install @reduxjs/toolkit react-redux
```

## Configuration du Store

### Store de base

```tsx
// store/store.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';
import userReducer from './userSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer,
  },
});

// Types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Provider

```tsx
// main.tsx
import { Provider } from 'react-redux';
import { store } from './store/store';

function App() {
  return (
    <Provider store={store}>
      <MainApp />
    </Provider>
  );
}
```

### Hooks typés

```tsx
// store/hooks.ts
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from './store';

export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
```

## createSlice

### Slice simple

```tsx
// store/counterSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
  step: number;
}

const initialState: CounterState = {
  value: 0,
  step: 1,
};

const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += state.step; // Immer permet la mutation
    },
    decrement: (state) => {
      state.value -= state.step;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
    setStep: (state, action: PayloadAction<number>) => {
      state.step = action.payload;
    },
    reset: () => initialState,
  },
});

export const { increment, decrement, incrementByAmount, setStep, reset } =
  counterSlice.actions;

export default counterSlice.reducer;
```

### Usage

```tsx
import { useAppDispatch, useAppSelector } from './store/hooks';
import { increment, decrement, setStep } from './store/counterSlice';

function Counter() {
  const { value, step } = useAppSelector((state) => state.counter);
  const dispatch = useAppDispatch();

  return (
    <div>
      <p>Count: {value}</p>
      <button onClick={() => dispatch(increment())}>+{step}</button>
      <button onClick={() => dispatch(decrement())}>-{step}</button>
      <input
        type="number"
        value={step}
        onChange={(e) => dispatch(setStep(Number(e.target.value)))}
      />
    </div>
  );
}
```

## createAsyncThunk

### Action asynchrone

```tsx
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

// Thunk
export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) {
        throw new Error('User not found');
      }
      return (await response.json()) as User;
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Unknown error'
      );
    }
  }
);

export const updateUser = createAsyncThunk(
  'user/updateUser',
  async (data: Partial<User> & { id: string }, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${data.id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      });
      return (await response.json()) as User;
    } catch (error) {
      return rejectWithValue('Failed to update user');
    }
  }
);

const initialState: UserState = {
  user: null,
  isLoading: false,
  error: null,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    logout: () => initialState,
  },
  extraReducers: (builder) => {
    builder
      // fetchUser
      .addCase(fetchUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // updateUser
      .addCase(updateUser.fulfilled, (state, action) => {
        state.user = action.payload;
      });
  },
});

export const { clearError, logout } = userSlice.actions;
export default userSlice.reducer;
```

### Usage du thunk

```tsx
function UserProfile({ userId }: { userId: string }) {
  const dispatch = useAppDispatch();
  const { user, isLoading, error } = useAppSelector((state) => state.user);

  useEffect(() => {
    dispatch(fetchUser(userId));
  }, [dispatch, userId]);

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error} />;
  if (!user) return null;

  return <Profile user={user} />;
}
```

## Sélecteurs avec createSelector

```tsx
import { createSelector } from '@reduxjs/toolkit';
import type { RootState } from './store';

// Sélecteurs de base
const selectTodos = (state: RootState) => state.todos.items;
const selectFilter = (state: RootState) => state.todos.filter;

// Sélecteur mémoïsé
export const selectFilteredTodos = createSelector(
  [selectTodos, selectFilter],
  (todos, filter) => {
    switch (filter) {
      case 'completed':
        return todos.filter((t) => t.completed);
      case 'active':
        return todos.filter((t) => !t.completed);
      default:
        return todos;
    }
  }
);

// Sélecteur paramétré
export const selectTodoById = createSelector(
  [selectTodos, (_state: RootState, id: string) => id],
  (todos, id) => todos.find((t) => t.id === id)
);

// Usage
function TodoList() {
  const filteredTodos = useAppSelector(selectFilteredTodos);
  // ...
}

function TodoItem({ id }: { id: string }) {
  const todo = useAppSelector((state) => selectTodoById(state, id));
  // ...
}
```

## RTK Query

### Configuration

```tsx
// store/api.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

interface User {
  id: string;
  name: string;
  email: string;
}

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['User', 'Post'],
  endpoints: (builder) => ({
    // Query (GET)
    getUsers: builder.query<User[], void>({
      query: () => '/users',
      providesTags: ['User'],
    }),

    getUserById: builder.query<User, string>({
      query: (id) => `/users/${id}`,
      providesTags: (_result, _error, id) => [{ type: 'User', id }],
    }),

    // Mutation (POST, PUT, DELETE)
    createUser: builder.mutation<User, Omit<User, 'id'>>({
      query: (body) => ({
        url: '/users',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['User'],
    }),

    updateUser: builder.mutation<User, Partial<User> & { id: string }>({
      query: ({ id, ...body }) => ({
        url: `/users/${id}`,
        method: 'PATCH',
        body,
      }),
      invalidatesTags: (_result, _error, { id }) => [{ type: 'User', id }],
    }),

    deleteUser: builder.mutation<void, string>({
      query: (id) => ({
        url: `/users/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['User'],
    }),
  }),
});

export const {
  useGetUsersQuery,
  useGetUserByIdQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
} = api;
```

### Intégration au store

```tsx
// store/store.ts
import { configureStore } from '@reduxjs/toolkit';
import { api } from './api';

export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});
```

### Usage RTK Query

```tsx
function UserList() {
  const { data: users, isLoading, error, refetch } = useGetUsersQuery();
  const [createUser, { isLoading: isCreating }] = useCreateUserMutation();

  const handleCreate = async () => {
    try {
      await createUser({ name: 'John', email: 'john@example.com' }).unwrap();
    } catch (error) {
      console.error('Failed to create user:', error);
    }
  };

  if (isLoading) return <Spinner />;
  if (error) return <Error onRetry={refetch} />;

  return (
    <div>
      <button onClick={handleCreate} disabled={isCreating}>
        Add User
      </button>
      <ul>
        {users?.map((user) => (
          <UserItem key={user.id} user={user} />
        ))}
      </ul>
    </div>
  );
}
```

## Middleware Personnalisé

```tsx
import { Middleware } from '@reduxjs/toolkit';

const loggerMiddleware: Middleware = (store) => (next) => (action) => {
  console.log('Dispatching:', action.type);
  const result = next(action);
  console.log('Next state:', store.getState());
  return result;
};

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(loggerMiddleware),
});
```

## Bonnes Pratiques

1. **Hooks typés** - Toujours utiliser useAppDispatch/useAppSelector
2. **Slices par feature** - Un fichier par domaine
3. **createSelector** - Pour les calculs dérivés coûteux
4. **RTK Query** - Préférer pour le data fetching
5. **Immer** - Mutations directes dans les reducers

## Quand utiliser Redux ?

- Applications complexes avec beaucoup d'état partagé
- Équipes larges (patterns prévisibles)
- Besoin de debugging avancé (DevTools)
- Historique d'actions, time-travel

## Voir aussi

- `zustand.md` - Alternative plus légère
- `context.md` - Pour état simple
- `../data/react-query.md` - Alternative à RTK Query

## Livrables

| Livrable | Description |
|----------|-------------|
| Store configuration | configureStore avec reducers et middleware |
| Slices | createSlice avec reducers et types TypeScript |
| Sélecteurs | createSelector pour données dérivées mémoïsées |
