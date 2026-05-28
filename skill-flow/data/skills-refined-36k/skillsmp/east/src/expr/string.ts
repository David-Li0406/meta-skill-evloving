/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { ArrayType, BlobType, BooleanType, IntegerType, isDataType, StringType, type EastType } from "../types.js";
import { valueOrExprToAstTyped } from "./ast.js";
import type { BooleanExpr } from "./boolean.js";
import type { IntegerExpr } from "./integer.js";
import { equal, notEqual, less, lessEqual, greater, greaterEqual } from "./block.js";
import type { ArrayExpr } from "./array.js";
import { AstSymbol, Expr, FactorySymbol, type ToExpr } from "./expr.js";
import type { ExprType } from "./types.js";
import { validateCrossPlatformCompatible } from "./regex_validation.js";

/**
 * Expression representing string values and operations.
 *
 * StringExpr provides methods for string manipulation, parsing, searching (including regex),
 * splitting, formatting, and encoding. Strings are immutable Unicode text values.
 *
 * @example
 * ```ts
 * // String manipulation
 * const formatName = East.function([StringType, StringType], StringType, ($, first, last) => {
 *   const full = first.concat(" ").concat(last);
 *   $.return(full.upperCase());
 * });
 *
 * // String parsing and validation
 * const extractNumber = East.function([StringType], StringType, ($, text) => {
 *   const trimmed = text.trim();
 *   $.if(trimmed.contains(/^\d+$/), $ => $.return(trimmed));
 *   $.return("0");
 * });
 *
 * // String splitting and joining
 * const processCsv = East.function([StringType], ArrayType(StringType), ($, csv) => {
 *   $.return(csv.split(","));
 * });
 * ```
 */
export class StringExpr extends Expr<StringType> {
  constructor(ast: AST, createExpr: ToExpr) {
    super(StringType, ast, createExpr);
  }

