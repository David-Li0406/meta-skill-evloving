# Booking Flow

How to book tickets after a movie/time is selected.

**Variables**: See [variables.md#pricing](variables.md#pricing), [variables.md#seats](variables.md#seats), [variables.md#send](variables.md#send)

---

## Prerequisites

Before starting, you need:
- `{SESSION_ID}` - from the movies response
- `{MOVIE_TITLE}` - for confirmation messages

---

## Step 1: Confirm Selection

**Output**:
```
Great, {MOVIE_TITLE} at {SESSION_TIME}! Let me get the pricing...
```

---

## Step 2: Fetch Pricing

**Command**:
```bash
cd $CLAUDE_PLUGIN_ROOT && bun run src/cli.ts pricing --session-id "{SESSION_ID}" --format markdown
```

**Output**: The CLI returns pre-formatted markdown - display it directly.

---

## Step 3: Get Ticket Quantities

Wait for Nathan to specify quantities (e.g., "2 adults", "1 adult and 1 child").

**Calculate total**:
- Sum: (quantity × price) for each ticket type
- Add: total_tickets × booking_fee

**Output format**:
```
{TICKET_QTY} {TICKET_TYPE} ticket(s) for **{MOVIE_TITLE}** at {SESSION_TIME}

{TICKET_QTY} × {TICKET_PRICE} = ${subtotal}
Booking fee: {total_tickets} × {BOOKING_FEE} = ${fee_total}

**Total: ${TOTAL_AMOUNT}**

Now, where would you like to sit?
```

---

## Step 4: Show Seat Map

**Command**:
```bash
cd $CLAUDE_PLUGIN_ROOT && bun run src/cli.ts seats --session-id "{SESSION_ID}" --format markdown
```

**Output**: The CLI returns pre-formatted markdown with the ASCII seat map - display it directly.

---

## Step 5: Send Ticket

**Command**:
```bash
cd $CLAUDE_PLUGIN_ROOT && bun run src/cli.ts send \
  --session-id "{SESSION_ID}" \
  --seats "{SEATS}" \
  --tickets "{TICKET_STRING}" \
  --format markdown
```

**Ticket string format**: `"TYPE:qty,TYPE:qty"`
- Example: `"ADULT:2,CHILD:1"`
- Use uppercase type names exactly as returned by pricing

**Output**: The CLI returns pre-formatted booking confirmation - display it directly.

**On error**: Display an error message and ask if they want to try again.
