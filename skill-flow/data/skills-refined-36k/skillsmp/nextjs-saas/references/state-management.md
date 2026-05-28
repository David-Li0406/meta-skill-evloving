# State Management

## Philosophy: Context Over Redux

For most SaaS applications, React Context + localStorage is sufficient. Only consider external state management (Zustand, Redux) when you have:

- Complex state with many actions
- State shared across unrelated component trees
- Time-travel debugging requirements
- Middleware needs (logging, persistence, async)

## Context Pattern

### Basic Context Structure

```typescript
// contexts/tenant-context.tsx
'use client'

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
  useCallback,
} from 'react'

// Types
interface Tenant {
  id: string
  name: string
  slug: string
}

interface TenantContextType {
  tenants: Tenant[]
  activeTenantId: string | null
  activeTenant: Tenant | null
  setActiveTenant: (id: string) => void
  loading: boolean
}

// Context
const TenantContext = createContext<TenantContextType | undefined>(undefined)

// Provider
export function TenantProvider({ children }: { children: ReactNode }) {
  const [tenants, setTenants] = useState<Tenant[]>([])
  const [activeTenantId, setActiveTenantId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  // Derived state
  const activeTenant = tenants.find(t => t.id === activeTenantId) ?? null

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('activeTenantId')
    if (stored) {
      setActiveTenantId(stored)
    }
    setLoading(false)
  }, [])

  // Persist to localStorage on change
  useEffect(() => {
    if (activeTenantId) {
      localStorage.setItem('activeTenantId', activeTenantId)
    }
  }, [activeTenantId])

  const setActiveTenant = useCallback((id: string) => {
    setActiveTenantId(id)
  }, [])

  return (
    <TenantContext.Provider
      value={{
        tenants,
        activeTenantId,
        activeTenant,
        setActiveTenant,
        loading,
      }}
    >
      {children}
    </TenantContext.Provider>
  )
}

// Hook
export function useTenant() {
  const context = useContext(TenantContext)
  if (context === undefined) {
    throw new Error('useTenant must be used within a TenantProvider')
  }
  return context
}
```

### Context with Data Fetching

```typescript
// contexts/projects-context.tsx
'use client'

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
  useCallback,
} from 'react'
import { createClient } from '@/utils/supabase/client'

interface Project {
  id: string
  name: string
  tenant_id: string
  status: 'active' | 'archived'
}

interface ProjectsContextType {
  projects: Project[]
  loading: boolean
  error: string | null
  refresh: () => Promise<void>
  addProject: (project: Omit<Project, 'id'>) => Promise<void>
  updateProject: (id: string, updates: Partial<Project>) => Promise<void>
  deleteProject: (id: string) => Promise<void>
}

const ProjectsContext = createContext<ProjectsContextType | undefined>(undefined)

export function ProjectsProvider({
  children,
  tenantId,
}: {
  children: ReactNode
  tenantId: string | null
}) {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const supabase = createClient()

  const fetchProjects = useCallback(async () => {
    if (!tenantId) {
      setProjects([])
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)

    const { data, error: fetchError } = await supabase
      .from('projects')
      .select('*')
      .eq('tenant_id', tenantId)
      .order('created_at', { ascending: false })

    if (fetchError) {
      setError(fetchError.message)
    } else {
      setProjects(data ?? [])
    }
    setLoading(false)
  }, [tenantId, supabase])

  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  const addProject = async (project: Omit<Project, 'id'>) => {
    const { data, error } = await supabase
      .from('projects')
      .insert(project)
      .select()
      .single()

    if (error) throw new Error(error.message)
    setProjects(prev => [data, ...prev])
  }

  const updateProject = async (id: string, updates: Partial<Project>) => {
    const { data, error } = await supabase
      .from('projects')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw new Error(error.message)
    setProjects(prev => prev.map(p => (p.id === id ? data : p)))
  }

  const deleteProject = async (id: string) => {
    const { error } = await supabase.from('projects').delete().eq('id', id)

    if (error) throw new Error(error.message)
    setProjects(prev => prev.filter(p => p.id !== id))
  }

  return (
    <ProjectsContext.Provider
      value={{
        projects,
        loading,
        error,
        refresh: fetchProjects,
        addProject,
        updateProject,
        deleteProject,
      }}
    >
      {children}
    </ProjectsContext.Provider>
  )
}

export function useProjects() {
  const context = useContext(ProjectsContext)
  if (context === undefined) {
    throw new Error('useProjects must be used within a ProjectsProvider')
  }
  return context
}
```

## Provider Composition

### Root Layout

```typescript
// app/layout.tsx
import { TenantProvider } from '@/contexts/tenant-context'
import { ThemeProvider } from '@/contexts/theme-context'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <TenantProvider>
            {children}
          </TenantProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### Nested Providers (Feature-Specific)

```typescript
// app/(dashboard)/layout.tsx
'use client'

