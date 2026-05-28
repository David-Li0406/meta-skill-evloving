---
name: develop-logic
description: Comprehensive guide to implementing full-stack logic, focusing on the "Hub-and-Spoke" binding architecture.
---
# Develop Logic Skill

## 1. The Architecture: Actions & Binding
In Simple Platform, logic is decoupled from execution triggers.
*   **Logic (The Code):** A pure function (WASM).
*   **Trigger (The Event):** A signal (DB change, Schedule, Webhook).
*   **Binding (The Link):** Connecting a Logic to a Trigger.

This allows one piece of Logic to be triggered by multiple events (e.g., "Send Email" triggered by "Signup" OR "Nightly Job").

> [!CAUTION]
> **Signature Mismatch Risk**
> *   **Server Actions** (`simple.Handle`) are NOT Record Behaviors.
> *   **Record Behaviors** (`export default ({$form})`) are NOT Server Actions.
> *   **NEVER** mix these signatures. See `rules/logic-standards.md`.

> [!IMPORTANT]
> **No Seeding in Code**
> Do not use logic to create seed data. Use SCL `instance` blocks. See `skills/data-seeding/SKILL.md`.

## 2. Server Actions (The Code)
**File:** `apps/<app>/actions/<name>/index.ts`
**Command:** `simple new action <app> <name> --scope myorg --env server`

```typescript
import simple from '@simpleplatform/sdk'
simple.Handle(async (req) => {
  const { id } = req.parse<{ id: string }>()
  // ... implementation ...
})
```

## 3. The Registration Pattern (SCL)
You must register the components in `apps/<app>/records/`.

### Step A: Define Logic (`20_logic.scl`)
```scl
set dev_simple_system.logic, action_process_order {
  name "process-order"
  display_name "Process Order"
  execution_environment server
  language go # or ts
}
```

### Step B: Define Trigger (`20_triggers.scl`)
**1. Database Event**
*   `operations`: `["insert", "update", "delete"]`
*   `condition`: jq expression (e.g., `.record.status == "Active"`).
    *   *Context:* `.record` (new), `.changes` (diff), `.operation`.

**2. Schedule (Cron)**
*   `time_schedule` options:
    *   `frequency`: `minutely`|`hourly`|`daily`|`weekly`
    *   `timezone`: IANA string (e.g. `America/New_York`)
    *   `weekdays`: `true`

**3. Webhook**
*   `method`: `post` (default), `get`, `put`, `delete`
*   `is_public`: `false` (requires auth) or `true` (open)

### Step C: Bind Them (`30_links.scl`)
This is the critical step that activates the logic.

```scl
set dev_simple_system.logic_trigger, bind_process_order {
  is_active true
  
  # Connect the dots
  logic_id `$var('meta') |> $jq('.logics[] | select(.name == "process-order") | .id')`
  trigger_id `$var('meta') |> $jq('.triggers[] | select(.name == "on-order-created") | .id')`
}
```

## 4. Client Record Behaviors
**File:** `apps/<app>/scripts/record-behaviors/<table>.js`

### Events
*   `load`: Set defaults (Client+Server).
*   `update`: React to changes (Client only).
*   `submit`: Validate (Client+Server).

### `$form` API
```javascript
// Properties
$form.event              // 'load', 'update', 'submit'
$form.record()           // Get all values

// Field Methods
$form('status').value()        // Get
$form('status').set('Active')  // Set
$form('total').editable(false) // Read-only
$form('notes').visible(false)  // Hide
$form('email').required(true)  // Mandate
$form('age').error('Too young') // Block save
```

### `$db` API (Read-Only)
```javascript
const { product } = await $db.query(
  `query($id: ID!) { ... }`, 
  { id: 123 }
)
```
