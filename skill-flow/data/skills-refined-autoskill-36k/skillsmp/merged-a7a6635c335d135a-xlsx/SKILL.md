---
name: xlsx
description: Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. Provides intelligent header detection and semantic column mapping for robust data import.
---

# Intelligence Capabilities

When working with imperfect input files (e.g., user uploads, legacy system exports), apply the following intelligent processing strategies.

## 1. Intelligent Header Detection

Never assume the first row is the header. Use the following heuristics:

- **Semantic Analysis**: Look for row content matching known keywords using Levenshtein distance (e.g., "Telefome" ≈ "Telefone").
- **Data Pattern Analysis**: The header is typically the last text-heavy row before data-heavy rows (dates, emails, CPFs).
- **Context**: Headers have high density (few empty cells) and are often below metadata rows (titles, dates).

## 2. Semantic Column Mapping

Map source columns to target fields using specific scoring:

- **Semantic (40%)**: Normalization + Synonyms (e.g., "Zap" -> "Phone").
- **Pattern (30%)**: Data validation samples (e.g., column has `\d{11}` -> "CPF").
- **Context (30%)**: Position and frequency of occurrence.

## 3. Real-World Examples

For handling:
- Metadata headers (Reports with titles)
- Ambiguous columns (Date formats)
- Unknown columns

---

# Requirements for Outputs

## All Excel files

### Zero Formula Errors

Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?).

### Preserve Existing Templates

Study and EXACTLY match existing format, style, and conventions when modifying files. Never impose standardized formatting on files with established patterns. Existing template conventions ALWAYS override these guidelines.

## Financial models

### Color Coding Standards

Unless otherwise stated by the user or existing template:

- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios.
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations.
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within the same workbook.
- **Red text (RGB: 255,0,0)**: External links to other files.
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated.

### Number Formatting Standards

#### Required Format Rules

- **Years**: Format as text strings (e.g., "2024" not "2,024").
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)").
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-").
- **Percentages**: Default to 0.0% format (one decimal).
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E).
- **Negative numbers**: Use parentheses (123) not minus -123.

### Formula Construction Rules

#### Assumptions Placement

Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells. Use cell references instead of hardcoded values in formulas.

#### Formula Error Prevention

- Verify all cell references are correct.
- Check for off-by-one errors in ranges.
- Ensure consistent formulas across all projection periods.
- Test with edge cases (zero values, negative numbers).
- Verify no unintended circular references.

#### Documentation Requirements for Hardcodes

Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]".

---

# XLSX Creation, Editing, and Analysis

## Overview

A user may ask you to create, edit, or analyze the contents of an .xlsx file. You have different tools and workflows available for different tasks.

## Important Requirements

**LibreOffice Required for Formula Recalculation**: You can assume LibreOffice is installed for recalculating formula values using the `recalc.py` script. The script automatically configures LibreOffice on first run.

## Reading and Analyzing Data

### Data Analysis with Pandas

For data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:

```python
import pandas as pd

# Read Excel
df = pd.read_excel('<input_path>')  # Default: first sheet
all_sheets = pd.read_excel('<input_path>', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('<output_path>', index=False)
```

## Excel File Workflows

## CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python and hardcoding them.** This ensures the spreadsheet remains dynamic and updateable.

### ❌ WRONG - Hardcoding Calculated Values

```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000
```

### ✅ CORRECT - Using Excel Formulas

```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'
```

This applies to ALL calculations - totals, percentages, ratios, differences, etc. The spreadsheet should be able to recalculate when source data changes.

## Common Workflow

1. **Choose tool**: pandas for data, openpyxl for formulas/formatting.
2. **Create/Load**: Create new workbook or load existing file.
3. **Modify**: Add/edit data, formulas, and formatting.
4. **Save**: Write to file.
5. **Recalculate formulas (MANDATORY IF USING FORMULAS)**: Use the recalc.py script.
   ```bash
   python recalc.py <output_path>
   ```
6. **Verify and fix any errors**:
   - The script returns JSON with error details.
   - If `status` is `errors_found`, check `error_summary` for specific error types and locations.
   - Fix the identified errors and recalculate again.

