---
name: csv-data-summarizer
description: Use this skill to analyze CSV files and generate comprehensive summary statistics and visualizations automatically, without user input.
---

# CSV Data Summarizer

This skill analyzes CSV files and provides comprehensive summaries with statistical insights and visualizations.

## When to Use This Skill

Use this skill whenever the user:
- Uploads or references a CSV file
- Asks to summarize, analyze, or visualize tabular data
- Requests insights from CSV data
- Wants to understand data structure and quality

## ⚠️ CRITICAL BEHAVIOR REQUIREMENT ⚠️

**DO NOT ASK THE USER WHAT THEY WANT TO DO WITH THE DATA.**
**DO NOT OFFER OPTIONS OR CHOICES.**
**DO NOT SAY "What would you like me to help you with?"**
**DO NOT LIST POSSIBLE ANALYSES.**

**IMMEDIATELY AND AUTOMATICALLY:**
1. Run the comprehensive analysis
2. Generate ALL relevant visualizations
3. Present complete results
4. NO questions, NO options, NO waiting for user input

**THE USER WANTS A FULL ANALYSIS RIGHT AWAY - JUST DO IT.**

## How It Works

The skill intelligently adapts to different data types by inspecting the data first, then determining what analyses are most relevant:

### Automatic Analysis Steps:

1. **Load and inspect** - Read CSV into pandas DataFrame
2. **Identify structure** - Detect column types, dates, numerics, categories
3. **Determine relevant analyses** based on actual data content:
   - **Sales/E-commerce data**: Time-series trends, revenue analysis
   - **Customer data**: Distribution analysis, segmentation
   - **Financial data**: Trend analysis, statistical summaries
   - **Operational data**: Performance metrics, distributions
   - **Survey data**: Frequency analysis, cross-tabulations
   - **Generic tabular data**: Adapts based on column types found
4. **Generate visualizations** - Only those that make sense for this dataset:
   - Time-series plots ONLY if date/timestamp columns exist
   - Correlation heatmaps ONLY if multiple numeric columns exist
   - Category distributions ONLY if categorical columns exist
   - Histograms for numeric distributions when relevant
5. **Present complete output** - Everything in one comprehensive response, including:
   - Data overview (rows, columns, types)
   - Key statistics and metrics relevant to the data type
   - Missing data analysis
   - Multiple relevant visualizations
   - Actionable insights based on patterns found in THIS specific dataset

## Behavior Guidelines

✅ **CORRECT APPROACH - SAY THIS:**
- "I'll analyze this data comprehensively right now."
- "Here's the complete analysis with visualizations:"
- "I've identified this as [type] data and generated relevant insights:"
- Then IMMEDIATELY show the full analysis

✅ **DO:**
- Immediately run the analysis script
- Generate ALL relevant charts automatically
- Provide complete insights without being asked
- Be thorough and complete in first response
- Act decisively without asking permission

❌ **NEVER SAY THESE PHRASES:**
- "What would you like to do with this data?"
- "What would you like me to help you with?"
- "Here are some common options:"
- Any sentence ending with "?" asking for user direction
- Any list of options or choices

❌ **FORBIDDEN BEHAVIORS:**
- Asking what the user wants
- Listing options for the user to choose from
- Waiting for user direction before analyzing
- Providing partial analysis that requires follow-up
- Describing what you COULD do instead of DOING it

## Usage

The skill provides a Python function `summarize_csv(file_path)` that:
- Accepts a path to a CSV file
- Returns a comprehensive text summary with statistics
- Generates multiple visualizations automatically based on data structure

## Technical Details

**Dependencies:** python>=3.8, pandas>=2.0.0, matplotlib>=3.7.0, seaborn>=0.12.0

**Files:**
- `analyze.py` - Core analysis logic
- `requirements.txt` - Python dependencies
- `resources/sample.csv` - Example dataset for testing
- `resources/README.md` - Additional documentation

## Notes

- Automatically detects date columns (columns containing 'date' in name)
- Handles missing data gracefully
- Generates visualizations only when date columns are present
- All numeric columns are included in statistical summary