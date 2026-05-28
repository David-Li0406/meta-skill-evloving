# GENERATED-DOCS.standard.md — Generated Documentation Standard

## Purpose

Generated docs are produced by automation (or partially automated flows). The goal is to keep them consistent, reproducible, and clearly sourced.

## Audience

* Contributors consuming docs
* Tooling maintaining docs

## Source of truth

* The generating source (schema, code comments, API definitions, scripts)
* The generation pipeline definition

## Required sections (at top of doc or in a header block)

1. **Generated notice**

   * clear statement that this file is generated
2. **Source**

   * where it comes from (path(s), tool, schema)
3. **How to regenerate**

   * exact command(s) or steps
4. **Do not edit by hand**

   * if applicable
5. **Version**

   * generator version or commit reference (optional but recommended)

## Structural rules

* Keep stable headings and anchors when possible.
* Prefer deterministic ordering.

## Allowed content

* Machine-friendly tables, lists, indexes

## Forbidden content

* Hand-written narrative mixed into generated output (unless via controlled templating)

## Maintenance rules

* Any changes should happen at the source or generator.
* If manual edits are required, the file should not be “generated”; split into two docs.

## Quality checklist

* Regeneration produces the same output given same inputs.
* Regeneration steps are documented and correct.

## Common failure modes

* People manually edit generated files
* No regeneration instructions
* Generator output not deterministic