  /**
   * Parses a value of the given type from the string using East's canonical text format.
   *
   * @param type - The East type to parse the string as
   * @returns An expression of the specified type
   *
   * @remarks The string must be formatted as produced by `East.print()`. For example, strings must be
   *          double-quoted, arrays use `[...]`, structs use `(...)`. This is NOT JSON parsing.
   *
   * @throws East runtime error if the string is not a valid representation of the type
   *
   * @example
   * ```ts
   * const parseInteger = East.function([StringType], IntegerType, ($, text) => {
   *   $.return(text.parse(IntegerType));
   * });
   * const compiled = East.compile(parseInteger.toIR(), []);
   * compiled("42");       // 42n
   * compiled("-100");     // -100n
   * // compiled("3.14") would throw error (not an integer format)
   * ```
   */
  parse<T>(type: T): ExprType<T> {
    if (!isDataType(type as any)) {
      throw new Error(`parse expected a DataType, but got: ${type}`);
    }
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: type as any,
      location: get_location(),
      builtin: "Parse",
      type_parameters: [type as any],
      arguments: [this[AstSymbol]],
    }) as ExprType<T>;
  }

  /**
   * Parses a value of the given type from JSON using East's canonical JSON format.
   *
   * @param type - The East type to parse the JSON as
   * @returns An expression of the specified type
   *
   * @throws East runtime error if the JSON is invalid or doesn't match the type
   *
   * @example
   * ```ts
   * const parseJsonArray = East.function([StringType], ArrayType(IntegerType), ($, json) => {
   *   $.return(json.parseJson(ArrayType(IntegerType)));
   * });
   * const compiled = East.compile(parseJsonArray.toIR(), []);
   * compiled("[1, 2, 3]");        // [1n, 2n, 3n]
   * compiled("[]");               // []
   * // compiled("{\"a\": 1}") would throw error (not an array)
   * ```
   */
  parseJson<T extends EastType>(type: T): ExprType<T> {
    return Expr.fromAst({
      ast_type: "Builtin",
      type: type,
      builtin: "StringParseJSON",
      location: [{ filename: "stdlib", line: 1, column: 1 }],
      type_parameters: [type],
      arguments: [this[AstSymbol]],
    });
  }

  /**
   * Concatenates two strings together (str + other).
   *
   * @param string - The string to append
   * @returns A StringExpr representing the concatenated result
   *
   * @example
   * ```ts
   * const joinStrings = East.function([StringType, StringType], StringType, ($, a, b) => {
   *   $.return(a.concat(b));
   * });
   * const compiled = East.compile(joinStrings.toIR(), []);
   * compiled("Hello, ", "World!");  // "Hello, World!"
   * compiled("foo", "bar");         // "foobar"
   * compiled("", "test");           // "test"
   * ```
   */
  concat(string: Expr<StringType> | string): StringExpr {
    const stringAst = valueOrExprToAstTyped(string, StringType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "StringConcat",
      type_parameters: [],
      arguments: [this[AstSymbol], stringAst],
    }) as StringExpr;
  }

  /**
   * Repeats the string a specified number of times.
   *
   * @param count - The number of times to repeat the string
   * @returns A StringExpr representing the repeated string
   *
   * @example
   * ```ts
   * const repeatString = East.function([StringType, IntegerType], StringType, ($, str, n) => {
   *   $.return(str.repeat(n));
   * });
   * const compiled = East.compile(repeatString.toIR(), []);
   * compiled("abc", 3n);   // "abcabcabc"
   * compiled("x", 5n);     // "xxxxx"
   * compiled("test", 0n);  // ""
   * compiled("hi", 1n);    // "hi"
   * ```
   */
  repeat(count: bigint | Expr<IntegerType>): StringExpr {
    const countAst = valueOrExprToAstTyped(count, IntegerType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "StringRepeat",
      type_parameters: [],
      arguments: [this[AstSymbol], countAst],
    }) as StringExpr;
  }

  /**
   * Returns the length of the string in Unicode code points.
   *
   * @returns An IntegerExpr representing the string length
   *
   * @example
   * ```ts
   * const getLength = East.function([StringType], IntegerType, ($, str) => {
   *   $.return(str.length());
   * });
   * const compiled = East.compile(getLength.toIR(), []);
   * compiled("hello");     // 5n
   * compiled("");          // 0n
   * compiled("😀🎉");      // 2n (2 emoji code points)
   * ```
   */
  length(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "StringLength",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Extracts a substring from the string between two indices.
   *
   * @param from - The starting index (inclusive)
   * @param to - The ending index (exclusive)
   * @returns A StringExpr containing the substring
   *
   * @remarks Indices are zero-based. Negative indices not supported.
   *
   * @example
   * ```ts
   * const substr = East.function([StringType, IntegerType, IntegerType], StringType, ($, str, start, end) => {
   *   $.return(str.substring(start, end));
   * });
   * const compiled = East.compile(substr.toIR(), []);
   * compiled("hello world", 0n, 5n);    // "hello"
   * compiled("hello world", 6n, 11n);   // "world"
   * compiled("test", 1n, 3n);           // "es"
   * ```
   */
  substring(from: bigint | Expr<IntegerType>, to: bigint | Expr<IntegerType>): StringExpr {
    const fromAst = valueOrExprToAstTyped(from, IntegerType);
    const toAst = valueOrExprToAstTyped(to, IntegerType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "StringSubstring",
      type_parameters: [],
      arguments: [this[AstSymbol], fromAst, toAst],
    }) as StringExpr;
  }

  /**
   * Converts the string to uppercase.
   *
   * @returns A StringExpr with all characters converted to uppercase
   *
   * @example
   * ```ts
   * const toUpper = East.function([StringType], StringType, ($, str) => {
   *   $.return(str.upperCase());
   * });
   * const compiled = East.compile(toUpper.toIR(), []);
   * compiled("hello");         // "HELLO"
   * compiled("Hello World");   // "HELLO WORLD"
   * compiled("test123");       // "TEST123"
   * ```
   */
  upperCase(): StringExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "StringUpperCase",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as StringExpr;
  }

  /**
   * Converts the string to lowercase.
   *
   * @returns A StringExpr with all characters converted to lowercase
   *
   * @example
   * ```ts
   * const toLower = East.function([StringType], StringType, ($, str) => {
   *   $.return(str.lowerCase());
   * });
   * const compiled = East.compile(toLower.toIR(), []);
   * compiled("HELLO");         // "hello"
   * compiled("Hello World");   // "hello world"
   * compiled("TEST123");       // "test123"
   * ```
   */
  lowerCase(): StringExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "StringLowerCase",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as StringExpr;
  }

  /**
   * Splits the string into an array of substrings using a delimiter.
   *
   * @param delimiter - The string to split on
   * @returns An ArrayExpr of StringType containing the split parts
   *
   * @example
   * ```ts
   * const splitString = East.function([StringType, StringType], ArrayType(StringType), ($, str, delim) => {
   *   $.return(str.split(delim));
   * });
   * const compiled = East.compile(splitString.toIR(), []);
   * compiled("a,b,c", ",");           // ["a", "b", "c"]
   * compiled("hello world", " ");     // ["hello", "world"]
   * compiled("one", ",");             // ["one"]
   * compiled("a,,b", ",");            // ["a", "", "b"]
   * ```
   */
  split(delimiter: Expr<StringType> | string): ArrayExpr<StringType> {
    const delimiterAst = valueOrExprToAstTyped(delimiter, StringType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: ArrayType(StringType),
      location: get_location(),
      builtin: "StringSplit",
      type_parameters: [],
      arguments: [this[AstSymbol], delimiterAst],
    }) as ArrayExpr<StringType>;
  }

  /**
   * Removes whitespace from both the beginning and end of the string.
   *
   * @returns A StringExpr with whitespace trimmed
   *
   * @example
   * ```ts
   * const trimString = East.function([StringType], StringType, ($, str) => {
   *   $.return(str.trim());
   * });
   * const compiled = East.compile(trimString.toIR(), []);
   * compiled("  hello  ");      // "hello"
   * compiled("test\n");         // "test"
   * compiled("  ");             // ""
   * compiled("no-space");       // "no-space"
   * ```
   */
  trim(): StringExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "StringTrim",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as StringExpr;
  }

  /**
   * Removes whitespace from the beginning of the string.
   *
   * @returns A StringExpr with leading whitespace removed
   *
   * @example
   * ```ts
   * const trimLeft = East.function([StringType], StringType, ($, str) => {
   *   $.return(str.trimStart());
   * });
   * const compiled = East.compile(trimLeft.toIR(), []);
   * compiled("  hello");        // "hello"
   * compiled("\ttest");         // "test"
   * compiled("  hello  ");      // "hello  "
   * ```
   */
  trimStart(): StringExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "StringTrimStart",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as StringExpr;
  }

  /**
   * Removes whitespace from the end of the string.
   *
   * @returns A StringExpr with trailing whitespace removed
   *
   * @example
   * ```ts
   * const trimRight = East.function([StringType], StringType, ($, str) => {
   *   $.return(str.trimEnd());
   * });
   * const compiled = East.compile(trimRight.toIR(), []);
   * compiled("hello  ");        // "hello"
   * compiled("test\n");         // "test"
   * compiled("  hello  ");      // "  hello"
   * ```
   */
  trimEnd(): StringExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "StringTrimEnd",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as StringExpr;
  }

  /**
   * Tests if the string starts with a specified prefix.
   *
   * @param prefix - The prefix to test for
   * @returns A BooleanExpr that is true if the string starts with the prefix
   *
   * @example
   * ```ts
   * const checkPrefix = East.function([StringType, StringType], BooleanType, ($, str, prefix) => {
   *   $.return(str.startsWith(prefix));
   * });
   * const compiled = East.compile(checkPrefix.toIR(), []);
   * compiled("hello world", "hello");   // true
   * compiled("test", "te");             // true
   * compiled("hello", "world");         // false
   * compiled("", "");                   // true
   * ```
   */
  startsWith(prefix: Expr<StringType> | string): BooleanExpr {
    const prefixAst = valueOrExprToAstTyped(prefix, StringType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "StringStartsWith",
      type_parameters: [],
      arguments: [this[AstSymbol], prefixAst],
    }) as BooleanExpr;
  }

  /**
   * Tests if the string ends with a specified suffix.
   *
   * @param suffix - The suffix to test for
   * @returns A BooleanExpr that is true if the string ends with the suffix
   *
   * @example
   * ```ts
   * const checkSuffix = East.function([StringType, StringType], BooleanType, ($, str, suffix) => {
   *   $.return(str.endsWith(suffix));
   * });
   * const compiled = East.compile(checkSuffix.toIR(), []);
   * compiled("hello world", "world");   // true
   * compiled("test", "st");             // true
   * compiled("hello", "world");         // false
   * compiled("", "");                   // true
   * ```
   */
  endsWith(suffix: Expr<StringType> | string): BooleanExpr {
    const suffixAst = valueOrExprToAstTyped(suffix, StringType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "StringEndsWith",
      type_parameters: [],
      arguments: [this[AstSymbol], suffixAst],
    }) as BooleanExpr;
  }

  /**
   * Tests if the string contains a substring or matches a regular expression.
   *
   * @param substringOrRegex - The substring or RegExp pattern to search for
   * @returns A BooleanExpr that is true if the string contains the substring or matches the regex
   *
   * @example
   * ```ts
   * const hasSubstring = East.function([StringType, StringType], BooleanType, ($, str, substr) => {
   *   $.return(str.contains(substr));
   * });
   * const compiled = East.compile(hasSubstring.toIR(), []);
   * compiled("hello world", "world");   // true
   * compiled("test", "xyz");            // false
   *
   * // With regex
   * const hasDigits = East.function([StringType], BooleanType, ($, str) => {
   *   $.return(str.contains(/\d+/));
   * });
   * compiled = East.compile(hasDigits.toIR(), []);
   * compiled("test123");                // true
   * compiled("test");                   // false
   * ```
   */
  contains(substringOrRegex: Expr<StringType> | string | RegExp): BooleanExpr {
    if (substringOrRegex instanceof RegExp) {
      const regexObj = substringOrRegex as RegExp;
      const validation = validateCrossPlatformCompatible(regexObj);
      
      if (!validation.isValid) {
        console.warn(`RegExp pattern may not be portable across backends: ${regexObj.source}`);
        for (const error of validation.errors) {
          console.warn(`  Error: ${error}`);
        }
      }
      
      if (validation.warnings.length > 0) {
        console.warn(`RegExp pattern has portability warnings: ${regexObj.source}`);
        for (const warning of validation.warnings) {
          console.warn(`  Warning: ${warning}`);
        }
      }

      const patternAst = valueOrExprToAstTyped(regexObj.source, StringType);
      const flagsAst = valueOrExprToAstTyped(regexObj.flags, StringType);
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: BooleanType,
        location: get_location(),
        builtin: "RegexContains",
        type_parameters: [],
        arguments: [this[AstSymbol], patternAst, flagsAst],
      }) as BooleanExpr;
    } else {
      const substringAst = valueOrExprToAstTyped(substringOrRegex as string | StringExpr, StringType);
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: BooleanType,
        location: get_location(),
        builtin: "StringContains",
        type_parameters: [],
        arguments: [this[AstSymbol], substringAst],
      }) as BooleanExpr;
    }
  }

  /**
   * Finds the index of the first occurrence of a substring or regex match.
   *
   * @param substringOrRegex - The substring or RegExp pattern to search for
   * @returns An IntegerExpr representing the zero-based index, or -1 if not found
   *
   * @example
   * ```ts
   * const findIndex = East.function([StringType, StringType], IntegerType, ($, str, substr) => {
   *   $.return(str.indexOf(substr));
   * });
   * const compiled = East.compile(findIndex.toIR(), []);
   * compiled("hello world", "world");   // 6n
   * compiled("test", "t");              // 0n
   * compiled("hello", "xyz");           // -1n
   *
   * // With regex
   * const findDigit = East.function([StringType], IntegerType, ($, str) => {
   *   $.return(str.indexOf(/\d/));
   * });
   * compiled = East.compile(findDigit.toIR(), []);
   * compiled("abc123");                 // 3n
   * ```
   */
  indexOf(substringOrRegex: Expr<StringType> | string | RegExp): IntegerExpr {
    if (substringOrRegex instanceof RegExp) {
      const regexObj = substringOrRegex as RegExp;
      const validation = validateCrossPlatformCompatible(regexObj);
      
      if (!validation.isValid) {
        console.warn(`RegExp pattern may not be portable across backends: ${regexObj.source}`);
        for (const error of validation.errors) {
          console.warn(`  Error: ${error}`);
        }
      }
      
      if (validation.warnings.length > 0) {
        console.warn(`RegExp pattern has portability warnings: ${regexObj.source}`);
        for (const warning of validation.warnings) {
          console.warn(`  Warning: ${warning}`);
        }
      }

      const patternAst = valueOrExprToAstTyped(regexObj.source, StringType);
      const flagsAst = valueOrExprToAstTyped(regexObj.flags, StringType);
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "RegexIndexOf",
        type_parameters: [],
        arguments: [this[AstSymbol], patternAst, flagsAst],
      }) as IntegerExpr;
    } else {
      const substringAst = valueOrExprToAstTyped(substringOrRegex, StringType);
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "StringIndexOf",
        type_parameters: [],
        arguments: [this[AstSymbol], substringAst],
      }) as IntegerExpr;
    }
  }

  /**
   * Replaces all occurrences of a substring or regex pattern with a replacement string.
   *
   * @param searchValue - The substring or RegExp pattern to search for
   * @param replaceValue - The replacement string (can include regex capture groups like $1, $2)
   * @returns A StringExpr with all occurrences replaced
   *
   * @example
   * ```ts
   * const replaceAll = East.function([StringType, StringType, StringType], StringType, ($, str, search, replace) => {
   *   $.return(str.replace(search, replace));
   * });
   * const compiled = East.compile(replaceAll.toIR(), []);
   * compiled("hello hello", "hello", "hi");         // "hi hi"
   * compiled("test_test_value", "test", "prod");    // "prod_prod_value"
   *
   * // With regex and capture groups
   * const swapWords = East.function([StringType], StringType, ($, str) => {
   *   $.return(str.replace(/(\w+) (\w+)/, "$2 $1"));
   * });
   * compiled = East.compile(swapWords.toIR(), []);
   * compiled("hello world");                        // "world hello"
   * ```
   */
  replace(searchValue: Expr<StringType> | string | RegExp, replaceValue: Expr<StringType> | string): StringExpr {
    if (searchValue instanceof RegExp) {
      const regexObj = searchValue as RegExp;

      // Strip 'g' flag before validation since we handle replaceAll semantics in the backend
      const flagsWithoutG = regexObj.flags.replace(/g/g, '');
      const regexForValidation = new RegExp(regexObj.source, flagsWithoutG);
      const validation = validateCrossPlatformCompatible(regexForValidation);

      if (!validation.isValid) {
        console.warn(`RegExp pattern may not be portable across backends: ${regexObj.source}`);
        for (const error of validation.errors) {
          console.warn(`  Error: ${error}`);
        }
      }

      if (validation.warnings.length > 0) {
        console.warn(`RegExp pattern has portability warnings: ${regexObj.source}`);
        for (const warning of validation.warnings) {
          console.warn(`  Warning: ${warning}`);
        }
      }

      const patternAst = valueOrExprToAstTyped(regexObj.source, StringType);
      const flagsAst = valueOrExprToAstTyped(regexObj.flags, StringType);
      const replaceAst = valueOrExprToAstTyped(replaceValue, StringType);
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: StringType,
        location: get_location(),
        builtin: "RegexReplace",
        type_parameters: [],
        arguments: [this[AstSymbol], patternAst, flagsAst, replaceAst],
      }) as StringExpr;
    } else {
      const searchAst = valueOrExprToAstTyped(searchValue as string | StringExpr, StringType);
      const replaceAst = valueOrExprToAstTyped(replaceValue, StringType);
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: StringType,
        location: get_location(),
        builtin: "StringReplace",
        type_parameters: [],
        arguments: [this[AstSymbol], searchAst, replaceAst],
      }) as StringExpr;
    }
  }

  /**
   * Encodes the string as UTF-8 bytes, returning a Blob.
   *
   * @returns A BlobExpr containing the UTF-8 encoded bytes
   *
   * @remarks No byte-order mark (BOM) is added. UTF-8 is a superset of ASCII.
   *
   * @example
   * ```ts
   * const encodeUtf8 = East.function([StringType], BlobType, ($, str) => {
   *   $.return(str.encodeUtf8());
   * });
   * const compiled = East.compile(encodeUtf8.toIR(), []);
   * compiled("hello");          // Blob with UTF-8 bytes
   * compiled("😀");             // Blob with UTF-8 encoded emoji
   * ```
   */
  encodeUtf8(): ExprType<BlobType> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BlobType,
      location: get_location(),
      builtin: "StringEncodeUtf8",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as ExprType<BlobType>;
  }

  /**
   * Encodes the string as UTF-16 bytes, returning a Blob.
   *
   * @returns A BlobExpr containing the UTF-16 encoded bytes
   *
   * @remarks Always uses little-endian with a byte-order mark (BOM). UTF-16 is common on Windows.
   *
   * @example
   * ```ts
   * const encodeUtf16 = East.function([StringType], BlobType, ($, str) => {
   *   $.return(str.encodeUtf16());
   * });
   * const compiled = East.compile(encodeUtf16.toIR(), []);
   * compiled("hello");          // Blob with UTF-16 LE bytes + BOM
   * compiled("😀");             // Blob with UTF-16 encoded emoji
   * ```
   */
  encodeUtf16(): ExprType<BlobType> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BlobType,
      location: get_location(),
      builtin: "StringEncodeUtf16",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as ExprType<BlobType>;
  }

  /**
   * Checks if this string equals another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are equal
   *
   * @example
   * ```ts
   * const isEqual = East.function([StringType, StringType], BooleanType, ($, a, b) => {
   *   $.return(a.equals(b));
   * });
   * const compiled = East.compile(isEqual.toIR(), []);
   * compiled("hello", "hello");   // true
   * compiled("hello", "world");   // false
   * ```
   */
  equals(other: StringExpr | string): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this string does not equal another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are not equal
   *
   * @example
   * ```ts
   * const isNotEqual = East.function([StringType, StringType], BooleanType, ($, a, b) => {
   *   $.return(a.notEquals(b));
   * });
   * const compiled = East.compile(isNotEqual.toIR(), []);
   * compiled("hello", "world");   // true
   * compiled("hello", "hello");   // false
   * ```
   */
  notEquals(other: StringExpr | string): BooleanExpr {
    return notEqual(this, other);
  }

  /**
   * Checks if this string is greater than another value (lexicographically).
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this string is greater
   *
   * @example
   * ```ts
   * const isGreater = East.function([StringType, StringType], BooleanType, ($, a, b) => {
   *   $.return(a.greaterThan(b));
   * });
   * const compiled = East.compile(isGreater.toIR(), []);
   * compiled("b", "a");     // true
   * compiled("a", "b");     // false
   * compiled("a", "a");     // false
   * ```
   */
  greaterThan(other: StringExpr | string): BooleanExpr {
    return greater(this, other);
  }

  /**
   * Checks if this string is less than another value (lexicographically).
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this string is less
   *
   * @example
   * ```ts
   * const isLess = East.function([StringType, StringType], BooleanType, ($, a, b) => {
   *   $.return(a.lessThan(b));
   * });
   * const compiled = East.compile(isLess.toIR(), []);
   * compiled("a", "b");     // true
   * compiled("b", "a");     // false
   * compiled("a", "a");     // false
   * ```
   */
  lessThan(other: StringExpr | string): BooleanExpr {
    return less(this, other);
  }

  /**
   * Checks if this string is greater than or equal to another value (lexicographically).
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this string is greater than or equal
   *
   * @example
   * ```ts
   * const isGreaterOrEqual = East.function([StringType, StringType], BooleanType, ($, a, b) => {
   *   $.return(a.greaterThanOrEqual(b));
   * });
   * const compiled = East.compile(isGreaterOrEqual.toIR(), []);
   * compiled("b", "a");     // true
   * compiled("a", "a");     // true
   * compiled("a", "b");     // false
   * ```
   */
  greaterThanOrEqual(other: StringExpr | string): BooleanExpr {
    return greaterEqual(this, other);
  }

  /**
   * Checks if this string is less than or equal to another value (lexicographically).
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this string is less than or equal
   *
   * @example
   * ```ts
   * const isLessOrEqual = East.function([StringType, StringType], BooleanType, ($, a, b) => {
   *   $.return(a.lessThanOrEqual(b));
   * });
   * const compiled = East.compile(isLessOrEqual.toIR(), []);
   * compiled("a", "b");     // true
   * compiled("a", "a");     // true
   * compiled("b", "a");     // false
   * ```
   */
  lessThanOrEqual(other: StringExpr | string): BooleanExpr {
    return lessEqual(this, other);
  }

  // ============================================================================
  // Aliases for comparison operations
  // ============================================================================

  /** Alias for {@link equals} */
  eq = this.equals;
  /** Alias for {@link equals} */
  equal = this.equals;

  /** Alias for {@link notEquals} */
  ne = this.notEquals;
  /** Alias for {@link notEquals} */
  notEqual = this.notEquals;

  /** Alias for {@link greaterThan} */
  gt = this.greaterThan;
  /** Alias for {@link greaterThan} */
  greater = this.greaterThan;

  /** Alias for {@link lessThan} */
  lt = this.lessThan;
  /** Alias for {@link lessThan} */
  less = this.lessThan;

  /** Alias for {@link greaterThanOrEqual} */
  gte = this.greaterThanOrEqual;
  /** Alias for {@link greaterThanOrEqual} */
  ge = this.greaterThanOrEqual;
  /** Alias for {@link greaterThanOrEqual} */
  greaterEqual = this.greaterThanOrEqual;

  /** Alias for {@link lessThanOrEqual} */
  lte = this.lessThanOrEqual;
  /** Alias for {@link lessThanOrEqual} */
  le = this.lessThanOrEqual;
  /** Alias for {@link lessThanOrEqual} */
  lessEqual = this.lessThanOrEqual;
}