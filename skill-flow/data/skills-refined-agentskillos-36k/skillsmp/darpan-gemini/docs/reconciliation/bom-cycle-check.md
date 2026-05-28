# BOM Cycle Check

Detect reciprocal (cyclic) BOM relationships before import and split the input file into importable rows and rows that would create loops.

## Service

### `BomServices.run#BomCycleCheck`

Separates a BOM CSV into two outputs:
- **Importable file**: Original columns only; rows that do not participate in a cycle.
- **Problem file**: Rows that form a cycle (mutual or self-reference) with extra columns `error_reason` and `cycle_description` when a header is present. `cycle_description` is written in human-readable form, e.g., `Cycle among A, B, C (path: A -> B -> C -> A)` or `Self relationship on A`.

**Key inputs**
- `bomFile` (FileItem) or `bomLocation` (component://, runtime://, or absolute path)
- `hasHeader` (default `true`) and `delimiter` (default `,`)
- Column hints: `parentFieldName` (default `product-sku`), `componentFieldName` (default `product-sku-to`)
- Optional `assocTypeFilter` to include only a specific association type (e.g., `PRODUCT_COMPONENT`)

**Outputs**
- `importableFileName` / `problemFileName`
- `importableLocation` / `problemLocation` (under `runtime://tmp/bom/cycle-check/output` by default)
- Counts: `importableRowCount`, `problemRowCount`, `totalRowCount`, `cycleCount`, `skippedRowCount`
- `cycleGroups`: list of detected cycle node sets

**Example**

```xml
<service-call name="BomServices.run#BomCycleCheck">
    <field-map field-name="bomLocation" value="component://darpan/data/SOC_BOM_KTO.csv"/>
    <field-map field-name="assocTypeFilter" value="PRODUCT_COMPONENT"/>
    <field-map field-name="hasHeader" value="true"/>
</service-call>
```

The outputs are written to `runtime://tmp/bom/cycle-check/output` with filenames like `SOC_BOM_KTO.csv-importable-20240601-120000.csv` and `SOC_BOM_KTO.csv-errors-20240601-120000.csv`.

## Screen

Navigate to **Reconciliation → BOM Cycle Check** to upload a BOM file (or reference an existing location), optionally filter by association type, and download the two generated CSVs. The page lists all generated outputs and highlights the last run counts (importable, problem, cycles).

## Detection notes

- Cycles are identified using strongly connected components (including self-references). Only rows that are part of a cycle are placed in the problem file.
- Rows missing parent/component values or filtered out by `assocTypeFilter` are skipped and not written to either output.
- The importable file preserves the input column set so it can be used directly for BOM load. The problem file adds human-readable context columns to help remediate loops.
