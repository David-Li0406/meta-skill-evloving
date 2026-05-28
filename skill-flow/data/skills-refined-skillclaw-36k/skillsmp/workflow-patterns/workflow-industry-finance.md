---
name: workflow-industry-finance
description: "Finance industry workflows (payments, fraud, compliance). Use when asking 'finance workflow', 'payment processing', 'fraud detection', or 'financial compliance'."
---

# Finance Industry Workflows

> **Skill Metadata**
> Category: `industry-workflows`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Pattern: Payment Processing with Fraud Detection

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# 1. Validate payment details
workflow.add_node("DataValidationNode", "validate", {
    "input": "{{input.payment}}",
    "schema": {"amount": "decimal", "card_number": "credit_card"}
})

# 2. Fraud check
workflow.add_node("APICallNode", "fraud_check", {
    "url": "https://api.fraudcheck.com/analyze",
    "method": "POST",
    "body": "{{validate.valid_data}}"
})

# 3. Risk assessment
workflow.add_node("ConditionalNode", "assess_risk", {
    "condition": "{{fraud_check.risk_score}}",
    "branches": {
        "low": "process_payment",
        "medium": "manual_review",
        "high": "reject_payment"
    }
})

# 4. Process payment
workflow.add_node("APICallNode", "process_payment", {
    "url": "https://api.paymentgateway.com/charge",
    "method": "POST",
    "body": "{{validate.valid_data}}"
})

# 5. Record transaction
workflow.add_node("DatabaseExecuteNode", "record", {
    "query": "INSERT INTO transactions (amount, status, timestamp) VALUES (?, ?, NOW())",
    "parameters": ["{{input.amount}}", "completed"]
})

workflow.add_connection("validate", "fraud_check")
workflow.add_connection("fraud_check", "assess_risk")
workflow.add_connection("assess_risk", "process_payment", "low")
workflow.add_connection("process_payment", "record")
```

<!-- Trigger Keywords: finance workflow, payment processing, fraud detection, financial compliance -->
