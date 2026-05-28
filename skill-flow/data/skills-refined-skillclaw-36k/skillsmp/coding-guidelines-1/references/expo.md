# Expo Patterns

Principles and research guidance for projects using Expo.

## Core Principles

### Managed Workflow
Expo provides a managed workflow with pre-configured native modules. Research available Expo packages before adding third-party alternatives.

### Research Before Implementation
Expo APIs evolve frequently. Always verify current syntax:
- Use context7 to query Expo documentation
- Search for: expo-router, expo packages, configuration

## Expo Router

### File-Based Routing
Routes are defined by file structure in `app/` directory. Research current conventions:

| File | Route |
|------|-------|
| `app/index.tsx` | `/` |
| `app/login.tsx` | `/login` |
| `app/[id].tsx` | Dynamic route `/123` |
| `app/_layout.tsx` | Layout wrapper |
| `app/+html.tsx` | Custom HTML (web SSR) |
| `app/api/health+api.ts` | API route |

### Navigation
Research current navigation APIs:

```tsx
import { router, useRouter, useSegments } from "expo-router";

// Programmatic navigation
router.replace("/login");
router.push("/details");

// Hooks for navigation state
const segments = useSegments();
const router = useRouter();
```

### Layout Pattern
`_layout.tsx` wraps child routes:

```tsx
import { Slot } from "expo-router";

const Layout = () => (
  <SafeAreaProvider>
    <Slot />
  </SafeAreaProvider>
);
```

## Common Expo Packages

Research these packages as needed:
- **expo-router** - File-based routing
- **react-native-safe-area-context** - Safe area handling
- **expo-status-bar** - Status bar control
- **expo-font** - Custom fonts
- **expo-image** - Optimized images
- **expo-secure-store** - Secure storage

## Auth Pattern

Research auth state management with routing:

```tsx
const useAuthRedirect = () => {
  const [user, setUser] = useState<User | undefined>();
  const router = useRouter();
  const segments = useSegments();

  useEffect(() => {
    // Subscribe to auth state changes
    const unsubscribe = auth.onSignInChange(setUser);
    return unsubscribe;
  }, []);

  useEffect(() => {
    // Redirect based on auth state
    const inAuthGroup = segments[0] === "login";
    if (!user && !inAuthGroup) router.replace("/login");
    if (user && inAuthGroup) router.replace("/");
  }, [user, segments]);
};
```

## Research Checklist

Before implementing, query documentation for:
- [ ] File naming conventions for routes
- [ ] Available Expo packages for the feature
- [ ] Current navigation API methods
- [ ] Web vs native differences in Expo Router
- [ ] Configuration options in app.json/app.config.js
- [ ] Any breaking changes in current Expo SDK version
