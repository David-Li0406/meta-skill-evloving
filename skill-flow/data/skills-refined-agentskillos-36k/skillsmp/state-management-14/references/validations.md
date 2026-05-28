# State Management - Validations

## Direct State Mutation

### **Id**
state-direct-mutation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - state\\.\\w+\\s*=
  - state\\.push\\(
  - state\\.splice\\(
  - state\\.pop\\(
  - state\\.shift\\(
  - state\\.unshift\\(
  - state\\[\\w+\\]\\s*=
### **Message**
Direct state mutation detected. This will cause bugs in Redux/React state.
### **Fix Action**
Use immutable update patterns or Immer: set({...state, key: value})
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Object.assign Mutation

### **Id**
state-object-assign-mutation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Object\\.assign\\(state,
### **Message**
Object.assign mutates first argument. Use spread instead.
### **Fix Action**
Replace with: Object.assign({}, state, changes) or {...state, ...changes}
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Inline Selector in Component

### **Id**
state-inline-selector
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useSelector\\(\\s*\\(\\s*state\\s*\\)\\s*=>\\s*state\\.\\w+\\.filter
  - useSelector\\(\\s*\\(\\s*state\\s*\\)\\s*=>\\s*state\\.\\w+\\.map
  - useSelector\\(\\s*\\(\\s*state\\s*\\)\\s*=>\\s*\\{[^}]+filter
### **Message**
Inline selector with filter/map creates new reference every render.
### **Fix Action**
Use createSelector from @reduxjs/toolkit for memoization
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Context with Frequently Changing Value

### **Id**
state-context-frequent-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Provider\\s+value=\\\{\\{[^}]+\\}\\}
  - createContext.*useState
### **Message**
Context value may change frequently, causing cascading re-renders.
### **Fix Action**
Use Zustand/Jotai for frequent updates, or memoize context value
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Object Selection Without Shallow Compare

### **Id**
state-missing-shallow-compare
### **Severity**
info
### **Type**
regex
### **Pattern**
  - useStore\\(\\s*\\(\\s*state\\s*\\)\\s*=>\\s*\\(\\{
  - useStore\\(\\s*state\\s*=>\\s*\\(\\{
### **Message**
Selecting object without shallow compare may cause extra re-renders.
### **Fix Action**
Use useShallow: useStore(useShallow(state => ({...})))
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Business Logic in Component with State

### **Id**
state-business-logic-in-component
### **Severity**
info
### **Type**
regex
### **Pattern**
  - useSelector[\\s\\S]{0,100}if\\s*\\([\\s\\S]{0,50}dispatch
  - useStore[\\s\\S]{0,100}if\\s*\\([\\s\\S]{0,50}\\w+Store
### **Message**
Business logic mixed with state selection in component.
### **Fix Action**
Move complex logic to actions/thunks or custom hooks
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Storing Derived State

### **Id**
state-derived-stored
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\bcount\\b.*length
  - \\btotal\\b.*reduce
  - \\bfiltered\\b.*filter
  - \\bsorted\\b.*sort
### **Message**
Possibly storing derived state. Consider computing from source state.
### **Fix Action**
Use selectors to derive state: const count = items.length
### **Applies To**
  - **/store/**/*.ts
  - **/redux/**/*.ts
  - **/slices/**/*.ts

## Generic Action Type Name

### **Id**
state-generic-action-name
### **Severity**
info
### **Type**
regex
### **Pattern**
  - type:\\s*['\"]SET_DATA['\"]
  - type:\\s*['\"]UPDATE['\"]
  - type:\\s*['\"]RESET['\"]
  - type:\\s*['\"]CLEAR['\"]
  - type:\\s*['\"]LOAD['\"]
### **Message**
Generic action type may conflict with other reducers.
### **Fix Action**
Use namespaced action types: 'users/setData', 'cart/reset'
### **Applies To**
  - **/*.ts
  - **/*.js

## Async Action Without Loading State

### **Id**
state-async-no-loading
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - async.*dispatch\\([^)]+\\)(?![\\s\\S]{0,100}loading)
  - await.*set\\(\\{(?![^}]*loading)
### **Message**
Async operation without loading state handling.
### **Fix Action**
Add loading state: set({ loading: true }) before, false after
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Async State Without Error Handling

### **Id**
state-async-no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - createAsyncThunk(?![\\s\\S]{0,500}rejected)
  - async.*set\\([^)]+\\)(?![\\s\\S]{0,100}catch)
### **Message**
Async operation without error state handling.
### **Fix Action**
Add error handling: catch errors and set error state
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Potential Async Race Condition

### **Id**
state-race-condition-risk
### **Severity**
info
### **Type**
regex
### **Pattern**
  - await.*await.*set
  - setTimeout.*set.*State
  - setInterval.*dispatch
### **Message**
Multiple async operations may cause race conditions.
### **Fix Action**
Use request cancellation or request ID tracking
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Potential Stale Closure

### **Id**
state-stale-closure
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useCallback\\([^)]+\\)\\s*,\\s*\\[\\s*\\]\\)
  - useMemo\\([^)]+state[^)]+\\)\\s*,\\s*\\[\\s*\\]\\)
### **Message**
Empty dependency array with state reference may cause stale closure.
### **Fix Action**
Add state to dependencies or use functional updates
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Store Subscription Without Cleanup

### **Id**
state-subscribe-no-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.subscribe\\([^)]+\\)(?![\\s\\S]{0,50}return)
  - store\\.subscribe(?![\\s\\S]{0,100}unsubscribe)
### **Message**
Store subscription without cleanup may cause memory leaks.
### **Fix Action**
Return unsubscribe function from useEffect cleanup
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Date Object in State

### **Id**
state-non-serializable-date
### **Severity**
info
### **Type**
regex
### **Pattern**
  - :\\s*new Date\\(\\)
  - Date\\.now\\(\\)
### **Message**
Date objects in state may break serialization. Use ISO strings.
### **Fix Action**
Use date.toISOString() or timestamp number instead
### **Applies To**
  - **/store/**/*.ts
  - **/slices/**/*.ts
  - **/redux/**/*.ts

## Function in State

### **Id**
state-non-serializable-function
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - initialState.*=>\\s*\\{
  - state:\\s*\\{[^}]*:\\s*\\([^)]*\\)\\s*=>
### **Message**
Functions in state break Redux serialization and DevTools.
### **Fix Action**
Keep functions in action creators, not in state
### **Applies To**
  - **/store/**/*.ts
  - **/slices/**/*.ts

## Using Deprecated connect() HOC

### **Id**
redux-connect-deprecation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - connect\\(mapStateToProps
  - import.*connect.*from ['\"]react-redux['\"]
### **Message**
connect() is deprecated. Use useSelector and useDispatch hooks.
### **Fix Action**
Replace with: const data = useSelector(selector); const dispatch = useDispatch();
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Using Classic Redux Without Toolkit

### **Id**
redux-no-toolkit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - createStore\\(
  - combineReducers\\(
  - import.*createStore.*from ['\"]redux['\"]
### **Message**
Classic Redux detected. Redux Toolkit is recommended.
### **Fix Action**
Migrate to @reduxjs/toolkit: configureStore, createSlice
### **Applies To**
  - **/*.ts
  - **/*.js

## Complex Nested Updates Without Immer

### **Id**
zustand-missing-immer
### **Severity**
info
### **Type**
regex
### **Pattern**
  - set\\(\\\{\\s*\\.\\.\.state,\\s*\\w+:\\s*\\{\\s*\\.\\.\.state\\.\\w+
### **Message**
Deep nested updates are verbose. Consider Immer middleware.
### **Fix Action**
Add immer middleware: create(immer((set) => ...))
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Selecting Entire Zustand State

### **Id**
zustand-full-state-select
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useStore\\(\\s*\\)(?!\\s*\\.)
  - useStore\\(\\s*state\\s*=>\\s*state\\s*\\)
### **Message**
Selecting entire store causes re-render on any change.
### **Fix Action**
Select specific state: useStore(state => state.user)
### **Applies To**
  - **/*.tsx
  - **/*.jsx