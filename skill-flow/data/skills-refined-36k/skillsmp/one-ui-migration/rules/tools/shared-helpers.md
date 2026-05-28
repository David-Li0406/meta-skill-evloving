# Shared Helpers

## What is this?

Common utility functions available in One-UI shared domain that can be reused across features.

## When to use

When you need common operations like JWT parsing, IP sorting, dialog configurations, or file downloads.

---

## Available Shared Helpers

### Dialog Configuration

Pre-configured dialog sizes for consistent UI:

```typescript
import {
  smallDialogConfig,
  mediumDialogConfig,
  largeDialogConfig,
  extraLargeDialogConfig
} from '@one-ui/shared/domain';

// Small dialog (400px width)
this.dialog.open(MyDialog, { ...smallDialogConfig, data });

// Medium dialog (560px width)
this.dialog.open(MyDialog, { ...mediumDialogConfig, data });

// Large dialog (720px width)
this.dialog.open(MyDialog, { ...largeDialogConfig, data });

// Extra large dialog (960px width)
this.dialog.open(MyDialog, { ...extraLargeDialogConfig, data });
```

---

### JWT Parsing

Parse JWT tokens to extract payload data:

```typescript
import { parseJwt } from '@one-ui/shared/domain';

// Get JWT from storage
const token = sessionStorage.getItem('mx_token');

// Parse to get payload
const payload = parseJwt(token);

// Access claims
console.log(payload.userId);
console.log(payload.username);
console.log(payload.exp); // Expiration time
```

**Type Definition**:
```typescript
interface JwtPayload {
  [key: string]: any;
  exp?: number;  // Expiration time (Unix timestamp)
  iat?: number;  // Issued at (Unix timestamp)
}
```

---

### IP Address Utilities

Convert IP addresses to numbers for proper sorting:

```typescript
import { convertIpToNumber } from '@one-ui/shared/domain';

// Problem: String sorting of IPs is wrong
// ['192.168.1.10', '192.168.1.2'].sort()  → ['192.168.1.10', '192.168.1.2'] ❌

// Solution: Convert to number for sorting
const columns = computed(() => [
  {
    key: 'ipAddress',
    header: this.#transloco.translate('general.common.ip_address'),
    sort: (data) => convertIpToNumber(data.ipAddress)  // ✅ Correct numeric sort
  }
]);
```

**How it works**:
```typescript
convertIpToNumber('192.168.1.1')   // → 3232235777
convertIpToNumber('192.168.1.10')  // → 3232235786
convertIpToNumber('10.0.0.1')      // → 167772161
```

---

### Options Lookup

Get display text from an options array by value:

```typescript
import { getTextByValue } from '@one-ui/shared/domain';

// Default usage (looks for 'value' and 'text' fields)
const options = [
  { value: '1', text: 'Option 1' },
  { value: '2', text: 'Option 2' }
];
getTextByValue(options, '1'); // → 'Option 1'

// Custom field names
const interfaces = [
  { id: 'eth0', label: 'Ethernet 0' },
  { id: 'eth1', label: 'Ethernet 1' }
];
getTextByValue(interfaces, 'eth0', 'id', 'label'); // → 'Ethernet 0'
```

**Signature**:
```typescript
function getTextByValue<T = any>(
  options: T[],
  value: any,
  valueField: string = 'value',
  textField: string = 'text'
): string
```

---

### File Download

Utilities for handling file downloads:

```typescript
import { createDownloadOptions, triggerFileDownload } from '@one-ui/shared/domain';

// Create download options for API calls
const downloadOptions = createDownloadOptions();

// Make API call with download options
this.http.get('/api/export/config', downloadOptions)
  .subscribe(blob => {
    // Trigger file download in browser
    triggerFileDownload(blob, 'config.json');
  });
```

**createDownloadOptions()**:
Returns HTTP options for blob responses:
```typescript
{
  responseType: 'blob',
  observe: 'response'
}
```

**triggerFileDownload(blob, filename)**:
- Creates a temporary download link
- Triggers download in the browser
- Automatically cleans up the temporary link

---

## Common Use Cases

### Table Column Sorting

```typescript
readonly columns = computed(() => [
  // String column - default sorting
  {
    key: 'name',
    header: this.#transloco.translate('general.common.name')
  },
  // IP address column - numeric sorting
  {
    key: 'ipAddress',
    header: this.#transloco.translate('general.common.ip_address'),
    sort: (data) => convertIpToNumber(data.ipAddress)
  },
  // Status column - display text from options
  {
    key: 'status',
    header: this.#transloco.translate('general.common.status'),
    valueFormatter: (data) => getTextByValue(STATUS_OPTIONS, data.statusRaw)
  }
]);
```

### Dialog with Standard Size

```typescript
openEditDialog(user: User) {
  const dialogRef = this.#dialog.open(UserEditDialog, {
    ...mediumDialogConfig,
    viewContainerRef: this.#viewContainerRef,
    data: { mode: 'edit', user }
  });

  dialogRef.afterClosed().subscribe(result => {
    if (result) {
      this.#store.updateUser({ input: result });
    }
  });
}
```

### Config Export/Import

```typescript
// Export config
exportConfig() {
  const downloadOptions = createDownloadOptions();

  this.#api.exportConfig$(downloadOptions).subscribe(blob => {
    triggerFileDownload(blob, `config-${Date.now()}.json`);
  });
}

// Import config
importConfig(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  this.#api.importConfig$(formData).subscribe(() => {
    this.#snackbar.success('Config imported successfully');
  });
}
```

### Authentication

```typescript
// Check if user is authenticated
isAuthenticated(): boolean {
  const token = sessionStorage.getItem('mx_token');
  if (!token) return false;

  const payload = parseJwt(token);
  const now = Math.floor(Date.now() / 1000);

  // Check if token is expired
  return payload.exp ? payload.exp > now : false;
}

// Get current user info
getCurrentUser(): User | null {
  const token = sessionStorage.getItem('mx_token');
  if (!token) return null;

  const payload = parseJwt(token);
  return {
    userId: payload.sub,
    username: payload.username,
    role: payload.role
  };
}
```

---

## Project-Specific Helpers

Some projects may have additional shared helpers in their own shared domain. Check your project's shared domain for:

- Date/time formatting utilities
- Project-specific validators
- Custom data transformations
- Business logic helpers

**Example Project Structure**:
```
libs/{scope}/shared/domain/src/lib/
├── helpers/
│   ├── dialog-config.ts        # ✅ Generic
│   ├── parseJwt.ts             # ✅ Generic
│   ├── ip-address.helper.ts    # ✅ Generic
│   ├── get-text-by-value.ts    # ✅ Generic
│   └── time.helper.ts          # ⚠️ Project-specific
```

---

## When to Add a Helper to Shared Domain

Add a helper to shared domain when:

1. **Reusability**: The function is used by **2+ features**
2. **Pure Function**: No side effects, just input → output
3. **Generic**: Not tied to a specific feature's domain logic

**Don't add to shared domain when**:
- Only used in one feature (keep in feature's helper file)
- Contains feature-specific business logic
- Depends on feature-specific types or state

---

## Related Tools

- [ddd-architecture.md](../reference/ddd-architecture.md#helper-ts-pure-functions) - Helper file patterns
- [dialogs.md](./ui/dialogs.md) - Dialog patterns
