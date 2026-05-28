# Rule Engine Test Service Documentation

This document describes the implementation and usage of the Rule Engine Test Service (`testRuleEngine.groovy`) and the underlying Cancellation Sync logic executed by `RuleServices.groovy`.

## Overview

The Rule Engine POC is designed to validate business logic using Apache Drools. The current implementation focuses on reconciling Order statuses between two systems (e.g., Shopify and OMS) to identify synchronization issues, specifically regarding order cancellations.

### Key Components
1.  **Service**: `reconciliation.ReconciliationSampleServices.execute#Rules`
2.  **Implementation**: `RuleServices.groovy` (Compiles and executes DRL)
3.  **Test Script**: `testRuleEngine.groovy` (Generates synthetic data and invokes the service)

## Cancellation Sync Logic

The `RuleServices.groovy` defines hardcoded Drools rules (DRL) to check the state of orders passed in a data map.

### Rules
The following rules are applied to each order record:

1.  **Check Shopify Cancelled**: Flags if `cancelledAt` is not null.
2.  **Check OMS Cancelled**: Flags if `status_id` is `"ORDER_CANCELLED"`.
3.  **Sync Issue: Shopify Cancelled but OMS Active**:
    *   **Condition**: `cancelledAt != null` AND `status_id != "ORDER_CANCELLED"`
    *   **Action**: Sets `syncIssue = true` and populates `syncIssueReason`.
4.  **Sync Issue: OMS Cancelled but Shopify Active**:
    *   **Condition**: `cancelledAt == null` AND `status_id == "ORDER_CANCELLED"`
    *   **Action**: Sets `syncIssue = true` and populates `syncIssueReason`.

### Filtering
The service post-processes the Drools results to **return only records where `syncIssue` is true**. Synced records (both cancelled or both active) are filtered out.

## Testing with `testRuleEngine.groovy`

The test script generates synthetic data to verify the logic across 4 scenarios without relying on external bulk files.

### Scenarios Covered
| Scenario | Shopify (`cancelledAt`) | OMS (`status_id`) | Expected Result |
| :--- | :--- | :--- | :--- |
| **1. Synced Cancelled** | Present | `ORDER_CANCELLED` | **Filtered Out** (No Issue) |
| **2. Synced Active** | Null | `ORDER_APPROVED` | **Filtered Out** (No Issue) |
| **3. Mismatch (Shopify)** | Present | `ORDER_APPROVED` | **Returned** (Sync Issue) |
| **4. Mismatch (OMS)** | Null | `ORDER_CANCELLED` | **Returned** (Sync Issue) |

### How to Run

Run the test script from the command line using the Moqui ExecWar JAR.

**Note**: Ensure no other Moqui instance is using the same transaction logs (port 9090 default). If an instance is running, stop it first or run the script inside that instance's context if available.

```bash
java -jar moqui.war -T runtime/component/darpan/src/reconciliation/sample/testRuleEngine.groovy
```

### Expected Output

The script logs the preparation of synthetic records and the execution results. The final output list should contain exactly **2 records** (the mismatches).

```json
[
    {
        "legacyResourceId": "1003",
        "syncIssue": true,
        "syncIssueReason": "Shopify cancelled but OMS status is ORDER_APPROVED",
        ...
    },
    {
        "legacyResourceId": "1004",
        "syncIssue": true,
        "syncIssueReason": "OMS cancelled but Shopify active",
        ...
    }
]
```
