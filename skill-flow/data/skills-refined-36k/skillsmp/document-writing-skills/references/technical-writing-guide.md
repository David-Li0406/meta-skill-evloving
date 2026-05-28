# Technical Writing Best Practices

This reference provides detailed guidance on technical writing style, grammar, and conventions.

## Style Guide Principles

### Voice and Tense

**Active Voice** (Preferred):
```
✅ The function returns a string.
✅ Click the Save button.
✅ The system processes requests in parallel.

❌ A string is returned by the function.
❌ The Save button should be clicked.
❌ Requests are processed in parallel by the system.
```

**Present Tense** (Preferred):
```
✅ The API returns JSON responses.
✅ When you click Submit, the form validates input.
✅ The database stores user credentials.

❌ The API will return JSON responses.
❌ When you click Submit, the form will validate input.
❌ The database would store user credentials.
```

### Person and Perspective

**Second Person for Instructions** (You):
```
✅ You can configure the timeout value in settings.
✅ To delete a record, click the trash icon.

❌ One can configure the timeout value in settings.
❌ The user should click the trash icon to delete a record.
```

**Third Person for Technical Description**:
```
✅ The function accepts two parameters.
✅ The service authenticates requests using JWT tokens.

❌ You accept two parameters in the function.
```

### Sentence Structure

**Short Sentences** (15-20 words ideal):
```
✅ The API endpoint accepts GET requests. It returns user data in JSON format.

❌ The API endpoint accepts GET requests and returns user data in JSON format, which includes fields for username, email, created date, and last login timestamp.
```

**Parallel Structure** in Lists:
```
✅ The function:
- Validates input parameters
- Processes the request
- Returns a response

❌ The function:
- Validates input parameters
- Processing of the request
- A response is returned
```

## Grammar and Punctuation

### Oxford Comma

**Always use** the Oxford (serial) comma:
```
✅ The API supports JSON, XML, and YAML formats.
❌ The API supports JSON, XML and YAML formats.
```

### Hyphens and Dashes

**Hyphen (-)** for compound modifiers:
```
✅ high-availability system
✅ real-time processing
✅ user-defined parameters
```

**En dash (–)** for ranges:
```
✅ Pages 10–15
✅ 2020–2025
✅ Monday–Friday
```

**Em dash (—)** for breaks in thought:
```
✅ The system—when properly configured—can handle 1M requests per second.
```

### Capitalization

**Title Case** for headings (major words capitalized):
```
✅ Getting Started with the API
✅ User Authentication and Authorization
❌ Getting started with the API
```

**Sentence case** for subheadings (only first word capitalized):
```
✅ Installing the required dependencies
✅ Configuring environment variables
❌ Installing The Required Dependencies
```

**Proper nouns** always capitalized:
```
✅ Python, JavaScript, PostgreSQL, AWS
❌ python, javascript, postgresql, aws
```

## Terminology and Word Choice

### Precision Over Vagueness

```
✅ Response time: 200ms (p95)
❌ Response time is fast

✅ Supports up to 10,000 concurrent connections
❌ Supports many concurrent connections

✅ Database is replicated across 3 availability zones
❌ Database is highly available
```

### Consistent Terminology

**Create a glossary** for domain terms:
```
✅ Throughout document: "authentication" (not mixing with "login", "sign-in", "auth")
✅ Throughout document: "endpoint" (not mixing with "API", "route", "path")
```

**Avoid synonyms** for technical terms:
```
❌ In paragraph 1: "Click the button"
   In paragraph 2: "Press the button"
   In paragraph 3: "Tap the button"

✅ Consistently: "Click the button"
```

### Common Word Choices

| Avoid | Prefer |
|-------|--------|
| utilize | use |
| in order to | to |
| at this point in time | now |
| due to the fact that | because |
| in the event that | if |
| please be advised that | (omit) |
| it should be noted that | (omit) |

## Numbers and Measurements

### Writing Numbers

**Spell out** numbers one through nine:
```
✅ The function takes three parameters.
✅ Configure the system with four replicas.
```

**Use numerals** for 10 and above:
```
✅ The database contains 15,000 records.
✅ Set timeout to 30 seconds.
```

**Always use numerals** for:
- Technical values: `3 GB RAM`, `5 ms latency`
- Versions: `version 2.0`, `Python 3.9`
- Percentages: `95% uptime`, `2% error rate`
- Currency: `$50`, `EUR 100`

### Units of Measurement

**Use standard abbreviations**:
```
✅ 100 ms (milliseconds)
✅ 5 GB (gigabytes)
✅ 2.5 GHz (gigahertz)

❌ 100 milliseconds
❌ 5 gigabytes
```

**Include space** between number and unit:
```
✅ 256 MB
✅ 3.2 GHz

❌ 256MB
❌ 3.2GHz
```

**Exception**: Percentages and degrees:
```
✅ 95%
✅ 90°
```

## Lists and Formatting

### When to Use Lists

**Numbered lists** for:
- Sequential steps
- Ranked items
- Items with specific order

**Bulleted lists** for:
- Unordered items
- Features or benefits
- Options or alternatives

### List Formatting

**Consistent punctuation**:
```
✅ Requirements:
- Python 3.9 or higher
- PostgreSQL 13+
- Redis 6.0+

✅ The function:
1. Validates input parameters.
2. Processes the request.
3. Returns a response.

❌ Requirements:
- Python 3.9 or higher.
- PostgreSQL 13+
- Redis 6.0+. (inconsistent)
```

**Parallel structure**:
```
✅ The system can:
- Process requests
- Store data
- Generate reports

❌ The system can:
- Process requests
- Data storage
- Generating reports
```

## Code Examples

### Inline Code

