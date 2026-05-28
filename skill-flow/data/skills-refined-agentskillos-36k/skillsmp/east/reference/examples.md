# East Examples

Working code examples for common East use cases.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Types and Values](#types-and-values)
- [Platform Functions](#platform-functions)
- [Control Flow](#control-flow)
- [Collections](#collections)
- [Grouping and Aggregation](#grouping-and-aggregation)
- [Variants and Pattern Matching](#variants-and-pattern-matching)
- [Error Handling](#error-handling)
- [Standard Library](#standard-library)
- [Patch Operations](#patch-operations)
- [Serialization](#serialization)

---

## Quick Start

```typescript
import { East, IntegerType, ArrayType, StructType, StringType, DictType, NullType } from "@elaraai/east";

// Platform function for logging
const log = East.platform("log", [StringType], NullType);

const platform = [
    log.implement(console.log),
];

// Define sale data type
const SaleType = StructType({
    product: StringType,
    quantity: IntegerType,
    price: IntegerType
});

// Calculate revenue per product from sales data
const calculateRevenue = East.function(
    [ArrayType(SaleType)],
    DictType(StringType, IntegerType),
    ($, sales) => {
        // Group sales by product and sum revenue (quantity x price)
        const revenueByProduct = sales.groupSum(
            ($, sale) => sale.product,
            ($, sale) => sale.quantity.multiply(sale.price)
        );

        // Log revenue
        $(log(East.str`Total Revenue: ${East.Integer.printCurrency(revenueByProduct.sum())}`));

        $.return(revenueByProduct);
    }
);

// Compile and execute
const compiled = East.compile(calculateRevenue, platform);

const sales = [
    { product: "Widget", quantity: 10n, price: 50n },
    { product: "Gadget", quantity: 5n, price: 100n },
    { product: "Widget", quantity: 3n, price: 50n }
];

compiled(sales);
// Logs: Total Revenue: $1,150
// Returns: Map { "Gadget" => 500n, "Widget" => 650n }
```

---

## Types and Values

### Primitive Types

```typescript
import { East, NullType, BooleanType, IntegerType, FloatType, StringType, DateTimeType, BlobType } from "@elaraai/east";

const primitiveDemo = East.function([], NullType, $ => {
    const nullVal = $.let(null, NullType);
    const boolVal = $.let(true);
    const intVal = $.let(42n);            // bigint for integers
    const floatVal = $.let(3.14);
    const strVal = $.let("hello");
    const dateVal = $.let(new Date());
    const blobVal = $.let(new Uint8Array([1, 2, 3]));

    $.return(null);
});
```

### Struct Types

```typescript
import { East, StructType, StringType, IntegerType } from "@elaraai/east";

const PersonType = StructType({
    name: StringType,
    age: IntegerType
});

const getPersonInfo = East.function([PersonType], StringType, ($, person) => {
    // Access struct fields directly as properties
    $.return(East.str`${person.name} is ${person.age} years old`);
});

const compiled = East.compile(getPersonInfo, []);
compiled({ name: "Alice", age: 30n });  // "Alice is 30 years old"
```

### Variant Types

```typescript
import { East, variant, VariantType, IntegerType, NullType } from "@elaraai/east";

const OptionType = VariantType({ some: IntegerType, none: NullType });

const unwrapOr = East.function([OptionType, IntegerType], IntegerType, ($, opt, defaultVal) => {
    const result = $.let(defaultVal);
    $.match(opt, {
        some: ($, x) => $.assign(result, x),
        none: $ => { /* keep default */ }
    });
    $.return(result);
});

const compiled = East.compile(unwrapOr, []);
compiled(variant("some", 42n), 0n);   // 42n
compiled(variant("none", null), 0n);  // 0n
```

### Ref Types (Mutable References)

```typescript
import { East, ref, RefType, IntegerType, ArrayType } from "@elaraai/east";

// Ref allows mutable state captured by closures
const counter = East.function([], IntegerType, $ => {
    const count = $.let(East.value(ref(0n)));

    // Update ref value
    $(count.update(count.get().add(1n)));
    $(count.update(count.get().add(1n)));

    // Merge with function
    $(count.merge(5n, ($, current, delta) => current.add(delta)));

    $.return(count.get());  // 7n
});
```

---

## Platform Functions

### Sync Platform Functions

```typescript
import { East, StringType, NullType, BlobType } from "@elaraai/east";
import * as fs from 'fs';

const log = East.platform("log", [StringType], NullType);
const readFile = East.platform("readFile", [StringType], BlobType);

const platform = [
    log.implement(console.log),
    readFile.implement((path) => fs.readFileSync(path)),
];

const processFile = East.function([StringType], NullType, ($, path) => {
    const content = $.let(readFile(path));
    $(log(East.str`File size: ${content.size()} bytes`));
    $.return(null);
});

const compiled = East.compile(processFile, platform);
```

### Async Platform Functions

```typescript
import { East, StringType, NullType, BlobType } from "@elaraai/east";
import * as fs from 'fs/promises';

const log = East.platform("log", [StringType], NullType);
const readFile = East.asyncPlatform("readFile", [StringType], BlobType);

const platform = [
    log.implement(console.log),
    readFile.implement((path) => fs.readFile(path)),
];

// Use asyncFunction for functions that call async platform functions
const processFile = East.asyncFunction([StringType], NullType, ($, path) => {
    const content = $.let(readFile(path));  // No await needed
    $(log(East.str`File size: ${content.size()} bytes`));
    $.return(null);
});

const compiled = East.compileAsync(processFile, platform);
await compiled("data.txt");  // Returns Promise
```

---

## Control Flow

### Conditionals

```typescript
import { East, IntegerType, StringType } from "@elaraai/east";

const classify = East.function([IntegerType], StringType, ($, x) => {
    const result = $.let("unknown");

    $.if(East.less(x, 0n), $ => {
        $.assign(result, "negative");
    }).elseIf(East.equal(x, 0n), $ => {
        $.assign(result, "zero");
    }).else($ => {
        $.assign(result, "positive");
    });

    $.return(result);
});
```

### Loops

```typescript
import { East, IntegerType, ArrayType } from "@elaraai/east";

const sumWithLoop = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
    const total = $.let(0n);

    // For loop over array
    $.for(arr, ($, value, index, label) => {
        $.assign(total, total.add(value));
    });

    $.return(total);
});

const factorial = East.function([IntegerType], IntegerType, ($, n) => {
    const result = $.let(1n);
    const i = $.let(n);

    // While loop
    $.while(East.greater(i, 0n), ($, label) => {
        $.assign(result, result.multiply(i));
        $.assign(i, i.subtract(1n));
    });

    $.return(result);
});
```

### Break and Continue

```typescript
import { East, IntegerType, ArrayType } from "@elaraai/east";

const findFirst = East.function([ArrayType(IntegerType), IntegerType], IntegerType, ($, arr, target) => {
    const result = $.let(-1n);

    $.for(arr, ($, value, index, label) => {
        $.if(East.equal(value, target), $ => {
            $.assign(result, index);
            $.break(label);
        });
    });

    $.return(result);
});
```

---

## Collections

### Array Operations

```typescript
import { East, IntegerType, ArrayType, StringType } from "@elaraai/east";

const arrayOps = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
    // Mutation
    $(arr.pushLast(100n));
    $(arr.pushFirst(0n));

    // Functional operations (return new arrays)
    const doubled = arr.map(($, x, i) => x.multiply(2n));
    const filtered = doubled.filter(($, x, i) => East.greater(x, 10n));
    const sorted = filtered.sort();

    // Reduction
    const sum = sorted.sum();
    const mean = sorted.mean();
    const max = sorted.maximum();

    $.return(sum);
});

// Slicing and concatenation
const sliceDemo = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
    const first5 = arr.slice(0n, 5n);
    const last5 = arr.slice(arr.size().subtract(5n), arr.size());
    const combined = first5.concat(last5);
    $.return(combined);
});
```

### Set Operations

```typescript
import { East, IntegerType, SetType } from "@elaraai/east";

const setOps = East.function([SetType(IntegerType), SetType(IntegerType)], SetType(IntegerType), ($, a, b) => {
    // Set operations
    const union = a.union(b);
    const intersection = a.intersection(b);
    const difference = a.difference(b);

    // Mutation
    $(a.insert(999n));
    $(a.tryInsert(999n));  // Returns false if already exists

    // Check membership
    const hasValue = a.has(42n);

    $.return(union);
});
```

### Dict Operations

```typescript
import { East, StringType, IntegerType, DictType } from "@elaraai/east";

const dictOps = East.function([DictType(StringType, IntegerType)], IntegerType, ($, inventory) => {
    // Get with default
    const count = inventory.get("widget", East.function([StringType], IntegerType, ($, key) => 0n));

    // Merge (update or initialize)
    $(inventory.merge("widget", 5n,
        ($, old, delta, key) => old.add(delta),
        ($, key) => 0n  // Initial value if key doesn't exist
    ));

    // Get keys as set
    const keys = inventory.keys();

    // Iterate
    $(inventory.forEach(($, value, key) => {
        // Process each entry
    }));

    $.return(inventory.sum());
});
```

---

## Grouping and Aggregation

```typescript
import { East, IntegerType, StringType, ArrayType, StructType, DictType } from "@elaraai/east";

const SaleType = StructType({
    product: StringType,
    category: StringType,
    quantity: IntegerType,
    price: IntegerType
});

const analytics = East.function([ArrayType(SaleType)], DictType(StringType, IntegerType), ($, sales) => {
    // Group by product and sum quantities
    const quantityByProduct = sales.groupSum(
        ($, sale, i) => sale.product,
        ($, sale, i) => sale.quantity
    );

    // Group by category and count
    const countByCategory = sales.groupSize(
        ($, sale, i) => sale.category
    );

    // Group by category and calculate mean price
    const avgPriceByCategory = sales.groupMean(
        ($, sale, i) => sale.category,
        ($, sale, i) => sale.price
    );

    // Group into arrays for further processing
    const salesByProduct = sales.groupToArrays(
        ($, sale, i) => sale.product,
        ($, sale, i) => sale
    );

    // Complex grouping with custom reducer
    const revenueByProduct = sales.groupReduce(
        ($, sale, i) => sale.product,                    // key function
        ($, sale, i) => sale.quantity.multiply(sale.price),  // value function
        ($, key) => 0n,                                  // initial value
        ($, acc, val, key) => acc.add(val)               // reducer
    );

    $.return(revenueByProduct);
});
```

---

## Variants and Pattern Matching

### Expression-Style Match

```typescript
import { East, variant, VariantType, IntegerType, StringType, NullType } from "@elaraai/east";

const ResultType = VariantType({
    success: IntegerType,
    error: StringType
});

const handleResult = East.function([ResultType], StringType, ($, result) => {
    // Expression-style match (returns a value)
    const message = result.match({
        success: ($, value) => East.str`Got value: ${value}`,
        error: ($, msg) => East.str`Error: ${msg}`
    }, $ => "Unknown");

    $.return(message);
});
```

### Statement-Style Match

```typescript
import { East, variant, VariantType, IntegerType, StringType, NullType } from "@elaraai/east";

const StatusType = VariantType({
    pending: NullType,
    processing: IntegerType,  // progress percentage
    complete: StringType      // result
});

const processStatus = East.function([StatusType], StringType, ($, status) => {
    const result = $.let("unknown");

    // Statement-style match
    $.match(status, {
        pending: $ => {
            $.assign(result, "Waiting to start...");
        },
        processing: ($, progress) => {
            $.assign(result, East.str`Processing: ${progress}%`);
        },
        complete: ($, output) => {
            $.assign(result, East.str`Done: ${output}`);
        }
    });

    $.return(result);
});
```

### Unwrap Operations

```typescript
import { East, variant, VariantType, IntegerType, NullType } from "@elaraai/east";

const OptionType = VariantType({ some: IntegerType, none: NullType });

const useOption = East.function([OptionType], IntegerType, ($, opt) => {
    // Check tag
    const isSome = opt.hasTag("some");
    const tag = opt.getTag();

    // Unwrap with default
    const value = opt.unwrap("some", $ => 0n);

    // Or pattern match
    const doubled = opt.match({
        some: ($, x) => x.multiply(2n)
    }, $ => 0n);

    $.return(value);
});
```

---

## Error Handling

### Try-Catch-Finally

```typescript
import { East, IntegerType, ArrayType, StringType, NullType } from "@elaraai/east";

const log = East.platform("log", [StringType], NullType);

const safeGet = East.function([ArrayType(IntegerType), IntegerType], IntegerType, ($, arr, index) => {
    const result = $.let(0n);
    const wasError = $.let(false);

    $.try($ => {
        $.assign(result, arr.get(index));
    }).catch(($, message, stack) => {
        $.assign(wasError, true);
        $(log(East.str`Error: ${message}`));
        // stack is ArrayExpr<StructType<{filename, line, column}>>
    }).finally($ => {
        $(log("Cleanup complete"));
    });

    $.return(result);
});
```

### Throwing Errors

```typescript
import { East, IntegerType, StringType } from "@elaraai/east";

const divide = East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => {
    $.if(East.equal(b, 0n), $ => {
        $.error("Division by zero");
    });
    $.return(a.divide(b));
});
```

---

## Standard Library

### Integer Formatting

```typescript
import { East, IntegerType, StringType } from "@elaraai/east";

const formatNumbers = East.function([IntegerType], StringType, ($, value) => {
    const comma = East.Integer.printCommaSeperated(value);      // "1,234,567"
    const compact = East.Integer.printCompact(value);           // "1.23M"
    const compactSI = East.Integer.printCompactSI(value);       // "1.23M"
    const ordinal = East.Integer.printOrdinal(value);           // "1st", "2nd", "3rd"
    const currency = East.Integer.printCurrency(value);         // "$1,234,567"
    const percentage = East.Integer.printPercentage(value);     // "45%"

    // Rounding
    const rounded = East.Integer.roundNearest(value, 100n);
    const roundedUp = East.Integer.roundUp(value, 100n);
    const roundedDown = East.Integer.roundDown(value, 100n);

    $.return(comma);
});
```

### Float Formatting

```typescript
import { East, FloatType, StringType } from "@elaraai/east";

const formatFloats = East.function([FloatType], StringType, ($, value) => {
    const comma = East.Float.printCommaSeperated(value, 2n);    // "1,234.57"
    const fixed = East.Float.printFixed(value, 3n);             // "1234.567"
    const compact = East.Float.printCompact(value);             // "1.23K"
    const currency = East.Float.printCurrency(value);           // "$1234.57"
    const percentage = East.Float.printPercentage(value, 1n);   // "45.2%"

    // Rounding to integer
    const floor = East.Float.roundFloor(value);
    const ceil = East.Float.roundCeil(value);
    const half = East.Float.roundHalf(value);

    // Rounding to decimals
    const twoDecimals = East.Float.roundToDecimals(value, 2n);

    // Approximate equality
    const isClose = East.Float.approxEqual(value, 3.14, 0.01);

    $.return(comma);
});
```

### DateTime Operations

```typescript
import { East, DateTimeType, IntegerType, StringType } from "@elaraai/east";

const dateOps = East.function([DateTimeType], StringType, ($, date) => {
    // Construction
    const fromEpoch = East.DateTime.fromEpochMilliseconds(1640000000000n);
    const fromComponents = East.DateTime.fromComponents(2025n, 1n, 15n, 10n, 30n);

    // Rounding
    const dayStart = East.DateTime.roundDownDay(date, 1n);
    const hourStart = East.DateTime.roundDownHour(date, 1n);
    const weekStart = East.DateTime.roundDownWeek(date, 1n);  // Monday
    const monthStart = East.DateTime.roundDownMonth(date, 1n);

    // Component access
    const year = date.getYear();
    const month = date.getMonth();
    const day = date.getDayOfMonth();
    const hour = date.getHour();

    // Arithmetic
    const tomorrow = date.addDays(1n);
    const nextWeek = date.addWeeks(1n);
    const twoHoursAgo = date.subtractHours(2n);

    // Duration
    const hoursSince = date.durationHours(fromEpoch);
    const daysSince = date.durationDays(fromEpoch);

    $.return(East.str`${year}-${month}-${day}`);
});
```

### Array Generation

```typescript
import { East, IntegerType, FloatType, ArrayType } from "@elaraai/east";

const generateArrays = East.function([], ArrayType(IntegerType), $ => {
    // Range: [start, end) with step
    const range = East.Array.range(0n, 10n, 2n);        // [0, 2, 4, 6, 8]

    // Linspace: n equally-spaced values [start, stop]
    const linspace = East.Array.linspace(0.0, 1.0, 5n); // [0.0, 0.25, 0.5, 0.75, 1.0]

    // Generate with function
    const squares = East.Array.generate(5n, IntegerType, ($, i) => i.multiply(i));
    // [0, 1, 4, 9, 16]

    $.return(range);
});
```

### CSV Operations

```typescript
import { East, BlobType, ArrayType, StructType, StringType, IntegerType } from "@elaraai/east";

const PersonType = StructType({ name: StringType, age: IntegerType });

const csvOps = East.function([BlobType], BlobType, ($, csvBlob) => {
    // Parse CSV to array of structs
    const people = csvBlob.decodeCsv(PersonType);

    // With options
    const peopleCustom = csvBlob.decodeCsv(PersonType, {
        delimiter: ';',
        hasHeader: true,
        skipEmptyLines: true,
        trimFields: true
    });

    // Serialize array to CSV
    const outputCsv = people.encodeCsv();

    // With options
    const outputCsvCustom = people.encodeCsv({
        delimiter: ',',
        includeHeader: true,
        newline: '\r\n'
    });

    $.return(outputCsv);
});
```

---

## Patch Operations

### Computing and Applying Diffs

```typescript
import { East, IntegerType, ArrayType, StructType, StringType, PatchType } from "@elaraai/east";

const PersonType = StructType({ name: StringType, age: IntegerType });

// Compute the difference between two values
const computeDiff = East.function(
    [PersonType, PersonType],
    PatchType(PersonType),
    ($, before, after) => {
        $.return(East.diff(before, after));
    }
);

// Apply a patch to a value
const applyDiff = East.function(
    [PersonType, PatchType(PersonType)],
    PersonType,
    ($, original, patch) => {
        $.return(East.applyPatch(original, patch));
    }
);

const compiled = East.compile(computeDiff, []);
const patch = compiled(
    { name: "Alice", age: 30n },
    { name: "Alice", age: 31n }
);
// patch = { type: "patch", value: { name: unchanged, age: replace(30n, 31n) } }
```

### Undo with Inverted Patches

```typescript
import { East, IntegerType, ArrayType, StructType, StringType, PatchType } from "@elaraai/east";

const DocumentType = StructType({ title: StringType, version: IntegerType });

// Track changes with undo capability
const editWithUndo = East.function(
    [DocumentType, DocumentType],
    StructType({ result: DocumentType, undo: PatchType(DocumentType) }),
    ($, original, edited) => {
        const patch = $.let(East.diff(original, edited));
        const undoPatch = $.let(East.invertPatch(patch, DocumentType));
        $.return({ result: edited, undo: undoPatch });
    }
);

const compiled = East.compile(editWithUndo, []);
const result = compiled(
    { title: "Draft", version: 1n },
    { title: "Final", version: 2n }
);
// result.undo can be applied to result.result to get back the original
```

### Composing Sequential Patches

```typescript
import { East, IntegerType, ArrayType, PatchType } from "@elaraai/east";

// Combine multiple patches into one
const combinePatches = East.function(
    [PatchType(ArrayType(IntegerType)), PatchType(ArrayType(IntegerType))],
    PatchType(ArrayType(IntegerType)),
    ($, first, second) => {
        $.return(East.composePatch(first, second, ArrayType(IntegerType)));
    }
);
```

---

## Serialization

### IR Serialization

```typescript
import { East, EastIR, IntegerType, StringType, NullType } from "@elaraai/east";

const log = East.platform("log", [StringType], NullType);

// Define function
const myFunction = East.function([IntegerType], IntegerType, ($, x) => {
    $.return(x.multiply(2n));
});

// Convert to IR
const ir = myFunction.toIR();

// Serialize to JSON
const jsonData = ir.toJSON();
const jsonString = JSON.stringify(jsonData);

// Deserialize and compile
const receivedData = JSON.parse(jsonString);
const receivedIR = EastIR.fromJSON(receivedData);
const compiled = receivedIR.compile([]);

compiled(21n);  // 42n
```

### BEAST Binary Format

```typescript
import { East, IntegerType, BlobType, StructType, StringType } from "@elaraai/east";

const PersonType = StructType({ name: StringType, age: IntegerType });

const serializeDemo = East.function([PersonType], PersonType, ($, person) => {
    // Encode to BEAST v2 format
    const blob = East.Blob.encodeBeast(person, 'v2');

    // Decode from BEAST v2
    const decoded = blob.decodeBeast(PersonType, 'v2');

    $.return(decoded);
});
```
