# Attack Pattern Library

Common attack patterns with detection methods and mitigations.

---

## Authentication Attacks

### Credential Stuffing

**Description:** Automated login attempts using leaked credentials from other breaches.

**Attack Flow:**
1. Attacker obtains credential dump from breach
2. Automates login attempts against target
3. Successful logins from reused passwords

**Detection:**
- High volume of failed logins
- Login attempts from unusual IPs/geos
- Multiple accounts from same IP

**Mitigations:**
```typescript
// Rate limiting by IP and account
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  keyGenerator: (req) => `${req.ip}:${req.body.email}`,
});

// Account lockout after failures
async function handleLogin(email: string, password: string) {
  const failedAttempts = await getFailedAttempts(email);
  if (failedAttempts > 5) {
    throw new Error('Account locked. Reset password to continue.');
  }
  // ... login logic
}

// Require MFA for new device/location
if (isNewDevice || isUnusualLocation) {
  return requireMFA(user);
}
```

---

### Session Hijacking

**Description:** Stealing or predicting session tokens to impersonate users.

**Attack Flow:**
1. Attacker intercepts session token (XSS, network sniffing, malware)
2. Uses token to authenticate as victim
3. Performs actions as victim

**Detection:**
- Session used from different IP/device
- Concurrent sessions from different locations
- Session used after logout

**Mitigations:**
```typescript
// Bind session to client fingerprint
const sessionData = {
  userId,
  ip: req.ip,
  userAgent: req.headers['user-agent'],
  createdAt: Date.now(),
};

// Validate on each request
function validateSession(session: Session, req: Request) {
  if (session.ip !== req.ip) {
    // Suspicious - require re-auth
    return false;
  }
  if (Date.now() - session.createdAt > SESSION_TTL) {
    return false;
  }
  return true;
}

// Use httpOnly, secure cookies
res.cookie('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 3600000,
});
```

---

### JWT Attacks

**Description:** Exploiting JWT implementation flaws.

**Attack Vectors:**
- Algorithm confusion (none, HS256→RS256)
- Weak secret brute-forcing
- Token not validated properly

**Mitigations:**
```typescript
// Explicitly specify algorithm
const payload = jwt.verify(token, secret, {
  algorithms: ['HS256'],  // Never allow 'none'
  issuer: 'my-app',
  audience: 'my-app-users',
});

// Use strong secrets
const secret = crypto.randomBytes(64).toString('hex');
// NOT: const secret = 'my-secret';

// Validate all claims
if (payload.exp < Date.now() / 1000) {
  throw new Error('Token expired');
}
if (payload.iss !== 'my-app') {
  throw new Error('Invalid issuer');
}
```

---

## Injection Attacks

### SQL Injection

**Description:** Injecting SQL commands through user input.

**Attack Flow:**
1. Attacker identifies input that reaches SQL query
2. Crafts payload: `' OR '1'='1' --`
3. Query logic altered, data exposed or modified

**Mitigations:**
```typescript
// VULNERABLE
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// SAFE: Parameterized query
const result = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// SAFE: ORM with parameters
const user = await User.findOne({
  where: { id: userId }  // ORM handles escaping
});

// Input validation
const userIdSchema = z.string().uuid();
const validatedId = userIdSchema.parse(userId);
```

---

### Command Injection

**Description:** Injecting OS commands through user input.

**Attack Flow:**
1. Attacker finds input passed to shell
2. Injects command: `; rm -rf / ;`
3. Arbitrary commands executed on server

**Mitigations:**
```typescript
// VULNERABLE
exec(`convert ${filename} output.png`);

// SAFE: Use arrays, not shell strings
execFile('convert', [filename, 'output.png']);

// SAFE: Validate input strictly
const filenameSchema = z.string().regex(/^[a-zA-Z0-9_-]+\.(jpg|png)$/);
const validFilename = filenameSchema.parse(filename);

// BEST: Avoid shell entirely
import sharp from 'sharp';
await sharp(filename).png().toFile('output.png');
```

