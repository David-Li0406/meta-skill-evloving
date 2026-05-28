/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import {
    East,
    IntegerType,
    NullType,
    StringType,
    DateTimeType,
    BlobType,
    FunctionType,
    AsyncFunctionType,
    StructType,
    OptionType,
    ArrayType,
    SetType,
    DictType,
    VariantType,
    RecursiveType,
    variant,
} from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Function", (test) => {
    test("simple function call returns correct result", $ => {
        const addOne = East.function([IntegerType], IntegerType, ($, x) => {
            return x.add(1n);
        });
        $(assert.equal(addOne(5n), 6n));
    });

    test("function with multiple arguments", $ => {
        const add = East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => {
            return a.add(b);
        });
        $(assert.equal(add(3n, 4n), 7n));
    });

    test("function with no arguments", $ => {
        const getFortyTwo = East.function([], IntegerType, _$ => {
            return 42n;
        });
        $(assert.equal(getFortyTwo(), 42n));
    });

    test("function returning null", $ => {
        const doNothing = East.function([], NullType, _$ => {
            return null;
        });
        $(assert.equal(doNothing(), null));
    });

    test("function stored in variable and called", $ => {
        const fn = $.const(East.function([IntegerType], IntegerType, ($, x) => {
            return x.multiply(2n);
        }));
        $(assert.equal(fn(10n), 20n));
    });

    test("function passed as argument to another function", $ => {
        const apply = East.function(
            [FunctionType([IntegerType], IntegerType), IntegerType],
            IntegerType,
            ($, f, x) => {
                return f(x);
            }
        );
        const double = East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n));
        $(assert.equal(apply(double, 5n), 10n));
    });

    test("function returned from another function", $ => {
        const makeAdder = East.function([IntegerType], FunctionType([IntegerType], IntegerType), ($, n) => {
            return East.function([IntegerType], IntegerType, ($, x) => x.add(n));
        });
        const addFive = makeAdder(5n);
        $(assert.equal(addFive(10n), 15n));
    });

    test("nested function calls", $ => {
        const square = East.function([IntegerType], IntegerType, ($, x) => x.multiply(x));
        const double = East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n));
        // double(square(3)) = double(9) = 18
        $(assert.equal(double(square(3n)), 18n));
    });

    test("function with early return", $ => {
        const absValue = East.function([IntegerType], IntegerType, ($, x) => {
            $.if(East.less(x, 0n), $ => {
                $.return(x.negate());
            });
            return x;
        });
        $(assert.equal(absValue(-5n), 5n));
        $(assert.equal(absValue(5n), 5n));
        $(assert.equal(absValue(0n), 0n));
    });

    test("function capturing outer variable (closure)", $ => {
        const multiplier = $.const(3n);
        const multiplyByThree = East.function([IntegerType], IntegerType, ($, x) => {
            return x.multiply(multiplier);
        });
        $(assert.equal(multiplyByThree(4n), 12n));
    });

    test("closure with captured variable used in loop", $ => {
        // This tests that closures work correctly when the captured variable
        // is accessed inside a ForArray loop
        const items = $.const([1n, 2n, 3n, 4n, 5n]);
        const target = $.const(10n);

        // Function captures items and target, uses them in a loop
        const sumAndCompare = East.function([ArrayType(IntegerType)], IntegerType, ($, selection) => {
            const sum = $.let(0n);
            $.for(selection, ($, idx) => {
                // Access captured 'items' array inside the loop using the index value
                $.assign(sum, sum.add(items.get(idx)));
            });
            // Compare sum to captured 'target'
            $.if(East.equal(sum, target), $ => {
                $.return(1n);  // Found match
            });
            return 0n;  // No match
        });

        // Selection [0, 3] means items[0] + items[3] = 1 + 4 = 5, not 10
        $(assert.equal(sumAndCompare([0n, 3n]), 0n));
        // Selection [1, 2, 4] means items[1] + items[2] + items[4] = 2 + 3 + 5 = 10
        $(assert.equal(sumAndCompare([1n, 2n, 4n]), 1n));
    });

    test("closure capturing multiple variables", $ => {
        const offset = $.const(100n);
        const multiplier = $.const(3n);
        const divisor = $.const(2n);

        // Function captures three variables
        const transform = East.function([IntegerType], IntegerType, ($, x) => {
            // (x * multiplier + offset) / divisor
            const scaled = $.let(x.multiply(multiplier));
            const shifted = $.let(scaled.add(offset));
            return shifted.divide(divisor);
        });

        // (10 * 3 + 100) / 2 = 130 / 2 = 65
        $(assert.equal(transform(10n), 65n));
        // (0 * 3 + 100) / 2 = 100 / 2 = 50
        $(assert.equal(transform(0n), 50n));
    });

    test("closure capturing array and iterating over it", $ => {
        const weights = $.const([2n, 3n, 5n, 7n]);

        // Function that computes weighted sum of input values
        const weightedSum = East.function([ArrayType(IntegerType)], IntegerType, ($, values) => {
            const sum = $.let(0n);
            $.for(values, ($, val, i) => {
                // Access captured 'weights' array using loop index
                const weight = $.let(weights.get(i));
                $.assign(sum, sum.add(val.multiply(weight)));
            });
            return sum;
        });

        // 1*2 + 2*3 + 3*5 + 4*7 = 2 + 6 + 15 + 28 = 51
        $(assert.equal(weightedSum([1n, 2n, 3n, 4n]), 51n));
    });

    test("closure used as callback in higher-order function", $ => {
        const factor = $.const(3n);

        // Higher-order function that applies a transform to each element
        const mapArray = East.function(
            [ArrayType(IntegerType), FunctionType([IntegerType], IntegerType)],
            ArrayType(IntegerType),
            ($, arr, fn) => {
                const result = $.let([] as bigint[], ArrayType(IntegerType));
                $.for(arr, ($, val) => {
                    $(result.pushLast(fn(val)));
                });
                return result;
            }
        );

        // Closure that captures 'factor' from outer scope
        const multiplyByFactor = East.function([IntegerType], IntegerType, ($, x) => {
            return x.multiply(factor);
        });

        const input = $.const([1n, 2n, 3n, 4n]);
        const output = $.let(mapArray(input, multiplyByFactor));

        // Each element multiplied by 3
        $(assert.equal(output.get(0n), 3n));
        $(assert.equal(output.get(1n), 6n));
        $(assert.equal(output.get(2n), 9n));
        $(assert.equal(output.get(3n), 12n));
    });

    test("closure with captured variable modified in loop", $ => {
        // Test that captured mutable variables work correctly with loops
        const threshold = $.const(5n);

        const countAboveThreshold = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
            const count = $.let(0n);
            $.for(arr, ($, val) => {
                $.if(East.greater(val, threshold), $ => {
                    $.assign(count, count.add(1n));
                });
            });
            return count;
        });

        // Values above 5: 7, 8, 9, 10 = 4 values
        $(assert.equal(countAboveThreshold([1n, 7n, 3n, 8n, 5n, 9n, 2n, 10n]), 4n));
    });

    test("function with string argument and return", $ => {
        const greet = East.function([StringType], StringType, ($, name) => {
            return East.str`Hello, ${name}!`;
        });
        $(assert.equal(greet("World"), "Hello, World!"));
    });

    test("struct with two functions", $ => {
        // Define a struct type containing two functions
        const MathOpsType = StructType({
            add: FunctionType([IntegerType, IntegerType], IntegerType),
            multiply: FunctionType([IntegerType, IntegerType], IntegerType),
        });

        // Create an instance with actual function implementations
        const mathOps = $.const({
            add: East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.add(b)),
            multiply: East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.multiply(b)),
        }, MathOpsType);

        // Call the functions from the struct
        $(assert.equal(mathOps.add(3n, 4n), 7n));
        $(assert.equal(mathOps.multiply(3n, 4n), 12n));

        // Chain operations
        $(assert.equal(mathOps.add(mathOps.multiply(2n, 3n), 4n), 10n));
    });

    test("variant Option containing a function - some case", $ => {
        // Define an Option type containing a function
        const MaybeTransformType = OptionType(FunctionType([IntegerType], IntegerType));

        // Create a some variant with a function
        const someTransform = $.const(
            variant("some", East.function([IntegerType], IntegerType, ($, x) => x.multiply(3n))),
            MaybeTransformType
        );

        // Match on the variant and call the function if present
        const result = $.let(0n);
        $.match(someTransform, {
            some: ($, fn) => {
                $.assign(result, fn(7n));
            },
            none: $ => {
                $.assign(result, -1n);
            },
        });
        $(assert.equal(result, 21n));
    });

    test("variant Option containing a function - none case", $ => {
        // Define an Option type containing a function
        const MaybeTransformType = OptionType(FunctionType([IntegerType], IntegerType));

        // Create a none variant
        const noTransform = $.const(variant("none", null), MaybeTransformType);

        // Match on the variant - should take the none branch
        const result = $.let(0n);
        $.match(noTransform, {
            some: ($, fn) => {
                $.assign(result, fn(7n));
            },
            none: $ => {
                $.assign(result, -1n);
            },
        });
        $(assert.equal(result, -1n));
    });

    test("array of functions", $ => {
        // Define an array type containing functions
        const TransformArrayType = ArrayType(FunctionType([IntegerType], IntegerType));

        // Create an array with multiple function implementations
        const transforms = $.const([
            East.function([IntegerType], IntegerType, ($, x) => x.add(1n)),
            East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n)),
            East.function([IntegerType], IntegerType, ($, x) => x.multiply(x)),
        ], TransformArrayType);

        // Call each function from the array by index
        $(assert.equal(transforms.get(0n)(5n), 6n));   // 5 + 1 = 6
        $(assert.equal(transforms.get(1n)(5n), 10n));  // 5 * 2 = 10
        $(assert.equal(transforms.get(2n)(5n), 25n));  // 5 * 5 = 25

        // Apply all transforms in sequence to a value
        const value = $.let(3n);
        $.for(transforms, ($, fn) => {
            $.assign(value, fn(value));
        });
        // 3 -> 4 (add 1) -> 8 (multiply 2) -> 64 (square)
        $(assert.equal(value, 64n));
    });

    test("linked list of functions using RecursiveType", $ => {
        // Define a linked list type where each node contains a function
        const FnListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({
                fn: FunctionType([IntegerType], IntegerType),
                next: self
            })
        }));

        // Create a linked list: add1 -> double -> square -> nil
        const nil = $.let(East.value(variant("nil"), FnListType));
        const squareNode = $.let(East.value(variant("cons", {
            fn: East.function([IntegerType], IntegerType, ($, x) => x.multiply(x)),
            next: nil
        }), FnListType));
        const doubleNode = $.let(East.value(variant("cons", {
            fn: East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n)),
            next: squareNode
        }), FnListType));
        const add1Node = $.let(East.value(variant("cons", {
            fn: East.function([IntegerType], IntegerType, ($, x) => x.add(1n)),
            next: doubleNode
        }), FnListType));

        // Traverse the list and apply each function in sequence
        const result = $.let(3n);
        const current = $.let(add1Node, FnListType);

        $.while(true, ($, label) => {
            $.match(current.unwrap(), {
                nil: $ => {
                    $.break(label);
                },
                cons: ($, node) => {
                    $.assign(result, node.fn(result));
                    $.assign(current, node.next);
                },
            });
        });

        // 3 -> 4 (add 1) -> 8 (double) -> 64 (square)
        $(assert.equal(result, 64n));
    });

    // =========================================================================
    // Recursive Types in Function Input/Output
    // =========================================================================

    test("function taking recursive type as input", $ => {
        // Define a linked list type
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        // Function that sums all elements in the list
        const sumList = East.function([ListType], IntegerType, ($, list) => {
            const sum = $.let(0n);
            const current = $.let(list, ListType);

            $.while(true, ($, label) => {
                $.match(current.unwrap(), {
                    nil: $ => {
                        $.break(label);
                    },
                    cons: ($, node) => {
                        $.assign(sum, sum.add(node.head));
                        $.assign(current, node.tail);
                    },
                });
            });
            return sum;
        });

        // Create list: 1 -> 2 -> 3 -> nil
        const nil = $.let(East.value(variant("nil"), ListType));
        const list = $.let(East.value(variant("cons", {
            head: 1n,
            tail: East.value(variant("cons", {
                head: 2n,
                tail: East.value(variant("cons", {
                    head: 3n,
                    tail: nil
                }), ListType)
            }), ListType)
        }), ListType));

        $(assert.equal(sumList(list), 6n));
    });

    test("function returning recursive type as output", $ => {
        // Define a linked list type
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        // Function that creates a list with n elements: n -> n-1 -> ... -> 1 -> nil
        const makeList = $.let(East.function([IntegerType], ListType, ($, n) => {
            const nil = $.let(East.value(variant("nil"), ListType));
            const result = $.let(nil, ListType);
            const i = $.let(1n);

            $.while(East.lessEqual(i, n), $ => {
                $.assign(result, East.value(variant("cons", {
                    head: i,
                    tail: result
                }), ListType));
                $.assign(i, i.add(1n));
            });

            return result;
        }));

        // Sum function to verify the list
        const sumList = $.let(East.function([ListType], IntegerType, ($, list) => {
            const sum = $.let(0n);
            const current = $.let(list, ListType);
            $.while(true, ($, label) => {
                $.match(current.unwrap(), {
                    nil: $ => $.break(label),
                    cons: ($, node) => {
                        $.assign(sum, sum.add(node.head));
                        $.assign(current, node.tail);
                    },
                });
            });
            return sum;
        }));

        // makeList(3) creates 3 -> 2 -> 1 -> nil, sum = 6
        $(assert.equal(sumList(makeList(3n)), 6n));
        // makeList(5) creates 5 -> 4 -> 3 -> 2 -> 1 -> nil, sum = 15
        $(assert.equal(sumList(makeList(5n)), 15n));
    });

    test("function taking and returning recursive type", $ => {
        // Linked list type (simpler for iteration)
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        // Function that doubles all values in the list (iterative)
        const doubleList = East.function([ListType], ListType, ($, list) => {
            // First pass: collect doubled values into array
            const values = $.let([] as bigint[], ArrayType(IntegerType));
            const current = $.let(list, ListType);
            $.while(true, ($, label) => {
                $.match(current.unwrap(), {
                    nil: $ => $.break(label),
                    cons: ($, node) => {
                        $(values.pushLast(node.head.multiply(2n)));
                        $.assign(current, node.tail);
                    },
                });
            });

            // Build result list in reverse
            const result = $.let(East.value(variant("nil"), ListType), ListType);
            const i = $.let(values.size().subtract(1n));
            $.while(East.greaterEqual(i, 0n), $ => {
                $.assign(result, East.value(variant("cons", {
                    head: values.get(i),
                    tail: result
                }), ListType));
                $.assign(i, i.subtract(1n));
            });
            return result;
        });

        // Function that sums all values in list (iterative)
        const sumList = East.function([ListType], IntegerType, ($, list) => {
            const sum = $.let(0n);
            const current = $.let(list, ListType);
            $.while(true, ($, label) => {
                $.match(current.unwrap(), {
                    nil: $ => $.break(label),
                    cons: ($, node) => {
                        $.assign(sum, sum.add(node.head));
                        $.assign(current, node.tail);
                    },
                });
            });
            return sum;
        });

        // Create list: 1 -> 2 -> 3 -> nil
        const nil = $.let(East.value(variant("nil"), ListType));
        const list = $.let(East.value(variant("cons", {
            head: 1n,
            tail: East.value(variant("cons", {
                head: 2n,
                tail: East.value(variant("cons", {
                    head: 3n,
                    tail: nil
                }), ListType)
            }), ListType)
        }), ListType));

        // Sum of original: 1 + 2 + 3 = 6
        $(assert.equal(sumList(list), 6n));
        // Sum of doubled: 2 + 4 + 6 = 12
        $(assert.equal(sumList(doubleList(list)), 12n));
    });

    test("struct containing function with recursive input/output", $ => {
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        // Struct with list operations
        const ListOpsType = StructType({
            prepend: FunctionType([ListType, IntegerType], ListType),
            sum: FunctionType([ListType], IntegerType),
        });

        const listOps = $.const({
            prepend: East.function([ListType, IntegerType], ListType, ($, list, val) => {
                return East.value(variant("cons", { head: val, tail: list }), ListType);
            }),
            sum: East.function([ListType], IntegerType, ($, list) => {
                const sum = $.let(0n);
                const current = $.let(list, ListType);
                $.while(true, ($, label) => {
                    $.match(current.unwrap(), {
                        nil: $ => $.break(label),
                        cons: ($, node) => {
                            $.assign(sum, sum.add(node.head));
                            $.assign(current, node.tail);
                        },
                    });
                });
                return sum;
            }),
        }, ListOpsType);

        const nil = $.let(East.value(variant("nil"), ListType));
        const list1 = $.let(listOps.prepend(nil, 1n), ListType);
        const list2 = $.let(listOps.prepend(list1, 2n), ListType);
        const list3 = $.let(listOps.prepend(list2, 3n), ListType);

        // list3 is 3 -> 2 -> 1 -> nil
        $(assert.equal(listOps.sum(list3), 6n));
    });

    test("option containing function with recursive type", $ => {
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        const MaybeTransformType = OptionType(FunctionType([ListType], IntegerType));

        // Some case with a sum function
        const someSum = $.const(
            variant("some", East.function([ListType], IntegerType, ($, list) => {
                const sum = $.let(0n);
                const current = $.let(list, ListType);
                $.while(true, ($, label) => {
                    $.match(current.unwrap(), {
                        nil: $ => $.break(label),
                        cons: ($, node) => {
                            $.assign(sum, sum.add(node.head));
                            $.assign(current, node.tail);
                        },
                    });
                });
                return sum;
            })),
            MaybeTransformType
        );

        const nil = $.let(East.value(variant("nil"), ListType));
        const list = $.let(East.value(variant("cons", {
            head: 5n,
            tail: East.value(variant("cons", { head: 3n, tail: nil }), ListType)
        }), ListType));

        const result = $.let(-1n);
        $.match(someSum, {
            some: ($, fn) => {
                $.assign(result, fn(list));
            },
            none: $ => {
                $.assign(result, 0n);
            },
        });

        $(assert.equal(result, 8n)); // 5 + 3 = 8
    });

    test("recursive type with function returning self", $ => {
        // Type where each node has a "next" function that returns the next node
        const ChainType = RecursiveType(self => VariantType({
            end: IntegerType,
            link: StructType({
                value: IntegerType,
                next: FunctionType([], self)
            })
        }));

        // Create chain: link(1, -> link(2, -> end(3)))
        const endNode = $.let(East.value(variant("end", 3n), ChainType));
        const link2 = $.let(East.value(variant("link", {
            value: 2n,
            next: East.function([], ChainType, _$ => endNode)
        }), ChainType));
        const link1 = $.let(East.value(variant("link", {
            value: 1n,
            next: East.function([], ChainType, _$ => link2)
        }), ChainType));

        // Traverse the chain and sum values
        const sum = $.let(0n);
        const current = $.let(link1, ChainType);

        $.while(true, ($, label) => {
            $.match(current.unwrap(), {
                end: ($, val) => {
                    $.assign(sum, sum.add(val));
                    $.break(label);
                },
                link: ($, node) => {
                    $.assign(sum, sum.add(node.value));
                    $.assign(current, node.next());
                },
            });
        });

        $(assert.equal(sum, 6n)); // 1 + 2 + 3 = 6
    });

    test("recursive type with function taking self as input", $ => {
        // A type where nodes can "merge" with other nodes
        const TreeType = RecursiveType(self => VariantType({
            leaf: IntegerType,
            branch: StructType({
                left: self,
                right: self,
                combine: FunctionType([self, self], self)
            })
        }));

        // Create a simple tree
        const leaf1 = $.let(East.value(variant("leaf", 1n), TreeType));
        const leaf2 = $.let(East.value(variant("leaf", 2n), TreeType));
        const leaf3 = $.let(East.value(variant("leaf", 3n), TreeType));
        const leaf4 = $.let(East.value(variant("leaf", 4n), TreeType));

        // Placeholder combiner for struct
        const placeholderCombiner = $.let(East.function([TreeType, TreeType], TreeType, ($, a, _b) => a));

        // Combine function that creates a new branch
        const combiner = East.function([TreeType, TreeType], TreeType, ($, a, b) => {
            return East.value(variant("branch", {
                left: a,
                right: b,
                combine: placeholderCombiner
            }), TreeType);
        });

        // Test that combiner works and returns correct type
        const branch1 = $.let(combiner(leaf1, leaf2), TreeType);
        const _branch2 = $.let(combiner(leaf3, leaf4), TreeType);

        // Verify leaf values can be extracted
        const leafVal = $.let(0n);
        $.match(leaf1.unwrap(), {
            leaf: ($, val) => {
                $.assign(leafVal, val);
            },
            branch: _$ => {},
        });
        $(assert.equal(leafVal, 1n));

        // Verify branch structure - extract left leaf value
        const branchLeftVal = $.let(0n);
        $.match(branch1.unwrap(), {
            leaf: _$ => {},
            branch: ($, b) => {
                $.match(b.left.unwrap(), {
                    leaf: ($, val) => {
                        $.assign(branchLeftVal, val);
                    },
                    branch: _$ => {},
                });
            },
        });
        $(assert.equal(branchLeftVal, 1n));

        // Test the combine function stored in branch
        // placeholderCombiner returns the first argument, so combine(leaf3, leaf4) returns leaf3
        const combinedTree = $.let(East.value(variant("leaf", 0n), TreeType), TreeType);
        $.match(branch1.unwrap(), {
            leaf: _$ => {},
            branch: ($, b) => {
                // Call the stored combine function
                $.assign(combinedTree, b.combine(leaf3, leaf4));
            },
        });
        // combinedTree should be leaf3 (since placeholderCombiner returns first arg)
        const combinedVal = $.let(0n);
        $.match(combinedTree.unwrap(), {
            leaf: ($, val) => {
                $.assign(combinedVal, val);
            },
            branch: _$ => {},
        });
        $(assert.equal(combinedVal, 3n));
    });

    test("higher-order function with recursive type parameters", $ => {
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        // fold function: applies fn to accumulator and each element
        const fold = East.function(
            [ListType, IntegerType, FunctionType([IntegerType, IntegerType], IntegerType)],
            IntegerType,
            ($, list, init, fn) => {
                const acc = $.let(init);
                const current = $.let(list, ListType);

                $.while(true, ($, label) => {
                    $.match(current.unwrap(), {
                        nil: $ => $.break(label),
                        cons: ($, node) => {
                            $.assign(acc, fn(acc, node.head));
                            $.assign(current, node.tail);
                        },
                    });
                });
                return acc;
            }
        );

        const nil = $.let(East.value(variant("nil"), ListType));
        const list = $.let(East.value(variant("cons", {
            head: 1n,
            tail: East.value(variant("cons", {
                head: 2n,
                tail: East.value(variant("cons", {
                    head: 3n,
                    tail: nil
                }), ListType)
            }), ListType)
        }), ListType));

        // Sum using fold
        const add = $.let(East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.add(b)));
        $(assert.equal(fold(list, 0n, add), 6n));

        // Product using fold
        const mul = $.let(East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.multiply(b)));
        $(assert.equal(fold(list, 1n, mul), 6n)); // 1 * 2 * 3 = 6
    });

    test("closure capturing recursive type value", $ => {
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        // Captured list
        const nil = $.let(East.value(variant("nil"), ListType));
        const capturedList = $.const(East.value(variant("cons", {
            head: 10n,
            tail: East.value(variant("cons", {
                head: 20n,
                tail: nil
            }), ListType)
        }), ListType), ListType);

        // Function that prepends a value to the captured list
        const prependToCaptured = East.function([IntegerType], ListType, ($, val) => {
            return East.value(variant("cons", { head: val, tail: capturedList }), ListType);
        });

        // Sum function
        const sumList = East.function([ListType], IntegerType, ($, list) => {
            const sum = $.let(0n);
            const current = $.let(list, ListType);
            $.while(true, ($, label) => {
                $.match(current.unwrap(), {
                    nil: $ => $.break(label),
                    cons: ($, node) => {
                        $.assign(sum, sum.add(node.head));
                        $.assign(current, node.tail);
                    },
                });
            });
            return sum;
        });

        // Prepend 5 to captured list [10, 20] -> [5, 10, 20]
        const newList = $.let(prependToCaptured(5n), ListType);
        $(assert.equal(sumList(newList), 35n)); // 5 + 10 + 20 = 35
    });

    test("async function with recursive input/output", $ => {
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        // Async function that reverses a list
        const reverseList = East.asyncFunction([ListType], ListType, ($, list) => {
            const nil = $.let(East.value(variant("nil"), ListType));
            const result = $.let(nil, ListType);
            const current = $.let(list, ListType);

            $.while(true, ($, label) => {
                $.match(current.unwrap(), {
                    nil: $ => $.break(label),
                    cons: ($, node) => {
                        $.assign(result, East.value(variant("cons", {
                            head: node.head,
                            tail: result
                        }), ListType));
                        $.assign(current, node.tail);
                    },
                });
            });
            return result;
        });

        // Create list 1 -> 2 -> 3 -> nil
        const nil = $.let(East.value(variant("nil"), ListType));
        const list = $.let(East.value(variant("cons", {
            head: 1n,
            tail: East.value(variant("cons", {
                head: 2n,
                tail: East.value(variant("cons", {
                    head: 3n,
                    tail: nil
                }), ListType)
            }), ListType)
        }), ListType));

        // Reverse and check first element (should be 3)
        const reversed = $.let(reverseList(list), ListType);
        const first = $.let(0n);
        $.match(reversed.unwrap(), {
            nil: _$ => {},
            cons: ($, node) => {
                $.assign(first, node.head);
            },
        });
        $(assert.equal(first, 3n));
    });

    test("simple async function returns resolved promise", $ => {
        const asyncGreet = East.asyncFunction([], StringType, _$ => {
            return "Hello, async!";
        });
        $(assert.equal(asyncGreet(), "Hello, async!"));
    });

    test("async function calls another async function", $ => {
        const asyncDouble = East.asyncFunction([IntegerType], IntegerType, (_$, x) => {
            return x.multiply(2n);
        });
        const asyncQuadruple = East.asyncFunction([IntegerType], IntegerType, ($, x) => {
            const doubled = $.let(asyncDouble(x));
            return asyncDouble(doubled);
        });
        $(assert.equal(asyncQuadruple(5n), 20n));
    });

    // =========================================================================
    // Function Serialization (BEAST2)
    // =========================================================================

    test("free function serialized to beast2 and deserialized can be called", $ => {
        const FnType = FunctionType([IntegerType], IntegerType);

        // Create a free function (no captures)
        const addOne = East.function([IntegerType], IntegerType, ($, x) => {
            return x.add(1n);
        });

        // Serialize to BEAST2
        const blob = $.let(East.Blob.encodeBeast(addOne, 'v2'));

        // Deserialize back to function
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        // Call the deserialized function
        $(assert.equal(decoded(41n), 42n));
        $(assert.equal(decoded(0n), 1n));
        $(assert.equal(decoded(-1n), 0n));
    });

    test("free function with multiple params serialized and called", $ => {
        const FnType = FunctionType([IntegerType, IntegerType], IntegerType);

        const add = East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => {
            return a.add(b);
        });

        const blob = $.let(East.Blob.encodeBeast(add, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(10n, 20n), 30n));
        $(assert.equal(decoded(-5n, 5n), 0n));
    });

    test("free function with control flow serialized and called", $ => {
        const FnType = FunctionType([IntegerType], IntegerType);

        // Absolute value function
        const abs = East.function([IntegerType], IntegerType, ($, x) => {
            $.if(East.less(x, 0n), ($) => {
                $.return(x.negate());
            });
            return x;
        });

        const blob = $.let(East.Blob.encodeBeast(abs, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(5n), 5n));
        $(assert.equal(decoded(-5n), 5n));
        $(assert.equal(decoded(0n), 0n));
    });

    test("free function with loop serialized and called", $ => {
        const FnType = FunctionType([IntegerType], IntegerType);

        // Sum from 1 to n
        const sumTo = East.function([IntegerType], IntegerType, ($, n) => {
            const sum = $.let(0n);
            const i = $.let(1n);
            $.while(East.lessEqual(i, n), ($) => {
                $.assign(sum, sum.add(i));
                $.assign(i, i.add(1n));
            });
            return sum;
        });

        const blob = $.let(East.Blob.encodeBeast(sumTo, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(5n), 15n));  // 1+2+3+4+5
        $(assert.equal(decoded(10n), 55n)); // 1+2+...+10
    });

    test("array of functions serialized and called", $ => {
        const FnType = FunctionType([IntegerType], IntegerType);
        const ArrayFnType = ArrayType(FnType);

        const funcs = $.const([
            East.function([IntegerType], IntegerType, ($, x) => x.add(1n)),
            East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n)),
            East.function([IntegerType], IntegerType, ($, x) => x.negate()),
        ], ArrayFnType);

        const blob = $.let(East.Blob.encodeBeast(funcs, 'v2'));
        const decoded = $.let(blob.decodeBeast(ArrayFnType, 'v2'));

        $(assert.equal(decoded.get(0n)(10n), 11n));  // addOne
        $(assert.equal(decoded.get(1n)(10n), 20n));  // double
        $(assert.equal(decoded.get(2n)(10n), -10n)); // negate
    });

    test("struct containing function serialized and called", $ => {
        const FnType = FunctionType([IntegerType], IntegerType);
        const StructWithFn = StructType({
            name: StringType,
            transform: FnType
        });

        const obj = $.const({
            name: "addOne",
            transform: East.function([IntegerType], IntegerType, ($, x) => x.add(1n)),
        }, StructWithFn);

        const blob = $.let(East.Blob.encodeBeast(obj, 'v2'));
        const decoded = $.let(blob.decodeBeast(StructWithFn, 'v2'));

        $(assert.equal(decoded.name, "addOne"));
        $(assert.equal(decoded.transform(5n), 6n));
    });

    test("function in recursive type (linked list) serialized and called", $ => {
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        const FnType = FunctionType([ListType], IntegerType);

        // Function that sums all elements in the list
        const sumList = East.function([ListType], IntegerType, ($, list) => {
            const sum = $.let(0n);
            const current = $.let(list, ListType);
            $.while(true, ($, label) => {
                $.match(current.unwrap(), {
                    nil: ($) => $.break(label),
                    cons: ($, node) => {
                        $.assign(sum, sum.add(node.head));
                        $.assign(current, node.tail);
                    },
                });
            });
            return sum;
        });

        // Serialize and deserialize
        const blob = $.let(East.Blob.encodeBeast(sumList, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        // Create list: 1 -> 2 -> 3 -> nil
        const nil = $.let(East.value(variant("nil"), ListType));
        const list = $.let(East.value(variant("cons", {
            head: 1n,
            tail: East.value(variant("cons", {
                head: 2n,
                tail: East.value(variant("cons", {
                    head: 3n,
                    tail: nil
                }), ListType)
            }), ListType)
        }), ListType));

        $(assert.equal(decoded(list), 6n));
    });

    test("function returning recursive type serialized and called", $ => {
        const ListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({ head: IntegerType, tail: self })
        }));

        const FnType = FunctionType([IntegerType], ListType);

        // Function that creates a list: n -> n-1 -> ... -> 1 -> nil
        const makeList = East.function([IntegerType], ListType, ($, n) => {
            const nil = $.let(East.value(variant("nil"), ListType));
            const result = $.let(nil, ListType);
            const i = $.let(1n);
            $.while(East.lessEqual(i, n), ($) => {
                $.assign(result, East.value(variant("cons", {
                    head: i,
                    tail: result
                }), ListType));
                $.assign(i, i.add(1n));
            });
            return result;
        });

        // Sum helper to verify the list
        const sumList = East.function([ListType], IntegerType, ($, list) => {
            const sum = $.let(0n);
            const current = $.let(list, ListType);
            $.while(true, ($, label) => {
                $.match(current.unwrap(), {
                    nil: ($) => $.break(label),
                    cons: ($, node) => {
                        $.assign(sum, sum.add(node.head));
                        $.assign(current, node.tail);
                    },
                });
            });
            return sum;
        });

        // Serialize and deserialize
        const blob = $.let(East.Blob.encodeBeast(makeList, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        // makeList(3) creates 3 -> 2 -> 1 -> nil, sum = 6
        $(assert.equal(sumList(decoded(3n)), 6n));
        // makeList(5) creates 5 -> 4 -> 3 -> 2 -> 1 -> nil, sum = 15
        $(assert.equal(sumList(decoded(5n)), 15n));
    });

    test("recursive type with function field serialized and called", $ => {
        // Linked list where each node contains a transform function
        const FnListType = RecursiveType(self => VariantType({
            nil: NullType,
            cons: StructType({
                fn: FunctionType([IntegerType], IntegerType),
                next: self
            })
        }));

        // Create list: add1 -> double -> square -> nil
        const nil = $.let(East.value(variant("nil"), FnListType));
        const squareNode = $.let(East.value(variant("cons", {
            fn: East.function([IntegerType], IntegerType, ($, x) => x.multiply(x)),
            next: nil
        }), FnListType));
        const doubleNode = $.let(East.value(variant("cons", {
            fn: East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n)),
            next: squareNode
        }), FnListType));
        const add1Node = $.let(East.value(variant("cons", {
            fn: East.function([IntegerType], IntegerType, ($, x) => x.add(1n)),
            next: doubleNode
        }), FnListType));

        // Serialize the entire list with embedded functions
        const blob = $.let(East.Blob.encodeBeast(add1Node, 'v2'));

        // Deserialize
        const decoded = $.let(blob.decodeBeast(FnListType, 'v2'));

        // Traverse and apply each function: 3 -> 4 (add1) -> 8 (double) -> 64 (square)
        const result = $.let(3n);
        const current = $.let(decoded, FnListType);

        $.while(true, ($, label) => {
            $.match(current.unwrap(), {
                nil: ($) => $.break(label),
                cons: ($, node) => {
                    $.assign(result, node.fn(result));
                    $.assign(current, node.next);
                },
            });
        });

        $(assert.equal(result, 64n));
    });

    // =========================================================================
    // Closure Serialization (Functions with Captures)
    // =========================================================================

    test("closure with integer capture serialized and called", $ => {
        const FnType = FunctionType([], IntegerType);

        // Create outer variable that will be captured
        const x = $.let(42n);

        // Create closure that captures x
        const getCaptured = $.let(East.function([], IntegerType, (_$) => {
            return x;
        }));

        // Serialize and deserialize
        const blob = $.let(East.Blob.encodeBeast(getCaptured, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        // Call the deserialized closure - should return captured value
        $(assert.equal(decoded(), 42n));
    });

    test("closure with multiple captures serialized and called", $ => {
        const FnType = FunctionType([], IntegerType);

        const a = $.let(10n);
        const b = $.let(20n);
        const c = $.let(12n);

        const sumCaptures = $.let(East.function([], IntegerType, (_$) => {
            return a.add(b).add(c);
        }));

        const blob = $.let(East.Blob.encodeBeast(sumCaptures, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 42n));
    });

    test("closure with array capture serialized and called", $ => {
        const FnType = FunctionType([], IntegerType);

        const arr = $.let([1n, 2n, 3n], ArrayType(IntegerType));

        const getLength = $.let(East.function([], IntegerType, (_$) => {
            return arr.length();
        }));

        const blob = $.let(East.Blob.encodeBeast(getLength, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 3n));
    });

    test("closure capturing another function serialized and called", $ => {
        const OuterFnType = FunctionType([IntegerType], IntegerType);

        // Create a function to be captured
        const addOne = $.let(East.function([IntegerType], IntegerType, ($, x) => {
            return x.add(1n);
        }));

        // Create closure that captures the function
        const applyAddOne = $.let(East.function([IntegerType], IntegerType, ($, x) => {
            return addOne(x);
        }));

        const blob = $.let(East.Blob.encodeBeast(applyAddOne, 'v2'));
        const decoded = $.let(blob.decodeBeast(OuterFnType, 'v2'));

        $(assert.equal(decoded(41n), 42n));
    });

    test("nested closure (closure returning closure) serialized and called", $ => {
        const InnerFnType = FunctionType([IntegerType], IntegerType);

        // makeAdder returns a closure that captures n
        const makeAdder = East.function([IntegerType], InnerFnType, ($, n) => {
            return East.function([IntegerType], IntegerType, ($, x) => {
                return x.add(n);
            });
        });

        // Create an adder that adds 5
        const addFive = $.let(makeAdder(5n));

        // Serialize and deserialize the closure (which captures 5)
        const blob = $.let(East.Blob.encodeBeast(addFive, 'v2'));
        const decoded = $.let(blob.decodeBeast(InnerFnType, 'v2'));

        $(assert.equal(decoded(37n), 42n));
        $(assert.equal(decoded(0n), 5n));
    });

    test("closure with struct capture serialized and called", $ => {
        const PointType = StructType({ x: IntegerType, y: IntegerType });
        const FnType = FunctionType([], IntegerType);

        const point = $.const({ x: 10n, y: 32n }, PointType);

        const getSum = $.let(East.function([], IntegerType, (_$) => {
            return point.x.add(point.y);
        }));

        const blob = $.let(East.Blob.encodeBeast(getSum, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 42n));
    });

    test("struct containing closure and captured value preserves identity", $ => {
        const FnType = FunctionType([IntegerType], NullType);
        const DataType = StructType({
            arr: ArrayType(IntegerType),
            push: FnType
        });

        // Create array and closure that captures it
        const arr = $.let([1n, 2n], ArrayType(IntegerType));
        const push = $.let(East.function([IntegerType], NullType, ($, val) => {
            $(arr.pushLast(val));
        }));

        // Create struct containing both - pass the expression values directly
        const data = $.const({ arr, push }, DataType);

        // Serialize and deserialize
        const blob = $.let(East.Blob.encodeBeast(data, 'v2'));
        const decoded = $.let(blob.decodeBeast(DataType, 'v2'));

        // Push via the decoded closure
        $(decoded.push(3n));

        // Check that the decoded array was modified (identity preserved)
        $(assert.equal(decoded.arr.length(), 3n));
        $(assert.equal(decoded.arr.get(2n), 3n));
    });

    // =========================================================================
    // Additional Edge Cases for Closure Serialization
    // =========================================================================

    test("separate closures in struct do not share captures after deserialization", $ => {
        // When two closures are serialized separately in a struct, each gets its own
        // copy of captured values - sharing is NOT preserved
        const FnType = FunctionType([], IntegerType);
        const MutatorType = FunctionType([IntegerType], NullType);
        const DataType = StructType({
            get: FnType,
            set: MutatorType
        });

        // Mutable variable
        const counter = $.let(0n);

        // Closure that reads the mutable capture
        const get = $.let(East.function([], IntegerType, (_$) => {
            return counter;
        }));

        // Closure that mutates the capture
        const set = $.let(East.function([IntegerType], NullType, ($, val) => {
            $.assign(counter, val);
        }));

        const data = $.const({ get, set }, DataType);

        const blob = $.let(East.Blob.encodeBeast(data, 'v2'));
        const decoded = $.let(blob.decodeBeast(DataType, 'v2'));

        // Initial value should be 0
        $(assert.equal(decoded.get(), 0n));

        // Mutate via the deserialized setter - this modifies setter's copy
        $(decoded.set(42n));

        // Getter has its own copy, so it still sees 0 (sharing not preserved)
        $(assert.equal(decoded.get(), 0n));
    });

    test("two closures sharing mutable variable at top level", $ => {
        // Simplest case: two closures at the same scope sharing a mutable variable
        const counter = $.let(0n);

        const inc = $.let(East.function([], NullType, ($) => {
            $.assign(counter, counter.add(1n));
        }));

        const get = $.let(East.function([], IntegerType, (_$) => {
            return counter;
        }));

        // Both should share the same counter
        $(assert.equal(get(), 0n));
        $(inc());
        $(assert.equal(get(), 1n));
        $(inc());
        $(inc());
        $(assert.equal(get(), 3n));
    });

    test("outer closure with shared mutable capture preserves sharing (no serialization)", $ => {
        // First verify the behavior without serialization
        const IncType = FunctionType([], NullType);
        const GetType = FunctionType([], IntegerType);
        const InnerType = StructType({
            inc: IncType,
            get: GetType
        });

        // Outer closure that creates shared state
        const makeCounter = $.let(East.function([], InnerType, ($) => {
            // This variable is captured by both inner closures
            const counter = $.let(0n);

            const inc = $.let(East.function([], NullType, ($) => {
                $.assign(counter, counter.add(1n));
            }));

            const get = $.let(East.function([], IntegerType, (_$) => {
                return counter;
            }));

            return { inc, get };
        }));

        // Call directly without serialization
        const inner = $.let(makeCounter());

        // Now inc and get share the same counter
        $(assert.equal(inner.get(), 0n));
        $(inner.inc());
        $(assert.equal(inner.get(), 1n));
        $(inner.inc());
        $(inner.inc());
        $(assert.equal(inner.get(), 3n));
    });

    test("outer closure with shared mutable capture preserves sharing (with serialization)", $ => {
        // When an outer closure captures a variable and contains inner closures
        // that also reference it, serializing the OUTER closure preserves sharing
        const IncType = FunctionType([], NullType);
        const GetType = FunctionType([], IntegerType);
        const InnerType = StructType({
            inc: IncType,
            get: GetType
        });
        const OuterType = FunctionType([], InnerType);

        // Outer closure that creates shared state
        const makeCounter = $.let(East.function([], InnerType, ($) => {
            // This variable is captured by both inner closures
            const counter = $.let(0n);

            const inc = $.let(East.function([], NullType, ($) => {
                $.assign(counter, counter.add(1n));
            }));

            const get = $.let(East.function([], IntegerType, (_$) => {
                return counter;
            }));

            return { inc, get };
        }));

        const blob = $.let(East.Blob.encodeBeast(makeCounter, 'v2'));
        const decoded = $.let(blob.decodeBeast(OuterType, 'v2'));

        // Call the outer closure to get the inner closures
        const inner = $.let(decoded());

        // Now inc and get share the same counter
        $(assert.equal(inner.get(), 0n));
        $(inner.inc());
        $(assert.equal(inner.get(), 1n));
        $(inner.inc());
        $(inner.inc());
        $(assert.equal(inner.get(), 3n));
    });

    test("async function with captures serialized and called", $ => {
        const FnType = AsyncFunctionType([], IntegerType);

        const x = $.let(42n);

        const getAsync = $.let(East.asyncFunction([], IntegerType, (_$) => {
            return x;
        }));

        const blob = $.let(East.Blob.encodeBeast(getAsync, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 42n));
    });

    test("deeply nested closures (A captures B captures C captures value)", $ => {
        const InnerType = FunctionType([], IntegerType);
        const MiddleType = FunctionType([], InnerType);
        const OuterType = FunctionType([], MiddleType);

        const value = $.let(42n);

        // C captures value
        const c = $.let(East.function([], IntegerType, (_$) => {
            return value;
        }));

        // B captures C
        const b = $.let(East.function([], InnerType, (_$) => {
            return c;
        }));

        // A captures B
        const a = $.let(East.function([], MiddleType, (_$) => {
            return b;
        }));

        const blob = $.let(East.Blob.encodeBeast(a, 'v2'));
        const decoded = $.let(blob.decodeBeast(OuterType, 'v2'));

        // Call through the chain: decoded() -> B, B() -> C, C() -> 42
        $(assert.equal(decoded()()(), 42n));
    });

    test("closure capturing struct value", $ => {
        const FnType = FunctionType([], IntegerType);
        const PointType = StructType({ x: IntegerType, y: IntegerType });

        // Capture a struct value
        const point = $.const({ x: 10n, y: 32n }, PointType);

        // Closure that returns the sum of x and y
        const getSum = $.let(East.function([], IntegerType, (_$) => {
            return point.x.add(point.y);
        }));

        const blob = $.let(East.Blob.encodeBeast(getSum, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 42n));
    });

    test("closure capturing Set", $ => {
        const FnType = FunctionType([], IntegerType);

        const s = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType));

        const getSize = $.let(East.function([], IntegerType, (_$) => {
            return s.size();
        }));

        const blob = $.let(East.Blob.encodeBeast(getSize, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 3n));
    });

    test("closure capturing Dict", $ => {
        const FnType = FunctionType([StringType], IntegerType);

        const d = $.let(new Map([["a", 1n], ["b", 2n]]), DictType(StringType, IntegerType));

        const getValue = $.let(East.function([StringType], IntegerType, ($, key) => {
            return d.get(key);
        }));

        const blob = $.let(East.Blob.encodeBeast(getValue, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded("a"), 1n));
        $(assert.equal(decoded("b"), 2n));
    });

    test("free function (no captures) serialized and called", $ => {
        const FnType = FunctionType([IntegerType, IntegerType], IntegerType);

        // Function with no captures - just uses parameters
        const add = $.let(East.function([IntegerType, IntegerType], IntegerType, (_$, a, b) => {
            return a.add(b);
        }));

        const blob = $.let(East.Blob.encodeBeast(add, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(20n, 22n), 42n));
    });

    test("closure capturing recursive type (linked list)", $ => {
        // Define a linked list type: .cons { head: Integer, tail: List } | .nil
        const ListType = RecursiveType(self => VariantType({
            cons: StructType({ head: IntegerType, tail: self }),
            nil: NullType
        }));
        const FnType = FunctionType([], IntegerType);

        // Build a list: cons(1, cons(2, cons(3, nil)))
        const nil = $.const(variant("nil", null), ListType);
        const list3 = $.const(variant("cons", { head: 3n, tail: nil }), ListType);
        const list2 = $.const(variant("cons", { head: 2n, tail: list3 }), ListType);
        const list1 = $.const(variant("cons", { head: 1n, tail: list2 }), ListType);

        // Closure that gets the head of the list
        const getHead = $.let(East.function([], IntegerType, (_$) => {
            return list1.unwrap().match({
                cons: (_$, data) => data.head,
                nil: _$ => 0n
            });
        }));

        const blob = $.let(East.Blob.encodeBeast(getHead, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 1n));
    });

    test("closure capturing variant value", $ => {
        const MaybeIntType = VariantType({ some: IntegerType, none: NullType });
        const FnType = FunctionType([], IntegerType);

        const maybeVal = $.const(variant("some", 42n), MaybeIntType);

        const extract = $.let(East.function([], IntegerType, (_$) => {
            return maybeVal.match({
                some: (_$, n) => n,
                none: _$ => 0n
            });
        }));

        const blob = $.let(East.Blob.encodeBeast(extract, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 42n));
    });

    test("closure capturing DateTime value", $ => {
        const FnType = FunctionType([], IntegerType);

        // Capture a specific datetime
        const dt = $.const(new Date("2025-06-15T12:00:00Z"), DateTimeType);

        const getYear = $.let(East.function([], IntegerType, (_$) => {
            return dt.getYear();
        }));

        const blob = $.let(East.Blob.encodeBeast(getYear, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 2025n));
    });

    test("closure capturing Blob value", $ => {
        const FnType = FunctionType([], IntegerType);

        // Capture a blob
        const b = $.const(new Uint8Array([1, 2, 3, 4, 5]), BlobType);

        const getLength = $.let(East.function([], IntegerType, (_$) => {
            return b.size();
        }));

        const blob = $.let(East.Blob.encodeBeast(getLength, 'v2'));
        const decoded = $.let(blob.decodeBeast(FnType, 'v2'));

        $(assert.equal(decoded(), 5n));
    });
});
