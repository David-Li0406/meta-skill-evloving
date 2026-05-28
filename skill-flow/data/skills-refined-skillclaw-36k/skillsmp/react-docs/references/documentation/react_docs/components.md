# React_Docs - Components

**Pages:** 33

---

## <Activity>

**URL:** https://react.dev/reference/react/Activity

**Contents:**
- <Activity>
- Reference
  - <Activity>
    - Props
    - Caveats
- Usage
  - Restoring the state of hidden components
  - Restoring the DOM of hidden components
  - Pre-rendering content that’s likely to become visible
  - Note

<Activity> lets you hide and restore the UI and internal state of its children.

You can use Activity to hide part of your application:

When an Activity boundary is hidden, React will visually hide its children using the display: "none" CSS property. It will also destroy their Effects, cleaning up any active subscriptions.

While hidden, children still re-render in response to new props, albeit at a lower priority than the rest of the content.

When the boundary becomes visible again, React will reveal the children with their previous state restored, and re-create their Effects.

In this way, Activity can be thought of as a mechanism for rendering “background activity”. Rather than completely discarding content that’s likely to become visible again, you can use Activity to maintain and restore that content’s UI and internal state, while ensuring that your hidden content has no unwanted side effects.

See more examples below.

In React, when you want to conditionally show or hide a component, you typically mount or unmount it based on that condition:

But unmounting a component destroys its internal state, which is not always what you want.

When you hide a component using an Activity boundary instead, React will “save” its state for later:

This makes it possible to hide and then later restore components in the state they were previously in.

The following example has a sidebar with an expandable section. You can press “Overview” to reveal the three subitems below it. The main app area also has a button that hides and shows the sidebar.

Try expanding the Overview section, and then toggling the sidebar closed then open:

The Overview section always starts out collapsed. Because we unmount the sidebar when isShowingSidebar flips to false, all its internal state is lost.

This is a perfect use case for Activity. We can preserve the internal state of our sidebar, even when visually hiding it.

Let’s replace the conditional rendering of our sidebar with an Activity boundary:

and check out the new behavior:

Our sidebar’s internal state is now restored, without any changes to its implementation.

Since Activity boundaries hide their children using display: none, their children’s DOM is also preserved when hidden. This makes them great for maintaining ephemeral state in parts of the UI that the user is likely to interact with again.

In this example, the Contact tab has a <textarea> where the user can enter a message. If you enter some text, change to the Home tab, then change back to the Contact tab, the draft message is lost:

This is because we’re fully unmounting Contact in App. When the Contact tab unmounts, the <textarea> element’s internal DOM state is lost.

If we switch to using an Activity boundary to show and hide the active tab, we can preserve the state of each tab’s DOM. Try entering text and switching tabs again, and you’ll see the draft message is no longer reset:

Again, the Activity boundary let us preserve the Contact tab’s internal state without changing its implementation.

So far, we’ve seen how Activity can hide some content that the user has interacted with, without discarding that content’s ephemeral state.

But Activity boundaries can also be used to prepare content that the user has yet to see for the first time:

When an Activity boundary is hidden during its initial render, its children won’t be visible on the page — but they will still be rendered, albeit at a lower priority than the visible content, and without mounting their Effects.

This pre-rendering allows the children to load any code or data they need ahead of time, so that later, when the Activity boundary becomes visible, the children can appear faster with reduced loading times.

Let’s look at an example.

In this demo, the Posts tab loads some data. If you press it, you’ll see a Suspense fallback displayed while the data is being fetched:

This is because App doesn’t mount Posts until its tab is active.

If we update App to use an Activity boundary to show and hide the active tab, Posts will be pre-rendered when the app first loads, allowing it to fetch its data before it becomes visible.

Try clicking the Posts tab now:

Posts was able to prepare itself for a faster render, thanks to the hidden Activity boundary.

Pre-rendering components with hidden Activity boundaries is a powerful way to reduce loading times for parts of the UI that the user is likely to interact with next.

Only Suspense-enabled data sources will be fetched during pre-rendering. They include:

Activity does not detect data that is fetched inside an Effect.

The exact way you would load data in the Posts component above depends on your framework. If you use a Suspense-enabled framework, you’ll find the details in its data fetching documentation.

Suspense-enabled data fetching without the use of an opinionated framework is not yet supported. The requirements for implementing a Suspense-enabled data source are unstable and undocumented. An official API for integrating data sources with Suspense will be released in a future version of React.

React includes an under-the-hood performance optimization called Selective Hydration. It works by hydrating your app’s initial HTML in chunks, enabling some components to become interactive even if other components on the page haven’t loaded their code or data yet.

Suspense boundaries participate in Selective Hydration, because they naturally divide your component tree into units that are independent from one another:

Here, MessageComposer can be fully hydrated during the initial render of the page, even before Chats is mounted and starts to fetch its data.

So by breaking up your component tree into discrete units, Suspense allows React to hydrate your app’s server-rendered HTML in chunks, enabling parts of your app to become interactive as fast as possible.

But what about pages that don’t use Suspense?

Take this tabs example:

Here, React must hydrate the entire page all at once. If Home or Video are slower to render, they could make the tab buttons feel unresponsive during hydration.

Adding Suspense around the active tab would solve this:

…but it would also change the UI, since the Placeholder fallback would be displayed on the initial render.

Instead, we can use Activity. Since Activity boundaries show and hide their children, they already naturally divide the component tree into independent units. And just like Suspense, this feature allows them to participate in Selective Hydration.

Let’s update our example to use Activity boundaries around the active tab:

Now our initial server-rendered HTML looks the same as it did in the original version, but thanks to Activity, React can hydrate the tab buttons first, before it even mounts Home or Video.

Thus, in addition to hiding and showing content, Activity boundaries help improve your app’s performance during hydration by letting React know which parts of your page can become interactive in isolation.

And even if your page doesn’t ever hide part of its content, you can still add always-visible Activity boundaries to improve hydration performance:

An Activity boundary hides its content by setting display: none on its children and cleaning up any of their Effects. So, most well-behaved React components that properly clean up their side effects will already be robust to being hidden by Activity.

But there are some situations where a hidden component behaves differently than an unmounted one. Most notably, since a hidden component’s DOM is not destroyed, any side effects from that DOM will persist, even after the component is hidden.

As an example, consider a <video> tag. Typically it doesn’t require any cleanup, because even if you’re playing a video, unmounting the tag stops the video and audio from playing in the browser. Try playing the video and then pressing Home in this demo:

The video stops playing as expected.

Now, let’s say we wanted to preserve the timecode where the user last watched, so that when they tab back to the video, it doesn’t start over from the beginning again.

This is a great use case for Activity!

Let’s update App to hide the inactive tab with a hidden Activity boundary instead of unmounting it, and see how the demo behaves this time:

Whoops! The video and audio continue to play even after it’s been hidden, because the tab’s <video> element is still in the DOM.

To fix this, we can add an Effect with a cleanup function that pauses the video:

We call useLayoutEffect instead of useEffect because conceptually the clean-up code is tied to the component’s UI being visually hidden. If we used a regular effect, the code could be delayed by (say) a re-suspending Suspense boundary or a View Transition.

Let’s see the new behavior. Try playing the video, switching to the Home tab, then back to the Video tab:

It works great! Our cleanup function ensures that the video stops playing if it’s ever hidden by an Activity boundary, and even better, because the <video> tag is never destroyed, the timecode is preserved, and the video itself doesn’t need to be initialized or downloaded again when the user switches back to keep watching it.

This is a great example of using Activity to preserve ephemeral DOM state for parts of the UI that become hidden, but the user is likely to interact with again soon.

Our example illustrates that for certain tags like <video>, unmounting and hiding have different behavior. If a component renders DOM that has a side effect, and you want to prevent that side effect when an Activity boundary hides it, add an Effect with a return function to clean it up.

The most common cases of this will be from the following tags:

Typically, though, most of your React components should already be robust to being hidden by an Activity boundary. And conceptually, you should think of “hidden” Activities as being unmounted.

To eagerly discover other Effects that don’t have proper cleanup, which is important not only for Activity boundaries but for many other behaviors in React, we recommend using <StrictMode>.

When an <Activity> is “hidden”, all its children’s Effects are cleaned up. Conceptually, the children are unmounted, but React saves their state for later. This is a feature of Activity because it means subscriptions won’t be active for hidden parts of the UI, reducing the amount of work needed for hidden content.

If you’re relying on an Effect mounting to clean up a component’s side effects, refactor the Effect to do the work in the returned cleanup function instead.

To eagerly find problematic Effects, we recommend adding <StrictMode> which will eagerly perform Activity unmounts and mounts to catch any unexpected side-effects.

**Examples:**

Example 1 (jsx):
```jsx
<Activity mode={visibility}>  <Sidebar /></Activity>
```

Example 2 (jsx):
```jsx
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>  <Sidebar /></Activity>
```

Example 3 (jsx):
```jsx
{isShowingSidebar && (  <Sidebar />)}
```

Example 4 (jsx):
```jsx
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>  <Sidebar /></Activity>
```

---

## Built-in React APIs

**URL:** https://react.dev/reference/react/apis

**Contents:**
- Built-in React APIs
- Resource APIs

In addition to Hooks and Components, the react package exports a few other APIs that are useful for defining components. This page lists all the remaining modern React APIs.

Resources can be accessed by a component without having them as part of their state. For example, a component can read a message from a Promise or read styling information from a context.

To read a value from a resource, use this API:

**Examples:**

Example 1 (javascript):
```javascript
function MessageComponent({ messagePromise }) {  const message = use(messagePromise);  const theme = use(ThemeContext);  // ...}
```

---

## Built-in React Components

**URL:** https://react.dev/reference/react/components

**Contents:**
- Built-in React Components
- Built-in components
- Your own components

React exposes a few built-in components that you can use in your JSX.

