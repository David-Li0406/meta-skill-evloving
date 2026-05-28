---
name: obsidian-vault
description: Context for Kevin's Obsidian vault structure, organization, and search strategies. Use for Obsidian notes, meetings, people profiles, and SIC docs.
---

# Obsidian Vault Context Skill

## Purpose
This skill provides comprehensive context about Kevin's Obsidian vault structure, file organization, naming conventions, and search strategies. It helps GitHub Copilot quickly locate and work with Obsidian notes without searching through random directories.

## When to Use This Skill
Invoke this skill when the user asks questions about:
- **People and meetings**: "When was the last time I met with [person]?", "What did we discuss with [person]?"
- **Topics and decisions**: "What did we decide about [topic]?", "When did we talk about [subject]?"
- **Creating new content**: "Create a meeting note", "Add a person profile"
- **Vault navigation**: Finding specific types of notes or understanding file locations
- **Obsidian configuration**: Plugin settings, templates, daily notes setup

## Vault Location
**Primary Vault:** `/Users/kevin/Documents/Obsidian/HPE/`

## Directory Structure

### Core Directories

#### `/Daily Notes/`
- **Purpose**: Daily notes created automatically via Daily Notes plugin
- **Format**: `YYYY-MM-DD.md` (e.g., `2024-01-13.md`)
- **Template**: `/Templates/Daily Template.md`
- **Contains**: 
  - Todoist task queries (Today's Tasks, This Week's Tasks)
  - Meeting links for that day
  - Short conversations and notes
  - Button macros for quick note creation

#### `/Meetings/`
- **Purpose**: Meeting notes organized by date and meeting name
- **Format**: `YYYY-MM-DD - [Meeting Name].md` (e.g., `2024-01-05 - Green Standup.md`)
- **Template**: `/Templates/Meeting Notes.md`
- **Contains**:
  - Frontmatter with `when` date and `tags: [meeting]`
  - Notable Attendees (with wiki links to People profiles)
  - Subject, Notes, Take Aways, Actions
- **Common Meeting Types**:
  - Green Standup
  - Magenta Standup
  - Aruba Weekly Sync
  - SIC Istanbul Sync
  - Storage Interlock
  - COM Interlock
  - 1-1 meetings

#### `/People/`
- **Purpose**: Person profiles for colleagues and contacts
- **Format**: `[Last Name], [First Name].md` (e.g., `Pahwa, Kashish.md`)
- **Contains**:
  - Frontmatter with `aliases: [First Last]` for easy linking
  - Overview section with role/title
  - Links to relevant projects (e.g., `[[SIC/Sustainability Insight Center]]`)
- **Usage**: Referenced in meeting notes with wiki links `[[Pahwa, Kashish]]`

#### `/SIC/`
- **Purpose**: Sustainability Insight Center (SIC) related notes
- **Contains**:
  - Technical documentation
  - Customer information
  - Project-specific notes
  - Integration details (Aruba, Storage, OpsRamp, etc.)
- **Key Files**:
  - `Sustainability Insight Center.md` - Main project overview
  - `SIC Customers.md` - Customer list
  - Various integration and technical notes

#### `/Templates/`
- **Purpose**: Templater templates for note creation
- **Files**:
  - `Daily Template.md` - Auto-applied to daily notes
  - `Meeting Notes.md` - Meeting note template
  - `Green Standup Notes.md` - Green team standup template
  - `Magenta Standup Notes.md` - Magenta team standup template
  - `Note.md` - Generic note template

#### `/Notes/`
- **Purpose**: General project notes and documentation
- **Usage**: Standalone notes not tied to meetings or daily entries

#### `/Clippings/`
- **Purpose**: Web clippings and saved articles

#### `/Omnivore/`
- **Purpose**: Articles saved via Omnivore plugin
- **Structure**: Organized by date subdirectories `YYYY-MM-DD/`

#### `/Green Lake/`
- **Purpose**: HPE GreenLake platform related notes

#### `/Groups/`
- **Purpose**: Team or group related notes

#### `/Media/`
- **Purpose**: Images, screenshots, and media files

## Installed Plugins

