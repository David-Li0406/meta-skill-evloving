# Browsing Flow

How to show movies and movie details.

**Variables**: See [variables.md#movies](variables.md#movies) and [variables.md#movie](variables.md#movie)

---

## Step 1: List Movies

**Command**:
```bash
cd $CLAUDE_PLUGIN_ROOT && bun run src/cli.ts movies --format markdown
```

**Output**: The CLI returns pre-formatted markdown - display it directly.

**Note**: Save the JSON from `sessionTimes[].sessionId` internally for booking.

---

## Step 2: Movie Details (Optional)

**Triggers**: "tell me more about X", "what's X about?"

**Command**:
```bash
cd $CLAUDE_PLUGIN_ROOT && bun run src/cli.ts movie --movie-url "{MOVIE_SLUG}" --format markdown
```

**Output**: The CLI returns pre-formatted markdown - display it directly.

**Note**: Session times come from `movies` response, not `movie` response. Use `{MOVIE_SLUG}` from movies response for the `--movie-url` parameter.

---

## Transition to Booking

When Nathan picks a time (e.g., "the 3pm", "book the 7:00pm session"):

1. Note the `{SESSION_ID}` from the movies response for that time
2. Confirm: "Great, {MOVIE_TITLE} at {SESSION_TIME}! Let me get pricing..."
3. Continue to [booking.md](booking.md) Step 2
