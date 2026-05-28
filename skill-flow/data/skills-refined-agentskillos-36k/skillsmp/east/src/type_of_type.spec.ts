/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { isDataTypeValue, toEastTypeValue } from "./type_of_type.js";
import {
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
    RefType,
    FunctionType,
    AsyncFunctionType,
    RecursiveType,
} from "./types.js";

describe("isDataTypeValue", () => {
    describe("primitive types", () => {
        it("returns true for Null", () => {
            assert.equal(isDataTypeValue(toEastTypeValue(NullType)), true);
        });

        it("returns true for Boolean", () => {
            assert.equal(isDataTypeValue(toEastTypeValue(BooleanType)), true);
        });

        it("returns true for Integer", () => {
            assert.equal(isDataTypeValue(toEastTypeValue(IntegerType)), true);
        });

        it("returns true for Float", () => {
            assert.equal(isDataTypeValue(toEastTypeValue(FloatType)), true);
        });

        it("returns true for String", () => {
            assert.equal(isDataTypeValue(toEastTypeValue(StringType)), true);
        });

        it("returns true for DateTime", () => {
            assert.equal(isDataTypeValue(toEastTypeValue(DateTimeType)), true);
        });

        it("returns true for Blob", () => {
            assert.equal(isDataTypeValue(toEastTypeValue(BlobType)), true);
        });
    });

    describe("function types", () => {
        it("returns false for Function", () => {
            const fnType = FunctionType([IntegerType], IntegerType);
            assert.equal(isDataTypeValue(toEastTypeValue(fnType)), false);
        });

        it("returns false for AsyncFunction", () => {
            const asyncFnType = AsyncFunctionType([StringType], BooleanType);
            assert.equal(isDataTypeValue(toEastTypeValue(asyncFnType)), false);
        });

        it("returns false for Function with no args", () => {
            const fnType = FunctionType([], NullType);
            assert.equal(isDataTypeValue(toEastTypeValue(fnType)), false);
        });
    });

    describe("container types with data", () => {
        it("returns true for Array of Integer", () => {
            const arrType = ArrayType(IntegerType);
            assert.equal(isDataTypeValue(toEastTypeValue(arrType)), true);
        });

        it("returns true for Set of String", () => {
            const setType = SetType(StringType);
            assert.equal(isDataTypeValue(toEastTypeValue(setType)), true);
        });

        it("returns true for Dict of String to Integer", () => {
            const dictType = DictType(StringType, IntegerType);
            assert.equal(isDataTypeValue(toEastTypeValue(dictType)), true);
        });

        it("returns true for Ref of Integer", () => {
            const refType = RefType(IntegerType);
            assert.equal(isDataTypeValue(toEastTypeValue(refType)), true);
        });

        it("returns true for nested Array of Array of Integer", () => {
            const nestedArr = ArrayType(ArrayType(IntegerType));
            assert.equal(isDataTypeValue(toEastTypeValue(nestedArr)), true);
        });
    });

    describe("container types with functions", () => {
        it("returns false for Array of Function", () => {
            const arrType = ArrayType(FunctionType([IntegerType], IntegerType));
            assert.equal(isDataTypeValue(toEastTypeValue(arrType)), false);
        });

        it("returns false for Dict with Function values", () => {
            const dictType = DictType(StringType, FunctionType([], NullType));
            assert.equal(isDataTypeValue(toEastTypeValue(dictType)), false);
        });

        it("returns false for Ref of Function", () => {
            const refType = RefType(FunctionType([IntegerType], IntegerType));
            assert.equal(isDataTypeValue(toEastTypeValue(refType)), false);
        });
    });

    describe("struct types", () => {
        it("returns true for Struct with data fields", () => {
            const structType = StructType({
                name: StringType,
                age: IntegerType,
                active: BooleanType,
            });
            assert.equal(isDataTypeValue(toEastTypeValue(structType)), true);
        });

        it("returns false for Struct with function field", () => {
            const structType = StructType({
                name: StringType,
                callback: FunctionType([StringType], NullType),
            });
            assert.equal(isDataTypeValue(toEastTypeValue(structType)), false);
        });

        it("returns false for Struct with nested function", () => {
            const structType = StructType({
                name: StringType,
                handlers: ArrayType(FunctionType([], NullType)),
            });
            assert.equal(isDataTypeValue(toEastTypeValue(structType)), false);
        });

        it("returns true for nested Struct with data", () => {
            const structType = StructType({
                person: StructType({
                    name: StringType,
                    age: IntegerType,
                }),
                active: BooleanType,
            });
            assert.equal(isDataTypeValue(toEastTypeValue(structType)), true);
        });
    });

    describe("variant types", () => {
        it("returns true for Variant with data cases", () => {
            const variantType = VariantType({
                None: NullType,
                Some: IntegerType,
            });
            assert.equal(isDataTypeValue(toEastTypeValue(variantType)), true);
        });

        it("returns false for Variant with function case", () => {
            const variantType = VariantType({
                Value: IntegerType,
                Callback: FunctionType([IntegerType], IntegerType),
            });
            assert.equal(isDataTypeValue(toEastTypeValue(variantType)), false);
        });

        it("returns false for Variant with nested function", () => {
            const variantType = VariantType({
                Data: StructType({ fn: FunctionType([], NullType) }),
                Empty: NullType,
            });
            assert.equal(isDataTypeValue(toEastTypeValue(variantType)), false);
        });
    });

    describe("recursive types", () => {
        it("returns true for recursive linked list of Integer", () => {
            // LinkedList = Recursive(T => Variant({ Nil: Null, Cons: Struct({ head: Integer, tail: T }) }))
            const linkedListType = RecursiveType(T =>
                VariantType({
                    Nil: NullType,
                    Cons: StructType({
                        head: IntegerType,
                        tail: T,
                    }),
                })
            );
            assert.equal(isDataTypeValue(toEastTypeValue(linkedListType)), true);
        });

        it("returns true for recursive binary tree of Integer", () => {
            // Tree = Recursive(T => Variant({ Leaf: Integer, Node: Struct({ left: T, right: T }) }))
            const treeType = RecursiveType(T =>
                VariantType({
                    Leaf: IntegerType,
                    Node: StructType({
                        left: T,
                        right: T,
                    }),
                })
            );
            assert.equal(isDataTypeValue(toEastTypeValue(treeType)), true);
        });

        it("returns false for recursive type with function", () => {
            // BadList = Recursive(T => Struct({ value: Integer, next: T, callback: Function }))
            const badListType = RecursiveType(T =>
                StructType({
                    value: IntegerType,
                    next: T,
                    callback: FunctionType([IntegerType], NullType),
                })
            );
            assert.equal(isDataTypeValue(toEastTypeValue(badListType)), false);
        });

        it("returns false for recursive type where function appears after recursive ref", () => {
            // Ensures we don't short-circuit on Recursive and miss the function
            const badType = RecursiveType(T =>
                StructType({
                    selfRef: T,  // This comes first
                    fn: FunctionType([], NullType),  // Function comes after
                })
            );
            assert.equal(isDataTypeValue(toEastTypeValue(badType)), false);
        });

        it("returns true for recursive type with Ref", () => {
            // RefList = Recursive(T => Variant({ Nil: Null, Cons: Struct({ head: Integer, tail: Ref(T) }) }))
            const refListType = RecursiveType(T =>
                VariantType({
                    Nil: NullType,
                    Cons: StructType({
                        head: IntegerType,
                        tail: RefType(T),
                    }),
                })
            );
            assert.equal(isDataTypeValue(toEastTypeValue(refListType)), true);
        });

        it("returns false for recursive type with function inside Ref", () => {
            const badRefType = RecursiveType(T =>
                StructType({
                    value: IntegerType,
                    next: RefType(T),
                    handler: RefType(FunctionType([IntegerType], NullType)),
                })
            );
            assert.equal(isDataTypeValue(toEastTypeValue(badRefType)), false);
        });
    });

    describe("complex nested types", () => {
        it("returns true for deeply nested data type", () => {
            const complexType = ArrayType(
                DictType(
                    StringType,
                    StructType({
                        items: ArrayType(
                            VariantType({
                                None: NullType,
                                Some: IntegerType,
                            })
                        ),
                    })
                )
            );
            assert.equal(isDataTypeValue(toEastTypeValue(complexType)), true);
        });

        it("returns false for deeply nested type with function", () => {
            const complexType = ArrayType(
                DictType(
                    StringType,
                    StructType({
                        items: ArrayType(
                            VariantType({
                                None: NullType,
                                Handler: FunctionType([StringType], NullType),
                            })
                        ),
                    })
                )
            );
            assert.equal(isDataTypeValue(toEastTypeValue(complexType)), false);
        });
    });
});
