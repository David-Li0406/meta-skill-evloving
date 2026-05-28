---
name: homepage
description: This skill should be used when managing homepage/CV content - updating personal info, adding/editing/removing work experience, education entries, or skills. It provides an interactive workflow for content management with data stored in TypeScript files.
---

# Homepage Content Management

## Overview

Manage CV-style content for the portfolio homepage. Content is stored in TypeScript data files under `src/content/homepage/`. The homepage displays four sections: Hero, Experience, Education, and Skills.

## Data Files

| Section    | Data File                            | Component                                |
| ---------- | ------------------------------------ | ---------------------------------------- |
| Hero       | `src/content/homepage/hero.ts`       | `src/components/sections/hero.tsx`       |
| Experience | `src/content/homepage/experience.ts` | `src/components/sections/experience.tsx` |
| Education  | `src/content/homepage/education.ts`  | `src/components/sections/education.tsx`  |
| Skills     | `src/content/homepage/skills.ts`     | `src/components/sections/skills.tsx`     |

## Workflow

### Step 1: Display Current State

Run the script to get a compact summary of all content:

```bash
python3 .claude/skills/homepage/scripts/read_content.py all
```

This outputs a token-efficient summary. To read a specific section:

```bash
python3 .claude/skills/homepage/scripts/read_content.py hero
python3 .claude/skills/homepage/scripts/read_content.py experience
python3 .claude/skills/homepage/scripts/read_content.py education
python3 .claude/skills/homepage/scripts/read_content.py skills
```

For full JSON data: `python3 .claude/skills/homepage/scripts/read_content.py json`

### Step 2: Present Options

**IMPORTANT**: Use the `AskUserQuestion` tool to present options. Do NOT just output text with options.

```
AskUserQuestion with:
  question: "Which section would you like to update?"
  header: "Section"
  options:
    - label: "Hero"
      description: "Edit name, title, overview, or primary skills"
    - label: "Experience"
      description: "Add, edit, or remove work experience"
    - label: "Education"
      description: "Add, edit, or remove education entries"
    - label: "Skills"
      description: "Add, edit, or remove skill categories"
```

---

## Hero Section

File: `src/content/homepage/hero.ts`

### Data Structure

```typescript
export interface HeroData {
  name: string;
  title: string;
  overview: string;
  primarySkills: string[];
}
```

### Edit Workflow

1. Use `AskUserQuestion` to ask which field to edit (name, title, overview, primarySkills)
2. Read the file to get current value
3. Use `AskUserQuestion` to get new value from user (use "Other" option for free-form input)
4. Update the exported `hero` object

---

## Experience Section

File: `src/content/homepage/experience.ts`

### Data Structure

```typescript
export interface Role {
  title: string;
  type: string; // "Full-time" | "Part-time" | "Freelance" | "Internship" | "Apprenticeship" | "Self-Employed"
  period: string; // "Mon YYYY - Mon YYYY" or "Mon YYYY - Present"
  bullets: string[];
}

export interface Job {
  company: string;
  location: string; // "City, Country (Remote)" or "City, Country"
  roles: Role[];
}
```

### Experience Workflow

First, use `AskUserQuestion` to ask what action to take:

- Add new experience
- Edit existing experience
- Remove experience

**Add Experience**: Use `AskUserQuestion` to gather company name, location, role details (title, type, period, bullets). Most recent jobs appear first in array.

**Edit Experience**: Use `AskUserQuestion` to select which company/role to edit (show numbered list from script output), then ask what to modify.

**Remove Experience**: Use `AskUserQuestion` to select which company to remove, then confirm deletion.

---

## Education Section

File: `src/content/homepage/education.ts`

### Data Structure

```typescript
export interface Education {
  institution: string;
  degree: string;
  gpa?: string;
  location: string;
  period: string; // "YYYY - YYYY"
}
```

### Education Workflow

Same workflow as Experience - use `AskUserQuestion` to ask what action (add/edit/remove), then gather details or select entries to modify.

---

## Skills Section

File: `src/content/homepage/skills.ts`

### Data Structure

```typescript
export interface SkillCategory {
  title: string;
  skills: string[];
}
```

### Skills Workflow

First, use `AskUserQuestion` to ask what action to take:

- Add new skill category
- Edit existing category
- Remove category

**Add Category**: Use `AskUserQuestion` to get category title, then gather initial skills list.

**Edit Category**: Use `AskUserQuestion` to select which category, then ask what to modify (rename, add skills, remove skills, reorder).

**Remove Category**: Use `AskUserQuestion` to select which category to remove, then confirm deletion.

---

## Content Guidelines

- Keep overview paragraph concise (3-5 sentences)
- Use action verbs for experience bullets ("Led", "Built", "Developed")
- Include quantifiable metrics where possible ("handled 300+ users")
- Order experience chronologically (most recent first)
- Group related skills in appropriate categories

## Resources

### scripts/

- `read_content.py` - Parses data files and outputs compact summary

### references/

- `data-schema.md` - TypeScript interfaces for all section data
