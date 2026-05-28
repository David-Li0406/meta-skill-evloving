---
name: css-styling-skill
description: Scans and updates project styling to adhere to the Super League "Dark Mode / Emerald Accent" design system. Use when the user requests style updates, UI polishing, or design system enforcement for Web (Tailwind) or Mobile (React Native).
---

# CSS Styling Skill

## Overview

This skill helps enforce the Super League Enterprise Standards for design and user experience. It provides guidelines and tools to ensure a consistent "Premium Aesthetic" across both Web and Mobile platforms.

**Core Design Principles:**
- **Premium Aesthetic:** Dark Mode with Emerald Accents.
- **Backgrounds:** `zinc-950`
- **Cards/Surfaces:** `zinc-900`
- **Primary Actions:** `emerald-500` (Text: White)
- **Typography:** Consistent, legible, "Inter" (or system default).

## When to Use

Use this skill when:
1.  **Refactoring UI:** Converting arbitrary CSS/Styles to the standard system.
2.  **Creating New Components:** Ensuring new UI matches existing premium look.
3.  **Auditing:** Checking for forbidden or "rogue" styles (e.g., random hex codes).
4.  **Cross-Platform Styling:** Translating web styles to mobile `StyleSheet` properties.

## Styling Guidelines

### 1. Web (Next.js + Tailwind CSS)

The project uses Tailwind CSS v4. Stick to utility classes.

| UI Element | Class(es) | Notes |
| :--- | :--- | :--- |
| **Page Background** | `bg-zinc-950` | Deep dark background |
| **Card / Container** | `bg-zinc-900 border border-zinc-800 rounded-lg` | Subtle border, distinct surface |
| **Primary Button** | `bg-emerald-500 hover:bg-emerald-600 text-white` | Clear call-to-action |
| **Secondary Button** | `bg-zinc-800 hover:bg-zinc-700 text-zinc-100` | Muted action |
| **Text (Body)** | `text-zinc-400` | Readable on dark bg |
| **Text (Heading)** | `text-zinc-50 font-bold` | High contrast |
| **Input Fields** | `bg-zinc-950 border-zinc-800 focus:ring-emerald-500` | Dark input, branded focus |

**Prohibited on Web:**
- **Inline Styles:** Avoid `style={{ ... }}`. Use Tailwind utility classes instead.
- Non-theme hex codes (e.g., `#00ff00`) - use closest Tailwind token.
- Non-theme hex codes (e.g., `#00ff00`) - use closest Tailwind token.
- `!important` unless absolutely necessary for overrides.

### 2. Mobile (React Native)

The mobile app does NOT use NativeWind. Use standard `StyleSheet`.

**Color Palette Map:**
```javascript
export const Colors = {
  background: '#09090b', // zinc-950
  card: '#18181b',       // zinc-900
  border: '#27272a',     // zinc-800
  primary: '#10b981',    // emerald-500
  text: '#fafafa',       // zinc-50
  textMuted: '#a1a1aa',  // zinc-400
};
```

**Common Patterns:**

```javascript
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background, // Match web bg-zinc-950
  },
  card: {
    backgroundColor: Colors.card,       // Match web bg-zinc-900
    borderRadius: 8,                    // Match web rounded-lg
    borderWidth: 1,
    borderColor: Colors.border,         // Match web border-zinc-800
    padding: 16,
  },
  buttonPrimary: {
    backgroundColor: Colors.primary,    // Match web bg-emerald-500
    padding: 12,
    borderRadius: 6,
    alignItems: 'center',
  },
  buttonText: {
    color: '#ffffff',
    fontWeight: '600',
  }
});
```

### 3. General Rules (All Platforms)

**Avoid Inline Styles:**
Inline styles cause performance issues (re-renders) and make code hard to read/maintain.
- **Bad:** `<View style={{ backgroundColor: 'red', padding: 10 }} />`
- **Good:** `<View style={styles.container} />` (Mobile) or `<div className="bg-red-500 p-4" />` (Web)

*Exceptions: Dynamic values (e.g., animations, progress bars) are allowed inline.*


### 3. Styling Best Practices
- **Use `StyleSheet.create`**: Always define styles in a `StyleSheet` object at the bottom of the file. Avoid inline styles (e.g., `style={{ marginTop: 10 }}`) as they cause re-renders and clutter code.
- **Use `Colors` Constant**: Never hardcode hex values. Import `{ Colors }` from `@/constants/Colors` and use the semantic or palette keys.
- **Typography**: Use standard font sizes and weights. Avoid magic numbers.js

## Workflows

### Audit Styles
Run the included script to find hardcoded values that deviate from the system.

```bash
node skills/css-styling-skill/scripts/audit_styles.js
```

### Apply Styles
1.  **Identify** the component platform (Web vs Mobile).
2.  **Web:** Replace inline styles or CSS modules with Tailwind utility classes from the table above.
3.  **Mobile:** Create/Update `StyleSheet` using the `Colors` palette map to match the Web aesthetic.
4.  **Verify:** Check distinct `zinc-900` vs `zinc-950` contrast and ensuring `emerald-500` is the only primary accent.
