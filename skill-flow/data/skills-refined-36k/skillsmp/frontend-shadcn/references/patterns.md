# Development Patterns

Patterns for building features in Vite + React + shadcn/ui + Tailwind + React Router v7 projects.

## Project Structure

```
src/
├── components/
│   ├── ui/              # shadcn/ui components (auto-generated)
│   ├── AppShell.tsx     # Main layout with header and outlet
│   └── AppSidebar.tsx   # Navigation sidebar
├── pages/               # Route page components (organized by feature)
│   ├── dashboard/
│   └── settings/
├── hooks/               # Custom React hooks
├── lib/
│   └── utils.ts         # cn() helper and shared utilities
├── App.tsx              # Route definitions
├── main.tsx             # Entry point with BrowserRouter
└── index.css            # Tailwind + shadcn theme variables
```

**Conventions:**

- Use `pages/` directory for page components organized by feature area
- Use shadcn/ui components from `components/ui/` for consistent styling
- Utility functions go in `lib/` directory
- Path alias `@/*` maps to `./src/*`

## Routing Architecture

### React Router v7 Setup

```typescript
// main.tsx - Entry point
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import './index.css'
import App from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
```

```typescript
// App.tsx - Route definitions
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
        <Route index element={<DashboardPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
    </Routes>
  )
}
```

### Key Imports

All routing imports come from `react-router` (NOT `react-router-dom`):

```typescript
import {
  BrowserRouter,    // Wrap app in main.tsx
  Routes, Route,    // Define routes in App.tsx
  Link,             // Navigation links
  Outlet,           // Render child routes
  useLocation,      // Get current path
  useParams,        // Get route params
  useSearchParams,  // Get/set query params
} from 'react-router'
```

### Nested Routes with Outlet

```typescript
// Parent route renders layout + Outlet
<Route path="/" element={<Layout />}>
  {/* Child routes render into Outlet */}
  <Route index element={<Home />} />
  <Route path="about" element={<About />} />
</Route>
```

## State Management

### URL-Based State

Use `useSearchParams` for state that should persist in the URL:

```typescript
const [searchParams, setSearchParams] = useSearchParams()

// Read value
const environment = searchParams.get('env')

// Update value
setSearchParams({ env: 'production' })
```

### Route-Based Logic

Use `useLocation` for determining active states:

```typescript
const location = useLocation()
const isActive = location.pathname === '/dashboard'
```

### Query Parameter Preservation

Create a helper to preserve query params across navigation:

```typescript
function createNavLink(path: string, searchParams: URLSearchParams) {
  const params = searchParams.toString()
  return params ? `${path}?${params}` : path
}
```

## Component Patterns

### Layout System

**AppShell** - Main content wrapper with header:

```typescript
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

**AppSidebar** - Navigation with active states:

```typescript
import { useLocation, Link } from 'react-router'
import {
  Sidebar, SidebarContent, SidebarGroup,
  SidebarGroupContent, SidebarGroupLabel, SidebarHeader,
  SidebarMenu, SidebarMenuButton, SidebarMenuItem,
} from '@/components/ui/sidebar'

export function AppSidebar() {
  const location = useLocation()

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
                    Dashboard
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
```

### Page Components

Consistent structure with header and content sections:

```typescript
export function DashboardPage() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-muted-foreground">Overview of your data</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* Content cards */}
      </div>
    </div>
  )
}
```

### Collapsible Sidebar Sections

```typescript
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { ChevronDown } from 'lucide-react'

<Collapsible defaultOpen className="group/collapsible">
  <SidebarMenuItem>
    <CollapsibleTrigger asChild>
      <SidebarMenuButton>
        <FolderIcon className="mr-2 h-4 w-4" />
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

## UI Patterns

### Common Layouts

- **Two-column layouts** for complex forms
- **Card-based layouts** for dashboards and listings
- **Consistent navigation** with back links and breadcrumbs

### Design Conventions

**shadcn/ui components:**

- Button, Input, Badge, Card, Tabs
- Sidebar, Dialog, Command, Table
- Tooltip, Dropdown Menu, Select

**Tailwind patterns:**

- `bg-muted`, `text-muted-foreground` - Muted backgrounds/text
- `space-y-4`, `gap-4` - Consistent spacing
- `flex-1` - Flexible sizing
- `border-b`, `border-r` - Borders

### Color-Coded Status

```typescript
// Status badges with semantic colors
<Badge variant="default">Active</Badge>      // Primary color
<Badge variant="secondary">Pending</Badge>   // Muted
<Badge variant="destructive">Error</Badge>   // Red
<Badge variant="outline">Draft</Badge>       // Outlined
```

## Development Workflow

### Before Starting Dev Server

Check if a dev server is already running on port 5173:

```bash
lsof -i :5173
```

### Testing Changes

1. Run the dev server and verify navigation works
2. Ensure query parameter preservation across route transitions
3. Verify active states for all sidebar menu items
4. Check conditional rendering for context-dependent sections

### Package Management

- Always use `npm install <package-name>` to add dependencies
- Never manually edit `package.json` to add packages
- Use `npx shadcn@latest add <component> -y` for shadcn components

### Theming Considerations

- Project typically uses light theme only (configure dark mode if needed)
- CSS variables defined in `index.css` control theme colors
- Avoid adding `dark:` classes unless dark mode is implemented
