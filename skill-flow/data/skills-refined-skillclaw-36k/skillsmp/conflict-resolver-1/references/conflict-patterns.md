# Git Conflict Resolution Patterns

Common conflict types and how to resolve them.

## Understanding Conflict Markers

```
<<<<<<< HEAD
Code from current branch (yours)
=======
Code from incoming branch (theirs)
>>>>>>> branch-name
```

## Pattern 1: Import Conflicts

### Scenario
Both branches added different imports.

### Conflict
```typescript
<<<<<<< HEAD
import { Button } from './Button';
import { Input } from './Input';
=======
import { Button } from './Button';
import { Card } from './Card';
>>>>>>> feature/cards
```

### Resolution
Combine all imports:
```typescript
import { Button } from './Button';
import { Card } from './Card';
import { Input } from './Input';
```

### Auto-Resolution: ✅ Safe

---

## Pattern 2: Additive Function Conflicts

### Scenario
Both branches added different functions to the same file.

### Conflict
```typescript
<<<<<<< HEAD
export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
=======
export function validatePhone(phone: string): boolean {
  return /^\+?[\d\s-]{10,}$/.test(phone);
}
>>>>>>> feature/phone-validation
```

### Resolution
Keep both functions:
```typescript
export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function validatePhone(phone: string): boolean {
  return /^\+?[\d\s-]{10,}$/.test(phone);
}
```

### Auto-Resolution: ✅ Safe

---

## Pattern 3: Same Function, Different Changes

### Scenario
Both branches modified the same function.

### Conflict
```typescript
<<<<<<< HEAD
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
=======
function calculateTotal(items: Item[]): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal * 1.1; // Add 10% tax
}
>>>>>>> feature/tax
```

### Resolution
**ASK USER** - Both changes have different intent:
- HEAD: Fixed quantity calculation
- Incoming: Added tax calculation

Options:
1. Keep HEAD (correct quantity, no tax)
2. Keep incoming (wrong quantity, with tax)
3. Merge both (correct quantity + tax):
```typescript
function calculateTotal(items: Item[]): number {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  return subtotal * 1.1; // Add 10% tax
}
```

### Auto-Resolution: ❌ Needs User Input

---

## Pattern 4: Package.json Dependencies

### Scenario
Both branches added different dependencies.

### Conflict
```json
<<<<<<< HEAD
  "dependencies": {
    "react": "^18.2.0",
    "axios": "^1.6.0"
  }
=======
  "dependencies": {
    "react": "^18.2.0",
    "lodash": "^4.17.21"
  }
>>>>>>> feature/utils
```

### Resolution
Combine dependencies:
```json
  "dependencies": {
    "axios": "^1.6.0",
    "lodash": "^4.17.21",
    "react": "^18.2.0"
  }
```

### Auto-Resolution: ✅ Safe (then run `npm install`)

---

## Pattern 5: Configuration Conflicts

### Scenario
Both branches modified configuration.

### Conflict
```typescript
// config.ts
<<<<<<< HEAD
export const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
};
=======
export const config = {
  apiUrl: 'https://api.example.com',
  retries: 3,
};
>>>>>>> feature/retry
```

### Resolution
Merge configuration options:
```typescript
export const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
  retries: 3,
};
```

### Auto-Resolution: ✅ Safe (if no conflicting values)

---

## Pattern 6: Type Definition Conflicts

### Scenario
Both branches extended the same type.

### Conflict
```typescript
<<<<<<< HEAD
interface User {
  id: string;
  name: string;
  email: string;
}
=======
interface User {
  id: string;
  name: string;
  avatar: string;
}
>>>>>>> feature/avatars
```

### Resolution
Combine properties:
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
}
```

### Auto-Resolution: ✅ Safe

---

## Pattern 7: Test File Conflicts

### Scenario
Both branches added different tests.

### Conflict
```typescript
<<<<<<< HEAD
describe('User', () => {
  it('should validate email', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });
});
=======
describe('User', () => {
  it('should validate phone', () => {
    expect(validatePhone('+1234567890')).toBe(true);
  });
});
>>>>>>> feature/phone
```

### Resolution
Keep all tests:
```typescript
describe('User', () => {
  it('should validate email', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  it('should validate phone', () => {
    expect(validatePhone('+1234567890')).toBe(true);
  });
});
```

### Auto-Resolution: ✅ Safe

---

## Decision Matrix

| Conflict Type | Auto-Resolve? | Strategy |
|--------------|---------------|----------|
| Different imports | ✅ Yes | Combine all |
| Different functions | ✅ Yes | Keep both |
| Same function, different logic | ❌ No | Ask user |
| Dependencies (no version conflict) | ✅ Yes | Combine |
| Dependencies (version conflict) | ❌ No | Ask user |
| Config (different keys) | ✅ Yes | Merge |
| Config (same key, different value) | ❌ No | Ask user |
| Type extensions | ✅ Yes | Combine |
| Different tests | ✅ Yes | Keep all |
| CSS/styles | ⚠️ Maybe | Check specificity |

## Post-Resolution Checklist

After resolving conflicts:

1. [ ] Remove all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
2. [ ] Ensure file is syntactically valid
3. [ ] Run typecheck
4. [ ] Run linter
5. [ ] Run tests
6. [ ] Stage resolved file: `git add <file>`
7. [ ] Complete merge: `git commit`
