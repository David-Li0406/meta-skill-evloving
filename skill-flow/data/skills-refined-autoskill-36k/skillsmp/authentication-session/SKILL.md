---
name: Authentication & Session
description: Manage Supabase auth, session persistence, and user state
---

# Authentication & Session Skill

## Overview
Handle Supabase authentication, session persistence, and user state management across the Smarter.Poker ecosystem.

## Core Principles

### Global Auth Handshake
Every page must use the singleton auth pattern:
```javascript
// In _app.js - SINGLE source of truth
const [session, setSession] = useState(null);
const [isAuthLoading, setIsAuthLoading] = useState(true);

useEffect(() => {
  const initAuth = async () => {
    const { data: { session } } = await supabase.auth.getSession();
    setSession(session);
    setIsAuthLoading(false);
  };
  
  initAuth();
  
  const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
    setSession(session);
  });
  
  return () => subscription.unsubscribe();
}, []);
```

### CRITICAL: Disable React Strict Mode
React Strict Mode causes double-mounting which breaks Supabase auth:
```javascript
// next.config.js
module.exports = {
  reactStrictMode: false  // REQUIRED for Supabase auth
};
```

## Session Persistence

### Check Logged In
```javascript
const isLoggedIn = session?.user != null;
```

### Get User Profile
```javascript
const { data: profile } = await supabase
  .from('profiles')
  .select('*')
  .eq('id', session.user.id)
  .single();
```

### Auth Loading States
Always show loading while auth initializes:
```jsx
if (isAuthLoading) {
  return <LoadingSpinner />;
}

if (!session) {
  return <LoginPage />;
}

return <AuthenticatedContent />;
```

## Login Flow

### Email/Password
```javascript
const { data, error } = await supabase.auth.signInWithPassword({
  email,
  password
});
```

### OAuth (Google, Discord)
```javascript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: window.location.origin
  }
});
```

### Magic Link
```javascript
const { error } = await supabase.auth.signInWithOtp({
  email,
  options: {
    emailRedirectTo: window.location.origin
  }
});
```

## Logout
```javascript
await supabase.auth.signOut();
// Session state will update via onAuthStateChange
```

## Domain Handling

### WWW Redirect (middleware.js)
```javascript
if (host.startsWith('www.')) {
  return NextResponse.redirect(
    new URL(request.url.replace('www.', ''))
  );
}
```

### Cookie Domain
Ensure cookies work across subdomains:
```javascript
const supabase = createClient(url, key, {
  auth: {
    persistSession: true,
    storageKey: 'smarter-poker-auth',
    storage: {
      getItem: (key) => cookies().get(key)?.value,
      setItem: (key, value) => {
        cookies().set(key, value, {
          domain: '.smarter.poker',
          secure: true,
          sameSite: 'lax'
        });
      }
    }
  }
});
```

## Profile Table
```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  username TEXT UNIQUE,
  full_name TEXT,
  avatar_url TEXT,
  display_name_preference TEXT DEFAULT 'username',
  xp INTEGER DEFAULT 0,
  diamonds INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Common Issues

### "Abort Plague"
Symptom: AbortErrors, session lost on navigation
Fix: Disable React Strict Mode

### Session Lost on Refresh
Check: Is `persistSession: true` in Supabase config?
Check: Is storage correctly configured?

### www vs non-www
Symptom: Logged out when switching domains
Fix: Set cookie domain to `.smarter.poker`
