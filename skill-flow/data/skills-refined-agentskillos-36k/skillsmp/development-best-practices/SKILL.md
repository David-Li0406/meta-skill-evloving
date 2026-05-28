---
name: development-best-practices
description: Core development principles including anti-hallucination, anti-hardcoding, error handling, logging, testing, and security standards. Use during feature design, implementation, and code review to ensure code quality and maintainability. Applies universally to all code regardless of technology or feature.
---

# Development Best Practices

Universal coding standards and anti-patterns that apply to ALL code regardless of feature or technology.

## Quick Start

**Validate feature design:**
```
"Check feature-5.1 design against development-best-practices"
```

**Validate implementation:**
```
"Verify src/services/ follows development-best-practices"
```

**Check code before commit:**
```
"Review my changes against development-best-practices before committing"
```

## Core Workflow

### Step 1: Anti-Hallucination Validation

**Purpose**: Prevent AI agents from inventing code, APIs, or file structures that don't exist

**Validation Checks**:

1. **File Existence Before Reading**
   ```python
   # ❌ BAD: Assume file exists
   with open('config.yaml') as f:
       config = yaml.load(f)

   # ✅ GOOD: Check existence first
   if os.path.exists('config.yaml'):
       with open('config.yaml') as f:
           config = yaml.load(f)
   else:
       raise FileNotFoundError("config.yaml not found")
   ```

2. **API Response Validation**
   ```typescript
   // ❌ BAD: Assume response structure
   const user = await api.getUser(userId);
   console.log(user.email);

   // ✅ GOOD: Validate response structure
   const user = await api.getUser(userId);
   if (!user || !user.email) {
       throw new Error("Invalid user response");
   }
   console.log(user.email);
   ```

3. **Test Assumptions with Actual Data**
   ```typescript
   // ❌ BAD: Assume API returns array
   const items = await api.getItems();
   items.forEach(item => console.log(item));

   // ✅ GOOD: Verify it's an array
   const items = await api.getItems();
   if (!Array.isArray(items)) {
       throw new Error("Expected array, got " + typeof items);
   }
   items.forEach(item => console.log(item));
   ```

4. **Read Actual Code, Don't Invent Signatures**
   ```typescript
   // ❌ BAD: Guess function signature
   // Assume: calculateTotal(items, tax, discount)
   const total = calculateTotal(cartItems, 0.08, 10);

   // ✅ GOOD: Read actual function signature first
   // After reading code: calculateTotal(items: Item[]): number
   // Tax/discount handled internally via config
   const total = calculateTotal(cartItems);
   ```

5. **Validate Configuration Values Exist**
   ```typescript
   // ❌ BAD: Assume env var exists
   const apiUrl = process.env.API_URL;
   fetch(apiUrl + '/users');

   // ✅ GOOD: Validate env var exists
   const apiUrl = process.env.API_URL;
   if (!apiUrl) {
       throw new Error("API_URL environment variable not set");
   }
   fetch(apiUrl + '/users');
   ```

**Checklist**:
- [ ] Verified file existence before reading/writing
- [ ] Validated API response structure before accessing
- [ ] Tested assumptions with console.log or debugger
- [ ] Read actual function signatures from source code
- [ ] Checked configuration values exist before using
- [ ] No invented APIs, methods, or properties

---

### Step 2: Anti-Hardcoding Validation

**Purpose**: Ensure all environment-specific values are externalized

**Validation Checks**:

1. **No Hardcoded URLs**
   ```typescript
   // ❌ BAD: Hardcoded URL
   const API_URL = 'https://api.prod.company.com';

   // ✅ GOOD: Environment variable
   const API_URL = process.env.API_URL || 'http://localhost:3000';
   ```

2. **No Hardcoded Credentials**
   ```typescript
   // ❌ BAD: Hardcoded API key
   const apiKey = 'sk_live_abc123xyz789';

   // ✅ GOOD: Environment variable
   const apiKey = process.env.API_KEY;
   if (!apiKey) throw new Error("API_KEY not configured");
   ```

