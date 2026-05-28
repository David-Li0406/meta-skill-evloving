---
name: create-area
description: Create PARA area notes for ongoing life responsibilities. Validates that the concept is truly an area (ongoing, no end date) rather than a project. Use when establishing new life domains or responsibilities to track.
allowed-tools: AskUserQuestion, mcp__plugin_para-obsidian_para-obsidian__para_create, mcp__plugin_para-obsidian_para-obsidian__para_list_areas, mcp__plugin_para-obsidian_para-obsidian__para_template_fields, mcp__plugin_para-obsidian_para-obsidian__para_config
---

# Create Area

Create PARA-compliant area notes for ongoing life responsibilities through collaborative dialogue.

## Core Philosophy

**From Tiago Forte's PARA Method:**

- **Area** = Standard to maintain over time. Continuous, no end date.
- **Areas map to roles** you play in life (parent, homeowner, professional).
- **Areas generate projects** - they're the "why" behind your projects.
- **Never "done"** - you maintain standards, not complete tasks.

## Critical Rules

1. **ALWAYS load existing areas first** - Prevent duplicates
2. **Validate it's truly an area** - If it has an end state, it's a project
3. **Areas have standards, not goals** - "Maintain health" vs "Lose 10kg"
4. **Keep areas broad** - 5-10 areas cover most of life
5. **Areas need routines** - What recurring activities maintain this area?

## Workflow Overview

```
Phase 0: Load Existing Areas (prevent duplicates)
    ↓
Phase 1: Gather Intent
    ├── What responsibility/domain?
    └── Validate it's ongoing (no end date)
    ↓
Phase 2: Define Standards (optional but recommended)
    ├── What standards to maintain?
    └── What routines support this area?
    ↓
Phase 3: Confirm & Create
```

---

## Phase 0: Load Existing Areas

**ALWAYS fetch existing areas first:**

```
para_list_areas({ response_format: "json" })
```

Use this to:
- Prevent creating duplicate areas
- Suggest if similar area already exists
- Show user their current life structure

---

## Phase 1: Gather Intent

### 1.1 Understand the Responsibility

If not provided in initial message, ask:

```
I'll help you create a new area. Areas are ongoing responsibilities - the
"departments" of your life that need continuous attention.

**What life responsibility or domain is this?**

Examples:
- 🏡 Home - Household maintenance and improvements
- 🏃 Health - Physical and mental wellness
- 💼 Career - Professional growth and work
- 👨‍👩‍👧 Family - Family relationships and care
- 💰 Finance - Money management and planning
```

### 1.2 Validate It's an Area (Not a Project)

**Key test:** Does it have an end state?

| User Says | Type | Action |
|-----------|------|--------|
| "Manage my health" | Area ✅ | Continue |
| "Lose 10kg" | Project ❌ | Suggest project instead |
| "Home maintenance" | Area ✅ | Continue |
| "Renovate kitchen" | Project ❌ | Suggest project instead |
| "Learn Spanish" | Ambiguous | Ask: ongoing skill or specific goal? |

If user describes something with an end state:

```
That sounds more like a **Project** (specific goal with end state) than an
**Area** (ongoing responsibility).

Would you like to:
1. **Create a project instead** - For "Lose 10kg" with a target date
2. **Reframe as an area** - "Health" is the area, weight loss is a project within it
3. **Continue as area** - If you see this as truly ongoing
```

### 1.3 Check for Duplicates

If similar area exists:

```
I notice you already have [[🏡 Home]] as an area.

Is this new area:
1. **Different enough** to be separate? (tell me how)
2. **Should merge** into the existing area?
3. **A project** within that area instead?
```

---

## Phase 2: Define Standards (Optional)

This phase helps create meaningful areas, but can be skipped for quick creation.

### 2.1 Standards to Maintain

```
Areas are defined by the standards you want to maintain.

**What standards matter for this area?**

Examples for "Health":
- [ ] Exercise 3x per week
- [ ] Annual checkup completed
- [ ] Sleep 7+ hours most nights

(Type your standards, or "skip" to add later)
```

