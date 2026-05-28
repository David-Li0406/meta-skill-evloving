# Interfaces

A mapping from target frontend interface to representation as IR.

## Statements

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `$(expr)` | `NullType` | `ExprIR` | Evaluates an expression that may have side-effects | ✅ |
| `$.const(value: V)` | `TypeOf<V>` | `LetIR` | Immutable variable | ✅ |
| `$.const(value, type: T)` | `T` | `LetIR` | Immutable variable | ✅ |
| `$.let(value: V)` | `TypeOf<V>` | `LetIR` | Mutable variable | ✅ |
| `$.let(value, type: T)` | `T` | `LetIR` | Mutable variable | ✅ |
| `$.let(undefined, type: T)` | `T` | `LetIR` | Uninitialized variable (not adding) | ⛔ |
| `$.assign(variable, value)` | `NullType` | `AssignIR` | Mutable variable | ✅ |
| `$.if(predicate, $ => { ... })` | `NullType` | `IfElseIR` | | ✅ |
| `$.if(predicate, $ => { ... }).else($ => { ... })` | `NullType` | `IfElseIR` | | ✅ |
| `$.if(predicate, $ => { ... }).elseIf(predicate, $ => { ... }).else($ => { ... })` | `NullType` | `IfElseIR` | | ✅ |
| `$.match(variant, { case1: ($, data) => { ... }, ... })` | `NullType` | `MatchIR` | Remove, change to builder pattern | ➖ |
| `$.match(variant).case("case1", ($, data) => { ...})` | `NullType` | `MatchIR` | (TODO) | ➕ |
| `$.match(variant).case("case1", ($, data) => { ...}).else($ => { ... })` | `NullType` | `MatchIR` | (TODO) | ➕ |
| `$.while(predicate, $ => { ... })` | `NullType` | `WhileIR` | | ✅ |
| `$.for(array, ($, value, index) => { ... })` | `NullType` | `ForArrayIR` | | ✅ |
| `$.for(set, ($, key) => { ... })` | `NullType` | `ForSetIR` | | ✅ |
| `$.for(dict, ($, value, key) => { ... })` | `NullType` | `ForDictIR` | | ✅ |
| `$.block($ => { ... })` | `NullType` | `BlockIR` | Introduce a new scope | ✅ |
| `$.try($ => { ... }).catch($ => { ... })` | `NullType` | `TryCatchIR` | | ✅ |
| `$.error(message: StringType)` | `NeverType`❗ | `ErrorIR` | | ✅ |
| `$.return(value)` | `NeverType` | `ReturnIR` | | ✅ |
| `$.continue(label)` | `NeverType` | `ContinueIR` | Could label be optional? | ✅ |
| `$.break(label)` | `NeverType` | `BreakIR` | Could label be optional?  | ✅ |

## Fundamental library functions

Note: users can do things like `const str = East.str` to avoid the prefix.
(The `function` name is really awkward though.)

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `East.function([...input_types]: I, output_type: O, ($, arg1, arg2) => { ... })` | `FunctionType<I, O>` | `FunctionIR` | Function/closure definition | ✅ |
| `East.function([...input_types]: I, undefined, ($, arg1, arg2) => { ... }: F)` | `FunctionType<I, TypeOf<ReturnType<F>>` | `FunctionIR` | Function/closure definition with inference | ✅ |
| ``` East.str`abc` ``` | `StringType` | Macro of builtins | String interpolation | ✅ |
| `East.print(value)` | `StringType` | `BuiltinIR` | | ✅ |
| `East.is(x, y)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `East.equal(x, y)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `East.notEqual(x, y)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `East.less(x, y)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `East.lessEqual(x, y)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `East.greater(x, y)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `East.greaterEqual(x, y)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `East.value(value, type: T)` | `T` | `ValueIR`/`NewArrayIR`/etc | Rename - `East.value`? | ✅ |
| `East.value(value: V)` | `ValueTypeOf<V>` | `ValueIR`/`NewArrayIR`/etc | Rename - `East.value`? | ✅ |

## `NullType`

None.

## `BooleanType`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `x.not()` | `BooleanType` | `BuiltinIR` | | ✅ |
| `x.and($ => y)` | `BooleanType` | `IfElseIR` | Short circuiting | ✅ |
| `x.or($ => y)` | `BooleanType` | `IfElseIR` | Short circuting | ✅ |
| `x.bitAnd(y)` | `BooleanType` | `BuiltinIR` - evaluates both arguments | | ✅ |
| `x.bitOr(y)` | `BooleanType` | `BuiltinIR` - evaluates both arguments | | ✅ |
| `x.bitXor(y)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `x.ifElse($ => { ... }, $ => { ... })` | `TypeUnion<ReturnType<T>, ReturnType<F>>` | `IfElseIR` | Inserts `AsIR` for type stability | ✅ |

Note: `AsIR` is a type-widening conversion, which ensures Julia type stability.

## `IntegerType`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `x.negate()` | `IntegerType` | `BuiltinIR` | | ✅ |
| `x.add(y)` | `IntegerType` | `BuiltinIR` | | ✅ |
| `x.subtract(y)` | `IntegerType` | `BuiltinIR` | | ✅ |
| `x.multiply(y)` | `IntegerType` | `BuiltinIR` | | ✅ |
| `x.divide(y)` | `IntegerType` | `BuiltinIR` | Floored, `0 / 0 = 0` | ✅ |
| `x.remainder(y)` | `IntegerType` | `BuiltinIR` | Floored | ✅ |
| `x.pow(y)` | `IntegerType` | `BuiltinIR` | | ✅ |
| `x.abs()` | `IntegerType` | `BuiltinIR` | | ✅ |
| `x.sign()` | `IntegerType` | `BuiltinIR` | | ✅ |
| `x.log(y)` | `IntegerType` | `BuiltinIR` | Floored, to custom base | ✅ |
| `x.toFloat()` | `FloatType` | `BuiltinIR` - `IntegerToFloat` | Can be approximate for very large integers | ✅ |
| `East.Integer.printCommaSeparated(x)` | `StringType` | Function & call | Format with comma separators like "1,234,567" | ✅ |
| `East.Integer.printCompact(x)` | `StringType` | Function & call | Format with business units like "21.5K", "1.82M", "314B" | ✅ |
| `East.Integer.printCompactSI(x)` | `StringType` | Function & call | Format with SI units like "21.5k", "1.82M", "314G" | ✅ |
| `East.Integer.printCompactComputing(x)` | `StringType` | Function & call | Format with binary units (1024) like "21.5ki", "1.82Mi", "314Gi" | ✅ |
| `East.Integer.printOrdinal(x)` | `StringType` | Function & call | Format as ordinal like "1st", "2nd", "3rd", "4th" | ✅ |
| `East.Integer.digitCount(x)` | `IntegerType` | Function & call | Count decimal digits (excluding sign) | ✅ |
| `East.Integer.roundNearest(x, step)` | `IntegerType` | Function & call | Round to nearest multiple of step | ✅ |
| `East.Integer.roundUp(x, step)` | `IntegerType` | Function & call | Round up to next multiple of step (ceiling) | ✅ |
| `East.Integer.roundDown(x, step)` | `IntegerType` | Function & call | Round down to previous multiple of step (floor) | ✅ |
| `East.Integer.roundTruncate(x, step)` | `IntegerType` | Function & call | Round towards zero to nearest multiple of step | ✅ |

**Should rounding be Expr methods?**

