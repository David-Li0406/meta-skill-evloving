/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 *
 * @remarks
 */
export type Location = {
  /** The source file path */
  filename: string,
  /** The 1-based line number */
  line: number,
  /** The 1-based column number */
  column: number,
}

/**
 * Formats a single location as a human-readable string.
 *
 * @param location - The source location to format
 * @returns A string in the format `"<filename> <line>:<column>"`
 *
 * @example
 * ```ts
 * const loc = { filename: "main.ts", line: 42, column: 15 };
 * printLocation(loc); // "main.ts 42:15"
 * ```
 */
export function printLocation(location: Location): string {
  return `${location.filename} ${location.line}:${location.column}`;
}

/**
 * Formats an array of locations as a stack trace string.
 *
 * @param locations - The source locations to format
 * @returns A stack trace string with each location on a new line
 *
 * @example
 * ```ts
 * const locs = [
 *   { filename: "main.ts", line: 42, column: 15 },
 *   { filename: "lib.ts", line: 10, column: 5 }
 * ];
 * printLocations(locs);
 * // "main.ts 42:15
 * //   at lib.ts 10:5"
 * ```
 */
export function printLocations(locations: Location[]): string {
  if (locations.length === 0) return '<unknown>';
  const [first, ...rest] = locations;
  const header = printLocation(first!);
  if (rest.length === 0) return header;
  return header + '\n' + rest.map(loc => `  at ${printLocation(loc)}`).join('\n');
}

/**
 * Determines if a stack frame should be included in location captures.
 * Filters out internal frames (Node.js internals, node_modules) to show
 * only user code in error stack traces.
 *
 * @param filename - The file path from the stack frame
 * @returns true if the frame should be included, false to filter it out
 */
function shouldIncludeFrame(filename: string): boolean {
  // Skip Node.js internal modules (e.g., node:internal/modules/...)
  if (filename.startsWith('node:')) return false;

  // Skip node_modules - filters out third-party packages including East
  // when installed as a dependency. Handles both Unix and Windows paths.
  if (filename.includes('/node_modules/') || filename.includes('\\node_modules\\')) return false;

  return true;
}

/**
 * Captures the call stack as an array of source locations, filtered to
 * show only user code.
 *
 * @returns An array of {@link Location} objects representing the call stack,
 *          from innermost (most recent) to outermost frame
 *
 * @remarks
 * This function uses JavaScript's Error stack traces to capture the call
 * stack. Internal frames (Node.js internals, node_modules packages) are
 * filtered out to provide clean stack traces showing only user code.
 * Returns an empty array if the stack trace cannot be parsed.
 *
 * @example
 * ```ts
 * function myFunction() {
 *   const stack = get_location(); // Gets call stack of user code
 *   console.log(printLocations(stack));
 * }
 * ```
 */
export function get_location(): Location[] {
  const err = new Error();
  const stack = err.stack;
  if (!stack) return [];

  const lines = stack.split('\n').slice(1); // Skip "Error" line
  const frames: Location[] = [];

  for (const line of lines) {
    // Simple regex that matches file:line:col at end of line
    const match = line.match(/\(?([^()\s]+):(\d+):(\d+)\)?$/);
    if (match) {
      const [, filename, lineNum, column] = match;
      if (filename && filename !== '' && shouldIncludeFrame(filename)) {
        frames.push({
          filename,
          line: Number(lineNum),
          column: Number(column),
        });
      }
    }
  }

  return frames;
}
