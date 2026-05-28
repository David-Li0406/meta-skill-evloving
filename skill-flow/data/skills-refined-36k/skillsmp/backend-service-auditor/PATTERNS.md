# Common Vulnerability Patterns by Framework

Quick reference for framework-specific vulnerabilities to check during audits.

---

## Node.js / Express / Fastify

### Prototype Pollution
```javascript
// VULNERABLE: Merging user input into objects
Object.assign(config, userInput);
_.merge(settings, req.body);

// SAFE: Validate and whitelist properties
const allowed = ['name', 'email'];
const safe = _.pick(req.body, allowed);
```

### NoSQL Injection (MongoDB)
```javascript
// VULNERABLE: User input in query operators
db.users.find({ password: req.body.password });
// Attack: { "$gt": "" } matches all

// SAFE: Validate types, use $eq explicitly
if (typeof password !== 'string') throw new Error();
db.users.find({ password: { $eq: password } });
```

### Path Traversal
```javascript
// VULNERABLE: Direct file access
const file = path.join(uploadDir, req.params.filename);
res.sendFile(file);
// Attack: ../../etc/passwd

// SAFE: Resolve and validate
const file = path.resolve(uploadDir, req.params.filename);
if (!file.startsWith(path.resolve(uploadDir))) throw new Error();
```

### Event Loop Blocking
```javascript
// VULNERABLE: Sync operations in handlers
app.get('/hash', (req, res) => {
  const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512');
});

// SAFE: Use async versions
app.get('/hash', async (req, res) => {
  const hash = await crypto.pbkdf2(password, salt, 100000, 64, 'sha512');
});
```

---

## Python / FastAPI / Django

### SQL Injection with f-strings
```python
# VULNERABLE: String formatting in queries
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# SAFE: Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Pickle Deserialization
```python
# VULNERABLE: Deserializing untrusted data
import pickle
data = pickle.loads(request.data)  # RCE possible

# SAFE: Use JSON or validate source
import json
data = json.loads(request.data)
```

### SSRF in requests
```python
# VULNERABLE: User-controlled URLs
url = request.form['url']
response = requests.get(url)  # Can hit internal services

# SAFE: Validate URL, use allowlist
from urllib.parse import urlparse
parsed = urlparse(url)
if parsed.netloc not in ALLOWED_HOSTS:
    raise ValueError("Invalid host")
```

### Template Injection (Jinja2)
```python
# VULNERABLE: User input in template
template = Template(user_input)  # SSTI possible

# SAFE: Use sandboxed environment
from jinja2.sandbox import SandboxedEnvironment
env = SandboxedEnvironment()
template = env.from_string(user_input)
```

---

## Go

### SQL Injection
```go
// VULNERABLE: String concatenation
query := "SELECT * FROM users WHERE id = " + userID
db.Query(query)

// SAFE: Prepared statements
db.Query("SELECT * FROM users WHERE id = $1", userID)
```

### Goroutine Leaks
```go
// VULNERABLE: Goroutine never exits
func process() {
    go func() {
        for {
            // No exit condition
        }
    }()
}

// SAFE: Use context for cancellation
func process(ctx context.Context) {
    go func() {
        for {
            select {
            case <-ctx.Done():
                return
            default:
                // work
            }
        }
    }()
}
```

### Missing Error Checks
```go
// VULNERABLE: Ignoring errors
file, _ := os.Open(path)
data, _ := ioutil.ReadAll(file)

// SAFE: Check all errors
file, err := os.Open(path)
if err != nil {
    return nil, fmt.Errorf("open failed: %w", err)
}
defer file.Close()
```

### Race Conditions
```go
// VULNERABLE: Concurrent map access
var cache = make(map[string]string)
func Set(k, v string) { cache[k] = v }  // Race!

// SAFE: Use sync.Map or mutex
var cache sync.Map
func Set(k, v string) { cache.Store(k, v) }
```

---

## Java / Spring

### Deserialization (Jackson)
```java
// VULNERABLE: Polymorphic deserialization
@JsonTypeInfo(use = Id.CLASS)
Object data;  // Allows arbitrary class instantiation

// SAFE: Restrict allowed types
@JsonTypeInfo(use = Id.NAME)
@JsonSubTypes({@Type(SafeClass.class)})
Object data;
```

### SpEL Injection
```java
// VULNERABLE: User input in SpEL
String expr = request.getParameter("filter");
parser.parseExpression(expr).getValue();  // RCE possible

// SAFE: Avoid SpEL with user input, or use SimpleEvaluationContext
SimpleEvaluationContext context = SimpleEvaluationContext.forReadOnlyDataBinding().build();
```

### Path Traversal
```java
// VULNERABLE: Direct path concatenation
File file = new File(baseDir + "/" + fileName);

// SAFE: Validate canonical path
File file = new File(baseDir, fileName);
if (!file.getCanonicalPath().startsWith(baseDir.getCanonicalPath())) {
    throw new SecurityException("Path traversal attempt");
}
```

### Transaction Propagation
```java
// VULNERABLE: Wrong propagation in nested call
@Transactional
public void outer() {
    inner();  // Runs in same transaction
}

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void inner() {
    // This won't start new transaction when called from same class!
}

// SAFE: Use separate bean or self-injection
```

---

## Common Cross-Framework Issues

### JWT Vulnerabilities
```
1. Algorithm confusion: Accept "none" or switch RS256→HS256
2. Missing expiration: Tokens valid forever
3. Weak secrets: Brute-forceable HMAC keys
4. Missing audience/issuer validation
5. Storing sensitive data in payload (readable by client)
```

### API Rate Limiting Bypass
```
1. Missing per-user limits (only global)
2. Bypassable via headers (X-Forwarded-For)
3. Different limits on authenticated vs anonymous
4. No limit on expensive operations (search, export)
```

### Authentication Bypass Patterns
```
1. Case sensitivity: Admin vs admin
2. Unicode normalization: 'ᴬdmin' normalized to 'Admin'
3. Null byte injection: admin%00.jpg
4. Type confusion: id=1 vs id[]=1
5. Mass assignment: {role: "admin"} in signup
```

### Timing Attacks
```python
# VULNERABLE: Early return reveals valid usernames
if not user_exists(username):
    return "Invalid credentials"  # Fast
if not verify_password(password, user.password):
    return "Invalid credentials"  # Slow

# SAFE: Constant-time comparison
if not user_exists(username):
    verify_password(password, DUMMY_HASH)  # Same timing
    return "Invalid credentials"
```

---

## Audit Commands by Stack

### Node.js
```bash
npm audit                          # Check vulnerabilities
npx depcheck                       # Find unused dependencies
grep -r "eval\|Function(" src/     # Find dangerous evals
grep -r "\.exec\|child_process" src/  # Find command execution
```

### Python
```bash
pip-audit                          # Check vulnerabilities
bandit -r src/                     # Security linter
safety check                       # Check requirements.txt
grep -r "pickle\|eval\|exec" src/  # Dangerous functions
```

### Go
```bash
go list -m all | nancy sleuth      # Check vulnerabilities
gosec ./...                        # Security linter
go vet ./...                       # Find common issues
go build -race ./...               # Race detector
```

### Java
```bash
./mvnw dependency-check:check      # OWASP dependency check
./mvnw spotbugs:check              # Bug finder
grep -r "Runtime.exec" src/        # Command execution
```