## `FloatType`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `x.negate()` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.add(y)` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.subtract(y)` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.multiply(y)` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.divide(y)` | `FloatType` | `BuiltinIR` | `0.0 / 0.0 = NaN` | ✅ |
| `x.remainder(y)` | `FloatType` | `BuiltinIR` | Floored | ✅ |
| `x.pow(y)` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.abs()` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.sign()` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.exp()` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.log()` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.sin()` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.cos()` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.tan()` | `FloatType` | `BuiltinIR` | | ✅ |
| `x.toInteger()` | `IntegerType`❗ | `BuiltinIR` - `FloatToInteger` | Fallible, must be exact integer and in range | ✅ |
| `x.roundNearest()` | `FloatType` | `BuiltinIR` | (TODO) | ➕ |
| `x.roundDown()` | `FloatType` | `BuiltinIR` | (TODO) | ➕ |
| `x.roundUp()` | `FloatType` | `BuiltinIR` | (TODO) | ➕ |
| `x.roundTruncate()` | `FloatType` | `BuiltinIR` | (TODO) | ➕ |
| `x.roundNearestToInteger()` | `IntegerType`❗ | `BuiltinIR` | Fallible (TODO) | ➕ |
| `x.roundDownToInteger()` | `IntegerType`❗ | `BuiltinIR` | Fallible (TODO) | ➕ |
| `x.roundUpToInteger()` | `IntegerType`❗ | `BuiltinIR` | Fallible (TODO) | ➕ |
| `x.roundTruncateToInteger()` | `IntegerType`❗ | `BuiltinIR` | Fallible (TODO) | ➕ |
| `East.Float.printCompact(x)` | `StringType` | Function & call | Format with business units like "21.5K", "1.82M", "314B" (TODO) | ➕ |
| `East.Float.printCompactSI(x)` | `StringType` | Function & call | Format with SI units like "21.5k", "1.82M", "314G" (TODO) | ➕ |

**Should rounding be Expr methods?**

## `StringType`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `str.parse(type: T)` | `T`❗ | `BuiltinIR` | Fallible | ✅ |
| `str.concat(str2)` | `StringType` | `BuiltinIR` | | ✅ |
| `str.repeat(n: IntegerType)` | `StringType` | `BuiltinIR` | | ✅ |
| `str.length()` | `IntegerType` | `BuiltinIR` | | ✅ |
| `str.upperCase()` | `StringType` | `BuiltinIR` | | ✅ |
| `str.lowerCase()` | `StringType` | `BuiltinIR` | | ✅ |
| `str.split(seperator)` | `ArrayType<StringType>` | `BuiltinIR` | | ✅ |
| `str.trim()` | `StringType` | `BuiltinIR` | | ✅ |
| `str.trimStart()` | `StringType` | `BuiltinIR` | | ✅ |
| `str.trimEnd()` | `StringType` | `BuiltinIR` | | ✅ |
| `str.startsWith(prefix)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `str.endsWith(suffix)` | `BooleanType` | `BuiltinIR` | | ✅ |
| `str.contains(substring: StringType)` | `BooleanType` | `BuiltinIR` - `StringContains` | | ✅ |
| `str.contains(pattern: Regex)` | `BooleanType` | `BuiltinIR` - `RegexContains` | | ✅ |
| `str.indexOf(substring: StringType)` | `IntegerType` | `BuiltinIR` - `StringContains` | | ✅ |
| `str.indexOf(pattern: Regex)` | `IntegerType` | `BuiltinIR` - `RegexContains` | | ✅ |
| `str.replace(substring: StringType, str2)` | `IntegerType` | `BuiltinIR` - `StringReplace` | | ✅ |
| `str.replace(pattern: Regex, str2)` | `IntegerType` | `BuiltinIR` - `RegexReplace` | | ✅ |
| `str.encodeUtf8()` | `BlobType` | `BuiltinIR` | Maybe add parameter for UFT-8 BOM? | ✅ |
| `str.parseJson(type: T)` | `T`❗ | `BuiltinIR` - `StringParseJSON` | Fallible | ✅ |
| `East.String.printError(message, stack)` | `StringType` | Macro of builtins | Pretty-print stack trace| ✅ |
| `East.String.printJson(value: T)` | `T` | `BuiltinIR` - `StringPrintJSON` | Like `JSON.stringify` | ✅ |

TODO:
 - padStart, padEnd, uriEncode, uriDecode, fancy capitalization (??), reverse (??)

## `DateTimeType`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `date.getYear()` | `IntegerType` | `BuiltinIR` - `DateTimeGetYear` | | ✅ |
| `date.getMonth()` | `IntegerType` | `BuiltinIR` - `DateTimeGetMonth` | 1-12 | ✅ |
| `date.getDayOfMonth()` | `IntegerType` | `BuiltinIR` - `DateTimeGetDayOfMonth` | 1-31 | ✅ |
| `date.getHour()` | `IntegerType` | `BuiltinIR` - `DateTimeGetHour` | 0-23 | ✅ |
| `date.getMinute()` | `IntegerType` | `BuiltinIR` - `DateTimeGetMinute` | 0-59 | ✅ |
| `date.getSecond()` | `IntegerType` | `BuiltinIR` - `DateTimeGetSecond` | 0-59 | ✅ |
| `date.getDayOfWeek()` | `IntegerType` | `BuiltinIR` - `DateTimeGetDayOfWeek` | 0-6, Sunday=0 | ✅ |
| `date.getMillisecond()` | `IntegerType` | `BuiltinIR` - `DateTimeGetMillisecond` | 0-999 | ✅ |
| `date.addMilliseconds(ms: IntegerType \| FloatType)` | `DateTimeType` | `BuiltinIR` - `DateTimeAddMilliseconds` | Float rounded to nearest ms | ✅ |
| `date.subtractMilliseconds(ms: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerNegate`/`FloatNegate` + `DateTimeAddMilliseconds` | | ✅ |
| `date.addSeconds(s: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.subtractSeconds(s: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerNegate` + `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.addMinutes(m: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.subtractMinutes(m: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerNegate` + `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.addHours(h: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.subtractHours(h: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerNegate` + `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.addDays(d: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.subtractDays(d: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerNegate` + `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.addWeeks(w: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.subtractWeeks(w: IntegerType \| FloatType)` | `DateTimeType` | Macro of `IntegerNegate` + `IntegerMultiply` + `DateTimeAddMilliseconds` | | ✅ |
| `date.durationMilliseconds(other: DateTimeType)` | `IntegerType` | `BuiltinIR` - `DateTimeDurationMilliseconds` | Positive if other > this | ✅ |
| `date.durationSeconds(other: DateTimeType)` | `FloatType` | Macro of `DateTimeDurationMilliseconds` + `IntegerToFloat` + `FloatDivide` | | ✅ |
| `date.durationMinutes(other: DateTimeType)` | `FloatType` | Macro of `DateTimeDurationMilliseconds` + `IntegerToFloat` + `FloatDivide` | | ✅ |
| `date.durationHours(other: DateTimeType)` | `FloatType` | Macro of `DateTimeDurationMilliseconds` + `IntegerToFloat` + `FloatDivide` | | ✅ |
| `date.durationDays(other: DateTimeType)` | `FloatType` | Macro of `DateTimeDurationMilliseconds` + `IntegerToFloat` + `FloatDivide` | | ✅ |
| `date.durationWeeks(other: DateTimeType)` | `FloatType` | Macro of `DateTimeDurationMilliseconds` + `IntegerToFloat` + `FloatDivide` | | ✅ |
| `date.toEpochMilliseconds()` | `IntegerType` | `BuiltinIR` - `DateTimeToEpochMilliseconds` | Milliseconds since Unix epoch | ✅ |
| `East.DateTime.fromEpochMilliseconds(ms: IntegerType)` | `DateTimeType` | `FunctionIR` wrapping `DateTimeFromEpochMilliseconds` | Create DateTime from Unix epoch milliseconds | ✅ |
| `East.DateTime.fromComponents(year, month, day, hour, minute, second, millisecond)` | `DateTimeType`❗ | `FunctionIR` wrapping `DateTimeFromComponents` | Fallible | ✅ |
| `date.printFormated(format)` | `DateTimeType` | Builtin? | Print formatted datetime (validate format statically) | ➕ |
| `East.DateTime.parseFormatted(str: StringType, format)` | `DateTimeType`❗ | Builtin? | Create DateTime from string of given format, fallible | ➕ |
| `East.DateTime.roundNearestSecond(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundUpSecond(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundDownSecond(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundNearestMinute(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundUpMinute(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundDownMinute(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundNearestHour(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundUpHour(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundDownHour(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundNearestDay(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundUpDay(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundDownDay(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundNearestWeek(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundUpWeek(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundDownWeek(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundDownMonth(step?)` | `DateTimeType` | Function | | ✅ |
| `East.DateTime.roundDownYear(step?)` | `DateTimeType` | Function | | ✅ |

