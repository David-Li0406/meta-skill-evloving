# Angular Code Templates

Ready-to-use templates for common Angular patterns. Copy and adapt these when scaffolding new files.

## Table of Contents
1. [Component Templates](#component-templates)
2. [SignalStore Template](#signalstore-template)
3. [Facade Template](#facade-template)
4. [Test Templates](#test-templates)
5. [Harness Template](#harness-template)

---

## Component Templates

### Smart (Container) Component

```typescript
import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserFacade } from './user.facade';
import { UserCardComponent } from '../ui/user-card.component';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, UserCardComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @if (facade.loading()) {
      <app-spinner />
    } @else if (facade.error()) {
      <app-error [message]="facade.error()" (retry)="facade.loadUsers()" />
    } @else {
      <div class="user-grid">
        @for (user of facade.users(); track user.id) {
          <app-user-card
            [user]="user"
            (select)="onUserSelect($event)"
          />
        }
      </div>
    }
  `,
})
export class UserListComponent {
  protected readonly facade = inject(UserFacade);

  constructor() {
    // Load on init via effect or ngOnInit
    this.facade.loadUsers();
  }

  onUserSelect(userId: string) {
    this.facade.selectUser(userId);
  }
}
```

### Dumb (Presentational) Component

```typescript
import { Component, input, output, ChangeDetectionStrategy } from '@angular/core';
import { User } from '../models/user.model';

@Component({
  selector: 'app-user-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <article class="user-card" (click)="select.emit(user().id)">
      <img [src]="user().avatar" [alt]="user().name" />
      <h3>{{ user().name }}</h3>
      <p>{{ user().email }}</p>
    </article>
  `,
  styles: `
    .user-card {
      cursor: pointer;
      padding: 1rem;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      transition: box-shadow 0.2s;

      &:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }
    }
  `
})
export class UserCardComponent {
  // Signal inputs
  user = input.required<User>();

  // Output events
  select = output<string>();
}
```

---

## SignalStore Template

### Feature SignalStore with Entities

```typescript
import {
  signalStore,
  withState,
  withMethods,
  withComputed,
  patchState
} from '@ngrx/signals';
import { withEntities, setEntities, addEntity, updateEntity, removeEntity } from '@ngrx/signals/entities';
import { inject, computed } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { UserApi } from '../api/user.api';
import { User } from '../models/user.model';

interface UserStoreState {
  selectedId: string | null;
  loading: boolean;
  error: string | null;
  filter: string;
}

export const UserStore = signalStore(
  // Entity management
  withEntities<User>(),

  // Additional state
  withState<UserStoreState>({
    selectedId: null,
    loading: false,
    error: null,
    filter: '',
  }),

  // Computed/derived values
  withComputed((store) => ({
    selectedUser: computed(() => {
      const id = store.selectedId();
      return id ? store.entityMap()[id] : null;
    }),
    filteredUsers: computed(() => {
      const filter = store.filter().toLowerCase();
      if (!filter) return store.entities();
      return store.entities().filter(u =>
        u.name.toLowerCase().includes(filter)
      );
    }),
  })),

  // Methods/actions
  withMethods((store, api = inject(UserApi)) => ({
    async loadAll() {
      patchState(store, { loading: true, error: null });
      try {
        const users = await lastValueFrom(api.getAll());
        patchState(store, setEntities(users), { loading: false });
      } catch (e) {
        patchState(store, { loading: false, error: 'Failed to load users' });
      }
    },

    async create(data: Omit<User, 'id'>) {
      const user = await lastValueFrom(api.create(data));
      patchState(store, addEntity(user));
    },

    async update(id: string, changes: Partial<User>) {
      await lastValueFrom(api.update(id, changes));
      patchState(store, updateEntity({ id, changes }));
    },

    async delete(id: string) {
      await lastValueFrom(api.delete(id));
      patchState(store, removeEntity(id));
    },

    select(id: string | null) {
      patchState(store, { selectedId: id });
    },

    setFilter(filter: string) {
      patchState(store, { filter });
    },
  }))
);
```

---

## Facade Template

### Domain Facade

```typescript
import { Injectable, inject, signal, computed } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { UserGateway } from '../ports/user.gateway';
import { User } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class UserFacade {
  private readonly gateway = inject(UserGateway);

  // State
  private readonly _users = signal<User[]>([]);
  private readonly _loading = signal(false);
  private readonly _error = signal<string | null>(null);
  private readonly _selectedId = signal<string | null>(null);

  // Public read-only signals
  readonly users = this._users.asReadonly();
  readonly loading = this._loading.asReadonly();
  readonly error = this._error.asReadonly();

  // Derived state
  readonly selectedUser = computed(() => {
    const id = this._selectedId();
    return this._users().find(u => u.id === id) ?? null;
  });

  // Actions
  async loadUsers(): Promise<void> {
    this._loading.set(true);
    this._error.set(null);

    try {
      const users = await this.gateway.getAll();
      this._users.set(users);
    } catch (e) {
      this._error.set('Failed to load users');
    } finally {
      this._loading.set(false);
    }
  }

  selectUser(id: string | null): void {
    this._selectedId.set(id);
  }

  async createUser(data: Omit<User, 'id'>): Promise<void> {
    const user = await this.gateway.create(data);
    this._users.update(users => [...users, user]);
  }
}
```

---

## Test Templates

### Sociable Component Test

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { provideHttpClient } from '@angular/common/http';
import { provideNoopAnimations } from '@angular/platform-browser/animations';
import { setupServer } from 'msw/node';

import { UserListComponent } from './user-list.component';
import { UserListHarness } from './user-list.harness';
import { getUsersMockHandler } from '../../api/endpoints/users.msw';

// MSW Setup
const server = setupServer(...getUsersMockHandler());

describe('UserListComponent (Sociable)', () => {
  let fixture: ComponentFixture<UserListComponent>;
  let harness: UserListHarness;

  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserListComponent],
      providers: [
        provideHttpClient(),
        provideNoopAnimations(),
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(UserListComponent);
    await fixture.whenStable();

    const loader = TestbedHarnessEnvironment.loader(fixture);
    harness = await loader.getHarness(UserListHarness);
  });

  it('should display users from API', async () => {
    const users = await harness.getDisplayedUsers();
    expect(users.length).toBeGreaterThan(0);
  });

  it('should show loading state', async () => {
    // Component loads on init, loading should briefly show
    expect(await harness.isLoading()).toBe(false); // Already loaded
  });

  it('should handle API errors', async () => {
    server.use(
      getUsersMockHandler((req, res, ctx) => res(ctx.status(500)))
    );

    // Force reload
    await harness.refresh();

    expect(await harness.getErrorMessage()).toBe('Failed to load users');
  });

  it('should select user on click', async () => {
    await harness.selectUser(0);

    const selected = await harness.getSelectedUserId();
    expect(selected).toBeTruthy();
  });
});
```

### SignalStore Unit Test

```typescript
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { setupServer } from 'msw/node';

import { UserStore } from './user.store';
import { getUsersMockHandler, createUserMockHandler } from '../../api/endpoints/users.msw';

const server = setupServer(
  ...getUsersMockHandler(),
  ...createUserMockHandler()
);

describe('UserStore', () => {
  let store: InstanceType<typeof UserStore>;

  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        UserStore,
      ],
    });
    store = TestBed.inject(UserStore);
  });

  describe('loadAll', () => {
    it('should load users from API', async () => {
      expect(store.entities().length).toBe(0);

      await store.loadAll();

      expect(store.entities().length).toBeGreaterThan(0);
      expect(store.loading()).toBe(false);
      expect(store.error()).toBeNull();
    });

    it('should handle errors', async () => {
      server.use(
        getUsersMockHandler((req, res, ctx) => res(ctx.status(500)))
      );

      await store.loadAll();

      expect(store.error()).toBe('Failed to load users');
      expect(store.loading()).toBe(false);
    });
  });

  describe('filteredUsers', () => {
    it('should filter by name', async () => {
      await store.loadAll();

      store.setFilter('john');

      const filtered = store.filteredUsers();
      expect(filtered.every(u => u.name.toLowerCase().includes('john'))).toBe(true);
    });
  });

  describe('selection', () => {
    it('should track selected user', async () => {
      await store.loadAll();
      const firstUser = store.entities()[0];

      store.select(firstUser.id);

      expect(store.selectedUser()).toEqual(firstUser);
    });
  });
});
```

---

## Harness Template

### Component Harness

```typescript
import { ComponentHarness, HarnessPredicate } from '@angular/cdk/testing';

