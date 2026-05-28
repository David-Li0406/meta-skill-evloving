---
name: ui-ux-prototype-prompt-generator
description: Use this skill when you need to generate detailed, structured prompts for creating UI/UX prototypes across various design systems, ensuring comprehensive design documentation for web and mobile applications.
---

# UI/UX Prototype Prompt Generator

Generate comprehensive, structured prompts for creating production-ready UI/UX prototypes with detailed specifications and design system adherence.

## When to Use This Skill

Use this skill when:
- Creating detailed design briefs for web or mobile applications
- Generating structured prompts for AI-assisted UI design
- Documenting UI specifications across multiple design systems
- Building design handoff documentation for development teams
- Prototyping mobile apps with specific design system constraints
- Generating comprehensive design documentation from high-level concepts

**Trigger phrases:**
- "Create a prototype prompt for [app description]"
- "Design a mobile app for [use case]"
- "Generate UI specifications for [feature]"
- "Build a design brief for [application type]"
- "Create design documentation for [platform]"

## Supported Design Systems

This skill generates prompts compatible with:

| Design System | Platform | Best For |
|---------------|----------|----------|
| **WeChat Work** | Enterprise messaging | Internal enterprise apps, workflow tools |
| **iOS Native (HIG)** | Apple platforms | Consumer iOS apps, native experiences |
| **Material Design 3** | Android, Web | Cross-platform apps, Google ecosystem |
| **Ant Design Mobile** | Mobile web, Hybrid | Admin panels, data-heavy mobile apps |

**Automatic adaptation**: Prompts adjust component names, interaction patterns, and visual styles based on selected design system.

## Prompt Generation Process

### Step 1: Gather Requirements

Extract from user input:
- **Application type** (e.g., task manager, e-commerce, social app)
- **Target platform** (iOS, Android, Web, Hybrid)
- **Design system preference** (if specified)
- **Key features** (user flows, core functionality)
- **Target audience** (demographic, use case context)

### Step 2: Structure the Prompt

Generate a comprehensive prompt with these sections:

1. **Project Overview** - App purpose, target users, core value proposition
2. **Design System Specification** - Selected system and adherence requirements
3. **Page/Screen List** - Complete navigation structure
4. **Detailed Specifications** - Per-screen component breakdown:
   - Layout structure
   - Component hierarchy
   - Interaction states
   - Visual styling (colors, typography, spacing)
   - Accessibility requirements
5. **User Flows** - Critical paths and interactions
6. **Edge Cases** - Empty states, error handling, loading states
7. **Responsive Behavior** - Breakpoints and adaptive layouts (for web)
8. **Design Tokens** - Colors, typography scales, spacing system

### Step 3: Output Structured Documentation

Deliver in Markdown format with:
- Clear section hierarchy (H2, H3 headings)
- Tables for component specifications
- Code blocks for design tokens
- ASCII diagrams for layouts (when helpful)

## Best Practices

### For High-Quality Prompts

1. **Be specific about target users**
   - Good: "25-35 year old professionals managing personal tasks"
   - Bad: "Anyone who needs a task manager"

2. **Specify design constraints**
   - Good: "iOS app following HIG, accessibility priority"
   - Bad: "Mobile app"

3. **Clarify feature priorities**
   - Good: "Core: task list, categories, quick add. Future: collaboration, attachments"
   - Bad: "Task manager with all features"

4. **Indicate technical constraints**
   - Mention if it's a web app (responsive required)
   - Note if it's a native app (platform-specific components)
   - Specify if hybrid (framework limitations)

## Common Patterns

### Pattern 1: Enterprise Work Dashboard (WeChat Work Style)
**Typical Structure:**
- Top navigation bar (44px, title + search/menu icons)
- Quick access grid (4-column icon grid)
- Data summary cards (key metrics in horizontal layout)
- Feature list (icon + text rows, 64px height each)
- Bottom tab bar (5 tabs, 50px height)

### Pattern 2: iOS Consumer App (iOS Native Style)
**Typical Structure:**
- Large title navigation bar (96px when expanded)
- Card-based content sections
- System standard lists (44px minimum row height)
- Tab bar with SF Symbols icons

### Pattern 3: Android App (Material Design Style)
**Typical Structure:**
- Top app bar (56px on mobile, 64px on tablet)
- FAB (Floating Action Button) for primary action
- Card-based content with elevation
- Bottom navigation or navigation drawer

### Pattern 4: Enterprise Form App (Ant Design Mobile)
**Typical Structure:**
- Simple navigation bar (45px)
- Form sections with grouped inputs
- List views with detailed information
- Fixed bottom action bar with primary button

## Troubleshooting

**Issue: User requirements are too vague**
**Solution:** Ask focused questions, provide examples of similar apps, suggest design systems to choose from, or create a default prompt and offer iteration.

**Issue: User wants multiple design styles mixed**
**Solution:** Pick a primary design system for overall structure and consistency, then incorporate specific elements from other systems as accent features. Explain trade-offs.

## Additional Resources

### Reference Files

Detailed documentation for design system specifications:
- **[references/design-systems.md](references/design-systems.md)** - Complete design system guide
  - Component libraries
  - Visual styles
  - Interaction patterns
  - Platform-specific guidelines

### Example Templates

Working prompt examples for common app types:
- **[examples/prompt-templates.md](examples/prompt-templates.md)** - Template library
  - Task manager (iOS Native)
  - Enterprise dashboard (WeChat Work)
  - E-commerce app (Material Design 3)
  - Admin panel (Ant Design Mobile)
  - Social app (Cross-platform)

---

**Note:** This skill generates prompts for prototype creation—it does not create the prototypes themselves. The output is a comprehensive text prompt that can be provided to another AI tool, developer, or design tool to generate the actual HTML/CSS/React code.