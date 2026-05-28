# shadcn/ui Setup Guide

Complete setup instructions for integrating shadcn/ui with Next.js.

## Prerequisites

- Next.js 15+ (App Router)
- React 18+
- Tailwind CSS 3.4+

## Initial Setup

### New Next.js Project

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint
cd my-app
```

### Initialize shadcn/ui

```bash
npx shadcn@latest init
```

You'll be prompted to configure:
1. **TypeScript**: Yes (recommended)
2. **Style**: Default or New York
3. **Base color**: Slate, Gray, Zinc, Neutral, or Stone
4. **Global CSS**: app/globals.css or src/app/globals.css
5. **CSS variables**: Yes (recommended)
6. **Tailwind config**: tailwind.config.ts or tailwind.config.js
7. **Components**: components or src/components
8. **Utils**: lib/utils or src/lib/utils
9. **React Server Components**: Yes (if using App Router)
10. **Write to components.json**: Yes

## Project Structure After Init

```
my-app/
├── app/                    # Next.js App Router (or pages/)
├── components/
│   └── ui/                # shadcn components go here
├── lib/
│   └── utils.ts           # cn() utility function
├── components.json        # shadcn configuration
├── tailwind.config.ts     # Tailwind configuration
└── globals.css            # Global styles with CSS variables
```

## Key Files Created

### components.json
Configuration file for shadcn. Controls component installation paths and styling.

### lib/utils.ts
```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```
The `cn()` utility combines class names and handles Tailwind conflicts.

### globals.css
Contains CSS variables for theming:
```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    /* ... more variables */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark mode variables */
  }
}
```

## Adding Components

### Single Component
```bash
npx shadcn@latest add button
```

### Multiple Components
```bash
npx shadcn@latest add button input label card
```

### All Components (not recommended)
```bash
npx shadcn@latest add --all
```

## Common Initial Components

For most projects, start with:
```bash
npx shadcn@latest add button input label card dialog toast
```

## Configuration Options

### Existing Next.js Project

If adding to an existing project, ensure:
1. Tailwind CSS is installed and configured
2. Run `npx shadcn@latest init` in project root
3. Follow prompts to integrate with existing setup

### Custom Paths

Edit `components.json` to customize paths:
```json
{
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

### TypeScript Configuration

Ensure `tsconfig.json` has path aliases:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

## Theme Customization

### Colors

Edit `globals.css` CSS variables:
```css
:root {
  --primary: 262.1 83.3% 57.8%;  /* Change primary color */
  --secondary: 220 14.3% 95.9%;
}
```

Or use HSL values directly:
```css
:root {
  --primary: 220 70% 50%;  /* Blue primary */
}
```

### Dark Mode

shadcn/ui uses `next-themes` for dark mode.

Install next-themes:
```bash
npm install next-themes
```

Wrap app with theme provider (`app/layout.tsx`):
```tsx
import { ThemeProvider } from "next-themes"

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

Add theme toggle:
```tsx
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  const { setTheme, theme } = useTheme()
  return (
    <Button
      variant="outline"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      Toggle theme
    </Button>
  )
}
```

### Typography

Edit Tailwind config for custom fonts:
```typescript
// tailwind.config.ts
import { fontFamily } from "tailwindcss/defaultTheme"

export default {
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-sans)", ...fontFamily.sans],
      },
    },
  },
}
```

Load font in layout:
```tsx
import { Inter } from "next/font/google"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.variable}>{children}</body>
    </html>
  )
}
```

## Icons

shadcn/ui uses Lucide React for icons:

```bash
npm install lucide-react
```

Usage:
```tsx
import { Check, X, Loader2 } from "lucide-react"

<Check className="h-4 w-4" />
<Loader2 className="h-4 w-4 animate-spin" />
```

## Form Validation

For forms with validation, install additional dependencies:

```bash
npm install react-hook-form zod @hookform/resolvers
```

Then add the form component:
```bash
npx shadcn@latest add form
```

## Toast Notifications

Two options:

### Built-in Toast
```bash
npx shadcn@latest add toast
```

Add Toaster to layout:
```tsx
import { Toaster } from "@/components/ui/toaster"

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  )
}
```

### Sonner (Modern Alternative)
```bash
npx shadcn@latest add sonner
```

Add to layout:
```tsx
import { Toaster } from "@/components/ui/sonner"

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  )
}
```

## Troubleshooting

### Components not found
- Check `components.json` paths match your project structure
- Verify path aliases in `tsconfig.json`

### Styling issues
- Ensure Tailwind CSS is properly configured
- Check that `globals.css` is imported in root layout
- Verify CSS variables are defined

### TypeScript errors
- Run `npm install @types/node @types/react @types/react-dom`
- Check that `tsconfig.json` includes necessary paths

### Dark mode not working
- Install `next-themes`: `npm install next-themes`
- Add ThemeProvider to root layout
- Ensure `suppressHydrationWarning` on `<html>` tag

## Best Practices

1. **Install components as needed**: Don't add all components upfront
2. **Use CSS variables**: Enables easy theming and dark mode
3. **Leverage cn() utility**: Properly merge Tailwind classes
4. **Follow naming conventions**: Keep component names from shadcn
5. **Customize cautiously**: Edit generated components in `components/ui/` carefully
6. **Version control**: Commit `components.json` to track configuration
