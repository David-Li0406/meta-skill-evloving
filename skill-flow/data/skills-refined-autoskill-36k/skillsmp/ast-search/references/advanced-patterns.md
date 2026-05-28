# Advanced ast-grep Patterns

## React Patterns

### Hooks

```bash
# Find all hook usages
ast-grep -p 'use$HOOK($$$)' -l tsx

# useState with destructuring
ast-grep -p 'const [$STATE, $SETTER] = useState($$$)' -l tsx

# useEffect with cleanup
ast-grep -p 'useEffect(() => { $$$ return $$$; }, [$$$])' -l tsx

# useMemo with dependencies
ast-grep -p 'useMemo(() => $$$, [$$$])' -l tsx

# useCallback
ast-grep -p 'useCallback($$$)' -l tsx

# Custom hook definitions
ast-grep -p 'function use$NAME($$$) { $$$ }' -l tsx
```

### Components

```bash
# Functional components
ast-grep -p 'function $Component($PROPS): JSX.Element { $$$ }' -l tsx
ast-grep -p 'const $Component = ($$$) => { $$$ }' -l tsx
ast-grep -p 'const $Component: React.FC<$$$> = ($$$) => { $$$ }' -l tsx

# forwardRef components
ast-grep -p 'forwardRef<$$$>(($PROPS, $REF) => { $$$ })' -l tsx

# memo wrapped components
ast-grep -p 'memo($COMPONENT)' -l tsx
ast-grep -p 'React.memo($COMPONENT)' -l tsx

# Component with specific prop
ast-grep -p '<$Component $PROP={$$$} $$$>' -l tsx
```

### Event Handlers

```bash
# onClick handlers
ast-grep -p 'onClick={$$$}' -l tsx

# onChange handlers
ast-grep -p 'onChange={$$$}' -l tsx

# onSubmit handlers
ast-grep -p 'onSubmit={$$$}' -l tsx

# Event handler definitions
ast-grep -p 'const handle$EVENT = ($$$) => { $$$ }' -l tsx
```

## Next.js Patterns

```bash
# Server components (app router)
ast-grep -p 'export default async function $PAGE($$$) { $$$ }' -l tsx

# Client components
ast-grep -p "'use client'" -l tsx

# Server actions
ast-grep -p "'use server'" -l tsx

# API routes (pages router)
ast-grep -p 'export default function handler($REQ, $RES) { $$$ }' -l typescript

# getServerSideProps
ast-grep -p 'export async function getServerSideProps($$$) { $$$ }' -l typescript

# getStaticProps
ast-grep -p 'export async function getStaticProps($$$) { $$$ }' -l typescript

# Dynamic imports
ast-grep -p "dynamic(() => import('$$$'))" -l tsx

# Image component usage
ast-grep -p '<Image src={$$$} $$$>' -l tsx

# Link component usage
ast-grep -p '<Link href={$$$} $$$>' -l tsx
```

## Express/Node.js Patterns

```bash
# Route handlers
ast-grep -p 'app.get($PATH, $$$)' -l javascript
ast-grep -p 'app.post($PATH, $$$)' -l javascript
ast-grep -p 'router.get($PATH, $$$)' -l javascript
ast-grep -p 'router.post($PATH, $$$)' -l javascript

# Middleware
ast-grep -p 'app.use($$$)' -l javascript

# Async route handlers
ast-grep -p 'async ($REQ, $RES, $NEXT) => { $$$ }' -l javascript

# Error handling middleware
ast-grep -p '($ERR, $REQ, $RES, $NEXT) => { $$$ }' -l javascript
```

## Testing Patterns

### Jest/Vitest

```bash
# Test blocks
ast-grep -p "describe('$$$', () => { $$$ })" -l typescript
ast-grep -p "it('$$$', () => { $$$ })" -l typescript
ast-grep -p "test('$$$', () => { $$$ })" -l typescript

# Async tests
ast-grep -p "it('$$$', async () => { $$$ })" -l typescript

# beforeEach/afterEach
ast-grep -p 'beforeEach(() => { $$$ })' -l typescript
ast-grep -p 'afterEach(() => { $$$ })' -l typescript

# Mock functions
ast-grep -p 'jest.fn($$$)' -l typescript
ast-grep -p 'vi.fn($$$)' -l typescript

# Spy on methods
ast-grep -p 'jest.spyOn($OBJ, $METHOD)' -l typescript
ast-grep -p 'vi.spyOn($OBJ, $METHOD)' -l typescript

# Assertions
ast-grep -p 'expect($$$).toBe($$$)' -l typescript
ast-grep -p 'expect($$$).toEqual($$$)' -l typescript
ast-grep -p 'expect($$$).toHaveBeenCalled($$$)' -l typescript
```

