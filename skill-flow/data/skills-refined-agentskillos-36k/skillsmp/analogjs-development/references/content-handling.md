# Content Handling

Comprehensive guide for Analogjs markdown content management.

## Table of Contents

- [Content Setup](#content-setup)
- [Content Attributes](#content-attributes)
- [Content List](#content-list)
- [Single Content](#single-content)
- [Markdown Rendering](#markdown-rendering)
- [Prerender Configuration](#prerender-configuration)

## Content Setup

### App Configuration

```typescript
// src/app/app.config.ts
import { ApplicationConfig } from '@angular/core';
import {
  provideHttpClient,
  withFetch,
  withInterceptors,
} from '@angular/common/http';
import {
  provideFileRouter,
  requestContextInterceptor,
} from '@analogjs/router';
import { provideContent, withMarkdownRenderer } from '@analogjs/content';
import { withShikiHighlighter } from '@analogjs/content/shiki-highlighter';

export const appConfig: ApplicationConfig = {
  providers: [
    provideFileRouter(),
    provideHttpClient(
      withFetch(),
      // WHY: requestContextInterceptor must be last
      withInterceptors([requestContextInterceptor])
    ),
    // WHY: provideContent enables markdown content handling
    provideContent(
      withMarkdownRenderer(),
      withShikiHighlighter()
    ),
  ],
};
```

### Content Directory Structure

```
src/
└── content/
    └── blog/
        ├── first-post.md
        ├── second-post.md
        └── third-post.md
```

## Content Attributes

### PostAttributes Interface

```typescript
// src/app/core/models/post-attributes.ts
export default interface PostAttributes {
  title: string;
  slug: string;
  date: string;
  description: string;
  coverImage?: string;
  tags?: string[];
  published?: boolean;
}
```

### Markdown Frontmatter

```markdown
---
title: My First Post
slug: first-post
date: 2024-01-15
description: This is my first blog post
coverImage: /images/first-post.jpg
tags:
  - angular
  - analogjs
published: true
---

# My First Post

Content goes here...
```

## Content List

### Using injectContentFiles

```typescript
// src/app/pages/blog/index.page.ts
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { injectContentFiles } from '@analogjs/content';
import PostAttributes from 'src/app/core/models/post-attributes';

@Component({
  selector: 'app-blog-index',
  imports: [RouterLink],
  template: `
    <h1>Blog</h1>
    <ul>
      @for (post of posts; track post.slug) {
        <li>
          <a [routerLink]="['/blog', post.slug]">
            {{ post.attributes.title }}
          </a>
          <time>{{ post.attributes.date }}</time>
        </li>
      } @empty {
        <li>No posts found</li>
      }
    </ul>
  `,
})
export default class BlogIndexPage {
  // WHY: injectContentFiles returns array of content files
  readonly posts = injectContentFiles<PostAttributes>((contentFile) =>
    contentFile.filename.includes('src/content/blog/')
  );
}
```

### Filtering and Sorting

```typescript
readonly posts = injectContentFiles<PostAttributes>((file) =>
  file.filename.includes('src/content/blog/')
)
  // WHY: Filter by published status
  .filter((post) => post.attributes.published !== false)
  // WHY: Sort by date descending
  .sort((a, b) =>
    new Date(b.attributes.date).getTime() -
    new Date(a.attributes.date).getTime()
  );
```

### Using contentFilesResource (Signal-based)

```typescript
import { contentFilesResource } from '@analogjs/content';

@Component({
  selector: 'app-blog-index',
  template: `
    @if (posts.isLoading()) {
      <p>Loading...</p>
    } @else {
      @for (post of posts.value(); track post.slug) {
        <article>{{ post.attributes.title }}</article>
      }
    }
  `,
})
export default class BlogIndexPage {
  // WHY: contentFilesResource provides signal-based reactive content
  readonly posts = contentFilesResource<PostAttributes>((file) =>
    file.filename.includes('src/content/blog/')
  );
}
```

## Single Content

### Using injectContent

```typescript
// src/app/pages/blog/[slug].page.ts
import { Component } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { injectContent, MarkdownComponent } from '@analogjs/content';
import PostAttributes from 'src/app/core/models/post-attributes';

@Component({
  selector: 'app-blog-post',
  imports: [AsyncPipe, MarkdownComponent],
  template: `
    @if (post$ | async; as post) {
      <article>
        <header>
          <h1>{{ post.attributes.title }}</h1>
          <time>{{ post.attributes.date }}</time>
        </header>
        <analog-markdown [content]="post.content" />
      </article>
    }
  `,
})
export default class BlogPostPage {
  // WHY: injectContent uses route param to find content
  readonly post$ = injectContent<PostAttributes>({
    param: 'slug',
    subdirectory: 'blog',
  });
}
```

### Using contentFileResource (Signal-based)

```typescript
import { contentFileResource } from '@analogjs/content';

@Component({
  selector: 'app-blog-post',
  template: `
    @if (post.isLoading()) {
      <p>Loading...</p>
    } @else if (post.value(); as p) {
      <article>
        <h1>{{ p.attributes.title }}</h1>
        <analog-markdown [content]="p.content" />
      </article>
    }
  `,
})
export default class BlogPostPage {
  // WHY: contentFileResource provides signal-based reactive single content
  readonly post = contentFileResource<PostAttributes>({
    param: 'slug',
    subdirectory: 'blog',
  });
}
```

## Markdown Rendering

### MarkdownComponent

```typescript
import { MarkdownComponent } from '@analogjs/content';

@Component({
  imports: [MarkdownComponent],
  template: `
    <!-- WHY: analog-markdown renders markdown content -->
    <analog-markdown [content]="post.content" />
  `,
})
export class PostComponent {}
```

### Shiki Highlighter Configuration

```typescript
// src/app/app.config.ts
import { withShikiHighlighter } from '@analogjs/content/shiki-highlighter';

provideContent(
  withMarkdownRenderer(),
  withShikiHighlighter({
    // WHY: Configure syntax highlighting themes and languages
    themes: ['github-dark', 'github-light'],
    langs: ['typescript', 'html', 'css', 'bash'],
  })
);
```

### Custom Markdown Components

```typescript
// Register custom component for markdown
import { withMarkdownRenderer } from '@analogjs/content';
import { CustomCodeComponent } from './custom-code.component';

provideContent(
  withMarkdownRenderer({
    loadMermaid: () => import('mermaid'),
  })
);
```

## Prerender Configuration

### Basic Prerender Setup

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import analog from '@analogjs/platform';

export default defineConfig({
  plugins: [
    analog({
      prerender: {
        routes: [
          '/',
          '/about',
          '/blog',
        ],
      },
    }),
  ],
});
```

### Dynamic Content Prerender

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [
    analog({
      prerender: {
        routes: async () => [
          '/',
          '/about',
          '/blog',
          // WHY: contentDir with transform generates routes from content files
          {
            contentDir: 'src/content/blog',
            transform: (file) => `/blog/${file.attributes['slug']}`,
          },
        ],
      },
    }),
  ],
});
```

### Filtering Content for Prerender

```typescript
{
  contentDir: 'src/content/blog',
  transform: (file) => {
    // WHY: Skip draft posts from prerendering
    if (file.attributes['published'] === false) {
      return false;
    }
    return `/blog/${file.attributes['slug']}`;
  },
}
```

### Sitemap Generation

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [
    analog({
      prerender: {
        routes: async () => [...],
        sitemap: {
          host: 'https://example.com',
        },
      },
    }),
  ],
});
```

### SSR Configuration

```typescript
// src/main.server.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideServerRendering } from '@angular/platform-server';
import { provideServerContext } from '@analogjs/router/server';
import { AppComponent } from './app/app';
import { appConfig } from './app/app.config';

export default () =>
  bootstrapApplication(AppComponent, {
    providers: [
      ...appConfig.providers,
      provideServerRendering(),
      // WHY: provideServerContext enables SSR context access
      provideServerContext(),
    ],
  });
```
