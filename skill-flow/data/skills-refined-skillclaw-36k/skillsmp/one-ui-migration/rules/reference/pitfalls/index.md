# Common Migration Pitfalls - Index

This document has been split into multiple files for better organization. Please refer to the specific files below:

## File Structure

| File | Topics |
|------|--------|
| [translation-layout.md](./translation-layout.md) | Translation keys, form layout, page styling, gl-page-content, table toolbar |
| [ddd-violations.md](./ddd-violations.md) | DDD architecture violations (5 types) |
| [angular-syntax.md](./angular-syntax.md) | Angular syntax pitfalls, signals, control flow |
| [forms-services.md](./forms-services.md) | Forms, services, directives, constants |

---

## Quick Reference

### Translation & Layout
- ⚠️ Translation Keys - MUST Match Source Exactly
- ⚠️ Form Layout - MUST Match Source Exactly
- ⚠️ Page Component Styling - NO Padding
- ⚠️ Page Layout - MUST Use gl-page-content
- ⚠️ Table Toolbar Button Order

### DDD Architecture Violations
- ❌ Violation 0: Page Form Template in Features Layer (MOST COMMON)
- ❌ Violation 1: UI Component Injecting Store
- ❌ Violation 2: Dialog in UI Layer
- ❌ Violation 3: Business Logic in Features
- ❌ Violation 4: Form with HTTP Calls in UI
- ❌ Violation 5: Shared Component in Wrong Layer

### Angular Syntax Pitfalls
- Mixing Old and New Control Flow
- Forgetting `track` in `@for`
- Using Module-based Patterns
- Not Using Signals with SignalStore
- mxLabelOptionalText - Use Default Value
- langChanged() Must Be Called in Injection Context
- Constructor vs inject() with Field Initializers
- input() vs @Input() Signal Behavior
- output() vs @Output() EventEmitter
- computed() vs effect() Usage
- viewChild() Signal Query

### Forms & Services
- ⚠️ Constants and Enums - Don't Create Separate Definition Files
- ⚠️ Service Usage - Use MxSnackbarService
- ⚠️ Form Controls - Use controls.xxx Instead of .get()
- ⚠️ Effect with Form Controls - MUST Use toSignal()
- ⚠️ Empty Value Display - Use EMPTY_DASH
- ⚠️ appNumberOnly Directive - MUST Migrate to oneUiNumberOnly
- ⚠️ Password Fields - Use mx-password-input
- ⚠️ Readonly Display - Use mx-key-value
