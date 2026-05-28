---
name: Modern Stack Expert
description: Comprehensive guide and best practices for Next.js, Expo, Convex, NestJS, and modern UI/UX design.
---

# Modern Stack Expert

This skill equips the agent with expert-level knowledge in the modern web and mobile development stack: **Next.js (App Router), Expo (React Native), Convex, NestJS, and Tailwind CSS**. It emphasizes performance, scalability, and high-quality UI/UX design.

## 1. Next.js & React Best Practices (Vercel Standards)

Adhere to these critical performance rules derived from Vercel's engineering practices.

### 1.1 Eliminating Waterfalls

**Impact: CRITICAL (2-10× improvement)**

- **Defer Await**: Move `await` operations into the branches where they are actually used.
- **Parallelize**: Use `Promise.all()` for independent operations.
- **Component Composition**: In RSCs, avoid blocking parent components with data fetching if children can fetch independently.

**Incorrect (Sequential):**

```typescript
const user = await fetchUser();
const posts = await fetchPosts(); // Waits for user
```

**Correct (Parallel):**

```typescript
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()]);
```

### 1.2 Bundle Size Optimization

**Impact: CRITICAL**

- **Avoid Barrel Files**: Import directly from source files (e.g., `import Button from '@mui/material/Button'`) unless using a bundler that optimizes this automatically (Next.js 13.5+ does for some libs).
- **Lazy Loading**: Use `next/dynamic` for heavy components that are not critical for the initial paint (e.g., Modals, Charts).
- **Defer Non-Critical Libs**: Load analytics or heavy client-side libraries after hydration or on interaction.

### 1.3 Server-Side Performance

**Impact: HIGH**

- **Minimize Serialization**: Only pass the fields needed by the client component from an RSC. Passing full objects bloats the HTML.
- **Deduplication**: Use `React.cache()` for per-request deduplication of data fetching functions.

### 1.4 Re-render Optimization

**Impact: MEDIUM**

- **Narrow Dependencies**: In `useEffect`, depend on primitives (`user.id`) rather than objects (`user`).
- **Derived State**: Calculate values during render / in the body of the function, not in `useEffect`.
- **Composition**: Push state down or lift content up to avoid re-rendering heavy sub-trees.

## 2. Convex Best Practices (Real-time Database)

### 2.1 Query & Mutation Efficiency

- **Reactivity**: Rely on Convex's automatic reactivity. Do not manually refetch data in `useEffect`.
- **Arguments**: Pass specific arguments to queries. Querying "all" and filtering on the client is an anti-pattern.
- **Indexing**: Always define indexes in `schema.ts` for fields used in `q.eq()` filters to ensure scalable performance.

**Incorrect:**

```typescript
// Client filtering (Slow)
const allUsers = useQuery(api.users.list);
const activeUsers = allUsers?.filter((u) => u.isActive);
```

**Correct:**

```typescript
// Server filtering (Fast)
const activeUsers = useQuery(api.users.listActive);
```

### 2.2 Security & Validation

- **Authentication**: Always check `ctx.auth.getUserIdentity()` in mutations/queries that access private data.
- **Zod/Validator**: Use `v` from `convex/values` to strictly validate all arguments.

## 3. Expo & React Native Best Practices

### 3.1 List Performance

**Impact: HIGH**

- **Use FlashList**: Replace `FlatList` with Shopify's `FlashList` for significantly better recycling and performance on long lists.

### 3.2 Image Optimization

- **Use expo-image**: Prefer `expo-image` over the standard `<Image />` component for better caching, blur-hash support, and performance.

### 3.3 Platform Specifics

- **File Extensions**: Use `.ios.tsx` and `.android.tsx` for platform-specific implementations of complex components.
- **Safe Area**: Always use `SafeAreaProvider` and `useSafeAreaInsets` instead of hardcoded top/bottom padding.

## 4. NestJS Best Practices (Backend Architecture)

### 4.1 Architecture

- **Modular Design**: Organize code by "Domain" (User, Auth, Payment) modules, not by technical layer (Controllers, Services).
- **DTOs**: Strict Data Transfer Objects with `class-validator` are mandatory for all Controller inputs.

### 4.2 Dependency Injection

- **Inversion of Control**: Never manually instantiate services (e.g., `new UserService()`). Always inject via the constructor.

## 5. UI/UX & Design Excellence

### 5.1 The "WOW" Factor

- **Aesthetics**: Use rich, harmonious color palettes (HSL). Avoid raw CSS colors like `red`, `blue`.
- **Motion**: Implement subtle micro-interactions using `framer-motion` (web) or `react-native-reanimated` (mobile). Elements should fade in, slide up, or scale gently.
- **Glassmorphism**: Use backdrops, blurs, and translucent layers to create depth.

### 5.2 Tailwind CSS

- **Utility First**: Use standard Tailwind utilities. Avoid arbitraries (`w-[123px]`) unless absolutely necessary.
- **Class Merging**: Always use a `cn()` helper (clsx + tailwind-merge) for conditional classes and reusable components.

## 6. Implementation Workflow for Agent

1.  **Analyze**: Determine which part of the stack is involved (Frontend vs Backend vs Mobile).
2.  **Plan**: Draft a mental model of the component/feature using these best practices.
3.  **Execute**: Write code that defaults to the "Correct" examples above.
    - _Check_: Am I creating a waterfall?
    - _Check_: Is this component too heavy?
    - _Check_: Is the UI "premium" enough?
4.  **Review**: Self-correct against the "Incorrect" patterns before finalizing.