### React Testing Library

```bash
# Queries
ast-grep -p 'screen.getByRole($$$)' -l tsx
ast-grep -p 'screen.getByText($$$)' -l tsx
ast-grep -p 'screen.findBy$QUERY($$$)' -l tsx

# User events
ast-grep -p 'userEvent.click($$$)' -l tsx
ast-grep -p 'userEvent.type($$$)' -l tsx

# Render
ast-grep -p 'render(<$COMPONENT $$$/>)' -l tsx
```

## Python Framework Patterns

### FastAPI

```bash
# Route decorators
ast-grep -p '@app.get($$$)
async def $FUNC($$$): $$$' -l python

ast-grep -p '@app.post($$$)
async def $FUNC($$$): $$$' -l python

# Dependency injection
ast-grep -p 'Depends($$$)' -l python

# Pydantic models
ast-grep -p 'class $MODEL(BaseModel): $$$' -l python

# Background tasks
ast-grep -p 'BackgroundTasks' -l python
```

### Django

```bash
# View functions
ast-grep -p 'def $VIEW(request$$$): $$$' -l python

# Class-based views
ast-grep -p 'class $VIEW(View): $$$' -l python
ast-grep -p 'class $VIEW(APIView): $$$' -l python

# Model definitions
ast-grep -p 'class $MODEL(models.Model): $$$' -l python

# URL patterns
ast-grep -p "path('$$$', $VIEW)" -l python

# Admin registration
ast-grep -p '@admin.register($MODEL)' -l python
```

### SQLAlchemy

```bash
# Model definitions
ast-grep -p 'class $MODEL(Base): $$$' -l python

# Column definitions
ast-grep -p 'Column($$$)' -l python

# Relationships
ast-grep -p 'relationship($$$)' -l python

# Query operations
ast-grep -p 'session.query($$$)' -l python
ast-grep -p 'session.add($$$)' -l python
ast-grep -p 'session.commit()' -l python
```

## Go Framework Patterns

### Gin

```bash
# Route handlers
ast-grep -p 'r.GET($PATH, $$$)' -l go
ast-grep -p 'r.POST($PATH, $$$)' -l go

# Handler functions
ast-grep -p 'func $NAME(c *gin.Context) { $$$ }' -l go

# Response methods
ast-grep -p 'c.JSON($$$)' -l go
ast-grep -p 'c.String($$$)' -l go

# Middleware
ast-grep -p 'r.Use($$$)' -l go
```

### Standard Library HTTP

```bash
# Handler functions
ast-grep -p 'func $NAME(w http.ResponseWriter, r *http.Request) { $$$ }' -l go

# Route registration
ast-grep -p 'http.HandleFunc($$$)' -l go
ast-grep -p 'http.Handle($$$)' -l go

# Server creation
ast-grep -p 'http.ListenAndServe($$$)' -l go
```

## TypeScript/JavaScript General

### Class Patterns

```bash
# Class with constructor
ast-grep -p 'class $CLASS { constructor($$$) { $$$ } $$$ }' -l typescript

# Private fields
ast-grep -p '#$FIELD' -l typescript

# Getter/Setter
ast-grep -p 'get $NAME() { $$$ }' -l typescript
ast-grep -p 'set $NAME($$$) { $$$ }' -l typescript

# Static methods
ast-grep -p 'static $METHOD($$$) { $$$ }' -l typescript

# Decorators
ast-grep -p '@$DECORATOR($$$)
$$$' -l typescript
```

### Module Patterns

```bash
# Named exports
ast-grep -p 'export { $$$ }' -l typescript
ast-grep -p 'export const $NAME = $$$' -l typescript
ast-grep -p 'export function $NAME($$$) { $$$ }' -l typescript

# Default exports
ast-grep -p 'export default $$$' -l typescript

# Named imports
ast-grep -p "import { $$$ } from '$MODULE'" -l typescript

# Default imports
ast-grep -p "import $NAME from '$MODULE'" -l typescript

# Dynamic imports
ast-grep -p "import('$$$')" -l typescript
ast-grep -p 'await import($$$)' -l typescript
```

