# React_Docs - Getting Started

**Pages:** 51

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already have, but instead triggers a re-render. This can be surprising at first!

This behavior helps you avoid subtle bugs. Here is a little chat app. Try to guess what happens if you press “Send” first and then change the recipient to Bob. Whose name will appear in the alert five seconds later?

Read State as a Snapshot to learn why state appears “fixed” and unchanging inside the event handlers.

This component is buggy: clicking “+3” increments the score only once.

State as a Snapshot explains why this is happening. Setting state requests a new re-render, but does not change it in the already running code. So score continues to be 0 right after you call setScore(score + 1).

You can fix this by passing an updater function when setting state. Notice how replacing setScore(score + 1) with setScore(s => s + 1) fixes the “+3” button. This lets you queue multiple state updates.

Read Queueing a Series of State Updates to learn how to queue a sequence of state updates.

State can hold any kind of JavaScript value, including objects. But you shouldn’t change objects and arrays that you hold in the React state directly. Instead, when you want to update an object and array, you need to create a new one (or make a copy of an existing one), and then update the state to use that copy.

Usually, you will use the ... spread syntax to copy objects and arrays that you want to change. For example, updating a nested object could look like this:

If copying objects in code gets tedious, you can use a library like Immer to reduce repetitive code:

Read Updating Objects in State to learn how to update objects correctly.

Arrays are another type of mutable JavaScript objects you can store in state and should treat as read-only. Just like with objects, when you want to update an array stored in state, you need to create a new one (or make a copy of an existing one), and then set state to use the new array:

If copying arrays in code gets tedious, you can use a library like Immer to reduce repetitive code:

Read Updating Arrays in State to learn how to update arrays correctly.

Head over to Responding to Events to start reading this chapter page by page!

Or, if you’re already familiar with these topics, why not read about Managing State?

**Examples:**