### Creating New Excel Files

```python
# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('<output_path>')
```

### Editing Existing Excel Files

```python
# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('<input_path>')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('<modified_output_path>')
```

## Recalculating Formulas

Excel files created or modified by openpyxl contain formulas as strings but not calculated values. Use the provided `recalc.py` script to recalculate formulas:

```bash
python recalc.py <excel_file> [timeout_seconds]
```

## Formula Verification Checklist

Quick checks to ensure formulas work correctly:

- [ ] **Test 2-3 sample references**: Verify they pull correct values before building full model.
- [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK).
- [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6).

### Common Pitfalls

- [ ] **NaN handling**: Check for null values with `pd.notna()`.
- [ ] **Division by zero**: Check denominators before using `/` in formulas (#DIV/0!).
- [ ] **Wrong references**: Verify all cell references point to intended cells (#REF!).

---

# Intelligent Spreadsheet Import and Analysis

## Overview

When importing or analyzing spreadsheets, especially for data import workflows, intelligent detection and mapping capabilities are essential for handling real-world spreadsheets that may have:

- Non-standard layouts (metadata rows, empty rows, merged cells).
- Varied column naming (synonyms, abbreviations, typos).
- Multiple data types requiring pattern recognition.
- Contextual relationships between columns.

This section provides advanced techniques for intelligent header detection, column mapping, and data pattern analysis.

---

## Intelligent Header Detection

### Overview

Header detection is the process of identifying which row in a spreadsheet contains the column names. Real-world spreadsheets often have:

- Title rows or metadata at the top.
- Empty separator rows.
- Multi-line headers (merged cells).
- Headers that don't start at row 1.

### Detection Strategy: Multi-Factor Analysis

Use a combination of semantic analysis, pattern recognition, and contextual clues to identify headers with high confidence.

#### 1. Semantic Analysis

Use similarity metrics to compare row cells against known header keywords. Implement Levenshtein distance, Jaro-Winkler similarity, and normalization functions to handle:

- Accent removal (á → a).
- Case insensitivity.
- Whitespace normalization.
- Synonym matching.

#### 2. Pattern-Based Data Type Detection

Analyze sample data values (first 5-10 rows) to infer column types:

- **CPF**: 11 digits, format XXX.XXX.XXX-XX.
- **Email**: Contains @ and valid domain.
- **Phone**: 10-11 digits, Brazilian formats.
- **Date**: Multiple formats (DD/MM/YYYY, MM/DD/YYYY, Excel serial).
- **Monetary**: R$, points, commas (Brazilian format).
- **CEP**: 8 digits, format XXXXX-XXX.

### Multi-Factor Scoring

Calculate header likelihood score using:

- Text ratio (30%): Headers are usually text, not numbers.
- Keyword matches (40%): Match against known header keywords.
- Fill ratio (20%): Headers usually have many filled cells.
- Position bonus (10%): Headers usually in first rows.

### Thresholds and Confidence Levels

- **Confidence ≥ 0.8**: High confidence - use automatically.
- **Confidence 0.6-0.8**: Medium confidence - show to user for confirmation.
- **Confidence < 0.6**: Low confidence - require user selection.

---

## Intelligent Column Mapping

### Overview

Column mapping matches spreadsheet column names to system fields. Real-world spreadsheets use varied naming that requires intelligent matching.

### Multi-Factor Scoring System

Use weighted scoring to determine best mapping:

- **Semantic Similarity (40%)**: String similarity and synonym matching.
- **Data Pattern Match (30%)**: Type inferred from actual values.
- **Position Context (15%)**: Expected position of field.
- **Frequency/Common Name (15%)**: Most common names get priority.

### Expanded Knowledge Base

Maintain comprehensive synonym mappings including:

- Portuguese and English variations.
- Regional differences.
- Common typos and abbreviations.
- Context-dependent synonyms.

---

## Data Pattern Analysis

### Overview

Pattern analysis identifies data types and formats by examining actual values, not just column names. This is crucial for:

- Validating mappings.
- Detecting errors.
- Normalizing data formats.
- Providing user feedback.

### Pattern Recognition

Define comprehensive patterns for common data types:

- **CPF**: Brazilian tax ID with validation algorithm.
- **Email**: Standard email format validation.
- **Phone (Brazilian)**: 10-11 digits with formatting.
- **Date**: Multiple format support (DD/MM/YYYY, Excel serial).
- **Monetary (Brazilian)**: R$ format with comma decimal separator.
- **CEP**: Brazilian postal code (8 digits).
- **UF**: Brazilian state abbreviations (2 letters).

### Validation and Normalization

For each pattern type:

- **Regex matching**: Initial pattern detection.
- **Validator function**: Domain-specific validation (e.g., CPF check digits).
- **Normalizer function**: Convert to standard format.
- **Formatter function**: Display in user-friendly format.

---

## Integration with Existing Code

### Integration with xlsx-helper.ts

Enhance `detectHeaderRow()` function in `src/lib/xlsx-helper.ts`:

```typescript
// Enhanced with multi-factor analysis
export function detectHeaderRowEnhanced(
  rows: unknown[][],
  maxRowsToScan = 15
): HeaderDetectionResult {
  const candidates: Array<{
    rowIndex: number;
    score: number;
    headers: string[];
  }> = [];

  // Calculate scores for each candidate row
  for (let i = 0; i < Math.min(rows.length, maxRowsToScan); i++) {
    const row = rows[i];
    if (!row || row.length === 0) continue;

    let score = 0;

    // Factor 1: Text ratio (30 points max)
    score += calculateTextRatio(row) * 30;

    // Factor 2: Keyword matches (40 points max)
    score += Math.min(countKeywordMatches(row) * 10, 40);

    // Factor 3: Fill ratio (20 points max)
    score += calculateFillRatio(row) * 20;

    // Factor 4: Position bonus (10 points)
    if (i < 5) score += 10;

    const headers = row.map(h => String(h ?? "").trim()).filter(Boolean);

    if (headers.length >= 2) {
      candidates.push({
        rowIndex: i,
        score,
        headers,
      });
    }
  }

  candidates.sort((a, b) => b.score - a.score);
  const best = candidates[0];

  // Calculate confidence
  let confidence: number;
  if (candidates.length === 1) {
    confidence = Math.min(best.score / 100, 1);
  } else {
    const scoreDiff = best.score - candidates[1].score;
    const relativeConfidence = scoreDiff / Math.max(best.score, 1);
    const absoluteConfidence = best.score / 100;
    confidence = Math.min((relativeConfidence + absoluteConfidence) / 2, 1);
  }

  return {
    headerRowIndex: best.rowIndex,
    confidence: Math.round(confidence * 100) / 100,
    headers: best.headers,
    candidates: candidates.slice(0, 5),
  };
}
```

### Integration with csv-validator.ts

Enhance `mapCSVHeaders()` function:

```typescript
// Enhanced with pattern analysis and fuzzy matching
export interface ColumnMappingResult {
  mapping: Record<string, string>;
  confidence: Record<string, number>;
  suggestions: Record<string, Array<{ field: string; score: number; reason: string }>>;
}

export function mapCSVHeadersIntelligent(
  headers: string[],
  sampleRows: Record<string, unknown>[],
  maxSuggestions = 3
): ColumnMappingResult {
  const mapping: Record<string, string> = {};
  const confidence: Record<string, number> = {};
  const suggestions: Record<string, Array<{ field: string; score: number; reason: string }> = {};

  for (const header of headers) {
    // Get column data
    const columnData = sampleRows
      .map(row => row[header])
      .filter(v => v !== undefined && v !== null)
      .slice(0, 10); // Sample first 10 rows

    // Detect pattern
    const pattern = detectColumnPattern(columnData);

    // Find best matches
    const matches = findBestSchemaMatches(header, pattern, headers.indexOf(header));

    if (matches.length > 0 && matches[0].score >= 0.5) {
      mapping[header] = matches[