### Async Patterns

```bash
# Async/await
ast-grep -p 'async function $NAME($$$) { $$$ }' -l typescript
ast-grep -p 'async ($$$) => { $$$ }' -l typescript
ast-grep -p 'await $EXPR' -l typescript

# Promise patterns
ast-grep -p 'new Promise(($RESOLVE, $REJECT) => { $$$ })' -l typescript
ast-grep -p '$PROMISE.then($$$)' -l typescript
ast-grep -p '$PROMISE.catch($$$)' -l typescript
ast-grep -p 'Promise.all($$$)' -l typescript
ast-grep -p 'Promise.allSettled($$$)' -l typescript

# Try/catch with async
ast-grep -p 'try { $$$ await $$$ } catch ($E) { $$$ }' -l typescript
```

### Error Handling

```bash
# Try/catch blocks
ast-grep -p 'try { $$$ } catch ($ERR) { $$$ }' -l typescript

# Throwing errors
ast-grep -p 'throw new Error($$$)' -l typescript
ast-grep -p 'throw new $ErrorType($$$)' -l typescript

# Error class definitions
ast-grep -p 'class $Error extends Error { $$$ }' -l typescript
```

## Database Query Patterns

### Prisma

```bash
# Find operations
ast-grep -p 'prisma.$MODEL.findMany($$$)' -l typescript
ast-grep -p 'prisma.$MODEL.findUnique($$$)' -l typescript
ast-grep -p 'prisma.$MODEL.findFirst($$$)' -l typescript

# Create operations
ast-grep -p 'prisma.$MODEL.create($$$)' -l typescript
ast-grep -p 'prisma.$MODEL.createMany($$$)' -l typescript

# Update operations
ast-grep -p 'prisma.$MODEL.update($$$)' -l typescript
ast-grep -p 'prisma.$MODEL.updateMany($$$)' -l typescript

# Delete operations
ast-grep -p 'prisma.$MODEL.delete($$$)' -l typescript
ast-grep -p 'prisma.$MODEL.deleteMany($$$)' -l typescript

# Transactions
ast-grep -p 'prisma.$transaction($$$)' -l typescript
```

### Drizzle

```bash
# Select queries
ast-grep -p 'db.select($$$).from($TABLE)' -l typescript

# Insert queries
ast-grep -p 'db.insert($TABLE).values($$$)' -l typescript

# Update queries
ast-grep -p 'db.update($TABLE).set($$$)' -l typescript

# Delete queries
ast-grep -p 'db.delete($TABLE)' -l typescript
```

## Security-Related Patterns

```bash
# Potential SQL injection (string concatenation in queries)
ast-grep -p '"SELECT $$$" + $VAR' -l javascript
ast-grep -p 'f"SELECT {$$$}"' -l python

# Eval usage (potential code injection)
ast-grep -p 'eval($$$)' -l javascript
ast-grep -p 'exec($$$)' -l python

# Dangerous innerHTML
ast-grep -p '$$$innerHTML = $$$' -l javascript
ast-grep -p 'dangerouslySetInnerHTML={$$$}' -l tsx

# Hardcoded secrets (look for assignment patterns)
ast-grep -p 'const $SECRET = "$$$"' -l typescript
ast-grep -p '$KEY = "$$$"' -l python

# Insecure random
ast-grep -p 'Math.random()' -l javascript

# Console statements (for cleanup)
ast-grep -p 'console.log($$$)' -l typescript
ast-grep -p 'console.error($$$)' -l typescript
ast-grep -p 'print($$$)' -l python
```

## Performance Patterns

```bash
# Unoptimized loops with await
ast-grep -p 'for ($$$) { $$$ await $$$ }' -l typescript

# Missing useMemo/useCallback
ast-grep -p 'const $VAR = $EXPENSIVE($$$)' -l tsx

# Inline object/array in deps
ast-grep -p 'useEffect($$$, [{ $$$ }])' -l tsx
ast-grep -p 'useEffect($$$, [[ $$$ ]])' -l tsx

# Direct state mutation patterns
ast-grep -p '$STATE.push($$$)' -l typescript
ast-grep -p '$STATE[$KEY] = $$$' -l typescript
```
