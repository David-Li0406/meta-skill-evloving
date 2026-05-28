/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Data structure and path types for e3.
 *
 * Terminology:
 * - **Dataset**: A location holding a value (leaf node in the data tree)
 * - **Tree**: A location containing datasets or nested trees (branch node)
 * - **Structure**: The shape of the data tree (what trees/datasets exist and their types)
 * - **Path**: An address pointing to a dataset or tree
 *
 * Paths use East's keypath syntax:
 * - `.field` for struct field access (backtick-quoted for special chars)
 * - `[N]` for array index access (future)
 * - `[key]` for dict key lookup (future)
 *
 * @see East serialization docs for keypath syntax details
 */

import { VariantType, StringType, ArrayType, DictType, RecursiveType, ValueTypeOf, printIdentifier, variant, EastTypeType } from '@elaraai/east';

/**
 * Structure definition for a data tree node.
 *
 * Defines the shape of the data tree - which paths are datasets (hold values)
 * and which are trees (hold other nodes).
 *
 * @remarks
 * - `value`: A dataset - holds a typed value. The type is an `EastTypeValue`.
 * - `struct`: A tree - has named children, each with its own structure.
 *
 * MVP only supports struct trees. Future: array, dict, variant trees.
 *
 * @example
 * ```ts
 * // A dataset holding an Integer value
 * const dataset: Structure = variant('value', variant('Integer', null));
 *
 * // A tree with named children
 * const tree: Structure = variant('struct', new Map([
 *   ['count', variant('value', variant('Integer', null))],
 *   ['items', variant('value', variant('Array', variant('String', null)))],
 * ]));
 * ```
 */
export const StructureType = RecursiveType(self => VariantType({
  /** Dataset: East type of the value (homoiconic EastTypeValue) */
  value: EastTypeType,
  /** Struct tree: named children mapping to child structures */
  struct: DictType(StringType, self),
}));
export type StructureType = typeof StructureType;

export type Structure = ValueTypeOf<typeof StructureType>;

// Backwards compatibility alias
/** @deprecated Use StructureType instead */
export const DatasetSchemaType = StructureType;
/** @deprecated Use Structure instead */
export type DatasetSchemaType = StructureType;
/** @deprecated Use Structure instead */
export type DatasetSchema = Structure;

/**
 * Path segment for navigating data trees.
 *
 * Uses East keypath syntax for consistency:
 * - `field`: Struct field access (rendered as `.field` or `` .`field` `` if quoted)
 * - `index`: Array element access (rendered as `[N]`) - future
 * - `key`: Dict key lookup (rendered as `[key]`) - future
 *
 * @example
 * ```ts
 * // Struct field access
 * const segment: PathSegment = variant('field', 'sales');
 *
 * // Array index (future)
 * const segment: PathSegment = variant('index', 0n);
 * ```
 */
export const PathSegmentType = VariantType({
  /** Struct field access by name */
  field: StringType,
  // Future: case: StringType for variant case identifiers
  // Future: index: IntegerType for array access
  // Future: key: StringType (or polymorphic) for dict access
});
export type PathSegmentType = typeof PathSegmentType;

export type PathSegment = ValueTypeOf<typeof PathSegmentType>;

/**
 * Path: sequence of segments identifying a location in a data tree.
 *
 * Paths point to either a dataset (leaf) or a tree (branch).
 * Used by tasks to specify where inputs come from and where outputs go.
 *
 * @example
 * ```ts
 * // Path to .inputs.sales.data
 * const path: TreePath = [
 *   variant('field', 'inputs'),
 *   variant('field', 'sales'),
 *   variant('field', 'data'),
 * ];
 * ```
 */
export const TreePathType = ArrayType(PathSegmentType);
export type TreePathType = typeof TreePathType;

export type TreePath = ValueTypeOf<typeof TreePathType>;

/**
 * Converts a path to East keypath string representation.
 *
 * Uses East's keypath syntax: `.field` for simple identifiers,
 * `` .`field` `` for identifiers needing quoting.
 *
 * @param path - The path to convert
 * @returns A keypath string (e.g., ".inputs.sales" or ".inputs.`my/field`")
 *
 * @example
 * ```ts
 * const path = treePath('inputs', 'sales');
 * pathToString(path); // ".inputs.sales"
 *
 * const path2 = treePath('inputs', 'my/field');
 * pathToString(path2); // ".inputs.`my/field`"
 * ```
 */