**Should rounding be Expr methods?**

## `BlobType`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `blob.size()` | `IntegerType` | `BuiltinIR` - `BlobSize` | Number of bytes in blob | ✅ |
| `blob.getUint8(offset)` | `IntegerType`❗ | `BuiltinIR` - `BlobGetUint8` | Get Uint8 at offset (0-255), errors on out-of-bounds | ✅ |
| `blob.getInt8(offset)` | `IntegerType`❗ | `BuiltinIR` - `BlobGetUint8` | Get Int8 at offset (0-255), errors on out-of-bounds | ➕❔ |
| `blob.getUint16(offset)` | `IntegerType`❗ | `BuiltinIR` - `BlobGetUint8` | Get Uint16 at offset (0-255), errors on out-of-bounds | ➕❔ |
| `blob.getInt16(offset)` | `IntegerType`❗ | `BuiltinIR` - `BlobGetUint8` | Get Int16 at offset (0-255), errors on out-of-bounds | ➕❔ |
| `blob.getUint32(offset)` | `IntegerType`❗ | `BuiltinIR` - `BlobGetUint8` | Get Uint32 at offset (0-255), errors on out-of-bounds | ➕❔ |
| `blob.getInt32(offset)` | `IntegerType`❗ | `BuiltinIR` - `BlobGetUint8` | Get Int32 at offset (0-255), errors on out-of-bounds | ➕❔ |
| `blob.getInt64(offset)` | `IntegerType`❗ | `BuiltinIR` - `BlobGetUint8` | Get Int64 at offset (0-255), errors on out-of-bounds | ➕❔ |
| `blob.decodeUtf8()` | `StringType`❗ | `BuiltinIR` - `BlobDecodeUtf8` | Decode as UTF-8, errors on invalid UTF-8 | ✅ |
| `blob.decodeUtf16()` | `StringType`❗ | `BuiltinIR` - `BlobDecodeUtf16` | Decode as UTF-16, errors on invalid UTF-16 | ✅ |
| `blob.decodeBeast(type: T, version: 'v1' | 'v2' = 'v1')` | `T`❗ | `BuiltinIR` - `BlobDecodeBeast`/`BlobDecodeBeast2` | Decode binary east format, errors on parsing problem | ✅ |
| `East.Blob.encodeBeast(value: T, version: 'v1' | 'v2' = 'v1')` | `BlobType` | `BuiltinIR` - `BlobEncodeBeast`/`BlobEncodeBeast2` | Encode binary east format | ✅ |

Note: `Uint64` is not representable as a single `IntegerType` value in East.

