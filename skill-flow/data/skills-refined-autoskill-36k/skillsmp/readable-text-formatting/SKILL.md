---
name: readable-text-formatting
description: Generate human-readable formatted text including aligned markdown tables and ASCII diagrams
---

# Readable Text Formatting

## When to Use

Use this skill whenever you need to generate:
- Markdown tables for documentation or reports
- ASCII art or text-based diagrams
- Text-based visual representations (boxes, borders, flowcharts)
- Any formatted text that humans will read in its raw form (not just rendered)

**Critical**: While markdown tables render correctly in most viewers regardless of alignment, the **raw text** should be human-readable for developers and users who view source files directly.

## Core Principles

### 1. Alignment is for Human Readers
The primary goal is to make raw text files readable. When someone opens a `.md` file in a text editor, they should be able to easily:
- Scan table columns
- Understand ASCII diagrams
- Follow text-based visual structures

### 2. Consistent Column Width
- Each column in a table should have consistent width throughout
- Use padding spaces to align content
- Consider the longest content in each column

### 3. Border Alignment
- All borders, edges, and box boundaries must align vertically
- Characters forming visual boundaries should line up perfectly

## Markdown Tables

### The Problem
AI often generates tables like this (difficult to read in raw form):

```markdown
| Name | Age | Occupation |
|---|---|---|
| Alice | 30 | Software Engineer |
| Bob | 25 | Designer |
| Christopher | 45 | Product Manager |
```

### The Solution
Properly aligned tables with consistent column widths:

```markdown
| Name        | Age | Occupation         |
|-------------|-----|--------------------|
| Alice       | 30  | Software Engineer  |
| Bob         | 25  | Designer           |
| Christopher | 45  | Product Manager    |
```

### How to Create Aligned Markdown Tables

**Step 1: Determine Column Widths**
For each column, find the maximum width needed:
- Check column header length
- Check all data values in that column
- Use the longest value as the column width

**Step 2: Pad All Cells**
Add spaces to the right of content to reach the column width:
```
"Alice"       → "Alice       " (12 chars total)
"30"          → "30  "         (4 chars total)
"Designer"    → "Designer           " (19 chars total)
```

**Step 3: Create Separator Line**
The separator line should match column widths exactly:
```markdown
|-------------|-----|--------------------|
```
Each separator section should be:
- Same width as the column (including padding)
- Filled with dashes (-)

### Template Pattern

```markdown
| [Header 1 + padding] | [Header 2 + padding] | [Header 3 + padding] |
|[dashes = col1 width]|[dashes = col2 width]|[dashes = col3 width]|
| [Data 1.1 + padding] | [Data 1.2 + padding] | [Data 1.3 + padding] |
| [Data 2.1 + padding] | [Data 2.2 + padding] | [Data 2.3 + padding] |
```

### Advanced Table Alignment

**Right-aligned numbers:**
```markdown
| Item        | Quantity | Price   | Total    |
|-------------|----------|---------|----------|
| Widget      |       10 |   $5.00 |  $50.00  |
| Gadget      |        5 |  $12.50 |  $62.50  |
| Tool        |      100 |   $1.00 | $100.00  |
```

**Mixed alignment (left for text, right for numbers):**
```markdown
| Product     | Stock | Revenue  |
|-------------|-------|----------|
| Alpha       |   150 | $45,000  |
| Beta        | 1,200 | $96,000  |
| Gamma       |    75 | $22,500  |
```

## ASCII Art and Text Diagrams

### The Problem
Unaligned ASCII art is confusing:

```
┌─────────────┐
│ Title Here │
│             │
│ Some content that is longer │
└─────────────┘
```

The right border doesn't align!

### The Solution
All borders must align vertically:

```
┌──────────────────────────────┐
│ Title Here                   │
│                              │
│ Some content that is longer  │
└──────────────────────────────┘
```

### How to Create Aligned ASCII Diagrams

**Step 1: Determine Maximum Width**
Find the longest line of content that will appear inside the box.

**Step 2: Calculate Border Width**
```
Border Width = Content Width + 2 (for left/right padding) + 2 (for border chars)
```

**Step 3: Build Each Line**
```
Top:    ┌ + (width-2 dashes) + ┐
Content: │ + (text + padding to width-2) + │
Bottom: └ + (width-2 dashes) + ┘
```

### Common ASCII Patterns

#### Simple Box
```
┌────────────────────┐
│  Content goes here │
│  Another line      │
└────────────────────┘
```

#### Box with Title
```
┌────────────────────┐
│      TITLE         │
├────────────────────┤
│  Content line 1    │
│  Content line 2    │
└────────────────────┘
```

#### Flowchart Nodes
```
    ┌─────────────┐
    │   Start     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  Process 1  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  Process 2  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │     End     │
    └─────────────┘
```

#### Side-by-side Boxes
```
┌─────────────┐       ┌─────────────┐
│   Box A     │  ───▶ │   Box B     │
│  Content A  │       │  Content B  │
└─────────────┘       └─────────────┘
```

### Character Sets for Borders

