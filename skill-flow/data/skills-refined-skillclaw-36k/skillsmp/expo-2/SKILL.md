---
name: expo
description: Best practices for React Native development with Expo and Expo Router.
---

# Expo & React Native Best Practices

## Navigation (Expo Router)
- Use **File-based routing** in the `app/` directory.
- Use `Link` from `expo-router` for navigation, but prefer `router.push()` or `router.replace()` for logic-based navigation in event handlers.
- **Navigation Context Stability**: Avoid using `useRouter` or `useNavigation` deep inside component trees that are rendered in Modals or Portals.
  - **Constraint**: React 19 / NativeWind interop can cause circular navigation context lookups, leading to "Navigation Context" crashes. 
  - **Fix**: Elevate navigation logic to the Screen/Page level and pass navigation handlers (like `onClose`) down to children.
- Screens should be wrapped in `Stack.Screen` or `Tabs.Screen` to configure headers.

## Styling & UI Robustness
- **Stray Text Crash**: React Native crashes if a raw string is outside a `<Text>` component. 
  - **Caution**: Avoid Tailwind patterns like `space-x` or `space-y` in complex layouts as they inject invisible spacers that can clip into text nodes. Prefer explicit margins (`mr-2`, `mt-4`).
  - **JSX Cleanliness**: Always ensure there is no accidental whitespace/comments between sibling components in a `View`.
- **Loading Guards**: Always use an `isLoading` check or an `ErrorBoundary` when accessing data from a hook (like `useHousehold`). Prevent the UI from rendering with `undefined` values.
- **Defensive API Consumption**: External APIs (like Open Food Facts) are unreliable. 
  - **Rule**: Never trust specific keys exist in a response. Always use extensive optional chaining (`data?.results?.[0]`) and fallback to empty defaults (`|| []`).
  - **Rule**: Check `response.ok` before calling `.json()`.
  - **Rule**: Limit "bonus" features. Stick strictly to the user's core intent (e.g., if asked for food search, don't implement full allergy taxonomies that increase surface area for crashes).
  - **Rule**: When searching for products, use localized API endpoints (e.g., `us.openfoodfacts.org`) to ensure results are regionally relevant.
- **Interactive Layers (Android)**: **Critical**: Absolute positioned elements (like dropdowns) that extend beyond their parent container's bounds are non-interactive on Android (clipping).
  - **Fix**: Place floating dropdown containers at the **end of the root component** (so they are direct children of the page) and use high `elevation` (Android) and `zIndex` (iOS).
- **Nested Scrolling**: Avoid nested `ScrollView`s. Use `FlatList` for dropdowns with `nestedScrollEnabled={true}`, `keyboardShouldPersistTaps="always"`, and `persistentScrollbar={true}`.
- **React 19 / NativeWind Stability (CRITICAL)**:
  - **Avoid `className` on Portals/Modals**: When using React 19, NativeWind v4's interop layer may crash when wrapping components logic that uses navigation.
  - **Safe Pattern**: For high-interaction components (Modals, FABs, Inputs), use standard React Native `style` props instead of `className` to bypass the interop layer.
  - **Defensive Filtering**: Always use optional chaining on dynamic data (e.g. `item.name?.toLowerCase() || ''`) when filtering lists to prevent crashes during re-renders.

## UX & Performance Standards
- **Optimistic Updates**: For list modifications (add, delete, toggle), update the local state **instantly** before the API call. Re-fetch or rollback only on error. This gives a "premium" snappy feel.
- **Search UX**: Every search input MUST have:
  - An `X` (clear) button inside the input area.
  - A transparent backdrop `<Pressable>` behind the dropdown to dismiss the results when tapping outside.

## Auth & Session Management
- **Root Auth Gate**: Implement a session listener in the `RootLayout` (`app/_layout.tsx`) that renders an `AuthScreen` if no session is present. This prevents "Logged In" UI loops for users without profiles.
- **Supabase Mobile Redirects**: By default, Supabase redirects email confirmations to `localhost:3000`. 
  - **Dev Fix**: Disable "Confirm Email" in the Supabase dashboard for rapid prototyping.
  - **Prod Fix**: Set the "Site URL" to your app's custom scheme (e.g., `pantryguard://`).

## Tooling
- Use `npx expo install` to install packages to ensure dependency compatibility.
- **Dependency Hygiene**: Before using a new JS library (like `lodash`), check if it requires `@types/` packages. Install types as `devDependencies` immediately to prevent TS errors.
- Use `Expo Go` for rapid prototyping on physical devices.
- **Networking Troubleshooting**: On Windows, Expo Go may fail with `java.io.IOException` (Network Isolation).
  - Fix 1: Use `npx expo start --tunnel` to bypass firewalls.
  - Fix 2: Ensure Windows network profile is set to **Private**, not Public.

## Specialized Hardware (Camera/Scanner)
- **Library**: Use `expo-camera` (modern `CameraView`) rather than the deprecated `expo-barcode-scanner`.
- **Styling**: **CRITICAL**: Always use inline `style={{ flex: 1 }}` for `CameraView`. Relying on `className="flex-1"` often results in a 0-height container (Black Screen) on certain platforms/plugin versions.
- **Focus Issues (Android)**: Barcode scanning on Android often suffers from "blurry focus". 
  - Fix: **Always** implement digital zoom controls (`+`/`-` buttons) in the UI. Zooming in (2x/3x) triggers a sensor refocus.
- **Permissions**: Never assume permission is granted. Handle the `!permission.granted` state with a dedicated UI.

## Push Notifications (Expo Go vs Dev Build)
- **CRITICAL**: Remote notifications provided by `expo-notifications` have been **Removed** from the Expo Go Go client (Android) as of SDK 53.
- **Rule**: You MUST guard all notification logic behind an environment check for `ExecutionEnvironment.StoreClient`.
- **Double Guard Pattern**:
  1. Do NOT use top-level `import * as Notifications`. Use `require()` inside the guarded block.
  2. Do NOT run `setNotificationHandler` or `scheduleNotificationAsync` if `isExpoGo` is true.
  3. Log a `[Dev]` message instead of crashing.
