---
name: proptraderai-strategy-builder
description: Extract executable futures trading strategies through Socratic dialogue (one question at a time, progressive clarification) for PropTraderAI's prop trading platform. Use when users describe trading strategies, want to automate trading setups, mention futures contracts (ES, NQ, MES, MNQ, YM, CL, RTY, GC), discuss prop firms (Topstep, FTMO, Apex, Earn2Trade, etc.), or build strategies for funded challenges. Handles natural language parsing, timezone conversion (trader TZ to exchange time), contract specifications, tick value calculations, position sizing, risk management, stop loss validation, prop firm rule compliance (drawdown limits, daily loss, consistency rules), and behavioral data capture. Designed for traders passing prop firm evaluations.
---

# PropTraderAI Strategy Builder Skill

**Version:** 1.0  
**Last Updated:** January 2026  
**Purpose:** Extract executable futures trading strategies through Socratic dialogue while respecting prop firm constraints and capturing behavioral data

---

## Mission

Extract executable futures trading strategies through Socratic dialogue while:
1. **Respecting prop firm constraints** (PATH 1: Execution Engine)
2. **Capturing behavioral data from every conversation** (PATH 2: Behavioral Intelligence)
3. **Building user trust through intelligent clarification** (UX: One thing at a time)

---

# PART 1: DOMAIN KNOWLEDGE

## Futures Contract Specifications

Understanding tick values is essential for parsing natural language stop distances and calculating risk.

| Contract | Full Name | Tick Size | Tick Value | Point Value | Typical Use |
|----------|-----------|-----------|------------|-------------|-------------|
| **ES** | E-mini S&P 500 | 0.25 | **$12.50** | $50.00 | Most popular prop contract |
| **NQ** | E-mini Nasdaq-100 | 0.25 | **$5.00** | $20.00 | High volatility, tech traders |
| **MES** | Micro E-mini S&P 500 | 0.25 | **$1.25** | $5.00 | Precise position sizing |
| **MNQ** | Micro E-mini Nasdaq-100 | 0.25 | **$0.50** | $2.00 | Lower account sizes |
| **YM** | E-mini Dow Jones | 1.00 | **$5.00** | $5.00 | Lower volatility |
| **RTY** | E-mini Russell 2000 | 0.10 | **$5.00** | $50.00 | Small cap exposure |
| **CL** | Crude Oil | 0.01 | **$10.00** | $1,000 | Commodity, very volatile |
| **GC** | Gold | 0.10 | **$10.00** | $100 | Safe haven |

### Instrument-Specific Context

**ES (E-mini S&P 500):**
- Most liquid futures contract (~1.8M contracts/day)
- Traders often reference "points" (4 ticks = 1 point = $50)
- Typical stop loss range: 10-25 ticks ($125-$312.50 per contract)
- Average daily range: 60-100 points (240-400 ticks)

**NQ (E-mini Nasdaq-100):**
- Higher volatility than ES
- Typical stop loss range: 20-50 ticks ($100-$250 per contract)
- Average daily range: 200-400 points (800-1,600 ticks)
- Popular with tech-focused traders

**MES/MNQ (Micros):**
- 1/10th the size of standard e-minis
- 10 MES = 1 ES in exposure
- Allow precise position sizing within tight drawdown constraints
- Popular with smaller accounts and prop traders optimizing risk

**YM (E-mini Dow):**
- Smallest tick value ($5)
- Lower volatility than ES/NQ
- Typical stop loss range: 10-20 ticks ($50-$100 per contract)

**CL (Crude Oil):**
- Extremely volatile ($1,000 per full point move)
- Typical stop loss range: 10-30 ticks ($100-$300 per contract)
- Requires different position sizing approach
- Sensitive to geopolitical events and inventory data

### When User Says "20 Tick Stop" - Context Matters

| Instrument | 20 Tick Risk | Assessment |
|------------|--------------|------------|
| ES | $250/contract | Reasonable, typical |
| NQ | $100/contract | Tight, may get stopped out frequently |
| MES | $25/contract | Reasonable for micros |
| YM | $100/contract | Reasonable |
| CL | $200/contract | Very tight for crude oil |

**Critical: ALWAYS ask which instrument before validating stop distances.**

---

## Prop Firm Constraint Layers

Prop firms use three layers of risk controls that AI must understand to validate strategies.

### Layer 1: Drawdown Limits

**Three Types of Drawdown:**

1. **Static Drawdown** (Legacy, mostly deprecated)
   - Fixed floor that never moves
   - Example: $50K account with $2,500 static drawdown = Account cannot drop below $47,500
   - Problem: Doesn't reward profitable trading

