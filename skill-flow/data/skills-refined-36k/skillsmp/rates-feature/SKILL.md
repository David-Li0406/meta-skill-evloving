---
name: rates-feature
description: Specialized guidance for developing features in the Rates module of the Viya application. Use when working on rate contracts, zones, surcharges, prices, transit times, or condition templates.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Rates Feature Development Skill

Guidelines for developing features in the **Rates** module. For general Vue.js patterns, use the **vue-component** skill.

---

## Quick Reference

### Key Paths

| Path | Purpose |
|------|---------|
| `src/views/rates/` | Rates page components and configuration |
| `src/views/rates/components/` | Reusable rates components (selectors, tables, helpers) |
| `src/views/rates/components/rates-tables/` | `RatesTable.vue` and `defaults.ts` (copy-paste infrastructure) |
| `src/views/rates/configuration/` | Configuration pages (zones, prices, surcharges, transit times) |
| `src/store/rates/` | Pinia store, converters, validation helpers |
| `src/services/rates/` | API service classes for rates endpoints |
| `src/components/condition-builder/` | Condition builder components (AND/OR logic, comparisons) |
| `playwright/tests/app-tests/rates/` | E2E tests and helpers for rates module |
| `src/generated/rates.ts` | Auto-generated TypeScript types from API |

### Common Commands

```bash
npm run type-check          # Type checking
npm run lint:fix            # Linting & formatting
npm run dev:docker:go       # Run dev server

# Run rates E2E tests
npx playwright test playwright/tests/app-tests/rates/rates.spec.ts

# Run with verbose logging
PW_VERBOSE=1 npx playwright test playwright/tests/app-tests/rates/rates.spec.ts
```

---

## Module Architecture

### Overview

The Rates module manages shipping rate contracts, service levels, zones, surcharges, prices, and transit times. It uses a **multi-step wizard pattern** with **layered tabs** for organizing complex configuration data.

```
Rate Contract
├── Zones (Contract-level)
│   ├── Range Zones (grouped by tab: origin, destination, etc.)
│   └── Combined Zones (combining multiple range zones)
├── Surcharges (Contract-level)
│   ├── Fixed Surcharges
│   └── Percentage Surcharges
└── Service Levels (e.g., "standard", "express")
    ├── Prices
    │   ├── Condition Tables (dynamic pricing based on conditions)
    │   └── Price Template Tables
    └── Transit Times
```

### Store Architecture

| File | Purpose |
|------|---------|
| `rates-store.ts` | Main Pinia store with state, actions, and getters |
| `rates-validation-helpers.ts` | **Central validation logic** for all rates data |
| `price-converters.ts` | Convert between API and frontend price formats |
| `surcharge-converters.ts` | Convert between API and frontend surcharge formats |
| `transit-converters.ts` | Convert between API and frontend transit time formats |
| `zones/zone-converters.ts` | Convert between API and frontend zone formats |
| `condition-templates/` | Condition template converters and helpers |

---

## Validation Architecture

### Three-Layer Validation System

1. **Step/Tab Level** - Error counts shown on wizard steps and tabs
   - Calculated in `calculateRatesValidation()` in `rates-validation-helpers.ts`
   - Returns `RatesValidation` type with error lists per field
   - Used by `LoadServiceLevelElements.vue` for step badges
   - Used by `SurchargesTab.vue` for tab badges

2. **Column Header Level** - Error counts shown in table column headers
   - Uses `validationHeader()` from `rates-tables/defaults.ts`
   - Counts rows with validation errors for that column
   - Shows red badge with count next to header text

3. **Cell Level** - Inline validation in individual cells
   - Uses `errors` prop on input/select components
   - Uses `errorAsTooltip` to show errors as tooltips (prevents overlap)
   - Implemented via `toErrorObjects()` helper

**When adding a new validated column, update ALL THREE levels:**
1. Add to `RatesValidation` type definition
2. Add to `calculateRatesValidation()` function
3. Add `validator` to column's `validationHeader()` call
4. Add validation to the cell component (if using custom selector)

### Static vs Dynamic Validation

| Category | Data Source | Validation Location | Example Fields |
|----------|-------------|---------------------|----------------|
| **Static** | Generated types (`@/generated/rates`) | Direct helper function (no store needed) | Price groups, distance units, currencies, country codes |
| **Dynamic** | Store state (loaded from API) | Store method wrapping `...Clean` helper | Service levels, zone references, surcharge labels |

### Static Validators (No Store Needed)

