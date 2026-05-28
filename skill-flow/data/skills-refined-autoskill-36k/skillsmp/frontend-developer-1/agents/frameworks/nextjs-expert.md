---
name: Next.js Expert
description: Expert Next.js 14+ - App Router, Server Components, SSR, SSG et API Routes
---

# Agent Next.js Expert

## Responsabilité

Maîtriser Next.js pour créer des applications React fullstack avec rendu serveur et optimisations intégrées.

## Tu NE fais PAS

- ❌ Implémenter les détails React (hooks complexes, patterns) → skill `react-expert`
- ❌ Gérer le state management global (Zustand, Redux) → `state-management/` ou `react-expert/state/`
- ❌ Optimiser les performances générales (memoization, virtualization) → `performance/`
- ❌ Configurer CI/CD et déploiement → skill `devops`

## Structure App Router

```
app/
├── layout.tsx          # Layout racine
├── page.tsx            # Page d'accueil (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── globals.css
├── (auth)/             # Route group (pas dans l'URL)
│   ├── login/
│   │   └── page.tsx    # /login
│   └── register/
│       └── page.tsx    # /register
├── dashboard/
│   ├── layout.tsx      # Layout dashboard
│   ├── page.tsx        # /dashboard
│   └── settings/
│       └── page.tsx    # /dashboard/settings
├── blog/
│   ├── page.tsx        # /blog
│   └── [slug]/
│       └── page.tsx    # /blog/[slug]
├── api/
│   └── users/
│       └── route.ts    # API: /api/users
└── @modal/             # Parallel route
    └── (.)photo/[id]/
        └── page.tsx    # Intercepted route
```

## Server Components vs Client Components

### Server Component (défaut)

```tsx
// app/users/page.tsx
// Par défaut, tous les composants sont Server Components

import { db } from '@/lib/db';

// Peut directement accéder à la DB
export default async function UsersPage() {
  const users = await db.user.findMany();

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Client Component

```tsx
'use client';

// Nécessaire pour : hooks React, event handlers, browser APIs

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### Pattern de composition

```tsx
// app/dashboard/page.tsx (Server Component)
import { db } from '@/lib/db';
import { InteractiveChart } from '@/components/InteractiveChart';

export default async function DashboardPage() {
  const data = await db.analytics.getStats();

  return (
    <div>
      <h1>Dashboard</h1>
      {/* Passer les données serveur au Client Component */}
      <InteractiveChart data={data} />
    </div>
  );
}

// components/InteractiveChart.tsx
'use client';

export function InteractiveChart({ data }: { data: Stats }) {
  // Interactivité côté client avec données serveur
  return <Chart data={data} />;
}
```

## Data Fetching

### Fetch avec cache

```tsx
// Par défaut, fetch est caché et dédupliqué
async function getUser(id: string) {
  const res = await fetch(`https://api.example.com/users/${id}`);
  return res.json();
}

// Options de cache
await fetch(url, { cache: 'force-cache' }); // Défaut
await fetch(url, { cache: 'no-store' }); // Pas de cache
await fetch(url, { next: { revalidate: 3600 } }); // ISR: revalider chaque heure
await fetch(url, { next: { tags: ['users'] } }); // Tag pour invalidation
```

### generateStaticParams (SSG)

```tsx
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await getPosts();

  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export default async function BlogPost({
  params,
}: {
  params: { slug: string };
}) {
  const post = await getPost(params.slug);
  return <article>{post.content}</article>;
}
```

### generateMetadata

```tsx
import type { Metadata } from 'next';

// Metadata statique
export const metadata: Metadata = {
  title: 'Mon Site',
  description: 'Description du site',
};

// Metadata dynamique
export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      images: [post.coverImage],
    },
  };
}
```

## Layouts et Templates

### Root Layout (obligatoire)

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: {
    template: '%s | Mon Site',
    default: 'Mon Site',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <header>Navigation</header>
        <main>{children}</main>
        <footer>Footer</footer>
      </body>
    </html>
  );
}
```

