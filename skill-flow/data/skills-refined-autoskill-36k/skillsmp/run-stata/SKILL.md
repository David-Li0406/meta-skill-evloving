---
name: run-stata
description: Run Stata code by copying it into tempdo.do and executing the file. Use this when the user wants to run Stata code, test a figure, execute a do-file section, or run regressions. This workaround ensures graphs display correctly and multi-line commands with /// work properly.
---

# Running Stata Code

## Overview
This skill runs Stata code by:
1. Preserving line 1 of tempdo.do (which sources setup_paths.do)
2. Replacing the rest of tempdo.do with the code to run
3. Executing tempdo.do as a complete file via Stata MCP

This workaround addresses two Stata MCP limitations:
- Graphs only display when running entire files (not selections)
- Line continuation with `///` doesn't work with Run Selection

## Instructions

When the user asks you to run Stata code:

1. **Read the current tempdo.do** to get line 1 (the setup_paths.do include)
   - Location: `FRRS_code/src/tempdo.do`
   - Line 1 should be: `do "C:\Users\illge\Princeton Dropbox\Sam Barnett\FRRS_rd2_replication\FRRS_code\src\setup_paths.do"`

2. **Write the new tempdo.do** with:
   - Line 1: Keep the original setup_paths.do include
   - Line 2: Empty line
   - Lines 3+: The Stata code the user wants to run

3. **Inform the user** that tempdo.do has been updated and they should:
   - Open tempdo.do in VSCode
   - Use Stata MCP's "Run File" command (not Run Selection)
   - The graph will appear in the Stata Graphs panel

## Example

User asks: "Run Figure 2a from analysis_KLMS.do"

Steps:
1. Find Figure 2a code in analysis_KLMS.do (search for "2a" or the figure comment)
2. Read tempdo.do line 1
3. Write tempdo.do with:
```stata
do "C:\Users\illge\Princeton Dropbox\Sam Barnett\FRRS_rd2_replication\FRRS_code\src\setup_paths.do"

*(2a) using mp_klms_U: rolling 6Y
use "$proc_analysis/maintable_data", clear
[... rest of figure code ...]
```
4. Tell user: "Updated tempdo.do with Figure 2a code. Open it and use Run File to execute."

## Key Paths
- tempdo.do: `FRRS_code/src/tempdo.do`
- setup_paths.do: `FRRS_code/src/setup_paths.do`
- analysis_KLMS.do: `FRRS_code/src/analysis_KLMS.do`
- data_construction_KLMS.do: `FRRS_code/src/data_construction_KLMS.do`

## Notes
- Always preserve the setup_paths.do include on line 1
- tempdo.do is in .gitignore so changes won't be committed
- If the user provides code directly, use that; if they reference a figure/table, find it in analysis_KLMS.do
