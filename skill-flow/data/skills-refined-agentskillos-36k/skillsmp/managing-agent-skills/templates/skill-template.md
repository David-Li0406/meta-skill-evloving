---
# YAML Frontmatter - Required for all skills
# Format: lowercase-with-hyphens, max 64 chars, gerund form (verb + -ing)
# Examples: processing-pdfs, analyzing-financial-statements, validating-api-responses
name: your-skill-name

# Description must include BOTH "what it does" AND "when to use it" with specific triggers
# Format: [What]. Use when [scenarios], or when user [provides data] or mentions [keywords].
# Max 1024 chars. Include 3-5 specific trigger keywords for discoverability.
# Example: "Calculates financial ratios from statements. Use when analyzing investments,
# or when user provides income statements, balance sheets, or mentions ROE, profitability."
description: Brief description of what this skill does and when to use it. Include specific trigger keywords and contexts that should activate this skill.
---

# Skill Name

# Brief overview (2-3 sentences) explaining the skill's purpose and primary capability.
# Focus on what makes this skill unique and what domain knowledge it provides.
Brief overview paragraph explaining the skill's purpose and primary capability.

## When to Use This Skill

# List 3-5 specific activation triggers. Include:
# - Task types: "analyzing", "processing", "validating", "generating"
# - Domain contexts: specific scenarios where this skill applies
# - Data formats: "CSV files", "JSON data", "API responses"
# - User language: keywords users might say
Activate this skill when:
- [Trigger condition 1 - e.g., "User needs to validate API responses"]
- [Trigger condition 2 - e.g., "Working with REST or GraphQL endpoints"]
- [Trigger condition 3 - e.g., "Task involves schema verification"]
- User mentions [specific keywords like "API validation", "schema", "endpoint testing"]

## Core Workflow

# Break complex tasks into clear numbered steps with subsections.
# Each step should have: description, specific actions, validation criteria.
# Keep steps focused - if a step is too long, break it into substeps.

### Step 1: [Step Name - Use action verb, e.g., "Validate Input Data"]

# Describe WHAT happens in this step and WHY it's important.
# Be specific about inputs/outputs, not just "process the data".
Describe what happens in this step.

**Actions**:
# List specific, actionable items with checkboxes for validation.
# Be concrete: "Check field X exists" not "validate data"
- [ ] Action item 1 [e.g., "Verify required fields present: company_name, fiscal_year"]
- [ ] Action item 2 [e.g., "Check numeric fields contain valid numbers (not None/NaN)"]
- [ ] Action item 3 [e.g., "Ensure dates in ISO format (YYYY-MM-DD)"]

**Validation**:
# Define specific success criteria. How do you know this step worked?
# Use measurable criteria: counts, formats, ranges, existence checks.
- Verify [validation criteria - e.g., "All required fields present and properly formatted"]

### Step 2: [Step Name - e.g., "Process Data" or "Execute Calculation"]

# Each step builds on previous steps. Reference earlier work when needed.
Describe what happens in this step.

**Actions**:
- [ ] Action item 1
- [ ] Action item 2

**Decision Point**:
# Use decision points when workflow branches based on conditions.
# Be specific about conditions and next steps.
- If [condition - e.g., "data contains errors"], proceed to Step 4 (Error Handling)
- If [other condition - e.g., "data valid"], proceed to Step 3 (Generate Output)

### Step 3: [Step Name - e.g., "Generate Output" or "Format Results"]

# Final steps should include output formatting and final validation.
Describe what happens in this step.

**Output**:
# Specify exact output format, file names, data structure.
# Include examples if format is complex or company-specific.
- [Expected output description - e.g., "Excel file named {company}_{year}_analysis.xlsx"]

## Supporting Resources

# Optional: Include this section if your skill uses progressive disclosure.
# If SKILL.md is under 500 lines and self-contained, omit this section.
# Use progressive disclosure when you have:
# - Detailed reference specs (REFERENCE.md)
# - Complex examples (examples.md)
# - Validation criteria (validation-rules.md)
# - Error scenarios (error-handling.md)

# For each supporting file, explain WHEN to load it (context matters!)
# Keep file references ONE LEVEL DEEP - don't create chains (file → file → file)

For detailed information, refer to:
- **reference.md**: [When to use - e.g., "Load when you need exact API endpoint specs or data format details"]
- **examples.md**: [When to use - e.g., "Load when user needs usage examples or sample inputs/outputs"]
- **validation-rules.md**: [When to use - e.g., "Load when validating results or checking quality criteria"]

Load these files only when needed for specific tasks.

## Dependencies

