"""Data loading and validation module.

Handles loading CSV/Excel files, detecting column types, and data quality checks.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

import pandas as pd
import numpy as np


class ColumnType(Enum):
    """Column data types."""
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    MIXED = "mixed"
    UNKNOWN = "unknown"


@dataclass
class ValidationResult:
    """Data validation results."""
    is_valid: bool
    total_rows: int
    total_columns: int
    missing_values: Dict[str, int]
    missing_percentage: Dict[str, float]
    column_types: Dict[str, ColumnType]
    warnings: List[str]
    errors: List[str]

    def has_issues(self) -> bool:
        """Check if there are any warnings or errors."""
        return len(self.warnings) > 0 or len(self.errors) > 0


def load_data(
    file_path: str,
    sheet_name: Union[str, int] = 0,
    encoding: str = 'utf-8',
    **kwargs
) -> pd.DataFrame:
    """Load data from CSV or Excel file.

    Args:
        file_path: Path to the data file
        sheet_name: Sheet name or index for Excel files (default: 0)
        encoding: File encoding for CSV files (default: 'utf-8')
        **kwargs: Additional arguments passed to pandas read functions

    Returns:
        Loaded DataFrame

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == '.csv':
        df = pd.read_csv(file_path, encoding=encoding, **kwargs)
    elif suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. "
            "Supported formats: .csv, .xlsx, .xls"
        )

    # Basic cleanup
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include=['object']).columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    return df


def detect_column_types(
    df: pd.DataFrame,
    numeric_threshold: float = 0.8
) -> Dict[str, ColumnType]:
    """Detect column types automatically.

    Args:
        df: Input DataFrame
        numeric_threshold: Ratio of non-null numeric values to consider column numeric

    Returns:
        Dictionary mapping column names to their detected types
    """
    column_types = {}

    for col in df.columns:
        series = df[col]

        # Skip completely empty columns
        if series.isna().all():
            column_types[col] = ColumnType.UNKNOWN
            continue

        # Get non-null values for type detection
        non_null = series.dropna()

        if len(non_null) == 0:
            column_types[col] = ColumnType.UNKNOWN
            continue

        # Check if boolean (already boolean type or only 0/1 values)
        if pd.api.types.is_bool_dtype(series):
            column_types[col] = ColumnType.BOOLEAN
            continue

        # Check for numeric type
        if pd.api.types.is_numeric_dtype(series):
            column_types[col] = ColumnType.NUMERIC
            continue

        # Try to convert to numeric for object dtype
        if series.dtype == 'object':
            # Try numeric conversion
            numeric_converted = pd.to_numeric(non_null, errors='coerce')
            numeric_ratio = numeric_converted.notna().sum() / len(non_null)

            if numeric_ratio >= numeric_threshold:
                column_types[col] = ColumnType.NUMERIC
                continue

            # Try datetime conversion
            try:
                pd.to_datetime(non_null, errors='coerce')
                datetime_converted = pd.to_datetime(non_null, errors='coerce')
                datetime_ratio = datetime_converted.notna().sum() / len(non_null)

                if datetime_ratio >= numeric_threshold:
                    column_types[col] = ColumnType.DATETIME
                    continue
            except Exception:
                pass

            # Check cardinality for categorical
            unique_ratio = non_null.nunique() / len(non_null)

            if unique_ratio < 0.5 or non_null.nunique() <= 20:
                column_types[col] = ColumnType.CATEGORICAL
            else:
                # Might be text data
                column_types[col] = ColumnType.CATEGORICAL

    return column_types


def validate_data(df: pd.DataFrame) -> ValidationResult:
    """Validate data and check for quality issues.

    Args:
        df: Input DataFrame

    Returns:
        ValidationResult with detailed information
    """
    total_rows = len(df)
    total_columns = len(df.columns)

    # Detect column types
    column_types = detect_column_types(df)

    # Check missing values
    missing_values = {}
    missing_percentage = {}

    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_values[col] = missing_count
        missing_percentage[col] = (missing_count / total_rows * 100) if total_rows > 0 else 0

    # Generate warnings and errors
    warnings = []
    errors = []

    # Check for high missing value ratios
    for col, pct in missing_percentage.items():
        if pct > 50:
            warnings.append(
                f"Column '{col}' has {pct:.1f}% missing values "
                f"({missing_values[col]}/{total_rows} rows)"
            )
        elif pct > 20:
            warnings.append(
                f"Column '{col}' has {pct:.1f}% missing values "
                f"({missing_values[col]}/{total_rows} rows)"
            )

    # Check for empty columns
    for col in df.columns:
        if df[col].isna().all():
            errors.append(f"Column '{col}' is completely empty")

    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        warnings.append(
            f"Found {duplicates} duplicate rows "
            f"({duplicates/total_rows*100:.1f}% of data)"
        )

    # Check for numeric columns with potential issues
    numeric_cols = [col for col, ctype in column_types.items() if ctype == ColumnType.NUMERIC]
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors='coerce')

        # Check for infinite values
        if np.isinf(series).any():
            inf_count = np.isinf(series).sum()
            warnings.append(
                f"Column '{col}' contains {inf_count} infinite values"
            )

        # Check for very large range (potential data quality issue)
        if series.notna().any():
            col_range = series.max() - series.min()
            if col_range > 0:
                cv = series.std() / series.mean() if series.mean() != 0 else 0
                if abs(cv) > 10:
                    warnings.append(
                        f"Column '{col}' has very high variability "
                        f"(CV={cv:.2f})"
                    )

    # Check for constant columns
    for col in df.columns:
        if df[col].notna().nunique() <= 1 and df[col].notna().any():
            warnings.append(
                f"Column '{col}' has only one unique value "
                f"(constant column)"
            )

    is_valid = len(errors) == 0

    return ValidationResult(
        is_valid=is_valid,
        total_rows=total_rows,
        total_columns=total_columns,
        missing_values=missing_values,
        missing_percentage=missing_percentage,
        column_types=column_types,
        warnings=warnings,
        errors=errors
    )


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Get list of numeric column names.

    Args:
        df: Input DataFrame

    Returns:
        List of numeric column names
    """
    column_types = detect_column_types(df)
    return [col for col, ctype in column_types.items() if ctype == ColumnType.NUMERIC]


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Get list of categorical column names.

    Args:
        df: Input DataFrame

    Returns:
        List of categorical column names
    """
    column_types = detect_column_types(df)
    return [col for col, ctype in column_types.items() if ctype == ColumnType.CATEGORICAL]


def prepare_data_for_analysis(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Dict[str, ColumnType]]:
    """Prepare data for statistical analysis.

    Args:
        df: Input DataFrame
        columns: Optional list of columns to include

    Returns:
        Tuple of (cleaned DataFrame, column types dict)
    """
    # Select columns if specified
    if columns is not None:
        df = df[columns].copy()

    # Detect column types
    column_types = detect_column_types(df)

    # Convert numeric columns
    numeric_cols = [col for col, ctype in column_types.items() if ctype == ColumnType.NUMERIC]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df, column_types


def get_data_summary(df: pd.DataFrame) -> Dict:
    """Get a summary of the data.

    Args:
        df: Input DataFrame

    Returns:
        Dictionary with data summary information
    """
    validation = validate_data(df)

    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)

    return {
        'shape': (validation.total_rows, validation.total_columns),
        'numeric_columns': numeric_cols,
        'categorical_columns': categorical_cols,
        'column_types': validation.column_types,
        'missing_values': validation.missing_values,
        'missing_percentage': validation.missing_percentage,
        'has_issues': validation.has_issues(),
        'warnings': validation.warnings,
        'errors': validation.errors,
    }
