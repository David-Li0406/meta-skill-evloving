# Next.js + Supabase Auth

## Patterns


---
  #### **Name**
Supabase Client Setup
  #### **Description**
Create properly configured Supabase clients for different contexts
  #### **When**
Setting up auth in a Next.js project
  #### **Example**
    // lib/supabase/client.ts (Browser client)
    'use client'
    import { createBrowserClient } from '@supabase/ssr'
    
    export function createClient() {
      return createBrowserClient(
        process.env.NEXT_PUBLIC_SUPABASE_URL!,
        process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
      )
    }
    
    // lib/supabase/server.ts (Server client)
    import { createServerClient } from '@supabase/ssr'
    import { cookies } from 'next/headers'
    
    export async function createClient() {
      const cookieStore = await cookies()
      return createServerClient(
        process.env.NEXT_PUBLIC_SUPABASE_URL!,
        process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
        {
          cookies: {
            getAll() {
              return cookieStore.getAll()
            },
            setAll(cookiesToSet) {
              cookiesToSet.forEach(({ name, value, options }) => {
                cookieStore.set(name, value, options)
              })
            },
          },
        }
      )
    }
    

---
  #### **Name**
Auth Middleware
  #### **Description**
Protect routes and refresh sessions in middleware
  #### **When**
You need route protection or session refresh
  #### **Example**
    // middleware.ts
    import { createServerClient } from '@supabase/ssr'
    import { NextResponse, type NextRequest } from 'next/server'
    
    export async function middleware(request: NextRequest) {
      let response = NextResponse.next({ request })
    
      const supabase = createServerClient(
        process.env.NEXT_PUBLIC_SUPABASE_URL!,
        process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
        {
          cookies: {
            getAll() {
              return request.cookies.getAll()
            },
            setAll(cookiesToSet) {
              cookiesToSet.forEach(({ name, value, options }) => {
                response.cookies.set(name, value, options)
              })
            },
          },
        }
      )
    
      // Refresh session if expired
      const { data: { user } } = await supabase.auth.getUser()
    
      // Protect dashboard routes
      if (request.nextUrl.pathname.startsWith('/dashboard') && !user) {
        return NextResponse.redirect(new URL('/login', request.url))
      }
    
      return response
    }
    
    export const config = {
      matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
    }
    

---
  #### **Name**
Auth Callback Route
  #### **Description**
Handle OAuth callback and exchange code for session
  #### **When**
Using OAuth providers (Google, GitHub, etc.)
  #### **Example**
    // app/auth/callback/route.ts
    import { createClient } from '@/lib/supabase/server'
    import { NextResponse } from 'next/server'
    
    export async function GET(request: Request) {
      const { searchParams, origin } = new URL(request.url)
      const code = searchParams.get('code')
      const next = searchParams.get('next') ?? '/'
    
      if (code) {
        const supabase = await createClient()
        const { error } = await supabase.auth.exchangeCodeForSession(code)
        if (!error) {
          return NextResponse.redirect(`${origin}${next}`)
        }
      }
    
      return NextResponse.redirect(`${origin}/auth/error`)
    }
    

---
  #### **Name**
Server Action Auth
  #### **Description**
Handle auth operations in Server Actions
  #### **When**
Login, logout, or signup from Server Components
  #### **Example**
    // app/actions/auth.ts
    'use server'
    import { createClient } from '@/lib/supabase/server'
    import { redirect } from 'next/navigation'
    import { revalidatePath } from 'next/cache'
    
    export async function signIn(formData: FormData) {
      const supabase = await createClient()
      const { error } = await supabase.auth.signInWithPassword({
        email: formData.get('email') as string,
        password: formData.get('password') as string,
      })
    
      if (error) {
        return { error: error.message }
      }
    
      revalidatePath('/', 'layout')
      redirect('/dashboard')
    }
    
    export async function signOut() {
      const supabase = await createClient()
      await supabase.auth.signOut()
      revalidatePath('/', 'layout')
      redirect('/')
    }
    

---
  #### **Name**
Get User in Server Component
  #### **Description**
Access the authenticated user in Server Components
  #### **When**
Rendering user-specific content server-side
  #### **Example**
    // app/dashboard/page.tsx
    import { createClient } from '@/lib/supabase/server'
    import { redirect } from 'next/navigation'
    
    export default async function DashboardPage() {
      const supabase = await createClient()
      const { data: { user } } = await supabase.auth.getUser()
    
      if (!user) {
        redirect('/login')
      }
    
      return (
        <div>
          <h1>Welcome, {user.email}</h1>
        </div>
      )
    }
    

## Anti-Patterns


---
  #### **Name**
getSession in Server Components
  #### **Description**
Using getSession() instead of getUser() for auth checks
  #### **Why**
getSession() trusts the JWT without verification. getUser() validates with Supabase.
  #### **Instead**
Always use getUser() for security-critical operations

---
  #### **Name**
Auth State in Client Without Listener
  #### **Description**
Checking auth once without listening for changes
  #### **Why**
Auth state can change (logout in another tab, token refresh)
  #### **Instead**
Use onAuthStateChange listener in Client Components

---
  #### **Name**
Storing Tokens Manually
  #### **Description**
Extracting and storing JWT tokens yourself
  #### **Why**
The @supabase/ssr library handles cookies properly
  #### **Instead**
Let the library manage tokens via cookies

---
  #### **Name**
Missing Middleware Session Refresh
  #### **Description**
Not refreshing the session in middleware
  #### **Why**
Sessions expire - middleware is the right place to refresh
  #### **Instead**
Always call supabase.auth.getUser() in middleware

---
  #### **Name**
No Auth Callback Route
  #### **Description**
Forgetting the callback route for OAuth
  #### **Why**
OAuth redirects need a route to exchange the code for a session
  #### **Instead**
Create app/auth/callback/route.ts