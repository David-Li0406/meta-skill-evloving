#!/usr/bin/env python3
"""
Laravel/Livewire Code Analyzer
Scans PHP files for common anti-patterns and code smells
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

class CodeAnalyzer:
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.issues = []
        
    def analyze(self) -> Dict:
        """Run all analysis checks"""
        print(f"🔍 Analyzing Laravel/Livewire code in: {self.directory}\n")
        
        # Find PHP files
        php_files = list(self.directory.rglob("*.php"))
        
        for file_path in php_files:
            self.analyze_file(file_path)
        
        return self.generate_report()
    
    def analyze_file(self, file_path: Path):
        """Analyze a single PHP file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Run all checks
            self.check_fat_controllers(file_path, content, lines)
            self.check_n_plus_one(file_path, content, lines)
            self.check_missing_type_hints(file_path, content, lines)
            self.check_magic_values(file_path, content, lines)
            self.check_inline_validation(file_path, content, lines)
            self.check_mass_assignment(file_path, content, lines)
            self.check_missing_transactions(file_path, content, lines)
            self.check_livewire_patterns(file_path, content, lines)
            
        except Exception as e:
            print(f"⚠️  Error analyzing {file_path}: {str(e)}")
    
    def check_fat_controllers(self, file_path: Path, content: str, lines: List[str]):
        """Check for fat controllers with business logic"""
        if 'Controller' not in file_path.name:
            return
        
        # Count lines in methods
        method_pattern = r'public function (\w+)\([^)]*\)\s*{([^}]+)}'
        methods = re.finditer(method_pattern, content, re.MULTILINE | re.DOTALL)
        
        for method in methods:
            method_name = method.group(1)
            method_body = method.group(2)
            line_count = len(method_body.split('\n'))
            
            if line_count > 30:
                line_num = content[:method.start()].count('\n') + 1
                self.add_issue(
                    file_path, line_num, 'HIGH',
                    f"Fat controller method '{method_name}' ({line_count} lines). Consider extracting to service/action class."
                )
    
    def check_n_plus_one(self, file_path: Path, content: str, lines: List[str]):
        """Check for potential N+1 query issues"""
        # Look for Model::all() or Model::get() without with()
        patterns = [
            (r'(\w+)::(?:all|get)\(\)(?!.*->with\()', "Missing eager loading. Use ->with() to prevent N+1 queries"),
            (r'foreach.*as.*{[^}]*->\w+->(?!with)', "Potential N+1 in loop. Eager load relationships"),
        ]
        
        for pattern, message in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                self.add_issue(file_path, line_num, 'HIGH', message)
    
    def check_missing_type_hints(self, file_path: Path, content: str, lines: List[str]):
        """Check for missing type hints and return types"""
        # Match public/protected functions without return types
        pattern = r'(?:public|protected|private)\s+function\s+(\w+)\([^)]*\)(?!\s*:\s*\w+)\s*{'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            func_name = match.group(1)
            # Skip magic methods and constructors
            if func_name.startswith('__') or func_name == 'register' or func_name == 'boot':
                continue
                
            line_num = content[:match.start()].count('\n') + 1
            self.add_issue(
                file_path, line_num, 'MEDIUM',
                f"Function '{func_name}' missing return type declaration"
            )
    
    def check_magic_values(self, file_path: Path, content: str, lines: List[str]):
        """Check for magic numbers and strings"""
        # Look for hardcoded status checks
        patterns = [
            r"status\s*===?\s*['\"](\w+)['\"]",
            r"role\s*===?\s*['\"](\w+)['\"]",
            r"type\s*===?\s*['\"](\w+)['\"]",
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                value = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                self.add_issue(
                    file_path, line_num, 'MEDIUM',
                    f"Magic string '{value}' detected. Consider using enum or constant"
                )
    
    def check_inline_validation(self, file_path: Path, content: str, lines: List[str]):
        """Check for inline validation in controllers"""
        if 'Controller' not in file_path.name:
            return
        
        # Look for $request->validate() with many rules
        pattern = r'\$\w+->validate\(\[(.*?)\]\)'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            rules = match.group(1)
            rule_count = rules.count("'")
            
            if rule_count > 10:  # More than 5 fields
                line_num = content[:match.start()].count('\n') + 1
                self.add_issue(
                    file_path, line_num, 'MEDIUM',
                    "Large inline validation detected. Consider using FormRequest class"
                )
    
    def check_mass_assignment(self, file_path: Path, content: str, lines: List[str]):
        """Check for dangerous mass assignment"""
        patterns = [
            r'::create\(\$request->all\(\)\)',
            r'::update\(\$request->all\(\)\)',
        ]
        
        for pattern in patterns:
            if re.search(pattern, content):
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    self.add_issue(
                        file_path, line_num, 'HIGH',
                        "Mass assignment vulnerability. Use validated() or only() instead of all()"
                    )
    
    def check_missing_transactions(self, file_path: Path, content: str, lines: List[str]):
        """Check for missing database transactions"""
        # Look for multiple database operations without transaction
        if 'DB::transaction' in content or 'db()->transaction' in content:
            return
        
        db_operations = [
            r'::create\(',
            r'->save\(',
            r'->update\(',
            r'->delete\(',
        ]
        
        operation_count = sum(len(re.findall(pattern, content)) for pattern in db_operations)
        
        if operation_count >= 3:
            self.add_issue(
                file_path, 1, 'MEDIUM',
                f"Multiple database operations ({operation_count}) without transaction wrapper"
            )
    
    def check_livewire_patterns(self, file_path: Path, content: str, lines: List[str]):
        """Check Livewire-specific patterns"""
        if 'Component' not in content or 'Livewire' not in content:
            return
        
        # Check for model binding in public properties
        if re.search(r'public\s+User\s+\$user', content):
            line_num = re.search(r'public\s+User\s+\$user', content).start()
            line_num = content[:line_num].count('\n') + 1
            self.add_issue(
                file_path, line_num, 'HIGH',
                "Direct model binding in Livewire component. Bind specific properties instead"
            )
        
        # Check for missing computed property attributes (Livewire 3)
        if 'getProperty' in content or 'get' in content:
            pattern = r'public function get(\w+)Property\(\)'
            matches = re.finditer(pattern, content)
            for match in matches:
                prop_name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                self.add_issue(
                    file_path, line_num, 'LOW',
                    f"Old Livewire 2 computed property syntax. Use #[Computed] attribute in Livewire 3"
                )
        
        # Check for missing real-time validation
        if '$rules' in content and 'updated(' not in content:
            self.add_issue(
                file_path, 1, 'LOW',
                "Consider adding updated() method for real-time validation"
            )
    
    def add_issue(self, file_path: Path, line: int, severity: str, message: str):
        """Add an issue to the report"""
        self.issues.append({
            'file': str(file_path.relative_to(self.directory)),
            'line': line,
            'severity': severity,
            'message': message
        })
    
    def generate_report(self) -> Dict:
        """Generate analysis report"""
        # Group by severity
        high = [i for i in self.issues if i['severity'] == 'HIGH']
        medium = [i for i in self.issues if i['severity'] == 'MEDIUM']
        low = [i for i in self.issues if i['severity'] == 'LOW']
        
        report = {
            'summary': {
                'total_issues': len(self.issues),
                'high': len(high),
                'medium': len(medium),
                'low': len(low),
            },
            'issues': {
                'high': high,
                'medium': medium,
                'low': low,
            }
        }
        
        self.print_report(report)
        return report
    
    def print_report(self, report: Dict):
        """Print formatted report to console"""
        print("\n" + "="*80)
        print("📊 ANALYSIS REPORT")
        print("="*80)
        
        summary = report['summary']
        print(f"\n📈 Summary:")
        print(f"   Total Issues: {summary['total_issues']}")
        print(f"   🔴 High:     {summary['high']}")
        print(f"   🟡 Medium:   {summary['medium']}")
        print(f"   🟢 Low:      {summary['low']}")
        
        for severity in ['high', 'medium', 'low']:
            issues = report['issues'][severity]
            if not issues:
                continue
            
            emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[severity]
            print(f"\n{emoji} {severity.upper()} Priority Issues:")
            print("-" * 80)
            
            for issue in issues:
                print(f"\n   📄 {issue['file']}:{issue['line']}")
                print(f"      {issue['message']}")
        
        print("\n" + "="*80 + "\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_code.py <directory>")
        print("Example: python3 analyze_code.py app/Http/Controllers")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"❌ Error: Directory '{directory}' not found")
        sys.exit(1)
    
    analyzer = CodeAnalyzer(directory)
    report = analyzer.analyze()
    
    # Optionally save to JSON
    if '--json' in sys.argv:
        with open('analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("💾 Report saved to analysis_report.json")

if __name__ == "__main__":
    main()
