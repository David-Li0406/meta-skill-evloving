# Color Semantic Cheat Sheet

**Strict Rule:** Always use the **Semantic Alias** in your code. Never use the Base Palette name or raw Hex/RGB values.

| Semantic Alias | Base Palette | Usage Intent |
| :--- | :--- | :--- |
| **`bg-primary`** | Pacific Blue 600 | Main Call-to-Action (buttons, active states, key branding). |
| **`text-primary-foreground`** | White | Text explicitly placed *on top* of a primary background. |
| **`bg-secondary`** | Porcelain 600 | Alternative actions, "Ghost" buttons, lower emphasis controls. |
| **`text-secondary-foreground`** | White | Text *on top* of secondary elements. |
| **`bg-background`** | Porcelain 50 | The main page background (very light warm gray). |
| **`text-foreground`** | Pacific Blue 950 | The default text color (deep teal/almost black) for the page. |
| **`bg-card`** | White | Background for constrained content cards, modals, and popups. |
| **`bg-muted`** | Porcelain 100 | Subtle backgrounds for disabled states or secondary sections. |
| **`text-muted-foreground`** | Porcelain 700 | Supporting text, captions, or placeholders. |
| **`bg-destructive`** | Tangerine Dream 600 | Destructive actions (Delete, Remove, Revoke). |
| **`bg-accent`** | Pacific Blue 100 | Highlighted items, active dropdown rows, or subtle emphasis. |
| **`border-border`** | Porcelain 200 | Default border color for inputs, dividers, and cards. |
| **`ring-ring`** | Pacific Blue 400 | Focus rings and outlines. |

## Usage Examples

**Correct (Semantic):**

```tsx
<button className="bg-primary text-primary-foreground hover:bg-primary-hover">
  Submit
</button>
```

**Incorrect (Base Palette - AVOID):**

```tsx
<button className="bg-pacific-blue-600 text-white">
  Submit
</button>
```

**Incorrect (Tailwind Default - FORBIDDEN):**

```tsx
<button className="bg-blue-600 text-white">
  Submit
</button>
```
