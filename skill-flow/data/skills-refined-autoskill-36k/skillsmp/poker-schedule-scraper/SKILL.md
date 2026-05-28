---
name: Poker Schedule Scraper
description: Automated scraping of poker tournament schedules from major tour websites
---

# Poker Schedule Scraper Skill

## 🎯 MISSION STATEMENT (LOCKED)
**Goal:** Create the MOST COMPREHENSIVE tournament database on the planet.

**Product:** **PokerNearMe** - A "Google-style" search engine for poker players to find:
- 🎰 All cash games and tournaments near them
- 🏢 **777 venues nationwide** (complete US coverage)

**Search Capabilities:**
- By **Distance** (miles from user)
- By **State**
- By **Dates** (start date, end date, specific day)
- By **Buy-in Amount** (min/max range)
- By **Tournament Type** (NLH, PLO, Mixed, Bounty, etc.)
- By **Series Name** (WSOP, WPT, MSPT, etc.)
- By **Game Type** (Cash vs Tournament)

**Display:**
- List view with all requested data
- **Optional Map View** showing all matching venues/events

**Data Quality Standard:**
- ✅ Complete yearly schedule for each tour
- ✅ Every individual event within each series
- ✅ Verified source URLs for daily updates
- ✅ 777 venue enrichment (address, lat/lng, hours, games offered)

---

## Overview
Efficiently scrape and populate the database with poker tournament schedules from major tours.

## ⚠️ PRIMARY SOURCE: POKER ATLAS
**ALWAYS check Poker Atlas FIRST before visiting individual tour websites.**

### Poker Atlas URLs
- **Main Site**: https://www.pokeratlas.com
- **Tournaments by State**: https://www.pokeratlas.com/poker-tournaments/[state]
- **Venue-Specific**: https://www.pokeratlas.com/poker-room/[venue-slug]/tournaments

### Why Poker Atlas First?
1. **Aggregated data** - All venues in one place
2. **Consistent format** - Standardized table structure
3. **Real-time updates** - Venues push updates here
4. **Complete info** - Buy-ins, dates, guarantees, structure

### Poker Atlas Venue Examples
| Venue | Poker Atlas URL |
|-------|-----------------|
| TCH Dallas | pokeratlas.com/poker-room/texas-card-house-dallas/tournaments |
| Wynn | pokeratlas.com/poker-room/wynn-las-vegas/tournaments |
| Borgata | pokeratlas.com/poker-room/borgata-hotel-casino-spa/tournaments |
| Thunder Valley | pokeratlas.com/poker-room/thunder-valley-casino-resort/tournaments |

---

## ✅ VERIFIED SOURCE URLs (Successfully Scraped)
**CRITICAL: Always save the EXACT URL where data was scraped to `scrape_url` field in database.**

### Poker Atlas (Primary - Use First)
| Venue | Verified Scrape URL | Last Scraped |
|-------|---------------------|--------------|
| TCH Dallas | https://www.pokeratlas.com/poker-room/texas-card-house-dallas/tournaments | 2026-01-21 |
| TCH Austin | https://www.pokeratlas.com/poker-room/texas-card-house-austin/tournaments | 2026-01-21 |
| TCH Houston | https://www.pokeratlas.com/poker-room/texas-card-house-houston/tournaments | 2026-01-21 |
| Talking Stick | https://www.pokeratlas.com/poker-room/talking-stick-resort/tournaments | Pending |
| Wynn | https://www.pokeratlas.com/poker-room/wynn-las-vegas/tournaments | Pending |
| Venetian | https://www.pokeratlas.com/poker-room/venetian/tournaments | Pending |
| Borgata | https://www.pokeratlas.com/poker-room/borgata-hotel-casino-spa/tournaments | Pending |
| bestbet Jax | https://www.pokeratlas.com/poker-room/bestbet-jacksonville/tournaments | Pending |
| Commerce | https://www.pokeratlas.com/poker-room/commerce-casino/tournaments | Pending |

