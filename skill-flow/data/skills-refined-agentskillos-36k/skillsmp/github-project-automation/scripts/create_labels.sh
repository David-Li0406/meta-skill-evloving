#!/bin/bash
# Create all labels for GitHub project organization

set -e

echo "🏷️  Creating GitHub labels..."
echo

# Epic labels (blue color scheme)
echo "Creating epic labels..."
gh label create "epic:authentication" --description "Authentication & User Management" --color "0052CC" --force
gh label create "epic:onboarding" --description "Onboarding & Profile Management" --color "0052CC" --force
gh label create "epic:core-features" --description "Core Feature Implementation" --color "0052CC" --force
gh label create "epic:admin" --description "Admin & Management Tools" --color "0052CC" --force
gh label create "epic:infrastructure" --description "Infrastructure & DevOps" --color "0052CC" --force
gh label create "epic:ui-ux" --description "UI Components & Design" --color "0052CC" --force

# Status labels (traffic light colors)
echo "Creating status labels..."
gh label create "status:done" --description "Fully implemented (code + functionality)" --color "0E8A16" --force
gh label create "status:in-progress" --description "Partially implemented" --color "FBCA04" --force
gh label create "status:backlog" --description "Not yet implemented" --color "D93F0B" --force

# Priority labels
echo "Creating priority labels..."
gh label create "priority:critical" --description "Critical for MVP" --color "B60205" --force
gh label create "priority:high" --description "High priority" --color "D93F0B" --force
gh label create "priority:medium" --description "Medium priority" --color "FBCA04" --force
gh label create "priority:low" --description "Low priority" --color "0E8A16" --force

# Type labels
echo "Creating type labels..."
gh label create "type:feature" --description "New feature or enhancement" --color "A2EEEF" --force
gh label create "type:bug" --description "Bug or issue" --color "D73A4A" --force
gh label create "type:tech-debt" --description "Technical debt" --color "FEF2C0" --force
gh label create "type:docs" --description "Documentation" --color "0075CA" --force

echo
echo "✅ All labels created successfully"
