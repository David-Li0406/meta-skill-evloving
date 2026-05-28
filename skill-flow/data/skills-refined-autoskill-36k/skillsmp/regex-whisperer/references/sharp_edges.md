# Regex Whisperer - Sharp Edges

## Catastrophic Backtracking

### **Id**
catastrophic-backtracking
### **Summary**
Regex causes application hang or crash
### **Severity**
high
### **Situation**
Regex takes forever or crashes on certain inputs
### **Why**
  Nested quantifiers.
  Ambiguous patterns.
  Exponential backtracking.
  
### **Solution**
  ## Preventing ReDoS
  
  ### The Problem
  
  ```javascript
  // DANGEROUS PATTERN
  const pattern = /^(a+)+$/;
  
  // This input causes exponential backtracking:
  'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaab'
  
  // Why? The engine tries every way to match a+ before failing
  ```
  
  ### Dangerous Patterns
  
  | Pattern | Problem |
  |---------|---------|
  | `(a+)+` | Nested quantifiers |
  | `(a|a)+` | Overlapping alternatives |
  | `(.*)+` | Greedy nested |
  | `(a+)*` | Optional nested |
  | `(.*?){n}` | Non-greedy nested |
  
  ### Safe Alternatives
  
  ```javascript
  // DANGEROUS
  const bad = /(.*,)*$/;
  
  // SAFE: Make inner group possessive or atomic
  // (Not all engines support this)
  
  // SAFE: Use negated class
  const good = /([^,]*,)*$/;
  
  // SAFE: Remove nesting
  const better = /[^,]*(,[^,]*)*/;
  ```
  
  ### Prevention Checklist
  
  | Check | Action |
  |-------|--------|
  | Nested quantifiers? | Flatten or use negated class |
  | Overlapping alternatives? | Make mutually exclusive |
  | Unknown input length? | Add timeout or limit |
  | User-provided input? | Sanitize or limit length |
  
  ### Runtime Protection
  
  ```javascript
  // Add timeout for user input
  function safeMatch(pattern, input, timeoutMs = 100) {
    const start = Date.now();
    // Use streaming/iterative approach
    // Or limit input length
    if (input.length > 10000) {
      throw new Error('Input too long');
    }
    return pattern.test(input);
  }
  ```
  
### **Symptoms**
  - CPU spike
  - Request timeout
  - Application hang
  - "Too long" errors
### **Detection Pattern**
slow regex|hang|timeout|backtrack

## False Validation

### **Id**
false-validation
### **Summary**
Regex validates but shouldn't
### **Severity**
high
### **Situation**
Invalid data passes regex validation
### **Why**
  Missing anchors.
  Partial matches.
  Greedy behavior.
  
### **Solution**
  ## Bulletproof Validation
  
  ### The Anchor Problem
  
  ```javascript
  // BROKEN: Matches anywhere in string
  const emailBad = /[^\s@]+@[^\s@]+/;
  'not an email abc@def.com junk'.match(emailBad);  // Matches!
  
  // FIXED: Anchored
  const emailGood = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  ```
  
  ### Common Validation Gaps
  
  | Gap | Example | Fix |
  |-----|---------|-----|
  | No start anchor | `/\d+/` matches 'a1b' | `/^\d+/` |
  | No end anchor | `/^\d+/` matches '123abc' | `/^\d+$/` |
  | Missing length | `/^\d+$/` accepts any length | `/^\d{10}$/` |
  | Missing boundaries | `/cat/` matches 'category' | `/\bcat\b/` |
  
  ### Validation Layers
  
  ```javascript
  function validateEmail(input) {
    // Layer 1: Basic regex
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input)) {
      return false;
    }
  
    // Layer 2: Length check
    if (input.length > 254) {
      return false;
    }
  
    // Layer 3: Domain check (optional)
    const domain = input.split('@')[1];
    if (domain.length > 253) {
      return false;
    }
  
    return true;
  }
  ```
  
  ### Test Both Sides
  
  ```javascript
  // MUST test that invalid inputs FAIL
  const invalidEmails = [
    '',
    'no-at-sign',
    '@no-local',
    'no-domain@',
    'has spaces@domain.com',
    'multiple@@at.com',
  ];
  
  invalidEmails.forEach(email => {
    expect(validateEmail(email)).toBe(false);
  });
  ```
  
### **Symptoms**
  - Invalid data in database
  - Security bypasses
  - But I validated it!
  - Edge case failures
### **Detection Pattern**
passed validation|shouldn't match|slipped through

