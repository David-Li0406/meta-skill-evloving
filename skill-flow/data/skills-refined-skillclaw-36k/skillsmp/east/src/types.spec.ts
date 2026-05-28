/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import util from "node:util";
import assert from "node:assert";
import {
    NeverType,
    NullType,
    BooleanType,
    IntegerType,
    FloatType,
    StringType,
    DateTimeType,
    BlobType,
    ArrayType,
    SetType,
    DictType,
    StructType,
    VariantType,
    FunctionType,
    AsyncFunctionType,
    OptionType,
    SomeType,
    isDataType,
    isImmutableType,
    isTypeEqual,
    isSubtype,
    isValueOf,
    printType,
    printIdentifier,
    TypeUnion,
    TypeIntersect,
    TypeEqual,
    EastTypeOf,
} from "./types.js";
import { variant } from "./containers/variant.js";

// Force node test to show full stack traces for easier debugging
Error.stackTraceLimit = Infinity

// Force node to print full objects in console.log output
util.inspect.defaultOptions.depth = null

describe("Type constructors", () => {
    test("ArrayType should create array types", () => {
        const type = ArrayType(IntegerType);
        assert.strictEqual(type.type, "Array");
        assert.strictEqual(type.value, IntegerType);
    });

    test("SetType should create set types", () => {
        const type = SetType(StringType);
        assert.strictEqual(type.type, "Set");
        assert.strictEqual(type.key, StringType);
    });

    test("SetType should throw for mutable key types", () => {
        assert.throws(() => SetType(ArrayType(IntegerType)), /Set key type must be an immutable type/);
    });

    test("DictType should create dict types", () => {
        const type = DictType(StringType, IntegerType);
        assert.strictEqual(type.type, "Dict");
        assert.strictEqual(type.key, StringType);
        assert.strictEqual(type.value, IntegerType);
    });

    test("DictType should throw for mutable key types", () => {
        assert.throws(() => DictType(ArrayType(IntegerType), StringType), /Dict key type must be an immutable type/);
    });

    test("StructType should create struct types", () => {
        const type = StructType({ x: IntegerType, y: FloatType });
        assert.strictEqual(type.type, "Struct");
        assert.strictEqual(type.fields.x, IntegerType);
        assert.strictEqual(type.fields.y, FloatType);
    });

    test("VariantType should create variant types with sorted cases", () => {
        const type = VariantType({ b: IntegerType, a: StringType });
        assert.strictEqual(type.type, "Variant");
        // Cases should be sorted alphabetically
        const keys = Object.keys(type.cases);
        assert.deepStrictEqual(keys, ["a", "b"]);
    });

    test("FunctionType should create function types", () => {
        const type = FunctionType([IntegerType, StringType], BooleanType);
        assert.strictEqual(type.type, "Function");
        assert.deepStrictEqual(type.inputs, [IntegerType, StringType]);
        assert.strictEqual(type.output, BooleanType);
    });

    test("AsyncFunctionType should create async function types", () => {
        const type = AsyncFunctionType([IntegerType, StringType], BooleanType);
        assert.strictEqual(type.type, "AsyncFunction");
        assert.deepStrictEqual(type.inputs, [IntegerType, StringType]);
        assert.strictEqual(type.output, BooleanType);
    });

    test("OptionType should create option types", () => {
        const type = OptionType(IntegerType);
        assert.strictEqual(type.type, "Variant");
        assert.strictEqual(type.cases.none, NullType);
        assert.strictEqual(type.cases.some, IntegerType);
    });
});

describe("isDataType", () => {
    test("should return true for primitive data types", () => {
        assert.strictEqual(isDataType(NeverType), true);
        assert.strictEqual(isDataType(NullType), true);
        assert.strictEqual(isDataType(BooleanType), true);
        assert.strictEqual(isDataType(IntegerType), true);
        assert.strictEqual(isDataType(FloatType), true);
        assert.strictEqual(isDataType(StringType), true);
        assert.strictEqual(isDataType(DateTimeType), true);
        assert.strictEqual(isDataType(BlobType), true);
    });

    test("should return true for collection data types", () => {
        assert.strictEqual(isDataType(ArrayType(IntegerType)), true);
        assert.strictEqual(isDataType(SetType(StringType)), true);
        assert.strictEqual(isDataType(DictType(StringType, IntegerType)), true);
    });

    test("should return true for struct with data fields", () => {
        assert.strictEqual(isDataType(StructType({ x: IntegerType, y: FloatType })), true);
    });

    test("should return false for struct with function field", () => {
        assert.strictEqual(isDataType(StructType({ x: IntegerType, f: FunctionType([], NullType) })), false);
    });

    test("should return true for variant with data cases", () => {
        assert.strictEqual(isDataType(VariantType({ none: NullType, some: IntegerType })), true);
    });

    test("should return false for variant with function case", () => {
        assert.strictEqual(isDataType(VariantType({ data: IntegerType, func: FunctionType([], NullType) })), false);
    });

    test("should return false for function types", () => {
        assert.strictEqual(isDataType(FunctionType([], NullType)), false);
    });

    test("should return false for async function types", () => {
        assert.strictEqual(isDataType(AsyncFunctionType([], NullType)), false);
    });
});