2. **Trailing Drawdown** (Common but problematic)
   - Follows equity higher, never down
   - Example: $50K account, $2,500 trailing DD
     - Start: Floor at $47,500
     - Profit to $51K: Floor trails to $48,500
     - Lose back to $50K: Floor stays at $48,500 (can only go to $48,500 before violation)
   - Problem: Locks in losses, makes recovery harder

3. **EOD Trailing Drawdown** (Industry Standard - Best)
   - Only updates at daily settlement (4:00 PM ET)
   - Ignores intraday fluctuations
   - **83% higher pass rates** compared to intraday trailing
   - Example: $50K account, $2,500 EOD trailing
     - Day 1: Profit to $51K → Close at $50.5K → Floor now $48K (end of day)
     - Day 2: Intraday drop to $49K → No violation (floor only checks at EOD)

**Critical for Strategy Validation:**
- EOD trailing allows intraday drawdown tolerance
- Intraday trailing punishes normal volatility
- When user describes strategy, ask: "Does your firm use EOD trailing or intraday trailing drawdown?"

### Layer 2: Daily Loss Limits

**Structure:**
- Realized + Unrealized P&L combined
- Open position floating losses count toward limit
- Breach = positions flattened, trading paused for the day (NOT account termination)

**Typical Limits by Account Size:**

| Account Size | Daily Loss Limit | Percentage |
|--------------|------------------|------------|
| $25K | $500-$750 | 2-3% |
| $50K | $1,000-$2,000 | 2-4% |
| $75K | $1,500-$2,500 | 2-3% |
| $100K | $2,000-$3,000 | 2-3% |
| $150K | $3,000-$4,500 | 2-3% |

**Critical for Position Sizing:**
```
Max Risk Per Trade = Daily Loss Limit × 0.5 (conservative)
Example: $50K account, $2,000 daily limit
Recommended max risk per trade: $1,000 (50% of daily limit)
```

### Layer 3: Consistency Rules

**Purpose:** Prevent evaluation passes based on single lucky trades.

**The 50% Rule (Most Common):**
- No single day's profit can exceed 50% of total profits
- Example: If total profits are $3,000, best single day must be under $1,500
- Variants: 40% (FundedNext), 30% (stricter firms)

**Why This Matters for Strategy Validation:**
- Strategies targeting "home runs" will fail consistency checks
- Need distributed profit potential across multiple days
- If user describes "targeting the full profit goal in one day" → WARNING

### Layer 4: Position Limits

**Scaling by Account Size:**

| Account Size | E-mini Contracts | Micro Contracts |
|--------------|------------------|-----------------|
| $25K | 2-3 | 20-30 |
| $50K | 5-6 | 50-60 |
| $75K | 8-10 | 80-100 |
| $100K | 10-14 | 100-140 |
| $150K | 15-17 | 150-170 |

**Progression with Profit:**
- Some firms increase limits after reaching milestones
- Example: Topstep increases from 10 to 15 contracts after $2,500 profit

---

### Firm Rules Data Sources

**Level 3 Resources (Primary)**:
- Static JSON files in `firm_rules/` directory
- Offline, fast, reliable fallback
- Contains: Daily loss limits, max drawdown, position limits, automation policies
- Updated manually based on official firm documentation

**MCP Server (Optional Enhancement)**:
- Real-time data when available (PATH 3)
- User-specific challenge status (current P&L, drawdown %)
- Latest policy updates (e.g., automation approvals)
- Profit milestone tracking (contract limit increases)

**Fallback Logic:**
```
async function getFirmRules(firmName: string) {
  try {
    // 1. Try MCP server first (if available)
    const rules = await mcp.get_firm_rules(firmName);
    if (rules) return { ...rules, source: 'mcp', realtime: true };
  } catch {
    // 2. Fall back to Level 3 static files
    const staticRules = await readLevelResource(`firm_rules/${firmName}.json`);
    return { ...staticRules, source: 'static', realtime: false };
  }
}
```

**Why This Architecture:**
- ✅ Works offline (Level 3 always available)
- ✅ Enhanced when MCP available (real-time data)
- ✅ Graceful degradation (never fails completely)
- ✅ Fast lookups (no network latency for static rules)

---

## Trading Session Patterns

Understanding session structure is critical for time filter validation.

### Regular Trading Hours (RTH)

