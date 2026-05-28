# Svelte & SvelteKit

## Patterns


---
  #### **Name**
Svelte 5 Runes
  #### **Description**
Fine-grained reactivity with $state, $derived, $effect
  #### **When**
Svelte 5 components
  #### **Example**
    # SVELTE 5 RUNES:
    
    """
    Runes are Svelte 5's new reactivity primitives.
    More explicit than Svelte 4's compiler magic,
    but more powerful and composable.
    """
    
    <script>
      // $state - reactive state
      let count = $state(0);
      let user = $state({ name: 'John', age: 30 });
    
      // $derived - computed values (replaces $:)
      let doubled = $derived(count * 2);
      let isAdult = $derived(user.age >= 18);
    
      // $effect - side effects (replaces $: with side effects)
      $effect(() => {
        console.log(`Count is now ${count}`);
        // Cleanup function (optional)
        return () => console.log('Cleaning up');
      });
    
      // $props - component props
      let { name, onUpdate } = $props();
    
      // $bindable - two-way bindable props
      let { value = $bindable() } = $props();
    
      function increment() {
        count++;  // Direct mutation works!
      }
    
      function updateName(newName) {
        user.name = newName;  // Deep reactivity
      }
    </script>
    
    <button onclick={increment}>
      Count: {count} (doubled: {doubled})
    </button>
    
    <input bind:value={user.name} />
    
    <!-- Runes work in .svelte.js files too -->
    // counter.svelte.js
    export function createCounter(initial = 0) {
      let count = $state(initial);
      let doubled = $derived(count * 2);
    
      return {
        get count() { return count; },
        get doubled() { return doubled; },
        increment: () => count++,
        decrement: () => count--
      };
    }
    

---
  #### **Name**
SvelteKit Load Functions
  #### **Description**
Server-side data loading
  #### **When**
Fetching data for pages
  #### **Example**
    # LOAD FUNCTIONS:
    
    """
    Load functions run on the server (or during prerendering).
    They fetch data before the page renders.
    """
    
    // +page.server.ts - runs ONLY on server
    import type { PageServerLoad } from './$types';
    import { db } from '$lib/db';
    
    export const load: PageServerLoad = async ({ params, locals }) => {
      const user = await db.user.findUnique({
        where: { id: params.id }
      });
    
      if (!user) {
        throw error(404, 'User not found');
      }
    
      return {
        user,
        // Sensitive data is safe here - server only
        secretData: user.privateInfo
      };
    };
    
    // +page.ts - runs on server AND client
    import type { PageLoad } from './$types';
    
    export const load: PageLoad = async ({ fetch, params }) => {
      // Use SvelteKit's fetch for proper credentials
      const res = await fetch(`/api/users/${params.id}`);
      const user = await res.json();
      return { user };
    };
    
    // +page.svelte - receives load data
    <script>
      let { data } = $props();
    </script>
    
    <h1>Hello, {data.user.name}!</h1>
    
    // +layout.server.ts - shared data for nested routes
    export const load: LayoutServerLoad = async ({ locals }) => {
      return {
        user: locals.user  // From hooks.server.ts
      };
    };
    

---
  #### **Name**
Form Actions
  #### **Description**
Progressive enhancement for forms
  #### **When**
