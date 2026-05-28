# Common Edge Case Checklist

When analysing a module, consider these common scenarios:

## For Functions Taking Numbers

- [ ] Zero (various representations: 0, 0.0, -0)
- [ ] Zero in context (false/missing, timers at zero, counters at zero, display with 0 items, contextual data mapping to 0)
- [ ] Numbers close to zero (0.0001, -0.0001)
- [ ] Negative numbers
- [ ] Very large numbers (approaching max values)
- [ ] Very small numbers (close to zero, min values)
- [ ] Special floating point values (if applicable: NaN, Infinity)
- [ ] Non-integer values where integers expected
- [ ] Numbers with lots of decimals vs numbers with no decimals
- [ ] Scientific notation (1E-16, 1E+10)
- [ ] Formatted numbers with separators: 1,000,000 or 1.000.000 (locale-dependent)
- [ ] 32-bit boundaries: -2147483648, 2147483647, 4294967295
- [ ] Powers of 2: 128, 256, 512, 1024, 2048

## For Size/Length Boundaries

- [ ] Common system limits: 127/128 bytes (ASCII boundary), 255/256 bytes (single-byte limit)
- [ ] Buffer boundaries: 32KB - 1, 32KB, 32KB + 1
- [ ] Buffer boundaries: 64KB - 1, 64KB, 64KB + 1
- [ ] Test at boundary-1, boundary, boundary+1 for relevant limits
- [ ] Test with and without whitespace to distinguish byte vs character limits

## For Currency/Financial Numbers

