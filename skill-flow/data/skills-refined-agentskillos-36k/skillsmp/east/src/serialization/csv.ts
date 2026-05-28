/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 *
 * CSV serialization following RFC 4180 (Common Format and MIME Type for CSV Files).
 * @see https://www.rfc-editor.org/rfc/rfc4180
 */

import type { ValueTypeOf, ArrayType } from "../types.js";
import { StructType, OptionType, StringType, BooleanType, ArrayType as ArrayTypeConstructor, DictType } from "../types.js";
import { variant, isVariant } from "../containers/variant.js";
import { SortedMap } from "../containers/sortedmap.js";
import type { EastTypeValue, StructTypeValue, VariantTypeValue } from "../type_of_type.js";
import { isTypeValueEqual, toEastTypeValue } from "../type_of_type.js";

// =============================================================================
// CSV Configuration Types (TypeScript interfaces for user-facing API)
// =============================================================================

/**
 * Configuration options for CSV parsing.
 * All properties are optional with sensible defaults.
 */
export type CsvParseOptions = {
  /** Field delimiter (default: ",") */
  delimiter?: string;
  /** Quote character (default: '"') */
  quoteChar?: string;
  /** Escape character (default: '"' for doubled quotes) */
  escapeChar?: string;
  /** Line ending - auto-detects if not provided */
  newline?: string;
  /** Whether first row is headers (default: true) */
  hasHeader?: boolean;
  /** String values to treat as null (default: [""]) */
  nullStrings?: string[];
  /** Skip rows that are entirely empty (default: true) */
  skipEmptyLines?: boolean;
  /** Trim whitespace from field values (default: false) */
  trimFields?: boolean;
  /** Map CSV headers to struct field names */
  columnMapping?: Map<string, string>;
  /** Error on schema mismatch (default: false) */
  strict?: boolean;
};

/**
 * Configuration options for CSV serialization.
 * All properties are optional with sensible defaults.
 */
export type CsvSerializeOptions = {
  /** Field delimiter (default: ",") */
  delimiter?: string;
  /** Quote character (default: '"') */
  quoteChar?: string;
  /** Escape character (default: '"') */
  escapeChar?: string;
  /** Line ending (default: "\r\n") */
  newline?: string;
  /** Include header row (default: true) */
  includeHeader?: boolean;
  /** String to output for null/none values (default: "") */
  nullString?: string;
  /** Always quote all fields (default: false) */
  alwaysQuote?: boolean;
};

// =============================================================================
// CSV Configuration East Types (for runtime config values)
// =============================================================================

/**
 * East type for CSV parse configuration.
 */
export const CsvParseConfigType = StructType({
  delimiter: OptionType(StringType),
  quoteChar: OptionType(StringType),
  escapeChar: OptionType(StringType),
  newline: OptionType(StringType),
  hasHeader: OptionType(BooleanType),
  nullStrings: OptionType(ArrayTypeConstructor(StringType)),
  skipEmptyLines: OptionType(BooleanType),
  trimFields: OptionType(BooleanType),
  columnMapping: OptionType(DictType(StringType, StringType)),
  strict: OptionType(BooleanType),
});

export type CsvParseConfigType = typeof CsvParseConfigType;

/**
 * East type for CSV serialize configuration.
 */
export const CsvSerializeConfigType = StructType({
  delimiter: OptionType(StringType),
  quoteChar: OptionType(StringType),
  escapeChar: OptionType(StringType),
  newline: OptionType(StringType),
  includeHeader: OptionType(BooleanType),
  nullString: OptionType(StringType),
  alwaysQuote: OptionType(BooleanType),
});

export type CsvSerializeConfigType = typeof CsvSerializeConfigType;

// =============================================================================
// Configuration Conversion Functions
// =============================================================================

/**
 * Converts TypeScript CsvParseOptions to an East config value.
 */