### 2.2 Supporting Routines

```
**What routines help maintain this area?**

| Frequency | Example |
|-----------|---------|
| Daily | Morning walk, medication |
| Weekly | Meal prep, gym sessions |
| Monthly | Budget review, date night |

(Type your routines, or "skip" to add later)
```

---

## Phase 3: Confirm & Create

### 3.1 Present Proposal

```
## Area Proposal

**Title:** 🌱 [Area Name]
**Type:** Ongoing responsibility
**Status:** active

### Standards to Maintain
- [ ] [Standard 1]
- [ ] [Standard 2]
- [ ] [Standard 3]
(or "To be defined" if skipped)

### Routines
- **Daily:** [routine or "—"]
- **Weekly:** [routine or "—"]
- **Monthly:** [routine or "—"]

---

**Ready to create?** (yes / tell me what to change)
```

### 3.2 Create Area Note

```
para_create({
  template: "area",
  title: "[Area name without emoji - template adds 🌱]",
  dest: "02 Areas",
  args: {
    "Status (active/inactive)": "active"
  },
  content: {
    "Description": "[What this area encompasses]",
    "Standards to Maintain": "[Checklist from Phase 2.1]",
    "Routines & Habits": "[Routines from Phase 2.2]"
  },
  response_format: "json"
})
```

### 3.3 Confirm Creation

```
Created: 🌱 [Area Name].md → 02 Areas

This area is now ready to:
- Track projects that serve this responsibility
- Hold resources related to this domain
- Guide your weekly reviews

Would you like to:
1. **Create a project** within this area
2. **Add more standards** to maintain
3. **Done** - Area is ready
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Duplicate area name | Suggest merge or differentiate |
| Sounds like a project | Offer to create project instead |
| Too narrow scope | Suggest broader area name |
| Area creation fails | Show error, preserve user input |

---

## Example Interaction

```
User: /para-obsidian:create-area

AI: I'll help you create a new area. Let me check your existing areas first.

    Your current areas:
    - 🎹 Movie Love
    - 🏠 Property
    - 🏡 Home
    - 🐶 Pet - Muffin
    - 📝 Note Taking
    - 🔧 Dotfiles
    - 🤖 AI Practice

    What life responsibility or domain do you want to track?

User: I want to manage my career development and professional growth

AI: Great! "Career" is a classic area - ongoing professional responsibility.

    What standards do you want to maintain? Examples:
    - [ ] Stay current with industry trends
    - [ ] Attend 2+ conferences per year
    - [ ] Maintain professional network

    (Type yours, or "skip" to add later)

User: skip for now

AI: No problem. Any routines that support your career?
    - Daily: Learning time?
    - Weekly: Networking?
    - Monthly: Skill review?

    (Type yours, or "skip")

User: Weekly learning - 2 hours on Fridays

AI: ## Area Proposal

    **Title:** 🌱 Career
    **Type:** Ongoing responsibility
    **Status:** active

    ### Standards to Maintain
    - To be defined

    ### Routines
    - **Weekly:** 2 hours learning on Fridays

    ---

    **Ready to create?** (yes / tell me what to change)

User: yes

AI: Created: 🌱 Career.md → 02 Areas

    Would you like to create a project within this area?
```

---

## Area Examples (Reference)

Common areas that cover most of life:

| Area | Covers |
|------|--------|
| 🏡 Home | Household, maintenance, improvements |
| 🏃 Health | Physical, mental, medical |
| 💼 Career | Work, professional development |
| 💰 Finance | Budget, investments, taxes |
| 👨‍👩‍👧 Family | Relationships, parenting, care |
| 🎓 Learning | Education, skills, growth |
| 🎨 Hobbies | Creative pursuits, recreation |
| 🤝 Social | Friendships, community, networking |

**Guideline:** Most people need 5-10 areas. More than 15 suggests over-categorization.
