# Browser Extension Checklist

Complete validation checklist for Chrome/browser extensions.

---

## Project Structure

- [ ] `manifest.json` (Manifest V3)
- [ ] `package.json` for build dependencies
- [ ] `tsconfig.json` with strict mode
- [ ] `src/ts/` for TypeScript source
- [ ] `src/html/` for HTML files
- [ ] `icons/` for extension icons
- [ ] `dist/` for build output
- [ ] `tests/` with setup and mocks
- [ ] `README.md` with installation
- [ ] `CLAUDE.md` with architecture

## Manifest V3

- [ ] `manifest_version: 3`
- [ ] `permissions` array (minimal required)
- [ ] `background.service_worker` configured
- [ ] `background.type: "module"` if using ES modules
- [ ] `action.default_popup` configured
- [ ] Icons: 16px, 48px, 128px

## The Triad

### Health (Doctor)
- [ ] Permissions validated on install
- [ ] Storage access verified
- [ ] Configuration validation on first run
- [ ] Clear error messages for missing permissions

### Safety (Safety Net)
- [ ] Destructive actions logged before execution
- [ ] Undo/restore functionality
- [ ] Confirmation for batch operations
- [ ] Data export before major operations

### Resilience (Statekeeper)
- [ ] State persists to chrome.storage or IndexedDB
- [ ] Graceful handling of storage errors
- [ ] Service worker survives restarts
- [ ] chrome.alarms for reliable scheduling

## Data Models

- [ ] TypeScript interfaces for all data
- [ ] Type guards for runtime validation
- [ ] Discriminated unions for messages
- [ ] Enums for fixed values
- [ ] No `any` types (ESLint rule)

## Code Organization

- [ ] `types.ts` - Type definitions
- [ ] `background.ts` - Service worker
- [ ] `popup.ts` - Popup controller
- [ ] `state.ts` or `telemetry.ts` - Persistence
- [ ] `utils.ts` - Pure utilities
- [ ] Clear separation: background ↔ UI via messages

## Error Handling

- [ ] Try-catch around chrome API calls
- [ ] Graceful fallbacks for storage errors
- [ ] User-friendly error messages
- [ ] Console logging for debugging
- [ ] No silent failures on critical paths

## Testing

- [ ] Vitest configured
- [ ] Chrome API mocks in `tests/setup.ts`
- [ ] `fake-indexeddb` for IndexedDB tests
- [ ] Type guard tests
- [ ] Message handler tests
- [ ] Tests run without browser

## Build & Deploy

- [ ] TypeScript compiles to `dist/js/`
- [ ] HTML copied to `dist/html/`
- [ ] Icons copied to `dist/icons/`
- [ ] Source maps generated
- [ ] `npm run build` produces loadable extension
- [ ] `npm run build:watch` for development

## TypeScript Config

- [ ] `strict: true`
- [ ] `noImplicitAny: true`
- [ ] `noUnusedLocals: true`
- [ ] `exactOptionalPropertyTypes: true`
- [ ] Target: ES2022 or later

## Message Passing

- [ ] Typed message actions (discriminated union)
- [ ] Typed responses (success/error)
- [ ] `sendResponse` called for all messages
- [ ] `return true` for async handlers
- [ ] Error handling in message handlers

```typescript
// Example message types
type Message =
  | { type: 'GET_STATE' }
  | { type: 'UPDATE_CONFIG'; payload: Config }
  | { type: 'TRIGGER_ACTION'; payload: { id: string } };

interface Response<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
}
```

## Security

- [ ] No `innerHTML` (use DOM APIs)
- [ ] Content Security Policy in manifest
- [ ] Input validation on all user data
- [ ] Minimal permissions requested
- [ ] No eval() or dynamic script loading

## Storage

- [ ] IndexedDB for large/structured data
- [ ] chrome.storage.local for simple config
- [ ] Atomic operations where possible
- [ ] Data retention policy (auto-cleanup)
- [ ] Export functionality for user data

## UI/UX

- [ ] Popup loads quickly (<100ms)
- [ ] Visual feedback for actions
- [ ] Loading states for async operations
- [ ] Error states displayed clearly
- [ ] Consistent styling

---

## Quick Validation

```bash
# Check project structure
ls manifest.json src/ts/ dist/

# Check TypeScript strictness
grep -E '"strict":|"noImplicitAny":' tsconfig.json

# Check for any types
grep -rE ": any" src/ts/

# Check message types
grep -E "type Message|interface.*Message" src/ts/types.ts

# Build and verify
npm run build
ls dist/
```