You can also define your own components as JavaScript functions.

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (jsx):
```jsx
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## Common components (e.g. <div>)

**URL:** https://react.dev/reference/react-dom/components/common

**Contents:**
- Common components (e.g. <div>)
- Reference
  - Common components (e.g. <div>)
    - Props
    - Caveats
  - ref callback function
    - Parameters
  - Note
    - React 19 added cleanup functions for ref callbacks.
    - Returns

All built-in browser components, such as <div>, support some common props and events.

See more examples below.

These special React props are supported for all built-in components:

children: A React node (an element, a string, a number, a portal, an empty node like null, undefined and booleans, or an array of other React nodes). Specifies the content inside the component. When you use JSX, you will usually specify the children prop implicitly by nesting tags like <div><span /></div>.

dangerouslySetInnerHTML: An object of the form { __html: '<p>some html</p>' } with a raw HTML string inside. Overrides the innerHTML property of the DOM node and displays the passed HTML inside. This should be used with extreme caution! If the HTML inside isn’t trusted (for example, if it’s based on user data), you risk introducing an XSS vulnerability. Read more about using dangerouslySetInnerHTML.

ref: A ref object from useRef or createRef, or a ref callback function, or a string for legacy refs. Your ref will be filled with the DOM element for this node. Read more about manipulating the DOM with refs.

suppressContentEditableWarning: A boolean. If true, suppresses the warning that React shows for elements that both have children and contentEditable={true} (which normally do not work together). Use this if you’re building a text input library that manages the contentEditable content manually.

suppressHydrationWarning: A boolean. If you use server rendering, normally there is a warning when the server and the client render different content. In some rare cases (like timestamps), it is very hard or impossible to guarantee an exact match. If you set suppressHydrationWarning to true, React will not warn you about mismatches in the attributes and the content of that element. It only works one level deep, and is intended to be used as an escape hatch. Don’t overuse it. Read about suppressing hydration errors.

style: An object with CSS styles, for example { fontWeight: 'bold', margin: 20 }. Similarly to the DOM style property, the CSS property names need to be written as camelCase, for example fontWeight instead of font-weight. You can pass strings or numbers as values. If you pass a number, like width: 100, React will automatically append px (“pixels”) to the value unless it’s a unitless property. We recommend using style only for dynamic styles where you don’t know the style values ahead of time. In other cases, applying plain CSS classes with className is more efficient. Read more about className and style.

These standard DOM props are also supported for all built-in components:

You can also pass custom attributes as props, for example mycustomprop="someValue". This can be useful when integrating with third-party libraries. The custom attribute name must be lowercase and must not start with on. The value will be converted to a string. If you pass null or undefined, the custom attribute will be removed.

These events fire only for the <form> elements:

These events fire only for the <dialog> elements. Unlike browser events, they bubble in React:

These events fire only for the <details> elements. Unlike browser events, they bubble in React:

These events fire for <img>, <iframe>, <object>, <embed>, <link>, and SVG <image> elements. Unlike browser events, they bubble in React:

These events fire for resources like <audio> and <video>. Unlike browser events, they bubble in React:

Instead of a ref object (like the one returned by useRef), you may pass a function to the ref attribute.

See an example of using the ref callback.

When the <div> DOM node is added to the screen, React will call your ref callback with the DOM node as the argument. When that <div> DOM node is removed, React will call your the cleanup function returned from the callback.

React will also call your ref callback whenever you pass a different ref callback. In the above example, (node) => { ... } is a different function on every render. When your component re-renders, the previous function will be called with null as the argument, and the next function will be called with the DOM node.

To support backwards compatibility, if a cleanup function is not returned from the ref callback, node will be called with null when the ref is detached. This behavior will be removed in a future version.

Your event handlers will receive a React event object. It is also sometimes known as a “synthetic event”.

It conforms to the same standard as the underlying DOM events, but fixes some browser inconsistencies.

Some React events do not map directly to the browser’s native events. For example in onMouseLeave, e.nativeEvent will point to a mouseout event. The specific mapping is not part of the public API and may change in the future. If you need the underlying browser event for some reason, read it from e.nativeEvent.

React event objects implement some of the standard Event properties:

Additionally, React event objects provide these properties:

React event objects implement some of the standard Event methods:

Additionally, React event objects provide these methods:

An event handler type for the CSS animation events.

An event handler type for the Clipboard API events.

e: A React event object with these extra ClipboardEvent properties:

An event handler type for the input method editor (IME) events.

An event handler type for the HTML Drag and Drop API events.

e: A React event object with these extra DragEvent properties:

It also includes the inherited MouseEvent properties:

It also includes the inherited UIEvent properties:

An event handler type for the focus events.

e: A React event object with these extra FocusEvent properties:

It also includes the inherited UIEvent properties:

An event handler type for generic events.

An event handler type for the onBeforeInput event.

An event handler type for keyboard events.

e: A React event object with these extra KeyboardEvent properties:

It also includes the inherited UIEvent properties:

An event handler type for mouse events.

e: A React event object with these extra MouseEvent properties:

It also includes the inherited UIEvent properties:

An event handler type for pointer events.

e: A React event object with these extra PointerEvent properties:

It also includes the inherited MouseEvent properties:

It also includes the inherited UIEvent properties:

An event handler type for touch events.

e: A React event object with these extra TouchEvent properties:

It also includes the inherited UIEvent properties:

An event handler type for the CSS transition events.

An event handler type for generic UI events.

An event handler type for the onWheel event.

e: A React event object with these extra WheelEvent properties:

It also includes the inherited MouseEvent properties:

It also includes the inherited UIEvent properties:

In React, you specify a CSS class with className. It works like the class attribute in HTML:

Then you write the CSS rules for it in a separate CSS file:

React does not prescribe how you add CSS files. In the simplest case, you’ll add a <link> tag to your HTML. If you use a build tool or a framework, consult its documentation to learn how to add a CSS file to your project.

Sometimes, the style values depend on data. Use the style attribute to pass some styles dynamically:

In the above example, style={{}} is not a special syntax, but a regular {} object inside the style={ } JSX curly braces. We recommend only using the style attribute when your styles depend on JavaScript variables.

To apply CSS classes conditionally, you need to produce the className string yourself using JavaScript.

For example, className={'row ' + (isSelected ? 'selected': '')} will produce either className="row" or className="row selected" depending on whether isSelected is true.

To make this more readable, you can use a tiny helper library like classnames:

It is especially convenient if you have multiple conditional classes:

Sometimes, you’ll need to get the browser DOM node associated with a tag in JSX. For example, if you want to focus an <input> when a button is clicked, you need to call focus() on the browser <input> DOM node.

To obtain the browser DOM node for a tag, declare a ref and pass it as the ref attribute to that tag:

React will put the DOM node into inputRef.current after it’s been rendered to the screen.

Read more about manipulating DOM with refs and check out more examples.

For more advanced use cases, the ref attribute also accepts a callback function.

You can pass a raw HTML string to an element like so:

This is dangerous. As with the underlying DOM innerHTML property, you must exercise extreme caution! Unless the markup is coming from a completely trusted source, it is trivial to introduce an XSS vulnerability this way.

For example, if you use a Markdown library that converts Markdown to HTML, you trust that its parser doesn’t contain bugs, and the user only sees their own input, you can display the resulting HTML like this:

The {__html} object should be created as close to where the HTML is generated as possible, like the above example does in the renderMarkdownToHTML function. This ensures that all raw HTML being used in your code is explicitly marked as such, and that only variables that you expect to contain HTML are passed to dangerouslySetInnerHTML. It is not recommended to create the object inline like <div dangerouslySetInnerHTML={{__html: markup}} />.

To see why rendering arbitrary HTML is dangerous, replace the code above with this:

The code embedded in the HTML will run. A hacker could use this security hole to steal user information or to perform actions on their behalf. Only use dangerouslySetInnerHTML with trusted and sanitized data.

This example shows some common mouse events and when they fire.

This example shows some common pointer events and when they fire.

In React, focus events bubble. You can use the currentTarget and relatedTarget to differentiate if the focusing or blurring events originated from outside of the parent element. The example shows how to detect focusing a child, focusing the parent element, and how to detect focus entering or leaving the whole subtree.

This example shows some common keyboard events and when they fire.

**Examples:**

Example 1 (jsx):
```jsx
<div className="wrapper">Some content</div>
```

Example 2 (jsx):
```jsx
<div ref={(node) => {  console.log('Attached', node);  return () => {    console.log('Clean up', node)  }}}>
```

Example 3 (jsx):
```jsx
<button onClick={e => {  console.log(e); // React event object}} />
```

Example 4 (jsx):
```jsx
<div  onAnimationStart={e => console.log('onAnimationStart')}  onAnimationIteration={e => console.log('onAnimationIteration')}  onAnimationEnd={e => console.log('onAnimationEnd')}/>
```

---

## Components and Hooks must be pure

**URL:** https://react.dev/reference/rules/components-and-hooks-must-be-pure

**Contents:**
- Components and Hooks must be pure
  - Note
  - Why does purity matter?
    - How does React run your code?
      - Deep Dive
    - How to tell if code runs in render
- Components and Hooks must be idempotent
- Side effects must run outside of render
  - Note
  - When is it okay to have mutation?

Pure functions only perform a calculation and nothing more. It makes your code easier to understand, debug, and allows React to automatically optimize your components and Hooks correctly.

This reference page covers advanced topics and requires familiarity with the concepts covered in the Keeping Components Pure page.

One of the key concepts that makes React, React is purity. A pure component or hook is one that is:

When render is kept pure, React can understand how to prioritize which updates are most important for the user to see first. This is made possible because of render purity: since components don’t have side effects in render, React can pause rendering components that aren’t as important to update, and only come back to them later when it’s needed.

Concretely, this means that rendering logic can be run multiple times in a way that allows React to give your user a pleasant user experience. However, if your component has an untracked side effect – like modifying the value of a global variable during render – when React runs your rendering code again, your side effects will be triggered in a way that won’t match what you want. This often leads to unexpected bugs that can degrade how your users experience your app. You can see an example of this in the Keeping Components Pure page.

React is declarative: you tell React what to render, and React will figure out how best to display it to your user. To do this, React has a few phases where it runs your code. You don’t need to know about all of these phases to use React well. But at a high level, you should know about what code runs in render, and what runs outside of it.

Rendering refers to calculating what the next version of your UI should look like. After rendering, Effects are flushed (meaning they are run until there are no more left) and may update the calculation if the Effects have impacts on layout. React takes this new calculation and compares it to the calculation used to create the previous version of your UI, then commits just the minimum changes needed to the DOM (what your user actually sees) to catch it up to the latest version.

One quick heuristic to tell if code runs during render is to examine where it is: if it’s written at the top level like in the example below, there’s a good chance it runs during render.

Event handlers and Effects don’t run in render:

Components must always return the same output with respect to their inputs – props, state, and context. This is known as idempotency. Idempotency is a term popularized in functional programming. It refers to the idea that you always get the same result every time you run that piece of code with the same inputs.

This means that all code that runs during render must also be idempotent in order for this rule to hold. For example, this line of code is not idempotent (and therefore, neither is the component):

new Date() is not idempotent as it always returns the current date and changes its result every time it’s called. When you render the above component, the time displayed on the screen will stay stuck on the time that the component was rendered. Similarly, functions like Math.random() also aren’t idempotent, because they return different results every time they’re called, even when the inputs are the same.

This doesn’t mean you shouldn’t use non-idempotent functions like new Date() at all – you should just avoid using them during render. In this case, we can synchronize the latest date to this component using an Effect:

By wrapping the non-idempotent new Date() call in an Effect, it moves that calculation outside of rendering.

If you don’t need to synchronize some external state with React, you can also consider using an event handler if it only needs to be updated in response to a user interaction.

Side effects should not run in render, as React can render components multiple times to create the best possible user experience.

Side effects are a broader term than Effects. Effects specifically refer to code that’s wrapped in useEffect, while a side effect is a general term for code that has any observable effect other than its primary result of returning a value to the caller.

Side effects are typically written inside of event handlers or Effects. But never during render.

While render must be kept pure, side effects are necessary at some point in order for your app to do anything interesting, like showing something on the screen! The key point of this rule is that side effects should not run in render, as React can render components multiple times. In most cases, you’ll use event handlers to handle side effects. Using an event handler explicitly tells React that this code doesn’t need to run during render, keeping render pure. If you’ve exhausted all options – and only as a last resort – you can also handle side effects using useEffect.

One common example of a side effect is mutation, which in JavaScript refers to changing the value of a non-primitive value. In general, while mutation is not idiomatic in React, local mutation is absolutely fine:

There is no need to contort your code to avoid local mutation. Array.map could also be used here for brevity, but there is nothing wrong with creating a local array and then pushing items into it during render.

Even though it looks like we are mutating items, the key point to note is that this code only does so locally – the mutation isn’t “remembered” when the component is rendered again. In other words, items only stays around as long as the component does. Because items is always recreated every time <FriendList /> is rendered, the component will always return the same result.

On the other hand, if items was created outside of the component, it holds on to its previous values and remembers changes:

When <FriendList /> runs again, we will continue appending friends to items every time that component is run, leading to multiple duplicated results. This version of <FriendList /> has observable side effects during render and breaks the rule.

Lazy initialization is also fine despite not being fully “pure”:

Side effects that are directly visible to the user are not allowed in the render logic of React components. In other words, merely calling a component function shouldn’t by itself produce a change on the screen.

One way to achieve the desired result of updating document.title outside of render is to synchronize the component with document.

As long as calling a component multiple times is safe and doesn’t affect the rendering of other components, React doesn’t care if it’s 100% pure in the strict functional programming sense of the word. It is more important that components must be idempotent.

A component’s props and state are immutable snapshots. Never mutate them directly. Instead, pass new props down, and use the setter function from useState.

You can think of the props and state values as snapshots that are updated after rendering. For this reason, you don’t modify the props or state variables directly: instead you pass new props, or use the setter function provided to you to tell React that state needs to update the next time the component is rendered.

Props are immutable because if you mutate them, the application will produce inconsistent output, which can be hard to debug as it may or may not work depending on the circumstances.

useState returns the state variable and a setter to update that state.

Rather than updating the state variable in-place, we need to update it using the setter function that is returned by useState. Changing values on the state variable doesn’t cause the component to update, leaving your users with an outdated UI. Using the setter function informs React that the state has changed, and that we need to queue a re-render to update the UI.

Once values are passed to a hook, you should not modify them. Like props in JSX, values become immutable when passed to a hook.

One important principle in React is local reasoning: the ability to understand what a component or hook does by looking at its code in isolation. Hooks should be treated like “black boxes” when they are called. For example, a custom hook might have used its arguments as dependencies to memoize values inside it:

If you were to mutate the Hook’s arguments, the custom hook’s memoization will become incorrect, so it’s important to avoid doing that.

Similarly, it’s important to not modify the return values of Hooks, as they may have been memoized.

Don’t mutate values after they’ve been used in JSX. Move the mutation to before the JSX is created.

When you use JSX in an expression, React may eagerly evaluate the JSX before the component finishes rendering. This means that mutating values after they’ve been passed to JSX can lead to outdated UIs, as React won’t know to update the component’s output.

**Examples:**

Example 1 (javascript):
```javascript
function Dropdown() {  const selectedItems = new Set(); // created during render  // ...}
```

Example 2 (javascript):
```javascript
function Dropdown() {  const selectedItems = new Set();  const onSelect = (item) => {    // this code is in an event handler, so it's only run when the user triggers this    selectedItems.add(item);  }}
```

Example 3 (javascript):
```javascript
function Dropdown() {  const selectedItems = new Set();  useEffect(() => {    // this code is inside of an Effect, so it only runs after rendering    logForAnalytics(selectedItems);  }, [selectedItems]);}
```

Example 4 (javascript):
```javascript
function Clock() {  const time = new Date(); // 🔴 Bad: always returns a different result!  return <span>{time.toLocaleString()}</span>}
```

---

## component-hook-factories

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/component-hook-factories

**Contents:**
- component-hook-factories
- Rule Details
  - Invalid
  - Valid
- Troubleshooting
  - I need dynamic component behavior

Validates against higher order functions defining nested components or hooks. Components and hooks should be defined at the module level.

Defining components or hooks inside other functions creates new instances on every call. React treats each as a completely different component, destroying and recreating the entire component tree, losing all state, and causing performance problems.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

You might think you need a factory to create customized components:

Pass JSX as children instead:

**Examples:**

Example 1 (jsx):
```jsx
// ❌ Factory function creating componentsfunction createComponent(defaultValue) {  return function Component() {    // ...  };}// ❌ Component defined inside componentfunction Parent() {  function Child() {    // ...  }  return <Child />;}// ❌ Hook factory functionfunction createCustomHook(endpoint) {  return function useData() {    // ...  };}
```

Example 2 (julia):
```julia
// ✅ Component defined at module levelfunction Component({ defaultValue }) {  // ...}// ✅ Custom hook at module levelfunction useData(endpoint) {  // ...}
```

Example 3 (javascript):
```javascript
// ❌ Wrong: Factory patternfunction makeButton(color) {  return function Button({children}) {    return (      <button style={{backgroundColor: color}}>        {children}      </button>    );  };}const RedButton = makeButton('red');const BlueButton = makeButton('blue');
```

Example 4 (jsx):
```jsx
// ✅ Better: Pass JSX as childrenfunction Button({color, children}) {  return (    <button style={{backgroundColor: color}}>      {children}    </button>  );}function App() {  return (    <>      <Button color="red">Red</Button>      <Button color="blue">Blue</Button>    </>  );}
```

---

## <form>

**URL:** https://react.dev/reference/react-dom/components/form

**Contents:**
- <form>
- Reference
  - <form>
    - Props
    - Caveats
- Usage
  - Handle form submission on the client
  - Handle form submission with a Server Function
  - Display a pending state during form submission
  - Optimistically updating form data

The built-in browser <form> component lets you create interactive controls for submitting information.

To create interactive controls for submitting information, render the built-in browser <form> component.

See more examples below.

<form> supports all common element props.

action: a URL or function. When a URL is passed to action the form will behave like the HTML form component. When a function is passed to action the function will handle the form submission in a Transition following the Action prop pattern. The function passed to action may be async and will be called with a single argument containing the form data of the submitted form. The action prop can be overridden by a formAction attribute on a <button>, <input type="submit">, or <input type="image"> component.

Pass a function to the action prop of form to run the function when the form is submitted. formData will be passed to the function as an argument so you can access the data submitted by the form. This differs from the conventional HTML action, which only accepts URLs. After the action function succeeds, all uncontrolled field elements in the form are reset.

Render a <form> with an input and submit button. Pass a Server Function (a function marked with 'use server') to the action prop of form to run the function when the form is submitted.

Passing a Server Function to <form action> allow users to submit forms without JavaScript enabled or before the code has loaded. This is beneficial to users who have a slow connection, device, or have JavaScript disabled and is similar to the way forms work when a URL is passed to the action prop.

You can use hidden form fields to provide data to the <form>’s action. The Server Function will be called with the hidden form field data as an instance of FormData.

In lieu of using hidden form fields to provide data to the <form>’s action, you can call the bind method to supply it with extra arguments. This will bind a new argument (productId) to the function in addition to the formData that is passed as an argument to the function.

When <form> is rendered by a Server Component, and a Server Function is passed to the <form>’s action prop, the form is progressively enhanced.

To display a pending state when a form is being submitted, you can call the useFormStatus Hook in a component rendered in a <form> and read the pending property returned.

Here, we use the pending property to indicate the form is submitting.

To learn more about the useFormStatus Hook see the reference documentation.

The useOptimistic Hook provides a way to optimistically update the user interface before a background operation, like a network request, completes. In the context of forms, this technique helps to make apps feel more responsive. When a user submits a form, instead of waiting for the server’s response to reflect the changes, the interface is immediately updated with the expected outcome.

For example, when a user types a message into the form and hits the “Send” button, the useOptimistic Hook allows the message to immediately appear in the list with a “Sending…” label, even before the message is actually sent to a server. This “optimistic” approach gives the impression of speed and responsiveness. The form then attempts to truly send the message in the background. Once the server confirms the message has been received, the “Sending…” label is removed.

In some cases the function called by a <form>’s action prop throws an error. You can handle these errors by wrapping <form> in an Error Boundary. If the function called by a <form>’s action prop throws an error, the fallback for the error boundary will be displayed.

Displaying a form submission error message before the JavaScript bundle loads for progressive enhancement requires that:

useActionState takes two parameters: a Server Function and an initial state. useActionState returns two values, a state variable and an action. The action returned by useActionState should be passed to the action prop of the form. The state variable returned by useActionState can be used to display an error message. The value returned by the Server Function passed to useActionState will be used to update the state variable.

Learn more about updating state from a form action with the useActionState docs

Forms can be designed to handle multiple submission actions based on the button pressed by the user. Each button inside a form can be associated with a distinct action or behavior by setting the formAction prop.

When a user taps a specific button, the form is submitted, and a corresponding action, defined by that button’s attributes and action, is executed. For instance, a form might submit an article for review by default but have a separate button with formAction set to save the article as a draft.

**Examples:**

Example 1 (jsx):
```jsx
<form action={search}>    <input name="query" />    <button type="submit">Search</button></form>
```

Example 2 (jsx):
```jsx
<form action={search}>    <input name="query" />    <button type="submit">Search</button></form>
```

Example 3 (javascript):
```javascript
import { updateCart } from './lib.js';function AddToCart({productId}) {  async function addToCart(formData) {    'use server'    const productId = formData.get('productId')    await updateCart(productId)  }  return (    <form action={addToCart}>        <input type="hidden" name="productId" value={productId} />        <button type="submit">Add to Cart</button>    </form>  );}
```

Example 4 (javascript):
```javascript
import { updateCart } from './lib.js';function AddToCart({productId}) {  async function addToCart(productId, formData) {    "use server";    await updateCart(productId)  }  const addProductToCart = addToCart.bind(null, productId);  return (    <form action={addProductToCart}>      <button type="submit">Add to Cart</button>    </form>  );}
```

---

## immutability

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/immutability

**Contents:**
- immutability
- Rule Details
- Common Violations
  - Invalid
  - Valid
- Troubleshooting
  - I need to add items to an array
  - I need to update nested objects

Validates against mutating props, state, and other values that are immutable.

A component’s props and state are immutable snapshots. Never mutate them directly. Instead, pass new props down, and use the setter function from useState.

Mutating arrays with methods like push() won’t trigger re-renders:

Create a new array instead:

Mutating nested properties doesn’t trigger re-renders:

Spread at each level that needs updating:

**Examples:**

Example 1 (jsx):
```jsx
// ❌ Array push mutationfunction Component() {  const [items, setItems] = useState([1, 2, 3]);  const addItem = () => {    items.push(4); // Mutating!    setItems(items); // Same reference, no re-render  };}// ❌ Object property assignmentfunction Component() {  const [user, setUser] = useState({name: 'Alice'});  const updateName = () => {    user.name = 'Bob'; // Mutating!    setUser(user); // Same reference  };}// ❌ Sort without spreadingfunction Component() {  const [items, setItems] = useState([3, 1, 2]);  const sortItems = () => {    setItems(items.sort()); // sort mutates!  };}
```

Example 2 (jsx):
```jsx
// ✅ Create new arrayfunction Component() {  const [items, setItems] = useState([1, 2, 3]);  const addItem = () => {    setItems([...items, 4]); // New array  };}// ✅ Create new objectfunction Component() {  const [user, setUser] = useState({name: 'Alice'});  const updateName = () => {    setUser({...user, name: 'Bob'}); // New object  };}
```

Example 3 (jsx):
```jsx
// ❌ Wrong: Mutating the arrayfunction TodoList() {  const [todos, setTodos] = useState([]);  const addTodo = (id, text) => {    todos.push({id, text});    setTodos(todos); // Same array reference!  };  return (    <ul>      {todos.map(todo => <li key={todo.id}>{todo.text}</li>)}    </ul>  );}
```

Example 4 (jsx):
```jsx
// ✅ Better: Create a new arrayfunction TodoList() {  const [todos, setTodos] = useState([]);  const addTodo = (id, text) => {    setTodos([...todos, {id, text}]);    // Or: setTodos(todos => [...todos, {id: Date.now(), text}])  };  return (    <ul>      {todos.map(todo => <li key={todo.id}>{todo.text}</li>)}    </ul>  );}
```

---

## incompatible-library

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/incompatible-library

**Contents:**
- incompatible-library
  - Note
- Rule Details
      - Deep Dive
    - Designing APIs that follow the Rules of React
  - Invalid
  - Pitfall
    - MobX
  - Valid

Validates against usage of libraries which are incompatible with memoization (manual or automatic).

These libraries were designed before React’s memoization rules were fully documented. They made the correct choices at the time to optimize for ergonomic ways to keep components just the right amount of reactive as app state changes. While these legacy patterns worked, we have since discovered that it’s incompatible with React’s programming model. We will continue working with library authors to migrate these libraries to use patterns that follow the Rules of React.

Some libraries use patterns that aren’t supported by React. When the linter detects usages of these APIs from a known list, it flags them under this rule. This means that React Compiler can automatically skip over components that use these incompatible APIs, in order to avoid breaking your app.

React Compiler automatically memoizes values following the Rules of React. If something breaks with manual useMemo, it will also break the compiler’s automatic optimization. This rule helps identify these problematic patterns.

One question to think about when designing a library API or hook is whether calling the API can be safely memoized with useMemo. If it can’t, then both manual and React Compiler memoizations will break your user’s code.

For example, one such incompatible pattern is “interior mutability”. Interior mutability is when an object or function keeps its own hidden state that changes over time, even though the reference to it stays the same. Think of it like a box that looks the same on the outside but secretly rearranges its contents. React can’t tell anything changed because it only checks if you gave it a different box, not what’s inside. This breaks memoization, since React relies on the outer object (or function) changing if part of its value has changed.

As a rule of thumb, when designing React APIs, think about whether useMemo would break it:

Instead, design APIs that return immutable state and use explicit update functions:

Examples of incorrect code for this rule:

MobX patterns like observer also break memoization assumptions, but the linter does not yet detect them. If you rely on MobX and find that your app doesn’t work with React Compiler, you may need to use the "use no memo" directive.

Examples of correct code for this rule:

Some other libraries do not yet have alternative APIs that are compatible with React’s memoization model. If the linter doesn’t automatically skip over your components or hooks that call these APIs, please file an issue so we can add it to the linter.

**Examples:**

Example 1 (jsx):
```jsx
// Example of how memoization breaks with these librariesfunction Form() {  const { watch } = useForm();  // ❌ This value will never update, even when 'name' field changes  const name = useMemo(() => watch('name'), [watch]);  return <div>Name: {name}</div>; // UI appears "frozen"}
```

Example 2 (javascript):
```javascript
function Component() {  const { someFunction } = useLibrary();  // it should always be safe to memoize functions like this  const result = useMemo(() => someFunction(), [someFunction]);}
```

Example 3 (jsx):
```jsx
// ✅ Good: Return immutable state that changes reference when updatedfunction Component() {  const { field, updateField } = useLibrary();  // this is always safe to memo  const greeting = useMemo(() => `Hello, ${field.name}!`, [field.name]);  return (    <div>      <input        value={field.name}        onChange={(e) => updateField('name', e.target.value)}      />      <p>{greeting}</p>    </div>  );}
```

Example 4 (javascript):
```javascript
// ❌ react-hook-form `watch`function Component() {  const {watch} = useForm();  const value = watch('field'); // Interior mutability  return <div>{value}</div>;}// ❌ TanStack Table `useReactTable`function Component({data}) {  const table = useReactTable({    data,    columns,    getCoreRowModel: getCoreRowModel(),  });  // table instance uses interior mutability  return <Table table={table} />;}
```

---

## <input>

**URL:** https://react.dev/reference/react-dom/components/input

**Contents:**
- <input>
- Reference
  - <input>
    - Props
    - Caveats
- Usage
  - Displaying inputs of different types
  - Providing a label for an input
  - Providing an initial value for an input
  - Reading the input values when submitting a form

The built-in browser <input> component lets you render different kinds of form inputs.

To display an input, render the built-in browser <input> component.

See more examples below.

<input> supports all common element props.

You can make an input controlled by passing one of these props:

When you pass either of them, you must also pass an onChange handler that updates the passed value.

These <input> props are only relevant for uncontrolled inputs:

These <input> props are relevant both for uncontrolled and controlled inputs:

To display an input, render an <input> component. By default, it will be a text input. You can pass type="checkbox" for a checkbox, type="radio" for a radio button, or one of the other input types.

Typically, you will place every <input> inside a <label> tag. This tells the browser that this label is associated with that input. When the user clicks the label, the browser will automatically focus the input. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the associated input.

If you can’t nest <input> into a <label>, associate them by passing the same ID to <input id> and <label htmlFor>. To avoid conflicts between multiple instances of one component, generate such an ID with useId.

You can optionally specify the initial value for any input. Pass it as the defaultValue string for text inputs. Checkboxes and radio buttons should specify the initial value with the defaultChecked boolean instead.

Add a <form> around your inputs with a <button type="submit"> inside. It will call your <form onSubmit> event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling e.preventDefault(). Read the form data with new FormData(e.target).

Give a name to every <input>, for example <input name="firstName" defaultValue="Taylor" />. The name you specified will be used as a key in the form data, for example { firstName: "Taylor" }.

By default, a <button> inside a <form> without a type attribute will submit it. This can be surprising! If you have your own custom Button React component, consider using <button type="button"> instead of <button> (with no type). Then, to be explicit, use <button type="submit"> for buttons that are supposed to submit the form.

An input like <input /> is uncontrolled. Even if you pass an initial value like <input defaultValue="Initial text" />, your JSX only specifies the initial value. It does not control what the value should be right now.

To render a controlled input, pass the value prop to it (or checked for checkboxes and radios). React will force the input to always have the value you passed. Usually, you would do this by declaring a state variable:

A controlled input makes sense if you needed state anyway—for example, to re-render your UI on every edit:

It’s also useful if you want to offer multiple ways to adjust the input state (for example, by clicking a button):

The value you pass to controlled components should not be undefined or null. If you need the initial value to be empty (such as with the firstName field below), initialize your state variable to an empty string ('').

If you pass value without onChange, it will be impossible to type into the input. When you control an input by passing some value to it, you force it to always have the value you passed. So if you pass a state variable as a value but forget to update that state variable synchronously during the onChange event handler, React will revert the input after every keystroke back to the value that you specified.

When you use a controlled input, you set the state on every keystroke. If the component containing your state re-renders a large tree, this can get slow. There’s a few ways you can optimize re-rendering performance.

For example, suppose you start with a form that re-renders all page content on every keystroke:

Since <PageContent /> doesn’t rely on the input state, you can move the input state into its own component:

This significantly improves performance because now only SignupForm re-renders on every keystroke.

If there is no way to avoid re-rendering (for example, if PageContent depends on the search input’s value), useDeferredValue lets you keep the controlled input responsive even in the middle of a large re-render.

If you render an input with value but no onChange, you will see an error in the console:

As the error message suggests, if you only wanted to specify the initial value, pass defaultValue instead:

If you want to control this input with a state variable, specify an onChange handler:

If the value is intentionally read-only, add a readOnly prop to suppress the error:

If you render a checkbox with checked but no onChange, you will see an error in the console:

As the error message suggests, if you only wanted to specify the initial value, pass defaultChecked instead:

If you want to control this checkbox with a state variable, specify an onChange handler:

You need to read e.target.checked rather than e.target.value for checkboxes.

If the checkbox is intentionally read-only, add a readOnly prop to suppress the error:

If you control an input, you must update its state variable to the input’s value from the DOM during onChange.

You can’t update it to something other than e.target.value (or e.target.checked for checkboxes):

You also can’t update it asynchronously:

To fix your code, update it synchronously to e.target.value:

If this doesn’t fix the problem, it’s possible that the input gets removed and re-added from the DOM on every keystroke. This can happen if you’re accidentally resetting state on every re-render, for example if the input or one of its parents always receives a different key attribute, or if you nest component function definitions (which is not supported and causes the “inner” component to always be considered a different tree).

If you provide a value to the component, it must remain a string throughout its lifetime.

You cannot pass value={undefined} first and later pass value="some string" because React won’t know whether you want the component to be uncontrolled or controlled. A controlled component should always receive a string value, not null or undefined.

If your value is coming from an API or a state variable, it might be initialized to null or undefined. In that case, either set it to an empty string ('') initially, or pass value={someValue ?? ''} to ensure value is a string.

Similarly, if you pass checked to a checkbox, ensure it’s always a boolean.

**Examples:**

Example 1 (jsx):
```jsx
<input name="myInput" />
```

Example 2 (jsx):
```jsx
function Form() {  const [firstName, setFirstName] = useState(''); // Declare a state variable...  // ...  return (    <input      value={firstName} // ...force the input's value to match the state variable...      onChange={e => setFirstName(e.target.value)} // ... and update the state variable on any edits!    />  );}
```

Example 3 (jsx):
```jsx
function Form() {  const [firstName, setFirstName] = useState('');  return (    <>      <label>        First name:        <input value={firstName} onChange={e => setFirstName(e.target.value)} />      </label>      {firstName !== '' && <p>Your name is {firstName}.</p>}      ...
```

Example 4 (jsx):
```jsx
function Form() {  // ...  const [age, setAge] = useState('');  const ageAsNumber = Number(age);  return (    <>      <label>        Age:        <input          value={age}          onChange={e => setAge(e.target.value)}          type="number"        />        <button onClick={() => setAge(ageAsNumber + 10)}>          Add 10 years        </button>
```

---

## <link>

**URL:** https://react.dev/reference/react-dom/components/link

**Contents:**
- <link>
- Reference
  - <link>
    - Props
    - Special rendering behavior
    - Special behavior for stylesheets
- Usage
  - Linking to related resources
  - Linking to a stylesheet
  - Note

The built-in browser <link> component lets you use external resources such as stylesheets or annotate the document with link metadata.

To link to external resources such as stylesheets, fonts, and icons, or to annotate the document with link metadata, render the built-in browser <link> component. You can render <link> from any component and React will in most cases place the corresponding DOM element in the document head.

See more examples below.

<link> supports all common element props.

These props apply when rel="stylesheet":

These props apply when rel="stylesheet" but disable React’s special treatment of stylesheets:

These props apply when rel="preload" or rel="modulepreload":

These props apply when rel="icon" or rel="apple-touch-icon":

These props apply in all cases:

Props that are not recommended for use with React:

React will always place the DOM element corresponding to the <link> component within the document’s <head>, regardless of where in the React tree it is rendered. The <head> is the only valid place for <link> to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render <link> components itself.

There are a few exceptions to this:

In addition, if the <link> is to a stylesheet (namely, it has rel="stylesheet" in its props), React treats it specially in the following ways:

There are two exception to this special behavior:

This special treatment comes with two caveats:

You can annotate the document with links to related resources such as an icon, canonical URL, or pingback. React will place this metadata within the document <head> regardless of where in the React tree it is rendered.

If a component depends on a certain stylesheet in order to be displayed correctly, you can render a link to that stylesheet within the component. Your component will suspend while the stylesheet is loading. You must supply the precedence prop, which tells React where to place this stylesheet relative to others — stylesheets with higher precedence can override those with lower precedence.

When you want to use a stylesheet, it can be beneficial to call the preinit function. Calling this function may allow the browser to start fetching the stylesheet earlier than if you just render a <link> component, for example by sending an HTTP Early Hints response.

Stylesheets can conflict with each other, and when they do, the browser goes with the one that comes later in the document. React lets you control the order of stylesheets with the precedence prop. In this example, three components render stylesheets, and the ones with the same precedence are grouped together in the <head>.

Note the precedence values themselves are arbitrary and their naming is up to you. React will infer that precedence values it discovers first are “lower” and precedence values it discovers later are “higher”.

If you render the same stylesheet from multiple components, React will place only a single <link> in the document head.

You can use the <link> component with the itemProp prop to annotate specific items within the document with links to related resources. In this case, React will not place these annotations within the document <head> but will place them like any other React component.

**Examples:**

Example 1 (jsx):
```jsx
<link rel="icon" href="favicon.ico" />
```

Example 2 (jsx):
```jsx
<link rel="icon" href="favicon.ico" />
```

Example 3 (jsx):
```jsx
<section itemScope>  <h3>Annotating specific items</h3>  <link itemProp="author" href="http://example.com/" />  <p>...</p></section>
```

---

## memo

**URL:** https://react.dev/reference/react/memo

**Contents:**
- memo
  - Note
- Reference
  - memo(Component, arePropsEqual?)
    - Parameters
    - Returns
- Usage
  - Skipping re-rendering when props are unchanged
  - Note
      - Deep Dive

memo lets you skip re-rendering a component when its props are unchanged.

React Compiler automatically applies the equivalent of memo to all components, reducing the need for manual memoization. You can use the compiler to handle component memoization automatically.

Wrap a component in memo to get a memoized version of that component. This memoized version of your component will usually not be re-rendered when its parent component is re-rendered as long as its props have not changed. But React may still re-render it: memoization is a performance optimization, not a guarantee.

See more examples below.

Component: The component that you want to memoize. The memo does not modify this component, but returns a new, memoized component instead. Any valid React component, including functions and forwardRef components, is accepted.

optional arePropsEqual: A function that accepts two arguments: the component’s previous props, and its new props. It should return true if the old and new props are equal: that is, if the component will render the same output and behave in the same way with the new props as with the old. Otherwise it should return false. Usually, you will not specify this function. By default, React will compare each prop with Object.is.

memo returns a new React component. It behaves the same as the component provided to memo except that React will not always re-render it when its parent is being re-rendered unless its props have changed.

React normally re-renders a component whenever its parent re-renders. With memo, you can create a component that React will not re-render when its parent re-renders so long as its new props are the same as the old props. Such a component is said to be memoized.

To memoize a component, wrap it in memo and use the value that it returns in place of your original component:

A React component should always have pure rendering logic. This means that it must return the same output if its props, state, and context haven’t changed. By using memo, you are telling React that your component complies with this requirement, so React doesn’t need to re-render as long as its props haven’t changed. Even with memo, your component will re-render if its own state changes or if a context that it’s using changes.

In this example, notice that the Greeting component re-renders whenever name is changed (because that’s one of its props), but not when address is changed (because it’s not passed to Greeting as a prop):

You should only rely on memo as a performance optimization. If your code doesn’t work without it, find the underlying problem and fix it first. Then you may add memo to improve performance.

If your app is like this site, and most interactions are coarse (like replacing a page or an entire section), memoization is usually unnecessary. On the other hand, if your app is more like a drawing editor, and most interactions are granular (like moving shapes), then you might find memoization very helpful.

Optimizing with memo is only valuable when your component re-renders often with the same exact props, and its re-rendering logic is expensive. If there is no perceptible lag when your component re-renders, memo is unnecessary. Keep in mind that memo is completely useless if the props passed to your component are always different, such as if you pass an object or a plain function defined during rendering. This is why you will often need useMemo and useCallback together with memo.

There is no benefit to wrapping a component in memo in other cases. There is no significant harm to doing that either, so some teams choose to not think about individual cases, and memoize as much as possible. The downside of this approach is that code becomes less readable. Also, not all memoization is effective: a single value that’s “always new” is enough to break memoization for an entire component.

In practice, you can make a lot of memoization unnecessary by following a few principles:

If a specific interaction still feels laggy, use the React Developer Tools profiler to see which components would benefit the most from memoization, and add memoization where needed. These principles make your components easier to debug and understand, so it’s good to follow them in any case. In the long term, we’re researching doing granular memoization automatically to solve this once and for all.

Even when a component is memoized, it will still re-render when its own state changes. Memoization only has to do with props that are passed to the component from its parent.

If you set a state variable to its current value, React will skip re-rendering your component even without memo. You may still see your component function being called an extra time, but the result will be discarded.

Even when a component is memoized, it will still re-render when a context that it’s using changes. Memoization only has to do with props that are passed to the component from its parent.

To make your component re-render only when a part of some context changes, split your component in two. Read what you need from the context in the outer component, and pass it down to a memoized child as a prop.

When you use memo, your component re-renders whenever any prop is not shallowly equal to what it was previously. This means that React compares every prop in your component with its previous value using the Object.is comparison. Note that Object.is(3, 3) is true, but Object.is({}, {}) is false.

To get the most out of memo, minimize the times that the props change. For example, if the prop is an object, prevent the parent component from re-creating that object every time by using useMemo:

A better way to minimize props changes is to make sure the component accepts the minimum necessary information in its props. For example, it could accept individual values instead of a whole object:

Even individual values can sometimes be projected to ones that change less frequently. For example, here a component accepts a boolean indicating the presence of a value rather than the value itself:

When you need to pass a function to memoized component, either declare it outside your component so that it never changes, or useCallback to cache its definition between re-renders.

In rare cases it may be infeasible to minimize the props changes of a memoized component. In that case, you can provide a custom comparison function, which React will use to compare the old and new props instead of using shallow equality. This function is passed as a second argument to memo. It should return true only if the new props would result in the same output as the old props; otherwise it should return false.

If you do this, use the Performance panel in your browser developer tools to make sure that your comparison function is actually faster than re-rendering the component. You might be surprised.

When you do performance measurements, make sure that React is running in the production mode.

If you provide a custom arePropsEqual implementation, you must compare every prop, including functions. Functions often close over the props and state of parent components. If you return true when oldProps.onClick !== newProps.onClick, your component will keep “seeing” the props and state from a previous render inside its onClick handler, leading to very confusing bugs.

Avoid doing deep equality checks inside arePropsEqual unless you are 100% sure that the data structure you’re working with has a known limited depth. Deep equality checks can become incredibly slow and can freeze your app for many seconds if someone changes the data structure later.

When you enable React Compiler, you typically don’t need React.memo anymore. The compiler automatically optimizes component re-rendering for you.

Without React Compiler, you need React.memo to prevent unnecessary re-renders:

With React Compiler enabled, the same optimization happens automatically:

Here’s the key part of what the React Compiler generates:

Notice the highlighted lines: The compiler wraps <ExpensiveChild name="John" /> in a cache check. Since the name prop is always "John", this JSX is created once and reused on every parent re-render. This is exactly what React.memo does - it prevents the child from re-rendering when its props haven’t changed.

The React Compiler automatically:

This means you can safely remove React.memo from your components when using React Compiler. The compiler provides the same optimization automatically, making your code cleaner and easier to maintain.

The compiler’s optimization is actually more comprehensive than React.memo. It also memoizes intermediate values and expensive computations within your components, similar to combining React.memo with useMemo throughout your component tree.

React compares old and new props by shallow equality: that is, it considers whether each new prop is reference-equal to the old prop. If you create a new object or array each time the parent is re-rendered, even if the individual elements are each the same, React will still consider it to be changed. Similarly, if you create a new function when rendering the parent component, React will consider it to have changed even if the function has the same definition. To avoid this, simplify props or memoize props in the parent component.

**Examples:**

Example 1 (javascript):
```javascript
const MemoizedComponent = memo(SomeComponent, arePropsEqual?)
```

Example 2 (javascript):
```javascript
import { memo } from 'react';const SomeComponent = memo(function SomeComponent(props) {  // ...});
```

Example 3 (javascript):
```javascript
const Greeting = memo(function Greeting({ name }) {  return <h1>Hello, {name}!</h1>;});export default Greeting;
```

Example 4 (jsx):
```jsx
function Page() {  const [name, setName] = useState('Taylor');  const [age, setAge] = useState(42);  const person = useMemo(    () => ({ name, age }),    [name, age]  );  return <Profile person={person} />;}const Profile = memo(function Profile({ person }) {  // ...});
```

---

## <meta>

**URL:** https://react.dev/reference/react-dom/components/meta

**Contents:**
- <meta>
- Reference
  - <meta>
    - Props
    - Special rendering behavior
- Usage
  - Annotating the document with metadata
  - Annotating specific items within the document with metadata

The built-in browser <meta> component lets you add metadata to the document.

To add document metadata, render the built-in browser <meta> component. You can render <meta> from any component and React will always place the corresponding DOM element in the document head.

See more examples below.

<meta> supports all common element props.

It should have exactly one of the following props: name, httpEquiv, charset, itemProp. The <meta> component does something different depending on which of these props is specified.

React will always place the DOM element corresponding to the <meta> component within the document’s <head>, regardless of where in the React tree it is rendered. The <head> is the only valid place for <meta> to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render <meta> components itself.

There is one exception to this: if <meta> has an itemProp prop, there is no special behavior, because in this case it doesn’t represent metadata about the document but rather metadata about a specific part of the page.

You can annotate the document with metadata such as keywords, a summary, or the author’s name. React will place this metadata within the document <head> regardless of where in the React tree it is rendered.

You can render the <meta> component from any component. React will put a <meta> DOM node in the document <head>.

You can use the <meta> component with the itemProp prop to annotate specific items within the document with metadata. In this case, React will not place these annotations within the document <head> but will place them like any other React component.

**Examples:**

Example 1 (jsx):
```jsx
<meta name="keywords" content="React, JavaScript, semantic markup, html" />
```

Example 2 (jsx):
```jsx
<meta name="keywords" content="React, JavaScript, semantic markup, html" />
```

Example 3 (jsx):
```jsx
<meta name="author" content="John Smith" /><meta name="keywords" content="React, JavaScript, semantic markup, html" /><meta name="description" content="API reference for the <meta> component in React DOM" />
```

Example 4 (jsx):
```jsx
<section itemScope>  <h3>Annotating specific items</h3>  <meta itemProp="description" content="API reference for using <meta> with itemProp" />  <p>...</p></section>
```

---

## <option>

**URL:** https://react.dev/reference/react-dom/components/option

**Contents:**
- <option>
- Reference
  - <option>
    - Props
    - Caveats
- Usage
  - Displaying a select box with options

The built-in browser <option> component lets you render an option inside a <select> box.

The built-in browser <option> component lets you render an option inside a <select> box.

See more examples below.

<option> supports all common element props.

Additionally, <option> supports these props:

Render a <select> with a list of <option> components inside to display a select box. Give each <option> a value representing the data to be submitted with the form.

Read more about displaying a <select> with a list of <option> components.

**Examples:**

Example 1 (jsx):
```jsx
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

Example 2 (jsx):
```jsx
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

---

## <progress>

**URL:** https://react.dev/reference/react-dom/components/progress

**Contents:**
- <progress>
- Reference
  - <progress>
    - Props
- Usage
  - Controlling a progress indicator

The built-in browser <progress> component lets you render a progress indicator.

To display a progress indicator, render the built-in browser <progress> component.

See more examples below.

<progress> supports all common element props.

Additionally, <progress> supports these props:

To display a progress indicator, render a <progress> component. You can pass a number value between 0 and the max value you specify. If you don’t pass a max value, it will assumed to be 1 by default.

If the operation is not ongoing, pass value={null} to put the progress indicator into an indeterminate state.

**Examples:**

Example 1 (jsx):
```jsx
<progress value={0.5} />
```

Example 2 (jsx):
```jsx
<progress value={0.5} />
```

---

## PureComponent

**URL:** https://react.dev/reference/react/PureComponent

**Contents:**
- PureComponent
  - Pitfall
- Reference
  - PureComponent
- Usage
  - Skipping unnecessary re-renders for class components
  - Pitfall
- Alternatives
  - Migrating from a PureComponent class component to a function
  - Note

We recommend defining components as functions instead of classes. See how to migrate.

PureComponent is similar to Component but it skips re-renders for same props and state. Class components are still supported by React, but we don’t recommend using them in new code.

To skip re-rendering a class component for same props and state, extend PureComponent instead of Component:

PureComponent is a subclass of Component and supports all the Component APIs. Extending PureComponent is equivalent to defining a custom shouldComponentUpdate method that shallowly compares props and state.

See more examples below.

React normally re-renders a component whenever its parent re-renders. As an optimization, you can create a component that React will not re-render when its parent re-renders so long as its new props and state are the same as the old props and state. Class components can opt into this behavior by extending PureComponent:

A React component should always have pure rendering logic. This means that it must return the same output if its props, state, and context haven’t changed. By using PureComponent, you are telling React that your component complies with this requirement, so React doesn’t need to re-render as long as its props and state haven’t changed. However, your component will still re-render if a context that it’s using changes.

In this example, notice that the Greeting component re-renders whenever name is changed (because that’s one of its props), but not when address is changed (because it’s not passed to Greeting as a prop):

We recommend defining components as functions instead of classes. See how to migrate.

We recommend using function components instead of class components in new code. If you have some existing class components using PureComponent, here is how you can convert them. This is the original code:

When you convert this component from a class to a function, wrap it in memo:

Unlike PureComponent, memo does not compare the new and the old state. In function components, calling the set function with the same state already prevents re-renders by default, even without memo.

**Examples:**

Example 1 (jsx):
```jsx
class Greeting extends PureComponent {  render() {    return <h1>Hello, {this.props.name}!</h1>;  }}
```

Example 2 (jsx):
```jsx
import { PureComponent } from 'react';class Greeting extends PureComponent {  render() {    return <h1>Hello, {this.props.name}!</h1>;  }}
```

Example 3 (jsx):
```jsx
class Greeting extends PureComponent {  render() {    return <h1>Hello, {this.props.name}!</h1>;  }}
```

---

## purity

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/purity

**Contents:**
- purity
- Rule Details
- Common Violations
  - Invalid
  - Valid
- Troubleshooting
  - I need to show the current time

Validates that components/hooks are pure by checking that they do not call known-impure functions.

React components must be pure functions - given the same props, they should always return the same JSX. When components use functions like Math.random() or Date.now() during render, they produce different output each time, breaking React’s assumptions and causing bugs like hydration mismatches, incorrect memoization, and unpredictable behavior.

In general, any API that returns a different value for the same inputs violates this rule. Usual examples include:

Examples of incorrect code for this rule:

Examples of correct code for this rule:

Calling Date.now() during render makes your component impure:

Instead, move the impure function outside of render:

**Examples:**

Example 1 (jsx):
```jsx
// ❌ Math.random() in renderfunction Component() {  const id = Math.random(); // Different every render  return <div key={id}>Content</div>;}// ❌ Date.now() for valuesfunction Component() {  const timestamp = Date.now(); // Changes every render  return <div>Created at: {timestamp}</div>;}
```

Example 2 (jsx):
```jsx
// ✅ Stable IDs from initial statefunction Component() {  const [id] = useState(() => crypto.randomUUID());  return <div key={id}>Content</div>;}
```

Example 3 (typescript):
```typescript
// ❌ Wrong: Time changes every renderfunction Clock() {  return <div>Current time: {Date.now()}</div>;}
```

Example 4 (jsx):
```jsx
function Clock() {  const [time, setTime] = useState(() => Date.now());  useEffect(() => {    const interval = setInterval(() => {      setTime(Date.now());    }, 1000);    return () => clearInterval(interval);  }, []);  return <div>Current time: {time}</div>;}
```

---

## React calls Components and Hooks

**URL:** https://react.dev/reference/rules/react-calls-components-and-hooks

**Contents:**
- React calls Components and Hooks
- Never call component functions directly
- Never pass around Hooks as regular values
  - Don’t dynamically mutate a Hook
  - Don’t dynamically use Hooks

React is responsible for rendering components and Hooks when necessary to optimize the user experience. It is declarative: you tell React what to render in your component’s logic, and React will figure out how best to display it to your user.

Components should only be used in JSX. Don’t call them as regular functions. React should call it.

React must decide when your component function is called during rendering. In React, you do this using JSX.

If a component contains Hooks, it’s easy to violate the Rules of Hooks when components are called directly in a loop or conditionally.

Letting React orchestrate rendering also allows a number of benefits:

Hooks should only be called inside of components or Hooks. Never pass it around as a regular value.

Hooks allow you to augment a component with React features. They should always be called as a function, and never passed around as a regular value. This enables local reasoning, or the ability for developers to understand everything a component can do by looking at that component in isolation.

Breaking this rule will cause React to not automatically optimize your component.

Hooks should be as “static” as possible. This means you shouldn’t dynamically mutate them. For example, this means you shouldn’t write higher order Hooks:

Hooks should be immutable and not be mutated. Instead of mutating a Hook dynamically, create a static version of the Hook with the desired functionality.

Hooks should also not be dynamically used: for example, instead of doing dependency injection in a component by passing a Hook as a value:

You should always inline the call of the Hook into that component and handle any logic in there.

This way, <Button /> is much easier to understand and debug. When Hooks are used in dynamic ways, it increases the complexity of your app greatly and inhibits local reasoning, making your team less productive in the long term. It also makes it easier to accidentally break the Rules of Hooks that Hooks should not be called conditionally. If you find yourself needing to mock components for tests, it’s better to mock the server instead to respond with canned data. If possible, it’s also usually more effective to test your app with end-to-end tests.

**Examples:**

Example 1 (jsx):
```jsx
function BlogPost() {  return <Layout><Article /></Layout>; // ✅ Good: Only use components in JSX}
```

Example 2 (javascript):
```javascript
function BlogPost() {  return <Layout>{Article()}</Layout>; // 🔴 Bad: Never call them directly}
```

Example 3 (javascript):
```javascript
function ChatInput() {  const useDataWithLogging = withLogging(useData); // 🔴 Bad: don't write higher order Hooks  const data = useDataWithLogging();}
```

Example 4 (javascript):
```javascript
function ChatInput() {  const data = useDataWithLogging(); // ✅ Good: Create a new version of the Hook}function useDataWithLogging() {  // ... Create a new version of the Hook and inline the logic here}
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (typescript):
```typescript
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (javascript):
```javascript
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## rules-of-hooks

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks

**Contents:**
- rules-of-hooks
- Rule Details
- Common Violations
  - Note
  - use hook
  - Invalid
  - Valid
- Troubleshooting
  - I want to fetch data based on some condition
  - Note

Validates that components and hooks follow the Rules of Hooks.

React relies on the order in which hooks are called to correctly preserve state between renders. Each time your component renders, React expects the exact same hooks to be called in the exact same order. When hooks are called conditionally or in loops, React loses track of which state corresponds to which hook call, leading to bugs like state mismatches and “Rendered fewer/more hooks than expected” errors.

These patterns violate the Rules of Hooks:

The use hook is different from other React hooks. You can call it conditionally and in loops:

However, use still has restrictions:

Learn more: use API Reference

Examples of incorrect code for this rule:

Examples of correct code for this rule:

You’re trying to conditionally call useEffect:

Call the hook unconditionally, check condition inside:

There are better ways to fetch data rather than in a useEffect. Consider using TanStack Query, useSWR, or React Router 6.4+ for data fetching. These solutions handle deduplicating requests, caching responses, and avoiding network waterfalls.

Learn more: Fetching Data

You’re trying to conditionally initialize state:

Always call useState, conditionally set the initial value:

You can configure custom effect hooks using shared ESLint settings (available in eslint-plugin-react-hooks 6.1.1 and later):

This shared configuration is used by both rules-of-hooks and exhaustive-deps rules, ensuring consistent behavior across all hook-related linting.

**Examples:**

Example 1 (javascript):
```javascript
// ✅ `use` can be conditionalif (shouldFetch) {  const data = use(fetchPromise);}// ✅ `use` can be in loopsfor (const promise of promises) {  results.push(use(promise));}
```

Example 2 (jsx):
```jsx
// ❌ Hook in conditionif (isLoggedIn) {  const [user, setUser] = useState(null);}// ❌ Hook after early returnif (!data) return <Loading />;const [processed, setProcessed] = useState(data);// ❌ Hook in callback<button onClick={() => {  const [clicked, setClicked] = useState(false);}}/>// ❌ `use` in try/catchtry {  const data = use(promise);} catch (e) {  // error handling}// ❌ Hook at module levelconst globalState = useState(0); // Outside component
```

Example 3 (javascript):
```javascript
function Component({ isSpecial, shouldFetch, fetchPromise }) {  // ✅ Hooks at top level  const [count, setCount] = useState(0);  const [name, setName] = useState('');  if (!isSpecial) {    return null;  }  if (shouldFetch) {    // ✅ `use` can be conditional    const data = use(fetchPromise);    return <div>{data}</div>;  }  return <div>{name}: {count}</div>;}
```

Example 4 (jsx):
```jsx
// ❌ Conditional hookif (isLoggedIn) {  useEffect(() => {    fetchUserData();  }, []);}
```

---

## <script>

**URL:** https://react.dev/reference/react-dom/components/script

**Contents:**
- <script>
- Reference
  - <script>
    - Props
    - Special rendering behavior
- Usage
  - Rendering an external script
  - Note
  - Rendering an inline script

The built-in browser <script> component lets you add a script to your document.

To add inline or external scripts to your document, render the built-in browser <script> component. You can render <script> from any component and React will in certain cases place the corresponding DOM element in the document head and de-duplicate identical scripts.

See more examples below.

<script> supports all common element props.

It should have either children or a src prop.

Other supported props:

Props that disable React’s special treatment of scripts:

Props that are not recommended for use with React:

React can move <script> components to the document’s <head> and de-duplicate identical scripts.

To opt into this behavior, provide the src and async={true} props. React will de-duplicate scripts if they have the same src. The async prop must be true to allow scripts to be safely moved.

This special treatment comes with two caveats:

If a component depends on certain scripts in order to be displayed correctly, you can render a <script> within the component. However, the component might be committed before the script has finished loading. You can start depending on the script content once the load event is fired e.g. by using the onLoad prop.

React will de-duplicate scripts that have the same src, inserting only one of them into the DOM even if multiple components render it.

When you want to use a script, it can be beneficial to call the preinit function. Calling this function may allow the browser to start fetching the script earlier than if you just render a <script> component, for example by sending an HTTP Early Hints response.

To include an inline script, render the <script> component with the script source code as its children. Inline scripts are not de-duplicated or moved to the document <head>.

**Examples:**

Example 1 (vue):
```vue
<script> alert("hi!") </script>
```

Example 2 (jsx):
```jsx
<script> alert("hi!") </script><script src="script.js" />
```

---

## <select>

**URL:** https://react.dev/reference/react-dom/components/select

**Contents:**
- <select>
- Reference
  - <select>
    - Props
    - Caveats
- Usage
  - Displaying a select box with options
  - Providing a label for a select box
  - Providing an initially selected option
  - Pitfall

The built-in browser <select> component lets you render a select box with options.

To display a select box, render the built-in browser <select> component.

See more examples below.

<select> supports all common element props.

You can make a select box controlled by passing a value prop:

When you pass value, you must also pass an onChange handler that updates the passed value.

If your <select> is uncontrolled, you may pass the defaultValue prop instead:

These <select> props are relevant both for uncontrolled and controlled select boxes:

Render a <select> with a list of <option> components inside to display a select box. Give each <option> a value representing the data to be submitted with the form.

Typically, you will place every <select> inside a <label> tag. This tells the browser that this label is associated with that select box. When the user clicks the label, the browser will automatically focus the select box. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the select box.

If you can’t nest <select> into a <label>, associate them by passing the same ID to <select id> and <label htmlFor>. To avoid conflicts between multiple instances of one component, generate such an ID with useId.

By default, the browser will select the first <option> in the list. To select a different option by default, pass that <option>’s value as the defaultValue to the <select> element.

Unlike in HTML, passing a selected attribute to an individual <option> is not supported.

Pass multiple={true} to the <select> to let the user select multiple options. In that case, if you also specify defaultValue to choose the initially selected options, it must be an array.

Add a <form> around your select box with a <button type="submit"> inside. It will call your <form onSubmit> event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling e.preventDefault(). Read the form data with new FormData(e.target).

Give a name to your <select>, for example <select name="selectedFruit" />. The name you specified will be used as a key in the form data, for example { selectedFruit: "orange" }.

If you use <select multiple={true}>, the FormData you’ll read from the form will include each selected value as a separate name-value pair. Look closely at the console logs in the example above.

By default, any <button> inside a <form> will submit it. This can be surprising! If you have your own custom Button React component, consider returning <button type="button"> instead of <button>. Then, to be explicit, use <button type="submit"> for buttons that are supposed to submit the form.

A select box like <select /> is uncontrolled. Even if you pass an initially selected value like <select defaultValue="orange" />, your JSX only specifies the initial value, not the value right now.

To render a controlled select box, pass the value prop to it. React will force the select box to always have the value you passed. Typically, you will control a select box by declaring a state variable:

This is useful if you want to re-render some part of the UI in response to every selection.

If you pass value without onChange, it will be impossible to select an option. When you control a select box by passing some value to it, you force it to always have the value you passed. So if you pass a state variable as a value but forget to update that state variable synchronously during the onChange event handler, React will revert the select box after every keystroke back to the value that you specified.

Unlike in HTML, passing a selected attribute to an individual <option> is not supported.

**Examples:**

Example 1 (jsx):
```jsx
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

Example 2 (jsx):
```jsx
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

Example 3 (jsx):
```jsx
function FruitPicker() {  const [selectedFruit, setSelectedFruit] = useState('orange'); // Declare a state variable...  // ...  return (    <select      value={selectedFruit} // ...force the select's value to match the state variable...      onChange={e => setSelectedFruit(e.target.value)} // ... and update the state variable on any change!    >      <option value="apple">Apple</option>      <option value="banana">Banana</option>      <option value="orange">Orange</option>    </select>  );}
```

---

## Server Components

**URL:** https://react.dev/reference/rsc/server-components

**Contents:**
- Server Components
  - Note
    - How do I build support for Server Components?
  - Server Components without a Server
  - Note
  - Server Components with a Server
  - Adding interactivity to Server Components
  - Note
    - There is no directive for Server Components.
  - Async components with Server Components

Server Components are a new type of Component that renders ahead of time, before bundling, in an environment separate from your client app or SSR server.

This separate environment is the “server” in React Server Components. Server Components can run once at build time on your CI server, or they can be run for each request using a web server.

While React Server Components in React 19 are stable and will not break between minor versions, the underlying APIs used to implement a React Server Components bundler or framework do not follow semver and may break between minors in React 19.x.

To support React Server Components as a bundler or framework, we recommend pinning to a specific React version, or using the Canary release. We will continue working with bundlers and frameworks to stabilize the APIs used to implement React Server Components in the future.

Server components can run at build time to read from the filesystem or fetch static content, so a web server is not required. For example, you may want to read static data from a content management system.

Without Server Components, it’s common to fetch static data on the client with an Effect:

This pattern means users need to download and parse an additional 75K (gzipped) of libraries, and wait for a second request to fetch the data after the page loads, just to render static content that will not change for the lifetime of the page.

With Server Components, you can render these components once at build time:

The rendered output can then be server-side rendered (SSR) to HTML and uploaded to a CDN. When the app loads, the client will not see the original Page component, or the expensive libraries for rendering the markdown. The client will only see the rendered output:

This means the content is visible during first page load, and the bundle does not include the expensive libraries needed to render the static content.

You may notice that the Server Component above is an async function:

Async Components are a new feature of Server Components that allow you to await in render.

See Async components with Server Components below.

Server Components can also run on a web server during a request for a page, letting you access your data layer without having to build an API. They are rendered before your application is bundled, and can pass data and JSX as props to Client Components.

Without Server Components, it’s common to fetch dynamic data on the client in an Effect:

With Server Components, you can read the data and render it in the component:

The bundler then combines the data, rendered Server Components and dynamic Client Components into a bundle. Optionally, that bundle can then be server-side rendered (SSR) to create the initial HTML for the page. When the page loads, the browser does not see the original Note and Author components; only the rendered output is sent to the client:

Server Components can be made dynamic by re-fetching them from a server, where they can access the data and render again. This new application architecture combines the simple “request/response” mental model of server-centric Multi-Page Apps with the seamless interactivity of client-centric Single-Page Apps, giving you the best of both worlds.

Server Components are not sent to the browser, so they cannot use interactive APIs like useState. To add interactivity to Server Components, you can compose them with Client Component using the "use client" directive.

A common misunderstanding is that Server Components are denoted by "use server", but there is no directive for Server Components. The "use server" directive is used for Server Functions.

For more info, see the docs for Directives.

In the following example, the Notes Server Component imports an Expandable Client Component that uses state to toggle its expanded state:

This works by first rendering Notes as a Server Component, and then instructing the bundler to create a bundle for the Client Component Expandable. In the browser, the Client Components will see output of the Server Components passed as props:

Server Components introduce a new way to write Components using async/await. When you await in an async component, React will suspend and wait for the promise to resolve before resuming rendering. This works across server/client boundaries with streaming support for Suspense.

You can even create a promise on the server, and await it on the client:

The note content is important data for the page to render, so we await it on the server. The comments are below the fold and lower-priority, so we start the promise on the server, and wait for it on the client with the use API. This will Suspend on the client, without blocking the note content from rendering.

Since async components are not supported on the client, we await the promise with use.

**Examples:**

Example 1 (jsx):
```jsx
// bundle.jsimport marked from 'marked'; // 35.9K (11.2K gzipped)import sanitizeHtml from 'sanitize-html'; // 206K (63.3K gzipped)function Page({page}) {  const [content, setContent] = useState('');  // NOTE: loads *after* first page render.  useEffect(() => {    fetch(`/api/content/${page}`).then((data) => {      setContent(data.content);    });  }, [page]);  return <div>{sanitizeHtml(marked(content))}</div>;}
```

Example 2 (javascript):
```javascript
// api.jsapp.get(`/api/content/:page`, async (req, res) => {  const page = req.params.page;  const content = await file.readFile(`${page}.md`);  res.send({content});});
```

Example 3 (javascript):
```javascript
import marked from 'marked'; // Not included in bundleimport sanitizeHtml from 'sanitize-html'; // Not included in bundleasync function Page({page}) {  // NOTE: loads *during* render, when the app is built.  const content = await file.readFile(`${page}.md`);  return <div>{sanitizeHtml(marked(content))}</div>;}
```

Example 4 (typescript):
```typescript
<div><!-- html for markdown --></div>
```

---

## set-state-in-effect

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-effect

**Contents:**
- set-state-in-effect
- Rule Details
- Common Violations
  - Invalid
  - Valid

Validates against calling setState synchronously in an effect, which can lead to re-renders that degrade performance.

Setting state immediately inside an effect forces React to restart the entire render cycle. When you update state in an effect, React must re-render your component, apply changes to the DOM, and then run effects again. This creates an extra render pass that could have been avoided by transforming data directly during render or deriving state from props. Transform data at the top level of your component instead. This code will naturally re-run when props or state change without triggering additional render cycles.

Synchronous setState calls in effects trigger immediate re-renders before the browser can paint, causing performance issues and visual jank. React has to render twice: once to apply the state update, then again after effects run. This double rendering is wasteful when the same result could be achieved with a single render.

In many cases, you may also not need an effect at all. Please see You Might Not Need an Effect for more information.

This rule catches several patterns where synchronous setState is used unnecessarily:

Examples of incorrect code for this rule:

Examples of correct code for this rule:

When something can be calculated from the existing props or state, don’t put it in state. Instead, calculate it during rendering. This makes your code faster, simpler, and less error-prone. Learn more in You Might Not Need an Effect.

**Examples:**

Example 1 (jsx):
```jsx
// ❌ Synchronous setState in effectfunction Component({data}) {  const [items, setItems] = useState([]);  useEffect(() => {    setItems(data); // Extra render, use initial state instead  }, [data]);}// ❌ Setting loading state synchronouslyfunction Component() {  const [loading, setLoading] = useState(false);  useEffect(() => {    setLoading(true); // Synchronous, causes extra render    fetchData().then(() => setLoading(false));  }, []);}// ❌ Transforming data in effectfunction Component({rawData}) {  const [processed, setProcessed] = useState([]);  useEffect(() => {    setProcessed(rawData.map(transform)); // Should derive in render  }, [rawData]);}// ❌ Deriving state from propsfunction Component({selectedId, items}) {  const [selected, setSelected] = useState(null);  useEffect(() => {    setSelected(items.find(i => i.id === selectedId));  }, [selectedId, items]);}
```

Example 2 (jsx):
```jsx
// ✅ setState in an effect is fine if the value comes from a reffunction Tooltip() {  const ref = useRef(null);  const [tooltipHeight, setTooltipHeight] = useState(0);  useLayoutEffect(() => {    const { height } = ref.current.getBoundingClientRect();    setTooltipHeight(height);  }, []);}// ✅ Calculate during renderfunction Component({selectedId, items}) {  const selected = items.find(i => i.id === selectedId);  return <div>{selected?.name}</div>;}
```

---

## set-state-in-render

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-render

**Contents:**
- set-state-in-render
- Rule Details
- Common Violations
  - Invalid
  - Valid
- Troubleshooting
  - I want to sync state to a prop

Validates against unconditionally setting state during render, which can trigger additional renders and potential infinite render loops.

Calling setState during render unconditionally triggers another render before the current one finishes. This creates an infinite loop that crashes your app.

A common problem is trying to “fix” state after it renders. Suppose you want to keep a counter from exceeding a max prop:

As soon as count exceeds max, an infinite loop is triggered.

Instead, it’s often better to move this logic to the event (the place where the state is first set). For example, you can enforce the maximum at the moment you update state:

Now the setter only runs in response to the click, React finishes the render normally, and count never crosses max.

In rare cases, you may need to adjust state based on information from previous renders. For those, follow this pattern of setting state conditionally.

**Examples:**

Example 1 (jsx):
```jsx
// ❌ Unconditional setState directly in renderfunction Component({value}) {  const [count, setCount] = useState(0);  setCount(value); // Infinite loop!  return <div>{count}</div>;}
```

Example 2 (jsx):
```jsx
// ✅ Derive during renderfunction Component({items}) {  const sorted = [...items].sort(); // Just calculate it in render  return <ul>{sorted.map(/*...*/)}</ul>;}// ✅ Set state in event handlerfunction Component() {  const [count, setCount] = useState(0);  return (    <button onClick={() => setCount(count + 1)}>      {count}    </button>  );}// ✅ Derive from props instead of setting statefunction Component({user}) {  const name = user?.name || '';  const email = user?.email || '';  return <div>{name}</div>;}// ✅ Conditionally derive state from props and state from previous rendersfunction Component({ items }) {  const [isReverse, setIsReverse] = useState(false);  const [selection, setSelection] = useState(null);  const [prevItems, setPrevItems] = useState(items);  if (items !== prevItems) { // This condition makes it valid    setPrevItems(items);    setSelection(null);  }  // ...}
```

Example 3 (jsx):
```jsx
// ❌ Wrong: clamps during renderfunction Counter({max}) {  const [count, setCount] = useState(0);  if (count > max) {    setCount(max);  }  return (    <button onClick={() => setCount(count + 1)}>      {count}    </button>  );}
```

Example 4 (jsx):
```jsx
// ✅ Clamp when updatingfunction Counter({max}) {  const [count, setCount] = useState(0);  const increment = () => {    setCount(current => Math.min(current + 1, max));  };  return <button onClick={increment}>{count}</button>;}
```

---

## static-components

**URL:** https://react.dev/reference/eslint-plugin-react-hooks/lints/static-components

**Contents:**
- static-components
- Rule Details
  - Invalid
  - Valid
- Troubleshooting
  - I need to render different components conditionally
  - Note

Validates that components are static, not recreated every render. Components that are recreated dynamically can reset state and trigger excessive re-rendering.

Components defined inside other components are recreated on every render. React sees each as a brand new component type, unmounting the old one and mounting the new one, destroying all state and DOM nodes in the process.

Examples of incorrect code for this rule:

Examples of correct code for this rule:

You might define components inside to access local state:

Pass data as props instead:

If you find yourself wanting to define components inside other components to access local variables, that’s a sign you should be passing props instead. This makes components more reusable and testable.

**Examples:**

Example 1 (jsx):
```jsx
// ❌ Component defined inside componentfunction Parent() {  const ChildComponent = () => { // New component every render!    const [count, setCount] = useState(0);    return <button onClick={() => setCount(count + 1)}>{count}</button>;  };  return <ChildComponent />; // State resets every render}// ❌ Dynamic component creationfunction Parent({type}) {  const Component = type === 'button'    ? () => <button>Click</button>    : () => <div>Text</div>;  return <Component />;}
```

Example 2 (jsx):
```jsx
// ✅ Components at module levelconst ButtonComponent = () => <button>Click</button>;const TextComponent = () => <div>Text</div>;function Parent({type}) {  const Component = type === 'button'    ? ButtonComponent  // Reference existing component    : TextComponent;  return <Component />;}
```

Example 3 (jsx):
```jsx
// ❌ Wrong: Inner component to access parent statefunction Parent() {  const [theme, setTheme] = useState('light');  function ThemedButton() { // Recreated every render!    return (      <button className={theme}>        Click me      </button>    );  }  return <ThemedButton />;}
```

Example 4 (jsx):
```jsx
// ✅ Better: Pass props to static componentfunction ThemedButton({theme}) {  return (    <button className={theme}>      Click me    </button>  );}function Parent() {  const [theme, setTheme] = useState('light');  return <ThemedButton theme={theme} />;}
```

---

## <StrictMode>

**URL:** https://react.dev/reference/react/StrictMode

**Contents:**
- <StrictMode>
- Reference
  - <StrictMode>
    - Props
    - Caveats
- Usage
  - Enabling Strict Mode for entire app
  - Note
  - Enabling Strict Mode for a part of the app
  - Note

<StrictMode> lets you find common bugs in your components early during development.

Use StrictMode to enable additional development behaviors and warnings for the component tree inside:

See more examples below.

Strict Mode enables the following development-only behaviors:

StrictMode accepts no props.

Strict Mode enables extra development-only checks for the entire component tree inside the <StrictMode> component. These checks help you find common bugs in your components early in the development process.

To enable Strict Mode for your entire app, wrap your root component with <StrictMode> when you render it:

We recommend wrapping your entire app in Strict Mode, especially for newly created apps. If you use a framework that calls createRoot for you, check its documentation for how to enable Strict Mode.

Although the Strict Mode checks only run in development, they help you find bugs that already exist in your code but can be tricky to reliably reproduce in production. Strict Mode lets you fix bugs before your users report them.

Strict Mode enables the following checks in development:

All of these checks are development-only and do not impact the production build.

You can also enable Strict Mode for any part of your application:

In this example, Strict Mode checks will not run against the Header and Footer components. However, they will run on Sidebar and Content, as well as all of the components inside them, no matter how deep.

When StrictMode is enabled for a part of the app, React will only enable behaviors that are possible in production. For example, if <StrictMode> is not enabled at the root of the app, it will not re-run Effects an extra time on initial mount, since this would cause child effects to double fire without the parent effects, which cannot happen in production.

React assumes that every component you write is a pure function. This means that React components you write must always return the same JSX given the same inputs (props, state, and context).

Components breaking this rule behave unpredictably and cause bugs. To help you find accidentally impure code, Strict Mode calls some of your functions (only the ones that should be pure) twice in development. This includes:

If a function is pure, running it twice does not change its behavior because a pure function produces the same result every time. However, if a function is impure (for example, it mutates the data it receives), running it twice tends to be noticeable (that’s what makes it impure!) This helps you spot and fix the bug early.

Here is an example to illustrate how double rendering in Strict Mode helps you find bugs early.

This StoryTray component takes an array of stories and adds one last “Create Story” item at the end:

There is a mistake in the code above. However, it is easy to miss because the initial output appears correct.

This mistake will become more noticeable if the StoryTray component re-renders multiple times. For example, let’s make the StoryTray re-render with a different background color whenever you hover over it:

Notice how every time you hover over the StoryTray component, “Create Story” gets added to the list again. The intention of the code was to add it once at the end. But StoryTray directly modifies the stories array from the props. Every time StoryTray renders, it adds “Create Story” again at the end of the same array. In other words, StoryTray is not a pure function—running it multiple times produces different results.

To fix this problem, you can make a copy of the array, and modify that copy instead of the original one:

This would make the StoryTray function pure. Each time it is called, it would only modify a new copy of the array, and would not affect any external objects or variables. This solves the bug, but you had to make the component re-render more often before it became obvious that something is wrong with its behavior.

In the original example, the bug wasn’t obvious. Now let’s wrap the original (buggy) code in <StrictMode>:

Strict Mode always calls your rendering function twice, so you can see the mistake right away (“Create Story” appears twice). This lets you notice such mistakes early in the process. When you fix your component to render in Strict Mode, you also fix many possible future production bugs like the hover functionality from before:

Without Strict Mode, it was easy to miss the bug until you added more re-renders. Strict Mode made the same bug appear right away. Strict Mode helps you find bugs before you push them to your team and to your users.

Read more about keeping components pure.

If you have React DevTools installed, any console.log calls during the second render call will appear slightly dimmed. React DevTools also offers a setting (off by default) to suppress them completely.

Strict Mode can also help find bugs in Effects.

Every Effect has some setup code and may have some cleanup code. Normally, React calls setup when the component mounts (is added to the screen) and calls cleanup when the component unmounts (is removed from the screen). React then calls cleanup and setup again if its dependencies changed since the last render.

When Strict Mode is on, React will also run one extra setup+cleanup cycle in development for every Effect. This may feel surprising, but it helps reveal subtle bugs that are hard to catch manually.

Here is an example to illustrate how re-running Effects in Strict Mode helps you find bugs early.

Consider this example that connects a component to a chat:

There is an issue with this code, but it might not be immediately clear.

To make the issue more obvious, let’s implement a feature. In the example below, roomId is not hardcoded. Instead, the user can select the roomId that they want to connect to from a dropdown. Click “Open chat” and then select different chat rooms one by one. Keep track of the number of active connections in the console:

You’ll notice that the number of open connections always keeps growing. In a real app, this would cause performance and network problems. The issue is that your Effect is missing a cleanup function:

Now that your Effect “cleans up” after itself and destroys the outdated connections, the leak is solved. However, notice that the problem did not become visible until you’ve added more features (the select box).

In the original example, the bug wasn’t obvious. Now let’s wrap the original (buggy) code in <StrictMode>:

With Strict Mode, you immediately see that there is a problem (the number of active connections jumps to 2). Strict Mode runs an extra setup+cleanup cycle for every Effect. This Effect has no cleanup logic, so it creates an extra connection but doesn’t destroy it. This is a hint that you’re missing a cleanup function.

Strict Mode lets you notice such mistakes early in the process. When you fix your Effect by adding a cleanup function in Strict Mode, you also fix many possible future production bugs like the select box from before:

Notice how the active connection count in the console doesn’t keep growing anymore.

Without Strict Mode, it was easy to miss that your Effect needed cleanup. By running setup → cleanup → setup instead of setup for your Effect in development, Strict Mode made the missing cleanup logic more noticeable.

Read more about implementing Effect cleanup.

Strict Mode can also help find bugs in callbacks refs.

Every callback ref has some setup code and may have some cleanup code. Normally, React calls setup when the element is created (is added to the DOM) and calls cleanup when the element is removed (is removed from the DOM).

When Strict Mode is on, React will also run one extra setup+cleanup cycle in development for every callback ref. This may feel surprising, but it helps reveal subtle bugs that are hard to catch manually.

Consider this example, which allows you to select an animal and then scroll to one of them. Notice when you switch from “Cats” to “Dogs”, the console logs show that the number of animals in the list keeps growing, and the “Scroll to” buttons stop working:

This is a production bug! Since the ref callback doesn’t remove animals from the list in the cleanup, the list of animals keeps growing. This is a memory leak that can cause performance problems in a real app, and breaks the behavior of the app.

The issue is the ref callback doesn’t cleanup after itself:

Now let’s wrap the original (buggy) code in <StrictMode>:

With Strict Mode, you immediately see that there is a problem. Strict Mode runs an extra setup+cleanup cycle for every callback ref. This callback ref has no cleanup logic, so it adds refs but doesn’t remove them. This is a hint that you’re missing a cleanup function.

Strict Mode lets you eagerly find mistakes in callback refs. When you fix your callback by adding a cleanup function in Strict Mode, you also fix many possible future production bugs like the “Scroll to” bug from before:

Now on inital mount in StrictMode, the ref callbacks are all setup, cleaned up, and setup again:

This is expected. Strict Mode confirms that the ref callbacks are cleaned up correctly, so the size never grows above the expected amount. After the fix, there are no memory leaks, and all the features work as expected.

Without Strict Mode, it was easy to miss the bug until you clicked around to app to notice broken features. Strict Mode made the bugs appear right away, before you push them to production.

React warns if some component anywhere inside a <StrictMode> tree uses one of these deprecated APIs:

These APIs are primarily used in older class components so they rarely appear in modern apps.

**Examples:**

Example 1 (jsx):
```jsx
<StrictMode>  <App /></StrictMode>
```

Example 2 (jsx):
```jsx
import { StrictMode } from 'react';import { createRoot } from 'react-dom/client';const root = createRoot(document.getElementById('root'));root.render(  <StrictMode>    <App />  </StrictMode>);
```

Example 3 (jsx):
```jsx
import { StrictMode } from 'react';import { createRoot } from 'react-dom/client';const root = createRoot(document.getElementById('root'));root.render(  <StrictMode>    <App />  </StrictMode>);
```

Example 4 (jsx):
```jsx
import { StrictMode } from 'react';function App() {  return (    <>      <Header />      <StrictMode>        <main>          <Sidebar />          <Content />        </main>      </StrictMode>      <Footer />    </>  );}
```

---

## <style>

**URL:** https://react.dev/reference/react-dom/components/style

**Contents:**
- <style>
- Reference
  - <style>
    - Props
    - Special rendering behavior
- Usage
  - Rendering an inline CSS stylesheet

The built-in browser <style> component lets you add inline CSS stylesheets to your document.

To add inline styles to your document, render the built-in browser <style> component. You can render <style> from any component and React will in certain cases place the corresponding DOM element in the document head and de-duplicate identical styles.

See more examples below.

<style> supports all common element props.

Props that are not recommended for use with React:

React can move <style> components to the document’s <head>, de-duplicate identical stylesheets, and suspend while the stylesheet is loading.

To opt into this behavior, provide the href and precedence props. React will de-duplicate styles if they have the same href. The precedence prop tells React where to rank the <style> DOM node relative to others in the document <head>, which determines which stylesheet can override the other.

This special treatment comes with three caveats:

If a component depends on certain CSS styles in order to be displayed correctly, you can render an inline stylesheet within the component.

The href prop should uniquely identify the stylesheet, because React will de-duplicate stylesheets that have the same href. If you supply a precedence prop, React will reorder inline stylesheets based on the order these values appear in the component tree.

Inline stylesheets will not trigger Suspense boundaries while they’re loading. Even if they load async resources like fonts or images.

**Examples:**

Example 1 (css):
```css
<style>{` p { color: red; } `}</style>
```

Example 2 (css):
```css
<style>{` p { color: red; } `}</style>
```

---

## <textarea>

**URL:** https://react.dev/reference/react-dom/components/textarea

**Contents:**
- <textarea>
- Reference
  - <textarea>
    - Props
    - Caveats
- Usage
  - Displaying a text area
  - Providing a label for a text area
  - Providing an initial value for a text area
  - Pitfall

The built-in browser <textarea> component lets you render a multiline text input.

To display a text area, render the built-in browser <textarea> component.

See more examples below.

<textarea> supports all common element props.

You can make a text area controlled by passing a value prop:

When you pass value, you must also pass an onChange handler that updates the passed value.

If your <textarea> is uncontrolled, you may pass the defaultValue prop instead:

These <textarea> props are relevant both for uncontrolled and controlled text areas:

Render <textarea> to display a text area. You can specify its default size with the rows and cols attributes, but by default the user will be able to resize it. To disable resizing, you can specify resize: none in the CSS.

Typically, you will place every <textarea> inside a <label> tag. This tells the browser that this label is associated with that text area. When the user clicks the label, the browser will focus the text area. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the text area.

If you can’t nest <textarea> into a <label>, associate them by passing the same ID to <textarea id> and <label htmlFor>. To avoid conflicts between instances of one component, generate such an ID with useId.

You can optionally specify the initial value for the text area. Pass it as the defaultValue string.

Unlike in HTML, passing initial text like <textarea>Some content</textarea> is not supported.

Add a <form> around your textarea with a <button type="submit"> inside. It will call your <form onSubmit> event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling e.preventDefault(). Read the form data with new FormData(e.target).

Give a name to your <textarea>, for example <textarea name="postContent" />. The name you specified will be used as a key in the form data, for example { postContent: "Your post" }.

By default, any <button> inside a <form> will submit it. This can be surprising! If you have your own custom Button React component, consider returning <button type="button"> instead of <button>. Then, to be explicit, use <button type="submit"> for buttons that are supposed to submit the form.

A text area like <textarea /> is uncontrolled. Even if you pass an initial value like <textarea defaultValue="Initial text" />, your JSX only specifies the initial value, not the value right now.

To render a controlled text area, pass the value prop to it. React will force the text area to always have the value you passed. Typically, you will control a text area by declaring a state variable:

This is useful if you want to re-render some part of the UI in response to every keystroke.

If you pass value without onChange, it will be impossible to type into the text area. When you control a text area by passing some value to it, you force it to always have the value you passed. So if you pass a state variable as a value but forget to update that state variable synchronously during the onChange event handler, React will revert the text area after every keystroke back to the value that you specified.

If you render a text area with value but no onChange, you will see an error in the console:

As the error message suggests, if you only wanted to specify the initial value, pass defaultValue instead:

If you want to control this text area with a state variable, specify an onChange handler:

If the value is intentionally read-only, add a readOnly prop to suppress the error:

If you control a text area, you must update its state variable to the text area’s value from the DOM during onChange.

You can’t update it to something other than e.target.value:

You also can’t update it asynchronously:

To fix your code, update it synchronously to e.target.value:

If this doesn’t fix the problem, it’s possible that the text area gets removed and re-added from the DOM on every keystroke. This can happen if you’re accidentally resetting state on every re-render. For example, this can happen if the text area or one of its parents always receives a different key attribute, or if you nest component definitions (which is not allowed in React and causes the “inner” component to remount on every render).

If you provide a value to the component, it must remain a string throughout its lifetime.

You cannot pass value={undefined} first and later pass value="some string" because React won’t know whether you want the component to be uncontrolled or controlled. A controlled component should always receive a string value, not null or undefined.

If your value is coming from an API or a state variable, it might be initialized to null or undefined. In that case, either set it to an empty string ('') initially, or pass value={someValue ?? ''} to ensure value is a string.

**Examples:**

Example 1 (jsx):
```jsx
<textarea />
```

Example 2 (jsx):
```jsx
<textarea name="postContent" />
```

Example 3 (jsx):
```jsx
function NewPost() {  const [postContent, setPostContent] = useState(''); // Declare a state variable...  // ...  return (    <textarea      value={postContent} // ...force the input's value to match the state variable...      onChange={e => setPostContent(e.target.value)} // ... and update the state variable on any edits!    />  );}
```

Example 4 (jsx):
```jsx
// 🔴 Bug: controlled text area with no onChange handler<textarea value={something} />
```

---

## <title>

**URL:** https://react.dev/reference/react-dom/components/title

**Contents:**
- <title>
- Reference
  - <title>
    - Props
    - Special rendering behavior
  - Pitfall
- Usage
  - Set the document title
  - Use variables in the title

The built-in browser <title> component lets you specify the title of the document.

To specify the title of the document, render the built-in browser <title> component. You can render <title> from any component and React will always place the corresponding DOM element in the document head.

See more examples below.

<title> supports all common element props.

React will always place the DOM element corresponding to the <title> component within the document’s <head>, regardless of where in the React tree it is rendered. The <head> is the only valid place for <title> to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render its <title> itself.

There are two exception to this:

Only render a single <title> at a time. If more than one component renders a <title> tag at the same time, React will place all of those titles in the document head. When this happens, the behavior of browsers and search engines is undefined.

Render the <title> component from any component with text as its children. React will put a <title> DOM node in the document <head>.

The children of the <title> component must be a single string of text. (Or a single number or a single object with a toString method.) It might not be obvious, but using JSX curly braces like this:

… actually causes the <title> component to get a two-element array as its children (the string "Results page" and the value of pageNumber). This will cause an error. Instead, use string interpolation to pass <title> a single string:

**Examples:**

Example 1 (typescript):
```typescript
<title>My Blog</title>
```

Example 2 (typescript):
```typescript
<title>My Blog</title>
```

Example 3 (typescript):
```typescript
<title>Results page {pageNumber}</title> // 🔴 Problem: This is not a single string
```

Example 4 (typescript):
```typescript
<title>{`Results page ${pageNumber}`}</title>
```

---

## useActionState

**URL:** https://react.dev/reference/react/useActionState

**Contents:**
- useActionState
  - Note
- Reference
  - useActionState(action, initialState, permalink?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Using information returned by a form action
    - Display information after submitting a form

useActionState is a Hook that allows you to update state based on the result of a form action.

In earlier React Canary versions, this API was part of React DOM and called useFormState.

Call useActionState at the top level of your component to create component state that is updated when a form action is invoked. You pass useActionState an existing form action function as well as an initial state, and it returns a new action that you use in your form, along with the latest form state and whether the Action is still pending. The latest form state is also passed to the function that you provided.

The form state is the value returned by the action when the form was last submitted. If the form has not yet been submitted, it is the initial state that you pass.

If used with a Server Function, useActionState allows the server’s response from submitting the form to be shown even before hydration has completed.

See more examples below.

useActionState returns an array with the following values:

Call useActionState at the top level of your component to access the return value of an action from the last time a form was submitted.

useActionState returns an array with the following items:

When the form is submitted, the action function that you provided will be called. Its return value will become the new current state of the form.

The action that you provide will also receive a new first argument, namely the current state of the form. The first time the form is submitted, this will be the initial state you provided, while with subsequent submissions, it will be the return value from the last time the action was called. The rest of the arguments are the same as if useActionState had not been used.

To display messages such as an error message or toast that’s returned by a Server Function, wrap the action in a call to useActionState.

When you wrap an action with useActionState, it gets an extra argument as its first argument. The submitted form data is therefore its second argument instead of its first as it would usually be. The new first argument that gets added is the current state of the form.

**Examples:**

Example 1 (unknown):
```unknown
const [state, formAction, isPending] = useActionState(fn, initialState, permalink?);
```

Example 2 (javascript):
```javascript
import { useActionState } from "react";async function increment(previousState, formData) {  return previousState + 1;}function StatefulForm({}) {  const [state, formAction] = useActionState(increment, 0);  return (    <form>      {state}      <button formAction={formAction}>Increment</button>    </form>  )}
```

Example 3 (jsx):
```jsx
import { useActionState } from 'react';import { action } from './actions.js';function MyComponent() {  const [state, formAction] = useActionState(action, null);  // ...  return (    <form action={formAction}>      {/* ... */}    </form>  );}
```

Example 4 (javascript):
```javascript
function action(currentState, formData) {  // ...  return 'next state';}
```

---

## useState

**URL:** https://react.dev/reference/react/useState

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething] using array destructuring.

useState returns an array with exactly two items:

To update what’s on the screen, call the set function with some next state:

React will store the next state, render your component again with the new values, and update the UI.

Calling the set function does not change the current state in the already executing code:

It only affects what useState will return starting from the next render.

In this example, the count state variable holds a number. Clicking the button increments it.

Suppose the age is 42. This handler calls setAge(age + 1) three times:

However, after one click, age will only be 43 rather than 45! This is because calling the set function does not update the age state variable in the already running code. So each setAge(age + 1) call becomes setAge(43).

To solve this problem, you may pass an updater function to setAge instead of the next state:

Here, a => a + 1 is your updater function. It takes the pending state and calculates the next state from it.

React puts your updater functions in a queue. Then, during the next render, it will call them in the same order:

There are no other queued updates, so React will store 45 as the current state in the end.

By convention, it’s common to name the pending state argument for the first letter of the state variable name, like a for age. However, you may also call it like prevAge or something else that you find clearer.

React may call your updaters twice in development to verify that they are pure.

You might hear a recommendation to always write code like setAge(a => a + 1) if the state you’re setting is calculated from the previous state. There is no harm in it, but it is also not always necessary.

In most cases, there is no difference between these two approaches. React always makes sure that for intentional user actions, like clicks, the age state variable would be updated before the next click. This means there is no risk of a click handler seeing a “stale” age at the beginning of the event handler.

However, if you do multiple updates within the same event, updaters can be helpful. They’re also helpful if accessing the state variable itself is inconvenient (you might run into this when optimizing re-renders).

If you prefer consistency over slightly more verbose syntax, it’s reasonable to always write an updater if the state you’re setting is calculated from the previous state. If it’s calculated from the previous state of some other state variable, you might want to combine them into one object and use a reducer.

This example passes the updater function, so the “+3” button works.

You can put objects and arrays into state. In React, state is considered read-only, so you should replace it rather than mutate your existing objects. For example, if you have a form object in state, don’t mutate it:

Instead, replace the whole object by creating a new one:

Read updating objects in state and updating arrays in state to learn more.

In this example, the form state variable holds an object. Each input has a change handler that calls setForm with the next state of the entire form. The { ...form } spread syntax ensures that the state object is replaced rather than mutated.

React saves the initial state once and ignores it on the next renders.

Although the result of createInitialTodos() is only used for the initial render, you’re still calling this function on every render. This can be wasteful if it’s creating large arrays or performing expensive calculations.

To solve this, you may pass it as an initializer function to useState instead:

Notice that you’re passing createInitialTodos, which is the function itself, and not createInitialTodos(), which is the result of calling it. If you pass a function to useState, React will only call it during initialization.

React may call your initializers twice in development to verify that they are pure.

This example passes the initializer function, so the createInitialTodos function only runs during initialization. It does not run when component re-renders, such as when you type into the input.

You’ll often encounter the key attribute when rendering lists. However, it also serves another purpose.

You can reset a component’s state by passing a different key to a component. In this example, the Reset button changes the version state variable, which we pass as a key to the Form. When the key changes, React re-creates the Form component (and all of its children) from scratch, so its state gets reset.

Read preserving and resetting state to learn more.

Usually, you will update state in event handlers. However, in rare cases you might want to adjust state in response to rendering — for example, you might want to change a state variable when a prop changes.

In most cases, you don’t need this:

In the rare case that none of these apply, there is a pattern you can use to update state based on the values that have been rendered so far, by calling a set function while your component is rendering.

Here’s an example. This CountLabel component displays the count prop passed to it:

Say you want to show whether the counter has increased or decreased since the last change. The count prop doesn’t tell you this — you need to keep track of its previous value. Add the prevCount state variable to track it. Add another state variable called trend to hold whether the count has increased or decreased. Compare prevCount with count, and if they’re not equal, update both prevCount and trend. Now you can show both the current count prop and how it has changed since the last render.

Note that if you call a set function while rendering, it must be inside a condition like prevCount !== count, and there must be a call like setPrevCount(count) inside of the condition. Otherwise, your component would re-render in a loop until it crashes. Also, you can only update the state of the currently rendering component like this. Calling the set function of another component during rendering is an error. Finally, your set call should still update state without mutation — this doesn’t mean you can break other rules of pure functions.

This pattern can be hard to understand and is usually best avoided. However, it’s better than updating state in an effect. When you call the set function during render, React will re-render that component immediately after your component exits with a return statement, and before rendering the children. This way, children don’t need to render twice. The rest of your component function will still execute (and the result will be thrown away). If your condition is below all the Hook calls, you may add an early return; to restart rendering earlier.

Calling the set function does not change state in the running code:

This is because states behaves like a snapshot. Updating state requests another render with the new state value, but does not affect the count JavaScript variable in your already-running event handler.

If you need to use the next state, you can save it in a variable before passing it to the set function:

React will ignore your update if the next state is equal to the previous state, as determined by an Object.is comparison. This usually happens when you change an object or an array in state directly:

You mutated an existing obj object and passed it back to setObj, so React ignored the update. To fix this, you need to ensure that you’re always replacing objects and arrays in state instead of mutating them:

You might get an error that says: Too many re-renders. React limits the number of renders to prevent an infinite loop. Typically, this means that you’re unconditionally setting state during render, so your component enters a loop: render, set state (which causes a render), render, set state (which causes a render), and so on. Very often, this is caused by a mistake in specifying an event handler:

If you can’t find the cause of this error, click on the arrow next to the error in the console and look through the JavaScript stack to find the specific set function call responsible for the error.

In Strict Mode, React will call some of your functions twice instead of once:

This is expected and shouldn’t break your code.

This development-only behavior helps you keep components pure. React uses the result of one of the calls, and ignores the result of the other call. As long as your component, initializer, and updater functions are pure, this shouldn’t affect your logic. However, if they are accidentally impure, this helps you notice the mistakes.

For example, this impure updater function mutates an array in state:

Because React calls your updater function twice, you’ll see the todo was added twice, so you’ll know that there is a mistake. In this example, you can fix the mistake by replacing the array instead of mutating it:

Now that this updater function is pure, calling it an extra time doesn’t make a difference in behavior. This is why React calling it twice helps you find mistakes. Only component, initializer, and updater functions need to be pure. Event handlers don’t need to be pure, so React will never call your event handlers twice.

Read keeping components pure to learn more.

You can’t put a function into state like this:

Because you’re passing a function, React assumes that someFunction is an initializer function, and that someOtherFunction is an updater function, so it tries to call them and store the result. To actually store a function, you have to put () => before them in both cases. Then React will store the functions you pass.

**Examples:**

Example 1 (jsx):
```jsx
const [state, setState] = useState(initialState)
```

Example 2 (javascript):
```javascript
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (jsx):
```jsx
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---
