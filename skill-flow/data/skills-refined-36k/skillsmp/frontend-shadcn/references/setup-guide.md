# Vite + React + Tailwind + shadcn/ui + React Router v7 Stack Setup Guide

This guide documents the complete process for bootstrapping a modern React application with this stack. Based on actual implementation experience and reference patterns.

## Prerequisites

- Node.js 22.x
- npm

### Node.js Version Management with asdf

Use [asdf](https://asdf-vm.com/) to manage Node.js versions consistently across the team:

```bash
# Install Node.js plugin (one-time setup)
asdf plugin add nodejs

# Set project Node.js version (creates .tool-versions file)
asdf set nodejs latest:22
```

The `.tool-versions` file created by `asdf set` ensures all team members use the same Node.js version.

## Step-by-Step Setup

### 1. Initialize Vite Project

```bash
npm create vite@latest . -- --template react-ts
npm install
```

**Commit:** `feat: initialize Vite project with React + TypeScript`

This creates the base React 19 + TypeScript project with Vite 7.x.

---

### 2. Install Tailwind CSS

```bash
npm install tailwindcss @tailwindcss/vite
```

**Note:** Tailwind v4 uses `@tailwindcss/vite` plugin instead of PostCSS config.

**Commit:** `build: install Tailwind CSS with @tailwindcss/vite plugin`

---

### 3. Configure Tailwind and Path Aliases

**Install @types/node for path resolution:**

```bash
npm install -D @types/node
```

**Update `vite.config.ts`:**

```typescript
import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

**Update `src/index.css`** (replace all content):

```css
@import "tailwindcss";
```

**Update `tsconfig.json`** (add compilerOptions):

```json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Update `tsconfig.app.json`** (add to compilerOptions):

```json
{
  "compilerOptions": {
    // ... existing options ...
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Commit:** `config: configure Tailwind CSS and TypeScript path aliases`

---

### 4. Initialize shadcn/ui

```bash
npx shadcn@latest init --base-color neutral
```

This will:

- Create `components.json`
- Update `src/index.css` with CSS variables and theme
- Create `src/lib/utils.ts` with `cn()` helper
- Install required dependencies (clsx, tailwind-merge, etc.)

**Interactive prompts (if not using --base-color):**

- Style: New York
- Base color: Neutral (or your preference)
- CSS variables: Yes

**Commit:** `feat: initialize shadcn/ui with Neutral color scheme`

---

### 5. Install React Router v7

**IMPORTANT:** React Router v7 uses the package name `react-router`, NOT `react-router-dom`.

```bash
npm install react-router
```

**Commit:** `build: install React Router v7`

---

### 6. Set Up React Router

**Update `src/main.tsx`:**

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
```

**Update `src/App.tsx`:**

```tsx
import { Routes, Route } from 'react-router'

function App() {
  return (
    <Routes>
      <Route path="/" element={<div>Home</div>} />
    </Routes>
  )
}

export default App
```

**Key imports from `react-router`:**

- `BrowserRouter` - Wrap app in main.tsx
- `Routes`, `Route` - Define routes in App.tsx
- `Link` - Navigation links
- `useLocation` - Get current path
- `useParams` - Get route params
- `useSearchParams` - Get/set query params
- `Outlet` - Render child routes

---

### 7. Add shadcn/ui Components

Add components as needed:

```bash
npx shadcn@latest add sidebar -y
npx shadcn@latest add card -y
npx shadcn@latest add button -y
npx shadcn@latest add collapsible -y
# etc.
```

The sidebar component includes many dependencies automatically:

- button, separator, sheet, tooltip, input, skeleton

**Commit each component addition separately or batch related ones.**

---

### 8. Create App Shell Structure

**Create `src/components/AppShell.tsx`:**

```tsx
import { Outlet } from 'react-router'
import { SidebarTrigger } from '@/components/ui/sidebar'

export function AppShell() {
  return (
    <div className="flex-1 flex flex-col h-screen bg-background">
      <header className="flex h-14 items-center gap-4 border-b bg-background px-4 lg:px-6">
        <SidebarTrigger />
        <div className="flex-1" />
      </header>
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
```

**Create `src/components/AppSidebar.tsx`:**

```tsx
import { useLocation, Link } from "react-router";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Home } from "lucide-react";

export function AppSidebar() {
  const location = useLocation();

  return (
    <Sidebar>
      <SidebarHeader className="border-b px-4 py-4">
        <span className="font-semibold">App Name</span>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive={location.pathname === '/'}>
                  <Link to="/">
                    <Home className="mr-2 h-4 w-4" />
                    Home
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
```

**Update `src/App.tsx` with layout:**

```tsx
import { Routes, Route } from 'react-router'
import { SidebarProvider } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/AppSidebar'
import { AppShell } from '@/components/AppShell'

function App() {
  return (
    <Routes>
      <Route path="/" element={
        <SidebarProvider>
          <AppSidebar />
          <AppShell />
        </SidebarProvider>
      }>
        <Route index element={<HomePage />} />
        <Route path="other" element={<OtherPage />} />
      </Route>
    </Routes>
  )
}
```

---

### 9. Optional: Add MapLibre GL JS

```bash
npm install maplibre-gl
```

**Commit:** `build: install MapLibre GL JS`

**Basic map component:**

```tsx
import { useEffect, useRef } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

export function Map() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
          },
        },
        layers: [{ id: 'osm', type: 'raster', source: 'osm' }],
      },
      center: [-104.99, 39.74],
      zoom: 10,
    });

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  return <div ref={mapContainer} style={{ height: 500 }} />;
}
```

**Important:** Import the CSS file for proper map styling.

---

## File Structure After Setup

```
├── .claude/
│   └── CLAUDE.md           # Project documentation
├── src/
│   ├── components/
│   │   ├── ui/             # shadcn/ui components (auto-generated)
│   │   ├── AppShell.tsx
│   │   └── AppSidebar.tsx
│   ├── hooks/
│   │   └── use-mobile.ts   # From shadcn sidebar
│   ├── lib/
│   │   └── utils.ts        # cn() helper
│   ├── pages/              # Route components
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css           # Tailwind + shadcn theme
├── components.json         # shadcn/ui config
├── tsconfig.json
├── tsconfig.app.json
├── vite.config.ts
└── package.json
```

---

## Key Patterns

### Sidebar Navigation with Active State

```tsx
<SidebarMenuButton asChild isActive={location.pathname === '/path'}>
  <Link to="/path">
    <Icon className="mr-2 h-4 w-4" />
    Label
  </Link>
</SidebarMenuButton>
```

### Collapsible Sidebar Sections

```tsx
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";

<Collapsible defaultOpen className="group/collapsible">
  <SidebarMenuItem>
    <CollapsibleTrigger asChild>
      <SidebarMenuButton>
        <Icon className="mr-2 h-4 w-4" />
        Section
        <ChevronDown className="ml-auto h-4 w-4 transition-transform group-data-[state=open]/collapsible:rotate-180" />
      </SidebarMenuButton>
    </CollapsibleTrigger>
    <CollapsibleContent>
      <SidebarMenuSub>
        {/* Sub items */}
      </SidebarMenuSub>
    </CollapsibleContent>
  </SidebarMenuItem>
</Collapsible>
```

### Nested Routes with Outlet

```tsx
// Parent route renders layout + Outlet
<Route path="/" element={<Layout />}>
  {/* Child routes render into Outlet */}
  <Route index element={<Home />} />
  <Route path="about" element={<About />} />
</Route>
```

---

## VSCode Debugging

Configure VSCode to debug the Vite dev server and React application.

### Launch Configuration

**Create `.vscode/launch.json`:**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Dev Server",
      "type": "node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "npx",
      "runtimeArgs": ["vite"],
      "skipFiles": ["<node_internals>/**", "**/node_modules/**"],
      "console": "integratedTerminal"
    },
    {
      "name": "Debug in Chrome",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src",
      "sourceMaps": true
    }
  ]
}
```

**Key patterns:**

- "Debug Dev Server" runs Vite with Node.js debugging for server-side breakpoints
- "Debug in Chrome" launches Chrome with DevTools protocol for client-side React debugging
- `webRoot` maps to `src/` for accurate source map resolution
- Default Vite port is `5173`

### Using the Debugger

**For client-side React debugging:**

1. Start the dev server: `npm run dev`
2. Select "Debug in Chrome" and press `F5`
3. Set breakpoints in React components (`.tsx` files)
4. Breakpoints pause execution in Chrome with VSCode controls

**Commit:** `config: add VSCode debugging configuration`

---

## Commit Message Format

```
<type>: <short description>