3. **Extract Magic Numbers to Constants**
   ```typescript
   // ❌ BAD: Magic numbers
   if (user.age >= 18 && cartTotal > 100) {
       applyDiscount(cartTotal * 0.1);
   }

   // ✅ GOOD: Named constants
   const MINIMUM_AGE = 18;
   const DISCOUNT_THRESHOLD = 100;
   const DISCOUNT_RATE = 0.1;

   if (user.age >= MINIMUM_AGE && cartTotal > DISCOUNT_THRESHOLD) {
       applyDiscount(cartTotal * DISCOUNT_RATE);
   }
   ```

4. **Use Feature Flags for Toggles**
   ```typescript
   // ❌ BAD: Hardcoded feature toggle
   const enableNewCheckout = true;

   // ✅ GOOD: Configuration-based feature flag
   const enableNewCheckout = config.get('features.newCheckout', false);
   ```

5. **No Environment-Specific Logic in Code**
   ```typescript
   // ❌ BAD: Environment checks in code
   if (process.env.NODE_ENV === 'production') {
       // Use production logic
   } else {
       // Use dev logic
   }

   // ✅ GOOD: Configuration-driven
   const useCache = config.get('cache.enabled');
   if (useCache) {
       // Use cache
   }
   ```

**Checklist**:
- [ ] No hardcoded URLs, endpoints, or service addresses
- [ ] No hardcoded API keys, tokens, or credentials
- [ ] No magic numbers (extracted to named constants)
- [ ] No hardcoded database connection strings
- [ ] No environment-specific logic in code (use config)
- [ ] Feature flags in configuration, not code

---

### Step 3: Error Handling Validation

**Purpose**: Ensure all risky operations have proper error handling

**Validation Checks**:

1. **Wrap Risky Operations in Try-Catch**
   ```typescript
   // ❌ BAD: No error handling
   const data = JSON.parse(jsonString);
   const result = await api.fetchData();

   // ✅ GOOD: Try-catch around risky operations
   let data;
   try {
       data = JSON.parse(jsonString);
   } catch (error) {
       console.error("Failed to parse JSON", error);
       throw new Error("Invalid JSON format");
   }

   let result;
   try {
       result = await api.fetchData();
   } catch (error) {
       console.error("API call failed", error);
       throw new Error("Failed to fetch data from API");
   }
   ```

2. **Propagate Errors Correctly**
   ```typescript
   // ❌ BAD: Swallow errors
   async function loadUser(userId: string) {
       try {
           return await api.getUser(userId);
       } catch (error) {
           console.error(error);
           return null; // Error swallowed
       }
   }

   // ✅ GOOD: Re-throw or return error
   async function loadUser(userId: string): Promise<User> {
       try {
           return await api.getUser(userId);
       } catch (error) {
           console.error("Failed to load user", userId, error);
           throw new Error(`User ${userId} not found`);
       }
   }
   ```

3. **User-Friendly Error Messages**
   ```typescript
   // ❌ BAD: Technical error to user
   catch (error) {
       alert(error.stack);
   }

   // ✅ GOOD: User-friendly message
   catch (error) {
       console.error("Technical error:", error);
       showNotification("Unable to load data. Please try again later.", "error");
   }
   ```

4. **Log Errors Appropriately**
   ```typescript
   // ❌ BAD: No logging
   catch (error) {
       throw error;
   }

   // ✅ GOOD: Log before re-throwing
   catch (error) {
       logger.error("Failed to process payment", {
           userId: user.id,
           amount: amount,
           error: error.message,
           stack: error.stack
       });
       throw new Error("Payment processing failed");
   }
   ```

5. **Cleanup with Finally Blocks**
   ```typescript
   // ❌ BAD: Resources not cleaned up
   const connection = await db.connect();
   await connection.query(sql);
   await connection.close();

   // ✅ GOOD: Finally block ensures cleanup
   const connection = await db.connect();
   try {
       await connection.query(sql);
   } finally {
       await connection.close();
   }
   ```

