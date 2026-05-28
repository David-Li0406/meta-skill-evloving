# CSV URL Parser Skill

This skill processes CSV files containing URLs and extracts query parameters as new columns.

## What it does

- Reads CSV files with headers
- Identifies URL columns (looks for 'url' or 'URL' headers)
- Extracts all query parameters from URLs
- Adds parameter names as new column headers
- Fills parameter values (multiple values joined with '|')
- Preserves all original data

## Usage

The skill will automatically activate when you mention:
- "Parse URLs in CSV"
- "Extract URL parameters"
- "Process CSV files with URLs"
- "Analyze URL parameters"

## Examples

**Input CSV:**
```csv
name,url
user1,https://example.com/page?utm_source=google&utm_campaign=summer&id=123
user2,https://example.com/page?utm_source=facebook&id=456&category=premium
```

**Output CSV:**
```csv
name,url,utm_source,utm_campaign,id,category
user1,https://example.com/page?utm_source=google&utm_campaign=summer&id=123,google,summer,123,
user2,https://example.com/page?utm_source=facebook&id=456&category=premium,facebook,,456,premium
```

## Features

- Handles multiple values for same parameter (joined with '|')
- Gracefully handles malformed URLs
- Preserves original data structure
- Processes all CSV files in directory or specific files
- Provides detailed progress feedback
