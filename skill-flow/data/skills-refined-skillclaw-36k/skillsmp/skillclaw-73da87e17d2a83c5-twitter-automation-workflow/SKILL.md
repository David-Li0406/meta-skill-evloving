---
name: twitter-automation-workflow
description: Use this skill when you want to automate the process of collecting tweets from Twitter based on specific search parameters and store the results in a database.
---

# Twitter Automation Workflow

This skill automates the collection of tweets from Twitter, allowing you to extract links and relevant information based on defined search criteria.

## Usage Scenarios

Use this skill when you want to automatically gather tweets that match specific search parameters instead of manually searching and copying links.

## How to Use

### Method A: MCP Driven Mode (Recommended, No Configuration Required)
Simply instruct the AI to execute the collection. The AI will automatically call the built-in `browser` skill, synchronize your profile, and handle all search logic.
- **Advantages**: Fully automated without needing to manually start the Chrome debugging port.
- **Example Command**: `@twitter-automation-workflow execute, using nano-banana-pro preset.`

### Method B: Local Script Mode (Requires Debugging Port)
If you prefer to run the process manually on your local terminal:
1. **Start Chrome Debugging Port**:
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```
2. **Run the Script**:
   ```bash
   node scripts/collector.js --preset nano-banana-pro --output preview
   ```

## Workflow Steps
1. Access the Twitter search page based on search parameters.
2. Automatically scroll to load more tweets.
3. Extract tweet links and basic information.
4. Deduplicate and apply simple filters.
5. Output a list of links (one per line) or a preview in HTML format.

## Quick Start

### Prerequisites

```bash
npm install playwright
npx playwright install chromium
```

### Running the Script

```bash
# Basic usage (default search parameters)
node scripts/collector.js

# Custom search parameters
node scripts/collector.js --query "your keywords" --since "24h"

# Generate a visual preview page
node scripts/collector.js --preset nano-banana-pro --output preview

# Export full text from the filtering page (based on third-party parsing)
node scripts/collector.js --preset nano-banana-pro --output filter-json
```

## Available Parameters

- `--query`: Search keywords (supports AND/OR logic)
- `--since`: Time range (24h, 7d, 30d)
- `--min-likes`: Minimum number of likes
- `--max-tweets`: Maximum number of tweets to collect (default 100)
- `--exclude`: Excluded keywords (space-separated)
- `--filter-content`: Content type filtering (media, videos, images)
- `--exclude-replies`: Exclude replies
- `--exclude-retweets`: Exclude retweets
- `--score-keywords`: Scoring keywords (comma-separated)
- `--min-score`: Minimum score threshold (0-1)
- `--output`: Output format (console/file/preview/filter-json)
- `--filter-url`: Filtering page address
- `--output-dir`: Output directory

## Preset Search Parameters

Built-in preset search configurations can be used directly from the plugin:

### Nano Banana Pro

Default search parameters (from your plugin configuration):

```
#NanoBananaPro OR #NanoBanana OR "Nano Banana" OR "prompt"
AND -female -woman -hair -GEMINIFOURTH
since_time:{{NOW-24h}}
min_faves:50
filter:media
-filter:replies
```

**Explanation**:
- Keywords: Related to Nano Banana Pro + prompt
- Exclusions: Female-related, GEMINIFOURTH
- Time: Last 24 hours
- Minimum likes: 50
- Content: Must include media
- Exclude replies

## Output Format

### Link List Format

The output will be plain text, with one link per line:

```
https://x.com/username/status/1234567890
https://x.com/username/status/1234567891
https://x.com/username/status/1234567892
```

**Usage**:
1. Copy the output content.
2. Paste it into the filtering webpage (`https://twitterhot.vercel.app/tweet-filter.html`).
3. Continue your existing filtering process.

### Output Statistics

At the end of the run, you will see:

```
✅ Collection complete
📊 Total: 100 tweets
✅ After deduplication: 95 tweets
🔗 Links have been output to the console
```

## Technical Implementation

### Core Logic

1. **Search Page Navigation**
   - Construct the complete Twitter search URL.
   - Support time variables (e.g., `{{NOW-24h}}`).

2. **Automatic Scrolling Collection**
   - Simulate human scrolling behavior.
   - Wait for content to load.
   - Stop condition: reach maximum number or bottom of the page.

3. **Tweet Extraction**
   - Selector: `article[data-testid="tweet"]`