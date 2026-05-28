---
name: exercise-author
description: Reads a module's README.md, identifies missing exercise files from the planning table, and creates standalone exercise files using TEMPLATE.md format. Use when exercises are planned but not yet implemented as individual files.
infer: true
---

# Exercise Author Skill

You generate missing exercise files from a module's README.md planning table.

## When to Use This Skill

Invoke this skill when:

- A module README.md has an exercise planning table but missing exercise files
- User asks to "create missing exercises" or "generate exercise files"
- User points to a module directory and wants all planned exercises implemented

**Example invocations:**

- "@exercise-author create missing exercises for module 99"
- "Generate all exercise files for modules/10-agentic-sdlc/"
- "Look at module 5 and create any exercises that don't exist yet"

## How It Works

### Step 1: Read Module README.md

1. Locate the module directory (e.g., `modules/99-agent-skills-vscode/`)
2. Read the `README.md` file
3. Find the "📋 Exercise Planning Table" section
4. Parse each row to extract:
   - Exercise number (e.g., "99.1", "99.2")
   - Exercise filename from link (e.g., "exercise-01.md")
   - Exercise title
   - Lead persona
   - Support personas
   - Problem description with metrics
   - Solution description
   - Key metrics (before→after)
   - Artifacts created

### Step 2: Check Which Files Exist

For each exercise in the planning table:

1. Check if the file exists in the module directory
2. If the file exists, skip it
3. If the file is missing, add to creation list

### Step 3: Create Missing Exercise Files

For each missing exercise file:

1. **Use the TEMPLATE.md structure** from `.github/skills/exercise-author/TEMPLATE.md`

2. **Fill in the template with data from the planning table:**
   - Exercise number and title from table
   - Lead persona
   - Support personas
   - Problem metrics from "Problem" column
   - Solution approach from "Solution" column
   - Before/After metrics from "Key Metrics" column
   - Artifacts from "Artifacts" column

3. **Generate realistic content:**
   - 📖 The Challenge: 2-3 paragraphs showing the problem through persona lenses
   - 🔄 The Transformation: Table with Before/After scenarios using metrics from planning table
   - 🎯 Your Goal: Single sentence objective derived from solution
   - 📋 Steps: 3-4 detailed steps to implement the solution
   - ✅ Success Criteria: 3-4 checkboxes for verifiable outcomes
   - 📚 Official Docs: 2-3 relevant documentation links
   - 🔗 What You Built: List artifacts with purposes
   - ➡️ Next Up: Link to next exercise or module

4. **Create the file** at `modules/[module-dir]/[exercise-filename]`

## Important Guidelines

### Metrics Must Be Concrete

Every Before/After comparison must include:

- **Time metrics** (e.g., "45 minutes → 5 minutes")
- **Count metrics** (e.g., "12 violations → 0 violations")
- **Round/cycle metrics** (e.g., "3 review rounds → 1 round")

Use the metrics from the planning table's "Key Metrics" column.

### Persona Voice Authenticity

Write in the persona's voice (see `modules/00-orientation/PERSONAS.md`):

- **Sarah (Skeptical Senior)**: ROI-focused, validates with metrics, "I tested this by..."
- **David (Seasoned Architect)**: Expertise validation, AI amplifies experience
- **Marcus (DevOps Developer)**: Infrastructure focus, workflow friction removal
- **Elena (Quality Champion)**: Quality validation, edge case coverage
- **Rafael (Product Visionary)**: Business value, stakeholder communication

### File Structure

Each exercise file must:

