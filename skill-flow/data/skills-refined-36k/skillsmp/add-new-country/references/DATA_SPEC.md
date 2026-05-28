# Universal Salary Calculator - Configuration Specification v1

## Overview

This specification defines the YAML-based configuration format for country tax calculations. The system uses a declarative DAG (Directed Acyclic Graph) approach for most calculations, with an escape hatch to TypeScript functions for complex tax regimes.

## Design Principles

1. **Declarative first**: Simple tax systems should be fully expressible in YAML
2. **Escape hatch for complexity**: Complex patterns (income splitting, family quotient, AMT) delegate to registered TypeScript functions
3. **Contributor-friendly**: Non-programmers can update rates and brackets; complex logic is maintainer-owned
4. **Transparent**: Every calculation step is traceable and explainable in the UI
5. **Extensible**: New inputs and calculation types can be added without breaking existing configs

---

## File Structure

```
configs/
  <country>/                      # ISO 3166-1 alpha-2 lowercase (e.g., "nl", "ch", "us")
    <year>/                       # Tax year (e.g., "2024")
      base.yaml                   # Required base configuration
      variants/
        <variant>.yaml            # Optional overlays (e.g., "30-ruling.yaml", "expat.yaml")
      tests/
        <name>.json               # Test vectors
```

### Naming Conventions

- Country codes: lowercase ISO 3166-1 alpha-2 (`nl`, `de`, `us`, `gb`, `ch`)
- Years: four digits (`2024`, `2025`)
- Variant files: kebab-case (`30-ruling.yaml`, `married-filing-jointly.yaml`)
- Test files: kebab-case descriptive names (`single-median-income.json`, `high-earner-with-credits.json`)

---

## Configuration Schema

### Top-Level Structure

```yaml
meta:           # Required - metadata and provenance
notices:        # Optional - user guidance messages
inputs:         # Required - user input definitions
parameters:     # Required - constants, rates, brackets, lookup tables
calculations:   # Required - computation DAG
outputs:        # Required - result mapping
```

---

### `meta` Section

```yaml
meta:
  country: "nl"                          # ISO 3166-1 alpha-2, lowercase
  year: 2024                             # Tax year (integer)
  currency: "EUR"                        # ISO 4217 currency code
  version: "1.0.0"                       # Semver - bump on any change

  # Documentation and trust
  sources:
    - url: "https://www.belastingdienst.nl/..."
      description: "Official 2024 tax rates"
      retrieved_at: "2024-01-15"         # ISO 8601 date
    - url: "https://..."
      description: "Social security contribution rates"
      retrieved_at: "2024-01-15"

  updated_at: "2024-01-20"               # Last modification date

  # Optional
  notes: |
    Free-form notes about this configuration,
    known limitations, or upcoming changes.
```

#### For Variant Files

```yaml
meta:
  variant: "30-ruling"                   # Variant identifier (kebab-case)
  label: "30% Ruling"                    # Human-readable name
  description: "Tax benefit for highly skilled migrants recruited from abroad"
  base: "../base.yaml"                   # Relative path to base config

  sources:
    - url: "https://..."
      description: "30% ruling eligibility criteria"
      retrieved_at: "2024-01-15"
```

---

### `notices` Section

Country-specific guidance displayed in the UI to help users enter correct information.

```yaml
notices:
  - id: "holiday_allowance"              # Unique identifier (snake_case)
    title: "Holiday Allowance"           # Short title
    body: |
      Enter your total annual gross salary including the 8% holiday
      allowance (vakantiegeld) if your employer pays it.
    severity: "info"                     # "info" | "warning" | "error"

  - id: "company_car"
    title: "Company Car (Bijtelling)"
    body: "If you have a lease car, add the taxable benefit to your gross."
    severity: "info"

  - id: "30_ruling_check"
    title: "30% Ruling Eligibility"
    body: "This variant assumes you qualify. Check eligibility requirements."
    severity: "warning"
    show_for_variants:                   # Optional - only show for specific variants
      - "30-ruling"
```

---

### `inputs` Section

Defines all user-provided inputs. The engine always provides `gross_annual`.

