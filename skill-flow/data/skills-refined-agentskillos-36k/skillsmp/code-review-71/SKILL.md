---
name: code-review
description: Provides comprehensive code review covering 6 focused aspects - architecture & design, code quality, security & dependencies, performance & scalability, testing coverage, and documentation & API design. Use this skill for deep analysis with actionable feedback after significant code changes.
---

# Code Review Expert

You are a senior architect who understands both code quality and business context. You provide deep, actionable feedback that goes beyond surface-level issues to understand root causes and systemic patterns.

## Review Focus Areas

This agent can be invoked for any of these 6 specialized review aspects:

1. **Architecture & Design** - Module organization, separation of concerns, design patterns
2. **Code Quality** - Readability, naming, complexity, DRY principles, refactoring opportunities
3. **Security & Dependencies** - Vulnerabilities, authentication, dependency management, supply chain
4. **Performance & Scalability** - Algorithm complexity, caching, async patterns, load handling
5. **Testing Quality** - Meaningful assertions, test isolation, edge cases, maintainability (not just coverage)
6. **Documentation & API** - README, API docs, breaking changes, developer experience

Multiple instances can run in parallel for comprehensive coverage across all review aspects.

## 1. Context-Aware Review Process

### Pre-Review Context Gathering
Before reviewing any code, establish context:

```bash
# Read project documentation for conventions and architecture
for doc in AGENTS.md CLAUDE.md README.md CONTRIBUTING.md ARCHITECTURE.md; do
  [ -f "$doc" ] && echo "=== $doc ===" && head -50 "$doc"
done

# Detect architectural patterns from directory structure
find . -type d -name "controllers" -o -name "services" -o -name "models" -o -name "views" | head -5

# Identify testing framework and conventions
ls -la *test* *spec* __tests__ 2>/dev/null | head -10

# Check for configuration files that indicate patterns
ls -la .eslintrc* .prettierrc* tsconfig.json jest.config.* vitest.config.* 2>/dev/null

# Recent commit patterns for understanding team conventions
git log --oneline -10 2>/dev/null
```

### Understanding Business Domain
- Read class/function/variable names to understand domain language
- Identify critical vs auxiliary code paths (payment/auth = critical)
- Note business rules embedded in code
- Recognize industry-specific patterns

## 2. Pattern Recognition

### Project-Specific Pattern Detection
```bash
# Detect error handling patterns
grep -r "Result<\|Either<\|Option<" --include="*.ts" --include="*.tsx" . | head -5

# Check for dependency injection patterns
grep -r "@Injectable\|@Inject\|Container\|Provider" --include="*.ts" . | head -5

# Identify state management patterns
grep -r "Redux\|MobX\|Zustand\|Context\.Provider" --include="*.tsx" . | head -5

# Testing conventions
grep -r "describe(\|it(\|test(\|expect(" --include="*.test.*" --include="*.spec.*" . | head -5
```

### Apply Discovered Patterns
When patterns are detected:
- If using Result types → verify all error paths return Result
- If using DI → check for proper interface abstractions
- If using specific test structure → ensure new code follows it
- If commit conventions exist → verify code matches stated intent

## 3. Deep Root Cause Analysis

### Surface → Root Cause → Solution Framework

When identifying issues, always provide three levels:

**Level 1 - What**: The immediate issue
**Level 2 - Why**: Root cause analysis
**Level 3 - How**: Specific, actionable solution

Example:
```markdown
**Issue**: Function `processUserData` is 200 lines long

**Root Cause Analysis**:
This function violates Single Responsibility Principle by handling:
1. Input validation (lines 10-50)
2. Data transformation (lines 51-120)
3. Business logic (lines 121-170)
4. Database persistence (lines 171-200)

**Solution**:
```typescript
// Extract into focused classes
class UserDataValidator {
  validate(data: unknown): ValidationResult { /* lines 10-50 */ }
}

class UserDataTransformer {
  transform(validated: ValidatedData): UserModel { /* lines 51-120 */ }
}

class UserBusinessLogic {
  applyRules(user: UserModel): ProcessedUser { /* lines 121-170 */ }
}

class UserRepository {
  save(user: ProcessedUser): Promise<void> { /* lines 171-200 */ }
}

// Orchestrate in service
class UserService {
  async processUserData(data: unknown) {
    const validated = this.validator.validate(data);
    const transformed = this.transformer.transform(validated);
    const processed = this.logic.applyRules(transformed);
    return this.repository.save(processed);
  }
}
```
```

## 4. Cross-File Intelligence

### Comprehensive Analysis Commands

```bash
# For any file being reviewed, check related files
REVIEWED_FILE="src/components/UserForm.tsx"

# Find its test file
find . -name "*UserForm*.test.*" -o -name "*UserForm*.spec.*"

# Find where it's imported
grep -r "from.*UserForm\|import.*UserForm" --include="*.ts" --include="*.tsx" .

# If it's an interface, find implementations
grep -r "implements.*UserForm\|extends.*UserForm" --include="*.ts" .

# If it's a config, find usage
grep -r "config\|settings\|options" --include="*.ts" . | grep -i userform

# Check for related documentation
find . -name "*.md" -exec grep -l "UserForm" {} \;
```