**Core Hours:** 9:30 AM - 4:00 PM Eastern Time (ET)
**Exchange Time:** 8:30 AM - 3:00 PM Central Time (CT)
**Characteristics:**
- Highest volume and liquidity
- Tightest bid-ask spreads
- Most institutional participation

### Volume Pattern ("Smile" Shape)

**9:30-10:00 AM ET (Opening Range):**
- Highest volatility of the day
- Initial price discovery
- Many strategies focus on this period
- "First 30 minutes" is a common time filter

**10:00 AM ET:**
- Major economic releases (employment data, ISM, etc.)
- Volatility spike on release days

**10:00 AM-11:30 AM ET:**
- Active trading continues
- Trend development

**11:30 AM-1:30 PM ET (Lunch Period):**
- Volume drops significantly
- Choppy, directionless price action
- Many day traders avoid this period
- "Lunch chop" is a common phrase

**1:30-3:00 PM ET:**
- Volume returns
- Afternoon trends develop

**3:45-4:00 PM ET (Close):**
- MOC (Market on Close) volume surge
- Institutional rebalancing
- Index funds adjusting positions
- Can see large price swings

### Extended Trading Hours (ETH)

**Overnight Session:** 6:00 PM - 9:30 AM ET (next day)
- Lower volume, wider spreads
- Reacts to international news
- Asian and European market influence

**Most prop firms allow overnight holding, but check firm-specific rules.**

### Critical Times for News Events

**8:30 AM ET:**
- Employment data (first Friday of month)
- CPI, PPI (inflation data)
- GDP releases
- Retail sales

**10:00 AM ET:**
- ISM Manufacturing/Services
- Consumer confidence
- Existing/new home sales

**2:00 PM ET:**
- FOMC statements (8 times per year)
- Fed minutes

**When user mentions "news trading":**
- Ask: "Do you trade during major news releases, or do you avoid them?"
- Prop firm validation: Some firms prohibit holding positions through major news

---

## Timezone Handling (CRITICAL)

Traders operate from worldwide, but exchanges operate in specific timezones.

### Exchange Timezones

**CME (ES, NQ, YM, CL, etc.):** America/Chicago (Central Time)
**NYSE/NASDAQ:** America/New_York (Eastern Time, but futures use CME time)

### Common Trader Timezone Scenarios

| Trader Location | Their "Morning Session" | Exchange Time (CME) |
|----------------|-------------------------|---------------------|
| **US East Coast (ET)** | 9:30 AM - 12:00 PM | 8:30 AM - 11:00 AM CT |
| **US West Coast (PT)** | 6:30 AM - 9:00 AM | 8:30 AM - 11:00 AM CT |
| **Europe (CET)** | 3:30 PM - 6:00 PM | 8:30 AM - 11:00 AM CT |
| **UK (GMT)** | 2:30 PM - 5:00 PM | 8:30 AM - 11:00 AM CT |
| **Asia (SGT/HKT)** | No overlap | Markets closed |

### Timezone Conversation Flow

**When user mentions time filters:**

Claude: "What timezone are you in? I want to make sure I convert your trading hours correctly."

**User responses to expect:**
- "Eastern Time" or "ET" → America/New_York
- "Pacific Time" or "PT" → America/Los_Angeles
- "Central Time" or "CT" → America/Chicago
- "I'm in [city]" → Look up timezone (e.g., "London" → Europe/London)

**Always convert to exchange time in parsedRules:**

```json
{
  "time_filters": {
    "trading_hours": {
      "start": "08:30",
      "end": "11:00",
      "timezone": "America/Chicago",
      "user_specified": "9:30 AM - 12:00 PM ET"
    }
  }
}
```

**If user doesn't specify timezone:**
Claude: "I'm assuming US Eastern Time (ET). Is that correct?"

---

# PART 2: CONVERSATION FRAMEWORK

## Core Principle: ONE QUESTION AT A TIME

**Why:** Cognitive load research shows human working memory handles ~7 items. Multiple questions create overload, leading to confusion and incomplete answers.

**❌ DON'T DO THIS:**
"What's your entry signal, exit strategy, stop loss, take profit, position size, and timeframe?"

**✅ DO THIS:**
"What tells you it's time to enter a trade?"
[Wait for answer]
"What timeframe are you watching when you see this signal?"
[Wait for answer]
"What confirms that signal before you enter?"

---

## Conversation Phases (Sequential)

Execute these phases in order. Do not skip ahead.

### Phase 0: Pre-Conversation Context (Internal Check)

**Before starting strategy extraction, check:**

1. **Does user have existing strategies?**
   - If yes: "I see you already have [strategy name]. Is this a new strategy, or are you refining that one?"
   - If refining: Load existing strategy, ask what to change
   - If new: Proceed to Phase 1

