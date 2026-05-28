---
name: Tournament Source Registry
description: Authoritative registry of verified source URLs for all 40 poker tournament brands. Use this skill when scraping tournament data.
---

# Tournament Source Registry Skill

## Purpose
This skill provides the **authoritative source of truth** for all poker tournament scraping operations. Every tournament brand has a verified source URL that MUST be used when building scrapers.

## 🚨 MANDATORY: Before Any Scraping Operation

1. **Consult this registry** before scraping any tournament data
2. **Use ONLY the URLs listed here** as your source of truth
3. **Never invent or extrapolate** tournament data
4. **Cite the source URL** in all generated SQL

---

## 40 Canonical Tournament Brands

### A-Tier: Major Tours (Official Websites)

| Brand | Source URL | Scrape Method |
|-------|-----------|---------------|
| **WSOP** | https://www.wsop.com/tournaments/ | HTML Table |
| **WSOP Circuit** | https://www.wsop.com/tournaments/ | HTML Table |
| **WPT** | https://www.wpt.com/schedule/ | JSON API |
| **WPT Prime** | https://www.wpt.com/schedule/ | JSON API |
| **MSPT** | https://msptpoker.com/schedule/ | HTML Cards |
| **RGPS** | https://rungoodpokerseries.com/schedule/ | HTML Cards |
| **PokerStars NAPT** | https://www.pokerstarslive.com/napt/ | HTML Table |
| **PokerGO Tour** | https://www.pokergo.com/schedule | JSON API |
| **Roughrider** | https://roughriderpokertour.com/schedule/ | HTML Cards |
| **Bar Poker Open** | https://barpokeropen.com/events/ | HTML Cards |
| **FPN** | https://freepokernetwork.com/events/ | HTML Cards |
| **LIPS** | https://www.lipspoker.com/schedule/ | Manual |
| **Card Player Cruises** | https://www.cardplayercruises.com/cruises/ | Manual |

### B-Tier: Vegas Venues (PokerAtlas Preferred)

| Venue | PokerAtlas URL |
|-------|---------------|
| **Wynn** | https://www.pokeratlas.com/poker-room/wynn-las-vegas/tournaments |
| **Venetian** | https://www.pokeratlas.com/poker-room/venetian-poker-room/tournaments |
| **ARIA** | https://www.pokeratlas.com/poker-room/aria-poker-room/tournaments |
| **ARIA Poker Classic** | https://www.pokeratlas.com/poker-room/aria-poker-room/tournaments |
| **U.S. Poker Open** | https://www.pokergo.com/schedule |
| **Poker Masters** | https://www.pokergo.com/schedule |

### C-Tier: Regional Venues (PokerAtlas)

| Venue | PokerAtlas URL |
|-------|---------------|
| **Borgata** | https://www.pokeratlas.com/poker-room/borgata-poker-room/tournaments |
| **Seminole Hard Rock** | https://www.pokeratlas.com/poker-room/seminole-hard-rock-hollywood/tournaments |
| **bestbet Jacksonville** | https://www.pokeratlas.com/poker-room/bestbet-jacksonville/tournaments |
| **Bay 101** | https://www.pokeratlas.com/poker-room/bay-101-casino/tournaments |
| **Thunder Valley** | https://www.pokeratlas.com/poker-room/thunder-valley-casino-resort/tournaments |
| **Graton** | https://www.pokeratlas.com/poker-room/graton-resort-casino/tournaments |
| **LAPC/Commerce** | https://www.pokeratlas.com/poker-room/commerce-casino/tournaments |
| **FireKeepers** | https://www.pokeratlas.com/poker-room/firekeepers-casino-hotel/tournaments |
| **Canterbury Park** | https://www.pokeratlas.com/poker-room/canterbury-park/tournaments |
| **Running Aces** | https://www.pokeratlas.com/poker-room/running-aces-casino/tournaments |
| **Mohegan Sun** | https://www.pokeratlas.com/poker-room/mohegan-sun-casino/tournaments |
| **Maryland Live** | https://www.pokeratlas.com/poker-room/maryland-live/tournaments |
| **MGM National Harbor** | https://www.pokeratlas.com/poker-room/mgm-national-harbor/tournaments |
| **Beau Rivage** | https://www.pokeratlas.com/poker-room/beau-rivage-resort-casino/tournaments |
| **Choctaw** | https://www.pokeratlas.com/poker-room/choctaw-casino-durant/tournaments |
| **Hard Rock Tulsa** | https://www.pokeratlas.com/poker-room/hard-rock-tulsa/tournaments |
| **Talking Stick** | https://www.pokeratlas.com/poker-room/talking-stick-resort/tournaments |
| **JACK Cleveland** | https://www.pokeratlas.com/poker-room/jack-cleveland-casino/tournaments |
| **Parx Casino** | https://www.pokeratlas.com/poker-room/parx-casino/tournaments |

### D-Tier: Texas Rooms

| Venue | PokerAtlas URL |
|-------|---------------|
| **TCH Dallas** | https://www.pokeratlas.com/poker-room/texas-card-house-dallas/tournaments |
| **TCH Houston** | https://www.pokeratlas.com/poker-room/texas-card-house-houston/tournaments |
| **The Lodge** | https://www.pokeratlas.com/poker-room/the-lodge-card-club/tournaments |
| **Champions Club** | https://www.pokeratlas.com/poker-room/champions-club-houston/tournaments |

### Special Status

| Brand | Status |
|-------|--------|
| **HPT** | ❌ DEFUNCT - Tour closed 2019 |
| **Regional** | https://www.pokeratlas.com/poker-tournaments |

---

## Database Schema

The `poker_series` table includes these scrape-tracking columns:

```sql
scrape_url TEXT        -- Authoritative source URL
last_scraped TIMESTAMPTZ  -- Last successful scrape timestamp
events_count INTEGER   -- Number of events in series
```

---

## SQL Template for New Series

```sql
INSERT INTO poker_series (
  series_uid, tour, series_name, venue, city, state, country,
  start_date, end_date, source, scrape_url
) VALUES (
  'series-uid-here',
  'TOUR_NAME',
  'Series Name Here',
  'Venue Name',
  'City',
  'ST',
  'USA',
  '2026-MM-DD',
  '2026-MM-DD',
  'Source Name',
  'https://source-url-here.com/schedule/'
) ON CONFLICT (series_uid) DO UPDATE SET
  scrape_url = EXCLUDED.scrape_url,
  updated_at = NOW();
```

---

## Scraper Implementation Pattern

```javascript
// Each tour gets its own scraper module
const TOUR_SCRAPERS = {
  'WSOP': {
    url: 'https://www.wsop.com/tournaments/',
    parser: parseWSOP,
    selector: '.tournament-row'
  },
  'MSPT': {
    url: 'https://msptpoker.com/schedule/',
    parser: parseMSPT,
    selector: '.event-card'
  }
  // ... etc
};
```