describe("isImmutableType", () => {
    test("should return true for primitive immutable types", () => {
        assert.strictEqual(isImmutableType(NeverType), true);
        assert.strictEqual(isImmutableType(NullType), true);
        assert.strictEqual(isImmutableType(BooleanType), true);
        assert.strictEqual(isImmutableType(IntegerType), true);
        assert.strictEqual(isImmutableType(FloatType), true);
        assert.strictEqual(isImmutableType(StringType), true);
        assert.strictEqual(isImmutableType(DateTimeType), true);
        assert.strictEqual(isImmutableType(BlobType), true);
    });

    test("should return false for mutable collection types", () => {
        assert.strictEqual(isImmutableType(ArrayType(IntegerType)), false);
        assert.strictEqual(isImmutableType(SetType(StringType)), false);
        assert.strictEqual(isImmutableType(DictType(StringType, IntegerType)), false);
    });

    test("should return true for struct with immutable fields", () => {
        assert.strictEqual(isImmutableType(StructType({ x: IntegerType, y: StringType })), true);
    });

    test("should return false for struct with mutable field", () => {
        assert.strictEqual(isImmutableType(StructType({ x: IntegerType, arr: ArrayType(IntegerType) })), false);
    });

    test("should return true for variant with immutable cases", () => {
        assert.strictEqual(isImmutableType(VariantType({ none: NullType, some: IntegerType })), true);
    });

    test("should return false for variant with mutable case", () => {
        assert.strictEqual(isImmutableType(VariantType({ data: IntegerType, list: ArrayType(IntegerType) })), false);
    });

    test("should return false for function types", () => {
        assert.strictEqual(isImmutableType(FunctionType([], NullType)), false);
    });

    test("should return false for async function types", () => {
        assert.strictEqual(isImmutableType(AsyncFunctionType([], NullType)), false);
    });
});

describe("isValueOf", () => {
    test("should validate primitive values", () => {
        assert.strictEqual(isValueOf(null, NullType), true);
        assert.strictEqual(isValueOf(true, BooleanType), true);
        assert.strictEqual(isValueOf(false, BooleanType), true);
        assert.strictEqual(isValueOf(42n, IntegerType), true);
        assert.strictEqual(isValueOf(3.14, FloatType), true);
        assert.strictEqual(isValueOf("hello", StringType), true);
        assert.strictEqual(isValueOf(new Date(), DateTimeType), true);
        assert.strictEqual(isValueOf(new Uint8Array([1, 2, 3]), BlobType), true);
    });

    test("should reject wrong primitive values", () => {
        assert.strictEqual(isValueOf(42, IntegerType), false); // number not bigint
        assert.strictEqual(isValueOf(42n, FloatType), false); // bigint not number
        assert.strictEqual(isValueOf("hello", IntegerType), false);
    });

    test("should return false for Never type", () => {
        assert.strictEqual(isValueOf(null, NeverType), false);
        assert.strictEqual(isValueOf(42, NeverType), false);
    });

    test("should validate array values", () => {
        assert.strictEqual(isValueOf([1n, 2n, 3n], ArrayType(IntegerType)), true);
        assert.strictEqual(isValueOf([], ArrayType(IntegerType)), true);
        assert.strictEqual(isValueOf([1, 2, 3], ArrayType(IntegerType)), false); // numbers not bigints
        assert.strictEqual(isValueOf("not array", ArrayType(IntegerType)), false);
    });

    test("should validate set values", () => {
        assert.strictEqual(isValueOf(new Set(["a", "b"]), SetType(StringType)), true);
        assert.strictEqual(isValueOf(new Set([1, 2]), SetType(StringType)), false); // numbers not strings
    });

    test("should validate dict values", () => {
        assert.strictEqual(isValueOf(new Map([["a", 1n]]), DictType(StringType, IntegerType)), true);
        assert.strictEqual(isValueOf(new Map([[1, "a"]]), DictType(StringType, IntegerType)), false); // wrong key type
    });

    test("should validate struct values", () => {
        const type = StructType({ x: IntegerType, y: StringType });
        assert.strictEqual(isValueOf({ x: 42n, y: "hello" }, type), true);
        assert.strictEqual(isValueOf({ x: 42, y: "hello" }, type), false); // wrong field type
        assert.strictEqual(isValueOf({ x: 42n }, type), false); // missing field
    });

    test("should validate variant values", () => {
        const type = VariantType({ none: NullType, some: IntegerType });
        assert.strictEqual(isValueOf(variant("none", null), type), true);
        assert.strictEqual(isValueOf(variant("some", 42n), type), true);
        assert.strictEqual(isValueOf(variant("other", null), type), false); // wrong tag
    });

    test("should throw for Function type", () => {
        assert.throws(() => isValueOf(() => {}, FunctionType([], NullType)), /Javascript functions cannot be converted to East functions/);
    });

    test("should throw for AsyncFunction type", () => {
        assert.throws(() => isValueOf(() => {}, AsyncFunctionType([], NullType)), /Javascript functions cannot be converted to East async functions/);
    });
});

