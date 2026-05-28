# artifact examples

validation artifacts by skill type. every improved skill must produce one.

## artifact checklist

minimum evidence for any artifact:

- concrete output (file, command log, or created component)
- evidence of applied values (timings, thresholds, constants)
- location or path to the artifact
- validation notes from consult thorough + consult quick

## domain skills

### emil-kowalski (UI/animation)

**artifact:** create a component using the skill's principles

```
created: ~/Developer/components/modal/
├── CLAUDE.md (decision tree, concrete values)
└── dialog.tsx (Radix Dialog with skill-defined animation)

validation points:
- entrance: 200ms, ease-out, scale(0.95->1)
- exit: 150ms, ease-in, fade only
- values match skill's concrete values table
```

**consult-light validation:**
```bash
cat <<'EOF' | copilot -p --model gemini-3-pro
Artifact validation for emil-kowalski skill.

Artifact: Modal component at ~/Developer/components/modal/
Principles applied:
- 200ms entrance (from skill's timing table)
- Scale from 0.95 (from skill's transform section)
- Fade-only exit (from skill's decision tree)

Questions:
1. Does this demonstrate restraint (not over-animated)?
2. Are timings from skill's primary sources?
3. Would Emil approve?

Output JSON: {"pass": bool, "score": 1-10, "confidence": 1-10}
EOF
```

### tdd-convex (testing)

**artifact:** write a test using the skill's patterns

```
created: packages/backend/convex/__tests__/new-feature.test.ts

validation points:
- uses convex-test patterns from skill
- follows red-green-refactor workflow
- test behavior not implementation
```

### design-system (components)

**artifact:** add a component using the updated design rules

```
created: ~/Developer/components/tabs/

validation points:
- spacing tokens match skill's concrete values
- interaction states follow decision tree
- new component documented in README
```

## tool skills

### slack (connections/)

**artifact:** run a workflow using skill patterns

```
executed: slack workspace audit for saya workspace

commands used:
- slack auth whoami -w saya
- slack channel list -w saya
- slack channel history -c general --limit 50 -w saya

validation points:
- used -w flag consistently (from skill's anti-patterns)
- used explicit subcommands (not bare search)
- followed multi-pass audit pattern
```

### imessage (connections/)

**artifact:** send a message using skill patterns

```
executed: messages send luke "test from skill validation"

validation points:
- used voice patterns from skill
- appropriate tone for recipient
- no emoji unless specified
```

### linear (connections/)

**artifact:** update an issue using skill workflow

```
executed: linear issue update for ABC-123

validation points:
- followed status transition rules
- included summary + next steps
- used correct team and project identifiers
```

## workflow skills

### loop (orchestration/)

**artifact:** execute one iteration on a real Linear issue

```
executed: loop iteration on ARB-123

steps completed:
1. detected project type (convex)
2. synced Linear state
3. ran consult-light for approach
4. executed flywheel-convex
5. checkpoint with consult-light

validation points:
- used appropriate flywheel for project type
- consulted before major decisions
- stayed within issue scope
```

### long-horizon (orchestration/)

**artifact:** complete a multi-step task autonomously

```
executed: multi-step feature implementation

phases completed:
1. init: gathered context
2. plan: created actionable steps
3. execute: implemented with TDD
4. review: consult-deep for architecture
5. finish: tests passing, PR ready

validation points:
- followed phase structure from skill
- used agentic review at appropriate points
- didn't abandon mid-task
```

### deep-work (orchestration/)

**artifact:** delegate a task to Codex successfully

```
executed: codex exec for refactoring task

validation points:
- prompt followed skill's structure
- monitored execution
- audited results before accepting
```

## meta skills

### skill-improve (meta/)

**artifact:** improve another skill using this skill

```
improved: consult-light skill

process:
1. self-eval: scored 6/10
2. gaps: missing decision tree for model selection
3. research: read copilot docs
4. rewrite: added model selection tree
5. consult-deep: depth_score 9/10
6. artifact: used improved skill for validation
7. consult-light: score 9/10

validation points:
- followed 7-step workflow exactly
- both consult-deep AND artifact required
- quality checklist completed
```

### create-skill (meta/)

**artifact:** create a new skill using this skill

```
created: new-skill-name/
├── SKILL.md
└── references/

validation points:
- followed skill anatomy from docs
- description uses third-person
- has decision tree and anti-patterns
```

### metaprompt-factory (meta/)

**artifact:** generate a metaprompt for a real task

```
created: metaprompts/code-review.xml

validation points:
- follows XML structure from skill
- variables are substitutable
- prompt is reusable
```

## review skills

### consult-light (review/)

**artifact:** run a consultation successfully

```
executed: copilot consultation

validation points:
- used stdin heredoc pattern
- model selection appropriate for task
- output was actionable
```

### consult-deep (review/)

**artifact:** run thorough review via Codex

```
executed: codex exec for architecture review

validation points:
- prompt included full context
- review was substantive
- recommendations were actionable
```

### pr-audit (review/)

**artifact:** audit a real PR

```
audited: PR #123 in project

validation points:
- checked security items from checklist
- verified test coverage
- provided pass/fail verdict
```

## validation template

```markdown
## artifact validation

**skill:** [skill_name]
**artifact type:** [component/workflow/task/skill]
**artifact location:** [path or description]

### principles applied

| principle | how applied | evidence |
|-----------|-------------|----------|
| [from skill] | [specific application] | [line/file/output] |

### consult-deep result

```json
{
  "pass": true,
  "depth_score": 9,
  "confidence": 9
}
```

### consult-light result

```json
{
  "pass": true,
  "score": 9,
  "confidence": 9
}
```

### verdict

- [ ] artifact demonstrates skill mastery
- [ ] principles correctly applied
- [ ] both validations passed
```

## artifact log template

```
Skill: [name]
Artifact: [path or description]
Date: [YYYY-MM-DD]

Evidence:
- values applied: [list]
- decision tree applied: [which branch]
- validation: consult-deep pass, consult-light pass
```
