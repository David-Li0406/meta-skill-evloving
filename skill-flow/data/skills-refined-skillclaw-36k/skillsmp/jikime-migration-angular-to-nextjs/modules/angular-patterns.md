# Angular Patterns Migration

Detailed patterns for migrating Angular components, services, and templates to Next.js.

## Component Migration

### Full Component Example

**Before (Angular)**:
```typescript
// user-profile.component.ts
@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss']
})
export class UserProfileComponent implements OnInit, OnDestroy {
  @Input() userId!: string;
  @Output() profileUpdated = new EventEmitter<User>();

  user: User | null = null;
  isLoading = true;
  private destroy$ = new Subject<void>();

  constructor(
    private userService: UserService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.userService.getUser(this.userId)
      .pipe(takeUntil(this.destroy$))
      .subscribe(user => {
        this.user = user;
        this.isLoading = false;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onSave(): void {
    if (this.user) {
      this.profileUpdated.emit(this.user);
    }
  }
}
```

```html
<!-- user-profile.component.html -->
<div class="profile" *ngIf="!isLoading; else loading">
  <h1>{{ user?.name }}</h1>
  <p>{{ user?.email }}</p>
  <button (click)="onSave()">Save</button>
</div>

<ng-template #loading>
  <div class="spinner">Loading...</div>
</ng-template>
```

**After (Next.js)**:
```tsx
// components/user-profile.tsx
'use client'

import { useUser } from '@/hooks/useUser'

interface UserProfileProps {
  userId: string
  onProfileUpdated?: (user: User) => void
}

export function UserProfile({ userId, onProfileUpdated }: UserProfileProps) {
  const { user, isLoading } = useUser(userId)

  const handleSave = () => {
    if (user && onProfileUpdated) {
      onProfileUpdated(user)
    }
  }

  if (isLoading) {
    return <div className="spinner">Loading...</div>
  }

  return (
    <div className="profile">
      <h1>{user?.name}</h1>
      <p>{user?.email}</p>
      <button onClick={handleSave}>Save</button>
    </div>
  )
}
```

---

## Lifecycle Hooks Mapping

| Angular | React | Notes |
|---------|-------|-------|
| `ngOnInit` | `useEffect(() => {}, [])` | Empty deps = mount |
| `ngOnDestroy` | `useEffect` cleanup | Return cleanup function |
| `ngOnChanges` | `useEffect` with deps | Add changed props to deps |
| `ngAfterViewInit` | `useEffect` + `useRef` | For DOM access |
| `ngDoCheck` | Rarely needed | React handles this |

### Lifecycle Example

**Before (Angular)**:
```typescript
export class DataComponent implements OnInit, OnChanges, OnDestroy {
  @Input() dataId!: string;
  private subscription?: Subscription;

  ngOnInit(): void {
    console.log('Component initialized');
    this.loadData();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['dataId'] && !changes['dataId'].firstChange) {
      this.loadData();
    }
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  private loadData(): void {
    this.subscription = this.service.getData(this.dataId).subscribe();
  }
}
```

**After (React)**:
```tsx
'use client'

import { useEffect } from 'react'

interface DataComponentProps {
  dataId: string
}

export function DataComponent({ dataId }: DataComponentProps) {
  // ngOnInit + ngOnChanges combined
  useEffect(() => {
    console.log('Component initialized or dataId changed')
    const controller = new AbortController()

    loadData(dataId, controller.signal)

    // ngOnDestroy equivalent (cleanup)
    return () => {
      controller.abort()
    }
  }, [dataId]) // Re-run when dataId changes

  return <div>Data for {dataId}</div>
}
```

---

## Template Syntax Conversion

### Conditionals

```html
<!-- Angular -->
<div *ngIf="isVisible">Visible content</div>
<div *ngIf="user; else noUser">{{ user.name }}</div>
<ng-template #noUser>No user found</ng-template>

<!-- Angular 17+ -->
@if (isVisible) {
  <div>Visible content</div>
}
```

```tsx
// React/Next.js
{isVisible && <div>Visible content</div>}

{user ? <div>{user.name}</div> : <div>No user found</div>}
```

### Loops

