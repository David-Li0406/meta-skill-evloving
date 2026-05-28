---
name: ui-ux-pro-max
description: Use this skill when you need to design, create, or update frontend UI/UX for web and mobile applications, including landing pages, dashboards, and e-commerce sites.
---

# UI/UX Pro Max - Design Intelligence

This skill provides a searchable database of UI styles, color palettes, font pairings, chart types, product recommendations, UX guidelines, and stack-specific best practices. It includes various styles, palettes, and elements to assist in frontend design.

## When to use

Run `ui-ux-pro-max .` when:

- A user requests UI/UX work (design, build, create, implement, review, fix, improve).
- A user needs to build frontend pages (landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app).

## How to use

### Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on the user's OS:

**macOS:**

```bash
brew install python3
```

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install python3
```

**Windows:**

```powershell
winget install Python.Python.3.12
```

### Step 1: Analyze User Requirements

Extract key information from the user request:

- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`.

### Step 2: Search Relevant Domains

Use `search.py` multiple times to gather comprehensive information. Search until you have enough context.

```bash
python3 .trae/skills/ui-ux-pro-max/scripts/search.py "<keywords>"
```