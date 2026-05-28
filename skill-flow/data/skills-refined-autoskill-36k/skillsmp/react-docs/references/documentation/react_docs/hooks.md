# React_Docs - Hooks

**Pages:** 16

---

## Built-in React DOM Hooks

**URL:** https://react.dev/reference/react-dom/hooks

**Contents:**
- Built-in React DOM Hooks
- Form Hooks

The react-dom package contains Hooks that are only supported for web applications (which run in the browser DOM environment). These Hooks are not supported in non-browser environments like iOS, Android, or Windows applications. If you are looking for Hooks that are supported in web browsers and other environments see the React Hooks page. This page lists all the Hooks in the react-dom package.

Forms let you create interactive controls for submitting information. To manage forms in your components, use one of these Hooks:

**Examples:**

Example 1 (jsx):
```jsx
function Form({ action }) {  async function increment(n) {    return n + 1;  }  const [count, incrementFormAction] = useActionState(increment, 0);  return (    <form action={action}>      <button formAction={incrementFormAction}>Count: {count}</button>      <Button />    </form>  );}function Button() {  const { pending } = useFormStatus();  return (    <button disabled={pending} type="submit">      Submit    </button>  );}
```

---

## config

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/config

**Contents:**
- config
- Rule Details
  - Invalid
  - Valid
- Troubleshooting
  - Configuration not working as expected

Validates the compiler configuration options.

React Compiler accepts various configuration options to control its behavior. This rule validates that your configuration uses correct option names and value types, preventing silent failures from typos or incorrect settings.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

Your compiler configuration might have typos or incorrect values:

Check the configuration documentation for valid options:

**Examples:**

Example 1 (css):
```css
// ❌ Unknown option namemodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compileMode: 'all' // Typo: should be compilationMode    }]  ]};// ❌ Invalid option valuemodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'everything' // Invalid: use 'all' or 'infer'    }]  ]};
```

Example 2 (css):
```css
// ✅ Valid compiler configurationmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'infer',      panicThreshold: 'critical_errors'    }]  ]};
```

Example 3 (css):
```css
// ❌ Wrong: Common configuration mistakesmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      // Typo in option name      compilationMod: 'all',      // Wrong value type      panicThreshold: true,      // Unknown option      optimizationLevel: 'max'    }]  ]};
```

Example 4 (css):
```css
// ✅ Better: Valid configurationmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'all', // or 'infer'      panicThreshold: 'none', // or 'critical_errors', 'all_errors'      // Only use documented options    }]  ]};
```

---

## error-boundaries

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/error-boundaries

**Contents:**
- error-boundaries
- Rule Details
  - Invalid
  - Valid
- Troubleshooting
  - Why is the linter telling me not to wrap use in try/catch?

Validates usage of Error Boundaries instead of try/catch for errors in child components.

Try/catch blocks can’t catch errors that happen during React’s rendering process. Errors thrown in rendering methods or hooks bubble up through the component tree. Only Error Boundaries can catch these errors.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

The use hook doesn’t throw errors in the traditional sense, it suspends component execution. When use encounters a pending promise, it suspends the component and lets React show a fallback. Only Suspense and Error Boundaries can handle these cases. The linter warns against try/catch around use to prevent confusion as the catch block would never run.

**Examples:**

Example 1 (jsx):
```jsx
// ❌ Try/catch won't catch render errorsfunction Parent() {  try {    return <ChildComponent />; // If this throws, catch won't help  } catch (error) {    return <div>Error occurred</div>;  }}
```

Example 2 (jsx):
```jsx
// ✅ Using error boundaryfunction Parent() {  return (    <ErrorBoundary>      <ChildComponent />    </ErrorBoundary>  );}
```

Example 3 (jsx):
```jsx
// ❌ Try/catch around `use` hookfunction Component({promise}) {  try {    const data = use(promise); // Won't catch - `use` suspends, not throws    return <div>{data}</div>;  } catch (error) {    return <div>Failed to load</div>; // Unreachable  }}// ✅ Error boundary catches `use` errorsfunction App() {  return (    <ErrorBoundary fallback={<div>Failed to load</div>}>      <Suspense fallback={<div>Loading...</div>}>        <DataComponent promise={fetchData()} />      </Suspense>    </ErrorBoundary>  );}
```

---

## eslint-plugin-react-hooks - This feature is available in the latest RC version

**URL:** https://react.dev/reference/eslint-plugin-react-hooks

**Contents:**
- eslint-plugin-react-hooks - This feature is available in the latest RC version
  - Note
- Recommended Rules

eslint-plugin-react-hooks provides ESLint rules to enforce the Rules of React.

This plugin helps you catch violations of React’s rules at build time, ensuring your components and hooks follow React’s rules for correctness and performance. The lints cover both fundamental React patterns (exhaustive-deps and rules-of-hooks) and issues flagged by React Compiler. React Compiler diagnostics are automatically surfaced by this ESLint plugin, and can be used even if your app hasn’t adopted the compiler yet.

When the compiler reports a diagnostic, it means that the compiler was able to statically detect a pattern that is not supported or breaks the Rules of React. When it detects this, it automatically skips over those components and hooks, while keeping the rest of your app compiled. This ensures optimal coverage of safe optimizations that won’t break your app.

What this means for linting, is that you don’t need to fix all violations immediately. Address them at your own pace to gradually increase the number of optimized components.

These rules are included in the recommended preset in eslint-plugin-react-hooks:

---

## exhaustive-deps

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps

**Contents:**
- exhaustive-deps
- Rule Details
- Common Violations
  - Invalid
  - Valid
- Troubleshooting
  - Adding a function dependency causes infinite loops
  - Running an effect only once
- Options

Validates that dependency arrays for React hooks contain all necessary dependencies.