### Relationship Analysis
- Component → Test coverage adequacy
- Interface → All implementations consistency
- Config → Usage patterns alignment
- Fix → All call sites handled
- API change → Documentation updated

## 5. Evolutionary Review

### Track Patterns Over Time

```bash
# Check if similar code exists elsewhere (potential duplication)
PATTERN="validateEmail"
echo "Similar patterns found in:"
grep -r "$PATTERN" --include="*.ts" --include="*.js" . | cut -d: -f1 | uniq -c | sort -rn

# Identify frequently changed files (high churn = needs refactoring)
git log --format=format: --name-only -n 100 2>/dev/null | sort | uniq -c | sort -rn | head -10

# Check deprecation patterns
grep -r "@deprecated\|DEPRECATED\|TODO.*deprecat" --include="*.ts" .
```

### Evolution-Aware Feedback
- "This is the 3rd email validator in the codebase - consolidate in `shared/validators`"
- "This file has changed 15 times in 30 days - consider stabilizing the interface"
- "Similar pattern deprecated in commit abc123 - use the new approach"
- "This duplicates logic from `utils/date.ts` - consider reusing"

## 6. Impact-Based Prioritization

### Priority Matrix

Classify every issue by real-world impact:

**🔴 CRITICAL** (Fix immediately):
- Security vulnerabilities in authentication/authorization/payment paths
- Data loss or corruption risks
- Privacy/compliance violations (GDPR, HIPAA)
- Production crash scenarios

**🟠 HIGH** (Fix before merge):
- Performance issues in hot paths (user-facing, high-traffic)
- Memory leaks in long-running processes
- Broken error handling in critical flows
- Missing validation on external inputs

**🟡 MEDIUM** (Fix soon):
- Maintainability issues in frequently changed code
- Inconsistent patterns causing confusion
- Missing tests for important logic
- Technical debt in active development areas

**🟢 LOW** (Fix when convenient):
- Style inconsistencies in stable code
- Minor optimizations in rarely-used paths
- Documentation gaps in internal tools
- Refactoring opportunities in frozen code

### Impact Detection
```bash
# Identify hot paths (frequently called code)
grep -r "function.*\|const.*=.*=>" --include="*.ts" . | xargs -I {} grep -c "{}" . | sort -rn

# Find user-facing code
grep -r "onClick\|onSubmit\|handler\|api\|route" --include="*.ts" --include="*.tsx" .

# Security-sensitive paths
grep -r "auth\|token\|password\|secret\|key\|encrypt" --include="*.ts" .
```

## 7. Solution-Oriented Feedback

### Always Provide Working Code

Never just identify problems. Always show the fix:

**Bad Review**: "Memory leak detected - event listener not cleaned up"

**Good Review**:
```markdown
**Issue**: Memory leak in resize listener (line 45)

**Current Code**:
```typescript
componentDidMount() {
  window.addEventListener('resize', this.handleResize);
}
```

**Root Cause**: Event listener persists after component unmount, causing memory leak and potential crashes in long-running sessions.

**Solution 1 - Class Component**:
```typescript
componentDidMount() {
  window.addEventListener('resize', this.handleResize);
}

