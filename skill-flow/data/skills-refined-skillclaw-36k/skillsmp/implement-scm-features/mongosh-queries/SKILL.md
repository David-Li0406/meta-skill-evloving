# SCM MongoDB Queries with mongosh

Quick reference for querying SCM-related collections using mongosh.

## Connection

**Important:** Always source `.env.local` first to load the `DATABASE_URL` environment variable:

```bash
source /Users/alexsmith/ai-coaching-platform/.env.local 2>/dev/null
mongosh "$DATABASE_URL" --eval "YOUR_COMMAND_HERE"
```

Or as a one-liner:

```bash
source /Users/alexsmith/ai-coaching-platform/.env.local 2>/dev/null && mongosh "$DATABASE_URL" --eval "YOUR_COMMAND_HERE"
```

## Query Categories

- [students.md](students.md) - Student records and progress
- [sections.md](sections.md) - Section configs and class settings
- [podsie.md](podsie.md) - Podsie completions and assignments
- [roadmaps.md](roadmaps.md) - Units, skills, and student assessment data
- [curriculum.md](curriculum.md) - Scope and sequence, learning content
- [calendar.md](calendar.md) - Unit schedules and planning
- [analytics.md](analytics.md) - Aggregations and reports
- [data-fixes.md](data-fixes.md) - Updates, bulk operations, and index management

## Tips

- **Escape `$`**: Use `\$` for MongoDB operators in shell commands
- **Use `.limit(N)`**: Always limit results when exploring data
- **Use `printjson()`**: For formatted JSON output
- **Check schema files**: See `src/lib/schema/mongoose-schema/` for field names
- **ID mismatch warning**: `students.studentID` (number) vs `roadmaps-student-data.studentId` (string slug)
