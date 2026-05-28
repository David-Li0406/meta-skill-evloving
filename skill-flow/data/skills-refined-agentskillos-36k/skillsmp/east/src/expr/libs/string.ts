/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { type StructType, StringType, type IntegerType } from "../../types.js";
import type { ArrayExpr } from "../array.js";
import { Expr } from "../expr.js";
import type { StringExpr } from "../string.js";

/** Standard library for string values */
export default {
  /**
   * Formats an error message and stack trace in a human-readable form.
   *
   * @param message - The error message to display
   * @param stack - An array of stack frames, each containing `filename`, `line`, and `column`
   * @returns A formatted error string with the message and stack trace
   *
   * @example
   * ```ts
   * const StackFrameType = StructType({ filename: StringType, line: IntegerType, column: IntegerType });
   *
   * const formatError = East.function([StringType, ArrayType(StackFrameType)], StringType, ($, msg, stack) => {
   *   $.return(East.printError(msg, stack));
   * });
   * const compiled = East.compile(formatError.toIR(), []);
   * const result = compiled("Division by zero", [
   *   { filename: "app.ts", line: 42n, column: 10n },
   *   { filename: "main.ts", line: 15n, column: 5n }
   * ]);
   * // Returns:
   * // "Error: Division by zero
   * //     [0] app.ts 42:10
   * //     [1] main.ts 15:5"
   * ```
   */
  printError(message: StringExpr, stack: ArrayExpr<StructType<{ filename: StringType, line: IntegerType, column: IntegerType }>>): StringExpr {
    return Expr.str`Error: ${message}\n    ${stack.map((_$, { filename, line, column }, i) => Expr.str`[${i}] ${filename} ${line}:${column}`).stringJoin("\n    ")}`;
  },

  /**
   * Creates a string containing East's canonical JSON representation of a value.
   *
   * @param value - The East value to serialize to JSON
   * @returns A JSON string representation of the value
   *
   * @example
   * ```ts
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   *
   * const toJson = East.function([PersonType], StringType, ($, person) => {
   *   $.return(East.String.printJson(person));
   * });
   * const compiled = East.compile(toJson.toIR(), []);
   * compiled({ name: "Alice", age: 30n });  // '{"name":"Alice","age":30}'
   * ```
   *
   * @example
   * ```ts
   * // Array to JSON
   * const arrayToJson = East.function([ArrayType(IntegerType)], StringType, ($, arr) => {
   *   $.return(East.String.printJson(arr));
   * });
   * const compiled = East.compile(arrayToJson.toIR(), []);
   * compiled([1n, 2n, 3n]);  // '[1,2,3]'
   * ```
   */
  printJson(value: Expr): StringExpr {
    return Expr.fromAst({
      ast_type: "Builtin",
      type: StringType,
      builtin: "StringPrintJSON",
      location: [{ filename: "stdlib", line: 1, column: 1 }],
      type_parameters: [Expr.type(value)],
      arguments: [Expr.ast(value)],
    })
  }
}