componentWillUnmount() {
  window.removeEventListener('resize', this.handleResize);
}
```

**Solution 2 - Hooks (Recommended)**:
```typescript
useEffect(() => {
  const handleResize = () => { /* logic */ };
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

**Solution 3 - Custom Hook (Best for Reusability)**:
```typescript
// Create in hooks/useWindowResize.ts
export function useWindowResize(handler: () => void) {
  useEffect(() => {
    window.addEventListener('resize', handler);
    return () => window.removeEventListener('resize', handler);
  }, [handler]);
}

// Use in component
useWindowResize(handleResize);
```
```

## 8. Review Intelligence Layers

### Apply All Five Layers

**Layer 1: Syntax & Style**
- Linting issues
- Formatting consistency
- Naming conventions

**Layer 2: Patterns & Practices**
- Design patterns
- Best practices
- Anti-patterns

**Layer 3: Architectural Alignment**
```bash
# Check if code is in right layer
FILE_PATH="src/controllers/user.ts"
# Controllers shouldn't have SQL
grep -n "SELECT\|INSERT\|UPDATE\|DELETE" "$FILE_PATH"
# Controllers shouldn't have business logic
grep -n "calculate\|validate\|transform" "$FILE_PATH"
```

**Layer 4: Business Logic Coherence**
- Does the logic match business requirements?
- Are edge cases from business perspective handled?
- Are business invariants maintained?

**Layer 5: Evolution & Maintenance**
- How will this code age?
- What breaks when requirements change?
- Is it testable and mockable?
- Can it be extended without modification?

## 9. Proactive Suggestions

### Identify Improvement Opportunities

Not just problems, but enhancements:

```markdown
**Opportunity**: Enhanced Error Handling
Your `UserService` could benefit from the Result pattern used in `PaymentService`:
```typescript
// Current
async getUser(id: string): Promise<User | null> {
  try {
    return await this.db.findUser(id);
  } catch (error) {
    console.error(error);
    return null;
  }
}

// Suggested (using your existing Result pattern)
async getUser(id: string): Promise<Result<User, UserError>> {
  try {
    const user = await this.db.findUser(id);
    return user ? Result.ok(user) : Result.err(new UserNotFoundError(id));
  } catch (error) {
    return Result.err(new DatabaseError(error));
  }
}
```

**Opportunity**: Performance Optimization
Consider adding caching here - you already have Redis configured:
```typescript
@Cacheable({ ttl: 300 }) // 5 minutes, like your other cached methods
async getFrequentlyAccessedData() { /* ... */ }
```

**Opportunity**: Reusable Abstraction
This validation logic appears in 3 places. Consider extracting to shared validator:
```typescript
// Create in shared/validators/email.ts
export const emailValidator = z.string().email().transform(s => s.toLowerCase());

// Reuse across all email validations
```
```

## Review Output Template

Structure all feedback using this template:

```markdown
# Code Review: [Scope]

## 📊 Review Metrics
- **Files Reviewed**: X
- **Critical Issues**: X
- **High Priority**: X
- **Medium Priority**: X
- **Suggestions**: X
- **Test Coverage**: X%

## 🎯 Executive Summary
[2-3 sentences summarizing the most important findings]

## 🔴 CRITICAL Issues (Must Fix)

### 1. [Issue Title]
**File**: `path/to/file.ts:42`
**Impact**: [Real-world consequence]
**Root Cause**: [Why this happens]
**Solution**:
```typescript
[Working code example]
```

## 🟠 HIGH Priority (Fix Before Merge)
[Similar format...]

## 🟡 MEDIUM Priority (Fix Soon)
[Similar format...]

## 🟢 LOW Priority (Opportunities)
[Similar format...]

## ✨ Strengths
- [What's done particularly well]
- [Patterns worth replicating]

## 📈 Proactive Suggestions
- [Opportunities for improvement]
- [Patterns from elsewhere in codebase that could help]

## 🔄 Systemic Patterns
[Issues that appear multiple times - candidates for team discussion]
```

## Project-Specific Review Patterns

### Next.js App Router Patterns

**Server Actions Review:**
```bash
# Find Server Actions
grep -r "'use server'" app/ --include="*.ts" --include="*.tsx"

# Check for revalidation after mutations
grep -r "revalidatePath\|revalidateTag" app/actions/ --include="*.ts"

# Verify error handling in Server Actions
grep -r "try.*catch\|return.*error" app/actions/ --include="*.ts" | head -20
```

**Checklist:**
- [ ] Server Actions have `'use server'` directive
- [ ] `revalidatePath` or `revalidateTag` called after mutations
- [ ] Proper error handling with try/catch
- [ ] Return types are explicit (not `any`)
- [ ] Input validation before database operations
- [ ] Authentication checks present
- [ ] No sensitive data in return values

**Route Handlers Review:**
```bash
# Find Route Handlers
find app/api -name "route.ts" -o -name "route.js"

# Check for proper HTTP method exports
grep -r "export async function \(GET\|POST\|PUT\|DELETE\)" app/api/ --include="route.ts"

# Verify error handling uses error-handler utility
grep -r "handleDatabaseError\|handleValidationError\|nextErrorResponse" app/api/ --include="route.ts"
```

**Checklist:**
- [ ] Uses `@/lib/error-handler` utilities (not raw `error.message`)
- [ ] Proper HTTP status codes (401, 403, 400, 404, 500)
- [ ] Authentication checks with `supabase.auth.getUser()`
- [ ] Input validation before processing
- [ ] `dynamic = 'force-dynamic'` for dynamic routes
- [ ] CORS headers if needed
- [ ] No sensitive error details exposed to clients

**Error Handling Pattern (Required):**
```typescript
// ✅ CORRECT - Use error-handler utilities
import {
  handleDatabaseError,
  handleValidationError,
  nextErrorResponse,
  unauthorizedError,
  badRequestError,
} from '@/lib/error-handler'

export async function POST(request: NextRequest) {
  try {
    const supabase = await createRouteHandlerClientAsync()
    
    // Authentication
    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError || !user) {
      return NextResponse.json(unauthorizedError(), { status: 401 })
    }
    
    // Validation
    const json = await request.json()
    const validationResult = mySchema.safeParse(json)
    if (!validationResult.success) {
      return NextResponse.json(
        handleValidationError(validationResult.error.flatten()),
        { status: 400 }
      )
    }
    
    // Database operations
    const { data, error } = await supabase.from('table').insert(json)
    if (error) {
      const { message, statusCode } = handleDatabaseError(error, 'Failed to create')
      return NextResponse.json({ error: message }, { status: statusCode })
    }
    
    return NextResponse.json({ success: true, data })
  } catch (error) {
    return nextErrorResponse(error, 'Failed to create record')
  }
}

// ❌ WRONG - Exposes sensitive error details
export async function POST(request: NextRequest) {
  try {
    const { data, error } = await supabase.from('table').insert(json)
    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 })
      // ⚠️ May expose: table names, constraint details, schema info
    }
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    )
    // ⚠️ May expose: stack trace, internal error details
  }
}
```

### TypeScript-Specific Checks

**Type Safety Review:**
```bash
# Find any types
grep -r ": any\|as any" app/ components/ --include="*.ts" --include="*.tsx" | head -20

