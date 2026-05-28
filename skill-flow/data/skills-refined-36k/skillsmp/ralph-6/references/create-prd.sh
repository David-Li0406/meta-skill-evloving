#!/bin/bash
# Create a new PRD file for Ralph Wiggum
# Usage: ./create-prd.sh <project-name>

PROJECT_NAME=${1:-"my-project"}
PRD_FILE="ralph/prd.json"

cat > "$PRD_FILE" << EOF
{
  "project": "$PROJECT_NAME",
  "description": "Long-running agent tasks",
  "created": "$(date +%Y-%m-%d)",
  "features": [
    {
      "id": "feature-1",
      "priority": 1,
      "title": "First Feature",
      "description": "Description of what needs to be done",
      "acceptance_criteria": [
        "Criterion 1",
        "Criterion 2",
        "Build passes without errors"
      ],
      "project_path": "$(pwd)",
      "passes": false
    }
  ]
}
EOF

echo "Created PRD at $PRD_FILE"
echo "Edit this file to add your features, then run: ./ralph/ralph.sh"