export class UserListHarness extends ComponentHarness {
  static hostSelector = 'app-user-list';

  // Locators
  protected getSpinner = this.locatorForOptional('app-spinner');
  protected getError = this.locatorForOptional('app-error');
  protected getUserCards = this.locatorForAll('app-user-card');
  protected getRefreshButton = this.locatorForOptional('button.refresh');

  // Static factory for filtering
  static with(options: { hasUsers?: boolean } = {}): HarnessPredicate<UserListHarness> {
    return new HarnessPredicate(UserListHarness, options);
  }

  // Query methods
  async isLoading(): Promise<boolean> {
    const spinner = await this.getSpinner();
    return spinner !== null;
  }

  async hasError(): Promise<boolean> {
    const error = await this.getError();
    return error !== null;
  }

  async getErrorMessage(): Promise<string | null> {
    const error = await this.getError();
    if (!error) return null;
    return error.text();
  }

  async getDisplayedUsers(): Promise<string[]> {
    const cards = await this.getUserCards();
    return Promise.all(cards.map(card => card.text()));
  }

  async getUserCount(): Promise<number> {
    const cards = await this.getUserCards();
    return cards.length;
  }

  // Action methods
  async selectUser(index: number): Promise<void> {
    const cards = await this.getUserCards();
    if (index >= cards.length) {
      throw new Error(`User index ${index} out of bounds`);
    }
    await cards[index].click();
  }

