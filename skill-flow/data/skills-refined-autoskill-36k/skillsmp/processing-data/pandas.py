"""Pandas DataFrame tools for data manipulation.

Security Note:
    The create_pandas_dataframe and run_dataframe_operation functions use
    allowlists to prevent arbitrary code execution. Only explicitly allowed
    pandas functions and DataFrame methods can be called.
"""

from __future__ import annotations

from typing import Any

from src.humcp.decorator import tool

try:
    import pandas as pd
except ImportError as err:
    raise ImportError(
        "pandas is required for Pandas tools. Install with: pip install pandas"
    ) from err

# Allowlist of safe pandas module functions for creating DataFrames
_ALLOWED_CREATE_FUNCTIONS = frozenset(
    {
        "DataFrame",
        "read_csv",
        "read_json",
        "read_excel",
        "read_parquet",
        "read_feather",
        "read_orc",
        "read_html",
        "read_xml",
        "read_clipboard",
        "read_fwf",
        "read_table",
        "read_sql",
        "read_sql_query",
        "read_sql_table",
    }
)

# Allowlist of safe DataFrame operations (read-only or non-destructive)
_ALLOWED_DATAFRAME_OPERATIONS = frozenset(
    {
        # Inspection
        "head",
        "tail",
        "describe",
        "info",
        "dtypes",
        "columns",
        "index",
        "shape",
        "size",
        "ndim",
        "empty",
        "values",
        "memory_usage",
        "sample",
        # Selection
        "loc",
        "iloc",
        "at",
        "iat",
        "get",
        "xs",
        # Filtering and querying
        "query",
        "filter",
        "where",
        "mask",
        "isin",
        "between",
        "duplicated",
        "drop_duplicates",
        "nlargest",
        "nsmallest",
        # Sorting
        "sort_values",
        "sort_index",
        "rank",
        # Aggregation
        "sum",
        "mean",
        "median",
        "mode",
        "std",
        "var",
        "min",
        "max",
        "count",
        "nunique",
        "value_counts",
        "agg",
        "aggregate",
        "groupby",
        # Transformation
        "apply",
        "map",
        "transform",
        "pipe",
        "assign",
        "rename",
        "reset_index",
        "set_index",
        "reindex",
        "drop",
        "dropna",
        "fillna",
        "replace",
        "astype",
        "copy",
        "T",
        "transpose",
        # String operations
        "str",
        # Datetime operations
        "dt",
        # Combining
        "merge",
        "join",
        "concat",
        "append",
        # Reshaping
        "pivot",
        "pivot_table",
        "melt",
        "stack",
        "unstack",
        "explode",
        # Missing data
        "isna",
        "isnull",
        "notna",
        "notnull",
        # Conversion
        "to_dict",
        "to_list",
        "to_numpy",
        "to_string",
        "to_markdown",
        "to_records",
        "items",
        "iterrows",
        "itertuples",
        # Comparison
        "eq",
        "ne",
        "lt",
        "le",
        "gt",
        "ge",
        "equals",
        "compare",
        # Math operations
        "abs",
        "round",
        "clip",
        "corr",
        "cov",
        "cumsum",
        "cumprod",
        "cummax",
        "cummin",
        "diff",
        "pct_change",
    }
)

# Allowlist of safe export functions
_ALLOWED_EXPORT_FUNCTIONS = frozenset(
    {
        "to_csv",
        "to_json",
        "to_excel",
        "to_parquet",
        "to_feather",
        "to_html",
        "to_xml",
        "to_markdown",
        "to_string",
        "to_dict",
        "to_records",
        "to_clipboard",
        "to_latex",
    }
)


class DataFrameManager:
    """Manages pandas DataFrames in memory"""

    def __init__(self):
        self.dataframes: dict[str, pd.DataFrame] = {}

    def add_dataframe(self, name: str, df: pd.DataFrame) -> None:
        """Add a DataFrame to the manager"""
        self.dataframes[name] = df

    def get_dataframe(self, name: str) -> pd.DataFrame | None:
        """Get a DataFrame by name"""
        return self.dataframes.get(name)

    def remove_dataframe(self, name: str) -> bool:
        """Remove a DataFrame by name"""
        if name in self.dataframes:
            del self.dataframes[name]
            return True
        return False

    def list_dataframes(self) -> list:
        """List all DataFrame names"""
        return list(self.dataframes.keys())

    def dataframe_exists(self, name: str) -> bool:
        """Check if a DataFrame exists"""
        return name in self.dataframes


_dataframe_manager = None


def get_dataframe_manager():
    """Get the global DataFrame manager instance"""
    global _dataframe_manager
    if _dataframe_manager is None:
        _dataframe_manager = DataFrameManager()
    return _dataframe_manager


