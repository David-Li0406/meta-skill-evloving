# Variable Mappings

Maps CLI JSON output fields to template variables for consistent prompting.

---

## movies

**Command**: `bun run src/cli.ts movies`

| JSON Field | Variable | Type | Example |
|------------|----------|------|---------|
| `movies[].title` | `{MOVIE_TITLE}` | string | Wicked: For Good |
| `movies[].rating` | `{RATING}` | string | PG |
| `movies[].thumbnail` | `{THUMBNAIL_URL}` | string | https://movingstory-prod.imgix.net/... |
| `movies[].movieUrl` | `{MOVIE_URL}` | string | https://www.classiccinemas.com.au/movies/wicked-for-good |
| `movies[].slug` | `{MOVIE_SLUG}` | string | wicked-for-good |
| `movies[].sessionTimes[].time` | `{SESSION_TIME}` | string | 3:00 pm |
| `movies[].sessionTimes[].sessionId` | `{SESSION_ID}` | string | 116239 |

**Transform**: Join `sessionTimes[].time` with ` | ` for display as `{SESSION_TIMES}`

---

## movie

**Command**: `bun run src/cli.ts movie --movie-url "{MOVIE_SLUG}"`

| JSON Field | Variable | Type | Example |
|------------|----------|------|---------|
| `title` | `{MOVIE_TITLE}` | string | You will be changed |
| `description` | `{DESCRIPTION}` | string | And now whatever way... |
| `trailerUrl` | `{TRAILER_URL}` | string\|null | https://youtube.com/... |
| `rating` | `{RATING}` | string\|null | PG |
| `duration` | `{DURATION}` | string\|null | 2h 40min |
| `country` | `{COUNTRY}` | string\|null | USA |
| `cast` | `{CAST}` | string\|null | Cynthia Erivo, Ariana Grande |
| `director` | `{DIRECTOR}` | string\|null | Jon M. Chu |
| `eventLinks[].name` | `{EVENT_NAME}` | string | BYO Baby at Classic |
| `eventLinks[].url` | `{EVENT_URL}` | string | /events/byo-baby-at-classic |

**Note**: Omit null fields from output (don't show "Unknown")

---

## session

**Command**: `bun run src/cli.ts session --session-id "{SESSION_ID}"`

| JSON Field | Variable | Type | Example |
|------------|----------|------|---------|
| `screenNumber` | `{SCREEN_NUMBER}` | string | Screen 3 |
| `dateTime` | `{SESSION_DATETIME}` | string | 1 Dec 2025, 3:30pm-5:36pm |

---

## pricing

**Command**: `bun run src/cli.ts pricing --session-id "{SESSION_ID}"`

| JSON Field | Variable | Type | Example |
|------------|----------|------|---------|
| `ticketTypes[]` | `{TICKET_TYPES}` | array | [{name, price}, ...] |
| `ticketTypes[].name` | `{TICKET_TYPE_NAME}` | string | ADULT |
| `ticketTypes[].price` | `{TICKET_PRICE}` | string | $27.00 |
| `bookingFee` | `{BOOKING_FEE}` | string | $1.95 |

**Transform**: Remove `$` and parse as float for calculations

---

## seats

**Command**: `bun run src/cli.ts seats --session-id "{SESSION_ID}"`

| JSON Field | Variable | Type | Example |
|------------|----------|------|---------|
| `seatMap.screenNumber` | `{SCREEN_NUMBER}` | string | Screen 3 |
| `seatMap.rows` | `{SEAT_ROWS}` | object | Keyed by row letter |
| `seatMap.rows[].id` | `{SEAT_ID}` | string | F9 |
| `seatMap.rows[].available` | `{SEAT_AVAILABLE}` | boolean | true |
| `seatMap.rows[].wheelchair` | `{SEAT_WHEELCHAIR}` | boolean | false |
| `seatMap.availableCount` | `{AVAILABLE_SEATS}` | number | 131 |
| `seatMap.totalSeats` | `{TOTAL_SEATS}` | number | 152 |

**Note**: CLI outputs ASCII seat map to stderr - display in code block

---

## send

**Command**: `bun run src/cli.ts send --session-id "{SESSION_ID}" --seats "{SEATS}" --tickets "{TICKET_STRING}"`

| JSON Field | Variable | Type | Example |
|------------|----------|------|---------|
| `success` | `{SEND_SUCCESS}` | boolean | true |
| `messageId` | `{MESSAGE_ID}` | string | 19ad73fd95486472 |
| `movieTitle` | `{MOVIE_TITLE}` | string | JIFF: The Pianist's Choice |
| `sessionDateTime` | `{SESSION_DATETIME}` | string | 1 Dec 2025, 3:30pm-5:36pm |
| `screenNumber` | `{SCREEN_NUMBER}` | string | Screen 3 |
| `seats` | `{SEATS}` | string | J6 |
| `pricing.tickets[].type` | `{TICKET_TYPE}` | string | ADULT |
| `pricing.tickets[].quantity` | `{TICKET_QTY}` | number | 1 |
| `pricing.ticketSubtotal` | `{TICKET_SUBTOTAL}` | number | 27 |
| `pricing.bookingFee` | `{BOOKING_FEE_AMOUNT}` | number | 1.95 |
| `pricing.totalAmount` | `{TOTAL_AMOUNT}` | number | 28.95 |

**Ticket string format**: `"TYPE:qty,TYPE:qty"` e.g., `"ADULT:2,CHILD:1"`