## `ArrayType<V>`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `array.size()` | `IntegerType` | `BuiltinIR` - `ArraySize` | Number of elements in array | ✅ |
| `array.has(index)` | `BooleanType` | `BuiltinIR` - `ArrayHas` | Check if index is valid (0 <= index < size) | ✅ |
| `array.get(key)` | `V`❗ | `BuiltinIR` - `ArrayGet` | Get element at index, errors on out-of-bounds | ✅ |
| `array.get(key, ($, key) => default)` | `V` | `BuiltinIR` - `ArrayGetOrDefault` | Get element at index, default on out-of-bounds | ✅ |
| `array.tryGet(key)` | `OptionType<V>` | `BuiltinIR` - `ArrayTryGet` | Safe get returning Option | ✅ |
| `array.update(key, value)` | `NullType`❗ | `BuiltinIR` - `ArrayUpdate` | Replace element at index, errors on out-of-bounds | ✅ |
| `array.merge(key, value, updateFn)` | `V` | `BuiltinIR` - `ArrayMerge` | Merge value with existing element using function | ✅ |
| `array.pushLast(value)` | `NullType` | `BuiltinIR` - `ArrayPushLast` | Add element to end of array | ✅ |
| `array.popLast()` | `V`❗ | `BuiltinIR` - `ArrayPopLast` | Remove element from end, errors on empty | ✅ |
| `array.pushFirst(value)` | `NullType` | `BuiltinIR` - `ArrayPushFirst` | Add element to start of array | ✅ |
| `array.popFirst()` | `V`❗ | `BuiltinIR` - `ArrayPopFirst` | Remove element from start, default errors on empty | ✅ |
| `array.pushHeap(value, by?)` | `NullType` | `BuiltinIR` - `ArrayPushHeap` | Assumes already a bin-min-heap | ➕ |
| `array.popHeap(by?)` | `V`❗ | `BuiltinIR` - `ArrayPopHeap` | Assumes already a bin-min-heap, error on empty | ➕ |
| `array.append(array)` | `NullType` | `BuiltinIR` - `ArrayAppend` | Append all elements from another array | ✅ |
| `array.prepend(array)` | `NullType` | `BuiltinIR` - `ArrayPrepend` | Prepend all elements from another array | ✅ |
| `array.mergeAll(array, mergeFn)` | `NullType` | `BuiltinIR` - `ArrayMergeAll` | Merge all elements from another array using function | ✅ |
| `array.clear()` | `NullType` | `BuiltinIR` - `ArrayClear` | Remove all elements | ✅ |
| `array.sortInPlace(by?)` | `NullType` | `BuiltinIR` - `ArraySortInPlace` | Sort array in-place, optional projection function | ✅ |
| `array.sort(by?)` | `ArrayType<V>` | `BuiltinIR` - `ArraySort` | Return new sorted array, optional projection function | ✅ |
| `array.reverseInPlace()` | `NullType` | `BuiltinIR` - `ArrayReverseInPlace` | Reverse array in-place | ✅ |
| `array.reverse()` | `ArrayType<V>` | `BuiltinIR` - `ArrayReverse` | Return new reversed array | ✅ |
| `array.isSorted(by?)` | `BooleanType` | `BuiltinIR` - `ArrayIsSorted` | Check if array is sorted, optional projection function | ✅ |
| `array.slice(start, end)` | `ArrayType<V>` | `BuiltinIR` - `ArraySlice` | Extract subarray | ✅ |
| `array.concat(other)` | `ArrayType<V>` | `BuiltinIR` - `ArrayConcat` | Concatenate two arrays into new array | ✅ |
| `array.getKeys(keys, onMissing?)` | `ArrayType<V>` | `BuiltinIR` - `ArrayGetKeys` | Get multiple elements by indices | ✅❔ |
| `array.forEach(fn)` | `NullType` | `BuiltinIR` - `ArrayForEach` | Execute function for each element | ✅ |
| `array.copy()` | `ArrayType<V>` | `BuiltinIR` - `ArrayCopy` | Create shallow copy of array | ✅ |
| `array.map(fn)` | `ArrayType<U>` | `BuiltinIR` - `ArrayMap` | Transform each element | ✅ |
| `array.filter(predicate)` | `ArrayType<V>` | `BuiltinIR` - `ArrayFilter` | Keep elements matching predicate | ✅ |
| `array.filterMap(fn)` | `ArrayType<U>` | `BuiltinIR` - `ArrayFilterMap` | Combined filter and map using Option | ✅ |
| `array.reduce(combine, init: V)` | `V` | `BuiltinIR` - `ArrayFold` | Reduce with initial value | ✅ |
| `array.mapReduce(fn, combine)` | `ArrayType<U>` | `BuiltinIR` - `ArrayMapReduce` | Map then reduce, error on empty | ✅ |
| `array.firstMap(fn)` | `ReturnType<fn>` | `BuiltinIR` - `ArrayFirstMap` | Like filterMap, but returns first entry eagerly | ✅ |
| `array.every(fn?)` | `BooleanType` | Macro using `ArrayFirstMap` | True if all elements match predicate, returns eagerly | ✅ |
| `array.some(fn?)` | `BooleanType` | Macro using `ArrayFirstMap` | True if any element matches predicate, returns eagerly | ✅ |
| `array.sum()` | `IntegerType \| FloatType` | Macro using `ArrayReduce` | Sum of numeric array | ✅ |
| `array.sum(fn)` | `IntegerType \| FloatType` | Macro using `ArrayReduce` | Sum with projection function | ✅ |
| `array.mean()` | `FloatType` | Macro using `ArrayReduce` | Mean of numeric array, `NaN` on empty | ✅ |
| `array.mean(fn)` | `FloatType` | Macro using `ArrayReduce` | Mean with projection function, `NaN` on empty | ✅ |
| `array.minimum()` | `T`❗ | Macro using `ArrayMapReduce` | Error on empty | ✅ |
| `array.minimum(by)` | `T`❗ | Macro using `ArrayMapReduce` | Choose what to order by - returns whole value | ✅ |
| `array.maximum()` | `T`❗ | Macro using `ArrayMapReduce` | Error on empty | ✅ |
| `array.maximum(by)` | `T`❗ | Macro using `ArrayMapReduce` | Choose what to order by - returns whole value | ✅ |
| `array.findMinimum()` | `OptionType<IntegerType>` | Macro using `ArrayMapReduce` | | ✅ |
| `array.findMinimum(fn)` | `OptionType<IntegerType>` | Macro using `ArrayMapReduce` | | ✅ |
| `array.findMaximum()` | `OptionType<IntegerType>` | Macro using `ArrayMapReduce` | | ✅ |
| `array.findMaximum(fn)` | `OptionType<IntegerType>` | Macro using `ArrayMapReduce` | | ✅ |
| `array.findFirst(value)` | `OptionType<IntegerType>` | Index of a value. Macro using `ArrayFirstMap` | | ✅ |
| `array.findFirst(value, by)` | `OptionType<IntegerType>` | Index where a projected value matches a provided value. Macro using `ArrayFirstMap` | | ✅ |
| `array.findAll(value)` | `ArrayType<IntegerType>` | Indices of a value. Macro using `ArrayFilterMap` | | ✅ |
| `array.findAll(value, by)` | `ArrayType<IntegerType>` | Index where a projected value matches a provided value. Macro using `ArrayFilterMap` | | ✅ |
| `array.stringJoin(separator)` | `StringType` | `BuiltinIR` - `ArrayStringJoin` | Join string array with separator | ✅ |
| `array.toSet(keyFn?)` | `SetType<K>` | `BuiltinIR` - `ArrayToSet` | Convert to set with key function, ignoring duplicates | ✅ |
| `array.toDict(keyFn, valueFn?, onConflictFn?)` | `DictType<K, U>` | `BuiltinIR` - `ArrayToDict` | Convert to dict with custom key/value functions | ✅ |
| `array.flatMap()` | `ArrayType<U>` | `BuiltinIR` - `ArrayFlattenToArray` | Flatten array of arrays | ✅ |
| `array.flatMap(fn)` | `ArrayType<U>` | `BuiltinIR` - `ArrayFlattenToArray` | Map then flatten | ✅ |
| `array.flattenToSet(fn?)` | `SetType<ReturnType<fn>>` | `BuiltinIR` - `ArrayFlattenToSet` | Flatten elements to set, ignoring duplicates | ✅ |
| `array.flattenToDict()` | `DictType<K, V>` | `BuiltinIR` - `ArrayFlattenToDict` | Flatten array of dicts | ✅ |
| `array.flattenToDict(fn, onConflictFn?)` | `DictType<K, V>` | `BuiltinIR` - `ArrayFlattenToDict` | Flatten with custom function | ✅ |
| `array.groupReduce(byFn, initFn, combineFn)` | `DictType<ReturnType<byFn>, ReturnType<initFn>>` | `BuiltinIR` - `ArrayGroupFold` | Group data and perform folds per group | ✅ |
| `array.groupToArrays(byFn, valueFn?)` | `DictType<ReturnType<byFn>, ArrayType<ReturnType<valueFn>>` | Macro: `groupReduce`, collect with `pushLast` | Group data into arrays | ✅ |
| `array.groupToSets(byFn, keyFn?)` | `DictType<ReturnType<byFn>, SetType<ReturnType<keyFn>>` | Macro: `groupReduce`, collect with `tryInsert` | Group data into sets, ignore duplicates | ✅ |
| `array.groupToDicts(byFn, keyFn, valueFn?)` | `DictType<ReturnType<byFn>, DictType<ReturnType<keyFn>, ReturnType<valueFn>>>`❗ | Macro: `groupReduce` with empty dict init, collect with `insert` | Group data into dicts, error on key clash | ✅ |
| `array.groupToDicts(byFn, keyFn, valueFn, combineFn)` | `DictType<ReturnType<byFn>, DictType<ReturnType<keyFn>, ReturnType<valueFn>>>` | Macro: `groupReduce` with empty dict init, collect with `merge(key, value, combineFn)` | Group data into dicts with conflict resolution  | ✅ |
| `array.groupSize(byFn?)` | `DictType<ReturnType<byFn>, IntegerType>` | Macro: `toDict` map to 1, add | Count elements per group | ✅ |
| `array.groupEvery(byFn, predFn)` | `DictType<ReturnType<byFn>, BooleanType>` | Macro: `groupReduce` with short-circuit `.and()` | Check all elements match predicate | ✅ |
| `array.groupSome(byFn, predFn)` | `DictType<ReturnType<byFn>, BooleanType>` | Macro: `groupReduce` with short-circuit `.or()` | Check any element matches predicate | ✅ |
| `array.groupSum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, ReturnType<valueFn>>` | Macro: `toDict`, add values | Sum values per group | ✅ |
| `array.groupMean(byFn, valueFn?)` | `DictType<ReturnType<byFn>, FloatType>` | Macro: `toDict` track {sum, count}, then `.map()` divide | Compute mean per group | ✅ |
| `array.groupMinimum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, V>` | Macro: `toDict` track {by, elem}, then `.map()` extract elem | Minimum element per group (returns element) | ✅ |
| `array.groupMaximum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, V>` | Macro: `toDict` track {by, elem}, then `.map()` extract elem | Maximum element per group (returns element) | ✅ |
| `array.groupFindFirst(byFn, value, projFn?)` | `DictType<ReturnType<byFn>, OptionType<IntegerType>>` | Macro: like `findFirst(value, by?)` per group | First index where projected value matches per group | ✅ |
| `array.groupFindAll(byFn, value, projFn?)` | `DictType<ReturnType<byFn>, ArrayType<IntegerType>>` | Macro: like `findAll(value, by?)` per group | All indices where projected value matches per group | ✅ |
| `array.groupFindMinimum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, IntegerType>` | Macro: `toDict` track {by, index}, then `.map()` extract index | Index of minimum value per group | ✅ |
| `array.groupFindMaximum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, IntegerType>` | Macro: `toDict` track {by, index}, then `.map()` extract index | Index of maximum value per group | ✅ |
| `East.Array.generate(n, ($, i) => V)` | `ArrayType<V>` | Builtin | | ✅ |
| `East.Array.range(inclusive_min, exclusive_max, step?)` | `ArrayType<IntegerType>` | Builtin | | ✅ |
| `East.Array.linspace(inclusive_min, inclusive_max, n)` | `ArrayType<FloatType>` | Builtin | | ✅ |

