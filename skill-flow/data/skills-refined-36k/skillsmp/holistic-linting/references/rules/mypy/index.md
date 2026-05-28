# MyPy Error Codes Reference

MyPy is a static type checker for Python that enforces type consistency and catches potential runtime errors at compile time. This reference documents all MyPy error codes organized by category.

## Error Code Organization

MyPy error codes fall into two main categories:

- **Default Error Codes**: Enabled by default, covering fundamental type safety checks
- **Optional Error Codes**: Enabled through specific configuration flags for stricter type checking

## Default Error Codes

These error codes are enabled by default and check for fundamental type safety issues.

### Attribute and Member Access

- [attr-defined](./default-errors/attribute-access.md) - Check that attribute exists
- [union-attr](./default-errors/attribute-access.md) - Check attribute exists in union types
- [has-type](./default-errors/attribute-access.md) - Check that type of target is known

### Name Definition and Resolution

- [name-defined](./default-errors/name-resolution.md) - Check that name is defined
- [used-before-def](./default-errors/name-resolution.md) - Check variable not used before definition
- [no-redef](./default-errors/name-resolution.md) - Check each name defined once

### Function Calls and Arguments

- [call-arg](./default-errors/function-calls.md) - Check arguments in calls
- [arg-type](./default-errors/function-calls.md) - Check argument types
- [call-overload](./default-errors/function-calls.md) - Check calls to overloaded functions
- [return](./default-errors/function-calls.md) - Check function returns value
- [return-value](./default-errors/function-calls.md) - Check return value compatibility
- [empty-body](./default-errors/function-calls.md) - Check functions have non-empty bodies
- [func-returns-value](./default-errors/function-calls.md) - Check called function returns value

### Type Annotations and Validity

- [valid-type](./default-errors/type-validity.md) - Check validity of types
- [var-annotated](./default-errors/type-validity.md) - Require annotation if variable type unclear
- [metaclass](./default-errors/type-validity.md) - Check class metaclass validity
- [valid-newtype](./default-errors/type-validity.md) - Check NewType target validity
- [type-var](./default-errors/type-validity.md) - Check type variable values
- [literal-required](./default-errors/type-validity.md) - Check literal used where expected

### Assignment and Type Checking

- [assignment](./default-errors/assignment.md) - Check types in assignment statement
- [method-assign](./default-errors/assignment.md) - Check assignment target is not method
- [override](./default-errors/assignment.md) - Check validity of overrides
- [typeddict-readonly-mutated](./default-errors/assignment.md) - Check ReadOnly TypedDict not mutated

### Collections and Container Operations

- [index](./default-errors/collections.md) - Check indexing operations
- [list-item](./default-errors/collections.md) - Check list items
- [dict-item](./default-errors/collections.md) - Check dict items
- [typeddict-item](./default-errors/collections.md) - Check TypedDict items
- [typeddict-unknown-key](./default-errors/collections.md) - Check TypedDict keys

### Operators and Expressions

- [operator](./default-errors/operators.md) - Check uses of operators
- [str-format](./default-errors/operators.md) - Check string formatting type-safety
- [str-bytes-safe](./default-errors/operators.md) - Check implicit bytes coercions

### Imports and Module Resolution

- [import](./default-errors/imports.md) - Check for import issues
- [import-not-found](./default-errors/imports.md) - Check import target can be found
- [import-untyped](./default-errors/imports.md) - Check import has type annotations

### Abstract Classes and Instantiation

- [abstract](./default-errors/abstract.md) - Check instantiation of abstract classes
- [type-abstract](./default-errors/abstract.md) - Safe handling of abstract type objects
- [safe-super](./default-errors/abstract.md) - Check abstract method calls via super

### Async and Coroutines

- [await-not-async](./default-errors/async.md) - Check await used in coroutines
- [unused-coroutine](./default-errors/async.md) - Check coroutine return value used
- [top-level-await](./default-errors/async.md) - Warn about top-level await expressions

### Type Inference and Overloading

