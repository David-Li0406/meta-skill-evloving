# Skill Review Guidelines
*Quality Assurance for ASE Skills*

**Purpose**: This guide helps you review and improve the quality of ASE skills. It is based on the "Skill Reviewer" agent pattern.

## Review Process

### 1. Structural Validation
- [ ] **Frontmatter**: Does `SKILL.md` have valid YAML frontmatter with `name` and `description`?
- [ ] **Naming**: Is the name kebab-case? (e.g., `intelligent-code-review`)
- [ ] **Directory**: Does it follow `skill-name/SKILL.md` structure?
- [ ] **Resources**: Are heavy docs moved to `resources/`?

### 2. Trigger Effectiveness (Critical!)
- [ ] **Use Case Driven**: Does description answer "When should I use this?"
- [ ] **Specific Keywords**: Are `intent_keywords` in `registry.json` distinct?
- [ ] **No Overlap**: Do keywords overlap with other global skills?
- [ ] **Examples**: Does description list 2-3 explicit example user queries?

### 3. Progressive Disclosure Check
- [ ] **SKILL.md Length**: Is it < 500 lines?
- [ ] **Separation**: Are "Concepts" and "Deep Dives" in `resources/`?
- [ ] **Links**: Do links in `SKILL.md` correctly point to resource files?

### 4. Content Quality
- [ ] **Imperative Tone**: Use "Use this to..." instead of "You should use this to..."
- [ ] **Actionable**: Does it tell the Agent *how* to think/act, not just *what* things are?
- [ ] **Personas**: If complex, does it use Personas (Multi-Agent routing) pattern?

## Common Anti-Patterns
- **Generic descriptions**: "Helps with coding." (Too broad, will trigger everywhere)
- **Missing registry**: Created file but forgot `registry.json`.
- **Broken links**: Referencing `../resources` incorrectly.
- **Huge SKILL.md**: Dumping 5000 lines of docs into the main file.