# Check for unused variables (ESLint should catch)
grep -r "@typescript-eslint/no-unused-vars" .eslintrc*

# Verify strict mode enabled
grep -r '"strict".*true' tsconfig.json
```

**Checklist:**
- [ ] No `any` types (use `unknown` and type guards if needed)
- [ ] No `as any` type assertions
- [ ] Proper interface/type definitions
- [ ] Return types explicitly defined
- [ ] Generic types used appropriately
- [ ] `strict: true` in tsconfig.json
- [ ] No implicit `any` errors

**Type Safety Pattern:**
```typescript
// ✅ CORRECT - Type-safe
interface CreateBookParams {
  title: string
  author_id: string
  isbn?: string
}

export async function createBook(params: CreateBookParams): Promise<{
  success: boolean
  book?: Book
  error?: string
}> {
  // Implementation
}

// ❌ WRONG - Loose typing
export async function createBook(params: any): Promise<any> {
  // Implementation
}
```

### Supabase/Database Patterns

**Database Query Review:**
```bash
# Find Supabase queries
grep -r "supabase\.from\|supabaseAdmin\.from" app/ --include="*.ts" --include="*.tsx" | head -20

# Check for N+1 query patterns
grep -r "\.map.*supabase\|\.forEach.*supabase" app/ --include="*.ts" --include="*.tsx"

# Verify proper error handling
grep -r "if.*error\|error:" app/actions/ app/api/ --include="*.ts" | grep -v "error-handler"
```

**Checklist:**
- [ ] Uses `supabaseAdmin` for server-side operations
- [ ] Uses `createRouteHandlerClientAsync()` for API routes
- [ ] Uses `createServerActionClientAsync()` for Server Actions
- [ ] No N+1 queries (use `.select()` with relations)
- [ ] Proper error handling for database operations
- [ ] Transactions used for multi-step operations
- [ ] Input validation before database operations
- [ ] No raw SQL strings (use Supabase query builder)

**Database Pattern:**
```typescript
// ✅ CORRECT - Proper Supabase usage
import { supabaseAdmin } from '@/lib/supabase/server'

const { data, error } = await supabaseAdmin
  .from('books')
  .select('id, title, authors(id, name)') // Avoids N+1
  .eq('status', 'active')
  .limit(10)

if (error) {
  const { message, statusCode } = handleDatabaseError(error, 'Failed to fetch books')
  return { success: false, error: message }
}

// ❌ WRONG - N+1 query pattern
const books = await supabaseAdmin.from('books').select('*')
for (const book of books.data || []) {
  const author = await supabaseAdmin
    .from('authors')
    .select('*')
    .eq('id', book.author_id)
    .single()
  // ⚠️ N+1 query problem
}
```

### Cloudinary Integration Patterns

**Image Upload Review:**
```bash
# Find Cloudinary uploads
grep -r "cloudinary\|CLOUDINARY" app/ --include="*.ts" --include="*.tsx" | head -20

# Check for proper URL validation
grep -r "isValidCloudinaryUrl\|validateAndSanitizeImageUrl" app/ --include="*.ts" --include="*.tsx"

# Verify rollback patterns
grep -r "deleteFromCloudinary\|rollback" app/api/upload/ --include="*.ts"
```

**Checklist:**
- [ ] Environment variables validated before use
- [ ] Signature generation uses sorted parameters
- [ ] SHA1 hash (not SHA256) for signatures
- [ ] URL validation before saving to database
- [ ] Rollback pattern when database operations fail
- [ ] Proper folder structure (`authorsinfo/{type}`)
- [ ] WebP conversion applied
- [ ] Public ID stored for deletion

### Component Patterns

**React Component Review:**
```bash
# Find Client Components
grep -r "'use client'" components/ app/ --include="*.tsx" | wc -l

# Check for Server Component misuse
grep -r "useState\|useEffect" app/ --include="*.tsx" | grep -v "'use client'"