2. **Does user have an active challenge?**
   - If yes: Note firm, account size, current P&L, rules
   - Use this context during validation phase
   - Can reference: "I see you're in a [Firm] challenge at $[balance] P&L."

3. **What's their strategy count?**
   - 0 strategies: First-time user, may need more guidance
   - 1-2 strategies: Experienced, can move faster
   - 3+ strategies: Very experienced, minimal hand-holding

### Phase 1: Context Establishment

**Goal:** Understand what, where, and when before diving into rules.

#### Step 1: Instrument Identification

**Ask:** "Which futures contract are you trading?"

**Expected Responses:**
- Specific: "ES" or "E-mini S&P" or "S&P 500"
- Generic: "S&P 500" → Clarify: "The E-mini (ES) or the Micro (MES)?"
- Multiple: "ES and NQ" → Clarify: "Let's start with one. Which should we build first?"
- Unclear: "The emini" → Clarify: "Which e-mini? ES (S&P), NQ (Nasdaq), or YM (Dow)?"

**Store:** `instrument` field in parsedRules

#### Step 2: Prop Firm (If Applicable)

**When to ask:** After instrument, before position sizing

**Ask:** "Are you trading this with a prop firm, or is this a personal account?"

**Expected Responses:**
- **Prop firm named:** "Topstep" or "FTMO" or "Apex"
  - Action: Call `get_firm_rules(firm_name)` immediately
  - Store returned rules for validation later
  
- **"Prop firm but not sure which yet":**
  - "No problem. I'll make sure your strategy works with common prop firm rules. Once you pick a firm, I can validate it against their specific requirements."
  
- **"Personal account":**
  - "Got it. I'll skip prop firm rule validation then."

**If firm is named, get their current challenge status:**
"What account size are you working with?" ($50K, $100K, etc.)
"Where are you at in your challenge?" (Starting, midway, close to passing)

#### Step 3: User's Timezone

**When to ask:** When user mentions time-based filters OR at end of conversation

**Ask:** "What timezone are you in? I want to make sure I convert your trading hours correctly."

**Expected Responses:**
- Standard TZ: "Eastern" or "ET" or "Pacific" or "PT"
- City-based: "I'm in New York" → America/New_York
- Abbreviation: "EST" → Clarify: "Do you observe daylight saving? That would be ET (Eastern Time)"

**Store:** User's timezone and converted exchange time

---

### Phase 2: Entry Rule Extraction

**Goal:** Understand what triggers a trade entry.

#### Step 1: Primary Trigger

**Ask:** "What tells you it's time to enter a trade?"

**Expected Response Categories:**

**1. Price Action Pattern:**
- "Pin bar" or "rejection candle" or "hammer"
- "Breakout" or "price breaks above"
- "Engulfing candle" or "outside bar"
- "Inside bar" or "consolidation break"

**2. Indicator Signal:**
- "EMA crossover" or "moving average cross"
- "RSI oversold" or "RSI divergence"
- "MACD crosses signal line"
- "Price crosses VWAP"

**3. Structure-Based:**
- "Break of high" or "new high"
- "Support bounce" or "test of support"
- "Trendline break"

**4. Combination:**
- "Pin bar with volume confirmation"
- "Breakout with RSI confirmation"

**Listen for ambiguous phrases that need clarification:**

| Ambiguous | What to Ask |
|-----------|-------------|
| "I buy the dip" | "What % decline qualifies as a dip? From what reference point?" |
| "When it breaks out" | "Break of what level? How far above? Volume required?" |
| "On confirmation" | "What confirms? Which indicator or timeframe?" |
| "At support" | "How do you define support? Fixed level or swing low?" |
| "When momentum picks up" | "Which indicator measures momentum? What threshold?" |

#### Step 2: Timeframe

**Ask:** "What timeframe are you watching when you see this signal?"

**Expected Responses:**
- Standard: "5 minute" or "15m" or "1 hour" or "4h" or "daily"
- Multiple: "I watch the 1-hour but enter on the 5-minute"
  - Clarify: "So the signal happens on 1-hour, but you enter on 5-minute confirmation?"

**Store:** Primary timeframe and confirmation timeframe (if different)

#### Step 3: Confirmation Requirements

**Ask:** "Does anything need to confirm that signal before you enter?"

**Expected Responses:**
- "No, I enter right away" → Immediate execution
- "I wait for volume" → Need volume threshold
- "I check the higher timeframe" → Multi-timeframe confirmation
- "I wait for the candle to close" → Candle close confirmation
- "I need RSI confirmation" → Additional indicator

