---
name: tailadmin-ui-patterns
description: Use this skill when building any dashboard or admin panel interface that requires TailAdmin design and Tailwind CSS classes.
---

# TailAdmin UI Patterns Skill

## When to Use This Skill

**ALWAYS invoke this skill for:**
- Dashboard interfaces and admin panels
- Data tables and grid layouts
- Charts, metrics, and KPI displays
- Form components (inputs, selects, checkboxes, toggles)
- Card layouts and stat boxes
- Navigation (sidebar, header, breadcrumbs)
- Buttons, badges, alerts, and modals
- Any UI requiring TailAdmin styling

## Critical Rule: FETCH BEFORE IMPLEMENTING

**NEVER guess or invent classes. ALWAYS fetch from the official repository first.**

```bash
# MANDATORY: Fetch TailAdmin source before ANY UI work
git clone --depth 1 https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template.git /tmp/tailadmin 2>/dev/null || echo "Already cloned"

# Verify the clone
ls /tmp/tailadmin/src/
```

## Repository Reference

| Item | Value |
|------|-------|
| **Repository** | https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template |
| **Branch** | `main` |
| **Source Path** | `src/` |
| **CSS Config** | `tailwind.config.js` |
| **Custom CSS** | `src/css/style.css` |

## Mandatory Fetch Commands

**Before implementing ANY TailAdmin UI, run these commands:**

```bash
# 1. Clone repository (if not already done)
git clone --depth 1 https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template.git /tmp/tailadmin 2>/dev/null

# 2. Check available page templates
ls /tmp/tailadmin/src/*.html

# 3. Check partials (reusable components)
ls /tmp/tailadmin/src/partials/

# 4. View Tailwind config for custom classes
cat /tmp/tailadmin/tailwind.config.js

# 5. View custom CSS definitions
cat /tmp/tailadmin/src/css/style.css
```

## Finding Specific Components

```bash
# Find dashboard/stats card patterns
grep -A 50 'stat\|kpi\|metric' /tmp/tailadmin/src/index.html | head -80

# Find table patterns
cat /tmp/tailadmin/src/tables.html | head -200

# Find form patterns  
cat /tmp/tailadmin/src/form-elements.html | head -200
```