## Encoding Issues

### **Id**
encoding-issues
### **Summary**
Regex fails on unicode or special characters
### **Severity**
medium
### **Situation**
Pattern works in tests but fails in production
### **Why**
  Unicode handling.
  Different character sets.
  Invisible characters.
  
### **Solution**
  ## Unicode-Safe Patterns
  
  ### The Unicode Problem
  
  ```javascript
  // BREAKS on non-ASCII
  const wordBad = /\w+/;  // Only matches [a-zA-Z0-9_]
  
  // Works on any word character
  const wordGood = /[\p{L}\p{N}_]+/u;  // Needs 'u' flag
  ```
  
  ### Flag Requirements
  
  | Flag | Purpose |
  |------|---------|
  | `u` | Unicode mode (required for \p{}) |
  | `s` | Dotall (. matches newline) |
  | `m` | Multiline (^ $ at line boundaries) |
  
  ### Common Unicode Issues
  
  | Issue | Example | Fix |
  |-------|---------|-----|
  | Accents | `café` not matching | Use `u` flag |
  | Emoji | `👍` breaking | Unicode property classes |
  | RTL text | Arabic/Hebrew | Use `u` flag |
  | Zero-width | Invisible chars | Explicit match |
  
  ### Safe Character Classes
  
  ```javascript
  // Letters (any language)
  const letter = /\p{L}/u;
  
  // Numbers (any script)
  const number = /\p{N}/u;
  
  // Whitespace (all types)
  const space = /\p{Z}/u;
  
  // Word characters (unicode-aware)
  const word = /[\p{L}\p{N}_]/u;
  ```
  
  ### Testing Unicode
  
  ```javascript
  const testStrings = [
    'hello',           // ASCII
    'café',            // Accented
    '日本語',          // Japanese
    'مرحبا',           // Arabic
    '🎉 party',        // Emoji
    'hello\u200Bworld' // Zero-width space
  ];
  ```
  
### **Symptoms**
  - Works in tests, fails production
  - International names failing
  - "Weird" characters breaking
  - Empty matches
### **Detection Pattern**
unicode|special character|doesn't match|encoding

## Maintenance Nightmare

### **Id**
maintenance-nightmare
### **Summary**
Nobody can understand or modify the regex
### **Severity**
medium
### **Situation**
Regex is correct but unmaintainable
### **Why**
  Too complex.
  No comments.
  No tests.
  
### **Solution**
  ## Maintainable Regex
  
  ### The Readability Debt
  
  ```javascript
  // UNMAINTAINABLE
  const pattern = /^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$/;
  
  // What does this match?
  // How do I modify it?
  // What edge cases exist?
  ```
  
  ### Refactoring Steps
  
  ```javascript
  // STEP 1: Break into pieces
  const countryCode = '(?:(?:\\+|00)33[\\s.-]{0,3}(?:\\(0\\)[\\s.-]{0,3})?|0)';
  const startDigit = '[1-9]';
  const restDigits = '(?:(?:[\\s.-]?\\d{2}){4}|\\d{2}(?:[\\s.-]?\\d{3}){2})';
  
  // STEP 2: Add comments
  // French phone number pattern:
  // - Starts with +33, 0033, or 0
  // - Followed by 9 digits
  // - Digits can be grouped with spaces, dots, or dashes
  
  // STEP 3: Compose with explanation
  const frenchPhone = new RegExp(
    '^' +
    countryCode +     // Country code or leading 0
    startDigit +      // First digit (1-9)
    restDigits +      // Remaining 8 digits
    '$'
  );
  ```
  
  ### Documentation Template
  
  ```javascript
  /**
   * Pattern: French Phone Number
   *
   * Matches:
   *   +33 1 23 45 67 89
   *   0033123456789
   *   01.23.45.67.89
   *
   * Rejects:
   *   0023456789 (too short)
   *   +34... (wrong country)
   *
   * Limitations:
   *   - Doesn't validate area codes
   *   - Allows any separator combination
   */
  ```
  
  ### The Simplification Check
  
  | If pattern is... | Consider |
  |------------------|----------|
  | > 50 chars | Breaking into parts |
  | > 3 groups | Named groups |
  | Has nested quantifiers | Refactoring |
  | No one understands | Rewriting simply |
  
### **Symptoms**
  - Fear of touching it
  - Don't know what it does
  - Copy-pasted from Stack Overflow
  - No tests
### **Detection Pattern**
what does this|don't understand|who wrote|scary regex