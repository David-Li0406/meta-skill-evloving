#!/usr/bin/env python3
"""
Error Analysis Helper Script

This script helps analyze Python stack traces and provide structured error information.
It can parse stack traces from files or stdin and categorize errors.
"""

import re
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ErrorInfo:
    """Structured information about an error."""
    error_type: str
    error_message: str
    file_path: Optional[str]
    line_number: Optional[int]
    function_name: Optional[str]
    stack_trace: List[str]
    category: str


class ErrorAnalyzer:
    """Analyzes Python errors and provides categorization."""
    
    ERROR_CATEGORIES = {
        'ImportError': 'Import/Dependency',
        'ModuleNotFoundError': 'Import/Dependency',
        'TypeError': 'Type',
        'AttributeError': 'Attribute/Name',
        'NameError': 'Attribute/Name',
        'IndexError': 'Index/Key',
        'KeyError': 'Index/Key',
        'FileNotFoundError': 'File/IO',
        'PermissionError': 'File/IO',
        'IOError': 'File/IO',
        'ConnectionError': 'Network/Connection',
        'TimeoutError': 'Network/Connection',
        'MemoryError': 'Memory/Resource',
        'RecursionError': 'Memory/Resource',
        'ValueError': 'Logic/Validation',
        'AssertionError': 'Logic/Validation',
        'ZeroDivisionError': 'Logic/Validation',
        'SyntaxError': 'Syntax',
        'IndentationError': 'Syntax',
    }
    
    def parse_stack_trace(self, stack_trace_text: str) -> ErrorInfo:
        """Parse a Python stack trace and extract structured information."""
        lines = stack_trace_text.strip().split('\n')
        
        # Find the error line (usually the last non-empty line)
        error_line = None
        for line in reversed(lines):
            if line.strip():
                error_line = line
                break
        
        if not error_line:
            raise ValueError("Could not find error line in stack trace")
        
        # Parse error type and message
        error_match = re.match(r'(\w+(?:Error|Exception)):\s*(.*)', error_line)
        if not error_match:
            raise ValueError(f"Could not parse error line: {error_line}")
        
        error_type = error_match.group(1)
        error_message = error_match.group(2)
        
        # Extract stack frames
        stack_frames = []
        file_path = None
        line_number = None
        function_name = None
        
        for i, line in enumerate(lines):
            # Match traceback lines
            file_match = re.match(r'\s*File "([^"]+)", line (\d+)', line)
            if file_match:
                current_file = file_match.group(1)
                current_line = int(file_match.group(2))
                
                # Get function name from next line
                if i + 1 < len(lines):
                    func_match = re.match(r'\s*in (\w+)', lines[i + 1])
                    current_func = func_match.group(1) if func_match else None
                else:
                    current_func = None
                
                stack_frames.append({
                    'file': current_file,
                    'line': current_line,
                    'function': current_func
                })
                
                # Keep the last (most specific) file/line/function
                file_path = current_file
                line_number = current_line
                function_name = current_func
        
        # Categorize error
        category = self.ERROR_CATEGORIES.get(error_type, 'Other')
        
        return ErrorInfo(
            error_type=error_type,
            error_message=error_message,
            file_path=file_path,
            line_number=line_number,
            function_name=function_name,
            stack_trace=[str(f) for f in stack_frames],
            category=category
        )
    
    def suggest_investigation_steps(self, error_info: ErrorInfo) -> List[str]:
        """Suggest investigation steps based on error type."""
        steps = []
        
        if error_info.category == 'Import/Dependency':
            steps = [
                "Check if module is installed: pip list | grep <module>",
                "Verify correct virtual environment is activated",
                "Check for circular imports",
                "Verify PYTHONPATH configuration",
                "Check package structure and __init__.py files"
            ]
        elif error_info.category == 'Type':
            steps = [
                "Check variable types at error location",
                "Trace variable transformations",
                "Verify function call arguments match signature",
                "Check for variable shadowing",
                "Review type conversions"
            ]
        elif error_info.category == 'Attribute/Name':
            steps = [
                "Check object initialization",
                "Verify all attributes are set in __init__",
                "Check for None values",
                "Verify variable scope",
                "Check for typos in attribute/variable names"
            ]
        elif error_info.category == 'Index/Key':
            steps = [
                "Check collection size before access",
                "Verify index calculation logic",
                "Check dictionary key existence",
                "Review loop bounds",
                "Validate data population logic"
            ]
        elif error_info.category == 'File/IO':
            steps = [
                "Verify file path (absolute vs relative)",
                "Check file existence",
                "Verify file permissions",
                "Check current working directory",
                "Review path construction logic"
            ]
        elif error_info.category == 'Network/Connection':
            steps = [
                "Verify service is running",
                "Test connection manually",
                "Check host and port configuration",
                "Verify network connectivity",
                "Review timeout settings"
            ]
        else:
            steps = [
                "Read full stack trace carefully",
                "Trace execution flow backwards",
                "Check variable values at error point",
                "Review recent code changes",
                "Add logging/print statements for debugging"
            ]
        
        return steps
    
    def format_analysis(self, error_info: ErrorInfo) -> str:
        """Format error analysis for display."""
        output = []
        output.append("=" * 80)
        output.append("ERROR ANALYSIS")
        output.append("=" * 80)
        output.append(f"\nError Type: {error_info.error_type}")
        output.append(f"Category: {error_info.category}")
        output.append(f"Message: {error_info.error_message}")
        
        if error_info.file_path:
            output.append(f"\nLocation:")
            output.append(f"  File: {error_info.file_path}")
            output.append(f"  Line: {error_info.line_number}")
            if error_info.function_name:
                output.append(f"  Function: {error_info.function_name}")
        
        if error_info.stack_trace:
            output.append(f"\nStack Frames: {len(error_info.stack_trace)}")
            for frame in error_info.stack_trace[-5:]:  # Show last 5 frames
                output.append(f"  {frame}")
        
        steps = self.suggest_investigation_steps(error_info)
        output.append(f"\nSuggested Investigation Steps:")
        for i, step in enumerate(steps, 1):
            output.append(f"  {i}. {step}")
        
        output.append("\n" + "=" * 80)
        
        return "\n".join(output)


def main():
    """Main entry point for the script."""
    analyzer = ErrorAnalyzer()
    
    if len(sys.argv) > 1:
        # Read from file
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        
        stack_trace = file_path.read_text()
    else:
        # Read from stdin
        print("Paste your stack trace (press Ctrl+D when done):")
        stack_trace = sys.stdin.read()
    
    try:
        error_info = analyzer.parse_stack_trace(stack_trace)
        print(analyzer.format_analysis(error_info))
    except Exception as e:
        print(f"Error analyzing stack trace: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