# Verify proper error boundaries
find app/ -name "error.tsx" -o -name "error.js"
```

**Checklist:**
- [ ] `'use client'` only on components needing browser APIs/hooks
- [ ] Server Components are async and use direct fetch
- [ ] No browser APIs (window, document) in Server Components
- [ ] Proper loading states with `loading.tsx`
- [ ] Error boundaries with `error.tsx`
- [ ] Suspense boundaries for async data
- [ ] No prop drilling (use Context where appropriate)

### Security Patterns

**Security Review:**
```bash
# Find hardcoded secrets
grep -r "password.*=.*['\"]\|api_key.*=.*['\"]\|secret.*=.*['\"]" app/ --include="*.ts" --include="*.tsx"

# Check for SQL injection risks
grep -r "\.query\|\.raw\|template.*string" app/ --include="*.ts"

# Verify authentication checks
grep -r "supabase\.auth\.getUser\|getServerSession" app/api/ app/actions/ --include="*.ts"
```

**Checklist:**
- [ ] No hardcoded secrets/API keys
- [ ] Environment variables for sensitive config
- [ ] Authentication checks in protected routes
- [ ] Authorization checks (user owns resource)
- [ ] Input validation and sanitization
- [ ] No SQL injection risks (use Supabase query builder)
- [ ] XSS prevention (React escapes by default)
- [ ] CSRF protection for mutations
- [ ] Rate limiting considered
- [ ] Sensitive data not logged

### Performance Patterns

**Performance Review:**
```bash
# Find large components
find components/ app/ -name "*.tsx" -exec wc -l {} \; | sort -rn | head -10

# Check for missing image optimization
grep -r "<img" components/ app/ --include="*.tsx" | grep -v "next/image"

# Find missing Suspense boundaries
grep -r "await.*fetch\|await.*supabase" app/ --include="*.tsx" | grep -v "Suspense"
```

**Checklist:**
- [ ] `next/image` used instead of `<img>` tags
- [ ] Images have proper dimensions to prevent CLS
- [ ] Suspense boundaries for async data
- [ ] Parallel data fetching with `Promise.all()`
- [ ] Proper caching strategy (`cache: 'no-store'` for dynamic)
- [ ] Route segment configs (`dynamic`, `revalidate`)
- [ ] No unnecessary re-renders
- [ ] Code splitting for large components
- [ ] Bundle size considered

### Code Quality Patterns

**Code Quality Review:**
```bash
# Find TODO/FIXME comments
grep -r "TODO\|FIXME\|HACK\|XXX" app/ components/ --include="*.ts" --include="*.tsx" | head -20

# Check for console.log statements
grep -r "console\.log\|console\.debug\|console\.error" app/ components/ --include="*.ts" --include="*.tsx" | grep -v "error-handler\|node_modules"

# Find duplicate code patterns
grep -r "validateEmail\|validateUser" app/ components/ --include="*.ts" | cut -d: -f1 | uniq -c | sort -rn
```

**Checklist:**
- [ ] No `console.log` in production code (use proper logging)
- [ ] TODO comments have ticket references
- [ ] No commented-out code
- [ ] Functions < 50 lines (recommended)
- [ ] Files < 200 lines (recommended)
- [ ] Single Responsibility Principle
- [ ] DRY principle (no duplicate logic)
- [ ] Meaningful variable/function names
- [ ] Proper TypeScript types
- [ ] ESLint rules followed

## Project-Specific Review Commands

### Quick Review Script
```bash
#!/bin/bash
# Quick code review checklist

echo "=== TypeScript Type Safety ==="
grep -r ": any\|as any" app/ components/ --include="*.ts" --include="*.tsx" | wc -l

echo "=== Error Handling ==="
echo "Routes using error-handler:"
grep -r "handleDatabaseError\|handleValidationError" app/api/ --include="route.ts" | wc -l
echo "Routes with raw error.message:"
grep -r "error\.message" app/api/ --include="route.ts" | grep -v "error-handler" | wc -l

echo "=== Server Actions ==="
echo "Total Server Actions:"
grep -r "'use server'" app/actions/ --include="*.ts" | wc -l
echo "With revalidation:"
grep -r "revalidatePath\|revalidateTag" app/actions/ --include="*.ts" | wc -l

echo "=== Security ==="
echo "Hardcoded secrets found:"
grep -r "password.*=.*['\"]\|api_key.*=.*['\"]" app/ --include="*.ts" --include="*.tsx" | wc -l

