---
name: memo
description: Records work information with multi-dimensional tracking. Use when user wants to record work events, tasks, or activities without executing them. Supports webpage content summarization and URL recording.
---

# Memo Command

This command records work information using the work-memo skill's capabilities. It's designed for information recording only - no task execution.

## Usage

Run this command with your work information:
```
/memo 填写的信息
```

Or provide a URL to fetch and summarize webpage content:
```
/memo https://example.com/article
```

## Process

1. **Parse the input** to extract work details from natural language or URL
2. **Identify dimensions** (type, urgency, importance, tags, contexts, dates)
3. **For URLs**: Fetch webpage content, extract and summarize
4. **Record the information** using the work-memo storage system
5. **Return confirmation** with recorded details

## Implementation

When this command is triggered:

### For Text Input

1. Parse the user's input to extract:
   - Title/description of work
   - Type (task, meeting, call, email, review, coding, design, etc.)
   - Priority indicators (urgent, important)
   - Tags (#work, #urgent, #project)
   - Contexts (@office, @home, @phone)
   - Dates (today, tomorrow, this week, etc.)

2. Use the work-memo skill's `memo_command.py` script to record the information

3. Return a confirmation with:
   - Recorded title
   - Identified type
   - Priority levels
   - Eisenhower quadrant
   - Tags and contexts

### For URL Input

1. Validate the URL format
2. Fetch webpage content using `web_scraper.py`
3. Extract main content from the webpage
4. Generate a summary of the content
5. Record to database with:
   - Webpage title as record title
   - URL stored in contexts
   - Content summary in description
   - Default type: research
   - Default tags: web, reading
6. Return confirmation with:
   - Webpage title
   - URL
   - Content summary
   - Record details

## Examples

### Text Input Examples

- `/memo 紧急会议今天 #work @office` → Records an urgent meeting for today
- `/memo 完成项目报告` → Records a task to complete a project report
- `/memo 修复登录bug #urgent` → Records an urgent bug fix task
- `/memo 团队例会 #meeting` → Records a team meeting
- `/memo 重要电话明天 @phone` → Records an important phone call for tomorrow

### URL Input Examples

- `/memo https://example.com/article` → Fetches webpage, summarizes content, and records URL
- `/memo https://docs.python.org/tutorial` → Records Python tutorial webpage with summary
- `/memo https://github.com/project/readme #project` → Records GitHub README with project tag

## Supported Features

### Natural Language Elements

- **Tags**: Use # followed by tag name (e.g., #work, #urgent, #project)
- **Contexts**: Use @ followed by context (e.g., @office, @home, @phone)
- **Priority**: Words like "urgent", "important", "紧急", "重要"
- **Dates**: "today", "tomorrow", "this week", "今天", "明天", "本周"
- **URLs**: Provide a URL starting with http:// or https://

### Automatic Detection

The command automatically detects:
- **URL Input**: If input starts with http:// or https://
- **Work Type**: Based on keywords (meeting, call, bug, report, etc.)
- **Urgency Level**: 1-5 scale based on urgency indicators
- **Importance Level**: 1-5 scale based on importance indicators
- **Eisenhower Quadrant**: Q1-Q4 based on urgency/importance combination

### Webpage Processing

When a URL is provided:
- **Content Extraction**: Extracts main content from webpage
- **Summary Generation**: Creates a concise summary (first 300 characters)
- **URL Storage**: Records the URL in contexts for easy reference
- **Default Tags**: Adds 'web' and 'reading' tags automatically
- **Default Type**: Sets record type to 'research'

## Output Format

### Text Input Output

```json
{
  "status": "recorded",
  "title": "紧急会议",
  "type": "meeting",
  "urgency": 4,
  "importance": 3,
  "eisenhower_quadrant": "Q1",
  "tags": ["work"],
  "contexts": ["office"],
  "date": "2026-01-20"
}
```

### URL Input Output

```json
{
  "status": "success",
  "id": "123",
  "title": "Article Title",
  "url": "https://example.com/article",
  "summary": "Content summary...",
  "type": "research",
  "urgency": 3,
  "importance": 3,
  "tags": ["web", "reading"],
  "contexts": ["https://example.com/article"],
  "eisenhower": "Q2",
  "created_at": "2026-01-20T10:00:00"
}
```

## Notes

- This is a **record-only** command - no tasks are executed
- All information is stored in the work-memo database
- Use natural language for best results
- The more context you provide, the better the categorization
- For URLs: Content is fetched and summarized, but not executed
- URL records default to 'research' type with 'web' and 'reading' tags
- Requires internet connection for URL processing