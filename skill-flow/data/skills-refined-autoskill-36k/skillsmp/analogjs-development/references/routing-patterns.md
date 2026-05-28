# Routing Patterns

Comprehensive guide for Analogjs file-based routing.

## Table of Contents

- [Page Components](#page-components)
- [Dynamic Routes](#dynamic-routes)
- [Route Groups](#route-groups)
- [Route Metadata](#route-metadata)
- [Layouts](#layouts)
- [API Routes](#api-routes)

## Page Components

### Basic Page Component

```typescript
// src/app/pages/index.page.ts
import { Component } from '@angular/core';

// WHY: Default export is required for Analogjs routing
@Component({
  selector: 'app-home',
  template: `
    <main>
      <h1>Welcome</h1>
    </main>
  `,
})
export default class HomePage {}
```

### Page with External Template

```typescript
// src/app/pages/about/index.page.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './index.page.html',
  styleUrl: './index.page.css',
})
export default class AboutPage {}
```

### Route Mapping

```
File Path                           → URL Route
src/app/pages/index.page.ts         → /
src/app/pages/about/index.page.ts   → /about
src/app/pages/blog/index.page.ts    → /blog
src/app/pages/blog/[slug].page.ts   → /blog/:slug
src/app/pages/(auth)/login.page.ts  → /login (grouped)
```

## Dynamic Routes

### Basic Dynamic Route

```typescript
// src/app/pages/blog/[slug].page.ts
import { Component } from '@angular/core';
import { injectContent } from '@analogjs/content';
import { MarkdownComponent } from '@analogjs/content';
import { AsyncPipe } from '@angular/common';
import PostAttributes from 'src/app/core/models/post-attributes';

// WHY: Bracket syntax creates dynamic route parameter
@Component({
  selector: 'app-blog-post',
  imports: [MarkdownComponent, AsyncPipe],
  template: `
    @if (post$ | async; as post) {
      <article>
        <h1>{{ post.attributes.title }}</h1>
        <analog-markdown [content]="post.content" />
      </article>
    }
  `,
})
export default class BlogPostPage {
  // WHY: injectContent() automatically uses 'slug' route param
  readonly post$ = injectContent<PostAttributes>({
    param: 'slug',
    subdirectory: 'blog',
  });
}
```

### Route Param as Input

```typescript
// src/app/pages/users/[id].page.ts
import { Component, input, inject } from '@angular/core';
import { UserService } from 'src/app/core/services/user.service';

@Component({
  selector: 'app-user-detail',
  template: `...`,
})
export default class UserDetailPage {
  // WHY: withComponentInputBinding() enables route params as inputs
  readonly id = input.required<string>();

  private readonly userService = inject(UserService);

  // Use id() to access the route parameter
}
```

### Multiple Dynamic Segments

```typescript
// src/app/pages/[category]/[slug].page.ts
@Component({
  selector: 'app-category-post',
  template: `...`,
})
export default class CategoryPostPage {
  readonly category = input.required<string>();
  readonly slug = input.required<string>();
}
```

## Route Groups

### Grouping Without URL Segment

```
src/app/pages/
├── (auth)/
│   ├── login.page.ts      → /login
│   └── register.page.ts   → /register
├── (dashboard)/
│   ├── index.page.ts      → /
│   └── settings.page.ts   → /settings
```

```typescript
// src/app/pages/(auth)/login.page.ts
// WHY: Parentheses create route group without URL segment
@Component({
  selector: 'app-login',
  template: `...`,
})
export default class LoginPage {}
```

## Route Metadata

### Basic Route Metadata

```typescript
// src/app/pages/about/index.page.ts
import { RouteMeta } from '@analogjs/router';

// WHY: routeMeta export configures route-level settings
export const routeMeta: RouteMeta = {
  title: 'About - My Site',
  meta: [
    { name: 'description', content: 'Learn more about us' },
    { property: 'og:title', content: 'About Us' },
  ],
};

@Component({
  selector: 'app-about',
  template: `...`,
})
export default class AboutPage {}
```

### Route Guards

```typescript
import { RouteMeta } from '@analogjs/router';
import { authGuard } from 'src/app/core/guards/auth.guard';

export const routeMeta: RouteMeta = {
  title: 'Dashboard',
  canActivate: [authGuard],
};
```

### SSR Options

```typescript
export const routeMeta: RouteMeta = {
  title: 'Client Only Page',
  meta: [{ name: 'description', content: 'This page is client-only' }],
  // WHY: Disable SSR for specific routes
  providers: [],
  data: {
    ssr: false,
  },
};
```

## Layouts

### Layout Route

```typescript
// src/app/pages/+layout.page.ts
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

// WHY: +layout.page.ts creates shared layout for child routes
@Component({
  selector: 'app-layout',
  imports: [RouterOutlet],
  template: `
    <header>
      <nav><!-- Navigation --></nav>
    </header>
    <main>
      <router-outlet />
    </main>
    <footer><!-- Footer --></footer>
  `,
})
export default class LayoutPage {}
```

### Nested Layout

```
src/app/pages/
├── +layout.page.ts           # Root layout
├── index.page.ts
└── dashboard/
    ├── +layout.page.ts       # Dashboard layout
    ├── index.page.ts
    └── settings.page.ts
```

## API Routes

### Basic API Route

```typescript
// src/server/routes/api/hello.ts
import { defineEventHandler } from 'h3';

// WHY: defineEventHandler creates API endpoint
export default defineEventHandler(() => {
  return { message: 'Hello from API' };
});

// Route: GET /api/hello
```

### API with Parameters

```typescript
// src/server/routes/api/users/[id].ts
import { defineEventHandler, getRouterParam } from 'h3';

export default defineEventHandler((event) => {
  const id = getRouterParam(event, 'id');
  // Fetch user by id
  return { id, name: 'John Doe' };
});

// Route: GET /api/users/:id
```

### API with Body

```typescript
// src/server/routes/api/users.post.ts
import { defineEventHandler, readBody } from 'h3';

// WHY: .post.ts suffix creates POST endpoint
export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  // Create user
  return { success: true, user: body };
});

// Route: POST /api/users
```

### HTTP Methods

```
File Name              → HTTP Method
users.ts               → GET
users.post.ts          → POST
users.put.ts           → PUT
users.patch.ts         → PATCH
users.delete.ts        → DELETE
```
