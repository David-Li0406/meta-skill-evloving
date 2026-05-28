# Astro Component Patterns

This reference provides common patterns and best practices for building Astro components.

## Container/Presentation Pattern

Separate data-fetching logic from presentation components:

```astro
---
// Container component - handles data fetching
import BlogPostCard from '@/components/BlogPostCard.astro';
import { getCollection } from 'astro:content';

const posts = await getCollection('blog');
const recentPosts = posts.slice(0, 3);
---

<section>
  <h2>Recent Posts</h2>
  <div class="grid">
    {recentPosts.map((post) => (
      <BlogPostCard post={post} />
    ))}
  </div>
</section>
```

```astro
---
// Presentation component - only displays data
export interface Props {
  post: {
    slug: string;
    data: {
      title: string;
      description: string;
      pubDate: Date;
    };
  };
}

const { post } = Astro.props;
const { data } = post;
---

<article class="card">
  <h3>{data.title}</h3>
  <p>{data.description}</p>
  <time>{data.pubDate.toLocaleDateString()}</time>
</article>
```

## Compound Component Pattern

Create components that work together:

```astro
---
// src/components/Card/Card.astro
interface Props {
  className?: string;
  variant?: 'default' | 'elevated' | 'outlined';
}

const { className, variant = 'default' } = Astro.props;

const variantClasses = {
  default: 'bg-white dark:bg-gray-800 rounded-lg shadow-sm',
  elevated: 'bg-white dark:bg-gray-800 rounded-lg shadow-lg',
  outlined: 'bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700'
};
---

<div class={`${variantClasses[variant]} ${className || ''}`}>
  <slot />
</div>
```

```astro
---
// src/components/Card/CardHeader.astro
interface Props {
  className?: string;
  padding?: 'sm' | 'md' | 'lg';
}

const { className, padding = 'md' } = Astro.props;

const paddingClasses = {
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6'
};
---

<header class={`border-b border-gray-200 dark:border-gray-700 ${paddingClasses[padding]} ${className || ''}`}>
  <slot />
</header>
```

```astro
---
// src/components/Card/CardBody.astro
interface Props {
  className?: string;
  padding?: 'sm' | 'md' | 'lg';
}

const { className, padding = 'md' } = Astro.props;

const paddingClasses = {
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6'
};
---

<div class={`${paddingClasses[padding]} ${className || ''}`}>
  <slot />
</div>
```

Usage:

```astro
---
import Card from '@/components/Card/Card.astro';
import CardHeader from '@/components/Card/CardHeader.astro';
import CardBody from '@/components/Card/CardBody.astro';
---

<Card>
  <CardHeader>
    <h2>Card Title</h2>
  </CardHeader>
  <CardBody>
    <p>Card content goes here</p>
  </CardBody>
</Card>
```

## Render Props Pattern

Pass render functions as props:

```astro
---
// src/components/DataFetcher.astro
export interface Props {
  url: string;
  render: (data: any) => any;
}

const { url, render } = Astro.props;
let data;
let error;

try {
  const response = await fetch(url);
  data = await response.json();
} catch (e) {
  error = e;
}
---

{error ? (
  <p>Error loading data</p>
) : (
  render(data)
)}
```

Usage:

```astro
---
import DataFetcher from '@/components/DataFetcher.astro';
---

<DataFetcher
  url="/api/posts"
  render={(posts) => (
    <ul>
      {posts.map((post) => (
        <li>{post.title}</li>
      ))}
    </ul>
  )}
/>
```

## Higher-Order Component Pattern

Wrap components with additional functionality:

```astro
---
// src/components/withLoading.astro
export interface Props {
  component: any;
  loading?: boolean;
  [key: string]: any;
}

const { component: Component, loading = false, ...props } = Astro.props;
---

{loading ? (
  <div class="flex items-center justify-center p-8">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 dark:border-blue-400 mr-3"></div>
    <span class="text-gray-600 dark:text-gray-400">Loading...</span>
  </div>
) : (
  <Component {...props} />
)}
```

## Context Provider Pattern

Share state across components:

```astro
---
// src/providers/UserProvider.astro
export interface Props {
  user?: {
    id: string;
    name: string;
    email: string;
  };
}

const { user } = Astro.props;
---

<script define:vars={{ user }}>
  export const userContext = user;
</script>

<slot />
```

```astro
---
// src/components/UserProfile.astro
<script>
  import { userContext } from '../providers/UserProvider.astro';

  // Access user context
  console.log('Current user:', userContext);
</script>

<div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm max-w-md mx-auto">
  <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">User Profile</h2>
  <div id="user-info" class="text-gray-600 dark:text-gray-400"></div>
</div>

<script>
  document.getElementById('user-info').textContent =
    userContext ? `Logged in as ${userContext.name}` : 'Not logged in';
</script>
```

## Layout Component Pattern

Create flexible layouts with slots:

