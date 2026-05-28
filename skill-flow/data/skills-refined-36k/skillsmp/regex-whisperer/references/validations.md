# Regex Whisperer - Validations

## Potential ReDoS Pattern

### **Id**
nested-quantifiers
### **Severity**
high
### **Type**
pattern
### **Check**
Regex should not have nested quantifiers
### **Pattern**
\([^)]*[+*][^)]*\)[+*]
### **Message**
Pattern has nested quantifiers - potential ReDoS.
### **Fix Action**
Flatten pattern or use negated character classes

## Validation Without Anchors

### **Id**
missing-anchors
### **Severity**
medium
### **Type**
conceptual
### **Check**
Validation patterns should be anchored
### **Indicators**
  - Validation regex without ^ and $
  - Partial match allowed
### **Message**
Validation pattern may not be properly anchored.
### **Fix Action**
Add ^ and $ anchors for full string validation

## Untested Regex

### **Id**
no-tests
### **Severity**
medium
### **Type**
conceptual
### **Check**
Complex regex should have test cases
### **Indicators**
  - No test file
  - No test cases
  - Complex pattern without tests
### **Message**
Regex has no test coverage.
### **Fix Action**
Add test cases for valid, invalid, and edge cases

## Complex Regex Without Comments

### **Id**
uncommented-complex
### **Severity**
medium
### **Type**
conceptual
### **Check**
Complex patterns should be documented
### **Indicators**
  - Long pattern without comments
  - Multiple groups unnamed
  - No explanation
### **Message**
Complex regex is not documented.
### **Fix Action**
Add comments, use named groups, or break into parts

## HTML Parsing With Regex

### **Id**
html-parsing
### **Severity**
high
### **Type**
conceptual
### **Check**
HTML should not be parsed with regex
### **Indicators**
  - Pattern matching HTML tags
  - <.*>
  - Extracting from HTML
### **Message**
Attempting to parse HTML with regex.
### **Fix Action**
Use proper HTML parser (DOMParser, cheerio)

## May Fail on Unicode

### **Id**
missing-unicode
### **Severity**
low
### **Type**
conceptual
### **Check**
Patterns handling text should consider unicode
### **Indicators**
  - \w without u flag
  - International text expected
  - User input
### **Message**
Pattern may fail on unicode characters.
### **Fix Action**
Add 'u' flag and use \p{L} for unicode letters