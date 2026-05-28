/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { BooleanType, FloatType, IntegerType, StringType } from "../../types.js";
import { Expr } from "../expr.js";

/** Standard library functions for floats */
export default {
  /**
   * Checks if two floats are approximately equal within an epsilon tolerance.
   *
   * @param x - The first float value
   * @param y - The second float value
   * @param epsilon - The maximum allowed difference between the values
   * @returns `true` if the absolute difference between `x` and `y` is less than or equal to `epsilon`
   *
   * @example
   * ```ts
   * const approxEq = East.function([FloatType, FloatType, FloatType], BooleanType, ($, x, y, eps) => {
   *   $.return(East.Float.approxEqual(x, y, eps));
   * });
   * const compiled = East.compile(approxEq.toIR(), []);
   * compiled(0.3, 0.1 + 0.2, 0.0001);  // true (handles floating point precision)
   * compiled(1.0, 1.1, 0.05);          // false
   * ```
   */
  approxEqual: Expr.function([FloatType, FloatType, FloatType], BooleanType, ($, x, y, epsilon) => {
    const diff = $.let(x.subtract(y).abs());
    $.return(Expr.lessEqual(diff, epsilon));
  }),

  /**
   * Rounds a float down to the nearest integer (floor).
   *
   * @param x - The float value to round
   * @returns The largest integer less than or equal to `x`
   *
   * @example
   * ```ts
   * const floor = East.function([FloatType], IntegerType, ($, x) => {
   *   $.return(East.Float.roundFloor(x));
   * });
   * const compiled = East.compile(floor.toIR(), []);
   * compiled(3.7);   // 3n
   * compiled(-2.3);  // -3n
   * ```
   */
  roundFloor: Expr.function([FloatType], IntegerType, ($, x) => {
    const rem = $.let(x.remainder(1.0));
    const is_exact = $.let(Expr.equal(rem, 0.0).bitOr(Expr.equal(rem, -0.0)));
    const floored_float = $.let(
      is_exact.ifElse(
        () => x,
        () => Expr.greaterEqual(x, 0.0).ifElse(
          () => x.subtract(rem),
          () => x.subtract(rem).subtract(1.0)
        )
      )
    );
    $.return(floored_float.toInteger());
  }),

  /**
   * Rounds a float up to the nearest integer (ceiling).
   *
   * @param x - The float value to round
   * @returns The smallest integer greater than or equal to `x`
   *
   * @example
   * ```ts
   * const ceil = East.function([FloatType], IntegerType, ($, x) => {
   *   $.return(East.Float.roundCeil(x));
   * });
   * const compiled = East.compile(ceil.toIR(), []);
   * compiled(3.2);   // 4n
   * compiled(-2.7);  // -2n
   * ```
   */
  roundCeil: Expr.function([FloatType], IntegerType, ($, x) => {
    // Use the step-based roundUp with step=1.0, then convert
    const rem = $.let(x.remainder(1.0));
    const is_exact = $.let(Expr.equal(rem, 0.0).bitOr(Expr.equal(rem, -0.0)));
    const ceiled_float = $.let(
      is_exact.ifElse(
        () => x,
        () => Expr.greaterEqual(x, 0.0).ifElse(
          () => x.subtract(rem).add(1.0),
          () => x.subtract(rem)
        )
      )
    );
    $.return(ceiled_float.toInteger());
  }),

  /**
   * Rounds a float to the nearest integer using half-away-from-zero rounding.
   *
   * @param x - The float value to round
   * @returns The nearest integer, with ties (0.5) rounding away from zero
   *
   * @example
   * ```ts
   * const roundHalf = East.function([FloatType], IntegerType, ($, x) => {
   *   $.return(East.Float.roundHalf(x));
   * });
   * const compiled = East.compile(roundHalf.toIR(), []);
   * compiled(3.5);   // 4n
   * compiled(3.4);   // 3n
   * compiled(-2.5);  // -3n
   * ```
   */
  roundHalf: Expr.function([FloatType], IntegerType, ($, x) => {
    const rounded_float = $.let(
      Expr.greaterEqual(x, 0.0).ifElse(
        () => x.add(0.5).subtract(x.add(0.5).remainder(1.0)),
        () => x.subtract(0.5).subtract(x.subtract(0.5).remainder(1.0))
      )
    );
    $.return(rounded_float.toInteger());
  }),

  /**
   * Truncates a float towards zero (removes the fractional part).
   *
   * @param x - The float value to truncate
   * @returns The integer part of `x`, discarding the fractional part
   *
   * @example
   * ```ts
   * const trunc = East.function([FloatType], IntegerType, ($, x) => {
   *   $.return(East.Float.roundTrunc(x));
   * });
   * const compiled = East.compile(trunc.toIR(), []);
   * compiled(3.7);   // 3n
   * compiled(-2.7);  // -2n
   * ```
   */
  roundTrunc: Expr.function([FloatType], IntegerType, ($, x) => {
    const truncated_float = $.let(x.subtract(x.remainder(1.0)));
    $.return(truncated_float.toInteger());
  }),

  /**
   * Rounds a float to the nearest multiple of a step value.
   *
   * @param x - The float value to round
   * @param step - The step value to round to (uses absolute value)
   * @returns The nearest multiple of `step`, with ties rounding away from zero
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const roundNearest = East.function([FloatType, FloatType], FloatType, ($, x, step) => {
   *   $.return(East.Float.roundNearest(x, step));
   * });
   * const compiled = East.compile(roundNearest.toIR(), []);
   * compiled(17.3, 5.0);     // 15.0
   * compiled(17.6, 5.0);     // 20.0
   * compiled(3.14159, 0.01); // 3.14
   * ```
   */
  roundNearest: Expr.function([FloatType, FloatType], FloatType, ($, x, step) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot round NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot round Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot round -Infinity"));

    $.if(Expr.equal(step, 0.0), $ => $.return(x));

    const abs_step = $.let(step.abs());
    const divisions = $.let(x.divide(abs_step));

    // Round to nearest integer multiple
    const rounded_divisions_float = $.let(
      Expr.greaterEqual(divisions, 0.0).ifElse(
        () => {
          const shifted = divisions.add(0.5);
          return shifted.subtract(shifted.remainder(1.0));
        },
        () => {
          const shifted = divisions.subtract(0.5);
          return shifted.subtract(shifted.remainder(1.0));
        }
      )
    );

    $.return(rounded_divisions_float.multiply(abs_step));
  }),

  /**
   * Rounds a float up to the next multiple of a step value (ceiling).
   *
   * @param x - The float value to round
   * @param step - The step value to round to (uses absolute value)
   * @returns The smallest multiple of `step` greater than or equal to `x`
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const roundUp = East.function([FloatType, FloatType], FloatType, ($, x, step) => {
   *   $.return(East.Float.roundUp(x, step));
   * });
   * const compiled = East.compile(roundUp.toIR(), []);
   * compiled(17.1, 5.0);  // 20.0
   * compiled(15.0, 5.0);  // 15.0 (already exact)
   * compiled(3.14, 0.1);  // 3.2
   * ```
   */
  roundUp: Expr.function([FloatType, FloatType], FloatType, ($, x, step) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot round NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot round Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot round -Infinity"));

    $.if(Expr.equal(step, 0.0), $ => $.return(x));

    const abs_step = $.let(step.abs());
    const divisions = $.let(x.divide(abs_step));
    const rem = $.let(divisions.remainder(1.0));

    // Check if already exact
    const is_exact = $.let(Expr.equal(rem, 0.0).bitOr(Expr.equal(rem, -0.0)));
    $.if(is_exact, $ => $.return(x));

    // Round up
    const ceiled = $.let(
      Expr.greaterEqual(x, 0.0).ifElse(
        () => divisions.subtract(rem).add(1.0),
        () => divisions.subtract(rem)
      )
    );
    $.return(ceiled.multiply(abs_step));
  }),

  /**
   * Rounds a float down to the previous multiple of a step value (floor).
   *
   * @param x - The float value to round
   * @param step - The step value to round to (uses absolute value)
   * @returns The largest multiple of `step` less than or equal to `x`
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const roundDown = East.function([FloatType, FloatType], FloatType, ($, x, step) => {
   *   $.return(East.Float.roundDown(x, step));
   * });
   * const compiled = East.compile(roundDown.toIR(), []);
   * compiled(17.9, 5.0);  // 15.0
   * compiled(15.0, 5.0);  // 15.0 (already exact)
   * compiled(3.19, 0.1);  // 3.1
   * ```
   */
  roundDown: Expr.function([FloatType, FloatType], FloatType, ($, x, step) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot round NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot round Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot round -Infinity"));

    $.if(Expr.equal(step, 0.0), $ => $.return(x));

    const abs_step = $.let(step.abs());
    const divisions = $.let(x.divide(abs_step));
    const rem = $.let(divisions.remainder(1.0));

    // Check if already exact
    const is_exact = $.let(Expr.equal(rem, 0.0).bitOr(Expr.equal(rem, -0.0)));
    $.if(is_exact, $ => $.return(x));

    // Round down
    const floored = $.let(
      Expr.greaterEqual(x, 0.0).ifElse(
        () => divisions.subtract(rem),
        () => divisions.subtract(rem).subtract(1.0)
      )
    );
    $.return(floored.multiply(abs_step));
  }),

  /**
   * Rounds a float towards zero to the nearest multiple of a step value (truncate).
   *
   * @param x - The float value to round
   * @param step - The step value to round to (uses absolute value)
   * @returns The multiple of `step` closest to zero that is between zero and `x`
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const roundTruncate = East.function([FloatType, FloatType], FloatType, ($, x, step) => {
   *   $.return(East.Float.roundTruncate(x, step));
   * });
   * const compiled = East.compile(roundTruncate.toIR(), []);
   * compiled(17.9, 5.0);   // 15.0
   * compiled(-17.9, 5.0);  // -15.0
   * ```
   */
  roundTruncate: Expr.function([FloatType, FloatType], FloatType, ($, x, step) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot round NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot round Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot round -Infinity"));

    $.if(Expr.equal(step, 0.0), $ => $.return(x));

    const abs_step = $.let(step.abs());
    const divisions = $.let(x.divide(abs_step));
    const truncated = $.let(divisions.subtract(divisions.remainder(1.0)));

    $.return(truncated.multiply(abs_step));
  }),

  /**
   * Rounds a float to a specified number of decimal places.
   *
   * @param x - The float value to round
   * @param decimals - The number of decimal places to round to
   * @returns The float rounded to the specified number of decimal places
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const roundDecimals = East.function([FloatType, IntegerType], FloatType, ($, x, decimals) => {
   *   $.return(East.Float.roundToDecimals(x, decimals));
   * });
   * const compiled = East.compile(roundDecimals.toIR(), []);
   * compiled(3.14159, 2n);  // 3.14
   * compiled(2.5, 0n);      // 3.0
   * ```
   */
  roundToDecimals: Expr.function([FloatType, IntegerType], FloatType, ($, x, decimals) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot round NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot round Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot round -Infinity"));

    // Build multiplier as 10^decimals iteratively
    const remaining = $.let(decimals);
    const multiplier = $.let(1.0);

    $.while(Expr.greater(remaining, 0n), $ => {
      $.assign(multiplier, multiplier.multiply(10.0));
      $.assign(remaining, remaining.subtract(1n));
    });

    const scaled = $.let(x.multiply(multiplier));
    const rounded = $.let(
      Expr.greaterEqual(scaled, 0.0).ifElse(
        () => {
          const shifted = scaled.add(0.5);
          return shifted.subtract(shifted.remainder(1.0));
        },
        () => {
          const shifted = scaled.subtract(0.5);
          return shifted.subtract(shifted.remainder(1.0));
        }
      )
    );

    $.return(rounded.divide(multiplier));
  }),

  /**
   * Formats a float with comma separators for thousands.
   *
   * @param x - The float value to format
   * @param decimals - The number of decimal places to display
   * @returns A formatted string with comma separators (e.g., `"1,234.567"`)
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const formatComma = East.function([FloatType, IntegerType], StringType, ($, x, decimals) => {
   *   $.return(East.Float.printCommaSeperated(x, decimals));
   * });
   * const compiled = East.compile(formatComma.toIR(), []);
   * compiled(1234.567, 2n);    // "1,234.57"
   * compiled(1000000, 0n);     // "1,000,000"
   * compiled(-5432.1, 3n);     // "-5,432.100"
   * ```
   */
  printCommaSeperated: Expr.function([FloatType, IntegerType], StringType, ($, x, decimals) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot format NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot format Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot format -Infinity"));

    const negative = $.let(Expr.less(x, 0.0));
    const abs_x = $.let(x.abs());

    // Build multiplier for rounding
    const remaining = $.let(decimals);
    const multiplier = $.let(1.0);
    $.while(Expr.greater(remaining, 0n), $ => {
      $.assign(multiplier, multiplier.multiply(10.0));
      $.assign(remaining, remaining.subtract(1n));
    });

    // Round and split
    const scaled = $.let(abs_x.multiply(multiplier));
    const shifted = $.let(scaled.add(0.5));
    const rounded_scaled_float = $.let(shifted.subtract(shifted.remainder(1.0)));
    const rounded_scaled = $.let(rounded_scaled_float.toInteger());
    const integer_part = $.let(rounded_scaled.divide(multiplier.toInteger()));
    const frac_part = $.let(rounded_scaled.remainder(multiplier.toInteger()));

    // Format integer with commas
    const int_with_commas = $.let(integer_part);
    const comma_ret = $.let("");

    $.while(Expr.greater(int_with_commas, 999n), $ => {
      const z = $.let(int_with_commas.remainder(1000n));

      $.if(
        Expr.less(z, 10n),
        $ => {
          $.assign(comma_ret, Expr.str`,00${z}${comma_ret}`);
        }
      ).else(
        $ => {
          $.if(
            Expr.less(z, 100n),
            $ => {
              $.assign(comma_ret, Expr.str`,0${z}${comma_ret}`);
            }
          ).else(
            $ => {
              $.assign(comma_ret, Expr.str`,${z}${comma_ret}`);
            }
          )
        }
      )

      $.assign(int_with_commas, int_with_commas.divide(1000n));
    });

    const int_str = $.let(Expr.str`${int_with_commas}${comma_ret}`);

    // Format fractional part with padding
    const frac_str = $.let(Expr.str`${frac_part}`);
    const padding_needed = $.let(decimals.subtract(frac_str.length()));
    const padding = $.let("");

    $.while(Expr.greater(padding_needed, 0n), $ => {
      $.assign(padding, Expr.str`0${padding}`);
      $.assign(padding_needed, padding_needed.subtract(1n));
    });

    const result = $.let(
      Expr.equal(decimals, 0n).ifElse(
        () => int_str,
        () => Expr.str`${int_str}.${padding}${frac_str}`
      )
    );

    $.return(negative.ifElse(() => Expr.str`-${result}`, () => result));
  }),

  /**
   * Formats a float as currency with comma separators and 2 decimal places.
   *
   * @param x - The float value to format as currency
   * @returns A formatted currency string (e.g., `"$1,234.56"`)
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const formatCurrency = East.function([FloatType], StringType, ($, x) => {
   *   $.return(East.Float.printCurrency(x));
   * });
   * const compiled = East.compile(formatCurrency.toIR(), []);
   * compiled(1234.567);   // "$1,234.57"
   * compiled(-42.5);      // "-$42.50"
   * compiled(1000000);    // "$1,000,000.00"
   * ```
   */
  printCurrency: Expr.function([FloatType], StringType, ($, x) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot format NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot format Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot format -Infinity"));

    const negative = $.let(Expr.less(x, 0.0));
    const abs_x = $.let(x.abs());

    // Round to cents
    const shifted = $.let(abs_x.multiply(100.0).add(0.5));
    const cents_total_float = $.let(shifted.subtract(shifted.remainder(1.0)));
    const cents_total = $.let(cents_total_float.toInteger());
    const dollars = $.let(cents_total.divide(100n));
    const cents = $.let(cents_total.remainder(100n));

    // Format dollars with commas
    const dollars_with_commas = $.let(dollars);
    const comma_ret = $.let("");

    $.while(Expr.greater(dollars_with_commas, 999n), $ => {
      const z = $.let(dollars_with_commas.remainder(1000n));

      $.if(
        Expr.less(z, 10n),
        $ => {
          $.assign(comma_ret, Expr.str`,00${z}${comma_ret}`);
        }
      ).else(
        $ => {
          $.if(
            Expr.less(z, 100n),
            $ => {
              $.assign(comma_ret, Expr.str`,0${z}${comma_ret}`);
            }
          ).else(
            $ => {
              $.assign(comma_ret, Expr.str`,${z}${comma_ret}`);
            }
          )
        }
      )

      $.assign(dollars_with_commas, dollars_with_commas.divide(1000n));
    });

    const dollars_str = $.let(Expr.str`${dollars_with_commas}${comma_ret}`);
    const cents_str = $.let(Expr.less(cents, 10n).ifElse(
      () => Expr.str`0${cents}`,
      () => Expr.str`${cents}`
    ));

    const result = $.let(Expr.str`${dollars_str}.${cents_str}`);

    $.return(negative.ifElse(() => Expr.str`-$${result}`, () => Expr.str`$${result}`));
  }),

  /**
   * Formats a float with a fixed number of decimal places.
   *
   * @param x - The float value to format
   * @param decimals - The number of decimal places to display
   * @returns A formatted string with the specified decimal places (e.g., `"3.14"`)
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const formatFixed = East.function([FloatType, IntegerType], StringType, ($, x, decimals) => {
   *   $.return(East.Float.printFixed(x, decimals));
   * });
   * const compiled = East.compile(formatFixed.toIR(), []);
   * compiled(3.14159, 2n);  // "3.14"
   * compiled(42, 3n);       // "42.000"
   * compiled(-0.5, 1n);     // "-0.5"
   * ```
   */
  printFixed: Expr.function([FloatType, IntegerType], StringType, ($, x, decimals) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot format NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot format Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot format -Infinity"));

    const negative = $.let(Expr.less(x, 0.0));
    const abs_x = $.let(x.abs());

    // Build multiplier
    const remaining = $.let(decimals);
    const multiplier = $.let(1.0);
    $.while(Expr.greater(remaining, 0n), $ => {
      $.assign(multiplier, multiplier.multiply(10.0));
      $.assign(remaining, remaining.subtract(1n));
    });

    // Round and split
    const scaled = $.let(abs_x.multiply(multiplier));
    const shifted = $.let(scaled.add(0.5));
    const rounded_scaled_float = $.let(shifted.subtract(shifted.remainder(1.0)));
    const rounded_scaled = $.let(rounded_scaled_float.toInteger());
    const integer_part = $.let(rounded_scaled.divide(multiplier.toInteger()));
    const frac_part = $.let(rounded_scaled.remainder(multiplier.toInteger()));

    // Format fractional part with padding
    const frac_str = $.let(Expr.str`${frac_part}`);
    const padding_needed = $.let(decimals.subtract(frac_str.length()));
    const padding = $.let("");

    $.while(Expr.greater(padding_needed, 0n), $ => {
      $.assign(padding, Expr.str`0${padding}`);
      $.assign(padding_needed, padding_needed.subtract(1n));
    });

    const result = $.let(
      Expr.equal(decimals, 0n).ifElse(
        () => Expr.str`${integer_part}`,
        () => Expr.str`${integer_part}.${padding}${frac_str}`
      )
    );

    $.return(negative.ifElse(() => Expr.str`-${result}`, () => result));
  }),

  /**
   * Formats a float in compact form with business unit suffixes.
   *
   * Uses suffixes: K (thousands), M (millions), B (billions), T (trillions),
   * Q (quadrillions), Qi (quintillions).
   *
   * @param x - The float value to format
   * @returns A compact formatted string (e.g., `"21.5K"`, `"1.82M"`, `"314B"`)
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const formatCompact = East.function([FloatType], StringType, ($, x) => {
   *   $.return(East.Float.printCompact(x));
   * });
   * const compiled = East.compile(formatCompact.toIR(), []);
   * compiled(1500);         // "1.5K"
   * compiled(2500000);      // "2.5M"
   * compiled(3140000000);   // "3.14B"
   * ```
   */
  printCompact: Expr.function([FloatType], StringType, ($, x) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot format NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot format Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot format -Infinity"));

    const negative = $.let(Expr.less(x, 0.0));
    const y = $.let(x.abs());

    $.if(Expr.less(y, 1000.0), $ => {
      const shifted = $.let(y.add(0.5));
      const rounded_int = $.let(shifted.subtract(shifted.remainder(1.0)));
      const rounded = $.let(rounded_int.divide(100.0));
      $.return(negative.ifElse(() => Expr.str`-${rounded}`, () => Expr.str`${rounded}`))
    });

    const scale = $.let(1n);
    const scaled = $.let(y);

    $.while(Expr.greaterEqual(scaled, 1000000.0), $ => {
      $.assign(scaled, scaled.divide(1000.0));
      $.assign(scale, scale.add(1n));
    });

    const suffix = $.let(
      Expr.equal(scale, 1n).ifElse(() => "K", () =>
        Expr.equal(scale, 2n).ifElse(() => "M", () =>
          Expr.equal(scale, 3n).ifElse(() => "B", () =>
            Expr.equal(scale, 4n).ifElse(() => "T", () =>
              Expr.equal(scale, 5n).ifElse(() => "Q", () => "Qi")
            )
          )
        )
      )
    );

    const div = $.let(scaled.divide(1000.0));

    $.if(Expr.greaterEqual(scaled, 100000.0), $ => {
      const shifted = $.let(div.add(0.5));
      const rounded_float = $.let(shifted.subtract(shifted.remainder(1.0)));
      const rounded = $.let(rounded_float.toInteger());
      $.return(negative.ifElse(() => Expr.str`-${rounded}${suffix}`, () => Expr.str`${rounded}${suffix}`));
    });

    $.if(Expr.greaterEqual(scaled, 10000.0), $ => {
      const shifted = $.let(div.multiply(10.0).add(0.5));
      const rounded_int = $.let(shifted.subtract(shifted.remainder(1.0)));
      const rounded = $.let(rounded_int.divide(10.0));
      $.return(negative.ifElse(() => Expr.str`-${rounded}${suffix}`, () => Expr.str`${rounded}${suffix}`));
    });

    const shifted = $.let(div.multiply(100.0).add(0.5));
    const rounded_int = $.let(shifted.subtract(shifted.remainder(1.0)));
    const rounded = $.let(rounded_int.divide(100.0));
    $.return(negative.ifElse(() => Expr.str`-${rounded}${suffix}`, () => Expr.str`${rounded}${suffix}`));
  }),

  /**
   * Formats a float as a percentage.
   *
   * Multiplies the value by 100 and appends a percent sign.
   *
   * @param x - The float value to format (e.g., `0.452` for 45.2%)
   * @param decimals - The number of decimal places to display
   * @returns A formatted percentage string (e.g., `"45.2%"`)
   * @throws {Error} When `x` is NaN, Infinity, or -Infinity
   *
   * @example
   * ```ts
   * const formatPercent = East.function([FloatType, IntegerType], StringType, ($, x, decimals) => {
   *   $.return(East.Float.printPercentage(x, decimals));
   * });
   * const compiled = East.compile(formatPercent.toIR(), []);
   * compiled(0.452, 1n);   // "45.2%"
   * compiled(0.5, 0n);     // "50%"
   * compiled(-0.123, 2n);  // "-12.30%"
   * ```
   */
  printPercentage: Expr.function([FloatType, IntegerType], StringType, ($, x, decimals) => {
    // Check for NaN/Infinity
    $.if(Expr.equal(x, NaN), $ => $.error("Cannot format NaN"));
    $.if(Expr.equal(x, Infinity), $ => $.error("Cannot format Infinity"));
    $.if(Expr.equal(x, -Infinity), $ => $.error("Cannot format -Infinity"));

    const percentage = $.let(x.multiply(100.0));

    // Build multiplier
    const remaining = $.let(decimals);
    const multiplier = $.let(1.0);
    $.while(Expr.greater(remaining, 0n), $ => {
      $.assign(multiplier, multiplier.multiply(10.0));
      $.assign(remaining, remaining.subtract(1n));
    });

    const scaled = $.let(percentage.multiply(multiplier));
    const shifted = $.let(
      Expr.greaterEqual(scaled, 0.0).ifElse(
        () => scaled.add(0.5),
        () => scaled.subtract(0.5)
      )
    );
    const rounded_int = $.let(shifted.subtract(shifted.remainder(1.0)));
    const rounded = $.let(rounded_int.divide(multiplier));

    $.return(Expr.str`${rounded}%`);
  }),
}
