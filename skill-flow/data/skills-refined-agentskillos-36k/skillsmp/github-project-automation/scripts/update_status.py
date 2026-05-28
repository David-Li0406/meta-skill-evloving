#!/usr/bin/env python3
"""
Synchronize GitHub Project status fields with issue labels
Usage: python3 update_status.py PROJECT_ID PROJECT_NUM OWNER REPO START_ISSUE END_ISSUE
"""

import json
import subprocess
import time
import sys

def get_issue_labels(issue_number):
    """Get labels for an issue"""
    cmd = ["gh", "issue", "view", str(issue_number), "--json", "labels"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    return [label["name"] for label in data["labels"]]

def get_project_item_id(issue_number, project_number, owner, repo):
    """Get the project item ID for an issue"""
    query = f'''query={{
      repository(owner: "{owner}", name: "{repo}") {{
        issue(number: {issue_number}) {{
          projectItems(first: 10) {{
            nodes {{
              id
              project {{
                number
              }}
            }}
          }}
        }}
      }}
    }}'''

    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    for item in data["data"]["repository"]["issue"]["projectItems"]["nodes"]:
        if item["project"]["number"] == project_number:
            return item["id"]
    return None

def update_issue_status(item_id, project_id, field_id, option_id):
    """Update the status field for a project item"""
    mutation = f'''
    mutation {{
      updateProjectV2ItemFieldValue(
        input: {{
          projectId: "{project_id}"
          itemId: "{item_id}"
          fieldId: "{field_id}"
          value: {{
            singleSelectOptionId: "{option_id}"
          }}
        }}
      ) {{
        projectV2Item {{
          id
        }}
      }}
    }}
    '''

    cmd = ["gh", "api", "graphql", "-f", f"query={mutation}"]
    subprocess.run(cmd, capture_output=True, text=True, check=True)

def get_status_field_info(project_id):
    """Get status field ID and option IDs"""
    query = f'''
    query {{
      node(id: "{project_id}") {{
        ... on ProjectV2 {{
          fields(first: 20) {{
            nodes {{
              ... on ProjectV2SingleSelectField {{
                id
                name
                options {{
                  id
                  name
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    '''

    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    for field in data["data"]["node"]["fields"]["nodes"]:
        if field and field.get("name") == "Status":
            return field
    return None

def main():
    if len(sys.argv) != 7:
        print("Usage: python3 update_status.py PROJECT_ID PROJECT_NUM OWNER REPO START_ISSUE END_ISSUE")
        print("Example: python3 update_status.py PVT_kwHOABC 4 myuser myrepo 64 151")
        sys.exit(1)

    PROJECT_ID = sys.argv[1]
    PROJECT_NUMBER = int(sys.argv[2])
    OWNER = sys.argv[3]
    REPO = sys.argv[4]
    START_ISSUE = int(sys.argv[5])
    END_ISSUE = int(sys.argv[6])

    print("📊 Getting project status field information...")
    status_field = get_status_field_info(PROJECT_ID)

    if not status_field:
        print("❌ Status field not found in project")
        sys.exit(1)

    STATUS_FIELD_ID = status_field["id"]

    # Map option names to IDs
    option_map = {opt["name"]: opt["id"] for opt in status_field["options"]}
    print(f"✅ Status field found with options: {', '.join(option_map.keys())}")

    # Map labels to status options (customize as needed)
    LABEL_TO_STATUS = {
        "status:backlog": option_map.get("Todo") or option_map.get("Backlog"),
        "status:in-progress": option_map.get("In Progress") or option_map.get("In progress"),
        "status:done": option_map.get("Done"),
    }

    print(f"\n📊 Updating issue statuses in project...")
    print()

    updated = 0
    skipped = 0
    errors = 0

    for issue_number in range(START_ISSUE, END_ISSUE + 1):
        try:
            # Get labels
            labels = get_issue_labels(issue_number)

            # Find status label
            status_label = None
            for label in labels:
                if label in LABEL_TO_STATUS:
                    status_label = label
                    break

            if not status_label:
                print(f"⚠️  Issue #{issue_number}: No status label found, skipping")
                skipped += 1
                continue

            # Get project item ID
            item_id = get_project_item_id(issue_number, PROJECT_NUMBER, OWNER, REPO)
            if not item_id:
                print(f"❌ Issue #{issue_number}: Not found in project")
                errors += 1
                continue

            # Update status
            option_id = LABEL_TO_STATUS[status_label]
            if not option_id:
                print(f"❌ Issue #{issue_number}: No matching status option for {status_label}")
                errors += 1
                continue

            update_issue_status(item_id, PROJECT_ID, STATUS_FIELD_ID, option_id)

            # Find status name from option ID
            status_name = next((name for name, id in option_map.items() if id == option_id), "Unknown")

            print(f"✅ Issue #{issue_number}: {status_label} → {status_name}")
            updated += 1

            # Rate limiting
            time.sleep(0.3)

        except Exception as e:
            print(f"❌ Issue #{issue_number}: Error - {e}")
            errors += 1

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 Summary:")
    print(f"   Updated: {updated}")
    print(f"   Skipped: {skipped}")
    print(f"   Errors: {errors}")
    print(f"   Total: {updated + skipped + errors}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    main()