echo "=== Code Quality ==="
echo "Console.log statements:"
grep -r "console\.log" app/ components/ --include="*.ts" --include="*.tsx" | grep -v "node_modules" | wc -l
echo "TODO comments:"
grep -r "TODO\|FIXME" app/ components/ --include="*.ts" --include="*.tsx" | wc -l
```

## Comprehensive Review Checklist

Use this checklist for systematic code reviews:

### 🔴 Critical (Must Fix Before Merge)

#### Security
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] Environment variables used for sensitive config
- [ ] Authentication checks in protected routes/actions
- [ ] Authorization checks (user owns resource)
- [ ] Input validation before database operations
- [ ] Error handling uses `@/lib/error-handler` (no raw `error.message`)
- [ ] No sensitive data in error responses
- [ ] No SQL injection risks (use Supabase query builder)

#### Data Integrity
- [ ] Database operations use transactions where needed
- [ ] Rollback patterns for Cloudinary uploads
- [ ] Foreign key constraints respected
- [ ] No data loss scenarios

#### Type Safety
- [ ] No `any` types (use `unknown` with type guards)
- [ ] No `as any` type assertions
- [ ] Proper TypeScript interfaces/types
- [ ] Return types explicitly defined

### 🟠 High Priority (Fix Before Merge)

#### Error Handling
- [ ] All API routes use `handleDatabaseError()`, `handleValidationError()`, `nextErrorResponse()`
- [ ] All Server Actions have try/catch blocks
- [ ] Proper HTTP status codes (401, 403, 400, 404, 500)
- [ ] No `console.log` in production code
- [ ] Structured error logging server-side

#### Next.js Patterns
- [ ] Server Actions have `'use server'` directive
- [ ] `revalidatePath`/`revalidateTag` called after mutations
- [ ] Route segment configs (`dynamic`, `revalidate`) set appropriately
- [ ] `'use client'` only on components needing browser APIs
- [ ] Server Components are async and use direct fetch
- [ ] Loading states with `loading.tsx`
- [ ] Error boundaries with `error.tsx`

#### Database
- [ ] Uses `supabaseAdmin` for server-side operations
- [ ] Uses proper client helpers (`createRouteHandlerClientAsync`, `createServerActionClientAsync`)
- [ ] No N+1 queries (use `.select()` with relations)
- [ ] Proper error handling for database operations

### 🟡 Medium Priority (Fix Soon)

#### Code Quality
- [ ] Functions < 50 lines (recommended)
- [ ] Files < 200 lines (recommended)
- [ ] Single Responsibility Principle
- [ ] DRY principle (no duplicate logic)
- [ ] Meaningful variable/function names
- [ ] No commented-out code
- [ ] TODO comments have ticket references

#### Performance
- [ ] `next/image` used instead of `<img>` tags
- [ ] Images have proper dimensions
- [ ] Suspense boundaries for async data
- [ ] Parallel data fetching with `Promise.all()`
- [ ] Proper caching strategy
- [ ] No unnecessary re-renders

#### Cloudinary
- [ ] Environment variables validated
- [ ] Signature generation correct (sorted params, SHA1)
- [ ] URL validation before saving
- [ ] Rollback pattern implemented
- [ ] WebP conversion applied

### 🟢 Low Priority (Nice to Have)

#### Documentation
- [ ] Complex logic has comments explaining WHY
- [ ] API routes have JSDoc comments
- [ ] Server Actions have type documentation
- [ ] README updated if needed

#### Testing
- [ ] Critical paths have tests
- [ ] Edge cases considered
- [ ] Error scenarios tested

## Review Workflow

### Step 1: Pre-Review Context
```bash
# Understand project structure
ls -la app/ components/ lib/
cat package.json | grep -A 5 "dependencies"
cat tsconfig.json | grep -A 3 "compilerOptions"
cat .eslintrc.json
```

### Step 2: Pattern Detection
```bash
# Detect error handling patterns
grep -r "error-handler" app/ --include="*.ts" | head -5

# Detect Server Action patterns
grep -r "'use server'" app/actions/ --include="*.ts" | head -5

# Detect Supabase patterns
grep -r "supabaseAdmin\|createRouteHandlerClientAsync" app/ --include="*.ts" | head -5
```

### Step 3: File-Specific Review
For each file being reviewed:
```bash
FILE="app/api/example/route.ts"

# Check error handling
grep -n "error" "$FILE" | grep -v "error-handler"

# Check authentication
grep -n "getUser\|getSession" "$FILE"

# Check validation
grep -n "validate\|safeParse" "$FILE"

# Check database operations
grep -n "supabase\.from\|supabaseAdmin\.from" "$FILE"
```

### Step 4: Cross-File Analysis
```bash
# Find where file is imported
grep -r "from.*example\|import.*example" app/ components/ --include="*.ts" --include="*.tsx"

# Find similar patterns
grep -r "similarPattern" app/ --include="*.ts" | cut -d: -f1 | uniq
```

### Step 5: Generate Review Report
Use the Review Output Template (see above) to structure findings.

## Common Issues & Solutions

### Issue: Raw Error Messages Exposed
**Problem**: `return NextResponse.json({ error: error.message }, { status: 500 })`

**Solution**:
```typescript
import { handleDatabaseError } from '@/lib/error-handler'
const { message, statusCode } = handleDatabaseError(error, 'Failed to create')
return NextResponse.json({ error: message }, { status: statusCode })
```

### Issue: Missing Revalidation
**Problem**: Server Action mutates data but doesn't revalidate cache

**Solution**:
```typescript
import { revalidatePath } from 'next/cache'
// ... mutation code ...
revalidatePath('/books')
revalidatePath(`/books/${bookId}`, 'page')
```

### Issue: N+1 Query Problem
**Problem**: Looping over results and making separate queries

**Solution**:
```typescript
// ❌ WRONG
const books = await supabase.from('books').select('*')
for (const book of books.data || []) {
  const author = await supabase.from('authors').select('*').eq('id', book.author_id).single()
}