```typescript
// Static validator - uses generated priceGroupValues, no store data needed
export const validatePriceGroups = (value: unknown): string | undefined => {
  if (!value || (Array.isArray(value) && value.length === 0)) return undefined;
  if (!Array.isArray(value)) return 'Must be an array';
  const invalid = value.filter((pg) => !(priceGroupValues as string[]).includes(pg));
  return invalid.length > 0 ? `Contains invalid price groups: ${invalid.join(', ')}` : undefined;
};
```

### Dynamic Validators (Store-Dependent)

For fields validated against runtime data, use the **`...Clean` pattern**:

**Step 1: Define `...Clean` function** (pure, testable):

```typescript
export const validateServiceLevelsClean = (
  value: unknown,
  availableServiceLevels: string[]
): string | undefined => {
  if (!value || (Array.isArray(value) && value.length === 0)) return undefined;
  if (!Array.isArray(value)) return 'Must be an array';
  const nonExisting = value.filter((sl) => !availableServiceLevels.includes(sl));
  return nonExisting.length > 0
    ? `Contains non-existing service levels: ${nonExisting.join(', ')}`
    : undefined;
};
```

**Step 2: Add store wrapper**:

```typescript
// In rates-store.ts
validateServiceLevels(value: unknown): string | undefined {
  return validateServiceLevelsClean(value, this.serviceLevelRefs);
},
```

### Selector Component Pattern

```vue
<script setup lang="ts">
import { toErrorObjects } from '@/views/rates/components/error-helpers';
import { validatePriceGroups } from '@/store/rates/rates-validation-helpers';

const data = defineModel<PriceGroup[]>({ required: true });

const errors = computed<ErrorObject[]>(() => {
  const isClearable = props.clearable ?? true;
  const isEmpty = !data.value || data.value.length === 0;
  if (isClearable && isEmpty) return [];

  // For static validators - import and use directly:
  return toErrorObjects(data.value, validatePriceGroups);
  
  // For dynamic validators - use via store:
  // return toErrorObjects(data.value, store.validateServiceLevels);
});
</script>

<template>
  <SelectComponent
    v-model="data"
    :errors="errors"
    error-as-tooltip  <!-- CRITICAL: Prevents error text from overlapping -->
  />
</template>
```

---

## RatesTable & Copy-Paste Architecture

### Overview

`RatesTable` is a TanStack Table wrapper that supports:
- Copy-paste from spreadsheets (Excel, Google Sheets, etc.)
- Expandable rows (historical versions)
- Column-level and cell-level validation
- Custom cell renderers

### Key Files

| File | Purpose |
|------|---------|
| `rates-tables/RatesTable.vue` | Main table component |
| `rates-tables/defaults.ts` | Copy-paste logic, validation headers, cell renderers |

### Copy-Paste Flow

1. User pastes in a cell (triggers `onPaste` event)
2. `handlePaste()` in `defaults.ts` processes clipboard data
3. Data is split by tabs (columns) and newlines (rows)
4. For each cell, `updateCell()` is called on the table's `meta`
5. The column-specific `updateCell` function parses and applies the value

### Adding a Copy-Pasteable Column

**Step 1: Define the column with `limitPasteToColumnIndices`**

```typescript
export const refLabelColumn = (
  onContract: boolean,
  pasteableColumns: number,
  validateSurchargeLabel: (value: unknown, row: ContractSurcharge, onContract: boolean) => string | undefined
): ColumnDef<ContractSurcharge> => ({
  id: 'label',
  accessorFn: (row) => row.label,
  header: validationHeader('Name', {
    validator: (value, row) => validateSurchargeLabel(value, row, onContract),
    noSubRowValidation: true,
  }),
  cell: copyPasteCell({
    limitPasteToColumnIndices: [...Array(pasteableColumns).keys()].map((i) => i + 2),
    validator: (value, row) => validateSurchargeLabel(value, row, onContract),
    readonlyInSubRows: true,
  }),
});
```

**Step 2: Use generic parser for comma/space-separated values**

```typescript
import { simpleCommaSeparatedColumnParser } from '@/utils/general';

// In updateCell():
if (columnId === 'serviceLevels') {
  currentRow.serviceLevels = simpleCommaSeparatedColumnParser(value);
}
```

**Step 3: Update download string function**

```typescript
export const fixedSurchargesDownloadString = (data: ContractSurcharge[]): string => {
  const headers = ['Name', 'Description', 'Service Levels'];
  const rows = data.map((item) => [
    item.label,
    item.description ?? '',
    item.serviceLevels?.join(', ') ?? '',
  ]);
  return getTableDownloadString(headers, rows);
};
```

