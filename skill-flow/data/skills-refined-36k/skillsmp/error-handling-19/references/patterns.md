# Error Handling Patterns

## Patterns

### **Result Type**
  #### **Description**
Result type for explicit error handling
  #### **Why Over Exceptions**
    | Aspect | Result Types | Exceptions |
    |--------|--------------|------------|
    | Visibility | Errors in type signature | Hidden in implementation |
    | Composability | map/flatMap chains | Try-catch nesting |
    | Forgettable | Compiler enforces handling | Easy to forget |
    | Performance | No stack trace overhead | Stack trace on every throw |
    
  #### **Example**
    type Result<T, E = Error> =
      | { success: true; data: T }
      | { success: false; error: E };
    
    function ok<T>(data: T): Result<T, never> {
      return { success: true, data };
    }
    
    function err<E>(error: E): Result<never, E> {
      return { success: false, error };
    }
    
    // Utility functions for composition
    function map<T, U, E>(result: Result<T, E>, fn: (data: T) => U): Result<U, E> {
      return result.success ? ok(fn(result.data)) : result;
    }
    
    function flatMap<T, U, E>(result: Result<T, E>, fn: (data: T) => Result<U, E>): Result<U, E> {
      return result.success ? fn(result.data) : result;
    }
    
    function unwrapOr<T, E>(result: Result<T, E>, defaultValue: T): T {
      return result.success ? result.data : defaultValue;
    }
    
    // Async Result handling
    async function mapAsync<T, U, E>(
      result: Result<T, E>,
      fn: (data: T) => Promise<U>
    ): Promise<Result<U, E>> {
      return result.success ? ok(await fn(result.data)) : result;
    }
    
    // Result.all for parallel operations
    function resultAll<T, E>(results: Result<T, E>[]): Result<T[], E> {
      const values: T[] = [];
      for (const result of results) {
        if (!result.success) return result;
        values.push(result.data);
      }
      return ok(values);
    }
    
    // Practical usage
    async function getUser(id: string): Promise<Result<User, UserError>> {
      try {
        const user = await db.query.users.findFirst({
          where: eq(users.id, id),
        });
        if (!user) {
          return err({ code: "NOT_FOUND", message: "User not found" });
        }
        return ok(user);
      } catch (e) {
        return err({ code: "DB_ERROR", message: "Database error" });
      }
    }
    
    // Composing Results
    const enrichedUser = await mapAsync(
      await getUser(id),
      async (user) => ({ ...user, profile: await fetchProfile(user.id) })
    );
    
    // Parallel operations with Result.all
    const [user, posts, settings] = await Promise.all([
      getUser(id),
      getPosts(id),
      getSettings(id),
    ]);
    const combined = resultAll([user, posts, settings]);
    
  #### **When Not To Use**
    - Simple scripts where exceptions are fine
    - Framework code that expects exceptions (Express error handlers)
    - When team isn't familiar with the pattern
    
  #### **Advanced Utilities**
    // Result.partition - separate successes from failures
    function partition<T, E>(results: Result<T, E>[]): { successes: T[]; failures: E[] } {
      const successes: T[] = [];
      const failures: E[] = [];
      for (const result of results) {
        if (result.success) successes.push(result.data);
        else failures.push(result.error);
      }
      return { successes, failures };
    }
    
    // Result.traverse - apply fallible operation to array, collect all or fail
    async function traverse<T, U, E>(
      items: T[],
      fn: (item: T) => Promise<Result<U, E>>
    ): Promise<Result<U[], E>> {
      const results: U[] = [];
      for (const item of items) {
        const result = await fn(item);
        if (!result.success) return result;
        results.push(result.data);
      }
      return ok(results);
    }
    
    // Result.recover - transform error to success (fallback)
    function recover<T, E>(
      result: Result<T, E>,
      fallback: (error: E) => T
    ): Result<T, never> {
      return result.success ? result : ok(fallback(result.error));
    }
    
    // Result.tap - side effect without changing result (logging, metrics)
    function tap<T, E>(
      result: Result<T, E>,
      onSuccess: (data: T) => void,
      onError?: (error: E) => void
    ): Result<T, E> {
      if (result.success) onSuccess(result.data);
      else onError?.(result.error);
      return result;
    }
    
    // Result.match - exhaustive pattern matching
    function match<T, E, R>(
      result: Result<T, E>,
      handlers: { ok: (data: T) => R; err: (error: E) => R }
    ): R {
      return result.success ? handlers.ok(result.data) : handlers.err(result.error);
    }
    
    // Usage example with all utilities
    const users = await traverse(userIds, getUser);
    const { successes, failures } = partition(results);
    
    const finalResult = tap(
      recover(apiResult, (err) => ({ fallback: true, reason: err.message })),
      (data) => logger.info('Success', data),
      (err) => logger.warn('Using fallback', err)
    );
    
    const message = match(result, {
      ok: (user) => `Welcome, ${user.name}!`,
      err: (e) => `Error: ${e.message}`,
    });
    
  #### **Performance Benchmarks**
    // Performance characteristics
    //
    // | Scenario                    | Result Type | Exceptions |
    // |-----------------------------|-------------|------------|
    // | Happy path (no error)       | ~same       | ~same      |
    // | Error path (rare)           | Faster      | Slower*    |
    // | Error path (frequent)       | Much faster | Much slower|
    // | Stack trace needed          | Manual      | Automatic  |
    // | Memory per error            | Lower       | Higher     |
    //
    // *Exceptions are slower due to stack trace capture
    //
    // Rule of thumb:
    // - Expected failures (validation, not found): Use Result
    // - Unexpected failures (bugs, crashes): Use Exceptions
    // - Hot paths with frequent failures: Definitely Result
    
    // Benchmark example (pseudo-code)
    // Result: ~50ns per error (no stack trace)
    // Exception: ~5000ns per error (with stack trace)
    //
    // For 10,000 validation errors:
    // Result: 0.5ms
    // Exception: 50ms (100x slower)
    
  #### **Validation Integration**
    import { z } from 'zod';
    
    // Convert Zod result to Result type
    function fromZod<T>(schema: z.ZodSchema<T>, data: unknown): Result<T, ValidationError> {
      const parsed = schema.safeParse(data);
      if (parsed.success) {
        return ok(parsed.data);
      }
      return err(new ValidationError(
        'Validation failed',
        Object.fromEntries(
          parsed.error.issues.map(i => [i.path.join('.'), [i.message]])
        )
      ));
    }
    
    // Usage with API handler
    const UserSchema = z.object({
      email: z.string().email(),
      name: z.string().min(1),
      age: z.number().min(0).optional(),
    });
    
    async function createUser(body: unknown): Promise<Result<User, AppError>> {
      const validated = fromZod(UserSchema, body);
      if (!validated.success) return validated;
    
      return await userRepository.create(validated.data);
    }
    
  #### **Debugging Patterns**
    // Problem: Result chains hide where errors originated
    // Solution: Add debug context at each step
    
    // Debug-aware Result wrapper
    function withDebug<T, E>(
      result: Result<T, E>,
      context: string
    ): Result<T, E & { _debug?: string[] }> {
      if (result.success) return result;
    
      const debugPath = (result.error as any)._debug || [];
      return err({
        ...result.error,
        _debug: [...debugPath, context],
      } as E & { _debug: string[] });
    }
    
    // Usage: trace error origin through chain
    const result = await pipe(
      getUser(id),
      (r) => withDebug(r, 'getUser'),
      (r) => flatMap(r, enrichProfile),
      (r) => withDebug(r, 'enrichProfile'),
      (r) => flatMap(r, validatePermissions),
      (r) => withDebug(r, 'validatePermissions'),
    );
    
    if (!result.success) {
      console.log('Error path:', result.error._debug);
      // Output: ['getUser', 'enrichProfile'] - failed at enrichProfile
    }
    
    // VS Code debugging tip: Add conditional breakpoint
    // Condition: !result.success
    // This pauses only when Result is an error
    