## `SetType<K>`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `set.size()` | `IntegerType` | `BuiltinIR` - `SetSize` | Number of elements in set | ✅ |
| `set.has(key)` | `BooleanType` | `BuiltinIR` - `SetHas` | Check if key exists in set | ✅ |
| `set.insert(key)` | `NullType`❗ | `BuiltinIR` - `SetInsert` | Insert key, errors on conflict | ✅ |
| `set.tryInsert(key)` | `BooleanType` | `BuiltinIR` - `SetTryInsert` | Safe insert returning success boolean | ✅ |
| `set.delete(key)` | `NullType`❗ | `BuiltinIR` - `SetDelete` | Delete key, errors on missing | ✅ |
| `set.tryDelete(key)` | `BooleanType` | `BuiltinIR` - `SetTryDelete` | Safe delete returning success boolean | ✅ |
| `set.clear()` | `NullType` | `BuiltinIR` - `SetClear` | Remove all elements | ✅ |
| `set.unionInPlace(other)` | `NullType` | `BuiltinIR` - `SetUnionInPlace` | Add all elements from other set (mutating) | ✅ |
| `set.union(other)` | `SetType<K>` | `BuiltinIR` - `SetUnion` | Return new set with union | ✅ |
| `set.intersection(other)` | `SetType<K>` | `BuiltinIR` - `SetIntersect` | Return new set with intersection | ✅ |
| `set.difference(other)` | `SetType<K>` | `BuiltinIR` - `SetDiff` | Return new set with difference (in this, not in other) | ✅ |
| `set.symmetricDifference(other)` | `SetType<K>` | `BuiltinIR` - `SetSymDiff` | Return new set with symmetric difference | ✅ |
| `set.isSubsetOf(other)` | `BooleanType` | `BuiltinIR` - `SetIsSubset` | Check if this is subset of other | ✅ |
| `set.isSupersetOf(other)` | `BooleanType` | `BuiltinIR` - `SetIsSubset` | Check if this is superset of other | ✅ |
| `set.isDisjointFrom(other)` | `BooleanType` | `BuiltinIR` - `SetIsDisjoint` | Check if sets have no common elements | ✅ |
| `set.copy()` | `SetType<K>` | `BuiltinIR` - `SetCopy` | Create shallow copy of set | ✅ |
| `set.filter(predicate)` | `SetType<K>` | `BuiltinIR` - `SetFilter` | Keep elements matching predicate | ✅ |
| `set.filterMap(fn)` | `DictType<K, V2>` | `BuiltinIR` - `SetFilterMap` | Combined filter and map using Option | ✅ |
| `set.forEach(fn)` | `NullType` | `BuiltinIR` - `SetForEach` | Execute function for each element | ✅ |
| `set.reduce(combineFn, init: V)` | `V` | `BuiltinIR` - `SetReduce` | Reduce with initial value | ✅ |
| `set.mapReduce(mapFn, combineFn)` | `ReturnType<mapFn>`❗ | `BuiltinIR` - `SetMapReduce` | Map-reduce without initial value | ✅ |
| `set.firstMap(fn)` | `ReturnType<fn>` | `BuiltinIR` - `SetFirstMap` | Like filterMap, but returns first entry eagerly (as option) | ✅ |
| `set.map(fn)` | `DictType<K, V>` | `BuiltinIR` - `SetMap` | Map to dict with same keys, new values | ✅ |
| `set.every(fn?)` | `BooleanType` | Macro using `SetFirstMap` | True if all elements match predicate (early termination) | ✅ |
| `set.some(fn?)` | `BooleanType` | Macro using `SetFirstMap` | True if any element matches predicate (early termination) | ✅ |
| `set.sum()` | `IntegerType \| FloatType` | Macro using `SetReduce` | Sum of numeric set | ✅ |
| `set.sum(fn)` | `IntegerType \| FloatType` | Macro using `SetReduce` | Sum with projection function | ✅ |
| `set.mean()` | `FloatType` | Macro using `SetReduce` | Mean of numeric set, `NaN` on empty | ✅ |
| `set.mean(fn)` | `FloatType` | Macro using `SetReduce` | Mean with projection function, `NaN` on empty | ✅ |
| `set.toArray()` | `ArrayType<K>` | `BuiltinIR` - `SetToArray` | Convert to array | ✅ |
| `set.toArray(fn)` | `ArrayType<V>` | `BuiltinIR` - `SetToArray` | Convert to array with mapping function | ✅ |
| `set.toSet(keyFn?)` | `SetType<U>` | `BuiltinIR` - `SetToSet` | Convert to set, ignore duplicates | ✅ |
| `set.toDict()` | `DictType<K, K>` | `BuiltinIR` - `SetToDict` | Convert to dict (key -> key) | ✅ |
| `set.toDict(keyFn, valueFn, onConflictFn?)` | `DictType<K2, V>` | `BuiltinIR` - `SetToDict` | Convert to dict with custom key/value functions | ✅ |
| `set.flattenToArray(fn)` | `ArrayType<V>` | `BuiltinIR` - `SetFlattenToArray` | Flatten set of collections to array | ✅ |
| `set.flattenToSet(fn?)` | `SetType<ReturnType<fn>>` | `BuiltinIR` - `SetFlattenToSet` | Flatten elements to set, ignoring duplicates | ✅ |
| `set.flattenToDict(fn, onConflictFn?)` | `DictType<K, V>` | `BuiltinIR` - `SetFlattenToDict` | Flatten set of dicts | ✅ |
| `set.groupReduce(byFn, initFn, combineFn)` | `DictType<ReturnType<byFn>, ReturnType<initFn>>` | `BuiltinIR` - `SetGroupFold` | Group data and perform reductions/folds per group | ✅ |
| `set.groupToArrays(byFn, valueFn?)` | `DictType<ReturnType<byFn>, ArrayType<ReturnType<valueFn>>` | Macro using `groupReduce` | Group data into arrays | ✅ |
| `set.groupToSets(byFn, keyFn?)` | `DictType<ReturnType<byFn>, SetType<ReturnType<keyFn>>` | Macro using `groupReduce` | Group data into sets, ignore if not unique | ✅ |
| `set.groupToDicts(byFn, keyFn, valueFn?)` | `DictType<ReturnType<byFn>, DictType<ReturnType<keyFn>, ReturnType<valueFn>>>`❗ | Macro using `groupReduce` | Group data into dicts, error if keys clash | ✅ |
| `set.groupToDicts(byFn, keyFn, valueFn, combineFn)` | `DictType<ReturnType<byFn>, DictType<ReturnType<keyFn>, ReturnType<valueFn>>>` | Macro using `groupReduce` | Group data into dicts, merge if keys clash | ✅ |
| `set.groupSize(byFn?)` | `DictType<ReturnType<byFn>, IntegerType>` | Macro using `toDict` | Count number of elements within each group | ✅ |
| `set.groupEvery(byFn, predFn)` | `DictType<ReturnType<byFn>, BooleanType>` | Macro using `groupReduce` | Is no predicate in the group `false` | ✅ |
| `set.groupSome(byFn, predFn)` | `DictType<ReturnType<byFn>, BooleanType>` | Macro using `groupReduce` | Is at least predicate in the group `true` | ✅ |
| `set.groupSum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, ReturnType<valueFn>>` | Macro using `toDict` | Sum of value by group | ✅ |
| `set.groupMean(byFn, valueFn?)` | `DictType<ReturnType<byFn>, FloatType>` | Macro using `toDict` | Mean of value by group | ✅ |
| `set.groupMinimum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, K>` | Macro | Minimum value per group | ➕ |
| `set.groupMaximum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, K>` | Macro | Maximum value per group | ➕ |
| `set.groupFindFirst(byFn, value, projFn?)` | `DictType<ReturnType<byFn>, OptionType<K>>` | Macro: like `findFirst(value, by?)` per group | First key where projected value matches per group | ➕ |
| `set.groupFindAll(byFn, value, projFn?)` | `DictType<ReturnType<byFn>, ArrayType<K>>` | Macro: like `findAll(value, by?)` per group | All keys where projected value matches per group | ➕ |
| `set.groupFindMinimum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, K>` | Macro | Original key of minimum value per group | ➕ |
| `set.groupFindMaximum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, K>` | Macro | Original key of maximum value per group | ➕ |
| `East.Set.generate(n, ($, i) => K)` | `SetType<K>` | Builtin | | ✅ |