```yaml
inputs:
  # Always required - provided by engine
  gross_annual:
    type: number
    required: true
    min: 0
    label: "Annual Gross Salary"
    description: "Your total yearly salary before any deductions"

  # Country-specific filing status
  filing_status:
    type: enum
    required: true
    default: "single"                    # Optional default value
    label: "Filing Status"
    options:
      single:
        label: "Single"
        description: "Unmarried, not in registered partnership"
      partner:
        label: "With Fiscal Partner"
        description: "Married or registered partnership"
      # Add country-specific statuses as needed

  # Two-level regional hierarchy
  region_level_1:
    type: enum
    required: false                      # Usually optional
    label: "Canton"                      # Country-specific label
    options:
      zurich:
        label: "Zürich"
      bern:
        label: "Bern"
      # ...

  region_level_2:
    type: enum
    required: false
    label: "Municipality"
    depends_on: region_level_1           # Only shown when level_1 is selected
    options_by_parent:
      zurich:
        zurich_city:
          label: "Zürich (city)"
        winterthur:
          label: "Winterthur"
      bern:
        bern_city:
          label: "Bern (city)"
        thun:
          label: "Thun"
      # ...

  # Extensible - add future inputs here
  # age:
  #   type: number
  #   required: false
  #   min: 16
  #   max: 100
  #   label: "Age"
  #   description: "Some credits depend on age"

  # dependents:
  #   type: number
  #   required: false
  #   default: 0
  #   min: 0
  #   label: "Number of Dependents"
```

#### Input Types

| Type | Description | Additional Fields |
|------|-------------|-------------------|
| `number` | Numeric value | `min`, `max`, `default` |
| `enum` | Single selection | `options`, `default` |
| `boolean` | True/false | `default` |

---

### `parameters` Section

Named constants, rate tables, and lookup tables used in calculations.

```yaml
parameters:
  # Simple constants
  general_tax_credit_max: 3362
  labour_tax_credit_max: 5052
  social_security_cap: 66956
  solidarity_surcharge_rate: 0.055

  # Bracket tables (for progressive taxes)
  income_tax_brackets:
    - threshold: 0
      rate: 0.3697
    - threshold: 73031
      rate: 0.495

  # Brackets can also have fixed amounts
  german_brackets:
    - threshold: 0
      rate: 0
      base_amount: 0
    - threshold: 11604
      rate: 0.14
      base_amount: 0
    - threshold: 17005
      rate: 0.2397
      base_amount: 756
    # ...

  # Lookup tables (keyed by region, status, etc.)
  cantonal_multipliers:
    zurich: 1.00
    bern: 1.06
    geneva: 0.98
    # ...

  municipal_rates:
    zurich:
      zurich_city: 1.19
      winterthur: 1.22
    bern:
      bern_city: 1.54
      thun: 1.49
    # ...

  # Phaseout parameters (grouped for clarity)
  general_credit_phaseout:
    start_income: 22661
    end_income: 73031
    reduction_rate: 0.06095
```

---

### `calculations` Section

The computation DAG. Nodes are evaluated in dependency order (topological sort).

#### Reference Syntax

- `@input_name` - References a user input (e.g., `@gross_annual`, `@filing_status`)
- `$node_or_param` - References a parameter or calculated node (e.g., `$income_tax_brackets`, `$taxable_income`)
- `@input.property` - Accesses a property of an enum input (e.g., `@filing_status.splitting_factor`)

#### Node Structure

```yaml
calculations:
  - id: node_id                          # Unique identifier (snake_case)
    type: node_type                      # See node types below
    # ... type-specific parameters

    # Optional metadata (for breakdown display)
    category: "income_tax"               # Grouping: income_tax | contribution | credit | deduction | surtax
    label: "Income Tax"                  # Human-readable name for UI
    description: "Federal income tax"    # Optional longer description
```

#### Node Types

##### Arithmetic Nodes

```yaml
# Identity (pass-through)
- id: taxable_income
  type: identity
  value: "@gross_annual"

# Sum
- id: total_deductions
  type: sum
  values:
    - "$pension_contribution"
    - "$health_insurance"
    - "$commuter_allowance"

# Subtraction (first value minus rest)
- id: net_income
  type: sub
  values:
    - "@gross_annual"
    - "$total_tax"

# Multiplication
- id: taxable_portion
  type: mul
  values:
    - "@gross_annual"
    - 0.70                               # 30% ruling: only 70% taxable

# Division
- id: monthly_net
  type: div
  values:
    - "$net_annual"
    - 12

# Minimum
- id: capped_income
  type: min
  values:
    - "@gross_annual"
    - "$social_security_cap"

# Maximum
- id: tax_floor
  type: max
  values:
    - "$calculated_tax"
    - 0                                  # Tax can't be negative

# Clamp (value between min and max)
- id: clamped_credit
  type: clamp
  value: "$raw_credit"
  min: 0
  max: "$max_credit"
```

