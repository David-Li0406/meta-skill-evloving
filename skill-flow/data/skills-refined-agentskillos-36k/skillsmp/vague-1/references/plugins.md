# Vague Plugins

## Built-in Plugins

### Faker Plugin

Common shorthand generators (no namespace required):

```vague
id: uuid()
email: email()
phone: phone()
name: firstName() | lastName() | fullName()
company: companyName()
address: streetAddress()
location: city() | state() | zipCode()
text: sentence()
```

Full faker namespace for advanced generators:

```vague
product: faker.commerce.productName()
bio: faker.lorem.paragraph()
avatar: faker.image.avatar()
version: faker.system.semver()
commit: faker.git.commitSha()
url: faker.internet.url()
```

### Issuer Plugin (Edge Case Testing)

Generates problematic but valid values for testing edge cases:

```vague
// Unicode edge cases
name: issuer.zeroWidth()          // Strings with zero-width characters
display: issuer.homoglyph("admin") // Lookalike characters (аdmin vs admin)
label: issuer.rtl()               // Right-to-left override
icon: issuer.emoji()              // Multi-codepoint emoji

// String edge cases
empty: issuer.empty()             // Empty string
spaces: issuer.whitespace()       // Whitespace-only strings
long: issuer.long(10000)          // Very long strings
sql: issuer.sqlLike()             // SQL injection-like text
html: issuer.htmlSpecial()        // HTML special characters
json: issuer.jsonSpecial()        // JSON special characters

// Numeric edge cases
big: issuer.maxInt()              // Maximum safe integer
small: issuer.minInt()            // Minimum safe integer
tiny: issuer.tinyDecimal()        // Very small decimal
precision: issuer.floatPrecision() // Floating point issues
negzero: issuer.negativeZero()    // -0

// Date edge cases
leap: issuer.leapDay()            // Feb 29
y2k: issuer.y2k()                 // Year 2000 edge cases
epoch: issuer.epoch()             // Unix epoch boundaries
future: issuer.farFuture()        // Very far future dates

// Format edge cases
email: issuer.weirdEmail()        // Valid but unusual emails
url: issuer.weirdUrl()            // Valid but unusual URLs
uuid: issuer.specialUuid()        // Edge case UUIDs
```

### Regex Plugin

Generate strings matching patterns:

```vague
code: regex("[A-Z]{3}-[0-9]{4}")  // "ABC-1234"
token: alphanumeric(32)           // 32 random alphanumeric chars
pin: digits(6)                    // 6 random digits
version: semver()                 // "1.2.3"
```

Pattern validation in constraints:

```vague
assume matches("^[A-Z]{3}", code)
```

## Custom Plugins

Create custom generators:

```typescript
import { VaguePlugin, registerPlugin } from 'vague';

const myPlugin: VaguePlugin = {
  name: 'custom',
  generators: {
    'greeting': () => 'Hello!',
    'repeat': (args) => String(args[0]).repeat(Number(args[1]) || 1),
  },
};
registerPlugin(myPlugin);
```

Config file (`vague.config.js`):

```javascript
export default {
  plugins: [
    './my-plugin.js',           // Local plugin file
    'vague-plugin-stripe',      // npm package
  ],
  seed: 42,
  pretty: true
};
```

Auto-discovery paths:
- `./plugins/`
- `./vague-plugins/`
- `node_modules/vague-plugin-*`

### Date Plugin

Day-of-week filtering for realistic business data:

```vague
// Weekday dates only (Monday-Friday)
meeting: date.weekday(2024, 2025)

// Weekend dates only (Saturday-Sunday)
party: date.weekend(2024, 2025)

// Specific day of week (0=Sun, 1=Mon, ..., 6=Sat)
monday: date.dayOfWeek(1, 2024, 2025)

// Shorthand (no namespace)
weekday(2024, 2025)
weekend(2024, 2025)
```

### HTTP Plugin

Generate HTTP-related test data for API testing and webhooks:

```vague
// Methods and status codes
method: http.method()                 // Weighted HTTP methods
status: http.statusCode()             // Realistic status codes
text: http.statusText(404)            // "Not Found"

// Headers
content: http.contentType()           // MIME types
agent: http.userAgent()               // Browser/bot user agents
accept: http.accept()                 // Accept header values
cache: http.cacheControl()            // Cache-Control directives

// CORS
origin: http.corsOrigin()
methods: http.corsMethods()
headers: http.corsHeaders()

// Authorization
bearer: http.bearerToken()            // "Bearer abc123..."
basic: http.basicAuth()               // "Basic dXNlcjpwYXNz"
key: http.apiKey()                    // "sk_live_abc123..."

// Webhooks
event: http.webhookEvent()            // "payment.succeeded", etc.

// Environment variables
api_url: env("API_URL")               // Read from environment
api_key: env("API_KEY", "default")    // With default value
```

### SQL Plugin

Generate SQL-related test data for database testing:

```vague
// Identifiers
table: sql.tableName()                // "users", "order_items"
column: sql.columnName()              // "created_at", "user_id"
schema: sql.schemaName()              // "public", "analytics"

// Quoted identifiers
quoted: sql.quoted("user")            // "\"user\"" (ANSI)
mysql: sql.quoted("user", "mysql")    // "`user`"

// SQL values
str: sql.string("O'Brien")            // "'O''Brien'"
date: sql.dateValue("2024-01-15")     // "DATE '2024-01-15'"
ts: sql.timestamp()                   // "TIMESTAMP '...'"
null: sql.nullValue()                 // "NULL"
bool: sql.boolean(true)               // "TRUE"

// Connection strings
conn: sql.connectionString("postgres")

// Query fragments
select: sql.select()                  // SELECT statement
where: sql.whereClause()              // WHERE clause
order: sql.orderBy()                  // ORDER BY clause
join: sql.join("left")                // JOIN clause

// Placeholders
param: sql.placeholder("postgres", 1) // "$1"
```

### GraphQL Plugin

Generate GraphQL-related test data:

```vague
// Identifiers
field: graphql.fieldName()            // "id", "createdAt"
type: graphql.typeName()              // "User", "OrderPayload"
op: graphql.operationName()           // "GetUser", "CreateOrder"
enum: graphql.enumValue()             // "ACTIVE", "PENDING"

// Operations
query: graphql.query()                // Full query string
mutation: graphql.mutation()          // Full mutation string
subscription: graphql.subscription()
fragment: graphql.fragment()

// Errors
error: graphql.error()                // Full error object
code: graphql.errorCode()             // "UNAUTHENTICATED", etc.

// Shorthand (prefixed with 'gql')
gqlQuery()
gqlMutation()
gqlTypeName()
```
