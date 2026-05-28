---
name: events-digest
description: Scan newsletters for local events relevant to your family
---

# Events Digest

You are a family concierge for [YOUR_NAME] and family. Scan email newsletters for events and activities in your city.

## Execution Flow

1. **Fetch event emails** from the past 3 days (or since last run if tracked):

   **Events email via Gmail MCP:**

   ```
   mcp__gmail__search_emails with query: "label:Events newer_than:3d"
   ```

   This captures event newsletters, auto-labeled via Gmail filters.

2. **Fetch local activities spreadsheet** (if you have one):

   ```
   WebFetch URL: [YOUR_COMMUNITY_ACTIVITIES_SPREADSHEET_URL]
   ```

   This could be a community-maintained list of recurring children's activities by day of week.

   **Filtering rules for activities data:**
   - **Age filter**: Filter by your child's age
   - **Location priority**: Prioritize neighborhoods closest to home
   - **Cost priority**: FREE activities first, then under $25
   - **Day matching**: Only include activities for days within the digest's date range

3. **Read each newsletter/event email** and extract event information

4. **Load references**:
   - `[YOUR_NOTES_PATH]/Resources/events-preferences.md` - What to look for, what we value
   - `references/backup-activities.md` - Evergreen activities for slow weeks

5. **Generate the digest** with sections:
   - **Happening Soon**: Events in next 7 days OR tickets/reservations opening soon
   - **Don't Miss Out**: Best picks specifically for your family
   - **Fresh**: Newly announced events
   - **Kids Activities This Week**: Age-appropriate recurring activities (grouped by day)

6. **Write to your notes location**:

   ```
   [YOUR_NOTES_PATH]/Briefings/events-YYYY-MM-DD.md
   ```

7. **Send email notification** to family members with highlights

8. **Output terminal link** to the note

## Output Format

```markdown
# Events - [Date]

## Happening Soon

- **[Event Name](link)** - Brief description. _[Venue/Location]_
  - Urgency: [Will sell out / Book now / Flexible]

## Don't Miss Out

- **[Event Name](link)** - Why this is perfect for us. _[Venue]_

## Fresh

- **[Event Name](link)** - What's new about this. _[Venue]_

## Kids Activities This Week

(Age-appropriate, prioritizing FREE and nearby)

### [Day]

- **[Activity Name]** - [Time] @ [Venue], [Neighborhood] | [Cost] | Ages [range]

### [Day]

- ...

## Evergreen Reminders

(Only if other sections are light)

- **[Activity](link)** - Why we shouldn't take this for granted
```

## Event Formatting Rules

- Every bullet MUST include a link
- Include urgency indicator for time-sensitive items
- Note if family-friendly or adults-only
- Include neighborhood/location for proximity assessment
- Keep descriptions to 1-2 sentences max

## Email Format

Subject: `Events Digest - [Date]`

Body: Top 3-5 highlights with links, then "Full digest in [notes app]"

Use Gmail MCP `draft_email` then `send_email` (or just `send_email` directly).

## Reference Files

Load these at the start of each run:

- `[YOUR_NOTES_PATH]/Resources/events-preferences.md` - User preferences
- `~/.claude/skills/events-digest/references/backup-activities.md` - Evergreen fallbacks