React hooks like useEffect, useMemo, and useCallback accept dependency arrays. When a value referenced inside these hooks isn’t included in the dependency array, React won’t re-run the effect or recalculate the value when that dependency changes. This causes stale closures where the hook uses outdated values.

This error often happens when you try to “trick” React about dependencies to control when an effect runs. Effects should synchronize your component with external systems. The dependency array tells React which values the effect uses, so React knows when to re-synchronize.

If you find yourself fighting with the linter, you likely need to restructure your code. See Removing Effect Dependencies to learn how.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

You have an effect, but you’re creating a new function on every render:

In most cases, you don’t need the effect. Call the function where the action happens instead:

If you genuinely need the effect (for example, to subscribe to something external), make the dependency stable:

You want to run an effect once on mount, but the linter complains about missing dependencies:

Either include the dependency (recommended) or use a ref if you truly need to run once:

You can configure custom effect hooks using shared ESLint settings (available in eslint-plugin-react-hooks 6.1.1 and later):

For backward compatibility, this rule also accepts a rule-level option:

**Examples:**

Example 1 (javascript):
```javascript
// ❌ Missing dependencyuseEffect(() => {  console.log(count);}, []); // Missing 'count'// ❌ Missing propuseEffect(() => {  fetchUser(userId);}, []); // Missing 'userId'// ❌ Incomplete dependenciesuseMemo(() => {  return items.sort(sortOrder);}, [items]); // Missing 'sortOrder'
```

Example 2 (javascript):
```javascript
// ✅ All dependencies includeduseEffect(() => {  console.log(count);}, [count]);// ✅ All dependencies includeduseEffect(() => {  fetchUser(userId);}, [userId]);
```

Example 3 (jsx):
```jsx
// ❌ Causes infinite loopconst logItems = () => {  console.log(items);};useEffect(() => {  logItems();}, [logItems]); // Infinite loop!
```

Example 4 (jsx):
```jsx
// ✅ Call it from the event handlerconst logItems = () => {  console.log(items);};return <button onClick={logItems}>Log</button>;// ✅ Or derive during render if there's no side effectitems.forEach(item => {  console.log(item);});
```

---

## gating

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/gating

**Contents:**
- gating
- Rule Details
  - Invalid
  - Valid

Validates configuration of gating mode.

Gating mode lets you gradually adopt React Compiler by marking specific components for optimization. This rule ensures your gating configuration is valid so the compiler knows which components to process.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

**Examples:**

Example 1 (css):
```css
// ❌ Missing required fieldsmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      gating: {        importSpecifierName: '__experimental_useCompiler'        // Missing 'source' field      }    }]  ]};// ❌ Invalid gating typemodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      gating: '__experimental_useCompiler' // Should be object    }]  ]};
```

Example 2 (julia):
```julia
// ✅ Complete gating configurationmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      gating: {        importSpecifierName: 'isCompilerEnabled', // exported function name        source: 'featureFlags' // module name      }    }]  ]};// featureFlags.jsexport function isCompilerEnabled() {  // ...}// ✅ No gating (compile everything)module.exports = {  plugins: [    ['babel-plugin-react-compiler', {      // No gating field - compiles all components    }]  ]};
```

---

## globals

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/globals

**Contents:**
- globals
- Rule Details
  - Invalid
  - Valid

Validates against assignment/mutation of globals during render, part of ensuring that side effects must run outside of render.

Global variables exist outside React’s control. When you modify them during render, you break React’s assumption that rendering is pure. This can cause components to behave differently in development vs production, break Fast Refresh, and make your app impossible to optimize with features like React Compiler.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

**Examples:**

Example 1 (javascript):
```javascript
// ❌ Global counterlet renderCount = 0;function Component() {  renderCount++; // Mutating global  return <div>Count: {renderCount}</div>;}// ❌ Modifying window propertiesfunction Component({userId}) {  window.currentUser = userId; // Global mutation  return <div>User: {userId}</div>;}// ❌ Global array pushconst events = [];function Component({event}) {  events.push(event); // Mutating global array  return <div>Events: {events.length}</div>;}// ❌ Cache manipulationconst cache = {};function Component({id}) {  if (!cache[id]) {    cache[id] = fetchData(id); // Modifying cache during render  }  return <div>{cache[id]}</div>;}
```

Example 2 (jsx):
```jsx
// ✅ Use state for countersfunction Component() {  const [clickCount, setClickCount] = useState(0);  const handleClick = () => {    setClickCount(c => c + 1);  };  return (    <button onClick={handleClick}>      Clicked: {clickCount} times    </button>  );}// ✅ Use context for global valuesfunction Component() {  const user = useContext(UserContext);  return <div>User: {user.id}</div>;}// ✅ Synchronize external state with Reactfunction Component({title}) {  useEffect(() => {    document.title = title; // OK in effect  }, [title]);  return <div>Page: {title}</div>;}
```

---

## preserve-manual-memoization

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization

**Contents:**
- preserve-manual-memoization
- Rule Details
  - Invalid
  - Valid
- Troubleshooting
  - Should I remove my manual memoization?

Validates that existing manual memoization is preserved by the compiler. React Compiler will only compile components and hooks if its inference matches or exceeds the existing manual memoization.

React Compiler preserves your existing useMemo, useCallback, and React.memo calls. If you’ve manually memoized something, the compiler assumes you had a good reason and won’t remove it. However, incomplete dependencies prevent the compiler from understanding your code’s data flow and applying further optimizations.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

You might wonder if React Compiler makes manual memoization unnecessary:

You can safely remove it if using React Compiler:

**Examples:**

