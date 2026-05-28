from __future__ import annotations

import math
from typing import Any

from src.humcp.decorator import tool


def _ok(data: dict[str, Any]) -> dict:
    return {"success": True, "data": data}


def _err(msg: str) -> dict:
    return {"success": False, "error": msg}


@tool()
async def add(a: float, b: float) -> dict:
    """Add two numbers."""
    return _ok({"operation": "add", "a": a, "b": b, "result": a + b})


@tool()
async def subtract(a: float, b: float) -> dict:
    """Subtract b from a."""
    return _ok({"operation": "subtract", "a": a, "b": b, "result": a - b})


@tool()
async def multiply(a: float, b: float) -> dict:
    """Multiply two numbers."""
    return _ok({"operation": "multiply", "a": a, "b": b, "result": a * b})


@tool()
async def divide(a: float, b: float) -> dict:
    """Divide a by b."""
    if b == 0:
        return _err("Division by zero")
    return _ok({"operation": "divide", "a": a, "b": b, "result": a / b})


@tool()
async def exponentiate(a: float, b: float) -> dict:
    """Raise a to the power of b."""
    try:
        result = math.pow(a, b)
    except (OverflowError, ValueError) as exc:
        return _err(f"Error computing power: {exc}")
    return _ok({"operation": "power", "a": a, "b": b, "result": result})


@tool()
async def factorial(n: int) -> dict:
    """Calculate factorial of n (must be non-negative)."""
    if n < 0:
        return _err("Factorial undefined for negative numbers")
    try:
        result = math.factorial(n)
    except (OverflowError, MemoryError):
        return _err("Factorial result too large to compute")
    return _ok({"operation": "factorial", "n": n, "result": result})


@tool()
async def is_prime(n: int) -> dict:
    """Check if n is prime."""
    if n <= 1:
        return _ok({"n": n, "is_prime": False})
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return _ok({"n": n, "is_prime": False, "divisible_by": i})
    return _ok({"n": n, "is_prime": True})


@tool()
async def square_root(n: float) -> dict:
    """Calculate square root of n (must be non-negative)."""
    if n < 0:
        return _err("Square root undefined for negative numbers")
    return _ok({"operation": "sqrt", "n": n, "result": math.sqrt(n)})


@tool()
async def absolute_value(n: float) -> dict:
    """Calculate absolute value of n."""
    return _ok({"operation": "abs", "n": n, "result": abs(n)})


@tool()
async def logarithm(n: float, base: float = 0) -> dict:
    """Calculate logarithm of n. Base defaults to e (natural log) if 0."""
    if n <= 0:
        return _err("Logarithm undefined for non-positive numbers")
    if base == 0:
        return _ok({"operation": "ln", "n": n, "result": math.log(n)})
    if base <= 0 or base == 1:
        return _err("Base must be positive and not 1")
    return _ok({"operation": "log", "n": n, "base": base, "result": math.log(n, base)})


@tool()
async def modulo(a: float, b: float) -> dict:
    """Calculate a modulo b."""
    if b == 0:
        return _err("Modulo by zero")
    return _ok({"operation": "mod", "a": a, "b": b, "result": a % b})


@tool()
async def greatest_common_divisor(a: int, b: int) -> dict:
    """Calculate GCD of a and b."""
    try:
        result = math.gcd(a, b)
    except Exception as e:
        return _err(f"GCD error: {e}")
    return _ok({"operation": "gcd", "a": a, "b": b, "result": result})