- [ ] Varying decimal places: 0 decimals (JPY), 2 decimals (USD), 3 decimals (KWD)
- [ ] Locale-specific formatting: 1,234.56 (US) vs 1 234,56 (France)
- [ ] Input variations: 5000, $5,000, $5 000, $5,000.00
- [ ] Rounding rules (banker's rounding, country-specific)
- [ ] Rounding accumulation errors
- [ ] Negative amounts (returns, refunds)

## For Date/Time Values

- [ ] Leap seconds (86,401 second days, e.g., 31 Dec 2016)
- [ ] Leap years: Feb 29, century boundaries (1900, 2000, 2100)
- [ ] Invalid dates: Feb 30/31, Apr 31, Sept 31, Nov 31
- [ ] Feb 29 in non-leap years (1900, 2001, 2100)
- [ ] Day 0, day 32, month 0, month 13
- [ ] DST transitions: duplicate times (fall back), missing times (spring forward)
- [ ] DST regional differences
- [ ] Time zone conversions
- [ ] 32-bit limits: before 1970-01-01, after 2038-02-07
- [ ] Invalid times masking as 1970-01-01 or 1969-12-31
- [ ] Calendar arithmetic: adding months/years across boundaries
- [ ] Duration arithmetic: 1 day vs 24 hours (DST effects)
- [ ] Date format parsing: multiple formats, locale differences (mm/dd vs dd/mm)
- [ ] Ambiguous formats: 01/02/2003 (Jan 2 or Feb 1?)
- [ ] Time formats: 12h am/pm vs 24h
- [ ] Ambiguous times: 12:00 (noon or midnight?)
- [ ] Timeouts: operation, network, response timeouts
- [ ] Time synchronisation: clock differences between machines
- [ ] Clock drift and skew
- [ ] Dates and times expressed without timezone information used in calculations of duration

## For Functions Taking Strings

- [ ] Empty string
- [ ] Single character
- [ ] Very long strings (10000+ chars)
- [ ] Strings with whitespace characters (newlines, tabs, spaces)
- [ ] Whitespace-only strings (only spaces, only tabs, only newlines)
- [ ] Mixed whitespace (tabs and spaces, newlines and spaces)
- [ ] Strings with long leading or trailing spaces
- [ ] Null/nil values vs empty string (based on language)

## For Functions Taking Names (person names, usernames)

- [ ] Single character names
- [ ] Very long names (35+ characters, up to 64 per ICAO)
- [ ] Extremely long names (Wolfeschlegelsteinhausenbergerdorff, 58+ char Welsh names)
- [ ] Names with punctuation (apostrophes, hyphens, periods)
- [ ] Names with accents/diacritics
- [ ] Non-Latin scripts (if internationalisation supported)
- [ ] Mononymic names (single name: "Teller", "They")
- [ ] System markers: FNU, LNU, XXX (and people actually named these)
- [ ] Reserved words: "Null", "Test", "Sample", "None", "Undefined"
- [ ] Common words as names: "Yellow Horse", "Znoneofthe"
- [ ] Multiple middle names (3+, test splitting/truncation)
- [ ] Fictional/brand names: "Superman Wheaton", "Facebook Jamal"
- [ ] Name changes (test update workflows)

## For Functions Taking Email Addresses

- [ ] Valid formats: subdomain, plus addressing, IP addresses
- [ ] Valid formats: dots and special characters in the first part
- [ ] Invalid formats: leading and trailing dots, multiple dots in a sequence
- [ ] Internationalised domains (if supported)
- [ ] Invalid formats: missing components, multiple @, dots in wrong places

## For Functions Taking URLs

- [ ] With/without protocols
- [ ] With ports and paths
- [ ] Internationalised domains
- [ ] Invalid: malformed, incomplete, with spaces

## For Functions Taking Geographic Data

- [ ] Single-letter city names (Y in France, A in Norway)
- [ ] Very long place names (58+ characters: Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch)
- [ ] Special characters (Scandinavian: AEroskoebing, Malmoe)
- [ ] Various postal code formats: 3-digit (Faroe), 4-digit (Austria), 5-digit (USA), 6 alphanumeric (UK/Canada), 10-digit (Iran)
- [ ] Postal codes optional (Fiji, UAE don't use)
- [ ] Postal code format changes (Singapore: 2-4-6 digits, Ireland added 2014)
- [ ] Regional postal code differences (China yes, Hong Kong no)
- [ ] Legacy data with old postal code formats

## For User Input with Security Implications

- [ ] SQL injection patterns
- [ ] XSS/script injection attempts
- [ ] HTML injection and malformed markup
- [ ] Path traversal attempts

## For File Paths and File System Operations

- [ ] Very long paths (>255 chars, test OS limits: 260 Windows, 4096 Linux/Mac)
- [ ] Long filenames (>255 chars)
- [ ] Special characters in filenames: * ? / \ | < > spaces, dots, etc.
- [ ] Unicode characters in filenames
- [ ] Leading/trailing spaces or dots
- [ ] Reserved filenames (CON, PRN, AUX, NUL on Windows)
- [ ] Current/parent directories (. and ..)
- [ ] Hidden files (.filename on Unix/Mac)
- [ ] File does not exist (test read/update/delete)
- [ ] File already exists (test create/copy)
- [ ] Directory when file expected (and vice versa)
- [ ] No disk space
- [ ] Minimal disk space (less than needed, just enough, slightly more)
- [ ] Read-only file system
- [ ] Write-protected files
- [ ] Locked files (by another process)
- [ ] Unavailable files (network drive disconnected)
- [ ] Remote files (network latency, timeouts)
- [ ] Corrupted files (invalid headers, truncated)
- [ ] Empty files (0 bytes)
- [ ] Symlinks and hard links
- [ ] Path separator variations (/, \, mixed, multiple //, trailing)

## For Internationalised Text

- [ ] Multiple character sets (Latin, Cyrillic, Arabic, Chinese, etc.)
- [ ] Right-to-left text (Hebrew U+05D0-U+05FF, Arabic U+0600-U+06FF)
- [ ] Homograph attacks: Cyrillic 'a' (U+0430) vs Latin 'a' (U+0061)
- [ ] Mixed scripts in single string (e.g., "paypal" mixing Cyrillic and Latin)
- [ ] Multiple representations: "cafe" precomposed (U+00E9) vs combining (U+0065+U+0301)
- [ ] Case transformation edge cases (eszett to SS, Turkish I/i, Greek Sigma variants)
- [ ] Combining characters and diacritics (U+0300-U+036F range)
- [ ] Zero-width characters (U+200B-U+200D, U+FEFF)
- [ ] Directional overrides (U+202D LTR, U+202E RTL)
- [ ] Emoji with modifiers (skin tones U+1F3FB-U+1F3FF, ZWJ sequences)
- [ ] Regional indicators (flag emoji): two characters, string length varies by encoding

## For Functions Taking Collections (Arrays/Lists)

- [ ] Empty collection
- [ ] Single element
- [ ] Many elements (100+)
- [ ] Duplicate elements (same value appears multiple times)
- [ ] Nested collections
- [ ] Collection with null/nil elements (if language allows)

## For Functions Taking Objects/Structures/Maps

- [ ] Empty object/structure
- [ ] Object with extra properties/fields
- [ ] Object with missing properties/fields
- [ ] Deeply nested objects
- [ ] Null/nil values vs empty objects (based on language)

## For Stateful Operations

- [ ] Operation before initialisation
- [ ] Multiple consecutive operations
- [ ] Operation after reset/clear
- [ ] Concurrent operations (if applicable)
- [ ] Repeating same action multiple times (where previously always executed once)
- [ ] Executing sequential actions in reverse order
- [ ] Executing sequential actions out of order/different order
- [ ] Executing one action multiple times within a sequence

## For Error Conditions

- [ ] Invalid type (string instead of number)
- [ ] Out of range values
- [ ] Missing required parameters
- [ ] Malformed data structures
- [ ] Invalid property values with specific error messages
- [ ] Error context preservation (line numbers, file names, contextual info)
- [ ] Error propagation through call chains
- [ ] Multiple errors in sequence
- [ ] Errors don't crash or prevent subsequent operations

## For Complex Interactions

- [ ] Multiple features used together
- [ ] State changes across multiple operations
- [ ] Three-way interactions between different features
- [ ] Property/option precedence and override behaviour
- [ ] Deep nesting of operations
- [ ] Property conflicts and precedence rules

## For Multiple/Related Parameters

- [ ] Same values for different parameters (e.g., same length strings, identical arrays, completely same values)
- [ ] Very close values (string one character shorter, numbers differing by 0.00001)
- [ ] Parameters with interdependencies

## For Documentation/Requirements

- [ ] Edge cases mentioned in documentation but not tested
- [ ] Requirements listed but not covered by tests
- [ ] Behaviour specified in design docs but missing tests

## For Violated Domain Constraints (Implicit Assumptions)

- [ ] Duplicate values where uniqueness assumed (IDs, usernames, keys)
- [ ] Null/empty/missing where mandatory assumed
- [ ] Empty collections where non-empty assumed
- [ ] Multiple items in 1:1 relationship
- [ ] Missing parent/child in relationship
- [ ] Orphaned records (missing foreign key targets)
- [ ] Circular references
- [ ] Wrong order where specific order assumed
- [ ] Unordered data where stable sort assumed
- [ ] Values outside implicit range (age 200, negative prices)
- [ ] Wrong scale/unit/precision
- [ ] Operations in wrong state
- [ ] Invalid state transitions
- [ ] Multiple simultaneous states
- [ ] Wrong format/encoding
- [ ] End before start (dates, ranges)
- [ ] Creation after modification (temporal violations)
- [ ] Future timestamps for past events
- [ ] Expired dates for active items