**Checklist**:
- [ ] All risky operations wrapped in try-catch
- [ ] Errors logged with context (user ID, action, etc.)
- [ ] Errors propagated or handled appropriately (not swallowed)
- [ ] User-friendly error messages (no stack traces to users)
- [ ] Cleanup code in finally blocks (close connections, files)
- [ ] Specific error types thrown (not generic Error)

---

### Step 4: Logging Validation

**Purpose**: Ensure consistent, structured logging throughout application

**Validation Checks**:

1. **Use Structured Logging (JSON Format)**
   ```typescript
   // ❌ BAD: String concatenation
   console.log("User " + userId + " logged in at " + new Date());

   // ✅ GOOD: Structured logging
   logger.info("User logged in", {
       userId: userId,
       timestamp: new Date().toISOString(),
       ipAddress: req.ip
   });
   ```

2. **No Sensitive Data in Logs**
   ```typescript
   // ❌ BAD: Logging sensitive data
   logger.info("User authenticated", {
       userId: user.id,
       password: user.password,  // 🚨 Never log passwords
       ssn: user.ssn             // 🚨 Never log PII
   });

   // ✅ GOOD: Redact sensitive data
   logger.info("User authenticated", {
       userId: user.id,
       email: maskEmail(user.email)  // user@example.com → u***@example.com
   });
   ```

3. **Appropriate Log Levels**
   ```typescript
   // ❌ BAD: Everything at INFO level
   logger.info("Starting application");
   logger.info("User not found");  // Should be WARN
   logger.info("Database connection failed");  // Should be ERROR
   logger.info("Query took 5ms");  // Should be DEBUG

   // ✅ GOOD: Proper log levels
   logger.info("Starting application");
   logger.warn("User not found", { userId });
   logger.error("Database connection failed", { error });
   logger.debug("Query executed", { duration: 5, query });
   ```

4. **Correlation IDs for Tracing**
   ```typescript
   // ❌ BAD: No request correlation
   logger.info("Processing payment");
   logger.info("Payment successful");

   // ✅ GOOD: Include correlation ID
   const correlationId = req.headers['x-correlation-id'] || uuidv4();
   logger.info("Processing payment", { correlationId, userId, amount });
   logger.info("Payment successful", { correlationId, transactionId });
   ```

5. **Performance Logging for Slow Operations**
   ```typescript
   // ❌ BAD: No performance tracking
   const result = await expensiveOperation();

   // ✅ GOOD: Log slow operations
   const start = Date.now();
   const result = await expensiveOperation();
   const duration = Date.now() - start;

   if (duration > 1000) {
       logger.warn("Slow operation detected", {
           operation: "expensiveOperation",
           duration,
           threshold: 1000
       });
   }
   ```

**Checklist**:
- [ ] Structured logging (JSON format, not string concat)
- [ ] No sensitive data in logs (passwords, tokens, PII)
- [ ] Appropriate log levels (ERROR, WARN, INFO, DEBUG)
- [ ] Correlation IDs included for request tracing
- [ ] Performance logging for operations >1s
- [ ] Contextual information (user ID, action, resource)

---

### Step 5: Testing Validation

**Purpose**: Ensure adequate test coverage and quality

**Validation Checks**:

1. **Unit Tests for Business Logic**
   ```typescript
   // ❌ BAD: No tests
   export function calculateDiscount(price: number, discountPercent: number) {
       return price * (discountPercent / 100);
   }

   // ✅ GOOD: Unit tests cover logic
   describe('calculateDiscount', () => {
       it('should calculate 10% discount correctly', () => {
           expect(calculateDiscount(100, 10)).toBe(10);
       });

       it('should handle 0% discount', () => {
           expect(calculateDiscount(100, 0)).toBe(0);
       });

       it('should handle 100% discount', () => {
           expect(calculateDiscount(100, 100)).toBe(100);
       });
   });
   ```