Example 1 (jsx):
```jsx
// ❌ Missing dependencies in useMemofunction Component({ data, filter }) {  const filtered = useMemo(    () => data.filter(filter),    [data] // Missing 'filter' dependency  );  return <List items={filtered} />;}// ❌ Missing dependencies in useCallbackfunction Component({ onUpdate, value }) {  const handleClick = useCallback(() => {    onUpdate(value);  }, [onUpdate]); // Missing 'value'  return <button onClick={handleClick}>Update</button>;}
```

Example 2 (jsx):
```jsx
// ✅ Complete dependenciesfunction Component({ data, filter }) {  const filtered = useMemo(    () => data.filter(filter),    [data, filter] // All dependencies included  );  return <List items={filtered} />;}// ✅ Or let the compiler handle itfunction Component({ data, filter }) {  // No manual memoization needed  const filtered = data.filter(filter);  return <List items={filtered} />;}
```

Example 3 (jsx):
```jsx
// Do I still need this?function Component({items, sortBy}) {  const sorted = useMemo(() => {    return [...items].sort((a, b) => {      return a[sortBy] - b[sortBy];    });  }, [items, sortBy]);  return <List items={sorted} />;}
```

Example 4 (jsx):
```jsx
// ✅ Better: Let the compiler optimizefunction Component({items, sortBy}) {  const sorted = [...items].sort((a, b) => {    return a[sortBy] - b[sortBy];  });  return <List items={sorted} />;}
```

---

## refs

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/refs

**Contents:**
- refs
- Rule Details
- How It Detects Refs
- Common Violations
  - Invalid
  - Valid
- Troubleshooting
  - The lint flagged my plain object with .current

Validates correct usage of refs, not reading/writing during render. See the “pitfalls” section in useRef() usage.

Refs hold values that aren’t used for rendering. Unlike state, changing a ref doesn’t trigger a re-render. Reading or writing ref.current during render breaks React’s expectations. Refs might not be initialized when you try to read them, and their values can be stale or inconsistent.

The lint only applies these rules to values it knows are refs. A value is inferred as a ref when the compiler sees any of the following patterns:

Returned from useRef() or React.createRef().

An identifier named ref or ending in Ref that reads from or writes to .current.

Passed through a JSX ref prop (for example <div ref={someRef} />).

Once something is marked as a ref, that inference follows the value through assignments, destructuring, or helper calls. This lets the lint surface violations even when ref.current is accessed inside another function that received the ref as an argument.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

The name heuristic intentionally treats ref.current and fooRef.current as real refs. If you’re modeling a custom container object, pick a different name (for example, box) or move the mutable value into state. Renaming avoids the lint because the compiler stops inferring it as a ref.

**Examples:**

Example 1 (jsx):
```jsx
const scrollRef = useRef(null);
```

Example 2 (unknown):
```unknown
buttonRef.current = node;
```

Example 3 (jsx):
```jsx
<input ref={inputRef} />
```

Example 4 (jsx):
```jsx
// ❌ Reading ref during renderfunction Component() {  const ref = useRef(0);  const value = ref.current; // Don't read during render  return <div>{value}</div>;}// ❌ Modifying ref during renderfunction Component({value}) {  const ref = useRef(null);  ref.current = value; // Don't modify during render  return <div />;}
```

---

## Rules of Hooks

**URL:** https://react.dev/reference/rules/rules-of-hooks

**Contents:**
- Rules of Hooks
- Only call Hooks at the top level
  - Note
- Only call Hooks from React functions

Hooks are defined using JavaScript functions, but they represent a special type of reusable UI logic with restrictions on where they can be called.

Functions whose names start with use are called Hooks in React.

Don’t call Hooks inside loops, conditions, nested functions, or try/catch/finally blocks. Instead, always use Hooks at the top level of your React function, before any early returns. You can only call Hooks while React is rendering a function component:

It’s not supported to call Hooks (functions starting with use) in any other cases, for example:

If you break these rules, you might see this error.

You can use the eslint-plugin-react-hooks plugin to catch these mistakes.

Custom Hooks may call other Hooks (that’s their whole purpose). This works because custom Hooks are also supposed to only be called while a function component is rendering.

Don’t call Hooks from regular JavaScript functions. Instead, you can:

✅ Call Hooks from React function components. ✅ Call Hooks from custom Hooks.

By following this rule, you ensure that all stateful logic in a component is clearly visible from its source code.

**Examples:**

Example 1 (jsx):
```jsx
function Counter() {  // ✅ Good: top-level in a function component  const [count, setCount] = useState(0);  // ...}function useWindowWidth() {  // ✅ Good: top-level in a custom Hook  const [width, setWidth] = useState(window.innerWidth);  // ...}
```

Example 2 (jsx):
```jsx
function Bad({ cond }) {  if (cond) {    // 🔴 Bad: inside a condition (to fix, move it outside!)    const theme = useContext(ThemeContext);  }  // ...}function Bad() {  for (let i = 0; i < 10; i++) {    // 🔴 Bad: inside a loop (to fix, move it outside!)    const theme = useContext(ThemeContext);  }  // ...}function Bad({ cond }) {  if (cond) {    return;  }  // 🔴 Bad: after a conditional return (to fix, move it before the return!)  const theme = useContext(ThemeContext);  // ...}function Bad() {  function handleClick() {    // 🔴 Bad: inside an event handler (to fix, move it outside!)    const theme = useContext(ThemeContext);  }  // ...}function Bad() {  const style = useMemo(() => {    // 🔴 Bad: inside useMemo (to fix, move it outside!)    const theme = useContext(ThemeContext);    return createStyle(theme);  });  // ...}class Bad extends React.Component {  render() {    // 🔴 Bad: inside a class component (to fix, write a function component instead of a class!)    useEffect(() => {})    // ...  }}function Bad() {  try {    // 🔴 Bad: inside try/catch/finally block (to fix, move it outside!)    const [x, setX] = useState(0);  } catch {    const [x, setX] = useState(1);  }}
```

