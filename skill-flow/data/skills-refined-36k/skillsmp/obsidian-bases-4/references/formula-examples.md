# Formula Examples

Real-world formula patterns for Obsidian Bases organized by category.

## Date & Time Formulas

### Calculate time until deadline

```yaml
days_until_due: 'due ? (due - today()).format("days") : ""'
hours_until: 'meeting_date ? (meeting_date - now()).format("hours") : ""'
```

### Determine if overdue

```yaml
is_overdue: due && due < today() && status == "active"
overdue_by: 'due && due < today() ? (today() - due).format("days") + " days" : ""'
```

### Age calculations

```yaml
age_in_days: '(today() - file.ctime).format("days")'
days_since_update: '(today() - file.mtime).format("days")'
days_since_contact: 'last_contact ? (today() - last_contact).format("days") : ""'
```

### Add duration to dates

```yaml
deadline: start_date + "2w"
reminder_date: due - "3d"
one_year_from_now: today() + "1y"
```

### Format dates

```yaml
formatted_date: 'due ? due.format("MMM DD, YYYY") : ""'
time_only: 'meeting_date ? meeting_date.time() : ""'
relative_time: 'file.mtime.relative()'  # "3 days ago"
```

## Text Manipulation

### Combine strings

```yaml
full_name: first_name + " " + last_name
display_text: file.name + " - " + category
label: status + ": " + priority
```

### Change case

```yaml
title_case: file.name.title()
lowercase: category.lower()
uppercase: status.toUpperCase()
```

### Extract parts

```yaml
domain: 'url ? url.split("/")[2] : ""'
first_word: 'description.split(" ")[0]'
filename: 'file.path.split("/").slice(-1)[0]'
```

### Check content

```yaml
has_keyword: description.contains("urgent")
starts_with_prefix: file.name.startsWith("TASK-")
ends_with_suffix: file.ext.endsWith(".md")
```

## Number Calculations

### Basic math

```yaml
total_cost: price * quantity
discounted_price: price * (1 - discount / 100)
average: (value1 + value2 + value3) / 3
```

### Percentage

```yaml
completion_rate: 'total_tasks > 0 ? ((completed_tasks / total_tasks) * 100).toFixed(0) + "%" : "N/A"'
percent_complete: '(completed / total * 100).toFixed(1) + "%"'
```

### Formatting numbers

```yaml
formatted_price: 'price ? "$" + price.toFixed(2) : ""'
rounded: value.round(2)
whole_number: value.floor()
```

### Min/Max

```yaml
priority_score: max(urgency, impact)
minimum_value: min(estimate_low, estimate_high)
```

## Conditional Logic

### Simple if/else

```yaml
status_emoji: 'status == "done" ? "✅" : "⏳"'
display_value: 'price ? "$" + price : "N/A"'
indicator: 'completed ? "✓" : "✗"'
```

### Multi-condition

```yaml
priority_level: 'priority == "urgent" ? "🔴" : priority == "high" ? "🟠" : priority == "medium" ? "🟡" : "🟢"'
```

### Complex conditions

```yaml
needs_attention: '(due && due < today() + "7d") || priority == "urgent"'
can_start: 'status == "planned" && dependencies_met && team_assigned'
```

## List Operations

### Count items

```yaml
tag_count: tags.length
attendee_count: 'attendees ? attendees.length : 0'
```

### Access elements

```yaml
first_tag: tags[0]
last_item: items[items.length - 1]
second_assignee: 'assignees.length > 1 ? assignees[1] : null'
```

### Check membership

```yaml
has_urgent_tag: tags.contains("urgent")
is_team_member: 'team && team.contains(link(this.file))'
```

### Filter lists

```yaml
active_tags: tags.filter(t => !t.startsWith("archived"))
high_priority_items: items.filter(item => item.priority == "high")
```

### Transform lists

```yaml
tag_names: tags.map(t => t.replace("category/", ""))
uppercase_list: items.map(i => i.toUpperCase())
```

### Join lists

```yaml
tag_string: tags.join(", ")
formatted_list: items.join(" • ")
```

## File & Link Formulas

### File properties

```yaml
file_size_kb: '(file.size / 1024).toFixed(2) + " KB"'
extension: file.ext
folder_path: file.folder
```

### Link checking

```yaml
has_project: 'project ? "✓" : "✗"'
linked_to_task: 'file.hasLink("Database/Tasks/Task-Name")'
```

### Link creation

```yaml
formatted_link: file.asLink("Custom Display")
linked_status: 'link(status, icon("circle"))'
```

## Object Operations

### Access nested properties