### **Typed Errors**
  #### **Description**
Typed error classes with operational vs programming distinction
  #### **Key Distinction**
    ##### **Operational Errors**
Expected failures (bad input, not found, rate limit) - return to client with details
    ##### **Programming Errors**
Bugs that shouldn't happen (null access, type errors) - crash, alert, hide from client
  #### **Performance Note**
Error creation with stack traces has overhead - avoid in hot paths. Use Result types for high-frequency expected failures.
  #### **Error Tracking Integration**
    - Include error.cause for chained errors
    - Add toJSON() for structured logging
    - Use Error.captureStackTrace for clean traces
    - Tag errors with requestId for correlation
  #### **Example**
    // errors/base.ts - Abstract base with operational vs programming
    export abstract class AppError extends Error {
      abstract readonly code: string;
      abstract readonly statusCode: number;
      abstract readonly isOperational: boolean;
    
      constructor(message: string, public readonly cause?: Error) {
        super(message);
        this.name = this.constructor.name;
        Error.captureStackTrace(this, this.constructor);
      }
    
      // Structured serialization for logging and responses
      toJSON() {
        return {
          code: this.code,
          message: this.message,
          ...(process.env.NODE_ENV === 'development' && {
            stack: this.stack,
            cause: this.cause?.message,
          }),
        };
      }
    }
    
    // Operational: expected failures - safe to show client
    export abstract class OperationalError extends AppError {
      readonly isOperational = true;
    }
    
    // Programming: bugs - hide from client, alert team
    export abstract class ProgrammerError extends AppError {
      readonly isOperational = false;
    }
    
    // Concrete operational errors
    export class NotFoundError extends OperationalError {
      readonly code = 'NOT_FOUND';
      readonly statusCode = 404;
      constructor(resource: string, id?: string) {
        super(id ? `${resource} with ID ${id} not found` : `${resource} not found`);
      }
    }
    
    export class ValidationError extends OperationalError {
      readonly code = 'VALIDATION_ERROR';
      readonly statusCode = 400;
      constructor(message: string, public readonly fields: Record<string, string[]>) {
        super(message);
      }
    }
    
    export class UnauthorizedError extends OperationalError {
      readonly code = 'UNAUTHORIZED';
      readonly statusCode = 401;
      constructor(message = 'Authentication required') { super(message); }
    }
    
    export class ForbiddenError extends OperationalError {
      readonly code = 'FORBIDDEN';
      readonly statusCode = 403;
      constructor(message = 'Access denied') { super(message); }
    }
    
    export class ConflictError extends OperationalError {
      readonly code = 'CONFLICT';
      readonly statusCode = 409;
      constructor(message: string) { super(message); }
    }
    
    export class RateLimitError extends OperationalError {
      readonly code = 'RATE_LIMIT';
      readonly statusCode = 429;
      constructor(public readonly retryAfter: number) {
        super(`Rate limit exceeded. Retry after ${retryAfter}s`);
      }
    }
    
    // Error codes enum - useful for microservices and client SDKs
    export const ErrorCodes = {
      // Client errors (4xx)
      VALIDATION_ERROR: 'VALIDATION_ERROR',
      NOT_FOUND: 'NOT_FOUND',
      UNAUTHORIZED: 'UNAUTHORIZED',
      FORBIDDEN: 'FORBIDDEN',
      CONFLICT: 'CONFLICT',
      RATE_LIMIT: 'RATE_LIMIT',
    
      // Server errors (5xx)
      INTERNAL_ERROR: 'INTERNAL_ERROR',
      SERVICE_UNAVAILABLE: 'SERVICE_UNAVAILABLE',
      GATEWAY_ERROR: 'GATEWAY_ERROR',
    
      // Domain-specific (extend per service)
      PAYMENT_FAILED: 'PAYMENT_FAILED',
      INVENTORY_EXHAUSTED: 'INVENTORY_EXHAUSTED',
    } as const;
    
    export type ErrorCode = typeof ErrorCodes[keyof typeof ErrorCodes];
    
    // Global error handler with operational distinction
    export function errorHandler(err: Error, req: Request): Response {
      const requestId = req.headers.get('x-request-id') || crypto.randomUUID();
    
      // Log all errors with context
      console.error('[Error]', {
        requestId,
        message: err.message,
        stack: err.stack,
        url: req.url,
      });
    
      // Operational: return details to client
      if (err instanceof OperationalError) {
        return Response.json(
          { ...err.toJSON(), requestId },
          { status: err.statusCode }
        );
      }
    
      // Programming error: hide details, alert team
      if (err instanceof AppError && !err.isOperational) {
        captureException(err, { tags: { requestId } });
      }
    
      // Unknown: generic message
      return Response.json(
        { code: 'INTERNAL_ERROR', message: 'Something went wrong', requestId },
        { status: 500 }
      );
    }
    
    // Type guards for exhaustive handling
    function isNotFoundError(e: unknown): e is NotFoundError {
      return e instanceof NotFoundError;
    }
    
    // Usage with exhaustive checking
    try {
      await updateUser(id, data);
    } catch (e) {
      if (isNotFoundError(e)) return handleNotFound(e);
      if (e instanceof ValidationError) return handleValidation(e);
      throw e; // Re-throw unexpected errors
    }
    