## `DictType<K, V>`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `dict.size()` | `IntegerType` | `BuiltinIR` - `DictSize` | Number of key-value pairs in dict | ✅ |
| `dict.has(key)` | `BooleanType` | `BuiltinIR` - `DictHas` | Check if key exists in dict | ✅ |
| `dict.get(key)` | `V`❗ | `BuiltinIR` - `DictGet` | Get value for key,  errors on missing | ✅ |
| `dict.get(key, $ => default)` | `V` | `BuiltinIR` - `DictGetOrDefault` | Get value for key, or default value on missing | ✅ |
| `dict.tryGet(key)` | `OptionType<V>` | `BuiltinIR` - `DictTryGet` | Safe get returning Option | ✅ |
| `dict.insert(key, value)` | `NullType`❗ | `BuiltinIR` - `DictInsert` | Insert key-value pair, default errors on conflict | ✅ |
| `dict.insertOrUpdate(key, value)` | `NullType` | `BuiltinIR` - `DictInsertOrUpdate` | Insert or update key-value pair | ✅ |
| `dict.update(key, value)` | `NullType`❗ | `BuiltinIR` - `DictUpdate` | Update existing key, errors on missing | ✅ |
| `dict.merge(key, value, mergeFn)` | `NullType`❗ | `BuiltinIR` - `DictMerge` | Merge value into existing key, errors on missing | ✅ |
| `dict.merge(key, value, mergeFn, initFn)` | `NullType` | `BuiltinIR` - `DictMerge2`? | Merge value into existing key, provide initializer for missing | ✅ |
| `dict.getOrInsert(key, defaultValue)` | `V` | `BuiltinIR` - `DictGetOrInsert` | Get value or insert default if missing | ✅ |
| `dict.delete(key)` | `NullType`❗ | `BuiltinIR` - `DictDelete` | Delete key, errors on missing | ✅ |
| `dict.tryDelete(key)` | `BooleanType` | `BuiltinIR` - `DictTryDelete` | Safe delete returning success boolean | ✅ |
| `dict.pop(key)` | `V`❗ | `BuiltinIR` - `DictPop` | Remove and return value, errors on missing | ✅ |
| `dict.swap(key, value)` | `V`❗ | `BuiltinIR` - `DictSwap` | Replace value and return old value, default errors on missing | ✅ |
| `dict.clear()` | `NullType` | `BuiltinIR` - `DictClear` | Remove all key-value pairs | ✅ |
| `dict.unionInPlace(other, merger?)` | `NullType` | `BuiltinIR` - `DictUnionInPlace` | Union in other dict in-place, merge function defaults to error (reduce pattern) | ✅ |
| `dict.mergeAll(other, merger, initialFn?)` | `NullType` | `BuiltinIR` - `DictUnionInPlace` | Merge other dict in-place, merging the values in a fold pattern | ✅ |
| `dict.keys()` | `SetType<K>` | `BuiltinIR` - `DictKeys` | Get set of all keys | ✅ |
| `dict.getKeys(keys, onMissing?)` | `DictType<K, V>` | `BuiltinIR` - `DictGetKeys` | Get multiple key-value pairs by keys | ✅ |
| `dict.forEach(fn)` | `NullType` | `BuiltinIR` - `DictForEach` | Execute function for each key-value pair | ✅ |
| `dict.copy()` | `DictType<K, V>` | `BuiltinIR` - `DictCopy` | Create shallow copy of dict | ✅ |
| `dict.map(fn)` | `DictType<K, U>` | `BuiltinIR` - `DictMap` | Transform values, keeping keys | ✅ |
| `dict.filter(predicate)` | `DictType<K, V>` | `BuiltinIR` - `DictFilter` | Keep key-value pairs matching predicate | ✅ |
| `dict.filterMap(fn)` | `DictType<K, U>` | `BuiltinIR` - `DictFilterMap` | Combined filter and map using Option | ✅ |
| `dict.reduce(combineFn, init: V)` | `V` | `BuiltinIR` - `DictReduce` | Reduce with initial value | ✅ |
| `dict.mapReduce(mapFn, combineFn)` | `ReturnType<mapFn>`❗ | `BuiltinIR` - `DictMapReduce` | Map-reduce without initial value | ✅ |
| `dict.firstMap(fn)` | `ReturnType<fn>` | `BuiltinIR` - `DictFirstMap` | Like filterMap, but returns first entry eagerly (as option) | ✅ |
| `dict.every(fn?)` | `BooleanType` | Macro using `DictFirstMap` | True if all key-value pairs match predicate (early termination) | ✅ |
| `dict.some(fn?)` | `BooleanType` | Macro using `DictFirstMap` | True if any key-value pair matches predicate (early termination) | ✅ |
| `dict.sum()` | `IntegerType \| FloatType` | Macro using `DictReduce` | Sum of numeric values | ✅ |
| `dict.sum(fn)` | `IntegerType \| FloatType` | Macro using `DictReduce` | Sum with projection function | ✅ |
| `dict.mean()` | `FloatType` | Macro using `DictReduce` | Mean of numeric values, `NaN` on empty | ✅ |
| `dict.mean(fn)` | `FloatType` | Macro using `DictReduce` | Mean with projection function, `NaN` on empty | ✅ |
| `dict.minimum()` | `V`❗ | Macro using `DictMapReduce` | Minimum value, error on empty | ➕ |
| `dict.minimum(by)` | `V`❗ | Macro using `DictMapReduce` | Minimum value with projection - returns whole value | ➕ |
| `dict.maximum()` | `V`❗ | Macro using `DictMapReduce` | Maximum value, error on empty | ➕ |
| `dict.maximum(by)` | `V`❗ | Macro using `DictMapReduce` | Maximum value with projection - returns whole value | ➕ |
| `dict.findMinimum()` | `OptionType<K>` | Macro using `DictMapReduce` | Find key of minimum value | ➕ |
| `dict.findMinimum(fn)` | `OptionType<K>` | Macro using `DictMapReduce` | Find key of minimum projected value | ➕ |
| `dict.findMaximum()` | `OptionType<K>` | Macro using `DictMapReduce` | Find key of maximum value | ➕ |
| `dict.findMaximum(fn)` | `OptionType<K>` | Macro using `DictMapReduce` | Find key of maximum projected value | ➕ |
| `dict.findFirst(value)` | `OptionType<K>` | Macro using `DictFirstMap` | Find first key where value matches | ➕ |
| `dict.findFirst(value, by)` | `OptionType<K>` | Macro using `DictFirstMap` | Find first key where projected value matches | ➕ |
| `dict.findAll(value)` | `ArrayType<K>` | Macro using `DictFilterMap` | Find all keys where value matches | ➕ |
| `dict.findAll(value, by)` | `ArrayType<K>` | Macro using `DictFilterMap` | Find all keys where projected value matches | ➕ |
| `dict.toArray()` | `ArrayType<V>` | `BuiltinIR` - `DictToArray` | Convert values to array | ✅ |
| `dict.toArray(fn)` | `ArrayType<U>` | `BuiltinIR` - `DictToArray` | Convert to array with mapping function | ✅ |
| `dict.toSet(keyFn?)` | `SetType<U>` | `BuiltinIR` - `DictToSet` | Convert to set, ignoring duplicates | ✅ |
| `dict.toDict(keyFn, valueFn?, onConflictFn?)` | `DictType<K2, V2>` | `BuiltinIR` - `DictToDict` | Convert to dict with custom key/value functions | ✅ |
| `dict.flattenToArray()` | `ArrayType<U>` | `BuiltinIR` - `DictFlattenToArray` | Flatten dict of arrays | ✅ |
| `dict.flattenToArray(fn)` | `ArrayType<U>` | `BuiltinIR` - `DictFlattenToArray` | Flatten with custom function | ✅ |
| `dict.flattenToSet(fn?)` | `SetType<ReturnType<fn>>` | `BuiltinIR` - `DictFlattenToSet` | Flatten elements to set, ignoring duplicates | ✅|
| `dict.flattenToDict()` | `DictType<K2, V2>` | `BuiltinIR` - `DictFlattenToDict` | Flatten dict of dicts | ✅ |
| `dict.flattenToDict(fn, onConflictFn?)` | `DictType<K2, V2>` | `BuiltinIR` - `DictFlattenToDict` | Flatten with custom function | ✅ |
| `dict.groupReduce(byFn, initFn, combineFn)` | `DictType<ReturnType<byFn>, ReturnType<initFn>>` | Macro | Group data and perform folds per group | ✅ |
| `dict.groupToArrays(byFn, valueFn?)` | `DictType<ReturnType<byFn>, ArrayType<ReturnType<valueFn>>` | Macro | Group data into arrays | ✅ |
| `dict.groupToSets(byFn, keyFn?)` | `DictType<ReturnType<byFn>, SetType<ReturnType<keyFn>>` | Macro | Group data into sets, ignore if not unique | ✅ |
| `dict.groupToDicts(byFn, keyFn, valueFn?)` | `DictType<ReturnType<byFn>, DictType<ReturnType<keyFn>, ReturnType<valueFn>>>`❗ | Macro | Group data into dicts, error if keys clash | ✅ |
| `dict.groupToDicts(byFn, keyFn, valueFn, combineFn)` | `DictType<ReturnType<byFn>, DictType<ReturnType<keyFn>, ReturnType<valueFn>>>` | Macro | Group data into dicts, merge if keys clash | ✅ |
| `dict.groupSize(byFn?)` | `DictType<ReturnType<byFn>, IntegerType>` | Macro | Count number of elements within each group | ✅ |
| `dict.groupEvery(byFn, predFn)` | `DictType<ReturnType<byFn>, BooleanType>` | Macro | Is no predicate in the group `false` | ✅ |
| `dict.groupSome(byFn, predFn)` | `DictType<ReturnType<byFn>, BooleanType>` | Macro | Is at least predicate in the group `true` | ✅ |
| `dict.groupSum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, ReturnType<valueFn>>` | Macro | Sum of value by group | ✅ |
| `dict.groupMean(byFn, valueFn?)` | `DictType<ReturnType<byFn>, FloatType>` | Macro | Mean of value by group | ✅ |
| `dict.groupMinimum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, V>` | Macro | Minimum value per group | ➕ |
| `dict.groupMaximum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, V>` | Macro | Maximum value per group | ➕ |
| `dict.groupFindFirst(byFn, value, projFn?)` | `DictType<ReturnType<byFn>, OptionType<K>>` | Macro: like `findFirst(value, by?)` per group | First key where projected value matches per group | ➕ |
| `dict.groupFindAll(byFn, value, projFn?)` | `DictType<ReturnType<byFn>, ArrayType<K>>` | Macro: like `findAll(value, by?)` per group | All keys where projected value matches per group | ➕ |
| `dict.groupFindMinimum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, K>` | Macro | Original key of minimum value per group | ➕ |
| `dict.groupFindMaximum(byFn, valueFn?)` | `DictType<ReturnType<byFn>, K>` | Macro | Original key of maximum value per group | ➕ |
| `East.Dict.generate(n, ($, i) => K, ($, i) => V)` | `DictType<K, V>` | Builtin | | ✅ |