### Tour Official Sites (Secondary)
| Tour | Verified Scrape URL | Last Scraped |
|------|---------------------|--------------|
| WSOP Circuit | https://www.wsop.com/tournaments/ | 2026-01-21 |
| WSOPC Thunder Valley | https://www.wsop.com/tournaments/2026-wsop-circuit-thunder-valley/ | 2026-01-21 |
| WSOPC Cherokee | https://www.wsop.com/tournaments/2026-wsop-circuit-harrah-s-cherokee/ | 2026-01-21 |
| WSOPC Baltimore | https://www.wsop.com/tournaments/2026-wsop-circuit-horseshoe-baltimore/ | 2026-01-21 |
| WPT Schedule | https://www.worldpokertour.com/schedule/ | 2026-01-21 |
| MSPT Schedule | https://msptpoker.com/schedule/ | 2026-01-21 |

### Venue Official Sites (Tertiary)
| Venue | Verified Scrape URL | Last Scraped |
|-------|---------------------|--------------|
| Talking Stick | https://www.talkingstickresort.com/phoenix-scottsdale-casino/poker/arena-poker-room-tournaments/ | 2026-01-21 |
| AZ State Champ | https://www.talkingstickresort.com/poker-tournaments/az-state-championship/ | 2026-01-21 |
| bestbet Blizzard | https://bestbetjax.com/poker/tournaments/bestbet-blizzard-festival | 2026-01-21 |
| LAPC | https://commercecasino.com/tournament/lapc/ | 2026-01-21 |
| Card Player (LAPC) | https://www.cardplayer.com/poker-tournaments/1627315-2026-l-a-poker-classic | 2026-01-21 |

### Aggregators (Backup/Verification)
| Source | Verified Scrape URL | Notes |
|--------|---------------------|-------|
| Hendon Mob | https://pokerdb.thehendonmob.com/venues/[venue-id]/festivals | Use for historical + upcoming |
| Card Player | https://www.cardplayer.com/poker-tournaments/[tournament-id] | Good for schedule tables |

---

## Secondary Sources (Individual Tour Websites)

## Database Schema
```sql
-- Series table (already exists)
CREATE TABLE poker_series (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  series_uid TEXT UNIQUE NOT NULL, -- e.g., 'wsopc-thunder-valley-2026'
  series_name TEXT NOT NULL,
  tour TEXT NOT NULL, -- 'WSOP Circuit', 'WPT', 'MSPT', etc.
  tier TEXT, -- 'Major', 'Regional', 'High Roller'
  venue_name TEXT,
  city TEXT,
  state TEXT,
  country TEXT DEFAULT 'USA',
  start_date DATE,
  end_date DATE,
  buy_in_min INTEGER,
  buy_in_max INTEGER,
  guarantee BIGINT,
  source TEXT, -- URL or source name
  events_scraped BOOLEAN DEFAULT FALSE,
  last_scraped TIMESTAMPTZ,
  scrape_url TEXT,
  scrape_status TEXT -- 'complete', 'series_only', 'pending', 'dates_announced'
);

-- Events table (already exists)
CREATE TABLE poker_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_uid TEXT UNIQUE NOT NULL, -- e.g., 'WSOPC-TV-2026-01'
  series_uid TEXT REFERENCES poker_series(series_uid),
  event_name TEXT NOT NULL,
  event_number INTEGER,
  event_type TEXT, -- 'main_event', 'side_event', 'satellite', 'high_roller'
  buy_in INTEGER NOT NULL,
  guarantee BIGINT,
  start_date DATE,
  start_time TIME,
  game_type TEXT, -- 'NLH', 'PLO', 'Mixed', 'Stud', etc.
  format TEXT, -- 'Single Day', 'Multi-Day', 'Multi-Flight', 'Turbo'
  venue_name TEXT,
  city TEXT,
  state TEXT,
  source TEXT,
  notes TEXT
);
```

## Scraping Workflow

### 1. Series Discovery
```javascript
// First scrape series-level data
const TOUR_URLS = {
  'WSOPC': 'https://www.wsop.com/tournaments/',
  'WPT': 'https://www.wpt.com/schedule/',
  'MSPT': 'https://msptpoker.com/schedule/',
  'RGPS': 'https://rungoodpokerseries.com/schedule/',
  'PGT': 'https://www.pgt.com/schedule/'
};

async function discoverSeries(tour) {
  // Navigate to tour schedule page
  // Extract: series name, dates, venue, city/state
  // Generate series_uid from tour + venue + year
  // Insert into poker_series with scrape_status = 'series_only'
}
```

