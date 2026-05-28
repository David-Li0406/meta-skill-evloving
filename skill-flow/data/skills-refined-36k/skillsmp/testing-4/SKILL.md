---
name: testing
description: Guide to running and writing tests for Actions and Record Behaviors.
---
# Testing Skill

## 1. Running Tests
The CLI runs **Vitest** under the hood.

```bash
# Run ALL tests in the workspace (all apps)
simple test

# Run tests for a specific App
simple test com.mycompany.crm

# Run tests for a specific Server Action
simple test com.mycompany.crm --action import-data
# OR via alias
simple test com.mycompany.crm -a import-data

# Run tests for a specific Record Behavior (Client Script)
simple test com.mycompany.crm --behavior order
# OR via alias
simple test com.mycompany.crm -b order
```

### Options
*   `--coverage`: Generate coverage report (text/lcov).
*   `--json`: Output results in JSON for CI integration.

## 2. Testing Actions (Server)
Actions are pure TypeScript functions. Helper utilities in `tests/helpers.ts` mock the SDK Request/Context.

**Path:** `apps/<app>/actions/<name>/tests/index.test.ts`

```typescript
import { describe, it, expect } from 'vitest'
import { handle } from '../index'
import { createMockRequest } from './helpers'

describe('import-data', () => {
  it('should parse input and return success', async () => {
    const req = createMockRequest({ source: 'api' })
    const res = await handle(req)
    expect(res).toEqual({ status: 'ok' })
  })
})
```

## 3. Testing Record Behaviors (Client)
Behaviors are scripts with injected globals (`$form`, `$db`). We MUST mock these.

**Path:** `apps/<app>/scripts/record-behaviors/<table_name>.test.js`

```javascript
import { describe, it, expect, vi } from 'vitest'
// Import the default export from the script
import script from './order.js'

describe('order behavior', () => {
  it('should set default status on load', async () => {
    // 1. Mock the API
    const $form = {
      'event': 'load',
      'status': { set: vi.fn(), value: () => null }
    }
    const $user = { id: 'usr_123' }

    // 2. Run the script
    await script({ $form, $user })

    // 3. Assertions
    expect($form['status'].set).toHaveBeenCalledWith('Draft')
  })
})
```
