import path from 'path';

/**
 * Symbol definition found during parsing.
 */
export interface SymbolDef {
  /** The type of symbol (e.g., function, class, variable). */
  kind: 'function' | 'class' | 'variable' | 'export' | 'interface' | 'type';
  /** The name of the symbol, potentially prefixed by its parent class. */
  name: string;
  /** The source line content representing the symbol signature. */
  signature: string;
  /** 1-based start line number. */
  start_line: number;
  /** 1-based end line number (currently estimated as same as start). */
  end_line: number;
  /** Whether the symbol is exported from the module. */
  exported: boolean;
}

/**
 * Import definition found during parsing.
 */
export interface ImportDef {
  /** The path or module name being imported. */
  path: string;
}

/**
 * Result of parsing a file.
 */
export interface ParseResult {
  symbols: SymbolDef[];
  imports: ImportDef[];
  language: string;
}

/**
 * A fast, heuristic-based parser for extracting symbols and imports.
 * Uses optimized Regex patterns to balance performance and coverage.
 */
export class SimpleParser {
  /**
   * Parse a file based on its extension.
   */
  static parse(filePath: string, content: string): ParseResult {
    const ext = path.extname(filePath);
    if (['.ts', '.js', '.tsx', '.jsx'].includes(ext)) {
      return this.parseTS(content);
    } else if (['.py'].includes(ext)) {
      return this.parsePython(content);
    }
    return { symbols: [], imports: [], language: 'unknown' };
  }