### 2. Event Detail Scraping
```javascript
async function scrapeEventDetails(seriesUid) {
  const series = await getSeries(seriesUid);
  
  // Navigate to series detail page
  // Extract each event row/card:
  //   - Event number, name, date, time
  //   - Buy-in, guarantee
  //   - Game type, format
  
  // Generate event_uid: TOUR-VENUE-YEAR-EVENT#
  // Insert into poker_events
  // Update poker_series.events_scraped = true
}
```

## SQL Generation Pattern
```sql
-- Series INSERT template (ALWAYS include scrape_url!)
INSERT INTO poker_series (
  series_uid, series_name, tour, tier, venue_name, 
  city, state, start_date, end_date, 
  buy_in_min, buy_in_max, guarantee, source, 
  scrape_url, events_scraped, scrape_status
) VALUES (
  '[tour]-[venue-slug]-[year]',
  '[Full Series Name]',
  '[Tour Name]',
  '[Major/Regional/High Roller]',
  '[Venue Name]',
  '[City]', '[ST]',
  '[YYYY-MM-DD]', '[YYYY-MM-DD]',
  [min_buyin], [max_buyin], [guarantee],
  '[source.com]',
  '[EXACT URL WHERE DATA WAS SCRAPED]', -- ⚠️ REQUIRED: Save exact source URL
  [true/false], '[complete/series_only/pending]'
) ON CONFLICT (series_uid) DO UPDATE SET 
  scrape_url = EXCLUDED.scrape_url,
  last_scraped = NOW();

-- Events INSERT template
INSERT INTO poker_events (
  id, event_uid, series_uid, event_name, event_number,
  event_type, buy_in, guarantee, start_date,
  game_type, format, venue_name, city, state, source
) VALUES (
  gen_random_uuid(),
  '[TOUR]-[VENUE]-[YEAR]-[##]',
  '[series_uid]',
  '[Event Name]',
  [event_number],
  '[main_event/side_event/satellite]',
  [buyin], [guarantee],
  '[YYYY-MM-DD]',
  '[NLH/PLO/Mixed]',
  '[Multi-Day/Single Day]',
  '[Venue]', '[City]', '[ST]', '[source]'
) ON CONFLICT (event_uid) DO NOTHING;
```

## 🎯 THE 55 CANONICAL TOURNAMENT SERIES (Master Checklist)
**CRITICAL: Complete ALL 55 series before moving to venue-level scraping.**

### Tier 1: National/Major (7 Series)
| # | Series | Tour | Status |
|---|--------|------|--------|
| 1 | WSOP (Summer Series) | WSOP | ✅ Series dates confirmed (May 26 - Jul 15) |
| 2 | WSOP Circuit | WSOP | ✅ 18 stops, 7 w/events uploaded |
| 3 | WSOP Online (U.S.) | WSOP | 🚫 N/A - Online excluded |
| 4 | WPT Main Tour | WPT | ✅ Lucky Hearts complete |
| 5 | WPT Prime | WPT | ✅ Jan-Apr mapped |
| 6 | PokerStars NAPT | PokerStars | ❌ NOT SCRAPED |
| 7 | PokerGO Tour (PGT) | PokerGO | ✅ Jan-Mar mapped |

### Tier 2: Large Regional (10 Series)
| # | Series | Tour | Status |
|---|--------|------|--------|
| 8 | MSPT | MSPT | ✅ 42 series, 120+ events COMPLETE |
| 9 | RGPS | RunGood | ⚠️ 13 stops mapped, needs events |
| 10 | SHRPO (Hollywood) | Seminole | ✅ Jul/Aug mapped |
| 11 | Seminole Showdown | Seminole | ✅ Apr confirmed |
| 12 | Seminole Classic | Seminole | ✅ Escalator X complete |
| 13 | Borgata Winter Poker Open | Borgata | ✅ Jan 2026 complete |
| 14 | Borgata Spring Poker Open | Borgata | ⚠️ Apr/May mapped, needs events |
| 15 | Bar Poker Open (BPO) | BPO | ❌ NOT SCRAPED |
| 16 | WPT Lucky Hearts (LHPO) | WPT | ✅ 58 events complete |
| 17 | Maryland Live Open (MAPO) | Maryland Live | ❌ NOT SCRAPED |
| 18 | Parx Big Stax | Parx Casino | ❌ NOT SCRAPED |

