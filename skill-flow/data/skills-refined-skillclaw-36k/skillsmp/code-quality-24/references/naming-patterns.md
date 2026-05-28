# Naming Patterns Reference

## Core Principle

Names must communicate three things:
1. **Who is acting** — The subject
2. **What action is occurring** — The verb
3. **Direction of data flow** — Where things go to/from

---

## Directional Naming Patterns

### Pattern 1: `verb_noun_to(target)`

Action flows **to** a target.

```python
send_message_to(user)
export_data_to(file)
copy_selection_to(clipboard)
dispatch_event_to(handler)
```

### Pattern 2: `verb_noun_from(source)`

Action flows **from** a source.

```python
receive_payment_from(customer)
import_data_from(file)
fetch_config_from(server)
read_bytes_from(stream)
```

### Pattern 3: `noun.verb_to(target)`

Object performs action toward target.

```python
cart.transfer_to(order)
user.send_notification_to(device)
document.export_to(pdf)
account.transfer_funds_to(recipient)
```

### Pattern 4: `verb(noun, to=target)`

Named parameter clarifies direction.

```python
assign(task, to=developer)
move(file, to=directory)
copy(data, from=source, to=destination)
send(email, to=recipients, cc=managers)
```

---

## The Read-Aloud Test

If you can't read the code naturally as a sentence, rename it.

| Code | Read Aloud | Verdict |
|------|------------|---------|
| `shop.buy_item(item, buyer)` | "shop buy item buyer" | ❌ Confusing |
| `shop.sell_item_to(item, buyer)` | "shop sell item to buyer" | ✅ Clear |
| `transfer(100, account)` | "transfer 100 account" | ❌ Direction unclear |
| `account.withdraw(100)` | "account withdraw 100" | ✅ Clear |
| `database.query(sql)` | "database query sql" | ✅ Clear |

---

## File Naming Conventions

### By Type

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `Button.tsx`, `UserProfile.tsx` |
| Pages | PascalCase | `Dashboard.tsx`, `Settings.tsx` |
| Services | PascalCase + Service | `AuthService.ts`, `EmailService.ts` |
| Repositories | PascalCase + Repository | `UserRepository.ts` |
| Use Cases | camelCase, verb-first | `registerUser.ts`, `createOrder.ts` |
| Utilities | camelCase | `formatDate.ts`, `parseUrl.ts` |
| Types/Interfaces | PascalCase | `User.ts`, `OrderItem.ts` |
| Tests | Source + `.test` | `Button.test.tsx` |
| Styles | kebab-case | `button.css`, `user-profile.css` |
| Config | camelCase | `database.ts`, `redis.ts` |
| Constants | UPPER_SNAKE_CASE (file) | `API_ENDPOINTS.ts` |

### By Layer

| Layer | Naming Pattern | Examples |
|-------|----------------|----------|
| 01-presentation | Component/Page names | `ProductCard.tsx`, `Checkout.tsx` |
| 02-logic | Service/UseCase names | `PaymentService.ts`, `processOrder.ts` |
| 03-data | Repository/Model names | `OrderRepository.ts`, `User.ts` |

---

## Variable Naming

### Booleans

Prefix with `is`, `has`, `should`, `can`, `will`:

```typescript
// Good
const isActive = true;
const hasPermission = user.roles.includes('admin');
const shouldRefresh = lastUpdate < threshold;
const canEdit = isOwner || isAdmin;

// Bad
const active = true;        // Is this a state or an action?
const permission = true;    // What about permission?
const refresh = true;       // Is this a flag or a function?
```

### Collections

Use plural nouns:

```typescript
// Good
const users = [];
const orderItems = [];
const selectedIds = new Set();

// Bad
const userList = [];        // Redundant "List"
const orderItemArray = [];  // Redundant "Array"
const selectedIdSet = [];   // Redundant "Set"
```

### Functions

Use verb-first:

```typescript
// Good
function calculateTotal() {}
function fetchUserData() {}
function validateInput() {}
function handleSubmit() {}

// Bad
function total() {}         // Is this a value or action?
function userData() {}      // Noun, not verb
function inputValidation() {} // Noun phrase
```

### Constants

UPPER_SNAKE_CASE for true constants:

```typescript
const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = 'https://api.example.com';
const DEFAULT_TIMEOUT_MS = 5000;
```

---

## Abbreviation Rules

### Never Abbreviate

```typescript
// Bad
const usr = getUser();
const btn = document.querySelector('button');
const msg = 'Hello';
const cfg = loadConfig();
const tmp = calculateTemp();

// Good
const user = getUser();
const button = document.querySelector('button');
const message = 'Hello';
const config = loadConfig();
const temperature = calculateTemperature();
```

### Acceptable Abbreviations

Only widely-understood technical abbreviations:

| Abbreviation | Meaning | Context |
|--------------|---------|---------|
| `id` | Identifier | Universal |
| `url` | Uniform Resource Locator | Web |
| `api` | Application Programming Interface | Tech |
| `html` | HyperText Markup Language | Web |
| `css` | Cascading Style Sheets | Web |
| `db` | Database | Backend |
| `io` | Input/Output | Systems |
| `i`, `j`, `k` | Loop counters | Loops only |

---

## Domain-Specific Naming

Match the language of your domain:

### E-commerce
```typescript
// Use business language
cart.addItem(product);
order.calculateSubtotal();
checkout.applyDiscount(coupon);
payment.processTransaction();
```

### Healthcare
```typescript
// Use medical terminology correctly
patient.scheduleMedication(prescription);
appointment.confirmWithProvider();
record.addDiagnosis(icdCode);
```

### Finance
```typescript
// Use financial terms
account.creditAmount(deposit);
account.debitAmount(withdrawal);
ledger.recordTransaction(entry);
portfolio.rebalanceAllocations();
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `data`, `info`, `stuff` | Too vague | Use specific noun |
| `handle`, `process`, `do` | Too generic | Use specific verb |
| `Manager`, `Handler`, `Processor` | God object smell | Split responsibilities |
| `temp`, `tmp`, `foo`, `bar` | Meaningless | Use descriptive name |
| `data1`, `data2` | Numbered variables | Use meaningful names |
| Hungarian notation (`strName`) | Type in name | Let types be types |
