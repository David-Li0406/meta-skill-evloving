# Nextjs Supabase Auth - Validations

## Using getSession() for Auth Checks

### **Id**
auth-getsession-insecure
### **Severity**
error
### **Type**
regex
### **Pattern**
  - getSession\\(\\)[\s\S]{0,50}?(?:user|session)(?![\s\S]{0,50}?getUser)
### **Message**
getSession() doesn't verify the JWT. Use getUser() for secure auth checks.
### **Fix Action**
Replace getSession() with getUser() for security-critical checks
### **Applies To**
  - *.tsx
  - *.ts
  - middleware.ts
### **Test Cases**
  #### **Should Match**
    -       const { data: { session } } = await supabase.auth.getSession()
      if (session?.user) {
        // Do something
      }
      
    -       const session = await supabase.auth.getSession()
      return session.data.user
      
    -       await supabase.auth.getSession()
      const user = session?.user
      
  #### **Should Not Match**
    -       const { data: { user } } = await supabase.auth.getUser()
      if (user) {
        // Secure check
      }
      
    -       // Get session for display, but verify with getUser
      const { data: { session } } = await supabase.auth.getSession()
      const { data: { user } } = await supabase.auth.getUser()
      
    -       // Just getting session for token, not for auth check
      const { data: { session } } = await supabase.auth.getSession()
      const token = session?.access_token
      

## OAuth Without Callback Route

### **Id**
auth-missing-callback
### **Severity**
error
### **Type**
file
### **Pattern**
app/auth/callback/route.ts
### **Message**
Using OAuth but missing callback route at app/auth/callback/route.ts
### **Fix Action**
Create app/auth/callback/route.ts to handle OAuth redirects
### **Applies To**
  - app/**/*
### **Test Cases**
  #### **Should Match**
    
---
      ###### **Description**
Project with OAuth but no callback route
      ###### **Files**
        - app/login/page.tsx
      ###### **Missing**
        - app/auth/callback/route.ts
  #### **Should Not Match**
    
---
      ###### **Description**
Project with OAuth and callback route
      ###### **Files**
        - app/login/page.tsx
        - app/auth/callback/route.ts
    
---
      ###### **Description**
Project without OAuth
      ###### **Files**
        - app/login/page.tsx

## Browser Client in Server Context

### **Id**
auth-browser-client-server
### **Severity**
error
### **Type**
regex
### **Pattern**
  - createBrowserClient[\s\S]*?cookies\(\)
  - import.*createBrowserClient.*from[\s\S]*?export.*async
### **Message**
Browser client used in server context. Use createServerClient instead.
### **Fix Action**
Import and use createServerClient from @supabase/ssr
### **Applies To**
  - app/**/page.tsx
  - app/**/layout.tsx
  - app/actions*.ts
  - middleware.ts
### **Test Cases**
  #### **Should Match**
    -       import { createBrowserClient } from '@supabase/ssr'
      import { cookies } from 'next/headers'
      
      export async function getData() {
        const supabase = createBrowserClient(...)
      }
      
    -       import { createBrowserClient } from '@supabase/ssr'
      
      export async function POST(request: Request) {
        const supabase = createBrowserClient(...)
      }
      
  #### **Should Not Match**
    -       'use client'
      import { createBrowserClient } from '@supabase/ssr'
      
      export function MyComponent() {
        const supabase = createBrowserClient(...)
      }
      
    -       import { createServerClient } from '@supabase/ssr'
      import { cookies } from 'next/headers'
      
      export async function getData() {
        const supabase = createServerClient(...)
      }
      

## Protected Routes Without Middleware

