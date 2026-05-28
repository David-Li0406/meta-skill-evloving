# Market Analysis Framework

## Purpose

Size the opportunity and understand market dynamics. Answer: "Is this market worth entering?"

---

## TAM/SAM/SOM Methodology

### Total Addressable Market (TAM)

**Definition:** The total global demand for the product/service if there were no competitors and no limitations.

**How to calculate:**
1. **Top-down:** Industry reports, analyst estimates
2. **Bottom-up:** # of potential users × average revenue per user

**Search queries:**
```
"{industry} market size 2024 2025"
"{product category} total addressable market"
"{industry} market research report"
```

**Sources to check:**
- Statista
- IBISWorld
- Grand View Research
- Allied Market Research
- Mordor Intelligence

### Serviceable Addressable Market (SAM)

**Definition:** The portion of TAM that you can realistically reach with your business model.

**Filters to apply:**
- Geographic constraints (where can you operate?)
- Language constraints
- Technical constraints (web only? mobile only?)
- Segment focus (SMB? Enterprise? Consumer?)

**Formula:**
```
SAM = TAM × (target segment % of total market)
```

### Serviceable Obtainable Market (SOM)

**Definition:** The realistic portion of SAM you can capture in 1-3 years.

**For solo builder, be conservative:**
- First year: 0.1% - 0.5% of SAM is optimistic
- With traction: 1-2% might be achievable
- Market leader rarely exceeds 30% of SAM

**Solo builder reality check:**
```
If SAM = $100M
Conservative SOM = $100K - $500K (0.1% - 0.5%)
That's still potentially $8K - $40K MRR
```

---

## Market Trends Analysis

### Growth Rate

**What to find:**
- Historical CAGR (Compound Annual Growth Rate)
- Projected growth rate
- Growth drivers

**Healthy signs:**
- CAGR > 10% = Growing market
- CAGR 5-10% = Stable market
- CAGR < 5% = Mature/declining

**Search queries:**
```
"{industry} growth rate CAGR"
"{industry} market forecast 2025 2030"
"{industry} trends driving growth"
```

### Trend Categories

| Trend Type | What to Look For |
|------------|------------------|
| Technology | New capabilities enabling solutions |
| Regulatory | Laws creating demand or barriers |
| Social | Behavioral shifts creating needs |
| Economic | Spending pattern changes |
| Competitive | Consolidation, new entrants |

### Trend Signals

**Positive signals:**
- Increasing search volume for problem/solution
- Growing Reddit/forum discussions
- New funding in the space
- Big players entering/acquiring
- Regulatory tailwinds

**Negative signals:**
- Declining search interest
- Market consolidation without growth
- Regulatory headwinds
- Big players exiting
- Commoditization

---

## Timing Assessment

### Market Timing Framework

| Timing | Characteristics | Strategy |
|--------|-----------------|----------|
| **Too Early** | Problem exists but market not ready, no willingness to pay | Wait or educate (expensive) |
| **Early Adopter** | Problem recognized, few solutions, willing to pay premium | Move fast, capture early users |
| **Growth** | Multiple solutions, market expanding rapidly | Differentiate, find niche |
| **Mature** | Established players, slow growth | Disrupt or avoid |
| **Declining** | Shrinking demand, consolidation | Avoid unless repositioning |

### Timing Signals

**Too early:**
- Lots of "what is {concept}?" searches
- Investors asking "what's the market?"
- Users don't understand the problem
- Infrastructure not ready

**Just right:**
- "Best {solution}" searches growing
- Competitors getting funded
- Users actively seeking solutions
- Adjacent problems being solved

**Too late:**
- Market dominated by 2-3 players
- Commoditized pricing
- Users satisfied with current solutions
- Innovation happening elsewhere

---

## Solo Builder Market Fit

### Ideal Market Characteristics

| Factor | Ideal for Solo Builder |
|--------|------------------------|
| Size | $100M - $1B SAM (big enough to matter, not attracting giants) |
| Growth | 10-30% CAGR (growing but not explosive) |
| Fragmentation | Many small players (no dominant winner) |
| Buyer | SMB or prosumer (shorter sales cycles) |
| Pricing | $20-500/mo (sustainable, not enterprise complexity) |
| Technology | Web-first (deployable by one person) |

### Markets to Avoid (for Solo)

- Enterprise-only (long sales cycles)
- Hardware-dependent (capital intensive)
- Highly regulated (compliance burden)
- Network-effect dependent (need critical mass)
- Low ARPU high volume (need scale)

---

## Data Sources

### Free Sources

| Source | Best For |
|--------|----------|
| Google Trends | Search interest over time |
| Statista (limited free) | Industry statistics |
| Crunchbase | Funding activity |
| SimilarWeb (limited) | Traffic estimates |
| LinkedIn | Company sizes, hiring |

### Search Patterns

```
# Market size
"{industry} market size 2024" OR "{industry} market size 2025"
"{industry} market research report free"

# Growth
"{industry} CAGR" OR "{industry} growth rate"
"{industry} market forecast"

# Trends
"{industry} trends 2024 2025"
"future of {industry}"
"{industry} emerging opportunities"

# Validation
"site:crunchbase.com {industry} funding"
"{industry} startups raised"
```

---

## Output Format

```markdown
## Market Analysis

### Market Size

| Metric | Value | Source |
|--------|-------|--------|
| TAM | ${X}B | {source} |
| SAM | ${X}M | Calculated: {explanation} |
| SOM (Year 1) | ${X}K | Conservative estimate |

### Growth & Trends

**Growth Rate:** {X}% CAGR (2024-2030)

**Key Trends:**
1. {Trend 1} - {Impact}
2. {Trend 2} - {Impact}
3. {Trend 3} - {Impact}

### Timing Assessment

**Current Phase:** {Too Early / Early Adopter / Growth / Mature / Declining}

**Evidence:**
- {Signal 1}
- {Signal 2}
- {Signal 3}

### Solo Builder Fit

**Fit Score:** {High / Medium / Low}

**Rationale:**
- Market size: {Assessment}
- Buyer type: {Assessment}
- Competition level: {Assessment}
- Technical feasibility: {Assessment}
```

---

## Red Flags

- Can't find market size data (market may not exist)
- All reports are 3+ years old (outdated space)
- Only enterprise players (not solo-friendly)
- Negative growth projections
- High regulatory mentions
- Requires physical infrastructure
