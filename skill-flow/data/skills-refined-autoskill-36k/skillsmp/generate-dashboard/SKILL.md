---
name: generate-dashboard
description: Generate an HTML dashboard from meeting analysis. Use when the user wants to create a visual summary, build a dashboard, generate a report, or visualize meeting insights.
---

# Generate Meeting Dashboard

Create a beautiful HTML dashboard from meeting analysis.

## Instructions

1. Read the analysis from `projects/{project}/analysis/{date}.json`
   - If analysis doesn't exist, run the analyze-meeting skill first
2. Use the template from `templates/dashboard.html` as a base
3. Generate a complete, standalone HTML file with:
   - Modern, clean design using Tailwind CSS (via CDN)
   - All extracted insights organized in visual cards
   - Responsive layout for desktop and mobile
   - Print-friendly styling
   - The project name and date prominently displayed

4. Replace template placeholders with actual content:
   - `{{PROJECT_NAME}}` → Project display name (convert kebab-case to Title Case)
   - `{{DATE}}` → Meeting date formatted nicely
   - `{{MEETING_TYPE}}` → Type of meeting (standup, sprint review, etc.)
   - `{{SUMMARY}}` → Meeting summary paragraph
   - `{{ATTENDEES}}` → HTML list items for each attendee
   - `{{KEY_TOPICS}}` → HTML list items for topics
   - `{{ACTION_ITEMS}}` → HTML cards for each action item with owner/deadline
   - `{{DECISIONS}}` → HTML list items for decisions
   - `{{QUESTIONS}}` → HTML list items for open questions
   - `{{NEXT_STEPS}}` → HTML list items for next steps

5. Save the dashboard to `projects/{project}/dashboards/{date}/index.html`

## Output

Confirm the dashboard location and provide a brief preview of what was generated.
