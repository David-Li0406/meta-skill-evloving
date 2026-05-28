# CLI Commands

All commands run from `$CLAUDE_PLUGIN_ROOT`:

```bash
cd $CLAUDE_PLUGIN_ROOT && bun run src/cli.ts <command>
```

---

## Output Format

Add `--format markdown` to any command for pre-formatted output:

```bash
bun run src/cli.ts movies --format markdown
```

| Format | Description |
|--------|-------------|
| `json` (default) | Machine-readable JSON with `selectorsUsed` debug field |
| `markdown` / `md` | Human-readable markdown, ready to display |

**Recommendation**: Use `--format markdown` to reduce token usage.

---

## movies

List all movies showing today.

```bash
bun run src/cli.ts movies --format markdown
```

**Returns**: Numbered list of movies with titles, ratings, and session times.

---

## movie

Get full movie details.

```bash
bun run src/cli.ts movie --movie-url "{MOVIE_SLUG}" --format markdown
```

**Returns**: Movie title, metadata, description, director, cast, and trailer link.

---

## pricing

Get ticket types and prices for a session.

```bash
bun run src/cli.ts pricing --session-id "{SESSION_ID}" --format markdown
```

**Returns**: Bullet list of ticket types with prices and booking fee.

---

## session

Get session details (screen, date/time).

```bash
bun run src/cli.ts session --session-id "{SESSION_ID}" --format markdown
```

**Returns**: Screen number and date/time.

---

## seats

Get seat map for a session.

```bash
bun run src/cli.ts seats --session-id "{SESSION_ID}" --format markdown
```

**Returns**: ASCII seat map in a code block with availability count.

---

## send

Generate ticket and email it.

```bash
bun run src/cli.ts send \
  --session-id "{SESSION_ID}" \
  --seats "{SEATS}" \
  --tickets "{TICKET_STRING}" \
  --format markdown
```

**Ticket string format**: `"TYPE:qty,TYPE:qty"` (e.g., `"ADULT:2,CHILD:1"`)

**Returns**: Booking confirmation with movie, date, screen, seats, and total.
