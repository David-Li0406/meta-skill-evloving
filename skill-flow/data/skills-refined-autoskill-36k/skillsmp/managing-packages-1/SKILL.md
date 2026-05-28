---
name: managing-packages
description: Create and manage TQL parsing pipeline packages. Use when creating parser packages, setting up package structure, or iterating on parsing logic.
disable-model-invocation: true
argument-hint: "[sample-file-or-data]"
---

# Create a TQL Parsing Pipeline Package

Guide the user through creating a Tenzir package that parses raw log data into
structured events.

## Preamble: TQL Fundamentals

Read the following pages unconditionally to understand the foundations of TQL:

- <https://docs.tenzir.com/explanations/language.md>
- <https://docs.tenzir.com/explanations/language/types.md>
- <https://docs.tenzir.com/explanations/language/statements.md>
- <https://docs.tenzir.com/explanations/language/expressions.md>
- <https://docs.tenzir.com/explanations/language/programs.md>

Critically, strictly adhere to the best practices in this language tutorial:

- <https://docs.tenzir.com/tutorials/learn-idiomatic-tql.md>

## Preamble: Package Management

Read the following pages to understand packages and testing:

- <https://docs.tenzir.com/explanations/packages.md>
- <https://docs.tenzir.com/reference/test-framework.md>
- <https://docs.tenzir.com/guides/testing/write-tests.md>

The `tenzir-ship` framework manages the `changelog/` directory. When adding
changelog entries to a package, spawn the `dev:changelog-adder` subagent.

## Workflow

Follow ALL phases in EXACT order. You MUST state "Phase N complete" before
proceeding to the next phase.

### Phase 1: Input Schema Analysis

**Objective**: Learn about the input data and understand its structure.

**Steps**:

1. Ask the user to provide sample log data (file path or pasted content)
2. Identify the data source format (CSV, JSON, YAML, syslog, etc.)
3. Identify vendor and product that may have generated this data
4. Document the complete input schema in terms of fields and types

**Completion**: State "Phase 1 complete" before proceeding.

### Phase 2: Package Scaffolding

**Objective**: Create the package structure for iterative development.

**Steps**:

1. Confirm the package ID with the user (typically vendor name, e.g., `fortinet`,
   `cisco`, `microsoft`). In the instructions below, replace `<pkg>` with the
   chosen package ID.
2. Create the package directory structure as described in the Write a Package
   tutorial. Include `operators/parse.tql`, `tests/parse.tql`, and
   `tests/inputs/sample.txt`.
3. Create `package.yaml` with the package metadata.
4. Create the initial `parse` operator in `operators/parse.tql` with just
   `read_lines` as a starting point.
5. Create a test file `tests/parse.tql` that reads from the input:

   ```tql
   from_file f"{env("TENZIR_INPUTS")}/sample.txt" {
     <pkg>::parse
   }
   ```

6. Save the sample log data to `tests/inputs/sample.txt`.
7. Create the initial baseline: `uvx tenzir-test --root <pkg> -u --summary`

**Completion**: State "Phase 2 complete" before proceeding.

### Phase 3: Iterate and Test

**Objective**: Refine the parser until all fields are parsed and properly typed.

**Prerequisites**: Read these guides for transformation patterns:

- <https://docs.tenzir.com/guides/data-shaping/transform-basic-values.md> - Type conversion, null handling, sentinel values
- <https://docs.tenzir.com/guides/data-shaping/extract-structured-data-from-text.md> - Nested structures, delimited data
- <https://docs.tenzir.com/guides/data-shaping/manipulate-strings.md> - String cleanup, splitting, extraction

Loop until all fields are properly parsed:

1. Make ONE modification to the `parse` operator. Work through these categories:
   - **Type conversion**: Parse timestamps, IPs, subnets (see `transform-basic-values`)
   - **Structure extraction**: Parse nested JSON, CSV, key-value pairs (see `extract-structured-data-from-text`)
   - **Data cleaning**: Normalize sentinel values to null, trim whitespace, extract substrings (see `transform-basic-values` and `manipulate-strings`)
2. Observe the impact of your change by re-running:
   - `uvx tenzir-test --root <pkg> --summary`
3. If the diff looks good, update the baseline: `uvx tenzir-test --root <pkg> -u --summary`
4. Go back to Step 1 and continue with the next modification

**Completion**: State "Phase 3 complete" before proceeding.

### Phase 4: Summarize

Provide a final summary of the parser's functionality:

- **Input**: Description of the input format and source
- **TQL**: The complete parsing logic
- **Output**: Description of the parsed schema with types
- **Package structure**: Tree view of the package
- **Noteworthy findings**: Any interesting discoveries or caveats