describe("isTypeEqual", () => {
    test("should compare primitive types", () => {
        assert.strictEqual(isTypeEqual(NullType, NullType), true);
        assert.strictEqual(isTypeEqual(IntegerType, IntegerType), true);
        assert.strictEqual(isTypeEqual(IntegerType, FloatType), false);
    });

    test("should compare array types", () => {
        assert.strictEqual(isTypeEqual(ArrayType(IntegerType), ArrayType(IntegerType)), true);
        assert.strictEqual(isTypeEqual(ArrayType(IntegerType), ArrayType(FloatType)), false);
        assert.strictEqual(isTypeEqual(ArrayType(IntegerType), IntegerType), false);
    });

    test("should compare set types", () => {
        assert.strictEqual(isTypeEqual(SetType(StringType), SetType(StringType)), true);
        assert.strictEqual(isTypeEqual(SetType(StringType), SetType(IntegerType)), false);
    });

    test("should compare dict types", () => {
        assert.strictEqual(isTypeEqual(DictType(StringType, IntegerType), DictType(StringType, IntegerType)), true);
        assert.strictEqual(isTypeEqual(DictType(StringType, IntegerType), DictType(IntegerType, StringType)), false);
    });

    test("should compare struct types", () => {
        const t1 = StructType({ x: IntegerType, y: FloatType });
        const t2 = StructType({ x: IntegerType, y: FloatType });
        const t3 = StructType({ x: IntegerType, y: StringType });
        assert.strictEqual(isTypeEqual(t1, t2), true);
        assert.strictEqual(isTypeEqual(t1, t3), false);
    });

    test("should compare variant types", () => {
        const t1 = VariantType({ none: NullType, some: IntegerType });
        const t2 = VariantType({ none: NullType, some: IntegerType });
        const t3 = VariantType({ none: NullType, some: FloatType });
        assert.strictEqual(isTypeEqual(t1, t2), true);
        assert.strictEqual(isTypeEqual(t1, t3), false);
    });

    test("should compare function types", () => {
        const t1 = FunctionType([IntegerType], StringType);
        const t2 = FunctionType([IntegerType], StringType);
        const t3 = FunctionType([FloatType], StringType);
        assert.strictEqual(isTypeEqual(t1, t2), true);
        assert.strictEqual(isTypeEqual(t1, t3), false);
    });

    test("should compare async function types", () => {
        const t1 = AsyncFunctionType([IntegerType], StringType);
        const t2 = AsyncFunctionType([IntegerType], StringType);
        const t3 = AsyncFunctionType([FloatType], StringType);
        assert.strictEqual(isTypeEqual(t1, t2), true);
        assert.strictEqual(isTypeEqual(t1, t3), false);
    });

    test("should distinguish sync and async function types", () => {
        const syncFn = FunctionType([IntegerType], StringType);
        const asyncFn = AsyncFunctionType([IntegerType], StringType);
        assert.strictEqual(isTypeEqual(syncFn, asyncFn), false);
        assert.strictEqual(isTypeEqual(asyncFn, syncFn), false);
    });
});

describe("isSubtype", () => {
    test("Never is subtype of everything", () => {
        assert.strictEqual(isSubtype(NeverType, NullType), true);
        assert.strictEqual(isSubtype(NeverType, IntegerType), true);
        assert.strictEqual(isSubtype(NeverType, FunctionType([], NullType)), true);
    });

    test("primitive types are only subtypes of themselves", () => {
        assert.strictEqual(isSubtype(IntegerType, IntegerType), true);
        assert.strictEqual(isSubtype(IntegerType, FloatType), false);
    });

    test("variant subtyping - fewer cases is subtype", () => {
        const t1 = VariantType({ a: IntegerType, b: StringType, c: FloatType });
        const t2 = VariantType({ a: IntegerType, b: StringType });
        assert.strictEqual(isSubtype(t1, t2), false);
        assert.strictEqual(isSubtype(t2, t1), true);
    });

    test("struct subtyping is structural", () => {
        const t1 = StructType({ x: IntegerType, y: FloatType });
        const t2 = StructType({ x: IntegerType, y: FloatType });
        assert.strictEqual(isSubtype(t1, t2), true);
    });

    test("function subtyping - contravariant inputs, covariant output", () => {
        const t1 = FunctionType([IntegerType], NeverType);
        const t2 = FunctionType([IntegerType], IntegerType);
        // t1 has output Never which is subtype of Integer, so t1 <: t2
        assert.strictEqual(isSubtype(t1, t2), true);
    });

    test("sync function is subtype of async function", () => {
        const syncFn = FunctionType([IntegerType], StringType);
        const asyncFn = AsyncFunctionType([IntegerType], StringType);
        // sync <: async - a sync function can be used where async is expected
        assert.strictEqual(isSubtype(syncFn, asyncFn), true);
    });

    test("async function is NOT subtype of sync function", () => {
        const syncFn = FunctionType([IntegerType], StringType);
        const asyncFn = AsyncFunctionType([IntegerType], StringType);
        // async is NOT subtype of sync - async cannot be used where sync is required
        assert.strictEqual(isSubtype(asyncFn, syncFn), false);
    });

    test("Never is subtype of async function", () => {
        assert.strictEqual(isSubtype(NeverType, AsyncFunctionType([], NullType)), true);
    });

    test("async function subtyping respects contravariance and covariance", () => {
        // Contravariant inputs: wider input -> subtype
        const t1 = AsyncFunctionType([NeverType], IntegerType);
        const t2 = AsyncFunctionType([IntegerType], IntegerType);
        // t1 accepts Never (nothing), t2 accepts Integer
        // For contravariance: t2's input (Integer) is supertype of t1's input (Never)
        // So t1 is NOT a subtype of t2 (t1 is more restrictive on inputs)
        assert.strictEqual(isSubtype(t1, t2), false);

        // Covariant output: narrower output -> subtype
        const t3 = AsyncFunctionType([IntegerType], NeverType);
        const t4 = AsyncFunctionType([IntegerType], IntegerType);
        // t3 outputs Never, t4 outputs Integer
        // Never <: Integer, so t3 <: t4
        assert.strictEqual(isSubtype(t3, t4), true);
    });

    test("sync function subtyping combined with async - sync with narrower output is subtype of async", () => {
        const syncFn = FunctionType([IntegerType], NeverType);
        const asyncFn = AsyncFunctionType([IntegerType], IntegerType);
        // sync <: async AND Never <: Integer for output
        assert.strictEqual(isSubtype(syncFn, asyncFn), true);
    });

    test("async function types with different signatures are not subtypes", () => {
        const t1 = AsyncFunctionType([IntegerType], StringType);
        const t2 = AsyncFunctionType([StringType], StringType);
        assert.strictEqual(isSubtype(t1, t2), false);
        assert.strictEqual(isSubtype(t2, t1), false);
    });
});

