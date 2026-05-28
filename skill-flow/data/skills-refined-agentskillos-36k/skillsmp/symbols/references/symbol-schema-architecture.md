# Symbol Schema & Architecture

Complete specification of symbol structure, layer taxonomy, domain organization, and relationship detection rules.

## Overview

The symbol system uses a standardized schema to represent all code elements (components, functions, classes, etc.) with consistent metadata enabling efficient querying and filtering.

**Key Features:**
- Standardized symbol structure across languages
- Architectural layer tags for precise filtering
- Domain-based organization
- Relationship detection between symbols
- Test file separation

---

## Symbol Structure Specification

### Core Symbol Schema

Every symbol includes these fields:

```typescript
interface Symbol {
  // Required fields
  name: string;           // Symbol name (exact)
  kind: SymbolKind;       // Symbol type
  file: string;           // Absolute or relative path
  line: number;           // Line number in file
  domain: string;         // Domain classification
  layer: LayerTag;        // Architectural layer tag
  summary: string;        // Brief description

  // Optional fields
  signature?: string;     // Function/method signature
  parent?: string;        // Parent class/module
  docstring?: string;     // Full documentation
  category?: string;      // Additional categorization
  priority?: Priority;    // Symbol priority
  exports?: string[];     // Exported symbols (modules)
  imports?: Import[];     // Import statements
  relationships?: Relationship[]; // Related symbols
}
```

### Field Definitions

#### Required Fields

**name** (string)
- Exact symbol name as defined in code
- Case-sensitive
- Examples: `Button`, `UserService`, `useAuth`