2. **Integration Tests for Service Interactions**
   ```typescript
   // ❌ BAD: Only unit tests, no integration tests

   // ✅ GOOD: Integration test for API interaction
   describe('UserService', () => {
       it('should fetch user from API', async () => {
           const userService = new UserService(mockApiClient);
           const user = await userService.getUser('user123');

           expect(user).toBeDefined();
           expect(user.id).toBe('user123');
           expect(mockApiClient.get).toHaveBeenCalledWith('/users/user123');
       });
   });
   ```

3. **Test Coverage Meets Threshold (>80%)**
   ```bash
   # Run test coverage
   npm run test:coverage

   # Ensure meets threshold
   # Lines: 85% (target: 80%)
   # Branches: 82% (target: 80%)
   # Functions: 90% (target: 80%)
   ```

4. **Edge Cases Covered**
   ```typescript
   // ❌ BAD: Only happy path tested
   it('should process valid input', () => {
       expect(processInput('valid')).toBe('processed');
   });

   // ✅ GOOD: Edge cases tested
   describe('processInput', () => {
       it('should process valid input', () => {
           expect(processInput('valid')).toBe('processed');
       });

       it('should handle empty string', () => {
           expect(() => processInput('')).toThrow('Input cannot be empty');
       });

       it('should handle null', () => {
           expect(() => processInput(null)).toThrow('Input cannot be null');
       });

       it('should handle very long input', () => {
           const longInput = 'a'.repeat(10000);
           expect(() => processInput(longInput)).toThrow('Input too long');
       });
   });
   ```

5. **Mocking Used Appropriately**
   ```typescript
   // ❌ BAD: Real API calls in tests
   it('should create user', async () => {
       const result = await realApi.createUser(userData);  // 🚨 Real API call
       expect(result.success).toBe(true);
   });

   // ✅ GOOD: Mock API calls
   it('should create user', async () => {
       const mockApi = {
           createUser: jest.fn().mockResolvedValue({ success: true, id: '123' })
       };
       const service = new UserService(mockApi);
       const result = await service.createUser(userData);

       expect(result.success).toBe(true);
       expect(mockApi.createUser).toHaveBeenCalledWith(userData);
   });
   ```

**Checklist**:
- [ ] Unit tests for all business logic functions
- [ ] Integration tests for service interactions
- [ ] Test coverage >80% (lines, branches, functions)
- [ ] Edge cases covered (null, empty, invalid, boundary)
- [ ] Mocking used for external dependencies
- [ ] Tests run in CI/CD pipeline

---

### Step 6: Security Validation

**Purpose**: Ensure security best practices followed

**Validation Checks**:

1. **Input Validation on All User Inputs**
   ```typescript
   // ❌ BAD: No input validation
   app.post('/users', async (req, res) => {
       const user = await db.createUser(req.body);
       res.json(user);
   });

   // ✅ GOOD: Validate input
   app.post('/users', async (req, res) => {
       const schema = z.object({
           email: z.string().email(),
           age: z.number().min(0).max(150),
           name: z.string().min(1).max(100)
       });

       const validated = schema.parse(req.body);
       const user = await db.createUser(validated);
       res.json(user);
   });
   ```

2. **Authentication Checks on Protected Operations**
   ```typescript
   // ❌ BAD: No auth check
   app.get('/admin/users', async (req, res) => {
       const users = await db.getAllUsers();
       res.json(users);
   });

   // ✅ GOOD: Require authentication
   app.get('/admin/users', requireAuth, async (req, res) => {
       const users = await db.getAllUsers();
       res.json(users);
   });
   ```

3. **Authorization/RBAC Enforced**
   ```typescript
   // ❌ BAD: No permission check
   app.delete('/users/:id', requireAuth, async (req, res) => {
       await db.deleteUser(req.params.id);
       res.json({ success: true });
   });

   // ✅ GOOD: Check permissions
   app.delete('/users/:id', requireAuth, requireRole('admin'), async (req, res) => {
       await db.deleteUser(req.params.id);
       res.json({ success: true });
   });
   ```

