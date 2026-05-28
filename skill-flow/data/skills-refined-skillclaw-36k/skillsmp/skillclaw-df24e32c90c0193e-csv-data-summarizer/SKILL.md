---
name: csv-data-summarizer
description: Use this skill when you need to analyze CSV files and generate comprehensive summary statistics and visualizations automatically, without requiring user input.
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

1. **Load and inspect** the CSV file into a pandas DataFrame.
2. **Identify data structure** - Detect column types, dates, numerics, categories.
3. **Determine relevant analyses** based on actual data content:
   - **Sales/E-commerce data**: Time-series trends, revenue analysis, product performance.
   - **Customer data**: Distribution analysis, segmentation, geographic patterns.
   - **Financial data**: Trend analysis, statistical summaries, correlations.
   - **Operational data**: Time-series, performance metrics, distributions.
   - **Survey data**: Frequency analysis, cross-tabulations, distributions.
   - **Generic tabular data**: Adapts based on column types found.
4. **Generate visualizations** that make sense for the dataset:
   - Time-series plots ONLY if date/timestamp columns exist.
   - Correlation heatmaps ONLY if multiple numeric columns exist.
   - Category distributions ONLY if categorical columns exist.
   - Histograms for numeric distributions when relevant.
5. **Present comprehensive output** automatically including:
   - Data overview (rows, columns, types).
   - Summary statistics.
   - Relevant visualizations.

## Behavior Guidelines

✅ **CORRECT APPROACH - SAY THIS:**
- "I'll analyze this data comprehensively right now."
- "Here's the complete analysis with visualizations:"
- Then IMMEDIATELY show the full analysis.

❌ **NEVER SAY THESE PHRASES:**
- "What would you like to do with this data?"
- "Here are some common options:"
- "I can create a comprehensive analysis if you'd like!"
- Any sentence ending with "?" asking for user direction.

❌ **FORBIDDEN BEHAVIORS:**
- Asking what the user wants.
- Listing options for the user to choose from.
- Waiting for user direction before analyzing.