export function csvParseOptionsToValue(options?: CsvParseOptions): ValueTypeOf<CsvParseConfigType> {
  const columnMappingValue = options?.columnMapping
    ? new SortedMap([...options.columnMapping.entries()])
    : undefined;

  return {
    delimiter: options?.delimiter !== undefined ? variant("some", options.delimiter) : variant("none", null),
    quoteChar: options?.quoteChar !== undefined ? variant("some", options.quoteChar) : variant("none", null),
    escapeChar: options?.escapeChar !== undefined ? variant("some", options.escapeChar) : variant("none", null),
    newline: options?.newline !== undefined ? variant("some", options.newline) : variant("none", null),
    hasHeader: options?.hasHeader !== undefined ? variant("some", options.hasHeader) : variant("none", null),
    nullStrings: options?.nullStrings !== undefined ? variant("some", options.nullStrings) : variant("none", null),
    skipEmptyLines: options?.skipEmptyLines !== undefined ? variant("some", options.skipEmptyLines) : variant("none", null),
    trimFields: options?.trimFields !== undefined ? variant("some", options.trimFields) : variant("none", null),
    columnMapping: columnMappingValue !== undefined ? variant("some", columnMappingValue) : variant("none", null),
    strict: options?.strict !== undefined ? variant("some", options.strict) : variant("none", null),
  };
}

/**
 * Converts TypeScript CsvSerializeOptions to an East config value.
 */
export function csvSerializeOptionsToValue(options?: CsvSerializeOptions): ValueTypeOf<CsvSerializeConfigType> {
  return {
    delimiter: options?.delimiter !== undefined ? variant("some", options.delimiter) : variant("none", null),
    quoteChar: options?.quoteChar !== undefined ? variant("some", options.quoteChar) : variant("none", null),
    escapeChar: options?.escapeChar !== undefined ? variant("some", options.escapeChar) : variant("none", null),
    newline: options?.newline !== undefined ? variant("some", options.newline) : variant("none", null),
    includeHeader: options?.includeHeader !== undefined ? variant("some", options.includeHeader) : variant("none", null),
    nullString: options?.nullString !== undefined ? variant("some", options.nullString) : variant("none", null),
    alwaysQuote: options?.alwaysQuote !== undefined ? variant("some", options.alwaysQuote) : variant("none", null),
  };
}

/**
 * Extracts resolved options from an East config value, applying defaults.
 */
export function resolveParseConfig(config: ValueTypeOf<CsvParseConfigType>): Required<Omit<CsvParseOptions, 'columnMapping'>> & { columnMapping: Map<string, string> } {
  return {
    delimiter: config.delimiter.type === "some" ? config.delimiter.value : ",",
    quoteChar: config.quoteChar.type === "some" ? config.quoteChar.value : '"',
    escapeChar: config.escapeChar.type === "some" ? config.escapeChar.value : '"',
    newline: config.newline.type === "some" ? config.newline.value : "",  // empty = auto-detect
    hasHeader: config.hasHeader.type === "some" ? config.hasHeader.value : true,
    nullStrings: config.nullStrings.type === "some" ? config.nullStrings.value : [""],
    skipEmptyLines: config.skipEmptyLines.type === "some" ? config.skipEmptyLines.value : true,
    trimFields: config.trimFields.type === "some" ? config.trimFields.value : false,
    columnMapping: config.columnMapping.type === "some" ? new Map(config.columnMapping.value) : new Map(),
    strict: config.strict.type === "some" ? config.strict.value : false,
  };
}

/**
 * Extracts resolved options from an East config value, applying defaults.
 */
export function resolveSerializeConfig(config: ValueTypeOf<CsvSerializeConfigType>): Required<CsvSerializeOptions> {
  return {
    delimiter: config.delimiter.type === "some" ? config.delimiter.value : ",",
    quoteChar: config.quoteChar.type === "some" ? config.quoteChar.value : '"',
    escapeChar: config.escapeChar.type === "some" ? config.escapeChar.value : '"',
    newline: config.newline.type === "some" ? config.newline.value : "\r\n",
    includeHeader: config.includeHeader.type === "some" ? config.includeHeader.value : true,
    nullString: config.nullString.type === "some" ? config.nullString.value : "",
    alwaysQuote: config.alwaysQuote.type === "some" ? config.alwaysQuote.value : false,
  };
}

// =============================================================================
// CSV Error Types
// =============================================================================

/**
 * Location information for CSV parsing errors.
 */
export interface CsvLocation {
  /** 1-indexed row number (excluding header) */
  row: number;
  /** 0-indexed column index */
  column: number;
  /** Column header name if available */
  columnName?: string;
}

/**
 * Error thrown during CSV parsing with location information.
 */
export class CsvError extends Error {
  constructor(
    message: string,
    public location?: CsvLocation
  ) {
    const locationStr = location
      ? ` at row ${location.row}, column ${location.column}${location.columnName ? ` (${location.columnName})` : ''}`
      : '';
    super(`CSV error: ${message}${locationStr}`);
    this.name = "CsvError";
  }
}

// =============================================================================
// Type Helpers (work with EastTypeValue)
// =============================================================================