### Tier 3: Las Vegas Majors (9 Series)
| # | Series | Venue | Status |
|---|--------|-------|--------|
| 19 | Wynn Millions | Wynn | ✅ Feb/Mar mapped ($7M GTD) |
| 20 | Wynn Summer Classic | Wynn | ⚠️ May/Jul series only |
| 21 | Venetian DeepStack (NYE) | Venetian | ✅ Complete |
| 22 | Venetian DeepStack (Spring) | Venetian | ✅ Complete |
| 23 | ARIA Poker Classic | ARIA | ❌ NOT SCRAPED |
| 24 | U.S. Poker Open | PokerGO | ❌ NOT SCRAPED |
| 25 | Poker Masters | PokerGO | ❌ NOT SCRAPED |
| 26 | Super High Roller Bowl | PokerGO | ❌ NOT SCRAPED |
| 27 | PokerGO Cup | PokerGO | ✅ Mar 1-15 mapped |

### Tier 4: State Recurring (25 Series)
| # | Series | State | Status |
|---|--------|-------|--------|
| 28 | L.A. Poker Classic (LAPC) | CA | ✅ 68 events complete |
| 29 | Bay 101 Shooting Star | CA | ❌ NOT SCRAPED |
| 30 | Gardens Poker Championship | CA | ❌ NOT SCRAPED |
| 31 | Bicycle Casino Series | CA | ❌ NOT SCRAPED |
| 32 | Thunder Valley Circuit | CA | ⚠️ WSOPC stop only |
| 33 | TCH Trailblazer | TX | ✅ Houston/Dallas/Austin mapped |
| 34 | TCH Poker Championship | TX | ⚠️ Big One only |
| 35 | Champions Club Series | TX | ❌ NOT SCRAPED |
| 36 | Texas Poker Open | TX | ❌ NOT SCRAPED |
| 37 | Bestbet Blizzard | FL | ✅ Feb complete |
| 38 | Bestbet Poker Series | FL | ⚠️ Winter StAC only |
| 39 | Arizona State Championship | AZ | ✅ Aug 14-20 mapped |
| 40 | MSPT Diamond (Talking Stick) | AZ | ✅ Jan complete |
| 41 | FireKeepers Series | MI | ❌ NOT SCRAPED |
| 42 | Running Aces Series | MN | ❌ NOT SCRAPED |
| 43 | Potawatomi Poker Classic | WI | ⚠️ MSPT stop only |
| 44 | Turning Stone Series | NY | ❌ NOT SCRAPED |
| 45 | Mohegan Sun Series | CT | ❌ NOT SCRAPED |
| 46 | Beau Rivage Heater | MS | ❌ NOT SCRAPED |
| 47 | Cherokee Poker Series | NC | ⚠️ WSOPC stop only |

### Tier 5: Brand-Based (4 Series)
| # | Series | Brand | Status |
|---|--------|-------|--------|
| 48 | Caesars Poker Series | Caesars | ❌ NOT SCRAPED |
| 49 | MGM Poker Series | MGM | ❌ NOT SCRAPED |
| 50 | Hard Rock Poker Series | Hard Rock | ❌ NOT SCRAPED |
| 51 | Horseshoe Poker Series | Horseshoe | ⚠️ WSOPC only |

### Additional Canonical (4 Series)
| # | Series | Tour | Status |
|---|--------|------|--------|
| 52 | WSOP Europe | WSOP | ✅ Prague Mar 31-Apr 12 |
| 53 | WPT World Championship | WPT | ⚠️ Dec TBD |
| 54 | Roughrider Poker Tour | Regional | ❌ NOT SCRAPED |
| 55 | Free Poker Network (FPN) | Amateur | ❌ NOT SCRAPED |

---

