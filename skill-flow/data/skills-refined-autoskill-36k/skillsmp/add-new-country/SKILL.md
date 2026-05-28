---
name: add-new-country
description: |
  Create YAML tax configurations for new countries in the universal salary calculator.
  Use when: (1) Adding a new country to the calculator, (2) Adding a new tax year for existing country,
  (3) Creating variant configs (expat regimes, special tax rules), (4) Writing test vectors for configs.
  Triggers: "add country", "create config for", "new tax year", "add variant", "30% ruling config", etc.

  IMPORTANT: This skill includes automated test validation. All configs MUST pass `npm run test:configs`
  before completion. The skill guides you through research, implementation, test creation, validation,
  and debugging until all tests pass.
---

# Add New Country Configuration

## Workflow

1. **Research** - Gather official tax rates, brackets, contributions, credits. See references/country-tax-research.md for guidance.
2. **Plan** - Identify complexity level and required nodes
3. **Implement** - Create base.yaml with all calculations
4. **Write Tests** - Create test vectors with expected values
5. **Validate** - Run test suite, debug failures until all tests pass
6. **Document** - Add sources and notices
7. **Add research to guides** - Add the research to the guides/countries/<country>.md file.

## Quick Reference

File structure:
```
configs/<country>/<year>/
  base.yaml
  variants/<name>.yaml
  tests/<name>.json
```

Reference syntax:
- `@input_name` - User inputs (e.g., `@gross_annual`, `@filing_status`)
- `$node_or_param` - Parameters or calculated nodes

Essential node types:
- `bracket_tax` - Progressive tax brackets
- `percent_of` - Flat percentage
- `credit` - Tax credits (with optional `phaseout`)
- `sum`, `sub`, `min`, `max` - Arithmetic
- `switch`, `lookup` - Conditionals
- `function` - Escape hatch for complex logic (DE, FR, US)

## Process

### Step 1: Research

Gather from official government sources:
- Income tax brackets and rates
- Social security / national insurance rates and caps
- Standard deductions and credits
- Filing status options
- Regional variations (if any)

Record all source URLs with retrieval dates.

If the country already has a year in it, consider searching for the same / similar sources to update for the new year requested. Chances are not much changed.


### Step 2: Assess Complexity

| Level    | Characteristics                                       | Approach                 |
| -------- | ----------------------------------------------------- | ------------------------ |
| Simple   | No income tax or flat tax (UAE, SG, HK)               | Pure YAML, minimal nodes |
| Moderate | Progressive brackets + contributions (NL, AU, IE, UK) | Pure YAML                |
| High     | Multi-level regions or special calculations (CH, US)  | YAML + lookups           |
| Complex  | Income splitting, family quotient (DE, FR)            | Use `function` node      |

### Step 3: Create base.yaml

Minimal template:
```yaml
meta:
  country: "xx"
  year: 2024
  currency: "XXX"
  version: "1.0.0"
  sources:
    - url: "https://..."
      description: "Official tax rates"
      retrieved_at: "2024-01-01"
  updated_at: "2024-01-01"

notices:
  - id: "salary_input"
    title: "Annual Gross"
    body: "Enter total annual salary before deductions."
    severity: "info"

inputs:
  gross_annual:
    type: number
    required: true
  filing_status:
    type: enum
    required: true
    default: "single"
    options:
      single:
        label: "Single"
        description: "Unmarried individual"

parameters:
  tax_brackets:
    - { threshold: 0, rate: 0.20 }
    - { threshold: 50000, rate: 0.40 }

calculations:
  - id: income_tax
    type: bracket_tax
    base: "@gross_annual"
    brackets: "$tax_brackets"
    category: income_tax
    label: "Income Tax"

  - id: net_annual
    type: sub
    values: ["@gross_annual", "$income_tax"]

outputs:
  gross: "@gross_annual"
  net: "$net_annual"
  effective_rate:
    type: div
    values:
      - type: sub
        values: ["@gross_annual", "$net_annual"]
      - "@gross_annual"
  breakdown:
    taxes:
      - "$income_tax"
```

