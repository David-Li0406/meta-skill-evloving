"""
Data Validation Script

Validates data file format and structure. Reads parameters from JSON stdin
and outputs validation results as JSON.

Parameters:
    file_path (str, required): Path to the data file to validate
    format (str, optional): Expected data format (csv, json, parquet)
"""

import json
import os
import sys
from typing import Any


def detect_format(file_path: str) -> str:
    """Detect file format from extension."""
    ext = os.path.splitext(file_path)[1].lower()
    format_map = {
        '.csv': 'csv',
        '.json': 'json',
        '.parquet': 'parquet',
        '.xlsx': 'excel',
        '.xls': 'excel',
    }
    return format_map.get(ext, 'unknown')


def validate_csv(file_path: str) -> dict:
    """Validate CSV file structure."""
    import csv
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        
        if header is None:
            return {'valid': False, 'error': 'Empty CSV file'}
        
        row_count = 1
        column_count = len(header)
        
        for row in reader:
            row_count += 1
            if len(row) != column_count:
                return {
                    'valid': False,
                    'error': f'Inconsistent column count at row {row_count}'
                }
        
        return {
            'valid': True,
            'format': 'csv',
            'columns': header,
            'column_count': column_count,
            'row_count': row_count,
        }


def validate_json(file_path: str) -> dict:
    """Validate JSON file structure."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        if len(data) == 0:
            return {'valid': True, 'format': 'json', 'record_count': 0, 'columns': []}
        
        if isinstance(data[0], dict):
            columns = list(data[0].keys())
            return {
                'valid': True,
                'format': 'json',
                'record_count': len(data),
                'columns': columns,
                'column_count': len(columns),
            }
        else:
            return {'valid': True, 'format': 'json', 'record_count': len(data), 'type': 'array'}
    
    elif isinstance(data, dict):
        return {
            'valid': True,
            'format': 'json',
            'keys': list(data.keys()),
            'type': 'object',
        }
    
    return {'valid': True, 'format': 'json', 'type': type(data).__name__}


def validate_parquet(file_path: str) -> dict:
    """Validate Parquet file structure."""
    try:
        import pyarrow.parquet as pq
    except ImportError:
        return {'valid': False, 'error': 'pyarrow not installed'}
    
    parquet_file = pq.ParquetFile(file_path)
    schema = parquet_file.schema_arrow
    metadata = parquet_file.metadata
    
    return {
        'valid': True,
        'format': 'parquet',
        'columns': [field.name for field in schema],
        'column_count': len(schema),
        'row_count': metadata.num_rows,
        'row_groups': metadata.num_row_groups,
    }


def validate_file(file_path: str, expected_format: str | None = None) -> dict:
    """Validate a data file."""
    # Check file exists
    if not os.path.exists(file_path):
        return {'valid': False, 'error': f'File not found: {file_path}'}
    
    if not os.path.isfile(file_path):
        return {'valid': False, 'error': f'Not a file: {file_path}'}
    
    # Detect format
    detected_format = detect_format(file_path)
    
    # Check format mismatch
    if expected_format and detected_format != expected_format:
        return {
            'valid': False,
            'error': f'Format mismatch: expected {expected_format}, detected {detected_format}'
        }
    
    # Validate based on format
    validators = {
        'csv': validate_csv,
        'json': validate_json,
        'parquet': validate_parquet,
    }
    
    validator = validators.get(detected_format)
    if validator is None:
        return {'valid': False, 'error': f'Unsupported format: {detected_format}'}
    
    return validator(file_path)


def execute(data: dict[str, Any]) -> dict[str, Any]:
    """Execute the validation script (native mode entry point)."""
    file_path = data.get('file_path')
    if not file_path:
        return {'valid': False, 'error': 'file_path parameter is required'}
    
    expected_format = data.get('format')
    
    try:
        result = validate_file(file_path, expected_format)
        return result
    except Exception as e:
        return {'valid': False, 'error': str(e)}


if __name__ == '__main__':
    # Read parameters from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({'valid': False, 'error': f'Invalid JSON input: {e}'}))
        sys.exit(1)
    
    result = execute(input_data)
    print(json.dumps(result, indent=2))

