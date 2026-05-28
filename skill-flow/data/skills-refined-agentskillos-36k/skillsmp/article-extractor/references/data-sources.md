**Skill**: [MQL5 Article Extractor](../SKILL.md)

### Topic Collections

#### TICK Data Research (`mql5_articles/tick_data/`)

- **Official Docs**: 3 Python MetaTrader5 TICK functions
  - `copy_ticks_from`, `copy_ticks_range`, `symbol_info_tick`
- **User Articles**: 9 articles on TICK data handling, storage, and analysis
- **Research Documentation**: `/docs/tick_research/` (4 files)

#### Python Integration (`mql5_articles/python_integration/`)

- **Official Docs**: 32 complete Python MetaTrader5 API functions
  - Connection, account info, symbol management, historical data, orders, positions
- **User Articles**: 15 implementation guides
  - ML/AI integration, trading automation, data analysis, socket communication
- **Research Documentation**: `/docs/python_research/` (1 file)

## Input Validation Workflow

When user makes vague request:

1. **Ask for domain confirmation** (if ambiguous):
   - "Is this for mql5.com articles? (This tool only works with mql5.com)"

1. **Request specific input**:
   - "Please provide one of:
     - Article URL: <https://www.mql5.com/en/articles/[ID>]
     - User ID: numeric or username from mql5.com profile
     - Path to file with article URLs"

1. **Suggest scope limits**:
   - "For testing, use --max-articles N to limit quantity"
   - "For production, omit limit to extract all"

1. **Confirm before large operations**:
   - If user says "all articles" → ask "User X has Y articles. Proceed with full extraction?"

## Common Usage Examples

### Example 1: Vague → Specific (Guided)

**User**: "Extract some trading articles"
**Skill**: "This extracts from mql5.com only. Please specify:

1. Article URL (<https://www.mql5.com/en/articles/[ID>])
1. MQL5 user ID (e.g., 29210372)
1. Path to URL file

Which do you have?"

**User**: "User 29210372"
**Skill**:

```bash
cd $HOME/eon/mql5
.venv/bin/python mql5_extract.py discover-and-extract --user-id 29210372
```

### Example 2: URL Provided (Direct)

**User**: "Extract <https://www.mql5.com/en/articles/19625>"
**Skill**:

```bash
cd $HOME/eon/mql5
.venv/bin/python mql5_extract.py single https://www.mql5.com/en/articles/19625
```

### Example 3: Out of Scope (Reject)

**User**: "Extract articles from reuters.com"
**Skill**: "This skill extracts from mql5.com ONLY. Reuters is not supported. Use general web scraping tools instead."

### Example 4: Testing (Limited)

**User**: "Test with 5 articles from user jslopes"
**Skill**:

```bash
cd $HOME/eon/mql5
.venv/bin/python mql5_extract.py discover-and-extract --user-id jslopes --max-articles 5
```

## Output Structure

All extractions go to:

```
mql5_articles/
├── 29210372/                 # User collections (numeric ID or username)
│   └── article_[ID]/
│       ├── article_[ID].md
│       ├── metadata.json
│       └── images/
├── tick_data/                # Topic collections
│   ├── official_docs/        # 3 Python MT5 TICK functions
│   │   ├── copy_ticks_from.md
```
