#!/bin/bash
# Claude-Driven Development Workflow
#
# This script demonstrates the workflow when Claude makes changes
# to the Requirements Framework during a development session.

echo "=== Claude-Driven Development Workflow ==="
echo ""
echo "This workflow is used when Claude edits files directly in"
echo "~/.claude/hooks/ during a development session."
echo ""

# Navigate to repository
cd ~/Tools/claude-requirements-framework

# Step 1: Claude makes changes
echo "Step 1: Claude edits files in ~/.claude/hooks/"
echo ""
echo "Example: Claude modified these files:"
echo "  - ~/.claude/hooks/lib/requirements.py"
echo "  - ~/.claude/hooks/check-requirements.py"
echo ""

# Step 2: Test the changes immediately
echo "Step 2: Test changes immediately (already in deployed location)..."
echo "python3 ~/.claude/hooks/test_requirements.py"
echo ""

# Step 3: Copy changes back to repository
echo "Step 3: Copy changes back to repository..."
echo ""
echo "For each file Claude modified:"
echo ""
echo '# Copy requirements.py'
echo 'cp ~/.claude/hooks/lib/requirements.py hooks/lib/requirements.py'
echo ""
echo '# Copy check-requirements.py'
echo 'cp ~/.claude/hooks/check-requirements.py hooks/check-requirements.py'
echo ""

# Step 4: Deploy from repo
echo "Step 4: Deploy from repo to maintain source of truth..."
echo "./sync.sh deploy"
echo ""

# Step 5: Review changes
echo "Step 5: Review what changed..."
echo "git diff"
echo ""

# Step 6: Verify tests still pass
echo "Step 6: Verify tests still pass..."
echo "python3 hooks/test_requirements.py"
echo ""

# Step 7: Commit
echo "Step 7: Commit changes..."
echo 'git add .'
echo 'git commit -m "feat: <description of what Claude built>"'
echo 'git push origin master'
echo ""

echo "=== Quick Reference Commands ==="
echo ""
echo "# When Claude edits ~/.claude/hooks/lib/some_file.py:"
echo "cp ~/.claude/hooks/lib/some_file.py hooks/lib/some_file.py"
echo "./sync.sh deploy"
echo "git add . && git commit -m 'feat: description'"
echo ""

echo "# When Claude edits ~/.claude/hooks/some_hook.py:"
echo "cp ~/.claude/hooks/some_hook.py hooks/some_hook.py"
echo "./sync.sh deploy"
echo "git add . && git commit -m 'feat: description'"
echo ""

echo "# Complete sequence:"
echo "cd ~/Tools/claude-requirements-framework"
echo "cp ~/.claude/hooks/MODIFIED_FILE hooks/MODIFIED_FILE"
echo "./sync.sh deploy"
echo "git diff"
echo "python3 hooks/test_requirements.py"
echo "git add . && git commit -m 'feat: description' && git push"
