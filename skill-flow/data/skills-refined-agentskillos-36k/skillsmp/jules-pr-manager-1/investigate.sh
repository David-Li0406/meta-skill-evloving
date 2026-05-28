#!/bin/bash
# .gemini/skills/jules-pr-manager/investigate.sh
# Investigates all open Jules PRs and their timelines in a context-efficient way.
# Now includes verification of Jules acknowledgement (:eyes:).

# 1. Get Repo Info
REPO_INFO=$(gh repo view --json owner,name)
OWNER=$(echo "$REPO_INFO" | jq -r .owner.login)
NAME=$(echo "$REPO_INFO" | jq -r .name)

# 2. List all open Jules PRs
PRS=$(gh pr list --search "author:app/google-labs-jules is:open" --json number,title,labels,updatedAt,mergeable,statusCheckRollup,isDraft,body)

# 3. For each PR, fetch and filter the timeline
echo "$PRS" | jq -c '.[]' | while read -r pr; do
  NUMBER=$(echo "$pr" | jq -r .number)
  
  # Fetch timeline
  TIMELINE=$(gh api "repos/$OWNER/$NAME/issues/$NUMBER/timeline" --paginate)
  
  # Filter timeline for efficiency
  # Note: jq sub() needs double backslashes for literals in shell heredocs/scripts
  FILTERED_TIMELINE=$(echo "$TIMELINE" | jq -c '[.[] | select(.event | test("committed|reviewed|commented|labeled|unlabeled")) | {
    event: .event,
    actor: (.actor.login // .user.login // .author.name),
    timestamp: (.created_at // .submitted_at // .author.date),
    body: (.body | select(. != null) | sub("\\n---\\n\\*PR created automatically.*"; "") | sub("^@jules "; "") | .[0:500]),
    state: .state,
    label: .label.name,
    sha: (.sha // .commit_id),
    acknowledged: (if .reactions then (.reactions.eyes > 0) else false end)
  }]')
  
  # Determine if the LAST review/comment (non-Jules) was acknowledged
  LAST_INSTRUCTION_ACK=$(echo "$FILTERED_TIMELINE" | jq -r 'map(select(.actor != "google-labs-jules[bot]" and .actor != "vercel[bot]" and .actor != "copilot-pull-request-reviewer" and (.event == "reviewed" or .event == "commented"))) | last | .acknowledged')
  
  # Add filtered timeline and acknowledgement status to the PR object
  echo "$pr" | jq --argjson timeline "$FILTERED_TIMELINE" --arg ack "$LAST_INSTRUCTION_ACK" '. + {timeline: $timeline, lastInstructionAcknowledged: ($ack == "true")}'
done | jq -s '.'
