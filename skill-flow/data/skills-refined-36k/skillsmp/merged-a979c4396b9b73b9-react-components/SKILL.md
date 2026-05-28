---
name: react:components
description: Use this skill to convert Stitch designs into modular Vite and React components while ensuring code quality and stability.
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
* **Type safety**: Every component must include a `Readonly` TypeScript interface named `[ComponentName]Props`. Avoid using the `any` type; prefer unions or unknown if necessary.
* **Project specific**: Focus on the target project's needs and constraints. Leave Google license headers out of the generated React components.
* **Style mapping**:
    * Extract the `tailwind.config` from the HTML `<head>`.
    * Sync these values with `resources/style-guide.json`.
    * Use theme-mapped Tailwind classes instead of arbitrary hex codes.

## React Native / NativeWind Stability
* **Avoid Primitive Crashes**: Prefer `Pressable` over `TouchableOpacity` or `TouchableHighlight` when using NativeWind v4 to handle complex class composition better.
* **No Web Transitions**: Avoid using `transition-*`, `duration-*`, `ease-*`, or `active:*` pseudo-classes on Native primitives to prevent instability. Use `react-native-reanimated` for all motion.
* **Smooth Gestures**: Use `measure()` to establish a coordinate baseline for sliders or drag handlers to prevent "frame one" jumps or flashes.
* **Rules of Hooks**: Declare hooks (`useMemo`, `useCallback`, `useEffect`) at the top level of the component, before any early returns.

## Execution Steps
1. **Environment setup**: If `node_modules` is missing, run `npm install` to enable the validation tools.
2. **Data layer**: Create `src/data/mockData.ts` based on the design content.
3. **Component drafting**: Use `resources/component-template.tsx` as a base. Replace all instances of `StitchComponent` with the actual name of the component you are creating.
4. **Application wiring**: Update the project entry point (like `App.tsx`) to render the new components.
5. **Quality check**:
    * Run `npm run validate <file_path>` for each component.
    * Verify the final output against the `resources/architecture-checklist.md`.
    * Start the dev server with `npm run dev` to verify the live result.

## Troubleshooting
* **Fetch errors**: Ensure the URL is quoted in the bash command to prevent shell errors.
* **Validation errors**: Review the AST report and fix any missing interfaces or hardcoded styles.

## Safe Refactoring & Editing
* **Anchor Strategy**: When using `replace_file_content`, include at least 2-3 lines of unchanged code (anchors) surrounding your target block to prevent accidental deletions.
* **Wrapper Integrity**: Verify the closing tag of any wrapping component matches the opening tag in your replacement block.
* **Global Consistency**: Before changing a shared design token, run a global search to identify all instances and apply the change structurally across the entire app.