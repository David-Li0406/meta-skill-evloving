# Regex Whisperer

## Patterns


---
  #### **Name**
Readable Regex
  #### **Description**
Writing regex humans can understand
  #### **When To Use**
Any regex that will be maintained
  #### **Implementation**
    ## Readable Regex Patterns
    
    ### 1. Use Verbose Mode
    
    ```javascript
    // BAD
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    // GOOD
    const emailRegex = new RegExp([
      '^',
      '[a-zA-Z0-9._%+-]+',  // Local part
      '@',
      '[a-zA-Z0-9.-]+',     // Domain
      '\\.',
      '[a-zA-Z]{2,}',       // TLD
      '$'
    ].join(''), '');
    ```
    
    ### 2. Named Capture Groups
    
    ```javascript
    // BAD
    const dateRegex = /(\d{4})-(\d{2})-(\d{2})/;
    const match = text.match(dateRegex);
    const year = match[1];  // What is [1]?
    
    // GOOD
    const dateRegex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
    const match = text.match(dateRegex);
    const year = match.groups.year;  // Clear!
    ```
    
    ### 3. Build Incrementally
    
    ```javascript
    // COMPOSABLE PATTERNS
    const digit = '\\d';
    const digits = `${digit}+`;
    const optionalSign = '[+-]?';
    const decimal = `\\.${digits}`;
    const optionalDecimal = `(${decimal})?`;
    
    const numberPattern = `${optionalSign}${digits}${optionalDecimal}`;
    ```
    
    ### 4. The Comment Pattern
    
    | Technique | Example |
    |-----------|---------|
    | Variable names | `const localPart = '[a-zA-Z0-9._%+-]+'` |
    | Inline comments | `// Matches ISO date format` |
    | Test cases as docs | `// "2024-01-15" → match` |
    

---
  #### **Name**
Common Patterns
  #### **Description**
Battle-tested patterns for common needs
  #### **When To Use**
Standard validation and extraction
  #### **Implementation**
    ## Reliable Common Patterns
    
    ### 1. Email (Pragmatic)
    
    ```javascript
    // Simple and catches most
    const email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // Note: True email validation is nearly impossible with regex
    // This catches 99% of real emails
    ```
    
    ### 2. URL
    
    ```javascript
    const url = /^https?:\/\/[^\s/$.?#].[^\s]*$/i;
    
    // For strict: use URL constructor instead
    try {
      new URL(input);
    } catch {
      // Invalid URL
    }
    ```
    
    ### 3. Phone Numbers (US)
    
    ```javascript
    // Flexible format
    const phone = /^[\d\s\-\(\)\.]+$/;
    
    // Then normalize and validate length
    const digits = phone.replace(/\D/g, '');
    if (digits.length === 10 || digits.length === 11) {
      // Valid
    }
    ```
    
    ### 4. Common Mistakes
    
    | Pattern | Problem | Better |
    |---------|---------|--------|
    | `.*` | Greedy, slow | `[^>]*` (negated class) |
    | `\d+` | No boundaries | `\b\d+\b` |
    | `^.*$` | Doesn't cross lines | Use `m` flag |
    | Escaping | Missing escapes | Test with literals |
    

---
  #### **Name**
Debugging Regex
  #### **Description**
Finding why your pattern doesn't work
  #### **When To Use**
When regex isn't matching as expected
  #### **Implementation**
    ## Regex Debugging
    
    ### 1. The Incremental Approach
    
    ```
    FULL PATTERN DOESN'T WORK?
    
    1. Start with smallest part
    2. Add one piece at a time
    3. Test after each addition
    4. Find exactly where it breaks
    ```
    
    ### 2. Debugging Tools
    
    | Tool | Use For |
    |------|---------|
    | regex101.com | Visual debugging, explanation |
    | regexr.com | Live testing with explanation |
    | debuggex.com | Visual railroad diagrams |
    | IDE inline | Quick test |
    
    ### 3. Common Failures
    
    | Symptom | Likely Cause |
    |---------|--------------|
    | No match at all | Escaping issue |
    | Matches too much | Greedy quantifier |
    | Matches too little | Missing optional |
    | Works sometimes | Anchor/boundary issue |
    | Catastrophic backtrack | Nested quantifiers |
    
    ### 4. The Test Matrix
    
    ```javascript
    const testCases = [
      // Should match
      { input: 'valid@email.com', expected: true },
      { input: 'test.user@domain.org', expected: true },
    
      // Should NOT match
      { input: 'no-at-sign.com', expected: false },
      { input: '@no-local.com', expected: false },
    
      // Edge cases
      { input: '', expected: false },
      { input: 'a@b.c', expected: true },  // Minimal valid
    ];
    ```
    

---
  #### **Name**
When Not to Regex
  #### **Description**
Recognizing when regex is the wrong tool
  #### **When To Use**
Before reaching for regex
  #### **Implementation**
    ## Alternatives to Regex
    
    ### 1. Don't Use Regex For
    
    | Task | Use Instead |
    |------|-------------|
    | HTML parsing | DOM parser |
    | JSON parsing | JSON.parse |
    | URL parsing | URL constructor |
    | CSV parsing | CSV library |
    | Nested structures | Parser library |
    | Simple contains | .includes() |
    | Simple split | .split() |
    | Simple replace | .replace(string, string) |
    
    ### 2. The HTML Warning
    
    ```
    NEVER parse HTML with regex:
    
    /<div>(.+?)<\/div>/  // BROKEN
    
    Why? HTML is not regular.
    - Tags can nest
    - Attributes can contain >
    - Comments break patterns
    - Self-closing tags vary
    
    Use: DOMParser, cheerio, etc.
    ```
    
    ### 3. String Methods First
    
    ```javascript
    // REGEX OVERKILL
    const hasPrefix = /^prefix/.test(str);
    
    // SIMPLER
    const hasPrefix = str.startsWith('prefix');
    
    // REGEX OVERKILL
    const parts = str.split(/,/);
    
    // SIMPLER
    const parts = str.split(',');
    ```
    
    ### 4. Decision Tree
    
    ```
    IS REGEX RIGHT?
    
    Fixed string? → Use string methods
    Nested structure? → Use parser
    Complex grammar? → Use parser
    Simple pattern? → Maybe regex
    Variable pattern? → Regex
    Performance critical? → Benchmark first
    ```
    

## Anti-Patterns


---
  #### **Name**
The Cryptic One-Liner
  #### **Description**
Writing incomprehensible regex
  #### **Why Bad**
    Nobody can maintain it.
    Bugs hide in complexity.
    Future you will suffer.
    
  #### **What To Do Instead**
    Break into pieces.
    Use named groups.
    Comment thoroughly.
    

---
  #### **Name**
The HTML Regex
  #### **Description**
Parsing HTML or XML with regex
  #### **Why Bad**
    Will break on edge cases.
    Nested tags impossible.
    Leads to security issues.
    
  #### **What To Do Instead**
    Use proper parser.
    DOMParser for browser.
    Cheerio for Node.
    

---
  #### **Name**
The Untested Regex
  #### **Description**
Using regex without test cases
  #### **Why Bad**
    Edge cases will bite you.
    False confidence.
    Production failures.
    
  #### **What To Do Instead**
    Test valid inputs.
    Test invalid inputs.
    Test edge cases.
    