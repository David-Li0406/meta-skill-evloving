# Support Data Analyzer Skill

A Claude Skill for analyzing customer support feedback data and generating prioritized strategic reports with real customer examples.

## What This Skill Does

Transforms raw support data (Excel/CSV) into actionable insights by:
- **Categorizing** thousands of issues into clear themes
- **Prioritizing** by volume, frustration, and revenue impact (P0-P3)
- **Extracting** real customer quotes to illustrate pain points
- **Trending** recent issues vs. historical baselines
- **Recommending** specific actions with timelines and impact estimates

## When to Use This Skill

Invoke this skill when you have:
- Excel/CSV files with support data (PIT, roadblocks, tickets, CSAT)
- Need to understand top customer pain points
- Want prioritized recommendations for product/eng teams
- Need to show trends (60-day vs. all-time)

## Quick Start

### 1. Prepare Your Data

Your Excel file should have these sheets (all optional except Support Data or PIT):

**PIT & Roadblocks** (strategic customer feedback):
- Submitted At Date
- Category (e.g., "Object", "Properties", "Pipelines")
- Sub Category (e.g., "Associations", "Create Property")
- Frustration Level (1-5 scale)
- MRR (CS) and MRR (Sales)
- Use Case Title and Use Case Body

**Support Data** (support tickets):
- Created UTC Date
- Support Product Area
- Support roadblock
- Ticket Name and Content

**CSAT** (optional - satisfaction surveys):
- Created At Date
- Score (1-5)
- Text (feedback)
- Event Trigger

**Ideas Forum** (optional - feature requests):
- Idea Title
- Count of Upvotes
- Portal Gross MRR

### 2. Invoke the Skill

```
User: "Analyze this support data and prioritize issues by customer impact.
       Focus on the last 60 days."

[Attach: Data Platform data - Code Orange.xlsx]
```

### 3. Review the Output

The skill generates a comprehensive markdown report:
- **Executive Summary**: Top 3 critical issues, key metrics, trends
- **P0-P3 Breakdown**: Each theme with 5 customer examples
- **Strategic Recommendations**: Immediate actions with timelines
- **CSAT Analysis**: Correlation with support themes
- **Revenue Protection**: MRR at risk by theme

## Example Use Cases

### Use Case 1: Quarterly Product Planning
"Analyze all our support data and show me the top 10 customer pain points with revenue impact."
→ Generates all-time analysis with P0-P3 priorities, MRR totals, and Ideas Forum validation

### Use Case 2: Sprint Planning (Last 60 Days)
"What are customers complaining about most in the last 60 days? Show trends vs. historical."
→ Generates filtered analysis with trend arrows, "NEW to top 5" flags, and frustration increases

### Use Case 3: Deep Dive on Specific Area
"Can you analyze just the property management issues in detail?"
→ Generates focused report with sub-theme breakdown and 7-10 examples per sub-issue

### Use Case 4: Customer Examples for Leadership
"Create a doc with real customer examples for each major pain point."
→ Generates separate customer feedback document with detailed quotes and interpretations

## Files in This Skill

```
support-data-analyzer/
├── Skill.md                              # Main skill instructions
├── README.md                             # This file
└── resources/
    ├── PRIORITIZATION_FRAMEWORK.md       # P0-P3 assignment criteria
    ├── REPORT_TEMPLATE.md                # Markdown report structure
    └── EXAMPLES.md                       # Sample analyses with annotations
```

## Configuration Options

### Time Filtering
- "Last 60 days" - Recent trends, worsening issues
- "Last 90 days" / "Q4 2025" - Quarter-based planning
- No filter (default) - All-time historical analysis

### Focus Areas
- "Focus on association issues" - Drills into sub-themes
- "Show me property management issues" - Single category deep-dive

### Output Formats
- Default: Single comprehensive report
- "Create two files: analysis + customer examples" - Separate docs

## Interpreting Results

### Priority Levels

**P0 (Critical)** - Ship stoppers, high revenue at risk
- Volume >150 (60d) or >1,000 (all-time) OR
- High frustration + substantial volume OR
- Revenue >$75K (60d) or >$4M (all-time)

**P1 (High)** - Significant pain, medium-high volume
- Volume 100-150 (60d) or 700-1,000 (all-time)
- Moderate frustration with good volume

**P2 (Medium)** - Specialized high pain or moderate volume
- Volume 30-100 (60d) or 200-700 (all-time)
- High frustration but niche use case

**P3 (Lower)** - Administrative, low frequency
- Volume <30 (60d) or <200 (all-time)

### Trend Indicators

- **↑ +14%** - Metric increasing (usually bad for frustration)
- **↓ -4pp** - Percentage point decrease (good if frustration)
- **NEW to top 3** - Issue surged recently, investigate urgently
- **⚠️** - Frustration ≥3.5/5, high pain when encountered

### Customer Examples

Each example includes:
- **Quote**: Real customer feedback (not synthesized)
- **Frustration**: 1-5 scale (if from PIT data)
- **MRR**: Revenue at risk (if available)
- **"What this means"**: Interpretation of business impact

## Tips for Best Results

### Data Quality
- ✅ Include frustration levels (1-5) for strategic depth
- ✅ Include MRR data to prioritize by revenue
- ✅ Use consistent date formats (YYYY-MM-DD)
- ✅ Categorize issues (Product Area > Sub Category)

### Analysis Scope
- 🎯 60 days: Best for recent trends and sprint planning
- 🎯 All-time: Best for big-picture strategy and Ideas Forum validation
- 🎯 Focused: Best for deep-dive into specific product area

### Interpreting Frustration
- 1-2: Annoyance, low priority
- 3: Moderate pain, workflow friction
- 4: High pain, actively seeking workarounds
- 5: Critical blocker, considering churn

## Customization

### Adjusting Priority Thresholds

Edit `resources/PRIORITIZATION_FRAMEWORK.md` to change:
- Volume thresholds for P0-P3
- Frustration weight in priority calculation
- Revenue impact thresholds

### Changing Report Structure

Edit `resources/REPORT_TEMPLATE.md` to:
- Add/remove sections
- Change formatting preferences
- Adjust example count per theme

## Dependencies

- **Python 3.8+** (for Excel processing)
- **openpyxl** (for .xlsx file reading)

Install dependencies:
```bash
pip install openpyxl
```

## Troubleshooting

### "Cannot read Excel file"
- Convert to CSV manually, or
- Check file is not corrupted
- Verify file has expected sheet names

### "Date filtering returns 0 results"
- Check date column format (should be YYYY-MM-DD HH:MM:SS)
- Verify date column name matches expected ("Created UTC Date", "Submitted At Date")

### "Missing frustration data"
- Frustration levels optional, will prioritize by volume only
- Note: Support tickets typically don't have frustration, only PIT data

### "MRR totals seem low"
- Not all issues have MRR data (support tickets often don't)
- "Revenue at risk" is from PIT data only, not complete picture

## Version History

- **v1.0.0** (2025-10-31): Initial release
  - Supports PIT, Support Tickets, CSAT, Ideas Forum
  - P0-P3 prioritization framework
  - 60-day and all-time analysis modes
  - Trend comparison
  - Customer example extraction

## Support

For issues or questions about this skill:
1. Check `resources/EXAMPLES.md` for sample analyses
2. Review `resources/PRIORITIZATION_FRAMEWORK.md` for priority logic
3. Verify your data format matches expected columns

## License

Internal use only. Do not distribute support data externally.
