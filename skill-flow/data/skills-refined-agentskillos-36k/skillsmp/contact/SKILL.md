---
name: contact
description: This skill should be used when managing contact information - updating email, social media links (LinkedIn, GitHub, Instagram), or location. It provides an interactive workflow for editing contact details stored in a TypeScript constants file.
---

# Contact Information Management

## Overview

Manage contact information for the portfolio website. Contact data is stored in a single TypeScript file at `src/lib/constants/contact.ts`. The contact page displays this information with icons and links.

## Data File

| Data                | File                           | Component                  |
| ------------------- | ------------------------------ | -------------------------- |
| Contact Information | `src/lib/constants/contact.ts` | `src/app/contact/page.tsx` |

## Workflow

### Step 1: Display Current State

Run the script to get a compact summary of current contact info:

```bash
python3 .claude/skills/contact/scripts/read_contact.py
```

For JSON output: `python3 .claude/skills/contact/scripts/read_contact.py json`

### Step 2: Present Options

Use the AskUserQuestion tool to ask what the user wants to update:

- **Email** - Update email address
- **LinkedIn** - Update LinkedIn profile URL
- **GitHub** - Update GitHub profile URL
- **Instagram** - Update Instagram profile URL
- **Location** - Update geographic location

---

## Contact Fields

File: `src/lib/constants/contact.ts`

### Data Structure

```typescript
export interface ContactInfo {
  email: string;
  linkedin: string;
  github: string;
  instagram: string;
  location: string;
}
```

### Edit Workflow

1. Display current contact info using the script
2. Ask which field(s) to edit using AskUserQuestion
3. Read the file to get current values
4. Get new value(s) from user
5. Update the `contactInfo` object

### Field-Specific Guidelines

**Email**:

- Plain email address without `mailto:` prefix
- Example: `"contact@example.com"`

**LinkedIn**:

- Full URL format: `https://www.linkedin.com/in/username/`
- Include trailing slash for consistency

**GitHub**:

- Full URL format: `https://github.com/username`
- No trailing slash

**Instagram**:

- Full URL format: `https://instagram.com/username`
- No trailing slash

**Location**:

- Geographic description (city, country, or region)
- Examples: `"Indonesia"`, `"San Francisco, USA"`, `"Remote"`

---

## Resources

### scripts/

- `read_contact.py` - Parses contact file and outputs compact summary

### references/

- `data-schema.md` - TypeScript interface and field descriptions