[Command: <npm/npx command if applicable>]
[- Additional context bullet points]
```

**Types:**

- `feat` - New feature
- `fix` - Bug fix
- `build` - Dependency changes
- `config` - Configuration changes
- `docs` - Documentation
- `chore` - Maintenance

**Examples:**

```
feat: initialize Vite project with React + TypeScript

Command: npm create vite@latest . -- --template react-ts && npm install
```

```
config: configure Tailwind CSS and TypeScript path aliases

Command: npm install -D @types/node
- Updated src/index.css with Tailwind import
- Added baseUrl and paths to tsconfig.json and tsconfig.app.json
- Updated vite.config.ts with tailwindcss plugin and path aliases
```

---

## Common Issues

### TypeScript Path Alias Errors

Ensure `baseUrl` and `paths` are in BOTH `tsconfig.json` and `tsconfig.app.json`.

### Unused Variable Errors

TypeScript is strict by default. Use `_varName` prefix for intentionally unused variables.

### React Router Import Errors

Use `react-router` not `react-router-dom` for v7.

### Tailwind Classes Not Working

Ensure `@import "tailwindcss";` is at the top of `index.css`.

### shadcn Components Not Styled

The `index.css` must have the CSS variables that `npx shadcn init` adds.

---

## shadcn/ui Component Reference

Common components to add:

```bash
npx shadcn@latest add button card sidebar collapsible dropdown-menu avatar separator sheet tooltip input skeleton badge tabs dialog alert
```

Search for components and get examples using the bundled MCP tools. See [mcp-tools.md](mcp-tools.md) for usage details.
