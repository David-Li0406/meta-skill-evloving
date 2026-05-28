# SIR: S-expression IR for AI Agents

SIR is a compact, JSON-array-based format for AI agents to produce East programs directly without generating TypeScript code.

**JSON Schema:** [`sir-schema.json`](./sir-schema.json)

## Design Principles

1. **Aligned with IR** - Uses actual IR node names and BuiltinName values from East
2. **Token-efficient** - Compact representation for LLM generation
3. **JSON-compatible** - Valid JSON that can be constrained via JSON Schema
4. **Type-inferrable** - Types can be inferred during lowering to full IR

## Format Overview

SIR uses JSON arrays as S-expressions:

```
["ir_node_or_builtin", arg1, arg2, ...]
```

### Literals (→ ValueIR)

```json
null                           // Null
true                           // Boolean
false
42                             // Integer (number without decimal)
3.14                           // Float (number with decimal)
"hello"                        // String
["DateTime", "2025-01-01T00:00:00.000"]  // DateTime
["Blob", "0x00ff"]             // Blob (hex string)
```

### Variables (→ VariableIR)

```json
"$x"                           // Variable reference ($ prefix)
"$items"
```

### Let Binding (→ LetIR)

```json
["Let", "$x", value_expr]
["Let", "$items", ["NewArray", 1, 2, 3]]
```

### Assignment (→ AssignIR)

```json
["Assign", "$x", new_value_expr]
```

### Functions (→ FunctionIR)

```json
["Function", ["$x"], body_expr]
["Function", ["$a", "$b"], ["IntegerAdd", "$a", "$b"]]
```

### Function Calls (→ CallIR)

```json
["Call", function_expr, arg1, arg2, ...]
["Call", "$myFn", 1, 2, 3]
```

### Collections (→ NewArrayIR, NewSetIR, NewDictIR)

```json
["NewArray", elem1, elem2, elem3]
["NewSet", key1, key2, key3]
["NewDict", [key1, val1], [key2, val2]]
```

### Structs (→ StructIR)

```json
["Struct", {"name": value_expr, "age": value_expr}]
["Struct", {"x": 10, "y": 20}]
```

### Field Access (→ GetFieldIR)

```json
["GetField", struct_expr, "fieldName"]
["GetField", "$point", "x"]
```

### Variants (→ VariantIR)

```json
["Variant", "some", value_expr]
["Variant", "none", null]
```

### Block (→ BlockIR)

```json
["Block",
  ["Let", "$x", 10],
  ["Let", "$y", 20],
  ["IntegerAdd", "$x", "$y"]
]
```

### Conditionals (→ IfElseIR)

```json
["IfElse",
  [condition1, then_expr1],
  [condition2, then_expr2],
  else_expr
]
```

### Pattern Matching (→ MatchIR)

```json
["Match", variant_expr,
  ["some", "$value", body_expr],
  ["none", "$_", default_expr]
]
```

### Loops (→ WhileIR, ForArrayIR, ForSetIR, ForDictIR)

```json
["While", condition_expr, body_expr]
["ForArray", "$arr", "$i", "$elem", body_expr]
["ForSet", "$set", "$key", body_expr]
["ForDict", "$dict", "$key", "$val", body_expr]
```

### Control Flow (→ ReturnIR, BreakIR, ContinueIR)

```json
["Return", value_expr]
["Break"]
["Continue"]
```

## Builtins (→ BuiltinIR)

Builtins use their exact BuiltinName from East:

### Comparison

```json
["Equal", a, b]
["NotEqual", a, b]
["Less", a, b]
["LessEqual", a, b]
["Greater", a, b]
["GreaterEqual", a, b]
```

### Boolean Operations

```json
["BooleanNot", a]
["BooleanAnd", a, b]
["BooleanOr", a, b]
["BooleanXor", a, b]
```

### Integer Arithmetic

```json
["IntegerAdd", a, b]
["IntegerSubtract", a, b]
["IntegerMultiply", a, b]
["IntegerDivide", a, b]
["IntegerRemainder", a, b]
["IntegerNegate", a]
["IntegerAbs", a]
["IntegerPow", base, exp]
```

### Float Arithmetic

```json
["FloatAdd", a, b]
["FloatSubtract", a, b]
["FloatMultiply", a, b]
["FloatDivide", a, b]
["FloatNegate", a]
["FloatAbs", a]
["FloatSqrt", a]
["FloatPow", base, exp]
["FloatSin", a]
["FloatCos", a]
["FloatLog", a]
["FloatExp", a]
```

### Type Conversion

```json
["IntegerToFloat", int_expr]
["FloatToInteger", float_expr]
```

### String Operations

```json
["StringConcat", a, b]
["StringLength", s]
["StringSubstring", s, start, end]
["StringUpperCase", s]
["StringLowerCase", s]
["StringSplit", s, delimiter]
["StringTrim", s]
["StringContains", s, substr]
["StringStartsWith", s, prefix]
["StringEndsWith", s, suffix]
["StringReplace", s, from, to]
["StringIndexOf", s, substr]
["Print", value]
["Parse", string_expr]   // requires type annotation
```

### Array Operations

```json
["ArraySize", arr]
["ArrayGet", arr, index]
["ArrayTryGet", arr, index]
["ArrayUpdate", arr, index, value]
["ArrayPushLast", arr, value]
["ArrayPopLast", arr]
["ArrayConcat", arr1, arr2]
["ArraySlice", arr, start, end]
["ArrayReverse", arr]
["ArraySort", arr, key_fn]
```

### Array Higher-Order Functions

