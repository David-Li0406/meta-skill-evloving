---
name: jikime-migration-angular-to-nextjs
description: |
  Angular to Next.js 16 migration specialist. Handles NgModule decomposition,
  RxJS to React patterns, Dependency Injection to Hooks, and Angular Forms
  to react-hook-form migration. Use when migrating Angular applications.
argument-hint: [source-path]
version: 1.0.0
tags: ["migration", "angular", "nextjs", "react", "rxjs", "app-router"]
triggers:
  keywords: ["angular", "ng", "angular-to-react", "angular-to-nextjs", "NgModule", "RxJS", "앵귤러"]
  phases: ["plan", "run"]
  agents: ["manager-migrate-nextjs", "frontend"]
  languages: ["typescript"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~5000
user-invocable: false
context: fork
agent: Explore
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Angular → Next.js 16 Migration Guide

Comprehensive guide for migrating Angular applications to Next.js 16 with App Router.

## Quick Reference

| Angular | Next.js 16 |
|---------|------------|
| `@Component` | Function component |
| `@Injectable` + DI | Custom hooks / Context |
| `NgModule` | Not needed (remove) |
| `*ngIf` / `*ngFor` | `{condition && ...}` / `.map()` |
| `[(ngModel)]` | Controlled components |
| Angular Router | App Router (file-based) |
| RxJS Observables | React Query / SWR / useState |
| Angular Forms | react-hook-form + zod |
| Services | Custom hooks |
| Guards | Middleware |
| Interceptors | Route handlers / Middleware |
| Pipes | Utility functions |

---

## Migration Workflow

```
┌────────────────────────────────────────────────────────────────┐
│  Phase 1: ANALYZE      Phase 2: DECOMPOSE     Phase 3: MIGRATE │
│  ┌──────────────┐     ┌──────────────┐      ┌──────────────┐  │
│  │   Angular    │────▶│   NgModule   │─────▶│   Component  │  │
│  │   Analysis   │     │   Breakdown  │      │   Migration  │  │
│  └──────────────┘     └──────────────┘      └──────────────┘  │
│         │                                          │           │
│         │            Phase 5: VERIFY         Phase 4: SERVICES │
│         │            ┌──────────────┐      ┌──────────────┐   │
│         └────────────│    Build &   │◀─────│    RxJS →    │   │
│                      │    Test      │      │    Hooks     │   │
│                      └──────────────┘      └──────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## Angular Detection

**Primary Indicators**:
- `@angular/core` in package.json
- `angular.json` configuration file
- `.component.ts`, `.service.ts`, `.module.ts` files

**Version Detection**:
```bash
# Check Angular version
cat package.json | grep "@angular/core"

# Version-specific considerations
# Angular 12-14: Ivy compilation
# Angular 15+: Standalone components available
# Angular 17+: Control flow syntax (@if, @for)
```

---

## Component Migration

### Basic Component

For detailed patterns, see:
- [Angular Patterns](modules/angular-patterns.md) - Component, service, and template migration

**Before (Angular)**:
```typescript
@Component({
  selector: 'app-user-card',
  template: `
    <div class="card">
      <h2>{{ user.name }}</h2>
      <p *ngIf="user.email">{{ user.email }}</p>
    </div>
  `,
  styles: [`
    .card { padding: 16px; border: 1px solid #ccc; }
  `]
})
export class UserCardComponent {
  @Input() user!: User;
  @Output() selected = new EventEmitter<User>();
}
```

**After (Next.js)**:
```tsx
interface UserCardProps {
  user: User
  onSelected?: (user: User) => void
}

export function UserCard({ user, onSelected }: UserCardProps) {
  return (
    <div className="p-4 border border-gray-300 rounded">
      <h2>{user.name}</h2>
      {user.email && <p>{user.email}</p>}
    </div>
  )
}
```

---

## Service → Hook Migration

For detailed RxJS patterns, see:
- [RxJS Migration](modules/rxjs-migration.md) - Observable to React Query/SWR patterns

### Quick Pattern

| Angular Service | Next.js Hook |
|-----------------|--------------|
| `BehaviorSubject` | `useState` + Context |
| `Observable.pipe()` | `useMemo` / derived state |
| `HttpClient.get()` | `fetch` + React Query/SWR |
| `tap()`, `map()` | Function composition |
| `switchMap()` | `useEffect` dependencies |
| `combineLatest()` | Multiple `useSWR` calls |

**Before (Angular Service)**:
```typescript
@Injectable({ providedIn: 'root' })
export class ProductService {
  constructor(private http: HttpClient) {}

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>('/api/products');
  }
}
```

**After (Custom Hook)**:
```typescript
import useSWR from 'swr'

