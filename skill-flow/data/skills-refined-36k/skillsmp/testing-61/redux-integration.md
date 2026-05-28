---
name: testing-redux
description: Apply Redux/RTK integration testing best practices using a real store, React Testing Library, and MSW. Auto-apply when editing Redux slices, thunks, RTK Query APIs, or React components wired to a store.
triggers:
  - files: ["**/*slice.js", "**/*store.js", "**/*api.js", "**/*.tsx", "**/*.jsx", "**/*.test.js"]
  - keywords: ["redux", "rtk", "createSlice", "configureStore", "Provider", "RTK Query", "createAsyncThunk"]
---

# Redux Integration Testing Skill

## Core Principles

- Behavior-first: assert user-visible outcomes, not internals.
- Real store: use `configureStore` with real reducers and middleware.
- Prefer MSW for network; avoid mocking Redux/RTK internals.
- Verify via UI; assert store directly only when it simplifies the test.

## Standard Setup

- Reusable `renderWithProviders` helper that:
  - Creates a `store` via `configureStore({ reducer, preloadedState, middleware })`.
  - Wraps `ui` with `<Provider store={store}>`.
  - Returns `{ store, ...renderResult }`.
- Add MSW server in test setup:
  - `beforeAll(server.listen)`, `afterEach(server.resetHandlers)`, `afterAll(server.close)`.
  - Prefer explicit handlers per test; fail on unhandled requests in CI.

## Do / Don’t

- Do: dispatch thunks and `unwrap()` when isolating async logic.
- Do: test RTK Query flows via UI with MSW handlers.
- Do: configure middleware (serializable/thunk extra) for tests when needed.
- Don’t: mock `useSelector`/`useDispatch`/RTK internals.
- Don’t: assert action types in component tests; assert UI behavior.
- Don’t: overuse fake timers; prefer natural async with `findBy*`/`waitFor`.

## Patterns

Render with providers:

```js
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import { render } from '@testing-library/react'
import rootReducer from '@/state/rootReducer'

export function setupStore(preloadedState, customize) {
  return configureStore({
    reducer: rootReducer,
    preloadedState,
    middleware: (getDefault) => (customize?.middleware ?? getDefault)({
      serializableCheck: { warnAfter: 64 },
      thunk: { extraArgument: { /* test deps */ } },
    }),
  })
}

export function renderWithProviders(ui, opts = {}) {
  const store = opts.store ?? setupStore(opts.preloadedState, opts)
  const Wrapper = ({ children }) => <Provider store={store}>{children}</Provider>
  return { store, ...render(ui, { wrapper: Wrapper }) }
}
```

Thunk isolation:

```js
const result = await store.dispatch(fetchUser(42)).unwrap()
expect(result.id).toBe(42)
expect(store.getState().user.byId[42]).toBeDefined()
```

RTK Query + MSW:

```js
server.use(rest.get('/api/todos', (_req, res, ctx) => res(ctx.json([{ id: 1, title: 'A' }]))) )
renderWithProviders(<Todos />)
expect(await screen.findByText('A')).toBeInTheDocument()
```

## Tips

- Disable `setupListeners` in tests unless verifying refetch-on-focus/reconnect.
- If serializable warnings arise, ignore specific actions/paths in `serializableCheck`.
- For listener middleware, start/stop listeners in each test and clear afterward.

## References

- React-Redux Testing: https://react-redux.js.org/using-react-redux/testing
- Redux Toolkit Testing: https://redux-toolkit.js.org/usage/writing-tests
- RTK Query Testing: https://redux-toolkit.js.org/rtk-query/usage/testing
- Testing Library Principles: https://testing-library.com/docs/guiding-principles
- MSW Docs: https://mswjs.io/docs
