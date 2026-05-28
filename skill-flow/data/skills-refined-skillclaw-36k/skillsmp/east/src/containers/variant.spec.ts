/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import assert from "node:assert";
import { variant, variant_symbol, match, none, some } from "./variant.js";

describe("variant function", () => {
    test("should create a variant with type and value", () => {
        const v = variant("success", 42);
        assert.strictEqual(v.type, "success");
        assert.strictEqual(v.value, 42);
        assert.strictEqual(v[variant_symbol], null);
    });

    test("should create variant with null value", () => {
        const v = variant("empty", null);
        assert.strictEqual(v.type, "empty");
        assert.strictEqual(v.value, null);
    });

    test("should create variant with object value", () => {
        const obj = { x: 1, y: 2 };
        const v = variant("point", obj);
        assert.strictEqual(v.type, "point");
        assert.deepStrictEqual(v.value, obj);
    });

    test("should create variant with array value", () => {
        const arr = [1, 2, 3];
        const v = variant("list", arr);
        assert.strictEqual(v.type, "list");
        assert.deepStrictEqual(v.value, arr);
    });
});

describe("match function", () => {
    test("should match on variant type and call corresponding function", () => {
        const v = variant("success", 42);
        const result = match(v, {
            success: (value: number) => value * 2,
            error: (_value: any) => -1,
        });
        assert.strictEqual(result, 84);
    });

    test("should match on different variant type", () => {
        const v = variant("error", "Something went wrong");
        const result = match(v, {
            success: (value: any) => value,
            error: (msg: string) => `Error: ${msg}`,
        });
        assert.strictEqual(result, "Error: Something went wrong");
    });

    test("should return default value when type not in handlers", () => {
        const v = variant("unknown", 123);
        const result = match(v, {
            unknown: (value: number) => value,
        } as any, "default");
        assert.strictEqual(result, 123);
    });

    test("should return default value when handler missing", () => {
        const v = variant("missing", 456);
        const result = match(v, {} as any, "default");
        assert.strictEqual(result, "default");
    });

    test("should handle variant with null value", () => {
        const v = variant("none", null);
        const result = match(v, {
            none: () => "nothing",
            some: (value: any) => `value: ${value}`,
        });
        assert.strictEqual(result, "nothing");
    });

    test("should pass correct value to handler", () => {
        const v = variant("data", { x: 10, y: 20 });
        const result = match(v, {
            data: (obj) => obj.x + obj.y,
        });
        assert.strictEqual(result, 30);
    });

    test("should handle multiple variant types", () => {
        const variants = [
            variant("a", 1),
            variant("b", 2),
            variant("c", 3),
        ];

        const results = variants.map(v => match(v, {
            a: (val) => val * 10,
            b: (val) => val * 20,
            c: (val) => val * 30,
        }));

        assert.deepStrictEqual(results, [10, 40, 90]);
    });
});

describe("none constant", () => {
    test("should be a variant with type 'none' and value null", () => {
        assert.strictEqual(none.type, "none");
        assert.strictEqual(none.value, null);
        assert.strictEqual(none[variant_symbol], null);
    });
});

describe("some function", () => {
    test("should create a variant with type 'some' and given value", () => {
        const v = some(42);
        assert.strictEqual(v.type, "some");
        assert.strictEqual(v.value, 42);
        assert.strictEqual(v[variant_symbol], null);
    });

    test("should create some with string value", () => {
        const v = some("hello");
        assert.strictEqual(v.type, "some");
        assert.strictEqual(v.value, "hello");
    });

    test("should create some with object value", () => {
        const obj = { data: 123 };
        const v = some(obj);
        assert.strictEqual(v.type, "some");
        assert.deepStrictEqual(v.value, obj);
    });

    test("should create some with null value", () => {
        const v = some(null);
        assert.strictEqual(v.type, "some");
        assert.strictEqual(v.value, null);
    });
});

describe("option type usage", () => {
    test("should work with none in match", () => {
        const result = match(none, {
            none: () => "no value",
            some: (val: any) => `value: ${val}`,
        });
        assert.strictEqual(result, "no value");
    });

    test("should work with some in match", () => {
        const result = match(some(100), {
            none: () => "no value",
            some: (val: number) => `value: ${val}`,
        });
        assert.strictEqual(result, "value: 100");
    });

    test("should handle option type pattern", () => {
        function getLength(opt: typeof none | ReturnType<typeof some<string>>): number {
            return match(opt, {
                none: () => 0,
                some: (str) => str.length,
            });
        }

        assert.strictEqual(getLength(none), 0);
        assert.strictEqual(getLength(some("hello")), 5);
    });
});

describe("variant_symbol", () => {
    test("should be a unique symbol", () => {
        assert.strictEqual(typeof variant_symbol, "symbol");
    });

    test("should be used as a brand on variant objects", () => {
        const v = variant("test", 123);
        assert.ok(variant_symbol in v);
        assert.strictEqual(v[variant_symbol], null);
    });

    test("should distinguish variant objects from regular objects", () => {
        const v = variant("test", 123);
        const regular = { type: "test", value: 123 };

        assert.ok(variant_symbol in v);
        assert.ok(!(variant_symbol in regular));
    });
});

describe("edge cases and advanced usage", () => {
    test("should handle variant with function value", () => {
        const fn = () => 42;
        const v = variant("func", fn);
        assert.strictEqual(v.type, "func");
        assert.strictEqual(v.value, fn);
        assert.strictEqual(v.value(), 42);
    });

    test("should handle variant with symbol value", () => {
        const sym = Symbol("test");
        const v = variant("symbol", sym);
        assert.strictEqual(v.type, "symbol");
        assert.strictEqual(v.value, sym);
    });

    test("should handle nested variants", () => {
        const inner = variant("inner", 42);
        const outer = variant("outer", inner);

        const result = match(outer, {
            outer: (innerVariant) => match(innerVariant, {
                inner: (val) => val * 2,
            }),
        });

        assert.strictEqual(result, 84);
    });

    test("match should work with empty string type", () => {
        const v = variant("", "empty type");
        const result = match(v, {
            "": (val) => `Got: ${val}`,
        });
        assert.strictEqual(result, "Got: empty type");
    });

    test("match should handle handler returning undefined", () => {
        const v = variant("test", 123);
        const result = match(v, {
            test: () => undefined,
        });
        assert.strictEqual(result, undefined);
    });

    test("match should preserve handler return type", () => {
        const v = variant("num", 42);
        const result = match(v, {
            num: (val) => ({ doubled: val * 2 }),
        });
        assert.deepStrictEqual(result, { doubled: 84 });
    });

    test("should handle variant with bigint value", () => {
        const v = variant("big", 9007199254740991n);
        const result = match(v, {
            big: (val) => val + 1n,
        });
        assert.strictEqual(result, 9007199254740992n);
    });
});