@tool()
async def create_pandas_dataframe(
    dataframe_name: str,
    create_using_function: str,
    function_parameters: dict[str, Any],
) -> dict:
    """
    Creates a pandas DataFrame by running a pandas function with specified parameters.
    The DataFrame is stored in memory and can be referenced by name in subsequent operations.

    Args:
        dataframe_name: The name to assign to the created DataFrame
        create_using_function: The pandas function to use (e.g., 'read_csv', 'read_json', 'DataFrame')
        function_parameters: Dictionary of parameters to pass to the pandas function

    Returns:
        Success status with the DataFrame name and info, or error message

    Examples:
        - Read CSV: {"dataframe_name": "csv_data", "create_using_function": "read_csv",
                     "function_parameters": {"filepath_or_buffer": "data.csv"}}
        - Read JSON: {"dataframe_name": "json_data", "create_using_function": "read_json",
                      "function_parameters": {"path_or_buf": "data.json"}}
        - Read Excel: {"dataframe_name": "excel_data", "create_using_function": "read_excel",
                       "function_parameters": {"io": "data.xlsx"}}
        - From dict: {"dataframe_name": "dict_data", "create_using_function": "DataFrame",
                      "function_parameters": {"data": {"col1": [1, 2], "col2": [3, 4]}}}
    """
    try:
        manager = get_dataframe_manager()

        # Check if dataframe already exists
        if manager.dataframe_exists(dataframe_name):
            return {
                "success": False,
                "error": f"DataFrame '{dataframe_name}' already exists. Use a different name or delete the existing one.",
            }

        # Validate function is in allowlist
        if create_using_function not in _ALLOWED_CREATE_FUNCTIONS:
            return {
                "success": False,
                "error": f"Function 'pd.{create_using_function}' is not allowed. "
                f"Allowed functions: {', '.join(sorted(_ALLOWED_CREATE_FUNCTIONS))}",
            }

        # Check if the function exists in pandas
        if not hasattr(pd, create_using_function):
            return {
                "success": False,
                "error": f"Function 'pd.{create_using_function}' does not exist in pandas",
            }

        # Create the dataframe
        dataframe = getattr(pd, create_using_function)(**function_parameters)

        # Validate the result
        if dataframe is None:
            return {
                "success": False,
                "error": f"Function returned None when creating DataFrame '{dataframe_name}'",
            }

        if not isinstance(dataframe, pd.DataFrame):
            return {
                "success": False,
                "error": f"Function did not return a DataFrame (got {type(dataframe).__name__})",
            }

        if dataframe.empty:
            return {
                "success": False,
                "error": f"Created DataFrame '{dataframe_name}' is empty",
            }

        # Store the dataframe
        manager.add_dataframe(dataframe_name, dataframe)

        # Get DataFrame info
        info = {
            "name": dataframe_name,
            "shape": dataframe.shape,
            "columns": list(dataframe.columns),
            "dtypes": {col: str(dtype) for col, dtype in dataframe.dtypes.items()},
            "memory_usage": dataframe.memory_usage(deep=True).sum(),
        }

        return {"success": True, "data": info}

    except Exception as e:
        return {"success": False, "error": f"Error creating DataFrame: {str(e)}"}


@tool()
async def run_dataframe_operation(
    dataframe_name: str,
    operation: str,
    operation_parameters: dict[str, Any] | None = None,
) -> dict:
    """
    Runs an operation on a stored pandas DataFrame with specified parameters.

    Args:
        dataframe_name: The name of the DataFrame to operate on
        operation: The DataFrame method to call (e.g., 'head', 'tail', 'describe', 'info')
        operation_parameters: Dictionary of parameters to pass to the operation (optional)

    Returns:
        Success status with the operation result as a string, or error message

    Examples:
        - First 5 rows: {"dataframe_name": "csv_data", "operation": "head", "operation_parameters": {"n": 5}}
        - Last 10 rows: {"dataframe_name": "csv_data", "operation": "tail", "operation_parameters": {"n": 10}}
        - Summary stats: {"dataframe_name": "csv_data", "operation": "describe", "operation_parameters": {}}
        - Column names: {"dataframe_name": "csv_data", "operation": "columns", "operation_parameters": {}}
        - Filter rows: {"dataframe_name": "csv_data", "operation": "query", "operation_parameters": {"expr": "age > 25"}}
    """
    try:
        if operation_parameters is None:
            operation_parameters = {}

        manager = get_dataframe_manager()

        # Get the dataframe
        dataframe = manager.get_dataframe(dataframe_name)
        if dataframe is None:
            return {
                "success": False,
                "error": f"DataFrame '{dataframe_name}' not found. Create it first using create_pandas_dataframe.",
            }

        # Validate operation is in allowlist
        if operation not in _ALLOWED_DATAFRAME_OPERATIONS:
            return {
                "success": False,
                "error": f"Operation '{operation}' is not allowed. "
                f"Use allowed operations like: head, tail, describe, query, etc.",
            }

        # Check if the operation exists
        if not hasattr(dataframe, operation):
            return {
                "success": False,
                "error": f"Operation '{operation}' does not exist on DataFrame",
            }

        # Run the operation
        result = getattr(dataframe, operation)
        # Handle both method calls and property access
        if callable(result):
            result = result(**operation_parameters)
        elif operation_parameters:
            return {
                "success": False,
                "error": f"Operation '{operation}' is a property and does not accept parameters",
            }

        # Convert result to string representation
        try:
            if isinstance(result, pd.DataFrame):
                result_str = result.to_string()
            elif isinstance(result, pd.Series):
                result_str = result.to_string()
            elif isinstance(result, pd.Index):
                result_str = str(list(result))
            else:
                result_str = str(result)
        except Exception:
            result_str = "Operation completed successfully (result could not be converted to string)"

        return {
            "success": True,
            "data": {
                "operation": operation,
                "dataframe": dataframe_name,
                "result": result_str,
            },
        }

    except Exception as e:
        return {"success": False, "error": f"Error running operation: {str(e)}"}