import { useTenant } from '@/contexts/tenant-context'
import { ProjectsProvider } from '@/contexts/projects-context'
import { Sidebar } from '@/components/dashboard/sidebar'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { activeTenantId } = useTenant()

  return (
    <ProjectsProvider tenantId={activeTenantId}>
      <div className="flex h-screen">
        <Sidebar />
        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </ProjectsProvider>
  )
}
```

## Custom Hooks

### useLocalStorage

```typescript
// hooks/use-local-storage.ts
'use client'

import { useState, useEffect, useCallback } from 'react'

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(initialValue)

  useEffect(() => {
    try {
      const item = window.localStorage.getItem(key)
      if (item) {
        setStoredValue(JSON.parse(item))
      }
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error)
    }
  }, [key])

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      try {
        const valueToStore =
          value instanceof Function ? value(storedValue) : value
        setStoredValue(valueToStore)
        window.localStorage.setItem(key, JSON.stringify(valueToStore))
      } catch (error) {
        console.warn(`Error setting localStorage key "${key}":`, error)
      }
    },
    [key, storedValue]
  )

  return [storedValue, setValue]
}
```

### useDebounce

```typescript
// hooks/use-debounce.ts
'use client'

import { useState, useEffect } from 'react'

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(timer)
    }
  }, [value, delay])

  return debouncedValue
}
```

### useMediaQuery

```typescript
// hooks/use-media-query.ts
'use client'

import { useState, useEffect } from 'react'

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const media = window.matchMedia(query)
    setMatches(media.matches)

    const listener = (event: MediaQueryListEvent) => {
      setMatches(event.matches)
    }

    media.addEventListener('change', listener)
    return () => media.removeEventListener('change', listener)
  }, [query])

  return matches
}

export function useMobile() {
  return useMediaQuery('(max-width: 768px)')
}
```

### useAsync

```typescript
// hooks/use-async.ts
'use client'

import { useState, useCallback } from 'react'

interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: Error | null
}

export function useAsync<T, Args extends unknown[]>(
  asyncFunction: (...args: Args) => Promise<T>
) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: false,
    error: null,
  })

  const execute = useCallback(
    async (...args: Args) => {
      setState({ data: null, loading: true, error: null })
      try {
        const data = await asyncFunction(...args)
        setState({ data, loading: false, error: null })
        return data
      } catch (error) {
        setState({ data: null, loading: false, error: error as Error })
        throw error
      }
    },
    [asyncFunction]
  )

  return { ...state, execute }
}
```

## UI State Patterns

### Sidebar State

```typescript
// hooks/use-sidebar.ts
'use client'

import { useLocalStorage } from './use-local-storage'

export function useSidebar() {
  const [collapsed, setCollapsed] = useLocalStorage('sidebar-collapsed', false)
  const [expandedSections, setExpandedSections] = useLocalStorage<string[]>(
    'sidebar-sections',
    []
  )

  const toggleCollapsed = () => setCollapsed(!collapsed)

  const toggleSection = (section: string) => {
    setExpandedSections(prev =>
      prev.includes(section)
        ? prev.filter(s => s !== section)
        : [...prev, section]
    )
  }

  const isSectionExpanded = (section: string) =>
    expandedSections.includes(section)

  return {
    collapsed,
    toggleCollapsed,
    toggleSection,
    isSectionExpanded,
  }
}
```

### Modal State

```typescript
// contexts/modal-context.tsx
'use client'

import { createContext, useContext, useState, ReactNode } from 'react'

type ModalType = 'create-project' | 'edit-tenant' | 'confirm-delete' | null

interface ModalContextType {
  activeModal: ModalType
  modalData: unknown
  openModal: (type: ModalType, data?: unknown) => void
  closeModal: () => void
}

const ModalContext = createContext<ModalContextType | undefined>(undefined)

export function ModalProvider({ children }: { children: ReactNode }) {
  const [activeModal, setActiveModal] = useState<ModalType>(null)
  const [modalData, setModalData] = useState<unknown>(null)

  const openModal = (type: ModalType, data?: unknown) => {
    setActiveModal(type)
    setModalData(data ?? null)
  }

  const closeModal = () => {
    setActiveModal(null)
    setModalData(null)
  }

  return (
    <ModalContext.Provider
      value={{ activeModal, modalData, openModal, closeModal }}
    >
      {children}
    </ModalContext.Provider>
  )
}

export function useModal() {
  const context = useContext(ModalContext)
  if (!context) {
    throw new Error('useModal must be used within a ModalProvider')
  }
  return context
}
```

## When to Use Zustand

If Context becomes unwieldy, consider Zustand:

```typescript
// stores/app-store.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  sidebarCollapsed: boolean
  toggleSidebar: () => void
  activeTenantId: string | null
  setActiveTenant: (id: string) => void
  theme: 'light' | 'dark' | 'system'
  setTheme: (theme: 'light' | 'dark' | 'system') => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      toggleSidebar: () =>
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

      activeTenantId: null,
      setActiveTenant: (id) => set({ activeTenantId: id }),

      theme: 'system',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'app-storage',
    }
  )
)
```
