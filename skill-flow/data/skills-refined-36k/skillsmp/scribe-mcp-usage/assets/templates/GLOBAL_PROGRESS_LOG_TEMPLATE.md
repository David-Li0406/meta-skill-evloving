{% extends "documents/base_log.md" %}
{% from "documents/base_log.md" import rotation_notice with context %}

{% block log_metadata %}
{% set log_config.title = "Global Progress Log" %}
{% set log_config.icon = "🌍" %}
{% set log_config.summary = "Repository-wide progress tracking for all Scribe MCP projects and development activities. This log captures project lifecycle events, system milestones, and cross-project achievements." %}
{% set log_config.maintained_by = "System" %}
{% endblock %}

{% block log_body %}
{% set rotation_raw = metadata.get("is_rotation", metadata.get("IS_ROTATION", is_rotation | default("false"))) %}
{% set rotation_active = rotation_raw in [True, "true", "True", 1, "1", "yes", "YES"] %}
{% if rotation_active %}
{{ rotation_notice(metadata) }}
{% endif %}

## 📊 Repository Status
**Total Projects:** {{ metadata.total_projects | default("0") }}
**Active Projects:** {{ metadata.active_projects | default("0") }}
**Completed Projects:** {{ metadata.completed_projects | default("0") }}
**Last Updated:** {{ metadata.last_updated | default(date_utc) }}

---

## 📜 Global Entries

### 🚀 Project Lifecycle Events

### 🎯 Manual Milestones

### 📋 System Events

---

## 📈 Statistics

### Project Status Breakdown
- **Planning:** {{ metadata.planning_projects | default("0") }} projects
- **In Progress:** {{ metadata.in_progress_projects | default("0") }} projects
- **Completed:** {{ metadata.completed_projects | default("0") }} projects
- **Archived:** {{ metadata.archived_projects | default("0") }} projects

### Recent Activity
- Most Active: `{{ metadata.most_active_project | default("N/A") }}`
- Latest Creation: `{{ metadata.latest_project | default("N/A") }}` ({{ metadata.latest_creation_date | default("N/A") }})

---

## 🔗 Quick Links
- **Active Projects**: [View All Projects](../dev_plans/)
- **Recent Research**: [Research Documents](../dev_plans/*/research/)
- **Bug Reports**: [Bug Tracker](../bugs/)
- **Archived Logs**: [Log Archive](archived_global_logs/)

---

## 📝 Global Log Entries

**All Scribe MCP global log entries will appear below this line automatically.**

---

## 📋 Entry Format
```
[EMOJI] [YYYY-MM-DD HH:MM:SS UTC] [Agent: <name>] [Project: <project>] Message text | key=value; key2=value2
```

**Entry Types:**
- **🚀** Project Created
- **📋** Phase Transition
- **✅** Project Completed
- **🎯** Manual Milestone
- **⚙️** System Event
- **🔧** Infrastructure Update

**Tips:**
- Project lifecycle events are logged automatically
- Manual milestones should capture significant achievements
- Include project context when applicable
- Use structured metadata for better tracking

---

*This log is automatically maintained by the Scribe MCP system.*

{% endblock %}