/**
 * Check if a type is an OptionType (Variant with exactly 'none' and 'some' cases).
 * Variant cases are sorted alphabetically, so none is at index 0, some at index 1.
 */
function isOptionTypeValue(type: EastTypeValue): type is VariantTypeValue {
  if (type.type !== "Variant") return false;
  return type.value.length === 2 && type.value?.[0]?.name === "none" && type.value?.[1]?.name === "some";
}

/**
 * Get the inner type of an OptionType.
 * Variant cases are sorted alphabetically, so 'some' is at index 1.
 */
function getOptionInnerTypeValue(type: EastTypeValue): EastTypeValue {
  if (type.type !== "Variant") throw new Error("Not an OptionType");
  return type.value?.[1]?.type as EastTypeValue;
}

/**
 * Check if a type is a supported primitive type for CSV fields.
 */
function isSupportedFieldTypeValue(type: EastTypeValue): boolean {
  if (
    isTypeValueEqual(type, variant("Never", null)) ||
    isTypeValueEqual(type, variant("Null", null)) ||
    isTypeValueEqual(type, variant("Boolean", null)) ||
    isTypeValueEqual(type, variant("Integer", null)) ||
    isTypeValueEqual(type, variant("Float", null)) ||
    isTypeValueEqual(type, variant("String", null)) ||
    isTypeValueEqual(type, variant("DateTime", null)) ||
    isTypeValueEqual(type, variant("Blob", null))
  ) {
    // its an literal
    return true
  } else if (isOptionTypeValue(type)) {
    const inner = type.value?.[1]?.type as EastTypeValue
    return isSupportedFieldTypeValue(inner);
  }
  return false;
}

// =============================================================================
// Field Decoders
// =============================================================================

type FieldDecoder = (value: string, location: CsvLocation) => any;

/**
 * Create a decoder for a single field based on its type.
 */
function createFieldDecoder(
  type: EastTypeValue,
  fieldName: string,
  nullStrings: string[],
  trimFields: boolean
): FieldDecoder {
  const isOption = isOptionTypeValue(type);
  const baseType = isOption ? getOptionInnerTypeValue(type) : type;

  return (value: string, location: CsvLocation): any => {
    // Apply trim if configured
    if (trimFields) {
      value = value.trim();
    }

    // Check for null
    if (nullStrings.includes(value)) {
      if (isOption) {
        return variant("none", null);
      } else {
        throw new CsvError(`null value for required field '${fieldName}'`, location);
      }
    }

    // Parse based on type
    let parsed: any;
    try {
      parsed = parseValue(value, baseType, location);
    } catch (e) {
      if (e instanceof CsvError) throw e;
      throw new CsvError(`failed to parse '${value}' as ${baseType.type}: ${e}`, location);
    }

    // Wrap in Option if needed
    if (isOption) {
      return variant("some", parsed);
    }
    return parsed;
  };
}

/**
 * Parse a string value to the given type.
 */
function parseValue(value: string, type: EastTypeValue, location: CsvLocation): any {
  switch (type.type) {
    case "Null":
      if (value !== "" && value !== "null") {
        throw new CsvError(`expected null, got '${value}'`, location);
      }
      return null;

    case "Boolean":
      if (value === "true") return true;
      if (value === "false") return false;
      throw new CsvError(`expected 'true' or 'false', got '${value}'`, location);

    case "Integer": {
      // Handle bigint
      const trimmed = value.trim();
      if (!/^-?\d+$/.test(trimmed)) {
        throw new CsvError(`expected integer, got '${value}'`, location);
      }
      return BigInt(trimmed);
    }

    case "Float": {
      // Handle special values
      if (value === "NaN") return NaN;
      if (value === "Infinity") return Infinity;
      if (value === "-Infinity") return -Infinity;
      if (value === "-0" || value === "-0.0") return -0;

      const num = parseFloat(value);
      if (isNaN(num) && value !== "NaN") {
        throw new CsvError(`expected float, got '${value}'`, location);
      }
      return num;
    }

    case "String":
      return value;

    case "DateTime": {
      // Parse ISO 8601 format
      const date = new Date(value);
      if (isNaN(date.getTime())) {
        throw new CsvError(`expected ISO 8601 date, got '${value}'`, location);
      }
      return date;
    }

    case "Blob": {
      // Parse hex string (0xABCD...)
      if (!value.startsWith("0x")) {
        throw new CsvError(`expected hex string starting with '0x', got '${value}'`, location);
      }
      const hex = value.slice(2);
      if (hex.length % 2 !== 0 || !/^[0-9a-fA-F]*$/.test(hex)) {
        throw new CsvError(`invalid hex string '${value}'`, location);
      }
      const bytes = new Uint8Array(hex.length / 2);
      for (let i = 0; i < bytes.length; i++) {
        bytes[i] = parseInt(hex.substring(i * 2, i * 2 + 2), 16);
      }
      return bytes;
    }

    default:
      throw new CsvError(`unsupported field type ${type.type}`, location);
  }
}