## 📊 SCRAPE STATUS SUMMARY
| Status | Count | Series |
|--------|-------|--------|
| ✅ Complete | 22 | WSOP, WSOPC, WPT, MSPT, Seminole, Borgata Winter, Venetian, LAPC, etc. |
| ⚠️ Partial | 11 | RGPS, Wynn Summer, Cherokee, Potawatomi, etc. |
| ❌ NOT SCRAPED | **22** | See list below |

---

## Priority Scraping Order
```
1. WSOPC (Jan-Dec) - 18 stops
2. WPT (year-round) - 15 stops  
3. MSPT (year-round) - 24 stops
4. Major Vegas (Wynn, Venetian, WSOP Summer)
5. Florida (Seminole, bestbet)
6. California (LAPC, Thunder Valley)
7. Regional (RGPS, state championships)
8. High Roller (PGT, Aria)
```

## Quick Commands
```bash
# Verify series counts
SELECT tour, COUNT(*) FROM poker_series GROUP BY tour ORDER BY count DESC;

# Find series needing event scraping
SELECT series_uid, series_name, start_date 
FROM poker_series 
WHERE events_scraped = FALSE 
  AND start_date > CURRENT_DATE
ORDER BY start_date;

# Count total events
SELECT COUNT(*) FROM poker_events;
```

## Typical Scrape Output
When scraping, generate SQL blocks like:
```sql
-- [TOUR NAME] [YEAR] - [VENUE]
-- Source: [url]
-- Scraped: [date]

INSERT INTO poker_series (...) VALUES (...);
INSERT INTO poker_events (...) VALUES (...), (...), ...;
```

## Daily/Weekly Automated Scraper

### Existing Infrastructure
Located at: `scripts/daily-tournament-scraper.js`

**GitHub Actions Workflow:** `.github/workflows/daily-scraper.yml`
- Runs at **6am UTC (midnight CST)** daily
- Can be manually triggered via GitHub Actions

### What It Does
1. Queries `poker_series` for series where `events_scraped = FALSE`
2. Checks if `last_scraped` is older than 7 days
3. Only processes future series (`start_date >= TODAY`)
4. Updates `scrape_status` and `last_scraped` timestamps

### Tour Configurations
```javascript
const TOUR_SCRAPERS = {
  'WSOP Circuit': { baseUrl: 'wsop.com/tournaments/', checkInterval: 7 },
  'WPT Main Tour': { baseUrl: 'worldpokertour.com/schedule/', checkInterval: 7 },
  'WPT Prime': { baseUrl: 'worldpokertour.com/schedule/', checkInterval: 7 },
  'RunGood Poker Series': { baseUrl: 'rungood.com/schedule/', checkInterval: 14 },
  'MSPT': { baseUrl: 'msptpoker.com/schedule/', checkInterval: 7 },
  'Venetian Poker Room': { baseUrl: 'venetianlasvegas.com/poker', checkInterval: 14 },
};
```

### Add New Tour to Scraper
Edit `scripts/daily-tournament-scraper.js`:
```javascript
'NEW_TOUR': {
  baseUrl: 'https://example.com/schedule/',
  urlPattern: (seriesName) => `https://example.com/${slug}/`,
  checkInterval: 7, // days between checks
},
```

### Required Secrets (GitHub Actions)
- `NEXT_PUBLIC_SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

### Run Manually
```bash
cd hub-vanguard
node scripts/daily-tournament-scraper.js
```

## Venue Monitoring List
The scraper should check these sources weekly:
| Venue | Check URL | Priority |
|-------|-----------|----------|
| Wynn | wynnlasvegas.com/poker | High |
| Venetian | venetianlasvegas.com/poker | High |
| Borgata | borgata.mgmresorts.com/poker | High |
| Seminole Hollywood | seminolehardrockpokeropen.com | High |
| Seminole Tampa | shrtpoker.com | Medium |
| Commerce (LAPC) | commercecasino.com/poker | Medium |
| bestbet Jax | bestbetjax.com/poker | Medium |
| Talking Stick | talkingstickresort.com/poker | Medium |
| Thunder Valley | thundervalleyresort.com/poker | Medium |

## Notes
- Always use `ON CONFLICT DO NOTHING` to prevent duplicates
- Generate deterministic `series_uid` and `event_uid` for idempotency
- Include source URL for verification
- Mark `scrape_status` accurately for tracking
