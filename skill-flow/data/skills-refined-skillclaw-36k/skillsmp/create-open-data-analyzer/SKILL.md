---
name: Create Open Data Analyzer
description: Workflow to build new analysis pipelines for external government datasets (Peru Compras / Open Data).
version: 1.0.0
---

# Skill: Create Open Data Analyzer

This skill is for adding new processing capabilities to the `open-data` module.
It handles the ingestion, parsing, and visualization of large datasets (usually CSVs from government portals).

## Execution Steps

### 1. Data Contract Definition
Locate `lib/open-data.ts`.
- **Action**: Define a TypeScript interface for the new raw data structure.
- *Example*:
```typescript
export interface RawOcamEntry {
  "RUC PROVEEDOR": string;
  "MONTO TOTAL": string; // Note: Raw data is often string
  "FECHA FORMALIZACION": string;
  // ...
}
```

### 2. Processing Logic
Create/Edit `lib/open-data-processing.ts`.
Implement a normalization function that converts Raw Strings -> Typed Objects (Numbers, Dates).

```typescript
export function normalizeOcamData(raw: RawOcamEntry[]): NormalizedEntry[] {
  return raw.map(item => ({
    amount: parseFloat(item["MONTO TOTAL"]),
    vendor: item["RUC PROVEEDOR"],
    date: parse(item["FECHA FORMALIZACION"], "dd/MM/yyyy", new Date())
  }))
}
```

### 3. Analysis Functions
Implement specific business logic questions as pure functions.
- *Top Vendors*: Sort by total amount.
- *Price Trends*: Group by month/week.
- *Competitor Analysis*: Filter by specific RUCs defined in `competitor_matrix` table.

### 4. API Endpoint (server-side)
Since datasets are large, processing should happen on the server.
- Create `app/api/open-data/[analysis-type]/route.ts`.
- This route should accept filters (Date Range, Category) and return the JSON ready for the chart.

### 5. Visualization Component
Create `components/open-data/[analysis-name]-chart.tsx`.
- Use `recharts`.
- Input: The processed JSON from the API.
- Output: BarChart, LineChart, or DataTable.

## Agent Check
- [ ] Did you handle messy data? (NaNs, Invalid Dates).
- [ ] Is the processing efficient? (Avoid nested loops on large arrays if possible).