### Active Community Plugins
1. **calendar** - Calendar view for daily notes
2. **dataview** - Query and display data from notes
3. **cm-editor-syntax-highlight-obsidian** - Enhanced syntax highlighting
4. **obsidian-outliner** - Better list handling
5. **templater-obsidian** - Advanced templating (uses `<% %>` syntax)
6. **todoist-sync-plugin** - Todoist integration with query blocks
7. **buttons** - Inline button creation with `button` code blocks
8. **periodic-notes** - Weekly/monthly note creation
9. **nldates-obsidian** - Natural language date parsing
10. **obsidian-jira-issue** - JIRA integration
11. **obsidian-omnivore** - Omnivore article saving
12. **editing-toolbar** - Enhanced editing toolbar

### Plugin Configuration

#### Daily Notes (`daily-notes.json`)
```json
{
  "folder": "Daily Notes",
  "autorun": true,
  "template": "Templates/Daily Template"
}
```

#### Templates (`templates.json`)
```json
{
  "folder": ""
}
```

## Todoist Integration

### Query Format (Updated Syntax)
```todoist
name: [Query Name]
filter: "[Todoist Filter]"
groupBy: date
sorting:
- date
- priority
```

**Important**: Use `groupBy: date` NOT `group: true` (old syntax deprecated)

### Common Filters
- `"#HPE & (today | overdue)"` - Today's and overdue HPE tasks
- `"#HPE & 7 days & !today"` - This week's HPE tasks (excluding today)

## Naming Conventions

### Meeting Notes
- **Format**: `YYYY-MM-DD - [Meeting Name].md`
- **Examples**:
  - `2024-01-05 - Green Standup.md`
  - `2024-01-03 - Royce 1-1.md`
  - `2024-01-05 - Kasish Devices and Workspaces.md`

### People Profiles
- **Format**: `[Last Name], [First Name].md`
- **Aliases**: Include `[First Last]` in frontmatter for easier linking
- **Example**:
  ```yaml
  ---
  aliases:
    - Kashish Pahwa
  ---
  ```

### Daily Notes
- **Format**: `YYYY-MM-DD.md`
- **Auto-created**: Via Daily Notes plugin in `/Daily Notes/` folder

## Wiki Links and References

### Linking Conventions
- **People**: `[[Pahwa, Kashish]]` or `[[Kashish Pahwa]]` (via alias)
- **Projects**: `[[SIC/Sustainability Insight Center]]`
- **Other notes**: `[[Note Name]]`

### Tags
- `#meeting` - Applied to all meeting notes
- `#note` - Applied to general notes
- `#HPE` - Used in Todoist filters for work tasks

## Dataview Queries

### Meeting List in Daily Notes
```dataview
LIST
WHERE when=date(this.file.name) AND contains(tags, "meeting")
```

### Note List in Daily Notes
```dataview
LIST
WHERE when=date(this.file.name) AND contains(tags, "note")
```

## Search Strategies

### Finding Meetings with a Person
1. **Check People profile**: `/People/[Last], [First].md` may have backlinks
2. **Search Meetings directory**: 
   ```bash
   grep -r "[Person Name]" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"
   ```
3. **Look for wiki links**: Search for `[[Last, First]]` or `[[First Last]]`

### Finding Discussions About a Topic
1. **Check SIC directory**: Topic-specific notes in `/SIC/`
2. **Search Meetings**: 
   ```bash
   grep -ri "[topic]" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"
   ```
3. **Search Daily Notes**: May contain brief mentions
4. **Check Notes directory**: Standalone documentation

### Finding Decisions
1. **Search for "decide"/"decided"** in Meetings:
   ```bash
   grep -ri "decide" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md" | grep -i "[topic]"
   ```
2. **Check "Take Aways" sections**: Meeting notes have Take Aways section
3. **Check "Actions" sections**: Action items from meetings

## Quick Reference Commands

### Search by Person
```bash
# Find all meetings with a person
grep -ri "kashish" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"

# Find person's profile
ls /Users/kevin/Documents/Obsidian/HPE/People/ | grep -i kashish
```

### Search by Topic
```bash
# Find topic in meetings
grep -ri "juniper" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"

# Find topic in SIC notes
grep -ri "horizontal.*scaler" /Users/kevin/Documents/Obsidian/HPE/SIC/ --include="*.md"
```

