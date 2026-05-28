# Meeting Minutes Tools Reference

SAGE provides access to searchable meeting minutes from Solano County committees and boards.

## Available Committees

| Committee ID | Name | Meetings | Date Range |
|--------------|------|----------|------------|
| `bos` | Board of Supervisors | 68 | 2024-01-09 to 2026-01-13 |
| `regis` | ReGIS Members (Regional GIS Consortium) | 30 | 2021-06-16 to 2026-01-21 |

## Meeting Tools

### list_committees
List all available committees with meeting counts and date ranges.

```
list_committees()
→ Returns: committee IDs, names, meeting counts, date ranges
```

### list_meetings
List meetings for a committee or year.

```
list_meetings({ committee: "bos", year: 2025 })
→ Returns: meeting IDs, dates, has_agenda, has_minutes, is_special_meeting
```

### search_meeting_minutes
Search across all meeting content with keyword matching.

```
search_meeting_minutes({
  query: "budget",
  committee: "bos",           // optional: "bos", "regis", or full name
  document_type: "minutes",   // optional: "agenda" or "minutes"
  date_from: "2025-01-01",    // optional
  date_to: "2025-12-31",      // optional
  top_k: 10                   // optional, default 10
})
→ Returns: matching chunks with relevance scores, text previews
```

**Search Tips:**
- Use specific terms: "resolution 2025", "sheriff budget", "zoning amendment"
- Filter by committee when you know which board discussed the topic
- Use date ranges to focus on recent meetings
- Search minutes for decisions/votes, agendas for upcoming items

### get_meeting
Get all content for a specific meeting.

```
get_meeting({ meeting_id: "bos-2025-12-09" })
→ Returns: all agenda items and minutes content for that meeting
```

**Meeting ID Format:**
- BOS: `bos-YYYY-MM-DD` (e.g., `bos-2025-12-09`)
- BOS Special: `bos-YYYY-MM-DD-special` (e.g., `bos-2025-12-23-special`)
- ReGIS: `regis-YYYY-MM-DD` (e.g., `regis-2026-01-21`)

### get_meeting_chunk
Get full text of a specific meeting chunk by ID.

```
get_meeting_chunk({ chunk_id: "bos-2025-12-09-minutes-001" })
→ Returns: full chunk with all metadata
```

### get_meetings_overview
Get statistics across all committees.

```
get_meetings_overview()
→ Returns: total meetings, chunks, meetings by year, chunks by committee
```

## Board of Supervisors (BOS) Meetings

### Meeting Types
- **Regular Meetings**: Typically Tuesdays at 9:00 AM
- **Special Meetings**: Budget hearings, closed sessions, emergency items

### Content Structure
BOS meeting content is organized by Legistar item numbers (e.g., "25-962").

**Chunk Types:**
| Type | Description |
|------|-------------|
| `action` | Resolutions, ordinances, contracts requiring board action |
| `public_hearing` | Items requiring public testimony |
| `report` | Receive and file reports, presentations |
| `general` | Other items, procedural matters |

### BOS-Specific Fields
- `is_special_meeting`: Boolean indicating special vs regular meeting
- `vote_result`: Vote tally when recorded (e.g., "5-0")
- `resolution_number`: Resolution number when applicable (e.g., "2025-253")

### Example Queries

**Find budget-related decisions:**
```
search_meeting_minutes({
  query: "budget appropriation",
  committee: "bos",
  document_type: "minutes",
  date_from: "2025-06-01"
})
```

**Find resolutions on a topic:**
```
search_meeting_minutes({
  query: "resolution housing",
  committee: "bos"
})
```

**Get full meeting content:**
```
get_meeting({
  meeting_id: "bos-2025-12-09",
  document_type: "minutes"
})
```

## ReGIS (Regional GIS Consortium) Meetings

### About ReGIS
The Solano Regional GIS Consortium (ReGIS) coordinates GIS activities across Solano County jurisdictions. Members include:
- Solano County departments
- Cities: Benicia, Dixon, Fairfield, Rio Vista, Suisun City, Vacaville, Vallejo
- Special districts: FSSD, SID, SCWA
- Other agencies: STA, Travis AFB, VFW

### Meeting Content
ReGIS meetings cover:
- GIS project updates and coordination
- Data sharing initiatives
- Technology discussions
- Member agency updates

**Chunk Types:**
| Type | Description |
|------|-------------|
| `attendance` | Roll call and introductions |
| `approval` | Minutes approval |
| `announcement` | Job openings, general announcements |
| `update` | Executive team and project updates |
| `discussion` | Open round table, presentations |
| `general` | Other agenda items |

### Example Queries

**Find GIS project discussions:**
```
search_meeting_minutes({
  query: "aerial imagery",
  committee: "regis"
})
```

**Find parcel data discussions:**
```
search_meeting_minutes({
  query: "parcel data feedback",
  committee: "regis",
  date_from: "2025-01-01"
})
```

## Integration Patterns

### Pattern 1: Research Board Actions
Find what the Board decided on a topic:

1. `search_meeting_minutes` → "topic" with committee: "bos", document_type: "minutes"
2. `get_meeting_chunk` → Full text of relevant items
3. Cross-reference with budget or code if needed

### Pattern 2: Track Project History
Follow a topic across multiple meetings:

1. `search_meeting_minutes` → broad search, no date filter
2. Review results chronologically
3. `get_meeting` for key meetings with detailed discussion

### Pattern 3: Prepare for Board Meeting
Research upcoming agenda items:

1. `list_meetings` → Find most recent meeting with agenda
2. `get_meeting` → document_type: "agenda"
3. Search past meetings for related decisions

### Pattern 4: Connect Policy to Decisions
Link General Plan/Code to Board actions:

1. `search_general_plan` or `search_county_code` → Find policy
2. `search_meeting_minutes` → Search for policy topic in BOS minutes
3. Explain: Policy intent → Board action → Implementation

## Data Coverage

### Board of Supervisors
- **Source**: Solano County Granicus system
- **Date Range**: January 2024 - January 2026
- **Documents**: Agendas and approved minutes
- **Update Frequency**: New meetings added periodically

### ReGIS
- **Source**: regis.solanocounty.com
- **Date Range**: June 2021 - January 2026
- **Documents**: Agendas and meeting minutes
- **Meetings**: Approximately monthly (some months skipped)

## Limitations

1. **Text-only**: Meeting content is extracted from PDFs; formatting/tables may not be preserved
2. **No attachments**: Staff reports, resolutions, and other attachments are not included
3. **Historical depth**: BOS coverage starts January 2024; earlier meetings not yet indexed
4. **Vote details**: Vote tallies may not be captured for all items
5. **Search is keyword-based**: Use specific terms rather than natural language questions

## Coming Soon

- Planning Commission meetings
- Other county boards and commissions
- Extended historical coverage
- Direct links to source documents