Example 3 (javascript):
```javascript
function FriendList() {  const [onlineStatus, setOnlineStatus] = useOnlineStatus(); // ✅}function setOnlineStatus() { // ❌ Not a component or custom Hook!  const [onlineStatus, setOnlineStatus] = useOnlineStatus();}
```

---

## unsupported-syntax

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/unsupported-syntax

**Contents:**
- unsupported-syntax
- Rule Details
  - Invalid
  - Valid
- Troubleshooting
  - I need to evaluate dynamic code
  - Note

Validates against syntax that React Compiler does not support. If you need to, you can still use this syntax outside of React, such as in a standalone utility function.

React Compiler needs to statically analyze your code to apply optimizations. Features like eval and with make it impossible to statically understand what the code does at compile time, so the compiler can’t optimize components that use them.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

You might need to evaluate user-provided code:

Use a safe expression parser instead:

Never use eval with user input - it’s a security risk. Use dedicated parsing libraries for specific use cases like mathematical expressions, JSON parsing, or template evaluation.

**Examples:**

Example 1 (typescript):
```typescript
// ❌ Using eval in componentfunction Component({ code }) {  const result = eval(code); // Can't be analyzed  return <div>{result}</div>;}// ❌ Using with statementfunction Component() {  with (Math) { // Changes scope dynamically    return <div>{sin(PI / 2)}</div>;  }}// ❌ Dynamic property access with evalfunction Component({propName}) {  const value = eval(`props.${propName}`);  return <div>{value}</div>;}
```

Example 2 (typescript):
```typescript
// ✅ Use normal property accessfunction Component({propName, props}) {  const value = props[propName]; // Analyzable  return <div>{value}</div>;}// ✅ Use standard Math methodsfunction Component() {  return <div>{Math.sin(Math.PI / 2)}</div>;}
```

Example 3 (typescript):
```typescript
// ❌ Wrong: eval in componentfunction Calculator({expression}) {  const result = eval(expression); // Unsafe and unoptimizable  return <div>Result: {result}</div>;}
```

Example 4 (jsx):
```jsx
// ✅ Better: Use a safe parserimport {evaluate} from 'mathjs'; // or similar libraryfunction Calculator({expression}) {  const [result, setResult] = useState(null);  const calculate = () => {    try {      // Safe mathematical expression evaluation      setResult(evaluate(expression));    } catch (error) {      setResult('Invalid expression');    }  };  return (    <div>      <button onClick={calculate}>Calculate</button>      {result && <div>Result: {result}</div>}    </div>  );}
```

---

## useContext

**URL:** https://react.dev/reference/react/useContext

**Contents:**
- useContext
- Reference
  - useContext(SomeContext)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Passing data deeply into the tree
  - Pitfall
  - Updating data passed via context

useContext is a React Hook that lets you read and subscribe to context from your component.

Call useContext at the top level of your component to read and subscribe to context.

See more examples below.

useContext returns the context value for the calling component. It is determined as the value passed to the closest SomeContext above the calling component in the tree. If there is no such provider, then the returned value will be the defaultValue you have passed to createContext for that context. The returned value is always up-to-date. React automatically re-renders components that read some context if it changes.

Call useContext at the top level of your component to read and subscribe to context.

useContext returns the context value for the context you passed. To determine the context value, React searches the component tree and finds the closest context provider above for that particular context.

To pass context to a Button, wrap it or one of its parent components into the corresponding context provider:

It doesn’t matter how many layers of components there are between the provider and the Button. When a Button anywhere inside of Form calls useContext(ThemeContext), it will receive "dark" as the value.

useContext() always looks for the closest provider above the component that calls it. It searches upwards and does not consider providers in the component from which you’re calling useContext().

Often, you’ll want the context to change over time. To update context, combine it with state. Declare a state variable in the parent component, and pass the current state down as the context value to the provider.

Now any Button inside of the provider will receive the current theme value. If you call setTheme to update the theme value that you pass to the provider, all Button components will re-render with the new 'light' value.

In this example, the MyApp component holds a state variable which is then passed to the ThemeContext provider. Checking the “Dark mode” checkbox updates the state. Changing the provided value re-renders all the components using that context.

Note that value="dark" passes the "dark" string, but value={theme} passes the value of the JavaScript theme variable with JSX curly braces. Curly braces also let you pass context values that aren’t strings.

If React can’t find any providers of that particular context in the parent tree, the context value returned by useContext() will be equal to the default value that you specified when you created that context:

The default value never changes. If you want to update context, use it with state as described above.

Often, instead of null, there is some more meaningful value you can use as a default, for example:

This way, if you accidentally render some component without a corresponding provider, it won’t break. This also helps your components work well in a test environment without setting up a lot of providers in the tests.

In the example below, the “Toggle theme” button is always light because it’s outside any theme context provider and the default context theme value is 'light'. Try editing the default theme to be 'dark'.

You can override the context for a part of the tree by wrapping that part in a provider with a different value.

You can nest and override providers as many times as you need.

Here, the button inside the Footer receives a different context value ("light") than the buttons outside ("dark").

You can pass any values via context, including objects and functions.

Here, the context value is a JavaScript object with two properties, one of which is a function. Whenever MyApp re-renders (for example, on a route update), this will be a different object pointing at a different function, so React will also have to re-render all components deep in the tree that call useContext(AuthContext).

In smaller apps, this is not a problem. However, there is no need to re-render them if the underlying data, like currentUser, has not changed. To help React take advantage of that fact, you may wrap the login function with useCallback and wrap the object creation into useMemo. This is a performance optimization:

As a result of this change, even if MyApp needs to re-render, the components calling useContext(AuthContext) won’t need to re-render unless currentUser has changed.

Read more about useMemo and useCallback.

There are a few common ways that this can happen:

You might have a provider without a value in the tree:

If you forget to specify value, it’s like passing value={undefined}.

You may have also mistakingly used a different prop name by mistake:

In both of these cases you should see a warning from React in the console. To fix them, call the prop value:

Note that the default value from your createContext(defaultValue) call is only used if there is no matching provider above at all. If there is a <SomeContext value={undefined}> component somewhere in the parent tree, the component calling useContext(SomeContext) will receive undefined as the context value.

**Examples:**

Example 1 (javascript):
```javascript
const value = useContext(SomeContext)
```

Example 2 (javascript):
```javascript
import { useContext } from 'react';function MyComponent() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
import { useContext } from 'react';function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 4 (jsx):
```jsx
function MyPage() {  return (    <ThemeContext value="dark">      <Form />    </ThemeContext>  );}function Form() {  // ... renders buttons inside ...}
```

---

## useEffectEvent

**URL:** https://react.dev/reference/react/useEffectEvent

**Contents:**
- useEffectEvent
- Reference
  - useEffectEvent(callback)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Reading the latest props and state

useEffectEvent is a React Hook that lets you extract non-reactive logic from your Effects into a reusable function called an Effect Event.

Call useEffectEvent at the top level of your component to declare an Effect Event. Effect Events are functions you can call inside Effects, such as useEffect:

See more examples below.

Returns an Effect Event function. You can call this function inside useEffect, useLayoutEffect, or useInsertionEffect.

Typically, when you access a reactive value inside an Effect, you must include it in the dependency array. This makes sure your Effect runs again whenever that value changes, which is usually the desired behavior.

But in some cases, you may want to read the most recent props or state inside an Effect without causing the Effect to re-run when those values change.

To read the latest props or state in your Effect, without making those values reactive, include them in an Effect Event.

In this example, the Effect should re-run after a render when url changes (to log the new page visit), but it should not re-run when numberOfItems changes. By wrapping the logging logic in an Effect Event, numberOfItems becomes non-reactive. It’s always read from the latest value without triggering the Effect.

You can pass reactive values like url as arguments to the Effect Event to keep them reactive while accessing the latest non-reactive values inside the event.

**Examples:**

Example 1 (javascript):
```javascript
const onSomething = useEffectEvent(callback)
```

Example 2 (javascript):
```javascript
import { useEffectEvent, useEffect } from 'react';function ChatRoom({ roomId, theme }) {  const onConnected = useEffectEvent(() => {    showNotification('Connected!', theme);  });  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.on('connected', () => {      onConnected();    });    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...}
```

Example 3 (javascript):
```javascript
import { useEffect, useContext, useEffectEvent } from 'react';function Page({ url }) {  const { items } = useContext(ShoppingCartContext);  const numberOfItems = items.length;  const onNavigate = useEffectEvent((visitedUrl) => {    logVisit(visitedUrl, numberOfItems);  });  useEffect(() => {    onNavigate(url);  }, [url]);  // ...}
```

---

## useEffect

**URL:** https://react.dev/reference/react/useEffect

**Contents:**
- useEffect
- Reference
  - useEffect(setup, dependencies?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Connecting to an external system
  - Note
    - Examples of connecting to an external system

useEffect is a React Hook that lets you synchronize a component with an external system.

Call useEffect at the top level of your component to declare an Effect:

See more examples below.

setup: The function with your Effect’s logic. Your setup function may also optionally return a cleanup function. When your component commits, React will run your setup function. After every commit with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. After your component is removed from the DOM, React will run your cleanup function.

optional dependencies: The list of all reactive values referenced inside of the setup code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is configured for React, it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like [dep1, dep2, dep3]. React will compare each dependency with its previous value using the Object.is comparison. If you omit this argument, your Effect will re-run after every commit of the component. See the difference between passing an array of dependencies, an empty array, and no dependencies at all.

useEffect returns undefined.

useEffect is a Hook, so you can only call it at the top level of your component or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.

If you’re not trying to synchronize with some external system, you probably don’t need an Effect.

When Strict Mode is on, React will run one extra development-only setup+cleanup cycle before the first real setup. This is a stress-test that ensures that your cleanup logic “mirrors” your setup logic and that it stops or undoes whatever the setup is doing. If this causes a problem, implement the cleanup function.

If some of your dependencies are objects or functions defined inside the component, there is a risk that they will cause the Effect to re-run more often than needed. To fix this, remove unnecessary object and function dependencies. You can also extract state updates and non-reactive logic outside of your Effect.

If your Effect wasn’t caused by an interaction (like a click), React will generally let the browser paint the updated screen first before running your Effect. If your Effect is doing something visual (for example, positioning a tooltip), and the delay is noticeable (for example, it flickers), replace useEffect with useLayoutEffect.

If your Effect is caused by an interaction (like a click), React may run your Effect before the browser paints the updated screen. This ensures that the result of the Effect can be observed by the event system. Usually, this works as expected. However, if you must defer the work until after paint, such as an alert(), you can use setTimeout. See reactwg/react-18/128 for more information.

Even if your Effect was caused by an interaction (like a click), React may allow the browser to repaint the screen before processing the state updates inside your Effect. Usually, this works as expected. However, if you must block the browser from repainting the screen, you need to replace useEffect with useLayoutEffect.

Effects only run on the client. They don’t run during server rendering.

Some components need to stay connected to the network, some browser API, or a third-party library, while they are displayed on the page. These systems aren’t controlled by React, so they are called external.

To connect your component to some external system, call useEffect at the top level of your component:

You need to pass two arguments to useEffect:

React calls your setup and cleanup functions whenever it’s necessary, which may happen multiple times:

Let’s illustrate this sequence for the example above.

When the ChatRoom component above gets added to the page, it will connect to the chat room with the initial serverUrl and roomId. If either serverUrl or roomId change as a result of a commit (say, if the user picks a different chat room in a dropdown), your Effect will disconnect from the previous room, and connect to the next one. When the ChatRoom component is removed from the page, your Effect will disconnect one last time.

To help you find bugs, in development React runs setup and cleanup one extra time before the setup. This is a stress-test that verifies your Effect’s logic is implemented correctly. If this causes visible issues, your cleanup function is missing some logic. The cleanup function should stop or undo whatever the setup function was doing. The rule of thumb is that the user shouldn’t be able to distinguish between the setup being called once (as in production) and a setup → cleanup → setup sequence (as in development). See common solutions.

Try to write every Effect as an independent process and think about a single setup/cleanup cycle at a time. It shouldn’t matter whether your component is mounting, updating, or unmounting. When your cleanup logic correctly “mirrors” the setup logic, your Effect is resilient to running setup and cleanup as often as needed.

An Effect lets you keep your component synchronized with some external system (like a chat service). Here, external system means any piece of code that’s not controlled by React, such as:

If you’re not connecting to any external system, you probably don’t need an Effect.

In this example, the ChatRoom component uses an Effect to stay connected to an external system defined in chat.js. Press “Open chat” to make the ChatRoom component appear. This sandbox runs in development mode, so there is an extra connect-and-disconnect cycle, as explained here. Try changing the roomId and serverUrl using the dropdown and the input, and see how the Effect re-connects to the chat. Press “Close chat” to see the Effect disconnect one last time.

Effects are an “escape hatch”: you use them when you need to “step outside React” and when there is no better built-in solution for your use case. If you find yourself often needing to manually write Effects, it’s usually a sign that you need to extract some custom Hooks for common behaviors your components rely on.

For example, this useChatRoom custom Hook “hides” the logic of your Effect behind a more declarative API:

Then you can use it from any component like this:

There are also many excellent custom Hooks for every purpose available in the React ecosystem.

Learn more about wrapping Effects in custom Hooks.

This example is identical to one of the earlier examples, but the logic is extracted to a custom Hook.

Sometimes, you want to keep an external system synchronized to some prop or state of your component.

For example, if you have a third-party map widget or a video player component written without React, you can use an Effect to call methods on it that make its state match the current state of your React component. This Effect creates an instance of a MapWidget class defined in map-widget.js. When you change the zoomLevel prop of the Map component, the Effect calls the setZoom() on the class instance to keep it synchronized:

In this example, a cleanup function is not needed because the MapWidget class manages only the DOM node that was passed to it. After the Map React component is removed from the tree, both the DOM node and the MapWidget class instance will be automatically garbage-collected by the browser JavaScript engine.

You can use an Effect to fetch data for your component. Note that if you use a framework, using your framework’s data fetching mechanism will be a lot more efficient than writing Effects manually.

If you want to fetch data from an Effect manually, your code might look like this:

Note the ignore variable which is initialized to false, and is set to true during cleanup. This ensures your code doesn’t suffer from “race conditions”: network responses may arrive in a different order than you sent them.

You can also rewrite using the async / await syntax, but you still need to provide a cleanup function:

Writing data fetching directly in Effects gets repetitive and makes it difficult to add optimizations like caching and server rendering later. It’s easier to use a custom Hook—either your own or maintained by the community.

Writing fetch calls inside Effects is a popular way to fetch data, especially in fully client-side apps. This is, however, a very manual approach and it has significant downsides:

This list of downsides is not specific to React. It applies to fetching data on mount with any library. Like with routing, data fetching is not trivial to do well, so we recommend the following approaches:

You can continue fetching data directly in Effects if neither of these approaches suit you.

Notice that you can’t “choose” the dependencies of your Effect. Every reactive value used by your Effect’s code must be declared as a dependency. Your Effect’s dependency list is determined by the surrounding code:

If either serverUrl or roomId change, your Effect will reconnect to the chat using the new values.

Reactive values include props and all variables and functions declared directly inside of your component. Since roomId and serverUrl are reactive values, you can’t remove them from the dependencies. If you try to omit them and your linter is correctly configured for React, the linter will flag this as a mistake you need to fix:

To remove a dependency, you need to “prove” to the linter that it doesn’t need to be a dependency. For example, you can move serverUrl out of your component to prove that it’s not reactive and won’t change on re-renders:

Now that serverUrl is not a reactive value (and can’t change on a re-render), it doesn’t need to be a dependency. If your Effect’s code doesn’t use any reactive values, its dependency list should be empty ([]):

An Effect with empty dependencies doesn’t re-run when any of your component’s props or state change.

If you have an existing codebase, you might have some Effects that suppress the linter like this:

When dependencies don’t match the code, there is a high risk of introducing bugs. By suppressing the linter, you “lie” to React about the values your Effect depends on. Instead, prove they’re unnecessary.

If you specify the dependencies, your Effect runs after the initial commit and after commits with changed dependencies.

In the below example, serverUrl and roomId are reactive values, so they both must be specified as dependencies. As a result, selecting a different room in the dropdown or editing the server URL input causes the chat to re-connect. However, since message isn’t used in the Effect (and so it isn’t a dependency), editing the message doesn’t re-connect to the chat.

When you want to update state based on previous state from an Effect, you might run into a problem:

Since count is a reactive value, it must be specified in the list of dependencies. However, that causes the Effect to cleanup and setup again every time the count changes. This is not ideal.

To fix this, pass the c => c + 1 state updater to setCount:

Now that you’re passing c => c + 1 instead of count + 1, your Effect no longer needs to depend on count. As a result of this fix, it won’t need to cleanup and setup the interval again every time the count changes.

If your Effect depends on an object or a function created during rendering, it might run too often. For example, this Effect re-connects after every commit because the options object is different for every render:

Avoid using an object created during rendering as a dependency. Instead, create the object inside the Effect:

Now that you create the options object inside the Effect, the Effect itself only depends on the roomId string.

With this fix, typing into the input doesn’t reconnect the chat. Unlike an object which gets re-created, a string like roomId doesn’t change unless you set it to another value. Read more about removing dependencies.

If your Effect depends on an object or a function created during rendering, it might run too often. For example, this Effect re-connects after every commit because the createOptions function is different for every render:

By itself, creating a function from scratch on every re-render is not a problem. You don’t need to optimize that. However, if you use it as a dependency of your Effect, it will cause your Effect to re-run after every commit.

Avoid using a function created during rendering as a dependency. Instead, declare it inside the Effect:

Now that you define the createOptions function inside the Effect, the Effect itself only depends on the roomId string. With this fix, typing into the input doesn’t reconnect the chat. Unlike a function which gets re-created, a string like roomId doesn’t change unless you set it to another value. Read more about removing dependencies.

By default, when you read a reactive value from an Effect, you have to add it as a dependency. This ensures that your Effect “reacts” to every change of that value. For most dependencies, that’s the behavior you want.

However, sometimes you’ll want to read the latest props and state from an Effect without “reacting” to them. For example, imagine you want to log the number of the items in the shopping cart for every page visit:

What if you want to log a new page visit after every url change, but not if only the shoppingCart changes? You can’t exclude shoppingCart from dependencies without breaking the reactivity rules. However, you can express that you don’t want a piece of code to “react” to changes even though it is called from inside an Effect. Declare an Effect Event with the useEffectEvent Hook, and move the code reading shoppingCart inside of it:

Effect Events are not reactive and must always be omitted from dependencies of your Effect. This is what lets you put non-reactive code (where you can read the latest value of some props and state) inside of them. By reading shoppingCart inside of onVisit, you ensure that shoppingCart won’t re-run your Effect.

Read more about how Effect Events let you separate reactive and non-reactive code.

If your app uses server rendering (either directly or via a framework), your component will render in two different environments. On the server, it will render to produce the initial HTML. On the client, React will run the rendering code again so that it can attach your event handlers to that HTML. This is why, for hydration to work, your initial render output must be identical on the client and the server.

In rare cases, you might need to display different content on the client. For example, if your app reads some data from localStorage, it can’t possibly do that on the server. Here is how you could implement this:

While the app is loading, the user will see the initial render output. Then, when it’s loaded and hydrated, your Effect will run and set didMount to true, triggering a re-render. This will switch to the client-only render output. Effects don’t run on the server, so this is why didMount was false during the initial server render.

Use this pattern sparingly. Keep in mind that users with a slow connection will see the initial content for quite a bit of time—potentially, many seconds—so you don’t want to make jarring changes to your component’s appearance. In many cases, you can avoid the need for this by conditionally showing different things with CSS.

When Strict Mode is on, in development, React runs setup and cleanup one extra time before the actual setup.

This is a stress-test that verifies your Effect’s logic is implemented correctly. If this causes visible issues, your cleanup function is missing some logic. The cleanup function should stop or undo whatever the setup function was doing. The rule of thumb is that the user shouldn’t be able to distinguish between the setup being called once (as in production) and a setup → cleanup → setup sequence (as in development).

Read more about how this helps find bugs and how to fix your logic.

First, check that you haven’t forgotten to specify the dependency array:

If you’ve specified the dependency array but your Effect still re-runs in a loop, it’s because one of your dependencies is different on every re-render.

You can debug this problem by manually logging your dependencies to the console:

You can then right-click on the arrays from different re-renders in the console and select “Store as a global variable” for both of them. Assuming the first one got saved as temp1 and the second one got saved as temp2, you can then use the browser console to check whether each dependency in both arrays is the same:

When you find the dependency that is different on every re-render, you can usually fix it in one of these ways:

As a last resort (if these methods didn’t help), wrap its creation with useMemo or useCallback (for functions).

If your Effect runs in an infinite cycle, these two things must be true:

Before you start fixing the problem, ask yourself whether your Effect is connecting to some external system (like DOM, network, a third-party widget, and so on). Why does your Effect need to set state? Does it synchronize with that external system? Or are you trying to manage your application’s data flow with it?

If there is no external system, consider whether removing the Effect altogether would simplify your logic.

If you’re genuinely synchronizing with some external system, think about why and under what conditions your Effect should update the state. Has something changed that affects your component’s visual output? If you need to keep track of some data that isn’t used by rendering, a ref (which doesn’t trigger re-renders) might be more appropriate. Verify your Effect doesn’t update the state (and trigger re-renders) more than needed.

Finally, if your Effect is updating the state at the right time, but there is still a loop, it’s because that state update leads to one of the Effect’s dependencies changing. Read how to debug dependency changes.

The cleanup function runs not only during unmount, but before every re-render with changed dependencies. Additionally, in development, React runs setup+cleanup one extra time immediately after component mounts.

If you have cleanup code without corresponding setup code, it’s usually a code smell:

Your cleanup logic should be “symmetrical” to the setup logic, and should stop or undo whatever setup did:

Learn how the Effect lifecycle is different from the component’s lifecycle.

If your Effect must block the browser from painting the screen, replace useEffect with useLayoutEffect. Note that this shouldn’t be needed for the vast majority of Effects. You’ll only need this if it’s crucial to run your Effect before the browser paint: for example, to measure and position a tooltip before the user sees it.

**Examples:**

Example 1 (jsx):
```jsx
useEffect(setup, dependencies?)
```

Example 2 (jsx):
```jsx
import { useState, useEffect } from 'react';import { createConnection } from './chat.js';function ChatRoom({ roomId }) {  const [serverUrl, setServerUrl] = useState('https://localhost:1234');  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => {      connection.disconnect();    };  }, [serverUrl, roomId]);  // ...}
```

Example 3 (jsx):
```jsx
import { useState, useEffect } from 'react';import { createConnection } from './chat.js';function ChatRoom({ roomId }) {  const [serverUrl, setServerUrl] = useState('https://localhost:1234');  useEffect(() => {  	const connection = createConnection(serverUrl, roomId);    connection.connect();  	return () => {      connection.disconnect();  	};  }, [serverUrl, roomId]);  // ...}
```

Example 4 (javascript):
```javascript
function useChatRoom({ serverUrl, roomId }) {  useEffect(() => {    const options = {      serverUrl: serverUrl,      roomId: roomId    };    const connection = createConnection(options);    connection.connect();    return () => connection.disconnect();  }, [roomId, serverUrl]);}
```

---

## useFormStatus

**URL:** https://react.dev/reference/react-dom/hooks/useFormStatus

**Contents:**
- useFormStatus
- Reference
  - useFormStatus()
    - Parameters
    - Returns
    - Caveats
- Usage
  - Display a pending state during form submission
  - Pitfall
      - useFormStatus will not return status information for a <form> rendered in the same component.

useFormStatus is a Hook that gives you status information of the last form submission.

The useFormStatus Hook provides status information of the last form submission.

To get status information, the Submit component must be rendered within a <form>. The Hook returns information like the pending property which tells you if the form is actively submitting.

In the above example, Submit uses this information to disable <button> presses while the form is submitting.

See more examples below.

useFormStatus does not take any parameters.

A status object with the following properties:

pending: A boolean. If true, this means the parent <form> is pending submission. Otherwise, false.

data: An object implementing the FormData interface that contains the data the parent <form> is submitting. If there is no active submission or no parent <form>, it will be null.

method: A string value of either 'get' or 'post'. This represents whether the parent <form> is submitting with either a GET or POST HTTP method. By default, a <form> will use the GET method and can be specified by the method property.

To display a pending state while a form is submitting, you can call the useFormStatus Hook in a component rendered in a <form> and read the pending property returned.

Here, we use the pending property to indicate the form is submitting.

The useFormStatus Hook only returns status information for a parent <form> and not for any <form> rendered in the same component calling the Hook, or child components.

Instead call useFormStatus from inside a component that is located inside <form>.

You can use the data property of the status information returned from useFormStatus to display what data is being submitted by the user.

Here, we have a form where users can request a username. We can use useFormStatus to display a temporary status message confirming what username they have requested.

useFormStatus will only return status information for a parent <form>.

If the component that calls useFormStatus is not nested in a <form>, status.pending will always return false. Verify useFormStatus is called in a component that is a child of a <form> element.

useFormStatus will not track the status of a <form> rendered in the same component. See Pitfall for more details.

**Examples:**

Example 1 (unknown):
```unknown
const { pending, data, method, action } = useFormStatus();
```

Example 2 (jsx):
```jsx
import { useFormStatus } from "react-dom";import action from './actions';function Submit() {  const status = useFormStatus();  return <button disabled={status.pending}>Submit</button>}export default function App() {  return (    <form action={action}>      <Submit />    </form>  );}
```

Example 3 (jsx):
```jsx
function Form() {  // 🚩 `pending` will never be true  // useFormStatus does not track the form rendered in this component  const { pending } = useFormStatus();  return <form action={submit}></form>;}
```

Example 4 (jsx):
```jsx
function Submit() {  // ✅ `pending` will be derived from the form that wraps the Submit component  const { pending } = useFormStatus();   return <button disabled={pending}>...</button>;}function Form() {  // This is the <form> `useFormStatus` tracks  return (    <form action={submit}>      <Submit />    </form>  );}
```

---

## use-memo

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/use-memo

**Contents:**
- use-memo
- Rule Details
  - Invalid
  - Valid
- Troubleshooting
  - I need to run side effects when dependencies change

Validates that the useMemo hook is used with a return value. See useMemo docs for more information.

useMemo is for computing and caching expensive values, not for side effects. Without a return value, useMemo returns undefined, which defeats its purpose and likely indicates you’re using the wrong hook.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

You might try to use useMemo for side effects:

If the side effect needs to happen in response to user interaction, it’s best to colocate the side effect with the event:

If the side effect sychronizes React state with some external state (or vice versa), use useEffect:

**Examples:**

Example 1 (javascript):
```javascript
// ❌ No return valuefunction Component({ data }) {  const processed = useMemo(() => {    data.forEach(item => console.log(item));    // Missing return!  }, [data]);  return <div>{processed}</div>; // Always undefined}
```

Example 2 (jsx):
```jsx
// ✅ Returns computed valuefunction Component({ data }) {  const processed = useMemo(() => {    return data.map(item => item * 2);  }, [data]);  return <div>{processed}</div>;}
```

Example 3 (jsx):
```jsx
// ❌ Wrong: Side effects in useMemofunction Component({user}) {  // No return value, just side effect  useMemo(() => {    analytics.track('UserViewed', {userId: user.id});  }, [user.id]);  // Not assigned to a variable  useMemo(() => {    return analytics.track('UserViewed', {userId: user.id});  }, [user.id]);}
```

Example 4 (jsx):
```jsx
// ✅ Good: Side effects in event handlersfunction Component({user}) {  const handleClick = () => {    analytics.track('ButtonClicked', {userId: user.id});    // Other click logic...  };  return <button onClick={handleClick}>Click me</button>;}
```

---
