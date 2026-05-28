"""
Code Analysis Script
Analyzes code files for quality metrics and potential issues.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ComplexityMetric:
    """Represents complexity metrics for a code element."""
    name: str
    cyclomatic_complexity: int
    lines_of_code: int
    parameters: int
    nested_depth: int


class PythonAnalyzer:
    """Analyzes Python code for various quality metrics."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        with open(file_path, 'r') as f:
            self.code = f.read()
        self.tree = ast.parse(self.code)
        self.lines = self.code.split('\n')
    
    def analyze(self) -> Dict[str, Any]:
        """Perform comprehensive code analysis."""
        return {
            'file': str(self.file_path),
            'total_lines': len(self.lines),
            'code_lines': self._count_code_lines(),
            'comment_lines': self._count_comment_lines(),
            'blank_lines': self._count_blank_lines(),
            'functions': self._analyze_functions(),
            'classes': self._analyze_classes(),
            'imports': self._analyze_imports(),
            'code_smells': self._detect_code_smells(),
            'complexity_summary': self._complexity_summary()
        }
    
    def _count_code_lines(self) -> int:
        """Count lines containing code."""
        code_lines = 0
        for line in self.lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                code_lines += 1
        return code_lines
    
    def _count_comment_lines(self) -> int:
        """Count lines containing comments."""
        return sum(1 for line in self.lines if line.strip().startswith('#'))
    
    def _count_blank_lines(self) -> int:
        """Count blank lines."""
        return sum(1 for line in self.lines if not line.strip())
    
    def _analyze_functions(self) -> List[Dict[str, Any]]:
        """Analyze all functions in the code."""
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'line': node.lineno,
                    'parameters': len(node.args.args),
                    'complexity': self._calculate_complexity(node),
                    'lines': self._count_node_lines(node),
                    'has_docstring': ast.get_docstring(node) is not None
                }
                functions.append(func_info)
        return functions
    
    def _analyze_classes(self) -> List[Dict[str, Any]]:
        """Analyze all classes in the code."""
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                class_info = {
                    'name': node.name,
                    'line': node.lineno,
                    'methods': len(methods),
                    'lines': self._count_node_lines(node),
                    'has_docstring': ast.get_docstring(node) is not None
                }
                classes.append(class_info)
        return classes
    
    def _analyze_imports(self) -> Dict[str, Any]:
        """Analyze import statements."""
        imports = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                else:
                    module = node.module or ''
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}" if module else alias.name)
        
        return {
            'count': len(imports),
            'modules': sorted(set(imports))
        }
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            # Each decision point adds 1 to complexity
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _count_node_lines(self, node: ast.AST) -> int:
        """Count lines of code in an AST node."""
        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
            return node.end_lineno - node.lineno + 1
        return 0
    
    def _detect_code_smells(self) -> List[Dict[str, Any]]:
        """Detect common code smells."""
        smells = []
        
        # Long functions
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                lines = self._count_node_lines(node)
                if lines > 50:
                    smells.append({
                        'type': 'long_function',
                        'name': node.name,
                        'line': node.lineno,
                        'severity': 'medium',
                        'message': f'Function has {lines} lines (recommended: <50)'
                    })
                
                # Too many parameters
                param_count = len(node.args.args)
                if param_count > 5:
                    smells.append({
                        'type': 'too_many_parameters',
                        'name': node.name,
                        'line': node.lineno,
                        'severity': 'medium',
                        'message': f'Function has {param_count} parameters (recommended: ≤5)'
                    })
                
                # High complexity
                complexity = self._calculate_complexity(node)
                if complexity > 10:
                    smells.append({
                        'type': 'high_complexity',
                        'name': node.name,
                        'line': node.lineno,
                        'severity': 'high',
                        'message': f'Cyclomatic complexity is {complexity} (recommended: ≤10)'
                    })
        
        # Large classes
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                if len(methods) > 20:
                    smells.append({
                        'type': 'large_class',
                        'name': node.name,
                        'line': node.lineno,
                        'severity': 'high',
                        'message': f'Class has {len(methods)} methods (recommended: <20)'
                    })
        
        # Magic numbers
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Num):
                # Skip common acceptable numbers
                if node.n not in (0, 1, -1, 2):
                    if hasattr(node, 'lineno'):
                        smells.append({
                            'type': 'magic_number',
                            'line': node.lineno,
                            'severity': 'low',
                            'message': f'Magic number {node.n} should be a named constant'
                        })
        
        return smells
    
    def _complexity_summary(self) -> Dict[str, Any]:
        """Generate complexity summary."""
        functions = self._analyze_functions()
        
        if not functions:
            return {
                'average_complexity': 0,
                'max_complexity': 0,
                'functions_over_10': 0
            }
        
        complexities = [f['complexity'] for f in functions]
        
        return {
            'average_complexity': sum(complexities) / len(complexities),
            'max_complexity': max(complexities),
            'functions_over_10': sum(1 for c in complexities if c > 10),
            'total_functions': len(functions)
        }


