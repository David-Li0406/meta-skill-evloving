# JSON Reconciliation

## Overview

The JSON reconciliation feature allows you to compare two JSON files using ID-based comparison and identify differences. The reconciliation validates both files against a JSON schema and outputs a detailed report with full object data preserved.

## Key Features

- **Schema Validation**: Validates both JSON files against a JSON Schema before reconciliation
- **ID-based Comparison**: Uses JSONPath expressions to extract identifiers from complex nested structures
- **Full Object Preservation**: Returns complete JSON objects for missing/mismatched data
- **Detailed Output**: JSON format with metadata, summary statistics, and full difference details

## Services

### `ReconciliationGenericServices.reconcile#GenericFiles`

Primary entry point for uploads. It stages files, then delegates to the shared router so upload and automation paths stay aligned.

**Input Parameters:**
- `file1` (FileItem, required): First file (CSV or JSON)
- `file2` (FileItem, required): Second file (CSV or JSON)
- `file1SystemEnumId` (required): Identifier for the source system of file 1
- `file2SystemEnumId` (required): Identifier for the source system of file 2
- `reconciliationMappingId` (required): Configuration ID that defines schemas and ID paths
- `sparkMaster` (optional): Spark master URL (default: "local[*]")

**Output:**
- `reconciliationType`: "CSV", "JSON", or "MIXED"
- `differenceCount`: Total differences found
- `diffLocation` / `diffFileName`: Path to the generated results
- `validationErrors`: Any schema validation errors found
- `processingWarnings`: Any normalization fallbacks that were applied

### `ReconciliationCoreServices.reconcile#FilesByMapping`

Shared router used by both Generic uploads and SFTP automation. It normalizes staged file locations, resolves mapping metadata (types, schemas, ID fields), and hands everything to the unified comparator.

**Inputs (key):** `reconciliationMappingId`, `file1Location`, `file2Location`, `file1SystemEnumId`, `file2SystemEnumId`, optional `file1Name`/`file2Name`, `file1FileTypeEnumId`/`file2FileTypeEnumId`, `file1SchemaFileName`/`file2SchemaFileName`, `hasHeader`, `outputLocation`, `sparkMaster`, `sparkAppName`.

**Outputs (key):** `file1Type`, `file2Type`, `reconciliationType`, `diffLocation`, `diffFileName`, `differenceCount`, `onlyInFile1Count`, `onlyInFile2Count`, `validationErrors`, `processingWarnings`.

### `ReconciliationCoreServices.reconcile#UnifiedFiles`

Single reconciliation engine for all file type combinations. It converts CSV/JSON inputs into a normalized Spark structure, runs the compare once, and always emits a JSON diff. The legacy CSV/JSON/Mixed services are now wrappers only.

**Inputs (key):** `file1Location`, `file2Location`, `file1Type`, `file2Type`, `file1IdField`/`file2IdField` (or `file1IdExpression`/`file2IdExpression`), `file1SchemaFileName`/`file2SchemaFileName` for JSON sources, `hasHeader`, `outputLocation`, `sparkMaster`, `sparkAppName`.

**Outputs (key):** `reconciliationType`, `diffLocation`, `diffFileName`, `differenceCount`, `onlyInFile1Count`, `onlyInFile2Count`, `validationErrors`, `processingWarnings`.

> **Note**: Direct usage of `ReconciliationJsonServices.reconcile#JsonFiles` is supported but the Generic service is preferred for UI integration.

## Schema Management

For details on creating and managing schemas used in reconciliation, see [JSON Schema Management](json-schema-management.md).


## JSONPath Expression

The `compareJsonPath` parameter uses JSONPath syntax to extract ID values from your JSON structure.

When a schema is provided and you pass a simple key (like `id` or `$.id`), the resolver expands it to the full JSONPath. For array-root schemas this becomes `$[*].id`.

### Examples

**Simple ID field at root:**
```
$.id
```

