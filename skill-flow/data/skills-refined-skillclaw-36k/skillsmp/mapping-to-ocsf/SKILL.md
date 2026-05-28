---
name: mapping-to-ocsf
description: Add OCSF mapping to a TQL parsing pipeline. Use when normalizing events to OCSF, creating OCSF operators, or validating OCSF compliance.
disable-model-invocation: true
argument-hint: "[package-directory]"
---

# Add OCSF Mapping to a TQL Parsing Pipeline

Guide the user through adding OCSF (Open Cybersecurity Schema Framework) mapping
to an existing parser package.

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

### Phase 0: Create Parser Package

**Objective**: Ensure a parser package exists before adding OCSF mapping.

**Steps**:

1. Ask the user for the package directory or sample log data
2. If a parser package exists (has `operators/parse.tql`), note the package
   directory and identifier, then proceed to Phase 1
3. If no parser exists, invoke `/tenzir:managing-packages` first

**Completion**: State "Phase 0 complete" with the package ID.

### Phase 1: OCSF Target Analysis

**Objective**: Identify the appropriate OCSF event class and plan the mapping.

**Steps**:

1. Examine the parsed data schema (from the `parse` operator output) to
   understand available fields.
2. Identify the most appropriate OCSF event class based on the data type.
3. Document which OCSF attribute groups will be populated (Classification,
   Occurrence, Context, Primary) as described in the Map Data to OCSF tutorial.
4. Identify needed profiles (Host, OSINT, Security Control, Network Proxy, etc.)
   to achieve mapping completeness.
5. Note any gaps in the source data for populating OCSF fields.

**Completion**: State "Phase 1 complete" before proceeding.

### Phase 2: OCSF Mapping Operator

**Objective**: Create the OCSF mapping operator with proper structure.

Let `<pkg>` be the package ID from Phase 0.

**Steps**:

1. Create a new operator `operators/ocsf/<type>.tql` where `<type>` is the event
   type (e.g., `proxy`, `flow`, `process`, `auth`)

2. Structure the mapping operator following the template pattern from the Map
   Data to OCSF tutorial. Use section comments to organize by attribute group
   (Preamble, Classification, Occurrence, Context, Primary, Profile-specific,
   Epilogue). Only include profile sections for profiles identified in Phase 1.

3. Create a test file `tests/ocsf/<type>.tql`:

   ```tql
   from_file f"{env("TENZIR_INPUTS")}/sample.txt" {
     <pkg>::parse
   }
   <pkg>::ocsf::<type>
   ocsf::cast
   ```

   The `ocsf::cast` operator validates the output against the OCSF schema and
   emits warnings on mismatches.

4. Run `uvx tenzir-test --root <pkg> --summary` and iterate until all warnings
   are gone.

5. Update the baseline with `uvx tenzir-test --root <pkg> -u --summary`

**Completion**: State "Phase 2 complete" before proceeding.

### Phase 3: Summarize

Provide a final summary of the complete parser with OCSF mapping:

- **Package name and structure**: Tree view of the package
- **Parser functionality**: What the parser extracts from raw logs
- **Target OCSF class and version**: The selected event class
- **OCSF attribute groups populated**: Classification, Occurrence, Context,
  Primary
- **OCSF profiles used**: List of enabled profiles
- **Field mapping overview**: Source field → Parsed field → OCSF field
- **Sample input**: Raw log example
- **Sample intermediate**: Parsed data example
- **Sample output**: OCSF event example
- **Limitations**: Any missing OCSF fields or `unmapped` contents

## OCSF Schema Lookup

For specific OCSF questions during the mapping process (event classes, objects,
attributes, profiles), spawn the `tenzir:ocsf` subagent. This fetches OCSF
schema documentation to help select the right class, understand attribute
requirements, and validate mappings.