### **Error Boundary**
  #### **Description**
React error boundaries for graceful failure isolation
  #### **What Boundaries Catch**
    - Errors during rendering
    - Errors in lifecycle methods
    - Errors in constructors of child components
  #### **What Boundaries Dont Catch**
    - Event handlers (use try-catch inside handlers)
    - Async code (setTimeout, requestAnimationFrame, promises)
    - Server-side rendering errors
    - Errors thrown in the error boundary itself
  #### **Strategic Placement**
    ##### **Route Level**
app/error.tsx - catches route segment errors
    ##### **Global Level**
app/global-error.tsx - catches root layout errors (must include <html>)
    ##### **Component Level**
Wrap risky components (external data, user content, third-party libs)
    ##### **Granular Rule**
Not every component needs a boundary - add around data-dependent, user-generated, or third-party components
  #### **Performance Note**
Error boundaries have minimal overhead - the class component stays mounted and only activates on error
  #### **Example**
    // app/error.tsx - Route-level boundary (Next.js App Router)
    "use client";
    
    import { useEffect } from 'react';
    import { captureException } from '@sentry/nextjs';
    
    export default function Error({
      error,
      reset,
    }: {
      error: Error & { digest?: string };
      reset: () => void;
    }) {
      useEffect(() => {
        // Log to error tracking with digest for server correlation
        captureException(error, { tags: { digest: error.digest } });
      }, [error]);
    
      return (
        <div className="flex min-h-[400px] flex-col items-center justify-center gap-4">
          <h2>Something went wrong</h2>
          <p className="text-muted-foreground">We've been notified.</p>
          <div className="flex gap-2">
            <button onClick={() => window.location.reload()}>Refresh</button>
            <button onClick={reset}>Try again</button>
          </div>
        </div>
      );
    }
    
    // app/global-error.tsx - Root layout errors (MUST include html/body)
    "use client";
    export default function GlobalError({ error, reset }) {
      return (
        <html><body>
          <h1>Critical Error</h1>
          <button onClick={reset}>Reset</button>
        </body></html>
      );
    }
    
    // Reusable boundary component for granular use
    class ErrorBoundary extends React.Component<
      { children: ReactNode; fallback?: ReactNode; onError?: (e: Error) => void },
      { hasError: boolean; error: Error | null }
    > {
      state = { hasError: false, error: null };
    
      static getDerivedStateFromError(error: Error) {
        return { hasError: true, error };
      }
    
      componentDidCatch(error: Error, info: React.ErrorInfo) {
        this.props.onError?.(error);
        captureException(error, { extra: { componentStack: info.componentStack } });
      }
    
      render() {
        if (this.state.hasError) {
          return this.props.fallback ?? <DefaultFallback />;
        }
        return this.props.children;
      }
    }
    
    // Strategic granular boundaries
    export default function Dashboard() {
      return (
        <div>
          <Header /> {/* Simple, trusted - no boundary */}
    
          <ErrorBoundary fallback={<ChartSkeleton />}>
            <AnalyticsChart /> {/* External API data - risky */}
          </ErrorBoundary>
    
          <ErrorBoundary fallback={<FeedSkeleton />}>
            <ActivityFeed /> {/* User-generated content - risky */}
          </ErrorBoundary>
        </div>
      );
    }
    
    // Event handlers need try-catch (boundaries don't catch these!)
    function RiskyButton() {
      const handleClick = async () => {
        try {
          await riskyOperation();
        } catch (e) {
          toast.error('Operation failed');
          captureException(e);
        }
      };
      return <button onClick={handleClick}>Click</button>;
    }
    
    // Suspense + Error Boundary combo (React 18+)
    import { Suspense } from 'react';
    
    function DataSection() {
      return (
        <ErrorBoundary fallback={<DataError />}>
          <Suspense fallback={<DataSkeleton />}>
            <AsyncDataComponent /> {/* Uses use() or throws promise */}
          </Suspense>
        </ErrorBoundary>
      );
    }
    
    // Suspense with error handling for data fetching
    function useDataWithSuspense<T>(fetcher: () => Promise<T>): T {
      const [promise] = useState(() => fetcher());
      const [result, setResult] = useState<{ data?: T; error?: Error } | null>(null);
    
      if (!result) {
        throw promise.then(
          data => setResult({ data }),
          error => setResult({ error })
        );
      }
    
      if (result.error) throw result.error; // Caught by ErrorBoundary
      return result.data!;
    }
    