- [name-match](./default-errors/advanced.md) - Check naming consistency
- [no-overload-impl](./default-errors/advanced.md) - Check overloaded functions have implementation
- [overload-overlap](./default-errors/advanced.md) - Check overloaded functions don't overlap
- [overload-cannot-match](./default-errors/advanced.md) - Check overload signatures can match
- [narrowed-type-not-subtype](./default-errors/advanced.md) - Check TypeIs narrows correctly
- [exit-return](./default-errors/advanced.md) - Check \_\_exit\_\_ return type
- [assert-type](./default-errors/advanced.md) - Check types in assert_type
- [truthy-function](./default-errors/advanced.md) - Check function not used in boolean context
- [annotation-unchecked](./default-errors/advanced.md) - Notify about annotation in unchecked function
- [prop-decorator](./default-errors/advanced.md) - Decorator preceding property not supported
- [syntax](./default-errors/advanced.md) - Report syntax errors
- [misc](./default-errors/advanced.md) - Miscellaneous checks

## Optional Error Codes

These error codes provide stricter type checking and are enabled through configuration flags.

### Strict Type Requirements

- [no-untyped-def](./optional-errors/strict-types.md) - Require function type annotations
- [no-untyped-call](./optional-errors/strict-types.md) - Prevent calling untyped functions
- [type-arg](./optional-errors/strict-types.md) - Require generic type arguments
- [no-any-return](./optional-errors/strict-types.md) - Check return values are not Any
- [no-any-unimported](./optional-errors/strict-types.md) - Check Any from unimported sources
- [explicit-any](./optional-errors/strict-types.md) - Disallow explicit Any annotations

### Code Quality and Redundancy

- [redundant-cast](./optional-errors/code-quality.md) - Flag unnecessary type casts
- [redundant-self](./optional-errors/code-quality.md) - Detect redundant Self annotations
- [redundant-expr](./optional-errors/code-quality.md) - Detect redundant expressions
- [unused-ignore](./optional-errors/code-quality.md) - Detect unnecessary type ignores
- [unused-awaitable](./optional-errors/code-quality.md) - Flag unawaited async values
- [ignore-without-code](./optional-errors/code-quality.md) - Ensure type ignores have error codes

### Logic and Control Flow

- [comparison-overlap](./optional-errors/logic.md) - Warn about invalid comparisons
- [unreachable](./optional-errors/logic.md) - Identify dead code
- [possibly-undefined](./optional-errors/logic.md) - Warn about conditionally defined variables
- [truthy-bool](./optional-errors/logic.md) - Check non-boolean context usage
- [truthy-iterable](./optional-errors/logic.md) - Check Iterable in boolean context
- [exhaustive-match](./optional-errors/logic.md) - Ensure match statements are exhaustive

### Modern Python Features

- [explicit-override](./optional-errors/modern.md) - Require @override decorator
- [mutable-override](./optional-errors/modern.md) - Check unsafe mutable attribute overrides
- [unimported-reveal](./optional-errors/modern.md) - Ensure reveal_type is imported
- [deprecated](./optional-errors/modern.md) - Flag use of deprecated features

## Configuration

To enable optional error codes, use one of these approaches:

### mypy.ini or setup.cfg

```ini
[mypy]
disallow_untyped_defs = True
disallow_untyped_calls = True
warn_return_any = True
warn_unused_ignores = True
strict_equality = True
enable_error_code = explicit-override,unused-awaitable,exhaustive-match
```

### pyproject.toml

```toml
[tool.mypy]
disallow_untyped_defs = true
disallow_untyped_calls = true
warn_return_any = true
warn_unused_ignores = true
strict_equality = true
enable_error_code = ["explicit-override", "unused-awaitable", "exhaustive-match"]
```

## Suppressing Error Codes

To suppress a specific error code, use the `# type: ignore[error-code]` comment:

```python
# Suppress one error code
x = "string" + 5  # type: ignore[operator]

# Suppress multiple error codes
y = some_any_value  # type: ignore[no-any-return, assignment]

# Suppress all errors on a line
z = ...  # type: ignore
```

## See Also

- [Official MyPy Documentation](https://mypy.readthedocs.io/)
- [MyPy Error Codes Documentation](https://mypy.readthedocs.io/en/stable/error_codes.html)
- [MyPy Configuration](https://mypy.readthedocs.io/en/stable/config_file.html)
