**Skill**: [MQL5 Article Extractor](../SKILL.md)

│ │ ├── copy*ticks_range.md
│ │ └── symbol_info_tick.md
│ └── user_articles/ # 9 articles by author
│ ├── artmedia70/article*[ID]/
│ ├── lazymesh/article*[ID]/
│ └── ...
├── python_integration/ # Topic collections
│ ├── official_docs/ # 32 MT5 Python API functions
│ │ ├── mt5initialize_py.md
│ │ ├── mt5copyticksfrom_py.md
│ │ └── ...
│ └── user_articles/ # 15 implementation articles
│ ├── dmitrievsky/article*[ID]/
│ ├── koshtenko/article\_[ID]/
│ └── ...
├── extraction_summary.json
└── extraction.log

`````

**Content Organization:**

- **User Collections** (e.g., `29210372/`): Articles by specific authors
- **Topic Collections** (e.g., `tick_data/`, `python_integration/`): Organized by research area
  - `official_docs/`: Official MQL5 documentation pages
  - `user_articles/`: Community-contributed articles by author

## Quality Verification

After extraction, verify outputs:

````bash
# Count articles extracted
find mql5_articles/ -name "article_*.md" | wc -l

# Check MQL5 code blocks
grep -r "```mql5" mql5_articles/ | wc -l

# View summary
cat mql5_articles/extraction_summary.json
`````

## Error Handling

If extraction fails:

1. Check logs: `tail -f logs/extraction.log`
1. Verify URL is mql5.com domain
1. Check internet connection
1. For batch: use `--resume` to continue from checkpoint

## CLI Options Reference

**Global options** (before subcommand):

- `--output DIR` - Custom output directory
- `--config FILE` - Custom config file
- `--verbose` - Debug logging
- `--quiet` - Error-only logging

**Batch options**:

- `--resume` - Continue from checkpoint
- `--no-checkpoint` - Disable checkpoint system
- `--max-articles N` - Limit to N articles

**Discovery options**:

- `--user-id ID` - MQL5 user ID or username
- `--save-urls FILE` - Save discovered URLs to file
- `--max-articles N` - Limit extraction

## Input Bounding Rules

**Rule 1: Domain Validation**
Only accept `mql5.com` URLs. Reject all other domains immediately.

**Rule 2: Input Type Classification**
Classify user input as:

- URL pattern → single extraction
- Numeric/username → discovery
- File path → batch
- Ambiguous → prompt for clarification

**Rule 3: Scope Enforcement**
If user mentions keywords like "yahoo", "google", "reuters", "bloomberg" → respond with scope limitation message.

**Rule 4: Confirmation for Large Operations**
If discovery would extract >10 articles, confirm with user before proceeding.

## Security Notes

- Only executes within `$HOME/eon/mql5`
- Uses virtual environment `.venv/bin/python`
- No network tools allowed (uses Playwright internally)
- Rate limiting enforced (2s between articles)
- Checkpoint files in project root only

## Typical Interaction Flow

1. User mentions MQL5 or trading articles
1. Skill activates and bounds request to mql5.com
1. If input vague → prompt for specifics (URL, user ID, or file)
1. Validate input type and domain
1. Execute appropriate command
1. Show output location and verification commands

## Success Indicators

After execution, report:

- Number of articles extracted
- Total word count
- Code blocks found
- Images downloaded
- Output directory location
- Link to extraction summary

---

**Remember**: This skill ONLY works with mql5.com. Any request for other domains is out of scope and should be rejected with a clear message.