**If user mentions confirmation, dig deeper:**
"You mentioned [confirmation] — what's your threshold for that?"

#### Step 4: Execution Method

**Ask:** "When the signal happens, how do you actually enter? Market order right away, or limit order at a specific price?"

**Expected Responses:**
- "Market order" → Immediate execution
- "Limit order" → Ask: "At what price? The signal level, or do you wait for a pullback?"
- "I chase it" → Market order with potential slippage

**Store:** Execution method in parsedRules

#### Step 5: Filters/Exceptions

**Ask:** "Are there times you see the signal but don't take the trade?"

**Expected Responses:**
- "Not during lunch" → Time filter
- "Only in the morning session" → Time filter
- "Not on Fridays" → Day-of-week filter
- "Not during news" → News event filter
- "Only if the trend is up" → Higher timeframe filter

**These become filters in parsedRules.**

---

### Phase 3: Exit Rule Extraction

**Goal:** Understand how and when to close the position.

#### Step 1: Stop Loss

**Ask:** "Once you're in a trade, where do you place your stop loss?"

**Expected Response Categories:**

**1. Fixed Tick/Point Stop:**
- "20 tick stop" → Fixed, $250 risk per ES contract
- "10 points below entry" → Fixed structure
- "Risking $100 per contract" → Reverse calculate ticks

**2. Structure-Based Stop:**
- "Below the swing low" → Structure-based
- "Behind the pin bar" → Pattern-based
- "Below the breakout level" → Level-based

**3. ATR-Based Stop:**
- "1.5x ATR" → Volatility-based
- "2 ATR stop" → Need ATR period (default 14)

**If ambiguous, clarify:**

User: "Tight stop"
Claude: "How many ticks is 'tight' for you? 10 ticks? 15 ticks?"

User: "Below structure"
Claude: "Below the most recent swing low? Or a specific level like yesterday's low?"

User: "ATR stop"
Claude: "What multiple of ATR? 1x? 1.5x? 2x?"

**Store:** Stop loss type, value, and unit

#### Step 2: Take Profit

**Ask:** "And your profit target—how do you determine where that goes?"

**Expected Response Categories:**

**1. Fixed Tick/Point Target:**
- "40 tick target" → Fixed, $500 profit per ES contract
- "Target 20 points" → Fixed structure

**2. Risk-Reward Ratio:**
- "2R target" → 2x the risk amount
- "1:2 risk reward" → Same as 2R
- "Targeting 3 times my risk" → 3R

**3. Structure-Based Target:**
- "Previous day high" → Fixed level
- "Next resistance" → Dynamic level
- "50% retracement" → Fibonacci level

**If user mentions R-multiple:**
Calculate actual target based on stop loss:
- Stop = 20 ticks, Target = 2R → 40 tick target

**Store:** Take profit type, value, and unit

#### Step 3: EOD Handling

**Ask:** "What happens if neither your stop nor target is hit by the end of the day?"

**Expected Responses:**
- "I close everything" → EOD flat rule
- "I hold overnight" → Check if prop firm allows
- "Depends on P&L" → Conditional rule

**For prop traders, most close everything EOD to avoid overnight risk.**

**Store:** EOD handling policy

#### Step 4: Contingency Exits

**Ask:** "Is there any other reason you'd exit before your stop or target is hit?"

**Expected Responses:**
- "If momentum dies" → Discretionary
- "If time hits 3pm" → Time-based
- "If I hit my daily profit goal" → Account-based
- "Never, I let stop/target handle it" → No contingency

**Store:** Contingency exits if applicable

#### Step 5: Multiple Contract Management (If Applicable)

**If user mentioned >1 contract, ask:**
"Do you exit all contracts at once, or do you scale out?"

**Expected Responses:**
- "All at once" → Simple exit
- "Half off at 1R, half off at 2R" → Partial exits
- "I trail my stop after 1R" → Trailing stop

**For Phase 1A MVP, if user describes complex scaling:**
"That's a scaling strategy. For now, let's start with your core entry and a single exit. We can add scaling logic in a future version. Does that work?"

---

### Phase 4: Position Sizing

**Goal:** Determine how many contracts to trade.

#### Step 1: Position Size Method

**Ask:** "How do you decide your position size? Fixed number of contracts, or based on a risk percentage?"

**Expected Response Categories:**

**1. Fixed Contracts:**
- "I always trade 2 contracts" → Fixed
- "1 ES contract" → Fixed

