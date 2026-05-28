# Power Automate Expression Reference

Quick reference for Power Automate expression syntax used in flow definitions.

## Expression Format

All expressions are wrapped in `@{...}` or use `@` prefix:

```
@{expression}           # Inline in strings
@expression             # Standalone
"@{concat('a','b')}"    # Result: "ab"
```

---

## Dynamic Content Access

### Trigger Outputs
```
@{triggerOutputs()}                              # Full trigger output
@{triggerOutputs()?['body']}                     # Body object
@{triggerOutputs()?['body/subject']}             # Nested property
@{triggerBody()}                                 # Shorthand for body
@{triggerBody()?['value']}                       # Array from trigger
```

### Action Outputs
```
@{body('Action_Name')}                           # Action body
@{body('Action_Name')?['value']}                 # Nested value
@{outputs('Action_Name')?['headers']}            # Response headers
@{outputs('Action_Name')?['statusCode']}         # HTTP status code
```

### Variables
```
@{variables('VariableName')}                     # Get variable value
```

### Loop Items
```
@{items('Apply_to_each')}                        # Current item
@{items('Apply_to_each')?['Name']}               # Item property
@{iterationIndexes('Apply_to_each')}             # Current index
```

---

## String Functions

```
@{concat('Hello ', 'World')}                     # "Hello World"
@{substring('Hello', 0, 3)}                      # "Hel"
@{replace('Hello', 'l', 'L')}                    # "HeLLo"
@{toLower('HELLO')}                              # "hello"
@{toUpper('hello')}                              # "HELLO"
@{trim('  hello  ')}                             # "hello"
@{split('a,b,c', ',')}                           # ["a","b","c"]
@{join(['a','b','c'], '-')}                      # "a-b-c"
@{length('hello')}                               # 5
@{indexOf('hello', 'l')}                         # 2
@{lastIndexOf('hello', 'l')}                     # 3
@{startsWith('hello', 'he')}                     # true
@{endsWith('hello', 'lo')}                       # true
@{contains('hello', 'ell')}                      # true
@{guid()}                                        # New GUID
@{nthIndexOf('hello', 'l', 2)}                   # 3
```

---

## Date/Time Functions

```
@{utcNow()}                                      # Current UTC timestamp
@{utcNow('yyyy-MM-dd')}                          # Formatted date
@{formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm')}  # Custom format
@{addDays(utcNow(), 7)}                          # Add days
@{addHours(utcNow(), 2)}                         # Add hours
@{addMinutes(utcNow(), 30)}                      # Add minutes
@{addSeconds(utcNow(), 60)}                      # Add seconds
@{subtractFromTime(utcNow(), 1, 'Day')}          # Subtract time
@{startOfDay(utcNow())}                          # Start of day
@{startOfMonth(utcNow())}                        # Start of month
@{dayOfWeek(utcNow())}                           # 0-6 (Sunday=0)
@{dayOfMonth(utcNow())}                          # 1-31
@{dayOfYear(utcNow())}                           # 1-366
@{ticks(utcNow())}                               # Ticks since epoch
@{convertTimeZone(utcNow(), 'UTC', 'GMT Standard Time')}
@{parseDateTime('2024-01-15')}                   # Parse string to date
```

### Date Format Specifiers
```
yyyy    # 4-digit year (2024)
MM      # 2-digit month (01-12)
dd      # 2-digit day (01-31)
HH      # 24-hour (00-23)
hh      # 12-hour (01-12)
mm      # Minutes (00-59)
ss      # Seconds (00-59)
tt      # AM/PM
```

---

## Math Functions

```
@{add(1, 2)}                                     # 3
@{sub(5, 2)}                                     # 3
@{mul(3, 4)}                                     # 12
@{div(10, 2)}                                    # 5
@{mod(7, 3)}                                     # 1
@{min(1, 2, 3)}                                  # 1
@{max(1, 2, 3)}                                  # 3
@{rand(1, 100)}                                  # Random 1-100
```

---

## Collection Functions

```
@{length(collection)}                            # Array length
@{first(collection)}                             # First item
@{last(collection)}                              # Last item
@{take(collection, 3)}                           # First 3 items
@{skip(collection, 2)}                           # Skip first 2
@{union(array1, array2)}                         # Merge arrays
@{intersection(array1, array2)}                  # Common items
@{contains(collection, item)}                    # Check membership
@{empty(collection)}                             # true if empty
@{createArray('a', 'b', 'c')}                    # Create array
@{json('[1,2,3]')}                               # Parse JSON array
@{sort(collection)}                              # Sort ascending
@{reverse(collection)}                           # Reverse order
```

---

## Logical Functions

```
@{if(condition, trueValue, falseValue)}          # Ternary
@{equals(value1, value2)}                        # Equality check
@{not(condition)}                                # Negation
@{and(cond1, cond2)}                             # Logical AND
@{or(cond1, cond2)}                              # Logical OR
@{greater(a, b)}                                 # a > b
@{greaterOrEquals(a, b)}                         # a >= b
@{less(a, b)}                                    # a < b
@{lessOrEquals(a, b)}                            # a <= b
@{coalesce(value1, value2, ...)}                 # First non-null
```

---

## Type Conversion

```
@{int('123')}                                    # Parse to integer
@{float('123.45')}                               # Parse to float
@{string(123)}                                   # Convert to string
@{bool('true')}                                  # Parse to boolean
@{json('{"a":1}')}                               # Parse JSON string
@{xml('<a>b</a>')}                               # Parse XML string
@{base64('text')}                                # Encode to base64
@{base64ToBinary(base64String)}                  # Decode base64
@{base64ToString(base64String)}                  # Decode to string
@{decodeUriComponent('%20')}                     # Decode URI
@{encodeUriComponent(' ')}                       # Encode URI
@{decodeBase64(base64String)}                    # Decode base64
@{dataUri(content)}                              # Create data URI
@{dataUriToBinary(dataUri)}                      # Data URI to binary
@{dataUriToString(dataUri)}                      # Data URI to string
```

---

## Workflow Functions

```
@{workflow().run.name}                           # Run name
@{workflow().tags.flowDisplayName}               # Flow display name
@{actions('ActionName')}                         # Action metadata
@{actions('ActionName').outputs}                 # Action outputs
@{result('ActionName')}                          # Action result
@{parameters('paramName')}                       # Parameter value
```

---

## Common Patterns

### Null-Safe Property Access
```
@{triggerBody()?['property']}                    # Returns null if missing
@{coalesce(triggerBody()?['prop'], 'default')}  # Default if null
```

### Conditional Text
```
@{if(empty(body('Action')?['value']), 'None', body('Action')?['value'])}
```

### Array Length Check
```
@{greater(length(body('GetItems')?['value']), 0)}
```

### Format Email List
```
@{join(body('GetUsers')?['value'], ';')}
```

### Extract Domain from Email
```
@{split(triggerBody()?['email'], '@')[1]}
```

### Date Comparison (Last 7 Days)
```
@{greaterOrEquals(triggerBody()?['Created'], addDays(utcNow(), -7))}
```