---

### XSS (Cross-Site Scripting)

**Description:** Injecting JavaScript that runs in other users' browsers.

**Attack Vectors:**
- Reflected: `?q=<script>alert(1)</script>`
- Stored: Comment contains `<script>...</script>`
- DOM-based: Client-side rendering of untrusted data

**Mitigations:**
```typescript
// React: Default escaping (safe)
return <div>{userInput}</div>;  // Auto-escaped

// React: Dangerous - only with sanitization
import DOMPurify from 'dompurify';
return <div dangerouslySetInnerHTML={{
  __html: DOMPurify.sanitize(userInput)
}} />;

// Server: Set CSP header
res.setHeader('Content-Security-Policy',
  "default-src 'self'; script-src 'self'"
);

// Server: Escape in templates
const escaped = html`<div>${escapeHtml(userInput)}</div>`;
```

---

## Authorization Attacks

### IDOR (Insecure Direct Object Reference)

**Description:** Accessing objects by manipulating IDs without authorization check.

**Attack Flow:**
1. User sees `/api/orders/123`
2. Changes to `/api/orders/124` (another user's order)
3. Accesses unauthorized data

**Mitigations:**
```typescript
// VULNERABLE
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  return res.json(order);  // No auth check!
});

// SAFE: Check ownership
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);

  if (!order) {
    return res.status(404).json({ error: 'Not found' });
  }

  if (order.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  return res.json(order);
});

// BETTER: Query by user
const order = await Order.findOne({
  where: { id: req.params.id, userId: req.user.id }
});
```

---

### Privilege Escalation

**Description:** Gaining higher privileges than authorized.

**Attack Vectors:**
- Mass assignment: `{ role: 'admin' }` in request
- Role parameter in URL
- JWT role claim tampering

**Mitigations:**
```typescript
// VULNERABLE: Mass assignment
const user = await User.update(req.body);  // Attacker sends { role: 'admin' }

// SAFE: Whitelist fields
const allowedFields = ['name', 'email', 'avatar'];
const updates = pick(req.body, allowedFields);
const user = await User.update(updates);

// SAFE: Role changes require admin
app.put('/api/users/:id/role', requireAdmin, async (req, res) => {
  // Only admins can change roles
  await User.update({ role: req.body.role });
});

// SAFE: Validate role from server, not client
const userRole = await getUserRole(req.user.id);  // From DB, not JWT
```

---

## API Attacks

### Rate Limit Bypass

**Description:** Circumventing rate limits to abuse APIs.

**Attack Vectors:**
- IP rotation
- Header manipulation (X-Forwarded-For)
- Different user agents
- Case variations in endpoint

**Mitigations:**
```typescript
// Layer rate limits
const globalLimiter = rateLimit({ windowMs: 60000, max: 1000 });
const userLimiter = rateLimit({
  windowMs: 60000,
  max: 100,
  keyGenerator: (req) => req.user?.id || req.ip,
});
const endpointLimiter = rateLimit({
  windowMs: 60000,
  max: 10,
  keyGenerator: (req) => `${req.user?.id}:${req.path}`,
});

// Don't trust X-Forwarded-For blindly
const getClientIp = (req) => {
  // Only trust XFF from known proxies
  if (TRUSTED_PROXIES.includes(req.socket.remoteAddress)) {
    return req.headers['x-forwarded-for']?.split(',')[0];
  }
  return req.socket.remoteAddress;
};

// Normalize endpoints before limiting
app.use((req, res, next) => {
  req.url = req.url.toLowerCase();
  next();
});
```

---

### API Parameter Tampering

**Description:** Modifying API parameters to bypass business logic.

**Attack Vectors:**
- Negative quantities
- Price manipulation
- Hidden admin parameters
- Type coercion

**Mitigations:**
```typescript
// Comprehensive validation with Zod
const orderSchema = z.object({
  productId: z.string().uuid(),
  quantity: z.number().int().positive().max(100),
  // Don't accept price from client!
});

// Calculate price server-side
async function createOrder(input: OrderInput) {
  const validated = orderSchema.parse(input);
  const product = await Product.findById(validated.productId);

  // Server-side price calculation
  const price = product.price * validated.quantity;

  return Order.create({
    ...validated,
    price,  // Never from client
    userId: currentUser.id,  // Never from client
  });
}
```

---

## Smart Contract Attacks

### Reentrancy

**Description:** Calling back into contract before state is updated.

**Attack Flow:**
1. Attacker contract calls `withdraw()`
2. Before balance updated, `withdraw()` sends ETH
3. Attacker's `receive()` calls `withdraw()` again
4. Repeat until drained

**Mitigations:**
```solidity
// VULNERABLE
function withdraw() public {
    uint256 amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0;  // Too late!
}

// SAFE: Checks-Effects-Interactions pattern
function withdraw() public {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;  // Update state first
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}

// SAFER: ReentrancyGuard
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

function withdraw() public nonReentrant {
    // ...
}
```

---

### Flash Loan Attack

**Description:** Using uncollateralized loans to manipulate prices or exploit logic.

**Attack Flow:**
1. Borrow large amount via flash loan
2. Manipulate price oracle or pool
3. Exploit protocol at manipulated price
4. Repay loan, keep profit

**Mitigations:**
```solidity
// Use time-weighted average prices (TWAP)
function getPrice() public view returns (uint256) {
    // Chainlink oracle (harder to manipulate)
    (, int256 price, , , ) = priceFeed.latestRoundData();
    return uint256(price);
}

// Add delay for large operations
function withdraw(uint256 amount) public {
    if (amount > LARGE_AMOUNT) {
        require(
            block.timestamp > lastDeposit[msg.sender] + 1 days,
            "Wait period required for large withdrawals"
        );
    }
}

// Check for flash loan context
require(
    msg.sender == tx.origin || isWhitelistedContract(msg.sender),
    "Flash loan protection"
);
```

---

### Price Oracle Manipulation

**Description:** Manipulating price feeds to exploit protocol logic.

**Attack Vectors:**
- DEX spot price manipulation
- Low-liquidity oracle exploitation
- Stale price exploitation

**Mitigations:**
```solidity
// Use multiple oracle sources
function getPrice() public view returns (uint256) {
    uint256 chainlinkPrice = getChainlinkPrice();
    uint256 uniswapTwapPrice = getUniswapTwapPrice();

    // Require prices within tolerance
    uint256 diff = chainlinkPrice > uniswapTwapPrice
        ? chainlinkPrice - uniswapTwapPrice
        : uniswapTwapPrice - chainlinkPrice;
    require(diff * 100 / chainlinkPrice < 5, "Price deviation too high");

    return (chainlinkPrice + uniswapTwapPrice) / 2;
}

// Check freshness
function getChainlinkPrice() internal view returns (uint256) {
    (, int256 price, , uint256 updatedAt, ) = priceFeed.latestRoundData();
    require(block.timestamp - updatedAt < 1 hours, "Stale price");
    return uint256(price);
}
```

---

## Quick Reference: Attack → Mitigation

| Attack | Primary Mitigation | Code Pattern |
|--------|-------------------|--------------|
| SQL Injection | Parameterized queries | `db.query('...', [param])` |
| XSS | Output encoding, CSP | `escapeHtml()`, CSP header |
| CSRF | CSRF tokens | `csrf.verify(token)` |
| IDOR | Authorization check | `if (obj.userId !== user.id)` |
| Credential Stuffing | Rate limiting, MFA | `rateLimit()`, `requireMFA()` |
| Session Hijacking | Secure cookies, binding | `httpOnly, secure, sameSite` |
| Command Injection | Avoid shell, validate | `execFile()`, whitelist |
| Path Traversal | Canonicalize, whitelist | `path.resolve()`, check prefix |
| Reentrancy | CEI pattern, guards | Update state before call |
| Flash Loan | TWAP, delays | Time-weighted prices |
