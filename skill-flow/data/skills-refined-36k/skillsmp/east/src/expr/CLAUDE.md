# Expressions

This folder contains the user-facing TypeScript interface for writing East functions.

## Expr

`Expr` is a superclass used in a fluent interface to build East expressions.
It has subtypes like `IntegerExpr` that supports methods like `add`, two add two integers.
We are flexible in accepting either other `Expr`s or direct values as arguments to `Expr` methods.

The `StructExpr` interface is special in that it directly exposes it's fields as dynamically generated getters.
This allows users to interact with `StructExpr` with natural JS syntax, like `struct.field` or `{ ...struct, field: new_value }`.
To enable this, there has been some effort put into `Expr` so that class instances do not expose any methods or properties that can clash with field names or appear in enumerations (spreading, etc).
This includes using symbols and non-enumerable properties to "hide" class data such as the AST, which can be accessed via `Expr.ast(expr)` instead.

Similarly `FunctionExpr` is extended to become a callable object, to allow for native JavaScript function call syntax in expressions.

## Structure

To split the code into multiple modules, we had to introduce a factory dependency injection pattern to construct concrete `Expr`s from AST.
The problem is that each concrete class needs to be able to construct the other concrete classes, but we need to avoid circular dependencies in JavaScript.
Note that there are some circular dependencies in TypeScript types.

The "standard library" is provided in the libs directory, and is also organized by data type.