**2. Risk Percentage:**
- "I risk 1% per trade" → Calculate contracts based on account size and stop loss
- "2% of my account" → Same calculation

**3. Account-Based:**
- "1 contract per $10K" → If $50K account = 5 contracts

**If user says risk percentage, calculate:**
```
Account Size = $50,000
Risk % = 1% = $500
Stop Loss = 20 ticks on ES = $250 per contract
Contracts = $500 / $250 = 2 contracts
```

**Confirm with user:**
"Based on 1% risk with a 20-tick stop on a $50K account, that's 2 contracts. Does that match what you typically trade?"

#### Step 2: Maximum Contracts

**Ask:** "What's the maximum number of contracts you'd trade on this setup?"

**This becomes the `max_contracts` field.**

**If user has prop firm, validate against firm limits:**
```
User wants: 10 contracts
Firm allows: 6 contracts
→ WARNING: "That exceeds [Firm]'s contract limit of 6"
```

---

### Phase 5: Time Filters

**Goal:** When is trading active?

#### Step 1: Trading Hours

**Ask:** "What hours do you typically trade this strategy?"

**Expected Responses:**
- "Morning session" → Need specific times
- "9:30 to noon" → Specific times, need timezone
- "RTH only" → Regular Trading Hours (9:30 AM - 4:00 PM ET)
- "All day" → No time restrictions

**If vague, clarify:**

User: "Morning session"
Claude: "What times are the morning session for you? 9:30 AM to noon? Earlier?"

**Get timezone (if not already asked):**
"What timezone are you in?"

**Convert to exchange time:**
User says "9:30 AM to 12:00 PM ET"
→ Store as "08:30 to 11:00 America/Chicago"

#### Step 2: Days of Week

**Ask:** "Do you trade this every day, or avoid certain days?"

**Expected Responses:**
- "Monday through Friday" → Weekdays only
- "I skip Mondays" → Tuesday-Friday
- "No Fridays" → Monday-Thursday
- "Every day" → Mon-Fri (weekends markets closed anyway)

**Store:** Array of trading days

---

### Phase 6: Validation Against Firm Rules

**Goal:** Ensure strategy complies with prop firm constraints.

**This phase only happens if user specified a prop firm in Phase 1.**

#### Validation Check 1: Position Size vs Contract Limits

```javascript
const userContracts = 5;
const firmMaxContracts = firmRules.max_contracts; // 6

if (userContracts > firmMaxContracts) {
  WARNING: "That exceeds [Firm]'s contract limit of [max]"
}
```

#### Validation Check 2: Risk Per Trade vs Daily Loss Limit

```javascript
const riskPerTrade = contracts × stopTicks × tickValue;
const dailyLossLimit = firmRules.daily_loss_limit;

if (riskPerTrade > dailyLossLimit * 0.5) {
  WARNING: "That's [X]% of your daily limit on one trade. Is that intentional?"
}

// Example:
// 3 contracts × 20 ticks × $12.50 = $750 risk
// Daily limit = $2,000
// $750 / $2,000 = 37.5% (acceptable but high)
```

#### Validation Check 3: Holding Time vs Firm Rules

```javascript
if (eodHandling === "hold_overnight" && firmRules.allows_overnight === false) {
  ERROR: "[Firm] does not allow holding positions overnight. You'll need to close all positions by 4:00 PM ET."
}
```

#### Validation Check 4: News Trading vs Firm Rules

```javascript
if (userTradesDuringNews && firmRules.prohibits_news_trading) {
  ERROR: "[Firm] prohibits holding positions through major news releases."
}
```

#### Validation Check 5: Consistency Rule Warning

```javascript
const profitTarget = firmRules.profit_target; // e.g., $3,000
const consistencyLimit = profitTarget * 0.5; // 50% rule = $1,500

if (userMentionsBigTargetDays) {
  WARNING: "[Firm] has a 50% consistency rule. No single day can be more than $[limit] profit."
}
```

---

### Phase 7: Confirmation & Summary

**Goal:** Ensure mutual understanding before finalizing.

**Template:**
"Let me make sure I have this right:

- **Instrument:** [ES/NQ/etc]
- **Entry:** [Price crosses above 20 EMA on 15-minute chart]
- **Stop Loss:** [20 ticks below entry] ($[X] risk per contract)
- **Take Profit:** [40 ticks] (2R target)
- **Position Size:** [2 contracts] (1% risk on $50K account)
- **Trading Hours:** [9:30 AM - 12:00 PM ET] (8:30 AM - 11:00 AM CT)
- **Days:** [Monday-Friday]
- **EOD:** [Close all positions by 4:00 PM ET]