### **Retry With Backoff**
  #### **Description**
Retry transient failures with exponential backoff and jitter
  #### **Key Principle**
Retry transient failures, fail fast on permanent errors
  #### **Transient Errors**
    ##### **Should Retry**
      - 429 Too Many Requests
      - 502 Bad Gateway
      - 503 Service Unavailable
      - 504 Gateway Timeout
      - ECONNREFUSED, ETIMEDOUT, ECONNRESET
      - Network errors (fetch failed)
    ##### **Should Not Retry**
      - 400 Bad Request (your bug)
      - 401 Unauthorized (auth is broken)
      - 403 Forbidden (permission issue)
      - 404 Not Found (resource doesn't exist)
      - 422 Validation Error (bad input)
  #### **Jitter Importance**
Without jitter, retries synchronize causing thundering herd - always add random jitter
  #### **Logging Requirement**
Always log retry attempts with attempt number, delay, and error for debugging
  #### **Example**
    // Production-ready retry with logging, jitter, and transient detection
    async function withRetry<T>(
      fn: () => Promise<T>,
      options: {
        maxAttempts?: number;
        baseDelay?: number;
        maxDelay?: number;
        shouldRetry?: (error: Error) => boolean;
        onRetry?: (error: Error, attempt: number, delay: number) => void;
      } = {}
    ): Promise<T> {
      const {
        maxAttempts = 3,
        baseDelay = 1000,
        maxDelay = 30000,
        shouldRetry = isTransientError,
        onRetry = defaultRetryLogger,
      } = options;
    
      let lastError: Error;
    
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
          return await fn();
        } catch (error) {
          lastError = error as Error;
    
          // Don't retry if max attempts reached or error is permanent
          if (attempt === maxAttempts || !shouldRetry(lastError)) {
            throw lastError;
          }
    
          // Exponential backoff with jitter (prevents thundering herd)
          const exponentialDelay = baseDelay * Math.pow(2, attempt - 1);
          const jitter = Math.random() * 1000; // 0-1s random jitter
          const delay = Math.min(exponentialDelay + jitter, maxDelay);
    
          // Log retry attempt (critical for debugging)
          onRetry(lastError, attempt, delay);
    
          await new Promise(r => setTimeout(r, delay));
        }
      }
    
      throw lastError!;
    }
    
    // Default logger - always log retries!
    function defaultRetryLogger(error: Error, attempt: number, delay: number) {
      console.warn(`[Retry] Attempt ${attempt} failed, retrying in ${delay.toFixed(0)}ms`, {
        error: error.message,
        attempt,
        delay,
      });
    }
    
    // Transient error detection
    function isTransientError(error: Error): boolean {
      // Network errors - always transient
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return true;
      }
    
      // Connection errors
      const message = error.message.toLowerCase();
      if (message.includes('econnrefused') ||
          message.includes('etimedout') ||
          message.includes('econnreset') ||
          message.includes('socket hang up')) {
        return true;
      }
    
      // HTTP status codes that might be transient
      if ('status' in error) {
        const status = (error as any).status;
        return status === 429 || status === 502 || status === 503 || status === 504;
      }
    
      // Database transient errors
      if (message.includes('deadlock') ||
          message.includes('lock wait timeout') ||
          message.includes('connection pool')) {
        return true;
      }
    
      return false;
    }
    
    // Usage examples
    // API calls
    const data = await withRetry(
      () => fetch('/api/data').then(r => {
        if (!r.ok) throw Object.assign(new Error(r.statusText), { status: r.status });
        return r.json();
      }),
      { maxAttempts: 3, baseDelay: 1000 }
    );
    
    // Database operations
    const user = await withRetry(
      () => db.query.users.findFirst({ where: eq(users.id, id) }),
      {
        maxAttempts: 3,
        shouldRetry: (e) => e.message.includes('deadlock'),
        onRetry: (e, attempt) => {
          logger.warn({ error: e, attempt }, 'DB retry');
        },
      }
    );
    
    // With custom backoff for rate limits
    const result = await withRetry(
      () => rateLimitedAPI.call(),
      {
        maxAttempts: 5,
        baseDelay: 2000, // Start higher for rate limits
        maxDelay: 60000, // Allow longer waits
      }
    );
    