```html
<!-- Angular -->
<ul>
  <li *ngFor="let item of items; let i = index; trackBy: trackById">
    {{ i }}: {{ item.name }}
  </li>
</ul>

<!-- Angular 17+ -->
@for (item of items; track item.id; let i = $index) {
  <li>{{ i }}: {{ item.name }}</li>
}
```

```tsx
// React/Next.js
<ul>
  {items.map((item, i) => (
    <li key={item.id}>
      {i}: {item.name}
    </li>
  ))}
</ul>
```

### Switch

```html
<!-- Angular -->
<div [ngSwitch]="status">
  <span *ngSwitchCase="'active'">Active</span>
  <span *ngSwitchCase="'pending'">Pending</span>
  <span *ngSwitchDefault>Unknown</span>
</div>

<!-- Angular 17+ -->
@switch (status) {
  @case ('active') { <span>Active</span> }
  @case ('pending') { <span>Pending</span> }
  @default { <span>Unknown</span> }
}
```

```tsx
// React/Next.js
const StatusBadge = ({ status }: { status: string }) => {
  switch (status) {
    case 'active':
      return <span>Active</span>
    case 'pending':
      return <span>Pending</span>
    default:
      return <span>Unknown</span>
  }
}
```

---

## Pipes → Utility Functions

**Before (Angular Pipes)**:
```typescript
// date-format.pipe.ts
@Pipe({ name: 'dateFormat' })
export class DateFormatPipe implements PipeTransform {
  transform(value: Date, format: string): string {
    return formatDate(value, format, 'en-US');
  }
}

// Usage in template
{{ createdAt | dateFormat:'short' }}
```

**After (Utility Function)**:
```typescript
// lib/utils/date.ts
import { format } from 'date-fns'

export function formatDate(date: Date, formatStr: string): string {
  return format(date, formatStr)
}

// Usage in component
{formatDate(createdAt, 'PP')}
```

### Common Pipe Conversions

| Angular Pipe | Next.js Equivalent |
|--------------|-------------------|
| `date` | `date-fns` format |
| `currency` | `Intl.NumberFormat` |
| `uppercase` / `lowercase` | String methods |
| `json` | `JSON.stringify` |
| `async` | `useSWR` / `useState` |
| `slice` | Array `.slice()` |
| `keyvalue` | `Object.entries()` |

---

## Directives → Hooks/Components

### Structural Directive → Component

**Before (Angular Directive)**:
```typescript
@Directive({ selector: '[appPermission]' })
export class PermissionDirective {
  @Input() set appPermission(permission: string) {
    if (!this.authService.hasPermission(permission)) {
      this.viewContainer.clear();
    } else {
      this.viewContainer.createEmbeddedView(this.templateRef);
    }
  }
}

// Usage
<button *appPermission="'admin'">Admin Only</button>
```

**After (React Component)**:
```tsx
// components/permission-gate.tsx
'use client'

import { useAuth } from '@/hooks/useAuth'

interface PermissionGateProps {
  permission: string
  children: React.ReactNode
}

export function PermissionGate({ permission, children }: PermissionGateProps) {
  const { hasPermission } = useAuth()

  if (!hasPermission(permission)) {
    return null
  }

  return <>{children}</>
}

// Usage
<PermissionGate permission="admin">
  <button>Admin Only</button>
</PermissionGate>
```

### Attribute Directive → Custom Hook

**Before (Angular Directive)**:
```typescript
@Directive({ selector: '[appClickOutside]' })
export class ClickOutsideDirective {
  @Output() appClickOutside = new EventEmitter<void>();

  @HostListener('document:click', ['$event'])
  onClick(event: Event): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.appClickOutside.emit();
    }
  }
}
```

**After (Custom Hook)**:
```typescript
// hooks/useClickOutside.ts
import { useEffect, RefObject } from 'react'

export function useClickOutside(
  ref: RefObject<HTMLElement>,
  handler: () => void
) {
  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return
      }
      handler()
    }

    document.addEventListener('mousedown', listener)
    document.addEventListener('touchstart', listener)

    return () => {
      document.removeEventListener('mousedown', listener)
      document.removeEventListener('touchstart', listener)
    }
  }, [ref, handler])
}

// Usage
const dropdownRef = useRef<HTMLDivElement>(null)
useClickOutside(dropdownRef, () => setIsOpen(false))
```

---

Version: 1.0.0
Source: jikime-migration-angular-to-nextjs SKILL.md
