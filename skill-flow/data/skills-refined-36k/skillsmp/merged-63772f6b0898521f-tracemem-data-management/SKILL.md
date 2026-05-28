---
name: tracemem-data-management
description: Use this skill when you need to read, write, or understand data governance in TraceMem.
---

# Skill: TraceMem Data Management

## Purpose
This skill provides comprehensive instructions for reading and writing data within TraceMem's governance model, ensuring compliance with policies and best practices.

## When to Use
- When you need to create, update, or delete records in TraceMem.
- When you need to retrieve information or query specific records.
- When you are performing actions that affect the real world and require auditability.

## When NOT to Use
- Do not write data if you are in `propose` mode or if you have not evaluated relevant policies.
- Do not use TraceMem for scratchpad operations or temporary variable storage.
- Avoid using standard SQL libraries or HTTP clients for governed data access.

## Core Rules
- **Governance First**: Always check policies before performing any write operations. Use `decision_evaluate` to verify if your action is allowed.
- **Data Products Only**: Access data exclusively through named Data Products. Each product typically supports only one operation (read or write).
- **Purpose is Mandatory**: Every read and write operation must include a valid `purpose` string that aligns with the product's allowed purposes.
- **Immutable Records**: All actions are recorded in an immutable append-only trace. Do not store sensitive information in purpose fields or context summaries.

## Correct Usage Pattern

### For Writing Data
1. **Check Policy**: Call `decision_evaluate` with your proposed inputs. If the outcome is `deny`, stop. If `requires_exception`, request approval.
2. **Execute Write**: Call `decision_write` with:
   - `product`: The write-capable data product.
   - `purpose`: Valid purpose.
   - `mutation`: 
     - `operation`: one of `insert`, `update`, `delete`.
     - `records`: Array of objects to write.
3. **Verify Result**: Check the response for `status: "executed"` and capture any returned IDs if applicable.

### For Reading Data
1. **Identify the Product**: Use `products_list` to find the correct Data Product for your need. Check its schema and `allowed_purposes`.
2. **Execute Read**: Call `decision_read` with:
   - `decision_id`: Your current open decision.
   - `product`: The name of the data product.
   - `purpose`: A valid purpose string.
   - `query`: The key-value filter for your query.
3. **Handle Results**: Process the response containing `records` and `summary`.

## Common Mistakes
- **Ignoring Policy**: Attempting to write without checking policy can lead to blocked actions.
- **Wrong Product Usage**: Using a product designed for one operation type (e.g., `insert`) for another (e.g., `delete`).
- **Implicit Purpose**: Failing to provide a purpose or using an invalid one.

## Safety Notes
- **Idempotency**: Use `idempotency_key` for writes that may be retried.
- **Audit Trails**: All query parameters and actions are recorded for audit purposes.
- **Read-Before-Write**: Always read the current state before modifying it to ensure decisions are based on the latest data.