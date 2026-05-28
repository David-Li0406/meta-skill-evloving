# Reconciliation POC (Sample Order Compare)

## Implementation Anchors (Current Repo)

- Service definition: `runtime/component/darpan/service/ReconciliationSampleServices.xml` (`compare#SampleOrderIds`)
- Script implementation: `runtime/component/darpan/src/reconciliation/sample/compareSampleOrderIds.groovy`
- Sample inputs: `runtime/component/darpan/data/sample/omsBulkData.json`, `runtime/component/darpan/data/sample/shopifyBulkData.json`

## 1. POC Objective

The objective of this POC is to validate the reconciliation approach using a narrowly scoped, high-value use case.

This POC will prove that:

- Data can be safely collected from multiple systems
- Reconciliation logic can be executed independently
- Results are clear and actionable

## 2. POC Scope

### In Scope

- Order creation reconciliation
- Shopify <-> OMS only (sample data)
- Presence validation of orders

### Out of Scope

- Fulfillment, returns, payments
- Real-time reconciliation
- Automated remediation
- Advanced reporting or alerting

## 3. Core Reconciliation Question

> Does `Shopify.legacyResourceId` exist in OMS as `EXTERNAL_ID`?

This single question defines the POC logic and success criteria for the sample service.

## 4. Systems Involved

- Shopify - Source of order creation (bulk export JSON)
- OMS - Downstream system expected to receive orders (bulk export JSON)
- Reconciliation Service - Standalone validation layer

## 5. Services Needed (POC Only)

- File drop endpoint for Shopify and OMS exports (SFTP or local drop)
- Ingestion job to load JSON exports into the reconciliation process
- Reconciliation engine to compare Shopify vs OMS by normalized `order_id`
- Reconciliation store to persist inputs and results
- Read-only results access (query or simple view)

## 6. Data Collection Approach (POC)

### Preferred Method: File-Based Ingestion

- JSON bulk exports from Shopify and OMS
- Files dropped to a known location (SFTP or local)
- Each reconciliation run processes:

  - One Shopify file
  - One OMS file

### Future-Compatible Alternatives

- REST APIs
- GraphQL queries

## 7. Standalone Architecture (POC)

- The reconciliation service will:

  - Run independently
  - Use its own database
  - Avoid querying or manipulating the commerce DB directly

This ensures:

- No production performance risk
- Safe handling of large datasets

## 8. Reconciliation Logic (POC)

1. Ingest Shopify order data
2. Ingest OMS order data
3. Store both datasets in reconciliation storage
4. Compare using normalized `order_id` as the primary key
5. Identify:

   - Orders present in Shopify but missing in OMS

## 9. Output and Results

The POC will produce:

- A queryable dataset or view
- Clear indicators for:

  - Matched orders
  - Missing OMS orders

The output should be simple, inspectable, and easy to validate.

## 10. Operational Flow

1. Data is received (JSON)
2. Data is persisted
3. Reconciliation logic runs
4. Results are stored and exposed

## 11. Pseudocode (compare#SampleOrderIds)

Inputs (defaults):
- omsLocation = component://darpan/data/sample/omsBulkData.json
- shopifyLocation = component://darpan/data/sample/shopifyBulkData.json
- omsOrderIdField = EXTERNAL_ID
- shopifyOrderIdField = legacyResourceId
- orderIdField = shopify_order_id
- logInputCounts = true
- sparkMaster = local[*]
- sparkAppName = ReconciliationSampleOrderCompare

Pseudocode:
1) Resolve omsLocation and shopifyLocation to local paths or URLs.
2) Read OMS JSON and select omsOrderIdField as order_id.
3) Read Shopify JSON and select shopifyOrderIdField as order_id.
   - If payload contains data.orders.edges, explode edges and use edge.node.<field>.
4) Trim, filter null/blank, drop duplicates on both sets.
5) If logInputCounts: count each set and log.
6) onlyInOms = omsDf left_anti join shopifyDf on order_id.
7) onlyInShopify = shopifyDf left_anti join omsDf on order_id.
8) Collect results into arrays and return counts.

Assumptions (POC):
- Shopify and OMS exports cover the same time window.
- Order IDs are stable and comparable between systems.
- Reconciliation runs independently of Shopify/OMS databases.
- Output is returned in memory for the sample service.

## 12. POC Success Criteria

The POC is successful if:

- Shopify and OMS data can be reconciled independently
- Missing orders are reliably identified
- No impact occurs on core commerce systems
- The approach is clearly extensible to future use cases