1. Start with `# Exercise N.X: [Title]`
2. Include all sections from TEMPLATE.md
3. Use proper emoji vocabulary (📖, ❌, ✨, 🎯, 📋, ✅, 📚, 🔗, ➡️)
4. Have horizontal rules (`---`) between major sections
5. Reference artifacts created (from planning table's "Artifacts" column)

### Official Documentation Links

Prioritize documentation in this order:

1. VS Code Copilot docs (for editor features)
2. GitHub Docs (for Copilot concepts, best practices)
3. Microsoft Learn (for Azure/enterprise features if relevant)

Never use third-party blog posts as primary documentation.

### Example File Generation

**CRITICAL**: Whenever an exercise asks users to create a file, automatically generate a reference implementation in `examples/completed-config/` to provide copy-paste scaffolding and validation.

#### Detecting File Creation Instructions

Scan exercise content (especially Steps section) for patterns indicating file creation:

- "Create `.github/instructions/frontend.instructions.md`"
- "Add `docs/ARCHITECTURE.md`"
- "Create a new file at `path/to/file.ext`"
- "Set up `.github/agents/feature-plan.agent.md`"
- Artifacts listed in planning table's "Artifacts" column

#### Example File Location Mapping

Mirror the repository structure in `examples/completed-config/`:

| User Creates                                    | Example Location                                                          |
| ----------------------------------------------- | ------------------------------------------------------------------------- |
| `.github/copilot-instructions.md`               | `examples/completed-config/.github/copilot-instructions.md`               |
| `.github/instructions/frontend.instructions.md` | `examples/completed-config/.github/instructions/frontend.instructions.md` |
| `.github/prompts/test-suite.prompt.md`          | `examples/completed-config/.github/prompts/test-suite.prompt.md`          |
| `.github/skills/api-endpoint-design/SKILL.md`   | `examples/completed-config/.github/skills/api-endpoint-design/SKILL.md`   |
| `.github/agents/feature-plan.agent.md`          | `examples/completed-config/.github/agents/feature-plan.agent.md`          |
| `.github/hooks/security.json`                   | `examples/completed-config/hooks/security.json`                           |
| `fanhub/docs/ARCHITECTURE.md`                   | `examples/completed-config/docs/ARCHITECTURE.md`                          |

**Note:** `.github/` maps to `examples/completed-config/.github/` but `fanhub/docs/` maps to `examples/completed-config/docs/` (no fanhub prefix).

#### Example Content Generation Guidelines

Create **complete, realistic implementations** that:

1. **Match the exercise's learning objectives** — Demonstrate the exact technique being taught
2. **Use persona-specific scenarios** — Reference FanHub domain (TV shows, characters, episodes)
3. **Include inline explanations** — Add comments/notes explaining key decisions
4. **Show concrete patterns** — No placeholders like `[YOUR CODE HERE]` or `TODO: implement`
5. **Reflect module progression** — Later modules build on earlier artifacts

**Content quality examples:**

✅ **Good example content:**

````markdown
# Frontend Instructions

## React Component Patterns

All React components in FanHub must follow these standards:

1. **Functional components with hooks** — No class components
   - Use `useState` for local state
   - Use `useEffect` for side effects
   - Use custom hooks for shared logic (e.g., `useFetchCharacters`)

2. **Props destructuring** — Always destructure props in component signature

   ```jsx
   // ✅ Good
   function CharacterCard({ name, actor, imageUrl }) { ... }

   // ❌ Avoid
   function CharacterCard(props) { const name = props.name; ... }
   ```
````

````

❌ **Avoid placeholder content:**
```markdown
# Frontend Instructions

## Component Guidelines

[Add your component guidelines here]

TODO: Document React patterns
````

#### Multi-File Examples

When exercises create multiple related files (e.g., skills with schemas + examples, hooks with JSON + scripts):

1. **Generate complete directory structures** — Create all subdirectories and files
2. **Ensure cross-references work** — Relative paths between files must be correct
3. **Maintain consistency** — Use the same naming/structure conventions

**Example:** Module 5 (Agent Skills) creates:

- `examples/completed-config/.github/skills/api-endpoint-design/SKILL.md`
- `examples/completed-config/.github/skills/api-endpoint-design/openapi-schema.yaml`
- `examples/completed-config/.github/skills/api-endpoint-design/example-endpoints/get-character.js`
- `examples/completed-config/.github/skills/api-endpoint-design/example-endpoints/post-review.js`

#### Auto-Insert Compare Your Work Section

When exercises involve file creation, automatically add this to the Success Criteria section:

```markdown
> 📂 **Compare Your Work**: [`examples/completed-config/{relative-path}`](../../examples/completed-config/{relative-path})
```

**Path calculation rules:**

- Use relative path from module directory to examples folder (typically `../../examples/`)
- Include the full path within `completed-config/`
- Link text should show the path for clarity

**Examples:**

- Module 1 → Module 5: `../../examples/completed-config/.github/skills/api-endpoint-design/SKILL.md`
- Module 10 → hooks: `../../examples/completed-config/hooks/security.json`

#### Example File Metadata

Add frontmatter comments to generated example files linking back to source exercise:

```markdown
<!-- Reference implementation for Module X, Exercise X.Y: [Title] -->
<!-- This example demonstrates: [brief description of what's being taught] -->

[Actual content starts here]
```

#### Validation Against Existing Examples

Before creating new example files:

1. **Check if file already exists** in `examples/completed-config/`
2. **If exists, verify it matches exercise intent** — Update if needed
3. **If missing, generate new file** — Follow existing formatting patterns
4. **Cross-reference related examples** — Ensure consistency with existing artifacts

Examine [examples/completed-config/](../../../examples/completed-config/) structure to maintain:

- Consistent formatting (Markdown style, YAML structure, code conventions)
- Appropriate depth (comprehensive but not overwhelming)
- Domain context (FanHub TV show site, not generic examples)

## Example Workflow

User says: "@exercise-author create missing exercises for module 99"

You:

1. Read `modules/99-agent-skills-vscode/README.md`
2. Parse exercise planning table
3. Check which files exist:
   - `exercise-01.md` ✅ exists
   - `exercise-02.md` ❌ missing
   - `exercise-03.md` ❌ missing
4. Create `modules/99-agent-skills-vscode/exercise-02.md` using planning table data + TEMPLATE.md structure
5. **Detect file creation instructions** in exercise-02.md:
   - Step 2 says "Create `.github/skills/bug-analyzer/SKILL.md`"
   - Artifacts list includes `.github/skills/bug-analyzer/examples/sample-bug.js`
6. **Generate example files**:
   - Create `examples/completed-config/.github/skills/bug-analyzer/SKILL.md` with complete skill definition
   - Create `examples/completed-config/.github/skills/bug-analyzer/examples/sample-bug.js` with realistic bug example
   - Add metadata comments linking back to Module 99, Exercise 2
7. **Add Compare Your Work section** to exercise-02.md Success Criteria:
   ```markdown
   > 📂 **Compare Your Work**: [`examples/completed-config/.github/skills/bug-analyzer/SKILL.md`](../../examples/completed-config/.github/skills/bug-analyzer/SKILL.md)
   ```
8. Create `modules/99-agent-skills-vscode/exercise-03.md` (repeat steps 5-7)
9. Report: "Created 2 missing exercises and 3 example files: exercise-02.md, exercise-03.md, and reference implementations in examples/completed-config/"

## Quality Checklist

Before creating each file, verify:

- [ ] All metrics from planning table are included
- [ ] Lead and support personas match the table
- [ ] Steps are actionable (commands, paths, expected results)
- [ ] Success criteria are verifiable checkboxes
- [ ] Artifacts listed in planning table appear in "What You Built"
- [ ] Official docs links are first-party (GitHub, VS Code, Microsoft)
- [ ] Persona voice is authentic to their background
- [ ] Before/After transformation shows measurable improvement
- [ ] **Example files generated** for all artifacts users create
- [ ] **Compare Your Work sections** added when files are created
- [ ] **Example content is complete** (no placeholders or TODOs)
- [ ] **Example paths are correct** (verified relative links work)

## Related Skills

- **exercise-author**: Creates individual exercises from scratch with user guidance
- **module-author**: Creates entire module README.md with exercise planning table

Use this skill when the planning is done (exercise table exists) but implementation is missing.
