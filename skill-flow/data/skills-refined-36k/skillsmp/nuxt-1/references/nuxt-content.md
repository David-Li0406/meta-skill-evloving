# Nuxt Content Reference

**Last Updated:** 2025-11 (v3.8.0)

**Check:** `@nuxt/content` in package.json

Nuxt Content v3 is a Git-based CMS that uses SQL-backed collections for querying markdown, YAML, JSON, and CSV files. Perfect for blogs, documentation sites, and content-heavy applications.

## Installation & Setup

```bash
pnpm add @nuxt/content
```

**nuxt.config.ts:**

```typescript
export default defineNuxtConfig({
  modules: ["@nuxt/content"],

  content: {
    // Optional configuration
    highlight: {
      theme: "github-dark",
      preload: ["typescript", "vue", "bash"],
    },
  },
})
```

## Collections

### Defining Collections

Create `content.config.ts` in your project root:

```typescript
import { defineCollection, defineContentConfig, z } from "@nuxt/content"

export default defineContentConfig({
  collections: {
    blog: defineCollection({
      type: "page",
      source: "blog/**/*.md",
      schema: z.object({
        title: z.string(),
        description: z.string(),
        date: z.string(),
        tags: z.array(z.string()).optional(),
        author: z.string().optional(),
        image: z.string().optional(),
        draft: z.boolean().default(false),
      }),
    }),

    docs: defineCollection({
      type: "page",
      source: "docs/**/*.md",
      schema: z.object({
        title: z.string(),
        description: z.string(),
        category: z.string().optional(),
      }),
    }),
  },
})
```

### Directory Structure

```
content/
├── blog/
│   ├── post-1.md
│   ├── post-2.md
│   └── post-3.md
└── docs/
    ├── getting-started.md
    └── api/
        └── components.md
```

## Frontmatter

Add metadata to content files:

```markdown
---
title: "My Blog Post"
description: "A brief description"
date: "2025-01-04"
tags: ["nuxt", "vue", "web-dev"]
author: "John Doe"
image: "/images/cover.jpg"
draft: false
---

# Content starts here

Your markdown content...
```

## Querying Collections

### queryCollection Composable

The main API for querying content in v3:

```vue
<script setup lang="ts">
// Get all articles from 'blog' collection
const { data: articles } = await useAsyncData("articles", () =>
  queryCollection("blog").all(),
)

// Get single article by path
const route = useRoute()
const { data: article } = await useAsyncData("article", () =>
  queryCollection("blog").path(route.path).first(),
)
</script>

<template>
  <div>
    <h1>{{ article?.title }}</h1>
    <ContentRenderer v-if="article" :value="article" />
  </div>
</template>
```

### Query Methods

#### all()

Get all matching documents:

```typescript
const posts = await queryCollection("blog").all()
```

#### first()

Get first matching document:

```typescript
const post = await queryCollection("blog").path("/blog/my-post").first()
```

#### where()

Filter by field with SQL operators:

```typescript
// Single condition
const published = await queryCollection("blog").where("draft", "=", false).all()

// Multiple conditions (AND)
const filtered = await queryCollection("blog")
  .where("draft", "=", false)
  .where("category", "=", "tech")
  .all()
```

#### andWhere()

Complex AND conditions:

```typescript
const posts = await queryCollection("blog")
  .where("published", "=", true)
  .andWhere((query) =>
    query.where("date", ">", "2024-01-01").where("category", "=", "news"),
  )
  .all()
```

#### orWhere()

OR conditions:

```typescript
const posts = await queryCollection("blog")
  .where("published", "=", true)
  .orWhere((query) =>
    query.where("featured", "=", true).where("priority", ">", 5),
  )
  .all()
```

#### order()

Sort results:

```typescript
// Descending
const posts = await queryCollection("blog").order("date", "DESC").all()

// Ascending
const posts = await queryCollection("blog").order("title", "ASC").all()
```

#### limit()

Limit results:

```typescript
const latest = await queryCollection("blog")
  .order("date", "DESC")
  .limit(5)
  .all()
```

#### skip()

Skip results (for pagination):

```typescript
const page = 2
const perPage = 10

const posts = await queryCollection("blog")
  .order("date", "DESC")
  .skip((page - 1) * perPage)
  .limit(perPage)
  .all()
```

#### select()

Select specific fields:

```typescript
const posts = await queryCollection("blog")
  .select(["title", "description", "date", "path"])
  .all()
```

#### path()

Filter by path:

```typescript
const post = await queryCollection("blog").path("/blog/my-post").first()
```

## ContentRenderer Component

Renders parsed markdown content (the main component for v3):

```vue
<script setup lang="ts">
const route = useRoute()
const { data: post } = await useAsyncData("post", () =>
  queryCollection("blog").path(route.path).first(),
)
</script>

<template>
  <article v-if="post" class="prose dark:prose-invert">
    <h1>{{ post.title }}</h1>
    <ContentRenderer :value="post" />
  </article>
</template>
```

With error handling:

```vue
<script setup lang="ts">
const route = useRoute()
const { data: post, error } = await useAsyncData("post", () =>
  queryCollection("blog").path(route.path).first(),
)

if (error.value || !post.value) {
  throw createError({
    statusCode: 404,
    message: "Post not found",
  })
}
</script>

<template>
  <ContentRenderer :value="post" />
</template>
```

## Common Patterns

### Blog List Page

```vue
<script setup lang="ts">
const { data: articles } = await useAsyncData("articles", () =>
  queryCollection("blog")
    .where("draft", "=", false)
    .order("date", "DESC")
    .all(),
)
</script>

<template>
  <div>
    <h1>Blog</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <article v-for="article of articles" :key="article.path" class="card">
        <NuxtImg
          v-if="article.image"
          :src="article.image"
          :alt="article.title"
          class="w-full h-48 object-cover"
        />
        <div class="p-4">
          <h2 class="text-xl font-bold">{{ article.title }}</h2>
          <p class="text-gray-600">{{ article.description }}</p>
          <div class="flex items-center gap-2 mt-2 text-sm text-gray-500">
            <span>{{ article.author }}</span>
            <span>•</span>
            <time>{{ article.date }}</time>
          </div>
          <NuxtLink
            :to="article.path"
            class="text-blue-500 hover:underline mt-2 inline-block"
          >
            Read more →
          </NuxtLink>
        </div>
      </article>
    </div>
  </div>
</template>
```

### Single Blog Post with Related Articles

```vue
<script setup lang="ts">
const route = useRoute()

const { data: article } = await useAsyncData("article", () =>
  queryCollection("blog").path(route.path).first(),
)

if (!article.value) {
  throw createError({
    statusCode: 404,
    message: "Article not found",
  })
}

// Get related articles by tags
const { data: related } = await useAsyncData("related", async () => {
  if (!article.value?.tags?.length) return []

  const all = await queryCollection("blog").where("draft", "=", false).all()

  // Filter by matching tags
  return all
    .filter(
      (post) =>
        post.path !== route.path &&
        post.tags?.some((tag) => article.value.tags.includes(tag)),
    )
    .slice(0, 3)
})

useSeoMeta({
  title: article.value.title,
  description: article.value.description,
  ogImage: article.value.image,
})
</script>

<template>
  <article class="prose dark:prose-invert mx-auto">
    <h1>{{ article.title }}</h1>
    <div class="flex items-center gap-4 text-gray-600 mb-8">
      <span>{{ article.author }}</span>
      <time>{{ article.date }}</time>
      <div v-if="article.tags" class="flex gap-2">
        <span v-for="tag of article.tags" :key="tag" class="badge">
          {{ tag }}
        </span>
      </div>
    </div>

    <ContentRenderer :value="article" />

    <div v-if="related?.length" class="mt-12">
      <h2>Related Articles</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="post of related" :key="post.path">
          <NuxtLink :to="post.path">{{ post.title }}</NuxtLink>
        </div>
      </div>
    </div>
  </article>
</template>
```