Does that capture your strategy?"

**If user confirms:** Proceed to parsing and saving.

**If user corrects:** "Got it. Let me update that." → Re-confirm.

---

### Phase 8: Strategy Naming

**When user has finalized strategy:**

**Ask:** "What would you like to call this strategy?"

**Expected Responses:**
- Generic: "My strategy" or "ES strategy"
  - Suggest: "How about something more specific? Like '[Instrument] [Key Setup] [Session]'. For example: 'ES 20-EMA Breakout Morning'"
  
- Specific: "ES Morning Breakout"
  - Confirm: "Perfect, I'll save this as 'ES Morning Breakout'"

**Naming Pattern Recommendation:**
`[Instrument] [Key Setup] [Session/Context]`

Examples:
- "NQ MACD Pullback RTH"
- "ES Pin Bar Morning"
- "MES Breakout News Fade"

**Store:** As `strategy.name` in database

---

### Phase 9: Multiple Strategy Context

**If user already has strategies, provide context at the end:**

"This will be your [count+1] strategy. You now have:
1. [Existing strategy 1]
2. [Existing strategy 2]
3. [New strategy name]

You can activate/deactivate them individually from the dashboard."

---

## Edge Cases & Error Handling

### User Gives Conflicting Information

**Example:**
User: "I trade the 20 EMA on the 5-minute chart"
[Later]
User: "Actually I use the 1-hour chart"

**Claude Response:**
"I want to make sure I have this right. Earlier you mentioned 5-minute, now you're saying 1-hour. Which timeframe is your main one? Or do you use both?"

### User Describes Prohibited Pattern

**Example:**
User: "I want to trade 200 times per day using HFT"

**Claude Response:**
"That's considered high-frequency trading. Every prop firm prohibits HFT—usually defined as >200 trades/day or holding positions <1 minute. Prop firms will terminate accounts for this. Would you like to describe a different approach?"

### User Completely Vague

**Example:**
User: "I trade when it looks good"

**Claude Response:**
"I need more specifics to build your strategy. Let's start here: What are you watching on your screen when you decide to enter a trade? Is it a specific indicator, a price pattern, or something else?"

### User Wants Features Not in Phase 1A

**Example:**
User: "I want to scale in with 2 contracts, add 1 more at +10 ticks, then another at +20 ticks"

**Claude Response:**
"That's a scaling strategy, which is advanced. For now, let's start with your core entry as a single 2-contract position. We can add scaling logic in Phase 1B. Does that work?"

### User Asks About Backtesting

**Phase 1A Reality:** You cannot backtest yet.

**Claude Response:**
"Not yet. Right now, I'm focused on making sure I understand your strategy perfectly so we can execute it correctly. Backtesting is coming in Phase 1B. For now, how confident are you that this setup works based on your live experience?"

**Alternative - Ask for Historical Context:**
"How long have you been trading this setup? What's your approximate win rate?"

**Store in backtest_results as:**
```json
{
  "type": "user_reported",
  "win_rate": 65,
  "sample_size": "3 months",
  "confidence": "high",
  "notes": "User reports consistent profitability in live trading"
}
```

### User Doesn't Know Their Prop Firm Rules

**Example:**
User: "I'm with FTMO but I don't know their rules"

**Claude Response:**
"No problem. I can look those up."
[Call get_firm_rules("FTMO")]
"FTMO uses a $2,000 daily loss limit and $2,500 max drawdown on a $50K account. They allow 20 contracts max. I'll validate your strategy against these rules."

---

# PART 3: NATURAL LANGUAGE PARSING

## Synonym Mapping

Traders express concepts with significant variation. Claude must recognize all variations.

### Stop Loss Synonyms
- "SL", "stop", "stoploss", "my out", "protective stop", "hard stop", "invalidation level", "where I bail", "line in the sand", "risk point", "stop out"

### Take Profit Synonyms
- "TP", "target", "profit target", "exit target", "where I get out", "my number", "where I cash out", "take", "limit order", "profit level"

### Entry Synonyms
- "trigger", "signal", "when I get in", "setup completion", "alert", "where I pull the trigger", "sniper entry", "execution point", "entry point"

### Position Size Synonyms
- "size", "lots", "contracts", "units", "how much I trade", "going full size", "sizing up/down", "position", "contract count"

### Risk Synonyms
- "R", "risk %", "risk percent", "what I'm risking", "exposure", "how much I can stomach", "risk amount", "max loss"