export function pathToString(path: TreePath): string {
  return path.map(segment => {
    if (segment.type === 'field') {
      return '.' + printIdentifier(segment.value);
    } else {
      throw new Error(`pathToString: unsupported path segment type: ${segment.type}`);
    }
  }).join('');
}

/**
 * Result of parsing a path with structure validation.
 */
export interface ParsePathResult {
  /** The parsed path segments */
  path: TreePath;
  /** The structure at the path location */
  structure: Structure;
}

/**
 * Parses an East keypath string into a path, validating against the structure.
 *
 * Supports `.field` syntax for struct field access.
 * Backtick-quoted identifiers (`` .`field` ``) are supported for special chars.
 *
 * @param pathStr - A keypath string (e.g., ".inputs.sales")
 * @param structure - The root structure to validate against
 * @returns The parsed path and the structure at that location
 *
 * @throws {Error} If a field doesn't exist in the structure or path descends into a dataset
 *
 * @remarks
 * - Empty string returns empty path (root) with the root structure
 * - Path must start with `.` (no leading slash)
 * - Backtick escaping: `` \` `` for literal backtick, `\\` for backslash
 * - Future: will disambiguate variant cases from struct fields using structure
 * - Future: will use structure to parse dict keys with correct type
 *
 * @example
 * ```ts
 * const structure = variant('struct', new Map([
 *   ['inputs', variant('struct', new Map([
 *     ['sales', variant('value', variant('Integer', null))],
 *   ]))],
 * ]));
 *
 * const { path, structure: leafStructure } = parsePath('.inputs.sales', structure);
 * // path = [field('inputs'), field('sales')]
 * // leafStructure = variant('value', variant('Integer', null))
 * ```
 */
export function parsePath(pathStr: string, structure: Structure): ParsePathResult {
  if (pathStr === '') return { path: [], structure };

  const segments: TreePath = [];
  let currentStructure = structure;
  let pos = 0;

  while (pos < pathStr.length) {
    if (pathStr[pos] === '.') {
      pos++;

      // Parse identifier (TODO: export parseIdentifier from east package)
      let fieldName: string;

      // Check for backtick-quoted identifier
      if (pos < pathStr.length && pathStr[pos] === '`') {
        pos++;
        fieldName = '';
        while (pos < pathStr.length && pathStr[pos] !== '`') {
          if (pathStr[pos] === '\\' && pos + 1 < pathStr.length) {
            // Escape sequence
            pos++;
            fieldName += pathStr[pos];
          } else {
            fieldName += pathStr[pos];
          }
          pos++;
        }
        if (pos < pathStr.length && pathStr[pos] === '`') {
          pos++; // consume closing backtick
        }
      } else {
        // Simple identifier: [a-zA-Z_][a-zA-Z0-9_]*
        fieldName = '';
        while (pos < pathStr.length && /[a-zA-Z0-9_]/.test(pathStr[pos]!)) {
          fieldName += pathStr[pos];
          pos++;
        }
      }

      if (fieldName.length === 0) {
        throw new Error(`parsePath: expected identifier after '.' at position ${pos}`);
      }

      // Validate against structure
      if (currentStructure.type === 'value') {
        throw new Error(`parsePath: cannot descend into dataset at '${pathToString(segments)}'`);
      }

      // currentStructure.type === 'struct' (only other option after 'value' check)
      const fields = currentStructure.value;
      const childStructure = fields.get(fieldName);
      if (childStructure === undefined) {
        const available = [...fields.keys()].map(k => printIdentifier(k)).join(', ');
        throw new Error(`parsePath: field '${fieldName}' not found at '${pathToString(segments)}'. Available: ${available}`);
      }
      segments.push(variant('field', fieldName));
      currentStructure = childStructure;
    } else {
      throw new Error(`parsePath: unexpected character at position ${pos}: '${pathStr[pos]}'`);
    }
  }

  return { path: segments, structure: currentStructure };
}

/**
 * Creates a path from field names, validating against the structure.
 *
 * Convenience function for the common case of navigating through struct fields.
 *
 * @param structure - The root structure to validate against
 * @param fields - Field names to include in the path
 * @returns The parsed path and the structure at that location
 *
 * @throws {Error} If a field doesn't exist in the structure
 *
 * @example
 * ```ts
 * const { path, structure: leafStructure } = treePath(rootStructure, 'inputs', 'sales');
 * ```
 */