### Documentation Site

```vue
<!-- pages/docs/[...slug].vue -->
<script setup lang="ts">
const route = useRoute()
const slug = (route.params.slug as string[])?.join("/") || "index"

const { data: doc } = await useAsyncData(`doc-${slug}`, () =>
  queryCollection("docs").path(`/docs/${slug}`).first(),
)

if (!doc.value) {
  throw createError({ statusCode: 404, message: "Documentation not found" })
}

// Get navigation
const { data: navigation } = await useAsyncData("docs-nav", () =>
  queryCollectionNavigation("docs"),
)

useSeoMeta({
  title: doc.value.title,
  description: doc.value.description,
})
</script>

<template>
  <div class="flex">
    <!-- Sidebar navigation -->
    <aside class="w-64 pr-8">
      <nav>
        <ul>
          <li v-for="link of navigation" :key="link.path">
            <NuxtLink :to="link.path">{{ link.title }}</NuxtLink>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1">
      <article class="prose dark:prose-invert">
        <h1>{{ doc.title }}</h1>
        <ContentRenderer :value="doc" />
      </article>
    </main>
  </div>
</template>
```

### Search

```vue
<script setup lang="ts">
const searchQuery = ref("")
const { data: allPosts } = await useAsyncData("all-posts", () =>
  queryCollection("blog").all(),
)

const results = computed(() => {
  if (!searchQuery.value) return []

  const query = searchQuery.value.toLowerCase()
  return (
    allPosts.value
      ?.filter(
        (post) =>
          post.title?.toLowerCase().includes(query) ||
          post.description?.toLowerCase().includes(query),
      )
      .slice(0, 10) || []
  )
})
</script>

<template>
  <div>
    <input
      v-model="searchQuery"
      type="search"
      placeholder="Search articles..."
      class="w-full px-4 py-2 border rounded"
    />

    <div v-if="results.length" class="mt-4">
      <div v-for="result of results" :key="result.path" class="mb-4">
        <NuxtLink :to="result.path" class="text-lg font-bold">
          {{ result.title }}
        </NuxtLink>
        <p class="text-gray-600">{{ result.description }}</p>
      </div>
    </div>
  </div>
</template>
```

### Pagination

```vue
<script setup lang="ts">
const route = useRoute()
const page = computed(() => parseInt(route.query.page as string) || 1)
const perPage = 10

const { data: posts } = await useAsyncData(
  `posts-page-${page.value}`,
  () =>
    queryCollection("blog")
      .where("draft", "=", false)
      .order("date", "DESC")
      .skip((page.value - 1) * perPage)
      .limit(perPage)
      .all(),
  {
    watch: [page],
  },
)

// Get total count for pagination
const { data: allPosts } = await useAsyncData("all-posts", () =>
  queryCollection("blog").where("draft", "=", false).all(),
)

const totalPages = computed(() =>
  Math.ceil((allPosts.value?.length || 0) / perPage),
)
</script>

<template>
  <div>
    <div class="grid gap-6">
      <article v-for="post of posts" :key="post.path">
        <!-- Article card -->
      </article>
    </div>

    <div class="flex justify-center gap-2 mt-8">
      <NuxtLink v-if="page > 1" :to="{ query: { page: page - 1 } }" class="btn">
        Previous
      </NuxtLink>

      <span>Page {{ page }} of {{ totalPages }}</span>

      <NuxtLink
        v-if="page < totalPages"
        :to="{ query: { page: page + 1 } }"
        class="btn"
      >
        Next
      </NuxtLink>
    </div>
  </div>
</template>
```

### Filter by Tags/Categories