@tool()
async def list_dataframes() -> dict:
    """
    List all DataFrames currently stored in memory.

    Returns:
        Success status with list of DataFrame names and their basic info
    """
    try:
        manager = get_dataframe_manager()
        dataframe_names = manager.list_dataframes()

        dataframes_info = []
        for name in dataframe_names:
            df = manager.get_dataframe(name)
            if df is not None:
                dataframes_info.append(
                    {
                        "name": name,
                        "shape": df.shape,
                        "columns": list(df.columns),
                        "memory_usage_bytes": df.memory_usage(deep=True).sum(),
                    }
                )

        return {"success": True, "data": dataframes_info, "count": len(dataframes_info)}

    except Exception as e:
        return {"success": False, "error": str(e)}


@tool()
async def get_dataframe_info(dataframe_name: str) -> dict:
    """
    Get detailed information about a specific DataFrame.

    Args:
        dataframe_name: The name of the DataFrame

    Returns:
        Success status with detailed DataFrame information
    """
    try:
        manager = get_dataframe_manager()
        dataframe = manager.get_dataframe(dataframe_name)

        if dataframe is None:
            return {
                "success": False,
                "error": f"DataFrame '{dataframe_name}' not found",
            }

        info = {
            "name": dataframe_name,
            "shape": dataframe.shape,
            "columns": list(dataframe.columns),
            "dtypes": {col: str(dtype) for col, dtype in dataframe.dtypes.items()},
            "memory_usage_bytes": dataframe.memory_usage(deep=True).sum(),
            "null_counts": dataframe.isnull().sum().to_dict(),
            "sample_data": dataframe.head().to_dict(orient="records"),
        }

        return {"success": True, "data": info}

    except Exception as e:
        return {"success": False, "error": str(e)}


@tool()
async def delete_dataframe(dataframe_name: str) -> dict:
    """
    Delete a DataFrame from memory.

    Args:
        dataframe_name: The name of the DataFrame to delete

    Returns:
        Success status with confirmation message
    """
    try:
        manager = get_dataframe_manager()

        if not manager.dataframe_exists(dataframe_name):
            return {
                "success": False,
                "error": f"DataFrame '{dataframe_name}' not found",
            }

        manager.remove_dataframe(dataframe_name)

        return {
            "success": True,
            "data": {"message": f"DataFrame '{dataframe_name}' deleted successfully"},
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@tool()
async def export_dataframe(
    dataframe_name: str,
    export_function: str,
    export_parameters: dict[str, Any],
) -> dict:
    """
    Export a DataFrame using pandas export functions (to_csv, to_json, to_excel, etc.).

    Args:
        dataframe_name: The name of the DataFrame to export
        export_function: The pandas export method to use (e.g., 'to_csv', 'to_json', 'to_excel')
        export_parameters: Dictionary of parameters to pass to the export function

    Returns:
        Success status with export confirmation

    Examples:
        - To CSV: {"dataframe_name": "data", "export_function": "to_csv",
                   "export_parameters": {"path_or_buf": "output.csv", "index": False}}
        - To JSON: {"dataframe_name": "data", "export_function": "to_json",
                    "export_parameters": {"path_or_buf": "output.json", "orient": "records"}}
        - To Excel: {"dataframe_name": "data", "export_function": "to_excel",
                     "export_parameters": {"excel_writer": "output.xlsx", "index": False}}
    """
    try:
        manager = get_dataframe_manager()
        dataframe = manager.get_dataframe(dataframe_name)

        if dataframe is None:
            return {
                "success": False,
                "error": f"DataFrame '{dataframe_name}' not found",
            }

        # Validate export function is in allowlist
        if export_function not in _ALLOWED_EXPORT_FUNCTIONS:
            return {
                "success": False,
                "error": f"Export function '{export_function}' is not allowed. "
                f"Allowed functions: {', '.join(sorted(_ALLOWED_EXPORT_FUNCTIONS))}",
            }

        # Check if the export function exists
        if not hasattr(dataframe, export_function):
            return {
                "success": False,
                "error": f"Export function '{export_function}' does not exist on DataFrame",
            }

        # Run the export
        getattr(dataframe, export_function)(**export_parameters)

        # Get the output path if available
        output_path = (
            export_parameters.get("path_or_buf")
            or export_parameters.get("excel_writer")
            or "output"
        )

        return {
            "success": True,
            "data": {
                "message": f"DataFrame '{dataframe_name}' exported successfully",
                "output": str(output_path),
                "function": export_function,
            },
        }

    except Exception as e:
        return {"success": False, "error": f"Error exporting DataFrame: {str(e)}"}
