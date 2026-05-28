# UXR Report Analyzer Skill

A Claude Skill for analyzing User Experience Research (UXR) report PDFs and generating comprehensive, structured analysis documents that integrate with HubSpot strategic planning workflows.

## Overview

This skill automates the process of transforming raw UXR report PDFs into standardized analysis documents that:
- Follow a consistent structure for easy cross-referencing
- Connect research findings to strategic objectives (SO1-SO5)
- Extract actionable insights and recommendations
- Build a knowledge graph across research studies
- Support strategic planning and product development

## What It Does

1. **Extracts content** from PDF reports using Prometheus MCP tools
2. **Analyzes findings** in context of HubSpot's Overall Data Strategy
3. **Structures insights** using a comprehensive template framework
4. **Generates analysis** in markdown format with metadata and cross-references
5. **Organizes files** by moving processed PDFs to archive folder
6. **Updates catalog** to maintain searchable research index

## Quick Start

### Installation
This skill is already installed in your Claude skills directory:
```
/Users/jvincent/.claude/skills/uxr-report-analyzer/
```

### Usage
Simply provide a UXR report PDF to analyze:

```
Analyze this report: /Users/jvincent/Projects/writing/resources/UXR Reports/Reports to Review/[Report_Name].pdf
```

Claude will:
1. Ask you for the original URL of the report
2. Extract and analyze the content
3. Generate a structured analysis file
4. Save it to the Analysis folder with current month-year in filename
5. Move the original PDF to Reviewed Reports folder
6. Update the research catalog

### Expected Output
A markdown file at:
```
/Users/jvincent/Projects/writing/resources/UXR Reports/Analysis/[Report_Name]_Analysis_[MM-YYYY].md
```

## File Structure

```
uxr-report-analyzer/
├── Skill.md                           # Main skill instructions
├── README.md                          # This file
└── resources/
    ├── ANALYSIS_TEMPLATE.md          # Detailed analysis structure template
    ├── EXAMPLE_ANALYSIS.md           # Reference example with annotations
    └── CHECKLIST.md                  # Quality assurance checklist
```

## Analysis Document Structure

Each generated analysis includes:

1. **HTML Comment Summary** - Quick reference metadata (lines 1-9)
2. **Metadata** - Study name, creators, URL
3. **The Big Picture** - 2-3 paragraph strategic summary
4. **Key Findings** - Themed insights with specific details
5. **Interesting Metrics** - Standout quantitative data (when applicable)
6. **Recommendations** - Strategic initiatives and tactical actions
7. **Connected Research** - Links to related studies in catalog
8. **Disconnected Research** - Contradictions with other research (when applicable)
9. **Slide/Section Index** - Searchable reference guide

## Dependencies

### Required MCP Tools
- `mcp__prometheus__prometheus_info` - PDF metadata and complexity assessment
- `mcp__prometheus__prometheus_extract_text` - Text extraction from PDFs
- `mcp__prometheus__prometheus_split` - PDF splitting for large documents (optional)

### Required Project Files
- `/Users/jvincent/Projects/writing/resources/CLAUDE.md` - Project organization context
- `/Users/jvincent/Projects/writing/resources/UXR Reports/Analysis/claude.md` - Research catalog
- `/Users/jvincent/Projects/writing/resources/2026 S7/claude.md` - Strategic objectives reference

## Key Features

### Intelligent PDF Processing
- Automatically assesses PDF complexity
- Adapts extraction strategy based on document size
- Handles reports from 10 to 150+ pages
- Maintains page references for citation

### Strategic Context Integration
- Connects findings to HubSpot's Data Strategy
- References strategic objectives (SO1-SO5)
- Identifies alignment and tensions with current strategy
- Builds cross-research knowledge graph

### Quality Standards
- Specificity: Exact numbers, percentages, quotes
- Strategic connection: Business implications for every insight
- Connected: References other research studies
- Clarity: No jargon; simple, powerful language
- Actionability: Specific, implementable recommendations

### Workflow Integration
- Follows established file organization (Reports to Review → Analysis → Reviewed Reports)
- Updates research catalog automatically
- Generates filenames with month-year for version tracking
- Maintains consistent structure for cross-referencing

## When to Use This Skill

**Use when:**
- You have a new UXR report PDF that needs analysis
- You're processing reports in the "Reports to Review" folder
- You need to add research to the strategic planning catalog
- You want to understand how new findings connect to existing research

**Don't use when:**
- You want to read an existing analysis (just use Read tool)
- You're asking general questions about research (reference existing analyses)
- The document is not a UXR/research report

## Examples

### Example 1: Standard Report
```
User: Analyze /Users/jvincent/Projects/writing/resources/UXR Reports/Reports to Review/Admin_Journey_Research.pdf

Claude:
1. Assesses PDF (39 pages, ~4000 tokens)
2. Asks for original URL
3. Extracts text using Prometheus
4. Reads project context and strategic objectives
5. Generates analysis: Admin_Journey_Research_Analysis_11-2025.md
6. Moves PDF to Reviewed Reports
7. Updates catalog
```

### Example 2: Large Report
```
User: Process this 150-page market study

Claude:
1. Assesses PDF (150 pages, high complexity)
2. Splits into 20-page chunks
3. Extracts and synthesizes across chunks
4. Generates comprehensive analysis with extensive index
5. Follows standard save and catalog workflow
```

## Customization

### Adapting for Different Research Types
The template works for various research formats:
- **Quantitative Studies**: Include "Interesting Metrics" section
- **JTBD Research**: Focus on job themes and opportunity scores
- **Market Analysis**: Emphasize competitive insights
- **Product Testing**: Include usability findings

### Modifying the Template
Edit `resources/ANALYSIS_TEMPLATE.md` to:
- Add new sections for specific research types
- Adjust guidelines for your organization
- Include additional quality standards
- Change formatting preferences

## Quality Assurance

Use `resources/CHECKLIST.md` to verify:
- [ ] All required sections included
- [ ] Strategic connections explicit
- [ ] Cross-references accurate
- [ ] Metrics and quotes specific
- [ ] Recommendations actionable
- [ ] File handling correct
- [ ] Catalog updated

## Troubleshooting

### PDF Won't Extract
- Check file path is absolute
- Verify Prometheus MCP tools are available
- Try splitting large PDFs first

### Missing Strategic Context
- Ensure project context files are accessible
- Verify paths in Skill.md match your setup
- Check that strategic objectives docs exist

### Analysis Quality Issues
- Review the example analysis in resources/
- Use the checklist for quality standards
- Compare against existing catalog entries

## Maintenance

### Regular Updates
- Add new research to Connected Research references as catalog grows
- Update strategic objectives references when company strategy changes
- Refine template based on what works well in practice

### Catalog Hygiene
- Periodically review and update catalog entries
- Ensure cross-references remain accurate
- Archive outdated research appropriately

## Support

For issues or questions:
1. Review the template and example files in `resources/`
2. Check the checklist for quality standards
3. Reference existing analyses in the catalog
4. Consult project organization docs in `/Users/jvincent/Projects/writing/CLAUDE.md`

## Version History

- **v1.0** (November 2025) - Initial release
  - PDF extraction via Prometheus MCP
  - Comprehensive analysis template
  - Strategic context integration
  - Automated catalog updates

## License

This skill is part of a personal writing project for HubSpot strategic planning.

---

**Maintained by**: Claude Code
**Last Updated**: 2025-11-02
