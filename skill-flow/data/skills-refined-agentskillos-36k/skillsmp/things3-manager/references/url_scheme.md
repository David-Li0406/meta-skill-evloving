# Things3 URL Scheme Reference

Quick reference for Things URL scheme parameters.

## Commands

### add (create to-do)
```
things:///add?title=...&when=today&deadline=2025-01-20&tags=work,urgent&list=ProjectName&checklist-items=Item1%0AItem2
```

Parameters:
- `title` - To-do title (required)
- `notes` - Notes text
- `when` - today, tomorrow, evening, someday, YYYY-MM-DD, or YYYY-MM-DD@HH:MM
- `deadline` - YYYY-MM-DD
- `tags` - Comma-separated tag names
- `list` - Project or area name
- `list-id` - Project or area UUID
- `heading` - Heading name within project
- `checklist-items` - Newline-separated (%0A) checklist items
- `show-quick-entry` - true to show dialog

### add-project
```
things:///add-project?title=...&area=AreaName&to-dos=Task1%0ATask2
```

Parameters:
- `title` - Project title (required)
- `notes`, `when`, `deadline`, `tags` - Same as add
- `area` - Area name
- `area-id` - Area UUID
- `to-dos` - Newline-separated to-do titles

### update (modify to-do)
Requires `auth-token` from Things settings.

```
things:///update?id=UUID&auth-token=TOKEN&title=NewTitle&when=tomorrow
```

Parameters:
- `id` - To-do UUID (required)
- `auth-token` - Auth token (required)
- `title`, `notes`, `when`, `deadline`, `tags` - Replace values
- `prepend-notes`, `append-notes` - Add to notes
- `add-tags` - Add tags without removing existing
- `list`, `list-id`, `heading` - Move to location
- `completed` - true to complete
- `canceled` - true to cancel
- `checklist-items` - Replace checklist
- `append-checklist-items` - Add to checklist

### update-project
Same as update but for projects. Use `area`/`area-id` instead of `list`/`list-id`.

### show
```
things:///show?id=UUID
things:///show?id=today
things:///show?id=inbox
```

Built-in list IDs: inbox, today, upcoming, anytime, someday, logbook, trash

### search
```
things:///search?query=keyword
```

### json (bulk operations)
```
things:///json?data=[{"type":"to-do","title":"Task"}]
```

Supports creating multiple items and nested projects with headings.

## Date Formats

- `today`, `tomorrow`, `evening`, `someday`
- `YYYY-MM-DD` (e.g., 2025-01-20)
- `YYYY-MM-DD@HH:MM` (e.g., 2025-01-20@14:00)
- Natural language in some contexts

## Getting UUIDs

Use `things3_read.py` with `--json` flag to get UUIDs:
```bash
python3 things3_read.py today --json
python3 things3_read.py search "task name" --json
```

## Auth Token

Required for update operations. Get via:
```bash
python3 things3_read.py token
```

Or in Things: Settings → General → Enable Things URLs (shows token)