# Optional: Include if your skill requires external packages, tools, or resources.
# Document ALL dependencies - Claude shouldn't have to guess what's needed.
# Include version requirements to avoid compatibility issues.

**Required**:
- [Dependency 1 with version - e.g., "pandas >= 1.5.0"]
- [Dependency 2 with version - e.g., "requests >= 2.28.0"]
- [System requirement - e.g., "Python 3.8+"]

**Installation**:
```bash
# Provide exact installation commands
pip install pandas>=1.5.0 requests>=2.28.0
```

## Usage Examples

# Optional but HIGHLY RECOMMENDED: Examples make abstract instructions concrete.
# Include 2-3 examples showing different scenarios or edge cases.
# Use real data formats your users will encounter.

### Example 1: [Scenario Name - e.g., "Basic Financial Analysis"]

**Input**: [Description of input - be specific about format]
```
# If applicable, show actual input format
company_name: "Acme Corp"
fiscal_year: 2024
revenue: 1000000
```

**Process**:
1. [Step description - e.g., "Validate input contains required fields"]
2. [Step description - e.g., "Calculate profitability ratios"]
3. [Step description - e.g., "Generate formatted report"]

**Output**: [Description of expected output with format]
```
# Show actual output format if applicable
ROE: 15.2%
Profit Margin: 12.5%
```

## Validation Checklist

# CRITICAL: Define specific, measurable success criteria.
# This checklist ensures task completion and quality.
# Group by category (data quality, calculations, output, etc.)

### Data Quality
- [ ] [Validation item 1 - e.g., "All required fields present"]
- [ ] [Validation item 2 - e.g., "No None/NaN values in numeric fields"]

### Processing
- [ ] [Validation item 3 - e.g., "All calculations completed successfully"]
- [ ] [Validation item 4 - e.g., "Results within expected ranges"]

### Output
- [ ] [Validation item 5 - e.g., "File created with correct naming convention"]
- [ ] [Validation item 6 - e.g., "Output formatted per template"]

## Key Principles

# Optional: Include 2-4 key principles that guide how this skill should be used.
# Focus on what makes this domain unique or error-prone.
# Keep concise - details belong in workflow steps.

- **[Principle 1]**: [Description - e.g., "Always validate input before processing"]
- **[Principle 2]**: [Description - e.g., "Use company-specific formulas, not standard industry formulas"]
- **[Principle 3]**: [Description - e.g., "Results must match internal benchmarks within 5% tolerance"]

## Troubleshooting

# Optional: Document common errors and their solutions.
# Include errors from: data quality issues, calculation failures, tool errors.
# Format as problem → solution pairs for quick reference.

**Issue**: [Problem description - e.g., "Script fails with 'KeyError: fiscal_year'"]
**Solution**: [Resolution steps - e.g., "Verify input JSON contains 'fiscal_year' field. Check spelling and case sensitivity."]

**Issue**: [Problem description - e.g., "Division by zero in ratio calculation"]
**Solution**: [Resolution steps - e.g., "Check that denominator fields (e.g., total_assets) are not zero or None before calculating."]

## Output Format

# Optional but recommended: Specify exact format Claude should deliver.
# Be specific about: file names, data structure, formatting requirements.
# Include examples or templates if format is complex.

When completing tasks, provide:
1. [Output component 1 - e.g., "Summary of results with key metrics highlighted"]
2. [Output component 2 - e.g., "Excel file with formatted data and charts"]
3. [Output component 3 - e.g., "Validation report confirming all checks passed"]

---

# IMPORTANT REMINDERS (Delete this section when creating actual skill)

## Content Guidelines
- ✅ Only include information Claude doesn't already know (company-specific, proprietary)
- ❌ Don't include basic programming concepts, standard libraries, general best practices
- ✅ Keep SKILL.md under 500 lines (use progressive disclosure if longer)
- ✅ Use consistent terminology throughout
- ✅ All file paths use forward slashes (/) for cross-platform compatibility

## YAML Rules
- Must use lowercase-with-hyphens for name
- Must be gerund form (verb + -ing)
- Description must include specific triggers and keywords
- Max 64 chars for name, 1024 for description
- No tabs in YAML (use spaces)

## Validation Before Finalizing
- [ ] YAML valid (delimiters, no tabs, required fields)
- [ ] Name format correct: lowercase-with-hyphens, gerund, <64 chars
- [ ] Description includes both "what" and "when" with 3+ triggers
- [ ] SKILL.md under 500 lines or properly split
- [ ] All referenced files exist
- [ ] No redundant information
- [ ] Specific validation criteria included
- [ ] Cross-platform compatible (forward slashes in paths)