### Step 4: Write Test Vectors

Create `tests/<name>.json` covering:
- Low income (below first bracket)
- Median income (~50-80k)
- High income (top bracket)
- Each filing status
- Regional variations if applicable

**IMPORTANT**: Use official government calculators or tax tables to get accurate expected values. Don't estimate!

Test vector format:
```json
{
  "name": "Single at median income",
  "description": "Verified against official calculator at ...",
  "inputs": {
    "gross_annual": 60000,
    "filing_status": "single"
  },
  "expected": {
    "net": 45000,
    "effective_rate": 0.25,
    "breakdown": {
      "income_tax": 12000,
      "social_security": 3000
    }
  },
  "tolerance": 50,
  "sources": [{
    "description": "Official tax calculator result",
    "url": "https://...",
    "retrieved_at": "2024-01-01"
  }]
}
```

**Tips**:
- Include `breakdown` expectations for major tax items to catch calculation errors early
- Set reasonable `tolerance` (e.g., 50 for rounding differences, 0.0001 for rates)
- Document source URLs so test vectors can be verified independently

### Step 5: Run Test Suite & Debug

**CRITICAL**: All tests MUST pass before the config is considered complete.

Run the test suite:
```bash
# Run all config tests
npm run test:configs

# Or run tests for specific country
npx vitest run packages/engine/__tests__/config-tests.test.ts -t "xx/2024"
```

#### Common Test Failures & Fixes

**Reference Errors** (`Reference not found: xyz`):
- Check that all `@` inputs are defined in `inputs:` section
- Check that all `$` references point to valid `parameters:` or `calculations:` nodes
- Ensure node IDs match exactly (case-sensitive)

**Calculation Mismatches** (Expected X, got Y):
- Verify bracket thresholds and rates from official sources
- Check for off-by-one errors in bracket calculations
- Ensure correct order of operations in compound calculations
- Validate phaseout calculations (start, end, rate)
- Check rounding modes and precision

**Type Errors** (`is not a number`):
- Ensure switch cases return the correct type for downstream nodes
- Check that conditionals return numeric values when used in arithmetic
- Verify lookup tables have numeric values where expected

**Breakdown Errors** (`Breakdown item not found`):
- Ensure all breakdown nodes have `category` and `label`
- Check that output section references match node IDs

#### Debugging Process

1. **Read the error message** - identifies which test and what failed
2. **Check test vector** - verify expected values are correct
3. **Trace calculation** - follow the node DAG from inputs to outputs
4. **Fix config** - adjust brackets, rates, or logic
5. **Re-run tests** - repeat until all pass

#### Validation Checklist

Once tests pass, verify:
- [ ] All `@` and `$` references resolve
- [ ] Every breakdown node has `category` and `label`
- [ ] Sources documented with URLs and dates
- [ ] Test vectors verified against official calculators
- [ ] Notices guide users on country-specific conventions
- [ ] **All tests pass: `npm run test:configs` shows 100% passing**

### Step 6: Document

Final touches:
- Add helpful notices explaining country-specific conventions
- Document any assumptions or limitations
- Add `description` to all enum options
- Review all source URLs are accessible and dated

## Creating Variants

For special regimes (expat rules, alternative tax treatments):

```yaml
meta:
  variant: "special-regime"
  label: "Special Regime Name"
  description: "Who qualifies and what it does"
  base: "../base.yaml"

parameters:
  # Override or add parameters

calculations:
  # Override nodes by matching id
  - id: taxable_income
    type: mul
    values: ["@gross_annual", 0.70]
```

**Don't forget**: Variants need their own test vectors too! Run `npm run test:configs` to ensure variant tests pass.

## Detailed Specification

See [references/DATA_SPEC.md](references/DATA_SPEC.md) for:
- Complete node type reference
- All input types and options
- Bracket table formats
- Overlay merge rules
- Validation requirements
