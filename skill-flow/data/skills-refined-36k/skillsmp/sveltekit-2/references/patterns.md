# SvelteKit

## Patterns


---
  #### **Name**
Server Load Functions
  #### **Description**
Load data on the server with access to cookies, secrets, and databases
  #### **When**
You need to fetch data that requires authentication or server-only resources
  #### **Example**
    // src/routes/dashboard/+page.server.ts
    import type { PageServerLoad } from './$types';
    
    export const load: PageServerLoad = async ({ locals, cookies }) => {
      const session = await locals.auth();
      if (!session) throw redirect(303, '/login');
    
      const data = await db.query('SELECT * FROM projects WHERE user_id = $1', [session.userId]);
      return { projects: data };
    };
    

---
  #### **Name**
Form Actions
  #### **Description**
Handle form submissions with progressive enhancement
  #### **When**
Processing user input, mutations, or any POST/PUT/DELETE operations
  #### **Example**
    // src/routes/todos/+page.server.ts
    import type { Actions } from './$types';
    
    export const actions: Actions = {
      create: async ({ request, locals }) => {
        const data = await request.formData();
        const title = data.get('title');
    
        await db.todo.create({ data: { title, userId: locals.user.id } });
        return { success: true };
      },
      delete: async ({ request }) => {
        const data = await request.formData();
        const id = data.get('id');
        await db.todo.delete({ where: { id } });
      }
    };
    
    // +page.svelte
    <form method="POST" action="?/create" use:enhance>
      <input name="title" required />
      <button>Add</button>
    </form>
    

---
  #### **Name**
Svelte 5 Runes
  #### **Description**
Use $state, $derived, and $effect for reactive state management
  #### **When**
Managing component state in Svelte 5
  #### **Example**
    <script lang="ts">
      let { data } = $props();
    
      let count = $state(0);
      let doubled = $derived(count * 2);
    
      $effect(() => {
        console.log(`Count changed to ${count}`);
        // Cleanup function (optional)
        return () => console.log('Cleaning up');
      });
    </script>
    
    <button onclick={() => count++}>
      {count} x 2 = {doubled}
    </button>
    

---
  #### **Name**
Layout Data Inheritance
  #### **Description**
Share data across routes using layout load functions
  #### **When**
You have data needed by multiple child routes (user session, settings)
  #### **Example**
    // src/routes/+layout.server.ts
    export const load = async ({ locals }) => {
      return {
        user: locals.user,
        settings: await getSettings(locals.user?.id)
      };
    };
    
    // src/routes/dashboard/+page.svelte
    <script>
      let { data } = $props();
      // data.user is available from parent layout
    </script>
    

---
  #### **Name**
API Routes with +server.ts
  #### **Description**
Create REST API endpoints when you need them
  #### **When**
Building APIs for external consumers or when form actions don't fit
  #### **Example**
    // src/routes/api/webhooks/stripe/+server.ts
    import type { RequestHandler } from './$types';
    import { json, error } from '@sveltejs/kit';
    
    export const POST: RequestHandler = async ({ request }) => {
      const signature = request.headers.get('stripe-signature');
      const body = await request.text();
    
      try {
        const event = stripe.webhooks.constructEvent(body, signature, secret);
        // Handle event...
        return json({ received: true });
      } catch (err) {
        throw error(400, 'Webhook signature verification failed');
      }
    };
    

---
  #### **Name**
Error Handling
  #### **Description**
Handle errors gracefully with +error.svelte pages
  #### **When**
You need custom error pages or want to catch specific errors
  #### **Example**
    // src/routes/+error.svelte
    <script>
      import { page } from '$app/stores';
    </script>
    
    <h1>{$page.status}: {$page.error?.message}</h1>
    
    {#if $page.status === 404}
      <p>Page not found</p>
    {:else}
      <p>Something went wrong</p>
    {/if}
    
    // Throwing errors in load functions
    import { error } from '@sveltejs/kit';
    
    export const load = async ({ params }) => {
      const post = await getPost(params.slug);
      if (!post) throw error(404, 'Post not found');
      return { post };
    };
    

## Anti-Patterns


---
  #### **Name**
Fetching in Components
  #### **Description**
Using fetch or onMount to load data that should come from load functions
  #### **Why**
Causes waterfalls, flashing content, and loses SSR benefits
  #### **Instead**
Use +page.ts or +page.server.ts load functions

---
  #### **Name**
Using Stores in Svelte 5
  #### **Description**
Using writable/readable stores when runes are available
  #### **Why**
Runes ($state, $derived) are simpler and more performant in Svelte 5
  #### **Instead**
Use $state for reactive variables, $derived for computed values

---
  #### **Name**
API Routes for Forms
  #### **Description**
Creating +server.ts endpoints just to handle form submissions
  #### **Why**
Form actions are simpler, support progressive enhancement, and handle CSRF
  #### **Instead**
Use form actions in +page.server.ts with use:enhance

---
  #### **Name**
Client-Side Auth Checks
  #### **Description**
Checking authentication in components or +page.ts
  #### **Why**
+page.ts runs on client too, exposing logic. Auth should be server-only
  #### **Instead**
Check auth in +page.server.ts or hooks.server.ts

---
  #### **Name**
Ignoring use:enhance
  #### **Description**
Using form actions without the enhance action
  #### **Why**
Without enhance, forms cause full page reloads
  #### **Instead**
Add use:enhance for SPA-like form submissions

---
  #### **Name**
Load Function Waterfalls
  #### **Description**
Sequential await calls in load functions that could be parallel
  #### **Why**
Increases page load time unnecessarily
  #### **Instead**
Use Promise.all for independent data fetches