```vue
<script setup lang="ts">
const selectedTag = ref<string | null>(null)

// Get all posts to extract unique tags
const { data: allPosts } = await useAsyncData("all-posts", () =>
  queryCollection("blog").where("draft", "=", false).all(),
)

const tags = computed(() => {
  const tagSet = new Set<string>()
  allPosts.value?.forEach((post) => {
    post.tags?.forEach((tag: string) => tagSet.add(tag))
  })
  return Array.from(tagSet).sort()
})

// Filter posts by selected tag
const filteredPosts = computed(() => {
  if (!selectedTag.value) return allPosts.value

  return allPosts.value?.filter((post) =>
    post.tags?.includes(selectedTag.value!),
  )
})
</script>

<template>
  <div>
    <div class="flex gap-2 mb-6">
      <button :class="{ active: !selectedTag }" @click="selectedTag = null">
        All
      </button>
      <button
        v-for="tag of tags"
        :key="tag"
        :class="{ active: selectedTag === tag }"
        @click="selectedTag = tag"
      >
        {{ tag }}
      </button>
    </div>

    <div class="grid gap-6">
      <article v-for="post of filteredPosts" :key="post.path">
        <h2>{{ post.title }}</h2>
        <p>{{ post.description }}</p>
        <NuxtLink :to="post.path">Read more</NuxtLink>
      </article>
    </div>
  </div>
</template>
```

## Server-Side Queries

Use `queryCollection` in API routes with event parameter:

```typescript
// server/api/posts.get.ts
export default defineEventHandler(async (event) => {
  const posts = await queryCollection(event, "blog")
    .where("draft", "=", false)
    .order("date", "DESC")
    .limit(10)
    .all()

  return posts
})
```

With query parameters:

```typescript
// server/api/posts/[slug].get.ts
export default defineEventHandler(async (event) => {
  const slug = getRouterParam(event, "slug")

  const post = await queryCollection(event, "blog")
    .path(`/blog/${slug}`)
    .first()

  if (!post) {
    throw createError({
      statusCode: 404,
      message: "Post not found",
    })
  }

  return post
})
```

## Navigation

Use `queryCollectionNavigation` for generating navigation:

```vue
<script setup lang="ts">
const { data: navigation } = await useAsyncData("navigation", () =>
  queryCollectionNavigation("docs"),
)
</script>

<template>
  <nav>
    <ul>
      <li v-for="item of navigation" :key="item.path">
        <NuxtLink :to="item.path">{{ item.title }}</NuxtLink>
        <ul v-if="item.children">
          <li v-for="child of item.children" :key="child.path">
            <NuxtLink :to="child.path">{{ child.title }}</NuxtLink>
          </li>
        </ul>
      </li>
    </ul>
  </nav>
</template>
```

### queryCollectionItemSurroundings

Get previous/next items for navigation:

```vue
<script setup lang="ts">
const route = useRoute()
const { data: surround } = await useAsyncData("surround", () =>
  queryCollectionItemSurroundings("docs", route.path),
)
</script>

<template>
  <div class="flex justify-between">
    <NuxtLink v-if="surround?.prev" :to="surround.prev.path">
      ← {{ surround.prev.title }}
    </NuxtLink>
    <NuxtLink v-if="surround?.next" :to="surround.next.path">
      {{ surround.next.title }} →
    </NuxtLink>
  </div>
</template>
```

### queryCollectionSearchSections

Full-text search across content sections:

```vue
<script setup lang="ts">
const searchQuery = ref("")

const { data: searchResults } = await useAsyncData(
  "search",
  () => queryCollectionSearchSections("docs", searchQuery.value),
  { watch: [searchQuery] },
)
</script>
```

## Prose Components

Nuxt Content provides `Prose*` components for rendering markdown elements with custom styling. Place in `components/content/`:

- `ProseH1`, `ProseH2`, `ProseH3` - Headings
- `ProseP` - Paragraphs
- `ProseA` - Links
- `ProseCode`, `ProsePre` - Code blocks
- `ProseImg` - Images
- `ProseUl`, `ProseOl`, `ProseLi` - Lists
- `ProseTable`, `ProseThead`, `ProseTbody`, `ProseTr`, `ProseTh`, `ProseTd` - Tables

