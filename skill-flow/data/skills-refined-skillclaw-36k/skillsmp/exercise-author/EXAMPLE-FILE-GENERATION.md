# Example File Generation Guide

This document explains how the exercise-author skill automatically generates reference implementations in the `/examples/completed-config/` folder.

## Overview

When creating exercise files, the exercise-author skill now:

1. **Detects** when exercises ask users to create files
2. **Generates** complete reference implementations in `examples/completed-config/`
3. **Adds** "Compare Your Work" links to Success Criteria
4. **Maintains** consistency with existing example patterns

This gives learners:

- **Copy-paste scaffolding** to get started quickly
- **Reference implementations** to validate their work
- **Complete examples** showing best practices

---

## How It Works

### 1. File Detection

The skill scans exercise content for file creation patterns:

```markdown
**Step 2:** Create `.github/instructions/frontend.instructions.md`

**Step 3:** Add `docs/ARCHITECTURE.md` to document the project structure
```

It also checks the "Artifacts" column in the planning table.

### 2. Path Mapping

Files are mapped to `examples/completed-config/`:

| Exercise File Path                   | Example File Path                                              |
| ------------------------------------ | -------------------------------------------------------------- |
| `.github/copilot-instructions.md`    | `examples/completed-config/.github/copilot-instructions.md`    |
| `.github/skills/api-design/SKILL.md` | `examples/completed-config/.github/skills/api-design/SKILL.md` |
| `fanhub/docs/ARCHITECTURE.md`        | `examples/completed-config/docs/ARCHITECTURE.md`               |

**Note:** `fanhub/docs/` becomes just `docs/` in examples (no fanhub prefix).

### 3. Content Generation

Example files contain **complete, realistic implementations**:

✅ **Good:**

```markdown
<!-- Reference implementation for Module 1, Exercise 1.1: Repository Documentation -->
<!-- This example demonstrates: Project structure documentation for Copilot context -->

# FanHub Architecture

## Project Structure
```

fanhub/
├── frontend/ # React SPA for UI
│ ├── src/
│ │ ├── components/ # Reusable React components
│ │ ├── pages/ # Page-level components
│ │ └── api/ # API client utilities
├── backend/ # Express.js API
│ ├── src/
│ │ ├── routes/ # Express route handlers
│ │ ├── services/ # Business logic
│ │ └── models/ # Data models

```

## Technology Stack

- **Frontend:** React 18, React Router, Tailwind CSS
- **Backend:** Node.js, Express, PostgreSQL
```

❌ **Avoid:**

```markdown
# Architecture

[Add your architecture documentation here]

TODO: Document project structure
```

### 4. Multi-File Support

When exercises create multiple related files, all are generated:

```
examples/completed-config/
└── .github/
    └── skills/
        └── api-endpoint-design/
            ├── SKILL.md              # Main skill definition
            ├── openapi-schema.yaml   # OpenAPI spec
            └── example-endpoints/
                ├── get-character.js  # Example endpoint
                └── post-review.js    # Example endpoint
```

### 5. Compare Your Work Links

Automatically added to Success Criteria:

```markdown
#### ✅ Success Criteria

- [ ] File created at correct location
- [ ] Content follows standards
- [ ] Copilot suggestions improve

> 📂 **Compare Your Work**: [`examples/completed-config/.github/instructions/frontend.instructions.md`](../../examples/completed-config/.github/instructions/frontend.instructions.md)
```

---

## Content Guidelines

### Use FanHub Domain Context

All examples should reference the FanHub TV show fan site:

```markdown
# API Endpoint Design Skill

## Example Endpoints

### GET /api/characters/:id

Returns character details including:

- Character name and actor
- Show appearances
- Related characters
- Fan ratings

### POST /api/reviews

Submits fan review for episode:

- Show ID and episode number
- Rating (1-5 stars)
- Review text
```

### Include Inline Explanations

Help learners understand the "why" behind decisions:

````markdown
## Component Patterns

1. **Use custom hooks for API calls** — Separates data fetching from UI logic
   ```javascript
   // Custom hook centralizes character fetching
   function useFetchCharacters() {
     const [characters, setCharacters] = useState([]);
     // ... fetch logic
   }
   ```
````

```

### Match Module Progression

Later modules build on earlier ones:

- **Module 1:** Basic documentation (ARCHITECTURE.md)
- **Module 3:** Reusable prompts reference Module 1 patterns
- **Module 5:** Skills use terminology from Module 1 docs
- **Module 7:** Agents orchestrate earlier skills

---

## Validation Checklist

Before generating example files:

- [ ] Check if file already exists in `examples/completed-config/`
- [ ] Ensure content matches exercise learning objectives
- [ ] Use FanHub domain (not generic examples)
- [ ] Include inline explanations for key decisions
- [ ] Add metadata comments linking to source exercise
- [ ] Verify relative paths in Compare Your Work links
- [ ] Test that all cross-references between files work
- [ ] Maintain consistency with existing example patterns

---

## Examples by Module

### Module 1: Repository Instructions

**Exercise 1.1** creates `docs/ARCHITECTURE.md`
- **Example:** `examples/completed-config/docs/ARCHITECTURE.md`
- **Content:** Complete project structure, tech stack, architectural decisions
- **Demonstrates:** How to document for Copilot context

### Module 3: Custom Prompts

**Exercise 3.1** creates `.github/prompts/test-suite.prompt.md`
- **Example:** `examples/completed-config/.github/prompts/test-suite.prompt.md`
- **Content:** Reusable prompt for generating test suites
- **Demonstrates:** Prompt structure, variable usage, output format

### Module 5: Agent Skills

**Exercise 5.1** creates API design skill with multiple files
- **Examples:**
  - `examples/completed-config/.github/skills/api-endpoint-design/SKILL.md`
  - `examples/completed-config/.github/skills/api-endpoint-design/openapi-schema.yaml`
  - `examples/completed-config/.github/skills/api-endpoint-design/example-endpoints/get-character.js`
- **Demonstrates:** Multi-file skills, schema references, concrete examples

### Module 7: Custom Agents

**Exercise 7.2** creates `.github/agents/feature-plan.agent.md`
- **Example:** `examples/completed-config/.github/agents/feature-plan.agent.md`
- **Content:** Complete agent definition with instructions and context
- **Demonstrates:** Agent structure, skill integration, output format

---

## Troubleshooting

### Problem: Example file path is wrong

**Check:**
- Is the relative path calculation correct from module to examples?
- Did you strip `fanhub/` prefix for `fanhub/docs/` paths?
- Are you using `../../examples/` from module directories?

### Problem: Example content is too generic

**Fix:**
- Add FanHub-specific examples (characters, shows, episodes)
- Include persona names (Sarah, Marcus, David, Elena, Rafael)
- Reference actual FanHub features (character detail pages, episode reviews)

### Problem: Multi-file example has broken cross-references

**Fix:**
- Verify all files in the directory structure are created
- Check that relative paths between files are correct
- Test links by navigating the generated structure

---

## Future Enhancements

Potential improvements to consider:

1. **Automatic example file updates** — When exercise content changes, update corresponding examples
2. **Example file testing** — Validate that example files can be copied and work correctly
3. **Version tracking** — Track which module version generated each example
4. **Interactive diff tool** — Show learners what's different between their work and examples

---

## Related Documentation

- [SKILL.md](SKILL.md) — Main exercise-author skill documentation
- [TEMPLATE.md](TEMPLATE.md) — Exercise file template structure
- [examples/README.md](../../../examples/README.md) — Examples folder overview
```
