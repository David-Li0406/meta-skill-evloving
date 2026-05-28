---
name: sales-and-customer-service-training
description: Use this skill when you want to train in sales and customer service through product and customer management, role-play simulations, and strategy development.
---

# Skill body

## Commands

| Command | Description |
|---------|-------------|
| `add-product` | Add products/services to the database |
| `add-customer` | Add customer profiles |
| `add-operator` | Add sales/customer service strategies/operators |
| `list` | View current products, customers, and operators |
| `call` | Start sales or customer service call session |

## Workflow

```
add-product → add-customer → add-operator → call → review
     ↓             ↓              ↓           ↓
  Products     Customers      Operators    Call/Simulation
   stored       stored        stored     & Review
```

## add-product

Add products/services for training.

### Option A: Manual Input

Ask user for:
- **name**: Product/service name (required)
- **description**: What the product/service does
- **features**: Key features list
- **benefits**: Customer benefits
- **common_issues**: Typical problems customers encounter
- **solutions**: Standard resolutions for common issues
- **faq**: Frequently asked questions and answers
- **escalation_criteria**: When to escalate to supervisor
- **price**: Pricing information
- **target_audience**: Ideal customers
- **competitors**: Alternative products
- **objections**: Common customer objections and rebuttals

Save using: `uv run scripts/save_record.py --type product --data '<json>'`

### Option B: File Import

If user provides DOCX/PDF/XLSX file:

```bash
uv run scripts/import_data.py --type product --file <path> --output .ezagent/database/products
```

### Validation

After saving, confirm by listing:
```bash
ls -la .ezagent/database/products/
```

## add-customer

Add customer personas for training.

### Option A: Manual Input

Ask user for:
- **name**: Customer name (required)
- **type**: Customer type (new/returning/vip/frustrated)
- **role**: Job title
- **company**: Company description
- **industry**: Industry sector
- **background**: Customer background and history
- **issue_type**: Type of issue they're calling about
- **emotional_state**: angry/frustrated/confused/neutral/calm
- **pain_points**: Challenges they face
- **goals**: What they want to achieve
- **objections**: Typical concerns
- **communication_style**: How they prefer to interact
- **difficulty**: easy/medium/hard

Save using: `uv run scripts/save_record.py --type customer --data '<json>'`

### Option B: File Import

If user provides DOCX/PDF/XLSX file:

```bash
uv run scripts/import_data.py --type customer --file <path> --output .ezagent/database/customers
```