  /**
   * Extract symbols and imports from TypeScript/JavaScript.
   */
  private static parseTS(content: string): ParseResult {
    const symbols: SymbolDef[] = [];
    const imports: ImportDef[] = [];
    const lines = content.split('\n');

    /**
     * REGEX LOGIC:
     * 1. exportRegex: Captures standard exports.
     *    - Supports: export [async] (const|let|var|function|class|interface|type) NAME
     * 2. defaultExportRegex: Captures default exports.
     *    - Supports: export default [function|class] NAME
     * 3. functionRegex: Captures standard function definitions.
     *    - Supports: [async] function NAME(...)
     * 4. arrowFuncRegex: Captures arrow function assignments.
     *    - Supports: [export] const NAME = [async] (...) =>
     * 5. classRegex: Captures class definitions.
     *    - Supports: class NAME [extends/implements]
     * 6. methodRegex: Captures class methods (indented).
     *    - Supports: [async] [static] NAME(...) [: ]
     * 7. importRegex: Captures ESM imports.
     *    - Supports: import ... from 'PATH'
     */
    const exportRegex =
      /export\s+(?:async\s+)?(const|let|var|function|class|interface|type)\s+([a-zA-Z0-9_]+)/;
    const defaultExportRegex = /export\s+default\s+(?:(?:function|class)\s+)?([a-zA-Z0-9_]+)/;
    const functionRegex = /(?:async\s+)?function\s+([a-zA-Z0-9_]+)\s*\(/;
    const arrowFuncRegex =
      /(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s+)?\(?.*?\)?\s*=>/;
    const variableRegex = /(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=/;
    const classRegex = /class\s+([a-zA-Z0-9_]+)/;
    const methodRegex = /^\s+(?:async\s+)?(?:static\s+)?([a-zA-Z0-9_]+)\s*\(.*\)\s*[:{]/;
    const importRegex = /import\s+.*from\s+['"]([^'"]+)['"]/;

    let currentClass: string | null = null;

    lines.forEach((line, index) => {
      const lineNum = index + 1;
      const trimmed = line.trim();
      if (trimmed.length === 0) return;

      // Import detection
      const impMatch = line.match(importRegex);
      if (impMatch) {
        imports.push({ path: impMatch[1] });
      }

      // Export detection
      const expMatch = line.match(exportRegex);
      if (expMatch) {
        const kind = expMatch[1];
        const name = expMatch[2];
        symbols.push({
          kind: 'export',
          name,
          signature: trimmed,
          start_line: lineNum,
          end_line: lineNum,
          exported: true,
        });
        symbols.push({
          kind: kind as any,
          name,
          signature: trimmed,
          start_line: lineNum,
          end_line: lineNum,
          exported: true,
        });
        if (kind === 'class') currentClass = name;
        return;
      }

      // Default export detection
      const defExpMatch = line.match(defaultExportRegex);
      if (defExpMatch && defExpMatch[1]) {
        symbols.push({
          kind: 'export',
          name: defExpMatch[1],
          signature: trimmed,
          start_line: lineNum,
          end_line: lineNum,
          exported: true,
        });
      }

      // Class detection
      const classMatch = line.match(classRegex);
      if (classMatch) {
        currentClass = classMatch[1];
        symbols.push({
          kind: 'class',
          name: currentClass,
          signature: trimmed,
          start_line: lineNum,
          end_line: lineNum,
          exported: false,
        });
        return;
      }

      // Method detection (only if inside class)
      const methodMatch = line.match(methodRegex);
      if (methodMatch && currentClass) {
        symbols.push({
          kind: 'function',
          name: `${currentClass}.${methodMatch[1]}`,
          signature: trimmed,
          start_line: lineNum,
          end_line: lineNum,
          exported: false,
        });
        return;
      }

      // Arrow function detection
      const arrowMatch = line.match(arrowFuncRegex);
      if (arrowMatch) {
        symbols.push({
          kind: 'function',
          name: arrowMatch[1],
          signature: trimmed,
          start_line: lineNum,
          end_line: lineNum,
          exported: false,
        });
        return;
      }

      // Variable detection (fallback)
      const varMatch = line.match(variableRegex);
      if (varMatch) {
        symbols.push({
          kind: 'variable',
          name: varMatch[1],
          signature: trimmed,
          start_line: lineNum,
          end_line: lineNum,
          exported: false,
        });
        return;
      }

      // Standard function detection
      const funcMatch = line.match(functionRegex);
      if (funcMatch) {
        symbols.push({
          kind: 'function',
          name: funcMatch[1],
          signature: trimmed,
          start_line: lineNum,
          end_line: lineNum,
          exported: false,
        });
      }
    });

    return { symbols, imports, language: 'typescript' };
  }

  /**
   * Extract symbols and imports from Python.
   */
  private static parsePython(content: string): ParseResult {
    const symbols: SymbolDef[] = [];
    const imports: ImportDef[] = [];
    const lines = content.split('\n');

    /**
     * REGEX LOGIC:
     * 1. defRegex: Captures function and method definitions.
     *    - Supports: [async] def NAME(...)
     * 2. classRegex: Captures class definitions.
     *    - Supports: class NAME[(...)]:
     * 3. importRegex: Captures module imports.
     *    - Supports: import MODULE or from MODULE import ...
     */
    const defRegex = /(?:async\s+)?def\s+([a-zA-Z0-9_]+)\s*\(/;
    const classRegex = /class\s+([a-zA-Z0-9_]+)(?:\(.*?\))?\s*:/;
    const importRegex = /^(?:from\s+([a-zA-Z0-9_.]+)\s+)?import/;

    let currentClass: string | null = null;

    lines.forEach((line, index) => {
      const lineNum = index + 1;
      const trimmedLine = line.trim();
      if (trimmedLine.length === 0) return;

      const leadingSpaces = line.match(/^(\s*)/)?.[1].length || 0;

      // Heuristic: Reset class context if we hit a non-indented line that isn't a class
      if (leadingSpaces === 0 && !trimmedLine.startsWith('class ')) {
        currentClass = null;
      }

      // Import detection
      const impMatch = trimmedLine.match(importRegex);
      if (impMatch) {
        imports.push({ path: impMatch[1] || 'module' });
      }

      // Class detection
      const classMatch = trimmedLine.match(classRegex);
      if (classMatch) {
        currentClass = classMatch[1];
        symbols.push({
          kind: 'class',
          name: currentClass,
          signature: trimmedLine,
          start_line: lineNum,
          end_line: lineNum,
          exported: true,
        });
        return;
      }

      // Function/Method detection
      const defMatch = trimmedLine.match(defRegex);
      if (defMatch) {
        const name = currentClass ? `${currentClass}.${defMatch[1]}` : defMatch[1];
        symbols.push({
          kind: 'function',
          name,
          signature: trimmedLine,
          start_line: lineNum,
          end_line: lineNum,
          exported: true,
        });
      }
    });

    return { symbols, imports, language: 'python' };
  }
}