Form submissions with server-side handling
  #### **Example**
    # FORM ACTIONS:
    
    """
    Form actions handle submissions on the server.
    Forms work without JavaScript (progressive enhancement).
    """
    
    // +page.server.ts
    import type { Actions } from './$types';
    import { fail, redirect } from '@sveltejs/kit';
    import { db } from '$lib/db';
    
    export const actions: Actions = {
      // Default action
      default: async ({ request }) => {
        const data = await request.formData();
        const email = data.get('email');
        const password = data.get('password');
    
        // Validation
        if (!email || !password) {
          return fail(400, {
            error: 'Email and password required',
            email  // Return for form repopulation
          });
        }
    
        // Create user
        try {
          await db.user.create({ data: { email, password } });
        } catch (e) {
          return fail(400, { error: 'Email already exists', email });
        }
    
        throw redirect(303, '/login');
      },
    
      // Named actions
      login: async ({ request, cookies }) => {
        const data = await request.formData();
        // ... login logic
        cookies.set('session', token, { path: '/' });
        throw redirect(303, '/dashboard');
      },
    
      logout: async ({ cookies }) => {
        cookies.delete('session', { path: '/' });
        throw redirect(303, '/');
      }
    };
    
    // +page.svelte
    <script>
      import { enhance } from '$app/forms';
    
      let { form } = $props();  // Action return data
    </script>
    
    <!-- Default action -->
    <form method="POST" use:enhance>
      <input name="email" value={form?.email ?? ''} />
      <input name="password" type="password" />
      {#if form?.error}
        <p class="error">{form.error}</p>
      {/if}
      <button>Sign Up</button>
    </form>
    
    <!-- Named action -->
    <form method="POST" action="?/logout" use:enhance>
      <button>Log Out</button>
    </form>
    

---
  #### **Name**
Svelte Stores
  #### **Description**
Shared reactive state (Svelte 4 pattern)
  #### **When**
State shared across components
  #### **Example**
    # SVELTE STORES:
    
    """
    Stores are reactive state containers.
    Still useful in Svelte 5 for cross-component state.
    """
    
    // stores/cart.ts
    import { writable, derived } from 'svelte/store';
    
    export const cart = writable<CartItem[]>([]);
    
    // Derived store
    export const cartTotal = derived(cart, $cart =>
      $cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
    );
    
    export const cartCount = derived(cart, $cart =>
      $cart.reduce((sum, item) => sum + item.quantity, 0)
    );
    
    // Custom store with methods
    function createCart() {
      const { subscribe, set, update } = writable<CartItem[]>([]);
    
      return {
        subscribe,
        addItem: (item: CartItem) => update(items => [...items, item]),
        removeItem: (id: string) => update(items =>
          items.filter(i => i.id !== id)
        ),
        clear: () => set([])
      };
    }
    
    export const cart = createCart();
    
    // Usage in component
    <script>
      import { cart, cartTotal } from '$lib/stores/cart';
    </script>
    
    <!-- Auto-subscribe with $ prefix -->
    <p>Items: {$cart.length}</p>
    <p>Total: ${$cartTotal}</p>
    
    <button onclick={() => cart.addItem(newItem)}>
      Add to Cart
    </button>
    

---
  #### **Name**
Transitions and Animations
  #### **Description**
Built-in animation primitives
  #### **When**
Adding motion to UI
  #### **Example**
    # TRANSITIONS:
    
    """
    Svelte has built-in transitions that animate
    elements entering and leaving the DOM.
    """
    
    <script>
      import { fade, fly, slide, scale } from 'svelte/transition';
      import { flip } from 'svelte/animate';
      import { cubicOut } from 'svelte/easing';
    
      let visible = $state(true);
      let items = $state([1, 2, 3, 4, 5]);
    </script>
    
    <!-- Simple transition -->
    {#if visible}
      <div transition:fade>Fades in and out</div>
    {/if}
    
    <!-- Transition with parameters -->
    {#if visible}
      <div transition:fly={{ y: 200, duration: 500, easing: cubicOut }}>
        Flies in from below
      </div>
    {/if}
    
    <!-- In/out transitions -->
    {#if visible}
      <div in:fade out:slide>
        Fades in, slides out
      </div>
    {/if}
    
    <!-- Animate list reordering -->
    {#each items as item (item)}
      <div animate:flip={{ duration: 300 }}>
        {item}
      </div>
    {/each}
    
    <!-- Custom transition -->
    <script>
      function typewriter(node, { speed = 50 }) {
        const text = node.textContent;
        const duration = text.length * speed;
    
        return {
          duration,
          tick: (t) => {
            const i = Math.floor(text.length * t);
            node.textContent = text.slice(0, i);
          }
        };
      }
    </script>
    
    <p in:typewriter={{ speed: 30 }}>Hello, world!</p>
    

---
  #### **Name**
Component Composition
  #### **Description**
Slots, snippets, and component patterns
  #### **When**
Building reusable components
  #### **Example**
    # COMPONENT PATTERNS:
    
    """
    Svelte components use slots for composition
    and snippets (Svelte 5) for render props.
    """
    
    <!-- Card.svelte -->
    <script>
      let { title, children } = $props();
    </script>
    
    <div class="card">
      <header>{title}</header>
      <main>{@render children()}</main>
    </div>
    
    <!-- Usage -->
    <Card title="Welcome">
      <p>This is the card content</p>
    </Card>
    
    <!-- Named slots (Svelte 4 style) -->
    <div class="card">
      <slot name="header" />
      <slot />
      <slot name="footer" />
    </div>
    
    <Card>
      <h2 slot="header">Title</h2>
      <p>Content</p>
      <button slot="footer">Action</button>
    </Card>
    
    <!-- Snippets (Svelte 5) - render props pattern -->
    <script>
      let { items, row } = $props();
    </script>
    
    <ul>
      {#each items as item}
        <li>{@render row(item)}</li>
      {/each}
    </ul>
    
    <!-- Usage with snippet -->
    <List {items}>
      {#snippet row(item)}
        <span>{item.name}: {item.value}</span>
      {/snippet}
    </List>
    

## Anti-Patterns


---
  #### **Name**
Fighting Reactivity
  #### **Description**
Using callbacks/events when assignment would work
  #### **Why**
    Svelte's reactivity is based on assignment. If you're creating
    callbacks to update state like in React, you're missing the point.
    Just assign to the variable.
    
  #### **Instead**
    // WRONG: React-style callbacks
    let count = $state(0);
    function setCount(newValue) {
      count = newValue;
    }
    <Child {count} {setCount} />
    
    // RIGHT: Direct binding
    let count = $state(0);
    <Child bind:count />
    
    // Or pass and mutate
    <Child {count} onIncrement={() => count++} />
    

---
  #### **Name**
Overusing Stores
  #### **Description**
Using stores when props/context would suffice
  #### **Why**
    Stores are global. Overusing them makes components less reusable
    and harder to test. Props are simpler for parent-child communication.
    
  #### **Instead**
    // WRONG: Store for local state
    import { writable } from 'svelte/store';
    const modalOpen = writable(false);
    
    // RIGHT: Component state
    let modalOpen = $state(false);
    
    // RIGHT: Context for subtree
    import { setContext, getContext } from 'svelte';
    setContext('theme', { mode: 'dark' });
    const theme = getContext('theme');
    

---
  #### **Name**
Not Using Form Actions
  #### **Description**
Client-side form handling when actions would work
  #### **Why**
    Form actions provide progressive enhancement - forms work without
    JavaScript. Client-only handlers break when JS fails or is slow.
    
  #### **Instead**
    // WRONG: Client-side only
    <form onsubmit={handleSubmit}>
      <input bind:value={email} />
    </form>
    
    // RIGHT: Form action with enhancement
    // +page.server.ts
    export const actions = {
      default: async ({ request }) => {
        const data = await request.formData();
        // Handle on server
      }
    };
    
    // +page.svelte
    <form method="POST" use:enhance>
      <input name="email" />
    </form>
    

---
  #### **Name**
Ignoring SSR Considerations
  #### **Description**
Using browser APIs without checking environment
  #### **Why**
    SvelteKit runs on the server. localStorage, window, document
    don't exist there. Your code will crash during SSR.
    
  #### **Instead**
    // WRONG: Direct browser API
    const theme = localStorage.getItem('theme');
    
    // RIGHT: Check browser environment
    import { browser } from '$app/environment';
    
    let theme = $state('light');
    
    $effect(() => {
      if (browser) {
        theme = localStorage.getItem('theme') ?? 'light';
      }
    });
    
    // RIGHT: Use onMount
    import { onMount } from 'svelte';
    
    onMount(() => {
      // Only runs in browser
      theme = localStorage.getItem('theme');
    });
    

---
  #### **Name**
Prop Drilling Through Many Levels
  #### **Description**
Passing props through intermediate components
  #### **Why**
    Makes intermediate components coupled to data they don't use.
    Hard to maintain when data shape changes.
    
  #### **Instead**
    // WRONG: Prop drilling
    <Parent {user}>
      <Intermediate {user}>
        <Child {user} />
      </Intermediate>
    </Parent>
    
    // RIGHT: Context
    // Parent
    import { setContext } from 'svelte';
    setContext('user', user);
    
    // Child (any depth)
    import { getContext } from 'svelte';
    const user = getContext('user');
    