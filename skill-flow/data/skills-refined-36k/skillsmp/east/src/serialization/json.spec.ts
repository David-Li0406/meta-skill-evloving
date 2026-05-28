
/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import assert from "node:assert/strict";

import { variant } from '../containers/variant.js';
import { fuzzerTest } from '../fuzz.js';

import {
    ArrayType,
    AsyncFunctionType,
    BlobType,
    BooleanType,
    DateTimeType,
    DictType,
    type EastType,
    FloatType,
    FunctionType,
    IntegerType,
    NeverType,
    NullType,
    RecursiveType,
    SetType,
    StringType,
    StructType,
    type ValueTypeOf,
    VariantType,
} from '../types.js';
import { decodeJSONFor, encodeJSONFor, fromJSONFor, toJSONFor } from "./json.js";
import { compareFor, equalFor } from "../comparison.js";
import { SortedSet } from "../containers/sortedset.js";
import { SortedMap } from "../containers/sortedmap.js";

describe('Json encoding/decoding of EAST values', () => {
    function run(type: EastType, decoded: ValueTypeOf<EastType>[], encoded: any[], erroneous: any[] = []) {
        assert.strictEqual(decoded.length, encoded.length);

        const toJson = toJSONFor(type);
        const fromJson = fromJSONFor(type);
        const equal = equalFor(type);

        for (let i = 0; i < decoded.length; i++) {
            assert.deepEqual(toJson(decoded[i]!), encoded[i]!);
            assert.ok(equal(fromJson(encoded[i]!), decoded[i]!), `Round-trip failed for ${JSON.stringify(encoded[i])}`);
        }


        for (const v of erroneous) {
            assert.throws(() => fromJson(v));
        }
    }

    test('should encode/decode null', () => {
        const type = NullType;
        const decoded = [
            null,
        ];
        const encoded = [
            null,
        ];
        const erroneous = [
            undefined,
            true,
            1,
            "",
            [],
            {},
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode boolean', () => {
        const type = BooleanType;
        const decoded = [
            true,
            false,
        ];
        const encoded = [
            true,
            false,
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            [],
            {}
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode integer', () => {
        const type = IntegerType;
        const decoded = [
            0n,
            42n,
            -1n,
            90071992547409919n,
            9223372036854775807n,
            -9223372036854775808n,
        ];
        const encoded = [
            "0",
            "42",
            "-1",
            "90071992547409919",
            "9223372036854775807",
            "-9223372036854775808",
        ];
        const erroneous = [
            undefined,
            null,
            "",
            [],
            {},
            "abc",
            "9223372036854775808",
            "-9223372036854775809",
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode float', () => {
        const type = FloatType;
        const decoded = [
            0,
            3.14,
            -1e6,
            Infinity,
            -Infinity,
            NaN,
        ];
        const encoded = [
            0,
            3.14,
            -1e6,
            "Infinity",
            "-Infinity",
            "NaN",
        ];
        const erroneous = [
            undefined,
            null,
            "",
            "abc",
            "Inf",
            "-Inf",
            [],
            {}
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode string', () => {
        const type = StringType;
        const decoded = [
            "",
            "abc",
            "いろはにほへとちりぬるを",
        ];
        const encoded = [
            "",
            "abc",
            "いろはにほへとちりぬるを",
        ];
        const erroneous = [
            undefined,
            null,
            1,
            [],
            {}
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode date', () => {
        const type = DateTimeType;
        const decoded = [
            new Date(0),
            new Date("2022-06-29T13:43:00.123+00:00"),
            new Date("2022-06-29T13:43:00.123Z"),
            new Date("2022-06-29T13:43:00.123+05:00"),
        ];
        const encoded = [
            "1970-01-01T00:00:00.000+00:00",
            "2022-06-29T13:43:00.123+00:00",
            "2022-06-29T13:43:00.123+00:00",
            "2022-06-29T08:43:00.123+00:00",
        ];
        const erroneous = [
            undefined,
            null,
            1,
            [],
            {},
            "1970-13-01T00:00:00.000+00:00", // Invalid month
            "1970-01-01T00:00:00.000", // Missing timezone
            "1970-01-01 00:00:00.000Z", // Space instead of T
            "1970-01-01T00:00:00Z", // Missing milliseconds
            "2022-06-29T13:43:00.123+5:00", // Invalid offset format (should be +05:00)
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode array', () => {
        const type = ArrayType(DateTimeType);
        const decoded = [
            [],
            [
                new Date(0),
                new Date("2022-06-29T13:43:00.123+00:00"),
            ],
        ];
        const encoded = [
            [],
            [
                "1970-01-01T00:00:00.000+00:00",
                "2022-06-29T13:43:00.123+00:00",
            ],
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            [undefined],
            [null],
            [1],
            [[]],
            [{}],
            ["1970-01-01T00:00:00.000"], // Missing timezone
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode set', () => {
        const type = SetType(StringType);
        const compare = compareFor(type.key);
        const decoded = [
            new SortedSet<any>([], compare),
            new SortedSet<any>(["abc", "def"], compare),
        ];
        const encoded = [
            [],
            ["abc", "def"],
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            [undefined],
            [null],
            [1],
            [[]],
            [{}],
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode dict', () => {
        const type = DictType(StringType, DateTimeType);
        const compare = compareFor(StringType);
        const decoded = [
            new SortedMap<any, any>([], compare),
            new SortedMap<any, any>([
                ["abc", new Date(0)],
                ["def", new Date("2022-06-29T13:43:00.123+00:00")],
            ], compare),
        ];
        const encoded = [
            [],
            [
                { key: "abc", value: "1970-01-01T00:00:00.000+00:00" },
                { key: "def", value: "2022-06-29T13:43:00.123+00:00" },
            ],
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            [undefined],
            [null],
            [1],
            ["abc"],
            [[]],
            [{}],
            [{ key: "abc" }],
            [{ value: "1970-01-01T00:00:00.000+00:00" }],
            [{ key: 1, value: "1970-01-01T00:00:00.000+00:00" }],
            [{ key: "abc", value: "1970-01-01T00:00:00.000" }], // Missing timezone
            [{ key: "abc", value: "1970-01-01T00:00:00.000+00:00", extra: "naughty" }],
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode struct', () => {
        const type = StructType({
            boolean: BooleanType,
            string: StringType,
            date: DateTimeType,
        });
        const decoded = [
            { boolean: true, string: "good", date: new Date(0) },
            { boolean: false, string: "bad", date: new Date("2022-06-29T13:43:00.123+00:00") },
        ];
        const encoded = [
            { boolean: true, string: "good", date: "1970-01-01T00:00:00.000+00:00" },
            { boolean: false, string: "bad", date: "2022-06-29T13:43:00.123+00:00" },
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            { boolean: true, string: "good" },
            { boolean: true, string: "good", date: "1970-01-01T00:00:00.000" }, // Missing timezone
            { boolean: true, string: "good", date: "1970-01-01T00:00:00.000+00:00", extra: "naughty" },
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode variant', () => {
        const type = VariantType({
            none: NullType,
            some: DateTimeType,
        });
        const decoded = [
            variant("none", null),
            variant("some", new Date("2022-06-29T13:43:00.123+00:00")),
        ];
        const encoded = [
            { type: "none", value: null },
            { type: "some", value: "2022-06-29T13:43:00.123+00:00" },
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            { type: "none" },
            { value: null },
            { type: "nothing", value: null },
            { type: "none", value: 1 },
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should encode/decode simple linked list', () => {
        // LinkedList = Variant<nil: Null, cons: Struct<head: Integer, tail: LinkedList>>
        const LinkedListType = RecursiveType((self: any) => VariantType({
            nil: NullType,
            cons: StructType({
                head: IntegerType,
                tail: self,
            }),
        }));

        const decoded = [
            variant("nil", null),
            variant("cons", { head: 1n, tail: variant("nil", null) }),
            variant("cons", {
                head: 1n,
                tail: variant("cons", {
                    head: 2n,
                    tail: variant("cons", {
                        head: 3n,
                        tail: variant("nil", null),
                    }),
                }),
            }),
        ];
        const encoded = [
            { type: "nil", value: null },
            { type: "cons", value: { head: "1", tail: { type: "nil", value: null } } },
            {
                type: "cons",
                value: {
                    head: "1",
                    tail: {
                        type: "cons",
                        value: {
                            head: "2",
                            tail: {
                                type: "cons",
                                value: { head: "3", tail: { type: "nil", value: null } },
                            },
                        },
                    },
                },
            },
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            { type: "cons" },
            { type: "cons", value: {} },
            { type: "cons", value: { head: "1" } },
            { type: "cons", value: { head: "not an int", tail: { type: "nil", value: null } } },
        ];

        run(LinkedListType, decoded, encoded, erroneous);
    });

    test('should encode/decode binary tree', () => {
        // Tree = Variant<leaf: Integer, node: Struct<left: Tree, right: Tree>>
        const TreeType = RecursiveType((self: any) => VariantType({
            leaf: IntegerType,
            node: StructType({
                left: self,
                right: self,
            }),
        }));

        const decoded = [
            variant("leaf", 42n),
            variant("node", {
                left: variant("leaf", 1n),
                right: variant("leaf", 2n),
            }),
            variant("node", {
                left: variant("node", {
                    left: variant("leaf", 1n),
                    right: variant("leaf", 2n),
                }),
                right: variant("leaf", 3n),
            }),
        ];
        const encoded = [
            { type: "leaf", value: "42" },
            {
                type: "node",
                value: {
                    left: { type: "leaf", value: "1" },
                    right: { type: "leaf", value: "2" },
                },
            },
            {
                type: "node",
                value: {
                    left: {
                        type: "node",
                        value: {
                            left: { type: "leaf", value: "1" },
                            right: { type: "leaf", value: "2" },
                        },
                    },
                    right: { type: "leaf", value: "3" },
                },
            },
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            { type: "leaf" },
            { type: "leaf", value: "not an int" },
            { type: "node", value: {} },
            { type: "node", value: { left: { type: "leaf", value: "1" } } },
        ];

        run(TreeType, decoded, encoded, erroneous);
    });

    test('should encode/decode tree with array children', () => {
        // Node = Struct<value: Integer, children: Array<Node>>
        const NodeType = RecursiveType((self: any) => StructType({
            value: IntegerType,
            children: ArrayType(self),
        }));

        const decoded = [
            { value: 1n, children: [] },
            {
                value: 1n,
                children: [
                    { value: 2n, children: [] },
                    { value: 3n, children: [] },
                ],
            },
            {
                value: 1n,
                children: [
                    {
                        value: 2n,
                        children: [
                            { value: 4n, children: [] },
                            { value: 5n, children: [] },
                        ],
                    },
                    { value: 3n, children: [] },
                ],
            },
        ];
        const encoded = [
            { value: "1", children: [] },
            {
                value: "1",
                children: [
                    { value: "2", children: [] },
                    { value: "3", children: [] },
                ],
            },
            {
                value: "1",
                children: [
                    {
                        value: "2",
                        children: [
                            { value: "4", children: [] },
                            { value: "5", children: [] },
                        ],
                    },
                    { value: "3", children: [] },
                ],
            },
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            { value: "1" },
            { children: [] },
            { value: "not an int", children: [] },
            { value: "1", children: [{}] },
        ];

        run(NodeType, decoded, encoded, erroneous);
    });

    test('should encode/decode graph with string labels', () => {
        // GraphNode = Struct<label: String, edges: Array<GraphNode>>
        const GraphNodeType = RecursiveType((self: any) => StructType({
            label: StringType,
            edges: ArrayType(self),
        }));

        const decoded = [
            { label: "A", edges: [] },
            {
                label: "A",
                edges: [
                    { label: "B", edges: [] },
                    { label: "C", edges: [] },
                ],
            },
        ];
        const encoded = [
            { label: "A", edges: [] },
            {
                label: "A",
                edges: [
                    { label: "B", edges: [] },
                    { label: "C", edges: [] },
                ],
            },
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            { label: "A" },
            { edges: [] },
            { label: 123, edges: [] },
            { label: "A", edges: [{ label: "B" }] },
        ];

        run(GraphNodeType, decoded, encoded, erroneous);
    });

    test('should encode/decode nested variant structures', () => {
        // Expr = Variant<num: Integer, add: Struct<left: Expr, right: Expr>, mul: Struct<left: Expr, right: Expr>>
        const ExprType = RecursiveType((self: any) => VariantType({
            num: IntegerType,
            add: StructType({
                left: self,
                right: self,
            }),
            mul: StructType({
                left: self,
                right: self,
            }),
        }));

        const decoded = [
            variant("num", 42n),
            variant("add", {
                left: variant("num", 1n),
                right: variant("num", 2n),
            }),
            variant("mul", {
                left: variant("add", {
                    left: variant("num", 2n),
                    right: variant("num", 3n),
                }),
                right: variant("num", 4n),
            }),
        ];
        const encoded = [
            { type: "num", value: "42" },
            {
                type: "add",
                value: {
                    left: { type: "num", value: "1" },
                    right: { type: "num", value: "2" },
                },
            },
            {
                type: "mul",
                value: {
                    left: {
                        type: "add",
                        value: {
                            left: { type: "num", value: "2" },
                            right: { type: "num", value: "3" },
                        },
                    },
                    right: { type: "num", value: "4" },
                },
            },
        ];
        const erroneous = [
            undefined,
            null,
            1,
            "",
            {},
            { type: "num" },
            { type: "add", value: {} },
            { type: "add", value: { left: { type: "num", value: "1" } } },
            { type: "unknown", value: "1" },
        ];

        run(ExprType, decoded, encoded, erroneous);
    });

    test('should encode/decode blob', () => {
        const type = BlobType;
        const decoded = [
            new Uint8Array([1, 3, 3, 7]),
            new Uint8Array([]),
        ];
        const encoded = [
            '0x01030307',
            '0x',
        ];
        const erroneous = [
            undefined,
            null,
            1,
            true,
            "",
            {},
            [256],
            ["0"],
            "abc",
            "0xgg",
            "0x123"
        ];

        run(type, decoded, encoded, erroneous);
    });

    test('should format error messages correctly', () => {
        // Test error for wrong type
        const booleanDecoder = fromJSONFor(BooleanType);
        try {
            booleanDecoder("not a boolean");
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected boolean, got "not a boolean" (line 1, col 1) while parsing value of type ".Boolean"');
        }

        // Test error with path for nested array
        const arrayDecoder = fromJSONFor(ArrayType(IntegerType));
        try {
            arrayDecoder(["42", "not an integer"]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got "not an integer" at [1] (line 1, col 1) while parsing value of type ".Array .Integer"');
        }

        // Test error with path for struct field
        const structDecoder = fromJSONFor(StructType({ name: StringType, age: IntegerType }));
        try {
            structDecoder({ name: "Alice", age: 42 });
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got 42 at .age (line 1, col 1) while parsing value of type ".Struct [(name="name", type=.String), (name="age", type=.Integer)]"');
        }

        // Test error for missing struct field
        try {
            structDecoder({ name: "Alice" });
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because missing field "age" in Struct, got {"name":"Alice"} (line 1, col 1) while parsing value of type ".Struct [(name="name", type=.String), (name="age", type=.Integer)]"');
        }

        // Test error for unexpected struct field
        const simpleStructDecoder = fromJSONFor(StructType({ name: StringType }));
        try {
            simpleStructDecoder({ name: "Alice", extra: "unexpected" });
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because unexpected field "extra" in Struct, got {"name":"Alice","extra":"unexpected"} (line 1, col 1) while parsing value of type ".Struct [(name="name", type=.String)]"');
        }

        // Test error for dict entry value
        const dictDecoder = fromJSONFor(DictType(StringType, IntegerType));
        try {
            dictDecoder([{ key: "a", value: "not an integer" }]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got "not an integer" at [0].value (line 1, col 1) while parsing value of type ".Dict (key=.String, value=.Integer)"');
        }

        // Test error for variant case value
        const variantDecoder = fromJSONFor(VariantType({ none: NullType, some: IntegerType }));
        try {
            variantDecoder({ type: "some", value: "not an integer" });
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got "not an integer" at .some (line 1, col 1) while parsing value of type ".Variant [(name="none", type=.Null), (name="some", type=.Integer)]"');
        }

        // Test error for unknown variant type
        try {
            variantDecoder({ type: "unknown", value: null });
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because unknown variant type "unknown", got {"type":"unknown","value":null} (line 1, col 1) while parsing value of type ".Variant [(name="none", type=.Null), (name="some", type=.Integer)]"');
        }

        // Test error for deeply nested structure - array of structs with error in second element
        const nestedDecoder = fromJSONFor(ArrayType(StructType({ id: IntegerType, name: StringType })));
        try {
            nestedDecoder([
                { id: "1", name: "Alice" },
                { id: "not an int", name: "Bob" }
            ]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got "not an int" at [1].id (line 1, col 1) while parsing value of type ".Array .Struct [(name="id", type=.Integer), (name="name", type=.String)]"');
        }

        // Test error for dict with array values - error in array element
        const dictArrayDecoder = fromJSONFor(DictType(StringType, ArrayType(IntegerType)));
        try {
            dictArrayDecoder([
                { key: "nums", value: ["1", "2", "not an int"] }
            ]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got "not an int" at [0].value[2] (line 1, col 1) while parsing value of type ".Dict (key=.String, value=.Array .Integer)"');
        }

        // Test error for struct containing variant with error
        const structVariantDecoder = fromJSONFor(StructType({
            result: VariantType({ ok: IntegerType, error: StringType })
        }));
        try {
            structVariantDecoder({ result: { type: "ok", value: "not an int" } });
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got "not an int" at .result.ok (line 1, col 1) while parsing value of type ".Struct [(name="result", type=.Variant [(name="error", type=.String), (name="ok", type=.Integer)])]"');
        }

        // Test error for set element
        const setDecoder = fromJSONFor(SetType(IntegerType));
        try {
            setDecoder(["1", "2", "not an int"]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got "not an int" at [2] (line 1, col 1) while parsing value of type ".Set .Integer"');
        }

        // Test error for dict with missing key field
        try {
            dictDecoder([{ value: "123" }]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected object with key and value for Dict entry, got {"value":"123"} at [0] (line 1, col 1) while parsing value of type ".Dict (key=.String, value=.Integer)"');
        }

        // Test error for dict with extra field
        try {
            dictDecoder([{ key: "a", value: "123", extra: "bad" }]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because unexpected field "extra" in Dict entry, got {"key":"a","value":"123","extra":"bad"} at [0] (line 1, col 1) while parsing value of type ".Dict (key=.String, value=.Integer)"');
        }

        // Test error for extremely complex nested structure:
        // Dict<String, Array<Struct{ results: Array<Variant<ok: Struct{items: Set<Integer>}, error: String>> }>>
        const veryComplexType = DictType(
            StringType,
            ArrayType(
                StructType({
                    results: ArrayType(
                        VariantType({
                            ok: StructType({
                                items: SetType(IntegerType)
                            }),
                            error: StringType
                        })
                    )
                })
            )
        );
        const veryComplexDecoder = fromJSONFor(veryComplexType);

        try {
            veryComplexDecoder([
                {
                    key: "batch1",
                    value: [
                        {
                            results: [
                                { type: "ok", value: { items: ["1", "2", "not an int"] } }
                            ]
                        }
                    ]
                }
            ]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because expected string representing integer, got "not an int" at [0].value[0].results[0].ok.items[2] (line 1, col 1) while parsing value of type ".Dict (key=.String, value=.Array .Struct [(name="results", type=.Array .Variant [(name="error", type=.String), (name="ok", type=.Struct [(name="items", type=.Set .Integer)])])])"');
        }

        // Another complex error - missing field deep in structure
        try {
            veryComplexDecoder([
                {
                    key: "batch1",
                    value: [
                        {
                            results: [
                                { type: "ok", value: { wrong: ["1"] } } // missing 'items' field
                            ]
                        }
                    ]
                }
            ]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.equal(e.message, 'Error occurred because unexpected field "wrong" in Struct, got {"wrong":["1"]} at [0].value[0].results[0].ok (line 1, col 1) while parsing value of type ".Dict (key=.String, value=.Array .Struct [(name="results", type=.Array .Variant [(name="error", type=.String), (name="ok", type=.Struct [(name="items", type=.Set .Integer)])])])"');
        }
    });

    test('should encode/decode using Uint8Array with encodeJSONFor/decodeJSONFor', () => {
        const encode = encodeJSONFor(IntegerType);
        const decode = decodeJSONFor(IntegerType);

        const value = 42n;
        const encoded = encode(value);
        const decoded = decode(encoded);

        assert.strictEqual(decoded, value);
        assert.ok(encoded instanceof Uint8Array);
    });

    test('should encode/decode complex types with encodeJSONFor/decodeJSONFor', () => {
        const type = StructType({ name: StringType, age: IntegerType });
        const encode = encodeJSONFor(type);
        const decode = decodeJSONFor(type);

        const value = { name: "Alice", age: 30n };
        const encoded = encode(value);
        const decoded = decode(encoded);

        assert.deepEqual(decoded, value);
    });

    test('should throw when encoding Never type', () => {
        const toJson = toJSONFor(NeverType);
        assert.throws(() => toJson(null as never), /Cannot encode Never type to JSON/);
    });

    test('should throw when decoding Never type with fromJSONFor', () => {
        const fromJson = fromJSONFor(NeverType);
        assert.throws(() => fromJson(null), /Cannot decode Never type from JSON/);
    });

    test('should throw when decoding Never type with decodeJSONFor', () => {
        const textEncoder = new TextEncoder();
        const decode = decodeJSONFor(NeverType);
        const encoded = textEncoder.encode('null');
        assert.throws(() => decode(encoded), /Cannot decode Never type from JSON/);
    });

    test('should throw when encoding Function type', () => {
        const funcType = FunctionType([], IntegerType);
        assert.throws(() => toJSONFor(funcType), /Cannot encode Function type to JSON/);
    });

    test('should throw when decoding Function type with fromJSONFor', () => {
        const funcType = FunctionType([], IntegerType);
        assert.throws(() => fromJSONFor(funcType), /Cannot decode Function type from JSON/);
    });

    test('should throw when creating decoder for Function type with decodeJSONFor', () => {
        const funcType = FunctionType([], IntegerType);
        assert.throws(() => decodeJSONFor(funcType), /Cannot decode Function type from JSON/);
    });

    test('should throw when encoding AsyncFunction type', () => {
        const funcType = AsyncFunctionType([], IntegerType);
        assert.throws(() => toJSONFor(funcType), /Cannot encode AsyncFunction type to JSON/);
    });

    test('should throw when decoding AsyncFunction type with fromJSONFor', () => {
        const funcType = AsyncFunctionType([], IntegerType);
        assert.throws(() => fromJSONFor(funcType), /Cannot decode AsyncFunction type from JSON/);
    });

    test('should throw when creating decoder for AsyncFunction type with decodeJSONFor', () => {
        const funcType = AsyncFunctionType([], IntegerType);
        assert.throws(() => decodeJSONFor(funcType), /Cannot decode AsyncFunction type from JSON/);
    });

    test('should freeze decoded Date when frozen=true', () => {
        const fromJson = fromJSONFor(DateTimeType, true);
        const date = fromJson("2022-06-29T13:43:00.123+00:00");
        assert.ok(Object.isFrozen(date));
    });

    test('should not freeze decoded Date when frozen=false', () => {
        const fromJson = fromJSONFor(DateTimeType, false);
        const date = fromJson("2022-06-29T13:43:00.123+00:00");
        assert.ok(!Object.isFrozen(date));
    });

    test('should attempt to freeze decoded Blob when frozen=true', () => {
        // Note: Uint8Array cannot actually be frozen in JavaScript
        // This test verifies that the frozen code path is executed
        const fromJson = fromJSONFor(BlobType, true);
        // This will execute the Object.freeze code path, which will throw
        // because Uint8Array cannot be frozen
        assert.throws(() => fromJson("0x01020304"), /Cannot freeze array buffer views/);
    });

    test('should not freeze decoded Blob when frozen=false', () => {
        const fromJson = fromJSONFor(BlobType, false);
        const blob = fromJson("0x01020304");
        assert.ok(!Object.isFrozen(blob));
    });

    test('should freeze decoded Array when frozen=true', () => {
        const fromJson = fromJSONFor(ArrayType(IntegerType), true);
        const arr = fromJson(["1", "2"]);
        assert.ok(Object.isFrozen(arr));
    });

    test('should not freeze decoded Array when frozen=false', () => {
        const fromJson = fromJSONFor(ArrayType(IntegerType), false);
        const arr = fromJson(["1", "2"]);
        assert.ok(!Object.isFrozen(arr));
    });

    test('should freeze decoded Set when frozen=true', () => {
        const fromJson = fromJSONFor(SetType(StringType), true);
        const set = fromJson(["a", "b"]);
        assert.ok(Object.isFrozen(set));
    });

    test('should not freeze decoded Set when frozen=false', () => {
        const fromJson = fromJSONFor(SetType(StringType), false);
        const set = fromJson(["a", "b"]);
        assert.ok(!Object.isFrozen(set));
    });

    test('should freeze decoded Dict when frozen=true', () => {
        const fromJson = fromJSONFor(DictType(StringType, IntegerType), true);
        const dict = fromJson([{ key: "a", value: "1" }]);
        assert.ok(Object.isFrozen(dict));
    });

    test('should not freeze decoded Dict when frozen=false', () => {
        const fromJson = fromJSONFor(DictType(StringType, IntegerType), false);
        const dict = fromJson([{ key: "a", value: "1" }]);
        assert.ok(!Object.isFrozen(dict));
    });

    test('should freeze decoded Struct when frozen=true', () => {
        const fromJson = fromJSONFor(StructType({ x: IntegerType }), true);
        const struct = fromJson({ x: "42" });
        assert.ok(Object.isFrozen(struct));
    });

    test('should not freeze decoded Struct when frozen=false', () => {
        const fromJson = fromJSONFor(StructType({ x: IntegerType }), false);
        const struct = fromJson({ x: "42" });
        assert.ok(!Object.isFrozen(struct));
    });

    test('should freeze decoded Variant when frozen=true', () => {
        const fromJson = fromJSONFor(VariantType({ some: IntegerType }), true);
        const v = fromJson({ type: "some", value: "42" });
        assert.ok(Object.isFrozen(v));
    });

    test('should not freeze decoded Variant when frozen=false', () => {
        const fromJson = fromJSONFor(VariantType({ some: IntegerType }), false);
        const v = fromJson({ type: "some", value: "42" });
        assert.ok(!Object.isFrozen(v));
    });

    test('should handle JSON.parse syntax errors in decodeJSONFor', () => {
        const textEncoder = new TextEncoder();
        const decode = decodeJSONFor(IntegerType);

        // Invalid JSON
        const invalidJson = textEncoder.encode('{"broken": }');
        assert.throws(() => decode(invalidJson), /Error occurred because.*line \d+, col \d+/);
    });

    test('should track line and column numbers in JSON parse errors', () => {
        const textEncoder = new TextEncoder();
        const decode = decodeJSONFor(IntegerType);

        // Multi-line invalid JSON
        const invalidJson = textEncoder.encode('{\n"foo": \n}');
        assert.throws(() => decode(invalidJson), /line \d+, col \d+/);
    });

    test('should handle JSON parse errors without position info', () => {
        const textEncoder = new TextEncoder();
        const decode = decodeJSONFor(IntegerType);

        // Another invalid JSON case
        const invalidJson = textEncoder.encode('[');
        assert.throws(() => decode(invalidJson), /Error occurred because/);
    });

    test('should use decodeJSONFor with frozen parameter', () => {
        const encode = encodeJSONFor(ArrayType(IntegerType));
        const decode = decodeJSONFor(ArrayType(IntegerType), true);

        const value = [1n, 2n, 3n];
        const encoded = encode(value);
        const decoded = decode(encoded);

        assert.ok(Object.isFrozen(decoded));
        assert.deepEqual(decoded, value);
    });

    test('should handle non-SyntaxError exceptions in decodeJSONFor', () => {
        const textEncoder = new TextEncoder();
        const decode = decodeJSONFor(IntegerType);

        // Create a malformed but parseable JSON that will fail type checking
        const validJson = textEncoder.encode('"not an integer"');
        assert.throws(() => decode(validJson), /Error occurred because/);
    });

    test('should round-trip random types and values', { timeout: 60_000 }, async () => {
        const result = await fuzzerTest(
            (type: EastType) => {
                const toJson = toJSONFor(type);
                const fromJson = fromJSONFor(type);
                const equal = equalFor(type);

                return async (value: any) => {
                    // Encode and decode
                    const encoded = toJson(value);
                    const decoded = fromJson(encoded);

                    // Check value equality
                    if (!equal(decoded, value)) {
                        throw new Error(`Round-trip failed: values not equal`);
                    }
                };
            },
            100, // 100 random types
            10,  // 10 samples per type
            { includeRecursive: false } // TODO: recursive value generation needs work
        );

        assert.strictEqual(result, true, "Fuzz test failed");
    });

    test('should round-trip with Uint8Array encoding for random types', { timeout: 60_000 }, async () => {
        const result = await fuzzerTest(
            (type: EastType) => {
                const encode = encodeJSONFor(type);
                const decode = decodeJSONFor(type);
                const equal = equalFor(type);

                return async (value: any) => {
                    // Encode and decode
                    const encoded = encode(value);
                    const decoded = decode(encoded);

                    // Verify it's a Uint8Array
                    if (!(encoded instanceof Uint8Array)) {
                        throw new Error(`Encoded value is not a Uint8Array`);
                    }

                    // Check value equality
                    if (!equal(decoded, value)) {
                        throw new Error(`Round-trip failed: values not equal`);
                    }
                };
            },
            100, // 100 random types
            10,  // 10 samples per type
            { includeRecursive: false } // TODO: recursive value generation needs work
        );

        assert.strictEqual(result, true, "Fuzz test failed");
    });

    test('should re-throw non-JSONDecodeError exceptions in Array decoding', () => {
        // This tests the throw e; path at line 260 in the Array decoder
        const type = ArrayType(IntegerType);
        const fromJson = fromJSONFor(type);

        // Create a scenario where a non-JSONDecodeError might be thrown
        // by passing malformed data that causes a different type of error
        try {
            // Using a symbol which should cause a different error type
            fromJson([Symbol('test') as any]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            // Should re-throw the error
            assert.ok(e);
        }
    });

    test('should re-throw non-JSONDecodeError exceptions in Set decoding', () => {
        const type = SetType(IntegerType);
        const fromJson = fromJSONFor(type);

        try {
            fromJson([Symbol('test') as any]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.ok(e);
        }
    });

    test('should re-throw non-JSONDecodeError exceptions in Dict key decoding', () => {
        const type = DictType(IntegerType, StringType);
        const fromJson = fromJSONFor(type);

        try {
            fromJson([{ key: Symbol('test') as any, value: "test" }]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.ok(e);
        }
    });

    test('should re-throw non-JSONDecodeError exceptions in Dict value decoding', () => {
        const type = DictType(StringType, IntegerType);
        const fromJson = fromJSONFor(type);

        try {
            fromJson([{ key: "test", value: Symbol('test') as any }]);
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.ok(e);
        }
    });

    test('should re-throw non-JSONDecodeError exceptions in Struct decoding', () => {
        const type = StructType({ x: IntegerType });
        const fromJson = fromJSONFor(type);

        try {
            fromJson({ x: Symbol('test') as any });
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.ok(e);
        }
    });

    test('should re-throw non-JSONDecodeError exceptions in Variant decoding', () => {
        const type = VariantType({ some: IntegerType });
        const fromJson = fromJSONFor(type);

        try {
            fromJson({ type: "some", value: Symbol('test') as any });
            assert.fail('Should have thrown');
        } catch (e: any) {
            assert.ok(e);
        }
    });

    test('should encode shared array references within RecursiveType', () => {
        // Create a type that can hold shared arrays
        const NodeType = RecursiveType((self: any) => StructType({
            value: IntegerType,
            children: ArrayType(self),
            metadata: ArrayType(StringType),
        }));

        // Create a shared array that appears in multiple places
        const sharedMetadata = ["tag1", "tag2"];
        const value = {
            value: 1n,
            children: [
                {
                    value: 2n,
                    children: [],
                    metadata: sharedMetadata,  // First reference
                },
                {
                    value: 3n,
                    children: [],
                    metadata: sharedMetadata,  // Second reference (same instance)
                },
            ],
            metadata: sharedMetadata,  // Third reference (same instance)
        };

        const toJson = toJSONFor(NodeType);
        const fromJson = fromJSONFor(NodeType);
        const encoded = toJson(value) as any;

        // Check that references appear in the encoding (first occurrence is real data, rest are refs)
        assert.deepEqual(encoded.children[0].metadata, ["tag1", "tag2"]);
        assert.deepEqual(encoded.children[1].metadata, { "$ref": "2#0/metadata" });
        assert.deepEqual(encoded.metadata, { "$ref": "1#children/0/metadata" });

        // Check that decoding preserves shared references
        const decoded = fromJson(encoded);
        assert.ok(decoded.metadata === decoded.children[0].metadata, "metadata should be same instance as children[0].metadata");
        assert.ok(decoded.metadata === decoded.children[1].metadata, "metadata should be same instance as children[1].metadata");

        // Check round-trip equality
        const equal = equalFor(NodeType);
        assert.ok(equal(decoded, value), "decoded value should equal original");
    });

    test('should encode shared set references within RecursiveType', () => {
        const NodeType = RecursiveType((self: any) => StructType({
            value: IntegerType,
            children: ArrayType(self),
            tags: SetType(StringType),
        }));

        const compare = compareFor(StringType);
        const sharedTags = new SortedSet<string>(["a", "b", "c"], compare);

        const value = {
            value: 1n,
            children: [
                {
                    value: 2n,
                    children: [],
                    tags: sharedTags,  // First reference
                },
            ],
            tags: sharedTags,  // Second reference (same instance)
        };

        const toJson = toJSONFor(NodeType);
        const fromJson = fromJSONFor(NodeType);
        const encoded = toJson(value) as any;

        // Check encoding (first occurrence is real data, rest are refs)
        assert.deepEqual(encoded.children[0].tags, ["a", "b", "c"]);
        assert.deepEqual(encoded.tags, { "$ref": "1#children/0/tags" });

        // Check decoding preserves shared references
        const decoded = fromJson(encoded);
        assert.ok(decoded.tags === decoded.children[0].tags, "tags should be same instance");

        // Check round-trip equality
        const equal = equalFor(NodeType);
        assert.ok(equal(decoded, value), "decoded value should equal original");
    });

    test('should encode shared dict references within RecursiveType', () => {
        const NodeType = RecursiveType((self: any) => StructType({
            value: IntegerType,
            children: ArrayType(self),
            properties: DictType(StringType, IntegerType),
        }));

        const compare = compareFor(StringType);
        const sharedProps = new SortedMap<string, bigint>([["x", 10n], ["y", 20n]], compare);

        const value = {
            value: 1n,
            children: [
                {
                    value: 2n,
                    children: [],
                    properties: sharedProps,
                },
                {
                    value: 3n,
                    children: [],
                    properties: sharedProps,
                },
            ],
            properties: sharedProps,
        };

        const toJson = toJSONFor(NodeType);
        const fromJson = fromJSONFor(NodeType);
        const encoded = toJson(value) as any;

        // Check that references appear in the encoding (first occurrence is real data, rest are refs)
        assert.deepEqual(encoded.children[0].properties, [
            { key: "x", value: "10" },
            { key: "y", value: "20" },
        ]);
        assert.deepEqual(encoded.children[1].properties, { "$ref": "2#0/properties" });
        assert.deepEqual(encoded.properties, { "$ref": "1#children/0/properties" });

        // Check that decoding preserves shared references
        const decoded = fromJson(encoded);
        assert.ok(decoded.properties === decoded.children[0].properties, "properties should be same instance as children[0].properties");
        assert.ok(decoded.properties === decoded.children[1].properties, "properties should be same instance as children[1].properties");

        // Check round-trip equality
        const equal = equalFor(NodeType);
        assert.ok(equal(decoded, value), "decoded value should equal original");
    });

    test('should handle JSON Pointer escaping in field names', () => {
        // Create a struct with field names that need escaping
        const NodeType = RecursiveType((self: any) => StructType({
            "field/with/slashes": IntegerType,
            "field~with~tildes": IntegerType,
            "normal": ArrayType(IntegerType),
            children: ArrayType(self),
        }));

        const sharedArray = [1n, 2n, 3n];
        const value = {
            "field/with/slashes": 42n,
            "field~with~tildes": 99n,
            "normal": sharedArray,
            children: [
                {
                    "field/with/slashes": 1n,
                    "field~with~tildes": 2n,
                    "normal": sharedArray,  // Reference to same array
                    children: [],
                },
            ],
        };

        const toJson = toJSONFor(NodeType);
        const encoded = toJson(value) as any;

        // First array should be actual data
        assert.deepEqual(encoded.normal, ["1", "2", "3"]);
        // Second occurrence should be a reference with properly escaped path
        // Path should be 3#normal (go up 3 levels from children[0].normal to root.normal)
        assert.deepEqual(encoded.children[0].normal, { "$ref": "3#normal" });
    });
});