#!/usr/bin/env python3
"""
Verify serena-skills functionality by testing scripts on itself.
This script tests all script categories using serena-skills directory as the test project.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

class FunctionalityVerifier:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skills_root = Path(__file__).parent.parent
        
    def run_test(self, name, cmd):
        """Run a single test command."""
        print(f"  Testing {name}...", end=" ")
        try:
            # Run from serena-skills directory
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                cwd=self.skills_root,
                timeout=30
            )
            if result.returncode == 0:
                print(f"{GREEN}✓ PASS{RESET}")
                self.passed += 1
                return True
            else:
                print(f"{RED}✗ FAIL{RESET}")
                if result.stderr:
                    print(f"    Error: {result.stderr[:200]}")
                self.failed += 1
                return False
        except Exception as e:
            print(f"{RED}✗ ERROR: {e}{RESET}")
            self.failed += 1
            return False
    
    def run_tests(self):
        """Run all functionality tests."""
        print(f"{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Serena Skills - Functionality Verification{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")
        print(f"Test project: {self.skills_root}\n")
        
        # Project Config
        print(f"{BLUE}1. Project Configuration{RESET}")
        self.run_test("activate_project", 
                     f'python scripts/project-config/activate_project.py --project-path "{self.skills_root}"')
        self.run_test("get_config", 
                     'python scripts/project-config/get_config.py')
        self.run_test("list_projects", 
                     'python scripts/project-config/list_projects.py')
        
        # File Operations
        print(f"\n{BLUE}2. File Operations{RESET}")
        self.run_test("list_dir", 
                     f'python scripts/file-ops/list_dir.py --project-root "{self.skills_root}" --path scripts')
        self.run_test("read_file", 
                     f'python scripts/file-ops/read_file.py --project-root "{self.skills_root}" --file SETUP.md --start-line 0 --end-line 5')
        self.run_test("find_file", 
                     f'python scripts/file-ops/find_file.py --project-root "{self.skills_root}" --mask "*.py" --path scripts')
        self.run_test("search_for_pattern", 
                     f'python scripts/file-ops/search_for_pattern.py --project-root "{self.skills_root}" --pattern "import" --path scripts')
        
        # Symbol Search (using Python files in lib/)
        print(f"\n{BLUE}3. Symbol Search{RESET}")
        # Check if lib directory has Python files
        lib_py_files = list((self.skills_root / "lib").rglob("*.py"))
        if lib_py_files and len(lib_py_files) > 0:
            test_file = str(lib_py_files[0].relative_to(self.skills_root)).replace('\\', '/')
            self.run_test("get_symbols_overview", 
                         f'python scripts/symbol-search/get_symbols_overview.py --project-root "{self.skills_root}" --file "{test_file}"')
            self.run_test("find_symbol", 
                         f'python scripts/symbol-search/find_symbol.py --project-root "{self.skills_root}" --pattern "def"')
        else:
            print(f"  {BLUE}Skipped (no Python files in lib/){RESET}")
        
        # Memory Manager
        print(f"\n{BLUE}4. Memory Manager{RESET}")
        test_memory_name = "test_verification"
        test_content = "Functionality verification test"
        
        self.run_test("write_memory", 
                     f'python scripts/memory-manager/write_memory.py --project-root "{self.skills_root}" --name "{test_memory_name}" --content "{test_content}"')
        self.run_test("read_memory", 
                     f'python scripts/memory-manager/read_memory.py --project-root "{self.skills_root}" --name "{test_memory_name}"')
        self.run_test("list_memories", 
                     f'python scripts/memory-manager/list_memories.py --project-root "{self.skills_root}"')
        self.run_test("delete_memory", 
                     f'python scripts/memory-manager/delete_memory.py --project-root "{self.skills_root}" --name "{test_memory_name}"')
        
        # Code Editor
        print(f"\n{BLUE}5. Code Editor{RESET}")
        test_file_path = ".tmp/test_functionality.txt"
        
        self.run_test("create_text_file", 
                     f'python scripts/code-editor/create_text_file.py --project-root "{self.skills_root}" --file "{test_file_path}" --content "Test content"')
        self.run_test("replace_content", 
                     f'python scripts/code-editor/replace_content.py --project-root "{self.skills_root}" --file "{test_file_path}" --old "Test" --new "Updated"')
        self.run_test("insert_at_line", 
                     f'python scripts/code-editor/insert_at_line.py --project-root "{self.skills_root}" --file "{test_file_path}" --line 1 --content "New line"')
        self.run_test("delete_lines", 
                     f'python scripts/code-editor/delete_lines.py --project-root "{self.skills_root}" --file "{test_file_path}" --start-line 1 --end-line 1')
        
        # Workflow Assistant
        print(f"\n{BLUE}6. Workflow Assistant{RESET}")
        self.run_test("think_collected_info", 
                     'python scripts/workflow-assistant/think_collected_info.py --context "Functionality verification"')
        self.run_test("think_are_done", 
                     'python scripts/workflow-assistant/think_are_done.py --task "Verification test" --status "in-progress"')
        
        # Shell Executor
        print(f"\n{BLUE}7. Shell Executor{RESET}")
        self.run_test("execute_shell_command", 
                     f'python scripts/shell-executor/execute_shell_command.py --project-root "{self.skills_root}" --command "echo test"')
        
        # Summary
        total = self.passed + self.failed
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Summary{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        print(f"Total tests: {total}")
        print(f"{GREEN}Passed: {self.passed}{RESET}")
        if self.failed > 0:
            print(f"{RED}Failed: {self.failed}{RESET}")
        
        if self.failed == 0:
            print(f"\n{GREEN}✓ All functionality tests passed!{RESET}")
            print(f"{GREEN}serena-skills is working correctly.{RESET}\n")
            return 0
        else:
            print(f"\n{RED}✗ Some tests failed.{RESET}")
            print(f"Please check the error messages above.\n")
            return 1

def main():
    verifier = FunctionalityVerifier()
    return verifier.run_tests()

if __name__ == "__main__":
    sys.exit(main())