describe("printType", () => {
    test("should print primitive types", () => {
        assert.strictEqual(printType(NeverType), ".Never");
        assert.strictEqual(printType(NullType), ".Null");
        assert.strictEqual(printType(BooleanType), ".Boolean");
        assert.strictEqual(printType(IntegerType), ".Integer");
        assert.strictEqual(printType(FloatType), ".Float");
        assert.strictEqual(printType(StringType), ".String");
        assert.strictEqual(printType(DateTimeType), ".DateTime");
        assert.strictEqual(printType(BlobType), ".Blob");
    });

    test("should print collection types", () => {
        assert.strictEqual(printType(ArrayType(IntegerType)), ".Array .Integer");
        assert.strictEqual(printType(SetType(StringType)), ".Set .String");
        assert.strictEqual(printType(DictType(StringType, IntegerType)), ".Dict (key=.String, value=.Integer)");
    });

    test("should print struct types", () => {
        assert.strictEqual(printType(StructType({ x: IntegerType })), `.Struct [(name="x", type=.Integer)]`);
        assert.strictEqual(printType(StructType({ x: IntegerType, y: FloatType })), `.Struct [(name="x", type=.Integer), (name="y", type=.Float)]`);
    });

    test("should print variant types", () => {
        assert.strictEqual(printType(VariantType({ none: NullType })), `.Variant [(name="none", type=.Null)]`);
        assert.strictEqual(printType(VariantType({ none: NullType, some: IntegerType })), `.Variant [(name="none", type=.Null), (name="some", type=.Integer)]`);
    });

    test("should print function types", () => {
        assert.strictEqual(printType(FunctionType([], NullType)), ".Function (inputs=[], output=.Null)");
        assert.strictEqual(printType(FunctionType([IntegerType, StringType], BooleanType)), ".Function (inputs=[.Integer, .String], output=.Boolean)");
    });

    test("should print async function types", () => {
        assert.strictEqual(printType(AsyncFunctionType([], NullType)), ".AsyncFunction (inputs=[], output=.Null)");
        assert.strictEqual(printType(AsyncFunctionType([IntegerType, StringType], BooleanType)), ".AsyncFunction (inputs=[.Integer, .String], output=.Boolean)");
    });
});

describe("printIdentifier", () => {
    test("should print valid identifiers as-is", () => {
        assert.strictEqual(printIdentifier("foo"), "foo");
        assert.strictEqual(printIdentifier("_bar"), "_bar");
        assert.strictEqual(printIdentifier("foo123"), "foo123");
    });

    test("should escape invalid identifiers", () => {
        assert.strictEqual(printIdentifier("foo bar"), "`foo bar`");
        assert.strictEqual(printIdentifier("123"), "`123`");
        assert.strictEqual(printIdentifier("foo-bar"), "`foo-bar`");
    });

    test("should escape special characters in identifiers", () => {
        assert.strictEqual(printIdentifier("foo`bar"), "`foo\\`bar`");
        assert.strictEqual(printIdentifier("foo\\bar"), "`foo\\\\bar`");
    });
});

describe("TypeUnion", () => {
    test("Never is identity for union", () => {
        assert.deepStrictEqual(TypeUnion(NeverType, IntegerType), IntegerType);
        assert.deepStrictEqual(TypeUnion(IntegerType, NeverType), IntegerType);
    });

    test("should union same primitive types", () => {
        assert.deepStrictEqual(TypeUnion(IntegerType, IntegerType), IntegerType);
    });

    test("should throw for different primitive types", () => {
        assert.throws(() => TypeUnion(IntegerType, FloatType), /Cannot union \.Integer with \.Float: incompatible types/);
    });

    test("should union array types with same element type", () => {
        const result = TypeUnion(ArrayType(IntegerType), ArrayType(IntegerType));
        assert.strictEqual(result.type, "Array");
    });

    test("should throw for array types with different element types", () => {
        assert.throws(() => TypeUnion(ArrayType(IntegerType), ArrayType(FloatType)), /\.Integer is not equal to \.Float: incompatible types/);
    });

    test("should union variant types", () => {
        const t1 = VariantType({ a: IntegerType, b: StringType });
        const t2 = VariantType({ b: StringType, c: FloatType });
        const result = TypeUnion(t1, t2);
        assert.strictEqual(result.type, "Variant");
        // Should have all cases: a, b (unioned), c
        assert.ok(result.cases.a);
        assert.ok(result.cases.b);
        assert.ok(result.cases.c);
    });

    test("should union struct types", () => {
        const t1 = StructType({ x: IntegerType, y: FloatType });
        const t2 = StructType({ x: IntegerType, y: FloatType });
        const result = TypeUnion(t1, t2);
        assert.strictEqual(result.type, "Struct");
    });

    test("should throw for structs with different field count", () => {
        const t1 = StructType({ x: IntegerType });
        const t2 = StructType({ x: IntegerType, y: FloatType });
        // t1 has 1 field, t2 has 2 fields
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*structs contain different number of fields/);
    });

    test("should throw for structs with different field names at position 0", () => {
        const t1 = StructType({ x: IntegerType });
        const t2 = StructType({ y: IntegerType });
        // Field at position 0: 'x' vs 'y'
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*struct field 0 has mismatched names x and y/);
    });

    test("should throw for structs with mismatched field names in multi-field structs", () => {
        const t1 = StructType({ a: IntegerType, b: StringType, c: FloatType });
        const t2 = StructType({ a: IntegerType, x: StringType, c: FloatType });
        // Field at position 1: 'b' vs 'x'
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*struct field 1 has mismatched names b and x/);
    });

    test("should union function types", () => {
        const t1 = FunctionType([IntegerType], IntegerType);
        const t2 = FunctionType([IntegerType], FloatType);
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*Cannot union \.Integer with \.Float: incompatible types/);
    });

    test("should union sync and async function types - result is async", () => {
        const syncFn = FunctionType([IntegerType], StringType);
        const asyncFn = AsyncFunctionType([IntegerType], StringType);
        const result = TypeUnion(syncFn, asyncFn);
        assert.strictEqual(result.type, "AsyncFunction");
    });

    test("should union two sync function types - result is sync", () => {
        const t1 = FunctionType([IntegerType], StringType);
        const t2 = FunctionType([IntegerType], StringType);
        const result = TypeUnion(t1, t2);
        assert.strictEqual(result.type, "Function");
    });

    test("should union two async function types - result is async", () => {
        const t1 = AsyncFunctionType([IntegerType], StringType);
        const t2 = AsyncFunctionType([IntegerType], StringType);
        const result = TypeUnion(t1, t2);
        assert.strictEqual(result.type, "AsyncFunction");
    });
});

