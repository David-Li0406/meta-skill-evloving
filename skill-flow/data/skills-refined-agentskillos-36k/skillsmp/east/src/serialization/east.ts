/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { type EastType, printIdentifier, type ValueTypeOf, TypeWiden, isTypeEqual, NeverType, NullType, BooleanType, IntegerType, FloatType, StringType, DateTimeType, BlobType, ArrayType, SetType, DictType, StructType, VariantType } from "../types.js";
import { compareFor } from "../comparison.js";
import { SortedMap } from "../containers/sortedmap.js";
import { SortedSet } from "../containers/sortedset.js";
import { isVariant, variant } from "../containers/variant.js";
import { EastTypeValueType, toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import { ref } from "../containers/ref.js";

class ParseError extends Error {
  constructor(message: string, public position: number, public path: string = '') {
    super(message);
    this.name = "ParseError";
  }
}

/**
 * Find the length of the common prefix between two path component arrays.
 */
function _commonPrefixLength(a: string[], b: string[]): number {
  let i = 0;
  while (i < a.length && i < b.length && a[i] === b[i]) {
    i++;
  }
  return i;
}

/**
 * Convert path component array to punctuated string for lookup/storage.
 * Example: [".field", "[3]"] -> ".field[3]"
 */
function _pathToPunctuated(path: string[]): string {
  return path.join("");
}

/**
 * Compute a relative reference string from currentPath to targetPath.
 * Returns a string like "2#.foo[0]" or "1#"
 *
 * The format is: "upLevels#remaining_path_components_as_punctuated"
 */
function _encodeRelativeRef(currentPath: string[], targetPath: string[]): string {
  const commonLen = _commonPrefixLength(currentPath, targetPath);
  const upLevels = currentPath.length - commonLen;
  const remaining = targetPath.slice(commonLen);

  if (remaining.length === 0) {
    return `${upLevels}#`;
  }

  const remainingStr = remaining.join("");
  return `${upLevels}#${remainingStr}`;
}

/**
 * Decode a relative reference string and return the target path array.
 * Input like "2#.foo[0]" returns the target path array.
 * Input like "1#" returns the target path array.
 */
function _decodeRelativeRef(refStr: string, currentPath: string[]): string[] {
  const hashIdx = refStr.indexOf('#');
  if (hashIdx === -1) {
    throw new Error(`Invalid relative reference: ${refStr}`);
  }

  const upLevelStr = refStr.substring(0, hashIdx);
  const remainingStr = refStr.substring(hashIdx + 1);

  let upLevels: number;
  try {
    upLevels = parseInt(upLevelStr);
  } catch {
    throw new Error(`Invalid relative reference: ${refStr}`);
  }

  if (upLevels < 0 || upLevels > currentPath.length) {
    throw new Error(`Invalid relative reference: going up ${upLevels} levels from depth ${currentPath.length}`);
  }

  // Build target path
  const targetPath = currentPath.slice(0, currentPath.length - upLevels);

  // Add remaining components if any
  if (remainingStr.length > 0) {
    // Parse the remaining punctuated path
    // Format: .field[0][key] etc.
    let pos = 0;
    while (pos < remainingStr.length) {
      if (remainingStr[pos] === '.') {
        // Identifier follows
        pos++;
        let end = pos;
        while (end < remainingStr.length && /[a-zA-Z0-9_]/.test(remainingStr[end]!)) {
          end++;
        }
        targetPath.push(`.${remainingStr.substring(pos, end)}`);
        pos = end;
      } else if (remainingStr[pos] === '[') {
        // Bracket expression
        let end = pos + 1;
        let depth = 1;
        while (end < remainingStr.length && depth > 0) {
          if (remainingStr[end] === '[') depth++;
          else if (remainingStr[end] === ']') depth--;
          end++;
        }
        targetPath.push(remainingStr.substring(pos, end));
        pos = end;
      } else {
        pos++;
      }
    }
  }

  return targetPath;
}

/**
 * Type-level context for tracking which RecursiveType we're inside during printing.
 * Uses late binding to break circular dependencies.
 */
/** Stack of printers for recursive types */
type EastPrintTypeContext = ((value: any, ctx?: EastPrintValueContext) => string)[];

/** Stack of parsers for recursive types */
type EastParseTypeContext = ((input: string, pos: number, ctx?: EastParseValueContext) => ParseSuccess<any>)[];

/**
 * Value-level context for tracking mutable aliases during printing.
 *
 * - refs: Map from mutable container values (Array/Set/Dict) to their path component arrays (e.g., [".field", "[3]"])
 * - currentPath: Stack of path components WITH punctuation (e.g., ".field", "[3]", "[(key)]")
 */
type EastPrintValueContext = {
  refs: Map<any, string[]>; // Mutable container -> path array with punctuation
  currentPath: string[]; // Path components with punctuation: [".field", "[3]", "[(x: 1)]"]
};

/**
 * Value-level context for tracking mutable aliases during parsing.
 *
 * - refs: Map from punctuated path strings to parsed mutable container values (Array/Set/Dict)
 * - currentPath: Stack of path components WITH punctuation (e.g., ".field", "[3]", "[(key)]")
 */
type EastParseValueContext = {
  refs: Map<string, any>; // Punctuated path string -> Mutable container value
  currentPath: string[]; // Path components with punctuation: [".field", "[3]", "[(x: 1)]"]
};

export function encodeEastFor(type: EastTypeValue): (x: any) => Uint8Array
export function encodeEastFor<T extends EastType>(type: T): (x: ValueTypeOf<T>) => Uint8Array
export function encodeEastFor(type: EastTypeValue | EastType): (x: any) => Uint8Array {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  const textEncoder = new TextEncoder();
  const printer = printFor(type as EastTypeValue);
  return (x: any) => textEncoder.encode(printer(x, { refs: new Map(), currentPath: [] }));
}

export function decodeEastFor(type: EastTypeValue): (x: Uint8Array) => any
export function decodeEastFor<T extends EastType>(type: T): (x: Uint8Array) => ValueTypeOf<T>
export function decodeEastFor(type: EastType | EastTypeValue): (x: Uint8Array) => any {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  const textDecoder = new TextDecoder();
  const parser = parseFor(type as EastTypeValue);
  return (x: Uint8Array) => {
    const result = parser(textDecoder.decode(x));
    if (result.success) {
      return result.value;
    } else {
      throw new Error(`Failed to decode East value of type ${printFor(EastTypeValueType)(type)}: ${result.error}`);
    }
  };
}

export function printFor(
  type: EastTypeValue,
  typeCtx?: EastPrintTypeContext
): (value: any, ctx?: EastPrintValueContext) => string
export function printFor<T extends EastType>(
  type: T,
): (value: ValueTypeOf<T>, ctx?: EastPrintValueContext) => string
export function printFor(
  type: EastTypeValue | EastType,
  typeCtx: EastPrintTypeContext = []
): (value: any, ctx?: EastPrintValueContext) => string {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type as EastType);
  }

  if (type.type === "Never") {
    return (_: unknown, _ctx?: EastPrintValueContext) => { throw new Error(`Attempted to print value of type .Never`)};
  } else if (type.type === "Null") {
     return (_: null, _ctx?: EastPrintValueContext) => "null";
  } else if (type.type === "Boolean") {
    return (x: boolean, _ctx?: EastPrintValueContext) => x.toString();
  } else if (type.type === "Integer") {
    return (x: bigint, _ctx?: EastPrintValueContext) => x.toString();
  } else if (type.type === "Float") {
    return (x: number, _ctx?: EastPrintValueContext) => {
      // Handle negative zero specially
      if (Object.is(x, -0)) {
        return "-0.0";
      }
      const str = x.toString();
      // check if str is integer-like
      if (/^-?\d+$/.test(str)) {
        // append a .0 to indicate it's a float
        return str + ".0";
      } else {
        return str;
      }
    }
  } else if (type.type === "String") {
    return (x: string, _ctx?: EastPrintValueContext) => JSON.stringify(x);
  } else if (type.type === "DateTime") {
    return (x: Date, _ctx?: EastPrintValueContext) => x.toISOString().substring(0, 23);
  } else if (type.type === "Blob") {
    return (x: Uint8Array, _ctx?: EastPrintValueContext) => `0x${[...x].map(b => b.toString(16).padStart(2, "0")).join("")}`;
  } else if (type.type === "Ref") {
    let value_printer: (value: any, ctx?: EastPrintValueContext) => string;
    const ret = (x: ref<any>, ctx: EastPrintValueContext = { refs: new Map(), currentPath: [] }) => {
      // Check for mutable alias
      if (ctx.refs.has(x)) {
        const targetPath = ctx.refs.get(x)!;
        const refStr = _encodeRelativeRef(ctx.currentPath, targetPath);
        return refStr;
      }
      // Register this ref
      ctx.refs.set(x, [...ctx.currentPath]);

      // Serialize ref
      ctx.currentPath.push(`[]`);
      const str = value_printer(x.value, ctx)
      ctx.currentPath.pop();
      return `&${str}`;
    };
    typeCtx.push(ret);
    value_printer = printFor(type.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Array") {
    let value_printer: (value: any, ctx?: EastPrintValueContext) => string;
    const ret = (x: any[], ctx: EastPrintValueContext = { refs: new Map(), currentPath: [] }) => {
      // Check for mutable alias
      if (ctx.refs.has(x)) {
        const targetPath = ctx.refs.get(x)!;
        const refStr = _encodeRelativeRef(ctx.currentPath, targetPath);
        return refStr;
      }
      // Register this array
      ctx.refs.set(x, [...ctx.currentPath]);

      // Serialize elements
      const parts: string[] = [];
      for (let i = 0; i < x.length; i++) {
        ctx.currentPath.push(`[${i}]`);
        parts.push(value_printer(x[i], ctx));
        ctx.currentPath.pop();
      }
      return `[${parts.join(", ")}]`;
    };
    typeCtx.push(ret);
    value_printer = printFor(type.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Set") {
    const key_printer = printFor(type.value, typeCtx);
    return (x: Set<any>, ctx: EastPrintValueContext = { refs: new Map(), currentPath: [] }) => {
      // Check for mutable alias
      if (ctx.refs.has(x)) {
        const targetPath = ctx.refs.get(x)!;
        const refStr = _encodeRelativeRef(ctx.currentPath, targetPath);
        return refStr;
      }
      // Register this set
      ctx.refs.set(x, [...ctx.currentPath]);

      // Serialize elements
      const parts: string[] = [];
      for (const k of x) {
        // Use fresh context for keys - no path syntax to reference inside keys
        parts.push(key_printer(k));
      }
      return `{${parts.join(",")}}`;
    };
  } else if (type.type === "Dict") {
    const key_printer = printFor(type.value.key, typeCtx);
    let value_printer: (value: any, ctx?: EastPrintValueContext) => string;
    const ret = (x: Map<any, any>, ctx: EastPrintValueContext = { refs: new Map(), currentPath: [] }) => {
      // Check for mutable alias
      if (ctx.refs.has(x)) {
        const targetPath = ctx.refs.get(x)!;
        const refStr = _encodeRelativeRef(ctx.currentPath, targetPath);
        return refStr;
      }
      // Register this dict
      ctx.refs.set(x, [...ctx.currentPath]);

      if (x.size === 0) return "{:}";

      // Serialize entries
      const parts: string[] = [];
      for (const [k, v] of x) {
        // Use fresh context for keys - no path syntax to reference inside keys
        const keyStr = key_printer(k);

        // Print value with path tracking
        ctx.currentPath.push(`[${keyStr}]`);
        const valueStr = value_printer(v, ctx);
        ctx.currentPath.pop();

        parts.push(`${keyStr}:${valueStr}`);
      }
      return `{${parts.join(",")}}`;
    };
    typeCtx.push(ret);
    value_printer = printFor(type.value.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Struct") {
    const field_printers: [string, (value: any, ctx?: EastPrintValueContext) => string][] = [];
    const ret = (x: Record<string, any>, ctx: EastPrintValueContext = { refs: new Map(), currentPath: [] }) => {
      const parts: string[] = [];
      for (const [k, printer] of field_printers) {
        const fieldName = printIdentifier(k);
        const pathComponent = k === fieldName ? `.${k}` : `.${fieldName}`;

        ctx.currentPath.push(pathComponent);
        const printed = printer(x[k], ctx);
        ctx.currentPath.pop();

        parts.push(`${fieldName}=${printed}`);
      }
      return `(${parts.join(", ")})`;
    };
    typeCtx.push(ret);
    for (const { name: k, type: t } of type.value) {
      field_printers.push([k, printFor(t, typeCtx)]);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Variant") {
    const case_printers: Record<string, (value: any, ctx?: EastPrintValueContext) => string> = {};
    const ret = (x: variant<string, any>, ctx: EastPrintValueContext = { refs: new Map(), currentPath: [] }) => {
      // Add variant case to path
      ctx.currentPath.push(`.${x.type}`);
      const result = case_printers[x.type]!(x.value, ctx);
      ctx.currentPath.pop();
      return result;
    };
    typeCtx.push(ret);
    for (const { name: k, type: t } of type.value) {
      if (t.type === "Null") {
        const prefix = `.${printIdentifier(k)}`;
        case_printers[k] = (_value: any, _ctx?: EastPrintValueContext) => prefix;
      } else {
        const prefix = `.${printIdentifier(k)} `;
        const print_data = printFor(t, typeCtx);
        case_printers[k] = (value: any, ctx?: EastPrintValueContext) => prefix + print_data(value, ctx);
      }
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Function") {
    // This is just a convenience printer - functions cannot be serialized/deserialized
    return (_: (x: any) => any, _ctx?: EastPrintValueContext) => `(${type.value.inputs.map((x: EastTypeValue) => printTypeValue(x)).join(", ")}) => ${printTypeValue(type.value.output)}`;
  } else if (type.type === "AsyncFunction") {
    // This is just a convenience printer - async functions cannot be serialized/deserialized
    return (_: (x: any) => any, _ctx?: EastPrintValueContext) => `async (${type.value.inputs.map((x: EastTypeValue) => printTypeValue(x)).join(", ")}) => ${printTypeValue(type.value.output)}`;
  } else if (type.type === "Recursive") {
    const ret = typeCtx[typeCtx.length - Number(type.value)];
    if (ret === undefined) {
      throw new Error(`Internal error: Recursive type context not found`);
    }
    return ret;
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  }
}

const printTypeValue = printFor(EastTypeValueType);

/** Create a parser for a specific EastType.
 *
 * You can optional specify that the resulting value should be frozen (making the collection types immutable).
 */
// Helper to convert position to line and column
function getLineAndColumn(input: string, position: number): { line: number, column: number } {
  let line = 1;
  let column = 1;
  for (let i = 0; i < position && i < input.length; i++) {
    if (input[i] === '\n') {
      line++;
      column = 1;
    } else {
      column++;
    }
  }
  return { line, column };
}

export function parseFor(type: EastTypeValue, frozen?: boolean): (x: string) => ParseResult<any>
export function parseFor<T extends EastType>(type: T, frozen?: boolean): (x: string) => ParseResult<ValueTypeOf<T>>
export function parseFor(type: EastTypeValue | EastType, frozen: boolean = false): (x: string) => ParseResult<any> {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  const parser = createParser(type as EastTypeValue, frozen);
  return (x: string) => {
    try {
      const { value, position } = parser(x, 0);
      const pos = consumeWhitespace(x, position);
      if (pos < x.length) {
        const { line, column } = getLineAndColumn(x, pos);
        return {
          success: false,
          error: `Error occurred because unexpected input after parsed value (line ${line}, col ${column}) while parsing value of type "${printFor(EastTypeValueType)(type)}"`,
          position: pos,
        };
      }
      return { success: true, value, position };
    } catch (e) {
      if (e instanceof ParseError) {
        const { line, column } = getLineAndColumn(x, e.position);
        const pathStr = e.path ? ` at ${e.path}` : '';
        return {
          success: false,
          error: `Error occurred because ${e.message}${pathStr} (line ${line}, col ${column}) while parsing value of type "${printFor(EastTypeValueType)(type)}"`,
          position: e.position,
        };
      }
      throw e;
    }
  };
}

// Public API - ParseResult stays the same (success/failure discriminated union)
type ParseResult<T> = {
  success: true;
  value: T;
  position: number;
} | {
  success: false;
  error: string;
  position: number;
};

// Internal parser success return type (throws ParseError on failure)
type ParseSuccess<T> = {
  value: T;
  position: number;
};

// Internal parsers throw ParseError and return ParseSuccess on success
type Parser<T> = (input: string, startPos: number, ctx?: EastParseValueContext) => ParseSuccess<T>;

// Consume whitespace by returning new position
const consumeWhitespace = (input: string, pos: number): number => {
  while (pos < input.length && /\s/.test(input[pos]!)) {
    pos++;
  }
  return pos;
};

const createParser = (type: EastTypeValue, frozen: boolean, typeCtx: EastParseTypeContext = []): Parser<any> => {
  switch (type.type) {
    case "Null":
       return parseNull;
    case "Boolean":
      return parseBoolean;
    case "Integer":
      return parseInteger;
    case "Float":
      return parseFloat;
    case "String":
      return parseString;
    case "DateTime":
      return parseDateTime(frozen);
    case "Blob":
      return parseBlob(frozen);
    case "Ref":
      return createRefParser(type.value, frozen, typeCtx);
    case "Array":
      return createArrayParser(type.value, frozen, typeCtx);
    case "Set":
      return createSetParser(type.value, frozen, typeCtx);
    case "Dict":
      return createDictParser(type.value.key, type.value.value, frozen, typeCtx);
    case "Struct":
      return createStructParser(type.value, frozen, typeCtx);
    case "Variant":
      return createVariantParser(type.value, frozen, typeCtx);
    case "Function":
      throw new Error(`Cannot parse .Function`);
    case "AsyncFunction":
      throw new Error(`Cannot parse .AsyncFunction`);
    case "Never":
      return (_input: string, pos: number, _ctx?: EastParseValueContext) => { throw new ParseError(`Attempted to parse value of type .Never`, pos) };
    case "Recursive":
      const ret = typeCtx[typeCtx.length - Number(type.value)];
      if (ret === undefined) {
        throw new Error(`Internal error: Recursive type context not found`);
      }
      return ret;
    default:
      throw new Error(`Unhandled type: ${(type satisfies never as any).type}`);
  }
};

const parseInteger: Parser<bigint> = (input: string, pos: number, _ctx?: EastParseValueContext) => {
  pos = consumeWhitespace(input, pos);

  if (pos >= input.length) {
    throw new ParseError("expected integer, got end of input", pos);
  }

  let start = pos;
  if (input[pos] === '-') {
    pos++;
  }

  let hasDigits = false;
  while (pos < input.length && /\d/.test(input[pos]!)) {
    hasDigits = true;
    pos++;
  }

  if (!hasDigits) {
    const got = start >= input.length ? 'end of input' : `'${input[start]}'`;
    throw new ParseError(`expected integer, got ${got}`, start);
  }

  const intStr = input.slice(start, pos);
  let value: bigint;

  try {
    value = BigInt(intStr);
  } catch {
    // BigInt() throws if the string is invalid (shouldn't happen given our parsing logic)
    throw new ParseError(`expected integer, got ${JSON.stringify(intStr)}`, start);
  }

  // Check for 64-bit signed integer range: -2^63 to 2^63-1
  if (value < -9223372036854775808n || value > 9223372036854775807n) {
    throw new ParseError(`integer out of range (must be 64-bit signed), got ${intStr}`, start);
  }

  return {
    value,
    position: pos
  };
};

const parseFloat: Parser<number> = (input: string, pos: number, _ctx?: EastParseValueContext) => {
  pos = consumeWhitespace(input, pos);

  if (pos >= input.length) {
    throw new ParseError("expected float, got end of input", pos);
  }

  // Accept NaN and Infinity
  if (input.startsWith('NaN', pos)) {
    return { value: NaN, position: pos + 3 };
  }
  if (input.startsWith('Infinity', pos)) {
    return { value: Infinity, position: pos + 8 };
  }

  let start = pos;
  if (input[pos] === '-') {
    pos++;
    if (input.startsWith('Infinity', pos)) {
      return { value: -Infinity, position: pos + 8 };
    }
  }

  let hasDigits = false;
  while (pos < input.length && /\d/.test(input[pos]!)) {
    hasDigits = true;
    pos++;
  }

  if (!hasDigits) {
    const got = start >= input.length ? 'end of input' : `'${input[start]}'`;
    throw new ParseError(`expected float, got ${got}`, start);
  }

  if (pos < input.length && input[pos] === '.') {
    pos++;
    while (pos < input.length && /\d/.test(input[pos]!)) {
      pos++;
    }
  }

  if (pos < input.length && (input[pos] === 'e' || input[pos] === 'E')) {
    pos++;
    if (pos < input.length && (input[pos] === '+' || input[pos] === '-')) {
      pos++;
    }
    let expDigits = false;
    while (pos < input.length && /\d/.test(input[pos]!)) {
      expDigits = true;
      pos++;
    }
    if (!expDigits) {
      throw new ParseError("expected digits in float exponent", pos);
    }
  }

  return {
    value: Number(input.slice(start, pos)),
    position: pos
  };
};

/**
 * Checks if the given position is at a valid token terminator.
 * Valid terminators are: EOF, whitespace, comma, or closing brackets/parens/braces.
 */
const isTokenTerminator = (input: string, pos: number): boolean => {
  if (pos >= input.length) return true; // EOF
  const ch = input[pos];
  return ch === ' ' || ch === '\t' || ch === '\n' || ch === '\r' ||
         ch === ',' || ch === ')' || ch === ']' || ch === '}';
};

/**
 * Parses a $.path reference and returns the referenced value.
 * Returns null if not at a reference (doesn't start with '$').
 * Throws ParseError if the reference is invalid or undefined.
 */
const parseReference = <T>(input: string, pos: number, ctx?: EastParseValueContext): ParseSuccess<T> | null => {
  // Check if this looks like a reference: either "#..." or "N#..." where N is a digit
  let refStart = pos;
  let isRelative = false;

  if (pos >= input.length || input[pos] !== '#') {
    // Check if it starts with a digit followed by '#' (relative reference)
    let digitEnd = pos;
    while (digitEnd < input.length && /[0-9]/.test(input[digitEnd]!)) {
      digitEnd++;
    }
    if (digitEnd > pos && digitEnd < input.length && input[digitEnd] === '#') {
      isRelative = true;
      refStart = pos;
    } else {
      return null; // Not a reference
    }
  }

  if (!ctx) {
    throw new ParseError("#reference outside recursive context", pos);
  }

  // Parse the path - it can contain:
  // - #.field (dot followed by identifier)
  // - #[index] (bracket with number or value)
  // - combinations like #.a.b[0].c
  // OR for relative: N#.field etc.

  let pathStart: number;
  if (isRelative) {
    // Find the # position
    pathStart = input.indexOf('#', pos);
    refStart = pathStart + 1; // Start after '#'
  } else {
    refStart = pos + 1; // Start after '#'
  }

  let pathEnd = refStart;

  while (pathEnd < input.length) {
    const ch = input[pathEnd];

    if (ch === '.') {
      // Dot followed by identifier - keep going until we hit non-identifier char
      pathEnd++;
      while (pathEnd < input.length && /[a-zA-Z0-9_]/.test(input[pathEnd]!)) {
        pathEnd++;
      }
    } else if (ch === '[') {
      // Bracket - find the matching close bracket
      pathEnd++;
      let depth = 1;
      while (pathEnd < input.length && depth > 0) {
        if (input[pathEnd] === '[') depth++;
        else if (input[pathEnd] === ']') depth--;
        pathEnd++;
      }
    } else {
      // Hit something that's not part of the path
      break;
    }
  }

  const refStr = input.substring(pos, pathEnd);

  // Resolve the target path
  let targetPathStr: string;
  try {
    if (isRelative) {
      // refStr is like "1#.a" - pass it directly to _decodeRelativeRef
      const targetPath = _decodeRelativeRef(refStr, ctx.currentPath);
      targetPathStr = _pathToPunctuated(targetPath);
    } else {
      // Absolute reference: just use the path part directly (without the leading #)
      targetPathStr = refStr.substring(1);
    }
  } catch (e) {
    throw new ParseError(`invalid reference ${refStr}: ${e instanceof Error ? e.message : String(e)}`, pos);
  }

  // Look up in refs map
  if (!ctx.refs.has(targetPathStr)) {
    throw new ParseError(`undefined reference ${refStr}`, pos);
  }

  return { value: ctx.refs.get(targetPathStr), position: pathEnd };
};

const parseBoolean: Parser<boolean> = (input: string, pos: number, _ctx?: EastParseValueContext) => {
  pos = consumeWhitespace(input, pos);

  if (input.startsWith('true', pos)) {
    return { value: true, position: pos + 4 };
  }

  if (input.startsWith('false', pos)) {
    return { value: false, position: pos + 5 };
  }

  const got = pos >= input.length ? 'end of input' : `'${input[pos]}'`;
  throw new ParseError(`expected boolean, got ${got}`, pos);
};

const parseNull: Parser<null> = (input: string, pos: number, _ctx?: EastParseValueContext) => {
  pos = consumeWhitespace(input, pos);

  if (input.startsWith('null', pos) && isTokenTerminator(input, pos + 4)) {
    return { value: null, position: pos + 4 };
  }

  const got = pos >= input.length ? 'end of input' : `'${input[pos]}'`;
  throw new ParseError(`expected null, got ${got}`, pos);
};

const parseString: Parser<string> = (input: string, pos: number, _ctx?: EastParseValueContext) => {
  pos = consumeWhitespace(input, pos);

  if (input[pos] !== '"') {
    const got = pos >= input.length ? 'end of input' : `'${input[pos]}'`;
    throw new ParseError(`expected '"', got ${got}`, pos);
  }

  pos += 1;
  let rangeStart = pos;
  let result = "";

  // search through for escape characters, copy string out in ranges
  while (pos < input.length) {
    const char = input[pos];
    if (char === '\\') {
      result = result + input.substring(rangeStart, pos);
      pos += 1;
      if (pos < input.length) {
        const char2 = input[pos];
        if (char2 === '\\' || char2 === '\"') {
          result = result + char2;
          pos += 1;
          rangeStart = pos;
        } else {
          // TODO we need to (a) deal with escape sequences at least for unprintable characters and (b) safely handle LTR-RTL transition characters
          throw new ParseError("unexpected escape sequence in string", pos);
        }
      } else {
        throw new ParseError("unterminated string (missing closing quote)", pos);
      }
    } else if (char === '\"') {
      result = result + input.substring(rangeStart, pos);
      return { value: result, position: pos + 1 };
    } else {
      pos += 1;
    }
  }

  throw new ParseError("unterminated string (missing closing quote)", pos);
};

const parseDateTime = (frozen: boolean): Parser<Date> => (input: string, pos: number, _ctx?: EastParseValueContext) => {
  // Datetime format is YYYY-MM-DDTHH:MM:SS.sss (optional miliseconds, no quotes, no timezone or Z)
  pos = consumeWhitespace(input, pos);

  const datetimeRegex = /^-?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?/;
  const match = datetimeRegex.exec(input.slice(pos));
  if (!match) {
    throw new ParseError("expected DateTime in format YYYY-MM-DDTHH:MM:SS.sss", pos);
  }

  const datetimeStr = match[0];
  const date = new Date(datetimeStr + 'Z'); // Our naive datetimes are treated as UTC
  if (isNaN(date.getTime())) {
    throw new ParseError(`invalid DateTime value, got ${JSON.stringify(datetimeStr)}`, pos);
  }
  if (frozen) {
    Object.freeze(date);
  }

  return { value: date, position: pos + datetimeStr.length };
}

const parseBlob = (frozen: boolean): Parser<Uint8Array> => (input: string, pos: number, _ctx?: EastParseValueContext) => {
  pos = consumeWhitespace(input, pos);

  if (pos >= input.length || input[pos] !== '0' || input[pos + 1] !== 'x') {
    throw new ParseError("expected Blob starting with 0x", pos);
  }
  pos += 2;

  let start = pos;
  while (pos < input.length && /[0-9a-fA-F]/.test(input[pos]!)) {
    pos++;
  }

  const hexStr = input.slice(start, pos);

  // Check for odd length or invalid hex characters
  if (hexStr.length % 2 !== 0) {
    throw new ParseError(`invalid hex string (odd length), got "0x${hexStr}"`, start - 2);
  }

  // Note: The while loop above already validates that all characters are valid hex,
  // so we don't need an additional check here. If there were invalid characters,
  // they would be left in the input and caught by downstream parsing.

  const byteLength = hexStr.length / 2;
  const bytes = new Uint8Array(byteLength);
  for (let i = 0; i < byteLength; i++) {
    bytes[i] = parseInt(hexStr.substring(i * 2, i * 2 + 2), 16);
  }

  if (frozen) {
    Object.freeze(bytes);
  }

  return { value: bytes, position: pos };
};

const createRefParser = (value_type: EastTypeValue, frozen: boolean, typeCtx: EastParseTypeContext): Parser<ref<any>> => {
  let valueParser: Parser<any>;
  const ret = (input: string, pos: number, ctx?: EastParseValueContext) => {
    pos = consumeWhitespace(input, pos);

    // Create context if we don't have one (for top-level parsing with aliases)
    const needsOwnContext = !ctx;
    if (needsOwnContext) {
      ctx = { refs: new Map(), currentPath: [] };
    }

    // Check for reference first
    const reference = parseReference<ref<any>>(input, pos, ctx);
    if (reference) {
      return reference;
    }

    if (pos >= input.length || input[pos] !== '&') {
      throw new ParseError("expected '&' to start ref", pos);
    }

    pos = consumeWhitespace(input, pos + 1);
    const r: ref<any> = ref(undefined);

    // Pre-register this ref if we have context
    if (ctx) {
      const pathStr = _pathToPunctuated(ctx.currentPath);
      ctx.refs.set(pathStr, r);
    }

    if (ctx) ctx.currentPath.push(`[]`);
    let value;
    let position;
    try {
      const result = valueParser(input, pos, ctx);
      value = result.value;
      position = result.position;
    } catch (e) {
      if (e instanceof ParseError) {
          const newPath = `[]` + (e.path ? e.path : '');
          throw new ParseError(e.message, e.position, newPath);
        }
        throw e;
    } finally {
      if (ctx) ctx.currentPath.pop();
    }

    r.value = value;

    return { value: r, position };
  };
  typeCtx.push(ret);
  valueParser = createParser(value_type, frozen, typeCtx);
  typeCtx.pop();
  return ret;
};

const createArrayParser = (value_type: EastTypeValue, frozen: boolean, typeCtx: EastParseTypeContext): Parser<any[]> => {
  let valueParser: Parser<any>;
  const ret = (input: string, pos: number, ctx?: EastParseValueContext) => {
    pos = consumeWhitespace(input, pos);

    // Create context if we don't have one (for top-level parsing with aliases)
    const needsOwnContext = !ctx;
    if (needsOwnContext) {
      ctx = { refs: new Map(), currentPath: [] };
    }

    // Check for reference first
    const ref = parseReference<any[]>(input, pos, ctx);
    if (ref) {
      return ref;
    }

    if (pos >= input.length || input[pos] !== '[') {
      throw new ParseError("expected '[' to start array", pos);
    }

    pos = consumeWhitespace(input, pos + 1);
    const values: any[] = [];

    // Pre-register this array if we have context
    if (ctx) {
      const pathStr = _pathToPunctuated(ctx.currentPath);
      ctx.refs.set(pathStr, values);
    }

    // Handle empty array
    if (input[pos] === ']') {
      if (frozen) {
        Object.freeze(values);
      }
      return { value: values, position: pos + 1 };
    }

    let elementIndex = 0;
    while (true) {
      if (ctx) ctx.currentPath.push(`[${elementIndex}]`);
      try {
        const { value: elementValue, position: elementPos } = valueParser(input, pos, ctx);
        values.push(elementValue);
        pos = consumeWhitespace(input, elementPos);
      } catch (e) {
        if (e instanceof ParseError) {
          const newPath = `[${elementIndex}]` + (e.path ? e.path : '');
          throw new ParseError(e.message, e.position, newPath);
        }
        throw e;
      } finally {
        if (ctx) ctx.currentPath.pop();
      }

      if (input[pos] === ']') {
        if (frozen) {
          Object.freeze(values);
        }
        return { value: values, position: pos + 1 };
      }

      if (input[pos] !== ',') {
        throw new ParseError("expected ',' or ']' after array element", pos);
      }

      pos = consumeWhitespace(input, pos + 1);
      elementIndex++;
    }
  };
  typeCtx.push(ret);
  valueParser = createParser(value_type, frozen, typeCtx);
  typeCtx.pop();
  return ret;
};

const createSetParser = (key_type: EastTypeValue, frozen: boolean, typeCtx: EastParseTypeContext): Parser<Set<any>> => {
  const keyParser = createParser(key_type, frozen, typeCtx);
  const keyCompare = compareFor(key_type);

  return (input: string, pos: number, ctx?: EastParseValueContext) => {
    pos = consumeWhitespace(input, pos);

    // Create context if we don't have one (for top-level parsing with aliases)
    const needsOwnContext = !ctx;
    if (needsOwnContext) {
      ctx = { refs: new Map(), currentPath: [] };
    }

    // Check for reference first
    const ref = parseReference<Set<any>>(input, pos, ctx);
    if (ref) {
      return ref;
    }

    if (pos >= input.length || input[pos] !== '{') {
      throw new ParseError("expected '{' to start set", pos);
    }

    pos = consumeWhitespace(input, pos + 1);
    const values = new SortedSet(undefined, keyCompare);

    // Pre-register this set if we have context
    if (ctx) {
      const pathStr = _pathToPunctuated(ctx.currentPath);
      ctx.refs.set(pathStr, values);
    }

    // Handle empty set
    if (input[pos] === '}') {
      if (frozen) {
        Object.freeze(values);
      }
      return { value: values, position: pos + 1 };
    }

    let elementIndex = 0;
    while (true) {
      try {
        const keyResult = keyParser(input, pos, ctx);
        values.add(keyResult.value);
        pos = consumeWhitespace(input, keyResult.position);
      } catch (e) {
        if (e instanceof ParseError) {
          const newPath = `[${elementIndex}]` + (e.path ? e.path : '');
          throw new ParseError(e.message, e.position, newPath);
        }
        throw e;
      }

      if (input[pos] === '}') {
        if (frozen) {
          Object.freeze(values);
        }
        return { value: values, position: pos + 1 };
      }

      if (input[pos] !== ',') {
        throw new ParseError("expected ',' or '}' after set element", pos);
      }

      pos = consumeWhitespace(input, pos + 1);
      elementIndex++;
    }
  };
};

const createDictParser = (key_type: EastTypeValue, value_type: EastTypeValue, frozen: boolean, typeCtx: EastParseTypeContext): Parser<SortedMap<any, any>> => {
  const keyParser = createParser(key_type, frozen, typeCtx);
  let valueParser: Parser<any>;
  const keyCompare = compareFor(key_type);
  const keyPrinter = printFor(key_type);

  const ret = (input: string, pos: number, ctx?: EastParseValueContext) => {
    pos = consumeWhitespace(input, pos);

    // Create context if we don't have one (for top-level parsing with aliases)
    const needsOwnContext = !ctx;
    if (needsOwnContext) {
      ctx = { refs: new Map(), currentPath: [] };
    }

    // Check for reference first
    const ref = parseReference<SortedMap<any, any>>(input, pos, ctx);
    if (ref) {
      return ref;
    }

    if (pos >= input.length || input[pos] !== '{') {
      throw new ParseError("expected '{' to start dict", pos);
    }

    pos = consumeWhitespace(input, pos + 1);
    const values = new SortedMap(undefined, keyCompare);

    // Pre-register this dict if we have context
    if (ctx) {
      const pathStr = _pathToPunctuated(ctx.currentPath);
      ctx.refs.set(pathStr, values);
    }

    // Handle empty dict
    if (input[pos] === ':') {
      pos = consumeWhitespace(input, pos + 1);
      if (input[pos] === '}') {
        if (frozen) {
          Object.freeze(values);
        }
        return { value: values, position: pos + 1 };
      } else {
        throw new ParseError("expected '}' after ':' in empty dict", pos);
      }
    }
    // be lenient and allow empty set syntax as well
    if (input[pos] === '}') {
      if (frozen) {
        Object.freeze(values);
      }
      return { value: values, position: pos + 1 };
    }

    let entryIndex = 0;
    while (true) {
      let dictKey: any;
      try {
        const { value: keyValue, position: keyPos } = keyParser(input, pos, ctx);
        dictKey = keyValue;
        pos = consumeWhitespace(input, keyPos);
      } catch (e) {
        if (e instanceof ParseError) {
          const newPath = `[${entryIndex}](key)` + (e.path ? e.path : '');
          throw new ParseError(e.message, e.position, newPath);
        }
        throw e;
      }

      if (input[pos] !== ':') {
        throw new ParseError(`expected ':' after dict key at entry ${entryIndex}`, pos);
      }

      // Track path for dict values
      if (ctx) {
        const keyStr = keyPrinter(dictKey);
        ctx.currentPath.push(`[${keyStr}]`);
      }
      try {
        const { value: dictValue, position: valuePos } = valueParser(input, pos + 1, ctx);
        values.set(dictKey, dictValue);
        pos = consumeWhitespace(input, valuePos);
      } catch (e) {
        if (e instanceof ParseError) {
          const keyStr = keyPrinter(dictKey);
          const newPath = `[${keyStr}]` + (e.path ? e.path : '');
          throw new ParseError(e.message, e.position, newPath);
        }
        throw e;
      } finally {
        if (ctx) ctx.currentPath.pop();
      }

      if (input[pos] === '}') {
        if (frozen) {
          Object.freeze(values);
        }
        return { value: values, position: pos + 1 };
      }

      if (input[pos] !== ',') {
        throw new ParseError("expected ',' or '}' after dict entry", pos);
      }

      pos = consumeWhitespace(input, pos + 1);
      entryIndex++;
    }
  };
  typeCtx.push(ret);
  valueParser = createParser(value_type, frozen, typeCtx);
  typeCtx.pop();
  return ret;
};

const parseQuotedIdentifier: Parser<string> = (input: string, pos: number, _ctx?: EastParseValueContext) => {
  pos = consumeWhitespace(input, pos);

  if (input[pos] !== '`') {
    throw new ParseError("expected identifier (opening `)", pos);
  }

  pos += 1;
  let rangeStart = pos;
  let result = "";

  // search through for escape characters, copy string out in ranges
  while (pos < input.length) {
    const char = input[pos];
    if (char === '\\') {
      result = result + input.substring(rangeStart, pos);
      pos += 1;
      if (pos < input.length) {
        const char2 = input[pos];
        if (char2 === '\\' || char2 === '`') {
          rangeStart = pos;
          pos += 1;
        } else {
          // TODO we need to (a) deal with escape sequences at least for unprintable characters and (b) safely handle LTR-RTL transition characters
          throw new ParseError("unexpected escape sequence in identifier", pos);
        }
      } else {
        throw new ParseError("unterminated identifier (missing closing `)", pos);
      }
    } else if (char === '`') {
      result = result + input.substring(rangeStart, pos);
      return { value: result, position: pos + 1 };
    }
    pos += 1;
  }

  throw new ParseError("unterminated identifier (missing closing `)", pos);
};

const parseIdentifier: Parser<string> = (input: string, pos: number, _ctx?: EastParseValueContext) => {
  pos = consumeWhitespace(input, pos);

  if (input[pos] === '`') {
    return parseQuotedIdentifier(input, pos, _ctx);
  }

  if (pos < input.length && /[a-zA-Z_]/.test(input[pos]!)) {
    const initial_pos = pos;
    pos += 1;

    while (pos < input.length && /[a-zA-Z0-9_]/.test(input[pos]!)) {
      pos += 1;
    }

    // TODO possibly should check that the following character is valid (EOF, comma, bracket, etc)?

    return { value: input.substring(initial_pos, pos), position: pos };
  }

  throw new ParseError("expected identifier", pos);
}

const createStructParser = (fields: { name: string, type: EastTypeValue }[], frozen: boolean, typeCtx: EastParseTypeContext): Parser<Record<string, any>> => {
  const fieldNames = fields.map(f => f.name);
  const fieldParsers: Parser<any>[] = [];

  const ret = (input: string, pos: number, ctx?: EastParseValueContext) => {
    pos = consumeWhitespace(input, pos);

    // Create context if we don't have one (for top-level parsing with aliases)
    const needsOwnContext = !ctx;
    if (needsOwnContext) {
      ctx = { refs: new Map(), currentPath: [] };
    }

    if (pos >= input.length || input[pos] !== '(') {
      throw new ParseError("expected '(' to start struct", pos);
    }
    pos += 1;

    const result: Record<string, any> = {};

    let fieldIndex = 0;

    while (fieldIndex < fieldNames.length) {
      const fieldName = fieldNames[fieldIndex]!;
      pos = consumeWhitespace(input, pos);

      // Check for early closing paren (missing fields)
      if (input[pos] === ')') {
        throw new ParseError(`missing required field '${fieldName}'`, pos);
      }

      // Try to parse an identifier
      let parsedFieldName: string;
      let namePos: number;
      try {
        const identResult = parseIdentifier(input, pos, ctx);
        parsedFieldName = identResult.value;
        namePos = identResult.position;
      } catch (e) {
        if (e instanceof ParseError) {
          // If we can't parse an identifier, the field is missing
          throw new ParseError(`missing required field '${fieldName}'`, pos);
        }
        throw e;
      }

      // Check if the parsed field name matches what we expect
      if (parsedFieldName !== fieldName) {
        throw new ParseError(`unknown field '${parsedFieldName}', expected one of: ${fieldNames.join(', ')}`, pos);
      }
      pos = namePos;

      pos = consumeWhitespace(input, pos);

      if (pos >= input.length || input[pos] !== '=') {
        throw new ParseError(`expected '=' after field name '${fieldName}'`, pos);
      }
      pos += 1;

      const parser = fieldParsers[fieldIndex]!;
      // Track path for struct fields
      const fieldPath = /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(fieldName) ? `.${fieldName}` : `[${JSON.stringify(fieldName)}]`;
      if (ctx) ctx.currentPath.push(fieldPath);
      try {
        const { value: fieldValue, position: valuePos} = parser(input, pos, ctx);
        result[fieldName] = fieldValue;
        pos = valuePos;
      } catch (e) {
        if (e instanceof ParseError) {
          const newPath = fieldPath + (e.path ? e.path : '');
          throw new ParseError(e.message, e.position, newPath);
        }
        throw e;
      } finally {
        if (ctx) ctx.currentPath.pop();
      }

      // Look for comma or closing paren
      pos = consumeWhitespace(input, pos);
      if (pos >= input.length) {
        throw new ParseError("unexpected end of input in struct", pos);
      }

      if (input[pos] === ',') {
        pos = consumeWhitespace(input, pos + 1);
        fieldIndex++;
      } else if (input[pos] === ')') {
        // Check if we've parsed all fields
        if (fieldIndex !== fieldNames.length - 1) {
          throw new ParseError(`missing required field '${fieldNames[fieldIndex + 1]}'`, pos);
        }
        // All fields parsed, break and handle closing paren after loop
        break;
      } else {
        throw new ParseError("expected ',' or ')' after struct field", pos);
      }
    }

    // After loop, we should be at ')'
    pos = consumeWhitespace(input, pos);
    if (pos >= input.length || input[pos] !== ')') {
      // We've parsed all fields but there's more content - must be an unknown field
      if (pos < input.length) {
        try {
          const { value: extraField } = parseIdentifier(input, pos, ctx);
          throw new ParseError(`unknown field '${extraField}', expected one of: ${fieldNames.join(', ')}`, pos);
        } catch (e) {
          if (e instanceof ParseError && e.message.startsWith("Unknown field")) {
            throw e;
          }
          // Couldn't parse identifier, just say we expected ')'
          throw new ParseError("expected ')' to close struct", pos);
        }
      }
      throw new ParseError("expected ')' to close struct", pos);
    }

    if (frozen) {
      Object.freeze(result);
    }

    return { value: result, position: pos+1 };
  };
  typeCtx.push(ret);
  for (const field of fields) {
    fieldParsers.push(createParser(field.type, frozen, typeCtx));
  }
  typeCtx.pop();
  return ret;
};

const createVariantParser = (cases: { name: string, type: EastTypeValue }[], frozen: boolean, typeCtx: EastParseTypeContext): Parser<variant> => {
  const caseParsers: Record<string, Parser<any>> = {};
  const caseNames = cases.map(c => c.name);

  const ret = (input: string, pos: number, ctx?: EastParseValueContext) => {
    pos = consumeWhitespace(input, pos);

    // Create context if we don't have one (for top-level parsing with aliases)
    const needsOwnContext = !ctx;
    if (needsOwnContext) {
      ctx = { refs: new Map(), currentPath: [] };
    }

    if (pos >= input.length || input[pos] !== '.') {
      throw new ParseError("expected '.' to start variant case", pos);
    }
    pos += 1;

    // We cannot have whitespace
    const pos2 = consumeWhitespace(input, pos);
    if (pos2 !== pos) {
      throw new ParseError("whitespace not allowed between '.' and case identifier", pos);
    }

    const { value: caseName, position: casePos } = parseIdentifier(input, pos, ctx);
    const valueParser = caseParsers[caseName];
    if (valueParser === undefined) {
      throw new ParseError(`unknown variant case .${printIdentifier(caseName)}, expected one of: ${caseNames.map(c => `.${printIdentifier(c)}`).join(', ')}`, pos);
    }

    // Create variant with undefined placeholder
    const v = variant(caseName, undefined);

    // Parse the value with case name in path
    if (ctx) ctx.currentPath.push(`.${caseName}`);
    try {
      const { value: caseValue, position: valuePos } = valueParser(input, casePos, ctx);
      // Mutate the variant's value field
      (v as any).value = caseValue;
      if (frozen) {
        Object.freeze(v);
      }
      return { value: v, position: valuePos };
    } catch (e) {
      if (e instanceof ParseError) {
        const newPath = `.${caseName}` + (e.path ? e.path : '');
        throw new ParseError(e.message, e.position, newPath);
      }
      throw e;
    } finally {
      if (ctx) ctx.currentPath.pop();
    }
  };
  typeCtx.push(ret);
  for (const { name, type: caseType } of cases) {
    if (caseType.type === 'Null') {
      // Special case for null type - the "null" is actually optional
      caseParsers[name] = (input: string, pos: number, _ctx?: EastParseValueContext) => {
        pos = consumeWhitespace(input, pos);

        if (input.startsWith('null', pos) && isTokenTerminator(input, pos + 4)) {
          return { value: null, position: pos + 4 };
        } else if (isTokenTerminator(input, pos)) {
          // No "null" present, but we're at a valid terminator - that's ok for optional null
          return { value: null, position: pos };
        } else {
          const got = pos >= input.length ? 'end of input' : `'${input[pos]}'`;
          throw new ParseError(`expected null, got ${got}`, pos);
        }
      };
    } else {
      caseParsers[name] = createParser(caseType, frozen, typeCtx);
    }
  }
  typeCtx.pop();
  return ret;
}

/**
 * Parse an East value and infer its type from the syntax.
 *
 * @param input - The string to parse
 * @param frozen - Whether to freeze mutable containers (default: false)
 * @returns A tuple of [inferred type, parsed value]
 * @throws {Error} When parsing fails or type conflicts are detected
 *
 * @remarks
 * Type inference rules:
 * - Primitive types are distinguished by syntax (floats have `.` or `e`, integers don't)
 * - Empty array `[]` has type `Array<Never>`
 * - Empty set `{}` has type `Set<Never>`
 * - Empty dict `{:}` has type `Dict<Never, Never>`
 * - Non-empty collections widen element/key/value types via `TypeWiden`
 * - Each variant literal `.case data` creates a single-case variant, multiple cases widen
 * - Structs infer each field independently
 * - Recursive types are never inferred (circular references cause errors)
 * - Functions cannot be parsed
 *
 * @example
 * ```typescript
 * // Integer
 * const [type1, value1] = parseInferred("42");
 * // type1 = IntegerType, value1 = 42n
 *
 * // Float
 * const [type2, value2] = parseInferred("3.14");
 * // type2 = FloatType, value2 = 3.14
 *
 * // Array with widening
 * const [type3, value3] = parseInferred("[1, 2, 3]");
 * // type3 = ArrayType(IntegerType), value3 = [1n, 2n, 3n]
 *
 * // Variant with widening
 * const [type4, value4] = parseInferred(".some 42");
 * // type4 = VariantType({ some: IntegerType }), value4 = variant("some", 42n)
 *
 * // Type mismatch error
 * parseInferred("[1, 2.5]"); // Error: cannot widen Integer to Float
 * ```
 */
export function parseInferred(input: string, frozen: boolean = false): [EastType, any] {
  try {
    const result = parseInferredValue(input, 0, frozen);
    const pos = consumeWhitespace(input, result.position);
    if (pos < input.length) {
      const { line, column } = getLineAndColumn(input, pos);
      throw new Error(`Unexpected input after parsed value at line ${line}, col ${column}`);
    }
    return [result.type, result.value];
  } catch (e) {
    if (e instanceof ParseError) {
      const { line, column } = getLineAndColumn(input, e.position);
      const pathStr = e.path ? ` at ${e.path}` : '';
      throw new Error(`${e.message}${pathStr} (line ${line}, col ${column})`);
    }
    throw e;
  }
}

// Internal type for inference results
type InferredValue = {
  type: EastType;
  value: any;
  position: number;
};

/**
 * Parse a value and infer its type.
 */
function parseInferredValue(input: string, startPos: number, frozen: boolean): InferredValue {
  const pos = consumeWhitespace(input, startPos);

  if (pos >= input.length) {
    throw new ParseError("unexpected end of input", pos);
  }

  const ch = input[pos]!;

  // Check for circular references - not supported in inference
  if (ch === '#' || (ch >= '0' && ch <= '9' && input.indexOf('#', pos) !== -1 && input.indexOf('#', pos) < pos + 10)) {
    // Rough heuristic: if we see a digit followed by # nearby, it might be a reference
    const nextHash = input.indexOf('#', pos);
    if (nextHash !== -1 && nextHash <= pos + 10) {
      throw new ParseError("circular references not supported in type inference", pos);
    }
  }

  // Dispatch based on first character
  if (ch === '[') {
    return parseInferredArray(input, pos, frozen);
  } else if (ch === '{') {
    return parseInferredSetOrDict(input, pos, frozen);
  } else if (ch === '(') {
    return parseInferredStruct(input, pos, frozen);
  } else if (ch === '.') {
    return parseInferredVariant(input, pos, frozen);
  } else if (ch === '"') {
    const { value, position } = parseString(input, pos);
    return { type: StringType, value, position };
  } else if (ch === '&') {
    throw new ParseError("ref types not supported in type inference", pos);
  } else if (input.startsWith('null', pos) && isTokenTerminator(input, pos + 4)) {
    return { type: NullType, value: null, position: pos + 4 };
  } else if (input.startsWith('true', pos) && isTokenTerminator(input, pos + 4)) {
    return { type: BooleanType, value: true, position: pos + 4 };
  } else if (input.startsWith('false', pos) && isTokenTerminator(input, pos + 5)) {
    return { type: BooleanType, value: false, position: pos + 5 };
  } else if (input.startsWith('0x', pos)) {
    const { value, position } = parseBlob(frozen)(input, pos);
    return { type: BlobType, value, position };
  } else if (input.startsWith('NaN', pos)) {
    return { type: FloatType, value: NaN, position: pos + 3 };
  } else if (input.startsWith('Infinity', pos)) {
    return { type: FloatType, value: Infinity, position: pos + 8 };
  } else if (ch === '-' && input.startsWith('-Infinity', pos)) {
    return { type: FloatType, value: -Infinity, position: pos + 9 };
  } else if (ch === '-' || (ch >= '0' && ch <= '9')) {
    // Check for datetime before trying number
    const datetimeMatch = /^-?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?/.exec(input.slice(pos));
    if (datetimeMatch) {
      const { value, position } = parseDateTime(frozen)(input, pos);
      return { type: DateTimeType, value, position };
    }
    return parseInferredNumber(input, pos);
  } else {
    throw new ParseError(`unexpected character '${ch}'`, pos);
  }
}

/**
 * Parse a number and infer whether it's an integer or float.
 * Floats must contain '.' or 'e'/'E', otherwise it's an integer.
 */
function parseInferredNumber(input: string, pos: number): InferredValue {
  // Try to parse as float first (lookahead for . or e)
  let hasDecimal = false;
  let hasExponent = false;
  let scanPos = pos;

  if (input[scanPos] === '-') scanPos++;

  while (scanPos < input.length && input[scanPos]! >= '0' && input[scanPos]! <= '9') {
    scanPos++;
  }

  if (scanPos < input.length && input[scanPos] === '.') {
    hasDecimal = true;
  }

  if (scanPos < input.length && (input[scanPos] === 'e' || input[scanPos] === 'E')) {
    hasExponent = true;
  }

  if (hasDecimal || hasExponent) {
    // It's a float
    const { value, position } = parseFloat(input, pos);
    return { type: FloatType, value, position };
  } else {
    // It's an integer
    const { value, position } = parseInteger(input, pos);
    return { type: IntegerType, value, position };
  }
}

/**
 * Parse an array and infer the element type by widening.
 */
function parseInferredArray(input: string, startPos: number, frozen: boolean): InferredValue {
  let pos = consumeWhitespace(input, startPos);

  if (input[pos] !== '[') {
    throw new ParseError("expected '[' to start array", pos);
  }

  pos = consumeWhitespace(input, pos + 1);
  const values: any[] = [];
  let elementType: EastType = NeverType;

  // Handle empty array
  if (input[pos] === ']') {
    const arr = frozen ? Object.freeze(values) : values;
    return { type: ArrayType(NeverType), value: arr, position: pos + 1 };
  }

  let elementIndex = 0;
  while (true) {
    try {
      const element = parseInferredValue(input, pos, frozen);
      values.push(element.value);

      // Widen element type
      try {
        elementType = TypeWiden(elementType, element.type);
      } catch (cause: unknown) {
        if (cause instanceof Error && cause.name === "TypeMismatchError") {
          throw new ParseError(`incompatible array element types: ${cause.message}`, pos, `[${elementIndex}]`);
        }
        throw cause;
      }

      pos = consumeWhitespace(input, element.position);
    } catch (e) {
      if (e instanceof ParseError) {
        const newPath = `[${elementIndex}]` + (e.path ? e.path : '');
        throw new ParseError(e.message, e.position, newPath);
      }
      throw e;
    }

    if (input[pos] === ']') {
      const arr = frozen ? Object.freeze(values) : values;
      return { type: ArrayType(elementType), value: arr, position: pos + 1 };
    }

    if (input[pos] !== ',') {
      throw new ParseError("expected ',' or ']' after array element", pos);
    }

    pos = consumeWhitespace(input, pos + 1);
    elementIndex++;
  }
}

/**
 * Parse either a set or dict and infer types.
 * Distinguishes based on presence of ':' (dict) vs no ':' (set).
 */
function parseInferredSetOrDict(input: string, startPos: number, frozen: boolean): InferredValue {
  let pos = consumeWhitespace(input, startPos);

  if (input[pos] !== '{') {
    throw new ParseError("expected '{' to start set or dict", pos);
  }

  pos = consumeWhitespace(input, pos + 1);

  // Check for empty dict syntax {:}
  if (input[pos] === ':') {
    pos = consumeWhitespace(input, pos + 1);
    if (input[pos] === '}') {
      const dict = new SortedMap(undefined, compareFor(NeverType));
      if (frozen) Object.freeze(dict);
      return { type: DictType(NeverType, NeverType), value: dict, position: pos + 1 };
    } else {
      throw new ParseError("expected '}' after ':' in empty dict", pos);
    }
  }

  // Check for empty set syntax {}
  if (input[pos] === '}') {
    const set = new SortedSet(undefined, compareFor(NeverType));
    if (frozen) Object.freeze(set);
    return { type: SetType(NeverType), value: set, position: pos + 1 };
  }

  // Parse first element to determine if set or dict
  const firstElementPos = pos;
  const firstElement = parseInferredValue(input, pos, frozen);
  pos = consumeWhitespace(input, firstElement.position);

  if (input[pos] === ':') {
    // It's a dict
    return parseInferredDictRest(input, startPos, frozen, firstElement, firstElementPos);
  } else {
    // It's a set
    return parseInferredSetRest(input, startPos, frozen, firstElement, firstElementPos);
  }
}

/**
 * Continue parsing a set after determining it's a set.
 */
function parseInferredSetRest(
  input: string,
  startPos: number,
  frozen: boolean,
  firstElement: InferredValue,
  firstElementPos: number
): InferredValue {
  let keyType: EastType = firstElement.type;
  const compare = compareFor(keyType);
  const values = new SortedSet(undefined, compare);

  try {
    values.add(firstElement.value);
  } catch (e) {
    throw new ParseError(`invalid set key: ${e instanceof Error ? e.message : String(e)}`, firstElementPos);
  }

  let pos = consumeWhitespace(input, firstElement.position);
  let elementIndex = 1;

  while (true) {
    if (input[pos] === '}') {
      if (frozen) Object.freeze(values);
      return { type: SetType(keyType), value: values, position: pos + 1 };
    }

    if (input[pos] !== ',') {
      throw new ParseError("expected ',' or '}' after set element", pos);
    }

    pos = consumeWhitespace(input, pos + 1);

    try {
      const element = parseInferredValue(input, pos, frozen);

      // Widen key type
      try {
        const newKeyType = TypeWiden(keyType, element.type);
        if (!isTypeEqual(keyType, newKeyType)) {
          // Type changed - need to rebuild set with new comparator
          const newCompare = compareFor(newKeyType);
          const newValues = new SortedSet(values, newCompare);
          values.clear();
          for (const v of newValues) {
            values.add(v);
          }
          keyType = newKeyType;
        }
      } catch (cause: unknown) {
        if (cause instanceof Error && cause.name === "TypeMismatchError") {
          throw new ParseError(`incompatible set element types: ${cause.message}`, pos, `[${elementIndex}]`);
        }
        throw cause;
      }

      values.add(element.value);
      pos = consumeWhitespace(input, element.position);
    } catch (e) {
      if (e instanceof ParseError) {
        const newPath = `[${elementIndex}]` + (e.path ? e.path : '');
        throw new ParseError(e.message, e.position, newPath);
      }
      throw e;
    }

    elementIndex++;
  }
}

/**
 * Continue parsing a dict after determining it's a dict.
 */
function parseInferredDictRest(
  input: string,
  _startPos: number,
  frozen: boolean,
  firstKey: InferredValue,
  _firstKeyPos: number
): InferredValue {
  let keyType: EastType = firstKey.type;
  let valueType: EastType = NeverType;
  const compare = compareFor(keyType);
  const values = new SortedMap(undefined, compare);

  let pos = consumeWhitespace(input, firstKey.position);

  if (input[pos] !== ':') {
    throw new ParseError("expected ':' after dict key", pos);
  }

  pos = consumeWhitespace(input, pos + 1);

  try {
    const firstValue = parseInferredValue(input, pos, frozen);
    valueType = firstValue.type;
    values.set(firstKey.value, firstValue.value);
    pos = consumeWhitespace(input, firstValue.position);
  } catch (e) {
    if (e instanceof ParseError) {
      const keyPrinter = printFor(keyType);
      const keyStr = keyPrinter(firstKey.value);
      const newPath = `[${keyStr}]` + (e.path ? e.path : '');
      throw new ParseError(e.message, e.position, newPath);
    }
    throw e;
  }

  let entryIndex = 1;

  while (true) {
    if (input[pos] === '}') {
      if (frozen) Object.freeze(values);
      return { type: DictType(keyType, valueType), value: values, position: pos + 1 };
    }

    if (input[pos] !== ',') {
      throw new ParseError("expected ',' or '}' after dict entry", pos);
    }

    pos = consumeWhitespace(input, pos + 1);

    let dictKey: any;
    let dictKeyType: EastType;
    let keyPos: number;

    try {
      const keyElement = parseInferredValue(input, pos, frozen);
      dictKey = keyElement.value;
      dictKeyType = keyElement.type;
      keyPos = pos;
      pos = consumeWhitespace(input, keyElement.position);
    } catch (e) {
      if (e instanceof ParseError) {
        const newPath = `[${entryIndex}](key)` + (e.path ? e.path : '');
        throw new ParseError(e.message, e.position, newPath);
      }
      throw e;
    }

    if (input[pos] !== ':') {
      throw new ParseError("expected ':' after dict key", pos);
    }

    pos = consumeWhitespace(input, pos + 1);

    try {
      const valueElement = parseInferredValue(input, pos, frozen);

      // Widen key and value types
      try {
        const newKeyType = TypeWiden(keyType, dictKeyType);
        const newValueType = TypeWiden(valueType, valueElement.type);

        if (!isTypeEqual(keyType, newKeyType)) {
          // Key type changed - need to rebuild dict with new comparator
          const newCompare = compareFor(newKeyType);
          const newValues = new SortedMap(values, newCompare);
          values.clear();
          for (const [k, v] of newValues) {
            values.set(k, v);
          }
          keyType = newKeyType;
        }

        valueType = newValueType;
      } catch (cause: unknown) {
        if (cause instanceof Error && cause.name === "TypeMismatchError") {
          throw new ParseError(`incompatible dict types: ${cause.message}`, keyPos, `[${entryIndex}]`);
        }
        throw cause;
      }

      values.set(dictKey, valueElement.value);
      pos = consumeWhitespace(input, valueElement.position);
    } catch (e) {
      if (e instanceof ParseError) {
        const keyPrinter = printFor(keyType);
        const keyStr = keyPrinter(dictKey);
        const newPath = `[${keyStr}]` + (e.path ? e.path : '');
        throw new ParseError(e.message, e.position, newPath);
      }
      throw e;
    }

    entryIndex++;
  }
}

/**
 * Parse a struct and infer field types.
 */
function parseInferredStruct(input: string, startPos: number, frozen: boolean): InferredValue {
  let pos = consumeWhitespace(input, startPos);

  if (input[pos] !== '(') {
    throw new ParseError("expected '(' to start struct", pos);
  }

  pos = consumeWhitespace(input, pos + 1);

  const fields: { [key: string]: EastType } = {};
  const values: { [key: string]: any } = {};
  const fieldOrder: string[] = [];

  // Handle empty struct
  if (input[pos] === ')') {
    const struct = frozen ? Object.freeze(values) : values;
    return { type: StructType({}), value: struct, position: pos + 1 };
  }

  while (true) {
    // Parse field name
    const { value: fieldName, position: namePos } = parseIdentifier(input, pos);
    pos = consumeWhitespace(input, namePos);

    if (input[pos] !== '=') {
      throw new ParseError(`expected '=' after field name '${fieldName}'`, pos);
    }

    pos = consumeWhitespace(input, pos + 1);

    // Parse field value and infer type
    const fieldPath = /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(fieldName) ? `.${fieldName}` : `[${JSON.stringify(fieldName)}]`;
    try {
      const fieldValue = parseInferredValue(input, pos, frozen);
      fields[fieldName] = fieldValue.type;
      values[fieldName] = fieldValue.value;
      fieldOrder.push(fieldName);
      pos = consumeWhitespace(input, fieldValue.position);
    } catch (e) {
      if (e instanceof ParseError) {
        const newPath = fieldPath + (e.path ? e.path : '');
        throw new ParseError(e.message, e.position, newPath);
      }
      throw e;
    }

    if (input[pos] === ')') {
      // Reorder fields to match insertion order
      const orderedFields: { [key: string]: EastType } = {};
      for (const name of fieldOrder) {
        orderedFields[name] = fields[name]!;
      }

      const struct = frozen ? Object.freeze(values) : values;
      return { type: StructType(orderedFields), value: struct, position: pos + 1 };
    }

    if (input[pos] !== ',') {
      throw new ParseError("expected ',' or ')' after struct field", pos);
    }

    pos = consumeWhitespace(input, pos + 1);
  }
}

/**
 * Parse a variant and infer the case type.
 */
function parseInferredVariant(input: string, startPos: number, frozen: boolean): InferredValue {
  let pos = consumeWhitespace(input, startPos);

  if (input[pos] !== '.') {
    throw new ParseError("expected '.' to start variant case", pos);
  }

  pos += 1;

  // Check for whitespace after '.'
  const pos2 = consumeWhitespace(input, pos);
  if (pos2 !== pos) {
    throw new ParseError("whitespace not allowed between '.' and case identifier", pos);
  }

  // Parse case name
  const { value: caseName, position: casePos } = parseIdentifier(input, pos);
  pos = consumeWhitespace(input, casePos);

  // Check if there's data following
  let caseType: EastType;
  let caseValue: any;
  let finalPos: number;

  if (isTokenTerminator(input, pos)) {
    // No data - this is a null variant
    caseType = NullType;
    caseValue = null;
    finalPos = pos;
  } else {
    // Parse the associated data
    try {
      const dataResult = parseInferredValue(input, pos, frozen);
      caseType = dataResult.type;
      caseValue = dataResult.value;
      finalPos = dataResult.position;
    } catch (e) {
      if (e instanceof ParseError) {
        const newPath = `.${caseName}` + (e.path ? e.path : '');
        throw new ParseError(e.message, e.position, newPath);
      }
      throw e;
    }
  }

  const v = variant(caseName, caseValue);
  if (frozen) Object.freeze(v);

  return {
    type: VariantType({ [caseName]: caseType }),
    value: v,
    position: finalPos
  };
}