See full list: https://content.nuxt.com/docs/components/prose

## Markdown Features

### Syntax Highlighting

Configure in `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  content: {
    highlight: {
      theme: {
        default: "github-light",
        dark: "github-dark",
      },
      preload: ["typescript", "vue", "bash", "json"],
    },
  },
})
```

Use in markdown:

````markdown
```typescript
interface User {
  name: string
  age: number
}
```
````

### Custom Vue Components in Markdown

Use Vue components directly in markdown (MDC syntax):

```markdown
# My Article

::Alert{type="info"}
This is an informational alert!
::

::CallToAction{title="Get Started" url="/docs"}
Learn more about Nuxt Content
::
```

Register components in `components/content/` directory:

```vue
<!-- components/content/Alert.vue -->
<script setup lang="ts">
defineProps<{
  type?: "info" | "warning" | "error"
}>()
</script>

<template>
  <div :class="`alert alert-${type}`">
    <slot />
  </div>
</template>
```

## TypeScript Support

Type your collections:

```typescript
// types/content.ts
export interface BlogPost {
  title: string
  description: string
  date: string
  tags?: string[]
  author?: string
  image?: string
  draft: boolean
  path: string
  body: any
}
```

Use in components:

```vue
<script setup lang="ts">
import type { BlogPost } from "~/types/content"

const { data: posts } = await useAsyncData("posts", () =>
  queryCollection<BlogPost>("blog").all(),
)
</script>
```

## Migration from v2

### Key Changes

1. **`queryContent()` → `queryCollection(name)`**

   ```typescript
   // v2
   queryContent("/blog").find()

   // v3
   queryCollection("blog").all()
   ```

2. **Collections must be defined in `content.config.ts`**

3. **Components removed:**
   - ❌ `<ContentDoc>` - use ContentRenderer
   - ❌ `<ContentList>` - query manually with queryCollection
   - ❌ `<ContentNavigation>` - use queryCollectionNavigation
   - ❌ `<ContentQuery>` - use queryCollection

4. **New query methods:**
   - `.all()` instead of `.find()`
   - `.first()` instead of `.findOne()`
   - `.where()` with SQL operators
   - `.order()` instead of `.sort()`

5. **SQL-backed storage** - faster queries for large datasets

## Deployment

Nuxt Content works with all Nuxt deployment targets. Key platforms with specific guides:

- **Cloudflare Pages/Workers** - Use D1 database adapter
- **Vercel** - Edge-compatible with serverless functions
- **Netlify** - Static or serverless deployment
- **NuxtHub** - First-party hosting with database support

See deployment guides: https://content.nuxt.com/docs/deploy

## Integrations

- **Nuxt Studio** - Visual CMS editor for content: https://nuxt.studio
- **I18n** - Multi-language content with locale-based collections
- **LLMs/AI** - Generate embeddings for semantic search

## Best Practices

1. **Define collections** - Create `content.config.ts` with schemas
2. **Use TypeScript** - Type your collections for better DX
3. **Cache queries** - Use `useAsyncData` with proper keys
4. **Server-side queries** - Query on server for API routes
5. **Index for performance** - Consider indexing frequently queried fields
6. **Validate frontmatter** - Use Zod schemas in collection definitions
7. **Handle 404s** - Check if content exists and throw errors
8. **Use path()** - More efficient than where() for path filtering
9. **Select fields** - Use `.select()` to reduce payload size
10. **Pagination** - Implement for large collections

## Official Resources

- **Documentation:** https://content.nuxt.com
- **Collections:** https://content.nuxt.com/docs/collections
- **Query API:** https://content.nuxt.com/docs/utils/query-collection
- **Migration Guide:** https://content.nuxt.com/docs/getting-started/migration
- **GitHub:** https://github.com/nuxt/content

---

**Note:** This reference covers Nuxt Content v3. The v2 API (`queryContent`, `ContentDoc`, `ContentList`) is deprecated and not compatible with v3.