def format_report(analysis: Dict[str, Any]) -> str:
    """Format analysis results as a readable report."""
    report = []
    report.append("=" * 60)
    report.append(f"CODE ANALYSIS REPORT: {analysis['file']}")
    report.append("=" * 60)
    report.append("")
    
    # Summary
    report.append("SUMMARY")
    report.append("-" * 60)
    report.append(f"Total Lines:       {analysis['total_lines']}")
    report.append(f"Code Lines:        {analysis['code_lines']}")
    report.append(f"Comment Lines:     {analysis['comment_lines']}")
    report.append(f"Blank Lines:       {analysis['blank_lines']}")
    report.append(f"Functions:         {len(analysis['functions'])}")
    report.append(f"Classes:           {len(analysis['classes'])}")
    report.append("")
    
    # Complexity
    complexity = analysis['complexity_summary']
    report.append("COMPLEXITY METRICS")
    report.append("-" * 60)
    report.append(f"Average Complexity:    {complexity['average_complexity']:.2f}")
    report.append(f"Maximum Complexity:    {complexity['max_complexity']}")
    report.append(f"Functions over 10:     {complexity['functions_over_10']}")
    report.append("")
    
    # Code Smells
    smells = analysis['code_smells']
    if smells:
        report.append("CODE SMELLS DETECTED")
        report.append("-" * 60)
        
        high_severity = [s for s in smells if s['severity'] == 'high']
        medium_severity = [s for s in smells if s['severity'] == 'medium']
        low_severity = [s for s in smells if s['severity'] == 'low']
        
        if high_severity:
            report.append("\nHIGH PRIORITY:")
            for smell in high_severity:
                report.append(f"  Line {smell['line']}: {smell['message']}")
        
        if medium_severity:
            report.append("\nMEDIUM PRIORITY:")
            for smell in medium_severity:
                report.append(f"  Line {smell['line']}: {smell['message']}")
        
        if low_severity:
            report.append(f"\n{len(low_severity)} low priority issues detected")
        
        report.append("")
    
    # Complex Functions
    complex_funcs = [f for f in analysis['functions'] if f['complexity'] > 5]
    if complex_funcs:
        report.append("COMPLEX FUNCTIONS")
        report.append("-" * 60)
        for func in sorted(complex_funcs, key=lambda x: x['complexity'], reverse=True)[:5]:
            report.append(f"  {func['name']} (line {func['line']}): "
                         f"complexity={func['complexity']}, lines={func['lines']}")
        report.append("")
    
    report.append("=" * 60)
    
    return "\n".join(report)


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        analyzer = PythonAnalyzer(file_path)
        analysis = analyzer.analyze()
        report = format_report(analysis)
        print(report)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: Invalid Python syntax: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
