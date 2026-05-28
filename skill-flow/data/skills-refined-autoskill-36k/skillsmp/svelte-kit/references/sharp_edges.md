# Svelte Kit - Sharp Edges

## Ssr Browser Apis

### **Id**
ssr-browser-apis
### **Summary**
Browser APIs crash during server-side rendering
### **Severity**
critical
### **Situation**
  You use localStorage, window, document, or other browser APIs
  directly in your component. It works in dev, then crashes in
  production during SSR.
  
### **Why**
  SvelteKit renders pages on the server first. The server doesn't
  have browser APIs. When your component tries to access window,
  it throws "window is not defined."
  
### **Solution**
  # CHECK FOR BROWSER ENVIRONMENT
  
  // Option 1: browser check
  import { browser } from '$app/environment';
  
  let theme = $state('light');
  
  $effect(() => {
    if (browser) {
      theme = localStorage.getItem('theme') ?? 'light';
    }
  });
  
  // Option 2: onMount (only runs in browser)
  import { onMount } from 'svelte';
  
  let windowWidth = $state(0);
  
  onMount(() => {
    windowWidth = window.innerWidth;
  
    const handleResize = () => {
      windowWidth = window.innerWidth;
    };
  
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  });
  
  // Option 3: Dynamic import for browser-only libraries
  onMount(async () => {
    const { Chart } = await import('chart.js');
    new Chart(canvas, config);
  });
  
### **Symptoms**
  - "window is not defined" error
  - "document is not defined" error
  - Works in dev, crashes in production
### **Detection Pattern**
(?<!browser\s*&&\s*)(?<!if\s*\(browser\)\s*)(window\.|document\.|localStorage)

## Reactive Statement Order

### **Id**
reactive-statement-order
### **Summary**
Reactive statements run in declaration order, not dependency order
### **Severity**
medium
### **Situation**
  In Svelte 4, you have multiple $: statements that depend on each
  other. You expect them to run in dependency order, but they run
  in declaration order.
  
### **Why**
  Svelte 4's $: statements run top-to-bottom in the order they appear
  in your script. If A depends on B but A is declared first, A will
  see the old value of B on the first run.
  
### **Solution**
  # ORDER REACTIVE STATEMENTS BY DEPENDENCY
  
  // WRONG: Order matters!
  $: doubled = count * 2;
  $: count = input.length;  // doubled uses stale count!
  
  // RIGHT: Dependencies first
  $: count = input.length;
  $: doubled = count * 2;
  
  // BETTER: Svelte 5 runes (no ordering issues)
  let input = $state('');
  let count = $derived(input.length);
  let doubled = $derived(count * 2);
  
  // Svelte 5 tracks dependencies automatically
  
### **Symptoms**
  - Values are one update behind
  - Stale data in derived values
  - Works after second interaction
### **Detection Pattern**


## Store Subscribe Leak

### **Id**
store-subscribe-leak
### **Summary**
Manual store subscriptions not unsubscribed cause memory leaks
### **Severity**
medium
### **Situation**
  You manually subscribe to a store with .subscribe() instead of
  using the $ prefix. You forget to unsubscribe in onDestroy.
  Subscriptions accumulate as components mount and unmount.
  
### **Why**
  The $ prefix auto-subscribes and auto-unsubscribes. Manual
  .subscribe() returns an unsubscribe function you must call.
  Forgetting to call it means the callback keeps running even
  after the component is destroyed.
  
### **Solution**
  # PREFER AUTO-SUBSCRIPTION
  
  // WRONG: Manual subscription without cleanup
  import { user } from '$lib/stores';
  
  let name;
  user.subscribe(u => {
    name = u.name;  // This keeps running forever!
  });
  
  // RIGHT: Auto-subscription with $ prefix
  import { user } from '$lib/stores';
  
  <p>{$user.name}</p>
  
  // If you must use manual subscription, clean up
  import { onDestroy } from 'svelte';
  
  const unsubscribe = user.subscribe(u => {
    name = u.name;
  });
  
  onDestroy(unsubscribe);
  
  // In Svelte 5 with runes, stores work differently
  import { user } from '$lib/stores';
  import { get } from 'svelte/store';
  
  // One-time read
  const currentUser = get(user);
  
  // For reactive, use $effect with store value
  