```astro
---
// src/layouts/MainLayout.astro
export interface Props {
  title: string;
  description?: string;
  noHeader?: boolean;
  noFooter?: boolean;
}

const { title, description, noHeader, noFooter } = Astro.props;
---

<html lang="en" class="h-full">
  <head>
    <title>{title}</title>
    {description && <meta name="description" content={description} />}
  </head>
  <body class="h-full m-0 font-sans leading-relaxed text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-900">
    <div class="flex flex-col min-h-screen">
      {!noHeader && (
        <header class="sticky top-0 z-50 border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg">
          <slot name="header" />
        </header>
      )}

      <main class="grow px-4 py-4 md:px-8 md:py-8 max-w-6xl mx-auto w-full">
        <slot />
      </main>

      {!noFooter && (
        <footer class="border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 mt-auto">
          <slot name="footer">
            <div class="text-center p-4">
              <p>&copy; 2024 Your Company</p>
            </div>
          </slot>
        </footer>
      )}
    </div>
  </body>
</html>
```

Usage:

```astro
---
import MainLayout from '@/layouts/MainLayout.astro';
import Header from '@/components/Header.astro';
import Navigation from '@/components/Navigation.astro';
---

<MainLayout
  title="About Us"
  description="Learn about our company"
>
  <slot slot="header">
    <Header>
      <Navigation />
    </Header>
  </slot>

  <section class="py-16 px-4">
    <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-6">About Our Company</h1>
    <p class="text-lg text-gray-600 dark:text-gray-400 max-w-3xl">We make amazing products...</p>
  </section>

  <slot slot="footer">
    <p>Custom footer content</p>
  </slot>
</MainLayout>
```

## Conditional Rendering Patterns

### Multiple Conditions

```astro
---
// Using ternary operators
const isAdmin = user?.role === 'admin';
const isAuthenticated = !!user;

{isAuthenticated ? (
  isAdmin ? <AdminPanel /> : <UserDashboard />
) : (
  <LoginForm />
)}
```

### Show/Hide Pattern

```astro
---
// Using boolean attributes
interface Props {
  show?: boolean;
  hide?: boolean;
  children: any;
}

const { show = true, hide = false, children } = Astro.props;
const shouldShow = show && !hide;
---

{shouldShow && children}
```

## List Rendering Patterns

### With Index

```astro
---
const items = ['Apple', 'Banana', 'Cherry'];
---

<ul>
  {items.map((item, index) => (
    <li data-index={index}>
      {index + 1}. {item}
    </li>
  ))}
</ul>
```

### With Conditional Rendering

```astro
---
const posts = [
  { title: 'Post 1', featured: true },
  { title: 'Post 2', featured: false },
  { title: 'Post 3', featured: true },
];
---

<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
  {posts.map((post) => (
    <article class={`p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm ${post.featured ? 'ring-2 ring-blue-500 dark:ring-blue-400' : ''}`}>
      <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">{post.title}</h2>
      {post.featured && <span class="inline-block px-3 py-1 text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30 rounded-full">Featured</span>}
    </article>
  ))}
</div>
```

## Form Component Pattern

```astro
---
// src/components/Form/Form.astro
export interface Props {
  action: string;
  method?: 'GET' | 'POST';
  className?: string;
}

const { action, method = 'POST', className } = Astro.props;
---

<form action={action} method={method} class={className}>
  <slot />
</form>
```

```astro
---
// src/components/Form/FormField.astro
export interface Props {
  label: string;
  name: string;
  type?: string;
  required?: boolean;
  error?: string;
}

const { label, name, type = 'text', required, error } = Astro.props;
---

<div class="mb-4">
  <label for={name} class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
    {label}
    {required && <span class="text-red-500">*</span>}
  </label>
  <input
    id={name}
    name={name}
    type={type}
    required={required}
    class={`w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white ${error ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : ''}`}
  />
  {error && <span class="text-red-500 text-sm mt-1">{error}</span>}
</div>
```

Usage:

```astro
---
import Form from '@/components/Form/Form.astro';
import FormField from '@/components/Form/FormField.astro';
import SubmitButton from '@/components/Form/SubmitButton.astro';
---

<Form action="/contact" method="POST">
  <FormField
    label="Name"
    name="name"
    required
    error={errors?.name}
  />
  <FormField
    label="Email"
    name="email"
    type="email"
    required
    error={errors?.email}
  />
  <FormField
    label="Message"
    name="message"
    type="textarea"
    required
  />
  <SubmitButton>Send Message</SubmitButton>
</Form>
```

## Best Practices

1. **Use TypeScript interfaces** for props to ensure type safety
2. **Keep components focused** on a single responsibility
3. **Use slots** for flexible content composition
4. **Use Tailwind CSS classes** for consistent styling
5. **Extract repeated logic** into utility functions
6. **Document complex components** with JSDoc comments
7. **Use semantic HTML** elements for accessibility
8. **Test components** in isolation when possible

## Tailwind CSS Tips

1. **Variant-based styling**: Create variant objects for different component styles
2. **Responsive design**: Use Tailwind's responsive prefixes (sm:, md:, lg:, xl:)
3. **Dark mode**: Leverage Tailwind's dark mode support with `dark:` prefix
4. **Component composition**: Combine utility classes for complex designs
5. **Consistent spacing**: Use Tailwind's spacing scale consistently
6. **Custom colors**: Define brand colors in your Tailwind config
7. **Animation**: Use Tailwind's animation utilities for transitions