**kind** (SymbolKind)
- Symbol type classification
- See [Symbol Kinds](#symbol-kinds) section

**file** (string)
- File path where symbol is defined
- Relative to project root
- Examples: `packages/ui/src/components/Button.tsx`, `services/api/app/services/user_service.py`

**line** (number)
- Line number where symbol is defined
- 1-indexed
- Enables precise code location

**domain** (string)
- Domain classification from `symbols.config.json`
- Examples: `ui`, `web`, `api`, `shared`, `mobile`
- Configured per project

**layer** (LayerTag)
- Architectural layer tag
- Assigned based on file path patterns
- See [Layer Tag Taxonomy](#layer-tag-taxonomy) section

**summary** (string)
- Brief one-sentence description
- Extracted from comments/docstrings or generated
- Max length: ~200 characters

#### Optional Fields

**signature** (string)
- Function/method signature
- Includes parameters and return type
- Examples:
  - `Button(props: ButtonProps): JSX.Element`
  - `def create_user(user_data: UserCreate) -> User:`

**parent** (string)
- Parent class or module name
- Used for methods, nested classes
- Examples: `UserService` (for methods), `Button` (for sub-components)

**docstring** (string)
- Complete documentation comment
- JSDoc, docstrings, or inline comments
- Preserved as-is from source code

**category** (string)
- Additional categorization beyond kind/layer
- Examples: `auth`, `data-fetching`, `ui-primitive`
- Project-specific

**priority** (Priority)
- Symbol importance ranking
- Values: `high`, `medium`, `low`
- Used for filtering and ordering

**exports** (string[])
- Array of exported symbol names (for modules)
- Examples: `["Button", "ButtonProps"]`

**imports** (Import[])
- Import statements
- Structure: `{ source: string, symbols: string[] }`
- Used for dependency analysis

**relationships** (Relationship[])
- Related symbols (props interfaces, used functions, etc.)
- Structure: `{ type: string, target: string }`
- See [Relationship Detection](#relationship-detection) section

---

## Symbol Kinds

### TypeScript/JavaScript Kinds

**component**
- React components (function or class)
- Examples: `Button`, `Card`, `UserProfile`
- Detected by: JSX return, React import, naming convention

**hook**
- React hooks (built-in or custom)
- Examples: `useUser`, `useAuth`, `useState`
- Detected by: `use` prefix, React Hooks API

**function**
- Regular functions and arrow functions
- Examples: `formatDate`, `validateEmail`, `fetchData`
- Excludes components and hooks

**class**
- Class declarations
- Examples: `ApiClient`, `EventEmitter`
- Excludes React components

**method**
- Class methods
- Parent field contains class name
- Examples: `getUserById`, `render`, `handleClick`

**interface**
- TypeScript interfaces
- Examples: `ButtonProps`, `User`, `ApiResponse`
- Used for type definitions

**type**
- TypeScript type aliases
- Examples: `UserId`, `ButtonVariant`, `ApiError`
- Includes union types, mapped types

### Python Kinds

**module**
- Python modules (files)
- Examples: `user_service`, `auth_middleware`
- Top-level organizational unit

**class**
- Python class definitions
- Examples: `UserService`, `UserRepository`, `HTTPException`
- Includes dataclasses, enums

**function**
- Module-level functions
- Examples: `create_user`, `validate_token`, `get_db`
- Includes async functions, decorators

**method**
- Class methods and instance methods
- Parent field contains class name
- Examples: `get_by_id`, `create`, `update`
- Includes static methods, class methods

---

## Layer Tag Taxonomy

Layer tags enable architectural filtering and validation. All symbols are assigned exactly one layer tag based on file path patterns.

### Backend Layers

**router** / **controller**
- HTTP endpoints and route handlers
- Request validation and routing logic
- Response formatting

**Patterns:**
```
app/api/*
app/routers/*
*/routers/*
*/controllers/*
app/endpoints/*
```

**Examples:**
```python
# File: services/api/app/routers/user_router.py
# Layer: router

@router.get("/users/{user_id}")
async def get_user(user_id: str) -> UserResponse:
    pass
```

---

**service**
- Business logic layer
- DTO mapping and orchestration
- Inter-layer coordination

**Patterns:**
```
app/services/*
*/services/*
app/business/*
```

**Examples:**
```python
# File: services/api/app/services/user_service.py
# Layer: service

class UserService:
    def create_user(self, user_data: UserCreate) -> User:
        # Business logic
        pass
```

---

**repository**
- Data access layer
- Database operations
- Query logic

**Patterns:**
```
app/repositories/*
*/repositories/*
app/data/*
*/dal/*
```

**Examples:**
```python
# File: services/api/app/repositories/user_repository.py
# Layer: repository

class UserRepository:
    def find_by_id(self, user_id: str) -> Optional[User]:
        # Database query
        pass
```

---

**schema** / **dto**
- Request/response data structures
- Validation schemas
- Data transfer objects

**Patterns:**
```
app/schemas/*
app/dtos/*
*/schemas/*
*/dtos/*
app/models/schemas/*
```

**Examples:**
```python
# File: services/api/app/schemas/user_schema.py
# Layer: schema

class UserCreate(BaseModel):
    email: str
    name: str
```

---

**core** / **model**
- Domain models
- Core utilities
- Database entities (ORM models)

**Patterns:**
```
app/core/*
app/models/*
*/core/*
*/models/*
app/domain/*
```

**Examples:**
```python
# File: services/api/app/models/user.py
# Layer: core

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
```

---

**middleware**
- Middleware functions
- Request/response interceptors
- Cross-cutting concerns

**Patterns:**
```
app/middleware/*
*/middleware/*
```

**Examples:**
```python
# File: services/api/app/middleware/auth_middleware.py
# Layer: middleware

async def auth_middleware(request: Request, call_next):
    # Authentication logic
    pass
```

---

**auth**
- Authentication and authorization
- Token management
- Permission checking

**Patterns:**
```
app/auth/*
*/auth/*
app/security/*
```

**Examples:**
```python
# File: services/api/app/auth/jwt_handler.py
# Layer: auth

def create_access_token(user_id: str) -> str:
    # JWT token creation
    pass
```

---

### Frontend Layers

**component**
- UI components
- Design system primitives
- Reusable UI elements

**Patterns:**
```
components/*
*/components/*
src/ui/*
*/ui/*
```

**Examples:**
```typescript
// File: packages/ui/src/components/Button.tsx
// Layer: component

export function Button(props: ButtonProps) {
  return <button {...props} />;
}
```

---

**hook**
- React hooks
- Custom state management
- Data fetching hooks

**Patterns:**
```
hooks/*
*/hooks/*
src/hooks/*
```

**Examples:**
```typescript
// File: apps/web/src/hooks/useUser.ts
// Layer: hook

export function useUser(userId: string) {
  return useQuery(['user', userId], () => fetchUser(userId));
}
```

---

**page**
- Application pages and routes
- Page-level components
- Route handlers

**Patterns:**
```
pages/*
app/*
*/pages/*
routes/*
views/*
screens/*
```

**Examples:**
```typescript
// File: apps/web/src/app/profile/page.tsx
// Layer: page

export default function ProfilePage() {
  return <div>Profile</div>;
}
```

---

**util**
- Shared utilities and helpers
- Pure functions
- Common libraries

**Patterns:**
```
utils/*
lib/*
*/utils/*
*/lib/*
helpers/*
```

**Examples:**
```typescript
// File: packages/shared/src/utils/formatDate.ts
// Layer: util

export function formatDate(date: Date): string {
  return date.toISOString();
}
```

---

**context**
- React context providers
- Global state management
- Context consumers

**Patterns:**
```
contexts/*
*/contexts/*
providers/*
store/*
```

**Examples:**
```typescript
// File: apps/web/src/contexts/UserContext.tsx
// Layer: context

export const UserContext = createContext<UserContextType>(null);
```

---

### Test Layer

**test**
- Test files and utilities
- Test fixtures
- Test helpers

**Patterns:**
```
**/*.test.*
**/*.spec.*
**/tests/*
**/__tests__/*
**/test/*
test_*.py
```

**Examples:**
```typescript
// File: packages/ui/src/components/Button.test.tsx
// Layer: test

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
  });
});
```

---

## Domain Organization

Domains group related code into logical units configured in `symbols.config.json`.

### Common Domain Patterns

**ui** - Design system and UI primitives
- Reusable components
- Design tokens
- UI utilities

**web** - Web application code
- Pages and routes
- App-specific hooks
- Web-specific features

**mobile** - Mobile application code
- Screens
- Native modules
- Mobile-specific hooks

**api** - Backend API code
- All backend layers (routers, services, repositories, etc.)
- Often split by layer for efficiency

**shared** - Shared code across domains
- Common types and interfaces
- Utilities used everywhere
- Cross-domain constants

### Domain Configuration

Defined in `symbols.config.json`:

```json
{
  "domains": {
    "ui": {
      "source": "packages/ui/src",
      "output": "ai/symbols-ui.json",
      "language": "typescript"
    },
    "web": {
      "source": "apps/web/src",
      "output": "ai/symbols-web.json",
      "language": "typescript"
    },
    "api": {
      "source": "services/api/app",
      "output": "ai/symbols-api.json",
      "language": "python",
      "enableLayerSplit": true
    }
  }
}
```

---

## Relationship Detection

Symbols can have relationships to other symbols, enabling context-aware querying.

### Relationship Types

**props**
- Props interface for React components
- Detection: Interface named `{ComponentName}Props`
- Example: `Button` → `ButtonProps`

**imports**
- Symbols imported by this symbol
- Detection: Import statements in file
- Used for dependency analysis

**exports**
- Symbols exported from module
- Detection: Export statements
- Used for module API discovery

**usages**
- Where this symbol is used
- Detection: Cross-reference analysis
- Limited to same domain

**parent**
- Parent class or module
- Detection: Class hierarchy, file structure
- Used for method → class relationships

**children**
- Child classes or sub-components
- Detection: Inheritance, composition patterns
- Inverse of parent relationship

### Relationship Detection Rules

**Component → Props Interface:**

```typescript
// Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary';
  onClick: () => void;
}

export function Button(props: ButtonProps) {
  // Component implementation
}

// Symbol relationship:
// Button (component) --[props]--> ButtonProps (interface)
```

**Method → Class:**

```python
# user_service.py
class UserService:
    def create_user(self, user_data: UserCreate) -> User:
        pass

# Symbol relationship:
# create_user (method) --[parent]--> UserService (class)
```

**Import Dependencies:**

```typescript
// ProfilePage.tsx
import { Button } from '@ui/components/Button';
import { useUser } from '@web/hooks/useUser';

export function ProfilePage() {
  // Page implementation
}

// Symbol relationships:
// ProfilePage (component) --[imports]--> Button (component)
// ProfilePage (component) --[imports]--> useUser (hook)
```

### Relationship Detection Limitations

- Limited to depth of 2 (no transitive relationships by default)
- Cross-domain relationships require both domains loaded
- Test relationships excluded unless tests explicitly loaded
- Performance consideration: `include_related=True` adds 2-3x token cost

---

## Symbol File Structure

### Domain Symbol Files

Standard format for domain-specific symbol files:

```json
{
  "domain": "ui",
  "language": "typescript",
  "extractedAt": "2025-11-06T10:30:00Z",
  "version": "1.0",
  "totalSymbols": 142,
  "symbols": [
    {
      "name": "Button",
      "kind": "component",
      "file": "packages/ui/src/components/Button.tsx",
      "line": 15,
      "domain": "ui",
      "layer": "component",
      "signature": "Button(props: ButtonProps): JSX.Element",
      "summary": "Base button component with variants",
      "docstring": "/** Base button component supporting multiple variants */",
      "category": "ui-primitive"
    },
    {
      "name": "ButtonProps",
      "kind": "interface",
      "file": "packages/ui/src/components/Button.tsx",
      "line": 8,
      "domain": "ui",
      "layer": "component",
      "signature": "interface ButtonProps",
      "summary": "Props for Button component"
    }
  ]
}
```

### Layer-Chunked Files

Format for layer-specific files (after chunking):

```json
{
  "layer": "services",
  "domain": "api",
  "language": "python",
  "extractedAt": "2025-11-06T10:30:00Z",
  "version": "1.0",
  "totalSymbols": 45,
  "symbols": [
    {
      "name": "UserService",
      "kind": "class",
      "file": "services/api/app/services/user_service.py",
      "line": 12,
      "domain": "api",
      "layer": "service",
      "summary": "User management business logic",
      "parent": null,
      "docstring": "User management service handling business logic and orchestration"
    },
    {
      "name": "create_user",
      "kind": "method",
      "file": "services/api/app/services/user_service.py",
      "line": 25,
      "domain": "api",
      "layer": "service",
      "signature": "def create_user(self, user_data: UserCreate) -> User:",
      "summary": "Create new user with validation",
      "parent": "UserService"
    }
  ]
}
```

### Test Symbol Files

Test symbols separated for on-demand loading:

```json
{
  "domain": "ui",
  "layer": "test",
  "language": "typescript",
  "extractedAt": "2025-11-06T10:30:00Z",
  "version": "1.0",
  "totalSymbols": 38,
  "symbols": [
    {
      "name": "Button.test",
      "kind": "function",
      "file": "packages/ui/src/components/Button.test.tsx",
      "line": 5,
      "domain": "ui",
      "layer": "test",
      "summary": "Button component test suite"
    }
  ]
}
```

---

## Schema Validation

### Required Field Validation

Every symbol must have:
- `name` - Non-empty string
- `kind` - Valid SymbolKind value
- `file` - Valid file path
- `line` - Positive integer
- `domain` - Configured domain name
- `layer` - Valid LayerTag
- `summary` - Non-empty string (max 200 chars)

### Optional Field Validation

When present:
- `signature` - Non-empty string (max 500 chars)
- `parent` - Valid symbol name
- `docstring` - String (any length)
- `priority` - One of: `high`, `medium`, `low`
- `exports` - Array of non-empty strings
- `imports` - Array of Import objects
- `relationships` - Array of Relationship objects

### File Structure Validation

- Valid JSON format
- Root object contains required metadata
- `symbols` is an array
- `totalSymbols` matches array length

### Validation Script

```bash
# Run validation
python scripts/validate_symbols.py ai/symbols-ui.json

# Output:
# ✓ Valid JSON structure
# ✓ All required fields present
# ✓ 142 symbols validated
# ✓ No duplicates found
# ✓ All layer tags assigned
# ✓ File paths valid
# Symbol file is valid.
```

---

## Schema Evolution

### Version 1.0 (Current)

Current schema version with all features documented above.

### Future Enhancements (Proposed)

**Symbol Metadata:**
- `complexity` - Cyclomatic complexity score
- `coverage` - Test coverage percentage
- `lastModified` - Last modification timestamp
- `author` - Symbol author/contributor

**Enhanced Relationships:**
- `calls` - Functions/methods called by this symbol
- `calledBy` - Symbols that call this symbol
- `implements` - Interface implementation relationships
- `extends` - Inheritance relationships

**Performance Metrics:**
- `tokenSize` - Estimated token count
- `dependencies` - Dependency count
- `cohesion` - Cohesion score

### Migration Strategy

When schema evolves:
1. Increment version number in files
2. Maintain backward compatibility
3. Provide migration script
4. Update validation rules
5. Document changes

---

## Architecture Integration

### Layered Architecture Validation

Use layer tags to validate architectural patterns:

**Router → Service → Repository pattern:**

```python
# Check routers don't call repositories directly
routers = load_api_layer("routers")
for router in routers["symbols"]:
    # Verify router only calls services
    # Violation: router calling repository directly
```

**Component → Hook → API pattern:**

```python
# Check components use hooks for data fetching
components = search_patterns(layer="component", domain="web")
for component in components:
    # Verify data fetching through hooks
    # Violation: component calling API directly
```

### Cross-Layer Dependencies

Detect and validate cross-layer dependencies:

```python
# Find all service → repository calls
services = load_api_layer("services")
repositories = load_api_layer("repositories")

# Analyze which services use which repositories
# Validate expected dependencies
```

### Architecture Decision Records (ADRs)

Document architectural patterns using symbol layer taxonomy:

```markdown
# ADR: Backend Layered Architecture

## Layers

- **Router Layer** (`layer: router`) - HTTP endpoints only
- **Service Layer** (`layer: service`) - Business logic
- **Repository Layer** (`layer: repository`) - Data access
- **Schema Layer** (`layer: schema`) - DTOs
- **Core Layer** (`layer: core`) - Models

## Rules

1. Routers MUST only call Services
2. Services MUST only call Repositories
3. Repositories MUST only access Core Models
4. All layers MAY use Schemas
```

Use symbol queries to validate ADR compliance.

---

## Performance Considerations

### Symbol Size Impact

**Average symbol sizes:**
- Component with props: ~200 tokens
- Function with signature: ~100 tokens
- Class with methods: ~150 tokens per method
- Interface/Type: ~50 tokens

**Optimization strategies:**
- Use `summary_only=True` for quick scans (50% reduction)
- Load layer-specific files instead of full domain (80-90% reduction)
- Apply `max_symbols` limits (proportional reduction)
- Exclude test symbols unless debugging

### Querying Performance

**Query efficiency:**
- Name-based queries: O(n) scan, fast with small n
- Pattern-based queries: O(n) regex matching, slower
- Layer-filtered queries: O(n) with layer pre-filter
- Domain-filtered queries: O(1) file selection + O(n) scan

**Best practices:**
- Combine filters to reduce search space
- Use layer loading for backend work
- Cache frequently accessed symbols
- Limit result sets with `limit` parameter

---

## See Also

- **[symbol-api-reference.md](./symbol-api-reference.md)** - Complete API documentation
- **[symbol-workflows-by-role.md](./symbol-workflows-by-role.md)** - Practical workflows
- **[symbol-script-operations.md](./symbol-script-operations.md)** - Script operations and maintenance
- **[symbol-performance-metrics.md](./symbol-performance-metrics.md)** - Detailed performance benchmarks
