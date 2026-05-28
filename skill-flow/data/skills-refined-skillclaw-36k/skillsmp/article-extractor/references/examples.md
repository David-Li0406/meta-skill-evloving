**Skill**: [MQL5 Article Extractor](../SKILL.md)

# MQL5 Article Extractor - Examples

## Example 1: Vague Request → Bounded Guidance

**User Input**: "I need to extract some trading articles"

**Skill Response**:

```
This skill extracts articles from mql5.com ONLY (not other trading sites).

Please specify one of:
1. MQL5 article URL: https://www.mql5.com/en/articles/[ID]
2. MQL5 user ID: numeric (29210372) or username (jslopes)
3. Path to text file containing article URLs

What would you like to extract?
```

---

## Example 2: Direct URL (Valid)

**User Input**: "Extract <https://www.mql5.com/en/articles/19625>"

**Skill Actions**:

1. Recognizes valid mql5.com URL
1. Executes single extraction:

   ```bash
   cd $HOME/eon/mql5
   .venv/bin/python mql5_extract.py single https://www.mql5.com/en/articles/19625
   ```

**Output**:

```
✅ Extraction successful!
   Article ID: 19625
   Title: Automating Trading Strategies in MQL5 (Part 34)...
   Author: Allan Munene Mutiiria
   Word count: 2,435
   Code blocks: 10
   Images: 9
   Output: $HOME/eon/mql5/mql5_articles/29210372/article_19625/
```

---

## Example 3: Out-of-Scope Domain (Rejected)

**User Input**: "Can you extract articles from Yahoo Finance?"

**Skill Response**:

```
❌ OUT OF SCOPE

This skill extracts from mql5.com ONLY. Yahoo Finance is not supported.

For general web scraping, use different tools or skills.

Valid inputs for this skill:
- mql5.com article URLs
- mql5.com user IDs
- Files containing mql5.com URLs
```

---

## Example 4: User ID Discovery (Valid)

**User Input**: "Get all articles from MQL5 user 29210372"

**Skill Actions**:

1. Validates user ID format
1. Confirms scope (mql5.com)
1. Checks article count
1. Prompts for confirmation if >10 articles

**Skill Response**:

```
User 29210372 has 77 articles on mql5.com.

Proceed with full extraction? This will:
- Take ~3-5 minutes (2s rate limit between articles)
- Download all images
- Create 77 article folders
- Generate ~400MB of data

Confirm? (Or use --max-articles 5 to test first)
```

**User**: "Yes"

**Skill Executes**:

```bash
cd $HOME/eon/mql5
.venv/bin/python mql5_extract.py discover-and-extract --user-id 29210372
```

---

## Example 5: Testing Limit (Bounded Operation)

**User Input**: "Test extraction with 3 articles from user jslopes"

**Skill Actions**:

```bash
cd $HOME/eon/mql5
.venv/bin/python mql5_extract.py discover-and-extract --user-id jslopes --max-articles 3
```

**Output**:

```
Discovered 12 articles for user jslopes
Limited to 3 articles

[Extraction progress...]

✅ Batch processing completed
Total: 3, Successful: 3, Failed: 0
Output: $HOME/eon/mql5/mql5_articles/jslopes/
```

---

## Example 6: Ambiguous Keywords (Prompt for Clarification)

**User Input**: "Extract trading strategies"

**Skill Response**:

```
"Trading strategies" could mean different sources.

This skill works with mql5.com ONLY.

Are you looking for:
1. Specific MQL5 article? → Provide URL
2. All articles from MQL5 author? → Provide user ID
3. Articles from different site? → Out of scope

Please clarify your request.
```

---

## Example 7: Batch File Processing (Valid)

**User Input**: "I have a file with 10 mql5 URLs, extract them all"

**Skill Actions**:

1. Ask for file path
1. Verify file exists
1. Preview first few URLs
1. Confirm all are mql5.com domain
1. Execute batch

**Skill Response**:

```
Please provide the file path containing URLs.
```

**User**: "/tmp/mql5_urls.txt"

**Skill Verifies**:

```bash
head -3 /tmp/mql5_urls.txt
# https://www.mql5.com/en/articles/19625
# https://www.mql5.com/en/articles/19624
# https://www.mql5.com/en/articles/19623
```

**Skill Executes**:

```bash
cd $HOME/eon/mql5
.venv/bin/python mql5_extract.py batch /tmp/mql5_urls.txt
```

---

## Example 8: Mixed Domain File (Reject Invalid)

**User Input**: "Extract from this file: mixed_urls.txt"

**File Contents**:

```
https://www.mql5.com/en/articles/19625
https://www.yahoo.com/finance/news/article
https://www.mql5.com/en/articles/19624
```

**Skill Response**:

```
❌ INVALID FILE

Line 2 contains non-mql5.com URL: https://www.yahoo.com/finance/news/article

This skill ONLY processes mql5.com URLs.

Options:
1. Remove non-mql5.com lines from file
2. Create mql5-only file
3. Extract valid URLs individually

Would you like me to filter and create mql5-only file?
```

---

## Example 9: Resume Interrupted Extraction (Valid)

**User Input**: "My batch extraction stopped at article 50, can I resume?"

**Skill Response**:

```
Yes! The checkpoint system saved your progress.

Resume command:
```

```bash
cd $HOME/eon/mql5
.venv/bin/python mql5_extract.py batch [original_file] --resume
```

```
This will skip the 50 already-processed articles and continue from article 51.

Checkpoint file: .extraction_checkpoint.json
```

---

## Example 10: Custom Output Location (Valid)

**User Input**: "Extract article 19625 to /tmp/test_output/"

**Skill Executes**:

```bash
cd $HOME/eon/mql5
.venv/bin/python mql5_extract.py --output /tmp/test_output single https://www.mql5.com/en/articles/19625
```

**Output**:

```
✅ Extraction successful!
Output: /tmp/test_output/29210372/article_19625/
```

---

## Bounding Summary

| User Intent                  | Skill Action           | Reason                     |
| ---------------------------- | ---------------------- | -------------------------- |
| "Extract mql5 article [URL]" | ✅ Execute             | Valid scope                |
| "Get user [ID] articles"     | ✅ Execute             | Valid scope                |
| "Extract from yahoo.com"     | ❌ Reject              | Out of scope               |
| "Extract trading articles"   | ⚠️ Prompt              | Ambiguous - need specifics |
| "Process URLs in [file]"     | ✅ Verify then execute | Valid if all mql5.com      |
| "Extract 1000 articles"      | ⚠️ Confirm             | Large operation warning    |
| "Scrape bloomberg"           | ❌ Reject              | Out of scope               |

---

## Skill Activation Keywords

The skill activates on:

- "mql5", "MQL5", "mql5.com"
- "MetaTrader", "MT5"
- "trading articles", "algorithmic trading"
- "extract mql5", "scrape mql5"
- URLs containing "mql5.com"

The skill rejects on:

- Other domains (yahoo, google, reuters, bloomberg, etc.)
- General "extract articles" without mql5 context
- Non-trading content requests
