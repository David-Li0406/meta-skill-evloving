#!/usr/bin/env python3
"""
Simple test script for refactoring assistant
"""

import json
import sys
sys.path.insert(0, '.')

try:
    from refactoring_assistant import RefactoringAssistant
    print("✓ Module import successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Load sample data
try:
    with open('sample_input.json', 'r') as f:
        data = json.load(f)
    print("✓ JSON data loaded")
except Exception as e:
    print(f"✗ JSON load error: {e}")
    sys.exit(1)

# Test 1: Initialization
try:
    assistant = RefactoringAssistant(data)
    print("✓ Assistant initialized")
except Exception as e:
    print(f"✗ Initialization error: {e}")
    sys.exit(1)

# Test 2: Process without review decisions
try:
    result1 = assistant.process()
    print(f"✓ Process without review decisions successful")
    print(f"  Stage: {result1.get('stage')}")
    print(f"  Checklist items: {len(result1.get('checklist', []))}")
except Exception as e:
    print(f"✗ Process error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Process with review decisions
review_decisions = [
    {'item_id': 0, 'approved': 'yes', 'feedback': '同意重构'},
    {'item_id': 1, 'approved': 'no', 'feedback': '影响太大'},
    {'item_id': 2, 'approved': 'yes', 'feedback': '测试充分，可执行'}
]

try:
    result2 = assistant.process(review_decisions)
    print(f"✓ Process with review decisions successful")
    print(f"  Stage: {result2.get('stage')}")
    print(f"  Status: {result2.get('status')}")
    print(f"  Report has keys: {list(result2.get('report', {}).keys())}")
except Exception as e:
    print(f"✗ Process with review error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All tests passed successfully!")