describe("TypeIntersect", () => {
    test("Never is absorbing for intersection", () => {
        assert.deepStrictEqual(TypeIntersect(NeverType, IntegerType), NeverType);
        assert.deepStrictEqual(TypeIntersect(IntegerType, NeverType), NeverType);
    });

    test("should intersect same primitive types", () => {
        assert.deepStrictEqual(TypeIntersect(IntegerType, IntegerType), IntegerType);
    });

    test("should throw for different primitive types", () => {
        assert.throws(() => TypeIntersect(IntegerType, FloatType), /Cannot intersect \.Integer with \.Float: incompatible types/);
    });

    test("should intersect variant types", () => {
        const t1 = VariantType({ a: IntegerType, b: StringType, c: FloatType });
        const t2 = VariantType({ b: StringType, c: FloatType, d: BooleanType });
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "Variant");
        // TypeIntersect for variants keeps cases in t1 that are also in t2
        assert.deepStrictEqual(result.cases, { b: StringType, c: FloatType });
    });

    test("should throw for variants with no overlapping cases", () => {
        const t1 = VariantType({ a: IntegerType });
        const t2 = VariantType({ b: StringType });
        // Returns t1's cases that are not in t2 (i.e., all of t1's cases)
        assert.throws(() => TypeIntersect(t1, t2));
    });

    test("should intersect sync and async function types - result is sync", () => {
        const syncFn = FunctionType([IntegerType], StringType);
        const asyncFn = AsyncFunctionType([IntegerType], StringType);
        const result = TypeIntersect(syncFn, asyncFn);
        // Intersection: both must be async for result to be async
        // sync ∩ async = sync (the more restrictive type)
        assert.strictEqual(result.type, "Function");
    });

    test("should intersect two sync function types - result is sync", () => {
        const t1 = FunctionType([IntegerType], StringType);
        const t2 = FunctionType([IntegerType], StringType);
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "Function");
    });

    test("should intersect two async function types - result is async", () => {
        const t1 = AsyncFunctionType([IntegerType], StringType);
        const t2 = AsyncFunctionType([IntegerType], StringType);
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "AsyncFunction");
    });
});

describe("TypeEqual", () => {
    test("should accept equal primitive types", () => {
        assert.deepStrictEqual(TypeEqual(IntegerType, IntegerType), IntegerType);
    });

    test("should throw for unequal primitive types", () => {
        assert.throws(() => TypeEqual(IntegerType, FloatType), /\.Integer is not equal to \.Float: incompatible types/);
    });

    test("should accept equal array types", () => {
        const result = TypeEqual(ArrayType(IntegerType), ArrayType(IntegerType));
        assert.strictEqual(result.type, "Array");
    });

    test("should throw for unequal variant case names", () => {
        const t1 = VariantType({ a: IntegerType, c: StringType });
        const t2 = VariantType({ a: IntegerType, b: StringType });
        assert.throws(() => TypeEqual(t1, t2), /\.Variant.*is not equal to.*variant case .* is not present in both variants/);
    });

    test("should throw for variants with different case count", () => {
        const t1 = VariantType({ a: IntegerType });
        const t2 = VariantType({ a: IntegerType, b: StringType });
        assert.throws(() => TypeEqual(t1, t2), /\.Variant.*is not equal to.*variants contain different number of cases/);
    });

    test("should throw for functions with different argument count", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = FunctionType([IntegerType, StringType], NullType);
        assert.throws(() => TypeEqual(t1, t2), /\.Function.*is not equal to.*functions take different number of arguments/);
    });

    test("should throw for sync vs async function types", () => {
        const syncFn = FunctionType([IntegerType], StringType);
        const asyncFn = AsyncFunctionType([IntegerType], StringType);
        assert.throws(() => TypeEqual(syncFn, asyncFn), /\.Function.*is not equal to.*incompatible types/);
    });

    test("should accept equal async function types", () => {
        const t1 = AsyncFunctionType([IntegerType, StringType], FloatType);
        const t2 = AsyncFunctionType([IntegerType, StringType], FloatType);
        const result = TypeEqual(t1, t2);
        assert.strictEqual(result.type, "AsyncFunction");
    });
});

