# XPath Operators and Functions

Complete reference for operators and functions available in ODK forms.

## Operators

### Math Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `${a} + ${b}` |
| `-` | Subtraction | `${a} - ${b}` |
| `*` | Multiplication | `${a} * ${b}` |
| `div` | Division | `${a} div ${b}` |
| `mod` | Modulo (remainder) | `${a} mod ${b}` |

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal | `${status} = 'active'` |
| `!=` | Not equal | `${status} != 'closed'` |
| `<` | Less than | `${age} < 18` |
| `<=` | Less than or equal | `${age} <= 5` |
| `>` | Greater than | `${score} > 80` |
| `>=` | Greater than or equal | `${age} >= 18` |

### Boolean Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Both true | `${a} > 0 and ${b} > 0` |
| `or` | Either true | `${a} = 'x' or ${a} = 'y'` |
| `not()` | Negation | `not(${excluded})` |

---

## Control Flow Functions

| Function | Description | Example |
|----------|-------------|---------|
| `if(cond, then, else)` | Conditional | `if(${age}>=18, 'adult', 'minor')` |
| `coalesce(a, b, ...)` | First non-empty | `coalesce(${phone}, 'N/A')` |
| `once(expr)` | Evaluate once | `once(random())` |

---

## String Functions

### Basic String Operations

| Function | Description | Example |
|----------|-------------|---------|
| `concat(a, b, ...)` | Join strings | `concat(${first}, ' ', ${last})` |
| `join(sep, nodeset)` | Join with separator | `join(', ', ${items})` |
| `string-length(str)` | Character count | `string-length(${name})` |
| `normalize-space(str)` | Trim whitespace | `normalize-space(${input})` |

### String Search

| Function | Description | Example |
|----------|-------------|---------|
| `contains(str, search)` | Contains substring | `contains(${notes}, 'urgent')` |
| `starts-with(str, prefix)` | Starts with | `starts-with(${id}, 'P')` |
| `ends-with(str, suffix)` | Ends with | `ends-with(${file}, '.pdf')` |

### String Extraction

| Function | Description | Example |
|----------|-------------|---------|
| `substr(str, start, end)` | Extract substring | `substr(${id}, 0, 3)` |
| `substring-before(str, delim)` | Before delimiter | `substring-before(${email}, '@')` |
| `substring-after(str, delim)` | After delimiter | `substring-after(${email}, '@')` |

### String Transformation

| Function | Description | Example |
|----------|-------------|---------|
| `translate(str, from, to)` | Replace chars | `translate(${text}, 'abc', 'ABC')` |
| `regex(str, pattern)` | Match regex | `regex(${email}, '[^@]+@.+')` |

### Type Conversion

| Function | Description | Example |
|----------|-------------|---------|
| `string(value)` | Convert to string | `string(${number})` |
| `boolean-from-string(str)` | String to boolean | `boolean-from-string('true')` |

---

## Math Functions

### Basic Math

| Function | Description | Example |
|----------|-------------|---------|
| `round(num, decimals)` | Round number | `round(${bmi}, 1)` |
| `int(num)` | Truncate to integer | `int(${age_decimal})` |
| `number(value)` | Convert to number | `number(${text_num})` |
| `abs(num)` | Absolute value | `abs(${difference})` |

### Advanced Math

| Function | Description | Example |
|----------|-------------|---------|
| `pow(base, exp)` | Power | `pow(${height}, 2)` |
| `sqrt(num)` | Square root | `sqrt(${area})` |
| `log(num)` | Natural logarithm | `log(${value})` |
| `log10(num)` | Base-10 logarithm | `log10(${value})` |
| `exp(num)` | e^num | `exp(${x})` |

### Trigonometry

| Function | Description |
|----------|-------------|
| `sin(rad)` | Sine |
| `cos(rad)` | Cosine |
| `tan(rad)` | Tangent |
| `asin(num)` | Arc sine |
| `acos(num)` | Arc cosine |
| `atan(num)` | Arc tangent |
| `atan2(y, x)` | Arc tangent of y/x |

### Constants and Random

| Function | Description | Example |
|----------|-------------|---------|
| `pi()` | Pi (3.14159...) | `${radius} * ${radius} * pi()` |
| `random()` | Random 0-1 | `int(random() * 1000)` |

---

## Date/Time Functions

### Current Date/Time

| Function | Description | Example |
|----------|-------------|---------|
| `today()` | Current date | `today()` |
| `now()` | Current datetime | `now()` |

### Date Conversion

| Function | Description | Example |
|----------|-------------|---------|
| `date(value)` | Convert to date | `date('2024-01-15')` |
| `decimal-date-time(dt)` | Days since epoch | `decimal-date-time(${timestamp})` |

### Date Formatting

| Function | Description | Example |
|----------|-------------|---------|
| `format-date(date, fmt)` | Format date | `format-date(${dob}, '%Y-%m-%d')` |
| `format-date-time(dt, fmt)` | Format datetime | `format-date-time(now(), '%Y-%m-%d %H:%M')` |

### Format Codes

| Code | Description | Example |
|------|-------------|---------|
| `%Y` | 4-digit year | 2024 |
| `%y` | 2-digit year | 24 |
| `%m` | Month (01-12) | 03 |
| `%n` | Month (1-12) | 3 |
| `%b` | Month abbreviation | Mar |
| `%d` | Day (01-31) | 05 |
| `%e` | Day (1-31) | 5 |
| `%H` | Hour 24h (00-23) | 14 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%a` | Day abbreviation | Mon |

---

## Select Functions

| Function | Description | Example |
|----------|-------------|---------|
| `selected(field, value)` | Value selected? | `selected(${symptoms}, 'fever')` |
| `selected-at(field, index)` | Selection at index | `selected-at(${choices}, 0)` |
| `count-selected(field)` | Count selections | `count-selected(${symptoms})` |
| `jr:choice-name(val, 'field')` | Get choice label | `jr:choice-name(${gender}, '${gender}')` |

---

## Repeat Functions

| Function | Description | Example |
|----------|-------------|---------|
| `count(nodeset)` | Count instances | `count(${children})` |
| `count-non-empty(nodeset)` | Count non-empty | `count-non-empty(${responses})` |
| `sum(nodeset)` | Sum values | `sum(${children}/age)` |
| `min(nodeset)` | Minimum value | `min(${scores})` |
| `max(nodeset)` | Maximum value | `max(${scores})` |
| `position(..)` | Current index | `position(..)` |
| `indexed-repeat(field, repeat, idx)` | Access instance | `indexed-repeat(${name}, ${people}, 1)` |

---

## Geographic Functions

| Function | Description | Example |
|----------|-------------|---------|
| `area(geoshape)` | Area in m² | `area(${plot_boundary})` |
| `distance(geo1, geo2)` | Distance in meters | `distance(${start}, ${end})` |

---

## Utility Functions

| Function | Description | Example |
|----------|-------------|---------|
| `uuid()` | Generate unique ID | `uuid()` |
| `boolean(value)` | Convert to boolean | `boolean(${has_data})` |
| `true()` | Boolean true | `true()` |
| `false()` | Boolean false | `false()` |
| `instance(name)` | Access external data | `instance('locations')` |
| `pulldata(file, col, key_col, key)` | Lookup from CSV | `pulldata('data', 'name', 'id', ${id})` |
| `randomize(nodeset)` | Randomize order | `randomize(${choices})` |
| `randomize(nodeset, seed)` | Seeded random | `randomize(${choices}, ${seed})` |
