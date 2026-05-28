# Nextjs Supabase Auth - Sharp Edges

## Auth Getsession Vs Getuser

### **Id**
auth-getsession-vs-getuser
### **Summary**
getSession() is not secure for auth checks
### **Severity**
critical
### **Situation**
Using getSession() to verify user authentication in Server Components
### **Why**
  getSession() reads the JWT from cookies but DOES NOT validate it.
  An attacker could forge a JWT, and getSession() would trust it.
  getUser() makes a request to Supabase to verify the token.
  
### **Solution**
  Always use getUser() for security-critical operations:
  
  // WRONG - trusts unverified JWT
  const { data: { session } } = await supabase.auth.getSession()
  if (session?.user) { /* could be spoofed */ }
  
  // RIGHT - verifies with Supabase
  const { data: { user } } = await supabase.auth.getUser()
  if (user) { /* actually authenticated */ }
  
### **Symptoms**
  - Security vulnerability in auth
  - User spoofing possible
  - Auth seems to work but is not secure
### **Detection Pattern**
getSession\\(\\)(?![\\s\\S]{0,100}?getUser)
### **Version Range**
>=2.0.0

## Auth Middleware Order

### **Id**
auth-middleware-order
### **Summary**
Middleware not refreshing session before route protection
### **Severity**
high
### **Situation**
Checking auth in middleware without refreshing the session first
### **Why**
  JWT tokens expire. If you check auth before refreshing, expired
  tokens cause spurious redirects. The session might be valid but
  the token just needs a refresh.
  
### **Solution**
  Always refresh session first in middleware:
  
  export async function middleware(request: NextRequest) {
    const response = NextResponse.next({ request })
    const supabase = createServerClient(...)
  
    // Refresh FIRST - this updates cookies if needed
    const { data: { user } } = await supabase.auth.getUser()
  
    // THEN check auth
    if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  
    return response
  }
  
### **Symptoms**
  - Users randomly logged out
  - Auth works sometimes, fails other times
  - Session seems to expire early
### **Detection Pattern**
middleware[\\s\\S]*?pathname[\\s\\S]*?getUser
### **Version Range**
>=1.0.0

## Auth Callback Missing

### **Id**
auth-callback-missing
### **Summary**
Missing auth callback route for OAuth
### **Severity**
high
### **Situation**
Setting up OAuth providers without the callback handler
### **Why**
  OAuth providers redirect back to your app with a code.
  Without the callback route, there's nowhere to exchange
  this code for a session, so login appears to fail.
  
### **Solution**
  Create the callback route handler:
  
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
  
  // In Supabase dashboard, set redirect URL to:
  // https://yoursite.com/auth/callback
  
### **Symptoms**
  - OAuth login fails after provider redirect
  - User lands on 404 after OAuth
  - code parameter in URL but not logged in
### **Detection Pattern**

### **Version Range**
>=1.0.0

## Auth Client Server Mismatch

### **Id**
auth-client-server-mismatch
### **Summary**
Using wrong Supabase client for the context
### **Severity**
high
### **Situation**
Using browser client in Server Component or vice versa
### **Why**
  Browser client (createBrowserClient) can't access server-only
  cookies. Server client (createServerClient) doesn't work in
  browser. Using the wrong one means auth state is lost.
  
### **Solution**
  Use the right client for each context:
  
  // In Server Components, Server Actions, Route Handlers:
  import { createClient } from '@/lib/supabase/server'
  
  // In Client Components:
  import { createClient } from '@/lib/supabase/client'
  
  // In middleware.ts - create inline with request/response cookies
  
  // Separate files make it clear:
  // lib/supabase/client.ts - 'use client', createBrowserClient
  // lib/supabase/server.ts - createServerClient with cookies()
  
### **Symptoms**
  - Auth works on server but not client
  - User appears logged out after refresh
  - getUser returns null when user is logged in
### **Detection Pattern**
createBrowserClient.*cookies\(\)|createServerClient.*'use client'
### **Version Range**
>=1.0.0

## Auth No Listener

### **Id**
auth-no-listener
### **Summary**
Client Component doesn't listen for auth changes
### **Severity**
medium
### **Situation**
Checking auth once without onAuthStateChange listener
### **Why**
  Auth state can change at any time: user logs out in another tab,
  token refreshes, session expires. Without a listener, your UI
  gets out of sync with reality.
  
