# Search Strategies Reference

Comprehensive keyword lists and search patterns for GitHub repository discovery.

## BidDeed.AI Focus Areas

### Foreclosure/Legal Domain
**Primary Keywords:**
- foreclosure auction, foreclosure data, foreclosure scraper
- legal document parsing, court records scraping
- auction bidding algorithm, auction automation
- lien search, title search automation

**Technology Keywords:**
- Python scraping, BeautifulSoup, Selenium, Playwright
- PDF extraction, OCR, document parsing
- legal data extraction, court data API

**Example Searches:**
```
site:github.com foreclosure auction scraper Python stars:>50
site:github.com legal document parsing PDF OCR
site:github.com court records data extraction stars:>100
site:github.com auction bidding algorithm machine learning
```

### Real Estate Data
**Primary Keywords:**
- property valuation, property appraisal API
- real estate data pipeline, MLS integration
- parcel data, GIS property data
- comparative market analysis, CMA automation

**Technology Keywords:**
- Zillow API, Redfin scraper, Realtor.com
- property database, real estate analytics
- geocoding, address standardization

**Example Searches:**
```
site:github.com property valuation API Python stars:>100
site:github.com real estate data pipeline scraper
site:github.com parcel GIS property mapping
site:github.com comparative market analysis CMA
```

### Machine Learning / Prediction
**Primary Keywords:**
- XGBoost real estate, property price prediction
- auction outcome prediction, bidding optimization
- real estate machine learning, housing market ML

**Technology Keywords:**
- scikit-learn real estate, pandas property analysis
- feature engineering real estate, model deployment

**Example Searches:**
```
site:github.com XGBoost property prediction Python stars:>200
site:github.com real estate price prediction machine learning
site:github.com auction bidding optimization algorithm
```

### Document Processing
**Primary Keywords:**
- PDF form filling, DOCX automation
- automated report generation, document templates
- mail merge, dynamic document creation

**Technology Keywords:**
- python-docx, pdfplumber, ReportLab
- Jinja2 templates, document generation

**Example Searches:**
```
site:github.com PDF form filling Python stars:>300
site:github.com DOCX automation python-docx
site:github.com automated report generation templates
```

### Geospatial / Mapping
**Primary Keywords:**
- property mapping, interactive maps
- GIS parcel data, geocoding service
- Leaflet property map, Mapbox real estate

**Technology Keywords:**
- Leaflet.js, Mapbox GL, OpenStreetMap
- geojson, spatial analysis, distance calculation

**Example Searches:**
```
site:github.com property mapping Leaflet stars:>500
site:github.com GIS parcel data visualization
site:github.com Mapbox real estate interactive map
```

---

## Life OS Focus Areas

### Productivity / ADHD Management
**Primary Keywords:**
- ADHD task management, ADHD productivity
- focus timer, Pomodoro technique
- habit tracking, routine automation
- time blocking, task breakdown

**Technology Keywords:**
- TypeScript productivity, React task manager
- habit tracker, time tracking automation

**Example Searches:**
```
site:github.com ADHD task management TypeScript stars:>100
site:github.com focus timer Pomodoro React
site:github.com habit tracking automation
site:github.com time blocking productivity app
```

### Timezone Management
**Primary Keywords:**
- dual timezone, timezone conversion
- calendar sync, cross-timezone scheduling
- time zone aware, multi-timezone display

**Technology Keywords:**
- moment-timezone, Luxon, date-fns-tz
- calendar API, scheduling automation

**Example Searches:**
```
site:github.com dual timezone calendar sync stars:>200
site:github.com timezone conversion scheduling
site:github.com multi-timezone display widget
```

### Learning / Knowledge Management
**Primary Keywords:**
- knowledge base, personal wiki
- note-taking automation, note sync
- learning analytics, spaced repetition
- second brain, Zettelkasten

**Technology Keywords:**
- Markdown knowledge base, Obsidian plugins
- Notion API, note automation
- flashcard system, learning tracker

**Example Searches:**
```
site:github.com knowledge base Markdown stars:>500
site:github.com note-taking automation sync
site:github.com spaced repetition learning
site:github.com Zettelkasten second brain
```

### Family / Personal Management
**Primary Keywords:**
- meal planning, recipe manager
- kosher recipe API, dietary tracking
- family calendar, shared calendar sync
- grocery list automation

**Technology Keywords:**
- recipe scraper, nutrition API
- calendar integration, family organization

**Example Searches:**
```
site:github.com meal planning recipe API Python stars:>100
site:github.com kosher recipe database
site:github.com family calendar sync automation
```

### Athletics / Swimming
**Primary Keywords:**
- sports analytics, swim timing
- athletic performance tracking
- recruiting database, athlete stats
- meet results parser

**Technology Keywords:**
- sports statistics, performance metrics
- data visualization sports, athlete tracking

**Example Searches:**
```
site:github.com sports analytics Python stars:>100
site:github.com swim timing performance tracking
site:github.com athlete recruiting database
site:github.com meet results parser scraper
```