4. **SQL Injection Prevention (Parameterized Queries)**
   ```typescript
   // ❌ BAD: String concatenation (SQL injection)
   const query = `SELECT * FROM users WHERE email = '${email}'`;
   const users = await db.query(query);

   // ✅ GOOD: Parameterized query
   const query = `SELECT * FROM users WHERE email = ?`;
   const users = await db.query(query, [email]);
   ```

5. **XSS Prevention (Output Encoding)**
   ```typescript
   // ❌ BAD: Unescaped user input
   res.send(`<h1>Welcome ${req.query.name}</h1>`);

   // ✅ GOOD: Escape user input
   const escape = require('escape-html');
   res.send(`<h1>Welcome ${escape(req.query.name)}</h1>`);
   ```

**Checklist**:
- [ ] Input validation on all user inputs (schema validation)
- [ ] Authentication required for protected endpoints
- [ ] Authorization/RBAC checks enforced
- [ ] Parameterized queries (no SQL injection)
- [ ] Output encoding (no XSS vulnerabilities)
- [ ] HTTPS enforced (no sensitive data over HTTP)
- [ ] CSRF protection enabled
- [ ] Rate limiting on public endpoints

---

## Available Resources

### Scripts

- **scripts/validate_no_hardcoded_values.py** — Scan for hardcoded URLs, keys, magic numbers
  ```bash
  python scripts/validate_no_hardcoded_values.py --path src/ --report hardcoding-report.json
  ```

- **scripts/check_error_handling.py** — Verify try-catch coverage for risky operations
  ```bash
  python scripts/check_error_handling.py --path src/ --threshold 90
  ```

- **scripts/verify_configuration.py** — Ensure all config externalized
  ```bash
  python scripts/verify_configuration.py --path src/ --config-file .env.example
  ```

- **scripts/check_logging_practices.py** — Validate logging standards
  ```bash
  python scripts/check_logging_practices.py --path src/ --check-sensitive-data
  ```

- **scripts/calculate_test_coverage.py** — Check test coverage meets threshold
  ```bash
  python scripts/calculate_test_coverage.py --threshold 80 --report coverage-report.json
  ```

### References

- **references/anti-hallucination-checklist.md** — Specific checks to prevent AI hallucination
- **references/configuration-patterns.md** — How to externalize configuration properly
- **references/error-handling-patterns.md** — Standard error handling approaches
- **references/logging-standards.md** — Structured logging formats and standards
- **references/testing-requirements.md** — Unit/integration test requirements
- **references/security-checklist.md** — Security validation checklist

---

## Integration with Workflow

### During Feature Design (`/design-features`)

Before designing features:
- Review anti-hallucination checklist
- Plan configuration externalization
- Design error handling strategy
- Plan logging approach
- Define test strategy
- Identify security requirements

### During Wave Design (`/design-waves`)

Before designing waves:
- Validate wave follows best practices
- Check for hardcoding opportunities
- Plan error handling for wave
- Define tests needed for wave

### During Implementation (`/implement-waves`)

Before implementing:
- Invoke `development-best-practices` skill
- Review relevant checklist sections
- Run validation scripts during implementation
- Test against best practices before commit

### During Code Review

Before merging:
- Run all validation scripts
- Review against best practices checklist
- Verify test coverage meets threshold
- Check security checklist

---

## Success Criteria

- ✅ No hallucinated code (all APIs/files verified to exist)
- ✅ No hardcoded values (URLs, credentials, magic numbers)
- ✅ All risky operations have error handling
- ✅ Structured logging with appropriate levels
- ✅ Test coverage >80%
- ✅ Security checklist items addressed

---

## Tips for Effective Practice

1. **Invoke early and often** - Use skill before design, during implementation, before commit
2. **Run validation scripts** - Catch violations automatically
3. **Review checklists** - Systematic approach beats ad-hoc checks
4. **Learn from violations** - Understand why rules exist
5. **Automate enforcement** - Use pre-commit hooks, CI/CD checks
6. **Update skill** - Add patterns as you discover them
7. **Share violations** - Help team learn from mistakes

---

**Last Updated**: 2025-01-30
