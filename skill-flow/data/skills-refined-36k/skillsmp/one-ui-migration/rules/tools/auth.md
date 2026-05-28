# Auth

## What is this?

One-UI authentication tools: Token storage, JWT parsing, AuthStore.

## When to use

When accessing token or user information.

---

## Token Storage

**Must use `sessionStorage`** with key `mx_token`:

```typescript
// ✅ CORRECT
sessionStorage.getItem('mx_token')
sessionStorage.setItem('mx_token', value)
sessionStorage.removeItem('mx_token')
```

---

## JWT Parsing

```typescript
import { parseJwt, type LoginData } from '@one-ui/mxsecurity/shared/domain';

const jwtData: LoginData = parseJwt(token);

// LoginData structure
interface LoginData {
  from_ip: string;
  login_time: number;
  role: string;
  sesstion_id: string;  // Note: API has typo
  username: string;
}
```

---

## AuthStore

```typescript
import { AuthStore } from '@one-ui/mxsecurity/shared/domain';

@Component({...})
export class MyComponent {
  readonly #authStore = inject(AuthStore);

  readonly username = this.#authStore.username;
  readonly role = this.#authStore.role;
  readonly isLoggedIn = this.#authStore.isLoggedIn;
}
```

---

## Common Mistakes

```typescript
// ❌ WRONG: Using localStorage
localStorage.getItem('token')
localStorage.setItem('token', value)

// ✅ CORRECT: Using sessionStorage + mx_token
sessionStorage.getItem('mx_token')
sessionStorage.setItem('mx_token', value)

// ❌ WRONG: Wrong key
sessionStorage.getItem('token')

// ✅ CORRECT: Correct key
sessionStorage.getItem('mx_token')
```

---

## Related Tools

- [signal-store.md](./signal-store.md) - Store management