```json
["ArrayMap", arr, ["Function", ["$x", "$i"], body]]
["ArrayFilter", arr, ["Function", ["$x", "$i"], predicate]]
["ArrayFold", arr, initial, ["Function", ["$acc", "$x", "$i"], body]]
["ArrayForEach", arr, ["Function", ["$x", "$i"], body]]
["ArrayFlattenToArray", arr, ["Function", ["$x", "$i"], body]]
```

### Set Operations

```json
["SetSize", set]
["SetHas", set, key]
["SetInsert", set, key]
["SetDelete", set, key]
["SetUnion", set1, set2]
["SetIntersect", set1, set2]
["SetDiff", set1, set2]
["SetMap", set, ["Function", ["$k"], body]]
["SetFilter", set, ["Function", ["$k"], predicate]]
["SetToArray", set, ["Function", ["$k"], body]]
```

### Dict Operations

```json
["DictSize", dict]
["DictHas", dict, key]
["DictGet", dict, key]
["DictTryGet", dict, key]
["DictInsert", dict, key, value]
["DictUpdate", dict, key, value]
["DictDelete", dict, key]
["DictKeys", dict]
["DictMap", dict, ["Function", ["$v", "$k"], body]]
["DictFilter", dict, ["Function", ["$v", "$k"], predicate]]
["DictToArray", dict, ["Function", ["$v", "$k"], body]]
```

## Pipe Desugaring

`pipe` is NOT an IR node. It's syntactic sugar that can be desugared during lowering.

In the TypeScript fluent API:
```typescript
East.array([1, 2, 3])
  .filter((x) => x.gt(0))
  .map((x) => x.multiply(2))
```

In SIR, this is written explicitly as nested builtins:
```json
["ArrayMap",
  ["ArrayFilter",
    ["NewArray", 1, 2, 3],
    ["Function", ["$x", "$i"], ["Greater", "$x", 0]]
  ],
  ["Function", ["$x", "$i"], ["IntegerMultiply", "$x", 2]]
]
```

Or with intermediate variables for clarity:
```json
["Block",
  ["Let", "$arr", ["NewArray", 1, 2, 3]],
  ["Let", "$filtered", ["ArrayFilter", "$arr", ["Function", ["$x", "$i"], ["Greater", "$x", 0]]]],
  ["ArrayMap", "$filtered", ["Function", ["$x", "$i"], ["IntegerMultiply", "$x", 2]]]
]
```

## Complete Example

Calculating the sum of squares of positive numbers:

```json
["Function", ["$numbers"],
  ["ArrayFold",
    ["ArrayFilter",
      ["ArrayMap",
        "$numbers",
        ["Function", ["$x", "$i"], ["IntegerMultiply", "$x", "$x"]]
      ],
      ["Function", ["$x", "$i"], ["Greater", "$x", 0]]
    ],
    0,
    ["Function", ["$acc", "$x", "$i"], ["IntegerAdd", "$acc", "$x"]]
  ]
]
```

Equivalent TypeScript fluent API:
```typescript
East.function([East.array(East.Integer)], East.Integer, ($numbers) =>
  $numbers
    .map((x) => x.multiply(x))
    .filter((x) => x.gt(0))
    .fold(East.integer(0), (acc, x) => acc.add(x))
)
```

## Type Annotations

For operations that require type information (like `Parse`), use a type annotation wrapper:

```json
["As", ["Integer"], expr]
["As", ["Array", ["Integer"]], expr]
["As", ["Dict", ["String"], ["Float"]], expr]
["As", ["Struct", {"x": ["Integer"], "y": ["Integer"]}], expr]
["As", ["Variant", {"some": ["Integer"], "none": ["Null"]}], expr]
```

## Mapping Reference

| SIR Form | IR Node | Notes |
|----------|---------|-------|
| literals | ValueIR | null, bool, int, float, string |
| `$var` | VariableIR | Variable reference |
| `["Let", ...]` | LetIR | |
| `["Assign", ...]` | AssignIR | |
| `["Function", ...]` | FunctionIR | |
| `["Call", ...]` | CallIR | |
| `["NewArray", ...]` | NewArrayIR | |
| `["NewSet", ...]` | NewSetIR | |
| `["NewDict", ...]` | NewDictIR | |
| `["Struct", {...}]` | StructIR | |
| `["GetField", ...]` | GetFieldIR | |
| `["Variant", ...]` | VariantIR | |
| `["Block", ...]` | BlockIR | |
| `["IfElse", ...]` | IfElseIR | |
| `["Match", ...]` | MatchIR | |
| `["While", ...]` | WhileIR | |
| `["ForArray", ...]` | ForArrayIR | |
| `["ForSet", ...]` | ForSetIR | |
| `["ForDict", ...]` | ForDictIR | |
| `["Return", ...]` | ReturnIR | |
| `["Break"]` | BreakIR | |
| `["Continue"]` | ContinueIR | |
| `["IntegerAdd", ...]` | BuiltinIR | builtin: "IntegerAdd" |
| `["ArrayMap", ...]` | BuiltinIR | builtin: "ArrayMap" |
| ... | BuiltinIR | All ~100 builtin names |

## Lowering SIR to IR

A SIR lowerer would:

1. Parse the JSON array structure
2. Infer types bottom-up (literals → operations → expressions)
3. Generate proper VariableIR nodes with unique names
4. Generate LocationValue (can use synthetic locations)
5. Produce full IR nodes with type annotations

The lowerer handles:
- Type inference for all expressions
- Variable scope tracking
- Mutable vs immutable variable detection
- Captured variable detection for closures