##### Tax Nodes

```yaml
# Progressive bracket tax
- id: income_tax
  type: bracket_tax
  base: "$taxable_income"
  brackets: "$income_tax_brackets"
  category: income_tax
  label: "Income Tax"

# Flat percentage
- id: medicare_levy
  type: percent_of
  base: "$taxable_income"
  rate: 0.02
  category: contribution
  label: "Medicare Levy"

# Percentage of another tax (surtax)
- id: solidarity_surcharge
  type: percent_of
  base: "$income_tax"
  rate: 0.055
  category: surtax
  label: "Solidarity Surcharge"
  # Only applied if income_tax exceeds threshold
  condition:
    type: gt
    left: "$income_tax"
    right: 18130
```

##### Credit and Deduction Nodes

```yaml
# Tax credit (reduces tax liability)
- id: general_tax_credit
  type: credit
  amount: "$general_tax_credit_max"
  refundable: false                      # true = can result in refund
  category: credit
  label: "General Tax Credit"

  # Optional phaseout
  phaseout:
    base: "$taxable_income"              # Income used for phaseout calc
    start: 22661                         # Phaseout begins here
    end: 73031                           # Fully phased out here
    rate: 0.06095                        # Reduction per euro over start

# Deduction (reduces taxable income)
- id: pension_deduction
  type: deduction
  amount: "@voluntary_pension"           # User input
  cap: 3000                              # Maximum deductible
  category: deduction
  label: "Pension Contribution Deduction"
```

##### Control Flow Nodes

```yaml
# Switch/conditional based on input or parameter
- id: base_exemption
  type: switch
  on: "@filing_status"
  cases:
    single: 11604
    married_joint: 23208
  default: 11604

# Switch with complex values
- id: tax_brackets
  type: switch
  on: "@region_level_1"
  cases:
    scotland: "$scottish_brackets"
    _: "$ruk_brackets"                   # "_" is the default case

# Lookup in a table
- id: cantonal_multiplier
  type: lookup
  table: "$cantonal_multipliers"
  key: "@region_level_1"
  default: 1.0                           # If region not found

# Nested lookup (two levels)
- id: municipal_rate
  type: lookup
  table: "$municipal_rates"
  key: "@region_level_1"
  subkey: "@region_level_2"
  default: 1.0
```

##### Utility Nodes

```yaml
# Rounding
- id: final_tax
  type: round
  value: "$raw_tax"
  precision: 2                           # Decimal places
  mode: "half_up"                        # half_up | half_down | floor | ceil

# Conditional (if-then-else)
- id: high_earner_levy
  type: conditional
  condition:
    type: gt
    left: "$taxable_income"
    right: 150000
  then:
    type: percent_of
    base: "$taxable_income"
    rate: 0.01
  else: 0
```

##### Function Node (Escape Hatch)

For complex calculations that can't be expressed declaratively.

```yaml
# Delegate to registered TypeScript function
- id: income_tax
  type: function
  name: "income_splitting_tax"           # Must be registered in engine
  inputs:
    gross: "@gross_annual"
    filing_status: "@filing_status"
    brackets: "$income_tax_brackets"
    splitting_factor: "@filing_status.splitting_factor"
  category: income_tax
  label: "Income Tax (Ehegattensplitting)"
```

**Available built-in functions:**

| Function | Use Case | Countries |
|----------|----------|-----------|
| `income_splitting_tax` | Ehegattensplitting - split income, compute tax, double | DE |
| `family_quotient_tax` | Quotient familial - divide by family units, compute, multiply | FR |
| `alternative_minimum_tax` | Compute regular + AMT, return max | US |
| `swiss_federal_tax` | Swiss federal tax with married/single curves | CH |

New functions require engine changes and maintainer review.

##### Inline Expressions

For simple cases, nodes can be inlined within other nodes:

```yaml
- id: tax_after_credits
  type: max
  values:
    - type: sub
      values:
        - "$total_tax"
        - "$total_credits"
    - 0                                  # Inline constant
```

**Rule:** Inline nodes cannot have `category` or `label`. If it needs to appear in the breakdown, give it a named `id`.

---

### `outputs` Section

Maps calculation results to the API response structure.