---

## Advanced Search Operators

### GitHub-Specific Operators
```
site:github.com                   # Limit to GitHub
stars:>100                        # Minimum stars
pushed:>2024-01-01                # Recently updated
language:Python                   # Specific language
created:>2023-01-01               # Created after date
fork:false                        # Exclude forks
size:<1000                        # Repository size (KB)
```

### Combining Operators
```
site:github.com foreclosure scraper language:Python stars:>50 pushed:>2024-01-01
site:github.com ADHD productivity language:TypeScript stars:>100 fork:false
site:github.com property valuation API Python stars:>200 pushed:>2023-01-01
```

### Exclusion Patterns
```
-tutorial                         # Exclude tutorials
-example -learning -course        # Exclude educational repos
-clone -copy                      # Exclude copies
-deprecated -archived             # Exclude abandoned
```

---

## Multi-Angle Search Strategies

### Pattern: Technology Discovery
For discovering tools in a specific domain:

1. **Broad domain search**
   - `site:github.com [domain] stars:>100`
2. **Technology-specific**
   - `site:github.com [domain] [tech-stack] stars:>50`
3. **Problem-statement**
   - `site:github.com [specific-problem] [language]`
4. **Alternative terms**
   - `site:github.com [synonym1] OR [synonym2] stars:>100`

**Example: Email Parsing**
```
1. site:github.com email parser stars:>100
2. site:github.com email parsing Python IMAP stars:>50
3. site:github.com parse confirmation email automation
4. site:github.com email extraction OR email scraping stars:>100
```

### Pattern: Framework Research
For finding implementations using specific frameworks:

1. **Framework name**
   - `site:github.com [framework-name] stars:>500`
2. **Framework + domain**
   - `site:github.com [framework] [domain] example`
3. **Framework + use-case**
   - `site:github.com [framework] [use-case] production`

**Example: LangGraph Research**
```
1. site:github.com LangGraph stars:>500
2. site:github.com LangGraph multi-agent workflow
3. site:github.com LangGraph production orchestration
```

### Pattern: Best Practices Discovery
For learning from high-quality projects:

1. **Awesome list**
   - `site:github.com awesome [domain] stars:>1000`
2. **Highly-starred domain repos**
   - `site:github.com [domain] stars:>5000`
3. **Official examples**
   - `site:github.com [org-name] [framework] examples`

**Example: React Best Practices**
```
1. site:github.com awesome react stars:>1000
2. site:github.com react application stars:>5000
3. site:github.com facebook react examples
```

---

## Quality Filters

### High-Quality Repository Signals
Search for repos that have:
- Comprehensive README with examples
- CI/CD badges (GitHub Actions, Travis, CircleCI)
- Active issues/PRs (community engagement)
- Tests directory
- Clear installation instructions
- LICENSE file
- Contributing guidelines

### Maintenance Indicators
- **Last commit:** within 6 months = active
- **Commit frequency:** regular commits = maintained
- **Issue response time:** quick responses = healthy
- **PR merge rate:** accepted PRs = collaborative

### Red Flags to Avoid
- No commits in 18+ months (unless very highly starred)
- Archived/deprecated status
- No documentation or README
- No license specified
- Excessive open issues with no responses
- Forks with fewer stars than original

---

## Domain-Specific Search Examples

### BidDeed.AI: Lien Discovery Enhancement
**Goal:** Find tools for automated legal document parsing

**Search Sequence:**
1. `site:github.com legal document parsing OCR Python stars:>50`
2. `site:github.com court records scraper PDF extraction`
3. `site:github.com mortgage lien search automation`
4. `site:github.com title search property records`

**Expected Results:**
- OCR libraries (Tesseract wrappers, AWS Textract)
- PDF parsing tools (pdfplumber, PyPDF2 advanced)
- Legal data scrapers (court record APIs)

### Life OS: ADHD Task Breakdown
**Goal:** Find task management with ADHD-specific features

**Search Sequence:**
1. `site:github.com ADHD task management productivity stars:>100`
2. `site:github.com time blocking focus timer React`
3. `site:github.com task breakdown subtask automation`
4. `site:github.com habit tracking ADHD executive function`

**Expected Results:**
- Focus timer apps (Pomodoro, time boxing)
- Task breakdown tools (automated subtask generation)
- Habit trackers with ADHD accommodations

### Both Projects: Real-Time Collaboration
**Goal:** Find websocket/real-time tech for collaborative features

**Search Sequence:**
1. `site:github.com real-time collaboration websocket stars:>500`
2. `site:github.com collaborative editing React TypeScript`
3. `site:github.com websocket server Node.js production`
4. `site:github.com operational transform CRDT`

**Expected Results:**
- WebSocket libraries (Socket.io, ws)
- Collaborative editing frameworks (Yjs, Automerge)
- Real-time sync patterns (OT, CRDT)