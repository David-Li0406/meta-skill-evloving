# URL Parameter Parser Skill

A Claude Code skill for parsing URLs in CSV files and extracting query parameters as new columns.

## Features

- 🎯 **Automatic URL Detection**: Finds 'url' or 'URL' columns in CSV files
- 📊 **Parameter Extraction**: Extracts all query parameters from URLs
- 🔧 **Dynamic Columns**: Creates new columns for each unique parameter
- ✅ **Data Preservation**: Maintains all original data while adding new columns
- 🚀 **Batch Processing**: Handles multiple CSV files at once

## Installation

This skill is part of the FeedMob Agent Skills collection. It will be automatically available when the skill collection is installed.

## Usage

The URL Parameter Parser skill will automatically activate when you mention:

- "Parse URLs in my CSV files"
- "Extract URL parameters from data.csv"
- "Process CSV files with URLs"
- "Analyze URL parameters in this spreadsheet"

## Example

**Before processing:**
```csv
name,url
user1,https://example.com/page?utm_source=google&utm_campaign=summer&id=123
user2,https://example.com/page?utm_source=facebook&id=456&category=premium
```

**After processing:**
```csv
name,url,utm_source,utm_campaign,id,category
user1,https://example.com/page?utm_source=google&utm_campaign=summer&id=123,google,summer,123,
user2,https://example.com/page?utm_source=facebook&id=456&category=premium,facebook,,456,premium
```

## Requirements

- Python 3.6 or higher with standard libraries (csv, urllib.parse)
- CSV files must have headers
- URL column should be named 'url' or 'URL'

## How it works

1. **File Detection**: Identifies CSV files in the current directory or specified paths
2. **URL Analysis**: Finds columns containing URLs (case-insensitive)
3. **Parameter Extraction**: Parses query parameters using Python's urllib.parse
4. **Column Creation**: Adds new columns for each unique parameter found
5. **Data Processing**: Fills new columns with parameter values
6. **File Update**: Saves the processed data back to the original file

## Features

- **Multiple Values**: When a parameter appears multiple times, values are joined with '|'
- **Error Handling**: Gracefully handles malformed URLs
- **Progress Feedback**: Provides detailed output during processing
- **Flexible Input**: Can process specific files or all CSV files in a directory

## Skill Details

- **Name**: `url-parameter-parser`
- **Tools**: Read, Write, Bash, Glob
- **Language**: Python
- **Dependencies**: Python 3.6+ standard libraries only

## Contributing

Improvements to this plugin are welcome! You can:
- Add support for different URL column names
- Enhance parameter value handling
- Add configuration options
- Provide feedback and suggestions
