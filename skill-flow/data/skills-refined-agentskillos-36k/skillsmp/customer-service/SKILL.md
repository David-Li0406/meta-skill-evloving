---
name: customer-service
description: Customer service training and practice system. Use when user wants to (1) add-product - add products/services to serve, (2) add-customer - add customer profiles, (3) add-operator - add service strategies/operators, (4) call - start customer service call session, (5) list - view current products, customers, and operators. Supports importing from DOCX, PDF, XLSX files. Data stored in .ezagent/database/customer_service/.
---

# Customer Service Training

Customer service training and practice system based on industry best practices including active listening, empathy-driven responses, and effective problem resolution.

## Commands

| Command | Description |
|---------|-------------|
| `add-product` | Add products/services to the database |
| `add-customer` | Add customer profiles |
| `add-operator` | Add service strategies/operators |
| `list` | View current products, customers, and operators |
| `call` | Start customer service call session |

## Workflow

```
add-product → add-customer → add-operator → call → review
     ↓             ↓              ↓           ↓
  Products     Customers      Operators    Call
   stored       stored        stored     & Review
```

---

## add-product

Add products/services for customer service training.

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
- **type**: Customer type (new/returning/vip/frustrated)
- **background**: Customer background and history
- **issue_type**: Type of issue they're calling about
- **emotional_state**: angry/frustrated/confused/neutral/calm
- **communication_style**: verbose/brief/technical/non-technical
- **expectations**: What they expect from the call
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

Add service strategies (operators) for training.

### Option A: Manual Input

Ask user for:
- **name**: Strategy name (required)
- **methodology**: HEAR, LAST, LEARN, or custom approach
- **greeting**: How to open the call
- **discovery_questions**: Key questions to understand the issue
- **empathy_phrases**: Phrases to show understanding
- **resolution_steps**: Standard problem-solving process
- **objection_handling**: How to handle difficult situations
- **closing_technique**: How to end calls professionally
- **follow_up**: Post-call actions

For methodology details, see [references/service-methodologies.md](references/service-methodologies.md).

Save using: `uv run scripts/save_record.py --type operator --data '<json>'`

### Option B: File Import

```bash
uv run scripts/import_data.py --type operator --file <path> --output .ezagent/database/customer_service/operators
```

---

## list

View current products, customers, and operators in the database.

### Usage

```bash
# List all records (summary)
uv run scripts/list_records.py

# List specific type
uv run scripts/list_records.py --type product
uv run scripts/list_records.py --type customer
uv run scripts/list_records.py --type operator

# Show detailed information
uv run scripts/list_records.py --verbose

# Output as JSON
uv run scripts/list_records.py --json
```

### Output Example

```
## 产品/服务 (2)
----------------------------------------
  1. 智能手表 (ID: 8fc94b13, 创建: 2026-01-23)
  2. 云存储服务 (ID: a1b2c3d4, 创建: 2026-01-22)

## 客户角色 (3)
----------------------------------------
  1. 张伟 (ID: e5f6g7h8, 创建: 2026-01-23)
  2. 李明 (ID: i9j0k1l2, 创建: 2026-01-22)
  3. 王阿姨 (ID: m3n4o5p6, 创建: 2026-01-21)

## 客服策略 (2)
----------------------------------------
  1. HEAR方法 (ID: q7r8s9t0, 创建: 2026-01-23)
  2. LAST方法 (ID: u1v2w3x4, 创建: 2026-01-22)

总计: 7 条记录
```

---

## call

Start a customer service call session.

### Required Parameters

User MUST provide the following three parameters:
- **product**: Name of the product/service to support
- **customer**: Name of the customer persona
- **operator**: Name of the service strategy to use

Example: `call --product "智能手表" --customer "张伟" --operator "HEAR方法"`

### Session Setup

1. **Require user to specify**: product name, customer name, and operator name
   - Do NOT list available options first
   - Do NOT check if directories are empty
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
   - Example: "错误：未找到产品 '智能手表'。请先使用 add-product 添加该产品。"

4. **If all data found**: Load the JSON files and proceed

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
- Start: "--- 客服电话已接通 ---"
- Opening: "[电话铃响...] 喂？是客服吗？"
- User can say "结束通话" or "exit" to finish

### Post-Call Review

After the call ends:

1. Read the conversation history from `.ezagent/history/` for the current session

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

## Service Methodology Quick Reference

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

For detailed guidance, see [references/service-methodologies.md](references/service-methodologies.md).