**Nested object:**
```
$.data.orderId
```

**Array of objects:**
```
$[*].id
```

**Deeply nested in array:**
```
$[*].data.orders.edges[*].node.legacyResourceId
```

## Output Format

The reconciliation output is a JSON file with the following structure:

```json
{
  "metadata": {
    "timestamp": "2026-01-02T12:00:00Z",
    "json1Label": "Orders File 1",
    "json2Label": "Orders File 2",
    "schemaFileName": "orders.schema.json",
    "compareJsonPath": "$[*].data.orders.edges[*].node.legacyResourceId",
    "validationPassed": true
  },
  "summary": {
    "totalDifferences": 4,
    "onlyInJson1Count": 2,
    "onlyInJson2Count": 2
  },
  "validationErrors": [],
  "differences": [
    {
      "type": "missing_in_json2",
      "id": "6470622019715",
      "presentIn": "Orders File 1",
      "missingIn": "Orders File 2",
      "data": {
        "legacyResourceId": "6470622019715",
        "id": "gid://shopify/Order/6470622019715",
        "name": "#GOR195874999",
        ...
      },
      "note": "Present in Orders File 1, missing in Orders File 2"
    }
  ]
}
```

## Usage Example

### Via Service Call

```xml
<service-call name="ReconciliationJsonServices.reconcile#JsonFiles">
    <field-map field-name="json1Location" value="component://darpan/data/orders-shopify.json"/>
    <field-map field-name="json2Location" value="component://darpan/data/orders-oms.json"/>
    <field-map field-name="schemaFileName" value="orders.schema.json"/>
    <field-map field-name="compareJsonPath" value="$[*].data.orders.edges[*].node.legacyResourceId"/>
    <field-map field-name="json1Label" value="Shopify Orders"/>
    <field-map field-name="json2Label" value="OMS Orders"/>
</service-call>
```

### Via File Upload Screen

1. Upload both JSON files
2. Select the JSON schema to validate against
3. Enter the JSONPath expression for the ID field
4. Optionally provide labels for the files
5. Submit to run reconciliation
6. Download the results JSON file
7. Use **View** next to a JSON result to see the summary and separate lists for records missing in each JSON file (with full order JSON payloads)

## Testing

Test files are located in `data/test/`:
- `test-orders-1.json`: Sample orders (3 orders)
- `test-orders-2.json`: Sample orders (3 orders, 1 overlapping)
- `test-json-reconciliation.groovy`: Test script

Schema: `runtime://schemas/json/test-orders.schema.json`

**Expected Results:**
- 2 orders only in file 1
- 2 orders only in file 2
- 1 order in both (should not appear in differences)

## Notes

- Schema validation is performed first; reconciliation continues even if validation fails
- For JSON array roots, validation reads the full array for small files and samples the first element for large payloads to reduce memory usage
- The reconciliation uses ID-based comparison (like CSV reconciliation)
- Full objects are preserved in the output for data analysis
- JSONPath library (`com.jayway.jsonpath:json-path:2.8.0`) is required
- Schema parsing for validation/generation uses Jackson ObjectMapper to avoid ad-hoc JSON handling
- Diff detail view streams large diff files and paginates missing-record lists independently (default 20 per page) using Moqui controls to keep previews responsive
- Diff detail view includes a Spark-backed record_id search (LIKE-based, full-file filter before pagination; auto-resets to the first page if the current page is beyond the filtered results)
- Schema generation requires non-empty JSON input files; empty uploads are rejected
- What changed: Diff View is hidden from the navigation menu and is accessed from the generated file list under File Reconciliation (direct `/Reconciliation/GenericReconciliationView` access removed)
- What changed: Simple ID keys are resolved against array-root schemas (e.g., `id` -> `$[*].id`) and small array payloads are fully validated before sampling large ones
- What changed: Schema generation in non-strict mode merges array item shapes to keep schemas compact instead of emitting large `anyOf` lists