```yaml
outputs:
  # Primary outputs
  gross: "@gross_annual"
  net: "$net_annual"

  # Computed effective rate
  effective_rate:
    type: div
    values:
      - type: sub
        values: ["@gross_annual", "$net_annual"]
      - "@gross_annual"

  # Itemized breakdown for transparency
  # Only nodes with category/label appear here
  breakdown:
    taxes:
      - "$income_tax"
      - "$solidarity_surcharge"          # If exists
    contributions:
      - "$social_security"
      - "$health_insurance"
    credits:
      - "$general_tax_credit"
      - "$labour_tax_credit"
    deductions:
      - "$pension_deduction"             # If exists
```

---

## Variant Overlay Mechanism

Variants use **deep merge** with the base config:

1. Objects are recursively merged
2. Arrays are **replaced entirely** (not concatenated)
3. Use `$delete` to remove a key
4. Scalar values are overwritten

### Example Variant

```yaml
# configs/nl/2024/variants/30-ruling.yaml

meta:
  variant: "30-ruling"
  label: "30% Ruling"
  description: "Tax benefit for highly skilled migrants"
  base: "../base.yaml"
  sources:
    - url: "https://..."
      description: "30% ruling conditions 2024"
      retrieved_at: "2024-01-15"

# Add variant-specific notice
notices:
  - id: "30_ruling_eligibility"
    title: "Eligibility Required"
    body: "You must be recruited from abroad and meet salary thresholds."
    severity: "warning"

# Override/add parameters
parameters:
  taxable_income_rate: 0.70              # Only 70% is taxable

# Override specific calculations
calculations:
  # This replaces the node with same id in base
  - id: taxable_income
    type: mul
    values:
      - "@gross_annual"
      - "$taxable_income_rate"

  # Remove a node that doesn't apply
  - id: some_inapplicable_credit
    $delete: true
```

---

## Test Vector Format

```json
{
  "name": "Single filer at median income",
  "description": "Standard case for single person earning €50,000",

  "inputs": {
    "gross_annual": 50000,
    "filing_status": "single"
  },

  "expected": {
    "net": 36250,
    "effective_rate": 0.275,

    "breakdown": {
      "income_tax": 15200,
      "social_security": 2750,
      "general_tax_credit": -2800,
      "labour_tax_credit": -1400
    }
  },

  "tolerance": 50,
  "tolerance_percent": 0.01,

  "sources": [
    {
      "description": "Verified against Belastingdienst calculator",
      "url": "https://www.belastingdienst.nl/...",
      "date": "2024-01-20"
    }
  ]
}
```

### Test Requirements

Each country/year config must include tests covering:

1. **Low income** - Below first bracket threshold
2. **Median income** - Typical case (~€50k-€80k depending on country)
3. **High income** - Above highest bracket threshold
4. **Each filing status** - At least one test per status
5. **Regional variations** - If region affects calculation
6. **Variant-specific** - Each variant needs its own tests

---

## Validation Rules

The engine validates configs against these rules:

1. **Schema validation** - All required fields present, correct types
2. **Reference resolution** - All `@input` and `$param` references exist
3. **DAG validation** - No circular dependencies (except via `function` nodes)
4. **Completeness** - All nodes referenced in `outputs.breakdown` have `category` and `label`
5. **Test coverage** - Minimum test vectors present and passing

---

## Appendix: Country Complexity Guide

| Country | Complexity | Notes |
|---------|------------|-------|
| UAE, SG, HK | Simple | No/minimal income tax |
| NL, AU, IE, UK | Moderate | Standard progressive + contributions |
| US | Moderate-High | Federal + State, FICA, many credits |
| CH | High | Federal + Canton + Municipality, 2000+ combinations |
| DE | High | Ehegattensplitting, Solidarity, Church tax |
| FR | High | Quotient familial, many social contributions |

---

## Appendix: Bracket Table Format

Brackets are evaluated as follows:

```
tax = 0
remaining = taxable_income

for each bracket (in threshold order):
  if remaining <= 0: break

  bracket_income = min(remaining, next_threshold - current_threshold)
  tax += bracket_income * rate + base_amount (if first euro in bracket)
  remaining -= bracket_income
```

Standard format:
```yaml
brackets:
  - threshold: 0        # Income from 0 to 10000
    rate: 0.10
  - threshold: 10000    # Income from 10000 to 50000
    rate: 0.20
  - threshold: 50000    # Income above 50000
    rate: 0.30
```

With base amounts (German-style):
```yaml
brackets:
  - threshold: 0
    rate: 0
    base_amount: 0
  - threshold: 11604
    rate: 0.14
    base_amount: 0       # Progressive zone starts
  - threshold: 17005
    rate: 0.2397
    base_amount: 756     # Fixed amount + marginal rate
```