  async refresh(): Promise<void> {
    const button = await this.getRefreshButton();
    if (!button) {
      throw new Error('Refresh button not found');
    }
    await button.click();
  }

  async getSelectedUserId(): Promise<string | null> {
    const host = await this.host();
    return host.getAttribute('data-selected-id');
  }
}
```

### Child Component Harness

```typescript
import { ComponentHarness } from '@angular/cdk/testing';

export class UserCardHarness extends ComponentHarness {
  static hostSelector = 'app-user-card';

  protected getNameElement = this.locatorFor('h3');
  protected getEmailElement = this.locatorFor('p');
  protected getAvatar = this.locatorFor('img');

  async getName(): Promise<string> {
    const el = await this.getNameElement();
    return el.text();
  }

  async getEmail(): Promise<string> {
    const el = await this.getEmailElement();
    return el.text();
  }

  async getAvatarSrc(): Promise<string | null> {
    const img = await this.getAvatar();
    return img.getAttribute('src');
  }

  async click(): Promise<void> {
    const host = await this.host();
    await host.click();
  }
}
```

---

## Directory Structure Template

```
feature-name/
├── feature-name.component.ts      # Smart component
├── feature-name.component.spec.ts # Sociable test
├── feature-name.harness.ts        # Test harness
├── feature-name.store.ts          # SignalStore (if needed)
├── feature-name.facade.ts         # Facade (alternative to store)
├── feature-name.routes.ts         # Route config
├── models/
│   └── feature.model.ts           # Domain models
├── ui/
│   ├── child.component.ts         # Dumb components
│   └── child.harness.ts           # Child harnesses
└── api/
    └── feature.api.ts             # HTTP service (or use generated)
```
