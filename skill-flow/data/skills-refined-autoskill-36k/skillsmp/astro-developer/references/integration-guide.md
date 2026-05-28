# Astro Integration Guide

This guide provides detailed setup instructions for common Astro integrations.

## UI Framework Integrations

### React

#### Installation

```bash
npx astro add react
```

#### Manual Setup

1. Install dependencies:

```bash
npm install @astrojs/react react react-dom
npm install -D @types/react @types/react-dom
```

2. Update `astro.config.mjs`:

```javascript
import { defineConfig } from "astro/config";
import react from "@astrojs/react";

export default defineConfig({
  integrations: [react()],
});
```

3. Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "react"
  }
}
```

#### Usage Examples

```astro
---
import ReactCounter from '../components/ReactCounter.jsx';
import { useState } from 'react';
---

<!-- Static React component -->
<ReactCounter initialCount={0} />

<!-- Interactive component with state -->
<ReactCounter client:load />

<!-- With props -->
<ReactCounter
  client:visible
  step={5}
  max={100}
/>
```

```jsx
// src/components/ReactCounter.jsx
import { useState, useEffect } from "react";

export default function ReactCounter({ initialCount = 0, step = 1, max = 10 }) {
  const [count, setCount] = useState(initialCount);

  useEffect(() => {
    console.log("Counter mounted");
  }, []);

  return (
    <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm max-w-sm mx-auto">
      <p className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
        Count: {count}
      </p>
      <div className="flex gap-2">
        <button
          onClick={() => setCount((c) => Math.min(c + step, max))}
          className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors duration-200"
        >
          Increment
        </button>
        <button
          onClick={() => setCount((c) => Math.max(c - step, 0))}
          className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-md transition-colors duration-200"
        >
          Decrement
        </button>
      </div>
    </div>
  );
}
```

### Vue

#### Installation

```bash
npx astro add vue
```

#### Manual Setup

1. Install dependencies:

```bash
npm install @astrojs/vue vue
```

2. Update `astro.config.mjs`:

```javascript
import { defineConfig } from "astro/config";
import vue from "@astrojs/vue";

export default defineConfig({
  integrations: [vue()],
});
```

#### Usage Examples

```astro
---
import VueCounter from '../components/VueCounter.vue';
---

<VueCounter client:load initial-value="10" />
```

```vue
<!-- src/components/VueCounter.vue -->
<template>
  <div
    class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm max-w-sm mx-auto"
  >
    <p class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
      Count: {{ count }}
    </p>
    <div class="flex gap-2">
      <button
        @click="increment"
        class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors duration-200"
      >
        Increment
      </button>
      <button
        @click="decrement"
        class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-md transition-colors duration-200"
      >
        Decrement
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const props = defineProps({
  initialValue: {
    type: Number,
    default: 0,
  },
});

const count = ref(props.initialValue);

const increment = () => {
  count.value++;
};

const decrement = () => {
  count.value = Math.max(0, count.value - 1);
};

onMounted(() => {
  console.log("Vue component mounted");
});
</script>
```

### Svelte

#### Installation

```bash
npx astro add svelte
```

#### Manual Setup

1. Install dependencies:

```bash
npm install @astrojs/svelte svelte
```

2. Update `astro.config.mjs`:

```javascript
import { defineConfig } from "astro/config";
import svelte from "@astrojs/svelte";

export default defineConfig({
  integrations: [svelte()],
});
```

#### Usage Examples

```astro
---
import SvelteCounter from '../components/SvelteCounter.svelte';
---

<SvelteCounter client:load initial={5} />
```

```svelte
<!-- src/components/SvelteCounter.svelte -->
<script>
  import { onMount } from 'svelte';

  export let initial = 0;
  let count = initial;

  function increment() {
    count += 1;
  }

  function decrement() {
    count = Math.max(0, count - 1);
  }

  onMount(() => {
    console.log('Svelte component mounted');
  });
</script>

<div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm max-w-sm mx-auto">
  <p class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Count: {count}</p>
  <div class="flex gap-2">
    <button
      on:click={increment}
      class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors duration-200"
    >
      Increment
    </button>
    <button
      on:click={decrement}
      class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-md transition-colors duration-200"
    >
      Decrement
    </button>
  </div>