### **Circuit Breaker**
  #### **Description**
Stop calling failing services - fail fast instead of waiting
  #### **States**
    ##### **Closed**
Normal operation - requests pass through
    ##### **Open**
Failing - requests rejected immediately without calling service
    ##### **Half Open**
Testing - one request allowed to check if service recovered
  #### **When To Use**
    - External API calls that might be down
    - Database connections under load
    - Microservice communication
    - Any remote call that can fail and cause cascading failures
  #### **Example**
    class CircuitBreaker {
      private state: 'closed' | 'open' | 'half-open' = 'closed';
      private failureCount = 0;
      private lastFailureTime = 0;
      private successCount = 0;
    
      constructor(
        private readonly options: {
          failureThreshold: number;     // Failures before opening
          resetTimeout: number;         // Time before trying again (ms)
          successThreshold: number;     // Successes to close from half-open
          onStateChange?: (from: string, to: string) => void;
        }
      ) {}
    
      async execute<T>(fn: () => Promise<T>): Promise<T> {
        if (this.state === 'open') {
          if (Date.now() - this.lastFailureTime >= this.options.resetTimeout) {
            this.transition('half-open');
          } else {
            throw new CircuitOpenError('Circuit breaker is open');
          }
        }
    
        try {
          const result = await fn();
          this.onSuccess();
          return result;
        } catch (error) {
          this.onFailure();
          throw error;
        }
      }
    
      private onSuccess() {
        if (this.state === 'half-open') {
          this.successCount++;
          if (this.successCount >= this.options.successThreshold) {
            this.transition('closed');
          }
        }
        this.failureCount = 0;
      }
    
      private onFailure() {
        this.failureCount++;
        this.lastFailureTime = Date.now();
    
        if (this.state === 'half-open') {
          this.transition('open');
        } else if (this.failureCount >= this.options.failureThreshold) {
          this.transition('open');
        }
      }
    
      private transition(newState: 'closed' | 'open' | 'half-open') {
        const oldState = this.state;
        this.state = newState;
        if (newState === 'closed') {
          this.failureCount = 0;
          this.successCount = 0;
        }
        this.options.onStateChange?.(oldState, newState);
      }
    }
    
    // Usage
    const paymentCircuit = new CircuitBreaker({
      failureThreshold: 5,
      resetTimeout: 30000,
      successThreshold: 3,
      onStateChange: (from, to) => {
        logger.warn({ from, to }, 'Payment circuit state change');
        if (to === 'open') alertOps('Payment service circuit opened');
      },
    });
    
    async function processPayment(order: Order) {
      return paymentCircuit.execute(() => paymentService.charge(order));
    }
    