// =============================================================================
// Field Encoders
// =============================================================================

type FieldEncoder = (value: any) => string;

/**
 * Create an encoder for a single field based on its type.
 */
function createFieldEncoder(type: EastTypeValue, nullString: string): FieldEncoder {
  const isOption = isOptionTypeValue(type);
  const baseType = isOption ? getOptionInnerTypeValue(type) : type;

  return (value: any): string => {
    // Handle Option type
    if (isOption) {
      if (value.type === "none") {
        return nullString;
      }
      value = value.value;
    }

    // Handle null
    if (value === null || value === undefined) {
      return nullString;
    }

    return encodeValue(value, baseType);
  };
}

/**
 * Encode a value to a string.
 */
function encodeValue(value: any, type: EastTypeValue): string {
  switch (type.type) {
    case "Null":
      return "";

    case "Boolean":
      return value ? "true" : "false";

    case "Integer":
      return value.toString();

    case "Float":
      if (Number.isNaN(value)) return "NaN";
      if (value === Infinity) return "Infinity";
      if (value === -Infinity) return "-Infinity";
      if (Object.is(value, -0)) return "-0";
      return value.toString();

    case "String":
      return value;

    case "DateTime":
      // ISO 8601 format without timezone suffix
      const d = value as Date;
      const year = d.getUTCFullYear();
      const month = String(d.getUTCMonth() + 1).padStart(2, '0');
      const day = String(d.getUTCDate()).padStart(2, '0');
      const hour = String(d.getUTCHours()).padStart(2, '0');
      const minute = String(d.getUTCMinutes()).padStart(2, '0');
      const second = String(d.getUTCSeconds()).padStart(2, '0');
      const ms = String(d.getUTCMilliseconds()).padStart(3, '0');
      return `${year}-${month}-${day}T${hour}:${minute}:${second}.${ms}`;

    case "Blob":
      // Encode as hex string
      const bytes = value as Uint8Array;
      let hex = "0x";
      for (const byte of bytes) {
        hex += byte.toString(16).padStart(2, '0');
      }
      return hex;

    default:
      throw new Error(`Unsupported field type ${type.type} for CSV encoding`);
  }
}

// =============================================================================
// CSV Parsing
// =============================================================================

/**
 * Parse a CSV row into an array of fields, handling quotes and escapes.
 */
function parseRow(
  blob: Uint8Array,
  offset: number,
  delimiter: string,
  quoteChar: string,
  escapeChar: string
): { fields: string[], newOffset: number, isEnd: boolean } {
  const decoder = new TextDecoder();
  const delimCode = delimiter.charCodeAt(0);
  const quoteCode = quoteChar.charCodeAt(0);
  const escapeCode = escapeChar.charCodeAt(0);

  const fields: string[] = [];
  let inQuote = false;
  let fieldChars: number[] = [];
  let i = offset;

  while (i < blob.length) {
    const byte = blob[i]!;

    if (inQuote) {
      if (byte === escapeCode && i + 1 < blob.length && blob[i + 1]! === quoteCode) {
        // Escaped quote
        fieldChars.push(quoteCode);
        i += 2;
      } else if (byte === quoteCode) {
        // End of quoted field
        inQuote = false;
        i++;
      } else {
        fieldChars.push(byte);
        i++;
      }
    } else {
      if (byte === quoteCode && fieldChars.length === 0) {
        // Start of quoted field
        inQuote = true;
        i++;
      } else if (byte === delimCode) {
        // End of field
        fields.push(decoder.decode(new Uint8Array(fieldChars)));
        fieldChars = [];
        i++;
      } else if (byte === 0x0D) { // CR
        // Check for CRLF
        if (i + 1 < blob.length && blob[i + 1] === 0x0A) {
          fields.push(decoder.decode(new Uint8Array(fieldChars)));
          return { fields, newOffset: i + 2, isEnd: false };
        }
        // Just CR
        fields.push(decoder.decode(new Uint8Array(fieldChars)));
        return { fields, newOffset: i + 1, isEnd: false };
      } else if (byte === 0x0A) { // LF
        fields.push(decoder.decode(new Uint8Array(fieldChars)));
        return { fields, newOffset: i + 1, isEnd: false };
      } else {
        fieldChars.push(byte);
        i++;
      }
    }
  }

  // End of file
  if (inQuote) {
    throw new CsvError("unclosed quote at end of file");
  }

  fields.push(decoder.decode(new Uint8Array(fieldChars)));
  return { fields, newOffset: i, isEnd: true };
}

