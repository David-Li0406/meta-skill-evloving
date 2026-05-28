/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, ArrayType, BooleanType, IntegerType, NullType, StringType, StructType, variant, VariantType, FloatType, DateTimeType, BlobType, SetType, DictType, RecursiveType, ref, RefType } from "../src/index.js";
import { EastTypeType, toEastTypeValue } from "../src/type_of_type.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("String", (test) => {
    test("Printing values", $ => {
        const MAX_INT64 = 9223372036854775807n;
        const MIN_INT64 = -9223372036854775808n;

        // Null
        $(assert.equal(East.print(East.value(null)), "null"));

        // Boolean
        $(assert.equal(East.print(East.value(true)), "true"));
        $(assert.equal(East.print(East.value(false)), "false"));

        // Integer - normal cases
        $(assert.equal(East.print(East.value(0n)), "0"));
        $(assert.equal(East.print(East.value(10n)), "10"));
        $(assert.equal(East.print(East.value(-1n)), "-1"));
        // Integer - boundary values
        $(assert.equal(East.print(East.value(MAX_INT64)), "9223372036854775807"));
        $(assert.equal(East.print(East.value(MIN_INT64)), "-9223372036854775808"));
        $(assert.equal(East.print(East.value(MAX_INT64 - 1n)), "9223372036854775806"));
        $(assert.equal(East.print(East.value(MIN_INT64 + 1n)), "-9223372036854775807"));
        $(assert.equal(East.print(East.value(4611686018427387903n)), "4611686018427387903"));
        $(assert.equal(East.print(East.value(-4611686018427387904n)), "-4611686018427387904"));

        // Float - normal cases
        $(assert.equal(East.print(East.value(0.0)), "0.0"));
        $(assert.equal(East.print(East.value(1.0)), "1.0"));
        $(assert.equal(East.print(East.value(-1.0)), "-1.0"));
        $(assert.equal(East.print(East.value(3.14)), "3.14"));
        $(assert.equal(East.print(East.value(-2.5)), "-2.5"));
        // Float - special values
        $(assert.equal(East.print(East.value(-0.0)), "-0.0"));
        $(assert.equal(East.print(East.value(NaN)), "NaN"));
        $(assert.equal(East.print(East.value(Infinity)), "Infinity"));
        $(assert.equal(East.print(East.value(-Infinity)), "-Infinity"));
        // Float - boundary values
        $(assert.equal(East.print(East.value(Number.MAX_VALUE)), "1.7976931348623157e+308"));
        $(assert.equal(East.print(East.value(-Number.MAX_VALUE)),"-1.7976931348623157e+308"));
        $(assert.equal(East.print(East.value(Number.MIN_VALUE)), "5e-324"));
        $(assert.equal(East.print(East.value(Number.EPSILON)), "2.220446049250313e-16"));

        // String - normal and Unicode cases
        $(assert.equal(East.print(East.value("")), "\"\""));
        $(assert.equal(East.print(East.value("hello")), "\"hello\""));
        $(assert.equal(East.print(East.value("café")), "\"café\""));
        $(assert.equal(East.print(East.value("🚀🌟")), "\"🚀🌟\""));
        $(assert.equal(East.print(East.value("東京")), "\"東京\""));
        $(assert.equal(East.print(East.value("いろはにほへと")), "\"いろはにほへと\""));

        // DateTime
        $(assert.equal(East.print(East.value(new Date("1970-01-01T00:00:00.000Z"))), "1970-01-01T00:00:00.000"));
        $(assert.equal(East.print(East.value(new Date("1969-12-31T23:59:59.999Z"))), "1969-12-31T23:59:59.999"));
        $(assert.equal(East.print(East.value(new Date("2024-01-15T10:30:00.123Z"))), "2024-01-15T10:30:00.123"));
        $(assert.equal(East.print(East.value(new Date("1900-01-01T00:00:00.000Z"))), "1900-01-01T00:00:00.000"));
        $(assert.equal(East.print(East.value(new Date("2100-12-31T23:59:59.999Z"))), "2100-12-31T23:59:59.999"));

        // Blob
        $(assert.equal(East.print(East.value(new Uint8Array([]), BlobType)), "0x"));
        $(assert.equal(East.print(East.value(new Uint8Array([0x00]), BlobType)), "0x00"));
        $(assert.equal(East.print(East.value(new Uint8Array([0xff]), BlobType)), "0xff"));
        $(assert.equal(East.print(East.value(new Uint8Array([0x00, 0xff]), BlobType)), "0x00ff"));
        $(assert.equal(East.print(East.value(new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]), BlobType)), "0x48656c6c6f"));
        $(assert.equal(East.print(East.value(new Uint8Array([0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef]), BlobType)), "0x0123456789abcdef"));

        // Ref
        $(assert.equal(East.print(East.value(ref(42n))), "&42"));
        $(assert.equal(East.print(East.value(ref("foo"))), "&\"foo\""));
        $(assert.equal(East.print(East.value(ref([1n, 2n, 3n]))), "&[1, 2, 3]"));

        // Array - normal and edge cases
        $(assert.equal(East.print(East.value([], ArrayType(IntegerType))), "[]"));
        $(assert.equal(East.print(East.value([1n], ArrayType(IntegerType))), "[1]"));
        $(assert.equal(East.print(East.value([1n,2n,3n], ArrayType(IntegerType))), "[1, 2, 3]"));
        $(assert.equal(East.print(East.value([MAX_INT64, MIN_INT64], ArrayType(IntegerType))), "[9223372036854775807, -9223372036854775808]"));
        $(assert.equal(East.print(East.value([[1n, 2n], [3n, 4n]], ArrayType(ArrayType(IntegerType)))), "[[1, 2], [3, 4]]"));

        // Set
        $(assert.equal(East.print(East.value(new Set([]), SetType(IntegerType))), "{}"));
        $(assert.equal(East.print(East.value(new Set([1n]), SetType(IntegerType))), "{1}"));
        $(assert.equal(East.print(East.value(new Set([3n, 1n, 2n]), SetType(IntegerType))), "{1,2,3}"));
        $(assert.equal(East.print(East.value(new Set(["b", "a", "c"]), SetType(StringType))), "{\"a\",\"b\",\"c\"}"));

        // Dict
        $(assert.equal(East.print(East.value(new Map<bigint, string>([]), DictType(IntegerType, StringType))), "{:}"));
        $(assert.equal(East.print(East.value(new Map<bigint, string>([[1n, "one"]]), DictType(IntegerType, StringType))), "{1:\"one\"}"));
        $(assert.equal(East.print(East.value(new Map<bigint, string>([[1n, "one"], [2n, "two"]]), DictType(IntegerType, StringType))), "{1:\"one\",2:\"two\"}"));
        $(assert.equal(East.print(East.value(new Map<bigint, string>([[3n, "c"], [1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType))), "{1:\"a\",2:\"b\",3:\"c\"}"));

        // Struct
        $(assert.equal(East.print(East.value({})), "()"));
        $(assert.equal(East.print(East.value({ a: 1n })), "(a=1)"));
        $(assert.equal(East.print(East.value({ a: 1n, b: true })), "(a=1, b=true)"));

        // Variant
        $(assert.equal(East.print(East.value(variant("none", null))), ".none"));
        $(assert.equal(East.print(East.value(variant("some", 42n))), ".some 42"));

        // Recursive type - linked list
        const LinkedListType = RecursiveType(list => VariantType({
            cons: StructType({
                head: IntegerType,
                tail: list
            }),
            nil: NullType
        }));
        const list0 = $.let(variant("nil", null), LinkedListType);
        const list1 = $.let(variant("cons", { head: 1n, tail: list0 }), LinkedListType);
        const list2 = $.let(variant("cons", { head: 2n, tail: list1 }), LinkedListType);
        $(assert.equal(East.print(list0), ".nil"));
        $(assert.equal(East.print(list1), ".cons (head=1, tail=.nil)"));
        $(assert.equal(East.print(list2), ".cons (head=2, tail=.cons (head=1, tail=.nil))"));

        // Recursive type - East types
        const nullType = $.let(toEastTypeValue(NullType), EastTypeType);
        const booleanType = $.let(toEastTypeValue(BooleanType), EastTypeType);
        const integerType = $.let(toEastTypeValue(IntegerType), EastTypeType);
        const floatType = $.let(toEastTypeValue(FloatType), EastTypeType);
        const dateTimeType = $.let(toEastTypeValue(DateTimeType), EastTypeType);
        const stringType = $.let(toEastTypeValue(StringType), EastTypeType);
        const blobType = $.let(toEastTypeValue(BlobType), EastTypeType);
        const refType = $.let(toEastTypeValue(RefType(IntegerType)), EastTypeType);
        const arrayType = $.let(toEastTypeValue(ArrayType(IntegerType)), EastTypeType);
        const setType = $.let(toEastTypeValue(SetType(StringType)), EastTypeType);
        const dictType = $.let(toEastTypeValue(DictType(StringType, IntegerType)), EastTypeType);
        const structType = $.let(toEastTypeValue(StructType({ name: StringType, age: IntegerType })), EastTypeType);
        const variantType = $.let(toEastTypeValue(VariantType({ none: NullType, some: IntegerType })), EastTypeType);
        const linkedListType = $.let(toEastTypeValue(LinkedListType), EastTypeType);

        $(assert.equal(East.print(nullType), '.Null'));
        $(assert.equal(East.print(booleanType), '.Boolean'));
        $(assert.equal(East.print(integerType), '.Integer'));
        $(assert.equal(East.print(floatType), '.Float'));
        $(assert.equal(East.print(dateTimeType), '.DateTime'));
        $(assert.equal(East.print(stringType), '.String'));
        $(assert.equal(East.print(blobType), '.Blob'));
        $(assert.equal(East.print(refType), '.Ref .Integer'));
        $(assert.equal(East.print(arrayType), '.Array .Integer'));
        $(assert.equal(East.print(setType), '.Set .String'));
        $(assert.equal(East.print(dictType), '.Dict (key=.String, value=.Integer)'));
        $(assert.equal(East.print(structType), '.Struct [(name=\"name\", type=.String), (name=\"age\", type=.Integer)]'));
        $(assert.equal(East.print(variantType), '.Variant [(name=\"none\", type=.Null), (name=\"some\", type=.Integer)]'));
        $(assert.equal(East.print(linkedListType), '.Variant [(name=\"cons\", type=.Struct [(name=\"head\", type=.Integer), (name=\"tail\", type=.Recursive 2)]), (name=\"nil\", type=.Null)]'));
    });

    test("Parsing values", $ => {
        const MAX_INT64 = 9223372036854775807n;
        const MIN_INT64 = -9223372036854775808n;

        // Null - success cases
        $(assert.equal(East.value("null").parse(NullType), null));
        // Null - error cases
        $(assert.throws(East.value("nil").parse(NullType)));
        $(assert.throws(East.value("").parse(NullType)));

        // Boolean - success cases
        $(assert.equal(East.value("true").parse(BooleanType), true));
        $(assert.equal(East.value("false").parse(BooleanType), false));
        // Boolean - error cases
        $(assert.throws(East.value("maybe").parse(BooleanType)));
        $(assert.throws(East.value("").parse(BooleanType)));

        // Integer - success cases (normal)
        $(assert.equal(East.value("0").parse(IntegerType), 0n));
        $(assert.equal(East.value("10").parse(IntegerType), 10n));
        $(assert.equal(East.value("-1").parse(IntegerType), -1n));
        // Integer - success cases (boundary values)
        $(assert.equal(East.value("9223372036854775807").parse(IntegerType), MAX_INT64));
        $(assert.equal(East.value("-9223372036854775808").parse(IntegerType), MIN_INT64));
        $(assert.equal(East.value("9223372036854775806").parse(IntegerType), MAX_INT64 - 1n));
        $(assert.equal(East.value("-9223372036854775807").parse(IntegerType), MIN_INT64 + 1n));
        $(assert.equal(East.value("4611686018427387903").parse(IntegerType), 4611686018427387903n));
        $(assert.equal(East.value("-4611686018427387904").parse(IntegerType), -4611686018427387904n));
        // Integer - error cases
        $(assert.throws(East.value("one").parse(IntegerType)));
        $(assert.throws(East.value("1.0").parse(IntegerType)));
        $(assert.throws(East.value("+1").parse(IntegerType)));
        $(assert.throws(East.value("1-").parse(IntegerType)));
        $(assert.throws(East.value("").parse(IntegerType)));

        // Float - success cases (normal)
        $(assert.equal(East.value("0.0").parse(FloatType), 0.0));
        $(assert.equal(East.value("1.0").parse(FloatType), 1.0));
        $(assert.equal(East.value("-1.0").parse(FloatType), -1.0));
        $(assert.equal(East.value("3.14").parse(FloatType), 3.14));
        $(assert.equal(East.value("-2.5").parse(FloatType), -2.5));
        // Float - success cases (special values)
        $(assert.equal(East.value("-0.0").parse(FloatType), -0.0));
        $(assert.equal(East.value("NaN").parse(FloatType), NaN));
        $(assert.equal(East.value("Infinity").parse(FloatType), Infinity));
        $(assert.equal(East.value("-Infinity").parse(FloatType), -Infinity));
        // Float - success cases (boundary values)
        $(assert.equal(East.value(String(Number.MAX_VALUE)).parse(FloatType), Number.MAX_VALUE));
        $(assert.equal(East.value(String(-Number.MAX_VALUE)).parse(FloatType), -Number.MAX_VALUE));
        $(assert.equal(East.value(String(Number.MIN_VALUE)).parse(FloatType), Number.MIN_VALUE));
        $(assert.equal(East.value(String(Number.EPSILON)).parse(FloatType), Number.EPSILON));

        // String - success cases (normal and Unicode)
        $(assert.equal(East.value("\"\"").parse(StringType), ""));
        $(assert.equal(East.value("\"hello\"").parse(StringType), "hello"));
        $(assert.equal(East.value("\"café\"").parse(StringType), "café"));
        $(assert.equal(East.value("\"🚀🌟\"").parse(StringType), "🚀🌟"));
        $(assert.equal(East.value("\"東京\"").parse(StringType), "東京"));
        $(assert.equal(East.value("\"いろはにほへと\"").parse(StringType), "いろはにほへと"));

        // DateTime - success cases
        $(assert.equal(East.value("1970-01-01T00:00:00.000").parse(DateTimeType), new Date("1970-01-01T00:00:00.000Z")));
        $(assert.equal(East.value("1969-12-31T23:59:59.999").parse(DateTimeType), new Date("1969-12-31T23:59:59.999Z")));
        $(assert.equal(East.value("2024-01-15T10:30:00.123").parse(DateTimeType), new Date("2024-01-15T10:30:00.123Z")));
        $(assert.equal(East.value("1900-01-01T00:00:00.000").parse(DateTimeType), new Date("1900-01-01T00:00:00.000Z")));
        $(assert.equal(East.value("2100-12-31T23:59:59.999").parse(DateTimeType), new Date("2100-12-31T23:59:59.999Z")));

        // Blob - success cases
        $(assert.equal(East.value("0x").parse(BlobType), new Uint8Array([])));
        $(assert.equal(East.value("0x00").parse(BlobType), new Uint8Array([0x00])));
        $(assert.equal(East.value("0xff").parse(BlobType), new Uint8Array([0xff])));
        $(assert.equal(East.value("0x00ff").parse(BlobType), new Uint8Array([0x00, 0xff])));
        $(assert.equal(East.value("0x48656c6c6f").parse(BlobType), new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f])));
        $(assert.equal(East.value("0x0123456789abcdef").parse(BlobType), new Uint8Array([0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef])));

        // Ref - success cases
        $(assert.equal(East.value("&42").parse(RefType(IntegerType)), ref(42n)));
        $(assert.equal(East.value("& 42").parse(RefType(IntegerType)), ref(42n)));
        $(assert.equal(East.value("&\"foo\"").parse(RefType(StringType)), ref("foo")));
        $(assert.equal(East.value("& \"foo\"").parse(RefType(StringType)), ref("foo")));
        $(assert.equal(East.value("&[1, 2, 3]").parse(RefType(ArrayType(IntegerType))), ref([1n, 2n, 3n])));
        $(assert.equal(East.value("& [1, 2, 3]").parse(RefType(ArrayType(IntegerType))), ref([1n, 2n, 3n])));
        // Ref - error cases
        $(assert.throws(East.value("42").parse(RefType(IntegerType))));
        $(assert.throws(East.value("&").parse(RefType(IntegerType))));
        $(assert.throws(East.value("").parse(RefType(IntegerType))));
        $(assert.throws(East.value("&3.14").parse(RefType(IntegerType))));

        // Array - success cases
        $(assert.equal(East.value("[]").parse(ArrayType(IntegerType)), []));
        $(assert.equal(East.value("[1]").parse(ArrayType(IntegerType)), [1n]));
        // $(assertEast.equal(Expr.from("[1,]").parse(ArrayType(IntegerType)), [1n])) // TODO fixme
        $(assert.equal(East.value("[1,2,3]").parse(ArrayType(IntegerType)), [1n, 2n, 3n]));
        // $(assertEast.equal(Expr.from("[1,2,3,]").parse(ArrayType(IntegerType)), [1n, 2n, 3n])) // TODO fixme
        $(assert.equal(East.value("[9223372036854775807, -9223372036854775808]").parse(ArrayType(IntegerType)), [MAX_INT64, MIN_INT64]));
        $(assert.equal(East.value("[[1, 2], [3, 4]]").parse(ArrayType(ArrayType(IntegerType))), [[1n, 2n], [3n, 4n]]));
        // Array - error cases
        $(assert.throws(East.value("[").parse(ArrayType(IntegerType))));
        $(assert.throws(East.value("]").parse(ArrayType(IntegerType))));
        $(assert.throws(East.value("[,]").parse(ArrayType(IntegerType))));
        $(assert.throws(East.value("1").parse(ArrayType(IntegerType))));
        $(assert.throws(East.value("").parse(ArrayType(IntegerType))));

        // Set - success cases
        $(assert.equal(East.value("{}").parse(SetType(IntegerType)), new Set([])));
        $(assert.equal(East.value("{1}").parse(SetType(IntegerType)), new Set([1n])));
        $(assert.equal(East.value("{1,2,3}").parse(SetType(IntegerType)), new Set([1n, 2n, 3n])));
        $(assert.equal(East.value("{\"a\",\"b\",\"c\"}").parse(SetType(StringType)), new Set(["a", "b", "c"])));

        // Dict - success cases
        $(assert.equal(East.value("{:}").parse(DictType(IntegerType, StringType)), new Map<bigint, string>([])));
        $(assert.equal(East.value("{1:\"one\"}").parse(DictType(IntegerType, StringType)), new Map<bigint, string>([[1n, "one"]])));
        $(assert.equal(East.value("{1:\"one\",2:\"two\"}").parse(DictType(IntegerType, StringType)), new Map<bigint, string>([[1n, "one"], [2n, "two"]])));
        $(assert.equal(East.value("{1:\"a\",2:\"b\",3:\"c\"}").parse(DictType(IntegerType, StringType)), new Map<bigint, string>([[1n, "a"], [2n, "b"], [3n, "c"]])));

        // Struct - success cases
        $(assert.equal(East.value("()").parse(StructType({})), {}));
        $(assert.equal(East.value("(a=1)").parse(StructType({ a: IntegerType })), { a: 1n }));
        $(assert.equal(East.value("(a=1,)").parse(StructType({ a: IntegerType })), { a: 1n }));
        $(assert.equal(East.value("(a=1, b=true)").parse(StructType({ a: IntegerType, b: BooleanType })), { a: 1n, b: true }));
        $(assert.equal(East.value("(a=1, b=true,)").parse(StructType({ a: IntegerType, b: BooleanType })), { a: 1n, b: true }));

        // Variant - success cases
        $(assert.equal(East.value(".none null").parse(VariantType({ none: NullType, some: IntegerType })), variant("none", null)));
        $(assert.equal(East.value(".none").parse(VariantType({ none: NullType, some: IntegerType })), variant("none", null)));
        $(assert.equal(East.value(".some 42").parse(VariantType({ none: NullType, some: IntegerType })), variant("some", 42n)));

        // Recursive type - linked list
        const LinkedListType = RecursiveType(list => VariantType({
            cons: StructType({
                head: IntegerType,
                tail: list
            }),
            nil: NullType
        }));
        const list0 = $.let(variant("nil", null), LinkedListType);
        const list1 = $.let(variant("cons", { head: 1n, tail: list0 }), LinkedListType);
        const list2 = $.let(variant("cons", { head: 2n, tail: list1 }), LinkedListType);
        $(assert.equal(East.value(".nil").parse(LinkedListType), list0));
        $(assert.equal(East.value(".cons (head=1, tail=.nil)").parse(LinkedListType), list1));
        $(assert.equal(East.value(".cons (head=2, tail=.cons (head=1, tail=.nil))").parse(LinkedListType), list2));

        // Recursive type - East types
        const nullType = $.let(toEastTypeValue(NullType), EastTypeType);
        const booleanType = $.let(toEastTypeValue(BooleanType), EastTypeType);
        const integerType = $.let(toEastTypeValue(IntegerType), EastTypeType);
        const floatType = $.let(toEastTypeValue(FloatType), EastTypeType);
        const dateTimeType = $.let(toEastTypeValue(DateTimeType), EastTypeType);
        const stringType = $.let(toEastTypeValue(StringType), EastTypeType);
        const blobType = $.let(toEastTypeValue(BlobType), EastTypeType);
        const refType = $.let(toEastTypeValue(RefType(IntegerType)), EastTypeType);
        const arrayType = $.let(toEastTypeValue(ArrayType(IntegerType)), EastTypeType);
        const setType = $.let(toEastTypeValue(SetType(StringType)), EastTypeType);
        const dictType = $.let(toEastTypeValue(DictType(StringType, IntegerType)), EastTypeType);
        const structType = $.let(toEastTypeValue(StructType({ name: StringType, age: IntegerType })), EastTypeType);
        const variantType = $.let(toEastTypeValue(VariantType({ none: NullType, some: IntegerType })), EastTypeType);
        const linkedListType = $.let(toEastTypeValue(LinkedListType), EastTypeType);

        $(assert.equal(East.value('.Null').parse(EastTypeType), nullType));
        $(assert.equal(East.value('.Boolean').parse(EastTypeType), booleanType));
        $(assert.equal(East.value('.Integer').parse(EastTypeType), integerType));
        $(assert.equal(East.value('.Float').parse(EastTypeType), floatType));
        $(assert.equal(East.value('.DateTime').parse(EastTypeType), dateTimeType));
        $(assert.equal(East.value('.String').parse(EastTypeType), stringType));
        $(assert.equal(East.value('.Blob').parse(EastTypeType), blobType));
        $(assert.equal(East.value('.Ref .Integer').parse(EastTypeType), refType));
        $(assert.equal(East.value('.Array .Integer').parse(EastTypeType), arrayType));
        $(assert.equal(East.value('.Set .String').parse(EastTypeType), setType));
        $(assert.equal(East.value('.Dict (key=.String, value=.Integer)').parse(EastTypeType), dictType));
        $(assert.equal(East.value('.Struct [(name=\"name\", type=.String), (name=\"age\", type=.Integer)]').parse(EastTypeType), structType));
        $(assert.equal(East.value('.Variant [(name=\"none\", type=.Null), (name=\"some\", type=.Integer)]').parse(EastTypeType), variantType));
        $(assert.equal(East.value('.Variant [(name=\"cons\", type=.Struct [(name=\"head\", type=.Integer), (name=\"tail\", type=.Recursive 2)]), (name=\"nil\", type=.Null)]').parse(EastTypeType), linkedListType));
    });

    test("String length", $ => {
        // Basic ASCII strings
        $(assert.equal(East.value("").length(), 0n));
        $(assert.equal(East.value("a").length(), 1n));
        $(assert.equal(East.value("hello").length(), 5n));
        $(assert.equal(East.value("Hello, World!").length(), 13n));

        // Unicode codepoints (not UTF-16 units)
        $(assert.equal(East.value("café").length(), 4n)); // é is 1 codepoint
        $(assert.equal(East.value("🚀").length(), 1n));  // Rocket emoji is 1 codepoint
        $(assert.equal(East.value("🚀🌟").length(), 2n)); // Two emoji codepoints
        $(assert.equal(East.value("東京").length(), 2n)); // Two Japanese characters

        // Mixed content
        $(assert.equal(East.value("Hello 🚀 World!").length(), 14n));
        $(assert.equal(East.value("Test: 123 ✓").length(), 11n));
    });

    test("String substring", $ => {
        // Basic substring operations
        $(assert.equal(East.value("hello").substring(0n, 5n), "hello"));
        $(assert.equal(East.value("hello").substring(1n, 4n), "ell"));
        $(assert.equal(East.value("hello").substring(0n, 3n), "hel"));
        $(assert.equal(East.value("hello").substring(2n, 5n), "llo"));

        // Empty results
        $(assert.equal(East.value("hello").substring(0n, 0n), ""));
        $(assert.equal(East.value("hello").substring(3n, 3n), ""));
        $(assert.equal(East.value("").substring(0n, 0n), ""));

        // Forgiving semantics - negative indices become 0
        $(assert.equal(East.value("hello").substring(-1n, 3n), "hel"));
        $(assert.equal(East.value("hello").substring(1n, -1n), ""));

        // Forgiving semantics - negative lengths become 0
        $(assert.equal(East.value("hello").substring(3n, 1n), ""));
        $(assert.equal(East.value("hello").substring(4n, 0n), ""));

        // Out of bounds indices
        $(assert.equal(East.value("hello").substring(0n, 10n), "hello"));
        $(assert.equal(East.value("hello").substring(3n, 10n), "lo"));
        $(assert.equal(East.value("hello").substring(10n, 15n), ""));
        $(assert.equal(East.value("hello").substring(5n, 10n), ""));

        // Unicode codepoint handling
        $(assert.equal(East.value("café").substring(0n, 4n), "café"));
        $(assert.equal(East.value("café").substring(1n, 3n), "af"));
        $(assert.equal(East.value("café").substring(3n, 4n), "é"));

        // Emoji handling (single codepoints)
        $(assert.equal(East.value("🚀🌟").substring(0n, 2n), "🚀🌟"));
        $(assert.equal(East.value("🚀🌟").substring(1n, 2n), "🌟"));
        $(assert.equal(East.value("🚀🌟").substring(0n, 1n), "🚀"));

        // Mixed Unicode content
        $(assert.equal(East.value("Hello 🚀 World!").substring(6n, 7n), "🚀"));
        $(assert.equal(East.value("Hello 🚀 World!").substring(0n, 6n), "Hello "));
        $(assert.equal(East.value("Hello 🚀 World!").substring(7n, 14n), " World!"));

        // Japanese characters
        $(assert.equal(East.value("東京").substring(0n, 2n), "東京"));
        $(assert.equal(East.value("東京").substring(0n, 1n), "東"));
        $(assert.equal(East.value("東京").substring(1n, 2n), "京"));
    });

    test("String case conversion", $ => {
        // Basic case conversion
        $(assert.equal(East.value("hello").upperCase(), "HELLO"));
        $(assert.equal(East.value("WORLD").lowerCase(), "world"));
        $(assert.equal(East.value("MiXeD cAsE").upperCase(), "MIXED CASE"));
        $(assert.equal(East.value("MiXeD cAsE").lowerCase(), "mixed case"));

        // Empty and whitespace
        $(assert.equal(East.value("").upperCase(), ""));
        $(assert.equal(East.value("").lowerCase(), ""));
        $(assert.equal(East.value("   ").upperCase(), "   "));
        $(assert.equal(East.value("   ").lowerCase(), "   "));

        // Numbers and symbols
        $(assert.equal(East.value("hello123!@#").upperCase(), "HELLO123!@#"));
        $(assert.equal(East.value("WORLD456$%^").lowerCase(), "world456$%^"));

        // Unicode handling
        $(assert.equal(East.value("café").upperCase(), "CAFÉ"));
        $(assert.equal(East.value("CAFÉ").lowerCase(), "café"));
        $(assert.equal(East.value("naïve").upperCase(), "NAÏVE"));
    });

    test("String split", $ => {
        // Basic splitting
        $(assert.equal(East.value("hello,world").split(","), East.value(["hello", "world"], ArrayType(StringType))));
        $(assert.equal(East.value("a,b,c").split(","), East.value(["a", "b", "c"], ArrayType(StringType))));
        $(assert.equal(East.value("one two three").split(" "), East.value(["one", "two", "three"], ArrayType(StringType))));

        // Empty delimiter - split into characters/codepoints
        $(assert.equal(East.value("hello").split(""), East.value(["h", "e", "l", "l", "o"], ArrayType(StringType))));
        $(assert.equal(East.value("🚀🌟").split(""), East.value(["🚀", "🌟"], ArrayType(StringType))));
        $(assert.equal(East.value("café").split(""), East.value(["c", "a", "f", "é"], ArrayType(StringType))));

        // No match - returns array with original string
        $(assert.equal(East.value("hello").split(","), East.value(["hello"], ArrayType(StringType))));
        $(assert.equal(East.value("no spaces").split(","), East.value(["no spaces"], ArrayType(StringType))));

        // Empty string
        $(assert.equal(East.value("").split(","), East.value([""], ArrayType(StringType))));
        $(assert.equal(East.value("").split(""), East.value([""], ArrayType(StringType))));

        // Multiple consecutive delimiters
        $(assert.equal(East.value("a,,b").split(","), East.value(["a", "", "b"], ArrayType(StringType))));
        $(assert.equal(East.value(",,").split(","), East.value(["", "", ""], ArrayType(StringType))));

        // Multi-character delimiter
        $(assert.equal(East.value("hello::world").split("::"), East.value(["hello", "world"], ArrayType(StringType))));
        $(assert.equal(East.value("one::two::three").split("::"), East.value(["one", "two", "three"], ArrayType(StringType))));
    });

    test("String trim", $ => {
        // Basic trimming
        $(assert.equal(East.value("  hello  ").trim(), "hello"));
        $(assert.equal(East.value("hello").trim(), "hello"));
        $(assert.equal(East.value("").trim(), ""));
        $(assert.equal(East.value("   ").trim(), ""));

        // Trim start only
        $(assert.equal(East.value("  hello  ").trimStart(), "hello  "));
        $(assert.equal(East.value("hello  ").trimStart(), "hello  "));
        $(assert.equal(East.value("  hello").trimStart(), "hello"));
        $(assert.equal(East.value("hello").trimStart(), "hello"));

        // Trim end only
        $(assert.equal(East.value("  hello  ").trimEnd(), "  hello"));
        $(assert.equal(East.value("  hello").trimEnd(), "  hello"));
        $(assert.equal(East.value("hello  ").trimEnd(), "hello"));
        $(assert.equal(East.value("hello").trimEnd(), "hello"));

        // Various whitespace characters
        $(assert.equal(East.value("\t\n hello \r\n\t").trim(), "hello"));
        $(assert.equal(East.value("\t\n hello \r\n\t").trimStart(), "hello \r\n\t"));
        $(assert.equal(East.value("\t\n hello \r\n\t").trimEnd(), "\t\n hello"));

        // Only whitespace
        $(assert.equal(East.value("\t\n\r ").trim(), ""));
        $(assert.equal(East.value("\t\n\r ").trimStart(), ""));
        $(assert.equal(East.value("\t\n\r ").trimEnd(), ""));

        // Unicode whitespace and content
        $(assert.equal(East.value("  café  ").trim(), "café"));
        $(assert.equal(East.value("  🚀  ").trim(), "🚀"));
    });

    test("String starts/ends with", $ => {
        // Basic starts with
        $(assert.equal(East.value("hello world").startsWith("hello"), true));
        $(assert.equal(East.value("hello world").startsWith("world"), false));
        $(assert.equal(East.value("hello").startsWith("hello"), true));
        $(assert.equal(East.value("hello").startsWith("hello world"), false));

        // Basic ends with
        $(assert.equal(East.value("hello world").endsWith("world"), true));
        $(assert.equal(East.value("hello world").endsWith("hello"), false));
        $(assert.equal(East.value("world").endsWith("world"), true));
        $(assert.equal(East.value("hello").endsWith("hello world"), false));

        // Empty string cases
        $(assert.equal(East.value("hello").startsWith(""), true));
        $(assert.equal(East.value("hello").endsWith(""), true));
        $(assert.equal(East.value("").startsWith(""), true));
        $(assert.equal(East.value("").endsWith(""), true));
        $(assert.equal(East.value("").startsWith("hello"), false));
        $(assert.equal(East.value("").endsWith("hello"), false));

        // Unicode handling
        $(assert.equal(East.value("café world").startsWith("café"), true));
        $(assert.equal(East.value("hello café").endsWith("café"), true));
        $(assert.equal(East.value("🚀🌟").startsWith("🚀"), true));
        $(assert.equal(East.value("🚀🌟").endsWith("🌟"), true));
    });

    test("String contains", $ => {
        // Basic contains
        $(assert.equal(East.value("hello world").contains("hello"), true));
        $(assert.equal(East.value("hello world").contains("world"), true));
        $(assert.equal(East.value("hello world").contains("lo wo"), true));
        $(assert.equal(East.value("hello world").contains("xyz"), false));

        // Exact match
        $(assert.equal(East.value("hello").contains("hello"), true));
        $(assert.equal(East.value("hello").contains("hello world"), false));

        // Empty string
        $(assert.equal(East.value("hello").contains(""), true));
        $(assert.equal(East.value("").contains(""), true));
        $(assert.equal(East.value("").contains("hello"), false));

        // Case sensitivity
        $(assert.equal(East.value("Hello World").contains("hello"), false));
        $(assert.equal(East.value("Hello World").contains("Hello"), true));

        // Unicode handling
        $(assert.equal(East.value("café world").contains("café"), true));
        $(assert.equal(East.value("hello café").contains("é"), true));
        $(assert.equal(East.value("🚀🌟⭐").contains("🌟"), true));
    });

    test("String indexOf", $ => {
        // Basic indexOf - returns codepoint positions
        $(assert.equal(East.value("hello world").indexOf("hello"), 0n));
        $(assert.equal(East.value("hello world").indexOf("world"), 6n));
        $(assert.equal(East.value("hello world").indexOf("o"), 4n));
        $(assert.equal(East.value("hello world").indexOf(" "), 5n));

        // Not found
        $(assert.equal(East.value("hello world").indexOf("xyz"), -1n));
        $(assert.equal(East.value("hello").indexOf("hello world"), -1n));

        // Empty string
        $(assert.equal(East.value("hello").indexOf(""), 0n));
        $(assert.equal(East.value("").indexOf(""), 0n));
        $(assert.equal(East.value("").indexOf("hello"), -1n));

        // Multiple occurrences - returns first
        $(assert.equal(East.value("hello hello").indexOf("hello"), 0n));
        $(assert.equal(East.value("hello hello").indexOf("o"), 4n));

        // Unicode codepoint handling
        $(assert.equal(East.value("café world").indexOf("é"), 3n));
        $(assert.equal(East.value("café world").indexOf("world"), 5n));
        $(assert.equal(East.value("🚀🌟⭐").indexOf("🌟"), 1n));
        $(assert.equal(East.value("🚀🌟⭐").indexOf("⭐"), 2n));

        // Japanese characters
        $(assert.equal(East.value("東京日本").indexOf("京"), 1n));
        $(assert.equal(East.value("東京日本").indexOf("日本"), 2n));
    });

    test("String replace", $ => {
        // Basic replace - replaces all occurrences
        $(assert.equal(East.value("hello world").replace("hello", "hi"), "hi world"));
        $(assert.equal(East.value("hello world").replace("world", "universe"), "hello universe"));
        $(assert.equal(East.value("hello hello").replace("hello", "hi"), "hi hi"));

        // Not found - returns original
        $(assert.equal(East.value("hello world").replace("xyz", "abc"), "hello world"));

        // Empty strings - replaceAll inserts between every character
        $(assert.equal(East.value("hello").replace("", "X"), "XhXeXlXlXoX"));
        $(assert.equal(East.value("hello").replace("hello", ""), ""));
        $(assert.equal(East.value("").replace("", "X"), "X"));
        $(assert.equal(East.value("").replace("hello", "world"), ""));

        // Replace with longer/shorter strings (all occurrences)
        $(assert.equal(East.value("hello").replace("ll", "L"), "heLo"));
        $(assert.equal(East.value("hello").replace("l", "LL"), "heLLLLo"));

        // Unicode handling
        $(assert.equal(East.value("café world").replace("café", "coffee"), "coffee world"));
        $(assert.equal(East.value("🚀🌟").replace("🚀", "🛸"), "🛸🌟"));

        // Case sensitivity
        $(assert.equal(East.value("Hello World").replace("hello", "hi"), "Hello World"));
        $(assert.equal(East.value("Hello World").replace("Hello", "Hi"), "Hi World"));
    });

    test("Regex replace", $ => {
        // Basic regex replace - replaces all matches
        $(assert.equal(East.value("hello123world456").replace(/\d+/g, "X"), "helloXworldX"));
        $(assert.equal(East.value("test test test").replace(/test/g, "exam"), "exam exam exam"));
        $(assert.equal(East.value("abc def ghi").replace(/\s+/g, "_"), "abc_def_ghi"));

        // Case insensitive replace
        $(assert.equal(East.value("Hello HELLO hello").replace(/hello/gi, "hi"), "hi hi hi"));
        $(assert.equal(East.value("Test TEST test").replace(/test/gi, "exam"), "exam exam exam"));

        // Not found - returns original
        $(assert.equal(East.value("hello world").replace(/xyz/g, "abc"), "hello world"));
        $(assert.equal(East.value("hello world").replace(/\d+/g, "X"), "hello world"));

        // Capture groups with $1, $2, etc.
        $(assert.equal(East.value("hello world").replace(/(\w+) (\w+)/, "$2 $1"), "world hello"));
        $(assert.equal(East.value("John Doe").replace(/(\w+) (\w+)/, "$2, $1"), "Doe, John"));
        $(assert.equal(East.value("2024-01-15").replace(/(\d{4})-(\d{2})-(\d{2})/, "$3/$2/$1"), "15/01/2024"));

        // Multiple capture groups
        $(assert.equal(East.value("abc123def456").replace(/([a-z]+)(\d+)/g, "[$1:$2]"), "[abc:123][def:456]"));
        $(assert.equal(East.value("test1 test2 test3").replace(/(\w+)(\d)/g, "$1-$2"), "test-1 test-2 test-3"));

        // Named capture groups with $<name>
        $(assert.equal(East.value("hello world").replace(/(?<first>\w+) (?<second>\w+)/, "$<second> $<first>"), "world hello"));
        $(assert.equal(East.value("John Doe").replace(/(?<first>\w+) (?<last>\w+)/, "$<last>, $<first>"), "Doe, John"));
        $(assert.equal(East.value("2024-01-15").replace(/(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/, "$<day>/$<month>/$<year>"), "15/01/2024"));

        // Special replacements are not supported - they throw errors unless the `$` is escaped (`$$`)
        $(assert.throws(East.value("hello world").replace(/world/, "[$&]")));  // $& = entire match
        $(assert.throws(East.value("test123abc").replace(/\d+/, "[$`]")));  // $` = before match
        $(assert.throws(East.value("test123abc").replace(/\d+/, "[$']")));  // $' = after match

        // Escaped dollar signs work correctly
        $(assert.equal(East.value("hello world").replace(/world/, "$$&"), "hello $&"));  // escaped $&
        $(assert.equal(East.value("test").replace(/test/, "$$$$"), "$$"));  // $$ becomes single $
        $(assert.equal(East.value("price: 100").replace(/(\d+)/, "$$$1"), "price: $100"));  // $$1 = literal $ + capture 1
        $(assert.equal(East.value("hello").replace(/hello/, "$$$$world"), "$$world"));  // $$$$ = $$

        // Invalid $ patterns throw errors (strict validation)
        $(assert.throws(East.value("hello").replace(/hello/, "$foo")));  // unrecognized pattern
        $(assert.throws(East.value("hello").replace(/hello/, "test$")));  // trailing $
        $(assert.throws(East.value("hello").replace(/hello/, "$x")));  // invalid escape
        $(assert.throws(East.value("hello").replace(/hello/, "$<")));  // unclosed named group
        $(assert.throws(East.value("hello").replace(/hello/, "$<>")));  // empty named group

        // Empty replacement
        $(assert.equal(East.value("hello123world456").replace(/\d+/g, ""), "helloworld"));
        $(assert.equal(East.value("test_test_test").replace(/_/g, ""), "testtesttest"));

        // Unicode handling
        $(assert.equal(East.value("café café").replace(/café/g, "coffee"), "coffee coffee"));
        $(assert.equal(East.value("🚀🌟🚀").replace(/🚀/g, "🛸"), "🛸🌟🛸"));
        $(assert.equal(East.value("東京東京").replace(/東京/g, "Tokyo"), "TokyoTokyo"));

        // Character classes and quantifiers
        $(assert.equal(East.value("hello world").replace(/[aeiou]/g, "*"), "h*ll* w*rld"));
        $(assert.equal(East.value("test123abc456").replace(/\d{3}/g, "XXX"), "testXXXabcXXX"));
        $(assert.equal(East.value("a1b22c333").replace(/\d+/g, "X"), "aXbXcX"));

        // Anchors with replaceAll semantics
        $(assert.equal(East.value("hello\nworld\ntest").replace(/^/gm, "> "), "> hello\n> world\n> test"));
        $(assert.equal(East.value("hello\nworld\ntest").replace(/$/gm, "!"), "hello!\nworld!\ntest!"));

        // Multiline and dotall flags
        $(assert.equal(East.value("hello\nworld").replace(/hello.*world/s, "replaced"), "replaced"));
        $(assert.equal(East.value("hello\nworld").replace(/^hello$/m, "HI"), "HI\nworld"));

        // Business analytics use cases
        // Clean up data: remove extra whitespace
        $(assert.equal(East.value("product   name   here").replace(/\s+/g, " "), "product name here"));

        // Extract and reformat: phone numbers
        $(assert.equal(East.value("555-1234").replace(/(\d{3})-(\d{4})/, "($1) $2"), "(555) 1234"));

        // Standardize: currency formatting
        $(assert.equal(East.value("price: $100.50 or $200.75").replace(/\$(\d+\.\d{2})/g, "USD $1"), "price: USD 100.50 or USD 200.75"));

        // Redact: sensitive data
        $(assert.equal(East.value("SSN: 123-45-6789").replace(/\d{3}-\d{2}-\d{4}/, "XXX-XX-XXXX"), "SSN: XXX-XX-XXXX"));
    });

    test("Regex contains", $ => {
        // Basic RegExp objects
        $(assert.equal(East.value("hello world").contains(/h.*o/), true));
        $(assert.equal(East.value("hello world").contains(/w.*d/), true));
        $(assert.equal(East.value("hello world").contains(/xyz/), false));

        // RegExp with flags
        $(assert.equal(East.value("Hello World").contains(/hello/), false));
        $(assert.equal(East.value("Hello World").contains(/hello/i), true));
        $(assert.equal(East.value("Hello World").contains(/WORLD/), false));
        $(assert.equal(East.value("Hello World").contains(/WORLD/i), true));

        // Complex patterns
        $(assert.equal(East.value("test123").contains(/\d+/), true));
        $(assert.equal(East.value("hello").contains(/[aeiou]/), true));
        $(assert.equal(East.value("test.txt").contains(/\./), true));

        // Multiple flags in RegExp
        $(assert.equal(East.value("Hello\nWorld").contains(/hello.*world/is), true));
        $(assert.equal(East.value("Hello\nWorld").contains(/hello.*world/i), false));
    });

    test("Regex indexOf", $ => {
        // Basic regex indexOf - returns codepoint positions
        $(assert.equal(East.value("hello world").indexOf(/h.*o/), 0n));
        $(assert.equal(East.value("hello world").indexOf(/w.*d/), 6n));
        $(assert.equal(East.value("hello world").indexOf(/o/), 4n));
        $(assert.equal(East.value("hello world").indexOf(/ /), 5n));

        // Not found
        $(assert.equal(East.value("hello world").indexOf(/xyz/), -1n));
        $(assert.equal(East.value("hello").indexOf(/world/), -1n));

        // Case sensitivity with flags
        $(assert.equal(East.value("Hello World").indexOf(/hello/), -1n));
        $(assert.equal(East.value("Hello World").indexOf(/hello/i), 0n));
        $(assert.equal(East.value("Hello World").indexOf(/WORLD/), -1n));
        $(assert.equal(East.value("Hello World").indexOf(/WORLD/i), 6n));

        // Anchors and boundaries
        $(assert.equal(East.value("hello world").indexOf(/^hello/), 0n));
        $(assert.equal(East.value("hello world").indexOf(/world$/), 6n));
        $(assert.equal(East.value("hello world").indexOf(/^world/), -1n));
        $(assert.equal(East.value("hello world").indexOf(/hello$/), -1n));

        // Character classes and quantifiers
        $(assert.equal(East.value("test123abc").indexOf(/\d/), 4n));
        $(assert.equal(East.value("test123abc").indexOf(/\d+/), 4n));
        $(assert.equal(East.value("test123abc").indexOf(/\d{3}/), 4n));
        $(assert.equal(East.value("test123abc").indexOf(/\d{4}/), -1n));
        $(assert.equal(East.value("hello world").indexOf(/[aeiou]/), 1n)); // 'e' at position 1

        // Special characters
        $(assert.equal(East.value("test.txt").indexOf(/\./), 4n));
        $(assert.equal(East.value("a+b*c").indexOf(/\+/), 1n));
        $(assert.equal(East.value("a+b*c").indexOf(/\*/), 3n));

        // Empty pattern
        $(assert.equal(East.value("hello").indexOf(/(?:)/), 0n)); // Empty group matches at start

        // Unicode codepoint handling
        $(assert.equal(East.value("café world").indexOf(/é/), 3n));
        $(assert.equal(East.value("café world").indexOf(/world/), 5n));
        $(assert.equal(East.value("🚀🌟⭐").indexOf(/🌟/), 1n));
        $(assert.equal(East.value("🚀🌟⭐").indexOf(/⭐/), 2n));
        $(assert.equal(East.value("🚀🌟⭐").indexOf(/🚀.*⭐/), 0n));

        // Japanese characters
        $(assert.equal(East.value("東京日本").indexOf(/京/), 1n));
        $(assert.equal(East.value("東京日本").indexOf(/日本/), 2n));

        // Multiple flags
        $(assert.equal(East.value("Hello\nWorld").indexOf(/hello.*world/is), 0n));
        $(assert.equal(East.value("Hello\nWorld").indexOf(/hello.*world/i), -1n)); // No 's' flag
    });

    test("Comparisons", $ => {
        // Equality tests
        $(assert.equal(East.value("hello"), "hello"));
        $(assert.equal(East.value(""), ""));
        $(assert.notEqual(East.value("hello"), "world"));
        $(assert.notEqual(East.value("hello"), "Hello"));

        // Lexical ordering tests
        $(assert.less(East.value(""), "a"));
        $(assert.less(East.value("a"), "b"));
        $(assert.less(East.value("aa"), "ab"));
        $(assert.less(East.value("apple"), "banana"));
        $(assert.less(East.value("Hello"), "hello")); // uppercase comes before lowercase in lexical order
        $(assert.less(East.value("10"), "9")); // string comparison, not numeric

        // Greater than tests
        $(assert.greater(East.value("b"), "a"));
        $(assert.greater(East.value("banana"), "apple"));
        $(assert.greater(East.value("hello"), "Hello"));
        $(assert.greater(East.value("z"), ""));

        // Less than or equal / Greater than or equal
        $(assert.lessEqual(East.value(""), ""));
        $(assert.lessEqual(East.value("hello"), "hello"));
        $(assert.lessEqual(East.value("a"), "b"));
        $(assert.greaterEqual(East.value(""), ""));
        $(assert.greaterEqual(East.value("hello"), "hello"));
        $(assert.greaterEqual(East.value("b"), "a"));

        // Unicode ordering
        $(assert.less(East.value("café"), "zebra"));
        // Note: Unicode ordering is by code point, not alphabetical in human languages

        // East.is, East.equal, East.less methods
        $(assert.equal(East.is(East.value("hello"), "hello"), true));
        $(assert.equal(East.is(East.value("hello"), "world"), false));
        $(assert.equal(East.equal(East.value("hello"), "hello"), true));
        $(assert.equal(East.equal(East.value("hello"), "world"), false));
        $(assert.equal(East.notEqual(East.value("hello"), "world"), true));
        $(assert.equal(East.less(East.value("a"), "b"), true));
        $(assert.equal(East.less(East.value("b"), "a"), false));
        $(assert.equal(East.lessEqual(East.value("a"), "a"), true));
        $(assert.equal(East.lessEqual(East.value("a"), "b"), true));
        $(assert.equal(East.greater(East.value("b"), "a"), true));
        $(assert.equal(East.greaterEqual(East.value("b"), "a"), true));

        // Instance method tests
        $(assert.equal(East.value("hello").equals("hello"), true));
        $(assert.equal(East.value("hello").equals("world"), false));
        $(assert.equal(East.value("hello").notEquals("world"), true));
        $(assert.equal(East.value("hello").notEquals("hello"), false));
        $(assert.equal(East.value("a").lessThan("b"), true));
        $(assert.equal(East.value("b").lessThan("a"), false));
        $(assert.equal(East.value("a").lessThanOrEqual("a"), true));
        $(assert.equal(East.value("a").lessThanOrEqual("b"), true));
        $(assert.equal(East.value("b").greaterThan("a"), true));
        $(assert.equal(East.value("a").greaterThan("b"), false));
        $(assert.equal(East.value("b").greaterThanOrEqual("a"), true));
        $(assert.equal(East.value("b").greaterThanOrEqual("b"), true));
    });

    test("JSON print", $ => {
        const printJson = East.String.printJson;

        // Null
        $(assert.equal(printJson(East.value(null)), "null"));

        // Boolean - all values
        $(assert.equal(printJson(East.value(true)), "true"));
        $(assert.equal(printJson(East.value(false)), "false"));

        // Integer - encoded as strings to preserve precision
        const MAX_INT64 = 9223372036854775807n; // 2^63 - 1
        const MIN_INT64 = -9223372036854775808n; // -2^63
        $(assert.equal(printJson(East.value(0n)), "\"0\""));
        $(assert.equal(printJson(East.value(42n)), "\"42\"")); // Normal case
        $(assert.equal(printJson(East.value(-123n)), "\"-123\"")); // Normal case
        $(assert.equal(printJson(East.value(1n)), "\"1\""));
        $(assert.equal(printJson(East.value(-1n)), "\"-1\""));
        // Edge cases: INT64 bounds
        $(assert.equal(printJson(East.value(MAX_INT64)), "\"9223372036854775807\"")); // MAX_INT64
        $(assert.equal(printJson(East.value(MIN_INT64)), "\"-9223372036854775808\"")); // MIN_INT64
        $(assert.equal(printJson(East.value(MAX_INT64 - 1n)), "\"9223372036854775806\"")); // MAX_INT64 - 1
        $(assert.equal(printJson(East.value(MIN_INT64 + 1n)), "\"-9223372036854775807\"")); // MIN_INT64 + 1
        // Powers of 2 near boundaries
        $(assert.equal(printJson(East.value(4611686018427387903n)), "\"4611686018427387903\"")); // 2^62-1
        $(assert.equal(printJson(East.value(-4611686018427387904n)), "\"-4611686018427387904\"")); // -2^62

        // Float - normal values
        $(assert.equal(printJson(East.value(0.0)), "0"));
        $(assert.equal(printJson(East.value(1.0)), "1"));
        $(assert.equal(printJson(East.value(-1.0)), "-1"));
        $(assert.equal(printJson(East.value(3.14)), "3.14"));
        $(assert.equal(printJson(East.value(-2.5)), "-2.5"));
        // Float - boundary values using Number constants
        $(assert.equal(printJson(East.value(Number.MAX_VALUE)), String(Number.MAX_VALUE))); // Largest finite float
        $(assert.equal(printJson(East.value(-Number.MAX_VALUE)), String(-Number.MAX_VALUE))); // Most negative finite float
        $(assert.equal(printJson(East.value(Number.MIN_VALUE)), String(Number.MIN_VALUE))); // Smallest positive denormal
        $(assert.equal(printJson(East.value(Number.EPSILON)), String(Number.EPSILON))); // Machine epsilon
        // Float - special values (CRITICAL for cross-language compliance!)
        $(assert.equal(printJson(East.value(-0.0)), "\"-0.0\"")); // Negative zero is distinct from +0.0
        $(assert.equal(printJson(East.value(NaN)), "\"NaN\""));
        $(assert.equal(printJson(East.value(Infinity)), "\"Infinity\""));
        $(assert.equal(printJson(East.value(-Infinity)), "\"-Infinity\""));

        // String
        $(assert.equal(printJson(East.value("")), "\"\"")); // Edge case: empty string
        $(assert.equal(printJson(East.value("hello")), "\"hello\"")); // Normal case: ASCII
        $(assert.equal(printJson(East.value("café")), "\"café\"")); // Edge case: Latin with diacritic
        $(assert.equal(printJson(East.value("🚀🌟")), "\"🚀🌟\"")); // Edge case: Emoji (multi-byte UTF-8)
        $(assert.equal(printJson(East.value("東京")), "\"東京\"")); // Edge case: CJK characters
        $(assert.equal(printJson(East.value("いろはにほへと")), "\"いろはにほへと\"")); // Edge case: Hiragana

        // DateTime - RFC 3339 with timezone (uses +00:00 format)
        $(assert.equal(printJson(East.value(new Date("1970-01-01T00:00:00.000Z"))), "\"1970-01-01T00:00:00.000+00:00\"")); // Edge case: Unix epoch
        $(assert.equal(printJson(East.value(new Date("1969-12-31T23:59:59.999Z"))), "\"1969-12-31T23:59:59.999+00:00\"")); // Edge case: Before epoch (negative timestamp)
        $(assert.equal(printJson(East.value(new Date("2024-01-15T10:30:00.123Z"))), "\"2024-01-15T10:30:00.123+00:00\"")); // Normal case
        $(assert.equal(printJson(East.value(new Date("1900-01-01T00:00:00.000Z"))), "\"1900-01-01T00:00:00.000+00:00\"")); // Edge case: Far past
        $(assert.equal(printJson(East.value(new Date("2100-12-31T23:59:59.999Z"))), "\"2100-12-31T23:59:59.999+00:00\"")); // Edge case: Far future

        // Blob - hex string
        $(assert.equal(printJson(East.value(new Uint8Array([]), BlobType)), "\"0x\"")); // Edge case: empty blob
        $(assert.equal(printJson(East.value(new Uint8Array([0x00]), BlobType)), "\"0x00\"")); // Edge case: single zero byte (minimum)
        $(assert.equal(printJson(East.value(new Uint8Array([0xff]), BlobType)), "\"0xff\"")); // Edge case: single 0xFF byte (maximum)
        $(assert.equal(printJson(East.value(new Uint8Array([0x00, 0xff]), BlobType)), "\"0x00ff\"")); // Edge case: min and max bytes together
        $(assert.equal(printJson(East.value(new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]), BlobType)), "\"0x48656c6c6f\"")); // Normal case: "Hello" in hex
        $(assert.equal(printJson(East.value(new Uint8Array([0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef]), BlobType)), "\"0x0123456789abcdef\"")); // Edge case: all hex digit values 0-9, a-f

        // Ref - JSON array
        $(assert.equal(printJson(East.value(ref(null), RefType(NullType))), "[null]"));
        $(assert.equal(printJson(East.value(ref(42n), RefType(IntegerType))), "[\"42\"]"));

        // Array - JSON array
        $(assert.equal(printJson(East.value([], ArrayType(IntegerType))), "[]")); // Edge case: empty array
        $(assert.equal(printJson(East.value([1n], ArrayType(IntegerType))), "[\"1\"]")); // Edge case: single element
        $(assert.equal(printJson(East.value([1n, 2n, 3n], ArrayType(IntegerType))), "[\"1\",\"2\",\"3\"]")); // Normal case
        $(assert.equal(printJson(East.value(["a", "b"], ArrayType(StringType))), "[\"a\",\"b\"]")); // Normal case
        // Nested arrays
        $(assert.equal(printJson(East.value([[1n, 2n], [3n, 4n]], ArrayType(ArrayType(IntegerType)))), "[[\"1\",\"2\"],[\"3\",\"4\"]]")); // Edge case: nested structure
        // Edge case: boundary integers in array
        $(assert.equal(printJson(East.value([MAX_INT64, MIN_INT64], ArrayType(IntegerType))), "[\"9223372036854775807\",\"-9223372036854775808\"]"));

        // Set - JSON array (sorted)
        $(assert.equal(printJson(East.value(new Set([]), SetType(IntegerType))), "[]")); // Edge case: empty set
        $(assert.equal(printJson(East.value(new Set([1n]), SetType(IntegerType))), "[\"1\"]")); // Edge case: single element
        $(assert.equal(printJson(East.value(new Set([3n, 1n, 2n]), SetType(IntegerType))), "[\"1\",\"2\",\"3\"]")); // Edge case: unsorted input becomes sorted output
        $(assert.equal(printJson(East.value(new Set(["b", "a", "c"]), SetType(StringType))), "[\"a\",\"b\",\"c\"]")); // Edge case: string sorting behavior

        // Dict - array of {"key": ..., "value": ...} objects
        $(assert.equal(printJson(East.value(new Map<bigint, string>([]), DictType(IntegerType, StringType))), "[]")); // Edge case: empty dict
        $(assert.equal(printJson(East.value(new Map<bigint, string>([[1n, "one"]]), DictType(IntegerType, StringType))), "[{\"key\":\"1\",\"value\":\"one\"}]")); // Edge case: single entry
        $(assert.equal(printJson(East.value(new Map<bigint, string>([[1n, "one"], [2n, "two"]]), DictType(IntegerType, StringType))), "[{\"key\":\"1\",\"value\":\"one\"},{\"key\":\"2\",\"value\":\"two\"}]")); // Normal case
        // Edge case: dict with non-string keys, sorted by key
        $(assert.equal(printJson(East.value(new Map<bigint, string>([[3n, "c"], [1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType))), "[{\"key\":\"1\",\"value\":\"a\"},{\"key\":\"2\",\"value\":\"b\"},{\"key\":\"3\",\"value\":\"c\"}]"));

        // Struct - JSON object
        $(assert.equal(printJson(East.value({})), "{}")); // Edge case: empty struct
        $(assert.equal(printJson(East.value({ a: 1n })), "{\"a\":\"1\"}")); // Edge case: single field
        $(assert.equal(printJson(East.value({ a: 1n, b: true })), "{\"a\":\"1\",\"b\":true}")); // Normal case: multiple fields
        $(assert.equal(printJson(East.value({ name: "Alice", age: 30n })), "{\"name\":\"Alice\",\"age\":\"30\"}")); // Normal case

        // Variant - {"type": "caseName", "value": ...}
        $(assert.equal(printJson(East.value(variant("none", null))), "{\"type\":\"none\",\"value\":null}")); // Edge case: nullary variant (null payload)
        $(assert.equal(printJson(East.value(variant("some", 42n))), "{\"type\":\"some\",\"value\":\"42\"}")); // Normal case: variant with data
        $(assert.equal(printJson(East.value(variant("ok", "success"))), "{\"type\":\"ok\",\"value\":\"success\"}")); // Normal case
        $(assert.equal(printJson(East.value(variant("error", "failure"))), "{\"type\":\"error\",\"value\":\"failure\"}")); // Normal case

        // Recursive type - linked list
        const LinkedListType = RecursiveType(list => VariantType({
            cons: StructType({
                head: IntegerType,
                tail: list
            }),
            nil: NullType
        }));
        const list0 = $.let(variant("nil", null), LinkedListType);
        const list1 = $.let(variant("cons", { head: 1n, tail: list0 }), LinkedListType);
        const list2 = $.let(variant("cons", { head: 2n, tail: list1 }), LinkedListType);
        $(assert.equal(printJson(list0), "{\"type\":\"nil\",\"value\":null}"));
        $(assert.equal(printJson(list1), "{\"type\":\"cons\",\"value\":{\"head\":\"1\",\"tail\":{\"type\":\"nil\",\"value\":null}}}"));
        $(assert.equal(printJson(list2), "{\"type\":\"cons\",\"value\":{\"head\":\"2\",\"tail\":{\"type\":\"cons\",\"value\":{\"head\":\"1\",\"tail\":{\"type\":\"nil\",\"value\":null}}}}}"));

        // Recursive type - East types
        const nullType = $.let(toEastTypeValue(NullType), EastTypeType);
        const booleanType = $.let(toEastTypeValue(BooleanType), EastTypeType);
        const integerType = $.let(toEastTypeValue(IntegerType), EastTypeType);
        const floatType = $.let(toEastTypeValue(FloatType), EastTypeType);
        const dateTimeType = $.let(toEastTypeValue(DateTimeType), EastTypeType);
        const stringType = $.let(toEastTypeValue(StringType), EastTypeType);
        const blobType = $.let(toEastTypeValue(BlobType), EastTypeType);
        const refType = $.let(toEastTypeValue(RefType(IntegerType)), EastTypeType);
        const arrayType = $.let(toEastTypeValue(ArrayType(IntegerType)), EastTypeType);
        const setType = $.let(toEastTypeValue(SetType(StringType)), EastTypeType);
        const dictType = $.let(toEastTypeValue(DictType(StringType, IntegerType)), EastTypeType);
        const structType = $.let(toEastTypeValue(StructType({ name: StringType, age: IntegerType })), EastTypeType);
        const variantType = $.let(toEastTypeValue(VariantType({ none: NullType, some: IntegerType })), EastTypeType);
        const linkedListType = $.let(toEastTypeValue(LinkedListType), EastTypeType);

        $(assert.equal(printJson(nullType), '{"type":"Null","value":null}'));
        $(assert.equal(printJson(booleanType), '{"type":"Boolean","value":null}'));
        $(assert.equal(printJson(integerType), '{"type":"Integer","value":null}'));
        $(assert.equal(printJson(floatType), '{"type":"Float","value":null}'));
        $(assert.equal(printJson(dateTimeType), '{"type":"DateTime","value":null}'));
        $(assert.equal(printJson(stringType), '{"type":"String","value":null}'));
        $(assert.equal(printJson(blobType), '{"type":"Blob","value":null}'));
        $(assert.equal(printJson(refType), '{"type":"Ref","value":{"type":"Integer","value":null}}'));
        $(assert.equal(printJson(arrayType), '{"type":"Array","value":{"type":"Integer","value":null}}'));
        $(assert.equal(printJson(setType), '{"type":"Set","value":{"type":"String","value":null}}'));
        $(assert.equal(printJson(dictType), '{"type":"Dict","value":{"key":{"type":"String","value":null},"value":{"type":"Integer","value":null}}}'));
        $(assert.equal(printJson(structType), '{"type":"Struct","value":[{"name":"name","type":{"type":"String","value":null}},{"name":"age","type":{"type":"Integer","value":null}}]}'));
        $(assert.equal(printJson(variantType), '{"type":"Variant","value":[{"name":"none","type":{"type":"Null","value":null}},{"name":"some","type":{"type":"Integer","value":null}}]}'));
        $(assert.equal(printJson(linkedListType), '{"type":"Variant","value":[{"name":"cons","type":{"type":"Struct","value":[{"name":"head","type":{"type":"Integer","value":null}},{"name":"tail","type":{"type":"Recursive","value":"2"}}]}},{"name":"nil","type":{"type":"Null","value":null}}]}'));
    });
    
    test("JSON parse", $ => {
        const MAX_INT64 = 9223372036854775807n; // 2^63 - 1
        const MIN_INT64 = -9223372036854775808n; // -2^63
        // Null
        $(assert.equal(East.value("null").parseJson(NullType), null));

        // Boolean
        $(assert.equal(East.value("true").parseJson(BooleanType), true));
        $(assert.equal(East.value("false").parseJson(BooleanType), false));

        // Integer - parsed from strings
        $(assert.equal(East.value("\"0\"").parseJson(IntegerType), 0n));
        $(assert.equal(East.value("\"42\"").parseJson(IntegerType), 42n)); // Normal case
        $(assert.equal(East.value("\"-123\"").parseJson(IntegerType), -123n)); // Normal case
        $(assert.equal(East.value("\"1\"").parseJson(IntegerType), 1n));
        $(assert.equal(East.value("\"-1\"").parseJson(IntegerType), -1n));
        // Edge cases: INT64 bounds
        $(assert.equal(East.value("\"9223372036854775807\"").parseJson(IntegerType), MAX_INT64)); // MAX_INT64
        $(assert.equal(East.value("\"-9223372036854775808\"").parseJson(IntegerType), MIN_INT64)); // MIN_INT64
        $(assert.equal(East.value("\"9223372036854775806\"").parseJson(IntegerType), MAX_INT64 - 1n)); // MAX_INT64 - 1
        $(assert.equal(East.value("\"-9223372036854775807\"").parseJson(IntegerType), MIN_INT64 + 1n)); // MIN_INT64 + 1

        // Float - normal values (from JSON numbers)
        $(assert.equal(East.value("0").parseJson(FloatType), 0.0));
        $(assert.equal(East.value("1").parseJson(FloatType), 1.0));
        $(assert.equal(East.value("-1").parseJson(FloatType), -1.0));
        $(assert.equal(East.value("3.14").parseJson(FloatType), 3.14));
        $(assert.equal(East.value("-2.5").parseJson(FloatType), -2.5));
        // Float - boundary values
        $(assert.equal(East.value(String(Number.MAX_VALUE)).parseJson(FloatType), Number.MAX_VALUE));
        $(assert.equal(East.value(String(-Number.MAX_VALUE)).parseJson(FloatType), -Number.MAX_VALUE));
        $(assert.equal(East.value(String(Number.MIN_VALUE)).parseJson(FloatType), Number.MIN_VALUE));
        $(assert.equal(East.value(String(Number.EPSILON)).parseJson(FloatType), Number.EPSILON));
        // Float - special values (from strings - CRITICAL!)
        $(assert.equal(East.value("\"-0.0\"").parseJson(FloatType), -0.0)); // Negative zero
        $(assert.equal(East.value("\"NaN\"").parseJson(FloatType), NaN));
        $(assert.equal(East.value("\"Infinity\"").parseJson(FloatType), Infinity));
        $(assert.equal(East.value("\"-Infinity\"").parseJson(FloatType), -Infinity));

        // String - RFC 3339 strings
        $(assert.equal(East.value("\"\"").parseJson(StringType), "")); // Edge case: empty string
        $(assert.equal(East.value("\"hello\"").parseJson(StringType), "hello")); // Normal case: ASCII
        $(assert.equal(East.value("\"café\"").parseJson(StringType), "café")); // Edge case: Latin with diacritic
        $(assert.equal(East.value("\"🚀🌟\"").parseJson(StringType), "🚀🌟")); // Edge case: Emoji (multi-byte UTF-8)
        $(assert.equal(East.value("\"東京\"").parseJson(StringType), "東京")); // Edge case: CJK characters
        $(assert.equal(East.value("\"いろはにほへと\"").parseJson(StringType), "いろはにほへと")); // Edge case: Hiragana

        // DateTime - RFC 3339 strings
        $(assert.equal(East.value("\"1970-01-01T00:00:00.000Z\"").parseJson(DateTimeType), new Date("1970-01-01T00:00:00.000Z"))); // Edge case: Unix epoch
        $(assert.equal(East.value("\"1969-12-31T23:59:59.999Z\"").parseJson(DateTimeType), new Date("1969-12-31T23:59:59.999Z"))); // Edge case: Before epoch (negative timestamp)
        $(assert.equal(East.value("\"2024-01-15T10:30:00.123Z\"").parseJson(DateTimeType), new Date("2024-01-15T10:30:00.123Z"))); // Normal case
        $(assert.equal(East.value("\"1900-01-01T00:00:00.000Z\"").parseJson(DateTimeType), new Date("1900-01-01T00:00:00.000Z"))); // Edge case: Far past
        $(assert.equal(East.value("\"2100-12-31T23:59:59.999Z\"").parseJson(DateTimeType), new Date("2100-12-31T23:59:59.999Z"))); // Edge case: Far future

        // Blob - hex strings
        $(assert.equal(East.value("\"0x\"").parseJson(BlobType), new Uint8Array([]))); // Edge case: empty blob
        $(assert.equal(East.value("\"0x00\"").parseJson(BlobType), new Uint8Array([0x00]))); // Edge case: single zero byte (minimum)
        $(assert.equal(East.value("\"0xff\"").parseJson(BlobType), new Uint8Array([0xff]))); // Edge case: single 0xFF byte (maximum)
        $(assert.equal(East.value("\"0x00ff\"").parseJson(BlobType), new Uint8Array([0x00, 0xff]))); // Edge case: min and max bytes together
        $(assert.equal(East.value("\"0x48656c6c6f\"").parseJson(BlobType), new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]))); // Normal case: "Hello" in hex

        // Ref - JSON array with single element
        $(assert.equal(East.value("[null]").parseJson(RefType(NullType)), ref(null)));
        $(assert.equal(East.value("[\"42\"]").parseJson(RefType(IntegerType)), ref(42n)));

        // Array - JSON arrays
        $(assert.equal(East.value("[]").parseJson(ArrayType(IntegerType)), [])); // Edge case: empty array
        $(assert.equal(East.value("[\"1\"]").parseJson(ArrayType(IntegerType)), [1n])); // Edge case: single element
        $(assert.equal(East.value("[\"1\",\"2\",\"3\"]").parseJson(ArrayType(IntegerType)), [1n, 2n, 3n])); // Normal case
        $(assert.equal(East.value("[\"a\",\"b\"]").parseJson(ArrayType(StringType)), ["a", "b"])); // Normal case
        // Nested arrays
        $(assert.equal(East.value("[[\"1\",\"2\"],[\"3\",\"4\"]]").parseJson(ArrayType(ArrayType(IntegerType))), [[1n, 2n], [3n, 4n]])); // Edge case: nested structure
        // Edge case: boundary integers in array
        $(assert.equal(East.value("[\"9223372036854775807\",\"-9223372036854775808\"]").parseJson(ArrayType(IntegerType)), [MAX_INT64, MIN_INT64]));

        // Set - JSON arrays
        $(assert.equal(East.value("[]").parseJson(SetType(IntegerType)), new Set([]))); // Edge case: empty set
        $(assert.equal(East.value("[\"1\"]").parseJson(SetType(IntegerType)), new Set([1n]))); // Edge case: single element
        $(assert.equal(East.value("[\"1\",\"2\",\"3\"]").parseJson(SetType(IntegerType)), new Set([1n, 2n, 3n]))); // Normal case
        $(assert.equal(East.value("[\"a\",\"b\",\"c\"]").parseJson(SetType(StringType)), new Set(["a", "b", "c"]))); // Normal case

        // Dict - arrays of {"key": ..., "value": ...} objects
        $(assert.equal(East.value("[]").parseJson(DictType(IntegerType, StringType)), new Map([]))); // Edge case: empty dict
        $(assert.equal(East.value("[{\"key\":\"1\",\"value\":\"one\"}]").parseJson(DictType(IntegerType, StringType)), new Map([[1n, "one"]]))); // Edge case: single entry
        $(assert.equal(East.value("[{\"key\":\"1\",\"value\":\"one\"},{\"key\":\"2\",\"value\":\"two\"}]").parseJson(DictType(IntegerType, StringType)), new Map([[1n, "one"], [2n, "two"]]))); // Normal case

        // Struct - JSON objects
        $(assert.equal(East.value("{}").parseJson(StructType({})), {})); // Edge case: empty struct
        $(assert.equal(East.value("{\"a\":\"1\"}").parseJson(StructType({ a: IntegerType })), { a: 1n })); // Edge case: single field
        $(assert.equal(East.value("{\"a\":\"1\",\"b\":true}").parseJson(StructType({ a: IntegerType, b: BooleanType })), { a: 1n, b: true })); // Normal case: multiple fields
        $(assert.equal(East.value("{\"name\":\"Alice\",\"age\":\"30\"}").parseJson(StructType({ name: StringType, age: IntegerType })), { name: "Alice", age: 30n })); // Normal case

        // Variant - {"type": "caseName", "value": ...}
        $(assert.equal(East.value("{\"type\":\"none\",\"value\":null}").parseJson(VariantType({ none: NullType, some: IntegerType })), variant("none", null))); // Edge case: nullary variant (null payload)
        $(assert.equal(East.value("{\"type\":\"some\",\"value\":\"42\"}").parseJson(VariantType({ none: NullType, some: IntegerType })), variant("some", 42n))); // Normal case: variant with data
        $(assert.equal(East.value("{\"type\":\"ok\",\"value\":\"success\"}").parseJson(VariantType({ ok: StringType, error: StringType })), variant("ok", "success"))); // Normal case
        $(assert.equal(East.value("{\"type\":\"error\",\"value\":\"failure\"}").parseJson(VariantType({ ok: StringType, error: StringType })), variant("error", "failure"))); // Normal case

        // Recursive type - linked list
        const LinkedListType = RecursiveType(list => VariantType({
            cons: StructType({
                head: IntegerType,
                tail: list
            }),
            nil: NullType
        }));
        const list0 = $.let(variant("nil", null), LinkedListType);
        const list1 = $.let(variant("cons", { head: 1n, tail: list0 }), LinkedListType);
        const list2 = $.let(variant("cons", { head: 2n, tail: list1 }), LinkedListType);
        $(assert.equal(East.value("{\"type\":\"nil\",\"value\":null}").parseJson(LinkedListType), list0));
        $(assert.equal(East.value("{\"type\":\"cons\",\"value\":{\"head\":\"1\",\"tail\":{\"type\":\"nil\",\"value\":null}}}").parseJson(LinkedListType), list1));
        $(assert.equal(East.value("{\"type\":\"cons\",\"value\":{\"head\":\"2\",\"tail\":{\"type\":\"cons\",\"value\":{\"head\":\"1\",\"tail\":{\"type\":\"nil\",\"value\":null}}}}}").parseJson(LinkedListType), list2));

        // Recursive type - East types
        const nullType = $.let(toEastTypeValue(NullType), EastTypeType);
        const booleanType = $.let(toEastTypeValue(BooleanType), EastTypeType);
        const integerType = $.let(toEastTypeValue(IntegerType), EastTypeType);
        const floatType = $.let(toEastTypeValue(FloatType), EastTypeType);
        const dateTimeType = $.let(toEastTypeValue(DateTimeType), EastTypeType);
        const stringType = $.let(toEastTypeValue(StringType), EastTypeType);
        const blobType = $.let(toEastTypeValue(BlobType), EastTypeType);
        const refType = $.let(toEastTypeValue(RefType(IntegerType)), EastTypeType);
        const arrayType = $.let(toEastTypeValue(ArrayType(IntegerType)), EastTypeType);
        const setType = $.let(toEastTypeValue(SetType(StringType)), EastTypeType);
        const dictType = $.let(toEastTypeValue(DictType(StringType, IntegerType)), EastTypeType);
        const structType = $.let(toEastTypeValue(StructType({ name: StringType, age: IntegerType })), EastTypeType);
        const variantType = $.let(toEastTypeValue(VariantType({ none: NullType, some: IntegerType })), EastTypeType);
        const linkedListType = $.let(toEastTypeValue(LinkedListType), EastTypeType);

        $(assert.equal(East.value('{"type":"Null","value":null}').parseJson(EastTypeType), nullType));
        $(assert.equal(East.value('{"type":"Boolean","value":null}').parseJson(EastTypeType), booleanType));
        $(assert.equal(East.value('{"type":"Integer","value":null}').parseJson(EastTypeType), integerType));
        $(assert.equal(East.value('{"type":"Float","value":null}').parseJson(EastTypeType), floatType));
        $(assert.equal(East.value('{"type":"DateTime","value":null}').parseJson(EastTypeType), dateTimeType));
        $(assert.equal(East.value('{"type":"String","value":null}').parseJson(EastTypeType), stringType));
        $(assert.equal(East.value('{"type":"Blob","value":null}').parseJson(EastTypeType), blobType));
        $(assert.equal(East.value('{"type":"Ref","value":{"type":"Integer","value":null}}').parseJson(EastTypeType), refType));
        $(assert.equal(East.value('{"type":"Array","value":{"type":"Integer","value":null}}').parseJson(EastTypeType), arrayType));
        $(assert.equal(East.value('{"type":"Set","value":{"type":"String","value":null}}').parseJson(EastTypeType), setType));
        $(assert.equal(East.value('{"type":"Dict","value":{"key":{"type":"String","value":null},"value":{"type":"Integer","value":null}}}').parseJson(EastTypeType), dictType));
        $(assert.equal(East.value('{"type":"Struct","value":[{"name":"name","type":{"type":"String","value":null}},{"name":"age","type":{"type":"Integer","value":null}}]}').parseJson(EastTypeType), structType));
        $(assert.equal(East.value('{"type":"Variant","value":[{"name":"none","type":{"type":"Null","value":null}},{"name":"some","type":{"type":"Integer","value":null}}]}').parseJson(EastTypeType), variantType));
        $(assert.equal(East.value('{"type":"Variant","value":[{"name":"cons","type":{"type":"Struct","value":[{"name":"head","type":{"type":"Integer","value":null}},{"name":"tail","type":{"type":"Recursive","value":"2"}}]}},{"name":"nil","type":{"type":"Null","value":null}}]}').parseJson(EastTypeType), linkedListType));
    });

    test("JSON parsing error messages", $ => {
        // === Primitive Type Validation Errors ===

        // Null - wrong type
        $(assert.throws(
            East.value("\"not null\"").parseJson(NullType),
            /Error occurred because expected null, got "not null" \(line 1, col 1\) while parsing value of type "\.Null"/
        ));
        $(assert.throws(
            East.value("123").parseJson(NullType),
            /Error occurred because expected null, got 123 \(line 1, col 1\) while parsing value of type "\.Null"/
        ));

        // Boolean - wrong type
        $(assert.throws(
            East.value("\"not a boolean\"").parseJson(BooleanType),
            /Error occurred because expected boolean, got "not a boolean" \(line 1, col 1\) while parsing value of type "\.Boolean"/
        ));
        $(assert.throws(
            East.value("123").parseJson(BooleanType),
            /Error occurred because expected boolean, got 123 \(line 1, col 1\) while parsing value of type "\.Boolean"/
        ));

        // String - wrong type
        $(assert.throws(
            East.value("123").parseJson(StringType),
            /Error occurred because expected string, got 123 \(line 1, col 1\) while parsing value of type "\.String"/
        ));
        $(assert.throws(
            East.value("true").parseJson(StringType),
            /Error occurred because expected string, got true \(line 1, col 1\) while parsing value of type "\.String"/
        ));

        // Float - wrong type (must be number or special string)
        $(assert.throws(
            East.value("\"not a float\"").parseJson(FloatType),
            /Error occurred because expected number or string representing special float value, got "not a float" \(line 1, col 1\) while parsing value of type "\.Float"/
        ));
        $(assert.throws(
            East.value("true").parseJson(FloatType),
            /Error occurred because expected number or string representing special float value, got true \(line 1, col 1\) while parsing value of type "\.Float"/
        ));

        // Integer - not a string
        $(assert.throws(
            East.value("123").parseJson(IntegerType),
            /Error occurred because expected string representing integer, got 123 \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));
        // Integer - empty string
        $(assert.throws(
            East.value("\"\"").parseJson(IntegerType),
            /Error occurred because expected string representing integer, got "" \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));
        // Integer - non-numeric string
        $(assert.throws(
            East.value("\"abc\"").parseJson(IntegerType),
            /Error occurred because expected string representing integer, got "abc" \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));
        // Integer - overflow (> MAX_INT64)
        $(assert.throws(
            East.value("\"9223372036854775808\"").parseJson(IntegerType),
            /Error occurred because integer out of range \(must be 64-bit signed\), got "9223372036854775808" \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));
        // Integer - underflow (< MIN_INT64)
        $(assert.throws(
            East.value("\"-9223372036854775809\"").parseJson(IntegerType),
            /Error occurred because integer out of range \(must be 64-bit signed\), got "-9223372036854775809" \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));

        // DateTime - not a string
        $(assert.throws(
            East.value("123").parseJson(DateTimeType),
            /Error occurred because expected string for DateTime, got 123 \(line 1, col 1\) while parsing value of type "\.DateTime"/
        ));
        // DateTime - missing timezone
        $(assert.throws(
            East.value("\"2024-01-15T10:30:00.123\"").parseJson(DateTimeType),
            /Error occurred because expected ISO 8601 date string with timezone/
        ));
        // DateTime - invalid date value
        $(assert.throws(
            East.value("\"2024-13-40T25:70:99.999Z\"").parseJson(DateTimeType),
            /Error occurred because invalid date string, got "2024-13-40T25:70:99.999Z" \(line 1, col 1\) while parsing value of type "\.DateTime"/
        ));

        // Blob - not a string
        $(assert.throws(
            East.value("123").parseJson(BlobType),
            /Error occurred because expected hex string starting with 0x, got 123 \(line 1, col 1\) while parsing value of type "\.Blob"/
        ));
        // Blob - missing 0x prefix
        $(assert.throws(
            East.value("\"48656c6c6f\"").parseJson(BlobType),
            /Error occurred because expected hex string starting with 0x, got "48656c6c6f" \(line 1, col 1\) while parsing value of type "\.Blob"/
        ));
        // Blob - odd number of hex digits or invalid hex
        $(assert.throws(
            East.value("\"0x123\"").parseJson(BlobType),
            /Error occurred because invalid hex string, got "0x123" \(line 1, col 1\) while parsing value of type "\.Blob"/
        ));
        // Blob - invalid hex characters
        $(assert.throws(
            East.value("\"0xZZZZ\"").parseJson(BlobType),
            /Error occurred because invalid hex string, got "0xZZZZ" \(line 1, col 1\) while parsing value of type "\.Blob"/
        ));

        // === Collection Type Validation Errors ===

        // Array - not an array
        $(assert.throws(
            East.value("\"not an array\"").parseJson(ArrayType(IntegerType)),
            /Error occurred because expected array, got "not an array" \(line 1, col 1\) while parsing value of type "\.Array \.Integer"/
        ));
        $(assert.throws(
            East.value("123").parseJson(ArrayType(IntegerType)),
            /Error occurred because expected array, got 123 \(line 1, col 1\) while parsing value of type "\.Array \.Integer"/
        ));

        // Set - not an array
        $(assert.throws(
            East.value("\"not an array\"").parseJson(SetType(IntegerType)),
            /Error occurred because expected array for Set, got "not an array" \(line 1, col 1\) while parsing value of type "\.Set \.Integer"/
        ));
        $(assert.throws(
            East.value("123").parseJson(SetType(IntegerType)),
            /Error occurred because expected array for Set, got 123 \(line 1, col 1\) while parsing value of type "\.Set \.Integer"/
        ));

        // Dict - not an array
        $(assert.throws(
            East.value("\"not an array\"").parseJson(DictType(StringType, IntegerType)),
            /Error occurred because expected array for Dict, got "not an array" \(line 1, col 1\) while parsing value of type .*/
        ));
        $(assert.throws(
            East.value("123").parseJson(DictType(StringType, IntegerType)),
            /Error occurred because expected array for Dict, got 123 \(line 1, col 1\) while parsing value of type .*/
        ));
        // Dict entry - not an object
        $(assert.throws(
            East.value("[\"not an object\"]").parseJson(DictType(StringType, IntegerType)),
            /Error occurred because expected object with key and value for Dict entry, got "not an object" at \[0\] \(line 1, col 1\) while parsing value of type .*/
        ));

        // Struct - not an object
        $(assert.throws(
            East.value("\"not an object\"").parseJson(StructType({ x: IntegerType })),
            /Error occurred because expected object for Struct, got "not an object" \(line 1, col 1\) while parsing value of type .*/
        ));
        $(assert.throws(
            East.value("123").parseJson(StructType({ x: IntegerType })),
            /Error occurred because expected object for Struct, got 123 \(line 1, col 1\) while parsing value of type .*/
        ));
        $(assert.throws(
            East.value("null").parseJson(StructType({ x: IntegerType })),
            /Error occurred because expected object for Struct, got null \(line 1, col 1\) while parsing value of type .*/
        ));

        // Variant - not an object
        $(assert.throws(
            East.value("\"not an object\"").parseJson(VariantType({ some: IntegerType, none: NullType })),
            /Error occurred because expected object with type and value for Variant, got "not an object" \(line 1, col 1\) while parsing value of type .*/
        ));
        $(assert.throws(
            East.value("123").parseJson(VariantType({ some: IntegerType, none: NullType })),
            /Error occurred because expected object with type and value for Variant, got 123 \(line 1, col 1\) while parsing value of type .*/
        ));
        // Variant - missing "type" or "value" field
        $(assert.throws(
            East.value("{\"value\":\"42\"}").parseJson(VariantType({ some: IntegerType, none: NullType })),
            /Error occurred because expected object with type and value for Variant, got \{"value":"42"\} \(line 1, col 1\) while parsing value of type .*/
        ));
        $(assert.throws(
            East.value("{\"type\":\"some\"}").parseJson(VariantType({ some: IntegerType, none: NullType })),
            /Error occurred because expected object with type and value for Variant, got \{"type":"some"\} \(line 1, col 1\) while parsing value of type .*/
        ));

        // === Nested Structure Errors (existing tests) ===

        // Test error with path for nested array
        $(assert.throws(
            East.value("[\"42\", \"not an integer\"]").parseJson(ArrayType(IntegerType)),
            /Error occurred because expected string representing integer, got "not an integer" at \[1\] \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error with path for struct field
        $(assert.throws(
            East.value("{\"name\":\"Alice\",\"age\":42}").parseJson(StructType({ name: StringType, age: IntegerType })),
            /Error occurred because expected string representing integer, got 42 at \.age \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for missing struct field
        $(assert.throws(
            East.value("{\"name\":\"Alice\"}").parseJson(StructType({ name: StringType, age: IntegerType })),
            /Error occurred because missing field "age" in Struct, got \{"name":"Alice"\} \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for unexpected struct field
        $(assert.throws(
            East.value("{\"name\":\"Alice\",\"extra\":\"unexpected\"}").parseJson(StructType({ name: StringType })),
            /Error occurred because unexpected field "extra" in Struct, got \{"name":"Alice","extra":"unexpected"\} \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for dict entry value
        $(assert.throws(
            East.value("[{\"key\":\"a\",\"value\":\"not an integer\"}]").parseJson(DictType(StringType, IntegerType)),
            /Error occurred because expected string representing integer, got "not an integer" at \[0\]\.value \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for variant case value
        $(assert.throws(
            East.value("{\"type\":\"some\",\"value\":\"not an integer\"}").parseJson(VariantType({ none: NullType, some: IntegerType })),
            /Error occurred because expected string representing integer, got "not an integer" at \.some \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for unknown variant type
        $(assert.throws(
            East.value("{\"type\":\"unknown\",\"value\":null}").parseJson(VariantType({ none: NullType, some: IntegerType })),
            /Error occurred because unknown variant type "unknown", got \{"type":"unknown","value":null\} \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for deeply nested structure - array of structs with error in second element
        $(assert.throws(
            East.value("[{\"id\":\"1\",\"name\":\"Alice\"},{\"id\":\"not an int\",\"name\":\"Bob\"}]").parseJson(ArrayType(StructType({ id: IntegerType, name: StringType }))),
            /Error occurred because expected string representing integer, got "not an int" at \[1\]\.id \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for dict with array values - error in array element
        $(assert.throws(
            East.value("[{\"key\":\"nums\",\"value\":[\"1\",\"2\",\"not an int\"]}]").parseJson(DictType(StringType, ArrayType(IntegerType))),
            /Error occurred because expected string representing integer, got "not an int" at \[0\]\.value\[2\] \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for struct containing variant with error
        $(assert.throws(
            East.value("{\"result\":{\"type\":\"ok\",\"value\":\"not an int\"}}").parseJson(StructType({ result: VariantType({ ok: IntegerType, error: StringType }) })),
            /Error occurred because expected string representing integer, got "not an int" at \.result\.ok \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for set element
        $(assert.throws(
            East.value("[\"1\",\"2\",\"not an int\"]").parseJson(SetType(IntegerType)),
            /Error occurred because expected string representing integer, got "not an int" at \[2\] \(line 1, col 1\) while parsing value of type "\.Set \.Integer"/
        ));

        // Test error for dict with missing key field
        $(assert.throws(
            East.value("[{\"value\":\"123\"}]").parseJson(DictType(StringType, IntegerType)),
            /Error occurred because expected object with key and value for Dict entry, got \{"value":"123"\} at \[0\] \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for dict with extra field
        $(assert.throws(
            East.value("[{\"key\":\"a\",\"value\":\"123\",\"extra\":\"bad\"}]").parseJson(DictType(StringType, IntegerType)),
            /Error occurred because unexpected field "extra" in Dict entry, got \{"key":"a","value":"123","extra":"bad"\} at \[0\] \(line 1, col 1\) while parsing value of type .*/
        ));
    });

    test("East parsing error messages", $ => {
        // === Primitive Type Validation Errors ===

        // Null - wrong input (identifier that's not 'null')
        $(assert.throws(
            East.value("false").parse(NullType),
            /Error occurred because expected null, got 'f' \(line 1, col 1\) while parsing value of type "\.Null"/
        ));
        $(assert.throws(
            East.value("123").parse(NullType),
            /Error occurred because expected null, got '1' \(line 1, col 1\) while parsing value of type "\.Null"/
        ));

        // Boolean - wrong input (identifier that's not 'true'/'false')
        $(assert.throws(
            East.value("null").parse(BooleanType),
            /Error occurred because expected boolean, got 'n' \(line 1, col 1\) while parsing value of type "\.Boolean"/
        ));
        $(assert.throws(
            East.value("123").parse(BooleanType),
            /Error occurred because expected boolean, got '1' \(line 1, col 1\) while parsing value of type "\.Boolean"/
        ));

        // String - wrong input (not starting with quote)
        $(assert.throws(
            East.value("123").parse(StringType),
            /Error occurred because expected '\"', got '1' \(line 1, col 1\) while parsing value of type "\.String"/
        ));
        $(assert.throws(
            East.value("true").parse(StringType),
            /Error occurred because expected '\"', got 't' \(line 1, col 1\) while parsing value of type "\.String"/
        ));

        // Float - wrong input (not a number)
        $(assert.throws(
            East.value("\"not a float\"").parse(FloatType),
            /Error occurred because expected float, got '\"' \(line 1, col 1\) while parsing value of type "\.Float"/
        ));
        $(assert.throws(
            East.value("true").parse(FloatType),
            /Error occurred because expected float, got 't' \(line 1, col 1\) while parsing value of type "\.Float"/
        ));

        // Integer - empty input
        $(assert.throws(
            East.value("").parse(IntegerType),
            /Error occurred because expected integer, got end of input \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));
        // Integer - non-numeric input
        $(assert.throws(
            East.value("abc").parse(IntegerType),
            /Error occurred because expected integer, got 'a' \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));
        // Integer - overflow (> MAX_INT64)
        $(assert.throws(
            East.value("9223372036854775808").parse(IntegerType),
            /Error occurred because integer out of range \(must be 64-bit signed\), got 9223372036854775808 \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));
        // Integer - underflow (< MIN_INT64)
        $(assert.throws(
            East.value("-9223372036854775809").parse(IntegerType),
            /Error occurred because integer out of range \(must be 64-bit signed\), got -9223372036854775809 \(line 1, col 1\) while parsing value of type "\.Integer"/
        ));

        // DateTime - wrong format (not YYYY-MM-DD...)
        $(assert.throws(
            East.value("123").parse(DateTimeType),
            /Error occurred because expected DateTime in format YYYY-MM-DDTHH:MM:SS\.sss \(line 1, col 1\) while parsing value of type "\.DateTime"/
        ));

        // Blob - invalid hex characters (caught as unexpected input after valid parse)
        $(assert.throws(
            East.value("0xZZZZ").parse(BlobType),
            /Error occurred because unexpected input after parsed value \(line 1, col 3\) while parsing value of type "\.Blob"/
        ));

        // === Collection Type Validation Errors ===

        // Array - not starting with '['
        $(assert.throws(
            East.value("\"not an array\"").parse(ArrayType(IntegerType)),
            /Error occurred because expected '\[' to start array \(line 1, col 1\) while parsing value of type "\.Array \.Integer"/
        ));
        $(assert.throws(
            East.value("123").parse(ArrayType(IntegerType)),
            /Error occurred because expected '\[' to start array \(line 1, col 1\) while parsing value of type "\.Array \.Integer"/
        ));

        // Set - not starting with '{'
        $(assert.throws(
            East.value("\"not a set\"").parse(SetType(IntegerType)),
            /Error occurred because expected '\{' to start set \(line 1, col 1\) while parsing value of type "\.Set \.Integer"/
        ));
        $(assert.throws(
            East.value("123").parse(SetType(IntegerType)),
            /Error occurred because expected '\{' to start set \(line 1, col 1\) while parsing value of type "\.Set \.Integer"/
        ));

        // Dict - not starting with '{'
        $(assert.throws(
            East.value("\"not a dict\"").parse(DictType(StringType, IntegerType)),
            /Error occurred because expected '\{' to start dict \(line 1, col 1\) while parsing value of type .*/
        ));
        $(assert.throws(
            East.value("123").parse(DictType(StringType, IntegerType)),
            /Error occurred because expected '\{' to start dict \(line 1, col 1\) while parsing value of type .*/
        ));

        // Struct - not starting with '('
        $(assert.throws(
            East.value("\"not a struct\"").parse(StructType({ x: IntegerType })),
            /Error occurred because expected '\(' to start struct \(line 1, col 1\) while parsing value of type .*/
        ));
        $(assert.throws(
            East.value("123").parse(StructType({ x: IntegerType })),
            /Error occurred because expected '\(' to start struct \(line 1, col 1\) while parsing value of type .*/
        ));

        // === Existing East-specific Tests ===

        // Test error on unsupported escape sequence
        $(assert.throws(
            East.value("\"hello\\nworld\"").parse(StringType),
            /Error occurred because unexpected escape sequence in string \(line 1, col 8\) while parsing value of type .*/
        ));

        // Test error on array with trailing comma
        $(assert.throws(
            East.value("[\"a\", \"b\",]").parse(ArrayType(StringType)),
            /Error occurred because expected '\"', got '\]' at \[2\] \(line 1, col 11\) while parsing value of type .*/
        ));

        // Test error on set with trailing comma
        $(assert.throws(
            East.value("{\"a\", \"b\",}").parse(SetType(StringType)),
            /Error occurred because expected '\"', got '\}' at \[2\] \(line 1, col 11\) while parsing value of type .*/
        ));

        // Test error on dict with trailing comma
        $(assert.throws(
            East.value("{\"a\": 1, \"b\": 2,}").parse(DictType(StringType, IntegerType)),
            /Error occurred because expected '\"', got '\}' at \[2\]\(key\) \(line 1, col 17\) while parsing value of type .*/
        ));

        // Test error on missing required struct field
        $(assert.throws(
            East.value("(name=\"Alice\")").parse(StructType({ name: StringType, age: IntegerType })),
            /Error occurred because missing required field 'age' \(line 1, col 14\) while parsing value of type .*/
        ));

        // Test error on unknown struct field
        $(assert.throws(
            East.value("(name=\"Alice\", unknown=\"value\")").parse(StructType({ name: StringType })),
            /Error occurred because expected '\)' to close struct \(line 1, col 16\) while parsing value of type .*/
        ));

        // Test error on unknown variant case
        $(assert.throws(
            East.value(".unknown").parse(VariantType({ success: NullType, error: StringType })),
            /Error occurred because unknown variant case \.unknown, expected one of: \.error, \.success \(line 1, col 2\) while parsing value of type .*/
        ));

        // Test error on variant case with incorrect payload
        $(assert.throws(
            East.value(".error 42").parse(VariantType({ success: NullType, error: StringType })),
            /Error occurred because expected '\"', got '4' at \.error \(line 1, col 8\) while parsing value of type .*/
        ));

        // Test error when data is provided for nullary case
        $(assert.throws(
            East.value(".success \"unexpected\"").parse(VariantType({ success: NullType, error: StringType })),
            /Error occurred because expected null, got '\"' at \.success \(line 1, col 10\) while parsing value of type .*/
        ));

        // Test error when no data is provided for data case
        $(assert.throws(
            East.value(".error").parse(VariantType({ success: NullType, error: StringType })),
            /Error occurred because expected '\"', got end of input at \.error \(line 1, col 7\) while parsing value of type .*/
        ));

        // Test error for type mismatch
        $(assert.throws(
            East.value("\"not a number\"").parse(IntegerType),
            /Error occurred because expected integer, got '\"' \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for malformed array input
        $(assert.throws(
            East.value("[unclosed array").parse(ArrayType(StringType)),
            /Error occurred because expected '\"', got 'u' at \[0\] \(line 1, col 2\) while parsing value of type .*/
        ));

        // Test error for extra tokens
        $(assert.throws(
            East.value("\"hello\" extra").parse(StringType),
            /Error occurred because unexpected input after parsed value \(line 1, col 9\) while parsing value of type .*/
        ));

        // Test error on unterminated string
        $(assert.throws(
            East.value("\"unterminated").parse(StringType),
            /Error occurred because unterminated string \(missing closing quote\) \(line 1, col 14\) while parsing value of type .*/
        ));

        // Test error on invalid empty Dict format
        $(assert.throws(
            East.value("{:  extra}").parse(DictType(StringType, IntegerType)),
            /Error occurred because expected '\}' after ':' in empty dict \(line 1, col 5\) while parsing value of type .*/
        ));

        // Test error on struct with wrong field name
        $(assert.throws(
            East.value("(wrong = 42)").parse(StructType({ expected: IntegerType })),
            /Error occurred because unknown field 'wrong', expected one of: expected \(line 1, col 2\) while parsing value of type .*/
        ));

        // Test error on missing equals after struct field name
        $(assert.throws(
            East.value("(x 42)").parse(StructType({ x: IntegerType })),
            /Error occurred because expected '=' after field name 'x' \(line 1, col 4\) while parsing value of type .*/
        ));

        // Test error on unexpected end of input in struct
        $(assert.throws(
            East.value("(x = 1").parse(StructType({ x: IntegerType, y: IntegerType })),
            /Error occurred because unexpected end of input in struct \(line 1, col 7\) while parsing value of type .*/
        ));

        // Test error on missing comma or closing paren in struct
        $(assert.throws(
            East.value("(x = 1 y = 2)").parse(StructType({ x: IntegerType, y: IntegerType })),
            /Error occurred because expected ',\' or '\)' after struct field \(line 1, col 8\) while parsing value of type .*/
        ));

        // Test error on variant with whitespace after dot
        $(assert.throws(
            East.value(". some 42").parse(VariantType({ some: IntegerType })),
            /Error occurred because whitespace not allowed between '\.' and case identifier \(line 1, col 2\) while parsing value of type .*/
        ));

        // Test error on float with missing exponent digits
        $(assert.throws(
            East.value("1.5e").parse(FloatType),
            /Error occurred because expected digits in float exponent \(line 1, col 5\) while parsing value of type "\.Float"/
        ));

        // Test error on DateTime with invalid format
        $(assert.throws(
            East.value("invalid-date").parse(DateTimeType),
            /Error occurred because expected DateTime in format YYYY-MM-DDTHH:MM:SS\.sss \(line 1, col 1\) while parsing value of type "\.DateTime"/
        ));

        // Test error on invalid DateTime value
        $(assert.throws(
            East.value("2022-13-40T25:61:61.999").parse(DateTimeType),
            /Error occurred because invalid DateTime value, got "2022-13-40T25:61:61.999" \(line 1, col 1\) while parsing value of type "\.DateTime"/
        ));

        // Test error on Blob with odd number of hex digits
        $(assert.throws(
            East.value("0x123").parse(BlobType),
            /Error occurred because invalid hex string \(odd length\), got "0x123" \(line 1, col 1\) while parsing value of type "\.Blob"/
        ));

        // Test error on Blob not starting with 0x
        $(assert.throws(
            East.value("123456").parse(BlobType),
            /Error occurred because expected Blob starting with 0x \(line 1, col 1\) while parsing value of type "\.Blob"/
        ));

        // Test error on array without opening bracket
        $(assert.throws(
            East.value("1, 2, 3]").parse(ArrayType(IntegerType)),
            /Error occurred because expected '\[' to start array \(line 1, col 1\) while parsing value of type "\.Array \.Integer"/
        ));

        // Test error on missing comma or closing bracket in array
        $(assert.throws(
            East.value("[1 2]").parse(ArrayType(IntegerType)),
            /Error occurred because expected ',\' or '\]' after array element \(line 1, col 4\) while parsing value of type "\.Array \.Integer"/
        ));

        // Test error on set without opening brace
        $(assert.throws(
            East.value("\"a\", \"b\"}").parse(SetType(StringType)),
            /Error occurred because expected '\{' to start set \(line 1, col 1\) while parsing value of type "\.Set \.String"/
        ));

        // Test error on missing comma or closing brace in set
        $(assert.throws(
            East.value("{\"a\" \"b\"}").parse(SetType(StringType)),
            /Error occurred because expected ',\' or '\}' after set element \(line 1, col 6\) while parsing value of type "\.Set \.String"/
        ));

        // Test error on dict without opening brace
        $(assert.throws(
            East.value("\"a\": 1}").parse(DictType(StringType, IntegerType)),
            /Error occurred because expected '\{' to start dict \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error on missing colon in dict entry
        $(assert.throws(
            East.value("{\"a\" 1}").parse(DictType(StringType, IntegerType)),
            /Error occurred because expected ':' after dict key at entry 0 \(line 1, col 6\) while parsing value of type .*/
        ));

        // Test error on missing comma or closing brace in dict
        $(assert.throws(
            East.value("{\"a\": 1 \"b\": 2}").parse(DictType(StringType, IntegerType)),
            /Error occurred because expected ',\' or '\}' after dict entry \(line 1, col 9\) while parsing value of type .*/
        ));

        // Test error on struct without opening paren
        $(assert.throws(
            East.value("x: 42)").parse(StructType({ x: IntegerType })),
            /Error occurred because expected '\(' to start struct \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error on variant without dot
        $(assert.throws(
            East.value("some 42").parse(VariantType({ some: IntegerType })),
            /Error occurred because expected '\.' to start variant case \(line 1, col 1\) while parsing value of type .*/
        ));

        // Test error for deeply nested structure - array of structs with error in second element
        $(assert.throws(
            East.value("[(id = 1, name = \"Alice\"), (id = true, name = \"Bob\")]").parse(ArrayType(StructType({ id: IntegerType, name: StringType }))),
            /Error occurred because expected integer, got 't' at \[1\]\.id \(line 1, col 34\) while parsing value of type .*/
        ));

        // Test error for dict with array values - error in array element
        $(assert.throws(
            East.value("{\"nums\": [1, 2, true]}").parse(DictType(StringType, ArrayType(IntegerType))),
            /Error occurred because expected integer, got 't' at \[\"nums\"\]\[2\] \(line 1, col 17\) while parsing value of type .*/
        ));

        // Test error for struct containing variant with error
        $(assert.throws(
            East.value("(result = .ok true)").parse(StructType({ result: VariantType({ ok: IntegerType, error: StringType }) })),
            /Error occurred because expected integer, got 't' at \.result\.ok \(line 1, col 15\) while parsing value of type .*/
        ));
    });

    test("Comparison method aliases", $ => {
        // Test short aliases (eq, ne, gt, lt, gte, lte, ge, le)
        $(assert.equal(East.value("hello").eq("hello"), true));
        $(assert.equal(East.value("hello").eq("world"), false));
        $(assert.equal(East.value("hello").ne("world"), true));
        $(assert.equal(East.value("hello").ne("hello"), false));
        $(assert.equal(East.value("world").gt("hello"), true));
        $(assert.equal(East.value("hello").gt("world"), false));
        $(assert.equal(East.value("hello").lt("world"), true));
        $(assert.equal(East.value("world").lt("hello"), false));
        $(assert.equal(East.value("hello").gte("hello"), true));
        $(assert.equal(East.value("world").gte("hello"), true));
        $(assert.equal(East.value("hello").lte("world"), true));
        $(assert.equal(East.value("world").ge("hello"), true));
        $(assert.equal(East.value("hello").le("world"), true));

        // Test medium aliases (equal, notEqual, greater, less, greaterEqual, lessEqual)
        $(assert.equal(East.value("hello").equal("hello"), true));
        $(assert.equal(East.value("hello").notEqual("world"), true));
        $(assert.equal(East.value("world").greater("hello"), true));
        $(assert.equal(East.value("hello").less("world"), true));
        $(assert.equal(East.value("hello").greaterEqual("hello"), true));
        $(assert.equal(East.value("hello").lessEqual("world"), true));
    });
});