Use backticks for:
- Variable names: `user_id`
- Function names: `getUserData()`
- File names: `config.json`
- Commands: `npm install`
- Short code snippets: `if (x > 0)`

### Code Blocks

**Always specify language** for syntax highlighting:
````markdown
```python
def calculate_total(items):
    return sum(item.price for item in items)
```

```javascript
const calculateTotal = (items) => {
  return items.reduce((sum, item) => sum + item.price, 0);
};
```

```bash
npm install express
npm start
```
````

**Include context and output**:
````markdown
```python
# Example: Calculate average response time
response_times = [120, 145, 98, 203]
average = sum(response_times) / len(response_times)
print(f"Average: {average}ms")
```

**Output**:
```
Average: 141.5ms
```
````

## Links and References

### Link Text

**Use descriptive link text**:
```
✅ See the [Authentication Guide](link) for details.
✅ For more information, refer to [PostgreSQL Documentation](link).

❌ Click [here](link) for the guide.
❌ More info [here](link).
```

### Version Pinning

**Pin versions** in links when possible:
```
✅ https://docs.python.org/3.9/library/json.html
❌ https://docs.python.org/library/json.html (version may change)
```

### Internal Cross-References

```
✅ See Section 3.2 for configuration details.
✅ As described in [Chapter 1](#chapter-1), the system uses JWT tokens.

❌ See above for configuration.
❌ As mentioned earlier, the system uses JWT tokens.
```

## Inclusive and Accessible Language

### Gender-Neutral Language

```
✅ The developer can configure their environment.
✅ Each user has their own dashboard.

❌ The developer can configure his environment.
```

### Avoid Ableist Language

| Avoid | Prefer |
|-------|--------|
| dummy variable | placeholder variable |
| kill the process | stop/terminate the process |
| sanity check | validation check |
| master/slave | primary/replica, leader/follower |

### Plain Language

**Avoid jargon** when simpler terms work:
```
✅ The system is not working correctly.
❌ The system is exhibiting anomalous behavior.

✅ This feature is experimental.
❌ This feature is in alpha stage of development lifecycle.
```

## Localization Considerations

### Date and Time Formats

**Use ISO 8601** for unambiguous dates:
```
✅ 2025-11-08 (YYYY-MM-DD)
✅ 2025-11-08T14:30:00Z (with time)

❌ 11/08/2025 (ambiguous: US vs EU format)
❌ 8 Nov 2025 (locale-dependent)
```

### Number Formats

**Use locale-neutral formats** in technical docs:
```
✅ 1,234,567 (with comma separators)
✅ 3.14159 (period for decimal)

Context-dependent: EUR 1.234,56 (European format when specifically discussing European currency)
```

### Currency

**Specify currency code**:
```
✅ USD 50
✅ EUR 100
✅ GBP 75

❌ $50 (which dollar?)
❌ €100 (may not render correctly)
```

### Avoid Culture-Specific References

```
❌ "The system is as easy as pie."
❌ "Click on the hamburger icon." (without visual)
❌ "On the top-left" (assumes LTR reading)

✅ "The system is easy to use."
✅ "Click the menu icon (☰)."
✅ "In the navigation area" (more universal)
```

## Document Metadata

### Standard Header

```markdown
---
title: [Document Title]
author: [Author Name]
date: 2025-11-08
version: 1.0.0
status: [Draft/Final/Deprecated]
audience: [Developers/End Users/Administrators]
---
```

### Version History

```markdown
## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-08 | J. Smith | Initial release |
| 1.1.0 | 2025-11-15 | J. Smith | Added API examples |
| 2.0.0 | 2025-12-01 | M. Jones | Breaking changes to authentication |
```

### Last Updated

**Include last updated date**:
```markdown
---
**Last updated**: 2025-11-08
**Next review**: 2026-02-08
---
```

## Accessibility (WCAG AA)

### Heading Hierarchy

**Use proper heading levels**:
```markdown
# H1: Document Title (only one per document)
## H2: Major Section
### H3: Subsection
#### H4: Sub-subsection

❌ Skipping levels (H1 → H3)
❌ Using headings for styling only
```

### Alt Text for Images

```markdown
✅ ![Architecture diagram showing client, API server, and database](./architecture.png)
❌ ![diagram](./architecture.png)
❌ ![](./architecture.png)
```

### Color and Contrast

**Don't rely on color alone**:
```
✅ **Error** (in red): Invalid input
✅ ✓ Success | ✗ Failure (icons + color)

❌ See the red text for errors
❌ Green = success, Red = failure (color only)
```

### Link Text

```
✅ Download the [User Guide (PDF, 2.3 MB)](link)

❌ [Click here](link) to download
```

## Common Mistakes to Avoid

### Overuse of Passive Voice

```
❌ "The configuration file is read by the application."
✅ "The application reads the configuration file."
```

### Ambiguous Pronouns

```
❌ "When the API calls the database, it returns a response."
   (What does "it" refer to?)

✅ "When the API calls the database, the database returns a response."
```

### Future Tense in Documentation

```
❌ "The function will validate input."
✅ "The function validates input."
```

### Unclear Instructions

```
❌ "Configure the system appropriately."
✅ "Set the timeout value to 30 seconds in config.json."
```

### Missing Context in Examples

```
❌
```python
result = calculate(x, y)
```

✅
```python
# Calculate the sum of two numbers
x = 10
y = 20
result = calculate(x, y)  # Returns: 30
```
```

## Summary

Technical writing requires:
1. **Clarity**: Active voice, present tense, short sentences
2. **Consistency**: Terminology, formatting, structure
3. **Precision**: Specific values, not vague descriptions
4. **Accessibility**: Proper headings, alt text, inclusive language
5. **Completeness**: Context, examples, expected output
