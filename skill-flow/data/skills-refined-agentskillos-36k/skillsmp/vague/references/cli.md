# Vague CLI Reference

## Basic Usage

```bash
# Generate data from a .vague file
node dist/cli.js <file.vague>

# With seed for reproducible output
node dist/cli.js <file.vague> --seed 123
```

## Output Formats

```bash
# JSON output (default)
node dist/cli.js data.vague -o output.json

# CSV output
node dist/cli.js data.vague -f csv -o output.csv

# CSV with semicolon delimiter
node dist/cli.js data.vague -f csv --csv-delimiter ";" -o output.csv

# CSV without header row
node dist/cli.js data.vague -f csv --csv-no-header -o output.csv
```

CSV Options:
- `-f, --format <fmt>`: Output format (`json` or `csv`)
- `--csv-delimiter <char>`: Field delimiter (default: `,`)
- `--csv-no-header`: Omit header row
- `--csv-arrays <mode>`: Array handling (`json`, `first`, `count`)
- `--csv-nested <mode>`: Nested object handling (`flatten`, `json`)

For multiple collections with CSV output:
- Single collection: writes to specified file
- Multiple collections: creates separate files (`output_users.csv`, `output_orders.csv`)

## Schema Validation

Validate generated data against an OpenAPI spec:

```bash
# Validate against OpenAPI spec
node dist/cli.js data.vague -v openapi.json -m '{"invoices": "Invoice"}'

# Validate only (exit code 1 on failure)
node dist/cli.js data.vague -v openapi.json -m '{"invoices": "Invoice"}' --validate-only
```

Options:
- `-v, --validate <spec>`: OpenAPI spec file to validate against
- `-m, --mapping <json>`: Map collection names to schema names
- `--validate-only`: Only validate, don't output data

## OpenAPI Example Population

Generate realistic examples and embed them in an OpenAPI spec:

```bash
# Populate OpenAPI spec with inline examples (bundled)
node dist/cli.js data.vague --oas-output api-with-examples.json --oas-source api.json

# With explicit mapping (collection -> schema)
node dist/cli.js data.vague --oas-output api.json --oas-source api.json -m '{"invoices": "Invoice"}'

# Multiple examples per schema
node dist/cli.js data.vague --oas-output api.json --oas-source api.json --oas-example-count 3

# External file references instead of inline examples
node dist/cli.js data.vague --oas-output api.json --oas-source api.json --oas-external
```

Options:
- `--oas-output <file>`: Output path for the populated OpenAPI spec
- `--oas-source <spec>`: Source OpenAPI spec to populate with examples
- `--oas-example-count <n>`: Number of examples per schema (default: 1)
- `--oas-external`: Use external file references instead of inline examples

## Schema Inference

Infer a Vague schema from existing JSON or CSV data:

```bash
# Infer from JSON
node dist/cli.js --infer data.json -o schema.vague

# Infer from CSV
node dist/cli.js --infer users.csv -o schema.vague

# CSV with custom collection name (default: derived from filename)
node dist/cli.js --infer data.csv --collection-name employees

# CSV with custom delimiter
node dist/cli.js --infer data.csv --infer-delimiter ";"

# Custom dataset name
node dist/cli.js --infer data.json --dataset-name TestFixtures
```

Options:
- `--infer <file>`: Input JSON or CSV file
- `--collection-name <name>`: Collection name for CSV (default: derived from filename)
- `--infer-delimiter <char>`: CSV delimiter (default: `,`)
- `--dataset-name <name>`: Name for generated dataset (default: `Generated`)
- `--no-formats`: Disable format detection (uuid, email, etc.)
- `--no-weights`: Disable weighted superpositions

## Auto-Detection

The CLI auto-detects collection-to-schema mappings:
- Case-insensitive: `pets` → `Pet`
- Plural to singular: `invoices` → `Invoice`
- snake_case to PascalCase: `line_items` → `LineItem`

## Data Validation

Validate external JSON data against a Vague schema:

```bash
# Validate data against Vague schema constraints
node dist/cli.js --validate-data data.json --schema schema.vague

# With mapping for collection names
node dist/cli.js --validate-data data.json --schema schema.vague -m '{"invoices": "Invoice"}'
```

Options:
- `--validate-data <file>`: JSON data file to validate
- `--schema <file>`: Vague schema file with constraints

## TypeScript Generation

Generate TypeScript type definitions from inferred schemas:

```bash
# Infer schema with TypeScript definitions
node dist/cli.js --infer data.json -o schema.vague --typescript
# Outputs: schema.vague and schema.vague.d.ts

# TypeScript only (no .vague file)
node dist/cli.js --infer data.json -o types.d.ts --ts-only
```

Options:
- `--typescript`: Also generate TypeScript definitions
- `--ts-only`: Generate only TypeScript (no .vague file)

## OpenAPI Linting

Lint OpenAPI specs with Spectral before using them:

```bash
# Lint an OpenAPI spec
node dist/cli.js --lint-spec openapi.json

# With verbose output (includes hints)
node dist/cli.js --lint-spec openapi.yaml --lint-verbose
```

Options:
- `--lint-spec <file>`: OpenAPI spec file to lint
- `--lint-verbose`: Show detailed lint results including hints

## Watch Mode

Regenerate output when input file changes:

```bash
node dist/cli.js data.vague -o output.json -w
```

## Debug Mode

Enable debug logging for troubleshooting:

```bash
node dist/cli.js schema.vague --debug
node dist/cli.js schema.vague --log-level info
```

## Project Commands

```bash
npm run build     # Compile TypeScript
npm test          # Run tests (vitest)
npm run dev       # Watch mode compilation
```
