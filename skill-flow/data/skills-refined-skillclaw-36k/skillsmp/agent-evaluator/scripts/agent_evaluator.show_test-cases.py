# Utility script to display loaded test cases from agent_evaluator.test-cases.md
# for audit/debug purposes. Groups with agent_evaluator.py for VS Code File Nesting.

import os
import sys

# Adjust path to import MarkdownTestLoader from agent_evaluator.test.py
import importlib.util

# Load the test module file directly (agent_evaluator.test.py is not a package)
test_module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agent_evaluator.test.py')
spec = importlib.util.spec_from_file_location('agent_evaluator_test_module', test_module_path)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)
MarkdownTestLoader = getattr(test_module, 'MarkdownTestLoader')

TEST_CASES_MD = os.path.normpath(os.path.join(os.path.dirname(__file__), 'agent_evaluator.test-cases.md'))

def main():
    loader = MarkdownTestLoader(TEST_CASES_MD)
    test_cases = loader.get_test_cases()
    print(f"Loaded {len(test_cases)} test cases from {TEST_CASES_MD}\n")
    for section, cases in test_cases.items():
        print(f"Section: {section} ({len(cases)} cases)")
        for case in cases:
            print(f"  - {case.get('title', case.get('name', '<unnamed>'))}")
    print("\nSummary:")
    for section, cases in test_cases.items():
        print(f"  {section}: {len(cases)} cases")
    print(f"\nTotal test cases: {sum(len(cases) for cases in test_cases.values())}")

if __name__ == "__main__":
    main()
