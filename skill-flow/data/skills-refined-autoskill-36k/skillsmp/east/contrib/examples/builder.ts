/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under AGPL-3.0. See LICENSE file for details.
 */
import type { EastIR } from "../../src/eastir.js";
import { East, type SubtypeExprOrValue } from "../../src/expr/index.js";
import { type EastType, FunctionType, IntegerType } from "../../src/types.js";

/** An example of using a fluent interface to build an East function */
export class FunctionBuilder<Is extends EastType[] = []> {
    constructor(private name: string, private inputs: Is = [] as unknown as Is) {
    }

    input<T extends EastType>(type: T): FunctionBuilder<[...Is, T]> {
        return new FunctionBuilder(this.name, [...this.inputs, type]);
    }

    output<T extends EastType>(type: T): FunctionBodyBuilder<Is, T> {
        return new FunctionBodyBuilder(this.name, this.inputs, type);
    }
}

class FunctionBodyBuilder<Is extends EastType[], O extends EastType> {
    constructor(private name: string, private inputs: Is, private output: O) {
    }

    body(expr: SubtypeExprOrValue<FunctionType<Is, O>>): FunctionFinalizer<Is, O> {
        const body = East.value(expr, FunctionType(this.inputs, this.output));

        return new FunctionFinalizer(this.name, this.inputs, this.output, body.toIR());
    }
}

class FunctionFinalizer<Is extends EastType[], O extends EastType> {
    constructor(public name: string, public inputs: Is, public output: O, private ir: EastIR<Is, O>) {}

    compile(): any {
        return this.ir.compile([]);
    }
}

// Example usage
const f = new FunctionBuilder("foo")
  .input(IntegerType)
  .input(IntegerType)
  .output(IntegerType)
  .body(($, x, y) => {
    const array = $.const([x, y]);
    const ret = $.let(0n);
    $.for(array, ($, item) => {
        $.assign(ret, ret.add(item));
    });
    return ret; // or $.return(ret);
  });

// Prints 3
console.log(f.compile()(1n, 2n));