/**
 * Check if a row is empty (all fields are empty strings).
 * Per RFC 4180, each line should contain the same number of fields,
 * but the skipEmptyLines option allows skipping rows where all fields are empty.
 * This handles blank lines in messy CSV data.
 */
function isEmptyRow(fields: string[]): boolean {
  if (fields.length === 0) return true;
  return fields.every(f => f === "");
}

/**
 * Creates a type-specialized CSV decoder for Array<Struct>.
 *
 * @param structType - The struct type for each row
 * @param config - Configuration as East value (from CsvParseConfigType)
 * @param frozen - Whether to freeze the decoded values
 */
export function decodeCsvFor(structType: EastTypeValue, config?: ValueTypeOf<CsvParseConfigType>, frozen?: boolean): (blob: Uint8Array) => any;
export function decodeCsvFor<T extends StructType>(structType: T, config?: ValueTypeOf<CsvParseConfigType>, frozen?: boolean): (blob: Uint8Array) => ValueTypeOf<ArrayType<T>>;
export function decodeCsvFor(structType: EastTypeValue | StructType, config?: ValueTypeOf<CsvParseConfigType>, frozen?: boolean): (blob: Uint8Array) => any {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(structType)) {
    structType = toEastTypeValue(structType);
  }

  // structType.value is array of { name: string, type: EastTypeValue }
  const fields = (structType as StructTypeValue).value;

  // Validate that all fields are supported types
  for (const { name, type: fieldType } of fields) {
    if (!isSupportedFieldTypeValue(fieldType)) {
      throw new Error(`CSV field '${name}' has unsupported type`);
    }
  }

  // Resolve config with defaults
  const resolved = config ? resolveParseConfig(config) : {
    delimiter: ",",
    quoteChar: '"',
    escapeChar: '"',
    newline: "",
    hasHeader: true,
    nullStrings: [""],
    skipEmptyLines: true,
    trimFields: false,
    columnMapping: new Map<string, string>(),
    strict: false,
  };

  const { delimiter, quoteChar, escapeChar, hasHeader, nullStrings, skipEmptyLines, trimFields, columnMapping, strict } = resolved;

  // Pre-build field info array (like Beast does)
  const fieldInfos = fields.map(({ name, type }) => ({
    name,
    type,
    isOptional: isOptionTypeValue(type),
    decoder: createFieldDecoder(type, name, nullStrings, trimFields),
  }));
  const fieldNames = fieldInfos.map(f => f.name);

  return (blob: Uint8Array): any[] => {
    // Skip UTF-8 BOM if present
    let offset = 0;
    if (blob.length >= 3 && blob[0] === 0xEF && blob[1] === 0xBB && blob[2] === 0xBF) {
      offset = 3;
    }

    // Parse header row
    let headers: string[];
    if (hasHeader) {
      const headerResult = parseRow(blob, offset, delimiter, quoteChar, escapeChar);
      headers = headerResult.fields.map(h => columnMapping.get(h) ?? h);
      offset = headerResult.newOffset;
    } else {
      headers = fieldNames;
    }

    // Build header index lookup
    const headerToIndex = new Map<string, number>();
    for (let i = 0; i < headers.length; i++) {
      headerToIndex.set(headers[i]!, i);
    }

    // Validate: check for missing required fields and extra columns
    for (const { name, isOptional } of fieldInfos) {
      if (!headerToIndex.has(name) && !isOptional) {
        throw new CsvError(`missing required column '${name}'`);
      }
    }
    if (strict) {
      for (const header of headers) {
        if (!fieldNames.includes(header)) {
          throw new CsvError(`unexpected column '${header}' in strict mode`);
        }
      }
    }

    // Build per-field decoder info with header indices
    const decoders = fieldInfos.map(({ name, isOptional, decoder }) => ({
      name,
      isOptional,
      decoder,
      headerIndex: headerToIndex.get(name) ?? null,
    }));

    // Parse data rows
    const result: any[] = [];
    let rowNum = 1;

    while (offset < blob.length) {
      const rowResult = parseRow(blob, offset, delimiter, quoteChar, escapeChar);
      const rowFields = rowResult.fields;
      offset = rowResult.newOffset;

      if (skipEmptyLines && isEmptyRow(rowFields)) {
        if (rowResult.isEnd) break;
        continue;
      }

      // Decode row into struct
      const row: any = {};
      for (const { name, isOptional, decoder, headerIndex } of decoders) {
        if (headerIndex === null) {
          row[name] = variant("none", null);
        } else if (headerIndex >= rowFields.length) {
          if (isOptional) {
            row[name] = variant("none", null);
          } else {
            throw new CsvError(`row has ${rowFields.length} fields, expected at least ${headerIndex + 1}`, { row: rowNum, column: headerIndex, columnName: name });
          }
        } else {
          row[name] = decoder(rowFields[headerIndex]!, { row: rowNum, column: headerIndex, columnName: name });
        }
      }

      if (frozen) Object.freeze(row);
      result.push(row);
      rowNum++;
      if (rowResult.isEnd) break;
    }

    if (frozen) Object.freeze(result);
    return result;
  };
}