### **Bulkhead**
  #### **Description**
Isolate failures - don't let one slow service exhaust all resources
  #### **Concept**
Like ship compartments - flood one, others stay dry
  #### **Implementation Options**
    - Separate thread pools per service
    - Semaphores to limit concurrent calls
    - Queue with max size per operation type
  #### **Example**
    class Bulkhead {
      private currentConcurrency = 0;
      private queue: Array<{ resolve: () => void }> = [];
    
      constructor(
        private readonly maxConcurrency: number,
        private readonly maxQueueSize: number = 100
      ) {}
    
      async execute<T>(fn: () => Promise<T>): Promise<T> {
        if (this.currentConcurrency >= this.maxConcurrency) {
          if (this.queue.length >= this.maxQueueSize) {
            throw new BulkheadFullError('Bulkhead queue full');
          }
          await new Promise<void>(resolve => this.queue.push({ resolve }));
        }
    
        this.currentConcurrency++;
        try {
          return await fn();
        } finally {
          this.currentConcurrency--;
          const next = this.queue.shift();
          next?.resolve();
        }
      }
    }
    
    // Separate bulkheads per external service
    const paymentBulkhead = new Bulkhead(10);   // Max 10 concurrent payment calls
    const inventoryBulkhead = new Bulkhead(20); // Max 20 concurrent inventory calls
    
    // Slow inventory service won't block payment processing
    async function checkout(order: Order) {
      const [payment, inventory] = await Promise.all([
        paymentBulkhead.execute(() => chargeCard(order)),
        inventoryBulkhead.execute(() => reserveItems(order)),
      ]);
    }
    
### **Structured Logging**
  #### **Description**
Log errors with context for debugging and correlation
  #### **Key Fields**
    ##### **Required**
      - timestamp
      - level (error, warn, info)
      - message
      - error.name
      - error.message
      - error.stack
    ##### **Recommended**
      - requestId (for correlation)
      - userId
      - traceId (for distributed tracing)
      - spanId
      - service
      - environment
  #### **Example**
    import pino from 'pino';
    
    const logger = pino({
      level: process.env.LOG_LEVEL || 'info',
      formatters: {
        level: (label) => ({ level: label }),
      },
      base: {
        service: 'api-gateway',
        environment: process.env.NODE_ENV,
      },
    });
    
    // Create child logger with request context
    function createRequestLogger(req: Request) {
      return logger.child({
        requestId: req.headers.get('x-request-id') || crypto.randomUUID(),
        traceId: req.headers.get('x-trace-id'),
        userId: req.user?.id,
        path: req.url,
        method: req.method,
      });
    }
    
    // Structured error logging
    function logError(log: pino.Logger, error: Error, context?: object) {
      log.error({
        err: {
          name: error.name,
          message: error.message,
          stack: error.stack,
          code: (error as any).code,
          cause: error.cause,
        },
        ...context,
      }, error.message);
    }
    
    // Usage in error handler
    app.use((err, req, res, next) => {
      const log = createRequestLogger(req);
      logError(log, err, {
        body: req.body,
        query: req.query,
      });
      // ... handle response
    });
    
### **Testing Error Handling**
  #### **Description**