describe("EastTypeOf", () => {
    test("should infer primitive types", () => {
        assert.deepStrictEqual(EastTypeOf(null), NullType);
        assert.deepStrictEqual(EastTypeOf(true), BooleanType);
        assert.deepStrictEqual(EastTypeOf(42n), IntegerType);
        assert.deepStrictEqual(EastTypeOf(3.14), FloatType);
        assert.deepStrictEqual(EastTypeOf("hello"), StringType);
    });

    test("should infer Date type", () => {
        assert.deepStrictEqual(EastTypeOf(new Date()), DateTimeType);
    });

    test("should infer Blob type", () => {
        assert.deepStrictEqual(EastTypeOf(new Uint8Array([1, 2, 3])), BlobType);
    });

    test("should infer array types", () => {
        const type = EastTypeOf([1n, 2n, 3n]);
        assert.strictEqual(type.type, "Array");
        assert.deepStrictEqual(type.value, IntegerType);
    });

    test("should infer struct types", () => {
        const type = EastTypeOf({ x: 42n, y: "hello" });
        assert.strictEqual(type.type, "Struct");
        assert.deepStrictEqual(type.fields.x, IntegerType);
        assert.deepStrictEqual(type.fields.y, StringType);
    });

    test("should throw for functions", () => {
        assert.throws(() => EastTypeOf(() => {}), /Javascript functions cannot be converted to East functions/);
    });

    test("should throw for unknown values", () => {
        // Symbol causes a TypeError when converted to string in the error message
        assert.throws(() => EastTypeOf(Symbol("test") as any), /TypeError.*Cannot convert a Symbol value to a string/);
    });
});

describe("AsyncFunctionType", () => {
    test("sync function in struct field can widen to async", () => {
        // A struct containing a sync callback
        const syncStruct = StructType({ callback: FunctionType([IntegerType], StringType) });
        // A struct expecting an async callback
        const asyncStruct = StructType({ callback: AsyncFunctionType([IntegerType], StringType) });
        // sync struct should be subtype of async struct (covariant in struct fields)
        assert.strictEqual(isSubtype(syncStruct, asyncStruct), true);
    });

    test("async function in struct field cannot narrow to sync", () => {
        const asyncStruct = StructType({ callback: AsyncFunctionType([IntegerType], StringType) });
        const syncStruct = StructType({ callback: FunctionType([IntegerType], StringType) });
        // async struct is NOT subtype of sync struct
        assert.strictEqual(isSubtype(asyncStruct, syncStruct), false);
    });

    test("higher-order function: accepting async callback is supertype of accepting sync callback", () => {
        // Function that takes a sync callback
        const takesSyncCallback = FunctionType([FunctionType([IntegerType], StringType)], NullType);
        // Function that takes an async callback
        const takesAsyncCallback = FunctionType([AsyncFunctionType([IntegerType], StringType)], NullType);
        // Due to contravariance: if you accept async (supertype), you're a subtype
        // takesSyncCallback accepts narrower input, so it's NOT a subtype of takesAsyncCallback
        assert.strictEqual(isSubtype(takesSyncCallback, takesAsyncCallback), false);
        // takesAsyncCallback accepts wider input, so it IS a subtype of takesSyncCallback
        assert.strictEqual(isSubtype(takesAsyncCallback, takesSyncCallback), true);
    });

    test("TypeUnion of functions returning sync vs async callbacks", () => {
        // Function returning a sync callback
        const returnsSync = FunctionType([], FunctionType([IntegerType], StringType));
        // Function returning an async callback
        const returnsAsync = FunctionType([], AsyncFunctionType([IntegerType], StringType));
        // Union should have async callback output (covariant: sync ∪ async = async)
        const result = TypeUnion(returnsSync, returnsAsync);
        assert.strictEqual(result.type, "Function");
        assert.strictEqual(result.output.type, "AsyncFunction");
    });

    test("TypeIntersect of functions accepting sync vs async callbacks", () => {
        // Function that takes a sync callback
        const takesSyncCallback = AsyncFunctionType([FunctionType([IntegerType], StringType)], NullType);
        // Function that takes an async callback
        const takesAsyncCallback = AsyncFunctionType([AsyncFunctionType([IntegerType], StringType)], NullType);
        // Intersection of inputs (contravariant): sync ∪ async = async for what can be passed
        // But TypeIntersect operates on the function types themselves
        const result = TypeIntersect(takesSyncCallback, takesAsyncCallback);
        assert.strictEqual(result.type, "AsyncFunction");
        // Input intersection: sync ∩ async = sync (the more restrictive)
        assert.strictEqual(result.inputs[0].type, "AsyncFunction");
    });
});