## `StructType<Fields>`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `struct.field` | `Fields[field]` | `BuiltinIR` | | ✅ |

Note: all other struct operations live in `East`, like `East.equal`, etc.

## `VariantType<Cases>`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `variant.match({ case1: ($, data) => { ... }, ... })` | `TypeUnion` of case results | `MatchIR` | Inserts `AsIR` for type stability, might need builder pattern here? | ➖ |
| `variant.match(b => b.case("case1", ($, data => { ... }).else($ => { ... })))` | `TypeUnion` of case results | `MatchIR` | Inserts `AsIR` for type stability, using builder pattern lets TS infer the output better | ➕ |
| `variant.unwrap(case)` | `Cases[case]` | Macro of `match` | Throws error if different case, default case "some" | ✅ |
| `variant.unwrap(case, $ => default)` | `Cases[case]` | Macro of `match` | Returns default if different case, default case "some" | ✅ |
| `variant.getTag()` | `StringType` | Macro of `match` | | ✅ |
| `variant.hasTag()` | `BooleanType` | Macro of `match` | | ✅ |
| `variant.map(($, value) => { ... }, case?)` | `BooleanType` | Macro of `match` | transform one of the wrapped variants, default case "some" | ➕ |

Note: `AsIR` is a type-widening conversion, which ensures Julia type stability.

## `FunctionType<I, O>`

