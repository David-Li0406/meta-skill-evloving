# Simple Next.js Project Setup

**Duration**: 15-30 minutes
**Use For**: Blogs, marketing sites, portfolios, simple applications
**Approach**: Streamlined, template-driven, minimal configuration

---

## Overview

This guide provides a fast path for setting up standard Next.js projects without complex requirements. Perfect for:
- Personal blogs or portfolios
- Marketing websites
- Documentation sites
- Simple content-driven applications
- Learning projects

**Not for**: Projects requiring database, custom auth, multi-tenant architecture, or complex integrations (use complex path instead).

---

## Workflow (CoD^Σ)

```
Template_Selection ← Vercel_MCP(search ∧ filter)
  ↓
Project_Setup ← {install, env_vars, config}
  ↓
Components ← Shadcn_MCP(Search → View → Example → Install)
  ↓
Design_System ← {tailwind_config, css_variables}
  ↓
Documentation ← {README, CLAUDE.md}
  ↓
Ready_to_Build
```

---

## Phase 1: Template Selection

### 1.1 Identify Requirements

Quick assessment:
- **Content type**: Blog, marketing, portfolio, docs?
- **Styling needs**: Pre-styled or custom?
- **Features needed**: SEO, RSS, sitemap, analytics?

### 1.2 Use Vercel MCP to Find Template

**Available simple templates** (from catalog):
- **Next.js Boilerplate** - Minimal starting point
- **Blog Starter Kit** - Markdown-based blog
- **Portfolio Starter Kit** - Portfolio + blog with MDX
- **Nextra Docs** - Documentation site
- **Next.js Commerce** - E-commerce (Shopify)

**Selection criteria**:
```
IF blog_only THEN Blog_Starter_Kit
ELSE IF portfolio_with_blog THEN Portfolio_Starter_Kit
ELSE IF documentation THEN Nextra_Docs
ELSE IF e_commerce THEN Next_JS_Commerce
ELSE Next_JS_Boilerplate
```

### 1.3 Install Template

**Method 1: NPM (Recommended)**
```bash
npx create-next-app@latest my-project --example [template-name]
cd my-project
```

**Method 2: Vercel CLI**
```bash
vercel --cwd ./my-project
```

**Examples**:
```bash
# Blog
npx create-next-app@latest my-blog --example blog-starter

# Portfolio
npx create-next-app@latest my-portfolio --example https://github.com/vercel/examples/tree/main/solutions/blog

# Docs
git clone https://github.com/shuding/nextra-docs-template my-docs
```

---

## Phase 2: Basic Setup

### 2.1 Install Dependencies

```bash
npm install
# or
pnpm install
# or
yarn install
```

### 2.2 Environment Variables

Create `.env.local`:
```bash
# If using analytics
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id

# If using external CMS (optional)
CMS_API_KEY=your-cms-key

# Base URL for production
NEXT_PUBLIC_BASE_URL=https://yourdomain.com
```

### 2.3 Verify Installation

```bash
npm run dev
```

Visit `http://localhost:3000` - confirm template loads correctly.

---

## Phase 3: Component Setup

### 3.1 Install Shadcn UI

**CRITICAL WORKFLOW**: Always follow `Search → View → Example → Install`

**Initialize Shadcn**:
```bash
npx shadcn@latest init
```

**Configuration prompts**:
- TypeScript: Yes
- Style: New York or Default
- Color: Slate (or preferred)
- CSS variables: Yes (✅ required)
- Tailwind config: Yes
- Components directory: `@/components`
- Utils directory: `@/lib/utils`

### 3.2 Install Core Components

**Recommended core set**:
```bash
# Navigation & Layout
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add separator

# Forms & Input (if needed)
npx shadcn@latest add input
npx shadcn@latest add textarea
npx shadcn@latest add label

# Feedback
npx shadcn@latest add toast
npx shadcn@latest add alert
```

**IMPORTANT RULES**:
1. Search first: `mcp__shadcn__search_items_in_registries([@ui], "component-name")`
2. View details: `mcp__shadcn__view_items_in_registries(["@ui/component"])`
3. Get example: `mcp__shadcn__get_item_examples_from_registries([@ui], "component-demo")`
4. Install: `npx shadcn@latest add component-name`
5. ❌ NEVER skip the Example step
6. ✅ Install one at a time, test each

### 3.3 Verify Components

Create test page:
```tsx
// app/test-components/page.tsx
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

export default function TestPage() {
  return (
    <div className="container mx-auto p-8">
      <Card className="p-6">
        <h1 className="text-2xl font-bold mb-4">Component Test</h1>
        <Button>Test Button</Button>
      </Card>
    </div>
  )
}
```

Visit `/test-components` to verify components render correctly.

---

## Phase 4: Quick Design System

### 4.1 Configure Tailwind CSS