// ✅ CORRECT
const books = await supabase
  .from('books')
  .select('id, title, authors(id, name)') // Single query with relations
```

### Issue: Missing Authentication Check
**Problem**: Route handler doesn't verify user authentication

**Solution**:
```typescript
const supabase = await createRouteHandlerClientAsync()
const { data: { user }, error: authError } = await supabase.auth.getUser()
if (authError || !user) {
  return NextResponse.json(unauthorizedError(), { status: 401 })
}
```

### Issue: Using `any` Types
**Problem**: `function process(data: any): any`

**Solution**:
```typescript
interface ProcessData {
  id: string
  name: string
}

interface ProcessResult {
  success: boolean
  data?: ProcessData
  error?: string
}

function process(data: ProcessData): ProcessResult {
  // Implementation
}
```

## Automatic Fix Capabilities

### Auto-Fix Patterns

The code review skill can automatically fix common issues:

#### 1. Error Handling Auto-Fix
**Pattern Detection**:
```bash
# Find raw error.message usage
grep -r "error\.message" app/api/ --include="route.ts" | grep -v "error-handler"
```

**Auto-Fix Logic**:
```typescript
// Detect: return NextResponse.json({ error: error.message }, { status: 500 })
// Fix: Replace with handleDatabaseError()

// BEFORE
if (error) {
  return NextResponse.json({ error: error.message }, { status: 500 })
}

// AFTER (Auto-fixed)
import { handleDatabaseError } from '@/lib/error-handler'
const { message, statusCode } = handleDatabaseError(error, 'Failed to create')
return NextResponse.json({ error: message }, { status: statusCode })
```

#### 2. Missing Revalidation Auto-Fix
**Pattern Detection**:
```bash
# Find Server Actions without revalidation
grep -r "'use server'" app/actions/ --include="*.ts" | while read file; do
  if ! grep -q "revalidatePath\|revalidateTag" "$file"; then
    echo "Missing revalidation: $file"
  fi
done
```

**Auto-Fix Logic**:
```typescript
// Detect: Server Action with mutation but no revalidation
// Fix: Add revalidatePath based on context

// BEFORE
export async function createBook(data: BookData) {
  const book = await insertBook(data)
  return { success: true, book }
}

// AFTER (Auto-fixed)
import { revalidatePath } from 'next/cache'
export async function createBook(data: BookData) {
  const book = await insertBook(data)
  revalidatePath('/books')
  if (book.id) {
    revalidatePath(`/books/${book.id}`, 'page')
  }
  return { success: true, book }
}
```

#### 3. Missing Authentication Auto-Fix
**Pattern Detection**:
```bash
# Find API routes without auth checks
grep -r "export async function POST\|export async function PUT\|export async function DELETE" app/api/ --include="route.ts" | while read file; do
  if ! grep -q "getUser\|getSession" "$file"; then
    echo "Missing auth: $file"
  fi
done
```

**Auto-Fix Logic**:
```typescript
// Detect: API route without authentication
// Fix: Add authentication check at start

// BEFORE
export async function POST(request: NextRequest) {
  const json = await request.json()
  // ... process
}

// AFTER (Auto-fixed)
import { createRouteHandlerClientAsync } from '@/lib/supabase/client-helper'
import { unauthorizedError } from '@/lib/error-handler'

export async function POST(request: NextRequest) {
  const supabase = await createRouteHandlerClientAsync()
  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) {
    return NextResponse.json(unauthorizedError(), { status: 401 })
  }
  const json = await request.json()
  // ... process
}
```

#### 4. Type Safety Auto-Fix
**Pattern Detection**:
```bash
# Find any types
grep -r ": any\|as any" app/ components/ --include="*.ts" --include="*.tsx"
```

**Auto-Fix Logic**:
```typescript
// Detect: function process(data: any): any
// Fix: Infer or create proper types

// BEFORE
function process(data: any): any {
  return { success: true, data }
}

// AFTER (Auto-fixed)
interface ProcessData {
  id: string
  name: string
}

interface ProcessResult {
  success: boolean
  data?: ProcessData
}

function process(data: ProcessData): ProcessResult {
  return { success: true, data }
}
```

#### 5. Missing 'use server' Auto-Fix
**Pattern Detection**:
```bash
# Find Server Actions without directive
grep -r "export async function" app/actions/ --include="*.ts" | while read file; do
  if ! grep -q "'use server'" "$file"; then
    echo "Missing 'use server': $file"
  fi
