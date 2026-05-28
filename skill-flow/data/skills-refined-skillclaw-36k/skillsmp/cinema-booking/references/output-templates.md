# Output Templates

Quick reference for display formats. For full workflows, see [browsing.md](browsing.md) and [booking.md](booking.md).

---

## Movies List

```
## Movies Showing Today

**1. {MOVIE_TITLE}** ({RATING})
   {SESSION_TIMES}
   {MOVIE_URL}

---

Want details on any of these, or pick a time to book?
```

---

## Movie Details

```
## {MOVIE_TITLE}

**{RATING}** | {DURATION} | {COUNTRY}

{DESCRIPTION}

**Director**: {DIRECTOR}
**Cast**: {CAST}

**Trailer**: {TRAILER_URL}

---

**Session times**: {SESSION_TIMES}

Want to book? Pick a time above.
```

---

## Pricing

```
**Available ticket types:**
- {TICKET_TYPE_NAME}: {TICKET_PRICE}

**Booking fee**: {BOOKING_FEE} per ticket

How many tickets?
```

---

## Pricing Summary

```
{TICKET_QTY} {TICKET_TYPE} for **{MOVIE_TITLE}** at {SESSION_TIME}

{TICKET_QTY} × {TICKET_PRICE} = ${subtotal}
Booking fee: {total_tickets} × {BOOKING_FEE} = ${fee}

**Total: ${TOTAL_AMOUNT}**

Where would you like to sit?
```

---

## Seat Map

```
**{SCREEN_NUMBER}**

\`\`\`
[ASCII MAP FROM STDERR]
\`\`\`

{AVAILABLE_SEATS} / {TOTAL_SEATS} available

Pick a seat (e.g., "E8").
```

---

## Booking Confirmation

```
Your ticket has been sent to your email.

---

**{MOVIE_TITLE}**
- **Date**: {SESSION_DATETIME}
- **Screen**: {SCREEN_NUMBER}
- **Seat(s)**: {SEATS}
- **Total**: ${TOTAL_AMOUNT}

Enjoy the film!
```
