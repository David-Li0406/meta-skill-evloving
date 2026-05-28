---
name: tracemem-data-operations
description: Use this skill when you need to read or write data in TraceMem, ensuring compliance with governance policies and best practices.
---

# Skill body

## Purpose
This skill provides instructions for safely reading and writing data in TraceMem, emphasizing the importance of governance and policy checks.

## When to Use
- When you need to create, update, or delete records in TraceMem.
- When you need to retrieve information from TraceMem.
- When you are performing actions that affect the real world and require audit trails.

## Core Rules
- **Governance First**: Always check policies before performing any read or write operations. Use `decision_evaluate` to verify if your action is allowed.
- **Use Data Products**: Access data exclusively through named Data Products. Do not use direct database queries or API calls.
- **Purpose is Mandatory**: Every read and write operation must include a valid `purpose` string that aligns with the product's allowed purposes.
- **One Operation Per Product**: Ensure you are using the correct operation for the product (e.g., `insert`, `update`, `delete` for writes; `read` for reads).
- **Audit Trails**: All actions are recorded in an immutable trace. Avoid storing sensitive information in purpose fields or query parameters.

## Correct Usage Pattern

### For Writing Data
1. **Check Policy**:
   Call `decision_evaluate` with your proposed inputs. If the outcome is `deny`, stop. If `requires_exception`, request approval.

2. **Execute Write**:
   Call `decision_write` with:
   - `product`: The write-capable data product.
   - `purpose`: Valid purpose.
   - `mutation`:
     - `operation`: one of `insert`, `update`, `delete`.
     - `records`: Array of objects to write.
   
   *Example*:
   ```json
   {
     "product": "orders_insert",
     "mutation": {
       "operation": "insert",
       "records": [{"user_id": 5, "item": "sku-123"}]
     }
   }
   ```

3. **Verify Result**:
   Check the response for `status: "executed"`. Capture returned IDs if applicable.

### For Reading Data
1. **Identify the Product**:
   Use `products_list` to find the correct Data Product for your need. Check its schema and `allowed_purposes`.

2. **Execute Read**:
   Call `decision_read` with:
   - `decision_id`: Your current open decision.
   - `product`: The name of the data product.
   - `purpose`: A valid purpose string.
   - `query`: The key-value filter.

   *Example*:
   ```json
   {
     "decision_id": "decision_123",
     "product": "customers_read",
     "purpose": "verification",
     "query": {"user_id": "123"}
   }
   ```

3. **Handle Results**:
   The response will contain `records` and `summary`.

## Common Mistakes
- **Ignoring Policy**: Attempting to read or write without checking policy first.
- **Wrong Product Usage**: Using a product designed for one operation type for another (e.g., reading from an insert product).
- **Implicit Purpose**: Failing to provide a purpose or using an invalid one.

## Safety Notes
- **Read-Before-Write**: Always read the current state before modifying it to ensure decisions are based on the latest data.
- **Sensitive Data Handling**: Avoid including PII in query parameters unless explicitly allowed by the Data Product.