### **Symptoms**
  - Memory usage grows over time
  - Old callbacks still execute
  - Console logs from destroyed components
### **Detection Pattern**
\.subscribe\s*\([^)]+\)(?![\s\S]*onDestroy)

## Missing Key In Each

### **Id**
missing-key-in-each
### **Summary**
Missing key in
### **Severity**
medium
### **Situation**
  You use #each without a key. Items have state (inputs, animations).
  You reorder or filter the list, and state sticks to wrong items.
  
### **Why**
  Without a key, Svelte updates list items by index. If you remove
  item 0, item 1 becomes the new item 0 and inherits item 0's DOM
  state. With a key, Svelte tracks items and updates correctly.
  
### **Solution**
  # ALWAYS USE KEYS FOR STATEFUL LISTS
  
  // WRONG: No key
  {#each items as item}
    <li><input bind:value={item.text} /></li>
  {/each}
  
  // RIGHT: Key by unique ID
  {#each items as item (item.id)}
    <li><input bind:value={item.text} /></li>
  {/each}
  
  // Index is usually wrong (same problem as no key)
  // WRONG:
  {#each items as item, i (i)}
  
  // Use stable unique identifier
  {#each items as item (item.id)}
  {#each items as item (item.uuid)}
  {#each items as item (item.email)}
  
### **Symptoms**
  - Input values appear on wrong items
  - Animations replay incorrectly
  - State "sticks" during reordering
### **Detection Pattern**
\{#each\s+\w+\s+as\s+\w+\s*\}(?!\s*\([^)]+\))

## Load Vs Server Load

### **Id**
load-vs-server-load
### **Summary**
Confusing +page.ts (universal) vs +page.server.ts (server-only)
### **Severity**
medium
### **Situation**
  You put sensitive code in +page.ts thinking it's server-only.
  But +page.ts runs on both server and client. Your API keys or
  database queries are exposed.
  
### **Why**
  +page.ts (universal load) runs on server during SSR and on client
  during navigation. +page.server.ts ONLY runs on server. Sensitive
  operations must go in .server.ts files.
  
### **Solution**
  # KNOW YOUR LOAD FUNCTION TYPE
  
  // +page.ts - runs on BOTH server and client
  // Use for: public API calls, data transformations
  export const load: PageLoad = async ({ fetch }) => {
    // This fetch runs on server AND client
    const res = await fetch('/api/public-data');
    return { data: await res.json() };
  };
  
  // +page.server.ts - runs ONLY on server
  // Use for: database queries, secrets, auth checks
  export const load: PageServerLoad = async ({ locals }) => {
    // Safe to use database directly
    const users = await db.user.findMany();
  
    // Safe to access secrets
    const apiKey = process.env.SECRET_API_KEY;
  
    return { users };
  };
  
  // Common mistake: sensitive data in +page.ts
  // WRONG:
  // +page.ts
  const data = await prisma.user.findMany();  // DB in universal!
  
  // RIGHT:
  // +page.server.ts
  const data = await prisma.user.findMany();  // DB in server-only
  
### **Symptoms**
  - Database credentials in client bundle
  - API keys exposed in network tab
  - Prisma/database imports in client code
### **Detection Pattern**


## Form Action Redirect

### **Id**
form-action-redirect
### **Summary**
Using return instead of throw for redirects in form actions
### **Severity**
medium
### **Situation**
  You return a redirect from a form action. The form submission
  "succeeds" but the page doesn't redirect. The action data shows
  the redirect info as form data.
  
### **Why**
  In SvelteKit, redirects must be thrown, not returned. The throw
  statement stops execution and triggers the redirect. A return
  just sends data back to the form.
  
### **Solution**
  # THROW REDIRECTS AND ERRORS
  
  // WRONG: Returning redirect
  export const actions = {
    default: async () => {
      // ... do stuff
      return redirect(303, '/success');  // Won't work!
    }
  };
  
  // RIGHT: Throw redirect
  import { redirect } from '@sveltejs/kit';
  
  export const actions = {
    default: async () => {
      // ... do stuff
      throw redirect(303, '/success');  // Works!
    }
  };
  
  // Same for errors
  // WRONG:
  return error(404, 'Not found');
  
  // RIGHT:
  throw error(404, 'Not found');
  
  // fail() is the exception - it IS returned
  import { fail } from '@sveltejs/kit';
  
  export const actions = {
    default: async ({ request }) => {
      const data = await request.formData();
      if (!data.get('email')) {
        return fail(400, { error: 'Email required' });  // Correct!
      }
    }
  };
  
### **Symptoms**
  - Redirect object appears as form data
  - Page doesn't redirect after form submit
  - Form shows weird object
### **Detection Pattern**
return\s+redirect\s*\(

## Binding Without Value

### **Id**
binding-without-value
### **Summary**
Using bind:value on elements that need explicit value
### **Severity**
low
### **Situation**
  You use bind:value on a select or radio button but forget to set
  initial value. The binding is undefined and doesn't match any option.
  
### **Why**
  Two-way binding syncs the variable with the element. If the initial
  value doesn't match any option, the element shows the first option
  but the variable stays undefined/initial.
  
### **Solution**
  # INITIALIZE BOUND VALUES
  
  // WRONG: No initial value
  let selected;  // undefined
  
  <select bind:value={selected}>
    <option value="a">A</option>
    <option value="b">B</option>
  </select>
  
  // RIGHT: Initialize to valid option
  let selected = $state('a');
  
  <select bind:value={selected}>
    <option value="a">A</option>
    <option value="b">B</option>
  </select>
  
  // Or use placeholder option
  let selected = $state('');
  
  <select bind:value={selected}>
    <option value="" disabled>Select one</option>
    <option value="a">A</option>
    <option value="b">B</option>
  </select>
  
### **Symptoms**
  - Select shows option but variable is undefined
  - Form submits wrong value
  - Validation thinks field is empty
### **Detection Pattern**


## Await Block Error Handling

### **Id**
await-block-error-handling
### **Summary**

### **Severity**
medium
### **Situation**
  You use an #await block without the :catch clause. The promise
  rejects, and the user sees nothing - the loading state or an
  empty component.
  
### **Why**
  #await blocks silently swallow errors if you don't handle them.
  Unlike try/catch which throws visibly, unhandled #await rejections
  just leave the component in a broken state.
  
### **Solution**
  # ALWAYS HANDLE AWAIT ERRORS
  
  // WRONG: No error handling
  {#await fetchData()}
    <p>Loading...</p>
  {:then data}
    <p>{data}</p>
  {/await}
  
  // RIGHT: Handle errors
  {#await fetchData()}
    <p>Loading...</p>
  {:then data}
    <p>{data}</p>
  {:catch error}
    <p class="error">Failed to load: {error.message}</p>
  {/await}
  
  // For complex error handling, use state
  let data = $state(null);
  let error = $state(null);
  let loading = $state(true);
  
  $effect(() => {
    fetchData()
      .then(d => { data = d; })
      .catch(e => { error = e; })
      .finally(() => { loading = false; });
  });
  
### **Symptoms**
  - Loading spinner never goes away
  - Component appears empty on error
  - No error message for user
### **Detection Pattern**
\{#await[^}]+\}[\s\S]*?\{:then[^}]*\}[\s\S]*?\{/await\}(?!\s*\{:catch)