Test your error handling - it's often the least tested code
  #### **Patterns**
    ##### **Unit Tests**
      // Test that errors are thrown correctly
      describe('getUser', () => {
        it('returns NotFoundError for missing user', async () => {
          await expect(getUser('nonexistent')).rejects.toThrow(NotFoundError);
        });
      
        it('returns ValidationError for invalid id', async () => {
          await expect(getUser('')).rejects.toThrow(ValidationError);
        });
      
        it('includes error code and message', async () => {
          try {
            await getUser('nonexistent');
          } catch (e) {
            expect(e).toBeInstanceOf(NotFoundError);
            expect(e.code).toBe('NOT_FOUND');
            expect(e.statusCode).toBe(404);
          }
        });
      });
      
      // Test Result types
      describe('getUserResult', () => {
        it('returns ok for existing user', async () => {
          const result = await getUserResult('user-1');
          expect(result.success).toBe(true);
          if (result.success) {
            expect(result.data.id).toBe('user-1');
          }
        });
      
        it('returns err for missing user', async () => {
          const result = await getUserResult('nonexistent');
          expect(result.success).toBe(false);
          if (!result.success) {
            expect(result.error.code).toBe('NOT_FOUND');
          }
        });
      });
      
    ##### **Integration Tests**
      // Test error responses from API
      describe('POST /api/orders', () => {
        it('returns 400 for invalid order', async () => {
          const res = await request(app)
            .post('/api/orders')
            .send({ items: [] });
      
          expect(res.status).toBe(400);
          expect(res.body.code).toBe('VALIDATION_ERROR');
          expect(res.body.fields).toHaveProperty('items');
        });
      
        it('returns 401 for unauthenticated request', async () => {
          const res = await request(app)
            .post('/api/orders')
            .send({ items: [{ id: '1', qty: 1 }] });
      
          expect(res.status).toBe(401);
          expect(res.body.code).toBe('UNAUTHORIZED');
        });
      
        it('returns 404 for nonexistent product', async () => {
          const res = await request(app)
            .post('/api/orders')
            .auth(validToken)
            .send({ items: [{ id: 'nonexistent', qty: 1 }] });
      
          expect(res.status).toBe(404);
        });
      });
      
    ##### **Error Boundary Tests**
      // Test React error boundaries
      import { render, screen } from '@testing-library/react';
      
      // Suppress console.error for expected errors
      const originalError = console.error;
      beforeAll(() => { console.error = jest.fn(); });
      afterAll(() => { console.error = originalError; });
      
      function ThrowingComponent() {
        throw new Error('Test error');
      }
      
      describe('ErrorBoundary', () => {
        it('renders fallback when child throws', () => {
          render(
            <ErrorBoundary fallback={<div>Error occurred</div>}>
              <ThrowingComponent />
            </ErrorBoundary>
          );
      
          expect(screen.getByText('Error occurred')).toBeInTheDocument();
        });
      
        it('calls onError callback', () => {
          const onError = jest.fn();
      
          render(
            <ErrorBoundary onError={onError} fallback={<div>Error</div>}>
              <ThrowingComponent />
            </ErrorBoundary>
          );
      
          expect(onError).toHaveBeenCalledWith(expect.any(Error));
        });
      
        it('renders children when no error', () => {
          render(
            <ErrorBoundary fallback={<div>Error</div>}>
              <div>Normal content</div>
            </ErrorBoundary>
          );
      
          expect(screen.getByText('Normal content')).toBeInTheDocument();
        });
      });
      
    ##### **Retry Tests**
      // Test retry logic
      describe('withRetry', () => {
        it('retries on transient error', async () => {
          let attempts = 0;
          const fn = jest.fn().mockImplementation(() => {
            attempts++;
            if (attempts < 3) throw new Error('Transient');
            return 'success';
          });
      
          const result = await withRetry(fn, { maxAttempts: 3 });
      
          expect(result).toBe('success');
          expect(fn).toHaveBeenCalledTimes(3);
        });
      
        it('throws after max attempts', async () => {
          const fn = jest.fn().mockRejectedValue(new Error('Always fails'));
      
          await expect(withRetry(fn, { maxAttempts: 3 }))
            .rejects.toThrow('Always fails');
          expect(fn).toHaveBeenCalledTimes(3);
        });
      
        it('does not retry permanent errors', async () => {
          const error = Object.assign(new Error('Not found'), { status: 404 });
          const fn = jest.fn().mockRejectedValue(error);
      
          await expect(withRetry(fn)).rejects.toThrow('Not found');
          expect(fn).toHaveBeenCalledTimes(1);
        });
      });
      

## Anti-Patterns

### **Swallowing Errors**
  #### **Description**
Catching and ignoring errors - the silent killer
  #### **Severity**