export function useProducts() {
  const { data, error, isLoading } = useSWR<Product[]>(
    '/api/products',
    (url) => fetch(url).then(res => res.json())
  )

  return { products: data ?? [], error, isLoading }
}
```

---

## Forms Migration

For detailed form patterns, see:
- [Forms Migration](modules/forms-migration.md) - Reactive Forms to react-hook-form

### Quick Reference

| Angular Forms | react-hook-form |
|---------------|-----------------|
| `FormGroup` | `useForm()` |
| `FormControl` | `register()` |
| `Validators.required` | `{ required: true }` or Zod |
| `formControlName` | `{...register('name')}` |
| `(ngSubmit)` | `handleSubmit()` |
| `form.valid` | `formState.isValid` |

---

## Routing Migration

### Angular Router → App Router

| Angular | Next.js App Router |
|---------|-------------------|
| `RouterModule.forRoot()` | `app/` directory structure |
| `path: 'users/:id'` | `app/users/[id]/page.tsx` |
| `canActivate` guard | `middleware.ts` |
| `resolve` | Server Component data fetching |
| `routerLink` | `<Link href="...">` |
| `ActivatedRoute` | `useParams()`, `useSearchParams()` |

**Route Structure Mapping**:
```
Angular:                          Next.js:
src/app/                          app/
├── app-routing.module.ts         ├── layout.tsx
├── home/                         ├── page.tsx (home)
│   └── home.component.ts         ├── about/
├── about/                        │   └── page.tsx
│   └── about.component.ts        └── users/
└── users/                            ├── page.tsx
    ├── user-list.component.ts        └── [id]/
    └── user-detail.component.ts          └── page.tsx
```

---

## NgModule Decomposition Strategy

**Step 1**: Identify module boundaries
```
AppModule
├── CoreModule (singleton services)
├── SharedModule (common components)
├── FeatureModule A
└── FeatureModule B
```

**Step 2**: Map to Next.js structure
```
Next.js equivalent:
app/
├── layout.tsx (replaces CoreModule bootstrap)
├── providers.tsx (replaces CoreModule services)
components/
├── ui/ (replaces SharedModule)
└── features/
    ├── feature-a/
    └── feature-b/
lib/
└── hooks/ (replaces injectable services)
```

---

## Dependency Injection → Context/Hooks

### Provider Pattern

**Before (Angular DI)**:
```typescript
@NgModule({
  providers: [
    { provide: API_URL, useValue: 'https://api.example.com' },
    AuthService,
    UserService
  ]
})
export class CoreModule {}
```

**After (React Context)**:
```tsx
// providers.tsx
'use client'

import { createContext, useContext } from 'react'

const ConfigContext = createContext({ apiUrl: '' })

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ConfigContext.Provider value={{ apiUrl: 'https://api.example.com' }}>
      {children}
    </ConfigContext.Provider>
  )
}

export const useConfig = () => useContext(ConfigContext)
```

---

## Target Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Framework | Next.js 16 | App Router architecture |
| Language | TypeScript 5.x | Type safety |
| Styling | Tailwind CSS 4.x | Utility-first CSS |
| UI Components | shadcn/ui | Accessible components |
| State | Zustand | Global state management |
| Forms | react-hook-form + zod | Form handling |
| Data Fetching | SWR or React Query | Server state |
| Icons | lucide-react | Icon library |

---

## Migration Checklist

```markdown
## Pre-Migration
- [ ] Angular version identified (12-17+)
- [ ] NgModule structure documented
- [ ] Services and DI dependencies mapped
- [ ] RxJS usage patterns analyzed
- [ ] Form complexity assessed

## Component Migration
- [ ] Templates converted to JSX
- [ ] @Input/@Output → props
- [ ] Lifecycle hooks → useEffect
- [ ] Pipes → utility functions
- [ ] Directives → custom hooks/components

## Service Migration
- [ ] HttpClient → fetch/SWR
- [ ] BehaviorSubject → useState/Context
- [ ] RxJS operators → useMemo/useEffect
- [ ] Singleton services → Context providers

## Routing Migration
- [ ] Routes converted to file-based
- [ ] Guards → middleware
- [ ] Resolvers → Server Component fetch
- [ ] Lazy loading → dynamic imports

## Verification
- [ ] TypeScript compiles without errors
- [ ] Build succeeds
- [ ] All routes accessible
- [ ] Forms working correctly
- [ ] Data fetching functional
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Missing `'use client'` | Add directive for components with hooks |
| RxJS subscribe leaks | Replace with SWR/React Query |
| NgModule circular deps | Restructure to feature folders |
| Zone.js expectations | Remove, React handles updates |
| Angular CDK usage | Replace with Radix UI primitives |
| `*ngFor` trackBy | Use stable `key` prop |

---

## Works Well With

- `jikime-migration-to-nextjs` - General migration workflow
- `jikime-framework-nextjs@16` - Next.js 16 patterns
- `jikime-lang-typescript` - TypeScript best practices
- `jikime-library-shadcn` - UI component migration

---

Version: 1.0.0
Last Updated: 2026-01-25
Source: Angular Official Docs, Next.js Migration Guide
