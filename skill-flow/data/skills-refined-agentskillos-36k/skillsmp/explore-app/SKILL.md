---
name: explore-app
description: Explore the Map Pin application features using parallel subagents. Launches 6 agents to explore map navigation, pin fields, search/filter, CRUD, sessions, and pin list features.
allowed-tools: Task, Read, Write, Bash, Glob
---

# Explore App Features

Launches multiple subagents in parallel to explore different feature areas of the Map Pin application.

## Usage

```
/explore-app
```

## What It Does

Spawns 6 parallel agents, each exploring a different feature:

1. **Map Navigation** - zoom controls, panning, map coordinates
2. **Pin Form Fields** - all form inputs and their accessible names
3. **Search & Filter** - search behavior, category filter, empty states
4. **CRUD & Snackbars** - create/read/update/delete, notifications
5. **Sessions & Spectator** - multi-session, watching mode
6. **Pin List & Categories** - list display, category colors

## Instructions

When this skill is invoked, create the screenshot directories and launch all 6 agents **in parallel** using the Task tool.

### Setup

```bash
mkdir -p screenshots/explore/{map-nav,pin-fields,search-filter,crud,sessions,pin-list}
```

### Launch These 6 Agents in Parallel

Use `Task` tool with `subagent_type: "general-purpose"` for each (they have Bash access to run agent-browser commands):

**Agent 1 - Map Navigation:**
```
Explore map navigation at http://localhost:5173

1. Open app, snapshot initial state
2. Find zoom controls - look for buttons without visible names in the map region
3. After zoom actions, check the Google Maps link URL which contains zoom level (z=XX) and coordinates (ll=lat,lng)
4. Document what map controls exist and how to verify zoom/pan changes
5. Click on map region to verify pin creation opens

Save screenshots to screenshots/explore/map-nav/
```

**Agent 2 - Pin Form Fields:**
```
Explore all pin form fields at http://localhost:5173

1. Click map region to open pin creation form
2. Snapshot and document ALL form fields with their exact accessible names:
   - Title field
   - Description field
   - Category dropdown (list all options)
   - Rating radio buttons (document exact names like "1 Star", "5 Stars")
   - Tags autocomplete
   - Date Visited picker
   - Favorite switch
3. Test filling each field and saving
4. Reopen pin to verify data persisted

Save screenshots to screenshots/explore/pin-fields/
```

**Agent 3 - Search & Filter:**
```
Explore search and filter at http://localhost:5173

1. Document the search input accessible name
2. Create 2-3 test pins with different categories
3. Test search - find the textbox, type search terms, observe results
4. Test search with no matches - document empty state message
5. Test category filter dropdown - list all options
6. Test filter with no matches - document empty state

Save screenshots to screenshots/explore/search-filter/
```

**Agent 4 - CRUD & Snackbars:**
```
Explore CRUD and notifications at http://localhost:5173

1. CREATE: Make a pin, observe for snackbar notification text
2. READ: Click pin in list, verify drawer opens
3. UPDATE: Change a field, save, look for snackbar text
4. DELETE: Delete pin, look for snackbar text
5. PERSISTENCE: Create pin, use "goto" to refresh page, verify pin exists
6. Document exact snackbar message text for each operation

Save screenshots to screenshots/explore/crud/
```

**Agent 5 - Sessions & Spectator:**
```
Explore sessions at http://localhost:5173

1. Find session info in sidebar - look for "You:" and session name
2. Find "Sessions Connected" section
3. Document how other sessions appear (as buttons?)
4. If other sessions exist, try clicking one
5. Look for "Watching" banner or spectator indicators
6. Document session-related UI elements and their accessible names

Save screenshots to screenshots/explore/sessions/
```

**Agent 6 - Pin List Display:**
```
Explore pin list display at http://localhost:5173

1. Snapshot the sidebar pin list structure
2. Document pin list item format:
   - How title appears
   - How rating appears (img with "X Stars"?)
   - How category appears
   - How tags appear
   - Favorite indicator if any
3. Create pins with different categories, note any visual differences
4. Document the pins count display format

Save screenshots to screenshots/explore/pin-list/
```

### After All Agents Complete

1. Read each agent's output
2. Consolidate findings into `docs/plans/e2e-test-strategy.md`
3. Create an implementation checklist with atomic, incremental tasks
4. Ask user for confirmation before implementing