// =============================================================================
// CSV Serialization
// =============================================================================

/**
 * Check if a string needs quoting.
 */
function needsQuoting(value: string, delimiter: string, quoteChar: string): boolean {
  return value.includes(delimiter) ||
    value.includes(quoteChar) ||
    value.includes('\r') ||
    value.includes('\n');
}

/**
 * Quote a string value, escaping internal quotes.
 */
function quoteField(value: string, quoteChar: string, escapeChar: string): string {
  const escaped = value.replace(new RegExp(quoteChar, 'g'), escapeChar + quoteChar);
  return quoteChar + escaped + quoteChar;
}

/**
 * Creates a type-specialized CSV encoder for Array<Struct>.
 *
 * @param structType - The struct type for each row
 * @param config - Configuration as East value (from CsvSerializeConfigType)
 */
export function encodeCsvFor(structType: EastTypeValue, config?: ValueTypeOf<CsvSerializeConfigType>): (value: any[]) => Uint8Array;
export function encodeCsvFor<T extends StructType>(structType: T, config?: ValueTypeOf<CsvSerializeConfigType>): (value: ValueTypeOf<ArrayType<T>>) => Uint8Array;
export function encodeCsvFor(structType: EastTypeValue | StructType, config?: ValueTypeOf<CsvSerializeConfigType>): (value: any[]) => Uint8Array {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(structType)) {
    structType = toEastTypeValue(structType);
  }

  const fields = (structType as StructTypeValue).value;

  // Validate that all fields are supported types
  for (const { name, type: fieldType } of fields) {
    if (!isSupportedFieldTypeValue(fieldType)) {
      throw new Error(`CSV field '${name}' has unsupported type`);
    }
  }

  // Resolve config with defaults
  const resolved = config ? resolveSerializeConfig(config) : {
    delimiter: ",",
    quoteChar: '"',
    escapeChar: '"',
    newline: "\r\n",
    includeHeader: true,
    nullString: "",
    alwaysQuote: false,
  };

  const { delimiter, quoteChar, escapeChar, newline, includeHeader, nullString, alwaysQuote } = resolved;

  const fieldNames = fields.map(f => f.name);
  const encoder = new TextEncoder();

  // Create field encoders
  const encoders: FieldEncoder[] = fields.map(({ type }) => createFieldEncoder(type, nullString));

  return (value: any[]): Uint8Array => {
    const lines: string[] = [];

    // Write header
    if (includeHeader) {
      const headerFields = fieldNames.map(name => {
        if (alwaysQuote || needsQuoting(name, delimiter, quoteChar)) {
          return quoteField(name, quoteChar, escapeChar);
        }
        return name;
      });
      lines.push(headerFields.join(delimiter));
    }

    // Write data rows
    for (const row of value) {
      const rowFields: string[] = [];
      for (let i = 0; i < fieldNames.length; i++) {
        const fieldName = fieldNames[i]!;
        const fieldValue = row[fieldName];
        let encoded = encoders[i]!(fieldValue);

        if (alwaysQuote || needsQuoting(encoded, delimiter, quoteChar)) {
          encoded = quoteField(encoded, quoteChar, escapeChar);
        }

        rowFields.push(encoded);
      }
      lines.push(rowFields.join(delimiter));
    }

    return encoder.encode(lines.join(newline));
  };
}
