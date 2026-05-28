/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { IntegerType, StringType } from "../../types.js";
import { Expr } from "../expr.js";

/** Standard library functions for integers */
export default {
  /**
   * Formats an integer with comma separators for thousands.
   *
   * @param x - The integer value to format
   * @returns A formatted string with comma separators (e.g., `"1,234,567"`)
   *
   * @example
   * ```ts
   * const formatComma = East.function([IntegerType], StringType, ($, x) => {
   *   $.return(East.Integer.printCommaSeperated(x));
   * });
   * const compiled = East.compile(formatComma.toIR(), []);
   * compiled(1234567n);    // "1,234,567"
   * compiled(1000n);       // "1,000"
   * compiled(-5432n);      // "-5,432"
   * ```
   */
  printCommaSeperated: Expr.function([IntegerType], StringType, ($, x) => {
    const y = $.let(x);

    const negative = $.let(false);
    $.if(Expr.less(y, 0n), $ => {
      $.if(Expr.equal(y, -9223372036854775808n), $ => $.return("-9,223,372,036,854,775,808")) // cannot negate -2^63 as an i64

      $.assign(negative, true);
      $.assign(y, y.negate());
    })

    const ret = $.let("")
    $.while(Expr.greater(y, 999n), $ => {
      const z = $.let(y.remainder(1000n));

      $.if(
        Expr.less(z, 10n),
        $ => {
          $.assign(ret, Expr.str`,00${z}${ret}`);
        }
      ).else(
        $ => {
          $.if(
            Expr.less(z, 100n),
            $ => {
              $.assign(ret, Expr.str`,0${z}${ret}`);
            }
          ).else(
            $ => {
              $.assign(ret, Expr.str`,${z}${ret}`);
            }
          )
        }
      )

      $.assign(y, y.divide(1000n));
    })

    $.if(negative,
      $ => $.return(Expr.str`-${y}${ret}`)
    ).else(
      $ => $.return(Expr.str`${y}${ret}`)
    )
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
     * const formatCurrency = East.function([IntegerType], StringType, ($, x) => {
     *   $.return(East.Integer.printCurrency(x));
     * });
     * const compiled = East.compile(formatCurrency.toIR(), []);
     * compiled(1234n);   // "$1,234"
     * compiled(-42n);      // "-$42"
     * compiled(1000000n);    // "$1,000,000"
     * ```
     */
    printCurrency: Expr.function([IntegerType], StringType, ($, x) => {
      // Check for NaN/Infinity
      const negative = $.let(Expr.less(x, 0n));
      const abs_x = $.let(x.abs());
  
      // Round to cents
      const shifted = $.let(abs_x.multiply(100.0).add(0.5));
      const cents_total_float = $.let(shifted.subtract(shifted.remainder(1.0)));
      const cents_total = $.let(cents_total_float.toInteger());
      const dollars = $.let(cents_total.divide(100n));
      
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
  
      const result = $.let(Expr.str`${dollars_str}`);
  
      $.return(negative.ifElse(() => Expr.str`-$${result}`, () => Expr.str`$${result}`));
    }),

  /**
   * Formats an integer in compact form with business unit suffixes.
   *
   * Uses suffixes: K (thousands), M (millions), B (billions), T (trillions),
   * Q (quadrillions), Qi (quintillions). Displays up to 3 significant digits.
   *
   * @param x - The integer value to format
   * @returns A compact formatted string (e.g., `"21.5K"`, `"1.82M"`, `"314B"`)
   *
   * @example
   * ```ts
   * const formatCompact = East.function([IntegerType], StringType, ($, x) => {
   *   $.return(East.Integer.printCompact(x));
   * });
   * const compiled = East.compile(formatCompact.toIR(), []);
   * compiled(1500n);        // "1.5K"
   * compiled(2500000n);     // "2.5M"
   * compiled(3140000000n);  // "3.14B"
   * compiled(500n);         // "500"
   * ```
   */
  printCompact: Expr.function([IntegerType], StringType, ($, x) => {
    const y = $.let(x);

    const negative = $.let(false);
    $.if(Expr.less(y, 0n), $ => {
      $.if(Expr.equal(y, -9223372036854775808n), $ => $.return("-9.22Qi")); // cannot negate -2^63 as an i64

      $.assign(negative, true);
      $.assign(y, y.negate());
    })

    $.if(Expr.less(y, 1000n), $ => $.return(negative.ifElse(() => Expr.str`-${y}`, () => Expr.str`${y}`)))

    const scale = $.let(1n);
    $.while(Expr.greaterEqual(y, 1000000n), $ => {
      $.assign(y, y.divide(1000n));
      $.assign(scale, scale.add(1n));
    });

    const suffix = $.let(Expr.equal(scale, 1n).ifElse(() => "K", () => Expr.equal(scale, 2n).ifElse(() => "M", () => Expr.equal(scale, 3n).ifElse(() => "B", () => Expr.equal(scale, 4n).ifElse(() => "T", () => Expr.equal(scale, 5n).ifElse(() => "Q", () => "Qi"))))));

    $.if(Expr.greaterEqual(y, 100000n), $ => {
      $.if(negative, $ => {
        $.return(Expr.str`-${y.divide(1000n)}${suffix}`)
      }).else($ => {
        $.return(Expr.str`${y.divide(1000n)}${suffix}`)
      });
    });

    $.if(Expr.greaterEqual(y, 10000n), $ => {
      const part = $.let(y.divide(100n).remainder(10n));

      $.if(negative,
        $ => $.return(Expr.str`-${y.divide(1000n)}.${part}${suffix}`)
      ).else(
        $ => $.return(Expr.str`${y.divide(1000n)}.${part}${suffix}`)
      );
    })

    const part = $.let(y.divide(10n).remainder(100n));
    $.if(
      Expr.greaterEqual(part, 10n),
      $ => {
        $.if(negative,
          $ => $.return(Expr.str`-${y.divide(1000n)}.${part}${suffix}`)
        ).else(
          $ => $.return(Expr.str`${y.divide(1000n)}.${part}${suffix}`)
        );
      }
    ).else(
      $ => {
        $.if(negative,
          $ => $.return(Expr.str`-${y.divide(1000n)}.0${part}${suffix}`)
        ).else(
          $ => $.return(Expr.str`${y.divide(1000n)}.0${part}${suffix}`)
        );
      }
    );
  }),

  /**
   * Formats an integer in compact form with SI (International System) unit suffixes.
   *
   * Uses SI suffixes: k (kilo, thousands), M (mega, millions), G (giga, billions),
   * T (tera, trillions), P (peta, quadrillions), E (exa, quintillions).
   * Displays up to 3 significant digits.
   *
   * @param x - The integer value to format
   * @returns A compact formatted string with SI units (e.g., `"21.5k"`, `"1.82M"`, `"314G"`)
   *
   * @example
   * ```ts
   * const formatSI = East.function([IntegerType], StringType, ($, x) => {
   *   $.return(East.Integer.printCompactSI(x));
   * });
   * const compiled = East.compile(formatSI.toIR(), []);
   * compiled(1500n);        // "1.5k"
   * compiled(2500000n);     // "2.5M"
   * compiled(3140000000n);  // "3.14G"
   * ```
   */
  printCompactSI: Expr.function([IntegerType], StringType, ($, x) => {
    const y = $.let(x);

    const negative = $.let(false);
    $.if(Expr.less(y, 0n), $ => {
      $.if(Expr.equal(y, -9223372036854775808n), $ => $.return("-9.22E")); // cannot negate -2^63 as an i64

      $.assign(negative, true);
      $.assign(y, y.negate());
    })

    $.if(Expr.less(y, 1000n), $ => $.return(negative.ifElse(() => Expr.str`-${y}`, () => Expr.str`${y}`)))

    const scale = $.let(1n);
    $.while(Expr.greaterEqual(y, 1000000n), $ => {
      $.assign(y, y.divide(1000n));
      $.assign(scale, scale.add(1n));
    });

    const suffix = $.let(Expr.equal(scale, 1n).ifElse(() => "k", () => Expr.equal(scale, 2n).ifElse(() => "M", () => Expr.equal(scale, 3n).ifElse(() => "G", () => Expr.equal(scale, 4n).ifElse(() => "T", () => Expr.equal(scale, 5n).ifElse(() => "P", () => "E"))))));

    $.if(Expr.greaterEqual(y, 100000n), $ => $.if(
      negative,
      $ => $.return(Expr.str`-${y.divide(1000n)}${suffix}`)
    ).else(
      $ => $.return(Expr.str`${y.divide(1000n)}${suffix}`)
    ));

    $.if(Expr.greaterEqual(y, 10000n), $ => {
      const part = $.let(y.divide(100n).remainder(10n));

      $.if(
        negative,
        $ => $.return(Expr.str`-${y.divide(1000n)}.${part}${suffix}`)
      ).else(
        $ => $.return(Expr.str`${y.divide(1000n)}.${part}${suffix}`)
      );
    })

    const part = $.let(y.divide(10n).remainder(100n));
    $.if(
      Expr.greaterEqual(part, 10n),
      $ => {
        $.if(
          negative,
          $ => $.return(Expr.str`-${y.divide(1000n)}.${part}${suffix}`)
        ).else(
          $ => $.return(Expr.str`${y.divide(1000n)}.${part}${suffix}`)
        );
      }
    ).else(
      $ => {
        $.if(
          negative,
          $ => $.return(Expr.str`-${y.divide(1000n)}.0${part}${suffix}`)
        ).else(
          $ => $.return(Expr.str`${y.divide(1000n)}.0${part}${suffix}`)
        );
      }
    );
  }),

  /**
   * Formats an integer in compact form with binary computing unit suffixes.
   *
   * Uses binary (base-1024) suffixes: ki (kibi, 1024), Mi (mebi, 1024²), Gi (gibi, 1024³),
   * Ti (tebi, 1024⁴), Pi (pebi, 1024⁵), Ei (exbi, 1024⁶).
   * Displays up to 3 significant digits. Commonly used for memory and storage sizes.
   *
   * @param x - The integer value to format
   * @returns A compact formatted string with binary units (e.g., `"21.5ki"`, `"1.82Mi"`, `"314Gi"`)
   *
   * @example
   * ```ts
   * const formatComputing = East.function([IntegerType], StringType, ($, x) => {
   *   $.return(East.Integer.printCompactComputing(x));
   * });
   * const compiled = East.compile(formatComputing.toIR(), []);
   * compiled(1536n);       // "1.5ki"  (1536 bytes = 1.5 KiB)
   * compiled(2621440n);    // "2.5Mi"  (2.5 MiB)
   * compiled(3221225472n); // "3Gi"    (3 GiB)
   * ```
   */
  printCompactComputing: Expr.function([IntegerType], StringType, ($, x) => {
    const y = $.let(x);

    const negative = $.let(false);
    $.if(Expr.less(y, 0n), $ => {

      $.if(Expr.equal(y, -9223372036854775808n), $ => $.return("-7.99Ei")); // cannot negate -2^63 as an i64

      $.assign(negative, true);
      $.assign(y, y.negate());
    })

    $.if(Expr.less(y, 1000n), $ => $.return(negative.ifElse(() => Expr.str`-${y}`, () => Expr.str`${y}`)))

    const scale = $.let(1n);
    $.while(Expr.greaterEqual(y, 1048576n), $ => {
      $.assign(y, y.divide(1024n));
      $.assign(scale, scale.add(1n));
    });

    const suffix = $.let(Expr.equal(scale, 1n).ifElse(() => "ki", () => Expr.equal(scale, 2n).ifElse(() => "Mi", () => Expr.equal(scale, 3n).ifElse(() => "Gi", () => Expr.equal(scale, 4n).ifElse(() => "Ti", () => Expr.equal(scale, 5n).ifElse(() => "Pi", () => "Ei"))))));

    $.if(Expr.greaterEqual(y, 102400n), $ => $.if(
      negative,
      $ => $.return(Expr.str`-${y.divide(1024n)}${suffix}`)
    ).else(
      $ => $.return(Expr.str`${y.divide(1024n)}${suffix}`)
    ));

    $.if(Expr.greaterEqual(y, 10240n), $ => {
      const part = $.let(y.multiply(10n).divide(1024n).remainder(10n));

      $.if(
        negative,
        $ => $.return(Expr.str`-${y.divide(1024n)}.${part}${suffix}`)
      ).else(
        $ => $.return(Expr.str`${y.divide(1024n)}.${part}${suffix}`)
      );
    })

    const part = $.let(y.multiply(100n).divide(1024n).remainder(100n));
    $.if(
      Expr.greaterEqual(part, 10n),
      $ => {
        $.if(
          negative,
          $ => $.return(Expr.str`-${y.divide(1024n)}.${part}${suffix}`)
        ).else(
          $ => $.return(Expr.str`${y.divide(1024n)}.${part}${suffix}`)
        );
      }
    ).else(
      $ => {
        $.if(
          negative,
          $ => $.return(Expr.str`-${y.divide(1024n)}.0${part}${suffix}`)
        ).else(
          $ => $.return(Expr.str`${y.divide(1024n)}.0${part}${suffix}`)
        );
      }
    );
  }),

  /**
   * Formats an integer as an ordinal number.
   *
   * @param x - The integer value to format
   * @returns An ordinal string (e.g., `"1st"`, `"2nd"`, `"3rd"`, `"4th"`)
   *
   * @example
   * ```ts
   * const formatOrdinal = East.function([IntegerType], StringType, ($, x) => {
   *   $.return(East.Integer.printOrdinal(x));
   * });
   * const compiled = East.compile(formatOrdinal.toIR(), []);
   * compiled(1n);    // "1st"
   * compiled(2n);    // "2nd"
   * compiled(3n);    // "3rd"
   * compiled(11n);   // "11th"
   * compiled(21n);   // "21st"
   * compiled(112n);  // "112th"
   * ```
   */
  printOrdinal: Expr.function([IntegerType], StringType, ($, x) => {
    const abs_x = $.let(x.abs());
    const last_digit = $.let(abs_x.remainder(10n));
    const last_two_digits = $.let(abs_x.remainder(100n));

    // Special cases for 11th, 12th, 13th
    $.if(Expr.greaterEqual(last_two_digits, 11n).bitAnd(Expr.lessEqual(last_two_digits, 13n)), $ => {
      $.return(Expr.str`${x}th`);
    });
    
    $.if(
      Expr.equal(last_digit, 1n),
      $ => $.return(Expr.str`${x}st`)
    ).else(
      $ => {
        $.if(
          Expr.equal(last_digit, 2n),
          $ => $.return(Expr.str`${x}nd`)
        ).else(
          $ => {
            $.if(
              Expr.equal(last_digit, 3n),
              $ => $.return(Expr.str`${x}rd`)
            ).else(
              $ => $.return(Expr.str`${x}th`)
            );
          }
        );
      }
    );
  }),

  /**
   * Counts the number of decimal digits in an integer (excluding the sign).
   *
   * @param x - The integer value
   * @returns The number of digits in the absolute value of `x`
   *
   * @example
   * ```ts
   * const countDigits = East.function([IntegerType], IntegerType, ($, x) => {
   *   $.return(East.Integer.digitCount(x));
   * });
   * const compiled = East.compile(countDigits.toIR(), []);
   * compiled(0n);       // 1n
   * compiled(42n);      // 2n
   * compiled(-1234n);   // 4n
   * compiled(1000000n); // 7n
   * ```
   */
  digitCount: Expr.function([IntegerType], IntegerType, ($, x) => {
    $.if(Expr.equal(x, 0n), $ => $.return(1n));
    $.return(x.abs().log(10n).add(1n));
  }),

  /**
   * Rounds an integer to the nearest multiple of a step value.
   *
   * @param x - The integer value to round
   * @param step - The step value to round to (uses absolute value)
   * @returns The nearest multiple of `step`, with ties rounding away from zero
   *
   * @example
   * ```ts
   * const roundNearest = East.function([IntegerType, IntegerType], IntegerType, ($, x, step) => {
   *   $.return(East.Integer.roundNearest(x, step));
   * });
   * const compiled = East.compile(roundNearest.toIR(), []);
   * compiled(17n, 5n);   // 15n
   * compiled(18n, 5n);   // 20n
   * compiled(-17n, 5n);  // -15n
   * ```
   */
  roundNearest: Expr.function([IntegerType, IntegerType], IntegerType, ($, x, step) => {
    // For step = 0, return original value
    $.if(Expr.equal(step, 0n), $ => $.return(x));

    const abs_step = $.let(step.abs());
    const abs_x = $.let(x.abs());
    const remainder = $.let(abs_x.remainder(abs_step));
    const half_step = $.let(abs_step.divide(2n));
    
    $.if(
      Expr.equal(remainder, 0n),
      $ => $.return(x) // Already a multiple
    ).else(
      $ => {
        const rounded_abs = $.let(
          Expr.less(remainder, half_step)
            .ifElse(
              () => abs_x.subtract(remainder), // Round down
              () => abs_x.add(abs_step.subtract(remainder)) // Round up
            )
        );
        
        $.if(
          Expr.greaterEqual(x, 0n),
          $ => $.return(rounded_abs)
        ).else(
          $ => $.return(rounded_abs.negate())
        );
      }
    );
  }),

  /**
   * Rounds an integer up to the next multiple of a step value (ceiling).
   *
   * @param x - The integer value to round
   * @param step - The step value to round to (uses absolute value)
   * @returns The smallest multiple of `step` greater than or equal to `x`
   *
   * @example
   * ```ts
   * const roundUp = East.function([IntegerType, IntegerType], IntegerType, ($, x, step) => {
   *   $.return(East.Integer.roundUp(x, step));
   * });
   * const compiled = East.compile(roundUp.toIR(), []);
   * compiled(17n, 5n);   // 20n
   * compiled(15n, 5n);   // 15n (already exact)
   * compiled(-17n, 5n);  // -15n (towards zero for negatives)
   * ```
   */
  roundUp: Expr.function([IntegerType, IntegerType], IntegerType, ($, x, step) => {
    // For step = 0, return original value
    $.if(Expr.equal(step, 0n), $ => $.return(x));

    const abs_step = $.let(step.abs());
    const remainder = $.let(x.remainder(abs_step));
    
    $.if(
      Expr.equal(remainder, 0n),
      $ => $.return(x) // Already a multiple
    ).else(
      $ => {
        $.if(Expr.greaterEqual(x, 0n),
          $ => $.return(x.add(abs_step.subtract(remainder))) // Positive: round up
        ).else(
          $ => $.return(x.subtract(remainder)) // Negative: round towards zero
        );
      }
    );
  }),

  /**
   * Rounds an integer down to the previous multiple of a step value (floor).
   *
   * @param x - The integer value to round
   * @param step - The step value to round to (uses absolute value)
   * @returns The largest multiple of `step` less than or equal to `x`
   *
   * @example
   * ```ts
   * const roundDown = East.function([IntegerType, IntegerType], IntegerType, ($, x, step) => {
   *   $.return(East.Integer.roundDown(x, step));
   * });
   * const compiled = East.compile(roundDown.toIR(), []);
   * compiled(17n, 5n);   // 15n
   * compiled(15n, 5n);   // 15n (already exact)
   * compiled(-17n, 5n);  // -20n (away from zero for negatives)
   * ```
   */
  roundDown: Expr.function([IntegerType, IntegerType], IntegerType, ($, x, step) => {
    // For step = 0, return original value
    $.if(Expr.equal(step, 0n), $ => $.return(x));

    const abs_step = $.let(step.abs());
    const remainder = $.let(x.remainder(abs_step));
    
    $.if(
      Expr.equal(remainder, 0n),
      $ => $.return(x) // Already a multiple
    ).else(
      $ => {
        $.if(
          Expr.greaterEqual(x, 0n),
          $ => $.return(x.subtract(remainder)) // Positive: round down
        ).else(
          $ => $.return(x.subtract(abs_step.add(remainder))) // Negative: round away from zero
        );
      }
    );
  }),

  /**
   * Rounds an integer towards zero to the nearest multiple of a step value (truncate).
   *
   * @param x - The integer value to round
   * @param step - The step value to round to (uses absolute value)
   * @returns The multiple of `step` closest to zero that is between zero and `x`
   *
   * @example
   * ```ts
   * const roundTruncate = East.function([IntegerType, IntegerType], IntegerType, ($, x, step) => {
   *   $.return(East.Integer.roundTruncate(x, step));
   * });
   * const compiled = East.compile(roundTruncate.toIR(), []);
   * compiled(17n, 5n);   // 15n
   * compiled(-17n, 5n);  // -15n
   * compiled(3n, 5n);    // 0n
   * ```
   */
  roundTruncate: Expr.function([IntegerType, IntegerType], IntegerType, ($, x, step) => {
    // For step = 0, return original value
    $.if(Expr.equal(step, 0n), $ => $.return(x));

    const abs_step = $.let(step.abs());
    const remainder = $.let(x.remainder(abs_step));

    $.if(
      Expr.equal(remainder, 0n),
      $ => $.return(x) // Already a multiple
    ).else(
      $ => $.return(x.subtract(remainder)) // Always subtract remainder (towards zero)
    );
  }),

  /**
   * Formats an integer as a percentage.
   *
   * @param x - The integer value to format
   * @returns A formatted percentage string (e.g., `"45%"`)
   *
   * @example
   * ```ts
   * const formatPercent = East.function([IntegerType], StringType, ($, x) => {
   *   $.return(East.Integer.printPercentage(x));
   * });
   * const compiled = East.compile(formatPercent.toIR(), []);
   * compiled(45n);   // "45%"
   * compiled(100n);  // "100%"
   * compiled(-25n);  // "-25%"
   * ```
   */
  printPercentage: Expr.function([IntegerType], StringType, ($, x) => {
    $.return(Expr.str`${x}%`);
  }),
}