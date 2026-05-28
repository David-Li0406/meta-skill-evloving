---
name: detailed-design-parser
description: Parses detailed-design.md files to extract and format file-specific changes for easier copying. Use this skill when the user wants to generate a `detailed-design-by-file.md` from a `detailed-design.md` file.
metadata:
  short-description: Parse detailed-design.md for file changes
---

# Detailed Design Parser

This skill helps in parsing `detailed-design.md` files to extract code changes and format them into a `detailed-design-by-file.md` file. This is useful for copying file contents to other applications.

## Usage

1.  Identify the `detailed-design.md` file path. It is usually located at `openspec/changes/<openspec_id>/detailed-design.md`.
2.  Run the `parse_design.py` script with the path to the `detailed-design.md` file.

## Script

The script `scripts/parse_design.py` takes the input file path as an argument and generates the output file in the same directory.

```bash
python {path}/scripts/parse_design.py <path_to_detailed_design_md>
```