export function treePath(structure: Structure, ...fields: string[]): ParsePathResult {
  return parsePath('.' + fields.map(printIdentifier).join('.'), structure);
}

/**
 * Result of parsing a dataset path specification.
 */
export interface ParseDatasetPathResult {
  /** Workspace name */
  ws: string;
  /** Path within the workspace */
  path: TreePath;
}

/**
 * Parse workspace.path.to.dataset syntax into workspace name and TreePath.
 *
 * This is a lenient parser that does not validate against a structure.
 * Use this for parsing user input where the structure is not yet known.
 *
 * @param pathSpec - Path specification in dot notation (e.g., "production.inputs.sales")
 * @returns Workspace name and path segments
 *
 * @throws {Error} If path is empty or has unclosed backticks
 *
 * @example
 * ```ts
 * parseDatasetPath("production")
 * // { ws: "production", path: [] }
 *
 * parseDatasetPath("production.inputs.sales")
 * // { ws: "production", path: [field("inputs"), field("sales")] }
 *
 * // For field names with special characters, use backticks:
 * parseDatasetPath("production.`my field`")
 * // { ws: "production", path: [field("my field")] }
 * ```
 */
export function parseDatasetPath(pathSpec: string): ParseDatasetPathResult {
  const segments = parsePathSegments(pathSpec);

  if (segments.length === 0) {
    throw new Error('Path cannot be empty');
  }

  const ws = segments[0]!;
  const path: TreePath = segments.slice(1).map((s) => variant('field', s));

  return { ws, path };
}

/**
 * Parse dot-separated path into segments, handling backtick-quoted identifiers.
 * @internal
 */
function parsePathSegments(pathSpec: string): string[] {
  const segments: string[] = [];
  let current = '';
  let inBackticks = false;

  for (let i = 0; i < pathSpec.length; i++) {
    const char = pathSpec[i];

    if (char === '`') {
      inBackticks = !inBackticks;
    } else if (char === '.' && !inBackticks) {
      if (current.length > 0) {
        segments.push(current);
        current = '';
      }
    } else {
      current += char;
    }
  }

  if (current.length > 0) {
    segments.push(current);
  }

  if (inBackticks) {
    throw new Error('Unclosed backtick in path');
  }

  return segments;
}

/**
 * Result of parsing a package reference.
 */
export interface ParsePackageRefResult {
  /** Package name */
  name: string;
  /** Version string, or undefined if not specified */
  version?: string;
}

/**
 * Parse a package reference like "name" or "name@version".
 *
 * @param ref - Package reference string
 * @returns Package name and optional version
 *
 * @example
 * ```ts
 * parsePackageRef("my-package")
 * // { name: "my-package", version: undefined }
 *
 * parsePackageRef("my-package@1.0.0")
 * // { name: "my-package", version: "1.0.0" }
 *
 * // Scoped packages work too:
 * parsePackageRef("@scope/package@2.0.0")
 * // { name: "@scope/package", version: "2.0.0" }
 * ```
 */
export function parsePackageRef(ref: string): ParsePackageRefResult {
  const atIdx = ref.lastIndexOf('@');
  // Handle scoped packages like @scope/name - only split on @ after position 0
  if (atIdx > 0) {
    return {
      name: ref.slice(0, atIdx),
      version: ref.slice(atIdx + 1),
    };
  }
  return { name: ref };
}

/**
 * Convert URL path segments to a TreePath.
 *
 * Takes slash-separated, URL-encoded path segments and converts them to
 * a TreePath of field variants.
 *
 * @param urlPath - URL path string (e.g., "inputs/sales/data" or "/inputs/sales/data")
 * @returns TreePath of field segments
 *
 * @example
 * ```ts
 * urlPathToTreePath("inputs/sales/data")
 * // [field("inputs"), field("sales"), field("data")]
 *
 * urlPathToTreePath("inputs/my%20field")
 * // [field("inputs"), field("my field")]
 *
 * urlPathToTreePath("")
 * // []
 * ```
 */
export function urlPathToTreePath(urlPath: string): TreePath {
  const segments = urlPath.split('/').filter(p => p);
  return segments.map(segment => variant('field', decodeURIComponent(segment)));
}
