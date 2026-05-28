#!/bin/bash
# TDD Workflow Example for Requirements Framework Development
#
# This script demonstrates the Test-Driven Development workflow
# for adding new features to the Requirements Framework.

# Navigate to repository
cd ~/Tools/claude-requirements-framework

echo "=== TDD Workflow: Adding a New Feature ==="
echo ""

# Step 1: Check sync status first
echo "Step 1: Check sync status..."
./sync.sh status

# Step 2: Write failing test (RED phase)
echo ""
echo "Step 2: Write failing test in hooks/test_requirements.py..."
echo ""
echo "Example test to add:"
echo '
def test_new_feature(self):
    """Test the new feature behavior."""
    # Arrange
    config = {
        "requirements": {
            "new_feature": {
                "enabled": True,
                "scope": "session"
            }
        }
    }

    # Act
    result = some_function_to_implement(config)

    # Assert
    self.assertTrue(result)
'

# Step 3: Deploy tests
echo ""
echo "Step 3: Deploy tests..."
./sync.sh deploy

# Step 4: Run tests (should fail - RED)
echo ""
echo "Step 4: Run tests - expecting failure (RED)..."
python3 ~/.claude/hooks/test_requirements.py
# Expected: New test fails

# Step 5: Implement feature
echo ""
echo "Step 5: Implement the feature in hooks/lib/..."
echo "Edit the appropriate file to make the test pass."

# Step 6: Deploy implementation
echo ""
echo "Step 6: Deploy implementation..."
./sync.sh deploy

# Step 7: Run tests (should pass - GREEN)
echo ""
echo "Step 7: Run tests - expecting success (GREEN)..."
python3 ~/.claude/hooks/test_requirements.py
# Expected: All tests pass

# Step 8: Refactor if needed (keep tests green)
echo ""
echo "Step 8: Refactor if needed, then re-run tests..."
./sync.sh deploy
python3 ~/.claude/hooks/test_requirements.py

# Step 9: Commit
echo ""
echo "Step 9: Commit changes..."
echo 'git add .'
echo 'git commit -m "feat: Add new feature (TDD)"'
echo 'git push origin master'

echo ""
echo "=== TDD Workflow Complete ==="
echo ""
echo "Summary:"
echo "1. Write failing test (RED)"
echo "2. Deploy tests: ./sync.sh deploy"
echo "3. Run tests: python3 ~/.claude/hooks/test_requirements.py"
echo "4. Implement feature"
echo "5. Deploy: ./sync.sh deploy"
echo "6. Run tests (GREEN)"
echo "7. Refactor if needed"
echo "8. Commit and push"