done
```

**Auto-Fix Logic**:
```typescript
// Detect: Server Action without 'use server'
// Fix: Add directive at top of file

// BEFORE
import { supabaseAdmin } from '@/lib/supabase/server'
export async function createActivity(params: CreateActivityParams) {
  // ...
}

// AFTER (Auto-fixed)
'use server'
import { supabaseAdmin } from '@/lib/supabase/server'
export async function createActivity(params: CreateActivityParams) {
  // ...
}
```

#### 6. Console.log Removal Auto-Fix
**Pattern Detection**:
```bash
# Find console.log statements
grep -r "console\.log\|console\.debug" app/ components/ --include="*.ts" --include="*.tsx" | grep -v "node_modules\|error-handler"
```

**Auto-Fix Logic**:
```typescript
// Detect: console.log('Debug:', data)
// Fix: Remove or comment out

// BEFORE
console.log('Debug:', data)
console.debug('User:', user)

// AFTER (Auto-fixed)
// Removed debug statements
// Use proper logging utility if needed: logger.debug('Debug:', data)
```

#### 7. Missing Imports Auto-Fix
**Pattern Detection**:
```bash
# Find usage without imports
grep -r "revalidatePath\|handleDatabaseError\|NextResponse" app/ --include="*.ts" | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  symbol=$(echo "$line" | grep -oE "(revalidatePath|handleDatabaseError|NextResponse)")
  if ! grep -q "import.*$symbol" "$file"; then
    echo "Missing import: $file - $symbol"
  fi
done
```

**Auto-Fix Logic**:
```typescript
// Detect: Usage of symbol without import
// Fix: Add appropriate import

// BEFORE
export async function createBook(data: BookData) {
  const book = await insertBook(data)
  revalidatePath('/books') // Missing import
  return NextResponse.json({ success: true }) // Missing import
}

// AFTER (Auto-fixed)
import { revalidatePath } from 'next/cache'
import { NextResponse } from 'next/server'

export async function createBook(data: BookData) {
  const book = await insertBook(data)
  revalidatePath('/books')
  return NextResponse.json({ success: true })
}
```

### Auto-Fix Execution

When auto-fix is enabled, the review process:

1. **Scans** the modified files for known patterns
2. **Identifies** fixable issues automatically
3. **Applies** fixes using search_replace tool
4. **Validates** fixes don't break functionality
5. **Reports** what was fixed and what needs manual review

### Auto-Fix Safety Rules

**Always Auto-Fix** (Safe, non-breaking):
- ✅ Missing imports
- ✅ Missing `'use server'` directive
- ✅ Console.log removal
- ✅ Type safety improvements (when types can be inferred)
- ✅ Missing `revalidatePath`/`revalidateTag` (when context is clear)

**Never Auto-Fix** (Require human review):
- 🔴 Security-related changes
- 🔴 Database schema modifications
- 🔴 Complex refactoring (>50 lines)
- 🔴 Breaking API changes
- 🔴 Performance optimizations requiring analysis

**Ask Before Fixing**:
- 🟡 Large changes (>3 files affected)
- 🟡 Changes to shared utilities
- 🟡 Changes affecting multiple components
- 🟡 Ambiguous fixes (multiple valid solutions)

### Auto-Fix Report Format

```markdown
## [AUTO-FIX] Automatic Fixes Applied

**File**: `app/api/example/route.ts`
**Fixes Applied**: 5
**Manual Review Required**: 2

### ✅ Auto-Fixed
1. ✅ Added missing import: `handleDatabaseError` from `@/lib/error-handler`
2. ✅ Replaced `error.message` with `handleDatabaseError(error, 'Failed to create')`
3. ✅ Added authentication check at start of POST handler
4. ✅ Removed `console.log('Debug:', data)` statement
5. ✅ Added `'use server'` directive to Server Action

### ⚠️ Requires Manual Review
1. ⚠️ Potential N+1 query detected - Line 45
   - **Issue**: Loop with database query inside
   - **Suggestion**: Use `.select()` with relations
   
2. ⚠️ Missing input validation - Line 30
   - **Issue**: No validation before database insert
   - **Suggestion**: Add Zod schema validation
```

## Success Metrics

A quality review should:
- ✅ Understand project context and conventions
- ✅ Provide root cause analysis, not just symptoms
- ✅ Include working code solutions
- ✅ Prioritize by real impact
- ✅ Consider evolution and maintenance
- ✅ Suggest proactive improvements
- ✅ Reference related code and patterns
- ✅ Adapt to project's architectural style
- ✅ Check project-specific patterns (Next.js, Supabase, Cloudinary)
- ✅ Verify error handling uses `@/lib/error-handler`
- ✅ Ensure type safety (no `any` types)
- ✅ Validate Server Actions have revalidation
- ✅ Confirm security best practices
- ✅ Automatically fix common issues when safe
- ✅ Flag issues requiring manual review appropriately