```yaml
author_name: 'author.name'
company_size: 'metadata.company.size'
```

### Check for properties

```yaml
has_email: 'file.hasProperty("email")'
contact_complete: 'email && phone && address'
```

## Aggregation (Summary Formulas)

### Custom averages

```yaml
# In summaries section
weighted_average: 'values.reduce((sum, v, i) => sum + v * weights[i], 0) / values.reduce((sum, w) => sum + w, 0)'
```

### Custom counts

```yaml
high_priority_count: 'values.filter(v => v == "high").length'
completed_percent: '(values.filter(v => v == "done").length / values.length * 100).toFixed(0) + "%"'
```

## Database-Specific Formulas

### Tasks

```yaml
is_overdue: due && due < today() && status == "active"
days_until_due: 'due ? (due - today()).format("days") : ""'
status_emoji: 'status == "done" ? "✅" : status == "active" ? "🔄" : status == "blocked" ? "🚫" : "📋"'
urgency_score: 'priority == "urgent" ? 4 : priority == "high" ? 3 : priority == "medium" ? 2 : 1'
```

### Projects

```yaml
completion_rate: 'total_tasks > 0 ? ((completed_tasks / total_tasks) * 100).toFixed(0) + "%" : "N/A"'
days_until_target: 'target_date ? (target_date - today()).format("days") : ""'
is_overdue: target_date && target_date < today() && status != "completed"
team_size: 'team ? team.length : 0'
budget_used_percent: 'budget > 0 ? ((spent / budget) * 100).toFixed(0) + "%" : "N/A"'
```

### People

```yaml
full_contact: 'email || linkedin || twitter ? "✓" : "✗"'
days_since_contact: 'last_contact ? (today() - last_contact).format("days") : ""'
needs_followup: 'next_action && !last_contact || (last_contact && last_contact < today() - "30d")'
contact_methods: '[email, linkedin, twitter].filter(c => c).length'
```

### Companies

```yaml
people_count: file.backlinks.filter(x => x.type == "person").length
has_website: 'website ? "✓" : "✗"'
contact_status: 'file.backlinks.filter(x => x.type == "person").length > 0 ? file.backlinks.filter(x => x.type == "person").length + " contacts" : "No contacts"'
```

### Meetings

```yaml
is_upcoming: 'meeting_date && meeting_date >= today()'
is_past: 'meeting_date && meeting_date < today()'
days_until_meeting: 'meeting_date ? (meeting_date - today()).format("days") : ""'
attendee_count: 'attendees ? attendees.length : 0'
```

### Bookmarks

```yaml
domain: 'url ? url.split("/")[2] : ""'
is_saved: 'saved ? "✓" : "✗"'
days_since_added: '(today() - file.ctime).format("days")'
star_rating: 'rating ? "⭐".repeat(rating) : ""'
```

## Performance Tips

### Avoid expensive operations

```yaml
# Expensive - avoid if possible
task_count: file.backlinks.filter(x => x.type == "task").length

# Better - use when you control the link direction
has_project: 'file.hasLink("Database/Projects/Project-Name")'
```

### Cache complex calculations

```yaml
# Instead of repeating complex formula in multiple places
# Define once as formula, reference elsewhere
priority_score: '(impact * urgency) / effort'

# Then use in filters
filters:
  and:
    - formula.priority_score > 5
```

### Handle null values

```yaml
# Always check for null before operations
safe_division: 'total > 0 ? (value / total) : 0'
safe_string: 'description ? description.toLowerCase() : ""'
safe_date: 'due ? due.format("YYYY-MM-DD") : "No date"'
```

## Common Patterns

### Emoji indicators

```yaml
priority_emoji: 'priority == "urgent" ? "🔴" : priority == "high" ? "🟠" : "🟢"'
status_indicator: 'status == "completed" ? "✅" : status == "active" ? "🔄" : "⏸️"'
boolean_check: 'value ? "✓" : "✗"'
```

### Display formatting

```yaml
formatted_currency: 'amount ? "$" + amount.toLocaleString() : ""'
formatted_percent: '(value * 100).toFixed(1) + "%"'
formatted_duration: 'hours > 0 ? hours + "h " + minutes + "m" : minutes + "m"'
```

### Scoring systems

```yaml
priority_score: 'priority == "urgent" ? 4 : priority == "high" ? 3 : priority == "medium" ? 2 : 1'
health_score: '(completion_rate * 0.5) + (on_time ? 30 : 0) + (budget_ok ? 20 : 0)'
engagement_score: '(days_since_contact ? 100 / days_since_contact : 0).round()'
```
