---
name: dev-swarm-stage-ux
description: Design the user experience including visual design system, wireframes, user flows, responsive guidelines, and accessibility requirements. Use when starting stage 05 (ux) or when user asks about UI design, wireframes, or design system.
---

# Stage 05 - UX Design

Design the user experience including visual design system, wireframes, user flows, responsive guidelines, and accessibility requirements to create a cohesive and user-centered product interface.

## When to Use This Skill

- User asks to start stage 05 (ux)
- User wants to create wireframes or design system
- User asks about UI design, accessibility, or responsive design

## Your Roles in This Skill

See `dev-swarm/docs/general-dev-stage-rule.md` for role selection guidance.

## Role Communication

See `dev-swarm/docs/general-dev-stage-rule.md` for the required role announcement format.

## Pre-Stage Check

Before starting, verify previous stages:

1. Check if `00-init-ideas/` through `04-prd/` folders have content (not just `.gitkeep`)
2. If any previous stage is empty and has no `SKIP.md`:
   - Ask user: "Stage {XX} is not complete. Would you like to skip it or start from that stage first?"

## Instructions

### Step 1: Context Review

Read all files to understand the project:

- `ideas.md`
- `00-init-ideas/*.md` through `04-prd/*.md` - All markdown files

### Step 2: Create Stage Proposal

**General Rules:** See `dev-swarm/docs/general-dev-stage-rule.md` → "Create Stage Proposal Rules" section.

If this stage is skipped (has SKIP.md), execute the next non-skipped stage's agent skill. Otherwise, create the file `05-ux/README.md` with the following content:

#### 2.1 Stage Goal

Brief the goal in 2-3 paragraphs:
- What this stage aims to achieve
- Why UX design is critical for product success and user adoption
- How this builds upon previous stages (personas, MVP scope, PRD)
- What deliverables will be produced

#### 2.2 File Selection

Select files from these options based on project needs:

**Design System:**
- `design-system-guide.md` - Color palette, typography, spacing, and button styles
- `design-ui-preview.html` - Sample HTML/CSS/JS page demonstrating the design system

**Wireframes & Layouts:**
- `wireframe_descriptions.md` - Textual descriptions of UI layout for each key screen

**User Flows & Navigation:**
- `user-flows/` - User navigation flow diagrams

**Responsive & Accessibility:**
- `responsive-design.md` - Guidelines for how UI adapts across screen sizes
- `accessibility.md` - Accessibility requirements following WCAG guidelines

For each selected file, provide:
- Short description
- Why it's essential for this project
- Key information it should include

#### 2.3 Request User Approval

Ask user: "Please check the Stage Proposal in `05-ux/README.md`. Update it directly or tell me how to update it."

### Step 3: Execute Stage Plan

Once user approves `05-ux/README.md`:

#### 3.1 Create All Planned Files

Create each file listed in the approved README:

- **For `.md` files:** Write comprehensive content based on personas, MVP requirements, and PRD
- **For diagram folders:** Follow `dev-swarm/docs/mermaid-diagram-guide.md` to create related diagrams files
- **For `.html` files:** Create functional preview pages demonstrating the design system with css/js as needed

**Quality Guidelines:**
- Base design decisions on user personas and their needs
- Align UX with MVP features defined in stage 03
- Ensure all user flows support functional requirements from stage 04
- Accessibility must meet WCAG 2.1 AA standards at minimum

#### 3.2 Request User Approval for Files

After creating all files:
- Provide a summary of what was created
- Highlight key design decisions and rationale
- Ask: "Please review the UX design files. You can update or delete files, or let me know how to modify them."

### Step 4: Finalize Stage

Once user approves all files:

#### 4.1 Documentation Finalization
- Sync `05-ux/README.md` to remove any deleted files
- Ensure all files are complete and well-formatted
- Check that all diagrams render correctly
- Validate HTML preview displays correctly

#### 4.2 Prepare for Next Stage
- Summarize key design decisions for reference in architecture stage
- Note any technical constraints discovered during UX design

#### 4.3 Announce Completion

Inform user:
- "Stage 05 (UX Design) is complete"
- Summary of deliverables created
- Key design decisions made
- "Ready to proceed to Stage 06 (Architecture) when you are"

## Stage Completion Rules

See `dev-swarm/docs/general-dev-stage-rule.md` for stage completion, commit, and skip rules.

## Key Principles

- Base design on user personas and needs
- Ensure accessibility compliance
- Keep design consistent across all screens
- Support smooth transition to architecture design
