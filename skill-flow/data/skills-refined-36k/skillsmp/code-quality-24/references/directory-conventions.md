# Directory Conventions Reference

## 3-Tier Architecture

All code must be organized into three tiers with clear boundaries.

```
project/
├── 01-presentation/    ← UI Layer
├── 02-logic/           ← Business Logic Layer
├── 03-data/            ← Data Layer
└── config/             ← Cross-cutting configuration
```

---

## Tier 1: Presentation (`01-presentation/`)

**Purpose:** Everything the user sees and interacts with.

**Contains:**
- React/Vue/Angular components
- Pages and layouts
- Styles (CSS, SCSS, CSS-in-JS)
- UI state (component-local state)
- Event handlers that call logic layer

**Does NOT contain:**
- Business logic
- Direct database access
- API calls (these go through logic layer)

### Structure

```
01-presentation/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   ├── Button.css
│   │   └── index.ts
│   ├── Card/
│   │   ├── Card.tsx
│   │   ├── Card.test.tsx
│   │   ├── Card.css
│   │   └── index.ts
│   └── index.ts          # Barrel export
├── pages/
│   ├── Dashboard/
│   │   ├── Dashboard.tsx
│   │   ├── Dashboard.test.tsx
│   │   └── index.ts
│   └── Settings/
│       ├── Settings.tsx
│       ├── Settings.test.tsx
│       └── index.ts
├── layouts/
│   ├── MainLayout.tsx
│   └── AuthLayout.tsx
├── hooks/
│   ├── useForm.ts
│   └── useModal.ts
└── styles/
    ├── global.css
    └── variables.css
```

### Component Folder Structure

Every component gets its own folder:

```
ComponentName/
├── ComponentName.tsx      # Main component
├── ComponentName.test.tsx # Tests
├── ComponentName.css      # Styles (if not CSS-in-JS)
├── ComponentName.types.ts # Types (if complex)
└── index.ts               # Re-export
```

**index.ts pattern:**
```typescript
export { ComponentName } from './ComponentName';
export type { ComponentNameProps } from './ComponentName.types';
```

---

## Tier 2: Logic (`02-logic/`)

**Purpose:** All business rules, workflows, and orchestration.

**Contains:**
- Services (business operations)
- Use cases (application workflows)
- Domain models and validation
- API clients
- State management (global state)

**Does NOT contain:**
- UI components
- Direct database queries (use repositories)
- Presentation concerns

### Structure

```
02-logic/
├── services/
│   ├── AuthService.ts
│   ├── AuthService.test.ts
│   ├── PaymentService.ts
│   ├── PaymentService.test.ts
│   └── index.ts
├── use-cases/
│   ├── registerUser.ts
│   ├── registerUser.test.ts
│   ├── processOrder.ts
│   ├── processOrder.test.ts
│   └── index.ts
├── domain/
│   ├── User.ts
│   ├── Order.ts
│   ├── validators/
│   │   ├── emailValidator.ts
│   │   └── orderValidator.ts
│   └── index.ts
├── api/
│   ├── client.ts
│   ├── endpoints/
│   │   ├── users.ts
│   │   └── orders.ts
│   └── index.ts
└── state/
    ├── store.ts
    ├── slices/
    │   ├── userSlice.ts
    │   └── cartSlice.ts
    └── index.ts
```

### Service Pattern

```typescript
// AuthService.ts
export class AuthService {
  constructor(
    private userRepository: UserRepository,
    private tokenService: TokenService
  ) {}

  async login(email: string, password: string): Promise<AuthResult> {
    const user = await this.userRepository.findByEmail(email);
    if (!user || !user.verifyPassword(password)) {
      throw new InvalidCredentialsError();
    }
    const token = this.tokenService.generate(user);
    return { user, token };
  }
}
```

---

## Tier 3: Data (`03-data/`)

**Purpose:** Data persistence and external data sources.

**Contains:**
- Repositories (data access)
- Database models/schemas
- Migrations
- External service adapters

**Does NOT contain:**
- Business logic
- UI components
- Validation rules (those belong in domain)

### Structure

```
03-data/
├── repositories/
│   ├── UserRepository.ts
│   ├── UserRepository.test.ts
│   ├── OrderRepository.ts
│   ├── OrderRepository.test.ts
│   └── index.ts
├── models/
│   ├── UserModel.ts
│   ├── OrderModel.ts
│   └── index.ts
├── migrations/
│   ├── 001_create_users.ts
│   ├── 002_create_orders.ts
│   └── index.ts
├── seeds/
│   ├── users.ts
│   └── products.ts
└── adapters/
    ├── StripeAdapter.ts
    └── SendGridAdapter.ts
```

### Repository Pattern

```typescript
// UserRepository.ts
export class UserRepository {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User | null> {
    const row = await this.db.query('SELECT * FROM users WHERE id = ?', [id]);
    return row ? this.toEntity(row) : null;
  }

  async save(user: User): Promise<void> {
    await this.db.query(
      'INSERT INTO users (id, email, name) VALUES (?, ?, ?)',
      [user.id, user.email, user.name]
    );
  }

  private toEntity(row: UserRow): User {
    return new User(row.id, row.email, row.name);
  }
}
```

---

## Config (`config/`)

**Purpose:** Cross-cutting configuration that doesn't fit in a single tier.

```
config/
├── database.ts
├── auth.ts
├── api.ts
├── feature-flags.ts
└── index.ts
```

---

## Dependency Rules

### Valid Imports

```
01-presentation → 02-logic ✅
02-logic → 03-data ✅
01-presentation → 03-data ❌ (skip layer)
03-data → 02-logic ❌ (reverse)
02-logic → 01-presentation ❌ (reverse)
```

### Enforcement

```typescript
// eslint config or custom validator
{
  "rules": {
    "import/no-restricted-paths": [
      "error",
      {
        "zones": [
          {
            "target": "./03-data",
            "from": "./02-logic"
          },
          {
            "target": "./03-data",
            "from": "./01-presentation"
          },
          {
            "target": "./02-logic",
            "from": "./01-presentation"
          }
        ]
      }
    ]
  }
}
```

---

## Shared Code

### Within a Tier

Create a `shared/` folder within the tier:

```
02-logic/
├── services/
├── shared/
│   ├── errors.ts
│   └── utils.ts
└── ...
```

### Across Tiers

Use the `config/` folder or create a `shared/` at project root:

```
project/
├── shared/
│   ├── types/
│   │   └── common.ts
│   └── constants/
│       └── errors.ts
├── 01-presentation/
├── 02-logic/
└── 03-data/
```

**Warning:** Shared folders can become dumping grounds. Be strict about what goes there.

---

## Index Files (Barrel Exports)

Each major folder should have an `index.ts` that exports its public API:

```typescript
// 02-logic/services/index.ts
export { AuthService } from './AuthService';
export { PaymentService } from './PaymentService';
export { UserService } from './UserService';
```

**Benefits:**
- Clean imports: `import { AuthService } from '@/logic/services'`
- Encapsulation: Only exported items are public
- Refactoring: Change internals without breaking imports