</div>
```

## Styling Integrations

### Tailwind CSS

#### Installation

```bash
npx astro add tailwind
```

#### Manual Setup

1. Install dependencies:

```bash
npm install -D tailwindcss @astrojs/tailwind
```

2. Initialize Tailwind:

```bash
npx tailwindcss init
```

3. Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
```

4. Update `astro.config.mjs`:

```javascript
import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";

export default defineConfig({
  integrations: [tailwind()],
});
```

5. Create `src/styles/global.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    font-family: "Inter", sans-serif;
  }
}
```

#### Usage

```astro
---
import '../styles/global.css';
---

<div class="bg-gray-100 p-6 rounded-lg">
  <h1 class="text-2xl font-bold text-gray-800">
    Hello Tailwind!
  </h1>
  <p class="mt-2 text-gray-600">
    Styled with utility classes
  </p>
</div>
```

### Styled Components

#### Installation

```bash
npx astro add styled-components
```

#### Usage

```astro
---
import styled from 'styled-components';

const Button = styled.button`
  background: ${props => props.primary ? '#bf0f8b' : 'white'};
  color: ${props => props.primary ? 'white' : '#bf0f8b'};
  font-size: 1em;
  padding: 0.5em 1em;
  border: 2px solid #bf0f8b;
  border-radius: 3px;
  cursor: pointer;

  &:hover {
    opacity: 0.8;
  }
`;
---

<div>
  <Button>Normal Button</Button>
  <Button primary>Primary Button</Button>
</div>
```

## Content Integrations

### MDX

#### Installation

```bash
npx astro add mdx
```

#### Manual Setup

1. Install dependencies:

```bash
npm install @astrojs/mdx
```

2. Update `astro.config.mjs`:

```javascript
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";

export default defineConfig({
  integrations: [mdx()],
});
```

#### Usage

````mdx
---
// src/pages/blog/post.mdx
import Counter from '../../components/Counter.jsx';

export const title = 'My MDX Post';
export const pubDate = '2024-01-01';
---

# {title}

Published: {pubDate}

This is an MDX file with React components:

<Counter client:load />

## Code Examples

```js
console.log("Hello MDX!");
```
````

````

### Content Collections with MDX

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { blog };
````

```mdx
---
// src/content/blog/my-post.mdx
title: 'My Blog Post'
pubDate: 2024-01-01
tags: ['astro', 'mdx']
---

import { Chart } from "@astrojs/chart";

# My Blog Post

<Chart client:load data={[1, 2, 3, 4]} />
```

## Database Integrations

### Prisma

1. Install dependencies:

```bash
npm install prisma @prisma/client
npm install -D prisma
```

2. Initialize Prisma:

```bash
npx prisma init
```

3. Create schema:

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

4. Create client instance:

```typescript
// src/lib/prisma.ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export default prisma;
```

5. Use in Astro pages:

```astro
---
import prisma from '@/lib/prisma';

const posts = await prisma.post.findMany({
  orderBy: { createdAt: 'desc' },
  take: 10,
});
---

{posts.map(post => (
  <article>
    <h2>{post.title}</h2>
    <p>{post.content}</p>
  </article>
))}
```

## API Integrations

### GraphQL (with Apollo Client)

1. Install dependencies:

```bash
npm install @apollo/client graphql
npm install -D @types/graphql
```

2. Create Apollo provider:

```astro
---
// src/providers/ApolloProvider.astro
import { ApolloClient, InMemoryCache } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://your-graphql-api.com/graphql',
  cache: new InMemoryCache(),
});

<script define:vars={{ client }}>
  window.__APOLLO_CLIENT__ = client;
</script>

<slot />
```

3. Create GraphQL query component:

```jsx
// src/components/PostList.jsx
import { useQuery, gql } from "@apollo/client";
import client from "../lib/apollo-client";

const GET_POSTS = gql`
  query GetPosts {
    posts {
      id
      title
      content
    }
  }
`;

export default function PostList() {
  const { loading, error, data } = useQuery(GET_POSTS, {
    client: window.__APOLLO_CLIENT__,
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      {data.posts.map((post) => (
        <article key={post.id}>
          <h3>{post.title}</h3>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  );
}
```

## Authentication Integrations

### Auth.js (NextAuth)

