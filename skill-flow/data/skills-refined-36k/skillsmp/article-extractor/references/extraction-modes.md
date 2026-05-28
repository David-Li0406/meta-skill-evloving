**Skill**: [MQL5 Article Extractor](../SKILL.md)

## Extraction Modes

### Mode 1: Single Article

**When**: User provides one article URL
**Command**:

```bash
.venv/bin/python mql5_extract.py single https://www.mql5.com/en/articles/[ID]
```

**Output**: `mql5_articles/[user_id]/article_[ID]/`

### Mode 2: Batch from File

**When**: User has URL file or wants multiple specific articles
**Command**:

```bash
.venv/bin/python mql5_extract.py batch urls.txt
```

**Checkpoint**: Auto-saves progress, resumable with `--resume`

### Mode 3: Auto-Discovery

**When**: User provides MQL5 user ID or username
**Command**:

```bash
.venv/bin/python mql5_extract.py discover-and-extract --user-id [USER_ID]
```

**Discovers**: All published articles for that user

## Official Documentation Extraction

### Mode 4: Official Docs (Single Page)

**When**: User wants official MQL5/Python MetaTrader5 documentation (not user articles)

**Scripts Location**: `/scripts/official_docs_extractor.py`

**Command**:

```bash
cd $HOME/eon/mql5
curl -s "https://www.mql5.com/en/docs/python_metatrader5/mt5copyticksfrom_py" > page.html
.venv/bin/python scripts/official_docs_extractor.py page.html "URL"
```

**Output**: Markdown file with source URL, HTML auto-deleted

### Mode 5: Batch Official Docs

**When**: User wants all Python MetaTrader5 API documentation

**Scripts Location**: `/scripts/extract_all_python_docs.sh`

**Command**:

```bash
cd $HOME/eon/mql5
./scripts/extract_all_python_docs.sh
```

**Result**: 32 official API function docs extracted

### Key Differences from User Articles

- Different HTML structure (div.docsContainer vs div.content)
- Inline tables and code examples preserved
- No images (documentation only)
- Simpler file naming (function_name.md)
- Source URLs embedded in markdown
- HTML files auto-deleted after conversion

## Data Sources

### User Collections

- **Primary Source**: <https://www.mql5.com/en/users/29210372/publications>
- **Author**: Allan Munene Mutiiria (77 technical articles)
- **Content Type**: MQL5 trading strategy implementations