### **Solution**
  Use onAuthStateChange in Client Components:
  
  'use client'
  import { useEffect, useState } from 'react'
  import { createClient } from '@/lib/supabase/client'
  
  export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const supabase = createClient()
  
    useEffect(() => {
      const { data: { subscription } } = supabase.auth.onAuthStateChange(
        (event, session) => {
          setUser(session?.user ?? null)
        }
      )
  
      return () => subscription.unsubscribe()
    }, [])
  
    return <AuthContext.Provider value={user}>{children}</AuthContext.Provider>
  }
  
### **Symptoms**
  - UI shows logged in after logout
  - Auth state stuck until refresh
  - Multiple tabs get out of sync
### **Detection Pattern**
createClient\\(\\)(?![\\s\\S]{0,500}?onAuthStateChange)
### **Version Range**
>=1.0.0

## Auth Redirect Loop

### **Id**
auth-redirect-loop
### **Summary**
Redirect loop between login and protected route
### **Severity**
medium
### **Situation**
Middleware redirects to login, but login also gets redirected
### **Why**
  If your middleware matcher is too broad, it catches the login page
  itself. User gets redirected to login, which redirects to login,
  infinite loop.
  
### **Solution**
  Exclude auth routes from middleware, or handle them explicitly:
  
  // Option 1: Matcher excludes auth routes
  export const config = {
    matcher: ['/((?!_next/static|_next/image|favicon.ico|login|auth).*)'],
  }
  
  // Option 2: Explicit handling in middleware
  export async function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl
  
    // Skip auth-related routes
    if (pathname.startsWith('/login') || pathname.startsWith('/auth')) {
      return NextResponse.next()
    }
  
    // ... rest of auth check
  }
  
### **Symptoms**
  - Browser shows "too many redirects"
  - Login page never loads
  - Infinite loading
### **Detection Pattern**
matcher.*(?!.*login|auth)
### **Version Range**
>=1.0.0

## Auth Pkce Cors

### **Id**
auth-pkce-cors
### **Summary**
CORS issues with PKCE flow
### **Severity**
medium
### **Situation**
Using signInWithOAuth and getting CORS errors
### **Why**
  OAuth with PKCE requires specific redirect URL configuration.
  If the redirect URL in Supabase dashboard doesn't match your
  actual callback URL exactly, you get CORS errors.
  
### **Solution**
  1. In Supabase Dashboard > Authentication > URL Configuration:
     - Site URL: https://yoursite.com
     - Redirect URLs: https://yoursite.com/auth/callback
  
  2. For local development, add:
     - http://localhost:3000/auth/callback
  
  3. In your OAuth call:
     await supabase.auth.signInWithOAuth({
       provider: 'google',
       options: {
         redirectTo: `${window.location.origin}/auth/callback`,
       },
     })
  
  4. Make sure the callback route exists at that path
  
### **Symptoms**
  - CORS error in console
  - OAuth popup closes but login fails
  - Invalid redirect URL error
### **Detection Pattern**
signInWithOAuth(?![\\s\\S]{0,100}?redirectTo)
### **Version Range**
>=1.0.0

## Auth Server Action Cookies

### **Id**
auth-server-action-cookies
### **Summary**
Cookies not being set in Server Actions
### **Severity**
medium
### **Situation**
Login works but session doesn't persist
### **Why**
  Server Actions can set cookies, but only if you use the right
  pattern. The createServerClient needs the cookies() function
  with both getAll and setAll implemented.
  
### **Solution**
  Make sure your server client sets cookies:
  
  // lib/supabase/server.ts
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
            // This is critical for Server Actions!
            try {
              cookiesToSet.forEach(({ name, value, options }) =>
                cookieStore.set(name, value, options)
              )
            } catch {
              // Called from Server Component - can't set cookies
            }
          },
        },
      }
    )
  }
  
### **Symptoms**
  - Login succeeds but immediately logged out
  - getUser() returns null after signIn
  - Works in API routes but not Server Actions
### **Detection Pattern**
createServerClient(?![\\s\\S]{0,200}?setAll)
### **Version Range**
>=1.0.0