### **Id**
auth-no-middleware
### **Severity**
warning
### **Type**
file
### **Pattern**
middleware.ts
### **Message**
No middleware.ts found. Consider adding middleware for route protection.
### **Fix Action**
Create middleware.ts to protect routes and refresh sessions
### **Applies To**
  - app/dashboard/**
  - app/admin/**
  - app/account/**
### **Test Cases**
  #### **Should Match**
    
---
      ###### **Description**
Project with protected routes but no middleware
      ###### **Files**
        - app/dashboard/page.tsx
        - app/admin/settings/page.tsx
      ###### **Missing**
        - middleware.ts
  #### **Should Not Match**
    
---
      ###### **Description**
Project with middleware
      ###### **Files**
        - app/dashboard/page.tsx
        - middleware.ts
    
---
      ###### **Description**
Project without protected routes
      ###### **Files**
        - app/page.tsx
        - app/about/page.tsx

## Hardcoded Auth Redirect URL

### **Id**
auth-hardcoded-redirect
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - redirectTo:\s*['"]https?://(?:localhost|127\.0\.0\.1)
  - redirect.*http://localhost
### **Message**
Hardcoded localhost redirect. Use origin for environment flexibility.
### **Fix Action**
Use window.location.origin or process.env.NEXT_PUBLIC_SITE_URL
### **Applies To**
  - *.tsx
  - *.ts
### **Test Cases**
  #### **Should Match**
    -       await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: 'http://localhost:3000/auth/callback'
        }
      })
      
    -       const redirect = 'https://localhost:3000/dashboard'
      
    -       redirectTo: "http://127.0.0.1:3000/auth/callback"
      
  #### **Should Not Match**
    -       await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`
        }
      })
      
    -       const redirectTo = process.env.NEXT_PUBLIC_SITE_URL + '/auth/callback'
      
    -       redirectTo: `${origin}/auth/callback`
      

## Auth Call Without Error Handling

### **Id**
auth-missing-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await supabase\.auth\.sign(?:In|Up|Out)(?![\s\S]{0,100}?error)
### **Message**
Auth operation without error handling. Always check for errors.
### **Fix Action**
Destructure { data, error } and handle error case
### **Applies To**
  - *.tsx
  - *.ts
### **Test Cases**
  #### **Should Match**
    -       await supabase.auth.signInWithPassword({
        email,
        password
      })
      redirect('/dashboard')
      
    -       await supabase.auth.signUp({ email, password })
      return { success: true }
      
    -       await supabase.auth.signOut()
      router.push('/')
      
  #### **Should Not Match**
    -       const { error } = await supabase.auth.signInWithPassword({
        email,
        password
      })
      if (error) return { error: error.message }
      
    -       const { data, error } = await supabase.auth.signUp({ email, password })
      if (error) throw error
      
    -       const { error } = await supabase.auth.signOut()
      if (!error) redirect('/')
      

## Auth Action Without Revalidation

### **Id**
auth-no-revalidate
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - signOut\(\)(?![\s\S]{0,100}?revalidate)
  - signIn(?:WithPassword|WithOAuth)(?![\s\S]{0,100}?revalidate)
### **Message**
Auth action without revalidatePath. Cache may show stale auth state.
### **Fix Action**
Add revalidatePath('/', 'layout') after auth operations
### **Applies To**
  - app/actions*.ts
  - **/actions/*.ts
### **Test Cases**
  #### **Should Match**
    -       'use server'
      export async function signOut() {
        const supabase = await createClient()
        await supabase.auth.signOut()
        redirect('/')
      }
      
    -       const { error } = await supabase.auth.signInWithPassword({
        email, password
      })
      redirect('/dashboard')
      
  #### **Should Not Match**
    -       'use server'
      export async function signOut() {
        const supabase = await createClient()
        await supabase.auth.signOut()
        revalidatePath('/', 'layout')
        redirect('/')
      }
      
    -       const { error } = await supabase.auth.signInWithPassword({
        email, password
      })
      if (!error) {
        revalidatePath('/', 'layout')
        redirect('/dashboard')
      }
      

## Client-Only Route Protection

### **Id**
auth-client-side-protection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - 'use client'[\s\S]*?getUser\(\)[\s\S]*?redirect
  - 'use client'[\s\S]*?useEffect[\s\S]*?redirect
### **Message**
Client-side route protection shows flash of content. Use middleware.
### **Fix Action**
Move protection to middleware.ts for better UX
### **Applies To**
  - app/**/page.tsx
### **Test Cases**
  #### **Should Match**
    -       'use client'
      import { useEffect } from 'react'
      import { useRouter } from 'next/navigation'
      
      export default function Dashboard() {
        const router = useRouter()
      
        useEffect(() => {
          supabase.auth.getUser().then(({ data }) => {
            if (!data.user) router.redirect('/login')
          })
        }, [])
      
        return <div>Dashboard Content</div>
      }
      
    -       'use client'
      
      export default function ProtectedPage() {
        const { data } = await supabase.auth.getUser()
        if (!data.user) redirect('/login')
      }
      
  #### **Should Not Match**
    -       // Server Component - no 'use client'
      import { redirect } from 'next/navigation'
      
      export default async function Dashboard() {
        const { data: { user } } = await supabase.auth.getUser()
        if (!user) redirect('/login')
        return <div>Dashboard</div>
      }
      
    -       'use client'
      
      export default function Dashboard() {
        // No redirect, just conditional rendering
        const [user, setUser] = useState(null)
      
        useEffect(() => {
          supabase.auth.getUser().then(({ data }) => {
            setUser(data.user)
          })
        }, [])
      
        if (!user) return <LoginPrompt />
        return <DashboardContent />
      }
      