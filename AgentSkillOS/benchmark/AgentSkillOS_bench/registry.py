"""
Evaluator function registry and decorator.
"""
from typing import Callable, Dict, Tuple, Any
from functools import wraps

# Global registry for evaluator functions
EVALUATOR_REGISTRY: Dict[str, Callable] = {}


def evaluator(name: str):
    """
    Decorator to register an evaluator function.

    All evaluator functions must have the signature:
        async def func(workspace: Path, op_args: Dict, value: Any = None, **kwargs) -> Tuple[bool, str]

    Returns:
        Tuple[bool, str]: (passed, error_message)

    Example:
        @evaluator("file_exists")
        async def eval_file_exists(workspace, op_args, **kwargs):
            path = op_args["path"]
            if (workspace / path).exists():
                return True, ""
            return False, f"File not found: {path}"
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                # Handle both sync and async functions
                if hasattr(result, '__await__'):
                    return await result
                return result
            except Exception as e:
                return False, f"Evaluator error: {str(e)}"

        # Register the function
        EVALUATOR_REGISTRY[name] = wrapper
        wrapper._evaluator_name = name
        return wrapper

    return decorator


def get_evaluator(name: str) -> Callable:
    """Get an evaluator function by name."""
    if name not in EVALUATOR_REGISTRY:
        raise KeyError(f"Unknown evaluator: {name}. Available: {list(EVALUATOR_REGISTRY.keys())}")
    return EVALUATOR_REGISTRY[name]


def list_evaluators() -> Dict[str, str]:
    """List all registered evaluators with their docstrings."""
    return {
        name: func.__doc__ or "No description"
        for name, func in EVALUATOR_REGISTRY.items()
    }


def register_evaluator(name: str, func: Callable) -> None:
    """Manually register an evaluator function."""
    EVALUATOR_REGISTRY[name] = func
