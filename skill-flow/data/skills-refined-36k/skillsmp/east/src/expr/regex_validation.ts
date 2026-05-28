/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

interface ValidationResult {
  isValid: boolean;
  warnings: string[];
  errors: string[];
}

export function validateCrossPlatformCompatible(regex: RegExp): ValidationResult {
  const result: ValidationResult = {
    isValid: true,
    warnings: [],
    errors: []
  };

  const pattern = regex.source;
  const flags = regex.flags;

  // Check flags compatibility
  validateFlags(flags, result);
  
  // Check pattern compatibility  
  validatePattern(pattern, result);

  result.isValid = result.errors.length === 0;
  return result;
}

function validateFlags(flags: string, result: ValidationResult): void {
  // Cross-platform compatible flags (supported by both JavaScript and PCRE)
  const supportedFlags = new Set(['i', 'm', 's']);
  
  // JavaScript-specific flags that aren't part of the common PCRE subset
  const jsOnlyFlags = new Set(['g', 'y', 'u', 'd']);
  
  for (const flag of flags) {
    if (jsOnlyFlags.has(flag)) {
      result.errors.push(`Flag '${flag}' is JavaScript-specific and not in the common PCRE subset`);
    } else if (!supportedFlags.has(flag)) {
      result.warnings.push(`Flag '${flag}' may not be supported across all regex backends`);
    }
  }

  // Note: Different backends handle global matching via different APIs
  if (flags.includes('g')) {
    result.warnings.push("Global flag 'g' behavior varies between backends - use with caution");
  }
}

function validatePattern(pattern: string, result: ValidationResult): void {
  // JavaScript-specific features that aren't in the common PCRE subset
  const jsOnlyFeatures = [
    { regex: /\\k<\w+>/, message: "Named backreferences \\k<name> are JavaScript-specific extensions" },
    { regex: /\(\?\<[=!]/, message: "Lookbehind assertions have inconsistent support across regex engines" },
    { regex: /\\p\{.*?\}/, message: "Unicode property escapes \\p{...} are not consistently supported" },
    { regex: /\\u\{[0-9a-fA-F]+\}/, message: "Extended Unicode codepoint escapes \\u{...} are JavaScript-specific" },
  ];

  // PCRE-specific features that aren't supported in JavaScript
  const pcreOnlyFeatures = [
    { regex: /\(\*[A-Z_]+\)/, message: "PCRE control verbs (*SKIP, *FAIL, etc.) are not in the common subset" },
    { regex: /\\K/, message: "Keep assertion \\K is PCRE-specific and not supported in JavaScript" },
    { regex: /\(\?\+|\*\+|\+\+|\?\+/, message: "Possessive quantifiers are PCRE-specific extensions" },
    { regex: /\(\?\?\)/, message: "Branch reset groups (?|...) are PCRE-specific extensions" },
  ];

  // Check for JavaScript-specific features
  for (const feature of jsOnlyFeatures) {
    if (feature.regex.test(pattern)) {
      result.errors.push(feature.message);
    }
  }

  // Check for PCRE-specific features  
  for (const feature of pcreOnlyFeatures) {
    if (feature.regex.test(pattern)) {
      result.errors.push(feature.message);
    }
  }

  // Warn about patterns that may behave differently across backends
  const warnings = [
    { regex: /\[\[:/, message: "POSIX character classes [[:alpha:]] may behave differently across engines" },
    { regex: /\(\?\#/, message: "Inline comments (?#...) are supported but may affect performance differently" },
    { regex: /\\x\{[0-9a-fA-F]+\}/, message: "Extended hex escapes \\x{...} may not be consistently supported" },
  ];

  for (const warning of warnings) {
    if (warning.regex.test(pattern)) {
      result.warnings.push(warning.message);
    }
  }
}

// Example usage and test cases
export function runCompatibilityTests(): void {
  console.log("=== Cross-Platform RegExp Validation Tests ===\n");

  const testCases: Array<{ name: string; regex: RegExp; expectedValid: boolean }> = [
    // ✅ Safe cross-platform patterns
    { name: "Basic word pattern", regex: /\w+/, expectedValid: true },
    { name: "Email pattern", regex: /\w+@\w+\.\w+/, expectedValid: true },
    { name: "Case insensitive", regex: /hello/i, expectedValid: true },
    { name: "Multiline mode", regex: /^test$/m, expectedValid: true },
    { name: "Dotall mode", regex: /a.*b/s, expectedValid: true },
    { name: "Character class", regex: /[a-z0-9]+/i, expectedValid: true },
    { name: "Anchors", regex: /^start.*end$/, expectedValid: true },
    { name: "Groups and alternation", regex: /(cat|dog)/, expectedValid: true },
    { name: "Quantifiers", regex: /a{2,5}b*c+d?/, expectedValid: true },

    // ⚠️ Problematic patterns
    { name: "Global flag", regex: /test/g, expectedValid: false }, // Has warnings
    { name: "Unicode flag", regex: /test/u, expectedValid: false },
    { name: "Sticky flag", regex: /test/y, expectedValid: false },
    
    // ❌ JavaScript-only features  
    { name: "Named backreference", regex: /(?<name>\w+)\k<name>/, expectedValid: false },
    { name: "Unicode property", regex: /\p{Letter}/u, expectedValid: false },
  ];

  for (const testCase of testCases) {
    const result = validateCrossPlatformCompatible(testCase.regex);
    const status = result.isValid ? "✅" : "❌";
    const expected = testCase.expectedValid ? "should pass" : "should fail";
    
    console.log(`${status} ${testCase.name} (${expected})`);
    console.log(`   Pattern: ${testCase.regex}`);
    
    if (result.errors.length > 0) {
      console.log(`   Errors: ${result.errors.join(", ")}`);
    }
    if (result.warnings.length > 0) {
      console.log(`   Warnings: ${result.warnings.join(", ")}`);
    }
    console.log();
  }
}

// Recommended patterns that work well across different regex backends
export const RECOMMENDED_PATTERNS = {
  email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
  phoneUS: /^\(\d{3}\)\s?\d{3}-\d{4}$/,
  uuid: /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,
  ipv4: /^(?:(?:25[0-5]|2[0-4]\d|[01]\d\d|\d{1,2})\.){3}(?:25[0-5]|2[0-4]\d|[01]\d\d|\d{1,2})$/,
  url: /^https?:\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?$/,
  identifier: /^[a-zA-Z_][a-zA-Z0-9_]*$/,
  number: /^-?\d+(\.\d+)?([eE][+-]?\d+)?$/,
  whitespace: /\s+/,
  word: /\b\w+\b/,
  lineBreak: /\r?\n/
};

if (import.meta.url === `file://${process.argv[1]}`) {
  runCompatibilityTests();
}