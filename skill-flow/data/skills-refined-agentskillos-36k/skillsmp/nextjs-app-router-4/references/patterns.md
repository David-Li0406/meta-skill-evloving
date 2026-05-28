# Next.js App Router

## Patterns


---
  #### **Name**
Server Component Data Fetching
  #### **Description**
Fetch data directly in Server Components using async/await
  #### **When**
You need to fetch data that doesn't require client interactivity
  #### **Example**
    // app/users/page.tsx
    export default async function UsersPage() {
      const users = await db.user.findMany()
      return <UserList users={users} />
    }
    

---
  #### **Name**
Client Component Islands
  #### **Description**
Wrap interactive parts in Client Components, keep the rest server
  #### **When**
You have a mostly static page with some interactive elements
  #### **Example**
    // app/dashboard/page.tsx (Server Component)
    export default async function Dashboard() {
      const data = await fetchDashboardData()
      return (
        <div>
          <h1>Dashboard</h1>
          <StaticMetrics data={data} />
          <InteractiveChart data={data} /> {/* Client Component */}
        </div>
      )
    }
    

---
  #### **Name**
Server Actions for Mutations
  #### **Description**
Use Server Actions instead of API routes for form submissions
  #### **When**
Handling form submissions or data mutations from the client
  #### **Example**
    // app/actions.ts
    'use server'
    
    export async function createUser(formData: FormData) {
      const name = formData.get('name')
      await db.user.create({ data: { name } })
      revalidatePath('/users')
    }
    

---
  #### **Name**
Parallel Data Fetching
  #### **Description**
Fetch multiple data sources in parallel using Promise.all
  #### **When**
Page needs data from multiple independent sources
  #### **Example**
    export default async function Page() {
      const [users, posts] = await Promise.all([
        fetchUsers(),
        fetchPosts()
      ])
      return <Content users={users} posts={posts} />
    }
    

---
  #### **Name**
Loading UI with Suspense
  #### **Description**
Use loading.tsx or Suspense for streaming loading states
  #### **When**
You want to show loading UI while data fetches
  #### **Example**
    // app/dashboard/loading.tsx
    export default function Loading() {
      return <DashboardSkeleton />
    }
    
    // Or with Suspense boundaries
    <Suspense fallback={<Skeleton />}>
      <SlowComponent />
    </Suspense>
    

## Anti-Patterns


---
  #### **Name**
Async Client Components
  #### **Description**
Adding async to components marked with 'use client'
  #### **Why**
Client Components run in the browser where top-level await doesn't work the same way
  #### **Instead**
Move data fetching to a Server Component parent or use useEffect

---
  #### **Name**
Over-using 'use client'
  #### **Description**
Adding 'use client' to every component
  #### **Why**
You lose the benefits of Server Components - smaller bundles, direct DB access, SEO
  #### **Instead**
Only add 'use client' when you need hooks, event handlers, or browser APIs

---
  #### **Name**
Fetching in Client Components
  #### **Description**
Using useEffect to fetch data that could be fetched on the server
  #### **Why**
Causes waterfalls, shows loading spinners, worse SEO, larger bundles
  #### **Instead**
Fetch in Server Components and pass data as props

---
  #### **Name**
Prop Drilling Through Server/Client Boundary
  #### **Description**
Passing many props from Server to Client just to pass them deeper
  #### **Why**
Creates tight coupling and makes refactoring hard
  #### **Instead**
Use composition - Client Component children can be Server Components

---
  #### **Name**
Server Imports in Client Components
  #### **Description**
Importing server-only modules (fs, db clients) in 'use client' files
  #### **Why**
Will fail at build time or runtime with cryptic errors
  #### **Instead**
Keep server code in Server Components, pass only serializable data