**Step 4: Update `pasteableColumns` count when adding columns**

---

## Condition Templates

### Overview

Condition Templates allow reusable condition definitions with variables that can be filled in when used in price tables.

### Data Structure

```typescript
ConditionTemplate: {
  reference: string;              // Unique identifier
  label?: string;                 // Display name
  description?: string;           // Documentation
  condition: AndCondition | OrCondition | CompareCondition | TemplateCondition;
  variables?: { [key: string]: string };  // Maps variable names to paths
}
```

**Variable Paths** use JSONPath-like notation:
- `$.and[0].decimal` → First condition in AND group, decimal comparison
- `$.or[1].boolean` → Second condition in OR group, boolean comparison

### Inline Variable Editing

Variables are edited **inline** within the condition tree:

1. Each comparison shows a "var" button when `onVariablesChange` is provided
2. Clicking "var" creates a variable with auto-generated name
3. Variable appears as teal tag with order number, name input, and delete button
4. Teal rounded border appears around the comparison

### Usage Tracking & Locking

When a template is **used** (`templateUsed: true`):

| Element | Editable | Reason |
|---------|----------|--------|
| Variable reference names | No | Used as column headers in price tables |
| Variable order numbers | No | Determines column order |
| Comparison paths | No | Changing would invalidate existing data |
| Comparison operators | Yes | Allows fixing logic errors |
| Add new variables | No | "var" button hidden |
| Delete variable comparisons | No | Trash icon hidden |

---

## Wizard Structure

```
LoadServiceLevelElements.vue (wizard container)
├── Step 0: Contract Zones (RatesStepsZones.vue)
├── Step 1: Contract Surcharges (SurchargesTab.vue) - onContract=true
├── Step 2: Service Level Prices (RatesStepsBasePrices.vue)
└── Step 3: Service Level Transit Times (RatesStepsTransitTimes.vue)
```

### Step Error Counts

```typescript
const stepErrorCount = computed(() => {
  const validation = store.getRatesValidation;
  return {
    zones: doubleRecordValidationCount(validation.zones.ranges) +
           recordValidationCount(validation.zones.combined),
    surcharges: doubleRecordValidationCount(validation.surcharges),
    prices: doubleRecordValidationCount(validation.prices.conditionTables) +
            doubleRecordValidationCount(validation.prices.priceTemplateTables),
    transitTimes: doubleRecordValidationCount(validation.transitTimes),
  };
});
```

---

## Lessons Learned

### Copy-Paste Architecture
- **Paste target**: Always the first non-readonly cell in the first editable column
- **Column indices**: Start at 2 (after expandable icon and createdOn columns)
- **Parser functions**: Use `simpleCommaSeparatedColumnParser` for comma/space-separated values
- **Case sensitivity**: Parser functions should handle case-insensitive input

### Validation
- **Three levels**: Step → Tab → Column header → Cell
- **Static vs Dynamic**: Use local validation for static types, store validation for dynamic data
- **`noSubRowValidation`**: Skip validation for historical version subrows

### Selector Components
- **`error-as-tooltip`**: Prevents multi-line error text from overlapping input
- **Empty check**: Skip validation entirely when clearable and empty
- **Readonly mode**: Show `InputComponent` with comma-separated values instead of disabled `SelectComponent`

### Render Function Patterns (h())

```typescript
cell: ({ getValue, row, column: { id }, table: { options } }) => {
  const cellValue = ref<MyType>();
  cellValue.value = getValue<MyType>();
  
  const handleUpdate = (newValue: MyType) => {
    options.meta?.updateCell(row.index, id, newValue);
  };
  
  return h(MySelector, {
    modelValue: cellValue.value,
    'onUpdate:modelValue': handleUpdate,
    readonly: getRowRealDepth(row.original, row.depth) > 0,
  });
},
```

---

## Checklist for New Validated Column

- [ ] Determine type: Static (direct validator) or Dynamic (`...Clean` + store wrapper)
- [ ] Add validator to `rates-validation-helpers.ts`
- [ ] If dynamic: Add store wrapper method in `rates-store.ts`
- [ ] Add to `RatesValidation` type
- [ ] Add to `calculateRatesValidation()`
- [ ] Add to column definition with `validationHeader()`
- [ ] Add to selector component with `toErrorObjects()`
- [ ] Update `pasteableColumns` count if copy-pasteable
- [ ] Update download string function
- [ ] Update copy-paste example in Vue template

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **vue-component** | General Vue.js component patterns |
| **playwright-test** | Writing E2E tests for rates features |
| **api-integration** | Working with rates API services |
