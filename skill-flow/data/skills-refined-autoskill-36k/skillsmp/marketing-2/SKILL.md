---
name: marketing
description: Sales training and practice system. Use when user wants to (1) add-product - add products to sell, (2) add-customer - add customer profiles, (3) add-operator - add sales strategies/operators, (4) list - view available products/customers/operators, (5) call - start sales call session. Supports importing from DOCX, PDF, XLSX files. Data stored in .ezagent/database/marketing/.
---

# Marketing & Sales Training

Sales training system using SPIN selling methodology for practice and improvement.

## Commands

| Command | Description |
|---------|-------------|
| `add-product` | Add products to the database |
| `add-customer` | Add customer profiles |
| `add-operator` | Add sales strategies/operators |
| `list` | View available products, customers, operators |
| `call` | Start sales call session |

## Workflow

```
add-product → add-customer → add-operator → call → review
     ↓             ↓              ↓           ↓
  Products     Customers      Operators    Sales
   stored       stored        stored      & Review
```

---

## add-product

Add products to sell.

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

Add customer profiles for sales practice.

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

Add sales strategies (operators).

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

## list

View current products, customers, and operators in the database.

### Execution

Extract and display names from all info.json files:

```bash
# List products
for f in .ezagent/database/marketing/products/*/info.json; do
  [ -f "$f" ] && cat "$f" | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1
done

# List customers
for f in .ezagent/database/marketing/customers/*/info.json; do
  [ -f "$f" ] && cat "$f" | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1
done

# List operators
for f in .ezagent/database/marketing/operators/*/info.json; do
  [ -f "$f" ] && cat "$f" | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1
done
```

### Output Format

Present results in a clear table:

```
Products:
- <product_name_1>
- <product_name_2>

Customers:
- <customer_name_1>
- <customer_name_2>

Operators:
- <operator_name_1>
- <operator_name_2>
```

If a category is empty, show "(none)".

---

## call

Start a sales call session.

### Step 1: Get User Input

Ask user to provide:
- **Product name**: Which product to sell
- **Customer name**: Which customer to engage
- **Operator/Strategy name**: Which sales strategy to use

### Step 2: Search Database

Search for each item by name in the database:

```bash
# Search for product (grep name in info.json files)
grep -rl '"name".*<product_name>' .ezagent/database/marketing/products/

# Search for customer
grep -rl '"name".*<customer_name>' .ezagent/database/marketing/customers/

# Search for operator
grep -rl '"name".*<operator_name>' .ezagent/database/marketing/operators/
```

**If any item is NOT found**: Stop and report which item(s) are missing. Do not proceed.

### Step 3: Load Data

Once all items are found, load their info:

```bash
cat <found_product_path>/info.json
cat <found_customer_path>/info.json
cat <found_operator_path>/info.json
```

Generate session ID: `session_<timestamp>`

### Step 4: Sales Call Execution

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

### Step 5: Post-Call Review

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
