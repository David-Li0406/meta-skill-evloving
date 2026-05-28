---
name: marketing
description: Sales training and simulation system. Use when user wants to (1) add-product - add products to sell, (2) add-customer - add customer profiles, (3) add-operator - add sales strategies/operators, (4) call - start sales role-play simulation. Supports importing from DOCX, PDF, XLSX files. Data stored in .ezagent/database/marketing/.
---

# Marketing & Sales Training

Sales simulation system using SPIN selling methodology for training and practice.

## Commands

| Command | Description |
|---------|-------------|
| `add-product` | Add products to the database |
| `add-customer` | Add customer profiles |
| `add-operator` | Add sales strategies/operators |
| `call` | Start sales role-play simulation |

## Workflow

```
add-product → add-customer → add-operator → call → review
     ↓             ↓              ↓           ↓
  Products     Customers      Operators   Simulation
   stored       stored        stored      & Review
```

---

## add-product

Add products for sales training.

### Option A: Manual Input

Ask user for:
- **name**: Product name (required)
- **description**: What the product does
- **features**: Key features list
- **benefits**: Customer benefits
- **price**: Pricing information
- **target_audience**: Ideal customers
- **competitors**: Alternative products
- **objections**: Common customer objections and rebuttals

Save using: `uv run scripts/save_record.py --type product --data '<json>'`

### Option B: File Import

If user provides DOCX/PDF/XLSX file:

```bash
uv run scripts/import_data.py --type product --file <path> --output .ezagent/database/marketing/products
```

### Validation

After saving, confirm by listing:
```bash
ls -la .ezagent/database/marketing/products/
```

---

## add-customer

Add customer personas for role-play.

### Option A: Manual Input

Ask user for:
- **name**: Customer name (required)
- **role**: Job title
- **company**: Company description
- **industry**: Industry sector
- **pain_points**: Challenges they face
- **goals**: What they want to achieve
- **objections**: Typical concerns
- **communication_style**: How they prefer to interact
- **difficulty**: easy/medium/hard

For persona templates, see [references/customer-personas.md](references/customer-personas.md).

Save using: `uv run scripts/save_record.py --type customer --data '<json>'`

### Option B: File Import

```bash
uv run scripts/import_data.py --type customer --file <path> --output .ezagent/database/marketing/customers
```

---

## add-operator

Add sales strategies (operators) for training.

### Option A: Manual Input

Ask user for:
- **name**: Strategy name (required)
- **methodology**: SPIN, Challenger, Solution Selling, etc.
- **approach**: Overall selling approach
- **opening**: How to start conversations
- **discovery_questions**: Key questions to ask
- **objection_handling**: How to handle objections
- **closing_technique**: How to close deals
- **key_phrases**: Effective phrases to use

For SPIN methodology details, see [references/spin-selling.md](references/spin-selling.md).

Save using: `uv run scripts/save_record.py --type operator --data '<json>'`

### Option B: File Import

```bash
uv run scripts/import_data.py --type operator --file <path> --output .ezagent/database/marketing/operators
```

---

## call

Start a sales simulation session.

### Prerequisites

1. At least one product in `.ezagent/database/marketing/products/`
2. At least one customer in `.ezagent/database/marketing/customers/`
3. At least one operator in `.ezagent/database/marketing/operators/`

### Session Setup

1. List available options:
   ```bash
   ls .ezagent/database/marketing/products/
   ls .ezagent/database/marketing/customers/
   ls .ezagent/database/marketing/operators/
   ```

2. Ask user to select:
   - Product to sell
   - Customer persona to engage
   - Sales strategy to use

3. Load selected data:
   ```bash
   cat .ezagent/database/marketing/products/<selected>/info.json
   cat .ezagent/database/marketing/customers/<selected>/info.json
   cat .ezagent/database/marketing/operators/<selected>/info.json
   ```

4. Generate session ID: `session_<timestamp>`

### Role-Play Execution

**You become the customer.** The user is the salesperson.

Instructions:
- Adopt the customer persona completely
- Respond based on persona's communication style
- Raise objections naturally per persona profile
- React to SPIN questions appropriately
- If well-engaged, show increasing interest
- If poorly handled, become more resistant

**Session markers**:
- Start: "--- Sales Call Started ---"
- User can say "end call" or "exit" to finish

### Post-Call Review

After the call ends:

1. Analyze the conversation for:
   - **spin_usage**: How well were SPIN questions used?
   - **objection_handling**: How were objections addressed?
   - **rapport_building**: Was trust established?
   - **product_presentation**: Was the product positioned well?
   - **closing_attempt**: Was there a clear next step?
   - **strengths**: What went well
   - **improvements**: What to work on
   - **score**: Overall score 1-10

2. Save the review:
   ```bash
   uv run scripts/save_session.py \
     --session-id <session_id> \
     --product <product_name> \
     --customer <customer_name> \
     --operator <strategy_name> \
     --review '<json_review>'
   ```

3. Present the review to the user with actionable feedback.

---

## Database Structure

```
.ezagent/database/marketing/
├── products/
│   └── <id>_<name>/
│       ├── info.json
│       └── README.md
├── customers/
│   └── <id>_<name>/
│       ├── info.json
│       └── README.md
├── operators/
│   └── <id>_<name>/
│       ├── info.json
│       └── README.md
└── history/
    └── <session_id>/
        ├── session.json
        └── README.md
```

## SPIN Methodology Quick Reference

- **S**ituation: Current state questions (keep brief)
- **P**roblem: Pain point discovery
- **I**mplication: Consequence exploration (creates urgency)
- **N**eed-Payoff: Value articulation (customer sells themselves)

For detailed guidance, see [references/spin-selling.md](references/spin-selling.md).
