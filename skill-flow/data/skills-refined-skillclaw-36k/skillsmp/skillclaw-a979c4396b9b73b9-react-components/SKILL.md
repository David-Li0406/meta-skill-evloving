---
name: react:components
description: Use this skill when you need to convert Stitch designs into modular Vite and React components while ensuring code quality and stability.
---

# Stitch to React Components

You are a frontend engineer focused on transforming designs into clean React code. You follow a modular approach and use automated tools to ensure code quality.

## Retrieval and Networking
1. **Namespace discovery**: Run `list_tools` to find the Stitch MCP prefix. Use this prefix (e.g., `stitch:`) for all subsequent calls.
2. **Metadata fetch**: Call `[prefix]:get_screen` to retrieve the design JSON.
3. **High-reliability download**: Internal AI fetch tools can fail on Google Cloud Storage domains.
   - Use the `Bash` tool to run: `bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"`.
   - This script handles the necessary redirects and security handshakes.
4. **Visual audit**: Check `screenshot.downloadUrl` to confirm the design intent and layout details.

## Architectural Rules
* **Modular components**: Break the design into independent files. Avoid large, single-file outputs.
* **Logic isolation**: Move event handlers and business logic into custom hooks in `src/hooks/`.
* **Data decoupling**: Move all static text, image URLs, and lists into `src/data/mockData.ts`.
* **Type safety**: Every component must include a `Readonly` TypeScript interface named `[ComponentName]Props`.
* **Project specific**: Focus on the target project's needs and constraints. Leave Google license headers out of the generated React components.
* **Style mapping**:
    * Extract the `tailwind.config` from the HTML `<head>`.
    * Sync these values with `resources/style-guide.json`.
    * Use theme-mapped Tailwind classes instead of arbitrary hex codes.

## React Native / NativeWind Stability
* **Avoid Primitive Crashes**: When using NativeWind v4, prefer `Pressable` over `TouchableOpacity` or `TouchableHighlight` to handle complex class composition better and avoid "Navigation Context" crashes.
* **No Web Transitions**: Do NOT use `transition-*`, `duration-*`, `ease-*`, or `active:*` pseudo-classes on Native primitives. These often cause instability or crashes in the interop layer. Use `react-native-reanimated` for all motion.
* **Smooth Gestures**: When implementing sliders or drag handlers, NEVER rely on relative coordinates (like `locationX`) blindly. Always use `measure()` to establish a coordinate baseline (`pageX`) to prevent "frame one" jumps or flashes.
* **Rules of Hooks**: NEVER place hooks (`useMemo`, `useCallback`, `useEffect`) after conditional returns (e.g., `if (isLoading) return ...`). This violates React's core rules and causes runtime crashes. All hooks must be declared at the top level of the component, *before* any early returns.

## Execution Steps
1. **Environment setup**: If `node_modules` is missing, run `npm install` to enable the validation tools.
2. **Data layer**: Create `src/data/mockData.ts` based on the design content.
3. **Component drafting**: Use `resources/component-template.tsx` as a base. Find and replace all instances of `StitchComponent` with the actual name of the component you are creating.
4. **Application wiring**: Update the project entry point (like `App.tsx`) to render the new components.
5. **Quality check**:
    * Run `npm run validate <file_path>` for each component.
    * Verify the final output against the `resources/architecture-check`.