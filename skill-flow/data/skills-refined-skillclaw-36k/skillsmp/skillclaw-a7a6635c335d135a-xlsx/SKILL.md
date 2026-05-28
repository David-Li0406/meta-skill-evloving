---
name: xlsx
description: Use this skill for comprehensive spreadsheet creation, editing, and analysis, including intelligent header detection and semantic column mapping for robust data import.
---

# Skill body

## Intelligence Capabilities

When working with imperfect input files (e.g., user uploads, legacy system exports), apply the following intelligent processing strategies.

### 1. Intelligent Header Detection
Never assume the first row is the header. Use the following heuristics:
- **Semantic Analysis**: Look for row content matching known keywords using Levenshtein distance (e.g., "Telefome" ≈ "Telefone").
- **Data Pattern Analysis**: The header is typically the last text-heavy row before data-heavy rows (dates, emails, CPFs).
- **Context**: Headers have high density (few empty cells) and are often below metadata rows (titles, dates).

### 2. Semantic Column Mapping
Map source columns to target fields using specific scoring:
- **Semantic (40%)**: Normalization + Synonyms (e.g., "Zap" -> "Phone").
- **Pattern (30%)**: Data validation samples (e.g., column has `\d{11}` -> "CPF").
- **Context (30%)**: Position and frequency of occurrence.

### 3. Real-World Examples
Refer to examples for handling:
- Metadata headers (Reports with titles)
- Ambiguous columns (Date formats)
- Unknown columns

## Requirements for Outputs

### All Excel files
- **Zero Formula Errors**: Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?).
- **Preserve Existing Templates**: Study and EXACTLY match existing format, style, and conventions when modifying files. Never impose standardized formatting on files with established patterns. Existing template conventions ALWAYS override these guidelines.

### Financial models
#### Color Coding Standards
Unless otherwise stated by the user or existing template:
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios.
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations.
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within the same workbook.
- **Red text (RGB: 255,0,0)**: External links to other workbooks.