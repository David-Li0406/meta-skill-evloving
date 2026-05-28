---
name: customer-sales-training
description: Use this skill when you want to train in customer service and sales through adding products, customers, and operators, and simulating calls.
---

# Customer Service and Sales Training

A comprehensive training system for customer service and sales using various methodologies, including SPIN selling and best practices for customer interactions.

## Commands

| Command | Description |
|---------|-------------|
| `add-product` | Add products/services to the database |
| `add-customer` | Add customer profiles |
| `add-operator` | Add service/sales strategies/operators |
| `list` | View current products, customers, and operators |
| `call` | Start customer service or sales call session |

## Workflow

```
add-product → add-customer → add-operator → call → review
     ↓             ↓              ↓           ↓
  Products     Customers      Operators    Call/Simulation
   stored       stored        stored     & Review
```

---

## add-product

Add products/services for training.

### Option A: Manual Input

Ask user for:
- **name**: Product/service name (required)
- **description**: What the product/service does
- **features**: Key features list
- **common_issues**: Typical problems customers encounter
- **solutions**: Standard resolutions for common issues
- **faq**: Frequently asked questions and answers
- **escalation_criteria**: When to escalate to supervisor
- **sla**: Service level agreements (response time, resolution time)

Save using: `uv run scripts/save_record.py --type product --data '<json>'`

### Option B: File Import

If user provides DOCX/PDF/XLSX file:

```bash
uv run scripts/import_data.py --type product --file <path> --output .ezagent/database/customer_service/products
```

### Validation

After saving, confirm by listing:
```bash
ls -la .ezagent/database/customer_service/products/
```

---

## add-customer

Add customer personas for training.

### Option A: Manual Input

Ask user for:
- **name**: Customer name (required)
- **type/role**: Customer type (new/returning/vip/frustrated) or job title
- **background/company**: Customer background and history or company description
- **issue_type/pain_points**: Type of issue they're calling about or challenges they face
- **emotional_state/goals**: angry/frustrated/confused/neutral/calm or what they want to achieve
- **communication_style**: verbose/brief/technical/non-technical
- **expectations/objections**: What they expect from the call or typical concerns
- **difficulty**: easy/medium/hard
- **special_needs**: Any accessibility or language considerations

For persona templates, see [references/customer-personas.md](references/customer-personas.md).

Save using: `uv run scripts/save_record.py --type customer --data '<json>'`

### Option B: File Import

```bash
uv run scripts/import_data.py --type customer --file <path> --output .ezagent/database/customer_service/customers
```

---

## add-operator

Add service/sales strategies (operators) for training.

### Option A: Manual Input

Ask user for:
- **name**: Strategy name (required)
- **methodology**: HEAR, LAST, SPIN, Challenger, Solution Selling, or custom approach
- **greeting/opening**: How to open the call or start conversations
- **discovery_questions**: Key questions to understand the issue or ask
- **empathy_phrases/objection_handling**: Phrases to show understanding or how to handle objections
- **resolution_steps/closing_technique**: Standard problem-solving process or how to close deals
- **follow_up/key_phrases**: Post-call actions or effective phrases to use

For methodology details, see [references/service-methodologies.md](references/service-methodologies.md).

Save using: `uv run scripts/save_record.py --type operator --data '<json>'`

### Option B: File Import

```bash
uv run scripts/import_data.py --type operator --file <path> --output .ezagent/database/customer_service/operators
```

---

## list

View current products, customers, and operators in the database.

### Execution

Extract and display names from all info.json files:

```bash
# List products
for f in .ezagent/database/customer_service/products/*/info.json; do
  [ -f "$f" ] && cat "$f" | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1
done

# List customers
for f in .ezagent/database/customer_service/customers/*/info.json; do
  [ -f "$f" ] && cat "$f" | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1
done

# List operators
for f in .ezagent/database/customer_service/operators/*/info.json; do
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

Start a customer service or sales call session.

### Required Parameters

User MUST provide the following three parameters:
- **product**: Name of the product/service to support
- **customer**: Name of the customer persona
- **operator**: Name of the service/sales strategy to use

Example: `call --product "<product_name>" --customer "<customer_name>" --operator "<strategy_name>"`

### Session Setup

1. **Require user to specify**: product name, customer name, and operator name
   - Do NOT list available options first
   - User must explicitly provide the names

2. **Search for specified data** in `.ezagent/database/customer_service/`:
   ```bash
   # Search for product by name (partial match)
   find .ezagent/database/customer_service/products -name "info.json" -exec grep -l "<product_name>" {} \;

   # Search for customer by name (partial match)
   find .ezagent/database/customer_service/customers -name "info.json" -exec grep -l "<customer_name>" {} \;

   # Search for operator by name (partial match)
   find .ezagent/database/customer_service/operators -name "info.json" -exec grep -l "<operator_name>" {} \;
   ```

3. **If any data is NOT FOUND**: Report error and stop. Do not proceed.

4. **If all data found**: Load the JSON files and proceed.

5. **Generate session ID**: `session_<YYYYMMDD>_<HHMMSS>`

### Call Execution

**You become the customer calling in.** The user is the service representative.

Instructions:
- Adopt the customer persona completely
- Start with the issue defined in the persona
- Match the emotional state specified
- React based on how well the user handles the situation
- If user shows empathy and competence, gradually calm down
- If user is dismissive or unhelpful, become more frustrated
- Present objections and follow-ups realistically

**Session markers**:
- Start: "--- Call Started ---"
- User can say "结束通话" or "exit" to finish

### Post-Call Review

After the call ends:

1. Read the conversation history from `.ezagent/history/` for the current session.

2. Analyze the conversation for:
   - **greeting_quality**: How well did they open the call?
   - **active_listening**: Did they understand the issue before responding?
   - **empathy_shown**: Were they compassionate and understanding?
   - **problem_resolution**: Was the issue effectively resolved?
   - **communication_clarity**: Was information clear and understandable?
   - **professionalism**: Was the tone appropriate throughout?
   - **closing_quality**: Was the call ended properly?
   - **strengths**: What went well
   - **improvements**: What to work on
   - **score**: Overall score 1-10

3. Save the review:
   ```bash
   uv run scripts/save_session.py \
     --session-id <session_id> \
     --product <product_name> \
     --customer <customer_name> \
     --operator <strategy_name> \
     --review '<json_review>'
   ```

4. Present the review to the user with actionable feedback.

---

## Database Structure

```
.ezagent/database/customer_service/
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

## Service and Sales Methodology Quick Reference

### HEAR Method
- **H**ear: Listen without interrupting
- **E**mpathize: Acknowledge their feelings
- **A**pologize: Take responsibility appropriately
- **R**esolve: Fix the problem or provide next steps

### LAST Method
- **L**isten: Understand the full issue
- **A**pologize: Express genuine regret
- **S**olve: Provide a solution
- **T**hank: Thank them for their patience

### SPIN Methodology
- **S**ituation: Current state questions (keep brief)
- **P**roblem: Pain point discovery
- **I**mplication: Consequence exploration (creates urgency)
- **N**eed-Payoff: Value articulation (customer sells themselves)

For detailed guidance, see [references/service-methodologies.md](references/service-methodologies.md) and [references/spin-selling.md](references/spin-selling.md).