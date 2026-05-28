---
name: svelte
description: Build Svelte 5 apps with async svelte and remote functions. Always use this when writing svelte code.
---

<rules>
1. [Reactivity]: `$derived` over `$effect` — $effect is escape hatch for external systems (DOM APIs, timers)
2. [Single-flight]: Same query + same args = one request (auto-deduplicated)
3. [Auth at DAL]: Every `.remote.ts` validates auth before DB calls
4. [DB layer]: Authorization-unaware, no `getRequestEvent()`
</rules>

## Type-safe Context

```ts
export const [useFoo, setupFoo] = createContext<Foo>();
```

## Type-safe Navigation (`$app/paths`)

```ts
import { resolve, asset } from '$app/paths';

// 静的パス (base path 付き)
resolve('/about');

// 動的パス - プレースホルダーは src/routes の構造と一致必須
resolve('/blog/[slug]', { slug: 'my-post' }); // ✅
resolve('/blog/[id]', { id: 'my-post' });     // ❌ TypeScript error

// 静的アセット (static/ 内)
asset('/favicon.png');
```

## Hydratable (v5.44+)

SSR データをクライアントで再利用し、hydration 時の重複 fetch を排除:

```ts
// Before: SSR と hydration で2回 fetch
const data = await fetchData();

// After: SSR の結果を再利用、1回で済む
const data = await hydratable('unique-key', () => fetchData());
```

注意: データは JSON serializable である必要あり

<do>
- class arrays (built-in clsx): `class={["btn", active && "active", size]}`
- `{@const x = derived}` - template内ローカル定数
- `$bindable()` - 双方向バインディング用props: `let { value = $bindable() } = $props()`
- リアクティブな async: `let data = $derived(await fetchData(id))` - idが変わると自動refetch
- lazy init: `let x = $derived.by(() => expensiveComputation())` - 参照時に初めて評価
- context は `await` より前に呼ぶ
- `{#snippet}` と `{@render}` を使う:
```svelte
<!-- 親: propsとしてsnippetを渡す -->
<Card>
  {#snippet header()}<h1>Title</h1>{/snippet}
  {#snippet children()}Content here{/snippet}
</Card>

<!-- 子: propsで受け取って@renderで描画 -->
<script>let { header, children } = $props()</script>

{@render header()}
{@render children()}

````
</do>

<dont>
- `<slot />` - 非推奨。`{#snippet}` を使う
- `svelte:boundary` - 不要。top-level awaitでエラーは親に伝播、pendingは自動処理
- `svelte:boundary` の `{#snippet pending()}` - 不安定。使う場合もpendingは避ける
- `base` from `$app/paths` - 非推奨。`resolve()` を使う
</dont>

<layers>
Anywhere → DAL (`$lib/data/*.remote.ts`) → DB (`$lib/server/database/*`)

- `*.remote.ts` - DAL with authorization (`query`/`form`/`command`)
- `*.server.ts`, `$lib/server` - Trusted, server-only execution (includes DB)
</layers>

## Remote Functions

Create in `.remote.ts` files.

### Types

```ts
import * as v from "valibot";
import { query, form, command } from "$app/server";

// QUERY: read data
export const getPost = query(v.string(), async (slug) => {
  return db.posts.findBySlug(slug);
});

// FORM: mutations with progressive enhancement
export const createPost = form(
  v.object({ title: v.string(), content: v.string() }),
  async (data) => {
    await db.posts.create(data);
    await listPosts.refresh();
    redirect(303, "/blog");
  },
);

// COMMAND: mutations that can be called from JS instead of form
export const deletePost = command(v.string(), async (id) => {
  await db.posts.delete(id);
  await listPosts.refresh();
});
````

### Command usage

```ts
await addLike(id);
// or let svelte update other queries after this:
// This is not necessary if `addLike` command runs `await getLikes().refresh()` server-side as above
await addLike(id).updates(getLikes());
```

with optimistic updates:

```ts
await addLike(id).updates(getLikes(id).withOverride((n) => n + 1));
```

### Form Usage

```svelte
<form {...createPost}>
  <input {...createPost.fields.title.as("text")} />
  <input {...createPost.fields.content.as("textarea")} />

  {#each createPost.fields.title.issues() as issue}
    <p class="error">{issue.message}</p>
  {/each}

  <button disabled={!!createPost.pending}>Submit</button>
</form>
```

Field Types:

```svelte
.as("text") .as("number") .as("email") .as("date")
.as("file") .as("checkbox") .as("radio", "value") .as("textarea") .as("select")
```

## Ecosystem

See context7 for library docs.

### Components & Styling

- bits-ui - headless components
- melt-ui - headless components (svelte 5 support is experimental, prefer bits-ui for now)
- Skeleton UI - styled components
- shadcn-svelte - copy-paste components like shadcn/ui in React
- svelte-sonner - toast notifications, built into shadcn-svelte
- PaneForge - write resizable panes declaratively
- Threlte - declarative ThreeJS for svelte
- Svelte Flow - node-based editor

### Icons

- lucide-svelte - icons
- @iconify/svelte - 200k+ icons from multiple sets
- svelte-radix - Radix icons
- svelte-heroes-v2 - hero-icons for svelte

### State & Async

- Remote Functions & Async Svelte - builtin to svelte and kit, very good
- @tanstack/svelte-query - async state management
- xstate + @xstate/svelte - statecharts, actor model FSM
- robot3 - lightweight (1kb) functional FSM

### Utility

- runed - svelte utility collection
- svelte-nuqs - URL query state sync
- svelte-persisted-store - localStorage-backed stores
- @testing-library/svelte - component testing

## References

- [Architecture](./references/architecture.md) - structures, auth helpers
- [Advanced Patterns](./references/advanced-patterns.md) - batching, optimistic UI, advanced form
- [File Uploads](./references/file-uploads.md) - form/command file upload patterns
- [XState](./references/xstate.md) - full-featured statecharts, actors, parallel states
- [Robot3](./references/robot3.md) - lightweight (1kb) functional FSM
- [Svelte Docs](https://svelte.dev/llms-medium.txt) - full documentation
