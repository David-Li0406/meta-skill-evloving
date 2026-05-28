/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { compareFor } from "../comparison.js";
import { SortedMap } from "../containers/sortedmap.js";
import { SortedSet } from "../containers/sortedset.js";
import { EastTypeValueType, toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import type { EastType, ValueTypeOf } from "../types.js";
import { isVariant, variant } from "../containers/variant.js";
import { printFor } from "./east.js";
import { ref } from "../containers/ref.js";

const printTypeValue = printFor(EastTypeValueType) as (type: EastTypeValue) => string;

/**
 * Encodes a JSON Pointer component according to RFC 6901.
 *
 * @param component - The path component to encode
 * @returns The encoded component with ~ and / escaped
 *
 * @remarks
 * Per RFC 6901, '~' is encoded as '~0' and '/' is encoded as '~1'.
 * The order matters: we must escape '~' first to avoid double-escaping.
 */
function _encodeJSONPointerComponent(component: string): string {
  return component.replace(/~/g, '~0').replace(/\//g, '~1');
}

/** Stack of encoders for recursive types */
type JSONEncodeTypeContext = ((value: any, ctx?: JSONEncodeValueContext) => unknown)[];

/**
 * Value-level context for tracking seen mutable containers during JSON encoding.
 *
 * @remarks
 * Tracks mutable containers (Array, Set, Dict) and their path arrays for generating relative references.
 */
type JSONEncodeValueContext = {
  refs: Map<any, string[]>;  // Mutable container -> path array
  currentPath: string[];     // Current position in JSON structure
};

/** Stack of decoders for recursive types */
type JSONDecodeTypeContext = ((json: any, ctx?: JSONDecodeValueContext) => any)[];

/**
 * Value-level context for tracking decoded mutable containers during JSON decoding.
 *
 * @remarks
 * Maps path arrays to decoded mutable containers (Array, Set, Dict) for resolving references.
 * Containers are added to the map BEFORE their contents are populated to handle circular references.
 */
type JSONDecodeValueContext = {
  refs: Map<string, any>;  // Stringified path -> decoded mutable container
  currentPath: string[];   // Current position during traversal
};

class JSONDecodeError extends Error {
  constructor(message: string, public path: string = '') {
    super(message);
    this.name = "JSONDecodeError";
  }
}

/**
 * Find the length of the common prefix between two path arrays.
 */
function _commonPrefixLength(a: string[], b: string[]): number {
  let i = 0;
  while (i < a.length && i < b.length && a[i] === b[i]) {
    i++;
  }
  return i;
}

/**
 * Compute a relative JSON Pointer reference from currentPath to targetPath.
 * Returns a string like "2#foo/bar" (up 2 levels, then follow foo/bar)
 * or "1#" (up 1 level, no remaining path).
 */
function encodeRelativeRef(currentPath: string[], targetPath: string[]): string {
  const commonLen = _commonPrefixLength(currentPath, targetPath);
  const upLevels = currentPath.length - commonLen;
  const remaining = targetPath.slice(commonLen);

  if (remaining.length === 0) {
    return `${upLevels}#`;
  }

  // Escape each component according to RFC 6901
  const escapedRemaining = remaining.map(_encodeJSONPointerComponent).join('/');
  return `${upLevels}#${escapedRemaining}`;
}

/**
 * Decode a relative JSON Pointer reference and return the target path array.
 * Input like "2#foo/bar" returns the target path array.
 * Input like "1#" returns the target path array.
 */
function _decodeRelativeRef(refStr: string, currentPath: string[]): string[] {
  const hashIdx = refStr.indexOf('#');
  if (hashIdx === -1) {
    throw new Error(`Invalid relative JSON Pointer reference: ${refStr}`);
  }

  const upLevelStr = refStr.substring(0, hashIdx);
  const remainingStr = refStr.substring(hashIdx + 1);

  let upLevels: number;
  try {
    upLevels = parseInt(upLevelStr);
  } catch {
    throw new Error(`Invalid relative JSON Pointer reference: ${refStr}`);
  }

  if (upLevels < 0 || upLevels > currentPath.length) {
    throw new Error(`Invalid relative JSON Pointer reference: going up ${upLevels} levels from depth ${currentPath.length}`);
  }

  // Build target path
  const targetPath = currentPath.slice(0, currentPath.length - upLevels);

  // Add remaining components if any
  if (remainingStr.length > 0) {
    const components = remainingStr.split('/');
    for (const component of components) {
      // Decode RFC 6901 escaping
      const unescaped = component.replace(/~1/g, '/').replace(/~0/g, '~');
      targetPath.push(unescaped);
    }
  }

  return targetPath;
}

/**
 * Decode a RFC 6901 JSON Pointer component.
 */
function _decodeJSONPointerComponent(component: string): string {
  return component.replace(/~1/g, '/').replace(/~0/g, '~');
}

export function encodeJSONFor(type: EastTypeValue): (x: any) => Uint8Array
export function encodeJSONFor<T extends EastType>(type: T): (x: ValueTypeOf<T>) => Uint8Array
export function encodeJSONFor(type: EastTypeValue | EastType): (x: any) => Uint8Array {
    // Convert EastType to EastTypeValue if necessary
    if (!isVariant(type)) {
        type = toEastTypeValue(type);
    }

    const textEncoder = new TextEncoder();
    const toJSON = toJSONFor(type as EastTypeValue);
    return (x: any) => textEncoder.encode(JSON.stringify(toJSON(x)));
}

export function decodeJSONFor(type: EastTypeValue, frozen?: boolean): (x: Uint8Array) => any
export function decodeJSONFor<T extends EastType>(type: T, frozen?: boolean): (x: Uint8Array) => ValueTypeOf<T>
export function decodeJSONFor(type: EastTypeValue | EastType, frozen: boolean = false): (x: Uint8Array) => any {
    // Convert EastType to EastTypeValue if necessary
    if (!isVariant(type)) {
        type = toEastTypeValue(type);
    }

    const textDecoder = new TextDecoder();
    const fromJSON = createJSONDecoder(type as EastTypeValue, frozen);
    return (x: Uint8Array) => {
        const jsonString = textDecoder.decode(x);
        let parsed: unknown;
        let _parseError: Error | null = null;
        let line = 1;
        let column = 1;

        try {
            parsed = JSON.parse(jsonString);
        } catch (e) {
            // Extract line and column from JSON.parse error if available
            if (e instanceof SyntaxError) {
                const match = e.message.match(/position (\d+)/);
                if (match) {
                    const position = parseInt(match[1]!);
                    for (let i = 0; i < position && i < jsonString.length; i++) {
                        if (jsonString[i] === '\n') {
                            line++;
                            column = 1;
                        } else {
                            column++;
                        }
                    }
                }
                throw new Error(`Error occurred because ${e.message} (line ${line}, col ${column}) while parsing value of type "${printTypeValue(type as EastTypeValue)}"`);
            }
            throw e;
        }

        try {
            return fromJSON(parsed);
        } catch (e) {
            if (e instanceof JSONDecodeError) {
                const pathStr = e.path ? ` at ${e.path}` : '';
                throw new Error(`Error occurred because ${e.message}${pathStr} (line 1, col 1) while parsing value of type "${printTypeValue(type as EastTypeValue)}"`);
            }
            throw e;
        }
    };
}

/**
 * Creates a JSON encoder function for a given East type.
 *
 * @param type - The East type to create an encoder for
 * @param recursiveContext - Optional context for handling recursive types (internal use)
 * @returns A function that converts East values to JSON-serializable values
 *
 * @remarks
 * The returned function accepts an optional context parameter for tracking object references.
 * When called without a context (the normal case), it operates independently.
 * When called with a context (inside a RecursiveType), it tracks references for aliasing.
 */
export function toJSONFor(type: EastTypeValue, typeCtx?: JSONEncodeTypeContext): (value: any, ctx?: JSONEncodeValueContext) => unknown
export function toJSONFor<T extends EastType>(
    type: T,
    typeCtx?: JSONEncodeTypeContext
): (value: ValueTypeOf<T>, ctx?: JSONEncodeValueContext) => unknown
export function toJSONFor(type: EastType | EastTypeValue, typeCtx: JSONEncodeTypeContext = []): (value: any, ctx?: JSONEncodeValueContext) => unknown {
    // Convert EastType to EastTypeValue if necessary
    if (!isVariant(type)) {
        type = toEastTypeValue(type);
    }

    if (type.type === "Never") {
        return ((_: never, _ctx?: JSONEncodeValueContext) => { throw new Error("Cannot encode Never type to JSON"); }) as any;
    } else if (type.type === "Null") {
        return (_: null, _ctx?: JSONEncodeValueContext) => null;
    } else if (type.type === "Boolean") {
        return (value: boolean, _ctx?: JSONEncodeValueContext) => value;
    } else if (type.type === "Integer") {
        return (value: bigint, _ctx?: JSONEncodeValueContext) => value.toString();
    } else if (type.type === "Float") {
        return (value: number, _ctx?: JSONEncodeValueContext) => {
            // Handle negative zero specially since JSON.parse("-0.0") returns 0
            if (Object.is(value, -0)) {
                return "-0.0";
            }
            return isFinite(value) ? value : value.toString();
        };
    } else if (type.type === "String") {
        return (value: string, _ctx?: JSONEncodeValueContext) => value;
    } else if (type.type === "DateTime") {
        // Encode as RFC 3339 date-time string (see RFC 3339 Section 5.6)
        // Always use UTC timezone (+00:00) for consistency
        return (date: Date, _ctx?: JSONEncodeValueContext) => {
            const year = date.getUTCFullYear();
            const month = (date.getUTCMonth() + 1).toString().padStart(2, '0');
            const day = date.getUTCDate().toString().padStart(2, '0');
            const hour = date.getUTCHours().toString().padStart(2, '0');
            const minute = date.getUTCMinutes().toString().padStart(2, '0');
            const second = date.getUTCSeconds().toString().padStart(2, '0');
            const ms = date.getUTCMilliseconds().toString().padStart(3, '0');

            return `${year}-${month}-${day}T${hour}:${minute}:${second}.${ms}+00:00`;
        }
    } else if (type.type === "Blob") {
        return (value: Uint8Array, _ctx?: JSONEncodeValueContext) => `0x${[...value].map(b => b.toString(16).padStart(2, "0")).join("")}`;
    } else if (type.type === "Ref") {
        let valueToJson: (value: any, ctx?: JSONEncodeValueContext) => unknown;
        const ret = (value: any, ctx: JSONEncodeValueContext = { refs: new Map(), currentPath: [] }) => {
            // Check if this ref was already seen
            if (ctx.refs.has(value)) {
                // Return a relative reference
                const targetPath = ctx.refs.get(value)!;
                const refStr = encodeRelativeRef(ctx.currentPath, targetPath);
                return { "$ref": refStr };
            }

            // First encounter - register the current path array
            ctx.refs.set(value, [...ctx.currentPath]);
            
            // Serialize the referenced value as array of one element
            ctx.currentPath.push("0");
            const result = [ valueToJson(value.value, ctx) ];
            ctx.currentPath.pop();
            return result;
        };
        typeCtx.push(ret);
        valueToJson = toJSONFor(type.value, typeCtx);
        typeCtx.pop();
        return ret;
    } else if (type.type === "Array") {
        let valueToJson: (value: any, ctx?: JSONEncodeValueContext) => unknown;
        const ret = (value: any[], ctx: JSONEncodeValueContext = { refs: new Map(), currentPath: [] }) => {
            // Check if this array was already seen
            if (ctx.refs.has(value)) {
                // Return a relative reference
                const targetPath = ctx.refs.get(value)!;
                const refStr = encodeRelativeRef(ctx.currentPath, targetPath);
                return { "$ref": refStr };
            }

            // First encounter - register the current path array
            ctx.refs.set(value, [...ctx.currentPath]);

            // Serialize array elements
            const result = [];
            for (let i = 0; i < value.length; i++) {
                ctx.currentPath.push(i.toString());
                result.push(valueToJson(value[i], ctx));
                ctx.currentPath.pop();
            }
            return result;
        };
        typeCtx.push(ret);
        valueToJson = toJSONFor(type.value, typeCtx);
        typeCtx.pop();
        return ret;
    } else if (type.type === "Set") {
        const keyToJson = toJSONFor(type.value, typeCtx);
        return (value: Set<any>, ctx?: JSONEncodeValueContext) => {
            // Check if we're tracking references (inside a RecursiveType)
            if (ctx) {
                // Check if this set was already seen
                if (ctx.refs.has(value)) {
                    // Return a relative reference
                    const targetPath = ctx.refs.get(value)!;
                    const refStr = encodeRelativeRef(ctx.currentPath, targetPath);
                    return { "$ref": refStr };
                }

                // First encounter - register the current path array
                ctx.refs.set(value, [...ctx.currentPath]);
            }

            // Serialize set elements
            const arr = [];
            let i = 0;
            for (const v of value) {
                if (ctx) ctx.currentPath.push(i.toString());
                arr.push(keyToJson(v, ctx));
                if (ctx) ctx.currentPath.pop();
                i++;
            }
            return arr;
        };
    } else if (type.type === "Dict") {
        const keyToJson = toJSONFor(type.value.key, typeCtx);
        let valueToJson: (value: any, ctx?: JSONEncodeValueContext) => unknown;
        const ret = (value: Map<any, any>, ctx: JSONEncodeValueContext = { refs: new Map(), currentPath: [] }) => {
            // Check if this dict was already seen
            if (ctx.refs.has(value)) {
                // Return a relative reference
                const targetPath = ctx.refs.get(value)!;
                const refStr = encodeRelativeRef(ctx.currentPath, targetPath);
                return { "$ref": refStr };
            }

            // First encounter - register the current path array
            ctx.refs.set(value, [...ctx.currentPath]);

            // Serialize dict entries
            const arr = [];
            let i = 0;
            for (const [k, v] of value) {
                const entry: any = {};

                // Encode key
                ctx.currentPath.push(i.toString(), "key");
                entry.key = keyToJson(k, ctx);
                ctx.currentPath.pop(); ctx.currentPath.pop();

                // Encode value
                ctx.currentPath.push(i.toString(), "value");
                entry.value = valueToJson(v, ctx);
                ctx.currentPath.pop(); ctx.currentPath.pop();

                arr.push(entry);
                i++;
            }
            return arr;
        };
        typeCtx.push(ret);
        valueToJson = toJSONFor(type.value.value, typeCtx);
        typeCtx.pop();
        return ret;
    } else if (type.type === "Struct") {
        const fieldToJson: { [key: string]: (value: any, ctx?: JSONEncodeValueContext) => unknown } = {};
        const ret = (value: any, ctx: JSONEncodeValueContext = { refs: new Map(), currentPath: [] }) => {
            const obj: any = {};
            for (const k in fieldToJson) {
                ctx.currentPath.push(k);
                obj[k] = fieldToJson[k]!(value[k], ctx);
                ctx.currentPath.pop();
            }
            return obj;
        };
        typeCtx.push(ret);
        for (const { name, type: t } of type.value) {
            fieldToJson[name] = toJSONFor(t, typeCtx);
        }
        typeCtx.pop();
        return ret;
    } else if (type.type === "Variant") {
        const caseToJson: { [key: string]: (value: any, ctx?: JSONEncodeValueContext) => unknown } = {};
        const ret = (value: variant, ctx: JSONEncodeValueContext = { refs: new Map(), currentPath: [] }) => {
            const type = value.type;
            ctx.currentPath.push(type);
            const encodedValue = caseToJson[type]!(value.value, ctx);
            ctx.currentPath.pop();
            return { type, value: encodedValue };
        };
        typeCtx.push(ret);
        for (const { name, type: t } of type.value) {
            caseToJson[name] = toJSONFor(t, typeCtx);
        }
        typeCtx.pop();
        return ret;
    } else if (type.type === "Recursive") {
        const ret = typeCtx[typeCtx.length - Number(type.value)];
        if (ret === undefined) {
            throw new Error(`Internal error: Recursive type context not found`);
        }
        return ret;
    } else if (type.type === "Function") {
        throw new Error(`Cannot encode Function type to JSON`);
    } else if (type.type === "AsyncFunction") {
        throw new Error(`Cannot encode AsyncFunction type to JSON`);
    } else {
        throw new Error(`Unhandled type ${(type satisfies never as any).type} for toJson`);
    }
}

export function fromJSONFor(type: EastTypeValue, frozen?: boolean): (value: unknown) => any
export function fromJSONFor<T extends EastType>(type: T, frozen?: boolean): (value: unknown) => ValueTypeOf<T>
export function fromJSONFor(type: EastTypeValue, frozen: boolean = false): (value: unknown) => any {
    // Convert EastType to EastTypeValue if necessary
    if (!isVariant(type)) {
        type = toEastTypeValue(type);
    }

    const decoder = createJSONDecoder(type, frozen);
    const typeName = printTypeValue(type);
    return (value: unknown) => {
        try {
            return decoder(value);
        } catch (e) {
            if (e instanceof JSONDecodeError) {
                const pathStr = e.path ? ` at ${e.path}` : '';
                throw new Error(`Error occurred because ${e.message}${pathStr} (line 1, col 1) while parsing value of type "${typeName}"`);
            }
            throw e;
        }
    };
}

/**
 * Creates a JSON decoder function for a given East type.
 *
 * @param type - The East type to create a decoder for
 * @param frozen - Whether to freeze decoded objects
 * @param recursiveContext - Optional context for handling recursive types (internal use)
 * @returns A function that converts JSON values to East values
 *
 * @remarks
 * The returned function accepts an optional context parameter for resolving references.
 * When called without a context (the normal case), it operates independently.
 * When called with a context (inside a RecursiveType), it resolves `$ref` references.
 */
function createJSONDecoder(
    type: EastTypeValue,
    frozen: boolean = false,
    typeCtx: JSONDecodeTypeContext = []
): (value: unknown, ctx?: JSONDecodeValueContext) => any {
    if (type.type === "Never") {
        return ((_: never, _ctx?: JSONDecodeValueContext) => { throw new Error("Cannot decode Never type from JSON"); }) as any;
    } else if (type.type === "Null") {
        return (value: unknown, _ctx?: JSONDecodeValueContext) => {
            if (value !== null) {
                throw new JSONDecodeError(`expected null, got ${JSON.stringify(value)}`);
            }
            return null;
        }
    } else if (type.type === "Boolean") {
        return (value: unknown, _ctx?: JSONDecodeValueContext) => {
            if (typeof value !== "boolean") {
                throw new JSONDecodeError(`expected boolean, got ${JSON.stringify(value)}`);
            }
            return value;
        }
    } else if (type.type === "Integer") {
        return (value: unknown, _ctx?: JSONDecodeValueContext) => {
            if (typeof value === "string" && value.length > 0) {
                let bigint: bigint;
                try {
                    bigint = BigInt(value);
                } catch {
                    throw new JSONDecodeError(`expected string representing integer, got ${JSON.stringify(value)}`);
                }
                // Check for 64-bit signed integer range: -2^63 to 2^63-1
                if (bigint < -9223372036854775808n || bigint > 9223372036854775807n) {
                    throw new JSONDecodeError(`integer out of range (must be 64-bit signed), got ${JSON.stringify(value)}`);
                }
                return bigint;
            } else {
                throw new JSONDecodeError(`expected string representing integer, got ${JSON.stringify(value)}`);
            }
        }
    } else if (type.type === "Float") {
        return (value: unknown, _ctx?: JSONDecodeValueContext) => {
            if (typeof value === "number") {
                return value;
            } else if (value === "-0.0") {
                return -0.0;
            } else if (value === "NaN") {
                return NaN;
            } else if (value === "Infinity") {
                return Infinity;
            } else if (value === "-Infinity") {
                return -Infinity;
            } else {
                throw new JSONDecodeError(`expected number or string representing special float value, got ${JSON.stringify(value)}`);
            }
        }
    } else if (type.type === "String") {
        return (value: unknown, _ctx?: JSONDecodeValueContext) => {
            if (typeof value !== "string") {
                throw new JSONDecodeError(`expected string, got ${JSON.stringify(value)}`);
            }
            return value;
        }
    } else if (type.type === "DateTime") {
        return (value: unknown, _ctx?: JSONDecodeValueContext) => {
            if (typeof value !== "string") {
                throw new JSONDecodeError(`expected string for DateTime, got ${JSON.stringify(value)}`);
            }
            // Require RFC 3339 date-time format with timezone (see RFC 3339 Section 5.6)
            // Per RFC 3339 Section 4.3, "unqualified local time" is unacceptable for interchange
            // Timezone must be either 'Z' (UTC) or numeric offset (e.g., '+05:00' or '-08:00')
            // Format: YYYY-MM-DDTHH:mm:ss.sss(Z|±HH:mm)
            const iso8601WithTimezone = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}(Z|[+-]\d{2}:\d{2})$/;
            if (!iso8601WithTimezone.test(value)) {
                throw new JSONDecodeError(`expected ISO 8601 date string with timezone (e.g. "2022-06-29T13:43:00.123Z" or "2022-06-29T13:43:00.123+05:00"), got ${JSON.stringify(value)}`);
            }
            const date = new Date(value);
            if (isNaN(date.getTime())) {
                throw new JSONDecodeError(`invalid date string, got ${JSON.stringify(value)}`);
            }
            if (frozen) {
                Object.freeze(date);
            }
            return date;
        }
    } else if (type.type === "Blob") {
        return (value: unknown, _ctx?: JSONDecodeValueContext) => {
            if (typeof value !== "string" || !value.startsWith("0x")) {
                throw new JSONDecodeError(`expected hex string starting with 0x, got ${JSON.stringify(value)}`);
            }
            const hex = value.slice(2);
            if (hex.length % 2 !== 0 || !/^[0-9a-fA-F]*$/.test(hex)) {
                throw new JSONDecodeError(`invalid hex string, got ${JSON.stringify(value)}`);
            }
            const bytes = new Uint8Array(hex.length / 2);
            for (let i = 0; i < bytes.length; i++) {
                bytes[i] = parseInt(hex.substring(i * 2, i * 2 + 2), 16);
            }
            if (frozen) {
                Object.freeze(bytes);
            }
            return bytes;
        }
    } else if (type.type === "Ref") {
        let valueFromJson: (value: unknown, ctx?: JSONDecodeValueContext) => any;
        const ret = (json: unknown, ctx: JSONDecodeValueContext = { refs: new Map(), currentPath: [] }) => {
            // Check for reference first (must appear before refs)
            if (json && typeof json === 'object' && "$ref" in json && Object.keys(json).length === 1) {
                const refStr = (json as any)["$ref"];
                if (typeof refStr === 'string') {
                    try {
                        const targetPath = _decodeRelativeRef(refStr, ctx.currentPath);
                        const pathKey = "/" + targetPath.map(_encodeJSONPointerComponent).join("/");
                        if (!ctx.refs.has(pathKey)) {
                            throw new JSONDecodeError(`undefined reference ${refStr}`);
                        }
                        return ctx.refs.get(pathKey);
                    } catch (e) {
                        if (e instanceof JSONDecodeError) {
                            throw e;
                        }
                        throw new JSONDecodeError(`invalid reference ${refStr}`);
                    }
                }
            }

            if (!Array.isArray(json) || json.length !== 1) {
                throw new JSONDecodeError(`expected array with 1 entry, got ${JSON.stringify(json)}`);
            }

            // Create array and pre-register (for circular references)
            const self: ref<any> = ref(undefined);
            const pathKey = "/" + ctx.currentPath.map(_encodeJSONPointerComponent).join("/");
            ctx.refs.set(pathKey, self);

            // Populate reference
            self.value = valueFromJson(json[0], ctx);
            if (frozen) {
                Object.freeze(self);
            }
            return self;
        };
        typeCtx.push(ret);
        valueFromJson = createJSONDecoder(type.value, frozen, typeCtx);
        typeCtx.pop();
        return ret;
    } else if (type.type === "Array") {
        let valueFromJson: (value: unknown, ctx?: JSONDecodeValueContext) => any;
        const ret = (json: unknown, ctx: JSONDecodeValueContext = { refs: new Map(), currentPath: [] }) => {
            // Check for reference first (must appear before refs)
            if (json && typeof json === 'object' && "$ref" in json && Object.keys(json).length === 1) {
                const refStr = (json as any)["$ref"];
                if (typeof refStr === 'string') {
                    try {
                        const targetPath = _decodeRelativeRef(refStr, ctx.currentPath);
                        const pathKey = "/" + targetPath.map(_encodeJSONPointerComponent).join("/");
                        if (!ctx.refs.has(pathKey)) {
                            throw new JSONDecodeError(`undefined reference ${refStr}`);
                        }
                        return ctx.refs.get(pathKey);
                    } catch (e) {
                        if (e instanceof JSONDecodeError) {
                            throw e;
                        }
                        throw new JSONDecodeError(`invalid reference ${refStr}`);
                    }
                }
            }

            if (!Array.isArray(json)) {
                throw new JSONDecodeError(`expected array, got ${JSON.stringify(json)}`);
            }

            // Create array and pre-register (for circular references)
            const array: any[] = [];
            const pathKey = "/" + ctx.currentPath.map(_encodeJSONPointerComponent).join("/");
            ctx.refs.set(pathKey, array);

            // Populate array
            for (let i = 0; i < json.length; i++) {
                ctx.currentPath.push(i.toString());
                try {
                    array.push(valueFromJson(json[i], ctx));
                } catch (e) {
                    if (e instanceof JSONDecodeError) {
                        const newPath = `[${i}]` + (e.path ? e.path : '');
                        throw new JSONDecodeError(e.message, newPath);
                    }
                    throw e;
                }
                ctx.currentPath.pop();
            }

            if (frozen) {
                Object.freeze(array);
            }
            return array;
        };
        typeCtx.push(ret);
        valueFromJson = createJSONDecoder(type.value, frozen, typeCtx);
        typeCtx.pop();
        return ret;
    } else if (type.type === "Set") {
        const keyFromJson = createJSONDecoder(type.value, frozen, typeCtx);
        const compare = compareFor(type.value);
        return (json: unknown, ctx?: JSONDecodeValueContext) => {
            // Check for reference first
            if (ctx && json && typeof json === 'object' && "$ref" in json && Object.keys(json).length === 1) {
                const refStr = (json as any)["$ref"];
                if (typeof refStr === 'string') {
                    try {
                        const targetPath = _decodeRelativeRef(refStr, ctx.currentPath);
                        const pathKey = "/" + targetPath.map(_encodeJSONPointerComponent).join("/");
                        if (!ctx.refs.has(pathKey)) {
                            throw new JSONDecodeError(`undefined reference ${refStr}`);
                        }
                        return ctx.refs.get(pathKey);
                    } catch (e) {
                        if (e instanceof JSONDecodeError) {
                            throw e;
                        }
                        throw new JSONDecodeError(`invalid reference ${refStr}`);
                    }
                }
            }

            if (!Array.isArray(json)) {
                throw new JSONDecodeError(`expected array for Set, got ${JSON.stringify(json)}`);
            }

            // Create set and pre-register
            const set = new SortedSet<any>([], compare);
            if (ctx) {
                const pathKey = "/" + ctx.currentPath.map(_encodeJSONPointerComponent).join("/");
                ctx.refs.set(pathKey, set);
            }

            // Populate set
            for (let i = 0; i < json.length; i++) {
                if (ctx) ctx.currentPath.push(i.toString());
                try {
                    set.add(keyFromJson(json[i], ctx));
                } catch (e) {
                    if (e instanceof JSONDecodeError) {
                        const newPath = `[${i}]` + (e.path ? e.path : '');
                        throw new JSONDecodeError(e.message, newPath);
                    }
                    throw e;
                }
                if (ctx) ctx.currentPath.pop();
            }

            if (frozen) {
                Object.freeze(set);
            }
            return set;
        }
    } else if (type.type === "Dict") {
        const keyFromJson = createJSONDecoder(type.value.key, frozen, typeCtx);
        let valueFromJson: (value: unknown, ctx?: JSONDecodeValueContext) => any;
        const compare = compareFor(type.value.key);
        const ret = (json: unknown, ctx: JSONDecodeValueContext = { refs: new Map(), currentPath: [] }) => {
            // Check for reference first
            if (json && typeof json === 'object' && "$ref" in json && Object.keys(json).length === 1) {
                const refStr = (json as any)["$ref"];
                if (typeof refStr === 'string') {
                    try {
                        const targetPath = _decodeRelativeRef(refStr, ctx.currentPath);
                        const pathKey = "/" + targetPath.map(_encodeJSONPointerComponent).join("/");
                        if (!ctx.refs.has(pathKey)) {
                            throw new JSONDecodeError(`undefined reference ${refStr}`);
                        }
                        return ctx.refs.get(pathKey);
                    } catch (e) {
                        if (e instanceof JSONDecodeError) {
                            throw e;
                        }
                        throw new JSONDecodeError(`invalid reference ${refStr}`);
                    }
                }
            }

            if (!Array.isArray(json)) {
                throw new JSONDecodeError(`expected array for Dict, got ${JSON.stringify(json)}`);
            }

            // Create dict and pre-register (for circular references)
            const dict = new SortedMap<any, any>([], compare);
            const pathKey = "/" + ctx.currentPath.map(_encodeJSONPointerComponent).join("/");
            ctx.refs.set(pathKey, dict);

            // Populate dict
            for (let i = 0; i < json.length; i++) {
                const item = json[i];
                if (typeof item !== "object" || item === null || !("key" in item) || !("value" in item)) {
                    throw new JSONDecodeError(`expected object with key and value for Dict entry, got ${JSON.stringify(item)}`, `[${i}]`);
                }
                // Check for extra fields in dict entry
                for (const k in item) {
                    if (k !== "key" && k !== "value") {
                        throw new JSONDecodeError(`unexpected field "${k}" in Dict entry, got ${JSON.stringify(item)}`, `[${i}]`);
                    }
                }

                let dictKey: any;
                ctx.currentPath.push(i.toString(), "key");
                try {
                    dictKey = keyFromJson((item as any).key, ctx);
                } catch (e) {
                    if (e instanceof JSONDecodeError) {
                        const newPath = `[${i}].key` + (e.path ? e.path : '');
                        throw new JSONDecodeError(e.message, newPath);
                    }
                    throw e;
                }
                ctx.currentPath.pop();

                ctx.currentPath.push("value");
                try {
                    const dictValue = valueFromJson((item as any).value, ctx);
                    dict.set(dictKey, dictValue);
                } catch (e) {
                    if (e instanceof JSONDecodeError) {
                        const newPath = `[${i}].value` + (e.path ? e.path : '');
                        throw new JSONDecodeError(e.message, newPath);
                    }
                    throw e;
                }
                ctx.currentPath.pop();
                ctx.currentPath.pop();
            }

            if (frozen) {
                Object.freeze(dict);
            }
            return dict;
        };
        typeCtx.push(ret);
        valueFromJson = createJSONDecoder(type.value.value, frozen, typeCtx);
        typeCtx.pop();
        return ret;
    } else if (type.type === "Struct") {
        const fieldFromJson: { [key: string]: (value: any, ctx?: JSONDecodeValueContext) => any } = {};
        const ret = (json: unknown, ctx: JSONDecodeValueContext = { refs: new Map(), currentPath: [] }) => {
            if (typeof json !== "object" || json === null) {
                throw new JSONDecodeError(`expected object for Struct, got ${JSON.stringify(json)}`);
            }
            // Check for extra fields
            for (const k in (json as any)) {
                if (!(k in fieldFromJson)) {
                    throw new JSONDecodeError(`unexpected field "${k}" in Struct, got ${JSON.stringify(json)}`);
                }
            }

            // Create struct
            const obj: any = {};

            // Populate fields
            for (const k in fieldFromJson) {
                if (!(k in (json as any))) {
                    throw new JSONDecodeError(`missing field "${k}" in Struct, got ${JSON.stringify(json)}`);
                }
                ctx.currentPath.push(k);
                try {
                    obj[k] = fieldFromJson[k]!((json as any)[k], ctx);
                } catch (e) {
                    if (e instanceof JSONDecodeError) {
                        const newPath = `.${k}` + (e.path ? e.path : '');
                        throw new JSONDecodeError(e.message, newPath);
                    }
                    throw e;
                }
                ctx.currentPath.pop();
            }

            if (frozen) {
                Object.freeze(obj); // is this overkill?
            }
            return obj;
        };
        typeCtx.push(ret);
        for (const { name, type: t } of type.value) {
            fieldFromJson[name] = createJSONDecoder(t, frozen, typeCtx);
        }
        typeCtx.pop();
        return ret;
    } else if (type.type === "Variant") {
        const caseFromJson: { [key: string]: ((value: any, ctx?: JSONDecodeValueContext) => any) | null } = {} as any;
        const ret = (json: unknown, ctx: JSONDecodeValueContext = { refs: new Map(), currentPath: [] }) => {
            if (typeof json !== "object" || json === null || !("type" in json) || !("value" in json)) {
                throw new JSONDecodeError(`expected object with type and value for Variant, got ${JSON.stringify(json)}`);
            }
            const typeStr = (json as any).type;
            if (!(typeStr in caseFromJson)) {
                throw new JSONDecodeError(`unknown variant type "${typeStr}", got ${JSON.stringify(json)}`);
            }
            const caseFn = caseFromJson[typeStr]!;

            // Create variant with undefined placeholder
            const v = variant(typeStr, undefined);

            // Decode the value
            ctx.currentPath.push(typeStr);
            try {
                const variantValue = caseFn((json as any).value, ctx);
                // Mutate the variant's value field
                (v as any).value = variantValue;
                if (frozen) {
                    Object.freeze(v);
                }
                return v;
            } catch (e) {
                if (e instanceof JSONDecodeError) {
                    const newPath = `.${typeStr}` + (e.path ? e.path : '');
                    throw new JSONDecodeError(e.message, newPath);
                }
                throw e;
            } finally {
                ctx.currentPath.pop();
            }
        };
        typeCtx.push(ret);
        for (const { name, type: t } of type.value) {
            caseFromJson[name] = createJSONDecoder(t, frozen, typeCtx);
        }
        typeCtx.pop();
        return ret;
    } else if (type.type === "Recursive") {
        const ret = typeCtx[typeCtx.length - Number(type.value)];
        if (ret === undefined) {
            throw new Error(`Internal error: Recursive type context not found`);
        }
        return ret;
    } else if (type.type === "Function") {
        throw new Error(`Cannot decode Function type from JSON`);
    } else if (type.type === "AsyncFunction") {
        throw new Error(`Cannot decode AsyncFunction type from JSON`);
    } else {
        throw new Error(`Unhandled type ${(type satisfies never as any).type} for fromJson`);
    }
}