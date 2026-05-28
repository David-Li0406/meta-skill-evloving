---
name: kmp-ui-bridge
description: Skill for translating web UI patterns (React/Tailwind) to native mobile patterns (Kotlin/Compose Multiplatform).
---

# KMP UI Bridge

This skill provides a translation layer between web and native mobile UI development.

## UI Mapping Guide

### Layouts

| Web (Tailwind) | Mobile (Compose) |
|----------------|------------------|
| `flex flex-col` | `Column` |
| `flex flex-row` | `Row` |
| `grid` | `LazyVerticalGrid` or `Box` |
| `p-4` | `Modifier.padding(16.dp)` |
| `gap-4` | `Arrangement.spacedBy(16.dp)` |
| `items-center` | `Alignment.CenterVertically` |
| `justify-between` | `Arrangement.SpaceBetween` |

### Components

| Web Component | Mobile Component |
|---------------|------------------|
| `<Button>` | `Button` or `IconButton` |
| `<Input>` | `TextField` or `OutlinedTextField` |
| `<img />` | `AsyncImage` (Coil) |
| `<Dialog>` | `AlertDialog` |
| `<toast>` | `Snackbar` |

### Styling

| Tailwind Class | Compose Parameter |
|----------------|-------------------|
| `rounded-lg` | `RoundedCornerShape(8.dp)` |
| `shadow-md` | `Modifier.shadow(elevation = 4.dp)` |
| `bg-primary` | `color = MaterialTheme.colorScheme.primary` |
| `font-bold` | `fontWeight = FontWeight.Bold` |

## Shared Logic Patterns

When moving logic from `src/` to `mobile/shared/`:
1.  Extract purely logical functions into `commonMain`.
2.  Use `Flow` instead of React state for asynchronous data streams.
3.  Implement `Repository` pattern to share API call logic.

## Examples

### translation-example.md
See `resources/translation-example.md` for a side-by-side comparison of a UI component in both platforms.
