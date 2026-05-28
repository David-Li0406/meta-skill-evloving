#!/usr/bin/env python3
"""
Big Number Calculator - Handles arbitrary precision integer arithmetic.
Uses Python's native arbitrary precision integers.
"""

import sys
import math
from typing import Union


def add(a: str, b: str) -> str:
    """Add two big integers."""
    return str(int(a) + int(b))


def subtract(a: str, b: str) -> str:
    """Subtract b from a."""
    return str(int(a) - int(b))


def multiply(a: str, b: str) -> str:
    """Multiply two big integers."""
    return str(int(a) * int(b))


def divide(a: str, b: str) -> str:
    """Integer division of a by b."""
    if int(b) == 0:
        raise ValueError("Division by zero")
    return str(int(a) // int(b))


def modulo(a: str, b: str) -> str:
    """Modulo operation: a mod b."""
    if int(b) == 0:
        raise ValueError("Modulo by zero")
    return str(int(a) % int(b))


def power(base: str, exp: str) -> str:
    """Compute base^exp for non-negative exponent."""
    e = int(exp)
    if e < 0:
        raise ValueError("Negative exponent not supported for integer power")
    return str(int(base) ** e)


def factorial(n: str) -> str:
    """Compute n! for non-negative integer n."""
    num = int(n)
    if num < 0:
        raise ValueError("Factorial not defined for negative numbers")
    return str(math.factorial(num))


def gcd(a: str, b: str) -> str:
    """Compute greatest common divisor of a and b."""
    return str(math.gcd(int(a), int(b)))


def lcm(a: str, b: str) -> str:
    """Compute least common multiple of a and b."""
    ia, ib = int(a), int(b)
    if ia == 0 or ib == 0:
        return "0"
    return str(abs(ia * ib) // math.gcd(ia, ib))


def is_prime(n: str) -> bool:
    """Check if n is a prime number (for reasonably sized numbers)."""
    num = int(n)
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True


def digit_count(n: str) -> int:
    """Return the number of digits in n."""
    num = int(n)
    if num == 0:
        return 1
    return len(str(abs(num)))


def digit_sum(n: str) -> str:
    """Return the sum of digits of n."""
    num = abs(int(n))
    return str(sum(int(d) for d in str(num)))


def fibonacci(n: str) -> str:
    """Compute the n-th Fibonacci number (0-indexed)."""
    num = int(n)
    if num < 0:
        raise ValueError("Fibonacci not defined for negative indices")
    if num == 0:
        return "0"
    if num == 1:
        return "1"
    a, b = 0, 1
    for _ in range(2, num + 1):
        a, b = b, a + b
    return str(b)


def binomial(n: str, k: str) -> str:
    """Compute binomial coefficient C(n, k)."""
    return str(math.comb(int(n), int(k)))


def format_result(result: str, scientific: bool = False) -> str:
    """Format result, optionally in scientific notation."""
    if not scientific:
        return result
    num = int(result)
    if num == 0:
        return "0"
    sign = "-" if num < 0 else ""
    num = abs(num)
    s = str(num)
    if len(s) <= 10:
        return result
    return f"{sign}{s[0]}.{s[1:10]}e{len(s)-1}"


OPERATIONS = {
    "add": (add, 2, "Add two numbers: a + b"),
    "sub": (subtract, 2, "Subtract: a - b"),
    "mul": (multiply, 2, "Multiply: a * b"),
    "div": (divide, 2, "Integer division: a // b"),
    "mod": (modulo, 2, "Modulo: a % b"),
    "pow": (power, 2, "Power: base^exp"),
    "fact": (factorial, 1, "Factorial: n!"),
    "gcd": (gcd, 2, "Greatest common divisor"),
    "lcm": (lcm, 2, "Least common multiple"),
    "prime": (lambda n: str(is_prime(n)), 1, "Check if prime"),
    "digits": (lambda n: str(digit_count(n)), 1, "Count digits"),
    "digitsum": (digit_sum, 1, "Sum of digits"),
    "fib": (fibonacci, 1, "Fibonacci number"),
    "binomial": (binomial, 2, "Binomial coefficient C(n,k)"),
}


def main():
    if len(sys.argv) < 2:
        print("Big Number Calculator")
        print("Usage: bignum_calc.py <operation> <args...>")
        print("\nOperations:")
        for op, (_, argc, desc) in OPERATIONS.items():
            print(f"  {op}: {desc}")
        sys.exit(0)

    op = sys.argv[1].lower()

    if op not in OPERATIONS:
        print(f"Unknown operation: {op}")
        print(f"Available: {', '.join(OPERATIONS.keys())}")
        sys.exit(1)

    func, argc, _ = OPERATIONS[op]
    args = sys.argv[2:2+argc]

    if len(args) < argc:
        print(f"Error: {op} requires {argc} argument(s)")
        sys.exit(1)

    try:
        result = func(*args)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