Example 1 (jsx):
```jsx
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (javascript):
```javascript
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (javascript):
```javascript
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Add React to an Existing Project

**URL:** https://react.dev/learn/add-react-to-an-existing-project

**Contents:**
- Add React to an Existing Project
  - Note
- Using React for an entire subroute of your existing website
- Using React for a part of your existing page
  - Step 1: Set up a modular JavaScript environment
  - Note
  - Step 2: Render React components anywhere on the page
- Using React Native in an existing native mobile app

If you want to add some interactivity to your existing project, you don’t have to rewrite it in React. Add React to your existing stack, and render interactive React components anywhere.

You need to install Node.js for local development. Although you can try React online or with a simple HTML page, realistically most JavaScript tooling you’ll want to use for development requires Node.js.

Let’s say you have an existing web app at example.com built with another server technology (like Rails), and you want to implement all routes starting with example.com/some-app/ fully with React.

Here’s how we recommend to set it up:

This ensures the React part of your app can benefit from the best practices baked into those frameworks.

Many React-based frameworks are full-stack and let your React app take advantage of the server. However, you can use the same approach even if you can’t or don’t want to run JavaScript on the server. In that case, serve the HTML/CSS/JS export (next export output for Next.js, default for Gatsby) at /some-app/ instead.

Let’s say you have an existing page built with another technology (either a server one like Rails, or a client one like Backbone), and you want to render interactive React components somewhere on that page. That’s a common way to integrate React—in fact, it’s how most React usage looked at Meta for many years!

You can do this in two steps:

The exact approach depends on your existing page setup, so let’s walk through some details.

A modular JavaScript environment lets you write your React components in individual files, as opposed to writing all of your code in a single file. It also lets you use all the wonderful packages published by other developers on the npm registry—including React itself! How you do this depends on your existing setup:

If your app is already split into files that use import statements, try to use the setup you already have. Check whether writing <div /> in your JS code causes a syntax error. If it causes a syntax error, you might need to transform your JavaScript code with Babel, and enable the Babel React preset to use JSX.

If your app doesn’t have an existing setup for compiling JavaScript modules, set it up with Vite. The Vite community maintains many integrations with backend frameworks, including Rails, Django, and Laravel. If your backend framework is not listed, follow this guide to manually integrate Vite builds with your backend.

To check whether your setup works, run this command in your project folder:

Then add these lines of code at the top of your main JavaScript file (it might be called index.js or main.js):

If the entire content of your page was replaced by a “Hello, world!”, everything worked! Keep reading.

Integrating a modular JavaScript environment into an existing project for the first time can feel intimidating, but it’s worth it! If you get stuck, try our community resources or the Vite Chat.

In the previous step, you put this code at the top of your main file:

Of course, you don’t actually want to clear the existing HTML content!

Instead, you probably want to render your React components in specific places in your HTML. Open your HTML page (or the server templates that generate it) and add a unique id attribute to any tag, for example:

This lets you find that HTML element with document.getElementById and pass it to createRoot so that you can render your own React component inside:

Notice how the original HTML content from index.html is preserved, but your own NavigationBar React component now appears inside the <nav id="navigation"> from your HTML. Read the createRoot usage documentation to learn more about rendering React components inside an existing HTML page.

When you adopt React in an existing project, it’s common to start with small interactive components (like buttons), and then gradually keep “moving upwards” until eventually your entire page is built with React. If you ever reach that point, we recommend migrating to a React framework right after to get the most out of React.

React Native can also be integrated into existing native apps incrementally. If you have an existing native app for Android (Java or Kotlin) or iOS (Objective-C or Swift), follow this guide to add a React Native screen to it.

**Examples:**

Example 1 (unknown):
```unknown
npm install react react-dom
```

Example 2 (jsx):
```jsx
import { createRoot } from 'react-dom/client';// Clear the existing HTML contentdocument.body.innerHTML = '<div id="app"></div>';// Render your React component insteadconst root = createRoot(document.getElementById('app'));root.render(<h1>Hello, world</h1>);
```

Example 3 (jsx):
```jsx
<!-- ... somewhere in your html ... --><nav id="navigation"></nav><!-- ... more html ... -->
```

---

## Build a React app from Scratch

**URL:** https://react.dev/learn/build-a-react-app-from-scratch

**Contents:**
- Build a React app from Scratch
      - Deep Dive
    - Consider using a framework
- Step 1: Install a build tool
  - Vite
  - Parcel
  - Rsbuild
  - Note
    - Metro for React Native
- Step 2: Build Common Application Patterns

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, you can build a React app from scratch.

Starting from scratch is an easy way to get started using React, but a major tradeoff to be aware of is that going this route is often the same as building your own adhoc framework. As your requirements evolve, you may need to solve more framework-like problems that our recommended frameworks already have well developed and supported solutions for.

For example, if in the future your app needs support for server-side rendering (SSR), static site generation (SSG), and/or React Server Components (RSC), you will have to implement those on your own. Similarly, future React features that require integrating at the framework level will have to be implemented on your own if you want to use them.

Our recommended frameworks also help you build better performing apps. For example, reducing or eliminating waterfalls from network requests makes for a better user experience. This might not be a high priority when you are building a toy project, but if your app gains users you may want to improve its performance.

Going this route also makes it more difficult to get support, since the way you develop routing, data-fetching, and other features will be unique to your situation. You should only choose this option if you are comfortable tackling these problems on your own, or if you’re confident that you will never need these features.

For a list of recommended frameworks, check out Creating a React App.

The first step is to install a build tool like vite, parcel, or rsbuild. These build tools provide features to package and run source code, provide a development server for local development and a build command to deploy your app to a production server.

Vite is a build tool that aims to provide a faster and leaner development experience for modern web projects.

Vite is opinionated and comes with sensible defaults out of the box. Vite has a rich ecosystem of plugins to support fast refresh, JSX, Babel/SWC, and other common features. See Vite’s React plugin or React SWC plugin and React SSR example project to get started.

Vite is already being used as a build tool in one of our recommended frameworks: React Router.

Parcel combines a great out-of-the-box development experience with a scalable architecture that can take your project from just getting started to massive production applications.

Parcel supports fast refresh, JSX, TypeScript, Flow, and styling out of the box. See Parcel’s React recipe to get started.

Rsbuild is an Rspack-powered build tool that provides a seamless development experience for React applications. It comes with carefully tuned defaults and performance optimizations ready to use.

Rsbuild includes built-in support for React features like fast refresh, JSX, TypeScript, and styling. See Rsbuild’s React guide to get started.

If you’re starting from scratch with React Native you’ll need to use Metro, the JavaScript bundler for React Native. Metro supports bundling for platforms like iOS and Android, but lacks many features when compared to the tools here. We recommend starting with Vite, Parcel, or Rsbuild unless your project requires React Native support.

The build tools listed above start off with a client-only, single-page app (SPA), but don’t include any further solutions for common functionality like routing, data fetching, or styling.

The React ecosystem includes many tools for these problems. We’ve listed a few that are widely used as a starting point, but feel free to choose other tools if those work better for you.

Routing determines what content or pages to display when a user visits a particular URL. You need to set up a router to map URLs to different parts of your app. You’ll also need to handle nested routes, route parameters, and query parameters. Routers can be configured within your code, or defined based on your component folder and file structures.

Routers are a core part of modern applications, and are usually integrated with data fetching (including prefetching data for a whole page for faster loading), code splitting (to minimize client bundle sizes), and page rendering approaches (to decide how each page gets generated).

Fetching data from a server or other data source is a key part of most applications. Doing this properly requires handling loading states, error states, and caching the fetched data, which can be complex.

Purpose-built data fetching libraries do the hard work of fetching and caching the data for you, letting you focus on what data your app needs and how to display it. These libraries are typically used directly in your components, but can also be integrated into routing loaders for faster pre-fetching and better performance, and in server rendering as well.

Note that fetching data directly in components can lead to slower loading times due to network request waterfalls, so we recommend prefetching data in router loaders or on the server as much as possible! This allows a page’s data to be fetched all at once as the page is being displayed.

If you’re fetching data from most backends or REST-style APIs, we suggest using:

If you’re fetching data from a GraphQL API, we suggest using:

Code-splitting is the process of breaking your app into smaller bundles that can be loaded on demand. An app’s code size increases with every new feature and additional dependency. Apps can become slow to load because all of the code for the entire app needs to be sent before it can be used. Caching, reducing features/dependencies, and moving some code to run on the server can help mitigate slow loading but are incomplete solutions that can sacrifice functionality if overused.

Similarly, if you rely on the apps using your framework to split the code, you might encounter situations where loading becomes slower than if no code splitting were happening at all. For example, lazily loading a chart delays sending the code needed to render the chart, splitting the chart code from the rest of the app. Parcel supports code splitting with React.lazy. However, if the chart loads its data after it has been initially rendered you are now waiting twice. This is a waterfall: rather than fetching the data for the chart and sending the code to render it simultaneously, you must wait for each step to complete one after the other.

Splitting code by route, when integrated with bundling and data fetching, can reduce the initial load time of your app and the time it takes for the largest visible content of the app to render (Largest Contentful Paint).

For code-splitting instructions, see your build tool docs:

Since the build tool you select only supports single page apps (SPAs), you’ll need to implement other rendering patterns like server-side rendering (SSR), static site generation (SSG), and/or React Server Components (RSC). Even if you don’t need these features at first, in the future there may be some routes that would benefit SSR, SSG or RSC.

Single-page apps (SPA) load a single HTML page and dynamically updates the page as the user interacts with the app. SPAs are easier to get started with, but they can have slower initial load times. SPAs are the default architecture for most build tools.

Streaming Server-side rendering (SSR) renders a page on the server and sends the fully rendered page to the client. SSR can improve performance, but it can be more complex to set up and maintain than a single-page app. With the addition of streaming, SSR can be very complex to set up and maintain. See Vite’s SSR guide.

Static site generation (SSG) generates static HTML files for your app at build time. SSG can improve performance, but it can be more complex to set up and maintain than server-side rendering. See Vite’s SSG guide.

React Server Components (RSC) lets you mix build-time, server-only, and interactive components in a single React tree. RSC can improve performance, but it currently requires deep expertise to set up and maintain. See Parcel’s RSC examples.

Your rendering strategies need to integrate with your router so apps built with your framework can choose the rendering strategy on a per-route level. This will enable different rendering strategies without having to rewrite your whole app. For example, the landing page for your app might benefit from being statically generated (SSG), while a page with a content feed might perform best with server-side rendering.

Using the right rendering strategy for the right routes can decrease the time it takes for the first byte of content to be loaded (Time to First Byte), the first piece of content to render (First Contentful Paint), and the largest visible content of the app to render (Largest Contentful Paint).

These are just a few examples of the features a new app will need to consider when building from scratch. Many limitations you’ll hit can be difficult to solve as each problem is interconnected with the others and can require deep expertise in problem areas you may not be familiar with.

If you don’t want to solve these problems on your own, you can get started with a framework that provides these features out of the box.

**Examples:**

Example 1 (python):
```python
npm create vite@latest my-app -- --template react-ts
```

Example 2 (unknown):
```unknown
npm install --save-dev parcel
```

Example 3 (unknown):
```unknown
npx create-rsbuild --template react
```

---

## Choosing the State Structure

**URL:** https://react.dev/learn/choosing-the-state-structure

**Contents:**
- Choosing the State Structure
  - You will learn
- Principles for structuring state
- Group related state
  - Pitfall
- Avoid contradictions in state
- Avoid redundant state
      - Deep Dive
    - Don’t mirror props in state
- Avoid duplication in state

Structuring state well can make a difference between a component that is pleasant to modify and debug, and one that is a constant source of bugs. Here are some tips you should consider when structuring state.

When you write a component that holds some state, you’ll have to make choices about how many state variables to use and what the shape of their data should be. While it’s possible to write correct programs even with a suboptimal state structure, there are a few principles that can guide you to make better choices:

The goal behind these principles is to make state easy to update without introducing mistakes. Removing redundant and duplicate data from state helps ensure that all its pieces stay in sync. This is similar to how a database engineer might want to “normalize” the database structure to reduce the chance of bugs. To paraphrase Albert Einstein, “Make your state as simple as it can be—but no simpler.”

Now let’s see how these principles apply in action.

You might sometimes be unsure between using a single or multiple state variables.

Technically, you can use either of these approaches. But if some two state variables always change together, it might be a good idea to unify them into a single state variable. Then you won’t forget to always keep them in sync, like in this example where moving the cursor updates both coordinates of the red dot:

Another case where you’ll group data into an object or an array is when you don’t know how many pieces of state you’ll need. For example, it’s helpful when you have a form where the user can add custom fields.

If your state variable is an object, remember that you can’t update only one field in it without explicitly copying the other fields. For example, you can’t do setPosition({ x: 100 }) in the above example because it would not have the y property at all! Instead, if you wanted to set x alone, you would either do setPosition({ ...position, x: 100 }), or split them into two state variables and do setX(100).

Here is a hotel feedback form with isSending and isSent state variables:

While this code works, it leaves the door open for “impossible” states. For example, if you forget to call setIsSent and setIsSending together, you may end up in a situation where both isSending and isSent are true at the same time. The more complex your component is, the harder it is to understand what happened.

Since isSending and isSent should never be true at the same time, it is better to replace them with one status state variable that may take one of three valid states: 'typing' (initial), 'sending', and 'sent':

You can still declare some constants for readability:

But they’re not state variables, so you don’t need to worry about them getting out of sync with each other.

If you can calculate some information from the component’s props or its existing state variables during rendering, you should not put that information into that component’s state.

For example, take this form. It works, but can you find any redundant state in it?

This form has three state variables: firstName, lastName, and fullName. However, fullName is redundant. You can always calculate fullName from firstName and lastName during render, so remove it from state.

This is how you can do it:

Here, fullName is not a state variable. Instead, it’s calculated during render:

As a result, the change handlers don’t need to do anything special to update it. When you call setFirstName or setLastName, you trigger a re-render, and then the next fullName will be calculated from the fresh data.

A common example of redundant state is code like this:

Here, a color state variable is initialized to the messageColor prop. The problem is that if the parent component passes a different value of messageColor later (for example, 'red' instead of 'blue'), the color state variable would not be updated! The state is only initialized during the first render.

This is why “mirroring” some prop in a state variable can lead to confusion. Instead, use the messageColor prop directly in your code. If you want to give it a shorter name, use a constant:

This way it won’t get out of sync with the prop passed from the parent component.

”Mirroring” props into state only makes sense when you want to ignore all updates for a specific prop. By convention, start the prop name with initial or default to clarify that its new values are ignored:

This menu list component lets you choose a single travel snack out of several:

Currently, it stores the selected item as an object in the selectedItem state variable. However, this is not great: the contents of the selectedItem is the same object as one of the items inside the items list. This means that the information about the item itself is duplicated in two places.

Why is this a problem? Let’s make each item editable:

Notice how if you first click “Choose” on an item and then edit it, the input updates but the label at the bottom does not reflect the edits. This is because you have duplicated state, and you forgot to update selectedItem.

Although you could update selectedItem too, an easier fix is to remove duplication. In this example, instead of a selectedItem object (which creates a duplication with objects inside items), you hold the selectedId in state, and then get the selectedItem by searching the items array for an item with that ID:

The state used to be duplicated like this:

But after the change it’s like this:

The duplication is gone, and you only keep the essential state!

Now if you edit the selected item, the message below will update immediately. This is because setItems triggers a re-render, and items.find(...) would find the item with the updated title. You didn’t need to hold the selected item in state, because only the selected ID is essential. The rest could be calculated during render.

Imagine a travel plan consisting of planets, continents, and countries. You might be tempted to structure its state using nested objects and arrays, like in this example:

Now let’s say you want to add a button to delete a place you’ve already visited. How would you go about it? Updating nested state involves making copies of objects all the way up from the part that changed. Deleting a deeply nested place would involve copying its entire parent place chain. Such code can be very verbose.

If the state is too nested to update easily, consider making it “flat”. Here is one way you can restructure this data. Instead of a tree-like structure where each place has an array of its child places, you can have each place hold an array of its child place IDs. Then store a mapping from each place ID to the corresponding place.

This data restructuring might remind you of seeing a database table:

Now that the state is “flat” (also known as “normalized”), updating nested items becomes easier.

In order to remove a place now, you only need to update two levels of state:

Here is an example of how you could go about it:

You can nest state as much as you like, but making it “flat” can solve numerous problems. It makes state easier to update, and it helps ensure you don’t have duplication in different parts of a nested object.

Ideally, you would also remove the deleted items (and their children!) from the “table” object to improve memory usage. This version does that. It also uses Immer to make the update logic more concise.

Sometimes, you can also reduce state nesting by moving some of the nested state into the child components. This works well for ephemeral UI state that doesn’t need to be stored, like whether an item is hovered.

This Clock component receives two props: color and time. When you select a different color in the select box, the Clock component receives a different color prop from its parent component. However, for some reason, the displayed color doesn’t update. Why? Fix the problem.

**Examples:**

Example 1 (jsx):
```jsx
const [x, setX] = useState(0);const [y, setY] = useState(0);
```

Example 2 (jsx):
```jsx
const [position, setPosition] = useState({ x: 0, y: 0 });
```

Example 3 (javascript):
```javascript
const isSending = status === 'sending';const isSent = status === 'sent';
```

Example 4 (javascript):
```javascript
const fullName = firstName + ' ' + lastName;
```

---

## Conditional Rendering

**URL:** https://react.dev/learn/conditional-rendering

**Contents:**
- Conditional Rendering
  - You will learn
- Conditionally returning JSX
  - Conditionally returning nothing with null
- Conditionally including JSX
  - Conditional (ternary) operator (? :)
      - Deep Dive
    - Are these two examples fully equivalent?
  - Logical AND operator (&&)
  - Pitfall

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statements, &&, and ? : operators.

Let’s say you have a PackingList component rendering several Items, which can be marked as packed or not:

Notice that some of the Item components have their isPacked prop set to true instead of false. You want to add a checkmark (✅) to packed items if isPacked={true}.

You can write this as an if/else statement like so:

If the isPacked prop is true, this code returns a different JSX tree. With this change, some of the items get a checkmark at the end:

Try editing what gets returned in either case, and see how the result changes!

Notice how you’re creating branching logic with JavaScript’s if and return statements. In React, control flow (like conditions) is handled by JavaScript.

In some situations, you won’t want to render anything at all. For example, say you don’t want to show packed items at all. A component must return something. In this case, you can return null:

If isPacked is true, the component will return nothing, null. Otherwise, it will return JSX to render.

In practice, returning null from a component isn’t common because it might surprise a developer trying to render it. More often, you would conditionally include or exclude the component in the parent component’s JSX. Here’s how to do that!

In the previous example, you controlled which (if any!) JSX tree would be returned by the component. You may already have noticed some duplication in the render output:

Both of the conditional branches return <li className="item">...</li>:

While this duplication isn’t harmful, it could make your code harder to maintain. What if you want to change the className? You’d have to do it in two places in your code! In such a situation, you could conditionally include a little JSX to make your code more DRY.

JavaScript has a compact syntax for writing a conditional expression — the conditional operator or “ternary operator”.

You can read it as “if isPacked is true, then (?) render name + ' ✅', otherwise (:) render name”.

If you’re coming from an object-oriented programming background, you might assume that the two examples above are subtly different because one of them may create two different “instances” of <li>. But JSX elements aren’t “instances” because they don’t hold any internal state and aren’t real DOM nodes. They’re lightweight descriptions, like blueprints. So these two examples, in fact, are completely equivalent. Preserving and Resetting State goes into detail about how this works.

Now let’s say you want to wrap the completed item’s text into another HTML tag, like <del> to strike it out. You can add even more newlines and parentheses so that it’s easier to nest more JSX in each of the cases:

This style works well for simple conditions, but use it in moderation. If your components get messy with too much nested conditional markup, consider extracting child components to clean things up. In React, markup is a part of your code, so you can use tools like variables and functions to tidy up complex expressions.

Another common shortcut you’ll encounter is the JavaScript logical AND (&&) operator. Inside React components, it often comes up when you want to render some JSX when the condition is true, or render nothing otherwise. With &&, you could conditionally render the checkmark only if isPacked is true:

You can read this as “if isPacked, then (&&) render the checkmark, otherwise, render nothing”.

Here it is in action:

A JavaScript && expression returns the value of its right side (in our case, the checkmark) if the left side (our condition) is true. But if the condition is false, the whole expression becomes false. React considers false as a “hole” in the JSX tree, just like null or undefined, and doesn’t render anything in its place.

Don’t put numbers on the left side of &&.

To test the condition, JavaScript converts the left side to a boolean automatically. However, if the left side is 0, then the whole expression gets that value (0), and React will happily render 0 rather than nothing.

For example, a common mistake is to write code like messageCount && <p>New messages</p>. It’s easy to assume that it renders nothing when messageCount is 0, but it really renders the 0 itself!

To fix it, make the left side a boolean: messageCount > 0 && <p>New messages</p>.

When the shortcuts get in the way of writing plain code, try using an if statement and a variable. You can reassign variables defined with let, so start by providing the default content you want to display, the name:

Use an if statement to reassign a JSX expression to itemContent if isPacked is true:

Curly braces open the “window into JavaScript”. Embed the variable with curly braces in the returned JSX tree, nesting the previously calculated expression inside of JSX:

This style is the most verbose, but it’s also the most flexible. Here it is in action:

Like before, this works not only for text, but for arbitrary JSX too:

If you’re not familiar with JavaScript, this variety of styles might seem overwhelming at first. However, learning them will help you read and write any JavaScript code — and not just React components! Pick the one you prefer for a start, and then consult this reference again if you forget how the other ones work.

Use the conditional operator (cond ? a : b) to render a ❌ if isPacked isn’t true.

**Examples:**

Example 1 (jsx):
```jsx
if (isPacked) {  return <li className="item">{name} ✅</li>;}return <li className="item">{name}</li>;
```

Example 2 (jsx):
```jsx
if (isPacked) {  return null;}return <li className="item">{name}</li>;
```

Example 3 (jsx):
```jsx
<li className="item">{name} ✅</li>
```

Example 4 (jsx):
```jsx
<li className="item">{name}</li>
```

---

## Creating a React App

**URL:** https://react.dev/learn/creating-a-react-app

**Contents:**
- Creating a React App
- Full-stack frameworks
  - Note
    - Full-stack frameworks do not require a server.
  - Next.js (App Router)
  - React Router (v7)
  - Expo (for native apps)
- Other frameworks
      - Deep Dive
    - Which features make up the React team’s full-stack architecture vision?

If you want to build a new app or website with React, we recommend starting with a framework.

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, you can build a React app from scratch.

These recommended frameworks support all the features you need to deploy and scale your app in production. They have integrated the latest React features and take advantage of React’s architecture.

All the frameworks on this page support client-side rendering (CSR), single-page apps (SPA), and static-site generation (SSG). These apps can be deployed to a CDN or static hosting service without a server. Additionally, these frameworks allow you to add server-side rendering on a per-route basis, when it makes sense for your use case.

This allows you to start with a client-only app, and if your needs change later, you can opt-in to using server features on individual routes without rewriting your app. See your framework’s documentation for configuring the rendering strategy.

Next.js’s App Router is a React framework that takes full advantage of React’s architecture to enable full-stack React apps.

Next.js is maintained by Vercel. You can deploy a Next.js app to any hosting provider that supports Node.js or Docker containers, or to your own server. Next.js also supports static export which doesn’t require a server.

React Router is the most popular routing library for React and can be paired with Vite to create a full-stack React framework. It emphasizes standard Web APIs and has several ready to deploy templates for various JavaScript runtimes and platforms.

To create a new React Router framework project, run:

React Router is maintained by Shopify.

Expo is a React framework that lets you create universal Android, iOS, and web apps with truly native UIs. It provides an SDK for React Native that makes the native parts easier to use. To create a new Expo project, run:

If you’re new to Expo, check out the Expo tutorial.

Expo is maintained by Expo (the company). Building apps with Expo is free, and you can submit them to the Google and Apple app stores without restrictions. Expo additionally provides opt-in paid cloud services.

There are other up-and-coming frameworks that are working towards our full stack React vision:

Next.js’s App Router bundler fully implements the official React Server Components specification. This lets you mix build-time, server-only, and interactive components in a single React tree.

For example, you can write a server-only React component as an async function that reads from a database or from a file. Then you can pass data down from it to your interactive components:

Next.js’s App Router also integrates data fetching with Suspense. This lets you specify a loading state (like a skeleton placeholder) for different parts of your user interface directly in your React tree:

Server Components and Suspense are React features rather than Next.js features. However, adopting them at the framework level requires buy-in and non-trivial implementation work. At the moment, the Next.js App Router is the most complete implementation. The React team is working with bundler developers to make these features easier to implement in the next generation of frameworks.

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, there are other options available for starting a React project from scratch.

Starting from scratch gives you more flexibility, but does require that you make choices on which tools to use for routing, data fetching, and other common usage patterns. It’s a lot like building your own framework, instead of using a framework that already exists. The frameworks we recommend have built-in solutions for these problems.

If you want to build your own solutions, see our guide to build a React app from Scratch for instructions on how to set up a new React project starting with a build tool like Vite, Parcel, or RSbuild.

If you’re a framework author interested in being included on this page, please let us know.

**Examples:**

Example 1 (python):
```python
npx create-next-app@latest
```

Example 2 (python):
```python
npx create-react-router@latest
```

Example 3 (python):
```python
npx create-expo-app@latest
```

Example 4 (javascript):
```javascript
// This component runs *only* on the server (or during the build).async function Talks({ confId }) {  // 1. You're on the server, so you can talk to your data layer. API endpoint not required.  const talks = await db.Talks.findAll({ confId });  // 2. Add any amount of rendering logic. It won't make your JavaScript bundle larger.  const videos = talks.map(talk => talk.video);  // 3. Pass the data down to the components that will run in the browser.  return <SearchableVideoList videos={videos} />;}
```

---

## Debugging and Troubleshooting

**URL:** https://react.dev/learn/react-compiler/debugging

**Contents:**
- Debugging and Troubleshooting
  - You will learn
- Understanding Compiler Behavior
  - Compiler Errors vs Runtime Issues
- Common Breaking Patterns
- Debugging Workflow
  - Compiler Build Errors
  - Runtime Issues
  - 1. Temporarily Disable Compilation
  - 2. Fix Issues Step by Step

This guide helps you identify and fix issues when using React Compiler. Learn how to debug compilation problems and resolve common issues.

React Compiler is designed to handle code that follows the Rules of React. When it encounters code that might break these rules, it safely skips optimization rather than risk changing your app’s behavior.

Compiler errors occur at build time and prevent your code from compiling. These are rare because the compiler is designed to skip problematic code rather than fail.

Runtime issues occur when compiled code behaves differently than expected. Most of the time, if you encounter an issue with React Compiler, it’s a runtime issue. This typically happens when your code violates the Rules of React in subtle ways that the compiler couldn’t detect, and the compiler mistakenly compiled a component it should have skipped.

When debugging runtime issues, focus your efforts on finding Rules of React violations in the affected components that were not detected by the ESLint rule. The compiler relies on your code following these rules, and when they’re broken in ways it can’t detect, that’s when runtime problems occur.

One of the main ways React Compiler can break your app is if your code was written to rely on memoization for correctness. This means your app depends on specific values being memoized to work properly. Since the compiler may memoize differently than your manual approach, this can lead to unexpected behavior like effects over-firing, infinite loops, or missing updates.

Common scenarios where this occurs:

Follow these steps when you encounter issues:

If you encounter a compiler error that unexpectedly breaks your build, this is likely a bug in the compiler. Report it to the facebook/react repository with:

For runtime behavior issues:

Use "use no memo" to isolate whether an issue is compiler-related:

If the issue disappears, it’s likely related to a Rules of React violation.

You can also try removing manual memoization (useMemo, useCallback, memo) from the problematic component to verify that your app works correctly without any memoization. If the bug still occurs when all memoization is removed, you have a Rules of React violation that needs to be fixed.

If you believe you’ve found a compiler bug:

**Examples:**

Example 1 (javascript):
```javascript
function ProblematicComponent() {  "use no memo"; // Skip compilation for this component  // ... rest of component}
```

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui

**Contents:**
- Describing the UI
  - In this chapter
- Your first component
- Ready to learn this topic?
- Importing and exporting components
- Ready to learn this topic?
- Writing markup with JSX
- Ready to learn this topic?
- JavaScript in JSX with curly braces
- Ready to learn this topic?

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable components. From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.

React applications are built from isolated pieces of UI called components. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button, or as large as an entire page. Here is a Gallery component rendering three Profile components:

Read Your First Component to learn how to declare and use React components.

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can export a component into its own file, and then import that component from another file:

Read Importing and Exporting Components to learn how to split components into their own files.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If we paste existing HTML markup into a React component, it won’t always work:

If you have existing HTML like this, you can fix it using a converter:

Read Writing Markup with JSX to learn how to write valid JSX.

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to “open a window” to JavaScript:

Read JavaScript in JSX with Curly Braces to learn how to access JavaScript data from JSX.

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

Read Passing Props to a Component to learn how to pass and read props.

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statements, &&, and ? : operators.

In this example, the JavaScript && operator is used to conditionally render a checkmark:

Read Conditional Rendering to learn the different ways to render content conditionally.

You will often want to display multiple similar components from a collection of data. You can use JavaScript’s filter() and map() with React to filter and transform your array of data into an array of components.

For each array item, you will need to specify a key. Usually, you will want to use an ID from the database as a key. Keys let React keep track of each item’s place in the list even if the list changes.

Read Rendering Lists to learn how to render a list of components, and how to choose a key.

Some JavaScript functions are pure. A pure function:

By strictly only writing your components as pure functions, you can avoid an entire class of baffling bugs and unpredictable behavior as your codebase grows. Here is an example of an impure component:

You can make this component pure by passing a prop instead of modifying a preexisting variable:

Read Keeping Components Pure to learn how to write components as pure, predictable functions.

React uses trees to model the relationships between components and modules.

A React render tree is a representation of the parent and child relationship between components.

An example React render tree.

Components near the top of the tree, near the root component, are considered top-level components. Components with no child components are leaf components. This categorization of components is useful for understanding data flow and rendering performance.

Modelling the relationship between JavaScript modules is another useful way to understand your app. We refer to it as a module dependency tree.

An example module dependency tree.

A dependency tree is often used by build tools to bundle all the relevant JavaScript code for the client to download and render. A large bundle size regresses user experience for React apps. Understanding the module dependency tree is helpful to debug such issues.

Read Your UI as a Tree to learn how to create a render and module dependency trees for a React app and how they’re useful mental models for improving user experience and performance.

Head over to Your First Component to start reading this chapter page by page!

Or, if you’re already familiar with these topics, why not read about Adding Interactivity?

---

## Editor Setup

**URL:** https://react.dev/learn/editor-setup

**Contents:**
- Editor Setup
  - You will learn
- Your editor
- Recommended text editor features
  - Linting
  - Formatting
    - Formatting on save

A properly configured editor can make code clearer to read and faster to write. It can even help you catch bugs as you write them! If this is your first time setting up an editor or you’re looking to tune up your current editor, we have a few recommendations.

VS Code is one of the most popular editors in use today. It has a large marketplace of extensions and integrates well with popular services like GitHub. Most of the features listed below can be added to VS Code as extensions as well, making it highly configurable!

Other popular text editors used in the React community include:

Some editors come with these features built in, but others might require adding an extension. Check to see what support your editor of choice provides to be sure!

Code linters find problems in your code as you write, helping you fix them early. ESLint is a popular, open source linter for JavaScript.

Make sure that you’ve enabled all the eslint-plugin-react-hooks rules for your project. They are essential and catch the most severe bugs early. The recommended eslint-config-react-app preset already includes them.

The last thing you want to do when sharing your code with another contributor is get into a discussion about tabs vs spaces! Fortunately, Prettier will clean up your code by reformatting it to conform to preset, configurable rules. Run Prettier, and all your tabs will be converted to spaces—and your indentation, quotes, etc will also all be changed to conform to the configuration. In the ideal setup, Prettier will run when you save your file, quickly making these edits for you.

You can install the Prettier extension in VSCode by following these steps:

Ideally, you should format your code on every save. VS Code has settings for this!

If your ESLint preset has formatting rules, they may conflict with Prettier. We recommend disabling all formatting rules in your ESLint preset using eslint-config-prettier so that ESLint is only used for catching logical mistakes. If you want to enforce that files are formatted before a pull request is merged, use prettier --check for your continuous integration.

---

## Escape Hatches

**URL:** https://react.dev/learn/escape-hatches

**Contents:**
- Escape Hatches
  - In this chapter
- Referencing values with refs
- Ready to learn this topic?
- Manipulating the DOM with refs
- Ready to learn this topic?
- Synchronizing with Effects
- Ready to learn this topic?
- You Might Not Need An Effect
- Ready to learn this topic?

Some of your components may need to control and synchronize with systems outside of React. For example, you might need to focus an input using the browser API, play and pause a video player implemented without React, or connect and listen to messages from a remote server. In this chapter, you’ll learn the escape hatches that let you “step outside” React and connect to external systems. Most of your application logic and data flow should not rely on these features.

When you want a component to “remember” some information, but you don’t want that information to trigger new renders, you can use a ref:

Like state, refs are retained by React between re-renders. However, setting state re-renders a component. Changing a ref does not! You can access the current value of that ref through the ref.current property.

A ref is like a secret pocket of your component that React doesn’t track. For example, you can use refs to store timeout IDs, DOM elements, and other objects that don’t impact the component’s rendering output.

Read Referencing Values with Refs to learn how to use refs to remember information.

React automatically updates the DOM to match your render output, so your components won’t often need to manipulate it. However, sometimes you might need access to the DOM elements managed by React—for example, to focus a node, scroll to it, or measure its size and position. There is no built-in way to do those things in React, so you will need a ref to the DOM node. For example, clicking the button will focus the input using a ref:

Read Manipulating the DOM with Refs to learn how to access DOM elements managed by React.

Some components need to synchronize with external systems. For example, you might want to control a non-React component based on the React state, set up a server connection, or send an analytics log when a component appears on the screen. Unlike event handlers, which let you handle particular events, Effects let you run some code after rendering. Use them to synchronize your component with a system outside of React.

Press Play/Pause a few times and see how the video player stays synchronized to the isPlaying prop value:

Many Effects also “clean up” after themselves. For example, an Effect that sets up a connection to a chat server should return a cleanup function that tells React how to disconnect your component from that server:

In development, React will immediately run and clean up your Effect one extra time. This is why you see "✅ Connecting..." printed twice. This ensures that you don’t forget to implement the cleanup function.

Read Synchronizing with Effects to learn how to synchronize components with external systems.

Effects are an escape hatch from the React paradigm. They let you “step outside” of React and synchronize your components with some external system. If there is no external system involved (for example, if you want to update a component’s state when some props or state change), you shouldn’t need an Effect. Removing unnecessary Effects will make your code easier to follow, faster to run, and less error-prone.

There are two common cases in which you don’t need Effects:

For example, you don’t need an Effect to adjust some state based on other state:

Instead, calculate as much as you can while rendering:

However, you do need Effects to synchronize with external systems.

Read You Might Not Need an Effect to learn how to remove unnecessary Effects.

Effects have a different lifecycle from components. Components may mount, update, or unmount. An Effect can only do two things: to start synchronizing something, and later to stop synchronizing it. This cycle can happen multiple times if your Effect depends on props and state that change over time.

This Effect depends on the value of the roomId prop. Props are reactive values, which means they can change on a re-render. Notice that the Effect re-synchronizes (and re-connects to the server) if roomId changes:

React provides a linter rule to check that you’ve specified your Effect’s dependencies correctly. If you forget to specify roomId in the list of dependencies in the above example, the linter will find that bug automatically.

Read Lifecycle of Reactive Events to learn how an Effect’s lifecycle is different from a component’s.

Event handlers only re-run when you perform the same interaction again. Unlike event handlers, Effects re-synchronize if any of the values they read, like props or state, are different than during last render. Sometimes, you want a mix of both behaviors: an Effect that re-runs in response to some values but not others.

All code inside Effects is reactive. It will run again if some reactive value it reads has changed due to a re-render. For example, this Effect will re-connect to the chat if either roomId or theme have changed:

This is not ideal. You want to re-connect to the chat only if the roomId has changed. Switching the theme shouldn’t re-connect to the chat! Move the code reading theme out of your Effect into an Effect Event:

Code inside Effect Events isn’t reactive, so changing the theme no longer makes your Effect re-connect.

Read Separating Events from Effects to learn how to prevent some values from re-triggering Effects.

When you write an Effect, the linter will verify that you’ve included every reactive value (like props and state) that the Effect reads in the list of your Effect’s dependencies. This ensures that your Effect remains synchronized with the latest props and state of your component. Unnecessary dependencies may cause your Effect to run too often, or even create an infinite loop. The way you remove them depends on the case.

For example, this Effect depends on the options object which gets re-created every time you edit the input:

You don’t want the chat to re-connect every time you start typing a message in that chat. To fix this problem, move creation of the options object inside the Effect so that the Effect only depends on the roomId string:

Notice that you didn’t start by editing the dependency list to remove the options dependency. That would be wrong. Instead, you changed the surrounding code so that the dependency became unnecessary. Think of the dependency list as a list of all the reactive values used by your Effect’s code. You don’t intentionally choose what to put on that list. The list describes your code. To change the dependency list, change the code.

Read Removing Effect Dependencies to learn how to make your Effect re-run less often.

React comes with built-in Hooks like useState, useContext, and useEffect. Sometimes, you’ll wish that there was a Hook for some more specific purpose: for example, to fetch data, to keep track of whether the user is online, or to connect to a chat room. To do this, you can create your own Hooks for your application’s needs.

In this example, the usePointerPosition custom Hook tracks the cursor position, while useDelayedValue custom Hook returns a value that’s “lagging behind” the value you passed by a certain number of milliseconds. Move the cursor over the sandbox preview area to see a moving trail of dots following the cursor:

You can create custom Hooks, compose them together, pass data between them, and reuse them between components. As your app grows, you will write fewer Effects by hand because you’ll be able to reuse custom Hooks you already wrote. There are also many excellent custom Hooks maintained by the React community.

Read Reusing Logic with Custom Hooks to learn how to share logic between components.

Head over to Referencing Values with Refs to start reading this chapter page by page!

**Examples:**

Example 1 (jsx):
```jsx
const ref = useRef(0);
```

Example 2 (jsx):
```jsx
function Form() {  const [firstName, setFirstName] = useState('Taylor');  const [lastName, setLastName] = useState('Swift');  // 🔴 Avoid: redundant state and unnecessary Effect  const [fullName, setFullName] = useState('');  useEffect(() => {    setFullName(firstName + ' ' + lastName);  }, [firstName, lastName]);  // ...}
```

Example 3 (javascript):
```javascript
function Form() {  const [firstName, setFirstName] = useState('Taylor');  const [lastName, setLastName] = useState('Swift');  // ✅ Good: calculated during rendering  const fullName = firstName + ' ' + lastName;  // ...}
```

---

## Extracting State Logic into a Reducer

**URL:** https://react.dev/learn/extracting-state-logic-into-a-reducer

**Contents:**
- Extracting State Logic into a Reducer
  - You will learn
- Consolidate state logic with a reducer
  - Step 1: Move from setting state to dispatching actions
  - Note
  - Step 2: Write a reducer function
  - Note
      - Deep Dive
    - Why are reducers called this way?
  - Step 3: Use the reducer from your component

Components with many state updates spread across many event handlers can get overwhelming. For these cases, you can consolidate all the state update logic outside your component in a single function, called a reducer.

As your components grow in complexity, it can get harder to see at a glance all the different ways in which a component’s state gets updated. For example, the TaskApp component below holds an array of tasks in state and uses three different event handlers to add, remove, and edit tasks:

Each of its event handlers calls setTasks in order to update the state. As this component grows, so does the amount of state logic sprinkled throughout it. To reduce this complexity and keep all your logic in one easy-to-access place, you can move that state logic into a single function outside your component, called a “reducer”.

Reducers are a different way to handle state. You can migrate from useState to useReducer in three steps:

Your event handlers currently specify what to do by setting state:

Remove all the state setting logic. What you are left with are three event handlers:

Managing state with reducers is slightly different from directly setting state. Instead of telling React “what to do” by setting state, you specify “what the user just did” by dispatching “actions” from your event handlers. (The state update logic will live elsewhere!) So instead of “setting tasks” via an event handler, you’re dispatching an “added/changed/deleted a task” action. This is more descriptive of the user’s intent.

The object you pass to dispatch is called an “action”:

It is a regular JavaScript object. You decide what to put in it, but generally it should contain the minimal information about what happened. (You will add the dispatch function itself in a later step.)

An action object can have any shape.

By convention, it is common to give it a string type that describes what happened, and pass any additional information in other fields. The type is specific to a component, so in this example either 'added' or 'added_task' would be fine. Choose a name that says what happened!

A reducer function is where you will put your state logic. It takes two arguments, the current state and the action object, and it returns the next state:

React will set the state to what you return from the reducer.

To move your state setting logic from your event handlers to a reducer function in this example, you will:

Here is all the state setting logic migrated to a reducer function:

Because the reducer function takes state (tasks) as an argument, you can declare it outside of your component. This decreases the indentation level and can make your code easier to read.

The code above uses if/else statements, but it’s a convention to use switch statements inside reducers. The result is the same, but it can be easier to read switch statements at a glance.

We’ll be using them throughout the rest of this documentation like so:

We recommend wrapping each case block into the { and } curly braces so that variables declared inside of different cases don’t clash with each other. Also, a case should usually end with a return. If you forget to return, the code will “fall through” to the next case, which can lead to mistakes!

If you’re not yet comfortable with switch statements, using if/else is completely fine.

Although reducers can “reduce” the amount of code inside your component, they are actually named after the reduce() operation that you can perform on arrays.

The reduce() operation lets you take an array and “accumulate” a single value out of many:

The function you pass to reduce is known as a “reducer”. It takes the result so far and the current item, then it returns the next result. React reducers are an example of the same idea: they take the state so far and the action, and return the next state. In this way, they accumulate actions over time into state.

You could even use the reduce() method with an initialState and an array of actions to calculate the final state by passing your reducer function to it:

You probably won’t need to do this yourself, but this is similar to what React does!

Finally, you need to hook up the tasksReducer to your component. Import the useReducer Hook from React:

Then you can replace useState:

with useReducer like so:

The useReducer Hook is similar to useState—you must pass it an initial state and it returns a stateful value and a way to set state (in this case, the dispatch function). But it’s a little different.

The useReducer Hook takes two arguments:

Now it’s fully wired up! Here, the reducer is declared at the bottom of the component file:

If you want, you can even move the reducer to a different file:

Component logic can be easier to read when you separate concerns like this. Now the event handlers only specify what happened by dispatching actions, and the reducer function determines how the state updates in response to them.

Reducers are not without downsides! Here’s a few ways you can compare them:

We recommend using a reducer if you often encounter bugs due to incorrect state updates in some component, and want to introduce more structure to its code. You don’t have to use reducers for everything: feel free to mix and match! You can even useState and useReducer in the same component.

Keep these two tips in mind when writing reducers:

Just like with updating objects and arrays in regular state, you can use the Immer library to make reducers more concise. Here, useImmerReducer lets you mutate the state with push or arr[i] = assignment:

Reducers must be pure, so they shouldn’t mutate state. But Immer provides you with a special draft object which is safe to mutate. Under the hood, Immer will create a copy of your state with the changes you made to the draft. This is why reducers managed by useImmerReducer can mutate their first argument and don’t need to return state.

Currently, the event handlers in ContactList.js and Chat.js have // TODO comments. This is why typing into the input doesn’t work, and clicking on the buttons doesn’t change the selected recipient.

Replace these two // TODOs with the code to dispatch the corresponding actions. To see the expected shape and the type of the actions, check the reducer in messengerReducer.js. The reducer is already written so you won’t need to change it. You only need to dispatch the actions in ContactList.js and Chat.js.

**Examples:**

Example 1 (javascript):
```javascript
function handleAddTask(text) {  setTasks([    ...tasks,    {      id: nextId++,      text: text,      done: false,    },  ]);}function handleChangeTask(task) {  setTasks(    tasks.map((t) => {      if (t.id === task.id) {        return task;      } else {        return t;      }    })  );}function handleDeleteTask(taskId) {  setTasks(tasks.filter((t) => t.id !== taskId));}
```

Example 2 (javascript):
```javascript
function handleAddTask(text) {  dispatch({    type: 'added',    id: nextId++,    text: text,  });}function handleChangeTask(task) {  dispatch({    type: 'changed',    task: task,  });}function handleDeleteTask(taskId) {  dispatch({    type: 'deleted',    id: taskId,  });}
```

Example 3 (javascript):
```javascript
function handleDeleteTask(taskId) {  dispatch(    // "action" object:    {      type: 'deleted',      id: taskId,    }  );}
```

Example 4 (unknown):
```unknown
dispatch({  // specific to component  type: 'what_happened',  // other fields go here});
```

---

## Importing and Exporting Components

**URL:** https://react.dev/learn/importing-and-exporting-components

**Contents:**
- Importing and Exporting Components
  - You will learn
- The root component file
- Exporting and importing a component
  - Note
      - Deep Dive
    - Default vs named exports
- Exporting and importing multiple components from the same file
  - Note
- Recap

The magic of components lies in their reusability: you can create components that are composed of other components. But as you nest more and more components, it often makes sense to start splitting them into different files. This lets you keep your files easy to scan and reuse components in more places.

In Your First Component, you made a Profile component and a Gallery component that renders it:

These currently live in a root component file, named App.js in this example. Depending on your setup, your root component could be in another file, though. If you use a framework with file-based routing, such as Next.js, your root component will be different for every page.

What if you want to change the landing screen in the future and put a list of science books there? Or place all the profiles somewhere else? It makes sense to move Gallery and Profile out of the root component file. This will make them more modular and reusable in other files. You can move a component in three steps:

Here both Profile and Gallery have been moved out of App.js into a new file called Gallery.js. Now you can change App.js to import Gallery from Gallery.js:

Notice how this example is broken down into two component files now:

You may encounter files that leave off the .js file extension like so:

Either './Gallery.js' or './Gallery' will work with React, though the former is closer to how native ES Modules work.

There are two primary ways to export values with JavaScript: default exports and named exports. So far, our examples have only used default exports. But you can use one or both of them in the same file. A file can have no more than one default export, but it can have as many named exports as you like.

How you export your component dictates how you must import it. You will get an error if you try to import a default export the same way you would a named export! This chart can help you keep track:

When you write a default import, you can put any name you want after import. For example, you could write import Banana from './Button.js' instead and it would still provide you with the same default export. In contrast, with named imports, the name has to match on both sides. That’s why they are called named imports!

People often use default exports if the file exports only one component, and use named exports if it exports multiple components and values. Regardless of which coding style you prefer, always give meaningful names to your component functions and the files that contain them. Components without names, like export default () => {}, are discouraged because they make debugging harder.

What if you want to show just one Profile instead of a gallery? You can export the Profile component, too. But Gallery.js already has a default export, and you can’t have two default exports. You could create a new file with a default export, or you could add a named export for Profile. A file can only have one default export, but it can have numerous named exports!

To reduce the potential confusion between default and named exports, some teams choose to only stick to one style (default or named), or avoid mixing them in a single file. Do what works best for you!

First, export Profile from Gallery.js using a named export (no default keyword):

Then, import Profile from Gallery.js to App.js using a named import (with the curly braces):

Finally, render <Profile /> from the App component:

Now Gallery.js contains two exports: a default Gallery export, and a named Profile export. App.js imports both of them. Try editing <Profile /> to <Gallery /> and back in this example:

Now you’re using a mix of default and named exports:

On this page you learned:

Currently, Gallery.js exports both Profile and Gallery, which is a bit confusing.

Move the Profile component to its own Profile.js, and then change the App component to render both <Profile /> and <Gallery /> one after another.

You may use either a default or a named export for Profile, but make sure that you use the corresponding import syntax in both App.js and Gallery.js! You can refer to the table from the deep dive above:

After you get it working with one kind of exports, make it work with the other kind.

**Examples:**

Example 1 (sql):
```sql
import Gallery from './Gallery';
```

Example 2 (javascript):
```javascript
export function Profile() {  // ...}
```

Example 3 (sql):
```sql
import { Profile } from './Gallery.js';
```

Example 4 (jsx):
```jsx
export default function App() {  return <Profile />;}
```

---

## Incremental Adoption

**URL:** https://react.dev/learn/react-compiler/incremental-adoption

**Contents:**
- Incremental Adoption
  - You will learn
- Why Incremental Adoption?
- Approaches to Incremental Adoption
- Directory-Based Adoption with Babel Overrides
  - Basic Configuration
  - Expanding Coverage
  - With Compiler Options
- Opt-in Mode with “use memo”
  - Note

React Compiler can be adopted incrementally, allowing you to try it on specific parts of your codebase first. This guide shows you how to gradually roll out the compiler in existing projects.

React Compiler is designed to optimize your entire codebase automatically, but you don’t have to adopt it all at once. Incremental adoption gives you control over the rollout process, letting you test the compiler on small parts of your app before expanding to the rest.

Starting small helps you build confidence in the compiler’s optimizations. You can verify that your app behaves correctly with compiled code, measure performance improvements, and identify any edge cases specific to your codebase. This approach is especially valuable for production applications where stability is critical.

Incremental adoption also makes it easier to address any Rules of React violations the compiler might find. Instead of fixing violations across your entire codebase at once, you can tackle them systematically as you expand compiler coverage. This keeps the migration manageable and reduces the risk of introducing bugs.

By controlling which parts of your code get compiled, you can also run A/B tests to measure the real-world impact of the compiler’s optimizations. This data helps you make informed decisions about full adoption and demonstrates the value to your team.

There are three main approaches to adopt React Compiler incrementally:

All approaches allow you to test the compiler on specific parts of your application before full rollout.

Babel’s overrides option lets you apply different plugins to different parts of your codebase. This is ideal for gradually adopting React Compiler directory by directory.

Start by applying the compiler to a specific directory:

As you gain confidence, add more directories:

You can also configure compiler options per override:

For maximum control, you can use compilationMode: 'annotation' to only compile components and hooks that explicitly opt in with the "use memo" directive.

This approach gives you fine-grained control over individual components and hooks. It’s useful when you want to test the compiler on specific components without affecting entire directories.

Add "use memo" at the beginning of functions you want to compile:

With compilationMode: 'annotation', you must:

This gives you precise control over which components are compiled while you evaluate the compiler’s impact.

The gating option enables you to control compilation at runtime using feature flags. This is useful for running A/B tests or gradually rolling out the compiler based on user segments.

The compiler wraps optimized code in a runtime check. If the gate returns true, the optimized version runs. Otherwise, the original code runs.

Create a module that exports your gating function:

If you encounter issues during adoption:

**Examples:**

Example 1 (css):
```css
// babel.config.jsmodule.exports = {  plugins: [    // Global plugins that apply to all files  ],  overrides: [    {      test: './src/modern/**/*.{js,jsx,ts,tsx}',      plugins: [        'babel-plugin-react-compiler'      ]    }  ]};
```

Example 2 (css):
```css
// babel.config.jsmodule.exports = {  plugins: [    // Global plugins  ],  overrides: [    {      test: ['./src/modern/**/*.{js,jsx,ts,tsx}', './src/features/**/*.{js,jsx,ts,tsx}'],      plugins: [        'babel-plugin-react-compiler'      ]    },    {      test: './src/legacy/**/*.{js,jsx,ts,tsx}',      plugins: [        // Different plugins for legacy code      ]    }  ]};
```

Example 3 (css):
```css
// babel.config.jsmodule.exports = {  plugins: [],  overrides: [    {      test: './src/experimental/**/*.{js,jsx,ts,tsx}',      plugins: [        ['babel-plugin-react-compiler', {          // options ...        }]      ]    },    {      test: './src/production/**/*.{js,jsx,ts,tsx}',      plugins: [        ['babel-plugin-react-compiler', {          // options ...        }]      ]    }  ]};
```

Example 4 (css):
```css
// babel.config.jsmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'annotation',    }],  ],};
```

---

## Installation

**URL:** https://react.dev/learn/react-compiler/installation

**Contents:**
- Installation
  - You will learn
- Prerequisites
- Installation
- Basic Setup
  - Pitfall
  - Babel
  - Vite
  - Next.js
  - React Router

This guide will help you install and configure React Compiler in your React application.

React Compiler is designed to work best with React 19, but it also supports React 17 and 18. Learn more about React version compatibility.

Install React Compiler as a devDependency:

React Compiler is designed to work by default without any configuration. However, if you need to configure it in special circumstances (for example, to target React versions below 19), refer to the compiler options reference.

The setup process depends on your build tool. React Compiler includes a Babel plugin that integrates with your build pipeline.

React Compiler must run first in your Babel plugin pipeline. The compiler needs the original source information for proper analysis, so it must process your code before other transformations.

Create or update your babel.config.js:

If you use Vite, you can add the plugin to vite-plugin-react:

Alternatively, if you prefer a separate Babel plugin for Vite:

Please refer to the Next.js docs for more information.

Install vite-plugin-babel, and add the compiler’s Babel plugin to it:

A community webpack loader is now available here.

Please refer to Expo’s docs to enable and use the React Compiler in Expo apps.

React Native uses Babel via Metro, so refer to the Usage with Babel section for installation instructions.

Please refer to Rspack’s docs to enable and use the React Compiler in Rspack apps.

Please refer to Rsbuild’s docs to enable and use the React Compiler in Rsbuild apps.

React Compiler includes an ESLint rule that helps identify code that can’t be optimized. When the ESLint rule reports an error, it means the compiler will skip optimizing that specific component or hook. This is safe: the compiler will continue optimizing other parts of your codebase. You don’t need to fix all violations immediately. Address them at your own pace to gradually increase the number of optimized components.

Install the ESLint plugin:

If you haven’t already configured eslint-plugin-react-hooks, follow the installation instructions in the readme. The compiler rules are available in the recommended-latest preset.

The ESLint rule will:

After installation, verify that React Compiler is working correctly.

Components optimized by React Compiler will show a “Memo ✨” badge in React DevTools:

If the compiler is working:

You can also verify the compiler is running by checking your build output. The compiled code will include automatic memoization logic that the compiler adds automatically.

If a component is causing issues after compilation, you can temporarily opt it out using the "use no memo" directive:

This tells the compiler to skip optimization for this specific component. You should fix the underlying issue and remove the directive once resolved.

For more troubleshooting help, see the debugging guide.

Now that you have React Compiler installed, learn more about:

**Examples:**

Example 1 (python):
```python
npm install -D babel-plugin-react-compiler@latest
```

Example 2 (python):
```python
yarn add -D babel-plugin-react-compiler@latest
```

Example 3 (python):
```python
pnpm install -D babel-plugin-react-compiler@latest
```

Example 4 (css):
```css
module.exports = {  plugins: [    'babel-plugin-react-compiler', // must run first!    // ... other plugins  ],  // ... other config};
```

---

## Installation

**URL:** https://react.dev/learn/installation

**Contents:**
- Installation
- Try React
- Creating a React App
- Build a React App from Scratch
- Add React to an existing project
  - Note
    - Should I use Create React App?
- Next steps

React has been designed from the start for gradual adoption. You can use as little or as much React as you need. Whether you want to get a taste of React, add some interactivity to an HTML page, or start a complex React-powered app, this section will help you get started.

You don’t need to install anything to play with React. Try editing this sandbox!

You can edit it directly or open it in a new tab by pressing the “Fork” button in the upper right corner.

Most pages in the React documentation contain sandboxes like this. Outside of the React documentation, there are many online sandboxes that support React: for example, CodeSandbox, StackBlitz, or CodePen.

To try React locally on your computer, download this HTML page. Open it in your editor and in your browser!

If you want to start a new React app, you can create a React app using a recommended framework.

If a framework is not a good fit for your project, you prefer to build your own framework, or you just want to learn the basics of a React app you can build a React app from scratch.

If want to try using React in your existing app or a website, you can add React to an existing project.

No. Create React App has been deprecated. For more information, see Sunsetting Create React App.

Head to the Quick Start guide for a tour of the most important React concepts you will encounter every day.

---

## Introduction

**URL:** https://react.dev/learn/react-compiler/introduction

**Contents:**
- Introduction
  - You will learn
- What does React Compiler do?
  - Before React Compiler
  - Note
  - After React Compiler
      - Deep Dive
    - What kind of memoization does React Compiler add?
    - Optimizing Re-renders
    - Expensive calculations also get memoized

React Compiler is a new build-time tool that automatically optimizes your React app. It works with plain JavaScript, and understands the Rules of React, so you don’t need to rewrite any code to use it.

React Compiler automatically optimizes your React application at build time. React is often fast enough without optimization, but sometimes you need to manually memoize components and values to keep your app responsive. This manual memoization is tedious, easy to get wrong, and adds extra code to maintain. React Compiler does this optimization automatically for you, freeing you from this mental burden so you can focus on building features.

Without the compiler, you need to manually memoize components and values to optimize re-renders:

This manual memoization has a subtle bug that breaks memoization:

Even though handleClick is wrapped in useCallback, the arrow function () => handleClick(item) creates a new function every time the component renders. This means that Item will always receive a new onClick prop, breaking memoization.

React Compiler is able to optimize this correctly with or without the arrow function, ensuring that Item only re-renders when props.onClick changes.

With React Compiler, you write the same code without manual memoization:

See this example in the React Compiler Playground

React Compiler automatically applies the optimal memoization, ensuring your app only re-renders when necessary.

React Compiler’s automatic memoization is primarily focused on improving update performance (re-rendering existing components), so it focuses on these two use cases:

React lets you express your UI as a function of their current state (more concretely: their props, state, and context). In its current implementation, when a component’s state changes, React will re-render that component and all of its children — unless you have applied some form of manual memoization with useMemo(), useCallback(), or React.memo(). For example, in the following example, <MessageButton> will re-render whenever <FriendList>’s state changes:

See this example in the React Compiler Playground

React Compiler automatically applies the equivalent of manual memoization, ensuring that only the relevant parts of an app re-render as state changes, which is sometimes referred to as “fine-grained reactivity”. In the above example, React Compiler determines that the return value of <FriendListCard /> can be reused even as friends changes, and can avoid recreating this JSX and avoid re-rendering <MessageButton> as the count changes.

React Compiler can also automatically memoize expensive calculations used during rendering:

See this example in the React Compiler Playground

However, if expensivelyProcessAReallyLargeArrayOfObjects is truly an expensive function, you may want to consider implementing its own memoization outside of React, because:

So if expensivelyProcessAReallyLargeArrayOfObjects was used in many different components, even if the same exact items were passed down, that expensive calculation would be run repeatedly. We recommend profiling first to see if it really is that expensive before making code more complicated.

We encourage everyone to start using React Compiler. While the compiler is still an optional addition to React today, in the future some features may require the compiler in order to fully work.

React Compiler is now stable and has been tested extensively in production. While it has been used in production at companies like Meta, rolling out the compiler to production for your app will depend on the health of your codebase and how well you’ve followed the Rules of React.

React Compiler can be installed across several build tools such as Babel, Vite, Metro, and Rsbuild.

React Compiler is primarily a light Babel plugin wrapper around the core compiler, which was designed to be decoupled from Babel itself. While the initial stable version of the compiler will remain primarily a Babel plugin, we are working with the swc and oxc teams to build first class support for React Compiler so you won’t have to add Babel back to your build pipelines in the future.

Next.js users can enable the swc-invoked React Compiler by using v15.3.1 and up.

By default, React Compiler will memoize your code based on its analysis and heuristics. In most cases, this memoization will be as precise, or moreso, than what you may have written.

However, in some cases developers may need more control over memoization. The useMemo and useCallback hooks can continue to be used with React Compiler as an escape hatch to provide control over which values are memoized. A common use-case for this is if a memoized value is used as an effect dependency, in order to ensure that an effect does not fire repeatedly even when its dependencies do not meaningfully change.

For new code, we recommend relying on the compiler for memoization and using useMemo/useCallback where needed to achieve precise control.

For existing code, we recommend either leaving existing memoization in place (removing it can change compilation output) or carefully testing before removing the memoization.

This section will help you get started with React Compiler and understand how to use it effectively in your projects.

In addition to these docs, we recommend checking the React Compiler Working Group for additional information and discussion about the compiler.

**Examples:**

Example 1 (jsx):
```jsx
import { useMemo, useCallback, memo } from 'react';const ExpensiveComponent = memo(function ExpensiveComponent({ data, onClick }) {  const processedData = useMemo(() => {    return expensiveProcessing(data);  }, [data]);  const handleClick = useCallback((item) => {    onClick(item.id);  }, [onClick]);  return (    <div>      {processedData.map(item => (        <Item key={item.id} onClick={() => handleClick(item)} />      ))}    </div>  );});
```

Example 2 (jsx):
```jsx
<Item key={item.id} onClick={() => handleClick(item)} />
```

Example 3 (jsx):
```jsx
function ExpensiveComponent({ data, onClick }) {  const processedData = expensiveProcessing(data);  const handleClick = (item) => {    onClick(item.id);  };  return (    <div>      {processedData.map(item => (        <Item key={item.id} onClick={() => handleClick(item)} />      ))}    </div>  );}
```

Example 4 (jsx):
```jsx
function FriendList({ friends }) {  const onlineCount = useFriendOnlineCount();  if (friends.length === 0) {    return <NoFriends />;  }  return (    <div>      <span>{onlineCount} online</span>      {friends.map((friend) => (        <FriendListCard key={friend.id} friend={friend} />      ))}      <MessageButton />    </div>  );}
```

---

## JavaScript in JSX with Curly Braces

**URL:** https://react.dev/learn/javascript-in-jsx-with-curly-braces

**Contents:**
- JavaScript in JSX with Curly Braces
  - You will learn
- Passing strings with quotes
- Using curly braces: A window into the JavaScript world
  - Where to use curly braces
- Using “double curlies”: CSS and other objects in JSX
  - Pitfall
- More fun with JavaScript objects and curly braces
- Recap
- Try out some challenges

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to open a window to JavaScript.

When you want to pass a string attribute to JSX, you put it in single or double quotes:

Here, "https://i.imgur.com/7vQD0fPs.jpg" and "Gregorio Y. Zara" are being passed as strings.

But what if you want to dynamically specify the src or alt text? You could use a value from JavaScript by replacing " and " with { and }:

Notice the difference between className="avatar", which specifies an "avatar" CSS class name that makes the image round, and src={avatar} that reads the value of the JavaScript variable called avatar. That’s because curly braces let you work with JavaScript right there in your markup!

JSX is a special way of writing JavaScript. That means it’s possible to use JavaScript inside it—with curly braces { }. The example below first declares a name for the scientist, name, then embeds it with curly braces inside the <h1>:

Try changing the name’s value from 'Gregorio Y. Zara' to 'Hedy Lamarr'. See how the list title changes?

Any JavaScript expression will work between curly braces, including function calls like formatDate():

You can only use curly braces in two ways inside JSX:

In addition to strings, numbers, and other JavaScript expressions, you can even pass objects in JSX. Objects are also denoted with curly braces, like { name: "Hedy Lamarr", inventions: 5 }. Therefore, to pass a JS object in JSX, you must wrap the object in another pair of curly braces: person={{ name: "Hedy Lamarr", inventions: 5 }}.

You may see this with inline CSS styles in JSX. React does not require you to use inline styles (CSS classes work great for most cases). But when you need an inline style, you pass an object to the style attribute:

Try changing the values of backgroundColor and color.

You can really see the JavaScript object inside the curly braces when you write it like this:

The next time you see {{ and }} in JSX, know that it’s nothing more than an object inside the JSX curlies!

Inline style properties are written in camelCase. For example, HTML <ul style="background-color: black"> would be written as <ul style={{ backgroundColor: 'black' }}> in your component.

You can move several expressions into one object, and reference them in your JSX inside curly braces:

In this example, the person JavaScript object contains a name string and a theme object:

The component can use these values from person like so:

JSX is very minimal as a templating language because it lets you organize data and logic using JavaScript.

Now you know almost everything about JSX:

This code crashes with an error saying Objects are not valid as a React child:

Can you find the problem?

**Examples:**

Example 1 (jsx):
```jsx
<ul style={  {    backgroundColor: 'black',    color: 'pink'  }}>
```

Example 2 (css):
```css
const person = {  name: 'Gregorio Y. Zara',  theme: {    backgroundColor: 'black',    color: 'pink'  }};
```

Example 3 (jsx):
```jsx
<div style={person.theme}>  <h1>{person.name}'s Todos</h1>
```

---

## Keeping Components Pure

**URL:** https://react.dev/learn/keeping-components-pure

**Contents:**
- Keeping Components Pure
  - You will learn
- Purity: Components as formulas
- Side Effects: (un)intended consequences
      - Deep Dive
    - Detecting impure calculations with StrictMode
  - Local mutation: Your component’s little secret
- Where you can cause side effects
      - Deep Dive
    - Why does React care about purity?

Some JavaScript functions are pure. Pure functions only perform a calculation and nothing more. By strictly only writing your components as pure functions, you can avoid an entire class of baffling bugs and unpredictable behavior as your codebase grows. To get these benefits, though, there are a few rules you must follow.

In computer science (and especially the world of functional programming), a pure function is a function with the following characteristics:

You might already be familiar with one example of pure functions: formulas in math.

Consider this math formula: y = 2x.

If x = 2 then y = 4. Always.

If x = 3 then y = 6. Always.

If x = 3, y won’t sometimes be 9 or –1 or 2.5 depending on the time of day or the state of the stock market.

If y = 2x and x = 3, y will always be 6.

If we made this into a JavaScript function, it would look like this:

In the above example, double is a pure function. If you pass it 3, it will return 6. Always.

React is designed around this concept. React assumes that every component you write is a pure function. This means that React components you write must always return the same JSX given the same inputs:

When you pass drinkers={2} to Recipe, it will return JSX containing 2 cups of water. Always.

If you pass drinkers={4}, it will return JSX containing 4 cups of water. Always.

Just like a math formula.

You could think of your components as recipes: if you follow them and don’t introduce new ingredients during the cooking process, you will get the same dish every time. That “dish” is the JSX that the component serves to React to render.

Illustrated by Rachel Lee Nabors

React’s rendering process must always be pure. Components should only return their JSX, and not change any objects or variables that existed before rendering—that would make them impure!

Here is a component that breaks this rule:

This component is reading and writing a guest variable declared outside of it. This means that calling this component multiple times will produce different JSX! And what’s more, if other components read guest, they will produce different JSX, too, depending on when they were rendered! That’s not predictable.

Going back to our formula y = 2x, now even if x = 2, we cannot trust that y = 4. Our tests could fail, our users would be baffled, planes would fall out of the sky—you can see how this would lead to confusing bugs!

You can fix this component by passing guest as a prop instead:

Now your component is pure, as the JSX it returns only depends on the guest prop.

In general, you should not expect your components to be rendered in any particular order. It doesn’t matter if you call y = 2x before or after y = 5x: both formulas will resolve independently of each other. In the same way, each component should only “think for itself”, and not attempt to coordinate with or depend upon others during rendering. Rendering is like a school exam: each component should calculate JSX on their own!

Although you might not have used them all yet, in React there are three kinds of inputs that you can read while rendering: props, state, and context. You should always treat these inputs as read-only.

When you want to change something in response to user input, you should set state instead of writing to a variable. You should never change preexisting variables or objects while your component is rendering.

React offers a “Strict Mode” in which it calls each component’s function twice during development. By calling the component functions twice, Strict Mode helps find components that break these rules.

Notice how the original example displayed “Guest #2”, “Guest #4”, and “Guest #6” instead of “Guest #1”, “Guest #2”, and “Guest #3”. The original function was impure, so calling it twice broke it. But the fixed pure version works even if the function is called twice every time. Pure functions only calculate, so calling them twice won’t change anything—just like calling double(2) twice doesn’t change what’s returned, and solving y = 2x twice doesn’t change what y is. Same inputs, same outputs. Always.

Strict Mode has no effect in production, so it won’t slow down the app for your users. To opt into Strict Mode, you can wrap your root component into <React.StrictMode>. Some frameworks do this by default.

In the above example, the problem was that the component changed a preexisting variable while rendering. This is often called a “mutation” to make it sound a bit scarier. Pure functions don’t mutate variables outside of the function’s scope or objects that were created before the call—that makes them impure!

However, it’s completely fine to change variables and objects that you’ve just created while rendering. In this example, you create an [] array, assign it to a cups variable, and then push a dozen cups into it:

If the cups variable or the [] array were created outside the TeaGathering function, this would be a huge problem! You would be changing a preexisting object by pushing items into that array.

However, it’s fine because you’ve created them during the same render, inside TeaGathering. No code outside of TeaGathering will ever know that this happened. This is called “local mutation”—it’s like your component’s little secret.

While functional programming relies heavily on purity, at some point, somewhere, something has to change. That’s kind of the point of programming! These changes—updating the screen, starting an animation, changing the data—are called side effects. They’re things that happen “on the side”, not during rendering.

In React, side effects usually belong inside event handlers. Event handlers are functions that React runs when you perform some action—for example, when you click a button. Even though event handlers are defined inside your component, they don’t run during rendering! So event handlers don’t need to be pure.

If you’ve exhausted all other options and can’t find the right event handler for your side effect, you can still attach it to your returned JSX with a useEffect call in your component. This tells React to execute it later, after rendering, when side effects are allowed. However, this approach should be your last resort.

When possible, try to express your logic with rendering alone. You’ll be surprised how far this can take you!

Writing pure functions takes some habit and discipline. But it also unlocks marvelous opportunities:

Every new React feature we’re building takes advantage of purity. From data fetching to animations to performance, keeping components pure unlocks the power of the React paradigm.

This component tries to set the <h1>’s CSS class to "night" during the time from midnight to six hours in the morning, and "day" at all other times. However, it doesn’t work. Can you fix this component?

You can verify whether your solution works by temporarily changing the computer’s timezone. When the current time is between midnight and six in the morning, the clock should have inverted colors!

**Examples:**

Example 1 (javascript):
```javascript
function double(number) {  return 2 * number;}
```

---

## Lifecycle of Reactive Effects

**URL:** https://react.dev/learn/lifecycle-of-reactive-effects

**Contents:**
- Lifecycle of Reactive Effects
  - You will learn
- The lifecycle of an Effect
  - Note
  - Why synchronization may need to happen more than once
  - How React re-synchronizes your Effect
  - Thinking from the Effect’s perspective
  - How React verifies that your Effect can re-synchronize
  - How React knows that it needs to re-synchronize the Effect
  - Each Effect represents a separate synchronization process

Effects have a different lifecycle from components. Components may mount, update, or unmount. An Effect can only do two things: to start synchronizing something, and later to stop synchronizing it. This cycle can happen multiple times if your Effect depends on props and state that change over time. React provides a linter rule to check that you’ve specified your Effect’s dependencies correctly. This keeps your Effect synchronized to the latest props and state.

Every React component goes through the same lifecycle:

It’s a good way to think about components, but not about Effects. Instead, try to think about each Effect independently from your component’s lifecycle. An Effect describes how to synchronize an external system to the current props and state. As your code changes, synchronization will need to happen more or less often.

To illustrate this point, consider this Effect connecting your component to a chat server:

Your Effect’s body specifies how to start synchronizing:

The cleanup function returned by your Effect specifies how to stop synchronizing:

Intuitively, you might think that React would start synchronizing when your component mounts and stop synchronizing when your component unmounts. However, this is not the end of the story! Sometimes, it may also be necessary to start and stop synchronizing multiple times while the component remains mounted.

Let’s look at why this is necessary, when it happens, and how you can control this behavior.

Some Effects don’t return a cleanup function at all. More often than not, you’ll want to return one—but if you don’t, React will behave as if you returned an empty cleanup function.

Imagine this ChatRoom component receives a roomId prop that the user picks in a dropdown. Let’s say that initially the user picks the "general" room as the roomId. Your app displays the "general" chat room:

After the UI is displayed, React will run your Effect to start synchronizing. It connects to the "general" room:

Later, the user picks a different room in the dropdown (for example, "travel"). First, React will update the UI:

Think about what should happen next. The user sees that "travel" is the selected chat room in the UI. However, the Effect that ran the last time is still connected to the "general" room. The roomId prop has changed, so what your Effect did back then (connecting to the "general" room) no longer matches the UI.

At this point, you want React to do two things:

Luckily, you’ve already taught React how to do both of these things! Your Effect’s body specifies how to start synchronizing, and your cleanup function specifies how to stop synchronizing. All that React needs to do now is to call them in the correct order and with the correct props and state. Let’s see how exactly that happens.

Recall that your ChatRoom component has received a new value for its roomId prop. It used to be "general", and now it is "travel". React needs to re-synchronize your Effect to re-connect you to a different room.

To stop synchronizing, React will call the cleanup function that your Effect returned after connecting to the "general" room. Since roomId was "general", the cleanup function disconnects from the "general" room:

Then React will run the Effect that you’ve provided during this render. This time, roomId is "travel" so it will start synchronizing to the "travel" chat room (until its cleanup function is eventually called too):

Thanks to this, you’re now connected to the same room that the user chose in the UI. Disaster averted!

Every time after your component re-renders with a different roomId, your Effect will re-synchronize. For example, let’s say the user changes roomId from "travel" to "music". React will again stop synchronizing your Effect by calling its cleanup function (disconnecting you from the "travel" room). Then it will start synchronizing again by running its body with the new roomId prop (connecting you to the "music" room).

Finally, when the user goes to a different screen, ChatRoom unmounts. Now there is no need to stay connected at all. React will stop synchronizing your Effect one last time and disconnect you from the "music" chat room.

Let’s recap everything that’s happened from the ChatRoom component’s perspective:

During each of these points in the component’s lifecycle, your Effect did different things:

Now let’s think about what happened from the perspective of the Effect itself:

This code’s structure might inspire you to see what happened as a sequence of non-overlapping time periods:

Previously, you were thinking from the component’s perspective. When you looked from the component’s perspective, it was tempting to think of Effects as “callbacks” or “lifecycle events” that fire at a specific time like “after a render” or “before unmount”. This way of thinking gets complicated very fast, so it’s best to avoid.

Instead, always focus on a single start/stop cycle at a time. It shouldn’t matter whether a component is mounting, updating, or unmounting. All you need to do is to describe how to start synchronization and how to stop it. If you do it well, your Effect will be resilient to being started and stopped as many times as it’s needed.

This might remind you how you don’t think whether a component is mounting or updating when you write the rendering logic that creates JSX. You describe what should be on the screen, and React figures out the rest.

Here is a live example that you can play with. Press “Open chat” to mount the ChatRoom component:

Notice that when the component mounts for the first time, you see three logs:

The first two logs are development-only. In development, React always remounts each component once.

React verifies that your Effect can re-synchronize by forcing it to do that immediately in development. This might remind you of opening a door and closing it an extra time to check if the door lock works. React starts and stops your Effect one extra time in development to check you’ve implemented its cleanup well.

The main reason your Effect will re-synchronize in practice is if some data it uses has changed. In the sandbox above, change the selected chat room. Notice how, when the roomId changes, your Effect re-synchronizes.

However, there are also more unusual cases in which re-synchronization is necessary. For example, try editing the serverUrl in the sandbox above while the chat is open. Notice how the Effect re-synchronizes in response to your edits to the code. In the future, React may add more features that rely on re-synchronization.

You might be wondering how React knew that your Effect needed to re-synchronize after roomId changes. It’s because you told React that its code depends on roomId by including it in the list of dependencies:

Here’s how this works:

Every time after your component re-renders, React will look at the array of dependencies that you have passed. If any of the values in the array is different from the value at the same spot that you passed during the previous render, React will re-synchronize your Effect.

For example, if you passed ["general"] during the initial render, and later you passed ["travel"] during the next render, React will compare "general" and "travel". These are different values (compared with Object.is), so React will re-synchronize your Effect. On the other hand, if your component re-renders but roomId has not changed, your Effect will remain connected to the same room.

Resist adding unrelated logic to your Effect only because this logic needs to run at the same time as an Effect you already wrote. For example, let’s say you want to send an analytics event when the user visits the room. You already have an Effect that depends on roomId, so you might feel tempted to add the analytics call there:

But imagine you later add another dependency to this Effect that needs to re-establish the connection. If this Effect re-synchronizes, it will also call logVisit(roomId) for the same room, which you did not intend. Logging the visit is a separate process from connecting. Write them as two separate Effects:

Each Effect in your code should represent a separate and independent synchronization process.

In the above example, deleting one Effect wouldn’t break the other Effect’s logic. This is a good indication that they synchronize different things, and so it made sense to split them up. On the other hand, if you split up a cohesive piece of logic into separate Effects, the code may look “cleaner” but will be more difficult to maintain. This is why you should think whether the processes are same or separate, not whether the code looks cleaner.

Your Effect reads two variables (serverUrl and roomId), but you only specified roomId as a dependency:

Why doesn’t serverUrl need to be a dependency?

This is because the serverUrl never changes due to a re-render. It’s always the same no matter how many times the component re-renders and why. Since serverUrl never changes, it wouldn’t make sense to specify it as a dependency. After all, dependencies only do something when they change over time!

On the other hand, roomId may be different on a re-render. Props, state, and other values declared inside the component are reactive because they’re calculated during rendering and participate in the React data flow.

If serverUrl was a state variable, it would be reactive. Reactive values must be included in dependencies:

By including serverUrl as a dependency, you ensure that the Effect re-synchronizes after it changes.

Try changing the selected chat room or edit the server URL in this sandbox:

Whenever you change a reactive value like roomId or serverUrl, the Effect re-connects to the chat server.

What happens if you move both serverUrl and roomId outside the component?

Now your Effect’s code does not use any reactive values, so its dependencies can be empty ([]).

Thinking from the component’s perspective, the empty [] dependency array means this Effect connects to the chat room only when the component mounts, and disconnects only when the component unmounts. (Keep in mind that React would still re-synchronize it an extra time in development to stress-test your logic.)

However, if you think from the Effect’s perspective, you don’t need to think about mounting and unmounting at all. What’s important is you’ve specified what your Effect does to start and stop synchronizing. Today, it has no reactive dependencies. But if you ever want the user to change roomId or serverUrl over time (and they would become reactive), your Effect’s code won’t change. You will only need to add them to the dependencies.

Props and state aren’t the only reactive values. Values that you calculate from them are also reactive. If the props or state change, your component will re-render, and the values calculated from them will also change. This is why all variables from the component body used by the Effect should be in the Effect dependency list.

Let’s say that the user can pick a chat server in the dropdown, but they can also configure a default server in settings. Suppose you’ve already put the settings state in a context so you read the settings from that context. Now you calculate the serverUrl based on the selected server from props and the default server:

In this example, serverUrl is not a prop or a state variable. It’s a regular variable that you calculate during rendering. But it’s calculated during rendering, so it can change due to a re-render. This is why it’s reactive.

All values inside the component (including props, state, and variables in your component’s body) are reactive. Any reactive value can change on a re-render, so you need to include reactive values as Effect’s dependencies.

In other words, Effects “react” to all values from the component body.

Mutable values (including global variables) aren’t reactive.

A mutable value like location.pathname can’t be a dependency. It’s mutable, so it can change at any time completely outside of the React rendering data flow. Changing it wouldn’t trigger a re-render of your component. Therefore, even if you specified it in the dependencies, React wouldn’t know to re-synchronize the Effect when it changes. This also breaks the rules of React because reading mutable data during rendering (which is when you calculate the dependencies) breaks purity of rendering. Instead, you should read and subscribe to an external mutable value with useSyncExternalStore.

A mutable value like ref.current or things you read from it also can’t be a dependency. The ref object returned by useRef itself can be a dependency, but its current property is intentionally mutable. It lets you keep track of something without triggering a re-render. But since changing it doesn’t trigger a re-render, it’s not a reactive value, and React won’t know to re-run your Effect when it changes.

As you’ll learn below on this page, a linter will check for these issues automatically.

If your linter is configured for React, it will check that every reactive value used by your Effect’s code is declared as its dependency. For example, this is a lint error because both roomId and serverUrl are reactive:

This may look like a React error, but really React is pointing out a bug in your code. Both roomId and serverUrl may change over time, but you’re forgetting to re-synchronize your Effect when they change. You will remain connected to the initial roomId and serverUrl even after the user picks different values in the UI.

To fix the bug, follow the linter’s suggestion to specify roomId and serverUrl as dependencies of your Effect:

Try this fix in the sandbox above. Verify that the linter error is gone, and the chat re-connects when needed.

In some cases, React knows that a value never changes even though it’s declared inside the component. For example, the set function returned from useState and the ref object returned by useRef are stable—they are guaranteed to not change on a re-render. Stable values aren’t reactive, so you may omit them from the list. Including them is allowed: they won’t change, so it doesn’t matter.

In the previous example, you’ve fixed the lint error by listing roomId and serverUrl as dependencies.

However, you could instead “prove” to the linter that these values aren’t reactive values, i.e. that they can’t change as a result of a re-render. For example, if serverUrl and roomId don’t depend on rendering and always have the same values, you can move them outside the component. Now they don’t need to be dependencies:

You can also move them inside the Effect. They aren’t calculated during rendering, so they’re not reactive:

Effects are reactive blocks of code. They re-synchronize when the values you read inside of them change. Unlike event handlers, which only run once per interaction, Effects run whenever synchronization is necessary.

You can’t “choose” your dependencies. Your dependencies must include every reactive value you read in the Effect. The linter enforces this. Sometimes this may lead to problems like infinite loops and to your Effect re-synchronizing too often. Don’t fix these problems by suppressing the linter! Here’s what to try instead:

Check that your Effect represents an independent synchronization process. If your Effect doesn’t synchronize anything, it might be unnecessary. If it synchronizes several independent things, split it up.

If you want to read the latest value of props or state without “reacting” to it and re-synchronizing the Effect, you can split your Effect into a reactive part (which you’ll keep in the Effect) and a non-reactive part (which you’ll extract into something called an Effect Event). Read about separating Events from Effects.

Avoid relying on objects and functions as dependencies. If you create objects and functions during rendering and then read them from an Effect, they will be different on every render. This will cause your Effect to re-synchronize every time. Read more about removing unnecessary dependencies from Effects.

The linter is your friend, but its powers are limited. The linter only knows when the dependencies are wrong. It doesn’t know the best way to solve each case. If the linter suggests a dependency, but adding it causes a loop, it doesn’t mean the linter should be ignored. You need to change the code inside (or outside) the Effect so that that value isn’t reactive and doesn’t need to be a dependency.

If you have an existing codebase, you might have some Effects that suppress the linter like this:

On the next pages, you’ll learn how to fix this code without breaking the rules. It’s always worth fixing!

In this example, the ChatRoom component connects to the chat room when the component mounts, disconnects when it unmounts, and reconnects when you select a different chat room. This behavior is correct, so you need to keep it working.

However, there is a problem. Whenever you type into the message box input at the bottom, ChatRoom also reconnects to the chat. (You can notice this by clearing the console and typing into the input.) Fix the issue so that this doesn’t happen.

**Examples:**

Example 1 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => {      connection.disconnect();    };  }, [roomId]);  // ...}
```

Example 2 (javascript):
```javascript
// ...    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => {      connection.disconnect();    };    // ...
```

Example 3 (javascript):
```javascript
// ...    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => {      connection.disconnect();    };    // ...
```

Example 4 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId /* "general" */ }) {  // ...  return <h1>Welcome to the {roomId} room!</h1>;}
```

---

## Managing State

**URL:** https://react.dev/learn/managing-state

**Contents:**
- Managing State
  - In this chapter
- Reacting to input with state
- Ready to learn this topic?
- Choosing the state structure
- Ready to learn this topic?
- Sharing state between components
- Ready to learn this topic?
- Preserving and resetting state
- Ready to learn this topic?

As your application grows, it helps to be more intentional about how your state is organized and how the data flows between your components. Redundant or duplicate state is a common source of bugs. In this chapter, you’ll learn how to structure your state well, how to keep your state update logic maintainable, and how to share state between distant components.

With React, you won’t modify the UI from code directly. For example, you won’t write commands like “disable the button”, “enable the button”, “show the success message”, etc. Instead, you will describe the UI you want to see for the different visual states of your component (“initial state”, “typing state”, “success state”), and then trigger the state changes in response to user input. This is similar to how designers think about UI.

Here is a quiz form built using React. Note how it uses the status state variable to determine whether to enable or disable the submit button, and whether to show the success message instead.

Read Reacting to Input with State to learn how to approach interactions with a state-driven mindset.

Structuring state well can make a difference between a component that is pleasant to modify and debug, and one that is a constant source of bugs. The most important principle is that state shouldn’t contain redundant or duplicated information. If there’s unnecessary state, it’s easy to forget to update it, and introduce bugs!

For example, this form has a redundant fullName state variable:

You can remove it and simplify the code by calculating fullName while the component is rendering:

This might seem like a small change, but many bugs in React apps are fixed this way.

Read Choosing the State Structure to learn how to design the state shape to avoid bugs.

Sometimes, you want the state of two components to always change together. To do it, remove state from both of them, move it to their closest common parent, and then pass it down to them via props. This is known as “lifting state up”, and it’s one of the most common things you will do writing React code.

In this example, only one panel should be active at a time. To achieve this, instead of keeping the active state inside each individual panel, the parent component holds the state and specifies the props for its children.

Read Sharing State Between Components to learn how to lift state up and keep components in sync.

When you re-render a component, React needs to decide which parts of the tree to keep (and update), and which parts to discard or re-create from scratch. In most cases, React’s automatic behavior works well enough. By default, React preserves the parts of the tree that “match up” with the previously rendered component tree.

However, sometimes this is not what you want. In this chat app, typing a message and then switching the recipient does not reset the input. This can make the user accidentally send a message to the wrong person:

React lets you override the default behavior, and force a component to reset its state by passing it a different key, like <Chat key={email} />. This tells React that if the recipient is different, it should be considered a different Chat component that needs to be re-created from scratch with the new data (and UI like inputs). Now switching between the recipients resets the input field—even though you render the same component.

Read Preserving and Resetting State to learn the lifetime of state and how to control it.

Components with many state updates spread across many event handlers can get overwhelming. For these cases, you can consolidate all the state update logic outside your component in a single function, called “reducer”. Your event handlers become concise because they only specify the user “actions”. At the bottom of the file, the reducer function specifies how the state should update in response to each action!

Read Extracting State Logic into a Reducer to learn how to consolidate logic in the reducer function.

Usually, you will pass information from a parent component to a child component via props. But passing props can become inconvenient if you need to pass some prop through many components, or if many components need the same information. Context lets the parent component make some information available to any component in the tree below it—no matter how deep it is—without passing it explicitly through props.

Here, the Heading component determines its heading level by “asking” the closest Section for its level. Each Section tracks its own level by asking the parent Section and adding one to it. Every Section provides information to all components below it without passing props—it does that through context.

Read Passing Data Deeply with Context to learn about using context as an alternative to passing props.

Reducers let you consolidate a component’s state update logic. Context lets you pass information deep down to other components. You can combine reducers and context together to manage state of a complex screen.

With this approach, a parent component with complex state manages it with a reducer. Other components anywhere deep in the tree can read its state via context. They can also dispatch actions to update that state.

Read Scaling Up with Reducer and Context to learn how state management scales in a growing app.

Head over to Reacting to Input with State to start reading this chapter page by page!

Or, if you’re already familiar with these topics, why not read about Escape Hatches?

---

## Manipulating the DOM with Refs

**URL:** https://react.dev/learn/manipulating-the-dom-with-refs

**Contents:**
- Manipulating the DOM with Refs
  - You will learn
- Getting a ref to the node
  - Example: Focusing a text input
  - Example: Scrolling to an element
      - Deep Dive
    - How to manage a list of refs using a ref callback
  - Note
- Accessing another component’s DOM nodes
  - Pitfall

React automatically updates the DOM to match your render output, so your components won’t often need to manipulate it. However, sometimes you might need access to the DOM elements managed by React—for example, to focus a node, scroll to it, or measure its size and position. There is no built-in way to do those things in React, so you will need a ref to the DOM node.

To access a DOM node managed by React, first, import the useRef Hook:

Then, use it to declare a ref inside your component:

Finally, pass your ref as the ref attribute to the JSX tag for which you want to get the DOM node:

The useRef Hook returns an object with a single property called current. Initially, myRef.current will be null. When React creates a DOM node for this <div>, React will put a reference to this node into myRef.current. You can then access this DOM node from your event handlers and use the built-in browser APIs defined on it.

In this example, clicking the button will focus the input:

While DOM manipulation is the most common use case for refs, the useRef Hook can be used for storing other things outside React, like timer IDs. Similarly to state, refs remain between renders. Refs are like state variables that don’t trigger re-renders when you set them. Read about refs in Referencing Values with Refs.

You can have more than a single ref in a component. In this example, there is a carousel of three images. Each button centers an image by calling the browser scrollIntoView() method on the corresponding DOM node:

In the above examples, there is a predefined number of refs. However, sometimes you might need a ref to each item in the list, and you don’t know how many you will have. Something like this wouldn’t work:

This is because Hooks must only be called at the top-level of your component. You can’t call useRef in a loop, in a condition, or inside a map() call.

One possible way around this is to get a single ref to their parent element, and then use DOM manipulation methods like querySelectorAll to “find” the individual child nodes from it. However, this is brittle and can break if your DOM structure changes.

Another solution is to pass a function to the ref attribute. This is called a ref callback. React will call your ref callback with the DOM node when it’s time to set the ref, and call the cleanup function returned from the callback when it’s time to clear it. This lets you maintain your own array or a Map, and access any ref by its index or some kind of ID.

This example shows how you can use this approach to scroll to an arbitrary node in a long list:

In this example, itemsRef doesn’t hold a single DOM node. Instead, it holds a Map from item ID to a DOM node. (Refs can hold any values!) The ref callback on every list item takes care to update the Map:

This lets you read individual DOM nodes from the Map later.

When Strict Mode is enabled, ref callbacks will run twice in development.

Read more about how this helps find bugs in callback refs.

Refs are an escape hatch. Manually manipulating another component’s DOM nodes can make your code fragile.

You can pass refs from parent component to child components just like any other prop.

In the above example, a ref is created in the parent component, MyForm, and is passed to the child component, MyInput. MyInput then passes the ref to <input>. Because <input> is a built-in component React sets the .current property of the ref to the <input> DOM element.

The inputRef created in MyForm now points to the <input> DOM element returned by MyInput. A click handler created in MyForm can access inputRef and call focus() to set the focus on <input>.

In the above example, the ref passed to MyInput is passed on to the original DOM input element. This lets the parent component call focus() on it. However, this also lets the parent component do something else—for example, change its CSS styles. In uncommon cases, you may want to restrict the exposed functionality. You can do that with useImperativeHandle:

Here, realInputRef inside MyInput holds the actual input DOM node. However, useImperativeHandle instructs React to provide your own special object as the value of a ref to the parent component. So inputRef.current inside the Form component will only have the focus method. In this case, the ref “handle” is not the DOM node, but the custom object you create inside useImperativeHandle call.

In React, every update is split in two phases:

In general, you don’t want to access refs during rendering. That goes for refs holding DOM nodes as well. During the first render, the DOM nodes have not yet been created, so ref.current will be null. And during the rendering of updates, the DOM nodes haven’t been updated yet. So it’s too early to read them.

React sets ref.current during the commit. Before updating the DOM, React sets the affected ref.current values to null. After updating the DOM, React immediately sets them to the corresponding DOM nodes.

Usually, you will access refs from event handlers. If you want to do something with a ref, but there is no particular event to do it in, you might need an Effect. We will discuss Effects on the next pages.

Consider code like this, which adds a new todo and scrolls the screen down to the last child of the list. Notice how, for some reason, it always scrolls to the todo that was just before the last added one:

The issue is with these two lines:

In React, state updates are queued. Usually, this is what you want. However, here it causes a problem because setTodos does not immediately update the DOM. So the time you scroll the list to its last element, the todo has not yet been added. This is why scrolling always “lags behind” by one item.

To fix this issue, you can force React to update (“flush”) the DOM synchronously. To do this, import flushSync from react-dom and wrap the state update into a flushSync call:

This will instruct React to update the DOM synchronously right after the code wrapped in flushSync executes. As a result, the last todo will already be in the DOM by the time you try to scroll to it:

Refs are an escape hatch. You should only use them when you have to “step outside React”. Common examples of this include managing focus, scroll position, or calling browser APIs that React does not expose.

If you stick to non-destructive actions like focusing and scrolling, you shouldn’t encounter any problems. However, if you try to modify the DOM manually, you can risk conflicting with the changes React is making.

To illustrate this problem, this example includes a welcome message and two buttons. The first button toggles its presence using conditional rendering and state, as you would usually do in React. The second button uses the remove() DOM API to forcefully remove it from the DOM outside of React’s control.

Try pressing “Toggle with setState” a few times. The message should disappear and appear again. Then press “Remove from the DOM”. This will forcefully remove it. Finally, press “Toggle with setState”:

After you’ve manually removed the DOM element, trying to use setState to show it again will lead to a crash. This is because you’ve changed the DOM, and React doesn’t know how to continue managing it correctly.

Avoid changing DOM nodes managed by React. Modifying, adding children to, or removing children from elements that are managed by React can lead to inconsistent visual results or crashes like above.

However, this doesn’t mean that you can’t do it at all. It requires caution. You can safely modify parts of the DOM that React has no reason to update. For example, if some <div> is always empty in the JSX, React won’t have a reason to touch its children list. Therefore, it is safe to manually add or remove elements there.

In this example, the button toggles a state variable to switch between a playing and a paused state. However, in order to actually play or pause the video, toggling state is not enough. You also need to call play() and pause() on the DOM element for the <video>. Add a ref to it, and make the button work.

For an extra challenge, keep the “Play” button in sync with whether the video is playing even if the user right-clicks the video and plays it using the built-in browser media controls. You might want to listen to onPlay and onPause on the video to do that.

**Examples:**

Example 1 (sql):
```sql
import { useRef } from 'react';
```

Example 2 (jsx):
```jsx
const myRef = useRef(null);
```

Example 3 (jsx):
```jsx
<div ref={myRef}>
```

Example 4 (unknown):
```unknown
// You can use any browser APIs, for example:myRef.current.scrollIntoView();
```

---

## Passing Data Deeply with Context

**URL:** https://react.dev/learn/passing-data-deeply-with-context

**Contents:**
- Passing Data Deeply with Context
  - You will learn
- The problem with passing props
- Context: an alternative to passing props
  - Step 1: Create the context
  - Step 2: Use the context
  - Step 3: Provide the context
- Using and providing context from the same component
  - Note
- Context passes through intermediate components

Usually, you will pass information from a parent component to a child component via props. But passing props can become verbose and inconvenient if you have to pass them through many components in the middle, or if many components in your app need the same information. Context lets the parent component make some information available to any component in the tree below it—no matter how deep—without passing it explicitly through props.

Passing props is a great way to explicitly pipe data through your UI tree to the components that use it.

But passing props can become verbose and inconvenient when you need to pass some prop deeply through the tree, or if many components need the same prop. The nearest common ancestor could be far removed from the components that need data, and lifting state up that high can lead to a situation called “prop drilling”.

Wouldn’t it be great if there were a way to “teleport” data to the components in the tree that need it without passing props? With React’s context feature, there is!

Context lets a parent component provide data to the entire tree below it. There are many uses for context. Here is one example. Consider this Heading component that accepts a level for its size:

Let’s say you want multiple headings within the same Section to always have the same size:

Currently, you pass the level prop to each <Heading> separately:

It would be nice if you could pass the level prop to the <Section> component instead and remove it from the <Heading>. This way you could enforce that all headings in the same section have the same size:

But how can the <Heading> component know the level of its closest <Section>? That would require some way for a child to “ask” for data from somewhere above in the tree.

You can’t do it with props alone. This is where context comes into play. You will do it in three steps:

Context lets a parent—even a distant one!—provide some data to the entire tree inside of it.

Using context in close children

Using context in distant children

First, you need to create the context. You’ll need to export it from a file so that your components can use it:

The only argument to createContext is the default value. Here, 1 refers to the biggest heading level, but you could pass any kind of value (even an object). You will see the significance of the default value in the next step.

Import the useContext Hook from React and your context:

Currently, the Heading component reads level from props:

Instead, remove the level prop and read the value from the context you just imported, LevelContext:

useContext is a Hook. Just like useState and useReducer, you can only call a Hook immediately inside a React component (not inside loops or conditions). useContext tells React that the Heading component wants to read the LevelContext.

Now that the Heading component doesn’t have a level prop, you don’t need to pass the level prop to Heading in your JSX like this anymore:

Update the JSX so that it’s the Section that receives it instead:

As a reminder, this is the markup that you were trying to get working:

Notice this example doesn’t quite work, yet! All the headings have the same size because even though you’re using the context, you have not provided it yet. React doesn’t know where to get it!

If you don’t provide the context, React will use the default value you’ve specified in the previous step. In this example, you specified 1 as the argument to createContext, so useContext(LevelContext) returns 1, setting all those headings to <h1>. Let’s fix this problem by having each Section provide its own context.

The Section component currently renders its children:

Wrap them with a context provider to provide the LevelContext to them:

This tells React: “if any component inside this <Section> asks for LevelContext, give them this level.” The component will use the value of the nearest <LevelContext> in the UI tree above it.

It’s the same result as the original code, but you did not need to pass the level prop to each Heading component! Instead, it “figures out” its heading level by asking the closest Section above:

Currently, you still have to specify each section’s level manually:

Since context lets you read information from a component above, each Section could read the level from the Section above, and pass level + 1 down automatically. Here is how you could do it:

With this change, you don’t need to pass the level prop either to the <Section> or to the <Heading>:

Now both Heading and Section read the LevelContext to figure out how “deep” they are. And the Section wraps its children into the LevelContext to specify that anything inside of it is at a “deeper” level.

This example uses heading levels because they show visually how nested components can override context. But context is useful for many other use cases too. You can pass down any information needed by the entire subtree: the current color theme, the currently logged in user, and so on.

You can insert as many components as you like between the component that provides context and the one that uses it. This includes both built-in components like <div> and components you might build yourself.

In this example, the same Post component (with a dashed border) is rendered at two different nesting levels. Notice that the <Heading> inside of it gets its level automatically from the closest <Section>:

You didn’t do anything special for this to work. A Section specifies the context for the tree inside it, so you can insert a <Heading> anywhere, and it will have the correct size. Try it in the sandbox above!

Context lets you write components that “adapt to their surroundings” and display themselves differently depending on where (or, in other words, in which context) they are being rendered.

How context works might remind you of CSS property inheritance. In CSS, you can specify color: blue for a <div>, and any DOM node inside of it, no matter how deep, will inherit that color unless some other DOM node in the middle overrides it with color: green. Similarly, in React, the only way to override some context coming from above is to wrap children into a context provider with a different value.

In CSS, different properties like color and background-color don’t override each other. You can set all <div>’s color to red without impacting background-color. Similarly, different React contexts don’t override each other. Each context that you make with createContext() is completely separate from other ones, and ties together components using and providing that particular context. One component may use or provide many different contexts without a problem.

Context is very tempting to use! However, this also means it’s too easy to overuse it. Just because you need to pass some props several levels deep doesn’t mean you should put that information into context.

Here’s a few alternatives you should consider before using context:

If neither of these approaches works well for you, consider context.

Context is not limited to static values. If you pass a different value on the next render, React will update all the components reading it below! This is why context is often used in combination with state.

In general, if some information is needed by distant components in different parts of the tree, it’s a good indication that context will help you.

In this example, toggling the checkbox changes the imageSize prop passed to each <PlaceImage>. The checkbox state is held in the top-level App component, but each <PlaceImage> needs to be aware of it.

Currently, App passes imageSize to List, which passes it to each Place, which passes it to the PlaceImage. Remove the imageSize prop, and instead pass it from the App component directly to PlaceImage.

You can declare context in Context.js.

**Examples:**

Example 1 (jsx):
```jsx
<Section>  <Heading level={3}>About</Heading>  <Heading level={3}>Photos</Heading>  <Heading level={3}>Videos</Heading></Section>
```

Example 2 (jsx):
```jsx
<Section level={3}>  <Heading>About</Heading>  <Heading>Photos</Heading>  <Heading>Videos</Heading></Section>
```

Example 3 (sql):
```sql
import { useContext } from 'react';import { LevelContext } from './LevelContext.js';
```

Example 4 (javascript):
```javascript
export default function Heading({ level, children }) {  // ...}
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={...} /> is rendered with no size prop, the size will be set to 100.

The default value is only used if the size prop is missing or if you pass size={undefined}. But if you pass size={null} or size={0}, the default value will not be used.

Sometimes, passing props gets very repetitive:

There’s nothing wrong with repetitive code—it can be more legible. But at times you may value conciseness. Some components forward all of their props to their children, like how this Profile does with Avatar. Because they don’t use any of their props directly, it can make sense to use a more concise “spread” syntax:

This forwards all of Profile’s props to the Avatar without listing each of their names.

Use spread syntax with restraint. If you’re using it in every other component, something is wrong. Often, it indicates that you should split your components and pass children as JSX. More on that next!

It is common to nest built-in browser tags:

Sometimes you’ll want to nest your own components the same way:

When you nest content inside a JSX tag, the parent component will receive that content in a prop called children. For example, the Card component below will receive a children prop set to <Avatar /> and render it in a wrapper div:

Try replacing the <Avatar> inside <Card> with some text to see how the Card component can wrap any nested content. It doesn’t need to “know” what’s being rendered inside of it. You will see this flexible pattern in many places.

You can think of a component with a children prop as having a “hole” that can be “filled in” by its parent components with arbitrary JSX. You will often use the children prop for visual wrappers: panels, grids, etc.

Illustrated by Rachel Lee Nabors

The Clock component below receives two props from its parent component: color and time. (The parent component’s code is omitted because it uses state, which we won’t dive into just yet.)

Try changing the color in the select box below:

This example illustrates that a component may receive different props over time. Props are not always static! Here, the time prop changes every second, and the color prop changes when you select another color. Props reflect a component’s data at any point in time, rather than only in the beginning.

However, props are immutable—a term from computer science meaning “unchangeable”. When a component needs to change its props (for example, in response to a user interaction or new data), it will have to “ask” its parent component to pass it different props—a new object! Its old props will then be cast aside, and eventually the JavaScript engine will reclaim the memory taken by them.

Don’t try to “change props”. When you need to respond to the user input (like changing the selected color), you will need to “set state”, which you can learn about in State: A Component’s Memory.

This Gallery component contains some very similar markup for two profiles. Extract a Profile component out of it to reduce the duplication. You’ll need to choose what props to pass to it.

**Examples:**

Example 1 (jsx):
```jsx
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (javascript):
```javascript
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (javascript):
```javascript
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## Preserving and Resetting State

**URL:** https://react.dev/learn/preserving-and-resetting-state

**Contents:**
- Preserving and Resetting State
  - You will learn
- State is tied to a position in the render tree
- Same component at the same position preserves state
  - Pitfall
- Different components at the same position reset state
  - Pitfall
- Resetting state at the same position
  - Option 1: Rendering a component in different positions
  - Option 2: Resetting state with a key

State is isolated between components. React keeps track of which state belongs to which component based on their place in the UI tree. You can control when to preserve state and when to reset it between re-renders.

React builds render trees for the component structure in your UI.

When you give a component state, you might think the state “lives” inside the component. But the state is actually held inside React. React associates each piece of state it’s holding with the correct component by where that component sits in the render tree.

Here, there is only one <Counter /> JSX tag, but it’s rendered at two different positions:

Here’s how these look as a tree:

These are two separate counters because each is rendered at its own position in the tree. You don’t usually have to think about these positions to use React, but it can be useful to understand how it works.

In React, each component on the screen has fully isolated state. For example, if you render two Counter components side by side, each of them will get its own, independent, score and hover states.

Try clicking both counters and notice they don’t affect each other:

As you can see, when one counter is updated, only the state for that component is updated:

React will keep the state around for as long as you render the same component at the same position in the tree. To see this, increment both counters, then remove the second component by unchecking “Render the second counter” checkbox, and then add it back by ticking it again:

Notice how the moment you stop rendering the second counter, its state disappears completely. That’s because when React removes a component, it destroys its state.

When you tick “Render the second counter”, a second Counter and its state are initialized from scratch (score = 0) and added to the DOM.

React preserves a component’s state for as long as it’s being rendered at its position in the UI tree. If it gets removed, or a different component gets rendered at the same position, React discards its state.

In this example, there are two different <Counter /> tags:

When you tick or clear the checkbox, the counter state does not get reset. Whether isFancy is true or false, you always have a <Counter /> as the first child of the div returned from the root App component:

Updating the App state does not reset the Counter because Counter stays in the same position

It’s the same component at the same position, so from React’s perspective, it’s the same counter.

Remember that it’s the position in the UI tree—not in the JSX markup—that matters to React! This component has two return clauses with different <Counter /> JSX tags inside and outside the if:

You might expect the state to reset when you tick checkbox, but it doesn’t! This is because both of these <Counter /> tags are rendered at the same position. React doesn’t know where you place the conditions in your function. All it “sees” is the tree you return.

In both cases, the App component returns a <div> with <Counter /> as a first child. To React, these two counters have the same “address”: the first child of the first child of the root. This is how React matches them up between the previous and next renders, regardless of how you structure your logic.

In this example, ticking the checkbox will replace <Counter> with a <p>:

Here, you switch between different component types at the same position. Initially, the first child of the <div> contained a Counter. But when you swapped in a p, React removed the Counter from the UI tree and destroyed its state.

When Counter changes to p, the Counter is deleted and the p is added

When switching back, the p is deleted and the Counter is added

Also, when you render a different component in the same position, it resets the state of its entire subtree. To see how this works, increment the counter and then tick the checkbox:

The counter state gets reset when you click the checkbox. Although you render a Counter, the first child of the div changes from a section to a div. When the child section was removed from the DOM, the whole tree below it (including the Counter and its state) was destroyed as well.

When section changes to div, the section is deleted and the new div is added

When switching back, the div is deleted and the new section is added

As a rule of thumb, if you want to preserve the state between re-renders, the structure of your tree needs to “match up” from one render to another. If the structure is different, the state gets destroyed because React destroys state when it removes a component from the tree.

This is why you should not nest component function definitions.

Here, the MyTextField component function is defined inside MyComponent:

Every time you click the button, the input state disappears! This is because a different MyTextField function is created for every render of MyComponent. You’re rendering a different component in the same position, so React resets all state below. This leads to bugs and performance problems. To avoid this problem, always declare component functions at the top level, and don’t nest their definitions.

By default, React preserves state of a component while it stays at the same position. Usually, this is exactly what you want, so it makes sense as the default behavior. But sometimes, you may want to reset a component’s state. Consider this app that lets two players keep track of their scores during each turn:

Currently, when you change the player, the score is preserved. The two Counters appear in the same position, so React sees them as the same Counter whose person prop has changed.

But conceptually, in this app they should be two separate counters. They might appear in the same place in the UI, but one is a counter for Taylor, and another is a counter for Sarah.

There are two ways to reset state when switching between them:

If you want these two Counters to be independent, you can render them in two different positions:

Clicking “next” again

Each Counter’s state gets destroyed each time it’s removed from the DOM. This is why they reset every time you click the button.

This solution is convenient when you only have a few independent components rendered in the same place. In this example, you only have two, so it’s not a hassle to render both separately in the JSX.

There is also another, more generic, way to reset a component’s state.

You might have seen keys when rendering lists. Keys aren’t just for lists! You can use keys to make React distinguish between any components. By default, React uses order within the parent (“first counter”, “second counter”) to discern between components. But keys let you tell React that this is not just a first counter, or a second counter, but a specific counter—for example, Taylor’s counter. This way, React will know Taylor’s counter wherever it appears in the tree!

In this example, the two <Counter />s don’t share state even though they appear in the same place in JSX:

Switching between Taylor and Sarah does not preserve the state. This is because you gave them different keys:

Specifying a key tells React to use the key itself as part of the position, instead of their order within the parent. This is why, even though you render them in the same place in JSX, React sees them as two different counters, and so they will never share state. Every time a counter appears on the screen, its state is created. Every time it is removed, its state is destroyed. Toggling between them resets their state over and over.

Remember that keys are not globally unique. They only specify the position within the parent.

Resetting state with a key is particularly useful when dealing with forms.

In this chat app, the <Chat> component contains the text input state:

Try entering something into the input, and then press “Alice” or “Bob” to choose a different recipient. You will notice that the input state is preserved because the <Chat> is rendered at the same position in the tree.

In many apps, this may be the desired behavior, but not in a chat app! You don’t want to let the user send a message they already typed to a wrong person due to an accidental click. To fix it, add a key:

This ensures that when you select a different recipient, the Chat component will be recreated from scratch, including any state in the tree below it. React will also re-create the DOM elements instead of reusing them.

Now switching the recipient always clears the text field:

In a real chat app, you’d probably want to recover the input state when the user selects the previous recipient again. There are a few ways to keep the state “alive” for a component that’s no longer visible:

No matter which strategy you pick, a chat with Alice is conceptually distinct from a chat with Bob, so it makes sense to give a key to the <Chat> tree based on the current recipient.

This example shows a message when you press the button. However, pressing the button also accidentally resets the input. Why does this happen? Fix it so that pressing the button does not reset the input text.

**Examples:**

Example 1 (jsx):
```jsx
{isPlayerA ? (  <Counter key="Taylor" person="Taylor" />) : (  <Counter key="Sarah" person="Sarah" />)}
```

Example 2 (jsx):
```jsx
<Chat key={to.id} contact={to} />
```

---

## Queueing a Series of State Updates

**URL:** https://react.dev/learn/queueing-a-series-of-state-updates

**Contents:**
- Queueing a Series of State Updates
  - You will learn
- React batches state updates
- Updating the same state multiple times before the next render
  - What happens if you update state after replacing it
  - Note
  - What happens if you replace state after updating it
  - Naming conventions
- Recap
- Try out some challenges

Setting a state variable will queue another render. But sometimes you might want to perform multiple operations on the value before queueing the next render. To do this, it helps to understand how React batches state updates.

You might expect that clicking the “+3” button will increment the counter three times because it calls setNumber(number + 1) three times:

However, as you might recall from the previous section, each render’s state values are fixed, so the value of number inside the first render’s event handler is always 0, no matter how many times you call setNumber(1):

But there is one other factor at play here. React waits until all code in the event handlers has run before processing your state updates. This is why the re-render only happens after all these setNumber() calls.

This might remind you of a waiter taking an order at the restaurant. A waiter doesn’t run to the kitchen at the mention of your first dish! Instead, they let you finish your order, let you make changes to it, and even take orders from other people at the table.

Illustrated by Rachel Lee Nabors

This lets you update multiple state variables—even from multiple components—without triggering too many re-renders. But this also means that the UI won’t be updated until after your event handler, and any code in it, completes. This behavior, also known as batching, makes your React app run much faster. It also avoids dealing with confusing “half-finished” renders where only some of the variables have been updated.

React does not batch across multiple intentional events like clicks—each click is handled separately. Rest assured that React only does batching when it’s generally safe to do. This ensures that, for example, if the first button click disables a form, the second click would not submit it again.

It is an uncommon use case, but if you would like to update the same state variable multiple times before the next render, instead of passing the next state value like setNumber(number + 1), you can pass a function that calculates the next state based on the previous one in the queue, like setNumber(n => n + 1). It is a way to tell React to “do something with the state value” instead of just replacing it.

Try incrementing the counter now:

Here, n => n + 1 is called an updater function. When you pass it to a state setter:

Here’s how React works through these lines of code while executing the event handler:

When you call useState during the next render, React goes through the queue. The previous number state was 0, so that’s what React passes to the first updater function as the n argument. Then React takes the return value of your previous updater function and passes it to the next updater as n, and so on:

React stores 3 as the final result and returns it from useState.

This is why clicking “+3” in the above example correctly increments the value by 3.

What about this event handler? What do you think number will be in the next render?

Here’s what this event handler tells React to do:

During the next render, React goes through the state queue:

React stores 6 as the final result and returns it from useState.

You may have noticed that setState(5) actually works like setState(n => 5), but n is unused!

Let’s try one more example. What do you think number will be in the next render?

Here’s how React works through these lines of code while executing this event handler:

During the next render, React goes through the state queue:

Then React stores 42 as the final result and returns it from useState.

To summarize, here’s how you can think of what you’re passing to the setNumber state setter:

After the event handler completes, React will trigger a re-render. During the re-render, React will process the queue. Updater functions run during rendering, so updater functions must be pure and only return the result. Don’t try to set state from inside of them or run other side effects. In Strict Mode, React will run each updater function twice (but discard the second result) to help you find mistakes.

It’s common to name the updater function argument by the first letters of the corresponding state variable:

If you prefer more verbose code, another common convention is to repeat the full state variable name, like setEnabled(enabled => !enabled), or to use a prefix like setEnabled(prevEnabled => !prevEnabled).

You’re working on an art marketplace app that lets the user submit multiple orders for an art item at the same time. Each time the user presses the “Buy” button, the “Pending” counter should increase by one. After three seconds, the “Pending” counter should decrease, and the “Completed” counter should increase.

However, the “Pending” counter does not behave as intended. When you press “Buy”, it decreases to -1 (which should not be possible!). And if you click fast twice, both counters seem to behave unpredictably.

Why does this happen? Fix both counters.

**Examples:**

Example 1 (unknown):
```unknown
setNumber(0 + 1);setNumber(0 + 1);setNumber(0 + 1);
```

Example 2 (javascript):
```javascript
setNumber(n => n + 1);setNumber(n => n + 1);setNumber(n => n + 1);
```

Example 3 (jsx):
```jsx
<button onClick={() => {  setNumber(number + 5);  setNumber(n => n + 1);}}>
```

Example 4 (jsx):
```jsx
<button onClick={() => {  setNumber(number + 5);  setNumber(n => n + 1);  setNumber(42);}}>
```

---

## Quick Start

**URL:** https://react.dev/learn

**Contents:**
- Quick Start
  - You will learn
- Creating and nesting components
- Writing markup with JSX
- Adding styles
- Displaying data
- Conditional rendering
- Rendering lists
- Responding to events
- Updating the screen

Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

React apps are made out of components. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

Now that you’ve declared MyButton, you can nest it into another component:

Notice that <MyButton /> starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

The export default keywords specify the main component in the file. If you’re not familiar with some piece of JavaScript syntax, MDN and javascript.info have great references.

The markup syntax you’ve seen above is called JSX. It is optional, but most React projects use JSX for its convenience. All of the tools we recommend for local development support JSX out of the box.

JSX is stricter than HTML. You have to close tags like <br />. Your component also can’t return multiple JSX tags. You have to wrap them into a shared parent, like a <div>...</div> or an empty <>...</> wrapper:

If you have a lot of HTML to port to JSX, you can use an online converter.

In React, you specify a CSS class with className. It works the same way as the HTML class attribute:

Then you write the CSS rules for it in a separate CSS file:

React does not prescribe how you add CSS files. In the simplest case, you’ll add a <link> tag to your HTML. If you use a build tool or a framework, consult its documentation to learn how to add a CSS file to your project.

JSX lets you put markup into JavaScript. Curly braces let you “escape back” into JavaScript so that you can embed some variable from your code and display it to the user. For example, this will display user.name:

You can also “escape into JavaScript” from JSX attributes, but you have to use curly braces instead of quotes. For example, className="avatar" passes the "avatar" string as the CSS class, but src={user.imageUrl} reads the JavaScript user.imageUrl variable value, and then passes that value as the src attribute:

You can put more complex expressions inside the JSX curly braces too, for example, string concatenation:

In the above example, style={{}} is not a special syntax, but a regular {} object inside the style={ } JSX curly braces. You can use the style attribute when your styles depend on JavaScript variables.

In React, there is no special syntax for writing conditions. Instead, you’ll use the same techniques as you use when writing regular JavaScript code. For example, you can use an if statement to conditionally include JSX:

If you prefer more compact code, you can use the conditional ? operator. Unlike if, it works inside JSX:

When you don’t need the else branch, you can also use a shorter logical && syntax:

All of these approaches also work for conditionally specifying attributes. If you’re unfamiliar with some of this JavaScript syntax, you can start by always using if...else.

You will rely on JavaScript features like for loop and the array map() function to render lists of components.

For example, let’s say you have an array of products:

Inside your component, use the map() function to transform an array of products into an array of <li> items:

Notice how <li> has a key attribute. For each item in a list, you should pass a string or a number that uniquely identifies that item among its siblings. Usually, a key should be coming from your data, such as a database ID. React uses your keys to know what happened if you later insert, delete, or reorder the items.

You can respond to events by declaring event handler functions inside your components:

Notice how onClick={handleClick} has no parentheses at the end! Do not call the event handler function: you only need to pass it down. React will call your event handler when the user clicks the button.

Often, you’ll want your component to “remember” some information and display it. For example, maybe you want to count the number of times a button is clicked. To do this, add state to your component.

First, import useState from React:

Now you can declare a state variable inside your component:

You’ll get two things from useState: the current state (count), and the function that lets you update it (setCount). You can give them any names, but the convention is to write [something, setSomething].

The first time the button is displayed, count will be 0 because you passed 0 to useState(). When you want to change state, call setCount() and pass the new value to it. Clicking this button will increment the counter:

React will call your component function again. This time, count will be 1. Then it will be 2. And so on.

If you render the same component multiple times, each will get its own state. Click each button separately:

Notice how each button “remembers” its own count state and doesn’t affect other buttons.

Functions starting with use are called Hooks. useState is a built-in Hook provided by React. You can find other built-in Hooks in the API reference. You can also write your own Hooks by combining the existing ones.

Hooks are more restrictive than other functions. You can only call Hooks at the top of your components (or other Hooks). If you want to use useState in a condition or a loop, extract a new component and put it there.

In the previous example, each MyButton had its own independent count, and when each button was clicked, only the count for the button clicked changed:

Initially, each MyButton’s count state is 0

The first MyButton updates its count to 1

However, often you’ll need components to share data and always update together.

To make both MyButton components display the same count and update together, you need to move the state from the individual buttons “upwards” to the closest component containing all of them.

In this example, it is MyApp:

Initially, MyApp’s count state is 0 and is passed down to both children

On click, MyApp updates its count state to 1 and passes it down to both children

Now when you click either button, the count in MyApp will change, which will change both of the counts in MyButton. Here’s how you can express this in code.

First, move the state up from MyButton into MyApp:

Then, pass the state down from MyApp to each MyButton, together with the shared click handler. You can pass information to MyButton using the JSX curly braces, just like you previously did with built-in tags like <img>:

The information you pass down like this is called props. Now the MyApp component contains the count state and the handleClick event handler, and passes both of them down as props to each of the buttons.

Finally, change MyButton to read the props you have passed from its parent component:

When you click the button, the onClick handler fires. Each button’s onClick prop was set to the handleClick function inside MyApp, so the code inside of it runs. That code calls setCount(count + 1), incrementing the count state variable. The new count value is passed as a prop to each button, so they all show the new value. This is called “lifting state up”. By moving state up, you’ve shared it between components.

By now, you know the basics of how to write React code!

Check out the Tutorial to put them into practice and build your first mini-app with React.

**Examples:**

Example 1 (javascript):
```javascript
function MyButton() {  return (    <button>I'm a button</button>  );}
```

Example 2 (jsx):
```jsx
export default function MyApp() {  return (    <div>      <h1>Welcome to my app</h1>      <MyButton />    </div>  );}
```

Example 3 (jsx):
```jsx
function AboutPage() {  return (    <>      <h1>About</h1>      <p>Hello there.<br />How do you do?</p>    </>  );}
```

Example 4 (jsx):
```jsx
<img className="avatar" />
```

---

## Reacting to Input with State

**URL:** https://react.dev/learn/reacting-to-input-with-state

**Contents:**
- Reacting to Input with State
  - You will learn
- How declarative UI compares to imperative
- Thinking about UI declaratively
  - Step 1: Identify your component’s different visual states
      - Deep Dive
    - Displaying many visual states at once
  - Step 2: Determine what triggers those state changes
  - Note
  - Step 3: Represent the state in memory with useState

React provides a declarative way to manipulate the UI. Instead of manipulating individual pieces of the UI directly, you describe the different states that your component can be in, and switch between them in response to the user input. This is similar to how designers think about the UI.

When you design UI interactions, you probably think about how the UI changes in response to user actions. Consider a form that lets the user submit an answer:

In imperative programming, the above corresponds directly to how you implement interaction. You have to write the exact instructions to manipulate the UI depending on what just happened. Here’s another way to think about this: imagine riding next to someone in a car and telling them turn by turn where to go.

Illustrated by Rachel Lee Nabors

They don’t know where you want to go, they just follow your commands. (And if you get the directions wrong, you end up in the wrong place!) It’s called imperative because you have to “command” each element, from the spinner to the button, telling the computer how to update the UI.

In this example of imperative UI programming, the form is built without React. It only uses the browser DOM:

Manipulating the UI imperatively works well enough for isolated examples, but it gets exponentially more difficult to manage in more complex systems. Imagine updating a page full of different forms like this one. Adding a new UI element or a new interaction would require carefully checking all existing code to make sure you haven’t introduced a bug (for example, forgetting to show or hide something).

React was built to solve this problem.

In React, you don’t directly manipulate the UI—meaning you don’t enable, disable, show, or hide components directly. Instead, you declare what you want to show, and React figures out how to update the UI. Think of getting into a taxi and telling the driver where you want to go instead of telling them exactly where to turn. It’s the driver’s job to get you there, and they might even know some shortcuts you haven’t considered!

Illustrated by Rachel Lee Nabors

You’ve seen how to implement a form imperatively above. To better understand how to think in React, you’ll walk through reimplementing this UI in React below:

In computer science, you may hear about a “state machine” being in one of several “states”. If you work with a designer, you may have seen mockups for different “visual states”. React stands at the intersection of design and computer science, so both of these ideas are sources of inspiration.

First, you need to visualize all the different “states” of the UI the user might see:

Just like a designer, you’ll want to “mock up” or create “mocks” for the different states before you add logic. For example, here is a mock for just the visual part of the form. This mock is controlled by a prop called status with a default value of 'empty':

You could call that prop anything you like, the naming is not important. Try editing status = 'empty' to status = 'success' to see the success message appear. Mocking lets you quickly iterate on the UI before you wire up any logic. Here is a more fleshed out prototype of the same component, still “controlled” by the status prop:

If a component has a lot of visual states, it can be convenient to show them all on one page:

Pages like this are often called “living styleguides” or “storybooks”.

You can trigger state updates in response to two kinds of inputs:

Illustrated by Rachel Lee Nabors

In both cases, you must set state variables to update the UI. For the form you’re developing, you will need to change state in response to a few different inputs:

Notice that human inputs often require event handlers!

To help visualize this flow, try drawing each state on paper as a labeled circle, and each change between two states as an arrow. You can sketch out many flows this way and sort out bugs long before implementation.

Next you’ll need to represent the visual states of your component in memory with useState. Simplicity is key: each piece of state is a “moving piece”, and you want as few “moving pieces” as possible. More complexity leads to more bugs!

Start with the state that absolutely must be there. For example, you’ll need to store the answer for the input, and the error (if it exists) to store the last error:

Then, you’ll need a state variable representing which one of the visual states that you want to display. There’s usually more than a single way to represent that in memory, so you’ll need to experiment with it.

If you struggle to think of the best way immediately, start by adding enough state that you’re definitely sure that all the possible visual states are covered:

Your first idea likely won’t be the best, but that’s ok—refactoring state is a part of the process!

You want to avoid duplication in the state content so you’re only tracking what is essential. Spending a little time on refactoring your state structure will make your components easier to understand, reduce duplication, and avoid unintended meanings. Your goal is to prevent the cases where the state in memory doesn’t represent any valid UI that you’d want a user to see. (For example, you never want to show an error message and disable the input at the same time, or the user won’t be able to correct the error!)

Here are some questions you can ask about your state variables:

After this clean-up, you’re left with 3 (down from 7!) essential state variables:

You know they are essential, because you can’t remove any of them without breaking the functionality.

These three variables are a good enough representation of this form’s state. However, there are still some intermediate states that don’t fully make sense. For example, a non-null error doesn’t make sense when status is 'success'. To model the state more precisely, you can extract it into a reducer. Reducers let you unify multiple state variables into a single object and consolidate all the related logic!

Lastly, create event handlers that update the state. Below is the final form, with all event handlers wired up:

Although this code is longer than the original imperative example, it is much less fragile. Expressing all interactions as state changes lets you later introduce new visual states without breaking existing ones. It also lets you change what should be displayed in each state without changing the logic of the interaction itself.

Make it so that clicking on the picture removes the background--active CSS class from the outer <div>, but adds the picture--active class to the <img>. Clicking the background again should restore the original CSS classes.

Visually, you should expect that clicking on the picture removes the purple background and highlights the picture border. Clicking outside the picture highlights the background, but removes the picture border highlight.

**Examples:**

Example 1 (jsx):
```jsx
const [answer, setAnswer] = useState('');const [error, setError] = useState(null);
```

Example 2 (jsx):
```jsx
const [isEmpty, setIsEmpty] = useState(true);const [isTyping, setIsTyping] = useState(false);const [isSubmitting, setIsSubmitting] = useState(false);const [isSuccess, setIsSuccess] = useState(false);const [isError, setIsError] = useState(false);
```

Example 3 (jsx):
```jsx
const [answer, setAnswer] = useState('');const [error, setError] = useState(null);const [status, setStatus] = useState('typing'); // 'typing', 'submitting', or 'success'
```

---

## React Compiler

**URL:** https://react.dev/learn/react-compiler

**Contents:**
- React Compiler
- Introduction
- Installation
- Incremental Adoption
- Debugging and Troubleshooting
- Configuration and Reference
- Additional resources

Learn what React Compiler does and how it automatically optimizes your React application by handling memoization for you, eliminating the need for manual useMemo, useCallback, and React.memo.

Get started with installing React Compiler and learn how to configure it with your build tools.

Learn strategies for gradually adopting React Compiler in your existing codebase if you’re not ready to enable it everywhere yet.

When things don’t work as expected, use our debugging guide to understand the difference between compiler errors and runtime issues, identify common breaking patterns, and follow a systematic debugging workflow.

For detailed configuration options and API reference:

In addition to these docs, we recommend checking the React Compiler Working Group for additional information and discussion about the compiler.

---

## React Developer Tools

**URL:** https://react.dev/learn/react-developer-tools

**Contents:**
- React Developer Tools
  - You will learn
- Browser extension
  - Safari and other browsers
- Mobile (React Native)

Use React Developer Tools to inspect React components, edit props and state, and identify performance problems.

The easiest way to debug websites built with React is to install the React Developer Tools browser extension. It is available for several popular browsers:

Now, if you visit a website built with React, you will see the Components and Profiler panels.

For other browsers (for example, Safari), install the react-devtools npm package:

Next open the developer tools from the terminal:

Then connect your website by adding the following <script> tag to the beginning of your website’s <head>:

Reload your website in the browser now to view it in developer tools.

To inspect apps built with React Native, you can use React Native DevTools, the built-in debugger that deeply integrates React Developer Tools. All features work identically to the browser extension, including native element highlighting and selection.

Learn more about debugging in React Native.

For versions of React Native earlier than 0.76, please use the standalone build of React DevTools by following the Safari and other browsers guide above.

**Examples:**

Example 1 (markdown):
```markdown
# Yarnyarn global add react-devtools# Npmnpm install -g react-devtools
```

Example 2 (unknown):
```unknown
react-devtools
```

Example 3 (html):
```html
<html>  <head>    <script src="http://localhost:8097"></script>
```

---

## Referencing Values with Refs

**URL:** https://react.dev/learn/referencing-values-with-refs

**Contents:**
- Referencing Values with Refs
  - You will learn
- Adding a ref to your component
- Example: building a stopwatch
- Differences between refs and state
      - Deep Dive
    - How does useRef work inside?
- When to use refs
- Best practices for refs
- Refs and the DOM

When you want a component to “remember” some information, but you don’t want that information to trigger new renders, you can use a ref.

You can add a ref to your component by importing the useRef Hook from React:

Inside your component, call the useRef Hook and pass the initial value that you want to reference as the only argument. For example, here is a ref to the value 0:

useRef returns an object like this:

Illustrated by Rachel Lee Nabors

You can access the current value of that ref through the ref.current property. This value is intentionally mutable, meaning you can both read and write to it. It’s like a secret pocket of your component that React doesn’t track. (This is what makes it an “escape hatch” from React’s one-way data flow—more on that below!)

Here, a button will increment ref.current on every click:

The ref points to a number, but, like state, you could point to anything: a string, an object, or even a function. Unlike state, ref is a plain JavaScript object with the current property that you can read and modify.

Note that the component doesn’t re-render with every increment. Like state, refs are retained by React between re-renders. However, setting state re-renders a component. Changing a ref does not!

You can combine refs and state in a single component. For example, let’s make a stopwatch that the user can start or stop by pressing a button. In order to display how much time has passed since the user pressed “Start”, you will need to keep track of when the Start button was pressed and what the current time is. This information is used for rendering, so you’ll keep it in state:

When the user presses “Start”, you’ll use setInterval in order to update the time every 10 milliseconds:

When the “Stop” button is pressed, you need to cancel the existing interval so that it stops updating the now state variable. You can do this by calling clearInterval, but you need to give it the interval ID that was previously returned by the setInterval call when the user pressed Start. You need to keep the interval ID somewhere. Since the interval ID is not used for rendering, you can keep it in a ref:

When a piece of information is used for rendering, keep it in state. When a piece of information is only needed by event handlers and changing it doesn’t require a re-render, using a ref may be more efficient.

Perhaps you’re thinking refs seem less “strict” than state—you can mutate them instead of always having to use a state setting function, for instance. But in most cases, you’ll want to use state. Refs are an “escape hatch” you won’t need often. Here’s how state and refs compare:

Here is a counter button that’s implemented with state:

Because the count value is displayed, it makes sense to use a state value for it. When the counter’s value is set with setCount(), React re-renders the component and the screen updates to reflect the new count.

If you tried to implement this with a ref, React would never re-render the component, so you’d never see the count change! See how clicking this button does not update its text:

This is why reading ref.current during render leads to unreliable code. If you need that, use state instead.

Although both useState and useRef are provided by React, in principle useRef could be implemented on top of useState. You can imagine that inside of React, useRef is implemented like this:

During the first render, useRef returns { current: initialValue }. This object is stored by React, so during the next render the same object will be returned. Note how the state setter is unused in this example. It is unnecessary because useRef always needs to return the same object!

React provides a built-in version of useRef because it is common enough in practice. But you can think of it as a regular state variable without a setter. If you’re familiar with object-oriented programming, refs might remind you of instance fields—but instead of this.something you write somethingRef.current.

Typically, you will use a ref when your component needs to “step outside” React and communicate with external APIs—often a browser API that won’t impact the appearance of the component. Here are a few of these rare situations:

If your component needs to store some value, but it doesn’t impact the rendering logic, choose refs.

Following these principles will make your components more predictable:

Limitations of React state don’t apply to refs. For example, state acts like a snapshot for every render and doesn’t update synchronously. But when you mutate the current value of a ref, it changes immediately:

This is because the ref itself is a regular JavaScript object, and so it behaves like one.

You also don’t need to worry about avoiding mutation when you work with a ref. As long as the object you’re mutating isn’t used for rendering, React doesn’t care what you do with the ref or its contents.

You can point a ref to any value. However, the most common use case for a ref is to access a DOM element. For example, this is handy if you want to focus an input programmatically. When you pass a ref to a ref attribute in JSX, like <div ref={myRef}>, React will put the corresponding DOM element into myRef.current. Once the element is removed from the DOM, React will update myRef.current to be null. You can read more about this in Manipulating the DOM with Refs.

Type a message and click “Send”. You will notice there is a three second delay before you see the “Sent!” alert. During this delay, you can see an “Undo” button. Click it. This “Undo” button is supposed to stop the “Sent!” message from appearing. It does this by calling clearTimeout for the timeout ID saved during handleSend. However, even after “Undo” is clicked, the “Sent!” message still appears. Find why it doesn’t work, and fix it.

**Examples:**

Example 1 (sql):
```sql
import { useRef } from 'react';
```

Example 2 (jsx):
```jsx
const ref = useRef(0);
```

Example 3 (json):
```json
{   current: 0 // The value you passed to useRef}
```

Example 4 (jsx):
```jsx
const [startTime, setStartTime] = useState(null);const [now, setNow] = useState(null);
```

---

## Removing Effect Dependencies

**URL:** https://react.dev/learn/removing-effect-dependencies

**Contents:**
- Removing Effect Dependencies
  - You will learn
- Dependencies should match the code
  - To remove a dependency, prove that it’s not a dependency
  - To change the dependencies, change the code
  - Pitfall
      - Deep Dive
    - Why is suppressing the dependency linter so dangerous?
- Removing unnecessary dependencies
  - Should this code move to an event handler?

When you write an Effect, the linter will verify that you’ve included every reactive value (like props and state) that the Effect reads in the list of your Effect’s dependencies. This ensures that your Effect remains synchronized with the latest props and state of your component. Unnecessary dependencies may cause your Effect to run too often, or even create an infinite loop. Follow this guide to review and remove unnecessary dependencies from your Effects.

When you write an Effect, you first specify how to start and stop whatever you want your Effect to be doing:

Then, if you leave the Effect dependencies empty ([]), the linter will suggest the correct dependencies:

Fill them in according to what the linter says:

Effects “react” to reactive values. Since roomId is a reactive value (it can change due to a re-render), the linter verifies that you’ve specified it as a dependency. If roomId receives a different value, React will re-synchronize your Effect. This ensures that the chat stays connected to the selected room and “reacts” to the dropdown:

Notice that you can’t “choose” the dependencies of your Effect. Every reactive value used by your Effect’s code must be declared in your dependency list. The dependency list is determined by the surrounding code:

Reactive values include props and all variables and functions declared directly inside of your component. Since roomId is a reactive value, you can’t remove it from the dependency list. The linter wouldn’t allow it:

And the linter would be right! Since roomId may change over time, this would introduce a bug in your code.

To remove a dependency, “prove” to the linter that it doesn’t need to be a dependency. For example, you can move roomId out of your component to prove that it’s not reactive and won’t change on re-renders:

Now that roomId is not a reactive value (and can’t change on a re-render), it doesn’t need to be a dependency:

This is why you could now specify an empty ([]) dependency list. Your Effect really doesn’t depend on any reactive value anymore, so it really doesn’t need to re-run when any of the component’s props or state change.

You might have noticed a pattern in your workflow:

The last part is important. If you want to change the dependencies, change the surrounding code first. You can think of the dependency list as a list of all the reactive values used by your Effect’s code. You don’t choose what to put on that list. The list describes your code. To change the dependency list, change the code.

This might feel like solving an equation. You might start with a goal (for example, to remove a dependency), and you need to “find” the code matching that goal. Not everyone finds solving equations fun, and the same thing could be said about writing Effects! Luckily, there is a list of common recipes that you can try below.

If you have an existing codebase, you might have some Effects that suppress the linter like this:

When dependencies don’t match the code, there is a very high risk of introducing bugs. By suppressing the linter, you “lie” to React about the values your Effect depends on.

Instead, use the techniques below.

Suppressing the linter leads to very unintuitive bugs that are hard to find and fix. Here’s one example:

Let’s say that you wanted to run the Effect “only on mount”. You’ve read that empty ([]) dependencies do that, so you’ve decided to ignore the linter, and forcefully specified [] as the dependencies.

This counter was supposed to increment every second by the amount configurable with the two buttons. However, since you “lied” to React that this Effect doesn’t depend on anything, React forever keeps using the onTick function from the initial render. During that render, count was 0 and increment was 1. This is why onTick from that render always calls setCount(0 + 1) every second, and you always see 1. Bugs like this are harder to fix when they’re spread across multiple components.

There’s always a better solution than ignoring the linter! To fix this code, you need to add onTick to the dependency list. (To ensure the interval is only setup once, make onTick an Effect Event.)

We recommend treating the dependency lint error as a compilation error. If you don’t suppress it, you will never see bugs like this. The rest of this page documents the alternatives for this and other cases.

Every time you adjust the Effect’s dependencies to reflect the code, look at the dependency list. Does it make sense for the Effect to re-run when any of these dependencies change? Sometimes, the answer is “no”:

To find the right solution, you’ll need to answer a few questions about your Effect. Let’s walk through them.

The first thing you should think about is whether this code should be an Effect at all.

Imagine a form. On submit, you set the submitted state variable to true. You need to send a POST request and show a notification. You’ve put this logic inside an Effect that “reacts” to submitted being true:

Later, you want to style the notification message according to the current theme, so you read the current theme. Since theme is declared in the component body, it is a reactive value, so you add it as a dependency:

By doing this, you’ve introduced a bug. Imagine you submit the form first and then switch between Dark and Light themes. The theme will change, the Effect will re-run, and so it will display the same notification again!

The problem here is that this shouldn’t be an Effect in the first place. You want to send this POST request and show the notification in response to submitting the form, which is a particular interaction. To run some code in response to particular interaction, put that logic directly into the corresponding event handler:

Now that the code is in an event handler, it’s not reactive—so it will only run when the user submits the form. Read more about choosing between event handlers and Effects and how to delete unnecessary Effects.

The next question you should ask yourself is whether your Effect is doing several unrelated things.

Imagine you’re creating a shipping form where the user needs to choose their city and area. You fetch the list of cities from the server according to the selected country to show them in a dropdown:

This is a good example of fetching data in an Effect. You are synchronizing the cities state with the network according to the country prop. You can’t do this in an event handler because you need to fetch as soon as ShippingForm is displayed and whenever the country changes (no matter which interaction causes it).

Now let’s say you’re adding a second select box for city areas, which should fetch the areas for the currently selected city. You might start by adding a second fetch call for the list of areas inside the same Effect:

However, since the Effect now uses the city state variable, you’ve had to add city to the list of dependencies. That, in turn, introduced a problem: when the user selects a different city, the Effect will re-run and call fetchCities(country). As a result, you will be unnecessarily refetching the list of cities many times.

The problem with this code is that you’re synchronizing two different unrelated things:

Split the logic into two Effects, each of which reacts to the prop that it needs to synchronize with:

Now the first Effect only re-runs if the country changes, while the second Effect re-runs when the city changes. You’ve separated them by purpose: two different things are synchronized by two separate Effects. Two separate Effects have two separate dependency lists, so they won’t trigger each other unintentionally.

The final code is longer than the original, but splitting these Effects is still correct. Each Effect should represent an independent synchronization process. In this example, deleting one Effect doesn’t break the other Effect’s logic. This means they synchronize different things, and it’s good to split them up. If you’re concerned about duplication, you can improve this code by extracting repetitive logic into a custom Hook.

This Effect updates the messages state variable with a newly created array every time a new message arrives:

It uses the messages variable to create a new array starting with all the existing messages and adds the new message at the end. However, since messages is a reactive value read by an Effect, it must be a dependency:

And making messages a dependency introduces a problem.

Every time you receive a message, setMessages() causes the component to re-render with a new messages array that includes the received message. However, since this Effect now depends on messages, this will also re-synchronize the Effect. So every new message will make the chat re-connect. The user would not like that!

To fix the issue, don’t read messages inside the Effect. Instead, pass an updater function to setMessages:

Notice how your Effect does not read the messages variable at all now. You only need to pass an updater function like msgs => [...msgs, receivedMessage]. React puts your updater function in a queue and will provide the msgs argument to it during the next render. This is why the Effect itself doesn’t need to depend on messages anymore. As a result of this fix, receiving a chat message will no longer make the chat re-connect.

Suppose that you want to play a sound when the user receives a new message unless isMuted is true:

Since your Effect now uses isMuted in its code, you have to add it to the dependencies:

The problem is that every time isMuted changes (for example, when the user presses the “Muted” toggle), the Effect will re-synchronize, and reconnect to the chat. This is not the desired user experience! (In this example, even disabling the linter would not work—if you do that, isMuted would get “stuck” with its old value.)

To solve this problem, you need to extract the logic that shouldn’t be reactive out of the Effect. You don’t want this Effect to “react” to the changes in isMuted. Move this non-reactive piece of logic into an Effect Event:

Effect Events let you split an Effect into reactive parts (which should “react” to reactive values like roomId and their changes) and non-reactive parts (which only read their latest values, like onMessage reads isMuted). Now that you read isMuted inside an Effect Event, it doesn’t need to be a dependency of your Effect. As a result, the chat won’t re-connect when you toggle the “Muted” setting on and off, solving the original issue!

You might run into a similar problem when your component receives an event handler as a prop:

Suppose that the parent component passes a different onReceiveMessage function on every render:

Since onReceiveMessage is a dependency, it would cause the Effect to re-synchronize after every parent re-render. This would make it re-connect to the chat. To solve this, wrap the call in an Effect Event:

Effect Events aren’t reactive, so you don’t need to specify them as dependencies. As a result, the chat will no longer re-connect even if the parent component passes a function that’s different on every re-render.

In this example, you want to log a visit every time roomId changes. You want to include the current notificationCount with every log, but you don’t want a change to notificationCount to trigger a log event.

The solution is again to split out the non-reactive code into an Effect Event:

You want your logic to be reactive with regards to roomId, so you read roomId inside of your Effect. However, you don’t want a change to notificationCount to log an extra visit, so you read notificationCount inside of the Effect Event. Learn more about reading the latest props and state from Effects using Effect Events.

Sometimes, you do want your Effect to “react” to a certain value, but that value changes more often than you’d like—and might not reflect any actual change from the user’s perspective. For example, let’s say that you create an options object in the body of your component, and then read that object from inside of your Effect:

This object is declared in the component body, so it’s a reactive value. When you read a reactive value like this inside an Effect, you declare it as a dependency. This ensures your Effect “reacts” to its changes:

It is important to declare it as a dependency! This ensures, for example, that if the roomId changes, your Effect will re-connect to the chat with the new options. However, there is also a problem with the code above. To see it, try typing into the input in the sandbox below, and watch what happens in the console:

In the sandbox above, the input only updates the message state variable. From the user’s perspective, this should not affect the chat connection. However, every time you update the message, your component re-renders. When your component re-renders, the code inside of it runs again from scratch.

A new options object is created from scratch on every re-render of the ChatRoom component. React sees that the options object is a different object from the options object created during the last render. This is why it re-synchronizes your Effect (which depends on options), and the chat re-connects as you type.

This problem only affects objects and functions. In JavaScript, each newly created object and function is considered distinct from all the others. It doesn’t matter that the contents inside of them may be the same!

Object and function dependencies can make your Effect re-synchronize more often than you need.

This is why, whenever possible, you should try to avoid objects and functions as your Effect’s dependencies. Instead, try moving them outside the component, inside the Effect, or extracting primitive values out of them.

If the object does not depend on any props and state, you can move that object outside your component:

This way, you prove to the linter that it’s not reactive. It can’t change as a result of a re-render, so it doesn’t need to be a dependency. Now re-rendering ChatRoom won’t cause your Effect to re-synchronize.

This works for functions too:

Since createOptions is declared outside your component, it’s not a reactive value. This is why it doesn’t need to be specified in your Effect’s dependencies, and why it won’t ever cause your Effect to re-synchronize.

If your object depends on some reactive value that may change as a result of a re-render, like a roomId prop, you can’t pull it outside your component. You can, however, move its creation inside of your Effect’s code:

Now that options is declared inside of your Effect, it is no longer a dependency of your Effect. Instead, the only reactive value used by your Effect is roomId. Since roomId is not an object or function, you can be sure that it won’t be unintentionally different. In JavaScript, numbers and strings are compared by their content:

Thanks to this fix, the chat no longer re-connects if you edit the input:

However, it does re-connect when you change the roomId dropdown, as you would expect.

This works for functions, too:

You can write your own functions to group pieces of logic inside your Effect. As long as you also declare them inside your Effect, they’re not reactive values, and so they don’t need to be dependencies of your Effect.

Sometimes, you may receive an object from props:

The risk here is that the parent component will create the object during rendering:

This would cause your Effect to re-connect every time the parent component re-renders. To fix this, read information from the object outside the Effect, and avoid having object and function dependencies:

The logic gets a little repetitive (you read some values from an object outside an Effect, and then create an object with the same values inside the Effect). But it makes it very explicit what information your Effect actually depends on. If an object is re-created unintentionally by the parent component, the chat would not re-connect. However, if options.roomId or options.serverUrl really are different, the chat would re-connect.

The same approach can work for functions. For example, suppose the parent component passes a function:

To avoid making it a dependency (and causing it to re-connect on re-renders), call it outside the Effect. This gives you the roomId and serverUrl values that aren’t objects, and that you can read from inside your Effect:

This only works for pure functions because they are safe to call during rendering. If your function is an event handler, but you don’t want its changes to re-synchronize your Effect, wrap it into an Effect Event instead.

This Effect sets up an interval that ticks every second. You’ve noticed something strange happening: it seems like the interval gets destroyed and re-created every time it ticks. Fix the code so that the interval doesn’t get constantly re-created.

**Examples:**

Example 1 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => connection.disconnect();  	// ...}
```

Example 2 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]); // ✅ All dependencies declared  // ...}
```

Example 3 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId }) { // This is a reactive value  useEffect(() => {    const connection = createConnection(serverUrl, roomId); // This Effect reads that reactive value    connection.connect();    return () => connection.disconnect();  }, [roomId]); // ✅ So you must specify that reactive value as a dependency of your Effect  // ...}
```

Example 4 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => connection.disconnect();  }, []); // 🔴 React Hook useEffect has a missing dependency: 'roomId'  // ...}
```

---

## Rendering Lists

**URL:** https://react.dev/learn/rendering-lists

**Contents:**
- Rendering Lists
  - You will learn
- Rendering data from arrays
- Filtering arrays of items
  - Pitfall
- Keeping list items in order with key
  - Note
      - Deep Dive
    - Displaying several DOM nodes for each list item
  - Where to get your key

You will often want to display multiple similar components from a collection of data. You can use the JavaScript array methods to manipulate an array of data. On this page, you’ll use filter() and map() with React to filter and transform your array of data into an array of components.

Say that you have a list of content.

The only difference among those list items is their contents, their data. You will often need to show several instances of the same component using different data when building interfaces: from lists of comments to galleries of profile images. In these situations, you can store that data in JavaScript objects and arrays and use methods like map() and filter() to render lists of components from them.

Here’s a short example of how to generate a list of items from an array:

Notice the sandbox above displays a console error:

You’ll learn how to fix this error later on this page. Before we get to that, let’s add some structure to your data.

This data can be structured even more.

Let’s say you want a way to only show people whose profession is 'chemist'. You can use JavaScript’s filter() method to return just those people. This method takes an array of items, passes them through a “test” (a function that returns true or false), and returns a new array of only those items that passed the test (returned true).

You only want the items where profession is 'chemist'. The “test” function for this looks like (person) => person.profession === 'chemist'. Here’s how to put it together:

Arrow functions implicitly return the expression right after =>, so you didn’t need a return statement:

However, you must write return explicitly if your => is followed by a { curly brace!

Arrow functions containing => { are said to have a “block body”. They let you write more than a single line of code, but you have to write a return statement yourself. If you forget it, nothing gets returned!

Notice that all the sandboxes above show an error in the console:

You need to give each array item a key — a string or a number that uniquely identifies it among other items in that array:

JSX elements directly inside a map() call always need keys!

Keys tell React which array item each component corresponds to, so that it can match them up later. This becomes important if your array items can move (e.g. due to sorting), get inserted, or get deleted. A well-chosen key helps React infer what exactly has happened, and make the correct updates to the DOM tree.

Rather than generating keys on the fly, you should include them in your data:

What do you do when each item needs to render not one, but several DOM nodes?

The short <>...</> Fragment syntax won’t let you pass a key, so you need to either group them into a single <div>, or use the slightly longer and more explicit <Fragment> syntax:

Fragments disappear from the DOM, so this will produce a flat list of <h1>, <p>, <h1>, <p>, and so on.

Different sources of data provide different sources of keys:

Imagine that files on your desktop didn’t have names. Instead, you’d refer to them by their order — the first file, the second file, and so on. You could get used to it, but once you delete a file, it would get confusing. The second file would become the first file, the third file would be the second file, and so on.

File names in a folder and JSX keys in an array serve a similar purpose. They let us uniquely identify an item between its siblings. A well-chosen key provides more information than the position within the array. Even if the position changes due to reordering, the key lets React identify the item throughout its lifetime.

You might be tempted to use an item’s index in the array as its key. In fact, that’s what React will use if you don’t specify a key at all. But the order in which you render items will change over time if an item is inserted, deleted, or if the array gets reordered. Index as a key often leads to subtle and confusing bugs.

Similarly, do not generate keys on the fly, e.g. with key={Math.random()}. This will cause keys to never match up between renders, leading to all your components and DOM being recreated every time. Not only is this slow, but it will also lose any user input inside the list items. Instead, use a stable ID based on the data.

Note that your components won’t receive key as a prop. It’s only used as a hint by React itself. If your component needs an ID, you have to pass it as a separate prop: <Profile key={id} userId={id} />.

On this page you learned:

This example shows a list of all people.

Change it to show two separate lists one after another: Chemists and Everyone Else. Like previously, you can determine whether a person is a chemist by checking if person.profession === 'chemist'.

**Examples:**

Example 1 (typescript):
```typescript
<ul>  <li>Creola Katherine Johnson: mathematician</li>  <li>Mario José Molina-Pasquel Henríquez: chemist</li>  <li>Mohammad Abdus Salam: physicist</li>  <li>Percy Lavon Julian: chemist</li>  <li>Subrahmanyan Chandrasekhar: astrophysicist</li></ul>
```

Example 2 (javascript):
```javascript
const people = [  'Creola Katherine Johnson: mathematician',  'Mario José Molina-Pasquel Henríquez: chemist',  'Mohammad Abdus Salam: physicist',  'Percy Lavon Julian: chemist',  'Subrahmanyan Chandrasekhar: astrophysicist'];
```

Example 3 (typescript):
```typescript
const listItems = people.map(person => <li>{person}</li>);
```

Example 4 (typescript):
```typescript
return <ul>{listItems}</ul>;
```

---

## Render and Commit

**URL:** https://react.dev/learn/render-and-commit

**Contents:**
- Render and Commit
  - You will learn
- Step 1: Trigger a render
  - Initial render
  - Re-renders when state updates
- Step 2: React renders your components
  - Pitfall
      - Deep Dive
    - Optimizing performance
- Step 3: React commits changes to the DOM

Before your components are displayed on screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

There are two reasons for a component to render:

When your app starts, you need to trigger the initial render. Frameworks and sandboxes sometimes hide this code, but it’s done by calling createRoot with the target DOM node, and then calling its render method with your component:

Try commenting out the root.render() call and see the component disappear!

Once the component has been initially rendered, you can trigger further renders by updating its state with the set function. Updating your component’s state automatically queues a render. (You can imagine these as a restaurant guest ordering tea, dessert, and all sorts of things after putting in their first order, depending on the state of their thirst or hunger.)

Illustrated by Rachel Lee Nabors

After you trigger a render, React calls your components to figure out what to display on screen. “Rendering” is React calling your components.

This process is recursive: if the updated component returns some other component, React will render that component next, and if that component also returns something, it will render that component next, and so on. The process will continue until there are no more nested components and React knows exactly what should be displayed on screen.

In the following example, React will call Gallery() and Image() several times:

Rendering must always be a pure calculation:

Otherwise, you can encounter confusing bugs and unpredictable behavior as your codebase grows in complexity. When developing in “Strict Mode”, React calls each component’s function twice, which can help surface mistakes caused by impure functions.

The default behavior of rendering all components nested within the updated component is not optimal for performance if the updated component is very high in the tree. If you run into a performance issue, there are several opt-in ways to solve it described in the Performance section. Don’t optimize prematurely!

After rendering (calling) your components, React will modify the DOM.

React only changes the DOM nodes if there’s a difference between renders. For example, here is a component that re-renders with different props passed from its parent every second. Notice how you can add some text into the <input>, updating its value, but the text doesn’t disappear when the component re-renders:

This works because during this last step, React only updates the content of <h1> with the new time. It sees that the <input> appears in the JSX in the same place as last time, so React doesn’t touch the <input>—or its value!

After rendering is done and React updated the DOM, the browser will repaint the screen. Although this process is known as “browser rendering”, we’ll refer to it as “painting” to avoid confusion throughout the docs.

Illustrated by Rachel Lee Nabors

---

## Responding to Events

**URL:** https://react.dev/learn/responding-to-events

**Contents:**
- Responding to Events
  - You will learn
- Adding event handlers
  - Pitfall
  - Reading props in event handlers
  - Passing event handlers as props
  - Naming event handler props
  - Note
- Event propagation
  - Pitfall

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to interactions like clicking, hovering, focusing form inputs, and so on.

To add an event handler, you will first define a function and then pass it as a prop to the appropriate JSX tag. For example, here is a button that doesn’t do anything yet:

You can make it show a message when a user clicks by following these three steps:

You defined the handleClick function and then passed it as a prop to <button>. handleClick is an event handler. Event handler functions:

By convention, it is common to name event handlers as handle followed by the event name. You’ll often see onClick={handleClick}, onMouseEnter={handleMouseEnter}, and so on.

Alternatively, you can define an event handler inline in the JSX:

Or, more concisely, using an arrow function:

All of these styles are equivalent. Inline event handlers are convenient for short functions.

Functions passed to event handlers must be passed, not called. For example:

The difference is subtle. In the first example, the handleClick function is passed as an onClick event handler. This tells React to remember it and only call your function when the user clicks the button.

In the second example, the () at the end of handleClick() fires the function immediately during rendering, without any clicks. This is because JavaScript inside the JSX { and } executes right away.

When you write code inline, the same pitfall presents itself in a different way:

Passing inline code like this won’t fire on click—it fires every time the component renders:

If you want to define your event handler inline, wrap it in an anonymous function like so:

Rather than executing the code inside with every render, this creates a function to be called later.

In both cases, what you want to pass is a function:

Read more about arrow functions.

Because event handlers are declared inside of a component, they have access to the component’s props. Here is a button that, when clicked, shows an alert with its message prop:

This lets these two buttons show different messages. Try changing the messages passed to them.

Often you’ll want the parent component to specify a child’s event handler. Consider buttons: depending on where you’re using a Button component, you might want to execute a different function—perhaps one plays a movie and another uploads an image.

To do this, pass a prop the component receives from its parent as the event handler like so:

Here, the Toolbar component renders a PlayButton and an UploadButton:

Finally, your Button component accepts a prop called onClick. It passes that prop directly to the built-in browser <button> with onClick={onClick}. This tells React to call the passed function on click.

If you use a design system, it’s common for components like buttons to contain styling but not specify behavior. Instead, components like PlayButton and UploadButton will pass event handlers down.

Built-in components like <button> and <div> only support browser event names like onClick. However, when you’re building your own components, you can name their event handler props any way that you like.

By convention, event handler props should start with on, followed by a capital letter.

For example, the Button component’s onClick prop could have been called onSmash:

In this example, <button onClick={onSmash}> shows that the browser <button> (lowercase) still needs a prop called onClick, but the prop name received by your custom Button component is up to you!

When your component supports multiple interactions, you might name event handler props for app-specific concepts. For example, this Toolbar component receives onPlayMovie and onUploadImage event handlers:

Notice how the App component does not need to know what Toolbar will do with onPlayMovie or onUploadImage. That’s an implementation detail of the Toolbar. Here, Toolbar passes them down as onClick handlers to its Buttons, but it could later also trigger them on a keyboard shortcut. Naming props after app-specific interactions like onPlayMovie gives you the flexibility to change how they’re used later.

Make sure that you use the appropriate HTML tags for your event handlers. For example, to handle clicks, use <button onClick={handleClick}> instead of <div onClick={handleClick}>. Using a real browser <button> enables built-in browser behaviors like keyboard navigation. If you don’t like the default browser styling of a button and want to make it look more like a link or a different UI element, you can achieve it with CSS. Learn more about writing accessible markup.

Event handlers will also catch events from any children your component might have. We say that an event “bubbles” or “propagates” up the tree: it starts with where the event happened, and then goes up the tree.

This <div> contains two buttons. Both the <div> and each button have their own onClick handlers. Which handlers do you think will fire when you click a button?

If you click on either button, its onClick will run first, followed by the parent <div>’s onClick. So two messages will appear. If you click the toolbar itself, only the parent <div>’s onClick will run.

All events propagate in React except onScroll, which only works on the JSX tag you attach it to.

Event handlers receive an event object as their only argument. By convention, it’s usually called e, which stands for “event”. You can use this object to read information about the event.

That event object also lets you stop the propagation. If you want to prevent an event from reaching parent components, you need to call e.stopPropagation() like this Button component does:

When you click on a button:

As a result of e.stopPropagation(), clicking on the buttons now only shows a single alert (from the <button>) rather than the two of them (from the <button> and the parent toolbar <div>). Clicking a button is not the same thing as clicking the surrounding toolbar, so stopping the propagation makes sense for this UI.

In rare cases, you might need to catch all events on child elements, even if they stopped propagation. For example, maybe you want to log every click to analytics, regardless of the propagation logic. You can do this by adding Capture at the end of the event name:

Each event propagates in three phases:

Capture events are useful for code like routers or analytics, but you probably won’t use them in app code.

Notice how this click handler runs a line of code and then calls the onClick prop passed by the parent:

You could add more code to this handler before calling the parent onClick event handler, too. This pattern provides an alternative to propagation. It lets the child component handle the event, while also letting the parent component specify some additional behavior. Unlike propagation, it’s not automatic. But the benefit of this pattern is that you can clearly follow the whole chain of code that executes as a result of some event.

If you rely on propagation and it’s difficult to trace which handlers execute and why, try this approach instead.

Some browser events have default behavior associated with them. For example, a <form> submit event, which happens when a button inside of it is clicked, will reload the whole page by default:

You can call e.preventDefault() on the event object to stop this from happening:

Don’t confuse e.stopPropagation() and e.preventDefault(). They are both useful, but are unrelated:

Absolutely! Event handlers are the best place for side effects.

Unlike rendering functions, event handlers don’t need to be pure, so it’s a great place to change something—for example, change an input’s value in response to typing, or change a list in response to a button press. However, in order to change some information, you first need some way to store it. In React, this is done by using state, a component’s memory. You will learn all about it on the next page.

Clicking this button is supposed to switch the page background between white and black. However, nothing happens when you click it. Fix the problem. (Don’t worry about the logic inside handleClick—that part is fine.)

**Examples:**

Example 1 (jsx):
```jsx
<button onClick={function handleClick() {  alert('You clicked me!');}}>
```

Example 2 (jsx):
```jsx
<button onClick={() => {  alert('You clicked me!');}}>
```

Example 3 (jsx):
```jsx
// This alert fires when the component renders, not when clicked!<button onClick={alert('You clicked me!')}>
```

Example 4 (jsx):
```jsx
<button onClick={() => alert('You clicked me!')}>
```

---

## Reusing Logic with Custom Hooks

**URL:** https://react.dev/learn/reusing-logic-with-custom-hooks

**Contents:**
- Reusing Logic with Custom Hooks
  - You will learn
- Custom Hooks: Sharing logic between components
  - Extracting your own custom Hook from a component
  - Hook names always start with use
  - Note
      - Deep Dive
    - Should all functions called during rendering start with the use prefix?
  - Custom Hooks let you share stateful logic, not state itself
- Passing reactive values between Hooks

React comes with several built-in Hooks like useState, useContext, and useEffect. Sometimes, you’ll wish that there was a Hook for some more specific purpose: for example, to fetch data, to keep track of whether the user is online, or to connect to a chat room. You might not find these Hooks in React, but you can create your own Hooks for your application’s needs.

Imagine you’re developing an app that heavily relies on the network (as most apps do). You want to warn the user if their network connection has accidentally gone off while they were using your app. How would you go about it? It seems like you’ll need two things in your component:

This will keep your component synchronized with the network status. You might start with something like this:

Try turning your network on and off, and notice how this StatusBar updates in response to your actions.

Now imagine you also want to use the same logic in a different component. You want to implement a Save button that will become disabled and show “Reconnecting…” instead of “Save” while the network is off.

To start, you can copy and paste the isOnline state and the Effect into SaveButton:

Verify that, if you turn off the network, the button will change its appearance.

These two components work fine, but the duplication in logic between them is unfortunate. It seems like even though they have different visual appearance, you want to reuse the logic between them.

Imagine for a moment that, similar to useState and useEffect, there was a built-in useOnlineStatus Hook. Then both of these components could be simplified and you could remove the duplication between them:

Although there is no such built-in Hook, you can write it yourself. Declare a function called useOnlineStatus and move all the duplicated code into it from the components you wrote earlier:

At the end of the function, return isOnline. This lets your components read that value:

Verify that switching the network on and off updates both components.

Now your components don’t have as much repetitive logic. More importantly, the code inside them describes what they want to do (use the online status!) rather than how to do it (by subscribing to the browser events).

When you extract logic into custom Hooks, you can hide the gnarly details of how you deal with some external system or a browser API. The code of your components expresses your intent, not the implementation.

React applications are built from components. Components are built from Hooks, whether built-in or custom. You’ll likely often use custom Hooks created by others, but occasionally you might write one yourself!

You must follow these naming conventions:

This convention guarantees that you can always look at a component and know where its state, Effects, and other React features might “hide”. For example, if you see a getColor() function call inside your component, you can be sure that it can’t possibly contain React state inside because its name doesn’t start with use. However, a function call like useOnlineStatus() will most likely contain calls to other Hooks inside!

If your linter is configured for React, it will enforce this naming convention. Scroll up to the sandbox above and rename useOnlineStatus to getOnlineStatus. Notice that the linter won’t allow you to call useState or useEffect inside of it anymore. Only Hooks and components can call other Hooks!

No. Functions that don’t call Hooks don’t need to be Hooks.

If your function doesn’t call any Hooks, avoid the use prefix. Instead, write it as a regular function without the use prefix. For example, useSorted below doesn’t call Hooks, so call it getSorted instead:

This ensures that your code can call this regular function anywhere, including conditions:

You should give use prefix to a function (and thus make it a Hook) if it uses at least one Hook inside of it:

Technically, this isn’t enforced by React. In principle, you could make a Hook that doesn’t call other Hooks. This is often confusing and limiting so it’s best to avoid that pattern. However, there may be rare cases where it is helpful. For example, maybe your function doesn’t use any Hooks right now, but you plan to add some Hook calls to it in the future. Then it makes sense to name it with the use prefix:

Then components won’t be able to call it conditionally. This will become important when you actually add Hook calls inside. If you don’t plan to use Hooks inside it (now or later), don’t make it a Hook.

In the earlier example, when you turned the network on and off, both components updated together. However, it’s wrong to think that a single isOnline state variable is shared between them. Look at this code:

It works the same way as before you extracted the duplication:

These are two completely independent state variables and Effects! They happened to have the same value at the same time because you synchronized them with the same external value (whether the network is on).

To better illustrate this, we’ll need a different example. Consider this Form component:

There’s some repetitive logic for each form field:

You can extract the repetitive logic into this useFormInput custom Hook:

Notice that it only declares one state variable called value.

However, the Form component calls useFormInput two times:

This is why it works like declaring two separate state variables!

Custom Hooks let you share stateful logic but not state itself. Each call to a Hook is completely independent from every other call to the same Hook. This is why the two sandboxes above are completely equivalent. If you’d like, scroll back up and compare them. The behavior before and after extracting a custom Hook is identical.

When you need to share the state itself between multiple components, lift it up and pass it down instead.

The code inside your custom Hooks will re-run during every re-render of your component. This is why, like components, custom Hooks need to be pure. Think of custom Hooks’ code as part of your component’s body!

Because custom Hooks re-render together with your component, they always receive the latest props and state. To see what this means, consider this chat room example. Change the server URL or the chat room:

When you change serverUrl or roomId, the Effect “reacts” to your changes and re-synchronizes. You can tell by the console messages that the chat re-connects every time that you change your Effect’s dependencies.

Now move the Effect’s code into a custom Hook:

This lets your ChatRoom component call your custom Hook without worrying about how it works inside:

This looks much simpler! (But it does the same thing.)

Notice that the logic still responds to prop and state changes. Try editing the server URL or the selected room:

Notice how you’re taking the return value of one Hook:

and passing it as an input to another Hook:

Every time your ChatRoom component re-renders, it passes the latest roomId and serverUrl to your Hook. This is why your Effect re-connects to the chat whenever their values are different after a re-render. (If you ever worked with audio or video processing software, chaining Hooks like this might remind you of chaining visual or audio effects. It’s as if the output of useState “feeds into” the input of the useChatRoom.)

As you start using useChatRoom in more components, you might want to let components customize its behavior. For example, currently, the logic for what to do when a message arrives is hardcoded inside the Hook:

Let’s say you want to move this logic back to your component:

To make this work, change your custom Hook to take onReceiveMessage as one of its named options:

This will work, but there’s one more improvement you can do when your custom Hook accepts event handlers.

Adding a dependency on onReceiveMessage is not ideal because it will cause the chat to re-connect every time the component re-renders. Wrap this event handler into an Effect Event to remove it from the dependencies:

Now the chat won’t re-connect every time that the ChatRoom component re-renders. Here is a fully working demo of passing an event handler to a custom Hook that you can play with:

Notice how you no longer need to know how useChatRoom works in order to use it. You could add it to any other component, pass any other options, and it would work the same way. That’s the power of custom Hooks.

You don’t need to extract a custom Hook for every little duplicated bit of code. Some duplication is fine. For example, extracting a useFormInput Hook to wrap a single useState call like earlier is probably unnecessary.

However, whenever you write an Effect, consider whether it would be clearer to also wrap it in a custom Hook. You shouldn’t need Effects very often, so if you’re writing one, it means that you need to “step outside React” to synchronize with some external system or to do something that React doesn’t have a built-in API for. Wrapping it into a custom Hook lets you precisely communicate your intent and how the data flows through it.

For example, consider a ShippingForm component that displays two dropdowns: one shows the list of cities, and another shows the list of areas in the selected city. You might start with some code that looks like this:

Although this code is quite repetitive, it’s correct to keep these Effects separate from each other. They synchronize two different things, so you shouldn’t merge them into one Effect. Instead, you can simplify the ShippingForm component above by extracting the common logic between them into your own useData Hook:

Now you can replace both Effects in the ShippingForm components with calls to useData:

Extracting a custom Hook makes the data flow explicit. You feed the url in and you get the data out. By “hiding” your Effect inside useData, you also prevent someone working on the ShippingForm component from adding unnecessary dependencies to it. With time, most of your app’s Effects will be in custom Hooks.

Start by choosing your custom Hook’s name. If you struggle to pick a clear name, it might mean that your Effect is too coupled to the rest of your component’s logic, and is not yet ready to be extracted.

Ideally, your custom Hook’s name should be clear enough that even a person who doesn’t write code often could have a good guess about what your custom Hook does, what it takes, and what it returns:

When you synchronize with an external system, your custom Hook name may be more technical and use jargon specific to that system. It’s good as long as it would be clear to a person familiar with that system:

Keep custom Hooks focused on concrete high-level use cases. Avoid creating and using custom “lifecycle” Hooks that act as alternatives and convenience wrappers for the useEffect API itself:

For example, this useMount Hook tries to ensure some code only runs “on mount”:

Custom “lifecycle” Hooks like useMount don’t fit well into the React paradigm. For example, this code example has a mistake (it doesn’t “react” to roomId or serverUrl changes), but the linter won’t warn you about it because the linter only checks direct useEffect calls. It won’t know about your Hook.

If you’re writing an Effect, start by using the React API directly:

Then, you can (but don’t have to) extract custom Hooks for different high-level use cases:

A good custom Hook makes the calling code more declarative by constraining what it does. For example, useChatRoom(options) can only connect to the chat room, while useImpressionLog(eventName, extraData) can only send an impression log to the analytics. If your custom Hook API doesn’t constrain the use cases and is very abstract, in the long run it’s likely to introduce more problems than it solves.

Effects are an “escape hatch”: you use them when you need to “step outside React” and when there is no better built-in solution for your use case. With time, the React team’s goal is to reduce the number of the Effects in your app to the minimum by providing more specific solutions to more specific problems. Wrapping your Effects in custom Hooks makes it easier to upgrade your code when these solutions become available.

Let’s return to this example:

In the above example, useOnlineStatus is implemented with a pair of useState and useEffect. However, this isn’t the best possible solution. There is a number of edge cases it doesn’t consider. For example, it assumes that when the component mounts, isOnline is already true, but this may be wrong if the network already went offline. You can use the browser navigator.onLine API to check for that, but using it directly would not work on the server for generating the initial HTML. In short, this code could be improved.

React includes a dedicated API called useSyncExternalStore which takes care of all of these problems for you. Here is your useOnlineStatus Hook, rewritten to take advantage of this new API:

Notice how you didn’t need to change any of the components to make this migration:

This is another reason for why wrapping Effects in custom Hooks is often beneficial:

Similar to a design system, you might find it helpful to start extracting common idioms from your app’s components into custom Hooks. This will keep your components’ code focused on the intent, and let you avoid writing raw Effects very often. Many excellent custom Hooks are maintained by the React community.

Today, with the use API, data can be read in render by passing a Promise to use:

We’re still working out the details, but we expect that in the future, you’ll write data fetching like this:

If you use custom Hooks like useData above in your app, it will require fewer changes to migrate to the eventually recommended approach than if you write raw Effects in every component manually. However, the old approach will still work fine, so if you feel happy writing raw Effects, you can continue to do that.

Let’s say you want to implement a fade-in animation from scratch using the browser requestAnimationFrame API. You might start with an Effect that sets up an animation loop. During each frame of the animation, you could change the opacity of the DOM node you hold in a ref until it reaches 1. Your code might start like this:

To make the component more readable, you might extract the logic into a useFadeIn custom Hook:

You could keep the useFadeIn code as is, but you could also refactor it more. For example, you could extract the logic for setting up the animation loop out of useFadeIn into a custom useAnimationLoop Hook:

However, you didn’t have to do that. As with regular functions, ultimately you decide where to draw the boundaries between different parts of your code. You could also take a very different approach. Instead of keeping the logic in the Effect, you could move most of the imperative logic inside a JavaScript class:

Effects let you connect React to external systems. The more coordination between Effects is needed (for example, to chain multiple animations), the more it makes sense to extract that logic out of Effects and Hooks completely like in the sandbox above. Then, the code you extracted becomes the “external system”. This lets your Effects stay simple because they only need to send messages to the system you’ve moved outside React.

The examples above assume that the fade-in logic needs to be written in JavaScript. However, this particular fade-in animation is both simpler and much more efficient to implement with a plain CSS Animation:

Sometimes, you don’t even need a Hook!

This component uses a state variable and an Effect to display a number that increments every second. Extract this logic into a custom Hook called useCounter. Your goal is to make the Counter component implementation look exactly like this:

You’ll need to write your custom Hook in useCounter.js and import it into the App.js file.

**Examples:**

Example 1 (jsx):
```jsx
function StatusBar() {  const isOnline = useOnlineStatus();  return <h1>{isOnline ? '✅ Online' : '❌ Disconnected'}</h1>;}function SaveButton() {  const isOnline = useOnlineStatus();  function handleSaveClick() {    console.log('✅ Progress saved');  }  return (    <button disabled={!isOnline} onClick={handleSaveClick}>      {isOnline ? 'Save progress' : 'Reconnecting...'}    </button>  );}
```

Example 2 (jsx):
```jsx
function useOnlineStatus() {  const [isOnline, setIsOnline] = useState(true);  useEffect(() => {    function handleOnline() {      setIsOnline(true);    }    function handleOffline() {      setIsOnline(false);    }    window.addEventListener('online', handleOnline);    window.addEventListener('offline', handleOffline);    return () => {      window.removeEventListener('online', handleOnline);      window.removeEventListener('offline', handleOffline);    };  }, []);  return isOnline;}
```

Example 3 (unknown):
```unknown
// 🔴 Avoid: A Hook that doesn't use Hooksfunction useSorted(items) {  return items.slice().sort();}// ✅ Good: A regular function that doesn't use Hooksfunction getSorted(items) {  return items.slice().sort();}
```

Example 4 (swift):
```swift
function List({ items, shouldSort }) {  let displayedItems = items;  if (shouldSort) {    // ✅ It's ok to call getSorted() conditionally because it's not a Hook    displayedItems = getSorted(items);  }  // ...}
```

---

## Scaling Up with Reducer and Context

**URL:** https://react.dev/learn/scaling-up-with-reducer-and-context

**Contents:**
- Scaling Up with Reducer and Context
  - You will learn
- Combining a reducer with context
  - Step 1: Create the context
  - Step 2: Put state and dispatch into context
  - Step 3: Use context anywhere in the tree
- Moving all wiring into a single file
  - Note
- Recap

Reducers let you consolidate a component’s state update logic. Context lets you pass information deep down to other components. You can combine reducers and context together to manage state of a complex screen.

In this example from the introduction to reducers, the state is managed by a reducer. The reducer function contains all of the state update logic and is declared at the bottom of this file:

A reducer helps keep the event handlers short and concise. However, as your app grows, you might run into another difficulty. Currently, the tasks state and the dispatch function are only available in the top-level TaskApp component. To let other components read the list of tasks or change it, you have to explicitly pass down the current state and the event handlers that change it as props.

For example, TaskApp passes a list of tasks and the event handlers to TaskList:

And TaskList passes the event handlers to Task:

In a small example like this, this works well, but if you have tens or hundreds of components in the middle, passing down all state and functions can be quite frustrating!

This is why, as an alternative to passing them through props, you might want to put both the tasks state and the dispatch function into context. This way, any component below TaskApp in the tree can read the tasks and dispatch actions without the repetitive “prop drilling”.

Here is how you can combine a reducer with context:

The useReducer Hook returns the current tasks and the dispatch function that lets you update them:

To pass them down the tree, you will create two separate contexts:

Export them from a separate file so that you can later import them from other files:

Here, you’re passing null as the default value to both contexts. The actual values will be provided by the TaskApp component.

Now you can import both contexts in your TaskApp component. Take the tasks and dispatch returned by useReducer() and provide them to the entire tree below:

For now, you pass the information both via props and in context:

In the next step, you will remove prop passing.

Now you don’t need to pass the list of tasks or the event handlers down the tree:

Instead, any component that needs the task list can read it from the TasksContext:

To update the task list, any component can read the dispatch function from context and call it:

The TaskApp component does not pass any event handlers down, and the TaskList does not pass any event handlers to the Task component either. Each component reads the context that it needs:

The state still “lives” in the top-level TaskApp component, managed with useReducer. But its tasks and dispatch are now available to every component below in the tree by importing and using these contexts.

You don’t have to do this, but you could further declutter the components by moving both reducer and context into a single file. Currently, TasksContext.js contains only two context declarations:

This file is about to get crowded! You’ll move the reducer into that same file. Then you’ll declare a new TasksProvider component in the same file. This component will tie all the pieces together:

This removes all the complexity and wiring from your TaskApp component:

You can also export functions that use the context from TasksContext.js:

When a component needs to read context, it can do it through these functions:

This doesn’t change the behavior in any way, but it lets you later split these contexts further or add some logic to these functions. Now all of the context and reducer wiring is in TasksContext.js. This keeps the components clean and uncluttered, focused on what they display rather than where they get the data:

You can think of TasksProvider as a part of the screen that knows how to deal with tasks, useTasks as a way to read them, and useTasksDispatch as a way to update them from any component below in the tree.

Functions like useTasks and useTasksDispatch are called Custom Hooks. Your function is considered a custom Hook if its name starts with use. This lets you use other Hooks, like useContext, inside it.

As your app grows, you may have many context-reducer pairs like this. This is a powerful way to scale your app and lift state up without too much work whenever you want to access the data deep in the tree.

**Examples:**

Example 1 (jsx):
```jsx
<TaskList  tasks={tasks}  onChangeTask={handleChangeTask}  onDeleteTask={handleDeleteTask}/>
```

Example 2 (jsx):
```jsx
<Task  task={task}  onChange={onChangeTask}  onDelete={onDeleteTask}/>
```

Example 3 (unknown):
```unknown
const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
```

Example 4 (javascript):
```javascript
import { TasksContext, TasksDispatchContext } from './TasksContext.js';export default function TaskApp() {  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);  // ...  return (    <TasksContext value={tasks}>      <TasksDispatchContext value={dispatch}>        ...      </TasksDispatchContext>    </TasksContext>  );}
```

---

## Separating Events from Effects

**URL:** https://react.dev/learn/separating-events-from-effects

**Contents:**
- Separating Events from Effects
  - You will learn
- Choosing between event handlers and Effects
  - Event handlers run in response to specific interactions
  - Effects run whenever synchronization is needed
- Reactive values and reactive logic
  - Logic inside event handlers is not reactive
  - Logic inside Effects is reactive
- Extracting non-reactive logic out of Effects
  - Declaring an Effect Event

Event handlers only re-run when you perform the same interaction again. Unlike event handlers, Effects re-synchronize if some value they read, like a prop or a state variable, is different from what it was during the last render. Sometimes, you also want a mix of both behaviors: an Effect that re-runs in response to some values but not others. This page will teach you how to do that.

First, let’s recap the difference between event handlers and Effects.

Imagine you’re implementing a chat room component. Your requirements look like this:

Let’s say you’ve already implemented the code for them, but you’re not sure where to put it. Should you use event handlers or Effects? Every time you need to answer this question, consider why the code needs to run.

From the user’s perspective, sending a message should happen because the particular “Send” button was clicked. The user will get rather upset if you send their message at any other time or for any other reason. This is why sending a message should be an event handler. Event handlers let you handle specific interactions:

With an event handler, you can be sure that sendMessage(message) will only run if the user presses the button.

Recall that you also need to keep the component connected to the chat room. Where does that code go?

The reason to run this code is not some particular interaction. It doesn’t matter why or how the user navigated to the chat room screen. Now that they’re looking at it and could interact with it, the component needs to stay connected to the selected chat server. Even if the chat room component was the initial screen of your app, and the user has not performed any interactions at all, you would still need to connect. This is why it’s an Effect:

With this code, you can be sure that there is always an active connection to the currently selected chat server, regardless of the specific interactions performed by the user. Whether the user has only opened your app, selected a different room, or navigated to another screen and back, your Effect ensures that the component will remain synchronized with the currently selected room, and will re-connect whenever it’s necessary.

Intuitively, you could say that event handlers are always triggered “manually”, for example by clicking a button. Effects, on the other hand, are “automatic”: they run and re-run as often as it’s needed to stay synchronized.

There is a more precise way to think about this.

Props, state, and variables declared inside your component’s body are called reactive values. In this example, serverUrl is not a reactive value, but roomId and message are. They participate in the rendering data flow:

Reactive values like these can change due to a re-render. For example, the user may edit the message or choose a different roomId in a dropdown. Event handlers and Effects respond to changes differently:

Let’s revisit the previous example to illustrate this difference.

Take a look at this line of code. Should this logic be reactive or not?

From the user’s perspective, a change to the message does not mean that they want to send a message. It only means that the user is typing. In other words, the logic that sends a message should not be reactive. It should not run again only because the reactive value has changed. That’s why it belongs in the event handler:

Event handlers aren’t reactive, so sendMessage(message) will only run when the user clicks the Send button.

Now let’s return to these lines:

From the user’s perspective, a change to the roomId does mean that they want to connect to a different room. In other words, the logic for connecting to the room should be reactive. You want these lines of code to “keep up” with the reactive value, and to run again if that value is different. That’s why it belongs in an Effect:

Effects are reactive, so createConnection(serverUrl, roomId) and connection.connect() will run for every distinct value of roomId. Your Effect keeps the chat connection synchronized to the currently selected room.

Things get more tricky when you want to mix reactive logic with non-reactive logic.

For example, imagine that you want to show a notification when the user connects to the chat. You read the current theme (dark or light) from the props so that you can show the notification in the correct color:

However, theme is a reactive value (it can change as a result of re-rendering), and every reactive value read by an Effect must be declared as its dependency. Now you have to specify theme as a dependency of your Effect:

Play with this example and see if you can spot the problem with this user experience:

When the roomId changes, the chat re-connects as you would expect. But since theme is also a dependency, the chat also re-connects every time you switch between the dark and the light theme. That’s not great!

In other words, you don’t want this line to be reactive, even though it is inside an Effect (which is reactive):

You need a way to separate this non-reactive logic from the reactive Effect around it.

Use a special Hook called useEffectEvent to extract this non-reactive logic out of your Effect:

Here, onConnected is called an Effect Event. It’s a part of your Effect logic, but it behaves a lot more like an event handler. The logic inside it is not reactive, and it always “sees” the latest values of your props and state.

Now you can call the onConnected Effect Event from inside your Effect:

This solves the problem. Note that you had to remove theme from the list of your Effect’s dependencies, because it’s no longer used in the Effect. You also don’t need to add onConnected to it, because Effect Events are not reactive and must be omitted from dependencies.

Verify that the new behavior works as you would expect:

You can think of Effect Events as being very similar to event handlers. The main difference is that event handlers run in response to a user interactions, whereas Effect Events are triggered by you from Effects. Effect Events let you “break the chain” between the reactivity of Effects and code that should not be reactive.

Effect Events let you fix many patterns where you might be tempted to suppress the dependency linter.

For example, say you have an Effect to log the page visits:

Later, you add multiple routes to your site. Now your Page component receives a url prop with the current path. You want to pass the url as a part of your logVisit call, but the dependency linter complains:

Think about what you want the code to do. You want to log a separate visit for different URLs since each URL represents a different page. In other words, this logVisit call should be reactive with respect to the url. This is why, in this case, it makes sense to follow the dependency linter, and add url as a dependency:

Now let’s say you want to include the number of items in the shopping cart together with every page visit:

You used numberOfItems inside the Effect, so the linter asks you to add it as a dependency. However, you don’t want the logVisit call to be reactive with respect to numberOfItems. If the user puts something into the shopping cart, and the numberOfItems changes, this does not mean that the user visited the page again. In other words, visiting the page is, in some sense, an “event”. It happens at a precise moment in time.

Split the code in two parts:

Here, onVisit is an Effect Event. The code inside it isn’t reactive. This is why you can use numberOfItems (or any other reactive value!) without worrying that it will cause the surrounding code to re-execute on changes.

On the other hand, the Effect itself remains reactive. Code inside the Effect uses the url prop, so the Effect will re-run after every re-render with a different url. This, in turn, will call the onVisit Effect Event.

As a result, you will call logVisit for every change to the url, and always read the latest numberOfItems. However, if numberOfItems changes on its own, this will not cause any of the code to re-run.

You might be wondering if you could call onVisit() with no arguments, and read the url inside it:

This would work, but it’s better to pass this url to the Effect Event explicitly. By passing url as an argument to your Effect Event, you are saying that visiting a page with a different url constitutes a separate “event” from the user’s perspective. The visitedUrl is a part of the “event” that happened:

Since your Effect Event explicitly “asks” for the visitedUrl, now you can’t accidentally remove url from the Effect’s dependencies. If you remove the url dependency (causing distinct page visits to be counted as one), the linter will warn you about it. You want onVisit to be reactive with regards to the url, so instead of reading the url inside (where it wouldn’t be reactive), you pass it from your Effect.

This becomes especially important if there is some asynchronous logic inside the Effect:

Here, url inside onVisit corresponds to the latest url (which could have already changed), but visitedUrl corresponds to the url that originally caused this Effect (and this onVisit call) to run.

In the existing codebases, you may sometimes see the lint rule suppressed like this:

We recommend never suppressing the linter.

The first downside of suppressing the rule is that React will no longer warn you when your Effect needs to “react” to a new reactive dependency you’ve introduced to your code. In the earlier example, you added url to the dependencies because React reminded you to do it. You will no longer get such reminders for any future edits to that Effect if you disable the linter. This leads to bugs.

Here is an example of a confusing bug caused by suppressing the linter. In this example, the handleMove function is supposed to read the current canMove state variable value in order to decide whether the dot should follow the cursor. However, canMove is always true inside handleMove.

The problem with this code is in suppressing the dependency linter. If you remove the suppression, you’ll see that this Effect should depend on the handleMove function. This makes sense: handleMove is declared inside the component body, which makes it a reactive value. Every reactive value must be specified as a dependency, or it can potentially get stale over time!

The author of the original code has “lied” to React by saying that the Effect does not depend ([]) on any reactive values. This is why React did not re-synchronize the Effect after canMove has changed (and handleMove with it). Because React did not re-synchronize the Effect, the handleMove attached as a listener is the handleMove function created during the initial render. During the initial render, canMove was true, which is why handleMove from the initial render will forever see that value.

If you never suppress the linter, you will never see problems with stale values.

With useEffectEvent, there is no need to “lie” to the linter, and the code works as you would expect:

This doesn’t mean that useEffectEvent is always the correct solution. You should only apply it to the lines of code that you don’t want to be reactive. In the above sandbox, you didn’t want the Effect’s code to be reactive with regards to canMove. That’s why it made sense to extract an Effect Event.

Read Removing Effect Dependencies for other correct alternatives to suppressing the linter.

Effect Events are very limited in how you can use them:

For example, don’t declare and pass an Effect Event like this:

Instead, always declare Effect Events directly next to the Effects that use them:

Effect Events are non-reactive “pieces” of your Effect code. They should be next to the Effect using them.

This Timer component keeps a count state variable which increases every second. The value by which it’s increasing is stored in the increment state variable. You can control the increment variable with the plus and minus buttons.

However, no matter how many times you click the plus button, the counter is still incremented by one every second. What’s wrong with this code? Why is increment always equal to 1 inside the Effect’s code? Find the mistake and fix it.

**Examples:**

Example 1 (jsx):
```jsx
function ChatRoom({ roomId }) {  const [message, setMessage] = useState('');  // ...  function handleSendClick() {    sendMessage(message);  }  // ...  return (    <>      <input value={message} onChange={e => setMessage(e.target.value)} />      <button onClick={handleSendClick}>Send</button>    </>  );}
```

Example 2 (javascript):
```javascript
function ChatRoom({ roomId }) {  // ...  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => {      connection.disconnect();    };  }, [roomId]);  // ...}
```

Example 3 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId }) {  const [message, setMessage] = useState('');  // ...}
```

Example 4 (unknown):
```unknown
// ...    sendMessage(message);    // ...
```

---

## Setup

**URL:** https://react.dev/learn/setup

**Contents:**
- Setup
- Editor Setup
- Using TypeScript
- React Developer Tools
- React Compiler
- Next steps

React integrates with tools like editors, TypeScript, browser extensions, and compilers. This section will help you get your environment set up.

See our recommended editors and learn how to set them up to work with React.

TypeScript is a popular way to add type definitions to JavaScript codebases. Learn how to integrate TypeScript into your React projects.

React Developer Tools is a browser extension that can inspect React components, edit props and state, and identify performance problems. Learn how to install it here.

React Compiler is a tool that automatically optimizes your React app. Learn more.

Head to the Quick Start guide for a tour of the most important React concepts you will encounter every day.

---

## Sharing State Between Components

**URL:** https://react.dev/learn/sharing-state-between-components

**Contents:**
- Sharing State Between Components
  - You will learn
- Lifting state up by example
  - Step 1: Remove state from the child components
  - Step 2: Pass hardcoded data from the common parent
  - Step 3: Add state to the common parent
      - Deep Dive
    - Controlled and uncontrolled components
- A single source of truth for each state
- Recap

Sometimes, you want the state of two components to always change together. To do it, remove state from both of them, move it to their closest common parent, and then pass it down to them via props. This is known as lifting state up, and it’s one of the most common things you will do writing React code.

In this example, a parent Accordion component renders two separate Panels:

Each Panel component has a boolean isActive state that determines whether its content is visible.

Press the Show button for both panels:

Notice how pressing one panel’s button does not affect the other panel—they are independent.

Initially, each Panel’s isActive state is false, so they both appear collapsed

Clicking either Panel’s button will only update that Panel’s isActive state alone

But now let’s say you want to change it so that only one panel is expanded at any given time. With that design, expanding the second panel should collapse the first one. How would you do that?

To coordinate these two panels, you need to “lift their state up” to a parent component in three steps:

This will allow the Accordion component to coordinate both Panels and only expand one at a time.

You will give control of the Panel’s isActive to its parent component. This means that the parent component will pass isActive to Panel as a prop instead. Start by removing this line from the Panel component:

And instead, add isActive to the Panel’s list of props:

Now the Panel’s parent component can control isActive by passing it down as a prop. Conversely, the Panel component now has no control over the value of isActive—it’s now up to the parent component!

To lift state up, you must locate the closest common parent component of both of the child components that you want to coordinate:

In this example, it’s the Accordion component. Since it’s above both panels and can control their props, it will become the “source of truth” for which panel is currently active. Make the Accordion component pass a hardcoded value of isActive (for example, true) to both panels:

Try editing the hardcoded isActive values in the Accordion component and see the result on the screen.

Lifting state up often changes the nature of what you’re storing as state.

In this case, only one panel should be active at a time. This means that the Accordion common parent component needs to keep track of which panel is the active one. Instead of a boolean value, it could use a number as the index of the active Panel for the state variable:

When the activeIndex is 0, the first panel is active, and when it’s 1, it’s the second one.

Clicking the “Show” button in either Panel needs to change the active index in Accordion. A Panel can’t set the activeIndex state directly because it’s defined inside the Accordion. The Accordion component needs to explicitly allow the Panel component to change its state by passing an event handler down as a prop:

The <button> inside the Panel will now use the onShow prop as its click event handler:

This completes lifting state up! Moving state into the common parent component allowed you to coordinate the two panels. Using the active index instead of two “is shown” flags ensured that only one panel is active at a given time. And passing down the event handler to the child allowed the child to change the parent’s state.

Initially, Accordion’s activeIndex is 0, so the first Panel receives isActive = true

When Accordion’s activeIndex state changes to 1, the second Panel receives isActive = true instead

It is common to call a component with some local state “uncontrolled”. For example, the original Panel component with an isActive state variable is uncontrolled because its parent cannot influence whether the panel is active or not.

In contrast, you might say a component is “controlled” when the important information in it is driven by props rather than its own local state. This lets the parent component fully specify its behavior. The final Panel component with the isActive prop is controlled by the Accordion component.

Uncontrolled components are easier to use within their parents because they require less configuration. But they’re less flexible when you want to coordinate them together. Controlled components are maximally flexible, but they require the parent components to fully configure them with props.

In practice, “controlled” and “uncontrolled” aren’t strict technical terms—each component usually has some mix of both local state and props. However, this is a useful way to talk about how components are designed and what capabilities they offer.

When writing a component, consider which information in it should be controlled (via props), and which information should be uncontrolled (via state). But you can always change your mind and refactor later.

In a React application, many components will have their own state. Some state may “live” close to the leaf components (components at the bottom of the tree) like inputs. Other state may “live” closer to the top of the app. For example, even client-side routing libraries are usually implemented by storing the current route in the React state, and passing it down by props!

For each unique piece of state, you will choose the component that “owns” it. This principle is also known as having a “single source of truth”. It doesn’t mean that all state lives in one place—but that for each piece of state, there is a specific component that holds that piece of information. Instead of duplicating shared state between components, lift it up to their common shared parent, and pass it down to the children that need it.

Your app will change as you work on it. It is common that you will move state down or back up while you’re still figuring out where each piece of the state “lives”. This is all part of the process!

To see what this feels like in practice with a few more components, read Thinking in React.

These two inputs are independent. Make them stay in sync: editing one input should update the other input with the same text, and vice versa.

**Examples:**

Example 1 (jsx):
```jsx
const [isActive, setIsActive] = useState(false);
```

Example 2 (javascript):
```javascript
function Panel({ title, children, isActive }) {
```

Example 3 (jsx):
```jsx
const [activeIndex, setActiveIndex] = useState(0);
```

Example 4 (jsx):
```jsx
<>  <Panel    isActive={activeIndex === 0}    onShow={() => setActiveIndex(0)}  >    ...  </Panel>  <Panel    isActive={activeIndex === 1}    onShow={() => setActiveIndex(1)}  >    ...  </Panel></>
```

---

## State as a Snapshot

**URL:** https://react.dev/learn/state-as-a-snapshot

**Contents:**
- State as a Snapshot
  - You will learn
- Setting state triggers renders
- Rendering takes a snapshot in time
- State over time
- Recap
- Try out some challenges
    - Challenge 1 of 1: Implement a traffic light

State variables might look like regular JavaScript variables that you can read and write to. However, state behaves more like a snapshot. Setting it does not change the state variable you already have, but instead triggers a re-render.

You might think of your user interface as changing directly in response to the user event like a click. In React, it works a little differently from this mental model. On the previous page, you saw that setting state requests a re-render from React. This means that for an interface to react to the event, you need to update the state.

In this example, when you press “send”, setIsSent(true) tells React to re-render the UI:

Here’s what happens when you click the button:

Let’s take a closer look at the relationship between state and rendering.

“Rendering” means that React is calling your component, which is a function. The JSX you return from that function is like a snapshot of the UI in time. Its props, event handlers, and local variables were all calculated using its state at the time of the render.

Unlike a photograph or a movie frame, the UI “snapshot” you return is interactive. It includes logic like event handlers that specify what happens in response to inputs. React updates the screen to match this snapshot and connects the event handlers. As a result, pressing a button will trigger the click handler from your JSX.

When React re-renders a component:

Illustrated by Rachel Lee Nabors

As a component’s memory, state is not like a regular variable that disappears after your function returns. State actually “lives” in React itself—as if on a shelf!—outside of your function. When React calls your component, it gives you a snapshot of the state for that particular render. Your component returns a snapshot of the UI with a fresh set of props and event handlers in its JSX, all calculated using the state values from that render!

Illustrated by Rachel Lee Nabors

Here’s a little experiment to show you how this works. In this example, you might expect that clicking the “+3” button would increment the counter three times because it calls setNumber(number + 1) three times.

See what happens when you click the “+3” button:

Notice that number only increments once per click!

Setting state only changes it for the next render. During the first render, number was 0. This is why, in that render’s onClick handler, the value of number is still 0 even after setNumber(number + 1) was called:

Here is what this button’s click handler tells React to do:

Even though you called setNumber(number + 1) three times, in this render’s event handler number is always 0, so you set the state to 1 three times. This is why, after your event handler finishes, React re-renders the component with number equal to 1 rather than 3.

You can also visualize this by mentally substituting state variables with their values in your code. Since the number state variable is 0 for this render, its event handler looks like this:

For the next render, number is 1, so that render’s click handler looks like this:

This is why clicking the button again will set the counter to 2, then to 3 on the next click, and so on.

Well, that was fun. Try to guess what clicking this button will alert:

If you use the substitution method from before, you can guess that the alert shows “0”:

But what if you put a timer on the alert, so it only fires after the component re-rendered? Would it say “0” or “5”? Have a guess!

Surprised? If you use the substitution method, you can see the “snapshot” of the state passed to the alert.

The state stored in React may have changed by the time the alert runs, but it was scheduled using a snapshot of the state at the time the user interacted with it!

A state variable’s value never changes within a render, even if its event handler’s code is asynchronous. Inside that render’s onClick, the value of number continues to be 0 even after setNumber(number + 5) was called. Its value was “fixed” when React “took the snapshot” of the UI by calling your component.

Here is an example of how that makes your event handlers less prone to timing mistakes. Below is a form that sends a message with a five-second delay. Imagine this scenario:

What do you expect the alert to display? Would it display, “You said Hello to Alice”? Or would it display, “You said Hello to Bob”? Make a guess based on what you know, and then try it:

React keeps the state values “fixed” within one render’s event handlers. You don’t need to worry whether the state has changed while the code is running.

But what if you wanted to read the latest state before a re-render? You’ll want to use a state updater function, covered on the next page!

Here is a crosswalk light component that toggles when the button is pressed:

Add an alert to the click handler. When the light is green and says “Walk”, clicking the button should say “Stop is next”. When the light is red and says “Stop”, clicking the button should say “Walk is next”.

Does it make a difference whether you put the alert before or after the setWalk call?

**Examples:**

Example 1 (jsx):
```jsx
<button onClick={() => {  setNumber(number + 1);  setNumber(number + 1);  setNumber(number + 1);}}>+3</button>
```

Example 2 (jsx):
```jsx
<button onClick={() => {  setNumber(0 + 1);  setNumber(0 + 1);  setNumber(0 + 1);}}>+3</button>
```

Example 3 (jsx):
```jsx
<button onClick={() => {  setNumber(1 + 1);  setNumber(1 + 1);  setNumber(1 + 1);}}>+3</button>
```

Example 4 (unknown):
```unknown
setNumber(0 + 5);alert(0);
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory

**Contents:**
- State: A Component's Memory
  - You will learn
- When a regular variable isn’t enough
- Adding a state variable
  - Meet your first Hook
  - Pitfall
  - Anatomy of useState
  - Note
- Giving a component multiple state variables
      - Deep Dive

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” should put a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

Here’s a component that renders a sculpture image. Clicking the “Next” button should show the next sculpture by changing the index to 1, then 2, and so on. However, this won’t work (you can try it!):

The handleClick event handler is updating a local variable, index. But two things prevent that change from being visible:

To update a component with new data, two things need to happen:

The useState Hook provides those two things:

To add a state variable, import useState from React at the top of the file:

Then, replace this line:

index is a state variable and setIndex is the setter function.

The [ and ] syntax here is called array destructuring and it lets you read values from an array. The array returned by useState always has exactly two items.

This is how they work together in handleClick:

Now clicking the “Next” button switches the current sculpture:

In React, useState, as well as any other function starting with “use”, is called a Hook.

Hooks are special functions that are only available while React is rendering (which we’ll get into in more detail on the next page). They let you “hook into” different React features.

State is just one of those features, but you will meet the other Hooks later.

Hooks—functions starting with use—can only be called at the top level of your components or your own Hooks. You can’t call Hooks inside conditions, loops, or other nested functions. Hooks are functions, but it’s helpful to think of them as unconditional declarations about your component’s needs. You “use” React features at the top of your component similar to how you “import” modules at the top of your file.

When you call useState, you are telling React that you want this component to remember something:

In this case, you want React to remember index.

The convention is to name this pair like const [something, setSomething]. You could name it anything you like, but conventions make things easier to understand across projects.

The only argument to useState is the initial value of your state variable. In this example, the index’s initial value is set to 0 with useState(0).

Every time your component renders, useState gives you an array containing two values:

Here’s how that happens in action:

You can have as many state variables of as many types as you like in one component. This component has two state variables, a number index and a boolean showMore that’s toggled when you click “Show details”:

It is a good idea to have multiple state variables if their state is unrelated, like index and showMore in this example. But if you find that you often change two state variables together, it might be easier to combine them into one. For example, if you have a form with many fields, it’s more convenient to have a single state variable that holds an object than state variable per field. Read Choosing the State Structure for more tips.

You might have noticed that the useState call does not receive any information about which state variable it refers to. There is no “identifier” that is passed to useState, so how does it know which of the state variables to return? Does it rely on some magic like parsing your functions? The answer is no.

Instead, to enable their concise syntax, Hooks rely on a stable call order on every render of the same component. This works well in practice because if you follow the rule above (“only call Hooks at the top level”), Hooks will always be called in the same order. Additionally, a linter plugin catches most mistakes.

Internally, React holds an array of state pairs for every component. It also maintains the current pair index, which is set to 0 before rendering. Each time you call useState, React gives you the next state pair and increments the index. You can read more about this mechanism in React Hooks: Not Magic, Just Arrays.

This example doesn’t use React but it gives you an idea of how useState works internally:

You don’t have to understand it to use React, but you might find this a helpful mental model.

State is local to a component instance on the screen. In other words, if you render the same component twice, each copy will have completely isolated state! Changing one of them will not affect the other.

In this example, the Gallery component from earlier is rendered twice with no changes to its logic. Try clicking the buttons inside each of the galleries. Notice that their state is independent:

This is what makes state different from regular variables that you might declare at the top of your module. State is not tied to a particular function call or a place in the code, but it’s “local” to the specific place on the screen. You rendered two <Gallery /> components, so their state is stored separately.

Also notice how the Page component doesn’t “know” anything about the Gallery state or even whether it has any. Unlike props, state is fully private to the component declaring it. The parent component can’t change it. This lets you add state to any component or remove it without impacting the rest of the components.

What if you wanted both galleries to keep their states in sync? The right way to do it in React is to remove state from child components and add it to their closest shared parent. The next few pages will focus on organizing state of a single component, but we will return to this topic in Sharing State Between Components.

When you press “Next” on the last sculpture, the code crashes. Fix the logic to prevent the crash. You may do this by adding extra logic to event handler or by disabling the button when the action is not possible.

After fixing the crash, add a “Previous” button that shows the previous sculpture. It shouldn’t crash on the first sculpture.

**Examples:**

Example 1 (sql):
```sql
import { useState } from 'react';
```

Example 2 (javascript):
```javascript
let index = 0;
```

Example 3 (jsx):
```jsx
const [index, setIndex] = useState(0);
```

Example 4 (javascript):
```javascript
function handleClick() {  setIndex(index + 1);}
```

---

## Synchronizing with Effects

**URL:** https://react.dev/learn/synchronizing-with-effects

**Contents:**
- Synchronizing with Effects
  - You will learn
- What are Effects and how are they different from events?
  - Note
- You might not need an Effect
- How to write an Effect
  - Step 1: Declare an Effect
  - Pitfall
  - Step 2: Specify the Effect dependencies
  - Pitfall

Some components need to synchronize with external systems. For example, you might want to control a non-React component based on the React state, set up a server connection, or send an analytics log when a component appears on the screen. Effects let you run some code after rendering so that you can synchronize your component with some system outside of React.

Before getting to Effects, you need to be familiar with two types of logic inside React components:

Rendering code (introduced in Describing the UI) lives at the top level of your component. This is where you take the props and state, transform them, and return the JSX you want to see on the screen. Rendering code must be pure. Like a math formula, it should only calculate the result, but not do anything else.

Event handlers (introduced in Adding Interactivity) are nested functions inside your components that do things rather than just calculate them. An event handler might update an input field, submit an HTTP POST request to buy a product, or navigate the user to another screen. Event handlers contain “side effects” (they change the program’s state) caused by a specific user action (for example, a button click or typing).

Sometimes this isn’t enough. Consider a ChatRoom component that must connect to the chat server whenever it’s visible on the screen. Connecting to a server is not a pure calculation (it’s a side effect) so it can’t happen during rendering. However, there is no single particular event like a click that causes ChatRoom to be displayed.

Effects let you specify side effects that are caused by rendering itself, rather than by a particular event. Sending a message in the chat is an event because it is directly caused by the user clicking a specific button. However, setting up a server connection is an Effect because it should happen no matter which interaction caused the component to appear. Effects run at the end of a commit after the screen updates. This is a good time to synchronize the React components with some external system (like network or a third-party library).

Here and later in this text, capitalized “Effect” refers to the React-specific definition above, i.e. a side effect caused by rendering. To refer to the broader programming concept, we’ll say “side effect”.

Don’t rush to add Effects to your components. Keep in mind that Effects are typically used to “step out” of your React code and synchronize with some external system. This includes browser APIs, third-party widgets, network, and so on. If your Effect only adjusts some state based on other state, you might not need an Effect.

To write an Effect, follow these three steps:

Let’s look at each of these steps in detail.

To declare an Effect in your component, import the useEffect Hook from React:

Then, call it at the top level of your component and put some code inside your Effect:

Every time your component renders, React will update the screen and then run the code inside useEffect. In other words, useEffect “delays” a piece of code from running until that render is reflected on the screen.

Let’s see how you can use an Effect to synchronize with an external system. Consider a <VideoPlayer> React component. It would be nice to control whether it’s playing or paused by passing an isPlaying prop to it:

Your custom VideoPlayer component renders the built-in browser <video> tag:

However, the browser <video> tag does not have an isPlaying prop. The only way to control it is to manually call the play() and pause() methods on the DOM element. You need to synchronize the value of isPlaying prop, which tells whether the video should currently be playing, with calls like play() and pause().

We’ll need to first get a ref to the <video> DOM node.

You might be tempted to try to call play() or pause() during rendering, but that isn’t correct:

The reason this code isn’t correct is that it tries to do something with the DOM node during rendering. In React, rendering should be a pure calculation of JSX and should not contain side effects like modifying the DOM.

Moreover, when VideoPlayer is called for the first time, its DOM does not exist yet! There isn’t a DOM node yet to call play() or pause() on, because React doesn’t know what DOM to create until you return the JSX.

The solution here is to wrap the side effect with useEffect to move it out of the rendering calculation:

By wrapping the DOM update in an Effect, you let React update the screen first. Then your Effect runs.

When your VideoPlayer component renders (either the first time or if it re-renders), a few things will happen. First, React will update the screen, ensuring the <video> tag is in the DOM with the right props. Then React will run your Effect. Finally, your Effect will call play() or pause() depending on the value of isPlaying.

Press Play/Pause multiple times and see how the video player stays synchronized to the isPlaying value:

In this example, the “external system” you synchronized to React state was the browser media API. You can use a similar approach to wrap legacy non-React code (like jQuery plugins) into declarative React components.

Note that controlling a video player is much more complex in practice. Calling play() may fail, the user might play or pause using the built-in browser controls, and so on. This example is very simplified and incomplete.

By default, Effects run after every render. This is why code like this will produce an infinite loop:

Effects run as a result of rendering. Setting state triggers rendering. Setting state immediately in an Effect is like plugging a power outlet into itself. The Effect runs, it sets the state, which causes a re-render, which causes the Effect to run, it sets the state again, this causes another re-render, and so on.

Effects should usually synchronize your components with an external system. If there’s no external system and you only want to adjust some state based on other state, you might not need an Effect.

By default, Effects run after every render. Often, this is not what you want:

To demonstrate the issue, here is the previous example with a few console.log calls and a text input that updates the parent component’s state. Notice how typing causes the Effect to re-run:

You can tell React to skip unnecessarily re-running the Effect by specifying an array of dependencies as the second argument to the useEffect call. Start by adding an empty [] array to the above example on line 14:

You should see an error saying React Hook useEffect has a missing dependency: 'isPlaying':

The problem is that the code inside of your Effect depends on the isPlaying prop to decide what to do, but this dependency was not explicitly declared. To fix this issue, add isPlaying to the dependency array:

Now all dependencies are declared, so there is no error. Specifying [isPlaying] as the dependency array tells React that it should skip re-running your Effect if isPlaying is the same as it was during the previous render. With this change, typing into the input doesn’t cause the Effect to re-run, but pressing Play/Pause does:

The dependency array can contain multiple dependencies. React will only skip re-running the Effect if all of the dependencies you specify have exactly the same values as they had during the previous render. React compares the dependency values using the Object.is comparison. See the useEffect reference for details.

Notice that you can’t “choose” your dependencies. You will get a lint error if the dependencies you specified don’t match what React expects based on the code inside your Effect. This helps catch many bugs in your code. If you don’t want some code to re-run, edit the Effect code itself to not “need” that dependency.

The behaviors without the dependency array and with an empty [] dependency array are different:

We’ll take a close look at what “mount” means in the next step.

This Effect uses both ref and isPlaying, but only isPlaying is declared as a dependency:

This is because the ref object has a stable identity: React guarantees you’ll always get the same object from the same useRef call on every render. It never changes, so it will never by itself cause the Effect to re-run. Therefore, it does not matter whether you include it or not. Including it is fine too:

The set functions returned by useState also have stable identity, so you will often see them omitted from the dependencies too. If the linter lets you omit a dependency without errors, it is safe to do.

Omitting always-stable dependencies only works when the linter can “see” that the object is stable. For example, if ref was passed from a parent component, you would have to specify it in the dependency array. However, this is good because you can’t know whether the parent component always passes the same ref, or passes one of several refs conditionally. So your Effect would depend on which ref is passed.

Consider a different example. You’re writing a ChatRoom component that needs to connect to the chat server when it appears. You are given a createConnection() API that returns an object with connect() and disconnect() methods. How do you keep the component connected while it is displayed to the user?

Start by writing the Effect logic:

It would be slow to connect to the chat after every re-render, so you add the dependency array:

The code inside the Effect does not use any props or state, so your dependency array is [] (empty). This tells React to only run this code when the component “mounts”, i.e. appears on the screen for the first time.

Let’s try running this code:

This Effect only runs on mount, so you might expect "✅ Connecting..." to be printed once in the console. However, if you check the console, "✅ Connecting..." gets printed twice. Why does it happen?

Imagine the ChatRoom component is a part of a larger app with many different screens. The user starts their journey on the ChatRoom page. The component mounts and calls connection.connect(). Then imagine the user navigates to another screen—for example, to the Settings page. The ChatRoom component unmounts. Finally, the user clicks Back and ChatRoom mounts again. This would set up a second connection—but the first connection was never destroyed! As the user navigates across the app, the connections would keep piling up.

Bugs like this are easy to miss without extensive manual testing. To help you spot them quickly, in development React remounts every component once immediately after its initial mount.

Seeing the "✅ Connecting..." log twice helps you notice the real issue: your code doesn’t close the connection when the component unmounts.

To fix the issue, return a cleanup function from your Effect:

React will call your cleanup function each time before the Effect runs again, and one final time when the component unmounts (gets removed). Let’s see what happens when the cleanup function is implemented:

Now you get three console logs in development:

This is the correct behavior in development. By remounting your component, React verifies that navigating away and back would not break your code. Disconnecting and then connecting again is exactly what should happen! When you implement the cleanup well, there should be no user-visible difference between running the Effect once vs running it, cleaning it up, and running it again. There’s an extra connect/disconnect call pair because React is probing your code for bugs in development. This is normal—don’t try to make it go away!

In production, you would only see "✅ Connecting..." printed once. Remounting components only happens in development to help you find Effects that need cleanup. You can turn off Strict Mode to opt out of the development behavior, but we recommend keeping it on. This lets you find many bugs like the one above.

React intentionally remounts your components in development to find bugs like in the last example. The right question isn’t “how to run an Effect once”, but “how to fix my Effect so that it works after remounting”.

Usually, the answer is to implement the cleanup function. The cleanup function should stop or undo whatever the Effect was doing. The rule of thumb is that the user shouldn’t be able to distinguish between the Effect running once (as in production) and a setup → cleanup → setup sequence (as you’d see in development).

Most of the Effects you’ll write will fit into one of the common patterns below.

A common pitfall for preventing Effects firing twice in development is to use a ref to prevent the Effect from running more than once. For example, you could “fix” the above bug with a useRef:

This makes it so you only see "✅ Connecting..." once in development, but it doesn’t fix the bug.

When the user navigates away, the connection still isn’t closed and when they navigate back, a new connection is created. As the user navigates across the app, the connections would keep piling up, the same as it would before the “fix”.

To fix the bug, it is not enough to just make the Effect run once. The effect needs to work after re-mounting, which means the connection needs to be cleaned up like in the solution above.

See the examples below for how to handle common patterns.

Sometimes you need to add UI widgets that aren’t written in React. For example, let’s say you’re adding a map component to your page. It has a setZoomLevel() method, and you’d like to keep the zoom level in sync with a zoomLevel state variable in your React code. Your Effect would look similar to this:

Note that there is no cleanup needed in this case. In development, React will call the Effect twice, but this is not a problem because calling setZoomLevel twice with the same value does not do anything. It may be slightly slower, but this doesn’t matter because it won’t remount needlessly in production.

Some APIs may not allow you to call them twice in a row. For example, the showModal method of the built-in <dialog> element throws if you call it twice. Implement the cleanup function and make it close the dialog:

In development, your Effect will call showModal(), then immediately close(), and then showModal() again. This has the same user-visible behavior as calling showModal() once, as you would see in production.

If your Effect subscribes to something, the cleanup function should unsubscribe:

In development, your Effect will call addEventListener(), then immediately removeEventListener(), and then addEventListener() again with the same handler. So there would be only one active subscription at a time. This has the same user-visible behavior as calling addEventListener() once, as in production.

If your Effect animates something in, the cleanup function should reset the animation to the initial values:

In development, opacity will be set to 1, then to 0, and then to 1 again. This should have the same user-visible behavior as setting it to 1 directly, which is what would happen in production. If you use a third-party animation library with support for tweening, your cleanup function should reset the timeline to its initial state.

If your Effect fetches something, the cleanup function should either abort the fetch or ignore its result:

You can’t “undo” a network request that already happened, but your cleanup function should ensure that the fetch that’s not relevant anymore does not keep affecting your application. If the userId changes from 'Alice' to 'Bob', cleanup ensures that the 'Alice' response is ignored even if it arrives after 'Bob'.

In development, you will see two fetches in the Network tab. There is nothing wrong with that. With the approach above, the first Effect will immediately get cleaned up so its copy of the ignore variable will be set to true. So even though there is an extra request, it won’t affect the state thanks to the if (!ignore) check.

In production, there will only be one request. If the second request in development is bothering you, the best approach is to use a solution that deduplicates requests and caches their responses between components:

This will not only improve the development experience, but also make your application feel faster. For example, the user pressing the Back button won’t have to wait for some data to load again because it will be cached. You can either build such a cache yourself or use one of the many alternatives to manual fetching in Effects.

Writing fetch calls inside Effects is a popular way to fetch data, especially in fully client-side apps. This is, however, a very manual approach and it has significant downsides:

This list of downsides is not specific to React. It applies to fetching data on mount with any library. Like with routing, data fetching is not trivial to do well, so we recommend the following approaches:

You can continue fetching data directly in Effects if neither of these approaches suit you.

Consider this code that sends an analytics event on the page visit:

In development, logVisit will be called twice for every URL, so you might be tempted to try to fix that. We recommend keeping this code as is. Like with earlier examples, there is no user-visible behavior difference between running it once and running it twice. From a practical point of view, logVisit should not do anything in development because you don’t want the logs from the development machines to skew the production metrics. Your component remounts every time you save its file, so it logs extra visits in development anyway.

In production, there will be no duplicate visit logs.

To debug the analytics events you’re sending, you can deploy your app to a staging environment (which runs in production mode) or temporarily opt out of Strict Mode and its development-only remounting checks. You may also send analytics from the route change event handlers instead of Effects. For more precise analytics, intersection observers can help track which components are in the viewport and how long they remain visible.

Some logic should only run once when the application starts. You can put it outside your components:

This guarantees that such logic only runs once after the browser loads the page.

Sometimes, even if you write a cleanup function, there’s no way to prevent user-visible consequences of running the Effect twice. For example, maybe your Effect sends a POST request like buying a product:

You wouldn’t want to buy the product twice. However, this is also why you shouldn’t put this logic in an Effect. What if the user goes to another page and then presses Back? Your Effect would run again. You don’t want to buy the product when the user visits a page; you want to buy it when the user clicks the Buy button.

Buying is not caused by rendering; it’s caused by a specific interaction. It should run only when the user presses the button. Delete the Effect and move your /api/buy request into the Buy button event handler:

This illustrates that if remounting breaks the logic of your application, this usually uncovers existing bugs. From a user’s perspective, visiting a page shouldn’t be different from visiting it, clicking a link, then pressing Back to view the page again. React verifies that your components abide by this principle by remounting them once in development.

This playground can help you “get a feel” for how Effects work in practice.

This example uses setTimeout to schedule a console log with the input text to appear three seconds after the Effect runs. The cleanup function cancels the pending timeout. Start by pressing “Mount the component”:

You will see three logs at first: Schedule "a" log, Cancel "a" log, and Schedule "a" log again. Three second later there will also be a log saying a. As you learned earlier, the extra schedule/cancel pair is because React remounts the component once in development to verify that you’ve implemented cleanup well.

Now edit the input to say abc. If you do it fast enough, you’ll see Schedule "ab" log immediately followed by Cancel "ab" log and Schedule "abc" log. React always cleans up the previous render’s Effect before the next render’s Effect. This is why even if you type into the input fast, there is at most one timeout scheduled at a time. Edit the input a few times and watch the console to get a feel for how Effects get cleaned up.

Type something into the input and then immediately press “Unmount the component”. Notice how unmounting cleans up the last render’s Effect. Here, it clears the last timeout before it has a chance to fire.

Finally, edit the component above and comment out the cleanup function so that the timeouts don’t get cancelled. Try typing abcde fast. What do you expect to happen in three seconds? Will console.log(text) inside the timeout print the latest text and produce five abcde logs? Give it a try to check your intuition!

Three seconds later, you should see a sequence of logs (a, ab, abc, abcd, and abcde) rather than five abcde logs. Each Effect “captures” the text value from its corresponding render. It doesn’t matter that the text state changed: an Effect from the render with text = 'ab' will always see 'ab'. In other words, Effects from each render are isolated from each other. If you’re curious how this works, you can read about closures.

You can think of useEffect as “attaching” a piece of behavior to the render output. Consider this Effect:

Let’s see what exactly happens as the user navigates around the app.

The user visits <ChatRoom roomId="general" />. Let’s mentally substitute roomId with 'general':

The Effect is also a part of the rendering output. The first render’s Effect becomes:

React runs this Effect, which connects to the 'general' chat room.

Let’s say <ChatRoom roomId="general" /> re-renders. The JSX output is the same:

React sees that the rendering output has not changed, so it doesn’t update the DOM.

The Effect from the second render looks like this:

React compares ['general'] from the second render with ['general'] from the first render. Because all dependencies are the same, React ignores the Effect from the second render. It never gets called.

Then, the user visits <ChatRoom roomId="travel" />. This time, the component returns different JSX:

React updates the DOM to change "Welcome to general" into "Welcome to travel".

The Effect from the third render looks like this:

React compares ['travel'] from the third render with ['general'] from the second render. One dependency is different: Object.is('travel', 'general') is false. The Effect can’t be skipped.

Before React can apply the Effect from the third render, it needs to clean up the last Effect that did run. The second render’s Effect was skipped, so React needs to clean up the first render’s Effect. If you scroll up to the first render, you’ll see that its cleanup calls disconnect() on the connection that was created with createConnection('general'). This disconnects the app from the 'general' chat room.

After that, React runs the third render’s Effect. It connects to the 'travel' chat room.

Finally, let’s say the user navigates away, and the ChatRoom component unmounts. React runs the last Effect’s cleanup function. The last Effect was from the third render. The third render’s cleanup destroys the createConnection('travel') connection. So the app disconnects from the 'travel' room.

When Strict Mode is on, React remounts every component once after mount (state and DOM are preserved). This helps you find Effects that need cleanup and exposes bugs like race conditions early. Additionally, React will remount the Effects whenever you save a file in development. Both of these behaviors are development-only.

In this example, the form renders a <MyInput /> component.

Use the input’s focus() method to make MyInput automatically focus when it appears on the screen. There is already a commented out implementation, but it doesn’t quite work. Figure out why it doesn’t work, and fix it. (If you’re familiar with the autoFocus attribute, pretend that it does not exist: we are reimplementing the same functionality from scratch.)

To verify that your solution works, press “Show form” and verify that the input receives focus (becomes highlighted and the cursor is placed inside). Press “Hide form” and “Show form” again. Verify the input is highlighted again.

MyInput should only focus on mount rather than after every render. To verify that the behavior is right, press “Show form” and then repeatedly press the “Make it uppercase” checkbox. Clicking the checkbox should not focus the input above it.

**Examples:**

Example 1 (sql):
```sql
import { useEffect } from 'react';
```

Example 2 (jsx):
```jsx
function MyComponent() {  useEffect(() => {    // Code here will run after *every* render  });  return <div />;}
```

Example 3 (jsx):
```jsx
<VideoPlayer isPlaying={isPlaying} />;
```

Example 4 (jsx):
```jsx
function VideoPlayer({ src, isPlaying }) {  // TODO: do something with isPlaying  return <video src={src} />;}
```

---

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react

**Contents:**
- Thinking in React
- Start with the mockup
- Step 1: Break the UI into a component hierarchy
- Step 2: Build a static version in React
  - Pitfall
- Step 3: Find the minimal but complete representation of UI state
      - Deep Dive
    - Props vs State
- Step 4: Identify where your state should live
- Step 5: Add inverse data flow

React can change how you think about the designs you look at and the apps you build. When you build a user interface with React, you will first break it apart into pieces called components. Then, you will describe the different visual states for each of your components. Finally, you will connect your components together so that the data flows through them. In this tutorial, we’ll guide you through the thought process of building a searchable product data table with React.

Imagine that you already have a JSON API and a mockup from a designer.

The JSON API returns some data that looks like this:

The mockup looks like this:

To implement a UI in React, you will usually follow the same five steps.

Start by drawing boxes around every component and subcomponent in the mockup and naming them. If you work with a designer, they may have already named these components in their design tool. Ask them!

Depending on your background, you can think about splitting up a design into components in different ways:

If your JSON is well-structured, you’ll often find that it naturally maps to the component structure of your UI. That’s because UI and data models often have the same information architecture—that is, the same shape. Separate your UI into components, where each component matches one piece of your data model.

There are five components on this screen:

If you look at ProductTable (lavender), you’ll see that the table header (containing the “Name” and “Price” labels) isn’t its own component. This is a matter of preference, and you could go either way. For this example, it is a part of ProductTable because it appears inside the ProductTable’s list. However, if this header grows to be complex (e.g., if you add sorting), you can move it into its own ProductTableHeader component.

Now that you’ve identified the components in the mockup, arrange them into a hierarchy. Components that appear within another component in the mockup should appear as a child in the hierarchy:

Now that you have your component hierarchy, it’s time to implement your app. The most straightforward approach is to build a version that renders the UI from your data model without adding any interactivity… yet! It’s often easier to build the static version first and add interactivity later. Building a static version requires a lot of typing and no thinking, but adding interactivity requires a lot of thinking and not a lot of typing.

To build a static version of your app that renders your data model, you’ll want to build components that reuse other components and pass data using props. Props are a way of passing data from parent to child. (If you’re familiar with the concept of state, don’t use state at all to build this static version. State is reserved only for interactivity, that is, data that changes over time. Since this is a static version of the app, you don’t need it.)

You can either build “top down” by starting with building the components higher up in the hierarchy (like FilterableProductTable) or “bottom up” by working from components lower down (like ProductRow). In simpler examples, it’s usually easier to go top-down, and on larger projects, it’s easier to go bottom-up.

(If this code looks intimidating, go through the Quick Start first!)

After building your components, you’ll have a library of reusable components that render your data model. Because this is a static app, the components will only return JSX. The component at the top of the hierarchy (FilterableProductTable) will take your data model as a prop. This is called one-way data flow because the data flows down from the top-level component to the ones at the bottom of the tree.

At this point, you should not be using any state values. That’s for the next step!

To make the UI interactive, you need to let users change your underlying data model. You will use state for this.

Think of state as the minimal set of changing data that your app needs to remember. The most important principle for structuring state is to keep it DRY (Don’t Repeat Yourself). Figure out the absolute minimal representation of the state your application needs and compute everything else on-demand. For example, if you’re building a shopping list, you can store the items as an array in state. If you want to also display the number of items in the list, don’t store the number of items as another state value—instead, read the length of your array.

Now think of all of the pieces of data in this example application:

Which of these are state? Identify the ones that are not:

What’s left is probably state.

Let’s go through them one by one again:

This means only the search text and the value of the checkbox are state! Nicely done!

There are two types of “model” data in React: props and state. The two are very different:

Props and state are different, but they work together. A parent component will often keep some information in state (so that it can change it), and pass it down to child components as their props. It’s okay if the difference still feels fuzzy on the first read. It takes a bit of practice for it to really stick!

After identifying your app’s minimal state data, you need to identify which component is responsible for changing this state, or owns the state. Remember: React uses one-way data flow, passing data down the component hierarchy from parent to child component. It may not be immediately clear which component should own what state. This can be challenging if you’re new to this concept, but you can figure it out by following these steps!

For each piece of state in your application:

In the previous step, you found two pieces of state in this application: the search input text, and the value of the checkbox. In this example, they always appear together, so it makes sense to put them into the same place.

Now let’s run through our strategy for them:

So the state values will live in FilterableProductTable.

Add state to the component with the useState() Hook. Hooks are special functions that let you “hook into” React. Add two state variables at the top of FilterableProductTable and specify their initial state:

Then, pass filterText and inStockOnly to ProductTable and SearchBar as props:

You can start seeing how your application will behave. Edit the filterText initial value from useState('') to useState('fruit') in the sandbox code below. You’ll see both the search input text and the table update:

Notice that editing the form doesn’t work yet. There is a console error in the sandbox above explaining why:

In the sandbox above, ProductTable and SearchBar read the filterText and inStockOnly props to render the table, the input, and the checkbox. For example, here is how SearchBar populates the input value:

However, you haven’t added any code to respond to the user actions like typing yet. This will be your final step.

Currently your app renders correctly with props and state flowing down the hierarchy. But to change the state according to user input, you will need to support data flowing the other way: the form components deep in the hierarchy need to update the state in FilterableProductTable.

React makes this data flow explicit, but it requires a little more typing than two-way data binding. If you try to type or check the box in the example above, you’ll see that React ignores your input. This is intentional. By writing <input value={filterText} />, you’ve set the value prop of the input to always be equal to the filterText state passed in from FilterableProductTable. Since filterText state is never set, the input never changes.

You want to make it so whenever the user changes the form inputs, the state updates to reflect those changes. The state is owned by FilterableProductTable, so only it can call setFilterText and setInStockOnly. To let SearchBar update the FilterableProductTable’s state, you need to pass these functions down to SearchBar:

Inside the SearchBar, you will add the onChange event handlers and set the parent state from them:

Now the application fully works!

You can learn all about handling events and updating state in the Adding Interactivity section.

This was a very brief introduction to how to think about building components and applications with React. You can start a React project right now or dive deeper on all the syntax used in this tutorial.

**Examples:**

Example 1 (json):
```json
[  { category: "Fruits", price: "$1", stocked: true, name: "Apple" },  { category: "Fruits", price: "$1", stocked: true, name: "Dragonfruit" },  { category: "Fruits", price: "$2", stocked: false, name: "Passionfruit" },  { category: "Vegetables", price: "$2", stocked: true, name: "Spinach" },  { category: "Vegetables", price: "$4", stocked: false, name: "Pumpkin" },  { category: "Vegetables", price: "$1", stocked: true, name: "Peas" }]
```

Example 2 (jsx):
```jsx
function FilterableProductTable({ products }) {  const [filterText, setFilterText] = useState('');  const [inStockOnly, setInStockOnly] = useState(false);
```

Example 3 (jsx):
```jsx
<div>  <SearchBar     filterText={filterText}     inStockOnly={inStockOnly} />  <ProductTable     products={products}    filterText={filterText}    inStockOnly={inStockOnly} /></div>
```

Example 4 (jsx):
```jsx
function SearchBar({ filterText, inStockOnly }) {  return (    <form>      <input         type="text"         value={filterText}         placeholder="Search..."/>
```

---

## Tutorial: Tic-Tac-Toe

**URL:** https://react.dev/learn/tutorial-tic-tac-toe

**Contents:**
- Tutorial: Tic-Tac-Toe
  - Note
  - What are you building?
- Setup for the tutorial
  - Note
- Overview
  - Inspecting the starter code
    - App.js
    - styles.css
    - index.js

You will build a small tic-tac-toe game during this tutorial. This tutorial does not assume any existing React knowledge. The techniques you’ll learn in the tutorial are fundamental to building any React app, and fully understanding it will give you a deep understanding of React.

This tutorial is designed for people who prefer to learn by doing and want to quickly try making something tangible. If you prefer learning each concept step by step, start with Describing the UI.

The tutorial is divided into several sections:

In this tutorial, you’ll build an interactive tic-tac-toe game with React.

You can see what it will look like when you’re finished here:

If the code doesn’t make sense to you yet, or if you are unfamiliar with the code’s syntax, don’t worry! The goal of this tutorial is to help you understand React and its syntax.

We recommend that you check out the tic-tac-toe game above before continuing with the tutorial. One of the features that you’ll notice is that there is a numbered list to the right of the game’s board. This list gives you a history of all of the moves that have occurred in the game, and it is updated as the game progresses.

Once you’ve played around with the finished tic-tac-toe game, keep scrolling. You’ll start with a simpler template in this tutorial. Our next step is to set you up so that you can start building the game.

In the live code editor below, click Fork in the top-right corner to open the editor in a new tab using the website CodeSandbox. CodeSandbox lets you write code in your browser and preview how your users will see the app you’ve created. The new tab should display an empty square and the starter code for this tutorial.

You can also follow this tutorial using your local development environment. To do this, you need to:

If you get stuck, don’t let this stop you! Follow along online instead and try a local setup again later.

Now that you’re set up, let’s get an overview of React!

In CodeSandbox you’ll see three main sections:

The App.js file should be selected in the Files section. The contents of that file in the code editor should be:

The browser section should be displaying a square with an X in it like this:

Now let’s have a look at the files in the starter code.

The code in App.js creates a component. In React, a component is a piece of reusable code that represents a part of a user interface. Components are used to render, manage, and update the UI elements in your application. Let’s look at the component line by line to see what’s going on:

The first line defines a function called Square. The export JavaScript keyword makes this function accessible outside of this file. The default keyword tells other files using your code that it’s the main function in your file.

The second line returns a button. The return JavaScript keyword means whatever comes after is returned as a value to the caller of the function. <button> is a JSX element. A JSX element is a combination of JavaScript code and HTML tags that describes what you’d like to display. className="square" is a button property or prop that tells CSS how to style the button. X is the text displayed inside of the button and </button> closes the JSX element to indicate that any following content shouldn’t be placed inside the button.

Click on the file labeled styles.css in the Files section of CodeSandbox. This file defines the styles for your React app. The first two CSS selectors (* and body) define the style of large parts of your app while the .square selector defines the style of any component where the className property is set to square. In your code, that would match the button from your Square component in the App.js file.

Click on the file labeled index.js in the Files section of CodeSandbox. You won’t be editing this file during the tutorial but it is the bridge between the component you created in the App.js file and the web browser.

Lines 1-5 bring all the necessary pieces together:

The remainder of the file brings all the pieces together and injects the final product into index.html in the public folder.

Let’s get back to App.js. This is where you’ll spend the rest of the tutorial.

Currently the board is only a single square, but you need nine! If you just try and copy paste your square to make two squares like this:

You’ll get this error:

React components need to return a single JSX element and not multiple adjacent JSX elements like two buttons. To fix this you can use Fragments (<> and </>) to wrap multiple adjacent JSX elements like this:

Great! Now you just need to copy-paste a few times to add nine squares and…

Oh no! The squares are all in a single line, not in a grid like you need for our board. To fix this you’ll need to group your squares into rows with divs and add some CSS classes. While you’re at it, you’ll give each square a number to make sure you know where each square is displayed.

In the App.js file, update the Square component to look like this:

The CSS defined in styles.css styles the divs with the className of board-row. Now that you’ve grouped your components into rows with the styled divs you have your tic-tac-toe board:

But you now have a problem. Your component named Square, really isn’t a square anymore. Let’s fix that by changing the name to Board:

At this point your code should look something like this:

Psssst… That’s a lot to type! It’s okay to copy and paste code from this page. However, if you’re up for a little challenge, we recommend only copying code that you’ve manually typed at least once yourself.

Next, you’ll want to change the value of a square from empty to “X” when the user clicks on the square. With how you’ve built the board so far you would need to copy-paste the code that updates the square nine times (once for each square you have)! Instead of copy-pasting, React’s component architecture allows you to create a reusable component to avoid messy, duplicated code.

First, you are going to copy the line defining your first square (<button className="square">1</button>) from your Board component into a new Square component:

Then you’ll update the Board component to render that Square component using JSX syntax:

Note how unlike the browser divs, your own components Board and Square must start with a capital letter.

Oh no! You lost the numbered squares you had before. Now each square says “1”. To fix this, you will use props to pass the value each square should have from the parent component (Board) to its child (Square).

Update the Square component to read the value prop that you’ll pass from the Board:

function Square({ value }) indicates the Square component can be passed a prop called value.

Now you want to display that value instead of 1 inside every square. Try doing it like this:

Oops, this is not what you wanted:

You wanted to render the JavaScript variable called value from your component, not the word “value”. To “escape into JavaScript” from JSX, you need curly braces. Add curly braces around value in JSX like so:

For now, you should see an empty board:

This is because the Board component hasn’t passed the value prop to each Square component it renders yet. To fix it you’ll add the value prop to each Square component rendered by the Board component:

Now you should see a grid of numbers again:

Your updated code should look like this:

Let’s fill the Square component with an X when you click it. Declare a function called handleClick inside of the Square. Then, add onClick to the props of the button JSX element returned from the Square:

If you click on a square now, you should see a log saying "clicked!" in the Console tab at the bottom of the Browser section in CodeSandbox. Clicking the square more than once will log "clicked!" again. Repeated console logs with the same message will not create more lines in the console. Instead, you will see an incrementing counter next to your first "clicked!" log.

If you are following this tutorial using your local development environment, you need to open your browser’s Console. For example, if you use the Chrome browser, you can view the Console with the keyboard shortcut Shift + Ctrl + J (on Windows/Linux) or Option + ⌘ + J (on macOS).

As a next step, you want the Square component to “remember” that it got clicked, and fill it with an “X” mark. To “remember” things, components use state.

React provides a special function called useState that you can call from your component to let it “remember” things. Let’s store the current value of the Square in state, and change it when the Square is clicked.

Import useState at the top of the file. Remove the value prop from the Square component. Instead, add a new line at the start of the Square that calls useState. Have it return a state variable called value:

value stores the value and setValue is a function that can be used to change the value. The null passed to useState is used as the initial value for this state variable, so value here starts off equal to null.

Since the Square component no longer accepts props anymore, you’ll remove the value prop from all nine of the Square components created by the Board component:

Now you’ll change Square to display an “X” when clicked. Replace the console.log("clicked!"); event handler with setValue('X');. Now your Square component looks like this:

By calling this set function from an onClick handler, you’re telling React to re-render that Square whenever its <button> is clicked. After the update, the Square’s value will be 'X', so you’ll see the “X” on the game board. Click on any Square, and “X” should show up:

Each Square has its own state: the value stored in each Square is completely independent of the others. When you call a set function in a component, React automatically updates the child components inside too.

After you’ve made the above changes, your code will look like this:

React DevTools let you check the props and the state of your React components. You can find the React DevTools tab at the bottom of the browser section in CodeSandbox:

To inspect a particular component on the screen, use the button in the top left corner of React DevTools:

For local development, React DevTools is available as a Chrome, Firefox, and Edge browser extension. Install it, and the Components tab will appear in your browser Developer Tools for sites using React.

By this point, you have all the basic building blocks for your tic-tac-toe game. To have a complete game, you now need to alternate placing “X”s and “O”s on the board, and you need a way to determine a winner.

Currently, each Square component maintains a part of the game’s state. To check for a winner in a tic-tac-toe game, the Board would need to somehow know the state of each of the 9 Square components.

How would you approach that? At first, you might guess that the Board needs to “ask” each Square for that Square’s state. Although this approach is technically possible in React, we discourage it because the code becomes difficult to understand, susceptible to bugs, and hard to refactor. Instead, the best approach is to store the game’s state in the parent Board component instead of in each Square. The Board component can tell each Square what to display by passing a prop, like you did when you passed a number to each Square.

To collect data from multiple children, or to have two child components communicate with each other, declare the shared state in their parent component instead. The parent component can pass that state back down to the children via props. This keeps the child components in sync with each other and with their parent.

Lifting state into a parent component is common when React components are refactored.

Let’s take this opportunity to try it out. Edit the Board component so that it declares a state variable named squares that defaults to an array of 9 nulls corresponding to the 9 squares:

Array(9).fill(null) creates an array with nine elements and sets each of them to null. The useState() call around it declares a squares state variable that’s initially set to that array. Each entry in the array corresponds to the value of a square. When you fill the board in later, the squares array will look like this:

Now your Board component needs to pass the value prop down to each Square that it renders:

Next, you’ll edit the Square component to receive the value prop from the Board component. This will require removing the Square component’s own stateful tracking of value and the button’s onClick prop:

At this point you should see an empty tic-tac-toe board:

And your code should look like this:

Each Square will now receive a value prop that will either be 'X', 'O', or null for empty squares.

Next, you need to change what happens when a Square is clicked. The Board component now maintains which squares are filled. You’ll need to create a way for the Square to update the Board’s state. Since state is private to a component that defines it, you cannot update the Board’s state directly from Square.

Instead, you’ll pass down a function from the Board component to the Square component, and you’ll have Square call that function when a square is clicked. You’ll start with the function that the Square component will call when it is clicked. You’ll call that function onSquareClick:

Next, you’ll add the onSquareClick function to the Square component’s props:

Now you’ll connect the onSquareClick prop to a function in the Board component that you’ll name handleClick. To connect onSquareClick to handleClick you’ll pass a function to the onSquareClick prop of the first Square component:

Lastly, you will define the handleClick function inside the Board component to update the squares array holding your board’s state:

The handleClick function creates a copy of the squares array (nextSquares) with the JavaScript slice() Array method. Then, handleClick updates the nextSquares array to add X to the first ([0] index) square.

Calling the setSquares function lets React know the state of the component has changed. This will trigger a re-render of the components that use the squares state (Board) as well as its child components (the Square components that make up the board).

JavaScript supports closures which means an inner function (e.g. handleClick) has access to variables and functions defined in an outer function (e.g. Board). The handleClick function can read the squares state and call the setSquares method because they are both defined inside of the Board function.

Now you can add X’s to the board… but only to the upper left square. Your handleClick function is hardcoded to update the index for the upper left square (0). Let’s update handleClick to be able to update any square. Add an argument i to the handleClick function that takes the index of the square to update:

Next, you will need to pass that i to handleClick. You could try to set the onSquareClick prop of square to be handleClick(0) directly in the JSX like this, but it won’t work:

Here is why this doesn’t work. The handleClick(0) call will be a part of rendering the board component. Because handleClick(0) alters the state of the board component by calling setSquares, your entire board component will be re-rendered again. But this runs handleClick(0) again, leading to an infinite loop:

Why didn’t this problem happen earlier?

When you were passing onSquareClick={handleClick}, you were passing the handleClick function down as a prop. You were not calling it! But now you are calling that function right away—notice the parentheses in handleClick(0)—and that’s why it runs too early. You don’t want to call handleClick until the user clicks!

You could fix this by creating a function like handleFirstSquareClick that calls handleClick(0), a function like handleSecondSquareClick that calls handleClick(1), and so on. You would pass (rather than call) these functions down as props like onSquareClick={handleFirstSquareClick}. This would solve the infinite loop.

However, defining nine different functions and giving each of them a name is too verbose. Instead, let’s do this:

Notice the new () => syntax. Here, () => handleClick(0) is an arrow function, which is a shorter way to define functions. When the square is clicked, the code after the => “arrow” will run, calling handleClick(0).

Now you need to update the other eight squares to call handleClick from the arrow functions you pass. Make sure that the argument for each call of the handleClick corresponds to the index of the correct square:

Now you can again add X’s to any square on the board by clicking on them:

But this time all the state management is handled by the Board component!

This is what your code should look like:

Now that your state handling is in the Board component, the parent Board component passes props to the child Square components so that they can be displayed correctly. When clicking on a Square, the child Square component now asks the parent Board component to update the state of the board. When the Board’s state changes, both the Board component and every child Square re-renders automatically. Keeping the state of all squares in the Board component will allow it to determine the winner in the future.

Let’s recap what happens when a user clicks the top left square on your board to add an X to it:

In the end the user sees that the upper left square has changed from empty to having an X after clicking it.

The DOM <button> element’s onClick attribute has a special meaning to React because it is a built-in component. For custom components like Square, the naming is up to you. You could give any name to the Square’s onSquareClick prop or Board’s handleClick function, and the code would work the same. In React, it’s conventional to use onSomething names for props which represent events and handleSomething for the function definitions which handle those events.

Note how in handleClick, you call .slice() to create a copy of the squares array instead of modifying the existing array. To explain why, we need to discuss immutability and why immutability is important to learn.

There are generally two approaches to changing data. The first approach is to mutate the data by directly changing the data’s values. The second approach is to replace the data with a new copy which has the desired changes. Here is what it would look like if you mutated the squares array:

And here is what it would look like if you changed data without mutating the squares array:

The result is the same but by not mutating (changing the underlying data) directly, you gain several benefits.

Immutability makes complex features much easier to implement. Later in this tutorial, you will implement a “time travel” feature that lets you review the game’s history and “jump back” to past moves. This functionality isn’t specific to games—an ability to undo and redo certain actions is a common requirement for apps. Avoiding direct data mutation lets you keep previous versions of the data intact, and reuse them later.

There is also another benefit of immutability. By default, all child components re-render automatically when the state of a parent component changes. This includes even the child components that weren’t affected by the change. Although re-rendering is not by itself noticeable to the user (you shouldn’t actively try to avoid it!), you might want to skip re-rendering a part of the tree that clearly wasn’t affected by it for performance reasons. Immutability makes it very cheap for components to compare whether their data has changed or not. You can learn more about how React chooses when to re-render a component in the memo API reference.

It’s now time to fix a major defect in this tic-tac-toe game: the “O”s cannot be marked on the board.

You’ll set the first move to be “X” by default. Let’s keep track of this by adding another piece of state to the Board component:

Each time a player moves, xIsNext (a boolean) will be flipped to determine which player goes next and the game’s state will be saved. You’ll update the Board’s handleClick function to flip the value of xIsNext:

Now, as you click on different squares, they will alternate between X and O, as they should!

But wait, there’s a problem. Try clicking on the same square multiple times:

The X is overwritten by an O! While this would add a very interesting twist to the game, we’re going to stick to the original rules for now.

When you mark a square with an X or an O you aren’t first checking to see if the square already has an X or O value. You can fix this by returning early. You’ll check to see if the square already has an X or an O. If the square is already filled, you will return in the handleClick function early—before it tries to update the board state.

Now you can only add X’s or O’s to empty squares! Here is what your code should look like at this point:

Now that the players can take turns, you’ll want to show when the game is won and there are no more turns to make. To do this you’ll add a helper function called calculateWinner that takes an array of 9 squares, checks for a winner and returns 'X', 'O', or null as appropriate. Don’t worry too much about the calculateWinner function; it’s not specific to React:

It does not matter whether you define calculateWinner before or after the Board. Let’s put it at the end so that you don’t have to scroll past it every time you edit your components.

You will call calculateWinner(squares) in the Board component’s handleClick function to check if a player has won. You can perform this check at the same time you check if a user has clicked a square that already has an X or an O. We’d like to return early in both cases:

To let the players know when the game is over, you can display text such as “Winner: X” or “Winner: O”. To do that you’ll add a status section to the Board component. The status will display the winner if the game is over and if the game is ongoing you’ll display which player’s turn is next:

Congratulations! You now have a working tic-tac-toe game. And you’ve just learned the basics of React too. So you are the real winner here. Here is what the code should look like:

As a final exercise, let’s make it possible to “go back in time” to the previous moves in the game.

If you mutated the squares array, implementing time travel would be very difficult.

However, you used slice() to create a new copy of the squares array after every move, and treated it as immutable. This will allow you to store every past version of the squares array, and navigate between the turns that have already happened.

You’ll store the past squares arrays in another array called history, which you’ll store as a new state variable. The history array represents all board states, from the first to the last move, and has a shape like this:

You will now write a new top-level component called Game to display a list of past moves. That’s where you will place the history state that contains the entire game history.

Placing the history state into the Game component will let you remove the squares state from its child Board component. Just like you “lifted state up” from the Square component into the Board component, you will now lift it up from the Board into the top-level Game component. This gives the Game component full control over the Board’s data and lets it instruct the Board to render previous turns from the history.

First, add a Game component with export default. Have it render the Board component and some markup:

Note that you are removing the export default keywords before the function Board() { declaration and adding them before the function Game() { declaration. This tells your index.js file to use the Game component as the top-level component instead of your Board component. The additional divs returned by the Game component are making room for the game information you’ll add to the board later.

Add some state to the Game component to track which player is next and the history of moves:

Notice how [Array(9).fill(null)] is an array with a single item, which itself is an array of 9 nulls.

To render the squares for the current move, you’ll want to read the last squares array from the history. You don’t need useState for this—you already have enough information to calculate it during rendering:

Next, create a handlePlay function inside the Game component that will be called by the Board component to update the game. Pass xIsNext, currentSquares and handlePlay as props to the Board component:

Let’s make the Board component fully controlled by the props it receives. Change the Board component to take three props: xIsNext, squares, and a new onPlay function that Board can call with the updated squares array when a player makes a move. Next, remove the first two lines of the Board function that call useState:

Now replace the setSquares and setXIsNext calls in handleClick in the Board component with a single call to your new onPlay function so the Game component can update the Board when the user clicks a square:

The Board component is fully controlled by the props passed to it by the Game component. You need to implement the handlePlay function in the Game component to get the game working again.

What should handlePlay do when called? Remember that Board used to call setSquares with an updated array; now it passes the updated squares array to onPlay.

The handlePlay function needs to update Game’s state to trigger a re-render, but you don’t have a setSquares function that you can call any more—you’re now using the history state variable to store this information. You’ll want to update history by appending the updated squares array as a new history entry. You also want to toggle xIsNext, just as Board used to do:

Here, [...history, nextSquares] creates a new array that contains all the items in history, followed by nextSquares. (You can read the ...history spread syntax as “enumerate all the items in history”.)

For example, if history is [[null,null,null], ["X",null,null]] and nextSquares is ["X",null,"O"], then the new [...history, nextSquares] array will be [[null,null,null], ["X",null,null], ["X",null,"O"]].

At this point, you’ve moved the state to live in the Game component, and the UI should be fully working, just as it was before the refactor. Here is what the code should look like at this point:

Since you are recording the tic-tac-toe game’s history, you can now display a list of past moves to the player.

React elements like <button> are regular JavaScript objects; you can pass them around in your application. To render multiple items in React, you can use an array of React elements.

You already have an array of history moves in state, so now you need to transform it to an array of React elements. In JavaScript, to transform one array into another, you can use the array map method:

You’ll use map to transform your history of moves into React elements representing buttons on the screen, and display a list of buttons to “jump” to past moves. Let’s map over the history in the Game component:

You can see what your code should look like below. Note that you should see an error in the developer tools console that says:

You’ll fix this error in the next section.

As you iterate through the history array inside the function you passed to map, the squares argument goes through each element of history, and the move argument goes through each array index: 0, 1, 2, …. (In most cases, you’d need the actual array elements, but to render a list of moves you will only need indexes.)

For each move in the tic-tac-toe game’s history, you create a list item <li> which contains a button <button>. The button has an onClick handler which calls a function called jumpTo (that you haven’t implemented yet).

For now, you should see a list of the moves that occurred in the game and an error in the developer tools console. Let’s discuss what the “key” error means.

When you render a list, React stores some information about each rendered list item. When you update a list, React needs to determine what has changed. You could have added, removed, re-arranged, or updated the list’s items.

Imagine transitioning from

In addition to the updated counts, a human reading this would probably say that you swapped Alexa and Ben’s ordering and inserted Claudia between Alexa and Ben. However, React is a computer program and does not know what you intended, so you need to specify a key property for each list item to differentiate each list item from its siblings. If your data was from a database, Alexa, Ben, and Claudia’s database IDs could be used as keys.

When a list is re-rendered, React takes each list item’s key and searches the previous list’s items for a matching key. If the current list has a key that didn’t exist before, React creates a component. If the current list is missing a key that existed in the previous list, React destroys the previous component. If two keys match, the corresponding component is moved.

Keys tell React about the identity of each component, which allows React to maintain state between re-renders. If a component’s key changes, the component will be destroyed and re-created with a new state.

key is a special and reserved property in React. When an element is created, React extracts the key property and stores the key directly on the returned element. Even though key may look like it is passed as props, React automatically uses key to decide which components to update. There’s no way for a component to ask what key its parent specified.

It’s strongly recommended that you assign proper keys whenever you build dynamic lists. If you don’t have an appropriate key, you may want to consider restructuring your data so that you do.

If no key is specified, React will report an error and use the array index as a key by default. Using the array index as a key is problematic when trying to re-order a list’s items or inserting/removing list items. Explicitly passing key={i} silences the error but has the same problems as array indices and is not recommended in most cases.

Keys do not need to be globally unique; they only need to be unique between components and their siblings.

In the tic-tac-toe game’s history, each past move has a unique ID associated with it: it’s the sequential number of the move. Moves will never be re-ordered, deleted, or inserted in the middle, so it’s safe to use the move index as a key.

In the Game function, you can add the key as <li key={move}>, and if you reload the rendered game, React’s “key” error should disappear:

Before you can implement jumpTo, you need the Game component to keep track of which step the user is currently viewing. To do this, define a new state variable called currentMove, defaulting to 0:

Next, update the jumpTo function inside Game to update that currentMove. You’ll also set xIsNext to true if the number that you’re changing currentMove to is even.

You will now make two changes to the Game’s handlePlay function which is called when you click on a square.

Finally, you will modify the Game component to render the currently selected move, instead of always rendering the final move:

If you click on any step in the game’s history, the tic-tac-toe board should immediately update to show what the board looked like after that step occurred.

If you look at the code very closely, you may notice that xIsNext === true when currentMove is even and xIsNext === false when currentMove is odd. In other words, if you know the value of currentMove, then you can always figure out what xIsNext should be.

There’s no reason for you to store both of these in state. In fact, always try to avoid redundant state. Simplifying what you store in state reduces bugs and makes your code easier to understand. Change Game so that it doesn’t store xIsNext as a separate state variable and instead figures it out based on the currentMove:

You no longer need the xIsNext state declaration or the calls to setXIsNext. Now, there’s no chance for xIsNext to get out of sync with currentMove, even if you make a mistake while coding the components.

Congratulations! You’ve created a tic-tac-toe game that:

Nice work! We hope you now feel like you have a decent grasp of how React works.

Check out the final result here:

If you have extra time or want to practice your new React skills, here are some ideas for improvements that you could make to the tic-tac-toe game, listed in order of increasing difficulty:

Throughout this tutorial, you’ve touched on React concepts including elements, components, props, and state. Now that you’ve seen how these concepts work when building a game, check out Thinking in React to see how the same React concepts work when building an app’s UI.

**Examples:**

Example 1 (jsx):
```jsx
export default function Square() {  return <button className="square">X</button>;}
```

Example 2 (jsx):
```jsx
export default function Square() {  return <button className="square">X</button>;}
```

Example 3 (jsx):
```jsx
export default function Square() {  return <button className="square">X</button>;}
```

Example 4 (sql):
```sql
import { StrictMode } from 'react';import { createRoot } from 'react-dom/client';import './styles.css';import App from './App';
```

---

## Understanding Your UI as a Tree

**URL:** https://react.dev/learn/understanding-your-ui-as-a-tree

**Contents:**
- Understanding Your UI as a Tree
  - You will learn
- Your UI as a tree
- The Render Tree
      - Deep Dive
    - Where are the HTML tags in the render tree?
- The Module Dependency Tree
- Recap

Your React app is taking shape with many components being nested within each other. How does React keep track of your app’s component structure?

React, and many other UI libraries, model UI as a tree. Thinking of your app as a tree is useful for understanding the relationship between components. This understanding will help you debug future concepts like performance and state management.

Trees are a relationship model between items. The UI is often represented using tree structures. For example, browsers use tree structures to model HTML (DOM) and CSS (CSSOM). Mobile platforms also use trees to represent their view hierarchy.

React creates a UI tree from your components. In this example, the UI tree is then used to render to the DOM.

Like browsers and mobile platforms, React also uses tree structures to manage and model the relationship between components in a React app. These trees are useful tools to understand how data flows through a React app and how to optimize rendering and app size.

A major feature of components is the ability to compose components of other components. As we nest components, we have the concept of parent and child components, where each parent component may itself be a child of another component.

When we render a React app, we can model this relationship in a tree, known as the render tree.

Here is a React app that renders inspirational quotes.

React creates a render tree, a UI tree, composed of the rendered components.

From the example app, we can construct the above render tree.

The tree is composed of nodes, each of which represents a component. App, FancyText, Copyright, to name a few, are all nodes in our tree.

The root node in a React render tree is the root component of the app. In this case, the root component is App and it is the first component React renders. Each arrow in the tree points from a parent component to a child component.

You’ll notice in the above render tree, there is no mention of the HTML tags that each component renders. This is because the render tree is only composed of React components.

React, as a UI framework, is platform agnostic. On react.dev, we showcase examples that render to the web, which uses HTML markup as its UI primitives. But a React app could just as likely render to a mobile or desktop platform, which may use different UI primitives like UIView or FrameworkElement.

These platform UI primitives are not a part of React. React render trees can provide insight to our React app regardless of what platform your app renders to.

A render tree represents a single render pass of a React application. With conditional rendering, a parent component may render different children depending on the data passed.

We can update the app to conditionally render either an inspirational quote or color.

With conditional rendering, across different renders, the render tree may render different components.

In this example, depending on what inspiration.type is, we may render <FancyText> or <Color>. The render tree may be different for each render pass.

Although render trees may differ across render passes, these trees are generally helpful for identifying what the top-level and leaf components are in a React app. Top-level components are the components nearest to the root component and affect the rendering performance of all the components beneath them and often contain the most complexity. Leaf components are near the bottom of the tree and have no child components and are often frequently re-rendered.

Identifying these categories of components are useful for understanding data flow and performance of your app.

Another relationship in a React app that can be modeled with a tree are an app’s module dependencies. As we break up our components and logic into separate files, we create JS modules where we may export components, functions, or constants.

Each node in a module dependency tree is a module and each branch represents an import statement in that module.

If we take the previous Inspirations app, we can build a module dependency tree, or dependency tree for short.

The module dependency tree for the Inspirations app.

The root node of the tree is the root module, also known as the entrypoint file. It often is the module that contains the root component.

Comparing to the render tree of the same app, there are similar structures but some notable differences:

Dependency trees are useful to determine what modules are necessary to run your React app. When building a React app for production, there is typically a build step that will bundle all the necessary JavaScript to ship to the client. The tool responsible for this is called a bundler, and bundlers will use the dependency tree to determine what modules should be included.

As your app grows, often the bundle size does too. Large bundle sizes are expensive for a client to download and run. Large bundle sizes can delay the time for your UI to get drawn. Getting a sense of your app’s dependency tree may help with debugging these issues.

---

## Updating Arrays in State

**URL:** https://react.dev/learn/updating-arrays-in-state

**Contents:**
- Updating Arrays in State
  - You will learn
- Updating arrays without mutation
  - Pitfall
  - Adding to an array
  - Removing from an array
  - Transforming an array
  - Replacing items in an array
  - Inserting into an array
  - Making other changes to an array

Arrays are mutable in JavaScript, but you should treat them as immutable when you store them in state. Just like with objects, when you want to update an array stored in state, you need to create a new one (or make a copy of an existing one), and then set state to use the new array.

In JavaScript, arrays are just another kind of object. Like with objects, you should treat arrays in React state as read-only. This means that you shouldn’t reassign items inside an array like arr[0] = 'bird', and you also shouldn’t use methods that mutate the array, such as push() and pop().

Instead, every time you want to update an array, you’ll want to pass a new array to your state setting function. To do that, you can create a new array from the original array in your state by calling its non-mutating methods like filter() and map(). Then you can set your state to the resulting new array.

Here is a reference table of common array operations. When dealing with arrays inside React state, you will need to avoid the methods in the left column, and instead prefer the methods in the right column:

Alternatively, you can use Immer which lets you use methods from both columns.

Unfortunately, slice and splice are named similarly but are very different:

In React, you will be using slice (no p!) a lot more often because you don’t want to mutate objects or arrays in state. Updating Objects explains what mutation is and why it’s not recommended for state.

push() will mutate an array, which you don’t want:

Instead, create a new array which contains the existing items and a new item at the end. There are multiple ways to do this, but the easiest one is to use the ... array spread syntax:

Now it works correctly:

The array spread syntax also lets you prepend an item by placing it before the original ...artists:

In this way, spread can do the job of both push() by adding to the end of an array and unshift() by adding to the beginning of an array. Try it in the sandbox above!

The easiest way to remove an item from an array is to filter it out. In other words, you will produce a new array that will not contain that item. To do this, use the filter method, for example:

Click the “Delete” button a few times, and look at its click handler.

Here, artists.filter(a => a.id !== artist.id) means “create an array that consists of those artists whose IDs are different from artist.id”. In other words, each artist’s “Delete” button will filter that artist out of the array, and then request a re-render with the resulting array. Note that filter does not modify the original array.

If you want to change some or all items of the array, you can use map() to create a new array. The function you will pass to map can decide what to do with each item, based on its data or its index (or both).

In this example, an array holds coordinates of two circles and a square. When you press the button, it moves only the circles down by 50 pixels. It does this by producing a new array of data using map():

It is particularly common to want to replace one or more items in an array. Assignments like arr[0] = 'bird' are mutating the original array, so instead you’ll want to use map for this as well.

To replace an item, create a new array with map. Inside your map call, you will receive the item index as the second argument. Use it to decide whether to return the original item (the first argument) or something else:

Sometimes, you may want to insert an item at a particular position that’s neither at the beginning nor at the end. To do this, you can use the ... array spread syntax together with the slice() method. The slice() method lets you cut a “slice” of the array. To insert an item, you will create an array that spreads the slice before the insertion point, then the new item, and then the rest of the original array.

In this example, the Insert button always inserts at the index 1:

There are some things you can’t do with the spread syntax and non-mutating methods like map() and filter() alone. For example, you may want to reverse or sort an array. The JavaScript reverse() and sort() methods are mutating the original array, so you can’t use them directly.

However, you can copy the array first, and then make changes to it.

Here, you use the [...list] spread syntax to create a copy of the original array first. Now that you have a copy, you can use mutating methods like nextList.reverse() or nextList.sort(), or even assign individual items with nextList[0] = "something".

However, even if you copy an array, you can’t mutate existing items inside of it directly. This is because copying is shallow—the new array will contain the same items as the original one. So if you modify an object inside the copied array, you are mutating the existing state. For example, code like this is a problem.

Although nextList and list are two different arrays, nextList[0] and list[0] point to the same object. So by changing nextList[0].seen, you are also changing list[0].seen. This is a state mutation, which you should avoid! You can solve this issue in a similar way to updating nested JavaScript objects—by copying individual items you want to change instead of mutating them. Here’s how.

Objects are not really located “inside” arrays. They might appear to be “inside” in code, but each object in an array is a separate value, to which the array “points”. This is why you need to be careful when changing nested fields like list[0]. Another person’s artwork list may point to the same element of the array!

When updating nested state, you need to create copies from the point where you want to update, and all the way up to the top level. Let’s see how this works.

In this example, two separate artwork lists have the same initial state. They are supposed to be isolated, but because of a mutation, their state is accidentally shared, and checking a box in one list affects the other list:

The problem is in code like this:

Although the myNextList array itself is new, the items themselves are the same as in the original myList array. So changing artwork.seen changes the original artwork item. That artwork item is also in yourList, which causes the bug. Bugs like this can be difficult to think about, but thankfully they disappear if you avoid mutating state.

You can use map to substitute an old item with its updated version without mutation.

Here, ... is the object spread syntax used to create a copy of an object.

With this approach, none of the existing state items are being mutated, and the bug is fixed:

In general, you should only mutate objects that you have just created. If you were inserting a new artwork, you could mutate it, but if you’re dealing with something that’s already in state, you need to make a copy.

Updating nested arrays without mutation can get a little bit repetitive. Just as with objects:

Here is the Art Bucket List example rewritten with Immer:

Note how with Immer, mutation like artwork.seen = nextSeen is now okay:

This is because you’re not mutating the original state, but you’re mutating a special draft object provided by Immer. Similarly, you can apply mutating methods like push() and pop() to the content of the draft.

Behind the scenes, Immer always constructs the next state from scratch according to the changes that you’ve done to the draft. This keeps your event handlers very concise without ever mutating state.

Fill in the handleIncreaseClick logic so that pressing ”+” increases the corresponding number:

**Examples:**

Example 1 (css):
```css
setArtists( // Replace the state  [ // with a new array    ...artists, // that contains all the old items    { id: nextId++, name: name } // and one new item at the end  ]);
```

Example 2 (css):
```css
setArtists([  { id: nextId++, name: name },  ...artists // Put old items at the end]);
```

Example 3 (javascript):
```javascript
setArtists(  artists.filter(a => a.id !== artist.id));
```

Example 4 (javascript):
```javascript
const nextList = [...list];nextList[0].seen = true; // Problem: mutates list[0]setList(nextList);
```

---

## Updating Objects in State

**URL:** https://react.dev/learn/updating-objects-in-state

**Contents:**
- Updating Objects in State
  - You will learn
- What’s a mutation?
- Treat state as read-only
      - Deep Dive
    - Local mutation is fine
- Copying objects with the spread syntax
      - Deep Dive
    - Using a single event handler for multiple fields
- Updating a nested object

State can hold any kind of JavaScript value, including objects. But you shouldn’t change objects that you hold in the React state directly. Instead, when you want to update an object, you need to create a new one (or make a copy of an existing one), and then set the state to use that copy.

You can store any kind of JavaScript value in state.

So far you’ve been working with numbers, strings, and booleans. These kinds of JavaScript values are “immutable”, meaning unchangeable or “read-only”. You can trigger a re-render to replace a value:

The x state changed from 0 to 5, but the number 0 itself did not change. It’s not possible to make any changes to the built-in primitive values like numbers, strings, and booleans in JavaScript.

Now consider an object in state:

Technically, it is possible to change the contents of the object itself. This is called a mutation:

However, although objects in React state are technically mutable, you should treat them as if they were immutable—like numbers, booleans, and strings. Instead of mutating them, you should always replace them.

In other words, you should treat any JavaScript object that you put into state as read-only.

This example holds an object in state to represent the current pointer position. The red dot is supposed to move when you touch or move the cursor over the preview area. But the dot stays in the initial position:

The problem is with this bit of code.

This code modifies the object assigned to position from the previous render. But without using the state setting function, React has no idea that object has changed. So React does not do anything in response. It’s like trying to change the order after you’ve already eaten the meal. While mutating state can work in some cases, we don’t recommend it. You should treat the state value you have access to in a render as read-only.

To actually trigger a re-render in this case, create a new object and pass it to the state setting function:

With setPosition, you’re telling React:

Notice how the red dot now follows your pointer when you touch or hover over the preview area:

Code like this is a problem because it modifies an existing object in state:

But code like this is absolutely fine because you’re mutating a fresh object you have just created:

In fact, it is completely equivalent to writing this:

Mutation is only a problem when you change existing objects that are already in state. Mutating an object you’ve just created is okay because no other code references it yet. Changing it isn’t going to accidentally impact something that depends on it. This is called a “local mutation”. You can even do local mutation while rendering. Very convenient and completely okay!

In the previous example, the position object is always created fresh from the current cursor position. But often, you will want to include existing data as a part of the new object you’re creating. For example, you may want to update only one field in a form, but keep the previous values for all other fields.

These input fields don’t work because the onChange handlers mutate the state:

For example, this line mutates the state from a past render:

The reliable way to get the behavior you’re looking for is to create a new object and pass it to setPerson. But here, you want to also copy the existing data into it because only one of the fields has changed:

You can use the ... object spread syntax so that you don’t need to copy every property separately.

Notice how you didn’t declare a separate state variable for each input field. For large forms, keeping all data grouped in an object is very convenient—as long as you update it correctly!

Note that the ... spread syntax is “shallow”—it only copies things one level deep. This makes it fast, but it also means that if you want to update a nested property, you’ll have to use it more than once.

You can also use the [ and ] braces inside your object definition to specify a property with a dynamic name. Here is the same example, but with a single event handler instead of three different ones:

Here, e.target.name refers to the name property given to the <input> DOM element.

Consider a nested object structure like this:

If you wanted to update person.artwork.city, it’s clear how to do it with mutation:

But in React, you treat state as immutable! In order to change city, you would first need to produce the new artwork object (pre-populated with data from the previous one), and then produce the new person object which points at the new artwork:

Or, written as a single function call:

This gets a bit wordy, but it works fine for many cases:

An object like this appears “nested” in code:

However, “nesting” is an inaccurate way to think about how objects behave. When the code executes, there is no such thing as a “nested” object. You are really looking at two different objects:

The obj1 object is not “inside” obj2. For example, obj3 could “point” at obj1 too:

If you were to mutate obj3.artwork.city, it would affect both obj2.artwork.city and obj1.city. This is because obj3.artwork, obj2.artwork, and obj1 are the same object. This is difficult to see when you think of objects as “nested”. Instead, they are separate objects “pointing” at each other with properties.

If your state is deeply nested, you might want to consider flattening it. But, if you don’t want to change your state structure, you might prefer a shortcut to nested spreads. Immer is a popular library that lets you write using the convenient but mutating syntax and takes care of producing the copies for you. With Immer, the code you write looks like you are “breaking the rules” and mutating an object:

But unlike a regular mutation, it doesn’t overwrite the past state!

The draft provided by Immer is a special type of object, called a Proxy, that “records” what you do with it. This is why you can mutate it freely as much as you like! Under the hood, Immer figures out which parts of the draft have been changed, and produces a completely new object that contains your edits.

Here is the above example converted to Immer:

Notice how much more concise the event handlers have become. You can mix and match useState and useImmer in a single component as much as you like. Immer is a great way to keep the update handlers concise, especially if there’s nesting in your state, and copying objects leads to repetitive code.

There are a few reasons:

In practice, you can often “get away” with mutating state in React, but we strongly advise you not to do that so that you can use new React features developed with this approach in mind. Future contributors and perhaps even your future self will thank you!

This form has a few bugs. Click the button that increases the score a few times. Notice that it does not increase. Then edit the first name, and notice that the score has suddenly “caught up” with your changes. Finally, edit the last name, and notice that the score has disappeared completely.

Your task is to fix all of these bugs. As you fix them, explain why each of them happens.

**Examples:**

Example 1 (jsx):
```jsx
const [x, setX] = useState(0);
```

Example 2 (jsx):
```jsx
const [position, setPosition] = useState({ x: 0, y: 0 });
```

Example 3 (unknown):
```unknown
position.x = 5;
```

Example 4 (javascript):
```javascript
onPointerMove={e => {  position.x = e.clientX;  position.y = e.clientY;}}
```

---

## Using TypeScript

**URL:** https://react.dev/learn/typescript

**Contents:**
- Using TypeScript
  - You will learn
- Installation
  - Adding TypeScript to an existing React project
- TypeScript with React Components
  - Note
  - Note
- Example Hooks
  - useState
  - useReducer

TypeScript is a popular way to add type definitions to JavaScript codebases. Out of the box, TypeScript supports JSX and you can get full React Web support by adding @types/react and @types/react-dom to your project.

All production-grade React frameworks offer support for using TypeScript. Follow the framework specific guide for installation:

To install the latest version of React’s type definitions:

The following compiler options need to be set in your tsconfig.json:

Every file containing JSX must use the .tsx file extension. This is a TypeScript-specific extension that tells TypeScript that this file contains JSX.

Writing TypeScript with React is very similar to writing JavaScript with React. The key difference when working with a component is that you can provide types for your component’s props. These types can be used for correctness checking and providing inline documentation in editors.

Taking the MyButton component from the Quick Start guide, we can add a type describing the title for the button:

These sandboxes can handle TypeScript code, but they do not run the type-checker. This means you can amend the TypeScript sandboxes to learn, but you won’t get any type errors or warnings. To get type-checking, you can use the TypeScript Playground or use a more fully-featured online sandbox.

This inline syntax is the simplest way to provide types for a component, though once you start to have a few fields to describe it can become unwieldy. Instead, you can use an interface or type to describe the component’s props:

The type describing your component’s props can be as simple or as complex as you need, though they should be an object type described with either a type or interface. You can learn about how TypeScript describes objects in Object Types but you may also be interested in using Union Types to describe a prop that can be one of a few different types and the Creating Types from Types guide for more advanced use cases.

The type definitions from @types/react include types for the built-in Hooks, so you can use them in your components without any additional setup. They are built to take into account the code you write in your component, so you will get inferred types a lot of the time and ideally do not need to handle the minutiae of providing the types.

However, we can look at a few examples of how to provide types for Hooks.

The useState Hook will re-use the value passed in as the initial state to determine what the type of the value should be. For example:

This will assign the type of boolean to enabled, and setEnabled will be a function accepting either a boolean argument, or a function that returns a boolean. If you want to explicitly provide a type for the state, you can do so by providing a type argument to the useState call:

This isn’t very useful in this case, but a common case where you may want to provide a type is when you have a union type. For example, status here can be one of a few different strings:

Or, as recommended in Principles for structuring state, you can group related state as an object and describe the different possibilities via object types:

The useReducer Hook is a more complex Hook that takes a reducer function and an initial state. The types for the reducer function are inferred from the initial state. You can optionally provide a type argument to the useReducer call to provide a type for the state, but it is often better to set the type on the initial state instead:

We are using TypeScript in a few key places:

A more explicit alternative to setting the type on initialState is to provide a type argument to useReducer:

The useContext Hook is a technique for passing data down the component tree without having to pass props through components. It is used by creating a provider component and often by creating a Hook to consume the value in a child component.

The type of the value provided by the context is inferred from the value passed to the createContext call:

This technique works when you have a default value which makes sense - but there are occasionally cases when you do not, and in those cases null can feel reasonable as a default value. However, to allow the type-system to understand your code, you need to explicitly set ContextShape | null on the createContext.

This causes the issue that you need to eliminate the | null in the type for context consumers. Our recommendation is to have the Hook do a runtime check for it’s existence and throw an error when not present:

React Compiler automatically memoizes values and functions, reducing the need for manual useMemo calls. You can use the compiler to handle memoization automatically.

The useMemo Hooks will create/re-access a memorized value from a function call, re-running the function only when dependencies passed as the 2nd parameter are changed. The result of calling the Hook is inferred from the return value from the function in the first parameter. You can be more explicit by providing a type argument to the Hook.

React Compiler automatically memoizes values and functions, reducing the need for manual useCallback calls. You can use the compiler to handle memoization automatically.

The useCallback provide a stable reference to a function as long as the dependencies passed into the second parameter are the same. Like useMemo, the function’s type is inferred from the return value of the function in the first parameter, and you can be more explicit by providing a type argument to the Hook.

When working in TypeScript strict mode useCallback requires adding types for the parameters in your callback. This is because the type of the callback is inferred from the return value of the function, and without parameters the type cannot be fully understood.

Depending on your code-style preferences, you could use the *EventHandler functions from the React types to provide the type for the event handler at the same time as defining the callback:

There is quite an expansive set of types which come from the @types/react package, it is worth a read when you feel comfortable with how React and TypeScript interact. You can find them in React’s folder in DefinitelyTyped. We will cover a few of the more common types here.

When working with DOM events in React, the type of the event can often be inferred from the event handler. However, when you want to extract a function to be passed to an event handler, you will need to explicitly set the type of the event.

There are many types of events provided in the React types - the full list can be found here which is based on the most popular events from the DOM.

When determining the type you are looking for you can first look at the hover information for the event handler you are using, which will show the type of the event.

If you need to use an event that is not included in this list, you can use the React.SyntheticEvent type, which is the base type for all events.

There are two common paths to describing the children of a component. The first is to use the React.ReactNode type, which is a union of all the possible types that can be passed as children in JSX:

This is a very broad definition of children. The second is to use the React.ReactElement type, which is only JSX elements and not JavaScript primitives like strings or numbers:

Note, that you cannot use TypeScript to describe that the children are a certain type of JSX elements, so you cannot use the type-system to describe a component which only accepts <li> children.

You can see an example of both React.ReactNode and React.ReactElement with the type-checker in this TypeScript playground.

When using inline styles in React, you can use React.CSSProperties to describe the object passed to the style prop. This type is a union of all the possible CSS properties, and is a good way to ensure you are passing valid CSS properties to the style prop, and to get auto-complete in your editor.

This guide has covered the basics of using TypeScript with React, but there is a lot more to learn. Individual API pages on the docs may contain more in-depth documentation on how to use them with TypeScript.

We recommend the following resources:

The TypeScript handbook is the official documentation for TypeScript, and covers most key language features.

The TypeScript release notes cover new features in depth.

React TypeScript Cheatsheet is a community-maintained cheatsheet for using TypeScript with React, covering a lot of useful edge cases and providing more breadth than this document.

TypeScript Community Discord is a great place to ask questions and get help with TypeScript and React issues.

**Examples:**

Example 1 (python):
```python
npm install --save-dev @types/react @types/react-dom
```

Example 2 (jsx):
```jsx
// Infer the type as "boolean"const [enabled, setEnabled] = useState(false);
```

Example 3 (tsx):
```tsx
// Explicitly set the type to "boolean"const [enabled, setEnabled] = useState<boolean>(false);
```

Example 4 (typescript):
```typescript
type Status = "idle" | "loading" | "success" | "error";const [status, setStatus] = useState<Status>("idle");
```

---

## Writing Markup with JSX

**URL:** https://react.dev/learn/writing-markup-with-jsx

**Contents:**
- Writing Markup with JSX
  - You will learn
- JSX: Putting markup into JavaScript
  - Note
- Converting HTML to JSX
  - Note
- The Rules of JSX
  - 1. Return a single root element
      - Deep Dive
    - Why do multiple JSX tags need to be wrapped?

JSX is a syntax extension for JavaScript that lets you write HTML-like markup inside a JavaScript file. Although there are other ways to write components, most React developers prefer the conciseness of JSX, and most codebases use it.

The Web has been built on HTML, CSS, and JavaScript. For many years, web developers kept content in HTML, design in CSS, and logic in JavaScript—often in separate files! Content was marked up inside HTML while the page’s logic lived separately in JavaScript:

But as the Web became more interactive, logic increasingly determined content. JavaScript was in charge of the HTML! This is why in React, rendering logic and markup live together in the same place—components.

Sidebar.js React component

Form.js React component

Keeping a button’s rendering logic and markup together ensures that they stay in sync with each other on every edit. Conversely, details that are unrelated, such as the button’s markup and a sidebar’s markup, are isolated from each other, making it safer to change either of them on their own.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information. The best way to understand this is to convert some HTML markup to JSX markup.

JSX and React are two separate things. They’re often used together, but you can use them independently of each other. JSX is a syntax extension, while React is a JavaScript library.

Suppose that you have some (perfectly valid) HTML:

And you want to put it into your component:

If you copy and paste it as is, it will not work:

This is because JSX is stricter and has a few more rules than HTML! If you read the error messages above, they’ll guide you to fix the markup, or you can follow the guide below.

Most of the time, React’s on-screen error messages will help you find where the problem is. Give them a read if you get stuck!

To return multiple elements from a component, wrap them with a single parent tag.

For example, you can use a <div>:

If you don’t want to add an extra <div> to your markup, you can write <> and </> instead:

This empty tag is called a Fragment. Fragments let you group things without leaving any trace in the browser HTML tree.

JSX looks like HTML, but under the hood it is transformed into plain JavaScript objects. You can’t return two objects from a function without wrapping them into an array. This explains why you also can’t return two JSX tags without wrapping them into another tag or a Fragment.

JSX requires tags to be explicitly closed: self-closing tags like <img> must become <img />, and wrapping tags like <li>oranges must be written as <li>oranges</li>.

This is how Hedy Lamarr’s image and list items look closed:

JSX turns into JavaScript and attributes written in JSX become keys of JavaScript objects. In your own components, you will often want to read those attributes into variables. But JavaScript has limitations on variable names. For example, their names can’t contain dashes or be reserved words like class.

This is why, in React, many HTML and SVG attributes are written in camelCase. For example, instead of stroke-width you use strokeWidth. Since class is a reserved word, in React you write className instead, named after the corresponding DOM property:

You can find all these attributes in the list of DOM component props. If you get one wrong, don’t worry—React will print a message with a possible correction to the browser console.

For historical reasons, aria-* and data-* attributes are written as in HTML with dashes.

Converting all these attributes in existing markup can be tedious! We recommend using a converter to translate your existing HTML and SVG to JSX. Converters are very useful in practice, but it’s still worth understanding what is going on so that you can comfortably write JSX on your own.

Here is your final result:

Now you know why JSX exists and how to use it in components:

This HTML was pasted into a component, but it’s not valid JSX. Fix it:

Whether to do it by hand or using the converter is up to you!

**Examples:**

Example 1 (jsx):
```jsx
<h1>Hedy Lamarr's Todos</h1><img   src="https://i.imgur.com/yXOvdOSs.jpg"   alt="Hedy Lamarr"   class="photo"><ul>    <li>Invent new traffic lights    <li>Rehearse a movie scene    <li>Improve the spectrum technology</ul>
```

Example 2 (javascript):
```javascript
export default function TodoList() {  return (    // ???  )}
```

Example 3 (jsx):
```jsx
<div>  <h1>Hedy Lamarr's Todos</h1>  <img     src="https://i.imgur.com/yXOvdOSs.jpg"     alt="Hedy Lamarr"     class="photo"  >  <ul>    ...  </ul></div>
```

Example 4 (jsx):
```jsx
<>  <h1>Hedy Lamarr's Todos</h1>  <img     src="https://i.imgur.com/yXOvdOSs.jpg"     alt="Hedy Lamarr"     class="photo"  >  <ul>    ...  </ul></>
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written like HTML, but it is actually JavaScript under the hood! This syntax is called JSX, and it lets you embed markup inside JavaScript.

Return statements can be written all on one line, as in this component:

But if your markup isn’t all on the same line as the return keyword, you must wrap it in a pair of parentheses:

Without parentheses, any code on the lines after return will be ignored!

Now that you’ve defined your Profile component, you can nest it inside other components. For example, you can export a Gallery component that uses multiple Profile components:

Notice the difference in casing:

And Profile contains even more HTML: <img />. In the end, this is what the browser sees:

Components are regular JavaScript functions, so you can keep multiple components in the same file. This is convenient when components are relatively small or tightly related to each other. If this file gets crowded, you can always move Profile to a separate file. You will learn how to do this shortly on the page about imports.

Because the Profile components are rendered inside Gallery—even several times!—we can say that Gallery is a parent component, rendering each Profile as a “child”. This is part of the magic of React: you can define a component once, and then use it in as many places and as many times as you like.

Components can render other components, but you must never nest their definitions:

The snippet above is very slow and causes bugs. Instead, define every component at the top level:

When a child component needs some data from a parent, pass it by props instead of nesting definitions.

Your React application begins at a “root” component. Usually, it is created automatically when you start a new project. For example, if you use CodeSandbox or if you use the framework Next.js, the root component is defined in pages/index.js. In these examples, you’ve been exporting root components.

Most React apps use components all the way down. This means that you won’t only use components for reusable pieces like buttons, but also for larger pieces like sidebars, lists, and ultimately, complete pages! Components are a handy way to organize UI code and markup, even if some of them are only used once.

React-based frameworks take this a step further. Instead of using an empty HTML file and letting React “take over” managing the page with JavaScript, they also generate the HTML automatically from your React components. This allows your app to show some content before the JavaScript code loads.

Still, many websites only use React to add interactivity to existing HTML pages. They have many root components instead of a single one for the entire page. You can use as much—or as little—React as you need.

You’ve just gotten your first taste of React! Let’s recap some key points.

React lets you create components, reusable UI elements for your app.

In a React app, every piece of UI is a component.

React components are regular JavaScript functions except:

This sandbox doesn’t work because the root component is not exported:

Try to fix it yourself before looking at the solution!

**Examples:**

Example 1 (julia):
```julia
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (jsx):
```jsx
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (jsx):
```jsx
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (jsx):
```jsx
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## You Might Not Need an Effect

**URL:** https://react.dev/learn/you-might-not-need-an-effect

**Contents:**
- You Might Not Need an Effect
  - You will learn
- How to remove unnecessary Effects
  - Updating state based on props or state
  - Caching expensive calculations
  - Note
      - Deep Dive
    - How to tell if a calculation is expensive?
  - Resetting all state when a prop changes
  - Adjusting some state when a prop changes

Effects are an escape hatch from the React paradigm. They let you “step outside” of React and synchronize your components with some external system like a non-React widget, network, or the browser DOM. If there is no external system involved (for example, if you want to update a component’s state when some props or state change), you shouldn’t need an Effect. Removing unnecessary Effects will make your code easier to follow, faster to run, and less error-prone.

There are two common cases in which you don’t need Effects:

You do need Effects to synchronize with external systems. For example, you can write an Effect that keeps a jQuery widget synchronized with the React state. You can also fetch data with Effects: for example, you can synchronize the search results with the current search query. Keep in mind that modern frameworks provide more efficient built-in data fetching mechanisms than writing Effects directly in your components.

To help you gain the right intuition, let’s look at some common concrete examples!

Suppose you have a component with two state variables: firstName and lastName. You want to calculate a fullName from them by concatenating them. Moreover, you’d like fullName to update whenever firstName or lastName change. Your first instinct might be to add a fullName state variable and update it in an Effect:

This is more complicated than necessary. It is inefficient too: it does an entire render pass with a stale value for fullName, then immediately re-renders with the updated value. Remove the state variable and the Effect:

When something can be calculated from the existing props or state, don’t put it in state. Instead, calculate it during rendering. This makes your code faster (you avoid the extra “cascading” updates), simpler (you remove some code), and less error-prone (you avoid bugs caused by different state variables getting out of sync with each other). If this approach feels new to you, Thinking in React explains what should go into state.

This component computes visibleTodos by taking the todos it receives by props and filtering them according to the filter prop. You might feel tempted to store the result in state and update it from an Effect:

Like in the earlier example, this is both unnecessary and inefficient. First, remove the state and the Effect:

Usually, this code is fine! But maybe getFilteredTodos() is slow or you have a lot of todos. In that case you don’t want to recalculate getFilteredTodos() if some unrelated state variable like newTodo has changed.

You can cache (or “memoize”) an expensive calculation by wrapping it in a useMemo Hook:

React Compiler can automatically memoize expensive calculations for you, eliminating the need for manual useMemo in many cases.

Or, written as a single line:

This tells React that you don’t want the inner function to re-run unless either todos or filter have changed. React will remember the return value of getFilteredTodos() during the initial render. During the next renders, it will check if todos or filter are different. If they’re the same as last time, useMemo will return the last result it has stored. But if they are different, React will call the inner function again (and store its result).

The function you wrap in useMemo runs during rendering, so this only works for pure calculations.

In general, unless you’re creating or looping over thousands of objects, it’s probably not expensive. If you want to get more confidence, you can add a console log to measure the time spent in a piece of code:

Perform the interaction you’re measuring (for example, typing into the input). You will then see logs like filter array: 0.15ms in your console. If the overall logged time adds up to a significant amount (say, 1ms or more), it might make sense to memoize that calculation. As an experiment, you can then wrap the calculation in useMemo to verify whether the total logged time has decreased for that interaction or not:

useMemo won’t make the first render faster. It only helps you skip unnecessary work on updates.

Keep in mind that your machine is probably faster than your users’ so it’s a good idea to test the performance with an artificial slowdown. For example, Chrome offers a CPU Throttling option for this.

Also note that measuring performance in development will not give you the most accurate results. (For example, when Strict Mode is on, you will see each component render twice rather than once.) To get the most accurate timings, build your app for production and test it on a device like your users have.

This ProfilePage component receives a userId prop. The page contains a comment input, and you use a comment state variable to hold its value. One day, you notice a problem: when you navigate from one profile to another, the comment state does not get reset. As a result, it’s easy to accidentally post a comment on a wrong user’s profile. To fix the issue, you want to clear out the comment state variable whenever the userId changes:

This is inefficient because ProfilePage and its children will first render with the stale value, and then render again. It is also complicated because you’d need to do this in every component that has some state inside ProfilePage. For example, if the comment UI is nested, you’d want to clear out nested comment state too.

Instead, you can tell React that each user’s profile is conceptually a different profile by giving it an explicit key. Split your component in two and pass a key attribute from the outer component to the inner one:

Normally, React preserves the state when the same component is rendered in the same spot. By passing userId as a key to the Profile component, you’re asking React to treat two Profile components with different userId as two different components that should not share any state. Whenever the key (which you’ve set to userId) changes, React will recreate the DOM and reset the state of the Profile component and all of its children. Now the comment field will clear out automatically when navigating between profiles.

Note that in this example, only the outer ProfilePage component is exported and visible to other files in the project. Components rendering ProfilePage don’t need to pass the key to it: they pass userId as a regular prop. The fact ProfilePage passes it as a key to the inner Profile component is an implementation detail.

Sometimes, you might want to reset or adjust a part of the state on a prop change, but not all of it.

This List component receives a list of items as a prop, and maintains the selected item in the selection state variable. You want to reset the selection to null whenever the items prop receives a different array:

This, too, is not ideal. Every time the items change, the List and its child components will render with a stale selection value at first. Then React will update the DOM and run the Effects. Finally, the setSelection(null) call will cause another re-render of the List and its child components, restarting this whole process again.

Start by deleting the Effect. Instead, adjust the state directly during rendering:

Storing information from previous renders like this can be hard to understand, but it’s better than updating the same state in an Effect. In the above example, setSelection is called directly during a render. React will re-render the List immediately after it exits with a return statement. React has not rendered the List children or updated the DOM yet, so this lets the List children skip rendering the stale selection value.

When you update a component during rendering, React throws away the returned JSX and immediately retries rendering. To avoid very slow cascading retries, React only lets you update the same component’s state during a render. If you update another component’s state during a render, you’ll see an error. A condition like items !== prevItems is necessary to avoid loops. You may adjust state like this, but any other side effects (like changing the DOM or setting timeouts) should stay in event handlers or Effects to keep components pure.

Although this pattern is more efficient than an Effect, most components shouldn’t need it either. No matter how you do it, adjusting state based on props or other state makes your data flow more difficult to understand and debug. Always check whether you can reset all state with a key or calculate everything during rendering instead. For example, instead of storing (and resetting) the selected item, you can store the selected item ID:

Now there is no need to “adjust” the state at all. If the item with the selected ID is in the list, it remains selected. If it’s not, the selection calculated during rendering will be null because no matching item was found. This behavior is different, but arguably better because most changes to items preserve the selection.

Let’s say you have a product page with two buttons (Buy and Checkout) that both let you buy that product. You want to show a notification whenever the user puts the product in the cart. Calling showNotification() in both buttons’ click handlers feels repetitive so you might be tempted to place this logic in an Effect:

This Effect is unnecessary. It will also most likely cause bugs. For example, let’s say that your app “remembers” the shopping cart between the page reloads. If you add a product to the cart once and refresh the page, the notification will appear again. It will keep appearing every time you refresh that product’s page. This is because product.isInCart will already be true on the page load, so the Effect above will call showNotification().

When you’re not sure whether some code should be in an Effect or in an event handler, ask yourself why this code needs to run. Use Effects only for code that should run because the component was displayed to the user. In this example, the notification should appear because the user pressed the button, not because the page was displayed! Delete the Effect and put the shared logic into a function called from both event handlers:

This both removes the unnecessary Effect and fixes the bug.

This Form component sends two kinds of POST requests. It sends an analytics event when it mounts. When you fill in the form and click the Submit button, it will send a POST request to the /api/register endpoint:

Let’s apply the same criteria as in the example before.

The analytics POST request should remain in an Effect. This is because the reason to send the analytics event is that the form was displayed. (It would fire twice in development, but see here for how to deal with that.)

However, the /api/register POST request is not caused by the form being displayed. You only want to send the request at one specific moment in time: when the user presses the button. It should only ever happen on that particular interaction. Delete the second Effect and move that POST request into the event handler:

When you choose whether to put some logic into an event handler or an Effect, the main question you need to answer is what kind of logic it is from the user’s perspective. If this logic is caused by a particular interaction, keep it in the event handler. If it’s caused by the user seeing the component on the screen, keep it in the Effect.

Sometimes you might feel tempted to chain Effects that each adjust a piece of state based on other state:

There are two problems with this code.

The first problem is that it is very inefficient: the component (and its children) have to re-render between each set call in the chain. In the example above, in the worst case (setCard → render → setGoldCardCount → render → setRound → render → setIsGameOver → render) there are three unnecessary re-renders of the tree below.

The second problem is that even if it weren’t slow, as your code evolves, you will run into cases where the “chain” you wrote doesn’t fit the new requirements. Imagine you are adding a way to step through the history of the game moves. You’d do it by updating each state variable to a value from the past. However, setting the card state to a value from the past would trigger the Effect chain again and change the data you’re showing. Such code is often rigid and fragile.

In this case, it’s better to calculate what you can during rendering, and adjust the state in the event handler:

This is a lot more efficient. Also, if you implement a way to view game history, now you will be able to set each state variable to a move from the past without triggering the Effect chain that adjusts every other value. If you need to reuse logic between several event handlers, you can extract a function and call it from those handlers.

Remember that inside event handlers, state behaves like a snapshot. For example, even after you call setRound(round + 1), the round variable will reflect the value at the time the user clicked the button. If you need to use the next value for calculations, define it manually like const nextRound = round + 1.

In some cases, you can’t calculate the next state directly in the event handler. For example, imagine a form with multiple dropdowns where the options of the next dropdown depend on the selected value of the previous dropdown. Then, a chain of Effects is appropriate because you are synchronizing with network.

Some logic should only run once when the app loads.

You might be tempted to place it in an Effect in the top-level component:

However, you’ll quickly discover that it runs twice in development. This can cause issues—for example, maybe it invalidates the authentication token because the function wasn’t designed to be called twice. In general, your components should be resilient to being remounted. This includes your top-level App component.

Although it may not ever get remounted in practice in production, following the same constraints in all components makes it easier to move and reuse code. If some logic must run once per app load rather than once per component mount, add a top-level variable to track whether it has already executed:

You can also run it during module initialization and before the app renders:

Code at the top level runs once when your component is imported—even if it doesn’t end up being rendered. To avoid slowdown or surprising behavior when importing arbitrary components, don’t overuse this pattern. Keep app-wide initialization logic to root component modules like App.js or in your application’s entry point.

Let’s say you’re writing a Toggle component with an internal isOn state which can be either true or false. There are a few different ways to toggle it (by clicking or dragging). You want to notify the parent component whenever the Toggle internal state changes, so you expose an onChange event and call it from an Effect:

Like earlier, this is not ideal. The Toggle updates its state first, and React updates the screen. Then React runs the Effect, which calls the onChange function passed from a parent component. Now the parent component will update its own state, starting another render pass. It would be better to do everything in a single pass.

Delete the Effect and instead update the state of both components within the same event handler:

With this approach, both the Toggle component and its parent component update their state during the event. React batches updates from different components together, so there will only be one render pass.

You might also be able to remove the state altogether, and instead receive isOn from the parent component:

“Lifting state up” lets the parent component fully control the Toggle by toggling the parent’s own state. This means the parent component will have to contain more logic, but there will be less state overall to worry about. Whenever you try to keep two different state variables synchronized, try lifting state up instead!

This Child component fetches some data and then passes it to the Parent component in an Effect:

In React, data flows from the parent components to their children. When you see something wrong on the screen, you can trace where the information comes from by going up the component chain until you find which component passes the wrong prop or has the wrong state. When child components update the state of their parent components in Effects, the data flow becomes very difficult to trace. Since both the child and the parent need the same data, let the parent component fetch that data, and pass it down to the child instead:

This is simpler and keeps the data flow predictable: the data flows down from the parent to the child.

Sometimes, your components may need to subscribe to some data outside of the React state. This data could be from a third-party library or a built-in browser API. Since this data can change without React’s knowledge, you need to manually subscribe your components to it. This is often done with an Effect, for example:

Here, the component subscribes to an external data store (in this case, the browser navigator.onLine API). Since this API does not exist on the server (so it can’t be used for the initial HTML), initially the state is set to true. Whenever the value of that data store changes in the browser, the component updates its state.

Although it’s common to use Effects for this, React has a purpose-built Hook for subscribing to an external store that is preferred instead. Delete the Effect and replace it with a call to useSyncExternalStore:

This approach is less error-prone than manually syncing mutable data to React state with an Effect. Typically, you’ll write a custom Hook like useOnlineStatus() above so that you don’t need to repeat this code in the individual components. Read more about subscribing to external stores from React components.

Many apps use Effects to kick off data fetching. It is quite common to write a data fetching Effect like this:

You don’t need to move this fetch to an event handler.

This might seem like a contradiction with the earlier examples where you needed to put the logic into the event handlers! However, consider that it’s not the typing event that’s the main reason to fetch. Search inputs are often prepopulated from the URL, and the user might navigate Back and Forward without touching the input.

It doesn’t matter where page and query come from. While this component is visible, you want to keep results synchronized with data from the network for the current page and query. This is why it’s an Effect.

However, the code above has a bug. Imagine you type "hello" fast. Then the query will change from "h", to "he", "hel", "hell", and "hello". This will kick off separate fetches, but there is no guarantee about which order the responses will arrive in. For example, the "hell" response may arrive after the "hello" response. Since it will call setResults() last, you will be displaying the wrong search results. This is called a “race condition”: two different requests “raced” against each other and came in a different order than you expected.

To fix the race condition, you need to add a cleanup function to ignore stale responses:

This ensures that when your Effect fetches data, all responses except the last requested one will be ignored.

Handling race conditions is not the only difficulty with implementing data fetching. You might also want to think about caching responses (so that the user can click Back and see the previous screen instantly), how to fetch data on the server (so that the initial server-rendered HTML contains the fetched content instead of a spinner), and how to avoid network waterfalls (so that a child can fetch data without waiting for every parent).

These issues apply to any UI library, not just React. Solving them is not trivial, which is why modern frameworks provide more efficient built-in data fetching mechanisms than fetching data in Effects.

If you don’t use a framework (and don’t want to build your own) but would like to make data fetching from Effects more ergonomic, consider extracting your fetching logic into a custom Hook like in this example:

You’ll likely also want to add some logic for error handling and to track whether the content is loading. You can build a Hook like this yourself or use one of the many solutions already available in the React ecosystem. Although this alone won’t be as efficient as using a framework’s built-in data fetching mechanism, moving the data fetching logic into a custom Hook will make it easier to adopt an efficient data fetching strategy later.

In general, whenever you have to resort to writing Effects, keep an eye out for when you can extract a piece of functionality into a custom Hook with a more declarative and purpose-built API like useData above. The fewer raw useEffect calls you have in your components, the easier you will find to maintain your application.

The TodoList below displays a list of todos. When the “Show only active todos” checkbox is ticked, completed todos are not displayed in the list. Regardless of which todos are visible, the footer displays the count of todos that are not yet completed.

Simplify this component by removing all the unnecessary state and Effects.

**Examples:**

Example 1 (jsx):
```jsx
function Form() {  const [firstName, setFirstName] = useState('Taylor');  const [lastName, setLastName] = useState('Swift');  // 🔴 Avoid: redundant state and unnecessary Effect  const [fullName, setFullName] = useState('');  useEffect(() => {    setFullName(firstName + ' ' + lastName);  }, [firstName, lastName]);  // ...}
```

Example 2 (javascript):
```javascript
function Form() {  const [firstName, setFirstName] = useState('Taylor');  const [lastName, setLastName] = useState('Swift');  // ✅ Good: calculated during rendering  const fullName = firstName + ' ' + lastName;  // ...}
```

Example 3 (jsx):
```jsx
function TodoList({ todos, filter }) {  const [newTodo, setNewTodo] = useState('');  // 🔴 Avoid: redundant state and unnecessary Effect  const [visibleTodos, setVisibleTodos] = useState([]);  useEffect(() => {    setVisibleTodos(getFilteredTodos(todos, filter));  }, [todos, filter]);  // ...}
```

Example 4 (javascript):
```javascript
function TodoList({ todos, filter }) {  const [newTodo, setNewTodo] = useState('');  // ✅ This is fine if getFilteredTodos() is not slow.  const visibleTodos = getFilteredTodos(todos, filter);  // ...}
```

---
