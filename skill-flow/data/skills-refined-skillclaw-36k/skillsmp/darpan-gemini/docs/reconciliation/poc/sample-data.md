# POC Sample Data

The sample compare service reads JSON files from `runtime/component/darpan/data/sample`.

## Files and Fields

- `runtime/component/darpan/data/sample/omsBulkData.json`
  - OMS bulk export as a JSON array.
  - Order ID field used by default: `EXTERNAL_ID`.
- `runtime/component/darpan/data/sample/shopifyBulkData.json`
  - Shopify bulk export in GraphQL format.
  - Order ID field used by default: `data.orders.edges[].node.legacyResourceId`.
- `runtime/component/darpan/data/sample/omsData.json`
  - Simplified OMS sample array.
  - Order ID field: `shopify_order_id`.
- `runtime/component/darpan/data/sample/shopifyData.json`
  - Simplified Shopify sample array.
  - Order ID field: `shopify_order_id`.

## Usage Notes

- The service `compare#SampleOrderIds` (defined in `runtime/component/darpan/service/ReconciliationSampleServices.xml`)
  defaults to `omsBulkData.json` and `shopifyBulkData.json`.
- Override `omsOrderIdField`, `shopifyOrderIdField`, or `orderIdField` to point at alternate fields.
- The script (`runtime/component/darpan/src/reconciliation/sample/compareSampleOrderIds.groovy`) detects the bulk GraphQL shape
  and falls back to a flat JSON array when the `data` wrapper is not present.
