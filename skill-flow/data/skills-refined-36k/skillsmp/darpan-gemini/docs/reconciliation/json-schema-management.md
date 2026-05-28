# JSON Schema Management

## Overview

Darpan provides comprehensive tooling to manage JSON Schemas, which are essential for validating data and defining ID paths for reconciliation.

## Key Features

- **Schema Repository**: Centralized storage of JSON schemas in `runtime/schemas/json/`.
- **Schema Wizard**: Interactive tool to generate schemas from sample JSON files.
- **Schema Editor**: Visual editor to refine schemas, set data types, and mark required fields.
- **Validation**: Validate any JSON file against a stored schema.

## Organization

Schemas are managed using **Schema Names** (human-readable identifiers) rather than raw filenames. While the underlying files are stored on disk, the system abstracts this to provide a user-friendly experience.

- **Storage Location**: `runtime/schemas/json/`
- **Naming Convention**: `[schemaName].schema.json`

## specialized Tools

### 1. JSON Schema Wizard

The Wizard simplifies the creation of new schemas, especially for complex or nested JSON structures.

**Process:**
1.  **Upload Sample**: Upload a representative JSON file (e.g., specific order export).
2.  **Inference**: The system analyzes the JSON structure.
    *   *Streaming & Sampling*: For large files, the system samples data to prevent memory issues.
    *   *Recursion Handling*: Circular references and deep nesting are handled gracefully.
3.  **Refinement**: You can review the inferred fields in a flat list view.
4.  **Generation**: The final standard JSON Schema (Draft 7) is generated and saved.

### 2. Schema Editor

Allows maintenance of existing schemas without editing raw JSON.

- **Tree/List View**: View schema properties in a hierarchical or flat list.
- **Edit Types**: Change property types (String, Integer, Boolean, etc.).
- **Required Fields**: Toggle required status for validation.
- **Description**: Add documentation to fields.

## Services

*   `JsonSchemaServices.create#JsonSchemaFromJson`: Creates a new schema from a JSON file.
*   `JsonSchemaServices.infer#JsonSchema`: Infers structure for the wizard.
*   `JsonSchemaServices.validate#JsonFileAgainstSchema`: Validates an uploaded file.
*   `JsonSchemaServices.resolve#JsonPathForKey`: Helper to find JSONPaths for specific keys (e.g., finding `$.data.orders[*].id` given just `id`).

## Best Practices

*   **Use Descriptive Names**: Naming schemas like "Shopify Orders" is better than `shopify_orders_v1.json`.
*   **Keep Samples Small**: While the tool handles large files, smaller representative samples yield faster inference.
*   **Validate Frequently**: Use the validation tools to ensure your data sources match your expectations.
