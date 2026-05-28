# Document Parsing Guidelines

## Purpose

This guide provides detailed instructions for Phase 1: Document Parsing. Follow these guidelines to ensure accurate extraction and understanding of source documents.

## Core Principles

1. **Preserve Original Content**: Never modify, summarize, or paraphrase the original text
2. **Maintain Structure**: Respect the original document's hierarchy and organization
3. **Extract All Data**: Identify and catalog all quantitative data points
4. **Identify Conclusions**: Locate and extract all conclusions and recommendations
5. **No Interpretation**: Do not interpret or add meaning to the content

## Document Type Detection

### Markdown Documents

**Characteristics**:
- File extension: `.md`
- Header syntax: `# H1`, `## H2`, `### H3`, etc.
- Bullet points: `- ` or `* ` or `1. `
- Emphasis: `**bold**`, `*italic*`, `` `code` ``

**Parsing Strategy**:
1. Parse headers to determine document structure
2. Extract content under each header
3. Identify lists and data tables
4. Preserve all formatting (bold, italic, links)

**Example**:
```markdown
# Quarterly Report Q3 2024

## Executive Summary

Revenue increased by 15% compared to Q2 2024.
- Metric A: 100 units (+20%)
- Metric B: 85 units (-5%)

## Key Findings

### Finding 1
Detailed analysis of finding 1...

### Finding 2
Detailed analysis of finding 2...

## Conclusions

1. Market conditions are favorable
2. Product performance exceeded expectations
3. Recommend expansion into new regions
```

**Expected Output**:
- Title: "Quarterly Report Q3 2024"
- Sections: Executive Summary, Key Findings, Conclusions
- Data points: 100, 85, 15%, 20%, -5%
- Conclusions: 3 conclusions extracted

### Plain Text Documents

**Characteristics**:
- No special formatting
- Paragraphs separated by blank lines
- May use indentation for structure
- Titles may be all caps or followed by colons

**Parsing Strategy**:
1. Detect section headers (all caps, ending with colon)
2. Group paragraphs under headers
3. Extract numerical data using regex patterns
4. Identify conclusion keywords (conclusion, finding, result, summary, recommendation)

**Example**:
```
QUARTERLY REPORT Q3 2024

EXECUTIVE SUMMARY:
Revenue increased by 15% compared to Q2 2024.
Metric A reached 100 units, showing 20% growth.
Metric B declined to 85 units, a 5% decrease.

KEY FINDINGS:
Finding 1: Detailed analysis of finding 1.
Finding 2: Detailed analysis of finding 2.

CONCLUSIONS:
Market conditions are favorable.
Product performance exceeded expectations.
Recommend expansion into new regions.
```

**Expected Output**:
- Title: "QUARTERLY REPORT Q3 2024"
- Sections: EXECUTIVE SUMMARY, KEY FINDINGS, CONCLUSIONS
- Data points: 15%, 100, 20%, 85, 5%
- Conclusions: 3 conclusions extracted

### JSON Documents

**Characteristics**:
- File extension: `.json`
- Structured data format
- Explicit fields for content

**Parsing Strategy**:
1. Parse JSON using `json` module
2. Extract top-level fields: title, sections, data_points, conclusions
3. Validate structure and required fields
4. Preserve all data exactly as provided

**Expected Schema**:
```json
{
  "title": "Document Title",
  "sections": [
    {
      "title": "Section Title",
      "content": "Section content...",
      "level": 1
    }
  ],
  "data_points": [
    {
      "label": "Metric A",
      "value": 100,
      "unit": "units",
      "category": "Executive Summary"
    }
  ],
  "conclusions": [
    {
      "text": "Conclusion text",
      "category": "Conclusions",
      "priority": "high"
    }
  ]
}
```

## Data Point Extraction

### Regex Pattern

Use this pattern to extract numerical data:
```regex
(\d+\.?\d*)\s*(%|\$|k|m|b)?\b
```

**Matches**:
- `15%` → value: 15.0, unit: `%`
- `$100k` → value: 100.0, unit: `$k`
- `1.5b` → value: 1.5, unit: `b`

### Data Point Classification

Assign data points to categories based on context:
- **Executive Summary**: Overall metrics, key performance indicators
- **Financial**: Revenue, profit, cost, margins
- **Operations**: Units sold, production metrics, efficiency
- **Market**: Share, growth rates, customer acquisition

## Conclusion Extraction

### Keyword Detection

Search for sections with these keywords:
- `conclusion`
- `finding`
- `result`
- `summary`
- `recommendation`
- `takeaway`

### Extraction Rules

1. Extract complete sentences from conclusion sections
2. Preserve original wording exactly
3. Include bullet points as separate conclusions
4. Numbered lists = separate conclusions
5. Maintain category context

**Example Extraction**:

**Source**:
```
## Conclusions

Based on the analysis, we conclude:
1. Market conditions are favorable for expansion
2. Product performance exceeded expectations by 20%

Recommendations:
- Enter new market segments
- Increase production capacity
```

**Extracted Conclusions**:
1. "Market conditions are favorable for expansion"
2. "Product performance exceeded expectations by 20%"
3. "Enter new market segments"
4. "Increase production capacity"

## Common Traps

| Trap | Symptom | Solution |
|------|----------|----------|
| Modifying content | Content summarized or paraphrased | Preserve exact text from source |
| Missing data points | Data not extracted correctly | Verify regex pattern and test on samples |
| Misclassified sections | Wrong category assigned | Check section headers and keywords |
| Incomplete conclusions | Conclusions truncated or merged | Extract complete sentences separately |
| Structure loss | Hierarchy flattened | Maintain level indicators and nesting |

## Verification Checklist

After parsing, verify:

- [ ] Document title extracted correctly
- [ ] All sections identified and labeled
- [ ] Section hierarchy preserved
- [ ] All numerical data points extracted
- [ ] Data points assigned correct categories
- [ ] All conclusions extracted exactly as written
- [ ] No content modified or interpreted
- [ ] Original structure maintained
- [ ] No duplicate or missing sections

## Exit Criteria

Proceed to Phase 2 when:

1. **Structure Complete**: All sections identified with correct hierarchy
2. **Data Catalogued**: All numerical data points extracted and classified
3. **Conclusions Extracted**: All conclusions and recommendations preserved exactly
4. **Content Integrity**: Zero modification of original content
5. **Validation Passed**: Verification checklist complete