### Search by Date Range
```bash
# Find meetings in January 2024
ls /Users/kevin/Documents/Obsidian/HPE/Meetings/ | grep "^2024-01-"

# Find daily notes in a date range
ls /Users/kevin/Documents/Obsidian/HPE/Daily\ Notes/ | grep "^2024-01-"
```

### Find Recent Meetings
```bash
# List meetings sorted by date (most recent last)
ls -t /Users/kevin/Documents/Obsidian/HPE/Meetings/ | head -20
```

## Common Workflows

### Answer "When was the last meeting with [Person]?"
1. Search Meetings directory for person's name
2. Look at filenames to get dates (format: YYYY-MM-DD)
3. Sort by date to find most recent
4. Can also check person's profile for backlinks

### Answer "What did we discuss/decide about [Topic]?"
1. Search Meetings directory for topic keyword
2. Search SIC directory if topic is SIC-related
3. Look in relevant sections: Subject, Notes, Take Aways, Actions
4. Check Daily Notes for brief mentions

### Create New Meeting Note
1. Use format: `YYYY-MM-DD - [Meeting Name].md`
2. Place in `/Meetings/` directory
3. Apply Meeting Notes template
4. Add frontmatter with date and meeting tag
5. Link to attendees' People profiles

### Create New Person Profile
1. Use format: `[Last], [First].md`
2. Place in `/People/` directory
3. Add frontmatter with aliases
4. Add Overview with role/context
5. Link to relevant projects

## Team Context

### Teams Mentioned
- **Green Team**: Has daily standups, planning meetings
- **Magenta Team**: Has daily standups
- **SIC Team**: Sustainability Insight Center project team

### Common Meeting Types
- Daily standups (Green, Magenta)
- Weekly syncs (Aruba, Istanbul)
- Planning meetings
- Interlocks (Storage, COM)
- 1-1 meetings

## Best Practices

1. **Always check exact directories first** - Don't search randomly
2. **Use grep with specific paths** - More efficient than broad searches
3. **Look for wiki link patterns** - `[[Name]]` for finding references
4. **Check both Meetings and Daily Notes** - Information may be in either
5. **Use date-based sorting** - Files are date-prefixed for easy sorting
6. **Check People profiles for context** - May have role/project information
7. **Search multiple forms of names** - "Kashish", "Pahwa", "Pahwa, Kashish"

## Example Queries and Responses

### Query: "When was the last time I was in a meeting with Kashish?"
**Strategy**:
1. Search: `grep -ri "kashish" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"`
2. Extract dates from filenames
3. Sort and return most recent

### Query: "When was the last time we talked about integrating with Juniper?"
**Strategy**:
1. Search: `grep -ri "juniper" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"`
2. Also search: `/SIC/` directory if SIC-related
3. Extract dates and contexts

### Query: "What did we decide to do about the horizontal auto scaler for SIC?"
**Strategy**:
1. Search SIC directory: `grep -ri "horizontal.*scaler" /Users/kevin/Documents/Obsidian/HPE/SIC/ --include="*.md"`
2. Search Meetings: `grep -ri "horizontal.*scaler" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"`
3. Look for "decide" or "decision" near mentions
4. Check Take Aways and Actions sections

## File Locations Quick Reference

| Content Type | Directory | Format |
|-------------|-----------|---------|
| Daily Notes | `/Daily Notes/` | `YYYY-MM-DD.md` |
| Meetings | `/Meetings/` | `YYYY-MM-DD - [Name].md` |
| People | `/People/` | `[Last], [First].md` |
| SIC Notes | `/SIC/` | `[Topic].md` |
| Templates | `/Templates/` | `[Template Name].md` |
| General Notes | `/Notes/` | `[Note Name].md` |
| Web Clippings | `/Clippings/` | Various |
| Saved Articles | `/Omnivore/` | `YYYY-MM-DD/` subdirs |
| GreenLake | `/Green Lake/` | Various |
| Media | `/Media/` | Images, screenshots |

---

**Remember**: This vault is highly structured. Always use the specific directories and naming conventions described above rather than searching broadly.