Edit `tailwind.config.ts`:
```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Use CSS variables only (no hardcoded values)
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // Add custom brand colors via CSS variables
        brand: {
          DEFAULT: "hsl(var(--brand))",
          foreground: "hsl(var(--brand-foreground))",
        },
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)"],
        mono: ["var(--font-geist-mono)"],
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config
```

### 4.2 Define CSS Variables

Edit `app/globals.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;

    /* Custom brand colors (optional) */
    --brand: 262 83% 58%;
    --brand-foreground: 210 40% 98%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;

    /* Custom brand colors dark mode */
    --brand: 262 80% 65%;
    --brand-foreground: 222.2 84% 4.9%;
  }
}
```

**RULE**: ✅ Always use CSS variables, ❌ Never hardcode colors in components

### 4.3 Typography Setup

Already included via Geist fonts (Next.js default). Optional: add custom font:

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

---

## Phase 5: Minimal Documentation

### 5.1 Update README.md

```markdown
# [Project Name]

[Brief description of your project]

## Tech Stack

- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Shadcn UI (@ui components)

## Getting Started

\`\`\`bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
\`\`\`

Visit [http://localhost:3000](http://localhost:3000)

## Project Structure

\`\`\`
/app              # App Router pages and layouts
/components/ui    # Shadcn UI components
/public           # Static assets
/lib              # Utility functions
\`\`\`

## Deployment

Deploy to Vercel:

\`\`\`bash
vercel
\`\`\`

Or use the Vercel dashboard for one-click deployment.
```

### 5.2 Create Basic CLAUDE.md

**Template**: Use @templates/claude-md-template.md

**Example**:
```markdown
# [Project Name]

## Overview
[2-3 sentence description]

## Tech Stack
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS + Shadcn UI (@ui)
- [Template name] template

## Development

### Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint

### Conventions
- Mobile-first responsive design
- Use Shadcn components from @ui registry
- Global Tailwind CSS variables only (no inline custom colors)
- Follow Next.js App Router conventions

### Component Usage
- Shadcn workflow: Search → View → Example → Install (never skip Example)
- Test each component after installation
- Keep components in /components/ui

## Anti-Patterns
❌ Hardcoded colors (use CSS variables)
   **Why**: Breaks theme switching and design system consistency

❌ Skipping Shadcn Example step
   **Why**: Examples reveal usage patterns and prevent integration issues

❌ Custom Tailwind without CSS variables
   **Why**: Bypasses design system, requires recompilation for changes

❌ Mixing Pages Router and App Router patterns
   **Why**: Creates conflicts and confusing behavior
```

---

## Phase 6: Verification Checklist

Before marking setup complete:

### ✅ Functional
- [ ] Template installed and running
- [ ] Development server starts without errors
- [ ] All pages load correctly
- [ ] Components render properly
- [ ] Styling works (light and dark mode if applicable)

### ✅ Components
- [ ] Shadcn initialized
- [ ] Core components installed (@ui registry)
- [ ] Components tested individually
- [ ] Examples reviewed for each component

### ✅ Design System
- [ ] Tailwind configured
- [ ] CSS variables defined
- [ ] Colors work in light/dark mode
- [ ] Typography set up
- [ ] No hardcoded colors in code

### ✅ Documentation
- [ ] README.md updated
- [ ] CLAUDE.md created
- [ ] Project structure documented
- [ ] Getting started instructions clear

---

## Common Issues & Solutions

### Issue: Shadcn init fails
**Solution**: Ensure TypeScript and Tailwind are installed first. Check `package.json` for required dependencies.

### Issue: Components don't render
**Solution**: Verify import paths in `tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### Issue: CSS variables not working
**Solution**: Ensure `globals.css` is imported in root layout:
```typescript
// app/layout.tsx
import "./globals.css"
```

### Issue: Dark mode not working
**Solution**: Add `next-themes` provider:
```bash
npm install next-themes
```

Then wrap app in `ThemeProvider` (see Shadcn dark mode docs).

---

## Next Steps

### Option A: Start Building
Begin adding your content and features to the template.

### Option B: Continue with SDD Workflow
If you need product specification and implementation planning:
```
Continue with: specify-feature skill → /plan → /tasks → /implement
```

### Option C: Add More Features
Consider adding:
- Analytics (Vercel Analytics, Google Analytics)
- SEO optimization (next-seo package)
- Content management (MDX, Contentful, Sanity)
- Forms (React Hook Form + Zod validation)

---

## Success Criteria Met

✅ Template selected and installed
✅ Development environment working
✅ Core components configured (Shadcn @ui)
✅ Design system established (CSS variables)
✅ Basic documentation created
✅ Ready to start building features

**Total time**: 15-30 minutes
**Next**: Build your application or continue with specify-feature skill for complex requirements

---

## References

- Template Catalog: @docs/vercel-nextjs-templates-catalog.md
- Shadcn UI: https://ui.shadcn.com
- Next.js Docs: https://nextjs.org/docs
- Tailwind CSS: https://tailwindcss.com/docs