| Usage | Returns | IR | Notes | Status |
| - | - | - | - | - |
| `f(...args)` | `O` | `BuiltinIR` | Overload of native JS call syntax | ✅ |
| `f.toIR()` | `Cases[case]` | `EastIR` | `f` must be a free function | ✅ |

The `EastIR` class has methods for compiling the IR to a callable JavaScript function, for serializing the IR as JSON, and a static method to deserialize IR from JSON.

TODO
 - do we want an `East.pipe(x, f1, f2, ...)` convenience function?
 - `f.compose(g)`?

## TODOs

(Meaning required modifications to _this document_)

 - Make clear what lives on expr methods and what is a library function
 - Where do median, variance, quantiles, etc live?

## Pattern Matching with Struct Projections

East should support convenient pattern matching on structs for find operations and comparisons. When a struct pattern is provided, East automatically generates a projection function and performs standard equality/comparison on the projected values.

### Type Constraints

Three levels of struct pattern constraints:

1. **StructUnorderedSubset**: Any subset of fields in any order (not used here)
2. **StructSubset**: Fields must appear in same relative order as type definition (for equality and ordering comparisons)
3. **StructPrefix**: Contiguous fields from start only (for binary search on sorted data)

Where: `Prefix ⊂ OrderedSubset ⊂ Subset`.

Technically we can use `StructUnorderedSubset` for equality checks but we require the struct fields to be ordered correctly everywhere else such that this appears sloppy.

### New Comparison Methods

| Method | Pattern Type | Returns | Semantics | Status |
| - | - | - | - | - |
| `East.matchEqual(value, pattern)` | `StructSubset<T>` | `BooleanType` | Equality on any field subset | ➕ |
| `East.matchNotEqual(value, pattern)` | `StructSubset<T>` | `BooleanType` | Inequality on any field subset | ➕ |
| `East.matchLess(value, pattern)` | `StructSubset<T>` | `BooleanType` | Lexicographic comparison on ordered subset | ➕ |
| `East.matchLessEqual(value, pattern)` | `StructSubset<T>` | `BooleanType` | Lexicographic comparison on ordered subset | ➕ |
| `East.matchGreater(value, pattern)` | `StructSubset<T>` | `BooleanType` | Lexicographic comparison on ordered subset | ➕ |
| `East.matchGreaterEqual(value, pattern)` | `StructSubset<T>` | `BooleanType` | Lexicographic comparison on ordered subset | ➕ |

**Implementation:** Generates projection function `($, x) => ({ field1: x.field1, ... })` and uses standard equality/comparison.

### Modified Array Methods

Find methods accept subset patterns for convenient searching:

| Method | Pattern Support | Example | Status |
| - | - | - | - |
| `array.findFirst(pattern)` | `StructSubset<T>` | `orders.findFirst({ state: "CA" })` | ➕ |
| `array.findFirst(value, projFn)` | Existing API | `orders.findFirst("CA", ($, o) => o.state)` | ✅ |
| `array.findAll(pattern)` | `StructSubset<T>` | `orders.findAll({ state: "CA", status: "pending" })` | ➕ |
| `array.findAll(value, projFn)` | Existing API | `orders.findAll("CA", ($, o) => o.state)` | ✅ |
| `array.groupFindFirst(byFn, pattern)` | `StructSubset<T>` | `orders.groupFindFirst(($, o) => o.region, { state: "CA" })` | ➕ |
| `array.groupFindAll(byFn, pattern)` | `StructSubset<T>` | `orders.groupFindAll(($, o) => o.region, { status: "pending" })` | ➕ |

### Modified Sorted Search Methods (Binary Search)

Sorted search methods require prefix (or whole value) patterns only:

| Method | Pattern Type | Example | Status |
| - | - | - | - |
| `array.findSortedFirst(prefix)` | `StructPrefix<T>` | `events.findSortedFirst({ year: 2024, month: 6 })` | ➕ |
| `array.findSortedLast(prefix)` | `StructPrefix<T>` | `events.findSortedLast({ year: 2024 })` | ➕ |
| `array.findSortedRange(prefix)` | `StructPrefix<T>` | `events.findSortedRange({ year: 2024, month: 6 })` | ➕ |
| `array.findSortedRange(start_prefix, end_prefix)` | `StructPrefix<T>` | `events.findSortedRange({ year: 2024, month: 6 }, { year: 2024, month: 8 })` | ➕ |
| `set.findKeyFirst(prefix)` | `StructPrefix<K>` | `dateSet.findKeyFirst({ year: 2024 })` | ➕ |
| `set.findKeyLast(prefix)` | `StructPrefix<K>` | `dateSet.findKeyLast({ year: 2024 })` | ➕ |
| `set.findKeyRange(prefix)` | `StructPrefix<K>` | `dateSet.findKeyAll({ year: 2024, month: 6 })` | ➕ |
| `set.findKeyRange(start_prefix, end_prefix)` | `StructPrefix<K>` | `dateSet.findKeyAll({ year: 2024, month: 6 }, { year: 2024, month: 8 })` | ➕ |
| `dict.findKeyFirst(prefix)` | `StructPrefix<K>` | `timeseriesDict.findKeyFirst({ year: 2024 })` | ➕ |
| `dict.findKeyLast(prefix)` | `StructPrefix<K>` | `timeseriesDict.findKeyLast({ year: 2024 })` | ➕ |
| `dict.findKeyRange(prefix)` | `StructPrefix<K>` | `timeseriesDict.findKeyRange({ year: 2024, month: 6 })` | ➕ |
| `dict.findKeyRange(start_prefix, end_prefix)` | `StructPrefix<K>` | `timeseriesDict.findKeyRange({ year: 2024, month: 6 }, { year: 2024, month: 8 })` | ➕ |

**Prefix Constraint:** Required because binary search relies on lexicographic ordering from the first field. Non-prefix patterns cannot use binary search.

### For loops

It would be great if `$.for(dict, ...)` loops could start at some key, possibly searched for using `findKeyFirst` (or using something like our "type minimum" to fill in the blanks).
This would enable range scan imperative algorithms, as user can `$.break()` once they encounter a key too large.
(The same should work for sets and arrays).

### Examples

```typescript
// Order type: { id, timestamp, customerId, state, city, status, total }

// Equality - any field subset
orders.findFirst({ state: "CA", status: "pending" })
// ↓ Generates:
orders.findFirst({ state: "CA", status: "pending" }, ($, o) =>
  ({ state: o.state, status: o.status })
)

// Ordering - fields in type order
orders.filter(($, o) =>
  East.matchGreaterEqual(o, { timestamp: yesterday, status: "pending" })
)

// Sorted search - prefix only (binary search)
// Keys type: { year, month, day }
timeseriesDict.findKeyRange({ year: 2024, month: 6 })
// Valid: year, year+month, year+month+day

timeseriesDict.findKeyRange({ month: 6 })
// ❌ Type error: Not a prefix (skips year)

// For custom algorithms, use explicit match functions
Expr.block($ => {
  $.for(orders, ($, idx, order) => {
    $.if(East.matchEqual(order, { state: "CA", age: 30 }), $ => {
      // Custom logic here
    });
  });
  return result;
})
```

### Design Notes

- **No new IR**: Pattern matching generates standard projection functions and equality/comparison operations
- **Type safety**: TypeScript enforces correct pattern constraints at compile time
- **Performance**: Julia backend can optimize away intermediate allocations through specialization
- **Explicit fallback**: Users can always write manual projections or field-by-field comparisons for edge cases