**Box Drawing Characters:**
- Light: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`
- Heavy: `━ ┃ ┏ ┓ ┗ ┛ ┣ ┫ ┳ ┻ ╋`
- Double: `═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬`
- ASCII-safe: `- | + (corners and intersections)`

**Arrows:**
- `→ ← ↑ ↓ ↔ ↕`
- `⇒ ⇐ ⇑ ⇓ ⇔`
- `▶ ◀ ▲ ▼`
- ASCII-safe: `> < ^ v`

## Step-by-Step Workflow

When asked to create formatted text:

### For Markdown Tables:

1. **List all column headers and data**
   ```
   Headers: Name, Age, City
   Row 1: Alice, 30, San Francisco
   Row 2: Bob, 25, New York
   ```

2. **Calculate column widths**
   ```
   Name column: max("Name", "Alice", "Bob") = 5
   Age column: max("Age", "30", "25") = 3
   City column: max("City", "San Francisco", "New York") = 13
   ```

3. **Build each row with padding**
   ```markdown
   | Name  | Age | City          |
   |-------|-----|---------------|
   | Alice | 30  | San Francisco |
   | Bob   | 25  | New York      |
   ```

### For ASCII Diagrams:

1. **Plan the content and structure**
   ```
   Need: Box with title "Configuration" and 3 content lines
   Longest line: "Database: PostgreSQL 14"
   ```

2. **Calculate dimensions**
   ```
   Content width: 24 chars
   Box width: 24 + 2 (padding) = 26
   Border width: 26 + 2 (borders) = 28
   ```

3. **Build line by line, ensuring alignment**
   ```
   ┌──────────────────────────┐
   │    Configuration         │
   ├──────────────────────────┤
   │  Server: localhost:5432  │
   │  Database: PostgreSQL 14 │
   │  User: admin             │
   └──────────────────────────┘
   ```

## Common Mistakes to Avoid

### ❌ Mistake 1: Inconsistent Column Widths
```markdown
| Name | Age | City |
|---|---|---|
| Alice | 30 | San Francisco |
| Bob | 25 | NY |
```

### ✅ Correct:
```markdown
| Name  | Age | City          |
|-------|-----|---------------|
| Alice | 30  | San Francisco |
| Bob   | 25  | NY            |
```

### ❌ Mistake 2: Misaligned Box Borders
```
┌─────────┐
│ Hello World! │
└─────────┘
```

### ✅ Correct:
```
┌──────────────┐
│ Hello World! │
└──────────────┘
```

### ❌ Mistake 3: Ignoring Content on Lines with Borders
```
┌────────────────┐
│  Username: admin │
│  Password: ***   │
└────────────────┘
```

### ✅ Correct:
```
┌──────────────────┐
│ Username: admin  │
│ Password: ***    │
└──────────────────┘
```

## Testing Your Output

Before finalizing formatted text, verify:

1. **Visual Alignment Check**
   - Copy the output to a monospace text editor
   - All vertical lines should align perfectly
   - All horizontal lines should be continuous

2. **Width Consistency Check**
   - Each row in a table should have the same total width
   - Each line in an ASCII box should have the same total width

3. **Border Integrity Check**
   - Top and bottom borders should have matching width
   - Left and right borders should align vertically on every line

## Best Practices

1. **Always use monospace mental model**: Assume the output will be viewed in a monospace font (like Consolas, Monaco, Courier)

2. **Measure twice, write once**: Calculate all widths before generating the formatted text

3. **Consistency over cleverness**: Simple, well-aligned text is better than complex, misaligned text

4. **Test with the longest content**: Always determine dimensions based on the longest/widest content

5. **Document your calculations**: When creating complex diagrams, show your width calculations in comments (you can remove them from the final output)

6. **Default to ASCII-safe characters when unsure**: If Unicode box-drawing characters might cause issues, use ASCII alternatives:
   - `+`, `-`, `|` for boxes
   - `>`, `<`, `^`, `v` for arrows

## Advanced Patterns

### Multi-level ASCII Hierarchy

```
┌─────────────────────────────────────┐
│           Application               │
├─────────────────────────────────────┤
│  ┌───────────┐    ┌───────────┐    │
│  │ Frontend  │◀──▶│  Backend  │    │
│  └───────────┘    └───────────┘    │
│         │              │            │
│         ▼              ▼            │
│  ┌───────────┐    ┌───────────┐    │
│  │    UI     │    │    API    │    │
│  └───────────┘    └───────────┘    │
└─────────────────────────────────────┘
```

### Complex Table with Merged Headers

```
| Category    | Q1 Results      | Q2 Results      | Q3 Results      | Q4 Results      |
|             | Sales | Profit  | Sales | Profit  | Sales | Profit  | Sales | Profit  |
|-------------|-------|---------|-------|---------|-------|---------|-------|---------|
| Product A   | $100K |  $20K   | $110K |  $22K   | $120K |  $25K   | $130K |  $28K   |
| Product B   | $80K  |  $15K   | $85K  |  $16K   | $90K  |  $18K   | $95K  |  $20K   |
| Product C   | $50K  |  $10K   | $55K  |  $11K   | $60K  |  $12K   | $65K  |  $13K   |
```

### Process Flow with Decision Points

```
        ┌──────────┐
        │  Start   │
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │ Validate │
        └────┬─────┘
             │
        ┌────▼────┐
        │  Valid? │
        └────┬────┘
             │
      ┌──────┴──────┐
      │             │
     YES            NO
      │             │
      ▼             ▼
┌──────────┐   ┌──────────┐
│ Process  │   │  Reject  │
└────┬─────┘   └────┬─────┘
     │              │
     │              │
     └──────┬───────┘
            │
            ▼
       ┌──────────┐
       │   End    │
       └──────────┘
```

## Quick Reference

**Formula for table column width:**
```
width = max(header_length, max(all_data_lengths_in_column))
```

**Formula for box width:**
```
box_width = max_content_width + 2 (padding) + 2 (borders)
```

**Padding calculation:**
```
padding_needed = column_width - actual_content_length
padded_content = content + (" " * padding_needed)
```

## Summary

Remember: The goal is **human readability in raw text form**.

- Markdown tables: Align columns for easy scanning
- ASCII diagrams: Align borders for visual clarity
- Always calculate dimensions before generating
- Test in a monospace editor before finalizing
- Consistency and simplicity are paramount
