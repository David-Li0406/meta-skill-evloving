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