critical
  #### **Real World Disaster**
    E-commerce checkout: Card charged but order creation silently fails.
    User thinks order placed. You have no logs. Days later, angry refund requests.
    
  #### **Detection**
    ##### **Eslint Rule**
{ "no-empty": ["error", { "allowEmptyCatch": false }] }
    ##### **Code Review**
Search for 'catch' followed by empty braces or only console.log
  #### **Wrong**
    try {
      await processPayment(order);
      await createOrder(order);
    } catch (e) {
      // Silent failure - payment charged, order lost!
    }
    
  #### **Fix Progression**
    ##### **Minimum**
Log the error - at least you'll know it happened
    ##### **Better**
Log + send to error tracking (Sentry, etc.)
    ##### **Best**
Log + track + queue for retry or manual intervention
  #### **Right**
    try {
      await processPayment(order);
      await createOrder(order);
    } catch (error) {
      logger.error({ error, orderId: order.id }, 'Order processing failed');
      captureException(error);
      await queueForManualReview(order);
      throw error; // Let caller know it failed
    }
    
  #### **Decision Matrix**
    ##### **Critical Operations**
Log + Alert + Queue for retry
    ##### **Important Operations**
Log + Queue for retry
    ##### **Nice To Have**
Log warning, continue
    ##### **Never Acceptable**
Empty catch block
### **Generic Catch**
  #### **Description**
Catching all errors identically - hiding bugs in expected errors
  #### **Severity**
high
  #### **Problem**
    All errors return 500. Validation errors (400), auth errors (401), not found (404)
    all look the same. Actual bugs hide among expected failures.
    
  #### **Wrong**
    try {
      await processOrder(order);
    } catch (e) {
      return res.status(500).json({ error: 'Something went wrong' });
    }
    
  #### **Right**
    try {
      await processOrder(order);
    } catch (e) {
      if (e instanceof ValidationError) {
        return res.status(400).json({ code: e.code, message: e.message, fields: e.fields });
      }
      if (e instanceof NotFoundError) {
        return res.status(404).json({ code: e.code, message: e.message });
      }
      if (e instanceof UnauthorizedError) {
        return res.status(401).json({ code: e.code, message: e.message });
      }
      // Unknown = actual bug - log, alert, return generic
      logger.error({ error: e }, 'Unexpected error');
      captureException(e);
      return res.status(500).json({ code: 'INTERNAL_ERROR', message: 'Something went wrong' });
    }
    
  #### **Key Principle**
Expected errors → handle specifically. Unexpected errors → log, alert, hide details.
### **Missing Error Boundaries**
  #### **Description**
React app without error boundaries - one component crash kills everything
  #### **Severity**
high
  #### **Problem**
    One bad API response in ActivityFeed component → entire app white screen.
    User loses all unsaved work. No graceful degradation.
    
  #### **Strategic Placement**
    ##### **Wrap Always**
External API data, user-generated content, third-party components
    ##### **No Boundary Needed**
Simple static UI, trusted internal components
  #### **Wrong**
    export default function App() {
      return (
        <div>
          <Header />
          <UserProfile />   {/* Throws → entire app dies */}
          <ActivityFeed />  {/* External API → risky */}
        </div>
      );
    }
    
  #### **Right**
    export default function App() {
      return (
        <div>
          <Header /> {/* Simple, trusted */}
          <ErrorBoundary fallback={<ProfileSkeleton />}>
            <UserProfile />
          </ErrorBoundary>
          <ErrorBoundary fallback={<FeedSkeleton />}>
            <ActivityFeed />
          </ErrorBoundary>
        </div>
      );
    }
    
### **No Retry Logic**
  #### **Description**
Treating transient failures as permanent - giving up too easily
  #### **Severity**
medium
  #### **Problem**
    Single network hiccup or momentary service restart causes permanent failure.
    API call fails once → user sees error, when retry would have succeeded.
    
  #### **When To Retry**
    ##### **Always**
429, 502, 503, 504, network errors, connection refused
    ##### **Never**
400, 401, 403, 404, 422 - these are permanent, retry won't help
  #### **Wrong**
    const data = await fetch('/api/data').then(r => r.json());
    // One failure = permanent failure
    
  #### **Right**
    const data = await withRetry(
      () => fetch('/api/data').then(r => {
        if (!r.ok) throw Object.assign(new Error(r.statusText), { status: r.status });
        return r.json();
      }),
      {
        maxAttempts: 3,
        baseDelay: 1000,
        shouldRetry: (e) => [429, 502, 503, 504].includes(e.status),
        onRetry: (e, attempt) => console.warn(`Retry ${attempt}:`, e.message),
      }
    );
    