1. Install dependencies:

```bash
npm install @auth/core
```

2. Create auth API route:

```javascript
// src/pages/api/auth/[...auth].js
import { Auth } from "@auth/core";
import GitHub from "@auth/core/providers/github";

export const { GET, POST } = Auth({
  providers: [
    GitHub({
      clientId: import.meta.env.GITHUB_ID,
      clientSecret: import.meta.env.GITHUB_SECRET,
    }),
  ],
  secret: import.meta.env.AUTH_SECRET,
  trustHost: true,
});
```

3. Create auth utilities:

```typescript
// src/lib/auth.ts
export async function getSession(request: Request) {
  const url = new URL("/api/auth/session", request.url);
  const response = await fetch(url, {
    headers: { cookie: request.headers.get("cookie") ?? "" },
  });
  return response.json();
}
```

4. Protect routes:

```astro
---
// src/pages/dashboard.astro
import { getSession } from '@/lib/auth';

const session = await getSession(Astro.request);

if (!session?.user) {
  return Astro.redirect('/login');
}
---

<h1>Welcome, {session.user.name}!</h1>
```

## Deployment Integrations

### Vercel

1. Install adapter:

```bash
npm install @astrojs/vercel
```

2. Update config:

```javascript
// astro.config.mjs
import { defineConfig } from "astro/config";
import vercel from "@astrojs/vercel/serverless";

export default defineConfig({
  output: "server",
  adapter: vercel(),
});
```

3. Environment variables (in Vercel dashboard):

```
DATABASE_URL=
AUTH_SECRET=
GITHUB_ID=
GITHUB_SECRET=
```

### Netlify

1. Install adapter:

```bash
npm install @astrojs/netlify
```

2. Update config:

```javascript
// astro.config.mjs
import { defineConfig } from "astro/config";
import netlify from "@astrojs/netlify/functions";

export default defineConfig({
  output: "server",
  adapter: netlify(),
});
```

3. Create Netlify redirects:

```
# netlify.toml
[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 404
```

## Development Tools

### Storybook (for UI components)

1. Install dependencies:

```bash
npm install -D @storybook/addon-essentials @storybook/addon-interactions @storybook/blocks storybook @storybook/addon-astro
```

2. Initialize Storybook:

```bash
npx storybook@latest init
```

3. Configure `.storybook/main.js`:

```javascript
module.exports = {
  stories: ["../src/**/*.stories.@(js|jsx|ts|tsx|mdx)"],
  addons: ["@storybook/addon-essentials"],
  framework: {
    name: "@storybook/addon-astro",
    options: {},
  },
};
```

### Vitest (for testing)

1. Install dependencies:

```bash
npm install -D vitest @vitest/ui jsdom
```

2. Configure `vitest.config.ts`:

```typescript
import { defineConfig } from "vitest/config";
import astro from "astro/config";

export default defineConfig({
  test: {
    environment: "jsdom",
  },
});
```

3. Create test:

```typescript
// src/components/Button.test.tsx
import { test, expect } from 'vitest';
import { render } from '@testing-library/react';
import Button from './Button';

test('renders button with text', () => {
  const { getByText } = render(<Button>Click me</Button>);
  expect(getByText('Click me')).toBeInTheDocument();
});
```

## Common Issues and Solutions

### Hydration Mismatches

Problem: Content differs between server and client render
Solution: Ensure consistent data or use client-only components

```astro
---
import { useClientOnly } from '@astroHooks/useClientOnly';
---

<ClientOnly fallback={<div>Loading...</div>}>
  <SomeReactComponent client:load />
</ClientOnly>
```

### Import Paths

Problem: Relative imports become unwieldy
Solution: Use path aliases

```javascript
// astro.config.mjs
export default defineConfig({
  vite: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
        "@/components": path.resolve(__dirname, "./src/components"),
      },
    },
  },
});
```

### Bundle Size

Problem: Large JavaScript bundles
Solution: Code splitting and dynamic imports

```javascript
// Lazy load components
const HeavyComponent = lazy(() => import("./HeavyComponent"));

// Use with Suspense in React
<Suspense fallback={<Loading />}>
  <HeavyComponent />
</Suspense>;
```

This integration guide helps you properly set up and configure various integrations for your Astro projects.