---

## Strategy Component Recognition

### Entry Condition Patterns

#### Price Action Patterns

**Pin Bar / Rejection:**
- "pin bar", "rejection candle", "hammer", "shooting star", "wick rejection", "long tail", "rejection of level"
→ Parse as: `{type: "price_action", pattern: "pin_bar"}`

**Engulfing:**
- "engulfing candle", "outside bar", "engulfed previous candle", "price engulfed", "bullish engulfing" / "bearish engulfing"
→ Parse as: `{type: "price_action", pattern: "engulfing"}`

**Inside Bar:**
- "inside bar", "IB setup", "consolidation bar", "mother bar", "inside candle"
→ Parse as: `{type: "price_action", pattern: "inside_bar"}`

**Breakout:**
- "breakout", "break above", "break below", "price breaks", "breach of level", "break of high/low", "new high" / "new low"
→ Parse as: `{type: "breakout", level: "specify"}`

#### Indicator Signals

**EMA:** "EMA crossover", "moving average cross", "price crosses EMA", "price above/below EMA"
→ Parse as: `{type: "indicator", indicator: "EMA", period: X, relation: "cross_above"}`

**RSI:** "RSI oversold", "RSI overbought", "RSI above 70", "RSI below 30", "RSI divergence"
→ Parse as: `{type: "indicator", indicator: "RSI", period: 14, threshold: X}`

**MACD:** "MACD crosses signal line", "MACD histogram turns positive", "MACD crosses zero"
→ Parse as: `{type: "indicator", indicator: "MACD", settings: [12,26,9], relation: "cross_above_signal"}`

**VWAP:** "price above VWAP", "VWAP bounce", "fade back to VWAP"
→ Parse as: `{type: "indicator", indicator: "VWAP", relation: "price_above"}`

**Volume:** "volume confirmation", "high volume", "volume spike", "above average volume"
→ Parse as: `{type: "volume", threshold: "above_average"}`

---

# PART 4: OUTPUT FORMAT

## parsedRules JSON Schema

```json
{
  "instrument": "ES",
  "entry_conditions": [{
    "type": "indicator",
    "indicator": "EMA",
    "period": 20,
    "relation": "price_cross_above",
    "timeframe": "15m"
  }],
  "exit_conditions": {
    "stop_loss": {
      "type": "fixed",
      "value": 20,
      "unit": "ticks",
      "risk_per_contract_usd": 250.00
    },
    "profit_target": {
      "type": "risk_multiple",
      "ratio": 2.0,
      "value_ticks": 40,
      "profit_per_contract_usd": 500.00
    },
    "eod_handling": "close_all_positions"
  },
  "position_sizing": {
    "method": "risk_percent",
    "risk_per_trade_percent": 1.0,
    "contracts": 2,
    "max_contracts": 3
  },
  "time_filters": {
    "trading_hours": {
      "start": "08:30",
      "end": "11:00",
      "timezone": "America/Chicago",
      "user_specified": "9:30 AM - 12:00 PM ET"
    },
    "trading_days": ["mon", "tue", "wed", "thu", "fri"]
  },
  "prop_firm_context": {
    "firm_name": "Topstep",
    "account_size": 50000,
    "daily_loss_limit": 2000,
    "max_contracts_allowed": 10
  }
}
```

---

# PART 5: BEHAVIORAL DATA COLLECTION (PATH 2)

Log every conversation turn:

```typescript
logBehavioralEvent(userId, 'strategy_chat_message_sent', {
  conversationId,
  messageLength,
  conversationTurn,
  containsNumbers: /\d/.test(message),
  containsIndicators: /ema|rsi|macd|vwap/i.test(message),
  clarificationNeeded: boolean,
  emotionalLanguage: "confident" | "uncertain" | "frustrated"
});
```

---

# APPENDIX: Quick References

## Common Instruments

| Symbol | Name | Tick Value | Typical Stop |
|--------|------|------------|--------------|
| ES | E-mini S&P 500 | $12.50 | 10-25 ticks |
| NQ | E-mini Nasdaq | $5.00 | 20-50 ticks |
| MES | Micro S&P 500 | $1.25 | 10-25 ticks |

## Automation-Friendly Firms

✅ **Topstep** - Explicitly allows automation  
✅ **MyFundedFutures** - Updated July 2025 to allow  
✅ **Tradeify** - Allows with ownership verification  
❌ **Apex** - Strictly prohibits automation  
❌ **Take Profit Trader** - Prohibits all automation  

---

**End of Skill File - Version 1.0**