### Nested Layout

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      <aside>Sidebar</aside>
      <section>{children}</section>
    </div>
  );
}
```

### Template (re-render à chaque navigation)

```tsx
// app/dashboard/template.tsx
export default function Template({ children }: { children: React.ReactNode }) {
  // Recrée l'état à chaque navigation
  return <div className="animate-in">{children}</div>;
}
```

## Loading et Error States

### Loading UI

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <div className="skeleton">Chargement...</div>;
}

// Avec Suspense manuel
import { Suspense } from 'react';

export default function Page() {
  return (
    <Suspense fallback={<LoadingSkeleton />}>
      <SlowComponent />
    </Suspense>
  );
}
```

### Error Handling

```tsx
// app/dashboard/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Une erreur est survenue</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Réessayer</button>
    </div>
  );
}
```

### Not Found

```tsx
// app/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>404 - Page non trouvée</h2>
      <Link href="/">Retour à l'accueil</Link>
    </div>
  );
}

// Trigger manuel
import { notFound } from 'next/navigation';

export default async function Page({ params }: { params: { id: string } }) {
  const item = await getItem(params.id);
  if (!item) notFound();

  return <div>{item.name}</div>;
}
```

## API Routes (Route Handlers)

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = searchParams.get('page') || '1';

  const users = await db.user.findMany({
    skip: (parseInt(page) - 1) * 10,
    take: 10,
  });

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await db.user.create({
    data: body,
  });

  return NextResponse.json(user, { status: 201 });
}

// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await db.user.delete({
    where: { id: params.id },
  });

  return new NextResponse(null, { status: 204 });
}
```

## Server Actions

```tsx
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const post = await db.post.create({
    data: { title, content },
  });

  revalidatePath('/posts');
  redirect(`/posts/${post.id}`);
}

export async function deletePost(id: string) {
  await db.post.delete({ where: { id } });
  revalidateTag('posts');
}
```

```tsx
// app/posts/new/page.tsx
import { createPost } from '@/app/actions';

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Titre" required />
      <textarea name="content" placeholder="Contenu" required />
      <button type="submit">Créer</button>
    </form>
  );
}
```

## Middleware

```tsx
// middleware.ts (à la racine)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Vérifier l'authentification
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Ajouter des headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');

  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

## Optimisations

### Image Component

```tsx
import Image from 'next/image';

export default function Avatar() {
  return (
    <Image
      src="/avatar.jpg"
      alt="Avatar"
      width={100}
      height={100}
      priority // Pour LCP
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  );
}

// Image responsive
<Image
  src="/hero.jpg"
  alt="Hero"
  fill
  sizes="(max-width: 768px) 100vw, 50vw"
  className="object-cover"
/>
```

### Link Component

```tsx
import Link from 'next/link';

// Prefetch automatique en viewport
<Link href="/about">À propos</Link>

// Désactiver prefetch
<Link href="/large-page" prefetch={false}>Large Page</Link>

// Navigation programmatique
'use client';
import { useRouter } from 'next/navigation';

export function LogoutButton() {
  const router = useRouter();

  async function logout() {
    await signOut();
    router.push('/login');
    router.refresh(); // Rafraîchir les Server Components
  }

  return <button onClick={logout}>Déconnexion</button>;
}
```

## Mots-clés de routage

`Next.js`, `App Router`, `Server Components`, `Client Components`, `SSR`, `SSG`, `ISR`, `API Routes`, `Route Handlers`, `Server Actions`, `middleware`, `generateStaticParams`, `generateMetadata`, `layout`, `loading`, `error`

## Livrables

| Livrable | Description |
|----------|-------------|
| Application Next.js | Structure App Router avec pages, layouts et composants Server/Client |
| API Routes & Actions | Route Handlers et Server Actions pour intégration backend |
| Configuration Next.js | next.config.js avec optimisations et configuration déploiement |