describe("Additional coverage tests", () => {
    test("TypeEqual should handle k1 > k2 variant case mismatch", () => {
        const t1 = VariantType({ a: IntegerType, c: StringType });
        const t2 = VariantType({ a: IntegerType, b: StringType });
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError.*variant case b is not present in both variants/);
    });

    test("TypeEqual should succeed for equal variant types", () => {
        const t1 = VariantType({ a: IntegerType, b: StringType });
        const t2 = VariantType({ a: IntegerType, b: StringType });
        const result = TypeEqual(t1, t2);
        assert.strictEqual(result.type, "Variant");
    });

    test("TypeEqual should succeed for equal function types", () => {
        const t1 = FunctionType([IntegerType, StringType], FloatType);
        const t2 = FunctionType([IntegerType, StringType], FloatType);
        const result = TypeEqual(t1, t2);
        assert.strictEqual(result.type, "Function");
    });

    test("TypeEqual should propagate errors from nested types", () => {
        const t1 = ArrayType(IntegerType);
        const t2 = ArrayType(FloatType);
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError/);
    });

    test("SomeType should create option variant with some case", () => {
        const type = SomeType(IntegerType);
        assert.strictEqual(type.type, "Variant");
        assert.deepStrictEqual((type.cases as any).some, IntegerType);
    });

    test("OptionType should create variant with none and some cases", () => {
        const type = OptionType(IntegerType);
        assert.strictEqual(type.type, "Variant");
        assert.deepStrictEqual((type.cases as any).none, NullType);
        assert.deepStrictEqual((type.cases as any).some, IntegerType);
    });

    test("TypeEqual should handle variant case where k1 < k2", () => {
        const t1 = VariantType({ a: IntegerType, b: StringType });
        const t2 = VariantType({ a: IntegerType, c: StringType });
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError.*variant case b is not present in both variants/);
    });

    test("TypeIntersect should throw for functions with different argument counts", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = FunctionType([IntegerType, StringType], NullType);
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError.*functions take different number of arguments/);
    });

    test("TypeEqual with nested type mismatch in array", () => {
        const t1 = StructType({ x: ArrayType(IntegerType) });
        const t2 = StructType({ x: ArrayType(FloatType) });
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError/);
    });

    test("TypeEqual should throw when comparing Variant with non-Variant", () => {
        const t1 = VariantType({ a: IntegerType });
        const t2 = IntegerType;
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError.*is not equal to.*incompatible types/);
    });

    test("TypeEqual should throw when comparing Function with non-Function", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError.*is not equal to.*incompatible types/);
    });

    test("TypeEqual should succeed for equal Dict types", () => {
        const t1 = DictType(StringType, IntegerType);
        const t2 = DictType(StringType, IntegerType);
        const result = TypeEqual(t1, t2);
        assert.strictEqual(result.type, "Dict");
    });

    test("TypeEqual should throw when comparing Dict with non-Dict", () => {
        const t1 = DictType(StringType, IntegerType);
        const t2 = IntegerType;
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError.*is not equal to.*incompatible types/);
    });

    test("TypeEqual should succeed for equal Struct types", () => {
        const t1 = StructType({ x: IntegerType, y: StringType });
        const t2 = StructType({ x: IntegerType, y: StringType });
        const result = TypeEqual(t1, t2);
        assert.strictEqual(result.type, "Struct");
    });

    test("TypeEqual should throw when comparing Struct with non-Struct", () => {
        const t1 = StructType({ x: IntegerType });
        const t2 = IntegerType;
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError.*is not equal to.*incompatible types/);
    });

    test("TypeEqual should throw when comparing Array with non-Array", () => {
        const t1 = ArrayType(IntegerType);
        const t2 = IntegerType;
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError.*is not equal to.*incompatible types/);
    });

    test("TypeEqual should succeed for equal Set types", () => {
        const t1 = SetType(StringType);
        const t2 = SetType(StringType);
        const result = TypeEqual(t1, t2);
        assert.strictEqual(result.type, "Set");
    });

    test("TypeEqual should throw when comparing Set with non-Set", () => {
        const t1 = SetType(StringType);
        const t2 = IntegerType;
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError.*is not equal to.*incompatible types/);
    });

    test("TypeIntersect should succeed for compatible function types", () => {
        const t1 = FunctionType([IntegerType], FloatType);
        const t2 = FunctionType([IntegerType], FloatType);
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "Function");
    });

    test("TypeIntersect should succeed for compatible async function types", () => {
        const t1 = AsyncFunctionType([IntegerType], FloatType);
        const t2 = AsyncFunctionType([IntegerType], FloatType);
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "AsyncFunction");
    });

    test("TypeIntersect should throw when intersecting Function with non-Function", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError.*Cannot intersect.*incompatible types/);
    });

    test("TypeIntersect should throw when intersecting AsyncFunction with non-Function", () => {
        const t1 = AsyncFunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError.*Cannot intersect.*incompatible types/);
    });

    test("TypeIntersect catch block with nested type error", () => {
        const t1 = ArrayType(IntegerType);
        const t2 = ArrayType(FloatType);
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError/);
    });

    test("TypeEqual catch block with deeply nested error", () => {
        const t1 = DictType(StringType, ArrayType(IntegerType));
        const t2 = DictType(StringType, ArrayType(FloatType));
        assert.throws(() => TypeEqual(t1, t2), /TypeMismatchError/);
    });

    test("TypeIntersect should throw when intersecting Variant with non-Variant", () => {
        const t1 = VariantType({ a: IntegerType });
        const t2 = IntegerType;
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError.*Cannot intersect.*incompatible types/);
    });

    test("TypeIntersect should succeed for compatible struct types", () => {
        const t1 = StructType({ x: IntegerType, y: StringType });
        const t2 = StructType({ x: IntegerType, y: StringType });
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "Struct");
    });

    test("TypeIntersect should throw when intersecting Struct with non-Struct", () => {
        const t1 = StructType({ x: IntegerType });
        const t2 = IntegerType;
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError.*Cannot intersect.*incompatible types/);
    });

    test("TypeIntersect should succeed for compatible dict types", () => {
        const t1 = DictType(StringType, IntegerType);
        const t2 = DictType(StringType, IntegerType);
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "Dict");
    });

    test("TypeIntersect should throw when intersecting Dict with non-Dict", () => {
        const t1 = DictType(StringType, IntegerType);
        const t2 = IntegerType;
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError.*Cannot intersect.*incompatible types/);
    });

    test("TypeIntersect should succeed for compatible set types", () => {
        const t1 = SetType(StringType);
        const t2 = SetType(StringType);
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "Set");
    });

    test("TypeIntersect should throw when intersecting Set with non-Set", () => {
        const t1 = SetType(StringType);
        const t2 = IntegerType;
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError.*Cannot intersect.*incompatible types/);
    });

    test("TypeIntersect should succeed for compatible array types", () => {
        const t1 = ArrayType(IntegerType);
        const t2 = ArrayType(IntegerType);
        const result = TypeIntersect(t1, t2);
        assert.strictEqual(result.type, "Array");
    });

    test("TypeIntersect should throw when intersecting Array with non-Array", () => {
        const t1 = ArrayType(IntegerType);
        const t2 = IntegerType;
        assert.throws(() => TypeIntersect(t1, t2), /TypeMismatchError.*Cannot intersect.*incompatible types/);
    });

    test("TypeIntersect should handle malformed types and wrap errors", () => {
        const malformedType = { type: "Array", value: null } as any;
        assert.throws(() => TypeIntersect(malformedType, IntegerType));
    });

    test("TypeEqual should handle malformed types and wrap errors", () => {
        const malformedType = { type: "Array", value: null } as any;
        assert.throws(() => TypeEqual(malformedType, IntegerType));
    });

    test("TypeUnion should throw for functions with different argument counts", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = FunctionType([IntegerType, StringType], NullType);
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*functions take different number of arguments/);
    });

    test("TypeUnion should throw when unioning Function with non-Function", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*Cannot union.*incompatible types/);
    });

    test("TypeUnion should throw when unioning AsyncFunction with non-Function", () => {
        const t1 = AsyncFunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*Cannot union.*incompatible types/);
    });

    test("TypeUnion should handle malformed types and wrap errors", () => {
        const malformedType = { type: "Array", value: null } as any;
        assert.throws(() => TypeUnion(malformedType, IntegerType));
    });

    test("TypeUnion should throw when unioning Dict with non-Dict", () => {
        const t1 = DictType(StringType, IntegerType);
        const t2 = IntegerType;
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*Cannot union.*incompatible types/);
    });

    test("TypeUnion should throw when unioning Struct with non-Struct", () => {
        const t1 = StructType({ x: IntegerType });
        const t2 = IntegerType;
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*Cannot union.*incompatible types/);
    });

    test("TypeUnion should throw when unioning Variant with non-Variant", () => {
        const t1 = VariantType({ a: IntegerType });
        const t2 = IntegerType;
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*Cannot union.*incompatible types/);
    });

    test("TypeUnion should throw when unioning Set with non-Set", () => {
        const t1 = SetType(StringType);
        const t2 = IntegerType;
        assert.throws(() => TypeUnion(t1, t2), /TypeMismatchError.*Cannot union.*incompatible types/);
    });

    test("isSubtype should return false for incompatible variant types", () => {
        const t1 = VariantType({ a: IntegerType });
        const t2 = IntegerType;
        assert.strictEqual(isSubtype(t1, t2), false);
    });

    test("isSubtype should return false for incompatible function types", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.strictEqual(isSubtype(t1, t2), false);
    });

    test("isSubtype should return false for async function compared to non-Function", () => {
        const t1 = AsyncFunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.strictEqual(isSubtype(t1, t2), false);
    });

    test("isSubtype should return false for Set compared to non-Set", () => {
        const t1 = SetType(StringType);
        const t2 = IntegerType;
        assert.strictEqual(isSubtype(t1, t2), false);
    });

    test("isSubtype should return false for Dict compared to non-Dict", () => {
        const t1 = DictType(StringType, IntegerType);
        const t2 = IntegerType;
        assert.strictEqual(isSubtype(t1, t2), false);
    });

    test("isSubtype should return false for Struct compared to non-Struct", () => {
        const t1 = StructType({ x: IntegerType });
        const t2 = IntegerType;
        assert.strictEqual(isSubtype(t1, t2), false);
    });

    test("isTypeEqual should return false for Function compared to non-Function", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.strictEqual(isTypeEqual(t1, t2), false);
    });

    test("isTypeEqual should return false for AsyncFunction compared to non-Function", () => {
        const t1 = AsyncFunctionType([IntegerType], NullType);
        const t2 = IntegerType;
        assert.strictEqual(isTypeEqual(t1, t2), false);
    });

    test("isTypeEqual should return false for sync vs async function", () => {
        const t1 = FunctionType([IntegerType], NullType);
        const t2 = AsyncFunctionType([IntegerType], NullType);
        assert.strictEqual(isTypeEqual(t1, t2), false);
    });

    test("isValueOf should return false for non-Set value with Set type", () => {
        assert.strictEqual(isValueOf([], SetType(IntegerType)), false);
    });

    test("isValueOf should return false for non-Map value with Dict type", () => {
        assert.strictEqual(isValueOf([], DictType(StringType, IntegerType)), false);
    });

    test("isSubtype should return false for Array compared to non-Array", () => {
        const t1 = ArrayType(IntegerType);
        const t2 = IntegerType;
        assert.strictEqual(isSubtype(t1, t2), false);
    });
});
